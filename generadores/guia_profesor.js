// Guía del profesor 82514, discusiones, ejercicios y rúbricas
const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, PageBreak, AlignmentType } = require("docx");
const { IQS, F, p, pRuns, h1, h2, h3, bullet, box, tabla, numberingConfig } = require("./lib_iqs");
const DATOS = require("./guia_datos.json");
const FICHAS = require("./fichas_datos");

const C = [];

// ============================================================ utilidades de limpieza de markdown
function limpiarLinea(t) {
 let s = t
 .replace(/^#{1,6}\s*/, "")
 .replace(/\*\*([^*]+)\*\*/g, "$1")
 .replace(/(^|[\s(«, –])\*(\S[^*\n]*?)\*(?=[\s.,;:)»!?, –]|$)/g, "$1$2")
 .replace(/`([^`]*)`/g, "$1")
 .replace(/\s+/g, " ")
 .trim();
 return s;
}

// Trocea un texto markdown en bloques: prosa, código, viñetas o tabla.
function bloquesMd(texto) {
 const bloques = [];
 const trozos = texto.split(/```[a-zA-Z]*\n?/);
 trozos.forEach((trozo, i) => {
 if (i % 2 === 1) { // interior de un cerco de código
 const lineas = trozo.replace(/\s+$/, "").split("\n").filter(l => l.trim() !== "");
 if (lineas.length) bloques.push({ tipo: "code", lineas });
 return;
 }
 trozo.split(/\n\s*\n/).forEach(par => {
 const lineas = par.split("\n").map(l => l.replace(/\s+$/, "")).filter(l => l.trim() !== "");
 if (!lineas.length) return;
 if (lineas.every(l => l.trim().startsWith("|"))) {
 bloques.push({ tipo: "tabla", lineas });
 } else if (lineas.every(l => /^\s*[-*]\s+/.test(l))) {
 bloques.push({ tipo: "vinetas", items: lineas.map(l => limpiarLinea(l.replace(/^\s*[-*]\s+/, ""))) });
 } else {
 bloques.push({ tipo: "p", texto: limpiarLinea(lineas.join(" ")) });
 }
 });
 });
 return bloques;
}

function parrafoCodigo(linea) {
 return new Paragraph({
 spacing: { after: 20, line: 240 },
 indent: { left: 360 },
 children: [new TextRun({ text: linea, font: "Consolas", size: 17, color: "333333" })],
 });
}

function tablaMd(lineas) {
 const filas = lineas
 .map(l => l.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map(cld => limpiarLinea(cld)))
 .filter(cells => !cells.every(cld => /^[-: ]*$/.test(cld)));
 const headers = filas[0];
 const rows = filas.slice(1);
 const n = headers.length;
 const w0 = Math.min(2000, Math.round(9360 / n));
 const wr = Math.floor((9360 - w0) / (n - 1));
 const widths = [w0, ...Array(n - 1).fill(wr)];
 return tabla(headers.map(hh => hh === "" ? "-" : hh), rows, widths, { headerFill: IQS.navy2 });
}

// Vuelca un texto markdown como párrafos docx; el primer bloque de prosa lleva la etiqueta en negrita.
function volcarMd(texto, etiqueta, colorEtiqueta) {
 const out = [];
 let etiquetaPuesta = false;
 for (const b of bloquesMd(texto)) {
 if (b.tipo === "p") {
 if (!etiquetaPuesta) {
 out.push(pRuns([
 { text: etiqueta + " ", bold: true, color: colorEtiqueta },
 { text: b.texto },
 ]));
 etiquetaPuesta = true;
 } else {
 out.push(p(b.texto));
 }
 } else if (b.tipo === "code") {
 if (!etiquetaPuesta) {
 out.push(pRuns([{ text: etiqueta + " ", bold: true, color: colorEtiqueta }]));
 etiquetaPuesta = true;
 }
 b.lineas.forEach(l => out.push(parrafoCodigo(l)));
 out.push(new Paragraph({ spacing: { after: 100 }, children: [] }));
 } else if (b.tipo === "vinetas") {
 b.items.forEach(it => out.push(bullet(it)));
 } else if (b.tipo === "tabla") {
 out.push(tablaMd(b.lineas));
 out.push(new Paragraph({ spacing: { after: 100 }, children: [] }));
 }
 }
 return out;
}

// ============================================================ Portada
C.push(
 new Paragraph({ spacing: { before: 1900, after: 200 }, alignment: AlignmentType.CENTER,
 children: [new TextRun({ text: "82514, Mecatrónica y Robótica", size: 44, bold: true, color: IQS.navy, font: F })] }),
 new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 },
 children: [new TextRun({ text: "Guía del profesor: discusiones, ejercicios y rúbricas", size: 32, color: IQS.navy2, font: F })] }),
 new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
 children: [new TextRun({ text: "Las 39 discusiones en fichas de bolsillo, los 87 ejercicios de los cuadernos con su solución y todas las rúbricas de evaluación del semestre", size: 22, color: IQS.grey, font: F })] }),
 new Paragraph({ alignment: AlignmentType.CENTER,
 children: [new TextRun({ text: "Curso 2026/27 · IQS Universitat Ramon Llull", size: 20, color: IQS.grey, font: F })] }),
 new Paragraph({ children: [new PageBreak()] })
);

// ============================================================ 1. Cómo usar esta guía
C.push(h1("1. Cómo usar esta guía"));
C.push(p("Este documento reúne en un solo sitio las tres cosas que hay que tener a mano cuando se da la clase y cuando se corrige: la versión de bolsillo de cada una de las treinta y nueve discusiones del curso, la solución de los ochenta y siete ejercicios de los veintinueve cuadernos de Colab, y todas las rúbricas de la asignatura, la de participación, las cuatro de los entregables corregidos y las dos mayores, la de la defensa del proyecto y la del seminario."));
C.push(p("Lo que este documento no es: un sustituto de los apuntes. Cada uno de los ocho documentos de apuntes termina con una «Guía de conducción de las discusiones» donde cada discusión está desarrollada por extenso, objetivo, formato y tiempos, respuestas que van a salir y qué hacer con cada una, desvíos frecuentes, maniobra de rescate si la clase no habla, y cierre, todo con sus citas de página. Las fichas del apartado 4 condensan cada discusión en un tercio de página para poder llevarla al aula; cuando haga falta el desarrollo, cada ficha remite a su apunte. Por la misma razón, las fichas no llevan citas de página: las citas viven en el apunte."));
C.push(p("El uso previsto de cada pieza. Antes de la sesión, releer la ficha correspondiente: treinta segundos bastan para recuperar la pregunta literal y la respuesta que debe quedar establecida. Durante la sesión, la pregunta de apertura se formula tal cual está escrita, está redactada para hacer hablar, y reformularla en caliente suele estropearla. Después de la sesión, este documento sirve de solucionario (apartado 5) y de cuaderno de corrección (apartados 3, 6 y 7). El apartado 8 es la tabla de guardia: qué rúbrica se aplica a qué actividad y en qué fecha."));
C.push(box("Regla de esta guía", "Todo lo que aquí aparece condensado existe desarrollado en otro documento: las discusiones, en los apuntes de cada bloque; los ejercicios, en los propios cuadernos con su contexto ejecutable; el calendario administrativo, en «Tareas, pruebas y entregables». Esta guía no añade contenido nuevo salvo las rúbricas de los apartados 3 y 6, que son la pieza que faltaba, y la columna de evidencia observable del apartado 7."));

// ============================================================ 2. El método en una página
C.push(new Paragraph({ children: [new PageBreak()] }));
C.push(h1("2. El método en una página"));
C.push(p("El método general está desarrollado al principio de la guía de discusiones del bloque 1, y las guías de los bloques siguientes lo dan por supuesto. Esta es la versión condensada para repasar antes de clase; si algo de la lista chirría o se olvida en el aula, el desarrollo completo con sus porqués está en los apuntes del bloque 1."));
C.push(bullet("Formular la pregunta, callar y contar diez segundos mirando al grupo. Sin reformular, sin añadir un ejemplo, sin rebajar la pregunta: el silencio es del que piensa, no del que espera. Si el profesor se contesta dos veces el primer día, la clase aprende en veinte minutos que no hace falta contestar, y eso no se revierte en el semestre.", "Los diez segundos de silencio. "));
C.push(bullet("La cerrada de recuperación tiene una respuesta, se dirige por nombre y se corrige en segundos: su función es forzar memoria, no discutir. La abierta admite varias respuestas defendibles y se lanza al grupo. La prueba: si uno sabe de antemano la palabra exacta que quiere oír, la pregunta es cerrada y no abre discusión.", "Pregunta cerrada y pregunta abierta no se mezclan. "));
C.push(bullet("Enunciar la afirmación en forma binaria, votar todos a la vez a una señal, contar en voz alta y escribir el número en la pizarra sin comentarlo. Discutir. Votar otra vez y escribir el segundo número al lado. Lo que importa es el delta: hace tangible que un argumento ha movido votos y legitima públicamente cambiar de opinión ante un dato.", "Votación a mano alzada, antes y después. "));
C.push(bullet("No se le corta: se cierra su turno con una síntesis que le reconozca la aportación y se pide expresamente la voz de alguien que no haya hablado. Anunciar el primer día la regla de las dos intervenciones antes de repetir; anunciada no ofende, aplicada por sorpresa parece personal.", "El que monopoliza. "));
C.push(bullet("La pregunta abierta en frío lo expone y confirma su decisión de no participar. Lo que funciona es invertir el orden: un minuto de trabajo en parejas y después la pregunta dirigida por su nombre pero en plural, qué habéis dicho en la pareja, de modo que expone un producto compartido. Sin nombres no hay pregunta dirigida: aprenderse los nombres es la herramienta más rentable del primer día.", "El que no habla nunca. "));
C.push(bullet("Primero pedir el razonamiento (cómo has llegado ahí), después devolver al grupo (¿alguien lo ve de otra manera?), y solo al final cerrar nombrando la fuente y la página. A menudo el propio estudiante encuentra el error al explicarse, y entonces el coste social es nulo. Excepción: el error factual puro no se explora, se corrige en cinco segundos con la página.", "La respuesta errónea, en tres movimientos. "));
C.push(bullet("Toda discusión termina con una posición del profesor, aunque sea de segundo orden: dos frases que separen lo que queda decidido por la fuente de lo que queda legítimamente abierto, y la idea fuerza escrita en la pizarra. Lo que no se dice nunca: «cada uno tiene su opinión y todas valen igual», es falso en una asignatura con fuentes con página y anula los diez minutos anteriores.", "El cierre con posición. "));

// ============================================================ 3. Rúbrica de participación
C.push(new Paragraph({ children: [new PageBreak()] }));
C.push(h1("3. Rúbrica de participación en discusiones"));
C.push(p("La participación cuenta en la nota de actividades de seguimiento y se anuncia el primer día, junto con la regla de que las preguntas hechas en clase, también en el seminario, cuentan para quien las hace. Esta rúbrica fija qué se está mirando cuando se anota participación, con tres dimensiones y cuatro niveles. No es una plantilla de examen oral: es un vocabulario común para que las anotaciones de septiembre y las de diciembre midan lo mismo."));
C.push(tabla(
 ["Dimensión", "Sobresaliente", "Adecuado", "Insuficiente", "Ausente"],
 [
 ["Calidad del razonamiento",
 "Construye un argumento con criterio explícito y lo aplica al caso; distingue lo que sabe de lo que supone; cambia de posición ante un dato y lo dice",
 "Da una respuesta pertinente y la justifica cuando se le pide; el criterio está, aunque haya que extraérselo",
 "Opina sin criterio o recita la definición sin aplicarla; confunde error factual con juicio discutible",
 "No interviene ni con andamiaje (minuto en parejas, votación, pregunta dirigida)"],
 ["Uso de evidencia del taller o del libro",
 "Apoya la intervención en un resultado concreto del cuaderno o en una afirmación de la fuente, y sabe decir de dónde sale",
 "Usa evidencia cuando se le reclama, aunque necesite ayuda para localizarla",
 "Argumenta solo de memoria o intuición; la evidencia que cita no dice lo que él dice",
 "Ninguna evidencia en todo el periodo observado"],
 ["Escucha y construcción sobre otros",
 "Retoma la intervención de un compañero para refinarla o refutarla con respeto; sus preguntas abren juego a los demás",
 "Escucha y responde a lo que se ha dicho, sin limitarse a esperar su turno",
 "Interviene ignorando lo anterior; repite lo ya dicho o monopoliza",
 "Desconectado: ni escucha activa ni intervención"],
 ],
 [1560, 1950, 1950, 1950, 1950]
));
C.push(h3("Cómo usarla sin burocratizar"));
C.push(p("La rúbrica muere el día que obliga a rellenar una parrilla de treinta nombres por sesión. El procedimiento que funciona es la anotación en caliente de como máximo cinco estudiantes por sesión, rotando por la lista de clase: se decide antes de empezar a quiénes se observa hoy, sin anunciarlo, y al salir se apunta junto a cada nombre una letra por dimensión (S, A, I o guion) con una palabra de contexto si la hay. Son treinta segundos al acabar la clase. Con cuarenta y tres sesiones y cinco observados por sesión, cada estudiante acumula seis u ocho observaciones repartidas en el semestre, que es más de lo que ninguna memoria retiene y suficiente para que un mal día no pese."));
C.push(p("Dos reglas de higiene. La primera: la nota de participación sale del patrón de las observaciones, no de un promedio aritmético de letras, un estudiante que arranca en silencio y termina construyendo sobre otros está progresando, y eso es exactamente lo que se quiere premiar. La segunda: la anotación registra también al monopolizador, porque tres intervenciones brillantes que no dejan hablar a nadie puntúan en la primera dimensión y suspenden en la tercera, y tener eso escrito es lo que permite decírselo en tutoría con datos y sin juicio."));

// ============================================================ 4. Fichas de discusión
const NOMBRES_BLOQUE = {
 1: "Bloque 1 · Introducción a la mecatrónica (S1–S4)",
 2: "Bloque 2 · Tipología de robots y seguridad (S5–S7)",
 3: "Bloque 3 · Sensores y actuadores (S8–S12)",
 4: "Bloque 4 · Cinemática y estática (S13–S19)",
 5: "Bloque 5 · Modelado y control (S20–S24)",
 6: "Bloque 6 · Percepción y SLAM (S25–S31)",
 7: "Bloque 7 · ROS 2 y planificación (S32–S37)",
 8: "Bloque 8 · Robot learning y cierre (S38–S43)",
};
C.push(new Paragraph({ children: [new PageBreak()] }));
C.push(h1("4. Fichas de discusión"));
C.push(p("Una ficha por discusión, agrupadas por bloque: sesión y minutos, la pregunta de apertura literal, se formula tal cual, incluida la puesta en escena que a veces lleva delante, la respuesta que debe quedar establecida al cerrar, y la remisión al apunte donde está el desarrollo completo. La respuesta canónica no es un resumen neutral: es la posición con la que hay que cerrar, redactada a partir del cierre prescrito en la guía de conducción de cada bloque."));

const ETIQ_PREG = ["Pregunta de apertura: ", "Segunda pregunta: ", "Tercera pregunta: "];
let nFichas = 0;
for (const b of DATOS.bloques) {
 C.push(h2(NOMBRES_BLOQUE[b.bloque]));
 for (const d of b.discusiones) {
 const clave = `${d.bloque}|${d.sesion}|${d.minutos}`;
 const ficha = FICHAS[clave];
 if (!ficha) throw new Error("Falta ficha para " + clave);
 nFichas++;
 C.push(h3(`${d.sesion} · ${d.minutos}, ${ficha.corto}`));
 d.preguntas.slice(0, 3).forEach((q, i) => {
 C.push(pRuns([
 { text: ETIQ_PREG[i], bold: true, color: IQS.navy2 },
 { text: "«" + q + "»", italics: true },
 ]));
 });
 C.push(pRuns([
 { text: "La respuesta que debe quedar establecida: ", bold: true, color: IQS.greenDark },
 { text: ficha.resp },
 ]));
 C.push(pRuns([
 { text: "Desarrollo completo: ", bold: true, size: 19, color: IQS.grey },
 { text: `apuntes del bloque ${d.bloque}, sección «Guía de conducción», apartado «${d.titulo}», con las respuestas que van a salir, los desvíos frecuentes y la maniobra de rescate.`, size: 19, color: IQS.grey },
 ]));
 }
}

// ============================================================ 5. Ejercicios de los cuadernos
const TALLERES_EN_CLASE = new Set(["S10", "S13", "S15", "S16", "S19", "S22", "S25", "S28", "S34"]);
C.push(new Paragraph({ children: [new PageBreak()] }));
C.push(h1("5. Ejercicios de los cuadernos con su solución"));
C.push(p("Los veintinueve cuadernos de Colab llevan tres ejercicios cada uno, con sus soluciones al final del propio cuaderno: son de autocorrección deliberadamente, y su función es que el estudiante compruebe si ha entendido, no generar corrección. Este apartado reproduce los ochenta y siete pares enunciado–solución tal como están en los cuadernos, para poder corregir en común o atender una consulta sin abrir Colab. El régimen de trabajo: en las nueve sesiones de taller (S10, S13, S15, S16, S19, S22, S25, S28 y S34) los ejercicios se hacen en clase; en el resto de sesiones con cuaderno quedan como trabajo personal de la semana."));
C.push(p("Los cinco que más discusión generan, y que conviene reservar para hacer en común: el sensor con probabilidad de acierto 0,5 que no cambia la creencia (S28), el óptimo de isotropía del 2R que no está donde dice la intuición (S18), el óptimo teórico de la relación de transmisión que cae fuera de la ventana viable del motor (S12), la heurística inadmisible que expande menos nodos y devuelve un camino un veinte por ciento peor (S35), y la política condicionada por instrucción que resuelve la multimodalidad (S40)."));

let nEjercicios = 0;
for (const cu of DATOS.cuadernos) {
 C.push(h2(`${cu.sesion}, ${cu.titulo}`));
 const modo = TALLERES_EN_CLASE.has(cu.sesion)
 ? "taller: los ejercicios se hacen y se comentan en la propia sesión"
 : "cuaderno de apoyo: los ejercicios quedan como trabajo personal de la semana";
 C.push(pRuns([
 { text: "Cuaderno ", bold: true, size: 19, color: IQS.grey },
 { text: `${cu.fichero} · bloque ${cu.bloque} · ${cu.fecha} (${cu.duracion}) · ${modo}.`, size: 19, color: IQS.grey },
 ]));
 for (const e of cu.ejercicios) {
 nEjercicios++;
 volcarMd(e.enunciado, `Ejercicio ${e.n}.`, IQS.navy).forEach(x => C.push(x));
 volcarMd(e.solucion, "Solución.", IQS.greenDark).forEach(x => C.push(x));
 }
}

// ============================================================ 6. Rúbricas de los entregables corregidos
C.push(new Paragraph({ children: [new PageBreak()] }));
C.push(h1("6. Rúbricas de los entregables corregidos"));
C.push(p("De los entregables del semestre, cuatro se recogen y se devuelven con comentarios: la tabla de riesgos de S7, la tabla de ganancias del taller de PID de S22, los ficheros de calibración de S25 y el paquete de ROS 2 de S34. Estas cuatro rúbricas fijan los criterios de esa corrección. Formato común: cuatro criterios por cuatro niveles, pensados para corregir una entrega en cinco minutos marcando una casilla por fila y escribiendo una línea de comentario. El nivel «bien» es el esperable de un equipo que ha trabajado; «excelente» exige el criterio que separa al que ha entendido del que ha ejecutado."));

C.push(h2("6.1. Tabla de riesgos de la célula (S7, por equipos, se corrige en el aula)"));
C.push(p("El entregable: una tabla de seis filas sobre la célula del robot ABB del laboratorio con carga y descarga manual de piezas, peligro, tarea, estimación, medida y método colaborativo si aplica, aplicando los cinco pasos de la ISO 12100:2010 particularizados por la ISO 10218-2:2025. La corrección en común de la propia sesión ya desmonta los dos errores dominantes (saltarse los límites de la aplicación y abusar de la formación como medida); la rúbrica sirve para la revisión posterior y la devolución por escrito."));
C.push(tabla(
 ["Criterio", "Excelente", "Bien", "Suficiente", "Insuficiente"],
 [
 ["Proceso de cinco pasos",
 "Los límites de la aplicación están definidos antes de listar peligros; las filas recorren el proceso completo hasta la validación",
 "El proceso está entero, pero los límites son genéricos o la validación se queda en una frase",
 "Empieza directamente por la lista de peligros; el proceso se reconstruye a medias",
 "Filas sueltas sin proceso reconocible"],
 ["Peligros y modos degradados",
 "Peligros identificados por tarea, con al menos un modo degradado (limpieza, mantenimiento, recuperación de fallos) y su peligro propio",
 "Peligros pertinentes del ciclo normal; los modos degradados aparecen solo nombrados",
 "Peligros genéricos de catálogo, intercambiables con cualquier otra célula",
 "Peligros irrelevantes para la célula o repetidos entre filas"],
 ["Jerarquía de reducción",
 "Cada medida está en el escalón correcto (eliminar–proteger–informar) y ninguna fila de riesgo alto descansa en formación o señalización",
 "La jerarquía se respeta en general; alguna medida se queda un escalón por debajo de lo posible",
 "Mezcla escalones sin criterio; la formación aparece como medida principal en algún riesgo alto",
 "Casi todas las medidas son de información, o no reducen el riesgo estimado"],
 ["Estimación y coherencia",
 "La estimación combina severidad, exposición y evitabilidad; la medida es proporcional a la estimación y el método colaborativo, si aplica, está justificado",
 "Estimaciones razonables con justificación desigual entre filas",
 "Estimaciones sin criterio visible o incoherentes con la medida elegida",
 "Sin estimación, o con método colaborativo asignado a voleo"],
 ],
 [1560, 1950, 1950, 1950, 1950]
));

C.push(h2("6.2. Tabla de ganancias del taller de PID (S22, por parejas, se recoge en el aula)"));
C.push(p("El entregable: la terna final (Kp, Ki, Kd) con sus métricas Mp y ts medidas sobre el cuaderno del taller, que alimenta la tabla común de la puesta en común. La regla que gobierna esta rúbrica es la del propio taller: la especificación define una región de ternas válidas, no un punto, de modo que no se corrige contra unas «ganancias buenas», se corrige el proceso, las condiciones de medida y la interpretación."));
C.push(tabla(
 ["Criterio", "Excelente", "Bien", "Suficiente", "Insuficiente"],
 [
 ["Cumplimiento de la especificación",
 "La respuesta cumple Mp y ts con cifras medidas y adjuntas; si algo no se cumple, la pareja lo sabe, lo cuantifica y explica por qué",
 "Cumple, con métricas medidas pero sin comentar el margen",
 "Cumple solo una de las dos especificaciones, o las métricas no salen de la medición",
 "Terna sin métricas, o métricas incompatibles con la respuesta mostrada"],
 ["Condiciones de medida declaradas",
 "Banda de tolerancia del ts, amplitud del escalón y estado de la saturación y el anti-windup declarados: los números son reproducibles y comparables",
 "Falta una condición, y se recupera al preguntar",
 "Números sin condiciones: no se pueden comparar con los de otra pareja",
 "La pareja no sabe con qué banda ha medido su ts"],
 ["Proceso de sintonía",
 "Recorrido P → PD → PID visible; el Kd de amortiguamiento y la banda de estabilidad del Ki calculados, no tanteados a ciegas",
 "Proceso razonable con algún salto sin justificar",
 "Tanteo puro que llegó a algo; la pareja no sabría reproducirlo",
 "Ganancias copiadas o sin proceso alguno"],
 ["Interpretación del compromiso",
 "Sitúa su terna dentro de la región (más rápida o más robusta) y explica qué ha sacrificado; entiende el papel del anti-windup en su propia respuesta",
 "Interpreta correctamente cuando se le pregunta",
 "Cree que su terna es «la buena» y que las demás están mal",
 "No sabe explicar el efecto de ninguna de las tres ganancias"],
 ],
 [1560, 1950, 1950, 1950, 1950]
));

C.push(h2("6.3. Calibración de la cámara (S25, por equipos, campus el mismo día)"));
C.push(p("El entregable: los ficheros de calibración de la cámara del equipo, intrínsecos, coeficientes de distorsión y error de reproyección, con las vistas usadas, subidos al campus el mismo día. Es el único entregable que se reutiliza: la parte de percepción del proyecto usará esta calibración en diciembre. Por eso la rúbrica pesa la verificación tanto como el número: la lección de la puesta en común es que el error de reproyección mide el ajuste, no la exactitud."));
C.push(tabla(
 ["Criterio", "Excelente", "Bien", "Suficiente", "Insuficiente"],
 [
 ["Cobertura de las vistas",
 "Vistas suficientes y variadas: inclinaciones marcadas, patrón en bordes y esquinas del campo, distancias distintas",
 "Cobertura razonable con los bordes del campo flojos",
 "Pocas vistas, o casi todas frontales y centradas",
 "Vistas insuficientes o repetidas: la distorsión no queda restringida"],
 ["Error de reproyección y su lectura",
 "Por debajo del criterio de 0,5 píxeles, y el equipo sabe qué mide y qué no mide ese número; si eliminó vistas malas, lo justifica",
 "Número correcto con interpretación parcial",
 "Número correcto interpretado como exactitud garantizada, o vistas eliminadas solo para «bajar la nota»",
 "Error por encima del criterio sin diagnóstico"],
 ["Verificación externa",
 "Comprobación contra algo que no entró en el ajuste: vista reservada, coherencia de la focal con la óptica y el tamaño de píxel, o medida de una pieza conocida",
 "Una verificación hecha, con ayuda",
 "Verificación mencionada pero no realizada",
 "Ninguna verificación: solo el número interno"],
 ["Ficheros y trazabilidad",
 "Formato reutilizable directamente en el proyecto, identificado (equipo, cámara, óptica, fecha) y con las vistas archivadas",
 "Reutilizable con retoques menores",
 "Falta identificación o faltan las vistas: habrá que rehacer parte en diciembre",
 "Ficheros ilegibles o incompletos"],
 ],
 [1560, 1950, 1950, 1950, 1950]
));

C.push(h2("6.4. Paquete de ROS 2 (S34, por parejas, campus el fin de semana)"));
C.push(p("El entregable: el paquete del taller funcionando, nodo publicador y suscriptor en rclpy, construido con colcon en su workspace, más las dos evidencias de introspección: la captura de rqt_graph con el grafo completo y el frames.pdf del árbol de transformadas. La rúbrica premia lo mismo que la puesta en común de errores de la sesión: que el sistema funcione en otra máquina y que la pareja sepa leer su propio grafo."));
C.push(tabla(
 ["Criterio", "Excelente", "Bien", "Suficiente", "Insuficiente"],
 [
 ["Construcción y ejecución",
 "colcon build limpio y ros2 run arranca los nodos en un workspace recién clonado; instrucciones mínimas incluidas",
 "Construye y ejecuta con algún aviso o con un paso manual sin documentar",
 "Construye, pero la ejecución exige arreglos, o solo funciona en la máquina de los autores",
 "No construye"],
 ["Nodos e interfaces",
 "Publicador y suscriptor con nombres, tipos de mensaje y QoS elegidos deliberadamente y coherentes con la semántica del canal",
 "Funciona con los valores por defecto, sin decisión consciente de QoS",
 "Nombres o tipos mal elegidos aunque el conjunto funcione",
 "Los nodos no llegan a comunicarse"],
 ["Evidencia de introspección",
 "rqt_graph muestra el grafo completo esperado y frames.pdf un árbol coherente; la pareja explica cada arista y quién la publica",
 "Capturas correctas con explicación incompleta",
 "Capturas presentes pero con el grafo a medias, o sin saber explicarlas",
 "Sin capturas, o capturas que no corresponden a su sistema"],
 ["Calidad del paquete",
 "package.xml y setup.py coherentes, nombres con convención, sin residuos de build en la entrega",
 "Detalles menores: dependencias de más, nombres mejorables",
 "Desordenado pero evaluable",
 "Estructura de paquete rota"],
 ],
 [1560, 1950, 1950, 1950, 1950]
));

// ============================================================ 7. Las rúbricas mayores
C.push(new Paragraph({ children: [new PageBreak()] }));
C.push(h1("7. Las rúbricas mayores: defensa del proyecto y seminario"));
C.push(p("Las dos rúbricas con más peso del curso, reproducidas del documento de tareas y entregables con una columna añadida: la evidencia observable, es decir, qué tiene que verse u oírse en la sala para marcar alto esa dimensión. La columna existe para corregir en directo sin discusiones posteriores: si la evidencia no ha aparecido, la dimensión no puntúa alto, por buena que fuera la intención."));
C.push(h2("7.1. Defensa del proyecto integrador (S43 · 18 dic, 12 min de defensa y 5 de preguntas, más memoria)"));
C.push(tabla(
 ["Peso", "Dimensión", "Qué se valora", "Evidencia observable"],
 [
 ["40%", "Integración técnica",
 "¿Los módulos hablan entre sí, hay un sistema, o cuatro prácticas juntas? Es la competencia RAM23-S de la guía docente",
 "Una demostración o vídeo donde la salida de un módulo alimenta al siguiente sin intervención manual; un diagrama de interfaces con tipos, frames y QoS; cualquier miembro sabe decir qué pasa aguas abajo cuando un módulo falla"],
 ["25%", "Resultados medidos",
 "Al menos una métrica cuantitativa: error de seguimiento, tiempo de ciclo, tasa de éxito en N intentos, error de localización",
 "Una tabla o gráfica con números propios y con las condiciones de medida declaradas (banda, número de intentos, escenario); no valen capturas de pantalla sin ejes ni adjetivos sin cifra"],
 ["20%", "Análisis crítico",
 "Limitaciones reconocidas, diagnóstico de lo que falló, camino propuesto",
 "Una lista de limitaciones que aparece sin que haya que preguntarla; al menos un fallo con su causa diagnosticada, no descrita; una propuesta de siguiente paso con su coste estimado"],
 ["15%", "Claridad y reparto",
 "Exposición ordenada y participación real de todos: la defensa es individual dentro del equipo",
 "Los cuatro hablan y responden preguntas fuera de su parte; hay un hilo problema–sistema–resultados–límites; los 12 minutos se respetan sin que el tribunal corte"],
 ],
 [700, 1550, 3300, 3810]
));
C.push(p("El criterio que se dice en voz alta antes de la primera defensa, porque está en los apuntes del bloque 8 y pierde fuerza si solo se aplica en silencio: un proyecto que no llegó a funcionar del todo, pero cuyo equipo sabe por qué, lo ha medido y propone un camino, puntúa por encima de uno que funciona sin que nadie sepa explicarlo."));
C.push(h2("7.2. Seminario de artículos (S41–S42 · 16 y 17 dic, 10 min por pareja y 5 de preguntas)"));
C.push(tabla(
 ["Peso", "Dimensión", "Qué se valora", "Evidencia observable"],
 [
 ["40%", "Comprensión técnica",
 "¿Entienden el método o repiten el resumen? Se comprueba en las preguntas, no en las diapositivas",
 "Explican el método con un ejemplo o esquema propio, no con la figura del artículo; sobreviven a un «¿qué pasaría si…?» sobre el método; distinguen lo que el artículo demuestra de lo que promete"],
 ["30%", "Claridad",
 "Estructura, ritmo, calidad de las figuras, capacidad de hacer accesible lo complejo",
 "Una figura propia o adaptada que se entiende en diez segundos; el guion problema–método–resultados–limitaciones–conexión con el curso es reconocible; los diez minutos se cumplen sin atropello final"],
 ["20%", "Análisis crítico",
 "Limitaciones reconocidas y no reconocidas, honestidad de la comparación, aplicabilidad real",
 "Nombran al menos una limitación que el artículo no reconoce; la comparación usa una línea base sensata; la conexión con un bloque del curso es concreta, no protocolaria"],
 ["10%", "Gestión de preguntas",
 "Responder lo que se sabe, admitir lo que no y razonar en voz alta",
 "Contestan sin escaparse de la pregunta; al menos un «no lo sé» limpio si toca, seguido de un razonamiento en voz alta de cómo se averiguaría"],
 ],
 [700, 1550, 3300, 3810]
));
C.push(p("Recordatorio operativo para S41: anunciar al abrir la sesión que las preguntas del público cuentan para la participación de quien las hace, es lo que evita la sala muda, y que la conexión explícita con al menos un bloque del curso es obligatoria en cada presentación."));

// ============================================================ 8. Cierre: qué rúbrica, a qué, cuándo
C.push(new Paragraph({ children: [new PageBreak()] }));
C.push(h1("8. Qué rúbrica se aplica a qué actividad, y cuándo"));
C.push(tabla(
 ["Rúbrica", "Actividad y agrupación", "Cuándo"],
 [
 ["Participación en discusiones (apdo. 3)", "Las 39 discusiones de esta guía; anotación en caliente de 5 estudiantes por sesión, rotando", "Todo el semestre"],
 ["Tabla de riesgos (apdo. 6.1)", "Taller de análisis de riesgos de la célula, por equipos", "S7 · vie 25 sep"],
 ["Ganancias del PID (apdo. 6.2)", "Taller de PID, por parejas", "S22 · vie 30 oct"],
 ["Calibración de cámara (apdo. 6.3)", "Ficheros de calibración, por equipos, se reutilizan en el proyecto", "S25 · vie 6 nov"],
 ["Paquete de ROS 2 (apdo. 6.4)", "Entregable del taller de ROS 2, por parejas", "S34 · vie 27 nov (campus, fin de semana)"],
 ["Seminario (apdo. 7.2)", "Presentaciones del seminario de artículos, por parejas", "S41–S42 · 16 y 17 dic"],
 ["Defensa del proyecto (apdo. 7.1)", "Defensa oral de los 5 equipos, más memoria", "S43 · vie 18 dic"],
 ],
 [2900, 4000, 2460]
));
C.push(p("Lo que deliberadamente no lleva rúbrica: los 87 ejercicios de los cuadernos se autocorrigen con las soluciones del apartado 5 y de los propios cuadernos; los ocho cuestionarios de bloque se corrigen automáticamente en el campus y se comentan los dos errores más frecuentes al abrir la sesión siguiente; y los deberes previos no se recogen, se comprueban con la pregunta de recuperación de los primeros cinco minutos. Mantener esas tres familias fuera de la maquinaria de rúbricas es lo que hace sostenible aplicar bien las siete que sí la llevan."));

// ============================================================ generación
const doc = new Document({
 numbering: numberingConfig,
 styles: { default: { document: { run: { font: F, size: 22 } } } },
 sections: [{ properties: { page: { margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } }, children: C }],
});
Packer.toBuffer(doc).then(b => {
 fs.writeFileSync("Guia_Profesor_Discusiones_Ejercicios_82514.docx", b);
 console.log(`OK guia profesor, fichas: ${nFichas}, ejercicios: ${nEjercicios}`);
});
