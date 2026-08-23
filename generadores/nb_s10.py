from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('scipy','scipy'), ('matplotlib','matplotlib')]
C = []

C.append(cabecera(
    "S10", "Fuerza, tacto y rango: galgas, puente de Wheatstone y LiDAR 2D", "3",
    "viernes 2 de octubre de 2026", "2 h",
    "Recorre las dos mitades de la sesión con números. Primero la medida de fuerza: factor de galga, puente de Wheatstone en cuarto, medio y puente completo, y por qué la configuración importa tanto como la galga. Después un LiDAR 2D simulado sobre un mapa poligonal, con su barrido angular, su nube de puntos cartesiana y el efecto del ruido sobre lo que se puede extraer de ella.",
    "Fraden (2016), cap. 5 y cap. 9 — puente de Wheatstone (pp. 215-216), los cinco métodos de medir fuerza (p. 355), galga extensométrica y factor de galga (pp. 355-356), sensores táctiles (pp. 357-359), telemetría ultrasónica (p. 314); Corke (2023), caps. 1, 6 y 9 — sensores activos (p. 9), LiDAR (p. 241), ventajas e inconvenientes frente a cámaras (p. 242), sensores de par en la articulación (p. 364).",
    "los apuntes del bloque 3"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=4, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.2)
plt.rcParams['axes.grid'] = True
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('Listo.')"""))

# ---------------- 1. Galga extensometrica
C.append(md("""## 1. La galga extensométrica: de la fuerza a la deformación

Fraden cataloga cinco maneras de medir una fuerza, y concluye que «en los sensores modernos, el método más comúnmente usado» es medir la deformación producida por la fuerza en un miembro elástico (Fraden, 2016, p. 355). El sensor de esa deformación es la galga: «un sensor elástico resistivo cuya resistencia es función de la deformación aplicada», gobernada por el factor de galga en dR/R = Se·ε (Fraden, 2016, pp. 355-356). Para los metales habituales Se vale unos 2; el platino llega a 6 y los semiconductores alcanzan de −100 a +150, a costa de una sensibilidad térmica fuerte que exige compensación (Fraden, 2016, p. 356).

El elemento elástico de nuestro ejemplo es una viga en voladizo de acero con la galga pegada en la raíz, que es la geometría de casi cualquier célula de carga de laboratorio."""))

C.append(code("""E_ACERO = 210e9            # Pa
L, ANCHO, ESPESOR = 0.100, 0.020, 0.005      # m: viga en voladizo
SE_METAL = 2.0             # factor de galga del constantan (Fraden, p. 356)
SE_SEMI = 120.0            # galga de silicio (Fraden, p. 356)
R0 = 350.0                 # ohmios, valor nominal habitual

def deformacion(F):
    \"\"\"Deformacion en la raiz de la viga en voladizo, adimensional (m/m).\"\"\"
    I = ANCHO * ESPESOR**3 / 12
    return F * L * (ESPESOR / 2) / (E_ACERO * I)

F = np.linspace(0, 50, 200)          # rango de medida: 0-50 N
eps = deformacion(F)

print(f'Deformación a fondo de escala (50 N): {eps[-1]*1e6:.0f} microdeformaciones')
print(f'dR/R con galga metálica   (Se = {SE_METAL:5.1f}): {SE_METAL*eps[-1]*100:.4f} %  '
      f'-> ΔR = {SE_METAL*eps[-1]*R0*1000:.2f} mΩ sobre {R0:.0f} Ω')
print(f'dR/R con galga de silicio (Se = {SE_SEMI:5.1f}): {SE_SEMI*eps[-1]*100:.4f} %  '
      f'-> ΔR = {SE_SEMI*eps[-1]*R0*1000:.2f} mΩ')
print(f'\\nMedir un cambio del {SE_METAL*eps[-1]*100:.3f} % sobre {R0:.0f} Ω con un óhmetro no es'
      ' viable: de ahí el puente.')"""))

# ---------------- 2. Puente de Wheatstone
C.append(md("""## 2. El puente de Wheatstone y por qué la configuración lo es todo

Como la variación relativa de resistencia es minúscula, la lectura se hace en puente de Wheatstone, la «implementación popular y muy efectiva de la técnica ratiométrica»: cuatro impedancias con salida Vout = (Z1/(Z1+Z2) − Z3/(Z3+Z4))·Vref, nula en equilibrio y sensible al desequilibrio de cualquiera de las ramas (Fraden, 2016, pp. 215-216). De las derivadas parciales de esa ecuación sale la regla práctica del laboratorio: colocando dos o cuatro galgas activas en ramas adecuadas, las contribuciones útiles se suman y las derivas térmicas comunes se cancelan.

Escribimos el puente exacto —sin aproximar— y comparamos las tres configuraciones sobre el mismo elemento elástico."""))

C.append(code("""def puente(d1, d2, d3, d4, Vref=5.0):
    \"\"\"Puente de Wheatstone exacto (Fraden, pp. 215-216).
    d_i es la variacion relativa de cada brazo: Z_i = R0*(1+d_i).\"\"\"
    Z1, Z2, Z3, Z4 = (1 + d1), (1 + d2), (1 + d3), (1 + d4)
    return (Z1 / (Z1 + Z2) - Z3 / (Z3 + Z4)) * Vref

x = SE_METAL * eps                  # dR/R de una galga sometida a +eps

VREF = 5.0
v_cuarto = puente(x, 0, 0, 0, VREF)          # 1 galga activa
v_medio = puente(x, -x, 0, 0, VREF)          # 2 galgas activas, tracción y compresión
v_completo = puente(x, -x, -x, x, VREF)      # 4 galgas activas

print(f'Salida a 50 N con Vref = {VREF} V')
print(f'  cuarto de puente : {v_cuarto[-1]*1000:6.3f} mV   ({v_cuarto[-1]/VREF*1000:.3f} mV/V)')
print(f'  medio puente     : {v_medio[-1]*1000:6.3f} mV   ({v_medio[-1]/VREF*1000:.3f} mV/V)')
print(f'  puente completo  : {v_completo[-1]*1000:6.3f} mV   ({v_completo[-1]/VREF*1000:.3f} mV/V)')
print('\\nEl puente completo cuadruplica la sensibilidad sin cambiar de galga.')"""))

C.append(md("""Falta la mitad más importante del argumento, que es la temperatura. En el cuarto de puente solo un brazo es una galga pegada a la pieza: los otros tres son resistencias fijas que no ven ni el calor ni la dilatación del elemento elástico, de modo que cualquier cambio térmico se traduce en un desequilibrio indistinguible de una fuerza. En el puente completo los cuatro brazos son galgas sobre la misma pieza y a la misma temperatura, y el término común se cancela en la resta.

Le damos un número: 20 K de variación térmica con un coeficiente combinado —resistivo más dilatación diferencial— de 20 ppm/K."""))

C.append(code("""ALFA_T = 20e-6                       # variacion relativa de R por kelvin (combinada)
dT = np.linspace(-20, 20, 100)
delta = ALFA_T * dT                  # afecta por igual a todas las galgas pegadas

# a fuerza NULA: lo que el puente cree estar midiendo por culpa de la temperatura
falso_cuarto = puente(delta, 0, 0, 0, VREF)                 # 3 brazos son resistencias fijas
falso_completo = puente(delta, delta, delta, delta, VREF)   # 4 galgas a la misma temperatura

# convertir la salida espuria a la fuerza que aparentaria (usando la sensibilidad de cada montaje)
sens_cuarto = v_cuarto[-1] / 50.0
sens_completo = v_completo[-1] / 50.0
F_falsa_cuarto = falso_cuarto / sens_cuarto
F_falsa_completo = falso_completo / sens_completo

print(f'Error aparente a +20 K, cuarto de puente : {F_falsa_cuarto[-1]:8.2f} N '
      f'({100*abs(F_falsa_cuarto[-1])/50:.1f} % del fondo de escala)')
print(f'Error aparente a +20 K, puente completo  : {F_falsa_completo[-1]:8.2e} N  (se cancela)')

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 3.5))
a1.plot(F, v_cuarto*1000, color='crimson', lw=2, label='cuarto de puente')
a1.plot(F, v_medio*1000, color=IQS_VERDE, lw=2, label='medio puente')
a1.plot(F, v_completo*1000, color=IQS_AZUL, lw=2, label='puente completo')
a1.set_xlabel('fuerza [N]'); a1.set_ylabel('Vout [mV]')
a1.legend(fontsize=8); a1.set_title(f'Sensibilidad (Vref = {VREF} V)')

a2.plot(dT, F_falsa_cuarto, color='crimson', lw=2, label='cuarto de puente')
a2.plot(dT, F_falsa_completo, color=IQS_AZUL, lw=2, label='puente completo')
a2.axhline(0, color='black', lw=0.8)
a2.set_xlabel('variación de temperatura [K]'); a2.set_ylabel('fuerza aparente [N]')
a2.legend(fontsize=8); a2.set_title('Deriva térmica a fuerza nula')
plt.tight_layout(); plt.show()"""))

C.append(md("""**El resultado que hay que fijar.** El puente completo gana por dos motivos independientes: cuadruplica la señal y anula la deriva común. Esa es la razón de que la célula de carga comercial sea siempre un elemento elástico mecanizado con cuatro galgas en puente completo, y de que un montaje improvisado a un cuarto de puente en el laboratorio dé lecturas que se mueven solas cuando alguien abre la ventana.

El mismo hardware, escalado, es el que permite el control de par de los robots: estimar el par a partir de la corriente del motor es posible en teoría, pero «la fricción y otros efectos enmascaran la señal», por lo que «los robots más sofisticados llevan sensores de par integrados en sus actuadores de articulación» o una muñeca de fuerza-par entre el brazo y la herramienta (Corke, 2023, p. 364).

### Ejercicio 1

Repite el cálculo del cuarto de puente con una galga de silicio (`SE_SEMI = 120`). Comprueba dos cosas: cuánta señal ganas, y cuánta no linealidad aparece al comparar la salida exacta del puente con la aproximación Vout ≈ Vref·x/4. ¿Compensa la ganancia de señal?"""))

C.append(code("""# Ejercicio 1: galga de silicio en cuarto de puente
# x_semi = SE_SEMI * eps
# exacta = puente(x_semi, 0, 0, 0, VREF)   ;   aprox = VREF * x_semi / 4
"""))

# ---------------- 3. LiDAR: el mapa y el barrido
C.append(md("""## 3. Un LiDAR 2D sobre un mapa poligonal

Cambiamos de propioceptivo a exteroceptivo y de contacto a distancia. El principio es el de todo sensor de rango activo: emitir energía y medir la reflexión (Fraden, 2016, p. 314; Corke, 2023, p. 9). El LiDAR «emite pulsos cortos de luz láser infrarroja y mide el tiempo que tardan los pulsos reflejados en volver; el alcance operativo puede llegar a 100 m con exactitud del orden de centímetros», y el 2D es «un telémetro 1D que rota alrededor de un eje fijo y devuelve una sección plana del mundo en coordenadas polares», con resoluciones típicas de cuarto, medio o un grado (Corke, 2023, p. 241).

Simular esa sección plana es un problema de geometría elemental: lanzar un rayo por cada ángulo del barrido e intersecarlo con todos los segmentos del mapa, quedándose con el más cercano. El mapa es una nave en L con dos obstáculos."""))

C.append(code("""def poligono_a_segmentos(pts):
    \"\"\"Convierte una lista cerrada de vertices en pares (A, B) de segmentos.\"\"\"
    P = np.asarray(pts, float)
    return P, np.roll(P, -1, axis=0)

NAVE = [(0, 0), (8, 0), (8, 6), (4.5, 6), (4.5, 3.5), (0, 3.5)]
CAJA = [(2.0, 1.0), (3.0, 1.0), (3.0, 2.0), (2.0, 2.0)]
PILAR = [(6.0, 3.0), (6.6, 3.0), (6.6, 3.6), (6.0, 3.6)]

A_list, B_list = [], []
for poli in (NAVE, CAJA, PILAR):
    a, b = poligono_a_segmentos(poli)
    A_list.append(a); B_list.append(b)
SEG_A = np.vstack(A_list); SEG_B = np.vstack(B_list)

def cruz(u, v):
    return u[..., 0] * v[..., 1] - u[..., 1] * v[..., 0]

def barrido(origen, angulos, rango_max=20.0):
    \"\"\"Lanza un rayo por angulo y devuelve la distancia al obstaculo mas cercano.\"\"\"
    o = np.asarray(origen, float)
    r = np.stack([np.cos(angulos), np.sin(angulos)], axis=1)[:, None, :]   # (M,1,2)
    s = (SEG_B - SEG_A)[None, :, :]                                        # (1,K,2)
    q = (SEG_A - o)[None, :, :]
    den = cruz(r, s)
    with np.errstate(divide='ignore', invalid='ignore'):
        t = cruz(q, s) / den            # distancia a lo largo del rayo
        u = cruz(q, r) / den            # posicion dentro del segmento
    valido = (np.abs(den) > 1e-12) & (t > 1e-9) & (u >= 0) & (u <= 1)
    t = np.where(valido, t, np.inf)
    return np.minimum(t.min(axis=1), rango_max)

RES_ANG = 0.25                                    # grados por paso (Corke, p. 241)
ang = np.radians(np.arange(0, 360, RES_ANG))
ORIGEN = np.array([2.0, 2.6])

rangos = barrido(ORIGEN, ang)
print(f'Rayos por barrido : {ang.size} (resolución {RES_ANG}°)')
print(f'Distancia mínima  : {rangos.min():.3f} m')
print(f'Distancia máxima  : {rangos.max():.3f} m')"""))

C.append(md("""La conversión a nube de puntos cartesiana es la operación que todo el bloque 6 dará por hecha, y conviene hacerla una vez a mano: cada medida es un par (ángulo, distancia) en el sistema del sensor, y el punto es el origen del sensor más la distancia por el vector unitario del ángulo. Si el sensor está montado sobre un robot que se mueve, hay una transformación más — y ahí empieza el SLAM.

Añadimos el ruido que corresponde a un LiDAR real: unos dos centímetros de desviación típica y una pequeña fracción de rayos sin retorno, que en un equipo real son superficies negras, cristales o ángulos de incidencia rasantes."""))

C.append(code("""rng = np.random.default_rng(10)

SIGMA = 0.02              # 2 cm de ruido: exactitud del orden de centimetros (Corke, p. 241)
P_FALLO = 0.02            # 2 % de rayos sin retorno

rangos_ruido = rangos + rng.normal(0, SIGMA, rangos.size)
sin_retorno = rng.random(rangos.size) < P_FALLO
rangos_ruido[sin_retorno] = np.nan

def a_cartesianas(origen, angulos, r):
    return origen[0] + r * np.cos(angulos), origen[1] + r * np.sin(angulos)

xc, yc = a_cartesianas(ORIGEN, ang, rangos)
xn, yn = a_cartesianas(ORIGEN, ang, rangos_ruido)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 4.2))
for ax, (X, Y), tit in [(a1, (xc, yc), 'Barrido ideal'),
                        (a2, (xn, yn), f'Con ruido σ = {SIGMA*100:.0f} cm y {P_FALLO*100:.0f} % sin retorno')]:
    for a, b in zip(SEG_A, SEG_B):
        ax.plot([a[0], b[0]], [a[1], b[1]], color='black', lw=1.6)
    ax.scatter(X, Y, s=3, color=IQS_AZUL if ax is a1 else IQS_VERDE)
    ax.plot(*ORIGEN, marker='*', ms=14, color='crimson')
    ax.set_aspect('equal'); ax.set_title(tit, fontsize=10)
    ax.set_xlabel('x [m]'); ax.set_ylabel('y [m]')
plt.tight_layout(); plt.show()

print(f'Puntos válidos: {np.isfinite(rangos_ruido).sum()} de {rangos.size}')"""))

C.append(md("""**Lo que hay que comentar mirando las dos figuras.** A escala de la nave las dos nubes parecen idénticas: dos centímetros de ruido no se ven cuando la sala mide ocho metros. El problema del ruido no es cómo se ve, sino qué impide hacer — y eso es lo que medimos ahora.

### Ejercicio 2

Corke advierte de que el barrido tarda un tiempo finito y de que el sensor se mueve mientras tanto (Corke, 2023, p. 242). Modela ese efecto: haz que el origen del barrido se desplace linealmente 0,3 m en x a lo largo de los 360°, en vez de estar fijo. Dibuja la nube resultante sobre el mapa y explica qué le pasa a las paredes."""))

C.append(code("""# Ejercicio 2: barrido con el sensor en movimiento
# pista: recorre los angulos en un bucle y llama a barrido() con un origen que avance
"""))

# ---------------- 4. Efecto del ruido
C.append(md("""## 4. Qué estropea el ruido: extraer una pared de la nube

La nube de puntos casi nunca es el producto final. Lo que un robot hace con ella es extraer estructura —rectas que son paredes, discontinuidades que son esquinas u obstáculos— y esas operaciones sí notan los dos centímetros. Ajustamos una recta a los puntos que caen sobre la pared del fondo y comparamos los residuos con y sin ruido; después contamos cuántos rayos alcanzan el pilar, que es lo que decide si el robot lo ve o se lo lleva por delante."""))

C.append(code("""# --- 1. ajuste de la pared y = 3.5 (el tramo de la izquierda del techo de la L) ---
en_pared = (np.abs(yc - 3.5) < 0.05) & (xc > 0.3) & (xc < 4.2)
print(f'Puntos sobre esa pared: {en_pared.sum()}')

def residuo_recta(X, Y):
    m, c = np.polyfit(X, Y, 1)
    return np.sqrt(((Y - (m * X + c))**2).mean()), m

r_ideal, m_ideal = residuo_recta(xc[en_pared], yc[en_pared])
val = en_pared & np.isfinite(xn) & np.isfinite(yn)
r_ruido, m_ruido = residuo_recta(xn[val], yn[val])

print(f'Residuo RMS del ajuste, sin ruido: {r_ideal*1000:7.2f} mm  (pendiente {m_ideal:+.4f})')
print(f'Residuo RMS del ajuste, con ruido: {r_ruido*1000:7.2f} mm  (pendiente {m_ruido:+.4f})')
print(f'La pendiente estimada se desvía {np.degrees(np.arctan(abs(m_ruido))):.2f}° de la horizontal.')

# --- 2. cuantos rayos alcanzan el pilar, en funcion de la resolucion angular ---
print(f'\\n{"resolución":>12} | {"rayos/barrido":>13} | {"impactos en el pilar":>21}')
print('-' * 52)
for res in [0.25, 0.5, 1.0, 2.0]:
    a = np.radians(np.arange(0, 360, res))
    rg = barrido(ORIGEN, a)
    X, Y = a_cartesianas(ORIGEN, a, rg)
    dentro = (X > 5.9) & (X < 6.7) & (Y > 2.9) & (Y < 3.7)
    print(f'{res:11.2f}° | {a.size:13d} | {dentro.sum():21d}')"""))

C.append(md("""**Las dos lecciones del apartado.** La primera: sin ruido el residuo del ajuste es exactamente nulo, porque los puntos están sobre la recta; con ruido crece hasta el orden de la desviación típica del sensor. Pero el ruido de rango no desplaza la pared, la *engorda*, y el ajuste promedia ese engrosamiento sobre centenares de puntos, de modo que la pendiente estimada se desvía menos de una décima de grado. Promediar es lo que salva la extracción de estructura, y por eso las paredes largas se detectan bien y las esquinas mal.

La segunda: la resolución angular decide qué objetos existen para el robot. El pilar de 60 cm a cuatro metros recibe casi cuarenta rayos a 0,25° y solo cinco a 2°, y con cinco rayos ruidosos ningún algoritmo de agrupamiento lo declarará obstáculo con fiabilidad. Junto con las contras que enumera Corke —peor comportamiento a pleno sol porque el pulso de retorno queda sepultado por la luz infrarroja solar, tiempo finito de barrido, ausencia de textura y color, piezas móviles, volumen, consumo y coste (Corke, 2023, p. 242)— este es el catálogo de razones por las que ningún AMR comercial navega solo con un LiDAR 2D.

### Ejercicio 3

Deduce la distancia máxima a la que un objeto de 20 cm de ancho es alcanzado por al menos tres rayos, para resoluciones de 0,25°, 0,5° y 1°. Compruébalo numéricamente moviendo el pilar en el mapa, y contrasta el resultado con el tamaño de los obstáculos que el robot del laboratorio debe esquivar."""))

C.append(code("""# Ejercicio 3: separacion entre rayos a distancia d es aproximadamente d * res_en_radianes
# pista: exige 3 rayos -> el ancho del objeto debe cubrir al menos 2 separaciones
"""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.** La galga de silicio multiplica la señal por sesenta: el cuarto de puente pasa de unos 0,7 mV a más de 40 mV a fondo de escala, lo que hace casi innecesario el amplificador de instrumentación. El precio es la no linealidad: con x = Se·ε del orden de 3·10⁻², la salida exacta x/(2(2+x)) se aparta de la aproximación x/4 en torno al 1,5 % del fondo de escala, frente a un 0,03 % con la galga metálica; y a eso hay que sumarle la sensibilidad térmica del silicio, muy superior, que Fraden señala como su inconveniente característico (Fraden, 2016, p. 356). Compensa en aplicaciones de bajo coste con electrónica sencilla y compensación por software, y no compensa en una célula de carga de precisión.

**Ejercicio 2.** Las paredes dejan de cerrar: la nube aparece «abierta» en el ángulo donde empieza y termina el barrido, y los tramos rectos se inclinan levemente porque cada punto se ha medido desde un origen distinto pero se dibuja como si todos compartieran uno. Con 0,3 m de desplazamiento el error es del mismo orden que el tamaño de un obstáculo pequeño, muchísimo mayor que los 2 cm de ruido. Corregirlo exige conocer el movimiento durante el barrido y deshacerlo punto a punto —*deskewing*—, y es la razón por la que en un robot rápido el LiDAR se sincroniza con la odometría.

**Ejercicio 3.** La separación transversal entre rayos consecutivos a distancia d vale aproximadamente d·Δθ con Δθ en radianes. Para que un objeto de ancho w reciba al menos tres rayos hace falta w ≥ 2·d·Δθ, es decir d ≤ w/(2Δθ). Con w = 0,20 m: 22,9 m a 0,25°, 11,5 m a 0,5° y 5,7 m a 1°. La cifra parece generosa hasta que se recuerda que el objeto debe además reflejar bien y no estar en ángulo rasante; con ambas condiciones el alcance útil se reduce a menos de la mitad, y ahí es donde aparece la necesidad de combinar el LiDAR con otros sensores."""))

C.append(md("""---

## Para llevarse de esta sesión

En la medida de fuerza, el sensor casi nunca es el problema: la galga metálica lleva décadas siendo la misma y funciona. Lo que decide la calidad de la medida es la configuración del puente y el elemento elástico — cuántas galgas activas, dónde pegadas y con qué simetría térmica. Un cuarto de puente con la mejor galga del mercado es peor instrumento que un puente completo con galgas corrientes, y esa es la moraleja transferible: en instrumentación, la arquitectura vence al componente.

En la medida de rango, el LiDAR 2D da datos métricos, baratos y fiables en un plano, y su límite no es la exactitud de cada rango sino la geometría del muestreo: la resolución angular decide qué existe y qué no, y el tiempo finito de barrido introduce un error que crece con la velocidad del robot. Con esas dos ideas y la metodología de selección de los apuntes —especificar primero la medida, después mirar el catálogo— el ejercicio de selección de la segunda hora se resuelve solo.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S10_Fuerza_Tacto_Rango.ipynb', C)
print('escrito S10')
