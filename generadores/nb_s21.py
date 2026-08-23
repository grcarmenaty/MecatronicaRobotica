from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('scipy','scipy'), ('matplotlib','matplotlib'), ('control','control')]
C = []

C.append(cabecera(
    "S21", "Respuesta temporal y frecuencial con python-control", "5",
    "jueves 29 de octubre de 2026", "1 h",
    "Estrena python-control sobre el motor de ayer: respuesta al escalón y sus tres indicadores de catálogo (tiempo de subida, sobreoscilación y tiempo de establecimiento), el papel del factor de amortiguamiento, la migración de los polos al cerrar el lazo, y la lectura del diagrama de Bode con sus márgenes de ganancia y de fase.",
    "Lynch y Park (2017), cap. 11 — constante de tiempo y ts ≈ 4·τ (pp. 409-410), forma estándar de segundo orden (p. 410, ec. 11.8), los tres regímenes de amortiguamiento (p. 411), sobreoscilación exacta y los valores de referencia para ζ = 0.1, 0.5 y 0.8 (pp. 412-413), mapa polos-transitorio (p. 412, fig. 11.5) y criterio de estabilidad (p. 424); De Silva et al. (2016), cap. 4 — reglas tr ≈ 1.8/ωn y ts ≈ 4.6/(ζ·ωn) y el papel del control de movimiento (p. 92, fig. 4.8), lazo cerrado Y/R = GcGa/(1+GcGa) (p. 93, ec. 4.16), identificación en frecuencia del disco duro (pp. 88-89, fig. 4.4); documentación de python-control (sin página).",
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

# ---------------- 1. Escalon e indicadores
C.append(md("""## 1. python-control en cinco llamadas, sobre el motor de ayer

Toda la sesión cabe en cinco funciones (python-control docs, sin página):

| Llamada | Qué hace |
|---|---|
| `ct.tf(num, den)` | crea la planta a partir de los coeficientes |
| `ct.step_response(G, t)` | simula la respuesta al escalón unitario |
| `ct.step_info(G)` | devuelve los indicadores: `RiseTime`, `Overshoot`, `SettlingTime`… |
| `ct.poles(G)` / `ct.zeros(G)` | polos y ceros |
| `ct.feedback(L, 1)` | cierra el lazo con realimentación unitaria |

Retomamos el motor de S20 con sus valores numéricos: `I = 5·10⁻⁴ kg·m²`, `K1 = 0.00302 N·m·s/rad`, `K2 = 0.05 N·m/V`. La velocidad es un primer orden puro, y ahí la única cifra que importa es la constante de tiempo: `τ` «es el tiempo en el que el decaimiento exponencial de primer orden ha caído aproximadamente al 37 % de su valor inicial», y el tiempo de establecimiento al 2 % sale de resolver `e^(−t/τ) = 0.02`, que da `3.91·τ`, «aproximadamente 4·τ» (Lynch y Park, 2017, pp. 409-410)."""))

C.append(code("""I, K1, K2 = 5.0e-4, 0.00302, 0.05      # motor de S20
G_w  = ct.tf([K2], [I, K1])            # velocidad: primer orden
G_th = ct.tf([K2], [I, K1, 0])         # posición: + integrador

tau_m = I / K1
t = np.linspace(0, 6*tau_m, 1200)
_, y = ct.step_response(G_w, t)
y_inf = float(ct.dcgain(G_w))

plt.figure(figsize=(9, 3.4))
plt.plot(t, y, color=IQS_AZUL, lw=2)
plt.axhline(y_inf, color='grey', ls=':', lw=1)
plt.axhline(0.632*y_inf, color=IQS_VERDE, ls='--', lw=1.2)
plt.axvline(tau_m, color=IQS_VERDE, ls='--', lw=1.2)
plt.plot([tau_m], [0.632*y_inf], 'o', color=IQS_VERDE, ms=7)
plt.annotate('en t = tau ha subido al 63 %\\n(le falta el 37 %)', xy=(tau_m, 0.632*y_inf),
             xytext=(tau_m*1.4, 0.35*y_inf), fontsize=9, color=IQS_VERDE,
             arrowprops=dict(arrowstyle='->', color=IQS_VERDE))
plt.xlabel('t [s]'); plt.ylabel('omega [rad/s] por voltio')
plt.title('Respuesta al escalón del motor en velocidad')
plt.tight_layout(); plt.show()

info = ct.step_info(G_w)
print(f'tau teórica   = {tau_m:.4f} s')
print(f'RiseTime      = {info["RiseTime"]:.4f} s   (regla 10-90 %: 2.2·tau = {2.2*tau_m:.4f} s)')
print(f'SettlingTime  = {info["SettlingTime"]:.4f} s   (regla del 2 %: 3.91·tau = {3.91*tau_m:.4f} s)')
print(f'Overshoot     = {info["Overshoot"]:.2f} %   (un primer orden nunca sobreoscila)')"""))

C.append(md("""**Comentario de aula.** Que la sobreoscilación salga exactamente cero no es una casualidad numérica: un sistema de primer orden **no puede** sobreoscilar, porque su respuesta es una exponencial monótona. Todo lo que veremos de aquí en adelante —picos, oscilaciones, tiempos de establecimiento largos— necesita al menos dos polos. Por eso el asunto de la sesión es el segundo orden.

Con la posición como salida aparece el integrador y la respuesta al escalón ya no se estabiliza: el eje sigue girando. Compruébalo con los polos antes de simular nada."""))

C.append(code("""print('Polos en velocidad :', np.round(ct.poles(G_w), 3))
print('Polos en posición  :', np.round(ct.poles(G_th), 3), ' <- el 0 es el integrador')
print()
print('Estabilidad (todas las partes reales < 0):')
print('  velocidad :', bool(np.all(ct.poles(G_w).real < 0)))
print('  posición  :', bool(np.all(ct.poles(G_th).real < 0)), ' <- marginalmente estable: hay un polo EN el eje')"""))

# ---------------- 2. Amortiguamiento
C.append(md("""## 2. El amortiguamiento manda

La plantilla universal es el segundo orden en forma estándar

`ë + 2·ζ·ωn·ė + ωn²·e = 0`

que define la frecuencia natural `ωn` y el factor de amortiguamiento `ζ` (Lynch y Park, 2017, p. 410, ec. 11.8). Las raíces del polinomio característico dictan tres regímenes (Lynch y Park, 2017, p. 411):

- **sobreamortiguado** (`ζ > 1`): dos exponenciales reales, manda la más lenta;
- **críticamente amortiguado** (`ζ = 1`): raíz doble en `−ωn`, la respuesta más rápida sin oscilación;
- **subamortiguado** (`ζ < 1`): raíces complejas conjugadas en `−ζωn ± j·ωd`, con `ωd = ωn·√(1−ζ²)`.

En el caso subamortiguado la sobreoscilación tiene fórmula cerrada, `e^(−πζ/√(1−ζ²))·100 %`, con el pico en `tp = π/ωd`; «ζ = 0.1 da una sobreoscilación del 73 %, ζ = 0.5 da el 16 % y ζ = 0.8 da el 1.5 %» (Lynch y Park, 2017, pp. 412-413). Estos tres números merecen memoria. Vamos a comprobarlos."""))

C.append(code("""def sobreoscilacion_teorica(z):
    \"\"\"Mp exacto en %, Lynch y Park, 2017, pp. 412-413.\"\"\"
    return 100*np.exp(-np.pi*z/np.sqrt(1 - z**2)) if z < 1 else 0.0

WN = 5.0
zetas = [0.1, 0.3, 0.5, 0.8, 1.0, 1.6]
t = np.linspace(0, 4, 1600)

plt.figure(figsize=(9, 3.6))
print(f'{"zeta":>6} {"Mp teórico":>12} {"Mp step_info":>14} {"tr [s]":>9} {"1.8/wn":>9} {"ts [s]":>9} {"4.6/(z·wn)":>12}')
print('-'*78)
for z in zetas:
    G = ct.tf([WN**2], [1, 2*z*WN, WN**2])
    _, y = ct.step_response(G, t)
    plt.plot(t, y, lw=2, label=f'zeta = {z}')
    inf = ct.step_info(G)
    ts_regla = 4.6/(z*WN)
    print(f'{z:6.1f} {sobreoscilacion_teorica(z):11.1f} % {inf["Overshoot"]:13.1f} % '
          f'{inf["RiseTime"]:9.3f} {1.8/WN:9.3f} {inf["SettlingTime"]:9.3f} {ts_regla:12.3f}')

plt.axhline(1, color='grey', ls=':', lw=1)
plt.xlabel('t [s]'); plt.ylabel('y'); plt.legend(fontsize=8, ncol=3)
plt.title(f'Respuesta al escalón con wn = {WN} rad/s fija y zeta variable')
plt.tight_layout(); plt.show()"""))

C.append(md("""Tres lecturas para la clase, en este orden:

1. **`ζ` decide la forma, `ωn` decide la escala de tiempo.** Todas las curvas del gráfico tienen la misma `ωn`; lo único que cambia es cuánto oscilan. Si multiplicas `ωn` por dos, la misma curva ocurre en la mitad de tiempo.
2. **Las reglas rápidas de De Silva funcionan, pero son reglas.** `tr ≈ 1.8/ωn` y `ts ≈ 4.6/(ζ·ωn)` (De Silva et al., 2016, p. 92, fig. 4.8) aciertan el orden de magnitud y sirven para el camino inverso —convertir un requisito de tiempo de subida en una `ωn` objetivo—, pero `tr` empeora notablemente cuando `ζ` se aleja de 0.5 y la fórmula de `ts` se degrada para `ζ ≥ 1`. Que los estudiantes vean la discrepancia en la tabla vale más que la advertencia verbal.
3. **El compromiso está a la vista.** Bajar `ζ` acelera la subida y empeora el establecimiento; subirlo hace lo contrario. El punto de diseño clásico está entre 0.7 y 1: sobreoscilación pequeña con el establecimiento más corto posible.

La frase que ordena todo el bloque está en la misma página de De Silva: «el papel del control de movimiento es forzar estas características a cumplir las especificaciones requeridas» (2016, p. 92). En S22 nos tocará forzarlas con un PID.

### Ejercicio 1

Dada `G(s) = 25/(s² + 4s + 25)`, calcula **a mano** `ωn`, `ζ`, la sobreoscilación y el tiempo de establecimiento aproximado. Después verifica con `ct.step_info` y discute las discrepancias."""))

C.append(code("""# Ejercicio 1
G_ej = ct.tf([25], [1, 4, 25])
# wn = ...   zeta = ...   Mp = ...   ts = ...
# print(ct.step_info(G_ej))"""))

# ---------------- 3. Polos y estabilidad
C.append(md("""## 3. Cerrar el lazo: los polos se mueven

El criterio de estabilidad se enuncia en una línea: la dinámica es estable si y solo si **todas las raíces del polinomio característico tienen parte real negativa** (Lynch y Park, 2017, p. 424). Y la geometría de las raíces se traduce directamente a la forma del transitorio: «raíces más a la izquierda en el plano complejo corresponden a tiempos de establecimiento más cortos, y raíces más alejadas del eje real corresponden a mayor sobreoscilación y oscilación», relaciones que «también valen para sistemas de orden superior» (Lynch y Park, 2017, p. 412, fig. 11.5).

Con un controlador proporcional `Gc = Kp` la transferencia en lazo cerrado es `Y/R = Gc·Ga/(1 + Gc·Ga)` (De Silva et al., 2016, p. 93, ec. 4.16), es decir `ct.feedback(Kp*G, 1)`. Al subir `Kp`, los polos se mueven — y en eso consiste todo el control clásico."""))

C.append(code("""KPS = [0.02, 0.1, 0.5, 2.0]
t = np.linspace(0, 4, 1600)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.8))
for Kp, col in zip(KPS, plt.cm.viridis(np.linspace(0, 0.85, len(KPS)))):
    T = ct.feedback(Kp*G_th, 1)
    p = ct.poles(T)
    a1.plot(p.real, p.imag, 'x', ms=10, mew=2, color=col, label=f'Kp = {Kp}')
    _, y = ct.step_response(T, t)
    a2.plot(t, y, lw=2, color=col, label=f'Kp = {Kp}')
    inf = ct.step_info(T)
    print(f'Kp = {Kp:5.2f}  polos = {np.round(p, 2)}   Mp = {inf["Overshoot"]:5.1f} %   ts = {inf["SettlingTime"]:5.2f} s')

a1.axvline(0, color='k', lw=1); a1.axhline(0, color='k', lw=0.5)
a1.set_xlabel('Re'); a1.set_ylabel('Im'); a1.set_title('Polos del lazo cerrado')
a1.legend(fontsize=8)
a2.axhline(1, color='grey', ls=':', lw=1)
a2.set_xlabel('t [s]'); a2.set_title('Respuesta al escalón de posición')
plt.tight_layout(); plt.show()"""))

C.append(md("""Los polos salen del eje real, se hacen complejos y suben en vertical: la parte real se queda **clavada** en `−K1/(2I)` y solo crece la imaginaria. Traducción: subir la ganancia proporcional en esta planta no acelera el establecimiento, solo añade oscilación. Es exactamente el diagnóstico que en S22 nos empujará a añadir el término derivativo, que es el único que puede mover la parte real hacia la izquierda.

Y aquí viene el detalle que enlaza con S20. Con el modelo reducido (dos polos), **por mucho que subas `Kp` el sistema nunca se hace inestable**: los polos suben pero jamás cruzan al semiplano derecho. Eso es un artefacto de haber despreciado la dinámica eléctrica. Repitamos el experimento con el modelo completo de tercer orden, el que sí incluye el polo rápido en `−794`."""))

C.append(code("""# Motor completo de S20 con integrador, normalizado: Theta(s)/U(s)
G_th3 = ct.tf([8e4], [1, 800, 4832, 0])

print(f'{"Kp":>6} {"polos del lazo cerrado":>46} {"estable"}')
print('-'*70)
for Kp in [0.5, 5, 20, 48, 50]:
    p = ct.poles(ct.feedback(Kp*G_th3, 1))
    print(f'{Kp:6.1f}  {str(np.round(p, 2)):>46}  {bool(np.all(p.real < 0))}')

gm, pm, wg, wp = ct.margin(G_th3)
print()
print(f'Ganancia última del modelo de 3.er orden : Kp = {gm:.1f}')
print(f'Frecuencia de la oscilación en ese punto : {wg:.1f} rad/s  ->  periodo {2*np.pi/wg:.3f} s')
print(f'Con el modelo reducido de 2 polos, la ganancia última es infinita: {ct.margin(G_th)[0]}')"""))

C.append(md("""**Este es el mensaje central de la sesión.** El modelo reducido dice que puedes subir la ganancia sin límite; el modelo completo dice que a partir de `Kp ≈ 48` el lazo oscila sin amortiguar y por encima se dispara. La diferencia entre los dos es un polo que en S20 declaramos irrelevante *para la respuesta en lazo abierto* — y lo era. En lazo cerrado, con ganancia alta, ese mismo polo decide la estabilidad.

De ahí la regla que conviene grabar: **un modelo se simplifica para el uso que se le va a dar**. El modelo de primer orden vale para dimensionar el motor; para decidir cuánta ganancia se puede meter, no.

### Ejercicio 2

Demuestra con papel (o con `ct.poles`, barriendo `Kp`) que el lazo cerrado del modelo reducido `Kp·G_th` es estable para **todo** `Kp > 0`, y explica por qué el criterio de Routh-Hurwitz lo permite en un polinomio de segundo grado pero no en uno de tercero."""))

C.append(code("""# Ejercicio 2
# for Kp in np.logspace(-2, 4, 13):
#     print(Kp, ct.poles(ct.feedback(Kp*G_th, 1)))"""))

# ---------------- 4. Bode y margenes
C.append(md("""## 4. La otra cara del mismo modelo: Bode y los márgenes

La respuesta en frecuencia consiste en excitar el sistema con senoides y registrar amplitud y fase. En la práctica industrial es, además de una herramienta de análisis, una **vía de obtención del modelo**: la planta del disco duro de De Silva se identificó midiendo su respuesta en frecuencia y ajustando el modelo sobre las curvas de magnitud y fase (De Silva et al., 2016, pp. 88-89, fig. 4.4), y las dos respuestas —temporal y frecuencial— contienen la misma información, «cualquiera de las dos dará el modelo idéntico» (De Silva et al., 2016, p. 88).

Lo que hay que saber leer en un Bode: pendiente de `−20 dB/década` por cada polo, un pico de resonancia que delata `ζ` pequeño, y la frecuencia hasta la que el sistema sigue a la entrada. Con `ct.bode_plot` es una línea (python-control docs, sin página)."""))

C.append(code("""fig = plt.figure(figsize=(9, 5))
omega = np.logspace(-1, 3.5, 600)
ct.bode_plot([G_w, G_th, G_th3], omega, label=['velocidad (1.er orden)',
                                               'posición (2 polos)',
                                               'posición (3.er orden)'])
plt.tight_layout(); plt.show()

print('Ganancia estática de la velocidad :', float(ct.dcgain(G_w)), 'rad/s por voltio')
print('En posición la magnitud crece sin límite al bajar la frecuencia: es el integrador.')"""))

C.append(md("""Y ahora los **márgenes**, que responden a una pregunta muy concreta del ingeniero: *¿cuánto puedo equivocarme antes de que el lazo se me vuelva inestable?*

- El **margen de ganancia** es el factor por el que se puede multiplicar la ganancia del lazo abierto antes de que el lazo cerrado se haga inestable; se mide en la frecuencia en la que la fase cruza `−180°`.
- El **margen de fase** es el retardo de fase adicional que el lazo tolera antes de desestabilizarse; se mide en la frecuencia de cruce de ganancia (donde la magnitud vale 0 dB).

En python-control, `ct.margin(L)` devuelve `(gm, pm, wg, wp)` con `gm` en **veces** (no en dB) y `pm` en grados; `ct.bode_plot(L, display_margins=True)` los dibuja sobre las curvas. El tratamiento cuantitativo de márgenes queda fuera del alcance de los apuntes del bloque y se remite a la asignatura de control; aquí lo usamos como herramienta de diagnóstico (material docente estándar; sin cita de libro)."""))

C.append(code("""L = 0.5 * G_th3                    # lazo abierto: proporcional + motor completo
gm, pm, wg, wp = ct.margin(L)
print(f'Margen de ganancia : {gm:6.2f} veces  = {20*np.log10(gm):5.1f} dB   (en w = {wg:6.2f} rad/s)')
print(f'Margen de fase     : {pm:6.2f} grados                  (en w = {wp:6.2f} rad/s)')

plt.figure(figsize=(9, 5))
ct.bode_plot(L, np.logspace(-1, 3.5, 800), display_margins=True)
plt.tight_layout(); plt.show()"""))

C.append(md("""Los valores de referencia que maneja la industria son un margen de ganancia de al menos 6 dB (factor 2) y un margen de fase entre 45° y 60°; el lazo de la celda anterior los cumple con holgura, y por eso su respuesta al escalón —la de `Kp = 0.5` en la sección 3— tenía una sobreoscilación del 23 %, alto pero perfectamente estable.

La regla de bolsillo que sí conviene dar en clase: para un segundo orden dominante, **el margen de fase en grados es aproximadamente cien veces el factor de amortiguamiento**, `ζ ≈ PM/100`. Es decir, 45° de margen de fase equivalen a `ζ ≈ 0.45`, o sea un 20 % de sobreoscilación, y 65° equivalen a `ζ ≈ 0.65`, un 7 %. Comprobémoslo midiendo las dos cosas sobre la misma planta."""))

C.append(code("""print(f'{"Kp":>7} {"PM [°]":>8} {"zeta = PM/100":>15} {"Mp predicho":>13} {"Mp medido":>11}')
print('-'*60)
for Kp in [0.2, 0.5, 1.0, 2.0, 5.0]:
    _, pm, _, _ = ct.margin(Kp*G_th3)
    z_est = pm/100
    mp_pred = 100*np.exp(-np.pi*z_est/np.sqrt(1 - z_est**2)) if z_est < 1 else 0.0
    mp_real = ct.step_info(ct.feedback(Kp*G_th3, 1))['Overshoot']
    print(f'{Kp:7.2f} {pm:8.1f} {z_est:15.2f} {mp_pred:12.1f} % {mp_real:10.1f} %')"""))

C.append(md("""La correspondencia no es exacta —la planta no es un segundo orden puro—, pero acierta la tendencia y el orden de magnitud con una sola llamada y sin simular. Ese es el valor de la regla: **decidir en el dominio de la frecuencia y verificar en el del tiempo**.

### Ejercicio 3

Encuentra, con `scipy.optimize.brentq` sobre `ct.margin`, el valor de `Kp` que deja el lazo con **exactamente 45° de margen de fase** para `G_th3`. Después cierra el lazo con ese `Kp` y comprueba con `ct.step_info` la sobreoscilación real. ¿Se cumple la regla `ζ ≈ PM/100`?"""))

C.append(code("""# Ejercicio 3
# f = lambda Kp: ct.margin(Kp*G_th3)[1] - 45
# Kp45 = brentq(f, 0.01, 40)"""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.** Comparando `s² + 4s + 25` con `s² + 2ζωn·s + ωn²`: `ωn = √25 = 5 rad/s` y `2ζωn = 4`, luego `ζ = 0.4`. Sobreoscilación `e^(−π·0.4/√(1−0.16))·100 = 25.4 %`, y `ts ≈ 4.6/(ζ·ωn) = 4.6/2 = 2.3 s`. `ct.step_info` devuelve `Overshoot ≈ 25.3 %` —la fórmula de la sobreoscilación es exacta— y `SettlingTime ≈ 1.71 s`, sensiblemente menor que la regla. La razón: la regla `4.6/(ζωn)` está construida sobre la **envolvente** exponencial `e^(−ζωn·t)`, y da el instante en que la envolvente entra en la banda del 2 %; la señal real puede entrar antes, porque el coseno que la modula pasa por cero. La regla es conservadora, que es como debe ser una regla de diseño.

**Ejercicio 2.** Con el modelo reducido, el polinomio del lazo cerrado es `I·s² + K1·s + K2·Kp`. Para un polinomio de segundo grado, Routh-Hurwitz se reduce a que **todos los coeficientes sean positivos**, y lo son para cualquier `Kp > 0`: no hay forma de desestabilizarlo. Al añadir el tercer polo el polinomio pasa a `s³ + a2·s² + a1·s + a0` y la condición deja de ser solo de signo: exige además `a2·a1 > a0`, un producto que la ganancia rompe en cuanto `Kp` sube lo suficiente. Ese `a2·a1 > a0` es literalmente la ganancia última que hemos medido con `ct.margin` (48.3). Dicho de otro modo: **hacen falta tres polos para que un proporcional pueda desestabilizar un lazo**, y todo sistema físico los tiene si se mira con suficiente resolución.

**Ejercicio 3.** El valor es `Kp ≈ 0.51`. Con él, `ct.step_info` sobre el lazo cerrado da una sobreoscilación en torno al 21-23 %, frente al 20.5 % que predice la regla con `ζ = 0.45`. La coincidencia es buena porque, con esa ganancia, los dos polos lentos del lazo cerrado dominan y el polo rápido en `−794` no participa del transitorio. Si repites el ejercicio con `PM = 20°`, la predicción se degrada: cuanto más se acerca el lazo a la inestabilidad, menos válida es la aproximación de segundo orden dominante."""))

C.append(md("""---

## Para llevarse de esta sesión

Un sistema lineal se lee en sus **polos**: parte real hacia la izquierda es rapidez, parte imaginaria es oscilación, y el semiplano derecho es la ruina. Todo lo demás —sobreoscilación, tiempo de subida, tiempo de establecimiento— son maneras de contar la misma información en el lenguaje del catálogo.

El factor de amortiguamiento `ζ` es el parámetro que hay que llevar en la cabeza, con sus tres anclas: `0.1 → 73 %`, `0.5 → 16 %`, `0.8 → 1.5 %` de sobreoscilación (Lynch y Park, 2017, pp. 412-413). Con esos tres números se estima a ojo cualquier respuesta y se detecta un ajuste sospechoso antes de simular.

Cerrar el lazo **mueve los polos**, y ese movimiento es el diseño. En la planta del motor, la ganancia proporcional solo los sube en vertical: más oscilación y el mismo tiempo de establecimiento. El término derivativo de mañana es el que los mueve a la izquierda.

Y la advertencia que se lleva la sesión: un modelo simplificado puede predecir estabilidad infinita donde el sistema real tiene una ganancia última muy concreta. En S22 mediremos esa ganancia última en el taller y la usaremos, con las fórmulas de Ziegler-Nichols, para sintonizar un PID de verdad.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S21_Respuesta_python_control.ipynb', C)
print('escrito S21')
