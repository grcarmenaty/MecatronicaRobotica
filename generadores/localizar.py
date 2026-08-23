#!/usr/bin/env python3
"""Dado un termino, dice en que pagina(s) impresa(s) del libro aparece."""
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
PAGES = {}
for f in glob.glob('libros/*.txt'):
    PAGES[os.path.basename(f)[:-4]] = open(f, errors='ignore').read().split('\f')

def printed(part, i):
    """numero impreso estimado de la pagina pdf i (0-based)."""
    pg = PAGES[part][i]
    lines = [l.strip() for l in pg.splitlines() if l.strip()]
    lin = OFF[part] + i + 1
    for l in lines[:2] + lines[-2:]:
        for m in re.finditer(r'(?<!\d)(\d{1,4})(?!\d)', l):
            n = int(m.group(1))
            if abs(n - lin) <= 2: return n
    return lin

def find(book, pattern, ctx=0):
    rx = re.compile(pattern, re.I)
    out = []
    for part in BOOKS[book]:
        for i, pg in enumerate(PAGES[part]):
            if rx.search(pg):
                out.append((printed(part, i), part, i))
    return out

if __name__ == '__main__':
    book, pat = sys.argv[1], sys.argv[2]
    hits = find(book, pat)
    if not hits: print(f"  (sin coincidencias de /{pat}/ en {book})")
    for p, part, i in hits[:12]:
        print(f"  {book} p.{p}  [{part} pdf{i+1}]")
