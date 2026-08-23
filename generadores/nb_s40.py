from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('matplotlib','matplotlib'), ('scipy','scipy'),
       ('scikit-learn','sklearn')]
C = []

C.append(cabecera(
    "S40", "Imitación, diffusion policies y modelos VLA", "8",
    "viernes 11 de diciembre de 2026", "2 h",
    "Implementa la clonación de comportamiento de principio a fin: un experto sintético demuestra una tarea de alcance con un obstáculo que hay que rodear, un regresor de scikit-learn aprende a copiarlo, y después se provoca el fallo característico —la deriva por acumulación de error al salirse de los estados demostrados—. La segunda mitad ilustra numéricamente por qué predecir la **media** de acciones multimodales estrella el robot contra el obstáculo, que es la motivación exacta de las diffusion policies, y cierra con la parte conceptual de los modelos VLA y los gemelos digitales.",
    "Ross, Gordon y Bagnell (2011), AISTATS, para DAgger. Zhao et al. (2023), ALOHA/ACT, arXiv:2304.13705. Chi et al. (2023), *Diffusion Policy*, arXiv:2303.04137. Brohan et al. (2023), RT-2, arXiv:2307.15818. Kim et al. (2024), OpenVLA, arXiv:2406.09246. Black et al. (2024), π0, arXiv:2410.24164. NVIDIA (2025), GR00T N1, arXiv:2503.14734. Gemini Robotics (Google DeepMind, 2025, informe técnico). ISO 23247 para el marco de gemelo digital en fabricación.",
    "los apuntes del bloque 8"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import NearestNeighbors
np.set_printoptions(precision=3, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.2)
plt.rcParams['axes.grid'] = True
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('Listo.')"""))

# ---------------- 1. tarea y experto
C.append(md("""## 1. La tarea y el experto sintético

El aprendizaje por imitación invierte la lógica del RL: en lugar de especificar **qué es hacerlo bien** —la recompensa— y dejar que el agente lo descubra, se muestra **cómo se hace** y se pide al modelo que lo reproduzca. Su forma más simple, la clonación de comportamiento (*behavior cloning*, BC), es aprendizaje supervisado puro: se registran pares (observación, acción) mientras alguien demuestra la tarea —hoy casi siempre por teleoperación— y se ajusta un modelo que predice la acción del demostrador a partir de la observación.

Esta asimetría explica la división del trabajo actual de la disciplina, y merece plantearse como pregunta en clase antes de escribir una línea: demostrar cómo se dobla una camiseta cuesta minutos; escribir una función de recompensa que defina «camiseta bien doblada» y esperar que el RL no la explote de forma perversa puede costar semanas. Por eso la locomoción —fácil de premiar, casi imposible de teleoperar de forma dinámica— es territorio del RL de S39, y la manipulación —fácil de demostrar, difícil de premiar— es territorio de la imitación.

La tarea de este cuaderno es la mínima que exhibe todos los fenómenos: un efector puntual en el plano debe ir desde la izquierda hasta un punto objetivo a la derecha, y en medio hay un **tabique** que solo se puede rodear por arriba o por abajo. La observación es la posición (x, y); la acción, el desplazamiento del siguiente paso. Es manipulación planar de juguete, pero conserva lo esencial: hay **dos** formas correctas de hacerlo y el fracaso tiene consecuencias.

El «experto» es un controlador escrito a mano —el equivalente sintético del humano que teleopera—: apuntar a la puerta elegida hasta cruzar el tabique y, después, a la meta."""))

C.append(code("""META   = np.array([1.0, 0.0])
PASO   = 0.035          # modulo del desplazamiento por paso
PARED_Y  = 0.90         # el tabique va de y = -0.90 a y = +0.90
PARED_GR = 0.05         # semigrosor del tabique, en x
HUECO    = 0.15         # holgura con la que el experto pasa por encima o por debajo

def unitario(v):
    return v / (np.linalg.norm(v) + 1e-12)

def choca(p):
    return abs(p[0]) <= PARED_GR and abs(p[1]) <= PARED_Y

def experto(p, lado=+1):
    \"\"\"Demostrador: apunta a la puerta (arriba si lado=+1, abajo si lado=-1)
    mientras no ha cruzado el tabique; despues, directo a la meta.\"\"\"
    puerta = np.array([0.0, lado * (PARED_Y + HUECO)])
    objetivo = puerta if p[0] < 0.0 else META
    return PASO * unitario(objetivo - p)

def rodar(politica, p0, n_pasos=250, empuje=None, empuje_en=20):
    \"\"\"Ejecuta una politica en lazo cerrado. 'empuje' = perturbacion externa
    aplicada en el paso 'empuje_en' (alguien mueve la pieza, el robot resbala...).\"\"\"
    p = np.array(p0, float)
    traza = [p.copy()]
    for k in range(n_pasos):
        p = p + politica(p)
        if empuje is not None and k == empuje_en:
            p = p + empuje
        traza.append(p.copy())
        if choca(p):
            return np.array(traza), 'CHOCA'
        if np.linalg.norm(p - META) < 0.06:
            return np.array(traza), 'exito'
        if np.abs(p).max() > 2.4:
            return np.array(traza), 'se escapa'
    return np.array(traza), 'sin llegar'

# el experto no falla nunca: es la referencia contra la que mediremos todo
rng = np.random.default_rng(40)
for lado in (+1, -1):
    resultados = {}
    for _ in range(80):
        p0 = np.array([-1.0 + rng.normal(0, 0.05), rng.normal(0, 0.10)])
        _, fin = rodar(lambda p: experto(p, lado), p0)
        resultados[fin] = resultados.get(fin, 0) + 1
    print(f'Experto por {"arriba" if lado > 0 else "abajo ":6s} en 80 ejecuciones: {resultados}')"""))

C.append(md("""### Las demostraciones

Cuarenta demostraciones desde posiciones iniciales repartidas a la izquierda, con un poco de ruido en la acción —ninguna teleoperación humana es determinista—. **Todas rodean por arriba**: es un demostrador consistente, el caso favorable. La multimodalidad la dejamos para la sección 4.

Fíjate en qué se guarda: pares (posición, desplazamiento). Ni recompensa, ni modelo del tabique, ni meta. El modelo solo verá esos pares — y esa es exactamente la información que sale de una sesión de teleoperación."""))

C.append(code("""SIGMA_DEMO = 0.003        # ruido del demostrador, por componente

def generar_demostraciones(n_demos=40, lado=+1, semilla=40, sigma=SIGMA_DEMO):
    rng = np.random.default_rng(semilla)
    X, Y, trazas = [], [], []
    for _ in range(n_demos):
        p = np.array([-1.0 + rng.normal(0, 0.05), rng.normal(0, 0.10)])
        traza = [p.copy()]
        for _ in range(250):
            a = experto(p, lado) + rng.normal(0, sigma, 2)
            X.append(p.copy())
            Y.append(a.copy())
            p = p + a
            traza.append(p.copy())
            if np.linalg.norm(p - META) < 0.06:
                break
        trazas.append(np.array(traza))
    return np.array(X), np.array(Y), trazas

X, Y, trazas = generar_demostraciones()
print(f'{len(trazas)} demostraciones  ->  {len(X)} pares (observacion, accion)')
print(f'Rango de x en los datos: [{X[:, 0].min():+.2f}, {X[:, 0].max():+.2f}]')
print(f'Rango de y en los datos: [{X[:, 1].min():+.2f}, {X[:, 1].max():+.2f}]')
print(f'Ninguna demostracion choca: '
      f'{not any(choca(q) for t in trazas for q in t)}')"""))

C.append(code("""def escenario(ax, titulo=''):
    ax.add_patch(plt.Rectangle((-PARED_GR, -PARED_Y), 2 * PARED_GR, 2 * PARED_Y, color='0.35'))
    ax.scatter(*META, marker='*', s=200, color='crimson', zorder=6)
    ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.35, 1.35)
    ax.set_aspect('equal'); ax.set_title(titulo, fontsize=10)
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.grid(alpha=.25)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 4.4))
escenario(a1, 'Las 40 demostraciones del experto')
for t in trazas:
    a1.plot(t[:, 0], t[:, 1], color=IQS_VERDE, lw=1, alpha=0.6)
    a1.scatter(t[0, 0], t[0, 1], s=14, color=IQS_AZUL, zorder=5)

escenario(a2, 'El campo de acciones demostrado')
paso = 14
a2.quiver(X[::paso, 0], X[::paso, 1], Y[::paso, 0], Y[::paso, 1],
          color=IQS_AZUL, scale=1.1, width=0.004)
plt.tight_layout(); plt.show()"""))

# ---------------- 2. BC
C.append(md("""## 2. Clonación de comportamiento con scikit-learn

Ahora el paso que hace del BC «aprendizaje supervisado puro»: un regresor que va de observación a acción. Usamos un perceptrón multicapa pequeño de `sklearn`, dos capas ocultas y nada exótico, porque lo importante no es el modelo sino lo que le pasa después.

Un detalle técnico que conviene señalar en clase porque muerde a todo el mundo: **entrenamos sobre la acción normalizada** (dividida por `PASO`, de modo que los objetivos son de orden 1) y multiplicamos de vuelta al predecir. Con objetivos de orden 0,03 el optimizador por defecto de `sklearn` ajusta bastante peor. Es escalado de datos de manual, y es el tipo de cosa que separa un experimento que funciona de uno que «no aprende» sin motivo aparente.

Y dos evaluaciones distintas, que **no hay que confundir nunca**:

1. **Error de predicción** sobre los datos: ¿el modelo copia bien las acciones del experto? Esto es lo que optimiza el entrenamiento.
2. **Éxito en la tarea** al ejecutar la política en lazo cerrado. Esto es lo único que importa.

La distancia entre esas dos cosas es toda la sección 3."""))

C.append(code("""def ajustar_politica(Xs, Ys, semilla=40):
    \"\"\"Regresor observacion -> accion normalizada. Aprendizaje supervisado puro.\"\"\"
    return MLPRegressor(hidden_layer_sizes=(64, 64), activation='tanh',
                        max_iter=1500, random_state=semilla, tol=1e-9).fit(Xs, Ys / PASO)

def como_politica(modelo):
    return lambda p: PASO * modelo.predict(p.reshape(1, -1))[0]

modelo_bc = ajustar_politica(X, Y)
pi_bc = como_politica(modelo_bc)

rmse = float(np.sqrt(((modelo_bc.predict(X) - Y / PASO) ** 2).sum(axis=1).mean())) * PASO
suelo = np.sqrt(2) * SIGMA_DEMO          # el ruido del propio demostrador, irreducible
print(f'RMSE de la accion sobre los datos : {rmse:.5f}  ({100*rmse/PASO:.1f} % del modulo)')
print(f'Ruido irreducible del demostrador : {suelo:.5f}  ({100*suelo/PASO:.1f} %)')
print('-> el modelo esta practicamente en el suelo de ruido: ha aprendido al experto.')

resultados = {}
for t in trazas[:20]:
    _, fin = rodar(pi_bc, t[0])
    resultados[fin] = resultados.get(fin, 0) + 1
print(f'\\nEjecutando desde los arranques demostrados: {resultados}')"""))

# ---------------- 3. deriva
C.append(md("""## 3. El fallo característico: deriva y errores compuestos

El BC ingenuo tiene un modo de fallo que el estudiante debe saber nombrar: **desplazamiento covariante** (*covariate shift*) con errores compuestos. La política se entrena con la distribución de estados que visita el experto; en ejecución, sus pequeños errores la llevan a estados ligeramente distintos, donde tiene aún menos datos, comete errores mayores, y la desviación se realimenta hasta salir por completo de la distribución de entrenamiento — el coche de la demo que, un palmo fuera del carril demostrado, ya no sabe volver.

Lo provocamos de la forma más limpia posible y sin tocar el modelo: **un empujón externo a mitad de ejecución**. Alguien mueve la pieza, la rueda patina, el operario roza el robot. El experto absorbe la perturbación sin inmutarse, porque recalcula su acción desde el estado actual. Veamos qué hace su clon."""))

C.append(code("""vecinos = NearestNeighbors(n_neighbors=1).fit(X)

def distancia_a_los_datos(traza):
    \"\"\"Para cada punto de la trayectoria, distancia al estado demostrado mas cercano.\"\"\"
    d, _ = vecinos.kneighbors(traza)
    return d.ravel()

EMPUJONES = [0.0, -0.2, -0.4, -0.6, -0.8]
ejecuciones = {}
print(f'{"empujon":>9}  {"clon (BC)":>10}  {"experto":>10}  {"distancia max. a los datos":>27}')
for d in EMPUJONES:
    tr, fin = rodar(pi_bc, np.array([-1.0, 0.0]), empuje=np.array([0.0, d]))
    tr_e, fin_e = rodar(lambda p: experto(p, +1), np.array([-1.0, 0.0]),
                        empuje=np.array([0.0, d]))
    dist = distancia_a_los_datos(tr)
    ejecuciones[d] = (tr, fin, dist, tr_e)
    print(f'{d:+9.2f}  {fin:>10}  {fin_e:>10}  {dist.max():27.3f}')"""))

C.append(code("""colores = {'exito': IQS_VERDE, 'CHOCA': 'crimson', 'se escapa': 'darkorange',
           'sin llegar': 'purple'}

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 4.4))
escenario(a1, 'El clon, tras un empujon a mitad de camino')
for t in trazas:
    a1.plot(t[:, 0], t[:, 1], color='0.8', lw=0.8, zorder=1)
for d, (tr, fin, dist, tr_e) in ejecuciones.items():
    a1.plot(tr_e[:, 0], tr_e[:, 1], color='0.45', lw=1.0, ls='--', zorder=2)
    a1.plot(tr[:, 0], tr[:, 1], color=colores[fin], lw=1.9, zorder=3)
a1.plot([], [], color='0.45', lw=1.2, ls='--', label='experto (siempre se recupera)')
for fin, col in colores.items():
    a1.plot([], [], color=col, lw=2, label=f'clon: {fin}')
a1.legend(fontsize=7, loc='lower left')

for d, (tr, fin, dist, tr_e) in ejecuciones.items():
    a2.plot(dist, color=colores[fin], lw=1.8, label=f'empujon {d:+.1f}')
a2.axvline(20, color='0.5', ls=':', lw=2)
a2.text(21, 0.02, 'empujon', fontsize=8, color='0.4')
a2.set_xlabel('paso de la ejecucion')
a2.set_ylabel('distancia al estado demostrado mas cercano')
a2.set_title('El error se acumula: la deriva', fontsize=10)
a2.legend(fontsize=7)
plt.tight_layout(); plt.show()"""))

C.append(md("""**Cómo comentarlo en clase.** La figura de la derecha es la que hay que dejar en la retina. Con un empujón pequeño la distancia a los datos sube un escalón y **vuelve a bajar**: el clon regresa al carril demostrado y termina la tarea. A partir de cierto empujón deja de volver: la distancia crece de forma monótona, porque cada paso lleva a un estado un poco más desconocido, donde la predicción es un poco peor, lo que lleva a un estado bastante más desconocido. Es una realimentación positiva del error, y por eso el fallo **no es proporcional a la perturbación**: hay un umbral, y pasado el umbral el desenlace es catastrófico.

Las líneas grises discontinuas son la clave del argumento: **el experto absorbe todos esos empujones sin despeinarse**. El experto no es más listo; simplemente sabe hacia dónde va desde cualquier estado. El clon solo sabe qué hacer en los estados que vio, y por debajo del tabique nunca ha visto nada.

Y conviene machacar el contraste con el número de la sección anterior: **el modelo copia al experto hasta el suelo de ruido del propio demostrador**. Un ingeniero que solo mirase la métrica de entrenamiento firmaría que la política es excelente. Esa métrica mide el ajuste *sobre los estados del experto*, y esos son precisamente los estados en los que la política no va a estar cuando algo se tuerza.

El remedio conceptual clásico es **DAgger**: ejecutar la política, pedir al experto que etiquete los estados que la política efectivamente visita, y reentrenar con el agregado de datos (Ross, Gordon y Bagnell, 2011, AISTATS). En la práctica moderna el problema se ataca además con abundancia y variedad de demostraciones y con una idea arquitectónica simple: el ***action chunking***, predecir de una vez un trozo de trayectoria de decenas de pasos en lugar de una acción por paso, lo que reduce el número de decisiones encadenadas y con ello la acumulación de error. Es una de las claves de ACT en el sistema ALOHA, que con teleoperación bimanual de bajo coste y unas decenas de demostraciones logra tareas de precisión como insertar una pila (Zhao et al., 2023, arXiv:2304.13705).

### Ejercicio 1

Implementa DAgger sobre los empujones que fallan: ejecuta la política, **etiqueta con el experto** las posiciones que efectivamente visitó (es decir, evalúa `experto(q, +1)` en cada punto de la trayectoria fallida), añade esos pares al conjunto de entrenamiento, reentrena y repite. ¿Cuántas rondas hacen falta? ¿Qué le pasa al conjunto de datos, y qué requisito práctico impone el método?"""))

C.append(code("""# Ejercicio 1: DAgger
X_d, Y_d = X.copy(), Y.copy()
pi_d = pi_bc
fallidos = [d for d, (_, fin, _, _) in ejecuciones.items() if fin != 'exito']
print('empujones que fallan de partida:', fallidos)
for ronda in range(3):
    nuevos_X, nuevos_Y = [], []
    for d in fallidos:
        tr, _ = rodar(pi_d, np.array([-1.0, 0.0]), empuje=np.array([0.0, d]))
        for q in tr:
            nuevos_X.append(q)
            nuevos_Y.append(experto(q, +1))       # el experto etiqueta lo que se visito
    X_d = np.vstack([X_d, np.array(nuevos_X)])
    Y_d = np.vstack([Y_d, np.array(nuevos_Y)])
    pi_d = como_politica(ajustar_politica(X_d, Y_d))
    res = [rodar(pi_d, np.array([-1.0, 0.0]), empuje=np.array([0.0, d]))[1] for d in fallidos]
    print(f'ronda {ronda + 1}: {len(X_d)} pares  ->  {res}')"""))

# ---------------- 4. multimodalidad
C.append(md("""## 4. Multimodalidad: por qué la media se estrella contra el tabique

Queda un defecto estructural del BC con regresión directa, y es el que motiva toda la línea de investigación actual. Si **la mitad de los demostradores rodea por arriba y la otra mitad por abajo**, la red que minimiza el error cuadrático predice la media — atravesar el obstáculo. Las demostraciones humanas son multimodales por naturaleza (hay muchas maneras válidas de agarrar una taza), y una política que promedia modos incompatibles produce acciones que no pertenecen a ninguno.

Lo demostramos con números, no con una analogía. Veinte demostraciones por arriba y veinte por abajo —todas perfectamente válidas, ninguna choca— y el mismo regresor sobre el conjunto mezclado."""))

C.append(code("""X_arr, Y_arr, tr_arr = generar_demostraciones(20, lado=+1, semilla=1)
X_aba, Y_aba, tr_aba = generar_demostraciones(20, lado=-1, semilla=2)
X_mm = np.vstack([X_arr, X_aba])
Y_mm = np.vstack([Y_arr, Y_aba])

pi_mm = como_politica(ajustar_politica(X_mm, Y_mm))

# --- el punto de la verdad: en el corredor, donde los dos modos se contradicen ---
p_critico = np.array([-0.5, 0.0])
a_arriba = experto(p_critico, +1)
a_abajo  = experto(p_critico, -1)
a_media  = 0.5 * (a_arriba + a_abajo)
a_modelo = pi_mm(p_critico)

def ang(a):
    return np.degrees(np.arctan2(a[1], a[0]))

print(f'En p = {p_critico}, en mitad del corredor:')
for nombre, a in [('demostrada por arriba', a_arriba), ('demostrada por abajo ', a_abajo),
                  ('media de las dos     ', a_media), ('predicha por el modelo', a_modelo)]:
    print(f'  {nombre}: {a}   angulo {ang(a):+7.1f} deg   modulo {np.linalg.norm(a):.4f}')
print(f'\\n  Las dos acciones validas apuntan a {ang(a_arriba):+.0f} y {ang(a_abajo):+.0f} grados.')
print(f'  El modelo predice {ang(a_modelo):+.0f} grados: DERECHO AL TABIQUE, que es justo')
print(f'  la unica direccion que ningun demostrador tomo nunca. Y ademas es mas corta')
print(f'  ({np.linalg.norm(a_media):.4f} frente a {PASO}): promediar direcciones opuestas encoge el vector.')"""))

C.append(code("""def tasa(politica, n=11, rango=0.15):
    res = {}
    for y0 in np.linspace(-rango, rango, n):
        _, fin = rodar(politica, np.array([-1.0, y0]))
        res[fin] = res.get(fin, 0) + 1
    return res

print('Politica entrenada sobre los DOS modos mezclados:')
print('  ', tasa(pi_mm))

# Y ahora, lo que si funciona: comprometerse con un modo en lugar de promediarlo.
pi_solo_arriba = como_politica(ajustar_politica(X_arr, Y_arr))
pi_solo_abajo  = como_politica(ajustar_politica(X_aba, Y_aba))
print('\\nUna politica por modo, con exactamente los mismos datos y el mismo modelo:')
print('  solo arriba:', tasa(pi_solo_arriba))
print('  solo abajo :', tasa(pi_solo_abajo))"""))

C.append(code("""fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 4.4))
escenario(a1, 'Dos modos validos, y lo que predice la regresion')
for t in tr_arr:
    a1.plot(t[:, 0], t[:, 1], color=IQS_VERDE, lw=0.9, alpha=0.55)
for t in tr_aba:
    a1.plot(t[:, 0], t[:, 1], color=IQS_AZUL, lw=0.9, alpha=0.55)
for a, col in [(a_arriba, IQS_VERDE), (a_abajo, IQS_AZUL), (a_modelo, 'crimson')]:
    a1.annotate('', xy=p_critico + 12 * a, xytext=p_critico,
                arrowprops=dict(color=col, width=2.4, headwidth=9))
a1.scatter(*p_critico, s=40, color='black', zorder=6)
a1.text(-1.28, -1.22, 'rojo = prediccion del regresor sobre los dos modos',
        fontsize=8, color='crimson')

escenario(a2, 'Promediar los modos frente a elegir uno')
for y0 in np.linspace(-0.15, 0.15, 7):
    tr, fin = rodar(pi_mm, np.array([-1.0, y0]))
    a2.plot(tr[:, 0], tr[:, 1], color='crimson', lw=1.8, zorder=4)
    for pol, col in ((pi_solo_arriba, IQS_VERDE), (pi_solo_abajo, IQS_AZUL)):
        tr2, _ = rodar(pol, np.array([-1.0, y0]))
        a2.plot(tr2[:, 0], tr2[:, 1], color=col, lw=1.0, alpha=0.8, zorder=3)
a2.plot([], [], color='crimson', lw=2, label='regresion sobre los dos modos')
a2.plot([], [], color=IQS_VERDE, lw=2, label='un solo modo')
a2.legend(fontsize=7, loc='lower left')
plt.tight_layout(); plt.show()"""))

C.append(md("""**Esta es la figura que justifica las diffusion policies.** Las flechas verde y azul son dos acciones perfectamente correctas; la roja es lo que el regresor predice, y apunta al tabique. No hay ningún error de entrenamiento: el modelo hace **exactamente lo que se le pidió**, minimizar el error cuadrático medio, y el minimizador del error cuadrático es la media condicional. El problema no es el ajuste, es la **hipótesis de que la acción correcta es una función del estado**. Cuando la demostración es multimodal, esa hipótesis es simplemente falsa.

Que las mismas demostraciones, el mismo modelo y el mismo entrenamiento den una política que funciona cuando se separan los modos y una que se estrella cuando se mezclan es la mejor prueba posible de que el problema está en la representación de la acción, no en la capacidad del aprendizaje.

La **política de difusión** resuelve el problema cambiando el tipo de objeto que se aprende: en lugar de una función que predice la acción, un **modelo generativo de la distribución de acciones condicionada a la observación** (Chi et al., 2023, arXiv:2303.04137). El mecanismo es el de los generadores de imágenes: en entrenamiento se aprende a quitar ruido a trayectorias de acción perturbadas; en inferencia se parte de ruido puro y se refina iterativamente, condicionando en la observación, hasta obtener una secuencia plausible. Al **muestrear** de la distribución en lugar de promediarla, el modelo elige un modo coherente —arriba o abajo, no el punto medio— y produce con naturalidad secuencias largas y suaves. El trabajo original reportó mejoras medias cercanas al 47 % sobre las líneas base de BC en una batería de tareas de manipulación (Chi et al., 2023, arXiv:2303.04137).

Nuestra separación manual de los modos es la caricatura pedagógica de esa idea: comprometerse con un modo funciona; promediarlos, no. Lo que hace una diffusion policy es lo mismo, pero sin que nadie tenga que decir a mano cuántos modos hay ni dónde están.

El precio es la **latencia**: generar cada trozo de acción requiere decenas de pasos de des-ruido, lo que compromete el control reactivo. De ahí dos evoluciones que aparecerán en los papers del seminario: acortar o destilar el muestreo, y sustituir la difusión por *flow matching* —un pariente que aprende un campo de velocidades determinista para transportar el ruido a la acción en pocos pasos de integración—, que es precisamente la cabeza de acción de π0 para emitir acciones continuas a 50 Hz (Black et al., 2024, arXiv:2410.24164).

### Ejercicio 2

Hay una tercera salida además de promediar y de separar los modos a mano: **condicionar la política**. Añade a la observación una tercera componente que indique el modo deseado (+1 «rodea por arriba», −1 «rodea por abajo»), entrena **un solo** regresor sobre los dos conjuntos mezclados y ejecútalo pidiéndole cada modo. ¿Funciona? ¿Con qué se corresponde esa tercera componente en un modelo VLA?

### Ejercicio 3

La media de las acciones no solo apunta mal: además es **más corta** que las acciones demostradas. Explica geométricamente por qué, relaciónalo con un fenómeno que ya se vio en el bloque 6 al promediar orientaciones, y discute qué tendría de malo «arreglarlo» normalizando la salida del regresor para forzar el módulo correcto."""))

C.append(code("""# Ejercicio 2: una politica condicionada por la "instruccion"
X_cond = np.vstack([np.hstack([X_arr, np.full((len(X_arr), 1), +1.0)]),
                    np.hstack([X_aba, np.full((len(X_aba), 1), -1.0)])])
Y_cond = np.vstack([Y_arr, Y_aba])
modelo_cond = ajustar_politica(X_cond, Y_cond)

for modo, nombre in [(+1.0, 'rodea por arriba'), (-1.0, 'rodea por abajo ')]:
    pol = lambda p, m=modo: PASO * modelo_cond.predict(np.append(p, m).reshape(1, -1))[0]
    print(f'instruccion "{nombre}" (modo {modo:+.0f}):  {tasa(pol)}')"""))

# ---------------- 5. VLA
C.append(md("""## 5. De aquí a los modelos VLA (parte conceptual)

Todo lo anterior cabe en dos dimensiones y cuarenta demostraciones. Los modelos **visión-lenguaje-acción** llevan exactamente la misma idea a la escala de los modelos fundacionales: se parte de un modelo visión-lenguaje preentrenado con datos de internet —que ya sabe qué es una esponja, leer una etiqueta o interpretar «recoge la mesa»— y se le añade la capacidad de emitir acciones robóticas, adaptándolo con grandes colecciones de demostraciones de muchos robots distintos (*cross-embodiment*). El lenguaje pasa a ser la interfaz de tarea.

La genealogía mínima que hay que poder recitar:

| Modelo | Aportación | Referencia |
|---|---|---|
| **RT-2** (Google DeepMind) | Expresa las acciones como *tokens* de texto para poder co-entrenar con datos web y robóticos; hereda de la web una generalización semántica que las demostraciones solas no dan, y ejecuta instrucciones sobre objetos y conceptos nunca vistos en los datos de robot | Brohan et al., 2023, arXiv:2307.15818 |
| **OpenVLA** | Abre la receta: 7.000 millones de parámetros entrenados sobre cerca de un millón de episodios reales de Open X-Embodiment, con pesos públicos; es la referencia académica reproducible | Kim et al., 2024, arXiv:2406.09246 |
| **π0** (Physical Intelligence) | Cabeza de *flow matching* sobre un backbone visión-lenguaje: acciones articulares continuas a 50 Hz, mezcla de plataformas y tareas largas y diestras como doblar ropa | Black et al., 2024, arXiv:2410.24164 |
| **GR00T N1** (NVIDIA) | Modelo fundacional abierto para humanoides, con arquitectura dual: Sistema 2 visión-lenguaje deliberativo a baja frecuencia y Sistema 1 generador de acciones por difusión a alta frecuencia; pirámide de datos reales, sintéticos y de vídeo humano | NVIDIA, 2025, arXiv:2503.14734 |
| **Gemini Robotics** | La misma apuesta desde la familia Gemini, con énfasis en razonamiento encarnado y generalización a robots nuevos | Google DeepMind, 2025, informe técnico |

Bajo el marketing, los **tres ingredientes comunes** conviene escribirlos en la pizarra: (1) un *backbone* visión-lenguaje preentrenado a escala web, que aporta semántica y lenguaje como interfaz de tarea; (2) datos robóticos multi-plataforma, porque ningún robot genera por sí solo el volumen necesario; (3) una **cabeza de acción** —tokens discretos en RT-2 y OpenVLA, difusión en GR00T N1, *flow matching* en π0— que convierte la salida del modelo en consignas motrices. Esa tercera casilla es exactamente el problema de la sección 4 de este cuaderno, resuelto de tres maneras distintas.

Y el inventario honesto de limitaciones, que es munición para el análisis crítico del seminario de S41-S42: las tasas de éxito en tareas largas siguen lejos del 100 % que exige una línea de producción; la latencia y el cómputo dificultan el despliegue a bordo; no existe todavía una evaluación estandarizada comparable entre laboratorios, porque cada paper elige sus tareas; y el rendimiento depende críticamente de la cobertura de los datos de demostración — **el VLA generaliza mejor lo semántico (objetos nuevos) que lo motriz (destrezas nuevas)**. En 2026 estos sistemas están en pilotos industriales, no en producción masiva.

Conviene cerrar el apartado con la observación que enlaza con las secciones 3 y 4: nada de lo que hemos visto desaparece por tener siete mil millones de parámetros. El desplazamiento covariante sigue ahí y se compensa con volumen y variedad de datos y con *action chunking*; la multimodalidad sigue ahí y se compensa con la cabeza de acción. Lo que cambia es la escala, no la física del problema.

### El gemelo digital, en una diapositiva

Un **gemelo digital** es una representación digital de un activo físico —una célula robotizada, una línea, una planta— mantenida en correspondencia con el activo mediante un vínculo de datos: los sensores y el control de planta actualizan el modelo, y el modelo devuelve predicciones y decisiones. El marco de referencia normativo es la serie **ISO 23247**, *Automation systems and integration — Digital twin framework for manufacturing*, citada por designación y sin página, como las normas del bloque 2.

La distinción que se pide en el examen: **un simulador a secas modela; un gemelo digital modela y está sincronizado con un activo concreto que existe.** La diferencia no es el motor de física, sino el vínculo de datos y el ciclo de vida compartido con el activo. Sus usos en fabricación, en orden de madurez: la **puesta en marcha virtual**, que valida programas de robot y de PLC, alcances, tiempos de ciclo y disposición de la célula antes de construirla —con impacto directo sobre el análisis de riesgos del bloque 2, porque permite ensayar velocidades y separaciones de los métodos colaborativos sin exponer a nadie—; la optimización en operación, alimentando el gemelo con datos reales para explorar variantes sin parar la línea; y, en la intersección con este bloque, el gemelo como **fábrica de datos**: la misma escena que valida la célula genera experiencia sintética para entrenar políticas, que es la pirámide de datos sintéticos que describe GR00T N1 (NVIDIA, 2025, arXiv:2503.14734).

El mensaje profesional para nuestros egresados, muchos de los cuales trabajarán en plantas: **el gemelo digital es hoy la puerta de entrada más realista de estas tecnologías en la fabricación** — antes de que un VLA toque la línea, habrá vivido en su gemelo."""))

C.append(md("""---

## Soluciones

**Ejercicio 1.** Una o dos rondas de DAgger bastan para recuperar los empujones que fallaban, y la tercera ya no cambia nada. El mecanismo es exactamente el que anuncia la teoría: los pares añadidos no son más demostraciones del experto sobre *su* trayectoria, sino **etiquetas del experto sobre los estados que la política visita de verdad** — que es la distribución que importa. Por eso el artículo original lo formula como un problema de aprendizaje en línea y no como «recoger más datos» (Ross, Gordon y Bagnell, 2011, AISTATS).

Lo que le pasa al conjunto de datos es igual de instructivo: crece deprisa y se **desequilibra** hacia las zonas de fallo, que quedan sobrerrepresentadas frente a la trayectoria nominal. Y la pega práctica hay que nombrarla, porque es la razón por la que DAgger se usa menos de lo que su elegancia sugiere: requiere que **el experto esté disponible durante todo el entrenamiento** para etiquetar. Aquí el experto es una función y contestar es gratis; cuando el experto es una persona con un mando de teleoperación, cada ronda de etiquetado es una sesión de laboratorio, y responder bien a «¿qué habrías hecho tú *aquí*?» sobre un estado que uno nunca provocó es sorprendentemente difícil.

**Ejercicio 2.** Funciona a la primera, y sin trampa: **un solo modelo**, entrenado sobre exactamente los mismos datos mezclados que antes se estrellaban, resuelve la tarea al cien por cien tanto si se le pide «arriba» como si se le pide «abajo». La única diferencia es que ahora el estado incluye la información que faltaba para que la acción correcta **sea** una función del estado.

Y ahí está la conexión con la sección 5, que conviene hacer explícita en la pizarra: esa tercera componente es, en miniatura, **la instrucción en lenguaje natural de un modelo VLA**. «Recoge la taza roja» y «recoge la taza azul» son dos modos incompatibles sobre la misma imagen; el lenguaje los desambigua y convierte un problema multimodal en uno unimodal condicionado. Los VLA no resuelven la multimodalidad *solo* con la cabeza de acción: buena parte del trabajo lo hace el condicionamiento.

Naturalmente, el truco tiene un límite y hay que decirlo: sirve cuando los modos son **nombrables y etiquetables**. Las cuatro maneras físicamente distintas de agarrar la misma taza no tienen nombre ni etiqueta en los datos, y ahí el condicionamiento no ayuda — hay que modelar la distribución, que es lo que hacen las diffusion policies.

**Ejercicio 3.** Geométricamente, la media de dos vectores del mismo módulo separados un ángulo θ tiene módulo `PASO · cos(θ/2)`. Cuando los dos modos apuntan a lados opuestos —en el corredor, uno dice «sube» y el otro «baja»— θ se acerca a 180° y el módulo tiende a cero. Es el mismo fenómeno que en el bloque 6 impide promediar orientaciones componente a componente: la media de dos cuaterniones no es un cuaternión válido y la media de dos ángulos no es un ángulo válido; por eso hay que usar `slerp` o promediar en el álgebra de Lie. Dicho de forma general: **el espacio de acciones no es el espacio vectorial euclídeo que la regresión supone**, y el error cuadrático medio no es la métrica correcta sobre él.

Normalizar la salida arregla el síntoma y empeora el diagnóstico: la dirección seguiría apuntando al tabique, solo que ahora el robot llegaría a él a velocidad nominal en vez de acercarse despacio. Y sobre todo se destruye la única señal que delataba el problema — un módulo anormalmente pequeño es un **detector de multimodalidad** barato y merece la pena monitorizarlo en cualquier conjunto de demostraciones antes de entrenar nada. La lección de diseño que conviene fijar: la elección de la representación de la acción (regresión directa, tokens discretos, difusión, flujo) es hoy una decisión de ingeniería de primer orden, con un compromiso explícito entre expresividad de la distribución y frecuencia de control alcanzable."""))

C.append(md("""---

## Para llevarse de esta sesión

**La imitación es aprendizaje supervisado, y por eso es a la vez tan práctica y tan frágil.** Se ahorra el diseño de la recompensa —que es donde el RL se atasca en manipulación— a cambio de heredar todos los problemas de la generalización fuera de distribución.

**El error de entrenamiento no predice el éxito de la tarea.** Un modelo que copia al experto hasta el suelo de ruido del demostrador se estrella si un empujón lo saca del carril demostrado, porque el error se realimenta paso a paso. Nombrar el fenómeno —desplazamiento covariante, errores compuestos— y conocer los tres remedios —DAgger, más y más variados datos, *action chunking*— es exactamente el nivel que se pide en el examen.

**Predecir la media de acciones multimodales es predecir una acción que ningún demostrador ejecutó nunca.** Con los mismos datos y el mismo modelo, separar los modos funciona y mezclarlos choca. Ese es el argumento entero de las diffusion policies (Chi et al., 2023, arXiv:2303.04137) y del *flow matching* de π0 (Black et al., 2024, arXiv:2410.24164), y se ve en un gráfico con cuarenta demostraciones de juguete.

Y la tesis del curso, para cerrar el bloque teórico: un modelo aprendido **no sustituye la arquitectura clásica, se instala en su nivel más alto**. El VLA observa la escena con la percepción del bloque 6 y decide qué hacer, emitiendo consignas de efector o articulares a 3-50 Hz —π0 publica acciones a 50 Hz (Black et al., 2024, arXiv:2410.24164)—; la cinemática del bloque 4 las traduce; los lazos del bloque 5 las ejecutan a centenares o miles de hercios sobre los actuadores del bloque 3; ROS 2 (bloque 7) lo comunica todo; y la seguridad del bloque 2 permanece deliberadamente **fuera** del modelo, implementada con ingeniería certificable e independiente y por debajo de cualquier componente aprendido, porque la ISO 10218:2025 exige garantías que una red entrenada no puede ofrecer por sí misma.

En una frase para cerrar el curso teórico: **el aprendizaje ha cambiado quién escribe la consigna, no quién la ejecuta** — y por eso un máster que entiende los bloques 2 a 7 está mejor preparado para la ola actual, no peor.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S40_Imitacion_VLA.ipynb', C)
print('escrito S40')
