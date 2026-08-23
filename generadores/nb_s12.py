from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('scipy','scipy'), ('matplotlib','matplotlib')]
C = []

C.append(cabecera(
    "S12", "Transmisiones, inercia reflejada y selección motor-reductora", "3",
    "jueves 8 de octubre de 2026", "1 h",
    "Convierte la tabla de referencia motor-carga en aritmética ejecutable: inercia reflejada a través de la reductora, relación de transmisión que minimiza el par requerido por acoplamiento de inercias, y una selección motor-reductora completa sobre un ciclo de trabajo real, con sus comprobaciones de par pico, par eficaz, velocidad y relación de inercias.",
    "Corke (2023), cap. 9 — motivación de la reductora y sus inconvenientes (p. 339), tabla de referencia carga-motor (pp. 339-340), inercia total J' = Jm + Jl/G² (p. 340), el hombro del PUMA 560 con G = 107,815 (p. 341), back-EMF y cota de velocidad (p. 346), sensores de par (p. 364), elasticidad de la transmisión (p. 367); De Silva et al. (2016), cap. 1 — jerarquía de decisión MDQ (pp. 7-8). La regla G = √(Jl/Jm) y los márgenes de catálogo son práctica de dimensionado, sin cita de libro.",
    "los apuntes del bloque 3"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
np.set_printoptions(precision=4, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.2)
plt.rcParams['axes.grid'] = True
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('Listo.')"""))

# ---------------- 1. La tabla de referencia
C.append(md("""## 1. Qué le hace la reductora a cada magnitud

La reductora existe por una asimetría: «los motores eléctricos son compactos y eficientes y pueden girar a muy alta velocidad, pero producen un par muy bajo; por ello es común usar una reductora para cambiar velocidad por incremento de par» (Corke, 2023, p. 339). Las cuatro relaciones que hay que saber de memoria son las de la tabla de referencia de Corke para una reducción G:1: el par en el eslabón es G veces el del motor, la velocidad de la carga es la del motor dividida por G, y —el resultado central— la inercia y la fricción viscosa de la carga vistas desde el motor quedan divididas por G², mientras que un par de perturbación en la carga llega al motor dividido por G (Corke, 2023, pp. 339-340).

Que la inercia vaya con G² y la perturbación con G es lo que hace la reductora tan poderosa y tan tramposa a la vez. Lo escribimos como código y lo aplicamos al hombro del PUMA 560, que usa G = 107,815 (Corke, 2023, p. 341)."""))

C.append(code("""def referir_al_motor(G, tau_l=None, w_l=None, J_l=None, tau_pert=None):
    \"\"\"Tabla de referencia carga -> motor para una reduccion G:1 (Corke, pp. 339-340).\"\"\"
    return {'par del motor necesario [N·m]': None if tau_l is None else tau_l / G,
            'velocidad del motor [rad/s]':  None if w_l is None else w_l * G,
            'inercia reflejada [kg·m²]':    None if J_l is None else J_l / G**2,
            'perturbación vista [N·m]':     None if tau_pert is None else tau_pert / G}

G_PUMA = 107.815                  # hombro del PUMA 560 (Corke, p. 341)
J_ESLABON = 3.0                   # kg*m^2, inercia del eslabon y su carga
TAU_PERT = 5.0                    # N*m, perturbacion en el eslabon (contacto, gravedad residual)

for k, v in referir_al_motor(G_PUMA, tau_l=60.0, w_l=2.0, J_l=J_ESLABON, tau_pert=TAU_PERT).items():
    print(f'{k:>32s}: {v:.5f}')

print(f'\\nLa inercia del eslabón, {J_ESLABON} kg·m², el motor la ve como '
      f'{J_ESLABON/G_PUMA**2:.2e} kg·m²:')
print('del mismo orden que la de su propio rotor, en vez de cuatro órdenes por encima.')"""))

# ---------------- 2. Inercia reflejada
C.append(md("""## 2. Inercia reflejada: por qué el motor deja de sentir la carga

La inercia total sobre el eje del motor es J' = Jm + Jl/G², suma de la inercia propia del motor, dato de su hoja de características, y de la inercia de la carga reflejada (Corke, 2023, p. 340). El segundo término es el que cambia con la configuración del robot —un brazo estirado tiene mucha más inercia que uno recogido—, así que con G grande el accionamiento se vuelve insensible a la carga y a sus variaciones. Esa es la razón, y no otra, por la que el control independiente por articulación funciona en la práctica industrial.

Lo dibujamos con la inercia del eslabón variando entre dos configuraciones extremas, que es la situación real de cualquier brazo."""))

C.append(code("""Jm = 1.0e-4                       # kg*m^2, inercia del rotor de un servo pequeno
JL_MIN, JL_MAX = 0.6, 3.0         # brazo recogido / brazo estirado

G = np.logspace(0, 2.7, 300)      # de 1:1 a 500:1
J_tot_min = Jm + JL_MIN / G**2
J_tot_max = Jm + JL_MAX / G**2

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 3.5))
a1.loglog(G, J_tot_max, color=IQS_AZUL, lw=2, label='brazo estirado (Jl = 3,0)')
a1.loglog(G, J_tot_min, color=IQS_VERDE, lw=2, label='brazo recogido (Jl = 0,6)')
a1.axhline(Jm, color='crimson', ls='--', lw=1.4, label='inercia del rotor Jm')
a1.axvline(G_PUMA, color='black', ls=':', lw=1.2)
a1.set_xlabel('relación de reducción G'); a1.set_ylabel("J' [kg·m²]")
a1.legend(fontsize=8); a1.set_title("Inercia total en el eje del motor J' = Jm + Jl/G²")

variacion = 100 * (J_tot_max - J_tot_min) / J_tot_min
a2.semilogx(G, variacion, color=IQS_AZUL, lw=2)
a2.axhline(20, color='crimson', ls='--', lw=1.4, label='20 % de variación')
a2.axvline(G_PUMA, color='black', ls=':', lw=1.2, label=f'G del PUMA = {G_PUMA:.0f}')
a2.set_xlabel('relación de reducción G'); a2.set_ylabel('variación de J\\' [%]')
a2.legend(fontsize=8); a2.set_title('Cuánto cambia la planta al mover el brazo')
plt.tight_layout(); plt.show()

for g in [1, 10, 50, 107.815, 300]:
    jmin, jmax = Jm + JL_MIN/g**2, Jm + JL_MAX/g**2
    print(f'G = {g:7.2f} -> J\\' entre {jmin:.2e} y {jmax:.2e} kg·m²  '
          f'(varía un {100*(jmax-jmin)/jmin:8.1f} %)')"""))

C.append(md("""**Lo que hay que hacer notar en clase.** Sin reductora la planta que ve el controlador cambia en un factor cinco al mover el brazo, y ninguna sintonía fija sirve para las dos configuraciones. Con la reducción del PUMA la variación se queda en poco más del doble, y a partir de G ≈ 300 baja del veinticinco por ciento: es entonces cuando un PID de ganancias fijas por articulación funciona razonablemente en todo el espacio de trabajo.

Nada de esto es gratis: «la desventaja de una reductora es el aumento de coste, peso, fricción, holgura (backlash), ruido mecánico y, para los engranajes armónicos, rizado de par», y por eso «los robots de muy altas prestaciones, como los usados en ensamblado electrónico de alta velocidad, usan motores caros de alto par con accionamiento directo o relación de reducción muy baja» (Corke, 2023, p. 339). A ello se añade la elasticidad que la transmisión introduce y que limita el ancho de banda de control (Corke, 2023, p. 367).

### Ejercicio 1

Con G = 1 (accionamiento directo) y con G = 100, calcula cuánto par de motor hace falta para rechazar una perturbación de 5 N·m aplicada en el eslabón, y cuánta aceleración de la carga produce esa perturbación si el motor no reacciona. ¿Por qué se dice que la reductora «esconde» la carga, y qué se pierde a cambio en un robot que debe detectar un contacto con una persona?"""))

C.append(code("""# Ejercicio 1
# pista: la perturbacion se refiere dividida por G, pero la inercia lo hace dividida por G^2
"""))

# ---------------- 3. G optima
C.append(md("""## 3. La relación de transmisión que minimiza el par requerido

Aquí aparece el compromiso que da sentido a todo el apartado. El par que el motor debe entregar para acelerar la articulación tiene dos términos que tiran en direcciones opuestas: acelerar su propio rotor, que exige más par cuanto mayor es G porque el rotor debe girar G veces más deprisa, y vencer el par de la carga referido, que exige menos par cuanto mayor es G. La suma tiene un mínimo.

τ_motor(G) = Jm·G·α + (Jl·α + τ_g)/G, donde α es la aceleración angular de la carga y τ_g el par de gravedad o proceso. Derivando e igualando a cero sale G* = √((Jl + τ_g/α)/Jm), que sin par externo se reduce a la regla clásica de adaptación de inercias G* = √(Jl/Jm) — coherente con la tabla de Corke pero no formulada en nuestros textos, así que se declara como práctica de dimensionado, sin cita de libro."""))

C.append(code("""ALFA_L = 4.0            # rad/s^2, aceleracion angular exigida a la articulacion
JL = 3.0                # kg*m^2
TAU_G = 60.0            # N*m, par de gravedad maximo en el eslabon

def par_motor_necesario(G, tau_g=TAU_G, Jl=JL, alfa=ALFA_L, Jmot=Jm):
    return Jmot * G * alfa + (Jl * alfa + tau_g) / G

for etiqueta, tg in [('sin par de gravedad', 0.0), (f'con τ_g = {TAU_G:.0f} N·m', TAU_G)]:
    res = minimize_scalar(lambda g: par_motor_necesario(g, tau_g=tg),
                          bounds=(1.0, 2000.0), method='bounded')
    G_teorico = np.sqrt((JL + tg / ALFA_L) / Jm)
    print(f'{etiqueta:>22}: G óptimo numérico = {res.x:6.1f} | '
          f'fórmula √((Jl+τ_g/α)/Jm) = {G_teorico:6.1f} | '
          f'par mínimo = {res.fun:.3f} N·m')

Gs = np.logspace(0.3, 3, 400)
fig, ax = plt.subplots(figsize=(7, 3.6))
ax.loglog(Gs, par_motor_necesario(Gs, tau_g=0.0), color=IQS_VERDE, lw=2,
          label='sin par de gravedad')
ax.loglog(Gs, par_motor_necesario(Gs), color=IQS_AZUL, lw=2, label=f'con τ_g = {TAU_G:.0f} N·m')
ax.loglog(Gs, Jm * Gs * ALFA_L, color='gray', lw=1, ls='--', label='término del rotor (∝ G)')
ax.loglog(Gs, (JL * ALFA_L + TAU_G) / Gs, color='gray', lw=1, ls=':', label='término de carga (∝ 1/G)')
for tg, col in [(0.0, IQS_VERDE), (TAU_G, IQS_AZUL)]:
    g_opt = np.sqrt((JL + tg / ALFA_L) / Jm)
    ax.plot(g_opt, par_motor_necesario(g_opt, tau_g=tg), 'o', color=col, ms=9, zorder=5)
ax.set_xlabel('relación de reducción G'); ax.set_ylabel('par del motor necesario [N·m]')
ax.legend(fontsize=8); ax.set_title('El mínimo está donde se cruzan los dos términos')
plt.tight_layout(); plt.show()"""))

C.append(md("""**Cómo se lee esta figura.** Las dos rectas grises son los dos términos por separado, y el mínimo de su suma cae exactamente donde se cortan: eso es lo que significa «acoplar inercias». El par de gravedad desplaza el óptimo hacia la derecha porque añade carga que la reductora sí puede aliviar, mientras que el término del rotor no cambia. Y el mínimo es muy plano: moverse un factor dos alrededor de G* cuesta apenas un veinticinco por ciento más de par, lo que da libertad para elegir una relación de catálogo en lugar de un número exacto.

Esa planitud es importante porque el óptimo teórico casi nunca es viable, como se ve enseguida.

### Ejercicio 2

Calcula el par necesario en G*, en G*/2 y en 2·G*, y comprueba numéricamente lo plano que es el mínimo. Después responde: si el motor disponible tuviera la mitad de inercia de rotor, ¿hacia dónde se movería el óptimo, y por qué es esa la razón de que los servomotores de robótica se diseñen largos y estrechos en lugar de cortos y gruesos?"""))

C.append(code("""# Ejercicio 2
# pista: par_motor_necesario(G_opt/2) y par_motor_necesario(2*G_opt)
"""))

# ---------------- 4. Seleccion completa
C.append(md("""## 4. Una selección motor-reductora, con números

El procedimiento de dimensionado es práctica de ingeniería estándar montada sobre las relaciones anteriores; los pasos son de los apuntes y los márgenes numéricos, de catálogo. Del ciclo de trabajo se obtienen el par pico y el par eficaz; con una G de tanteo se refieren par, velocidad e inercia al eje del motor; se comprueba la velocidad, cuyo techo físico lo fija la back-EMF frente a la tensión de bus disponible (Corke, 2023, p. 346); se comprueba que el par eficaz cabe en el par nominal con margen térmico y el pico en el par máximo; y se evalúa la relación de inercias, que los fabricantes recomiendan mantener en el orden de la unidad a la decena.

El ciclo es un giro de 90° con perfil trapezoidal de velocidad, seguido de una pausa. La articulación es un hombro, así que el par de gravedad varía con el coseno del ángulo."""))

C.append(code("""W_MAX_L = 2.0            # rad/s, velocidad maxima de la articulacion
RECORRIDO = np.pi / 2    # 90 grados
T_PAUSA = 0.6            # s de reposo al final de cada ciclo
D_L = 0.8                # N*m*s/rad, friccion viscosa en la articulacion

t_acc = W_MAX_L / ALFA_L
d_acc = 0.5 * ALFA_L * t_acc**2
t_cte = (RECORRIDO - 2 * d_acc) / W_MAX_L
T_CICLO = 2 * t_acc + t_cte + T_PAUSA

dt = 5e-4
t = np.arange(0, T_CICLO, dt)
alfa = np.zeros_like(t)
alfa[t < t_acc] = ALFA_L
alfa[(t >= t_acc + t_cte) & (t < 2 * t_acc + t_cte)] = -ALFA_L
w_l = np.cumsum(alfa) * dt
th_l = np.cumsum(w_l) * dt

tau_l = JL * alfa + D_L * w_l + TAU_G * np.cos(th_l)     # par requerido en la articulacion

print(f'Ciclo: {t_acc:.2f} s de aceleración + {t_cte:.2f} s a velocidad constante + '
      f'{t_acc:.2f} s de frenado + {T_PAUSA:.1f} s de pausa = {T_CICLO:.2f} s')
print(f'Recorrido conseguido: {np.degrees(th_l[-1]):.1f}°')
print(f'Par pico en la articulación : {np.abs(tau_l).max():.2f} N·m')
print(f'Par eficaz (RMS) del ciclo  : {np.sqrt((tau_l**2).mean()):.2f} N·m')"""))

C.append(code("""# --- catalogo del servomotor candidato (datos de hoja de caracteristicas) ---
MOTOR = {'Jm': 1.0e-4, 'tau_nom': 0.90, 'tau_max': 2.70, 'w_max': 450.0}

def evaluar(G, margen_w=0.90):
    \"\"\"Refiere el ciclo al eje del motor y comprueba las cuatro condiciones.\"\"\"
    tau_m = MOTOR['Jm'] * G * alfa + tau_l / G          # par instantaneo del motor
    pico = np.abs(tau_m).max()
    rms = np.sqrt((tau_m**2).mean())
    w_m = np.abs(w_l).max() * G
    ratio = JL / (G**2 * MOTOR['Jm'])
    ok = (pico <= MOTOR['tau_max'] and rms <= MOTOR['tau_nom']
          and w_m <= margen_w * MOTOR['w_max'] and ratio <= 10.0)
    return pico, rms, w_m, ratio, ok

print(f'{"G":>7} | {"τ pico":>7} | {"τ RMS":>7} | {"ω motor":>8} | {"Jl/(G²Jm)":>10} | veredicto')
print('-' * 74)
for g in [10, 25, 50, 100, 160, 250]:
    pico, rms, w_m, ratio, ok = evaluar(g)
    motivos = []
    if pico > MOTOR['tau_max']: motivos.append('pico')
    if rms > MOTOR['tau_nom']: motivos.append('RMS')
    if w_m > 0.9 * MOTOR['w_max']: motivos.append('velocidad')
    if ratio > 10.0: motivos.append('inercias')
    veredicto = 'VALE' if ok else 'no: ' + ', '.join(motivos)
    print(f'{g:7d} | {pico:7.2f} | {rms:7.2f} | {w_m:8.1f} | {ratio:10.2f} | {veredicto}')

print(f'\\nLímites del motor: τ_max = {MOTOR["tau_max"]} N·m, τ_nom = {MOTOR["tau_nom"]} N·m, '
      f'ω_max = {MOTOR["w_max"]:.0f} rad/s (se usa el 90 %)')
print(f'G óptimo por acoplamiento de inercias: {np.sqrt((JL + TAU_G/ALFA_L)/MOTOR["Jm"]):.0f} '
      '-> inalcanzable, la velocidad del motor lo prohíbe.')"""))

C.append(code("""gg = np.linspace(5, 300, 400)
pico = np.array([evaluar(g)[0] for g in gg])
rms = np.array([evaluar(g)[1] for g in gg])
wm = np.array([evaluar(g)[2] for g in gg])

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 3.5))
a1.plot(gg, pico, color=IQS_AZUL, lw=2, label='par pico referido')
a1.plot(gg, rms, color=IQS_VERDE, lw=2, label='par eficaz referido')
a1.axhline(MOTOR['tau_max'], color='crimson', ls='--', lw=1.3, label='τ máx del motor')
a1.axhline(MOTOR['tau_nom'], color='crimson', ls=':', lw=1.3, label='τ nominal del motor')
a1.set_ylim(0, 3.2); a1.set_xlabel('G'); a1.set_ylabel('N·m')
a1.legend(fontsize=7); a1.set_title('Comprobación de par')

a2.plot(gg, wm, color=IQS_AZUL, lw=2, label='velocidad del motor en el ciclo')
a2.axhline(0.9 * MOTOR['w_max'], color='crimson', ls='--', lw=1.3, label='90 % de ω máx')
a2.set_xlabel('G'); a2.set_ylabel('rad/s')
a2.legend(fontsize=8); a2.set_title('Comprobación de velocidad')
plt.tight_layout(); plt.show()

valida = np.array([evaluar(g)[4] for g in gg])
print(f'Ventana válida de G: de {gg[valida].min():.0f} a {gg[valida].max():.0f}.')
print('Dentro de ella se elige la relación de catálogo más próxima al óptimo de')
print('inercias, que es la mayor posible: G = 160.')"""))

C.append(md("""**La decisión razonada, que es lo que se pide en el examen.** Con G pequeño el motor no llega al par; con G grande no llega a la velocidad; entre ambos hay una ventana, y dentro de la ventana se elige la relación de catálogo más cercana al óptimo de inercias, que además deja la relación Jl/(G²·Jm) cerca de la unidad y por tanto un lazo de control fácil de sintonizar. Todo el razonamiento cabe en cuatro comprobaciones y ninguna de ellas es opcional.

Y el cierre conceptual del bloque: sensor, accionamiento y transmisión no se eligen por separado. La reductora que abarata el motor degrada la transparencia al par que el control de fuerza necesita, y esa tensión la resuelven de formas distintas el robot industrial con G alto, el colaborativo midiendo el par en la articulación (Corke, 2023, p. 364) y el actuador serie-elástico con elasticidad deliberada (Corke, 2023, pp. 367-370). Elegir entre esas tres respuestas es exactamente la jerarquía de decisión multiobjetivo del MDQ (De Silva et al., 2016, pp. 7-8).

### Ejercicio 3

El cliente quiere el mismo movimiento en la mitad de tiempo. Duplica `W_MAX_L` y cuadruplica `ALFA_L`, y vuelve a levantar la tabla de veredictos. ¿Sigue habiendo alguna G válida con este motor? Si no la hay, di cuál de las cuatro comprobaciones falla primero y qué característica del motor habría que mejorar."""))

C.append(code("""# Ejercicio 3: ciclo el doble de rápido
# pista: hay que regenerar alfa, w_l, th_l y tau_l con los nuevos W_MAX_L y ALFA_L
"""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.** La perturbación de 5 N·m en el eslabón llega al motor como 5 N·m con G = 1 y como 0,05 N·m con G = 100: el motor apenas la nota. Pero si el motor no reacciona, esa perturbación acelera la carga con α = τ/J', y J' referido a la carga es Jl + G²·Jm, que con G = 100 vale 3 + 1 = 4 kg·m² frente a 3 kg·m² en directo, es decir, la reductora también frena el movimiento parásito. Lo que se pierde es la *transparencia*: un contacto con una persona produce en el motor una señal cien veces más pequeña, enterrada bajo la fricción de la propia reductora, y por eso un robot con G alto no puede detectar colisiones por corriente con la sensibilidad que exige la limitación de fuerza de S7. La respuesta industrial es medir el par donde ocurre, en la articulación (Corke, 2023, p. 364).

**Ejercicio 2.** El par necesario en G*/2 y en 2·G* es exactamente el mismo por simetría de la función G + c/G, y vale 1,25 veces el mínimo: el óptimo es muy plano, lo que en la práctica significa que basta con acertar el orden de magnitud. Con la mitad de inercia de rotor, G* = √((Jl + τ_g/α)/Jm) crece en un factor √2 y el par mínimo baja: un motor con menos inercia de rotor permite reducciones mayores y necesita menos par. Esa es la razón de que los servomotores de robótica se diseñen con rotores largos y de diámetro pequeño — la inercia crece con la cuarta potencia del radio y solo linealmente con la longitud, así que estilizar el rotor es la forma barata de mejorar la dinámica.

**Ejercicio 3.** Con el ciclo el doble de rápido la velocidad de la articulación se duplica, de modo que la velocidad del motor para una G dada también se duplica y el límite superior de la ventana cae a la mitad; a la vez, la aceleración se cuadruplica y el par requerido sube, con lo que el límite inferior de la ventana sube. La ventana se cierra: con este motor no queda ninguna G válida, y la primera comprobación que falla al subir G es la de velocidad. Hay dos salidas y conviene discutirlas: un motor con mayor velocidad máxima —lo que en el fondo significa mayor tensión de bus frente a la back-EMF (Corke, 2023, p. 346)— o un motor con más par y menos inercia de rotor, que es más caro. Suavizar el perfil de velocidad, si el proceso lo permite, es la tercera y suele ser la más barata."""))

C.append(md("""---

## Para llevarse de esta sesión

La reductora no es un accesorio mecánico: es el elemento que decide qué planta ve el controlador. Divide el par por G, la velocidad la multiplica por G, y la inercia y la fricción de la carga las divide por G² — y de esas cuatro relaciones sale todo lo demás, desde la insensibilidad a la configuración del brazo hasta la imposibilidad de detectar un contacto suave por corriente.

El dimensionado no tiene misterio pero no admite atajos: par pico, par eficaz, velocidad y relación de inercias, las cuatro, sobre el ciclo de trabajo completo y no sobre el caso peor imaginado. El óptimo teórico de acoplamiento de inercias sirve para saber hacia dónde mirar, pero la elección real la acota casi siempre la velocidad máxima del motor, que a su vez es una consecuencia directa de la back-EMF de la sesión anterior. Y esa cadena —de la ecuación eléctrica del motor a la elección de una reductora de catálogo— es exactamente lo que el bloque quería enseñar.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S12_Transmisiones_Seleccion.ipynb', C)
print('escrito S12')
