#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Notación limpia en los decks (subíndices reales, sin T_AB), logo IQS en portadas
y referencia al cuaderno del taller S13."""
import sys
fallos = []
def carga(f): return open(f, encoding="utf-8").read()
def guarda(f, s): open(f, "w", encoding="utf-8").write(s)
def rep(src, viejo, nuevo, ctx, n=1):
    c = src.count(viejo)
    if c != n:
        fallos.append(f"{ctx}: esperaba {n}, hay {c}: {viejo[:70]!r}")
        return src
    return src.replace(viejo, nuevo)

ARCH = ["decks.js", "decks_b3b4b5.js", "decks_b6b7b8.js"]

# ── 1. bullets() con soporte de runs (subíndices) ──
B_VIEJO = '''function bullets(s, items, { x = 0.7, y = 1.6, w = 6.0, h = 5.3, size = 14 } = {}) {
  const arr = [];
  items.forEach((it, i) => {
    if (it.h) arr.push({ text: it.t, options: { bold: true, color: NAVY, fontSize: size + 1, bullet: false, paraSpaceAfter: 4, breakLine: true } });
    else arr.push({ text: it.t, options: { bullet: { code: "2022", indent: 14 }, color: INK, fontSize: size, paraSpaceAfter: 8, breakLine: i < items.length - 1 } });
  });
  s.addText(arr, { x, y, w, h, fontFace: "Calibri", valign: "top", margin: 0 });
}'''
B_NUEVO = '''function bullets(s, items, { x = 0.7, y = 1.6, w = 6.0, h = 5.3, size = 14 } = {}) {
  const arr = [];
  items.forEach((it, i) => {
    const fin = i < items.length - 1;
    if (it.h) arr.push({ text: it.t, options: { bold: true, color: NAVY, fontSize: size + 1, bullet: false, paraSpaceAfter: 4, breakLine: true } });
    else if (it.r) it.r.forEach((sg, j) => arr.push({ text: sg.t, options: { bullet: j === 0 ? { code: "2022", indent: 14 } : false, color: INK, fontSize: size, subscript: !!sg.sub, paraSpaceAfter: 8, breakLine: j === it.r.length - 1 ? fin : false } }));
    else arr.push({ text: it.t, options: { bullet: { code: "2022", indent: 14 }, color: INK, fontSize: size, paraSpaceAfter: 8, breakLine: fin } });
  });
  s.addText(arr, { x, y, w, h, fontFace: "Calibri", valign: "top", margin: 0 });
}'''
for f in ARCH:
    s = carga(f)
    s = rep(s, B_VIEJO, B_NUEVO, f + " bullets rich")
    guarda(f, s)

# ── 2. Logo IQS real en las portadas de los 3 generadores ──
LOGO_VIEJO = '''  s.addText("IQS", { x: 0.7, y: 0.5, w: 1.6, h: 0.8, fontFace: "Arial", fontSize: 40, bold: true, color: WHITE, margin: 0 });
  s.addShape("rect", { x: 0.7, y: 1.28, w: 1.6, h: 0.26, fill: { color: GREEN }, line: { type: "none" } });
  s.addText("UNIVERSITAT RAMON LLULL", { x: 0.7, y: 1.3, w: 3.5, h: 0.24, fontFace: "Arial", fontSize: 8, bold: true, color: NAVY, margin: 0.04 });'''
LOGO_NUEVO = '''  s.addImage({ path: MEDIA + "logo_iqs_blanco.png", x: 0.7, y: 0.42, w: 1.3, h: 1.3 });'''
for f in ARCH:
    s = carga(f)
    s = rep(s, LOGO_VIEJO, LOGO_NUEVO, f + " logo")
    guarda(f, s)

# ── 3. decks_b3b4b5: notación ──
s = carga("decks_b3b4b5.js")
s = rep(s, 'body: "fs ≥ 2·f_señal para evitar el aliasing;',
        'body: [{ text: "f" }, { text: "s", options: { subscript: true } }, { text: " ≥ 2·f" }, { text: "señal", options: { subscript: true } }, { text: " para evitar el aliasing;' , "fs nyquist")
s = rep(s, ' los analizadores usan factor 2,56. Pregunta: ¿qué pasa si muestreo una vibración de 400 Hz a 500 Hz? Ningún filtro digital posterior deshace un aliasing ya cometido.",',
        ' los analizadores usan factor 2,56. Pregunta: ¿qué pasa si muestreo una vibración de 400 Hz a 500 Hz? Ningún filtro digital posterior deshace un aliasing ya cometido." }],', "fs nyquist cierre")
s = rep(s, 'body: "Modelo de error de cada canal: x_medido = s·x + b + ε. El bias b deriva',
        'body: "Modelo de error de cada canal: la lectura vale s·x + b + ε. El bias b deriva', "x_medido")
s = rep(s, '«cualquier pose es siempre una pose relativa» (Corke p. 26), notación T_AB; 10-35',
        '«cualquier pose es siempre una pose relativa» (Corke p. 26), notación de subíndices origen-destino; 10-35', "seg S13")
s = rep(s, '''    { t: "A cada cuerpo se une rígidamente un marco dextrógiro; T_AB = pose de {B} respecto de {A}; el marco de referencia es {0} o {W}." },''',
        '''    { r: [{ t: "A cada cuerpo se une rígidamente un marco dextrógiro; T" }, { t: "AB", sub: true }, { t: " es la pose de {B} respecto de {A}; el marco de referencia es {0} o {W}." }] },''', "bullet T_AB")
s = rep(s, '''    body: "T_AC = T_AB · T_BC: el subíndice interior «se cancela». Regla mecánica que evita el 80 % de los errores de orden del taller.",''',
        '''    body: [{ text: "T" }, { text: "AC", options: { subscript: true } }, { text: " = T" }, { text: "AB", options: { subscript: true } }, { text: " · T" }, { text: "BC", options: { subscript: true } }, { text: ": el subíndice interior «se cancela». Regla mecánica que evita el 80 % de los errores de orden del taller." }],''', "card subindices")
s = rep(s, '''    ["PoE (Lynch y Park)", "M = pose del efector en configuración cero; S_i = eje de husillo de la articulación i. «No hay que definir marcos de eslabón». La base del análisis de velocidad (S17):"],''',
        '''    ["PoE (Lynch y Park)", [{ text: "M = pose del efector en configuración cero; S" }, { text: "i", options: { subscript: true } }, { text: " = eje de husillo de la articulación i. «No hay que definir marcos de eslabón». La base del análisis de velocidad (S17):" }]],''', "PoE S_i")
s = rep(s, "bucle que integra q con el q_dot del jacobiano", "bucle que integra q con la velocidad articular que da el jacobiano", "nota q_dot")
s = rep(s, '''    { t: "Reductora G: ω ÷G, τ ×η·G; inercia aparente del rotor vista desde la articulación: G²·I_rotor — puede superar la del eslabón." },''',
        '''    { r: [{ t: "Reductora G: ω ÷G, τ ×η·G; inercia aparente del rotor vista desde la articulación: G²·I" }, { t: "rotor", sub: true }, { t: ", que puede superar la del eslabón." }] },''', "I_rotor")
s = rep(s, '''    ["Segundo orden", "ë + 2ζωₙ·ė + ωₙ²·e = 0 define frecuencia natural ωₙ y amortiguamiento ζ; sobre-, crítica- o subamortiguado según ζ; ω_d = ωₙ·√(1−ζ²)."],''',
        '''    ["Segundo orden", [{ text: "ë + 2ζωₙ·ė + ωₙ²·e = 0 define frecuencia natural ωₙ y amortiguamiento ζ; sobre-, crítica- o subamortiguado según ζ; ω" }, { text: "d", options: { subscript: true } }, { text: " = ωₙ·√(1−ζ²)." }]],''', "omega_d 1")
s = rep(s, '''    ["Sobreoscilación", "Mp = e^(−πζ/√(1−ζ²))·100 %, pico en tp = π/ω_d. Para memorizar: ζ = 0.1 → 73 % · ζ = 0.5 → 16 % · ζ = 0.8 → 1.5 %."],''',
        '''    ["Sobreoscilación", [{ text: "Mp = e^(−πζ/√(1−ζ²))·100 %, pico en tp = π/ω" }, { text: "d", options: { subscript: true } }, { text: ". Para memorizar: ζ = 0.1 → 73 % · ζ = 0.5 → 16 % · ζ = 0.8 → 1.5 %." }]],''', "omega_d 2")
s = rep(s, "eslabón en plano vertical, τ = M·θ_dd + m·g·r·cosθ + b·θ_d con los números del libro",
        "eslabón en plano vertical, τ = M·θ̈ + m·g·r·cosθ + b·θ̇ con los números del libro", "seg S22")
s = rep(s, '''    ["Saturación", "τ_max = 1.5 N·m: aparece el windup"],''',
        '''    ["Saturación", [{ text: "τ" }, { text: "max", options: { subscript: true } }, { text: " = 1.5 N·m: aparece el windup" }]],''', "tau_max")
# cuaderno S13 en el taller de spatialmath
s = rep(s, 'title: "Taller con spatialmath-python",', 'title: "Taller con spatialmath-python · cuaderno 82514_S13",', "titulo taller S13")
s = rep(s, 'body: "Cadena mundo → mesa → pieza → cámara: calcular la pose de la pieza vista desde la cámara componiendo e invirtiendo transformaciones.",',
        'body: "Cadena mundo → mesa → pieza → cámara: calcular la pose de la pieza componiendo e invirtiendo transformaciones. Guiado paso a paso, con soluciones, en el cuaderno 82514_S13_Pose_Rotaciones.",', "ejercicio guiado S13")
guarda("decks_b3b4b5.js", s)

# ── 4. decks_b6b7b8: notación ──
s = carga("decks_b6b7b8.js")
s = rep(s, 'body: "El robot no conoce su estado: mantiene una distribución de probabilidad sobre él, la creencia bel(x_t), condicionada',
        'body: "El robot no conoce su estado: mantiene una distribución de probabilidad sobre él (la creencia), condicionada', "bel x_t")
s = rep(s, '''    { t: "El problema se plantea en el espacio de configuraciones: hallar un camino en C_free desde la configuración inicial a la meta (Lynch y Park, 2017, p. 353)." },''',
        '''    { r: [{ t: "El problema se plantea en el espacio de configuraciones: hallar un camino en C" }, { t: "libre", sub: true }, { t: " desde la configuración inicial a la meta (Lynch y Park, 2017, p. 353)." }] },''', "C_free")
guarda("decks_b6b7b8.js", s)

# ── 5. apuntes: notación residual ──
s = carga("apuntes_b4.js")
s = rep(s, "notación T_AB: pose de {B} respecto de {A}.", "notación de subíndices origen-destino: la pose de {B} respecto de {A} lleva los subíndices AB.", "ap4 1")
s = rep(s, "«T_AB se denomina transformación homogénea», miembro de SE(2)", "«la matriz de la pose relativa se denomina transformación homogénea», miembro de SE(2)", "ap4 2")
s = rep(s, "composición T_AC = T_AB·T_BC, inversa T^-1 = [R^T, −R^T·p; 0 1]; insistir en leer los subíndices",
        "composición encadenando subíndices (AC = AB por BC), inversa con la traspuesta; insistir en leer los subíndices", "ap4 3")
s = s.replace("p_A = T_AB·p", "el punto en {A} es la transformación por el punto en {B}: p")  # línea 85 aproximada
s = s.replace("T_AC = T_AB·T_BC", "la de A a C es el producto de la de A a B por la de B a C")
s = s.replace("T^-1 = [R^T, −R^T·p; 0 1]", "T⁻¹ = [Rᵀ, −Rᵀ·p; 0 1]")
guarda("apuntes_b4.js", s)

s = carga("apuntes_b6.js")
s = s.replace("f/ρ_w y f/ρ_h", "f/ρw y f/ρh").replace("(u_0, v_0)", "(u₀, v₀)")
guarda("apuntes_b6.js", s)

# ── 6. examenes.js: subíndices Unicode en enunciados ──
s = carga("examenes.js")
for viejo, nuevo in [("a1 = ", "a₁ = "), ("a2 = ", "a₂ = "), ("(a1 + a2", "(a₁ + a₂"), ("|a1 − a2|", "|a₁ − a₂|"),
                     ("q1 y q2", "q₁ y q₂"), ("q2 es relativo", "q₂ es relativo"), ("Da q1 y q2 en grados", "Da q₁ y q₂ en grados"),
                     ("rama de q2 positivo", "rama de q₂ positivo"), ("ωn = ", "ωₙ = "), ("y ωn.", "y ωₙ."),
                     ("ζ y frecuencia natural ωn", "ζ y frecuencia natural ωₙ"), ("Kp = M·ωn²", "Kp = M·ωₙ²"),
                     ("Kd = 2ζωn·M − b", "Kd = 2ζωₙ·M − b"), ("θ1 = q1", "θ₁ = q₁"), ("θ2 = q2", "θ₂ = q₂"),
                     ("d1 = 0, a1 = ", "d₁ = 0, a₁ = "), ("d2 = 0, a2 = ", "d₂ = 0, a₂ = "), ("α1 = 0", "α₁ = 0"), ("α2 = 0", "α₂ = 0"),
                     ("q2 = ±", "q₂ = ±"), ("q1 = ", "q₁ = "), ("sin q2", "sin q₂"), ("cos q2", "cos q₂"),
                     ("q2 = 0° o ±180°", "q₂ = 0° o ±180°"), ("q2 = 0, ±180°", "q₂ = 0, ±180°"),
                     ("a1·cos q1 + a2·cos(q1+q2)", "a₁·cos q₁ + a₂·cos(q₁+q₂)"), ("a1·sin q1 + a2·sin(q1+q2)", "a₁·sin q₁ + a₂·sin(q₁+q₂)"),
                     ("a1·a2·sin", "a₁·a₂·sin"), ("(x² + y² − a1² − a2²)/(2·a1·a2)", "(x² + y² − a₁² − a₂²)/(2·a₁·a₂)"),
                     ("φ = q1 + q2", "φ = q₁ + q₂"), ("rint = |a1 − a2|", "rint = |a₁ − a₂|"), ("rext = a1 + a2", "rext = a₁ + a₂")]:
    s = s.replace(viejo, nuevo)
guarda("examenes.js", s)

if fallos:
    print("FALLOS:")
    for x in fallos: print(" -", x)
    sys.exit(1)
print("notación y logos aplicados")
