from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('matplotlib','matplotlib'), ('scipy','scipy')]
C = []

C.append(cabecera(
    "S28", "Filtro de Bayes, filtro de Kalman y EKF", "6",
    "viernes 13 de noviembre de 2026", "2 h",
    "Implementa el ciclo predicción-corrección de principio a fin: primero el filtro de Bayes discreto sobre un pasillo, después el filtro de Kalman en una dimensión, y por último un EKF para ver qué se rompe cuando el sistema deja de ser lineal.",
    "Thrun, Burgard y Fox (2005), caps. 2 y 3 — algoritmo del filtro de Bayes (p. 27), filtro de Kalman (pp. 40-42), EKF (pp. 54-56).",
    "los apuntes del bloque 6"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=3, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.2)
plt.rcParams['axes.grid'] = True
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('Listo.')"""))

# ---------------- 1. Filtro de Bayes discreto
C.append(md("""## 1. El filtro de Bayes, en un pasillo de 20 celdas

Antes de las gaussianas, el caso discreto: la creencia es un vector de probabilidades sobre las celdas del pasillo. Es la forma más transparente de ver el ciclo, porque se puede dibujar entero.

El robot no sabe dónde está. Hay puertas en tres celdas y su sensor solo dice «veo puerta» o «no veo puerta», con ruido. Recorre el algoritmo del libro (Thrun et al., 2005, p. 27) línea a línea: predicción con el modelo de movimiento, corrección con la verosimilitud, y normalización."""))

C.append(code("""N = 20                       # celdas del pasillo
PUERTAS = [4, 9, 15]         # donde hay puerta

# --- modelo de observacion: P(z | x) ---
P_ACIERTO = 0.8              # ve puerta estando en puerta / no la ve no estando
def verosimilitud(z):
    \"\"\"Vector de P(z | x) para cada celda x.\"\"\"
    hay = np.zeros(N, bool); hay[PUERTAS] = True
    p = np.where(hay, P_ACIERTO, 1 - P_ACIERTO)
    return p if z == 'puerta' else 1 - p

# --- modelo de movimiento: avanza u celdas con ruido ---
def predecir(bel, u, p_exacto=0.8, p_desliza=0.1):
    \"\"\"Convolucion circular: avanza u, u-1 o u+1 celdas.\"\"\"
    nuevo = np.zeros(N)
    for despl, peso in [(u, p_exacto), (u - 1, p_desliza), (u + 1, p_desliza)]:
        nuevo += peso * np.roll(bel, despl)
    return nuevo

def corregir(bel, z):
    bel = bel * verosimilitud(z)
    return bel / bel.sum()          # normalizacion

bel = np.ones(N) / N                # sin idea de donde esta: uniforme
print('Creencia inicial uniforme, maximo =', bel.max().round(3))"""))

C.append(md("""Ahora la secuencia que se comenta en clase: el robot ve una puerta, avanza, vuelve a ver una puerta. Fíjate en cómo la creencia pasa de plana a multimodal (tres candidatas, una por puerta) y de multimodal a casi unimodal cuando el movimiento rompe la simetría."""))

C.append(code("""historia = [('inicio', bel.copy())]

bel = corregir(bel, 'puerta');   historia.append(('ve puerta', bel.copy()))
bel = predecir(bel, 5);          historia.append(('avanza 5', bel.copy()))
bel = corregir(bel, 'puerta');   historia.append(('ve puerta otra vez', bel.copy()))

fig, axes = plt.subplots(len(historia), 1, figsize=(9, 7), sharex=True)
for ax, (titulo, b) in zip(axes, historia):
    ax.bar(range(N), b, color=IQS_AZUL)
    ax.bar(PUERTAS, [b.max()] * len(PUERTAS), color=IQS_VERDE, alpha=0.18, width=0.9)
    ax.set_ylabel(titulo, rotation=0, ha='right', fontsize=9)
    ax.set_ylim(0, max(0.05, b.max() * 1.15))
axes[-1].set_xlabel('celda del pasillo (en verde, las celdas con puerta)')
plt.tight_layout(); plt.show()

print('Celda mas probable:', int(bel.argmax()), ' con probabilidad', round(float(bel.max()), 3))"""))

C.append(md("""**Lo que hay que hacer notar en clase.** La predicción *aplana* la creencia (el movimiento añade incertidumbre) y la corrección la *afila* (la medida quita incertidumbre). Ese vaivén es el latido de todo el bloque, y reaparece idéntico en Kalman, en el filtro de partículas y en el SLAM.

### Ejercicio 1

Sube `P_ACIERTO` a 0.95 y bájalo a 0.55, y vuelve a ejecutar la secuencia. ¿Cuántas observaciones hacen falta para que la creencia se concentre en un solo pico en cada caso? ¿Qué pasa si el sensor es «honesto pero inútil», con `P_ACIERTO = 0.5`?"""))

C.append(code("""# Ejercicio 1: prueba aqui
# P_ACIERTO = 0.95   (recuerda re-ejecutar la celda de definiciones)"""))

# ---------------- 2. Kalman 1D
C.append(md("""## 2. El filtro de Kalman en una dimensión

Ahora el caso gaussiano lineal. Si el sistema es lineal, el ruido gaussiano y la creencia inicial gaussiana, la creencia sigue siendo gaussiana para siempre y basta propagar media y varianza (Thrun et al., 2005, pp. 40-42).

Un carro se mueve en línea recta con velocidad constante ordenada. La odometría acumula error; un sensor de posición mide con ruido. Las dos fases del algoritmo son cuatro líneas."""))

C.append(code("""def kf_paso(mu, sigma2, u, z, A=1.0, B=1.0, C=1.0, R=0.5, Q=2.0):
    \"\"\"Un ciclo del filtro de Kalman escalar.
    R = varianza del ruido de proceso (movimiento);  Q = varianza del ruido de medida.\"\"\"
    # --- prediccion ---
    mu_b     = A * mu + B * u
    sigma2_b = A * sigma2 * A + R
    # --- correccion ---
    K      = sigma2_b * C / (C * sigma2_b * C + Q)      # ganancia de Kalman
    mu     = mu_b + K * (z - C * mu_b)
    sigma2 = (1 - K * C) * sigma2_b
    return mu, sigma2, K

rng = np.random.default_rng(7)
T, u = 40, 1.0
R_real, Q_real = 0.5, 2.0

x = 0.0
xs, zs, mus, sig, Ks = [], [], [], [], []
mu, sigma2 = 0.0, 1.0
for t in range(T):
    x = x + u + rng.normal(0, np.sqrt(R_real))      # mundo real
    z = x + rng.normal(0, np.sqrt(Q_real))          # medida ruidosa
    mu, sigma2, K = kf_paso(mu, sigma2, u, z, R=R_real, Q=Q_real)
    xs.append(x); zs.append(z); mus.append(mu); sig.append(sigma2); Ks.append(K)

xs, zs, mus, sig, Ks = map(np.array, (xs, zs, mus, sig, Ks))
err_medida = np.abs(zs - xs).mean()
err_filtro = np.abs(mus - xs).mean()
print(f'Error medio de la medida cruda : {err_medida:.3f}')
print(f'Error medio del filtro         : {err_filtro:.3f}')
print(f'El filtro reduce el error un {100*(1-err_filtro/err_medida):.0f} %')"""))

C.append(code("""fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.4))
t = np.arange(T)
a1.plot(t, xs, color='black', lw=2, label='posición real')
a1.scatter(t, zs, s=14, color='crimson', alpha=0.6, label='medida')
a1.plot(t, mus, color=IQS_AZUL, lw=2, label='estimación KF')
a1.fill_between(t, mus - 2*np.sqrt(sig), mus + 2*np.sqrt(sig), color=IQS_AZUL, alpha=0.15,
                label='±2σ')
a1.legend(fontsize=8); a1.set_xlabel('paso'); a1.set_title('Seguimiento')

a2.plot(t, Ks, color=IQS_VERDE, lw=2)
a2.set_xlabel('paso'); a2.set_title('Ganancia de Kalman K')
a2.set_ylim(0, 1)
plt.tight_layout(); plt.show()"""))

C.append(md("""**La ganancia es la protagonista.** Arranca alta —el filtro no sabe nada y hace caso a la medida— y se estabiliza en el valor que equilibra su confianza en la predicción con su confianza en el sensor. Es exactamente la lectura que pide el guion de la sesión: *mucha confianza en el sensor la acerca a la medida; poca, a la predicción*.

### Ejercicio 2

Ejecuta la simulación con un sensor diez veces peor (`Q = 20`) y con uno diez veces mejor (`Q = 0.2`), dejando `R` fijo. Anota a qué valor converge `K` en cada caso y explica el resultado sin mirar la fórmula."""))

C.append(code("""# Ejercicio 2
for Q_prueba in [0.2, 2.0, 20.0]:
    mu, sigma2 = 0.0, 1.0
    for t in range(60):
        mu, sigma2, K = kf_paso(mu, sigma2, 1.0, 0.0, R=0.5, Q=Q_prueba)
    print(f'Q = {Q_prueba:5.1f}  ->  K converge a {K:.3f}')"""))

# ---------------- 3. EKF
C.append(md("""## 3. Cuando el sistema no es lineal: el EKF

Casi ningún robot es lineal —un vehículo que gira no lo es—, así que el EKF linealiza en torno a la estimación actual mediante jacobianas y aplica las mismas ecuaciones (Thrun et al., 2005, pp. 54-56).

El ejemplo mínimo que deja ver el problema: el estado es una posición en el plano y el sensor mide **solo la distancia** a una baliza. La medida es no lineal en el estado."""))

C.append(code("""BALIZA = np.array([10.0, 0.0])

def h(x):                       # modelo de observacion: distancia a la baliza
    return np.linalg.norm(x - BALIZA)

def H(x):                       # su jacobiana (1x2)
    d = x - BALIZA
    return (d / np.linalg.norm(d)).reshape(1, 2)

def ekf_paso(mu, P, u, z, R, Q):
    mu_b = mu + u                       # movimiento lineal: F = I
    P_b  = P + R
    Hx   = H(mu_b)
    S    = Hx @ P_b @ Hx.T + Q
    K    = P_b @ Hx.T @ np.linalg.inv(S)
    mu   = mu_b + (K * (z - h(mu_b))).ravel()
    P    = (np.eye(2) - K @ Hx) @ P_b
    return mu, P

rng = np.random.default_rng(3)
R = np.diag([0.02, 0.02]); Q = np.array([[0.25]])
x = np.array([0.0, 3.0]); mu = np.array([0.0, 3.0]); P = np.eye(2) * 0.5
u = np.array([0.4, 0.0])

reales, ests, trazas = [], [], []
for t in range(30):
    x = x + u + rng.multivariate_normal([0, 0], R)
    z = h(x) + rng.normal(0, np.sqrt(Q[0, 0]))
    mu, P = ekf_paso(mu, P, u, z, R, Q)
    reales.append(x.copy()); ests.append(mu.copy()); trazas.append(np.trace(P))

reales, ests = np.array(reales), np.array(ests)
print('Error final:', round(float(np.linalg.norm(reales[-1] - ests[-1])), 3), 'm')"""))

C.append(code("""fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.6))
a1.plot(reales[:, 0], reales[:, 1], color='black', lw=2, label='real')
a1.plot(ests[:, 0], ests[:, 1], color=IQS_AZUL, lw=2, ls='--', label='EKF')
a1.scatter(*BALIZA, marker='*', s=180, color=IQS_VERDE, label='baliza', zorder=5)
a1.legend(fontsize=8); a1.set_aspect('equal'); a1.set_title('Trayectoria')

a2.plot(trazas, color=IQS_VERDE, lw=2)
a2.set_title('traza de P (incertidumbre total)'); a2.set_xlabel('paso')
plt.tight_layout(); plt.show()"""))

C.append(md("""**Lo que se ve y hay que comentar.** La incertidumbre no baja igual en todas las direcciones: una sola distancia a una baliza fija bien el radio pero mal el ángulo, así que la elipse de covarianza se estira. Con una segunda baliza en otra posición el problema desaparece — y eso es exactamente el argumento de por qué la localización necesita varios puntos de referencia, que retomaremos en S29.

### Ejercicio 3

Añade una segunda baliza en `[0, 10]` y modifica `h` y `H` para que devuelvan dos distancias en lugar de una. Compara la traza de `P` con la del caso de una sola baliza."""))

C.append(md("""---

## Soluciones

**Ejercicio 1.** Con `P_ACIERTO = 0.95` una sola observación deja tres picos muy marcados y la segunda ya resuelve; con `0.55` hacen falta muchas más observaciones y la creencia queda plana. Con `0.5` la verosimilitud es constante: la corrección multiplica por el mismo número en todas las celdas y, tras normalizar, **la creencia no cambia**. Un sensor que no discrimina no aporta información, por bien calibrado que esté.

**Ejercicio 2.** `K` converge a valores mayores cuanto menor es `Q`: con un sensor bueno el filtro se fía de la medida (`K → 1`), con uno malo se fía de su predicción (`K → 0`). La ganancia es literalmente la fracción de la innovación que el filtro se cree.

**Ejercicio 3.** Con dos balizas no alineadas con el robot, la traza de `P` cae mucho más deprisa y la elipse deja de ser alargada: el problema pasa de estar mal condicionado en una dirección a estar bien condicionado en las dos. Es el mismo fenómeno que la dilución de precisión en GPS."""))

C.append(md("""---

## Para llevarse de esta sesión

Todo estimador de este bloque es el mismo ciclo: **predecir** con el modelo de movimiento, que aumenta la incertidumbre, y **corregir** con la medida, que la reduce. Kalman lo hace con dos números, el filtro de partículas de S30 con miles de muestras, y el SLAM de S31 con un grafo — pero el ciclo no cambia.

La linealización del EKF es una aproximación que funciona mientras la no linealidad sea suave y la incertidumbre pequeña. Cuando deja de serlo, el filtro diverge sin avisar: no hay ninguna señal interna que diga «me he perdido». Esa es la motivación de la sesión siguiente.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S28_Bayes_Kalman_EKF.ipynb', C)
print('escrito S28')
