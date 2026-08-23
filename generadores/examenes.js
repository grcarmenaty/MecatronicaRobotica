// Genera 18 enunciados de examen (3 exámenes × 6 versiones), 3 documentos de
// corrección con rúbrica, y el banco de preguntas Moodle en docx.
const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, PageBreak, AlignmentType, ImageRun } = require("docx");
const { IQS, F, p, pRuns, h1, h2, h3, bullet, box, tabla, numberingConfig } = require("./lib_iqs");

const D = JSON.parse(fs.readFileSync("examenes_datos.json", "utf-8"));
const LOGO = fs.readFileSync("media/logo_iqs_color.png");
const logoPar = (w = 132, h = 101) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 }, children: [new ImageRun({ type: "png", data: LOGO, transformation: { width: w, height: h } })] });
const BANCO = JSON.parse(fs.readFileSync("banco.json", "utf-8"));

const fx = n => String(n).replace(".", ",");

function docBase(children) {
 return new Document({
 numbering: numberingConfig,
 styles: { default: { document: { run: { font: F, size: 22 } } } },
 sections: [{ properties: { page: { margin: { top: 1200, bottom: 1200, left: 1350, right: 1350 } } }, children }],
 });
}

function cabecera(titulo, version, fecha, dur) {
 return [
 logoPar(),
 pRuns([
 { text: "82514 · Mecatrónica y Robótica · ", size: 26, bold: true, color: IQS.navy },
 { text: titulo, size: 26, bold: true, color: IQS.navy },
 ], { alignment: AlignmentType.CENTER, spacing: { after: 60 } }),
 pRuns([
 { text: `Versión ${version} · ${fecha} · Duración: ${dur}`, size: 22, color: IQS.grey },
 ], { alignment: AlignmentType.CENTER, spacing: { after: 160 } }),
 pRuns([{ text: "Apellidos y nombre: ______________________________________________ DNI: ______________", size: 22 }], { spacing: { after: 160 } }),
 box("Instrucciones", "Puntuación total: 10 puntos. Material permitido: calculadora no programable y una hoja A4 de formulario manuscrito por las dos caras. Parte A (test): cada acierto suma su valor; cada error resta un tercio del valor de la pregunta; en blanco no puntúa; la parte A no puede quedar negativa. En los problemas, indica el planteamiento y las unidades: un resultado sin desarrollo no puntúa. Los errores de arrastre no se penalizan dos veces."),
 p(""),
 ];
}

function parteTest(test, valor) {
 const out = [h2(`Parte A · Test (${fx(valor)} puntos; ${test.length} preguntas)`)];
 out.push(p(`Marca UNA opción por pregunta en la propia hoja. Acierto: +${fx(valor / test.length)} · error: −${fx(Math.round(valor / test.length / 3 * 100) / 100)} · blanco: 0.`, { run: { color: IQS.grey, size: 20 } }));
 test.forEach((q, i) => {
 out.push(pRuns([
 { text: `${i + 1}. `, bold: true },
 { text: q.enun },
 ], { spacing: { before: 120, after: 40 } }));
 "ABCD".split("").forEach((L, j) => {
 out.push(pRuns([{ text: ` ${L}) `, bold: true, size: 21 }, { text: q.ops[j], size: 21 }], { spacing: { after: 20 }, alignment: AlignmentType.LEFT }));
 });
 });
 return out;
}

function rejillaTabla(g) {
 const obs = new Set(g.obs.map(o => o[0] + "," + o[1]));
 const filas = [];
 for (let f_ = 0; f_ < 5; f_++) {
 const fila = [`f=${f_}`];
 for (let c = 0; c < 5; c++) {
 let t = "";
 if (g.S[0] === f_ && g.S[1] === c) t = "S";
 else if (g.G[0] === f_ && g.G[1] === c) t = "G";
 else if (obs.has(f_ + "," + c)) t = "X";
 fila.push(t);
 }
 filas.push(fila);
 }
 return tabla(["", "c=0", "c=1", "c=2", "c=3", "c=4"], filas, [800, 800, 800, 800, 800, 800]);
}

/* ══════════════ ENUNCIADOS ══════════════ */

function enunciadoP1(v) {
 const c = [];
 c.push(...cabecera("Examen Parcial 1 · Bloques 1–4", v.version, "Viernes 6 de noviembre de 2026 (S25)", "2 horas"));
 c.push(...parteTest(v.test, 2.0));
 c.push(new Paragraph({ children: [new PageBreak()] }));

 c.push(h2("Parte B · Diseño mecatrónico e instrumentación (2,0 puntos)"));
 const B = v.B;
 c.push(pRuns([{ text: "B1 (1,0 pt). ", bold: true }, { text: `Debes monitorizar la vibración de un husillo cuya componente dominante está en f = ${B.f} Hz. (a) ¿Qué frecuencia de muestreo mínima exige el teorema de Nyquist? (b) ¿Qué frecuencia usarías en la práctica aplicando el factor 2,56 de los analizadores? (c) Un compañero propone muestrear a ${B.fs_err} Hz «porque es mayor que f»: explica qué ocurrirá y calcula la frecuencia a la que aparecerá la señal observada.` }]));
 c.push(pRuns([{ text: "B2 (1,0 pt). ", bold: true }, { text: `Un diseño mecatrónico interconectado alcanza índices de diseño Ie = ${fx(B.Ie)} (subsistema eléctrico) e Im = ${fx(B.Im)} (mecánico); aislados, sus óptimos serían Iue = ${fx(B.Iue)} e Ium = ${fx(B.Ium)}. Con pesos αe = αm = 1, calcula el MDQ e interpreta el resultado en una frase. ¿Puede el MDQ superar el valor 1 en un diseño real? Justifícalo.` }]));

 c.push(h2("Parte C · Cinemática directa del 2R (3,0 puntos)"));
 const C = v.C;
 c.push(p(`Un manipulador plano de dos eslabones rotativos (2R) tiene longitudes a₁ = ${fx(C.a1)} m y a₂ = ${fx(C.a2)} m. Los ángulos articulares q₁ y q₂ se miden en sentido antihorario; q₂ es relativo al primer eslabón.`));
 c.push(pRuns([{ text: "C1 (1,0 pt). ", bold: true }, { text: `Para q = (${C.q1}°, ${C.q2}°), calcula la posición (x, y) del efector y su orientación φ respecto al eje x.` }]));
 c.push(pRuns([{ text: "C2 (1,0 pt). ", bold: true }, { text: "Escribe la tabla de parámetros de Denavit-Hartenberg (θ, d, a, α) del robot." }]));
 c.push(pRuns([{ text: "C3 (1,0 pt). ", bold: true }, { text: `Determina el espacio de trabajo alcanzable (radio interior y exterior) y razona si el punto Pf = (${fx(C.Pfuera[0])}, ${fx(C.Pfuera[1])}) m es alcanzable.` }]));

 c.push(h2("Parte D · Cinemática inversa, jacobiano y estática (3,0 puntos)"));
 const Dd = v.Dd;
 c.push(pRuns([{ text: "D1 (1,25 pt). ", bold: true }, { text: `Calcula las dos soluciones de la cinemática inversa (codo arriba y codo abajo) para el punto P = (${fx(Dd.P[0])}, ${fx(Dd.P[1])}) m, usando la ley de los cosenos y atan2. Da q₁ y q₂ en grados.` }]));
 c.push(pRuns([{ text: "D2 (0,75 pt). ", bold: true }, { text: "Escribe el jacobiano J(q) del 2R para la rama de q₂ positivo del apartado anterior y calcula su determinante. ¿En qué configuraciones es singular el robot y qué significa físicamente?" }]));
 c.push(pRuns([{ text: "D3 (1,0 pt). ", bold: true }, { text: `En esa misma configuración, el efector debe ejercer la fuerza F = (${Dd.F[0]}, ${Dd.F[1]}) N sobre el entorno. Calcula los pares articulares mediante τ = Jᵀ(q)·F.` }]));
 return c;
}

function enunciadoP2(v) {
 const c = [];
 c.push(...cabecera("Examen Parcial 2 · Bloques 5–7", v.version, "Viernes 11 de diciembre de 2026 (S40)", "2 horas"));
 c.push(...parteTest(v.test, 2.0));
 c.push(new Paragraph({ children: [new PageBreak()] }));

 const B = v.B;
 c.push(h2("Parte B · Control de una articulación (3,0 puntos)"));
 c.push(p(`Una articulación con la gravedad compensada responde a M·θ̈ + b·θ̇ = τ, con M = ${fx(B.M)} kg·m² y b = ${fx(B.b)} N·m·s/rad.`));
 c.push(pRuns([{ text: "B1 (1,0 pt). ", bold: true }, { text: `Diseña un controlador PD, τ = Kp·e + Kd·ė, para que el lazo cerrado tenga amortiguamiento ζ = ${fx(B.zeta)} y frecuencia natural ωₙ = ${fx(B.wn)} rad/s.` }]));
 c.push(pRuns([{ text: "B2 (0,75 pt). ", bold: true }, { text: "¿Qué sobreoscilación Mp predice ese amortiguamiento ante un escalón? Da el valor en % y la fórmula empleada." }]));
 c.push(pRuns([{ text: "B3 (0,75 pt). ", bold: true }, { text: `Si en realidad actúa además el par de gravedad m·g·r·cosθ con m = ${fx(B.m)} kg y r = ${fx(B.r)} m, calcula el error estacionario que deja el PD al regular en θd = 0 (usa cosθ ≈ 1 y g = 9,81 m/s²). ¿Qué término del PID lo elimina y qué nuevo problema introduce ese término?` }]));
 c.push(pRuns([{ text: "B4 (0,5 pt). ", bold: true }, { text: "El actuador satura en τmax. Explica qué es el windup del integrador, por qué aparece con la saturación y un remedio práctico." }]));

 const C = v.C;
 c.push(h2("Parte C · Estimación con filtro de Kalman (2,5 puntos)"));
 c.push(p(`Un filtro de Kalman 1D sigue un estado con modelo de paseo aleatorio (predicción: la media no cambia y la covarianza crece con Q). Estado actual: media = ${fx(C.x0)}, covarianza P = ${fx(C.P0)}. Ruido de proceso Q = ${fx(C.Q)}; ruido de medida R = ${fx(C.R)}. Llega la medida z = ${fx(C.z)}.`));
 c.push(pRuns([{ text: "C1 (1,5 pt). ", bold: true }, { text: "Calcula la covarianza predicha, la ganancia de Kalman K, la media corregida y la covarianza posterior." }]));
 c.push(pRuns([{ text: "C2 (0,5 pt). ", bold: true }, { text: "Sin recalcular: si R fuera diez veces mayor, ¿hacia dónde se movería la estimación corregida y por qué?" }]));
 c.push(pRuns([{ text: "C3 (0,5 pt). ", bold: true }, { text: "¿Por qué la localización global (pose inicial desconocida) exige un filtro de partículas y no basta un EKF?" }]));

 const g = v.Dd;
 c.push(h2("Parte D · Planificación y ROS 2 (2,5 puntos)"));
 c.push(p(`La rejilla 5×5 siguiente usa coordenadas (fila f, columna c); X marca celda ocupada. Un planificador A* 4-conectado (coste 1 por paso, heurística Manhattan) parte de S = (${g.S[0]}, ${g.S[1]}) hacia G = (${g.G[0]}, ${g.G[1]}).`));
 c.push(rejillaTabla(g));
 c.push(p(""));
 c.push(pRuns([{ text: "D1 (1,5 pt). ", bold: true }, { text: "Calcula h(S); para cada vecino libre de S, su f = g + h; indica qué celda expande primero A*, y la longitud (en pasos) del camino óptimo." }]));
 c.push(pRuns([{ text: "D2 (0,5 pt). ", bold: true }, { text: "Si la heurística sobreestimara el coste restante, ¿A* seguiría garantizando el óptimo? Justifica con el concepto de admisibilidad." }]));
 c.push(pRuns([{ text: "D3 (0,5 pt). ", bold: true }, { text: "En el taller, un LiDAR publica a 40 Hz pero al suscriptor «no le llega nada». Da las dos causas de QoS más probables y cómo las corregirías." }]));
 return c;
}

function enunciadoF(v) {
 const c = [];
 c.push(...cabecera("Examen Final · Bloques 1–8", v.version, "Convocatoria de enero de 2027", "3 horas"));
 c.push(...parteTest(v.test, 2.4));
 c.push(new Paragraph({ children: [new PageBreak()] }));

 c.push(h2("Parte B · Seguridad y normativa (1,6 puntos)"));
 c.push(p(`Caso: ${v.caso}`));
 c.push(pRuns([{ text: "B1 (0,6 pt). ", bold: true }, { text: "¿Qué método (o combinación) de operación colaborativa de la ISO 10218:2025 propondrías para esta aplicación? Justifica la elección frente a las alternativas." }]));
 c.push(pRuns([{ text: "B2 (0,6 pt). ", bold: true }, { text: "Identifica tres peligros relevantes; al menos uno debe corresponder a un modo degradado (limpieza, mantenimiento, recuperación de fallos)." }]));
 c.push(pRuns([{ text: "B3 (0,4 pt). ", bold: true }, { text: "Propón una medida de reducción del riesgo por cada nivel de la jerarquía (eliminar por diseño → proteger → informar), en ese orden." }]));

 const C = v.C;
 c.push(h2("Parte C · Cinemática y control (3,0 puntos)"));
 c.push(p(`Un manipulador plano 2R tiene a₁ = ${fx(C.a1)} m y a₂ = ${fx(C.a2)} m.`));
 c.push(pRuns([{ text: "C1 (1,0 pt). ", bold: true }, { text: `Para q = (${C.q1}°, ${C.q2}°), calcula la posición (x, y) del efector y su orientación φ.` }]));
 c.push(pRuns([{ text: "C2 (1,0 pt). ", bold: true }, { text: "Escribe el jacobiano J(q) en esa configuración, calcula su determinante e indica las configuraciones singulares del robot." }]));
 c.push(pRuns([{ text: "C3 (1,0 pt). ", bold: true }, { text: `Una articulación equivalente con la gravedad compensada responde a M·θ̈ + b·θ̇ = τ, con M = ${fx(C.M)} kg·m² y b = ${fx(C.b)} N·m·s/rad. Diseña un PD para ζ = ${fx(C.zeta)} y ωₙ = ${fx(C.wn)} rad/s.` }]));

 const dd = v.Dd;
 c.push(h2("Parte D · Estimación probabilística (1,5 puntos)"));
 c.push(p(`Un robot debe estimar si una puerta está abierta o cerrada. Creencia inicial: p(abierta) = 0,5. El sensor devuelve «abierta» con probabilidad ${fx(dd.hit)} si la puerta está realmente abierta, y con probabilidad ${fx(dd.fa)} si está cerrada (falsa alarma).`));
 c.push(pRuns([{ text: "D1 (1,0 pt). ", bold: true }, { text: "El sensor devuelve «abierta». Calcula la creencia posterior con la regla de Bayes. El sensor vuelve a devolver «abierta»: calcula la nueva creencia." }]));
 c.push(pRuns([{ text: "D2 (0,5 pt). ", bold: true }, { text: "¿Qué hipótesis (de Markov) sobre las medidas estás usando al encadenar las dos actualizaciones?" }]));

 const E = v.E;
 c.push(h2("Parte E · Aprendizaje por refuerzo y planificación (1,5 puntos)"));
 c.push(pRuns([{ text: "E1 (1,0 pt). ", bold: true }, { text: `Un agente de Q-learning tiene Q(s, a) = ${fx(E.Q)}. Ejecuta a, recibe r = ${fx(E.r)} y llega a s' donde max Q(s', a') = ${fx(E.maxQ)}. Con γ = ${fx(E.g)} y α = ${fx(E.a)}, calcula el error de diferencia temporal y el nuevo Q(s, a).` }]));
 c.push(pRuns([{ text: "E2 (0,5 pt). ", bold: true }, { text: "Explica en dos frases por qué el behavior cloning (imitación pura) falla cuando el robot se aleja de los estados demostrados, y qué familia de métodos lo mitiga." }]));
 return c;
}

/* ══════════════ CORRECCIONES ══════════════ */

function tablaTest(v, n) {
 const filas = [];
 for (let i = 0; i < n; i++) filas.push([String(i + 1), v.test[i].corr]);
 return tabla(["Pregunta", "Correcta"], filas, [1200, 1200]);
}

function rubricaComun(nombre, filas) {
 return [
 h1(`Rúbrica de corrección · ${nombre}`),
 p("Criterios generales: el planteamiento correcto (modelo, fórmula o método adecuado) vale el 40 % de cada apartado; el desarrollo coherente, el 30 %; el resultado numérico correcto con unidades, el 30 % restante. Un resultado sin desarrollo no puntúa. Los errores de arrastre no se penalizan dos veces: si un apartado usa un valor erróneo anterior con método correcto, puntúa completo. Resultados sin unidades: −10 % del apartado. Parte A (test): cada error resta un tercio del valor de la pregunta; la parte no puede quedar negativa."),
 tabla(["Apartado", "Puntos", "Qué se puntúa", "Errores frecuentes (descuento orientativo)"], filas, [1050, 850, 3600, 3860]),
 p(""),
 ];
}

function correccionP1() {
 const c = [];
 c.push(logoPar());
 c.push(pRuns([{ text: "82514 · Corrección y rúbrica · Examen Parcial 1 (B1–B4) · 6 versiones", size: 28, bold: true, color: IQS.navy }], { alignment: AlignmentType.CENTER, spacing: { after: 200 } }));
 c.push(...rubricaComun("Parcial 1", [
 ["A (test)", "2,0", "10 preguntas · 0,20 por acierto, −0,07 por error", "-"],
 ["B1", "1,0", "(a) fs ≥ 2f (0,3) · (b) 2,56·f (0,3) · (c) explicar aliasing irreversible y calcular |fs−f| (0,4)", "Decir que basta fs > f (−0,4); creer que un filtro digital posterior lo arregla (−0,2)"],
 ["B2", "1,0", "Fórmula del MDQ como cociente (0,4) · cálculo (0,3) · interpretación y cota MDQ ≤ 1 con motivo (0,3)", "Usar suma en vez de cociente (−0,4); afirmar que puede superar 1 porque los aislados son óptimos (−0,3)"],
 ["C1", "1,0", "x, y por suma de proyecciones (0,7) · φ = q1+q2 (0,3)", "Olvidar que q₂ es relativo (−0,3); grados/radianes mezclados (−0,3)"],
 ["C2", "1,0", "Tabla DH 2 filas: θi variable, d = 0, a = ai, α = 0 (1,0)", "Poner a en la columna d (−0,3); añadir filas de herramienta no pedidas (0)"],
 ["C3", "1,0", "Anillo [|a1−a2|, a1+a2] (0,6) · comprobación del punto con su radio (0,4)", "Dar solo el radio exterior (−0,4)"],
 ["D1", "1,25", "cos q₂ por ley de cosenos (0,5) · dos ramas ±q2 (0,25) · q1 con atan2 en ambas (0,5)", "atan(y/x) sin cuadrante (−0,25); una sola rama (−0,35)"],
 ["D2", "0,75", "J correcto (0,4) · det J = a₁·a₂·sin q₂ (0,2) · singular en q₂ = 0, ±180° con lectura física (0,15)", "Confundir singularidad con límite articular (−0,2)"],
 ["D3", "1,0", "τ = Jᵀ·F con la traspuesta (0,4) · producto correcto con signos (0,4) · unidades N·m (0,2)", "Usar J en lugar de Jᵀ (−0,4)"],
 ]));
 for (const v of D.P1) {
 c.push(new Paragraph({ children: [new PageBreak()] }));
 c.push(h1(`Solución · Versión ${v.version}`));
 c.push(h3("Parte A, Test"));
 c.push(tablaTest(v, 10));
 const B = v.B, C = v.C, dd = v.Dd;
 c.push(h3("Parte B"));
 c.push(p(`B1: (a) fs,min = 2·${B.f} = ${B.fs_min} Hz. (b) fs,práctica = 2,56·${B.f} ≈ ${B.fs_prac} Hz. (c) A ${B.fs_err} Hz se viola Nyquist: la señal aparece como alias en |${B.fs_err} − ${B.f}| = ${B.alias} Hz, y ningún filtrado digital posterior puede deshacerlo.`));
 c.push(p(`B2: MDQ = (Ie² + Im²)/(Iue² + Ium²) = (${fx(B.Ie)}² + ${fx(B.Im)}²)/(${fx(B.Iue)}² + ${fx(B.Ium)}²) = ${fx(B.mdq)}. El conjunto interconectado alcanza el ${fx(Math.round(B.mdq * 1000) / 10)} % del ideal de los subsistemas aislados. No puede superar 1: interconectados, los subsistemas no pueden rendir por encima de su óptimo aislado (Ie ≤ Iue, Im ≤ Ium).`));
 c.push(h3("Parte C"));
 c.push(p(`C1: x = a₁·cos q₁ + a₂·cos(q₁+q₂) = ${fx(C.x)} m; y = a₁·sin q₁ + a₂·sin(q₁+q₂) = ${fx(C.y)} m; φ = q₁ + q₂ = ${C.phi}°.`));
 c.push(p(`C2: DH del 2R, fila 1: θ₁ = q₁ (variable), d1 = 0, a₁ = ${fx(C.a1)}, α₁ = 0; fila 2: θ₂ = q₂ (variable), d2 = 0, a₂ = ${fx(C.a2)}, α₂ = 0.`));
 c.push(p(`C3: anillo con rint = |a₁ − a₂| = ${fx(C.rmin)} m y rext = a1 + a₂ = ${fx(C.rmax)} m. Para Pf: ‖Pf‖ = ${fx(C.rPf)} m → ${C.alcanzable ? "alcanzable (dentro del anillo)" : "NO alcanzable (fuera del anillo)"}.`));
 c.push(h3("Parte D"));
 c.push(p(`D1: cos q₂ = (x² + y² − a₁² − a₂²)/(2·a₁·a₂) = ${fx(dd.c2)} → q₂ = ±${fx(dd.q2a)}°. Rama q2 positivo: q₁ = ${fx(dd.q1a)}°; rama q2 negativo: q₁ = ${fx(dd.q1b)}°. (Comprobación: la FK de ambas devuelve P.)`));
 c.push(p(`D2: J = [[${fx(dd.J[0][0])}, ${fx(dd.J[0][1])}], [${fx(dd.J[1][0])}, ${fx(dd.J[1][1])}]] (fila 1: ∂x/∂q; fila 2: ∂y/∂q). det J = a₁·a₂·sin q₂ = ${fx(dd.detJ)} m². Singular en q₂ = 0° o ±180° (brazo estirado o plegado): se pierde la capacidad de moverse en la dirección radial.`));
 c.push(p(`D3: τ = Jᵀ·F = (${fx(dd.tau[0])}, ${fx(dd.tau[1])}) N·m para F = (${dd.F[0]}, ${dd.F[1]}) N.`));
 }
 return c;
}

function correccionP2() {
 const c = [];
 c.push(logoPar());
 c.push(pRuns([{ text: "82514 · Corrección y rúbrica · Examen Parcial 2 (B5–B7) · 6 versiones", size: 28, bold: true, color: IQS.navy }], { alignment: AlignmentType.CENTER, spacing: { after: 200 } }));
 c.push(...rubricaComun("Parcial 2", [
 ["A (test)", "2,0", "10 preguntas · 0,20 por acierto, −0,07 por error", "-"],
 ["B1", "1,0", "Ecuación de lazo cerrado M·s²+(b+Kd)·s+Kp (0,4) · Kp = M·ωₙ² (0,3) · Kd = 2ζωₙ·M − b (0,3)", "Olvidar restar b en Kd (−0,25); identificar mal el polinomio característico (−0,4)"],
 ["B2", "0,75", "Fórmula Mp = e^(−πζ/√(1−ζ²)) (0,4) · valor en % (0,35)", "Confundir Mp con el valor de pico absoluto (−0,3)"],
 ["B3", "0,75", "Equilibrio Kp·e = m·g·r (0,35) · valor en rad o grados (0,2) · término I y su coste (orden 3, cotas de Ki / windup) (0,2)", "No linealizar cosθ ≈ 1 (−0,1); omitir el problema que introduce I (−0,2)"],
 ["B4", "0,5", "Windup: integral acumulando bajo saturación → sobreoscilación (0,3) · un remedio: integración condicional o límite del integrador (0,2)", "-"],
 ["C1", "1,5", "P⁻ = P+Q (0,4) · K = P⁻/(P⁻+R) (0,4) · media corregida (0,4) · P⁺ = (1−K)·P⁻ (0,3)", "Intercambiar Q y R (−0,5); K fuera de [0,1] sin detectar el error (−0,3)"],
 ["C2", "0,5", "Con R×10, K baja → la estimación se queda cerca de la predicción (0,5)", "-"],
 ["C3", "0,5", "Una gaussiana es unimodal; la localización global exige creencias multimodales → partículas (0,5)", "-"],
 ["D1", "1,5", "h(S) Manhattan (0,3) · f de cada vecino libre (0,6) · celda expandida (0,3) · longitud óptima (0,3)", "Contar diagonales en 4-conectada (−0,4); h desde G en vez de hasta G (−0,3)"],
 ["D2", "0,5", "No: sin admisibilidad (h puede sobreestimar) se pierde la garantía de optimalidad (0,5)", "-"],
 ["D3", "0,5", "QoS incompatible (reliable/best effort) y ROS_DOMAIN_ID / descubrimiento (0,5); remedio: alinear perfiles, aislar dominios", "-"],
 ]));
 for (const v of D.P2) {
 c.push(new Paragraph({ children: [new PageBreak()] }));
 c.push(h1(`Solución · Versión ${v.version}`));
 c.push(h3("Parte A, Test"));
 c.push(tablaTest(v, 10));
 const B = v.B, C = v.C, g = v.Dd;
 c.push(h3("Parte B"));
 c.push(p(`B1: lazo cerrado M·s² + (b + Kd)·s + Kp. Igualando a s² + 2ζωn·s + ωn²: Kp = M·ωₙ² = ${fx(B.Kp)} N·m/rad; Kd = 2ζωₙ·M − b = ${fx(B.Kd)} N·m·s/rad.`));
 c.push(p(`B2: Mp = e^(−πζ/√(1−ζ²)) = ${fx(B.Mp)} %.`));
 c.push(p(`B3: en equilibrio Kp·e = m·g·r → e = ${fx(B.m)}·9,81·${fx(B.r)}/${fx(B.Kp)} = ${fx(B.ess_rad)} rad = ${fx(B.ess_deg)}°. Lo elimina el término integral; a cambio sube el orden a tres (acota Ki) y trae el riesgo de windup con saturación.`));
 c.push(p("B4: con el actuador saturado, el integrador sigue acumulando error; al llegar al objetivo ese exceso «tarda en desenrollarse» y produce gran sobreoscilación y establecimiento largo. Remedios: integración condicional (congelar I mientras satura) o límite duro del integrador."));
 c.push(h3("Parte C"));
 c.push(p(`C1: P⁻ = P + Q = ${fx(C.Pm)}; K = P⁻/(P⁻ + R) = ${fx(C.K)}; media corregida = ${fx(C.x0)} + K·(${fx(C.z)} − ${fx(C.x0)}) = ${fx(C.xh)}; P⁺ = (1 − K)·P⁻ = ${fx(C.Pp)}.`));
 c.push(p("C2: con R diez veces mayor, K cae → el filtro confía menos en la medida y la estimación se queda cerca de la predicción (la media apenas se mueve)."));
 c.push(p("C3: la creencia de la localización global es multimodal («uno de estos pasillos idénticos») y una gaussiana (EKF) es unimodal por construcción; el filtro de partículas representa esa multimodalidad con muestras."));
 c.push(h3("Parte D"));
 const vec = g.vecinos.map(w => `(${w.celda[0]},${w.celda[1]}): f = 1 + ${w.h} = ${w.f}`).join(" · ");
 c.push(p(`D1: h(S) = ${g.hS}. Vecinos libres de S: ${vec}. Expande primero: ${g.expandir.map(e => `(${e[0]},${e[1]})`).join(" o ")} (mínima f; empate válido). Longitud óptima: ${g.lopt} pasos.`));
 c.push(p("D2: no. La garantía de optimalidad exige heurística admisible (que nunca sobreestime); si sobreestima, A* puede cerrar la meta por un camino subóptimo."));
 c.push(p("D3: (1) perfiles de QoS incompatibles entre publicador y suscriptor (reliable frente a best effort): alinearlos; (2) dominios distintos o descubrimiento roto (ROS_DOMAIN_ID diferente): unificar el dominio. Diagnóstico con ros2 topic info --verbose."));
 }
 return c;
}

function correccionF() {
 const c = [];
 c.push(logoPar());
 c.push(pRuns([{ text: "82514 · Corrección y rúbrica · Examen Final (B1–B8) · 6 versiones", size: 28, bold: true, color: IQS.navy }], { alignment: AlignmentType.CENTER, spacing: { after: 200 } }));
 c.push(...rubricaComun("Final", [
 ["A (test)", "2,4", "12 preguntas · 0,20 por acierto, −0,07 por error", "-"],
 ["B1", "0,6", "Método adecuado al caso y justificación frente a alternativas (0,6)", "Elegir «cobot» como si fuera un método (−0,3): los métodos son parada monitorizada, guiado manual, velocidad y separación, y limitación de potencia y fuerza"],
 ["B2", "0,6", "Tres peligros pertinentes, al menos uno de modo degradado (0,2 cada uno)", "Tres variantes del mismo peligro (máx. 0,2)"],
 ["B3", "0,4", "Una medida por nivel, en el orden de la jerarquía (0,4)", "Empezar por señalización/formación (−0,2)"],
 ["C1", "1,0", "x, y (0,7) · φ (0,3)", "Grados/radianes mezclados (−0,3)"],
 ["C2", "1,0", "J correcto (0,5) · det (0,25) · singularidades q₂ = 0, ±180° (0,25)", "Usar Jᵀ como J (−0,3)"],
 ["C3", "1,0", "Kp = M·ωₙ² (0,5) · Kd = 2ζωₙ·M − b (0,5)", "Olvidar b (−0,25)"],
 ["D1", "1,0", "Posterior 1 con Bayes y normalización (0,6) · posterior 2 encadenada (0,4)", "No normalizar (−0,4)"],
 ["D2", "0,5", "Independencia condicional de las medidas dado el estado (Markov de medida) (0,5)", "-"],
 ["E1", "1,0", "TD = r + γ·maxQ' − Q (0,6) · Qnuevo = Q + α·TD (0,4)", "Olvidar restar Q en el TD (−0,4)"],
 ["E2", "0,5", "Deriva por errores compuestos fuera de la distribución demostrada (0,3) · mitigación: DAgger / diffusion policies / más demostraciones (0,2)", "-"],
 ]));
 for (const v of D.F) {
 c.push(new Paragraph({ children: [new PageBreak()] }));
 c.push(h1(`Solución · Versión ${v.version}`));
 c.push(h3("Parte A, Test"));
 c.push(tablaTest(v, 12));
 c.push(h3("Parte B (orientación de corrección)"));
 c.push(p(`Caso: ${v.caso}`));
 c.push(p("B1: se valora el ajuste método-caso. Interacción esporádica con célula rápida → parada monitorizada de seguridad o velocidad y separación; contacto frecuente o mesa compartida → limitación de potencia y fuerza (con umbrales de la ISO/TS 15066); tránsito de personas/vehículos → velocidad y separación con escáneres certificados; combinaciones bien justificadas puntúan completo. B2: tres peligros distintos y pertinentes (atrapamiento, golpe, herramienta, caída de carga, arranque inesperado…), con al menos un modo degradado. B3: una medida por nivel en orden: diseño (eliminar el solape persona-robot, limitar velocidad/fuerza por diseño), protección (escáner, resguardo, parada segura), información (señalización, formación, procedimiento)."));
 const C = v.C, dd = v.Dd, E = v.E;
 c.push(h3("Parte C"));
 c.push(p(`C1: x = ${fx(C.x)} m; y = ${fx(C.y)} m; φ = ${C.phi}°.`));
 c.push(p(`C2: J = [[${fx(C.J[0][0])}, ${fx(C.J[0][1])}], [${fx(C.J[1][0])}, ${fx(C.J[1][1])}]]; det J = a₁·a₂·sin q₂ = ${fx(C.detJ)} m². Singular en q₂ = 0° o ±180°.`));
 c.push(p(`C3: Kp = M·ωₙ² = ${fx(C.Kp)} N·m/rad; Kd = 2ζωₙ·M − b = ${fx(C.Kd)} N·m·s/rad.`));
 c.push(h3("Parte D"));
 c.push(p(`D1: posterior1 = ${fx(dd.hit)}·0,5 / (${fx(dd.hit)}·0,5 + ${fx(dd.fa)}·0,5) = ${fx(dd.post1)}. Segunda medida igual: posterior2 = ${fx(dd.hit)}·${fx(dd.post1)} / (${fx(dd.hit)}·${fx(dd.post1)} + ${fx(dd.fa)}·(1 − ${fx(dd.post1)})) = ${fx(dd.post2)}.`));
 c.push(p("D2: la hipótesis de Markov de la medida: cada observación depende solo del estado actual, de modo que las medidas son condicionalmente independientes dado el estado y pueden encadenarse multiplicando verosimilitudes."));
 c.push(h3("Parte E"));
 c.push(p(`E1: TD = r + γ·maxQ' − Q = ${fx(E.r)} + ${fx(E.g)}·${fx(E.maxQ)} − ${fx(E.Q)} = ${fx(E.td)}; Qnuevo = ${fx(E.Q)} + ${fx(E.a)}·${fx(E.td)} = ${fx(E.Qn)}.`));
 c.push(p("E2: al desviarse de las trayectorias demostradas el robot entra en estados sin datos, comete errores que lo alejan más (errores compuestos) y la política diverge; lo mitigan DAgger (agregar correcciones), más cobertura de demostraciones o políticas generativas (diffusion policies)."));
 }
 return c;
}

/* ══════════════ BANCO DOCX ══════════════ */
function bancoDocx() {
 const c = [];
 c.push(logoPar());
 c.push(pRuns([{ text: "82514 · Banco de preguntas Moodle · Cuestionarios de bloque (15 min)", size: 28, bold: true, color: IQS.navy }], { alignment: AlignmentType.CENTER, spacing: { after: 120 } }));
 c.push(p("Ocho bancos de 12 preguntas ABCD, uno por bloque. Configuración recomendada del cuestionario en Moodle: 10 preguntas aleatorias del banco del bloque, 15 minutos, un intento, orden de preguntas y de opciones barajado por Moodle, revisión tras el cierre. La opción correcta aparece aquí siempre como A), Moodle baraja las opciones al presentar; los ficheros .gift.txt de la carpeta moodle se importan directamente (Banco de preguntas → Importar → formato GIFT)."));
 for (let b = 1; b <= 8; b++) {
 c.push(new Paragraph({ children: [new PageBreak()] }));
 c.push(h1(`Bloque ${b}, 12 preguntas`));
 BANCO[String(b)].forEach((q, i) => {
 c.push(pRuns([{ text: `B${b}-${String(i + 1).padStart(2, "0")}. `, bold: true }, { text: q[0] }], { spacing: { before: 140, after: 40 } }));
 "ABCD".split("").forEach((L, j) => {
 c.push(pRuns([
 { text: ` ${L}) `, bold: true, size: 21, color: j === q[2] ? IQS.greenDark : "000000" },
 { text: q[1][j], size: 21, color: j === q[2] ? IQS.greenDark : "000000", bold: j === q[2] },
 ], { spacing: { after: 20 }, alignment: AlignmentType.LEFT }));
 });
 c.push(pRuns([{ text: " Retroalimentación: ", bold: true, size: 20, color: IQS.grey }, { text: q[3], size: 20, color: IQS.grey }], { spacing: { after: 60 }, alignment: AlignmentType.LEFT }));
 });
 }
 return c;
}

/* ══════════════ ESCRITURA ══════════════ */
const trabajos = [];
for (const v of D.P1) trabajos.push([`Examen_82514_Parcial1_v${v.version}.docx`, enunciadoP1(v)]);
for (const v of D.P2) trabajos.push([`Examen_82514_Parcial2_v${v.version}.docx`, enunciadoP2(v)]);
for (const v of D.F) trabajos.push([`Examen_82514_Final_v${v.version}.docx`, enunciadoF(v)]);
trabajos.push(["Correccion_82514_Parcial1.docx", correccionP1()]);
trabajos.push(["Correccion_82514_Parcial2.docx", correccionP2()]);
trabajos.push(["Correccion_82514_Final.docx", correccionF()]);
trabajos.push(["Banco_Preguntas_Moodle_82514.docx", bancoDocx()]);

(async () => {
 for (const [nombre, children] of trabajos) {
 const buf = await Packer.toBuffer(docBase(children));
 fs.writeFileSync("examenes/" + nombre, buf);
 console.log("OK", nombre);
 }
})();
