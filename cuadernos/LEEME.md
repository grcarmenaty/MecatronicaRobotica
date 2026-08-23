# Cuadernos de clase · 82514 Mecatrónica y Robótica
Curso 2026/27 · IQS Universitat Ramon Llull

29 cuadernos de Google Colab, uno por cada sesión del semestre que se apoya en cálculo,
simulación o programación. Los ocho documentos de apuntes y las presentaciones son
independientes: estos cuadernos son la parte ejecutable.

## Cómo usarlos

Sube toda esta carpeta a tu Google Drive (por ejemplo dentro de `Mecatronica`). Para abrir
uno: botón derecho sobre el fichero → Abrir con → Google Colaboratory. La primera celda
instala lo que falte; en Colab tarda uno o dos minutos, y en los del bloque 4 algo más
porque instala la Robotics Toolbox.

Todos se han ejecutado de principio a fin sin errores antes de entregarse. Ninguno
descarga datos de internet ni necesita GPU: todo es sintético y offline, de modo que
funcionan aunque el aula tenga mala conexión.

## Estructura de cada cuaderno

Cabecera con la sesión, la fecha y las fuentes · celda de instalación · tres a cinco
secciones con explicación antes de cada bloque de código · tres ejercicios para los
estudiantes · soluciones al final · un cierre de «para llevarse de esta sesión».

Las afirmaciones teóricas llevan la misma cita con página que los apuntes, verificada
contra los PDF de la carpeta de bibliografía.

## Índice

### Bloque 3 · Sensores y actuadores
- S08 Características de sensores — transferencia, histéresis, resolución, respuesta dinámica
- S09 Encoders e IMU — cuadratura, deriva del giróscopo, fusión complementaria
- S10 Fuerza, tacto y rango — galga y puente de Wheatstone, LiDAR 2D simulado
- S11 Actuadores eléctricos — modelo del motor DC, curva par-velocidad, punto de operación
- S12 Transmisiones y selección — inercia reflejada, relación de transmisión, selección razonada

### Bloque 4 · Cinemática y estática
- S13 Pose y rotaciones — SO(2)/SE(2), SO(3)/SE(3), bloqueo de cardán, cuaterniones
- S14 Cinemática directa — 2R y 3R a mano, Denavit-Hartenberg, producto de exponenciales
- S15 Taller de cinemática directa 6R — Robotics Toolbox, Puma560 e IRB140
- S16 Cinemática inversa — analítica del 2R, las ocho ramas del PUMA, ikine_LM
- S17 Jacobiano — deducción a mano, diferencias finitas, jacob0
- S18 Singularidades y manipulabilidad — det J, elipsoide, Yoshikawa, número de condición
- S19 Estática y trayectorias — tau = J^T·F, dualidad, quíntico y trapezoidal

### Bloque 5 · Modelado y control en Python
- S20 Modelado y función de transferencia — del motor DC a la FT, polos, constantes de tiempo
- S21 Respuesta con python-control — escalón, indicadores, Bode y márgenes
- S22 Taller de PID — efecto de cada ganancia, Ziegler-Nichols, saturación y anti-windup
- S23 Espacio de estados — conversión, controlabilidad, observabilidad, asignación de polos
- S24 Dinámica y par calculado — Euler-Lagrange del 2R, par calculado frente a PD

### Bloque 6 · Percepción, estimación y SLAM
- S25 Formación de imagen y calibración — modelo estenopeico, distorsión, calibración sintética
- S26 Procesado clásico — convolución, bordes, regiones y momentos, esquinas
- S27 Percepción aprendida — filtros diseñados frente a aprendidos, campo receptivo, clasificador
- S28 Bayes, Kalman y EKF — pasillo discreto, KF en 1D, EKF con baliza
- S29 Localización con EKF — mapa de balizas, elipses de covarianza
- S30 Filtro de partículas y MCL — localización global en pasillo simétrico
- S31 SLAM — EKF-SLAM y optimización de grafo de poses con cierre de bucle

### Bloque 7 · Software robótico y planificación
- S34 Entorno ROS 2 y TF2 — diagnóstico de la instalación local, cadena de transformadas en numpy
- S35 Planificación — mapa de coste, transformada de distancia, A*, PRM, RRT

### Bloque 8 · Robótica basada en aprendizaje
- S38 MDP y Q-learning — gridworld, iteración de valor, Q-learning tabular
- S39 RL profundo y sim-to-real — CartPole, política lineal por CEM, aleatorización de dominio
- S40 Imitación y VLA — clonación de comportamiento, deriva, multimodalidad, modelos VLA

## Sesiones sin cuaderno, y por qué

S01-S07 (bloques 1 y 2) son conceptuales: definiciones, historia, taxonomías, normativa.
S32, S33, S36 y S37 son de ROS 2, Nav2 y MoveIt 2, que no se ejecutan en Colab; el
diagnóstico y la parte conceptual de TF2 están en el cuaderno de S34.
S41 a S43 son seminario de artículos y defensas del proyecto.
