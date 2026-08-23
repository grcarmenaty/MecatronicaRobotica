from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('scipy','scipy'), ('matplotlib','matplotlib'), ('control','control')]
C = []

C.append(cabecera(
    "S23", "Espacio de estados, controlabilidad y realimentación de estado", "5",
    "miércoles 4 de noviembre de 2026", "1 h",
    "La tercera forma del modelo, pendiente desde S20: escribe el motor como cuádrupla (A, B, C, D), comprueba que la conversión de ida y vuelta con la función de transferencia no pierde nada, aplica la condición de rango de Kalman a un sistema controlable y a uno que no lo es, y diseña una realimentación de estado por asignación de polos midiendo lo que cuesta en amplitud de mando.",
    "De Silva et al. (2016), cap. 4 — las tres formas del modelo (p. 88), definición del espacio de estados y dimensiones de A, B, C y D (p. 90, ecs. 4.5-4.6), el disco duro como misma planta en tres formas (p. 90, ecs. 4.7-4.8), observador en la estructura de servocontrol (p. 102, fig. 4.15); Lynch y Park (2017) — condición de rango de Kalman rank[B AB … Aⁿ⁻¹B] = n y existencia de u = −K·x (p. 528), robots no holonómicos y controlabilidad no lineal (pp. 528-529), lectura del mapa de polos (p. 412); documentación de python-control (sin página).",
    "los apuntes del bloque 5"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
import control as ct

np.set_printoptions(precision=4, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.2)
plt.rcParams['axes.grid'] = True
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('python-control', ct.__version__, '- listo.')"""))

# ---------------- 1. La representacion en espacio de estados
C.append(md("""## 1. El mismo motor con otra ropa

«Un sistema también puede describirse usando una descripción por variables de estado, llamada espacio de estados, que es una colección de ecuaciones diferenciales»:

`ẋ = A·x + B·u`
`y = C·x + D·u`

«donde x es un vector columna (n×1) que representa los estados de un sistema de orden n, u es un vector columna (m×1) que representa las entradas, y es un vector columna (p×1) que representa la salida, A es la matriz del sistema (n×n), B la matriz de entrada (n×m), C la matriz de salida (p×n) y D la matriz de transmisión directa (p×m)» (De Silva et al., 2016, p. 90, ecs. 4.5-4.6).

Para el motor de S20, con `x = [θ, ω]` y salida de posición, las matrices se leen **directamente** de la EDO reducida `θ̈ = −(K1/I)·θ̇ + (K2/I)·u`:

`A = [[0, 1], [0, −K1/I]]`,  `B = [0, K2/I]ᵀ`,  `C = [1, 0]`,  `D = 0`

La primera fila de `A` no dice nada de física: dice que la derivada de la posición es la velocidad. Es contabilidad. Toda la física está en la segunda fila y en `B`."""))

C.append(code("""I, K1, K2 = 5.0e-4, 0.00302, 0.05        # el motor de S20

A = np.array([[0.0, 1.0],
              [0.0, -K1/I]])
B = np.array([[0.0],
              [K2/I]])
Cm = np.array([[1.0, 0.0]])              # medimos la posición
Dm = np.array([[0.0]])

motor_ss = ct.ss(A, B, Cm, Dm)
print(motor_ss)
print()
print('Autovalores de A :', np.round(np.linalg.eigvals(A), 3))
print('Polos del sistema:', np.round(ct.poles(motor_ss), 3), ' <- son lo mismo, por definición')"""))

C.append(md("""**Ida y vuelta.** Las conversiones `ct.ss2tf` y `ct.tf2ss` transitan entre formas sin pérdida de información (python-control docs, sin página). De Silva lo ilustra con su disco duro: la misma planta de cuarto orden aparece como función de transferencia, como cero-polo-ganancia y como cuádrupla de matrices (2016, p. 90, ecs. 4.7-4.8). Comprobémoslo con el motor y, ya puestos, con el modelo de tercer orden completo."""))

C.append(code("""G_desde_ss = ct.ss2tf(motor_ss)
print('De espacio de estados a función de transferencia:')
print(G_desde_ss)
print('Ese "+" suelto delante del 100 es un coeficiente de orden 1e-16: ruido numérico')
print('de la conversión, no un cero real del sistema.')
print()

G_th3 = ct.tf([8e4], [1, 800, 4832, 0])         # motor completo de S21
ss3 = ct.tf2ss(G_th3)
print('De función de transferencia a espacio de estados (3.er orden):')
print('A =\\n', np.round(ss3.A, 2))
print('B =', np.round(ss3.B.ravel(), 4), '   C =', np.round(ss3.C.ravel(), 4))
print()
print('Polos de la FT      :', np.round(ct.poles(G_th3), 2))
print('Autovalores de la A :', np.round(np.linalg.eigvals(ss3.A), 2))"""))

C.append(md("""Fíjate en que las matrices que devuelve `tf2ss` **no son** las que habríamos escrito a mano: python-control usa una realización canónica propia, con estados que no tienen significado físico. Es un punto que conviene subrayar en clase: la función de transferencia determina el comportamiento entrada-salida, pero **no** determina las variables de estado. Hay infinitas realizaciones del mismo sistema, todas con los mismos autovalores. Elegir estados con significado físico —posición, velocidad, corriente— es decisión del ingeniero, y es la que hace que el modelo sirva para diagnosticar y no solo para simular.

Qué gana el ingeniero con la forma matricial, en tres puntos:

1. **Generalidad.** Varias entradas y varias salidas caben sin cambiar nada: las dimensiones de `u` e `y` son parámetros, no supuestos.
2. **Visibilidad interna.** La función de transferencia solo relaciona entrada con salida; el estado expone las variables internas —la velocidad, la corriente— aunque no se midan.
3. **Las preguntas de diseño se vuelven álgebra lineal.** La estabilidad son los autovalores de `A`, la controlabilidad es un rango, y el diseño del controlador es la elección de una matriz `K`. Eso es el resto de la sesión.

### Ejercicio 1

Escribe a mano el espacio de estados del motor **con la velocidad como salida** en lugar de la posición (`C = [0, 1]`), conviértelo con `ct.ss2tf` y comprueba que sale `K2/(I·s + K1)`, la función de transferencia de S20. ¿Por qué desaparece un polo si `A` sigue siendo 2×2?"""))

C.append(code("""# Ejercicio 1
# motor_vel = ct.ss(A, B, np.array([[0.0, 1.0]]), Dm)
# print(ct.ss2tf(motor_vel))"""))

# ---------------- 2. Controlabilidad y observabilidad
C.append(md("""## 2. ¿Se puede? Controlabilidad y observabilidad

Antes de diseñar una realimentación conviene saber si el problema tiene solución. Los sistemas lineales «se saben linealmente controlables si se satisface la condición de rango de Kalman:

`rank[B  A·B  A²·B  ⋯  Aⁿ⁻¹·B] = dim(x) = n`»

(Lynch y Park, 2017, p. 528). La intuición, sin pretensión de demostración: la columna `B` es la dirección en la que la entrada empuja el estado **ahora**; `A·B` es adónde la dinámica propaga ese empujón un instante después; `A²·B`, dos instantes después. Si esas direcciones generan todo el espacio, cualquier punto es alcanzable componiendo empujones; si no, hay un subespacio al que la entrada nunca llega.

Su hermana simétrica es la **observabilidad**: ¿determinan las medidas el estado? Se comprueba con el rango de `[C; C·A; …; C·Aⁿ⁻¹]`. En python-control, `ct.ctrb(A, B)` y `ct.obsv(A, C)`."""))

C.append(code("""Co = ct.ctrb(A, B)
print('Matriz de controlabilidad [B  A·B]:'); print(Co)
print(f'rango = {np.linalg.matrix_rank(Co)} de {A.shape[0]}  ->  controlable\\n')

Ob_pos = ct.obsv(A, Cm)
print('Observabilidad midiendo la POSICIÓN:'); print(Ob_pos)
print(f'rango = {np.linalg.matrix_rank(Ob_pos)} de {A.shape[0]}  ->  observable\\n')

C_vel = np.array([[0.0, 1.0]])
Ob_vel = ct.obsv(A, C_vel)
print('Observabilidad midiendo solo la VELOCIDAD:'); print(Ob_vel)
print(f'rango = {np.linalg.matrix_rank(Ob_vel)} de {A.shape[0]}  ->  NO observable')"""))

C.append(md("""El segundo resultado tiene una lectura física inmediata y muy buena para el aula: **con un tacómetro no se puede saber dónde está el eje**. Integrando la velocidad se obtiene la posición salvo una constante desconocida, y esa constante es el estado inobservable. Es exactamente el motivo por el que un servo lleva encoder de posición y no solo tacogenerador, y el mismo argumento que en el bloque 6 justifica que la odometría necesite una referencia externa.

Ahora el contraejemplo de controlabilidad. Añadimos al motor un tercer estado: la **temperatura del bobinado**, que evoluciona con su propia constante de tiempo y que ningún actuador térmico controla."""))

C.append(code("""TAU_TERM = 30.0        # s, constante de tiempo térmica del bobinado

A3 = np.block([[A,                np.zeros((2, 1))],
               [np.zeros((1, 2)), np.array([[-1/TAU_TERM]])]])
B3 = np.vstack([B, [[0.0]]])          # la tensión no calienta directamente en este modelo

Co3 = ct.ctrb(A3, B3)
print('A ampliada con el estado térmico:'); print(np.round(A3, 4))
print('\\nB ampliada:', B3.ravel())
print(f'\\nrango de controlabilidad = {np.linalg.matrix_rank(Co3)} de {A3.shape[0]}  ->  NO controlable')
print('El subespacio inalcanzable es justamente la dirección de la temperatura:')
print('  ninguna combinación de B, A·B y A²·B tiene componente en la tercera coordenada.')
print('\\nAutovalores:', np.round(np.linalg.eigvals(A3), 4),
      ' <- el modo térmico es estable, así que el sistema es *estabilizable* aunque no controlable.')"""))

C.append(md("""La distinción del último renglón merece medio minuto: un modo **no controlable pero estable** no impide diseñar un controlador; simplemente hay que aceptar que ese modo evoluciona solo. Lo que sí sería fatal es un modo no controlable e **inestable**.

**Nota cultural que conecta con el bloque 7.** La importancia del resultado se aprecia donde falla. Lynch y Park introducen la condición de Kalman precisamente para robots móviles: la cinemática del uniciclo linealizada no pasa el test —«no hay ningún controlador lineal que pueda estabilizar la configuración completa del chasis para un robot no holonómico; el robot no holonómico no es linealmente controlable»— y sin embargo el coche aparca, porque existen nociones **no lineales** de controlabilidad bajo las cuales el sistema sí lo es, ya que la restricción de velocidad no reduce el conjunto de configuraciones alcanzables (Lynch y Park, 2017, pp. 528-529).

### Ejercicio 2

Modifica `B3` para que la tensión sí caliente el bobinado (por ejemplo, tercera componente `0.05`). ¿Pasa el sistema a ser controlable? Comprueba el rango y explica el resultado en términos físicos: ¿puedes llevar el motor a *cualquier* combinación de posición, velocidad y temperatura?"""))

C.append(code("""# Ejercicio 2
# B3b = np.vstack([B, [[0.05]]])
# print(np.linalg.matrix_rank(ct.ctrb(A3, B3b)))"""))

# ---------------- 3. Realimentacion de estado
C.append(md("""## 3. Realimentación de estado: `u = −K·x`

Si el PID combinaba el error, su integral y su derivada, la realimentación de estado generaliza la idea: medir (o estimar) el vector de estados completo y aplicar `u = −K·x`. Para un sistema linealmente controlable esta estructura basta, porque «la controlabilidad lineal implica la existencia de la ley de control lineal simple `u = −K·x`» que estabiliza el origen (Lynch y Park, 2017, p. 528).

El diseño por **asignación de polos** hace explícito el vínculo con S21: en lazo cerrado la dinámica es

`ẋ = (A − B·K)·x`

de modo que elegir `K` equivale a colocar los autovalores de `A − B·K` donde el transitorio deseado los pida, con las mismas reglas de lectura del mapa de polos —parte real, rapidez; parte imaginaria, oscilación— (Lynch y Park, 2017, p. 412). En python-control es una línea: `K = ct.place(A, B, polos)`.

Comparamos dos juegos: unos polos moderados en `−5 ± 5j` y otros agresivos en `−20 ± 5j`, partiendo de un error inicial de 1 rad."""))

C.append(code("""t = np.linspace(0, 1.5, 900)
X0 = [1.0, 0.0]                    # 1 rad de error de posición, en reposo

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 3.6))
print(f'{"polos deseados":>22} {"K = [k1, k2]":>22} {"|u| máximo [V]":>16} {"t al 2 % [s]":>14}')
print('-'*78)
for polos, col in [([-5+5j, -5-5j], IQS_AZUL), ([-20+5j, -20-5j], IQS_VERDE)]:
    K = ct.place(A, B, polos)
    lazo = ct.ss(A - B@K, B, Cm, Dm)
    resp = ct.initial_response(lazo, t, X0=X0)
    u = -(K @ resp.states).ravel()
    fuera = np.where(np.abs(resp.outputs) > 0.02)[0]
    ts = t[fuera[-1]] if len(fuera) else 0.0
    a1.plot(t, resp.outputs, lw=2, color=col, label=f'polos en {polos[0]:.0f}')
    a2.plot(t, u, lw=2, color=col, label=f'polos en {polos[0]:.0f}')
    print(f'{str(np.round(polos, 1)):>22} {str(np.round(K.ravel(), 4)):>22} {np.abs(u).max():16.2f} {ts:14.3f}')

a1.axhline(0, color='grey', ls=':', lw=1)
a1.set_xlabel('t [s]'); a1.set_ylabel('theta [rad]'); a1.set_title('Regulación desde 1 rad de error')
a1.legend(fontsize=8)
a2.set_xlabel('t [s]'); a2.set_ylabel('u [V]'); a2.set_title('Mando: el precio de ir deprisa')
plt.tight_layout(); plt.show()"""))

C.append(md("""**Cuatro veces más rápido, ocho veces y media más mando.** Es la lección que hay que dejar clavada: la asignación de polos no tiene coste en el papel —cualquier juego de polos es alcanzable si el sistema es controlable— pero sí en el amplificador. Y si el mando pedido supera el tope del actuador, el diseño lineal deja de valer y volvemos exactamente al problema de S22: saturación.

Hay una observación más, que cierra el círculo del bloque. Para el motor con `x = [θ, ω]`, la ley

`u = −k1·θ − k2·ω`

es **formalmente un PD** con `Kp = k1` y `Kd = k2` sobre la referencia cero. La realimentación de estado contiene a nuestros controladores anteriores como casos particulares; lo que aporta es un método sistemático para elegir las ganancias en lugar de sintonizarlas a mano (observación docente; sin cita de libro)."""))

C.append(code("""for polos in [[-5+5j, -5-5j], [-20+5j, -20-5j]]:
    K = ct.place(A, B, polos)
    Kp_equiv, Kd_equiv = K.ravel()
    zeta = (K1/I + K2/I*Kd_equiv) / (2*np.sqrt(K2/I*Kp_equiv))
    wn = np.sqrt(K2/I*Kp_equiv)
    print(f'polos {str(np.round(polos,1)):>18}  ->  PD equivalente Kp = {Kp_equiv:6.3f} V/rad, '
          f'Kd = {Kd_equiv:6.4f} V·s/rad   (wn = {wn:5.2f} rad/s, zeta = {zeta:4.2f})')"""))

C.append(md("""### Ejercicio 3

El amplificador del motor da como mucho **10 V**. Encuentra el par de polos de la forma `−a ± 5j` más rápido (mayor `a`) que respeta ese límite partiendo de 1 rad de error. Sugerencia: barre `a` de 5 a 60 y quédate con el mayor que cumpla."""))

C.append(code("""# Ejercicio 3
# for a in range(5, 61, 5):
#     K = ct.place(A, B, [-a+5j, -a-5j])
#     ..."""))

# ---------------- 4. Cierre: observador y LQR
C.append(md("""## 4. Dos cabos sueltos: el observador y el LQR

**¿Y si no medimos todo el estado?** La ley `u = −K·x` necesita `x` completo y rara vez se mide todo. La respuesta industrial es el **observador**, que aparece como un bloque en la estructura de servocontrol de De Silva: «la realimentación de control requiere la medición de todos los estados del sistema… y sin embargo a menudo no es factible medir todos los estados por practicidad, coste u otras razones. Aquí es cuando se emplea un observador para estimar todos los estados del sistema a partir de un número limitado de medidas reales. La eficacia del observador depende de la exactitud del modelo del observador al estimar los estados» (2016, p. 102, fig. 4.15). Corre el modelo en paralelo con la planta y corrige su estimación con la discrepancia en las salidas medidas; su diseño es formalmente **dual** al de `K` —de ahí que la observabilidad se compruebe igual que la controlabilidad— y es, en esencia, el filtro de Kalman que el bloque 6 desarrollará en detalle.

**¿Y si no sé qué polos quiero?** La alternativa a imponerlos es el **LQR**: elegir `K` minimizando un coste cuadrático que pesa el error de estado contra el esfuerzo de control, `∫(xᵀQx + uᵀRu)dt`. En python-control, `ct.lqr(A, B, Q, R)` (docs, sin página). Es la primera aparición del diseño por optimización, que en el bloque 8 volverá convertido en aprendizaje por refuerzo."""))

C.append(code("""print(f'{"R (peso del mando)":>20} {"K = [k1, k2]":>22} {"polos resultantes":>28} {"|u(0)| [V]":>12}')
print('-'*86)
Q = np.diag([100.0, 1.0])
for R in [0.01, 1.0, 100.0]:
    K, S, E = ct.lqr(A, B, Q, np.array([[R]]))
    u0 = abs(float(np.ravel(K @ np.array(X0))[0]))
    print(f'{R:20.2f} {str(np.round(K.ravel(), 3)):>22} {str(np.round(E, 1)):>28} {u0:12.2f}')

print()
print('Subir R = penalizar el mando = polos más lentos y menos voltios.')
print('Es el mismo compromiso de la sección 3, pero elegido con un criterio explícito')
print('en lugar de a ojo sobre el plano complejo.')"""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.** Con `C = [0, 1]`, `ct.ss2tf` devuelve `100·s/(s² + 6.04·s)`, y aquí está lo interesante: **no simplifica**. Al tomar la velocidad como salida aparece un cero en el origen que cancela exactamente el polo del origen; tachándolos a mano queda `100/(s + 6.04)`, que es `K2/(I·s + K1)` dividido arriba y abajo por `I` — la función de transferencia de S20. Si se quiere la forma reducida, `ct.minreal` hace la cancelación. La lección es la incómoda: el polo del integrador **no ha desaparecido** del sistema —los autovalores de `A` siguen siendo 0 y −6.04— sino que ha dejado de ser visible desde ese par entrada-salida. La función de transferencia solo muestra la parte del sistema que es a la vez controlable y observable; en espacio de estados no hay cancelaciones silenciosas, y por eso es la representación que se usa para diseñar.

**Ejercicio 2.** Sí: con `B3 = [0, 100, 0.05]ᵀ` la matriz de controlabilidad pasa a rango 3 y el sistema es controlable. Pero conviene desconfiar del resultado. Que el rango sea 3 significa que existe una entrada que lleva el estado a cualquier punto **en teoría**; en la práctica, la dirección térmica está tan mal condicionada (basta mirar los valores singulares de la matriz de controlabilidad, que difieren en varios órdenes de magnitud) que fijar la temperatura a un valor arbitrario exigiría tensiones absurdas durante minutos. La controlabilidad es una propiedad binaria; el **grado** de controlabilidad, que es lo que importa en ingeniería, lo dan los valores singulares. Misma diferencia que entre «el jacobiano no es singular» y «el robot está lejos de la singularidad», que ya discutimos en el bloque 4.

**Ejercicio 3.** Con el barrido de 5 en 5, el mayor valor que cumple es `a = 30`: `K = ct.place(A, B, [-30+5j, -30-5j])` da `k1 = 9.25` y un mando inicial de 9.25 V. Afinando, el límite exacto está en `a = 31` (9.86 V); con `a = 32` el mando ya pide 10.5 V. La cuenta se puede hacer sin simular: el polinomio deseado es `s² + 2a·s + (a²+25)`, y comparándolo con el del lazo cerrado sale `k1 = (a²+25)/(K2/I) = (a²+25)/100`. Obsérvese que el mando inicial es prácticamente `k1·θ(0)`, porque en `t = 0` la velocidad es nula: **el pico de mando de una realimentación de estado lo fija la ganancia de posición multiplicada por el error inicial**. Es una regla de dimensionado directa: si conoces el mayor salto de referencia que vas a pedir, conoces el mayor mando que necesitarás, y con eso se elige el amplificador (o se limita la agresividad del diseño)."""))

C.append(md("""---

## Para llevarse de esta sesión

La función de transferencia y el espacio de estados son **el mismo sistema**, y python-control transita entre ambos en una línea. Lo que cambia es lo que cada forma deja ver: la primera, la relación entrada-salida; la segunda, todas las variables internas y las cancelaciones que la primera esconde.

La controlabilidad es un **rango**, y responde a una pregunta que hay que hacerse antes de diseñar nada: ¿puede la entrada llevar el estado a donde quiero? Su hermana, la observabilidad, responde a la simétrica: ¿determinan mis sensores el estado? Un tacómetro solo no observa la posición, y ese hecho de tres líneas de álgebra decide el catálogo de sensores de un servo.

Colocar polos es diseñar. Y colocarlos lejos a la izquierda **cuesta voltios**: la asignación de polos no tiene coste en el papel, pero el amplificador sí lo tiene. Esa es la misma frontera que en S22 nos encontramos como saturación, y la que el LQR permite negociar de forma explícita.

Mañana, en S24, damos el último paso del bloque: de un eje con parámetros constantes a un manipulador donde la matriz de inercia cambia con la configuración y las articulaciones se estorban entre sí.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S23_Espacio_Estados.ipynb', C)
print('escrito S23')
