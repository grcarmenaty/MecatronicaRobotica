from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('scipy','scipy'), ('matplotlib','matplotlib'), ('control','control')]
C = []

C.append(cabecera(
    "S22", "Taller: control PID de una articulación", "5",
    "viernes 30 de octubre de 2026", "2 h",
    "Taller completo sobre una articulación con gravedad: simulador explícito de la planta no lineal, efecto de subir Kp, Ki y Kd por separado, sintonía sistemática por Ziegler-Nichols a partir de la ganancia última, y el problema que estropea cualquier PID bien sintonizado —la saturación del actuador y el windup del integrador— con las dos protecciones canónicas medidas una al lado de la otra.",
    "Lynch y Park (2017), cap. 11 — planta de un eje con gravedad y valores numéricos (pp. 421-422, ecs. 11.19-11.21), ley PID y muelle/amortiguador virtuales (pp. 422-423, ec. 11.23), dinámica del error PD con ζ y ωn (p. 423, ecs. 11.25-11.26), error estacionario con gravedad y límites de Kp (p. 424), cotas de estabilidad de Ki y anti-windup (pp. 424-425, ecs. 11.29-11.30); De Silva et al. (2016), cap. 4 — vigencia industrial del PID (p. 93), derivada sobre la salida (p. 95), orden de sintonía y tabla de efectos (p. 98, tabla 4.1), Ziegler-Nichols (pp. 98-99), windup e integración condicional (pp. 99-100, ec. 4.24), PID discreto (pp. 104-106) y saturación (p. 109).",
    "los apuntes del bloque 5"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
import control as ct
from scipy.optimize import brentq

np.set_printoptions(precision=4, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.2)
plt.rcParams['axes.grid'] = True
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('python-control', ct.__version__, '- listo.')"""))

# ---------------- 1. Planta y simulador
C.append(md("""## 1. La planta del taller y el simulador

El sistema es el eslabón que gira en plano vertical movido por un motor, con la dinámica de Lynch y Park:

`τ = M·θ̈ + m·g·r·cos θ + b·θ̇`

donde `M` es la inercia del eslabón respecto al eje, `m` su masa, `r` la distancia del eje al centro de masas y `b` la fricción viscosa (2017, pp. 421-422, ecs. 11.19-11.21). Usamos **los valores numéricos del libro** para que los resultados del aula sean comparables con las figuras del capítulo 11: `M = 0.5 kg·m²`, `m = 1 kg`, `r = 0.1 m`, `b = 0.1 N·m·s/rad` (Lynch y Park, 2017, p. 422).

Sobre ella, el PID:

`τ = Kp·θe + Ki·∫θe·dt + Kd·θ̇e`,  con `θe = θd − θ`

«La ganancia proporcional Kp actúa como un muelle virtual que intenta reducir el error de posición» y «la ganancia derivativa Kd actúa como un amortiguador virtual» (Lynch y Park, 2017, pp. 422-423, ec. 11.23). Merece la pena recordar en clase que este esquema de los años cuarenta «sigue siendo ampliamente utilizado en la industria hoy en día tras más de 70 años» (De Silva et al., 2016, p. 93).

**Dos detalles de implementación** que el simulador incorpora desde el principio:

- La derivada se calcula **sobre la salida**, no sobre el error, porque la referencia cambia a saltos y su derivada dispararía el mando (De Silva et al., 2016, p. 95). Por eso en el código aparece `− Kd·θ̇`.
- El actuador no es ideal: le ponemos una constante de tiempo `τ_a = 20 ms`, que representa el lazo de corriente del amplificador — el polo eléctrico que en S20 despreciamos. Sin ella la planta sería un segundo orden puro y **ningún** valor de `Kp` la desestabilizaría, cosa que no ocurre en ningún laboratorio del mundo. Esta adición es didáctica y no procede de los libros del bloque (sin cita de libro), pero es la que hace que la sesión se parezca al banco de pruebas.

**Objetivo del taller:** llevar el eslabón de `θ = −π/2` a `θ = 0` con sobreimpulso inferior al 5 % y tiempo de establecimiento por debajo de 1.5 s, primero sin saturación y después con ella."""))

C.append(code("""M, m, r, b, g = 0.5, 1.0, 0.1, 0.1, 9.81   # Lynch y Park, 2017, p. 422
TAU_A = 0.02          # constante de tiempo del actuador (lazo de corriente)
H, T_FIN = 0.001, 6.0 # paso de integración y horizonte
TH0, THD = -np.pi/2, 0.0

def simula(Kp, Ki, Kd, th0=TH0, thd=THD, tau_max=None, antiwindup=None,
           lim_int=0.25, T=T_FIN):
    \"\"\"Planta no lineal + PID discreto por ecuaciones en diferencias
    (De Silva et al., 2016, pp. 104-106). Devuelve un array [t, theta, tau_mandado, integral].
    antiwindup: None | 'cond' (integración condicional) | 'clamp' (límite del integrador).\"\"\"
    th, w, tau, integ = th0, 0.0, 0.0, 0.0
    n = int(T/H)
    log = np.zeros((n, 4))
    for k in range(n):
        e = thd - th
        u = Kp*e + Ki*integ - Kd*w                      # derivada sobre la salida
        u_sat = u if tau_max is None else min(max(u, -tau_max), tau_max)
        if antiwindup == 'cond' and u != u_sat:
            pass                                        # no acumular mientras satura
        else:
            integ += e*H
            if antiwindup == 'clamp':
                integ = min(max(integ, -lim_int), lim_int)
        tau += (u_sat - tau)*H/TAU_A                    # actuador de primer orden
        acc = (tau - b*w - m*g*r*np.cos(th)) / M        # planta no lineal
        w  += acc*H
        th += w*H
        log[k] = (k*H, th, u_sat, integ)
    return log

def metricas(log, th0=TH0, thd=THD, tol=0.02):
    \"\"\"Sobreimpulso [%], tiempo de establecimiento al 2 % [s] y error final [rad].\"\"\"
    t, th = log[:, 0], log[:, 1]
    salto = abs(thd - th0)
    Mp = 100*max(0.0, (th.max() - thd)/salto)
    fuera = np.where(np.abs(th - thd) > tol*salto)[0]
    ts = t[fuera[-1]] if len(fuera) and fuera[-1] < len(t)-1 else np.nan
    return Mp, ts, thd - th[-1]

print(f'Par de gravedad a sostener en theta = 0 : {m*g*r:.3f} N·m')
print(f'Pasos de simulación por ensayo          : {int(T_FIN/H)}')"""))

# ---------------- 2. Efecto de las ganancias
C.append(md("""## 2. Ronda 1: qué hace cada ganancia, una por una

La brújula cualitativa es la tabla de efectos de De Silva: subir `Kp` o `Ki` acelera la respuesta y **degrada la estabilidad**; el derivativo amortigua y permite volver a subir `Kp` — con la advertencia de que son «reglas generales» con excepciones y de que el derivativo solo ayuda hasta cierto límite y con señal poco ruidosa (2016, p. 98, tabla 4.1).

Empezamos por el control **solo proporcional**, que es el que enseña más en menos tiempo."""))

C.append(code("""def theta_equilibrio(Kp):
    \"\"\"Reposo del control P con gravedad: Kp·(thd - th) = m·g·r·cos(th)
    (Lynch y Park, 2017, p. 424).\"\"\"
    return brentq(lambda th: Kp*(THD - th) - m*g*r*np.cos(th), -1.5, 0.5)

fig, ax = plt.subplots(figsize=(9, 3.6))
print(f'{"Kp":>6} {"Mp [%]":>9} {"theta_eq [rad]":>16} {"error de reposo":>17} {"pico a pico a 20 s":>20}')
print('-'*74)
for Kp, col in zip([1, 3, 5, 6], plt.cm.viridis(np.linspace(0, 0.85, 4))):
    lg = simula(Kp, 0, 0)
    Mp, ts, ess = metricas(lg)
    ax.plot(lg[:, 0], lg[:, 1], lw=2, color=col, label=f'Kp = {Kp}')
    largo = simula(Kp, 0, 0, T=20.0)
    ultimo = largo[largo[:, 0] > 19.0, 1]
    th_eq = theta_equilibrio(Kp)
    print(f'{Kp:6.1f} {Mp:9.1f} {th_eq:16.3f} {THD-th_eq:17.3f} {ultimo.max()-ultimo.min():20.3f}')
ax.axhline(THD, color='grey', ls=':', lw=1)
ax.axhline(TH0, color='grey', ls=':', lw=0.7)
ax.set_xlabel('t [s]'); ax.set_ylabel('theta [rad]')
ax.set_title('Solo proporcional: más rápido, más oscilante, y siempre con error')
ax.legend(fontsize=8); plt.tight_layout(); plt.show()"""))

C.append(md("""Dos fenómenos que hay que nombrar en voz alta. Antes, una advertencia sobre la tabla: `metricas` devuelve `nan` en el tiempo de establecimiento cuando la respuesta **no llega a entrar** en la banda del 2 % dentro del horizonte simulado, que es lo que pasa en todos los ensayos de esta primera ronda. Por eso aquí medimos otras dos cosas: el ángulo de reposo teórico y la amplitud pico a pico que queda a los 20 segundos.

**El error estacionario no se va nunca.** El eslabón se para en el ángulo que cumple `Kp·θe = m·g·r·cos θ`, porque sostenerlo exige par y el proporcional solo da par si hay error (Lynch y Park, 2017, p. 424). Subir `Kp` reduce el error —de 0.73 rad a 0.19 rad al pasar de 1 a 5— pero no lo elimina: es una asíntota, no una solución.

**Y hay un techo para `Kp`.** La última columna lo dice sin ambigüedad: con `Kp = 1` la oscilación se ha extinguido casi del todo a los 20 s, con `Kp = 5` se mantiene con amplitud constante —estamos justo en el borde— y con `Kp = 6` crece. El lazo se ha vuelto inestable. Ese techo no aparece en la fórmula del libro —que analiza la planta sin retardo de actuador— sino en el simulador, y es exactamente el fenómeno que en S21 medimos con `ct.margin`: la ganancia última. Aquí la calculamos sobre la planta **linealizada en el punto de destino**: en `θd = 0` la derivada del par de gravedad respecto al ángulo, `−m·g·r·sen θ`, vale cero, así que la gravedad no aporta rigidez y la planta linealizada es simplemente `1/(M·s² + b·s)` en cascada con el actuador."""))

C.append(code("""P_lin = ct.tf([1], [M, b, 0]) * ct.tf([1], [TAU_A, 1])   # planta linealizada en theta = 0
print(P_lin)

Ku, pm, wg, wp = ct.margin(P_lin)
Tu = 2*np.pi/wg
print(f'Ganancia última      Ku = {Ku:.2f}')
print(f'Periodo de oscilación Tu = {Tu:.2f} s   (frecuencia {wg:.2f} rad/s)')
print()
print('Compáralo con el barrido de arriba: Kp = 5 aguanta a duras penas y Kp = 6 ya no.')"""))

C.append(md("""Ahora el **derivativo**, con `Kp` deliberadamente alto (16, tres veces la ganancia última) para que se vea que el amortiguamiento es lo que compra ese margen. La fórmula que hay que usar sale de sustituir la ley PD en la planta sin gravedad: `M·ë + (b+Kd)·ė + Kp·e = 0`, un segundo orden estándar con

`ζ = (b + Kd)/(2·√(Kp·M))`  y  `ωn = √(Kp/M)`

(Lynch y Park, 2017, p. 423, ecs. 11.25-11.26). Imponer amortiguamiento crítico `ζ = 1` da directamente `Kd = 2·√(Kp·M) − b`. Este es el puente exacto con S21: **las ganancias colocan `ζ` y `ωn`**."""))

C.append(code("""KP_TALLER = 16.0
Kd_critico = 2*np.sqrt(KP_TALLER*M) - b
print(f'Kd de amortiguamiento crítico para Kp = {KP_TALLER:.0f} : {Kd_critico:.3f} N·m·s/rad')
print()

fig, ax = plt.subplots(figsize=(9, 3.6))
print(f'{"Kd":>7} {"zeta previsto":>15} {"Mp [%]":>9} {"ts [s]":>9} {"error final":>13}')
print('-'*56)
for Kd, col in zip([0.0, 1.0, Kd_critico/2, Kd_critico, 2*Kd_critico],
                   plt.cm.viridis(np.linspace(0, 0.85, 5))):
    lg = simula(KP_TALLER, 0, Kd)
    Mp, ts, ess = metricas(lg)
    zeta = (b + Kd)/(2*np.sqrt(KP_TALLER*M))
    ax.plot(lg[:, 0], lg[:, 1], lw=2, color=col, label=f'Kd = {Kd:.2f}')
    print(f'{Kd:7.2f} {zeta:15.2f} {Mp:9.1f} {ts:9.2f} {ess:13.3f}')
ax.axhline(THD, color='grey', ls=':', lw=1); ax.set_ylim(-2.0, 1.5)
ax.set_xlabel('t [s]'); ax.set_ylabel('theta [rad]')
ax.set_title(f'PD con Kp = {KP_TALLER:.0f}: el derivativo es lo que hace posible ganancia alta')
ax.legend(fontsize=8); plt.tight_layout(); plt.show()"""))

C.append(md("""Con `Kd = 0` y `Kp = 16` el lazo es un desastre; con el `Kd` crítico, cero sobreimpulso. Pero el error estacionario sigue ahí: **el derivativo no lo toca**, porque en reposo `θ̇ = 0` y su contribución es nula.

Ese error solo lo elimina el **integral**, que «permite par de sostén con error cero, pues basta con que la integral acumulada sea no nula» (Lynch y Park, 2017, p. 424). El precio es que la dinámica del error pasa a tercer orden, `M·e⁽³⁾ + (b+Kd)·ë + Kp·ė + Ki·e = 0`, con una **doble cota** de estabilidad:

`(b + Kd)·Kp/M > Ki > 0`

(Lynch y Park, 2017, pp. 424-425, ecs. 11.29-11.30). Demasiado integrador desestabiliza. Vamos a comprobar que la cota es real."""))

C.append(code("""Ki_max = (b + Kd_critico)*KP_TALLER/M     # Lynch y Park, 2017, p. 425, ec. 11.30
print(f'Cota superior teórica de Ki : {Ki_max:.1f}')
print()

fig, ax = plt.subplots(figsize=(9, 3.6))
print(f'{"Ki":>8} {"Mp [%]":>9} {"ts [s]":>9} {"error final [rad]":>19}')
print('-'*48)
for Ki, col in zip([0.0, 0.5, 2.0, 8.0, 30.0], plt.cm.viridis(np.linspace(0, 0.85, 5))):
    lg = simula(KP_TALLER, Ki, Kd_critico)
    Mp, ts, ess = metricas(lg)
    ax.plot(lg[:, 0], lg[:, 1], lw=2, color=col, label=f'Ki = {Ki}')
    print(f'{Ki:8.1f} {Mp:9.1f} {ts:9.2f} {ess:19.4f}')
ax.axhline(THD, color='grey', ls=':', lw=1)
ax.set_xlabel('t [s]'); ax.set_ylabel('theta [rad]'); ax.set_ylim(-1.8, 0.6)
ax.set_title('El integral mata el error estacionario... y trae sobreimpulso')
ax.legend(fontsize=8); plt.tight_layout(); plt.show()

lg = simula(KP_TALLER, Ki_max, Kd_critico)
print()
print(f'Justo en la cota Ki = {Ki_max:.0f}: Mp = {metricas(lg)[0]:.0f} % -> el lazo ha dejado de servir.')
print('La cota del libro se deduce sin el retardo de actuador, así que en el simulador')
print('el deterioro empieza bastante antes de llegar a ella.')"""))

C.append(md("""### Ejercicio 1

La tabla de De Silva dice que subir `Ki` «acelera la respuesta y degrada la estabilidad» (2016, p. 98, tabla 4.1). En el barrido de arriba, sin embargo, el **tiempo de establecimiento mejora** al pasar de `Ki = 0.5` a `Ki = 2`. ¿Contradice esto la tabla? Repite el barrido midiendo por separado el tiempo hasta entrar en la banda del 5 % y el tiempo hasta el 0.5 %, y explica qué está midiendo cada uno."""))

C.append(code("""# Ejercicio 1
# for Ki in [0, 0.5, 2, 8]:
#     lg = simula(KP_TALLER, Ki, Kd_critico)
#     print(Ki, metricas(lg, tol=0.05), metricas(lg, tol=0.005))"""))

# ---------------- 3. Ziegler-Nichols
C.append(md("""## 3. Ronda 2: sintonía sistemática por Ziegler-Nichols

Hasta aquí hemos sintonizado mirando. El método de Ziegler-Nichols —desarrollado por dos ingenieros de Taylor Instrument en los años cuarenta— obtiene un juego inicial de ganancias con **fórmulas**, a partir de la información de la respuesta a escalón o de la respuesta en frecuencia del sistema (De Silva et al., 2016, pp. 98-99).

Usamos la variante de la **ganancia última**: se sube el proporcional puro hasta que el lazo oscila de forma sostenida, y se anotan la ganancia `Ku` y el periodo de la oscilación `Tu`. Esos dos números los tenemos ya: los ha dado `ct.margin` sobre la planta linealizada, y coinciden con lo que veíamos en el barrido de `Kp`. La tabla clásica es:

| Controlador | Kp | Ti | Td |
|---|---|---|---|
| P | 0.5·Ku | — | — |
| PI | 0.45·Ku | Tu/1.2 | — |
| PID | 0.6·Ku | Tu/2 | Tu/8 |

con `Ki = Kp/Ti` y `Kd = Kp·Td`."""))

C.append(code("""def ziegler_nichols(Ku, Tu, tipo='PID'):
    \"\"\"Tabla clásica de la ganancia última (De Silva et al., 2016, pp. 98-99).\"\"\"
    if tipo == 'P':
        return 0.5*Ku, 0.0, 0.0
    if tipo == 'PI':
        Kp = 0.45*Ku; Ti = Tu/1.2
        return Kp, Kp/Ti, 0.0
    Kp = 0.6*Ku; Ti, Td = Tu/2, Tu/8
    return Kp, Kp/Ti, Kp*Td

fig, ax = plt.subplots(figsize=(9, 3.6))
print(f'{"tipo":>5} {"Kp":>8} {"Ki":>8} {"Kd":>8}  {"Mp [%]":>8} {"ts [s]":>8} {"error final":>13}')
print('-'*66)
for tipo, col in zip(['P', 'PI', 'PID'], [IQS_AZUL, IQS_VERDE, 'crimson']):
    Kp, Ki, Kd = ziegler_nichols(Ku, Tu, tipo)
    lg = simula(Kp, Ki, Kd)
    Mp, ts, ess = metricas(lg)
    ax.plot(lg[:, 0], lg[:, 1], lw=2, color=col, label=f'Z-N {tipo}')
    print(f'{tipo:>5} {Kp:8.2f} {Ki:8.2f} {Kd:8.3f}  {Mp:8.1f} {ts:8.2f} {ess:13.4f}')

ax.axhline(THD, color='grey', ls=':', lw=1)
ax.set_xlabel('t [s]'); ax.set_ylabel('theta [rad]')
ax.set_title('Ziegler-Nichols sobre la articulación con gravedad')
ax.legend(fontsize=8); plt.tight_layout(); plt.show()"""))

C.append(md("""**Interpretación honrada del resultado, que es lo que hay que discutir en clase.** Ziegler-Nichols da un lazo que funciona —el PID elimina el error estacionario y responde deprisa— pero con un sobreimpulso enorme. No es un fallo del método: Z-N está pensado para plantas de proceso autorreguladas y su criterio de diseño clásico es la razón de decaimiento de un cuarto, que es de por sí bastante oscilatoria; sobre una planta con integrador como la nuestra sale todavía más agresivo. **Es un punto de partida, no un punto de llegada**, y el propio De Silva lo presenta como «un juego inicial de ganancias» (2016, pp. 98-99).

El refinamiento a mano es el que ya hemos justificado: `Kp` tan alto como el actuador permita, `Kd` para amortiguamiento crítico, `Ki` el mínimo que quite el error estacionario en un tiempo razonable. Comparemos las dos sintonías contra la especificación del taller."""))

C.append(code("""SINTONIAS = {
    'Ziegler-Nichols PID': ziegler_nichols(Ku, Tu, 'PID'),
    'sintonía del taller': (KP_TALLER, 2.0, Kd_critico),
}

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.6))
print(f'{"sintonía":>22} {"Kp":>7} {"Ki":>7} {"Kd":>7} {"Mp [%]":>8} {"ts [s]":>8} {"|tau| max":>10}')
print('-'*76)
for (nombre, (Kp, Ki, Kd)), col in zip(SINTONIAS.items(), [IQS_VERDE, IQS_AZUL]):
    lg = simula(Kp, Ki, Kd)
    Mp, ts, ess = metricas(lg)
    a1.plot(lg[:, 0], lg[:, 1], lw=2, color=col, label=nombre)
    a2.plot(lg[:, 0], lg[:, 2], lw=2, color=col, label=nombre)
    print(f'{nombre:>22} {Kp:7.2f} {Ki:7.2f} {Kd:7.2f} {Mp:8.1f} {ts:8.2f} {np.abs(lg[:, 2]).max():10.1f}')

a1.axhline(THD, color='grey', ls=':', lw=1)
a1.set_xlabel('t [s]'); a1.set_ylabel('theta [rad]'); a1.set_title('Posición')
a1.legend(fontsize=8)
a2.set_xlabel('t [s]'); a2.set_ylabel('par mandado [N·m]'); a2.set_title('Esfuerzo de control')
plt.tight_layout(); plt.show()

print()
print('Especificación del taller: Mp < 5 % y ts < 1.5 s.')"""))

C.append(md("""Mira la gráfica de la derecha antes de celebrar nada. La sintonía del taller cumple la especificación, sí, pero **pide 25 N·m de pico** a un actuador que tiene que sostener menos de 1 N·m en régimen. Ningún motor real da eso. Ese es el asunto de la segunda parte del taller.

### Ejercicio 2

Aplica Ziegler-Nichols en su variante **PI** y explica por qué, sobre esta planta, el PI es notablemente peor que el PID. Relaciónalo con la fórmula `ζ = (b + Kd)/(2·√(Kp·M))`: ¿qué vale `ζ` cuando `Kd = 0` y `Kp = 0.45·Ku`?"""))

C.append(code("""# Ejercicio 2
# Kp, Ki, Kd = ziegler_nichols(Ku, Tu, 'PI')
# zeta = (b + Kd)/(2*np.sqrt(Kp*M))"""))

# ---------------- 4. Saturacion y windup
C.append(md("""## 4. Ronda 3: el actuador se satura y el integrador se desboca

«Las señales en los lazos de control están siempre limitadas»: los sensores tienen rango de medida y el actuador tiene un tope —una válvula va de cerrada a abierta, y la corriente de un motor DC se limita para no dañar el bobinado ni el acoplamiento—. El efecto colateral es que la saturación «reduce efectivamente la ganancia a amplitudes altas y por tanto ralentiza la respuesta del sistema a las perturbaciones» (De Silva et al., 2016, p. 109).

El problema serio aparece al combinar saturación con término integral. Tal como lo describe De Silva: ante un cambio grande de referencia el término integral empuja la señal de control hasta su límite sin conseguir eliminar el error; la parte integral —proporcional al área bajo la curva de error— **sigue creciendo** mientras dura la saturación, y cuando la referencia ya está al alcance «la señal de control permanece en su límite durante más tiempo antes de deshacerse conforme a los errores negativos»; «la consecuencia es una respuesta con una gran sobreoscilación y un largo tiempo de establecimiento» (2016, pp. 99-100, figs. 4.12-4.13).

Ponemos `τ_max = 1.5 N·m` —un actuador que puede sostener el eslabón con margen, pero no acelerarlo como pedía la sintonía del taller— y subimos `Ki` a 5 para que el fenómeno se vea a escala de gráfico."""))

C.append(code("""TAU_MAX = 1.5
KI_DEMO = 5.0
gan = (KP_TALLER, KI_DEMO, Kd_critico)

lg_ideal = simula(*gan)                              # actuador ilimitado
lg_sat   = simula(*gan, tau_max=TAU_MAX)             # saturado, sin protección

fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(12.5, 3.5))
a1.plot(lg_ideal[:, 0], lg_ideal[:, 1], color=IQS_AZUL, lw=2, label='actuador ideal')
a1.plot(lg_sat[:, 0],   lg_sat[:, 1],   color='crimson', lw=2, label='con saturación')
a1.axhline(THD, color='grey', ls=':', lw=1)
a1.set_xlabel('t [s]'); a1.set_ylabel('theta [rad]'); a1.set_title('Posición'); a1.legend(fontsize=8)

a2.plot(lg_ideal[:, 0], lg_ideal[:, 2], color=IQS_AZUL, lw=2)
a2.plot(lg_sat[:, 0],   lg_sat[:, 2],   color='crimson', lw=2)
a2.axhline(TAU_MAX, color='k', ls='--', lw=1); a2.axhline(-TAU_MAX, color='k', ls='--', lw=1)
a2.set_xlabel('t [s]'); a2.set_ylabel('par [N·m]'); a2.set_title('Mando (líneas negras: el tope)')

a3.plot(lg_ideal[:, 0], lg_ideal[:, 3], color=IQS_AZUL, lw=2)
a3.plot(lg_sat[:, 0],   lg_sat[:, 3],   color='crimson', lw=2)
a3.set_xlabel('t [s]'); a3.set_ylabel('integral del error'); a3.set_title('Aquí está el windup')
plt.tight_layout(); plt.show()

for nombre, lg in [('actuador ideal', lg_ideal), ('con saturación', lg_sat)]:
    Mp, ts, ess = metricas(lg)
    print(f'{nombre:>16}: Mp = {Mp:5.1f} %   ts = {ts:5.2f} s   integral máxima = {np.abs(lg[:, 3]).max():.2f}')"""))

C.append(md("""El panel de la derecha es el que hay que proyectar grande. Con el actuador ideal la integral sube a 0.5 y baja; con saturación llega a 1.2 y tarda en volver, porque durante todo el tramo saturado el controlador **sigue sumando error que no puede corregir**. Cuando el eslabón por fin llega, el integrador ordena seguir empujando y el eslabón se pasa de largo.

Nótese la trampa pedagógica: el par de sostén necesario en `θ = 0` es `m·g·r = 0.98 N·m`, muy por debajo del tope de 1.5 N·m. **El actuador es de sobra suficiente para la tarea**; lo que no es suficiente es para el transitorio que el controlador quiere. El windup no es un problema de dimensionado, es un problema de que el controlador no sabe que su mando no se está ejecutando."""))

# ---------------- 5. Anti-windup
C.append(md("""## 5. Anti-windup: las dos protecciones canónicas, medidas

**Remedio 1 — integración condicional.** «La forma más sencilla de superar el problema es dejar de actualizar la parte integral cuando la señal de control está limitada», para lo cual el controlador «naturalmente tiene que conocer cuáles son los límites» (De Silva et al., 2016, p. 100). En el código es el bloque `if antiwindup == 'cond' and u != u_sat: pass`.

**Remedio 2 — límite del integrador.** El «anti-windup del integrador, que impone un límite a cuánto se permite crecer a la integral del error» (Lynch y Park, 2017, p. 425). En el código, `np.clip` sobre `integ`. El límite hay que elegirlo con criterio: tiene que dejar sitio a la integral que el régimen permanente necesita, que aquí es `m·g·r/Ki = 0.98/5 = 0.20`. Ponemos 0.25.

Existen esquemas más finos: De Silva describe la condición de desaturación que reactiva el integrador «en el momento más temprano posible», cuando la pendiente de la salida del PID se anula (2016, p. 100, ec. 4.24). No lo implementamos, pero conviene mencionarlo."""))

C.append(code("""ensayos = [
    ('sin saturación',            dict(),                                                    IQS_AZUL),
    ('saturado, sin protección',  dict(tau_max=TAU_MAX),                                     'crimson'),
    ('saturado + integr. condic.',dict(tau_max=TAU_MAX, antiwindup='cond'),                  IQS_VERDE),
    ('saturado + límite integral',dict(tau_max=TAU_MAX, antiwindup='clamp', lim_int=0.25),   'darkorange'),
]

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 3.8))
print(f'{"ensayo":>28} {"Mp [%]":>9} {"ts [s]":>9} {"error final":>13} {"int. máx":>10}')
print('-'*74)
for nombre, kw, col in ensayos:
    lg = simula(*gan, **kw)
    Mp, ts, ess = metricas(lg)
    a1.plot(lg[:, 0], lg[:, 1], lw=2, color=col, label=nombre)
    a2.plot(lg[:, 0], lg[:, 3], lw=2, color=col)
    print(f'{nombre:>28} {Mp:9.1f} {ts:9.2f} {ess:13.4f} {np.abs(lg[:, 3]).max():10.2f}')

a1.axhline(THD, color='grey', ls=':', lw=1)
a1.set_xlabel('t [s]'); a1.set_ylabel('theta [rad]'); a1.set_title('Posición')
a1.legend(fontsize=8, loc='lower right')
a2.set_xlabel('t [s]'); a2.set_ylabel('integral del error'); a2.set_title('Integral acumulada')
plt.tight_layout(); plt.show()"""))

C.append(md("""**La conclusión del taller, en una frase:** el anti-windup no acelera el actuador —el tramo saturado dura exactamente lo mismo en las cuatro curvas— pero elimina el sobreimpulso parásito que el integrador ciego añadía. Y fíjate en el detalle que más sorprende a los estudiantes: con integración condicional el lazo saturado se establece **antes** que el lazo sin límite de par. No es magia: la saturación amortigua el transitorio agresivo que la sintonía pedía, y una vez retirado el windup lo que queda es una respuesta más suave.

Es el ejemplo perfecto del principio con el que arrancó el curso en el bloque 1: **el controlador debe modelar también las limitaciones de su propio hardware**. Un PID que ignora su actuador es un PID a medias.

### Ejercicio 3

Baja `τ_max` a 1.0 N·m y repite las cuatro curvas. Después bájalo a 0.9 N·m, por debajo del par de gravedad `m·g·r = 0.98 N·m`. ¿Qué ocurre y por qué no lo arregla ningún anti-windup?"""))

C.append(code("""# Ejercicio 3
# for tm in [1.0, 0.9]:
#     for aw in [None, 'cond', 'clamp']:
#         print(tm, aw, metricas(simula(*gan, tau_max=tm, antiwindup=aw)))"""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.** No hay contradicción: son dos cosas distintas. Con la banda del 5 % el tiempo de establecimiento **empeora** al subir `Ki` (más sobreimpulso, más oscilación: la tabla de De Silva tiene razón); con la banda del 0.5 % **mejora**, porque sin integrador el error estacionario de gravedad es de 0.06 rad y el lazo nunca entra en una banda tan estrecha — el tiempo de establecimiento es infinito por definición. La moraleja de taller es que **el tiempo de establecimiento no significa nada si no se dice la tolerancia**, y que un indicador mal definido puede hacer que un ajuste peor parezca mejor. Es exactamente el tipo de discusión que conviene tener antes de escribir una especificación en un pliego.

**Ejercicio 2.** Z-N PI da `Kp = 0.45·Ku ≈ 2.26` y `Kd = 0`. Entonces `ζ = (b + 0)/(2·√(Kp·M)) = 0.1/(2·√1.13) = 0.047`: prácticamente **sin amortiguamiento**. En el simulador el eslabón llega a pasar por encima del punto más alto y sigue girando: el sobreimpulso medido supera el 200 %. Ocurre porque lo único que amortigua esta planta es la fricción viscosa del eje, que es minúscula, y el integrador aún empuja mientras el eslabón se acerca. En una planta de proceso con constante de tiempo dominante y amortiguamiento propio, el PI de Z-N funciona razonablemente; en un servo mecánico de baja fricción, el término derivativo no es opcional. De ahí la práctica industrial de robots: PD o PID con `Kd` grande, nunca PI.

**Ejercicio 3.** Con `τ_max = 1.0 N·m` el tramo saturado se alarga, el windup empeora en el caso sin protección y las dos protecciones siguen funcionando, aunque el establecimiento se retrasa: el actuador ya no tiene margen para acelerar. Con `τ_max = 0.9 N·m` el sistema **no puede alcanzar la referencia**, porque sostener el eslabón en `θ = 0` requiere 0.98 N·m y el actuador solo da 0.9: se queda parado en el ángulo donde el par máximo iguala el par de gravedad, `cos θ = 0.9/0.98`, es decir unos 23° por debajo. Ningún anti-windup lo arregla porque no es un problema de control sino de **dimensionado del actuador**: el punto de operación deseado está fuera del espacio alcanzable. Es la comprobación que hay que hacer antes de sintonizar nada — y la que en los proyectos se olvida primero."""))

C.append(md("""---

## Para llevarse de esta sesión

Las tres ganancias tienen tres papeles que no se solapan: `Kp` es un **muelle** (rigidez frente al error), `Kd` un **amortiguador** (opone la velocidad, permite subir `Kp`) y `Ki` una **memoria** (el único que puede dar par con error cero). Si un lazo tiene error estacionario, no se arregla con `Kd`; si oscila, no se arregla con `Ki`.

La sintonía no es magia ni es arte: hay fórmulas. `ζ = (b+Kd)/(2√(Kp·M))` y `ωn = √(Kp/M)` colocan la respuesta donde S21 dijo, y las cotas `(b+Kd)·Kp/M > Ki > 0` dicen hasta dónde se puede llegar (Lynch y Park, 2017, pp. 423-425). Ziegler-Nichols da un punto de partida en dos números medibles, `Ku` y `Tu`, y hay que refinarlo casi siempre.

La advertencia de práctica profesional que cierra el capítulo del libro conviene leerla literalmente: «en la práctica, `Ki = 0` para muchos controladores de robots, ya que la estabilidad es primordial» (Lynch y Park, 2017, p. 425). En S24 veremos la alternativa que la industria prefiere al integrador: compensar la gravedad con el modelo en lugar de descubrirla acumulando error.

Y el límite del actuador no es un detalle de implementación: es parte de la planta. El windup es lo que le pasa a un controlador que no lo sabe.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S22_Taller_PID.ipynb', C)
print('escrito S22')
