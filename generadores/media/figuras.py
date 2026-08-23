#!/usr/bin/env python3
"""Figuras tecnicas y GIFs animados para los decks, con paleta IQS."""
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import os

AZUL, VERDE, NAVY2, GRIS = '#1B2A80', '#1FA355', '#2E3FA3', '#8A8FA8'
plt.rcParams.update({'figure.dpi':110, 'font.family':'sans-serif', 'font.size':13,
                     'axes.edgecolor':'#CCCCCC', 'axes.labelcolor':'#333','xtick.color':'#555','ytick.color':'#555'})
os.makedirs('figs', exist_ok=True); os.makedirs('gifs', exist_ok=True)
rng = np.random.default_rng(42)

def guardar(fig, nombre):
    fig.savefig(f'figs/{nombre}.png', bbox_inches='tight', facecolor='white')
    plt.close(fig); print('fig', nombre)

# ── B3: histeresis ──────────────────────────────────────────
x = np.linspace(0,1,200)
sube = x + 0.06*np.sin(np.pi*x)
baja = x - 0.06*np.sin(np.pi*x)
fig, ax = plt.subplots(figsize=(7.2,4.2))
ax.plot(x, sube, color=AZUL, lw=3, label='carga creciente')
ax.plot(x[::-1], baja[::-1], color=VERDE, lw=3, label='carga decreciente')
ax.annotate('', xy=(0.5, sube[100]), xytext=(0.5, baja[100]),
            arrowprops=dict(arrowstyle='<->', color='crimson', lw=2))
ax.text(0.52, 0.5, 'histéresis', color='crimson')
ax.set_xlabel('magnitud de entrada (normalizada)'); ax.set_ylabel('salida del sensor')
ax.legend(frameon=False); ax.grid(alpha=0.3)
guardar(fig, 'b3_histeresis')

# ── B3: curva par-velocidad del motor DC ────────────────────
w = np.linspace(0, 480, 100)
par = 0.6*(1 - w/480)
carga = 0.00045*w + 0.08
fig, ax = plt.subplots(figsize=(7.2,4.2))
ax.plot(w, par, color=AZUL, lw=3, label='motor (a tensión nominal)')
ax.plot(w, carga, color=VERDE, lw=3, label='carga')
i = np.argmin(np.abs(par-carga))
ax.plot(w[i], par[i], 'o', ms=11, color='crimson', zorder=5)
ax.annotate('punto de operación', xy=(w[i],par[i]), xytext=(w[i]-190,par[i]+0.12),
            arrowprops=dict(arrowstyle='->', color='crimson'))
ax.set_xlabel('velocidad (rad/s)'); ax.set_ylabel('par (N·m)')
ax.legend(frameon=False); ax.grid(alpha=0.3)
guardar(fig, 'b3_par_velocidad')

# ── B3: cuadratura del encoder ──────────────────────────────
t = np.linspace(0, 4, 800)
A = (np.sin(2*np.pi*t) > 0).astype(float)
B = (np.sin(2*np.pi*t - np.pi/2) > 0).astype(float)
fig, ax = plt.subplots(figsize=(7.6,3.6))
ax.step(t, A*0.8 + 1.3, where='post', color=AZUL, lw=2.5)
ax.step(t, B*0.8, where='post', color=VERDE, lw=2.5)
ax.text(-0.28, 1.7, 'A', color=AZUL, fontsize=15, weight='bold')
ax.text(-0.28, 0.4, 'B', color=VERDE, fontsize=15, weight='bold')
ax.axvline(1.0, color='crimson', ls='--', lw=1.5)
ax.text(1.03, 2.28, 'A adelanta a B → giro +', color='crimson', fontsize=11)
ax.set_xlabel('tiempo'); ax.set_yticks([]); ax.set_ylim(-0.3, 2.5); ax.grid(alpha=0.25, axis='x')
guardar(fig, 'b3_cuadratura')

# ── B4: espacio de trabajo 2R + elipses de manipulabilidad ──
a1, a2 = 1.0, 0.8
def fk(q):
    return np.array([a1*np.cos(q[0]) + a2*np.cos(q[0]+q[1]),
                     a1*np.sin(q[0]) + a2*np.sin(q[0]+q[1])])
def J(q):
    s1,c1 = np.sin(q[0]),np.cos(q[0]); s12,c12 = np.sin(q[0]+q[1]),np.cos(q[0]+q[1])
    return np.array([[-a1*s1-a2*s12, -a2*s12],[a1*c1+a2*c12, a2*c12]])
fig, ax = plt.subplots(figsize=(6.8,6.2))
th = np.linspace(0,2*np.pi,200)
ax.fill(*( (a1+a2)*np.cos(th), (a1+a2)*np.sin(th) ), color=AZUL, alpha=0.08)
ax.fill(*( (a1-a2)*np.cos(th), (a1-a2)*np.sin(th) ), color='white')
ax.plot((a1+a2)*np.cos(th), (a1+a2)*np.sin(th), color=AZUL, lw=1.5)
ax.plot((a1-a2)*np.cos(th), (a1-a2)*np.sin(th), color=AZUL, lw=1.5, ls='--')
for q, col in [ (np.array([0.5, 1.9]), VERDE), (np.array([0.9, 0.55]), 'crimson'), (np.array([-0.4, 2.6]), NAVY2) ]:
    p0 = np.zeros(2); p1 = np.array([a1*np.cos(q[0]), a1*np.sin(q[0])]); p2 = fk(q)
    ax.plot([p0[0],p1[0],p2[0]],[p0[1],p1[1],p2[1]], '-o', color=col, lw=3, ms=6)
    U,S,_ = np.linalg.svd(J(q))
    ang = np.degrees(np.arctan2(U[1,0],U[0,0]))
    from matplotlib.patches import Ellipse
    ax.add_patch(Ellipse(p2, 0.55*S[0], 0.55*S[1], angle=ang, fill=False, color=col, lw=2))
ax.set_aspect('equal'); ax.set_xlim(-2,2.3); ax.set_ylim(-1.4,2.3)
ax.set_title('Espacio de trabajo del 2R y elipses de manipulabilidad', fontsize=12)
ax.grid(alpha=0.25)
guardar(fig, 'b4_workspace_elipses')

# ── B5: comparativa P / PD / PID ────────────────────────────
from scipy.signal import lti, step
t = np.linspace(0, 6, 500)
fig, ax = plt.subplots(figsize=(7.4,4.4))
wn = 3.0
for nombre, num, den, col in [
    ('P',   [4],           [1, 0.8, 4],       GRIS),
    ('PD',  [3, 6],        [1, 3.8, 6],       VERDE),
    ('PID', [3, 6.5, 4],   [1, 3.8, 6.5, 4],  AZUL)]:
    _, y = step(lti(num, den), T=t)
    ax.plot(t, y, lw=3, color=col, label=nombre)
ax.axhline(1, color='#999', ls=':', lw=1.5)
ax.set_xlabel('tiempo (s)'); ax.set_ylabel('salida')
ax.legend(frameon=False); ax.grid(alpha=0.3)
guardar(fig, 'b5_p_pd_pid')

# ── B6: proyeccion pinhole ─────────────────────────────────
fig, ax = plt.subplots(figsize=(7.8,4.0))
ax.plot([0,0],[-1.5,1.5], color='#333', lw=3)                      # plano imagen
ax.plot([2,2],[-2,2], color='#bbb', lw=1)                          # centro optico plano
ax.plot(2, 0, 'o', color='crimson', ms=9); ax.text(2.06, -0.35, 'centro óptico', color='crimson')
for (X,Y,col) in [(5.4,1.5,AZUL),(6.5,-1.1,VERDE)]:
    ax.plot(X, Y, 's', color=col, ms=11)
    u = -2*(Y)/(X-2)
    ax.plot([X,0],[Y,u], color=col, lw=1.6, ls='-')
    ax.plot(0, u, 'o', color=col, ms=8)
ax.annotate('f', xy=(1,-1.9), ha='center'); ax.plot([0,2],[-1.75,-1.75], color='#333', lw=1)
ax.plot([0,0.1],[-1.75,-1.75], color='#333')
ax.set_xlim(-1.2,7.2); ax.set_ylim(-2.3,2.3); ax.axis('off')
ax.set_title('El modelo estenopeico: cada punto 3D cae por su rayo — la profundidad se pierde', fontsize=12)
guardar(fig, 'b6_pinhole')

# ── B6: Kalman 1D (del cuaderno S28) ───────────────────────
def kf(mu, s2, u, z, R=0.5, Q=2.0):
    mu_b, s2_b = mu+u, s2+R
    K = s2_b/(s2_b+Q)
    return mu_b+K*(z-mu_b), (1-K)*s2_b, K
T=40; x=0.0; mu, s2 = 0.0, 1.0
xs,zs,mus,sig=[],[],[],[]
r2 = np.random.default_rng(7)
for _ in range(T):
    x += 1 + r2.normal(0,np.sqrt(0.5)); z = x + r2.normal(0,np.sqrt(2.0))
    mu, s2, _ = kf(mu, s2, 1.0, z)
    xs.append(x); zs.append(z); mus.append(mu); sig.append(s2)
xs,zs,mus,sig = map(np.array,(xs,zs,mus,sig))
tt=np.arange(T)
fig, ax = plt.subplots(figsize=(7.4,4.2))
ax.plot(tt,xs,color='#333',lw=2.5,label='posición real')
ax.scatter(tt,zs,s=16,color='crimson',alpha=0.6,label='medida')
ax.plot(tt,mus,color=AZUL,lw=2.5,label='estimación KF')
ax.fill_between(tt, mus-2*np.sqrt(sig), mus+2*np.sqrt(sig), color=AZUL, alpha=0.15, label='±2σ')
ax.legend(frameon=False, loc='upper left'); ax.set_xlabel('paso'); ax.grid(alpha=0.3)
guardar(fig, 'b6_kalman')

# ── B7: A* frente a Dijkstra (nodos expandidos) ────────────
H,W = 40,60
mapa = np.zeros((H,W)); mapa[8:32, 28] = 1; mapa[20, 28:44] = 1
def vecinos(n):
    y,x = n
    for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
        if 0<=y+dy<H and 0<=x+dx<W and mapa[y+dy,x+dx]==0: yield (y+dy,x+dx)
import heapq
def busca(start, goal, heur):
    dist={start:0}; prev={}; exp=set()
    pq=[(heur(start),0,start)]
    while pq:
        _,d,n = heapq.heappop(pq)
        if n in exp: continue
        exp.add(n)
        if n==goal: break
        for v in vecinos(n):
            nd=d+1
            if nd < dist.get(v,1e9):
                dist[v]=nd; prev[v]=n
                heapq.heappush(pq,(nd+heur(v),nd,v))
    cam=[goal]
    while cam[-1]!=start: cam.append(prev[cam[-1]])
    return exp, cam
start, goal = (20,4), (20,55)
h0 = lambda n: 0
h1 = lambda n: abs(n[0]-goal[0])+abs(n[1]-goal[1])
fig, axes = plt.subplots(1,2, figsize=(11.5,3.9))
for ax, h, nombre in [(axes[0],h0,'Dijkstra'),(axes[1],h1,'A* (heurística admisible)')]:
    exp, cam = busca(start, goal, h)
    img = np.ones((H,W,3))
    for (y,x) in exp: img[y,x]=(0.83,0.88,0.98)
    img[mapa==1]=(0.15,0.16,0.3)
    for (y,x) in cam: img[y,x]=(0.12,0.64,0.33)
    ax.imshow(img, origin='lower'); ax.set_title(f'{nombre} — {len(exp)} nodos expandidos', fontsize=12)
    ax.plot(start[1],start[0],'o',color=AZUL); ax.plot(goal[1],goal[0],'*',color='crimson',ms=13)
    ax.set_xticks([]); ax.set_yticks([])
guardar(fig, 'b7_astar_dijkstra')

# ── B8: politica del gridworld ─────────────────────────────
Hg,Wg = 6,8
obst = {(2,2),(2,3),(3,5),(1,5)}; meta=(1,7); peligro=(4,6)
V = np.zeros((Hg,Wg))
for _ in range(60):
    Vn = V.copy()
    for y in range(Hg):
        for x in range(Wg):
            if (y,x)==meta or (y,x) in obst: continue
            vals=[]
            for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                ny,nx = min(max(y+dy,0),Hg-1), min(max(x+dx,0),Wg-1)
                if (ny,nx) in obst: ny,nx=y,x
                r = 1.0 if (ny,nx)==meta else (-1.0 if (ny,nx)==peligro else -0.04)
                vals.append(r + 0.95*V[ny,nx])
            Vn[y,x]=max(vals)
    V=Vn
fig, ax = plt.subplots(figsize=(7.6,5.2))
Vplot = V.copy();
im = ax.imshow(Vplot, cmap='Blues', origin='upper')
for y in range(Hg):
    for x in range(Wg):
        if (y,x) in obst: ax.add_patch(plt.Rectangle((x-0.5,y-0.5),1,1,color='#26284f')); continue
        if (y,x)==meta: ax.text(x,y,'META',ha='center',va='center',color=VERDE,weight='bold'); continue
        if (y,x)==peligro: ax.text(x,y,'−1',ha='center',va='center',color='crimson',weight='bold'); continue
        best=None; bv=-1e9
        for (dy,dx),flecha in [((-1,0),'↑'),((1,0),'↓'),((0,-1),'←'),((0,1),'→')]:
            ny,nx = min(max(y+dy,0),Hg-1), min(max(x+dx,0),Wg-1)
            if (ny,nx) in obst: ny,nx=y,x
            r = 1.0 if (ny,nx)==meta else (-1.0 if (ny,nx)==peligro else -0.04)
            v = r+0.95*V[ny,nx]
            if v>bv: bv,best=v,flecha
        ax.text(x,y,best,ha='center',va='center',color='#123',fontsize=15)
ax.set_title('Política óptima del gridworld (iteración de valor)', fontsize=12)
ax.set_xticks([]); ax.set_yticks([])
guardar(fig, 'b8_gridworld')

# ═══ GIFS ═══════════════════════════════════════════════════
# ── GIF B4: 2R siguiendo trayectoria quintica ──────────────
q0, qf = np.array([2.6, 1.9]), np.array([0.35, 0.8])
tau = np.linspace(0,1,42)
s = 10*tau**3 - 15*tau**4 + 6*tau**5
QQ = q0[None,:] + s[:,None]*(qf-q0)[None,:]
fig, ax = plt.subplots(figsize=(5.6,5.2))
def frame4(i):
    ax.clear()
    th = np.linspace(0,2*np.pi,150)
    ax.plot((a1+a2)*np.cos(th),(a1+a2)*np.sin(th), color='#ccc', lw=1)
    pts = np.array([fk(q) for q in QQ[:i+1]])
    ax.plot(pts[:,0], pts[:,1], color=VERDE, lw=2)
    q = QQ[i]; p1=np.array([a1*np.cos(q[0]),a1*np.sin(q[0])]); p2=fk(q)
    ax.plot([0,p1[0],p2[0]],[0,p1[1],p2[1]],'-o',color=AZUL,lw=5,ms=8)
    ax.plot(*fk(qf),'*',color='crimson',ms=15)
    ax.set_aspect('equal'); ax.set_xlim(-2,2); ax.set_ylim(-2,2)
    ax.set_title('Trayectoria quíntica en espacio articular', fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
an = FuncAnimation(fig, frame4, frames=len(QQ))
an.save('gifs/b4_trayectoria.gif', writer=PillowWriter(fps=14)); plt.close(fig); print('gif b4')

# ── GIF B6: filtro de particulas convergiendo ──────────────
L=20; puertas=[4,9,15]
def vero(z):
    hay=np.zeros(L,bool); hay[puertas]=True
    p=np.where(hay,0.8,0.2)
    return p if z=='p' else 1-p
M=260
part = rng.uniform(0,L,M)
verdad = 2.0
frames_data=[part.copy()]
acciones=[('z','p'),('u',5),('z','p'),('u',3),('z','n'),('u',2),('z','p')]
for tipo,val in acciones:
    if tipo=='u':
        part=(part+val+rng.normal(0,0.35,M))%L; verdad=(verdad+val)%L
    else:
        w=vero(val)[np.clip(part.astype(int),0,L-1)]
        w=w/w.sum(); idx=rng.choice(M,M,p=w); part=part[idx]+rng.normal(0,0.12,M)
    frames_data.append(part.copy())
fig, ax = plt.subplots(figsize=(7.6,2.9))
def frame6(i):
    ax.clear()
    for pu in puertas: ax.axvspan(pu-0.5,pu+0.5,color=VERDE,alpha=0.2)
    ax.hist(frames_data[i], bins=60, range=(0,L), color=AZUL)
    ax.set_xlim(0,L); ax.set_yticks([])
    ax.set_title(f'MCL: la nube de partículas — paso {i}', fontsize=11)
an = FuncAnimation(fig, frame6, frames=len(frames_data))
an.save('gifs/b6_particulas.gif', writer=PillowWriter(fps=1.6)); plt.close(fig); print('gif b6')

# ── GIF B7: RRT creciendo ──────────────────────────────────
lim=10; obst_c=[(5,5,1.6),(3,8,1.1),(7,2,1.2)]
def libre(p):
    return all(np.hypot(p[0]-cx,p[1]-cy)>r for cx,cy,r in obst_c)
start=np.array([0.6,0.6]); goal=np.array([9.3,9.3])
nodes=[start]; parent={0:None}; edges=[]
hist=[]
r3=np.random.default_rng(11)
for it in range(300):
    muestra = goal if r3.random()<0.06 else r3.uniform(0,lim,2)
    d=[np.linalg.norm(muestra-n) for n in nodes]
    j=int(np.argmin(d)); cerca=nodes[j]
    paso = cerca + 0.55*(muestra-cerca)/max(1e-9,np.linalg.norm(muestra-cerca))
    if libre(paso):
        nodes.append(paso); parent[len(nodes)-1]=j; edges.append((cerca,paso))
        hist.append(list(edges))
        if np.linalg.norm(paso-goal)<0.6: break
sel = hist[::max(1,len(hist)//36)] + [hist[-1]]
fig, ax = plt.subplots(figsize=(5.6,5.2))
def frame7(i):
    ax.clear()
    for cx,cy,r in obst_c: ax.add_patch(plt.Circle((cx,cy),r,color='#26284f'))
    for a,b in sel[i]:
        ax.plot([a[0],b[0]],[a[1],b[1]], color=AZUL, lw=1)
    ax.plot(*start,'o',color=VERDE,ms=10); ax.plot(*goal,'*',color='crimson',ms=15)
    ax.set_xlim(0,lim); ax.set_ylim(0,lim); ax.set_aspect('equal')
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title('RRT: las muestras tiran del árbol', fontsize=11)
an = FuncAnimation(fig, frame7, frames=len(sel))
an.save('gifs/b7_rrt.gif', writer=PillowWriter(fps=9)); plt.close(fig); print('gif b7')

# ── GIF B5: efecto de subir Kp ─────────────────────────────
fig, ax = plt.subplots(figsize=(6.4,4.0))
Kps = np.linspace(1, 30, 34)
def frame5(i):
    ax.clear()
    Kp = Kps[i]
    _, y = step(lti([Kp],[1, 2, Kp]), T=np.linspace(0,6,400))
    ax.plot(np.linspace(0,6,400), y, color=AZUL, lw=3)
    ax.axhline(1, color='#999', ls=':')
    ax.set_ylim(0,1.9); ax.set_xlabel('tiempo (s)')
    ax.set_title(f'Subir Kp: más rápido, más sobreoscilación   (Kp = {Kp:.0f})', fontsize=11)
    ax.grid(alpha=0.3)
an = FuncAnimation(fig, frame5, frames=len(Kps))
an.save('gifs/b5_kp.gif', writer=PillowWriter(fps=8)); plt.close(fig); print('gif b5')

# ── GIF B8: iteracion de valor propagandose ────────────────
Vv = np.zeros((Hg,Wg)); framesV=[Vv.copy()]
for _ in range(18):
    Vn=Vv.copy()
    for y in range(Hg):
        for x in range(Wg):
            if (y,x)==meta or (y,x) in obst: continue
            vals=[]
            for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                ny,nx=min(max(y+dy,0),Hg-1),min(max(x+dx,0),Wg-1)
                if (ny,nx) in obst: ny,nx=y,x
                r=1.0 if (ny,nx)==meta else (-1.0 if (ny,nx)==peligro else -0.04)
                vals.append(r+0.95*Vv[ny,nx])
            Vn[y,x]=max(vals)
    Vv=Vn; framesV.append(Vv.copy())
fig, ax = plt.subplots(figsize=(6.4,4.4))
def frame8(i):
    ax.clear()
    ax.imshow(framesV[i], cmap='Blues', vmin=-1, vmax=1.2, origin='upper')
    for (y,x) in obst: ax.add_patch(plt.Rectangle((x-0.5,y-0.5),1,1,color='#26284f'))
    ax.text(meta[1],meta[0],'META',ha='center',va='center',color=VERDE,weight='bold',fontsize=9)
    ax.text(peligro[1],peligro[0],'−1',ha='center',va='center',color='crimson',weight='bold')
    ax.set_title(f'Iteración de valor: el valor se propaga desde la meta (barrido {i})', fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
an = FuncAnimation(fig, frame8, frames=len(framesV))
an.save('gifs/b8_valor.gif', writer=PillowWriter(fps=2.5)); plt.close(fig); print('gif b8')

print('\nlisto')
