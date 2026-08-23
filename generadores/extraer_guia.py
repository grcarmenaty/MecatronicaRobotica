# -*- coding: utf-8 -*-
"""Extractor para la Guía del Profesor 82514.
(a) Secciones «Guía de conducción» de los 8 apuntes -> discusiones (título h2, pregunta de apertura literal, cierre).
(b) 29 notebooks -> pares ejercicio/solución.
Vuelca todo a guia_datos.json.
"""
import json, re, glob, os, sys

BASE = "/home/claude/work/curso_82514"

# ---------------------------------------------------------------- JS string parser
def parse_js_string(s, i):
    """s[i] es la comilla de apertura ". Devuelve (texto, indice tras la comilla de cierre)."""
    assert s[i] == '"'
    out = []
    i += 1
    while i < len(s):
        c = s[i]
        if c == "\\":
            nxt = s[i + 1]
            if nxt == "n":
                out.append("\n")
            elif nxt == "t":
                out.append("\t")
            else:
                out.append(nxt)
            i += 2
            continue
        if c == '"':
            return "".join(out), i + 1
        out.append(c)
        i += 1
    raise ValueError("string sin cerrar")


def tokens_guia(src):
    """Genera (tipo, texto) para h1/h2/h3/p a partir del fragmento JS de la guía.
    Para pRuns concatena los runs de texto en un solo párrafo."""
    toks = []
    for m in re.finditer(r'children\.push\((h1|h2|h3|p|pRuns|box)\(', src):
        kind = m.group(1)
        j = m.end()
        if kind in ("h1", "h2", "h3", "p", "box"):
            # primer argumento string
            while src[j] != '"':
                j += 1
            txt, j2 = parse_js_string(src, j)
            if kind == "box":
                # box(titulo, texto): coger también el texto
                k = j2
                while src[k] != '"':
                    k += 1
                txt2, _ = parse_js_string(src, k)
                toks.append(("box", txt + " — " + txt2))
            else:
                toks.append((kind, txt))
        else:  # pRuns: array de objetos { text: "..." }
            # buscar el cierre '])' del array respetando strings
            depth = 1  # el '(' de pRuns ya está abierto
            k = j
            parts = []
            while k < len(src) and depth > 0:
                c = src[k]
                if c == '"':
                    txt, k = parse_js_string(src, k)
                    parts.append(txt)
                    continue
                if c == "(":
                    depth += 1
                elif c == ")":
                    depth -= 1
                k += 1
            # los strings de un pRuns alternan claves ya filtradas: solo valores text
            toks.append(("p", "".join(parts)))
    return toks


def extraer_discusiones():
    apuntes = [
        (1, "apuntes_b1_v2.js"), (2, "apuntes_b2_v2.js"), (3, "apuntes_b3.js"),
        (4, "apuntes_b4.js"), (5, "apuntes_b5.js"), (6, "apuntes_b6.js"),
        (7, "apuntes_b7.js"), (8, "apuntes_b8.js"),
    ]
    bloques = []
    for nb, fn in apuntes:
        src = open(os.path.join(BASE, fn), encoding="utf-8").read()
        i0 = src.find('h1("Guía de conducción')
        i1 = src.find('h1("Bibliografía', i0)
        frag = src[i0:i1 if i1 > 0 else len(src)]
        toks = tokens_guia(frag)
        discusiones = []
        cur = None
        subseccion = None
        for kind, txt in toks:
            if kind == "h2":
                m = re.search(r"S(\d+)", txt)
                mmin = re.search(r"\(([^)]*min[^)]*)\)", txt)
                if m and mmin:
                    cur = {
                        "bloque": nb,
                        "titulo": txt,
                        "sesion": "S" + m.group(1),
                        "minutos": mmin.group(1),
                        "apertura_parrafos": [],
                        "preguntas": [],
                        "objetivo": "",
                        "cierre": "",
                    }
                    discusiones.append(cur)
                    subseccion = None
                else:
                    cur = None  # «Método general», etc.
                    subseccion = None
            elif kind == "h3" and cur is not None:
                t = txt.lower()
                if "pregunta" in t and "apertura" in t:
                    subseccion = "apertura"
                elif t == "cierre":
                    subseccion = "cierre"
                elif t == "objetivo":
                    subseccion = "objetivo"
                else:
                    subseccion = None
            elif kind == "p" and cur is not None and subseccion:
                if subseccion == "apertura":
                    cur["apertura_parrafos"].append(txt)
                elif subseccion == "cierre":
                    cur["cierre"] = (cur["cierre"] + " " + txt).strip()
                elif subseccion == "objetivo":
                    if not cur["objetivo"]:
                        cur["objetivo"] = txt
        # extraer preguntas literales entre « »
        for d in discusiones:
            segs = []
            for par in d["apertura_parrafos"]:
                segs += re.findall(r"«([^«»]+)»", par)
            d["preguntas"] = [s for s in segs if ("¿" in s or len(s) > 70)]
            del d["apertura_parrafos"]
        bloques.append({"bloque": nb, "fichero": fn, "discusiones": discusiones})
    return bloques


# ---------------------------------------------------------------- notebooks
def extraer_notebooks():
    cuadernos = []
    for path in sorted(glob.glob(os.path.join(BASE, "notebooks", "*.ipynb"))):
        nb = json.load(open(path, encoding="utf-8"))
        fn = os.path.basename(path)
        ses = re.search(r"_S(\d+)_", fn).group(1)
        cells = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "markdown"]
        head = cells[0]
        mt = re.search(r"Sesión S\d+\s*—\s*(.+)", head.splitlines()[0])
        titulo = mt.group(1).strip() if mt else fn
        bloque, fecha, dur = "", "", ""
        mmeta = re.search(r"\*\*Bloque (\d+)\*\*\s*·\s*([^·]+?)\s*·\s*([^·]+?)\s*·", head)
        if mmeta:
            bloque, fecha, dur = mmeta.group(1), mmeta.group(2).strip(), mmeta.group(3).strip()
        # ejercicios
        ejercicios = []
        for c in cells:
            for m in re.finditer(r"### Ejercicio (\d+)\n(.*?)(?=### Ejercicio \d+|\Z)", c, re.S):
                ejercicios.append({"n": int(m.group(1)), "enunciado": m.group(2).strip()})
        # soluciones
        soluciones = {}
        for c in cells:
            if re.search(r"^## Soluciones", c, re.M):
                body = c.split("## Soluciones", 1)[1]
                for m in re.finditer(r"\*\*Ejercicio (\d+)\.\*\*\s*(.*?)(?=\*\*Ejercicio \d+\.\*\*|\Z)", body, re.S):
                    soluciones[int(m.group(1))] = m.group(2).strip()
        for e in ejercicios:
            e["solucion"] = soluciones.get(e["n"], "")
        cuadernos.append({
            "sesion": "S" + ses,
            "fichero": fn,
            "titulo": titulo,
            "bloque": bloque,
            "fecha": fecha,
            "duracion": dur,
            "ejercicios": sorted(ejercicios, key=lambda e: e["n"]),
        })
    return cuadernos


bloques = extraer_discusiones()
cuadernos = extraer_notebooks()

n_disc = sum(len(b["discusiones"]) for b in bloques)
n_ej = sum(len(c["ejercicios"]) for c in cuadernos)
sin_preg = [(d["bloque"], d["titulo"]) for b in bloques for d in b["discusiones"] if not d["preguntas"]]
sin_cierre = [(d["bloque"], d["titulo"]) for b in bloques for d in b["discusiones"] if not d["cierre"]]
sin_sol = [(c["sesion"], e["n"]) for c in cuadernos for e in c["ejercicios"] if not e["solucion"]]

datos = {"bloques": bloques, "cuadernos": cuadernos,
         "conteos": {"discusiones": n_disc, "cuadernos": len(cuadernos), "ejercicios": n_ej}}
json.dump(datos, open(os.path.join(BASE, "guia_datos.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print(f"Discusiones: {n_disc}  (por bloque: {[len(b['discusiones']) for b in bloques]})")
print(f"Cuadernos: {len(cuadernos)}   Ejercicios: {n_ej}")
print("Sin pregunta literal:", sin_preg or "ninguna")
print("Sin cierre:", sin_cierre or "ninguna")
print("Sin solución:", sin_sol or "ninguno")
