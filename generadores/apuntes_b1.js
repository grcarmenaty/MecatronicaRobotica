const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, PageBreak, AlignmentType } = require("docx");
const { IQS, F, p, pRuns, h1, h2, h3, bullet, box, tabla, tablaTiempos, numberingConfig } = require("./lib_iqs");

const children = [];

// ---------- Portada ----------
children.push(
  new Paragraph({ spacing: { before: 2000, after: 200 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "Bloque 1", size: 40, bold: true, color: IQS.greenDark, font: F })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
    children: [new TextRun({ text: "Introducción a la mecatrónica y panorama 2026 de la robótica", size: 44, bold: true, color: IQS.navy, font: F })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
    children: [new TextRun({ text: "82514 — Mecatrónica y Robótica · IQS Universitat Ramon Llull", size: 24, color: IQS.grey, font: F })] }),
  new Paragraph({ alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "Apuntes del profesor · Sesiones S1–S4 (9, 10, 16 y 17 de septiembre de 2026) · 4 horas", size: 22, color: IQS.grey, font: F })] }),
  new Paragraph({ children: [new PageBreak()] })
);

// ---------- Objetivos ----------
children.push(h1("Objetivos de aprendizaje del bloque"));
children.push(bullet("Definir la mecatrónica como disciplina de diseño integrado multidominio y enumerar los componentes de un sistema mecatrónico típico."));
children.push(bullet("Explicar por qué el diseño secuencial (no acoplado) produce sistemas subóptimos, y describir el diseño concurrente y el Cociente de Diseño Mecatrónico (MDQ)."));
children.push(bullet("Situar los hitos históricos de la robótica industrial y enunciar la definición operativa de robot: percibir, planificar, actuar."));
children.push(bullet("Describir el panorama actual del sector (Physical AI, humanoides, modelos fundacionales) y sus implicaciones profesionales y éticas."));
children.push(box("Materiales del bloque", "Presentación B1 (IQS_B1_Introduccion.pptx). Lecturas: De Silva et al., Mechatronics: Fundamentals and Applications, cap. 1; Corke, Robotics, Vision and Control (3.ª ed. Python), cap. 1. Para S4: selección de artículos del seminario."));

// ============ SESIÓN 1 ============
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("Sesión S1 (mié 9 sep, 1 h) — Qué es la mecatrónica"));
children.push(h2("Estructura de la clase"));
children.push(tablaTiempos([
  ["0–10 min", "Presentación de la asignatura", "Guía docente en pantalla: bloques, evaluación, proyecto integrador, política de IA generativa (se permite con declaración de uso y defensa oral). Presentarse y pedir a los estudiantes una ronda rápida de expectativas."],
  ["10–15 min", "Pregunta de arranque", "«¿Qué objetos de vuestro día a día son mecatrónicos?» Recoger respuestas en pizarra; volveremos a la lista al final."],
  ["15–35 min", "Teoría: definición y dominios", "Apartados 1.1 y 1.2 de estos apuntes. Insistir en la palabra clave: sinergia, no yuxtaposición."],
  ["35–50 min", "Teoría: componentes y ejemplos", "Apartado 1.3. Desarrollar el ejemplo del disco duro y del servomotor; el ABS como sistema multidominio."],
  ["50–60 min", "Cierre y discusión", "Revisar la lista inicial: ¿cuáles eran realmente mecatrónicos? Anunciar la lectura recomendada (De Silva, cap. 1)."],
]));

children.push(h2("1.1. Definición de mecatrónica"));
children.push(p("La mecatrónica es la aplicación sinérgica de la mecánica, la electrónica, la ingeniería de control y la ingeniería informática al desarrollo de productos y sistemas electromecánicos mediante un enfoque de diseño integrado (De Silva, cap. 1). Las dos palabras que soportan todo el peso de la definición son «sinérgica» e «integrado»: no se trata de que un producto contenga piezas mecánicas y electrónica —eso lo cumple cualquier electrodoméstico desde hace un siglo—, sino de que sus subsistemas se conciban, modelen y optimicen juntos, teniendo en cuenta sus interacciones dinámicas desde la primera fase del diseño."));
children.push(p("El término tiene fecha y lugar de nacimiento conocidos: lo acuñó la empresa japonesa Yaskawa Electric en 1969 (registrándolo como marca en 1972 y liberando los derechos en 1982), como contracción de mechanics y electronics. La historia del término es un buen recurso docente: nació en la industria, no en la academia, y nació precisamente en el país que estaba industrializando la robótica."));
children.push(p("La mecatrónica es particularmente aplicable a los sistemas de dominio mixto o multidominio: aquellos que combinan varios dominios físicos —eléctrico, mecánico, fluídico y térmico— de manera integrada. El ejemplo canónico de De Silva es el sistema de frenos antibloqueo (ABS) de un automóvil: involucra mecánica (la dinámica del vehículo y de la rueda), electrónica (sensores de velocidad de giro y unidad de control), hidráulica (el circuito de frenado) y transferencia de calor (la disipación en los discos). Diseñar el ABS de forma «óptima» exige tratarlo como un producto mecatrónico único, no como cuatro problemas independientes."));
children.push(box("Idea fuerza para el aula", "Un sistema electromecánico diseñado por partes funciona; un sistema mecatrónico diseñado de forma integrada funciona mejor, cuesta menos energía y es más fiable. La mecatrónica es, ante todo, una metodología de diseño, no una lista de componentes."));

children.push(h2("1.2. Los dominios de la mecatrónica"));
children.push(p("Conviene dibujar en la pizarra el diagrama clásico (figura 1.2 de De Silva): la mecatrónica como intersección de la ingeniería mecánica, la ingeniería eléctrica y electrónica, la ingeniería de control y la ingeniería informática. Alrededor de esa intersección orbitan las actividades que la asignatura recorrerá durante el semestre: modelado y análisis (bloques 4 y 5), sensores y transductores (bloque 3), actuadores (bloque 3), controladores (bloque 5), procesamiento de señal y percepción (bloque 6), software (bloque 7) y diseño integrado del sistema completo (proyecto integrador)."));
children.push(p("Un matiz importante que De Silva subraya: cada aspecto o problema dentro de un sistema mecatrónico puede tener a su vez carácter multidominio. Un servomotor de corriente continua es en sí mismo un dispositivo mecatrónico —con sus componentes mecánicos (rotor, estátor, rodamientos, encoder óptico), eléctricos (bobinados, electrónica de potencia y conmutación) y de control (lazo de realimentación de posición o velocidad)— y a la vez es un componente dentro de un sistema mecatrónico mayor, como un robot o un automóvil. Esta estructura anidada (sistemas dentro de sistemas) reaparecerá cuando estudiemos arquitecturas de robots."));

children.push(h2("1.3. Componentes de un sistema mecatrónico y ejemplos"));
children.push(p("Según De Silva, un sistema mecatrónico típico consta de: un esqueleto mecánico, actuadores, sensores, controladores, dispositivos de acondicionamiento y modificación de señal, hardware y software digital, dispositivos de interfaz y fuentes de alimentación. Esta lista es literalmente el índice de la asignatura, y merece la pena decirlo en voz alta: el bloque 3 cubre sensores y actuadores, el 4 el esqueleto (su geometría y movimiento), el 5 los controladores y el modelado, el 6 el procesamiento de la información sensorial y el 7 el software que lo integra todo."));
children.push(pRuns([
  { text: "Ejemplo 1 — El disco duro (HDD). ", bold: true },
  { text: "Un dispositivo cotidiano (aunque cada vez menos) que condensa toda la disciplina en unos centímetros: estructuras mecánicas microminiatura (los platos girando a 7200 rpm, el cabezal volando a nanómetros de la superficie), un motor de husillo, un actuador de bobina móvil para el brazo, sensores de posición embebidos en las propias pistas, y un circuito de control que ejecuta un lazo de seguimiento de pista con precisión submicrométrica. Preguntar a los estudiantes: ¿por qué no puede diseñarse el servo del brazo sin conocer la mecánica del brazo? La respuesta (resonancias estructurales, masa móvil) anticipa el bloque 5." },
]));
children.push(pRuns([
  { text: "Ejemplo 2 — El servomotor. ", bold: true },
  { text: "Motor con realimentación sensorial para generar movimientos precisos. Identificar sobre un despiece sus tres capas: mecánica (rotor, estátor, rodamientos, encoder), eléctrica (bobinados, etapa de potencia, conmutación) y de control (lazo cerrado). Es el «átomo» de la robótica: un robot industrial de seis ejes son seis servomotores coordinados más un esqueleto." },
]));
children.push(pRuns([
  { text: "Ejemplo 3 — Áreas de aplicación. ", bold: true },
  { text: "Recorrer rápido la lista de De Silva para transmitir amplitud: transporte terrestre (airbag, ABS, control de crucero, suspensión activa), aéreo (simuladores, control de vuelo, tren de aterrizaje), fabricación (robots de soldadura, pintura, ensamblado e inspección, AGV, CNC, micromecanizado), medicina (robótica quirúrgica y de rehabilitación, telemedicina), oficina y hogar (impresoras multifunción, aspiradoras robóticas), ingeniería civil (grúas y excavadoras) y espacio (los rovers de exploración de Marte, «sistemas fundamentalmente mecatrónicos»). Conclusión de De Silva: no hay límite a los dispositivos que pueden incorporar mecatrónica; las fronteras entre disciplinas se difuminan." },
]));

// ============ SESIÓN 2 ============
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("Sesión S2 (jue 10 sep, 1 h) — El proceso de diseño mecatrónico"));
children.push(h2("Estructura de la clase"));
children.push(tablaTiempos([
  ["0–5 min", "Recuperación", "Dos preguntas rápidas sobre S1: definición de mecatrónica y componentes de un sistema mecatrónico."],
  ["5–20 min", "Teoría: modelado y diseño", "Apartado 2.1. Dibujar el bucle modelo-diseño en pizarra."],
  ["20–40 min", "Teoría: diseño acoplado y MDQ", "Apartados 2.2 y 2.3. Las ecuaciones se presentan conceptualmente; no se exige su manipulación en el examen, sí su interpretación."],
  ["40–52 min", "Caso práctico en parejas", "«Diseñad el accionamiento de una cinta transportadora»: primero secuencialmente, luego identificando qué decisiones deberían tomarse de forma acoplada (motor-reductora-control). Puesta en común."],
  ["52–60 min", "Cierre", "Evolución de diseño e instrumentación integrada (apartado 2.4). Anunciar S3: historia de la robótica."],
]));

children.push(h2("2.1. Modelado y diseño: un bucle iterativo"));
children.push(p("Un modelo es una representación de un sistema real (De Silva). En ingeniería mecatrónica, modelado y diseño avanzan de la mano de forma iterativa: los objetivos y especificaciones de diseño alimentan un modelo del sistema; el modelo permite predecir el desempeño; la predicción informa las decisiones de diseño; el diseño resultante refina el modelo, y el ciclo se repite. Este bucle (figura 1.3 de De Silva) es el esquema conceptual central del proceso de diseño mecatrónico y estructura el proyecto integrador de la asignatura: los equipos construirán primero un modelo cinemático (bloque 4), lo usarán para diseñar el control (bloque 5) y lo refinarán con percepción y navegación (bloques 6 y 7)."));
children.push(p("De Silva señala la energía como hilo unificador del diseño integrado, por dos razones. Primera: los puertos de energía y potencia enlazan la dinámica eléctrica con la mecánica, lo que permite formulaciones híbridas multidominio (la potencia eléctrica v·i que entra en un motor ideal es igual a la potencia mecánica ω·τ que sale: v·i = ω·τ). Segunda: un diseño óptimo persigue mínima disipación —más disipación significa menor eficiencia, más problemas térmicos, más ruido, vibración, desgaste e impacto ambiental. También advierte contra el sobredimensionamiento sistemático mediante factores de seguridad excesivos y especificaciones de «peor caso»: no producen diseños óptimos ni, muchas veces, los más económicos."));

children.push(h2("2.2. Por qué falla el diseño secuencial (no acoplado)"));
children.push(p("El enfoque tradicional de diseño de un sistema multidominio es secuencial: primero se diseña la parte mecánica y estructural; después se seleccionan e interconectan los componentes eléctricos y electrónicos; luego se elige un computador y su interfaz; y por último se añade el controlador. Cada subsistema se diseña por separado manteniendo constantes sus interacciones con los demás: esto es el diseño no acoplado."));
children.push(p("De Silva identifica tres problemas estructurales de este enfoque. Primero, al interconectar dos componentes diseñados por separado, sus características y condiciones de operación originales cambian por efecto de la carga y de las interacciones dinámicas: el motor que en el catálogo daba cierto par a cierta velocidad ya no lo da cuando arrastra la inercia real de la transmisión. Segundo, el acoplamiento perfecto de dos componentes diseñados independientemente es prácticamente imposible: uno quedará subutilizado o sobrecargado, y ambas condiciones son ineficientes y no deseables. Tercero, tras la interconexión algunas variables que eran externas pasan a ser internas y quedan «ocultas»: ya no pueden monitorizarse con sensores ni controlarse directamente, lo que genera problemas invisibles para el sistema de supervisión."));

children.push(h2("2.3. Diseño acoplado y Cociente de Diseño Mecatrónico (MDQ)"));
children.push(p("El marco formal del diseño acoplado modela el sistema electromecánico como dos subsistemas unidos por un transformador de energía ideal, con variables de paso (corriente i, par τ) y variables de puerto (tensión v, velocidad angular ω), ligadas por la relación de potencia v·i = ω·τ. Si cada subsistema se diseña por separado, cada uno alcanza su índice de diseño óptimo aislado (I-ue para el eléctrico, I-um para el mecánico), donde el índice de diseño se define como la medida del grado en que un diseño satisface sus especificaciones. Pero al interconectarlos, ninguno de los dos índices se alcanza realmente."));
children.push(p("El diseño mecatrónico se formula entonces como un problema de optimización conjunta: minimizar la función de coste J = αe·(Iue − Ie)² + αm·(Ium − Im)², donde Ie e Im son los índices realmente alcanzados tras la interconexión y αe, αm ponderan la importancia de cada dominio. De forma equivalente, De Silva (2003) propone maximizar el Cociente de Diseño Mecatrónico: MDQ = αe·(Ie/Iue)² + αm·(Im/Ium)². La lectura conceptual es lo importante: el MDQ mide cuánto se acerca el sistema completo al ideal de cada uno de sus dominios, y el diseño mecatrónico busca el mejor compromiso global en lugar del óptimo local de cada parte."));
children.push(p("El MDQ se generaliza a más de dos categorías, con índices que pueden representar fiabilidad, mantenibilidad, eficiencia, relación coste-eficacia, potencia, tamaño y geometría, facilidad de control (control friendliness) y nivel de inteligencia. Para explorar el espacio de diseños, De Silva propone algoritmos genéticos: cada cromosoma codifica un diseño completo, cada gen un elemento de información (un componente, una estructura de conexión, un parámetro), los alelos son las opciones disponibles, y la función de aptitud es el propio MDQ. La optimización puede además organizarse jerárquicamente: una capa superior decide el tipo de actuador (hidráulico, DC, de inducción, paso a paso) y una capa inferior elige el motor concreto dentro del catálogo disponible."));

children.push(h2("2.4. Evolución de diseño e instrumentación integrada"));
children.push(p("La evolución de diseño extiende la idea de mantenimiento predictivo al diseño mismo: igual que un sistema de monitorización de salud de máquina detecta componentes defectuosos, puede detectar regiones de debilidad de diseño. El marco de De Silva tiene cinco etapas: (1) desarrollar un modelo del sistema existente; (2) establecer, mediante monitorización y un sistema experto, qué segmentos del sistema pueden modificarse —los «sitios modificables»—; (3) formular una función de desempeño que represente la bondad del diseño (el MDQ); (4) hacer evolucionar el modelo con un método de optimización (por ejemplo programación genética) maximizando esa función; (5) implementar en el sistema real los cambios del modelo evolucionado."));
children.push(p("Por último, la instrumentación —sensores, actuadores, interfaces, controladores— debe tratarse como aspecto integral del diseño, no como un añadido posterior. De Silva reconoce, no obstante, una limitación práctica: el enfoque mecatrónico pleno exige poder modificar todo el sistema de forma concurrente, y eso rara vez es realista cuando el proceso ya existe. Su ejemplo: en un sistema de transporte con vehículos guiados ya construido, sustituir algunos vagones no permite rediseñar la infraestructura; los vagones nuevos pueden instrumentarse de forma mecatrónica, pero el sistema global no operará de forma óptima. Es una lección de humildad ingenieril útil para el proyecto: casi siempre se diseña con restricciones heredadas."));

// ============ SESIÓN 3 ============
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("Sesión S3 (mié 16 sep, 1 h) — Historia y definición de robot"));
children.push(h2("Estructura de la clase"));
children.push(tablaTiempos([
  ["0–5 min", "Recuperación", "Pregunta rápida: los tres problemas del diseño no acoplado."],
  ["5–25 min", "Teoría: historia", "Apartado 3.1. Contar la historia como narrativa (autómatas → término «robot» → Unimation) apoyándose en las imágenes de la presentación."],
  ["25–40 min", "Teoría: definición de robot y sensores", "Apartados 3.2 y 3.3. La definición «percibir, planificar, actuar» es de las pocas que se preguntará literalmente en el examen."],
  ["40–55 min", "Teoría: telerobots y autonomía", "Apartado 3.4. Discusión: ¿es un dron teledirigido un robot? ¿Y un coche con mantenimiento de carril?"],
  ["55–60 min", "Cierre", "Anunciar S4 (panorama 2026) y pedir que traigan un ejemplo de robot «moderno» visto en prensa."],
]));

children.push(h2("3.1. De los autómatas a Unimation"));
children.push(p("La prehistoria de la robótica son los autómatas del siglo XVIII. El pato de Vaucanson (1739) batía las alas, comía grano y defecaba, pero ejecutaba un único programa fijo grabado en sus levas. El salto conceptual llega con el telar de Jacquard (1801): una máquina reprogramable, cuyo patrón de tejido se codificaba en tarjetas perforadas. Corke subraya que el telar «tiene muchos rasgos distintivos de un robot moderno: realizaba una tarea física y era reprogramable». Esa idea influyó en Babbage y, a través de él, en Ada Lovelace y el primer algoritmo: la historia de la robótica y la de la computación comparten raíz."));
children.push(p("La palabra «robot» nace en el teatro: la obra checa R.U.R. (Rossum's Universal Robots, 1920) de Karel Čapek, con el término roboti sugerido por su hermano Josef, emparentado en checo con «servidumbre». Los robots de la obra son personas artificiales que acaban rebelándose —el molde de casi toda la ciencia ficción posterior, incluidas las Tres Leyes de la Robótica con las que Isaac Asimov exploró la moralidad de la interacción humano-robot en sus relatos (1950–1985). Merece la pena señalar a los estudiantes cuánto de nuestras expectativas sobre los robots viene de la ficción y no de la ingeniería."));
children.push(p("La robótica industrial real comienza con una patente y un cóctel. George C. Devol solicitó en 1954 (concedida en 1961) la patente de un «Programmed Article Transfer»: un brazo de coordenadas polares sobre raíl cuyas secuencias de movimiento se grababan como patrones magnéticos en un tambor —el concepto de «Universal Automation», contraído en «Unimation». Devol conoció a Joseph Engelberger en un cóctel en 1954; juntos fundaron Unimation Inc. (Danbury, Connecticut), la primera empresa de robótica del mundo. El primer Unimate entró en servicio en 1961 en una planta de fundición a presión de General Motors en Nueva Jersey. En 1968 Unimation licenció su tecnología a Kawasaki Heavy Industries, que produjo el primer robot industrial japonés —el punto de partida del dominio japonés del sector que llega hasta hoy. Desde entonces se han fabricado millones de manipuladores para soldadura, pintura, carga de máquinas, montaje, clasificación y paletizado."));
children.push(box("Anécdota para el aula", "En 1966 Engelberger llevó un Unimate al programa de televisión The Tonight Show: el robot sirvió una cerveza, metió un putt de golf y dirigió la banda. Engelberger, «padre de la robótica», dedicó su segunda carrera a los robots de servicio hospitalarios (HelpMate Robotics). La asociación AAA entrega cada año un premio con su nombre."));

children.push(h2("3.2. La definición de robot"));
children.push(p("«No puedo definir un robot, pero sé reconocer uno cuando lo veo», bromeaba Engelberger. La definición operativa que adopta Corke —y esta asignatura— es: un robot es una máquina orientada a objetivos capaz de percibir, planificar y actuar (sense, plan, act). Un robot percibe su entorno, usa esa información junto con un objetivo para planificar una acción, y la ejecuta: mover la herramienta de un manipulador para asir una pieza, o conducir un vehículo móvil hasta un destino. Esta tríada organiza literalmente el resto del curso: percibir es el bloque 6, planificar el 7, actuar los bloques 3, 4 y 5."));

children.push(h2("3.3. Sensores propioceptivos y exteroceptivos"));
children.push(p("Primera clasificación técnica del curso, tomada de Corke: los sensores propioceptivos miden el estado del propio robot —los ángulos de las articulaciones de un brazo, las revoluciones de las ruedas de un móvil, la corriente que consume un motor—, mientras que los exteroceptivos miden el estado del mundo respecto al robot —desde el sensor de choque de una aspiradora hasta un receptor GPS, una brújula, o sensores activos que emiten pulsos acústicos, ópticos o de radio y miden distancias por tiempo de vuelo. La distinción reaparecerá en el bloque 3 (catálogo de sensores) y en el 6 (fusión sensorial: la propiocepción da odometría, la exterocepción corrige su deriva)."));

children.push(h2("3.4. Telerobots y grados de autonomía"));
children.push(p("Entre la teleoperación pura y la autonomía plena hay un espectro. El primer telerobot documentado es el barco radiocontrolado de Tesla (1898), su «teleautomaton». El origen técnico moderno está en el Proyecto Manhattan: Ray Goertz desarrolló en Argonne los brazos maestro-esclavo (hoy líder-seguidor) para manipular material radiactivo, con realimentación de fuerza del seguidor al líder. Sus descendientes directos son los ROV que exploraron el Titanic y los robots quirúrgicos actuales, que son teleoperados, no autónomos —una precisión que sorprende a muchos estudiantes."));
children.push(p("Corke distingue dos modos híbridos de compartir el control: en el control alternado (traded control), la función de control pasa del humano al computador y viceversa, como el piloto que conecta y desconecta el piloto automático; en el control compartido (shared control), ambos controlan a la vez, como un coche que mantiene el carril mientras el conductor gestiona la velocidad. Los rovers marcianos ilustran el punto medio: navegan autónomamente entre puntos, pero reciben objetivos de alto nivel de operadores en la Tierra, porque la latencia de minutos impone decisión local. Buena pregunta de discusión: ¿dónde está cada robot que conocen en ese espectro?"));

// ============ SESIÓN 4 ============
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("Sesión S4 (jue 17 sep, 1 h) — Panorama 2026 y lanzamiento del seminario"));
children.push(h2("Estructura de la clase"));
children.push(tablaTiempos([
  ["0–5 min", "Recuperación", "Definición de robot y ejemplos de sensores propioceptivos/exteroceptivos."],
  ["5–25 min", "Teoría: el momento actual de la robótica", "Apartado 4.1. Apoyarse en vídeos cortos (2–3 min) de humanoides y VLA en la presentación."],
  ["25–35 min", "Teoría: ética", "Apartado 4.2. Formato debate: dos afirmaciones proyectadas, votación a mano alzada, argumentos."],
  ["35–50 min", "Lanzamiento del seminario de artículos", "Apartado 4.3: reglas, calendario (presentaciones en S41–S42), reparto de temas/artículos por parejas."],
  ["50–60 min", "Cuestionario de seguimiento del bloque 1", "8–10 preguntas tipo test (Moodle/Kahoot). Cuenta para la evaluación continua."],
]));

children.push(h2("4.1. El momento «Physical AI»: por qué 2026 no es 2016"));
children.push(p("La robótica vive desde 2023 su transformación más profunda desde la llegada del microprocesador: la aplicación de modelos fundacionales —la tecnología detrás de los grandes modelos de lenguaje— al control de robots físicos. Los llamados modelos visión-lenguaje-acción (VLA) se entrenan con grandes volúmenes de demostraciones robóticas e imágenes y aprenden a producir directamente acciones motoras a partir de observaciones de cámara e instrucciones en lenguaje natural. Los tres ejemplos que hay que conocer en 2026: π0 (pi-zero) de Physical Intelligence, un modelo de flujo visión-lenguaje-acción para control general de robots; GR00T de NVIDIA, modelo fundacional abierto orientado a robots humanoides; y Gemini Robotics de Google DeepMind. La industria agrupa esta ola bajo la etiqueta «Physical AI» o «IA encarnada» (embodied AI)."));
children.push(p("En paralelo, los robots humanoides han pasado de curiosidad de laboratorio a producto con inversión industrial masiva, con pilotos en logística y fabricación, y los robots colaborativos y móviles autónomos (AMR) siguen siendo el segmento de mayor crecimiento en fábrica. Para los estudiantes el mensaje es doble: primero, los fundamentos que estudiaremos (cinemática, control, percepción probabilística) no caducan —los VLA generan consignas que ejecutan exactamente los lazos de control que veremos en el bloque 5—; segundo, el perfil profesional que demanda el mercado combina esos fundamentos con software moderno (Python, ROS 2) y con criterio para evaluar cuándo la IA aporta valor. En el bloque 8 volveremos sobre esto con detalle técnico, y el seminario de artículos os mantendrá pegados a la frontera durante todo el semestre."));

children.push(h2("4.2. Consideraciones éticas"));
children.push(p("Corke dedica su sección 1.5 a la ética y conviene traerla al aula el primer día que hablamos del presente. La preocupación más citada es el empleo: la IA ya realiza tareas de información (análisis de imágenes médicas, decisiones de crédito, redacción automática) y se teme que los robots invadan pronto las tareas físicas, aunque destreza, fiabilidad y coste aún lo limitan. Los contraargumentos también son serios: hay trabajos que las personas no deberían hacer (entornos insalubres o peligrosos) y trabajos sin mano de obra disponible; y la automatización ha sido crítica para mantener industrias enteras —y sus empleos e impuestos— en países de salarios altos. El caso de los coches autónomos añade otra dimensión: los conductores humanos matan a más de un millón de personas al año, y sin embargo la incomodidad social ante el coche autónomo es mayor que ante el conductor humano; ¿a quién culpamos cuando el robot se equivoca? La posición de Corke, que hago mía ante los estudiantes: estas cuestiones no deben decidirlas solo los roboticistas, pero tampoco pueden ignorarlas; participar en el debate es parte de la profesión."));

children.push(h2("4.3. Organización del seminario de artículos"));
children.push(bullet("por parejas, cada equipo elige (o recibe) un artículo científico publicado en los últimos 12–18 meses sobre robótica: VLA y robot learning, SLAM moderno, humanoides, manipulación, percepción, HRI o seguridad.", "Formato: "));
children.push(bullet("fuentes recomendadas: arXiv (cs.RO), ICRA/IROS/RSS/CoRL, Science Robotics, IEEE T-RO y RA-L. Validación del artículo por el profesor antes del 30 de septiembre.", "Selección: "));
children.push(bullet("presentación de 10 minutos + 5 de preguntas en S41–S42 (16–17 de diciembre): problema, método, resultados, limitaciones y conexión con los bloques del curso.", "Entrega: "));
children.push(bullet("claridad (30%), comprensión técnica (40%), análisis crítico (20%), gestión de preguntas (10%). Se permite IA generativa como asistente de estudio con declaración de uso; la defensa es oral e individual.", "Rúbrica: "));

// Bibliografía
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("Bibliografía del bloque"));
children.push(bullet("Mechatronics: Fundamentals and Applications, CRC Press, 2016 — capítulo 1 completo (secciones 1.1–1.7).", "De Silva, C. W. et al. "));
children.push(bullet("Robotics, Vision and Control: Fundamental Algorithms in Python, 3.ª ed., Springer, 2023 — capítulo 1 (historia, tipos, definición, visión robótica, ética).", "Corke, P. "));
children.push(bullet("Modern Robotics: Mechanics, Planning, and Control, Cambridge University Press, 2017 — capítulo 1 como lectura complementaria de contexto.", "Lynch, K. M. y Park, F. C. "));

const doc = new Document({
  numbering: numberingConfig,
  styles: { default: { document: { run: { font: F, size: 22 } } } },
  sections: [{ properties: { page: { margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } }, children }],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync("Apuntes_B1_Introduccion_Mecatronica.docx", buf); console.log("OK B1"); });
