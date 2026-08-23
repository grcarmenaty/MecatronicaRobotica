#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Replanificación con exámenes: parcial 1 en S25, parcial 2 en S40, B6→8h, B8→2h+seminario,
cuestionarios Moodle de 15 min. Actualiza decks, apuntes B6/B8, plan y tareas."""
import sys

fallos = []
def carga(f): return open(f, encoding="utf-8").read()
def guarda(f, s): open(f, "w", encoding="utf-8").write(s)
def rep(src, viejo, nuevo, ctx, n=1):
    c = src.count(viejo)
    if c != n:
        fallos.append(f"{ctx}: esperaba {n}, hay {c}: {viejo[:80]!r}")
        return src
    return src.replace(viejo, nuevo)

# ═════════════ decks.js (B1, B2) ═════════════
s = carga("decks.js")
s = rep(s, "35-50 lanzamiento del seminario; 50-60 cuestionario B1.",
        "35-45 lanzamiento del seminario; 45-60 cuestionario B1 en Moodle (15 min).", "B1 S4 seg")
s = rep(s, "Cerrar la sesión con el cuestionario de seguimiento del bloque 1 (8-10 preguntas, Moodle/Kahoot, 10 min). Cuenta para evaluación continua.",
        "Cerrar la sesión con el cuestionario de seguimiento del bloque 1 en Moodle: 15 minutos, 10 preguntas ABCD del banco del bloque. Cuenta para evaluación continua.", "B1 nota seminario")
s = rep(s, "80-110 taller de análisis de riesgos; 110-120 cuestionario B2 y cierre de equipos.",
        "80-105 taller de análisis de riesgos; 105-120 cuestionario B2 en Moodle (15 min) y cierre de equipos.", "B2 S7 seg")
s = rep(s, "Corrección en común como síntesis del bloque. Después: cuestionario B2 y cierre de equipos del proyecto.",
        "Corrección en común como síntesis del bloque. Después: cuestionario B2 en Moodle (15 min) y cierre de equipos del proyecto.", "B2 taller card")
guarda("decks.js", s)

# ═════════════ decks_b3b4b5.js (B3, B4, B5) ═════════════
s = carga("decks_b3b4b5.js")
s = rep(s, "40-50 ejercicio guiado de selección motor-reductora en la pizarra; 50-60 cuestionario B3 (10 min) y cierre del bloque",
        "40-45 ejercicio guiado de selección motor-reductora en la pizarra; 45-60 cuestionario B3 en Moodle (15 min) y cierre del bloque", "B3 S12 seg")
s = rep(s, "Cuestionario B3 (10 min): características, cuadratura, bias de IMU, factor de galga, LiDAR, back-EMF, inercia reflejada.",
        "Cuestionario B3 (15 min, Moodle): características, cuadratura, bias de IMU, factor de galga, LiDAR, back-EMF, inercia reflejada.", "B3 card quiz")
s = rep(s, "Últimos 10 minutos: cuestionario B3.", "Últimos 15 minutos: cuestionario B3 en Moodle.", "B3 nota reductora", 0) if False else s
s = rep(s, "Ejercicio guiado con números en la pizarra; comentar los márgenes de catálogo (par RMS < nominal, pico < máximo, factor de servicio). Cerrar el bloque enlazando con B4.",
        "Ejercicio guiado con números en la pizarra; comentar los márgenes de catálogo (par RMS < nominal, pico < máximo, factor de servicio). Cuestionario B3 en Moodle en los últimos 15 minutos; cerrar el bloque enlazando con B4.", "B3 nota reductora")
s = rep(s, "95-110 repaso del bloque con el mapa en pizarra y las cinco ecuaciones; 110-120 cuestionario B4.",
        "95-105 repaso del bloque con el mapa en pizarra y las cinco ecuaciones; 105-120 cuestionario B4 en Moodle (15 min).", "B4 S19 seg")
s = rep(s, "Cuestionario B4 (10 min, 8-10 preguntas): bloqueo de cardán",
        "Cuestionario B4 (15 min, 10 preguntas ABCD): bloqueo de cardán", "B4 card quiz")
s = rep(s, "40-50 síntesis del bloque con el arco S20-S24; 50-60 cuestionario B5.",
        "40-45 síntesis del bloque con el arco S20-S24; 45-60 cuestionario B5 en Moodle (15 min).", "B5 S24 seg")
s = rep(s, 'title: "Cuestionario B5 (10 min, 8-10 preguntas)"', 'title: "Cuestionario B5 (15 min, 10 preguntas ABCD)"', "B5 card quiz")
s = rep(s, "Mensaje de apertura: hasta ahora el robot era geometría (B4); a partir de hoy es física — fuerzas, pares, corrientes — y el control convierte esa física en el movimiento que queremos. Cuestionario B5 en los últimos 10 minutos de S24.",
        "Mensaje de apertura: hasta ahora el robot era geometría (B4); a partir de hoy es física — fuerzas, pares, corrientes — y el control convierte esa física en el movimiento que queremos. Cuestionario B5 en los últimos 15 minutos de S24; el viernes siguiente a este bloque (6 nov) es el parcial 1 de B1-B4.", "B5 hoja nota")
guarda("decks_b3b4b5.js", s)

# ═════════════ decks_b6b7b8.js (B6, B7, B8) ═════════════
s = carga("decks_b6b7b8.js")

# — B6 hoja de ruta —
s = rep(s, '''    ["S25 · vie 6 nov · 2 h", "Formación de imagen, modelo de cámara y calibración"],
    ["S26 · mié 11 nov · 1 h", "Procesado clásico: convolución, bordes, regiones, puntos"],
    ["S27 · jue 12 nov · 1 h", "Percepción con aprendizaje profundo: detección y segmentación"],''',
'''    ["S25 · vie 6 nov · 2 h", "EXAMEN PARCIAL 1 (bloques 1-4): test y problemas"],
    ["S26 · mié 11 nov · 1 h", "Formación de imagen y modelo de cámara · calibración en cuaderno guiado"],
    ["S27 · jue 12 nov · 1 h", "Procesado clásico y aprendido: el criterio del ingeniero"],''', "B6 hoja rows")
s = rep(s, 'El bloque recorre la mitad «percibir» de la tríada percibir-planificar-actuar. Las dos horas de los viernes concentran los talleres (OpenCV, filtros) y los desarrollos largos; los días de una hora son teoría densa. Cuestionario de seguimiento al cierre de S31.',
        'El bloque recorre la mitad «percibir» de la tríada. El viernes 6 de noviembre (S25) es el examen parcial 1 de B1-B4, así que la docencia del bloque empieza el miércoles 11: el bloque se compacta a 8 horas — la calibración pasa a cuaderno guiado en casa y el procesado clásico y el aprendido comparten sesión. Cuestionario B6 en Moodle al cierre de S31.', "B6 hoja nota")

# — B6: S25 → parcial + info + nueva S26 —
VIEJO_S25 = '''sectionSlide(p6, "S25", "Formación de imagen y calibración", "Cámara estenopeica · proyección perspectiva · intrínsecos y extrínsecos · calibración",
  "0-10 repaso B5 y apertura del bloque; 10-35 cámara estenopeica y proyección perspectiva; 35-60 modelo matricial (intrínsecos, extrínsecos, distorsión); 60-70 descanso; 70-100 taller de calibración con OpenCV y tablero de ajedrez; 100-120 discusión de resultados y errores de reproyección.", { f: "fotos/b6_estereo3.jpg", cap: "Cámara estéreo: recuperar la profundidad perdida", credito: "Foto: T. Cognard CC BY-SA 3.0 — Wikimedia Commons" });'''
NUEVO_S25 = '''sectionSlide(p6, "S25", "Examen parcial 1", "Bloques 1-4 · test y tres problemas · 2 horas",
  "Reservar aula de examen. Llevar impresas las 6 versiones (A-F) y repartirlas en damero. 0-5 acomodo, identificación e instrucciones; 5-115 examen; 115-120 recogida y recuento. Corrección con la rúbrica publicada; soluciones en el campus en una semana.");

{
  const s = contentSlide(p6, "Parcial 1: estructura y reglas", "S25 · Examen");
  const partes = [
    ["A", "Test (2,0 pt)", "10 preguntas ABCD sobre B1-B4; cada error resta un tercio; en blanco no puntúa"],
    ["B", "Diseño mecatrónico e instrumentación (2,0 pt)", "Nyquist y aliasing con cálculo · MDQ: cálculo e interpretación"],
    ["C", "Cinemática directa (3,0 pt)", "FK del 2R con números · tabla DH · espacio de trabajo alcanzable"],
    ["D", "IK, jacobiano y estática (3,0 pt)", "Las dos ramas de la IK · det J y singularidades · pares con τ = Jᵀ·F"],
  ];
  partes.forEach((c, i) => card(s, 0.7, 1.7 + i * 1.16, 11.9, 1.0, { title: c[1], body: c[2], num: c[0], bodySize: 12, titleSize: 13.5 }));
  card(s, 0.7, 6.42, 11.9, 0.62, { title: "", body: "Material: calculadora no programable y una hoja A4 de formulario manuscrito por las dos caras. Seis versiones (A-F) en damero. Los errores de arrastre no se penalizan dos veces.", fill: "E3F7EC", bodySize: 11.5 });
  s.addNotes("Proyectar esta diapositiva la semana anterior (al cerrar B5) y dejarla publicada en el campus. El día del examen: recordar las reglas del test (el error resta un tercio, en blanco no puntúa), que el planteamiento vale el 40 por ciento de cada apartado y que un resultado sin desarrollo no puntúa. Las seis versiones comparten estructura y dificultad: decirlo para desactivar la percepción de agravio.");
  footer(s, "Parcial 1 · viernes 6 de noviembre · 2 h");
}

sectionSlide(p6, "S26", "Formación de imagen y calibración exprés", "Cámara estenopeica · proyección · intrínsecos y extrínsecos · calibración como cuaderno guiado",
  "0-5 devolución exprés del parcial y apertura del bloque; 5-20 cámara estenopeica y proyección perspectiva; 20-40 modelo matricial: intrínsecos, extrínsecos y distorsión; 40-50 calibración: método de Zhang, criterio del error de reproyección y encargo del cuaderno guiado (entrega antes de S28); 50-60 cierre: la cámara es un sensor de rayos, no de distancias.", { f: "fotos/b6_estereo3.jpg", cap: "Cámara estéreo: recuperar la profundidad perdida", credito: "Foto: T. Cognard CC BY-SA 3.0 — Wikimedia Commons" });'''
s = rep(s, VIEJO_S25, NUEVO_S25, "B6 S25→parcial+S26")

# — B6 kickers de las diapositivas que pasan a S26 —
s = rep(s, '"La cámara, de Mozi al modelo matricial", "S25 · Imagen"', '"La cámara, de Mozi al modelo matricial", "S26 · Imagen"', "kicker mozi")
s = rep(s, '"De la escena 3D a la imagen 2D", "S25 · Proyección"', '"De la escena 3D a la imagen 2D", "S26 · Proyección"', "kicker proyeccion")
s = rep(s, '"Modelo matricial y calibración", "S25 · Parámetros"', '"Modelo matricial y calibración", "S26 · Parámetros"', "kicker matricial")
s = rep(s, '''  card(s, 6.85, 4.27, 5.75, 2.35, {
    title: "Taller de calibración (30 min)",
    body: "Tablero de ajedrez, 15-20 vistas variadas, findChessboardCorners y calibrateCamera en OpenCV.\\n\\nCriterio de calidad: error de reproyección por debajo de un píxel. Discutir por qué empeora si todas las vistas son frontales.",
    bodySize: 12.5,
  });''', '''  card(s, 6.85, 4.27, 5.75, 2.35, {
    title: "Calibración: cuaderno guiado en casa",
    body: "Tablero de ajedrez, 15-20 vistas variadas, findChessboardCorners y calibrateCamera en OpenCV.\\n\\nEntrega en el campus antes de S28; criterio de calidad: error de reproyección por debajo de un píxel. Los resultados se comentan al abrir S28.",
    bodySize: 12.5,
  });''', "card calibracion")
s = rep(s, "Recoger los ficheros de calibración: se reutilizan en el proyecto.",
        "La calibración se hace en el cuaderno guiado en casa (entrega antes de S28); los ficheros se reutilizan en el proyecto.", "nota matricial")

# — B6: antigua S26 → S27 fusionada; borrar antigua portadilla S27 —
s = rep(s, '''sectionSlide(p6, "S26", "Procesado clásico de imagen", "Convolución · bordes · regiones · características de punto",
  "0-5 recuperación de S25; 5-20 convolución y filtrado espacial; 20-35 detección de bordes (gradiente, Canny); 35-48 segmentación por regiones y características de punto; 48-60 demostración en vivo con OpenCV y cierre.");''',
'''sectionSlide(p6, "S27", "Procesado clásico y aprendido", "Convolución y bordes · regiones y puntos · rasgos aprendidos · el criterio del ingeniero",
  "0-5 recuperación de S26 y demo del umbral que se rompe al cambiar la luz; 5-25 caja clásica en galería: convolución, Canny, blobs y puntos de interés; 25-40 de rasgos diseñados a aprendidos: YOLO, segmentación y SAM; 40-52 discusión con la tabla de criterio sobre tres casos; 52-60 síntesis y anuncio del giro probabilístico de S28.");''', "B6 S26→S27")
s = rep(s, '''sectionSlide(p6, "S27", "Percepción con aprendizaje profundo", "Rasgos aprendidos · detección · segmentación · criterio de elección",
  "0-5 recuperación; 5-20 de rasgos diseñados a aprendidos; 20-35 detección de objetos (YOLO y familia); 35-48 segmentación semántica, de instancias y fundacional (SAM); 48-60 cuándo clásico y cuándo aprendido, con casos.");
''', "", "B6 borrar S27 vieja")
s = rep(s, '"Cuatro herramientas clásicas que siguen vigentes", "S26 · Procesado"', '"Cuatro herramientas clásicas que siguen vigentes", "S27 · Procesado"', "kicker herramientas")

# — B6 S31 cuestionario 15 min —
s = rep(s, "95-115 FastSLAM, mapas de ocupación y panorama de SLAM visual y neuronal; 115-120 cuestionario de seguimiento B6.",
        "95-105 FastSLAM, mapas de ocupación y panorama de SLAM visual y neuronal; 105-120 cuestionario B6 en Moodle (15 min).", "B6 S31 seg")
s = rep(s, "Reservar los últimos 10 minutos para el cuestionario B6.", "Reservar los últimos 15 minutos para el cuestionario B6 en Moodle.", "B6 nota quiz")

# — B7 cuestionario 15 min —
s = rep(s, "90-115 integración del stack completo y síntesis del bloque; 115-120 cuestionario B7.",
        "90-105 integración del stack completo y síntesis del bloque; 105-120 cuestionario B7 en Moodle (15 min).", "B7 S37 seg")
s = rep(s, "Reservar 5 minutos para el cuestionario B7.", "Reservar los últimos 15 minutos para el cuestionario B7 en Moodle.", "B7 nota quiz")

# — B8 hoja de ruta —
s = rep(s, '''    ["S39 · jue 10 dic · 1 h", "RL profundo, simuladores y el problema sim-to-real"],
    ["S40 · vie 11 dic · 2 h", "Imitación, diffusion policies, modelos VLA y gemelos digitales"],''',
'''    ["S39 · jue 10 dic · 1 h", "RL profundo, imitación y modelos VLA · sim-to-real"],
    ["S40 · vie 11 dic · 2 h", "EXAMEN PARCIAL 2 (bloques 5-7)"],''', "B8 hoja rows")
s = rep(s, "El bloque nuevo de la asignatura. Enfoque introductorio y conceptual: no se exige derivar algoritmos de RL, sí entender qué problema resuelven, cuándo se usan y qué los limita. El seminario cierra el semestre y es el mecanismo que mantendrá vivo este bloque cada curso.",
        "El bloque nuevo de la asignatura, compactado a dos sesiones de docencia porque el viernes 11 es el parcial 2 (B5-B7). Enfoque conceptual: entender qué problema resuelve cada método y qué lo limita; los gemelos digitales quedan como lectura guiada. El cuestionario B8 se hace en Moodle, en casa, del 11 al 15 de diciembre. El seminario cierra el semestre.", "B8 hoja nota")

# — B8: S39 retitulada y fusionada —
s = rep(s, '''sectionSlide(p8, "S39", "RL profundo y sim-to-real", "Políticas parametrizadas · PPO · simuladores · brecha de realidad",
  "0-5 recuperación de S38; 5-20 de la tabla a la política parametrizada; 20-38 PPO y por qué se impuso en robótica; 38-55 simuladores y el problema sim-to-real con la aleatorización de dominio; 55-60 cierre y preparación de S40.");''',
'''sectionSlide(p8, "S39", "RL profundo, imitación y VLA", "PPO y sim-to-real · behavior cloning y diffusion policies · modelos fundacionales",
  "0-5 recuperación de S38; 5-15 políticas parametrizadas y PPO (solo las ideas); 15-25 simuladores y aleatorización de dominio; 25-40 imitación: behavior cloning, errores compuestos y diffusion policies; 40-52 modelos VLA: RT-2, OpenVLA, π0 y GR00T; 52-60 cierre — gemelos digitales como lectura guiada, logística del seminario y del parcial 2, y cuestionario B8 en Moodle (11-15 dic).");''', "B8 S39 retitulada")

# — B8: kickers de las diapositivas que pasan a S39 —
s = rep(s, '"Aprender de demostraciones", "S40 · Imitación"', '"Aprender de demostraciones", "S39 · Imitación"', "kicker imitacion")
s = rep(s, '"Modelos visión-lenguaje-acción", "S40 · Modelos fundacionales"', '"Modelos visión-lenguaje-acción", "S39 · Modelos fundacionales"', "kicker vla")
s = rep(s, '"Gemelos digitales y síntesis del bloque", "S40 · Cierre"', '"Gemelos digitales y síntesis del bloque", "S39 · Cierre y lectura"', "kicker gemelos")
s = rep(s, "Esta es la diapositiva de cierre conceptual de la asignatura completa. Dedicarle tiempo: es la respuesta a la pregunta que muchos traen desde septiembre, «¿para qué estudio cinemática si ya existe la IA?». Después, cuestionario B8.",
        "Esta es la diapositiva de cierre conceptual de la asignatura completa. Dedicarle tiempo: es la respuesta a la pregunta que muchos traen desde septiembre, «¿para qué estudio cinemática si ya existe la IA?». El cuestionario B8 se hace en Moodle, en casa, en la ventana del 11 al 15 de diciembre; recordarlo aquí.", "B8 nota gemelos")

# — B8: quitar portadilla S40 de su sitio e insertar parcial 2 tras la diapositiva de gemelos —
s = rep(s, '''sectionSlide(p8, "S40", "Imitación, VLA y gemelos digitales", "Behavior cloning · diffusion policies · modelos fundacionales · gemelos digitales",
  "0-10 recuperación; 10-35 aprendizaje por imitación y behavior cloning con sus fallos; 35-55 diffusion policies; 55-65 descanso; 65-95 modelos VLA: RT-2, OpenVLA, π0, GR00T N1, Gemini Robotics; 95-110 gemelos digitales en fabricación; 110-120 síntesis del bloque y cuestionario B8.");
''', "", "B8 borrar S40 vieja")
ANCLA_S41 = 'sectionSlide(p8, "S41 · S42", "Seminario de artículos científicos"'
BLOQUE_S40 = '''sectionSlide(p8, "S40", "Examen parcial 2", "Bloques 5-7 · test y tres problemas · 2 horas",
  "Reservar aula de examen. Seis versiones (A-F) en damero. 0-5 acomodo e instrucciones; 5-115 examen; 115-120 recogida. La rúbrica y las soluciones se publican tras la corrección; el cuestionario B8 sigue abierto en Moodle hasta el 15 de diciembre.");

{
  const s = contentSlide(p8, "Parcial 2: estructura y reglas", "S40 · Examen");
  const partes = [
    ["A", "Test (2,0 pt)", "10 preguntas ABCD sobre B5-B7; cada error resta un tercio; en blanco no puntúa"],
    ["B", "Control de una articulación (3,0 pt)", "Diseño PD para ζ y ωn · sobreoscilación · error estacionario con gravedad · windup"],
    ["C", "Estimación (2,5 pt)", "Un paso completo de filtro de Kalman 1D · lectura de la ganancia · EKF frente a MCL"],
    ["D", "Planificación y ROS 2 (2,5 pt)", "A* sobre rejilla con heurística Manhattan · admisibilidad · diagnóstico de QoS"],
  ];
  partes.forEach((c, i) => card(s, 0.7, 1.7 + i * 1.16, 11.9, 1.0, { title: c[1], body: c[2], num: c[0], bodySize: 12, titleSize: 13.5 }));
  card(s, 0.7, 6.42, 11.9, 0.62, { title: "", body: "Material: calculadora no programable y una hoja A4 de formulario manuscrito por las dos caras. El planteamiento vale el 40 % de cada apartado; un resultado sin desarrollo no puntúa.", fill: "E3F7EC", bodySize: 11.5 });
  s.addNotes("Proyectar al cerrar S39 y publicar en el campus. Recordar que B8 entra solo en el cuestionario de Moodle y en el examen final de enero, no en este parcial. Insistir en el formulario manuscrito: prepararlo es la mejor sesión de repaso que existe.");
  footer(s, "Parcial 2 · viernes 11 de diciembre · 2 h");
}

''' + ANCLA_S41
s = rep(s, ANCLA_S41, BLOQUE_S40, "B8 insertar parcial 2")
guarda("decks_b6b7b8.js", s)

# ═════════════ apuntes_b6.js ═════════════
s = carga("apuntes_b6.js")
s = rep(s, "Apuntes del profesor con citas de fuente · Sesiones S25–S31 (6, 11, 12, 13, 18, 19 y 20 de noviembre de 2026) · 10 horas",
        "Apuntes del profesor con citas de fuente · Examen parcial 1 en S25 (6 nov) · Docencia S26–S31 (11, 12, 13, 18, 19 y 20 de noviembre de 2026) · 8 horas", "B6 portada")
VIEJO_H1_S25 = 'children.push(h1("Sesión S25 (vie 6 nov, 2 h) — Formación de imagen y calibración"));'
NUEVO_S25_APUNTES = '''children.push(h1("Sesión S25 (vie 6 nov, 2 h) — Examen parcial 1 (bloques 1–4)"));
children.push(h2("Guion de la sesión"));
children.push(seg("0–5 min", "Acomodo e instrucciones"));
children.push(punto("Repartir las seis versiones (A–F) en damero; recordar las reglas: test con penalización de un tercio por error, planteamiento al 40 % en los problemas, material limitado a calculadora no programable y una hoja A4 de formulario manuscrito."));
children.push(seg("5–115 min", "Examen"));
children.push(punto("Estructura: A test de 10 preguntas ABCD (2,0 pt) · B diseño mecatrónico e instrumentación (2,0 pt) · C cinemática directa del 2R (3,0 pt) · D cinemática inversa, jacobiano y estática (3,0 pt)."));
children.push(seg("115–120 min", "Recogida"));
children.push(punto("Recontar entregas contra la lista; publicar soluciones y rúbrica en el campus en el plazo de una semana; los dos fallos más frecuentes se comentan al abrir S26."));
children.push(box("Logística del parcial", "Los enunciados (6 versiones), la rúbrica de corrección y las soluciones completas de cada versión están en la carpeta de exámenes del curso (Examen_82514_Parcial1_vA–vF y Correccion_82514_Parcial1). Las seis versiones comparten estructura y dificultad: cambian los números y el subconjunto de test."));

children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("Sesión S26 (mié 11 nov, 1 h) — Formación de imagen y modelo de cámara"));
children.push(box("Reorganización del bloque", "Con el parcial 1 ocupando la S25, este bloque se compacta de 10 a 8 horas: la teoría de imagen y cámara se condensa en esta sesión de 1 h, el taller de calibración pasa al cuaderno guiado 82514_S25 como trabajo en casa (entrega en el campus antes de S28), y el procesado clásico y el aprendido comparten la S27. Los apartados conservan su numeración original (25.x, 26.x, 27.x)."));'''
s = rep(s, VIEJO_H1_S25, NUEVO_S25_APUNTES, "B6 S25 apuntes")
# guion nuevo de S26 (sustituye el guion de 2 h)
VIEJO_GUION_S25 = '''children.push(h2("Guion de la clase"));
children.push(seg("0–10 min", "Apertura del bloque"));'''
NUEVO_GUION_S26 = '''children.push(h2("Guion de la clase"));
children.push(seg("0–5 min", "Devolución exprés del parcial y apertura del bloque"));
children.push(punto("Comentar los dos fallos más frecuentes del parcial 1 (sin resolverlo entero: las soluciones están publicadas) y presentar el arco del bloque: percibir en tres pasos — imagen (S26), interpretación (S27), incertidumbre (S28-S31)."));
children.push(punto("Motivar con el proyecto integrador: sin percepción, el robot móvil del bloque 7 no puede ni localizarse ni evitar obstáculos; todo lo de este bloque se usa en Nav2."));'''
s = rep(s, VIEJO_GUION_S25, NUEVO_GUION_S26, "B6 guion S26 apertura")
s = rep(s, '''children.push(seg("10–35 min", "Teoría: cámara estenopeica y proyección perspectiva (apdo. 25.1)"));''',
        '''children.push(seg("5–20 min", "Teoría: cámara estenopeica y proyección perspectiva (apdo. 25.1)"));''', "B6 seg 25.1")
s = rep(s, '''children.push(seg("35–60 min", "Teoría: modelo matricial y parámetros de la cámara (apdo. 25.2)"));''',
        '''children.push(seg("20–40 min", "Teoría: modelo matricial y parámetros de la cámara (apdo. 25.2)"));''', "B6 seg 25.2")
s = rep(s, '''children.push(seg("60–70 min", "Descanso"));
children.push(punto("—"));
children.push(seg("70–90 min", "Teoría: calibración de cámara (apdo. 25.3)"));''',
        '''children.push(seg("40–50 min", "Teoría: calibración de cámara (apdo. 25.3)"));''', "B6 seg 25.3")
s = rep(s, '''children.push(seg("90–115 min", "Taller OpenCV básico"));
children.push(punto("Cuaderno guiado: cargar imagen, explorar el array de píxeles, convertir a gris, findChessboardCorners + calibrateCamera sobre un juego de imágenes de damero, y undistort para corregir la distorsión (guion propio del curso; sin cita de libro)."));
children.push(punto("Comprobación numérica: comparar la f en píxeles estimada con la esperada a partir de la óptica y el tamaño de píxel del sensor; discutir el error de reproyección como métrica de calidad."));
children.push(punto("Los grupos que acaben antes: proyectar un cubo virtual sobre el damero con projectPoints — es la matriz C funcionando al revés."));
children.push(seg("115–120 min", "Cierre"));''',
        '''children.push(seg("50–60 min", "Encargo del cuaderno de calibración y cierre"));
children.push(punto("Encargar el cuaderno guiado 82514_S25 como trabajo en casa con entrega antes de S28: cargar imagen, convertir a gris, findChessboardCorners + calibrateCamera sobre el juego de imágenes de damero, y undistort; comprobación numérica de la focal en píxeles y error de reproyección como métrica de calidad (guion propio del curso; sin cita de libro)."));
children.push(punto("Ampliación voluntaria del cuaderno: proyectar un cubo virtual sobre el damero con projectPoints — es la matriz C funcionando al revés."));''', "B6 taller→cuaderno")
s = rep(s, "children.push(punto(\"Encargar para S26 la lectura ligera de Corke (2023), cap. 11, pp. 440-452 (operaciones espaciales y bordes).\"));",
        "children.push(punto(\"Encargar para S27 la lectura ligera de Corke (2023), cap. 11, pp. 440-452 (operaciones espaciales y bordes).\"));", "B6 encargo lectura")
# antigua S26 → S27 fusionada
s = rep(s, 'children.push(h1("Sesión S26 (mié 11 nov, 1 h) — Procesado clásico de imagen"));',
        'children.push(h1("Sesión S27 (jue 12 nov, 1 h) — Procesado clásico y aprendido: el criterio del ingeniero"));', "B6 h1 S26→S27")
s = rep(s, '''children.push(seg("0–5 min", "Recuperación de S25"));
children.push(punto("Dos preguntas a mano alzada: ¿cuántos parámetros describen una cámara y cómo se reparten (Corke, 2023, p. 548)? ¿Qué información pierde la proyección perspectiva?"));
children.push(seg("5–20 min", "Teoría: convolución y filtrado espacial (apdo. 26.1)"));''',
        '''children.push(seg("0–5 min", "Recuperación de S26 y plan de la sesión fusionada"));
children.push(punto("Dos preguntas a mano alzada: ¿cuántos parámetros describen una cámara y cómo se reparten (Corke, 2023, p. 548)? ¿Qué información pierde la proyección perspectiva? Anunciar el plan: primera media hora, la caja clásica en galería; segunda, los rasgos aprendidos y el criterio de elección."));
children.push(seg("5–25 min", "Teoría: la caja clásica en galería — convolución, bordes, regiones y puntos (apdos. 26.1–26.4)"));''', "B6 guion S27 arranque")
s = rep(s, '''children.push(seg("20–35 min", "Teoría: detección de bordes (apdo. 26.2)"));''', "", "B6 seg 26.2 fuera")
s = rep(s, '''children.push(seg("35–50 min", "Teoría: regiones y puntos de interés (apdos. 26.3 y 26.4)"));''', "", "B6 seg 26.3 fuera")
s = rep(s, '''children.push(seg("50–60 min", "Demo y cierre"));
children.push(punto("Demo en vivo (5 min): cadena umbral → blobs → centroides sobre piezas del laboratorio en OpenCV; cambiar la iluminación en directo para que se rompa — motiva la S27."));
children.push(punto("Cierre: anunciar que la S27 responde a la pregunta que deja la demo: ¿y si la apariencia no se deja describir con umbrales y núcleos a mano?"));''',
        '''children.push(seg("25–40 min", "Teoría: de rasgos diseñados a aprendidos — YOLO, segmentación y SAM (apdos. 27.1–27.3)"));
children.push(punto("Demo del gancho (3 min): cadena umbral → blobs sobre piezas del laboratorio; cambiar la iluminación en directo para que se rompa, y leer la sentencia de Corke: las técnicas clásicas «han sido eclipsadas por las basadas en aprendizaje profundo» (Corke, 2023, p. 510)."));
children.push(punto("CNN en una idea: convoluciones aprendidas apiladas; la primera capa aprende núcleos como los de la fig. 11.15 (Corke, 2023, p. 444). Hitos mínimos: LeNet, AlexNet 2012, ResNet (He et al., 2015, arXiv:1512.03385)."));
children.push(punto("Detección en una pasada: YOLO «enmarca la detección como un problema de regresión» (Redmon et al., 2016, arXiv:1506.02640); segmentación semántica y de instancias (Mask R-CNN; He et al., 2017, arXiv:1703.06870); modelos fundacionales: SAM segmenta sin reentrenar (Kirillov et al., 2023, arXiv:2304.02643)."));
children.push(seg("40–52 min", "Discusión: cuándo clásico y cuándo aprendido (apdo. 27.4)"));
children.push(punto("Tabla de decisión sobre tres casos: inspección dimensional de pieza torneada, recogida de objetos variados en logística, detección de personas en célula colaborativa."));
children.push(punto("Regla que debe quedar: la geometría calibrada de S26 no se «aprende» — incluso el sistema más neuronal necesita su matriz K; el clásico gana con iluminación controlada, tolerancias métricas y pocos datos (posición del curso; sin cita de libro)."));
children.push(seg("52–60 min", "Síntesis y cierre"));
children.push(punto("Síntesis en una frase: clásico para medir, aprendido para reconocer — y ambos sobre la misma geometría calibrada. Anunciar el giro del bloque: S28 abandona la imagen y ataca la incertidumbre; pedir repaso de gaussianas multivariantes (media, covarianza)."));''', "B6 guion S27 resto")
# borrar la antigua cabecera+guion de S27 (el material teórico 27.x queda como referencia)
s = rep(s, '''children.push(h1("Sesión S27 (jue 12 nov, 1 h) — Percepción con aprendizaje profundo"));

children.push(h2("Guion de la clase"));
children.push(seg("0–5 min", "Gancho"));
children.push(punto("Recuperar la demo rota de S26 (el umbral que muere al cambiar la luz) y leer la sentencia de Corke: las técnicas clásicas «han sido eclipsadas por las basadas en aprendizaje profundo» (Corke, 2023, p. 510)."));
children.push(seg("5–20 min", "Teoría: redes convolucionales (apdo. 27.1)"));''',
        '''children.push(h2("Material de la segunda parte de S27: percepción con aprendizaje profundo (apdos. 27.1–27.4)"));
children.push(seg("Referencia", "Redes convolucionales (apdo. 27.1)"));''', "B6 borrar h1 S27 vieja")
s = rep(s, '''children.push(seg("20–35 min", "Teoría: detección de objetos, YOLO (apdo. 27.2)"));''',
        '''children.push(seg("Referencia", "Detección de objetos, YOLO (apdo. 27.2)"));''', "B6 seg 27.2")
s = rep(s, '''children.push(seg("35–45 min", "Teoría: segmentación (apdo. 27.3)"));''',
        '''children.push(seg("Referencia", "Segmentación (apdo. 27.3)"));''', "B6 seg 27.3")
s = rep(s, '''children.push(seg("45–55 min", "Discusión: cuándo clásico y cuándo aprendido (apdo. 27.4)"));''',
        '''children.push(seg("Referencia", "Cuándo clásico y cuándo aprendido (apdo. 27.4)"));''', "B6 seg 27.4")
s = rep(s, '''children.push(seg("55–60 min", "Cierre"));
children.push(punto("Anunciar el giro del bloque: S28 abandona la imagen y ataca la incertidumbre; pedir repaso de gaussianas multivariantes (media, covarianza) y de álgebra de matrices."));''',
        "", "B6 cierre S27 viejo fuera")
s = rep(s, "la calibración de S25 y una hipótesis de plano", "la calibración de S26 y una hipótesis de plano", "B6 calib S25→S26 (x2)", 2)
s = rep(s, "la geometría calibrada de S25 no se «aprende»", "la geometría calibrada de S26 no se «aprende»", "B6 geom calib", 1)
s = rep(s, "combinado con la calibración de S26 y una hipótesis de plano de trabajo conocido", "combinado con la calibración de S26 y una hipótesis de plano de trabajo conocido", "noop", 1) if False else s
guarda("apuntes_b6.js", s)

# ═════════════ apuntes_b8.js ═════════════
s = carga("apuntes_b8.js")
s = rep(s, "Apuntes del profesor con citas de fuente · Sesiones S38–S42 (9, 10, 11, 16 y 17 de diciembre de 2026) · 6 horas",
        "Apuntes del profesor con citas de fuente · Docencia S38–S39 · Examen parcial 2 en S40 · Seminario S41–S42 y defensas S43 (9–18 de diciembre de 2026)", "B8 portada")
s = rep(s, 'children.push(h1("Sesión S39 (jue 10 dic, 1 h) — RL profundo, simuladores y sim-to-real"));',
        'children.push(h1("Sesión S39 (jue 10 dic, 1 h) — RL profundo, imitación y modelos VLA"));', "B8 h1 S39")
s = rep(s, '''children.push(seg("5–20 min", "Teoría: del Q tabular a los gradientes de política (apdo. 39.1)"));''',
        '''children.push(seg("5–15 min", "Teoría: del Q tabular a las políticas parametrizadas y PPO (apdos. 39.1–39.2)"));''', "B8 seg 39.1")
s = rep(s, '''children.push(seg("20–35 min", "Teoría: PPO, el caballo de batalla (apdo. 39.2)"));''', "", "B8 seg 39.2 fuera")
s = rep(s, '''children.push(seg("35–50 min", "Teoría: simuladores y sim-to-real (apdo. 39.3)"));''',
        '''children.push(seg("15–25 min", "Teoría: simuladores y sim-to-real (apdo. 39.3)"));''', "B8 seg 39.3")
s = rep(s, '''children.push(seg("50–60 min", "Discusión y cierre"));
children.push(punto("Debate breve por parejas: ¿qué parámetros aleatorizaríais para transferir una política de empuje de cajas con el ABB del laboratorio? Recoger 3–4 respuestas (fricción caja-mesa, masa de la caja, latencia de red, posición inicial, iluminación si hay cámara)."));
children.push(punto("Anticipar S40: hasta aquí el robot aprende solo con recompensa; mañana veremos que muchas veces es más barato enseñarle con demostraciones — imitación y modelos fundacionales."));
children.push(punto("Recordatorio logístico del seminario: quien aún no tenga las diapositivas validadas, tutoría virtual el viernes por la tarde."));''',
        '''children.push(seg("25–40 min", "Teoría: imitación — behavior cloning, errores compuestos y diffusion policies (apdos. 40.1–40.2)"));
children.push(punto("Behavior cloning: supervisado sobre pares (observación, acción) teleoperados; su fallo característico: el desplazamiento covariante y los errores compuestos, con DAgger como remedio clásico (Ross, Gordon y Bagnell, 2011, AISTATS) y el action chunking de ALOHA/ACT como mitigación práctica (Zhao et al., 2023, arXiv:2304.13705)."));
children.push(punto("Multimodalidad con el ejemplo del obstáculo: la regresión a la media atraviesa el obstáculo; la diffusion policy genera la distribución de secuencias de acciones por des-ruido condicionado (Chi et al., 2023, arXiv:2303.04137)."));
children.push(punto("La división del trabajo actual en una frase: el refuerzo domina donde la recompensa es fácil de escribir (locomoción) y la imitación donde la tarea es fácil de demostrar (manipulación)."));
children.push(seg("40–52 min", "Teoría: modelos fundacionales VLA (apdo. 40.3)"));
children.push(punto("Genealogía mínima en pizarra: RT-2 (Brohan et al., 2023, arXiv:2307.15818) → OpenVLA (Kim et al., 2024, arXiv:2406.09246) → π0 con flow matching (Black et al., 2024, arXiv:2410.24164) → GR00T N1 con arquitectura de dos sistemas (NVIDIA, 2025, arXiv:2503.14734) → Gemini Robotics (Google DeepMind, 2025, informe técnico)."));
children.push(punto("Los tres ingredientes comunes: preentrenamiento visión-lenguaje a escala de internet, datos robóticos multi-plataforma y una cabeza de acción; y las limitaciones que debe conocer un ingeniero: fiabilidad, latencia, evaluación no estandarizada, dependencia de los datos."));
children.push(punto("Síntesis del curso (apdo. 40.5): el VLA decide y emite consignas a 3–50 Hz; B4 las traduce, B5 las ejecuta a kilohercios, B6 alimenta al modelo, B7 lo comunica y la seguridad de B2 no se aprende: se garantiza por diseño."));
children.push(seg("52–60 min", "Cierre y logística"));
children.push(punto("Gemelos digitales como lectura guiada (apdo. 40.4, con la ISO 23247): entra en el cuestionario B8 y en el examen final de enero, no en el parcial 2."));
children.push(punto("Logística: cuestionario B8 en Moodle, en casa, del 11 al 15 de diciembre; parcial 2 (B5-B7) mañana viernes; orden definitivo de las presentaciones del seminario publicado hoy; tutoría virtual para diapositivas pendientes."));''', "B8 guion S39 fusionado")
s = rep(s, '''children.push(h1("Sesión S40 (vie 11 dic, 2 h) — Imitación, modelos VLA y gemelos digitales"));

children.push(h2("Guion de la clase"));
children.push(seg("0–10 min", "Recuperación y mapa de la sesión"));
children.push(punto("Preguntas orales de repaso: ¿qué optimiza PPO y para qué sirve el recorte? ¿Qué es domain randomization y qué problema ataca?"));
children.push(punto("Plantear la limitación del RL puro: diseñar recompensas para tareas de manipulación cotidianas (doblar una camiseta) es endiabladamente difícil; a menudo es más fácil demostrar la tarea que especificarla — hoja de ruta: imitación → diffusion policies → VLA → gemelos digitales → síntesis del curso."));''',
        '''children.push(h1("Sesión S40 (vie 11 dic, 2 h) — Examen parcial 2 (bloques 5–7)"));

children.push(h2("Guion de la sesión"));
children.push(seg("0–5 min", "Acomodo e instrucciones"));
children.push(punto("Repartir las seis versiones (A–F) en damero; recordar las reglas: test con penalización de un tercio por error, planteamiento al 40 % en los problemas, calculadora no programable y una hoja A4 de formulario manuscrito."));
children.push(seg("5–115 min", "Examen"));
children.push(punto("Estructura: A test de 10 preguntas ABCD (2,0 pt) · B control de una articulación (3,0 pt) · C un paso completo de filtro de Kalman 1D (2,5 pt) · D planificación con A* y diagnóstico de QoS (2,5 pt). El bloque 8 no entra: se evalúa en el cuestionario de Moodle y en el final de enero."));
children.push(seg("115–120 min", "Recogida"));
children.push(punto("Recontar entregas; publicar soluciones y rúbrica (Correccion_82514_Parcial2) tras la corrección; recordar que el cuestionario B8 sigue abierto en Moodle hasta el 15 de diciembre."));
children.push(box("Material de referencia de la segunda parte de S39", "Los apartados 40.1–40.5 que siguen (imitación, diffusion policies, VLA, gemelos digitales y síntesis del curso) son el material condensado en la S39 y la lectura guiada del bloque; conservan su numeración original."));''', "B8 S40 examen")
s = rep(s, '''children.push(seg("10–35 min", "Teoría: behavior cloning y sus límites (apdo. 40.1)"));''',
        '''children.push(seg("Referencia", "Behavior cloning y sus límites (apdo. 40.1)"));''', "B8 seg 40.1")
s = rep(s, '''children.push(seg("35–55 min", "Teoría: diffusion policies (apdo. 40.2)"));''',
        '''children.push(seg("Referencia", "Diffusion policies (apdo. 40.2)"));''', "B8 seg 40.2")
s = rep(s, '''children.push(seg("55–65 min", "Descanso"));
children.push(punto("—"));
children.push(seg("65–90 min", "Teoría: modelos fundacionales VLA (apdo. 40.3)"));''',
        '''children.push(seg("Referencia", "Modelos fundacionales VLA (apdo. 40.3)"));''', "B8 seg 40.3")
s = rep(s, '''children.push(seg("90–105 min", "Teoría: gemelos digitales y síntesis del curso (apdos. 40.4 y 40.5)"));''',
        '''children.push(seg("Referencia", "Gemelos digitales y síntesis del curso (apdos. 40.4 y 40.5) — lectura guiada"));''', "B8 seg 40.4")
s = rep(s, '''children.push(seg("105–120 min", "Cuestionario de seguimiento B8 y cierre"));
children.push(punto("Cuestionario tipo test (8–10 preguntas, Moodle): elementos del MDP y retorno descontado, actualización de Q-learning (identificar términos), idea del recorte de PPO, domain randomization, BC frente a diffusion policy, ingredientes de un VLA, gemelo digital."));
children.push(punto("Logística del seminario: publicar el orden definitivo de las 6 presentaciones (3 el miércoles 16, 3 el jueves 17), recordar reglas de tiempo (10 + 5) y que la asistencia y las preguntas del público puntúan en participación."));''',
        '''children.push(seg("Referencia", "Cuestionario B8 (en Moodle, en casa, 11–15 dic)"));
children.push(punto("Cuestionario tipo test (10 preguntas ABCD, 15 min, Moodle): elementos del MDP y retorno descontado, actualización de Q-learning (identificar términos), idea del recorte de PPO, domain randomization, BC frente a diffusion policy, ingredientes de un VLA, gemelo digital."));''', "B8 quiz S40")
s = rep(s, "recordar qué entra del bloque 8 en la evaluación (cuestionario ya hecho en S40;",
        "recordar qué entra del bloque 8 en la evaluación (cuestionario B8 hecho en Moodle en la ventana del 11 al 15 de diciembre;", "B8 S42 cierre")
guarda("apuntes_b8.js", s)

if fallos:
    print("FALLOS:")
    for x in fallos: print(" -", x)
    sys.exit(1)
print("parte 1 (decks + apuntes B6/B8) completada")
