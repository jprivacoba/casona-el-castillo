#!/usr/bin/env python3
"""Valida el bloque espejo SEO y el JSON-LD de web/index.html.

Chequea:
  1. El JSON-LD parsea como JSON válido y tiene la forma @graph esperada.
  2. Cada pregunta del FAQPage aparece LITERALMENTE en el texto visible
     del bloque #seo-content (los <dt>). Google penaliza el FAQ structured
     data cuyas preguntas no están visibles en la página.
  3. Los @id referenciados dentro del @graph existen como nodos del @graph.

Uso:  python3 tool/validar_seo.py [ruta/a/index.html]
"""
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = ROOT / "web" / "index.html"

OK = "\033[32m✓\033[0m"
BAD = "\033[31m✗\033[0m"


def norm(s: str) -> str:
    """Normaliza para comparar: unicode NFC, entidades HTML, espacios colapsados."""
    s = html.unescape(s)
    s = unicodedata.normalize("NFC", s)
    s = s.replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s)


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    src = path.read_text(encoding="utf-8")
    errors = []

    print(f"Validando {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}\n")

    # ── 1. JSON-LD ────────────────────────────────────────────────────────────
    blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', src, re.S
    )
    if not blocks:
        print(f"{BAD} No se encontró ningún bloque application/ld+json")
        return 1

    graphs = []
    for i, block in enumerate(blocks, 1):
        try:
            data = json.loads(block)
        except json.JSONDecodeError as e:
            print(f"{BAD} JSON-LD #{i} no parsea: {e}")
            errors.append("json-parse")
            continue
        print(f"{OK} JSON-LD #{i} parsea correctamente")
        graphs.append(data)

    if not graphs:
        return 1

    nodes = []
    for data in graphs:
        nodes.extend(data.get("@graph", [data]))

    def types_of(node):
        t = node.get("@type", [])
        return t if isinstance(t, list) else [t]

    print(f"{OK} @graph con {len(nodes)} nodos:")
    for n in nodes:
        print(f"    · {'+'.join(types_of(n)):24} {n.get('@id', '(sin @id)')}")

    # tipos que esperamos presentes
    present = {t for n in nodes for t in types_of(n)}
    for req in ("Organization", "WebSite", "WebPage", "EventVenue", "LocalBusiness", "FAQPage"):
        if req in present:
            print(f"{OK} tipo {req} presente")
        else:
            print(f"{BAD} falta el tipo {req}")
            errors.append(f"tipo-{req}")

    # ── 2. @id internos referenciados existen ─────────────────────────────────
    # Un @id puede declararse en un nodo anidado (p.ej. el logo dentro de
    # Organization), así que hay que recorrer todo el árbol, no solo el nivel
    # superior del @graph. Se considera "declarado" el nodo que además del @id
    # trae otras claves; si solo trae @id es una referencia, no una definición.
    def collect_declared(obj, out):
        if isinstance(obj, dict):
            if "@id" in obj and len(obj) > 1:
                out.add(obj["@id"])
            for v in obj.values():
                collect_declared(v, out)
        elif isinstance(obj, list):
            for v in obj:
                collect_declared(v, out)

    declared = set()
    collect_declared(nodes, declared)

    def collect_refs(obj, out):
        if isinstance(obj, dict):
            if set(obj.keys()) == {"@id"}:
                out.add(obj["@id"])
            for v in obj.values():
                collect_refs(v, out)
        elif isinstance(obj, list):
            for v in obj:
                collect_refs(v, out)

    refs = set()
    collect_refs(nodes, refs)
    dangling = {r for r in refs if r.startswith("https://casonafundoelcastillo.cl/#")} - declared
    if dangling:
        for d in sorted(dangling):
            print(f"{BAD} @id referenciado pero no declarado: {d}")
            errors.append("dangling-id")
    else:
        print(f"{OK} los {len(refs)} @id referenciados existen en el @graph")

    # ── 3. FAQ 1:1 contra el texto visible ────────────────────────────────────
    faq_nodes = [n for n in nodes if "FAQPage" in types_of(n)]
    questions = [
        q["name"] for n in faq_nodes for q in n.get("mainEntity", []) if "name" in q
    ]

    seo_match = re.search(
        r'<div id="seo-content".*?>(.*)</div>\s*(?:<script|</body)', src, re.S
    )
    if not seo_match:
        print(f"{BAD} No se encontró el bloque <div id=\"seo-content\">")
        return 1
    seo_html = seo_match.group(1)
    visible_text = norm(strip_tags(seo_html))
    dts = [norm(strip_tags(d)) for d in re.findall(r"<dt>(.*?)</dt>", seo_html, re.S)]

    print(f"\n── FAQPage: {len(questions)} preguntas vs {len(dts)} <dt> visibles ──")
    for q in questions:
        nq = norm(q)
        in_dt = nq in dts
        in_text = nq in visible_text
        if in_dt and in_text:
            print(f"{OK} {q}")
        else:
            detail = []
            if not in_dt:
                detail.append("no coincide con ningún <dt>")
            if not in_text:
                detail.append("no está en el texto visible")
            print(f"{BAD} {q}  →  {', '.join(detail)}")
            errors.append("faq-mismatch")

    # <dt> visibles que no están en el FAQPage (no es error, pero se avisa)
    orphan_dts = [d for d in dts if d not in {norm(q) for q in questions}]
    for d in orphan_dts:
        print(f"⚠  <dt> visible sin entrada en FAQPage: {d}")

    # ── 3b. Paridad con la UI de Flutter (lib/faq_section.dart) ───────────────
    # Las preguntas tienen que estar VISIBLES para el usuario, no solo en el
    # espejo oculto: Google exige que el FAQPage refleje contenido de la página.
    faq_dart = ROOT / "lib" / "faq_section.dart"
    if faq_dart.exists():
        dart_src = faq_dart.read_text(encoding="utf-8")
        # pregunta: '...' — puede venir con comillas simples y concatenación
        dart_qs = [
            norm(m.group(1))
            for m in re.finditer(r"pregunta:\s*'((?:[^'\\]|\\.)*)'", dart_src)
        ]
        print(f"\n── Paridad con la UI Flutter: {len(dart_qs)} preguntas en lib/faq_section.dart ──")
        faltan_en_ui = [q for q in questions if norm(q) not in dart_qs]
        sobran_en_ui = [q for q in dart_qs if q not in {norm(x) for x in questions}]
        if not faltan_en_ui and not sobran_en_ui:
            print(f"{OK} las {len(dart_qs)} preguntas de la UI coinciden con el FAQPage")
        for q in faltan_en_ui:
            print(f"{BAD} en el JSON-LD pero NO visible en la app Flutter: {q}")
            errors.append("faq-no-visible-en-app")
        for q in sobran_en_ui:
            print(f"{BAD} visible en la app pero NO en el JSON-LD: {q}")
            errors.append("faq-app-sin-schema")
    else:
        print(f"\n{BAD} no existe lib/faq_section.dart — el FAQ del schema no sería visible al usuario")
        errors.append("sin-faq-section")

    # ── 4. Salud del espejo ───────────────────────────────────────────────────
    print("\n── Espejo SEO ──")
    chars = len(visible_text)
    h2 = len(re.findall(r"<h2[ >]", seo_html))
    h3 = len(re.findall(r"<h3[ >]", seo_html))
    print(f"{OK} texto visible: {chars} caracteres")
    print(f"{OK} encabezados: {len(re.findall(r'<h1[ >]', seo_html))} h1, {h2} h2, {h3} h3")

    # Buscar .remove() solo en JS real: se descartan los comentarios // y /* */,
    # porque el propio index.html documenta "NO reemplazar por seo.remove()" y
    # eso no debe contar como violación.
    js = "\n".join(re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", src, re.S))
    js_sin_comentarios = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
    js_sin_comentarios = re.sub(r"//[^\n]*", "", js_sin_comentarios)
    if re.search(r"\.remove\(\)|removeChild", js_sin_comentarios):
        print(f"{BAD} se detectó .remove() sobre el espejo SEO — debe usarse aria-hidden + inert")
        errors.append("remove-detectado")
    else:
        print(f"{OK} ningún .remove()/removeChild en el JS del espejo")
    if "aria-hidden" in src and "inert" in src:
        print(f"{OK} el listener usa aria-hidden + inert (no elimina el nodo)")
    else:
        print(f"{BAD} no se encontró el patrón aria-hidden + inert")
        errors.append("sin-aria-inert")

    print()
    if errors:
        print(f"{BAD} {len(errors)} problema(s): {', '.join(sorted(set(errors)))}")
        return 1
    print(f"{OK} Todo válido.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
