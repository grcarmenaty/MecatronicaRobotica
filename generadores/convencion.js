// Convención terminológica del curso 82514: fuentes, reglas y tabla de términos.
const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, PageBreak, AlignmentType, ImageRun } = require("docx");
const { IQS, F, p, pRuns, h1, h2, bullet, box, tabla, numberingConfig } = require("./lib_iqs");

const LOGO = fs.readFileSync("media/logo_iqs_color.png");
const C = [];

C.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 300, after: 200 }, children: [new ImageRun({ type: "png", data: LOGO, transformation: { width: 190, height: 145 } })] }));
C.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({ text: "82514 · Mecatrónica y Robótica", size: 40, bold: true, color: IQS.navy, font: F })] }));
C.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 400 }, children: [new TextRun({ text: "Convención terminológica del curso · Traducción de términos de robótica", size: 26, color: IQS.navy2, font: F })] }));

C.push(h1("1. La duda concreta: ¿«pose» o «posición»?"));
C.push(p("«Pose» no es un anglicismo gratuito: es un término técnico con significado propio que «posición» no cubre. La pose de un cuerpo rígido es el conjunto de su posición (dónde está: tres coordenadas) y su orientación (hacia dónde mira: tres grados de libertad más). Decir «posición» cuando hay orientación en juego sería técnicamente incorrecto: la cinemática directa de un manipulador no devuelve solo una posición, devuelve una pose; la repetibilidad de catálogo de un robot es repetibilidad de pose; y lo que estima la localización de un robot móvil es su pose (x, y, θ). Esta es exactamente la definición del vocabulario internacional de robótica, la norma ISO 8373 (Robotics. Vocabulary), que define pose como la combinación de posición y orientación."));
C.push(p("En castellano conviven dos soluciones. La escuela clásica española (Barrientos, Peñín, Balaguer y Aracil, Fundamentos de robótica, McGraw-Hill) usa «localización» para el conjunto posición más orientación. La literatura actual en español (revistas como RIAI, tesis doctorales, cursos de SLAM y visión) usa «pose» de forma generalizada. En esta asignatura se usa «pose», por dos motivos: primero, es el uso vivo que los estudiantes encontrarán en la bibliografía y en la profesión; segundo, y decisivo aquí, «localización» ya está ocupada en el propio curso: en el bloque 6 significa el problema de localization (estimar dónde está el robot en un mapa, con EKF y filtro de partículas). Usar la misma palabra para dos conceptos distintos en la misma asignatura sería una fuente segura de confusión. La palabra «postura» tampoco sirve como sustituto: en el curso (y en la literatura de manipulabilidad) se reserva para la configuración articular q del robot."));
C.push(box("Regla del curso", "Pose = posición + orientación (se define así en su primera aparición, bloque 4, y se mantiene en todo el material). Posición = solo las coordenadas de traslación. Postura o configuración = el vector articular q. Localización = el problema de estimar la pose en un mapa (bloque 6)."));

C.push(h1("2. Dónde encontrar convenciones de traducción"));
C.push(p("No existe hoy una norma española vigente de vocabulario de robótica: la adopción española UNE-EN ISO 8373:1998 (Robots manipuladores industriales. Vocabulario) fue anulada en 2012 y las ediciones posteriores de la ISO 8373 (la vigente es de 2021, en revisión) no tienen versión oficial en español, solo inglesa y francesa. En la práctica, la convención se construye con esta jerarquía de fuentes:"));
C.push(bullet("el vocabulario oficial de la disciplina, consultable término a término (gratis) en la Online Browsing Platform de ISO. Su última versión española es la UNE-EN ISO 8373:1998, útil todavía como referencia histórica de traducciones (efector final, espacio de trabajo, repetibilidad de pose...). Las normas las elabora el comité ISO/TC 299 y en España el CTN 116 de UNE.", "ISO 8373 (Robotics. Vocabulary): "));
C.push(bullet("el Vocabulario Electrotécnico Internacional (IEV) de la IEC, en electropedia.org, tiene traducción española oficial de miles de términos de sensores, máquinas eléctricas, control y automática (transductor, servomecanismo, realimentación...). Es la mejor fuente normativa gratuita en español para la mitad eléctrica del curso.", "IEC Electropedia: "));
C.push(bullet("Barrientos, Peñín, Balaguer y Aracil, Fundamentos de robótica (2.ª ed., McGraw-Hill) y Ollero, Robótica: manipuladores y robots móviles (Marcombo) fijaron el español académico del área: articulación, eslabón, elemento terminal, localización, muñeca, cinemática directa e inversa. Cuando dudes de un término de manipuladores, mira cómo lo llama Barrientos.", "Los libros canónicos en español: "));
C.push(bullet("la Revista Iberoamericana de Automática e Informática Industrial (RIAI, del comité español de automática CEA) y las tesis de las escuelas de ingeniería muestran el uso real actual: ahí «pose», «cierre de bucle» o «mapa de ocupación» están completamente asentados.", "El uso vivo revisado por pares: "));
C.push(bullet("para el español general (mayúsculas, extranjerismos, siglas), RAE y FundéuRAE. No cubren el tecnicismo robótico, pero resuelven el resto.", "RAE y FundéuRAE: "));

C.push(h1("3. Reglas de traducción del curso"));
C.push(bullet("Se traduce el concepto cuando existe término español asentado: espacio de trabajo, realimentación, muestreo, cierre de bucle, aleatorización de dominio, gemelo digital."));
C.push(bullet("En la primera aparición de un término traducido poco obvio se añade el original entre paréntesis: torsor (wrench), holgura (backlash), prealimentación (feedforward), clonación de comportamiento (behavior cloning)."));
C.push(bullet("Se mantienen en inglés, en cursiva conceptual, los términos sin traducción asentada cuya versión española nadie usa en la práctica: windup (con su explicación), aliasing (existe «solapamiento», se anota), pick and place, log-odds."));
C.push(bullet("Los identificadores de software, comandos y nombres de API no se traducen nunca (topic, launch file, colcon, jacob0, teach, RViz); los conceptos que representan sí (nodo, servicio, acción, parámetro)."));
C.push(bullet("Siglas internacionales invariables: SLAM, EKF, MCL, PID, IMU, AGV, AMR, VLA, MDP, DH, PoE."));

C.push(new Paragraph({ children: [new PageBreak()] }));
C.push(h1("4. Tabla de convención término a término"));
const filas = [
 ["pose", "pose", "Posición + orientación (ISO 8373). No confundir con posición, postura (= configuración q) ni localización (= localization, B6)"],
 ["position / orientation", "posición / orientación", "Traducción directa"],
 ["configuration / posture", "configuración, postura", "El vector articular q"],
 ["localization", "localización", "Estimar la pose en un mapa (B6). Reservada para este uso"],
 ["end effector", "efector (final)", "UNE-EN ISO 8373:1998: «efector final». Barrientos: «elemento terminal». El curso abrevia a «efector»"],
 ["workspace", "espacio de trabajo", "Alcanzable frente a diestro"],
 ["joint / link", "articulación / eslabón", "Convención universal en español"],
 ["wrist / elbow / shoulder", "muñeca / codo / hombro", "Muñeca esférica, codo arriba/abajo"],
 ["gripper", "pinza", "También «garra» en parte de la literatura"],
 ["forward / inverse kinematics", "cinemática directa / inversa", "FK/IK como siglas admitidas"],
 ["jacobian", "jacobiano", "Masculino en la literatura española de robótica"],
 ["singularity / manipulability", "singularidad / manipulabilidad", "Elipsoide de manipulabilidad"],
 ["wrench", "torsor (wrench)", "Término clásico de la mecánica española para el par fuerza-momento. Corregido en el curso (antes «llave»)"],
 ["screw axis", "eje helicoidal", "Del producto de exponenciales. Corregido (antes «eje de husillo»; husillo se reserva para el elemento mecánico)"],
 ["twist", "velocidad espacial (twist)", "El vector 6D de velocidades lineal y angular"],
 ["gimbal lock", "bloqueo de cardán", "Asentado en español"],
 ["quaternion", "cuaternión", "Plural: cuaterniones"],
 ["trajectory / path", "trayectoria / camino", "Trayectoria = camino + ley temporal"],
 ["payload", "carga útil", "Traducción directa"],
 ["backlash", "holgura (backlash)", "Original entre paréntesis en primera aparición"],
 ["encoder", "encoder", "«Codificador» existe (IEV) pero la industria usa encoder; se mantiene"],
 ["strain gauge", "galga extensométrica", "Término normalizado"],
 ["back-EMF", "fuerza contraelectromotriz (back-EMF)", "Término IEV; la sigla inglesa se anota por su ubicuidad"],
 ["feedback / feedforward", "realimentación / prealimentación (feedforward)", "IEV: realimentación. Feedforward se anota porque domina en la práctica"],
 ["setpoint / reference", "consigna / referencia", "Ambas usadas; consigna en contexto industrial"],
 ["overshoot", "sobreoscilación", "En Hispanoamérica: sobrepaso o sobreimpulso; se anota en el aula"],
 ["settling / rise time", "tiempo de establecimiento / de subida", "Traducción directa"],
 ["steady-state error", "error estacionario", "También «error en régimen permanente»"],
 ["windup", "windup (saturación del integrador)", "Sin traducción asentada; se explica siempre"],
 ["sampling / aliasing", "muestreo / aliasing", "«Solapamiento» existe para aliasing; se anota y se mantiene el inglés por uso"],
 ["belief / likelihood", "creencia / verosimilitud", "Estándar en la literatura bayesiana en español"],
 ["particle filter / resampling", "filtro de partículas / remuestreo", "Traducción directa"],
 ["loop closure", "cierre de bucle", "SLAM; asentado en español"],
 ["occupancy grid / costmap", "mapa de ocupación / mapa de coste", "costmap se conserva al citar la API de Nav2"],
 ["sampling-based planner", "planificador de muestreo", "PRM, RRT"],
 ["reinforcement learning / reward / policy", "aprendizaje por refuerzo / recompensa / política", "Traducción directa"],
 ["behavior cloning", "clonación de comportamiento (behavior cloning)", "Corregido en el curso (antes «clonado»)"],
 ["domain randomization", "aleatorización de dominio", "Traducción directa"],
 ["digital twin", "gemelo digital", "Asentado (marco ISO 23247)"],
 ["cobot / collaborative robot", "cobot, robot colaborativo", "Recordar que no es una categoría legal (B2)"],
 ["node / topic / service / action", "nodo / topic / servicio / acción", "topic se conserva por ser identificador de la API de ROS 2"],
 ["robot cell", "célula robotizada", "En España, célula; «celda» es frecuente en Hispanoamérica. Unificado a célula"],
];
C.push(tabla(["Inglés", "Término del curso", "Nota y fuente"], filas, [2300, 2900, 4160]));

C.push(h1("5. Correcciones aplicadas al material"));
C.push(p("Tras esta revisión se han corregido en todos los documentos (apuntes, presentaciones, guía del profesor y exámenes): «llave / llave de fuerza» pasa a «torsor (wrench)»; «eje de husillo» pasa a «eje helicoidal» (además evita el choque con el husillo mecánico del ejercicio de vibraciones de S8); «clonado de comportamiento» pasa a «clonación de comportamiento»; y «celda» se unifica con «célula robotizada». El término «pose» se mantiene deliberadamente con su definición en la primera aparición, por las razones del apartado 1."));

const doc = new Document({
  numbering: numberingConfig,
  styles: { default: { document: { run: { font: F, size: 22 } } } },
  sections: [{ properties: { page: { margin: { top: 1200, bottom: 1200, left: 1350, right: 1350 } } }, children: C }],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync("Convencion_Terminologica_82514.docx", buf); console.log("OK convencion"); });
