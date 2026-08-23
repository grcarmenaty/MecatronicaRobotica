#!/usr/bin/env python3
"""Renderiza las ecuaciones del curso como PNG transparentes (pdflatex + pdftocairo).
Genera eq/{clave}.png y eq/dims.json con {clave: [w_px, h_px]}."""
import json, os, subprocess, tempfile
from PIL import Image

NAVY = "1B2A80"
WHITE = "FFFFFF"

# clave: (latex, color)  — \displaystyle implícito
EQS = {
 # B1
 "mdq_j":    (r"J \,=\, \alpha_e\,(I_{ue}-I_e)^2 \,+\, \alpha_m\,(I_{um}-I_m)^2", NAVY),
 "mdq":      (r"\mathrm{MDQ} \,=\, \frac{\alpha_e I_e^2 + \alpha_m I_m^2}{\alpha_e I_{ue}^2 + \alpha_m I_{um}^2}", NAVY),
 # B3 / B5 — motor DC
 "motor3":   (r"\begin{aligned} I\ddot{\theta} + D\dot{\theta} + \tau_{\mathrm{carga}} &= \tau_M \\[2pt] K_e\dot{\theta} + L_a\,\frac{di}{dt} + R_a i &= u \\[2pt] \tau_M &= K_t\, i \end{aligned}", NAVY),
 "tau_kt":   (r"\tau = K_t\, i", NAVY),
 "reduccion":(r"\ddot{\theta} = -\frac{K_1}{I}\,\dot{\theta} + \frac{K_2}{I}\,u - \frac{1}{I}\,\tau_{\mathrm{carga}}", NAVY),
 "tf_vel":   (r"\frac{\Omega(s)}{U(s)} = \frac{K_2}{I s + K_1}", NAVY),
 "tf_pos":   (r"\frac{\Theta(s)}{U(s)} = \frac{K_2}{s\,(I s + K_1)}", NAVY),
 # B4
 "so3":      (r"R^{\top} R = I, \qquad \det R = +1", NAVY),
 "se3_T":    (r"T = \begin{bmatrix} R & p \\ 0 & 1 \end{bmatrix}", NAVY),
 "t_comp":   (r"T_{AC} = T_{AB}\; T_{BC}", NAVY),
 "t_inv":    (r"T^{-1} = \begin{bmatrix} R^{\top} & -R^{\top} p \\ 0 & 1 \end{bmatrix}", NAVY),
 "rodrigues":(r"R = I + \sin\theta\,[\hat{\omega}] + (1-\cos\theta)\,[\hat{\omega}]^2", NAVY),
 "fk2r":     (r"x = a_1\cos q_0 + a_2\cos(q_0{+}q_1), \qquad y = a_1\sin q_0 + a_2\sin(q_0{+}q_1)", NAVY),
 "poe":      (r"T(q) = e^{[S_1]q_1}\, e^{[S_2]q_2} \cdots\, e^{[S_n]q_n}\, M", NAVY),
 "poe_c":    (r"T(q) = \prod_i e^{[S_i]q_i}\, M", NAVY),
 "jac":      (r"\dot{x} = J(q)\,\dot{q}", NAVY),
 "vel_res":  (r"\dot{q} = J^{-1}(q)\,\nu, \qquad q_{k+1} = q_k + \dot{q}\,\delta t", NAVY),
 "yoshikawa":(r"m(q) = \sqrt{\det\!\left( J(q)\, J^{\top}(q) \right)}", NAVY),
 "estatica": (r"\tau = J^{\top}(q)\, F", NAVY),
 "est_deriv":(r"f_{\mathrm{tip}}^{\top} v_{\mathrm{tip}} = \tau^{\top} \dot{q} \;\;\Longrightarrow\;\; \tau = J^{\top}(q)\, f_{\mathrm{tip}}", NAVY),
 # B5
 "analog_mec":(r"m\ddot{x} + c\dot{x} + kx = F", NAVY),
 "analog_ele":(r"L\ddot{q} + R\dot{q} + \frac{q}{C} = v", NAVY),
 "seg_orden":(r"\ddot{e} + 2\zeta\omega_n\,\dot{e} + \omega_n^2\, e = 0", NAVY),
 "mp":       (r"M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}} \times 100\,\%", NAVY),
 "pid":      (r"\tau = K_p\, e + K_i \!\int\! e\, dt + K_d\, \dot{e}", NAVY),
 "planta":   (r"\tau = M\ddot{\theta} + mgr\cos\theta + b\dot{\theta}", NAVY),
 "pd_zw":    (r"\zeta = \frac{b + K_d}{2\sqrt{K_p M}}, \qquad \omega_n = \sqrt{\frac{K_p}{M}}", NAVY),
 "ss":       (r"\dot{x} = A x + B u, \qquad y = C x + D u", NAVY),
 "kalman":   (r"\mathrm{rank}\,[\, B \;\; AB \;\; A^2 B \;\cdots\; A^{n-1} B \,] = n", NAVY),
 "manip":    (r"M(q)\,\ddot{q} + C(q,\dot{q})\,\dot{q} + g(q) = \tau", WHITE),
 "manip_n":  (r"M(q)\,\ddot{q} + C(q,\dot{q})\,\dot{q} + g(q) = \tau", NAVY),
 "lagrange": (r"\tau = \frac{d}{dt}\frac{\partial L}{\partial \dot{q}} - \frac{\partial L}{\partial q}, \qquad L = K - P", NAVY),
 "par_calc": (r"\tau = \hat{M}(q)\left( \ddot{q}_d + K_p e + K_d \dot{e} + K_i\!\int\! e \right) + \hat{h}(q, \dot{q})", NAVY),
 # B6
 "pinhole":  (r"u = f\,\frac{X}{Z}, \qquad v = f\,\frac{Y}{Z}", NAVY),
 # B8
 "qlearn":   (r"Q(s,a) \,\leftarrow\, Q(s,a) + \alpha\left[\, r + \gamma \max_{a'} Q(s',a') - Q(s,a) \right]", NAVY),
}

PLANTILLA = r"""\documentclass[12pt]{article}
\usepackage{amsmath}\usepackage{xcolor}\pagestyle{empty}
\usepackage[paperwidth=60cm,paperheight=8cm,margin=0.3cm]{geometry}
\definecolor{c}{HTML}{%s}
\begin{document}
\color{c}
$\displaystyle %s$
\end{document}"""

os.makedirs("eq", exist_ok=True)
dims = {}
for clave, (latex, color) in EQS.items():
    d = tempfile.mkdtemp()
    open(os.path.join(d, "t.tex"), "w").write(PLANTILLA % (color, latex))
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "t.tex"], cwd=d, capture_output=True, text=True)
    if r.returncode:
        print(f"{clave}: LATEX FALLA"); print(r.stdout[-600:]); continue
    subprocess.run(["pdftocairo", "-png", "-transp", "-r", "600", "t.pdf", "out"], cwd=d, check=True, capture_output=True)
    im = Image.open(os.path.join(d, "out-1.png"))
    bbox = im.getbbox()
    im = im.crop(bbox)
    im.save(f"eq/{clave}.png")
    dims[clave] = list(im.size)
    print(f"{clave}: {im.size}")

json.dump(dims, open("eq/dims.json", "w"))
print("hecho:", len(dims), "ecuaciones")
