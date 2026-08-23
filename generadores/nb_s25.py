from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('matplotlib','matplotlib'), ('opencv-python','cv2')]
C = []

C.append(cabecera(
    "S25", "Formación de imagen y calibración de cámara", "6",
    "viernes 6 de noviembre de 2026", "2 h",
    "Recorre el camino completo del modelo estenopeico: proyecta puntos 3D a píxeles con la matriz K, comprueba a mano que la profundidad se pierde, introduce y corrige la distorsión radial, y calibra una cámara con un tablero de ajedrez sintético generado aquí mismo, recuperando K con cv2.calibrateCamera y midiendo el error de reproyección.",
    "Corke (2023), cap. 13 — proyección perspectiva (p. 540), ecuaciones de proyección central (p. 542), forma lineal homogénea (p. 544), matriz intrínseca K (p. 546), factorización C = K·[R|t] (pp. 546-547), recuento de 11 parámetros y ambigüedad de escala (p. 548), distorsión de lente (p. 552), calibración por mínimos cuadrados (p. 554).",
    "los apuntes del bloque 6"))

C.append(instalacion(PKG, """import numpy as np
import cv2
import matplotlib.pyplot as plt
np.set_printoptions(precision=3, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.2)
plt.rcParams['axes.grid'] = True
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('OpenCV', cv2.__version__)"""))

# ---------------- 1. Proyeccion
C.append(md("""## 1. Del punto 3D al píxel: la matriz de cámara

El modelo estenopeico son dos divisiones. Con el plano de imagen a distancia *f* del origen de la cámara, un punto **P** = (X, Y, Z) expresado en el sistema de la cámara cae en u = f·X/Z, v = f·Y/Z (Corke, 2023, p. 542). Esa división por Z es la fuente de toda la no linealidad del bloque.

En coordenadas homogéneas la proyección «puede escribirse en forma lineal» p̃ ~ C·P̃ (Corke, 2023, p. 544), y la matriz de cámara se factoriza como **C = K·[R|t]**: los intrínsecos en K —focal en píxeles y punto principal (Corke, 2023, p. 546)— y los extrínsecos en la pose cámara-mundo (Corke, 2023, pp. 546-547). Empecemos construyendo K y proyectando un objeto conocido."""))

C.append(code("""def matriz_K(f_px, cx, cy):
    \"\"\"Matriz intrinseca 3x3 con pixeles cuadrados y sin sesgo.\"\"\"
    return np.array([[f_px, 0.0, cx],
                     [0.0, f_px, cy],
                     [0.0,  0.0, 1.0]])

def proyectar(P_mundo, K, R, t):
    \"\"\"P_mundo: (N,3) en metros. Devuelve pixeles (N,2) y la profundidad Z de cada punto.\"\"\"
    P_cam = (R @ P_mundo.T).T + t          # cambio de sistema: extrinsecos
    p_hom = (K @ P_cam.T).T                # intrinsecos, aun homogeneo
    Z = p_hom[:, 2]
    return p_hom[:, :2] / Z[:, None], Z    # la division por Z: proyeccion perspectiva

# --- una camara concreta: 640x480, focal 800 px ---
W, H = 640, 480
K = matriz_K(800.0, W / 2, H / 2)
R = np.eye(3)                              # camara alineada con el mundo
t = np.array([0.0, 0.0, 0.0])

# --- un objeto: cubo de 0.20 m de lado centrado 1 m delante de la camara ---
s = 0.10
esquinas = np.array([[x, y, z] for x in (-s, s) for y in (-s, s) for z in (-s, s)], float)
CUBO = esquinas + np.array([0.0, 0.0, 1.0])
ARISTAS = [(0,1),(0,2),(1,3),(2,3),(4,5),(4,6),(5,7),(6,7),(0,4),(1,5),(2,6),(3,7)]

px, Z = proyectar(CUBO, K, R, t)
print('K =\\n', K)
print('primera esquina: 3D', CUBO[0], '->  pixel', px[0].round(1), ' a Z =', Z[0], 'm')"""))

C.append(md("""La focal en píxeles es el único mando que controla el «zum». Duplicarla equivale a acercarse el doble sin moverse: el objeto ocupa el doble de píxeles, y el punto principal se queda quieto."""))

C.append(code("""def dibujar_cubo(ax, px, color, etiqueta):
    for i, j in ARISTAS:
        ax.plot(*zip(px[i], px[j]), color=color, lw=1.6)
    ax.plot([], [], color=color, lw=1.6, label=etiqueta)

fig, ax = plt.subplots(figsize=(6, 4.6))
for f_px, color in [(400.0, IQS_VERDE), (800.0, IQS_AZUL), (1600.0, 'crimson')]:
    p, _ = proyectar(CUBO, matriz_K(f_px, W/2, H/2), R, t)
    dibujar_cubo(ax, p, color, f'f = {f_px:.0f} px')
ax.scatter([W/2], [H/2], marker='+', s=120, color='black')
ax.text(W/2 + 8, H/2 + 12, 'punto principal', fontsize=8)
ax.set_xlim(0, W); ax.set_ylim(H, 0)          # el eje v de la imagen crece hacia abajo
ax.set_aspect('equal'); ax.legend(fontsize=8)
ax.set_xlabel('u [px]'); ax.set_ylabel('v [px]')
ax.set_title('El mismo cubo con tres distancias focales')
plt.tight_layout(); plt.show()"""))

# ---------------- 2. Perdida de profundidad
C.append(md("""## 2. Lo que la proyección destruye: la profundidad

Un píxel no corresponde a un punto del mundo sino a un **rayo completo**. Multiplicar las coordenadas de un punto por cualquier escalar λ > 0 no cambia su píxel: la cámara es un sensor de direcciones, no de distancias.

De ahí la ambigüedad fundamental de la proyección perspectiva que Corke enuncia explícitamente: un objeto grande y lejano y uno pequeño y cercano pueden producir exactamente la misma imagen (Corke, 2023, p. 548). Vamos a comprobarlo con números, porque es la frase que justifica todo lo que viene después (estéreo, SLAM, sensores de rango)."""))

C.append(code("""# El mismo cubo, escalado y alejado por el mismo factor lambda
for lam in [1.0, 2.0, 5.0]:
    p, Zs = proyectar(CUBO * lam, K, R, t)
    print(f'lambda = {lam:4.1f}  ->  lado = {0.20*lam:.2f} m,  Z = {Zs.mean():.2f} m,'
          f'  esquina 0 en pixel {p[0].round(2)}')

print('\\nLos pixeles son identicos: una sola vista no puede distinguir escala de distancia.')

# Y al reves: dado un pixel, que puntos del mundo lo generan?
u_obj = np.array([420.0, 180.0])
rayo = np.linalg.inv(K) @ np.array([u_obj[0], u_obj[1], 1.0])   # direccion en el sistema camara
print('\\nPixel', u_obj, '-> rayo (direccion unitaria):', (rayo/np.linalg.norm(rayo)).round(3))
for Zc in [0.5, 1.0, 3.0]:
    print(f'   a Z = {Zc:.1f} m el punto seria', (rayo/rayo[2]*Zc).round(3))"""))

C.append(md("""**Lo que hay que decir en clase.** La matriz K es invertible, así que de un píxel se recupera el rayo sin ninguna pérdida; lo que no se recupera es *dónde a lo largo del rayo*. Recuperar esa incógnita cuesta otra vista (estéreo, movimiento), otro sensor (lidar, ToF) o un modelo aprendido — y es exactamente la agenda de S27 y S31.

### Ejercicio 1

Un sensor de 1/2,5" tiene píxeles de 1,4 μm y la óptica montada es de 6 mm. Calcula la focal en píxeles que debería devolver la calibración y compárala con los 800 px que hemos supuesto. ¿Qué campo de visión horizontal tiene esa cámara con un sensor de 640 px de ancho?"""))

C.append(code("""# Ejercicio 1: escribe aqui el calculo
# f_px = f_mm / tamano_pixel_mm
# fov  = 2 * arctan(ancho_px / (2 * f_px))"""))

# ---------------- 3. Distorsion
C.append(md("""## 3. Distorsión de lente y su corrección

El modelo estenopeico ideal no basta con lentes reales: aparecen la distorsión radial (abarrilamiento y acorchetado) y la tangencial, que se tratan como «parámetros intrínsecos adicionales» (Corke, 2023, p. 552). El modelo que usa OpenCV actúa sobre las coordenadas normalizadas (x, y) = ((u−u₀)/f, (v−v₀)/f):

x_d = x·(1 + k₁r² + k₂r⁴ + k₃r⁶) + [tangencial],  con r² = x² + y²

Vamos a implementarlo a mano en las dos direcciones. La directa es una fórmula; la inversa —quitar la distorsión— **no tiene forma cerrada** y se resuelve iterando, detalle que casi nadie cuenta y que explica por qué `cv2.undistort` es más caro de lo que parece."""))

C.append(code("""def distorsionar_norm(x, y, d):
    \"\"\"Coordenadas normalizadas ideales -> distorsionadas. d = (k1, k2, p1, p2, k3).\"\"\"
    k1, k2, p1, p2, k3 = d
    r2 = x*x + y*y
    radial = 1 + k1*r2 + k2*r2**2 + k3*r2**3
    xd = x*radial + 2*p1*x*y + p2*(r2 + 2*x*x)
    yd = y*radial + p1*(r2 + 2*y*y) + 2*p2*x*y
    return xd, yd

def desdistorsionar_pixel(u, v, K, d, iteraciones=8):
    \"\"\"Pixel distorsionado -> pixel ideal. Punto fijo: no hay solucion cerrada.\"\"\"
    x = (u - K[0, 2]) / K[0, 0]; y = (v - K[1, 2]) / K[1, 1]
    x0, y0 = x.copy(), y.copy()
    k1, k2, p1, p2, k3 = d
    for _ in range(iteraciones):
        r2 = x*x + y*y
        radial = 1 + k1*r2 + k2*r2**2 + k3*r2**3
        dx = 2*p1*x*y + p2*(r2 + 2*x*x)
        dy = p1*(r2 + 2*y*y) + 2*p2*x*y
        x = (x0 - dx) / radial
        y = (y0 - dy) / radial
    return K[0, 0]*x + K[0, 2], K[1, 1]*y + K[1, 2]

DIST = np.array([-0.30, 0.10, 0.0, 0.0, 0.0])    # abarrilamiento fuerte, sin tangencial

# Comprobacion de coherencia ida y vuelta sobre una rejilla de pixeles
u0, v0 = np.meshgrid(np.linspace(20, W-20, 9), np.linspace(20, H-20, 7))
xn, yn = (u0 - K[0,2])/K[0,0], (v0 - K[1,2])/K[1,1]
xd, yd = distorsionar_norm(xn, yn, DIST)
ud, vd = K[0,0]*xd + K[0,2], K[1,1]*yd + K[1,2]
ur, vr = desdistorsionar_pixel(ud, vd, K, DIST)
print('Error maximo del ida y vuelta:', np.abs(np.hypot(ur-u0, vr-v0)).max().round(6), 'px')
print('Desplazamiento maximo por distorsion:', np.hypot(ud-u0, vd-v0).max().round(1), 'px')"""))

C.append(md("""Un desplazamiento de decenas de píxeles en las esquinas no es cosmético: arruina la triangulación y sesga la odometría visual. Se ve mejor dibujando la rejilla ideal y la distorsionada juntas."""))

C.append(code("""fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.0))
for ax, (X, Y, tit) in zip((a1, a2),
        [(u0, v0, 'rejilla ideal (estenopeica)'), (ud, vd, f'con k1={DIST[0]}, k2={DIST[1]}')]):
    for i in range(X.shape[0]):
        ax.plot(X[i, :], Y[i, :], color=IQS_AZUL, lw=1.2)
    for j in range(X.shape[1]):
        ax.plot(X[:, j], Y[:, j], color=IQS_AZUL, lw=1.2)
    ax.set_xlim(-40, W+40); ax.set_ylim(H+40, -40); ax.set_aspect('equal'); ax.set_title(tit)
a2.quiver(u0, v0, ud-u0, vd-v0, color=IQS_VERDE, angles='xy', scale_units='xy', scale=1, width=0.004)
plt.tight_layout(); plt.show()"""))

# ---------------- 4. Damero sintetico
C.append(md("""## 4. Un tablero de ajedrez sintético (sin descargar nada)

Para calibrar hacen falta varias vistas de un damero plano en poses variadas — el método de Zhang que implementa `cv2.calibrateCamera`. Aquí las **generamos nosotros**, lo cual tiene una ventaja pedagógica enorme: conocemos la verdad de terreno y podremos comprobar si la calibración la recupera.

La receta: dibujar el damero como textura plana, mapearlo al plano de imagen con la homografía H = K·[r₁ r₂ t] (es la matriz de cámara con Z = 0, porque el tablero es plano), y aplicarle después la distorsión con el mapa inverso de la sección anterior."""))

C.append(code("""NX, NY, LADO = 9, 6, 0.025       # esquinas interiores en x, en y, y lado del cuadro en metros
PX, MARGEN = 60, 60              # pixeles por cuadro en la textura y margen blanco

def textura_damero():
    ancho, alto = (NX+1)*PX, (NY+1)*PX
    t = np.full((alto + 2*MARGEN, ancho + 2*MARGEN), 255, np.uint8)   # margen blanco: lo exige el detector
    for i in range(NY+1):
        for j in range(NX+1):
            if (i + j) % 2 == 0:
                t[MARGEN+i*PX:MARGEN+(i+1)*PX, MARGEN+j*PX:MARGEN+(j+1)*PX] = 30
    return t

TEX = textura_damero()
ESCALA = np.array([[LADO/PX, 0, -MARGEN*LADO/PX],       # pixel de textura -> (X, Y, 1) del tablero
                   [0, LADO/PX, -MARGEN*LADO/PX],
                   [0, 0, 1.0]])

# Mapa fijo de distorsion: para cada pixel de SALIDA, de que pixel ideal viene
_u, _v = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
MAPX, MAPY = desdistorsionar_pixel(_u, _v, K, DIST)
MAPX, MAPY = MAPX.astype(np.float32), MAPY.astype(np.float32)

def vista_damero(rvec, tvec, rng=None, con_distorsion=True):
    Rv, _ = cv2.Rodrigues(np.asarray(rvec, float))
    Hom = K @ np.column_stack([Rv[:, 0], Rv[:, 1], np.asarray(tvec, float)]) @ ESCALA
    img = cv2.warpPerspective(TEX, Hom, (W, H), flags=cv2.INTER_LINEAR,
                              borderMode=cv2.BORDER_CONSTANT, borderValue=170)
    if con_distorsion:
        img = cv2.remap(img, MAPX, MAPY, cv2.INTER_LINEAR,
                        borderMode=cv2.BORDER_CONSTANT, borderValue=170)
    if rng is not None:                                  # ruido de sensor, para que no sea de juguete
        img = np.clip(img.astype(np.float32) + rng.normal(0, 2.0, img.shape), 0, 255).astype(np.uint8)
    return img

rng = np.random.default_rng(25)
POSES = []
for dx, dy in [(-0.06, -0.04), (0.06, -0.04), (-0.06, 0.04), (0.06, 0.04), (0.0, 0.0), (0.0, 0.0)]:
    for s in (-1, 1):                                    # inclinaciones a un lado y a otro
        POSES.append((np.array([s*0.26, s*0.24*np.sign(dx if dx else 1.0), s*0.10]) + rng.normal(0, 0.05, 3),
                      np.array([-0.125+dx, -0.0875+dy, 0.55+0.06*s]) + rng.normal(0, 0.01, 3)))

VISTAS = [vista_damero(rv, tv, rng) for rv, tv in POSES]
print(len(VISTAS), 'vistas generadas de', VISTAS[0].shape, 'px')"""))

C.append(code("""fig, axes = plt.subplots(2, 4, figsize=(11, 5.0))
for ax, img in zip(axes.ravel(), VISTAS):
    ax.imshow(img, cmap='gray', vmin=0, vmax=255); ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
fig.suptitle('Ocho de las doce vistas sintéticas del damero (con distorsión y ruido)', fontsize=10)
plt.tight_layout(); plt.show()"""))

# ---------------- 5. Calibracion
C.append(md("""## 5. Calibrar: recuperar K y medir el error de reproyección

La calibración es «la estimación de los parámetros de la transformación perspectiva» (Corke, 2023, p. 540). El procedimiento tiene tres pasos y ni uno más:

1. **Detectar** las esquinas interiores del damero en cada vista (`findChessboardCorners` + `cornerSubPix` para llevarlas a precisión subpíxel).
2. **Emparejar** cada esquina detectada con su coordenada 3D conocida sobre el plano del tablero (Z = 0 por construcción).
3. **Resolver** el problema de mínimos cuadrados que da K, los coeficientes de distorsión y una pose por vista — el mismo espíritu que la solución lineal clásica con diana 3D (ec. 13.16; Corke, 2023, p. 554), pero no lineal y con varias vistas.

Fijamos `CALIB_FIX_K3` y `CALIB_ZERO_TANGENT_DIST` porque sabemos que nuestra cámara sintética no tiene ni k₃ ni tangencial: pedirle a un ajuste que estime parámetros que valen cero solo añade varianza."""))

C.append(code("""# Coordenadas 3D de las esquinas interiores, en el sistema del tablero (Z = 0)
objp = np.zeros((NX*NY, 3), np.float32)
objp[:, :2] = np.mgrid[0:NX, 0:NY].T.reshape(-1, 2) * LADO
objp[:, :2] += LADO                       # la primera esquina interior esta a un cuadro del borde

puntos_3d, puntos_2d, usadas = [], [], []
for i, img in enumerate(VISTAS):
    encontrado, esquinas = cv2.findChessboardCorners(img, (NX, NY), None)
    if not encontrado:
        continue
    cv2.cornerSubPix(img, esquinas, (7, 7), (-1, -1),
                     (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01))
    puntos_3d.append(objp.copy()); puntos_2d.append(esquinas); usadas.append(i)

print(f'Damero detectado en {len(usadas)} de {len(VISTAS)} vistas '
      f'({NX*NY} esquinas por vista, {len(usadas)*NX*NY} correspondencias en total)')

banderas = cv2.CALIB_FIX_K3 | cv2.CALIB_ZERO_TANGENT_DIST
err_rms, K_est, dist_est, rvecs, tvecs = cv2.calibrateCamera(
    puntos_3d, puntos_2d, (W, H), None, None, flags=banderas)

print(f'\\nError de reproyeccion RMS = {err_rms:.3f} px  (el criterio practico es < 0.5 px)')
print('\\nK estimada:\\n', K_est.round(2))
print('\\nK verdadera:\\n', K.round(2))
print('\\nk1, k2 estimados:', dist_est.ravel()[:2].round(4), '   verdaderos:', DIST[:2])"""))

C.append(md("""La comprobación que pide el guion de la sesión no es mirar el RMS global, sino **el error de reproyección vista a vista**: si una vista destaca sobre las demás, ahí hay una detección mala o un damero que no era plano."""))

C.append(code("""errores = []
for i in range(len(puntos_3d)):
    proy, _ = cv2.projectPoints(puntos_3d[i], rvecs[i], tvecs[i], K_est, dist_est)
    errores.append(float(np.sqrt(((proy - puntos_2d[i])**2).sum(axis=2).mean())))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.6))
a1.bar(range(len(errores)), errores, color=IQS_AZUL)
a1.axhline(err_rms, color='crimson', ls='--', lw=1.4, label=f'RMS global {err_rms:.3f} px')
a1.set_xlabel('vista'); a1.set_ylabel('error [px]'); a1.legend(fontsize=8)
a1.set_title('Error de reproyección por vista')

# Correccion de la distorsion en una vista, con la calibracion recien obtenida
corregida = cv2.undistort(VISTAS[usadas[0]], K_est, dist_est)
a2.imshow(np.hstack([VISTAS[usadas[0]], corregida]), cmap='gray', vmin=0, vmax=255)
a2.set_title('Vista original  |  corregida con undistort'); a2.set_xticks([]); a2.set_yticks([])
a2.grid(False)
plt.tight_layout(); plt.show()

print('Error relativo en la focal:', f'{100*abs(K_est[0,0]-K[0,0])/K[0,0]:.2f} %')
print('Error en el punto principal:',
      round(float(np.hypot(K_est[0,2]-K[0,2], K_est[1,2]-K[1,2])), 2), 'px')"""))

C.append(md("""### Ejercicio 2

Repite la calibración usando **solo tres vistas** (`puntos_3d[:3]`, `puntos_2d[:3]`) y luego solo las tres vistas frontales sin inclinación. Compara la K recuperada y el RMS con los de las doce vistas. ¿Qué falla exactamente cuando el damero no se inclina?

### Ejercicio 3

Quita las banderas (`flags=0`) para que el ajuste estime también k₃ y los coeficientes tangenciales, que en nuestra cámara sintética valen exactamente cero. ¿Baja el RMS? ¿Mejora K? Piensa qué implica esa disociación al calibrar una cámara real, donde no conoces la verdad."""))

C.append(code("""# Ejercicios 2 y 3: prueba aqui
# err3, K3, d3, _, _ = cv2.calibrateCamera(puntos_3d[:3], puntos_2d[:3], (W, H), None, None, flags=banderas)
# print(err3, K3[0,0])"""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.** f_px = 6 mm / 0,0014 mm = **4286 px**, muy lejos de los 800 px del ejemplo: con esa óptica y ese sensor la cámara es teleobjetivo. El campo de visión horizontal con 640 px de ancho sería 2·arctan(640/(2·4286)) ≈ **8,5°**. La moraleja es la comprobación que pide el guion: la focal que devuelve la calibración debe cuadrar con la focal física dividida por el tamaño de píxel; si no cuadra por un factor de 2, casi siempre es que se está calibrando a media resolución.

**Ejercicio 2.** Con tres vistas el RMS *baja* (menos datos, más fácil de ajustar) mientras que la K empeora: el RMS mide el ajuste, no la exactitud. Con vistas solo frontales el problema es de observabilidad: si el tablero es paralelo al sensor en todas las vistas, la focal y la distancia al tablero son casi indistinguibles (acercar la cámara o alargar la focal producen la misma imagen — es la ambigüedad de escala de la sección 2, Corke, 2023, p. 548). Inclinar el damero es lo que rompe esa degeneración, y por eso todas las recetas prácticas insisten en ello.

**Ejercicio 3.** El RMS baja ligeramente porque hay más parámetros libres para absorber el ruido, pero k₃ y los tangenciales se ajustan a valores no nulos que compensan entre sí, y K suele empeorar. Es sobreajuste puro y duro. En una cámara real la única defensa es validar con vistas que no hayan entrado en el ajuste, y desconfiar de los modelos de distorsión de orden alto salvo con ópticas de ojo de pez."""))

C.append(md("""---

## Para llevarse de esta sesión

La cámara es un **sensor de rayos**, no de distancias. K es invertible y de un píxel se recupera exactamente la dirección; lo que se pierde para siempre en una sola vista es la posición a lo largo de esa dirección. Todo el bloque 6 puede leerse como distintas maneras de recuperar esa incógnita.

Once parámetros describen una cámara: cinco intrínsecos y seis extrínsecos (Corke, 2023, p. 548), más los coeficientes de distorsión. Calibrar es estimarlos, y el error de reproyección es la única métrica honesta de si ha salido bien — con la advertencia de que un RMS bajo con pocas vistas o vistas poco variadas no significa nada.

Y una frontera que conviene dejar clara antes de S27: por muy aprendida que sea la percepción, convertir píxeles en metros sigue pasando por K. La geometría de esta sesión no se aprende, se mide.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S25_Formacion_Imagen_Calibracion.ipynb', C)
print('escrito S25')
