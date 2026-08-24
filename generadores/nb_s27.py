from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('matplotlib','matplotlib'), ('opencv-python','cv2'),
       ('scikit-learn','sklearn')]
C = []

C.append(cabecera(
    "S27", "Percepción con aprendizaje profundo: los conceptos, sin GPU", "6",
    "jueves 12 de noviembre de 2026", "1 h",
    "Enseña qué cambia realmente al pasar de rasgos diseñados a rasgos aprendidos, sin GPU y sin descargar ni un solo peso: aprende un núcleo convolucional por mínimos cuadrados y lo compara con el Sobel diseñado en S26, mide cómo el apilamiento de capas agranda el campo receptivo, y entrena un clasificador con scikit-learn sobre datos sintéticos para ver entrenamiento, capacidad y generalización. Lo que harían YOLO o SAM se explica, no se ejecuta.",
    "Corke (2023), cap. 12 — las técnicas clásicas «han sido eclipsadas» por el aprendizaje profundo (p. 510) — y cap. 11 — galería de núcleos que la primera capa reaprende (p. 444), criterio de Harris (p. 516). Papers citados por identificador arXiv: ResNet (arXiv:1512.03385), YOLO (arXiv:1506.02640), Faster R-CNN (arXiv:1506.01497), FCN (arXiv:1411.4038), U-Net (arXiv:1505.04597), Mask R-CNN (arXiv:1703.06870), ViT (arXiv:2010.11929), SAM (arXiv:2304.02643).",
    "los apuntes del bloque 6"))

C.append(instalacion(PKG, """import warnings
import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
warnings.filterwarnings('ignore')          # avisos de convergencia de sklearn
np.set_printoptions(precision=4, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.2)
plt.rcParams['axes.grid'] = False
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('Todo offline: ni un byte descargado, ni una GPU encendida.')"""))

# ---------------- 1. Filtro disenado vs aprendido
C.append(md("""## 1. Un núcleo diseñado y un núcleo aprendido

La frase que abre la sesión es de Corke, autor del manual de referencia de la visión geométrica clásica, en la edición de 2023: las técnicas clásicas de segmentación «han sido eclipsadas por las basadas en aprendizaje profundo» (Corke, 2023, p. 510). Conviene entender exactamente **qué** se sustituye, porque no es la convolución: la convolución sigue ahí. Lo que cambia es de dónde salen los coeficientes del núcleo.

En S26 elegimos a mano el núcleo de Sobel. Ahora vamos a hacer lo contrario: no diremos qué núcleo queremos, solo daremos **pares entrada-salida deseada**, y dejaremos que unos mínimos cuadrados encuentren los nueve coeficientes. Es, literalmente, lo que hace el descenso de gradiente en la primera capa de una red convolucional, solo que aquí el problema es lineal y se resuelve de una vez."""))

C.append(code("""rng = np.random.default_rng(27)
H, W = 220, 300

# --- escena sintetica: tres piezas claras y unas rayas finas igual de claras (distractores) ---
PIEZAS = np.zeros((H, W))
cv2.rectangle(PIEZAS, (30, 40), (120, 140), 1, -1)
cv2.circle(PIEZAS, (210, 90), 45, 1, -1)
cv2.drawContours(PIEZAS, [np.array([[60, 200], [160, 200], [110, 150]])], 0, 1, -1)

img = np.full((H, W), 80.0)
img[PIEZAS > 0] = 215
for y0 in (25, 175, 205):
    cv2.line(img, (0, y0), (W, y0), 215, 3)      # rayas: mismo brillo, NO son piezas
for x0 in (150, 260):
    cv2.line(img, (x0, 0), (x0, H), 215, 3)
I = np.clip(img + rng.normal(0, 5, img.shape), 0, 255).astype(np.uint8).astype(float) / 255.0

def vecindarios(I, k):
    \"\"\"Matriz (n_pixeles, k*k): cada fila es la ventana k x k centrada en un pixel.\"\"\"
    p = k // 2
    Ip = np.pad(I, p, mode='edge')
    return np.stack([Ip[i:i+I.shape[0], j:j+I.shape[1]].ravel()
                     for i in range(k) for j in range(k)], axis=1)

print('Escena', I.shape, ' fraccion de pixeles que son pieza:', round(float(PIEZAS.mean()), 3))"""))

C.append(code("""SOBEL = np.array([[-1., 0., 1.], [-2., 0., 2.], [-1., 0., 1.]]) / 8   # el nucleo DISENADO en S26

# El "maestro" produce la salida deseada; le anadimos ruido para que no sea un ejercicio de algebra exacta
objetivo = cv2.filter2D(I, -1, SOBEL, borderType=cv2.BORDER_REPLICATE)
objetivo += rng.normal(0, 0.004, objetivo.shape)

A = vecindarios(I, 3)                                   # 66 000 ejemplos, 9 incognitas
coef, *_ = np.linalg.lstsq(A, objetivo.ravel(), rcond=None)
nucleo_aprendido = coef.reshape(3, 3)

print('Núcleo APRENDIDO de los datos:\\n', nucleo_aprendido)
print('\\nNúcleo DISEÑADO (Sobel/8):\\n', SOBEL)
print('\\nMáxima diferencia entre coeficientes:', np.abs(nucleo_aprendido - SOBEL).max().round(5))"""))

C.append(md("""**Ese es todo el misterio.** Con suficientes ejemplos, el ajuste redescubre el operador de Sobel hasta la cuarta cifra: nadie le ha dicho que las derivadas se calculan así. La primera capa de una CNN entrenada sobre imágenes naturales aprende exactamente la galería de núcleos de la fig. 11.15 del libro —gaussianas orientadas, detectores de borde— (Corke, 2023, p. 444), y por la misma razón: son los filtros que mejor explican los datos.

La diferencia con S26 no es matemática, es **de origen**: el coste de la percepción migra del ingenio del ingeniero al conjunto de datos etiquetado."""))

# ---------------- 2. El objetivo define el nucleo
C.append(md("""## 2. El objetivo define el núcleo (y el tamaño del núcleo pone el techo)

Lo anterior era un poco tramposo: le pedíamos imitar un filtro que ya existía. Cambiemos la tarea a una **semántica**, de las que ningún núcleo clásico resuelve: «marca los píxeles que pertenecen a una pieza, y no los de las rayas finas», que tienen exactamente el mismo brillo.

Es un problema deliberadamente imposible para un umbral. Y la pregunta interesante es cuánto contexto espacial hace falta para resolverlo."""))

C.append(code("""def aprender_nucleo(I, objetivo, k):
    \"\"\"Ajusta por minimos cuadrados el mejor filtro lineal k x k mas sesgo para la tarea.\"\"\"
    A = np.column_stack([vecindarios(I, k), np.ones(I.size)])
    w, *_ = np.linalg.lstsq(A, objetivo.ravel(), rcond=None)
    nucleo, sesgo = w[:-1].reshape(k, k), w[-1]
    salida = cv2.filter2D(I, -1, nucleo, borderType=cv2.BORDER_REPLICATE) + sesgo
    acierto = float(((salida > 0.5) == (objetivo > 0.5)).mean())
    return nucleo, salida, acierto

tallas = [1, 3, 5, 9, 13]
resultados = {k: aprender_nucleo(I, PIEZAS, k) for k in tallas}
for k in tallas:
    print(f'núcleo {k:2d}×{k:2d}  ({k*k:3d} parámetros)  ->  acierto por píxel = '
          f'{resultados[k][2]*100:5.2f} %')"""))

C.append(code("""fig, axes = plt.subplots(2, 3, figsize=(12, 5.2))
axes[0, 0].imshow(I, cmap='gray'); axes[0, 0].set_title('entrada', fontsize=9)
axes[1, 0].imshow(PIEZAS, cmap='gray'); axes[1, 0].set_title('objetivo (piezas sí, rayas no)', fontsize=9)
for ax, k in zip(axes[0, 1:], [1, 13]):
    ax.imshow(resultados[k][1] > 0.5, cmap='gray')
    ax.set_title(f'salida del núcleo {k}×{k}', fontsize=9)
for ax, k in zip(axes[1, 1:], [1, 13]):
    ax.imshow(resultados[k][0], cmap='RdBu_r'); ax.set_title(f'núcleo {k}×{k} aprendido', fontsize=9)
for ax in axes.ravel():
    ax.set_xticks([]); ax.set_yticks([])
plt.tight_layout(); plt.show()"""))

C.append(md("""El núcleo 1×1 solo puede mirar el brillo del píxel y confunde rayas con piezas: se queda en el 90 % (que es justo el porcentaje de píxeles fáciles). El 13×13 aprende un patrón **centro-periferia** —positivo en el centro, negativo alrededor— que responde a manchas anchas y no a rayas finas, y llega al 98 %. Nadie ha diseñado ese filtro; lo ha dictado la tarea.

Y aparece de paso la variable que gobierna toda la arquitectura de una CNN: **cuánto contexto ve una unidad**. Es el campo receptivo, y es el tema de la sección siguiente.

### Ejercicio 1

Cambia el objetivo a «marca solo el círculo» (usa una máscara únicamente con el círculo) y vuelve a ajustar núcleos de varios tamaños. ¿Se puede resolver con un filtro lineal? ¿Qué tamaño de núcleo haría falta para distinguir el círculo del rectángulo, que mide 90×100 px?"""))

C.append(code("""# Ejercicio 1: prueba aqui
# SOLO_CIRCULO = np.zeros((H, W)); cv2.circle(SOLO_CIRCULO, (210, 90), 45, 1, -1)
# for k in [1, 5, 13]:
#     print(k, aprender_nucleo(I, SOLO_CIRCULO, k)[2])"""))

# ---------------- 3. Campo receptivo
C.append(md("""## 3. Apilar capas: el campo receptivo

Una CNN no usa un núcleo de 13×13; usa muchas capas de 3×3. La razón es aritmética pura y merece hacerse en clase con números.

Al encadenar dos convoluciones de 3×3, cada píxel de salida depende de una ventana de 5×5 de la entrada: **la composición de dos filtros pequeños equivale a uno grande**. Con L capas de k×k sin submuestreo, el campo receptivo es 1 + L·(k−1). Vamos a comprobarlo empíricamente propagando una delta."""))

C.append(code("""def campo_receptivo_empirico(k, capas, N=121):
    \"\"\"Propaga una delta por 'capas' convoluciones k x k y mide el soporte resultante.\"\"\"
    d = np.zeros((N, N)); d[N//2, N//2] = 1.0
    nucleo = np.ones((k, k)) / (k*k)
    anchos = []
    for _ in range(capas):
        d = cv2.filter2D(d, -1, nucleo, borderType=cv2.BORDER_CONSTANT)
        fil = np.nonzero(d.sum(axis=1) > 1e-12)[0]
        anchos.append(int(fil.max() - fil.min() + 1))
    return anchos

emp = campo_receptivo_empirico(3, 12)
print(' capa  campo medido  1 + L·(k-1)   parámetros acumulados (3×3)')
for L, a in enumerate(emp, 1):
    print(f' {L:4d} {a:12d} {1 + L*2:12d} {9*L:20d}')

# La composicion explicita: 3x3 (*) 3x3 = 5x5
k3 = np.array([[1., 2., 1.], [2., 4., 2.], [1., 2., 1.]]) / 16
comp = cv2.filter2D(np.pad(k3, 2), -1, k3, borderType=cv2.BORDER_CONSTANT)
print('\\nDos gaussianas 3×3 encadenadas dan este 5×5 (soporte 5, no 3):')
print((comp[1:6, 1:6] * 256).round(1))"""))

C.append(code("""L = np.arange(1, 13)
sin_pool = 1 + L * 2                                  # k = 3, stride 1
con_pool = np.zeros_like(L)                           # k = 3 y submuestreo /2 cada dos capas
r, salto = 1, 1
for i, _ in enumerate(L):
    r = r + 2 * salto
    con_pool[i] = r
    if (i + 1) % 2 == 0:
        salto *= 2

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.6))
a1.plot(L, sin_pool, 'o-', color=IQS_AZUL, label='3×3, sin submuestreo: 1 + 2L')
a1.plot(L, con_pool, 's-', color=IQS_VERDE, label='3×3 + submuestreo /2 cada 2 capas')
a1.set_xlabel('capas apiladas'); a1.set_ylabel('campo receptivo [px]')
a1.legend(fontsize=8); a1.grid(True); a1.set_title('Cómo crece lo que ve una unidad')

a2.plot(L, 9*L, 'o-', color=IQS_AZUL, label='L capas de 3×3: 9L parámetros')
a2.plot(L, sin_pool**2, 's--', color='crimson', label='un solo núcleo del mismo campo: (1+2L)²')
a2.set_yscale('log'); a2.set_xlabel('capas apiladas'); a2.set_ylabel('parámetros')
a2.legend(fontsize=8); a2.grid(True); a2.set_title('Por qué se apila en vez de agrandar')
plt.tight_layout(); plt.show()

print(f'Con 12 capas de 3×3: campo receptivo {sin_pool[-1]} px con {9*12} parámetros;')
print(f'un único núcleo de {sin_pool[-1]}×{sin_pool[-1]} necesitaría {sin_pool[-1]**2}.')"""))

C.append(md("""**Las dos razones por las que se apila** están en esas dos gráficas: apilar da campo receptivo grande con pocos parámetros, y además intercala no linealidades entre capa y capa, de modo que la composición ya no es un filtro lineal equivalente sino una función mucho más expresiva. Añadir submuestreo hace crecer el campo exponencialmente, que es como una red de 50 capas acaba viendo la imagen entera.

Ese apilamiento profundo tuvo un problema práctico durante años —las redes muy profundas no entrenaban— hasta que las conexiones residuales de ResNet lo resolvieron (He et al., 2015, arXiv:1512.03385); y años después los transformers de visión demostraron que con datos suficientes ni siquiera la convolución es imprescindible (Dosovitskiy et al., 2020, arXiv:2010.11929)."""))

# ---------------- 4. Entrenamiento y generalizacion
C.append(md("""## 4. Entrenar y generalizar: lo que de verdad cambia

Hasta aquí hemos ajustado filtros lineales. El segundo ingrediente del aprendizaje profundo es la **no linealidad**, y con ella aparecen los dos conceptos que un ingeniero debe manejar antes de integrar cualquier red en un robot: capacidad y generalización.

Lo montamos con `scikit-learn` sobre datos sintéticos en dos dimensiones —dos medias lunas solapadas— porque así se puede *ver* la frontera de decisión. Todo lo que se observe aquí vale, sin cambios conceptuales, para una red de cien capas sobre imágenes."""))

C.append(code("""X, y = make_moons(n_samples=500, noise=0.30, random_state=27)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, train_size=80, random_state=27, stratify=y)
print('Entrenamiento:', X_tr.shape[0], 'muestras   |   Test:', X_te.shape[0], 'muestras')

modelos = {
    'logística (lineal)': LogisticRegression(),
    'MLP (30 neuronas)': MLPClassifier((30,), max_iter=8000, random_state=27, alpha=1e-7),
    'MLP (100, 100)':    MLPClassifier((100, 100), max_iter=8000, random_state=27, alpha=1e-7),
}
for nombre, m in modelos.items():
    m.fit(X_tr, y_tr)
    print(f'{nombre:20s}  entrenamiento = {m.score(X_tr, y_tr)*100:5.1f} %'
          f'   test = {m.score(X_te, y_te)*100:5.1f} %')"""))

C.append(code("""uu, vv = np.meshgrid(np.linspace(X[:,0].min()-.5, X[:,0].max()+.5, 300),
                     np.linspace(X[:,1].min()-.5, X[:,1].max()+.5, 300))
rejilla = np.column_stack([uu.ravel(), vv.ravel()])

fig, axes = plt.subplots(1, 3, figsize=(13, 3.8))
for ax, (nombre, m) in zip(axes, modelos.items()):
    ax.contourf(uu, vv, m.predict(rejilla).reshape(uu.shape), levels=1,
                colors=[IQS_AZUL, IQS_VERDE], alpha=0.18)
    ax.scatter(X_te[:,0], X_te[:,1], c=y_te, cmap='coolwarm', s=8, alpha=0.35)
    ax.scatter(X_tr[:,0], X_tr[:,1], c=y_tr, cmap='coolwarm', s=42, edgecolors='k', lw=0.7)
    ax.set_title(f'{nombre}\\ntest = {m.score(X_te, y_te)*100:.1f} %', fontsize=9)
    ax.set_xticks([]); ax.set_yticks([])
fig.suptitle('Puntos grandes: entrenamiento. Puntos pálidos: test que el modelo nunca vio.',
             fontsize=9)
plt.tight_layout(); plt.show()"""))

C.append(md("""Léelas de izquierda a derecha. La frontera lineal es una recta y no puede seguir el arco de las lunas, así que se queda unos puntos por debajo. La MLP de 30 neuronas curva la frontera y gana varios puntos en test sin memorizar. La MLP grande acierta el **100 %** en entrenamiento —dibuja islas alrededor de puntos sueltos— pero en datos nuevos no llega al 90 %. Ese último comportamiento tiene nombre y hay que saber medirlo."""))

C.append(code("""capacidades = [(2,), (5,), (10,), (30,), (100, 100), (300, 300)]
acc_tr, acc_te, npar = [], [], []
for h in capacidades:
    m = MLPClassifier(h, max_iter=8000, random_state=27, alpha=1e-7).fit(X_tr, y_tr)
    acc_tr.append(m.score(X_tr, y_tr)); acc_te.append(m.score(X_te, y_te))
    npar.append(sum(c.size for c in m.coefs_) + sum(b.size for b in m.intercepts_))
    print(f'capas ocultas {str(h):12s} {npar[-1]:7d} parámetros   '
          f'entren. {acc_tr[-1]*100:5.1f} %   test {acc_te[-1]*100:5.1f} %')

fig, ax = plt.subplots(figsize=(7.5, 3.6))
xs = np.arange(len(capacidades))
ax.plot(xs, np.array(acc_tr)*100, 'o-', color=IQS_AZUL, label='acierto en entrenamiento')
ax.plot(xs, np.array(acc_te)*100, 's-', color=IQS_VERDE, label='acierto en test')
ax.fill_between(xs, np.array(acc_te)*100, np.array(acc_tr)*100, color='crimson', alpha=0.12)
ax.set_xticks(xs); ax.set_xticklabels([f'{h}\\n{p} par.' for h, p in zip(capacidades, npar)],
                                      fontsize=7)
ax.set_ylabel('acierto [%]'); ax.grid(True); ax.legend(fontsize=8)
ax.set_title('Capacidad frente a generalización (zona roja = brecha)')
plt.tight_layout(); plt.show()

print('Brecha de generalización con el modelo mayor:',
      f'{(acc_tr[-1]-acc_te[-1])*100:.1f} puntos porcentuales')
print('Con ruido 0.30 en los datos, ningún modelo puede pasar de ~90 % en test:')
print('esa parte del error es irreducible y no la arregla ninguna arquitectura.')"""))

C.append(md("""**El mensaje de ingeniería.** El acierto en entrenamiento **no** mide nada: solo dice cuánto ha memorizado el modelo. La única cifra que importa es la de datos que nunca vio, y la brecha entre ambas es lo que se vigila. Cuando un proveedor presenta un detector con «99 % de precisión», la primera pregunta es sobre qué conjunto.

### Ejercicio 2

Sube `train_size` de 80 a 400 muestras y repite el barrido de capacidades. ¿Qué le pasa a la brecha? Formula la regla práctica que se deduce: ¿qué se hace antes, agrandar el modelo o conseguir más datos?

### Ejercicio 3

Añade regularización subiendo `alpha` de `1e-7` a `1.0` en la MLP de (300, 300) y vuelve a medir entrenamiento y test. ¿Se cierra la brecha? ¿A costa de qué?"""))

C.append(code("""# Ejercicios 2 y 3: prueba aqui
# X_tr2, X_te2, y_tr2, y_te2 = train_test_split(X, y, train_size=400, random_state=27, stratify=y)
# m = MLPClassifier((300, 300), max_iter=8000, random_state=27, alpha=1.0).fit(X_tr, y_tr)"""))

# ---------------- 5. YOLO y SAM sin ejecutarlos
C.append(md("""## 5. Qué harían aquí YOLO y SAM (explicado, no ejecutado)

Este cuaderno no descarga pesos ni enciende una GPU, así que la parte final es conceptual. Pero con lo que acabamos de construir, describir estos sistemas ya no es magia: son las mismas piezas a otra escala.

**Detección de objetos: YOLO.** La tarea produce, para cada objeto, una caja englobante, una clase y una confianza; se evalúa con IoU y mAP. Hay dos linajes: los detectores de dos etapas, que generan propuestas de región y las clasifican después —Faster R-CNN integró la propuesta en la propia red (Ren et al., 2015, arXiv:1506.01497)—, y los de una sola etapa. YOLO es el emblema de los segundos: «enmarcamos la detección de objetos como un problema de regresión hacia cajas englobantes separadas espacialmente y probabilidades de clase asociadas», de modo que «una única red neuronal predice cajas y probabilidades de clase directamente de la imagen completa en una sola evaluación» (Redmon et al., 2016, arXiv:1506.02640). Sobre nuestra escena de la sección 2, YOLO devolvería tres cajas etiquetadas «pieza» y ninguna sobre las rayas — es decir, la salida de nuestro núcleo 13×13, pero con la caja ya agrupada y sin que nadie haya tenido que definir «pieza». Esa única pasada por la red es lo que lo hizo dominante en robótica: cabe en el presupuesto de latencia de un robot móvil con GPU embarcada.

**Segmentación: de FCN a SAM.** Las redes totalmente convolucionales demostraron que un clasificador puede convertirse en etiquetador denso píxel a píxel (Long et al., 2014, arXiv:1411.4038); U-Net fijó la arquitectura codificador-decodificador con conexiones de salto (Ronneberger et al., 2015, arXiv:1505.04597); y Mask R-CNN añadió la máscara por instancia a la detección (He et al., 2017, arXiv:1703.06870), que es la salida natural para manipulación porque «qué píxeles son esta pieza concreta» es exactamente lo que necesita un agarre. El salto reciente son los modelos fundacionales: SAM se entrena a escala masiva para segmentar a partir de indicaciones —un punto, una caja— y transfiere a dominios nuevos sin reentrenar (Kirillov et al., 2023, arXiv:2304.02643). Sobre nuestra escena, bastaría hacer clic dentro del triángulo para obtener su máscara exacta, sin haber definido nunca qué es un triángulo.

**Y la frontera que no se mueve.** El detector más moderno entrega píxeles. Convertir píxeles en metros sigue pasando por la matriz K, la calibración y la pose de S25. Por eso los sistemas reales de percepción robótica son casi siempre híbridos: red para la apariencia, geometría calibrada para la medida. En una célula colaborativa, además, la función de seguridad no se delega en la red: se resuelve con sensórica certificada, y la red queda como capa adicional que no es de seguridad."""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.** Con la máscara del círculo, ningún filtro lineal pequeño lo resuelve bien: el rectángulo y el círculo tienen el mismo brillo y ambos son «manchas anchas», así que un núcleo centro-periferia responde igual a los dos. Para distinguirlos por tamaño el núcleo tendría que abarcar la pieza mayor, unos 13×13 como mínimo y realmente más cerca de 90×100 px, con lo que el número de parámetros se dispara a decenas de miles. Ese es exactamente el argumento de la sección 3: la respuesta no es agrandar el núcleo, es apilar capas — y añadir no linealidades, porque la forma «redondo frente a rectangular» no es una función lineal de los píxeles.

**Ejercicio 2.** Con 400 muestras de entrenamiento la brecha se reduce drásticamente y los modelos grandes dejan de perder frente a los medianos. La regla práctica: cuando entrenamiento y test están muy separados, el problema son los datos, no la arquitectura; cuando ambos son bajos y parecidos, el problema es la capacidad. Diagnosticar cuál de los dos casos se tiene, antes de tocar nada, ahorra semanas.

**Ejercicio 3.** Con `alpha = 1.0` la penalización sobre los pesos aplana la frontera: el acierto en entrenamiento baja bastante y el de test se mantiene o mejora ligeramente, de modo que la brecha se cierra. El coste es sesgo: si el problema real necesitara una frontera muy sinuosa, la regularización impediría representarla. Regularizar es cambiar varianza por sesgo, y el punto óptimo depende de cuántos datos haya."""))

C.append(md("""---

## Para llevarse de esta sesión

La convolución no ha desaparecido: lo que ha cambiado es que los coeficientes ya no los escribe el ingeniero, los dicta la tarea a través de los datos. Lo hemos comprobado en las dos direcciones: unos mínimos cuadrados redescubren Sobel cuando el objetivo es derivar, y encuentran un detector centro-periferia que nadie habría escrito cuando el objetivo es «esto es una pieza y esto no».

Apilar capas pequeñas es una decisión de ingeniería, no estética: da campo receptivo grande con pocos parámetros y añade no linealidad entre medias. Y la métrica que cuenta nunca es el error de entrenamiento, sino el de datos nunca vistos; la brecha entre ambos es la que decide si un modelo se puede embarcar.

Lo que **no** cambia con el aprendizaje profundo es la geometría: la matriz K de S25 sigue siendo necesaria para pasar de píxeles a metros. Con esto cerramos la mitad de visión del bloque; a partir de S28 el problema deja de ser la imagen y pasa a ser la incertidumbre.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S27_Percepcion_Aprendida.ipynb', C)
print('escrito S27')
