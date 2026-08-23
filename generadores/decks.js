const pptxgen = require("pptxgenjs");

// Paleta IQS
const NAVY = "1B2A80";
const NAVY_LT = "2E3FA3";
const GREEN = "2FD26E";
const GREEN_DK = "1FA355";
const GREY = "595959";
const BG_LT = "F2F4FB";
const WHITE = "FFFFFF";
const INK = "1A1A2E";

const W = 13.33, H = 7.5;

function newDeck() {
 const p = new pptxgen();
 p.layout = "LAYOUT_WIDE";
 return p;
}

// Diagonal IQS: triángulo navy-claro en esquina
function diag(slide, opts = {}) {
 slide.addShape("rtTriangle", {
 x: opts.x ?? -0.02, y: opts.y ?? 3.4, w: opts.w ?? 5.6, h: opts.h ?? 4.12,
 fill: { color: opts.color ?? NAVY_LT }, line: { type: "none" },
 flipH: opts.flipH ?? false, rotate: opts.rotate ?? 0,
 });
}

function titleSlide(p, { curso, bloque, titulo, sub, fechas }) {
 const s = p.addSlide();
 s.background = { color: NAVY };
 diag(s, { x: 7.9, y: 2.6, w: 5.45, h: 4.92, flipH: true, color: NAVY_LT });
 s.addShape("rtTriangle", { x: 10.4, y: 4.9, w: 2.95, h: 2.62, fill: { color: GREEN }, line: { type: "none" }, flipH: true, transparency: 12 });
 s.addImage({ path: MEDIA + "logo_iqs_blanco.png", x: 0.7, y: 0.42, w: 1.3, h: 1.3 });
 s.addText(curso, { x: 0.7, y: 2.5, w: 9.5, h: 0.5, fontFace: "Calibri", fontSize: 18, color: GREEN, bold: true, margin: 0 });
 s.addText(bloque, { x: 0.7, y: 3.0, w: 9.0, h: 0.6, fontFace: "Calibri", fontSize: 22, color: WHITE, margin: 0 });
 s.addText(titulo, { x: 0.7, y: 3.55, w: 8.6, h: 1.7, fontFace: "Calibri", fontSize: 40, bold: true, color: WHITE, margin: 0 });
 s.addText(sub, { x: 0.7, y: 5.5, w: 8.0, h: 0.5, fontFace: "Calibri", fontSize: 16, color: "C9D2F5", margin: 0 });
 s.addText(fechas, { x: 0.7, y: 6.0, w: 8.0, h: 0.5, fontFace: "Calibri", fontSize: 14, color: "9AA7E8", margin: 0 });
 return s;
}

function sectionSlide(p, num, titulo, sub, notas, foto) {
 const s = p.addSlide();
 s.background = { color: NAVY };
 diag(s, { x: -0.02, y: 3.1, w: 6.4, h: 4.42, color: NAVY_LT });
 s.addShape("rtTriangle", { x: -0.02, y: 5.3, w: 3.2, h: 2.22, fill: { color: GREEN }, line: { type: "none" }, transparency: 10 });
 s.addShape("ellipse", { x: 0.75, y: 1.15, w: 1.15, h: 1.15, fill: { color: GREEN }, line: { type: "none" } });
 s.addText(num, { x: 0.75, y: 1.15, w: 1.15, h: 1.15, align: "center", valign: "middle", fontFace: "Calibri", fontSize: 30, bold: true, color: NAVY, margin: 0 });
 s.addText(titulo, { x: 2.2, y: 1.0, w: 10.3, h: 1.5, valign: "middle", fontFace: "Calibri", fontSize: 34, bold: true, color: WHITE, margin: 0 });
 s.addText(sub, { x: 2.25, y: 2.5, w: 9.8, h: 0.9, fontFace: "Calibri", fontSize: 16, color: "C9D2F5", margin: 0 });
 if (foto) {
 const b = img(s, foto.f, 8.55, 3.32, 4.1, 3.2);
 s.addShape("rect", { x: b.x, y: b.y + b.h, w: b.w, h: 0.06, fill: { color: GREEN }, line: { type: "none" } });
 if (foto.cap) s.addText(foto.cap, { x: 8.3, y: b.y + b.h + 0.14, w: 4.55, h: 0.55, fontFace: "Calibri", fontSize: 10, color: "C9D2F5", align: "center", margin: 0 });
 if (foto.credito) s.addText(foto.credito, { x: 7.3, y: 7.14, w: 5.55, h: 0.25, fontFace: "Calibri", fontSize: 8, color: "8A97D8", align: "right", margin: 0 });
 }
 if (notas) s.addNotes(notas);
 return s;
}

function contentSlide(p, titulo, kicker) {
 const s = p.addSlide();
 s.background = { color: WHITE };
 if (kicker) s.addText(kicker.toUpperCase(), { x: 0.7, y: 0.38, w: 11.9, h: 0.3, fontFace: "Calibri", fontSize: 12, bold: true, color: GREEN_DK, charSpacing: 2, margin: 0 });
 s.addText(titulo, { x: 0.7, y: 0.62, w: 11.9, h: 0.75, fontFace: "Calibri", fontSize: 30, bold: true, color: NAVY, margin: 0 });
 return s;
}

function card(s, x, y, w, h, { title, body, fill = BG_LT, titleColor = NAVY, num, numFill = GREEN, numColor = NAVY, bodySize = 12.5, titleSize = 15 }) {
 s.addShape("roundRect", { x, y, w, h, rectRadius: 0.08, fill: { color: fill }, line: { type: "none" } });
 let tx = x + 0.22, tw = w - 0.44, ty = y + 0.16;
 if (num) {
 s.addShape("ellipse", { x: x + 0.2, y: y + 0.2, w: 0.5, h: 0.5, fill: { color: numFill }, line: { type: "none" } });
 s.addText(num, { x: x + 0.2, y: y + 0.2, w: 0.5, h: 0.5, align: "center", valign: "middle", fontFace: "Calibri", fontSize: 16, bold: true, color: numColor, margin: 0 });
 tx = x + 0.85; tw = w - 1.05;
 }
 if (title) s.addText(title, { x: tx, y: ty, w: tw, h: 0.55, fontFace: "Calibri", fontSize: titleSize, bold: true, color: titleColor, valign: "middle", margin: 0 });
 const by = title ? y + (num ? 0.85 : 0.7) : y + 0.12;
 s.addText(body, { x: x + 0.22, y: by, w: w - 0.44, h: h - (by - y) - 0.14, fontFace: "Calibri", fontSize: bodySize, color: INK, valign: "middle", margin: 0 });
}

function bullets(s, items, { x = 0.7, y = 1.6, w = 6.0, h = 5.3, size = 14 } = {}) {
 const arr = [];
 items.forEach((it, i) => {
 const fin = i < items.length - 1;
 if (it.h) arr.push({ text: it.t, options: { bold: true, color: NAVY, fontSize: size + 1, bullet: false, paraSpaceAfter: 4, breakLine: true } });
 else if (it.r) it.r.forEach((sg, j) => arr.push({ text: sg.t, options: { bullet: j === 0 ? { code: "2022", indent: 14 } : false, color: INK, fontSize: size, subscript: !!sg.sub, paraSpaceAfter: 8, breakLine: j === it.r.length - 1 ? fin : false } }));
 else arr.push({ text: it.t, options: { bullet: { code: "2022", indent: 14 }, color: INK, fontSize: size, paraSpaceAfter: 8, breakLine: fin } });
 });
 s.addText(arr, { x, y, w, h, fontFace: "Calibri", valign: "top", margin: 0 });
}

function footer(s, txt) {
 s.addText(txt, { x: 0.7, y: 7.05, w: 12.0, h: 0.3, fontFace: "Calibri", fontSize: 10, color: GREY, margin: 0 });
}


// ── Diapositivas de material visual (fotos con licencia, figuras y GIFs) ──
const MEDIA = __dirname + "/media/";
const DIMS = require("./media/dims.json");
function fit(fich, x, y, w, h) {
 const d = DIMS[fich];
 if (!d) throw new Error("sin dims: " + fich);
 const r = Math.min(w / d[0], h / d[1]);
 const fw = d[0] * r, fh = d[1] * r;
 return { x: x + (w - fw) / 2, y: y + (h - fh) / 2, w: fw, h: fh };
}
function img(s, fich, x, y, w, h) {
 const b = fit(fich, x, y, w, h);
 s.addImage({ path: MEDIA + fich, x: b.x, y: b.y, w: b.w, h: b.h });
 return b;
}
function eqImg(s, clave, x, y, w, hmax) {
 const d = DIMS["eq/" + clave + ".png"];
 let fw = w, fh = w * d[1] / d[0];
 if (hmax && fh > hmax) { fh = hmax; fw = hmax * d[0] / d[1]; }
 s.addImage({ path: MEDIA + "eq/" + clave + ".png", x: x + (w - fw) / 2, y, w: fw, h: fh });
 return fh;
}
function slideFotos(pres, titulo, kicker, items, credito, notas) {
 const s = contentSlide(pres, titulo, kicker);
 items.forEach(it => {
 const b = img(s, it.f, it.x, it.y, it.w, it.h);
 if (it.cap) s.addText(it.cap, { x: it.x, y: Math.min(b.y + b.h + 0.04, 6.92), w: it.w, h: 0.32, fontFace: "Calibri", fontSize: 10.5, color: GREY, align: "center", margin: 0 });
 });
 if (credito) footer(s, credito);
 if (notas) s.addNotes(notas);
 return s;
}

/* ==================== DECK B1 ==================== */
const p1 = newDeck();

titleSlide(p1, {
 curso: "82514 · MECATRÓNICA Y ROBÓTICA",
 bloque: "Bloque 1",
 titulo: "Introducción a la mecatrónica\ny panorama 2026 de la robótica",
 sub: "Sesiones S1–S4 · 4 horas",
 fechas: "9, 10, 16 y 17 de septiembre de 2026 · IQS Universitat Ramon Llull",
});

// Agenda
{
 const s = contentSlide(p1, "Hoja de ruta del bloque", "Bloque 1");
 const rows = [
 ["S1 · mié 9 sep · 1 h", "¿Qué es la mecatrónica? Definición, dominios y componentes"],
 ["S2 · jue 10 sep · 1 h", "El proceso de diseño mecatrónico: diseño acoplado y MDQ"],
 ["S3 · mié 16 sep · 1 h", "Historia de la robótica y definición de robot"],
 ["S4 · jue 17 sep · 1 h", "Panorama 2026, ética y lanzamiento del seminario de artículos"],
 ];
 rows.forEach((r, i) => {
 const y = 1.7 + i * 1.25;
 card(s, 0.7, y, 11.9, 1.05, { title: r[0], body: r[1], num: String(i + 1), bodySize: 13, titleSize: 14 });
 });
 s.addNotes("Presentar el bloque como el «porqué» del curso: vocabulario, método de diseño y contexto. El cuestionario de seguimiento del bloque cierra S4.");
 footer(s, "82514 Mecatrónica y Robótica · B1 · IQS");
}

// S1 section
sectionSlide(p1, "S1", "¿Qué es la mecatrónica?", "Definición · sistemas multidominio · componentes · ejemplos", "0-10 presentación asignatura; 10-15 pregunta de arranque (objetos mecatrónicos cotidianos); 15-35 definición y dominios; 35-50 componentes y ejemplos; 50-60 discusión y cierre.");

{
 const s = contentSlide(p1, "Una definición con dos palabras clave", "S1 · Definición");
 bullets(s, [
 { t: "Aplicación sinérgica de la mecánica, la electrónica, el control y la informática", h: true },
 { t: "…al desarrollo de productos electromecánicos mediante un enfoque de diseño integrado (De Silva, cap. 1)." },
 { t: "Sinergia: los subsistemas se conciben y optimizan juntos, no se yuxtaponen." },
 { t: "Integrado: las interacciones dinámicas entran en el diseño desde la primera fase." },
 { t: "El término lo acuñó Yasakawa Electric (Japón) en 1969; marca registrada en 1972, liberada en 1982." },
 ], { w: 6.6 });
 card(s, 7.6, 1.7, 5.0, 4.6, {
 title: "Sistema multidominio: el ABS",
 body: "Frenos antibloqueo de un automóvil:\n\n• Mecánica, dinámica del vehículo y de la rueda\n• Electrónica, sensores de giro y ECU\n• Hidráulica, circuito de frenado\n• Térmica, disipación en los discos\n\nDiseñarlo de forma «óptima» exige tratarlo como un único producto mecatrónico.",
 bodySize: 13,
 });
 s.addNotes("Insistir: electromecánico ≠ mecatrónico. La mecatrónica es una metodología de diseño, no una lista de piezas. La historia del término (nace en la industria japonesa) conecta con la historia de la robótica de S3.");
 footer(s, "De Silva, Mechatronics: Fundamentals and Applications, cap. 1");
}

{
 const s = contentSlide(p1, "Componentes de un sistema mecatrónico", "S1 · Anatomía");
 const comps = [
 ["Esqueleto mecánico", "Estructura y mecanismos, bloque 4"],
 ["Actuadores", "Motores, hidráulica, neumática, bloque 3"],
 ["Sensores", "Propioceptivos y exteroceptivos, bloque 3"],
 ["Controladores", "Lazos de control, bloque 5"],
 ["Acondicionamiento de señal", "Amplificación, filtrado, conversión A/D"],
 ["Hardware y software digital", "Computación embebida, bloque 7"],
 ["Interfaces", "Comunicación entre dominios y con el usuario"],
 ["Fuentes de alimentación", "Energía: el hilo unificador del diseño"],
 ];
 comps.forEach((c, i) => {
 const col = i % 4, row = Math.floor(i / 4);
 card(s, 0.7 + col * 3.075, 1.75 + row * 2.5, 2.85, 2.25, { title: c[0], body: c[1], num: String(i + 1), bodySize: 12, titleSize: 13.5 });
 });
 s.addNotes("Esta lista de De Silva es literalmente el índice de la asignatura: señalarlo en voz alta. Ejemplo anidado: el servomotor es un sistema mecatrónico completo dentro de otro mayor.");
 footer(s, "De Silva, cap. 1 · La lista es el índice del curso");
}

{
 const s = contentSlide(p1, "Dos ejemplos canónicos", "S1 · Ejemplos");
 card(s, 0.7, 1.7, 5.9, 4.9, {
 title: "El disco duro (HDD)",
 body: "Mecatrónica en miniatura:\n\n• Platos a 7200 rpm; cabezal «volando» a nanómetros de la superficie\n• Motor de husillo + actuador de bobina móvil para el brazo\n• Posición embebida en las pistas (sensado)\n• Lazo de seguimiento con precisión submicrométrica\n\nPregunta: ¿por qué el servo del brazo no puede diseñarse sin conocer la mecánica del brazo? (resonancias, masa móvil → bloque 5)",
 bodySize: 13,
 });
 card(s, 6.85, 1.7, 5.75, 4.9, {
 title: "El servomotor",
 body: "El «átomo» de la robótica:\n\n• Mecánica, rotor, estátor, rodamientos, encoder óptico\n• Eléctrica, bobinados, etapa de potencia, conmutación\n• Control, lazo cerrado de posición / velocidad\n\nUn robot industrial de 6 ejes = 6 servomotores coordinados + un esqueleto.\n\nAplicaciones (De Silva): transporte, fabricación, medicina, hogar, espacio… «no hay límite».",
 bodySize: 13,
 });
 s.addNotes("Cerrar S1 recuperando la lista de objetos de la pregunta inicial: ¿cuáles eran de verdad mecatrónicos según la definición?");
 footer(s, "De Silva, cap. 1");
}

// S2
sectionSlide(p1, "S2", "El proceso de diseño mecatrónico", "Bucle modelado-diseño · diseño acoplado · MDQ · evolución de diseño", "0-5 recuperación; 5-20 modelado y diseño; 20-40 diseño acoplado y MDQ; 40-52 caso práctico en parejas (cinta transportadora); 52-60 cierre.");

{
 const s = contentSlide(p1, "Modelado y diseño: un bucle iterativo", "S2 · Método");
 const steps = ["Objetivos y especificaciones", "Modelo del sistema", "Predicción del desempeño", "Decisiones de diseño", "Refinamiento del modelo"];
 steps.forEach((t, i) => {
 card(s, 0.7 + i * 2.5, 1.9, 2.25, 1.5, { title: `${i + 1}`, body: t, fill: i % 2 ? BG_LT : "E3F7EC", bodySize: 12.5, titleSize: 16 });
 if (i < 4) s.addText("→", { x: 2.9 + i * 2.5, y: 2.3, w: 0.35, h: 0.6, fontSize: 20, bold: true, color: GREEN_DK, align: "center", margin: 0 });
 });
 bullets(s, [
 { t: "«Un modelo es una representación de un sistema real», y el bucle se recorre varias veces.", },
 { t: "La energía como hilo unificador: la potencia enlaza dominios (v·i = ω·τ) y la disipación mínima es objetivo de diseño (eficiencia, térmica, ruido, desgaste)." },
 { t: "Cuidado con los factores de seguridad excesivos y el diseño por «peor caso»: no dan diseños óptimos ni más baratos." },
 { t: "Este bucle estructura el proyecto integrador: modelo cinemático (B4) → control (B5) → percepción y navegación (B6–B7)." },
 ], { y: 3.8, w: 11.9, h: 3.0 });
 s.addNotes("Dibujar el bucle en pizarra aunque esté en pantalla: el gesto de cerrar el ciclo importa. v·i = ω·τ: potencia eléctrica de entrada igual a potencia mecánica de salida en el transformador ideal.");
 footer(s, "De Silva, cap. 1, fig. 1.3");
}

{
 const s = contentSlide(p1, "Por qué falla el diseño secuencial", "S2 · Diseño no acoplado");
 const probs = [
 ["Las características cambian", "Al interconectar dos componentes diseñados por separado, la carga y las interacciones dinámicas alteran sus condiciones de operación originales."],
 ["El acoplamiento perfecto es imposible", "Un componente quedará subutilizado o sobrecargado; ambas condiciones son ineficientes y no deseables."],
 ["Aparecen variables ocultas", "Variables externas pasan a ser internas tras la interconexión: ya no pueden monitorizarse con sensores ni controlarse directamente."],
 ];
 probs.forEach((c, i) => card(s, 0.7 + i * 4.05, 1.8, 3.8, 3.1, { title: c[0], body: c[1], num: String(i + 1), bodySize: 12.5 }));
 card(s, 0.7, 5.2, 11.9, 1.5, {
 title: "El enfoque tradicional",
 body: "Mecánica primero → electrónica después → computador → controlador al final. Cada subsistema se diseña «congelando» sus interacciones con el resto: eso es el diseño no acoplado.",
 fill: "E3F7EC", bodySize: 13,
 });
 s.addNotes("Ejemplo motor de catálogo: el par-velocidad nominal deja de cumplirse con la inercia real de la transmisión. Estos tres problemas justifican todo el marco MDQ de la siguiente diapositiva.");
 footer(s, "De Silva, cap. 1");
}

{
 const s = contentSlide(p1, "El Cociente de Diseño Mecatrónico (MDQ)", "S2 · Diseño acoplado");
 bullets(s, [
 { t: "Índice de diseño I: grado en que un diseño satisface sus especificaciones.", },
 { t: "Aislados, cada subsistema alcanza su óptimo (Iue eléctrico, Ium mecánico); interconectados, ninguno lo alcanza." },
 { t: "Diseño mecatrónico = optimización conjunta: minimizar el coste J o maximizar el MDQ (ecs. 1.2 y 1.4; De Silva et al., 2016, pp. 6-7):" },
 ], { w: 6.9, h: 2.4 });
 eqImg(s, "mdq_j", 0.95, 4.05, 6.2, 0.52);
 eqImg(s, "mdq", 1.45, 4.85, 5.2, 1.15);
 s.addText("Generalizable: fiabilidad, mantenibilidad, eficiencia, coste, tamaño, facilidad de control, inteligencia.", { x: 0.95, y: 6.25, w: 6.6, h: 0.5, fontFace: "Calibri", fontSize: 11.5, color: GREY, margin: 0 });
 card(s, 7.9, 1.7, 4.7, 4.9, {
 title: "Optimización con algoritmos genéticos",
 body: "• Cromosoma = un diseño completo\n• Gen = un elemento de información (componente, conexión, parámetro)\n• Alelos = opciones disponibles\n• Función de aptitud = el MDQ\n\nJerárquico: una capa elige el tipo de actuador (hidráulico, DC, inducción, paso a paso); otra, el motor concreto del catálogo.",
 bodySize: 13,
 });
 s.addNotes("Las fórmulas se interpretan, no se manipulan en el examen. Lectura: el MDQ mide cuánto se acerca el conjunto al ideal de cada dominio; el diseño mecatrónico busca el mejor compromiso global, no el óptimo local. Cerrar con evolución de diseño (5 etapas) e instrumentación integrada: contar el caso del transporte guiado (restricciones heredadas).");
 footer(s, "De Silva, cap. 1, ecs. 1.1–1.5");
}

// S3
sectionSlide(p1, "S3", "Historia y definición de robot", "De los autómatas a Unimation · percibir, planificar, actuar", "0-5 recuperación; 5-25 historia como narrativa; 25-40 definición y sensores; 40-55 telerobots y autonomía + discusión; 55-60 cierre.");

slideFotos(p1, "Tres máquinas que cuentan la historia", "S1–S3 · Imágenes", [
 { f: "fotos/b1_unimate.jpg", x: 0.7, y: 1.5, w: 6.2, h: 4.7, cap: "Unimate sirviendo café, Biltmore Hotel, 1967" },
 { f: "fotos/b1_jacquard.jpg", x: 7.15, y: 1.5, w: 5.45, h: 2.42, cap: "Telar de Jacquard: el programa en tarjetas perforadas" },
 { f: "fotos/b1_hdd.jpg", x: 7.15, y: 4.35, w: 5.45, h: 1.85, cap: "Brazo actuador de un disco duro: mecatrónica en miniatura" },
], "Fotos: F. Q. Brown/Los Angeles Times CC BY 4.0 · A. Meskens CC BY-SA 3.0 · Mk2010 CC BY 4.0 · Wikimedia Commons",
"Apoyo visual del hilo histórico de S1-S3: el telar reprogramable (1801), el Unimate en su papel más famoso (1966-67) y el HDD como ejemplo canónico de De Silva. Dejarla proyectada durante la narración histórica y volver a ella al cerrar S3.");

{
 const s = contentSlide(p1, "De los autómatas a la fábrica", "S3 · Historia");
 const tl = [
 ["1739", "Pato de Vaucanson: un solo programa fijo (levas)"],
 ["1801", "Telar de Jacquard: reprogramable con tarjetas perforadas"],
 ["1920", "R.U.R. de Karel Čapek: nace la palabra «robot» (roboti, servidumbre)"],
 ["1954–61", "Patente de Devol; Unimation Inc. (Devol + Engelberger)"],
 ["1961", "Primer Unimate en producción: GM, Nueva Jersey"],
 ["1968", "Licencia a Kawasaki: primer robot industrial japonés"],
 ];
 tl.forEach((t, i) => {
 const col = i % 3, row = Math.floor(i / 3);
 card(s, 0.7 + col * 4.05, 1.75 + row * 2.25, 3.8, 2.05, { title: t[0], body: t[1], titleColor: GREEN_DK, bodySize: 13, titleSize: 20 });
 });
 card(s, 0.7, 6.4, 11.9, 0.7, { title: "", body: "Asimov (1950–85) explora la moralidad con las Tres Leyes: nuestras expectativas sobre robots vienen de la ficción tanto como de la ingeniería.", fill: "E3F7EC", bodySize: 12.5 });
 s.addNotes("Anécdota: Engelberger llevó un Unimate a The Tonight Show en 1966 (sirvió cerveza, metió un putt, dirigió la banda). Devol y Engelberger se conocieron en un cóctel en 1954. El telar de Jacquard influyó en Babbage y Ada Lovelace: robótica y computación comparten raíz.");
 footer(s, "Corke, RVC3, cap. 1, secciones 1.1 y excursus");
}

{
 const s = contentSlide(p1, "¿Qué es un robot?", "S3 · Definición");
 const tri = [
 ["PERCIBIR", "Sensores: estado propio y del mundo", "Bloques 3 y 6"],
 ["PLANIFICAR", "De la información + objetivo a la acción", "Bloque 7"],
 ["ACTUAR", "Ejecutar movimiento con precisión", "Bloques 3, 4 y 5"],
 ];
 tri.forEach((t, i) => {
 const x = 0.7 + i * 4.05;
 card(s, x, 1.8, 3.8, 2.3, { title: t[0], body: t[1] + "\n\n" + t[2], num: String(i + 1), bodySize: 12.5, titleSize: 16 });
 if (i < 2) s.addText("→", { x: x + 3.8, y: 2.6, w: 0.3, h: 0.6, fontSize: 22, bold: true, color: GREEN_DK, align: "center", margin: 0 });
 });
 card(s, 0.7, 4.4, 5.9, 2.3, {
 title: "Sensores propioceptivos",
 body: "Miden el estado del propio robot: ángulos articulares, revoluciones de rueda, corriente de motor. Base de la odometría.",
 bodySize: 13,
 });
 card(s, 6.85, 4.4, 5.75, 2.3, {
 title: "Sensores exteroceptivos",
 body: "Miden el mundo respecto al robot: choque, GPS, brújula, tiempo de vuelo (acústico, óptico, radio). Corrigen la deriva propioceptiva.",
 bodySize: 13,
 });
 s.addNotes("«Una máquina orientada a objetivos que puede percibir, planificar y actuar» (Corke), de las pocas definiciones literales de examen. Cita de Engelberger: «no puedo definir un robot, pero lo reconozco cuando lo veo». La tríada organiza el curso: decirlo explícitamente.");
 footer(s, "Corke, RVC3, cap. 1, sección 1.3");
}

{
 const s = contentSlide(p1, "Telerobots y el espectro de autonomía", "S3 · Autonomía");
 bullets(s, [
 { t: "Telerobots: del «teleautomaton» de Tesla (1898) a los brazos maestro-esclavo de Goertz (Argonne, Proyecto Manhattan) con realimentación de fuerza.", },
 { t: "Sus herederos: los ROV del Titanic y la cirugía robótica actual, teleoperada, no autónoma." },
 { t: "Control alternado (traded): humano y computador se pasan el control (piloto automático)." },
 { t: "Control compartido (shared): ambos a la vez (mantener carril + conductor gestiona velocidad)." },
 { t: "Rovers marcianos: autonomía local con objetivos de alto nivel desde la Tierra (latencia de minutos)." },
 ], { w: 6.9 });
 card(s, 7.9, 1.7, 4.7, 4.9, {
 title: "Discusión (10 min)",
 body: "¿Dónde está cada uno en el espectro?\n\n• Un dron de carreras FPV\n• Un taxi autónomo comercial\n• El brazo del laboratorio ejecutando un programa\n\nLa última incomoda: un robot industrial clásico ni percibe ni planifica, ¿es un robot o automatización programable?",
 fill: "E3F7EC", bodySize: 13,
 });
 s.addNotes("La definición sense-plan-act es una vara de medir, no una frontera nítida. Pedir ejemplos de robots «modernos» de prensa para S4.");
 footer(s, "Corke, RVC3, cap. 1, excursus 1.5–1.6");
}

// S4
sectionSlide(p1, "S4", "Panorama 2026 y seminario", "Physical AI · humanoides · ética · lanzamiento del seminario de artículos", "0-5 recuperación; 5-25 panorama con vídeos cortos; 25-35 ética en formato debate; 35-45 lanzamiento del seminario; 45-60 cuestionario B1 en Moodle (15 min).");


slideFotos(p1, "El panorama 2026, en imágenes", "S4 · Panorama", [
 { f: "fotos/b1_rover2.jpg", x: 0.7, y: 1.5, w: 5.85, h: 2.5, cap: "Ingenuity, fotografiado por Perseverance: autonomía a 300 millones de km" },
 { f: "fotos/b2_auto.jpg", x: 6.75, y: 1.5, w: 5.85, h: 2.5, cap: "Robotaxi en flota comercial: el robot de servicio ya está en la calle" },
 { f: "fotos/b2_dron.jpg", x: 0.7, y: 4.32, w: 5.85, h: 2.5, cap: "Multirrotor: percepción y control embarcados de serie" },
 { f: "fotos/b7_atlas.jpg", x: 6.75, y: 4.32, w: 5.85, h: 2.5, cap: "Atlas (2013): del DARPA Robotics Challenge a los humanoides industriales" },
], "Fotos: NASA/JPL-Caltech CC BY 2.0 · Dllu CC BY-SA 4.0 · J. Sorenson CC0 · DARPA dominio público · Wikimedia Commons",
"Cuatro imágenes para la conversación del panorama: pedir a la clase que sitúe cada una en la tríada percibir-planificar-actuar y en el espectro de autonomía de S3 antes de pasar a los VLA.");

{
 const s = contentSlide(p1, "El momento «Physical AI»: por qué 2026 no es 2016", "S4 · Panorama");
 bullets(s, [
 { t: "Desde 2023: modelos fundacionales aplicados al control de robots físicos.", h: true },
 { t: "Modelos visión-lenguaje-acción (VLA): de cámara + instrucción en lenguaje natural a acciones motoras." },
 { t: "π0 (Physical Intelligence) · GR00T (NVIDIA, humanoides) · Gemini Robotics (Google DeepMind)." },
 { t: "Humanoides: de curiosidad a pilotos industriales en logística y fabricación." },
 { t: "Cobots y AMR siguen siendo el mayor segmento de crecimiento en fábrica." },
 ], { w: 6.9 });
 card(s, 7.9, 1.7, 4.7, 4.9, {
 title: "Mensaje doble para el curso",
 body: "1. Los fundamentos no caducan: los VLA generan consignas que ejecutan los lazos de control del bloque 5, sobre la cinemática del bloque 4.\n\n2. El perfil que demanda el mercado: fundamentos + Python + ROS 2 + criterio para saber cuándo la IA aporta valor.\n\nEl bloque 8 vuelve aquí con detalle técnico.",
 bodySize: 13,
 });
 s.addNotes("Apoyarse en 2-3 vídeos cortos (humanoides en almacén; demo VLA). No profundizar técnicamente: eso es B8. El objetivo es motivación y contexto profesional.");
 footer(s, "Ver bloque 8 · Physical AI, VLA, humanoides");
}

{
 const s = contentSlide(p1, "Ética: preguntas sin respuesta fácil", "S4 · Debate");
 const qs = [
 ["Empleo", "La IA ya hace tareas de información; ¿invadirán los robots las físicas? Contrapunto: trabajos peligrosos o sin mano de obra, e industrias (automóvil) viables gracias a la automatización."],
 ["Coches autónomos", "Los conductores humanos matan a >1 millón de personas/año; aún así el coche autónomo genera más incomodidad. ¿A quién culpamos cuando el robot se equivoca?"],
 ["Cuidado de personas", "Robots en cirugía, mayores y educación: ¿eficiencia ganada o contacto humano perdido?"],
 ];
 qs.forEach((c, i) => card(s, 0.7 + i * 4.05, 1.8, 3.8, 3.4, { title: c[0], body: c[1], num: String(i + 1), bodySize: 12.5 }));
 card(s, 0.7, 5.5, 11.9, 1.2, {
 title: "La posición de Corke (y de esta asignatura)",
 body: "Estas cuestiones no deben decidirlas solo los roboticistas, pero tampoco pueden ignorarlas. Participar en el debate es parte de la profesión.",
 fill: "E3F7EC", bodySize: 13,
 });
 s.addNotes("Formato: proyectar dos afirmaciones, votación a mano alzada, pedir argumentos de ambos lados. 10 minutos máximo.");
 footer(s, "Corke, RVC3, cap. 1, sección 1.5");
}

{
 const s = contentSlide(p1, "Seminario de artículos científicos", "S4 · Evaluación continua");
 const cards = [
 ["Formato", "Parejas. Un artículo de los últimos 12–18 meses: VLA y robot learning, SLAM, humanoides, manipulación, percepción, HRI, seguridad."],
 ["Fuentes", "arXiv (cs.RO), ICRA, IROS, RSS, CoRL, Science Robotics, IEEE T-RO / RA-L. Validación del profesor antes del 30 de septiembre."],
 ["Entrega", "Presentación de 10 min + 5 de preguntas en S41–S42 (16–17 dic): problema, método, resultados, limitaciones, conexión con el curso."],
 ["Rúbrica", "Claridad 30% · comprensión técnica 40% · análisis crítico 20% · preguntas 10%. IA generativa permitida con declaración; defensa oral individual."],
 ];
 cards.forEach((c, i) => {
 const col = i % 2, row = Math.floor(i / 2);
 card(s, 0.7 + col * 6.1, 1.75 + row * 2.55, 5.85, 2.3, { title: c[0], body: c[1], num: String(i + 1), bodySize: 12.5 });
 });
 s.addNotes("Cerrar la sesión con el cuestionario de seguimiento del bloque 1 en Moodle: 15 minutos, 10 preguntas ABCD del banco del bloque. Cuenta para evaluación continua.");
 footer(s, "Presentaciones: S41–S42 · 16 y 17 de diciembre");
}

p1.writeFile({ fileName: "IQS_B1_Introduccion.pptx" }).then(() => console.log("OK deck B1"));

/* ==================== DECK B2 ==================== */
const p2 = newDeck();

titleSlide(p2, {
 curso: "82514 · MECATRÓNICA Y ROBÓTICA",
 bloque: "Bloque 2",
 titulo: "Tipología de robots, cobots\ny humanoides. Seguridad",
 sub: "Sesiones S5–S7 · 5 horas",
 fechas: "18, 23 y 25 de septiembre de 2026 · IQS Universitat Ramon Llull",
});

{
 const s = contentSlide(p2, "Hoja de ruta del bloque", "Bloque 2");
 const rows = [
 ["S5 · vie 18 sep · 2 h", "Taxonomía de robots, configuraciones de manipuladores, grados de autonomía"],
 ["S6 · mié 23 sep · 1 h", "Robots móviles: ruedas, patas, aire; AGV frente a AMR"],
 ["S7 · vie 25 sep · 2 h", "Cobots y seguridad: ISO 10218:2025, métodos colaborativos, análisis de riesgos"],
 ];
 rows.forEach((r, i) => card(s, 0.7, 1.8 + i * 1.5, 11.9, 1.25, { title: r[0], body: r[1], num: String(i + 1), bodySize: 13, titleSize: 14 }));
 card(s, 0.7, 6.35, 11.9, 0.75, { title: "", body: "Jueves 24 de septiembre: festivo (La Mercè). Los equipos del proyecto integrador quedan cerrados al final de S7.", fill: "E3F7EC", bodySize: 12.5 });
 footer(s, "82514 Mecatrónica y Robótica · B2 · IQS");
}

sectionSlide(p2, "S5", "Taxonomía y configuraciones", "Dos taxonomías · configuraciones de manipuladores · espectro de autonomía", "0-10 repaso cuestionario B1; 10-35 taxonomías (clasificar fotos); 35-65 configuraciones; 65-75 descanso; 75-95 autonomía; 95-115 actividad de fichas; 115-120 equipos del proyecto.", { f: "fotos/b2_davinci.jpg", cap: "Da Vinci Xi: el telerobot quirúrgico", credito: "Foto: Alvarogarciamd CC BY-SA 4.0 · Wikimedia Commons" });

slideFotos(p2, "La taxonomía, en imágenes", "S5 · Tipos de robots", [
 { f: "fotos/b2_humanoide.jpg", x: 0.7, y: 1.5, w: 5.85, h: 2.5, cap: "Humanoide (ASIMO): móvil y de servicio a la vez" },
 { f: "fotos/b2_cuadrupedo.jpg", x: 6.75, y: 1.5, w: 5.85, h: 2.5, cap: "Cuadrúpedo de inspección (Spot)" },
 { f: "fotos/b2_delta.jpg", x: 0.7, y: 4.35, w: 5.85, h: 2.5, cap: "Robot delta: cadenas cinemáticas cerradas" },
 { f: "fotos/b2_agv.jpg", x: 6.75, y: 4.35, w: 5.85, h: 2.5, cap: "AGV portacontenedores (puerto de Róterdam)" },
], "Fotos: Gnsin CC BY-SA 3.0 · ArticCynda CC BY-SA 4.0 · Trungdoanhong CC BY-SA 4.0 · CC0 · Wikimedia Commons",
"Usar en la dinámica de clasificación: proyectar cada imagen y pedir a la clase que la sitúe en ambas taxonomías antes de dar la respuesta.");

{
 const s = contentSlide(p2, "Dos taxonomías complementarias", "S5 · Clasificación");
 card(s, 0.7, 1.75, 5.9, 2.2, {
 title: "Por movilidad",
 body: "• Fijos («primera generación»: la célula va al robot)\n• Móviles: ruedas o patas (tierra), alas o rotores (aire), superficie o inmersión (agua)",
 bodySize: 13,
 });
 card(s, 0.7, 4.15, 5.9, 2.5, {
 title: "Por función (Corke)",
 body: "• Fabricación, herederos del Unimate\n• Servicio, limpieza, cuidado, rehabilitación, transporte\n• Campo, agricultura, minería, construcción, exteriores\n• Humanoides, a la vez móviles y de servicio: las categorías no son excluyentes",
 bodySize: 13,
 });
 card(s, 6.85, 1.75, 5.75, 4.9, {
 title: "Fabricación frente a colaborativo",
 body: "Robot de fabricación: brazo sobre base fija, tareas repetitivas en célula local, piezas presentadas de forma ordenada → máxima velocidad y precisión. Peligroso: seguridad por exclusión (jaula).\n\nCobot: seguro para el humano, baja velocidad, se detiene ante una obstrucción. Sustituye vallado por sensórica y control.\n\nCampo y servicio, dos retos extra: entorno desordenado y cambiante, y personas cerca (el reparto circula entre ellas; el coche las lleva dentro; el quirúrgico opera dentro).",
 bodySize: 13,
 });
 s.addNotes("Dinámica: proyectar fotos de robots reales y que la clase los clasifique en ambas taxonomías antes de dar la respuesta. La «escalera de intimidad física» explica por qué percepción y seguridad dominan la robótica moderna.");
 footer(s, "Corke, RVC3, cap. 1, sección 1.2");
}

{
 const s = contentSlide(p2, "Configuraciones de manipuladores", "S5 · Manipuladores");
 const cfg = [
 ["Cartesiano (PPP)", "Espacio en caja; rígido; pórticos de paletizado y metrología"],
 ["SCARA (RRP)", "Rígido en Z, ágil en el plano; ensamblado electrónico de alta velocidad"],
 ["Esférico (RRP)", "El Unimate original y el Stanford Arm; espacio esférico"],
 ["Articulado (6R)", "El estándar: Mitsubishi y ABB del laboratorio; máxima destreza"],
 ["Paralelo / delta", "Cadenas cerradas; poca inercia, altísima velocidad; envasado"],
 ["Cilíndrico (RPP)", "Espacio cilíndrico; hoy minoritario"],
 ];
 cfg.forEach((c, i) => {
 const col = i % 3, row = Math.floor(i / 3);
 card(s, 0.7 + col * 4.05, 1.75 + row * 2.2, 3.8, 1.95, { title: c[0], body: c[1], bodySize: 12, titleSize: 14 });
 });
 card(s, 0.7, 6.2, 11.9, 0.95, {
 title: "",
 body: "Conceptos que reaparecen en B4: grados de libertad (6 para pose arbitraria) · espacio alcanzable frente a diestro · repetibilidad (±0,01–0,05 mm, la cifra estrella de catálogo) frente a exactitud (peor; clave en programación fuera de línea).",
 fill: "E3F7EC", bodySize: 12,
 });
 s.addNotes("Dibujar cada configuración con su espacio de trabajo en pizarra. Los robots del laboratorio son articulados de 6 ejes: todo el bloque 4 se apoya en esa configuración.");
 footer(s, "R = articulación rotativa · P = prismática");
}

{
 const s = contentSlide(p2, "El espectro de autonomía", "S5 · Autonomía");
 const sp = [
 ["Teleoperación", "El humano controla todo; el robot ejecuta. ROV, cirugía robótica"],
 ["Control alternado", "Se pasan el control por turnos. Piloto automático"],
 ["Control compartido", "Ambos a la vez. Mantener carril + velocidad humana"],
 ["Autonomía supervisada", "El robot decide localmente; el humano fija objetivos. Rovers, AMR"],
 ];
 sp.forEach((c, i) => {
 card(s, 0.7 + i * 3.075, 1.9, 2.85, 2.6, { title: c[0], body: c[1], num: String(i + 1), bodySize: 12, titleSize: 13.5 });
 if (i < 3) s.addText("→", { x: 3.48 + i * 3.075, y: 2.9, w: 0.3, h: 0.5, fontSize: 18, bold: true, color: GREEN_DK, align: "center", margin: 0 });
 });
 card(s, 0.7, 4.9, 11.9, 1.8, {
 title: "Actividad en equipos (20 min)",
 body: "6 fichas por equipo: robot industrial, cobot, AMR, humanoide, quirúrgico, dron. Para cada una: taxonomía (movilidad y función), configuración cinemática si aplica, y posición en el espectro de autonomía. Puesta en común con votación.",
 fill: "E3F7EC", bodySize: 13,
 });
 s.addNotes("Al cierre: formación de equipos del proyecto integrador (definitivos en S7).");
 footer(s, "Corke, RVC3, cap. 1");
}

sectionSlide(p2, "S6", "Robots móviles", "Locomoción con ruedas y patas · AGV frente a AMR · aire y agua", "0-5 recuperación (dibujar SCARA y articulado); 5-25 ruedas; 25-40 AGV/AMR, patas y aire; 40-55 ejercicio de selección de plataforma; 55-60 cierre.", { f: "fotos/b2_dron.jpg", cap: "Multirrotor: locomoción aérea", credito: "Foto: J. Sorenson CC0 · Wikimedia Commons" });

{
 const s = contentSlide(p2, "Locomoción con ruedas", "S6 · Arquitecturas");
 const loc = [
 ["Diferencial", "Dos motrices independientes + apoyos. Gira sobre sí mismo. La arquitectura de la mayoría de AMR; modelo cinemático más simple (B4)"],
 ["Ackermann", "Dirección delantera tipo coche. Radio de giro mínimo; no holonómico (sin desplazamiento lateral) → condiciona la planificación (B7)"],
 ["Omnidireccional", "Ruedas mecanum o esféricas: holonómico (traslación y rotación simultáneas). Sensible al suelo; menos carga"],
 ["Orugas", "Terreno suelto; giro por deslizamiento (skid-steer) que castiga la odometría"],
 ];
 loc.forEach((c, i) => {
 const col = i % 2, row = Math.floor(i / 2);
 card(s, 0.7 + col * 6.1, 1.75 + row * 2.55, 5.85, 2.3, { title: c[0], body: c[1], num: String(i + 1), bodySize: 12.5 });
 });
 s.addNotes("La rueda es lo más eficiente sobre superficie preparada; la arquitectura determina la maniobrabilidad. «Holonómico» se define formalmente en B4; aquí, intuición: ¿puede moverse lateralmente sin maniobrar?");
 footer(s, "Corke, RVC3, parte II (contexto)");
}


slideFotos(p2, "Robots de servicio, entre personas", "S6 · Servicio", [
 { f: "fotos/b7_roomba2.jpg", x: 0.7, y: 1.5, w: 3.85, h: 4.9, cap: "Roomba: el robot doméstico más vendido de la historia" },
 { f: "fotos/b2_auto.jpg", x: 4.72, y: 1.5, w: 3.85, h: 4.9, cap: "Robotaxi: servicio autónomo en vía pública" },
 { f: "fotos/b8_ajedrez3.jpg", x: 8.74, y: 1.5, w: 3.9, h: 4.9, cap: "Compartir mesa con un brazo industrial: interacción humano-robot" },
], "Fotos: CEphoto, U. Aranas CC BY-SA 4.0 · Dllu CC BY-SA 4.0 · S. Kazantsev CC BY-SA 4.0 · Wikimedia Commons",
"Tres robots de servicio con tres niveles de convivencia con personas: casa, calle y mesa compartida. Con la última, anticipar la pregunta de seguridad que abre S7: ¿qué hace falta para que esto sea seguro?");

{
 const s = contentSlide(p2, "AGV frente a AMR, y el resto del mapa", "S6 · Plataformas");
 card(s, 0.7, 1.75, 5.9, 2.9, {
 title: "AGV",
 body: "Sigue infraestructura física: filoguiado, banda magnética, balizas. Ruta fija; se detiene ante obstáculos.\n\nEl entorno se adapta al vehículo.",
 bodySize: 13,
 });
 card(s, 6.85, 1.75, 5.75, 2.9, {
 title: "AMR",
 body: "Navega con un mapa que construye y mantiene (SLAM → B6); planifica rutas y rodea obstáculos (Nav2 → B7).\n\nEl vehículo se adapta al entorno. Mismo hardware, distinto software: 30 años de progreso en percepción.",
 bodySize: 13,
 });
 card(s, 0.7, 4.85, 11.9, 1.85, {
 title: "Patas, aire y agua",
 body: "Patas: escaleras y escombros a cambio de equilibrio dinámico y consumo; cuadrúpedos de inspección y humanoides bípedos (viables gracias también al RL → B8). Aire: multirrotores (estacionario, simplicidad) frente a ala fija (cobertura). Agua: ROV teleoperados y AUV autónomos. Todos comparten sense-plan-act con sensórica distinta.",
 fill: "E3F7EC", bodySize: 13,
 });
 s.addNotes("Ejercicio (15 min): elegir plataforma para almacén, hospital y viña, justificando locomoción, sensórica y autonomía. Recordar cierre de equipos del proyecto en S7.");
 footer(s, "Transición AGV→AMR = valor añadido por software");
}

sectionSlide(p2, "S7", "Cobots, seguridad y normativa", "ISO 10218:2025 · cuatro métodos colaborativos · análisis de riesgos", "0-10 recuperación; 10-40 marco normativo; 40-70 métodos colaborativos con vídeos; 70-80 descanso; 80-105 taller de análisis de riesgos; 105-120 cuestionario B2 en Moodle (15 min) y cierre de equipos.", { f: "fotos/b2_cobot3.png", cap: "UR16e: fuerza limitada y par medido en cada eje", credito: "Foto: Auledas CC BY-SA 4.0 · Wikimedia Commons" });

{
 const s = contentSlide(p2, "El marco normativo: ISO 10218:2025", "S7 · Normativa");
 card(s, 0.7, 1.75, 5.9, 2.6, {
 title: "Parte 1, El fabricante",
 body: "Requisitos del robot como componente: paradas de seguridad, límites de eje, modos de operación.",
 bodySize: 13,
 });
 card(s, 6.85, 1.75, 5.75, 2.6, {
 title: "Parte 2, El integrador",
 body: "Requisitos del sistema completo: layout de la célula, resguardos, dispositivos de protección, validación. El integrador es responsable legal de la evaluación de riesgos.",
 bodySize: 13,
 });
 card(s, 0.7, 4.55, 11.9, 2.1, {
 title: "Dos ideas clave",
 body: "1. Comprar un robot «seguro» no hace segura la célula: la seguridad es una propiedad de la aplicación integrada.\n2. «Cobot» no es una categoría legal, sino una aplicación colaborativa: la revisión de 2025 integró en la ISO 10218 los requisitos que vivían en la ISO/TS 15066 (2016), que sigue siendo la referencia de los límites biomecánicos de fuerza y presión por región corporal.",
 fill: "E3F7EC", bodySize: 13,
 });
 s.addNotes("No memorizar cláusulas: entender la arquitectura de la norma y la división de responsabilidades. Ejemplo provocador: un cobot con una cuchilla no es una aplicación colaborativa segura; un robot clásico puede participar en una célula colaborativa bien diseñada.");
 footer(s, "ISO 10218-1/-2:2025 · ISO/TS 15066:2016");
}

{
 const s = contentSlide(p2, "Los cuatro métodos de operación colaborativa", "S7 · Métodos");
 const met = [
 ["Parada monitorizada de seguridad", "El robot se detiene (parada segura) cuando entra una persona y reanuda al salir. Colaboración por turnos."],
 ["Guiado manual", "El operador mueve el robot físicamente, con compensación de gravedad. Programación por demostración."],
 ["Velocidad y separación", "Monitorización en tiempo real de la distancia persona-robot; la velocidad se modula hasta detenerse. Escáneres láser / visión de seguridad certificada: células sin vallado con robots rápidos."],
 ["Limitación de potencia y fuerza", "Se admite contacto, con fuerza, par y presión bajo los umbrales biomecánicos (ISO/TS 15066). El método de los cobots con medición de par articular."],
 ];
 met.forEach((c, i) => {
 const col = i % 2, row = Math.floor(i / 2);
 card(s, 0.7 + col * 6.1, 1.7 + row * 2.3, 5.85, 2.1, { title: c[0], body: c[1], num: String(i + 1), bodySize: 12, titleSize: 13.5 });
 });
 card(s, 0.7, 6.4, 11.9, 0.7, {
 title: "",
 body: "Los métodos se combinan (separación en aproximación + fuerza limitada en la entrega) y tienen coste de productividad: elegir método es diseño mecatrónico, el MDQ del bloque 1 reaparece.",
 fill: "E3F7EC", bodySize: 12,
 });
 s.addNotes("Vídeos cortos de cada método; los estudiantes identifican cuál es cuál antes de nombrarlos.");
 footer(s, "ISO 10218:2025 · ISO/TS 15066");
}

{
 const s = contentSlide(p2, "Taller: análisis de riesgos en 5 pasos", "S7 · Taller");
 const steps = [
 ["Límites", "Espacio, tareas, quién interactúa y cómo"],
 ["Peligros", "Por tarea, incluidos modos degradados: limpieza, mantenimiento, recuperación de fallos"],
 ["Estimación", "Severidad × exposición × probabilidad de evitación"],
 ["Reducción", "Jerarquía: eliminar por diseño → proteger → informar (en ese orden)"],
 ["Validación", "Comprobar que las medidas funcionan y documentarlo"],
 ];
 steps.forEach((c, i) => {
 card(s, 0.7 + i * 2.5, 1.85, 2.25, 2.6, { title: c[0], body: c[1], num: String(i + 1), bodySize: 11.5, titleSize: 13 });
 if (i < 4) s.addText("→", { x: 2.88 + i * 2.5, y: 2.8, w: 0.3, h: 0.5, fontSize: 16, bold: true, color: GREEN_DK, align: "center", margin: 0 });
 });
 card(s, 0.7, 4.8, 11.9, 1.9, {
 title: "Encargo (30 min, en equipos)",
 body: "Célula propuesta: robot ABB del laboratorio con carga y descarga manual de piezas. Entregable: tabla de riesgos de 6 filas (peligro, tarea, estimación, medida, método colaborativo si aplica). Corrección en común como síntesis del bloque. Después: cuestionario B2 en Moodle (15 min) y cierre de equipos del proyecto.",
 fill: "E3F7EC", bodySize: 13,
 });
 s.addNotes("Alineado con ISO 12100. Recordar: los accidentes reales se concentran en los modos degradados, no en la operación normal. Las normas del laboratorio ya establecidas son de obligado cumplimiento (no se modifican aquí).");
 footer(s, "ISO 12100 · ISO 10218-2:2025");
}

p2.writeFile({ fileName: "IQS_B2_Tipologia_Seguridad.pptx" }).then(() => console.log("OK deck B2"));
