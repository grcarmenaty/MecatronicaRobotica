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

// Fila de agenda: banda con círculo numerado y texto en dos estilos
function agendaRow(s, y, h, num, label, desc, labelSize = 13.5, descSize = 12.5) {
 s.addShape("roundRect", { x: 0.7, y, w: 11.9, h, rectRadius: 0.08, fill: { color: BG_LT }, line: { type: "none" } });
 s.addShape("ellipse", { x: 0.92, y: y + h / 2 - 0.25, w: 0.5, h: 0.5, fill: { color: GREEN }, line: { type: "none" } });
 s.addText(num, { x: 0.92, y: y + h / 2 - 0.25, w: 0.5, h: 0.5, align: "center", valign: "middle", fontFace: "Calibri", fontSize: 15, bold: true, color: NAVY, margin: 0 });
 s.addText([
 { text: label + " ", options: { bold: true, color: NAVY, fontSize: labelSize } },
 { text: ", " + desc, options: { color: INK, fontSize: descSize } },
 ], { x: 1.62, y, w: 10.75, h, valign: "middle", fontFace: "Calibri", margin: 0 });
}

// Flecha horizontal entre tarjetas
function arrowR(s, x, y, size = 18) {
 s.addText("→", { x, y, w: 0.32, h: 0.5, fontSize: size, bold: true, color: GREEN_DK, align: "center", margin: 0 });
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

/* ==================== DECK B6, Percepción y SLAM ==================== */
const p6 = newDeck();

titleSlide(p6, {
 curso: "82514 · MECATRÓNICA Y ROBÓTICA",
 bloque: "Bloque 6",
 titulo: "Percepción robótica: visión,\nestimación de estado y SLAM",
 sub: "Sesiones S25–S31 · 10 horas",
 fechas: "6, 11, 12, 13, 18, 19 y 20 de noviembre de 2026 · IQS Universitat Ramon Llull",
});

{
 const s = contentSlide(p6, "Hoja de ruta del bloque", "Bloque 6");
 const rows = [
 ["S25 · vie 6 nov · 2 h", "EXAMEN PARCIAL 1 (bloques 1-4): test y problemas"],
 ["S26 · mié 11 nov · 1 h", "Formación de imagen y modelo de cámara · calibración en cuaderno guiado"],
 ["S27 · jue 12 nov · 1 h", "Procesado clásico y aprendido: el criterio del ingeniero"],
 ["S28 · vie 13 nov · 2 h", "Filtro de Bayes, filtro de Kalman y EKF"],
 ["S29 · mié 18 nov · 1 h", "Localización con EKF sobre mapa de balizas"],
 ["S30 · jue 19 nov · 1 h", "Filtro de partículas y localización de Montecarlo"],
 ["S31 · vie 20 nov · 2 h", "SLAM: EKF-SLAM, GraphSLAM, FastSLAM y SLAM visual"],
 ];
 rows.forEach((r, i) => agendaRow(s, 1.62 + i * 0.79, 0.68, String(i + 1), r[0], r[1], 12.5, 11.5));
 s.addNotes("El bloque recorre la mitad «percibir» de la tríada. El viernes 6 de noviembre (S25) es el examen parcial 1 de B1-B4, así que la docencia del bloque empieza el miércoles 11: el bloque se compacta a 8 horas, la calibración pasa a cuaderno guiado en casa y el procesado clásico y el aprendido comparten sesión. Cuestionario B6 en Moodle al cierre de S31.");
 footer(s, "82514 Mecatrónica y Robótica · B6 · IQS");
}

sectionSlide(p6, "S25", "Examen parcial 1", "Bloques 1-4 · test y tres problemas · 2 horas",
 "Reservar aula de examen. Llevar impresas las 6 versiones (A-F) y repartirlas en damero. 0-5 acomodo, identificación e instrucciones; 5-115 examen; 115-120 recogida y recuento. Corrección con la rúbrica publicada; soluciones en el campus en una semana.");

{
 const s = contentSlide(p6, "Parcial 1: estructura y reglas", "S25 · Examen");
 const partes = [
 ["A", "Test (2,0 pt)", "10 preguntas ABCD sobre B1-B4; cada error resta un tercio; en blanco no puntúa"],
 ["B", "Diseño mecatrónico e instrumentación (2,0 pt)", "Nyquist y aliasing con cálculo · MDQ: cálculo e interpretación"],
 ["C", "Cinemática directa (3,0 pt)", "FK del 2R con números · tabla DH · espacio de trabajo alcanzable"],
 ["D", "IK, jacobiano y estática (3,0 pt)", "Las dos ramas de la IK · det J y singularidades · pares con τ = Jᵀ·F"],
 ];
 partes.forEach((c, i) => card(s, 0.7, 1.7 + i * 1.16, 11.9, 1.0, { title: c[1], body: c[2], num: c[0], bodySize: 12, titleSize: 13.5 }));
 card(s, 0.7, 6.42, 11.9, 0.62, { title: "", body: "Material: calculadora no programable y una hoja A4 de formulario manuscrito por las dos caras. Seis versiones (A-F) en damero. Los errores de arrastre no se penalizan dos veces.", fill: "E3F7EC", bodySize: 11.5 });
 s.addNotes("Proyectar esta diapositiva la semana anterior (al cerrar B5) y dejarla publicada en el campus. El día del examen: recordar las reglas del test (el error resta un tercio, en blanco no puntúa), que el planteamiento vale el 40 por ciento de cada apartado y que un resultado sin desarrollo no puntúa. Las seis versiones comparten estructura y dificultad: decirlo para desactivar la percepción de agravio.");
 footer(s, "Parcial 1 · viernes 6 de noviembre · 2 h");
}

sectionSlide(p6, "S26", "Formación de imagen y calibración exprés", "Cámara estenopeica · proyección · intrínsecos y extrínsecos · calibración como cuaderno guiado",
 "0-5 devolución exprés del parcial y apertura del bloque; 5-20 cámara estenopeica y proyección perspectiva; 20-40 modelo matricial: intrínsecos, extrínsecos y distorsión; 40-50 calibración: método de Zhang, criterio del error de reproyección y encargo del cuaderno guiado (entrega antes de S28); 50-60 cierre: la cámara es un sensor de rayos, no de distancias.", { f: "fotos/b6_estereo3.jpg", cap: "Cámara estéreo: recuperar la profundidad perdida", credito: "Foto: T. Cognard CC BY-SA 3.0 · Wikimedia Commons" });

slideFotos(p6, "La cámara, de Mozi al modelo matricial", "S26 · Imagen", [
 { f: "figs/b6_pinhole.png", x: 0.7, y: 1.6, w: 6.6, h: 4.4, cap: "El modelo estenopeico: la profundidad se pierde en la proyección" },
 { f: "fotos/b6_camara_obscura.jpg", x: 7.5, y: 1.6, w: 5.1, h: 4.4, cap: "Dibujo técnico hecho con cámara oscura (Verbruggen, s. XVIII)" },
], "Figura propia del curso · Dibujo: dominio público / CC BY-SA 3.0 · Wikimedia Commons",
"El dibujo de Verbruggen conecta con la historia de la cámara oscura del guion (Mozi, s. V a. C.); la figura es la que se deriva en pizarra.");

{
 const s = contentSlide(p6, "De la escena 3D a la imagen 2D", "S26 · Proyección");
 bullets(s, [
 { t: "La cámara estenopeica: el modelo mínimo", h: true },
 { t: "Un punto del mundo, el centro óptico y su proyección en el plano imagen están alineados: la geometría se reduce a triángulos semejantes." },
 { t: "Las coordenadas de imagen resultan de dividir por la profundidad, esa división es la fuente de todo lo demás:" },
 { t: "Consecuencia central: la proyección pierde la profundidad. Un punto de la imagen corresponde a un rayo completo del espacio, no a un punto." },
 { t: "Recuperar 3D exige información añadida: estéreo, movimiento, un sensor de profundidad o un modelo del objeto." },
 ], { w: 6.7, h: 4.1 });
 eqImg(s, "pinhole", 1.7, 5.8, 3.1, 0.72);
 card(s, 7.7, 1.7, 4.9, 4.9, {
 title: "Ambigüedad de la perspectiva",
 body: "Objetos de tamaño y distancia distintos producen la misma imagen: la escala es indeterminable a partir de una vista.\n\nEs el mismo problema que la visión biológica resuelve con dos ojos y que la robótica resuelve con estéreo, estructura desde el movimiento o LiDAR.\n\nEn el bloque 7 esa profundidad reaparece convertida en mapa de ocupación.",
 bodySize: 12.5,
 });
 s.addNotes("Derivar los triángulos semejantes en pizarra antes de escribir las fórmulas. La pregunta que abre la sesión: «¿por qué una foto no basta para que un robot agarre un objeto?». La respuesta, la profundidad se pierde en la división por Z, justifica los tres bloques siguientes.");
 footer(s, "Corke, 2023, cap. 13 · Formación de imagen");
}

{
 const s = contentSlide(p6, "Modelo matricial y calibración", "S26 · Parámetros");
 card(s, 0.7, 1.72, 5.9, 2.35, {
 title: "Parámetros intrínsecos (K)",
 body: "Distancias focales en píxeles, punto principal y factor de sesgo. Describen la cámara: no cambian al moverla.",
 bodySize: 12.5,
 });
 card(s, 6.85, 1.72, 5.75, 2.35, {
 title: "Parámetros extrínsecos (R, t)",
 body: "Rotación y traslación del marco de la cámara respecto al mundo. Describen dónde está: cambian en cada instante y los estima la localización.",
 bodySize: 12.5,
 });
 card(s, 0.7, 4.27, 5.9, 2.35, {
 title: "Distorsión de lente",
 body: "El modelo estenopeico ideal no captura la lente real: coeficientes radiales y tangenciales corrigen la curvatura de las rectas hacia los bordes.",
 bodySize: 12.5,
 });
 card(s, 6.85, 4.27, 5.75, 2.35, {
 title: "Calibración: cuaderno guiado en casa",
 body: "Tablero de ajedrez, 15-20 vistas variadas, findChessboardCorners y calibrateCamera en OpenCV.\n\nEntrega en el campus antes de S28; criterio de calidad: error de reproyección por debajo de un píxel. Los resultados se comentan al abrir S28.",
 bodySize: 12.5,
 });
 s.addNotes("La matriz de proyección completa combina K, R y t. Insistir en la separación conceptual: los intrínsecos se calibran una vez; los extrínsecos son el estado que estimarán los filtros de S28-S31. La calibración se hace en el cuaderno guiado en casa (entrega antes de S28); los ficheros se reutilizan en el proyecto.");
 footer(s, "Corke, 2023, cap. 13 · Calibración con OpenCV");
}

sectionSlide(p6, "S27", "Procesado clásico y aprendido", "Convolución y bordes · regiones y puntos · rasgos aprendidos · el criterio del ingeniero",
 "0-5 recuperación de S26 y demo del umbral que se rompe al cambiar la luz; 5-25 caja clásica en galería: convolución, Canny, blobs y puntos de interés; 25-40 de rasgos diseñados a aprendidos: YOLO, segmentación y SAM; 40-52 discusión con la tabla de criterio sobre tres casos; 52-60 síntesis y anuncio del giro probabilístico de S28.");

{
 const s = contentSlide(p6, "Cuatro herramientas clásicas que siguen vigentes", "S27 · Procesado");
 const items = [
 ["Convolución", "Una ventana recorre la imagen combinando vecindarios: suavizado gaussiano, realce, derivadas. Es la operación base, y la misma que ejecuta cada capa convolucional de la sesión siguiente."],
 ["Bordes", "El gradiente marca discontinuidades de intensidad. Canny añade supresión no máxima e histéresis. Aviso: «los bordes de la imagen no son necesariamente los mismos que los bordes de los objetos» (Corke, 2023, p. 454)."],
 ["Regiones", "Umbralizado y etiquetado de componentes conexas producen blobs con área, centroide y momentos: base de la inspección industrial por visión."],
 ["Puntos", "Esquinas y descriptores invariantes permiten emparejar la misma escena entre vistas: es la materia prima del SLAM visual de S31."],
 ];
 items.forEach((c, i) => {
 const col = i % 2, row = Math.floor(i / 2);
 card(s, 0.7 + col * 6.1, 1.72 + row * 2.5, 5.85, 2.25, { title: c[0], body: c[1], num: String(i + 1), bodySize: 11.5, titleSize: 14 });
 });
 s.addNotes("Demostración en vivo: cargar una imagen del laboratorio y aplicar las cuatro operaciones en secuencia, comentando qué se conserva y qué se pierde en cada paso. El mensaje: estas técnicas no están obsoletas; son rápidas, deterministas y explicables, y por eso sobreviven en inspección industrial.");
 footer(s, "Corke, 2023, caps. 11-12 · pp. 454, 505, 517");
}


{
 const s = contentSlide(p6, "De rasgos diseñados a rasgos aprendidos", "S27 · Aprendizaje profundo");
 bullets(s, [
 { t: "El cambio de paradigma", h: true },
 { t: "Durante décadas el ingeniero diseñaba el descriptor; hoy la red lo aprende de los datos. Corke lo dice sin rodeos: estas técnicas «han sido eclipsadas por las basadas en aprendizaje profundo» (Corke, 2023, p. 510)." },
 { t: "Detección: una sola pasada de red produce cajas, clases y confianzas, la familia YOLO como estándar práctico en tiempo real." },
 { t: "Segmentación semántica: una etiqueta por píxel. De instancias: además separa objetos individuales del mismo tipo." },
 { t: "Modelos fundacionales de segmentación (SAM y sucesores): segmentan objetos no vistos en entrenamiento a partir de una indicación." },
 ], { w: 7.0 });
 card(s, 8.0, 1.7, 4.6, 4.9, {
 title: "Coste oculto",
 body: "Los datos, no el modelo, son el cuello de botella: etiquetar es caro y el dominio de entrenamiento condiciona el resultado.\n\nUna red entrenada con imágenes de día falla de noche; una entrenada en simulación falla en la planta.\n\nEs el mismo problema sim-to-real que veremos en el bloque 8.",
 bodySize: 12.5,
 });
 s.addNotes("No entrar en arquitecturas ni entrenamiento: el objetivo es criterio de ingeniero. Mostrar una inferencia en vivo si hay GPU disponible, o un vídeo si no. La transición al bloque 8 queda abierta con el problema de dominio.");
 footer(s, "Corke, 2023, cap. 12 · p. 510");
}

{
 const s = contentSlide(p6, "Cuándo clásico y cuándo aprendido", "S27 · Criterio");
 card(s, 0.7, 1.75, 5.9, 4.55, {
 title: "Elegir clásico",
 body: "• Escena controlada: iluminación fija, fondo conocido, pieza siempre igual\n• Se exige determinismo y explicabilidad (auditoría, certificación)\n• Latencia mínima en hardware modesto, sin GPU\n• No hay datos etiquetados ni presupuesto para generarlos\n• Medición metrológica: dimensiones, posición subpíxel",
 bodySize: 12.5,
 });
 card(s, 6.85, 1.75, 5.75, 4.55, {
 title: "Elegir aprendido",
 body: "• Variabilidad alta: objetos deformables, iluminación cambiante, desorden\n• La tarea es de reconocimiento semántico, no de medida\n• Existen datos, o un modelo preentrenado que se ajusta con pocos ejemplos\n• Se acepta un comportamiento estadístico con tasa de error medida\n• Hay cómputo suficiente en el robot o en el borde",
 bodySize: 12.5,
 });
 s.addNotes("Cerrar con un caso de laboratorio: verificar la presencia de un tornillo en una pieza fija es clásico; localizar piezas revueltas en un contenedor es aprendido. Pedir a los equipos que anticipen cuál necesitará su proyecto.");
 footer(s, "Síntesis del profesor a partir de Corke, 2023, caps. 11-12");
}

sectionSlide(p6, "S28", "Bayes, Kalman y EKF", "Creencia · predicción y corrección · linealización",
 "0-10 recuperación y apertura del bloque probabilístico; 10-40 estado, creencia y filtro de Bayes con su algoritmo; 40-65 filtro de Kalman: hipótesis y las dos fases; 65-75 descanso; 75-100 EKF y linealización; 100-120 taller: filtro de Kalman 1D en Python sobre datos ruidosos.");

slideFotos(p6, "Estimar: la curva y la nube", "S28–S30 · Figura y animación", [
 { f: "figs/b6_kalman.png", x: 0.7, y: 1.55, w: 5.9, h: 4.6, cap: "Filtro de Kalman 1D: estimación ±2σ frente a la medida cruda (S28)" },
 { f: "gifs/b6_particulas.gif", x: 6.85, y: 1.9, w: 5.7, h: 3.8, cap: "MCL: la nube de partículas converge (cuaderno S30)" },
], "Figura y animación propias del curso (cuadernos S28 y S30)",
"La animación reproduce la secuencia del pasillo con puertas: uniforme, multimodal tras la primera puerta, colapso con el movimiento. Es la imagen que deben recordar del bloque.");

{
 const s = contentSlide(p6, "El filtro de Bayes: creencia recursiva", "S28 · Estimación");
 card(s, 0.7, 1.7, 6.1, 2.15, {
 title: "La creencia",
 body: "El robot no conoce su estado: mantiene una distribución de probabilidad sobre él (la creencia), condicionada a todas las medidas y controles pasados (Thrun et al., 2005, pp. 26-28).",
 bodySize: 12.5,
 });
 card(s, 7.05, 1.7, 5.55, 2.15, {
 title: "Las dos hipótesis de Markov",
 body: "El estado siguiente depende solo del actual y del control; la medida depende solo del estado actual. Sin ellas no hay recursión (Thrun et al., 2005, pp. 28-33).",
 bodySize: 12.5,
 });
 const steps = [
 ["Predicción", "Propagar la creencia con el modelo de movimiento y el control: la incertidumbre crece"],
 ["Corrección", "Ponderar por la verosimilitud de la medida observada: la incertidumbre se reduce"],
 ["Normalización", "Escalar para que la creencia vuelva a ser una distribución de probabilidad"],
 ];
 steps.forEach((c, i) => {
 card(s, 0.7 + i * 4.05, 4.15, 3.8, 2.15, { title: c[0], body: c[1], num: String(i + 1), bodySize: 12, titleSize: 14 });
 if (i < 2) arrowR(s, 4.62 + i * 4.05, 5.0, 20);
 });
 s.addNotes("Escribir el algoritmo del filtro de Bayes en pizarra línea a línea (Thrun et al., 2005, p. 27): es el esqueleto del que Kalman, EKF y el filtro de partículas son casos particulares. Insistir en el ritmo predicción-corrección: es el latido de todo el bloque.");
 footer(s, "Thrun et al., 2005, pp. 26-33 · Algoritmo del filtro de Bayes, p. 27");
}

{
 const s = contentSlide(p6, "Kalman y su extensión no lineal", "S28 · KF y EKF");
 bullets(s, [
 { t: "Filtro de Kalman: el caso gaussiano lineal", h: true },
 { t: "Si el sistema es lineal, el ruido gaussiano y la creencia inicial gaussiana, la creencia se mantiene gaussiana para siempre: basta propagar media y covarianza (Thrun et al., 2005, pp. 40-42)." },
 { t: "La ganancia de Kalman arbitra entre predicción y medida: mucha confianza en el sensor la acerca a la medida; poca, a la predicción." },
 { t: "El problema: casi ningún robot es lineal. Un vehículo que gira no lo es." },
 { t: "EKF: linealizar en torno a la estimación actual mediante jacobianas, y aplicar las mismas ecuaciones (Thrun et al., 2005, pp. 54-56)." },
 ], { w: 7.0 });
 card(s, 8.0, 1.7, 4.6, 4.9, {
 title: "Precio de linealizar",
 body: "La linealización es una aproximación: si la no linealidad es fuerte o la incertidumbre grande, la gaussiana deja de describir la creencia real.\n\nEl EKF puede divergir y no avisa.\n\nDe ahí el filtro de partículas de S30: sin hipótesis gaussiana, a cambio de coste.",
 bodySize: 12.5,
 });
 s.addNotes("Taller de la segunda mitad: implementar un KF 1D sobre una señal ruidosa y observar el efecto de variar las covarianzas de proceso y medida. Que cada estudiante rompa el filtro subiendo la no linealidad: la divergencia se ve mejor de lo que se explica.");
 footer(s, "Thrun et al., 2005, pp. 40-42, 54-56");
}

sectionSlide(p6, "S29", "Localización con EKF", "Taxonomía del problema · modelo de movimiento · modelo de observación",
 "0-5 recuperación de S28; 5-20 el problema de localización y su taxonomía; 20-40 los dos modelos: movimiento y observación; 40-55 el ciclo completo sobre mapa de balizas y sus límites; 55-60 cierre y anuncio de S30.");

{
 const s = contentSlide(p6, "Localizar: taxonomía y los dos modelos", "S29 · Localización");
 const tax = [
 ["Seguimiento", "La pose inicial se conoce; solo hay que corregir la deriva. El EKF basta"],
 ["Global", "La pose inicial se desconoce: la creencia puede ser multimodal"],
 ["Secuestro", "El robot es desplazado sin avisar: el filtro debe recuperarse de una creencia errónea"],
 ];
 tax.forEach((c, i) => card(s, 0.7 + i * 4.05, 1.72, 3.8, 2.2, { title: c[0], body: c[1], num: String(i + 1), bodySize: 12, titleSize: 14 }));
 card(s, 0.7, 4.2, 5.9, 2.35, {
 title: "Modelo de movimiento",
 body: "Predice la pose a partir del control u odometría, con su ruido. Thrun distingue el modelo de velocidad del basado en odometría, en general más preciso en robots con encoders (Thrun et al., 2005, cap. 5).",
 bodySize: 12.5,
 });
 card(s, 6.85, 4.2, 5.75, 2.35, {
 title: "Modelo de observación",
 body: "Predice qué mediría el sensor desde una pose dada. Para telémetros, el modelo de haz combina medida correcta, objetos inesperados, fallos y ruido aleatorio (Thrun et al., 2005, p. 153 y ss.).",
 bodySize: 12.5,
 });
 s.addNotes("Clave conceptual: el EKF sigue bien pero no localiza globalmente, porque una gaussiana no representa «estoy en uno de estos cuatro pasillos idénticos». Esa limitación motiva exactamente la sesión siguiente. Ejemplo del pasillo simétrico en pizarra.");
 footer(s, "Thrun et al., 2005, cap. 5, cap. 6 (p. 153), cap. 7 (p. 192 y ss.)");
}

sectionSlide(p6, "S30", "Filtro de partículas y MCL", "Muestreo · pesos · remuestreo · robustez",
 "0-5 recuperación; 5-25 el filtro de partículas: representación por muestras, pesos y remuestreo; 25-42 localización de Montecarlo sobre mapa de rejilla; 42-55 robustez, variantes (AMCL, MCL aumentado) y comparación con EKF; 55-60 cierre.");

{
 const s = contentSlide(p6, "Representar la creencia con muestras", "S30 · Filtro de partículas");
 const cyc = [
 ["Muestrear", "Cada partícula se propaga con el modelo de movimiento y su ruido"],
 ["Pesar", "Cada partícula recibe un peso proporcional a la verosimilitud de la medida desde su pose"],
 ["Remuestrear", "Se sortean partículas con probabilidad proporcional al peso: sobreviven las coherentes"],
 ];
 cyc.forEach((c, i) => {
 card(s, 0.7 + i * 4.05, 1.75, 3.8, 2.5, { title: c[0], body: c[1], num: String(i + 1), bodySize: 12, titleSize: 14 });
 if (i < 2) arrowR(s, 4.62 + i * 4.05, 2.85, 20);
 });
 card(s, 0.7, 4.5, 5.9, 2.1, {
 title: "Qué gana",
 body: "No exige gaussianidad ni linealidad: representa creencias multimodales, resuelve la localización global y, con las variantes adecuadas, el secuestro.",
 bodySize: 12.5,
 });
 card(s, 6.85, 4.5, 5.75, 2.1, {
 title: "Qué cuesta",
 body: "El número de partículas gobierna precisión y coste. Con pocas, el filtro puede empobrecerse y descartar la hipótesis correcta; AMCL adapta ese número en marcha, y es el localizador de Nav2 en el bloque 7.",
 bodySize: 12.5,
 });
 s.addNotes("Demostración visual obligatoria: la nube de partículas de una localización global convergiendo a un único cúmulo. Es la imagen que los estudiantes recuerdan del bloque. Cerrar la comparación EKF/PF en una frase: gaussiana barata frente a muestras robustas.");
 footer(s, "Thrun et al., 2005, cap. 4 y cap. 8 · MCL y AMCL");
}

sectionSlide(p6, "S31", "SLAM: del EKF a los grafos", "Online y completo · EKF-SLAM · GraphSLAM · FastSLAM · SLAM visual",
 "0-10 recuperación de S29-S30; 10-35 el problema SLAM (online frente a completo) y por qué es circular; 35-60 EKF-SLAM y su límite cuadrático; 60-70 descanso; 70-95 GraphSLAM, grafos de factores y cierre de bucle; 95-105 FastSLAM, mapas de ocupación y panorama de SLAM visual y neuronal; 105-120 cuestionario B6 en Moodle (15 min).", { f: "fotos/b6_nube.png", cap: "Nube de puntos LiDAR: la materia prima del mapa", credito: "Foto: D. L. Lu CC BY 4.0 · Wikimedia Commons" });

{
 const s = contentSlide(p6, "El problema circular del SLAM", "S31 · Formulación");
 bullets(s, [
 { t: "Mapear y localizarse a la vez", h: true },
 { t: "Para construir el mapa hace falta saber dónde está el robot; para saber dónde está hace falta el mapa. SLAM resuelve ambos simultáneamente (Thrun et al., 2005, cap. 10)." },
 { t: "SLAM online: estima la pose actual y el mapa. SLAM completo: estima toda la trayectoria y el mapa (Thrun et al., 2005, p. 309 y ss.)." },
 { t: "El problema de correspondencia, ¿es este el punto de referencia que ya vi?, es la fuente principal de fallo catastrófico." },
 { t: "El cierre de bucle reconoce un lugar ya visitado y corrige de golpe la deriva acumulada de toda la trayectoria." },
 ], { w: 7.0 });
 card(s, 8.0, 1.7, 4.6, 4.9, {
 title: "EKF-SLAM",
 body: "El vector de estado incluye la pose y todos los puntos de referencia; la covarianza los correlaciona.\n\nEsa correlación es lo que hace funcionar el cierre de bucle: corregir la pose corrige todo el mapa.\n\nSu límite es el coste: la covarianza crece con el cuadrado del número de puntos.",
 bodySize: 12.5,
 });
 s.addNotes("Dibujar la matriz de covarianza creciendo con cada punto de referencia nuevo: la explicación gráfica del límite cuadrático es más eficaz que la algebraica. La correlación es virtud y coste a la vez.");
 footer(s, "Thrun et al., 2005, cap. 10 · pp. 309-312");
}

{
 const s = contentSlide(p6, "GraphSLAM, FastSLAM y el panorama actual", "S31 · Enfoques");
 const en = [
 ["GraphSLAM", "La trayectoria y las medidas forman un grafo: nodos son poses y puntos, aristas son restricciones blandas. Resolver el SLAM es minimizar el error de todas las restricciones (Thrun et al., 2005, cap. 11). Es el enfoque dominante en sistemas reales."],
 ["FastSLAM", "Factoriza el problema con un filtro de partículas para la trayectoria y filtros independientes por punto de referencia: escala a mapas grandes (Thrun et al., 2005, cap. 13, pp. 437-439)."],
 ["Mapas de ocupación", "Con la pose ya conocida, el mapeo se reduce a acumular evidencia por celda en log-odds (Thrun et al., 2005, pp. 281-286). Es el mapa que consumirá Nav2 en el bloque 7."],
 ["SLAM visual y neuronal", "Cámaras en lugar de LiDAR; y una frontera de investigación activa donde el mapa es una representación aprendida (NeRF, neuronal; 3D Gaussian Splatting, de primitivas explícitas) en vez de una nube de puntos."],
 ];
 en.forEach((c, i) => {
 const col = i % 2, row = Math.floor(i / 2);
 card(s, 0.7 + col * 6.1, 1.72 + row * 2.5, 5.85, 2.25, { title: c[0], body: c[1], num: String(i + 1), bodySize: 11.5, titleSize: 14 });
 });
 s.addNotes("Cierre del bloque: los grafos de factores son hoy el estándar y el motivo de que el SLAM pasara de apéndice a tema propio en esta asignatura. El panorama neuronal se presenta como frontera, no como examen, es material natural para el seminario de artículos de S41-S42. Reservar los últimos 15 minutos para el cuestionario B6 en Moodle.");
 footer(s, "Thrun et al., 2005, caps. 11 y 13 · pp. 337-339, 437-439, 281-286");
}

p6.writeFile({ fileName: "IQS_B6_Percepcion_SLAM.pptx" }).then(() => console.log("OK deck B6"));

/* ==================== DECK B7, ROS 2 y planificación ==================== */
const p7 = newDeck();

titleSlide(p7, {
 curso: "82514 · MECATRÓNICA Y ROBÓTICA",
 bloque: "Bloque 7",
 titulo: "Software robótico: ROS 2,\nsimulación y planificación",
 sub: "Sesiones S32–S37 · 8 horas",
 fechas: "25, 26 y 27 de noviembre y 2, 3 y 4 de diciembre de 2026 · IQS Universitat Ramon Llull",
});

{
 const s = contentSlide(p7, "Hoja de ruta del bloque", "Bloque 7");
 const rows = [
 ["S32 · mié 25 nov · 1 h", "Arquitectura de ROS 2: nodos, topics, DDS y QoS"],
 ["S33 · jue 26 nov · 1 h", "Servicios, acciones, parámetros, launch y colcon"],
 ["S34 · vie 27 nov · 2 h", "Taller: nodo rclpy, simulación en Gazebo y TF2"],
 ["S35 · mié 2 dic · 1 h", "Planificación: mapas, A*, PRM y RRT"],
 ["S36 · jue 3 dic · 1 h", "Navegación autónoma con Nav2"],
 ["S37 · vie 4 dic · 2 h", "Manipulación con MoveIt 2 e integración del stack"],
 ];
 rows.forEach((r, i) => agendaRow(s, 1.7 + i * 0.92, 0.78, String(i + 1), r[0], r[1], 13, 12));
 s.addNotes("Este es el bloque que faltaba por completo en la asignatura anterior. Todo funciona sobre los ordenadores existentes con simulación: no requiere hardware nuevo. Al terminar, cada equipo debe tener su proyecto corriendo en ROS 2.");
 footer(s, "82514 Mecatrónica y Robótica · B7 · IQS");
}

sectionSlide(p7, "S32", "Arquitectura de ROS 2", "Grafo de computación · topics y mensajes · DDS y QoS",
 "0-5 apertura del bloque; 5-20 de programa único a grafo de computación; 20-40 topics, mensajes y publicación/suscripción; 40-55 DDS y políticas de QoS con casos; 55-60 cierre y preparación del taller.", { f: "fotos/b7_roomba2.jpg", cap: "Roomba: un grafo de sensores y nodos con ruedas", credito: "Foto: CEphoto, U. Aranas CC BY-SA 4.0 · Wikimedia Commons" });

slideFotos(p7, "Las plataformas del stack", "S32–S36 · Hardware de referencia", [
 { f: "fotos/b7_turtlebot.jpg", x: 0.7, y: 1.5, w: 5.85, h: 5.0, cap: "TurtleBot3: la plataforma de referencia de ROS 2 y Nav2" },
 { f: "fotos/b7_almacen.jpg", x: 6.75, y: 1.5, w: 5.85, h: 5.0, cap: "Flota de robots de almacén (Ocado): el AMR de S6, en producción" },
], "Fotos: Kuscu0 CC BY-SA 4.0 · Techwords CC BY-SA 4.0 · Wikimedia Commons",
"El TurtleBot es el robot de los tutoriales oficiales que usa el taller S34 en simulación; la foto del almacén cierra el círculo con la distinción AGV/AMR del bloque 2.");

{
 const s = contentSlide(p7, "De un programa único a un grafo de procesos", "S32 · Arquitectura");
 bullets(s, [
 { t: "La idea que organiza todo el ecosistema", h: true },
 { t: "Un sistema robótico no es un programa: es un conjunto de procesos independientes, nodos, que se comunican por mensajes." },
 { t: "Cada nodo hace una cosa: leer el LiDAR, estimar la pose, planificar, mandar velocidades a las ruedas." },
 { t: "Ventaja de ingeniería: se sustituye un nodo sin tocar los demás, se reutiliza código entre robots y se depura por partes." },
 { t: "El precio: ya no hay una traza de ejecución única; depurar exige inspeccionar el grafo y los flujos de mensajes." },
 ], { w: 6.9 });
 card(s, 7.9, 1.7, 4.7, 4.9, {
 title: "Herramientas de inspección",
 body: "ros2 node list, qué está corriendo\nros2 topic list, qué canales existen\nros2 topic echo, ver mensajes en vivo\nros2 topic hz, frecuencia real\nrqt_graph, el grafo dibujado\n\nEstos cinco comandos resuelven la mayoría de los problemas del taller.",
 bodySize: 12.5,
 });
 s.addNotes("Dibujar el grafo de un robot móvil completo en pizarra: sensor, localización, planificador, controlador, actuadores. Los estudiantes deben salir sabiendo que «depurar ROS» significa mirar el grafo, no leer un main. Documentación: docs.ros.org, LTS Jazzy Jalisco.");
 footer(s, "docs.ros.org (Jazzy) · Understanding nodes and topics");
}

{
 const s = contentSlide(p7, "DDS y calidad de servicio", "S32 · Transporte");
 card(s, 0.7, 1.72, 5.9, 2.3, {
 title: "DDS: el transporte real",
 body: "ROS 2 no inventa su capa de red: se apoya en DDS, un estándar industrial de publicación/suscripción con descubrimiento automático. Por eso no hay un nodo maestro central como en ROS 1.",
 bodySize: 12.5,
 });
 card(s, 6.85, 1.72, 5.75, 2.3, {
 title: "Por qué importa en el aula",
 body: "Si dos ordenadores comparten red, sus grafos se ven entre sí. Aislar los equipos con ROS_DOMAIN_ID distintos evita horas de confusión en el taller.",
 bodySize: 12.5,
 });
 const qos = [
 ["Fiabilidad", "reliable reenvía hasta confirmar; best effort descarta. Un LiDAR a 40 Hz prefiere best effort; una orden de parada, reliable"],
 ["Durabilidad", "transient local guarda el último mensaje para quien llegue tarde: así funcionan los mapas y las descripciones del robot"],
 ["Perfil incompatible", "Si publicador y suscriptor no acuerdan perfil, no se conectan y no hay error visible: causa clásica de «no llega nada»"],
 ];
 qos.forEach((c, i) => card(s, 0.7 + i * 4.05, 4.25, 3.8, 2.3, { title: c[0], body: c[1], num: String(i + 1), bodySize: 11.5, titleSize: 13.5 }));
 s.addNotes("La incompatibilidad silenciosa de QoS es el fallo que más tiempo consume a los principiantes: anticiparlo aquí ahorra media sesión de taller. Documentación: About QoS settings, docs.ros.org (Jazzy).");
 footer(s, "docs.ros.org (Jazzy) · About QoS settings · About DDS/RMW");
}

sectionSlide(p7, "S33", "Servicios, acciones y orquestación", "Servicios · acciones · parámetros · launch · colcon",
 "0-5 recuperación de S32; 5-25 servicios y acciones frente a topics; 25-42 parámetros y launch files; 42-55 workspaces, paquetes y colcon; 55-60 preparación del entorno para el taller de S34.");

{
 const s = contentSlide(p7, "Tres formas de comunicar, tres semánticas", "S33 · Comunicación");
 const modes = [
 ["Topic", "Flujo continuo, sin respuesta, muchos a muchos.\n\nDatos de sensor, comandos de velocidad, estado.\n\n«Publico lo que sé; quien quiera, que escuche»."],
 ["Servicio", "Petición y respuesta, bloqueante y breve.\n\nConsultar una configuración, activar un modo.\n\n«Te pregunto y espero tu respuesta ahora»."],
 ["Acción", "Objetivo de larga duración con retroalimentación y cancelación.\n\nNavegar a un punto, ejecutar una trayectoria.\n\n«Encárgate de esto, ve informando, puedo cancelar»."],
 ];
 modes.forEach((c, i) => card(s, 0.7 + i * 4.05, 1.75, 3.8, 3.5, { title: c[0], body: c[1], num: String(i + 1), bodySize: 12, titleSize: 15 }));
 card(s, 0.7, 5.5, 11.9, 1.15, {
 title: "",
 body: "Regla práctica: si la tarea puede tardar y podría querer cancelarse, es una acción. Nav2 y MoveIt 2 exponen precisamente sus interfaces principales como acciones.",
 fill: "E3F7EC", bodySize: 12.5,
 });
 s.addNotes("El error típico del principiante es resolverlo todo con topics y acabar inventando a mano la lógica de una acción. Pedir a los estudiantes que clasifiquen cinco interacciones de su proyecto en estas tres categorías.");
 footer(s, "docs.ros.org (Jazzy) · Understanding services, actions, parameters");
}

{
 const s = contentSlide(p7, "Configurar, lanzar y construir", "S33 · Orquestación");
 const org = [
 ["Parámetros", "Configuración con nombre y tipo por nodo, ajustable sin recompilar y consultable en marcha: el mismo nodo sirve para varios robots"],
 ["Launch files", "Un sistema real arranca decenas de nodos; el launch los declara con sus parámetros y remapeos, y los levanta con una orden"],
 ["Workspace y paquetes", "El código vive en paquetes dentro de un workspace; el paquete es la unidad de reutilización y distribución"],
 ["colcon", "Construye todos los paquetes resolviendo dependencias. Con --symlink-install los cambios en Python se aplican sin reconstruir"],
 ];
 org.forEach((c, i) => {
 const col = i % 2, row = Math.floor(i / 2);
 card(s, 0.7 + col * 6.1, 1.75 + row * 2.45, 5.85, 2.2, { title: c[0], body: c[1], num: String(i + 1), bodySize: 12, titleSize: 14 });
 });
 card(s, 0.7, 6.4, 11.9, 0.7, {
 title: "",
 body: "Antes de S34: ros2 pkg create --build-type ament_python mi_paquete · colcon build --symlink-install · source install/setup.bash",
 fill: "E3F7EC", bodySize: 12,
 });
 s.addNotes("Dejar el entorno preparado hoy: los estudiantes que lleguen al taller sin workspace pierden la primera media hora. Publicar los comandos en el campus virtual al terminar la clase.");
 footer(s, "docs.ros.org (Jazzy) · Creating a workspace, package and launch file");
}

sectionSlide(p7, "S34", "Taller: rclpy, Gazebo y TF2", "Nodo en Python · simulación · árbol de transformadas",
 "0-15 anatomía de un nodo rclpy sobre plantilla; 15-45 escribir publicador y suscriptor y verlos en el grafo; 45-55 descanso; 55-85 simulación en Gazebo con el puente ros_gz; 85-110 TF2: árbol de transformadas, view_frames y tf2_echo; 110-120 puesta en común de errores frecuentes.");

{
 const s = contentSlide(p7, "Anatomía de un nodo y del taller", "S34 · Taller");
 bullets(s, [
 { t: "Un nodo rclpy en cinco piezas", h: true },
 { t: "Heredar de Node y darle nombre; crear publicadores y suscriptores con su tipo de mensaje, tema y perfil de QoS." },
 { t: "Un temporizador marca el ritmo de publicación; las devoluciones de llamada reaccionan a lo que llega." },
 { t: "rclpy.spin cede el control al ejecutor: a partir de ahí manda el flujo de mensajes, no el programa." },
 { t: "El punto de entrada se declara en setup.py para que colcon genere el ejecutable." },
 ], { w: 6.9 });
 card(s, 7.9, 1.7, 4.7, 4.9, {
 title: "Comandos del taller",
 body: "ros2 run mi_paquete mi_nodo\nros2 topic echo /cmd_vel\nros2 topic hz /scan\nrqt_graph\n\nros2 launch nav2_bringup\n tb3_simulation_launch.py\n\nros2 run tf2_tools view_frames\nros2 run tf2_ros tf2_echo map base_link",
 bodySize: 12,
 });
 s.addNotes("Ritmo del taller: cada bloque de 30 minutos termina con algo funcionando y visible. No dejar que nadie avance a Gazebo sin ver su nodo en rqt_graph. Recorrer los puestos durante los primeros 15 minutos: los fallos de entorno se detectan ahí.");
 footer(s, "docs.ros.org (Jazzy) · rclpy · gazebosim.org · ros_gz");
}

{
 const s = contentSlide(p7, "Simulación y el árbol de transformadas", "S34 · Gazebo y TF2");
 card(s, 0.7, 1.72, 5.9, 2.5, {
 title: "Gazebo y el puente ros_gz",
 body: "El simulador aporta física, sensores sintéticos y mundo; el puente traduce entre los mensajes de Gazebo y los de ROS 2.\n\nPermite desarrollar el stack completo sin tocar hardware, y sin poder romperlo.",
 bodySize: 12.5,
 });
 card(s, 6.85, 1.72, 5.75, 2.5, {
 title: "TF2: quién está dónde",
 body: "Mantiene el árbol de transformadas entre todos los marcos del robot y del mundo, con su historia temporal.\n\nPermite preguntar «dónde estaba el sensor respecto al mapa en el instante de esta medida»: sin eso, fusionar sensores es imposible.",
 bodySize: 12.5,
 });
 card(s, 0.7, 4.42, 11.9, 2.2, {
 title: "La convención que ordena la navegación (REP 105)",
 body: "map → odom → base_link → marcos de sensores. La transformada odom→base_link es continua pero deriva; la map→odom la corrige a saltos cuando la localización se actualiza. Entender esta cadena explica por qué el robot «salta» en RViz al cerrar un bucle, y conecta directamente con la localización del bloque 6 y con AMCL en S36.",
 fill: "E3F7EC", bodySize: 12.5,
 });
 s.addNotes("El árbol roto, un marco desconectado, es el segundo fallo más frecuente del taller después de QoS. Enseñar view_frames como primer diagnóstico. REP 105 se cita por designación, sin página.");
 footer(s, "docs.ros.org (Jazzy) · Introducing tf2 · REP 105");
}

sectionSlide(p7, "S35", "Planificación de trayectorias", "Mapas y C-space · A* · PRM y RRT · campos potenciales",
 "0-5 recuperación; 5-15 formulación: del mapa al espacio de configuraciones; 15-25 mapas de ocupación y de coste; 25-40 búsqueda en grafos: transformada de distancia y A*; 40-52 PRM y RRT; 52-60 campos potenciales y cierre.");

slideFotos(p7, "Buscar y muestrear, en imágenes", "S35 · Figura y animación", [
 { f: "figs/b7_astar_dijkstra.png", x: 0.7, y: 1.7, w: 7.3, h: 3.1, cap: "Mismo mapa, mismo camino óptimo: A* expande menos de la mitad de nodos" },
 { f: "gifs/b7_rrt.gif", x: 8.15, y: 1.55, w: 4.45, h: 4.6, cap: "RRT: las muestras tiran del árbol (cuaderno S35)" },
], "Figura y animación propias del curso (cuaderno S35)",
"La comparación de nodos expandidos es el argumento visual de la heurística admisible; la animación de RRT acompaña la frase de Lynch y Park que cita el guion.");

{
 const s = contentSlide(p7, "Del mapa al espacio de configuraciones", "S35 · Formulación");
 bullets(s, [
 { t: "Planificar no es dibujar una línea en el mapa", h: true },
 { r: [{ t: "El problema se plantea en el espacio de configuraciones: hallar un camino en C" }, { t: "libre", sub: true }, { t: " desde la configuración inicial a la meta (Lynch y Park, 2017, p. 353)." }] },
 { t: "Un robot circular en el plano se convierte en un punto si se inflan los obstáculos con su radio (Lynch y Park, 2017, p. 359)." },
 { t: "Inflar el obstáculo con el tamaño del robot es exactamente lo que hace la capa de inflado del costmap (Corke, 2023, p. 181)." },
 { t: "Completitud: un planificador puede ser completo, completo en resolución o completo probabilísticamente (Lynch y Park, 2017, p. 356)." },
 ], { w: 7.0 });
 card(s, 8.0, 1.7, 4.6, 4.9, {
 title: "Dos mapas, dos papeles",
 body: "Mapa de ocupación: qué celdas están libres, ocupadas o desconocidas, evidencia acumulada (Thrun et al., 2005, pp. 284-286).\n\nMapa de coste: cuánto cuesta pasar por cada celda, con obstáculos inflados y gradiente de proximidad (Corke, 2023, p. 182).\n\nEl primero describe el mundo; el segundo codifica la política de conducción.",
 bodySize: 12,
 });
 s.addNotes("La distinción entre mapa de ocupación y mapa de coste es la que permite entender Nav2 mañana. Ejemplo: dos rutas igual de cortas, una pegada a la pared y otra por el centro del pasillo, el coste, no la ocupación, decide.");
 footer(s, "Lynch y Park, 2017, pp. 353-359 · Corke, 2023, pp. 177-182");
}

{
 const s = contentSlide(p7, "Buscar y muestrear", "S35 · Algoritmos");
 const alg = [
 ["Transformada de distancia", "Propaga la distancia a la meta por todo el mapa; después basta descender el gradiente. Cara, pero da el camino óptimo desde cualquier punto (Corke, 2023, pp. 177-181)."],
 ["A*", "Búsqueda informada: coste acumulado más heurística de coste restante. Garantiza optimalidad solo si la heurística es admisible, es decir, nunca sobreestima (Corke, 2023, p. 175)."],
 ["PRM", "Muestrea configuraciones libres, las conecta en un grafo y luego consulta con A*. Compensa cuando hay muchas consultas sobre el mismo mapa (Lynch y Park, 2017, p. 384)."],
 ["RRT", "Crece un árbol hacia muestras aleatorias: «las muestras tiran del árbol» (Lynch y Park, 2017, p. 379). Domina en alta dimensión y admite restricciones no holonómicas (Corke, 2023, pp. 196-199)."],
 ];
 alg.forEach((c, i) => {
 const col = i % 2, row = Math.floor(i / 2);
 card(s, 0.7 + col * 6.1, 1.72 + row * 2.5, 5.85, 2.25, { title: c[0], body: c[1], num: String(i + 1), bodySize: 11.5, titleSize: 14 });
 });
 s.addNotes("Contar la anécdota de Shakey y el «truco de A*» de Hart, Nilsson y Raphael, 1966 (Corke, 2023, p. 174): el algoritmo que hoy mueve robots de almacén nació con el primer robot móvil que razonaba. Mencionar D* como A* dinámico que replanifica en marcha (Corke, 2023, pp. 182-184) y RRT* con recableado (Lynch y Park, 2017, p. 383).");
 footer(s, "Corke, 2023, pp. 174-199 · Lynch y Park, 2017, pp. 378-386");
}

sectionSlide(p7, "S36", "Navegación autónoma con Nav2", "Servidores · costmaps por capas · behavior trees · AMCL",
 "0-5 recuperación de S35; 5-20 arquitectura de servidores de Nav2; 20-38 costmaps por capas; 38-52 behavior trees, recuperación y AMCL; 52-60 demostración en simulación y cierre.");

{
 const s = contentSlide(p7, "Nav2: cómo se organiza un stack real", "S36 · Arquitectura");
 const nav = [
 ["Servidores especializados", "Planificador global, controlador local, suavizador, comportamientos de recuperación: cada uno es un servidor con su interfaz de acción, sustituible por configuración"],
 ["Costmaps por capas", "Estática (el mapa), obstáculos (sensores en vivo), inflado (margen del robot). Se combinan en un único mapa de coste maestro"],
 ["Behavior tree", "La lógica de navegación no está cableada: es un árbol que decide qué hacer y cómo reaccionar al fallo, reintentar, limpiar el costmap, girar en el sitio"],
 ["AMCL", "La localización de Nav2 es el filtro de partículas adaptativo del bloque 6: aquí es donde aquella teoría se convierte en un nodo que se lanza"],
 ];
 nav.forEach((c, i) => {
 const col = i % 2, row = Math.floor(i / 2);
 card(s, 0.7 + col * 6.1, 1.72 + row * 2.5, 5.85, 2.25, { title: c[0], body: c[1], num: String(i + 1), bodySize: 11.5, titleSize: 14 });
 });
 s.addNotes("El mensaje del día: Nav2 no es un algoritmo, es una arquitectura donde encajan los algoritmos de S35 y los filtros de B6. Demostración en simulación: fijar una meta en RViz y comentar en voz alta qué servidor actúa en cada momento y qué rama del árbol se dispara al bloquearse el paso.");
 footer(s, "docs.nav2.org · Navigation Concepts, Costmap 2D, Behavior Trees, AMCL");
}

sectionSlide(p7, "S37", "MoveIt 2 e integración del stack", "move_group · planning scene · OMPL · planificación cartesiana",
 "0-10 recuperación; 10-35 MoveIt 2: move_group y planning scene; 35-55 OMPL y los planificadores de muestreo en producción; 55-65 descanso; 65-90 planificación cartesiana y criterio de elección; 90-105 integración del stack completo y síntesis del bloque; 105-120 cuestionario B7 en Moodle (15 min).", { f: "fotos/b4_paletizado.png", cap: "Pick and place: la tarea canónica de MoveIt", credito: "Foto: CollaborativePalletizer CC BY-SA 4.0 · Wikimedia Commons" });

{
 const s = contentSlide(p7, "MoveIt 2: planificar con el mundo dentro", "S37 · Manipulación");
 card(s, 0.7, 1.72, 5.9, 2.45, {
 title: "move_group",
 body: "El nodo orquestador: recibe objetivos como acción, consulta la cinemática del bloque 4, invoca al planificador y devuelve una trayectoria ejecutable.",
 bodySize: 12.5,
 });
 card(s, 6.85, 1.72, 5.75, 2.45, {
 title: "Planning scene",
 body: "El modelo del mundo del manipulador: el robot, los obstáculos conocidos y los objetos percibidos.\n\nPlanificar sin escena es planificar contra el aire: aquí entra la percepción del bloque 6.",
 bodySize: 12.5,
 });
 card(s, 0.7, 4.37, 5.9, 2.25, {
 title: "OMPL y la elección del planificador",
 body: "La biblioteca de planificadores de muestreo por defecto. RRT-Connect, el RRT bidireccional de Lynch y Park, 2017, p. 382, es el caballo de batalla: rápido, sin garantía de optimalidad.",
 bodySize: 12.5,
 });
 card(s, 6.85, 4.37, 5.75, 2.25, {
 title: "Cartesiano frente a articular",
 body: "Si la tarea exige una trayectoria recta del efector, soldar, dispensar, insertar, se planifica en el espacio cartesiano y se paga en riesgo de singularidad (bloque 4). Si no, la planificación articular es más robusta.",
 bodySize: 12.5,
 });
 s.addNotes("Cierre del bloque y del semestre técnico: dibujar el stack completo en pizarra, percepción, localización, planificación, control, y señalar qué bloque de la asignatura aporta cada caja. Es la diapositiva mental que deben llevarse al examen. Reservar los últimos 15 minutos para el cuestionario B7 en Moodle.");
 footer(s, "moveit.picknik.ai · Concepts, OMPL, computeCartesianPath");
}

p7.writeFile({ fileName: "IQS_B7_ROS2_Planificacion.pptx" }).then(() => console.log("OK deck B7"));

/* ==================== DECK B8, Robótica basada en aprendizaje ==================== */
const p8 = newDeck();

titleSlide(p8, {
 curso: "82514 · MECATRÓNICA Y ROBÓTICA",
 bloque: "Bloque 8",
 titulo: "Robótica basada en aprendizaje\ny seminario de artículos",
 sub: "Sesiones S38–S42 · 6 horas",
 fechas: "9, 10, 11, 16 y 17 de diciembre de 2026 · IQS Universitat Ramon Llull",
});

{
 const s = contentSlide(p8, "Hoja de ruta del bloque", "Bloque 8");
 const rows = [
 ["S38 · mié 9 dic · 1 h", "Aprendizaje por refuerzo: MDP y Q-learning"],
 ["S39 · jue 10 dic · 1 h", "RL profundo, imitación y modelos VLA · sim-to-real"],
 ["S40 · vie 11 dic · 2 h", "EXAMEN PARCIAL 2 (bloques 5-7)"],
 ["S41 · mié 16 dic · 1 h", "Seminario de artículos científicos I"],
 ["S42 · jue 17 dic · 1 h", "Seminario de artículos científicos II y cierre"],
 ];
 rows.forEach((r, i) => agendaRow(s, 1.75 + i * 1.05, 0.88, String(i + 1), r[0], r[1], 13, 12));
 s.addNotes("El bloque nuevo de la asignatura, compactado a dos sesiones de docencia porque el viernes 11 es el parcial 2 (B5-B7). Enfoque conceptual: entender qué problema resuelve cada método y qué lo limita; los gemelos digitales quedan como lectura guiada. El cuestionario B8 se hace en Moodle, en casa, del 11 al 15 de diciembre. El seminario cierra el semestre.");
 footer(s, "82514 Mecatrónica y Robótica · B8 · IQS");
}

sectionSlide(p8, "S38", "Aprendizaje por refuerzo: MDP y Q-learning", "Interacción y recompensa · política y valor · aprendizaje sin modelo",
 "0-5 apertura del bloque; 5-20 el problema del RL y el MDP con sus cinco elementos; 20-38 política y funciones de valor; 38-55 Q-learning tabular con la actualización en pizarra y un ejemplo de rejilla; 55-60 límites del enfoque tabular y anuncio de S39.", { f: "fotos/b8_ajedrez3.jpg", cap: "Decisión secuencial: un brazo industrial juega al ajedrez", credito: "Foto: S. Kazantsev CC BY-SA 4.0 · Wikimedia Commons" });

slideFotos(p8, "Manipular y decidir", "S38–S40 · Imágenes del bloque", [
 { f: "fotos/b8_mano.jpg", x: 0.7, y: 1.5, w: 5.85, h: 5.0, cap: "Banco de manipulación diestra (NIST): el problema que motiva el bloque" },
 { f: "figs/b8_gridworld.png", x: 6.75, y: 1.7, w: 5.85, h: 4.6, cap: "La política óptima del gridworld de S38: flechas que rodean el peligro" },
], "Foto: NIST, dominio público · Wikimedia Commons · Figura propia del curso (cuaderno S38)",
"La foto sirve de apertura del bloque; la política del gridworld es el resultado que los estudiantes reproducen en el cuaderno de S38.");

{
 const s = contentSlide(p8, "El marco: decisión secuencial bajo incertidumbre", "S38 · MDP");
 const mdp = [
 ["Estado", "Lo que el agente observa del mundo en cada instante"],
 ["Acción", "Lo que puede hacer desde ese estado"],
 ["Transición", "Cómo evoluciona el mundo: puede ser estocástica"],
 ["Recompensa", "La señal escalar que define qué es «bien». Diseñarla es la parte difícil"],
 ["Descuento", "Cuánto pesa el futuro frente al presente"],
 ];
 mdp.forEach((c, i) => card(s, 0.7 + i * 2.5, 1.8, 2.25, 2.7, { title: c[0], body: c[1], num: String(i + 1), bodySize: 11.5, titleSize: 13.5 }));
 card(s, 0.7, 4.75, 5.9, 1.9, {
 title: "Lo distintivo del RL",
 body: "Sutton y Barto señalan dos rasgos propios: la búsqueda por ensayo y error, y la recompensa retardada, la acción buena de ahora puede pagarse mucho después (2018, cap. 1).",
 bodySize: 12.5,
 });
 card(s, 6.85, 4.75, 5.75, 1.9, {
 title: "El dilema permanente",
 body: "Explorar acciones nuevas frente a explotar lo que ya funciona. La estrategia epsilon-greedy es la respuesta mínima y la que usaremos en el ejemplo (Sutton y Barto, 2018, cap. 2).",
 bodySize: 12.5,
 });
 s.addNotes("El objetivo es maximizar el retorno acumulado, no la recompensa inmediata. Insistir en el diseño de la recompensa: la mayoría de los fracasos prácticos del RL en robótica son recompensas mal especificadas que el agente explota de formas imprevistas. Pedir ejemplos a la clase.");
 footer(s, "Sutton y Barto, 2018, caps. 1-3 (citado por capítulo)");
}

slideFotos(p8, "El valor se propaga desde la meta", "S38 · Animación", [
 { f: "gifs/b8_valor.gif", x: 0.8, y: 1.55, w: 7.2, h: 5.0, cap: "Iteración de valor, barrido a barrido: el valor fluye hacia atrás desde la meta" },
], "Animación propia del curso (cuaderno S38)",
"Proyectar tras escribir la actualizacion de Q-learning: el valor fluye hacia atrás desde la meta exactamente como el ejemplo de pizarra del guion. Detener la animación en el barrido 3 y preguntar qué celdas saben ya algo y cuáles no.");

{
 const s = contentSlide(p8, "Q-learning: aprender el valor de actuar", "S38 · Algoritmo");
 bullets(s, [
 { t: "De valor a política", h: true },
 { t: "La función Q(s,a) estima el retorno esperado de tomar la acción a en el estado s y actuar bien después. Si se conoce Q, la política óptima es elegir la acción de mayor Q." },
 { t: "Q-learning aprende Q sin modelo del mundo: solo con transiciones observadas (s, a, r, s'). La actualización:" },
 { t: "El corchete es el error de diferencia temporal: la sorpresa entre lo que esperaba y lo que la experiencia dice ahora (Sutton y Barto, 2018, cap. 6)." },
 ], { w: 7.2, h: 3.9 });
 eqImg(s, "qlearn", 0.85, 5.62, 6.9, 0.6);
 card(s, 8.2, 1.7, 4.4, 4.9, {
 title: "El muro de la tabla",
 body: "Q-learning tabular exige una entrada por cada par estado-acción.\n\nUn brazo de 6 ejes con estados continuos no cabe en ninguna tabla, y estados nunca visitados no aportan nada.\n\nLa solución, aproximar Q o la política con una red, es la sesión siguiente.",
 bodySize: 12.5,
 });
 s.addNotes("Ejecutar el ejemplo de rejilla en pizarra: cinco iteraciones a mano bastan para que se vea cómo el valor se propaga hacia atrás desde la meta. Escribir la actualización completa y desglosar cada término antes de correr el ejemplo.");
 footer(s, "Sutton y Barto, 2018, cap. 6 · Q-learning");
}

sectionSlide(p8, "S39", "RL profundo, imitación y VLA", "PPO y sim-to-real · behavior cloning y diffusion policies · modelos fundacionales",
 "0-5 recuperación de S38; 5-15 políticas parametrizadas y PPO (solo las ideas); 15-25 simuladores y aleatorización de dominio; 25-40 imitación: behavior cloning, errores compuestos y diffusion policies; 40-52 modelos VLA: RT-2, OpenVLA, π0 y GR00T; 52-60 cierre, gemelos digitales como lectura guiada, logística del seminario y del parcial 2, y cuestionario B8 en Moodle (11-15 dic).");

{
 const s = contentSlide(p8, "De la tabla a la red, y de la simulación al robot", "S39 · RL profundo");
 card(s, 0.7, 1.72, 5.9, 2.4, {
 title: "Política parametrizada",
 body: "Una red sustituye a la tabla: recibe la observación y produce la acción. Generaliza a estados nunca vistos, a cambio de perder las garantías teóricas del caso tabular (Sutton y Barto, 2018, cap. 13).",
 bodySize: 12.5,
 });
 card(s, 6.85, 1.72, 5.75, 2.4, {
 title: "PPO",
 body: "El algoritmo de referencia en robótica: mejora la política limitando cuánto puede cambiar en cada paso, mediante un recorte que evita saltos destructivos (Schulman et al., 2017, arXiv:1707.06347).\n\nTolera hiperparámetros razonables sin ajuste fino: por eso se impuso.",
 bodySize: 12,
 });
 card(s, 0.7, 4.32, 5.9, 2.3, {
 title: "Por qué en simulación",
 body: "PPO necesita millones de interacciones. En un robot real serían años y varios robots rotos; en simulación paralela masiva (MuJoCo, Isaac Lab), horas.",
 bodySize: 12.5,
 });
 card(s, 6.85, 4.32, 5.75, 2.3, {
 title: "La brecha de realidad",
 body: "Lo aprendido en simulación falla en el robot: fricción, retardos y ruido no modelados. La aleatorización de dominio entrena bajo parámetros variables para forzar políticas robustas (Tobin et al., 2017, arXiv:1703.06907; OpenAI, 2019, arXiv:1910.07113).",
 bodySize: 11.5,
 });
 s.addNotes("La receta que convirtió a los cuadrúpedos comerciales en productos: PPO en miles de simulaciones paralelas más aleatorización de dominio. Mostrar un vídeo de entrenamiento paralelo: la imagen de mil robots aprendiendo a la vez explica el método sin ecuaciones.");
 footer(s, "Schulman et al., 2017 · Tobin et al., 2017 · OpenAI, 2019");
}


{
 const s = contentSlide(p8, "Aprender de demostraciones", "S39 · Imitación");
 bullets(s, [
 { t: "Behavior cloning: el enfoque directo", h: true },
 { t: "Un humano teleopera el robot; la red aprende a reproducir la acción demostrada dada la observación. Es aprendizaje supervisado sobre pares observación-acción." },
 { t: "Ventaja decisiva sobre el RL: no hace falta diseñar recompensa ni explorar millones de veces." },
 { t: "Su fallo característico: al desviarse ligeramente entra en estados no demostrados y el error se acumula." },
 { t: "Diffusion policies: en lugar de predecir una acción, generan secuencias de acciones por un proceso de difusión, lo que maneja mejor la multimodalidad (Chi et al., 2023, arXiv:2303.04137)." },
 ], { w: 7.1 });
 card(s, 8.1, 1.7, 4.5, 4.9, {
 title: "Por qué importa la multimodalidad",
 body: "Ante un obstáculo, esquivar por la izquierda o por la derecha son ambas correctas.\n\nUna red que predice la acción promedio elige el centro: choca.\n\nGenerar la distribución completa de acciones, y no su media, resuelve el problema.",
 bodySize: 12.5,
 });
 s.addNotes("El ejemplo del obstáculo es el que hace entender por qué las diffusion policies desplazaron al behavior cloning ingenuo. Mencionar ACT y la línea de manipulación bimanual de bajo coste (Zhao et al., 2023, arXiv:2304.13705) como referencia para el seminario.");
 footer(s, "Chi et al., 2023, arXiv:2303.04137 · Zhao et al., 2023, arXiv:2304.13705");
}

{
 const s = contentSlide(p8, "Modelos visión-lenguaje-acción", "S39 · Modelos fundacionales");
 const vla = [
 ["RT-2", "Demuestra que un modelo visión-lenguaje entrenado con datos web transfiere conocimiento al control robótico (Google DeepMind, 2023, arXiv:2307.15818)"],
 ["OpenVLA", "Abre la receta completa: 7B de parámetros y pesos publicados, lo que permite reproducir y ajustar (Kim et al., 2024, arXiv:2406.09246)"],
 ["π0", "Modelo de flujo visión-lenguaje-acción para control general de robots, de Physical Intelligence (Black et al., 2024, arXiv:2410.24164)"],
 ["GR00T N1", "Modelo fundacional abierto para robots humanoides generalistas (NVIDIA, 2025, arXiv:2503.14734). Gemini Robotics lleva la familia Gemini al control físico (Google DeepMind, 2025)"],
 ];
 vla.forEach((c, i) => {
 const col = i % 2, row = Math.floor(i / 2);
 card(s, 0.7 + col * 6.1, 1.72 + row * 2.4, 5.85, 2.15, { title: c[0], body: c[1], num: String(i + 1), bodySize: 11.5, titleSize: 14 });
 });
 card(s, 0.7, 6.32, 11.9, 0.78, {
 title: "",
 body: "El patrón común: una arquitectura preentrenada con datos de internet, ajustada con demostraciones robóticas, que acepta instrucciones en lenguaje natural y produce acciones motoras.",
 fill: "E3F7EC", bodySize: 12,
 });
 s.addNotes("Estos cuatro son los que hay que conocer en 2026. Mostrar un vídeo de π0 o GR00T ejecutando una tarea larga y preguntar: ¿qué parte de lo que veis es percepción, cuál planificación, cuál control? La respuesta, el VLA genera consignas que ejecutan los lazos del bloque 5, es la síntesis del curso.");
 footer(s, "arXiv:2307.15818 · 2406.09246 · 2410.24164 · 2503.14734");
}

{
 const s = contentSlide(p8, "Gemelos digitales y síntesis del bloque", "S39 · Cierre y lectura");
 card(s, 0.7, 1.72, 5.9, 2.55, {
 title: "Gemelo digital",
 body: "Una réplica virtual de la célula o la planta, sincronizada con datos reales, sobre la que se simula, se valida y se entrena antes de tocar el sistema físico.\n\nEn robótica cierra el círculo: es el mismo simulador de S39 puesto al servicio de la ingeniería de fabricación.",
 bodySize: 12.5,
 });
 card(s, 6.85, 1.72, 5.75, 2.55, {
 title: "Eco del bloque 1",
 body: "Es la evolución de diseño de De Silva llevada a su consecuencia: un modelo del sistema real que se monitoriza, se optimiza y devuelve mejoras al sistema (De Silva et al., 2016, p. 8).\n\nLa idea tenía diez años; hoy tiene herramientas.",
 bodySize: 12.5,
 });
 card(s, 0.7, 4.47, 11.9, 2.15, {
 title: "Dónde encaja el aprendizaje en el temario clásico",
 body: "El aprendizaje no sustituye a la cinemática, al control ni a la estimación: se apoya en ellos. Un VLA decide qué hacer; la cinemática del bloque 4 y los lazos del bloque 5 lo ejecutan; la percepción del bloque 6 le da los ojos; ROS 2 del bloque 7 lo conecta con el hardware. El ingeniero valioso en 2026 es el que entiende ambas mitades y sabe cuándo cada una aporta valor.",
 fill: "E3F7EC", bodySize: 12.5,
 });
 s.addNotes("Esta es la diapositiva de cierre conceptual de la asignatura completa. Dedicarle tiempo: es la respuesta a la pregunta que muchos traen desde septiembre, «¿para qué estudio cinemática si ya existe la IA?». El cuestionario B8 se hace en Moodle, en casa, en la ventana del 11 al 15 de diciembre; recordarlo aquí.");
 footer(s, "De Silva et al., 2016, p. 8 · Síntesis del curso");
}

sectionSlide(p8, "S40", "Examen parcial 2", "Bloques 5-7 · test y tres problemas · 2 horas",
 "Reservar aula de examen. Seis versiones (A-F) en damero. 0-5 acomodo e instrucciones; 5-115 examen; 115-120 recogida. La rúbrica y las soluciones se publican tras la corrección; el cuestionario B8 sigue abierto en Moodle hasta el 15 de diciembre.");

{
 const s = contentSlide(p8, "Parcial 2: estructura y reglas", "S40 · Examen");
 const partes = [
 ["A", "Test (2,0 pt)", "10 preguntas ABCD sobre B5-B7; cada error resta un tercio; en blanco no puntúa"],
 ["B", "Control de una articulación (3,0 pt)", "Diseño PD para ζ y ωn · sobreoscilación · error estacionario con gravedad · windup"],
 ["C", "Estimación (2,5 pt)", "Un paso completo de filtro de Kalman 1D · lectura de la ganancia · EKF frente a MCL"],
 ["D", "Planificación y ROS 2 (2,5 pt)", "A* sobre rejilla con heurística Manhattan · admisibilidad · diagnóstico de QoS"],
 ];
 partes.forEach((c, i) => card(s, 0.7, 1.7 + i * 1.16, 11.9, 1.0, { title: c[1], body: c[2], num: c[0], bodySize: 12, titleSize: 13.5 }));
 card(s, 0.7, 6.42, 11.9, 0.62, { title: "", body: "Material: calculadora no programable y una hoja A4 de formulario manuscrito por las dos caras. El planteamiento vale el 40 % de cada apartado; un resultado sin desarrollo no puntúa.", fill: "E3F7EC", bodySize: 11.5 });
 s.addNotes("Proyectar al cerrar S39 y publicar en el campus. Recordar que B8 entra solo en el cuestionario de Moodle y en el examen final de enero, no en este parcial. Insistir en el formulario manuscrito: prepararlo es la mejor sesión de repaso que existe.");
 footer(s, "Parcial 2 · viernes 11 de diciembre · 2 h");
}

sectionSlide(p8, "S41 · S42", "Seminario de artículos científicos", "16 y 17 de diciembre · presentaciones por parejas y cierre del semestre",
 "Cada sesión: 0-5 encuadre y orden de intervención; 5-55 cinco presentaciones de 10 minutos (7 de exposición y 3 de preguntas), cronometradas; 55-60 síntesis del profesor. En S42, los últimos 15 minutos se dedican al cierre global y al mapa de artículos por bloque.");

{
 const s = contentSlide(p8, "Cómo se desarrollan las dos sesiones", "S41–S42 · Logística");
 card(s, 0.7, 1.72, 5.9, 2.45, {
 title: "Formato",
 body: "Parejas. 7 minutos de exposición y 3 de preguntas, cronometrados en pantalla.\n\nOrden publicado la víspera. Cinco parejas por sesión.\n\nToda entrega es defendible oralmente y de forma individual.",
 bodySize: 12.5,
 });
 card(s, 6.85, 1.72, 5.75, 2.45, {
 title: "Qué debe cubrir cada presentación",
 body: "Problema · método · resultados · limitaciones · conexión explícita con al menos un bloque del curso.\n\nLa última es obligatoria: es lo que convierte el seminario en parte de la asignatura y no en un añadido.",
 bodySize: 12.5,
 });
 card(s, 0.7, 4.37, 11.9, 2.25, {
 title: "Preguntas comodín del profesor",
 body: "Si el público no pregunta, el profesor dispone de una batería preparada: ¿cuál es la línea base con la que se comparan y es justa? ¿Qué pasaría con este método en el robot del laboratorio? ¿Qué limitación reconocen los autores y cuál se les ha escapado? ¿Qué bloque del curso hace falta dominar para implementar esto? Estas preguntas también modelan qué se espera del público en la sesión siguiente.",
 fill: "E3F7EC", bodySize: 12.5,
 });
 s.addNotes("Cronometrar en serio desde la primera pareja: si se permite que la primera se alargue, la sesión se descuadra. Anotar la rúbrica en caliente, entre presentaciones, no al final. Las preguntas del público cuentan para la participación de quien las hace: decirlo al empezar.");
 footer(s, "Seminario lanzado en S4 · 17 de septiembre");
}

{
 const s = contentSlide(p8, "Rúbrica de evaluación", "S41–S42 · Evaluación");
 const rub = [
 ["40%", "Comprensión técnica", "¿Entienden el método o repiten el resumen? Se comprueba en las preguntas, no en las diapositivas"],
 ["30%", "Claridad", "Estructura, ritmo, calidad de las figuras y capacidad de hacer accesible lo complejo"],
 ["20%", "Análisis crítico", "Limitaciones reconocidas y no reconocidas, honestidad de la comparación, aplicabilidad real"],
 ["10%", "Gestión de preguntas", "Responder lo que se sabe, admitir lo que no y razonar en voz alta"],
 ];
 rub.forEach((c, i) => {
 const y = 1.75 + i * 1.32;
 s.addShape("roundRect", { x: 0.7, y, w: 11.9, h: 1.14, rectRadius: 0.08, fill: { color: i % 2 ? BG_LT : "E3F7EC" }, line: { type: "none" } });
 s.addText(c[0], { x: 0.95, y, w: 1.25, h: 1.14, align: "center", valign: "middle", fontFace: "Calibri", fontSize: 26, bold: true, color: GREEN_DK, margin: 0 });
 s.addText([
 { text: c[1], options: { bold: true, color: NAVY, fontSize: 14, breakLine: true } },
 { text: c[2], options: { color: INK, fontSize: 12 } },
 ], { x: 2.35, y, w: 10.0, h: 1.14, valign: "middle", fontFace: "Calibri", margin: 0 });
 });
 s.addNotes("Publicar la rúbrica en el campus el mismo día del lanzamiento (S4) y volver a proyectarla al empezar S41: nadie debe llegar sin saber cómo se le evalúa. El peso mayor en comprensión técnica es deliberado y conviene explicarlo: premia estudiar el artículo, no maquetar diapositivas.");
 footer(s, "Rúbrica publicada en S4 · Presentaciones S41–S42");
}

sectionSlide(p8, "S43", "Defensas del proyecto y cierre", "18 de diciembre · 2 h · defensas, repaso del examen y síntesis del semestre",
 "0-10 encuadre y rúbrica en pantalla; 10-95 defensas de los cinco equipos (12 min + 5 de preguntas, cronometrados, cerrando rúbrica entre equipo y equipo); 95-105 repaso orientado al examen de enero con lo que entra de forma literal por bloque; 105-120 cierre del semestre, mapa de artículos de S42 y encuesta de retroalimentación.");

{
 const s = contentSlide(p8, "La defensa: qué se evalúa y con qué peso", "S43 · Proyecto integrador");
 const rub = [
 ["40%", "Integración técnica", "¿Los módulos hablan entre sí, hay un sistema, o cuatro prácticas juntas? Es la competencia RAM23-S de la guía docente"],
 ["25%", "Resultados medidos", "Al menos una métrica: error de seguimiento, tiempo de ciclo, tasa de éxito en N intentos, error de localización"],
 ["20%", "Análisis crítico", "Limitaciones reconocidas, diagnóstico de lo que falló y camino propuesto"],
 ["15%", "Claridad y reparto", "Exposición ordenada y participación real de todos los miembros: la defensa es individual"],
 ];
 rub.forEach((c, i) => {
 const y = 1.7 + i * 1.2;
 s.addShape("roundRect", { x: 0.7, y, w: 11.9, h: 1.04, rectRadius: 0.08, fill: { color: i % 2 ? BG_LT : "E3F7EC" }, line: { type: "none" } });
 s.addText(c[0], { x: 0.95, y, w: 1.25, h: 1.04, align: "center", valign: "middle", fontFace: "Calibri", fontSize: 24, bold: true, color: GREEN_DK, margin: 0 });
 s.addText([
 { text: c[1], options: { bold: true, color: NAVY, fontSize: 13.5, breakLine: true } },
 { text: c[2], options: { color: INK, fontSize: 11.5 } },
 ], { x: 2.35, y, w: 10.0, h: 1.04, valign: "middle", fontFace: "Calibri", margin: 0 });
 });
 card(s, 0.7, 6.42, 11.9, 0.56, {
 title: "",
 body: "Criterio que se dice en voz alta antes de empezar: un proyecto que no funcionó del todo, pero cuyo equipo sabe por qué, lo ha medido y propone un camino, puntúa por encima de uno que funciona sin explicación.",
 fill: BG_LT, bodySize: 11.5,
 });
 s.addNotes("Proyectar la rúbrica antes de la primera defensa y cerrar la puntuación de cada equipo en los 30 segundos siguientes a su turno: acumular la corrección para el final la degrada. Preguntas comodín si el público calla: qué falló primero y cómo se diagnosticó; qué harían con una semana más; qué cambiaría con otro robot; qué medida de seguridad del bloque 2 exigiría su célula.");
 footer(s, "Rúbrica del proyecto · RAM23-S de la guía docente");
}

{
 const s = contentSlide(p8, "Repaso del examen: qué entra de forma literal", "S43 · Cierre del semestre");
 const rep = [
 ["B1", "Definición de mecatrónica y los ocho componentes de un sistema mecatrónico"],
 ["B2", "Las dos partes de la ISO 10218 y los cuatro métodos de operación colaborativa"],
 ["B3", "Características estáticas de un sensor y criterios de selección de actuador"],
 ["B4", "Cinemática directa e inversa, jacobiano y singularidades"],
 ["B5", "Modelado de un lazo, respuesta temporal y sintonía"],
 ["B6", "Filtro de Bayes, ciclo predicción-corrección y formulación del SLAM"],
 ["B7", "Grafo de computación de ROS 2, A* y familias de planificadores"],
 ["B8", "MDP, actualización de Q-learning y qué es un modelo VLA"],
 ];
 rep.forEach((c, i) => {
 const col = i % 2, row = Math.floor(i / 2);
 const x = 0.7 + col * 6.1, y = 1.7 + row * 1.16;
 s.addShape("roundRect", { x, y, w: 5.85, h: 1.0, rectRadius: 0.08, fill: { color: BG_LT }, line: { type: "none" } });
 s.addShape("ellipse", { x: x + 0.2, y: y + 0.25, w: 0.5, h: 0.5, fill: { color: GREEN }, line: { type: "none" } });
 s.addText(c[0], { x: x + 0.2, y: y + 0.25, w: 0.5, h: 0.5, align: "center", valign: "middle", fontFace: "Calibri", fontSize: 14, bold: true, color: NAVY, margin: 0 });
 s.addText(c[1], { x: x + 0.85, y, w: 4.8, h: 1.0, valign: "middle", fontFace: "Calibri", fontSize: 11.5, color: INK, margin: 0 });
 });
 card(s, 0.7, 6.4, 11.9, 0.58, {
 title: "",
 body: "No se pregunta de forma literal: manipular la ecuación del MDP, derivar las ecuaciones del EKF ni reproducir la arquitectura interna de un VLA. Examen de muestra con solución comentada, publicado hoy en el campus.",
 fill: "E3F7EC", bodySize: 11.5,
 });
 s.addNotes("Terminar el semestre con las dos síntesis visuales: el mapa de artículos por bloque construido en S42 y el diagrama del stack completo de S37. Después, la encuesta anónima de retroalimentación (5 min): qué bloque fue más útil, cuál más difícil, qué debería ocupar más o menos tiempo. Ese es el insumo para revisar la guía docente el curso que viene.");
 footer(s, "Convocatoria de enero · Tutorías durante el periodo de exámenes");
}

p8.writeFile({ fileName: "IQS_B8_Robot_Learning.pptx" }).then(() => console.log("OK deck B8"));
