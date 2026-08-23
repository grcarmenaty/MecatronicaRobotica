from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('scipy','scipy'), ('matplotlib','matplotlib')]
C = []

C.append(cabecera(
    "S08", "Características estáticas y dinámicas de un sensor", "3",
    "miércoles 30 de septiembre de 2026", "1 h",
    "Fabrica un sensor sintético con todos los defectos de un sensor real —no linealidad, sesgo, dispersión, histéresis, cuantización y retardo— y calcula sobre sus datos los mismos indicadores que aparecen en una hoja de características: sensibilidad, span, FSO, exactitud, repetibilidad, histéresis, resolución y constante de tiempo.",
    "Fraden (2016), caps. 2 y 8 — función de transferencia (p. 13) y su inversa (p. 14), sensibilidad (p. 18), calibración por regresión (pp. 20-25), span (p. 30), FSO y exactitud (p. 31), histéresis (p. 35), no linealidad (p. 36), repetibilidad y resolución (p. 38), respuesta dinámica de primer orden (pp. 41-42), elección posición/velocidad/aceleración (p. 327); De Silva et al. (2016), p. 152 — Nyquist-Shannon.",
    "los apuntes del bloque 3"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=4, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.2)
plt.rcParams['axes.grid'] = True
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('Listo.')"""))

# ---------------- 1. Funcion de transferencia
C.append(md("""## 1. La función de transferencia y su linealización

Toda la caracterización estática cuelga de una sola curva. La relación estímulo-respuesta invariante en el tiempo «se denomina comúnmente función de transferencia» S = f(s) (Fraden, 2016, p. 13), pero en operación el problema es el inverso: se mide S y se quiere s, de modo que el sistema de medida aplica la función inversa F(S) para «romper el código» (Fraden, 2016, p. 14). Todo lo demás —sensibilidad, no linealidad, exactitud— son formas de medir cuánto se aparta esa curva del ideal recto.

Trabajamos con un sensor de presión piezorresistivo sintético de span 0-200 kPa (Fraden, 2016, p. 30) y salida en milivoltios, con una curvatura deliberada del orden del 6 % del fondo de escala. Primero lo calibramos por regresión sobre 21 puntos repartidos por todo el span, que es exactamente el método que recomienda el libro cuando hay más medidas que incógnitas (Fraden, 2016, pp. 22-25)."""))

C.append(code("""rng = np.random.default_rng(8)

SPAN = (0.0, 200.0)               # kPa: span o fondo de escala de entrada (Fraden, p. 30)

def sensor_ideal(s):
    \"\"\"Funcion de transferencia S = f(s) del sensor, en mV. Ligeramente cuadratica.\"\"\"
    return 0.5 + 0.020 * s - 2.5e-5 * s**2

s_cal = np.linspace(*SPAN, 21)                                  # puntos de calibracion
S_cal = sensor_ideal(s_cal) + rng.normal(0, 0.004, s_cal.size)  # ruido de medida

# --- calibracion: recta de minimos cuadrados sobre TODO el span (Fraden, pp. 22-25) ---
b_rec, a_rec = np.polyfit(s_cal, S_cal, 1)          # S ~ a_rec + b_rec * s
# --- calibracion alternativa: polinomio de 2.o grado (Fraden, pp. 15-19) ---
coef2 = np.polyfit(s_cal, S_cal, 2)

FSO = sensor_ideal(SPAN[1]) - sensor_ideal(SPAN[0])             # fondo de escala de salida (p. 31)
resid = S_cal - (a_rec + b_rec * s_cal)
no_lin = 100 * np.abs(resid).max() / FSO                        # no linealidad (p. 36)

print(f'Span de entrada      : {SPAN[0]:.0f} a {SPAN[1]:.0f} kPa')
print(f'FSO (salida)         : {FSO:.3f} mV')
print(f'Sensibilidad media   : {b_rec*1000:.2f} uV/kPa')
print(f'Sensibilidad a 0 kPa : {(0.020 - 5e-5*0)*1000:.2f} uV/kPa   (derivada dS/ds, Fraden p. 18)')
print(f'Sensibilidad a 200   : {(0.020 - 5e-5*200)*1000:.2f} uV/kPa')
print(f'No linealidad        : {no_lin:.2f} % FSO')"""))

C.append(md("""La sensibilidad se ha calculado de las dos maneras que el libro distingue: como pendiente constante de la recta ajustada y como derivada dS/ds punto a punto, que es la definición válida cuando la curva no es recta (Fraden, 2016, p. 18). Aquí la sensibilidad cae a la mitad de un extremo al otro del span, y ese solo dato ya dice que la inversa lineal no puede servir en todo el rango.

Lo que importa de verdad al usuario del sensor no es el error en milivoltios sino en kilopascales: dividir el error de salida por la sensibilidad local es lo que convierte una desviación de la curva en un error de medida."""))

C.append(code("""s_fino = np.linspace(*SPAN, 400)
S_fino = sensor_ideal(s_fino)

def inversa_lineal(S):
    \"\"\"F(S) suponiendo el sensor recto: la que usaria un sistema sin linealizar.\"\"\"
    return (S - a_rec) / b_rec

def inversa_cuad(S):
    \"\"\"F(S) resolviendo el ajuste de 2.o grado. Es la linealizacion por software.\"\"\"
    disc = coef2[1]**2 - 4 * coef2[0] * (coef2[2] - S)
    return (-coef2[1] + np.sqrt(disc)) / (2 * coef2[0])

s_lineal = inversa_lineal(S_fino)
s_cuad = inversa_cuad(S_fino)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.4))
a1.plot(s_fino, S_fino, color=IQS_AZUL, lw=2, label='función de transferencia real')
a1.plot(s_fino, a_rec + b_rec * s_fino, color=IQS_VERDE, lw=2, ls='--', label='recta de calibración')
a1.scatter(s_cal, S_cal, s=16, color='crimson', zorder=5, label='puntos de calibración')
a1.set_xlabel('estímulo s [kPa]'); a1.set_ylabel('salida S [mV]')
a1.legend(fontsize=8); a1.set_title('S = f(s)')

a2.plot(s_fino, s_lineal - s_fino, color=IQS_AZUL, lw=2, label='inversa lineal')
a2.plot(s_fino, s_cuad - s_fino, color=IQS_VERDE, lw=2, label='inversa cuadrática')
a2.axhline(0, color='black', lw=0.8)
a2.set_xlabel('presión verdadera [kPa]'); a2.set_ylabel('error [kPa]')
a2.legend(fontsize=8); a2.set_title('Error de la función inversa F(S)')
plt.tight_layout(); plt.show()

print(f'Error máximo con inversa lineal    : {np.abs(s_lineal - s_fino).max():.2f} kPa')
print(f'Error máximo con inversa cuadrática: {np.abs(s_cuad - s_fino).max():.2f} kPa')"""))

C.append(md("""**Lo que hay que hacer notar en clase.** La linealización no ha tocado el sensor: el hardware sigue siendo igual de curvo. Lo que ha cambiado es el modelo que el procesador usa para invertir la lectura, y eso reduce el error un orden de magnitud sin gastar un euro. Es la estrategia moderna que los apuntes defienden frente a forzar la linealidad física, y el mismo argumento que se aplica al termistor NTC (Fraden, 2016, pp. 532-534).

### Ejercicio 1

Sustituye la recta de mínimos cuadrados por la *recta terminal*, la que pasa por los dos puntos extremos del span (s = 0 y s = 200 kPa). Recalcula la no linealidad en % FSO y compárala con la que acabas de obtener. ¿Cuál de las dos rectas conviene declarar en el catálogo si se quiere una cifra de no linealidad pequeña, y cuál si se quiere que el error medio de medida sea pequeño?"""))

C.append(code("""# Ejercicio 1: recta terminal por los dos extremos del span
# pista: b_term = (S(200) - S(0)) / 200 ;  a_term = S(0)
"""))

# ---------------- 2. Exactitud vs repetibilidad
C.append(md("""## 2. Exactitud frente a repetibilidad

Es la distinción que más cuesta y la que más dinero cuesta equivocar. La exactitud, «que en realidad significa inexactitud», es «la mayor desviación del valor representado por el sensor respecto al valor ideal o verdadero del estímulo» (Fraden, 2016, p. 31); la repetibilidad es la incapacidad de dar el mismo valor en condiciones idénticas, y se expresa como la diferencia máxima entre dos ciclos de calibración en porcentaje del fondo de escala (Fraden, 2016, p. 38).

Simulamos cinco ciclos completos de calibración del mismo sensor. Cada ciclo arrastra un desplazamiento propio —el sensor «se despierta» distinto cada día— y además todos comparten un sesgo sistemático constante, que es el defecto que la calibración sí puede eliminar."""))

C.append(code("""SESGO_SISTEMATICO = 0.030      # mV, comun a todos los ciclos: se calibra
DERIVA_POR_CICLO = 0.012       # mV, cambia de un ciclo a otro: NO se calibra
RUIDO_PUNTO = 0.003            # mV

s_pts = np.linspace(*SPAN, 11)
N_CICLOS = 5
lecturas = np.empty((N_CICLOS, s_pts.size))

for c in range(N_CICLOS):
    offset_ciclo = rng.normal(0, DERIVA_POR_CICLO)
    lecturas[c] = (sensor_ideal(s_pts) + SESGO_SISTEMATICO + offset_ciclo
                   + rng.normal(0, RUIDO_PUNTO, s_pts.size))

# convertir a kPa con la inversa linealizada del apartado anterior, para que
# lo que quede sea sesgo y dispersion y no la no linealidad ya estudiada
s_est = inversa_cuad(lecturas)
error = s_est - s_pts                                   # kPa

FS = SPAN[1] - SPAN[0]
exactitud = 100 * np.abs(error).max() / FS              # % FS (Fraden, p. 31)
repetibilidad = 100 * (s_est.max(axis=0) - s_est.min(axis=0)).max() / FS   # % FS (p. 38)

print(f'Exactitud (máxima desviación al valor verdadero): {exactitud:.2f} % FS')
print(f'Repetibilidad (dispersión entre ciclos)         : {repetibilidad:.2f} % FS')
print(f'Cociente exactitud/repetibilidad                : {exactitud/repetibilidad:.1f}')"""))

C.append(code("""fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.4))
for c in range(N_CICLOS):
    a1.plot(s_pts, error[c], marker='o', ms=4, lw=1.2, alpha=0.85, label=f'ciclo {c+1}')
a1.axhline(0, color='black', lw=0.8)
a1.set_xlabel('presión verdadera [kPa]'); a1.set_ylabel('error [kPa]')
a1.legend(fontsize=7, ncol=2); a1.set_title('Error de cada ciclo de calibración')

media = error.mean(axis=0)
disp = error.max(axis=0) - error.min(axis=0)
a2.plot(s_pts, media, color=IQS_AZUL, lw=2, label='sesgo medio (calibrable)')
a2.plot(s_pts, disp, color=IQS_VERDE, lw=2, label='dispersión entre ciclos (no calibrable)')
a2.axhline(0, color='black', lw=0.8)
a2.set_xlabel('presión verdadera [kPa]'); a2.set_ylabel('kPa')
a2.legend(fontsize=8); a2.set_title('Lo que se puede corregir y lo que no')
plt.tight_layout(); plt.show()

# que pasa si corregimos el sesgo medio
error_corregido = error - media
print(f'Exactitud tras corregir el sesgo medio: {100*np.abs(error_corregido).max()/FS:.2f} % FS')
print('La repetibilidad no cambia: la corrección de sesgo no toca la dispersión.')"""))

C.append(md("""**El aviso de ingeniero.** Un sensor puede repetir exquisitamente un valor sesgado. Ese sensor es malo en exactitud y excelente en repetibilidad, y para un lazo de control realimentado suele ser preferible al contrario, porque un sesgo estable se compensa con una constante y una dispersión no se compensa con nada. Cuando en el catálogo solo aparece una cifra, hay que leer la letra pequeña para saber cuál de las dos es.

### Ejercicio 2

Sube `DERIVA_POR_CICLO` a 0.05 mV y baja `SESGO_SISTEMATICO` a cero. Vuelve a calcular las dos cifras. ¿Cuál de los dos sensores —el de sesgo grande y dispersión pequeña o el de sesgo nulo y dispersión grande— elegirías para el lazo de par de un robot colaborativo, y por qué?"""))

C.append(code("""# Ejercicio 2: repite el bucle de arriba cambiando las dos constantes
# SESGO_SISTEMATICO, DERIVA_POR_CICLO = 0.0, 0.05
"""))

# ---------------- 3. Histeresis y resolucion
C.append(md("""## 3. Histéresis, cuantización y resolución

Dos defectos más de la hoja de características, y son de naturaleza distinta. La histéresis es la desviación de la salida en un mismo punto según el estímulo se aproxime desde un lado o desde el otro (Fraden, 2016, p. 35): es un defecto del sensor, tiene memoria y no se corrige con una tabla estática. La resolución «describe los incrementos más pequeños del estímulo que pueden detectarse» (Fraden, 2016, p. 38): en una cadena digital la fija el conversor A/D, y sí se corrige — comprando más bits.

Barremos el span de subida y de bajada con una histéresis del 0,5 % del FSO, y digitalizamos la salida con un A/D de 10 bits sobre un rango de entrada de 0 a 5 mV."""))

C.append(code("""H_FSO = 0.005                       # histeresis: 0,5 % del FSO (Fraden, p. 35)
N_BITS, V_AD = 10, 5.0              # conversor A/D: 10 bits sobre 0-5 mV

s_sub = np.linspace(SPAN[0], SPAN[1], 200)
s_baj = s_sub[::-1]
S_sub = sensor_ideal(s_sub) - H_FSO * FSO / 2       # ramas de ida y de vuelta
S_baj = sensor_ideal(s_baj) + H_FSO * FSO / 2

hist_medida = 100 * np.abs(S_baj[::-1] - S_sub).max() / FSO
print(f'Histéresis medida: {hist_medida:.2f} % FSO')

LSB = V_AD / 2**N_BITS                              # mV por escalon
def cuantizar(S):
    return np.round(S / LSB) * LSB

sens_0, sens_200 = 0.020, 0.020 - 5e-5 * 200        # mV/kPa en los dos extremos
print(f'\\nLSB del A/D de {N_BITS} bits: {LSB*1000:.2f} uV')
print(f'Resolución a   0 kPa: {LSB/sens_0:.3f} kPa   (sensibilidad alta)')
print(f'Resolución a 200 kPa: {LSB/sens_200:.3f} kPa   (sensibilidad baja: peor resolución)')
print(f'Escalones usados en todo el span: {int(FSO/LSB)} de los {2**N_BITS} disponibles')"""))

C.append(code("""fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.4))
a1.plot(s_sub, S_sub, color=IQS_AZUL, lw=2, label='rama de subida')
a1.plot(s_baj, S_baj, color=IQS_VERDE, lw=2, label='rama de bajada')
a1.set_xlabel('estímulo s [kPa]'); a1.set_ylabel('salida S [mV]')
a1.legend(fontsize=8); a1.set_title(f'Lazo de histéresis ({hist_medida:.2f} % FSO)')

zona = (s_fino > 150) & (s_fino < 165)              # zoom para ver los escalones
a2.plot(s_fino[zona], sensor_ideal(s_fino[zona]), color=IQS_AZUL, lw=2, label='salida analógica')
a2.step(s_fino[zona], cuantizar(sensor_ideal(s_fino[zona])), color=IQS_VERDE, lw=2,
        where='mid', label=f'digitalizada, {N_BITS} bits')
a2.set_xlabel('estímulo s [kPa]'); a2.set_ylabel('salida S [mV]')
a2.legend(fontsize=8); a2.set_title('Cuantización: la resolución del sistema')
plt.tight_layout(); plt.show()

err_cuant = cuantizar(sensor_ideal(s_fino)) - sensor_ideal(s_fino)
print(f'Error de cuantización RMS: {np.sqrt((err_cuant**2).mean())*1000:.2f} uV'
      f'  (teórico LSB/√12 = {LSB/np.sqrt(12)*1000:.2f} uV)')"""))

C.append(md("""**Dos lecturas para el aula.** La primera: la resolución no es una cifra única cuando el sensor no es lineal, porque el mismo escalón del A/D vale el doble de kilopascales donde la sensibilidad es la mitad. La segunda: solo se están usando unos 600 de los 1024 escalones del conversor, porque el rango de entrada del A/D no está adaptado al FSO del sensor — un acondicionamiento con ganancia que lleve el FSO al fondo de escala del A/D recupera esa resolución perdida gratis, y es lo primero que hay que mirar en cualquier cadena de instrumentación."""))

# ---------------- 4. Respuesta dinamica
C.append(md("""## 4. Respuesta dinámica: el sensor de primer orden

Todo lo anterior vale con estímulo lento. Cuando el estímulo varía deprisa «la respuesta del sensor generalmente no lo sigue con fidelidad perfecta» y aparece un error dinámico que, a diferencia del estático, «es siempre dependiente del tiempo» (Fraden, 2016, p. 41). El caso canónico es el sensor de primer orden con un solo elemento almacenador de energía —el sensor de temperatura y su capacidad térmica—, especificado por su constante de tiempo τ, «una medida de la inercia del sensor», o equivalentemente por la frecuencia de corte a −3 dB (Fraden, 2016, pp. 41-42).

Simulamos una sonda de temperatura con τ = 2,5 s sometida a un escalón de 20 a 80 °C, y comprobamos numéricamente las dos formas de leer la misma constante."""))

C.append(code("""TAU = 2.5                                    # constante de tiempo del sensor, s

def primer_orden(u, dt, tau, y0):
    \"\"\"Integra tau*dy/dt + y = u por Euler explicito.\"\"\"
    y = np.empty_like(u); y[0] = y0
    for k in range(1, u.size):
        y[k] = y[k-1] + dt / tau * (u[k-1] - y[k-1])
    return y

dt = 0.005
t = np.arange(0, 20, dt)
u = np.where(t < 2.0, 20.0, 80.0)            # escalon de 60 grados en t = 2 s
y = primer_orden(u, dt, TAU, 20.0)

# lectura de tau al 63,2 % del salto (Fraden, p. 42)
objetivo = 20.0 + 0.632 * 60.0
i63 = np.argmax((t > 2.0) & (y >= objetivo))
tau_est = t[i63] - 2.0
f_corte = 1.0 / (2 * np.pi * TAU)

print(f'tau nominal              : {TAU:.2f} s')
print(f'tau leída al 63,2 %      : {tau_est:.2f} s')
print(f'Frecuencia de corte -3 dB: {f_corte:.4f} Hz')
print(f'Error dinámico 1 s tras el escalón: {u[int(3.0/dt)] - y[int(3.0/dt)]:.1f} °C')""" ))

C.append(code("""# barrido en frecuencia: cuanto atenua el sensor una senoide de amplitud 1
frecs = np.array([0.005, 0.01, 0.02, f_corte, 0.1, 0.2])
ganancia = []
for f in frecs:
    tt = np.arange(0, 8 * TAU + 3 / f, dt)          # transitorio + tres periodos
    uu = np.sin(2 * np.pi * f * tt)
    yy = primer_orden(uu, dt, TAU, 0.0)
    regimen = tt > tt[-1] - 1 / f                   # ultimo periodo completo
    ganancia.append(yy[regimen].max() - yy[regimen].min())
ganancia = np.array(ganancia) / 2
teorica = 1 / np.sqrt(1 + (2 * np.pi * frecs * TAU)**2)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.4))
a1.plot(t, u, color='black', lw=1.5, label='estímulo real')
a1.plot(t, y, color=IQS_AZUL, lw=2, label='lectura del sensor')
a1.axvline(2.0 + TAU, color=IQS_VERDE, ls='--', lw=1.5, label='t = escalón + τ')
a1.axhline(objetivo, color=IQS_VERDE, ls=':', lw=1.2)
a1.set_xlabel('t [s]'); a1.set_ylabel('°C'); a1.legend(fontsize=8)
a1.set_title('Respuesta al escalón')

a2.semilogx(frecs, 20 * np.log10(teorica), color=IQS_AZUL, lw=2, label='teórica')
a2.semilogx(frecs, 20 * np.log10(ganancia), 'o', color=IQS_VERDE, ms=7, label='simulada')
a2.axhline(-3, color='crimson', ls='--', lw=1.2, label='-3 dB')
a2.axvline(f_corte, color='crimson', ls=':', lw=1.2)
a2.set_xlabel('frecuencia [Hz]'); a2.set_ylabel('ganancia [dB]')
a2.legend(fontsize=8); a2.set_title('Respuesta en frecuencia')
plt.tight_layout(); plt.show()"""))

C.append(md("""**El puente con el resto del bloque.** La constante de tiempo del escalón y la frecuencia de corte del barrido son el mismo número visto de dos formas, y las dos aparecen en el catálogo indistintamente. Esta idea, unida a la regla con que Fraden abre su capítulo de velocidad y aceleración —posición hasta ~10 Hz, velocidad hasta ~1 kHz, aceleración por encima, porque derivar una posición ruidosa «puede resultar en errores extremadamente altos» (Fraden, 2016, p. 327)— y a la de Nyquist-Shannon, que exige muestrear al menos al doble de la frecuencia de la señal (De Silva et al., 2016, p. 152), resuelve la mitad de los problemas de selección de sensor de S10.

### Ejercicio 3

Sustituye el escalón por una rampa de 5 °C/s y mide el retardo en régimen permanente entre el estímulo y la lectura. Comprueba que el error en régimen vale exactamente τ multiplicado por la pendiente de la rampa, y razona qué implica eso para un sensor de temperatura montado en un proceso que calienta continuamente."""))

C.append(code("""# Ejercicio 3: rampa
# u_rampa = 20.0 + 5.0 * t   ->  primer_orden(u_rampa, dt, TAU, 20.0)
"""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.** La recta terminal pasa exactamente por los extremos, así que el residuo se anula en s = 0 y en s = 200 y se concentra en el centro del span, donde alcanza aproximadamente el doble que el residuo máximo de la recta de mínimos cuadrados: la no linealidad declarada sale peor. La de mínimos cuadrados reparte el error a ambos lados de cero y minimiza el error cuadrático medio, así que da mejor cifra de catálogo y mejor error medio de medida; la terminal solo tiene sentido cuando la aplicación exige coincidencia exacta en los extremos del rango. Moraleja: dos fabricantes honestos pueden declarar no linealidades distintas del mismo sensor sin mentir, según la recta de referencia que hayan elegido.

**Ejercicio 2.** Con sesgo sistemático nulo y deriva de ciclo grande, la exactitud y la repetibilidad se acercan porque ya no hay una componente calibrable que las separe. Para el lazo de par de un cobot conviene el sensor de sesgo grande y dispersión pequeña: el sesgo se mide una vez en la puesta en marcha y se resta en el software, mientras que la dispersión entra directamente como ruido en la realimentación y obliga a bajar las ganancias del controlador. La repetibilidad es la propiedad que el control no puede arreglar.

**Ejercicio 3.** Para τ·dy/dt + y = u con u = k·t, la solución en régimen permanente es y = k·(t − τ): la lectura reproduce la rampa con la pendiente correcta pero retrasada exactamente τ segundos, lo que equivale a un error constante de k·τ = 5 · 2,5 = 12,5 °C. El sensor nunca alcanza al proceso mientras este siga calentando, y el error no disminuye con el tiempo — solo se ve al parar el calentamiento. Es la razón por la que en un proceso con rampas conocidas se compensa el retardo por software en lugar de comprar un sensor más rápido."""))

C.append(md("""---

## Para llevarse de esta sesión

Una hoja de características no es una lista de adjetivos: cada cifra se puede calcular sobre datos, y este cuaderno las ha calculado todas sobre un sensor que cabía en cuatro líneas. El estudiante debe salir sabiendo que exactitud y repetibilidad miden cosas distintas, que la no linealidad depende de la recta de referencia que se elija, y que la resolución del sistema la fija el eslabón más pobre de la cadena, que casi nunca es el sensor.

La segunda idea es que la mitad de los defectos se arreglan en el procesador y la otra mitad no. La no linealidad y el sesgo sistemático se corrigen con un modelo inverso mejor; la histéresis, la dispersión entre ciclos y el retardo dinámico exigen mejor hardware o un estimador con memoria. Saber en qué grupo cae cada defecto es lo que separa una especificación realista de una lista de deseos.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S08_Caracteristicas_Sensores.ipynb', C)
print('escrito S08')
