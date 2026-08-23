const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, PageBreak, AlignmentType } = require("docx");
const { IQS, F, p, pRuns, h1, h2, bullet, box, tabla, numberingConfig } = require("./lib_iqs");

const children = [];

children.push(
 new Paragraph({ spacing: { before: 2000, after: 200 }, alignment: AlignmentType.CENTER,
 children: [new TextRun({ text: "82514, Mecatrónica y Robótica", size: 44, bold: true, color: IQS.navy, font: F })] }),
 new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 },
 children: [new TextRun({ text: "Informe de verificación de las citas de los apuntes", size: 30, color: IQS.navy2, font: F })] }),
 new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
 children: [new TextRun({ text: "992 citas comprobadas contra el texto de los cinco libros de la carpeta de bibliografía", size: 22, color: IQS.grey, font: F })] }),
 new Paragraph({ alignment: AlignmentType.CENTER,
 children: [new TextRun({ text: "Curso 2026/27 · IQS Universitat Ramon Llull", size: 20, color: IQS.grey, font: F })] }),
 new Paragraph({ children: [new PageBreak()] })
);

children.push(h1("1. Resultado"));
children.push(p("Se han comprobado las 992 citas con número de página que contienen los ocho documentos de apuntes. El resultado es que no hay ninguna página equivocada: todas las referencias apuntan a la página del libro donde efectivamente está el contenido que se afirma. Se han corregido dos atribuciones imprecisas, ambas en el bloque 6, que se detallan en el apartado 4."));
children.push(tabla(
 ["Resultado", "Citas", "Cómo se resolvió"],
 [
 ["Confirmadas automáticamente", "655", "Se localizaron en la página citada los anclajes de la afirmación: nombres propios, acrónimos, números de figura o ecuación y términos técnicos"],
 ["Sin término comprobable, corroboradas", "223", "La afirmación era demasiado breve para extraer anclajes, pero otra cita distinta a la misma página sí quedó confirmada"],
 ["Sin término comprobable, revisadas a mano", "77", "Se abrió cada una de las 46 páginas y se comprobó que su encabezado de sección corresponde al tema citado"],
 ["Marcadas como dudosas por el detector", "37", "Revisadas una a una: 35 resultaron correctas y 2 imprecisas (apartado 4)"],
 ],
 [3300, 900, 5160]
));

children.push(h2("Reparto por libro y por bloque"));
children.push(tabla(
 ["Libro", "Citas"],
 [
 ["Corke (2023), Robotics, Vision and Control, 3.ª ed. Python", "459"],
 ["Lynch y Park (2017), Modern Robotics", "214"],
 ["De Silva et al. (2016), Mechatronics", "111"],
 ["Fraden (2016), Handbook of Modern Sensors, 5.ª ed.", "105"],
 ["Thrun, Burgard y Fox (2005), Probabilistic Robotics", "103"],
 ],
 [6660, 2700]
));
children.push(tabla(
 ["Bloque", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8"],
 [["Citas", "88", "74", "202", "238", "140", "172", "77", "1"]],
 [1500, 985, 985, 985, 985, 985, 985, 985, 965]
));
children.push(p("El bloque 8 tiene una sola cita con página porque sus fuentes son artículos de arXiv y el libro de Sutton y Barto, que se cita por capítulo al no estar todavía en la carpeta de bibliografía."));

children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("2. Método"));
children.push(p("El problema de fondo es que los libros están en la carpeta partidos en varios PDF, de modo que el número de página del libro no coincide con el número de página del fichero. Fiarse de un desplazamiento fijo es frágil: el prólogo con numeración romana, las páginas en blanco y los saltos de capítulo lo desvían."));
children.push(p("Por eso el primer paso fue construir, para cada uno de los diecinueve ficheros, un índice de número impreso a página del PDF, leyendo el número que aparece en la cabecera o el pie de cada página. Con ese índice, una cita a la página 254 de Corke se resuelve a la página que lleva impreso el 254, no a la que caería por aritmética. Como red de seguridad, cada consulta busca también por desplazamiento lineal en una ventana de dos páginas arriba y abajo."));
children.push(p("El segundo paso fue extraer de cada afirmación en español sus anclajes: nombres propios y acrónimos, que se escriben igual en ambos idiomas (Kalman, RRT, SCARA, PUMA, Denavit, Ziegler); números de figura, tabla y ecuación; y unos doscientos cincuenta términos técnicos con su raíz en inglés. Una cita se da por confirmada cuando al menos uno de esos anclajes aparece en la página citada."));
children.push(box("Un fallo del propio verificador que conviene conocer", "La primera versión no entendía las citas compuestas del tipo «(Corke, 2023, p. 324; Lynch y Park, 2017, p. 190)»: leía el primer autor con la última página y generaba falsos errores. Corregido esto, el número de citas analizadas pasó de 829 a 992, porque cada referencia dentro de un mismo paréntesis se cuenta y se comprueba por separado."));

children.push(h1("3. Los 37 avisos del detector, uno a uno"));
children.push(p("Ninguno de los avisos era un número de página equivocado. Estas son las causas reales, útiles porque explican qué tipo de comprobación automática no funciona con este material:"));
children.push(bullet("el PDF de Thrun escribe «Kalman_ﬁlter» y «Particle_ﬁlter» con el ligado tipográfico fi, que no coincide con la búsqueda de «filter». Ambas páginas, la 42 y la 98, contienen exactamente el algoritmo que se cita.", "Ligados tipográficos: "));
children.push(bullet("la frase citada de De Silva sobre la conversión analógico-digital está partida entre dos líneas en la página 147, de modo que no se encuentra como cadena continua. La página es la correcta.", "Frases partidas por el salto de línea: "));
children.push(bullet("«cuadratura», «modelo», «puerta» o «bloqueo de cardán» no estaban en el diccionario de doscientos cincuenta términos. Las páginas 310 de Fraden, 3 de De Silva y 53 de Corke son correctas.", "Términos ausentes del diccionario: "));
children.push(bullet("una afirmación citada a las páginas 231 y 232 de Lynch y Park tiene el ejemplo en la 231 y las tolerancias numéricas en la 232; el detector solo miraba la primera. El rango citado es correcto.", "Citas a un rango de páginas: "));
children.push(p("Se comprobaron además a mano las citas con datos numéricos concretos, que son las más falsables: los resultados del taller de cinemática directa de Corke, t = 1,21 y 1,44 con orientación de 70 grados en la página 258, y t = 0,005, 0 y 0,332 con ángulos rpy de 0, −90 y −90 grados en la 278, los valores del péndulo de Lynch y Park en la página 422, el número de condición 232,1 de la página 317 de Corke y el radio del elipsoide como recíproco de la raíz de los autovalores en la 318. Todos correctos."));

children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("4. Las dos correcciones aplicadas"));
children.push(p("Ambas estaban en el bloque 6 y ninguna era un error de página: eran atribuciones que abarcaban más de lo que dice la página citada. Los apuntes ya se han regenerado con la corrección."));
children.push(tabla(
 ["Dónde", "Decía", "Dice ahora"],
 [
 ["B6, sesión S25, historia de la cámara oscura",
 "Atribuía a las páginas 540-541 de Corke la mención de Mozi y de Aristóteles. Mozi y la cámara oscura sí están ahí; Aristóteles aparece en la página 553, al hablar de la historia de la óptica",
 "Se separan las dos referencias: Mozi y la cámara oscura en las páginas 540-541, y la teoría de la visión de Aristóteles en la 553"],
 ["B6, sesión S30, ilustración del pasillo",
 "Citaba las páginas 250-252 de Thrun para la secuencia gráfica del pasillo con tres puertas. Esas páginas contienen la sección de localización de Montecarlo y su algoritmo, pero la ilustración de las puertas es del capítulo introductorio",
 "Se distingue: la ilustración de las puertas en las páginas 28-31 y el algoritmo MCL que la implementa en las 250-252"],
 ],
 [2100, 3900, 3360]
));

children.push(h1("5. Alcance y límites de esta verificación"));
children.push(p("Lo que se ha comprobado es que la página citada contiene el material del que trata la afirmación. Eso descarta el error más probable y más embarazoso, una página mal copiada, y confirma que las 992 referencias son navegables: si en clase abres el libro por donde dicen los apuntes, encontrarás lo que buscas."));
children.push(p("Lo que no puede garantizar un procedimiento automático es el matiz interpretativo: que la formulación en español recoja exactamente la fuerza de la afirmación original, sin generalizar de más. Para eso hace falta leer, y ahí sigue valiendo la recomendación de siempre: repasa el bloque antes de darlo. Las citas entrecomilladas se tomaron como traducción casi literal del original y se verificaron contra el texto inglés; las afirmaciones sin comillas son formulación propia apoyada en la página citada."));
children.push(box("Reproducible", "El verificador está guardado como verificar.py, junto con localizar.py, que dice en qué página impresa de un libro aparece un término dado. Si más adelante se añaden fuentes a la carpeta o se editan los apuntes, basta volver a ejecutarlos para repetir la comprobación completa."));

const doc = new Document({
 numbering: numberingConfig,
 styles: { default: { document: { run: { font: F, size: 22 } } } },
 sections: [{ properties: { page: { margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } }, children }],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync("Informe_Verificacion_Citas_82514.docx", buf); console.log("OK informe"); });
