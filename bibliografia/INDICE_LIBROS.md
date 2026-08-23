# Guía de fuentes indexadas (curso 82514)

Todos los ficheros en libros/*.txt son extracciones `pdftotext -layout`
con páginas separadas por form-feed (\f). Para verificar una cita:
página del libro = índice de página del PDF (1-based) + OFFSET del fichero.

En Python: `pages = open(f).read().split('\f')`; pages[i] es la página pdf i+1 → página de libro i+1+OFFSET.
Comprueba siempre el número impreso en la cabecera/pie de la página antes de citar.

## De Silva et al. (2016), Mechatronics: Fundamentals and Applications, CRC Press
- desilva_p01.txt  OFFSET = -14  (portada+frontmatter; libro pp. 1-45: cap.1 Mechatronic Engineering pp.1-13; cap.2 Modeling pp.17-35; cap.3 Mechanics of Materials pp.37-45)
- desilva_p02.txt  OFFSET = +45  (libro pp. 46-103: resto cap.3; cap.4 Control of Mechatronic Systems desde p. 85)
- desilva_p03.txt  OFFSET = +103 (libro pp. 104-154: resto cap.4; cap.5 Introduction to Sensors and Signal Processing desde p. 143)

## Corke (2023), Robotics, Vision and Control, 3.ª ed. Python, Springer
- rvc3_p01.txt  OFFSET = -26  (frontmatter; cap.1 pp. 1-19; inicio cap.2 pp. 23-27)
- rvc3_p02.txt  OFFSET = +27  (pp. 28-131: cap.2 pose 2D/3D; cap.3 Time and Motion pp. 87-126, nav. inercial p. 107; inicio cap.4)
- rvc3_p03.txt  OFFSET = +131 (pp. 132-214: cap.4 vehículos [Ackermann p.132, diferencial pp.140-142, omni pp.144-146, cuadrirrotor pp.147-152, holonomía pp.153-155]; cap.5 Navigation pp. 161-214 [planificación, A*, PRM, RRT, D*])
- rvc3_p04.txt  OFFSET = +214 (pp. 215-344: cap.6 Localization and Mapping pp. 215-250 [EKF loc., PF, SLAM, pose graph, odometría lidar]; cap.7 Robot Arm Kinematics pp. 251-290 [FK p.255, config. pp.254-255, prismáticas p.260, PUMA p.261, ETS/DH, IK, trayectorias p.285]; inicio cap.8 Manipulator Velocity pp. 291+)
- rvc3_p05.txt  OFFSET = +345 (pp. 346-438: cap.9 Dynamics and Control pp. 346-380 [actuadores, back-EMF p.346, par calculado p.360]; cap.10 Light and Color; cap.11 inicio p. 427 Obtaining an Image)
- rvc3_p06.txt  OFFSET = +439 (pp. 440-502: cap.11 Images and Image Processing [bordes p.454]; cap.12 Image Feature Extraction desde p. 479)
- rvc3_p07.txt  OFFSET = +501 (pp. 502-578: cap.12 [regiones p.505, deep learning "eclipsed" p.510, puntos p.517]; cap.13 Image Formation desde p. ~543 [proyección perspectiva, calibración])

## Lynch y Park (2017), Modern Robotics, Cambridge
- mr_p01.txt  OFFSET = -18  (frontmatter; pp. 1-388: cap.2 C-space [Def. 2.1 p.12, no holonomía p.32, task/workspace pp.32-33]; cap.3 Rigid-Body Motions; cap.4 Forward Kinematics; cap.5 Velocity Kinematics and Statics [jacobiano, manipulabilidad, estática/dualidad]; cap.6 Inverse Kinematics; cap.7 Closed Chains; cap.8 Dynamics of Open Chains; cap.9 Trajectory Generation; cap.10 Motion Planning inicio)
- mr_p02.txt  OFFSET = +387 (pp. 388-625: resto cap.10 [campos potenciales p.388]; cap.11 Robot Control; cap.12 Grasping; cap.13 Wheeled Mobile Robots)

## Thrun, Burgard y Fox (2005), Probabilistic Robotics, MIT Press
- thrun_p01.txt  OFFSET = -21  (frontmatter; pp. 1-152: cap.2 Recursive State Estimation [filtro de Bayes]; cap.3 Gaussian Filters [KF, EKF p.54]; cap.4 Nonparametric Filters [filtro de partículas]; cap.5 Motion Models [velocity model p.129, odometry model])
- thrun_p02.txt  OFFSET = +152 (pp. 153-324: cap.6 Measurement Models [beam model p.153]; cap.7 Localization Markov/Gaussian [EKF loc. p.192+]; cap.8 Grid and Monte Carlo Localization [MCL]; cap.9 Occupancy Grids p.281+; inicio cap.10 EKF SLAM)
- thrun_p03.txt  OFFSET = +324 (pp. 325-589: cap.10 EKF SLAM; cap.11 GraphSLAM p.337+; cap.12 SEIF; cap.13 FastSLAM p.437+; caps. 14-17 [POMDP, exploración])
- thrun_p04.txt  OFFSET = +588 (pp. 589-648: final cap.17, bibliografía)

## Fraden (2016), Handbook of Modern Sensors, 5.ª ed., Springer
- fraden_p01.txt  OFFSET = -17  (frontmatter; pp. 1-286: cap.1 Data Acquisition; cap.2 Transfer Functions [características, calibración p.23ss]; cap.3 Sensor Characteristics [span, exactitud, histéresis, resolución...]; cap.4 Physical Principles [capacitancia p.63ss, inducción, piezo, efecto Hall...]; caps. 5-6 [interfaces, óptica]; cap.7 inicio)
- fraden_p02.txt  OFFSET = +285 (pp. 286-499: cap.7 Position, Displacement, and Level [encoders, LVDT, magnéticos]; cap.8 Velocity and Acceleration [acelerómetros, giróscopos]; cap.9 Force, Strain, Tactile [galgas p.~355, táctiles p.365]; cap.10 Pressure; cap.11 Flow; cap.12 Acoustic [micrófonos p.435])
- fraden_p03.txt  OFFSET = +498 (pp. 499-664: caps. 14-15 [detectores de radiación/ionización p.513]; cap.16 Temperature [termistores NTC p.538, termopares]; cap.17 Chemical p.578; apéndices p.648)

## Normas y papers (sin PDF; citar por designación)
- ISO 10218-1:2025 / ISO 10218-2:2025 (fabricante/integrador); ISO/TS 15066:2016 (métodos colaborativos cl. 5.5, límites biomecánicos anexo A); ISO 12100:2010 (análisis de riesgos).
- π0: Black et al., 2024, arXiv:2410.24164. GR00T N1: NVIDIA, 2025, arXiv:2503.14734. Isaac Lab: NVIDIA, 2025. Sutton y Barto (2018), Reinforcement Learning: An Introduction, 2.ª ed., MIT Press (citar por capítulo, sin página: no está en la carpeta).
- ROS 2 / Nav2 / MoveIt 2 / Gazebo: documentación oficial (docs.ros.org, docs.nav2.org, moveit.picknik.ai), citar sin página.
