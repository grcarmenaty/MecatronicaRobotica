const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, PageBreak, AlignmentType } = require("docx");
const { IQS, F, p, pRuns, h1, h2, bullet, box, tabla, numberingConfig } = require("./lib_iqs");

const children = [];

children.push(
 new Paragraph({ spacing: { before: 2000, after: 200 }, alignment: AlignmentType.CENTER,
 children: [new TextRun({ text: "82514, Mecatrónica y Robótica", size: 44, bold: true, color: IQS.navy, font: F })] }),
 new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 },
 children: [new TextRun({ text: "Checklist de fuentes citadas en los apuntes", size: 30, color: IQS.navy2, font: F })] }),
 new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
 children: [new TextRun({ text: "Qué está ya en la carpeta de Drive y qué conviene añadir", size: 22, color: IQS.grey, font: F })] }),
 new Paragraph({ alignment: AlignmentType.CENTER,
 children: [new TextRun({ text: "Curso 2026/27 · IQS Universitat Ramon Llull", size: 20, color: IQS.grey, font: F })] }),
 new Paragraph({ children: [new PageBreak()] })
);

children.push(h1("1. Cómo usar esta lista"));
children.push(p("Los apuntes de los ocho bloques contienen unas 750 citas con página verificada sobre cinco libros, más un conjunto de fuentes que se citan por designación o identificador y que no tienen paginación en los apuntes: normas, artículos de investigación y documentación oficial de software. Esta lista separa lo que ya tienes de lo que falta, y ordena lo que falta por urgencia real."));
children.push(box("Criterio de urgencia", "Imprescindible significa que sin ese documento no puedes preparar la sesión con rigor. Recomendable significa que el contenido de los apuntes es suficiente para dar la clase, pero tener la fuente mejora tus respuestas a preguntas y te sirve para el seminario. Opcional significa que basta con conocer su existencia: son referencias que los estudiantes pueden querer seguir."));

children.push(h1("2. Ya lo tienes: los cinco libros de la carpeta"));
children.push(p("Estas son las ediciones exactas sobre las que se verificaron las citas con número de página. Si sustituyes alguna edición, las páginas de los apuntes dejarán de corresponder."));
children.push(tabla(
 ["Libro", "Edición citada", "Bloques que lo usan"],
 [
 ["De Silva, C. W. et al., Mechatronics: Fundamentals and Applications", "CRC Press, 2016", "B1, B3, B5, B8"],
 ["Corke, P., Robotics, Vision and Control: Fundamental Algorithms in Python", "3.ª ed., Springer, 2023", "B1, B2, B4, B5, B6, B7"],
 ["Lynch, K. M. y Park, F. C., Modern Robotics", "Cambridge U. Press, 2017", "B2, B4, B5, B7"],
 ["Thrun, S., Burgard, W. y Fox, D., Probabilistic Robotics", "MIT Press, 2005", "B6, B7"],
 ["Fraden, J., Handbook of Modern Sensors", "5.ª ed., Springer, 2016", "B3"],
 ],
 [4700, 1900, 2760]
));

children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("3. Falta: normas técnicas"));
children.push(p("Las normas ISO son de pago y no circulan libremente. La vía habitual es la biblioteca del centro, que suele tener suscripción a AENOR o a la ISO Store; conviene pedirlas con antelación porque la gestión puede tardar. Las tres primeras son las que sostienen la sesión S7 completa."));
children.push(tabla(
 ["Norma", "Para qué se cita", "Sesión", "Urgencia"],
 [
 ["ISO 10218-1:2025", "Requisitos de seguridad del robot como componente: obligaciones del fabricante", "S7", "Imprescindible"],
 ["ISO 10218-2:2025", "Requisitos de la aplicación robótica: obligaciones del integrador y evaluación de riesgos", "S7", "Imprescindible"],
 ["ISO/TS 15066:2016", "Los cuatro métodos de operación colaborativa (cl. 5.5) y los límites biomecánicos por región corporal (anexo A)", "S7", "Imprescindible"],
 ["ISO 12100:2010", "Metodología general de análisis y reducción de riesgos en máquinas: los cinco pasos del taller", "S7", "Recomendable"],
 ["ISO 23247 (serie)", "Marco de gemelos digitales para fabricación", "S40", "Opcional"],
 ["REP 105 (ROS)", "Convención de marcos map → odom → base_link", "S34", "Gratuita (ros.org/reps)"],
 ],
 [1900, 4600, 900, 1960]
));
children.push(box("Atajo si la biblioteca tarda", "Para dar S7 con solvencia bastan las dos ideas que ya están desarrolladas en los apuntes del bloque 2: la división de responsabilidades fabricante/integrador, y que «cobot» no es una categoría de robot sino una propiedad de la aplicación. Lo que realmente necesitas del texto original son los valores numéricos del anexo A de la ISO/TS 15066 si quieres que el taller de análisis de riesgos llegue a cifras concretas."));

children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("4. Falta: artículos de investigación"));
children.push(p("Todos son de acceso libre en arxiv.org: basta con abrir arxiv.org/abs/ seguido del identificador. Descargarlos en una subcarpeta de Drive te deja el bloque 8 y la parte moderna del 6 autocontenidos, y te da el repertorio de artículos validados para el seminario de S41–S42."));

children.push(h2("Percepción y SLAM moderno (bloque 6, sesiones S27 y S31)"));
children.push(tabla(
 ["Identificador", "Artículo", "Por qué se cita"],
 [
 ["arXiv:1512.03385", "He et al., 2015, ResNet", "Conexiones residuales: por qué se pudieron entrenar redes profundas"],
 ["arXiv:1506.02640", "Redmon et al., 2016, YOLO", "Detección en una sola pasada: el estándar práctico en tiempo real"],
 ["arXiv:1506.01497", "Ren et al., 2015, Faster R-CNN", "El linaje alternativo de dos etapas con propuestas de región"],
 ["arXiv:1411.4038", "Long et al., 2014, FCN", "Origen de la segmentación semántica píxel a píxel"],
 ["arXiv:1505.04597", "Ronneberger et al., 2015, U-Net", "Decodificador con conexiones de salto; muy usada fuera de robótica"],
 ["arXiv:1703.06870", "He et al., 2017, Mask R-CNN", "Segmentación de instancias sobre detección"],
 ["arXiv:2010.11929", "Dosovitskiy et al., 2020, ViT", "La convolución deja de ser imprescindible con datos suficientes"],
 ["arXiv:2304.02643", "Kirillov et al., 2023, SAM", "Segmentación fundacional: generaliza sin reentrenar"],
 ["arXiv:1502.00956", "Mur-Artal et al., 2015, ORB-SLAM", "Sistema completo de SLAM visual: la referencia de S31"],
 ["arXiv:2003.08934", "Mildenhall et al., 2020, NeRF", "Campos de radiancia: el panorama de reconstrucción neuronal"],
 ["arXiv:2308.04079", "Kerbl et al., 2023, 3D Gaussian Splatting", "Calidad y tiempo real con primitivas gaussianas explícitas"],
 ],
 [1750, 3150, 4460]
));

children.push(h2("Aprendizaje y modelos fundacionales (bloque 8, sesiones S39 y S40)"));
children.push(tabla(
 ["Identificador", "Artículo", "Por qué se cita"],
 [
 ["arXiv:1707.06347", "Schulman et al., 2017, PPO", "El algoritmo de referencia en RL para robótica"],
 ["arXiv:1502.05477", "Schulman et al., 2015, TRPO", "El antecedente del que PPO simplifica la idea"],
 ["arXiv:1703.06907", "Tobin et al., 2017, Domain randomization", "La técnica base para cruzar la brecha sim-to-real"],
 ["arXiv:1910.07113", "OpenAI, 2019, Destreza manual", "Caso de referencia de aleatorización de dominio a gran escala"],
 ["arXiv:2303.04137", "Chi et al., 2023, Diffusion Policy", "Por qué generar la distribución de acciones y no su media"],
 ["arXiv:2304.13705", "Zhao et al., 2023, ACT / ALOHA", "Imitación bimanual con hardware de bajo coste"],
 ["arXiv:2307.15818", "Brohan et al., 2023, RT-2", "Transferencia de conocimiento web al control robótico"],
 ["arXiv:2406.09246", "Kim et al., 2024, OpenVLA", "La receta VLA abierta y reproducible"],
 ["arXiv:2410.24164", "Black et al., 2024, π0", "Modelo de flujo visión-lenguaje-acción de Physical Intelligence"],
 ["arXiv:2503.14734", "NVIDIA, 2025, GR00T N1", "Modelo fundacional abierto para humanoides generalistas"],
 ],
 [1750, 3150, 4460]
));
children.push(p("Se menciona además AlexNet (Krizhevsky et al., 2012, NeurIPS), que no tiene versión en arXiv, y el informe técnico de Gemini Robotics (Google DeepMind, 2025), que se publica en el blog de investigación de DeepMind y no lleva identificador de arXiv."));

children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("5. Falta: un libro de acceso libre"));
children.push(tabla(
 ["Obra", "Uso en el curso", "Dónde"],
 [
 ["Sutton, R. S. y Barto, A. G., Reinforcement Learning: An Introduction, 2.ª ed., MIT Press, 2018", "Toda la sesión S38 y parte de S39: MDP, política y funciones de valor, Q-learning, gradiente de política. En los apuntes se cita por capítulo (1, 2, 3, 6 y 13), no por página, precisamente porque no estaba en la carpeta", "Los autores publican el PDF completo de forma gratuita en la web de Rich Sutton (incompleteideas.net). Si lo añades a Drive, avísame y convierto las citas por capítulo en citas con página"],
 ],
 [3100, 3400, 2860]
));

children.push(h1("6. No hace falta descargar: documentación en línea"));
children.push(p("Estas fuentes se citan por nombre de sección y se consultan en la web. Son gratuitas y se actualizan, así que descargarlas tiene poco sentido; lo útil es fijar la versión con la que trabajarás y anotarla."));
children.push(tabla(
 ["Fuente", "Qué sostiene", "Bloque"],
 [
 ["docs.ros.org, versión LTS Jazzy Jalisco", "Sesiones S32 y S33 completas y la mitad de S34: nodos, topics, DDS y QoS, servicios, acciones, parámetros, launch, colcon, rclpy y TF2", "B7"],
 ["docs.nav2.org", "Sesión S36 completa: conceptos de navegación, costmaps por capas, behavior trees y AMCL", "B7"],
 ["moveit.picknik.ai", "Sesión S37: move_group, planning scene, OMPL, planificación cartesiana", "B7"],
 ["gazebosim.org y paquete ros_gz", "Segunda mitad de S34: simulación y puente con ROS 2", "B7"],
 ["Robotics Toolbox for Python y spatialmath (petercorke.com)", "Talleres de S13, S15, S16 y S19", "B4"],
 ["python-control (readthedocs)", "Talleres de S21 a S24, en sustitución de Matlab y Simulink", "B5"],
 ["OpenCV", "Talleres de visión de S25 y S26", "B6"],
 ["Gymnasium, MuJoCo, NVIDIA Isaac Lab", "Demostraciones de S39 y S40", "B8"],
 ],
 [3100, 4500, 1760]
));
children.push(box("Sugerencia práctica", "Fija ahora la versión LTS de ROS 2 con la que darás el curso y anótala en el campus virtual: si los estudiantes instalan versiones distintas, el taller de S34 se convierte en una sesión de soporte técnico. El resto de paquetes de Python conviene congelarlos en un fichero de requisitos único para toda la asignatura."));

children.push(h1("7. Resumen de lo que hay que conseguir"));
children.push(bullet("las cuatro normas de seguridad (ISO 10218-1 y -2:2025, ISO/TS 15066:2016, ISO 12100:2010) por vía de biblioteca, con margen porque la gestión tarda. Sostienen la sesión S7.", "Con antelación: "));
children.push(bullet("los veintiún artículos de arXiv, en una subcarpeta de la carpeta Mecatronica. Son gratuitos, se descargan en una sesión y dejan autocontenidos el bloque 8 y la parte moderna del 6.", "Cuando tengas un rato: "));
children.push(bullet("el PDF gratuito de Sutton y Barto (2018). Es lo único que convertiría citas por capítulo en citas con página.", "Fácil y con recompensa: "));
children.push(bullet("la ISO 23247 de gemelos digitales, que solo se menciona de pasada en S40.", "Puede esperar: "));
children.push(p("Si añades material a la carpeta, dímelo y actualizo los apuntes afectados: con Sutton y Barto puedo pasar las citas del bloque 8 de capítulo a página, y con las normas puedo incorporar los valores concretos del anexo A al taller de análisis de riesgos de S7."));

const doc = new Document({
 numbering: numberingConfig,
 styles: { default: { document: { run: { font: F, size: 22 } } } },
 sections: [{ properties: { page: { margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } }, children }],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync("Checklist_Fuentes_82514.docx", buf); console.log("OK checklist"); });
