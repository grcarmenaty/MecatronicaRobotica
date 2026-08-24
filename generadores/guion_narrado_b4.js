// Guion narrado de clase del Bloque 4 (S13 a S19): discurso literal del profesor
// anclado a las 29 diapositivas de IQS_B4_Cinematica_Estatica.pptx.
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, PageBreak, AlignmentType, ShadingType, ImageRun,
} = require("docx");
const { IQS, F, p, h1, box, bullet, numberingConfig } = require("./lib_iqs");

const LOGO = fs.readFileSync("media/logo_iqs_color.png");
const C = [];

// ---------- helpers ----------
const logoPar = () => new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { before: 300, after: 200 },
  children: [new ImageRun({ type: "png", data: LOGO, transformation: { width: 190, height: 145 } })],
});

function marca(fill, etiqueta, resto) {
  const runs = [new TextRun({ text: etiqueta, bold: true, color: IQS.navy, font: F, size: 19 })];
  if (resto) runs.push(new TextRun({ text: "   " + resto, color: "444444", font: F, size: 19, italics: true }));
  return new Paragraph({
    spacing: { before: 280, after: 120 },
    shading: { type: ShadingType.CLEAR, fill },
    border: { left: { style: "single", size: 20, color: IQS.navy } },
    children: runs,
  });
}
const proy = (n, titulo, resto) => C.push(marca("DDE3F5", "PROYECTOR · diapositiva " + n + " «" + titulo + "»", resto));
const piz = (t) => C.push(marca("FCEED2", "PIZARRA", t));
const cua = (t) => C.push(marca("DFF3E7", "PANTALLA", t));
const dem = (t) => C.push(marca("F2E4F0", "EN EL AULA", t));
const hab = (...ts) => ts.forEach(t => C.push(p(t)));
const acc = (t) => C.push(new Paragraph({
  spacing: { before: 60, after: 140 },
  children: [new TextRun({ text: "( " + t + " )", italics: true, color: IQS.grey, size: 20, font: F })],
}));
const salto = () => C.push(new Paragraph({ children: [new PageBreak()] }));

// ---------- portada ----------
C.push(logoPar());
C.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({ text: "82514 · Mecatrónica y Robótica", size: 40, bold: true, color: IQS.navy, font: F })] }));
C.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 }, children: [new TextRun({ text: "Guion narrado de clase · Bloque 4: Cinemática y estática de manipuladores", size: 28, color: IQS.navy2, font: F })] }));
C.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 400 }, children: [new TextRun({ text: "Sesiones S13 a S19 · 9 a 23 de octubre de 2026 · 10 horas · ligado a IQS_B4_Cinematica_Estatica.pptx (29 diapositivas)", size: 22, color: IQS.grey, font: F })] }));

h1("Cómo usar este guion");
C.push(p("Este documento contiene la clase hablada: lo que el profesor dice, en primera persona y con las palabras que diría en el aula, sincronizado con lo que debe verse en el proyector en cada momento. No sustituye a la guía del profesor (que recoge discusiones, soluciones y logística) ni a las notas del orador de la presentación (que son recordatorios telegráficos): esto es el discurso completo, pensado para preparar la clase, para ensayarla o para que otro docente pueda impartirla sin haberla diseñado."));
C.push(bullet("marca el momento de cambiar de diapositiva, con su número y su título exactos en la presentación del bloque. Entre dos marcas, todo el texto se dice con esa diapositiva en pantalla.", "PROYECTOR "));
C.push(bullet("indica trabajo en pizarra. La pizarra tiene prioridad sobre la diapositiva: cuando hay derivación, la diapositiva queda de fondo y el foco es la tiza.", "PIZARRA "));
C.push(bullet("indica que en el proyector debe verse el cuaderno Jupyter o la herramienta en vivo, no la presentación.", "PANTALLA "));
C.push(bullet("señala demostraciones físicas u organización del aula (el libro que gira, los portátiles, las parejas).", "EN EL AULA "));
C.push(bullet("los paréntesis en cursiva son acotaciones (tiempos, descansos, avisos); no se leen en voz alta.", "Acotaciones: "));
C.push(p("Los tiempos son orientativos y suman el total de cada sesión con margen. El discurso es un modelo: conviene decirlo con palabras propias, pero los números de los ejemplos, las citas de los libros y el orden de las ideas están calculados y verificados, y los ejemplos resueltos son espejo de las partes C y D del parcial 1 (con otros números). Los cuadernos citados están en el repositorio del curso; las páginas son de Corke, Robotics, Vision and Control (3.ª ed., 2023) y de Lynch y Park, Modern Robotics (2017)."));
salto();

// =====================================================================
// S13
// =====================================================================
h1("S13 · viernes 9 de octubre · 2 h · Posición y orientación (diapositivas 1 a 8)");
C.push(box("Antes de empezar", "Presentación en la diapositiva 1. Cuaderno 82514_S13_Pose_Rotaciones abierto y probado (spatialmath-python y matplotlib instalados). Un libro grande o una caja a mano para la demostración de no conmutatividad. Tiza o rotulador: hay dos derivaciones en pizarra."));

proy(1, "Portada del bloque 4", "min 0 a 2");
hab("Buenos días. Hoy empezamos el bloque 4, cinemática y estática de manipuladores, y os aviso desde ya: es el corazón geométrico de la asignatura. Hasta ahora hemos hablado de componentes, motores, sensores, electrónica de potencia. A partir de hoy hablamos del robot entero: dónde está su mano, cómo llega a un punto, qué fuerzas soporta cuando empuja. Son siete sesiones, diez horas, y terminan con el cuestionario del bloque y, dos semanas más tarde, con el primer parcial.");

proy(2, "Hoja de ruta del bloque", "min 2 a 8");
hab("Este es el mapa, y os pido que lo leáis como una escalera. Hoy aprendemos a describir dónde está algo. Parece poco, pero es la mitad del trabajo del bloque: posición y orientación juntas, lo que llamaremos pose. El miércoles 14 resolvemos la cinemática directa: si conozco los ángulos del robot, ¿dónde acaba su mano? El jueves 15 la programamos en Python con la Robotics Toolbox y la comparamos con el ABB del laboratorio. El viernes 16, dos horas para el problema contrario, la cinemática inversa, que es el que de verdad se cobra en la industria: sé dónde quiero la pieza, dadme los ángulos. Y la última semana conecta todo con una sola matriz, el jacobiano: velocidades el miércoles 21, singularidades el jueves 22, y fuerzas, trayectorias y repaso el viernes 23.",
"En cuanto a evaluación, dos cosas. El último día, cuestionario B4 en Moodle, quince minutos, dentro de la propia sesión. Y en el parcial 1, el 6 de noviembre, las partes C y D salen de este bloque. Los ejemplos que haremos en clase tienen exactamente esa estructura, con otros números: cuando lleguemos a ellos os lo iré señalando.");

proy(3, "S13 · Posición y orientación", "min 8 a 10");
hab("El plan de hoy en concreto: la primera hora es orientación, que es la parte que menos intuición trae de serie. La segunda hora es la pose completa y un taller con Python en el que todo lo que hagamos en la pizarra se vuelve código de cuatro líneas. Descanso a la hora en punto.");

proy(4, "Del PUMA al laboratorio", "min 10 a 13");
hab("Antes de la primera ecuación, mirad estas dos máquinas. El de la izquierda es un PUMA, años ochenta, el arquetipo del brazo industrial: es el mismo modelo que viene en los libros y el que cargaremos en el taller del jueves. El de la derecha es un seis ejes actual, la misma configuración que los ABB y los Mitsubishi que tenemos en el aula taller. Entre uno y otro hay cuarenta años, y la geometría no ha cambiado: seis giros encadenados. Ese es el objeto que vamos a aprender a describir, y la herramienta para describirlo es sorprendentemente vieja: matrices.");

piz("Dibujar dos marcos {A} y {B} y un punto; escribir la pregunta del día: ¿cómo se describe {B} visto desde {A}?");
proy(5, "Rotaciones: el grupo SO(3)", "min 13 a 35");
hab("Primera idea, y es la frase que quiero que os llevéis grabada del día: cualquier pose es siempre una pose relativa. Corke lo escribe así, literal, en la página 26. No existe la posición absoluta: la pieza está donde está respecto de la mesa, la mesa respecto del robot, el robot respecto de la nave. Por eso a cada cuerpo rígido le pegamos un marco de coordenadas, tres ejes perpendiculares a derechas, y siempre hablamos de la pose de un marco respecto de otro. Fijaos en la notación con dos subíndices, origen y destino: dentro de un rato veréis que esos subíndices se encadenan solos y os harán gratis la mitad de los ejercicios.");
piz("Derivar R(θ) en 2D proyectando los ejes girados; señalar que las columnas de R son los ejes del marco girado.");
hab("Derivemos la primera matriz de rotación en el plano. No os la aprendáis: mirad de dónde sale. Giro el marco un ángulo θ y escribo sus dos ejes nuevos vistos desde el marco viejo; esas dos proyecciones, puestas como columnas, son la matriz. Eso es todo. Una matriz de rotación no es un truco de álgebra: sus columnas son, literalmente, los ejes del marco girado. De ahí salen las dos propiedades que la definen: R traspuesta por R igual a identidad, porque los ejes son unitarios y perpendiculares, y determinante más uno, que descarta los marcos especulares, los levógiros. El conjunto de matrices que cumplen las dos cosas tiene nombre, SO(3), y la primera consecuencia práctica os va a gustar: la inversa de una rotación es su traspuesta. Invertir orientaciones no cuesta nada.",
"¿Para qué la usamos? Para tres cosas distintas, y conviene tenerlas separadas: representar una orientación, cambiar de marco un vector, y rotar un vector dentro de un marco. La misma matriz, tres papeles.");
dem("Libro en alto: girarlo 90° alrededor del eje vertical y después 90° alrededor de un eje horizontal; repetir en orden inverso.");
hab("Ahora el experimento clásico. Miradme el libro: lo giro noventa grados así, y ahora noventa así. Quedaos con cómo queda. Vuelvo a empezar y hago los mismos giros en orden contrario... y no acaba igual. La composición de rotaciones en tres dimensiones no conmuta. En el plano sí conmuta, y por eso vuestra intuición de 2D os traiciona en 3D. Cuando multipliquéis matrices de rotación, el orden es sagrado.",
"Última cuenta antes de cambiar de tema. Una matriz de rotación son nueve números, pero la ortonormalidad impone seis ligaduras. Nueve menos seis: tres. Tres grados de libertad de verdad. Entonces, ¿no habrá una forma de escribir una orientación con solo tres números? Haberla hayla, y tiene trampa.");

proy(6, "Tres maneras de escribir una orientación", "min 35 a 58");
hab("Primera familia: tres ángulos. Euler demostró que cualquier orientación se consigue con tres giros consecutivos sobre ejes del cuerpo, por ejemplo Z, luego Y, luego Z. En vehículos se usa la variante roll, pitch, yaw. Doce secuencias posibles, y aquí viene la primera advertencia de ingeniería: cuando alguien os pase «los ángulos» de un sensor o de un controlador, preguntad siempre qué convención usa, porque hay una docena y no se anuncian.",
"El problema de los tres ángulos no es de convención, es estructural: el bloqueo de cardán. Cuando el segundo giro alinea dos de los ejes, se pierde un grado de libertad y hay orientaciones a las que no se puede llegar suavemente. No es una curiosidad matemática: la plataforma inercial del Apolo 13 tenía tres cardanes justamente por esto, y los astronautas tenían que vigilar no acercarse a la configuración bloqueada. Corke lo resume en una frase que os pongo en la diapositiva: todas las representaciones de tres ángulos sufren el bloqueo de cardán. Todas.",
"Segunda familia: eje y ángulo. Cualquier rotación es girar θ alrededor de algún eje unitario. La fórmula de Rodrigues, que tenéis abajo, convierte ese par eje y ángulo en la matriz. Guardad esta idea con cariño, porque el producto de exponenciales del miércoles es exactamente esto aplicado a un robot entero.",
"Tercera familia: cuaterniones unitarios. Cuatro números y una ligadura. No os asusten: la parte vectorial es el eje por el seno de la mitad del ángulo. Componen barato, se interpolan bien y no tienen singularidad. Por eso son el estándar en robótica, en visión, en gráficos y en navegación. La regla del curso, que es la que os pediré en el cuestionario, está en la franja verde: matrices para operar, ángulos para comunicar con humanos, cuaterniones para interpolar y almacenar.");

acc("Descanso, min 58 a 70. Al volver, dejar proyectada la diapositiva 7.");

proy(7, "SE(3) y el taller de spatialmath", "min 70 a 85");
hab("Segunda hora. Ya sabemos orientar; ahora juntamos orientación y posición en un solo objeto. El truco tiene siglo y medio: coordenadas homogéneas. Meto la rotación R y la traslación t en una matriz cuatro por cuatro con una fila de ceros y un uno, y de repente componer poses es multiplicar matrices, y la cadena de subíndices funciona igual que esta mañana: el interior se cancela. Este conjunto se llama SE(3), y su versión plana, matrices tres por tres, SE(2).",
"Fijaos en la fórmula de la inversa: no hace falta resolver ningún sistema, se traspone R y se recoloca t. Y una norma de higiene numérica que en el taller es obligatoria: después de calcular una inversa, comprobad que T por su inversa da la identidad. Es una línea de código y os caza el noventa por ciento de los errores de orden.");

proy(8, "Ejemplo resuelto: componer poses en 2D", "min 85 a 92");
hab("Primer ejemplo con números del bloque. Leed el enunciado conmigo: la mesa está en el mundo en (1,0, 0,5) metros, girada 90 grados; la pieza está sobre la mesa en (0,2, 0,1), girada menos 30. ¿Pose de la pieza en el mundo?",
"Paso uno, y es el paso que vale puntos en el parcial: plantear la cadena antes de tocar ningún número. Mundo, mesa, pieza: la pose que busco es la del mundo a la mesa compuesta con la de la mesa a la pieza. El subíndice interior, la mesa, se cancela. Escribidlo siempre así, aunque os parezca ceremonioso.",
"Paso dos, ejecutar. El giro de 90 grados de la mesa convierte el (0,2, 0,1) en (menos 0,1, 0,2): lo que era «adelante» para la mesa es «arriba» para el mundo. Sumo la posición de la mesa y me queda (0,9, 0,7). Y las orientaciones, en el plano, simplemente se suman: 90 menos 30, 60 grados. Ahí tenéis la ecuación completa en la diapositiva.",
"Y paso tres, que en este curso nunca es opcional: comprobar con la máquina. Dos líneas de spatialmath, las tenéis abajo, y el resultado imprime (0,9, 0,7) y 60 grados. En el parcial, la parte C empieza exactamente con una composición como esta. Con otros números, claro.");

cua("Cuaderno 82514_S13_Pose_Rotaciones, min 92 a 115. La presentación queda en pausa.");
hab("Portátiles. El cuaderno reproduce todo lo de hoy en el mismo orden, con una sección por idea: rotaciones 2D con rot2 y trplot2, ángulos de Euler con eul2r y tr2eul, la demo interactiva del bloqueo de cardán, y SE(2) y SE(3) con composición e inversa. Id ejecutando y modificando: cambiad ángulos, romped cosas, es la manera de que esto se asiente. En la última sección tenéis el ejercicio guiado: una cadena mundo, mesa, pieza, cámara en la que hay que componer hacia delante y también invertir para responder qué ve la cámara. Es el ejemplo de antes con un eslabón más. Voy pasando por las mesas.");

hab("Cerramos. Tres frases para llevarse hoy. Una: toda pose es relativa, y los subíndices encadenados hacen la contabilidad por vosotros. Dos: una rotación es una matriz con columnas que son ejes, su inversa es la traspuesta, y en 3D el orden importa. Tres: matrices para operar, ángulos para comunicar, cuaterniones para interpolar. Para el miércoles, quince minutos de lectura: Corke, páginas 255 a 260, el planteamiento de la cinemática directa. Nos vemos aquí.");
acc("Cierre, min 115 a 120.");
salto();

// =====================================================================
// S14
// =====================================================================
h1("S14 · miércoles 14 de octubre · 1 h · Cinemática directa (diapositivas 9 a 11)");
C.push(box("Antes de empezar", "Presentación en la diapositiva 9. Pizarra limpia: la sesión tiene dos derivaciones (FK del 2R por proyecciones y la lógica del producto de exponenciales). El ejercicio por parejas del final usa el 2R del libro de Corke; el ejemplo resuelto usa el 2R del curso (0,35 y 0,2 m), que reaparecerá en S16, S17 y S19."));

proy(9, "S14 · Cinemática directa", "min 0 a 5");
hab("Buenos días. Dos preguntas de calentamiento sobre el viernes, respondedme de memoria. Primera: ¿cuánto cuesta invertir una transformación homogénea? Poco: traspones R y recolocas t, sin resolver sistemas. Segunda: ¿qué le pasa a cualquier representación de tres ángulos en alguna configuración? Bloqueo de cardán. Bien. Hoy, en una hora, resolvemos el primero de los dos grandes problemas del bloque: la cinemática directa. Dados los ángulos de las articulaciones, ¿dónde está el efector?");

proy(10, "Tres convenciones para la misma FK", "min 5 a 20, primero la franja superior");
hab("La definición formal la tenéis arriba, es de Lynch y Park: calcular la posición y orientación del marco del efector a partir de las coordenadas articulares. Quedaos con dos propiedades que hacen de este el problema «fácil»: la solución siempre existe y es única. Un robot con unos ángulos dados está donde está, no hay ambigüedad. El problema difícil, el inverso, os lo guardo para el viernes.");
piz("Dibujar el 2R plano (eslabones a₁ y a₂, ángulos q₁ y q₂) y derivar la posición del efector por suma de proyecciones; dejar la fórmula escrita, es la ecuación de la diapositiva.");
hab("Derivémoslo para el robot más simple que existe con dos articulaciones, el 2R plano, porque es el caballo de batalla de todo el bloque. La posición del efector es la suma de dos vectores: el primer eslabón proyectado con el ángulo q₁, y el segundo proyectado con el ángulo acumulado q₁ más q₂. Ojo con ese detalle, el ángulo del segundo eslabón se mide desde el primero, así que en el mundo lleva la suma. Y la orientación del efector es directamente q₁ más q₂. Esta fórmula de dos líneas es la cinemática directa completa del 2R, y la vamos a exprimir durante tres semanas.");
hab("Ahora, la pregunta de ingeniería: esto ha sido geometría de bachillerato porque el robot tenía dos ejes paralelos. ¿Cómo se escribe la FK de un seis ejes real sin equivocarse? Hay tres convenciones en uso, y las tres describen lo mismo. Vamos a verlas como tres dialectos del mismo idioma.");
hab("Primera, la secuencia de transformaciones elementales, ETS, que es la que usa Corke. Se lee la geometría del robot de izquierda a derecha: giro según Z con q₁, traslado a₁ en X, giro con q₂, traslado a₂. Cada símbolo es una matriz elemental y la FK es su producto. Es la más transparente: si sabéis dibujar el robot, sabéis escribir su ETS.",
"Segunda, Denavit y Hartenberg, la del artículo de 1955 y la de los catálogos. Cuatro parámetros por eslabón, θ, d, a y α, ordenados en una tabla. Cada fila codifica cuatro transformaciones elementales en orden fijo. Su virtud es que es compacta y universal: cuatro números por eslabón describen un robot entero y cualquiera en el mundo lo reconstruye. Su peligro: hay variantes de numeración, y una tabla DH heredada sin saber la variante es una fuente clásica de horas perdidas.",
"Tercera, el producto de exponenciales, la de Lynch y Park y la más moderna.");
piz("Sobre el dibujo del 2R: congelar el robot en su configuración cero, marcar M, y mostrar que girar la articulación 1 arrastra todo lo que cuelga de ella: cada articulación aplica una exponencial al resto de la cadena.");
hab("La idea es preciosa y es Rodrigues otra vez. Congelad el robot en su configuración cero y llamad M a la pose del efector en esa foto. Ahora girad solo la articulación uno: todo lo que cuelga de ella gira en bloque alrededor de su eje. Ese giro es una exponencial, la de Rodrigues, aplicada a M. Girad también la dos: otra exponencial más cerca del efector. La FK es M premultiplicada por una exponencial por articulación, y no hay que definir ni un solo marco intermedio. Además, los ejes S que aparecen aquí son exactamente las columnas del jacobiano que derivaremos el miércoles que viene: este formalismo es una inversión a futuro.");

proy(11, "Ejemplo resuelto: FK del 2R con números", "min 20 a 32");
hab("Vamos a ponerle números, y estos números os los vais a encontrar más veces: este 2R con eslabones de 0,35 y 0,2 metros es el robot oficioso del bloque. Enunciado: q igual a 30 y 60 grados; pregunto posición, orientación, tabla DH y espacio de trabajo.",
"Paso uno, la posición, con la fórmula de la pizarra. Primer término: 0,35 por coseno de 30. Segundo término: 0,2 por coseno de la suma, 90 grados, que es cero. En x me queda 0,303. En y: 0,35 por seno de 30, que es 0,175, más 0,2 por seno de 90, que es 0,2: total 0,375. Fijaos en la lectura física: el segundo eslabón apunta recto hacia arriba porque el ángulo acumulado es 90, por eso solo aporta a la y.",
"Paso dos, la orientación: 30 más 60, 90 grados. La pose completa del efector: (0,303, 0,375) y 90 grados.",
"Paso tres, la tabla DH, que aquí es trivial y por eso es buen momento para escribirla sin miedo: dos filas, θ es la variable articular, d cero porque es plano, a los largos de los eslabones, α cero porque los ejes son paralelos. Dos filas, ocho números, robot descrito.",
"Paso cuatro, el espacio de trabajo, que es la pregunta con trampa favorita de los exámenes: ¿a qué puntos llega este robot? Brazo estirado: 0,35 más 0,2, 0,55 metros de radio exterior. Brazo plegado: 0,35 menos 0,2, 0,15 de radio interior. Un anillo. Un punto a 0,6 metros es inalcanzable, obvio; pero un punto a 0,1 también lo es, porque el robot no puede plegarse más de lo que el codo permite. Cuando el viernes calculéis cinemática inversa, la primera comprobación siempre será esta: ¿está el punto dentro del anillo?",
"Esta estructura, FK con números, tabla y espacio de trabajo, es la parte C del parcial 1. Con otros largos y otros ángulos.");

dem("Parejas, min 32 a 55: cada pareja escribe la ETS, la tabla DH y la terna M, S₁, S₂ del 2R del libro (eslabones de 1 m) y verifica las tres en q = (30°, 40°).");
hab("Ahora vosotros, por parejas, con el 2R del libro de Corke, el de eslabones de un metro. Cada pareja escribe las tres descripciones: la ETS, la tabla DH y la terna del producto de exponenciales. Después, con la calculadora o con Python, evaluad las tres en q igual a 30 y 40 grados. Si todo está bien, las tres tienen que dar lo mismo: posición (1,21, 1,44) y orientación 70 grados. Si alguna no cuadra, el error casi siempre está en el orden de las transformaciones o en la fila de la tabla: usad la cancelación de subíndices para auditarlo. Diez minutos y ponemos en común.");
hab("Puesta en común. ¿Qué dialecto os ha resultado más cómodo? La respuesta correcta es: depende del uso. ETS para entender y leer geometría, DH para compartir modelos con el resto del mundo, producto de exponenciales para preparar el análisis de velocidad. En este curso los usaremos así, cada uno en su papel.");
hab("Última cosa. Mañana, taller entero de ordenador: traed portátil con la Robotics Toolbox instalada, que la FK de un seis ejes de verdad no se hace a mano, se programa. Hasta mañana.");
acc("Cierre, min 55 a 60.");
salto();

// =====================================================================
// S15
// =====================================================================
h1("S15 · jueves 15 de octubre · 1 h · Taller: FK de un 6R en Python (diapositivas 12 y 13)");
C.push(box("Antes de empezar", "Aula taller. Presentación en la diapositiva 12 solo para abrir; la sesión vive en el cuaderno 82514_S15. Robot ABB encendido con el controlador accesible para leer pose y articulares. Recordar en voz alta que las normas de seguridad fijadas en S7 siguen vigentes."));

proy(12, "S15 · Taller: FK de un 6R en Python", "min 0 a 5");
hab("Buenos días. Hoy no hay teoría nueva: hay una hora para que la cinemática directa pase de la pizarra a vuestras manos. El objetivo tiene tres partes: cargar modelos de robots reales en la Robotics Toolbox, calcular y leer poses con soltura, y comparar el modelo con el ABB que tenemos aquí al lado. Lo primero de todo: abrid el cuaderno 82514_S15 y ejecutad la primera celda, los import. Si a alguien le falla, mano arriba ahora, no en el minuto cuarenta.");

proy(13, "Del modelo de libro al robot del laboratorio", "min 5 a 8, luego la pantalla es el cuaderno");
hab("Estas son las cuatro llamadas de la sesión, os las presento y las vais probando. Uno: cargar el PUMA con models.DH.Puma560, el primer robot industrial moderno, y el IRB140 de ABB. Dos: las configuraciones con nombre, qz todo a cero, qr la postura de referencia; son propiedades del robot y podéis definir las vuestras. Tres: fkine para la cinemática directa y printline para leerla en formato humano, posición y ángulos. Cuatro: teach, que os abre deslizadores, uno por articulación, con la pose del efector actualizándose en vivo. Con eso se juega; jugando es como se entiende una cadena cinemática.");

cua("Cuaderno 82514_S15, min 8 a 40: modelos, fkine y printline, verificación de la cadena, exploración con teach, 6R genérico como ETS.");
hab("Os marco los hitos del cuaderno. Primero, cargad el IRB140 y calculad la pose en qr: os tiene que dar la posición (0,005, 0, 0,332) con esa orientación de menos noventa grados que veis en la diapositiva. Segundo, verificad a mano el producto de la cadena para una configuración: es la misma multiplicación de matrices del viernes, la toolbox solo os ahorra teclearla. Tercero, abrid teach con el PUMA y buscad dos cosas: la muñeca esférica, esos tres ejes que se cortan en un punto, y qué articulaciones mueven mucho el efector y cuáles poco según la postura. Y cuarto, el 6R genérico escrito como ETS, para que veáis que un robot industrial es la receta del miércoles con una muñeca ZYZ al final.",
"Una trampa clásica os va a salir al paso, y os la anticipo: en los modelos DH de libro, el «efector» es el centro de la muñeca, que está dentro del robot. La brida real, donde se atornilla la pinza, exige añadir la transformación de herramienta. Si vuestros números no cuadran con la intuición, empezad por ahí.");

dem("min 40 a 55: junto al ABB, con el controlador en modo lectura.");
hab("Ahora, todos alrededor del robot. En el controlador leemos dos cosas: las coordenadas articulares y la pose de la brida que él calcula. Meted esas articulares en vuestro modelo de la toolbox y comparad poses. No van a coincidir exactamente, y esa discrepancia es la lección: ¿qué herramienta lleva montada? ¿Dónde ha puesto el integrador la base? ¿Qué convención de ángulos usa este controlador para la orientación? Un modelo no está terminado hasta que explica las diferencias con la máquina real. Esto, en la industria, se llama calibrar la célula, y es un oficio.");

hab("Para casa, un mini reto con truco: usando solo teach, sin ninguna función más, intentad llevar el efector del PUMA a tocar un punto objetivo que os doy en el cuaderno. Contad los intentos. Mañana empezamos preguntando cuántos os ha costado, y veréis que la respuesta motiva sola la clase entera: se llama cinemática inversa. Hasta mañana.");
acc("Cierre, min 55 a 60.");
salto();

// =====================================================================
// S16
// =====================================================================
h1("S16 · viernes 16 de octubre · 2 h · Cinemática inversa (diapositivas 14 a 17)");
C.push(box("Antes de empezar", "Presentación en la diapositiva 14. Pizarra limpia para la derivación estrella del bloque (2R por ley de cosenos). Cuaderno 82514_S16 probado. El ejemplo resuelto reutiliza el 2R del curso (0,35 y 0,2 m) y sus dos ramas alimentan S17 y S19: merece la pena hacerlo despacio."));

proy(14, "S16 · Cinemática inversa", "min 0 a 10");
hab("Buenos días. ¿Cuántos intentos os costó tocar el punto con teach? ¿Ocho? ¿Doce? Eso que hicisteis a ojo, iterar ángulos hasta acertar una pose, es exactamente el problema que hoy resolvemos con matemáticas: la cinemática inversa. Dada la pose deseada del efector, encontrar las coordenadas articulares.",
"Y os aviso de que este problema tiene otra personalidad. La directa era una función: siempre una respuesta, siempre la misma. La inversa puede no tener solución, si pido un punto fuera del alcance; puede tener varias, y hoy veremos exactamente cuántas; y puede tener infinitas, en configuraciones especiales o en robots redundantes. El anuncio del día, para que lo tengáis en la cabeza toda la sesión: un seis ejes industrial típico llega a la misma pose de ocho maneras distintas. Al final de la mañana sabréis de dónde sale ese ocho.");

piz("Derivación estrella: el 2R con ley de cosenos. Dibujar el triángulo (dos eslabones y la recta del origen al punto), obtener cos q₂, discutir el ±, y el hombro con atan2 en dos términos.");
proy(15, "IK analítica: del 2R a las ocho soluciones", "min 10 a 35, mitad izquierda");
hab("Empezamos por el 2R, en pizarra y despacio, porque esta derivación es la madre de todas las soluciones analíticas. Quiero llegar al punto P. Los dos eslabones y la línea del origen a P forman un triángulo, y del triángulo, ley de los cosenos, sale el coseno del ángulo del codo. Antes de seguir, mirad ese coseno: si me sale mayor que uno en valor absoluto, no hay triángulo, el punto está fuera del alcance. La existencia de solución se decide aquí, en una desigualdad.",
"Si hay triángulo, hay dos codos posibles: el positivo y el negativo, codo arriba y codo abajo. El signo más menos que aparece al despejar no es una molestia, es información: son dos configuraciones físicas distintas que llegan al mismo sitio.",
"Y el hombro sale con atan2 de dos argumentos: el ángulo hasta el punto, menos la corrección por el codo. Aquí va la regla de oficio del curso, y la vais a usar en todos los ejercicios: siempre atan2 con dos argumentos, jamás la arcotangente del cociente. La arcotangente pierde el cuadrante; atan2 no. Esta regla, sola, vale puntos en el parcial.");

proy(16, "Ejemplo resuelto: la IK y sus dos ramas", "min 35 a 47");
hab("Números. El mismo robot del miércoles, 0,35 y 0,2, y ahora le pido que alcance el punto (0,4, 0,2). Primera comprobación, siempre: ¿es alcanzable? Distancia al origen: raíz de 0,16 más 0,04, 0,447 metros. El anillo iba de 0,15 a 0,55: dentro. Adelante.",
"Ley de los cosenos: el coseno del codo me da 0,268. Dos codos posibles: más 74,5 grados o menos 74,5.",
"Rama codo abajo, con q₂ positivo: el hombro sale de atan2(0,2, 0,4), que es 26,6 grados, menos la corrección del codo, 25,5: q₁ igual a 1,0 grados. Prácticamente horizontal.",
"Rama codo arriba: q₁ igual a 52,1 grados. Dos posturas completamente distintas, mirad las dos tarjetas.",
"Y ahora el paso que os pido siempre y que casi nadie hace por iniciativa propia: verificar cerrando el círculo. Meto cada pareja de ángulos en la cinemática directa del miércoles y las dos me devuelven (0,4, 0,2). Si la FK no te devuelve el punto, la IK está mal, no hay discusión posible. En el parcial, la parte D es exactamente este ejercicio con otros números, y el criterio de corrección premia esa verificación.");

proy(15, "IK analítica: del 2R a las ocho soluciones", "min 47 a 60, ahora la mitad derecha y las tarjetas");
hab("Del 2R al seis ejes industrial. La pregunta es: ¿cuándo existe solución en forma cerrada, con fórmulas? Respuesta: cuando la geometría colabora, y la colaboración estándar es la muñeca esférica, tres últimos ejes cortándose en un punto. Eso permite el truco del desacoplo: la posición del centro de la muñeca solo depende de las tres primeras articulaciones, así que resuelvo primero un problema de posición con tres incógnitas, mi 2R con una cintura debajo, y después la orientación restante con las tres últimas, que es extraer tres ángulos de Euler de una matriz.",
"Contemos soluciones. La cintura puede mirar al punto o darle la espalda: lefty y righty, dos. El codo, arriba o abajo: por dos, cuatro. La muñeca, volteada o no: por dos, ocho. Ocho soluciones para la misma pose, y ya sabéis de dónde salen. En la práctica alguna cae por límites articulares o por colisión con la mesa, pero el programador tiene que elegir rama, y elegirla mal es la diferencia entre un movimiento limpio y un codazo a la célula.",
"Casos degenerados, tarjeta de arriba: punto fuera del alcance, cero soluciones; objetivo en el eje de la cintura, con x e y nulos, infinitas soluciones para la primera articulación. Y con esto tenemos el mapa completo del problema analítico.");

acc("Descanso, min 60 a 70.");

proy(17, "IK numérica y taller con la toolbox", "min 70 a 85");
hab("Segunda hora. ¿Y si el robot no tiene muñeca esférica, o quiero un método que valga para cualquier geometría? Entonces la IK se resuelve como se resuelven casi todas las ecuaciones difíciles de la ingeniería: numéricamente, con Newton. Mirad la cadena de cuatro pasos: parto de una semilla, una estimación inicial; mido el error entre la pose deseada y la que da la FK; linealizo con una matriz que os presento formalmente el miércoles, el jacobiano, y doy el paso de Newton con su pseudoinversa; y repito hasta que el error baja de la tolerancia. Con una buena semilla, esto converge a precisión de centésimas de milímetro en un puñado de iteraciones.",
"Las dos letras pequeñas del método, que en el taller vais a ver en vivo. Una: converge a una solución, no a todas; a cuál, lo decide la semilla. Si quiero la rama codo abajo, siembro cerca de codo abajo. Dos: cerca de configuraciones singulares el método sufre, puede saltar de rama o no converger. Las singularidades, que de momento son solo una palabra, tienen sesión propia el jueves.");

cua("Cuaderno 82514_S16, min 85 a 115: ikine_a con banderas de rama, fallos con diagnóstico, ikine_LM con y sin semilla, y la síntesis por parejas.");
hab("Taller. Tres bloques y una síntesis. Primero, la analítica con ikine_a: pedidle una pose y verificad con fkine, siempre; después explorad las ocho ramas con las banderas de configuración, izquierda o derecha, codo arriba o abajo, muñeca volteada o no. Segundo, los fallos con diagnóstico: pedidle un punto a tres metros y leed el error, fuera de alcance; poned la muñeca a cero y observad que dos ejes se alinean y solo queda determinada una suma de ángulos, vuestra primera singularidad de verdad. Tercero, la numérica con ikine_LM: la misma pose con semillas distintas os devuelve ramas distintas; sin semilla, el resultado depende de un arranque aleatorio, y ese no determinismo en una fábrica es un defecto, no una curiosidad.",
"La síntesis, por parejas: para un punto de la mesa que os doy en el cuaderno, obtened las ocho soluciones, descartad las que violan límites articulares o chocan con la mesa, y elegid una razonadamente: la más cercana a la postura actual, o la que deja el codo alto. Escribid la justificación en una frase, que es lo que os pediré en el parcial.");

hab("Cierre en una frase por método: la IK industrial es analítica cuando la geometría lo permite, porque es instantánea y da todas las ramas; y numérica en el resto, pagando semilla y convergencia. En ambos casos, la multiplicidad de soluciones no es un problema matemático, es una decisión de programación. Para el miércoles: Corke, 310 a 315, el jacobiano. Es la lectura más importante del bloque.");
acc("Cierre, min 115 a 120.");
salto();

// =====================================================================
// S17
// =====================================================================
h1("S17 · miércoles 21 de octubre · 1 h · Jacobiano y cinemática diferencial (diapositivas 18 a 22)");
C.push(box("Antes de empezar", "Presentación en la diapositiva 18. La derivación de J para el 2R se hace en pizarra partiendo de la FK de S14 (conviene llevarla escrita en un lateral). El ejemplo resuelto continúa el de S16: misma configuración codo abajo. Cuaderno 82514_S17 listo para la demo de jacob0 y la de velocidad resuelta."));

proy(18, "S17 · Jacobiano y cinemática diferencial", "min 0 a 3");
hab("Buenos días. Recuperación exprés del viernes: ¿cuántas soluciones tenía la IK del seis ejes con muñeca esférica? Ocho. ¿Y de qué dependía la rama a la que convergía el método numérico? De la semilla. Perfecto. Hoy os presento la matriz más importante de la robótica de manipuladores. No exagero: la que bautizamos hoy va a aparecer en la IK numérica que ya usasteis, en las singularidades de mañana y en las fuerzas del viernes.");

proy(19, "El 2R, en movimiento", "min 3 a 5");
hab("Dos imágenes para abrir el apetito, las dos hechas con el robot del curso y las dos las vais a generar vosotros. A la izquierda, el espacio de trabajo del 2R con unas elipses dibujadas en tres posturas: fijaos en que cerca del borde las elipses se aplastan. A la derecha, una animación de una trayectoria: la punta del robot no va en línea recta aunque las articulaciones se muevan suavemente. Las dos cosas, las elipses aplastadas y la recta que no es recta, quedan explicadas hoy y mañana.");

piz("Derivar J en el 2R: partir de la FK de S14, derivar respecto del tiempo con la regla de la cadena, agrupar en matriz por columnas. Dejar J escrita.");
proy(20, "El jacobiano: la matriz que todo lo conecta", "min 5 a 25");
hab("Vamos a derivar. Tengo la posición del efector como función de los ángulos, la FK del otro día. La derivo respecto del tiempo: regla de la cadena, cada término es la parcial respecto de un ángulo por la velocidad de ese ángulo. Si lo ordeno en forma matricial, me queda la velocidad del efector igual a una matriz por las velocidades articulares. Esa matriz de parciales es el jacobiano, J de q. La definición formal es la de Lynch y Park que tenéis en pantalla: la sensibilidad lineal de la velocidad del efector a la velocidad articular. Y subrayad el «de q»: J depende de la configuración. No hay «el jacobiano del robot», hay el jacobiano del robot en esta postura.",
"La manera de entenderlo no es la fórmula, es la lectura por columnas: la columna i es la velocidad del efector cuando solo la articulación i se mueve, a velocidad uno. Hagamos el experimento mental antes de calcular nada. Brazo estirado del todo. Solo muevo el hombro: la punta se mueve perpendicular al brazo, rápido. Solo muevo el codo: la punta se mueve... también perpendicular al brazo. Las dos columnas apuntan igual. Guardad esa imagen: es la semilla de la clase de mañana.",
"Dos apuntes de nomenclatura para el taller. En 3D la velocidad del efector tiene seis componentes, tres lineales y tres angulares, así que J es seis por n; jacob0 os la da en el marco del mundo y jacobe en el del efector, que es el útil cuando el sensor de fuerza va montado en la muñeca. Y existe el jacobiano analítico, que expresa la orientación en tasas de ángulos RPY: hereda la singularidad de representación de los tres ángulos, el precio de siempre.");

proy(21, "Ejemplo resuelto: jacobiano y velocidades", "min 25 a 35");
hab("Números, continuando exactamente donde lo dejamos el viernes: la rama codo abajo, hombro a 1,0 grados, codo a 74,5. Evalúo las cuatro parciales y me queda la matriz que veis: primera fila (menos 0,200, menos 0,194), segunda (0,400, 0,050). Su determinante, 0,067 metros cuadrados.",
"Ahora la pregunta práctica: quiero que el efector se mueva a diez centímetros por segundo hacia la derecha, en x. Resuelvo el sistema, J por q punto igual a v, y obtengo: hombro a 0,074 radianes por segundo, codo a menos 0,593. Pasadlo a grados para sentirlo: cuatro grados por segundo el hombro y treinta y cuatro, en sentido contrario, el codo. Leedlo físicamente: para un movimiento cartesiano modesto, el codo está trabajando ocho veces más rápido que el hombro. Esa asimetría es información sobre la postura.",
"Y la referencia de escala: este determinante, 0,067, está cerca de su máximo posible para este robot, que es el producto de los dos eslabones, 0,07. Traducción: configuración cómoda, lejos de singularidad. Mañana veremos qué pasa cuando ese número se acerca a cero: las velocidades articulares que acabamos de calcular se disparan.");

proy(22, "Control de velocidad resuelta", "min 35 a 52");
hab("Y ahora, la recompensa: con el jacobiano se puede mover el robot en cartesiano sin resolver la cinemática inversa. El algoritmo se llama control de velocidad resuelta y cabe en cuatro pasos: fijo la velocidad deseada del efector, por ejemplo línea recta a velocidad constante; invierto J para obtener las velocidades articulares; integro un pasito de tiempo; y vuelta a empezar, porque el robot se ha movido y J ya es otra. Corke lo llama un algoritmo simple y elegante, y lo es: es la manera en que muchos robots reales ejecutan el jog cartesiano de la botonera.");
cua("Cuaderno 82514_S17: demo de velocidad resuelta, el efector del PUMA en línea recta; después, jacob0 en dos configuraciones para la tarjeta de la derecha.");
hab("Vedlo correr. El bucle son cinco líneas: jacobiano, resolver, integrar, repetir. El efector va en línea recta de verdad, cosa que la trayectoria articular de la animación de antes no conseguía. Dos letras pequeñas antes de que os enamoréis del método. Primera: integrar en lazo abierto deriva, los errores se acumulan; en la práctica se cierra el lazo con la pose real medida. Segunda, y es la puerta de mañana: el algoritmo exige invertir J en cada paso. ¿Qué pasa si en alguna postura J no se puede invertir? Esa pregunta, exactamente esa, es la clase de mañana.",
"Cierro con el mapa que os prometí: el jacobiano ya conecta la FK con las velocidades, es el corazón del paso de Newton de la IK numérica que usasteis el viernes, mañana define las singularidades y el viernes, transpuesto, os dará las fuerzas. Una matriz, cuatro capítulos. Hasta mañana.");
acc("Cierre, min 52 a 60: preguntas sueltas y recogida.");
salto();

// =====================================================================
// S18
// =====================================================================
h1("S18 · jueves 22 de octubre · 1 h · Singularidades y manipulabilidad (diapositivas 23 y 24)");
C.push(box("Antes de empezar", "Presentación en la diapositiva 23. Cuaderno 82514_S18 con la demo preparada (svd del jacobiano, plot_ellipsoid, m(q) a lo largo de una trayectoria). Recuperar en un lateral de la pizarra la J del 2R de ayer: la predicción del brazo estirado se verifica sobre ella."));

proy(23, "S18 · Singularidades y manipulabilidad", "min 0 a 5");
hab("Buenos días. Ayer os dejé una pregunta cargada: ¿qué pasa cuando J no se puede invertir? Y una imagen: brazo estirado, las dos columnas del jacobiano apuntando en la misma dirección. Hoy le ponemos nombre, teoría y número a esa situación. Se llama singularidad cinemática, y es probablemente el concepto de este bloque que más se nota en el taller: es la razón de que un robot industrial, a mitad de una trayectoria aparentemente inocente, frene de golpe o cancele el movimiento con un error críptico.");

proy(24, "Singularidades y elipsoide de manipulabilidad", "min 5 a 40");
hab("Definición, la de Lynch y Park: una postura en la que el efector pierde la capacidad de moverse instantáneamente en una o más direcciones. Matemáticamente: J deja de tener rango máximo. En el 2R lo tenéis en la pizarra: brazo estirado, columnas paralelas, rango uno. Físicamente: por muy rápido que muevas las articulaciones, hay una dirección, la del brazo, en la que la punta no puede moverse ahora mismo. Para alejarse del borde primero hay que doblar el codo.",
"Una propiedad que os evitará discusiones estériles: la singularidad no depende del marco en el que escribas el jacobiano. Es un hecho geométrico del robot, no de tu descripción. Cambiar de coordenadas no cura nada.",
"En un seis ejes real, los tres casos clásicos que todo integrador conoce de memoria. Singularidad de muñeca: dos ejes de la muñeca se alinean cuando el ángulo intermedio pasa por cero; ya la visteis el viernes en el taller sin saber su nombre, cuando solo quedaba determinada la suma de dos ángulos. Singularidad de codo: el brazo completamente extendido, nuestro caso de pizarra en grande. Singularidad de hombro: el centro de la muñeca cruza el eje de la cintura. Los controladores industriales las vigilan en tiempo real, y su reacción estándar es frenar o abortar, porque la alternativa es pedirle a algún motor velocidad infinita.",
"Ahora, la pregunta de ingeniero: la singularidad exacta es un punto, pero ¿cómo de cerca es «demasiado cerca»? Para responder con un número necesitamos geometría. Imaginad todas las combinaciones de velocidades articulares de tamaño uno, una esfera en el espacio articular. El jacobiano transforma esa esfera en un elipsoide de velocidades del efector: el elipsoide de manipulabilidad. Si es casi una esfera, la postura es isótropa, el robot se mueve igual de bien en todas las direcciones. Si está muy achatado, hay una dirección casi prohibida: estamos cerca de una singularidad. En la singularidad exacta, el elipsoide colapsa a un segmento: una dimensión entera de movimiento ha desaparecido. Son las elipses aplastadas que os enseñé ayer en la primera imagen.",
"Y el número único, para monitorizar: la medida de Yoshikawa, proporcional al volumen del elipsoide. Cerca de cero, mal. Con su letra pequeña, que os pongo en la diapositiva: mide volumen, no forma; un elipsoide largo y finísimo puede conservar volumen decente siendo pésimo en una dirección. Para afinar se miran los valores singulares de J, el mayor y el menor, que son exactamente los semiejes.");

cua("Cuaderno 82514_S18, min 40 a 55: svd del jacobiano en dos posturas, plot_ellipsoid, y m(q) graficada a lo largo de una trayectoria.");
hab("A la máquina, tres experimentos. Uno: jacob0 del PUMA en su postura nominal y en una casi estirada; comparad determinante y valores singulares con la svd, y ved cómo el valor singular pequeño se hunde al acercarse al estiramiento. Dos: dibujad el elipsoide traslacional con plot_ellipsoid en las dos posturas; la diferencia visual es todo el concepto. Tres: graficad la manipulabilidad a lo largo de una trayectoria completa; veréis un valle profundo a mitad de camino. Ese valle, mañana, cuando hagamos trayectorias cartesianas, va a ser exactamente el punto donde el movimiento se estropea. Guardad la gráfica.");

hab("Cierre. La singularidad no es una avería ni mala suerte: es una propiedad geométrica del robot, anticipable con una svd, monitorizable con un número. Y la primera herramienta contra ella no es matemática, es de oficio: diseñar la tarea, colocar la pieza y elegir la rama de IK para que la trayectoria pase lejos. Mañana, última sesión del bloque: fuerzas, trayectorias, repaso y cuestionario. Traed portátil.");
acc("Cierre, min 55 a 60.");
salto();

// =====================================================================
// S19
// =====================================================================
h1("S19 · viernes 23 de octubre · 2 h · Estática, trayectorias y cierre (diapositivas 25 a 29)");
C.push(box("Antes de empezar", "Presentación en la diapositiva 25. Pizarra limpia para la derivación por potencia (la más corta del bloque) y para el mapa final. Cuaderno 82514_S19 listo. Cuestionario B4 programado en Moodle (15 min, 10 preguntas) para abrirse en el último cuarto de hora; avisar a los rezagados de que se hace en clase."));

proy(25, "S19 · Estática, trayectorias y cierre", "min 0 a 2");
hab("Buenos días. Última sesión del bloque, con cuatro platos: fuerzas sin movimiento, la dualidad más bonita de la robótica, trayectorias que respetan a los motores, y el repaso con el cuestionario. Empezamos fuerte, con una derivación de dos líneas.");

piz("Derivación por conservación de potencia: potencia articular τᵀ·q̇ igual a potencia en el efector Fᵀ·ẋ; sustituir ẋ = J·q̇, exigir validez para todo q̇, y despejar τ = Jᵀ·F.");
proy(26, "Estática: τ = Jᵀ·F y la dualidad", "min 2 a 20");
hab("Situación: el robot no se mueve, pero empuja. Aprieta una pieza, sostiene una carga, taladra. ¿Qué par tiene que hacer cada motor para sostener una fuerza F en la punta? La derivación es la más elegante del bloque y sale de un principio de primero de carrera: la potencia ni se crea ni se destruye. La potencia que entra por los motores es par por velocidad articular; la que sale por el efector es fuerza por velocidad de la punta. Igualadlas, sustituid la velocidad de la punta por J por q punto, que es lo de esta semana, y exigid que valga para cualquier velocidad. Lo que queda es: τ igual a J transpuesta por F. La misma matriz de toda la semana. Sin derivar ni una fuerza, sin un solo diagrama de sólido libre.",
"La versión completa en 3D usa el torsor, wrench en inglés: el vector de seis componentes con tres fuerzas y tres momentos, y el par generalizado es J transpuesta por el torsor. Es la fórmula con la que se dimensionan muñecas y se leen los sensores de fuerza.",
"Y ahora la frase de Corke que parece magia: la traspuesta del jacobiano nunca puede ser singular. La estática funciona incluso en las posturas donde la cinemática de velocidades falla. ¿Cómo puede ser? Pensad en vuestro propio cuerpo: cuando lleváis una maleta pesada, ¿cómo ponéis el brazo? Colgando, recto del todo. Exactamente la singularidad de codo. Velocidad imposible, fuerza gratis: el esqueleto aguanta la carga y el músculo casi no trabaja. La dualidad completa es esa: el elipsoide de fuerza tiene los mismos ejes que el de velocidad y semiejes recíprocos. Donde moverse es fácil, empujar es caro; donde moverse es imposible, sostener es gratis.");

proy(27, "Ejemplo resuelto: pares estáticos", "min 20 a 32");
hab("Números, y cerramos el círculo del robot del curso: misma configuración codo abajo del viernes pasado, hombro a 1,0 grados, codo a 74,5. Ahora el efector tiene que empujar hacia arriba con diez newtons. ¿Qué pares soportan los motores?",
"Paso uno: no hay nada que derivar. El jacobiano ya lo calculamos el miércoles; lo traspongo y multiplico por la fuerza. Resultado: 4,0 newton metro el hombro, 0,5 el codo.",
"Paso dos, la lectura, que es lo que os pediré explicar: ¿por qué el codo casi no trabaja? Mirad la postura: el segundo eslabón está casi vertical, casi alineado con la fuerza. El momento es brazo por fuerza perpendicular, y aquí casi no hay brazo perpendicular. El hombro, en cambio, ve la fuerza con 0,4 metros de brazo efectivo: 4 newton metro.",
"Y el caso límite, que conecta con el dimensionado de motores del bloque 3: brazo estirado horizontal, la peor postura para sostener peso. Ahí los brazos de palanca son los eslabones enteros: 0,55 por diez, 5,5 newton metro en el hombro; 0,2 por diez, 2,0 en el codo. Cuando en el bloque 3 elegíais motor por par nominal, este era el número que había que mirar: el peor caso estático del espacio de trabajo, no el caso cómodo. La franja verde de abajo resume la dualidad en una frase para el cuestionario: empujar es barato justo donde moverse es caro.");

proy(28, "Trayectorias: caminos y leyes temporales", "min 32 a 55");
hab("Cambio de tema, el último del bloque: ya sabemos dónde está el robot, cómo llegar y qué fuerzas hace. Falta el cómo moverse con elegancia del punto A al punto B. La definición de Lynch y Park separa dos cosas que en el lenguaje coloquial van juntas: el camino, que es geometría pura, por dónde paso; y la ley temporal, cuándo paso por cada punto. La misma recta recorrida suave o a tirones son la misma geometría con distinta ley temporal.",
"Tres leyes temporales de catálogo. La cúbica: un polinomio de grado tres que sale y llega con velocidad nula. Su defecto está escondido en la aceleración: en los extremos salta de golpe, tirón seco, jerk infinito; para mover mecánica real es mala educación. La quíntica: grado cinco, seis condiciones, también impone las aceleraciones en los extremos; el movimiento es visiblemente más suave y es la que se usa por defecto en este curso. Y la trapezoidal, la del control de motores industrial: acelero constante, crucero a velocidad máxima, freno constante. No es la más suave, pero aprovecha al máximo los límites del accionamiento, y su perfil de velocidad en trapecio se lee de un vistazo en cualquier osciloscopio de variador.",
"Y la decisión de arquitectura, abajo: ¿interpolo en el espacio articular o en el cartesiano? Articular con jtraj: suave y barato para los motores, pero la punta no describe una recta, es la animación del miércoles. Cartesiano con ctraj más IK: la recta perfecta, pero puede exigir mucho a las articulaciones, y en el ejemplo del libro la manipulabilidad se hunde hacia el segundo 1,3 del recorrido, justo el valle que visteis ayer en vuestra gráfica. Soldadura y dispensado exigen cartesiano; un pick and place rápido, articular. Elegir es parte del oficio.");

acc("Descanso, min 55 a 65.");

cua("Cuaderno 82514_S19, min 65 a 90: quintic() y trapezoidal() escalares con sus gráficas, jtraj entre dos configuraciones, ctraj más IK con m(q) monitorizada.");
hab("Último taller del bloque, cuatro hitos. Uno: generad una quíntica y una trapezoidal escalares y mirad las tres gráficas, posición, velocidad y aceleración; localizad el tirón de la cúbica si la generáis para comparar. Dos: jtraj entre dos configuraciones del PUMA y observad la trayectoria de la punta, curva. Tres: la misma pareja de poses con ctraj más IK, punta recta, y graficad la manipulabilidad por el camino: el valle de ayer aparece en vuestro propio experimento. Cuatro, para quien vaya sobrado: probad a esquivar el valle cambiando la rama de IK de partida, que es la maniobra de oficio de la que hablamos ayer.");

piz("Mapa del bloque construido con la clase: Pose → FK → IK → Jacobiano → Singularidades → Estática y trayectorias, con flechas y una palabra por flecha.");
proy(29, "Las cinco ecuaciones del bloque", "min 90 a 105");
hab("Repaso final, y lo hacemos al revés de lo habitual: primero el mapa lo construís vosotros. Decidme las estaciones del bloque en orden y qué conecta cada una con la siguiente... Eso es: la pose describe, la FK predice, la IK invierte, el jacobiano deriva, la singularidad avisa y la estática traspone. Ahora sí, la diapositiva: las cinco ecuaciones que se llevan de este bloque. Os pido a cinco personas, una por tarjeta, que me digan qué significa y dónde la usamos esta semana. La ortonormalidad que define una rotación. La transformación homogénea que compone poses. El producto de exponenciales que da la FK. La ecuación diferencial que bautizó al jacobiano. Y la traspuesta que convierte fuerzas en pares. Si sabéis contar la historia que las une, el cuestionario de ahora mismo es un trámite.");

hab("Y con esto, cuestionario B4: quince minutos, diez preguntas, en Moodle, ahora. Es individual, con el material cerrado, y los errores más comunes los comentamos el lunes al abrir el bloque 5. Recordatorio de calendario mientras lo abrís: el parcial 1 es el viernes 6 de noviembre, dos horas, bloques 1 a 4; las partes C y D son exactamente los ejemplos resueltos de estas dos semanas con otros números, y el criterio de corrección premia plantear la cadena, la regla del atan2 y verificar con la FK. Cuando terminéis el cuestionario podéis salir. Ha sido un placer de bloque: nos vemos el lunes con los robots móviles.");
acc("Cuestionario, min 105 a 120.");

// ---------- documento ----------
const doc = new Document({
  numbering: numberingConfig,
  styles: { default: { document: { run: { font: F, size: 22 } } } },
  sections: [{ properties: { page: { margin: { top: 1200, bottom: 1200, left: 1350, right: 1350 } } }, children: C }],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync("Guion_Narrado_B4_Cinematica.docx", buf); console.log("OK guion narrado B4"); });
