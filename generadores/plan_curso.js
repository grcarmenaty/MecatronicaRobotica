const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, PageBreak, AlignmentType, ImageRun } = require("docx");
const { IQS, F, p, pRuns, h1, h2, bullet, box, tabla, numberingConfig } = require("./lib_iqs");

const children = [];
const LOGO_IQS = fs.readFileSync("media/logo_iqs_color.png");
const logoPortada = new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 600, after: 200 }, children: [new ImageRun({ type: "png", data: LOGO_IQS, transformation: { width: 200, height: 153 } })] });

// Portada
children.push(
 logoPortada,
 new Paragraph({ spacing: { before: 400, after: 200 }, alignment: AlignmentType.CENTER,
 children: [new TextRun({ text: "82514, Mecatrónica y Robótica", size: 52, bold: true, color: IQS.navy, font: F })] }),
 new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 },
 children: [new TextRun({ text: "Plan del curso 2026/27 · Calendario y programación de sesiones", size: 30, color: IQS.navy2, font: F })] }),
 new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
 children: [new TextRun({ text: "IQS, Universitat Ramon Llull · 6 ECTS · Primer semestre", size: 22, color: IQS.grey, font: F })] }),
 new Paragraph({ alignment: AlignmentType.CENTER,
 children: [new TextRun({ text: "Horario: miércoles 1 h · jueves 1 h · viernes 2 h", size: 22, color: IQS.grey, font: F })] }),
 new Paragraph({ children: [new PageBreak()] })
);

children.push(h1("1. Estructura general del semestre"));
children.push(p("El periodo lectivo va del lunes 7 de septiembre al martes 22 de diciembre de 2026. Con clases los miércoles (1 h), jueves (1 h) y viernes (2 h), el semestre ofrece 43 sesiones y 57 horas lectivas una vez descontados los festivos de Barcelona que caen en día de clase: el viernes 11 de septiembre (Diada Nacional de Catalunya) y el jueves 24 de septiembre (La Mercè). El lunes 12 de octubre y el martes 8 de diciembre también son festivos, pero no afectan al horario de la asignatura."));
children.push(box("Criterio de diseño", "Las sesiones de 1 h (miércoles y jueves) se reservan para teoría y resolución guiada de ejercicios; la sesión de 2 h del viernes concentra los talleres con ordenador, los casos integradores y las actividades de discusión, y aloja los dos exámenes parciales (S25 y S40), que necesitan las dos horas."));

children.push(h2("Distribución de horas por bloque"));
children.push(tabla(
 ["Bloque", "Horas", "Semanas (aprox.)"],
 [
 ["B1. Introducción a la mecatrónica y panorama 2026 de la robótica", "4 h", "9 sep – 17 sep"],
 ["B2. Tipología de robots, cobots y humanoides. Seguridad y normativa", "5 h", "18 sep – 25 sep"],
 ["B3. Sensores y actuadores", "6 h", "30 sep – 8 oct"],
 ["B4. Cinemática y estática de robots", "10 h", "9 oct – 23 oct"],
 ["B5. Modelado y control de sistemas mecatrónicos en Python", "6 h", "28 oct – 5 nov"],
 ["B6. Percepción robótica: visión, estimación de estado y SLAM", "8 h", "11 nov – 20 nov"],
 ["B7. Software robótico: ROS 2, simulación y planificación", "8 h", "25 nov – 4 dic"],
 ["B8. Robótica basada en aprendizaje (docencia)", "2 h", "9 dic – 10 dic"],
 ["EXÁMENES PARCIALES: P1 (B1–B4) y P2 (B5–B7)", "4 h", "6 nov · 11 dic"],
 ["Seminario de artículos científicos", "2 h", "16 – 17 dic"],
 ["Cierre: defensas del proyecto y repaso del examen final", "2 h", "18 dic"],
 ],
 [5700, 1100, 2560]
));

children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("2. Calendario sesión a sesión"));
children.push(p("La numeración de sesiones (S1–S43) se usa también en los documentos de apuntes de cada bloque, donde encontrarás la estructura interna de cada clase minuto a minuto y la teoría correspondiente."));

const cal = [
 ["S1", "mié 9 sep", "1 h", "B1", "Presentación de la asignatura. Qué es la mecatrónica: definición, dominios y componentes"],
 ["S2", "jue 10 sep", "1 h", "B1", "El proceso de diseño mecatrónico: diseño acoplado, MDQ, evolución de diseño"],
 ["-", "vie 11 sep", "-", "-", "FESTIVO, Diada Nacional de Catalunya"],
 ["S3", "mié 16 sep", "1 h", "B1", "Historia de la robótica y definición de robot: sentir, planificar, actuar"],
 ["S4", "jue 17 sep", "1 h", "B1", "Panorama 2026: Physical AI, humanoides, mercado. Lanzamiento del seminario de artículos"],
 ["S5", "vie 18 sep", "2 h", "B2", "Taxonomía de robots. Configuraciones de manipuladores y espacios de trabajo. Grados de autonomía"],
 ["S6", "mié 23 sep", "1 h", "B2", "Robots móviles: locomoción con ruedas y patas, AGV frente a AMR, drones"],
 ["-", "jue 24 sep", "-", "-", "FESTIVO, La Mercè"],
 ["S7", "vie 25 sep", "2 h", "B2", "Robots colaborativos y seguridad: ISO 10218:2025, métodos colaborativos, análisis de riesgos"],
 ["S8", "mié 30 sep", "1 h", "B3", "Arquitectura de instrumentación. Características estáticas y dinámicas de los sensores"],
 ["S9", "jue 1 oct", "1 h", "B3", "Sensores de posición, velocidad e inercia: encoders, resolvers, IMU"],
 ["S10", "vie 2 oct", "2 h", "B3", "Sensores de fuerza y táctiles. Sensores de rango: LiDAR y cámaras de profundidad. Ejercicios"],
 ["S11", "mié 7 oct", "1 h", "B3", "Actuadores eléctricos: DC, BLDC, paso a paso, servoaccionamientos"],
 ["S12", "jue 8 oct", "1 h", "B3", "Actuadores hidráulicos y neumáticos. Transmisiones y selección motor-reductora"],
 ["S13", "vie 9 oct", "2 h", "B4", "Posición y orientación: rotaciones, transformaciones homogéneas. Taller con spatialmath (Python)"],
 ["S14", "mié 14 oct", "1 h", "B4", "Cinemática directa: convención de Denavit-Hartenberg"],
 ["S15", "jue 15 oct", "1 h", "B4", "Taller: cinemática directa con la Robotics Toolbox for Python"],
 ["S16", "vie 16 oct", "2 h", "B4", "Cinemática inversa: soluciones analíticas y numéricas. Taller"],
 ["S17", "mié 21 oct", "1 h", "B4", "Jacobiano y cinemática diferencial"],
 ["S18", "jue 22 oct", "1 h", "B4", "Singularidades y manipulabilidad"],
 ["S19", "vie 23 oct", "2 h", "B4", "Estática y fuerzas. Generación de trayectorias articulares y cartesianas. Repaso del bloque"],
 ["S20", "mié 28 oct", "1 h", "B5", "Modelado de sistemas electromecánicos: EDO y función de transferencia"],
 ["S21", "jue 29 oct", "1 h", "B5", "Respuesta temporal y frecuencial con python-control"],
 ["S22", "vie 30 oct", "2 h", "B5", "Taller: control PID de una articulación; sintonía y simulación"],
 ["S23", "mié 4 nov", "1 h", "B5", "Representación en espacio de estados"],
 ["S24", "jue 5 nov", "1 h", "B5", "Dinámica de manipuladores: Euler-Lagrange y control por par calculado"],
 ["S25", "vie 6 nov", "2 h", "EXAMEN", "PARCIAL 1 (bloques 1–4): test de 10 preguntas + tres problemas. 6 versiones"],
 ["S26", "mié 11 nov", "1 h", "B6", "Formación de imagen y modelo de cámara; calibración como cuaderno guiado en casa"],
 ["S27", "jue 12 nov", "1 h", "B6", "Procesado clásico y aprendido: convolución, bordes, blobs, YOLO, SAM y el criterio del ingeniero"],
 ["S28", "vie 13 nov", "2 h", "B6", "Probabilidad para robótica: filtro de Bayes y filtro de Kalman. Taller"],
 ["S29", "mié 18 nov", "1 h", "B6", "Localización con EKF"],
 ["S30", "jue 19 nov", "1 h", "B6", "Filtro de partículas y localización de Montecarlo"],
 ["S31", "vie 20 nov", "2 h", "B6", "SLAM: EKF-SLAM, grafos de factores, SLAM visual y panorama actual (NeRF, 3DGS)"],
 ["S32", "mié 25 nov", "1 h", "B7", "Arquitectura de ROS 2: nodos, topics, DDS"],
 ["S33", "jue 26 nov", "1 h", "B7", "Servicios, acciones, parámetros y launch files"],
 ["S34", "vie 27 nov", "2 h", "B7", "Taller ROS 2: paquete en Python, simulación con Gazebo, TF2"],
 ["S35", "mié 2 dic", "1 h", "B7", "Planificación de trayectorias: mapas de coste, A*, RRT"],
 ["S36", "jue 3 dic", "1 h", "B7", "Navegación autónoma con Nav2"],
 ["S37", "vie 4 dic", "2 h", "B7", "Manipulación con MoveIt 2. Integración del stack completo"],
 ["S38", "mié 9 dic", "1 h", "B8", "Aprendizaje por refuerzo: MDP, recompensas, Q-learning"],
 ["S39", "jue 10 dic", "1 h", "B8", "RL profundo, imitación y modelos VLA (π0, GR00T); sim-to-real. Gemelos digitales como lectura"],
 ["S40", "vie 11 dic", "2 h", "EXAMEN", "PARCIAL 2 (bloques 5–7): test de 10 preguntas + tres problemas. 6 versiones"],
 ["S41", "mié 16 dic", "1 h", "B8", "Seminario de artículos científicos I"],
 ["S42", "jue 17 dic", "1 h", "B8", "Seminario de artículos científicos II"],
 ["S43", "vie 18 dic", "2 h", "Cierre", "Presentaciones finales del proyecto integrador. Repaso orientado al examen de enero"],
];
children.push(tabla(["Sesión", "Fecha", "Dur.", "Bloque", "Contenido"], cal, [800, 1250, 700, 900, 5710]));

children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("3. Evaluación: pesos, exámenes e hitos"));
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
children.push(h2("Hitos de evaluación continua"));
children.push(bullet("asignación de artículos en S4 (17 sep); presentaciones en S41–S42 (16–17 dic).", "Seminario de artículos: "));
children.push(bullet("formación de equipos en S5; entrega 1 (modelo cinemático) tras B4; entrega 2 (control) el miércoles 11 de noviembre (S26, movida para no chocar con el parcial 1); entrega 3 (percepción o navegación en simulación) tras B7; defensa final en S43.", "Proyecto integrador: "));
children.push(bullet("cuestionarios Moodle de 15 minutos (10 preguntas ABCD) al cierre de cada bloque: S4, S7, S12, S19, S24, S31 y S37; el de B8 se hace en casa, en la ventana del 11 al 15 de diciembre.", "Cuestionarios: "));
children.push(bullet("Parcial 1 (B1–B4) el viernes 6 de noviembre (S25) y Parcial 2 (B5–B7) el viernes 11 de diciembre (S40), ambos de 2 horas y en 6 versiones; examen final en la convocatoria de enero.", "Exámenes: "));
children.push(bullet("3 horas, bloques 1–8 con énfasis en B8 e integración; incluye la recuperación por bloques de los parciales. El repaso de S43 fija qué entra de forma literal.", "Examen final (enero): "));

children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("4. Materiales del curso"));
children.push(p("Cada bloque tiene dos ficheros: un documento de apuntes del profesor, con el guion de cada sesión segmento a segmento y la teoría extensa, donde cada afirmación relevante lleva su cita con página verificada sobre las ediciones de la carpeta de bibliografía, y una presentación de aula en estilo IQS con notas del orador en cada diapositiva."));
children.push(tabla(
 ["Bloque", "Sesiones", "Apuntes del profesor", "Presentación"],
 [
 ["B1. Introducción a la mecatrónica", "S1–S4", "Apuntes_B1_Introduccion_Mecatronica.docx", "IQS_B1_Introduccion.pptx"],
 ["B2. Tipología, cobots y seguridad", "S5–S7", "Apuntes_B2_Tipologia_Seguridad.docx", "IQS_B2_Tipologia_Seguridad.pptx"],
 ["B3. Sensores y actuadores", "S8–S12", "Apuntes_B3_Sensores_Actuadores.docx", "IQS_B3_Sensores_Actuadores.pptx"],
 ["B4. Cinemática y estática", "S13–S19", "Apuntes_B4_Cinematica_Estatica.docx", "IQS_B4_Cinematica_Estatica.pptx"],
 ["B5. Modelado y control en Python", "S20–S24", "Apuntes_B5_Modelado_Control.docx", "IQS_B5_Modelado_Control.pptx"],
 ["B6. Percepción, estimación y SLAM", "S26–S31 (parcial 1 en S25)", "Apuntes_B6_Percepcion_SLAM.docx", "IQS_B6_Percepcion_SLAM.pptx"],
 ["B7. ROS 2, simulación y planificación", "S32–S37", "Apuntes_B7_ROS2_Planificacion.docx", "IQS_B7_ROS2_Planificacion.pptx"],
 ["B8. Robot learning, seminario y cierre", "S38–S43 (parcial 2 en S40)", "Apuntes_B8_Robot_Learning.docx", "IQS_B8_Robot_Learning.pptx"],
 ],
 [2150, 1080, 3400, 2730]
));
children.push(box("Ediciones de referencia para las citas", "De Silva, C. W. et al. (2016), Mechatronics: Fundamentals and Applications, CRC Press · Corke, P. (2023), Robotics, Vision and Control: Fundamental Algorithms in Python, 3.ª ed., Springer · Lynch, K. M. y Park, F. C. (2017), Modern Robotics, Cambridge University Press · Thrun, S., Burgard, W. y Fox, D. (2005), Probabilistic Robotics, MIT Press · Fraden, J. (2016), Handbook of Modern Sensors, 5.ª ed., Springer. Las normas (ISO 10218:2025, ISO/TS 15066:2016, ISO 12100:2010), la documentación de ROS 2, Nav2 y MoveIt 2, y los artículos de arXiv se citan por designación o identificador, sin página."));

const doc = new Document({
 numbering: numberingConfig,
 styles: { default: { document: { run: { font: F, size: 22 } } } },
 sections: [{ properties: { page: { margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } }, children }],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync("Plan_Curso_82514_2026-27.docx", buf); console.log("OK plan"); });
