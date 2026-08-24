# Informe de verificación independiente · 82514 Mecatrónica y Robótica

Verificación integral del material docente realizada el 23-24 de agosto de 2026 en la rama
`claude/verify-teaching-materials-7mpq8x`. Las fuentes de contraste fueron las extracciones
de los cinco libros de la carpeta de Drive `Mecatronica/Fuentes` (con un índice de página
impresa reconstruido localmente, página a página) y los artículos de `Fuentes citadas`.
Las correcciones se aplicaron siempre por partida doble: en el generador y en el entregable,
con los PDF regenerados y el paginado verificado contra el original.

## 1. Qué se verificó y con qué método

| Área | Método | Resultado |
|---|---|---|
| Ejecución de los 29 cuadernos | nbclient, ejecución completa celda a celda | **29/29 sin errores**, reverificado tras cada corrección |
| Soluciones numéricas de los 18 exámenes | Recomputación independiente desde los enunciados (numpy) | **~340 valores comprobados** contra las 3 correcciones: todos cuadran |
| Problemas A* del Parcial 2 | Rejillas parseadas de las tablas reales de los docx + A* propio | h(S), f de vecinos y longitud óptima correctos en las 6 versiones |
| Claves del test | Triple cruce docx examen ↔ corrección ↔ examenes_datos.json | 0 discrepancias; la opción marcada es idéntica entre versiones |
| Banco Moodle (96 GIFT) | Validación sintáctica + cruce con el Banco docx | Sintaxis correcta; 1 correcta + 3 distractores + feedback en las 96 |
| Calendario del plan 2026-27 | Las 43 fechas contra el calendario real | Días de semana, festivos (11-S, 24-S), sin huecos, 57 h: todo cuadra |
| Citas con página (1746 extraídas de apuntes, cuadernos, presentaciones y guía) | Anclajes automáticos + índice de página impresa + corroboración + verificación semántica con lectura de la página citada | Ver §3 |
| Contenido de preguntas (92 de examen + 96 GIFT) | Revisión experta por lotes | 2 errores (corregidos) y ~15 matices, ver §4 y §6 |
| IDs de arXiv | Consulta de arxiv.org/abs de los 21+1 identificadores | Todos corresponden al artículo, autor y año declarados |
| Atribuciones de imágenes | Cruce decks ↔ atribuciones.json ↔ pies de diapositiva | 34/34 fotos con atribución registrada y crédito visible |
| Terminología (Convención del curso) | Barrido de variantes desaconsejadas en todo el material | Ver §2 |

Nota sobre las fuentes: en los PDF de Corke, las páginas en blanco de los saltos de capítulo
desvían el desplazamiento lineal hasta +2 páginas a partir de la p. ~305 (ficheros rvc3_p04,
p05 y p07). Cualquier verificación por offset fijo en ese rango necesita el índice de número
impreso; el `verificar.py` del curso ya lo usaba, así que sus conclusiones siguen en pie.

## 2. Terminología: corregido

La pasada de corrección terminológica documentada en la Convención (llave→torsor,
eje de husillo→helicoidal, clonado→clonación, celda→célula) **se había aplicado a docx y
pptx pero no a los cuadernos**. Corregido ahora en cuaderno + generador:

* S14: «eje/ejes/movimiento de husillo» → «helicoidal» (7).
* S19: «llave / llaves de fuerza» → «torsor(es) (wrench)» con concordancia (4).
* S40, notas del orador de B8 y gd_b8.js: «clonado de comportamiento» → «clonación» (5).
* S21, S22, guía del profesor y un resto en apuntes B5: «sobreimpulso» → «sobreoscilación»
  (33, ajustando adjetivos: «medida», «parásita», «exacta»…; en S21 se renombró el
  identificador Python `sobreimpulso_teorico` → `sobreoscilacion_teorica`).
* Apuntes B8: «**el** clonación» → «**la** clonación» (concordancia que dejó la pasada previa).
* Apuntes B4: «**una** torsor aplic**ada**» → «**un** torsor aplic**ado**» (ídem).
* S24 y apuntes B5: «centrífugos» → «centrípetos» en las citas y paráfrasis de Lynch y Park
  (el original dice *centripetal*); se conserva «fuerzas centrífugas» donde describe la
  carga mecánica real del rotor.

Quedan como **decisión del autor** (no corregido):
* «retroalimentación» aparece en sentido pedagógico (feedback a estudiantes en B8/Tareas y
  el campo estándar de Moodle en el Banco) y en el feedback de las acciones de ROS 2 (B7);
  el control usa siempre «realimentación». Si se quiere unificar también el sentido ROS 2,
  son 4 apariciones (examen Final vE, Parcial 2 vF, GIFT B7, diapositiva B7).
* «feedforward de velocidad» en el guion de S11 y apdo. 11.3 de B3 (la convención pide
  «prealimentación (feedforward)» en primera aparición).
* Los cuadernos y su LEEME usan em dashes con normalidad, mientras el README declara que
  «todo el material evita el em dash»; también los usan los tres documentos de referencia.
  O se ajusta el README (el criterio aplica a docx/pptx) o se limpian los cuadernos.
* «variables “de puerto”» en apuntes B1 para las *across variables* de De Silva: traducción
  discutible («variables transversales» sería más fiel).

## 3. Citas: resultado y correcciones

De las **1746 citas con página** extraídas de los entregables finales (apuntes 1178,
cuadernos 408, presentaciones 133, guía 27), la pasada automática de anclajes confirmó el
71 % y la corroboración por página compartida otro 16 %. Los 654 casos restantes más
todas las citas textuales y con datos numéricos (incluida una muestra de control de 80
confirmadas) pasaron a verificación semántica con lectura de la página citada. Esa pasada
se completó al 100 %: **652 ítems verificados uno a uno, 611 correctas (93,7 %), 38
imprecisas (5,8 %: página vecina o matiz) y 3 incorrectas (0,5 %)**. Ninguna de las
imprecisiones apuntaba a un libro equivocado: todas eran desplazamientos de una o dos
páginas, o afirmaciones propias del curso que la cita hacía parecer del libro.

Corregido (generador + entregable + PDF):

| Dónde | Antes | Ahora | Motivo |
|---|---|---|---|
| Apuntes B1 (paletizado) | Corke p. 3 | p. 4 | la frase está en la p. 4 |
| Apuntes B1 (extero/propioceptivo) | Corke p. 8 | pp. 8-9 | los ejemplos citados están en la 9 |
| Apuntes B1 («servidumbre») | Corke p. 2 | pp. 2-3 | la palabra cae al inicio de la 3 |
| Apuntes B2 (clasificación funcional) | Corke pp. 4-5 | pp. 4-7 | fabricación/servicio/campo llegan a la 7 |
| Apuntes B3 (G del PUMA) | Corke p. 341 | pp. 339-341 | el principio está en 339-340 |
| Apuntes B4 (cuaterniones) | Corke p. 59 | pp. 59-60 | el dato de coste está en la 60 |
| Apuntes B4 y S16 (atan2, 3 sitios) | L&P p. 220 y ss. | p. 219 y ss. | la regla del cuadrante está en la 219 |
| Apuntes B4 (IRB140 «de ABB») | Corke p. 277 | pp. 277 y 301 | la atribución a ABB está en la 301 |
| Apuntes B4 (columnas colineales, 3 sitios) | L&P p. 173 | p. 172 | la afirmación exacta está en la 172 |
| Apuntes B6 (ganancia de Kalman, quote) | Thrun p. 42 | p. 43 | el pasaje está en la 43 |
| Apuntes B6 y S29 (cita de Cox 1991, 3 sitios) | Thrun p. 219 | p. 233 | el quote está en 7.10, p. 233 |
| Apuntes B7 (PRM pasajes estrechos) | Corke p. 187 | pp. 187-188 | el modo de fallo está en la 188 |
| S17 (columnas colineales) | L&P p. 173 | p. 172 | la afirmación exacta está en la 172 |
| S29 (seguimiento de posición) | Thrun p. 194 | pp. 193-194 | «pose inicial conocida» cierra la 193 |
| S29 (h(x) rango-rumbo) | Corke p. 220 | p. 219 | la ec. 6.9 está impresa en la 219 |
| S26 (blobs y descriptores) | Corke pp. 502-504 | pp. 499-504 | la extracción por blob empieza en la 499 |
| S24 y B5 (Coriolis/centrípetos) | «centrífugos» | «centrípetos» | fidelidad al original *centripetal* |
| Diapositiva 5 de B5 (constantes de tiempo) | L&P p. 310 | De Silva p. 91 | la afirmación es de De Silva |
| Diapositiva 5 de B5 (física→EDO, pie) | Corke pp. 346-348 | pp. 334-341 | el modelado está en 9.1 |
| Diapositiva 18 de B5 (dinámica inversa) | Corke p. 359 | pp. 359-360 | la ec. 9.17 está en la 360 |
| Diapositiva 6 de B4 (parametrizaciones) | L&P pp. 77-84 | ap. B, pp. 575-582 | Euler/rpy/cuaterniones están en el apéndice B |
| Diapositiva 10 de B1 (MDQ) | «pp. 6-7; De Silva, 2003» | «De Silva et al., 2016, pp. 6-7» | las páginas son de la ed. 2016 |
| Diapositiva 12 de B8 (gemelo digital) | De Silva p. 7 | p. 8 | la p. 7 es la formulación del MDQ |

Señalado sin corregir (defendible o requiere decisión del autor):
* Apuntes B4 (Corke p. 267): la causa «casi siempre» de los desajustes toolbox-controlador
  es formulación propia que la cita hace parecer del libro.
* S20: el valor `Ke = 0.060 V·s/rad` es un parámetro elegido por el curso junto a la cita
  de L&P p. 308 (que define la constante, no el valor); bastaría un «(valor del curso)».
* Apuntes B6 (Corke pp. 546-547) y B6 p. 472 (FastSLAM), S30 p. 98: matices menores donde
  la página citada cubre el grueso de la afirmación.
* Diapositiva 15 de B4: el dato «ocho soluciones» no está en L&P pp. 220-225 (L&P da cuatro
  de posición), pero el pie de la misma diapositiva ya cita Corke pp. 281-282, donde sí está.

## 4. Exámenes y banco de preguntas: corregido

* **Final, 6 versiones**: la línea de instrucciones decía «Acierto: +0,19999999999999998»
  (2,4/12 sin redondear). Corregido a «+0,2» y arreglada la función `fx` de `examenes.js`.
* **Pregunta del bias inercial** (P1 vD q6, GIFT B3-08, banco): decía «bias de un
  giróscopo… al integrar dos veces, el error crece cuadráticamente». La doble integración
  con crecimiento cuadrático corresponde al **acelerómetro** (el bias del giróscopo se
  integra una vez y da deriva lineal de actitud, exactamente lo que enseña el propio S09).
  Corregido el enunciado a «bias de un acelerómetro» en toda la cadena.
* **Pregunta de estática** (P1 vE q9, GIFT B4-12, banco): la opción correcta afirmaba «la
  traspuesta del jacobiano nunca puede ser singular» (frase heredada de Corke p. 325, pero
  falsa como enunciado matemático: rank Jᵀ = rank J). Reescrita como «no requiere invertir
  el jacobiano: la estática sigue definida incluso en singularidades». En apuntes B4 y S19
  la frase se conserva porque es cita literal de Corke, y el propio texto la explica bien.

## 5. Erratas y datos factuales: corregido

* «Yasakawa» → «Yaskawa» (3, apuntes B1). Cóctel Devol-Engelberger: 1954 → **1956** (2;
  1954 es la patente). R.U.R.: «estrenada en 1920» → «publicada en 1920 y estrenada en 1921».
  A*: «se publicó en 1966» → **1968** (2, apuntes B7; Hart, Nilsson y Raphael, IEEE Trans. SSC).
* «y I-um» → «e Ium»; duplicación «a la vez… a la vez»; asignación del debate de S4
  reescrita a «la posición contraria a la que ha votado» (coherente con su propia consigna).
* B2: «mientras el espacio de trabajo «la decide…»» → «mientras **la del** espacio de
  trabajo «la decide…»» (antecedente claro). B3: «el doble de la **del** señal» → «de la señal».
* B4: «la torsor aplicada / se exprese la torsor / si la torsor» → masculino (7 en total con
  las de §2). B5: «colación de ecuaciones» → «**colección**» (dentro de una cita traducida).
* B6: «calidad **estatal** del arte» → «de estado del arte» (calco de *state-of-the-art*);
  «la mejor de **las** siete minutos» → «los»; «resume **tres** milenios» → «cuatro» (la cita
  que sigue habla de hace 4000 años); «qué **le** preguntaríais a los autores» → «les» (2, B6 y B8).
* B8: «la ecuación del **MDQ**» → «**MDP**» (gazapo en la lista de lo que entra en el examen);
  «grupos **frías**» → «fríos»; «**una** comodín» → «un comodín».
* S09: «un cuento» → «una cuenta» (2). S13: «componer **e** invertir»; «Dos **ternas** de
  ángulos» (el print comparaba ternas rpy, no parejas).
* S19: tiempo mínimo por aceleración de la solución del ejercicio 2, 2,4495 → **2,4028 s**
  (√(10/√3), no √6). S21: la regla 4,6/(ζ·ωn) es la banda del **1 %**, no del 2 % (e^−4,6 ≈ 0,010).
* S27: **bug real de código**: `aprender_nucleo` medía el acierto contra la variable global
  `PIEZAS` en lugar del parámetro `objetivo`, de modo que el ejercicio 2 (aprender otro
  objetivo) no medía lo que decía medir. Corregido y el cuaderno reejecutado.
* Bibliografía: `gitignore.txt` renombrado a `.gitignore` (no estaba activo); añadido
  arXiv **2503.20020 (Gemini Robotics)** a `lista.txt` (el cuaderno de descarga ya lo
  incluía) y corregido el Checklist, que afirmaba que ese informe no tenía identificador
  de arXiv. Nota: YOLO (1506.02640) es v1 de 2015 y el curso lo data 2016 (CVPR): correcto
  como fecha de publicación.

## 6. Señalado para decisión del autor (no corregido)

Preguntas de test cuyo enunciado es defendible pero matizable (redacciones sugeridas en
las notas del repositorio de verificación):
* «**La** condición» de IK cerrada del 6R = muñeca esférica (B4-08 y P1): es condición
  suficiente, no necesaria (Pieper; los UR con tres ejes paralelos también tienen IK cerrada;
  el propio guion de S16 la llama «condición necesaria», que convendría rebajar a «suficiente»).
* «transformador ideal» para v·i = ω·τ (B1-06): en grafos de enlace ese acoplamiento es un
  girador; «convertidor ideal» evitaría la reclamación.
* «la ISO/TS 15066 **sigue siendo la** referencia» (B2-11) y «responsabilidad **legal**»
  (B2-09): matizables tras la ISO 10218:2025.
* Convolución = «la misma operación» que una capa CNN (B6-04): estrictamente correlación
  cruzada; «esencialmente la misma» lo blinda.
* Nodo ROS 2 = «proceso independiente» (B7-01): la composición de nodos rompe la
  equivalencia estricta. QoS incompatible «sin error visible» (B7-04): desde Galactic hay
  warning por defecto. MoveIt «sin planning scene no hay comprobación de colisiones»
  (B7-12): las autocolisiones se comprueban siempre.

Hallazgos técnicos de la revisión de cuadernos y apuntes que implican reescribir texto
didáctico (se listan con su corrección propuesta; no se han tocado para no alterar
decisiones pedagógicas):
* S08 (solución ej. 1): el residuo de la recta terminal es ~1,5× el de mínimos cuadrados
  con esta parábola (|c|L²/4 frente a ~|c|L²/6); el «doble» corresponde a la recta minimax.
* S09 (solución ej. 1): el umbral de saltos con FS = 4000 Hz es ~12,6 rad/s según la propia
  fórmula, no «unos 6». (ej. 3): el enunciado anuncia «desplazamiento contrario» pero la
  solución (correcta) dice que el óptimo se mueve en el mismo sentido. (ej. 2): la deriva
  residual simulada es ~0,5°, no «unos pocos grados», y el bias simulado es constante.
* S11: «el pico de corriente solo aparece en el modelo completo» está contradicho por su
  propia simulación (el reducido arranca en u/Ra = 12 A > pico real 11,29 A); «sin back-EMF
  la corriente sería infinita» debería ser «quedaría en la de bloqueo u/Ra».
* S12 (solución ej. 3): con los datos nuevos la ventana de G se estrecha a ≈64-101 pero no
  «se cierra» (G = 100 de la tabla sigue siendo válida). El texto del apartado paralelo en
  apuntes B3 arrastra lo mismo, más el «óptimo ~420» que con Jl = 3 y Jm = 1e-4 es √30000 ≈ 173,
  y un «se acerca al máximo» que en realidad lo supera (2,88 > 2,70 N·m).
* Apuntes B3 (guion S8): el diálogo del 10 kHz «porque es más del doble de ocho mil» no se
  sostiene (2×8 = 16 kHz); habría que cambiar los números o la réplica.
* S13: la comprobación impresa «Inversa = conjugado» no compara inv() con el conjugado.
* S14: «corona circular barrida» → el conjunto es el **toro** generado por la circunferencia
  de radio a2; «DH desde los años sesenta» → 1955 (como dice el propio [MD 20]); convendría
  advertir que spatialmath usa S = (v, ω) mientras L&P escriben (ω, v).
* S15: la «firma DH» de la muñeca esférica debe ser a4 = a5 = 0 y d5 = 0 (d6 ≠ 0 es
  compatible: el propio IRB 140 tiene d6 = 0,065); el ejemplo de convenciones rpy/eul de
  [CODE 10] es degenerado (misma terna en las tres convenciones); «tres articulaciones»
  → son dos (q2, q3) y de 90°.
* S16: «ramas distintas: 6» está inflado por redondeo (son 3); la pista comentada
  `interp1` lanza TypeError (el método es `T_a.interp(T_b, s)`); el «salto de rama» del
  solver no implica pérdida de rango del jacobiano; la solución del ej. 2 minimiza L1
  aunque el enunciado pide norma euclídea.
* Apuntes B4 (guion S16): mezcla numeración 1-based (L&P) y 0-based (Corke) sin aviso;
  «ocho coordenadas» vs «ocho configuraciones» para la misma cita.
* Apuntes B1: el bloque de dinamización de debates está redactado en primera persona para
  el profesor dentro de un documento de apuntes (¿debería vivir en la guía?).
* Apuntes B2: «funda a la cuchilla» clasificada como eliminación por diseño (es resguardo);
  la estimación de riesgo de ISO 12100 omite la probabilidad de ocurrencia del suceso;
  la votación «a mano alzada» del guion contradice la mecánica «con dedos» de la guía;
  «cuando yo diga tres… tres, dos, uno» (la señal cae al principio de la cuenta).
* Apuntes B3: factor de galga «hasta ±150» (guion) vs «−100 a +150» (apartado);
  «energía electromagnética óptica, de microondas o acústica» agrupa mal la acústica;
  «setecientos táctiles» → «tácteles» (el término que el propio texto fija);
  la referencia a «S11» para el lazo de control corresponde al bloque 5.

## 7. Cobertura

Todo lo determinista (ejecución, exámenes, claves, GIFT, calendario, arXiv, terminología,
atribuciones) está verificado al 100 %. La verificación semántica por agentes cubrió la
totalidad de las citas de riesgo y de las citas textuales/numéricas en los bloques
completados; los cuadernos S08-S21 y S23 y los apuntes B1-B6 recibieron además revisión
técnica línea a línea. El resto de la revisión línea a línea (S24-S40 en profundidad,
B7-B8, guía completa, guion narrado y las 8 presentaciones como documentos) quedó limitada
por los cortes del límite de gasto de la sesión; los tres flujos de trabajo quedan
reanudables con `resumeFromRunId` (véanse los journals en la sesión) si se quiere apurar
la cola restante.
