#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Edición masiva de los 3 generadores de decks:
   ecuaciones LaTeX como imagen, encaje con ratio real, fotos en portadillas,
   nuevas diapositivas de fotos y limpieza de avisos obvios."""
import re, sys

ARCHIVOS = ["decks.js", "decks_b3b4b5.js", "decks_b6b7b8.js"]
src = {f: open(f, encoding="utf-8").read() for f in ARCHIVOS}
fallos = []

def rep(f, viejo, nuevo, n=1):
    c = src[f].count(viejo)
    if c != n:
        fallos.append(f"{f}: esperaba {n}, hay {c}: {viejo[:90]!r}")
        return
    src[f] = src[f].replace(viejo, nuevo)

def rep_opc(f, viejo, nuevo):
    src[f] = src[f].replace(viejo, nuevo)

# ══ 1. sectionSlide con foto opcional (los 3 archivos) ══
SEC_VIEJO = '''  s.addText(sub, { x: 2.25, y: 2.5, w: 9.8, h: 0.9, fontFace: "Calibri", fontSize: 16, color: "C9D2F5", margin: 0 });
  if (notas) s.addNotes(notas);
  return s;
}'''
SEC_NUEVO = '''  s.addText(sub, { x: 2.25, y: 2.5, w: 9.8, h: 0.9, fontFace: "Calibri", fontSize: 16, color: "C9D2F5", margin: 0 });
  if (foto) {
    const b = img(s, foto.f, 8.5, 2.95, 4.15, 3.55);
    s.addShape("rect", { x: b.x, y: b.y + b.h, w: b.w, h: 0.06, fill: { color: GREEN }, line: { type: "none" } });
    if (foto.cap) s.addText(foto.cap, { x: 8.3, y: b.y + b.h + 0.14, w: 4.55, h: 0.55, fontFace: "Calibri", fontSize: 10, color: "C9D2F5", align: "center", margin: 0 });
    if (foto.credito) s.addText(foto.credito, { x: 7.3, y: 7.14, w: 5.55, h: 0.25, fontFace: "Calibri", fontSize: 8, color: "8A97D8", align: "right", margin: 0 });
  }
  if (notas) s.addNotes(notas);
  return s;
}'''
for f in ARCHIVOS:
    rep(f, "function sectionSlide(p, num, titulo, sub, notas) {", "function sectionSlide(p, num, titulo, sub, notas, foto) {")
    rep(f, SEC_VIEJO, SEC_NUEVO)

# ══ 2. Bloque de material visual: encaje con ratio real + eqImg ══
MEDIA_VIEJO = '''const MEDIA = __dirname + "/media/";
function slideFotos(pres, titulo, kicker, items, credito, notas) {
  const s = contentSlide(pres, titulo, kicker);
  items.forEach(it => {
    s.addImage({ path: MEDIA + it.f, x: it.x, y: it.y, w: it.w, h: it.h, sizing: { type: "contain", w: it.w, h: it.h } });
    if (it.cap) s.addText(it.cap, { x: it.x, y: it.y + it.h + 0.03, w: it.w, h: 0.3, fontFace: "Calibri", fontSize: 10.5, color: GREY, align: "center", margin: 0 });
  });
  if (credito) footer(s, credito);
  if (notas) s.addNotes(notas);
  return s;
}'''
MEDIA_NUEVO = '''const MEDIA = __dirname + "/media/";
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
}'''
for f in ARCHIVOS:
    rep(f, MEDIA_VIEJO, MEDIA_NUEVO)

# ══ 3. Fotos en portadillas de sección ══
def foto_seccion(f, marcador, foto_js):
    i = src[f].find(marcador)
    if i < 0:
        fallos.append(f"{f}: no encuentro sección {marcador[:60]!r}")
        return
    j = src[f].find('");', i)
    fin = src[f].find(');\n', i)
    if j < 0 or fin != j + 1:
        fallos.append(f"{f}: cierre raro en {marcador[:60]!r}")
        return
    src[f] = src[f][:j+1] + ", " + foto_js + src[f][j+1:]

foto_seccion("decks.js", 'sectionSlide(p2, "S5", "Taxonomía y configuraciones"',
  '{ f: "fotos/b2_davinci.jpg", cap: "Da Vinci Xi: el telerobot quirúrgico", credito: "Foto: Alvarogarciamd CC BY-SA 4.0 — Wikimedia Commons" }')
foto_seccion("decks.js", 'sectionSlide(p2, "S6", "Robots móviles"',
  '{ f: "fotos/b2_dron.jpg", cap: "Multirrotor: locomoción aérea", credito: "Foto: J. Sorenson CC0 — Wikimedia Commons" }')
foto_seccion("decks.js", 'sectionSlide(p2, "S7", "Cobots, seguridad y normativa"',
  '{ f: "fotos/b2_cobot3.png", cap: "UR16e: fuerza limitada y par medido en cada eje", credito: "Foto: Auledas CC BY-SA 4.0 — Wikimedia Commons" }')
foto_seccion("decks_b3b4b5.js", 'sectionSlide(p3, "S8", "Arquitectura de instrumentación"',
  '{ f: "fotos/b3_ultrasonido.jpg", cap: "HC-SR04: sensor y acondicionamiento en la misma placa", credito: "Foto: S. Dwivedi CC BY-SA 4.0 — Wikimedia Commons" }')
foto_seccion("decks_b3b4b5.js", 'sectionSlide(p3, "S10", "Fuerza, tacto y rango"',
  '{ f: "fotos/b6_estereo3.jpg", cap: "Par estéreo: profundidad por triangulación", credito: "Foto: T. Cognard CC BY-SA 3.0 — Wikimedia Commons" }')
foto_seccion("decks_b3b4b5.js", 'sectionSlide(p3, "S11", "Actuadores eléctricos"',
  '{ f: "fotos/b3_stepper.jpg", cap: "NEMA 17: el paso a paso de referencia", credito: "Foto: oomlout CC BY-SA 2.0 — Wikimedia Commons" }')
foto_seccion("decks_b3b4b5.js", 'sectionSlide(p3, "S12", "Hidráulica, neumática y reductoras"',
  '{ f: "fotos/b3_harmonic.jpg", cap: "Harmonic drive: reducción alta sin holgura", credito: "Foto: wdwd CC BY-SA 4.0 — Wikimedia Commons" }')
foto_seccion("decks_b3b4b5.js", 'sectionSlide(p4, "S13", "Posición y orientación"',
  '{ f: "fotos/b4_abb3.jpg", cap: "ASEA/ABB: medio siglo de brazos de 6 ejes", credito: "Foto: Dependability CC BY-SA 4.0 — Wikimedia Commons" }')
foto_seccion("decks_b3b4b5.js", 'sectionSlide(p4, "S19", "Estática, trayectorias y cierre"',
  '{ f: "fotos/b4_paletizado.png", cap: "Paletizado: trayectorias punto a punto con carga", credito: "Foto: CollaborativePalletizer CC BY-SA 4.0 — Wikimedia Commons" }')
foto_seccion("decks_b3b4b5.js", 'sectionSlide(p5, "S20", "Modelado electromecánico"',
  '{ f: "fotos/b1_watt.jpg", cap: "Regulador centrífugo de Watt: el primer lazo realimentado", credito: "Foto: A. Dingley CC BY 3.0 — Wikimedia Commons" }')
foto_seccion("decks_b6b7b8.js", 'sectionSlide(p6, "S25", "Formación de imagen y calibración"',
  '{ f: "fotos/b6_estereo3.jpg", cap: "Cámara estéreo: recuperar la profundidad perdida", credito: "Foto: T. Cognard CC BY-SA 3.0 — Wikimedia Commons" }')
foto_seccion("decks_b6b7b8.js", 'sectionSlide(p6, "S31", "SLAM: del EKF a los grafos"',
  '{ f: "fotos/b6_nube.png", cap: "Nube de puntos LiDAR: la materia prima del mapa", credito: "Foto: D. L. Lu CC BY 4.0 — Wikimedia Commons" }')
foto_seccion("decks_b6b7b8.js", 'sectionSlide(p7, "S32", "Arquitectura de ROS 2"',
  '{ f: "fotos/b7_roomba2.jpg", cap: "Roomba: un grafo de sensores y nodos con ruedas", credito: "Foto: CEphoto, U. Aranas CC BY-SA 4.0 — Wikimedia Commons" }')
foto_seccion("decks_b6b7b8.js", 'sectionSlide(p7, "S37", "MoveIt 2 e integración del stack"',
  '{ f: "fotos/b4_paletizado.png", cap: "Pick and place: la tarea canónica de MoveIt", credito: "Foto: CollaborativePalletizer CC BY-SA 4.0 — Wikimedia Commons" }')
foto_seccion("decks_b6b7b8.js", 'sectionSlide(p8, "S38", "Aprendizaje por refuerzo: MDP y Q-learning"',
  '{ f: "fotos/b8_ajedrez3.jpg", cap: "Decisión secuencial: un brazo industrial juega al ajedrez", credito: "Foto: S. Kazantsev CC BY-SA 4.0 — Wikimedia Commons" }')

# ══ 4. Nuevas diapositivas de fotos ══
def antes_de(f, ancla, bloque):
    i = src[f].find(ancla)
    if i < 0:
        fallos.append(f"{f}: sin ancla {ancla[:60]!r}")
        return
    j = src[f].rfind('\n{', 0, i)
    src[f] = src[f][:j] + '\n' + bloque + src[f][j:]

antes_de("decks.js", 'contentSlide(p1, "El momento «Physical AI»', '''
slideFotos(p1, "El panorama 2026, en imágenes", "S4 · Panorama", [
  { f: "fotos/b1_rover2.jpg", x: 0.7, y: 1.5, w: 5.85, h: 2.5, cap: "Ingenuity, fotografiado por Perseverance: autonomía a 300 millones de km" },
  { f: "fotos/b2_auto.jpg", x: 6.75, y: 1.5, w: 5.85, h: 2.5, cap: "Robotaxi en flota comercial: el robot de servicio ya está en la calle" },
  { f: "fotos/b2_dron.jpg", x: 0.7, y: 4.32, w: 5.85, h: 2.5, cap: "Multirrotor: percepción y control embarcados de serie" },
  { f: "fotos/b7_atlas.jpg", x: 6.75, y: 4.32, w: 5.85, h: 2.5, cap: "Atlas (2013): del DARPA Robotics Challenge a los humanoides industriales" },
], "Fotos: NASA/JPL-Caltech CC BY 2.0 · Dllu CC BY-SA 4.0 · J. Sorenson CC0 · DARPA dominio público — Wikimedia Commons",
"Cuatro imágenes para la conversación del panorama: pedir a la clase que sitúe cada una en la tríada percibir-planificar-actuar y en el espectro de autonomía de S3 antes de pasar a los VLA.");
''')

antes_de("decks.js", 'contentSlide(p2, "AGV frente a AMR', '''
slideFotos(p2, "Robots de servicio, entre personas", "S6 · Servicio", [
  { f: "fotos/b7_roomba2.jpg", x: 0.7, y: 1.5, w: 3.85, h: 4.9, cap: "Roomba: el robot doméstico más vendido de la historia" },
  { f: "fotos/b2_auto.jpg", x: 4.72, y: 1.5, w: 3.85, h: 4.9, cap: "Robotaxi: servicio autónomo en vía pública" },
  { f: "fotos/b8_ajedrez3.jpg", x: 8.74, y: 1.5, w: 3.9, h: 4.9, cap: "Compartir mesa con un brazo industrial: interacción humano-robot" },
], "Fotos: CEphoto, U. Aranas CC BY-SA 4.0 · Dllu CC BY-SA 4.0 · S. Kazantsev CC BY-SA 4.0 — Wikimedia Commons",
"Tres robots de servicio con tres niveles de convivencia con personas: casa, calle y mesa compartida. Con la última, anticipar la pregunta de seguridad que abre S7: ¿qué hace falta para que esto sea seguro?");
''')

antes_de("decks_b3b4b5.js", 'contentSlide(p3, "Hidráulica y neumática"', '''
slideFotos(p3, "Actuadores y transmisiones, de cerca", "S11–S12 · Hardware", [
  { f: "fotos/b3_stepper.jpg", x: 0.7, y: 1.5, w: 3.85, h: 4.9, cap: "Paso a paso NEMA 17: posicionar en lazo abierto contando pasos" },
  { f: "fotos/b3_harmonic.jpg", x: 4.72, y: 1.5, w: 3.85, h: 4.9, cap: "Harmonic drive: la reductora de las articulaciones robóticas" },
  { f: "fotos/b2_cobot3.png", x: 8.74, y: 1.5, w: 3.9, h: 4.9, cap: "UR16e: seis servoaccionamientos con par medido en cada eje" },
], "Fotos: oomlout CC BY-SA 2.0 · wdwd CC BY-SA 4.0 · Auledas CC BY-SA 4.0 — Wikimedia Commons",
"Pasar de la foto al concepto: el paso a paso pierde pasos bajo sobrecarga (lazo abierto), el harmonic drive explica la inercia reflejada dividida por G² y el cobot integra motor, reductora, encoder y medición de par en cada eje.");
''')

# ══ 5. Ecuaciones como imagen y limpieza Unicode ══

# — B1: MDQ —
rep("decks.js", '''  bullets(s, [
    { t: "Índice de diseño I: grado en que un diseño satisface sus especificaciones.", },
    { t: "Aislados, cada subsistema alcanza su óptimo (Iue eléctrico, Ium mecánico); interconectados, ninguno lo alcanza." },
    { t: "Diseño mecatrónico = optimización conjunta:", },
    { t: "Minimizar  J = αe·(Iue − Ie)² + αm·(Ium − Im)²   (ec. 1.2, p. 6)" },
    { t: "…o maximizar  MDQ = (αe·Ie² + αm·Im²) / (αe·Iue² + αm·Ium²)   (ec. 1.4, p. 7; De Silva, 2003)" },
    { t: "Generalizable: fiabilidad, mantenibilidad, eficiencia, coste, tamaño, facilidad de control, inteligencia." },
  ], { w: 6.9 });''', '''  bullets(s, [
    { t: "Índice de diseño I: grado en que un diseño satisface sus especificaciones.", },
    { t: "Aislados, cada subsistema alcanza su óptimo (Iue eléctrico, Ium mecánico); interconectados, ninguno lo alcanza." },
    { t: "Diseño mecatrónico = optimización conjunta: minimizar el coste J o maximizar el MDQ (ecs. 1.2 y 1.4, pp. 6-7; De Silva, 2003):" },
  ], { w: 6.9, h: 2.4 });
  eqImg(s, "mdq_j", 0.95, 4.05, 6.2, 0.52);
  eqImg(s, "mdq", 1.45, 4.85, 5.2, 1.15);
  s.addText("Generalizable: fiabilidad, mantenibilidad, eficiencia, coste, tamaño, facilidad de control, inteligencia.", { x: 0.95, y: 6.25, w: 6.6, h: 0.5, fontFace: "Calibri", fontSize: 11.5, color: GREY, margin: 0 });''')

# — B3: motor DC —
rep("decks_b3b4b5.js", '''  bullets(s, [
    { t: "Modelo completo (De Silva, p. 91)", h: true },
    { t: "Mecánica: I·θ_dd + D·θ_d + τ_carga = τ_M   ·   Eléctrica: Ke·θ_d + La·di/dt + Ra·i = u   ·   Acoplo: τ_M = Kt·i." },
    { t: "Back-EMF: un motor que gira actúa como generador, Vb = Km·ω se opone a la corriente; cuando iguala la tensión del amplificador el par cae a cero — cota de velocidad y amortiguamiento aparente (Corke, p. 346)." },
    { t: "De ahí sale la curva par-velocidad lineal a tensión constante: par máximo a rotor parado, velocidad máxima sin carga." },
    { t: "Simplificación útil: la constante de tiempo eléctrica « la mecánica → se desprecia el transitorio eléctrico." },
    { t: "Fricción real: viscosa B·ω + Coulomb dependiente del signo — reaparecerá como perturbación del control (B5)." },
  ], { w: 7.3, size: 12.5 });''', '''  bullets(s, [
    { t: "Modelo completo (De Silva, p. 91): mecánica, malla eléctrica y acoplo par-corriente", h: true },
    { t: "Back-EMF: un motor que gira actúa como generador, Vb = Km·ω se opone a la corriente; cuando iguala la tensión del amplificador el par cae a cero — cota de velocidad y amortiguamiento aparente (Corke, p. 346)." },
    { t: "De ahí sale la curva par-velocidad lineal a tensión constante: par máximo a rotor parado, velocidad máxima sin carga. Fricción real: viscosa B·ω + Coulomb — perturbación del control (B5)." },
  ], { w: 7.3, size: 12.5, h: 2.9 });
  eqImg(s, "motor3", 1.15, 4.55, 5.0, 1.62);
  s.addText("Simplificación útil: la constante de tiempo eléctrica « la mecánica → se desprecia el transitorio eléctrico.", { x: 0.95, y: 6.4, w: 7.0, h: 0.4, fontFace: "Calibri", fontSize: 11.5, color: GREY, margin: 0 });''')

# — B4: SO(3) —
rep("decks_b3b4b5.js", "R^T·R = I y det R = +1 definen SO(3) (Lynch y Park, p. 70).", "Rᵀ·R = I y det R = +1 definen SO(3) (Lynch y Park, p. 70).")
rep("decks_b3b4b5.js", "La inversa es gratis: R^-1 = R^T (Proposición 3.3).", "La inversa es gratis: R⁻¹ = Rᵀ (Proposición 3.3).")
rep("decks_b3b4b5.js", "notación T_AB; 10-35 matrices de rotación 2D y 3D, R^T·R = I y det R = +1", "notación T_AB; 10-35 matrices de rotación 2D y 3D, Rᵀ·R = I y det R = +1")

# — B4: parametrizaciones —
rep("decks_b3b4b5.js", '''    ["Tres ángulos", "Euler ZYZ: R = Rz(phi)·Ry(theta)·Rz(psi); RPY (Cardan) con secuencia ZYX en vehículos. 12 secuencias posibles. Problema estructural: bloqueo de cardán cuando dos ejes se alinean (pitch = ±90°) — la anécdota del Apolo 13."],
    ["Eje-ángulo", "Girar θ alrededor de un eje unitario w: coordenadas exponenciales. Fórmula de Rodrigues: R = I + sin(θ)·[w] + (1 − cos(θ))·[w]^2, con [w] la matriz antisimétrica de w."],
    ["Cuaterniones unitarios", "4 números y una ligadura; parte vectorial w_hat·sin(θ/2). Componen barato y no tienen singularidad: el estándar en robótica, visión, gráficos y navegación."],
  ];
  cols.forEach((c, i) => card(s, 0.7 + i * 4.05, 1.7, 3.8, 3.6, { title: c[0], body: c[1], num: String(i + 1), bodySize: 11.5, titleSize: 14 }));''', '''    ["Tres ángulos", "Euler ZYZ: R = Rz(φ)·Ry(θ)·Rz(ψ); RPY (Cardan) con secuencia ZYX en vehículos. 12 secuencias posibles. Problema estructural: bloqueo de cardán cuando dos ejes se alinean (pitch = ±90°) — la anécdota del Apolo 13."],
    ["Eje-ángulo", "Girar θ alrededor de un eje unitario ŵ: coordenadas exponenciales, con [ŵ] la matriz antisimétrica de ŵ. Fórmula de Rodrigues:"],
    ["Cuaterniones unitarios", "4 números y una ligadura; parte vectorial ŵ·sin(θ/2). Componen barato y no tienen singularidad: el estándar en robótica, visión, gráficos y navegación."],
  ];
  cols.forEach((c, i) => card(s, 0.7 + i * 4.05, 1.7, 3.8, 3.6, { title: c[0], body: c[1], num: String(i + 1), bodySize: 11.5, titleSize: 14 }));
  eqImg(s, "rodrigues", 4.95, 4.62, 3.4, 0.5);''')

# — B4: SE(3) —
rep("decks_b3b4b5.js", '''  bullets(s, [
    { t: "La transformación homogénea", h: true },
    { t: "T = [R p; 0 1], matriz 4x4 del grupo SE(3): «muy comúnmente usada en robótica, gráficos y visión» (Corke, p. 62)." },
    { t: "Composición: T_AC = T_AB·T_BC. Inversa sin resolver sistemas: T^-1 = [R^T, −R^T·p; 0 1]." },
    { t: "En 2D: SE(2), matrices 3x3 con p homogéneo." },
    { t: "Verificación numérica obligatoria en el taller: T·T^-1 = I." },
  ], { w: 6.0, size: 13 });''', '''  bullets(s, [
    { t: "La transformación homogénea", h: true },
    { t: "Matriz 4x4 del grupo SE(3): «muy comúnmente usada en robótica, gráficos y visión» (Corke, p. 62). En 2D: SE(2), matrices 3x3 con p homogéneo." },
    { t: "Composición por producto; inversa sin resolver sistemas — y verificación numérica obligatoria en el taller: T·T⁻¹ = I." },
  ], { w: 6.0, size: 13, h: 2.3 });
  eqImg(s, "se3_T", 0.85, 4.0, 2.35, 1.0);
  eqImg(s, "t_comp", 3.55, 4.28, 2.9, 0.5);
  eqImg(s, "t_inv", 1.35, 5.25, 4.3, 1.3);''')

# — B4: FK tres convenciones —
rep("decks_b3b4b5.js", '''  card(s, 0.7, 1.6, 11.9, 0.85, {
    title: "",
    body: "FK: «el cálculo de la posición y orientación del marco del efector a partir de sus coordenadas articulares» (Lynch y Park, p. 137). Siempre existe y es única — el problema difícil será el inverso (S16). Ejemplo 2R: x = a1·cos(q0) + a2·cos(q0+q1), y = a1·sin(q0) + a2·sin(q0+q1).",
    fill: "E3F7EC", bodySize: 11.5,
  });''', '''  card(s, 0.7, 1.6, 11.9, 0.8, {
    title: "",
    body: "FK: «el cálculo de la posición y orientación del marco del efector a partir de sus coordenadas articulares» (Lynch y Park, p. 137). Siempre existe y es única — el problema difícil será el inverso (S16). Para el 2R plano:",
    fill: "E3F7EC", bodySize: 11.5,
  });
  eqImg(s, "fk2r", 2.2, 2.52, 8.9, 0.46);''')
rep("decks_b3b4b5.js", '''    ["Denavit-Hartenberg", "4 parámetros por eslabón (theta_j, d_j, a_j, alpha_j) en una tabla compacta: «la manera de compartir modelos desde los años 60». Cada fila = rz ⊕ tz ⊕ tx ⊕ rx. Ojo con la numeración 0/1."],
    ["PoE (Lynch y Park)", "T(q) = e^[S1]q1 · e^[S2]q2 ··· e^[Sn]qn · M\\n\\nM = pose del efector en configuración cero; S_i = eje de husillo de cada articulación. «No hay que definir marcos de eslabón». La base del análisis de velocidad (S17)."],
  ];
  cols.forEach((c, i) => card(s, 0.7 + i * 4.05, 2.65, 3.8, 3.05, { title: c[0], body: c[1], num: String(i + 1), bodySize: 11, titleSize: 13.5 }));''', '''    ["Denavit-Hartenberg", "4 parámetros por eslabón (θⱼ, dⱼ, aⱼ, αⱼ) en una tabla compacta: «la manera de compartir modelos desde los años 60». Cada fila = rz ⊕ tz ⊕ tx ⊕ rx. Ojo con la numeración 0/1."],
    ["PoE (Lynch y Park)", "M = pose del efector en configuración cero; S_i = eje de husillo de la articulación i. «No hay que definir marcos de eslabón». La base del análisis de velocidad (S17):"],
  ];
  cols.forEach((c, i) => card(s, 0.7 + i * 4.05, 3.1, 3.8, 2.72, { title: c[0], body: c[1], num: String(i + 1), bodySize: 11, titleSize: 13.5 }));
  eqImg(s, "poe", 8.95, 5.28, 3.35, 0.42);''')
rep("decks_b3b4b5.js", '''  card(s, 0.7, 5.9, 11.9, 0.85, {
    title: "",
    body: "Ejercicio por parejas: para el 2R, escribir (i) la ETS, (ii) la tabla DH y (iii) M, S1 y S2 del PoE; comprobar que las tres dan la misma T(q) en q = (30°, 40°): t = (1.21, 1.44), orientación 70° (Corke, p. 258).",
    fill: BG_LT, bodySize: 11.5,
  });''', '''  card(s, 0.7, 6.02, 11.9, 0.8, {
    title: "",
    body: "Ejercicio por parejas: para el 2R, escribir (i) la ETS, (ii) la tabla DH y (iii) M, S1 y S2 del PoE; comprobar que las tres dan la misma T(q) en q = (30°, 40°): t = (1.21, 1.44), orientación 70° (Corke, p. 258).",
    fill: BG_LT, bodySize: 11.5,
  });''')

# — B4: jacobiano —
rep("decks_b3b4b5.js", '''  bullets(s, [
    { t: "x_dot = J(q)·q_dot", h: true },
    { t: "«J(q), de dimensión m x n, se llama el jacobiano»: la sensibilidad lineal de la velocidad del efector a la velocidad articular; depende de la configuración q (Lynch y Park, p. 171)." },''', '''  eqImg(s, "jac", 1.0, 1.6, 2.7, 0.72);
  bullets(s, [
    { t: "«J(q), de dimensión m x n, se llama el jacobiano»: la sensibilidad lineal de la velocidad del efector a la velocidad articular; depende de la configuración q (Lynch y Park, p. 171)." },''')
rep("decks_b3b4b5.js", '''    { t: "Jacobiano analítico: expresar la orientación en tasas RPY añade una singularidad de representación — otra vez el coste de los tres ángulos." },
  ], { w: 6.9, size: 13 });''', '''    { t: "Jacobiano analítico: expresar la orientación en tasas RPY añade una singularidad de representación — otra vez el coste de los tres ángulos." },
  ], { y: 2.55, w: 6.9, size: 13, h: 4.3 });''')

# — B4: velocidad resuelta —
rep("decks_b3b4b5.js", '["Velocidad deseada", "nu del efector (6D), p. ej. línea recta a velocidad constante"],', '["Velocidad deseada", "ν del efector (6D), p. ej. línea recta a velocidad constante"],')
rep("decks_b3b4b5.js", '["Invertir J", "q_dot = J^-1(q)·nu en cada instante"],', '["Invertir J", "q̇ = J⁻¹(q)·ν en cada instante"],')
rep("decks_b3b4b5.js", '["Integrar", "q(t+dt) = q(t) + q_dot·dt"],', '["Integrar", "q(t+Δt) = q(t) + q̇·Δt"],')

# — B4: singularidades / Yoshikawa —
rep("decks_b3b4b5.js", '''  card(s, 7.9, 4.7, 4.7, 1.95, {
    title: "Medida de Yoshikawa",
    body: "m(q) = sqrt(det(J·J^T)), proporcional al volumen del elipsoide (método manipulability). Aviso: mide volumen, no isotropía.",
    fill: "E3F7EC", bodySize: 12,
  });''', '''  card(s, 7.9, 4.7, 4.7, 1.95, {
    title: "Medida de Yoshikawa",
    body: "Proporcional al volumen del elipsoide (método manipulability). Aviso: mide volumen, no isotropía.",
    fill: "E3F7EC", bodySize: 11,
  });
  eqImg(s, "yoshikawa", 8.55, 5.85, 3.4, 0.62);''')

# — B4: estática —
rep("decks_b3b4b5.js", '''  bullets(s, [
    { t: "Derivación por conservación de potencia", h: true },
    { t: "f_tip^T·v_tip = tau^T·q_dot; sustituyendo v_tip = J(q)·q_dot y exigiendo validez para todo q_dot: tau = J^T(q)·f_tip (Lynch y Park, p. 175)." },
    { t: "Versión 6D con llaves (wrenches): w = (fx, fy, fz, mx, my, mz) y Q = J^T(q)·w." },
    { t: "«La traspuesta del jacobiano nunca puede ser singular» (Corke, p. 325): la estática funciona incluso donde la cinemática diferencial falla." },
    { t: "Aplicación exprés: par de hombro para sostener 10 N con el brazo extendido → dimensionado de actuadores de B3." },
  ], { w: 6.9, size: 13 });''', '''  bullets(s, [
    { t: "Derivación por conservación de potencia", h: true },
    { t: "La potencia en el efector iguala la articular; exigiendo validez para todo q̇ (Lynch y Park, p. 175):" },
  ], { w: 6.9, size: 13, h: 1.6 });
  eqImg(s, "est_deriv", 0.85, 3.28, 6.6, 0.6);
  bullets(s, [
    { t: "Versión 6D con llaves (wrenches): w = (fx, fy, fz, mx, my, mz) y Q = Jᵀ(q)·w." },
    { t: "«La traspuesta del jacobiano nunca puede ser singular» (Corke, p. 325): la estática funciona incluso donde la cinemática diferencial falla." },
    { t: "Aplicación exprés: par de hombro para sostener 10 N con el brazo extendido → dimensionado de actuadores de B3." },
  ], { y: 4.2, w: 6.9, size: 13, h: 2.5 });''')
rep("decks_b3b4b5.js", 'contentSlide(p4, "Estática: tau = J^T·F y la dualidad", "S19 · Fuerzas sin movimiento")', 'contentSlide(p4, "Estática: τ = Jᵀ·F y la dualidad", "S19 · Fuerzas sin movimiento")')

# — B4: trayectorias —
rep("decks_b3b4b5.js", '["Cúbico", "s(t) = a0 + a1·t + a2·t^2 + a3·t^3 con velocidad nula en los extremos. Defecto: aceleración discontinua en 0 y T — tirones (jerk infinito)."],', '["Cúbico", "s(t) = a₀ + a₁·t + a₂·t² + a₃·t³ con velocidad nula en los extremos. Defecto: aceleración discontinua en 0 y T — tirones (jerk infinito)."],')
rep("decks_b3b4b5.js", "si v^2/a > 1 degenera en triángulo bang-bang", "si v²/a > 1 degenera en triángulo bang-bang")

# — B4: cinco ecuaciones —
rep("decks_b3b4b5.js", '''  const eqs = [
    ["Rotación", "R^T·R = I\\ndet R = +1\\n(SO(3))"],
    ["Pose", "T = [R p; 0 1]\\n(SE(3))"],
    ["FK (PoE)", "T(q) = e^[S1]q1 ···\\ne^[Sn]qn · M"],
    ["Diferencial", "x_dot = J(q)·q_dot"],
    ["Estática", "tau = J^T(q)·F"],
  ];
  eqs.forEach((c, i) => {
    const x = 0.7 + i * 2.5;
    card(s, x, 1.8, 2.25, 2.3, { title: c[0], body: c[1], num: String(i + 1), bodySize: 11.5, titleSize: 13 });
    if (i < 4) arrowR(s, x + 2.22, 2.7, 15);
  });''', '''  const eqs = [
    ["Rotación", "so3", "SO(3)"],
    ["Pose", "se3_T", "SE(3)"],
    ["FK (PoE)", "poe_c", ""],
    ["Diferencial", "jac", ""],
    ["Estática", "estatica", ""],
  ];
  eqs.forEach((c, i) => {
    const x = 0.7 + i * 2.5;
    card(s, x, 1.8, 2.25, 2.3, { title: c[0], body: "", num: String(i + 1), bodySize: 11.5, titleSize: 13 });
    const hq = eqImg(s, c[1], x + 0.14, 2.9, 1.97, 0.85);
    if (c[2]) s.addText(c[2], { x, y: 3.55, w: 2.25, h: 0.3, align: "center", fontFace: "Calibri", fontSize: 10.5, color: GREY, margin: 0 });
    if (i < 4) arrowR(s, x + 2.22, 2.7, 15);
  });''')
rep("decks_b3b4b5.js", "definición de singularidad · Yoshikawa · tau = \n", "definición de singularidad · Yoshikawa · tau = \n", 0) if False else None
rep("decks_b3b4b5.js", "· ocho soluciones IK · definición de singularidad · Yoshikawa · tau = J^T·F · trapezoidal frente a quíntico.", "· ocho soluciones IK · definición de singularidad · Yoshikawa · τ = Jᵀ·F · trapezoidal frente a quíntico.")
rep("decks_b3b4b5.js", '["S19 · vie 23 oct · 2 h", "Estática tau = J^T·F, trayectorias y repaso · cuestionario B4"],', '["S19 · vie 23 oct · 2 h", "Estática τ = Jᵀ·F, trayectorias y repaso · cuestionario B4"],')
rep("decks_b3b4b5.js", '"tau = J^T·F · dualidad fuerza-velocidad · leyes temporales · repaso y cuestionario B4",', '"τ = Jᵀ·F · dualidad fuerza-velocidad · leyes temporales · repaso y cuestionario B4",')
rep("decks_b3b4b5.js", '"x_dot = J(q)·q_dot · columnas con significado · velocidad resuelta",', '"ẋ = J(q)·q̇ · columnas con significado · velocidad resuelta",')

# — B5: motor con carga —
rep("decks_b3b4b5.js", '''  bullets(s, [
    { t: "Las tres ecuaciones del accionamiento", h: true },
    { t: "Acoplo electromecánico: τ = Kt·i (constante de par, N·m/A)." },
    { t: "Malla eléctrica: V = Kt·ω + R·i + L·di/dt — back-EMF, caída resistiva, término inductivo." },
    { t: "Mecánica del conjunto: I·θ_dd + D·θ_d + τ_carga = τ_M." },
    { t: "Reducción a primer orden: la constante de tiempo eléctrica « la mecánica → θ_dd = −(K1/I)·θ_d + (K2/I)·u − (1/I)·τ_carga." },
    { t: "Reductora G: ω ÷G, τ ×η·G; inercia aparente del rotor vista desde la articulación: G²·I_rotor — puede superar la del eslabón." },
  ], { w: 6.9, size: 12.5 });''', '''  bullets(s, [
    { t: "Las tres ecuaciones del accionamiento: acoplo par-corriente, malla eléctrica con back-EMF y mecánica del conjunto", h: true },
  ], { w: 6.9, size: 12.5, h: 0.9 });
  eqImg(s, "motor3", 1.15, 2.5, 4.7, 1.55);
  bullets(s, [
    { t: "Reducción a primer orden: la constante de tiempo eléctrica « la mecánica (Lynch y Park, p. 310):" },
  ], { y: 4.3, w: 6.9, size: 12.5, h: 0.65 });
  eqImg(s, "reduccion", 1.15, 4.98, 4.9, 0.62);
  bullets(s, [
    { t: "Reductora G: ω ÷G, τ ×η·G; inercia aparente del rotor vista desde la articulación: G²·I_rotor — puede superar la del eslabón." },
  ], { y: 5.85, w: 6.9, size: 12.5, h: 1.1 });''')
rep("decks_b3b4b5.js", '''  card(s, 7.9, 1.6, 4.7, 2.7, {
    title: "Función de transferencia",
    body: "Velocidad: Ω(s)/U(s) = K2/(I·s + K1) — primer orden.\\n\\nPosición: Θ(s)/U(s) = K2/(s·(I·s + K1)) — se añade un integrador.",
    bodySize: 12.5,
  });''', '''  card(s, 7.9, 1.6, 4.7, 2.7, { title: "Función de transferencia", body: "", bodySize: 12.5 });
  s.addText("Velocidad — primer orden:", { x: 8.15, y: 2.18, w: 4.2, h: 0.28, fontFace: "Calibri", fontSize: 11.5, color: INK, margin: 0 });
  eqImg(s, "tf_vel", 8.6, 2.48, 2.5, 0.62);
  s.addText("Posición — se añade un integrador:", { x: 8.15, y: 3.28, w: 4.2, h: 0.28, fontFace: "Calibri", fontSize: 11.5, color: INK, margin: 0 });
  eqImg(s, "tf_pos", 8.55, 3.58, 2.6, 0.62);''')

# — B5: analogías —
rep("decks_b3b4b5.js", '''  card(s, 0.7, 1.7, 5.9, 2.15, {
    title: "Mecánico",
    body: "m·x_dd + c·x_d + k·x = F\\n\\nmasa · amortiguador · muelle · fuerza",
    bodySize: 13,
  });
  card(s, 6.85, 1.7, 5.75, 2.15, {
    title: "Eléctrico",
    body: "L·q_dd + R·q_d + q/C = v\\n\\ninductancia · resistencia · 1/capacidad · tensión",
    bodySize: 13,
  });''', '''  card(s, 0.7, 1.7, 5.9, 2.15, { title: "Mecánico", body: "", bodySize: 13 });
  eqImg(s, "analog_mec", 1.55, 2.42, 4.2, 0.58);
  s.addText("masa · amortiguador · muelle · fuerza", { x: 0.92, y: 3.28, w: 5.46, h: 0.3, align: "center", fontFace: "Calibri", fontSize: 11.5, color: GREY, margin: 0 });
  card(s, 6.85, 1.7, 5.75, 2.15, { title: "Eléctrico", body: "", bodySize: 13 });
  eqImg(s, "analog_ele", 7.7, 2.36, 4.05, 0.66);
  s.addText("inductancia · resistencia · 1/capacidad · tensión", { x: 7.07, y: 3.28, w: 5.31, h: 0.3, align: "center", fontFace: "Calibri", fontSize: 11.5, color: GREY, margin: 0 });''')

# — B5: S21 Unicode —
rep("decks_b3b4b5.js", '["Segundo orden", "e_dd + 2ζωn·e_d + ωn²·e = 0 define frecuencia natural ωn y amortiguamiento ζ; sobre-, crítica- o subamortiguado según ζ; ωd = ωn·sqrt(1−ζ²)."],', '["Segundo orden", "ë + 2ζωₙ·ė + ωₙ²·e = 0 define frecuencia natural ωₙ y amortiguamiento ζ; sobre-, crítica- o subamortiguado según ζ; ω_d = ωₙ·√(1−ζ²)."],')
rep("decks_b3b4b5.js", '["Sobreoscilación", "Mp = e^(−πζ/sqrt(1−ζ²))·100 %, pico en tp = π/ωd. Para memorizar: ζ = 0.1 → 73 % · ζ = 0.5 → 16 % · ζ = 0.8 → 1.5 %."],', '["Sobreoscilación", "Mp = e^(−πζ/√(1−ζ²))·100 %, pico en tp = π/ω_d. Para memorizar: ζ = 0.1 → 73 % · ζ = 0.5 → 16 % · ζ = 0.8 → 1.5 %."],')
rep("decks_b3b4b5.js", '["Reglas rápidas", "tr ≈ 1.8/ωn y ts ≈ 4.6/(ζ·ωn).', '["Reglas rápidas", "tr ≈ 1.8/ωₙ y ts ≈ 4.6/(ζ·ωₙ).')

# — B5: PID —
rep("decks_b3b4b5.js", '''  bullets(s, [
    { t: "τ = Kp·e + Ki·∫e·dt + Kd·e_dot", h: true },
    { t: "Kp es «un muelle virtual» y Kd «un amortiguador virtual» (Lynch y Park, pp. 422-423); el PID «sigue ampliamente usado tras más de 70 años» (De Silva, p. 93)." },
    { t: "PD sin gravedad: M·e_dd + (b+Kd)·e_d + Kp·e = 0 → ζ = (b+Kd)/(2·sqrt(Kp·M)), ωn = sqrt(Kp/M): las ganancias colocan ζ y ωn — el puente con S21." },
    { t: "Con gravedad el PD deja error estacionario: sostener el eslabón exige par no nulo, y Kp·θe = m·g·r·cosθ en el reposo." },
    { t: "El término I lo elimina, pero sube el orden a tres y acota Ki: (b+Kd)·Kp/M > Ki > 0. En la práctica, «Ki = 0 en muchos controladores de robots»." },
  ], { w: 7.3, size: 12.5 });''', '''  eqImg(s, "pid", 1.0, 1.62, 3.5, 0.66);
  bullets(s, [
    { t: "Kp es «un muelle virtual» y Kd «un amortiguador virtual» (Lynch y Park, pp. 422-423); el PID «sigue ampliamente usado tras más de 70 años» (De Silva, p. 93)." },
    { t: "PD sin gravedad: M·ë + (b+Kd)·ė + Kp·e = 0 — las ganancias colocan ζ y ωₙ, el puente con S21:" },
  ], { y: 2.5, w: 7.3, size: 12.5, h: 1.8 });
  eqImg(s, "pd_zw", 1.35, 4.35, 3.9, 0.78);
  bullets(s, [
    { t: "Con gravedad el PD deja error estacionario: sostener el eslabón exige par no nulo, y Kp·θe = m·g·r·cosθ en el reposo." },
    { t: "El término I lo elimina, pero sube el orden a tres y acota Ki: (b+Kd)·Kp/M > Ki > 0. En la práctica, «Ki = 0 en muchos controladores de robots»." },
  ], { y: 5.3, w: 7.3, size: 12.5, h: 1.7 });''')
rep("decks_b3b4b5.js", '''  card(s, 8.3, 1.6, 4.3, 3.0, {
    title: "La planta del taller",
    body: "Eslabón en plano vertical: τ = M·θ_dd + m·g·r·cosθ + b·θ_d, con M = 0.5 kg·m², m = 1 kg, r = 0.1 m, b = 0.1 (números del libro, para comparar resultados).",
    bodySize: 12,
  });''', '''  card(s, 8.3, 1.6, 4.3, 3.0, { title: "La planta del taller", body: "", bodySize: 12 });
  eqImg(s, "planta", 8.5, 2.32, 3.9, 0.52);
  s.addText("Eslabón en plano vertical con M = 0.5 kg·m², m = 1 kg, r = 0.1 m, b = 0.1 — números del libro, para comparar resultados.", { x: 8.52, y: 3.05, w: 3.9, h: 1.4, fontFace: "Calibri", fontSize: 11.5, color: INK, margin: 0 });''')

# — B5: espacio de estados —
rep("decks_b3b4b5.js", '''  bullets(s, [
    { t: "x_dot = A·x + B·u,   y = C·x + D·u", h: true },
    { t: "El estado es la memoria mínima del sistema: lo que hay que conocer hoy para predecir mañana dadas las entradas." },
    { t: "El motor DC con x = [θ, ω]: A = [[0, 1], [0, −K1/I]], B = [0, K2/I], C = [1, 0] — el sistema de S20 con otra ropa." },
    { t: "Controlabilidad (Kalman): rank[B, A·B, A²·B, …, A^(n−1)·B] = n. Intuición: B es donde empuja la entrada y A·B adónde se propaga; si esas direcciones no llenan el espacio, hay estados inalcanzables." },
    { t: "Nota para B7: un robot móvil no holonómico no es linealmente controlable y aun así llega a todas partes maniobrando." },
  ], { w: 6.9, size: 12.5 });''', '''  eqImg(s, "ss", 0.95, 1.62, 4.4, 0.55);
  bullets(s, [
    { t: "El estado es la memoria mínima del sistema: lo que hay que conocer hoy para predecir mañana dadas las entradas." },
    { t: "El motor DC con x = [θ, ω]: A = [[0, 1], [0, −K1/I]], B = [0, K2/I], C = [1, 0] — el sistema de S20 con otra ropa." },
    { t: "Controlabilidad: la condición de rango de Kalman (abajo). Intuición: B es donde empuja la entrada y A·B adónde se propaga; si esas direcciones no llenan el espacio, hay estados inalcanzables." },
    { t: "Nota para B7: un robot móvil no holonómico no es linealmente controlable y aun así llega a todas partes maniobrando." },
  ], { y: 2.45, w: 6.9, size: 12.5, h: 3.3 });
  eqImg(s, "kalman", 1.0, 5.95, 5.4, 0.5);''')
rep("decks_b3b4b5.js", '"x_dot = A·x + B·u · controlabilidad de Kalman · u = −K·x · observadores",', '"ẋ = A·x + B·u · controlabilidad de Kalman · u = −K·x · observadores",')

# — B5: ecuación del manipulador —
rep("decks_b3b4b5.js", '''  s.addShape("roundRect", { x: 0.7, y: 1.6, w: 11.9, h: 0.95, rectRadius: 0.08, fill: { color: NAVY }, line: { type: "none" } });
  s.addText([
    { text: "M(q)·q_dd + C(q, q_d)·q_d + g(q) = tau", options: { bold: true, fontSize: 18, color: WHITE } },
    { text: "      lineal en q_dd · cuadrática en q_d · trigonométrica en q", options: { fontSize: 12.5, color: "C9D2F5" } },
  ], { x: 0.95, y: 1.6, w: 11.4, h: 0.95, valign: "middle", fontFace: "Calibri", margin: 0 });''', '''  s.addShape("roundRect", { x: 0.7, y: 1.6, w: 11.9, h: 0.95, rectRadius: 0.08, fill: { color: NAVY }, line: { type: "none" } });
  eqImg(s, "manip", 1.15, 1.83, 5.5, 0.5);
  s.addText("lineal en q̈ · cuadrática en q̇ · trigonométrica en q", { x: 7.1, y: 1.6, w: 5.3, h: 0.95, valign: "middle", fontFace: "Calibri", fontSize: 12.5, color: "C9D2F5", margin: 0 });''')
rep("decks_b3b4b5.js", '["C(q, q_d) — Coriolis", "Términos centrífugos con q_di² y de Coriolis con q_di·q_dj: solo aparecen en movimiento y crecen con la velocidad."],', '["C(q, q̇) — Coriolis", "Términos centrífugos con q̇ᵢ² y de Coriolis con q̇ᵢ·q̇ⱼ: solo aparecen en movimiento y crecen con la velocidad."],')
rep("decks_b3b4b5.js", '''  card(s, 0.7, 5.6, 11.9, 1.05, {
    title: "",
    body: "Receta lagrangiana: coordenadas generalizadas q → L(q, q_d) = K − P → tau = d/dt(∂L/∂q_d) − ∂L/∂q. Versión completa de ingeniería con fricción y fuerza externa: Q = M·q_dd + C·q_d + f(q_d) + g(q) + J^T(q)·w (dinámica inversa; Corke, ec. 9.11).",
    fill: "E3F7EC", bodySize: 11.5,
  });''', '''  card(s, 0.7, 5.6, 6.55, 1.05, {
    title: "",
    body: "Versión completa de ingeniería con fricción y fuerza externa: Q = M·q̈ + C·q̇ + f(q̇) + g(q) + Jᵀ(q)·w (dinámica inversa; Corke, ec. 9.11).",
    fill: "E3F7EC", bodySize: 11.5,
  });
  s.addText("Receta lagrangiana:", { x: 7.5, y: 5.52, w: 2.0, h: 0.3, fontFace: "Calibri", fontSize: 11, color: GREY, margin: 0 });
  eqImg(s, "lagrange", 7.5, 5.84, 4.85, 0.82);''')
rep("decks_b3b4b5.js", '"Euler-Lagrange · M(q)·q_dd + C·q_d + g = tau · control por dinámica inversa · cuestionario B5",', '"Euler-Lagrange · M(q)·q̈ + C·q̇ + g = τ · control por dinámica inversa · cuestionario B5",')

# — B5: par calculado —
rep("decks_b3b4b5.js", '["PID sobre el error", "q_dd_ref = qd_dd + Kp·e + Kd·e_dot + Ki·∫e"],', '["PID sobre el error", "q̈_ref = q̈_d + Kp·e + Kd·ė + Ki·∫e"],')
rep("decks_b3b4b5.js", '["Trayectoria deseada", "qd, qd_dot, qd_dd (B4, S19)"],', '["Trayectoria deseada", "q_d, q̇_d, q̈_d (B4, S19)"],')
rep("decks_b3b4b5.js", '["Modelo inverso", "tau = M_hat(q)·q_dd_ref + h_hat(q, q_d)"],', '["Modelo inverso", "τ = M̂(q)·q̈_ref + ĥ(q, q̇)"],')
rep("decks_b3b4b5.js", '["Robot real", "q y q_d medidos realimentan el lazo"],', '["Robot real", "q y q̇ medidos realimentan el lazo"],')
rep("decks_b3b4b5.js", "Con linealización ideal, la dinámica del error es e_dd + Kv·e_dot + Kp·e = 0:", "Con linealización ideal, la dinámica del error es ë + Kv·ė + Kp·e = 0:")
rep("decks_b3b4b5.js", "PID + compensación de gravedad: tau = Kp·e + Ki·∫e + Kd·e_dot + g_hat(q), suficiente a velocidades pequeñas.", "PID + compensación de gravedad: τ = Kp·e + Ki·∫e + Kd·ė + ĝ(q), suficiente a velocidades pequeñas.")

# — B5: arco —
rep("decks_b3b4b5.js", '["S23", "Estado: x_dot = A·x + B·u, u = −K·x"],', '["S23", "Estado: ẋ = A·x + B·u, u = −K·x"],')
rep("decks_b3b4b5.js", '["S24", "M(q)·q_dd + C·q_d + g = tau y par calculado"],', '["S24", "M(q)·q̈ + C·q̇ + g = τ y par calculado"],')

# — B5: notas con ASCII —
rep("decks_b3b4b5.js", "la receta reproduce f − m·g = m·x_dd.", "la receta reproduce f − m·g = m·ẍ.")
rep("decks_b3b4b5.js", "(par en reposo → gravedad; par con q_d² → centrífugo; acoplo entre ejes → términos no diagonales de M y C).", "(par en reposo → gravedad; par con q̇² → centrífugo; acoplo entre ejes → términos no diagonales de M y C).")

# — B6: pinhole —
rep("decks_b6b7b8.js", '''    { t: "Las coordenadas de imagen resultan de dividir por la profundidad: u = f·X/Z, v = f·Y/Z. Esa división es la fuente de todo lo demás." },
    { t: "Consecuencia central: la proyección pierde la profundidad. Un punto de la imagen corresponde a un rayo completo del espacio, no a un punto." },
    { t: "Recuperar 3D exige información añadida: estéreo, movimiento, un sensor de profundidad o un modelo del objeto." },
  ], { w: 6.7 });''', '''    { t: "Las coordenadas de imagen resultan de dividir por la profundidad — esa división es la fuente de todo lo demás:" },
    { t: "Consecuencia central: la proyección pierde la profundidad. Un punto de la imagen corresponde a un rayo completo del espacio, no a un punto." },
    { t: "Recuperar 3D exige información añadida: estéreo, movimiento, un sensor de profundidad o un modelo del objeto." },
  ], { w: 6.7, h: 4.1 });
  eqImg(s, "pinhole", 1.7, 5.8, 3.1, 0.72);''')

# — B8: Q-learning —
rep("decks_b6b7b8.js", '''    { t: "Q-learning aprende Q sin modelo del mundo: solo con transiciones observadas (s, a, r, s')." },
    { t: "La actualización: Q(s,a) ← Q(s,a) + α·[ r + γ·max_a' Q(s',a') − Q(s,a) ]" },
    { t: "El corchete es el error de diferencia temporal: la sorpresa entre lo que esperaba y lo que la experiencia dice ahora (Sutton y Barto, 2018, cap. 6)." },
  ], { w: 7.2 });''', '''    { t: "Q-learning aprende Q sin modelo del mundo: solo con transiciones observadas (s, a, r, s'). La actualización:" },
    { t: "El corchete es el error de diferencia temporal: la sorpresa entre lo que esperaba y lo que la experiencia dice ahora (Sutton y Barto, 2018, cap. 6)." },
  ], { w: 7.2, h: 3.9 });
  eqImg(s, "qlearn", 0.85, 5.62, 6.9, 0.6);''')

# ══ 6. Limpieza de avisos obvios sobre GIF ══
rep("decks_b3b4b5.js", '"Trayectoria quíntica en espacio articular (GIF: se anima al proyectar)"', '"Trayectoria quíntica en espacio articular: la punta no describe una recta"')
rep("decks_b3b4b5.js", '"El GIF se reproduce en modo presentación de PowerPoint. La elipse achatada', '"La elipse achatada')
rep("decks_b3b4b5.js", '"Barrido de Kp (GIF: se anima al proyectar)"', '"Barrido de Kp: más rápido, pero con más sobreoscilación"')
rep("decks_b6b7b8.js", '"MCL: la nube de partículas converge (GIF, cuaderno S30)"', '"MCL: la nube de partículas converge (cuaderno S30)"')
rep("decks_b6b7b8.js", '"El GIF reproduce la secuencia del pasillo con puertas:', '"La animación reproduce la secuencia del pasillo con puertas:')
rep("decks_b6b7b8.js", '"RRT: las muestras tiran del árbol (GIF, cuaderno S35)"', '"RRT: las muestras tiran del árbol (cuaderno S35)"')
rep("decks_b6b7b8.js", 'el GIF de RRT acompaña la frase de Lynch y Park que cita el guion.', 'la animación de RRT acompaña la frase de Lynch y Park que cita el guion.')
rep("decks_b6b7b8.js", '"Iteración de valor, barrido a barrido (GIF: se anima al proyectar)"', '"Iteración de valor, barrido a barrido: el valor fluye hacia atrás desde la meta"')
rep("decks_b6b7b8.js", "Detener el GIF en el barrido 3", "Detener la animación en el barrido 3")

for f in ARCHIVOS:
    open(f, "w", encoding="utf-8").write(src[f])

if fallos:
    print("FALLOS:")
    for x in fallos: print(" -", x)
    sys.exit(1)
print("edición completada sin fallos")
