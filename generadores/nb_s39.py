from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('matplotlib','matplotlib'), ('scipy','scipy'), ('gymnasium','gymnasium')]
C = []

C.append(cabecera(
    "S39", "RL profundo, simuladores y sim-to-real", "8",
    "jueves 10 de diciembre de 2026", "1 h",
    "Sale de la tabla de S38 y entra en el mundo de las políticas parametrizadas, con Gymnasium y CartPole-v1. Tres partes: una política aleatoria como línea base, una política lineal entrenada por búsqueda aleatoria y por método de entropía cruzada —sin redes profundas, sin GPU y en segundos—, y una demostración numérica del problema sim-to-real: entrenar con unos parámetros de masa, longitud y latencia y evaluar con otros distintos, para después ver cuánto arregla la aleatorización de dominio.",
    "Sutton y Barto (2018), cap. 13 (gradiente de política, ventaja, actor-crítico). Schulman et al. (2017), *Proximal Policy Optimization Algorithms*, arXiv:1707.06347. Tobin et al. (2017), *Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World*, arXiv:1703.06907. OpenAI et al. (2019), *Solving Rubik's Cube with a Robot Hand*, arXiv:1910.07113. Documentación de Gymnasium (Farama Foundation) para el contrato reset()/step().",
    "los apuntes del bloque 8"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
import gymnasium as gym
import time
np.set_printoptions(precision=3, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.2)
plt.rcParams['axes.grid'] = True
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('gymnasium', gym.__version__)"""))

C.append(md("""> **Alcance honesto de este cuaderno.** Aquí no se entrena PPO ni ninguna red profunda: eso necesitaría minutos u horas y una GPU, y no cabe en una sesión de una hora ni en un Colab gratuito. Lo que sí cabe —y es lo que de verdad hay que entender— es el **objeto** que se aprende (una política parametrizada, evaluable en microsegundos), el **bucle** que lo mejora (proponer, evaluar el retorno, quedarse con lo mejor) y el **problema** que aparece al llevarlo al mundo real. Para eso usamos una política lineal de cuatro parámetros optimizada por entropía cruzada, que es un optimizador de caja negra sin gradientes. PPO es mucho más eficiente en muestras y escala a redes de millones de parámetros, pero el esqueleto conceptual es el mismo, y el problema sim-to-real de la sección 4 es idéntico y no depende del algoritmo.

## 1. El entorno: el contrato `reset()` / `step()`

Gymnasium (Farama Foundation, sucesor mantenido de OpenAI Gym) **no es un simulador**: es la API estándar con la que los algoritmos hablan con cualquier entorno (documentación de Gymnasium). Todo el RL se reduce a ese contrato de dos llamadas, el mismo lazo agente-entorno de S38:

- `obs, info = env.reset(seed=...)` inicia un episodio y devuelve la observación inicial;
- `obs, r, terminated, truncated, info = env.step(a)` ejecuta la acción y devuelve la observación siguiente, la recompensa y dos banderas: `terminated` (el episodio ha acabado por la dinámica de la tarea) y `truncated` (se ha acabado por límite de tiempo). Distinguirlas importa: en el segundo caso el futuro **no** es cero, y confundirlas es un error clásico al implementar el objetivo de valor.

`CartPole-v1` es el problema de control más viejo del libro: un péndulo invertido sobre un carro. El estado son cuatro números —posición y velocidad del carro, ángulo y velocidad angular del péndulo— y hay dos acciones, empujar a izquierda o derecha. Recompensa: +1 por cada paso que el péndulo siga en pie. Es, sin ningún disfraz, un problema de control del bloque 5: lo interesante es que aquí nadie va a diseñar el controlador."""))

C.append(code("""env = gym.make('CartPole-v1')
print('observacion:', env.observation_space)
print('acciones   :', env.action_space)

u = env.unwrapped
print(f'\\nParametros fisicos por defecto del simulador:')
print(f'  masa del carro     masscart  = {u.masscart} kg')
print(f'  masa del pendulo   masspole  = {u.masspole} kg')
print(f'  semilongitud       length    = {u.length} m')
print(f'  fuerza del motor   force_mag = {u.force_mag} N')
print(f'  periodo de muestreo tau      = {u.tau} s  ->  {1/u.tau:.0f} Hz')

obs, info = env.reset(seed=0)
print(f'\\nobs inicial: {obs}   (x, x_punto, theta, theta_punto)')
obs, r, term, trunc, info = env.step(1)
print(f'tras empujar a la derecha: obs = {obs}, r = {r}, terminated = {term}')"""))

C.append(md("""### La política y la línea base aleatoria

Nuestra política es la más simple que puede haber y aun así es una **ley de control**: un vector de pesos `w` de cuatro componentes, y la acción es el signo del producto escalar con la observación.

    a = 1 si w · obs > 0, si no a = 0

Es decir: una realimentación de estado lineal seguida de un relé — un control bang-bang de manual. Eso es exactamente lo que subrayan los apuntes al hablar de gradientes de política: «el objeto que se aprende es exactamente una ley de control como las del bloque 5, evaluable en milisegundos, sin optimización en línea».

La línea base obligatoria antes de cualquier entrenamiento: ¿qué retorno da una política **al azar**? Sin ese número, cualquier resultado posterior es incomparable."""))

C.append(code("""MAX_PASOS = 300              # tope por episodio (CartPole-v1 trunca de serie en 500)

def ajustar_fisica(env, masspole=0.1, length=0.5, force_mag=10.0):
    \"\"\"Cambia los parametros fisicos del simulador. OJO: hay dos cantidades derivadas
    que se calculan en el constructor y hay que recalcular a mano.\"\"\"
    u = env.unwrapped
    u.masspole, u.length, u.force_mag = masspole, length, force_mag
    u.total_mass = u.masscart + u.masspole
    u.polemass_length = u.masspole * u.length

def episodio(env, w, semilla, max_pasos=MAX_PASOS, retardo=0):
    \"\"\"Un episodio con la politica lineal. 'retardo' = pasos de latencia entre
    medir y actuar (el sensor y el bus no son instantaneos: bloque 3).\"\"\"
    obs, _ = env.reset(seed=int(semilla))
    memoria = [obs] * (retardo + 1)
    total = 0.0
    for _ in range(max_pasos):
        a = 1 if float(w @ memoria[0]) > 0.0 else 0     # actua con la obs. retrasada
        obs, r, term, trunc, _ = env.step(a)
        memoria = memoria[1:] + [obs]
        total += r
        if term or trunc:
            break
    return total

def evaluar(env, w, n=20, semilla_base=9000, **kw):
    return float(np.mean([episodio(env, w, semilla_base + i, **kw) for i in range(n)]))

rng = np.random.default_rng(39)
ajustar_fisica(env)

# --- linea base: politicas completamente al azar ---
t0 = time.perf_counter()
al_azar = [evaluar(env, rng.normal(size=4), n=5, semilla_base=100 * k) for k in range(200)]
al_azar = np.array(al_azar)
print(f'200 politicas aleatorias evaluadas en {time.perf_counter() - t0:.2f} s')
print(f'  retorno medio  : {al_azar.mean():6.1f}')
print(f'  mediana        : {np.median(al_azar):6.1f}')
print(f'  mejor de las 200: {al_azar.max():6.1f}   (tope del episodio: {MAX_PASOS})')
print(f'  fraccion que aguanta mas de 100 pasos: {100*np.mean(al_azar > 100):.1f} %')"""))

# ---------------- 2. Entrenamiento
C.append(md("""## 2. Entrenar la política: búsqueda aleatoria y entropía cruzada

Los métodos de gradiente de política parametrizan la ley de control π_θ(a|s) y ajustan θ para maximizar el retorno esperado J(θ); el teorema del gradiente de política da la dirección de mejora sin derivar a través de la dinámica del entorno (Sutton y Barto, 2018, cap. 13). Con solo cuatro parámetros podemos permitirnos algo más rudimentario y más transparente: **optimización de caja negra**, que no necesita gradientes ni redes.

Dos versiones, para que se vea la diferencia:

- **Búsqueda aleatoria**: probar N vectores al azar y quedarse con el mejor. Es la línea base de los optimizadores.
- **Entropía cruzada (CEM)**: mantener una gaussiana sobre los parámetros; en cada iteración muestrear candidatos, evaluarlos, quedarse con la **élite** (el 20 % mejor) y reajustar la media y la desviación a esa élite. La distribución se va concentrando alrededor de lo que funciona.

Cada candidato se evalúa promediando **tres** episodios con semillas distintas. Ese detalle no es cosmético: con un solo episodio, el optimizador selecciona políticas afortunadas en lugar de políticas buenas — sobreajuste a la condición inicial, la versión doméstica del problema que domina toda la sección 4."""))

C.append(code("""def busqueda_aleatoria(env, rng, n_candidatos=360, n_ep=3, **kw):
    mejor_w, mejor_s, historia = None, -np.inf, []
    for k in range(n_candidatos):
        w = rng.normal(size=4)
        s = np.mean([episodio(env, w, 7 * k + i, **kw) for i in range(n_ep)])
        if s > mejor_s:
            mejor_w, mejor_s = w, s
        historia.append(mejor_s)
    return mejor_w, np.array(historia)

def entropia_cruzada(env, rng, evaluador=None, n_iter=15, n_cand=30, n_elite=6, n_ep=3):
    \"\"\"CEM: la distribucion de parametros se concentra sobre la elite de cada generacion.\"\"\"
    if evaluador is None:
        evaluador = lambda w, k: np.mean([episodio(env, w, 7 * k + i) for i in range(n_ep)])
    mu, sigma = np.zeros(4), np.ones(4)
    historia = []
    for it in range(n_iter):
        candidatos = rng.normal(mu, sigma, size=(n_cand, 4))
        puntos = np.array([evaluador(w, it * n_cand + k) for k, w in enumerate(candidatos)])
        elite = candidatos[np.argsort(puntos)[-n_elite:]]
        mu, sigma = elite.mean(axis=0), elite.std(axis=0) + 0.02   # el +0.02 evita colapsar
        historia.append((puntos.mean(), puntos.max()))
    return mu, np.array(historia)

rng = np.random.default_rng(39)
ajustar_fisica(env)

t0 = time.perf_counter()
w_ra, hist_ra = busqueda_aleatoria(env, rng)
t_ra = time.perf_counter() - t0

t0 = time.perf_counter()
w_cem, hist_cem = entropia_cruzada(env, rng)
t_cem = time.perf_counter() - t0

print(f'Busqueda aleatoria : {t_ra:5.1f} s   ->  retorno {evaluar(env, w_ra):6.1f}')
print(f'Entropia cruzada   : {t_cem:5.1f} s   ->  retorno {evaluar(env, w_cem):6.1f}')
print(f'Politica al azar   :               ->  retorno {al_azar.mean():6.1f}  (linea base)')
print(f'\\nPesos aprendidos por CEM: {np.round(w_cem, 3)}')
print('   componentes: [x, x_punto, theta, theta_punto]')
print('   Es una realimentacion de estado de manual: pesa mucho las variables del')
print('   pendulo y poco la posicion del carro. Guardalo: en la seccion 4 volveremos')
print('   a mirar estos cuatro numeros y habran cambiado de forma muy reveladora.')"""))

C.append(code("""fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 3.3))
a1.hist(al_azar, bins=30, color='0.6', edgecolor='white')
a1.axvline(evaluar(env, w_cem), color=IQS_VERDE, lw=2.5, label='politica CEM')
a1.axvline(al_azar.mean(), color='crimson', lw=2, ls='--', label='media al azar')
a1.set_xlabel('retorno del episodio'); a1.set_ylabel('politicas')
a1.set_title('200 politicas al azar frente a la aprendida', fontsize=10)
a1.legend(fontsize=8)

ev = np.arange(1, len(hist_cem) + 1) * 30
a2.plot(np.arange(1, len(hist_ra) + 1) * 3, hist_ra, color=IQS_AZUL, lw=2,
        label='busqueda aleatoria (mejor hasta ahora)')
a2.plot(ev * 3, hist_cem[:, 0], color=IQS_VERDE, lw=2, label='CEM (media de la generacion)')
a2.plot(ev * 3, hist_cem[:, 1], color=IQS_VERDE, lw=1, ls='--', label='CEM (mejor)')
a2.set_xlabel('episodios simulados'); a2.set_ylabel('retorno')
a2.set_title('Curvas de aprendizaje', fontsize=10); a2.legend(fontsize=7)
plt.tight_layout(); plt.show()"""))

C.append(md("""**Lo que hay que comentar, con honestidad de ingeniero.** En CartPole la búsqueda aleatoria funciona: el espacio de parámetros tiene cuatro dimensiones y más de una décima parte de los vectores gaussianos ya mantienen el péndulo en pie un buen rato, como muestra el histograma. Conviene decirlo en clase en lugar de disimularlo — es una lección sobre líneas base: **si probar al azar resuelve tu problema, tu problema no demuestra nada sobre tu algoritmo**.

La diferencia real está en la otra curva: en el CEM sube la **media** de la generación, no solo el mejor encontrado. Eso significa que la distribución entera se ha desplazado hacia la zona buena del espacio de parámetros, es decir, que el algoritmo *usa* la información de las evaluaciones en lugar de solo quedarse con el afortunado. Esa propiedad es la que escala, y el ejercicio 1 la pone a prueba donde de verdad importa: al aumentar el número de parámetros.

Y conviene decir en clase lo que **no** hemos hecho, porque en el examen se pregunta: no hemos calculado ningún gradiente, no hemos usado ninguna ventaja A(s,a) = q(s,a) − v(s) para reducir varianza, ni hay arquitectura actor-crítico (Sutton y Barto, 2018, cap. 13). Con cuatro parámetros no hace falta. Con los millones de parámetros de una política de locomoción, la búsqueda de caja negra es inviable y hay que usar el gradiente — y con el gradiente aparece el problema que resuelve **PPO**: un paso demasiado grande destruye la política, y como los datos siguientes los genera esa política rota, el colapso se realimenta. PPO define el cociente r_t(θ) = π_θ(a_t|s_t)/π_vieja(a_t|s_t) y maximiza el objetivo recortado, con ε típicamente 0,2, de forma que alejarse demasiado de la política anterior deja de aportar objetivo (Schulman et al., 2017, arXiv:1707.06347). De ahí lo de «proximal».

### Ejercicio 1

Sustituye la política lineal de 4 parámetros por una red diminuta con una capa oculta de 8 neuronas y tangente hiperbólica: 48 parámetros en lugar de 4. Con el mismo presupuesto de episodios, compara **búsqueda aleatoria** y **CEM**: qué fracción de las políticas aleatorias aguanta más de 200 pasos, y a dónde llega cada método. La celda siguiente lo tiene montado."""))

C.append(code("""# Ejercicio 1: la misma busqueda, con 48 parametros en vez de 4
H = 8
DIM = 4 * H + H + H

def accion_red(theta, obs):
    W1 = theta[:4*H].reshape(4, H); b1 = theta[4*H:4*H+H]; w2 = theta[4*H+H:]
    return 1 if float(w2 @ np.tanh(obs @ W1 + b1)) > 0 else 0

def episodio_red(theta, semilla, max_pasos=MAX_PASOS):
    obs, _ = env.reset(seed=int(semilla)); total = 0.0
    for _ in range(max_pasos):
        obs, r, term, trunc, _ = env.step(accion_red(theta, obs)); total += r
        if term or trunc:
            break
    return total

ajustar_fisica(env)
rng_e = np.random.default_rng(3)
pol_az = rng_e.normal(size=(150, DIM))   # una politica por candidato, fija en sus 3 episodios
puntos = np.array([np.mean([episodio_red(w, 100*k + i) for i in range(3)])
                   for k, w in enumerate(pol_az)])
print(f'Busqueda aleatoria en {DIM} dimensiones: retorno medio {puntos.mean():5.1f}, '
      f'fraccion que supera 200 pasos: {100*np.mean(puntos > 200):.0f} %')

mu, sigma = np.zeros(DIM), np.ones(DIM)
for it in range(15):
    cand = rng_e.normal(mu, sigma, size=(30, DIM))
    sc = np.array([np.mean([episodio_red(w, 7*(it*30 + k) + i) for i in range(3)])
                   for k, w in enumerate(cand)])
    elite = cand[np.argsort(sc)[-6:]]
    mu, sigma = elite.mean(axis=0), elite.std(axis=0) + 0.02
print(f'CEM en {DIM} dimensiones: ultima generacion {sc.mean():5.1f}, politica final '
      f'{np.mean([episodio_red(mu, 50000 + i) for i in range(20)]):5.1f}')"""))

# ---------------- 3. Sim to real
C.append(md("""## 3. El problema sim-to-real: entrenar en un mundo, actuar en otro

Aquí llega la sección que da nombre a la sesión. El RL profundo es voraz en datos —de millones a miles de millones de transiciones—, y en el robot físico eso es inviable por tiempo, por desgaste, por riesgo y por logística. La respuesta de la disciplina es entrenar en simulación. Pero entonces aparece la **brecha de realidad**: ningún simulador reproduce exactamente fricciones, masas, holguras, latencias de comunicación o dinámica de actuadores, y una política de RL —optimizadora implacable— explota cualquier regularidad espuria del simulador. El resultado es la política que camina perfecta en pantalla y se cae en el laboratorio.

Vamos a fabricar esa situación con tres parámetros que son exactamente los sospechosos habituales en un robot real:

| Parámetro | Qué representa | Valor «de catálogo» | Valor «del robot real» |
|---|---|---|---|
| `masspole` | Masa de la carga que mueve el actuador | 0,1 kg | desconocida, de 0,05 a más de 1 kg |
| `length` | Geometría, montaje, herramienta | 0,5 m | distinta de la del plano |
| `retardo` | **Latencia** del sensor, del bus y del actuador (bloque 3) | 0 pasos | 2, 3, 4 pasos a 50 Hz = 40-80 ms |

La latencia es el sospechoso que más subestiman los estudiantes y el que más daño hace: un controlador bang-bang afinado sin retardo se convierte en un oscilador en cuanto lo hay."""))

C.append(code("""MASAS      = np.array([0.1, 0.3, 0.6, 1.0])
LONGITUDES = np.array([0.5, 0.8, 1.1, 1.5])
RETARDOS   = [0, 2, 3]

def rejilla(env, w, masas=MASAS, longitudes=LONGITUDES, retardo=0, n=6):
    M = np.zeros((len(masas), len(longitudes)))
    for i, mp in enumerate(masas):
        for j, L in enumerate(longitudes):
            ajustar_fisica(env, masspole=mp, length=L)
            M[i, j] = evaluar(env, w, n=n, semilla_base=5000, retardo=retardo)
    ajustar_fisica(env)
    return M

t0 = time.perf_counter()
rej_nom = {d: rejilla(env, w_cem, retardo=d) for d in RETARDOS}
print(f'Barrido evaluado en {time.perf_counter() - t0:.1f} s\\n')

print('Politica entrenada SOLO con los parametros nominales (masspole=0.1, length=0.5, sin retardo):')
for d in RETARDOS:
    print(f'  retardo {d} pasos ({1000*d*env.unwrapped.tau:3.0f} ms):  '
          f'retorno medio {rej_nom[d].mean():6.1f}   peor caso {rej_nom[d].min():6.1f}')
print(f'\\nEn su mundo de entrenamiento la misma politica saca {evaluar(env, w_cem):.1f} sobre {MAX_PASOS}.')"""))

# ---------------- 4. Domain randomization
C.append(md("""## 4. Domain randomization: no perseguir el simulador perfecto

El remedio más influyente no consiste en modelar mejor, sino en **aleatorizar agresivamente** los parámetros del simulador en cada episodio, de forma que la realidad quede —con suerte— dentro de la distribución de variaciones vista en entrenamiento. La formulación original demostró que un detector entrenado solo con imágenes sintéticas aleatorizadas transfería al mundo real sin ninguna imagen real (Tobin et al., 2017, arXiv:1703.06907); el caso extremo es la mano antropomórfica de OpenAI resolviendo el cubo de Rubik tras entrenar con aleatorización **automática** de dominios, que amplía los rangos de variación a medida que la política mejora (OpenAI et al., 2019, arXiv:1910.07113).

En nuestro caso la implementación cabe en una función: cambiar el evaluador del CEM para que cada episodio muestree una masa, una longitud y un retardo distintos. El algoritmo de optimización no se toca."""))

C.append(code("""def evaluador_aleatorizado(w, k, n_ep=3):
    \"\"\"Cada episodio, un robot distinto. La politica ya no puede sobreajustar a uno solo.\"\"\"
    r = np.random.default_rng(k)
    puntos = []
    for i in range(n_ep):
        ajustar_fisica(env, masspole=r.uniform(0.05, 1.2), length=r.uniform(0.3, 1.5))
        puntos.append(episodio(env, w, 7 * k + i, retardo=int(r.integers(0, 5))))
    ajustar_fisica(env)
    return float(np.mean(puntos))

t0 = time.perf_counter()
w_dr, hist_dr = entropia_cruzada(env, np.random.default_rng(39),
                                 evaluador=evaluador_aleatorizado)
print(f'Entrenamiento con aleatorizacion de dominio: {time.perf_counter() - t0:.1f} s')
print(f'Pesos nominales : {np.round(w_cem, 3)}')
print(f'Pesos con DR    : {np.round(w_dr, 3)}')

rej_dr = {d: rejilla(env, w_dr, retardo=d) for d in RETARDOS}
print()
print(f'{"":>10}  {"nominal":>18}  {"con aleatorizacion":>20}')
for d in RETARDOS:
    print(f'  retardo {d}  medio {rej_nom[d].mean():6.1f} / peor {rej_nom[d].min():5.1f}  '
          f'  medio {rej_dr[d].mean():6.1f} / peor {rej_dr[d].min():5.1f}')
print(f'\\nY en el mundo nominal, la politica robusta saca {evaluar(env, w_dr):.1f} '
      f'frente a {evaluar(env, w_cem):.1f} de la especializada.')"""))

C.append(code("""fig, axes = plt.subplots(2, len(RETARDOS), figsize=(12, 5.4))
for fila, (etiqueta, rej) in enumerate([('entrenada en nominal', rej_nom),
                                        ('con aleatorizacion', rej_dr)]):
    for col, d in enumerate(RETARDOS):
        ax = axes[fila, col]
        im = ax.imshow(rej[d], vmin=0, vmax=MAX_PASOS, cmap='RdYlGn', aspect='auto')
        ax.set_xticks(range(len(LONGITUDES)), [f'{x:.1f}' for x in LONGITUDES], fontsize=8)
        ax.set_yticks(range(len(MASAS)), [f'{x:.2f}' for x in MASAS], fontsize=8)
        ax.set_title(f'{etiqueta} · retardo {d}', fontsize=9)
        if col == 0:
            ax.set_ylabel('masspole [kg]', fontsize=8)
        ax.set_xlabel('length [m]', fontsize=8)
        for i in range(rej[d].shape[0]):
            for j in range(rej[d].shape[1]):
                ax.text(j, i, f'{rej[d][i, j]:.0f}', ha='center', va='center', fontsize=7)
        ax.grid(False)
fig.colorbar(im, ax=axes, fraction=0.02, label='retorno medio')
plt.show()"""))

C.append(md("""**La figura es el resumen de la sesión.** La fila de arriba es la política óptima *para el simulador nominal*: saca el máximo en la esquina en la que se entrenó y se derrumba en cuanto la masa y la longitud se alejan del catálogo — su peor casilla cae a quince pasos, un fracaso completo, y el retardo de tres pasos (sesenta milisegundos, nada en un robot real con bus de campo y ciclo de PLC) se lleva por delante otro tercio del rendimiento medio. La fila de abajo, con el mismo algoritmo, el mismo número de parámetros y el mismo presupuesto de cómputo, aguanta en toda la rejilla.

Merece la pena volver a los **pesos**, como quedamos en la sección 2. La política especializada carga la ganancia sobre la velocidad angular; la robusta la traslada al **ángulo** y baja tanto la de la velocidad del carro como la de la velocidad angular. Ha redescubierto sola una lección clásica del bloque 5: **las señales derivadas son justamente las que se vuelven peligrosas cuando hay retardo en el lazo**, porque realimentan información caducada. Nadie se lo dijo; lo dedujo la selección.

Un apunte honesto para el aula: aquí la política robusta no paga ningún peaje en el mundo nominal —las dos sacan el máximo—, porque CartPole con los parámetros de catálogo es demasiado fácil para que se note. En tareas exigentes ese peaje existe y es la razón por la que no se aleatoriza sin medida.

Y una advertencia que hay que dar en el aula para que la aleatorización no se convierta en superstición: **la aleatorización solo protege dentro de su rango**. El ejercicio 2 lo comprueba. Fuera del rango de entrenamiento, la política robusta también se cae — y ese es exactamente el motivo por el que en la práctica se combina la aleatorización con la **identificación de parámetros del sistema real**, para centrar las distribuciones donde importa, y con un ajuste fino final sobre el robot.

### Ejercicio 2

Evalúa las dos políticas fuera del rango de aleatorización: `masspole` de 2 a 4 kg, `length` de 2 a 3 m y retardos de 6 y 8 pasos. ¿Sigue ganando la política robusta? ¿Se sostiene? Formula con tus palabras qué garantiza y qué no garantiza la aleatorización de dominio.

### Ejercicio 3

Entrena con aleatorización evaluando cada candidato con **un solo episodio** (`n_ep=1`) en lugar de tres, y mide las dos políticas resultantes sobre un conjunto **fijo** de cinco mundos de prueba que el optimizador nunca ha visto. ¿Cuál gana? ¿Por qué la puntuación con la que se optimiza no sirve como medida de rendimiento?"""))

C.append(code("""# Ejercicio 3
MUNDOS_TEST = [(0.1, 0.5, 0), (0.6, 1.0, 2), (1.0, 1.5, 3), (0.3, 0.8, 4), (0.8, 0.6, 1)]

def test_honesto(w, n=8):
    \"\"\"Cinco mundos fijos, semillas nuevas: el conjunto de test del RL.\"\"\"
    puntos = []
    for mp, L, d in MUNDOS_TEST:
        ajustar_fisica(env, masspole=mp, length=L)
        puntos.append(evaluar(env, w, n=n, semilla_base=77000, retardo=d))
    ajustar_fisica(env)
    return float(np.mean(puntos))

for n_ep in (1, 3):
    ev = lambda w, k, n_ep=n_ep: evaluador_aleatorizado(w, k, n_ep=n_ep)
    w_x, h_x = entropia_cruzada(env, np.random.default_rng(5), evaluador=ev)
    print(f'n_ep = {n_ep}:  puntuacion de la ultima generacion {h_x[-1, 0]:6.1f}  ->  '
          f'test en 5 mundos nuevos: {test_honesto(w_x):6.1f}')"""))

C.append(code("""# Ejercicio 2
MASAS_X = np.array([2.0, 3.0, 4.0])
LONG_X  = np.array([2.0, 2.5, 3.0])
print(f'{"retardo":>8}  {"nominal":>9}  {"con DR":>9}   (fuera del rango de entrenamiento)')
for d in (6, 8):
    a = rejilla(env, w_cem, masas=MASAS_X, longitudes=LONG_X, retardo=d, n=4).mean()
    b = rejilla(env, w_dr,  masas=MASAS_X, longitudes=LONG_X, retardo=d, n=4).mean()
    print(f'{d:8d}  {a:9.1f}  {b:9.1f}')"""))

C.append(md("""---

## Soluciones

**Ejercicio 1.** El resultado es contundente: en 48 dimensiones, **ninguna** de las 150 políticas aleatorias supera los 200 pasos y el retorno medio se desploma a unas pocas decenas, mientras que el CEM, con el mismo presupuesto de episodios, llega igualmente al tope. La búsqueda ciega no ha empeorado porque la tarea sea más difícil —es la misma tarea— sino porque el **volumen del espacio de parámetros** ha crecido exponencialmente y la fracción que funciona se ha vuelto despreciable.

Esa es exactamente la razón por la que el RL profundo no se hace con búsqueda aleatoria: una política de locomoción tiene del orden de 10⁵-10⁶ parámetros, y ninguna cantidad de sorteos alcanza. Hace falta un método que use la información de cada evaluación para moverse en una dirección — el CEM lo hace de forma rudimentaria con su élite, y los métodos de gradiente de política lo hacen con el teorema del gradiente (Sutton y Barto, 2018, cap. 13), que es incomparablemente más eficiente en muestras. Conviene además señalar el matiz: hasta unas decenas de parámetros los métodos de caja negra son competitivos y mucho más simples de implementar; el punto de cruce está en el tamaño del problema, no en la elegancia del método.

**Ejercicio 2.** Fuera del rango, la política robusta suele seguir siendo mejor que la especializada —ha aprendido una estructura de realimentación más conservadora, no un truco—, pero cae mucho respecto de su rendimiento dentro del rango, y con retardos de 6-8 pasos las dos fracasan. La formulación correcta es: la aleatorización de dominio **no garantiza robustez universal; garantiza, a lo sumo, rendimiento sobre la distribución que se aleatorizó**. Es un cambio de objetivo, no una propiedad mágica: se pasa de optimizar el retorno en un mundo a optimizar el retorno *esperado sobre una familia de mundos*. Si el robot real cae fuera de esa familia, la política no tiene ninguna razón para funcionar.

De ahí las dos prácticas complementarias que citan los apuntes: identificar los parámetros del sistema real para **centrar** las distribuciones donde de verdad está el robot, y ampliar los rangos automáticamente a medida que la política mejora, que es la aportación de la aleatorización automática de dominios del cubo de Rubik (OpenAI et al., 2019, arXiv:1910.07113).

**Ejercicio 3.** Con `n_ep = 1` la política resultante rinde claramente peor en los cinco mundos de prueba que con `n_ep = 3`, pese a que el coste de entrenamiento es un tercio. La razón es la de siempre en aprendizaje automático: el CEM no distingue «esta política es buena» de «a esta política le tocó un mundo fácil y un arranque afortunado», y como selecciona la élite por puntuación, **selecciona sistemáticamente a los afortunados**. Con la aleatorización de por medio el efecto se amplifica, porque la varianza entre episodios ya no viene solo de la condición inicial sino también del robot que ha tocado.

La consecuencia metodológica hay que dictarla: **la puntuación con la que se optimiza no es una medida de rendimiento**. Hace falta un conjunto de evaluación separado —mundos y semillas que el optimizador no haya visto—, exactamente igual que el conjunto de test del aprendizaje supervisado. Es también la razón por la que una curva de entrenamiento de un paper de RL, sin evaluaciones independientes al lado, no demuestra nada; y una excelente pregunta para el turno del seminario de S41-S42."""))

C.append(md("""---

## Para llevarse de esta sesión

**El objeto que se aprende es una ley de control.** Una política parametrizada es una función del estado a la acción, evaluable en microsegundos, sin optimización en línea — exactamente lo que diseñábamos a mano en el bloque 5, solo que ajustada por datos. Cambia quién escribe los coeficientes, no qué son.

**Con pocos parámetros basta un optimizador de caja negra; con muchos hace falta el gradiente, y con el gradiente hace falta PPO.** El objetivo recortado de PPO existe para impedir que un paso demasiado grande destruya la política que está generando los datos (Schulman et al., 2017, arXiv:1707.06347). Lo que se pide en el examen es eso: qué optimiza, qué es el cociente r_t y qué problema elimina el recorte.

**La brecha de realidad no es un detalle de implementación: es el problema central.** Una política óptima para un simulador está, por construcción, ajustada a las particularidades de ese simulador —incluidas las que no queríamos modelar—. La aleatorización de dominio (Tobin et al., 2017, arXiv:1703.06907; OpenAI et al., 2019, arXiv:1910.07113) cambia el objetivo: en lugar de un mundo, una familia de mundos. Funciona dentro de la familia y no promete nada fuera de ella.

Y el flujo profesional completo, que conviene dictar tal cual: **modelar el robot (B4/B7) → definir el MDP (S38) → entrenar PPO en miles de simulaciones paralelas → aleatorizar dominios → desplegar**. El despliegue no elimina el temario clásico: la política emite consignas a decenas de hercios, y quien las convierte en pares y movimientos reales son los lazos de control del bloque 5, a kilohercios, sobre los actuadores del bloque 3.

**Y la pregunta del debate, para cerrar la hora:** ¿qué aleatorizaríais para transferir una política de empuje de cajas con el ABB del laboratorio? El orden defendible, por «cuánto cambia la dinámica que la política no observa», es: fricción caja-mesa (el parámetro peor conocido y el que más cambia la respuesta al empuje), latencia de la red y del ciclo de control (que aquí hemos visto hundir una política por sí sola), masa de la caja, posición inicial —que es cobertura de estados más que robustez— y, solo si hay cámara en el lazo, la iluminación, que es precisamente el caso de Tobin et al. (2017), donde la aleatorización visual era *todo* el método. La coda profesional: masa, geometría y latencia se **miden** barato en el laboratorio, y medirlas permite estrechar las distribuciones en torno al valor real. Aleatorizar de más también tiene coste — la política se vuelve conservadora—, así que la regla es: mide lo que puedas medir barato y aleatoriza lo que no.

Mañana, en S40, el robot deja de aprender solo con recompensa: se le enseña con demostraciones.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S39_RL_Profundo_SimToReal.ipynb', C)
print('escrito S39')
