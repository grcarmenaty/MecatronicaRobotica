#!/usr/bin/env python3
"""Inserta el helper de diapositivas visuales y 13 diapositivas de media en los 3 scripts de decks."""
import re, json

HELPER = '''
// ── Diapositivas de material visual (fotos con licencia, figuras y GIFs) ──
const MEDIA = __dirname + "/media/";
function slideFotos(pres, titulo, kicker, items, credito, notas) {
  const s = contentSlide(pres, titulo, kicker);
  items.forEach(it => {
    s.addImage({ path: MEDIA + it.f, x: it.x, y: it.y, w: it.w, h: it.h, sizing: { type: "contain", w: it.w, h: it.h } });
    if (it.cap) s.addText(it.cap, { x: it.x, y: it.y + it.h + 0.03, w: it.w, h: 0.3, fontFace: "Calibri", fontSize: 10.5, color: GREY, align: "center", margin: 0 });
  });
  if (credito) footer(s, credito);
  if (notas) s.addNotes(notas);
  return s;
}
'''

def before_anchor(src, anchor, bloque):
    """Inserta bloque antes de la llave { que abre el bloque cuyo contentSlide contiene anchor."""
    i = src.find(anchor)
    assert i >= 0, f"ancla no encontrada: {anchor[:60]}"
    j = src.rfind('\n{', 0, i)
    assert j >= 0
    return src[:j] + '\n' + bloque + src[j:]

# ═══ decks.js (B1, B2) ═══
s = open('decks.js').read()
assert 'slideFotos' not in s
s = s.replace('/* ==================== DECK B1 ==================== */', HELPER + '\n/* ==================== DECK B1 ==================== */')

b1 = '''slideFotos(p1, "Tres máquinas que cuentan la historia", "S1–S3 · Imágenes", [
  { f: "fotos/b1_unimate.jpg", x: 0.7, y: 1.5, w: 6.2, h: 4.7, cap: "Unimate sirviendo café — Biltmore Hotel, 1967" },
  { f: "fotos/b1_jacquard.jpg", x: 7.15, y: 1.5, w: 5.45, h: 2.42, cap: "Telar de Jacquard: el programa en tarjetas perforadas" },
  { f: "fotos/b1_hdd.jpg", x: 7.15, y: 4.35, w: 5.45, h: 1.85, cap: "Brazo actuador de un disco duro: mecatrónica en miniatura" },
], "Fotos: F. Q. Brown/Los Angeles Times CC BY 4.0 · A. Meskens CC BY-SA 3.0 · Mk2010 CC BY 4.0 — Wikimedia Commons",
"Apoyo visual del hilo histórico de S1-S3: el telar reprogramable (1801), el Unimate en su papel más famoso (1966-67) y el HDD como ejemplo canónico de De Silva. Dejarla proyectada durante la narración histórica y volver a ella al cerrar S3.");
'''
s = before_anchor(s, 'contentSlide(p1, "De los autómatas a la fábrica"', b1)

b2 = '''slideFotos(p2, "La taxonomía, en imágenes", "S5 · Tipos de robots", [
  { f: "fotos/b2_humanoide.jpg", x: 0.7, y: 1.5, w: 5.85, h: 2.5, cap: "Humanoide (ASIMO): móvil y de servicio a la vez" },
  { f: "fotos/b2_cuadrupedo.jpg", x: 6.75, y: 1.5, w: 5.85, h: 2.5, cap: "Cuadrúpedo de inspección (Spot)" },
  { f: "fotos/b2_delta.jpg", x: 0.7, y: 4.35, w: 5.85, h: 2.5, cap: "Robot delta: cadenas cinemáticas cerradas" },
  { f: "fotos/b2_agv.jpg", x: 6.75, y: 4.35, w: 5.85, h: 2.5, cap: "AGV portacontenedores (puerto de Róterdam)" },
], "Fotos: Gnsin CC BY-SA 3.0 · ArticCynda CC BY-SA 4.0 · Trungdoanhong CC BY-SA 4.0 · CC0 — Wikimedia Commons",
"Usar en la dinámica de clasificación: proyectar cada imagen y pedir a la clase que la sitúe en ambas taxonomías antes de dar la respuesta.");
'''
s = before_anchor(s, 'contentSlide(p2, "Dos taxonomías complementarias"', b2)
open('decks.js','w').write(s)
print('decks.js: +2 diapositivas')

# ═══ decks_b3b4b5.js ═══
s = open('decks_b3b4b5.js').read()
assert 'slideFotos' not in s
s = s.replace('/* ==================== DECK B3 ==================== */', HELPER + '\n/* ==================== DECK B3 ==================== */')

b3a = '''slideFotos(p3, "El hardware, de cerca", "S9–S10 · Sensores reales", [
  { f: "fotos/b3_encoder.jpg", x: 0.7, y: 1.5, w: 5.85, h: 2.5, cap: "Encoder incremental (corte): disco y detector" },
  { f: "fotos/b3_imu.jpg", x: 6.75, y: 1.5, w: 5.85, h: 2.5, cap: "IMU MEMS sobre un centavo (DARPA TIMU)" },
  { f: "fotos/b3_galga.jpg", x: 0.7, y: 4.35, w: 5.85, h: 2.5, cap: "Galga extensométrica sin montar" },
  { f: "fotos/b3_lidar.jpg", x: 6.75, y: 4.35, w: 5.85, h: 2.5, cap: "LiDAR Velodyne sobre vehículo autónomo" },
], "Fotos: Lambtron CC BY-SA 4.0 · Univ. Michigan dominio público · Pleriche CC BY-SA 4.0 · S. Jurvetson CC BY 2.0 — Wikimedia Commons",
"Proyectar al presentar cada familia de sensor: la escala del IMU sobre el centavo es el dato que más recuerdan.");
'''
s = before_anchor(s, 'contentSlide(p3, "Posición y desplazamiento"', b3a)

b3b = '''slideFotos(p3, "Tres curvas que hay que saber leer", "S8–S11 · Figuras del bloque", [
  { f: "figs/b3_histeresis.png", x: 0.7, y: 1.5, w: 5.85, h: 2.6, cap: "Histéresis: la salida depende del camino (S8)" },
  { f: "figs/b3_cuadratura.png", x: 6.75, y: 1.5, w: 5.85, h: 2.6, cap: "Cuadratura A/B: cuenta y sentido de giro (S9)" },
  { f: "figs/b3_par_velocidad.png", x: 3.6, y: 4.42, w: 6.1, h: 2.45, cap: "Curva par-velocidad y punto de operación (S11)" },
], "Figuras propias del curso (generadas con los cuadernos de Colab)",
"Las tres curvas del bloque en una diapositiva: recuperarla en el repaso previo al cuestionario B3.");
'''
s = before_anchor(s, 'contentSlide(p3, "El motor DC y la fuerza contraelectromotriz"', b3b)

b4a = '''slideFotos(p4, "Del PUMA al laboratorio", "S13–S15 · Manipuladores reales", [
  { f: "fotos/b4_puma.jpg", x: 0.7, y: 1.5, w: 5.85, h: 5.0, cap: "Unimate PUMA 500: el arquetipo (Deutsches Museum)" },
  { f: "fotos/b4_kuka.jpg", x: 6.75, y: 1.5, w: 5.85, h: 5.0, cap: "Brazos industriales de 6 ejes: la configuración del laboratorio" },
], "Fotos: Theoprakt CC BY-SA 3.0 · Mixabest CC BY-SA 3.0 — Wikimedia Commons",
"El PUMA conecta con la historia de S3 (Unimation) y con el modelo Puma560 del taller S15; los 6R naranjas son la misma configuración que los Mitsubishi y ABB del aula-taller.");
'''
s = before_anchor(s, 'contentSlide(p4, "Rotaciones: el grupo SO(3)"', b4a)

b4b = '''slideFotos(p4, "El 2R, en movimiento", "S17–S19 · Figura y animación", [
  { f: "figs/b4_workspace_elipses.png", x: 0.7, y: 1.5, w: 5.9, h: 5.0, cap: "Espacio de trabajo y elipses de manipulabilidad en tres posturas" },
  { f: "gifs/b4_trayectoria.gif", x: 6.85, y: 1.5, w: 5.7, h: 5.0, cap: "Trayectoria quíntica en espacio articular (GIF: se anima al proyectar)" },
], "Figuras y animación propias del curso (cuadernos S17–S19)",
"El GIF se reproduce en modo presentación de PowerPoint. La elipse achatada de la postura estirada es el puente visual hacia singularidades (S18).");
'''
s = before_anchor(s, 'contentSlide(p4, "El jacobiano: la matriz que todo lo conecta"', b4b)

b5a = '''slideFotos(p5, "El actuador por dentro y las tres letras", "S20–S22 · Motor y PID", [
  { f: "fotos/b5_motor.jpg", x: 0.7, y: 1.5, w: 5.85, h: 5.0, cap: "Máquina eléctrica en corte: rotor, estátor, devanados" },
  { f: "figs/b5_p_pd_pid.png", x: 6.75, y: 1.7, w: 5.85, h: 4.5, cap: "P, PD y PID sobre la misma planta: qué aporta cada término" },
], "Foto: Technisches Museum Wien, dominio público — Wikimedia Commons · Figura propia del curso",
"La figura anticipa el taller de S22: P deja error o oscila, D amortigua, I elimina el error de régimen.");
'''
s = before_anchor(s, 'contentSlide(p5, "El motor DC con carga: de la física a la EDO"', b5a)

b5b = '''slideFotos(p5, "Subir Kp, en vivo", "S22 · Animación del taller", [
  { f: "gifs/b5_kp.gif", x: 0.9, y: 1.55, w: 7.4, h: 5.0, cap: "Barrido de Kp: la respuesta se acelera y la sobreoscilación crece (GIF)" },
], "Animación propia del curso (cuaderno S22)", null);
'''
b5b = b5b.rstrip()[:-2] + '''
'''
b5b = '''slideFotos(p5, "Subir Kp, en vivo", "S22 · Animación del taller", [
  { f: "gifs/b5_kp.gif", x: 0.8, y: 1.55, w: 7.2, h: 5.0, cap: "Barrido de Kp (GIF: se anima al proyectar)" },
], "Animación propia del curso (cuaderno S22)",
"Proyectar en bucle mientras las parejas hacen la ronda 1 del taller: es la referencia visual de lo que deben estar viendo en su pantalla.");
const _s5kp = p5; { const s = _s5kp.slides ? null : null; }
'''
# limpiar el truco anterior: version final simple
b5b = '''slideFotos(p5, "Subir Kp, en vivo", "S22 · Animación del taller", [
  { f: "gifs/b5_kp.gif", x: 0.8, y: 1.55, w: 7.2, h: 5.0, cap: "Barrido de Kp (GIF: se anima al proyectar)" },
], "Animación propia del curso (cuaderno S22)",
"Proyectar en bucle mientras las parejas hacen la ronda 1 del taller: es la referencia visual de lo que deben ver en su pantalla. A la derecha queda espacio para anotar en la pizarra las ganancias que va cantando cada pareja.");
'''
s = before_anchor(s, 'contentSlide(p5, "La ley PID y la dinámica del error"', b5b)
open('decks_b3b4b5.js','w').write(s)
print('decks_b3b4b5.js: +6 diapositivas')

# ═══ decks_b6b7b8.js ═══
s = open('decks_b6b7b8.js').read()
assert 'slideFotos' not in s
s = s.replace('/* ==================== DECK B6', HELPER + '\n/* ==================== DECK B6')

b6a = '''slideFotos(p6, "La cámara, de Mozi al modelo matricial", "S25 · Imagen", [
  { f: "figs/b6_pinhole.png", x: 0.7, y: 1.6, w: 6.6, h: 4.4, cap: "El modelo estenopeico: la profundidad se pierde en la proyección" },
  { f: "fotos/b6_camara_obscura.jpg", x: 7.5, y: 1.6, w: 5.1, h: 4.4, cap: "Dibujo técnico hecho con cámara oscura (Verbruggen, s. XVIII)" },
], "Figura propia del curso · Dibujo: dominio público / CC BY-SA 3.0 — Wikimedia Commons",
"El dibujo de Verbruggen conecta con la historia de la cámara oscura del guion (Mozi, s. V a. C.); la figura es la que se deriva en pizarra.");
'''
s = before_anchor(s, 'contentSlide(p6, "De la escena 3D a la imagen 2D"', b6a)

b6b = '''slideFotos(p6, "Estimar: la curva y la nube", "S28–S30 · Figura y animación", [
  { f: "figs/b6_kalman.png", x: 0.7, y: 1.55, w: 5.9, h: 4.6, cap: "Filtro de Kalman 1D: estimación ±2σ frente a la medida cruda (S28)" },
  { f: "gifs/b6_particulas.gif", x: 6.85, y: 1.9, w: 5.7, h: 3.8, cap: "MCL: la nube de partículas converge (GIF, cuaderno S30)" },
], "Figura y animación propias del curso (cuadernos S28 y S30)",
"El GIF reproduce la secuencia del pasillo con puertas: uniforme, multimodal tras la primera puerta, colapso con el movimiento. Es la imagen que deben recordar del bloque.");
'''
s = before_anchor(s, 'contentSlide(p6, "El filtro de Bayes: creencia recursiva"', b6b)

b7a = '''slideFotos(p7, "Las plataformas del stack", "S32–S36 · Hardware de referencia", [
  { f: "fotos/b7_turtlebot.jpg", x: 0.7, y: 1.5, w: 5.85, h: 5.0, cap: "TurtleBot3: la plataforma de referencia de ROS 2 y Nav2" },
  { f: "fotos/b7_almacen.jpg", x: 6.75, y: 1.5, w: 5.85, h: 5.0, cap: "Flota de robots de almacén (Ocado): el AMR de S6, en producción" },
], "Fotos: Kuscu0 CC BY-SA 4.0 · Techwords CC BY-SA 4.0 — Wikimedia Commons",
"El TurtleBot es el robot de los tutoriales oficiales que usa el taller S34 en simulación; la foto del almacén cierra el círculo con la distinción AGV/AMR del bloque 2.");
'''
s = before_anchor(s, 'contentSlide(p7, "De un programa único a un grafo de procesos"', b7a)

b7b = '''slideFotos(p7, "Buscar y muestrear, en imágenes", "S35 · Figura y animación", [
  { f: "figs/b7_astar_dijkstra.png", x: 0.7, y: 1.7, w: 7.3, h: 3.1, cap: "Mismo mapa, mismo camino óptimo: A* expande menos de la mitad de nodos" },
  { f: "gifs/b7_rrt.gif", x: 8.15, y: 1.55, w: 4.45, h: 4.6, cap: "RRT: las muestras tiran del árbol (GIF, cuaderno S35)" },
], "Figura y animación propias del curso (cuaderno S35)",
"La comparación de nodos expandidos es el argumento visual de la heurística admisible; el GIF de RRT acompaña la frase de Lynch y Park que cita el guion.");
'''
s = before_anchor(s, 'contentSlide(p7, "Del mapa al espacio de configuraciones"', b7b)

b8a = '''slideFotos(p8, "Manipular y decidir", "S38–S40 · Imágenes del bloque", [
  { f: "fotos/b8_mano.jpg", x: 0.7, y: 1.5, w: 5.85, h: 5.0, cap: "Banco de manipulación diestra (NIST): el problema que motiva el bloque" },
  { f: "figs/b8_gridworld.png", x: 6.75, y: 1.7, w: 5.85, h: 4.6, cap: "La política óptima del gridworld de S38: flechas que rodean el peligro" },
], "Foto: NIST, dominio público — Wikimedia Commons · Figura propia del curso (cuaderno S38)",
"La foto sirve de apertura del bloque; la política del gridworld es el resultado que los estudiantes reproducen en el cuaderno de S38.");
'''
s = before_anchor(s, 'contentSlide(p8, "El marco: decisión secuencial bajo incertidumbre"', b8a)

b8b = '''slideFotos(p8, "El valor se propaga desde la meta", "S38 · Animación", [
  { f: "gifs/b8_valor.gif", x: 0.8, y: 1.55, w: 7.2, h: 5.0, cap: "Iteración de valor, barrido a barrido (GIF: se anima al proyectar)" },
], "Animación propia del curso (cuaderno S38)",
"Proyectar tras escribir la actualizacion de Q-learning: el valor fluye hacia atrás desde la meta exactamente como el ejemplo de pizarra del guion. Detener el GIF en el barrido 3 y preguntar qué celdas saben ya algo y cuáles no.");
'''
s = before_anchor(s, 'contentSlide(p8, "Q-learning: aprender el valor de actuar"', b8b)
open('decks_b6b7b8.js','w').write(s)
print('decks_b6b7b8.js: +6 diapositivas')
print('total: 14 diapositivas nuevas (2+6+6)')
