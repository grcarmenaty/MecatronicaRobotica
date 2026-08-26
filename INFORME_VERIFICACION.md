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
| Revisión técnica línea a línea de todo el material | 38 lotes: apuntes B1-B8, 8 presentaciones (diapositivas y notas), guía del profesor, guion narrado, plan, tareas, análisis y una pasada de coherencia cruzada | **38/38 completados**, ver §5 y §6 |
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
cuadernos 408, presentaciones 133, guía 27), la pasada automática de anclajes confirmó
1242 (71 %) y la corroboración por página compartida otras 287 (16 %). Los 217 restantes
(sin ancla, ancla fallida o página adyacente), más todas las citas textuales y con datos
numéricos y una muestra de control de 80 confirmadas, formaron el conjunto que pasó a
verificación semántica con lectura de la página citada. Esa pasada se completó al 100 %:
**652 ítems verificados uno a uno, 611 correctas (93,7 %), 38
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
### Bugs de código encontrados y corregidos

Los tres son silenciosos: el cuaderno se ejecutaba sin error y producía salidas de aspecto
razonable, así que ninguna ejecución los habría delatado.

* **S27** (`aprender_nucleo`): medía el acierto contra la variable global `PIEZAS` en lugar
  del parámetro `objetivo`, de modo que el ejercicio 2 (aprender otro objetivo) no medía lo
  que decía medir: devolvía 72,5 % cuando el acierto real contra la máscara pedida es 90,4 %.
* **S29** (`elipse`): `np.linalg.eigh` devuelve los autovalores en orden **ascendente**, pero
  el ángulo se tomaba del autovector del **mayor** (`vecs[:, -1]`) mientras `width` recibía el
  autovalor menor. En matplotlib el eje `width` se alinea con `angle`, así que **todas las
  elipses de covarianza del cuaderno se dibujaban giradas 90°** (comprobado: con P = diag(1, 100)
  el eje largo salía en x en vez de en y). Justo lo contrario de lo que la sesión quiere
  enseñar, porque la lectura de la geometría de las elipses es el objetivo del cuaderno.
  Corregido invirtiendo el orden de los ejes (`vals[::-1]`).
* **S39** (búsqueda aleatoria): el vector de pesos `rng_e.normal(size=DIM)` se sorteaba
  **dentro** del bucle de los tres episodios, de modo que cada episodio usaba una política
  distinta: se evaluaban 450 políticas de un episodio en lugar de 150 políticas de tres
  (el bloque del CEM justo debajo sí fija `w` por candidato, lo que hacía la comparación
  desigual). Corregido sorteando una política por candidato. Con el arreglo, la afirmación
  del texto «ninguna de **las 150** políticas aleatorias supera los 200 pasos» pasa a ser
  literalmente cierta (0 % y retorno medio 18,0 frente a 268,6 del CEM).

Los tres cuadernos se reejecutaron de principio a fin tras el arreglo, sin errores.

* Bibliografía: `gitignore.txt` renombrado a `.gitignore` (no estaba activo); añadido
  arXiv **2503.20020 (Gemini Robotics)** a `lista.txt` (el cuaderno de descarga ya lo
  incluía) y corregido el Checklist, que afirmaba que ese informe no tenía identificador
  de arXiv. Nota: YOLO (1506.02640) es v1 de 2015 y el curso lo data 2016 (CVPR): correcto
  como fecha de publicación.



### Segunda pasada: presentaciones, guía, guion, plan y coherencia cruzada

Errores técnicos confirmados contra la fuente y corregidos en generador + entregable + PDF.

**Observabilidad de la baliza lejana (B6).** Es el hallazgo de más peso. El cuaderno S29 lo
tiene bien («una baliza lejana orienta igual de bien pero sitúa mucho peor»), pero los
apuntes B6 y la guía de discusiones decían lo contrario: «la fila del rumbo decae con la
distancia, de modo que una baliza lejana casi no informa sobre la orientación», y la
respuesta prevista para la pregunta trampa daba por buena esa lectura y concluía «para
observar la orientación hacen falta hitos cercanos». En el jacobiano de rango-rumbo solo
decaen con la distancia las derivadas respecto de la posición (±Δ/r²): ∂φ/∂θ = −1 no
depende del rango, y la propia sección 4 del cuaderno lo mide (información sobre θ constante
e igual a 1/σφ²). Lo que se pierde a 50 m es la posición transversal: 1° de incertidumbre
angular son 87 cm de error lateral frente a los 5 cm que aporta el rango. Reescritos los
cuatro pasajes afectados (teoría 29.2, objetivo de la discusión, pregunta trampa y dos
respuestas previstas) para que digan lo que el cuaderno demuestra.

* **B8, PPO frente a TRPO.** Los apuntes atribuían a PPO las políticas de locomoción de
  ANYmal de Hwangbo et al. (2019, Science Robotics 4(26)). El artículo entrena con **TRPO**
  (comprobado en el propio texto del artículo, arXiv 1901.08652). Reescrito en dos sitios:
  PPO se presenta como el algoritmo por defecto de los flujos actuales, y ANYmal como
  entrenado con su antecesor de la misma familia de región de confianza.
* **B7, perfiles de QoS.** «Los perfiles predefinidos *sensor data* y *services* recogen
  exactamente estos casos» era falso para `/map`: ninguno de los cinco perfiles predefinidos
  de ROS 2 (default, services, sensor data, parameters, system default) usa durabilidad
  *transient local*; todos son *volatile* (verificado en docs.ros.org, Jazzy). Reescrito en
  los dos sitios para decir que esa durabilidad hay que declararla a mano.
* **B5, ecuación de desaturación del antiwindup.** `e = −(Ti·de/dt + Td·d²e/dt²)` era
  dimensionalmente inconsistente y no es lo que dice la fuente: De Silva et al. (2016),
  ec. 4.24, escribe `e = −Ti·(de/dt + Td·d²e/dt²)`. Corregido.
* **B5, lugar de las raíces.** Los apuntes pedían ver «cómo los polos migran hacia el eje
  imaginario al subir la ganancia», y el cuaderno S21 demuestra justo lo contrario: tras el
  punto de ruptura la parte real queda clavada en −K1/(2I) y los polos suben en vertical
  (por eso el modelo reducido nunca se desestabiliza). Corregido para que coincida con el
  cuaderno.
* **B6, `projectPoints`.** «Es la matriz C funcionando al revés» → aplica la proyección en
  sentido directo, como dice el propio texto unas líneas más abajo.
* **B4, elipsoide de velocidad.** «Los radios son los recíprocos de las raíces de los
  autovalores» solo es cierto para la matriz que Corke pasa a `plot_ellipsoid`,
  `E = (J·Jᵀ)⁻¹`. Explicitada la matriz.
* **B4, arcocoseno.** Lo que vale ±1 en la frontera del espacio de trabajo es el
  **argumento** del arcocoseno, no su valor.
* **B4, numeración de articulaciones.** Añadida la advertencia de que el «q4 = 0» de la
  singularidad de muñeca del PUMA es la numeración base 0 de Corke (la quinta articulación,
  ejes 4 y 6 en numeración industrial): el material mezclaba las dos convenciones sin aviso.
* **B2/B3, el UR16e.** Pies de foto y notas del orador decían «par medido en cada eje». La
  e-Series de Universal Robots estima el par por corriente y lleva un sensor fuerza-par de
  seis ejes en la brida; el par medido articulación a articulación es del KUKA LBR iiwa o
  del Franka. Corregidos los dos pies y las dos notas.
* **B2, estimación de riesgo (ISO 12100).** «Severidad × exposición × probabilidad de
  evitación» invierte el papel de la evitabilidad, que resta riesgo. Reescrito como
  «severidad del daño y probabilidad de que ocurra: exposición, suceso peligroso y
  posibilidad de evitarlo», en la diapositiva y en los dos pasajes de los apuntes.
* **B2, taxonomía.** «Fijos (primera generación: la célula va al robot)» → «el trabajo va
  al robot».
* **B4, cita de Corke.** «no **todas** las ocho soluciones son físicamente alcanzables»
  (faltaba la palabra; Corke, p. 282, *not all eight solutions are physically achievable*).
* **B6, convoluciones.** «La misma que ejecuta cada capa convolucional del bloque
  siguiente» → de la **sesión** siguiente (S27 es del propio B6).
* **B6, 3D Gaussian Splatting** agrupado como «representación neuronal»: es explícito, sin
  red. Reescrito como «representación aprendida (NeRF, neuronal; 3DGS, de primitivas
  explícitas)». Y «la **mitad** percibir de la tríada» → «la parte de percibir».
* **B7, A* en 1968** (quedaba un 1966 en las notas del orador) y «AMCL en la sesión
  siguiente» (S34) → «AMCL en S36». La «retroalimentación» de las acciones de ROS 2 se deja
  como está: es una de las cuatro apariciones que §2 señala como decisión del autor.
* **B8, MDQ → MDP** en la diapositiva de qué entra en el examen (ya corregido en apuntes).
* **B8 y Tareas, el windup bajo un PD.** El resumen del parcial 2 decía «diseño de un PD
  con sobreoscilación, error de gravedad y windup»; el windup es de la acción integral y el
  examen lo introduce, correctamente, en el apartado B3-B4 al pasar al PID. Reescrito en los
  tres sitios.
* **B1**, «Yasakawa» → «Yaskawa» también en la diapositiva (la errata viene de De Silva,
  que la escribe así en el original), y «transformador ideal» → «convertidor
  electromecánico ideal» en las notas de S2 (v·i = ω·τ describe un girador, no un
  transformador).
* **B3**, «feedforward de velocidad» → «prealimentación de velocidad» y «grippers» →
  «pinzas» (la Convención lo fija; 5 apariciones entre apuntes B3, deck, fichas y guía,
  con su artículo corregido); en la guía, «feedforward de par puro» → «prealimentación de
  par puro» (3).

Erratas numéricas y de redacción de la guía del profesor y del guion narrado:

* Guía S19: `T ≥ √(10·D/(√3·a_max))` = **2,403 s**, no 2,4495 (que es √6); el cuaderno ya
  estaba corregido, la guía arrastraba el valor viejo. Guía S21: la regla 4,6/(ζ·ωn) es la
  banda del **1 %** (4,6 = ln 100) mientras `ct.step_info` mide sobre la del 2 %.
* Guía S20: «un cambio de inercia de factor dos, reflejado al motor, es cuarenta veces
  menor que la inercia del rotor» no cuadra con sus propios números: 0,35/100² = 3,5·10⁻⁵
  frente a 1,2·10⁻⁵ del rotor, es decir unas **tres veces mayor**. Reescrito con el número
  honesto (el efecto 1/G² atenúa la variación pero con G = 100 no la borra).
* Guía S38: desde (7,0) la meta está a **dieciséis** pasos, no quince
  (0,5¹⁶ ≈ 1,5·10⁻⁵). Verificado que el `+0,169` de γ = 0,995 sí es el valor que imprime el
  cuaderno, y que (7,0) sí existe en una rejilla 8×10.
* Guía S14: el espacio de trabajo del 2R con α₁ = 90° es el **toro** que genera la
  circunferencia de radio a₂ al barrerla alrededor del eje de la base, no «la corona
  circular barrida» (una corona barrida sería un sólido). Guía S15: qn y q_trabajo difieren
  en **dos** articulaciones (q2 y q3) y en 90° cada una, no en «tres y en ángulos
  moderados»; y `qtrabajo` del enunciado → `q_trabajo`, el nombre que usa la solución.
  Guía S16: «es que **es** físicamente imposible de ejecutar». Guía S35: escape de Markdown
  `A\*` sin resolver en el enunciado (el docx no interpreta escapes; el cuaderno sí, y por
  eso allí se deja como estaba). Guía B3: «el husillo a ocho mil hercios» → «el husillo, con
  la vibración a medir hasta ocho mil hercios» (8 kHz es la banda, no el giro).
* Guía B3: el «óptimo del orden de 420» se atribuía a la regla de adaptación de inercias
  `G = √(Jl/Jm)`, que con los datos del cuaderno da **173** y cae dentro de la ventana. Los
  420 son el óptimo que minimiza el par del motor, `G* = √((Jl + τ_g/α)/Jm)`, que es lo que
  calcula el cuaderno S12. Separados los dos números para que la lección se sostenga.
* Guion narrado B4: «las tres tienen que dar**lo** mismo» → «dar lo mismo»; «el **par** M,
  S₁, S₂» → «la terna» (son tres elementos, como dice el propio párrafo siguiente); «la
  receta del **martes**» → del miércoles (S14 es miércoles 14 de octubre); «Denavit y
  Hartenberg, la de los años sesenta» → «la del artículo de 1955» (Corke, excurso 7.4).
  Se comprueba y **se mantiene** la anécdota del Apolo 13: es la que trae Corke en su
  excurso 2.14, con la transcripción del bucle de control de la misión.

Exámenes, calendario y bibliografía:

* Los 18 enunciados decían «cada error resta un tercio del valor de la pregunta» y a
  continuación «error: −0,07», cuando un tercio de 0,2 es 0,0667. Corregido a **−0,067** en
  los 18 y arreglado el redondeo del generador (era a dos decimales).
* Tareas §3: el calendario maestro **duplicaba las filas S25 y S26** con contenidos
  contradictorios (la misma S25 como examen parcial 1 y como taller de calibración),
  resto de una versión anterior a mover el parcial. Eliminadas las dos filas obsoletas y
  reubicada en S24 la lectura de Corke que encargaban. La preparación de la defensa pasa de
  la columna «se encarga» de S43 (última sesión, donde se celebra) a la de S42.
* Tareas §5: la tabla tiene **once** filas y el texto decía diez; el entregable de
  calibración figuraba en S25 cuando el propio §2 y el calendario lo describen como cuaderno
  en casa encargado en S26 y entregado antes de S28. Tareas §6: la entrega 2 del proyecto
  aparecía en «S24 · 5 nov» contra el «S26 · 11 nov» del Plan y del calendario. Tareas §8:
  el texto hablaba de **tres** deberes críticos y la tabla marca cuatro (S21, S22, S34 y S41).
* README: B1 = S01-S04 y B2 = S05-S07 (decía S01-S03 y S04-S07, contra el Plan, el
  calendario y los propios apuntes), y el umbral de recuperación es «un parcial por debajo
  de 4», no «algún bloque».
* `bibliografia/LEEME.md`: cuatro de las cinco filas asignaban los libros a bloques
  distintos de los que realmente los citan (Corke se usa en B1-B7, Lynch y Park en B2, B4,
  B5 y B7, Thrun en B6 y B7, De Silva en B1, B3, B5 y B8); «25 artículos» → **22**, que son
  los que tiene `lista.txt`; y el «unas 750 citas» ahora explica su relación con las 992 del
  Informe de verificación de citas (que cuenta por separado las referencias que comparten
  paréntesis). En el Checklist, «los veintiún artículos» → veintidós.

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
  apuntes B3 arrastra lo mismo, más un «se acerca al máximo» que en realidad lo supera
  (2,88 > 2,70 N·m).
* Apuntes B3 (guion S8): el diálogo del 10 kHz «porque es más del doble de ocho mil» no se
  sostiene (2×8 = 16 kHz), y hay que elegir entre dos diseños coherentes del mismo cebo, que
  es decisión pedagógica: (a) el alumno muestrea a 10 kHz y **no** llega a Nyquist, en cuyo
  caso la justificación que se le pone en boca debe cambiar y la réplica debe preguntar qué
  hay por encima de 5 kHz; o (b) el alumno muestrea a 20 kHz aplicando bien la regla pero
  suponiendo que la señal está limitada a 8 kHz, que es lo que encaja con la réplica actual
  («qué hay en la señal por encima de 8 kHz») y con «ha aplicado correctamente una regla que
  ha entendido mal». Afecta a tres pasajes de apuntes B3 y a la guía.
* S13: la comprobación impresa «Inversa = conjugado» no compara inv() con el conjugado.
* S14: convendría advertir que spatialmath usa S = (v, ω) mientras L&P escriben (ω, v).
  («Corona circular barrida» → toro, y la fecha de DH en el guion, ya corregidos.)
* S15: la «firma DH» de la muñeca esférica debe ser a4 = a5 = 0 y d5 = 0 (d6 ≠ 0 es
  compatible: el propio IRB 140 tiene d6 = 0,065); el ejemplo de convenciones rpy/eul de
  [CODE 10] es degenerado (misma terna en las tres convenciones).
* S16: «ramas distintas: 6» está inflado por redondeo (son 3); la pista comentada
  `interp1` lanza TypeError (el método es `T_a.interp(T_b, s)`); el «salto de rama» del
  solver no implica pérdida de rango del jacobiano; la solución del ej. 2 minimiza L1
  aunque el enunciado pide norma euclídea.
* Apuntes B4 (guion S16): mezcla numeración 1-based (L&P) y 0-based (Corke) sin aviso;
  «ocho coordenadas» vs «ocho configuraciones» para la misma cita.
* Apuntes B1: el bloque de dinamización de debates está redactado en primera persona para
  el profesor dentro de un documento de apuntes (¿debería vivir en la guía?).
* Apuntes B2: «funda a la cuchilla» clasificada como eliminación por diseño (es resguardo);
  la votación «a mano alzada» del guion contradice la mecánica «con dedos» de la guía;
  «cuando yo diga tres… tres, dos, uno» (la señal cae al principio de la cuenta).
* Apuntes B3: factor de galga «hasta ±150» (guion) vs «−100 a +150» (apartado);
  «energía electromagnética óptica, de microondas o acústica» agrupa mal la acústica;
  «setecientos táctiles» → «tácteles» (el término que el propio texto fija);
  la referencia a «S11» para el lazo de control corresponde al bloque 5.


De la segunda pasada, comprobados y **no** corregidos porque la decisión es del autor:

* **Plan, criterio de los talleres.** El apartado 1 declara que «la sesión de 2 h del viernes
  concentra los talleres con ordenador», y S15 («Taller: cinemática directa con la Robotics
  Toolbox») y S21 («Respuesta temporal y frecuencial con python-control») son trabajo con
  ordenador en jueves de 1 h. O se matiza el criterio o se mueven las sesiones.
* **Cuántos talleres tienen entregable.** Tres recuentos distintos: Tareas §2 dice nueve
  (S7, S10, S13, S15, S16, S19, S22, S28, S34), Tareas §5 tabula once y la guía del profesor
  habla de «las nueve sesiones de taller (S10, S13, S15, S16, S19, S22, S25, S28 y S34)».
  Se ha corregido el «diez» del §5 para que cuadre con su propia tabla, pero hace falta
  decidir qué cuenta como taller con entregable y unificar las tres listas.
* **Pesos de la evaluación.** Tareas §1 declara que «este documento usa la propuesta» de
  modernización (examen al 30 %, proyecto al 20 %) y §9 la deja abierta, mientras el Plan da
  la decisión por cerrada en 40/30/10/20 y sus propios pesos suman 40. Es la «decisión
  pendiente» que el propio §9 anuncia; no la he tomado.
* **Cabeceras de dos cuadernos sobre días de examen.** `82514_S25_Formacion_Imagen_Calibracion`
  se declara «viernes 6 de noviembre» y `82514_S40_Imitacion_VLA` «viernes 11 de diciembre»,
  que son el parcial 1 y el parcial 2. Con el calendario vigente esos contenidos caen en S26
  y S39; renumerar los ficheros afecta al LEEME de cuadernos, a los apuntes y a los enlaces
  del campus, así que lo dejo señalado. Los enlaces «Abrir en Colab» que ahora llevan las
  portadillas de sesión rotulan siempre el número del cuaderno al que saltan, precisamente
  para que el desfase se vea en lugar de quedar tapado.
* **Checklist, contenido docente en S40.** Cuatro referencias (ISO 23247, artículos de B8,
  simuladores) sitúan materia en S40, que es el parcial 2; y los talleres de visión en
  «S25 y S26», cuando S25 es el parcial 1.
* **B2, el reparto horario de S7.** Las notas planifican «80-105 taller de riesgos»
  (25 min) para un encargo que la propia diapositiva y sus notas fijan en 30 min más
  corrección en común, con el cuestionario de bloque ocupando 105-120. La sesión de 120 min
  no cuadra; hay que recortar el encargo o mover los tramos.
* **B7, campos potenciales.** Aparecen en la portadilla de S35 y en el plan de la sesión
  («52-60 campos potenciales y cierre»), pero no hay ninguna diapositiva de contenido ni
  entrada en la hoja de ruta; la tabla comparativa solo cubre transformada de distancia,
  A*, PRM y RRT.
* **B8, alcance del examen final.** Una diapositiva enumera contenido que «entra de forma
  literal» para los ocho bloques mientras sus notas describen el final como centrado en B8 e
  integración para quien haya superado los parciales.
* **Plan y decks, nombre del bloque 8.** «B8. Robot learning, seminario y cierre» en la tabla
  de materiales frente a «B8. Robótica basada en aprendizaje» en la de horas: el anglicismo
  no está en la convención. En el Plan quedan además dos notas de proceso del generador
  («Decisión que cierra la incoherencia pendiente», «(diseño intocado)») dentro del
  entregable.
* **Seminario, S41 y S42.** Cinco presentaciones de 10 + 5 min en cada una son 75 min en
  sesiones de 1 h, y S42 aloja además el cierre del curso.

## 7. Cobertura

Las tres pasadas están completas al 100 %:

* **Citas**, 55/55 lotes: los 652 ítems seleccionados verificados uno a uno contra la página
  del libro.
* **Cuadernos**, 29/29: ejecución completa más revisión técnica línea a línea de cada uno,
  reejecutados tras cada corrección.
* **Documentos**, 38/38 lotes: apuntes B1-B8, las ocho presentaciones (diapositivas y notas
  del orador), la guía del profesor completa, el guion narrado de B4, el plan del curso, el
  documento de tareas, el análisis de partida y una pasada final de coherencia cruzada entre
  todos ellos.

Todo lo determinista (ejecución, exámenes, claves, GIFT, calendario, arXiv, terminología,
atribuciones) está verificado al 100 %.

Queda fuera de esta verificación lo que no es comprobable desde el repositorio: las cuatro
normas ISO, que son de pago y se citan siempre por designación; el laboratorio, que el
material declara intocado; y las decisiones pedagógicas y de calendario recogidas en §6,
que son del autor.

Cada hallazgo de los agentes de revisión se comprobó a mano antes de aplicarlo. Varios no
sobrevivieron a esa comprobación y se dejan anotados aquí para que no vuelvan a levantarse:
la anécdota del **Apolo 13** del bloqueo de cardán es la que trae Corke (excurso 2.14); la
muñeca **ZYX** del desacoplo es la de Lynch y Park (p. 225), distinta de la ZYZ del 6R
genérico de Corke (p. 260) y de la ZXZ del PUMA (p. 282), y las tres están bien citadas;
«roboti, raíz de servidumbre» es literalmente lo que dice Corke (p. 2), aunque el sustantivo
checo sea *robota*; la marca «mechatronics» se data en 1972 porque así lo dice De Silva
(p. 10), que es la fuente citada, y el registro japonés nº 46-32714 es de Showa 46 (1971): la
discrepancia es de la fuente, no del curso; el óptimo «~420» de S12 sí es el que calcula el
cuaderno; el paso 0 del MCL de S30 sí tiene **cinco** cúmulos y no cuatro (las cuatro puertas
generan hipótesis a ±3 m, de las que sobreviven cinco: ≈2, 8, 12, 18 y 28 m, comprobado
ejecutando el cuaderno); `v*(7,0) = +0,169` con γ = 0,995 es el valor que imprime el cuaderno S38, y (7,0)
está dentro de una rejilla de 8×10; y la frase «la traspuesta del jacobiano nunca puede ser
singular» se conserva donde aparece **como cita de Corke** (p. 325), que es quien la escribe,
mientras que en la pregunta de examen, donde se enunciaba como afirmación propia, ya se
reescribió (§4).
