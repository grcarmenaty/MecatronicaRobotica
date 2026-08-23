from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('matplotlib','matplotlib'), ('opencv-python','cv2')]
C = []

C.append(cabecera(
    "S26", "Procesado clásico de imagen", "6",
    "miércoles 11 de noviembre de 2026", "1 h",
    "Recorre la cadena clásica completa sobre una escena sintética generada aquí mismo: convolución a mano y filtro gaussiano, gradiente y Canny, umbralizado con componentes conexas y sus momentos (área y centroide), y detección de esquinas de Harris.",
    "Corke (2023), caps. 11 y 12 — convolución (p. 441), galería de núcleos (p. 444), suavizado media frente a gaussiana (pp. 442-443), bordes (p. 446), Sobel y derivada de gaussiana (p. 448), Canny (p. 450), comparación (p. 452), blobs y sus descriptores (pp. 502-504), puntos de interés (p. 514), criterio de Harris (p. 516), SIFT (p. 523).",
    "los apuntes del bloque 6"))

C.append(instalacion(PKG, """import numpy as np
import cv2
import matplotlib.pyplot as plt
np.set_printoptions(precision=3, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.2)
plt.rcParams['axes.grid'] = False
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('OpenCV', cv2.__version__)"""))

# ---------------- 1. La escena y la convolucion
C.append(md("""## 1. La escena sintética y la convolución

No descargamos ninguna imagen: fabricamos una escena que se parece a lo que ve una cámara sobre una mesa de laboratorio —piezas claras sobre un fondo con gradiente de iluminación y ruido de sensor—. Tener la verdad de terreno permite comprobar si cada operador hace lo que decimos que hace.

La primera familia de operadores es la convolución: cada píxel de salida es función de una ventana w×w de la entrada, y cuando esa función es lineal la operación es O = K ⊛ I con núcleo K (ec. 11.1; Corke, 2023, p. 441). Su potencia está en que un único mecanismo cubre familias enteras de operaciones: el núcleo «puede elegirse para realizar funciones como suavizado, cálculo de gradiente o detección de bordes» (Corke, 2023, p. 441)."""))

C.append(code("""H, W = 400, 520
rng = np.random.default_rng(26)

def escena():
    u = np.arange(W)[None, :]
    img = 70 + 45 * (u / W) * np.ones((H, 1))            # gradiente de iluminacion
    cv2.rectangle(img, (40, 60), (200, 180), 215, -1)     # pieza rectangular
    cv2.circle(img, (330, 115), 55, 200, -1)              # pieza redonda
    cv2.drawContours(img, [np.array([[90, 350], [200, 350], [145, 240]])], 0, 230, -1)  # triangulo
    cv2.rectangle(img, (280, 230), (400, 290), 195, -1)   # pieza en L: dos rectangulos
    cv2.rectangle(img, (340, 230), (400, 360), 195, -1)
    cv2.circle(img, (460, 330), 26, 225, -1)              # pieza pequena
    img += rng.normal(0, 6.0, img.shape)                  # ruido de sensor
    return np.clip(img, 0, 255).astype(np.uint8)

I = escena()
print('Imagen', I.shape, I.dtype, ' rango', I.min(), '-', I.max())
print('Un trozo del array de pixeles (fila 100, columnas 30-40):\\n', I[100, 30:41])"""))

C.append(code("""def convolucion(I, nucleo):
    \"\"\"Correlacion 2D a mano: suma ponderada de versiones desplazadas de la imagen.
    Es lo que hace cv2.filter2D; la convolucion estricta usaria el nucleo volteado.\"\"\"
    kh, kw = nucleo.shape
    ph, pw = kh // 2, kw // 2
    Ip = np.pad(I.astype(float), ((ph, ph), (pw, pw)), mode='edge')
    O = np.zeros(I.shape, float)
    for i in range(kh):
        for j in range(kw):
            O += nucleo[i, j] * Ip[i:i+I.shape[0], j:j+I.shape[1]]
    return O

# La galeria de nucleos habituales (Corke, 2023, p. 444)
K_media  = np.ones((11, 11)) / 121
K_gauss  = cv2.getGaussianKernel(11, 2.5) @ cv2.getGaussianKernel(11, 2.5).T
K_sobel  = np.array([[-1., 0., 1.], [-2., 0., 2.], [-1., 0., 1.]])
K_lapl   = np.array([[0., 1., 0.], [1., -4., 1.], [0., 1., 0.]])

# Comprobacion: nuestra implementacion coincide con OpenCV
mia = convolucion(I, K_gauss)
suya = cv2.filter2D(I.astype(float), -1, K_gauss, borderType=cv2.BORDER_REPLICATE)
print('Diferencia maxima con cv2.filter2D:', np.abs(mia - suya).max().round(9))
print('Suma de los nucleos suavizadores:', K_media.sum().round(3), K_gauss.sum().round(3),
      ' | de los derivadores:', K_sobel.sum().round(3), K_lapl.sum().round(3))"""))

C.append(md("""Esa última línea contiene una regla de oro: **los núcleos que suavizan suman 1** (conservan el nivel medio de gris) y **los que derivan suman 0** (una zona uniforme les da respuesta nula). Si un núcleo escrito a mano no cumple la suya, hay una errata.

La comparación clásica es media frente a gaussiana: la media 11×11 promedia la ventana pero introduce artefactos direccionales, mientras que la gaussiana suaviza de forma isótropa (Corke, 2023, pp. 442-443)."""))

C.append(code("""salidas = [(I, 'original'), (convolucion(I, K_media), 'media 11×11'),
           (convolucion(I, K_gauss), 'gaussiana σ = 2,5'),
           (convolucion(I, K_lapl), 'laplaciano (deriva: suma 0)')]

fig, axes = plt.subplots(1, 4, figsize=(13, 3.2))
for ax, (S, tit) in zip(axes, salidas):
    ax.imshow(S, cmap='gray'); ax.set_title(tit, fontsize=9); ax.set_xticks([]); ax.set_yticks([])
plt.tight_layout(); plt.show()

# Cuanto ruido quita cada uno: desviacion tipica en un trozo de fondo sin piezas
trozo = (slice(320, 360), slice(215, 255))
for S, tit in salidas[:3]:
    print(f'{tit:22s} sigma del fondo = {np.std(S[trozo]):5.2f}')"""))

# ---------------- 2. Gradiente y Canny
C.append(md("""## 2. Gradiente, magnitud y Canny

«Con frecuencia nos interesa encontrar los bordes de los objetos de una escena» (Corke, 2023, p. 446): un borde es una transición rápida de intensidad, es decir, un máximo de la magnitud del gradiente. El gradiente se obtiene por convolución con núcleos de Sobel o con derivadas de gaussiana (fig. 11.18; Corke, 2023, p. 448).

Derivar amplifica el ruido de alta frecuencia, así que **siempre** se suaviza antes: es el mismo σ de la sección anterior, actuando ahora como parámetro de escala."""))

C.append(code("""Isuave = cv2.GaussianBlur(I, (0, 0), 2.0)

Gu = convolucion(Isuave, K_sobel)         # derivada en u (columnas)
Gv = convolucion(Isuave, K_sobel.T)       # derivada en v (filas)
mag = np.hypot(Gu, Gv)
ang = np.arctan2(Gv, Gu)

# Canny: magnitud + direccion + supresion de no maximos + histeresis (Corke, 2023, p. 450)
bordes_canny = cv2.Canny(Isuave, 40, 110)
bordes_crudos = (mag > 0.35 * mag.max()).astype(np.uint8) * 255

fig, axes = plt.subplots(1, 4, figsize=(13, 3.2))
for ax, (S, tit, cm) in zip(axes, [
        (Gu, 'gradiente en u', 'gray'), (mag, 'magnitud |∇I|', 'gray'),
        (bordes_crudos, 'umbral sobre la magnitud', 'gray'), (bordes_canny, 'Canny', 'gray')]):
    ax.imshow(S, cmap=cm); ax.set_title(tit, fontsize=9); ax.set_xticks([]); ax.set_yticks([])
plt.tight_layout(); plt.show()

print('Pixeles marcados como borde:  umbral crudo =', int((bordes_crudos > 0).sum()),
      ' | Canny =', int((bordes_canny > 0).sum()))"""))

C.append(md("""La comparación es la de la fig. 11.20 del libro (Corke, 2023, p. 452), y la aportación de Canny se ve de un vistazo: bordes de un píxel de grosor, conectados y con muchas menos respuestas espurias, gracias a la supresión de no máximos y al umbral con histéresis que encadena píxeles entre el umbral alto y el bajo (Corke, 2023, p. 450).

### Ejercicio 1

Ejecuta `cv2.Canny` sobre `I` **sin suavizar** y con σ = 5. Cuenta píxeles de borde en cada caso y mira las tres imágenes juntas. Después mueve los umbrales a (10, 30) y a (100, 200) manteniendo σ = 2. ¿Cuál de los dos mandos —la escala σ o los umbrales— controla qué se detecta y cuál controla cuánto?"""))

C.append(code("""# Ejercicio 1: prueba aqui
# for sigma in [0.0, 2.0, 5.0]:
#     J = I if sigma == 0 else cv2.GaussianBlur(I, (0, 0), sigma)
#     print(sigma, int((cv2.Canny(J, 40, 110) > 0).sum()))"""))

# ---------------- 3. Umbral y componentes conexas
C.append(md("""## 3. Del píxel a la pieza: umbral, componentes conexas y momentos

La segunda familia clásica agrupa píxeles homogéneos en regiones con significado. La cadena elemental es binarizar con un umbral —fijo, de Otsu o adaptativo— y etiquetar las componentes conexas; de cada blob se extraen área, centroide, caja englobante, relación de aspecto y circularidad (Corke, 2023, pp. 502-504).

El centroide sale de los **momentos** de la región: m₀₀ es el área, y el centroide es (m₁₀/m₀₀, m₀₁/m₀₀). Vamos a calcularlos a mano y a comprobarlos contra `cv2.moments`."""))

C.append(code("""umbral, binaria = cv2.threshold(cv2.GaussianBlur(I, (0, 0), 1.5), 0, 255,
                                cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print('Umbral elegido por Otsu:', umbral)

n, etiquetas, stats, centroides = cv2.connectedComponentsWithStats(binaria, connectivity=8)
print('Componentes conexas (incluido el fondo):', n)

def momentos_a_mano(mascara):
    \"\"\"m00 = area, m10 y m01 = primeros momentos -> centroide.\"\"\"
    v, u = np.nonzero(mascara)
    m00 = float(v.size)
    return m00, u.sum() / m00, v.sum() / m00

filas = []
for k in range(1, n):                      # la etiqueta 0 es el fondo
    mascara = (etiquetas == k).astype(np.uint8)
    area, cu, cv_ = momentos_a_mano(mascara)
    if area < 300:                         # descartar motas de ruido
        continue
    M = cv2.moments(mascara, binaryImage=True)
    contorno = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0][0]
    perim = cv2.arcLength(contorno, True)
    circularidad = 4 * np.pi * area / perim**2          # 1.0 = circulo perfecto
    x, y, w, h = stats[k, :4]
    filas.append((k, area, cu, cv_, M['m00'], w / h, circularidad))

print(f'\\n{"id":>3} {"área px":>9} {"cu":>7} {"cv":>7} {"m00 cv2":>9} {"asp.":>6} {"circ.":>6}')
for f in filas:
    print(f'{f[0]:3d} {f[1]:9.0f} {f[2]:7.1f} {f[3]:7.1f} {f[4]:9.0f} {f[5]:6.2f} {f[6]:6.2f}')"""))

C.append(md("""La columna `m00 cv2` reproduce exactamente nuestro recuento de píxeles: el «área» de un blob binario no es más que contar. Y la circularidad separa sin ambigüedad los círculos (≈ 1) del triángulo y de la pieza en L (mucho menor), que es el tipo de criterio con el que se filtran y ordenan colecciones de blobs en una célula industrial."""))

C.append(code("""fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.2))
a1.imshow(binaria, cmap='gray'); a1.set_title(f'binaria (Otsu, umbral = {umbral:.0f})', fontsize=9)

a2.imshow(etiquetas, cmap='tab10'); a2.set_title('componentes conexas y centroides', fontsize=9)
for k, area, cu, cv_, _, _, circ in filas:
    a2.plot(cu, cv_, marker='+', ms=13, mew=2.2, color='white')
    a2.text(cu + 8, cv_ - 8, f'{int(area)} px\\nc={circ:.2f}', color='white', fontsize=7)
for ax in (a1, a2):
    ax.set_xticks([]); ax.set_yticks([])
plt.tight_layout(); plt.show()"""))

C.append(md("""**El puente entre imagen y acción.** El centroide en píxeles, combinado con la K calibrada en S25 y la hipótesis de que la pieza está sobre un plano conocido, se convierte en una posición métrica sobre la mesa: es la cadena completa de un *pick-and-place* con visión 2D industrial. La fragilidad también hay que enseñarla, y es lo que pide el ejercicio siguiente.

### Ejercicio 2

Cambia la iluminación de la escena sumando un gradiente mucho más fuerte (por ejemplo `I2 = np.clip(I.astype(float) + 90*np.arange(W)/W, 0, 255).astype(np.uint8)`) y vuelve a aplicar Otsu. ¿Cuántos blobs sobreviven? Prueba después con `cv2.adaptiveThreshold`. Este es exactamente el fallo que la S27 usará como gancho."""))

C.append(code("""# Ejercicio 2: prueba aqui
# I2 = np.clip(I.astype(float) + 90*np.arange(W)/W, 0, 255).astype(np.uint8)
# _, b2 = cv2.threshold(I2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)"""))

# ---------------- 4. Esquinas
C.append(md("""## 4. Puntos de interés: el detector de Harris

La tercera familia no busca objetos sino **anclas geométricas**: «puntos salientes, puntos clave o puntos de esquina» que puedan reencontrarse de forma fiable entre imágenes distintas de la misma escena (Corke, 2023, p. 514).

El criterio se lee en los autovalores de la matriz de estructura local (sumas de productos de gradientes en una ventana): dos autovalores pequeños = zona plana; uno grande y otro pequeño = borde; los dos grandes = esquina (Corke, 2023, p. 516). Harris opera con una función de los autovalores que evita calcularlos explícitamente. Vamos a construir la matriz de estructura a mano para ver ese criterio en tres puntos elegidos a dedo."""))

C.append(code("""Ix = cv2.Sobel(Isuave.astype(float), cv2.CV_64F, 1, 0, ksize=3)
Iy = cv2.Sobel(Isuave.astype(float), cv2.CV_64F, 0, 1, ksize=3)

def matriz_estructura(u, v, w=7):
    \"\"\"M = suma en la ventana de [[Ix2, IxIy], [IxIy, Iy2]].\"\"\"
    s = (slice(v-w, v+w+1), slice(u-w, u+w+1))
    a, b = Ix[s], Iy[s]
    return np.array([[(a*a).sum(), (a*b).sum()], [(a*b).sum(), (b*b).sum()]])

print(f'{"":26s}{"lambda_min":>12s} {"lambda_max":>12s} {"R de Harris":>14s}')
for nombre, (u, v) in [('zona plana ', (470, 100)), ('borde recto', (40, 120)),
                       ('esquina    ', (40, 60))]:
    M = matriz_estructura(u, v)
    lam = np.linalg.eigvalsh(M)
    R = np.linalg.det(M) - 0.04 * np.trace(M)**2      # criterio de Harris, sin calcular autovalores
    print(f'{nombre} en ({u:3d},{v:3d}): {lam[0]:12.3g} {lam[1]:12.3g} {R:14.3g}')
print('\\nPlana: los dos pequeños.  Borde: uno grande y otro pequeño -> R muy negativo.')
print('Esquina: los dos grandes -> R muy positivo. Ese signo es todo el detector.')"""))

C.append(code("""respuesta = cv2.cornerHarris(np.float32(Isuave), blockSize=5, ksize=3, k=0.04)
esquinas = np.argwhere(respuesta > 0.02 * respuesta.max())

# Version practica y ya filtrada por distancia minima
buenas = cv2.goodFeaturesToTrack(Isuave, maxCorners=40, qualityLevel=0.05, minDistance=18)
buenas = buenas.reshape(-1, 2)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.2))
a1.imshow(respuesta, cmap='inferno'); a1.set_title('respuesta de Harris', fontsize=9)
a2.imshow(I, cmap='gray')
a2.scatter(esquinas[:, 1], esquinas[:, 0], s=4, color=IQS_VERDE, alpha=0.5)
a2.scatter(buenas[:, 0], buenas[:, 1], s=70, facecolors='none', edgecolors=IQS_AZUL, lw=1.8)
a2.set_title(f'{len(buenas)} esquinas tras filtrar (goodFeaturesToTrack)', fontsize=9)
for ax in (a1, a2):
    ax.set_xticks([]); ax.set_yticks([])
plt.tight_layout(); plt.show()

print('Píxeles por encima del umbral de Harris:', len(esquinas),
      ' -> tras la supresión por distancia mínima:', len(buenas))"""))

C.append(md("""Fíjate en dónde **no** hay esquinas: en el círculo apenas salen, porque un borde curvo suave no tiene dos direcciones dominantes en una ventana pequeña. Y fíjate en el interior de las piezas: perfectamente plano, respuesta nula.

Estos puntos, cuando se les añade un descriptor invariante a escala y rotación —SIFT usa pirámides de imagen y diferencias de gaussianas (Corke, 2023, p. 523)—, son la materia prima de la correspondencia entre imágenes y, por tanto, de la odometría visual y del SLAM visual que cerrará el bloque en S31.

### Ejercicio 3

Rota la escena 30° con `cv2.warpAffine` y vuelve a detectar esquinas. ¿Se detectan los mismos puntos físicos? Repite escalando la imagen al 50 %. ¿Sobreviven? Ahí está, en dos líneas, la motivación de los detectores invariantes a escala."""))

C.append(code("""# Ejercicio 3: prueba aqui
# M = cv2.getRotationMatrix2D((W/2, H/2), 30, 1.0)
# Irot = cv2.warpAffine(I, M, (W, H))"""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.** Sin suavizar salen unos 2900 píxeles de borde, un 40 % más que con σ = 2, y el exceso son motas sueltas sobre el fondo ruidoso; con σ = 5 quedan menos de 400, se pierde el 80 % de los bordes y las esquinas se redondean. La regla que hay que extraer: **σ decide a qué escala se mira** (qué se considera borde y qué se considera textura), y los umbrales deciden **cuánta** evidencia se exige para llamarlo borde. Son mandos independientes y confundirlos es el error habitual: subir umbrales para quitar ruido cuando el problema era la escala.

**Ejercicio 2.** Otsu supone un histograma bimodal global; con un gradiente de iluminación fuerte, la zona oscura de la imagen cae entera por debajo del umbral y las piezas de ese lado desaparecen (o el fondo iluminado del otro lado se convierte en blob). `cv2.adaptiveThreshold` calcula un umbral por vecindario y sobrevive mucho mejor, pero fragmenta las piezas grandes. No hay ajuste que arregle esto en general: es el límite estructural del enfoque por umbral y el gancho de la S27.

**Ejercicio 3.** Con rotación, Harris es bastante estable: la matriz de estructura rota con la imagen y sus autovalores no cambian, así que los mismos vértices físicos se detectan. Con escala, no: una esquina detectada con `blockSize=5` a tamaño completo puede quedar por debajo de la ventana al reducir la imagen, y la respuesta cae. Harris es invariante a rotación pero **no** a escala; ese es exactamente el hueco que llenan SIFT y compañía con su espacio de escalas (Corke, 2023, p. 523)."""))

C.append(md("""---

## Para llevarse de esta sesión

Toda la primera mitad del procesado clásico es **una sola operación**, la convolución, con distintos núcleos: suavizar, derivar, detectar bordes. Cambiar de tarea es cambiar de núcleo, y quien diseña el núcleo es el ingeniero. Esa frase, dicha hoy, es la que la S27 va a poner en cuestión: la primera capa de una red convolucional aprende núcleos sospechosamente parecidos a los de la fig. 11.15 del libro, pero los aprende de los datos.

La cadena umbral → componentes conexas → momentos es transparente, métrica y barata, y sigue siendo la respuesta correcta cuando hay control de iluminación y tolerancias que cumplir. Su punto de rotura es igual de claro: la iluminación. Cuando la apariencia deja de poder describirse con un umbral, hace falta otra cosa.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S26_Procesado_Clasico.ipynb', C)
print('escrito S26')
