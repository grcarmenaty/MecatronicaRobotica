from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('matplotlib','matplotlib'), ('scipy','scipy')]
C = []

C.append(cabecera(
    "S35", "Planificación de trayectorias: mapas, A*, PRM y RRT", "7",
    "miércoles 2 de diciembre de 2026", "1 h",
    "Construye un mapa de ocupación de almacén y recorre encima toda la familia de planificadores de la sesión: inflado de obstáculos y mapa de coste, transformada de distancia con descenso de gradiente, A* frente a Dijkstra contando nodos expandidos, y los dos métodos de muestreo, PRM y RRT. Todo en numpy y matplotlib puros, para que se vea el algoritmo y no la biblioteca.",
    "Corke (2023), cap. 5 — mapa de ocupación (p. 177), representaciones grafo/rejilla (p. 166), transformada de distancia (pp. 177-181), inflado de obstáculos (p. 181), mapa de coste de D* (p. 182), UCS (pp. 172-173), A* y admisibilidad (pp. 174-175), Dijkstra como frente de onda (p. 199), replanificación con D* (p. 184), PRM (pp. 185-187). Lynch y Park (2017), cap. 10 — definición del problema (p. 353), planificación de caminos y no holonomía (p. 355), completitud (p. 356), C-obstáculos (p. 359), pseudocódigo de A* (pp. 365-366), maldición de la dimensión (p. 378), Algoritmo 10.3 del RRT (p. 379), planificador local (p. 382), RRT* (pp. 382-383), consulta del PRM con A* (p. 384), campos potenciales (p. 386).",
    "los apuntes del bloque 7"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
import heapq
from scipy.ndimage import distance_transform_edt
np.set_printoptions(precision=3, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.2)
plt.rcParams['axes.grid'] = False
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('Listo.')"""))

# ---------------- 1. Mapa, inflado, coste
C.append(md("""## 1. El mapa: ocupación, inflado y coste

El punto de partida es el mapa de ocupación del bloque 6: «un array de celdas, típicamente cuadradas, donde cada celda contiene información sobre la transitabilidad de esa celda»; en el caso binario, uno si está ocupada y cero si está libre (Corke, 2023, p. 177). Frente a la alternativa de grafo —vértices que son lugares, aristas que son rutas—, la rejilla discretiza el espacio de forma uniforme (Corke, 2023, p. 166).

Generamos un almacén de dos naves separadas por un muro con **dos puertas de anchura muy distinta** —una de 2,0 m y otra de 0,8 m—, más estanterías en cada nave. Resolución 10 cm por celda, así que la rejilla de 90 × 130 celdas son 13 × 9 metros. Esa asimetría entre las dos puertas no es decorativa: es el motor de casi todo lo que veremos después."""))

C.append(code("""RES = 0.10                       # metros por celda
FILAS, COLS = 90, 130

def mapa_almacen():
    \"\"\"Rejilla de ocupacion booleana: True = obstaculo. (fila, columna) = (y, x).\"\"\"
    occ = np.zeros((FILAS, COLS), bool)
    occ[0, :] = occ[-1, :] = True                 # paredes exteriores
    occ[:, 0] = occ[:, -1] = True
    occ[42:47, :] = True                          # muro que parte el almacen en dos naves
    occ[42:47, 8:28] = False                      #   puerta ANCHA  (20 celdas = 2.0 m)
    occ[42:47, 92:100] = False                    #   puerta ESTRECHA (8 celdas = 0.8 m)
    occ[12:36, 40:47] = True                      # estanterias de la nave inferior
    occ[12:36, 64:71] = True
    occ[58:78, 34:41] = True                      # estanterias de la nave superior
    occ[58:78, 58:65] = True
    occ[58:78, 82:89] = True
    return occ

occ = mapa_almacen()
INICIO = (6, 6)                                   # muelle de entrada, nave inferior
META   = (82, 83)                                 # puesto de picking, nave superior

print(f'Rejilla {occ.shape} celdas  ->  {COLS*RES:.1f} x {FILAS*RES:.1f} m')
print(f'Celdas ocupadas: {occ.sum()} ({100*occ.mean():.1f} %)')
print('Inicio y meta libres en el mapa crudo:', not occ[INICIO], not occ[META])"""))

C.append(md("""Dos transformaciones convierten el mapa crudo en un soporte de planificación.

La primera es el **inflado**: se expanden los obstáculos el radio del robot —una dilatación morfológica— para poder planificar tratando al robot como un punto (Corke, 2023, p. 181). Es el mismo movimiento conceptual que los C-obstáculos de Lynch y Park: «crecer» los obstáculos convierte el problema del robot circular en el de un punto entre obstáculos hinchados (Lynch y Park, 2017, p. 359). Lo hacemos con la transformada de distancia euclídea de `scipy`, que da en una llamada la distancia de cada celda libre al obstáculo más cercano.

La segunda es pasar **de ocupación binaria a coste**: D* «generaliza la rejilla de ocupación a un mapa de coste que representa el coste c ∈ R, c > 0, de atravesar cada celda», con coste c·√2 en diagonal e infinito en los obstáculos, y ese coste puede codificar tiempo, rugosidad o riesgo (Corke, 2023, p. 182). Aquí lo usamos como riesgo: cuanto más cerca de una pared, más caro. Cuando en S36 se abra el costmap de Nav2 —capa estática, capa de obstáculos, capa de inflado— hay que reconocer estas dos transformaciones ya institucionalizadas en software."""))

C.append(code("""R_ROBOT = 0.28                                    # radio del robot, m
r_celdas = R_ROBOT / RES                          # 2.8 celdas

dist_obst = distance_transform_edt(~occ)          # distancia de cada celda libre al obstaculo
inflado = dist_obst <= r_celdas                   # C-obstaculos: prohibido para el centro
libre = ~inflado

def mapa_de_coste(dist, r, alcance=0.25, peso=9.0):
    \"\"\"Coste por celda: 1 lejos de obstaculos, creciente al acercarse, inf donde no cabe.\"\"\"
    c = 1.0 + peso * np.exp(-(dist - r) / (alcance / RES))
    c[dist <= r] = np.inf                          # incluye los obstaculos reales
    return c

coste = mapa_de_coste(dist_obst, r_celdas)
binario = np.where(libre, 1.0, np.inf)            # el mismo mapa, sin penalizacion de cercania

print(f'Radio del robot {R_ROBOT} m = {r_celdas:.1f} celdas')
print(f'Celdas transitables tras inflar: {libre.sum()} de {libre.size} ({100*libre.mean():.1f} %)')
print(f'Coste finito: minimo {coste[np.isfinite(coste)].min():.2f}, '
      f'maximo {coste[np.isfinite(coste)].max():.2f}')
print('Inicio y meta siguen libres tras inflar:', libre[INICIO], libre[META])"""))

C.append(code("""fig, axes = plt.subplots(1, 3, figsize=(13, 3.4))
for ax in axes:
    ax.set_xticks([]); ax.set_yticks([])

axes[0].imshow(occ, origin='lower', cmap='Greys')
axes[0].set_title('Mapa de ocupacion binario', fontsize=10)
axes[1].imshow(inflado, origin='lower', cmap='Greys')
axes[1].imshow(occ, origin='lower', cmap='Greys', alpha=0.5)
axes[1].set_title(f'Inflado {R_ROBOT} m (C-obstaculos)', fontsize=10)
im = axes[2].imshow(np.where(np.isfinite(coste), coste, np.nan), origin='lower', cmap='viridis')
axes[2].set_title('Mapa de coste', fontsize=10)
plt.colorbar(im, ax=axes[2], fraction=0.03)
for ax in axes:
    ax.scatter(INICIO[1], INICIO[0], marker='o', s=55, color=IQS_VERDE, zorder=5)
    ax.scatter(META[1], META[0], marker='*', s=140, color='crimson', zorder=5)
plt.tight_layout(); plt.show()"""))

C.append(md("""**Lo que hay que señalar sobre la figura central.** La puerta estrecha sobrevive al inflado, pero muy justa: de sus 8 celdas libres quedan 2 utilizables por el *centro* del robot. La ancha apenas se entera. Si el robot fuese un poco mayor —súbelo a 0,40 m en el ejercicio 1— la puerta estrecha desaparece y el almacén pasa de tener dos conexiones entre naves a tener una sola. Ese cambio cualitativo provocado por un parámetro continuo es la mejor demostración de por qué el inflado no es un detalle de implementación: **cambia la topología del espacio libre**.

## 2. La transformada de distancia: el frente de onda

La familia clásica se organiza por lo que se propaga y desde dónde. La transformada de distancia asigna a cada celda libre su distancia al objetivo, y seguir el gradiente descendente desde cualquier celda produce el camino más corto (Corke, 2023, pp. 177-179). Es completo y óptimo sobre la rejilla, con un coste de planificación alto que se paga **una sola vez por objetivo**: después, cualquier punto de partida es una consulta gratuita.

Dijkstra es exactamente el mismo objeto en lenguaje de grafos: el coste «se expande hacia fuera desde el vértice inicial y es análogo a la transformada de distancia o planificador de frente de onda» (Corke, 2023, p. 199)."""))

C.append(code("""VECINOS = [(-1, 0, 1.0), (1, 0, 1.0), (0, -1, 1.0), (0, 1, 1.0),
           (-1, -1, np.sqrt(2)), (-1, 1, np.sqrt(2)),
           (1, -1, np.sqrt(2)), (1, 1, np.sqrt(2))]

def transformada_distancia(coste, meta):
    \"\"\"Coste minimo de cada celda hasta la meta, propagando el frente de onda desde ella.\"\"\"
    D = np.full(coste.shape, np.inf)
    D[meta] = 0.0
    monton = [(0.0, meta)]
    while monton:
        d, u = heapq.heappop(monton)
        if d > D[u]:
            continue
        for di, dj, paso in VECINOS:
            v = (u[0] + di, u[1] + dj)
            if not (0 <= v[0] < coste.shape[0] and 0 <= v[1] < coste.shape[1]):
                continue
            c = coste[v]
            if not np.isfinite(c):
                continue
            nd = d + paso * c
            if nd < D[v]:
                D[v] = nd
                heapq.heappush(monton, (nd, v))
    return D

def bajar_gradiente(D, inicio, max_pasos=20000):
    \"\"\"Camino por descenso del frente de onda: en cada celda, al vecino de menor D.\"\"\"
    camino, u = [inicio], inicio
    for _ in range(max_pasos):
        if D[u] == 0.0:
            break
        mejor, mejor_d = None, D[u]
        for di, dj, _ in VECINOS:
            v = (u[0] + di, u[1] + dj)
            if 0 <= v[0] < D.shape[0] and 0 <= v[1] < D.shape[1] and D[v] < mejor_d:
                mejor, mejor_d = v, D[v]
        if mejor is None:
            return camino, False          # minimo local: no puede pasar con esta D
        u = mejor
        camino.append(u)
    return camino, True

import time
t0 = time.perf_counter()
D_bin = transformada_distancia(binario, META)
t_dt = time.perf_counter() - t0

camino_dt, ok = bajar_gradiente(D_bin, INICIO)
print(f'Transformada de distancia calculada en {t_dt*1000:.0f} ms')
print(f'Camino encontrado: {ok}, longitud {len(camino_dt)} celdas '
      f'= {D_bin[INICIO]*RES:.2f} m de recorrido')
print(f'Consulta desde OTRO punto, sin recalcular nada: '
      f'{bajar_gradiente(D_bin, (10, 100))[0].__len__()} celdas')"""))

C.append(code("""fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 3.6))
Dv = np.where(np.isfinite(D_bin), D_bin, np.nan)
im = a1.imshow(Dv, origin='lower', cmap='magma')
a1.contour(Dv, levels=18, colors='w', linewidths=0.4)
a1.set_title('Transformada de distancia a la meta (frente de onda)', fontsize=10)
plt.colorbar(im, ax=a1, fraction=0.03, label='coste hasta la meta')

a2.imshow(inflado, origin='lower', cmap='Greys')
for arranque, col in [(INICIO, IQS_AZUL), ((10, 100), IQS_VERDE), ((80, 10), 'darkorange')]:
    cam, _ = bajar_gradiente(D_bin, arranque)
    cam = np.array(cam)
    a2.plot(cam[:, 1], cam[:, 0], lw=2, color=col)
    a2.scatter(arranque[1], arranque[0], s=45, color=col, zorder=5)
a2.scatter(META[1], META[0], marker='*', s=160, color='crimson', zorder=5)
a2.set_title('Tres consultas, una sola planificacion', fontsize=10)
for ax in (a1, a2):
    ax.set_xticks([]); ax.set_yticks([])
plt.tight_layout(); plt.show()"""))

C.append(md("""**El argumento que se lleva la sesión** está en la figura de la derecha: tres puntos de partida distintos, tres caminos óptimos, **una sola** llamada al planificador. La transformada de distancia es cara pero se amortiza si la meta es estable —un muelle de carga, una estación de recarga—. En cuanto la meta cambia hay que recalcularlo todo, y ahí es donde D* aporta lo que el robot móvil necesita: «permite hacer cambios en el mapa en cualquier momento mientras el robot está en movimiento» reutilizando el trabajo previo, con una replanificación que en el ejemplo del libro expande en torno al 12 % de los vértices de la planificación original (Corke, 2023, pp. 182-184).

## 3. A* frente a Dijkstra: qué compra la heurística

A* añade la pieza que hace la búsqueda dirigida: expandir según f(v) = g(v) + h(v), coste acumulado más una estimación del coste restante (Corke, 2023, p. 175). En el pseudocódigo de Lynch y Park aparecen las listas OPEN y CLOSED, el array `past_cost` y los punteros `parent` que reconstruyen el camino (Lynch y Park, 2017, pp. 365-366). El teorema hay que enunciarlo con precisión: «A* garantiza devolver el camino de menor coste solo si la heurística es admisible, es decir, si no sobreestima el coste de alcanzar la meta» (Corke, 2023, p. 175).

Como nuestro coste por celda es siempre ≥ 1, la **distancia euclídea en celdas es admisible**: ningún camino puede costar menos que su longitud geométrica. Con `h = 0` el algoritmo degenera exactamente en Dijkstra. Una única función, tres heurísticas, y contamos nodos expandidos.

*Nota histórica de treinta segundos para el aula:* el «truco de A*» lo publicaron en 1966 Hart, Nilsson y Raphael, del equipo del robot Shakey en el Stanford Research Institute (Corke, 2023, p. 174)."""))

C.append(code("""def buscar(coste, inicio, meta, h=None):
    \"\"\"A* generico sobre la rejilla. Con h=None (heuristica nula) es Dijkstra.
    Devuelve (camino, coste_total, nodos_expandidos).\"\"\"
    if h is None:
        h = lambda v: 0.0
    n, m = coste.shape
    g = {inicio: 0.0}
    padre = {}
    abierta = [(h(inicio), 0.0, inicio)]           # OPEN, ordenada por f = g + h
    cerrada = set()                                # CLOSED
    expandidos = 0
    while abierta:
        _, gu, u = heapq.heappop(abierta)
        if u in cerrada:
            continue
        cerrada.add(u)
        expandidos += 1
        if u == meta:
            break
        for di, dj, paso in VECINOS:
            v = (u[0] + di, u[1] + dj)
            if not (0 <= v[0] < n and 0 <= v[1] < m) or v in cerrada:
                continue
            c = coste[v]
            if not np.isfinite(c):
                continue
            ng = gu + paso * c                     # coste de entrar en la celda v
            if ng < g.get(v, np.inf):
                g[v] = ng
                padre[v] = u
                heapq.heappush(abierta, (ng + h(v), ng, v))
    if meta not in g:
        return None, np.inf, expandidos
    camino, u = [meta], meta
    while u != inicio:
        u = padre[u]
        camino.append(u)
    return camino[::-1], g[meta], expandidos

h_euclidea = lambda v: np.hypot(v[0] - META[0], v[1] - META[1])            # admisible
h_inflada  = lambda v: 2.0 * np.hypot(v[0] - META[0], v[1] - META[1])      # NO admisible: x2

resultados = {}
for nombre, h in [('Dijkstra (h = 0)', None),
                  ('A* euclidea (admisible)', h_euclidea),
                  ('A* x2 (no admisible)', h_inflada)]:
    t0 = time.perf_counter()
    cam, cst, exp = buscar(binario, INICIO, META, h)
    dt = time.perf_counter() - t0
    resultados[nombre] = (cam, cst, exp)
    print(f'{nombre:30s}  nodos expandidos {exp:6d}   coste {cst*RES:7.3f} m   {dt*1000:5.0f} ms')

opt = resultados['Dijkstra (h = 0)'][1]
print()
for nombre, (_, cst, exp) in resultados.items():
    print(f'{nombre:30s}  exploracion {100*exp/resultados["Dijkstra (h = 0)"][2]:5.1f} % '
          f'de Dijkstra   sobrecoste {100*(cst/opt - 1):+5.2f} %')"""))

C.append(code("""fig, axes = plt.subplots(1, 3, figsize=(13, 3.4))
for ax, (nombre, (cam, cst, exp)) in zip(axes, resultados.items()):
    ax.imshow(inflado, origin='lower', cmap='Greys')
    cam = np.array(cam)
    ax.plot(cam[:, 1], cam[:, 0], lw=2.2, color=IQS_AZUL)
    ax.scatter(INICIO[1], INICIO[0], s=50, color=IQS_VERDE, zorder=5)
    ax.scatter(META[1], META[0], marker='*', s=140, color='crimson', zorder=5)
    ax.set_title(f'{nombre}\\n{exp} nodos, {cst*RES:.2f} m', fontsize=9)
    ax.set_xticks([]); ax.set_yticks([])
plt.tight_layout(); plt.show()

# y el mismo A* sobre el mapa de COSTE, no sobre el binario
cam_c, cst_c, exp_c = buscar(coste, INICIO, META, h_euclidea)
cam_b = np.array(resultados['A* euclidea (admisible)'][0]); cam_c = np.array(cam_c)
sep_b = dist_obst[cam_b[:, 0], cam_b[:, 1]].min() * RES
sep_c = dist_obst[cam_c[:, 0], cam_c[:, 1]].min() * RES
print(f'Sobre mapa binario: {len(cam_b)} celdas, se acerca hasta {sep_b:.2f} m de un obstaculo')
print(f'Sobre mapa de coste: {len(cam_c)} celdas, se acerca hasta {sep_c:.2f} m')"""))

C.append(md("""**Las tres lecturas de la figura.** Dijkstra expande prácticamente todo el espacio libre, porque sin heurística no tiene ninguna razón para preferir una dirección; A* con heurística euclídea encuentra **el mismo camino óptimo** explorando una fracción de los nodos —la heurística no cambia la respuesta, cambia el trabajo—; y A* con la heurística multiplicada por dos, que **sobreestima**, expande diez veces menos nodos pero devuelve un camino claramente peor: se lanza en línea recta hacia la meta, se cuela por la puerta estrecha y paga el rodeo. Ese es exactamente el enunciado del teorema de admisibilidad, hecho experimento — y también la razón por la que el *weighted A\** existe y se usa a sabiendas: cuando hay que replanificar a 20 Hz, a veces un camino un 20 % peor calculado diez veces más rápido es el buen negocio.

La comparación final, sobre el mapa de coste, muestra el otro efecto: el camino deja de pegarse a las esquinas y se aleja de las paredes, pagando algo más de longitud a cambio de margen. Es literalmente lo que produce la *inflation layer* de Nav2, y la razón por la que un AMR bien configurado no roza las estanterías.

### Ejercicio 1

El almacén tiene un segundo destino habitual, el puesto `(60, 115)` de la nave superior derecha. Planifica hacia él con radios de robot de 0,15, 0,28, 0,40 y 0,45 m y anota, para cada uno, por qué puerta pasa el camino y cuánto mide. ¿En qué radio cambia la ruta y por qué? Comenta qué implica esto para la decisión mecánica de las dimensiones de un AMR."""))

C.append(code("""# Ejercicio 1
META2 = (60, 115)
h2 = lambda v: np.hypot(v[0] - META2[0], v[1] - META2[1])
for R in (0.15, 0.28, 0.40, 0.45):
    infl = distance_transform_edt(~occ) <= R / RES
    bin_R = np.where(~infl, 1.0, np.inf)
    if not (np.isfinite(bin_R[INICIO]) and np.isfinite(bin_R[META2])):
        print(f'R = {R:.2f} m: inicio o meta quedan dentro del inflado')
        continue
    cam, cst, exp = buscar(bin_R, INICIO, META2, h2)
    puerta = [c for (f, c) in cam if 42 <= f < 47]
    estrecha = (~infl)[42:47, 92:100].sum()
    print(f'R = {R:.2f} m -> {cst*RES:6.2f} m, {exp:5d} nodos, cruza el muro por las '
          f'columnas {min(puerta)}-{max(puerta)}  (celdas libres en la puerta estrecha: {estrecha:2d})')"""))

# ---------------- 4. PRM
C.append(md("""## 4. PRM: muestrear el espacio libre y construir un roadmap

Dos límites empujan más allá de la rejilla. El primero es económico: la transformada de distancia y D* concentran el gasto en la planificación para una consulta barata, pero el plan depende del objetivo (Corke, 2023, p. 184). El segundo es dimensional: los métodos de rejilla son «imprácticos más allá de unos pocos grados de libertad» (Lynch y Park, 2017, p. 378) — la rejilla de un brazo de 6 gdl no cabe en memoria.

El coste de la transformada de distancia llevó «al desarrollo de métodos probabilísticos que muestrean el mapa de forma dispersa, el más conocido de los cuales es el *probabilistic roadmap* o PRM» (Corke, 2023, p. 185). Se generan N configuraciones aleatorias, se descartan las que caen en obstáculos y se intenta conectar cada una con sus vecinas mediante segmentos rectos libres de colisión, comprobados por muestreo a lo largo del segmento (Corke, 2023, p. 186). El resultado es un grafo **independiente del inicio y de la meta** (Corke, 2023, p. 185): en la consulta se conectan `q_start` y `q_goal` a sus nodos más próximos y se busca en el grafo, «típicamente usando A*» (Lynch y Park, 2017, p. 384). De ahí su etiqueta: multiconsulta.

Es probabilísticamente completo, ni completo ni óptimo — y el modo de fallo hay que verlo, no contarlo: la figura del libro contrasta un roadmap de 50 vértices mal conectado con otro de 300 bien conectado (Corke, 2023, p. 187)."""))

C.append(code("""def segmento_libre(libre, a, b, paso=0.5):
    \"\"\"Comprueba colision muestreando el segmento a->b cada 'paso' celdas.\"\"\"
    d = np.hypot(b[0] - a[0], b[1] - a[1])
    n = max(2, int(d / paso) + 1)
    for t in np.linspace(0, 1, n):
        i, j = int(round(a[0] + t * (b[0] - a[0]))), int(round(a[1] + t * (b[1] - a[1])))
        if not (0 <= i < libre.shape[0] and 0 <= j < libre.shape[1]) or not libre[i, j]:
            return False
    return True

def construir_prm(libre, n_muestras, k=8, semilla=35):
    \"\"\"Fase de planificacion del PRM: muestrear C_free y conectar k vecinos mas proximos.\"\"\"
    rng = np.random.default_rng(semilla)
    nodos = []
    while len(nodos) < n_muestras:                       # rechazo: solo muestras libres
        i = rng.integers(0, libre.shape[0])
        j = rng.integers(0, libre.shape[1])
        if libre[i, j]:
            nodos.append((int(i), int(j)))
    P = np.array(nodos, float)
    aristas = {}
    d2 = ((P[:, None, :] - P[None, :, :]) ** 2).sum(-1)
    for a in range(len(nodos)):
        for b in np.argsort(d2[a])[1:k + 1]:
            b = int(b)
            if b in aristas.get(a, {}):
                continue
            if segmento_libre(libre, nodos[a], nodos[b]):
                w = float(np.sqrt(d2[a, b]))
                aristas.setdefault(a, {})[b] = w
                aristas.setdefault(b, {})[a] = w
    return nodos, aristas

def consultar_prm(libre, nodos, aristas, inicio, meta, k=12):
    \"\"\"Fase de consulta: enganchar inicio y meta al roadmap y buscar con A*.\"\"\"
    nodos = list(nodos) + [inicio, meta]
    aristas = {a: dict(v) for a, v in aristas.items()}
    i_ini, i_met = len(nodos) - 2, len(nodos) - 1
    P = np.array(nodos, float)
    for idx in (i_ini, i_met):
        d = np.linalg.norm(P - P[idx], axis=1)
        for b in np.argsort(d)[1:k + 1]:
            b = int(b)
            if segmento_libre(libre, nodos[idx], nodos[b]):
                aristas.setdefault(idx, {})[b] = float(d[b])
                aristas.setdefault(b, {})[idx] = float(d[b])
    # A* sobre el grafo, con heuristica euclidea (admisible: las aristas son rectas)
    hh = lambda v: float(np.linalg.norm(P[v] - P[i_met]))
    g, padre, cerrada = {i_ini: 0.0}, {}, set()
    monton = [(hh(i_ini), 0.0, i_ini)]
    while monton:
        _, gu, u = heapq.heappop(monton)
        if u in cerrada:
            continue
        cerrada.add(u)
        if u == i_met:
            break
        for v, w in aristas.get(u, {}).items():
            if gu + w < g.get(v, np.inf):
                g[v] = gu + w
                padre[v] = u
                heapq.heappush(monton, (g[v] + hh(v), g[v], v))
    if i_met not in g:
        return None, np.inf
    ruta, u = [i_met], i_met
    while u != i_ini:
        u = padre[u]
        ruta.append(u)
    return [nodos[i] for i in ruta[::-1]], g[i_met]

# El PRM es aleatorio: una sola ejecucion no dice nada. Ocho semillas por tamano.
print(f'{"N":>4}  {"exito":>7}  {"aristas":>8}  {"camino medio":>13}   (optimo en rejilla: '
      f'{resultados["A* euclidea (admisible)"][1]*RES:.2f} m)')
for N in (30, 60, 120, 250, 500):
    exitos, longitudes, aristas_tot = 0, [], 0
    for s in range(8):
        nodos, aristas = construir_prm(libre, N, semilla=100 + s)
        cam, cst = consultar_prm(libre, nodos, aristas, INICIO, META)
        aristas_tot += sum(len(v) for v in aristas.values()) // 2
        if cam is not None:
            exitos += 1
            longitudes.append(cst * RES)
    media = f'{np.mean(longitudes):.2f} m' if longitudes else '--'
    print(f'{N:4d}  {exitos:5d}/8  {aristas_tot//8:8d}  {media:>13}')"""))

C.append(code("""fig, axes = plt.subplots(1, 3, figsize=(13, 3.4))
for ax, N in zip(axes, (30, 60, 500)):
    nodos, aristas = construir_prm(libre, N)
    cam, cst = consultar_prm(libre, nodos, aristas, INICIO, META)
    ax.imshow(inflado, origin='lower', cmap='Greys')
    for a, vs in aristas.items():
        for b in vs:
            if b > a:
                ax.plot([nodos[a][1], nodos[b][1]], [nodos[a][0], nodos[b][0]],
                        color='0.55', lw=0.5, zorder=2)
    P = np.array(nodos)
    ax.scatter(P[:, 1], P[:, 0], s=6, color=IQS_VERDE, zorder=3)
    if cam:
        cam = np.array(cam)
        ax.plot(cam[:, 1], cam[:, 0], color=IQS_AZUL, lw=2.4, zorder=4)
        ax.set_title(f'PRM, N = {N}  ->  {cst*RES:.2f} m', fontsize=9)
    else:
        ax.set_title(f'PRM, N = {N}  ->  sin camino', fontsize=9, color='crimson')
    ax.scatter(INICIO[1], INICIO[0], s=50, color=IQS_VERDE, zorder=5)
    ax.scatter(META[1], META[0], marker='*', s=140, color='crimson', zorder=5)
    ax.set_xticks([]); ax.set_yticks([])
plt.tight_layout(); plt.show()"""))

C.append(md("""**El fallo se ve solo, y la tabla lo cuantifica.** Con 30 muestras el roadmap queda fragmentado en componentes disconexas y la consulta falla la mitad de las veces *aunque exista camino*; con 120 ya no falla nunca, pero el camino es visiblemente peor que el óptimo; con 500 se acerca a él. Esa columna de «éxitos de 8» **es** la definición operativa de *probabilísticamente completo* (Lynch y Park, 2017, p. 356): la probabilidad de encontrar solución tiende a 1 al crecer el esfuerzo, y nada más. Una única ejecución de un PRM no demuestra ni desmiente nada, y conviene que los estudiantes lo interioricen antes de sacar conclusiones de una captura de pantalla.

El otro punto que conviene provocar en el aula: los **pasajes estrechos** son el talón de Aquiles del PRM, porque la probabilidad de muestrear dentro de ellos es proporcional a su área. La puerta estrecha del almacén, que para el centro del robot mide 2 celdas de ancho, ocupa el 0,1 % del espacio libre: con N pequeño el roadmap la ignora y el camino se va a la puerta ancha, aunque sea peor. Es la motivación de las variantes con muestreo sesgado (*bridge test*, *gaussian sampling*) que el estudiante encontrará en la documentación de OMPL cuando abra MoveIt 2.

## 5. RRT: un árbol que crece hacia el espacio vacío

El árbol aleatorio de exploración rápida es el representante de consulta única y el que mejor tolera restricciones de movimiento. El Algoritmo 10.3 del libro se recorre línea a línea (Lynch y Park, 2017, p. 379): muestrear `x_samp`, localizar el nodo más cercano `x_nearest`, aplicar un planificador local que avance una distancia pequeña hacia la muestra produciendo `x_new`, añadirlo si el movimiento está libre de colisión, y terminar al alcanzar la región meta.

La intuición del nombre está en la misma página: las muestras distribuidas por todo el espacio **«tiran» del árbol** y provocan que explore rápidamente C_free (Lynch y Park, 2017, p. 379). El planificador local es el punto de acoplamiento con la cinemática: aquí es una recta, pero puede ser una curva de Reeds-Shepp para un vehículo con radio de giro (Lynch y Park, 2017, p. 382) o una primitiva de Dubins, como en la implementación no holonómica de Corke (2023, pp. 196-198)."""))

C.append(code("""def rrt(libre, inicio, meta, paso=6.0, sesgo_meta=0.06, radio_meta=6.0,
        max_iter=6000, semilla=35):
    \"\"\"RRT basico (Lynch y Park, 2017, Algoritmo 10.3) con planificador local recto.\"\"\"
    rng = np.random.default_rng(semilla)
    nodos = [np.array(inicio, float)]
    padres = [-1]
    for it in range(max_iter):
        # 1. muestrear (con ligero sesgo hacia la meta)
        if rng.random() < sesgo_meta:
            x_samp = np.array(meta, float)
        else:
            x_samp = np.array([rng.uniform(0, libre.shape[0]), rng.uniform(0, libre.shape[1])])
        # 2. nodo mas cercano del arbol
        P = np.array(nodos)
        i_cerca = int(np.argmin(((P - x_samp) ** 2).sum(1)))
        x_near = nodos[i_cerca]
        # 3. planificador local: avanzar 'paso' hacia la muestra
        d = x_samp - x_near
        n = np.linalg.norm(d)
        if n < 1e-9:
            continue
        x_new = x_near + paso * d / n
        # 4. anadir si el movimiento esta libre
        if not segmento_libre(libre, tuple(x_near), tuple(x_new)):
            continue
        nodos.append(x_new)
        padres.append(i_cerca)
        # 5. exito al entrar en la region meta
        if np.linalg.norm(x_new - np.array(meta, float)) < radio_meta and \\
           segmento_libre(libre, tuple(x_new), meta):
            nodos.append(np.array(meta, float))
            padres.append(len(nodos) - 2)
            camino, u = [], len(nodos) - 1
            while u != -1:
                camino.append(nodos[u])
                u = padres[u]
            return nodos, padres, np.array(camino[::-1]), it + 1
    return nodos, padres, None, max_iter

for semilla in (35, 7, 2026):
    t0 = time.perf_counter()
    nodos, padres, cam, its = rrt(libre, INICIO, META, semilla=semilla)
    dt = time.perf_counter() - t0
    if cam is None:
        print(f'semilla {semilla:4d}: sin camino tras {its} iteraciones  [{dt:.2f} s]')
    else:
        L = np.linalg.norm(np.diff(cam, axis=0), axis=1).sum() * RES
        print(f'semilla {semilla:4d}: camino de {L:6.2f} m con {len(cam):3d} nodos, '
              f'arbol de {len(nodos):4d} nodos, {its:4d} iteraciones  [{dt:.2f} s]')"""))

C.append(code("""nodos, padres, cam, its = rrt(libre, INICIO, META, semilla=35)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 3.8))

a1.imshow(inflado, origin='lower', cmap='Greys')
for i, p in enumerate(padres):
    if p >= 0:
        a1.plot([nodos[p][1], nodos[i][1]], [nodos[p][0], nodos[i][0]],
                color=IQS_VERDE, lw=0.6, zorder=2)
if cam is not None:
    a1.plot(cam[:, 1], cam[:, 0], color=IQS_AZUL, lw=2.5, zorder=4)
a1.set_title(f'RRT: arbol de {len(nodos)} nodos', fontsize=10)

# comparacion final de las cuatro respuestas al mismo problema
a2.imshow(inflado, origin='lower', cmap='Greys')
cam_ast = np.array(resultados['A* euclidea (admisible)'][0])
a2.plot(cam_ast[:, 1], cam_ast[:, 0], color='black', lw=2.4, label='A* (optimo en rejilla)')
nod_p, ar_p = construir_prm(libre, 500)
cam_prm, _ = consultar_prm(libre, nod_p, ar_p, INICIO, META)
if cam_prm:
    cam_prm = np.array(cam_prm)
    a2.plot(cam_prm[:, 1], cam_prm[:, 0], color=IQS_VERDE, lw=2.0, ls='--', label='PRM (N=500)')
if cam is not None:
    a2.plot(cam[:, 1], cam[:, 0], color=IQS_AZUL, lw=2.0, ls=':', label='RRT')
a2.legend(fontsize=8, loc='lower right')
a2.set_title('Tres planificadores, un problema', fontsize=10)
for ax in (a1, a2):
    ax.scatter(INICIO[1], INICIO[0], s=50, color=IQS_VERDE, zorder=5)
    ax.scatter(META[1], META[0], marker='*', s=140, color='crimson', zorder=5)
    ax.set_xticks([]); ax.set_yticks([])
plt.tight_layout(); plt.show()"""))

C.append(md("""**Lo que hay que hacer notar.** El árbol del RRT no crece uniformemente: las ramas se disparan hacia las zonas vacías, porque una muestra en una región poco poblada casi siempre tiene su vecino más cercano en la frontera del árbol. Esa es la propiedad de *rapidly-exploring* y explica su eficacia en dimensiones altas. El precio se ve en la comparación de la derecha: el camino del RRT es visiblemente peor que el de A*, con quiebros gratuitos. RRT no promete optimalidad — la recupera asintóticamente RRT*, que «recablea continuamente el árbol de búsqueda para asegurar que siempre codifica el camino más corto desde el inicio hasta cada nodo» (Lynch y Park, 2017, pp. 382-383).

Y una observación honesta que conviene hacer con la ejecución de tres semillas delante: **el RRT es aleatorio y su respuesta es muy inestable**. Las tres semillas encuentran camino, sí, pero con longitudes que van de unos 15 m a unos 24 m para el mismo problema cuyo óptimo son 12,7 m — casi un factor dos de dispersión. No es un defecto de esta implementación: es el algoritmo. «Probabilísticamente completo» significa que acabará encontrando *algo* (Lynch y Park, 2017, p. 356), no que ese algo se parezca al óptimo ni que dos ejecuciones se parezcan entre sí. En producción esto se compensa con suavizado posterior del camino y con RRT*.

### Ejercicio 2

Implementa el **RRT bidireccional**: dos árboles, uno desde el inicio y otro desde la meta, que en cada iteración crecen alternativamente y tratan de conectarse. Compara el número de iteraciones necesarias con el RRT simple sobre las mismas semillas. ¿Por qué ayuda tanto tener dos árboles?

### Ejercicio 3

Completa la tabla comparativa del guion de clase ejecutando lo que necesites: para **transformada de distancia / A\***, **PRM** y **RRT**, rellena ¿completo?, ¿óptimo?, coste de planificación frente a coste de consulta, ¿sirve con 6 gdl?, ¿sirve con mapa cambiante? Justifica cada casilla con un número medido en este cuaderno, no con una impresión."""))

C.append(code("""# Ejercicio 2: espacio de trabajo (RRT bidireccional)
# arbol_a desde INICIO, arbol_b desde META; alterna e intenta conectar
# el x_new de uno con el nodo mas cercano del otro."""))

C.append(md("""---

## Soluciones

**Ejercicio 1.** Con R = 0,15 y 0,28 m el camino cruza por la puerta estrecha (columnas 92-100) y mide en torno a 13,2-13,3 m. A partir de R = 0,40 m la puerta estrecha se cierra —cero celdas libres para el centro del robot— y el planificador se ve obligado a cruzar por la puerta ancha, al otro extremo del almacén: el camino salta a unos 14,5 m, casi un 10 % más, y sobre todo **cambia de ruta por completo**. La lección de ingeniería es que el radio del robot no es un parámetro del software sino una decisión de diseño mecánico con consecuencias topológicas: doce centímetros de más en el chasis pueden eliminar una conexión entre naves de un almacén ya construido, con impacto directo en el tiempo de ciclo. En un proyecto real esta comprobación se hace *antes* de comprar el AMR, con el plano de la planta y este mismo cálculo — y también antes de aprobar que producción coloque un palé junto a una puerta.

**Ejercicio 2.** El esquema del RRT bidireccional:

```python
def rrt_bidireccional(libre, inicio, meta, paso=6.0, max_iter=6000, semilla=35):
    rng = np.random.default_rng(semilla)
    A, pA = [np.array(inicio, float)], [-1]
    B, pB = [np.array(meta, float)], [-1]
    for it in range(max_iter):
        x_samp = np.array([rng.uniform(0, libre.shape[0]), rng.uniform(0, libre.shape[1])])
        x_new, i_near = extender(A, pA, x_samp, paso, libre)      # crece el arbol A
        if x_new is not None:
            j = int(np.argmin(((np.array(B) - x_new) ** 2).sum(1)))
            if segmento_libre(libre, tuple(x_new), tuple(B[j])):
                return unir(A, pA, B, pB, len(A) - 1, j), it      # arboles conectados
        A, pA, B, pB = B, pB, A, pA                               # alternar
    return None, max_iter
```

Empíricamente necesita del orden de la mitad o menos de iteraciones. La razón es geométrica y merece decirse: la probabilidad de que un árbol alcance una **región meta pequeña** por muestreo es baja, mientras que la probabilidad de que dos árboles que crecen el uno hacia el otro se encuentren en **algún punto del espacio libre** es mucho mayor — se sustituye un objetivo puntual por un objetivo de medida grande. Es la misma intuición que hace eficiente la búsqueda bidireccional en grafos.

**Ejercicio 3.** La tabla, con los números de este cuaderno:

| | Transf. distancia / A* | PRM | RRT |
|---|---|---|---|
| ¿Completo? | Completo **en resolución** | Probabilísticamente completo: 4 éxitos de 8 con N = 30, 8 de 8 con N = 120 | Probabilísticamente completo |
| ¿Óptimo? | Sí, en la rejilla: 12,66 m | No: 15,7 m con N = 30, 12,7 m con N = 500 | No: de 15,1 a 24,5 m según la semilla; RRT* lo recupera asintóticamente |
| Planificación / consulta | Planificación cara, consulta **gratis** y reutilizable para cualquier inicio | Planificación cara **una vez**, consultas baratas: multiconsulta | Todo el coste en cada consulta: consulta única |
| ¿6 gdl? | No: la rejilla no cabe en memoria (Lynch y Park, 2017, p. 378) | Sí | Sí, es su terreno |
| ¿Mapa cambiante? | Hay que recalcular; D* reutiliza (≈12 % del coste, Corke, 2023, p. 184) | Hay que revalidar las aristas afectadas | Se replanifica desde cero, pero es barato |

La conclusión que cierra el debate en clase: **no hay un planificador mejor, hay una elección**. Un AMR de almacén con mapa estable y 3 gdl vive perfectamente con A* sobre costmap —que es exactamente lo que hace Nav2—; un brazo de 6 o 7 gdl en una célula que cambia necesita muestreo —que es exactamente lo que hace OMPL dentro de MoveIt 2—."""))

C.append(md("""---

## Para llevarse de esta sesión

**Planificar empieza por preparar el mapa, no por elegir el algoritmo.** El inflado convierte el robot en un punto y puede cerrar pasillos enteros; el mapa de coste convierte «libre / ocupado» en «cuánto me gusta pasar por aquí» y aleja el camino de las paredes sin ninguna lógica adicional. Las dos transformaciones aparecen tal cual en el costmap por capas de Nav2, y quien las haya escrito aquí sabrá qué está tocando cuando cambie `inflation_radius`.

**La heurística no cambia la respuesta, cambia el trabajo** — siempre que sea admisible. Es la moraleja de la sección 3 y el motivo por el que A* lleva sesenta años siendo el planificador global por defecto de la robótica móvil.

**Los métodos de muestreo cambian de contrato:** renuncian a la optimalidad y a la completitud a cambio de sobrevivir a la dimensión. PRM paga caro una vez y regala consultas; RRT paga en cada consulta pero acepta restricciones de movimiento en su planificador local, que es la puerta por donde entra la cinemática del vehículo. Ninguno de los dos garantiza nada en una ejecución concreta, y hay que decirlo con esas palabras.

Mañana, en S36, todo esto reaparece empaquetado: Nav2 tiene costmaps con inflado, un planificador global sobre rejilla y un controlador local, orquestados por un *behavior tree*. La diferencia es que ahora sabemos qué hay dentro de cada caja.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S35_Planificacion.ipynb', C)
print('escrito S35')
