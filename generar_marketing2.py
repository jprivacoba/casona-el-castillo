#!/usr/bin/env python3
"""
Generador de afiches multifoto - Casona Fundo El Castillo  (tanda 2)
"""
import os, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

BASE = r"c:\Users\jpriv\OneDrive\Documentos\casona-el-castillo"
IMG  = os.path.join(BASE, "assets", "images")
OUT  = os.path.join(BASE, "marketing")
os.makedirs(OUT, exist_ok=True)

# ── COLORES ───────────────────────────────────────────────────────────────────
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
BLACK     = (0,   0,   0)

# ── MARCA ─────────────────────────────────────────────────────────────────────
NOMBRE1   = "Casona Fundo"
NOMBRE2   = "El Castillo"
TAGLINE   = "Un lugar con historia"
SUBTAG    = "Venue de Eventos * Patrimonio Historico"
UBICACION = "Los Andes, Valparaiso - Chile"
IG        = "@casonafundoelcastillo"
WA        = "+56 9 9779 4301"
WEB       = "casonafundoelcastillo.cl"
DESDE     = "Mas de 80 anos de historia"
PARQUE    = "Parque centenario"

# ── FONTS ─────────────────────────────────────────────────────────────────────
F = r"C:\Windows\Fonts"
PALATINO    = os.path.join(F, "pala.ttf")
PALATINO_B  = os.path.join(F, "palab.ttf")
PALATINO_I  = os.path.join(F, "palai.ttf")
PALATINO_BI = os.path.join(F, "palabi.ttf")
SEGOE       = os.path.join(F, "segoeui.ttf")
SEGOE_B     = os.path.join(F, "segoeuib.ttf")
SEGOE_L     = os.path.join(F, "segoeuil.ttf")
SEGOE_SB    = os.path.join(F, "seguisb.ttf")

def fnt(path, size):
    try:    return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

# ── HELPERS ───────────────────────────────────────────────────────────────────
def ct(draw, x, y, text, font, fill, anchor="mm"):
    draw.text((x, y), text, font=font, fill=fill, anchor=anchor)

def hline(draw, x1, y, x2, fill=GOLD, w=2):
    draw.line([(x1, y), (x2, y)], fill=fill, width=w)

def vline(draw, x, y1, y2, fill=GOLD, w=2):
    draw.line([(x, y1), (x, y2)], fill=fill, width=w)

def load(path, size, crop=True):
    if not os.path.exists(path):
        return Image.new("RGB", size, DARK)
    img = Image.open(path).convert("RGB")
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

def dark_ov(img, alpha=140):
    ov = Image.new("RGBA", img.size, (0, 0, 0, alpha))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

def grad_v(img, a0=0, a1=220, color=DARK):
    ov   = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d    = ImageDraw.Draw(ov)
    w, h = img.size
    for i in range(h):
        a = int(a0 + (a1 - a0) * i / max(h-1,1))
        d.line([(0,i),(w,i)], fill=(*color, a))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

def grad_h(img, a0=0, a1=220, color=DARK):
    ov   = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d    = ImageDraw.Draw(ov)
    w, h = img.size
    for i in range(w):
        a = int(a0 + (a1 - a0) * i / max(w-1,1))
        d.line([(i,0),(i,h)], fill=(*color, a))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

def corner_frame(draw, x1, y1, x2, y2, color=GOLD, size=50, w=2):
    for (cx,cy),(sx,sy) in zip([(x1,y1),(x2,y1),(x1,y2),(x2,y2)],
                                [(1,1),(-1,1),(1,-1),(-1,-1)]):
        draw.line([(cx,cy),(cx+sx*size,cy)], fill=color, width=w)
        draw.line([(cx,cy),(cx,cy+sy*size)], fill=color, width=w)

def brighten(img, factor=1.12):
    return ImageEnhance.Brightness(img).enhance(factor)

def warm(img, factor=1.08):
    r, g, b = img.split()
    r = ImageEnhance.Brightness(r.convert("L")).enhance(factor).convert("L")
    return Image.merge("RGB", (r, g, b))

def save(img, name):
    if img.mode != "RGB":
        img = img.convert("RGB")
    jpg = os.path.join(OUT, name + ".jpg")
    pdf = os.path.join(OUT, name + ".pdf")
    img.save(jpg, "JPEG", quality=95, dpi=(300,300))
    img.save(pdf, "PDF",  resolution=150)
    print(f"  OK {name}")

# ── CATALOGOS DE FOTOS ────────────────────────────────────────────────────────
# Fotos de la casona / parque (horizontal e vertical mezcladas)
CASONA = [
    os.path.join(IMG, "hero.jpg"),
    os.path.join(IMG, "quienes-somos.jpg"),
    os.path.join(IMG, "img3.jpg"),
    os.path.join(IMG, "img7.jpg"),
    os.path.join(IMG, "img10.jpg"),
    os.path.join(IMG, "img11.jpg"),
    os.path.join(IMG, "img16.jpg"),
    os.path.join(IMG, "img17.jpg"),
    os.path.join(IMG, "img23.jpg"),
    os.path.join(IMG, "img29.jpg"),
    os.path.join(IMG, "img35.jpg"),
    os.path.join(IMG, "img36.jpg"),
    os.path.join(IMG, "img43.jpg"),
    os.path.join(IMG, "img47.jpg"),
    os.path.join(IMG, "img50.jpg"),
    os.path.join(IMG, "img53.jpg"),
    os.path.join(IMG, "img54.jpg"),
    os.path.join(IMG, "img55.jpg"),
]
EVENTOS = [
    os.path.join(IMG, "imagenes", "eventos", "WhatsApp Image 2026-03-09 at 13.03.52.jpeg"),
    os.path.join(IMG, "imagenes", "eventos", "WhatsApp Image 2026-03-09 at 13.03.53.jpeg"),
    os.path.join(IMG, "imagenes", "eventos", "WhatsApp Image 2026-03-09 at 13.03.54.jpeg"),
    os.path.join(IMG, "imagenes", "eventos", "WhatsApp Image 2026-03-09 at 13.03.55.jpeg"),
    os.path.join(IMG, "imagenes", "eventos", "WhatsApp Image 2026-03-09 at 13.04.50.jpeg"),
    os.path.join(IMG, "imagenes", "eventos", "WhatsApp Image 2026-03-09 at 13.04.51.jpeg"),
    os.path.join(IMG, "imagenes", "eventos", "WhatsApp Image 2026-03-09 at 12.58.04.jpeg"),
]
CARPA = [
    os.path.join(IMG, "carpa", "carpa_new1.jpg"),
    os.path.join(IMG, "carpa", "carpa_new2.jpg"),
    os.path.join(IMG, "carpa", "carpa_new3.jpg"),
    os.path.join(IMG, "carpa", "carpa1.jpeg"),
    os.path.join(IMG, "carpa", "carpa2.jpeg"),
]
HISTORIA = [
    os.path.join(IMG, "imagenes", "historia", "WhatsApp Image 2026-03-09 at 13.01.59.jpeg"),
    os.path.join(IMG, "imagenes", "historia", "WhatsApp Image 2026-03-09 at 13.02.00.jpeg"),
    os.path.join(IMG, "imagenes", "historia", "WhatsApp Image 2026-03-09 at 13.02.03.jpeg"),
    os.path.join(IMG, "imagenes", "historia", "WhatsApp Image 2026-03-09 at 13.02.04.jpeg"),
]
ALL_PHOTOS = [p for p in CASONA + EVENTOS + CARPA if os.path.exists(p)]

# =============================================================================
# AFICHE 6 — "Triptych horizontal"  1080x1080
# Tres fotos verticales side-by-side + banda de texto oscura inferior
# =============================================================================
def afiche6():
    W, H = 1080, 1080
    canvas = Image.new("RGB", (W, H), DARK)
    draw   = ImageDraw.Draw(canvas)

    # Tres fotos verticales
    photos  = [CASONA[1], EVENTOS[0], CARPA[0]]  # quienes-somos, evento, carpa
    GAP     = 6
    PW_each = (W - GAP * 2) // 3
    PH_foto = 700

    for i, path in enumerate(photos):
        x  = i * (PW_each + GAP)
        ph = load(path, (PW_each, PH_foto))
        ph = brighten(ph, 1.08)
        canvas.paste(ph, (x, 0))
        # Separador dorado vertical
        if i > 0:
            draw.rectangle([x - GAP, 0, x - 1, PH_foto], fill=GOLD_D)

    draw = ImageDraw.Draw(canvas)

    # Banda oscura inferior
    draw.rectangle([0, PH_foto, W, H], fill=DARK)
    hline(draw, 60, PH_foto + 6, W-60, GOLD, w=2)

    ct(draw, W//2, PH_foto + 68,  NOMBRE1, fnt(PALATINO_I,  54), GOLD_L)
    ct(draw, W//2, PH_foto + 136, NOMBRE2, fnt(PALATINO_BI, 66), GOLD)

    hline(draw, 180, PH_foto + 174, W - 180, GOLD_L, w=1)
    ct(draw, W//2, PH_foto + 210, TAGLINE.upper(), fnt(SEGOE_L, 22), CREAM_ALT)
    ct(draw, W//2, PH_foto + 248, UBICACION,       fnt(SEGOE_L, 18), MUTED)
    hline(draw, 180, PH_foto + 274, W - 180, GOLD_L, w=1)
    ct(draw, W//2, PH_foto + 308, IG + "   " + WA, fnt(SEGOE, 18), GOLD_L)

    save(canvas, "afiche6_triptych")


# =============================================================================
# AFICHE 7 — "Grilla 2x2"  1080x1080
# Cuatro fotos en grilla con franja dorada central y texto superpuesto
# =============================================================================
def afiche7():
    W, H = 1080, 1080
    canvas = Image.new("RGB", (W, H), DARK)

    GAP     = 8
    HW      = (W - GAP)  // 2
    HH      = (H - GAP)  // 2
    BAND    = 110  # ancho de la banda central

    photos = [CASONA[0], EVENTOS[1], CARPA[1], CASONA[6]]

    positions = [(0,0), (HW+GAP,0), (0,HH+GAP), (HW+GAP,HH+GAP)]
    for path, (px, py) in zip(photos, positions):
        ph = load(path, (HW, HH))
        ph = dark_ov(ph, 40)
        canvas.paste(ph, (px, py))

    draw = ImageDraw.Draw(canvas)

    # Cruz dorada central
    cx, cy = W//2, H//2
    BH = BAND // 2

    draw.rectangle([0,   cy-BH,  W,   cy+BH], fill=DARK)
    draw.rectangle([cx-BH, 0,    cx+BH, H  ], fill=DARK)

    # Borde dorado de la cruz
    hline(draw, 0, cy-BH, W, GOLD, w=2)
    hline(draw, 0, cy+BH, W, GOLD, w=2)
    vline(draw, cx-BH, 0, H, GOLD, w=2)
    vline(draw, cx+BH, 0, H, GOLD, w=2)

    # Texto en banda horizontal
    ct(draw, W//2, cy - 22, NOMBRE1, fnt(PALATINO_I,  40), GOLD_L)
    ct(draw, W//2, cy + 30, NOMBRE2, fnt(PALATINO_BI, 46), GOLD)

    # Labels en cuadrantes
    labels = ["Parque", "Eventos", "Historia", "Carpa"]
    label_pos = [
        (HW//2,        HH - 28),
        (HW + GAP + HW//2, HH - 28),
        (HW//2,        HH + GAP + HH - 28),
        (HW + GAP + HW//2, HH + GAP + HH - 28),
    ]
    for lbl, (lx, ly) in zip(labels, label_pos):
        draw.rectangle([lx - 60, ly - 18, lx + 60, ly + 18], fill=(*DARK, 200))
        ct(draw, lx, ly, lbl.upper(), fnt(SEGOE_SB, 16), GOLD, anchor="mm")

    # Contacto en banda vertical
    ct(draw, cx, H//4,     IG,        fnt(SEGOE_B,  16), GOLD,      anchor="mm")
    ct(draw, cx, H//4+30,  WA,        fnt(SEGOE_L,  14), CREAM_ALT, anchor="mm")
    ct(draw, cx, 3*H//4,   UBICACION, fnt(SEGOE_L,  13), MUTED,     anchor="mm")
    ct(draw, cx, 3*H//4+28,WEB,       fnt(SEGOE_L,  13), GOLD_L,    anchor="mm")

    save(canvas, "afiche7_grilla_2x2")


# =============================================================================
# AFICHE 8 — "Mosaico asimetrico"  1080x1080
# Foto grande izquierda + columna de 3 fotos derecha + texto
# =============================================================================
def afiche8():
    W, H = 1080, 1080
    canvas = Image.new("RGB", (W, H), DARK)
    GAP = 6

    # Foto grande izquierda (60%)
    BIG_W = int(W * 0.60) - GAP
    big   = load(CASONA[0], (BIG_W, H))
    big   = grad_v(big, a0=0, a1=160)
    canvas.paste(big, (0, 0))

    # Columna derecha: 3 fotos iguales
    SM_W = W - BIG_W - GAP * 2
    SM_H = (H - GAP * 2) // 3
    right_photos = [EVENTOS[2], CARPA[0], CASONA[4]]
    for i, path in enumerate(right_photos):
        ph = load(path, (SM_W, SM_H))
        y  = i * (SM_H + GAP)
        canvas.paste(ph, (BIG_W + GAP, y))

    draw = ImageDraw.Draw(canvas)

    # Separadores dorados columna derecha
    for i in range(1, 3):
        y = i * (SM_H + GAP) - GAP
        draw.rectangle([BIG_W + GAP, y, W, y + GAP], fill=DARK)
        hline(draw, BIG_W + GAP, y + GAP//2, W, GOLD, w=2)

    # Texto sobre la foto grande
    corner_frame(draw, 30, 30, BIG_W - 30, H-30, color=GOLD_D, size=40, w=1)

    ct(draw, BIG_W//2, H - 290, NOMBRE1, fnt(PALATINO_I,  58), GOLD_L)
    ct(draw, BIG_W//2, H - 210, NOMBRE2, fnt(PALATINO_BI, 72), GOLD)
    hline(draw, 80, H-160, BIG_W-80, GOLD, w=1)
    ct(draw, BIG_W//2, H-125, TAGLINE.upper(), fnt(SEGOE_L, 22), CREAM_ALT)
    ct(draw, BIG_W//2, H- 85, UBICACION,       fnt(SEGOE_L, 18), MUTED)
    ct(draw, BIG_W//2, H- 48, IG,              fnt(SEGOE_B, 18), GOLD_L)

    # Labels columna derecha
    right_labels = ["Eventos", "Nuestra Carpa", "El Castillo"]
    for i, lbl in enumerate(right_labels):
        ly = i * (SM_H + GAP) + SM_H - 30
        ct(draw, BIG_W + GAP + SM_W//2, ly, lbl.upper(),
           fnt(SEGOE_SB, 13), GOLD, anchor="mm")

    save(canvas, "afiche8_mosaico_asimetrico")


# =============================================================================
# AFICHE 9 — "Collage polaroid"  1080x1080
# Fondo crema con 5 fotos simulando polaroids con sombra y rotacion
# =============================================================================
def afiche9():
    W, H = 1080, 1080
    canvas = Image.new("RGB", (W, H), CREAM_ALT)
    draw   = ImageDraw.Draw(canvas)

    # Patron de fondo: grilla sutil dorada
    for x in range(0, W, 60):
        draw.line([(x,0),(x,H)], fill=(*GOLD_L, 30), width=1)
    for y in range(0, H, 60):
        draw.line([(0,y),(W,y)], fill=(*GOLD_L, 30), width=1)

    # Titulo central encima
    ct(draw, W//2, 68,  NOMBRE1, fnt(PALATINO_I, 48), DARK)
    ct(draw, W//2, 126, NOMBRE2, fnt(PALATINO_B, 58), GOLD)
    hline(draw, 160, 162, W-160, GOLD, w=2)

    # Definir posiciones y rotaciones de los polaroids
    POL_W, POL_H = 300, 310  # foto dentro del polaroid
    BORDER = 14              # borde blanco superior y laterales
    FOOT   = 54              # pie blanco inferior (lugar para leyenda)
    TOTAL_W = POL_W + BORDER * 2
    TOTAL_H = POL_H + BORDER + FOOT

    configs = [
        # (cx, cy, angle, path, label)
        (220, 430,  -8,  CASONA[1],   "La Casona"),
        (560, 380,   4,  EVENTOS[0],  "Momentos"),
        (860, 430,  -5,  CARPA[0],    "La Carpa"),
        (320, 740,   6,  CASONA[5],   "El Parque"),
        (720, 730,  -3,  CASONA[10],  "Historia"),
    ]

    for cx, cy, angle, path, label in configs:
        # Crear polaroid
        pol = Image.new("RGB", (TOTAL_W, TOTAL_H), WHITE)
        foto = load(path, (POL_W, POL_H))
        pol.paste(foto, (BORDER, BORDER))

        # Leyenda en pie
        pd = ImageDraw.Draw(pol)
        ct(pd, TOTAL_W//2, TOTAL_H - FOOT//2, label.upper(),
           fnt(PALATINO_I, 20), (*DARK,), anchor="mm")

        # Sombra
        shadow = Image.new("RGBA", (TOTAL_W + 16, TOTAL_H + 16), (0,0,0,0))
        sd     = ImageDraw.Draw(shadow)
        sd.rectangle([8, 8, TOTAL_W+8, TOTAL_H+8], fill=(0,0,0,80))
        shadow = shadow.filter(ImageFilter.GaussianBlur(8))
        # Rotar polaroid
        pol_rgba   = pol.convert("RGBA")
        pol_rotado = pol_rgba.rotate(angle, expand=True, resample=Image.BICUBIC)

        # Pegar sombra y polaroid
        sh_rotado = shadow.rotate(angle, expand=True, resample=Image.BICUBIC)
        px = cx - sh_rotado.width  // 2
        py = cy - sh_rotado.height // 2
        canvas.paste(Image.new("RGB", sh_rotado.size, CREAM_ALT),
                     (px, py), sh_rotado)
        px = cx - pol_rotado.width  // 2
        py = cy - pol_rotado.height // 2
        canvas.paste(pol_rotado.convert("RGB"), (px, py), pol_rotado)

    draw = ImageDraw.Draw(canvas)

    # Footer
    hline(draw, 120, H-110, W-120, GOLD, w=1)
    ct(draw, W//2, H-76,  IG,        fnt(SEGOE_B, 20), GOLD)
    ct(draw, W//2, H-42,  WA + "  *  " + UBICACION, fnt(SEGOE_L, 16), MUTED)

    save(canvas, "afiche9_polaroids")


# =============================================================================
# AFICHE 10 — "Film strip"  1080x1080
# Tira de pelicula con 5 fotos + texto lateral
# =============================================================================
def afiche10():
    W, H = 1080, 1080
    canvas = Image.new("RGB", (W, H), DARK)
    draw   = ImageDraw.Draw(canvas)

    # Panel izquierdo oscuro con texto
    PANEL_W = 320
    draw.rectangle([0, 0, PANEL_W, H], fill=DARK)

    # Líneas decorativas
    hline(draw, 40, 100, PANEL_W - 20, GOLD,   w=2)
    hline(draw, 40, 106, PANEL_W - 20, GOLD_L, w=1)

    ct(draw, PANEL_W//2, 170, NOMBRE1, fnt(PALATINO_I,  36), GOLD_L)
    ct(draw, PANEL_W//2, 220, NOMBRE2, fnt(PALATINO_BI, 44), GOLD)

    hline(draw, 40, 256, PANEL_W - 20, GOLD_L, w=1)

    ct(draw, PANEL_W//2, 310, TAGLINE,   fnt(PALATINO_I, 20), CREAM_ALT)
    ct(draw, PANEL_W//2, 348, UBICACION, fnt(SEGOE_L,    15), MUTED)

    hline(draw, 40, 382, PANEL_W - 20, GOLD_D, w=1)

    items = [
        "Matrimonios",
        "Eventos corp.",
        "Cumpleanos",
        "Fotografias",
        "Parque privado",
    ]
    y = 420
    for it in items:
        ct(draw, PANEL_W//2, y, "* " + it, fnt(SEGOE_L, 18), CREAM_ALT)
        y += 42

    hline(draw, 40, y + 10, PANEL_W - 20, GOLD, w=2)
    ct(draw, PANEL_W//2, y + 48, IG,  fnt(SEGOE_B, 16), GOLD)
    ct(draw, PANEL_W//2, y + 78, WA,  fnt(SEGOE,   16), CREAM_ALT)
    ct(draw, PANEL_W//2, y + 106,WEB, fnt(SEGOE_L, 14), MUTED)

    hline(draw, 40, H - 100, PANEL_W - 20, GOLD_L, w=1)
    hline(draw, 40, H -  96, PANEL_W - 20, GOLD,   w=2)

    # Film strip a la derecha
    FILM_X  = PANEL_W + 8
    FILM_W  = W - FILM_X
    STRIP_W = 40   # perforaciones
    PHOTO_W = FILM_W - STRIP_W * 2
    N       = 5
    GAP     = 8
    PHOTO_H = (H - GAP * (N - 1)) // N

    film_photos = [CASONA[0], EVENTOS[0], CARPA[0], CASONA[3], EVENTOS[3]]

    # Fondo film
    draw.rectangle([FILM_X, 0, W, H], fill=(15, 12, 8))

    # Perforaciones (sprocket holes)
    HOLE_W, HOLE_H = 22, 30
    for strip_x in [FILM_X + 8, W - STRIP_W + 8]:
        for yi in range(0, H, 70):
            draw.rounded_rectangle(
                [strip_x, yi + 20, strip_x + HOLE_W, yi + 20 + HOLE_H],
                radius=4, fill=DARK
            )

    # Fotos
    for i, path in enumerate(film_photos):
        py = i * (PHOTO_H + GAP)
        ph = load(path, (PHOTO_W, PHOTO_H))
        ph = brighten(ph, 1.05)
        canvas.paste(ph, (FILM_X + STRIP_W, py))

    save(canvas, "afiche10_filmstrip")


# =============================================================================
# AFICHE 11 — "Magazin cover"  1080x1350  (Instagram portrait 4:5)
# Foto grande fondo + recuadros tipo revista con titulares
# =============================================================================
def afiche11():
    W, H = 1080, 1350
    canvas = Image.new("RGB", (W, H), DARK)

    # Foto de fondo completa
    bg = load(CASONA[0], (W, H))
    bg = grad_v(bg, a0=0,  a1=180, color=DARK)
    bg = grad_v(bg, a0=120, a1=0,  color=DARK)  # tambien oscurece arriba
    canvas.paste(bg, (0,0))

    draw = ImageDraw.Draw(canvas)

    # Cabecera estilo revista
    draw.rectangle([0, 0, W, 130], fill=(*DARK, 220))
    hline(draw, 0, 130, W, GOLD, w=3)

    ct(draw, W//2, 42,  "CASONA FUNDO EL CASTILLO",  fnt(PALATINO_B, 36), GOLD)
    ct(draw, W//2, 96,  SUBTAG,                       fnt(SEGOE_L,   17), CREAM_ALT)

    # Recuadro central (foto 2a encima del bg)
    inset_path = EVENTOS[0]
    inset = load(inset_path, (560, 360))
    canvas.paste(inset, ((W - 560)//2, 180))
    draw.rectangle([(W-560)//2, 180, (W+560)//2, 540], outline=GOLD, width=3)

    # Texto sobre la foto grande (zona inferior)
    ct(draw, W//2, 620, NOMBRE1, fnt(PALATINO_I,  68), WHITE)
    ct(draw, W//2, 706, NOMBRE2, fnt(PALATINO_BI, 86), GOLD)

    hline(draw, 120, 762, W-120, GOLD, w=2)
    ct(draw, W//2, 806, TAGLINE.upper(), fnt(SEGOE_L, 28), CREAM_ALT)

    # Mini grilla de fotos: 3 columnas x 2 filas
    MINI_W, MINI_H = 300, 190
    GAP_M = 10
    grid_photos = [
        CARPA[0], CASONA[3], CASONA[7],
        HISTORIA[0], EVENTOS[4], CARPA[2],
    ]
    grid_y0 = 870
    for i, path in enumerate(grid_photos):
        row = i // 3
        col = i % 3
        gx  = col * (MINI_W + GAP_M) + (W - 3*MINI_W - 2*GAP_M)//2
        gy  = grid_y0 + row * (MINI_H + GAP_M)
        mini = load(path, (MINI_W, MINI_H))
        canvas.paste(mini, (gx, gy))
        draw.rectangle([gx, gy, gx+MINI_W, gy+MINI_H], outline=GOLD_D, width=2)

    # Footer
    hline(draw, 60, 1296, W-60, GOLD, w=2)
    ct(draw, W//2, 1326, IG + "   *   " + WA, fnt(SEGOE_B, 20), GOLD)

    save(canvas, "afiche11_magazine_portrait")


# =============================================================================
# AFICHE 12 — "Panoramica collage"  1200x628  (horizontal multifoto)
# 5 fotos cosidas horizontalmente + overlay y texto
# =============================================================================
def afiche12():
    W, H = 1200, 628
    canvas = Image.new("RGB", (W, H), DARK)

    # 5 fotos cosidas (cada una 240px de ancho)
    photos = [CASONA[0], EVENTOS[1], CARPA[0], CASONA[2], EVENTOS[4]]
    PW = W // len(photos)
    for i, path in enumerate(photos):
        ph = load(path, (PW, H))
        canvas.paste(ph, (i * PW, 0))

    # Overlay diagonal oscuro en el centro para legibilidad
    ov   = Image.new("RGBA", (W, H), (0,0,0,0))
    ovd  = ImageDraw.Draw(ov)
    # Gradiente diagonal: oscuro en top-left y bottom
    for i in range(H):
        a = int(180 * (1 - abs(i - H//2) / (H//2)) * 0.6 + 80)
        ovd.line([(0,i),(W,i)], fill=(0,0,0,a))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), ov).convert("RGB")

    draw = ImageDraw.Draw(canvas)

    # Línea dorada horizontal al 40% del alto
    hline(draw, 0, int(H*0.36), W, GOLD, w=2)
    hline(draw, 0, int(H*0.68), W, GOLD, w=2)

    # Texto centrado
    ct(draw, W//2, H*2//5,  NOMBRE1, fnt(PALATINO_I,  56), GOLD_L)
    ct(draw, W//2, H*2//5 + 68, NOMBRE2, fnt(PALATINO_BI, 70), GOLD)

    ct(draw, W//2, int(H*0.80), TAGLINE.upper(), fnt(SEGOE_L, 24), WHITE)
    ct(draw, W//2, int(H*0.92), IG + "  *  " + WA, fnt(SEGOE, 18), GOLD_L)

    save(canvas, "afiche12_panorama_collage")


# =============================================================================
# AFICHE 13 — "Story multifoto"  1080x1920  (stories con muchas fotos)
# Composicion vertical: foto grande + 3 minis + foto grande + texto
# =============================================================================
def afiche13():
    W, H = 1080, 1920
    canvas = Image.new("RGB", (W, H), DARK)

    # Sección 1: foto grande (40% arriba)
    f1 = load(CASONA[0], (W, 760))
    f1 = grad_v(f1, a0=0, a1=200, color=DARK)
    canvas.paste(f1, (0, 0))

    # Sección 2: 3 fotos pequeñas (18% medio-superior)
    THIRD = W // 3
    mini_paths = [EVENTOS[0], CARPA[0], CASONA[4]]
    for i, path in enumerate(mini_paths):
        mi = load(path, (THIRD - 4, 340))
        canvas.paste(mi, (i * THIRD + 2, 762))

    # Sección 3: foto mediana (23%)
    f3 = load(HISTORIA[1], (W, 440))
    f3 = grad_v(f3, a0=60, a1=180, color=DARK)
    canvas.paste(f3, (0, 1106))

    # Sección 4: texto sobre fondo oscuro (restante inferior)
    draw = ImageDraw.Draw(canvas)

    # Separadores dorados
    hline(draw, 0, 760,  W, GOLD, w=3)
    hline(draw, 0, 1104, W, GOLD, w=2)
    hline(draw, 0, 1548, W, GOLD, w=3)

    # Fondo inferior
    draw.rectangle([0, 1548, W, H], fill=DARK)

    # Texto hero sobre primera foto
    ct(draw, W//2, 160, NOMBRE1, fnt(PALATINO_I,  60), WHITE)
    ct(draw, W//2, 242, NOMBRE2, fnt(PALATINO_BI, 80), GOLD)
    hline(draw, 120, 302, W-120, GOLD, w=2)
    ct(draw, W//2, 342, TAGLINE.upper(), fnt(SEGOE_L, 30), CREAM_ALT)

    # Labels sobre miniaturas
    mini_labels = ["Celebraciones", "La Carpa", "El Parque"]
    for i, lbl in enumerate(mini_labels):
        lx = i * THIRD + THIRD // 2
        draw.rectangle([lx - 80, 1064, lx + 80, 1100], fill=(*DARK, 200))
        ct(draw, lx, 1082, lbl.upper(), fnt(SEGOE_SB, 14), GOLD, anchor="mm")

    # Texto sobre foto historia
    ct(draw, W//2, 1330, "Mas de 80 anos de historia", fnt(PALATINO_I, 36), WHITE)
    ct(draw, W//2, 1378, "en el corazon de los Andes.", fnt(PALATINO_I, 36), GOLD_L)

    # Zona contacto inferior
    ct(draw, W//2, 1640, "Tu celebracion,", fnt(PALATINO_I, 46), CREAM)
    ct(draw, W//2, 1700, "nuestro escenario.", fnt(PALATINO_BI, 46), GOLD)

    hline(draw, 100, 1762, W-100, GOLD_L, w=1)

    ct(draw, W//2, 1812, IG,  fnt(SEGOE_B, 30), GOLD)
    ct(draw, W//2, 1862, WA,  fnt(SEGOE,   26), CREAM_ALT)
    ct(draw, W//2, 1908, WEB, fnt(SEGOE_L, 22), MUTED)

    save(canvas, "afiche13_story_multifoto")


# =============================================================================
# AFICHE 14 — "Carpa spotlight"  1080x1080
# Enfocado en la carpa de eventos, collage 3 fotos + info
# =============================================================================
def afiche14():
    W, H = 1080, 1080
    canvas = Image.new("RGB", (W, H), DARK)

    # Foto carpa grande arriba
    f_main = load(CARPA[0], (W, 560))
    f_main = grad_v(f_main, a0=0, a1=180, color=DARK)
    canvas.paste(f_main, (0, 0))

    # Tres fotos de evento abajo a la izquierda (columna)
    SMALL_W = 340
    small_paths = [CARPA[1], CARPA[2], EVENTOS[2]]
    SH = (H - 560 - 12) // 3
    for i, path in enumerate(small_paths):
        ph = load(path, (SMALL_W, SH - 4))
        canvas.paste(ph, (0, 560 + i * (SH + 4) + 2))

    # Texto en zona inferior derecha
    draw = ImageDraw.Draw(canvas)

    # Separadores
    hline(draw, 0,       558, W, GOLD, w=3)
    vline(draw, SMALL_W + 3, 560, H, GOLD, w=2)

    # Panel de texto inferior derecha
    TX = SMALL_W + 20
    TW = W - TX - 20
    TC = TX + TW // 2

    ct(draw, TC, 640,  "Nuestra",        fnt(PALATINO_I,  38), GOLD_L)
    ct(draw, TC, 692,  "Carpa de",       fnt(PALATINO_I,  50), WHITE)
    ct(draw, TC, 754,  "Eventos",        fnt(PALATINO_BI, 60), GOLD)

    hline(draw, TX, 804, W - 20, GOLD_L, w=1)

    feats = [
        "Hasta 200 personas",
        "Iluminacion especial",
        "Clima controlado",
        "Equipamiento completo",
    ]
    y = 830
    for f in feats:
        ct(draw, TC, y, "* " + f, fnt(SEGOE_L, 18), CREAM_ALT)
        y += 36

    hline(draw, TX, y + 8, W - 20, GOLD, w=2)
    ct(draw, TC, y + 42,  IG,          fnt(SEGOE_B, 18), GOLD)
    ct(draw, TC, y + 76,  WA,          fnt(SEGOE,   17), CREAM_ALT)

    # Texto sobre foto main
    ct(draw, W//2, 80,  NOMBRE1, fnt(PALATINO_I,  52), GOLD_L)
    ct(draw, W//2, 148, NOMBRE2, fnt(PALATINO_BI, 68), GOLD)
    ct(draw, W//2, 510, UBICACION, fnt(SEGOE_L, 20), CREAM_ALT)

    save(canvas, "afiche14_carpa_spotlight")


# =============================================================================
# AFICHE 15 — "Historia & Naturaleza"  1080x1080
# Collage 4 fotos con golden ratio layout + texto poetico
# =============================================================================
def afiche15():
    W, H = 1080, 1080
    canvas = Image.new("RGB", (W, H), CREAM)

    # Layout golden ratio: un foto grande 60% izquierda, 3 pequeñas derecha
    # + banda dorada y texto

    BIG_W = int(W * 0.618)  # proporcion aurea
    SM_W  = W - BIG_W - 6
    SM_H  = (H - 12) // 3

    # Foto grande izquierda
    big = load(HISTORIA[0], (BIG_W, H))
    big = dark_ov(big, 30)
    canvas.paste(big, (0, 0))

    # Tres fotos pequeñas derecha
    sm_paths = [CASONA[2], CASONA[7], HISTORIA[2]]
    for i, path in enumerate(sm_paths):
        ph = load(path, (SM_W, SM_H - 4))
        canvas.paste(ph, (BIG_W + 6, i * (SM_H + 4) + 2))

    draw = ImageDraw.Draw(canvas)

    # Divisor vertical dorado
    draw.rectangle([BIG_W, 0, BIG_W + 6, H], fill=GOLD)

    # Separadores horizontales columna derecha
    for i in range(1, 3):
        draw.rectangle([BIG_W + 6, i*(SM_H+4)-4, W, i*(SM_H+4)], fill=(*CREAM,255))
        hline(draw, BIG_W + 6, i*(SM_H+4) - 2, W, GOLD, w=2)

    # Texto sobre foto grande
    corner_frame(draw, 28, 28, BIG_W-28, H-28, color=GOLD_D, size=45, w=1)

    ct(draw, BIG_W//2, H - 330, "Un lugar",    fnt(PALATINO_I, 48), WHITE)
    ct(draw, BIG_W//2, H - 270, "con alma.",    fnt(PALATINO_I, 48), GOLD_L)

    hline(draw, 70, H-228, BIG_W-70, GOLD, w=1)

    ct(draw, BIG_W//2, H-192, NOMBRE1 + " " + NOMBRE2, fnt(PALATINO_B, 28), GOLD)
    ct(draw, BIG_W//2, H-152, DESDE,      fnt(SEGOE_L, 18), CREAM_ALT)
    ct(draw, BIG_W//2, H-116, UBICACION,  fnt(SEGOE_L, 17), MUTED)

    hline(draw, 70, H-86, BIG_W-70, GOLD_L, w=1)
    ct(draw, BIG_W//2, H-54, IG, fnt(SEGOE_B, 18), GOLD_L)

    # Labels miniaturas
    mini_labels = ["Historia", "El Parque", "La Casona"]
    for i, lbl in enumerate(mini_labels):
        ly = i * (SM_H + 4) + SM_H - 28
        ct(draw, BIG_W + 6 + SM_W//2, ly, lbl.upper(),
           fnt(SEGOE_SB, 14), WHITE, anchor="mm")

    save(canvas, "afiche15_historia_naturaleza")


# =============================================================================
print("=" * 60)
print("  CASONA EL CASTILLO - Afiches Tanda 2 (multifoto)")
print("=" * 60)
print()

afiche6()
afiche7()
afiche8()
afiche9()
afiche10()
afiche11()
afiche12()
afiche13()
afiche14()
afiche15()

print()
print("LISTO - Archivos en:", OUT)
print("=" * 60)
