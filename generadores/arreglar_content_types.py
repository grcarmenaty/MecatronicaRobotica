#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Restaura la entrada Default jpg en [Content_Types].xml de los pptx.

python-pptx elimina esa entrada al reescribir un fichero, y PowerPoint se queja de
que la presentación está dañada. Este script la vuelve a poner. Es idempotente:
ejecutarlo dos veces no hace nada la segunda.

Uso:  python3 arreglar_content_types.py [fichero.pptx ...]
Sin argumentos procesa todos los IQS_B*.pptx del directorio actual.
"""
import glob
import shutil
import sys
import zipfile

CT = "[Content_Types].xml"
ENTRADA = '<Default Extension="jpg" ContentType="image/jpeg"/>'


def arreglar(ruta):
    with zipfile.ZipFile(ruta) as z:
        nombres = z.namelist()
        datos = {n: z.read(n) for n in nombres}
    ct = datos[CT].decode("utf-8")
    if 'Extension="jpg"' in ct:
        return "ya correcto"
    if not any(n.lower().endswith(".jpg") for n in nombres):
        return "sin jpg, no hace falta"
    ct = ct.replace("<Types ", "<Types ", 1)
    i = ct.find(">", ct.find("<Types ")) + 1
    ct = ct[:i] + ENTRADA + ct[i:]
    datos[CT] = ct.encode("utf-8")
    tmp = ruta + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for n in nombres:
            z.writestr(n, datos[n])
    shutil.move(tmp, ruta)
    return "corregido"


ficheros = sys.argv[1:] or sorted(glob.glob("IQS_B*.pptx"))
if not ficheros:
    print("no hay pptx que procesar")
    sys.exit(0)
for f in ficheros:
    print(f"{f}: {arreglar(f)}")
