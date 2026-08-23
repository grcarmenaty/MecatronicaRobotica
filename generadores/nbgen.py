#!/usr/bin/env python3
"""Generador de notebooks del curso 82514 con plantilla comun."""
import json, os, re

NBDIR = 'notebooks'
os.makedirs(NBDIR, exist_ok=True)

def md(text):
    src = text.rstrip('\n').split('\n')
    # cada linea debe llevar su salto, como en code(): si no, el renderizador
    # concatena todo el markdown en un solo parrafo
    return {"cell_type": "markdown", "metadata": {},
            "source": [l + '\n' for l in src[:-1]] + [src[-1]] if src else []}

def code(text):
    src = text.rstrip('\n').split('\n')
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
            "source": [l + '\n' for l in src[:-1]] + [src[-1]] if src else []}

def cabecera(ses, titulo, bloque, fecha, dur, objetivo, usa, apuntes):
    return md(f"""# 82514 · Sesión {ses} — {titulo}

**Bloque {bloque}** · {fecha} · {dur}  ·  IQS Universitat Ramon Llull

**Qué hace este cuaderno.** {objetivo}

**Se apoya en:** {usa}

**Cómo usarlo en clase.** Sigue el guion de la sesión {ses} en {apuntes}. Ejecuta la celda de instalación una sola vez al empezar; en Colab tarda un par de minutos. Las celdas marcadas **Ejercicio** son para que los trabajen los estudiantes: las soluciones están al final del cuaderno.

---""")

def instalacion(paquetes, extra=''):
    body = f"""# Ejecutar una sola vez. En Colab tarda 1-2 minutos.
import importlib, subprocess, sys

def asegurar(mods):
    faltan = []
    for pip_name, import_name in mods:
        try:
            importlib.import_module(import_name)
        except ImportError:
            faltan.append(pip_name)
    if faltan:
        print('Instalando:', ' '.join(faltan))
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q'] + faltan, check=False)
    else:
        print('Todo instalado ya.')

asegurar({paquetes!r})"""
    if extra:
        body += '\n\n' + extra
    return code(body)

CIERRE = """---

## Para llevarse de esta sesión

{ideas}

*Cuaderno del curso 82514 Mecatrónica y Robótica · IQS Universitat Ramon Llull · curso 2026/27*"""

def escribir(nombre, celdas):
    nb = {"nbformat": 4, "nbformat_minor": 0,
          "metadata": {"colab": {"name": nombre, "provenance": [], "toc_visible": True},
                       "kernelspec": {"name": "python3", "display_name": "Python 3"},
                       "language_info": {"name": "python"}},
          "cells": celdas}
    ruta = os.path.join(NBDIR, nombre)
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    return ruta
