from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('matplotlib','matplotlib'), ('scipy','scipy')]
C = []

C.append(cabecera(
    "S31", "SLAM: del EKF al grafo de poses", "6",
    "viernes 20 de noviembre de 2026", "2 h",
    "Cierra el bloque con las dos grandes familias del SLAM funcionando de verdad: un EKF-SLAM con balizas de posición desconocida, en el que el vector de estado crece cada vez que aparece una baliza nueva y las correlaciones cruzadas hacen que reobservar un hito antiguo corrija el mapa entero; y después la optimización de un grafo de poses en 2D resuelto por mínimos cuadrados con scipy, donde una sola arista de cierre de bucle redistribuye la deriva a lo largo de toda la trayectoria.",
    "Thrun, Burgard y Fox (2005), caps. 9-13 — huevo y gallina del cartografiado (p. 282), SLAM online frente a completo (pp. 309-310), EKF-SLAM como el algoritmo más temprano e influyente (p. 312), algoritmo EKF_SLAM (p. 321), lista provisional de hitos candidatos (p. 329), límite de ~1000 características (p. 330), coste cuadrático (p. 331), GraphSLAM resuelve el SLAM completo (p. 337), grafo de restricciones blandas (p. 339), FastSLAM Rao-Blackwellizado (pp. 437-439), cierre de bucle (p. 472), rejillas de ocupación (pp. 281-286). Corke (2023), cap. 6 — huevo y gallina (p. 227), construcción EKF-SLAM (pp. 227-228), matriz de covarianza del mapa (p. 229), pose-graph y pesos por calidad del sensor (pp. 230-232).",
    "los apuntes del bloque 6"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
np.set_printoptions(precision=3, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.2)
plt.rcParams['axes.grid'] = True
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('Listo.')"""))

# ---------------- 1. El problema
C.append(md("""## 1. El problema SLAM: cuando el mapa también es incógnita

En S29 y S30 el mapa venía dado. Cuando no lo tenemos, localización y cartografiado hay que resolverlos a la vez, y ambos libros usan la misma imagen doméstica: «este es un problema de "huevo y gallina": necesitamos un mapa para localizarnos y necesitamos localizarnos para construir el mapa» (Corke, 2023, p. 227; la misma imagen en Thrun et al., 2005, p. 282).

La formalización distingue dos problemas, y la distinción no es pedantería porque determina qué algoritmos aplican (Thrun et al., 2005, pp. 309-310):

- **SLAM online**: estimar la pose *actual* y el mapa, p(x_t, m | z₁:t, u₁:t), descartando el pasado a medida que se filtra. Es lo que hace un filtro — y por tanto lo que hará nuestro EKF-SLAM.
- **SLAM completo**: estimar la *trayectoria entera* junto con el mapa, p(x₁:t, m | z₁:t, u₁:t). Es lo que hace un optimizador sobre toda la historia — GraphSLAM «resuelve el problema de SLAM completo» (Thrun et al., 2005, p. 337).

Montamos el escenario: un robot diferencial recorre un circuito cerrado de unos 56 m con balizas cuya posición **no conoce**. Reutilizamos el modelo de movimiento por odometría de S29 y el modelo de observación de rango y rumbo."""))

C.append(code("""def envolver(a):
    return (a + np.pi) % (2*np.pi) - np.pi

def g(x, u):
    r1, tr, r2 = u
    th = x[2]
    return np.array([x[0] + tr*np.cos(th + r1), x[1] + tr*np.sin(th + r1),
                     envolver(th + r1 + r2)])

def G_jac(x, u):
    r1, tr, _ = u
    th = x[2]
    return np.array([[1., 0., -tr*np.sin(th + r1)], [0., 1., tr*np.cos(th + r1)], [0., 0., 1.]])

def V_jac(x, u):
    r1, tr, _ = u
    th = x[2]
    return np.array([[-tr*np.sin(th + r1), np.cos(th + r1), 0.],
                     [ tr*np.cos(th + r1), np.sin(th + r1), 0.],
                     [ 1., 0., 1.]])

ALFA = np.array([0.002, 0.002, 0.005, 0.002])

def M_ruido(u):
    r1, tr, r2 = u
    return np.diag([ALFA[0]*r1**2 + ALFA[1]*tr**2,
                    ALFA[2]*tr**2 + ALFA[3]*(r1**2 + r2**2),
                    ALFA[0]*r2**2 + ALFA[1]*tr**2])

# --- circuito cerrado: cuatro rectas y cuatro curvas de 90 grados ---
U = []
for _ in range(4):
    U += [np.array([0.0, 0.60, 0.0])] * 20
    U += [np.array([np.pi/40, 0.16, np.pi/40])] * 10

VERDAD = [np.array([0.0, 0.0, 0.0])]
for u in U:
    VERDAD.append(g(VERDAD[-1], u))               # la trayectoria verdadera cierra el bucle exactamente
VERDAD = np.array(VERDAD)

# --- odometria: lo que el robot CREE que ha hecho ---
rng = np.random.default_rng(31)
U_ODO = [u + rng.normal(0, np.maximum(np.sqrt(np.diag(M_ruido(u))), 1e-12)) for u in U]
ODO = [np.array([0.0, 0.0, 0.0])]
for u in U_ODO:
    ODO.append(g(ODO[-1], u))
ODO = np.array(ODO)

BALIZAS = np.array([[3.0, -1.5], [9.0, -1.0], [14.5, 3.0], [14.0, 9.0], [10.0, 15.0],
                    [4.0, 15.5], [-2.0, 11.0], [-2.0, 4.0], [6.0, 7.0]])
Q = np.diag([0.05**2, np.deg2rad(1.5)**2])
ALCANCE = 7.0

print(f'{len(U)} pasos, recorrido de {sum(u[1] for u in U):.1f} m, {len(BALIZAS)} balizas')
print(f'La trayectoria verdadera vuelve al origen con error {np.linalg.norm(VERDAD[-1,:2]):.3f} m')
print(f'La odometría integrada acaba a {np.linalg.norm(ODO[-1,:2] - VERDAD[-1,:2]):.2f} m de la verdad')
print(f'Dimensión del estado en SLAM: 3 + 2N = {3 + 2*len(BALIZAS)} si se descubren todas')"""))

# ---------------- 2. EKF-SLAM
C.append(md("""## 2. EKF-SLAM: el estado que crece

«Históricamente, el más temprano —y quizá el más influyente— algoritmo de SLAM se basa en el filtro de Kalman extendido» (Thrun et al., 2005, p. 312). La construcción cabe en una frase: **aumentar el estado**. El vector pasa a ser la pose seguida de las coordenadas de los hitos descubiertos, de dimensión 3 + 2N en el plano, y el EKF de S28 se aplica tal cual sobre ese estado gigante (algoritmo EKF_SLAM en Thrun et al., 2005, p. 321; la misma construcción en Corke, 2023, pp. 227-228).

Hay tres piezas de código, y solo la tercera es nueva respecto a S29:

1. **Predicción** — solo cambia el bloque de la pose, pero hay que propagar también los bloques cruzados pose-mapa. Los hitos no se mueven, así que su bloque no toca.
2. **Corrección** — idéntica a S29, salvo que la jacobiana H tiene columnas no nulas en la pose *y* en el hito observado.
3. **Inicialización de un hito nuevo** — el estado y la covarianza *crecen*. La posición inicial sale del modelo de observación invertido, y su incertidumbre hereda la de la pose desde la que se vio."""))

C.append(code("""def h_baliza(pose, m):
    dx, dy = m[0] - pose[0], m[1] - pose[1]
    return np.array([np.hypot(dx, dy), envolver(np.arctan2(dy, dx) - pose[2])])

def H_baliza(pose, m):
    \"\"\"Devuelve las dos submatrices: derivada respecto a la pose (2x3) y al hito (2x2).\"\"\"
    dx, dy = m[0] - pose[0], m[1] - pose[1]
    q = dx*dx + dy*dy
    r = np.sqrt(q)
    H_pose = np.array([[-dx/r, -dy/r,  0.], [ dy/q, -dx/q, -1.]])
    H_hito = np.array([[ dx/r,  dy/r], [-dy/q,  dx/q]])
    return H_pose, H_hito

def anadir_hito(mu, P, z):
    \"\"\"Inicializa un hito nuevo: crece el estado y crece la covarianza.\"\"\"
    r, phi = z
    ang = mu[2] + phi
    m = np.array([mu[0] + r*np.cos(ang), mu[1] + r*np.sin(ang)])
    Gx = np.array([[1., 0., -r*np.sin(ang)], [0., 1., r*np.cos(ang)]])   # d m / d pose
    Gz = np.array([[np.cos(ang), -r*np.sin(ang)], [np.sin(ang), r*np.cos(ang)]])  # d m / d z
    n = P.shape[0]
    P_nuevo = np.zeros((n+2, n+2))
    P_nuevo[:n, :n] = P
    cruzada = Gx @ P[:3, :]                       # correlacion del hito nuevo con TODO lo anterior
    P_nuevo[n:, :n] = cruzada
    P_nuevo[:n, n:] = cruzada.T
    P_nuevo[n:, n:] = Gx @ P[:3, :3] @ Gx.T + Gz @ Q @ Gz.T
    return np.concatenate([mu, m]), P_nuevo"""))

C.append(code("""rng = np.random.default_rng(131)
mu = np.array([0.0, 0.0, 0.0])          # el origen del mapa lo define la pose inicial, por definicion
P = np.zeros((3, 3))                    # y por tanto se conoce sin error
indice = {}                             # id de baliza -> posicion en el vector de estado

traza_pose, traza_hito, n_hitos, POSES = [], {j: [] for j in range(len(BALIZAS))}, [], []
for k, u in enumerate(U_ODO):
    # ---- 1. prediccion: solo la pose se mueve, pero arrastra sus correlaciones ----
    Gk, Vk = G_jac(mu[:3], u), V_jac(mu[:3], u)
    P[:3, :3] = Gk @ P[:3, :3] @ Gk.T + Vk @ M_ruido(u) @ Vk.T
    if P.shape[0] > 3:
        P[:3, 3:] = Gk @ P[:3, 3:]
        P[3:, :3] = P[:3, 3:].T
    mu[:3] = g(mu[:3], u)

    # ---- 2 y 3. observaciones ----
    for j, m_verdadero in enumerate(BALIZAS):
        z_ideal = h_baliza(VERDAD[k+1], m_verdadero)
        if z_ideal[0] > ALCANCE:
            continue
        z = z_ideal + rng.normal(0, np.sqrt(np.diag(Q)))
        z[1] = envolver(z[1])
        if j not in indice:                          # baliza nueva: el estado CRECE
            indice[j] = P.shape[0]
            mu, P = anadir_hito(mu, P, z)
            continue
        s = indice[j]                                # baliza conocida: correccion normal
        H_pose, H_hito = H_baliza(mu[:3], mu[s:s+2])
        H = np.zeros((2, P.shape[0]))
        H[:, :3] = H_pose
        H[:, s:s+2] = H_hito
        S = H @ P @ H.T + Q
        K = P @ H.T @ np.linalg.inv(S)
        y = z - h_baliza(mu[:3], mu[s:s+2]); y[1] = envolver(y[1])
        mu = mu + K @ y; mu[2] = envolver(mu[2])
        P = (np.eye(P.shape[0]) - K @ H) @ P

    POSES.append(mu[:3].copy())
    n_hitos.append(len(indice))
    traza_pose.append(float(np.trace(P[:3, :3])))
    for j, s in indice.items():
        traza_hito[j].append((k, float(np.trace(P[s:s+2, s:s+2]))))

POSES = np.array(POSES)
err_mapa = np.array([np.linalg.norm(mu[indice[j]:indice[j]+2] - BALIZAS[j]) for j in sorted(indice)])
print(f'Balizas descubiertas: {len(indice)}  ->  dimensión final del estado: {P.shape[0]}')
print(f'Error medio del mapa estimado: {err_mapa.mean():.3f} m  (peor baliza: {err_mapa.max():.3f} m)')
print(f'Error de la pose final: EKF-SLAM {np.linalg.norm(POSES[-1,:2]-VERDAD[-1,:2]):.3f} m'
      f'   frente a odometría sola {np.linalg.norm(ODO[-1,:2]-VERDAD[-1,:2]):.3f} m')"""))

C.append(code("""fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.5, 5.0),
                             gridspec_kw={'width_ratios': [1.25, 1]})
a1.plot(VERDAD[:,0], VERDAD[:,1], color='black', lw=2.2, label='trayectoria verdadera')
a1.plot(ODO[:,0], ODO[:,1], color='crimson', lw=1.5, ls='--', label='odometría integrada')
a1.plot(POSES[:,0], POSES[:,1], color=IQS_AZUL, lw=1.8, label='EKF-SLAM')
a1.scatter(BALIZAS[:,0], BALIZAS[:,1], marker='*', s=230, color=IQS_VERDE,
           edgecolors='black', lw=0.6, zorder=5, label='balizas verdaderas')
mapa = np.array([mu[indice[j]:indice[j]+2] for j in sorted(indice)])
a1.scatter(mapa[:,0], mapa[:,1], marker='x', s=90, color=IQS_AZUL, lw=2.2, zorder=6,
           label='mapa estimado')
a1.set_aspect('equal'); a1.legend(fontsize=8); a1.set_xlabel('x [m]'); a1.set_ylabel('y [m]')
a1.set_title('El robot construye el mapa mientras se localiza en él', fontsize=10)

a2.plot(traza_pose, color=IQS_AZUL, lw=2, label='traza de P de la pose')
a2b = a2.twinx()
a2b.step(range(len(n_hitos)), n_hitos, color=IQS_VERDE, lw=1.6, where='post',
         label='balizas en el estado')
a2b.set_ylabel('nº de balizas en el estado'); a2b.grid(False)
a2.set_xlabel('paso'); a2.set_ylabel('incertidumbre de la pose')
a2.legend(fontsize=8, loc='upper left'); a2b.legend(fontsize=8, loc='lower right')
a2.set_title('La incertidumbre crece... hasta el cierre de bucle', fontsize=10)
plt.tight_layout(); plt.show()"""))

C.append(md("""**El momento que hay que señalar con el dedo.** La curva azul de la derecha crece durante todo el recorrido —el robot se aleja de la zona bien conocida— y en torno al paso 95 se desploma. Ahí el robot ha vuelto al punto de partida y ha vuelto a ver las primeras balizas, que conoce muy bien porque las midió cuando su propia pose era casi exacta. Eso es un **cierre de bucle** dentro de un filtro, y ocurre solo, sin ningún módulo dedicado: es la consecuencia de que el mapa y la pose viven en la misma gaussiana.

### Ejercicio 1

Reduce el alcance del sensor a 4 m y vuelve a ejecutar. ¿Cuántas balizas descubre? ¿Qué le pasa a la traza de P y al error del mapa? Prueba después a poner las nueve balizas dentro de un cuadrado de 3 m en el centro del circuito."""))

C.append(code("""# Ejercicio 1: prueba aqui
# ALCANCE = 4.0     (y re-ejecuta la celda del filtro)"""))

# ---------------- 3. Las correlaciones
C.append(md("""## 3. Las correlaciones: por qué reobservar un hito corrige todo el mapa

Aquí está la magia del SLAM, y es puramente algebraica. Los bloques **no diagonales** de la covarianza guardan las correlaciones cruzadas entre la pose y cada hito, y entre los hitos entre sí. Cuando el robot corrige su pose con una baliza, esas correlaciones propagan la corrección a todo lo demás: la matriz de covarianza de Corke (2023, p. 229) lo muestra gráficamente, y es la figura que hay que proyectar.

Dibujémosla con nuestros propios números."""))

C.append(code("""desv = np.sqrt(np.diag(P))
CORR = P / np.outer(desv, desv)                 # matriz de correlacion: mas legible que la covarianza

fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.5, 4.6),
                             gridspec_kw={'width_ratios': [1, 1.25]})
im = a1.imshow(np.abs(CORR), cmap='inferno', vmin=0, vmax=1)
a1.axhline(2.5, color='white', lw=1.2); a1.axvline(2.5, color='white', lw=1.2)
a1.set_title('|correlación| del estado completo (3 + 2N)', fontsize=10)
a1.set_xlabel('pose  |  balizas'); a1.grid(False)
plt.colorbar(im, ax=a1, fraction=0.046)

for j, color in [(0, IQS_AZUL), (5, 'crimson'), (6, IQS_VERDE)]:
    serie = np.array(traza_hito[j])
    a2.plot(serie[:, 0], serie[:, 1], color=color, lw=2,
            label=f'baliza {j} (descubierta en el paso {int(serie[0,0])})')
a2.set_xlabel('paso'); a2.set_ylabel('traza de P del hito')
a2.legend(fontsize=8); a2.set_title('La incertidumbre de un hito nunca sube', fontsize=10)
plt.tight_layout(); plt.show()

# Comprobamos primero que estos pares NUNCA estuvieron a la vista a la vez
visibles = [{j for j, m in enumerate(BALIZAS) if h_baliza(p, m)[0] <= ALCANCE} for p in VERDAD[1:]]
print('Correlación entre pares de balizas que nunca se vieron a la vez:')
for i, j in [(0, 4), (2, 6), (3, 6)]:
    juntas = any(i in s and j in s for s in visibles)
    print(f'  baliza {i} y baliza {j}:  correlación {CORR[indice[i], indice[j]]:+.3f}'
          f'   ¿coincidieron alguna vez a la vista? {"sí" if juntas else "no"}')
print('\\nNunca se vieron juntas y sin embargo están correlacionadas:')
print('la pose del robot las conectó al pasar. Eso es exactamente lo que hace SLAM.')"""))

C.append(md("""Dos lecturas que hay que hacer sobre esas gráficas.

**Primera: la incertidumbre de un hito nunca crece.** A diferencia de la pose, que se degrada entre observaciones, un hito solo puede mejorar — no se mueve, así que la predicción no le añade ruido. Su traza baja a saltos y se queda plana. En el límite, la incertidumbre del mapa converge a un valor no nulo que depende de la incertidumbre inicial de la pose desde la que se vio la primera baliza: el mapa está anclado al origen, y esa parte de la incertidumbre no se elimina nunca.

**Segunda: las balizas acaban correlacionadas aunque nunca se hayan visto juntas.** La pose del robot fue el intermediario. Y por eso una corrección local se propaga globalmente — que es la virtud del EKF-SLAM y también su factura, porque cada actualización toca toda la matriz: «las actualizaciones requieren un tiempo cuadrático en el número de hitos del mapa» (Thrun et al., 2005, p. 331), lo que en la práctica lo confina «a mapas relativamente escasos, con menos de 1000 características» (Thrun et al., 2005, p. 330).

### Ejercicio 2

Mide el coste real: cronometra un paso completo del filtro con 9, 50 y 200 balizas (puedes generarlas al azar y forzar su inicialización) y comprueba si la curva es cuadrática. Contrasta el resultado con la afirmación del libro."""))

C.append(code("""# Ejercicio 2: prueba aqui
# import time
# for N in [9, 50, 200]:
#     dim = 3 + 2*N; Pn = np.eye(dim); Hn = np.zeros((2, dim))"""))

# ---------------- 4. Grafo de poses
C.append(md("""## 4. El grafo de poses y el cierre de bucle por mínimos cuadrados

La segunda familia cambia la pregunta: en lugar de filtrar hacia delante, acumula restricciones y optimiza todo a la vez. El contraste lo da el propio Thrun: «mientras que el EKF representa la información mediante una matriz de covarianza y un vector de medias, GraphSLAM representa la información como un grafo de restricciones blandas», con la consecuencia computacional en forma de exclamación: «actualizar la covarianza en un EKF es computacionalmente costoso; ¡hacer crecer el grafo es barato!» (Thrun et al., 2005, p. 339).

La formulación operativa moderna es el **pose-graph** (Corke, 2023, pp. 230-232): los nodos son poses del robot, las aristas son restricciones —odometría entre poses consecutivas, cierres de bucle entre poses lejanas en el tiempo—, cada una ponderada por la confianza en el sensor que la produjo (Corke, 2023, p. 232), y resolver el SLAM es minimizar por mínimos cuadrados no lineales el error total del grafo.

Lo montamos con `scipy.optimize.least_squares` sobre la misma trayectoria. Submuestreamos a un nodo cada cuatro pasos."""))

C.append(code("""def relativa(a, b):
    \"\"\"Pose de b vista desde a: la resta en SE(2).\"\"\"
    c, s = np.cos(a[2]), np.sin(a[2])
    d = b[:2] - a[:2]
    return np.array([c*d[0] + s*d[1], -s*d[0] + c*d[1], envolver(b[2] - a[2])])

SALTO = 4
NODOS = np.arange(0, len(VERDAD), SALTO)
V_VERDAD, V_ODO = VERDAD[NODOS], ODO[NODOS]
N = len(NODOS)

# --- aristas: odometria entre nodos consecutivos ---
ARISTAS = [(i, i+1, relativa(V_ODO[i], V_ODO[i+1]), np.array([0.05, 0.05, 0.02]))
           for i in range(N-1)]

# --- una arista mas: el CIERRE DE BUCLE. El robot reconoce el punto de partida ---
z_cierre = relativa(V_VERDAD[-1], V_VERDAD[0]) + np.array([0.02, 0.02, 0.005])
ARISTAS.append((N-1, 0, z_cierre, np.array([0.03, 0.03, 0.01])))

def desempaquetar(p):
    \"\"\"El nodo 0 se fija en el origen: sin eso el problema tiene 3 grados de libertad libres.\"\"\"
    return np.vstack([np.zeros(3), p.reshape(-1, 3)])

def residuos(p):
    V = desempaquetar(p)
    r = []
    for i, j, z, sigma in ARISTAS:
        e = relativa(V[i], V[j]) - z
        e[2] = envolver(e[2])
        r.append(e / sigma)              # ponderar por la calidad del sensor de cada arista
    return np.concatenate(r)

p0 = V_ODO[1:].ravel().copy()            # arrancamos de la odometria: es la mejor estimacion inicial
chi2_0 = float(np.sum(residuos(p0)**2))
sol = least_squares(residuos, p0, method='lm', xtol=1e-10, ftol=1e-10)
V_OPT = desempaquetar(sol.x)

print(f'Nodos: {N}   aristas: {len(ARISTAS)} '
      f'({N-1} de odometría + 1 de cierre de bucle)')
print(f'Incógnitas: {3*(N-1)}   residuos: {3*len(ARISTAS)}')
print(f'\\nchi2 antes de optimizar : {chi2_0:10.1f}')
print(f'chi2 después            : {2*sol.cost:10.1f}   ({sol.nfev} evaluaciones)')

err = lambda A: float(np.linalg.norm(A[:, :2] - V_VERDAD[:, :2], axis=1).mean())
print(f'\\nError medio de la trayectoria:  odometría {err(V_ODO):.3f} m'
      f'  ->  grafo optimizado {err(V_OPT):.3f} m')
print(f'Distancia entre el último nodo y el primero: {np.linalg.norm(V_ODO[-1,:2]-V_ODO[0,:2]):.3f} m'
      f'  ->  {np.linalg.norm(V_OPT[-1,:2]-V_OPT[0,:2]):.3f} m')"""))

C.append(code("""fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(13.5, 4.4))
for ax, (V, tit, color) in zip((a1, a2), [
        (V_ODO, f'ANTES: odometría\\nerror medio {err(V_ODO):.2f} m', 'crimson'),
        (V_OPT, f'DESPUÉS: grafo optimizado\\nerror medio {err(V_OPT):.2f} m', IQS_AZUL)]):
    ax.plot(V_VERDAD[:,0], V_VERDAD[:,1], color='black', lw=2.2, label='verdad')
    ax.plot(V[:,0], V[:,1], color=color, lw=1.8, marker='o', ms=3, label='estimación')
    ax.plot([V[-1,0], V[0,0]], [V[-1,1], V[0,1]], color=IQS_VERDE, lw=2.2, ls=':',
            label='arista de cierre')
    ax.set_aspect('equal'); ax.legend(fontsize=8); ax.set_title(tit, fontsize=10)
    ax.set_xlabel('x [m]')

d_odo = np.linalg.norm(V_ODO[:,:2] - V_VERDAD[:,:2], axis=1)
d_opt = np.linalg.norm(V_OPT[:,:2] - V_VERDAD[:,:2], axis=1)
a3.plot(d_odo, color='crimson', lw=1.9, label='odometría')
a3.plot(d_opt, color=IQS_AZUL, lw=1.9, label='grafo optimizado')
a3.set_xlabel('nodo'); a3.set_ylabel('error de posición [m]'); a3.legend(fontsize=8)
a3.set_title('El cierre reparte el error\\npor toda la trayectoria', fontsize=10)
plt.tight_layout(); plt.show()"""))

C.append(md("""**El momento estelar del SLAM.** Reobservar un lugar antiguo añade **una sola arista** al grafo y, al reoptimizar, esa arista redistribuye el error acumulado a lo largo de toda la trayectoria: nótese en la tercera gráfica que el error del optimizado no es cero en ninguna parte, pero tampoco crece sin freno — se ha *repartido*. Es exactamente lo que un filtro no puede hacer, porque un filtro solo puede corregir el presente (el fenómeno se ilustra en Thrun et al., 2005, p. 472).

Conviene ser honesto sobre lo que la optimización **no** hace: no recupera la trayectoria verdadera. Una única restricción de bucle solo dice «el principio y el final coinciden»; con esa información, el error medio baja de unos 3,3 m a menos de 1 m, pero no a cero. Añadir más cierres de bucle —cada vez que el robot cruza su propio camino— es lo que hace que un mapa real quede métricamente correcto.

Y una nota de implementación que se ve en el código: hay que **fijar un nodo**. Sin él, el problema tiene tres grados de libertad libres (trasladar y rotar el grafo entero no cambia ninguna restricción relativa) y el sistema normal es singular. En los optimizadores serios eso se llama fijar la *gauge*, y se hace anclando un nodo o añadiendo un prior.

Esta formulación como grafo de factores es hoy el estándar de facto de la industria, con optimizadores como g2o, GTSAM o Ceres bajo el capó de la mayoría de sistemas comerciales y de investigación.

### Ejercicio 3

Sube el sigma de la arista de cierre de bucle de 0,03 a 3,0 (es decir, di que el reconocimiento de lugar es poco fiable) y vuelve a optimizar. ¿Qué pasa con el error? Después haz lo contrario, bájalo a 0,001. ¿Qué le pasa a la forma del circuito, y qué te dice eso sobre pesar bien las aristas (Corke, 2023, p. 232)?"""))

C.append(code("""# Ejercicio 3: prueba aqui
# ARISTAS[-1] = (N-1, 0, z_cierre, np.array([3.0, 3.0, 1.0]))
# sol2 = least_squares(residuos, p0, method='lm'); V2 = desempaquetar(sol2.x)"""))

# ---------------- 5. Panorama
C.append(md("""## 5. Panorama: FastSLAM, rejillas, SLAM visual y reconstrucción neuronal

Lo que queda del temario no se programa aquí, pero con las dos implementaciones anteriores ya se puede situar todo en el mapa.

**FastSLAM** rescata las partículas de S30 con un truco de factorización. Un filtro de partículas ingenuo sobre el estado conjunto pose+mapa es inviable por dimensión, pero FastSLAM usa partículas para representar la distribución sobre **trayectorias** y explota que, condicionado a una trayectoria conocida, los hitos son independientes entre sí: cada partícula lleva su propia trayectoria y su propio mapa formado por pequeños EKF de dimensión 2, uno por hito (Thrun et al., 2005, pp. 437-439). Eso resuelve de golpe el coste cuadrático de la sección 3 y la asociación de datos, que cada partícula decide por su cuenta — las que se equivocan mueren en el remuestreo. El precio es el de siempre: en bucles largos, pocas partículas conservan la trayectoria correcta (Thrun et al., 2005, pp. 471-472).

**Rejillas de ocupación.** En robótica móvil de interior el mapa no suele ser una lista de hitos sino una rejilla de celdas con probabilidad de ocupación, estimada suponiendo la trayectoria conocida (Thrun et al., 2005, p. 281). La actualización usa la representación log-odds, que convierte el producto de evidencias en una suma: l_t,i = l_t−1,i + modelo_inverso − l₀ (algoritmo en Thrun et al., 2005, p. 286). Es exactamente la representación que los equipos verán en el bloque 7: `slam_toolbox` produce rejillas que Nav2 consume para costear y planificar.

**SLAM visual.** Aquí se cierra el círculo del bloque: los hitos son los puntos con descriptor de S26 y el sensor es la cámara calibrada de S25. ORB-SLAM integra en tiempo real seguimiento, cartografiado, relocalización y cierre de bucle sobre un grafo optimizado (Mur-Artal et al., 2015, arXiv:1502.00956) — arquitectónicamente es el pose-graph de la sección 4 cuyo modelo de observación es la proyección perspectiva de S25. Verlo así es el examen conceptual del bloque.

**La frontera.** NeRF representa la escena como un campo neuronal de densidad y radiancia optimizado para reproducir las vistas de entrada (Mildenhall et al., 2020, arXiv:2003.08934); 3D Gaussian Splatting sustituye la red por millones de gaussianas 3D explícitas y alcanza calidad estado del arte con renderizado en tiempo real (Kerbl et al., 2023, arXiv:2308.04079). Ambas se están incorporando como representación del mapa dentro de sistemas de SLAM denso.

**La tesis final del bloque**, que el cuestionario comprobará: las representaciones del mapa cambian cada década —rejillas, puntos, campos neuronales, gaussianas—, pero el esqueleto no ha cambiado desde el capítulo 2 de Thrun: modelos probabilísticos de movimiento y observación, una creencia sobre el estado, y predicción-corrección u optimización para reconciliarlos."""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.** Con 4 m de alcance el robot descubre menos balizas y, sobre todo, pasa tramos largos sin ver ninguna: la traza de P crece mucho más entre observaciones y el error del mapa empeora, porque cada baliza nueva se inicializa desde una pose peor conocida y esa incertidumbre se le queda dentro para siempre. Con las nueve balizas apiñadas en el centro ocurre algo peor y muy instructivo: el robot las ve todas casi en la misma dirección durante buena parte del recorrido, la geometría queda mal condicionada y el mapa se estira. Es la dilución de precisión de S29, ahora afectando también al mapa.

**Ejercicio 2.** El coste por paso crece aproximadamente como el cuadrado de la dimensión del estado, dominado por los productos `P @ H.T` y `(I − K H) @ P`, que son O(n²) con n = 3 + 2N. Con 200 hitos el estado tiene 403 componentes y cada corrección mueve una matriz de 403×403; multiplicado por varias observaciones por paso y por miles de pasos, se entiende el límite práctico de ~1000 características que da el libro (Thrun et al., 2005, p. 330). Este es el problema que FastSLAM y los grafos resuelven, cada uno a su manera.

**Ejercicio 3.** Con sigma = 3,0 la arista de cierre casi no pesa: la optimización apenas mueve nada y el resultado se parece a la odometría; el bucle sigue abierto. Con sigma = 0,001 pasa lo contrario: el cierre se impone de forma casi rígida y la optimización deforma el resto del circuito para satisfacerlo, dejando las rectas dobladas — el error global puede incluso empeorar en el interior de la trayectoria. La moraleja es la de Corke: los pesos de las aristas deben reflejar la incertidumbre **real** de cada sensor (Corke, 2023, p. 232). Un cierre de bucle mal pesado no es una ayuda, es una restricción falsa que el optimizador se cree a rajatabla."""))

C.append(md("""---

## Para llevarse de esta sesión

SLAM no es un algoritmo nuevo: es **meter el mapa dentro del estado**. En el EKF eso significa un vector que crece a 3 + 2N y una covarianza densa cuyos bloques cruzados son precisamente lo que hace que reobservar un hito antiguo corrija el mapa entero. Esa virtud tiene su factura en coste cuadrático (Thrun et al., 2005, p. 331) y en la irreversibilidad de una asociación de datos equivocada.

La alternativa moderna cambia la representación, no la física: en lugar de una gaussiana que se propaga, un grafo de restricciones que se optimiza. Crecer el grafo es barato (Thrun et al., 2005, p. 339), y a cambio hay que resolver un problema de mínimos cuadrados cada vez que se quiere una respuesta. El cierre de bucle deja de ser un evento afortunado y pasa a ser una arista más — una que redistribuye el error por toda la historia, algo que ningún filtro puede hacer.

Con esto se cierra el bloque 6. El mapa conceptual completo cabe en una línea: **cámara → rasgos (clásicos o aprendidos) → medidas z; odometría → u; filtro de Bayes como tronco; EKF y partículas como ramas; SLAM como el caso en que el mapa entra en el estado.** En el bloque 7 nada de esto se vuelve a implementar: se configura. Pero quien haya escrito estas líneas sabrá por qué AMCL pide una pose inicial, por qué `slam_toolbox` produce una rejilla de ocupación y por qué la TF entre sensores calibrados no es un detalle administrativo.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S31_SLAM.ipynb', C)
print('escrito S31')
