from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('scipy','scipy'), ('matplotlib','matplotlib')]
C = []

C.append(cabecera(
    "S09", "Encoders en cuadratura e IMU", "3",
    "jueves 1 de octubre de 2026", "1 h",
    "Decodifica de cero las señales A y B de un encoder incremental —cuenta, sentido y resolución x4— y después construye la cadena completa de una IMU: integración del giróscopo con su deriva, inclinómetro por acelerómetro con su ruido, y filtro complementario que se queda con lo bueno de cada uno.",
    "Fraden (2016), caps. 7 y 8 — encoder óptico incremental y absoluto (p. 309), señales en cuadratura (p. 310), acelerómetro de segundo orden (p. 329), giróscopo de rotor (pp. 340-341) y MEMS de Coriolis (p. 342); Corke (2023), caps. 1 y 3 — propioceptivo frente a exteroceptivo (pp. 8-9), INS (p. 107), MEMS vibratorios (p. 108), masa de prueba (p. 111), el acelerómetro mide gravedad y movimiento (pp. 112-113), IMU y AHRS (pp. 117-118), modelo de error y bias (p. 118), características complementarias (p. 119).",
    "los apuntes del bloque 3"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=4, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.2)
plt.rcParams['axes.grid'] = True
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('Listo.')"""))

# ---------------- 1. Encoder en cuadratura
C.append(md("""## 1. Del disco ranurado a la cuenta: decodificar A y B

El encoder óptico incremental es el sensor propioceptivo por antonomasia (Corke, 2023, pp. 8-9). Su principio es la modulación de luz por rejilla: un disco «con secciones transparentes y opacas» interrumpe el haz entre emisor y detector infrarrojos, y el fotodetector entrega una salida binaria (Fraden, 2016, p. 309). Un solo canal cuenta pasos pero no sabe hacia dónde; la detección de sentido exige dos canales ópticos desfasados 90°, «cuyas señales en cuadratura indican el sentido de giro según cuál adelante a cuál» (Fraden, 2016, p. 310).

Fabricamos las dos señales a partir de un perfil de movimiento que acelera, mantiene velocidad e invierte el sentido, y las muestreamos a 20 kHz como haría el periférico de un microcontrolador."""))

C.append(code("""N_LINEAS = 500                 # lineas del disco (Fraden, p. 309)
FS = 20_000.0                  # frecuencia de muestreo del contador, Hz
DT = 1.0 / FS

t = np.arange(0, 1.2, DT)

# perfil de velocidad: rampa, meseta, inversion y meseta negativa
omega = np.piecewise(t,
    [t < 0.4, (t >= 0.4) & (t < 0.7), (t >= 0.7) & (t < 1.0), t >= 1.0],
    [lambda x: 50 * x, 20.0, lambda x: 20 - 116.7 * (x - 0.7), -15.0])   # rad/s
theta = np.concatenate([[0.0], np.cumsum(0.5 * (omega[1:] + omega[:-1]) * DT)])

# --- generacion de las senales A y B en cuadratura ---
ciclos = theta * N_LINEAS / (2 * np.pi)          # un ciclo completo por linea del disco
A = ((ciclos % 1.0) < 0.5).astype(int)
B = (((ciclos - 0.25) % 1.0) < 0.5).astype(int)  # B retrasada 90 grados respecto a A

print(f'Velocidad máxima: {np.abs(omega).max():.1f} rad/s = {np.abs(omega).max()*60/(2*np.pi):.0f} rpm')
print(f'Flancos por segundo a esa velocidad: {4*N_LINEAS*np.abs(omega).max()/(2*np.pi):.0f}')
print(f'Muestras por estado de cuadratura : {FS/(4*N_LINEAS*np.abs(omega).max()/(2*np.pi)):.1f}')"""))

C.append(md("""El decodificador x4 es más simple de lo que su fama sugiere. El par (A, B) recorre cíclicamente cuatro estados y cambia de uno en uno; basta convertir ese par de código Gray a un entero de 0 a 3 y mirar la diferencia con el estado anterior: un salto de +1 (módulo 4) es una cuenta en un sentido, un salto de 3 —que es −1 módulo 4— es una cuenta en el otro, y un salto de 2 significa que se han perdido cuentas porque la lectura ha ido demasiado lenta.

Ese salto de 2 es la trampa de examen: el contador no puede detectar si ha perdido dos cuentas o seis, y por eso el muestreo del encoder tiene su propia condición de Nyquist (De Silva et al., 2016, p. 152)."""))

C.append(code("""def decodificar_x4(A, B):
    \"\"\"Decodificador en cuadratura x4. Devuelve la cuenta acumulada y los saltos ambiguos.\"\"\"
    codigo = 2 * B + (A ^ B)                     # Gray -> binario 0,1,2,3 (A adelantando a B suma)
    salto = np.diff(codigo) % 4
    paso = np.where(salto == 1, 1, np.where(salto == 3, -1, 0))
    ambiguos = int((salto == 2).sum())           # cuentas perdidas: sentido indeterminado
    return np.concatenate([[0], np.cumsum(paso)]), ambiguos

cuenta, ambiguos = decodificar_x4(A, B)

CPR = 4 * N_LINEAS                               # cuentas por vuelta con decodificacion x4
theta_est = cuenta * 2 * np.pi / CPR
error = theta_est - theta
LSB = 2 * np.pi / CPR

print(f'Cuentas por vuelta (x4)   : {CPR}')
print(f'Resolución angular        : {np.degrees(LSB):.4f} ° por cuenta')
print(f'Cuenta final              : {cuenta[-1]:+d}  (vueltas: {cuenta[-1]/CPR:+.3f})')
print(f'Ángulo final real         : {np.degrees(theta[-1]):+.2f} °')
print(f'Ángulo final decodificado : {np.degrees(theta_est[-1]):+.2f} °')
print(f'Error máximo              : {np.degrees(np.abs(error).max()):.4f} ° = {np.abs(error).max()/LSB:.2f} cuentas')
print(f'Saltos ambiguos detectados: {ambiguos}')"""))

C.append(code("""fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(12.5, 3.2))

z = slice(6000, 6060)                            # zoom de 3 ms en pleno giro directo
a1.step(t[z]*1000, A[z] + 2.4, where='post', color=IQS_AZUL, lw=1.8)
a1.step(t[z]*1000, B[z] + 1.0, where='post', color=IQS_VERDE, lw=1.8)
a1.text(t[z][0]*1000, 3.6, 'A', color=IQS_AZUL, fontsize=11)
a1.text(t[z][0]*1000, 2.2, 'B', color=IQS_VERDE, fontsize=11)
a1.set_yticks([]); a1.set_xlabel('t [ms]'); a1.set_title('A adelanta a B: giro directo')

a2.plot(t, np.degrees(theta), color='black', lw=2.2, label='ángulo real')
a2.plot(t, np.degrees(theta_est), color=IQS_AZUL, lw=1.2, ls='--', label='decodificado')
a2.set_xlabel('t [s]'); a2.set_ylabel('grados'); a2.legend(fontsize=8)
a2.set_title('Posición reconstruida')

a3.plot(t, omega, color=IQS_VERDE, lw=2)
a3.axhline(0, color='black', lw=0.8)
a3.set_xlabel('t [s]'); a3.set_ylabel('rad/s'); a3.set_title('Velocidad (nótese la inversión)')
plt.tight_layout(); plt.show()"""))

C.append(md("""**Lo que hay que hacer notar en clase.** El error nunca supera una cuenta y no crece con el tiempo: el encoder incremental no deriva, solo cuantiza. Esa es su diferencia esencial con la IMU del apartado 3, donde el error sí crece sin límite. Lo que el incremental no tiene es referencia absoluta —al encender no sabe dónde está—, y de ahí la maniobra de búsqueda de cero de cualquier robot industrial, o la alternativa del encoder absoluto codificado en Gray, binario o BCD (Fraden, 2016, p. 309)."""))

# ---------------- 2. Resolucion
C.append(md("""## 2. Resolución: cuentas por vuelta, y dónde se monta el encoder

La aritmética es elemental y aun así es donde más se equivoca el estudiante. Un disco de N líneas da N ciclos por vuelta; leyendo solo los flancos de subida de A se obtienen N cuentas (x1), leyendo ambos flancos de A se obtienen 2N (x2), y leyendo los cuatro flancos de A y B se obtienen 4N (x4) sin tocar el disco. La resolución angular es 360°/(4N).

La segunda mitad del cálculo es la que importa en robótica: si el encoder va montado en el eje del motor, antes de la reductora, la resolución que se ve en la articulación se multiplica por la relación de reducción G. Es el motivo por el que casi todos los servoaccionamientos lo montan ahí (el esquema motor-encoder está en Corke, 2023, p. 335)."""))

C.append(code("""G = 100.0                                  # relacion de la reductora, articulacion:motor

print(f'{"líneas N":>9} | {"x1":>7} | {"x2":>7} | {"x4":>7} | {"°/cuenta (x4)":>14} | {"°/cuenta en la art.":>20}')
print('-' * 82)
for N in [100, 500, 1024, 2500]:
    res_motor = 360.0 / (4 * N)
    print(f'{N:9d} | {N:7d} | {2*N:7d} | {4*N:7d} | {res_motor:14.4f} | {res_motor/G:20.5f}')

# cuantas lineas hacen falta para 0,01 grados en la articulacion
objetivo = 0.01
N_nec = 360.0 / (4 * objetivo * G)
print(f'\\nPara {objetivo} ° en la articulación con G = {G:.0f} bastan N = {N_nec:.0f} líneas.')
print('Sin reductora harían falta', int(360.0 / (4 * objetivo)), 'líneas: un disco impracticable.')"""))

C.append(md("""**La conclusión de diseño.** La reductora no solo multiplica el par: multiplica la resolución de la medida y divide el efecto de la holgura del contaje. Ese es un argumento a favor del G alto que se suma a los de S12, y también su contrapartida — el backlash de la propia reductora puede destruir la precisión que el encoder promete, porque el encoder mide el motor y no el eslabón.

### Ejercicio 1

Baja `FS` a 4000 Hz, vuelve a generar A y B y decodifica. Cuenta los saltos ambiguos y compara el ángulo final con el real. ¿A qué velocidad de giro empieza a fallar el contaje con esa frecuencia de muestreo? Escribe la condición general que relaciona N, la velocidad máxima y la frecuencia de muestreo."""))

C.append(code("""# Ejercicio 1: repite la generacion de A y B con FS = 4000 Hz
# pista: la condicion es FS > 4 * N_LINEAS * omega_max / (2*pi), con margen
"""))

# ---------------- 3. Giroscopo y deriva
C.append(md("""## 3. El giróscopo y su deriva

Cambiamos de familia. El giróscopo MEMS mide velocidad angular explotando la aceleración de Coriolis: «la rotación se sustituye por vibración» y la aceleración resultante, proporcional a la velocidad de giro, aparece en el tercer eje perpendicular (Fraden, 2016, p. 342); Corke describe la misma pieza como «una masa que vibra a varios kHz en un plano, cuyo desplazamiento ortogonal por rotación se mide capacitivamente» (Corke, 2023, p. 108).

El modelo de error es el corazón del apartado: la salida es una versión corrompida del valor verdadero, x medida = s·x + b + ε, con factor de escala s, bias b y ruido ε, y «en la práctica el bias es el mayor problema porque varía con el tiempo y la temperatura y tiene un efecto muy dañino sobre la posición y orientación estimadas» (Corke, 2023, p. 118). Lo comprobamos integrando un giróscopo con un bias modesto de 1 °/s durante un minuto."""))

C.append(code("""rng = np.random.default_rng(9)

DT_I = 0.01                                    # 100 Hz, tipico de una IMU de consumo
ti = np.arange(0, 60, DT_I)

# movimiento real de la plataforma: balanceo lento de +-20 grados
theta_real = np.radians(20) * np.sin(2 * np.pi * 0.05 * ti)
omega_real = np.radians(20) * 2 * np.pi * 0.05 * np.cos(2 * np.pi * 0.05 * ti)

BIAS = np.radians(1.0)                         # 1 grado/s de bias (Corke, p. 118)
ESCALA = 1.01                                  # 1 % de error de factor de escala
RUIDO_G = np.radians(0.15)

gyro = ESCALA * omega_real + BIAS + rng.normal(0, RUIDO_G, ti.size)
theta_gyro = np.concatenate([[theta_real[0]], theta_real[0] + np.cumsum(gyro[1:]) * DT_I])

print(f'Bias del giróscopo        : {np.degrees(BIAS):.2f} °/s')
print(f'Deriva teórica en 60 s    : {np.degrees(BIAS)*60:.1f} °')
print(f'Error final integrando    : {np.degrees(theta_gyro[-1] - theta_real[-1]):.1f} °')
print(f'Error RMS solo giróscopo  : {np.degrees(np.sqrt(((theta_gyro-theta_real)**2).mean())):.2f} °')"""))

C.append(md("""Sesenta grados de error en un minuto con un sensor perfectamente honesto. Y esto es solo la orientación: al integrar dos veces una aceleración con bias el error de posición crece con el cuadrado del tiempo, que es la respuesta cuantitativa a por qué un dron no puede navegar con su IMU de diez euros y por qué un INS de verdad —«una unidad autocontenida que estima velocidad, orientación y posición integrando aceleraciones y velocidades angulares, sin entradas externas» (Corke, 2023, p. 107)— cuesta lo que cuesta.

El remedio no es un giróscopo mejor sino un segundo sensor con defectos distintos. El acelerómetro mide la dirección de la gravedad y por tanto la inclinación, sin deriva alguna, pero con dos pegas: es ruidoso y, sobre todo, «los acelerómetros miden la gravedad y el movimiento del cuerpo» a la vez, de modo que cualquier aceleración propia contamina la estimación (Corke, 2023, pp. 112-113)."""))

C.append(code("""RUIDO_A = np.radians(2.0)                      # el inclinometro es ruidoso

theta_acc = theta_real + rng.normal(0, RUIDO_A, ti.size)
# ...y ademas se contamina cuando la plataforma acelera linealmente (Corke, pp. 112-113)
sacudida = (ti > 25) & (ti < 30)
theta_acc[sacudida] += np.radians(12.0)

print(f'Error RMS solo acelerómetro           : '
      f'{np.degrees(np.sqrt(((theta_acc-theta_real)**2).mean())):.2f} °')
print(f'Error RMS del acelerómetro fuera de la sacudida: '
      f'{np.degrees(np.sqrt(((theta_acc-theta_real)[~sacudida]**2).mean())):.2f} °')
print('Sin deriva, pero ruidoso y vulnerable a la aceleración propia.')"""))

C.append(md("""### Ejercicio 2

El bias de un giróscopo se puede estimar antes de arrancar: si el robot está quieto, la media de la salida del giróscopo *es* el bias. Calcula la media de `gyro` sobre los tres primeros segundos suponiendo que la plataforma estuviese inmóvil, réstala e integra de nuevo. ¿Cuánta deriva queda? ¿Por qué no desaparece del todo?"""))

C.append(code("""# Ejercicio 2: calibracion del bias en reposo
# pista: genera un tramo de reposo con omega_real = 0 y estima BIAS con su media
"""))

# ---------------- 4. Fusion complementaria
C.append(md("""## 4. Fusión complementaria: cada sensor donde es bueno

La salida de ingeniería es la fusión, que explota que «los distintos sensores tienen características complementarias»: el bias de los giróscopos hace crecer el error con el tiempo, pero en los acelerómetros solo causa un sesgo de orientación; los acelerómetros responden al movimiento de traslación y los buenos giróscopos no (Corke, 2023, p. 119).

El filtro complementario es la versión mínima de esa idea, y en una línea: pasa el giróscopo por un filtro paso alto y el acelerómetro por un paso bajo, de forma que las dos respuestas suman exactamente la unidad. El parámetro es una constante de tiempo τ que decide en qué frecuencia se cede el testigo de un sensor al otro. El estimador serio —el filtro de Kalman— es materia del bloque 6, pero hace conceptualmente lo mismo."""))

C.append(code("""def complementario(gyro, theta_acc, dt, tau):
    \"\"\"Filtro complementario: alto para el giroscopo, bajo para el acelerometro.\"\"\"
    alfa = tau / (tau + dt)
    th = np.empty_like(gyro); th[0] = theta_acc[0]
    for k in range(1, gyro.size):
        th[k] = alfa * (th[k-1] + gyro[k] * dt) + (1 - alfa) * theta_acc[k]
    return th

TAU_F = 1.0
theta_fus = complementario(gyro, theta_acc, DT_I, TAU_F)

def rms(x):
    return np.degrees(np.sqrt((x**2).mean()))

print(f'Error RMS  giróscopo integrado : {rms(theta_gyro - theta_real):6.2f} °')
print(f'Error RMS  acelerómetro solo   : {rms(theta_acc  - theta_real):6.2f} °')
print(f'Error RMS  fusión (τ = {TAU_F} s)   : {rms(theta_fus  - theta_real):6.2f} °')

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 3.4))
a1.plot(ti, np.degrees(theta_acc), color='lightgray', lw=1, label='acelerómetro')
a1.plot(ti, np.degrees(theta_gyro), color='crimson', lw=1.6, label='giróscopo integrado')
a1.plot(ti, np.degrees(theta_real), color='black', lw=2, label='real')
a1.plot(ti, np.degrees(theta_fus), color=IQS_AZUL, lw=2, label='fusión')
a1.set_xlabel('t [s]'); a1.set_ylabel('inclinación [°]'); a1.legend(fontsize=8)
a1.set_title('Las tres estimaciones')

taus = np.logspace(-1.3, 1.5, 40)
errores = [rms(complementario(gyro, theta_acc, DT_I, tt) - theta_real) for tt in taus]
a2.semilogx(taus, errores, color=IQS_VERDE, lw=2)
mejor = taus[int(np.argmin(errores))]
a2.axvline(mejor, color=IQS_AZUL, ls='--', lw=1.5, label=f'óptimo τ ≈ {mejor:.2f} s')
a2.set_xlabel('τ del filtro [s]'); a2.set_ylabel('error RMS [°]')
a2.legend(fontsize=8); a2.set_title('Sintonía del filtro complementario')
plt.tight_layout(); plt.show()"""))

C.append(md("""**Cómo leer la curva de la derecha.** Con τ muy pequeño el filtro es todo acelerómetro: hereda su ruido y su vulnerabilidad a la sacudida. Con τ muy grande es todo giróscopo: hereda la deriva. El mínimo existe porque los dos errores crecen en direcciones opuestas, y su posición depende del cociente entre el bias del giróscopo y el ruido del acelerómetro — que es exactamente la información que un filtro de Kalman codifica en sus matrices de covarianza.

### Ejercicio 3

Multiplica por diez el bias del giróscopo (`BIAS = np.radians(10.0)`) y vuelve a trazar la curva de sintonía. ¿Hacia dónde se desplaza el τ óptimo, y por qué? Repite ahora bajando el ruido del acelerómetro a 0,2° y explica el desplazamiento contrario."""))

C.append(code("""# Ejercicio 3: repite la generacion de gyro y theta_acc con los nuevos parametros
# y vuelve a evaluar 'errores' sobre el mismo vector 'taus'
"""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.** Con FS = 4000 Hz aparecen miles de saltos ambiguos en cuanto la velocidad supera unos 6 rad/s, y el ángulo final decodificado se queda muy corto porque cada salto de 2 se descarta como cero. La condición general es FS > 4·N·ω_máx/(2π), es decir, más de una muestra por estado de cuadratura; en la práctica se pide un factor de seguridad de 2 a 4 sobre esa cifra. Es literalmente la condición de Nyquist (De Silva et al., 2016, p. 152) aplicada a una señal cuadrada, y por eso los periféricos de encoder de los microcontroladores se implementan en hardware y no por interrupción.

**Ejercicio 2.** Restar la media medida en reposo elimina la mayor parte de la deriva —de sesenta grados se baja a unos pocos—, pero no toda: queda el error de estimación del propio bias, que es del orden del ruido dividido por la raíz del número de muestras promediadas, y sobre todo queda la parte del bias que cambia con el tiempo y la temperatura después de la calibración. Esa componente variable es precisamente la que Corke señala como el problema real (Corke, 2023, p. 118), y la que ninguna calibración inicial puede eliminar: hay que reestimarla en marcha, que es lo que hace un filtro con el bias en el vector de estado.

**Ejercicio 3.** Con un bias diez veces mayor el giróscopo se degrada mucho más rápido, así que el óptimo se desplaza hacia τ más pequeños: conviene ceder antes el testigo al acelerómetro. Al bajar el ruido del acelerómetro ocurre lo mismo por la otra razón — un acelerómetro mejor merece más peso—, y el τ óptimo vuelve a bajar. La regla cualitativa que hay que retener: τ óptimo crece con la calidad del giróscopo y decrece con la calidad del acelerómetro."""))

C.append(md("""---

## Para llevarse de esta sesión

El encoder y la IMU fallan de maneras opuestas, y esa oposición organiza toda la propiocepción del robot. El encoder cuantiza pero no deriva: su error está acotado por una cuenta para siempre, y su precio es no tener referencia absoluta al encender. La IMU no cuantiza pero deriva sin límite, porque integra un bias: su error crece linealmente en orientación y cuadráticamente en posición, y ninguna calibración de fábrica lo evita.

De ahí sale la única estrategia sensata, que es la que recorre el resto del curso: no buscar el sensor perfecto sino combinar sensores con defectos complementarios. El filtro complementario de este cuaderno tiene un parámetro y dos líneas; el filtro de Kalman del bloque 6 tendrá matrices y un modelo de ruido, pero responde a la misma pregunta — cuánto me creo a cada uno, y en qué banda de frecuencias.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S09_Encoders_IMU.ipynb', C)
print('escrito S09')
