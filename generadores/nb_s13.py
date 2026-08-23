from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('matplotlib','matplotlib'), ('spatialmath-python','spatialmath')]
C = []

C.append(cabecera(
    "S13", "Pose, rotaciones y transformaciones homogéneas", "4",
    "viernes 9 de octubre de 2026", "2 h",
    "Convierte el álgebra de poses de la pizarra en código ejecutable: SO(2)/SE(2) en el plano, SO(3)/SE(3) en el espacio, las tres familias de parametrización de la orientación (ángulos, eje-ángulo, cuaterniones), una demostración numérica del bloqueo de cardán, y la cadena de transformaciones mundo → mesa → pieza → cámara compuesta e invertida a mano y con spatialmath.",
    "Corke (2023), cap. 2 — pose relativa (p. 26), marcos de referencia (pp. 26-27), rot2 y trplot2 (p. 34), SE(2) y transformación homogénea (p. 37), SO(3) (p. 46), composición como producto (p. 48), Euler ZYZ (p. 49), RPY y su singularidad (pp. 50-51), bloqueo de cardán (pp. 52-54), cuaterniones unitarios (pp. 57-60), SE(3) (pp. 62-63) y clases de pose (p. 90); Lynch y Park (2017), cap. 3 — condiciones de matriz de rotación (p. 69), definiciones de SO(3)/SO(2) e inversa traspuesta (p. 70), los tres usos de R (p. 71), so(3) (p. 77), coordenadas exponenciales (p. 79), fórmula de Rodrigues (p. 84) y definición de SE(3) (p. 89).",
    "los apuntes del bloque 4"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
from spatialmath import SO2, SE2, SO3, SE3, UnitQuaternion
from spatialmath.base import rot2, trot2, transl2, rpy2r, tr2rpy, eul2r, tr2eul, angvec2r, tr2angvec, vex, skew

np.set_printoptions(precision=4, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.4)
plt.rcParams['axes.grid'] = True
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
np.random.seed(4)
print('Listo. spatialmath cargado.')"""))

# ---------------- 1. SO(2) y SE(2)
C.append(md("""## 1. El plano: SO(2) y SE(2)

Toda la sesión cuelga de una sola frase: «cualquier pose es siempre una pose relativa, descrita por el movimiento necesario para llegar hasta ella desde la pose de referencia» (Corke, 2023, p. 26). Para operar con ella unimos rígidamente a cada cuerpo un marco dextrógiro y describimos la traslación entre orígenes y la rotación entre ejes (Corke, 2023, pp. 26-27).

Empezamos en 2D, donde todo se puede dibujar. La matriz de rotación tiene por columnas los ejes del marco girado; no vale cualquier matriz: sus columnas han de ser unitarias y ortogonales —seis ligaduras en 3D, tres en 2D, compactadas en `R.T @ R == I`— y además `det R = +1` para excluir marcos levógiros (Lynch y Park, 2017, p. 69). Eso define el grupo SO(2) (Definición 3.2; Lynch y Park, 2017, p. 70).

La propiedad que más usaremos en todo el bloque: **la inversa de una rotación es su traspuesta**, `R⁻¹ = Rᵀ` (Proposición 3.3; Lynch y Park, 2017, p. 70). Invertir orientaciones es gratis."""))

C.append(code("""th = 0.3                      # rad
R = rot2(th)                  # (Corke, 2023, p. 34)
print('R(0.3) =\\n', R)

print('\\nR.T @ R = I ?      ', np.allclose(R.T @ R, np.eye(2)))
print('det R = +1 ?       ', np.isclose(np.linalg.det(R), 1.0))
print('R^-1 == R.T ?      ', np.allclose(np.linalg.inv(R), R.T))

# Composicion: rotar 0.3 y luego 0.4 equivale a rotar 0.7
print('\\nR(0.3)@R(0.4) == R(0.7) ?', np.allclose(rot2(0.3) @ rot2(0.4), rot2(0.7)))

# Los tres usos de R (Lynch y Park, 2017, p. 71): aqui, rotar un vector
v = np.array([1.0, 0.0])
print('R @ [1,0] =', R @ v, ' -> longitud', round(float(np.linalg.norm(R @ v)), 6))"""))

C.append(md("""Ahora la pose completa en el plano. Empaquetamos rotación y traslación en una matriz 3x3 que opera sobre coordenadas homogéneas (el punto con un 1 añadido): `p_A = T_AB · p_B`. «T_AB se denomina transformación homogénea» y estas matrices forman el grupo SE(2) (Corke, 2023, p. 37).

Dibujamos los marcos con matplotlib en vez de con `trplot2` para no depender del backend interactivo de Colab: cada marco es simplemente su origen más sus dos columnas de rotación."""))

C.append(code("""def dibujar_marco2(ax, T, nombre, color, escala=0.6):
    \"\"\"Dibuja un marco 2D a partir de una SE(2) de 3x3: origen + columnas de R.\"\"\"
    T = np.asarray(T)
    o, Rm = T[:2, 2], T[:2, :2]
    for k, (etq, dx) in enumerate(zip(('x', 'y'), Rm.T)):
        ax.arrow(o[0], o[1], escala*dx[0], escala*dx[1], head_width=0.09,
                 color=color, length_includes_head=True)
        ax.text(o[0] + 1.15*escala*dx[0], o[1] + 1.15*escala*dx[1], f'{etq}{nombre}',
                color=color, fontsize=9)
    ax.plot(*o, 'o', color=color, ms=5)

# TA = transl2(1, 2) @ trot2(30 grados)   (Corke, 2023, p. 38)
TA = transl2(1, 2) @ trot2(30, unit='deg')
TB = transl2(2, 1) @ trot2(0, unit='deg')
TAB = np.linalg.inv(TA) @ TB          # pose de {B} vista desde {A}

fig, ax = plt.subplots(figsize=(6, 4.2))
dibujar_marco2(ax, np.eye(3), '0', 'black')
dibujar_marco2(ax, TA, 'A', IQS_AZUL)
dibujar_marco2(ax, TB, 'B', IQS_VERDE)
ax.set_xlim(-0.8, 3.6); ax.set_ylim(-0.6, 3.4); ax.set_aspect('equal')
ax.set_title('Marcos {0}, {A} y {B} en el plano')
plt.tight_layout(); plt.show()

print('T_0A =\\n', TA)
print('\\nT_AB (pose de B vista desde A) =\\n', TAB)
print('\\nT_0A @ T_AB == T_0B ?', np.allclose(TA @ TAB, TB))""" ))

C.append(md("""**Lo que hay que hacer notar.** La composición se lee «en cadena»: `T_0B = T_0A · T_AB`, los subíndices interiores se cancelan. La inmensa mayoría de los errores de laboratorio son errores de subíndices, no de concepto; conviene imponer esta disciplina desde el primer minuto.

### Ejercicio 1

Comprueba que `T_AB` calculada arriba coincide con la que obtienes componiendo a mano: la posición de B vista desde A es `Rᵀ_0A · (p_0B − p_0A)` y la orientación es `Rᵀ_0A · R_0B`. Después dibuja el marco {B} visto desde {A} sobre el marco {A} y convéncete de que es la misma flecha."""))

C.append(code("""# Ejercicio 1: escribe aqui la comprobacion a mano
R0A, p0A = TA[:2, :2], TA[:2, 2]
R0B, p0B = TB[:2, :2], TB[:2, 2]
# ..."""))

# ---------------- 2. SO(3)
C.append(md("""## 2. El espacio: SO(3) y la no conmutatividad

En 3D la rotación es un miembro de SO(3) (Corke, 2023, p. 46) y la composición de orientaciones se implementa como producto de matrices (Corke, 2023, p. 48). La diferencia esencial con el plano es que **ese producto no conmuta**: en clase se demuestra en diez segundos con dos giros de 90 grados de un libro físico; aquí lo hacemos con dos matrices.

Contamos también los grados de libertad: nueve números menos las seis ligaduras de `RᵀR = I` dejan **tres** grados de libertad. De ahí la tentación —y el peligro— de las parametrizaciones de tres ángulos de la sección siguiente."""))

C.append(code("""Rx90 = SO3.Rx(90, unit='deg')
Rz90 = SO3.Rz(90, unit='deg')

A = Rx90 * Rz90        # primero z, luego x
B = Rz90 * Rx90        # al reves

print('Rx·Rz =\\n', A.R)
print('\\nRz·Rx =\\n', B.R)
print('\\n¿Conmutan?', np.allclose(A.R, B.R))

# a donde va el eje x del cuerpo en cada caso
print('\\nRx·Rz aplicada a [1,0,0] ->', A.R @ np.array([1, 0, 0]))
print('Rz·Rx aplicada a [1,0,0] ->', B.R @ np.array([1, 0, 0]))

# grados de libertad
print('\\nNumeros en R:', 9, '| ligaduras de R.T@R=I:', 6, '| gdl:', 3)""" ))

# ---------------- 3. Tres angulos y el bloqueo de cardan
C.append(md("""## 3. Tres ángulos y el bloqueo de cardán, demostrado con números

Hay doce secuencias válidas de tres ángulos: seis eulerianas (mismo eje primero y tercero) y seis cardánicas (tres ejes distintos) (Corke, 2023, p. 48). En dinámica mecánica es habitual la ZYZ, `R = Rz(φ)·Ry(θ)·Rz(ψ)` (Corke, 2023, p. 49). Los ángulos de balanceo-cabeceo-guiñada (roll-pitch-yaw) son cardánicos y arrastran una ambigüedad práctica: hay dos secuencias en uso común, ZYX y XYZ, según el ámbito (Corke, 2023, p. 50). **La primera pregunta ante cualquier controlador o fichero de calibración debe ser siempre: ¿qué secuencia y en qué unidades?**

El defecto es estructural, no de una convención concreta: «todas las representaciones de tres ángulos, ya sean eulerianas o cardánicas, sufren el problema del bloqueo de cardán cuando dos ejes se alinean» (Corke, 2023, p. 53). Para la secuencia ZYX la singularidad está en cabeceo = ±90 grados (Corke, 2023, p. 51). El término viene de los cardanes de la navegación inercial y se hizo famoso con el Apolo 13 (Corke, 2023, pp. 52 y 54).

Lo demostramos de dos maneras complementarias."""))

C.append(code("""# --- ida y vuelta en un caso normal ---
rpy0 = np.array([0.1, 0.2, 0.3])
R0 = rpy2r(*rpy0, order='zyx')                 # (Corke, 2023, p. 51)
print('rpy -> R -> rpy :', tr2rpy(R0, order='zyx'), ' recuperado?',
      np.allclose(tr2rpy(R0, order='zyx'), rpy0))

eul0 = np.array([0.1, 0.2, 0.3])
Re = eul2r(*eul0)                              # ZYZ (Corke, 2023, p. 49)
print('eul -> R -> eul :', tr2eul(Re), ' recuperado?', np.allclose(tr2eul(Re), eul0))

# --- SINTOMA 1: en pitch = 90 grados se pierde un grado de libertad ---
print('\\n--- bloqueo de cardan: pitch = 90 grados ---')
Ra = rpy2r(0.3, np.pi/2, 0.1, order='zyx')
Rb = rpy2r(0.5, np.pi/2, 0.3, order='zyx')     # mismo (roll - yaw) = 0.2
Rc = rpy2r(0.5, np.pi/2, -0.1, order='zyx')    # mismo (roll + yaw) = 0.4
print('(0.3, 90, 0.1) == (0.5, 90, 0.3) ?', np.allclose(Ra, Rb), '  <- solo cuenta roll - yaw')
print('(0.3, 90, 0.1) == (0.5, 90,-0.1) ?', np.allclose(Ra, Rc))
print('Dos parejas de angulos distintas dan LA MISMA orientacion: la representacion degenera.')"""))

C.append(md("""El segundo síntoma es el que de verdad duele en un controlador: cerca de la singularidad, orientaciones muy parecidas exigen **tasas de ángulos arbitrariamente grandes**. Lo medimos con el número de condición de la matriz que relaciona las derivadas de los ángulos con la velocidad angular, calculada aquí por diferencias finitas."""))

C.append(code("""def B_rpy(rpy, h=1e-7):
    \"\"\"Matriz 3x3 que mapea (roll_dot, pitch_dot, yaw_dot) -> velocidad angular omega.
    Columna i = vex( dR/drpy_i · R.T ), por diferencias finitas.\"\"\"
    R0 = rpy2r(*rpy, order='zyx')
    cols = []
    for i in range(3):
        e = np.zeros(3); e[i] = h
        dR = (rpy2r(*(np.asarray(rpy) + e), order='zyx') - R0) / h
        cols.append(vex(dR @ R0.T))
    return np.column_stack(cols)

print(f\"{'pitch (deg)':>12} {'|det B|':>12} {'cond(B)':>12}\")
for pd in [0, 45, 80, 89, 89.9, 89.99]:
    Bm = B_rpy([0.2, np.deg2rad(pd), 0.1])
    print(f'{pd:>12} {abs(np.linalg.det(Bm)):>12.6f} {np.linalg.cond(Bm):>12.1f}')

print('\\nEl determinante va a cero y el numero de condicion explota:')
print('para mover el efector un poco cerca de pitch=90 hacen falta tasas de angulos enormes.')"""))

C.append(md("""**Moraleja docente.** Los tres ángulos son excelentes para *comunicar* orientaciones a humanos y pésimos como *representación interna* de un algoritmo. Este mismo fenómeno reaparecerá dos veces más en el bloque: en la singularidad de muñeca del PUMA (S16) y en el jacobiano analítico (S17).

### Ejercicio 2

Repite el barrido de `B_rpy` con la secuencia `'xyz'` en lugar de `'zyx'`. ¿Sigue habiendo singularidad? ¿En qué ángulo? Comprueba después qué le pasa a `tr2rpy` cuando le pasas una `R` con cabeceo exactamente 90 grados: ¿qué valores devuelve para roll y yaw, y por qué precisamente esos?"""))

C.append(code("""# Ejercicio 2
# for pd in [0, 45, 80, 89, 89.9]:
#     ..."""))

# ---------------- 4. Eje-angulo y cuaterniones
C.append(md("""## 4. Eje-ángulo y cuaterniones unitarios: las representaciones sin singularidad

El teorema de Euler garantiza que toda orientación se alcanza girando un ángulo `th` alrededor de un único eje unitario `w`. Lynch y Park lo formalizan como las **coordenadas exponenciales** de la rotación (2017, p. 79): con la matriz antisimétrica `[w]` asociada al eje —el conjunto de esas matrices es so(3), el álgebra de Lie del grupo (2017, p. 77)—, la rotación es `R = e^([w]·th)`, con la forma cerrada conocida como **fórmula de Rodrigues**:

`R = I + sin(th)·[w] + (1 − cos(th))·[w]²`   (ecuación 3.51; Lynch y Park, 2017, p. 84)

El cuaternión unitario empaqueta exactamente esa información —un escalar `cos(th/2)` y un vector `ŵ·sin(th/2)` (Corke, 2023, p. 57)— en cuatro números con una ligadura de norma. «Los cuaterniones unitarios se usan ampliamente hoy en robótica, visión por computador, gráficos por computador y sistemas de navegación aeroespacial» (Corke, 2023, p. 59): componen barato, se renormalizan trivialmente frente a la deriva numérica y no tienen singularidad de representación."""))

C.append(code("""# --- Rodrigues a mano, comparada con la toolbox ---
def rodrigues(w, th):
    \"\"\"R = I + sin(th)·[w] + (1-cos(th))·[w]^2  (Lynch y Park, 2017, p. 84).\"\"\"
    w = np.asarray(w, float); w = w / np.linalg.norm(w)
    W = skew(w)                                     # matriz antisimetrica [w], so(3)
    return np.eye(3) + np.sin(th) * W + (1 - np.cos(th)) * (W @ W)

w, th = np.array([1.0, 2.0, 2.0]), 0.9
R_mano = rodrigues(w, th)
R_tbox = angvec2r(th, w)
print('Rodrigues a mano == angvec2r de la toolbox ?', np.allclose(R_mano, R_tbox))
print('¿Es una rotacion valida? R.T@R=I:', np.allclose(R_mano.T @ R_mano, np.eye(3)),
      '| det:', round(float(np.linalg.det(R_mano)), 9))

# problema inverso: de R a (th, w)
th2, w2 = tr2angvec(R_mano)
print('\\nRecuperado th =', round(float(th2), 6), ' eje =', w2.round(6),
      '| eje original normalizado =', (w / np.linalg.norm(w)).round(6))"""))

C.append(code("""# --- cuaterniones unitarios (Corke, 2023, pp. 59-60) ---
q1 = UnitQuaternion.Rx(0.4)
q2 = UnitQuaternion.Rz(1.1)

print('q1 =', q1)
print('q2 =', q2)
print('q1*q2 (composicion) =', q1 * q2)
print('\\n¿Componer cuaterniones == componer matrices?',
      np.allclose((q1 * q2).R, q1.R @ q2.R))
print('¿Norma unitaria?', round(float(np.linalg.norm((q1 * q2).A)), 12))
print('Inversa = conjugado:', np.allclose((q1.inv() * q1).R, np.eye(3)))

# relacion explicita con eje-angulo: (cos(th/2), w_hat·sin(th/2))
th, eje = 0.9, np.array([1.0, 2.0, 2.0]); eje = eje / np.linalg.norm(eje)
q_mano = np.hstack([np.cos(th/2), eje * np.sin(th/2)])
q_tbox = UnitQuaternion.AngVec(th, eje).A
print('\\n(cos(th/2), w·sin(th/2)) =', q_mano.round(6))
print('UnitQuaternion.AngVec     =', q_tbox.round(6))
print('¿Coinciden?', np.allclose(q_mano, q_tbox))"""))

C.append(md("""Un último argumento a favor del cuaternión: **interpola bien**. La interpolación esférica (slerp) recorre el camino más corto sobre la esfera de orientaciones a velocidad angular constante, cosa que la interpolación lineal de tres ángulos no garantiza. Lo comprobamos midiendo el ángulo girado entre pasos consecutivos."""))

C.append(code("""qa = UnitQuaternion.RPY([0.0, 0.0, 0.0])
qb = UnitQuaternion.RPY([0.6, 0.9, 2.4])

s = np.linspace(0, 1, 21)
q_slerp = qa.interp(qb, s)          # slerp: 21 cuaterniones unitarios
rpy_a, rpy_b = np.array([0.0, 0.0, 0.0]), np.array([0.6, 0.9, 2.4])
R_lineal = [rpy2r(*(rpy_a + si * (rpy_b - rpy_a)), order='zyx') for si in s]

def paso_angular(Rs):
    \"\"\"Angulo girado entre poses consecutivas, en grados.\"\"\"
    d = []
    for R1, R2 in zip(Rs[:-1], Rs[1:]):
        ang, _ = tr2angvec(np.asarray(R1).T @ np.asarray(R2))
        d.append(np.rad2deg(abs(ang)))
    return np.array(d)

d_slerp = paso_angular([q.R for q in q_slerp])
d_lin = paso_angular(R_lineal)

fig, ax = plt.subplots(figsize=(8, 3.2))
ax.plot(d_slerp, 'o-', color=IQS_AZUL, label='slerp (cuaterniones)')
ax.plot(d_lin, 's-', color=IQS_VERDE, label='interpolación lineal de RPY')
ax.set_xlabel('paso'); ax.set_ylabel('ángulo girado (grados)')
ax.set_title('Velocidad angular a lo largo de la interpolación'); ax.legend(fontsize=8)
plt.tight_layout(); plt.show()

print(f'slerp : paso min {d_slerp.min():.3f}°, max {d_slerp.max():.3f}°, '
      f'dispersion {d_slerp.std():.4f}')
print(f'RPY   : paso min {d_lin.min():.3f}°, max {d_lin.max():.3f}°, '
      f'dispersion {d_lin.std():.4f}')"""))

# ---------------- 5. SE(3)
C.append(md("""## 5. SE(3): la cadena mundo → mesa → pieza → cámara

En 3D empaquetamos todo en la matriz 4x4 `T = [R p; 0 1]`: «el grupo euclidiano especial SE(3), también conocido como el grupo de los movimientos de cuerpo rígido» (Definición 3.13; Lynch y Park, 2017, p. 89), «muy comúnmente usada en robótica, gráficos por computador y visión» (Corke, 2023, p. 62) y pensable como el par ordenado (R, t) (Corke, 2023, p. 63).

Dos operaciones y ya está todo:

- composición: `T_AC = T_AB · T_BC`
- inversa en forma cerrada: `T⁻¹ = [Rᵀ, −Rᵀ·p; 0 1]` — **nunca** se invierte una T con un solver genérico

Montamos la célula de trabajo típica del laboratorio: una mesa colocada respecto del mundo, una pieza sobre la mesa y una cámara mirándola. La pregunta operativa es siempre la misma: ¿dónde está la pieza *vista desde la cámara*?"""))

C.append(code("""# Cadenas al estilo de Corke (2023, pp. 90 y 105)
T_mundo_mesa   = SE3.Trans(1.2, 0.5, 0.0) * SE3.Rz(25, unit='deg')
T_mesa_pieza   = SE3.Trans(0.30, 0.10, 0.75) * SE3.Rz(-40, unit='deg')
T_mundo_camara = SE3.Trans(0.8, -0.4, 1.9) * SE3.Rx(180, unit='deg') * SE3.Rz(60, unit='deg')

T_mundo_pieza = T_mundo_mesa * T_mesa_pieza          # composicion en cadena
T_camara_pieza = T_mundo_camara.inv() * T_mundo_pieza  # lo que "ve" la camara

print('Pieza en el mundo:'); T_mundo_pieza.printline()
print('Pieza vista desde la camara:'); T_camara_pieza.printline()
print('\\nDistancia camara-pieza:', round(float(np.linalg.norm(T_camara_pieza.t)), 4), 'm')"""))

C.append(code("""# La inversa en forma cerrada, escrita a mano
def inv_se3(T):
    \"\"\"T^-1 = [R.T, -R.T·p; 0 1]  -- sin resolver ningun sistema.\"\"\"
    T = np.asarray(T)
    R, p = T[:3, :3], T[:3, 3]
    Ti = np.eye(4)
    Ti[:3, :3] = R.T
    Ti[:3, 3] = -R.T @ p
    return Ti

Tc = T_mundo_camara.A
print('inv_se3 == SE3.inv() ?', np.allclose(inv_se3(Tc), T_mundo_camara.inv().A))
print('T @ T^-1 == I ?        ', np.allclose(Tc @ inv_se3(Tc), np.eye(4)))

# error numerico frente al solver generico (aqui minusculo, pero crece con el
# condicionamiento y no aporta nada: la forma cerrada es exacta y mas rapida)
err_cerrada = np.abs(Tc @ inv_se3(Tc) - np.eye(4)).max()
err_solver = np.abs(Tc @ np.linalg.inv(Tc) - np.eye(4)).max()
print(f'\\nerror max forma cerrada: {err_cerrada:.2e}   solver generico: {err_solver:.2e}')"""))

C.append(md("""Y la comprobación que cierra el círculo: si vuelvo a componer desde la cámara, tengo que recuperar la pieza en el mundo.

### Ejercicio 3

La cámara ve la pieza y queremos que el robot, cuya base está en `SE3.Trans(0.0, 0.0, 0.0)`, la coja. Añade al montaje una brida de robot con `T_mundo_brida = SE3.Trans(0.6, 0.2, 1.1) * SE3.Ry(90, unit='deg')` y calcula (a) la pose de la pieza vista desde la brida y (b) la pose de la cámara vista desde la mesa. Verifica en los dos casos que componiendo de vuelta recuperas la pose en el mundo con `np.allclose`."""))

C.append(code("""print('Vuelta atras: T_mundo_camara · T_camara_pieza == T_mundo_pieza ?',
      np.allclose((T_mundo_camara * T_camara_pieza).A, T_mundo_pieza.A))

# Ejercicio 3
T_mundo_brida = SE3.Trans(0.6, 0.2, 1.1) * SE3.Ry(90, unit='deg')
# ..."""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.** `R_AB = R0A.T @ R0B` y `p_AB = R0A.T @ (p0B - p0A)`; montando `T_AB` con esas dos piezas se obtiene exactamente la matriz que devuelve `np.linalg.inv(TA) @ TB`, porque eso *es* la fórmula cerrada de la inversa de una SE(2) compuesta con TB. Numéricamente:

```python
R_AB = R0A.T @ R0B
p_AB = R0A.T @ (p0B - p0A)
T_AB_mano = np.eye(3); T_AB_mano[:2,:2] = R_AB; T_AB_mano[:2,2] = p_AB
np.allclose(T_AB_mano, TAB)   # True
```

El marco {B} dibujado en coordenadas de {A} es la misma flecha física: solo hemos cambiado el observador, no hemos movido nada. Es el segundo de los «tres usos» de una matriz de rotación (Lynch y Park, 2017, p. 71).

**Ejercicio 2.** Sí, sigue habiendo singularidad: con la secuencia `'xyz'` el determinante de `B` se anula cuando el **segundo** ángulo vale ±90 grados. La singularidad no está atada a un eje concreto, sino a la estructura de «tres rotaciones sucesivas»: siempre ocurre cuando el primer y el tercer eje se alinean, que es lo que sucede cuando el ángulo intermedio los pone en paralelo. Eso es literalmente lo que dice Corke: el problema afecta a *todas* las representaciones de tres ángulos (2023, p. 53).

Al pedir `tr2rpy` de una R con cabeceo exactamente 90 grados, la función devuelve una solución de la familia infinita —típicamente asignando 0 a uno de los dos ángulos degenerados y toda la diferencia al otro—. No es un fallo de la función: no hay más información en la matriz. Solo está determinada la combinación `roll − yaw`.

**Ejercicio 3.** `T_brida_pieza = T_mundo_brida.inv() * T_mundo_pieza` y `T_mesa_camara = T_mundo_mesa.inv() * T_mundo_camara`. Las dos comprobaciones de vuelta (`T_mundo_brida * T_brida_pieza` y `T_mundo_mesa * T_mesa_camara`) dan `True` con `np.allclose`. Lo que hay que subrayar en clase es que **no hemos hecho geometría, hemos hecho contabilidad de subíndices**: una vez fijada la disciplina T_AB, cualquier pregunta de la célula («¿dónde está X visto desde Y?») se responde con un producto y, como mucho, una inversa. Esta misma contabilidad es la calibración cámara-robot del bloque 6 y la cinemática directa de S14."""))

C.append(md("""---

## Para llevarse de esta sesión

**Matrices para operar, ángulos para comunicar, cuaterniones para interpolar y almacenar.** Es el resumen en una frase de la sesión, y la regla práctica que evita el 90 % de los problemas: en cuanto una orientación entra en un algoritmo debe dejar de ser una terna de ángulos.

El bloqueo de cardán no es una curiosidad histórica ni un defecto de una convención concreta: es una consecuencia topológica de intentar cubrir SO(3) con tres números. Lo hemos visto degenerar en dos formas —dos ternas distintas dando la misma orientación, y el número de condición de la transformación de tasas explotando— y volverá a aparecer en S16 (singularidad de muñeca) y en S17 (jacobiano analítico). Cuando vuelva, conviene reconocerlo como el mismo animal.

Y el aparato algebraico de SE(3) —componer y invertir— es literalmente todo lo que hace falta para la cinemática directa: un robot serie no es más que una cadena de poses relativas, cada una función de una variable articular. Eso es exactamente lo que montaremos en S14.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S13_Pose_Rotaciones.ipynb', C)
print('escrito S13')
