from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('matplotlib','matplotlib'), ('scipy','scipy')]
C = []

C.append(cabecera(
    "S38", "Aprendizaje por refuerzo: MDP y Q-learning", "8",
    "miércoles 9 de diciembre de 2026", "1 h",
    "Monta un gridworld con obstáculos y meta y lo recorre tres veces: primero como MDP explícito, escribiendo la dinámica p(s',r|s,a) en una matriz y resolviendo la ecuación de optimalidad de Bellman por iteración de valor; después mirando qué son de verdad la política y la función de valor; y por último aprendiendo la misma solución **sin conocer el modelo**, con Q-learning tabular y exploración epsilon-greedy, curva de aprendizaje incluida y política final dibujada con flechas.",
    "Sutton y Barto (2018), *Reinforcement Learning: An Introduction*, 2.ª ed. — cap. 1 (ensayo y error, recompensa demorada), cap. 2 (exploración frente a explotación, epsilon-greedy), cap. 3 (MDP, retorno descontado, política, funciones de valor, ecuaciones de Bellman y de optimalidad) y cap. 6 (aprendizaje por diferencia temporal y Q-learning). Se cita por capítulo porque es la referencia de los apuntes del bloque 8.",
    "los apuntes del bloque 8"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=3, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.2)
plt.rcParams['axes.grid'] = False
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('Listo.')"""))

# ---------------- 1. El MDP
C.append(md("""## 1. El gridworld como MDP explícito

El aprendizaje por refuerzo es «el tercer paradigma» y el que mejor se ajusta a un robot: nadie proporciona la acción correcta, hay una señal escalar de recompensa a menudo demorada, y el agente genera sus propios datos al actuar (Sutton y Barto, 2018, cap. 1). La formalización estándar es el **proceso de decisión de Markov**: conjuntos S y A, dinámica p(s', r | s, a), y la propiedad de Markov —el estado resume todo lo relevante del pasado— (Sutton y Barto, 2018, cap. 3).

El escenario es el del guion de clase, ampliado a un tamaño en el que se ve algo: un AMR en una planta de 8 × 10 celdas con estanterías (obstáculos), un muelle de carga (la meta, recompensa +1) y una zona de tránsito de personas que hay que evitar (recompensa −1 y fin de episodio). Cada paso cuesta −0,04, que es la forma limpia de decir «llega pronto» sin premiar explícitamente el acercarse — y así evitamos de entrada el *reward hacking* del robot que vibra junto a la meta cosechando recompensa de aproximación.

El movimiento es **estocástico**, que es lo que lo hace interesante y realista: la acción ordenada se ejecuta con probabilidad 0,8 y con 0,1 el robot se desvía a cada lado. Es la abstracción mínima del deslizamiento de ruedas del bloque 3."""))

C.append(code("""FILAS, COLS = 8, 10
OBSTACULOS = [(2, 2), (3, 2), (4, 2), (5, 2), (2, 5), (3, 5), (4, 5), (6, 7), (5, 7), (1, 7)]
META       = (0, 9)          # muelle de carga:   recompensa +1
PELIGRO    = (1, 9)          # paso de personas:  recompensa -1
COSTE_PASO = -0.04
GAMMA      = 0.95

ACCIONES = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}     # arriba, abajo, izq, der
NOMBRES  = ['^', 'v', '<', '>']
P_ORDENADA, P_DESVIO = 0.8, 0.1

celdas = [(i, j) for i in range(FILAS) for j in range(COLS) if (i, j) not in OBSTACULOS]
idx = {c: k for k, c in enumerate(celdas)}
nS, nA = len(celdas), len(ACCIONES)
TERMINALES = {idx[META], idx[PELIGRO]}

def desplazar(c, a):
    \"\"\"Aplica un movimiento; chocar contra pared u obstaculo deja al robot donde estaba.\"\"\"
    i, j = c[0] + ACCIONES[a][0], c[1] + ACCIONES[a][1]
    return (i, j) if (0 <= i < FILAS and 0 <= j < COLS and (i, j) not in OBSTACULOS) else c

# --- dinamica explicita p(s'|s,a) y recompensa esperada r(s,a) ---
P = np.zeros((nS, nA, nS))
R = np.zeros((nS, nA))
for c, s in idx.items():
    for a in range(nA):
        if s in TERMINALES:
            P[s, a, s] = 1.0                       # estados absorbentes
            continue
        perpendiculares = [2, 3] if a in (0, 1) else [0, 1]
        for aa, p in [(a, P_ORDENADA)] + [(x, P_DESVIO) for x in perpendiculares]:
            c2 = desplazar(c, aa)
            s2 = idx[c2]
            P[s, a, s2] += p
            r = 1.0 if c2 == META else (-1.0 if c2 == PELIGRO else COSTE_PASO)
            R[s, a] += p * r

print(f'Estados: {nS}   Acciones: {nA}   gamma = {GAMMA}')
print('Suma de probabilidades por (s,a):', np.allclose(P.sum(axis=2), 1.0))
print(f'Recompensa esperada de "ir a la derecha" desde la celda vecina a la meta: '
      f'{R[idx[(0, 8)], 3]:.3f}')"""))

C.append(md("""### El retorno y la ecuación de optimalidad

El objetivo no es la recompensa inmediata sino el **retorno descontado**, G_t = r_{t+1} + γ·r_{t+2} + γ²·r_{t+3} + …, con 0 ≤ γ < 1 (Sutton y Barto, 2018, cap. 3). El descuento hace finita la suma, expresa preferencia por lo temprano y actúa como perilla de diseño: con γ cerca de 0 el agente es miope, con γ cerca de 1 pesa el largo plazo.

Como aquí **sí conocemos** p(s',r|s,a), podemos resolver el problema exactamente con la ecuación de optimalidad de Bellman,

    v*(s) = max_a  Σ_{s'} p(s'|s,a) · [ r(s,a,s') + γ · v*(s') ]

aplicándola como una asignación hasta que deja de cambiar nada. Eso es la **iteración de valor**. Conviene decir en clase que este es el caso que el RL *no* tiene: aquí conocemos el modelo del mundo. La sección 3 resolverá lo mismo sin él."""))

C.append(code("""def iteracion_de_valor(P, R, gamma=GAMMA, tol=1e-10, max_iter=5000):
    v = np.zeros(nS)
    for k in range(max_iter):
        q = R + gamma * (P @ v)                    # (nS, nA): valor de cada accion
        v_nuevo = q.max(axis=1)
        for s in TERMINALES:
            v_nuevo[s] = 0.0                       # el episodio acaba: no hay futuro
        if np.abs(v_nuevo - v).max() < tol:
            v = v_nuevo
            break
        v = v_nuevo
    return v, q.argmax(axis=1), k

v_opt, pi_opt, iters = iteracion_de_valor(P, R)
print(f'Convergencia en {iters} iteraciones')
print(f'v* en la salida (7,0): {v_opt[idx[(7, 0)]]:.3f}')
print(f'v* junto a la meta (0,8): {v_opt[idx[(0, 8)]]:.3f}')
print(f'v* junto al peligro (2,9): {v_opt[idx[(2, 9)]]:.3f}')

# ¿que hace la politica optima en la celda pegada al peligro?
c = (2, 9)
q_c = R[idx[c]] + GAMMA * (P[idx[c]] @ v_opt)
print(f'\\nValores de accion q*({c}, a):')
for a in range(nA):
    print(f'   {NOMBRES[a]}  {q_c[a]:+.3f}')"""))

C.append(md("""## 2. Política y función de valor, dibujadas

Una política π(a|s) es la ley de control del agente: la probabilidad de ejecutar a en el estado s (Sutton y Barto, 2018, cap. 3). Conviene decirlo con estas palabras en clase: **una política es exactamente lo mismo que una ley de control del bloque 5** —una función del estado a la acción—, solo que aquí no la deriva el ingeniero de un modelo, sino que la aprende el agente de datos.

Sobre ella se definen v_π(s), esperanza del retorno partiendo de s, y q_π(s,a), esperanza del retorno partiendo de s tras ejecutar a. Y la consecuencia práctica que justifica todo lo que viene: **si alguien nos regala q\\*, actuar óptimamente es trivial** — en cada estado, elegir la acción que la maximiza, sin conocer el modelo ni planificar. Por eso una familia entera de algoritmos se dedica a estimar q* de la experiencia."""))

C.append(code("""def dibujar(ax, valores, politica=None, titulo='', cmap='viridis'):
    \"\"\"Pinta el gridworld: color = valor de estado, flechas = politica.\"\"\"
    M = np.full((FILAS, COLS), np.nan)
    for c, s in idx.items():
        M[c] = valores[s]
    ax.imshow(M, cmap=cmap)
    for (i, j) in OBSTACULOS:
        ax.add_patch(plt.Rectangle((j - .5, i - .5), 1, 1, color='0.35'))
    ax.add_patch(plt.Rectangle((META[1] - .5, META[0] - .5), 1, 1, fill=False,
                               edgecolor=IQS_VERDE, lw=3))
    ax.add_patch(plt.Rectangle((PELIGRO[1] - .5, PELIGRO[0] - .5), 1, 1, fill=False,
                               edgecolor='crimson', lw=3))
    if politica is not None:
        for c, s in idx.items():
            if s in TERMINALES:
                continue
            di, dj = ACCIONES[int(politica[s])]
            ax.arrow(c[1], c[0], 0.3 * dj, 0.3 * di, head_width=0.16,
                     color='white', lw=1.2)
    ax.set_title(titulo, fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])

# comparacion: politica optima frente a una politica fija tonta ("siempre a la derecha")
pi_tonta = np.full(nS, 3)

def evaluar_politica(pi, gamma=GAMMA, tol=1e-10):
    \"\"\"v_pi resolviendo la ecuacion de Bellman de esa politica (sin maximo).\"\"\"
    v = np.zeros(nS)
    for _ in range(5000):
        v_nuevo = np.array([0.0 if s in TERMINALES else R[s, pi[s]] + gamma * P[s, pi[s]] @ v
                            for s in range(nS)])
        if np.abs(v_nuevo - v).max() < tol:
            return v_nuevo
        v = v_nuevo
    return v

v_tonta = evaluar_politica(pi_tonta)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 3.6))
dibujar(a1, v_tonta, pi_tonta, 'Politica "siempre a la derecha": v_pi')
dibujar(a2, v_opt, pi_opt, 'Politica optima: v* y pi*')
plt.tight_layout(); plt.show()

print(f'Valor medio de los estados no terminales:')
print(f'   politica tonta : {v_tonta[[s for s in range(nS) if s not in TERMINALES]].mean():+.3f}')
print(f'   politica optima: {v_opt[[s for s in range(nS) if s not in TERMINALES]].mean():+.3f}')"""))

C.append(md("""**Lo que hay que leer en la figura de la derecha.** Tres cosas, y las tres son la sesión entera:

1. El valor **decrece suavemente al alejarse de la meta**, aproximadamente como γ elevado al número de pasos que faltan. Esa es la imagen mental correcta de la función de valor: una predicción a largo plazo, no una recompensa.
2. Las flechas rodean la celda de peligro **por el lado ancho**, no pegadas a ella. Nadie ha programado ese margen: sale de que el movimiento es estocástico y pasar rozando tiene una probabilidad de 0,1 de acabar en −1. Es exactamente el mismo razonamiento que el inflado del costmap de S35, pero derivado de la incertidumbre en lugar de la geometría.
3. La política tonta tiene valor negativo en casi toda la planta: chocar contra una estantería y quedarse quieto cuesta −0,04 por paso, para siempre.

### Ejercicio 1

Cambia γ a 0,5 y a 0,995 y vuelve a resolver. ¿Cómo cambian el mapa de valores y las flechas? Fíjate especialmente en las celdas de la esquina inferior izquierda, las más lejanas a la meta. Después prueba `COSTE_PASO = 0.0` y explica qué le pasa a la política y por qué."""))

C.append(code("""# Ejercicio 1
no_terminales = [s for s in range(nS) if s not in TERMINALES]
_, pi_ref, _ = iteracion_de_valor(P, R, gamma=0.95)
for g in (0.5, 0.95, 0.995):
    v, pi, it = iteracion_de_valor(P, R, gamma=g)
    quieto = COSTE_PASO / (1 - g)          # valor de no llegar nunca a la meta
    cambia = sum(pi[s] != pi_ref[s] for s in no_terminales)
    print(f'gamma = {g:5.3f} ({it:3d} iter)  v*(7,0) = {v[idx[(7,0)]]:+7.4f}   '
          f'v*(0,8) = {v[idx[(0,8)]]:+7.4f}   '
          f'"nunca llego" = {quieto:+7.4f}   politica distinta en {cambia:2d} estados')"""))

# ---------------- 3. Q-learning
C.append(md("""## 3. Q-learning tabular: la misma solución, sin modelo

Ahora tiramos `P` y `R` a la basura. El agente solo puede **actuar y observar**: ejecuta una acción, ve dónde acaba y qué recompensa recibe. Esa es la situación real de un robot.

La idea del aprendizaje por diferencia temporal es aprender de cada transición sin esperar al final del episodio, moviendo la estimación actual hacia un objetivo construido con la recompensa observada y la propia estimación del estado siguiente (*bootstrap*). La regla que el estudiante debe saber escribir y ejecutar (Sutton y Barto, 2018, cap. 6):

    Q(s_t, a_t) ← Q(s_t, a_t) + α · [ r_{t+1} + γ · max_{a'} Q(s_{t+1}, a') − Q(s_t, a_t) ]

Cada pieza tiene nombre: **α** es la tasa de aprendizaje; el corchete es el **error de diferencia temporal**; y el **máximo** es lo que hace al algoritmo *off-policy* — aprende sobre la política codiciosa aunque los datos se generen explorando con otra.

Para generar datos hace falta explorar, y ahí aparece el dilema fundamental (Sutton y Barto, 2018, cap. 2). La solución más simple y sorprendentemente competitiva es **epsilon-greedy**: con probabilidad ε una acción al azar, si no la mejor conocida; y ε decrece con el tiempo."""))

C.append(code("""def paso_entorno(s, a, rng):
    \"\"\"El entorno: dado (s,a) devuelve (s', r, terminado). El agente NO ve esta funcion.\"\"\"
    c = celdas[s]
    perpendiculares = [2, 3] if a in (0, 1) else [0, 1]
    real = rng.choice([a] + perpendiculares, p=[P_ORDENADA, P_DESVIO, P_DESVIO])
    c2 = desplazar(c, int(real))
    if c2 == META:
        return idx[c2], 1.0, True
    if c2 == PELIGRO:
        return idx[c2], -1.0, True
    return idx[c2], COSTE_PASO, False

def q_learning(n_episodios=6000, alfa_ini=0.20, alfa_fin=0.05, gamma=GAMMA,
               eps_ini=1.0, eps_fin=0.05, max_pasos=120, semilla=38):
    rng = np.random.default_rng(semilla)
    Q = np.zeros((nS, nA))
    arranques = [s for s in range(nS) if s not in TERMINALES]
    retornos, errores = [], []
    for ep in range(n_episodios):
        eps = max(eps_fin, eps_ini * (1 - ep / (0.8 * n_episodios)))   # decae y se estabiliza
        alpha = alfa_ini + (alfa_fin - alfa_ini) * ep / n_episodios    # y alpha decrece: converge
        s = int(rng.choice(arranques))
        G, descuento = 0.0, 1.0
        for t in range(max_pasos):
            # --- epsilon-greedy ---
            a = int(rng.integers(nA)) if rng.random() < eps else int(np.argmax(Q[s]))
            s2, r, fin = paso_entorno(s, a, rng)
            # --- actualizacion de Q-learning ---
            objetivo = r + (0.0 if fin else gamma * Q[s2].max())
            Q[s, a] += alpha * (objetivo - Q[s, a])
            G += descuento * r
            descuento *= gamma
            s = s2
            if fin:
                break
        retornos.append(G)
        errores.append(np.abs(Q.max(axis=1) - v_opt).mean())
    return Q, np.array(retornos), np.array(errores)

import time
t0 = time.perf_counter()
Q, retornos, errores = q_learning()
print(f'Entrenamiento: {time.perf_counter() - t0:.1f} s, {len(retornos)} episodios')

pi_q = Q.argmax(axis=1)
v_q = Q.max(axis=1)
no_term = [s for s in range(nS) if s not in TERMINALES]
coincide = np.mean([pi_q[s] == pi_opt[s] for s in no_term])
print(f'Error medio |max_a Q(s,a) - v*(s)| : {np.abs(v_q[no_term] - v_opt[no_term]).mean():.4f}')
print(f'La politica aprendida coincide con la optima en el {100*coincide:.0f} % de los estados')"""))

C.append(code("""def suavizar(x, k=100):
    return np.convolve(x, np.ones(k) / k, mode='valid')

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 3.3))
a1.plot(suavizar(retornos), color=IQS_AZUL, lw=1.8)
a1.axhline(np.mean([v_opt[s] for s in no_term]), color=IQS_VERDE, ls='--', lw=2,
           label='retorno medio bajo pi* (referencia)')
a1.set_xlabel('episodio'); a1.set_ylabel('retorno descontado (media movil de 100)')
a1.set_title('Curva de aprendizaje', fontsize=10); a1.legend(fontsize=8); a1.grid(alpha=.3)

a2.plot(errores, color='crimson', lw=1.5)
a2.set_yscale('log')
a2.set_xlabel('episodio'); a2.set_ylabel('|max_a Q - v*| medio')
a2.set_title('Distancia a la solucion exacta', fontsize=10); a2.grid(alpha=.3)
plt.tight_layout(); plt.show()"""))

C.append(code("""fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 3.6))
dibujar(a1, v_opt, pi_opt, 'Iteracion de valor (conoce el modelo)')
dibujar(a2, v_q, pi_q, 'Q-learning (solo experiencia)')
plt.tight_layout(); plt.show()

# donde discrepan las dos politicas?
discrepan = [celdas[s] for s in no_term if pi_q[s] != pi_opt[s]]
print('Celdas donde la politica aprendida difiere de la optima:', discrepan)
for c in discrepan[:4]:
    s = idx[c]
    q_exacto = R[s] + GAMMA * (P[s] @ v_opt)
    print(f'  {c}: q* = {np.round(q_exacto, 3)}  ->  diferencia entre las dos mejores: '
          f'{np.sort(q_exacto)[-1] - np.sort(q_exacto)[-2]:.4f}')"""))

C.append(md("""**Cómo comentar el resultado.** Las dos figuras son casi la misma, y ahí está toda la gracia: **una la calculó alguien que conocía la física del mundo; la otra la aprendió un agente que solo sabe caer y levantarse**. La curva de aprendizaje sube deprisa al principio —cuando el valor «se propaga» hacia atrás desde la meta, casilla a casilla, exactamente como en el ejemplo a mano de la pizarra— y luego se aplana en el nivel de la política óptima.

Y el detalle honesto: las pocas celdas donde la política aprendida difiere de la óptima son celdas **casi indiferentes**, donde las dos mejores acciones tienen valores q* que se diferencian en milésimas. El agente no se ha equivocado en nada importante; simplemente no tiene datos suficientes para desempatar, y tampoco le hace falta.

### Ejercicio 2

Ejecuta `q_learning` con ε **fijo** en 0,02 (casi sin exploración) y con ε fijo en 0,9 (casi solo exploración), dejando todo lo demás igual. Compara las tres curvas de aprendizaje y el porcentaje de estados con política correcta. ¿Cuál aprende mejor y por qué? Relaciónalo con el dilema exploración/explotación (Sutton y Barto, 2018, cap. 2).

### Ejercicio 3

Reproduce a mano una actualización, como en la pizarra. Toma el estado `(0, 8)` —la celda pegada al muelle—, la acción «derecha», α = 0,5 y γ = 0,9, con `Q` inicialmente a cero. Calcula la actualización si el robot llega a la meta (r = +1) y comprueba el resultado con código. Después ejecuta la segunda actualización desde `(0, 7)` con la acción «derecha» y observa cómo el valor ha empezado a propagarse hacia atrás."""))

C.append(code("""# Ejercicio 2
print(f'{"exploracion":>22}  {"politica ok":>11}  {"error en v":>10}  {"retorno durante":>15}')
for etiqueta, kw in [('epsilon fijo = 0.02', dict(eps_ini=0.02, eps_fin=0.02)),
                     ('epsilon decreciente', dict()),
                     ('epsilon fijo = 0.90', dict(eps_ini=0.90, eps_fin=0.90))]:
    Q2, ret2, _ = q_learning(**kw)
    ok = np.mean([Q2.argmax(axis=1)[s] == pi_opt[s] for s in no_term])
    err = np.abs(Q2.max(axis=1)[no_term] - v_opt[no_term]).mean()
    print(f'{etiqueta:>22}  {100*ok:9.0f} %  {err:10.4f}  {ret2[-500:].mean():+15.3f}')"""))

C.append(code("""# Ejercicio 3: espacio de trabajo
# Q_mano = np.zeros((nS, nA)); alpha, gamma = 0.5, 0.9
# s = idx[(0, 8)]; a = 3   # derecha"""))

C.append(md("""---

## Soluciones

**Ejercicio 1.** El resultado numérico es más fino de lo que uno espera y merece comentarse con cuidado. Con γ = 0,5, `v*(7,0)` vale exactamente −0,0800, que es **el valor de no llegar nunca**: −0,04/(1−0,5). Desde la esquina más lejana, con γ = 0,5 la meta está a dieciséis pasos y 0,5¹⁶ ≈ 1,5·10⁻⁵ — el muelle es, literalmente, invisible desde allí. Con γ = 0,995 el valor de esa misma celda pasa a ser positivo (+0,169): la meta ya pesa. La regla práctica que hay que dictar: el **horizonte efectivo** es del orden de 1/(1−γ) pasos y debe cubrir la tarea; por eso en robótica γ ≈ 0,99.

Ahora la sorpresa: la política apenas cambia (cuatro o cinco estados de setenta). Y tiene sentido — en un mundo donde solo hay una fuente de recompensa, la dirección correcta es la misma seas miope o previsor; lo que γ cambia es **cuánto vale** estar en cada sitio, no hacia dónde ir. En tareas con recompensas en conflicto (un atajo arriesgado frente a un rodeo seguro) γ sí cambia la política, y ese es el experimento que merece proponerse en clase como extensión.

Con `COSTE_PASO = 0.0` pasa algo parecido y por la misma razón: con γ = 0,95, el propio descuento ya codifica la prisa (llegar diez pasos más tarde multiplica la recompensa por 0,95¹⁰ ≈ 0,6), así que la política solo cambia en un estado, aunque todos los valores suben mucho porque vagar deja de costar. El coste por paso se vuelve imprescindible cuando γ se acerca a 1: ahí, sin él, **todas** las políticas que acaban llegando valen lo mismo y el agente no tiene ningún motivo para darse prisa. Es el primer ejemplo de diseño de recompensa del curso, y el aviso que lo acompaña: el agente optimiza lo que se mide, no lo que se quiso decir.

**Ejercicio 2.** La tabla separa dos cosas que los estudiantes tienden a confundir: **lo bien que se aprende** y **lo bien que se vive mientras se aprende**.

Con ε = 0,02 el agente explota casi siempre lo que cree saber, y como al principio no sabe nada se queda dando vueltas por la zona que descubrió primero: aprende bien esa región y peor el resto, y el porcentaje de política correcta se desploma. Con ε = 0,9 ocurre algo que sorprende a casi todo el mundo: la tabla Q converge **casi tan bien como con la estrategia decreciente**, muy por encima del caso poco explorador. No es un error — Q-learning es *off-policy*, así que la regla del máximo aprende sobre la política codiciosa aunque el comportamiento sea casi aleatorio, y comportarse al azar es una forma estupenda de visitar indefinidamente todos los pares (s,a), que es justo la condición de convergencia del libro (Sutton y Barto, 2018, cap. 6). Lo que se paga está en la última columna: el retorno obtenido **durante** el entrenamiento es negativo, frente al positivo de las otras dos, porque nueve de cada diez acciones son aleatorias y el robot se mete en la zona de peligro sin parar.

Y ahí está la conclusión, que conviene enunciar en voz alta: en simulación, explorar es gratis y ε alto sale barato; **en un robot real, explorar significa chocar**. Por eso el RL sobre hardware físico gira en torno a explorar poco, con seguridad, o a no explorar en el robot en absoluto — que es el argumento de la sesión de mañana.

**Ejercicio 3.** La primera actualización, con Q a cero y el episodio terminando en la meta:

```
Q(s, a) <- 0 + 0.5 * [ 1.0 + 0 (terminal) - 0 ] = 0.5
```

La segunda, desde `(0,7)` con «derecha», llegando a `(0,8)` sin terminar:

```
Q(s', a) <- 0 + 0.5 * [ -0.04 + 0.9 * max_a Q((0,8), a) - 0 ]
          = 0.5 * [ -0.04 + 0.9 * 0.5 ] = 0.205
```

Ese 0,205 es **la recompensa de la meta viajando hacia atrás un paso**, atenuada por α y por γ. Repetido miles de veces por todos los estados, ese goteo es literalmente todo lo que hace Q-learning. Merece la pena hacerlo a mano en la pizarra antes de enseñar el código: la imagen del valor que fluye desde la recompensa hacia los estados lejanos es la que hay que llevarse."""))

C.append(md("""---

## Para llevarse de esta sesión

**Un MDP son cuatro cosas: estados, acciones, dinámica y recompensa.** Modelar bien la tarea es elegir esas cuatro, y la propiedad de Markov no es un teorema sino una decisión de diseño del ingeniero: la pose y las velocidades de un vehículo suelen ser un buen estado; la última imagen de cámara, a menudo no.

**La función de valor es una predicción, no una recompensa.** Es lo que permite actuar bien a largo plazo con decisiones locales, y explica por qué la política óptima rodea el peligro por el lado ancho sin que nadie se lo haya programado.

**Q-learning llega a la misma respuesta sin conocer el mundo**, con una regla de una línea y muchísima experiencia. El precio es exactamente ese: experiencia. Aquí han hecho falta seis mil episodios para una planta de setenta celdas.

Y ese precio es la pregunta con la que se cierra la clase: ¿qué pasa con la tabla Q si el estado es una imagen de 640×480, o el vector de 12 posiciones y 12 velocidades articulares de un cuadrúpedo? La tabla de este cuaderno tiene 70 × 4 = 280 números. La del cuadrúpedo no cabe en ningún sitio, y discretizarla explota combinatoriamente. La salida —aproximar Q, o mejor la propia política, con una red neuronal— es el programa de S39.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S38_MDP_Q_learning.ipynb', C)
print('escrito S38')
