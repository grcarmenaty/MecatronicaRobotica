const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, PageBreak, AlignmentType } = require("docx");
const { IQS, F, p, pRuns, h1, h2, h3, bullet, box, tabla, tablaTiempos, numberingConfig } = require("./lib_iqs");

const children = [];

// ---------- Portada ----------
children.push(
  new Paragraph({ spacing: { before: 2000, after: 200 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "Bloque 2", size: 40, bold: true, color: IQS.greenDark, font: F })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
    children: [new TextRun({ text: "Tipología de robots, cobots y humanoides. Seguridad y normativa", size: 44, bold: true, color: IQS.navy, font: F })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
    children: [new TextRun({ text: "82514 — Mecatrónica y Robótica · IQS Universitat Ramon Llull", size: 24, color: IQS.grey, font: F })] }),
  new Paragraph({ alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "Apuntes del profesor · Sesiones S5–S7 (18, 23 y 25 de septiembre de 2026) · 5 horas", size: 22, color: IQS.grey, font: F })] }),
  new Paragraph({ children: [new PageBreak()] })
);

children.push(h1("Objetivos de aprendizaje del bloque"));
children.push(bullet("Clasificar cualquier robot según las dos taxonomías de referencia (movilidad y función) y describir las configuraciones cinemáticas de manipuladores y sus espacios de trabajo."));
children.push(bullet("Comparar las arquitecturas de locomoción de robots móviles y distinguir AGV de AMR."));
children.push(bullet("Explicar el marco normativo de seguridad para robots industriales y colaborativos (ISO 10218:2025, ISO/TS 15066) y los cuatro métodos de operación colaborativa."));
children.push(bullet("Esbozar un análisis de riesgos de una célula robotizada sencilla."));
children.push(box("Materiales del bloque", "Presentación B2 (IQS_B2_Tipologia_Seguridad.pptx). Lecturas: Corke, RVC3 cap. 1 (tipos de robots); normativa ISO 10218:2025 (resumen del profesor incluido en estos apuntes). Los robots Mitsubishi y ABB del laboratorio sirven de ejemplo transversal."));

// ============ SESIÓN 5 ============
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("Sesión S5 (vie 18 sep, 2 h) — Taxonomía de robots y configuraciones"));
children.push(h2("Estructura de la clase"));
children.push(tablaTiempos([
  ["0–10 min", "Recuperación del bloque 1", "Repaso breve del cuestionario de S4: comentar los errores más comunes."],
  ["10–35 min", "Teoría: taxonomías", "Apartado 5.1. Proyectar fotos y pedir a la clase que clasifique cada robot antes de dar la respuesta."],
  ["35–65 min", "Teoría: configuraciones de manipuladores", "Apartado 5.2. Dibujar cada configuración con su espacio de trabajo; conectar con los robots del laboratorio (antropomórficos de 6 ejes)."],
  ["65–75 min", "Descanso", "—"],
  ["75–95 min", "Teoría: grados de autonomía", "Apartado 5.3. Retomar traded/shared control de S3 y formalizar el espectro."],
  ["95–115 min", "Actividad en equipos", "Cada equipo recibe 6 fichas de robots reales (industrial, cobot, AMR, humanoide, quirúrgico, dron) y debe clasificarlos en ambas taxonomías, identificar configuración y grado de autonomía. Puesta en común."],
  ["115–120 min", "Cierre", "Formación de equipos del proyecto integrador (quedará cerrada en S7)."],
]));

children.push(h2("5.1. Dos taxonomías complementarias"));
children.push(p("Corke propone clasificar los robots con dos ejes complementarios. Por movilidad: los robots de primera generación estaban fijos en su emplazamiento, mientras que los robots móviles se desplazan por el mundo mediante ruedas o patas en tierra, alas fijas o rotores en el aire, o desplazándose por o sobre el agua. Por función: los robots de fabricación (manufacturing robots) operan en fábricas y son los descendientes directos de los Unimate; los robots de servicio prestan servicios a personas —limpieza, cuidado personal, rehabilitación, transporte de objetos—; los robots de campo (field robots) trabajan a la intemperie en monitorización ambiental, agricultura, minería, construcción o silvicultura; y los robots humanoides tienen forma humana y son, señala Corke, a la vez robots móviles y de servicio: las categorías no son excluyentes."));
children.push(p("La definición de robot de fabricación de Corke encierra la clave económica del sector: es típicamente un manipulador de tipo brazo sobre base fija que realiza tareas repetitivas dentro de una célula de trabajo local, donde las piezas se le presentan de forma ordenada, maximizando la ventaja de su alta velocidad y precisión. Velocidad y precisión implican peligro: la seguridad se logra tradicionalmente excluyendo a las personas del espacio de trabajo —el robot vive en una jaula. Los robots colaborativos (cobots) invierten el planteamiento: son seguros para el ser humano porque operan a baja velocidad y se detienen ante una obstrucción. Esa diferencia, que en S7 convertiremos en normativa, es también una diferencia de filosofía de diseño mecatrónico: el cobot sustituye vallado por sensórica, limitación de potencia y control."));
children.push(p("Los robots de campo y servicio afrontan dos retos específicos que los de fábrica no tienen: operar en un entorno complejo, desordenado y cambiante (el robot de reparto hospitalario entre camillas y personas; el rover marciano sin mapa preciso), y hacerlo con seguridad en presencia de personas —el robot de reparto circula entre ellas, el coche autónomo las lleva dentro, y el robot quirúrgico opera dentro de ellas. Esta escalera de intimidad física es un buen recurso para que los estudiantes interioricen por qué percepción y seguridad dominan la robótica moderna."));

children.push(h2("5.2. Configuraciones cinemáticas de manipuladores"));
children.push(p("Un manipulador es una cadena de eslabones unidos por articulaciones rotativas (R) o prismáticas (P). La secuencia de los tres primeros ejes —los que posicionan la muñeca— define la configuración y la forma del espacio de trabajo:"));
children.push(bullet("tres ejes prismáticos (PPP). Espacio de trabajo en forma de caja, rigidez alta, cinemática trivial. Típico de pórticos de paletizado y máquinas de medición.", "Cartesiano: "));
children.push(bullet("dos rotativas y una prismática (RRP) con ejes rotativos verticales. Rígido en vertical y ágil en el plano: el estándar del ensamblado electrónico de alta velocidad (pick and place).", "SCARA: "));
children.push(bullet("RPP. Espacio de trabajo cilíndrico; hoy es una configuración minoritaria.", "Cilíndrico: "));
children.push(bullet("RRP con muñeca esférica; espacio de trabajo esférico. El Unimate original y el Stanford Arm eran esféricos.", "Esférico: "));
children.push(bullet("seis ejes rotativos (el estándar industrial: los Mitsubishi y ABB del laboratorio). Máxima destreza y espacio de trabajo casi esférico a costa de cinemática y dinámica más complejas: es la configuración que usaremos en el bloque 4.", "Articulado o antropomórfico: "));
children.push(bullet("la base y la plataforma están unidas por varias cadenas cinemáticas cerradas (ejemplo: robot delta). Poca inercia móvil, altísima velocidad y rigidez, espacio de trabajo pequeño: envasado y pick and place alimentario.", "Paralelo: "));
children.push(p("Conceptos asociados que hay que dejar definidos porque reaparecen en el bloque 4: grados de libertad (número de coordenadas independientes; seis para pose arbitraria en el espacio), espacio de trabajo alcanzable frente a espacio diestro (donde el efector alcanza cualquier orientación), repetibilidad (dispersión al volver al mismo punto programado, la especificación estrella de catálogo, típicamente ±0,01–0,05 mm en robots industriales) frente a exactitud (error respecto a una pose absoluta ordenada, generalmente peor y relevante en programación fuera de línea)."));

children.push(h2("5.3. El espectro de autonomía"));
children.push(p("Formalizamos lo visto en S3 como un espectro con cuatro escalones: teleoperación pura (el humano controla todo; el telerobot ejecuta: ROV, cirugía robótica), control alternado o traded control (humano y computador se pasan el control: piloto automático), control compartido o shared control (ambos a la vez: mantenimiento de carril con conductor gestionando velocidad) y autonomía supervisada (el robot decide localmente y el humano fija objetivos de alto nivel: rovers marcianos, AMR de almacén). Preguntas útiles: ¿dónde colocamos un dron de carreras FPV?, ¿y un taxi autónomo comercial?, ¿y el brazo del laboratorio ejecutando un programa? Esta última incomoda productivamente: un robot industrial clásico ni percibe ni planifica —ejecuta—, y por eso algunos autores lo consideran «solo» automatización programable; la definición sense-plan-act es una vara de medir, no una frontera nítida."));

// ============ SESIÓN 6 ============
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("Sesión S6 (mié 23 sep, 1 h) — Robots móviles"));
children.push(h2("Estructura de la clase"));
children.push(tablaTiempos([
  ["0–5 min", "Recuperación", "Configuraciones de manipuladores: pedir que dibujen SCARA y articulado con sus espacios de trabajo."],
  ["5–25 min", "Teoría: locomoción con ruedas", "Apartado 6.1. Dibujar cada arquitectura y sus restricciones de movimiento."],
  ["25–40 min", "Teoría: AGV frente a AMR; patas y aire", "Apartados 6.2 y 6.3."],
  ["40–55 min", "Ejercicio guiado", "Elegir plataforma para tres escenarios (almacén, hospital, viña) justificando locomoción, sensórica y autonomía."],
  ["55–60 min", "Cierre", "Anunciar S7 (seguridad, 2 h) y recordar el cierre de equipos del proyecto."],
]));

children.push(h2("6.1. Locomoción con ruedas"));
children.push(p("La rueda es el mecanismo de locomoción más eficiente sobre superficie preparada, y la arquitectura de tracción determina la maniobrabilidad. Tracción diferencial: dos ruedas motrices independientes más apoyos locos; gira sobre sí misma; es la arquitectura de la mayoría de AMR y robots educativos, y su modelo cinemático —que derivaremos en el bloque 4— es el más simple. Triciclo y Ackermann: dirección en las ruedas delanteras como un coche; no puede girar sobre sí mismo y tiene radio de giro mínimo, pero es estable a velocidad; su restricción no holonómica (no puede desplazarse lateralmente) condicionará la planificación en el bloque 7. Omnidireccional: ruedas suecas (mecanum) o esféricas que permiten trasladarse en cualquier dirección y rotar simultáneamente —holonómico—, a cambio de sensibilidad al estado del suelo y menor capacidad de carga. Orugas: tracción sobre terreno suelto, giro por deslizamiento (skid-steer) que castiga la odometría."));

children.push(h2("6.2. AGV frente a AMR"));
children.push(p("La distinción industrial clave del momento. El AGV (Automated Guided Vehicle) sigue infraestructura física —filoguiado, banda magnética, balizas reflectantes— y se detiene ante cualquier obstáculo: ruta fija, entorno adaptado al vehículo. El AMR (Autonomous Mobile Robot) navega con un mapa que él mismo construye y mantiene (SLAM, bloque 6), planifica rutas y rodea obstáculos: el vehículo se adapta al entorno. La transición AGV→AMR resume treinta años de progreso en percepción y es el ejemplo perfecto de valor añadido por software: el hardware (chasis diferencial, LiDAR) es casi el mismo; la diferencia es el stack de navegación que veremos con Nav2 en el bloque 7."));

children.push(h2("6.3. Patas, aire y agua"));
children.push(p("Las patas ganan donde las ruedas pierden: escaleras, escombros, terreno discontinuo. El coste es complejidad: equilibrio dinámico, muchas articulaciones actuadas y consumo. Los cuadrúpedos comerciales (inspección industrial) y los humanoides bípedos (logística, pilotos en fábricas desde 2024–2026) son el segmento de mayor crecimiento; su viabilidad reciente se debe tanto a actuadores y baterías como al aprendizaje por refuerzo aplicado a la locomoción, que veremos en el bloque 8. En el aire, los multirrotores dominan por simplicidad mecánica y vuelo estacionario (inspección, agricultura, reparto), con el ala fija reservada a la cobertura de área; bajo el agua, los ROV teleoperados y los AUV autónomos completan el mapa. Todos comparten la misma anatomía sense-plan-act con sensórica distinta: IMU y GNSS fuera, presión y sonar debajo del agua, LiDAR y cámaras en interiores."));

// ============ SESIÓN 7 ============
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("Sesión S7 (vie 25 sep, 2 h) — Cobots, seguridad y normativa"));
children.push(h2("Estructura de la clase"));
children.push(tablaTiempos([
  ["0–10 min", "Recuperación", "AGV frente a AMR; arquitecturas de locomoción."],
  ["10–40 min", "Teoría: marco normativo", "Apartado 7.1. No memorizar números de cláusula: entender la arquitectura de la norma y quién es responsable de qué."],
  ["40–70 min", "Teoría: los cuatro métodos colaborativos", "Apartado 7.2. Vídeos cortos de cada método; los estudiantes deben identificar cuál es cuál."],
  ["70–80 min", "Descanso", "—"],
  ["80–110 min", "Taller: análisis de riesgos", "Apartado 7.3. En equipos: análisis de riesgos simplificado de una célula con el robot ABB del laboratorio y carga/descarga manual de piezas. Plantilla en la presentación."],
  ["110–120 min", "Cierre del bloque", "Cuestionario de seguimiento B2 + cierre de equipos del proyecto integrador."],
]));

children.push(h2("7.1. El marco normativo: ISO 10218:2025"));
children.push(p("La seguridad de robots industriales se rige por la norma ISO 10218 «Robotics — Safety requirements», profundamente revisada en 2025. La norma tiene dos partes: la parte 1 se dirige al fabricante del robot (requisitos del robot como componente: paradas de seguridad, límites de eje, modos de operación) y la parte 2 al integrador de la célula o aplicación robótica (requisitos del sistema completo: layout, resguardos, dispositivos de protección, validación). Esta división de responsabilidades es el concepto más importante para un futuro ingeniero: comprar un robot «seguro» no hace segura la célula; la seguridad es una propiedad de la aplicación integrada, y el integrador —el papel que muchos de vuestros estudiantes desempeñarán— es legalmente responsable de la evaluación de riesgos."));
children.push(p("La revisión de 2025 integró en la propia ISO 10218 los requisitos de operación colaborativa que antes vivían en la especificación técnica ISO/TS 15066 (2016), que sigue siendo la referencia para los valores límite biomecánicos (umbrales de fuerza y presión admisibles por región corporal en caso de contacto). Mensaje clave: «cobot» no es una categoría legal de robot, sino una aplicación colaborativa; un brazo de fuerza limitada mal integrado (por ejemplo, con una herramienta cortante) no es una aplicación colaborativa segura, y un robot industrial clásico puede participar en una aplicación colaborativa si la célula lo permite con las salvaguardas adecuadas."));

children.push(h2("7.2. Los cuatro métodos de operación colaborativa"));
children.push(bullet("el robot se detiene (con categoría de parada segura) cuando una persona entra en el espacio colaborativo y reanuda cuando sale. Es el método más simple: colaboración por turnos.", "Parada monitorizada de seguridad (safety-rated monitored stop): "));
children.push(bullet("el operador mueve el robot guiándolo físicamente, con el robot compensando su propio peso. Uso típico: programación por demostración y manipulación asistida de cargas.", "Guiado manual (hand guiding): "));
children.push(bullet("el sistema monitoriza en tiempo real la distancia entre robot y persona y modula la velocidad (hasta detenerse) para que nunca sea posible el contacto. Requiere sensórica de seguridad certificada (escáneres láser, visión de seguridad) y es la base de las células sin vallado con robots rápidos.", "Monitorización de velocidad y separación (speed and separation monitoring): "));
children.push(bullet("se admite el contacto físico, pero el robot limita fuerza, par y presión por debajo de los umbrales biomecánicos de ISO/TS 15066 para cada región corporal. Es el método que popularizaron los cobots (Universal Robots y similares) con medición de par en las articulaciones.", "Limitación de potencia y fuerza (power and force limiting): "));
children.push(p("Conviene insistir en que los métodos se combinan: una célula real puede usar monitorización de velocidad y separación en aproximación y limitación de fuerza en la zona de entrega de piezas. Y en que la velocidad reducida tiene coste de productividad: elegir método colaborativo es una decisión de diseño mecatrónico con variables técnicas, económicas y humanas —el MDQ del bloque 1 reaparece."));

children.push(h2("7.3. Análisis de riesgos de una célula robotizada"));
children.push(p("El proceso que exige la norma (alineado con ISO 12100, la norma madre de seguridad de máquinas) se resume en cinco pasos que los equipos aplicarán en el taller: (1) determinar los límites de la aplicación: espacio, tareas, quién interactúa y cómo; (2) identificar los peligros por tarea —atrapamiento, impacto, aplastamiento, herramienta, pieza proyectada— incluyendo los modos degradados (limpieza, mantenimiento, recuperación de fallos, que concentran los accidentes reales); (3) estimar el riesgo de cada peligro (severidad del daño y probabilidad de que ocurra: exposición, suceso peligroso y posibilidad de evitar o limitar el daño); (4) reducir el riesgo siguiendo la jerarquía: eliminar por diseño, proteger con resguardos y dispositivos, informar con señalización y formación —en ese orden—; (5) validar que las medidas funcionan y documentarlo. El entregable del taller es una tabla de riesgos de seis filas sobre la célula propuesta; corregirla en común es la mejor síntesis del bloque."));
children.push(box("Conexión con el laboratorio", "En las prácticas con los robots Mitsubishi y ABB, la primera sesión incluye las normas de seguridad del aula-taller. Estos apuntes dan el marco conceptual; las normas concretas del laboratorio (ya establecidas) son de obligado cumplimiento y no se modifican en esta programación."));

// Bibliografía
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("Bibliografía del bloque"));
children.push(bullet("Robotics, Vision and Control: Fundamental Algorithms in Python, 3.ª ed., Springer, 2023 — capítulo 1, sección 1.2 (tipos de robots).", "Corke, P. "));
children.push(bullet("ISO 10218-1:2025 e ISO 10218-2:2025, Robotics — Safety requirements. Consultar el resumen de cambios publicado por los organismos de normalización; el texto íntegro está disponible a través de la biblioteca.", "ISO: "));
children.push(bullet("ISO/TS 15066:2016, Robots and robotic devices — Collaborative robots (valores límite biomecánicos).", "ISO: "));
children.push(bullet("Modern Robotics, Cambridge, 2017 — capítulo 2 (grados de libertad y espacios de configuración) como preparación del bloque 4.", "Lynch, K. M. y Park, F. C. "));

const doc = new Document({
  numbering: numberingConfig,
  styles: { default: { document: { run: { font: F, size: 22 } } } },
  sections: [{ properties: { page: { margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } }, children }],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync("Apuntes_B2_Tipologia_Seguridad.docx", buf); console.log("OK B2"); });
