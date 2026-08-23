from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('matplotlib','matplotlib'), ('spatialmath-python','spatialmath'),
       ('roboticstoolbox-python','roboticstoolbox')]
C = []

C.append(cabecera(
    "S19", "Estática, dualidad fuerza-velocidad y generación de trayectorias", "4",
    "viernes 23 de octubre de 2026", "2 h",
    "Cierra el bloque con las dos aplicaciones que reutilizan todo lo anterior: la estática tau = J^T·F, con el elipsoide de fuerzas como dual exacto del de manipulabilidad, y la generación de trayectorias punto a punto con polinomio quíntico y perfil trapezoidal, en espacio articular y en espacio cartesiano, monitorizando la manipulabilidad a lo largo del camino.",
    "Lynch y Park (2017), cap. 5 — deducción de tau = J^T·f_tip por conservación de potencia, ecuación 5.3 (pp. 174-175), elipsoide de fuerza y semiejes recíprocos (pp. 176-177), la maleta pesada y el elipsoide de fuerza infinito en la singularidad (p. 177) y llaves de fuerza (p. 190); cap. 9 — camino frente a ley temporal (p. 325), s(t) de [0, T] a [0, 1] (p. 326), polinomio cúbico (p. 329), quíntico más suave (p. 330), perfil trapezoidal (pp. 330-331), tiempo mínimo (pp. 331-332), degeneración en triángulo bang-bang (p. 331) y jerk infinito (p. 333); Corke (2023) — quíntico con seis condiciones de contorno (pp. 98-99), trapezoidal (p. 100), interpolación de pose (p. 105), jtraj (p. 286), ctraj (p. 287), caída de manipulabilidad en la trayectoria cartesiana (p. 289), Q = J^T·w y el par de hombro (p. 324) y la traspuesta nunca es singular (p. 325).",
    "los apuntes del bloque 4"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
import roboticstoolbox as rtb
from roboticstoolbox import quintic, trapezoidal, jtraj, ctraj
from spatialmath import SE3

np.set_printoptions(precision=4, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.4)
plt.rcParams['axes.grid'] = True
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('roboticstoolbox', rtb.__version__, '- listo.')"""))

C.append(md("""> **Aviso para Colab.** `roboticstoolbox-python` **tarda varios minutos** en instalarse la primera vez; lanza la celda de instalación nada más abrir el cuaderno. Las secciones 1, 2 y 3 solo necesitan numpy, así que da tiempo de sobra. Como en el resto del bloque, **nada de `robot.plot()` ni `robot.teach()`**."""))

# ---------------- 1. Estatica
C.append(md("""## 1. Estática: `tau = Jᵀ·F`

El jacobiano también gobierna las fuerzas, y el argumento es de **conservación de potencia**. Con el robot en equilibrio estático —sin potencia empleada en moverlo—, la potencia medida en la punta debe igualar la generada en las articulaciones:

`f_tipᵀ·v_tip = tauᵀ·q̇`

Sustituyendo `v_tip = J(q)·q̇` y exigiendo que la igualdad valga para **toda** velocidad articular arbitraria, se concluye

`tau = Jᵀ(q)·f_tip`   (ecuación 5.3; Lynch y Park, 2017, pp. 174-175)

La versión general con llaves de fuerza (*wrenches*) de seis componentes es idéntica (Lynch y Park, 2017, p. 190): en notación de Corke, una llave `w = (fx, fy, fz, mx, my, mz)` aplicada en el efector y expresada en el marco del mundo se transforma al espacio articular como `Q = Jᵀ(q)·w` (Corke, 2023, p. 324).

Empezamos por el 2R, donde el resultado se puede comprobar con el momento de una fuerza."""))

C.append(code("""A1, A2 = 1.0, 0.8

def fk_2r(q, a1=A1, a2=A2):
    q1, q2 = q
    return np.array([a1*np.cos(q1) + a2*np.cos(q1+q2),
                     a1*np.sin(q1) + a2*np.sin(q1+q2)])

def jac_2r(q, a1=A1, a2=A2):
    q1, q2 = q
    s1, c1 = np.sin(q1), np.cos(q1)
    s12, c12 = np.sin(q1+q2), np.cos(q1+q2)
    return np.array([[-a1*s1 - a2*s12, -a2*s12],
                     [ a1*c1 + a2*c12,  a2*c12]])

def puntos_2r(q, a1=A1, a2=A2):
    q1, q2 = q
    p0 = np.zeros(2)
    p1 = p0 + a1*np.array([np.cos(q1), np.sin(q1)])
    p2 = p1 + a2*np.array([np.cos(q1+q2), np.sin(q1+q2)])
    return np.vstack([p0, p1, p2])

q = np.deg2rad([30.0, 45.0])
F = np.array([0.0, -50.0])            # 50 N hacia abajo: una carga de ~5 kg en la punta
tau = jac_2r(q).T @ F
print(f'Postura q = (30°, 45°), fuerza F = {F} N')
print(f'  pares necesarios: tau1 = {tau[0]:7.3f} N·m   tau2 = {tau[1]:7.3f} N·m')

# comprobacion independiente: momento de la fuerza respecto de cada eje
P = puntos_2r(q)
brazo1 = P[2] - P[0]                  # de la base a la punta
brazo2 = P[2] - P[1]                  # del codo a la punta
mom1 = brazo1[0]*F[1] - brazo1[1]*F[0]
mom2 = brazo2[0]*F[1] - brazo2[1]*F[0]
print(f'  momento de F respecto de la base: {mom1:7.3f} N·m')
print(f'  momento de F respecto del codo  : {mom2:7.3f} N·m')
print('\\n¿Coinciden con J.T @ F?', np.allclose(tau, [mom1, mom2]))
print('La formula no es un truco algebraico: es el momento de la fuerza, articulacion')
print('a articulacion, calculado de una sola vez.')"""))

C.append(md("""Y la comprobación por **potencia virtual**, que es de donde sale la fórmula: para cualquier velocidad articular que uno elija, la potencia calculada en las articulaciones y la calculada en la punta tienen que coincidir."""))

C.append(code("""rng = np.random.default_rng(19)
print(f\"{'q_dot':>26} {'P articular':>13} {'P en la punta':>15}   iguales?\")
for _ in range(5):
    qd = rng.uniform(-2, 2, 2)
    P_art = tau @ qd
    P_punta = F @ (jac_2r(q) @ qd)
    print(f'{str(qd.round(3)):>26} {P_art:>13.6f} {P_punta:>15.6f}   '
          f'{np.isclose(P_art, P_punta)}')
print('\\nLa igualdad vale para CUALQUIER q_dot: por eso tau = J.T @ F.')"""))

C.append(md("""Ahora la lectura de ingeniería, que es la que conecta con el dimensionado de actuadores del bloque 3: **¿cómo varía el par de hombro necesario según la postura?** Sostener la misma carga con el brazo estirado o recogido no cuesta lo mismo, ni de lejos."""))

C.append(code("""q2s = np.deg2rad(np.linspace(1, 179, 300))
taus = np.array([jac_2r([np.deg2rad(20), q2]).T @ F for q2 in q2s])

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 3.6))
a1.plot(np.rad2deg(q2s), np.abs(taus[:, 0]), color=IQS_AZUL, lw=2, label='|tau1| (hombro)')
a1.plot(np.rad2deg(q2s), np.abs(taus[:, 1]), color=IQS_VERDE, lw=2, label='|tau2| (codo)')
a1.set_xlabel('q2 (grados)'); a1.set_ylabel('par (N·m)'); a1.legend(fontsize=8)
a1.set_title('Par para sostener 50 N con q1 = 20°', fontsize=10)

alcance = np.array([np.linalg.norm(fk_2r([np.deg2rad(20), q2])) for q2 in q2s])
a2.plot(alcance, np.abs(taus[:, 0]), color=IQS_AZUL, lw=2)
a2.set_xlabel('distancia de la punta al eje del hombro (m)')
a2.set_ylabel('|tau1| (N·m)'); a2.set_title('El par es proporcional al brazo de palanca', fontsize=10)
plt.tight_layout(); plt.show()

j_max, j_min = int(np.abs(taus[:, 0]).argmax()), int(np.abs(taus[:, 0]).argmin())
print(f'Par de hombro maximo: {abs(taus[j_max,0]):.2f} N·m con q2 = {np.rad2deg(q2s[j_max]):.0f}°')
print(f'Par de hombro minimo: {abs(taus[j_min,0]):.2f} N·m con q2 = {np.rad2deg(q2s[j_min]):.0f}°')
print(f'Factor entre el caso peor y el mejor: {abs(taus[j_max,0]/taus[j_min,0]):.1f}x')"""))

C.append(md("""**Y la observación más sutil de la sesión.** «El mapeo entre una llave aplicada al efector y la fuerza articular generalizada involucra la traspuesta del jacobiano, y **esta nunca puede ser singular**» (Corke, 2023, p. 325). A diferencia del mapeo de velocidades, la estática **no explota** en las singularidades: `Jᵀ` siempre existe y siempre da un par finito. Lo que explota es su *inversa* —el problema de «qué fuerza puedo ejercer con estos pares»—, que es exactamente lo que formaliza la dualidad de la sección siguiente."""))

C.append(code("""q_sing = np.deg2rad([20.0, 0.0])        # brazo estirado: J es singular
J_s = jac_2r(q_sing)
print('En la singularidad (brazo estirado):')
print('  det J =', round(float(np.linalg.det(J_s)), 12))
print('  tau = J.T @ F =', (J_s.T @ F).round(4), 'N·m   <- perfectamente finito')
try:
    np.linalg.solve(J_s, [0.1, 0.0])
except np.linalg.LinAlgError as e:
    print('  pero q_dot = J^-1 @ v ->', type(e).__name__, ':', e)
print('\\nLa estatica sobrevive donde la cinematica diferencial se rompe.')"""))

# ---------------- 2. Dualidad
C.append(md("""## 2. La dualidad fuerza-velocidad

Los dos elipsoides se construyen con la misma técnica. El de **manipulabilidad** mapea velocidades articulares de norma unidad a velocidades de la punta, `v = J·q̇`. El de **fuerza** mapea el contorno de iso-esfuerzo unitario de pares articulares al espacio de fuerzas de la punta, a través de la traspuesta inversa: `f = J⁻ᵀ·tau` (Lynch y Park, 2017, p. 176).

El resultado central: «los ejes principales del elipsoide de manipulabilidad y del elipsoide de fuerza están alineados, y las longitudes de los semiejes principales del elipsoide de fuerza son los **recíprocos** de las del elipsoide de manipulabilidad» (Lynch y Park, 2017, pp. 176-177). En consecuencia, «si es difícil generar velocidad de la punta en una dirección, es fácil generar fuerza en esa misma dirección, y viceversa» (Lynch y Park, 2017, p. 176).

Lo comprobamos con la SVD: si `J = U·Σ·Vᵀ`, entonces `J⁻ᵀ = U·Σ⁻¹·Vᵀ`. **Mismas direcciones U, semiejes invertidos.**"""))

C.append(code("""def elipse(M, n=200):
    th = np.linspace(0, 2*np.pi, n)
    return M @ np.vstack([np.cos(th), np.sin(th)])

for etq, q_i in [('postura sana  q = (25°, 95°)', np.deg2rad([25, 95])),
                 ('casi singular q = (25°, 12°)', np.deg2rad([25, 12]))]:
    J = jac_2r(q_i)
    U, S, Vt = np.linalg.svd(J)
    Uf, Sf, _ = np.linalg.svd(np.linalg.inv(J).T)
    print(f'{etq}')
    print(f'   semiejes de velocidad : {S.round(4)}')
    print(f'   semiejes de fuerza    : {Sf.round(4)}   '
          f'(1/S = {(1/S).round(4)})')
    print(f'   ¿reciprocos? {np.allclose(np.sort(Sf), np.sort(1/S))}'
          f'   ¿mismas direcciones? {np.allclose(np.abs(U), np.abs(Uf[:, ::-1]))}')"""))

C.append(code("""fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.8))
for ax, (q_i, titulo) in zip(axes, [(np.deg2rad([25, 95]), 'postura sana'),
                                    (np.deg2rad([25, 12]), 'casi singular')]):
    J = jac_2r(q_i)
    P = puntos_2r(q_i)
    Ev = elipse(J) * 0.30                       # velocidades
    Ef = elipse(np.linalg.inv(J).T) * 0.30      # fuerzas

    ax.plot(P[:, 0], P[:, 1], 'o-', lw=3, ms=7, color='black')
    ax.plot(P[-1, 0] + Ev[0], P[-1, 1] + Ev[1], color=IQS_AZUL, lw=2,
            label='elipsoide de velocidad')
    ax.fill(P[-1, 0] + Ev[0], P[-1, 1] + Ev[1], color=IQS_AZUL, alpha=0.12)
    ax.plot(P[-1, 0] + Ef[0], P[-1, 1] + Ef[1], color=IQS_VERDE, lw=2, ls='--',
            label='elipsoide de fuerza')
    ax.fill(P[-1, 0] + Ef[0], P[-1, 1] + Ef[1], color=IQS_VERDE, alpha=0.12)
    ax.set_aspect('equal'); ax.legend(fontsize=8)
    ax.set_title(titulo, fontsize=10)
plt.tight_layout(); plt.show()

print('Las dos elipses estan giradas 90 grados una respecto de la otra: donde una es')
print('larga, la otra es corta. Eso es la dualidad, dibujada.')"""))

C.append(md("""**El ejemplo somático del libro lo fija para siempre.** Transportar una maleta pesada es mucho más fácil con el brazo colgando estirado, porque en esa configuración singular la carga se soporta con la estructura, casi sin par en las articulaciones (Lynch y Park, 2017, p. 177). En la singularidad, el elipsoide de manipulabilidad colapsa a un segmento mientras «el elipsoide de fuerza se vuelve infinitamente largo en la dirección ortogonal al segmento» (Lynch y Park, 2017, p. 177).

Lo medimos: par necesario para sostener la misma carga en función de lo estirado que esté el brazo, con el brazo colgando hacia abajo."""))

C.append(code("""u = np.array([0.0, 1.0])          # direccion vertical: la del peso

print(f\"{'q2 (grados)':>12} {'|tau| para 50 N (N·m)':>23} {'f vertical maxima con':>24}\")
print(f\"{'':>12} {'':>23} {'|tau| = 1 (N)':>24}\")
for q2d in [90, 45, 20, 10, 5, 2, 0.5]:
    q_m = np.array([-np.pi/2 + np.deg2rad(q2d)/2, np.deg2rad(q2d)])   # brazo hacia abajo
    J = jac_2r(q_m)
    tau_m = J.T @ np.array([0.0, -50.0])
    # fuerza maxima ejercible en la direccion u con pares de norma unidad:
    # tau = J.T @ (c·u) y |tau| <= 1  ->  c <= 1 / |J.T @ u|
    f_vert = 1.0 / np.linalg.norm(J.T @ u)
    print(f'{q2d:>12} {np.linalg.norm(tau_m):>23.3f} {f_vert:>24.2f}')
print('\\nCuanto mas estirado el brazo, menos par hace falta y mas fuerza puede ejercer:')
print('las posturas singulares son MALAS para mover y EXCELENTES para sostener.')"""))

C.append(md("""**La lección de diseño de célula**, que conviene decir con todas las letras: taladrar, prensar o soportar conviene hacerlo cerca de una singularidad; seguir trayectorias finas, lejos. Es la misma geometría, leída al revés.

### Ejercicio 1

Calcula con el PUMA 560 los pares necesarios para sostener una masa de 10 kg colgada de la brida (`w = [0, 0, −98.1, 0, 0, 0]`) en `qn` y en `qs` (brazo estirado). ¿En qué articulación aparece el par mayor y por qué? Compara los dos casos y relaciónalo con el dimensionado de actuadores del bloque 3."""))

C.append(code("""# Ejercicio 1
puma = rtb.models.DH.Puma560()
w = np.array([0.0, 0.0, -98.1, 0.0, 0.0, 0.0])       # 10 kg colgando
# tau = puma.jacob0(q).T @ w
# ..."""))

# ---------------- 3. Trayectorias
C.append(md("""## 3. Leyes temporales: quíntico y trapezoidal

Generar movimiento exige separar dos decisiones: «una trayectoria es la combinación de un **camino**, una descripción puramente geométrica de la secuencia de configuraciones alcanzadas por el robot, y una **ley temporal** (*time scaling*) que especifica los instantes en los que se alcanzan esas configuraciones» (Lynch y Park, 2017, p. 325). Normalizando el camino con un parámetro `s` en [0, 1], la ley temporal es una función `s(t)` de [0, T] en [0, 1] (Lynch y Park, 2017, p. 326).

**El polinomio quíntico** añade dos coeficientes al cúbico para imponer también las aceleraciones de contorno: «un polinomio quíntico (de quinto orden) se usa comúnmente» y sus seis condiciones se resuelven con un sistema lineal 6x6 (Corke, 2023, pp. 98-99). Frente al cúbico da «un movimiento más suave con una velocidad máxima mayor» (Lynch y Park, 2017, p. 330), y sobre todo evita el **jerk infinito** del cúbico en el arranque y la parada (Lynch y Park, 2017, p. 333).

**El perfil trapezoidal** manda en la industria: «muy común en control de motores», concatena aceleración constante, crucero a velocidad constante y deceleración constante (Lynch y Park, 2017, pp. 330-331). Su ventaja es explotar los límites reales del accionamiento; su precio, aceleración discontinua. Si el tramo de crucero desaparece degenera en el triángulo «bang-bang» (Lynch y Park, 2017, p. 331).

Los montamos los dos a mano y los contrastamos con `quintic` y `trapezoidal` de la toolbox (Corke, 2023, pp. 99-100)."""))

C.append(code("""def quintico(q0, qf, t, T=None):
    \"\"\"s(t) quintico con velocidad Y aceleracion nulas en los dos extremos.
    Seis condiciones de contorno -> sistema lineal 6x6 (Corke, 2023, pp. 98-99).\"\"\"
    t = np.asarray(t, float)
    T = t[-1] if T is None else T
    M = np.array([[0,      0,      0,     0,    0, 1],      # s(0)   = 0
                  [T**5,   T**4,   T**3,  T**2, T, 1],      # s(T)   = 1
                  [0,      0,      0,     0,    1, 0],      # s'(0)  = 0
                  [5*T**4, 4*T**3, 3*T**2, 2*T, 1, 0],      # s'(T)  = 0
                  [0,      0,      0,     2,    0, 0],      # s''(0) = 0
                  [20*T**3, 12*T**2, 6*T,  2,   0, 0]])     # s''(T) = 0
    c = np.linalg.solve(M, np.array([0, 1, 0, 0, 0, 0], float))
    s = np.polyval(c, t)
    sd = np.polyval(np.polyder(c, 1), t)
    sdd = np.polyval(np.polyder(c, 2), t)
    return q0 + (qf - q0)*s, (qf - q0)*sd, (qf - q0)*sdd

def trapezoidal_mano(q0, qf, t, v_max, a_max):
    \"\"\"Perfil trapezoidal con cotas de velocidad y aceleracion.
    Si no hay tramo de crucero, degenera en triangulo bang-bang
    (Lynch y Park, 2017, pp. 330-331).\"\"\"
    t = np.asarray(t, float)
    D = qf - q0
    signo = np.sign(D) if D != 0 else 1.0
    D = abs(D)
    ta = v_max / a_max                       # tiempo de aceleracion
    d_acc = 0.5 * a_max * ta**2
    if 2*d_acc > D:                          # triangulo: nunca se alcanza v_max
        ta = np.sqrt(D / a_max); tc = 0.0; v_pico = a_max * ta
    else:
        tc = (D - 2*d_acc) / v_max; v_pico = v_max
    T = 2*ta + tc
    q, qd, qdd = np.zeros_like(t), np.zeros_like(t), np.zeros_like(t)
    for i, ti in enumerate(t):
        ti = min(max(ti, 0.0), T)
        if ti < ta:
            q[i] = 0.5*a_max*ti**2;                 qd[i] = a_max*ti;   qdd[i] = a_max
        elif ti < ta + tc:
            q[i] = 0.5*a_max*ta**2 + v_pico*(ti-ta); qd[i] = v_pico;    qdd[i] = 0.0
        else:
            td = T - ti
            q[i] = D - 0.5*a_max*td**2;             qd[i] = a_max*td;  qdd[i] = -a_max
    return q0 + signo*q, signo*qd, signo*qdd, T

# --- contraste con la toolbox ---
T = 2.0
t = np.linspace(0, T, 201)
q_q, qd_q, qdd_q = quintico(0.0, 1.0, t)
tg = quintic(0.0, 1.0, t)
print('¿nuestro quintico == quintic de la toolbox?',
      np.allclose(q_q, tg.q), np.allclose(qd_q, tg.qd), np.allclose(qdd_q, tg.qdd))
print(f'  velocidad maxima: {qd_q.max():.4f}   valor teorico 15·D/(8·T) = {15/(8*T):.4f}')
print(f'  aceleracion max : {qdd_q.max():.4f}   valor teorico 10·D/(√3·T²) = '
      f'{10/(np.sqrt(3)*T**2):.4f}')"""))

C.append(code("""V, Amax = 0.75, 1.2
q_t, qd_t, qdd_t, T_t = trapezoidal_mano(0.0, 1.0, t, V, Amax)
tp = trapezoidal(0.0, 1.0, t, V=V)
print(f'Trapezoidal a mano: T = {T_t:.4f} s, v pico = {qd_t.max():.4f}')
print(f'trapezoidal de la toolbox: v pico = {tp.qd.max():.4f}')

fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.4))
for ax, (yq, yt, etq) in zip(axes, [(q_q, q_t, 'posición s(t)'),
                                    (qd_q, qd_t, 'velocidad'),
                                    (qdd_q, qdd_t, 'aceleración')]):
    ax.plot(t, yq, color=IQS_AZUL, lw=2, label='quíntico')
    ax.plot(t, yt, color=IQS_VERDE, lw=2, ls='--', label='trapezoidal')
    ax.set_xlabel('t (s)'); ax.set_title(etq, fontsize=10); ax.legend(fontsize=8)
plt.tight_layout(); plt.show()

print(f\"{'perfil':>14} {'v pico':>9} {'a pico':>9} {'a continua?':>13}\")
print(f'{\"quintico\":>14} {qd_q.max():>9.4f} {abs(qdd_q).max():>9.4f} {\"si\":>13}')
print(f'{\"trapezoidal\":>14} {qd_t.max():>9.4f} {abs(qdd_t).max():>9.4f} {\"no\":>13}')"""))

C.append(md("""**Lo que hay que hacer leer en las tres gráficas.** El quíntico arranca y para con aceleración nula —de ahí que su curva de aceleración sea continua y su jerk finito—, pero paga ese lujo con un pico de velocidad más alto para el mismo tiempo. El trapezoidal recorre la misma distancia en el mismo tiempo con menos velocidad de pico, porque aprovecha todo el tramo de crucero, pero su aceleración salta de golpe en cuatro instantes: eso es lo que en un accionamiento real se traduce en vibración y ruido. Las leyes en S de los controladores comerciales suavizan precisamente esos saltos limitando el jerk (Lynch y Park, 2017, p. 333).

Y el caso degenerado que hay que provocar: si la distancia es corta o la aceleración baja, el tramo de crucero desaparece y queda el triángulo **bang-bang** de acelerar y frenar (Lynch y Park, 2017, p. 331)."""))

C.append(code("""fig, ax = plt.subplots(figsize=(8, 3.2))
for D, col in [(1.0, IQS_AZUL), (0.4, IQS_VERDE), (0.1, 'crimson')]:
    t_l = np.linspace(0, 2.5, 400)
    _, qd_l, _, T_l = trapezoidal_mano(0.0, D, t_l, V, Amax)
    tipo = 'trapecio' if T_l > 2*V/Amax + 1e-9 else 'triangulo (bang-bang)'
    ax.plot(t_l, qd_l, color=col, lw=2, label=f'D = {D}  ->  T = {T_l:.2f} s, {tipo}')
ax.axhline(V, color='grey', ls=':', lw=1)
ax.set_xlabel('t (s)'); ax.set_ylabel('velocidad'); ax.legend(fontsize=8)
ax.set_title('Cuando el crucero desaparece: degeneración a triángulo', fontsize=10)
plt.tight_layout(); plt.show()

print(f'Con v_max = {V} y a_max = {Amax}, la distancia minima para que haya crucero es')
print(f'D = v_max²/a_max = {V**2/Amax:.4f}. Por debajo, el perfil es un triangulo.')"""))

C.append(md("""### Ejercicio 2

Genera con `quintico` una trayectoria de 90 grados en 1,5 s y comprueba si respeta unos límites de accionamiento de 60 grados/s y 90 grados/s². Si no los respeta, encuentra el tiempo mínimo `T` que sí lo hace (usa las fórmulas `v_pico = 15·D/(8T)` y `a_pico = 10·D/(√3·T²)`). Después resuelve el mismo problema con el trapezoidal y compara los dos tiempos. ¿Cuál es más rápido y por qué?"""))

C.append(code("""# Ejercicio 2
D_ej = np.deg2rad(90); V_ej = np.deg2rad(60); A_ej = np.deg2rad(90)
# T_min_quintico = max(15*D_ej/(8*V_ej), np.sqrt(10*D_ej/(np.sqrt(3)*A_ej)))
# ..."""))

# ---------------- 4. Articular frente a cartesiano
C.append(md("""## 4. Movimiento articular frente a movimiento cartesiano

Queda decidir **en qué espacio** se define el camino, y esta es la decisión que un programador de robots toma varias veces al día.

El **movimiento articular** interpola directamente entre configuraciones: se resuelve la IK solo en los dos extremos y `jtraj` genera el quíntico multi-eje coordinado (Corke, 2023, p. 286). Es suave y barato para los accionamientos; a cambio, la punta describe una curva no intuitiva.

El **movimiento cartesiano** impone la recta: `ctraj` interpola la pose entre las dos T extremas (Corke, 2023, p. 287; la interpolación de pose se introdujo en el cap. 3, p. 105) y después cada pose intermedia se convierte a articular con la IK (Corke, 2023, p. 289). Es lo que exigen soldadura, corte o dispensado.

Comparamos los dos sobre un movimiento del PUMA 560 entre dos puntos a la misma altura, fijando la rama de IK para que la comparación sea limpia."""))

C.append(code("""T_ini = SE3(0.5, -0.3, 0.4) * SE3.Ry(np.pi/2)
T_fin = SE3(0.5,  0.3, 0.4) * SE3.Ry(np.pi/2)
RAMA, N = 'ruf', 60

sol_i = puma.ikine_a(T_ini, RAMA)
sol_f = puma.ikine_a(T_fin, RAMA)
print('IK en los extremos:', sol_i.success, sol_f.success)
print('  q inicial (grados):', np.rad2deg(sol_i.q).round(1))
print('  q final   (grados):', np.rad2deg(sol_f.q).round(1))

# --- movimiento articular: quintico multi-eje (Corke, 2023, p. 286) ---
traj_art = jtraj(sol_i.q, sol_f.q, N)
Q_art = traj_art.q

# --- movimiento cartesiano: recta en el espacio + IK punto a punto ---
Ts = ctraj(T_ini, T_fin, N)                       # (Corke, 2023, p. 287)
Q_car = puma.ikine_a(Ts, RAMA).q
Q_car = np.unwrap(Q_car, axis=0)                  # deshace los saltos de +-2*pi

P_art = np.array([puma.fkine(q).t for q in Q_art])
P_car = np.array([puma.fkine(q).t for q in Q_car])
print(f'\\nDesviacion maxima de la punta respecto de la recta ideal:')
print(f'  movimiento articular : {np.abs(P_art[:,0] - 0.5).max()*1000:8.2f} mm')
print(f'  movimiento cartesiano: {np.abs(P_car[:,0] - 0.5).max()*1000:8.2f} mm')"""))

C.append(md("""> **Detalle práctico que vale la clase entera:** la IK analítica devuelve los ángulos envueltos en (−180°, 180°], así que resolver punto a punto puede producir saltos artificiales de 360 grados cuando una articulación cruza esa frontera. `np.unwrap` los deshace. Sin ese paso, la gráfica articular muestra un escalón vertical que **no corresponde a ningún movimiento real del robot** — y es un error muy fácil de cometer y muy difícil de diagnosticar mirando solo la punta."""))

C.append(code("""m_art = np.array([puma.manipulability(q) for q in Q_art])
m_car = np.array([puma.manipulability(q) for q in Q_car])
s = np.linspace(0, 1, N)

fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(13, 3.6))

a1.plot(P_art[:, 1], P_art[:, 0], color=IQS_AZUL, lw=2, label='articular')
a1.plot(P_car[:, 1], P_car[:, 0], color=IQS_VERDE, lw=2, ls='--', label='cartesiano')
a1.set_xlabel('y (m)'); a1.set_ylabel('x (m)'); a1.legend(fontsize=8)
a1.set_title('Camino de la punta (vista en planta)', fontsize=10)

for k in range(6):
    a2.plot(s, np.rad2deg(Q_art[:, k]), color=IQS_AZUL, lw=1.4, alpha=0.8)
    a2.plot(s, np.rad2deg(Q_car[:, k]), color=IQS_VERDE, lw=1.4, ls='--', alpha=0.8)
a2.set_xlabel('s'); a2.set_ylabel('grados')
a2.set_title('Coordenadas articulares\\n(azul articular, verde cartesiano)', fontsize=9)

a3.plot(s, m_art, color=IQS_AZUL, lw=2, label='articular')
a3.plot(s, m_car, color=IQS_VERDE, lw=2, ls='--', label='cartesiano')
a3.set_xlabel('s'); a3.set_ylabel('Yoshikawa m'); a3.legend(fontsize=8)
a3.set_title('Manipulabilidad a lo largo del camino', fontsize=10)
plt.tight_layout(); plt.show()

print(f'Manipulabilidad minima  articular: {m_art.min():.5f}   '
      f'cartesiano: {m_car.min():.5f}')
print(f'Salto articular maximo  articular: {np.abs(np.diff(Q_art, axis=0)).max():.4f} rad   '
      f'cartesiano: {np.abs(np.diff(Q_car, axis=0)).max():.4f} rad')"""))

C.append(md("""**La lectura conjunta, que es el cierre del bloque.** El movimiento articular es suave para los motores y ninguna articulación se sale de rango si los extremos son válidos, pero la punta se desvía varios centímetros de la recta: inaceptable si hay que soldar. El cartesiano clava la recta, pero exige más a las articulaciones y su manipulabilidad cae más, porque el camino impuesto no respeta la geometría cómoda del robot.

En el ejemplo del libro, la trayectoria cartesiana resuelta con IK analítica pasa cerca de la singularidad de muñeca y su manipulabilidad cae casi a cero, mientras que la resuelta con IK numérica la mantiene alta «porque minimiza implícitamente la velocidad de todas las articulaciones» (Corke, 2023, p. 289). En una sola gráfica convergen FK, IK y sus ramas, jacobiano, singularidades, manipulabilidad y generación de trayectorias: todo el contenido de S13 a S19 aplicado a una decisión real de programación.

### Ejercicio 3

Repite la comparación con `T_fin = SE3(0.7, 0.3, 0.15) * SE3.Ry(np.pi/2)` —un punto más bajo y más alejado— y mira qué le pasa a la manipulabilidad de la trayectoria cartesiana. Después resuelve la misma trayectoria cartesiana con `ikine_LM` sembrando cada punto con la solución del anterior y compara las tres curvas de `m`. ¿Cuál mandarías al robot?"""))

C.append(code("""# Ejercicio 3
T_fin2 = SE3(0.7, 0.3, 0.15) * SE3.Ry(np.pi/2)
# ..."""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.** `tau = puma.jacob0(q).T @ w`. En `qn` el par mayor aparece en la **articulación 2, el hombro**, y vale 58,5 N·m; en `qs`, con el brazo estirado, sube a 84,7 N·m — un 45 % más por el mismo kilo colgado. La razón es puramente de brazo de palanca: el hombro soporta el momento de la carga respecto de su eje, y ese momento es la fuerza por la distancia horizontal de la punta al eje. Las tres articulaciones de muñeca ven par exactamente nulo, porque la fuerza pasa por el centro de muñeca y no tiene brazo respecto de sus ejes. Para contrastar, en `qr` (brazo vertical, carga justo encima del eje) el par de hombro cae a 2 N·m: el peso lo aguanta la estructura, no los motores.

La conexión con el bloque 3 es directa y conviene explicitarla: el par que hay que dimensionar en el motor del hombro no es «el par de la carga» sino **el peor caso sobre el espacio de trabajo utilizable**, y `Jᵀ·w` es la herramienta que lo calcula de una vez, para todas las posturas, sin dibujar ningún diagrama de sólido libre. Súmese luego el peso de los propios eslabones y se tiene el dimensionado estático completo.

**Ejercicio 2.** Con `D = 90° = 1.5708 rad`, el quíntico en 1,5 s da `v_pico = 15·D/(8·1.5) = 1.9635 rad/s = 112.5 grados/s` y `a_pico = 10·D/(√3·1.5²) = 4.031 rad/s² = 231 grados/s²`. **Viola los dos límites.** Los tiempos mínimos son:

- por velocidad: `T ≥ 15·D/(8·v_max) = 2.8125` s
- por aceleración: `T ≥ sqrt(10·D/(√3·a_max)) = 2.4495` s

luego manda la velocidad: `T_min ≈ 2.81 s`.

Para el trapezoidal con `v_max = 60°/s` y `a_max = 90°/s²`: `ta = 0.667 s`, distancia de aceleración `20°` por rampa, quedan `50°` de crucero a 60°/s, es decir `0.833 s`. Total `T ≈ 2.17 s`.

El trapezoidal es **claramente más rápido** —2,17 s frente a 2,81 s, un 23 % menos— y la razón es estructural, no un accidente de los números: el trapezoidal mantiene la velocidad en su valor máximo durante todo el crucero, mientras que el quíntico solo la alcanza en un instante y el resto del tiempo va por debajo. Con cotas de velocidad y aceleración dadas, el trapezoidal es el movimiento de tiempo mínimo de su clase (Lynch y Park, 2017, pp. 331-332). Ese es exactamente el motivo de que domine en control de motores.

**Ejercicio 3.** Con el punto final más bajo y alejado, la trayectoria cartesiana obliga al robot a estirarse y su manipulabilidad cae de forma notable a lo largo del camino, con la consiguiente subida de las velocidades articulares en el tramo final. La articular apenas se resiente, porque nunca sale de la «recta» del espacio articular entre dos posturas cómodas.

La versión con `ikine_LM` encadenando semillas es la más interesante: sigue la recta cartesiana igual de bien que la analítica —es la misma restricción geométrica— pero mantiene la manipulabilidad más alta, porque en cada paso el solver arranca de la solución anterior y converge a la raíz más próxima, lo que equivale a minimizar implícitamente el movimiento articular (Corke, 2023, p. 289).

¿Cuál mandaría al robot? Depende de la tarea, y esa es la respuesta correcta: si la punta tiene que describir la recta (soldar, cortar, dispensar), cartesiana con semilla encadenada; si solo hay que ir de A a B esquivando nada en particular (recoger, depositar), articular, que es más rápida y menos exigente. Lo que no se puede hacer es elegir por costumbre."""))

C.append(md("""---

## Para llevarse de esta sesión

`tau = Jᵀ·F` es la segunda vida del jacobiano, y sale de una línea de conservación de potencia. Responde a la vez a «qué pares necesito para empujar con esta fuerza» y a «qué pares necesito para resistir esta carga», así que es la herramienta de dimensionado estático de actuadores — el cierre del círculo que abrió el bloque 3. Y tiene una propiedad que conviene memorizar: **la traspuesta nunca es singular**, la estática no explota donde la cinemática diferencial se rompe.

La dualidad fuerza-velocidad es de esas ideas que, una vez vistas, ya no se olvidan: mismos ejes, semiejes recíprocos. **Las posturas singulares son malas para mover y excelentes para sostener.** La maleta que se lleva con el brazo estirado, la prensa que trabaja con el codo bloqueado y el robot que no consigue seguir una recta cerca del límite de alcance son el mismo fenómeno con tres disfraces.

En trayectorias, la separación entre **camino** y **ley temporal** es lo que permite razonar: el camino decide la geometría (¿recta en el espacio o recta en las articulaciones?), la ley temporal decide la suavidad y el tiempo (¿quíntico o trapezoidal?). Son decisiones independientes y hay que tomarlas por separado, con criterio.

Y el mapa completo del bloque, que es lo que entra en el cuestionario: pose (S13) → cinemática directa (S14-S15) → inversa (S16) → jacobiano (S17) → singularidades y manipulabilidad (S18) → estática y trayectorias (S19). Cinco ecuaciones lo resumen todo: `RᵀR = I` con `det R = +1`; `T = [R p; 0 1]`; `T(q) = e^([S1]q1)···e^([Sn]qn)·M`; `ẋ = J(q)·q̇`; y `tau = Jᵀ(q)·F`.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S19_Estatica_Trayectorias.ipynb', C)
print('escrito S19')
