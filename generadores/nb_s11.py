from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('scipy','scipy'), ('matplotlib','matplotlib')]
C = []

C.append(cabecera(
    "S11", "Actuadores eléctricos: el motor DC de la ecuación al punto de operación", "3",
    "miércoles 7 de octubre de 2026", "1 h",
    "Monta el modelo del motor DC pieza a pieza —ecuación eléctrica, ecuación mecánica y el acoplamiento por Kt y Ke—, deduce de él la curva par-velocidad, encuentra el punto de operación con una carga real y simula el arranque para ver de dónde sale el pico de corriente y por qué el transitorio eléctrico se puede despreciar.",
    "De Silva et al. (2016), cap. 4 — modelo dinámico completo del motor DC y constante de tiempo eléctrica despreciable (p. 91); Corke (2023), cap. 9 — actuadores eléctricos en robótica (p. 334), cadena del accionamiento y par proporcional a corriente (p. 335), fricción viscosa y de Coulomb (p. 336), lazos anidados (p. 342), back-EMF y cota de velocidad (p. 346), sensores de par en la articulación (p. 364), actuador serie-elástico (pp. 367-370).",
    "los apuntes del bloque 3"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
np.set_printoptions(precision=4, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.2)
plt.rcParams['axes.grid'] = True
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('Listo.')"""))

# ---------------- 1. El modelo
C.append(md("""## 1. Tres ecuaciones y una constante que aparece dos veces

«La mayoría de los robots actuales se accionan mediante motores eléctricos rotativos» (Corke, 2023, p. 334), y el modelo mínimo de todos ellos son las tres ecuaciones que escribe De Silva: la mecánica I·θ̈ + D·θ̇ + τ_carga = τ_M, la eléctrica del inducido Ke·θ̇ + La·di/dt + Ra·i = u, y el acoplamiento electromecánico τ_M = Kt·i (De Silva et al., 2016, p. 91). Corke escribe la misma relación de par como τ = Km·i, con Km la constante de par en N·m/A (Corke, 2023, p. 335).

El término Ke·θ̇ es la fuerza contraelectromotriz y es la clave de todo: «un motor que gira actúa como un generador y produce una tensión Vb llamada back EMF que se opone a la corriente que entra al motor... Cuando esta tensión iguala la máxima tensión posible del amplificador de potencia, ya no puede entrar más corriente al motor y el par cae a cero — esto fija una cota superior a la velocidad del motor» (Corke, 2023, p. 346). Empezamos comprobando numéricamente por qué la constante de par y la de back-EMF son el mismo número en unidades del SI, cosa que Corke hace explícita al dar a Km ambas unidades (Corke, 2023, p. 346)."""))

C.append(code("""# --- motor DC de 24 V, tamano tipico de articulacion pequena o rueda de AMR ---
Ra = 2.0          # ohm, resistencia del inducido
La = 1.8e-3       # H, inductancia del inducido
Kt = 0.050        # N*m/A, constante de par
Ke = 0.050        # V*s/rad, constante de back-EMF  (mismo numero en el SI)
Jm = 5.0e-5       # kg*m^2, inercia del rotor
Bv = 5.0e-6       # N*m*s/rad, friccion viscosa (Corke, p. 336)
V_BUS = 24.0      # V, tension maxima del amplificador

tau_e = La / Ra                              # constante de tiempo electrica
tau_m = Ra * Jm / (Kt * Ke + Ra * Bv)        # constante de tiempo mecanica

print(f'Constante de tiempo eléctrica  τ_e = {tau_e*1000:6.2f} ms')
print(f'Constante de tiempo mecánica   τ_m = {tau_m*1000:6.2f} ms')
print(f'Cociente τ_m / τ_e = {tau_m/tau_e:.0f}  ->  el transitorio eléctrico es despreciable'
      ' (De Silva et al., p. 91)')

# --- por que Kt y Ke son el mismo numero: balance de potencia ---
i, w = 3.0, 200.0
P_mecanica = (Kt * i) * w                    # par por velocidad
P_convertida = (Ke * w) * i                  # back-EMF por corriente
print(f'\\nCon i = {i} A y ω = {w} rad/s:')
print(f'  potencia mecánica entregada  = {P_mecanica:.1f} W')
print(f'  potencia eléctrica convertida = {P_convertida:.1f} W')
print('  Son iguales porque no hay dónde perder energía en la conversión: Kt = Ke en el SI.')"""))

# ---------------- 2. Curva par-velocidad
C.append(md("""## 2. La curva par-velocidad

En régimen permanente la corriente ya no cambia, el término La·di/dt desaparece y la ecuación eléctrica se reduce a i = (u − Ke·ω)/Ra. Sustituyendo en τ = Kt·i sale la curva par-velocidad del motor DC a tensión constante, que es una recta: par máximo con el rotor bloqueado, cuando la back-EMF es nula y toda la tensión cae en Ra, y par nulo a la velocidad de vacío ω₀ = u/Ke, cuando la back-EMF iguala la tensión de alimentación y ya no entra corriente (Corke, 2023, p. 346).

Esa recta contiene toda la información de catálogo del motor, y la potencia mecánica —su producto por la velocidad— es una parábola con el máximo justo en el punto medio."""))

C.append(code("""def par_motor(w, u=V_BUS):
    \"\"\"Par en el eje en regimen permanente, descontando la friccion viscosa.\"\"\"
    return Kt * (u - Ke * w) / Ra - Bv * w

def corriente(w, u=V_BUS):
    return (u - Ke * w) / Ra

w0 = V_BUS / Ke                          # velocidad de vacio ideal
tau_bloqueo = Kt * V_BUS / Ra            # par con el rotor bloqueado

print(f'Par de bloqueo      : {tau_bloqueo:.3f} N·m   (corriente {corriente(0):.1f} A)')
print(f'Velocidad de vacío  : {w0:.0f} rad/s = {w0*60/(2*np.pi):.0f} rpm')

w = np.linspace(0, w0, 400)
P_mec = par_motor(w) * w
i_w = corriente(w)
P_ele = V_BUS * i_w
with np.errstate(divide='ignore', invalid='ignore'):
    rend = np.where(P_ele > 1e-9, P_mec / P_ele, 0.0)

k_pmax = int(np.argmax(P_mec))
k_rmax = int(np.argmax(rend))
print(f'Potencia máxima     : {P_mec[k_pmax]:.1f} W a {w[k_pmax]:.0f} rad/s '
      f'({w[k_pmax]/w0*100:.0f} % de la velocidad de vacío)')
print(f'Rendimiento máximo  : {rend[k_rmax]*100:.0f} % a {w[k_rmax]:.0f} rad/s')
print('El punto de máxima potencia y el de máximo rendimiento NO coinciden.')"""))

C.append(code("""fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 3.5))

for u, col, ls in [(24.0, IQS_AZUL, '-'), (16.0, IQS_VERDE, '--'), (8.0, 'crimson', ':')]:
    ww = np.linspace(0, u / Ke, 200)
    a1.plot(ww, par_motor(ww, u), color=col, ls=ls, lw=2, label=f'u = {u:.0f} V')
a1.set_xlabel('velocidad ω [rad/s]'); a1.set_ylabel('par [N·m]')
a1.legend(fontsize=8); a1.set_title('Curva par-velocidad: la back-EMF pone el techo')

a2.plot(w, P_mec, color=IQS_AZUL, lw=2, label='potencia mecánica [W]')
a2.plot(w, rend * 100, color=IQS_VERDE, lw=2, label='rendimiento [%]')
a2.axvline(w[k_pmax], color=IQS_AZUL, ls=':', lw=1.2)
a2.axvline(w[k_rmax], color=IQS_VERDE, ls=':', lw=1.2)
a2.set_xlabel('velocidad ω [rad/s]'); a2.legend(fontsize=8)
a2.set_title('Potencia y rendimiento a 24 V')
plt.tight_layout(); plt.show()"""))

C.append(md("""**Lo que hay que hacer notar en clase.** Bajar la tensión desplaza la recta en paralelo hacia la izquierda: cambia la velocidad de vacío pero no la pendiente, que solo depende de Kt·Ke/Ra. Por eso regular la tensión —lo que hace un puente en H con PWM— es una manera perfectamente razonable de regular la velocidad, y por eso el mismo motor a media tensión conserva casi todo su par a baja velocidad.

El punto de máxima potencia está a la mitad de la velocidad de vacío y con la mitad de la corriente de bloqueo, y es un punto pésimo para trabajar: el rendimiento allí ronda el 50 %, porque la mitad de la energía se disipa en Ra. Un motor bien elegido trabaja mucho más cerca de su velocidad de vacío.

### Ejercicio 1

Comprueba analíticamente que la potencia mecánica es máxima en ω₀/2 y que allí la corriente es la mitad de la de bloqueo. Después duplica `Ra` y vuelve a trazar la curva: ¿cambia la velocidad de vacío? ¿Cambia el par de bloqueo? ¿Y el rendimiento máximo?"""))

C.append(code("""# Ejercicio 1
# pista: P(w) = Kt*(V - Ke*w)*w/Ra  es una parabola invertida en w
"""))

# ---------------- 3. Punto de operacion
C.append(md("""## 3. El punto de operación con una carga

El motor solo, en el vacío, no dice nada útil: gira a ω₀ y ya está. Lo que interesa es dónde se cruza su curva con la de la carga, porque en régimen permanente el par que entrega y el que la carga pide tienen que ser iguales. Ese cruce es el punto de operación, y se encuentra resolviendo una ecuación no lineal en cuanto la carga deja de ser una recta.

Ponemos dos cargas de comportamiento opuesto: una carga de tipo ventilador, cuyo par crece con el cuadrado de la velocidad, y una carga de par constante, que es lo que ve un eje que levanta un peso contra la gravedad."""))

C.append(code("""def carga_ventilador(w):
    \"\"\"Par resistente tipo ventilador o rodadura aerodinamica.\"\"\"
    return 0.050 + 1.2e-6 * w**2

def carga_constante(w):
    \"\"\"Par resistente constante: gravedad sobre un eje.\"\"\"
    return 0.150 * np.ones_like(np.asarray(w, float))

def punto_operacion(carga, u=V_BUS):
    \"\"\"Resuelve par_motor(w) = carga(w) en el rango util de velocidad.\"\"\"
    f = lambda ww: par_motor(ww, u) - float(carga(ww))
    if f(0.0) <= 0:
        return None                       # el motor no arranca contra esa carga
    return brentq(f, 0.0, u / Ke)

for nombre, carga in [('ventilador', carga_ventilador), ('par constante', carga_constante)]:
    w_op = punto_operacion(carga)
    tau_op = par_motor(w_op)
    i_op = corriente(w_op)
    print(f'Carga {nombre:>14}: ω = {w_op:6.1f} rad/s = {w_op*60/(2*np.pi):5.0f} rpm | '
          f'τ = {tau_op:.3f} N·m | i = {i_op:5.2f} A | '
          f'P_mec = {tau_op*w_op:5.1f} W | η = {100*tau_op*w_op/(V_BUS*i_op):.0f} %')

# que pasa si la carga crece hasta pasar del par de bloqueo
print(f'\\nPar de bloqueo disponible: {tau_bloqueo:.3f} N·m')
print('Carga de 0.7 N·m ->', 'arranca' if punto_operacion(lambda w: 0.7) else
      'NO arranca: el motor se cala y consume la corriente de bloqueo')"""))

C.append(code("""fig, ax = plt.subplots(figsize=(6.5, 3.8))
ax.plot(w, par_motor(w), color=IQS_AZUL, lw=2.4, label='motor a 24 V')
ax.plot(w, par_motor(w, 16.0) * (w <= 16/Ke), color=IQS_AZUL, lw=1.2, ls='--', label='motor a 16 V')
ax.plot(w, carga_ventilador(w), color=IQS_VERDE, lw=2, label='carga ventilador')
ax.plot(w, carga_constante(w), color='crimson', lw=2, label='carga de par constante')

for carga, col in [(carga_ventilador, IQS_VERDE), (carga_constante, 'crimson')]:
    wo = punto_operacion(carga)
    ax.plot(wo, par_motor(wo), 'o', color=col, ms=9, zorder=5)
ax.set_xlim(0, w0); ax.set_ylim(0, tau_bloqueo * 1.05)
ax.set_xlabel('velocidad ω [rad/s]'); ax.set_ylabel('par [N·m]')
ax.legend(fontsize=8); ax.set_title('Puntos de operación')
plt.tight_layout(); plt.show()"""))

C.append(md("""**La lectura de estabilidad, que casi nunca se cuenta.** El cruce con el ventilador es estable: si el motor se acelera por encima del punto, la carga pide más par del que el motor da y frena; si se ralentiza, sobra par y acelera. Con la carga de par constante también, porque la recta del motor cae y la carga no sube. El caso peligroso es una carga cuyo par crezca al bajar la velocidad más deprisa que el del motor — ahí el punto de cruce es inestable y el motor se cala. Es la misma pregunta que el estudiante volverá a ver en el bloque 5 con otro vocabulario.

### Ejercicio 2

Con la carga de par constante de 0,15 N·m, ¿qué tensión de alimentación hace falta para girar exactamente a 300 rad/s? Resuélvelo con `brentq` sobre la tensión y comprueba después el resultado despejando a mano de la ecuación de régimen permanente. ¿Qué corriente circula en ese punto y qué te dice sobre el calentamiento del motor?"""))

C.append(code("""# Ejercicio 2
# pista: define g(u) = par_motor(300.0, u) - 0.150 y busca su raiz en u entre 0 y 48 V
"""))

# ---------------- 4. Arranque
C.append(md("""## 4. El arranque, simulado con las dos ecuaciones completas

Hasta aquí todo era régimen permanente. Para ver el arranque hay que integrar el sistema completo de dos estados —corriente y velocidad— y compararlo con el modelo simplificado que se obtiene al despreciar La, que es lo que autoriza De Silva por ser «la constante de tiempo eléctrica típicamente mucho menor que la mecánica» (De Silva et al., 2016, p. 91).

El arranque es también donde vive el peor problema práctico del accionamiento: con el rotor parado no hay back-EMF, así que la corriente inicial es la de bloqueo, u/Ra, muchas veces la nominal."""))

C.append(code("""def modelo_completo(t, x, u, carga):
    \"\"\"Estados x = [i, w]. Sistema de 2.o orden: electrico + mecanico.\"\"\"
    i, w = x
    di = (u - Ra * i - Ke * w) / La
    dw = (Kt * i - Bv * w - float(carga(w))) / Jm
    return [di, dw]

def modelo_reducido(t, x, u, carga):
    \"\"\"Estado x = [w]. Se desprecia La: la corriente sigue instantaneamente a la tension.\"\"\"
    w = x[0]
    i = (u - Ke * w) / Ra
    return [(Kt * i - Bv * w - float(carga(w))) / Jm]

T_FIN = 0.30
te = np.linspace(0, T_FIN, 2000)

sol_c = solve_ivp(modelo_completo, (0, T_FIN), [0.0, 0.0], t_eval=te,
                  args=(V_BUS, carga_ventilador), method='LSODA', rtol=1e-8, atol=1e-10)
sol_r = solve_ivp(modelo_reducido, (0, T_FIN), [0.0], t_eval=te,
                  args=(V_BUS, carga_ventilador), method='LSODA', rtol=1e-8, atol=1e-10)

i_c, w_c = sol_c.y
w_r = sol_r.y[0]
i_r = (V_BUS - Ke * w_r) / Ra

w_final = punto_operacion(carga_ventilador)
print(f'Corriente de pico en el arranque : {i_c.max():.2f} A  '
      f'(la de bloqueo es {V_BUS/Ra:.1f} A)')
print(f'Velocidad final simulada         : {w_c[-1]:.1f} rad/s')
print(f'Punto de operación del apartado 3: {w_final:.1f} rad/s')
k63 = int(np.argmax(w_c >= 0.632 * w_final))
print(f'Tiempo hasta el 63 % de la velocidad final: {te[k63]*1000:.0f} ms')
print(f'Error del modelo reducido: máximo {np.abs(w_c-w_r).max():.1f} rad/s durante el transitorio,'
      f' {abs(w_c[-1]-w_r[-1]):.4f} rad/s en régimen')"""))

C.append(code("""fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 3.5))
a1.plot(te*1000, w_c, color=IQS_AZUL, lw=2.2, label='modelo completo (2 estados)')
a1.plot(te*1000, w_r, color=IQS_VERDE, lw=1.4, ls='--', label='modelo reducido (sin La)')
a1.axhline(w_final, color='crimson', ls=':', lw=1.4, label='punto de operación')
a1.set_xlabel('t [ms]'); a1.set_ylabel('ω [rad/s]'); a1.legend(fontsize=8)
a1.set_title('Arranque: velocidad')

a2.plot(te*1000, i_c, color=IQS_AZUL, lw=2.2, label='modelo completo')
a2.plot(te*1000, i_r, color=IQS_VERDE, lw=1.4, ls='--', label='modelo reducido')
a2.axhline(V_BUS/Ra, color='crimson', ls=':', lw=1.4, label='corriente de bloqueo')
a2.set_xlim(0, 30); a2.set_xlabel('t [ms]'); a2.set_ylabel('corriente [A]')
a2.legend(fontsize=8); a2.set_title('Arranque: corriente (zoom en los 30 primeros ms)')
plt.tight_layout(); plt.show()"""))

C.append(md("""**Dos conclusiones y un aviso.** La primera: el modelo reducido se aparta unos pocos rad/s del completo solo durante los primeros milisegundos, y coincide con él hasta la cuarta cifra en régimen permanente, porque el transitorio eléctrico se extingue mientras el mecánico apenas ha empezado. Ese es exactamente el argumento de De Silva para quedarse con un modelo de primer orden en velocidad, que es el que se usará para sintonizar controladores en los bloques 4 y 5.

La segunda: ese mismo modelo reducido no sirve para dimensionar el accionamiento, porque el pico de corriente que hay que soportar solo aparece en el modelo completo. El aviso, por tanto, es que la simplificación es legítima para control y peligrosa para diseño eléctrico — de ahí que todo amplificador serio arranque con limitación de corriente, que además es la base del lazo interno de la estructura de lazos anidados de Corke (2023, p. 342).

### Ejercicio 3

Añade la fricción de Coulomb que Corke incluye en el modelo realista, τ_f = B·ω + τ_C·signo(ω) con τ_C = 0,02 N·m (Corke, 2023, p. 336), y vuelve a simular el arranque. Observa qué le pasa al inicio del movimiento y calcula la tensión mínima que consigue mover el eje. Explica por qué esta no linealidad es la pesadilla del control de par (Corke, 2023, p. 364)."""))

C.append(code("""# Ejercicio 3: friccion de Coulomb
# def carga_con_coulomb(w):
#     return carga_ventilador(w) + 0.02*np.sign(w)
"""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.** P(ω) = Kt·(V − Ke·ω)·ω/Ra es una parábola con raíces en ω = 0 y ω = ω₀, luego su máximo está en el punto medio ω₀/2; allí la corriente vale (V − Ke·ω₀/2)/Ra = V/(2Ra), la mitad de la de bloqueo. Al duplicar Ra la velocidad de vacío no cambia —solo depende de V y Ke— pero el par de bloqueo se reduce a la mitad, la recta se aplana y la potencia máxima cae a la mitad. El rendimiento máximo también empeora, porque Ra es literalmente el elemento que convierte energía eléctrica en calor: un motor con Ra grande es un motor que se calienta antes de mover nada.

**Ejercicio 2.** Despejando de τ = Kt·(u − Ke·ω)/Ra − B·ω con τ = 0,150 N·m y ω = 300 rad/s sale u = Ra·(τ + B·ω)/Kt + Ke·ω = 2·(0,150 + 0,0015)/0,05 + 15 ≈ 21,1 V, y `brentq` da el mismo número. La corriente en ese punto es (21,1 − 15)/2 ≈ 3,0 A, que disipa unos 18 W solo en Ra: el motor entrega 45 W mecánicos y calienta 18 W, es decir, trabaja en torno al 70 % de rendimiento. Esa disipación, y no el par, es lo que limita el par continuo de catálogo.

**Ejercicio 3.** Con fricción de Coulomb el motor no se mueve hasta que el par supera τ_C: hace falta u > Ra·(τ_C + τ_carga(0))/Kt ≈ 2,8 V solo para despegar, y a velocidades bajas aparece un escalón de par que cambia de signo al cambiar el sentido del movimiento. Para el control de par es una pesadilla porque no es proporcional a la corriente, no es continua en ω = 0 y varía con la temperatura y el desgaste: por mucho que se mida la corriente con precisión, «la fricción y otros efectos enmascaran la señal» (Corke, 2023, p. 364). De ahí que los robots que necesitan control de par de verdad midan el par en la articulación en lugar de deducirlo, o interpongan un elemento elástico de rigidez conocida como en el SEA (Corke, 2023, pp. 367-370)."""))

C.append(md("""---

## Para llevarse de esta sesión

El motor DC es la máquina más didáctica de la mecatrónica porque todo su comportamiento cabe en una recta. Esa recta la dibuja la back-EMF: sin ella el motor absorbería corriente infinita y giraría sin límite, y con ella aparecen de golpe la velocidad de vacío, el par de bloqueo, el amortiguamiento aparente y la relación entre tensión y velocidad. Quien entiende Ke entiende el motor.

La segunda idea es de método: el mismo sistema admite dos modelos y hay que saber cuándo vale cada uno. El de primer orden, con La despreciada, es el correcto para diseñar el control, y lo será en los bloques 4 y 5. El de segundo orden completo es el correcto para dimensionar el amplificador y los conductores, porque el pico de corriente de arranque solo existe en él. Elegir el modelo demasiado simple no es un error de cálculo sino de criterio, y suele costar un puente en H.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S11_Actuadores_Electricos.ipynb', C)
print('escrito S11')
