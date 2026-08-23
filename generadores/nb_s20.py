from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('scipy','scipy'), ('matplotlib','matplotlib'), ('control','control')]
C = []

C.append(cabecera(
    "S20", "Modelado del motor DC: de la ecuación diferencial a la función de transferencia", "5",
    "miércoles 28 de octubre de 2026", "1 h",
    "Recorre el camino completo del modelado de un accionamiento: escribe la EDO acoplada del motor DC con carga, la simula tal cual, la reduce a primer orden despreciando el transitorio eléctrico, y comprueba con python-control que la función de transferencia resultante tiene los polos y ceros que la física anuncia. Cierra con el efecto de la reductora sobre la inercia vista desde la articulación.",
    "De Silva et al. (2016), cap. 4 — formas del modelo (p. 88), función de transferencia como cociente de polinomios (p. 88, ec. 4.1), forma cero-polo-ganancia (pp. 89-90, ec. 4.3), ecuaciones del motor DC y reducción a primer orden (p. 91, ecs. 4.10-4.15); Lynch y Park (2017), cap. 8 — constante de par (p. 306), malla eléctrica (p. 307, ec. 8.102), Ke y Kt con el mismo valor numérico y desprecio de L·di/dt (p. 308), reductora (p. 309), reducciones de 100 o más (p. 310) e inercia aparente G²·I_rotor (pp. 310-311); Corke (2023), cap. 9 — fuerza contraelectromotriz como amortiguamiento adicional (p. 346) y efecto 1/G y 1/G² de la reducción (p. 348).",
    "los apuntes del bloque 5"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
import control as ct
from scipy.integrate import solve_ivp

np.set_printoptions(precision=4, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.2)
plt.rcParams['axes.grid'] = True
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('python-control', ct.__version__, '- listo.')"""))

# ---------------- 1. La EDO del motor
C.append(md("""## 1. El motor DC con carga: dos dominios, tres ecuaciones

El accionamiento dominante en robótica es el motor de corriente continua con reductora, y su modelo es el punto de partida de todo el bloque. Son tres ecuaciones que se escriben solas si se ordenan por dominio:

- **Acoplamiento electromecánico.** El par es proporcional a la corriente, `τ_M = Kt·i`, con `Kt` la constante de par en N·m/A (Lynch y Park, 2017, p. 306).
- **Malla eléctrica.** `u = Ke·θ̇ + La·di/dt + Ra·i`, donde el primer término es la fuerza contraelectromotriz (De Silva et al., 2016, p. 91, ec. 4.11; la misma ecuación en Lynch y Park, 2017, p. 307, ec. 8.102).
- **Balance mecánico.** `I·θ̈ + D·θ̇ + τ_carga = τ_M`, con `I` la inercia del conjunto rotor-carga y `D` la fricción viscosa (De Silva et al., 2016, p. 91, ec. 4.10).

La fuerza contraelectromotriz merece un minuto de clase: «un motor que gira actúa como un generador y produce una tensión que se opone a la corriente entrante»; cuando esa tensión iguala la máxima del amplificador el par cae a cero —lo que fija la velocidad máxima— y su efecto sobre la dinámica «se parece a una fuente adicional de amortiguamiento» (Corke, 2023, p. 346). En unidades del SI `Ke` (V·s/rad) y `Kt` (N·m/A) tienen **el mismo valor numérico**, porque describen la misma propiedad del motor (Lynch y Park, 2017, p. 308).

El sistema es de **tercer orden**: posición, velocidad y corriente. Empezamos simulándolo entero, sin simplificar nada."""))

C.append(code("""# Motor DC pequeño de servoaccionamiento, valores de catálogo tipicos
Ra   = 1.2        # ohm      resistencia de inducido
La   = 1.5e-3     # H        inductancia de inducido
Kt   = 0.060      # N·m/A    constante de par
Ke   = 0.060      # V·s/rad  constante de fcem (mismo valor: Lynch y Park, 2017, p. 308)
Iner = 5.0e-4     # kg·m²    inercia rotor + carga, reflejada al eje del motor (carga pesada)
D    = 2.0e-5     # N·m·s/rad fricción viscosa
U_NOM = 24.0      # V        tensión nominal del amplificador

def motor3(t, x, u, tau_carga=0.0):
    \"\"\"Modelo completo de tercer orden. x = [theta, omega, i].
    De Silva et al., 2016, p. 91, ecs. 4.10-4.12.\"\"\"
    th, w, i = x
    di = (u - Ke*w - Ra*i) / La
    dw = (Kt*i - D*w - tau_carga) / Iner
    return [w, dw, di]

t_eval = np.linspace(0, 1.0, 2001)
sol = solve_ivp(motor3, [0, 1.0], [0.0, 0.0, 0.0], args=(U_NOM,),
                t_eval=t_eval, rtol=1e-9, atol=1e-12)
th3, w3, i3 = sol.y

print(f'Velocidad en régimen : {w3[-1]:8.1f} rad/s  ({w3[-1]*60/(2*np.pi):.0f} rpm)')
print(f'Corriente en régimen : {i3[-1]:8.3f} A')
print(f'Pico de corriente    : {i3.max():8.3f} A  (en t = {t_eval[i3.argmax()]*1000:.1f} ms)')""" ))

C.append(md("""Fíjate en el pico de corriente del arranque: con el rotor parado no hay fuerza contraelectromotriz, así que la corriente solo la limita `Ra`, y vale `U/Ra`. Es el número que dimensiona el amplificador y el que justifica que en el laboratorio haya un límite de corriente — el mismo límite que en S22 nos saturará el actuador.

Ahora las dos escalas de tiempo del sistema, que son el asunto central de la sesión:

- **Constante de tiempo eléctrica** `τ_e = La/Ra`: lo que tarda la corriente en establecerse con el rotor bloqueado.
- **Constante de tiempo mecánica** `τ_m = I/K1`, con `K1 = (Ke·Kt + Ra·D)/Ra`: lo que tarda la velocidad en establecerse.

El término `Ke·Kt/Ra` dentro de `K1` es exactamente el amortiguamiento eléctrico que describía Corke: la fcem aparece en el modelo mecánico como fricción viscosa añadida, y en este motor es **cien veces mayor** que la fricción mecánica real."""))

C.append(code("""K1 = (Ke*Kt + Ra*D) / Ra       # De Silva et al., 2016, p. 91, ec. 4.14
K2 = Kt / Ra                   # De Silva et al., 2016, p. 91, ec. 4.15

tau_e = La / Ra
tau_m = Iner / K1

print(f'K1 = {K1:.5f} N·m·s/rad   (amortiguamiento eléctrico Ke·Kt/Ra = {Ke*Kt/Ra:.5f}, mecánico D = {D:.5f})')
print(f'K2 = {K2:.5f} N·m/V')
print(f'tau_e = {tau_e*1000:6.2f} ms')
print(f'tau_m = {tau_m*1000:6.2f} ms')
print(f'separación de escalas  tau_m / tau_e = {tau_m/tau_e:.0f}')
print(f'ganancia estática K2/K1 = {K2/K1:.2f} rad/s por voltio  ->  {U_NOM*K2/K1:.0f} rad/s a {U_NOM:.0f} V')"""))

C.append(md("""**Modelo reducido.** Como «la constante de tiempo eléctrica es típicamente mucho menor que la constante de tiempo mecánica, el retardo debido al transitorio eléctrico puede ignorarse», y el tercer orden se derrumba a

`θ̈ = −(K1/I)·θ̇ + (K2/I)·u − (1/I)·τ_carga`

con `K1 = (Ke·Kt + Ra·D)/Ra` y `K2 = Kt/Ra` (De Silva et al., 2016, p. 91, ecs. 4.13-4.15). Lynch y Park llegan al mismo sitio despreciando `L·di/dt`, hipótesis que «se satisface exactamente cuando el motor opera a corriente constante» (2017, p. 308). Superpongamos las dos velocidades."""))

C.append(code("""def motor1(t, x, u, tau_carga=0.0):
    \"\"\"Modelo reducido de primer orden en velocidad. x = [theta, omega].\"\"\"
    th, w = x
    return [w, (-K1*w + K2*u - tau_carga) / Iner]

sol1 = solve_ivp(motor1, [0, 1.0], [0.0, 0.0], args=(U_NOM,),
                 t_eval=t_eval, rtol=1e-9, atol=1e-12)
w1 = sol1.y[1]

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.4))
a1.plot(t_eval, w3, color=IQS_AZUL, lw=2, label='3.er orden (con La)')
a1.plot(t_eval, w1, color=IQS_VERDE, lw=2, ls='--', label='1.er orden (reducido)')
a1.axhline(U_NOM*K2/K1, color='grey', ls=':', lw=1)
a1.axvline(tau_m, color='grey', ls=':', lw=1)
a1.text(tau_m*1.05, 40, 'tau_m', fontsize=8, color='grey')
a1.set_xlabel('t [s]'); a1.set_ylabel('omega [rad/s]'); a1.legend(fontsize=8)
a1.set_title('Velocidad ante escalón de 24 V')

msk = t_eval < 0.02
a2.plot(t_eval[msk]*1000, w3[msk], color=IQS_AZUL, lw=2)
a2.plot(t_eval[msk]*1000, w1[msk], color=IQS_VERDE, lw=2, ls='--')
a2.set_xlabel('t [ms]'); a2.set_title('Los primeros 20 ms: aquí vive tau_e')
plt.tight_layout(); plt.show()

err = np.abs(w3 - w1).max() / w3[-1] * 100
print(f'Discrepancia máxima entre los dos modelos: {err:.2f} % del valor de régimen')"""))

# ---------------- 2. Funcion de transferencia
C.append(md("""## 2. La función de transferencia, polos y ceros

Un sistema lineal admite tres descripciones equivalentes: función de transferencia, forma cero-polo-ganancia y espacio de estados (De Silva et al., 2016, p. 88; la tercera la dejamos para S23). La función de transferencia es el cociente de polinomios en `s` entre las transformadas de la salida y la entrada con condiciones iniciales nulas (De Silva et al., 2016, p. 88, ec. 4.1).

Transformando `I·ω̇ + K1·ω = K2·u` sale de inmediato

`Ω(s)/U(s) = K2/(I·s + K1)`

—un primer orden con constante de tiempo `I/K1` y ganancia estática `K2/K1`— y con la posición como salida se añade un integrador:

`Θ(s)/U(s) = K2/(s·(I·s + K1))`

Ese es el modelo tipo `K/(s·(τ·s+1))` que será la planta del taller de S22. En python-control, `ct.tf(numerador, denominador)`."""))

C.append(code("""G_w  = ct.tf([K2], [Iner, K1])        # Omega(s)/U(s): primer orden
G_th = ct.tf([K2], [Iner, K1, 0])     # Theta(s)/U(s): + integrador
# Modelo completo: Omega(s)/U(s) = Kt / ((La·s + Ra)(I·s + D) + Kt·Ke)
den3 = np.polyadd(np.polymul([La, Ra], [Iner, D]), [0, 0, Kt*Ke])
G_3  = ct.tf([Kt] / den3[0], den3 / den3[0])   # normalizado: coeficientes legibles

print('Velocidad (reducido):'); print(G_w)
print('Posición (reducido):');  print(G_th)
print('Velocidad (3.er orden, normalizado):'); print(G_3)"""))

C.append(md("""La lectura de los polos es el objetivo de la celda siguiente. El modelo reducido en velocidad tiene **un** polo en `−K1/I = −1/τ_m`; el de posición añade un polo **en el origen**, que es el integrador, y por eso la posición no tiene valor de régimen ante un escalón de tensión: el eje sigue girando. El modelo completo tiene **dos** polos reales muy separados: uno prácticamente en `−1/τ_m` y otro perdido en `−1/τ_e`, mil veces más a la izquierda.

Ninguno de los tres tiene ceros: el motor no tiene caminos directos entrada-salida que se cancelen. La forma cero-polo-ganancia `G(s) = K·∏(s−zᵢ)/∏(s−pⱼ)` (De Silva et al., 2016, pp. 89-90, ec. 4.3) es lo que devuelven `ct.poles` y `ct.zeros`."""))

C.append(code("""for nombre, G in [('velocidad reducido', G_w), ('posición reducido', G_th),
                  ('velocidad 3.er orden', G_3)]:
    p = ct.poles(G); z = ct.zeros(G)
    print(f'{nombre:22s} polos = {np.round(p, 2)}   ceros = {z if len(z) else "ninguno"}')

p3 = np.sort_complex(ct.poles(G_3)).real
print()
print(f'Polo lento del modelo completo   : {p3[-1]:9.2f} 1/s   ->  constante de tiempo {-1/p3[-1]*1000:7.2f} ms')
print(f'Polo rápido del modelo completo  : {p3[0]:9.2f} 1/s   ->  constante de tiempo {-1/p3[0]*1000:7.2f} ms')
print(f'Polo del modelo reducido         : {ct.poles(G_w)[0].real:9.2f} 1/s   ->  constante de tiempo {tau_m*1000:7.2f} ms')
print(f'Ganancia estática: completo {ct.dcgain(G_3):.3f}  |  reducido {ct.dcgain(G_w):.3f} rad/s por voltio')"""))

C.append(md("""**Lo que hay que hacer notar en clase.** El polo rápido está tan lejos que su exponencial se ha extinguido cuando la mecánica apenas ha empezado a moverse; despreciarlo es exactamente eso: quitar del modelo un modo que no se ve. Y la ganancia estática coincide hasta el último decimal, porque en régimen permanente `La·di/dt = 0` y las dos ecuaciones son la misma.

### Ejercicio 1

Un compañero propone un motor con la misma mecánica pero **doble resistencia de inducido** (`Ra = 2.4 Ω`). Sin simular, di qué le pasa a `K1`, a `K2`, a la constante de tiempo mecánica y a la velocidad de régimen. Después compruébalo con las celdas de arriba."""))

C.append(code("""# Ejercicio 1: cambia Ra y recalcula K1, K2, tau_m y la velocidad de régimen
Ra_nuevo = 2.4
# K1_nuevo = ...
# K2_nuevo = ...
"""))

# ---------------- 3. tau_e frente a tau_m
C.append(md("""## 3. ¿Cuándo se puede despreciar la dinámica eléctrica?

La simplificación no es un dogma, es una desigualdad: vale mientras `τ_e ≪ τ_m`. Conviene cuantificar el «mucho menor», porque en un motor de bobinado grande, en un accionamiento con inductancias parásitas del cableado o en un motor sin escobillas con mucha inductancia, el cociente se acerca peligrosamente a uno.

Barremos `La` para que `τ_e/τ_m` recorra tres décadas y medimos, para cada valor, el error máximo entre la respuesta del modelo completo y la del reducido."""))

C.append(code("""def error_reduccion(La_val):
    \"\"\"Error máximo relativo entre el modelo completo y el reducido, para una La dada.\"\"\"
    den = np.polyadd(np.polymul([La_val, Ra], [Iner, D]), [0, 0, Kt*Ke])
    G_full = ct.tf([Kt] / den[0], den / den[0])
    t = np.linspace(0, 6*tau_m, 1200)
    _, y_full = ct.step_response(U_NOM*G_full, t)
    _, y_red  = ct.step_response(U_NOM*G_w,    t)
    return np.abs(y_full - y_red).max() / y_red[-1] * 100

cocientes, errores, La_vals = [], [], np.logspace(np.log10(La), np.log10(La*400), 25)
for La_val in La_vals:
    cocientes.append((La_val/Ra) / tau_m)
    errores.append(error_reduccion(La_val))

plt.figure(figsize=(9, 3.4))
plt.loglog(cocientes, errores, 'o-', color=IQS_AZUL, lw=2, ms=4)
plt.axhline(2, color=IQS_VERDE, ls='--', lw=1.5)
plt.text(cocientes[0], 2.3, 'error del 2 %', color=IQS_VERDE, fontsize=9)
plt.xlabel('tau_e / tau_m'); plt.ylabel('error máximo del modelo reducido [%]')
plt.title('El precio de despreciar el transitorio eléctrico')
plt.tight_layout(); plt.show()

for c, e in zip(cocientes[::6], errores[::6]):
    print(f'tau_e/tau_m = {c:8.4f}   ->  error {e:6.2f} %')"""))

C.append(md("""**Regla práctica que sale del gráfico.** Con `τ_e/τ_m` por debajo de 1/50 el error del modelo reducido está en el nivel del ruido de medida y nadie discutirá el modelo de primer orden. Hacia 1/10 el transitorio eléctrico ya se ve —del orden del 7 %— y por encima de 1/4 el sistema de segundo orden pasa a ser **subamortiguado**: la velocidad sobreoscila ante un escalón de tensión, algo que el modelo de primer orden es incapaz de reproducir por construcción. Ahí ya no hay simplificación que valga.

Esto no es una curiosidad académica. Es la razón por la que un accionamiento con **lazo de corriente interno** —el amplificador regula la corriente mucho más rápido que la mecánica— permite al ingeniero de control trabajar toda la vida con el modelo de primer orden y olvidarse de la electricidad. Y es también la razón por la que en S22 añadiremos al simulador del taller un pequeño retardo de actuador: es este mismo polo rápido, el que hoy hemos despreciado, el que pone el límite superior a la ganancia proporcional.

### Ejercicio 2

Busca, con la función `error_reduccion`, el valor de `La` a partir del cual el error del modelo reducido supera el **5 %**. Exprésalo también como cociente `τ_e/τ_m`."""))

C.append(code("""# Ejercicio 2: barrido fino
# for La_val in np.logspace(...):
#     print(La_val, error_reduccion(La_val))"""))

# ---------------- 4. Reductora
C.append(md("""## 4. La reductora: lo que la articulación ve de verdad

El motor casi nunca ataca la articulación en directo, porque su par «es típicamente demasiado bajo para ser útil»; la reductora multiplica el par y divide la velocidad, `ω_red = ω_motor/G` y `τ_red = η·G·τ_motor` con rendimiento `η ≤ 1` (Lynch y Park, 2017, p. 309). Como muchos motores DC pasan de 10 000 rpm en vacío, «las articulaciones de robots suelen llevar reducciones de 100 o más» (Lynch y Park, 2017, p. 310).

El efecto menos intuitivo y más importante para el control es el de las inercias: vista desde la articulación, la inercia del rotor aparece **multiplicada por G²** —la inercia aparente `G²·I_rotor`—, y puede ser del orden de la del propio eslabón o mayor (Lynch y Park, 2017, pp. 310-311). Con reducciones grandes la inercia de cada articulación queda dominada por su propio rotor y la matriz de masas del robot «se hace más diagonal», desacoplando la dinámica (Lynch y Park, 2017, p. 311). Corke lo resume desde el lado de las perturbaciones: la reducción «disminuye la magnitud de los pares de perturbación en 1/G y la variación de inercia y fricción en 1/G²», a costa de coste, peso, fricción y ruido mecánico (2023, p. 348)."""))

C.append(code("""I_rotor   = 1.2e-5    # kg·m²  inercia propia del rotor
I_eslabon = 0.35      # kg·m²  inercia del eslabón, vista en la articulación
eta = 0.85            # rendimiento de la reductora
I_LIM = 2.0           # A, límite de corriente del amplificador

print(f'{"G":>5} {"G²·I_rotor":>12} {"I_eslabón":>11} {"% rotor":>9} {"w_art [rad/s]":>15} {"tau_art [N·m]":>15}')
print('-'*72)
for G in [1, 10, 50, 100, 200]:
    I_ap    = G**2 * I_rotor             # inercia aparente del rotor en la articulación
    frac    = 100 * I_ap / (I_ap + I_eslabon)
    w_max   = (U_NOM*K2/K1) / G          # Lynch y Park, 2017, p. 309: w_red = w_motor/G
    tau_max = eta * G * Kt * I_LIM       # Lynch y Park, 2017, p. 309: tau_red = eta·G·tau_motor
    print(f'{G:5d} {I_ap:12.4f} {I_eslabon:11.4f} {frac:8.1f} % {w_max:15.2f} {tau_max:15.2f}')

print()
print('La columna "% rotor" es la fracción de la inercia total de la articulación que aporta')
print('el propio rotor a través de G² (Lynch y Park, 2017, pp. 310-311).')"""))

C.append(md("""Lee la tabla de arriba abajo. Sin reductora (`G = 1`) la articulación es puro eslabón: el rotor no pinta nada y toda la dinámica depende de la carga —y de la configuración del brazo, que en S24 veremos que cambia la inercia por un factor grande—. Con `G = 100` ya una cuarta parte de la inercia que ve la articulación es rotor, y con `G = 200` es más de la mitad: una fracción creciente de la inercia total es **constante**, no depende de dónde esté el brazo ni de la carga que lleve. Ese es, en una línea, el motivo de que el control articular independiente de S22 funcione en robots industriales muy reducidos y falle en robots rápidos con reducción baja, que es donde S24 necesitará el par calculado.

Fíjate también en las dos últimas columnas: la reducción compra par a cambio de velocidad, exactamente en la proporción `G` (con la pérdida `η` en el par). No hay nada gratis; hay un intercambio.

### Ejercicio 3

Con `G = 100`, calcula la constante de tiempo mecánica **vista desde la articulación** incluyendo la inercia del eslabón reflejada al eje del motor (`I_total_motor = I_rotor + I_eslabon/G²`). Compárala con la `τ_m` de la sección 1 y explica por qué una reductora grande hace el accionamiento *más rápido* aunque el eslabón sea pesado."""))

C.append(code("""# Ejercicio 3
G = 100
# I_total_motor = ...
# tau_m_art = I_total_motor / K1"""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.** Con `Ra` doble: `K2 = Kt/Ra` se **divide por dos** (la mitad de par por voltio) y `K1 = (Ke·Kt + Ra·D)/Ra = Ke·Kt/Ra + D` pasa de 0.00302 a 0.00302/2 aproximadamente, porque el término `D` es despreciable frente a `Ke·Kt/Ra`; es decir, `K1` **también se divide casi por dos**. Consecuencias: la constante de tiempo mecánica `τ_m = I/K1` se **duplica** (el motor es más lento, porque el amortiguamiento eléctrico que lo frenaba también se ha reducido... y sobre todo porque cuesta el doble meter corriente), mientras que la ganancia estática `K2/K1` queda **casi igual**, ya que ambos se dividen por lo mismo. La velocidad de régimen apenas cambia; lo que cambia es el tiempo que tarda en alcanzarla y, sobre todo, el par disponible en el arranque, que se reduce a la mitad. Moraleja de catálogo: la resistencia de inducido no fija la velocidad final, fija la aceleración.

**Ejercicio 2.** El umbral del 5 % se cruza en torno a `La ≈ 13 mH`, es decir unas **nueve veces** la inductancia nominal, lo que corresponde a `τ_e/τ_m ≈ 0.065`. Y para bajar del 2 % hace falta `τ_e/τ_m ≈ 0.024`, o sea que la mecánica sea unas cuarenta veces más lenta que la eléctrica. Este motor lo es por un factor 130, así que estamos cómodos — pero no con tanto margen como sugería la palabra «típicamente» del libro.

**Ejercicio 3.** `I_total_motor = 1.2e-5 + 0.35/100² = 1.2e-5 + 3.5e-5 = 4.7e-5 kg·m²`, frente a los `5.0e-4 kg·m²` que usamos en la sección 1. La constante de tiempo cae de unos 166 ms a unos 16 ms: **diez veces más rápido**. La reductora no ha cambiado el motor ni el eslabón, ha cambiado *quién manda*: la inercia del eslabón, dividida por `G² = 10 000` al reflejarla al eje del motor, casi desaparece. Ese es el mismo fenómeno que la tabla anterior contaba desde el otro lado (multiplicando la del rotor por `G²` al reflejarla a la articulación). Y explica el efecto 1/G² de Corke (2023, p. 348): si la inercia del eslabón cambia con la configuración un factor dos, ese cambio, reflejado al motor, es cuarenta veces menor que la inercia fija del rotor — el motor casi no se entera."""))

C.append(md("""---

## Para llevarse de esta sesión

Modelar es escribir las leyes de cada dominio y **pegarlas por las constantes de acoplamiento**: en el motor DC, `Kt` y `Ke`, que numéricamente son la misma. Todo lo demás es álgebra.

Simplificar un modelo no es hacerlo peor: es **quitar los modos que no se ven**. El transitorio eléctrico se desprecia porque `τ_e ≪ τ_m`, y hoy hemos cuantificado exactamente cuánto cuesta esa decisión — nada mientras la separación de escalas sea de dos órdenes de magnitud, y bastante en cuanto baja de uno.

La función de transferencia no añade física, añade **legibilidad**: un polo en el origen es un integrador, un polo lejano a la izquierda es un modo rápido, y la ganancia estática es el cociente de los términos independientes. Mañana, en S21, esos polos serán lo único que miremos para predecir la forma de la respuesta.

Y la reductora, que parece un detalle mecánico, es en realidad una decisión de control: con `G` grande cada articulación se vuelve una planta casi lineal, casi invariante y casi desacoplada de las demás. Todo el bloque 5 vive de esa aproximación hasta que S24 la rompe.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S20_Modelado_FT.ipynb', C)
print('escrito S20')
