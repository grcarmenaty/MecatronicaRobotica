#!/usr/bin/env python3
"""Ejecuta los notebooks y reporta errores. Uso: python3 probar_nb.py [patron]"""
import sys, glob, json, subprocess, os, re, tempfile

pat = sys.argv[1] if len(sys.argv) > 1 else '*'
files = sorted(glob.glob(f'notebooks/{pat}.ipynb'))
if not files:
    print('sin notebooks que casen con', pat); sys.exit(0)

fallos = 0
for f in files:
    nb = json.load(open(f, encoding='utf-8'))
    # Extraer el codigo, saltando la celda de instalacion (ya esta todo aqui)
    src = ["import matplotlib; matplotlib.use('Agg')\n"]
    for c in nb['cells']:
        if c['cell_type'] != 'code':
            continue
        body = ''.join(c['source'])
        # neutralizar la instalacion pero conservar los imports de esa misma celda
        body = re.sub(r'^\s*subprocess\.run\(.*?\)\s*$', '        pass', body, flags=re.M)
        body = body.replace('plt.show()', 'plt.close("all")')
        src.append(body + '\n')
    script = '\n'.join(src)
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False, encoding='utf-8') as tf:
        tf.write(script); ruta = tf.name
    r = subprocess.run([sys.executable, ruta], capture_output=True, text=True, timeout=600)
    os.unlink(ruta)
    nombre = os.path.basename(f)
    if r.returncode == 0:
        n = sum(1 for c in nb['cells'] if c['cell_type'] == 'code')
        print(f'  OK    {nombre:52s} {n:2d} celdas de codigo')
    else:
        fallos += 1
        err = r.stderr.strip().split('\n')
        print(f'  FALLA {nombre}')
        for l in err[-6:]:
            print('        ', l[:150])
print(f'\n{len(files)-fallos}/{len(files)} notebooks ejecutan sin error')
sys.exit(1 if fallos else 0)
