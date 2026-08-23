from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('matplotlib','matplotlib'), ('spatialmath-python','spatialmath'),
       ('roboticstoolbox-python','roboticstoolbox')]
C = []

C.append(cabecera(
    "S18", "Singularidades y elipsoide de manipulabilidad", "4",
    "jueves 22 de octubre de 2026", "1 h",
    "Localiza las singularidades del 2R y del PUMA 560 siguiendo el determinante del jacobiano a lo largo de barridos articulares, dibuja el elipsoide de manipulabilidad en dos posturas —una sana y otra casi singular— y cuantifica la diferencia con las dos medidas escalares del bloque: la de Yoshikawa y el número de condición.",
    "Lynch y Park (2017), cap. 5 — elipsoide de manipulabilidad y su colapso a un segmento (p. 173), cociente de semiejes como número de condición (p. 174), definición de singularidad cinemática como pérdida de rango de J (p. 191), independencia de la elección de marcos (pp. 192-193) y catálogo de casos en robots 6R (pp. 193-195); Corke (2023), cap. 8 — hiperelipsoide en el espacio de velocidades de la tarea (pp. 316-317), elipsoides traslacional y rotacional por separado (pp. 317-318), medida de Yoshikawa y el método manipulability (p. 319), la Yoshikawa mide volumen y no isotropía (p. 328), singularidad de muñeca del PUMA con q4 = 0 (p. 282) y caída de manipulabilidad en trayectoria cartesiana (p. 289).",
    "los apuntes del bloque 4"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
import roboticstoolbox as rtb
from spatialmath import SE3

np.set_printoptions(precision=4, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.4)
plt.rcParams['axes.grid'] = True
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('roboticstoolbox', rtb.__version__, '- listo.')"""))

C.append(md("""> **Aviso para Colab.** `roboticstoolbox-python` **tarda varios minutos** en instalarse la primera vez; lanza la celda de instalación al abrir el cuaderno. Las secciones 1 y 2 solo necesitan numpy. Como en las sesiones anteriores, **nada de `robot.plot()` ni `robot.teach()`**: los elipsoides los dibujamos nosotros con matplotlib, que además obliga a entender de dónde salen."""))

# ---------------- 1. det J a lo largo de un barrido
C.append(md("""## 1. El determinante del jacobiano a lo largo de un barrido articular

Una singularidad cinemática es una postura en la que el efector pierde capacidad instantánea de movimiento: «el jacobiano permite identificar posturas en las que el efector del robot pierde la capacidad de moverse instantáneamente en una o más direcciones. Tal postura se denomina singularidad cinemática, o simplemente singularidad. **Matemáticamente, una postura singular es aquella en la que el jacobiano J(q) deja de tener rango máximo**» (Lynch y Park, 2017, p. 191).

Para un robot con J cuadrado, «rango no máximo» equivale a determinante nulo. La forma más directa de localizar las singularidades del 2R es barrer el espacio articular y mirar `det J`.

Para el 2R plano el determinante tiene una forma cerrada preciosa: `det J = a1·a2·sin(q2)`. **No depende de q1 en absoluto** —girar el hombro reorienta el brazo entero pero no cambia su geometría interna— y se anula en `q2 = 0` (brazo estirado) y `q2 = ±180°` (brazo replegado sobre sí mismo)."""))

C.append(code("""A1, A2 = 1.0, 0.8

def jac_2r(q, a1=A1, a2=A2):
    q1, q2 = q
    s1, c1 = np.sin(q1), np.cos(q1)
    s12, c12 = np.sin(q1+q2), np.cos(q1+q2)
    return np.array([[-a1*s1 - a2*s12, -a2*s12],
                     [ a1*c1 + a2*c12,  a2*c12]])

q2s = np.linspace(-np.pi, np.pi, 721)
dets = np.array([np.linalg.det(jac_2r([0.4, q2])) for q2 in q2s])
teorico = A1 * A2 * np.sin(q2s)
print('¿det J == a1·a2·sin(q2)?', np.allclose(dets, teorico))

# ¿depende de q1?
for q1 in [0.0, 1.0, 2.5, -0.7]:
    d = np.linalg.det(jac_2r([q1, 0.9]))
    print(f'  q1 = {q1:5.2f}, q2 = 0.90  ->  det J = {d:.6f}')
print('El determinante no depende de q1: la singularidad es una propiedad de la FORMA del brazo.')"""))

C.append(code("""fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 3.6))

a1.plot(np.rad2deg(q2s), dets, color=IQS_AZUL, lw=2)
a1.axhline(0, color='crimson', lw=1)
for q_sing in [-180, 0, 180]:
    a1.axvline(q_sing, color='crimson', ls=':', lw=1.4)
a1.set_xlabel('q2 (grados)'); a1.set_ylabel('det J')
a1.set_title('2R plano: det J = a1·a2·sin(q2)', fontsize=10)

conds = np.array([np.linalg.cond(jac_2r([0.4, q2])) for q2 in q2s])
a2.semilogy(np.rad2deg(q2s), conds, color=IQS_VERDE, lw=2)
for q_sing in [-180, 0, 180]:
    a2.axvline(q_sing, color='crimson', ls=':', lw=1.4)
a2.set_xlabel('q2 (grados)'); a2.set_ylabel('cond(J)  (escala log)')
a2.set_title('El número de condición explota en las singularidades', fontsize=10)
plt.tight_layout(); plt.show()

print('Fuera de las singularidades el numero de condicion es de unas pocas unidades;')
print(f'a 1 grado del brazo estirado ya vale {np.linalg.cond(jac_2r([0.4, np.deg2rad(1)])):.0f}.')"""))

C.append(md("""**El punto que hay que dejar claro.** El determinante se anula *exactamente* en la singularidad, pero eso no es lo que importa en la práctica: nadie manda un robot exactamente a `q2 = 0`. Lo que importa es la **vecindad**, donde el número de condición ya vale cientos y el control de velocidad resuelta de S17 demanda velocidades articulares desmesuradas. Por eso los controladores industriales reducen velocidad o rechazan la trayectoria mucho antes de llegar al punto singular.

Y una propiedad estructural que conviene subrayar: la definición «es independiente de la elección de jacobiano en el espacio o en el cuerpo» y las singularidades «son también independientes de la elección de marco fijo y de marco del efector» (Lynch y Park, 2017, pp. 192-193). **Cambiar el marco equivale a recolocar el robot, y recolocar un robot no puede cambiar sus singularidades.** Lo comprobamos numéricamente en S17 con `jacob0` y `jacobe`; aquí lo hacemos con el PUMA."""))

C.append(code("""puma = rtb.models.DH.Puma560()

for etq, q in [('qn', puma.qn), ('qr', puma.qr),
               ('muñeca singular (q5=0)', np.array([0, 0.5, -1.0, 0.7, 0.0, 0.3]))]:
    d0 = np.linalg.det(puma.jacob0(q))
    de = np.linalg.det(puma.jacobe(q))
    print(f'{etq:>24}:  det jacob0 = {d0:11.6f}   det jacobe = {de:11.6f}   '
          f'iguales? {np.isclose(d0, de)}')

print('\\nRango del jacobiano en la muñeca singular:',
      np.linalg.matrix_rank(puma.jacob0(np.array([0, 0.5, -1.0, 0.7, 0.0, 0.3])), tol=1e-9),
      'de 6')
print('-> ha perdido una direccion: es exactamente la singularidad de muñeca de S16')
print('   (Corke, 2023, p. 282).')"""))

C.append(md("""### Ejercicio 1

Barre `q5` del PUMA de −100 a 100 grados (sus límites) manteniendo el resto en `qn`, y dibuja `|det(puma.jacob0(q))|` en escala logarítmica. ¿Dónde está el mínimo y cuánto vale el determinante allí? Comprueba el rango de J en ese punto con `np.linalg.matrix_rank`."""))

C.append(code("""# Ejercicio 1
q5s = np.deg2rad(np.linspace(-100, 100, 401))
# ..."""))

# ---------------- 2. El elipsoide de manipulabilidad
C.append(md("""## 2. El elipsoide de manipulabilidad

Para cuantificar la proximidad a una singularidad se estudia **cómo J deforma las velocidades**. Considérese el conjunto de velocidades articulares de esfuerzo unidad, `q̇ᵀq̇ = 1`: su imagen a través del jacobiano es un elipsoide en el espacio de velocidades del efector, «el elipsoide de manipulabilidad» (Lynch y Park, 2017, p. 173). En la formulación de Corke, los puntos que cumplen `νᵀ·(J·Jᵀ)⁻¹·ν = 1` forman «un hiperelipsoide en el espacio de velocidades de la tarea», idealmente próximo a esférico —isótropo— y con radios del mismo orden (Corke, 2023, pp. 316-317).

La construcción se hace con la descomposición en valores singulares `J = U·Σ·Vᵀ`: **las direcciones principales del elipsoide son las columnas de U y los semiejes son los valores singulares**. Interpretación directa: el semieje mayor es la dirección en la que el efector se mueve con más facilidad; el menor, la dirección difícil.

«Según la configuración del manipulador se aproxima a una singularidad, el elipsoide colapsa a un segmento» (Lynch y Park, 2017, p. 173)."""))

C.append(code("""def elipse_manipulabilidad(J, n=200):
    \"\"\"Contorno del elipsoide de manipulabilidad 2D: imagen del circulo unidad de q_dot.\"\"\"
    th = np.linspace(0, 2*np.pi, n)
    return J @ np.vstack([np.cos(th), np.sin(th)])

def puntos_2r(q, a1=A1, a2=A2):
    q1, q2 = q
    p0 = np.zeros(2)
    p1 = p0 + a1*np.array([np.cos(q1), np.sin(q1)])
    p2 = p1 + a2*np.array([np.cos(q1+q2), np.sin(q1+q2)])
    return np.vstack([p0, p1, p2])

posturas = [(np.deg2rad([25, 95]), 'postura sana'),
            (np.deg2rad([25, 8]),  'casi singular')]

fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6))
for ax, (q, titulo) in zip(axes, posturas):
    J = jac_2r(q)
    U, S, Vt = np.linalg.svd(J)
    P = puntos_2r(q)
    E = elipse_manipulabilidad(J) * 0.35 + P[-1][:, None]     # escalado para que quepa

    ax.plot(P[:, 0], P[:, 1], 'o-', lw=3, ms=7, color='black')
    ax.plot(E[0], E[1], color=IQS_AZUL, lw=2)
    ax.fill(E[0], E[1], color=IQS_AZUL, alpha=0.12)
    for k in range(2):
        v = U[:, k] * S[k] * 0.35
        ax.arrow(P[-1, 0], P[-1, 1], v[0], v[1], head_width=0.05,
                 color=IQS_VERDE if k == 0 else 'crimson',
                 length_includes_head=True, lw=2)
    m = np.sqrt(np.linalg.det(J @ J.T))
    ax.set_title(f'{titulo}\\nσ = {S.round(3)}   cond = {S[0]/S[1]:.1f}   '
                 f'Yoshikawa m = {m:.4f}', fontsize=9)
    ax.set_aspect('equal'); ax.set_xlim(-0.6, 2.3); ax.set_ylim(-0.8, 1.9)
plt.tight_layout(); plt.show()

print('En verde el semieje mayor (direccion facil), en rojo el menor (direccion dificil).')"""))

C.append(md("""En 3D la construcción es la misma: la imagen de la esfera unidad de velocidades articulares. Para robots espaciales el elipsoide completo es 6D y no visualizable, así que se dibujan por separado el **traslacional** y el **rotacional** extrayendo los bloques correspondientes de J (Corke, 2023, pp. 317-318).

Dibujamos el elipsoide traslacional del PUMA 560 en dos posturas: la nominal y una casi estirada."""))

C.append(code("""def elipsoide(J3, n=40):
    \"\"\"Malla del elipsoide imagen de la esfera unidad a traves de un bloque 3xn de J.\"\"\"
    u = np.linspace(0, 2*np.pi, 2*n); v = np.linspace(0, np.pi, n)
    esfera = np.array([np.outer(np.cos(u), np.sin(v)).ravel(),
                       np.outer(np.sin(u), np.sin(v)).ravel(),
                       np.outer(np.ones_like(u), np.cos(v)).ravel()])
    # imagen de la esfera unidad de q_dot: basta la SVD del bloque traslacional
    U, S, _ = np.linalg.svd(J3, full_matrices=False)
    E = U @ np.diag(S) @ esfera
    return [E[k].reshape(2*n, n) for k in range(3)]

q_est = np.array([0.0, -0.2, -0.05, 0.0, 0.1, 0.0])       # brazo casi estirado
fig = plt.figure(figsize=(11, 4.4))
for k, (etq, q) in enumerate([('qn (nominal)', puma.qn), ('casi estirado', q_est)]):
    J = puma.jacob0(q)
    X, Y, Z = elipsoide(J[:3, :])
    ax = fig.add_subplot(1, 2, k+1, projection='3d')
    ax.plot_surface(X, Y, Z, color=IQS_AZUL, alpha=0.28, linewidth=0)
    lim = 1.6
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-lim, lim)
    S = np.linalg.svd(J[:3, :], compute_uv=False)
    ax.set_title(f'{etq}\\nsemiejes = {S.round(3)}   cond = {S[0]/S[2]:.1f}', fontsize=9)
    ax.set_xlabel('vx'); ax.set_ylabel('vy'); ax.set_zlabel('vz')
fig.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.02, wspace=0.1)
plt.show()"""))

# ---------------- 3. Medidas escalares
C.append(md("""## 3. Las dos medidas escalares: Yoshikawa y número de condición

De la forma del elipsoide se derivan dos números.

**El número de condición geométrico**, cociente entre los semiejes mayor y menor: cuanto más próximo a 1, más isótropa la postura (Lynch y Park, 2017, p. 174). Mide **forma**.

**La medida de Yoshikawa**, `m(q) = sqrt(det(J(q)·Jᵀ(q)))`, proporcional al volumen del elipsoide y calculada en la toolbox por el método `manipulability` (Corke, 2023, p. 319). Mide **tamaño**. Se anula exactamente en las singularidades, lo que la convierte en un buen indicador para monitorizar trayectorias.

**Aviso de interpretación imprescindible:** «la medida de Yoshikawa es el volumen del elipsoide de velocidad» pero **no mide isotropía**, de modo que un elipsoide muy alargado puede tener buen volumen (Corke, 2023, p. 328). Hay que usar las dos."""))

C.append(code("""def yoshikawa(J):
    return float(np.sqrt(max(0.0, np.linalg.det(J @ J.T))))

# comprobamos que nuestra formula coincide con el metodo de la toolbox
for etq, q in [('qz', puma.qz), ('qn', puma.qn), ('qr', puma.qr), ('casi estirado', q_est)]:
    J = puma.jacob0(q)
    print(f'{etq:>15}:  m a mano = {yoshikawa(J):.6f}   '
          f'puma.manipulability = {puma.manipulability(q):.6f}   '
          f'cond = {np.linalg.cond(J):10.3e}')
print('\\nOjo con qz y qr: m = 0 exactamente. Las dos configuraciones con nombre mas')
print('usadas del PUMA son SINGULARES, y por eso su numero de condicion es astronomico.')

print('\\n(m es tambien |det J| cuando J es cuadrado:',
      round(abs(np.linalg.det(puma.jacob0(puma.qn))), 6), ')')"""))

C.append(md("""Ahora el contraejemplo que hace concreto el aviso de Corke: **dos posturas con volúmenes parecidos y formas radicalmente distintas**. Lo buscamos por fuerza bruta en el 2R, donde todo se puede dibujar."""))

C.append(code("""rng = np.random.default_rng(18)
muestras = []
for _ in range(4000):
    q = np.array([rng.uniform(-np.pi, np.pi), rng.uniform(-np.pi, np.pi)])
    J = jac_2r(q)
    muestras.append((q, yoshikawa(J), np.linalg.cond(J)))

m_vals = np.array([s[1] for s in muestras])
c_vals = np.array([s[2] for s in muestras])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 3.6))
ax1.scatter(m_vals, c_vals, s=6, color=IQS_AZUL, alpha=0.35)
ax1.set_yscale('log'); ax1.set_xlabel('Yoshikawa m (volumen)')
ax1.set_ylabel('número de condición (forma)')
ax1.set_title('Volumen y forma no son la misma cosa', fontsize=10)

# mapa de m(q) sobre el espacio articular del 2R
Q1, Q2 = np.meshgrid(np.linspace(-np.pi, np.pi, 160), np.linspace(-np.pi, np.pi, 160))
M = A1 * A2 * np.abs(np.sin(Q2))
c = ax2.contourf(np.rad2deg(Q1), np.rad2deg(Q2), M, levels=18, cmap='viridis')
ax2.contour(np.rad2deg(Q1), np.rad2deg(Q2), M, levels=[1e-3], colors='crimson')
ax2.set_xlabel('q1 (grados)'); ax2.set_ylabel('q2 (grados)')
ax2.set_title('m(q) del 2R: las bandas rojas son singularidades', fontsize=10)
plt.colorbar(c, ax=ax2)
plt.tight_layout(); plt.show()

print(f'Rango de m: {m_vals.min():.4f} a {m_vals.max():.4f}')
print(f'La postura mas isotropa encontrada tiene cond = {c_vals.min():.3f} '
      f'y m = {m_vals[c_vals.argmin()]:.4f}')"""))

C.append(md("""### Ejercicio 2

En el mapa de `m(q)` del 2R, las singularidades son las bandas horizontales `q2 = 0` y `q2 = ±180°`. Encuentra numéricamente el `q2` **más isótropo** (el de menor número de condición) barriendo `q2` en (0, 180°). ¿Sale `q2 = 90°`, como sugiere la intuición del «brazo en L»? Repite con `a1 = 1.0, a2 = 1.0` y con `a1 = 1.0, a2 = 0.3`, y explica qué cambia.

### Ejercicio 3

Calcula la medida de Yoshikawa del PUMA 560 sobre 2000 configuraciones aleatorias dentro de sus límites articulares y dibuja el histograma. ¿Qué fracción de configuraciones tiene `m` por debajo del 10 % del máximo encontrado? Ese porcentaje es una estimación cruda de «cuánto del espacio articular es zona mala»."""))

C.append(code("""# Ejercicio 2
# def cond_2r(q2, a1=A1, a2=A2): ...

# Ejercicio 3
# qlim = puma.qlim
# ..."""))

# ---------------- 4. Barrido en el PUMA
C.append(md("""## 4. Manipulabilidad a lo largo de un camino del PUMA

El uso operativo de `m(q)` es monitorizar una trayectoria y ver si pasa cerca de una zona mala. En el ejemplo del libro, una trayectoria cartesiana del PUMA resuelta con IK analítica ve caer su manipulabilidad casi a cero por la singularidad de muñeca (Corke, 2023, p. 289); aquí lo reproducimos con un barrido articular sencillo, que es lo que retomaremos en S19 con trayectorias de verdad."""))

C.append(code("""# camino articular: interpolamos linealmente entre qn y una postura casi estirada
s = np.linspace(0, 1, 200)
camino = np.array([(1-si)*puma.qn + si*q_est for si in s])

m = np.array([puma.manipulability(q) for q in camino])
cond = np.array([np.linalg.cond(puma.jacob0(q)) for q in camino])
m_trans = np.array([yoshikawa(puma.jacob0(q)[:3, :]) for q in camino])

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 3.6))
a1.plot(s, m, color=IQS_AZUL, lw=2, label='m completa (6D)')
a1.plot(s, m_trans, color=IQS_VERDE, lw=2, ls='--', label='m traslacional (3D)')
a1.set_xlabel('s (parámetro del camino)'); a1.set_ylabel('Yoshikawa m')
a1.legend(fontsize=8); a1.set_title('Manipulabilidad a lo largo del camino', fontsize=10)

a2.semilogy(s, cond, color='crimson', lw=2)
a2.set_xlabel('s'); a2.set_ylabel('cond(J)'); a2.set_title('Número de condición', fontsize=10)
plt.tight_layout(); plt.show()

j = int(m.argmin())
print(f'Minimo de m en s = {s[j]:.3f}:  m = {m[j]:.3e}   cond = {cond[j]:.3e}')
print(f'Maximo de m: {m.max():.5f} en s = {s[int(m.argmax())]:.3f}')
print('\\nLa manipulabilidad no baja: se ANULA. Este camino, que parece inocente porque')
print('es una recta en el espacio articular entre dos posturas validas, ATRAVIESA una')
print('singularidad. Nadie lo habria adivinado mirando los dos extremos.')"""))

C.append(md("""**El mensaje de cierre para la clase.** La singularidad no es una avería sino una **propiedad geométrica anticipable**: está escrita en la tabla DH del robot antes de que nadie lo encienda. Y la primera herramienta para evitarla no es el algoritmo de control, es el **diseño de la tarea**: dónde se coloca la pieza respecto del robot, con qué orientación se presenta la herramienta, por qué zona del espacio de trabajo se pide que pase la trayectoria.

Un robot bien colocado no necesita ninguna estrategia sofisticada de evitación de singularidades. Uno mal colocado no hay estrategia que lo salve."""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.** El mínimo está en `q5 = 0`, donde `|det J|` cae varios órdenes de magnitud —numéricamente queda en el nivel del redondeo, del orden de 1e-17— y `np.linalg.matrix_rank(J, tol=1e-9)` devuelve **5** en vez de 6. Esa es exactamente la definición de singularidad de Lynch y Park (2017, p. 191): pérdida de rango. Geométricamente, con `q5 = 0` los ejes de las articulaciones 4 y 6 quedan colineales y sus columnas del jacobiano son idénticas: dos motores haciendo lo mismo, una dirección de movimiento perdida. Es la misma postura que en S16 daba infinitas soluciones de IK con solo `q4 + q6` determinada.

**Ejercicio 2.** No, no sale 90 grados, y esa es la gracia del ejercicio. Barriendo `q2` con `a1 = 1.0, a2 = 0.8` el mínimo del número de condición está en `q2 ≈ 135°` y vale **1.19**; con `a1 = a2 = 1.0` el mínimo está en `q2 ≈ 132°` y vale **1.618**; con `a1 = 1.0, a2 = 0.3` el mínimo se desplaza a `q2 ≈ 120°` y sube a **3.06**.

Tres lecturas. Primera: la intuición geométrica del «brazo en L» es falsa — el óptimo de isotropía no coincide con el óptimo del determinante (que sí está en 90 grados, porque `det J = a1·a2·sin(q2)`). Volumen y forma tienen óptimos distintos, que es exactamente el aviso de Corke (2023, p. 328) hecho número. Segunda: ni siquiera con eslabones iguales el 2R llega a ser perfectamente isótropo; su mejor número de condición es 1.618, no 1. Tercera y más útil para el diseño: con `a2 = 0.3` el mínimo alcanzable ya es 3.06, es decir, el robot **nunca** es cómodo en ninguna postura, porque la columna 2 de J tiene módulo `a2` siempre (lo vimos en S17) y un segundo eslabón corto tiene poca autoridad sobre la punta. La isotropía del elipsoide es en buena medida una decisión de **proporciones de eslabones**, tomada en la mesa de dibujo y no corregible por software.

**Ejercicio 3.**

```python
qlim = puma.qlim
rng = np.random.default_rng(0)
Q = rng.uniform(qlim[0], qlim[1], size=(2000, 6))
ms = np.array([puma.manipulability(q) for q in Q])
frac = (ms < 0.1*ms.max()).mean()
```

La fracción sale en el entorno del 40-50 %: **casi la mitad del espacio articular del PUMA es zona de manipulabilidad pobre**. El histograma es fuertemente asimétrico, con una acumulación grande cerca de cero y una cola larga. Esto sorprende a los estudiantes y conviene explotarlo: un robot industrial no es «igual de bueno» en todo su volumen de trabajo, ni de lejos. El volumen de trabajo de catálogo dice dónde *llega* la punta; no dice dónde puede el robot moverse con soltura, y esa es una información que el fabricante no publica y que el integrador tiene que calcularse."""))

C.append(md("""---

## Para llevarse de esta sesión

Una singularidad es **pérdida de rango del jacobiano**, y punto. Todo lo demás —el determinante que se anula, el número de condición que explota, el elipsoide que colapsa a un segmento, las soluciones infinitas de la IK, las velocidades articulares que se disparan— son manifestaciones del mismo hecho. Que sea independiente del marco elegido es lo que la convierte en una propiedad del robot y no de nuestra descripción de él.

Las dos medidas escalares no son intercambiables y hay que usarlas juntas: **Yoshikawa mide volumen, el número de condición mide forma**. Un elipsoide grande y muy alargado tiene buena `m` y es una postura pésima si la tarea necesita moverse en la dirección estrecha. El propio Corke lo advierte explícitamente (2023, p. 328) y es el error de interpretación más común del tema.

La lectura de ingeniería que hay que llevarse: la manipulabilidad no es solo un diagnóstico, es un **criterio de diseño de célula**. Antes de programar la trayectoria conviene mapear `m(q)` sobre la zona de trabajo prevista y colocar la pieza donde el robot está cómodo. En S19 vamos a ver la otra cara de la moneda: esas mismas posturas singulares, malas para mover, son excelentes para **sostener**.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S18_Singularidades_Manipulabilidad.ipynb', C)
print('escrito S18')
