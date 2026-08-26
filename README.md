# 82514 · Mecatrónica y Robótica

Material docente completo de la asignatura **82514 Mecatrónica y Robótica** (máster, 6 ECTS),
curso **2026/27**, IQS Universitat Ramon Llull.

El repositorio contiene tanto los documentos finales listos para el aula como el código que
los genera, de modo que cualquier corrección se aplica editando el generador y reconstruyendo,
no retocando el `.docx` o el `.pptx` a mano.

---

## Qué hay aquí

| Carpeta | Contenido |
|---|---|
| `entregables/planificacion/` | Plan del curso 2026/27, tareas y sistema de evaluación, guía del profesor |
| `entregables/apuntes/` | 8 documentos de apuntes, uno por bloque (docx y pdf) |
| `entregables/presentaciones/` | 8 presentaciones, 166 diapositivas con notas del orador y transiciones |
| `entregables/examenes/` | 18 enunciados (3 pruebas x 6 versiones), 3 correcciones con rúbrica y el banco de preguntas, en docx y pdf |
| `entregables/moodle/` | 96 preguntas ABCD en formato GIFT, 12 por bloque, para los cuestionarios de 15 minutos |
| `entregables/guiones/` | Guion narrado de clase del bloque 4, con el discurso literal ligado a cada diapositiva |
| `entregables/referencia/` | Convención terminológica, checklist de fuentes, informe de verificación de citas y análisis de partida |
| `cuadernos/` | 29 cuadernos Jupyter y Colab, uno por sesión con cálculo o programación |
| `generadores/` | Todo el código que produce lo anterior, más las imágenes y ecuaciones que consume |

## Estructura del curso

Ocho bloques, 43 sesiones, con laboratorio propio que no se ha modificado.

| Bloque | Tema | Sesiones |
|---|---|---|
| B1 | Introducción a la mecatrónica | S01 a S04 |
| B2 | Tipología de robots y seguridad | S05 a S07 |
| B3 | Sensores y actuadores | S08 a S12 |
| B4 | Cinemática y estática de manipuladores | S13 a S19 |
| B5 | Modelado y control en Python | S20 a S24 |
| B6 | Percepción, estimación y SLAM | S25 a S31 |
| B7 | Software robótico y planificación | S32 a S37 |
| B8 | Robótica basada en aprendizaje | S38 a S43 |

### Evaluación

| Componente | Peso |
|---|---|
| Exámenes (parcial 1: 15, parcial 2: 15, final: 10) | 40 % |
| Evaluación continua (cuestionarios 12, entregables 8, seminario 10) | 30 % |
| Laboratorio | 20 % |
| Proyecto | 10 % |

Parcial 1 el viernes 6 de noviembre de 2026 (2 h, bloques 1 a 4). Parcial 2 el viernes
11 de diciembre (2 h, bloques 5 a 7). Final en enero (3 h) con recuperación por bloques
para quien tenga un parcial por debajo de 4.

---

## Reconstruir el material

Los generadores están escritos para ejecutarse **desde dentro de `generadores/`**: las rutas
a `media/` son relativas a esa carpeta.

```bash
cd generadores
npm install docx pptxgenjs
pip install python-pptx python-docx numpy pillow --break-system-packages

# Presentaciones (pipeline completo: construir, inyectar notas, aplicar transiciones)
node decks.js && node decks_b3b4b5.js && node decks_b6b7b8.js
python3 notas.py
python3 arreglar_content_types.py
python3 transiciones.py

# Enlaces «Abrir en Colab» en las portadillas de sesión (desde entregables/presentaciones/,
# con la rama del repositorio desde la que deben abrirse los cuadernos)
cd ../entregables/presentaciones
python3 ../../generadores/enlaces_colab.py main
cd ../../generadores

# Apuntes (b1 y b2 usan la versión _v2, que es la vigente)
node apuntes_b1_v2.js && node apuntes_b2_v2.js
for b in 3 4 5 6 7 8; do node apuntes_b$b.js; done

# Exámenes y banco de preguntas
python3 examenes_calc.py && node examenes.js
python3 banco_moodle.py

# Documentos de planificación y referencia
node plan_curso.js && node tareas.js && node guia_profesor.js
node convencion.js && node guion_narrado_b4.js
```

Los ficheros resultantes aparecen en `generadores/`. Cópialos sobre la carpeta
correspondiente de `entregables/` cuando estés conforme con el resultado.

Notas del pipeline de presentaciones, por si algo falla:

* `notas.py` verifica el número de diapositivas y un fragmento del título antes de escribir.
  Si has añadido o quitado diapositivas, hay que resecuenciar las notas en `notas_b*.py`.
* Al reescribir un `.pptx`, python-pptx elimina la entrada `Default Extension="jpg"` de
  `[Content_Types].xml` y PowerPoint avisa de que el fichero está dañado.
  `arreglar_content_types.py` la restaura y es idempotente, así que ejecútalo siempre
  después de `notas.py`.
* Las ecuaciones se generan con LaTeX en `media/ecuaciones.py` y se guardan como PNG
  transparentes en `media/eq/`, con sus dimensiones en `media/dims.json`.
* `enlaces_colab.py` pone el enlace al cuaderno en la portadilla de cada sesión que lo tiene,
  y llama solo a `arreglar_content_types.py` al acabar. Es idempotente. El enlace cuelga de la
  forma, no del texto: un hipervínculo de texto hace que PowerPoint y LibreOffice repinten el
  rótulo del azul del tema, ilegible sobre el azul marino de la portadilla. Hay que pasarle la
  rama desde la que se sirven los cuadernos, porque la URL de Colab la lleva dentro; si se
  renombran o renumeran ficheros de `cuadernos/`, hay que revisar el mapa de sesiones del
  propio script.

---

## Convenciones del material

* **Terminología.** El documento `entregables/referencia/Convencion_Terminologica_82514.docx`
  fija la traducción de unos cuarenta términos y las fuentes en las que se apoya (ISO 8373,
  IEC Electropedia, Barrientos, Ollero y RIAI). Resumen operativo: *pose* es posición más
  orientación, *localización* queda reservada al problema de localization del bloque 6,
  *torsor* traduce wrench y *eje helicoidal* traduce screw axis.
* **Sin guiones largos.** Todo el material evita el em dash de forma deliberada.
* **Sin Matlab ni Simulink.** El curso trabaja en Python: NumPy, python-control,
  Robotics Toolbox for Python, spatialmath y OpenCV.
* **Ejemplos y exámenes.** Los ejemplos resueltos en clase del bloque 4 comparten estructura
  con las partes C y D del parcial 1, con números distintos que no colisionan con ninguna de
  las seis versiones del examen.

## Qué no está en el repositorio

Por derechos de autor y por tamaño, quedan fuera (y están en `.gitignore`) las carpetas de
bibliografía: los extractos de los libros de texto de referencia y los artículos descargados
para preparar los bloques 6 y 8. Las páginas citadas en apuntes y presentaciones remiten a
las ediciones indicadas en cada documento.

## Sobre los PDF

Cada documento está en `.docx` o `.pptx` (la fuente editable) y en `.pdf` (la copia para
imprimir o proyectar). Los PDF de este commit se han regenerado a partir de las fuentes
vigentes, así que reflejan las correcciones de terminología, la notación con subíndices y
los ejemplos resueltos del bloque 4. Si editas una fuente, vuelve a exportar su PDF:

```bash
soffice --headless --convert-to pdf fichero.docx --outdir .
```

## Créditos de las imágenes

Las fotografías proceden de Wikimedia Commons con sus licencias CC correspondientes; la
atribución completa de cada una está en `generadores/media/atribuciones.json` y en el pie de
la diapositiva donde aparece. Las figuras y animaciones son propias del curso, generadas por
los cuadernos y por `generadores/media/figuras.py`.
