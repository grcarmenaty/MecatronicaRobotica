#!/usr/bin/env python3
"""Verifica TODAS las citas (Autor, año, p. N) de los apuntes contra el texto de los PDF."""
import re, glob, json, os, unicodedata, sys

BOOKS = {
 'desilva': ['desilva_p01','desilva_p02','desilva_p03'],
 'corke':   ['rvc3_p01','rvc3_p02','rvc3_p03','rvc3_p04','rvc3_p05','rvc3_p06','rvc3_p07'],
 'lynch':   ['mr_p01','mr_p02'],
 'thrun':   ['thrun_p01','thrun_p02','thrun_p03','thrun_p04'],
 'fraden':  ['fraden_p01','fraden_p02','fraden_p03'],
}
OFF = {'desilva_p01':-14,'desilva_p02':45,'desilva_p03':103,
 'rvc3_p01':-26,'rvc3_p02':27,'rvc3_p03':131,'rvc3_p04':214,'rvc3_p05':345,'rvc3_p06':439,'rvc3_p07':501,
 'mr_p01':-18,'mr_p02':387,'thrun_p01':-21,'thrun_p02':152,'thrun_p03':324,'thrun_p04':588,
 'fraden_p01':-17,'fraden_p02':285,'fraden_p03':498}

PAGES, IDX = {}, {}
for f in glob.glob('libros/*.txt'):
    k = os.path.basename(f)[:-4]
    PAGES[k] = open(f, errors='ignore').read().split('\f')
    j = f'libros/{k}.idx.json'
    IDX[k] = {int(a): b for a, b in json.load(open(j)).items()} if os.path.exists(j) else {}

def norm(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+',' ', s)

def resolve(book, pnum):
    """Devuelve (texto_concatenado, como_se_resolvio). Prueba indice impreso y offset."""
    chunks, how = [], []
    for part in BOOKS[book]:
        pgs = PAGES[part]
        # 1) por numero impreso
        for i in IDX.get(part, {}).get(pnum, []):
            chunks.append(pgs[i]); how.append(f'{part}:impreso')
        # 2) por offset lineal, ventana +-2
        base = pnum - OFF[part] - 1
        for d in (0,-1,1,-2,2):
            i = base + d
            if 0 <= i < len(pgs):
                chunks.append(pgs[i])
                if d == 0: how.append(f'{part}:offset')
    return norm(' '.join(chunks)), how

# --- lexico ES -> raiz EN (solo pares inequivocos) ---
LEX = {
'sensor':'sensor','sensores':'sensor','actuador':'actuat','actuadores':'actuat','calibrac':'calibrat',
'camara':'camera','kalman':'kalman','particula':'particle','bayes':'bayes','slam':'slam','grafo':'graph',
'ocupacion':'occupanc','jacobian':'jacobian','singularidad':'singular','singularidades':'singular',
'cinematica':'kinematic','cinematico':'kinematic','trayectoria':'trajector','manipulabilidad':'manipulab',
'rotacion':'rotat','rotaciones':'rotat','planificac':'plan','muestreo':'sampl','potencial':'potential',
'heuristica':'heuristic','borde':'edge','bordes':'edge','convolucion':'convolution','profundidad':'depth',
'perspectiva':'perspectiv','mecatronic':'mechatronic','energia':'energ','acoplado':'coupl','acoplada':'coupl',
'colaborativ':'collaborativ','holonom':'holonom','odometr':'odometr','encoder':'encoder','galga':'strain',
'piezoelectr':'piezoelectr','termopar':'thermocouple','termistor':'thermistor','histeresis':'hysteresis',
'exactitud':'accurac','estabilidad':'stabil','dinamica':'dynamic','dinamico':'dynamic','tactil':'tactile',
'presion':'pressure','fuerza':'force','fuerzas':'force','velocidad':'veloc','gaussian':'gaussian',
'covarianza':'covarianc','linealiza':'lineariz','remuestre':'resampl','imagen':'image','imagenes':'image',
'pixel':'pixel','segmentac':'segment','descriptor':'descriptor','giroscop':'gyro','acelerometro':'accelerom',
'lidar':'lidar','laser':'laser','magnetic':'magnet','capacit':'capacit','transformada':'transform',
'bucle':'loop','celda':'cell','baliza':'landmark','creencia':'belief','recompensa':'reward','politica':'polic',
'refuerzo':'reinforc','esfuerzo':'strain','deformacion':'strain','par':'torque','momento':'torque',
'engranaje':'gear','reductora':'gear','transmision':'transmission','hidraulic':'hydraulic','neumatic':'pneumatic',
'motor':'motor','inductiv':'inductiv','resistiv':'resistiv','optic':'optic','infrarroj':'infrared',
'ultrasonic':'ultrason','temperatura':'temperatur','termic':'thermal','ruido':'noise','filtro':'filter',
'estimacion':'estimat','estado':'state','observacion':'observation','medida':'measurement','medicion':'measurement',
'incertidumbre':'uncertaint','probabilidad':'probabilit','distribucion':'distribut','varianza':'varianc',
'control':'control','realimentacion':'feedback','lazo':'loop','ganancia':'gain','polo':'pole','cero':'zero',
'amortigua':'damp','frecuencia':'frequenc','respuesta':'response','transferencia':'transfer','laplace':'laplace',
'espacio':'space','configuracion':'configurat','libertad':'freedom','articulacion':'joint','articular':'joint',
'eslabon':'link','efector':'effector','muneca':'wrist','prismatic':'prismatic','rotativ':'revolute',
'paralelo':'parallel','serie':'serial','robot':'robot','movil':'mobile','rueda':'wheel','ruedas':'wheel',
'obstaculo':'obstacle','mapa':'map','navegacion':'navigat','localizacion':'localiz','pose':'pose',
'cuaternion':'quaternion','homogenea':'homogeneous','matriz':'matri','vector':'vector','angulo':'angle',
'euler':'euler','lagrange':'lagrang','newton':'newton','raphson':'raphson','denavit':'denavit',
'hartenberg':'hartenberg','exponencial':'exponential','tornillo':'screw','rigido':'rigid','solido':'rigid',
'inercia':'inertia','masa':'mass','gravedad':'gravit','coriolis':'coriolis','friccion':'friction',
'simulacion':'simulat','simulador':'simulat','aprendizaje':'learning','imitacion':'imitat','difusion':'diffusion',
'red':'network','neuronal':'neural','profundo':'deep','entrenamiento':'train','entrenad':'train',
'deteccion':'detect','clasificac':'classif','caracteristica':'feature','esquina':'corner','umbral':'threshold',
'histograma':'histogram','gradiente':'gradient','region':'region','contorno':'contour','estereo':'stereo',
'proyeccion':'projection','intrinsec':'intrinsic','extrinsec':'extrinsic','distorsion':'distortion',
'lente':'lens','foco':'foc','focal':'focal','resolucion':'resolution','sensibilidad':'sensitivit',
'linealidad':'lineari','deriva':'drift','offset':'offset','span':'span','rango':'range',
'seguridad':'safet','riesgo':'risk','norma':'standard','colision':'collision','parada':'stop',
'humano':'human','persona':'human','celda':'cell','fabricacion':'manufactur','industrial':'industrial',
}
STOP = set('para pero como este esta estos estas cada solo tras entre desde donde cuando porque aunque sobre segun mediante ademas tambien mismo misma otro otra todo toda parte partes forma manera caso casos hace hacer puede pueden debe deben ser son fue era hay son sus del las los una uno con por que las les nos'.split())

# nombres propios / acronimos / terminos que se escriben igual en ambos idiomas
def anchors(claim):
    a = set()
    # acronimos y nombres propios (mayuscula interior)
    for w in re.findall(r'\b[A-Z][A-Za-z0-9\-]{2,}\b', claim):
        wl = norm(w).strip()
        if wl and wl not in ('sesion','apartado','bloque','taller','figura','tabla','ecuacion','python','iqs','matlab','simulink','drive','word'):
            a.add(('propio', wl))
    # numeros de figura / ecuacion / tabla
    for m in re.finditer(r'(?:fig\.?|figura|ec\.?|ecuacion|tabla|table)\s*([0-9]+\.[0-9]+)', claim, re.I):
        a.add(('num', m.group(1).replace('.',' ')))
    # lexico
    c = norm(claim)
    for es, en in LEX.items():
        if es in c: a.add(('lex', en))
    return a

AUT = r'(De Silva[^,;)]*|Corke|Lynch y Park|Thrun[^,;)]*|Fraden)'
PAR = re.compile(r'\(([^()]{0,300}?(?:19|20)\d\d[^()]{0,300}?)\)')
SUB = re.compile(AUT + r'[^,;)]{0,30}?,\s*(?:19|20)\d\d,\s*pp?\.\s*(\d{1,4})(?:\s*[-\u2013]\s*(\d{1,4}))?')
KEY = {'De':'desilva','Co':'corke','Ly':'lynch','Th':'thrun','Fr':'fraden'}

def claims(text):
    """Cada (autor, pagina) dentro de un parentesis, incluidas citas compuestas."""
    out = []
    for pm in PAR.finditer(text):
        inner, start = pm.group(1), pm.start()
        seg = text[max(0, start-450):start]
        cut = max(seg.rfind('. '), seg.rfind('\u00bb '), seg.rfind('; '))
        frase = seg[cut+1:] if cut > 0 else seg
        for m in SUB.finditer(inner):
            p1 = int(m.group(2)); p2 = int(m.group(3)) if m.group(3) else None
            out.append((KEY[m.group(1)[:2]], p1, p2, frase.strip(), m.group(0)))
    return out

rows = []
for js in sorted(glob.glob('apuntes_b*.js')):
    if js in ('apuntes_b1.js','apuntes_b2.js'): continue   # sustituidos por _v2
    blk = re.search(r'b(\d)', js).group(1)
    txt = open(js, errors='ignore').read()
    for book, p1, p2, frase, raw in claims(txt):
        pgs_to_try = [p1] + ([p2] if p2 else []) + ([p1+1] if p2 and p2-p1 <= 3 else [])
        best = None
        for pn in pgs_to_try:
            page, how = resolve(book, pn)
            if len(page.strip()) < 60: continue
            A = anchors(frase)
            if not A:
                best = ('SIN_ANCLA', 0, 0, pn); break
            hit = [x for x in A if x[1] in page]
            strong = [x for x in hit if x[0] in ('propio','num')]
            score = (len(strong)*2 + len(hit))
            cand = ('OK' if hit else 'FALLO', len(hit), len(A), pn)
            if best is None or cand[1] > best[1]: best = cand
            if hit: break
        if best is None: best = ('SIN_TEXTO', 0, 0, p1)
        rows.append({'blq': blk, 'js': js, 'libro': book, 'pag': p1, 'pag2': p2,
                     'estado': best[0], 'aciertos': best[1], 'anclas': best[2],
                     'frase': frase[-230:], 'cita': raw})

json.dump(rows, open('verificacion.json','w'), ensure_ascii=False)
from collections import Counter
print(f"TOTAL de citas analizadas: {len(rows)}\n")
c = Counter(r['estado'] for r in rows)
for k, v in c.most_common(): print(f"  {k:12s} {v:5d}   ({100*v/len(rows):.1f}%)")
print("\nPor bloque:")
for b in sorted({r['blq'] for r in rows}):
    sub = [r for r in rows if r['blq']==b]
    cc = Counter(r['estado'] for r in sub)
    print(f"  B{b}: {len(sub):4d} citas  OK={cc['OK']:4d}  FALLO={cc['FALLO']:3d}  sin_ancla={cc['SIN_ANCLA']:3d}  sin_texto={cc['SIN_TEXTO']:3d}")
