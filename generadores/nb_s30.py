from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('matplotlib','matplotlib'), ('scipy','scipy')]
C = []

C.append(cabecera(
    "S30", "Filtro de partículas y localización de Montecarlo", "6",
    "jueves 19 de noviembre de 2026", "1 h",
    "Implementa el filtro de partículas completo —muestrear, pesar, remuestrear— y lo pone a resolver la localización GLOBAL en un pasillo con puertas repetidas, el problema exacto en el que el EKF de S29 fracasa. Se ve la nube pasar de uniforme a multimodal y de multimodal a unimodal, y se cierra con el secuestro del robot y la inyección de partículas.",
    "Thrun, Burgard y Fox (2005), caps. 4 y 8 — la creencia como conjunto de muestras (p. 97), algoritmo del filtro de partículas (p. 98), factor de importancia (p. 99), el remuestreo como «supervivencia del más apto» (p. 100), por qué el EKF no resuelve la localización global (p. 194), MCL como «el algoritmo de localización más popular» (p. 238), algoritmo MCL (p. 252), secuencia del pasillo con puertas (pp. 250-252), inyección de partículas aleatorias (pp. 256-257). Corke (2023), p. 236 — el estimador de Montecarlo no supone nada sobre la distribución de los errores.",
    "los apuntes del bloque 6"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=3, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.2)
plt.rcParams['axes.grid'] = True
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('Listo.')"""))

# ---------------- 1. La nube
C.append(md("""## 1. La creencia como nube de muestras

El filtro de partículas es la aproximación **no paramétrica** del filtro de Bayes: la creencia bel(x) se representa por un conjunto de M muestras del espacio de estados, cada una una hipótesis concreta (Thrun et al., 2005, p. 97). Corke lo formula con sencillez: el estimador de Montecarlo «no hace suposiciones sobre la distribución de los errores», «puede manejar múltiples hipótesis sobre el estado del sistema», y «la idea básica es desarmantemente simple» (Corke, 2023, p. 236).

El algoritmo son tres operaciones (Tabla 4.3; Thrun et al., 2005, p. 98):

1. **Predecir** — mover cada partícula con una realización distinta del ruido del modelo de movimiento, x⁽ᵐ⁾ ~ p(x | u, x⁽ᵐ⁾).
2. **Pesar** — dar a cada partícula el factor de importancia w⁽ᵐ⁾ = p(z | x⁽ᵐ⁾), la verosimilitud de la medida real desde esa hipótesis (Thrun et al., 2005, p. 99).
3. **Remuestrear** — extraer con reemplazo M partículas con probabilidad proporcional a su peso.

El escenario: un pasillo de 30 m con puertas en posiciones conocidas. El robot mide **la distancia a la puerta más cercana** y avanza con odometría ruidosa. No sabe dónde empieza."""))

C.append(code("""LARGO = 30.0
PUERTAS = np.array([5.0, 15.0, 21.0, 25.0])    # tres a distancia 10 y una intrusa: la clave del problema
SIGMA_Z, SIGMA_U = 0.35, 0.10                  # ruido del sensor y de la odometria
PASO = 1.0
M = 3000

def h(x):
    \"\"\"Modelo de observacion: distancia a la puerta mas cercana. Vectorizado sobre partículas.\"\"\"
    x = np.atleast_1d(x)
    return np.min(np.abs(x[:, None] - PUERTAS[None, :]), axis=1)

def predecir(P, u, rng):
    \"\"\"Paso 1: cada partícula avanza con SU PROPIA realizacion del ruido.\"\"\"
    return np.clip(P + u + rng.normal(0, SIGMA_U, P.size), 0.0, LARGO)

def pesar(P, z):
    \"\"\"Paso 2: factor de importancia = verosimilitud gaussiana de la medida.\"\"\"
    w = np.exp(-0.5 * ((z - h(P)) / SIGMA_Z)**2) + 1e-300
    return w / w.sum()

def remuestrear(P, w, rng):
    \"\"\"Paso 3: remuestreo sistematico. Un solo numero aleatorio, O(M), baja varianza.\"\"\"
    posiciones = (rng.random() + np.arange(P.size)) / P.size
    return P[np.searchsorted(np.cumsum(w), posiciones)]

def n_efectivo(w):
    \"\"\"Numero efectivo de partículas: 1 / suma(w^2). Mide cuantas cuentan de verdad.\"\"\"
    return 1.0 / np.sum(w**2)

print('Pasillo de', LARGO, 'm con puertas en', PUERTAS)
print('Distancia a la puerta más cercana desde x = 2, 8 y 12 m:', h(np.array([2.0, 8.0, 12.0])))
print('Las tres darían la MISMA lectura: ahí está la ambigüedad que un EKF no puede representar.')"""))

C.append(md("""Esa última línea es todo el problema. Con las puertas repetidas cada 10 m, una sola medida es compatible con varias posiciones muy separadas: la creencia verdadera es **multimodal**, y ninguna gaussiana puede representarla (Thrun et al., 2005, p. 194)."""))

# ---------------- 2. Localizacion global
C.append(md("""## 2. Localización global: de uniforme a multimodal a unimodal

Ahora la secuencia completa, que es la narración gráfica del pasillo con puertas del libro (Thrun et al., 2005, pp. 250-252). El robot arranca en x = 2 m sin la menor idea de dónde está, así que la nube inicial es **uniforme** sobre todo el pasillo — una creencia que un EKF no puede ni siquiera escribir.

Recorre el pasillo avanzando 1 m por paso. Fíjate en cuándo se resuelve la ambigüedad y por qué."""))

C.append(code("""# --- mundo verdadero: trayectoria y medidas ---
rng_mundo = np.random.default_rng(30)
X_VERDAD, Z = [2.0], []
for t in range(26):
    if t > 0:
        X_VERDAD.append(X_VERDAD[-1] + PASO + rng_mundo.normal(0, SIGMA_U))
    Z.append(float(h(np.array([X_VERDAD[-1]]))[0] + rng_mundo.normal(0, SIGMA_Z)))
X_VERDAD = np.array(X_VERDAD)

# --- filtro de partículas (MCL) ---
rng = np.random.default_rng(300)
P = rng.uniform(0.0, LARGO, M)                    # creencia inicial: ignorancia total
nube, neff, estim = [], [], []
for t, z in enumerate(Z):
    if t > 0:
        P = predecir(P, PASO, rng)                # 1. predecir
    w = pesar(P, z)                               # 2. pesar
    neff.append(n_efectivo(w))
    P = remuestrear(P, w, rng)                    # 3. remuestrear
    nube.append(P.copy())
    estim.append(float(np.median(P)))             # la MEDIANA, no la media: la media no significa nada
                                                  # cuando la creencia es multimodal

estim = np.array(estim)
print(f'{"paso":>5} {"x verdad":>9} {"mediana":>9} {"desv. típ.":>11} {"N_ef":>8}')
for t in [0, 1, 3, 5, 7, 8, 14, 25]:
    print(f'{t:5d} {X_VERDAD[t]:9.2f} {estim[t]:9.2f} {nube[t].std():11.2f} {neff[t]:8.0f}')"""))

C.append(code("""instantes = [0, 1, 3, 5, 8, 25]
fig, axes = plt.subplots(len(instantes), 1, figsize=(9.5, 8.0), sharex=True)
for ax, t in zip(axes, instantes):
    ax.hist(nube[t], bins=120, range=(0, LARGO), color=IQS_AZUL)
    for p in PUERTAS:
        ax.axvline(p, color=IQS_VERDE, lw=2.2, alpha=0.55)
    ax.axvline(X_VERDAD[t], color='crimson', lw=1.8, ls='--')
    ax.set_ylabel(f'paso {t}', rotation=0, ha='right', fontsize=9)
    ax.set_yticks([]); ax.grid(False)
axes[0].set_title('Nube de partículas (verde: puertas · rojo discontinuo: posición verdadera)',
                  fontsize=10)
axes[-1].set_xlabel('posición en el pasillo [m]')
plt.tight_layout(); plt.show()"""))

C.append(md("""**La secuencia que hay que narrar en clase, panel a panel.**

- *Paso 0*: la nube uniforme se convierte, con una sola medida, en **cinco cúmulos**. El robot ha pasado de «no sé nada» a «estoy en uno de estos cinco sitios». Eso ya es información, y es literalmente inexpresable con media y covarianza.
- *Paso 1*: al moverse desaparece la ambigüedad izquierda-derecha de cada puerta y quedan **tres modas**, una por cada puerta del tramo regular.
- *Pasos 3 y 5*: las tres modas se mantienen y avanzan en paralelo. El filtro no elige: **espera**, que es exactamente lo que debe hacer.
- *Paso 8*: la puerta intrusa de x = 21 rompe la periodicidad. Las hipótesis falsas predicen una distancia que no se mide, sus pesos se hunden y desaparecen en el remuestreo. La nube colapsa a **una sola moda**, la verdadera.
- *Paso 25*: seguimiento fino, con una desviación típica de unos 20 cm.

El remuestreo es el paso genuinamente nuevo y el libro le pone la metáfora exacta: es «una implementación probabilística de la idea darwiniana de la supervivencia del más apto», que reenfoca el conjunto de partículas hacia las regiones de alta probabilidad a posteriori (Thrun et al., 2005, p. 100)."""))

C.append(code("""fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.5, 4.0),
                             gridspec_kw={'width_ratios': [1.3, 1]})
for t in range(len(nube)):
    sub = nube[t][::12]                          # una de cada 12 partículas, para que se vea algo
    a1.scatter(np.full(sub.size, t), sub, s=1.2, color=IQS_AZUL, alpha=0.25)
a1.plot(range(len(nube)), X_VERDAD, color='crimson', lw=2.0, label='posición verdadera')
a1.plot(range(len(nube)), estim, color='black', lw=1.2, ls='--', label='mediana de la nube')
for p in PUERTAS:
    a1.axhline(p, color=IQS_VERDE, lw=1.6, alpha=0.5)
a1.set_xlabel('paso'); a1.set_ylabel('posición [m]'); a1.legend(fontsize=8)
a1.set_title('La nube en el tiempo: tres carriles que se funden en uno', fontsize=10)

a2.plot(neff, color=IQS_VERDE, lw=2)
a2.axhline(M/2, color='gray', ls=':', lw=1.2)
a2.text(1, M/2*1.05, 'M/2', fontsize=8, color='gray')
a2.set_xlabel('paso'); a2.set_ylabel('N efectivo')
a2.set_title(f'Partículas que cuentan de verdad (de {M})', fontsize=10)
plt.tight_layout(); plt.show()

print('Error final de la mediana:', round(float(abs(estim[-1] - X_VERDAD[-1])), 3), 'm')"""))

C.append(md("""### Ejercicio 1

Baja `M` a 100 partículas y vuelve a ejecutar la sección varias veces cambiando la semilla. ¿Cuántas veces se pierde el filtro? Explica el mecanismo: ¿en qué paso concreto muere la hipótesis correcta?

### Ejercicio 2

Quita la puerta intrusa (`PUERTAS = np.array([5.0, 15.0, 25.0])`) para que el pasillo sea perfectamente periódico y repite. ¿Colapsa alguna vez la nube? ¿Está el filtro fallando o está diciendo la verdad?"""))

C.append(code("""# Ejercicios 1 y 2: prueba aqui
# M = 100
# PUERTAS = np.array([5.0, 15.0, 25.0])"""))

# ---------------- 3. Por que el EKF fracasa
C.append(md("""## 3. Por qué el EKF fracasa exactamente aquí

Montemos el EKF equivalente sobre el mismo problema, con la misma h(x) y las mismas medidas. Su jacobiano es trivial: H = ∂h/∂x = signo(x − puerta más cercana), es decir, ±1.

Lo ejecutamos dos veces. Primero desde la **localización global**: sin información inicial, lo único razonable es inicializar en el centro del pasillo con una varianza enorme. Después desde el **seguimiento de posición**, con una buena estimación inicial — el caso para el que el EKF sí está pensado (Thrun et al., 2005, p. 194)."""))

C.append(code("""def ekf_pasillo(mu, sigma2):
    for t, z in enumerate(Z):
        if t > 0:                                        # prediccion (F = 1)
            mu, sigma2 = mu + PASO, sigma2 + SIGMA_U**2
        j = int(np.argmin(np.abs(mu - PUERTAS)))         # a que puerta cree ver
        h_mu = abs(mu - PUERTAS[j])
        H = np.sign(mu - PUERTAS[j]) or 1.0              # jacobiano: +-1
        S = H * sigma2 * H + SIGMA_Z**2
        K = sigma2 * H / S
        mu = mu + K * (z - h_mu)
        sigma2 = (1 - K * H) * sigma2
    return mu, np.sqrt(sigma2)

print(f'{"arranque":>34} {"mu final":>9} {"sigma":>7} {"verdad":>8} {"error":>7} {"error/sigma":>12}')
for nombre, mu0, s0 in [('global: centro y varianza enorme', 15.0, 75.0),
                        ('seguimiento: buena inicial      ',  2.5,  1.0)]:
    mu_f, sd_f = ekf_pasillo(mu0, s0)
    err = abs(mu_f - X_VERDAD[-1])
    print(f'{nombre:>34} {mu_f:9.2f} {sd_f:7.3f} {X_VERDAD[-1]:8.2f} {err:7.2f} {err/sd_f:12.1f}')

print('\\nFiltro de partículas desde la misma ignorancia total:',
      f'error {abs(estim[-1] - X_VERDAD[-1]):.2f} m')"""))

C.append(md("""**Ahí está la lección de la sesión, y conviene decirla despacio.** Desde la localización global el EKF no solo se equivoca: se equivoca **con una desviación típica de 17 cm**, es decir, anuncia una confianza altísima en una posición errónea por metros. El error es más de diez desviaciones típicas. Un filtro que se equivoca y lo sabe es manejable; uno que se equivoca y está convencido es peligroso, porque el planificador se cree la covarianza.

La razón no es una mala implementación: es estructural. La gaussiana solo tiene una moda, así que en cuanto la creencia verdadera se reparte entre tres puertas, el filtro tiene que elegir una — y una vez elegida, cada nueva medida la refuerza, porque es coherente con la puerta equivocada. Con la buena inicialización, en cambio, el mismo código funciona perfectamente: el EKF es un excelente seguidor de posición y un pésimo localizador global.

MCL es, en palabras del libro, «posiblemente el algoritmo de localización más popular hasta la fecha» (Thrun et al., 2005, p. 238), y esta comparación explica por qué: es el que los robots reales necesitan al encenderse."""))

# ---------------- 4. Secuestro
C.append(md("""## 4. El robot secuestrado y la inyección de partículas

El MCL básico hereda del remuestreo un defecto letal: con el tiempo, todas las partículas acaban cerca de una sola moda, y si el robot es **secuestrado** —«teletransportado a otro lugar» durante la operación (Thrun et al., 2005, p. 194)— no queda ninguna hipótesis cerca de la verdad, y ninguna cantidad de remuestreo puede resucitar una hipótesis que ya no existe.

La cura clásica es «la inyección de partículas aleatorias» en cada iteración (Thrun et al., 2005, p. 256). Vamos a medir cuánto hace falta inyectar."""))

C.append(code("""def mcl_con_secuestro(fraccion_inyectada, pasos=40, paso_secuestro=20):
    rng = np.random.default_rng(300)
    rng_m = np.random.default_rng(31)
    P = rng.uniform(0.0, LARGO, M)
    x, errores, verdad = 2.0, [], []
    for t in range(pasos):
        if t > 0:
            x = x + PASO + rng_m.normal(0, SIGMA_U)
            if t == paso_secuestro:
                x = 2.0                                # SECUESTRO: de vuelta al principio
            P = predecir(P, PASO, rng)
        z = float(h(np.array([x]))[0] + rng_m.normal(0, SIGMA_Z))
        P = remuestrear(P, pesar(P, z), rng)
        if fraccion_inyectada > 0:                     # partículas nuevas repartidas al azar
            n = int(fraccion_inyectada * M)
            P[rng.integers(0, M, n)] = rng.uniform(0.0, LARGO, n)
        errores.append(abs(np.median(P) - x)); verdad.append(x)
    return np.array(errores), np.array(verdad)

fig, ax = plt.subplots(figsize=(9, 3.8))
for frac, color in [(0.0, 'crimson'), (0.02, 'darkorange'), (0.05, IQS_AZUL)]:
    err, verdad = mcl_con_secuestro(frac)
    ax.plot(err, color=color, lw=1.8, label=f'inyección {frac*100:.0f} %')
    print(f'inyección {frac*100:4.1f} %  ->  error tras 1 paso: {err[21]:5.2f} m,'
          f'   tras 7 pasos: {err[27]:5.2f} m,   tras 19 pasos: {err[39]:5.2f} m')
ax.axvline(20, color='black', ls=':', lw=1.5)
ax.text(20.4, ax.get_ylim()[1]*0.85, 'secuestro', fontsize=8)
ax.set_xlabel('paso'); ax.set_ylabel('error de la mediana [m]'); ax.legend(fontsize=8)
ax.set_title('Sin partículas nuevas no hay recuperación posible', fontsize=10)
plt.tight_layout(); plt.show()"""))

C.append(md("""Sin inyección el filtro **no se recupera nunca**: se queda a veinte metros de la verdad, y no porque el algoritmo esté mal, sino porque no queda ninguna partícula donde está el robot y el remuestreo solo puede copiar lo que ya existe. Lo poco que baja el error al final de la simulación es un artefacto del final del pasillo, que comprime la nube contra la pared.

Con inyección la recuperación es completa, y su ritmo dice algo interesante: hacen falta unos siete pasos con el 5 % y unos diez con el 2 %. No es solo que la nube tarde en migrar; es que **el robot secuestrado tiene que volver a resolver la localización global desde cero**, con sus modas y todo, y eso cuesta los mismos pasos que costó al principio de la sesión. Durante ese tránsito la mediana señala a la mayoría equivocada, lo cual es un buen recordatorio de que resumir una creencia multimodal con un solo número es tirar información.

En un sistema real no se inyecta una fracción fija sino que se **liga la inyección al rendimiento del filtro**: se añaden partículas cuando la verosimilitud media de las medidas se desploma, señal de que la nube ya no explica lo que el sensor ve (Thrun et al., 2005, pp. 256-257). Así, en operación normal apenas se añaden y tras un secuestro la inyección repuebla el mapa. La otra mejora práctica es el tamaño adaptativo de la nube: muchas partículas mientras la creencia está dispersa, pocas cuando está concentrada — la idea del KLD-sampling que implementan los MCL adaptativos, y por tanto AMCL, el nodo de localización de Nav2 que los equipos ejecutarán en el bloque 7.

### Ejercicio 3

Implementa la versión adaptativa: en lugar de una fracción fija, calcula en cada paso la verosimilitud media `pesar(...)` **antes** de normalizar y usa su caída respecto a la media histórica para decidir cuántas partículas inyectar. Comprueba que en operación normal inyecta casi cero y que tras el secuestro dispara."""))

C.append(code("""# Ejercicio 3: prueba aqui
# w_sin_normalizar = np.exp(-0.5*((z - h(P))/SIGMA_Z)**2)
# verosimilitud_media = w_sin_normalizar.mean()"""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.** Con M = 100 el filtro se pierde con frecuencia. El mecanismo es concreto y hay que verlo: en el paso 0, repartir 100 partículas sobre 30 m deja unas 3 partículas por metro, así que a cada uno de los cinco cúmulos le tocan muy pocas; el remuestreo, que es un sorteo, puede fácilmente no sacar ninguna del cúmulo correcto. Y una vez muerta, la hipótesis verdadera no vuelve: el remuestreo copia, no crea. Este es el argumento cuantitativo de por qué el número de partículas necesario crece con el volumen del espacio de estados, y por qué el filtro de partículas es imbatible en la pose 3D de un robot móvil e inviable, en su forma ingenua, sobre el estado gigante del SLAM.

**Ejercicio 2.** Con el pasillo perfectamente periódico la nube **nunca** colapsa: se queda indefinidamente con tres modas equiespaciadas que avanzan en paralelo. Y el filtro no está fallando: está diciendo exactamente la verdad, que es que el problema no tiene solución única. Ningún algoritmo puede distinguir posiciones que generan medidas idénticas. La lección de ingeniería es que la ambigüedad se resuelve en el **entorno** —una puerta distinta, un marcador, una baliza UWB— y no en el estimador.

**Ejercicio 3.** La verosimilitud media sin normalizar es el mejor detector de «me he perdido» que tiene un filtro de partículas: mientras la nube explica las medidas se mantiene alta y estable, y en cuanto el robot es secuestrado se desploma uno o dos órdenes de magnitud en un solo paso. Una regla que funciona es inyectar una fracción proporcional a max(0, 1 − verosimilitud_actual / media_móvil), acotada por arriba. Es la versión práctica del *augmented MCL* del libro, y su virtud es no pagar nada en operación normal."""))

C.append(md("""---

## Para llevarse de esta sesión

El filtro de partículas no es un filtro distinto: es **el mismo filtro de Bayes de S28** con la creencia representada por muestras en lugar de por momentos. Predecir es mover cada muestra con su propio ruido, corregir es pesar por la verosimilitud, y el remuestreo es lo único genuinamente nuevo — la supervivencia del más apto (Thrun et al., 2005, p. 100).

Lo que se compra con ese cambio de representación es la capacidad de decir «podría estar aquí o allá», y eso es justo lo que la localización global exige. Lo que se paga es cómputo, y una diversidad que hay que administrar: remuestrear demasiado empobrece la nube, y un secuestro sin inyección de partículas no tiene arreglo.

Y una regla que conviene fijar antes del bloque 7: **con la pose inicial conocida y modelos suaves, EKF; sin pose inicial o con ambigüedad, partículas.** No son competidores, son herramientas para regímenes distintos — y en la práctica muchos sistemas usan MCL para arrancar y un filtro gaussiano para el seguimiento fino.

Queda la última pregunta del bloque, que abre S31: todo esto ha supuesto que el mapa lo teníamos. ¿Y si no?

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S30_Filtro_Particulas_MCL.ipynb', C)
print('escrito S30')
