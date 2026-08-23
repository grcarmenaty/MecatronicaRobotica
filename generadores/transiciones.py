#!/usr/bin/env python3
"""Añade transición fade a todas las diapositivas de los 8 pptx (post-proceso XML)."""
import glob, os, re, shutil, subprocess, sys, zipfile

TRANS = '<p:transition spd="med"><p:fade/></p:transition>'

def procesar(pptx):
    tmp = pptx + '.tmpdir'
    if os.path.exists(tmp): shutil.rmtree(tmp)
    with zipfile.ZipFile(pptx) as z:
        z.extractall(tmp)
    slides = glob.glob(os.path.join(tmp, 'ppt', 'slides', 'slide*.xml'))
    n = 0
    for s in slides:
        xml = open(s, encoding='utf-8').read()
        if '<p:transition' in xml:
            continue
        if '</p:clrMapOvr>' in xml:
            xml = xml.replace('</p:clrMapOvr>', '</p:clrMapOvr>' + TRANS, 1)
        else:
            xml = xml.replace('</p:sld>', TRANS + '</p:sld>', 1)
        open(s, 'w', encoding='utf-8').write(xml)
        n += 1
    out = os.path.abspath(pptx)
    os.remove(out)
    # rezip desde dentro del directorio para rutas relativas correctas
    subprocess.run(['zip', '-q', '-r', '-X', out, '.'], cwd=tmp, check=True)
    shutil.rmtree(tmp)
    print(f'{os.path.basename(pptx)}: fade en {n}/{len(slides)} diapositivas')

for f in sorted(glob.glob('IQS_B*.pptx')):
    procesar(f)
