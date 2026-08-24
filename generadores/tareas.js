const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, PageBreak, AlignmentType, ImageRun } = require("docx");
const { IQS, F, p, pRuns, h1, h2, h3, bullet, box, tabla, numberingConfig } = require("./lib_iqs");

const C = [];
const LOGO_IQS = fs.readFileSync("media/logo_iqs_color.png");
const logoPortada = new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 600, after: 200 }, children: [new ImageRun({ type: "png", data: LOGO_IQS, transformation: { width: 200, height: 153 } })] });

// ---------- Portada ----------
C.push(logoPortada);
C.push(
 new Paragraph({ spacing: { before: 400, after: 200 }, alignment: AlignmentType.CENTER,
 children: [new TextRun({ text: "82514, Mecatrónica y Robótica", size: 44, bold: true, color: IQS.navy, font: F })] }),
 new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 },
 children: [new TextRun({ text: "Tareas, pruebas y entregables del semestre", size: 32, color: IQS.navy2, font: F })] }),
 new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
 children: [new TextRun({ text: "Todo lo que hay que encargar, recoger, corregir y publicar, sesión a sesión", size: 22, color: IQS.grey, font: F })] }),
 new Paragraph({ alignment: AlignmentType.CENTER,
 children: [new TextRun({ text: "Curso 2026/27 · IQS Universitat Ramon Llull", size: 20, color: IQS.grey, font: F })] }),
 new Paragraph({ children: [new PageBreak()] })
);

// ---------- 1 ----------
C.push(h1("1. Para qué sirve este documento"));
C.push(p("Los ocho documentos de apuntes contienen, dentro del guion de cada sesión, todo lo que hay que hacer en clase. El problema es que las tareas están repartidas: un encargo de lectura al final de S13, un entregable ligero en mitad de S28, un cuestionario en los últimos quince minutos de S19. Preparar la semana obliga a rastrearlos. Este documento los reúne todos en un único sitio, ordenados por fecha, para que puedas responder de un vistazo a tres preguntas: qué tengo que llevar preparado a la próxima clase, qué recojo, y qué queda pendiente de corregir."));
C.push(p("Está pensado para imprimirse y anotarse encima. El apartado 3 es el calendario maestro y probablemente el único que consultarás cada semana; el resto desarrolla cada familia de tareas con su contenido, su rúbrica y su lógica de evaluación."));
C.push(box("Aviso sobre los pesos", "La guía docente oficial reparte la nota en examen final 40%, actividades de seguimiento 30%, trabajos y presentaciones 10% y trabajo experimental 20%. La propuesta de modernización planteaba bajar el examen a 30% y crear un 20% de proyecto integrador absorbiendo el 10% de trabajos y presentaciones. Este documento usa la propuesta, pero deja marcada en el apartado 9 la incoherencia que hay que resolver antes de septiembre: si el 10% de trabajos y presentaciones desaparece, el seminario de artículos necesita un sitio explícito en la tabla de pesos."));

// ---------- 2 ----------
C.push(h1("2. Las siete familias de tarea, de un vistazo"));
C.push(tabla(
 ["Familia", "Cuántas", "Cuándo", "Quién la corrige y cómo"],
 [
 ["Cuestionarios de seguimiento", "8, uno por bloque (Moodle, 15 min, 10 preguntas ABCD)", "Últimos 15 min de S4, S7, S12, S19, S24, S31 y S37; el B8 en casa (11–15 dic)", "Corrección automática en Moodle; revisión en clase de los dos errores más frecuentes"],
 ["Talleres con entregable", "9 sesiones", "S7, S10, S13, S15, S16, S19, S22, S28, S34 · el de calibración pasa a cuaderno en casa (S26→S28)", "Se recoge en el aula o se sube al campus el mismo día; corrección en común"],
 ["Ejercicios de los cuadernos", "87 (3 por cuaderno × 29)", "Durante o después de cada sesión con cuaderno", "Autocorrección: cada cuaderno lleva sus soluciones al final"],
 ["Entregas del proyecto", "3 parciales + defensa", "Tras B4, B5 y B7; defensa en S43", "Profesor, con la rúbrica del apartado 6"],
 ["Seminario de artículos", "1 por pareja", "Validación antes del 30 sep; presentación en S41–S42", "Profesor, con la rúbrica del apartado 7"],
 ["Deberes previos y lecturas", "16 encargos", "Repartidos; ver calendario", "No se corrigen: se comprueban con la pregunta de recuperación del inicio de la sesión siguiente"],
 ["Exámenes", "2 parciales + final (6 versiones cada uno)", "P1 (B1–B4): S25, 6 nov · P2 (B5–B7): S40, 11 dic · Final: enero", "Profesor, con las rúbricas de los documentos de corrección; soluciones publicadas tras cada examen"],
 ],
 [2450, 1250, 2600, 3060]
));

// ---------- 3 ----------
C.push(new Paragraph({ children: [new PageBreak()] }));
C.push(h1("3. Calendario maestro"));
C.push(p("Una fila por sesión. La columna «se encarga» es lo que los estudiantes tienen que traer o hacer para la sesión siguiente; la columna «se recoge o evalúa» es lo que sale de esa clase con nota o con registro. Las sesiones sin nada en ninguna de las dos columnas son de teoría pura y no generan trabajo administrativo."));

const cal = [
 ["S1", "mié 9 sep", "Leer De Silva cap. 1, pp. 1-10", "-"],
 ["S2", "jue 10 sep", "Leer Corke cap. 1, pp. 1-9", "-"],
 ["S3", "mié 16 sep", "Traer un ejemplo de robot de prensa reciente", "-"],
 ["S4", "jue 17 sep", "Elegir artículo del seminario (validación antes del 30 sep)", "Cuestionario B1 · lanzamiento del seminario"],
 ["S5", "vie 18 sep", "Leer Corke cap. 4, pp. 139-146", "Fichas de clasificación en equipo · equipos de proyecto formados"],
 ["S6", "mié 23 sep", "Opcional: Corke cap. 4, pp. 147-155", "-"],
 ["S7", "vie 25 sep", "-", "Tabla de riesgos de 6 filas (equipo) · Cuestionario B2 · equipos cerrados"],
 ["S8", "mié 30 sep", "Repasar Fraden cap. 3, pp. 62-103", "-"],
 ["S9", "jue 1 oct", "Leer preguntas de selección de acelerómetro (Fraden p. 332)", "-"],
 ["S10", "vie 2 oct", "-", "Ejercicio de selección de sensores (puesta en común)"],
 ["S11", "mié 7 oct", "Calcular la inercia reflejada del ejemplo del campus", "-"],
 ["S12", "jue 8 oct", "-", "Ejercicio de selección motor-reductora · Cuestionario B3"],
 ["S13", "vie 9 oct", "Leer Corke cap. 7, pp. 255-260", "Taller de pose con spatialmath"],
 ["S14", "mié 14 oct", "-", "-"],
 ["S15", "jue 15 oct", "-", "Taller de cinemática directa 6R · comparación con el ABB real"],
 ["S16", "vie 16 oct", "Leer Corke cap. 8, pp. 310-315", "Taller de cinemática inversa"],
 ["S17", "mié 21 oct", "-", "-"],
 ["S18", "jue 22 oct", "-", "-"],
 ["S19", "vie 23 oct", "ENTREGA 1 del proyecto: modelo cinemático", "Taller de estática y trayectorias · Cuestionario B4"],
 ["S20", "mié 28 oct", "Instalar python-control · leer De Silva pp. 88-93", "-"],
 ["S21", "jue 29 oct", "Traer portátil con python-control · releer De Silva pp. 93-95", "-"],
 ["S22", "vie 30 oct", "-", "Taller de PID: tabla de ganancias y métricas por pareja"],
 ["S23", "mié 4 nov", "Leer Lynch y Park pp. 271-275", "-"],
 ["S24", "jue 5 nov", "Preparar el parcial 1 (formulario A4 manuscrito) · leer Corke cap. 11, pp. 440-452 para S26", "Cuestionario B5 · último día lectivo antes del parcial"],
 ["S25", "vie 6 nov", "-", "EXAMEN PARCIAL 1 (bloques 1–4) · 2 h · 6 versiones"],
 ["S26", "mié 11 nov", "ENTREGA 2 del proyecto: control (movida por el parcial) · empezar el cuaderno de calibración", "Encargo del cuaderno de calibración (entrega antes de S28)"],
 ["S27", "jue 12 nov", "-", "-"],
 ["S28", "vie 13 nov", "-", "Entregable ligero: gráfica del filtro de Kalman al campus"],
 ["S29", "mié 18 nov", "-", "-"],
 ["S30", "jue 19 nov", "-", "-"],
 ["S31", "vie 20 nov", "-", "Cuestionario B6"],
 ["S32", "mié 25 nov", "Traer portátil con ROS 2 Jazzy instalado y verificado", "-"],
 ["S33", "jue 26 nov", "-", "Cuestionario relámpago de 3 preguntas (topic/servicio/acción)"],
 ["S34", "vie 27 nov", "Opcional: Corke cap. 5, pp. 177-187", "Entregable ligero del taller de ROS 2"],
 ["S35", "mié 2 dic", "-", "-"],
 ["S36", "jue 3 dic", "-", "-"],
 ["S37", "vie 4 dic", "ENTREGA 3 del proyecto: percepción o navegación", "Cuestionario B7"],
 ["S38", "mié 9 dic", "-", "-"],
 ["S39", "jue 10 dic", "-", "-"],
 ["S40", "vie 11 dic", "Preparar la presentación del seminario · cuestionario B8 en Moodle (hasta el 15 dic)", "EXAMEN PARCIAL 2 (bloques 5–7) · 2 h · 6 versiones"],
 ["S41", "mié 16 dic", "-", "Seminario: 5 presentaciones con rúbrica"],
 ["S42", "jue 17 dic", "Preparar la defensa del proyecto", "Seminario: 5 presentaciones con rúbrica · cierre"],
 ["S43", "vie 18 dic", "-", "DEFENSA del proyecto (5 equipos) · encuesta de retroalimentación"],
];
C.push(tabla(["Ses.", "Fecha", "Se encarga para la siguiente", "Se recoge o evalúa"], cal, [700, 1150, 3800, 3710]));

// ---------- 4 ----------
C.push(new Paragraph({ children: [new PageBreak()] }));
C.push(h1("4. Los ocho cuestionarios de seguimiento"));
C.push(p("Formato común: 15 minutos y 10 preguntas ABCD extraídas al azar del banco de 12 del bloque (ficheros GIFT importables en Moodle; cada error resta un tercio), en los últimos quince minutos de la última sesión del bloque, salvo el B8, que se abre en Moodle del 11 al 15 de diciembre por coincidir su sesión de cierre con el parcial 2. No son un examen: son el mecanismo que obliga a repasar antes de que el bloque se cierre y que te dice, a ti, qué no ha quedado. La regla de oro es empezar la sesión siguiente comentando los dos errores más frecuentes, porque un cuestionario que se corrige solo y del que nunca se habla deja de tomarse en serio a la tercera semana."));
C.push(tabla(
 ["Cuest.", "Sesión y fecha", "Qué entra"],
 [
 ["B1", "S4 · jue 17 sep", "Definición de mecatrónica y los ocho componentes; los tres problemas del diseño no acoplado; lectura del MDQ; fechas clave 1920, 1961 y 1968; definición de robot; sensores propioceptivos y exteroceptivos"],
 ["B2", "S7 · vie 25 sep", "Taxonomías de robots; Definición 2.1 de configuración y grados de libertad; configuraciones de manipuladores; restricción no holonómica; las dos partes de la ISO 10218 y los cuatro métodos colaborativos"],
 ["B3", "S12 · jue 8 oct", "Características estáticas y dinámicas; cuadratura del encoder; error de bias y deriva en IMU; puente de Wheatstone; curva par-velocidad; criterios de selección de actuador"],
 ["B4", "S19 · vie 23 oct", "Bloqueo de cardán; definición de SO(3) y SE(3); producto de exponenciales; las ocho soluciones del PUMA; jacobiano y singularidades; dualidad fuerza-velocidad"],
 ["B5", "S24 · jue 5 nov", "EDO del motor y su reducción; especificaciones y ubicación de polos; efecto de cada ganancia del PID; anti-windup; controlabilidad y observabilidad"],
 ["B6", "S31 · vie 20 nov", "Proyección y calibración; Canny y Harris; criterio clásico frente a aprendido; ciclo predicción-corrección; formulación del SLAM online y completo"],
 ["B7", "S37 · vie 4 dic", "QoS y grafo de computación; elección entre topic, servicio y acción; comandos de colcon; admisibilidad de la heurística de A*; capas del costmap"],
 ["B8", "Moodle, en casa · 11–15 dic", "Elementos del MDP y retorno descontado; términos de la actualización de Q-learning; idea del recorte de PPO; aleatorización de dominio; qué es un modelo VLA; gemelo digital (lectura guiada)"],
 ],
 [800, 1750, 6810]
));
C.push(pRuns([
 { text: "Cuestionario relámpago de S33. ", bold: true },
 { text: "Aparte de los ocho, el guion de S33 incluye tres preguntas rápidas con mando o formulario para fijar la regla de elección entre topic, servicio y acción. No lleva nota: es una comprobación de comprensión en caliente, y conviene mantenerla así para que nadie la viva como examen sorpresa." },
]));

// ---------- 4bis ----------
C.push(h1("4 bis. Los exámenes: dos parciales y un final, en seis versiones"));
C.push(p("Parcial 1 (S25, viernes 6 de noviembre, 2 h): bloques 1–4. Parte A, test de 10 preguntas ABCD (2,0 pt, extraídas de los bancos de B1–B4); parte B, Nyquist/aliasing y MDQ (2,0 pt); parte C, cinemática directa del 2R con tabla DH y espacio de trabajo (3,0 pt); parte D, cinemática inversa, jacobiano y estática (3,0 pt). Parcial 2 (S40, viernes 11 de diciembre, 2 h): bloques 5–7. Parte A, test (2,0 pt); parte B, diseño PD con gravedad y paso al PID con windup (3,0 pt); parte C, un paso completo de filtro de Kalman 1D (2,5 pt); parte D, A* sobre rejilla y diagnóstico de QoS (2,5 pt). Examen final (enero, 3 h): bloques 1–8; test de 12 preguntas (2,4 pt), caso de seguridad ISO (1,6 pt), cinemática y control (3,0 pt), Bayes discreto (1,5 pt) y Q-learning con actualización numérica (1,5 pt); incluye la recuperación por bloques de los parciales."));
C.push(p("Cada examen existe en seis versiones (A–F) con idéntica estructura y dificultad: cambian los parámetros numéricos y el subconjunto de test, y las soluciones de cada versión están calculadas y publicadas en los documentos de corrección (Correccion_82514_Parcial1, _Parcial2 y _Final), que incluyen además la rúbrica de corrección por apartados con los errores frecuentes y su descuento. Regla de reparto: versiones en damero para que dos vecinos nunca compartan números."));
C.push(box("Pesos", "Parcial 1: 15 % · Parcial 2: 15 % · Final: 10 % (partida de exámenes, 40 % de la guía docente). Los parciales no liberan materia del final, pero quien tenga los dos parciales aprobados afronta un final centrado en B8 e integración; quien tenga un parcial por debajo de 4 recupera ese bloque de materia dentro del final."));

// ---------- 5 ----------
C.push(h1("5. Talleres con entregable"));
C.push(p("Once sesiones producen algo tangible que sale del aula. Conviene distinguir los dos tipos: el entregable de registro, que solo sirve para constatar que el equipo ha hecho el trabajo y se puntúa como presente o ausente dentro de las actividades de seguimiento, y el entregable con corrección, que se revisa y devuelve con comentarios."));
C.push(tabla(
 ["Sesión", "Qué se entrega", "Tipo", "Cuándo"],
 [
 ["S7", "Tabla de riesgos de seis filas sobre la célula del laboratorio (por equipo)", "Con corrección", "En el aula, al acabar el taller"],
 ["S10", "Selección razonada de sensores para tres casos", "Registro", "Puesta en común, sin recogida"],
 ["S12", "Selección motor-reductora con números", "Registro", "Puesta en común, sin recogida"],
 ["S13", "Cuaderno de pose ejecutado con los ejercicios resueltos", "Registro", "Campus, fin de semana"],
 ["S15", "Comparación entre el modelo de la toolbox y el ABB real", "Registro", "En el aula"],
 ["S16", "Cuaderno de cinemática inversa con las ocho ramas", "Registro", "Campus, fin de semana"],
 ["S19", "Trayectoria articular y cartesiana del 2R", "Registro", "Campus, fin de semana"],
 ["S22", "Tabla de ganancias finales y métricas (Mp, ts) por pareja", "Con corrección", "En el aula, para la puesta en común"],
 ["S28", "Ficheros de calibración de la cámara (cuaderno encargado en S26)", "Con corrección", "Campus, antes de la sesión"],
 ["S28", "Gráfica de mu ± 2 sigma frente a la trayectoria verdadera", "Registro", "Campus, al acabar"],
 ["S34", "Paquete de ROS 2 funcionando con su captura de rqt_graph", "Con corrección", "Campus, fin de semana"],
 ],
 [900, 4300, 1700, 2460]
));
C.push(box("Los ficheros de calibración del cuaderno S26→S28", "Son el único entregable que se reutiliza más adelante: la calibración que cada equipo obtenga es la que usará en la parte de percepción del proyecto. Conviene recogerlos con nombre de equipo y guardarlos, porque rehacer una calibración en diciembre cuesta una sesión entera."));

// ---------- 6 ----------
C.push(new Paragraph({ children: [new PageBreak()] }));
C.push(h1("6. El proyecto integrador"));
C.push(p("Es la pieza que obliga a conectar los bloques y la que más peso tiene fuera del examen. Equipos formados en S5 y cerrados en S7; tres entregas parciales alineadas con el final de los bloques que las alimentan, y defensa oral en S43. La lógica de las entregas parciales no es burocrática: cada una obliga a cerrar una etapa antes de que el bloque siguiente la dé por sabida, y permite detectar en octubre al equipo que no arranca en lugar de descubrirlo en diciembre."));
C.push(tabla(
 ["Hito", "Fecha", "Qué se entrega", "Qué se comprueba"],
 [
 ["Formación de equipos", "S5 · 18 sep", "Composición propuesta", "Tamaño y mezcla de perfiles"],
 ["Equipos cerrados", "S7 · 25 sep", "Composición definitiva y tema elegido", "Que el alcance sea abarcable en el semestre"],
 ["Entrega 1", "S19 · 23 oct", "Modelo cinemático del robot elegido, con su verificación numérica", "Que el modelo esté validado, no solo escrito"],
 ["Entrega 2", "S26 · 11 nov", "Control implementado sobre el modelo, con respuesta medida", "Que haya al menos una métrica de desempeño"],
 ["Entrega 3", "S37 · 4 dic", "Percepción o navegación en simulación, integrada con lo anterior", "Que los módulos hablen entre sí"],
 ["Defensa", "S43 · 18 dic", "12 min de defensa y 5 de preguntas, más memoria", "Integración, resultados medidos, análisis crítico"],
 ],
 [1750, 1200, 3400, 3010]
));
C.push(h2("Rúbrica de la defensa"));
C.push(tabla(
 ["Peso", "Dimensión", "Qué se valora"],
 [
 ["40%", "Integración técnica", "¿Los módulos hablan entre sí, hay un sistema, o cuatro prácticas juntas? Es la competencia RAM23-S de la guía docente"],
 ["25%", "Resultados medidos", "Al menos una métrica cuantitativa: error de seguimiento, tiempo de ciclo, tasa de éxito en N intentos, error de localización"],
 ["20%", "Análisis crítico", "Limitaciones reconocidas, diagnóstico de lo que falló, camino propuesto"],
 ["15%", "Claridad y reparto", "Exposición ordenada y participación real de todos: la defensa es individual dentro del equipo"],
 ],
 [800, 2300, 6260]
));
C.push(p("El criterio que conviene decir en voz alta antes de la primera defensa, y que está también en los apuntes del bloque 8: un proyecto que no llegó a funcionar del todo, pero cuyo equipo sabe por qué, lo ha medido y propone un camino, puntúa por encima de uno que funciona sin que nadie sepa explicarlo. Es la lección de ingeniería más transferible del curso y pierde fuerza si se dice solo en la corrección individual."));
C.push(box("Declaración de uso de IA generativa", "Obligatoria en las tres entregas parciales y en la memoria final. No es un trámite: la política del curso permite el uso de asistentes de IA para estudiar y programar, y a cambio exige que se declare y que cualquier parte del trabajo sea defendible oralmente por cualquier miembro del equipo. Conviene comprobarlo en la entrega 1, cuando todavía hay margen para corregir el hábito."));

// ---------- 7 ----------
C.push(h1("7. El seminario de artículos"));
C.push(p("Por parejas, un artículo publicado en los últimos doce a dieciocho meses, presentado en diez minutos más cinco de preguntas. Es el mecanismo que mantiene la asignatura pegada a la frontera sin que tengas que rehacer el temario cada año, y por eso conviene protegerlo: si se convierte en un relleno de final de semestre, deja de funcionar."));
C.push(tabla(
 ["Hito", "Fecha", "Qué pasa"],
 [
 ["Lanzamiento", "S4 · 17 sep", "Reglas, fuentes recomendadas, rúbrica y formación de parejas"],
 ["Validación del artículo", "antes del 30 sep", "El profesor aprueba cada artículo: venue reconocida o arXiv con tracción, resultados experimentales, extensión abordable"],
 ["Presentaciones I", "S41 · 16 dic", "Cinco parejas, cronometradas"],
 ["Presentaciones II y cierre", "S42 · 17 dic", "Cinco parejas y mapa de artículos por bloque"],
 ],
 [2100, 1500, 5760]
));
C.push(h2("Rúbrica del seminario"));
C.push(tabla(
 ["Peso", "Dimensión", "Qué se valora"],
 [
 ["40%", "Comprensión técnica", "¿Entienden el método o repiten el resumen? Se comprueba en las preguntas, no en las diapositivas"],
 ["30%", "Claridad", "Estructura, ritmo, calidad de las figuras, capacidad de hacer accesible lo complejo"],
 ["20%", "Análisis crítico", "Limitaciones reconocidas y no reconocidas, honestidad de la comparación, aplicabilidad real"],
 ["10%", "Gestión de preguntas", "Responder lo que se sabe, admitir lo que no y razonar en voz alta"],
 ],
 [800, 2300, 6260]
));
C.push(p("Cada presentación debe cubrir problema, método, resultados, limitaciones y conexión explícita con al menos un bloque del curso. La última es obligatoria y es la que convierte el seminario en parte de la asignatura en lugar de un añadido. Las preguntas del público cuentan para la participación de quien las hace, y conviene anunciarlo al empezar S41 para que la sala no quede muda."));

// ---------- 8 ----------
C.push(new Paragraph({ children: [new PageBreak()] }));
C.push(h1("8. Ejercicios de los cuadernos y deberes previos"));
C.push(h2("Los 87 ejercicios de los cuadernos"));
C.push(p("Los veintinueve cuadernos de Colab llevan tres ejercicios cada uno, con sus soluciones al final del propio cuaderno. Son de autocorrección deliberadamente: su función es que el estudiante compruebe si ha entendido, no generar trabajo de corrección. En las sesiones de taller se hacen en clase; en las de teoría con cuaderno de apoyo quedan como trabajo personal de la semana."));
C.push(p("Vale la pena saber cuáles son los cinco que más discusión generan, porque son los que conviene reservar para hacer en común en lugar de dejarlos sueltos: en S28, el sensor con probabilidad de acierto 0,5 que no cambia la creencia; en S18, que el óptimo de isotropía del 2R no está donde dice la intuición; en S12, que el óptimo teórico de la relación de transmisión cae fuera de la ventana viable del motor; en S35, que una heurística inadmisible expande menos nodos pero devuelve un camino un 20% peor; y en S40, que la política condicionada por una instrucción resuelve la multimodalidad que el regresor simple no puede, que es el puente conceptual hacia los modelos VLA."));
C.push(h2("Los dieciséis deberes previos"));
C.push(p("No se corrigen. Su cumplimiento se comprueba con la pregunta de recuperación de los primeros cinco minutos de la sesión siguiente, que es más eficaz que recogerlos y cuesta la décima parte. Los cuatro que son condición necesaria y no simple recomendación, porque sin ellos la sesión no se puede dar, están marcados en la tabla."));
C.push(tabla(
 ["Para", "Qué hay que traer hecho", "¿Crítico?"],
 [
 ["S2", "De Silva cap. 1, pp. 1-10", "No"],
 ["S3", "Corke cap. 1, pp. 1-9", "No"],
 ["S4", "Un ejemplo de robot visto en prensa reciente", "No"],
 ["S6", "Corke cap. 4, pp. 139-146", "No"],
 ["S9", "Fraden cap. 3, pp. 62-103 (principios físicos)", "No"],
 ["S10", "Preguntas de selección de acelerómetro (Fraden p. 332)", "No"],
 ["S12", "Inercia reflejada del ejemplo publicado en el campus", "No"],
 ["S14", "Corke cap. 7, pp. 255-260", "No"],
 ["S17", "Corke cap. 8, pp. 310-315", "No"],
 ["S21", "python-control instalado y verificado", "Sí"],
 ["S22", "Portátil con python-control funcionando; ley PID releída", "Sí"],
 ["S24", "Lynch y Park pp. 271-275 (Lagrange y ejemplo 2R)", "No"],
 ["S26", "Corke cap. 11, pp. 440-452", "No"],
 ["S34", "Portátil con ROS 2 Jazzy instalado y verificado", "Sí"],
 ["S35", "Opcional: Corke cap. 5, pp. 177-187", "No"],
 ["S41", "Presentación del seminario preparada", "Sí"],
 ],
 [800, 6700, 1860]
));
C.push(box("Los cuatro críticos y cómo protegerlos", "S21, S22 y S34 dependen de que el software esté instalado antes de entrar en el aula, y S41 de que la presentación del seminario esté preparada. La medida que funciona es dedicar los últimos dos minutos de la sesión anterior a que cada estudiante ejecute la comprobación delante de ti y levante la mano si falla, en lugar de anunciarlo y confiar. Para ROS 2 el cuaderno de S34 incluye una celda de diagnóstico pensada exactamente para eso, y conviene publicarla en el campus una semana antes."));

// ---------- 9 ----------
C.push(h1("9. Dos decisiones pendientes antes de septiembre"));
C.push(h3("Dónde puntúa el seminario de artículos"));
C.push(p("La guía docente oficial tiene una partida de trabajos y presentaciones del 10%, que es donde encajaría el seminario de forma natural. La propuesta de modernización disolvía esa partida dentro del proyecto integrador para crear un 20% de proyecto. Si se aprueba la propuesta tal cual, el seminario se queda sin casilla. Hay dos salidas razonables: dejarlo dentro de actividades de seguimiento, que es donde también están los cuestionarios, o mantener la partida de trabajos y presentaciones con su 10% y bajar el proyecto al 10%. La primera es más simple; la segunda hace más visible el peso del seminario, que es la actividad que más trabajo personal exige. Conviene decidirlo antes de publicar la guía, porque los estudiantes preguntarán el primer día."));
C.push(h3("Qué pasa con el laboratorio"));
C.push(p("El trabajo experimental con los robots Mitsubishi y ABB mantiene su 20% y su diseño no se ha tocado, tal como acordamos. Pero su calendario y el de la teoría no están sincronizados en este documento porque las prácticas se programan aparte. Merece una comprobación antes de septiembre: el modelo cinemático no aparece hasta el 9 de octubre y el control hasta finales de ese mes, de modo que cualquier práctica de programación de robot anterior a esas fechas irá por delante de la teoría que la sostiene. No es necesariamente un problema, a veces conviene que el laboratorio abra apetito, pero es mejor que sea una decisión y no un accidente."));

// ---------- 10 ----------
C.push(h1("10. Qué hay que publicar en el campus, y cuándo"));
C.push(tabla(
 ["Cuándo", "Qué se publica"],
 [
 ["Antes del 9 de septiembre", "Guía docente, calendario de sesiones, política de IA generativa, bibliografía y enlaces a los cuadernos de Colab"],
 ["S4 · 17 de septiembre", "Reglas y rúbrica del seminario, lista de fuentes recomendadas, plazo de validación del 30 de septiembre"],
 ["S5 · 18 de septiembre", "Enunciado del proyecto integrador con las tres entregas, sus fechas y la rúbrica de la defensa"],
 ["S11 · antes del 7 de octubre", "Ejemplo de cálculo de inercia reflejada para el deber previo de S12"],
 ["S20 · antes del 28 de octubre", "Instrucciones de instalación de python-control y comprobación"],
 ["Antes del 25 de noviembre", "Instrucciones de instalación de ROS 2 Jazzy, contenedor docker alternativo y celda de diagnóstico del cuaderno de S34"],
 ["Tras cada bloque", "Cuestionario abierto durante 48 h y, después, comentario de los dos errores más frecuentes"],
 ["S43 · 18 de diciembre", "Examen de muestra con solución comentada y calendario de tutorías de enero"],
 ],
 [2400, 6960]
));
C.push(p("Una última recomendación de método: la mitad de los problemas administrativos de un semestre vienen de plazos que existen en la cabeza del profesor pero no en el campus. Publicar cada fecha en el momento en que se anuncia en clase, y no después, elimina casi todas las reclamaciones de diciembre."));

const doc = new Document({
 numbering: numberingConfig,
 styles: { default: { document: { run: { font: F, size: 22 } } } },
 sections: [{ properties: { page: { margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } }, children: C }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync("Tareas_Pruebas_Entregables_82514.docx", b); console.log("OK tareas"); });
