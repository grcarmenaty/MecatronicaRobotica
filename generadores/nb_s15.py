from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('matplotlib','matplotlib'), ('spatialmath-python','spatialmath'),
       ('roboticstoolbox-python','roboticstoolbox')]
C = []

C.append(cabecera(
    "S15", "Taller: cinemática directa de un 6R con la Robotics Toolbox", "4",
    "jueves 15 de octubre de 2026", "1 h",
    "Pasa del robot de pizarra a modelos completos de robots comerciales de seis ejes: carga el PUMA 560 y el ABB IRB 140 incluidos en la Robotics Toolbox for Python, evalúa fkine sobre las configuraciones con nombre, lee la pose con printline en varios formatos, reconstruye la cadena eslabón a eslabón y compara configuraciones.",
    "Corke (2023), cap. 7 — modelos incluidos y Puma560 (p. 281), IRB140 como «modelo Denavit-Hartenberg de un robot industrial popular» (p. 277), configuraciones articulares con nombre qr y qz (p. 265), fkine e printline con t = 0.005, 0, 0.332 y rpy = 0, −90, −90 grados (p. 278), la tabla DH del PUMA 560 (p. 274) y su secuencia elemental (p. 275), el efector de los modelos DH en el centro de la muñeca y la transformación de herramienta (p. 267), el PUMA 560 como arquetipo (p. 261), muñeca esférica ZYZ del 6R (p. 260) y el brazo articulado de 6 ejes como estándar industrial (p. 254).",
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

C.append(md("""> **Aviso para Colab.** La instalación de `roboticstoolbox-python` arrastra bastantes dependencias y **tarda varios minutos** la primera vez. Conviene lanzar la celda de instalación nada más abrir el cuaderno y explicar la teoría mientras corre. Si Colab pide reiniciar el entorno de ejecución tras la instalación, hazlo y vuelve a ejecutar la celda: la segunda vez detecta que ya está todo y termina en un segundo.
>
> **Aviso de método.** En este taller **no** usamos `robot.plot()` ni `robot.teach()`: abren ventanas interactivas que en Colab fallan o se quedan colgadas. Todo lo hacemos con salidas numéricas y con figuras propias de matplotlib, que además obligan a entender qué se está dibujando."""))

# ---------------- 1. Cargar modelos
C.append(md("""## 1. Dos robots de catálogo en dos líneas

La Robotics Toolbox encapsula todo el aparato de S13 y S14 en objetos robot con métodos uniformes. Se puede construir un modelo a mano —definiendo la ETS o los eslabones DH— o instanciarlo desde la colección incluida: `rtb.models.DH.Puma560()` carga el PUMA 560 clásico (Corke, 2023, p. 281) y `rtb.models.DH.IRB140()` «un modelo Denavit-Hartenberg de un robot industrial popular» de ABB (Corke, 2023, p. 277).

El PUMA 560 no es un capricho nostálgico: «fue el primer robot industrial moderno, con diseño antropomórfico, motores eléctricos y muñeca esférica: el arquetipo de todo lo que siguió» (Corke, 2023, p. 261). Es exactamente la arquitectura del brazo articulado de seis ejes que B2 presentó como estándar industrial (Corke, 2023, p. 254) y la del robot ABB del aula-taller."""))

C.append(code("""puma = rtb.models.DH.Puma560()
irb = rtb.models.DH.IRB140()

print(puma)"""))

C.append(md("""Esa tabla es literalmente la Tabla 7.1 del libro (Corke, 2023, p. 274) y cada fila es la secuencia elemental `Rz(theta_j)·Tz(d_j)·Tx(a_j)·Rx(alpha_j)` que escribimos a mano en S14 (ecuación 7.4; Corke, 2023, p. 275). Merece la pena leerla en voz alta en clase: los `alpha` de ±90 grados son los que sacan al robot del plano, y los tres ceros finales en `a` y `d` de las filas 5 y 6 son la firma de la **muñeca esférica** — tres ejes que se cortan en un punto.

Lo comprobamos numéricamente: si los tres últimos ejes concurren, el centro de muñeca no se mueve por más que giren `q4`, `q5` y `q6`."""))

C.append(code("""print(irb)"""))

C.append(code("""def origenes(robot, q):
    \"\"\"Posiciones de los origenes de todos los marcos de la cadena, base incluida.\"\"\"
    return np.array([T.t for T in robot.fkine_all(q)])

# el centro de muneca es el origen del marco 4 (indice 4 contando la base como 0)
rng = np.random.default_rng(15)
q_base = puma.qn.copy()
centros = []
for _ in range(6):
    q = q_base.copy()
    q[3:] = rng.uniform(-2, 2, 3)          # movemos SOLO la muneca
    centros.append(origenes(puma, q)[4])
centros = np.array(centros)

print('Centro de muneca con q4, q5, q6 aleatorios (q1-q3 fijos):')
print(centros.round(6))
print('\\nDispersion maxima:', np.abs(centros - centros[0]).max().round(12))
print('-> los tres ultimos ejes CONCURREN: eso es la muñeca esferica (Corke, 2023, p. 260).')"""))

# ---------------- 2. Configuraciones con nombre y fkine
C.append(md("""## 2. Configuraciones con nombre, `fkine` y `printline`

Los modelos definen propiedades como `qz` (todo a cero) o `qr` (reposo), que «son simplemente configuraciones articulares con nombre» y a las que pueden añadirse otras propias (Corke, 2023, p. 265). Usarlas hace los ejercicios reproducibles: `puma.qn` es la configuración nominal que el libro utiliza en casi todos los ejemplos del capítulo.

`fkine` devuelve una `SE3` y `printline` la resume en una línea, con el formato de orientación que se le pida. La referencia de contraste es la del libro: `irb140.fkine(irb140.qr).printline('rpy/xyz')` da `t = 0.005, 0, 0.332` con `rpy = 0, −90, −90` grados (Corke, 2023, p. 278)."""))

C.append(code("""print('Configuraciones con nombre del PUMA 560:', list(puma.configs.keys()))
print('Configuraciones con nombre del IRB 140 :', list(irb.configs.keys()))

print('\\n--- IRB 140 en qr, la referencia del libro ---')
irb.fkine(irb.qr).printline('rpy/xyz')
print('Libro (Corke, 2023, p. 278):  t = 0.005, 0, 0.332;  rpy/xyz = 0°, -90°, -90°')"""))

C.append(code("""T_n = puma.fkine(puma.qn)
print('PUMA 560 en qn, la misma pose leida de cuatro maneras:\\n')
for fmt in ['rpy/xyz', 'rpy/zyx', 'eul', 'angvec']:
    print(f'  {fmt:>8} : ', end='')
    T_n.printline(fmt)

print('\\nY la matriz homogenea completa, que es lo unico sin ambiguedad:')
print(T_n)"""))

C.append(md("""**Punto para insistir en clase.** Las cuatro líneas de arriba describen **la misma pose**. Los números de orientación cambian por completo según la convención elegida; la matriz 4x4 no. Es la advertencia de S13 aplicada a una herramienta real: ante cualquier controlador o fichero de calibración, la primera pregunta es siempre qué secuencia de ángulos y en qué unidades.

### Ejercicio 1

Añade al PUMA una configuración propia llamada `q_trabajo` con `q = (0°, −45°, 90°, 0°, 45°, 0°)` (basta con guardarla en una variable) y compara su pose con la de `qn`: ¿a qué distancia están las dos puntas y cuánto han girado una respecto de la otra? Pista: la distancia es `np.linalg.norm(T1.t - T2.t)` y el ángulo se saca de `(T1.inv() * T2).angvec()`."""))

C.append(code("""# Ejercicio 1
q_trabajo = np.deg2rad([0, -45, 90, 0, 45, 0])
# ..."""))

# ---------------- 3. La cadena eslabon a eslabon
C.append(md("""## 3. La cadena, eslabón a eslabón

`fkine` es una caja negra de una línea; conviene abrirla al menos una vez. La cinemática directa no es más que el producto de las matrices `A_j` de cada fila DH, que es exactamente lo que hicimos a mano en S14. La toolbox expone cada una con `robot.links[j].A(q_j)`.

Reconstruimos el producto a mano y comparamos con `fkine`."""))

C.append(code("""q = puma.qn

T_acum = SE3()
print('Producto acumulado de las filas DH:')
for j, eslabon in enumerate(puma.links):
    T_acum = T_acum * eslabon.A(q[j])
    p = T_acum.t
    print(f'  tras la articulacion {j+1}:  origen en ({p[0]:7.4f}, {p[1]:7.4f}, {p[2]:7.4f})')

print('\\n¿El producto a mano coincide con puma.fkine(q)?',
      np.allclose(T_acum.A, puma.fkine(q).A))
print('Error maximo:', np.abs(T_acum.A - puma.fkine(q).A).max())"""))

C.append(md("""Con los orígenes de todos los marcos ya podemos dibujar el robot nosotros mismos —una figura de palotes en 3D— sin tocar `robot.plot()`. Es lo que hace internamente cualquier visualizador: unir los orígenes consecutivos de la cadena."""))

C.append(code("""def dibujar_robot(ax, robot, q, color, etq):
    P = origenes(robot, q)
    ax.plot(P[:, 0], P[:, 1], P[:, 2], 'o-', lw=2.5, ms=5, color=color, label=etq)
    ax.scatter(*P[-1], s=70, color=color, marker='*')

fig = plt.figure(figsize=(11, 4.2))
for k, (nombre, q_i) in enumerate([('qz', puma.qz), ('qr', puma.qr), ('qn', puma.qn)]):
    ax = fig.add_subplot(1, 3, k+1, projection='3d')
    dibujar_robot(ax, puma, q_i, IQS_AZUL, nombre)
    ax.set_xlim(-0.8, 0.8); ax.set_ylim(-0.8, 0.8); ax.set_zlim(0, 1.4)
    ax.set_title(f'PUMA 560 en {nombre}', fontsize=10)
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
plt.tight_layout(); plt.show()"""))

C.append(md("""**La trampa clásica de los modelos DH.** El «efector» de estos modelos suele ser el centro de la muñeca esférica, que «está físicamente dentro del robot»; la pose de la punta real de la herramienta exige componer la transformación de herramienta correspondiente (Corke, 2023, p. 267). Cuando en el laboratorio la toolbox y el controlador «no coincidan», la causa casi siempre está ahí o en la convención de ángulos.

Lo montamos: una pinza de 18 cm de largo montada en la brida."""))

C.append(code("""print('Herramienta por defecto del modelo (identidad):')
print(puma.tool)

puma.tool = SE3.Tz(0.18)          # pinza de 18 cm a lo largo del eje z de la brida
T_con = puma.fkine(puma.qn)
puma.tool = SE3()                 # la dejamos como estaba
T_sin = puma.fkine(puma.qn)

print('Sin herramienta :', T_sin.t.round(4))
print('Con herramienta :', T_con.t.round(4))
print('Desplazamiento  :', round(float(np.linalg.norm(T_con.t - T_sin.t)), 4), 'm')
print('\\n18 cm de discrepancia son 18 cm de pieza mal cogida: por eso la transformacion')
print('de herramienta es la primera sospechosa cuando modelo y controlador no cuadran.')"""))

# ---------------- 4. Comparacion de configuraciones
C.append(md("""## 4. Comparar configuraciones: dónde está y hacia dónde mira

El ejercicio central del taller es sistemático: barrer un conjunto de configuraciones, calcular la pose de cada una y **leerla**. Con una tabla y dos gráficas se ve mucho más de lo que se ve con un visualizador interactivo, porque obliga a mirar números.

Comparamos las cuatro configuraciones con nombre del PUMA 560 y les añadimos dos propias."""))

C.append(code("""casos = {'qz  (cero)': puma.qz,
         'qr  (reposo)': puma.qr,
         'qn  (nominal)': puma.qn,
         'qs  (estirado)': puma.qs,
         'trabajo': np.deg2rad([0, -45, 90, 0, 45, 0]),
         'lateral': np.deg2rad([90, -30, 60, 0, 60, 0])}

print(f\"{'configuracion':>16} {'x':>8} {'y':>8} {'z':>8} {'|p|':>8} "
      f\"{'roll':>7} {'pitch':>7} {'yaw':>7}\")
poses = {}
for nombre, q_i in casos.items():
    T = puma.fkine(q_i)
    poses[nombre] = T
    r, p_, y_ = np.rad2deg(T.rpy(order='xyz'))
    t = T.t
    print(f'{nombre:>16} {t[0]:>8.4f} {t[1]:>8.4f} {t[2]:>8.4f} '
          f'{np.linalg.norm(t):>8.4f} {r:>7.1f} {p_:>7.1f} {y_:>7.1f}')

print(f'\\nAlcance maximo del modelo: {puma.reach:.4f} m')"""))

C.append(code("""# Distancias entre puntas y giro relativo entre orientaciones
nombres = list(casos.keys())
n = len(nombres)
D = np.zeros((n, n)); Ang = np.zeros((n, n))
for i, ni in enumerate(nombres):
    for j, nj in enumerate(nombres):
        D[i, j] = np.linalg.norm(poses[ni].t - poses[nj].t)
        ang, _ = (poses[ni].inv() * poses[nj]).angvec()
        Ang[i, j] = np.rad2deg(abs(ang))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4))
for ax, M, titulo, cmap in [(a1, D, 'distancia entre puntas (m)', 'Blues'),
                            (a2, Ang, 'giro relativo (grados)', 'Greens')]:
    im = ax.imshow(M, cmap=cmap)
    ax.set_xticks(range(n)); ax.set_xticklabels(nombres, rotation=60, ha='right', fontsize=7)
    ax.set_yticks(range(n)); ax.set_yticklabels(nombres, fontsize=7)
    ax.set_title(titulo, fontsize=10); ax.grid(False)
    for i in range(n):
        for j in range(n):
            ax.text(j, i, f'{M[i,j]:.0f}' if M.max() > 10 else f'{M[i,j]:.2f}',
                    ha='center', va='center', fontsize=6.5)
    plt.colorbar(im, ax=ax, shrink=0.8)
plt.tight_layout(); plt.show()"""))

C.append(md("""**Lo que se ve y hay que comentar.** Hay parejas de configuraciones muy separadas en el espacio articular cuyas puntas están cerca, y parejas con la punta en el mismo sitio pero con orientaciones muy distintas. Ese desacoplo entre «distancia articular» y «distancia cartesiana» es la razón de que la planificación de movimiento no pueda hacerse solo en uno de los dos espacios — y es la antesala directa de S16: si varias configuraciones producen poses parecidas, ¿cuántas producen *exactamente* la misma?

### Ejercicio 2

Barre `q1` de −160 a 160 grados (los límites del modelo) manteniendo el resto de articulaciones en `qn`, y dibuja la trayectoria que describe la punta en el plano xy. ¿Qué curva es y por qué? Comprueba que el radio de esa curva coincide con `np.hypot(x, y)` evaluado en `qn`.

### Ejercicio 3

Compara el PUMA 560 y el IRB 140 en sus respectivas configuraciones `qz`: ¿cuál tiene mayor alcance (`robot.reach`)? Dibuja los dos robots con `dibujar_robot` en los mismos ejes y comenta las diferencias de arquitectura que se aprecian en las tablas DH (número de eslabones con `d` no nulo, valores de `alpha`)."""))

C.append(code("""# Ejercicio 2
q1s = np.deg2rad(np.linspace(-160, 160, 60))
# ...

# Ejercicio 3
print('alcance PUMA 560:', round(puma.reach, 4), 'm')
print('alcance IRB 140 :', round(irb.reach, 4), 'm')"""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.**

```python
T1, T2 = puma.fkine(puma.qn), puma.fkine(q_trabajo)
d = np.linalg.norm(T1.t - T2.t)                # 0.5827 m
ang, eje = (T1.inv() * T2).angvec()            # 180°, alrededor del eje y
```

La distancia entre puntas es de unos 58 cm y el giro relativo, exactamente 180 grados alrededor del eje y: las dos configuraciones apuntan la herramienta en sentidos opuestos. Lo interesante didácticamente es que las dos configuraciones difieren en solo dos articulaciones, hombro y codo (`q2` y `q3`, 90 grados cada una), y aun así la punta se va 58 cm y da media vuelta: en un 6R, los cambios articulares cerca de la base producen desplazamientos cartesianos grandes en la punta, porque el brazo actúa como palanca. Eso es exactamente lo que el jacobiano de S17 va a cuantificar.

**Ejercicio 2.** La punta describe una **circunferencia** en el plano xy centrada en el eje de la primera articulación. La razón es puramente geométrica: `q1` es un giro alrededor del eje vertical de la base, así que mueve rígidamente todo el resto del robot; la distancia de la punta a ese eje, `np.hypot(x, y)`, es un invariante del movimiento y la altura `z` tampoco cambia. Que el radio coincida con `np.hypot(x, y)` en `qn` no es una comprobación menor: es la verificación de que el modelo tiene la primera articulación donde creemos, y es el primer test que conviene hacerle a cualquier modelo DH que llegue de fuera.

**Ejercicio 3.** El PUMA 560 tiene un alcance de 1,71 m frente a los 1,23 m del IRB 140, que es un robot compacto pensado para célula pequeña. Ojo con el dato: `reach` es la suma de las longitudes de los eslabones del modelo, una cota superior geométrica, no el alcance útil de catálogo. En las tablas se aprecia que ambos comparten la arquitectura antropomórfica con muñeca esférica —los `alpha` de ±90 grados en las mismas posiciones y los tres últimos eslabones sin longitud— pero difieren en las dimensiones y en el `d` de la tercera fila, que refleja el offset de hombro. Ese offset es justamente lo que en S16 va a duplicar las soluciones de la primera articulación en soluciones «zurda» y «diestra» (Lynch y Park, 2017, pp. 223-224)."""))

C.append(md("""---

## Para llevarse de esta sesión

Un modelo de robot en la toolbox es exactamente el mismo objeto que construimos a mano en S14: una tabla DH y un producto de matrices. `fkine` no hace magia, hace `A_1 · A_2 · ... · A_6`, y conviene haberlo comprobado al menos una vez con `links[j].A(q_j)` para no tratar la librería como un oráculo.

De los detalles del ecosistema hay dos que ahorran horas de laboratorio. Las **configuraciones con nombre** (`qz`, `qr`, `qn`) hacen los ejercicios reproducibles y son el vocabulario común de todos los ejemplos del libro. Y la **transformación de herramienta**: los modelos DH sitúan su efector en el centro de la muñeca, físicamente dentro del robot, así que cualquier comparación con un controlador real que no la tenga en cuenta va a fallar por la longitud de la pinza — y fallará de forma sistemática, no aleatoria, que es la pista para diagnosticarlo.

El mini-reto que abre la sesión siguiente: intenta llevar la punta del PUMA a un punto concreto de la mesa **probando valores articulares a mano**. Nadie lo consigue en menos de veinte intentos. Ese fracaso es la motivación entera de la cinemática inversa de S16.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S15_Taller_FK_6R.ipynb', C)
print('escrito S15')
