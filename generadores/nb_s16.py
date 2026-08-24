from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('matplotlib','matplotlib'), ('spatialmath-python','spatialmath'),
       ('roboticstoolbox-python','roboticstoolbox')]
C = []

C.append(cabecera(
    "S16", "Cinemática inversa: analítica, ramas múltiples y métodos numéricos", "4",
    "viernes 16 de octubre de 2026", "2 h",
    "Resuelve la cinemática inversa del 2R plano en forma cerrada —con sus dos ramas de codo arriba y codo abajo y todos sus casos degenerados—, enumera las ocho soluciones analíticas del PUMA 560 y comprueba, semilla a semilla, que la cinemática inversa numérica con ikine_LM devuelve la rama que le toca y no la que uno espera.",
    "Lynch y Park (2017), cap. 6 — ley de cosenos y las dos soluciones del 2R plano con su espacio de trabajo, Figura 6.1 (p. 220), muñeca esférica y condición de convergencia (p. 221), theta1 = atan2(py, px) (p. 222), infinitas soluciones con px = py = 0 (p. 223), cuatro soluciones de posición del brazo con offset (pp. 223-224), orientación como ángulos de Euler ZYX (pp. 224-225), Newton-Raphson (pp. 226-227), algoritmo con pseudoinversa y tolerancias (p. 230), convergencia del 2R (pp. 231-232) y criterio secundario en redundantes (p. 233); Corke (2023), cap. 7 — muñeca esférica como condición necesaria de forma cerrada (p. 281), ocho soluciones, banderas de configuración, fuera de alcance y singularidad de muñeca con q4 = 0 (p. 282) e ikine_LM con semilla (p. 283).",
    "los apuntes del bloque 4"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
import roboticstoolbox as rtb
from spatialmath import SE3

np.set_printoptions(precision=4, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.4)
plt.rcParams['axes.grid'] = True
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('roboticstoolbox', rtb.__version__, '- listo.')"""))

C.append(md("""> **Aviso para Colab.** `roboticstoolbox-python` **tarda varios minutos** en instalarse la primera vez. Lanza la celda de instalación al abrir el cuaderno; la teoría de la sección 1 solo necesita numpy, así que se puede avanzar mientras corre.
>
> Como en S15, **nada de `robot.plot()` ni `robot.teach()`**: todo con salidas numéricas y figuras propias."""))

# ---------------- 1. IK analitica del 2R
C.append(md("""## 1. El 2R plano en forma cerrada: dos ramas y una ley de cosenos

La cinemática inversa invierte el mapa de S14: dada la pose deseada, encontrar las coordenadas articulares que la producen. **No es una función.** Puede no existir solución —si la pose está fuera del espacio de trabajo—, puede haber un número finito o puede haber infinitas.

El 2R plano contiene toda la esencia del método analítico. Dado el objetivo (x, y), el triángulo formado por los dos eslabones y la recta al objetivo se resuelve con la ley de cosenos: de `L1² + L2² − 2·L1·L2·cos(beta) = x² + y²` se despeja el ángulo interior del codo, y el del hombro se obtiene combinando `atan2(y, x)` con un ángulo auxiliar (Lynch y Park, 2017, p. 220). Existen **dos soluciones simétricas** respecto de la recta al objetivo, visibles en la Figura 6.1 del libro junto con el espacio de trabajo alcanzable (Lynch y Park, 2017, p. 220).

Dos disciplinas de cálculo que deben quedar automatizadas desde este ejemplo:

1. **Usar siempre `atan2` de dos argumentos**, que conserva el cuadrante, y nunca arcotangentes de cocientes (Lynch y Park, 2017, p. 219 y ss.).
2. **Discutir la existencia antes de calcular**: el argumento del arcocoseno debe estar en [−1, 1], y su valor límite delimita exactamente la frontera del espacio de trabajo."""))

C.append(code("""A1, A2 = 1.0, 0.8      # longitudes de los eslabones (m)

def ik_2r(x, y, a1=A1, a2=A2, tol=1e-12):
    \"\"\"IK analitica del 2R plano. Devuelve (estado, lista de soluciones [q1, q2]).
    estado: 'ok' | 'fuera' | 'dentro' | 'frontera' | 'infinitas'.\"\"\"
    r2 = x*x + y*y
    r = np.sqrt(r2)

    # --- discutir la EXISTENCIA antes de calcular nada ---
    if r > a1 + a2 + tol:
        return 'fuera', []                        # mas lejos que el brazo estirado
    if r < abs(a1 - a2) - tol:
        return 'dentro', []                       # dentro del agujero central
    if r < tol and abs(a1 - a2) < tol:
        return 'infinitas', []                    # objetivo en la base con a1 == a2

    # --- ley de cosenos para el codo (Lynch y Park, 2017, p. 220) ---
    c2 = np.clip((r2 - a1**2 - a2**2) / (2 * a1 * a2), -1.0, 1.0)
    s2 = np.sqrt(max(0.0, 1 - c2**2))

    sols = []
    for signo in (-1.0, +1.0):                    # codo arriba (-) y codo abajo (+)
        q2 = np.arctan2(signo * s2, c2)
        # el hombro: angulo al objetivo menos el angulo auxiliar del triangulo
        q1 = np.arctan2(y, x) - np.arctan2(a2 * np.sin(q2), a1 + a2 * np.cos(q2))
        sols.append(np.array([q1, q2]))

    if s2 < 1e-8:                                  # las dos ramas coinciden
        return 'frontera', [sols[0]]
    return 'ok', sols

def fk_2r(q, a1=A1, a2=A2):
    q1, q2 = q
    return np.array([a1*np.cos(q1) + a2*np.cos(q1+q2),
                     a1*np.sin(q1) + a2*np.sin(q1+q2)])

objetivo = (1.0, 0.9)
estado, sols = ik_2r(*objetivo)
print(f'objetivo {objetivo} -> estado: {estado}')
for etq, q in zip(['codo arriba', 'codo abajo '], sols):
    print(f'  {etq}: q = ({np.rad2deg(q[0]):7.2f}°, {np.rad2deg(q[1]):7.2f}°)  '
          f'-> FK = {fk_2r(q).round(6)}')"""))

C.append(md("""Verificar la IK con la FK **siempre**, sin excepciones. Es la única comprobación que detecta un error de signo o de cuadrante, y no cuesta nada. Aquí lo hacemos sobre una malla de objetivos aleatorios dentro del espacio de trabajo."""))

C.append(code("""rng = np.random.default_rng(16)
errores, ramas = [], 0
for _ in range(500):
    ang = rng.uniform(0, 2*np.pi)
    rad = rng.uniform(abs(A1-A2) + 0.02, A1 + A2 - 0.02)
    obj = np.array([rad*np.cos(ang), rad*np.sin(ang)])
    estado, sols = ik_2r(*obj)
    if estado != 'ok':
        continue
    ramas += len(sols)
    for q in sols:
        errores.append(np.linalg.norm(fk_2r(q) - obj))
errores = np.array(errores)
print(f'{len(errores)} soluciones comprobadas ({ramas//2} objetivos x 2 ramas)')
print(f'error maximo FK(IK(objetivo)) - objetivo: {errores.max():.3e} m')"""))

C.append(code("""fig, ax = plt.subplots(figsize=(5.8, 5.0))

# espacio de trabajo alcanzable: corona entre |a1-a2| y a1+a2 (Lynch y Park, 2017, p. 220)
ang = np.linspace(0, 2*np.pi, 300)
ax.plot((A1+A2)*np.cos(ang), (A1+A2)*np.sin(ang), '--', color='grey', lw=1)
ax.plot(abs(A1-A2)*np.cos(ang), abs(A1-A2)*np.sin(ang), '--', color='grey', lw=1)

for q, col, etq in zip(sols, [IQS_AZUL, IQS_VERDE], ['codo arriba', 'codo abajo']):
    q1, q2 = q
    p0 = np.array([0.0, 0.0])
    p1 = A1 * np.array([np.cos(q1), np.sin(q1)])
    p2 = p1 + A2 * np.array([np.cos(q1+q2), np.sin(q1+q2)])
    P = np.vstack([p0, p1, p2])
    ax.plot(P[:, 0], P[:, 1], 'o-', lw=3, ms=7, color=col, label=etq)

ax.plot(*objetivo, '*', ms=18, color='crimson', label='objetivo')
ax.plot([0, objetivo[0]], [0, objetivo[1]], ':', color='crimson', lw=1)
ax.set_aspect('equal'); ax.legend(fontsize=9)
ax.set_title('Las dos ramas de la IK del 2R: simétricas respecto de la recta al objetivo')
plt.tight_layout(); plt.show()"""))

C.append(md("""### Los casos degenerados, uno a uno

Aquí es donde se aprende de verdad. Recorremos las cuatro situaciones que rompen la fórmula ingenua:

- **fuera de alcance**: `r > a1 + a2`, el arcocoseno se sale de [−1, 1];
- **dentro del agujero central**: `r < |a1 − a2|`, con `a1 ≠ a2` el brazo no llega a doblarse tanto;
- **frontera del espacio de trabajo**: `r = a1 + a2` exactamente, las dos ramas colapsan en una — es la **singularidad** de la que hablará S18;
- **infinitas soluciones**: objetivo en la base con `a1 = a2`, cualquier `q1` sirve con `q2 = ±180°`. Es el análogo plano del caso `px = py = 0` del 6R (Lynch y Park, 2017, p. 223)."""))

C.append(code("""casos = [('normal            ', (1.0, 0.9), A1, A2),
         ('fuera de alcance  ', (1.9, 0.5), A1, A2),
         ('dentro del agujero', (0.05, 0.0), A1, A2),
         ('frontera exacta   ', (A1 + A2, 0.0), A1, A2),
         ('infinitas (a1==a2)', (0.0, 0.0), 1.0, 1.0)]

for etq, obj, a1, a2 in casos:
    estado, sols = ik_2r(*obj, a1=a1, a2=a2)
    detalle = ', '.join(f'({np.rad2deg(q[0]):.1f}°, {np.rad2deg(q[1]):.1f}°)' for q in sols)
    print(f'{etq}  objetivo {str(obj):>14}  ->  {estado:>9}  '
          f'{len(sols)} solucion(es)  {detalle}')

print('\\nNota: en la frontera las dos ramas coinciden (q2 = 0, brazo estirado).')
print('El determinante del jacobiano se anula ahi: es LA singularidad del 2R (S18).')"""))

C.append(md("""### Ejercicio 1

Dibuja el espacio de trabajo del 2R con `a1 = 1.0` y `a2 = 0.8` marcando en color distinto los puntos con dos soluciones, con una y con ninguna. Pista: barre una malla de puntos en `[-2, 2] x [-2, 2]` con `ik_2r` y colorea según el estado devuelto.

### Ejercicio 2

Modifica `ik_2r` para que, además de las dos ramas, devuelva la solución **más próxima a una configuración actual `q_ahora`** (la que minimiza `np.linalg.norm(q - q_ahora)` con los ángulos envueltos a [−π, π]). Ese criterio es el que usan de facto los controladores industriales para no dar volantazos entre puntos consecutivos de una trayectoria."""))

C.append(code("""# Ejercicio 1
# xs = np.linspace(-2, 2, 200); ys = np.linspace(-2, 2, 200)
# ...

# Ejercicio 2
# def envolver(a): return np.arctan2(np.sin(a), np.cos(a))
# ..."""))

# ---------------- 2. Las ocho soluciones del PUMA
C.append(md("""## 2. Las ocho soluciones del PUMA 560

La geometría que hace tratable el 6R industrial es la **muñeca esférica**: tres ejes que se cortan en un punto, el centro de muñeca (Lynch y Park, 2017, p. 221). «Una condición necesaria para la solución en forma cerrada de un robot de 6 ejes es un mecanismo de muñeca esférica» (Corke, 2023, p. 281).

Su virtud es que **desacopla** el problema: la posición del centro de muñeca depende solo de las tres primeras articulaciones y la orientación restante la absorben las tres de la muñeca. Para el brazo tipo PUMA sin offset, la primera sale directamente de la proyección en planta, `theta1 = atan2(py, px)` (Lynch y Park, 2017, p. 222); con offset de hombro aparecen dos soluciones —zurda y diestra— y las articulaciones 2 y 3 se reducen al 2R plano de la sección anterior, de modo que «en general, un brazo tipo PUMA con offset tendrá cuatro soluciones al problema de posición inversa» (Lynch y Park, 2017, pp. 223-224).

El problema de orientación es «completamente directo»: conocidas q1-q3, las tres articulaciones de la muñeca son los ángulos de Euler ZYX de una rotación conocida (Lynch y Park, 2017, pp. 224-225) — la conexión explícita con S13. Como la muñeca alcanza cada orientación de dos maneras (volteada o no), el total es **4 x 2 = 8**: «en general hay ocho configuraciones articulares distintas que dan la misma pose del efector» (Corke, 2023, p. 282).

Las banderas de `ikine_a` son `l`/`r` (zurda/diestra), `u`/`d` (codo arriba/abajo) y `f`/`n` (muñeca volteada o no) (Corke, 2023, p. 282)."""))

C.append(code("""puma = rtb.models.DH.Puma560()
T_obj = puma.fkine(puma.qn)
print('Pose objetivo (la del PUMA en qn):'); T_obj.printline()

banderas = ['lun', 'luf', 'ldn', 'ldf', 'run', 'ruf', 'rdn', 'rdf']
soluciones = {}
print(f\"\\n{'rama':>6} {'q1':>8} {'q2':>8} {'q3':>8} {'q4':>8} {'q5':>8} {'q6':>8}  ok?\")
for b in banderas:
    sol = puma.ikine_a(T_obj, b)
    soluciones[b] = sol.q
    ok = np.allclose(puma.fkine(sol.q).A, T_obj.A, atol=1e-6)
    g = np.rad2deg(sol.q)
    print(f'{b:>6} ' + ' '.join(f'{v:>8.1f}' for v in g) + f'  {ok}')

Q = np.array(list(soluciones.values()))
print(f'\\nConfiguraciones distintas: {len(np.unique(Q.round(4), axis=0))} de 8')
print('Todas producen EXACTAMENTE la misma pose del efector.')"""))

C.append(md("""Ocho maneras de coger la misma pieza. Elegir rama no es un tecnicismo: determina por dónde pasa el robot, qué obstáculos esquiva y cerca de qué singularidades trabaja. Y además, «debido a los límites mecánicos de los ángulos articulares y a posibles colisiones entre eslabones, no todas son físicamente alcanzables» (Corke, 2023, p. 282).

Lo comprobamos contra los límites articulares del modelo y dibujamos las ocho posturas."""))

C.append(code("""qlim = puma.qlim          # 2 x 6: fila 0 minimos, fila 1 maximos
print(f\"{'rama':>6} {'dentro de limites?':>20}  articulaciones fuera\")
alcanzables = []
for b, q in soluciones.items():
    fuera = [i+1 for i in range(6) if q[i] < qlim[0, i] or q[i] > qlim[1, i]]
    if not fuera:
        alcanzables.append(b)
    print(f'{b:>6} {str(len(fuera) == 0):>20}  {fuera if fuera else "-"}')
print(f'\\nFisicamente alcanzables: {len(alcanzables)} de 8 -> {alcanzables}')"""))

C.append(code("""def origenes(robot, q):
    return np.array([T.t for T in robot.fkine_all(q)])

fig = plt.figure(figsize=(11.5, 5.6))
for k, (b, q) in enumerate(soluciones.items()):
    ax = fig.add_subplot(2, 4, k+1, projection='3d')
    P = origenes(puma, q)
    col = IQS_VERDE if b in alcanzables else 'crimson'
    ax.plot(P[:, 0], P[:, 1], P[:, 2], 'o-', lw=2, ms=3.5, color=col)
    ax.scatter(*P[-1], s=60, marker='*', color='black')
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(0, 1.6)
    ax.set_title(b + ('' if b in alcanzables else ' (no alcanzable)'), fontsize=8)
    ax.set_xticklabels([]); ax.set_yticklabels([]); ax.set_zticklabels([])
fig.subplots_adjust(left=0.02, right=0.98, top=0.94, bottom=0.02, wspace=0.05, hspace=0.15)
plt.show()"""))

C.append(md("""Y los dos fallos con diagnóstico que conviene provocar delante de la clase: una pose **fuera de alcance** y la **singularidad de muñeca**. Con `q5 = 0` los ejes de las articulaciones 4 y 6 se alinean y «lo mejor que puede hacerse es restringir la suma»: los valores individuales quedan indeterminados (Corke, 2023, p. 282). Es el bloqueo de cardán de S13 reapareciendo en el hardware."""))

C.append(code("""sol_lejos = puma.ikine_a(SE3.Tx(3.0))
print('Objetivo a 3 m:  success =', sol_lejos.success, ' | razon:', sol_lejos.reason)

# --- singularidad de muneca: q5 = 0 alinea los ejes 4 y 6 ---
q_sing = np.array([0.0, 0.5, -1.0, 0.7, 0.0, 0.3])     # q5 = 0
T_sing = puma.fkine(q_sing)
print('\\nPostura con q5 = 0 (muñeca singular). q4 + q6 =',
      round(float(np.rad2deg(q_sing[3] + q_sing[5])), 3), 'grados')

for delta in [0.0, 0.4, -0.9]:
    q_alt = q_sing.copy()
    q_alt[3] += delta        # subo q4
    q_alt[5] -= delta        # y bajo q6 lo mismo: la suma no cambia
    igual = np.allclose(puma.fkine(q_alt).A, T_sing.A, atol=1e-9)
    print(f'  q4 = {np.rad2deg(q_alt[3]):7.2f}°, q6 = {np.rad2deg(q_alt[5]):7.2f}°'
          f'  -> ¿misma pose? {igual}')
print('\\nInfinitas soluciones: solo esta determinada la suma q4 + q6.')"""))

# ---------------- 3. IK numerica
C.append(md("""## 3. Cinemática inversa numérica: `ikine_LM` y la tiranía de la semilla

Cuando la geometría no da forma cerrada —cadenas redundantes, muñecas no esféricas, robots colaborativos con offsets— la IK se plantea como búsqueda de raíces: definir `g(q) = xd − f(q)` y resolver `g(q) = 0` con Newton-Raphson, linealizando en cada iteración con el jacobiano (Lynch y Park, 2017, pp. 226-227). Cuando el jacobiano no es cuadrado o es singular se usa su pseudoinversa, que da el menor cambio articular compatible con el error (Lynch y Park, 2017, p. 230).

Las propiedades prácticas son el espejo exacto de las analíticas. **A favor:** generalidad total. **En contra:** «siempre que exista una estimación inicial suficientemente próxima» es la condición de convergencia (Lynch y Park, 2017, p. 221), solo se obtiene una solución por ejecución y **la rama depende de la semilla**.

En la toolbox, `ikine_LM` implementa esta familia (Corke, 2023, p. 283). El experimento del taller es lanzar la misma pose objetivo con varias semillas y ver qué sale."""))

C.append(code("""semillas = {
    'qz (todo cero)': puma.qz,
    'qr (reposo)': puma.qr,
    'qn (la solucion exacta)': puma.qn,
    'perturbada +0.3': puma.qn + 0.3,
    'perturbada -0.5': puma.qn - 0.5,
    'lejana': np.array([1.5, -1.0, 2.0, 1.0, -1.0, 2.0]),
}

print(f\"{'semilla':>24} {'exito':>6} {'iter':>5} {'|error| pose':>13}   q obtenida (grados)\")
resultados = {}
for etq, q0 in semillas.items():
    sol = puma.ikine_LM(T_obj, q0=q0)
    resultados[etq] = sol
    err = np.abs(puma.fkine(sol.q).A - T_obj.A).max() if sol.success else np.nan
    g = np.rad2deg(sol.q).round(0)
    print(f'{etq:>24} {str(sol.success):>6} {sol.iterations:>5} {err:>13.2e}   {g}')"""))

C.append(code("""# ¿Cuantas ramas DISTINTAS ha encontrado el solver numerico?
qs = np.array([s.q for s in resultados.values() if s.success])
def envolver(a):
    return np.arctan2(np.sin(a), np.cos(a))
qs_norm = np.round(envolver(qs), 3)
unicas = np.unique(qs_norm, axis=0)
print(f'Semillas lanzadas: {len(qs)}   ->   ramas distintas encontradas: {len(unicas)}')

# ¿coincide alguna con las ocho analiticas?
Q_an = envolver(np.array(list(soluciones.values())))
print('\\n¿Cada solucion numerica coincide con alguna rama analitica?')
for etq, s in resultados.items():
    if not s.success:
        print(f'  {etq:>24}: no convergio'); continue
    d = np.abs(envolver(Q_an - s.q)).max(axis=1)
    j = int(d.argmin())
    print(f'  {etq:>24}: rama {banderas[j]:>4}  (distancia {d[j]:.4f} rad)')"""))

C.append(md("""**Lo que hay que hacer notar en clase.** Ni siquiera partiendo de una semilla razonable el solver devuelve «la solución obvia»: devuelve la primera raíz que encuentra bajando por el gradiente, que puede estar del otro lado del robot. Esa no unicidad no es un defecto de la implementación, es la estructura del problema.

La consecuencia industrial es directa: en una trayectoria punto a punto **hay que sembrar el solver con la configuración actual del robot**, no con cero, o el robot dará un volantazo entre dos puntos consecutivos. Lo comprobamos con un barrido: mismo objetivo, semillas aleatorias, y medimos cuánto se aleja la solución de la semilla."""))

C.append(code("""rng = np.random.default_rng(160)
dist_semilla, exitos = [], 0
for _ in range(40):
    q0 = rng.uniform(-2.0, 2.0, 6)
    sol = puma.ikine_LM(T_obj, q0=q0)
    if sol.success:
        exitos += 1
        dist_semilla.append(np.abs(envolver(sol.q - q0)).sum())
dist_semilla = np.array(dist_semilla)

fig, ax = plt.subplots(figsize=(8, 3.2))
ax.hist(dist_semilla, bins=14, color=IQS_AZUL, alpha=0.85)
ax.set_xlabel('desplazamiento articular total desde la semilla (rad)')
ax.set_ylabel('nº de casos'); ax.set_title('40 semillas aleatorias, la misma pose objetivo')
plt.tight_layout(); plt.show()

print(f'Convergieron {exitos} de 40 intentos.')
print(f'Desplazamiento articular desde la semilla: '
      f'min {dist_semilla.min():.2f}, mediana {np.median(dist_semilla):.2f}, '
      f'max {dist_semilla.max():.2f} rad')"""))

C.append(md("""### Ejercicio 3

Toma una trayectoria de diez poses en línea recta entre `puma.fkine(puma.qn)` y esa misma pose desplazada 20 cm en x. Resuélvela dos veces con `ikine_LM`: (a) sembrando siempre con `puma.qz` y (b) sembrando cada punto con la solución del punto anterior. Dibuja las seis coordenadas articulares en función del punto y compara la suavidad de las dos soluciones. ¿Cuál mandarías a un robot real?"""))

C.append(code("""# Ejercicio 3
T_a = puma.fkine(puma.qn)
T_b = SE3.Tx(0.2) * T_a
# Ts = [T_a.interp1(T_b, s) for s in np.linspace(0, 1, 10)]   # o usa rtb.ctraj
# ..."""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.** El resultado es una **corona circular** de radio exterior `a1 + a2 = 1.8` y radio interior `|a1 − a2| = 0.2`. Dentro de la corona hay dos soluciones en todos los puntos salvo en las dos circunferencias frontera, donde solo hay una (las ramas colapsan); fuera de la corona exterior y dentro de la interior no hay ninguna. El código:

```python
xs = ys = np.linspace(-2, 2, 300)
X, Y = np.meshgrid(xs, ys)
estados = np.vectorize(lambda x, y: {'ok': 2, 'frontera': 1}.get(ik_2r(x, y)[0], 0))(X, Y)
plt.contourf(X, Y, estados, levels=[-0.5, 0.5, 1.5, 2.5])
```

La lectura importante: la frontera del espacio de trabajo es exactamente el lugar geométrico donde el número de soluciones cambia. Ese cambio de número de soluciones es la firma de una **singularidad**, y por eso la frontera del espacio de trabajo y las singularidades son el mismo fenómeno visto desde dos lados (S18).

**Ejercicio 2.** Basta ordenar las ramas por distancia:

```python
def ik_2r_cercana(x, y, q_ahora, **kw):
    estado, sols = ik_2r(x, y, **kw)
    if not sols:
        return estado, None
    d = [np.abs(np.arctan2(np.sin(q - q_ahora), np.cos(q - q_ahora))).sum() for q in sols]
    return estado, sols[int(np.argmin(d))]
```

Envolver la diferencia a [−π, π] es imprescindible: sin eso, una solución a `q1 = 179°` y otra a `q1 = −179°` parecen estar a 358 grados cuando en realidad están a 2. Es el error clásico y da saltos espectaculares en el robot real. Nótese que este criterio **puede cambiar de rama** a mitad de trayectoria si el objetivo cruza una singularidad; los controladores industriales lo prohíben explícitamente y obligan a declarar la configuración en la instrucción de movimiento.

**Ejercicio 3.** Con semilla fija `qz` las coordenadas articulares dan saltos: cada punto se resuelve de forma independiente y el solver puede caer en ramas distintas para poses casi iguales, con discontinuidades de más de un radián entre puntos consecutivos. Con semilla encadenada (la solución anterior) las seis curvas salen suaves y monótonas, porque el solver arranca ya muy cerca de la raíz correcta y no tiene ocasión de saltar de cuenca de atracción.

A un robot real se manda la segunda, sin ninguna duda. Y conviene explicitar el porqué: la primera versión no es «peor numéricamente» —todas sus soluciones son exactas, todas producen la pose pedida—, es que es **físicamente imposible de ejecutar**, porque exigiría que la muñeca girara 180 grados entre dos puntos separados por 2 cm. Esa distinción entre «solución matemáticamente correcta» y «solución ejecutable» es el contenido de esta sesión."""))

C.append(md("""---

## Para llevarse de esta sesión

La cinemática inversa **no es una función**, y todo lo demás se deduce de ahí. Puede no haber solución, puede haber ocho o puede haber infinitas, y el trabajo del ingeniero no termina cuando encuentra una: termina cuando ha elegido cuál, con un criterio explícito.

La vía analítica existe cuando la geometría lo permite —muñeca esférica— y es imbatible: devuelve **todas** las ramas, de forma exacta, en microsegundos. La numérica funciona siempre, incluso en cadenas redundantes, pero devuelve una sola solución por ejecución y esa solución la decide la semilla. Ninguna de las dos «resuelve el problema» por sí sola: la analítica te obliga a elegir rama y la numérica elige por ti, que es peor.

Y un hilo que conviene dejar tendido hacia las dos sesiones siguientes: los tres puntos donde la IK se ha portado mal —la frontera del espacio de trabajo, la muñeca con `q5 = 0`, el salto de rama del solver numérico— son el mismo fenómeno. En todos ellos el jacobiano pierde rango. Eso es lo que vamos a construir en S17 y a diagnosticar en S18.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S16_Cinematica_Inversa.ipynb', C)
print('escrito S16')
