// Respuestas canónicas de las 39 discusiones (redactadas para la Guía del Profesor a partir
// del cierre de cada guía de conducción). Clave: "bloque|sesión|minutos" tal como salen de guia_datos.json.
module.exports = {
 // ---------------- Bloque 1 ----------------
 "1|S1|50–60 min": {
 corto: "Electromecánico o mecatrónico",
 resp: "La mecatrónica es una metodología de diseño, no una lista de componentes: «sinérgico» e «integrado» hablan de cómo se tomaron las decisiones, no de qué piezas lleva el objeto. Por eso media lista de la pizarra no puede clasificarse mirando el objeto: haría falta ver el expediente de diseño. No cerrar con «casi todo es mecatrónico» ni con «es discutible»: la definición se aplica, no se opina.",
 },
 "1|S3|47–55 min": {
 corto: "Telerobots, autonomía y el brazo del laboratorio",
 resp: "La definición de robot, percibir, planificar, actuar, es una vara de medir, no una frontera nítida: ante cualquier máquina, la pregunta útil no es «¿es un robot?» sino qué percibe, qué planifica y quién pone el objetivo. El brazo del laboratorio es un robot en el uso industrial de la palabra y un caso incompleto medido con la definición del libro, y ambas afirmaciones son verdaderas a la vez.",
 },
 "1|S4|25–35 min": {
 corto: "El debate de ética",
 resp: "La posición que queda establecida es la del libro: son cuestiones que no deben ni pueden decidirse solo por los roboticistas, pero que tampoco deben ser ignoradas por ellos; participar en el debate social es parte de la profesión. Antes de decirlo, señalar el delta de votos de la pizarra: eso es lo que han hecho unos argumentos en diez minutos. Lo que nunca se dice: «cada uno tiene su opinión y todas valen igual».",
 },
 // ---------------- Bloque 2 ----------------
 "2|S5|88–95 min": {
 corto: "Calibración del espectro de autonomía a mano alzada",
 resp: "El escalón de autonomía no es una propiedad del robot sino del reparto de control en una tarea y un modo concretos: la misma máquina cambia de escalón cuando cambia de modo. Cirugía robótica y ROV están clasificados en el libro como teleoperación y el rover marciano como autonomía con objetivos remotos; el dron, el taxi y el brazo son aplicaciones nuestras del criterio, y ser honesto con esa diferencia enseña cómo se usa una fuente.",
 },
 "2|S5|95–115 min": {
 corto: "La actividad de fichas en equipos y su puesta en común",
 resp: "Las taxonomías son herramientas de descripción, no cajones excluyentes: la ficha que cuesta clasificar señala un rasgo del objeto, el humanoide pertenece a dos categorías a la vez, no un fallo de la clase. No se reparte plantilla con las «respuestas correctas», ni en el aula ni en el campus: se dan las definiciones con su página, porque la tabla resuelta no existe y sostenerlo es parte de lo que se enseña.",
 },
 "2|S7|30–36 min": {
 corto: "El cobot con herramienta cortante",
 resp: "El robot se certifica, la aplicación se valida: un cobot certificado con una cuchilla en la brida no es una aplicación colaborativa válida, y un robot industrial de jaula puede formar parte de una aplicación colaborativa. La pregunta profesional no es si algo «es un cobot», sino qué método colaborativo aplica esta tarea y con qué evidencia. Ni «los cobots son seguros» ni «son peligrosos»: las dos frases son igual de falsas.",
 },
 "2|S7|100–110 min": {
 corto: "Corrección en común del taller de análisis de riesgos",
 resp: "La seguridad no es un componente que se compra ni una cláusula que se cita: es el resultado de un proceso documentado sobre una aplicación concreta, y la jerarquía eliminar–proteger–informar es un orden obligatorio, no un menú. Los accidentes reales se concentran en los modos degradados, y la «formación del operario» como medida estrella de los riesgos altos es el error que hay que desmontar. No existe una tabla correcta única, y decirlo forma parte del cierre.",
 },
 // ---------------- Bloque 3 ----------------
 "3|S10|50–55 min": {
 corto: "Por qué la manipulación diestra sigue limitada por el tacto",
 resp: "En tacto, el transductor está resuelto y el sistema no: lo que falta es integración mecánica, cableado, robustez y procesado, no principio físico. Corolario de criterio: cuando una tecnología lleva veinte años prometida y no llega, hay que preguntar por la integración y el procesado, no por el transductor. La conexión queda abierta hacia las pinzas del laboratorio y hacia las manos de los humanoides, hoy la parte menos resuelta de la máquina.",
 },
 "3|S10|110–115 min": {
 corto: "Puesta en común del ejercicio de selección de sensores",
 resp: "El error típico es empezar por el catálogo; la metodología obliga a empezar por la medida, magnitud, banda de frecuencia, rango, entorno, y decidir por jerarquía: primero la tecnología, después el componente (es el MDQ de De Silva funcionando). La especificación define una región de soluciones aceptables, no un punto: por eso han salido sensores distintos igualmente defendibles y lo que se evalúa es el razonamiento y su orden. No se da «la solución oficial» de los tres casos.",
 },
 "3|S11|30–40 min": {
 corto: "Las ventajas del BLDC",
 resp: "La ventaja del brushless no está en la física instantánea del par sino en la térmica y en la fiabilidad: las «tres ventajas» del catálogo son en realidad dos argumentos y medio. Y la lección epistémica que justifica los minutos: el libro da el hecho, la robótica industrial usa brushless, y no la explicación electromagnética, de modo que lo discutido son razones de catálogo y práctica industrial, y hay que decir en voz alta ese estatus. Nunca zanjar con «en la industria se usa brushless y punto».",
 },
 "3|S12|48–50 min": {
 corto: "Puesta en común de la selección motor-reductora",
 resp: "Sensor, accionamiento y transmisión no se eligen por separado: las comprobaciones del dimensionado tiran en direcciones opuestas y el resultado es una ventana de valores admisibles, no un número. Dentro de la ventana, la elección ya no es de mecánica sino de control: la relación de inercias decide si el lazo del bloque 5 será sintonizable. La G «buena» no se anuncia antes de que la contradicción esté escrita en la pizarra.",
 },
 // ---------------- Bloque 4 ----------------
 "4|S15|48–55 min": {
 corto: "Por qué la toolbox y el robot del laboratorio no dan lo mismo",
 resp: "Un modelo cinemático no coincide con el robot por defecto: coincide cuando se han hecho coincidir explícitamente sus extremos y su convención. Ante cualquier discrepancia, la lista de sospechosos es herramienta, base y convención de ángulos, en ese orden. No cerrar con «el robot está muy bien calibrado y estas cosas son normales»: es la versión amable del error que se acaba de desmontar.",
 },
 "4|S16|25–35 min": {
 corto: "Existencia antes de calcular",
 resp: "La cinemática inversa no es una función: puede no haber solución, haber varias ramas o infinitas, y todo lo demás se deduce de ahí. La disciplina que queda: comprobar existencia antes de calcular, y usar siempre atan2 de dos argumentos en lugar de arcotangentes de cocientes, porque conserva el cuadrante. El patrón, reducir a triángulos, cosenos y atan2, enumerar ramas, es el mismo que reutiliza el seis ejes tras el desacoplo.",
 },
 "4|S17|48–55 min": {
 corto: "La deriva de integración",
 resp: "Integrar velocidades sin medir acumula error, y ningún refinamiento numérico arregla un lazo abierto: cada vez que aparezca una integración de velocidades, jogging, odometría de B6, estimador inercial, la primera pregunta es quién cierra el lazo y con qué medida. Con la honestidad añadida que prepara el bloque 6: la «medida» industrial de la pose sale de la cinemática directa sobre los encoders, es decir, del propio modelo.",
 },
 "4|S19|95–110 min": {
 corto: "El repaso del bloque: el mapa de seis casillas",
 resp: "El cierre es estructural, no un resumen: en este bloque el robot ha sido geometría, y toda la geometría se apoya en dos objetos, una pose y un jacobiano; el resto son formas de mirarlos. Y la conexión hacia delante: a partir de S20 el robot pasa a ser física, y las fuerzas calculadas hoy con la traspuesta del jacobiano serán las que haya que generar y controlar. Nada de listas de «lo que entra y lo que no entra».",
 },
 // ---------------- Bloque 5 ----------------
 "5|S21|50–58 min": {
 corto: "Discrepancias: la predicción a mano contra ct.step_info()",
 resp: "En control conviven dos tipos de fórmula y hay que saber cuál se tiene en la mano: la sobreoscilación es una identidad exacta y el tiempo de establecimiento una regla conservadora construida sobre la envolvente. Corolario que se usa desde mañana: ningún tiempo de establecimiento significa nada sin su banda de tolerancia. Nunca cerrar con «para lo que nos interesa da igual»: desactiva el hábito de comprobar.",
 },
 "5|S22|110–120 min": {
 corto: "Puesta en común del taller de PID",
 resp: "La especificación define una región de ternas válidas, no un punto: por eso las diez soluciones distintas de la tabla están todas bien. Dentro de la región, la sintonía rápida se paga en sensibilidad a las variaciones del proceso, y elegir dónde ponerse es una decisión de ingeniería que ningún pliego toma por ti; y el controlador debe modelar también su propio hardware (anti-windup, saturación). Bajo ningún concepto se dan «las ganancias buenas» del taller.",
 },
 // ---------------- Bloque 6 ----------------
 "6|S25|85–90 min": {
 corto: "Qué mata una calibración",
 resp: "La calibración describe una cámara concreta en un montaje concreto y muere cuando cambia cualquiera de los dos: los intrínsecos mueren con la óptica (enfoque, zum, montura, ciclos térmicos) y los extrínsecos con la pose, y se recuperan a coste muy distinto. Corolario de proyecto: patrón de verificación, umbral de aviso y responsable se deciden al diseñar la célula, no cuando falla. No prescribir el «recalibrar por si acaso cada semana»: es ritual, no criterio.",
 },
 "6|S25|106–113 min": {
 corto: "Qué dice y qué no dice el error de reproyección",
 resp: "El error de reproyección es la única métrica interna disponible y es imprescindible, pero mide el ajuste sobre las mismas vistas que se usaron para ajustar, y puede bajar empeorando la calibración. La exactitud solo se comprueba contra algo que no entró en el ajuste: una vista reservada, la coherencia con la óptica y el tamaño de píxel, o una pieza patrón. La frase que resume el bloque: la geometría no se aprende, se mide.",
 },
 "6|S26|0–5 min": {
 corto: "El repaso a mano alzada que abre S26",
 resp: "Las dos respuestas que hay que dejar puestas: once parámetros, cinco intrínsecos y seis extrínsecos; y la proyección pierde la profundidad, de un píxel se sabe un rayo, no un punto. El cierre es una frase de tránsito, no una síntesis: guardad esos once números, porque en el minuto cuarenta la matriz K convertirá un centroide en milímetros. Ni amenaza de examen ni juicios sobre el nivel del grupo: enmudecen la hora entera.",
 },
 "6|S27|31–35 min": {
 corto: "Latencia y precisión",
 resp: "En percepción embarcada la magnitud de diseño no es la precisión: es el producto de la velocidad por la latencia, la distancia ciega, y la precisión solo se compara a igualdad de ese producto. Corolario de proyecto: la primera cifra que hay que medir en el hardware propio es el tiempo de inferencia, porque el mAP viene en el artículo y la latencia depende de su GPU. No decir que «los detectores modernos ya son suficientemente rápidos».",
 },
 "6|S27|45–55 min": {
 corto: "Los tres casos: clásico frente a aprendido",
 resp: "La geometría calibrada no se aprende, incluso el sistema más neuronal necesita su matriz K, y el clásico sigue ganando con iluminación controlada, tolerancias métricas y pocos datos; el aprendido gana con variabilidad y semántica. Los tres casos acaban en soluciones híbridas, que es el estado real de la percepción industrial, y la seguridad no se decide en esta tabla. Lo que queda escrito no es «depende», sino de qué depende.",
 },
 "6|S28|33–40 min": {
 corto: "La hipótesis de Markov",
 resp: "La hipótesis de Markov no es una propiedad del mundo sino del estado que hemos elegido: diseñar consiste en meter en el estado lo suficiente para que lo que queda fuera se pueda tratar como ruido. Corolario que se cobra en el taller: cuando un filtro se equivoca con la banda de confianza estrecha, la sospecha no es el ajuste del ruido, es que falta una variable en el estado. Ampliar el estado tiene precio computacional, y de ahí las dos familias de aproximaciones de las tres sesiones siguientes.",
 },
 "6|S29|49–55 min": {
 corto: "La pregunta trampa de la baliza lejana",
 resp: "El jacobiano de la medida es geometría y se lee: cada fila dice en qué dirección del espacio de estados informa esa medida, y la longitud de esa flecha decide si la componente se corrige o no; con la baliza lejana, la misma medida deja de informar de lo mismo. Corolario profesional: la colocación de balizas o reflectores es parte del diseño del estimador, y un mapa de hitos lejanos y agrupados no se arregla con ningún ajuste de software.",
 },
 "6|S30|52–60 min": {
 corto: "EKF frente a MCL",
 resp: "Las seis filas de la tabla son consecuencias de una sola decisión, la representación de la creencia: la pregunta profesional no es qué algoritmo es mejor, sino qué forma tiene la creencia que hay que representar. Si tiene que poder decir «no sé dónde estoy», ninguna gaussiana sirve; si tiene que actualizarse en microsegundos, ninguna nube sirve. Se cierra dejando sin contestar, literalmente: «¿Y si tampoco tenemos el mapa?».",
 },
 "6|S31|85–100 min": {
 corto: "El panorama de SLAM neuronal",
 resp: "Cambia la representación del mapa, rejilla, puntos, campo neuronal, gaussianas, pero el esqueleto probabilístico, modelos, creencia y optimización, es el de este bloque; y lo nuevo se apoya en lo viejo, porque estas reconstrucciones necesitan poses que produce la geometría clásica. Es panorama y no materia cerrada: el cuestionario solo pide saber qué es cada cosa y dónde encaja. No tomar partido en ningún sentido: ambas posiciones son especulación disfrazada de criterio.",
 },
 // ---------------- Bloque 7 ----------------
 "7|S32|50–55 min": {
 corto: "El ejercicio de QoS a mano alzada",
 resp: "La QoS es un contrato entre dos extremos que se deduce de la semántica del canal, no de la «importancia» del dato, y las dos preguntas que lo resuelven son qué cuesta perder un mensaje y quién necesita el último si llega tarde. Corolario operativo que se cobra en el taller: cuando un topic exista y no llegue nada, la primera sospecha es la incompatibilidad de QoS y el primer comando es ros2 topic info con detalle.",
 },
 "7|S34|103–108 min": {
 corto: "Quién publicará map a odom",
 resp: "La tabla de REP 105 con su física, en tres líneas de pizarra: odom→base_link es continua y con deriva y la publica la odometría; map→odom es exacta y con saltos y la publica la localización; base_link→sensor es fija y calibrada y la publica la descripción del robot. Ningún frame es a la vez exacto y continuo, y por eso hacen falta dos. El cierre es una promesa, no una respuesta: la arista que falta la publicará en S36 el filtro de partículas del bloque 6.",
 },
 "7|S34|110–117 min": {
 corto: "Errores frecuentes del taller de ROS 2",
 resp: "Lo que queda no es la lista de errores, que se olvida, sino la estructura: en un sistema distribuido síntoma y causa no se corresponden uno a uno, y de uno a otra se pasa con introspección, un ingeniero que domina estas herramientas diagnostica un robot ajeno sin leer su código. Los errores son normales y, sobre todo, diagnosticables; la tabla síntoma→causa de la pizarra se fotografía, se sube al campus y se amplía durante el proyecto.",
 },
 "7|S35|45–55 min": {
 corto: "La tabla comparativa de planificadores",
 resp: "Las cinco propiedades, completitud, optimalidad, dónde está el coste, mapa cambiante, dimensión, son cinco preguntas de proyecto, y se elige por la restricción más dura, no por la propiedad más prestigiosa. Planificar empieza por preparar el mapa, no por elegir el algoritmo. Sin ganador: A* domina en móvil 2D por buenas razones y no vale para el brazo, y esa asimetría es la que da sentido a S37. La tabla no se borra: se fotografía para abrir S36.",
 },
 "7|S36|28–32 min": {
 corto: "El costmap local: por qué no puede vivir en map",
 resp: "El frame de cada módulo es una decisión de arquitectura de control: se elige por la clase de error que ese módulo tolera, no por la exactitud del frame. La regla de tres líneas: reaccionar en odom, decidir en map, no mezclar sin pasar por el árbol. Y la consigna de diagnóstico: cuando el robot haga algo absurdo justo después de una corrección de localización, el sospechoso es el frame. No es un detalle de Nav2: aparece igual en cualquier stack.",
 },
 "7|S37|80–105 min": {
 corto: "El stack completo y la puesta en común de riesgos",
 resp: "Cada flecha del diagrama es una interfaz de ROS 2 con su tipo y su QoS, y cada caja un conjunto de nodos con parámetros que hay que justificar, no copiar. Lo que la puesta en común demuestra: los proyectos no fallan por el algoritmo, fallan por las flechas, QoS, frames, sellos de tiempo y semántica de interfaz. Encargo operativo: el diagrama se fotografía y entra en la memoria de cada equipo, y los riesgos se publican para todos, porque el riesgo de un equipo es el aviso de otro.",
 },
 // ---------------- Bloque 8 ----------------
 "8|S38|12–17 min": {
 corto: "Qué hace exactamente el descuento (gamma)",
 resp: "Gamma define un horizonte efectivo del orden de 1/(1−γ) pasos y ese horizonte tiene que cubrir la tarea: con 0,99 son unos cien pasos y con 0,9 son diez. Gamma no es un mando de comportamiento: es parte de la definición del objetivo, y cuando la política sale mal la primera sospecha es la recompensa, no el descuento. No bendecir el «se deja en 0,99 y no se piensa más».",
 },
 "8|S38|17–20 min": {
 corto: "Formulación del MDP y reward hacking",
 resp: "El agente optimiza lo que se mide y no lo que se quiso decir: la recompensa no se lee, se ataca. El procedimiento operativo que queda: antes de entrenar, buscar con lápiz las dos políticas, la que quieres y la más barata que puntúa, y si no coinciden, la recompensa está mal. Y el enlace que justifica el resto del bloque: la dificultad de especificar es la razón de ser de la imitación. No dejar en la pizarra una recompensa «arreglada» como solución.",
 },
 "8|S39|50–57 min": {
 corto: "Sim-to-real: qué se puede y qué no se puede aleatorizar",
 resp: "La regla del cuaderno, dictada: mide lo que puedas medir barato y aleatoriza lo que no. Con su alcance exacto: la aleatorización garantiza rendimiento sobre la familia de mundos que se aleatorizó y no promete nada fuera de ella. Corolario para el seminario y el proyecto: ante una transferencia exitosa, la pregunta no es si aleatorizaron, es qué rango aleatorizaron y si el robot real cae dentro. «Con suficiente aleatorización está resuelto» es la afirmación más extendida y más falsa del área.",
 },
 "8|S40|32–35 min": {
 corto: "Imitación frente a refuerzo",
 resp: "La elección entre refuerzo e imitación no la decide el robot: la decide qué es más barato en ese problema, especificar el éxito o demostrarlo. Y el corolario que prepara el tramo siguiente: los sistemas de manipulación que vienen son imitación a escala, y arrastran los problemas de la imitación, deriva por errores compuestos y multimodalidad, por muchos parámetros que tengan. Ninguna de las dos familias es «la avanzada».",
 },
 "8|S40|80–90 min": {
 corto: "Los modelos VLA: qué cambian y qué no",
 resp: "Lo que cambian: el lenguaje se convierte en la interfaz de tarea y el preentrenamiento a escala aporta una generalización semántica que las demostraciones solas no dan. Lo que no cambian: la consigna se ejecuta sobre la cinemática, los lazos de control, los actuadores y el middleware del resto del curso, y las funciones de seguridad siguen fuera del modelo. Limitaciones sin dramatismo: fiabilidad en tareas largas, latencia y cómputo, evaluación no estandarizada, dependencia de la cobertura de datos. Y la advertencia mayor de la guía: no tomar partido en ningún sentido.",
 },
 "8|S40|100–105 min": {
 corto: "Qué haría falta para confiar una célula a un VLA",
 resp: "Las funciones de seguridad se implementan con ingeniería certificable, independiente y por debajo de cualquier componente aprendido; y no es una limitación temporal del estado del arte, sino una consecuencia de qué garantías se pueden demostrar sobre un componente estadístico. Casi todo lo que la clase exige está en el sistema alrededor del modelo, y el ingeniero que sabe montar ese sistema es el perfil que este curso ha intentado formar.",
 },
 "8|S42|53–58 min": {
 corto: "El mapa colectivo de artículos: la última pizarra del curso",
 resp: "La pizarra lo demuestra sin necesidad de argumentarlo: los artículos de frontera que ellos han elegido se apoyan en los ocho bloques del curso, y ninguno los sustituye. Leer, destilar y defender un artículo en quince minutos es exactamente la competencia profesional que el seminario entrena. Sin discurso de despedida, la pizarra es mejor cierre, y sin comentar públicamente qué presentación ha sido la mejor: las notas se publican individualmente con su justificación.",
 },
};
