#!/usr/bin/env python3
"""
Generador de materiales de marketing - Casona Fundo El Castillo
Produce 5 afiches + 1 díptico en JPG y PDF
"""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os

BASE = r"c:\Users\jpriv\OneDrive\Documentos\casona-el-castillo"
IMG  = os.path.join(BASE, "assets", "images")
OUT  = os.path.join(BASE, "marketing")
os.makedirs(OUT, exist_ok=True)

# ── COLORES (del theme.dart) ──────────────────────────────────────────────────
DARK      = (30,  23,  16)
GOLD      = (184, 147, 90)
GOLD_L    = (212, 180, 131)
GOLD_D    = (140, 105, 55)
CREAM     = (250, 247, 243)
CREAM_ALT = (243, 235, 224)
SAGE      = (107, 122, 92)
TEXT_C    = (42,  33,  24)
MUTED     = (138, 128, 119)
WHITE     = (255, 255, 255)

# ── MARCA ─────────────────────────────────────────────────────────────────────
NOMBRE1  = "Casona Fundo"
NOMBRE2  = "El Castillo"
TAGLINE  = "Un lugar con historia"
SUBTAG   = "Venue de Eventos · Patrimonio Histórico"
UBICACION= "Los Andes, Valparaíso · Chile"
IG       = "@casonafundoelcastillo"
WA       = "+56 9 9779 4301"
WEB      = "casonafundoelcastillo.cl"
DESDE    = "Más de 80 años de historia"
PARQUE   = "Parque centenario"

# ── FONTS ─────────────────────────────────────────────────────────────────────
F = r"C:\Windows\Fonts"
PALATINO      = os.path.join(F, "pala.ttf")
PALATINO_B    = os.path.join(F, "palab.ttf")
PALATINO_I    = os.path.join(F, "palai.ttf")
PALATINO_BI   = os.path.join(F, "palabi.ttf")
SEGOE         = os.path.join(F, "segoeui.ttf")
SEGOE_B       = os.path.join(F, "segoeuib.ttf")
SEGOE_L       = os.path.join(F, "segoeuil.ttf")
SEGOE_SB      = os.path.join(F, "seguisb.ttf")

def fnt(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

# ── HELPERS ───────────────────────────────────────────────────────────────────
def ct(draw, x, y, text, font, fill, anchor="mm"):
    draw.text((x, y), text, font=font, fill=fill, anchor=anchor)

def hline(draw, x1, y, x2, fill=GOLD, w=2):
    draw.line([(x1, y), (x2, y)], fill=fill, width=w)

def vline(draw, x, y1, y2, fill=GOLD, w=2):
    draw.line([(x, y1), (x, y2)], fill=fill, width=w)

def load_img(path, size, crop=True):
    if not os.path.exists(path):
        img = Image.new("RGBA", size, (*DARK, 255))
        return img
    img = Image.open(path).convert("RGBA")
    if crop:
        ir = img.width / img.height
        tr = size[0] / size[1]
        if ir > tr:
            nw = int(img.height * tr)
            l  = (img.width - nw) // 2
            img = img.crop((l, 0, l + nw, img.height))
        else:
            nh = int(img.width / tr)
            t  = (img.height - nh) // 2
            img = img.crop((0, t, img.width, t + nh))
    return img.resize(size, Image.LANCZOS)

def dark_overlay(img, alpha=140):
    ov = Image.new("RGBA", img.size, (0, 0, 0, alpha))
    return Image.alpha_composite(img.convert("RGBA"), ov)

def gradient_v(img, a0=0, a1=220, color=DARK):
    """Gradiente vertical top→bottom."""
    ov   = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(ov)
    w, h = img.size
    for i in range(h):
        a = int(a0 + (a1 - a0) * i / max(h - 1, 1))
        draw.line([(0, i), (w, i)], fill=(*color, a))
    return Image.alpha_composite(img.convert("RGBA"), ov)

def gradient_h(img, a0=0, a1=220, color=DARK):
    """Gradiente horizontal left→right."""
    ov   = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(ov)
    w, h = img.size
    for i in range(w):
        a = int(a0 + (a1 - a0) * i / max(w - 1, 1))
        draw.line([(i, 0), (i, h)], fill=(*color, a))
    return Image.alpha_composite(img.convert("RGBA"), ov)

def corner_frame(draw, x1, y1, x2, y2, color=GOLD, size=40, w=2):
    """Marcos de esquinas estilo clásico."""
    corners = [(x1,y1),(x2,y1),(x1,y2),(x2,y2)]
    signs   = [(1,1),(-1,1),(1,-1),(-1,-1)]
    for (cx,cy),(sx,sy) in zip(corners, signs):
        draw.line([(cx,cy),(cx+sx*size,cy)], fill=color, width=w)
        draw.line([(cx,cy),(cx,cy+sy*size)], fill=color, width=w)

def save(img, name):
    rgb  = img.convert("RGB")
    jpg  = os.path.join(OUT, name + ".jpg")
    pdf  = os.path.join(OUT, name + ".pdf")
    rgb.save(jpg, "JPEG", quality=95, dpi=(300, 300))
    rgb.save(pdf, "PDF", resolution=150)
    print(f"  OK {name}.jpg  +  .pdf")
    return rgb

# =============================================================================
# AFICHE 1 — "Elegancia Oscura"  1080×1080  (Instagram cuadrado)
# Fondo oscuro premium, foto central con marco dorado, tipografía clásica
# =============================================================================
def afiche1():
    W, H = 1080, 1080
    canvas = Image.new("RGB", (W, H), DARK)
    draw   = ImageDraw.Draw(canvas)

    # Textura sutil: franja horizontal oscura en parte superior
    for i in range(200):
        a = int(255 * (1 - i / 200) * 0.3)
        draw.line([(0, i), (W, i)], fill=(255, 240, 200))  # tono cálido casi invisible

    # Imagen hero con marco
    MARGIN = 60
    IMG_Y1, IMG_Y2 = 230, 680
    hero = load_img(os.path.join(IMG, "hero.jpg"), (W - MARGIN*2, IMG_Y2 - IMG_Y1))
    hero = dark_overlay(hero, 50)
    canvas.paste(hero.convert("RGB"), (MARGIN, IMG_Y1))

    draw = ImageDraw.Draw(canvas)
    # Marco dorado exterior alrededor de la foto
    draw.rectangle([MARGIN-3, IMG_Y1-3, W-MARGIN+3, IMG_Y2+3], outline=GOLD_D, width=1)
    draw.rectangle([MARGIN+2, IMG_Y1+2, W-MARGIN-2, IMG_Y2-2], outline=GOLD, width=2)

    # Líneas decorativas superiores
    hline(draw, MARGIN, 60,     W-MARGIN, GOLD,   w=1)
    hline(draw, MARGIN, 65,     W-MARGIN, GOLD_L, w=1)

    # Nombre
    ct(draw, W//2, 120, NOMBRE1, fnt(PALATINO_I, 56),  GOLD_L)
    ct(draw, W//2, 185, NOMBRE2, fnt(PALATINO_BI, 74), GOLD)

    # Ornamento central entre nombre e imagen
    ct(draw, W//2, 220, "* * *", fnt(SEGOE, 18), GOLD_D)

    # Zona inferior
    hline(draw, 160, 720, W-160, GOLD,   w=2)
    ct(draw, W//2, 762, TAGLINE.upper(), fnt(SEGOE_L, 24), CREAM_ALT)
    hline(draw, 160, 800, W-160, GOLD_L, w=1)

    ct(draw, W//2, 840, SUBTAG,    fnt(SEGOE_L, 20), MUTED)
    ct(draw, W//2, 878, UBICACION, fnt(SEGOE_L, 18), MUTED)

    hline(draw, 160, 918, W-160, GOLD, w=1)

    ct(draw, W//2, 955,  IG, fnt(SEGOE_B, 20), GOLD)
    ct(draw, W//2, 990,  WA, fnt(SEGOE,   20), CREAM_ALT)
    ct(draw, W//2, 1022, WEB,fnt(SEGOE_L, 17), MUTED)

    hline(draw, MARGIN, 1055, W-MARGIN, GOLD_L, w=1)
    hline(draw, MARGIN, 1060, W-MARGIN, GOLD,   w=1)

    save(canvas, "afiche1_elegancia_oscura")


# =============================================================================
# AFICHE 2 — "Foto Envolvente"  1080×1080  (Instagram cuadrado)
# Foto full-bleed con overlay gradiente y texto blanco elegante
# =============================================================================
def afiche2():
    W, H = 1080, 1080

    hero = load_img(os.path.join(IMG, "hero.jpg"), (W, H))
    # Gradiente: top transparente → bottom muy oscuro
    hero = gradient_v(hero, a0=20, a1=240, color=DARK)
    # Gradiente adicional top suave
    hero = gradient_v(hero, a0=100, a1=0, color=DARK)

    canvas = hero.convert("RGB")
    draw   = ImageDraw.Draw(canvas)

    # Marca superior izquierda
    corner_frame(draw, 44, 44, W-44, H-44, color=GOLD_D, size=50, w=1)

    hline(draw, 80, 88,  340, GOLD,   w=2)
    ct(draw, 210, 110, "CASONA FUNDO",        fnt(PALATINO_I, 22), GOLD_L, anchor="mm")
    ct(draw, 210, 136, "EL CASTILLO",         fnt(PALATINO,   17), WHITE,  anchor="mm")
    hline(draw, 80, 158, 340, GOLD,   w=2)

    # Texto principal (zona inferior)
    ct(draw, W//2, 680, NOMBRE1, fnt(PALATINO_I,  72), WHITE)
    ct(draw, W//2, 768, NOMBRE2, fnt(PALATINO_BI, 96), GOLD)

    hline(draw, 200, 828, W-200, GOLD_L, w=2)
    ct(draw, W//2, 868, TAGLINE.upper(), fnt(SEGOE_L, 30), CREAM_ALT)
    ct(draw, W//2, 912, UBICACION,       fnt(SEGOE_L, 20), MUTED)

    hline(draw, 200, 950, W-200, GOLD_D, w=1)
    ct(draw, W//2, 985,  IG,  fnt(SEGOE_B, 22), GOLD)
    ct(draw, W//2, 1022, WA,  fnt(SEGOE,   20), CREAM_ALT)

    save(canvas, "afiche2_foto_envolvente")


# =============================================================================
# AFICHE 3 — "Split Eventos"  1080×1080
# Mitad izquierda foto, mitad derecha crema con info de servicios
# =============================================================================
def afiche3():
    W, H = 1080, 1080
    canvas = Image.new("RGB", (W, H), CREAM)
    draw   = ImageDraw.Draw(canvas)

    # Mitad izquierda: foto de evento
    ev_path = os.path.join(IMG, "imagenes", "eventos",
                           "WhatsApp Image 2026-03-09 at 13.03.52.jpeg")
    foto = load_img(ev_path, (510, H))
    canvas.paste(foto.convert("RGB"), (0, 0))

    # Gradiente de transición hacia la derecha
    tr = gradient_h(Image.new("RGBA", (180, H), (0,0,0,0)), a0=0, a1=255, color=CREAM)
    canvas.paste(tr.convert("RGB"), (330, 0))

    draw = ImageDraw.Draw(canvas)

    # Franja dorada vertical
    draw.rectangle([492, 0, 500, H], fill=GOLD)

    # ── Panel derecho ──
    rx  = 520
    rw  = W - rx
    rc  = rx + rw // 2

    hline(draw, rx+30, 70, W-40, GOLD, w=2)
    ct(draw, rc, 110, "VENUE DE EVENTOS",         fnt(SEGOE_SB, 15), GOLD, anchor="mm")
    ct(draw, rc, 160, "Casona Fundo",             fnt(PALATINO_I, 52),  DARK, anchor="mm")
    ct(draw, rc, 225, "El Castillo",              fnt(PALATINO_B, 60),  GOLD, anchor="mm")
    hline(draw, rx+50, 268, W-50, GOLD_L, w=1)

    ct(draw, rc, 308, "Celebra en un entorno",    fnt(PALATINO_I, 28), TEXT_C, anchor="mm")
    ct(draw, rc, 348, "único e histórico.",        fnt(PALATINO_I, 28), TEXT_C, anchor="mm")

    hline(draw, rx+50, 388, W-50, GOLD_L, w=1)

    items = [
        ("Matrimonios",          "Ceremonias íntimas o grandes"),
        ("Eventos Corporativos", "Reuniones y celebraciones"),
        ("Fiestas & Cumpleaños", "Momentos que perduran"),
        ("Fotografía & Arte",    "Escenarios únicos"),
    ]
    y = 420
    for titulo, desc in items:
        draw.rectangle([rx+30, y+4, rx+35, y+28], fill=GOLD)
        ct(draw, rx+50, y+10, titulo, fnt(SEGOE_B, 18), DARK, anchor="lm")
        ct(draw, rx+50, y+32, desc,   fnt(SEGOE_L, 16), MUTED, anchor="lm")
        y += 70

    hline(draw, rx+30, y+8, W-40, GOLD, w=2)
    y += 32

    ct(draw, rc, y+20,  "*  " + DESDE,  fnt(SEGOE_L, 18), SAGE, anchor="mm")
    ct(draw, rc, y+52,  "*  " + PARQUE, fnt(SEGOE_L, 18), SAGE, anchor="mm")
    ct(draw, rc, y+84,  "*  " + UBICACION, fnt(SEGOE_L, 18), SAGE, anchor="mm")

    y += 120
    hline(draw, rx+30, y, W-40, GOLD_L, w=1)
    ct(draw, rc, y+34,  IG,  fnt(SEGOE_B, 20), GOLD, anchor="mm")
    ct(draw, rc, y+68,  WA,  fnt(SEGOE,   20), DARK, anchor="mm")
    ct(draw, rc, y+100, WEB, fnt(SEGOE_L, 17), MUTED, anchor="mm")

    save(canvas, "afiche3_split_eventos")


# =============================================================================
# AFICHE 4 — "Story Vertical"  1080×1920  (Instagram / WhatsApp Stories)
# =============================================================================
def afiche4():
    W, H = 1080, 1920
    canvas = Image.new("RGB", (W, H), DARK)

    # Zona superior: foto hero (65% del alto)
    hero = load_img(os.path.join(IMG, "hero.jpg"), (W, 1260))
    hero = gradient_v(hero, a0=0, a1=255, color=DARK)
    canvas.paste(hero.convert("RGB"), (0, 0))

    draw = ImageDraw.Draw(canvas)

    # Textura superior: gradiente oscuro encima del hero
    for i in range(350):
        a = int(180 * (1 - i/350))
        draw.line([(0, i), (W, i)], fill=(*DARK, a))

    # ── Header superior ──
    corner_frame(draw, 40, 40, W-40, H-40, color=GOLD_D, size=60, w=1)

    ct(draw, W//2, 130, NOMBRE1, fnt(PALATINO_I,  58), GOLD_L)
    ct(draw, W//2, 206, NOMBRE2, fnt(PALATINO_BI, 80), GOLD)
    hline(draw, 100, 266, W-100, GOLD, w=2)
    ct(draw, W//2, 306, TAGLINE.upper(), fnt(SEGOE_L, 30), WHITE)
    ct(draw, W//2, 352, UBICACION,       fnt(SEGOE_L, 22), CREAM_ALT)

    # ── Bloque central sobre foto ──
    # Caja oscura semitransparente
    box = Image.new("RGBA", (W, 480), (0,0,0,0))
    bd  = ImageDraw.Draw(box)
    for i in range(480):
        a = int(220 * (0.3 + 0.7 * i/479))
        bd.line([(0,i),(W,i)], fill=(*DARK, a))
    canvas.paste(box.convert("RGB"), (0, 830))

    draw = ImageDraw.Draw(canvas)
    hline(draw, 80, 850, W-80, GOLD, w=1)

    ct(draw, W//2, 910, "Tu evento merece un",     fnt(PALATINO_I, 42), CREAM)
    ct(draw, W//2, 968, "escenario irrepetible.",   fnt(PALATINO_I, 42), GOLD)

    hline(draw, 80, 1020, W-80, GOLD_L, w=1)

    props = [
        "*  Matrimonios · Fiestas · Eventos corporativos",
        "*  Casona histórica de diseño francés",
        "*  Parque centenario de acceso privado",
        "*  A 75 km de Santiago",
    ]
    y = 1058
    for p in props:
        ct(draw, W//2, y, p, fnt(SEGOE_L, 24), CREAM_ALT)
        y += 52

    hline(draw, 80, y+10, W-80, GOLD, w=1)

    # ── Mini galería 2 fotos ──
    ev1 = os.path.join(IMG, "imagenes", "eventos",
                       "WhatsApp Image 2026-03-09 at 13.03.53.jpeg")
    ev2 = os.path.join(IMG, "carpa", "carpa_new1.jpg")
    tw, th = W//2 - 6, 310

    f1 = load_img(ev1, (tw, th))
    f2 = load_img(ev2, (tw, th))
    canvas.paste(f1.convert("RGB"), (0,    1330))
    canvas.paste(f2.convert("RGB"), (tw+6, 1330))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0,    1330, tw,    1640], outline=GOLD_D, width=2)
    draw.rectangle([tw+6, 1330, W,     1640], outline=GOLD_D, width=2)

    # ── Footer contacto ──
    draw.rectangle([0, 1658, W, H], fill=(*DARK, 255))
    hline(draw, 60, 1672, W-60, GOLD, w=2)

    ct(draw, W//2, 1730, IG,  fnt(SEGOE_B, 30), GOLD)
    ct(draw, W//2, 1786, WA,  fnt(SEGOE,   28), CREAM_ALT)
    ct(draw, W//2, 1836, WEB, fnt(SEGOE_L, 22), MUTED)

    hline(draw, 60, 1878, W-60, GOLD, w=2)

    save(canvas, "afiche4_story_vertical")


# =============================================================================
# AFICHE 5 — "Banner Horizontal"  1200×628  (Facebook / LinkedIn / compartir)
# =============================================================================
def afiche5():
    W, H = 1200, 628
    canvas = Image.new("RGB", (W, H), DARK)

    # Foto lado izquierdo (55%)
    split  = int(W * 0.56)
    hero   = load_img(os.path.join(IMG, "hero.jpg"), (split, H))
    canvas.paste(hero.convert("RGB"), (0, 0))

    # Gradiente de transición
    tr = gradient_h(Image.new("RGBA",(220, H),(0,0,0,0)), a0=0, a1=255, color=DARK)
    canvas.paste(tr.convert("RGB"), (split - 220, 0))

    draw = ImageDraw.Draw(canvas)

    # Línea dorada vertical separadora
    vline(draw, split + 8, 36, H - 36, GOLD, w=2)

    # ── Panel derecho ──
    px  = split + 32
    pw  = W - px
    pc  = px + pw // 2

    hline(draw, px, 42,  W-36, GOLD,   w=1)
    ct(draw, pc, 82,  NOMBRE1, fnt(PALATINO_I,  48), GOLD_L, anchor="mm")
    ct(draw, pc, 140, NOMBRE2, fnt(PALATINO_BI, 62), GOLD,   anchor="mm")
    hline(draw, px, 178, W-36, GOLD_L, w=1)

    ct(draw, pc, 216, TAGLINE,  fnt(PALATINO_I, 26), CREAM_ALT, anchor="mm")
    ct(draw, pc, 255, UBICACION,fnt(SEGOE_L,    18), MUTED,     anchor="mm")

    hline(draw, px, 286, W-36, GOLD_D, w=1)

    ct(draw, pc, 324, "* " + DESDE,  fnt(SEGOE_L, 18), SAGE, anchor="mm")
    ct(draw, pc, 358, "* " + PARQUE, fnt(SEGOE_L, 18), SAGE, anchor="mm")

    hline(draw, px, 394, W-36, GOLD, w=2)

    ct(draw, pc, 432, IG,  fnt(SEGOE_B, 20), GOLD,      anchor="mm")
    ct(draw, pc, 466, WA,  fnt(SEGOE,   20), CREAM_ALT, anchor="mm")
    ct(draw, pc, 498, WEB, fnt(SEGOE_L, 17), MUTED,     anchor="mm")

    hline(draw, px, 534, W-36, GOLD, w=1)

    save(canvas, "afiche5_banner_horizontal")


# =============================================================================
# DÍPTICO — Portada + Interior  (A4 landscape @ 150 dpi = 1748×1240 px)
# =============================================================================
def diptico():
    PW, PH = 1748, 1240

    # ── PORTADA ──────────────────────────────────────────────────────────────
    hero = load_img(os.path.join(IMG, "hero.jpg"), (PW, PH))
    hero = gradient_v(hero, a0=40, a1=230, color=DARK)
    hero = dark_overlay(hero, 80)
    p1   = hero.convert("RGB")
    d1   = ImageDraw.Draw(p1)

    corner_frame(d1, 36, 36, PW-36, PH-36, color=GOLD_D, size=70, w=1)
    corner_frame(d1, 52, 52, PW-52, PH-52, color=GOLD,   size=50, w=2)

    cy = PH // 2
    ct(d1, PW//2, cy - 200, NOMBRE1,         fnt(PALATINO_I,  80), GOLD_L)
    ct(d1, PW//2, cy -  90, NOMBRE2,         fnt(PALATINO_BI,108), GOLD)
    hline(d1, PW//2 - 280, cy - 30, PW//2 + 280, GOLD, w=2)
    ct(d1, PW//2, cy + 30,  TAGLINE.upper(), fnt(SEGOE_L, 38), WHITE)
    ct(d1, PW//2, cy + 86,  DESDE + "  ·  " + PARQUE, fnt(SEGOE_L, 24), CREAM_ALT)
    hline(d1, PW//2 - 200, cy + 128, PW//2 + 200, GOLD_L, w=1)
    ct(d1, PW//2, cy + 172, UBICACION,       fnt(SEGOE_L, 26), MUTED)

    hline(d1, 100, PH - 120, PW - 100, GOLD, w=1)
    ct(d1, PW//2, PH - 72,
       IG + "   ·   " + WA + "   ·   " + WEB,
       fnt(SEGOE, 20), GOLD_L)

    # ── INTERIOR ─────────────────────────────────────────────────────────────
    p2 = Image.new("RGB", (PW, PH), CREAM)
    d2 = ImageDraw.Draw(p2)

    # Franja dorada superior e inferior
    d2.rectangle([0, 0,    PW, 10],   fill=GOLD)
    d2.rectangle([0, PH-10, PW, PH],  fill=GOLD)

    # Header
    d2.rectangle([0, 10, PW, 110], fill=DARK)
    ct(d2, PW//2, 60,
       "CASONA FUNDO EL CASTILLO   ·   " + UBICACION.upper(),
       fnt(SEGOE_L, 20), GOLD, anchor="mm")

    # ── Columna izquierda: servicios ──────────────────────────────────────────
    C1X  = 60
    C1W  = 540
    C1CX = C1X + C1W // 2

    y = 146
    ct(d2, C1CX, y, "Nuestros Espacios", fnt(PALATINO_I, 38), DARK, anchor="mm")
    y += 44
    hline(d2, C1X, y, C1X + C1W, GOLD, w=1)
    y += 24

    servicios = [
        ("Casona Principal",
         "Diseño francés de más de 80 años.",
         "Ideal para ceremonias y recepciones."),
        ("Carpa de Eventos",
         "Espacio adaptable para hasta 200 personas.",
         "Clima controlado, iluminación especial."),
        ("Parque Centenario",
         "Jardines históricos únicos en la región.",
         "Perfectos para fotos y ritos al aire libre."),
        ("Acceso & Ubicación",
         "Los Andes, Valparaíso · Chile.",
         "A 75 km de Santiago, fácil llegada."),
    ]

    for titulo, l1, l2 in servicios:
        d2.rectangle([C1X, y, C1X+5, y+52], fill=GOLD)
        ct(d2, C1X+18, y+14, titulo, fnt(PALATINO_B, 22), DARK, anchor="lm")
        y += 44
        ct(d2, C1X+18, y,    l1,     fnt(SEGOE_L,   17), MUTED, anchor="lm")
        y += 27
        ct(d2, C1X+18, y,    l2,     fnt(SEGOE_L,   17), MUTED, anchor="lm")
        y += 38

    hline(d2, C1X, y+8, C1X + C1W, GOLD, w=1)
    y += 32
    ct(d2, C1CX, y,    "CONTACTO",  fnt(SEGOE_SB, 16), GOLD, anchor="mm")
    y += 36
    ct(d2, C1CX, y,    IG,          fnt(SEGOE_B, 21), DARK, anchor="mm")
    y += 36
    ct(d2, C1CX, y,    WA,          fnt(SEGOE,   21), SAGE, anchor="mm")
    y += 34
    ct(d2, C1CX, y,    WEB,         fnt(SEGOE_L, 18), MUTED, anchor="mm")

    # ── Divisor central ──────────────────────────────────────────────────────
    vline(d2, C1X + C1W + 30, 120, PH - 20, GOLD_L, w=1)

    # ── Columna derecha: galería ──────────────────────────────────────────────
    C2X = C1X + C1W + 66
    C2W = PW - C2X - 60

    ct(d2, C2X + C2W//2, 158, "Galería", fnt(PALATINO_I, 38), DARK, anchor="mm")
    hline(d2, C2X, 196, C2X + C2W, GOLD, w=1)

    gallery = [
        os.path.join(IMG, "img2.jpg"),
        os.path.join(IMG, "img6.jpg"),
        os.path.join(IMG, "img10.jpg"),
        os.path.join(IMG, "carpa", "carpa_new1.jpg"),
        os.path.join(IMG, "imagenes", "eventos",
                     "WhatsApp Image 2026-03-09 at 13.03.53.jpeg"),
        os.path.join(IMG, "quienes-somos.jpg"),
    ]

    TW = C2W // 3 - 8
    TH = (PH - 220) // 2 - 14

    for i, path in enumerate(gallery):
        row = i // 3
        col = i % 3
        gx  = C2X + col * (TW + 8)
        gy  = 212 + row * (TH + 8)
        thumb = load_img(path, (TW, TH))
        p2.paste(thumb.convert("RGB"), (gx, gy))
        d2.rectangle([gx, gy, gx+TW, gy+TH], outline=GOLD_D, width=2)

    # ── Guardar ───────────────────────────────────────────────────────────────
    p1.save(os.path.join(OUT, "diptico_portada.jpg"),  "JPEG", quality=95, dpi=(150,150))
    p2.save(os.path.join(OUT, "diptico_interior.jpg"), "JPEG", quality=95, dpi=(150,150))

    # PDF combinado (2 páginas)
    p1.save(
        os.path.join(OUT, "diptico_completo.pdf"),
        "PDF", resolution=150, save_all=True, append_images=[p2]
    )
    print("  OK diptico_portada.jpg")
    print("  OK diptico_interior.jpg")
    print("  OK diptico_completo.pdf  (2 paginas A4 landscape)")


# =============================================================================
print("=" * 60)
print("  CASONA FUNDO EL CASTILLO — Generador de Marketing")
print("=" * 60)
print("\n[Afiches]")
afiche1()
afiche2()
afiche3()
afiche4()
afiche5()
print("\n[Díptico]")
diptico()
print(f"\nLISTO Archivos guardados en:  {OUT}")
print("=" * 60)
