#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parte 2: plan_curso.js y tareas.js con exámenes, pesos y cuestionarios de 15 min."""
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

# ═════════ plan_curso.js ═════════
s = carga("plan_curso.js")
s = rep(s, '''    ["B6. Percepción robótica: visión, estimación de estado y SLAM", "10 h", "6 nov – 20 nov"],
    ["B7. Software robótico: ROS 2, simulación y planificación", "8 h", "25 nov – 4 dic"],
    ["B8. Robótica basada en aprendizaje y seminario de artículos", "6 h", "9 dic – 17 dic"],
    ["Cierre: presentaciones del proyecto y repaso del examen", "2 h", "18 dic"],''',
'''    ["B6. Percepción robótica: visión, estimación de estado y SLAM", "8 h", "11 nov – 20 nov"],
    ["B7. Software robótico: ROS 2, simulación y planificación", "8 h", "25 nov – 4 dic"],
    ["B8. Robótica basada en aprendizaje (docencia)", "2 h", "9 dic – 10 dic"],
    ["EXÁMENES PARCIALES: P1 (B1–B4) y P2 (B5–B7)", "4 h", "6 nov · 11 dic"],
    ["Seminario de artículos científicos", "2 h", "16 – 17 dic"],
    ["Cierre: defensas del proyecto y repaso del examen final", "2 h", "18 dic"],''', "plan horas bloques")
s = rep(s, '''  ["S25", "vie 6 nov", "2 h", "B6", "Formación de imagen y calibración de cámara. Taller de visión clásica con OpenCV"],
  ["S26", "mié 11 nov", "1 h", "B6", "Segmentación y extracción de características clásicas"],
  ["S27", "jue 12 nov", "1 h", "B6", "Percepción con aprendizaje profundo: CNN, detección y segmentación"],''',
'''  ["S25", "vie 6 nov", "2 h", "EXAMEN", "PARCIAL 1 (bloques 1–4): test de 10 preguntas + tres problemas. 6 versiones"],
  ["S26", "mié 11 nov", "1 h", "B6", "Formación de imagen y modelo de cámara; calibración como cuaderno guiado en casa"],
  ["S27", "jue 12 nov", "1 h", "B6", "Procesado clásico y aprendido: convolución, bordes, blobs, YOLO, SAM y el criterio del ingeniero"],''', "plan cal S25-27")
s = rep(s, '''  ["S39", "jue 10 dic", "1 h", "B8", "RL profundo, simuladores (MuJoCo, Isaac) y el problema sim-to-real"],
  ["S40", "vie 11 dic", "2 h", "B8", "Aprendizaje por imitación y modelos fundacionales VLA (π0, GR00T, Gemini Robotics). Gemelos digitales"],''',
'''  ["S39", "jue 10 dic", "1 h", "B8", "RL profundo, imitación y modelos VLA (π0, GR00T); sim-to-real. Gemelos digitales como lectura"],
  ["S40", "vie 11 dic", "2 h", "EXAMEN", "PARCIAL 2 (bloques 5–7): test de 10 preguntas + tres problemas. 6 versiones"],''', "plan cal S39-40")
s = rep(s, '''children.push(h1("3. Hitos de evaluación continua"));''',
'''children.push(h1("3. Evaluación: pesos, exámenes e hitos"));
children.push(p("La nota final respeta las cuatro partidas de la guía docente oficial y queda así repartida:"));
children.push(tabla(
  ["Partida (guía docente)", "Peso", "Desglose"],
  [
    ["Exámenes", "40 %", "Parcial 1 (B1–B4, S25 · 6 nov): 15 % · Parcial 2 (B5–B7, S40 · 11 dic): 15 % · Examen final (enero, B1–B8 con énfasis en B8 e integración): 10 %. El final incluye recuperación por bloques para quien tenga un parcial por debajo de 4"],
    ["Actividades de seguimiento", "30 %", "Cuestionarios Moodle de bloque (8 × 15 min, 10 preguntas ABCD): 12 % · Entregables de clase (riesgos S7, sensores S10, PID S22, cuaderno de calibración S26→S28, ROS 2 S34): 8 % · Seminario de artículos: 10 %"],
    ["Trabajos y presentaciones", "10 %", "Proyecto integrador: entregas parciales y defensa en S43 con su rúbrica"],
    ["Trabajo experimental (laboratorio)", "20 %", "Prácticas con los robots Mitsubishi y ABB según su calendario propio (diseño intocado)"],
  ],
  [2600, 800, 5960]
));
children.push(box("Decisión que cierra la incoherencia pendiente", "El seminario de artículos queda dentro de actividades de seguimiento (10 %), y el proyecto integrador ocupa la partida de trabajos y presentaciones (10 %). Así las cuatro partidas oficiales de la guía docente se mantienen intactas (40/30/10/20) y cada actividad tiene casilla propia."));
children.push(p("Cada examen existe en seis versiones (A–F) con la misma estructura y dificultad y distinto juego de números y subconjunto de test; los enunciados, la rúbrica de corrección por apartados y las soluciones completas de cada versión están en la carpeta de exámenes (Examen_82514_… y Correccion_82514_…). Los cuestionarios Moodle se montan importando los ficheros GIFT del banco (12 preguntas por bloque; el cuestionario extrae 10 al azar)."));
children.push(h2("Hitos de evaluación continua"));''', "plan seccion evaluacion")
s = rep(s, 'children.push(bullet("cuestionarios breves al cierre de cada bloque (S4, S7, S12, S19, S24, S31, S37, S40), pensados para los últimos 10 minutos de la sesión.", "Actividades de seguimiento: "));',
        'children.push(bullet("cuestionarios Moodle de 15 minutos (10 preguntas ABCD) al cierre de cada bloque: S4, S7, S12, S19, S24, S31 y S37; el de B8 se hace en casa, en la ventana del 11 al 15 de diciembre.", "Cuestionarios: "));\nchildren.push(bullet("Parcial 1 (B1–B4) el viernes 6 de noviembre (S25) y Parcial 2 (B5–B7) el viernes 11 de diciembre (S40), ambos de 2 horas y en 6 versiones; examen final en la convocatoria de enero.", "Exámenes: "));', "plan hitos quiz")
s = rep(s, 'children.push(bullet("formación de equipos en S5; entrega 1 (modelo cinemático) tras B4; entrega 2 (control) tras B5; entrega 3 (percepción o navegación en simulación) tras B7; defensa final en S43.", "Proyecto integrador: "));',
        'children.push(bullet("formación de equipos en S5; entrega 1 (modelo cinemático) tras B4; entrega 2 (control) el miércoles 11 de noviembre (S26, movida para no chocar con el parcial 1); entrega 3 (percepción o navegación en simulación) tras B7; defensa final en S43.", "Proyecto integrador: "));', "plan hitos proyecto")
s = rep(s, 'children.push(bullet("según el peso aprobado en la guía docente; el repaso de S43 orienta sobre estructura y tipo de problemas.", "Examen final (enero): "));',
        'children.push(bullet("3 horas, bloques 1–8 con énfasis en B8 e integración; incluye la recuperación por bloques de los parciales. El repaso de S43 fija qué entra de forma literal.", "Examen final (enero): "));', "plan hitos final")
s = rep(s, '["B6. Percepción, estimación y SLAM", "S25–S31", "Apuntes_B6_Percepcion_SLAM.docx", "IQS_B6_Percepcion_SLAM.pptx"],',
        '["B6. Percepción, estimación y SLAM", "S26–S31 (parcial 1 en S25)", "Apuntes_B6_Percepcion_SLAM.docx", "IQS_B6_Percepcion_SLAM.pptx"],', "plan tabla materiales B6")
s = rep(s, '["B8. Robot learning, seminario y cierre", "S38–S43", "Apuntes_B8_Robot_Learning.docx", "IQS_B8_Robot_Learning.pptx"],',
        '["B8. Robot learning, seminario y cierre", "S38–S43 (parcial 2 en S40)", "Apuntes_B8_Robot_Learning.docx", "IQS_B8_Robot_Learning.pptx"],', "plan tabla materiales B8")
s = rep(s, 'children.push(box("Criterio de diseño", "Las sesiones de 1 h (miércoles y jueves) se reservan para teoría y resolución guiada de ejercicios; la sesión de 2 h del viernes concentra los talleres con ordenador, los casos integradores y las actividades de discusión, que necesitan continuidad."));',
        'children.push(box("Criterio de diseño", "Las sesiones de 1 h (miércoles y jueves) se reservan para teoría y resolución guiada de ejercicios; la sesión de 2 h del viernes concentra los talleres con ordenador, los casos integradores y las actividades de discusión — y aloja los dos exámenes parciales (S25 y S40), que necesitan las dos horas."));', "plan criterio")
guarda("plan_curso.js", s)

# ═════════ tareas.js ═════════
s = carga("tareas.js")
s = rep(s, "un cuestionario en los últimos diez minutos de S19", "un cuestionario en los últimos quince minutos de S19", "tareas intro")
s = rep(s, '["Cuestionarios de seguimiento", "8, uno por bloque", "Últimos 10 min de S4, S7, S12, S19, S24, S31, S37 y S40", "Corrección automática en el campus; revisión en clase de los dos errores más frecuentes"],',
        '["Cuestionarios de seguimiento", "8, uno por bloque (Moodle, 15 min, 10 preguntas ABCD)", "Últimos 15 min de S4, S7, S12, S19, S24, S31 y S37; el B8 en casa (11–15 dic)", "Corrección automática en Moodle; revisión en clase de los dos errores más frecuentes"],', "tareas fila quiz")
s = rep(s, '["Examen final", "1", "Convocatoria de enero", "Profesor; el repaso de S43 fija qué entra literalmente"],',
        '["Exámenes", "2 parciales + final (6 versiones cada uno)", "P1 (B1–B4): S25, 6 nov · P2 (B5–B7): S40, 11 dic · Final: enero", "Profesor, con las rúbricas de los documentos de corrección; soluciones publicadas tras cada examen"],', "tareas fila examen")
s = rep(s, '["Talleres con entregable", "9 sesiones", "S7, S10, S13, S15, S16, S19, S22, S25, S28, S34", "Se recoge en el aula o se sube al campus el mismo día; corrección en común"],',
        '["Talleres con entregable", "9 sesiones", "S7, S10, S13, S15, S16, S19, S22, S28, S34 · el de calibración pasa a cuaderno en casa (S26→S28)", "Se recoge en el aula o se sube al campus el mismo día; corrección en común"],', "tareas fila talleres")
s = rep(s, '["S24", "jue 5 nov", "ENTREGA 2 del proyecto: control", "Cuestionario B5"],',
        '''["S24", "jue 5 nov", "Preparar el parcial 1 (formulario A4 manuscrito)", "Cuestionario B5 · último día lectivo antes del parcial"],
  ["S25", "vie 6 nov", "—", "EXAMEN PARCIAL 1 (bloques 1–4) · 2 h · 6 versiones"],
  ["S26", "mié 11 nov", "ENTREGA 2 del proyecto: control (movida por el parcial) · empezar el cuaderno de calibración", "Encargo del cuaderno de calibración (entrega antes de S28)"],''', "tareas cal S24-26")
s = rep(s, '["S40", "vie 11 dic", "Preparar la presentación del seminario", "Cuestionario B8"],',
        '''["S40", "vie 11 dic", "Preparar la presentación del seminario · cuestionario B8 en Moodle (hasta el 15 dic)", "EXAMEN PARCIAL 2 (bloques 5–7) · 2 h · 6 versiones"],''', "tareas cal S40")
s = rep(s, "C.push(p(\"Formato común: de ocho a diez preguntas cortas de respuesta cerrada, en los últimos diez minutos de la última sesión del bloque, a través del campus con corrección automática.",
        "C.push(p(\"Formato común: 15 minutos y 10 preguntas ABCD extraídas al azar del banco de 12 del bloque (ficheros GIFT importables en Moodle; cada error resta un tercio), en los últimos quince minutos de la última sesión del bloque — salvo el B8, que se abre en Moodle del 11 al 15 de diciembre por coincidir su sesión de cierre con el parcial 2.", "tareas seccion 4 quiz")
s = rep(s, '["B8", "S40 · vie 11 dic", "Elementos del MDP y retorno descontado; términos de la actualización de Q-learning; idea del recorte de PPO; aleatorización de dominio; qué es un modelo VLA"],',
        '["B8", "Moodle, en casa · 11–15 dic", "Elementos del MDP y retorno descontado; términos de la actualización de Q-learning; idea del recorte de PPO; aleatorización de dominio; qué es un modelo VLA; gemelo digital (lectura guiada)"],', "tareas quiz B8")
# nueva sección de exámenes al final de la sección 4
s = rep(s, '''// ---------- 5 ----------
C.push(h1("5. Talleres con entregable"));''',
'''// ---------- 4bis ----------
C.push(h1("4 bis. Los exámenes: dos parciales y un final, en seis versiones"));
C.push(p("Parcial 1 (S25, viernes 6 de noviembre, 2 h): bloques 1–4. Parte A, test de 10 preguntas ABCD (2,0 pt, extraídas de los bancos de B1–B4); parte B, Nyquist/aliasing y MDQ (2,0 pt); parte C, cinemática directa del 2R con tabla DH y espacio de trabajo (3,0 pt); parte D, cinemática inversa, jacobiano y estática (3,0 pt). Parcial 2 (S40, viernes 11 de diciembre, 2 h): bloques 5–7. Parte A, test (2,0 pt); parte B, diseño PD con gravedad y paso al PID con windup (3,0 pt); parte C, un paso completo de filtro de Kalman 1D (2,5 pt); parte D, A* sobre rejilla y diagnóstico de QoS (2,5 pt). Examen final (enero, 3 h): bloques 1–8; test de 12 preguntas (2,4 pt), caso de seguridad ISO (1,6 pt), cinemática y control (3,0 pt), Bayes discreto (1,5 pt) y Q-learning con actualización numérica (1,5 pt); incluye la recuperación por bloques de los parciales."));
C.push(p("Cada examen existe en seis versiones (A–F) con idéntica estructura y dificultad: cambian los parámetros numéricos y el subconjunto de test, y las soluciones de cada versión están calculadas y publicadas en los documentos de corrección (Correccion_82514_Parcial1, _Parcial2 y _Final), que incluyen además la rúbrica de corrección por apartados con los errores frecuentes y su descuento. Regla de reparto: versiones en damero para que dos vecinos nunca compartan números."));
C.push(box("Pesos", "Parcial 1: 15 % · Parcial 2: 15 % · Final: 10 % (partida de exámenes, 40 % de la guía docente). Los parciales no liberan materia del final, pero quien tenga los dos parciales aprobados afronta un final centrado en B8 e integración; quien tenga un parcial por debajo de 4 recupera ese bloque de materia dentro del final."));

// ---------- 5 ----------
C.push(h1("5. Talleres con entregable"));''', "tareas seccion examenes")
guarda("tareas.js", s)

if fallos:
    print("FALLOS:")
    for x in fallos: print(" -", x)
    sys.exit(1)
print("parte 2 (plan + tareas) completada")
