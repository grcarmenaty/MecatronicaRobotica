from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('matplotlib','matplotlib'), ('scipy','scipy')]
C = []

C.append(cabecera(
    "S29", "Localización con EKF sobre un mapa de balizas", "6",
    "miércoles 18 de noviembre de 2026", "1 h",
    "Pone la maquinaria de S28 a trabajar sobre un robot diferencial real: modelo de movimiento por odometría, observación de rango y rumbo a balizas de posición conocida, y el ciclo EKF completo con las elipses de covarianza dibujadas a lo largo de la trayectoria. Primero se ve la deriva sin límite del dead reckoning y después cómo cada avistamiento colapsa la elipse.",
    "Thrun, Burgard y Fox (2005), caps. 5 y 7 — modelo por velocidades (p. 121), modelo por odometría (p. 132), coeficientes de ruido α (pp. 123-124), taxonomía de la localización (p. 194), localización de Markov (p. 197), la localización EKF como caso especial (p. 201), algoritmo EKF_localization (p. 204), correspondencias por máxima verosimilitud (p. 217), sentencia de Cox (p. 219). Corke (2023), cap. 6 — elipses de dead reckoning (p. 216), los fenicios y los hitos conocidos (p. 218), modelo de rango y rumbo (p. 220), riesgo de la asociación errónea (p. 223).",
    "los apuntes del bloque 6"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
np.set_printoptions(precision=3, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.2)
plt.rcParams['axes.grid'] = True
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('Listo.')"""))

# ---------------- 1. Los dos modelos
C.append(md("""## 1. Los dos modelos: movimiento por odometría y observación de baliza

Localizar un robot móvil es estimar su pose respecto a un mapa dado, y su importancia difícilmente se exagera: Thrun recoge la sentencia de Cox de que la localización «ha sido señalada como el problema más fundamental para dotar a un robot móvil de capacidades autónomas» (Thrun et al., 2005, p. 219). Hoy resolvemos el caso fácil de la taxonomía —seguimiento de posición, con pose inicial conocida (Thrun et al., 2005, pp. 193-194)— porque es el que un EKF puede resolver.

**Movimiento.** Usamos el modelo por odometría, que descompone el desplazamiento entre dos instantes en rotación-traslación-rotación, u = (δrot1, δtrans, δrot2). Frente al modelo por velocidades (Thrun et al., 2005, p. 121), «la experiencia práctica sugiere que la odometría, aunque sigue siendo errónea, suele ser más exacta que la velocidad»; a cambio, solo está disponible *a posteriori*, lo que la hace inservible para planificar y perfecta para filtrar (Thrun et al., 2005, p. 132).

**Observación.** Si el mapa dice que la baliza está en (mx, my), desde la pose (x, y, θ) esperamos medir r = √((mx−x)² + (my−y)²) y φ = atan2(my−y, mx−x) − θ — la h(x) que aparece dentro del algoritmo de localización EKF (Thrun et al., 2005, p. 204) y que Corke formula de forma idéntica (Corke, 2023, p. 220)."""))

C.append(code("""def envolver(a):
    \"\"\"Lleva un angulo al intervalo (-pi, pi]. Sin esto, la innovacion angular explota.\"\"\"
    return (a + np.pi) % (2*np.pi) - np.pi

def g(x, u):
    \"\"\"Modelo de movimiento por odometria: rotar, avanzar, rotar.\"\"\"
    r1, tr, r2 = u
    th = x[2]
    return np.array([x[0] + tr*np.cos(th + r1),
                     x[1] + tr*np.sin(th + r1),
                     envolver(th + r1 + r2)])

def G_jac(x, u):
    \"\"\"Jacobiano de g respecto al estado (3x3).\"\"\"
    r1, tr, _ = u
    th = x[2]
    return np.array([[1.0, 0.0, -tr*np.sin(th + r1)],
                     [0.0, 1.0,  tr*np.cos(th + r1)],
                     [0.0, 0.0,  1.0]])

def V_jac(x, u):
    \"\"\"Jacobiano de g respecto al control (3x3): traslada el ruido de odometria al estado.\"\"\"
    r1, tr, _ = u
    th = x[2]
    return np.array([[-tr*np.sin(th + r1), np.cos(th + r1), 0.0],
                     [ tr*np.cos(th + r1), np.sin(th + r1), 0.0],
                     [ 1.0,                0.0,             1.0]])

# Coeficientes alfa del ruido de odometria (Thrun et al., 2005, pp. 123-124)
ALFA = np.array([0.02, 0.02, 0.05, 0.02])

def M_ruido(u):
    r1, tr, r2 = u
    return np.diag([ALFA[0]*r1**2 + ALFA[1]*tr**2,
                    ALFA[2]*tr**2 + ALFA[3]*(r1**2 + r2**2),
                    ALFA[0]*r2**2 + ALFA[1]*tr**2])

# Comprobacion del jacobiano por diferencias finitas: si esto no cuadra, el filtro divergira
x0, u0 = np.array([1.0, 2.0, 0.4]), np.array([0.15, 0.5, -0.05])
num = np.zeros((3, 3))
for k in range(3):
    d = np.zeros(3); d[k] = 1e-6
    num[:, k] = (g(x0 + d, u0) - g(x0 - d, u0)) / 2e-6
print('Error del jacobiano G frente a diferencias finitas:',
      np.abs(num - G_jac(x0, u0)).max().round(9))"""))

C.append(code("""def h_baliza(x, m):
    \"\"\"Prediccion de medida: rango y rumbo a la baliza m desde la pose x.\"\"\"
    dx, dy = m[0] - x[0], m[1] - x[1]
    r = np.hypot(dx, dy)
    return np.array([r, envolver(np.arctan2(dy, dx) - x[2])])

def H_jac(x, m):
    \"\"\"Jacobiano de h respecto al estado (2x3).\"\"\"
    dx, dy = m[0] - x[0], m[1] - x[1]
    q = dx*dx + dy*dy
    r = np.sqrt(q)
    return np.array([[-dx/r, -dy/r,  0.0],
                     [ dy/q, -dx/q, -1.0]])

# Q: ruido del sensor. 5 cm en rango, 1 grado en rumbo
Q = np.diag([0.05**2, np.deg2rad(1.0)**2])
ALCANCE = 8.0                      # la baliza solo se ve si esta a menos de 8 m

m_prueba = np.array([5.0, 5.0])
print('Desde la pose', x0, 'a la baliza', m_prueba, ':')
print('  medida esperada  r =', h_baliza(x0, m_prueba)[0].round(3),
      'm,  phi =', np.rad2deg(h_baliza(x0, m_prueba)[1]).round(2), 'grados')
print('  jacobiano H =\\n', H_jac(x0, m_prueba))"""))

C.append(md("""Merece la pena leer las dos filas de H, porque tienen geometría (Thrun et al., 2005, p. 204). **La fila del rango** es el vector unitario que va del robot a la baliza cambiado de signo: medir distancia corrige a lo largo de la línea de vista, y su tercera columna es 0, así que el rango no dice absolutamente nada sobre θ. **La fila del rumbo** es perpendicular a la anterior, su parte de posición decae como 1/r, y lleva un −1 en la columna de θ.

De ahí sale la respuesta a la pregunta trampa del guion, que analizaremos con números en la sección 4: una baliza lejana **orienta igual de bien** (el −1 no depende de la distancia) pero **sitúa mucho peor** en la dirección transversal, porque ahí el rumbo es la única fuente de corrección y su valor en metros se degrada con r."""))

# ---------------- 2. Dead reckoning
C.append(md("""## 2. Dead reckoning: la incertidumbre que crece sin límite

Antes de encender el sensor, la referencia contra la que compararemos todo: integrar la odometría sin corregir. Es la mitad de predicción del ciclo, ejecutada sola.

El robot recorre un circuito cerrado. Simulamos el movimiento **verdadero** aplicando a cada control una realización del ruido que describe el modelo α, y el filtro predice con el control nominal. Dibujamos la elipse de covarianza al 95 % cada pocos pasos, como en la figura de Corke (2023, p. 216)."""))

C.append(code("""rng = np.random.default_rng(29)

# --- circuito: dos rectas y dos curvas, 120 pasos ---
def controles():
    u = []
    for _ in range(28): u.append((0.0, 0.42, 0.0))          # recta
    for _ in range(16): u.append((np.pi/32, 0.30, np.pi/32))  # curva a la izquierda
    for _ in range(24): u.append((0.0, 0.42, 0.0))
    for _ in range(16): u.append((np.pi/32, 0.30, np.pi/32))
    for _ in range(28): u.append((0.0, 0.42, 0.0))
    return [np.array(c) for c in u]

U = controles()
POSE0 = np.array([0.0, 0.0, 0.0])

def muestrear_control(u):
    \"\"\"Control realmente ejecutado por el robot: el nominal mas el ruido del modelo alfa.\"\"\"
    s = np.sqrt(np.diag(M_ruido(u)))
    return u + rng.normal(0, np.maximum(s, 1e-9))

# Trayectoria verdadera (la misma para las dos simulaciones: fijamos la semilla)
rng = np.random.default_rng(29)
VERDAD, U_REAL = [POSE0.copy()], []
for u in U:
    ur = muestrear_control(u)
    U_REAL.append(ur)
    VERDAD.append(g(VERDAD[-1], ur))
VERDAD = np.array(VERDAD)

def elipse(ax, mu, P, color, n_sigma=2.4477, **kw):
    \"\"\"Elipse de covarianza al 95 % en el plano (x, y): sqrt(chi2_2gl(0.95)) = 2.4477.\"\"\"
    vals, vecs = np.linalg.eigh(P[:2, :2])
    ang = np.degrees(np.arctan2(vecs[1, -1], vecs[0, -1]))
    e = Ellipse(mu[:2], *(2*n_sigma*np.sqrt(np.maximum(vals, 0))), angle=ang,
                facecolor='none', edgecolor=color, lw=1.3, **kw)
    ax.add_patch(e)

# --- dead reckoning: solo prediccion ---
mu, P = POSE0.copy(), np.diag([0.01, 0.01, 0.001])
DR, P_DR = [mu.copy()], [P.copy()]
for u in U:
    P = G_jac(mu, u) @ P @ G_jac(mu, u).T + V_jac(mu, u) @ M_ruido(u) @ V_jac(mu, u).T
    mu = g(mu, u)
    DR.append(mu.copy()); P_DR.append(P.copy())
DR = np.array(DR)

print('Error final del dead reckoning:', round(float(np.linalg.norm(DR[-1,:2]-VERDAD[-1,:2])), 3), 'm')
print('Desviación típica final en x:', round(float(np.sqrt(P_DR[-1][0,0])), 3),
      'm   en y:', round(float(np.sqrt(P_DR[-1][1,1])), 3), 'm')"""))

# ---------------- 3. El ciclo EKF
C.append(md("""## 3. El ciclo EKF completo con balizas

Ahora el algoritmo `EKF_localization` con correspondencias conocidas, línea a línea (Thrun et al., 2005, p. 204): predicción de la media con g y de la covarianza con G y el ruido de odometría; y, para cada baliza observada, predicción de la medida h(μ̄), innovación con la aritmética angular tratada con cuidado, ganancia de Kalman y corrección.

Nótese que las correcciones se aplican **una baliza cada vez**, reutilizando la media ya corregida. Es lo que hace el algoritmo del libro y evita construir matrices grandes."""))

C.append(code("""BALIZAS = np.array([[2.0, 6.0], [10.0, 1.0], [14.0, 7.0],
                    [6.0, 12.0], [-2.0, 9.0], [16.0, 13.0]])

def observar(x_verdadero):
    \"\"\"Devuelve [(indice_baliza, z)] de las balizas dentro del alcance, con ruido.\"\"\"
    obs = []
    for j, m in enumerate(BALIZAS):
        z = h_baliza(x_verdadero, m)
        if z[0] <= ALCANCE:
            z = z + rng.normal(0, np.sqrt(np.diag(Q)))
            obs.append((j, np.array([z[0], envolver(z[1])])))
    return obs

rng = np.random.default_rng(129)
mu, P = POSE0.copy(), np.diag([0.01, 0.01, 0.001])
EKF, P_EKF, n_obs = [mu.copy()], [P.copy()], []

for k, u in enumerate(U):
    # ---- prediccion ----
    Gk, Vk = G_jac(mu, u), V_jac(mu, u)
    P  = Gk @ P @ Gk.T + Vk @ M_ruido(u) @ Vk.T
    mu = g(mu, u)
    # ---- correccion, una baliza cada vez ----
    obs = observar(VERDAD[k+1])
    for j, z in obs:
        Hk = H_jac(mu, BALIZAS[j])
        S  = Hk @ P @ Hk.T + Q
        K  = P @ Hk.T @ np.linalg.inv(S)
        y  = z - h_baliza(mu, BALIZAS[j])
        y[1] = envolver(y[1])                      # la innovacion angular, envuelta
        mu = mu + K @ y
        mu[2] = envolver(mu[2])
        P  = (np.eye(3) - K @ Hk) @ P
    n_obs.append(len(obs))
    EKF.append(mu.copy()); P_EKF.append(P.copy())

EKF = np.array(EKF)
err_dr  = np.linalg.norm(DR[:, :2]  - VERDAD[:, :2], axis=1)
err_ekf = np.linalg.norm(EKF[:, :2] - VERDAD[:, :2], axis=1)
print(f'Balizas vistas por paso: media {np.mean(n_obs):.2f}, '
      f'pasos sin ninguna: {sum(1 for n in n_obs if n == 0)}')
print(f'Error medio  dead reckoning = {err_dr.mean():.3f} m   EKF = {err_ekf.mean():.3f} m')
print(f'Error final  dead reckoning = {err_dr[-1]:.3f} m   EKF = {err_ekf[-1]:.3f} m')"""))

C.append(code("""fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.5, 5.0),
                             gridspec_kw={'width_ratios': [1.35, 1]})

a1.plot(VERDAD[:,0], VERDAD[:,1], color='black', lw=2.2, label='trayectoria verdadera')
a1.plot(DR[:,0], DR[:,1], color='crimson', lw=1.6, ls='--', label='dead reckoning')
a1.plot(EKF[:,0], EKF[:,1], color=IQS_AZUL, lw=1.8, label='EKF con balizas')
for k in range(0, len(DR), 8):
    elipse(a1, DR[k],  P_DR[k],  'crimson', alpha=0.55)
    elipse(a1, EKF[k], P_EKF[k], IQS_AZUL)
a1.scatter(BALIZAS[:,0], BALIZAS[:,1], marker='*', s=230, color=IQS_VERDE,
           edgecolors='black', lw=0.6, zorder=6, label='balizas del mapa')
a1.set_aspect('equal'); a1.legend(fontsize=8, loc='upper left')
a1.set_xlabel('x [m]'); a1.set_ylabel('y [m]')
a1.set_title('Elipses de covarianza al 95 % a lo largo del recorrido', fontsize=10)

pasos = np.arange(len(err_dr))
a2.plot(pasos, err_dr, color='crimson', lw=1.6, label='error dead reckoning')
a2.plot(pasos, err_ekf, color=IQS_AZUL, lw=1.8, label='error EKF')
a2.plot(pasos, [2.4477*np.sqrt(np.trace(p[:2,:2])/2) for p in P_EKF],
        color=IQS_VERDE, lw=1.4, ls=':', label='radio 95 % del EKF')
a2.set_xlabel('paso'); a2.set_ylabel('error de posición [m]')
a2.legend(fontsize=8); a2.set_title('El sensor acota el error; la odometría sola no', fontsize=10)
plt.tight_layout(); plt.show()"""))

C.append(md("""**Lo que hay que hacer notar en clase.** La elipse roja del dead reckoning crece sin freno y, además, crece de forma **anisótropa**: se alarga en la dirección perpendicular al avance porque un pequeño error de rumbo se amplifica con la distancia recorrida. La azul del EKF respira —crece entre observaciones y se contrae en cuanto entra una baliza— pero se mantiene acotada.

La frase de Corke resume tres milenios de navegación: «hemos visto cómo la incertidumbre en la posición crece sin límite usando solo dead reckoning; la solución, como descubrieron los fenicios hace 4000 años, es usar información adicional procedente de observaciones de características o hitos conocidos del mundo» (Corke, 2023, p. 218).

Fíjate también en la curva verde de la derecha: el radio al 95 % que anuncia el filtro envuelve casi siempre al error real. Cuando no lo hace, el filtro es **optimista**, y un filtro optimista es peligroso porque el planificador se lo cree.

### Ejercicio 1

Sube el ruido de rumbo del sensor a 10° (`Q = np.diag([0.05**2, np.deg2rad(10)**2])`) y vuelve a ejecutar. ¿Qué componente de la elipse deja de contraerse? Prueba después a empeorar solo el rango (30 cm) y compara."""))

C.append(code("""# Ejercicio 1: prueba aqui
# Q = np.diag([0.05**2, np.deg2rad(10.0)**2])   (y re-ejecuta la celda del ciclo EKF)"""))

# ---------------- 4. Geometria y limites
C.append(md("""## 4. Geometría de la corrección y límites del EKF

Dos experimentos numéricos cortos que cierran la sesión, y que son exactamente las dos preguntas del guion.

**Primero, la pregunta trampa: qué se pierde con la distancia.** La cantidad que hay que mirar es la matriz de información de la observación, Hᵀ·Q⁻¹·H: cuánto aprende el filtro de un solo avistamiento. La calculamos para una baliza situada a distintas distancias delante del robot."""))

C.append(code("""x_r = np.array([0.0, 0.0, 0.0])
sr, sphi = np.sqrt(Q[0, 0]), np.sqrt(Q[1, 1])
print(f'{"dist. [m]":>10} {"info en x,y":>13} {"info en theta":>14} {"sigma lateral":>15}')
for d in [1.0, 2.0, 5.0, 10.0, 20.0]:
    Hk = H_jac(x_r, np.array([d, 0.0]))
    Info = Hk.T @ np.linalg.inv(Q) @ Hk
    print(f'{d:10.1f} {np.trace(Info[:2,:2]):13.1f} {Info[2,2]:14.1f} {d*sphi:12.3f} m')

print(f'\\nInformación sobre theta: constante = 1/sigma_phi^2 = {1/sphi**2:.0f}.')
print('El rumbo se mide con la misma precisión angular esté la baliza donde esté.')
print(f'Información sobre la posición: cae y satura en la que aporta el rango, 1/sigma_r^2 = {1/sr**2:.0f}.')
print(f'Motivo: la componente transversal solo la fija el rumbo, y {np.rad2deg(sphi):.0f} grado a 20 m'
      f' son {20*sphi:.2f} m de error lateral, frente a los {sr:.2f} m del rango.')"""))

C.append(md("""**Segundo, la asociación de datos.** Hasta ahora hemos supuesto que cada observación viene etiquetada con la baliza que la produjo. En la realidad casi nunca es así: el EKF estándar elige el hito más verosímil dado el estado (Thrun et al., 2005, p. 217), y Corke advierte del riesgo desde la práctica — una asociación equivocada inyecta una corrección coherentemente errónea y el filtro no tiene forma de detectarla (Corke, 2023, p. 223).

La conclusión de la tabla anterior conviene enunciarla antes de seguir: **una baliza lejana orienta bien y sitúa mal**; una cercana hace las dos cosas bien. Por eso, cuando se instrumenta una nave, las balizas no se ponen todas en la pared del fondo.

Vamos a provocar ahora el fallo de asociación: repetimos el filtro estropeando las correspondencias, primero en un solo paso y después durante doce pasos seguidos."""))

C.append(code("""def correr_ekf(sabotaje=()):
    rng_l = np.random.default_rng(129)
    mu, P = POSE0.copy(), np.diag([0.01, 0.01, 0.001])
    traza = [mu.copy()]
    for k, u in enumerate(U):
        Gk, Vk = G_jac(mu, u), V_jac(mu, u)
        P  = Gk @ P @ Gk.T + Vk @ M_ruido(u) @ Vk.T
        mu = g(mu, u)
        for j, m in enumerate(BALIZAS):
            z = h_baliza(VERDAD[k+1], m)
            if z[0] > ALCANCE:
                continue
            z = np.array([z[0], envolver(z[1])]) + rng_l.normal(0, np.sqrt(np.diag(Q)))
            j_usada = (j + 1) % len(BALIZAS) if k in sabotaje else j     # asociacion equivocada
            Hk = H_jac(mu, BALIZAS[j_usada])
            S  = Hk @ P @ Hk.T + Q
            K  = P @ Hk.T @ np.linalg.inv(S)
            y  = z - h_baliza(mu, BALIZAS[j_usada]); y[1] = envolver(y[1])
            mu = mu + K @ y; mu[2] = envolver(mu[2])
            P  = (np.eye(3) - K @ Hk) @ P
        traza.append(mu.copy())
    return np.array(traza)

casos = [('asociación correcta', (), IQS_AZUL, '-'),
         ('una sola errónea (k=40)', (40,), 'darkorange', '--'),
         ('doce erróneas (k=40..51)', tuple(range(40, 52)), 'crimson', '-.')]

fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.5, 4.4),
                             gridspec_kw={'width_ratios': [1.25, 1]})
a1.plot(VERDAD[:,0], VERDAD[:,1], color='black', lw=2.4, label='verdad')
for nombre, sab, color, ls in casos:
    tr = correr_ekf(sab)
    err = np.linalg.norm(tr[:, :2] - VERDAD[:, :2], axis=1)
    a1.plot(tr[:,0], tr[:,1], color=color, lw=1.7, ls=ls, label=nombre)
    a2.plot(err, color=color, lw=1.7, ls=ls, label=nombre)
    print(f'{nombre:26s} error máximo = {err.max():6.2f} m   error final = {err[-1]:.3f} m')

a1.scatter(BALIZAS[:,0], BALIZAS[:,1], marker='*', s=200, color=IQS_VERDE, edgecolors='k', lw=0.6)
a1.set_aspect('equal'); a1.legend(fontsize=8); a1.set_xlabel('x [m]'); a1.set_ylabel('y [m]')
a1.set_title('Efecto de una asociación de datos equivocada', fontsize=10)
a2.set_xlabel('paso'); a2.set_ylabel('error de posición [m]'); a2.legend(fontsize=8)
a2.set_title('El filtro no avisa: solo se desvía', fontsize=10)
plt.tight_layout(); plt.show()"""))

C.append(md("""**El matiz que hay que comentar.** Una sola asociación equivocada lanza la estimación casi cuatro metros fuera; doce seguidas, casi ocho, y el robot pasa un tercio del recorrido creyéndose en un sitio en el que no está. Que en este escenario acabe recuperándose no debe leerse como buena noticia: se recupera porque el mapa es generoso y siguen entrando observaciones correctas desde varias direcciones. Con menos balizas, o si el error hubiese llegado a encoger la covarianza en el sitio equivocado, no habría vuelta atrás — y ocho metros de desvío en una nave son una estantería.

Lo importante es que en ninguno de los dos casos hay una alarma interna. Por eso las implementaciones serias vigilan la **distancia de Mahalanobis de la innovación**, yᵀ·S⁻¹·y, y rechazan las observaciones que superan un umbral: es el equivalente probabilístico de decir «esto que veo no encaja con lo que creo, y prefiero ignorarlo».

### Ejercicio 2

Elimina las tres primeras balizas del mapa (`BALIZAS[3:]`) y vuelve a correr el filtro. ¿Cuántos pasos se queda el robot sin ver ninguna? Comprueba en la gráfica del error que en esos tramos el EKF se comporta exactamente como el dead reckoning.

### Ejercicio 3

Coloca todas las balizas alineadas sobre la recta y = 15 y vuelve a ejecutar. Mira la forma de las elipses. ¿En qué dirección deja de corregir el filtro y por qué? (Pista: mira la fila del rango en H y pregúntate qué direcciones generan esas filas cuando todas las balizas están en la misma dirección.)"""))

C.append(code("""# Ejercicios 2 y 3: prueba aqui
# BALIZAS = BALIZAS[3:]
# BALIZAS = np.array([[0., 15.], [6., 15.], [12., 15.], [18., 15.]])"""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.** Con 10° de ruido en rumbo, la elipse deja de contraerse en la dirección **transversal** a la línea robot-baliza y la orientación queda mal estimada; el error de posición sube porque un rumbo malo se convierte en deriva lateral en cuanto el robot avanza. Empeorando solo el rango (30 cm) ocurre lo simétrico: la elipse se alarga **a lo largo** de la línea de vista. Es la lectura geométrica de las dos filas de H: cada fila corrige en su propia dirección y solo en la suya.

**Ejercicio 2.** Con el mapa reducido hay tramos largos sin ninguna baliza a la vista, y en ellos las dos curvas de error se superponen: sin medida no hay corrección, y el EKF *es* dead reckoning. Lo importante es que la elipse anunciada también crece en esos tramos, así que el filtro es honesto sobre lo que ignora — que es más de lo que se puede decir de una odometría sin modelo de ruido.

**Ejercicio 3.** Con todas las balizas alineadas y lejanas, las filas del rango de H apuntan casi todas en la misma dirección, así que las correcciones de rango solo informan sobre esa dirección; la perpendicular queda gobernada únicamente por las filas de rumbo, mucho más débiles a distancia (información ∝ 1/r²). El resultado son elipses muy alargadas paralelas a la línea de balizas. Es exactamente el mismo fenómeno que la dilución de precisión geométrica en GPS: no importa cuántas referencias haya, sino cómo estén repartidas angularmente."""))

C.append(md("""---

## Para llevarse de esta sesión

El EKF de localización no es un algoritmo nuevo: es el de S28 con g y h concretas. Todo el trabajo de ingeniería está en los **modelos** —qué ruido tiene la odometría, qué ruido tiene el sensor y qué se ve desde dónde— y no en las ecuaciones del filtro, que se copian del libro (Thrun et al., 2005, p. 204).

Sin observaciones, la incertidumbre crece sin límite; con observaciones de hitos conocidos, se acota. Esa es la diferencia entre navegar y estar perdido, y lleva cuatro mil años siendo la misma (Corke, 2023, p. 218).

Los dos límites que quedan abiertos son el puente a S30. Primero, la asociación de datos: una sola correspondencia equivocada envenena la gaussiana de forma irreversible. Segundo, y más grave, la **unimodalidad**: una gaussiana no puede decir «podría estar aquí o allá», así que este filtro no resuelve la localización global ni se recupera de un secuestro (Thrun et al., 2005, p. 194). Para ambos males, la medicina es la misma: representar la creencia con muestras.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S29_Localizacion_EKF.ipynb', C)
print('escrito S29')
