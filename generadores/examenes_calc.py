#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Calcula los parámetros y las soluciones de las 6 versiones (A-F) de los 3 exámenes.
Todas las soluciones numéricas se calculan aquí (numpy), nada a mano. Emite examenes_datos.json."""
import json, math, random
import numpy as np

VERS = "ABCDEF"
banco = json.load(open("banco.json", encoding="utf-8"))

def preguntas_bloques(bloques):
    out = []
    for b in bloques:
        for q in banco[str(b)]:
            out.append({"bloque": b, "enun": q[0], "ops": q[1], "corr": q[2]})
    return out

def seleccion_test(pool, n, offset, paso, semilla):
    idxs, vistos = [], set()
    k = 0
    while len(idxs) < n:
        i = (offset + paso * k) % len(pool)
        if i not in vistos:
            vistos.add(i); idxs.append(i)
        k += 1
    rng = random.Random(semilla)
    sel = []
    for i in idxs:
        q = pool[i]
        orden = list(range(4)); rng.shuffle(orden)
        ops = [q["ops"][j] for j in orden]
        corr_letra = "ABCD"[orden.index(q["corr"])]
        sel.append({"enun": q["enun"], "ops": ops, "corr": corr_letra})
    return sel

D = {"P1": [], "P2": [], "F": []}
r2 = lambda x: round(float(x), 2)
r3 = lambda x: round(float(x), 3)
gdeg = lambda x: round(math.degrees(float(x)), 1)

# ══ PARCIAL 1 (B1-B4) ══
pool14 = preguntas_bloques([1, 2, 3, 4])
f_sig  = [820, 640, 950, 730, 880, 560]
fs_err = [900, 700, 1000, 800, 950, 600]
mdq_p  = [(0.82,0.76,0.95,0.90),(0.78,0.84,0.92,0.94),(0.80,0.70,0.90,0.88),
          (0.86,0.74,0.96,0.86),(0.75,0.81,0.88,0.93),(0.83,0.79,0.94,0.91)]
c2r = [
 dict(a1=0.5, a2=0.3, q1=30, q2=45, P=(0.75, 0.15), Pfuera=(0.9, 0.2),  F=(10, 0)),
 dict(a1=0.6, a2=0.4, q1=20, q2=60, P=(0.80, 0.30), Pfuera=(0.1, 0.05), F=(0, 12)),
 dict(a1=0.4, a2=0.3, q1=40, q2=30, P=(0.55, 0.25), Pfuera=(0.8, 0.1),  F=(8, 6)),
 dict(a1=0.5, a2=0.4, q1=25, q2=50, P=(0.70, 0.35), Pfuera=(1.0, 0.0),  F=(12, 0)),
 dict(a1=0.7, a2=0.4, q1=15, q2=70, P=(0.85, 0.40), Pfuera=(0.2, 0.1),  F=(0, 10)),
 dict(a1=0.6, a2=0.3, q1=35, q2=40, P=(0.75, 0.30), Pfuera=(1.0, 0.3),  F=(9, 5)),
]
for v in range(6):
    letra = VERS[v]
    test = seleccion_test(pool14, 10, 3 + v, 5, 100 + v)
    f = f_sig[v]; fe = fs_err[v]
    Ie, Im, Iue, Ium = mdq_p[v]
    mdq = (Ie**2 + Im**2) / (Iue**2 + Ium**2)
    c = c2r[v]
    a1, a2 = c["a1"], c["a2"]
    q1, q2 = math.radians(c["q1"]), math.radians(c["q2"])
    x = a1*math.cos(q1) + a2*math.cos(q1+q2)
    y = a1*math.sin(q1) + a2*math.sin(q1+q2)
    phi = c["q1"] + c["q2"]
    rmin, rmax = abs(a1-a2), a1+a2
    Pf = c["Pfuera"]; rPf = math.hypot(*Pf)
    alcanzable_f = rmin <= rPf <= rmax
    xd, yd = c["P"]
    c2v = (xd**2 + yd**2 - a1**2 - a2**2) / (2*a1*a2)
    assert -1 <= c2v <= 1, f"P1 v{letra}: punto IK no alcanzable (c2={c2v})"
    q2a = math.acos(c2v); q2b = -q2a
    def q1_de(q2_):
        return math.atan2(yd, xd) - math.atan2(a2*math.sin(q2_), a1 + a2*math.cos(q2_))
    q1a, q1b = q1_de(q2a), q1_de(q2b)
    s1, c1 = math.sin(q1a), math.cos(q1a)
    s12, c12 = math.sin(q1a+q2a), math.cos(q1a+q2a)
    J = np.array([[-a1*s1 - a2*s12, -a2*s12], [a1*c1 + a2*c12, a2*c12]])
    detJ = a1*a2*math.sin(q2a)
    F = np.array(c["F"])
    tau = J.T @ F
    xv = a1*math.cos(q1a) + a2*math.cos(q1a+q2a); yv = a1*math.sin(q1a) + a2*math.sin(q1a+q2a)
    assert abs(xv-xd) < 1e-9 and abs(yv-yd) < 1e-9
    D["P1"].append(dict(version=letra, test=test,
        B=dict(f=f, fs_min=2*f, fs_prac=round(2.56*f), fs_err=fe, alias=abs(fe-f),
               Ie=Ie, Im=Im, Iue=Iue, Ium=Ium, mdq=r3(mdq)),
        C=dict(a1=a1, a2=a2, q1=c["q1"], q2=c["q2"], x=r3(x), y=r3(y), phi=phi,
               rmin=r3(rmin), rmax=r3(rmax), Pfuera=Pf, rPf=r3(rPf), alcanzable=alcanzable_f),
        Dd=dict(P=c["P"], c2=r3(c2v), q2a=gdeg(q2a), q2b=gdeg(q2b), q1a=gdeg(q1a), q1b=gdeg(q1b),
                J=[[r3(J[0,0]), r3(J[0,1])], [r3(J[1,0]), r3(J[1,1])]], detJ=r3(detJ),
                F=c["F"], tau=[r3(tau[0]), r3(tau[1])])))

# ══ PARCIAL 2 (B5-B7) ══
pool57 = preguntas_bloques([5, 6, 7])
ctrl = [
 dict(M=0.5, b=0.1, zeta=0.7, wn=4.0, m=1.0, r=0.10),
 dict(M=0.4, b=0.2, zeta=0.8, wn=5.0, m=0.8, r=0.12),
 dict(M=0.6, b=0.1, zeta=0.7, wn=3.0, m=1.2, r=0.10),
 dict(M=0.5, b=0.15, zeta=0.9, wn=4.0, m=1.0, r=0.15),
 dict(M=0.3, b=0.1, zeta=0.8, wn=6.0, m=0.6, r=0.10),
 dict(M=0.8, b=0.2, zeta=0.7, wn=3.5, m=1.5, r=0.12),
]
kal = [
 dict(x0=2.0, P0=1.0, Q=0.25, R=0.5, z=3.0),
 dict(x0=5.0, P0=0.8, Q=0.20, R=1.0, z=4.2),
 dict(x0=1.0, P0=1.5, Q=0.30, R=0.6, z=1.8),
 dict(x0=3.0, P0=0.5, Q=0.25, R=0.75, z=2.2),
 dict(x0=4.0, P0=1.2, Q=0.40, R=0.8, z=5.0),
 dict(x0=0.0, P0=1.0, Q=0.30, R=1.2, z=1.5),
]
rejillas = [
 dict(S=(0,0), G=(4,4), obs=[(1,1),(1,2),(1,3),(3,1),(3,2)]),
 dict(S=(0,0), G=(4,4), obs=[(0,2),(1,2),(2,2),(3,2)]),
 dict(S=(4,0), G=(0,4), obs=[(2,1),(2,2),(2,3),(1,1)]),
 dict(S=(0,0), G=(4,3), obs=[(1,1),(2,1),(3,1),(3,3)]),
 dict(S=(0,4), G=(4,0), obs=[(1,3),(2,3),(3,3),(2,1)]),
 dict(S=(0,0), G=(3,4), obs=[(1,0),(1,1),(1,2),(3,2)]),
]
def bfs_optimo(S, G, obs):
    from collections import deque
    obs = set(map(tuple, obs))
    vis = {tuple(S): 0}
    dq = deque([tuple(S)])
    while dq:
        u = dq.popleft()
        if u == tuple(G):
            return vis[u]
        for d in ((1,0),(-1,0),(0,1),(0,-1)):
            w = (u[0]+d[0], u[1]+d[1])
            if 0 <= w[0] < 5 and 0 <= w[1] < 5 and w not in obs and w not in vis:
                vis[w] = vis[u] + 1; dq.append(w)
    return None
for v in range(6):
    letra = VERS[v]
    test = seleccion_test(pool57, 10, 2 + v, 7, 200 + v)
    cc = ctrl[v]
    M, b, zeta, wn = cc["M"], cc["b"], cc["zeta"], cc["wn"]
    Kp = M * wn**2
    Kd = 2*zeta*wn*M - b
    assert Kd > 0
    Mp = math.exp(-math.pi*zeta/math.sqrt(1-zeta**2)) * 100
    ess = cc["m"]*9.81*cc["r"] / Kp
    kk = kal[v]
    Pm = kk["P0"] + kk["Q"]
    K = Pm / (Pm + kk["R"])
    xh = kk["x0"] + K*(kk["z"] - kk["x0"])
    Pp = (1-K)*Pm
    g = rejillas[v]
    S, G, obs = g["S"], g["G"], g["obs"]
    lopt = bfs_optimo(S, G, obs)
    manh = lambda a, bb: abs(a[0]-bb[0]) + abs(a[1]-bb[1])
    vecinos = []
    for d in ((1,0),(-1,0),(0,1),(0,-1)):
        w = (S[0]+d[0], S[1]+d[1])
        if 0 <= w[0] < 5 and 0 <= w[1] < 5 and w not in [tuple(o) for o in obs]:
            vecinos.append(dict(celda=list(w), gcost=1, h=manh(w, G), f=1+manh(w, G)))
    fmin = min(x["f"] for x in vecinos)
    expandir = [x["celda"] for x in vecinos if x["f"] == fmin]
    D["P2"].append(dict(version=letra, test=test,
        B=dict(M=M, b=b, zeta=zeta, wn=wn, Kp=r3(Kp), Kd=r3(Kd), Mp=r2(Mp),
               m=cc["m"], r=cc["r"], ess_rad=r3(ess), ess_deg=r2(math.degrees(ess))),
        C=dict(**kk, Pm=r3(Pm), K=r3(K), xh=r3(xh), Pp=r3(Pp)),
        Dd=dict(S=list(S), G=list(G), obs=[list(o) for o in obs], hS=manh(S, G),
                vecinos=vecinos, expandir=expandir, lopt=lopt)))

# ══ FINAL (B1-B8) ══
pool18 = preguntas_bloques([1, 2, 3, 4, 5, 6, 7, 8])
casos_iso = [
 "Célula de plegado: un robot de 6 ejes alimenta una plegadora; un operario retira las piezas plegadas de una mesa contigua varias veces por hora.",
 "Estación de paletizado con un cobot junto a un pasillo peatonal señalizado por el que circulan carretillas y personas.",
 "Célula de pulido: un cobot con herramienta rotativa pule piezas metálicas; el operario recarga la bandeja de piezas cada pocos minutos.",
 "Puesto de inspección compartido: robot y operario trabajan sobre la misma mesa; el robot presenta la pieza y la persona la inspecciona y marca defectos.",
 "Célula de soldadura por puntos con recargas manuales de componentes dos veces por turno; el resto del tiempo la célula trabaja sola.",
 "Zona de kitting: un AMR cruza el área para recoger cajas que un brazo deposita en su plataforma; hay personal de almacén trabajando cerca.",
]
c2r_f = [
 dict(a1=0.4, a2=0.25, q1=50, q2=35, M=0.4, b=0.1, zeta=0.8, wn=5.0),
 dict(a1=0.5, a2=0.35, q1=30, q2=55, M=0.5, b=0.2, zeta=0.7, wn=4.0),
 dict(a1=0.6, a2=0.35, q1=20, q2=45, M=0.6, b=0.1, zeta=0.9, wn=3.0),
 dict(a1=0.45, a2=0.3, q1=40, q2=50, M=0.3, b=0.1, zeta=0.7, wn=6.0),
 dict(a1=0.55, a2=0.3, q1=25, q2=65, M=0.7, b=0.2, zeta=0.8, wn=3.5),
 dict(a1=0.5, a2=0.3, q1=45, q2=30, M=0.45, b=0.15, zeta=0.75, wn=4.5),
]
bayes_p = [
 dict(hit=0.7, fa=0.3), dict(hit=0.75, fa=0.25), dict(hit=0.65, fa=0.30),
 dict(hit=0.8, fa=0.3), dict(hit=0.7, fa=0.2), dict(hit=0.72, fa=0.28),
]
qlrn = [
 dict(Q=2.0, r=1.0, g=0.9, a=0.5, maxQ=3.0),
 dict(Q=1.5, r=0.0, g=0.9, a=0.4, maxQ=2.5),
 dict(Q=0.0, r=5.0, g=0.8, a=0.5, maxQ=1.0),
 dict(Q=3.0, r=-1.0, g=0.9, a=0.3, maxQ=3.0),
 dict(Q=2.5, r=2.0, g=0.95, a=0.5, maxQ=2.0),
 dict(Q=1.0, r=1.0, g=0.9, a=0.6, maxQ=4.0),
]
for v in range(6):
    letra = VERS[v]
    test = seleccion_test(pool18, 12, v, 8, 300 + v)
    c = c2r_f[v]
    a1, a2 = c["a1"], c["a2"]
    q1, q2 = math.radians(c["q1"]), math.radians(c["q2"])
    x = a1*math.cos(q1) + a2*math.cos(q1+q2)
    y = a1*math.sin(q1) + a2*math.sin(q1+q2)
    s1, c1 = math.sin(q1), math.cos(q1)
    s12, c12 = math.sin(q1+q2), math.cos(q1+q2)
    J = np.array([[-a1*s1 - a2*s12, -a2*s12], [a1*c1 + a2*c12, a2*c12]])
    detJ = a1*a2*math.sin(q2)
    Kp = c["M"]*c["wn"]**2
    Kd = 2*c["zeta"]*c["wn"]*c["M"] - c["b"]
    assert Kd > 0
    bp = bayes_p[v]
    post1 = bp["hit"]*0.5 / (bp["hit"]*0.5 + bp["fa"]*0.5)
    post2 = bp["hit"]*post1 / (bp["hit"]*post1 + bp["fa"]*(1-post1))
    ql = qlrn[v]
    td = ql["r"] + ql["g"]*ql["maxQ"] - ql["Q"]
    Qn = ql["Q"] + ql["a"]*td
    D["F"].append(dict(version=letra, test=test, caso=casos_iso[v],
        C=dict(a1=a1, a2=a2, q1=c["q1"], q2=c["q2"], x=r3(x), y=r3(y), phi=c["q1"]+c["q2"],
               J=[[r3(J[0,0]), r3(J[0,1])], [r3(J[1,0]), r3(J[1,1])]], detJ=r3(detJ),
               M=c["M"], b=c["b"], zeta=c["zeta"], wn=c["wn"], Kp=r3(Kp), Kd=r3(Kd)),
        Dd=dict(hit=bp["hit"], fa=bp["fa"], post1=r3(post1), post2=r3(post2)),
        E=dict(**ql, td=r3(td), Qn=r3(Qn))))

json.dump(D, open("examenes_datos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("examenes_datos.json listo:", len(D["P1"]), "P1 ·", len(D["P2"]), "P2 ·", len(D["F"]), "Final")
