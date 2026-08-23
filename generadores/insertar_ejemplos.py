#!/usr/bin/env python:
# -*- coding: utf-8 -*-
"""Inserta 5 diapositivas de ejemplo resuelto en el deck B4 (cinemática)."""
import sys
f = "decks_b3b4b5.js"
src = open(f, encoding="utf-8").read()
fallos = []

def antes_de_seccion(marcador, bloque):
    global src
    i = src.find(marcador)
    if i < 0: fallos.append("sin sección: " + marcador[:50]); return
    src = src[:i] + bloque + "\n" + src[i:]

def antes_de_bloque(ancla, bloque):
    global src
    i = src.find(ancla)
    if i < 0: fallos.append("sin ancla: " + ancla[:50]); return
    j = src.rfind("\n{", 0, i)
    if j < 0: fallos.append("sin llave: " + ancla[:50]); return
    src = src[:j] + "\n" + bloque + src[j:]

E1 = '''
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
'''

E2 = '''
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
'''

E3 = '''
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
'''

E4 = '''
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
'''

E5 = '''
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
'''

antes_de_seccion('sectionSlide(p4, "S14", "Cinemática directa"', E1)
antes_de_seccion('sectionSlide(p4, "S15", "Taller: FK de un 6R en Python"', E2)
antes_de_bloque('contentSlide(p4, "IK numérica y taller con la toolbox"', E3)
antes_de_bloque('contentSlide(p4, "Control de velocidad resuelta"', E4)
antes_de_bloque('contentSlide(p4, "Trayectorias: caminos y leyes temporales"', E5)

open(f, "w", encoding="utf-8").write(src)
if fallos:
    print("FALLOS:", fallos); sys.exit(1)
print("5 ejemplos insertados en B4")
