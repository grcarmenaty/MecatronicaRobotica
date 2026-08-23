from nbgen import md, code, cabecera, instalacion, escribir

PKG = [('numpy','numpy'), ('matplotlib','matplotlib'), ('scipy','scipy')]
C = []

C.append(cabecera(
    "S34", "Entorno ROS 2 y el árbol de transformadas TF2", "7",
    "viernes 27 de noviembre de 2026", "2 h",
    "Dos cosas muy distintas y las dos necesarias. Primero, una celda de diagnóstico que verifica si la máquina donde se ejecuta este cuaderno tiene ROS 2 accesible: variables de entorno, ejecutable `ros2`, versión y biblioteca `rclpy`. Segundo, la parte conceptual de TF2 reimplementada en numpy puro —composición de la cadena map → odom → base_link → laser, consulta de la pose de un sensor en el marco del mapa, el salto de la corrección de localización y la transformación de una nube de puntos del láser al mapa— para que la mecánica del árbol de transformadas quede entendida antes de tocar `tf2_ros`.",
    "docs.ros.org (Jazzy Jalisco), tutoriales *Introducing tf2* y concepto *About tf2*, y tutoriales de `tf2_tools` y `tf2_echo`; REP 105, *Coordinate Frames for Mobile Platforms*, para la convención map → odom → base_link.",
    "los apuntes del bloque 7"))

C.append(instalacion(PKG, """import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=3, suppress=True)
plt.rcParams['figure.figsize'] = (9, 3.2)
plt.rcParams['axes.grid'] = True
IQS_AZUL, IQS_VERDE = '#1B2A80', '#1FA355'
print('Listo.')"""))

# ---------------- 0. Aviso
C.append(md("""> ## ⚠️ ROS 2 **no** se ejecuta en Colab
>
> Conviene decirlo de entrada y sin rodeos, porque es la primera pregunta del taller. **Este cuaderno no ejecuta ROS 2, y no hay ningún truco de instalación que lo arregle.** ROS 2 Jazzy Jalisco es un conjunto de paquetes binarios para Ubuntu 24.04 que necesitan un descubrimiento DDS multicast entre procesos, una sesión con `source /opt/ros/jazzy/setup.bash` y —para Gazebo y RViz2— un servidor gráfico. Un cuaderno de Colab no es nada de eso: es un proceso Python efímero en un contenedor sin ninguna de esas piezas.
>
> Por tanto, **el taller de la sesión S34 se hace en el portátil de cada estudiante**, con ROS 2 nativo sobre Ubuntu 24.04 o con el contenedor Docker del curso, tal y como se anunció al cerrar S33. Los comandos del guion —`ros2 pkg create`, `colcon build`, `ros2 run`, `ros2 topic echo`, `ros2 run tf2_tools view_frames`— se teclean allí, no aquí.
>
> Entonces, ¿para qué sirve este cuaderno?
>
> 1. **Para verificar la instalación antes de venir a clase** (sección 1). La celda de diagnóstico se ejecuta *en la máquina del estudiante* —descargando el `.ipynb` y abriéndolo con Jupyter local, o pegando la celda en una terminal Python con el entorno de ROS 2 activado— e imprime un informe legible: qué variables de entorno hay, si `ros2` está en el `PATH`, qué distribución responde y si `rclpy` importa. Con eso, quien llegue el viernes con el entorno roto ya lo sabrá el jueves.
> 2. **Para entender TF2 sin TF2** (secciones 2 a 4). Lo que hace `tf2_ros` es álgebra de transformadas homogéneas con sellos de tiempo: exactamente las matrices de SE(3) del bloque 4. Reimplementarlo en cincuenta líneas de numpy quita la magia y deja ver qué se está calculando cuando se escribe `buffer.lookup_transform('map', 'laser', t)`, por qué el árbol es un árbol y no un grafo, y qué significa exactamente que la corrección de localización «salte».
>
> Ejecutado en Colab, el diagnóstico dirá honestamente que no hay ROS 2 y el resto del cuaderno funcionará igual."""))

# ---------------- 1. Diagnostico
C.append(md("""## 1. ¿Hay ROS 2 en esta máquina? Celda de diagnóstico

La celda siguiente no instala nada ni modifica nada: solo mira. Recorre las variables de entorno que un `source setup.bash` deja puestas, busca el ejecutable `ros2` en el `PATH`, le pide la versión mediante `subprocess` —con `try/except` y `timeout`, porque en una máquina sin ROS 2 la llamada falla y no debe reventar el cuaderno— e intenta importar `rclpy`.

Las variables que se comprueban y qué significan:

| Variable | Qué indica |
|---|---|
| `ROS_DISTRO` | Nombre de la distribución activa; en el curso debe decir `jazzy`. |
| `ROS_VERSION` | `2` si el entorno cargado es ROS 2 (un `1` delataría un ROS 1 heredado). |
| `AMENT_PREFIX_PATH` | Prefijos donde `ros2` busca paquetes; si está vacía, no se ha hecho `source`. |
| `ROS_DOMAIN_ID` | Dominio DDS. Dos ordenadores con el mismo dominio en la misma red **se ven entre sí**: en el aula conviene que cada pareja use uno distinto. |
| `RMW_IMPLEMENTATION` | Proveedor DDS elegido (`rmw_fastrtps_cpp` por defecto en Jazzy). |
| `ROS_LOCALHOST_ONLY` | Si vale `1`, el descubrimiento se limita a la máquina local. |

**El error más frecuente del taller no es que ROS 2 falte, sino que la terminal no lo tenga cargado**: sin `source /opt/ros/jazzy/setup.bash` no hay ni `ros2` ni variables, y el estudiante concluye que la instalación está rota cuando lo único que pasa es que su shell no la ha visto."""))

C.append(code("""import os, sys, shutil, subprocess, platform

CLAVES = ['ROS_DISTRO', 'ROS_VERSION', 'AMENT_PREFIX_PATH', 'ROS_DOMAIN_ID',
          'RMW_IMPLEMENTATION', 'ROS_LOCALHOST_ONLY', 'ROS_PYTHON_VERSION']

def diagnostico_ros2(timeout=8.0):
    \"\"\"Comprueba si hay ROS 2 accesible desde este interprete. No instala ni modifica nada.
    Devuelve un diccionario con los hallazgos; imprimirlo es tarea de informe_ros2().\"\"\"
    d = {'plataforma': f'{platform.system()} {platform.release()}',
         'python': sys.version.split()[0],
         'entorno': {k: os.environ.get(k) for k in CLAVES}}

    # --- 1. ejecutable ros2 en el PATH ---
    d['ruta_ros2'] = shutil.which('ros2')

    # --- 2. 'ros2 --version' por subprocess, blindado ---
    d['version'], d['error_version'] = None, None
    if d['ruta_ros2'] is not None:
        try:
            r = subprocess.run([d['ruta_ros2'], '--version'],
                               capture_output=True, text=True, timeout=timeout)
            salida = (r.stdout + r.stderr).strip()
            d['version'] = salida if salida else '(sin salida)'
        except FileNotFoundError:
            d['error_version'] = 'el ejecutable ha desaparecido entre which() y run()'
        except subprocess.TimeoutExpired:
            d['error_version'] = f'ros2 --version no ha respondido en {timeout:.0f} s'
        except OSError as e:
            d['error_version'] = f'error del sistema al lanzarlo: {e}'
        except Exception as e:                      # red de seguridad: nunca romper el cuaderno
            d['error_version'] = f'{type(e).__name__}: {e}'
    else:
        d['error_version'] = 'no hay ningun ejecutable llamado ros2 en el PATH'

    # --- 3. la biblioteca cliente de Python ---
    try:
        import rclpy
        d['rclpy'] = getattr(rclpy, '__file__', 'importado')
    except ImportError as e:
        d['rclpy'] = None
        d['error_rclpy'] = str(e)
    except Exception as e:
        d['rclpy'] = None
        d['error_rclpy'] = f'{type(e).__name__}: {e}'
    return d

print('Funcion de diagnostico definida.')"""))

C.append(code("""def informe_ros2(d=None, ancho=72):
    \"\"\"Imprime el diagnostico en formato legible y emite un veredicto.\"\"\"
    d = diagnostico_ros2() if d is None else d
    print('=' * ancho)
    print('  DIAGNOSTICO DE ROS 2  ·  82514 Mecatronica y Robotica  ·  sesion S34')
    print('=' * ancho)
    print(f'  Plataforma : {d["plataforma"]}')
    print(f'  Python     : {d["python"]}')
    print('-' * ancho)
    print('  Variables de entorno')
    for k, v in d['entorno'].items():
        if v is None:
            print(f'    {k:22s} -- no definida --')
        else:
            v = v if len(v) <= 44 else v[:41] + '...'
            print(f'    {k:22s} {v}')
    print('-' * ancho)
    print('  Ejecutable ros2')
    print(f'    ruta       : {d["ruta_ros2"] or "no encontrado en el PATH"}')
    print(f'    version    : {d["version"] or "(no obtenida)"}')
    if d['error_version']:
        print(f'    incidencia : {d["error_version"]}')
    print('-' * ancho)
    print('  Biblioteca cliente Python (rclpy)')
    print(f'    {"importa correctamente: " + str(d["rclpy"]) if d["rclpy"] else "no disponible: " + d.get("error_rclpy", "")}')
    print('=' * ancho)

    # --- veredicto ---
    distro = d['entorno'].get('ROS_DISTRO')
    if d['ruta_ros2'] and d['rclpy'] and distro:
        print(f'  VEREDICTO: entorno ROS 2 "{distro}" operativo.')
        if distro != 'jazzy':
            print(f'             AVISO: el curso usa jazzy y aqui hay {distro}.')
        if d['entorno'].get('ROS_DOMAIN_ID') is None:
            print('             AVISO: ROS_DOMAIN_ID sin definir (dominio 0). En el aula,')
            print('                    exporta uno distinto por pareja para no interferir.')
    elif d['ruta_ros2'] or d['rclpy'] or distro:
        print('  VEREDICTO: instalacion INCOMPLETA o entorno a medio cargar.')
        print('             Prueba:  source /opt/ros/jazzy/setup.bash  y repite.')
    else:
        print('  VEREDICTO: aqui NO hay ROS 2 -- es lo normal en Google Colab.')
        print('             El taller de S34 se hace en tu portatil (Ubuntu 24.04 nativo')
        print('             o el contenedor Docker del curso). Las secciones 2-4 de este')
        print('             cuaderno funcionan igual, porque son numpy puro.')
    print('=' * ancho)
    return d

diag = informe_ros2()"""))

C.append(md("""**Qué hacer con el resultado.** Si el veredicto dice que no hay ROS 2 y estás en Colab, todo correcto: sigue con la sección 2. Si estás en tu portátil y sale lo mismo, ese es el problema que hay que resolver *antes* del viernes, no durante el taller. La secuencia de comprobación es siempre la misma y en este orden:

```bash
source /opt/ros/jazzy/setup.bash     # 1. cargar el entorno
ros2 --version                       # 2. responde el ejecutable?
ros2 run demo_nodes_cpp talker       # 3. y en otra terminal (con source tambien):
ros2 run demo_nodes_py listener      #    llegan los mensajes?
```

Ese par talker/listener es el criterio de aceptación que se anunció en S32: si un nodo C++ y uno Python se hablan, el middleware funciona y el taller puede empezar. Si los procesos arrancan pero no llega nada, el sospechoso habitual no es ROS sino la red —cortafuegos bloqueando el multicast de descubrimiento DDS, o dos personas compartiendo `ROS_DOMAIN_ID`—.

### Ejercicio 1

Amplía `diagnostico_ros2` para que, si encuentra `ros2`, ejecute también `ros2 pkg list` y cuente cuántos paquetes hay instalados, informando de si están presentes tres que el taller necesita: `demo_nodes_py`, `tf2_tools` y `teleop_twist_keyboard`. Mantén el mismo blindaje con `try/except` y `timeout`, y haz que la función siga devolviendo un informe legible cuando no haya ROS 2."""))

C.append(code("""# Ejercicio 1: escribe aqui tu ampliacion.
# Pista: r = subprocess.run([ruta, 'pkg', 'list'], capture_output=True, text=True, timeout=20)
#        paquetes = r.stdout.split()"""))

# ---------------- 2. TF2 en numpy
C.append(md("""## 2. TF2 sin TF2: el árbol de transformadas en numpy puro

Lo que TF2 hace es esto y solo esto: mantener «la relación entre sistemas de coordenadas en una estructura de árbol almacenada en el tiempo (*buffered in time*)» y permitir «transformar puntos, vectores, etc., entre dos sistemas de coordenadas cualesquiera en cualquier instante deseado» (docs.ros.org, tutorial *Introducing tf2*). Cada arista del árbol es una transformada homogénea con sello de tiempo — un elemento de SE(3), exactamente el objeto del bloque 4.

La convención de un robot móvil está estandarizada en **REP 105, *Coordinate Frames for Mobile Platforms***, y es la cadena

```
map  →  odom  →  base_link  →  laser
```

con una división del trabajo que hay que tener clarísima antes del taller:

| Arista | Quién la publica | Cómo se comporta |
|---|---|---|
| `map → odom` | El sistema de localización (AMCL en S36) | **Salta.** Discontinua, pero sin deriva a largo plazo. |
| `odom → base_link` | La odometría (ruedas + IMU) | **Continua y suave.** Nunca salta, pero deriva sin límite. |
| `base_link → laser` | `robot_state_publisher`, desde el URDF | **Fija.** Es geometría de montaje, no cambia. |

Toda la arquitectura de navegación de ROS 2 descansa en esa tabla: quien necesita continuidad (un controlador local) trabaja en `odom`; quien necesita consistencia global (un planificador) trabaja en `map`.

Empecemos por las piezas de álgebra."""))

C.append(code("""# ---------- transformadas homogeneas 4x4 (SE(3)), como en el bloque 4 ----------

def Rz(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s, 0.], [s, c, 0.], [0., 0., 1.]])

def Ry(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, 0., s], [0., 1., 0.], [-s, 0., c]])

def T(x=0.0, y=0.0, z=0.0, yaw=0.0, pitch=0.0):
    \"\"\"Transformada homogenea padre->hijo: rotacion Rz(yaw)Ry(pitch) y traslacion (x,y,z).\"\"\"
    M = np.eye(4)
    M[:3, :3] = Rz(yaw) @ Ry(pitch)
    M[:3, 3] = (x, y, z)
    return M

def inversa(M):
    \"\"\"Inversa de una transformada homogenea, sin invertir la matriz: R^T y -R^T t.\"\"\"
    R, t = M[:3, :3], M[:3, 3]
    Mi = np.eye(4)
    Mi[:3, :3] = R.T
    Mi[:3, 3] = -R.T @ t
    return Mi

def aplicar(M, P):
    \"\"\"Aplica M a un punto o a una nube (N,3). Devuelve (N,3).\"\"\"
    P = np.atleast_2d(np.asarray(P, float))
    return P @ M[:3, :3].T + M[:3, 3]

def xyyaw(M):
    \"\"\"Lectura amable de una pose plana: (x, y, yaw en grados).\"\"\"
    return M[0, 3], M[1, 3], np.degrees(np.arctan2(M[1, 0], M[0, 0]))

# comprobacion elemental: M @ inversa(M) = I
M = T(1.5, -0.4, 0.2, yaw=0.7, pitch=0.1)
print('||M @ inversa(M) - I|| =', np.abs(M @ inversa(M) - np.eye(4)).max())"""))

C.append(md("""Ahora el árbol. Lo representamos como un diccionario `hijo -> (padre, T_padre_hijo)`, que es justo la información que viaja por los topics `/tf` y `/tf_static`: cada mensaje `TransformStamped` lleva un `frame_id` (el padre), un `child_frame_id` y la transformada.

La consulta `lookup(destino, origen)` devuelve la matriz que **lleva puntos expresados en `origen` a coordenadas de `destino`**, subiendo desde cada frame hasta el ancestro común y componiendo. Es lo mismo que hace `Buffer.lookup_transform(destino, origen, t)` de `tf2_ros`, sin la interpolación temporal (que añadimos en el ejercicio 3)."""))

C.append(code("""# ---------- el arbol de frames: hijo -> (padre, T_padre_hijo) ----------

def cadena_a_raiz(frame, arbol):
    ruta = [frame]
    while frame in arbol:
        frame = arbol[frame][0]
        ruta.append(frame)
    return ruta

def lookup(destino, origen, arbol):
    \"\"\"T_destino_origen: la transformada que expresa en 'destino' lo que estaba en 'origen'.\"\"\"
    r_destino = cadena_a_raiz(destino, arbol)
    comun = next((f for f in cadena_a_raiz(origen, arbol) if f in r_destino), None)
    if comun is None:
        raise ValueError(f'no hay camino de {origen!r} a {destino!r}: el arbol esta roto')
    def hasta_comun(f):                      # compone T_comun_f subiendo por el arbol
        M = np.eye(4)
        while f != comun:
            padre, T_padre_hijo = arbol[f]
            M = T_padre_hijo @ M
            f = padre
        return M
    return inversa(hasta_comun(destino)) @ hasta_comun(origen)

# ---------- el arbol del AMR del taller, segun REP 105 ----------
arbol = {
    # localizacion: corrige la deriva de la odometria. Salta.
    'odom':      ('map',       T(0.30, -0.15, yaw=np.radians(2.0))),
    # odometria: continua, deriva. Es la pose del robot "segun sus ruedas".
    'base_link': ('odom',      T(4.00,  1.20, yaw=np.radians(35.0))),
    # montaje del laser, del URDF: 20 cm delante, 18 cm arriba, 3 grados cabeceando.
    'laser':     ('base_link', T(0.20,  0.00, 0.18, pitch=np.radians(3.0))),
}

for hijo, (padre, _) in arbol.items():
    print(f'  {padre:10s} -> {hijo}')
print('\\nraiz del arbol:', cadena_a_raiz('laser', arbol)[-1])"""))

# ---------------- 3. Pose del sensor en el mapa
C.append(md("""## 3. ¿Dónde está el láser, visto desde el mapa?

Esta es la consulta que en el taller se hace con `ros2 run tf2_ros tf2_echo map laser` y que dentro de cualquier nodo se escribe `buffer.lookup_transform('map', 'laser', tiempo)`. Aquí sale de componer tres matrices.

Conviene hacer notar en clase la diferencia entre las tres respuestas: la pose del robot **según su odometría** (`odom → base_link`), la pose del robot **según el mapa** (`map → base_link`, ya corregida) y la pose del **sensor** en el mapa (`map → laser`, que además incorpora el montaje). Confundirlas es el origen de la mitad de los errores de integración que veremos en S36."""))

C.append(code("""for destino, origen in [('odom', 'base_link'), ('map', 'base_link'),
                        ('map', 'laser'), ('base_link', 'laser'), ('laser', 'map')]:
    x, y, yaw = xyyaw(lookup(destino, origen, arbol))
    print(f'  T_{destino:10s}_{origen:10s}  x={x:7.3f}  y={y:7.3f}  yaw={yaw:8.2f} deg')

print()
# la propiedad que hace del arbol un arbol y no una coleccion de datos sueltos:
A = lookup('map', 'laser', arbol)
B = inversa(lookup('laser', 'map', arbol))
print('lookup(map,laser) == inversa(lookup(laser,map)) ?',
      bool(np.allclose(A, B)))

# y la composicion es asociativa: map<-base <- laser
Cc = lookup('map', 'base_link', arbol) @ lookup('base_link', 'laser', arbol)
print('composicion por tramos == consulta directa ?', bool(np.allclose(A, Cc)))"""))

C.append(md("""### Qué pasa cuando la corrección de localización salta

Aquí está la lección central de la sesión. AMCL no publica una corrección suave: publica la que corresponde a su estimación actual, y cuando el filtro de partículas resuelve una ambigüedad —o el robot cierra un bucle— esa estimación **cambia de golpe**. La arista `map → odom` salta.

Simulamos exactamente eso: el robot avanza en línea recta según su odometría, y a mitad de recorrido la localización se corrige 0,45 m y 6°. Miramos las dos trayectorias, en `odom` y en `map`."""))

C.append(code("""pasos = 60
salto_en = 30
correccion_antes   = T(0.30, -0.15, yaw=np.radians(2.0))
correccion_despues = T(0.72,  0.02, yaw=np.radians(8.0))   # AMCL reubica al robot

pos_odom, pos_map = [], []
for k in range(pasos):
    # odometria: avance continuo y suave, sin ningun salto jamas
    arbol['base_link'] = ('odom', T(0.10 * k, 0.02 * k, yaw=np.radians(12.0)))
    # localizacion: constante a trozos, con un salto en 'salto_en'
    arbol['odom'] = ('map', correccion_antes if k < salto_en else correccion_despues)
    pos_odom.append(lookup('odom', 'base_link', arbol)[:3, 3])
    pos_map.append(lookup('map',  'base_link', arbol)[:3, 3])

pos_odom, pos_map = np.array(pos_odom), np.array(pos_map)
d_odom = np.linalg.norm(np.diff(pos_odom, axis=0), axis=1)
d_map  = np.linalg.norm(np.diff(pos_map,  axis=0), axis=1)
print(f'Desplazamiento por paso en odom : min {d_odom.min():.3f}  max {d_odom.max():.3f} m')
print(f'Desplazamiento por paso en map  : min {d_map.min():.3f}  max {d_map.max():.3f} m')
print(f'\\nEl salto de la correccion aparece en map como un desplazamiento de '
      f'{d_map.max():.3f} m en un solo paso.')"""))

C.append(code("""fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.6))
a1.plot(pos_odom[:, 0], pos_odom[:, 1], 'o-', ms=3, color=IQS_VERDE, lw=2,
        label='base_link en odom (continua)')
a1.plot(pos_map[:, 0], pos_map[:, 1], 'o-', ms=3, color=IQS_AZUL, lw=2,
        label='base_link en map (salta)')
a1.scatter(*pos_map[salto_en, :2], s=120, facecolor='none', edgecolor='crimson', lw=2,
           zorder=5, label='paso del salto')
a1.set_aspect('equal'); a1.legend(fontsize=8); a1.set_title('Trayectoria en los dos marcos')
a1.set_xlabel('x [m]'); a1.set_ylabel('y [m]')

a2.plot(d_odom, color=IQS_VERDE, lw=2, label='en odom')
a2.plot(d_map, color=IQS_AZUL, lw=2, label='en map')
a2.axvline(salto_en - 1, color='crimson', ls=':', lw=2)
a2.set_xlabel('paso'); a2.set_ylabel('desplazamiento [m]')
a2.set_title('Continuidad: |Δposición| por paso'); a2.legend(fontsize=8)
plt.tight_layout(); plt.show()"""))

C.append(md("""**Lo que hay que decir en clase mientras se ve el gráfico.** El robot físico no ha dado ningún salto: se ha movido igual de suave todo el rato, y la curva verde lo demuestra. Lo que ha saltado es *nuestra creencia sobre dónde estaba*. Por eso REP 105 separa los dos marcos y por eso la regla de oro de la navegación es:

- **Control local y evitación de obstáculos → marco `odom`.** Un controlador que derive su acción de una posición que salta 45 cm produciría una sacudida en los motores.
- **Metas, planificación global y almacenamiento de mapas → marco `map`.** Ahí la deriva acumulada arruinaría cualquier objetivo dado en coordenadas absolutas.

Y un corolario que en el taller sale solo: si dos nodos publican la misma arista `odom → base_link` —por ejemplo, la odometría de ruedas y un filtro de fusión que nadie desactivó—, TF2 recibe dos versiones alternadas del mismo dato y el robot «tiembla» en RViz. El árbol es un árbol: **cada frame tiene exactamente un padre**.

### Ejercicio 2

Cuantifica la deriva. Haz que `odom → base_link` acumule un error creciente (por ejemplo, un yaw que crece 0,3° por paso además del avance) y que `map → odom` se corrija cada 20 pasos para compensarlo exactamente. Representa, frente al paso: (a) el error de la pose en `odom` respecto de la verdad, que debe crecer sin límite; y (b) el error en `map`, que debe quedar acotado pero con dientes de sierra. Es la figura que resume por qué existe la arista de localización."""))

C.append(code("""# Ejercicio 2: espacio de trabajo
# verdad = T(...)   # pose real conocida por construccion
# error_odom.append(np.linalg.norm(...))"""))

# ---------------- 4. Nube de puntos
C.append(md("""## 4. Del barrido láser al mapa: transformar una nube de puntos

El caso de uso que justifica todo lo anterior. Un `sensor_msgs/msg/LaserScan` llega con un `frame_id` que dice `laser`: los rangos están medidos **desde el sensor**, en su sistema de coordenadas. Para dibujarlos sobre el mapa, compararlos con paredes conocidas o meterlos en un costmap hay que llevarlos al marco `map`, y eso es una única multiplicación por `T_map_laser` aplicada a toda la nube de golpe.

Montamos un escenario cerrado: un mapa con paredes, un robot con una pose real conocida, un barrido de 360 haces generado por trazado de rayos contra esas paredes, y la reconstrucción en el mapa. Al final comparamos qué pasa si se usa la transformada correcta y qué pasa si se usa la equivocada."""))

C.append(code("""# ---------- escenario: una sala rectangular con dos obstaculos ----------
PAREDES = [((0., 0.), (12., 0.)), ((12., 0.), (12., 8.)),
           ((12., 8.), (0., 8.)), ((0., 8.), (0., 0.)),
           ((4., 2.), (4., 5.)), ((7., 6.), (10., 6.))]

def trazar_rayo(origen, direccion, alcance=15.0):
    \"\"\"Distancia al primer segmento de PAREDES cortado por el rayo. Alcance si no corta.\"\"\"
    ox, oy = origen; dx, dy = direccion
    mejor = alcance
    for (ax, ay), (bx, by) in PAREDES:
        ex, ey = bx - ax, by - ay
        den = dx * ey - dy * ex
        if abs(den) < 1e-12:
            continue
        t = ((ax - ox) * ey - (ay - oy) * ex) / den      # a lo largo del rayo
        s = ((ax - ox) * dy - (ay - oy) * dx) / den      # a lo largo del segmento
        if 0.0 < t < mejor and 0.0 <= s <= 1.0:
            mejor = t
    return mejor

def barrido(pose_xy, yaw, n=360, alcance=15.0, sigma=0.02, rng=None):
    \"\"\"Devuelve (angulos, rangos) de un LaserScan simulado, en el marco del sensor.\"\"\"
    ang = np.linspace(-np.pi, np.pi, n, endpoint=False)
    rangos = np.array([trazar_rayo(pose_xy, (np.cos(yaw + a), np.sin(yaw + a)), alcance)
                       for a in ang])
    if rng is not None:
        rangos = rangos + rng.normal(0, sigma, n)
    return ang, rangos

print('Escenario listo:', len(PAREDES), 'segmentos de pared.')"""))

C.append(code("""rng = np.random.default_rng(34)

# --- pose real del robot (la que el mundo conoce y el robot no) ---
X_REAL, Y_REAL, YAW_REAL = 6.0, 3.0, np.radians(25.0)

# --- el arbol tal y como lo publica el robot ---
arbol = {
    'odom':      ('map',       T(0.0, 0.0, yaw=0.0)),           # localizacion perfecta, de momento
    'base_link': ('odom',      T(X_REAL, Y_REAL, yaw=YAW_REAL)),
    'laser':     ('base_link', T(0.20, 0.0, 0.18, pitch=np.radians(3.0))),
}

# el sensor esta 20 cm delante del centro del robot: el barrido sale de AHI
T_map_laser = lookup('map', 'laser', arbol)
x_l, y_l, yaw_l = xyyaw(T_map_laser)
ang, rangos = barrido((x_l, y_l), np.radians(yaw_l), n=360, sigma=0.02, rng=rng)

# --- la nube, en el marco del sensor: (N,3) con z=0 ---
nube_laser = np.stack([rangos * np.cos(ang), rangos * np.sin(ang), np.zeros_like(ang)], axis=1)

# --- una sola linea la lleva al mapa ---
nube_map = aplicar(T_map_laser, nube_laser)

# --- y la version equivocada: usar base_link como si fuera el sensor ---
nube_mal = aplicar(lookup('map', 'base_link', arbol), nube_laser)

valido = rangos < 14.5
err = np.linalg.norm(nube_map[valido, :2] - nube_mal[valido, :2], axis=1)
print(f'Puntos del barrido: {len(rangos)}  (con eco: {valido.sum()})')
print(f'Error medio al ignorar el montaje base_link->laser: {err.mean():.3f} m')
print(f'Altura media de la nube en el mapa (por el cabeceo de 3 grados): {nube_map[valido, 2].mean():.3f} m')"""))

C.append(code("""fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 4.0))

for ax, titulo in [(a1, 'Nube en el marco del sensor (laser)'),
                   (a2, 'La misma nube en el marco del mapa')]:
    ax.set_aspect('equal'); ax.set_title(titulo, fontsize=10)
    ax.set_xlabel('x [m]'); ax.set_ylabel('y [m]')

a1.scatter(nube_laser[valido, 0], nube_laser[valido, 1], s=4, color=IQS_AZUL)
a1.scatter([0], [0], marker='^', s=120, color=IQS_VERDE, zorder=5)
a1.text(0.3, 0.3, 'laser', fontsize=8, color=IQS_VERDE)

for (ax_, ay_), (bx_, by_) in PAREDES:
    a2.plot([ax_, bx_], [ay_, by_], color='0.35', lw=2.5, zorder=1)
a2.scatter(nube_map[valido, 0], nube_map[valido, 1], s=5, color=IQS_AZUL,
           label='T_map_laser (correcta)', zorder=3)
a2.scatter(nube_mal[valido, 0], nube_mal[valido, 1], s=5, color='crimson', alpha=0.45,
           label='T_map_base_link (mal)', zorder=2)
a2.scatter([X_REAL], [Y_REAL], marker='o', s=70, color=IQS_VERDE, zorder=5, label='base_link')
a2.scatter([x_l], [y_l], marker='^', s=90, color='black', zorder=5, label='laser')
a2.legend(fontsize=7, loc='upper left')
plt.tight_layout(); plt.show()"""))

C.append(md("""**Cómo leerlo.** A la izquierda, la nube tal y como la ve el sensor: un dibujo centrado en sí mismo, sin ninguna relación con el mapa. A la derecha, la misma nube transformada: los puntos caen **sobre las paredes**. Nadie ha «alineado» nada; simplemente se ha aplicado la composición de la cadena.

La nube roja es el error clásico de un estudiante con prisa: usar la pose del robot en lugar de la del sensor. Con 20 cm de desplazamiento el desajuste ya es visible, y en un costmap eso significa marcar como ocupadas celdas libres justo delante del robot. Es también, dicho sea de paso, la razón por la que la calibración extrínseca de los sensores no es papeleo: la arista `base_link → laser` del URDF **es** el resultado de esa calibración.

Un detalle que suele pasar desapercibido y merece un minuto: por el cabeceo de 3° del montaje, la nube transformada no está exactamente a z = 0. Un LiDAR 2D mal nivelado no mide un corte horizontal del mundo, sino un cono — y a 10 metros esos 3° son medio metro de altura. En un pasillo con rampa, eso es lo que hace que el robot «vea» el suelo como si fuera un obstáculo.

### Ejercicio 3

TF2 no solo compone: **interpola en el tiempo**. Implementa `lookup_interpolado(destino, origen, t)` sobre un búfer de transformadas con sello de tiempo `[(t0, T0), (t1, T1), ...]`, interpolando linealmente la traslación y el ángulo de yaw entre las dos muestras que rodean a `t`. Después comprueba qué pasa si se pide una `t` posterior a la última muestra: TF2 lanza en ese caso una `ExtrapolationException`, y tu función debería hacer algo equivalente. ¿Por qué crees que la biblioteca prefiere fallar a extrapolar?"""))

C.append(code("""# Ejercicio 3: espacio de trabajo
# buffer = [(0.0, T(0,0)), (0.1, T(0.05,0)), (0.2, T(0.11,0.01))]
# def lookup_interpolado(destino, origen, t, buffer): ..."""))

# ---------------- Soluciones
C.append(md("""---

## Soluciones

**Ejercicio 1.** La ampliación natural, respetando el blindaje del original:

```python
d['paquetes'] = None
if d['ruta_ros2'] is not None:
    try:
        r = subprocess.run([d['ruta_ros2'], 'pkg', 'list'],
                           capture_output=True, text=True, timeout=20)
        paquetes = set(r.stdout.split())
        d['paquetes'] = len(paquetes)
        d['taller'] = {p: (p in paquetes) for p in
                       ('demo_nodes_py', 'tf2_tools', 'teleop_twist_keyboard')}
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as e:
        d['error_paquetes'] = f'{type(e).__name__}: {e}'
```

Un Jazzy de escritorio (`ros-jazzy-desktop`) suele rondar los 300-400 paquetes. La comprobación útil no es el número sino la lista: `teleop_twist_keyboard` **no** viene en el metapaquete de escritorio y hay que instalarlo aparte (`sudo apt install ros-jazzy-teleop-twist-keyboard`), y es exactamente el que falta cada año a mitad de la Parte 2 del taller.

**Ejercicio 2.** Con la odometría acumulando 0,3°/paso, el error en `odom` crece de forma monótona —y aproximadamente lineal en el ángulo, cuadrática en la posición al integrarlo sobre el avance—, sin ninguna cota. En `map`, el error crece igual entre correcciones pero vuelve a cero cada 20 pasos: la gráfica es una sierra acotada por lo que la odometría puede derivar en un intervalo de corrección. Las dos conclusiones para el aula: (1) `map` es *exacta pero discontinua* y `odom` es *continua pero inexacta*, y no existe un marco que sea las dos cosas — de ahí que REP 105 obligue a tener ambos; (2) la altura de los dientes de sierra es el criterio de diseño para elegir la frecuencia de AMCL: si el robot deriva más de lo que tolera el controlador entre dos correcciones, hay que localizar más a menudo (o mejorar la odometría).

**Ejercicio 3.** La interpolación:

```python
def lookup_interpolado(destino, origen, t, buf):
    ts = [ti for ti, _ in buf]
    if t < ts[0] or t > ts[-1]:
        raise ValueError(f'extrapolacion pedida en t={t}: el buffer cubre [{ts[0]}, {ts[-1]}]')
    k = np.searchsorted(ts, t)
    if k == 0 or ts[k] == t:
        return buf[k][1]
    (t0, T0), (t1, T1) = buf[k - 1], buf[k]
    a = (t - t0) / (t1 - t0)
    x = (1 - a) * T0[0, 3] + a * T1[0, 3]
    y = (1 - a) * T0[1, 3] + a * T1[1, 3]
    y0, y1 = np.arctan2(T0[1, 0], T0[0, 0]), np.arctan2(T1[1, 0], T1[0, 0])
    dyaw = (y1 - y0 + np.pi) % (2 * np.pi) - np.pi     # camino corto en el circulo
    return T(x, y, yaw=y0 + a * dyaw)
```

Dos finuras que conviene comentar: la traslación se interpola linealmente sin problema, pero **el ángulo hay que interpolarlo por el camino corto** (de ahí el módulo), porque de 179° a −179° la interpolación ingenua daría una vuelta completa; y en 3D el equivalente correcto es un `slerp` sobre cuaterniones, que es justo lo que hace `tf2`.

Sobre por qué TF2 prefiere fallar a extrapolar: extrapolar es inventarse datos, y en TF2 el resultado se usa para decidir dónde hay obstáculos. Si el nodo del láser va 200 ms retrasado y alguien extrapola la pose del robot, la nube se pega sobre las paredes del mapa con un desplazamiento silencioso y sistemático, y el fallo aparece más tarde, en otro sitio, como «el costmap tiene fantasmas». Una excepción es ruidosa y se arregla; un dato inventado es plausible y se propaga. Ese es el criterio de diseño."""))

C.append(md("""---

## Para llevarse de esta sesión

**ROS 2 no se ejecuta en un cuaderno, y está bien que así sea.** Es un sistema distribuido de procesos que se descubren por DDS, no una biblioteca de Python. Lo que sí cabe en un cuaderno es la comprobación previa —el diagnóstico de la sección 1, que cada estudiante debe pasar en su portátil antes del taller— y la parte conceptual, que es la que de verdad cuesta entender.

**TF2 es álgebra del bloque 4 con dos añadidos:** un árbol que dice qué se compone con qué, y un búfer temporal que dice *cuándo*. Ni más ni menos. Una vez visto que `lookup('map', 'laser')` son tres matrices multiplicadas, deja de ser magia y pasa a ser contabilidad — y con ello se puede razonar sobre sus fallos en lugar de sufrirlos.

**La tabla de REP 105 es el resumen de la sesión:** `odom → base_link` continua y con deriva; `map → odom` exacta y con saltos; `base_link → laser` fija y calibrada. Quien tenga clara esa división sabrá, en S36, por qué AMCL publica precisamente la arista que publica y no la pose del robot, y por qué el controlador local de Nav2 trabaja en `odom` mientras el planificador global trabaja en `map`.

Mañana, en S35, dejamos de mover el robot y empezamos a decidir por dónde: mapas de ocupación, inflado, A*, PRM y RRT.

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""))

escribir('82514_S34_Entorno_ROS2_TF2.ipynb', C)
print('escrito S34')
