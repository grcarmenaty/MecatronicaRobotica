#!/usr/bin/env python3
"""Busca en Wikimedia Commons candidatas por concepto, descarga miniaturas y guarda metadatos."""
import json, os, re, sys, time, urllib.parse, urllib.request

UA = {'User-Agent': 'curso82514-educational/1.0 (contacto: profesor IQS)'}
API = 'https://commons.wikimedia.org/w/api.php'

def api(params):
    time.sleep(2.2)
    params = dict(params, format='json')
    url = API + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    return json.load(urllib.request.urlopen(req, timeout=30))

def search(term, n=4):
    r = api({'action':'query','list':'search','srsearch':term,'srnamespace':6,'srlimit':n})
    return [x['title'] for x in r.get('query',{}).get('search',[])]

def info(title):
    r = api({'action':'query','titles':title,'prop':'imageinfo',
             'iiprop':'url|extmetadata|size','iiurlwidth':1400})
    pages = r['query']['pages']
    for _, v in pages.items():
        ii = v.get('imageinfo',[{}])[0]
        md = ii.get('extmetadata',{})
        def g(k): return re.sub(r'<[^>]+>','',md.get(k,{}).get('value','')).strip()
        return {'title': title, 'thumb': ii.get('thumburl'), 'w': ii.get('width'),
                'lic': g('LicenseShortName'), 'autor': g('Artist')[:80]}
    return None

CONCEPTOS = {
 'b2_cobot':        'Universal Robots UR10 arm',
 'b2_delta':        'delta robot',
 'b2_scara':        'SCARA robot',
 'b2_humanoide':    'ASIMO Honda robot',
 'b3_encoder':      'incremental rotary encoder',
 'b3_lidar':        'Velodyne lidar',
 'b4_puma':         'PUMA 560 robot',
 'b4_abb':          'ABB IRB robot',
 'b4_kuka':         'KUKA industrial robot',
 'b5_motor':        'electric motor rotor stator cutaway',
 'b6_estereo':      'stereo camera rig',
 'b7_turtlebot':    'TurtleBot',
 'b7_almacen':      'warehouse logistics robot',
 'b8_ajedrez':      'chess robot arm',
 
 'b1_unimate':      'Unimate industrial robot',
 'b1_jacquard':     'Jacquard loom punched cards',
 'b1_rover':        'Mars rover Perseverance surface NASA',
 'b1_hdd':          'hard disk drive open actuator arm platter',
 'b2_agv':          'automated guided vehicle warehouse robot',
 'b2_cuadrupedo':   'quadruped robot Spot Boston Dynamics',
 'b3_galga':        'strain gauge foil sensor',
 'b3_imu':          'inertial measurement unit MEMS gyroscope chip',
 'b6_camara_obscura':'camera obscura drawing historical',
 'b8_mano':         'robot hand dexterous manipulation',

 'b1_rover2':       'Perseverance Mars rover',
 'b1_watt':         'Watt centrifugal governor steam',
 'b2_cobot2':       'Universal Robots UR5 collaborative',
 'b2_davinci':      'Da Vinci surgical robot system',
 'b2_exo':          'powered exoskeleton rehabilitation',
 'b2_dron':         'quadcopter drone in flight',
 'b2_auto':         'Waymo self-driving car',
 'b3_ultrasonido':  'HC-SR04 ultrasonic sensor module',
 'b3_cmos':         'CMOS image sensor die chip',
 'b3_servo':        'RC servo motor',
 'b3_stepper':      'stepper motor NEMA',
 'b3_harmonic':     'harmonic drive strain wave gear',
 'b4_abb2':         'ABB IRB 6640 industrial robot',
 'b4_soldadura':    'robot welding car body factory',
 'b4_paletizado':   'palletizing robot boxes',
 'b5_bldc':         'brushless DC motor stator winding',
 'b6_estereo2':     'stereo camera vision system',
 'b6_aruco':        'ArUco fiducial marker robot',
 'b6_nube':         'lidar point cloud scan 3D',
 'b7_atlas':        'Atlas humanoid robot DARPA',
 'b7_roomba':       'Roomba robot vacuum underside sensors',
 'b8_ajedrez2':     'chess playing robot arm',
 'b8_rubik':        'robot solving Rubik cube',

 'b2_cobot3':       'Universal Robots cobot',
 'b2_exo2':         'exoskeleton ReWalk suit',
 'b4_soldadura2':   'welding robots assembly line',
 'b4_abb3':         'ABB robot',
 'b5_bldc2':        'brushless DC electric motor',
 'b6_estereo3':     'stereo camera',
 'b6_aruco2':       'fiducial marker ArUco',
 'b7_roomba2':      'Roomba vacuum robot',
 'b8_ajedrez3':     'chess robot',
 'b8_rubik2':       'Rubik cube robot machine',
}

os.makedirs('cand', exist_ok=True)
manifest = {}
previo = json.load(open('candidatas.json')) if os.path.exists('candidatas.json') else {}
manifest.update({k:v for k,v in previo.items() if v})
pend = {k:t for k,t in CONCEPTOS.items() if not manifest.get(k)}
print(f'pendientes: {len(pend)}')
for clave, term in pend.items():
    try:
        titles = search(term)
    except Exception as e:
        print(f'{clave}: ERROR busqueda {e}'); continue
    cands = []
    for i, t in enumerate(titles):
        if not re.search(r'\.(jpe?g|png)$', t, re.I): continue
        try:
            inf = info(t)
        except Exception:
            continue
        if not inf or not inf['thumb'] or (inf['w'] or 0) < 500: continue
        fn = f"cand/{clave}_{i}.jpg"
        try:
            req = urllib.request.Request(inf['thumb'].replace('1400px','480px') if '1400px' in (inf['thumb'] or '') else inf['thumb'], headers=UA)
            open(fn,'wb').write(urllib.request.urlopen(req, timeout=30).read())
            inf['fichero'] = fn
            cands.append(inf)
        except Exception:
            continue
    manifest[clave] = cands
    print(f'{clave}: {len(cands)} candidatas  ' + ' | '.join(c['title'][5:60] for c in cands))

json.dump(manifest, open('candidatas.json','w'), ensure_ascii=False, indent=1)
print('\nguardado candidatas.json')
