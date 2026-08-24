from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('scipy','scipy'), ('matplotlib','matplotlib'), ('control','control')]
C = []

C.append(cabecera(
    "S24", "Dinámica del manipulador 2R y control por par calculado", "5",
    "jueves 5 de noviembre de 2026", "1 h",
    "Cierra el bloque pasando de un eje a un brazo: implementa la ecuación del manipulador 2R obtenida por Euler-Lagrange con sus tres términos —matriz de inercia, Coriolis y centrífugas, y gravedad—, comprueba numéricamente sus propiedades, y compara sobre la misma trayectoria un PD articular independiente, un PD con compensación de gravedad y el control por par calculado.",
    "Lynch y Park (2017), cap. 8 — receta de Euler-Lagrange (pp. 272-273, ec. 8.3), ejemplo del 2R plano con gravedad (pp. 273-275, ec. 8.9), forma matricial τ = M(q)·q̈ + c(q,q̇) + g(q) (p. 275, ec. 8.10), estructura lineal en q̈, cuadrática en q̇ y trigonométrica en q (p. 275), términos centrípetos y de Coriolis (p. 276); cap. 11 — control descentralizado y matriz de masas casi diagonal (p. 431), par calculado (p. 429, ec. 11.35), balance experimental (p. 430, fig. 11.19), PID con compensación de gravedad (p. 432, ec. 11.38); Corke (2023), cap. 9 — dinámica inversa (pp. 348-349, ec. 9.11), la gravedad como término dominante (pp. 349-350), matriz de inercia variable con la configuración, factor 2.156 en el PUMA 560 (pp. 352-353), control por dinámica inversa y ganancia unidad (p. 359), dinámica del error desacoplada ë + Kv·ė + Kp·e = 0 (p. 360, ec. 9.17) y requisitos del modelo (p. 360).",
    "los apuntes del bloque 5"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

np.set_printoptions(precision=4, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.2)
plt.rcParams['axes.grid'] = True
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('Listo.')"""))

# ---------------- 1. La ecuacion del manipulador
C.append(md("""## 1. Euler-Lagrange sobre el 2R: los tres términos

La receta lagrangiana tiene cuatro pasos: elegir coordenadas generalizadas `q` —los ángulos articulares—, formar el lagrangiano `L(q, q̇) = K − P` (energía cinética menos potencial) y aplicar

`τ = d/dt(∂L/∂q̇) − ∂L/∂q`

(Lynch y Park, 2017, pp. 272-273, ec. 8.3). Aplicada al 2R plano bajo gravedad con las masas concentradas en los extremos de los eslabones, el álgebra es «directa pero tediosa» (p. 274) y produce `τ1` y `τ2` con todos sus términos (pp. 273-275, ec. 8.9). Lo interesante viene al reagrupar:

`τ = M(q)·q̈ + c(q, q̇) + g(q)`

«donde M(q) es la matriz de masas simétrica definida positiva, c(q, q̇) es el vector que contiene los pares de Coriolis y centrípetos y g(q) es el vector de pares gravitatorios» (Lynch y Park, 2017, p. 275, ec. 8.10).

La estructura es general y conviene enunciarla como tal: «las ecuaciones de movimiento son lineales en q̈, cuadráticas en q̇ y trigonométricas en q. Esto es cierto en general para cadenas serie que contienen articulaciones rotativas, no solo para el robot 2R» (Lynch y Park, 2017, p. 275)."""))

C.append(code("""L1, L2 = 1.0, 1.0        # longitudes de los eslabones [m]
M1, M2 = 1.0, 1.0        # masas puntuales en los extremos [kg]
GRAV = 9.81

def matriz_inercia(q):
    \"\"\"M(q), simétrica y definida positiva (Lynch y Park, 2017, p. 275, ec. 8.10).\"\"\"
    c2 = np.cos(q[1])
    return np.array([[M1*L1**2 + M2*(L1**2 + 2*L1*L2*c2 + L2**2), M2*(L1*L2*c2 + L2**2)],
                     [M2*(L1*L2*c2 + L2**2),                      M2*L2**2]])

def vector_velocidad(q, dq):
    \"\"\"c(q, q̇): términos centrípetos (con q̇i²) y de Coriolis (con q̇1·q̇2),
    Lynch y Park, 2017, p. 276.\"\"\"
    s2 = np.sin(q[1])
    return np.array([-M2*L1*L2*s2*(2*dq[0]*dq[1] + dq[1]**2),
                      M2*L1*L2*s2*dq[0]**2])

def vector_gravedad(q):
    \"\"\"g(q): el único término que no se anula con el robot parado.\"\"\"
    return np.array([(M1 + M2)*L1*GRAV*np.cos(q[0]) + M2*GRAV*L2*np.cos(q[0] + q[1]),
                     M2*GRAV*L2*np.cos(q[0] + q[1])])

def dinamica_inversa(q, dq, ddq):
    \"\"\"Dados configuración, velocidad y aceleración, devuelve los pares necesarios
    (Corke, 2023, pp. 348-349, ec. 9.11).\"\"\"
    return matriz_inercia(q) @ ddq + vector_velocidad(q, dq) + vector_gravedad(q)

q_ext = np.array([0.0, 0.0])        # brazo estirado en horizontal
print('Brazo estirado en horizontal, parado:')
print('  M(q) =\\n', matriz_inercia(q_ext))
print('  g(q) =', vector_gravedad(q_ext), 'N·m   <- solo sostenerse ya cuesta esto')
print('  c(q, 0) =', vector_velocidad(q_ext, np.zeros(2)), ' <- sin velocidad no hay Coriolis')"""))

C.append(md("""**La gravedad primero.** Con el brazo estirado en horizontal y **completamente parado**, el hombro necesita casi 30 N·m. Es la observación de Corke con números del PUMA 560: la gravedad «es generalmente el término dominante» y está presente con el robot inmóvil — sostener el hombro del PUMA en su configuración nominal exige 31.6 N·m (2023, pp. 349-350). Cualquier controlador que no lo sepa empieza perdiendo.

**La matriz de inercia después.** Es simétrica y definida positiva, y —esto es lo que rompe todo lo que hemos supuesto hasta ahora— **depende de la configuración**. Vamos a medir cuánto."""))

C.append(code("""q2 = np.linspace(0, np.pi, 361)
M11 = np.array([matriz_inercia([0.0, x])[0, 0] for x in q2])
M12 = np.array([matriz_inercia([0.0, x])[0, 1] for x in q2])
autoval = np.array([np.linalg.eigvalsh(matriz_inercia([0.0, x])) for x in q2])

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.4))
a1.plot(np.degrees(q2), M11, color=IQS_AZUL, lw=2, label='M11 (inercia vista por el hombro)')
a1.plot(np.degrees(q2), M12, color=IQS_VERDE, lw=2, label='M12 (acoplamiento entre ejes)')
a1.axhline(0, color='grey', ls=':', lw=1)
a1.set_xlabel('ángulo del codo q2 [°]'); a1.set_ylabel('kg·m²'); a1.legend(fontsize=8)
a1.set_title('La inercia cambia con la postura')

a2.plot(np.degrees(q2), autoval[:, 0], color=IQS_AZUL, lw=2, label='autovalor menor')
a2.plot(np.degrees(q2), autoval[:, 1], color=IQS_VERDE, lw=2, label='autovalor mayor')
a2.set_xlabel('ángulo del codo q2 [°]'); a2.set_ylabel('kg·m²'); a2.legend(fontsize=8)
a2.set_title('Ambos positivos siempre: M es definida positiva')
plt.tight_layout(); plt.show()

print(f'M11 va de {M11.min():.2f} a {M11.max():.2f} kg·m²  ->  factor {M11.max()/M11.min():.2f}')
print(f'Autovalor menor mínimo en todo el rango: {autoval[:, 0].min():.3f}  (> 0, definida positiva)')
print(f'Máxima asimetría numérica de M: {max(abs(matriz_inercia([0, x])[0,1] - matriz_inercia([0, x])[1,0]) for x in q2):.1e}')
print()
print('En el PUMA 560, Corke mide una variación de 2.156 para el primer eje (2023, pp. 352-353).')
print('Nuestro 2R sin reductora es aún más extremo: un factor 5.')"""))

C.append(md("""Ese número es el que **rompe el supuesto silencioso de S22**: la planta de una articulación de robot no tiene parámetros constantes. El taller del viernes ajustó `Kd = 2·√(Kp·M) − b` con una `M` fija; si la inercia real varía un factor cinco, ese amortiguamiento crítico solo es crítico en una postura.

Y hay más: los elementos fuera de la diagonal, `M12`, acoplan la aceleración de una articulación con el par en la otra (Corke, 2023, pp. 352-353). Acelerar el codo genera par en el hombro aunque el hombro esté quieto.

**Coriolis y centrífugas.** Los términos cuadráticos tienen nombre y física propia: «los términos cuadráticos que contienen q̇ᵢ² se llaman términos centrípetos, y los que contienen q̇ᵢ·q̇ⱼ con i ≠ j se llaman términos de Coriolis» (Lynch y Park, 2017, p. 276). Separémoslos numéricamente para ver quién aporta qué."""))

C.append(code("""q_med = np.array([0.0, np.pi/3])
casos = [('solo el hombro gira   (dq = [2, 0])', np.array([2.0, 0.0])),
         ('solo el codo gira     (dq = [0, 2])', np.array([0.0, 2.0])),
         ('los dos giran         (dq = [2, 2])', np.array([2.0, 2.0]))]

print(f'{"caso":>38} {"c1 [N·m]":>10} {"c2 [N·m]":>10}')
print('-'*60)
for nombre, dq in casos:
    c = vector_velocidad(q_med, dq)
    print(f'{nombre:>38} {c[0]:10.3f} {c[1]:10.3f}')

print()
print('El primer caso es puramente centrífugo en el eje 2: el codo siente par aunque no se mueva.')
print('El tercero añade el término de Coriolis en el eje 1, que cruza las dos velocidades.')
print('Consecuencia: q̈ = 0 NO significa que las masas no aceleren (Lynch y Park, 2017, p. 276).')"""))

# ---------------- 2. Dinamica directa
C.append(md("""## 2. Dinámica directa: soltar el brazo y ver si la física se conserva

La dinámica inversa responde a «qué pares necesito»; la **directa** responde a «qué hace el robot con estos pares», y es lo que integra cualquier simulador:

`q̈ = M(q)⁻¹·(τ − c(q, q̇) − g(q))`

Antes de usarla para controlar conviene verificarla. La prueba estándar es soltar el brazo desde el reposo **sin pares** y comprobar que la energía mecánica se conserva: si el modelo tiene un signo cambiado o un término perdido, la energía deriva y se ve enseguida."""))

C.append(code("""def dinamica_directa(t, x, tau=np.zeros(2)):
    q, dq = x[:2], x[2:]
    ddq = np.linalg.solve(matriz_inercia(q), tau - vector_velocidad(q, dq) - vector_gravedad(q))
    return np.concatenate([dq, ddq])

def energia(q, dq):
    cinetica = 0.5 * dq @ matriz_inercia(q) @ dq
    potencial = (M1 + M2)*GRAV*L1*np.sin(q[0]) + M2*GRAV*L2*np.sin(q[0] + q[1])
    return cinetica + potencial

t_ev = np.linspace(0, 4, 801)
sol = solve_ivp(dinamica_directa, [0, 4], [0.0, 0.0, 0.0, 0.0], t_eval=t_ev,
                rtol=1e-9, atol=1e-9)
E = np.array([energia(sol.y[:2, i], sol.y[2:, i]) for i in range(sol.y.shape[1])])

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.4))
a1.plot(sol.t, np.degrees(sol.y[0]), color=IQS_AZUL, lw=2, label='hombro q1')
a1.plot(sol.t, np.degrees(sol.y[1]), color=IQS_VERDE, lw=2, label='codo q2')
a1.set_xlabel('t [s]'); a1.set_ylabel('ángulo [°]'); a1.legend(fontsize=8)
a1.set_title('Caída libre del 2R desde la horizontal')

a2.plot(sol.t, E - E[0], color='crimson', lw=2)
a2.set_xlabel('t [s]'); a2.set_ylabel('E(t) − E(0)  [J]')
a2.set_title('Deriva de energía del integrador')
plt.tight_layout(); plt.show()

print(f'Energía inicial            : {E[0]:.6f} J')
print(f'Deriva máxima en 4 s       : {np.abs(E - E[0]).max():.2e} J')
print('La deriva es del orden de la tolerancia del integrador: el modelo conserva la energía.')
print('El movimiento, en cambio, es caótico — es el doble péndulo de manual.')"""))

C.append(md("""### Ejercicio 1

Comprueba que `dinamica_inversa` y `dinamica_directa` son inversas: elige una configuración, una velocidad y una aceleración cualesquiera, calcula el par con la primera, mételo en la segunda y verifica que devuelve la aceleración de partida. Es la prueba de consistencia que hay que hacer **siempre** antes de usar un modelo dinámico para controlar."""))

C.append(code("""# Ejercicio 1
# q = np.array([0.3, -0.7]); dq = np.array([1.0, -2.0]); ddq = np.array([0.5, 1.5])
# tau = dinamica_inversa(q, dq, ddq)
# ..."""))

# ---------------- 3. Control
C.append(md("""## 3. Tres controladores sobre la misma trayectoria

**Opción 1 — control articular independiente.** Replicar en cada eje el PD de S22 sin compartir información entre articulaciones. Es legítimo cuando la dinámica está aproximadamente desacoplada: en robots cartesianos, o «en robots muy reducidos en ausencia de gravedad», donde `M(q)` «es casi diagonal, pues está dominada por las inercias aparentes de los propios motores» (Lynch y Park, 2017, p. 431) — el efecto `G²` que calculamos en S20. Nuestro 2R **no tiene reductora**, así que es el peor caso posible para esta estrategia.

**Opción 2 — PD con compensación de gravedad**, `τ = Kp·e + Kd·ė + ĝ(q)`: solo necesita el término gravitatorio del modelo y es suficiente a velocidades y aceleraciones pequeñas (Lynch y Park, 2017, p. 432, ec. 11.38). Es el compromiso más usado en la industria.

**Opción 3 — par calculado**, `τ = M̂(q)·(q̈d + Kd·ė + Kp·e) + ĥ(q, q̇)` (Lynch y Park, 2017, p. 429, ec. 11.35; Corke, 2023, pp. 359-360, ec. 9.16). «Pertenece a una clase de controladores conocidos como control por dinámica inversa, en los que un sistema no lineal se pone en cascada con su inverso de modo que el sistema completo tiene ganancia unidad» (Corke, 2023, p. 359). Con linealización ideal, la dinámica del error es

`ë + Kd·ė + Kp·e = 0`

**desacoplada e independiente de la configuración** (Corke, 2023, p. 360, ec. 9.17), de modo que las ganancias se eligen con las recetas de segundo orden de S21 y no hay nada que resintonizar cuando el brazo cambia de postura.

Trayectoria de prueba: polinomio quíntico de `q = [0, 0]` a `q = [π/2, −π/2]` en 1 s. Para que la comparación sea justa, los tres controladores usan la misma `ωn = 20 rad/s` con `ζ = 1`; el PD toma sus ganancias multiplicando por la diagonal de la inercia en la postura inicial."""))

C.append(code("""def quintico(t, T, q0, qf):
    \"\"\"Perfil quíntico: posición, velocidad y aceleración deseadas.\"\"\"
    if t >= T:
        return qf.copy(), np.zeros(2), np.zeros(2)
    s = t/T
    return (q0 + (qf - q0)*(10*s**3 - 15*s**4 + 6*s**5),
            (qf - q0)*(30*s**2 - 60*s**3 + 30*s**4)/T,
            (qf - q0)*(60*s - 180*s**2 + 120*s**3)/T**2)

Q0, QF = np.array([0.0, 0.0]), np.array([np.pi/2, -np.pi/2])
WN, ZETA = 20.0, 1.0
KP, KD = WN**2, 2*ZETA*WN                       # dinámica del error deseada
M_NOM = np.diag(np.diag(matriz_inercia(Q0)))    # inercia nominal para el PD desacoplado
KP_PD, KD_PD = M_NOM*KP, M_NOM*KD
H_SIM = 2e-4

def simula(modo, T_tray=1.0, T_sim=2.0, factor_modelo=1.0):
    \"\"\"modo: 'pd' | 'pd+g' | 'par calculado'. factor_modelo escala M̂ y ĥ.\"\"\"
    q, dq = Q0.copy(), np.zeros(2)
    n = int(T_sim/H_SIM)
    log = np.zeros((n, 6))
    for k in range(n):
        t = k*H_SIM
        qd, dqd, ddqd = quintico(t, T_tray, Q0, QF)
        e, de = qd - q, dqd - dq
        if modo == 'pd':
            tau = KP_PD @ e + KD_PD @ de
        elif modo == 'pd+g':
            tau = KP_PD @ e + KD_PD @ de + vector_gravedad(q)
        else:
            tau = factor_modelo*(matriz_inercia(q) @ (ddqd + KD*de + KP*e)
                                 + vector_velocidad(q, dq) + vector_gravedad(q))
        ddq = np.linalg.solve(matriz_inercia(q), tau - vector_velocidad(q, dq) - vector_gravedad(q))
        dq = dq + ddq*H_SIM
        q  = q + dq*H_SIM
        log[k] = (t, e[0], e[1], tau[0], tau[1], np.abs(e).max())
    return log

print(f'Ganancias del PD desacoplado: Kp = {np.diag(KP_PD)} N·m/rad, Kd = {np.diag(KD_PD)} N·m·s/rad')
print(f'Dinámica del error del par calculado: e" + {KD:.0f}·e\\' + {KP:.0f}·e = 0  (wn = {WN:.0f}, zeta = {ZETA:.0f})')"""))

C.append(code("""fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 3.8))
print(f'{"controlador":>18} {"error máx [°]":>15} {"error final [°]":>17} {"|tau| máx [N·m]":>17}')
print('-'*72)
for modo, col in [('pd', 'crimson'), ('pd+g', IQS_VERDE), ('par calculado', IQS_AZUL)]:
    lg = simula(modo)
    a1.plot(lg[:, 0], np.degrees(lg[:, 5]), lw=2, color=col, label=modo)
    a2.plot(lg[:, 0], lg[:, 3], lw=2, color=col, label=modo)
    print(f'{modo:>18} {np.degrees(lg[:, 5]).max():15.3f} {np.degrees(np.abs(lg[-1, 1:3])).max():17.4f} '
          f'{np.abs(lg[:, 3:5]).max():17.1f}')

a1.set_yscale('log')
a1.set_xlabel('t [s]'); a1.set_ylabel('|error| máximo de las dos articulaciones [°]')
a1.set_title('Error de seguimiento (escala logarítmica)'); a1.legend(fontsize=8)
a2.set_xlabel('t [s]'); a2.set_ylabel('par del hombro [N·m]')
a2.set_title('Par del eje 1'); a2.legend(fontsize=8)
plt.tight_layout(); plt.show()"""))

C.append(md("""**Tres órdenes de magnitud.** El par calculado sigue la trayectoria con un error de milésimas de grado; el PD con compensación de gravedad se queda en poco más de un grado; el PD desnudo, en casi tres, y además **no llega nunca** a la referencia: su error final no es cero porque sostener el brazo exige par y el PD solo da par si hay error — es el mismo error estacionario de S22, ahora en dos ejes a la vez.

Mira también el panel derecho: los tres piden pares del mismo orden. El par calculado no gana porque empuje más, gana porque **empuja en el momento correcto**, y ese momento se lo dice el modelo. Es la diferencia entre reaccionar y anticipar. El balance experimental del libro coincide: el par calculado sigue la trayectoria mejor que el feedforward solo y que el feedback solo, y con menos esfuerzo de control que el feedback solo (Lynch y Park, 2017, p. 430, fig. 11.19).

### Ejercicio 2

Repite la comparación con una trayectoria **tres veces más lenta** (`T_tray = 3.0`, `T_sim = 4.0`). ¿Cuánto mejora cada controlador? ¿Sigue mereciendo la pena el modelo completo?"""))

C.append(code("""# Ejercicio 2
# for modo in ['pd', 'pd+g', 'par calculado']:
#     lg = simula(modo, T_tray=3.0, T_sim=4.0)
#     print(modo, np.degrees(lg[:, 5]).max())"""))

# ---------------- 4. El precio del modelo
C.append(md("""## 4. El par calculado no es gratis

Tres facturas, todas de Corke (2023, p. 360):

1. **Exige conocimiento.** Masas, centros de masas, tensores de inercia y fricción de cada eslabón — parámetros que los fabricantes rara vez publican completos y que en la práctica hay que identificar.
2. **Exige cómputo en el lazo.** La dinámica inversa se evalúa en cada periodo de servo, aunque `M̂`, `Ĉ` y `ĝ` pueden refrescarse a menor tasa porque la configuración cambia despacio.
3. **Degrada con la incertidumbre.** Si el modelo no es exacto la inversa no es perfecta y aparece un término de forzamiento en la dinámica del error, que deja de ser homogénea.

Ese tercer punto es el que hay que medir, y es lo que cierra la sesión: ¿cuánto se estropea el par calculado si el modelo se equivoca un 20 %?"""))

C.append(code("""print(f'{"modelo M̂, ĥ":>16} {"error máx [°]":>15} {"error final [°]":>17}')
print('-'*52)
for factor in [1.0, 1.1, 1.2, 0.9, 0.8]:
    lg = simula('par calculado', factor_modelo=factor)
    print(f'{factor:>15.0%} {np.degrees(lg[:, 5]).max():15.3f} '
          f'{np.degrees(np.abs(lg[-1, 1:3])).max():17.4f}')

print()
print('Referencia: el PD desacoplado con el modelo perfecto daba 2.67° de error máximo.')"""))

C.append(md("""El resultado es tranquilizador y hay que subrayarlo: con un error de modelo del 20 % el par calculado **sigue siendo mejor** que un PD con modelo perfecto. La linealización por realimentación no es frágil; degrada de forma suave. Por eso la estrategia sensata en un robot real no es «modelo exacto o nada», sino meter en el controlador todo el modelo que se tenga —empezando por la gravedad, que es el término dominante— y dejar que el feedback se ocupe del resto. Como resume Corke, «en general el uso de prealimentación permite reducir la ganancia de realimentación» (2023, pp. 347-348).

### Ejercicio 3

Implementa la **prealimentación de par puro**: calcular la dinámica inversa a lo largo de la trayectoria **deseada** (con `qd`, `dqd`, `ddqd` en lugar de `q`, `dq`, `ddq`) y sumarle un PD. Su dinámica de error, `M(q*)·ë + Kd·ė + Kp·e = 0`, sigue acoplada por la matriz `M` no diagonal y depende de la configuración (Corke, 2023, p. 359, ec. 9.15). Compáralo con el par calculado y comprueba si la diferencia se nota en esta trayectoria."""))

C.append(code("""# Ejercicio 3
# tau = dinamica_inversa(qd, dqd, ddqd) + KP_PD @ e + KD_PD @ de"""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.** Con `q = [0.3, −0.7]`, `dq = [1, −2]` y `ddq = [0.5, 1.5]`, la dinámica inversa devuelve un par que, sustituido en la directa, reproduce `ddq` con un error de orden `1e-15` — el redondeo de la aritmética en punto flotante. La prueba es trivial de escribir y salva muchas horas: cualquier discrepancia mayor delata un signo, una transposición o un término mal copiado. Conviene además probarla con velocidades altas, porque un error en `c(q, q̇)` solo se manifiesta cuando `q̇` es grande y podría pasar desapercibido en una prueba estática.

**Ejercicio 2.** Con la trayectoria de 3 s: el PD baja de 2.67° a unos 1.6°, el PD con gravedad de 1.20° a 0.14° —una mejora de casi un orden de magnitud— y el par calculado sigue en el nivel del error numérico. La lectura es exactamente la que da el libro: la compensación de gravedad basta «a velocidades y aceleraciones pequeñas» (Lynch y Park, 2017, p. 432), porque los términos de Coriolis y centrípetos escalan con `q̇²` y a velocidad reducida se hacen despreciables, mientras que la gravedad no depende de la velocidad y sigue ahí. Por eso la mayoría de los robots industriales, que se mueven despacio comparados con sus límites dinámicos, funcionan perfectamente con PID más compensación de gravedad. El par calculado se gana el sueldo en robots rápidos, ligeros y de reducción baja.

**Ejercicio 3.** La prealimentación de par puro mejora mucho al PD —queda entre el PD con gravedad y el par calculado— pero no alcanza a este último, y la diferencia crece con la velocidad de la trayectoria. La razón es estructural: la prealimentación evalúa el modelo **fuera del lazo**, en la trayectoria deseada, así que compensa lo que el robot *debería* estar haciendo, no lo que hace. Mientras el seguimiento sea bueno la diferencia es pequeña; en cuanto el robot se desvía —una perturbación, una carga inesperada— el término anticipativo está calculado en el sitio equivocado. El par calculado evalúa el modelo en el estado **medido** y por eso cancela la dinámica real, no la prevista."""))

C.append(md("""---

## Para llevarse de esta sesión

`M(q)·q̈ + C(q,q̇)·q̇ + g(q) = τ` es la ecuación del bloque y de todo lo que viene después. Cada término tiene una firma reconocible: par con el robot **parado** es gravedad; par que crece con el **cuadrado** de la velocidad es centrífugo o de Coriolis; par en un eje cuando acelera **otro** eje son los elementos fuera de la diagonal de `M`.

La planta de una articulación de robot **no tiene parámetros constantes**: en nuestro 2R la inercia vista por el hombro varía un factor cinco con la postura, y en el PUMA 560 un factor 2.156 (Corke, 2023, pp. 352-353). Todo el bloque 5 hasta hoy vivía del supuesto contrario, legítimo solo cuando la reducción es grande — el `G²` de S20.

El par calculado no es más que **poner el modelo dentro del lazo**: cancelar la no linealidad con su inversa para que lo que quede sea la ecuación lineal de segundo orden de S21, sobre la que ya sabemos elegir `ζ` y `ωn`. Y si el modelo no es perfecto, degrada suavemente.

El arco del bloque queda cerrado: física → EDO (S20) → polos y respuesta (S21) → PID y sus límites (S22) → estado y realimentación (S23) → dinámica multiarticular y par calculado (S24). La misma ecuación que hoy hemos derivado será la que los simuladores del bloque 8 integren hacia delante y la que los controladores de los brazos del laboratorio inviertan hacia atrás.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S24_Dinamica_Par_Calculado.ipynb', C)
print('escrito S24')
