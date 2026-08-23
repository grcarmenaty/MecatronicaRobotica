from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('matplotlib','matplotlib'), ('spatialmath-python','spatialmath')]
C = []

C.append(cabecera(
    "S14", "Cinemática directa: trigonometría, Denavit-Hartenberg y PoE", "4",
    "miércoles 14 de octubre de 2026", "1 h",
    "Resuelve la cinemática directa de un 2R y de un 3R planos dos veces —a mano con trigonometría y con una tabla de parámetros de Denavit-Hartenberg— y comprueba numéricamente que las dos descripciones son el mismo objeto matemático. Cierra con el producto de exponenciales de Lynch y Park como tercera vía.",
    "Lynch y Park (2017), cap. 4 — definición de cinemática directa (p. 137) y fórmula del producto de exponenciales, ecuación 4.14 (p. 142), más la fórmula de Rodrigues del cap. 3 (p. 84); Corke (2023), cap. 7 — la FK como mapeo de coordenadas articulares a pose (p. 255), ETS del brazo de un eslabón (p. 256), evaluación con fkine (p. 257), el 2R plano en q = (30°, 40°) con t = 1.21, 1.44 y orientación 70° (p. 258), muñeca esférica ZYZ del 6R (p. 260), la tabla DH y sus cuatro parámetros (p. 274) y la secuencia elemental de cada fila, ecuación 7.4 (p. 275).",
    "los apuntes del bloque 4"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
from spatialmath import SE2, SE3

np.set_printoptions(precision=4, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.4)
plt.rcParams['axes.grid'] = True
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('Listo.')"""))

# ---------------- 1. El 2R a mano
C.append(md("""## 1. El 2R plano, a mano

«La cinemática directa de un robot se refiere al cálculo de la posición y orientación del marco de su efector final a partir de sus coordenadas articulares» (Lynch y Park, 2017, p. 137); en la formulación de Corke, «un mapeo de las coordenadas articulares, o configuración del robot, a la pose del efector» (Corke, 2023, p. 255).

Conviene subrayar en clase la asimetría con lo que viene después: **la FK siempre existe, es única y es barata**. Toda la dificultad de la cinemática de manipuladores vive en el problema inverso (S16) y en el diferencial (S17).

Para el brazo plano de dos eslabones la trigonometría cabe en dos líneas, proyectando cada eslabón sobre los ejes:

```
x     = a1·cos(q1) + a2·cos(q1 + q2)
y     = a1·sin(q1) + a2·sin(q1 + q2)
theta = q1 + q2
```

La referencia numérica de contraste es la del libro: con `a1 = a2 = 1` y `q = (30°, 40°)` el efector queda en `t = 1.21, 1.44` con orientación 70 grados (Corke, 2023, p. 258)."""))

C.append(code("""A1, A2 = 1.0, 1.0        # longitudes de los eslabones (m)

def fk_2r_mano(q, a1=A1, a2=A2):
    \"\"\"Cinematica directa del 2R plano por trigonometria. Devuelve (x, y, theta).\"\"\"
    q1, q2 = q
    x = a1 * np.cos(q1) + a2 * np.cos(q1 + q2)
    y = a1 * np.sin(q1) + a2 * np.sin(q1 + q2)
    return np.array([x, y, q1 + q2])

q_ref = np.deg2rad([30.0, 40.0])
x, y, th = fk_2r_mano(q_ref)
print(f'q = (30°, 40°)  ->  t = {x:.4f}, {y:.4f}   orientación = {np.rad2deg(th):.1f}°')
print('Valor del libro  ->  t = 1.21, 1.44        orientación = 70°   (Corke, 2023, p. 258)')

# unos cuantos casos limite que conviene tener en la cabeza
for etq, qq in [('brazo estirado  ', [0.0, 0.0]),
                ('codo a 90°      ', [0.0, np.pi/2]),
                ('brazo replegado ', [0.0, np.pi])]:
    xx, yy, tt = fk_2r_mano(qq)
    print(f'{etq} q = {np.rad2deg(qq).round(0)}  ->  t = ({xx:.3f}, {yy:.3f})  '
          f'|t| = {np.hypot(xx, yy):.3f}')"""))

C.append(md("""Un dibujo del brazo vale por media hora de explicación. Dibujamos la cadena eslabón a eslabón: cada articulación es un punto y cada eslabón un segmento."""))

C.append(code("""def puntos_2r(q, a1=A1, a2=A2):
    \"\"\"Coordenadas de base, codo y punta.\"\"\"
    q1, q2 = q
    p0 = np.array([0.0, 0.0])
    p1 = p0 + a1 * np.array([np.cos(q1), np.sin(q1)])
    p2 = p1 + a2 * np.array([np.cos(q1 + q2), np.sin(q1 + q2)])
    return np.vstack([p0, p1, p2])

fig, ax = plt.subplots(figsize=(5.6, 4.6))
posturas = {'q = (30°, 40°)': np.deg2rad([30, 40]),
            'q = (60°, -80°)': np.deg2rad([60, -80]),
            'q = (110°, 20°)': np.deg2rad([110, 20])}
for (etq, qq), col in zip(posturas.items(), [IQS_AZUL, IQS_VERDE, 'crimson']):
    P = puntos_2r(qq)
    ax.plot(P[:, 0], P[:, 1], 'o-', lw=3, ms=7, color=col, label=etq)

# espacio de trabajo alcanzable: corona circular entre |a1-a2| y a1+a2
ang = np.linspace(0, 2*np.pi, 200)
ax.plot((A1+A2)*np.cos(ang), (A1+A2)*np.sin(ang), ':', color='grey', lw=1)
ax.set_aspect('equal'); ax.legend(fontsize=8)
ax.set_title('El 2R plano en tres configuraciones')
plt.tight_layout(); plt.show()"""))

# ---------------- 2. El 3R a mano
C.append(md("""## 2. El 3R plano: la cadena se alarga, la idea no cambia

Añadir un eslabón no añade ninguna idea nueva: cada eslabón aporta su proyección y los ángulos se **acumulan**. Este es el punto que hay que dejar claro antes de introducir cualquier convención, porque después las convenciones ocultan esta simplicidad detrás de una notación.

```
x     = a1·cos(q1) + a2·cos(q1+q2) + a3·cos(q1+q2+q3)
y     = a1·sin(q1) + a2·sin(q1+q2) + a3·sin(q1+q2+q3)
theta = q1 + q2 + q3
```

El 3R plano tiene además una propiedad que se explota en S16: con tres grados de libertad en un espacio de tareas de tres dimensiones (x, y, θ) el problema inverso tiene solución para poses completas, no solo para posiciones."""))

C.append(code("""A = np.array([1.0, 0.8, 0.4])     # a1, a2, a3

def fk_nr_mano(q, a=A):
    \"\"\"FK de un brazo plano de n eslabones. Devuelve (x, y, theta) y los puntos.\"\"\"
    acum = np.cumsum(np.asarray(q, float))          # angulos acumulados
    P = np.zeros((len(q) + 1, 2))
    for j, (aj, thj) in enumerate(zip(a, acum)):
        P[j+1] = P[j] + aj * np.array([np.cos(thj), np.sin(thj)])
    return np.array([P[-1, 0], P[-1, 1], acum[-1]]), P

q3 = np.deg2rad([25.0, 45.0, -30.0])
pose3, P3 = fk_nr_mano(q3)
print('3R en q = (25°, 45°, -30°):')
print(f'  t = ({pose3[0]:.4f}, {pose3[1]:.4f})   theta = {np.rad2deg(pose3[2]):.1f}°')
print('  puntos de la cadena (base, codo1, codo2, punta):\\n', P3.round(4))

# el 2R es el caso particular con a3 = 0
pose2, _ = fk_nr_mano(np.deg2rad([30, 40, 0]), a=[A1, A2, 0.0])
print('\\n¿fk_nr_mano reproduce fk_2r_mano?',
      np.allclose(pose2, fk_2r_mano(np.deg2rad([30, 40]))))"""))

# ---------------- 3. DH
C.append(md("""## 3. La misma cadena con parámetros de Denavit-Hartenberg

Desde los años sesenta, «bastante antes de la llegada de URDF», la forma estándar de compartir un modelo de brazo es una tabla en la que cada fila describe la relación entre dos marcos de eslabón consecutivos con solo **cuatro** parámetros `(theta_j, d_j, a_j, alpha_j)` (Corke, 2023, p. 274). Cada fila equivale a una secuencia de cuatro transformaciones elementales:

`A_j = Rz(theta_j) · Tz(d_j) · Tx(a_j) · Rx(alpha_j)`   (ecuación 7.4; Corke, 2023, p. 275)

y la cinemática directa es el producto de todas ellas. Cuatro parámetros bastan —en lugar de los seis de una pose general— porque la convención impone dos ligaduras sobre la colocación de los marcos; ese es también su coste: los marcos DH obedecen reglas y no siempre coinciden con los marcos «naturales» del robot.

**Advertencia de índices que ahorra un disgusto:** Corke numera articulaciones y parámetros desde 0, mientras los textos clásicos lo hacen desde 1 (Corke, 2023, p. 274). Aquí numeramos desde 1, como en la pizarra.

Para un brazo plano de revolución la tabla es trivial: `d_j = 0`, `alpha_j = 0`, `a_j` es la longitud del eslabón y `theta_j` es la variable articular."""))

C.append(code("""def A_dh(theta, d, a, alpha):
    \"\"\"Una fila DH estandar: Rz(theta)·Tz(d)·Tx(a)·Rx(alpha)  (Corke, 2023, p. 275).\"\"\"
    return SE3.Rz(theta) * SE3.Tz(d) * SE3.Tx(a) * SE3.Rx(alpha)

def fk_dh(tabla, q):
    \"\"\"FK por producto de filas DH. 'tabla' = lista de (d, a, alpha) para juntas de revolucion;
    la variable articular q_j se suma al theta_j de la fila.\"\"\"
    T = SE3()
    for (d, a, alpha), qj in zip(tabla, q):
        T = T * A_dh(qj, d, a, alpha)
    return T

# tabla DH del 2R plano: dos filas, todo cero salvo a
TABLA_2R = [(0.0, A1, 0.0), (0.0, A2, 0.0)]

print('Tabla DH del 2R plano')
print(f\"{'j':>2} {'theta_j':>10} {'d_j':>6} {'a_j':>6} {'alpha_j':>8}\")
for j, (d, a, al) in enumerate(TABLA_2R, start=1):
    print(f'{j:>2} {\"q\" + str(j):>10} {d:>6.2f} {a:>6.2f} {al:>8.2f}')

T_dh = fk_dh(TABLA_2R, q_ref)
print('\\nFK por DH en q = (30°, 40°):')
T_dh.printline()"""))

C.append(md("""Y ahora la comprobación que da sentido a toda la sesión: **la trigonometría de la sección 1 y la tabla DH describen el mismo robot**, así que tienen que dar exactamente la misma pose. Si no coinciden, el error está en la tabla, no en la geometría."""))

C.append(code("""def comparar(q, tabla, a_trig):
    \"\"\"Compara la FK trigonometrica y la FK por DH de un brazo plano.\"\"\"
    pose_mano, _ = fk_nr_mano(q, a=a_trig)
    T = fk_dh(tabla, q)
    x, y = T.t[0], T.t[1]
    th = np.arctan2(T.R[1, 0], T.R[0, 0])          # angulo de giro alrededor de z
    return pose_mano, np.array([x, y, th])

print(f\"{'q (grados)':>26} {'mano (x, y, th°)':>30} {'DH (x, y, th°)':>30}  igual?\")
for qq in [np.deg2rad([30, 40]), np.deg2rad([0, 0]), np.deg2rad([90, -45]),
           np.deg2rad([-120, 200])]:
    pm, pd = comparar(qq, TABLA_2R, [A1, A2])
    m = f'({pm[0]:7.4f}, {pm[1]:7.4f}, {np.rad2deg(pm[2]):7.1f})'
    d = f'({pd[0]:7.4f}, {pd[1]:7.4f}, {np.rad2deg(pd[2]):7.1f})'
    ok = np.allclose(pm[:2], pd[:2]) and np.isclose(np.cos(pm[2]), np.cos(pd[2])) \\
         and np.isclose(np.sin(pm[2]), np.sin(pd[2]))
    print(f'{str(np.rad2deg(qq).round(0)):>26} {m:>30} {d:>30}   {ok}')"""))

C.append(code("""# Lo mismo para el 3R: tabla de tres filas
TABLA_3R = [(0.0, A[0], 0.0), (0.0, A[1], 0.0), (0.0, A[2], 0.0)]

rng = np.random.default_rng(14)
errores = []
for _ in range(200):
    qq = rng.uniform(-np.pi, np.pi, 3)
    pm, pd = comparar(qq, TABLA_3R, A)
    dth = np.arctan2(np.sin(pm[2] - pd[2]), np.cos(pm[2] - pd[2]))   # diferencia envuelta
    errores.append(max(abs(pm[0]-pd[0]), abs(pm[1]-pd[1]), abs(dth)))
errores = np.array(errores)
print('3R plano, 200 configuraciones aleatorias:')
print(f'  error maximo entre trigonometria y DH: {errores.max():.3e}')
print('  Coinciden hasta el error de redondeo: son la MISMA cinematica escrita dos veces.')"""))

C.append(md("""### Ejercicio 1

Modifica la tabla DH del 2R para que el segundo eslabón, en vez de estar en el plano, esté girado 90 grados respecto del primero (`alpha_1 = pi/2`). Evalúa la FK en `q = (0, 0)` y en `q = (0, 90°)` y describe con palabras qué robot has construido. ¿Sigue siendo plano? ¿Cuál es ahora su espacio de trabajo?

### Ejercicio 2

Escribe la tabla DH de un brazo plano de **cuatro** eslabones con `a = (1.0, 0.8, 0.5, 0.3)` y comprueba contra `fk_nr_mano` en 500 configuraciones aleatorias. Después responde: ¿cuántas configuraciones distintas crees que alcanzan una misma pose (x, y, θ)? (Es la pregunta de S16, plantéala aquí.)"""))

C.append(code("""# Ejercicio 1
# TABLA_MOD = [(0.0, A1, np.pi/2), (0.0, A2, 0.0)]
# ...

# Ejercicio 2
# A4 = [1.0, 0.8, 0.5, 0.3]
# ..."""))

# ---------------- 4. PoE
C.append(md("""## 4. La tercera vía: el producto de exponenciales

Lynch y Park describen la misma cinemática sin ninguna tabla. La observación de partida: con el robot en su **configuración de casa** (todas las variables articulares a cero), cada articulación aplica al resto de la cadena un movimiento helicoidal exponencial alrededor de su propio eje. El resultado es la fórmula del producto de exponenciales:

`T(q) = e^([S1]·q1) · e^([S2]·q2) · ... · e^([Sn]·qn) · M`   (ecuación 4.14; Lynch y Park, 2017, p. 142)

Solo hacen falta tres ingredientes: la pose `M` del efector con el robot en casa, los ejes helicoidales `S_i` expresados en el marco fijo en esa configuración, y las variables articulares. La ventaja que Lynch y Park subrayan: «a diferencia de la representación D-H, no es necesario definir marcos de eslabón» (2017, p. 142); los ejes se leen directamente del dibujo del robot en casa.

Para el 2R plano: `M = Tx(a1 + a2)`; ambos ejes son giros alrededor de z, el primero por el origen y el segundo por el punto `(a1, 0)`. Un eje helicoidal se escribe `S = (v, w)` con `w` la dirección del eje y `v = −w × p`, donde `p` es un punto del eje. La conexión con S13 es directa: `e^([S]·q)` se calcula con la fórmula de Rodrigues extendida a SE(3) (Lynch y Park, 2017, p. 84)."""))

C.append(code("""def poe_2r(q, a1=A1, a2=A2):
    \"\"\"Producto de exponenciales del 2R plano (Lynch y Park, 2017, p. 142).\"\"\"
    M = SE3.Tx(a1 + a2)                       # pose del efector en la configuracion de casa
    w = np.array([0.0, 0.0, 1.0])             # ambos ejes son z
    S1 = np.hstack([-np.cross(w, [0.0, 0.0, 0.0]), w])   # eje por el origen
    S2 = np.hstack([-np.cross(w, [a1, 0.0, 0.0]), w])    # eje por el codo
    return SE3.Exp(S1 * q[0]) * SE3.Exp(S2 * q[1]) * M

T_poe = poe_2r(q_ref)
print('PoE en q = (30°, 40°):'); T_poe.printline()
print('\\n¿PoE == DH?         ', np.allclose(T_poe.A, fk_dh(TABLA_2R, q_ref).A))
pm, _ = fk_nr_mano(q_ref, a=[A1, A2])
print('¿PoE == trigonometría?', np.allclose(T_poe.t[:2], pm[:2]))

rng = np.random.default_rng(41)
err = max(np.abs(poe_2r(qq).A - fk_dh(TABLA_2R, qq).A).max()
          for qq in rng.uniform(-np.pi, np.pi, (100, 2)))
print(f'\\nError maximo PoE vs DH en 100 configuraciones aleatorias: {err:.3e}')"""))

C.append(md("""**Cuándo usar cada una.** La ETS y la trigonometría se leen directamente de la geometría; DH es el formato compacto para intercambiar modelos y el que documentan los controladores industriales; el PoE es el que se conecta mejor con el análisis de velocidad, porque las columnas del jacobiano de S17 serán precisamente estos mismos ejes helicoidales transformados a la configuración actual. Las tres describen el mismo objeto matemático y **deben dar exactamente la misma T(q)** — que es lo que acabamos de verificar tres veces.

### Ejercicio 3

Escribe el PoE del 3R plano (tres ejes z, situados en el origen, en `(a1, 0)` y en `(a1+a2, 0)`, con `M = Tx(a1+a2+a3)`) y compáralo con `fk_nr_mano` en 100 configuraciones aleatorias. Después dibuja los tres ejes helicoidales sobre la figura del brazo **en la configuración de casa** y explica por qué no hace falta ningún marco de eslabón."""))

C.append(code("""# Ejercicio 3
# def poe_3r(q, a=A):
#     M = SE3.Tx(a.sum())
#     ..."""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.** Con `alpha_1 = pi/2` el eje de la segunda articulación deja de ser paralelo al de la primera: pasa a ser perpendicular. El robot deja de ser plano y se convierte en el embrión de un brazo antropomórfico —cintura más hombro—, exactamente los dos primeros ejes de un 6R industrial. En `q = (0, 0)` la punta sigue en `(a1 + a2, 0, 0)` porque `Tx` va antes de `Rx` en la fila; en `q = (0, 90°)` la punta sube a `(a1, 0, a2)`. El espacio de trabajo ya no es una corona plana sino una superficie de revolución en 3D: la corona circular barrida alrededor del eje de la primera articulación. Este es el mecanismo por el que un solo parámetro `alpha` no nulo saca al robot del plano, y por eso `alpha` es el parámetro DH que más errores provoca.

**Ejercicio 2.** La tabla es `[(0, 1.0, 0), (0, 0.8, 0), (0, 0.5, 0), (0, 0.3, 0)]` y el error máximo frente a `fk_nr_mano` queda en el orden de 1e-15. Sobre la segunda pregunta: un brazo plano de cuatro eslabones tiene 4 gdl en un espacio de tareas de 3 dimensiones (x, y, θ), luego es **redundante** y para una pose alcanzable genérica hay una familia continua —una curva de un parámetro— de configuraciones que la producen, no un número finito. Ese es justamente el caso en el que la IK analítica de S16 no sirve y hay que ir a la numérica, que además permite optimizar un criterio secundario (Lynch y Park, 2017, p. 233).

**Ejercicio 3.**

```python
def poe_3r(q, a=A):
    M = SE3.Tx(a.sum())
    w = np.array([0., 0., 1.])
    puntos = [[0,0,0], [a[0],0,0], [a[0]+a[1],0,0]]
    T = SE3()
    for qj, p in zip(q, puntos):
        S = np.hstack([-np.cross(w, p), w])
        T = T * SE3.Exp(S * qj)
    return T * M
```

El error frente a `fk_nr_mano` vuelve a ser de redondeo. La razón de que no haga falta ningún marco de eslabón es que **cada eje helicoidal se describe en el marco fijo, en la configuración de casa**: no se propaga ninguna descripción a lo largo de la cadena, sino que se compone la acción de cada articulación sobre todo lo que cuelga de ella. Dibujar los tres ejes sobre el brazo estirado lo hace evidente: los ejes son tres puntos alineados sobre el eje x, con la misma dirección z. Ahí es donde el PoE gana en robustez de modelado — y donde se paga en aparato matemático."""))

C.append(md("""---

## Para llevarse de esta sesión

La cinemática directa **no tiene dificultad conceptual**: es una cadena de poses relativas, cada una función de una variable articular, multiplicadas en orden. Todo lo que parece complicado en esta sesión es notación, no geometría, y por eso la moraleja del ejercicio central es la que hay que repetir: trigonometría, DH y PoE dan la misma matriz hasta el error de redondeo, porque describen el mismo robot.

Lo que sí hay que llevarse es la lectura crítica de cada convención. DH es un formato de intercambio nacido en 1955 y sigue vivo porque cabe en cuatro columnas de una tabla; su precio son las reglas de asignación de marcos y las variantes incompatibles (estándar frente a modificada) que producen tablas que no se pueden mezclar. El PoE evita esas reglas y conecta de forma natural con la cinemática de velocidad, pero exige el aparato exponencial de S13.

Y una observación de la que tirará todo el bloque: al escribir la FK hemos construido, sin decirlo, el objeto que derivaremos en S17. `x = f(q)` es la función; su jacobiana `J(q) = df/dq` es el jacobiano, y sus columnas serán los ejes helicoidales del PoE vistos desde la configuración actual.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S14_Cinematica_Directa.ipynb', C)
print('escrito S14')
