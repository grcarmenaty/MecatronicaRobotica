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

/* ==================== DECK B3 ==================== */
const p3 = newDeck();

titleSlide(p3, {
 curso: "82514 · MECATRÓNICA Y ROBÓTICA",
 bloque: "Bloque 3",
 titulo: "Sensores y actuadores",
 sub: "Sesiones S8–S12 · 6 horas",
 fechas: "30 de septiembre y 1, 2, 7 y 8 de octubre de 2026 · IQS Universitat Ramon Llull",
});

// Hoja de ruta B3
{
 const s = contentSlide(p3, "Hoja de ruta del bloque", "Bloque 3");
 const rows = [
 ["S8 · mié 30 sep · 1 h", "Arquitectura de instrumentación y características de sensores"],
 ["S9 · jue 1 oct · 1 h", "Sensores de posición, velocidad e inercia (encoders, LVDT, IMU)"],
 ["S10 · vie 2 oct · 2 h", "Fuerza, tacto y rango; ejercicio puntuable de selección de sensores"],
 ["S11 · mié 7 oct · 1 h", "Actuadores eléctricos: motor DC, BLDC, paso a paso y servoaccionamientos"],
 ["S12 · jue 8 oct · 1 h", "Hidráulica, neumática y selección motor-reductora · cuestionario B3"],
 ];
 rows.forEach((r, i) => agendaRow(s, 1.62 + i * 1.05, 0.9, String(i + 1), r[0], r[1]));
 s.addNotes("Presentar el bloque como las dos cajas de los extremos del sistema mecatrónico de B1: percibir (S8-S10) y actuar (S11-S12). El entregable del bloque es el cuestionario B3 en los últimos 10 minutos de S12; el ejercicio de selección de sensores de S10 es puntuable en clase.");
 footer(s, "82514 Mecatrónica y Robótica · B3 · IQS");
}

// S8
sectionSlide(p3, "S8", "Arquitectura de instrumentación", "Cadena de adquisición · Nyquist · características estáticas y dinámicas",
 "0-5 apertura del bloque (sensores S8-S10, actuadores S11-S12; anunciar cuestionario B3 en S12); 5-20 cadena de instrumentación (Fraden pp. 2-5) y teorema de Nyquist con las figuras de aliasing (De Silva pp. 150-152); 20-45 características estáticas sobre una única gráfica en la pizarra (Fraden pp. 13-38); 45-55 características dinámicas y regla posición/velocidad/aceleración (Fraden pp. 41-42 y 327); 55-60 cierre con one-minute paper: definir resolución y distinguirla de exactitud.", { f: "fotos/b3_ultrasonido.jpg", cap: "HC-SR04: sensor y acondicionamiento en la misma placa", credito: "Foto: S. Dwivedi CC BY-SA 4.0 · Wikimedia Commons" });

{
 const s = contentSlide(p3, "La cadena de instrumentación", "S8 · Adquisición de datos");
 const chain = [
 ["Sensor", "estímulo → señal eléctrica"],
 ["Acondicionador", "interfaz de señal"],
 ["Multiplexor", "un canal cada vez"],
 ["Conversor A/D", "muestreo y cuantización"],
 ["Computador", "gobierna la temporización"],
 ["Actuador", "motor, solenoide, válvula"],
 ];
 chain.forEach((c, i) => {
 const x = 0.7 + i * 2.03;
 card(s, x, 1.7, 1.75, 1.5, { title: c[0], body: c[1], titleSize: 11.5, bodySize: 9.5 });
 if (i < 5) arrowR(s, x + 1.73, 2.2, 15);
 });
 card(s, 0.7, 3.5, 5.9, 1.75, {
 title: "Vocabulario preciso (Fraden)",
 body: "Sensor: «recibe un estímulo y responde con una señal eléctrica». Transductor: convierte una energía en otra. Actuador: «lo opuesto a un sensor». El altavoz es transductor; el motor, actuador.",
 bodySize: 12,
 });
 card(s, 6.85, 3.5, 5.75, 1.75, {
 title: "Pasivo / activo · directo / complejo",
 body: "El termistor es activo: necesita excitación externa que el estímulo modifica. Un sensor complejo encadena transductores antes del sensor directo final.",
 bodySize: 12,
 });
 card(s, 0.7, 5.45, 11.9, 1.25, {
 title: "Muestreo: teorema de Nyquist-Shannon",
 body: [{ text: "f" }, { text: "s", options: { subscript: true } }, { text: " ≥ 2·f" }, { text: "señal", options: { subscript: true } }, { text: " para evitar el aliasing; los analizadores usan factor 2,56. Pregunta: ¿qué pasa si muestreo una vibración de 400 Hz a 500 Hz? Ningún filtro digital posterior deshace un aliasing ya cometido." }],
 fill: "E3F7EC", bodySize: 12,
 });
 s.addNotes("Escribir la definición de sensor en la pizarra y contraponerla a transductor y actuador. Dibujar el diagrama de bloques completo aunque esté en pantalla. Cerrar el segmento con la pregunta de los 400 Hz a 500 Hz: la señal aparece como un alias de baja frecuencia.");
 footer(s, "Fraden, 2016, pp. 2-5 · De Silva et al., 2016, pp. 147-152");
}

{
 const s = contentSlide(p3, "Características estáticas y dinámicas", "S8 · Hoja de datos");
 const specs = [
 ["Span (FS)", "Rango dinámico de estímulos convertibles (p. 30)"],
 ["Exactitud", "«En realidad, inexactitud»: máxima desviación del valor verdadero (p. 31)"],
 ["Histéresis", "La salida depende del lado por el que llega el estímulo (p. 35)"],
 ["No linealidad", "Desviación máxima respecto a la recta de ajuste (p. 36)"],
 ["Saturación", "La respuesta se limita a estímulos altos (p. 37)"],
 ["Repetibilidad", "Dispersión entre ciclos idénticos, en % FS (p. 38)"],
 ["Banda muerta", "Insensibilidad en un rango de entrada (p. 38)"],
 ["Resolución", "Incremento más pequeño de estímulo detectable (p. 38)"],
 ];
 specs.forEach((c, i) => {
 const col = i % 4, row = Math.floor(i / 4);
 card(s, 0.7 + col * 3.075, 1.7 + row * 1.62, 2.85, 1.47, { title: c[0], body: c[1], titleSize: 13, bodySize: 10.5 });
 });
 card(s, 0.7, 5.12, 11.9, 1.15, {
 title: "Características dinámicas",
 body: "Orden cero (instantáneo) · primer orden con constante de tiempo τ y corte a −3 dB (sensor de temperatura) · segundo orden con masa móvil (acelerómetro, S9). Regla de Fraden: posición hasta ~10 Hz, velocidad hasta ~1 kHz, aceleración por encima (p. 327).",
 fill: "E3F7EC", bodySize: 11.5,
 });
 card(s, 0.7, 6.42, 11.9, 0.52, {
 title: "",
 body: "Aviso de ingeniero: repetibilidad ≠ exactitud, un sesgo estable se calibra; una dispersión, no. Calibración solo si las tolerancias superan la exactitud requerida (p. 20).",
 fill: BG_LT, bodySize: 11,
 });
 s.addNotes("Recorrer todas las especificaciones sobre una única gráfica anotada en la pizarra: el estudiante debe salir sabiendo leer una hoja de datos como la tabla de Fraden (p. 8). Función de transferencia S = f(s) y su inversa F(S) para «romper el código»; sensibilidad como derivada dS/ds. Ejemplo de no linealidad: el termistor NTC, que se linealiza por software (p. 532).");
 footer(s, "Fraden, 2016, pp. 13-42");
}

// S9
sectionSlide(p3, "S9", "Posición, velocidad e inercia", "Encoders · LVDT · efecto Hall · acelerómetros · giróscopos · IMU",
 "0-5 recuperación de S8 (span; por qué no derivar posición para obtener aceleración) e introducción propioceptivo/exteroceptivo (Corke pp. 8-9); 5-25 posición y desplazamiento: encoder con cuadratura en pizarra, LVDT, Hall (Fraden pp. 288-310); 25-45 acelerómetros y giróscopos (Fraden pp. 327-344); 45-55 IMU y navegación inercial con el modelo de error (Corke pp. 107-119); 55-60 cierre: anunciar S10 con ejercicio puntuable y encargar la lista de selección de acelerómetro (Fraden p. 332).");

slideFotos(p3, "El hardware, de cerca", "S9–S10 · Sensores reales", [
 { f: "fotos/b3_encoder.jpg", x: 0.7, y: 1.5, w: 5.85, h: 2.5, cap: "Encoder incremental (corte): disco y detector" },
 { f: "fotos/b3_imu.jpg", x: 6.75, y: 1.5, w: 5.85, h: 2.5, cap: "IMU MEMS sobre un centavo (DARPA TIMU)" },
 { f: "fotos/b3_galga.jpg", x: 0.7, y: 4.35, w: 5.85, h: 2.5, cap: "Galga extensométrica sin montar" },
 { f: "fotos/b3_lidar.jpg", x: 6.75, y: 4.35, w: 5.85, h: 2.5, cap: "LiDAR Velodyne sobre vehículo autónomo" },
], "Fotos: Lambtron CC BY-SA 4.0 · Univ. Michigan dominio público · Pleriche CC BY-SA 4.0 · S. Jurvetson CC BY 2.0 · Wikimedia Commons",
"Proyectar al presentar cada familia de sensor: la escala del IMU sobre el centavo es el dato que más recuerdan.");

{
 const s = contentSlide(p3, "Posición y desplazamiento", "S9 · Propioceptivos");
 const cols = [
 ["Encoder óptico", "Disco con sectores opacos y transparentes que interrumpe un haz. Incremental (un pulso por paso) o absoluto (código Gray/binario en el radio). Dos canales A y B en cuadratura (90°) dan cuenta y sentido de giro; decodificación x4 multiplica la resolución."],
 ["LVDT", "Transformador con núcleo móvil: primario senoidal, secundarios en oposición de fase; salida nula en el centro, amplitud proporcional al desplazamiento y sentido dado por la fase. Sin contacto ni desgaste; resolución nanométrica. Versión rotativa: RVDT; pariente industrial: el resolver."],
 ["Efecto Hall", "Tensión transversal proporcional al campo magnético. Sensores analógicos y biestables para posición y proximidad, y la base de la conmutación electrónica de los BLDC de S11."],
 ];
 cols.forEach((c, i) => card(s, 0.7 + i * 4.05, 1.7, 3.8, 3.35, { title: c[0], body: c[1], num: String(i + 1), bodySize: 11.5, titleSize: 14 }));
 card(s, 0.7, 5.3, 5.9, 1.35, {
 title: "Truco de diseño",
 body: "Encoder incremental en el lado del motor: la reductora multiplica su resolución efectiva sobre la articulación por G.",
 bodySize: 11.5,
 });
 card(s, 6.85, 5.3, 5.75, 1.35, {
 title: "Clasificación robótica (Corke)",
 body: "Propioceptivos: «el estado del propio robot» (hoy). Exteroceptivos: «el mundo respecto al robot» (S10: rango).",
 bodySize: 11.5,
 });
 s.addNotes("Dibujar en la pizarra las señales A y B en cuadratura y deducir con la clase cómo dan sentido y cuenta; calcular la resolución angular de un encoder de N líneas con decodificación x4. El LVDT es el sensor del caso piezoeléctrico de De Silva (p. 117).");
 footer(s, "Fraden, 2016, pp. 103, 288-293 y 309-310 · Corke, 2023, pp. 8-9");
}

{
 const s = contentSlide(p3, "Inercia: acelerómetros, giróscopos e IMU", "S9 · Navegación inercial");
 bullets(s, [
 { t: "Acelerómetro = masa sísmica + suspensión + amortiguamiento", h: true },
 { t: "Sistema de segundo orden con frecuencia natural ω0 y amortiguamiento ζ; detección capacitiva diferencial, piezorresistiva o piezoeléctrica." },
 { t: "Corke: «los acelerómetros miden la gravedad y el movimiento del cuerpo» a la vez, en reposo miden g: base de la estimación de inclinación." },
 { t: "Giróscopo de rotor (precesión, T = I·ω·Ω), hoy eclipsado por los ópticos RLG/FOG (efecto Sagnac) y los MEMS vibratorios (aceleración de Coriolis)." },
 { t: "INS: estima velocidad, orientación y posición integrando, sin entradas externas; IMU de 6/9 ejes y AHRS." },
 ], { w: 6.7, size: 13 });
 card(s, 7.6, 1.6, 5.0, 3.1, {
 title: "El enemigo: el bias",
 body: "Modelo de error de cada canal: la lectura vale s·x + b + ε. El bias b deriva con el tiempo y la temperatura; al integrar dos veces, el error de posición crece cuadráticamente.\n\nPregunta: ¿por qué el dron del laboratorio no navega solo con su IMU de 10 €?",
 bodySize: 12,
 });
 card(s, 7.6, 4.9, 5.0, 1.75, {
 title: "Fusión de sensores",
 body: "Giróscopo (deriva con t) + acelerómetro (referencia de g) + magnetómetro (rumbo, sensible a campos espurios): características complementarias → filtro de Kalman en B6.",
 fill: "E3F7EC", bodySize: 12,
 });
 s.addNotes("Escribir la ecuación de segundo orden del acelerómetro con ω0 y ζ (Fraden p. 329) y el concepto de masa de prueba sobre muelle (Corke p. 111). La advertencia de que miden gravedad y movimiento a la vez es la idea clave de la sesión. Cerrar con la pregunta provocadora del dron: deriva cuadrática al integrar dos veces un bias.");
 footer(s, "Fraden, 2016, pp. 327-344 · Corke, 2023, pp. 107-119");
}

// S10
sectionSlide(p3, "S10", "Fuerza, tacto y rango", "Galgas y puente de Wheatstone · táctiles · ultrasonidos, LiDAR y profundidad · selección",
 "0-10 recuperación: dos estudiantes a la pizarra (cuadratura del encoder y esquema del LVDT); 10-35 fuerza y galgas extensométricas con el puente de Wheatstone (Fraden pp. 215-216 y 355-356); 35-55 sensores táctiles (Fraden pp. 357-359) y discusión sobre manipulación diestra; 55-65 descanso; 65-90 sensores de rango: ultrasonidos, LiDAR, cámaras de profundidad (Fraden p. 314; Corke pp. 241-242); 90-115 ejercicio puntuable de selección de sensores en parejas (tres casos); 115-120 cierre y lectura previa de S11 (Corke p. 334).", { f: "fotos/b6_estereo3.jpg", cap: "Par estéreo: profundidad por triangulación", credito: "Foto: T. Cognard CC BY-SA 3.0 · Wikimedia Commons" });

{
 const s = contentSlide(p3, "Fuerza y tacto", "S10 · El sentido del contacto");
 card(s, 0.7, 1.7, 5.9, 3.4, {
 title: "Galgas extensométricas",
 body: "Sensor elástico resistivo: la resistencia es función de la deformación (efecto piezorresistivo). Factor de galga dR/R = Se·ε, con Se ≈ 2 en metales (constantán) y hasta ±150 en silicio (con fuerte sensibilidad térmica).\n\nPuente de Wheatstone: la configuración de 4 galgas activas compensa la temperatura y cuadruplica la sensibilidad.",
 num: "1", bodySize: 12,
 });
 card(s, 6.85, 1.7, 5.75, 3.4, {
 title: "Sensores táctiles",
 body: "Tres subgrupos: de contacto (binarios), espaciales (distribución de presión en un área) y de deslizamiento.\n\nRequisitos industriales orientativos: punto de contacto de 1-2 mm², sensibilidad 0,4-10 N, ancho de banda ≥ 100 Hz, histéresis baja; matrices de 10-20 puntos por lado. Construcciones: membrana con espaciador y películas PVDF en modo activo.",
 num: "2", bodySize: 12,
 });
 card(s, 0.7, 5.35, 11.9, 1.3, {
 title: "En robots",
 body: "Célula de carga = elemento elástico + galgas. Los robots con control de par montan sensores de par en las articulaciones o una muñeca de fuerza-par en el efector (Corke, p. 364). Discusión: ¿por qué la manipulación diestra sigue limitada por el tacto?",
 fill: "E3F7EC", bodySize: 12,
 });
 s.addNotes("Escribir el puente de Wheatstone, su condición de equilibrio y la salida desequilibrada; razonar sobre las derivadas de la ec. 5.39 por qué 4 galgas activas compensan temperatura. De los cinco métodos de medir fuerza de Fraden, el dominante es medir la deformación de un elemento elástico (p. 355). Conectar la discusión táctil con los grippers del laboratorio y los humanoides de B2.");
 footer(s, "Fraden, 2016, pp. 215-216 y 355-359 · Corke, 2023, p. 364");
}

{
 const s = contentSlide(p3, "Rango y selección de sensores", "S10 · Exteroceptivos + ejercicio");
 const rng = [
 ["Ultrasonidos", "Tiempo de vuelo acústico: L = v·t·cosΘ/2; Doppler para velocidad. Baratos; limitados por la velocidad del sonido y el ancho del haz."],
 ["LiDAR", "Pulsos láser IR y tiempo de vuelo: hasta 100 m con exactitud centimétrica; 1D, 2D (sección polar) y 3D (abanico rotatorio, 0,25° y 40 barridos/s). Métrico y funciona a oscuras; peor a pleno sol, sin color, con piezas móviles."],
 ["Cámaras de profundidad", "Luz estructurada y tiempo de vuelo (RealSense/Kinect): imagen + distancia por píxel; baratas y ricas en textura, menos precisas en exteriores."],
 ];
 rng.forEach((c, i) => card(s, 0.7 + i * 4.05, 1.7, 3.8, 2.6, { title: c[0], body: c[1], num: String(i + 1), bodySize: 11, titleSize: 13.5 }));
 const met = ["Magnitud y span", "Resolución y ancho de banda", "Muestreo por Nyquist", "Entorno y coste", "Decisión tipo MDQ"];
 met.forEach((t, i) => {
 card(s, 0.7 + i * 2.5, 4.6, 2.25, 1.15, { title: "", body: t, fill: i % 2 ? BG_LT : "E3F7EC", bodySize: 11.5 });
 if (i < 4) arrowR(s, 2.92 + i * 2.5, 4.95, 15);
 });
 card(s, 0.7, 6.0, 11.9, 0.85, {
 title: "",
 body: "Ejercicio puntuable en parejas, (a) fuerza de agarre de una pinza (0-50 N, 100 Hz); (b) navegación de un AMR de interior; (c) vibración de un husillo a 8 kHz. Trampas del caso (c): derivar posición (Fraden, p. 327) o muestrear a 10 kHz (aliasing).",
 fill: BG_LT, bodySize: 11,
 });
 s.addNotes("Principio activo general de los sensores de rango: emitir energía y medir la reflexión. Metodología obligatoria del ejercicio: tabla de especificaciones (Fraden p. 8), lista de preguntas de selección (p. 332), Nyquist (De Silva p. 152) y jerarquía de decisión con el espíritu del MDQ. Puesta en común con defensa oral de una pareja por caso.");
 footer(s, "Fraden, 2016, pp. 8, 314 y 332 · Corke, 2023, pp. 241-242 · De Silva et al., 2016, p. 152");
}

// S11
sectionSlide(p3, "S11", "Actuadores eléctricos", "Motor DC y back-EMF · BLDC · paso a paso · servoaccionamientos y SEA",
 "0-5 recuperación de S10 (¿qué puente para una célula de carga?) y panorama: «la mayoría de los robots actuales se accionan mediante motores eléctricos rotativos» (Corke p. 334); 5-25 modelo del motor DC y fuerza contraelectromotriz, con la curva par-velocidad deducida en pizarra (De Silva p. 91; Corke pp. 335-346); 25-40 BLDC y paso a paso con criterio rápido de elección; 40-55 servoaccionamientos: lazo anidado, feedforward, control de par y SEA (Corke pp. 342-370); 55-60 cierre y encargo: gearbox (Corke p. 339) e inercia reflejada.", { f: "fotos/b3_stepper.jpg", cap: "NEMA 17: el paso a paso de referencia", credito: "Foto: oomlout CC BY-SA 2.0 · Wikimedia Commons" });

slideFotos(p3, "Tres curvas que hay que saber leer", "S8–S11 · Figuras del bloque", [
 { f: "figs/b3_histeresis.png", x: 0.7, y: 1.5, w: 5.85, h: 2.6, cap: "Histéresis: la salida depende del camino (S8)" },
 { f: "figs/b3_cuadratura.png", x: 6.75, y: 1.5, w: 5.85, h: 2.6, cap: "Cuadratura A/B: cuenta y sentido de giro (S9)" },
 { f: "figs/b3_par_velocidad.png", x: 3.6, y: 4.42, w: 6.1, h: 2.45, cap: "Curva par-velocidad y punto de operación (S11)" },
], "Figuras propias del curso (generadas con los cuadernos de Colab)",
"Las tres curvas del bloque en una diapositiva: recuperarla en el repaso previo al cuestionario B3.");

{
 const s = contentSlide(p3, "El motor DC y la fuerza contraelectromotriz", "S11 · El actuador de referencia");
 bullets(s, [
 { t: "Modelo completo (De Silva, p. 91): mecánica, malla eléctrica y acoplo par-corriente", h: true },
 { t: "Back-EMF: un motor que gira actúa como generador, Vb = Km·ω se opone a la corriente; cuando iguala la tensión del amplificador el par cae a cero, cota de velocidad y amortiguamiento aparente (Corke, p. 346)." },
 { t: "De ahí sale la curva par-velocidad lineal a tensión constante: par máximo a rotor parado, velocidad máxima sin carga. Fricción real: viscosa B·ω + Coulomb, perturbación del control (B5)." },
 ], { w: 7.3, size: 12.5, h: 2.9 });
 eqImg(s, "motor3", 1.15, 4.55, 5.0, 1.62);
 s.addText("Simplificación útil: la constante de tiempo eléctrica « la mecánica → se desprecia el transitorio eléctrico.", { x: 0.95, y: 6.4, w: 7.0, h: 0.4, fontFace: "Calibri", fontSize: 11.5, color: GREY, margin: 0 });
 const chain = [["Amplificador de potencia", "tensión / corriente"], ["Motor DC", "τ = Kt·i"], ["Encoder", "posición y velocidad"], ["Inercia + fricción", "la carga mecánica"]];
 chain.forEach((c, i) => {
 card(s, 8.3, 1.6 + i * 1.32, 4.3, 1.0, { title: "", body: c[0] + " · " + c[1], fill: i % 2 ? BG_LT : "E3F7EC", bodySize: 11.5 });
 if (i < 3) s.addText("↓", { x: 10.25, y: 2.53 + i * 1.32, w: 0.4, h: 0.4, fontSize: 15, bold: true, color: GREEN_DK, align: "center", margin: 0 });
 });
 s.addNotes("Dibujar la cadena del accionamiento (Corke p. 335) y deducir en pizarra la curva par-velocidad a partir de las dos ecuaciones. Pregunta de control: ¿por qué la back-EMF limita la velocidad máxima? Este modelo es el punto de partida del modelado de B5 (S20).");
 footer(s, "De Silva et al., 2016, p. 91 · Corke, 2023, pp. 335-346");
}

{
 const s = contentSlide(p3, "BLDC, paso a paso y servoaccionamientos", "S11 · Mapa de accionamientos");
 const g = [
 ["DC de escobillas", "Barato y simple; escobillas con desgaste y chispas. Robots pequeños y de hobby."],
 ["BLDC", "Imanes al rotor, bobinados al estátor; conmutación electrónica con sensores Hall o sensorless. Sin desgaste, mejor disipación, más par por volumen: el estándar de los industriales."],
 ["Paso a paso", "Avance en pasos discretos: posiciona en lazo abierto contando pasos; pierde pasos bajo sobrecarga; microstepping para suavizar."],
 ["Servoaccionamiento", "Lazo anidado: velocidad dentro, posición fuera; feedforward de velocidad para reducir el error de seguimiento. El control de par exige medición de par integrada."],
 ];
 g.forEach((c, i) => {
 const col = i % 2, row = Math.floor(i / 2);
 card(s, 0.7 + col * 6.1, 1.7 + row * 2.3, 5.85, 2.1, { title: c[0], body: c[1], num: String(i + 1), bodySize: 11.5, titleSize: 13.5 });
 });
 card(s, 0.7, 6.2, 11.9, 0.75, {
 title: "",
 body: "Actuador serie-elástico (SEA): motor y carga unidos por un muelle → control de fuerza y operación segura junto a personas (Corke, pp. 367-370), el hardware coherente con los cobots de S7.",
 fill: "E3F7EC", bodySize: 11.5,
 });
 s.addNotes("Conectar los sensores Hall de S9 con la conmutación del BLDC. Historia del término servo: el steering engine de 1866 (Corke p. 335). Criterio rápido de elección DC/BLDC/paso a paso por coste, mantenimiento y necesidad de realimentación: construir la tabla en la pizarra con la clase.");
 footer(s, "Corke, 2023, pp. 334-346 y 364-370 · Fraden, 2016, p. 293");
}

// S12
sectionSlide(p3, "S12", "Hidráulica, neumática y reductoras", "Mapa de actuación · inercia reflejada · selección motor-reductora · cuestionario B3",
 "0-5 recuperación de S11 (back-EMF y velocidad máxima); 5-20 actuación hidráulica y neumática con ventajas e inconvenientes a dos columnas (Corke p. 334); 20-40 transmisiones e inercia reflejada con la tabla 9.1 de Corke (pp. 339-341); 40-45 ejercicio guiado de selección motor-reductora en la pizarra; 45-60 cuestionario B3 en Moodle (15 min) y cierre del bloque: en B4 sensores y actuadores se integran en el robot completo.", { f: "fotos/b3_harmonic.jpg", cap: "Harmonic drive: reducción alta sin holgura", credito: "Foto: wdwd CC BY-SA 4.0 · Wikimedia Commons" });


slideFotos(p3, "Actuadores y transmisiones, de cerca", "S11–S12 · Hardware", [
 { f: "fotos/b3_stepper.jpg", x: 0.7, y: 1.5, w: 3.85, h: 4.9, cap: "Paso a paso NEMA 17: posicionar en lazo abierto contando pasos" },
 { f: "fotos/b3_harmonic.jpg", x: 4.72, y: 1.5, w: 3.85, h: 4.9, cap: "Harmonic drive: la reductora de las articulaciones robóticas" },
 { f: "fotos/b2_cobot3.png", x: 8.74, y: 1.5, w: 3.9, h: 4.9, cap: "UR16e: seis servoaccionamientos con par medido en cada eje" },
], "Fotos: oomlout CC BY-SA 2.0 · wdwd CC BY-SA 4.0 · Auledas CC BY-SA 4.0 · Wikimedia Commons",
"Pasar de la foto al concepto: el paso a paso pierde pasos bajo sobrecarga (lazo abierto), el harmonic drive explica la inercia reflejada dividida por G² y el cobot integra motor, reductora, encoder y medición de par en cada eje.");

{
 const s = contentSlide(p3, "Hidráulica y neumática", "S12 · Más allá del motor eléctrico");
 card(s, 0.7, 1.7, 5.9, 3.3, {
 title: "Hidráulica",
 body: "«Para fuerzas muy altas es común la actuación electrohidráulica: hidráulica con válvulas operadas eléctricamente» (Corke).\n\nCircuito: grupo de presión (bomba + depósito + acumulador) → servoválvulas → cilindro o motor.\n\nA favor: densidad de fuerza altísima, mantiene carga. En contra: coste, fugas, ruido, rendimiento.",
 bodySize: 12,
 });
 card(s, 6.85, 1.7, 5.75, 3.3, {
 title: "Neumática",
 body: "«Posible aunque poco común; con la ventaja de generar movimiento siendo naturalmente flexible (compliant)» (Corke).\n\nLimpia, barata y rápida, pero de baja rigidez por la compresibilidad del aire.\n\nDominio típico: pinzas y clasificadores de alta cadencia.",
 bodySize: 12,
 });
 card(s, 0.7, 5.25, 11.9, 1.4, {
 title: "Dónde encaja cada tecnología",
 body: "Prensas y maquinaria pesada → hidráulica · pinzas y alta cadencia → neumática · casi todo lo demás → eléctrico. La selección del tipo de actuador es la capa superior de la jerarquía MDQ (De Silva, p. 8).",
 fill: "E3F7EC", bodySize: 12,
 });
 s.addNotes("Construir la comparativa a dos columnas con aportaciones de la clase antes de mostrarla. Anclar con ejemplos: la excavadora y la pinza de fin de brazo. Recordar que el MDQ de B1 formaliza esta decisión.");
 footer(s, "Corke, 2023, p. 334 · De Silva et al., 2016, p. 8");
}

{
 const s = contentSlide(p3, "Reductora, inercia reflejada y selección", "S12 · Cambiar velocidad por par");
 card(s, 0.7, 1.7, 5.9, 2.9, {
 title: "Reducción G:1 (Corke, tabla 9.1)",
 body: "Par ×G · velocidad ÷G · inercia de carga vista desde el motor ÷G² · par de perturbación ÷G.\n\nInercia total en el eje del motor: J' = Jm + Jl/G². Con G grande el motor «no siente» la carga, G = 107,8 en el hombro del PUMA 560.",
 bodySize: 12,
 });
 card(s, 0.7, 4.8, 5.9, 1.85, {
 title: "El precio de la reductora",
 body: "Coste, peso, fricción, holgura (backlash), ruido y rizado de par; elasticidad de la transmisión (harmonic drive, correas). Alternativa: direct-drive.",
 bodySize: 12,
 });
 const steps = [
 ["1", "Par de carga pico y RMS en el ciclo (perfil trapezoidal)"],
 ["2", "Referir al motor con un G de tanteo (tabla 9.1)"],
 ["3", "Comprobar velocidad del motor frente a ω·G y la cota de la back-EMF"],
 ["4", "Relación de inercias Jl/(G²·Jm) ≈ 1: el G óptimo iguala inercias"],
 ];
 steps.forEach((c, i) => {
 card(s, 6.85, 1.7 + i * 1.05, 5.75, 0.9, { title: "", body: "Paso " + c[0] + ", " + c[1], fill: i % 2 ? BG_LT : "E3F7EC", bodySize: 11 });
 });
 card(s, 6.85, 5.95, 5.75, 0.7, {
 title: "",
 body: "Cuestionario B3 (15 min, Moodle): características, cuadratura, bias de IMU, factor de galga, LiDAR, back-EMF, inercia reflejada.",
 fill: "E3F7EC", bodySize: 10.5,
 });
 s.addNotes("Motivación de Corke: «los motores eléctricos son compactos y eficientes y pueden girar muy rápido, pero producen un par muy bajo». Ejercicio guiado con números en la pizarra; comentar los márgenes de catálogo (par RMS < nominal, pico < máximo, factor de servicio). Cuestionario B3 en Moodle en los últimos 15 minutos; cerrar el bloque enlazando con B4.");
 footer(s, "Corke, 2023, pp. 339-346");
}

p3.writeFile({ fileName: "IQS_B3_Sensores_Actuadores.pptx" }).then(() => console.log("OK deck B3"));

/* ==================== DECK B4 ==================== */
const p4 = newDeck();

titleSlide(p4, {
 curso: "82514 · MECATRÓNICA Y ROBÓTICA",
 bloque: "Bloque 4",
 titulo: "Cinemática y estática\nde manipuladores",
 sub: "Sesiones S13–S19 · 10 horas",
 fechas: "9, 14, 15, 16, 21, 22 y 23 de octubre de 2026 · IQS Universitat Ramon Llull",
});

{
 const s = contentSlide(p4, "Hoja de ruta del bloque", "Bloque 4");
 const rows = [
 ["S13 · vie 9 oct · 2 h", "Pose: marcos, rotaciones y transformaciones homogéneas + taller spatialmath"],
 ["S14 · mié 14 oct · 1 h", "Cinemática directa: ETS, Denavit-Hartenberg y producto de exponenciales"],
 ["S15 · jue 15 oct · 1 h", "Taller: FK de un 6R con la Robotics Toolbox y el ABB del laboratorio"],
 ["S16 · vie 16 oct · 2 h", "Cinemática inversa: solución analítica, ocho soluciones y métodos numéricos"],
 ["S17 · mié 21 oct · 1 h", "Jacobiano y cinemática diferencial; control de velocidad resuelta"],
 ["S18 · jue 22 oct · 1 h", "Singularidades y elipsoide de manipulabilidad"],
 ["S19 · vie 23 oct · 2 h", "Estática τ = Jᵀ·F, trayectorias y repaso · cuestionario B4"],
 ];
 rows.forEach((r, i) => agendaRow(s, 1.55 + i * 0.78, 0.68, String(i + 1), r[0], r[1], 12.5, 11.5));
 s.addNotes("Presentar el arco del bloque: pose → FK → IK → jacobiano → singularidades → estática y trayectorias. El jacobiano es el objeto más reutilizado: conecta FK diferencial, IK numérica, singularidades y estática. Cuestionario B4 en los últimos 10 minutos de S19.");
 footer(s, "82514 Mecatrónica y Robótica · B4 · IQS");
}

// S13
sectionSlide(p4, "S13", "Posición y orientación", "Marcos y pose relativa · SO(3) · Euler, eje-ángulo y cuaterniones · SE(3) · taller",
 "0-10 mapa del bloque y pose relativa: «cualquier pose es siempre una pose relativa» (Corke p. 26), notación de subíndices origen-destino; 10-35 matrices de rotación 2D y 3D, Rᵀ·R = I y det R = +1 (Lynch y Park pp. 69-71), no conmutatividad con el libro físico; 35-60 ángulos de Euler y RPY, bloqueo de cardán y Apolo 13, eje-ángulo y cuaterniones (Corke pp. 48-59); 60-70 descanso; 70-85 transformaciones homogéneas SE(2)/SE(3); 85-115 taller con spatialmath-python; 115-120 cierre: matrices para operar, ángulos para comunicar, cuaterniones para interpolar.", { f: "fotos/b4_abb3.jpg", cap: "ASEA/ABB: medio siglo de brazos de 6 ejes", credito: "Foto: Dependability CC BY-SA 4.0 · Wikimedia Commons" });

slideFotos(p4, "Del PUMA al laboratorio", "S13–S15 · Manipuladores reales", [
 { f: "fotos/b4_puma.jpg", x: 0.7, y: 1.5, w: 5.85, h: 5.0, cap: "Unimate PUMA 500: el arquetipo (Deutsches Museum)" },
 { f: "fotos/b4_kuka.jpg", x: 6.75, y: 1.5, w: 5.85, h: 5.0, cap: "Brazos industriales de 6 ejes: la configuración del laboratorio" },
], "Fotos: Theoprakt CC BY-SA 3.0 · Mixabest CC BY-SA 3.0 · Wikimedia Commons",
"El PUMA conecta con la historia de S3 (Unimation) y con el modelo Puma560 del taller S15; los 6R naranjas son la misma configuración que los Mitsubishi y ABB del aula-taller.");

{
 const s = contentSlide(p4, "Rotaciones: el grupo SO(3)", "S13 · La orientación como matriz");
 bullets(s, [
 { t: "«Cualquier pose es siempre una pose relativa» (Corke, p. 26)", h: true },
 { r: [{ t: "A cada cuerpo se une rígidamente un marco dextrógiro; T" }, { t: "AB", sub: true }, { t: " es la pose de {B} respecto de {A}; el marco de referencia es {0} o {W}." }] },
 { t: "Matriz de rotación: columnas = ejes del marco girado; Rᵀ·R = I y det R = +1 definen SO(3) (Lynch y Park, p. 70)." },
 { t: "La inversa es gratis: R⁻¹ = Rᵀ (Proposición 3.3)." },
 { t: "Tres usos: representar una orientación, cambiar el marco de un vector y rotar un vector (Lynch y Park, p. 71)." },
 { t: "9 números − 6 ligaduras = 3 grados de libertad → motivan las parametrizaciones de 3 parámetros." },
 ], { w: 6.9, size: 13 });
 card(s, 7.9, 1.6, 4.7, 2.6, {
 title: "Demostración en el aula",
 body: "La composición 3D es producto de matrices y no conmuta: girar un libro físico 90° en Z y luego en Y no acaba igual que en el orden inverso. En 2D sí conmuta.",
 bodySize: 12.5,
 });
 card(s, 7.9, 4.4, 4.7, 2.25, {
 title: "Leer los subíndices en cadena",
 body: [{ text: "T" }, { text: "AC", options: { subscript: true } }, { text: " = T" }, { text: "AB", options: { subscript: true } }, { text: " · T" }, { text: "BC", options: { subscript: true } }, { text: ": el subíndice interior «se cancela». Regla mecánica que evita el 80 % de los errores de orden del taller." }],
 fill: "E3F7EC", bodySize: 12.5,
 });
 s.addNotes("Derivar R(θ) 2x2 en pizarra proyectando los ejes rotados. Insistir en que las condiciones de ortonormalidad excluyen los marcos levógiros. La cuenta 9 − 6 = 3 motiva el siguiente segmento (tres ángulos).");
 footer(s, "Corke, 2023, pp. 26-48 · Lynch y Park, 2017, pp. 69-71");
}

{
 const s = contentSlide(p4, "Tres maneras de escribir una orientación", "S13 · Parametrizaciones");
 const cols = [
 ["Tres ángulos", "Euler ZYZ: R = Rz(φ)·Ry(θ)·Rz(ψ); RPY (Cardan) con secuencia ZYX en vehículos. 12 secuencias posibles. Problema estructural: bloqueo de cardán cuando dos ejes se alinean (pitch = ±90°), la anécdota del Apolo 13."],
 ["Eje-ángulo", "Girar θ alrededor de un eje unitario ŵ: coordenadas exponenciales, con [ŵ] la matriz antisimétrica de ŵ. Fórmula de Rodrigues:"],
 ["Cuaterniones unitarios", "4 números y una ligadura; parte vectorial ŵ·sin(θ/2). Componen barato y no tienen singularidad: el estándar en robótica, visión, gráficos y navegación."],
 ];
 cols.forEach((c, i) => card(s, 0.7 + i * 4.05, 1.7, 3.8, 3.6, { title: c[0], body: c[1], num: String(i + 1), bodySize: 11.5, titleSize: 14 }));
 eqImg(s, "rodrigues", 4.95, 4.62, 3.4, 0.5);
 card(s, 0.7, 5.55, 11.9, 1.1, {
 title: "",
 body: "Regla del curso: matrices para operar, ángulos para comunicar con humanos, cuaterniones para interpolar y almacenar. «Todas las representaciones de tres ángulos sufren el bloqueo de cardán» (Corke, p. 53).",
 fill: "E3F7EC", bodySize: 12.5,
 });
 s.addNotes("Explorar el bloqueo de cardán con la demo interactiva tripleangledemo del taller. Señalar la ambigüedad de convenciones RPY (ZYX frente a XYZ) como fuente clásica de errores al integrar hardware. Conectar Rodrigues con el producto de exponenciales de S14.");
 footer(s, "Corke, 2023, pp. 48-59 · Lynch y Park, 2017, pp. 77-84");
}

{
 const s = contentSlide(p4, "SE(3) y el taller de spatialmath", "S13 · Pose completa = rotación + traslación");
 bullets(s, [
 { t: "La transformación homogénea", h: true },
 { t: "Matriz 4x4 del grupo SE(3): «muy comúnmente usada en robótica, gráficos y visión» (Corke, p. 62). En 2D: SE(2), matrices 3x3 con p homogéneo." },
 { t: "Composición por producto; inversa sin resolver sistemas, y verificación numérica obligatoria en el taller: T·T⁻¹ = I." },
 ], { w: 6.0, size: 13, h: 2.3 });
 eqImg(s, "se3_T", 0.85, 4.0, 2.35, 1.0);
 eqImg(s, "t_comp", 3.55, 4.28, 2.9, 0.5);
 eqImg(s, "t_inv", 1.35, 5.25, 4.3, 1.3);
 card(s, 7.0, 1.6, 5.6, 3.5, {
 title: "Taller con spatialmath-python · cuaderno 82514_S13",
 body: "R = rot2(0.3); trplot2(R)\nTA = transl2(1, 2) @ trot2(30, unit=\"deg\")\nR = eul2r(0.1, 0.2, 0.3); gamma = tr2eul(R)\nT0 = SE3.Trans([0.4, 0.2, 0]) * SE3.RPY(0, 0, 3)\naTb = SE3.Tx(-2) * SE3.Rz(-pi/2) * SE3.Rx(pi/2)",
 bodySize: 12.5,
 });
 card(s, 7.0, 5.3, 5.6, 1.35, {
 title: "Ejercicio guiado",
 body: "Cadena mundo → mesa → pieza → cámara: calcular la pose de la pieza componiendo e invirtiendo transformaciones. Guiado paso a paso, con soluciones, en el cuaderno 82514_S13_Pose_Rotaciones.",
 fill: "E3F7EC", bodySize: 12,
 });
 s.addNotes("El taller reproduce las sesiones del libro de Corke (pp. 34-38, 49-52, 90 y 105), de modo que los estudiantes pueden continuar en casa con el texto. Comprobar entornos al empezar: spatialmath-python y matplotlib instalados. Encargo de lectura para S14: Corke pp. 255-260.");
 footer(s, "Corke, 2023, pp. 37-63, 90 y 105 · Lynch y Park, 2017, p. 89");
}

// S14

{
 const s = contentSlide(p4, "Ejemplo resuelto: componer poses en 2D", "S13 · Ejemplo en clase");
 card(s, 0.7, 1.58, 11.9, 0.92, { title: "", body: "Enunciado. La mesa {M} está en el mundo {W} en (1,0, 0,5) m, girada 90°. La pieza {P} está sobre la mesa en (0,2, 0,1) m, girada −30°. ¿Cuál es la pose de la pieza en el mundo?", fill: "E3F7EC", bodySize: 12.5 });
 bullets(s, [
  { t: "Paso 1. Plantear la cadena: mundo → mesa → pieza. Los subíndices interiores se cancelan: la pose buscada compone las dos conocidas." },
  { t: "Paso 2. Girar y sumar: el giro de 90° convierte (0,2, 0,1) en (−0,1, 0,2); sumado a la posición de la mesa da la posición de la pieza. Las orientaciones se suman: 90° − 30° = 60°." },
 ], { y: 2.75, w: 11.9, h: 1.7, size: 13 });
 eqImg(s, "ej_comp", 1.1, 4.55, 11.1, 0.85);
 card(s, 0.7, 5.75, 11.9, 0.95, { title: "", body: "Comprobación en el cuaderno 82514_S13: SE2(1.0, 0.5, 90, unit='deg') * SE2(0.2, 0.1, -30, unit='deg'). El resultado imprime (0,9, 0,7) y 60°.", fill: BG_LT, bodySize: 12 });
 footer(s, "Ejemplo guiado en el cuaderno 82514_S13_Pose_Rotaciones");
}

sectionSlide(p4, "S14", "Cinemática directa", "El problema FK · ETS · Denavit-Hartenberg · producto de exponenciales",
 "0-5 recuperación de S13 (inversa de T; bloqueo de cardán); 5-20 el problema cinemático directo y el 2R plano en pizarra; 20-40 las tres convenciones: ETS (Corke p. 256), DH (p. 274) y PoE (Lynch y Park p. 142), derivando la lógica del PoE sobre el 2R; 40-55 ejercicio por parejas: mismo robot, tres descripciones, verificando t = (1.21, 1.44) y 70° en q = (30°, 40°); 55-60 cierre y anuncio del taller S15 con portátiles.");

{
 const s = contentSlide(p4, "Tres convenciones para la misma FK", "S14 · De las articulaciones a la pose");
 card(s, 0.7, 1.6, 11.9, 0.8, {
 title: "",
 body: "FK: «el cálculo de la posición y orientación del marco del efector a partir de sus coordenadas articulares» (Lynch y Park, p. 137). Siempre existe y es única, el problema difícil será el inverso (S16). Para el 2R plano:",
 fill: "E3F7EC", bodySize: 11.5,
 });
 eqImg(s, "fk2r", 2.2, 2.52, 8.9, 0.46);
 const cols = [
 ["ETS (Corke)", "La pose como secuencia de transformaciones elementales que se lee directamente de la geometría: E = rz(q0) ⊕ tx(a1). El 6R general acaba en una muñeca ZYZ. Ideal para entender."],
 ["Denavit-Hartenberg", "4 parámetros por eslabón (θⱼ, dⱼ, aⱼ, αⱼ) en una tabla compacta: «la manera de compartir modelos desde los años 60». Cada fila = rz ⊕ tz ⊕ tx ⊕ rx. Ojo con la numeración 0/1."],
 ["PoE (Lynch y Park)", [{ text: "M = pose del efector en configuración cero; S" }, { text: "i", options: { subscript: true } }, { text: " = eje helicoidal de la articulación i. «No hay que definir marcos de eslabón». La base del análisis de velocidad (S17):" }]],
 ];
 cols.forEach((c, i) => card(s, 0.7 + i * 4.05, 3.1, 3.8, 2.72, { title: c[0], body: c[1], num: String(i + 1), bodySize: 11, titleSize: 13.5 }));
 eqImg(s, "poe", 8.95, 5.28, 3.35, 0.42);
 card(s, 0.7, 6.02, 11.9, 0.8, {
 title: "",
 body: "Ejercicio por parejas: para el 2R, escribir (i) la ETS, (ii) la tabla DH y (iii) M, S1 y S2 del PoE; comprobar que las tres dan la misma T(q) en q = (30°, 40°): t = (1.21, 1.44), orientación 70° (Corke, p. 258).",
 fill: BG_LT, bodySize: 11.5,
 });
 s.addNotes("Derivar la lógica del PoE en pizarra sobre el 2R: cada articulación aplica un giro exponencial al resto de la cadena desde la configuración de casa; conectar con Rodrigues (S13). Discusión de cierre: ETS para leer geometría, DH para intercambiar modelos, PoE para el análisis de velocidad; la relación formal PoE-DH está en el apéndice C de Lynch y Park.");
 footer(s, "Corke, 2023, pp. 255-275 · Lynch y Park, 2017, pp. 137-142");
}

// S15

{
 const s = contentSlide(p4, "Ejemplo resuelto: FK del 2R con números", "S14 · Ejemplo en clase");
 card(s, 0.7, 1.58, 11.9, 0.92, { title: "", body: "Enunciado. Un 2R plano tiene a₁ = 0,35 m y a₂ = 0,2 m. Para q = (30°, 60°): posición y orientación del efector, tabla DH y espacio de trabajo.", fill: "E3F7EC", bodySize: 12.5 });
 bullets(s, [
  { t: "Paso 1. Posición por suma de proyecciones (el segundo eslabón sale con el ángulo acumulado q₁ + q₂ = 90°):" },
 ], { y: 2.72, w: 11.9, h: 0.6, size: 13 });
 eqImg(s, "ej_fk", 1.0, 3.35, 11.3, 0.5);
 bullets(s, [
  { t: "Paso 2. Orientación: φ = q₁ + q₂ = 90°. La pose completa del efector es (0,303, 0,375, 90°)." },
  { t: "Paso 3. Tabla DH (dos filas): θ₁ = q₁, d = 0, a = 0,35, α = 0 · θ₂ = q₂, d = 0, a = 0,2, α = 0." },
  { t: "Paso 4. Espacio de trabajo: anillo entre a₁ − a₂ = 0,15 m y a₁ + a₂ = 0,55 m. Un punto a 0,6 m del origen es inalcanzable; uno a 0,1 m también, por el hueco interior." },
 ], { y: 4.15, w: 11.9, h: 2.4, size: 13 });
 footer(s, "Misma estructura que la parte C del parcial 1, con otros números · cuaderno 82514_S14");
}

sectionSlide(p4, "S15", "Taller: FK de un 6R en Python", "Robotics Toolbox · PUMA 560 e IRB140 · validación con el ABB del laboratorio",
 "0-5 objetivo y puesta en marcha (import roboticstoolbox y spatialmath); 5-20 modelos incluidos y configuraciones con nombre (qr, qz) con fkine y printline (Corke pp. 265-278); 20-40 ejercicios guiados: verificar productos de la cadena, exploración con teach, 6R genérico como ETS con muñeca ZYZ; 40-55 comparación con el ABB del laboratorio: leer pose y articulares del controlador y discutir discrepancias (herramienta, base, convención de ángulos); 55-60 cierre y mini-reto con teach que motiva la IK de S16.");

{
 const s = contentSlide(p4, "Del modelo de libro al robot del laboratorio", "S15 · Taller Robotics Toolbox");
 bullets(s, [
 { t: "Las cuatro llamadas del taller", h: true },
 { t: "puma = models.DH.Puma560(), el arquetipo: «el primer robot industrial moderno» (Corke, p. 261); irb140 = models.DH.IRB140()." },
 { t: "Configuraciones con nombre: qr y qz son propiedades del robot; pueden añadirse otras." },
 { t: "irb140.fkine(irb140.qr).printline(\"rpy/xyz\") → t = (0.005, 0, 0.332), rpy = (0, −90, −90)°." },
 { t: "teach: deslizadores por articulación con la pose del efector en vivo, localizar la muñeca esférica." },
 { t: "Trampa clásica DH: el «efector» del modelo es el centro de la muñeca, dentro del robot; la brida real exige añadir la transformación de herramienta (Corke, p. 267)." },
 ], { w: 6.9, size: 12.5 });
 card(s, 7.9, 1.6, 4.7, 3.1, {
 title: "Contra el ABB del laboratorio",
 body: "Leer en el controlador la pose de la brida y las coordenadas articulares e introducirlas en el modelo de la toolbox. Discutir las discrepancias: herramienta montada, base desplazada y convención de ángulos del controlador.",
 bodySize: 12.5,
 });
 card(s, 7.9, 4.9, 4.7, 1.75, {
 title: "Mini-reto para casa",
 body: "Usando solo teach, tocar un punto objetivo con el efector del puma. Anotar cuántos intentos requiere, la motivación directa de la IK de S16.",
 fill: "E3F7EC", bodySize: 12.5,
 });
 s.addNotes("Comprobar los entornos en los primeros minutos. Con el modelo en pantalla y el robot a la vista, identificar cintura, hombro, codo y muñeca. Las normas de seguridad del aula-taller establecidas en S7 siguen vigentes en todas las sesiones con robot.");
 footer(s, "Corke, 2023, pp. 261-281");
}

// S16
sectionSlide(p4, "S16", "Cinemática inversa", "2R analítico · desacoplo con muñeca esférica · ocho soluciones · Newton-Raphson · taller",
 "0-10 el problema inverso y su estructura (puede no haber solución, haber varias o infinitas); 10-35 solución analítica del 2R en pizarra con ley de cosenos y atan2 (Lynch y Park p. 220); 35-60 el 6R con muñeca esférica: desacoplo posición/orientación y 4×2 = 8 soluciones (Corke p. 282; Lynch y Park pp. 221-225); 60-70 descanso; 70-85 métodos numéricos Newton-Raphson con el jacobiano (Lynch y Park pp. 226-232); 85-115 taller de IK con la toolbox (ikine_a con banderas, ikine_LM con semillas); 115-120 cierre: analítica cuando la geometría lo permite, numérica en el resto.");

{
 const s = contentSlide(p4, "IK analítica: del 2R a las ocho soluciones", "S16 · Forma cerrada");
 bullets(s, [
 { t: "2R plano en pizarra", h: true },
 { t: "Ley de cosenos para el codo, atan2 de dos argumentos para el hombro (conserva el cuadrante); dos ramas: codo arriba / codo abajo." },
 { t: "6R industrial: condición de forma cerrada = muñeca esférica (tres ejes que se cortan en un punto)." },
 { t: "Desacoplo: la posición del centro de muñeca depende solo de q1-q3; la orientación restante la resuelven q4-q6 (extraer Euler ZYX)." },
 { t: "Con offset de hombro: lefty/righty × codo arriba/abajo = 4 soluciones de posición; × muñeca volteada o no = 8 en total (Corke, p. 282)." },
 ], { w: 6.9, size: 13 });
 card(s, 7.9, 1.6, 4.7, 2.85, {
 title: "Casos degenerados",
 body: "Pose fuera de alcance → sin solución. Objetivo con px = py = 0 → infinitas soluciones de theta1. Y «por límites articulares y colisiones no las ocho soluciones son físicamente alcanzables».",
 bodySize: 12.5,
 });
 card(s, 7.9, 4.65, 4.7, 2.0, {
 title: "Regla de oficio",
 body: "Siempre atan2(y, x), nunca arcotangentes de cociente: la regla reaparece en todas las soluciones analíticas.",
 fill: "E3F7EC", bodySize: 12.5,
 });
 s.addNotes("Mostrar geométricamente las dos soluciones del 2R y su espacio de trabajo (fig. 6.1 de Lynch y Park). El desacoplo es el mismo truco que estructura el 6R con ETS de S14 (muñeca ZYZ). Anunciar al empezar el resultado central del día: ocho configuraciones para la misma pose.");
 footer(s, "Lynch y Park, 2017, pp. 220-225 · Corke, 2023, pp. 281-282");
}


{
 const s = contentSlide(p4, "Ejemplo resuelto: la IK y sus dos ramas", "S16 · Ejemplo en clase");
 card(s, 0.7, 1.58, 11.9, 0.8, { title: "", body: "Enunciado. El mismo 2R (a₁ = 0,35 m, a₂ = 0,2 m) debe alcanzar el punto P = (0,4, 0,2) m. Calcular las dos soluciones articulares.", fill: "E3F7EC", bodySize: 12.5 });
 bullets(s, [
  { t: "Paso 1. Ley de los cosenos para el codo (P está a 0,447 m del origen, dentro del anillo):" },
 ], { y: 2.55, w: 11.9, h: 0.55, size: 13 });
 eqImg(s, "ej_c2", 1.6, 3.12, 10.1, 0.78);
 bullets(s, [
  { t: "Paso 2. El hombro con atan2 (nunca la arcotangente del cociente: pierde el cuadrante):" },
 ], { y: 4.08, w: 11.9, h: 0.55, size: 13 });
 eqImg(s, "ej_q1", 1.6, 4.62, 9.4, 0.48);
 card(s, 0.7, 5.35, 5.9, 1.3, { title: "Codo abajo (q₂ = +74,5°)", body: "q₁ = 1,0°. La FK devuelve (0,4, 0,2): verificado.", bodySize: 12 });
 card(s, 6.85, 5.35, 5.75, 1.3, { title: "Codo arriba (q₂ = −74,5°)", body: "q₁ = 52,1°. La FK también devuelve (0,4, 0,2): las dos ramas son válidas.", bodySize: 12 });
 footer(s, "Misma estructura que la parte D del parcial 1, con otros números · cuaderno 82514_S16");
}

{
 const s = contentSlide(p4, "IK numérica y taller con la toolbox", "S16 · Cuando no hay forma cerrada");
 const steps = [
 ["Semilla q0", "elección inicial (o aleatoria)"],
 ["Error", "g(q) = xd − f(q)"],
 ["Paso de Newton", "linealizar con J y usar su pseudoinversa"],
 ["Parada", "tolerancia (100 μm en pocas iteraciones)"],
 ];
 steps.forEach((c, i) => {
 const x = 0.7 + i * 3.075;
 card(s, x, 1.7, 2.78, 1.7, { title: c[0], body: c[1], num: String(i + 1), bodySize: 11, titleSize: 13 });
 if (i < 3) arrowR(s, x + 2.76, 2.25, 16);
 });
 card(s, 0.7, 3.75, 5.9, 2.85, {
 title: "Analítica: ikine_a",
 body: "sol = puma.ikine_a(T) y verificar siempre con puma.fkine(sol.q). Explorar las 8 ramas con las banderas \"l\"/\"r\", \"u\"/\"d\", \"f\"/\"n\". Fallos con diagnóstico: ikine_a(SE3.Tx(3)) → success=False, «fuera de alcance»; con q4 = 0 los ejes 3 y 5 se alinean y solo queda determinada la suma q3 + q5.",
 bodySize: 11.5,
 });
 card(s, 6.85, 3.75, 5.75, 2.85, {
 title: "Numérica: ikine_LM",
 body: "sol = puma.ikine_LM(T, q0=...): converge a la rama que dicta la semilla; sin semilla, valores iniciales aleatorios. Puede fallar o saltar de rama cerca de singularidades.\n\nSíntesis por parejas: obtener las 8 soluciones para un punto de la mesa, descartar las no alcanzables y elegir razonadamente.",
 bodySize: 11.5,
 });
 s.addNotes("Mensaje final de la sesión: la IK industrial es analítica cuando la geometría lo permite (rápida, todas las ramas) y numérica en el resto; ambas exigen gestionar la multiplicidad desde la programación de la tarea. Encargo de lectura para S17: Corke pp. 310-315.");
 footer(s, "Lynch y Park, 2017, pp. 226-232 · Corke, 2023, pp. 282-283");
}

// S17
sectionSlide(p4, "S17", "Jacobiano y cinemática diferencial", "ẋ = J(q)·q̇ · columnas con significado · velocidad resuelta",
 "0-5 recuperación de S16 (ocho soluciones; dependencia de la semilla); 5-25 derivación del jacobiano en el 2R con la regla de la cadena y lectura física de sus columnas (Lynch y Park pp. 171-173); 25-40 jacobiano geométrico 6×n con jacob0/jacobe y jacobiano analítico con su singularidad de representación (Corke pp. 310-312); 40-55 control de velocidad resuelta con demo en la toolbox (Corke pp. 313-314); 55-60 cierre: J conecta FK diferencial, IK numérica, singularidades y estática.");

slideFotos(p4, "El 2R, en movimiento", "S17–S19 · Figura y animación", [
 { f: "figs/b4_workspace_elipses.png", x: 0.7, y: 1.5, w: 5.9, h: 5.0, cap: "Espacio de trabajo y elipses de manipulabilidad en tres posturas" },
 { f: "gifs/b4_trayectoria.gif", x: 6.85, y: 1.5, w: 5.7, h: 5.0, cap: "Trayectoria quíntica en espacio articular: la punta no describe una recta" },
], "Figuras y animación propias del curso (cuadernos S17–S19)",
"La elipse achatada de la postura estirada es el puente visual hacia singularidades (S18).");

{
 const s = contentSlide(p4, "El jacobiano: la matriz que todo lo conecta", "S17 · Cinemática diferencial");
 eqImg(s, "jac", 1.0, 1.6, 2.7, 0.72);
 bullets(s, [
 { t: "«J(q), de dimensión m x n, se llama el jacobiano»: la sensibilidad lineal de la velocidad del efector a la velocidad articular; depende de la configuración q (Lynch y Park, p. 171)." },
 { t: "Columna i = velocidad del efector cuando solo la articulación i se mueve a velocidad unidad, dibujarlas en el 2R en dos posturas." },
 { t: "En 3D la velocidad es 6D (lineal + angular): J es 6 x n; jacob0 la expresa en el marco del mundo, jacobe en el del efector (útil con sensores de fuerza)." },
 { t: "Jacobiano analítico: expresar la orientación en tasas RPY añade una singularidad de representación, otra vez el coste de los tres ángulos." },
 ], { y: 2.55, w: 6.9, size: 13, h: 4.3 });
 card(s, 7.9, 1.6, 4.7, 2.6, {
 title: "Aviso que estructura S18",
 body: "Cuando las columnas se alinean (brazo estirado), hay direcciones en las que el efector no puede moverse: el jacobiano pierde rango.",
 bodySize: 12.5,
 });
 card(s, 7.9, 4.4, 4.7, 2.25, {
 title: "Demo con el UR5",
 body: "J = robot.jacob0(q) sobre el modelo del libro: comparar columnas en configuraciones distintas y verificar la dependencia de q.",
 fill: "E3F7EC", bodySize: 12.5,
 });
 s.addNotes("Partir de la FK del 2R de S14 y derivar respecto del tiempo con la regla de la cadena. La lectura por columnas es la que fija la intuición: pedir a la clase que prediga la columna 2 en el brazo estirado antes de calcularla.");
 footer(s, "Lynch y Park, 2017, pp. 171-173 · Corke, 2023, pp. 310-312");
}


{
 const s = contentSlide(p4, "Ejemplo resuelto: jacobiano y velocidades", "S17 · Ejemplo en clase");
 card(s, 0.7, 1.58, 11.9, 0.8, { title: "", body: "Enunciado. En la rama codo abajo del ejemplo de S16 (q₁ = 1,0°, q₂ = 74,5°), calcular J y det J, y las velocidades articulares para mover el efector a v = (0,1, 0) m/s.", fill: "E3F7EC", bodySize: 12.5 });
 bullets(s, [
  { t: "Paso 1. Evaluar el jacobiano en la configuración (derivadas de la FK) y su determinante:" },
 ], { y: 2.55, w: 11.9, h: 0.55, size: 13 });
 eqImg(s, "ej_J", 1.6, 3.1, 10.1, 0.85);
 bullets(s, [
  { t: "Paso 2. Resolver q̇ = J⁻¹·v: q̇ = (0,074, −0,593) rad/s, es decir, 4,3 °/s el hombro y −34,0 °/s el codo." },
  { t: "Lectura física: mover el efector a solo 10 cm/s exige 34 grados por segundo en el codo. Cerca de la singularidad esa demanda se dispara: es el aviso de S18." },
  { t: "Referencia de escala: det J = 0,067 m², cerca de su máximo posible a₁·a₂ = 0,07: configuración cómoda, lejos de singularidad." },
 ], { y: 4.2, w: 11.9, h: 2.3, size: 13 });
 footer(s, "Cuaderno 82514_S17 · la demo con jacob0 usa estos mismos números");
}

{
 const s = contentSlide(p4, "Control de velocidad resuelta", "S17 · Mover en cartesiano sin IK");
 const steps = [
 ["Velocidad deseada", "ν del efector (6D), p. ej. línea recta a velocidad constante"],
 ["Invertir J", "q̇ = J⁻¹(q)·ν en cada instante"],
 ["Integrar", "q(t+Δt) = q(t) + q̇·Δt"],
 ["Repetir", "J(q) cambia con la configuración: recalcular en cada paso"],
 ];
 steps.forEach((c, i) => {
 const x = 0.7 + i * 3.075;
 card(s, x, 1.7, 2.78, 1.85, { title: c[0], body: c[1], num: String(i + 1), bodySize: 11, titleSize: 12.5 });
 if (i < 3) arrowR(s, x + 2.76, 2.3, 16);
 });
 card(s, 0.7, 3.9, 5.9, 2.7, {
 title: "Por qué importa",
 body: "«La esencia del control de movimiento de velocidad resuelta, un algoritmo simple y elegante que genera movimiento del efector a velocidad constante sin requerir cinemática inversa» (Corke, p. 313).",
 bodySize: 12.5,
 });
 card(s, 6.85, 3.9, 5.75, 2.7, {
 title: "Letra pequeña",
 body: "La integración en lazo abierto deriva: se corrige cerrando el lazo con la pose real. Y el algoritmo exige J invertible, qué pasa cuando no lo es se responde en S18.",
 fill: "E3F7EC", bodySize: 12.5,
 });
 s.addNotes("Demo en la toolbox: bucle que integra q con la velocidad articular que da el jacobiano para mover el efector del puma en línea recta. Discutir la deriva de integración y su corrección en lazo cerrado antes de enunciar el problema de la invertibilidad.");
 footer(s, "Corke, 2023, pp. 313-314");
}

// S18
sectionSlide(p4, "S18", "Singularidades y manipulabilidad", "Pérdida de rango · casos clásicos del 6R · elipsoide · medida de Yoshikawa",
 "0-5 recuperación de S17 (qué representa la columna i de J); 5-25 singularidades cinemáticas: definición por rango, independencia del marco y casos clásicos del 6R (Lynch y Park pp. 191-195); 25-45 elipsoide de manipulabilidad y medidas escalares (Lynch y Park pp. 173-174; Corke pp. 316-319); 45-55 demo con la toolbox: svd del jacobiano, plot_ellipsoid y m(q) a lo largo de una trayectoria; 55-60 cierre: la singularidad es anticipable y el diseño de la tarea es la primera herramienta para evitarla.");

{
 const s = contentSlide(p4, "Singularidades y elipsoide de manipulabilidad", "S18 · Geometría del movimiento posible");
 bullets(s, [
 { t: "Singularidad cinemática", h: true },
 { t: "Postura en la que el efector «pierde la capacidad de moverse instantáneamente en una o más direcciones»: J(q) deja de tener rango máximo (Lynch y Park, p. 191)." },
 { t: "No depende del marco elegido: es un hecho del robot, no de la descripción." },
 { t: "Casos clásicos 6R: dos ejes rotativos colineales (muñeca con q4 = 0), tres ejes paralelos coplanarios (codo estirado), cuatro ejes concurrentes." },
 { t: "En la práctica: cerca de la singularidad, velocidades cartesianas modestas exigen velocidades articulares enormes; los controladores industriales frenan o abortan." },
 ], { w: 6.9, size: 13 });
 card(s, 7.9, 1.6, 4.7, 2.9, {
 title: "Elipsoide de manipulabilidad",
 body: "La esfera unidad de velocidades articulares, mapeada por J, se convierte en un elipsoide de velocidades del efector. Casi esfera → postura isótropa; radios dispares → cerca de singular; en la singularidad «colapsa a un segmento».",
 bodySize: 12,
 });
 card(s, 7.9, 4.7, 4.7, 1.95, { title: "Medida de Yoshikawa", body: "", fill: "E3F7EC", bodySize: 11 });
 eqImg(s, "yoshikawa", 8.4, 5.34, 3.7, 0.54);
 s.addText("Proporcional al volumen del elipsoide. Aviso: mide volumen, no isotropía.", { x: 8.12, y: 6.04, w: 4.26, h: 0.55, fontFace: "Calibri", fontSize: 10.5, color: INK, align: "center", margin: 0 });
 s.addNotes("Demo: J = puma.jacob0(q) en qn y casi estirado; comparar det y valores singulares con np.linalg.svd; dibujar el elipsoide traslacional con plot_ellipsoid y graficar m(q) a lo largo de una trayectoria (se retoma en S19). Mensaje de cierre: la singularidad no es una avería sino una propiedad geométrica anticipable.");
 footer(s, "Lynch y Park, 2017, pp. 173-174 y 191-195 · Corke, 2023, pp. 316-319 y 328");
}

// S19
sectionSlide(p4, "S19", "Estática, trayectorias y cierre", "τ = Jᵀ·F · dualidad fuerza-velocidad · leyes temporales · repaso y cuestionario B4",
 "0-25 estática por conservación de potencia hasta tau = J^T(q)·f_tip y torsores 6D (Lynch y Park pp. 174-175; Corke pp. 324-325); 25-40 dualidad fuerza-velocidad con los elipsoides recíprocos y el ejemplo de la maleta (Lynch y Park pp. 176-177); 40-65 leyes temporales: cúbico, quíntico y trapezoidal (Lynch y Park pp. 325-333; Corke pp. 98-100); 65-75 descanso; 75-95 taller de trayectorias articulares y cartesianas (jtraj, ctraj) con monitorización de manipulabilidad; 95-105 repaso del bloque con el mapa en pizarra y las cinco ecuaciones; 105-120 cuestionario B4 en Moodle (15 min).", { f: "fotos/b4_paletizado.png", cap: "Paletizado: trayectorias punto a punto con carga", credito: "Foto: CollaborativePalletizer CC BY-SA 4.0 · Wikimedia Commons" });

{
 const s = contentSlide(p4, "Estática: τ = Jᵀ·F y la dualidad", "S19 · Fuerzas sin movimiento");
 bullets(s, [
 { t: "Derivación por conservación de potencia", h: true },
 { t: "La potencia en el efector iguala la articular; exigiendo validez para todo q̇ (Lynch y Park, p. 175):" },
 ], { w: 6.9, size: 13, h: 1.6 });
 eqImg(s, "est_deriv", 0.85, 3.28, 6.6, 0.6);
 bullets(s, [
 { t: "Versión 6D con torsores (wrenches): w = (fx, fy, fz, mx, my, mz) y Q = Jᵀ(q)·w." },
 { t: "«La traspuesta del jacobiano nunca puede ser singular» (Corke, p. 325): la estática funciona incluso donde la cinemática diferencial falla." },
 { t: "Aplicación exprés: par de hombro para sostener 10 N con el brazo extendido → dimensionado de actuadores de B3." },
 ], { y: 4.2, w: 6.9, size: 13, h: 2.5 });
 card(s, 7.9, 1.6, 4.7, 2.9, {
 title: "Dualidad fuerza-velocidad",
 body: "El elipsoide de fuerza tiene los mismos ejes que el de velocidad y semiejes recíprocos: donde es fácil generar velocidad es difícil generar fuerza, y viceversa.",
 bodySize: 12.5,
 });
 card(s, 7.9, 4.7, 4.7, 1.95, {
 title: "El ejemplo somático",
 body: "Sostener una maleta pesada con el brazo colgando recto: velocidad nula, fuerza máxima, el brazo humano trabaja en su singularidad.",
 fill: "E3F7EC", bodySize: 12.5,
 });
 s.addNotes("Derivar en pizarra la conservación de potencia: es la deducción más corta y elegante del bloque. En la singularidad el elipsoide de velocidad colapsa y el de fuerza se alarga sin límite en la dirección ortogonal.");
 footer(s, "Lynch y Park, 2017, pp. 174-177 · Corke, 2023, pp. 324-325");
}


{
 const s = contentSlide(p4, "Ejemplo resuelto: pares estáticos", "S19 · Ejemplo en clase");
 card(s, 0.7, 1.58, 11.9, 0.8, { title: "", body: "Enunciado. En la configuración del ejemplo (q₁ = 1,0°, q₂ = 74,5°), el efector debe empujar hacia arriba con F = (0, 10) N. ¿Qué pares soportan las articulaciones?", fill: "E3F7EC", bodySize: 12.5 });
 bullets(s, [
  { t: "Paso 1. La estática usa el MISMO jacobiano de S17, traspuesto: no hay que derivar nada nuevo." },
 ], { y: 2.55, w: 11.9, h: 0.55, size: 13 });
 eqImg(s, "ej_tau", 1.6, 3.12, 8.6, 0.85);
 bullets(s, [
  { t: "Paso 2. Lectura: el hombro soporta 4,0 N·m y el codo solo 0,5 N·m, porque en esta postura el segundo eslabón queda casi vertical bajo la fuerza." },
  { t: "Caso límite para dimensionar (B3): con el brazo estirado (q = 0), sostener los mismos 10 N exige τ_hombro = 0,55 · 10 = 5,5 N·m y τ_codo = 0,2 · 10 = 2,0 N·m: el peor caso del catálogo de motores." },
 ], { y: 4.2, w: 11.9, h: 1.7, size: 13 });
 card(s, 0.7, 6.0, 11.9, 0.7, { title: "", body: "La dualidad en una frase: donde el elipsoide de velocidad es corto, el de fuerza es largo. Empujar es barato justo donde moverse es caro.", fill: "E3F7EC", bodySize: 12 });
 footer(s, "Misma estructura que la parte D del parcial 1, con otros números · cuaderno 82514_S19");
}

{
 const s = contentSlide(p4, "Trayectorias: caminos y leyes temporales", "S19 · Del punto A al punto B");
 card(s, 0.7, 1.6, 11.9, 0.8, {
 title: "",
 body: "«Una trayectoria consiste en un camino (geometría pura) y una ley temporal (time scaling) que fija los instantes» (Lynch y Park, p. 325); s(t): [0, T] → [0, 1].",
 fill: "E3F7EC", bodySize: 12,
 });
 const cols = [
 ["Cúbico", "s(t) = a₀ + a₁·t + a₂·t² + a₃·t³ con velocidad nula en los extremos. Defecto: aceleración discontinua en 0 y T, tirones (jerk infinito)."],
 ["Quíntico", "Seis coeficientes: impone también las aceleraciones de contorno (sistema lineal 6x6). Movimiento más suave; «se usa comúnmente»."],
 ["Trapezoidal (LSPB)", "«Muy común en control de motores»: aceleración constante, crucero, deceleración. Aprovecha mejor los límites del accionamiento; si v²/a > 1 degenera en triángulo bang-bang."],
 ];
 cols.forEach((c, i) => card(s, 0.7 + i * 4.05, 2.6, 3.8, 2.55, { title: c[0], body: c[1], num: String(i + 1), bodySize: 11.5, titleSize: 13.5 }));
 card(s, 0.7, 5.4, 11.9, 1.25, {
 title: "Taller: articular frente a cartesiano",
 body: "jtraj(q1, q2, t): suave para los motores, la punta no describe recta. ctraj(TE1, TE2, t) + IK: recta perfecta, pero puede exigir mucho a las articulaciones, en el ejemplo del libro m(q) cae casi a cero hacia t = 1.3 s por la singularidad de muñeca.",
 fill: BG_LT, bodySize: 11.5,
 });
 s.addNotes("Empezar el taller con quintic() y trapezoidal() escalares y sus gráficas de posición, velocidad y aceleración (Corke pp. 99-100). La comparación articular/cartesiano con la manipulabilidad monitorizada cierra el círculo con S18: la IK numérica mantiene m(q) alta porque minimiza implícitamente la velocidad articular.");
 footer(s, "Lynch y Park, 2017, pp. 325-333 · Corke, 2023, pp. 98-100 y 286-289");
}

{
 const s = contentSlide(p4, "Las cinco ecuaciones del bloque", "S19 · Repaso y cuestionario B4");
 const eqs = [
 ["Rotación", "so3", "SO(3)"],
 ["Pose", "se3_T", "SE(3)"],
 ["FK (PoE)", "poe_c", ""],
 ["Diferencial", "jac", ""],
 ["Estática", "estatica", ""],
 ];
 eqs.forEach((c, i) => {
 const x = 0.7 + i * 2.5;
 card(s, x, 1.8, 2.25, 2.3, { title: c[0], body: "", num: String(i + 1), bodySize: 11.5, titleSize: 13 });
 eqImg(s, c[1], x + 0.14, 2.92, 1.97, 0.78);
 if (c[2]) s.addText(c[2], { x, y: 3.8, w: 2.25, h: 0.26, align: "center", fontFace: "Calibri", fontSize: 10, color: GREY, margin: 0 });
 if (i < 4) arrowR(s, x + 2.22, 2.7, 15);
 });
 card(s, 0.7, 4.5, 11.9, 1.1, {
 title: "El mapa del bloque",
 body: "Pose (S13) → FK (S14-S15) → IK (S16) → jacobiano (S17) → singularidades y manipulabilidad (S18) → estática y trayectorias (S19). En cada nodo, una pregunta tipo del cuestionario.",
 fill: "E3F7EC", bodySize: 12,
 });
 card(s, 0.7, 5.8, 11.9, 0.85, {
 title: "",
 body: "Cuestionario B4 (15 min, 10 preguntas ABCD): bloqueo de cardán · SO(3)/SE(3) · PoE · ocho soluciones IK · definición de singularidad · Yoshikawa · τ = Jᵀ·F · trapezoidal frente a quíntico.",
 fill: BG_LT, bodySize: 11.5,
 });
 s.addNotes("Construir el mapa en la pizarra con la clase, no proyectarlo primero. Repasar las cinco ecuaciones en voz alta pidiendo a estudiantes distintos que expliquen qué significa cada una y dónde se usó. Después, cuestionario B4 vía campus con corrección automática; los errores más comunes se revisan al inicio de S20.");
 footer(s, "Cuestionario B4 · páginas de referencia en el guion de S19");
}

p4.writeFile({ fileName: "IQS_B4_Cinematica_Estatica.pptx" }).then(() => console.log("OK deck B4"));

/* ==================== DECK B5 ==================== */
const p5 = newDeck();

titleSlide(p5, {
 curso: "82514 · MECATRÓNICA Y ROBÓTICA",
 bloque: "Bloque 5",
 titulo: "Modelado y control\nde sistemas robóticos",
 sub: "Sesiones S20–S24 · 6 horas",
 fechas: "28, 29 y 30 de octubre y 4 y 5 de noviembre de 2026 · IQS Universitat Ramon Llull",
});

{
 const s = contentSlide(p5, "Hoja de ruta del bloque", "Bloque 5");
 const rows = [
 ["S20 · mié 28 oct · 1 h", "Modelado de sistemas electromecánicos: EDO, función de transferencia, analogías"],
 ["S21 · jue 29 oct · 1 h", "Respuesta temporal y frecuencial con python-control"],
 ["S22 · vie 30 oct · 2 h", "Taller: control PID de una articulación, saturación y anti-windup"],
 ["S23 · mié 4 nov · 1 h", "Espacio de estados, controlabilidad y realimentación de estado"],
 ["S24 · jue 5 nov · 1 h", "Dinámica de manipuladores y par calculado · cuestionario B5"],
 ];
 rows.forEach((r, i) => agendaRow(s, 1.62 + i * 1.05, 0.9, String(i + 1), r[0], r[1]));
 s.addNotes("Mensaje de apertura: hasta ahora el robot era geometría (B4); a partir de hoy es física, fuerzas, pares, corrientes, y el control convierte esa física en el movimiento que queremos. Cuestionario B5 en los últimos 15 minutos de S24; el viernes siguiente a este bloque (6 nov) es el parcial 1 de B1-B4.");
 footer(s, "82514 Mecatrónica y Robótica · B5 · IQS");
}

// S20
sectionSlide(p5, "S20", "Modelado electromecánico", "La EDO del motor DC con carga · función de transferencia · analogías entre dominios",
 "0-5 presentación del bloque (modelar → analizar → controlar → estado → dinámica multiarticular); 5-25 la EDO del motor DC con carga: acoplo τ = Kt·i, malla eléctrica, back-EMF y reducción a primer orden (Lynch y Park pp. 306-311; De Silva p. 91; Corke p. 346); 25-40 función de transferencia y formas del modelo (De Silva pp. 88-90); 40-55 analogías entre dominios con la tabla fuerza-tensión construida con la clase; 55-60 cierre: instalar python-control y leer De Silva pp. 88-93.", { f: "fotos/b1_watt.jpg", cap: "Regulador centrífugo de Watt: el primer lazo realimentado", credito: "Foto: A. Dingley CC BY 3.0 · Wikimedia Commons" });

slideFotos(p5, "El actuador por dentro y las tres letras", "S20–S22 · Motor y PID", [
 { f: "fotos/b5_motor.jpg", x: 0.7, y: 1.5, w: 5.85, h: 5.0, cap: "Máquina eléctrica en corte: rotor, estátor, devanados" },
 { f: "figs/b5_p_pd_pid.png", x: 6.75, y: 1.7, w: 5.85, h: 4.5, cap: "P, PD y PID sobre la misma planta: qué aporta cada término" },
], "Foto: Technisches Museum Wien, dominio público · Wikimedia Commons · Figura propia del curso",
"La figura anticipa el taller de S22: P deja error o oscila, D amortigua, I elimina el error de régimen.");

{
 const s = contentSlide(p5, "El motor DC con carga: de la física a la EDO", "S20 · Modelado");
 bullets(s, [
 { t: "Las tres ecuaciones del accionamiento: acoplo par-corriente, malla eléctrica con back-EMF y mecánica del conjunto", h: true },
 ], { w: 6.9, size: 12.5, h: 0.9 });
 eqImg(s, "motor3", 1.15, 2.5, 4.7, 1.55);
 bullets(s, [
 { t: "Reducción a primer orden: la constante de tiempo eléctrica « la mecánica (Lynch y Park, p. 310):" },
 ], { y: 4.3, w: 6.9, size: 12.5, h: 0.65 });
 eqImg(s, "reduccion", 1.15, 4.98, 4.9, 0.62);
 bullets(s, [
 { r: [{ t: "Reductora G: ω ÷G, τ ×η·G; inercia aparente del rotor vista desde la articulación: G²·I" }, { t: "rotor", sub: true }, { t: ", que puede superar la del eslabón." }] },
 ], { y: 5.85, w: 6.9, size: 12.5, h: 1.1 });
 card(s, 7.9, 1.6, 4.7, 2.7, { title: "Función de transferencia", body: "", bodySize: 12.5 });
 s.addText("Velocidad, primer orden:", { x: 8.15, y: 2.18, w: 4.2, h: 0.28, fontFace: "Calibri", fontSize: 11.5, color: INK, margin: 0 });
 eqImg(s, "tf_vel", 8.6, 2.48, 2.5, 0.62);
 s.addText("Posición, se añade un integrador:", { x: 8.15, y: 3.28, w: 4.2, h: 0.28, fontFace: "Calibri", fontSize: 11.5, color: INK, margin: 0 });
 eqImg(s, "tf_pos", 8.55, 3.58, 2.6, 0.62);
 card(s, 7.9, 4.5, 4.7, 2.15, {
 title: "Por qué la reductora ayuda al control",
 body: "«Disminuye los pares de perturbación en 1/G y la variación de inercia y fricción en 1/G²» (Corke, p. 348), reaparecerá en S24.",
 fill: "E3F7EC", bodySize: 12.5,
 });
 s.addNotes("Experimento mental de la back-EMF: girar el eje a mano con el motor desconectado y medir Kt·ω en bornes (Lynch y Park p. 308). Dos caminos hacia el modelo: derivación física o identificación de la respuesta medida, el HDD del libro obtiene la misma planta por ambas vías (De Silva pp. 88-89).");
 footer(s, "De Silva et al., 2016, pp. 88-91 · Lynch y Park, 2017, pp. 306-311 · Corke, 2023, pp. 346-348");
}

{
 const s = contentSlide(p5, "Analogías entre dominios físicos", "S20 · Un solo lenguaje");
 card(s, 0.7, 1.7, 5.9, 2.15, { title: "Mecánico", body: "", bodySize: 13 });
 eqImg(s, "analog_mec", 1.55, 2.42, 4.2, 0.58);
 s.addText("masa · amortiguador · muelle · fuerza", { x: 0.92, y: 3.28, w: 5.46, h: 0.3, align: "center", fontFace: "Calibri", fontSize: 11.5, color: GREY, margin: 0 });
 card(s, 6.85, 1.7, 5.75, 2.15, { title: "Eléctrico", body: "", bodySize: 13 });
 eqImg(s, "analog_ele", 7.7, 2.36, 4.05, 0.66);
 s.addText("inductancia · resistencia · 1/capacidad · tensión", { x: 7.07, y: 3.28, w: 5.31, h: 0.3, align: "center", fontFace: "Calibri", fontSize: 11.5, color: GREY, margin: 0 });
 card(s, 0.7, 4.05, 11.9, 1.3, {
 title: "La misma EDO, distinta física",
 body: "masa ↔ inductancia · amortiguador ↔ resistencia · muelle ↔ 1/capacidad (analogía fuerza-tensión). Dinámica rápida en el aula: ¿el análogo eléctrico de la suspensión de un coche? ¿El análogo mecánico de un filtro RC?",
 fill: "E3F7EC", bodySize: 12.5,
 });
 card(s, 0.7, 5.55, 11.9, 1.25, {
 title: "El motor DC como sistema mixto",
 body: "La malla eléctrica y el balance mecánico se acoplan por Kt (par-corriente) y Ke (tensión-velocidad): el ejemplo canónico de por qué la mecatrónica necesita un lenguaje común. El disco duro: cadena de masas, muelles y amortiguadores → función de transferencia de la misma familia.",
 fill: BG_LT, bodySize: 12,
 });
 s.addNotes("Escribir las dos EDO en paralelo y construir la tabla de la analogía con aportaciones de la clase. Cierre de la sesión: encargar pip install control y comprobar import control as ct antes de S21.");
 footer(s, "De Silva et al., 2016, pp. 88-91");
}

// S21
sectionSlide(p5, "S21", "Respuesta temporal y frecuencial", "Primer y segundo orden · polos y estabilidad · python-control",
 "0-5 recuperación: un estudiante deriva la función de transferencia del motor de velocidad; 5-15 python-control en diez minutos: ct.tf, ct.step_response, ct.poles, ct.step_info con el motor de S20 en directo; 15-35 respuesta de primer y segundo orden: τ, ζ, ωn, sobreoscilación y valores para memorizar (Lynch y Park pp. 409-413); 35-50 polos, estabilidad y Bode (Lynch y Park p. 424; De Silva pp. 88-89); 50-60 ejercicio individual con G(s) = 25/(s² + 4s + 25) y cierre con encargos para el taller.");

{
 const s = contentSlide(p5, "Respuesta de primer y segundo orden", "S21 · Leer la dinámica");
 const g = [
 ["Primer orden", "Solución e^(−t/τ): en t = τ la señal ha decaído al 37 %; tiempo de establecimiento al 2 % ≈ 4·τ."],
 ["Segundo orden", [{ text: "ë + 2ζωₙ·ė + ωₙ²·e = 0 define frecuencia natural ωₙ y amortiguamiento ζ; sobre-, crítica- o subamortiguado según ζ; ω" }, { text: "d", options: { subscript: true } }, { text: " = ωₙ·√(1−ζ²)." }]],
 ["Sobreoscilación", [{ text: "Mp = e^(−πζ/√(1−ζ²))·100 %, pico en tp = π/ω" }, { text: "d", options: { subscript: true } }, { text: ". Para memorizar: ζ = 0.1 → 73 % · ζ = 0.5 → 16 % · ζ = 0.8 → 1.5 %." }]],
 ["Reglas rápidas", "tr ≈ 1.8/ωₙ y ts ≈ 4.6/(ζ·ωₙ). «El papel del control de movimiento es forzar estas características a cumplir las especificaciones» (De Silva, p. 92)."],
 ];
 g.forEach((c, i) => {
 const col = i % 2, row = Math.floor(i / 2);
 card(s, 0.7 + col * 6.1, 1.7 + row * 2.45, 5.85, 2.25, { title: c[0], body: c[1], num: String(i + 1), bodySize: 12, titleSize: 14 });
 });
 card(s, 0.7, 6.35, 11.9, 0.6, {
 title: "",
 body: "Ejercicio individual: para G(s) = 25/(s² + 4s + 25), predecir a mano ζ, ωn, Mp y ts, y verificar con ct.step_info().",
 fill: "E3F7EC", bodySize: 11.5,
 });
 s.addNotes("Ejecutar el motor de S20 en vivo con valores numéricos y señalar la constante de tiempo sobre la gráfica de step_response. El ejercicio final se corrige discutiendo las discrepancias entre la predicción manual y step_info.");
 footer(s, "Lynch y Park, 2017, pp. 409-413 · De Silva et al., 2016, p. 92");
}

{
 const s = contentSlide(p5, "Polos, estabilidad y respuesta en frecuencia", "S21 · El mapa del plano s");
 bullets(s, [
 { t: "El criterio y el mapa", h: true },
 { t: "Estable ⇔ todas las raíces del polinomio característico tienen parte real negativa (Lynch y Park, p. 424)." },
 { t: "Raíces más a la izquierda → establecimiento más corto; más lejos del eje real → más sobreoscilación. Válido también en orden superior." },
 { t: "Respuesta en frecuencia: el diagrama de Bode (magnitud y fase frente a frecuencia); la identificación del HDD de S20 se hizo exactamente así." },
 { t: "Mover una ganancia y ver los polos desplazarse: la semilla del diseño de control de S22-S23." },
 ], { w: 6.9, size: 13 });
 card(s, 7.9, 1.6, 4.7, 3.0, {
 title: "python-control, las llamadas del día",
 body: "G = ct.tf([K2], [I, K1])\nt, y = ct.step_response(G)\nct.poles(G)\nct.step_info(G)\nct.bode_plot(G)",
 bodySize: 13,
 });
 card(s, 7.9, 4.8, 4.7, 1.85, {
 title: "En vivo",
 body: "ct.poles() sobre el motor con y sin integrador: el integrador añade un polo en s = 0, al borde de la estabilidad.",
 fill: "E3F7EC", bodySize: 12.5,
 });
 s.addNotes("Comprobar en vivo con ct.poles() el efecto del integrador y de una ganancia sobre la posición de los polos. Encargos para S22: portátil con python-control funcionando y relectura de la ley PID (De Silva pp. 93-95).");
 footer(s, "Lynch y Park, 2017, pp. 412 y 424 · De Silva et al., 2016, pp. 88-89");
}

// S22
sectionSlide(p5, "S22", "Taller: PID de una articulación", "La planta del péndulo motorizado · ley PID · sintonía · saturación y anti-windup",
 "0-10 la planta del taller: eslabón en plano vertical, τ = M·θ̈ + m·g·r·cosθ + b·θ̇ con los números del libro (Lynch y Park pp. 421-422); objetivo Mp < 5 % y ts < 1.5 s; 10-30 la ley PID y la dinámica del error: PD como muelle-amortiguador virtual, error estacionario por gravedad, cotas de Ki (Lynch y Park pp. 422-425); 30-75 taller parte 1: rondas P → PD → PID con anotación de ganancias y métricas (De Silva p. 98); 75-85 descanso; 85-110 taller parte 2: saturación, windup y dos remedios (De Silva pp. 99-100 y 109; Lynch y Park p. 425); 110-120 puesta en común y anticipo del espacio de estados.");

slideFotos(p5, "Subir Kp, en vivo", "S22 · Animación del taller", [
 { f: "gifs/b5_kp.gif", x: 0.8, y: 1.55, w: 7.2, h: 5.0, cap: "Barrido de Kp: más rápido, pero con más sobreoscilación" },
], "Animación propia del curso (cuaderno S22)",
"Proyectar en bucle mientras las parejas hacen la ronda 1 del taller: es la referencia visual de lo que deben ver en su pantalla. A la derecha queda espacio para anotar en la pizarra las ganancias que va cantando cada pareja.");

{
 const s = contentSlide(p5, "La ley PID y la dinámica del error", "S22 · Teoría del taller");
 eqImg(s, "pid", 1.0, 1.62, 3.5, 0.66);
 bullets(s, [
 { t: "Kp es «un muelle virtual» y Kd «un amortiguador virtual» (Lynch y Park, pp. 422-423); el PID «sigue ampliamente usado tras más de 70 años» (De Silva, p. 93)." },
 { t: "PD sin gravedad: M·ë + (b+Kd)·ė + Kp·e = 0, las ganancias colocan ζ y ωₙ, el puente con S21:" },
 ], { y: 2.5, w: 7.3, size: 12.5, h: 1.8 });
 eqImg(s, "pd_zw", 1.35, 4.35, 3.9, 0.78);
 bullets(s, [
 { t: "Con gravedad el PD deja error estacionario: sostener el eslabón exige par no nulo, y Kp·θe = m·g·r·cosθ en el reposo." },
 { t: "El término I lo elimina, pero sube el orden a tres y acota Ki: (b+Kd)·Kp/M > Ki > 0. En la práctica, «Ki = 0 en muchos controladores de robots»." },
 ], { y: 5.3, w: 7.3, size: 12.5, h: 1.7 });
 card(s, 8.3, 1.6, 4.3, 3.0, { title: "La planta del taller", body: "", bodySize: 12 });
 eqImg(s, "planta", 8.5, 2.32, 3.9, 0.52);
 s.addText("Eslabón en plano vertical con M = 0.5 kg·m², m = 1 kg, r = 0.1 m, b = 0.1, números del libro, para comparar resultados.", { x: 8.52, y: 3.05, w: 3.9, h: 1.4, fontFace: "Calibri", fontSize: 11.5, color: INK, margin: 0 });
 card(s, 8.3, 4.8, 4.3, 1.85, {
 title: "Objetivo",
 body: "Llevar el eslabón de θ = −π/2 a θ = 0 con Mp < 5 % y ts < 1.5 s; primero sin y luego con saturación del actuador.",
 fill: "E3F7EC", bodySize: 12,
 });
 s.addNotes("Estrategia de sintonía que se defiende en la puesta en común: elegir Kp y Kd para el transitorio y añadir el mínimo Ki útil. El esqueleto de código simula la planta no lineal por integración explícita con paso de 1 ms y un PID discreto.");
 footer(s, "Lynch y Park, 2017, pp. 421-425 · De Silva et al., 2016, pp. 93-98");
}

{
 const s = contentSlide(p5, "Sintonía por rondas, saturación y anti-windup", "S22 · El taller en cinco pasos");
 const steps = [
 ["Solo P", "subir Kp hasta oscilar; queda error de gravedad"],
 ["PD", "Kd para ζ = 1: sin sobreoscilación, el error persiste"],
 ["PID", "Ki dentro de sus cotas: error estacionario nulo"],
 ["Saturación", [{ text: "τ" }, { text: "max", options: { subscript: true } }, { text: " = 1.5 N·m: aparece el windup" }]],
 ["Anti-windup", "dos remedios; comparar curvas"],
 ];
 steps.forEach((c, i) => {
 const x = 0.7 + i * 2.5;
 card(s, x, 1.7, 2.25, 1.9, { title: c[0], body: c[1], num: String(i + 1), bodySize: 10.5, titleSize: 13 });
 if (i < 4) arrowR(s, x + 2.22, 2.35, 15);
 });
 card(s, 0.7, 3.95, 5.9, 2.7, {
 title: "El windup",
 body: "Con el actuador saturado el integrador sigue acumulando; al llegar al objetivo, el par tarda en «desenrollarse»: «gran sobreoscilación y largo tiempo de establecimiento» (De Silva, pp. 99-100). La saturación además «reduce la ganancia a amplitudes altas y ralentiza la respuesta» (p. 109).",
 bodySize: 11.5,
 });
 card(s, 6.85, 3.95, 5.75, 2.7, {
 title: "Dos remedios",
 body: "1. Integración condicional: «dejar de actualizar la parte integral cuando la señal de control está limitada» (De Silva, p. 100).\n\n2. Límite del integrador: «imponer un límite a cuánto puede crecer la integral del error» (Lynch y Park, p. 425).",
 bodySize: 11.5,
 });
 s.addNotes("Cada pareja anota sus ganancias finales y sus métricas (Mp, ts) para la puesta en común: discutir la dispersión de ganancias válidas y el compromiso velocidad-robustez. Mencionar Ziegler-Nichols como alternativa sistemática (De Silva pp. 98-99), queda como lectura. En el laboratorio la saturación es el límite de corriente del amplificador: el windup aparece a la primera referencia agresiva.");
 footer(s, "De Silva et al., 2016, pp. 98-100 y 109 · Lynch y Park, 2017, p. 425");
}

// S23
sectionSlide(p5, "S23", "Espacio de estados", "ẋ = A·x + B·u · controlabilidad de Kalman · u = −K·x · observadores",
 "0-5 recuperación de S22 (error estacionario del PD con gravedad; anti-windup); 5-25 la representación en espacio de estados con el motor DC como ejemplo, x = [θ, ω] (De Silva p. 90); 25-40 controlabilidad conceptual con la condición de rango de Kalman y comprobación con ct.ctrb (Lynch y Park p. 528); 40-55 realimentación de estado u = −K·x, asignación de polos con ct.place, observador y mención de LQR; 55-60 cierre: anunciar S24 con la dinámica multiarticular y el cuestionario B5.");

{
 const s = contentSlide(p5, "Estado, controlabilidad y realimentación", "S23 · Ver todas las variables");
 eqImg(s, "ss", 0.95, 1.62, 4.4, 0.55);
 bullets(s, [
 { t: "El estado es la memoria mínima del sistema: lo que hay que conocer hoy para predecir mañana dadas las entradas." },
 { t: "El motor DC con x = [θ, ω]: A = [[0, 1], [0, −K1/I]], B = [0, K2/I], C = [1, 0], el sistema de S20 con otra ropa." },
 { t: "Controlabilidad: la condición de rango de Kalman (abajo). Intuición: B es donde empuja la entrada y A·B adónde se propaga; si esas direcciones no llenan el espacio, hay estados inalcanzables." },
 { t: "Nota para B7: un robot móvil no holonómico no es linealmente controlable y aun así llega a todas partes maniobrando." },
 ], { y: 2.45, w: 6.9, size: 12.5, h: 3.3 });
 eqImg(s, "kalman", 1.0, 5.95, 5.4, 0.5);
 card(s, 7.9, 1.6, 4.7, 2.9, {
 title: "u = −K·x y asignación de polos",
 body: "Si el sistema es controlable, existe K que estabiliza el origen; K pesa todos los estados, no solo el error de salida. K = ct.place(A, B, polos): demo con polos en −5 ± 5j frente a −20 ± 5j.",
 bodySize: 12,
 });
 card(s, 7.9, 4.7, 4.7, 1.95, {
 title: "Observador y LQR",
 body: "El observador estima los estados no medidos a partir de pocas medidas reales (su eficacia depende del modelo). LQR: K que minimiza un coste cuadrático (ct.lqr), puente con B8.",
 fill: "E3F7EC", bodySize: 12,
 });
 s.addNotes("Comprobar la controlabilidad en vivo con ct.ctrb y matrix_rank sobre el motor (controlable) y sobre un contraejemplo con un estado desconectado de la entrada. Frente al PID, la realimentación de estado ve el interior del sistema, no solo la salida.");
 footer(s, "De Silva et al., 2016, pp. 90-102 · Lynch y Park, 2017, p. 528");
}

// S24
sectionSlide(p5, "S24", "Dinámica y par calculado", "Euler-Lagrange · M(q)·q̈ + C·q̇ + g = τ · control por dinámica inversa · cuestionario B5",
 "0-5 motivación: cada motor de un manipulador serie no ve una inercia constante sino un robot entero moviéndose; 5-25 Euler-Lagrange en cuatro pasos, el 2R con gravedad y la forma matricial de la ecuación del manipulador con su jerarquía de términos (Lynch y Park pp. 272-276; Corke pp. 348-353); 25-40 del PID articular independiente al par calculado, con feedforward y PID + gravedad como alternativas (Lynch y Park pp. 429-432; Corke pp. 359-360); 40-45 síntesis del bloque con el arco S20-S24; 45-60 cuestionario B5 en Moodle (15 min).");

{
 const s = contentSlide(p5, "La ecuación del manipulador", "S24 · Euler-Lagrange");
 s.addShape("roundRect", { x: 0.7, y: 1.6, w: 11.9, h: 0.95, rectRadius: 0.08, fill: { color: NAVY }, line: { type: "none" } });
 eqImg(s, "manip", 1.15, 1.83, 5.5, 0.5);
 s.addText("lineal en q̈ · cuadrática en q̇ · trigonométrica en q", { x: 7.1, y: 1.6, w: 5.3, h: 0.95, valign: "middle", fontFace: "Calibri", fontSize: 12.5, color: "C9D2F5", margin: 0 });
 const cols = [
 ["M(q), inercia", "Matriz de masas simétrica definida positiva; acopla los ejes y varía con la configuración: la inercia vista por el hombro del PUMA 560 cambia un factor 2.16."],
 ["C(q, q̇), Coriolis", "Términos centrífugos con q̇ᵢ² y de Coriolis con q̇ᵢ·q̇ⱼ: solo aparecen en movimiento y crecen con la velocidad."],
 ["g(q), gravedad", "«Generalmente el término dominante» (Corke, p. 350): actúa incluso parado. Después, la fricción es «la siguiente más dominante» (p. 353)."],
 ];
 cols.forEach((c, i) => card(s, 0.7 + i * 4.05, 2.85, 3.8, 2.5, { title: c[0], body: c[1], num: String(i + 1), bodySize: 11.5, titleSize: 13 }));
 card(s, 0.7, 5.6, 6.55, 1.05, {
 title: "",
 body: "Versión completa de ingeniería con fricción y fuerza externa: Q = M·q̈ + C·q̇ + f(q̇) + g(q) + Jᵀ(q)·w (dinámica inversa; Corke, ec. 9.11).",
 fill: "E3F7EC", bodySize: 11.5,
 });
 s.addText("Receta lagrangiana:", { x: 7.5, y: 5.52, w: 2.0, h: 0.3, fontFace: "Calibri", fontSize: 11, color: GREY, margin: 0 });
 eqImg(s, "lagrange", 7.5, 5.84, 4.85, 0.82);
 s.addNotes("Calentar con la masa puntual vertical: la receta reproduce f − m·g = m·ẍ. Presentar el 2R con gravedad sin el álgebra completa (ec. 8.9) y reagrupar en la forma matricial. Para el cuestionario: identificar qué término produce cada fenómeno (par en reposo → gravedad; par con q̇² → centrífugo; acoplo entre ejes → términos no diagonales de M y C).");
 footer(s, "Lynch y Park, 2017, pp. 272-276 · Corke, 2023, pp. 348-353");
 // texto de la banda navy en blanco
}

{
 const s = contentSlide(p5, "Control por par calculado", "S24 · Cancelar la dinámica con el modelo");
 const flow = [
 ["Trayectoria deseada", "q_d, q̇_d, q̈_d (B4, S19)"],
 ["PID sobre el error", "q̈_ref = q̈_d + Kp·e + Kd·ė + Ki·∫e"],
 ["Modelo inverso", "τ = M̂(q)·q̈_ref + ĥ(q, q̇)"],
 ["Robot real", "q y q̇ medidos realimentan el lazo"],
 ];
 flow.forEach((c, i) => {
 const x = 0.7 + i * 3.075;
 card(s, x, 1.7, 2.78, 1.9, { title: c[0], body: c[1], num: String(i + 1), bodySize: 10.5, titleSize: 12 });
 if (i < 3) arrowR(s, x + 2.76, 2.3, 16);
 });
 card(s, 0.7, 3.9, 11.9, 0.9, {
 title: "",
 body: "Con linealización ideal, la dinámica del error es ë + Kv·ė + Kp·e = 0: lineal, desacoplada e independiente de la configuración (Corke, ec. 9.17). Es «control por dinámica inversa: un sistema no lineal en cascada con su inverso, de ganancia unidad» (Corke, p. 359).",
 fill: "E3F7EC", bodySize: 11.5,
 });
 card(s, 0.7, 5.0, 5.9, 1.7, {
 title: "Alternativas más simples",
 body: "PID articular independiente: válido si M es casi diagonal (robots cartesianos o muy reducidos: el 1/G²). PID + compensación de gravedad: τ = Kp·e + Ki·∫e + Kd·ė + ĝ(q), suficiente a velocidades pequeñas.",
 bodySize: 11.5,
 });
 card(s, 6.85, 5.0, 5.75, 1.7, {
 title: "Requisitos y límites",
 body: "Exige estimar masas, centros de masas, inercias y fricción; con error de modelo aparece un forzamiento en la dinámica del error. En la práctica: mejor seguimiento que feedforward o feedback solos, con menos esfuerzo de control.",
 bodySize: 11.5,
 });
 s.addNotes("Contrastar con el feedforward de par: también usa el modelo, pero su dinámica de error sigue acoplada por M no diagonal y depende de la configuración (Corke, ec. 9.15). Conexiones hacia delante: M, C, g reaparecen en simulación (Gazebo/Isaac, B8) y el par calculado es la base de los controladores sobre MoveIt 2 (B7).");
 footer(s, "Lynch y Park, 2017, pp. 429-432 · Corke, 2023, pp. 359-360");
}

{
 const s = contentSlide(p5, "El arco del bloque y el cuestionario B5", "S24 · Síntesis");
 const arc = [
 ["S20", "Física → EDO y función de transferencia"],
 ["S21", "Polos, ζ y ωn: leer la respuesta"],
 ["S22", "PID: sintonía, saturación, anti-windup"],
 ["S23", "Estado: ẋ = A·x + B·u, u = −K·x"],
 ["S24", "M(q)·q̈ + C·q̇ + g = τ y par calculado"],
 ];
 arc.forEach((c, i) => {
 const x = 0.7 + i * 2.5;
 card(s, x, 1.8, 2.25, 2.15, { title: c[0], body: c[1], titleColor: GREEN_DK, bodySize: 11, titleSize: 16 });
 if (i < 4) arrowR(s, x + 2.22, 2.6, 15);
 });
 card(s, 0.7, 4.35, 11.9, 1.15, {
 title: "Cuestionario B5 (15 min, 10 preguntas ABCD)",
 body: "EDO del motor y reducción · especificaciones y polos · dinámica del error PD/PID y windup · condición de Kalman · términos de la ecuación del manipulador y par calculado. Incluye un cálculo corto: dinámica de error de un PD con números dados.",
 fill: "E3F7EC", bodySize: 12,
 });
 card(s, 0.7, 5.7, 11.9, 0.95, {
 title: "",
 body: "Hacia delante: la dinámica M, C, g reaparece en simulación (Gazebo/Isaac, B8) y el par calculado es la base de los controladores de los brazos que se programarán sobre MoveIt 2 en B7.",
 fill: BG_LT, bodySize: 12,
 });
 s.addNotes("Recorrer el arco completo en la pizarra con la clase antes de proyectarlo. No se pide reproducir la derivación completa del 2R: sí identificar qué término de la ecuación del manipulador produce cada fenómeno físico. Cerrar con las conexiones hacia B6-B8.");
 footer(s, "82514 Mecatrónica y Robótica · B5 · Cuestionario B5");
}

p5.writeFile({ fileName: "IQS_B5_Modelado_Control.pptx" }).then(() => console.log("OK deck B5"));
