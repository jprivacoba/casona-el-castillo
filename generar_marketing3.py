#!/usr/bin/env python3
"""
Generador de afiches tanda 3 - foco matrimonios
Usa assets/image.png (foto B&W novios) + fotos del parque/casona
Ubicacion: "A 8 minutos de Enjoy Santiago"
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

BASE = r"c:\Users\jpriv\OneDrive\Documentos\casona-el-castillo"
IMG  = os.path.join(BASE, "assets", "images")
OUT  = os.path.join(BASE, "marketing")
os.makedirs(OUT, exist_ok=True)

# Foto estrella: B&W novios
FOTO_BW   = os.path.join(BASE, "assets", "image.png")

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
UBICACION = "A 8 minutos de Enjoy Santiago"
IG        = "@casonafundoelcastillo"
WA        = "+56 9 9779 4301"
WEB       = "casonafundoelcastillo.cl"
BODA_TAG  = "El escenario perfecto para tu matrimonio"
PARQUE    = "Parque centenario privado"
DESDE     = "Mas de 80 anos de historia"

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
GEORGIA_I   = os.path.join(F, "georgiai.ttf")
GEORGIA_B   = os.path.join(F, "georgiab.ttf")

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

def load_bw(path, size, crop=True):
    """Carga imagen y convierte a B&W con mayor contraste."""
    img = load(path, size, crop)
    img = ImageOps.grayscale(img).convert("RGB")
    img = ImageEnhance.Contrast(img).enhance(1.15)
    return img

def dark_ov(img, alpha=140):
    ov = Image.new("RGBA", img.size, (0, 0, 0, alpha))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

def colored_ov(img, color, alpha=80):
    ov = Image.new("RGBA", img.size, (*color, alpha))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

def grad_v(img, a0=0, a1=220, color=DARK):
    ov   = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d    = ImageDraw.Draw(ov)
    w, h = img.size
    for i in range(h):
        a = int(a0 + (a1 - a0) * i / max(h-1, 1))
        d.line([(0,i),(w,i)], fill=(*color, a))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

def grad_h(img, a0=0, a1=220, color=DARK):
    ov   = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d    = ImageDraw.Draw(ov)
    w, h = img.size
    for i in range(w):
        a = int(a0 + (a1 - a0) * i / max(w-1, 1))
        d.line([(i,0),(i,h)], fill=(*color, a))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

def corner_frame(draw, x1, y1, x2, y2, color=GOLD, size=50, w=2):
    for (cx,cy),(sx,sy) in zip([(x1,y1),(x2,y1),(x1,y2),(x2,y2)],
                                [(1,1),(-1,1),(1,-1),(-1,-1)]):
        draw.line([(cx,cy),(cx+sx*size,cy)], fill=color, width=w)
        draw.line([(cx,cy),(cx,cy+sy*size)], fill=color, width=w)

def save(img, name):
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save(os.path.join(OUT, name+".jpg"), "JPEG", quality=95, dpi=(300,300))
    img.save(os.path.join(OUT, name+".pdf"), "PDF",  resolution=150)
    print(f"  OK {name}")

# Fotos de parque/casona (sin carpa_new)
PARQUE_FOTOS = [
    os.path.join(IMG, "hero.jpg"),
    os.path.join(IMG, "quienes-somos.jpg"),
    os.path.join(IMG, "img7.jpg"),
    os.path.join(IMG, "img10.jpg"),
    os.path.join(IMG, "img16.jpg"),
    os.path.join(IMG, "img23.jpg"),
    os.path.join(IMG, "img35.jpg"),
    os.path.join(IMG, "img47.jpg"),
    os.path.join(IMG, "img50.jpg"),
    os.path.join(IMG, "img53.jpg"),
    os.path.join(IMG, "img55.jpg"),
]
EVENTOS_FOTOS = [
    os.path.join(IMG, "imagenes", "eventos", "WhatsApp Image 2026-03-09 at 13.03.52.jpeg"),
    os.path.join(IMG, "imagenes", "eventos", "WhatsApp Image 2026-03-09 at 13.03.53.jpeg"),
    os.path.join(IMG, "imagenes", "eventos", "WhatsApp Image 2026-03-09 at 13.04.50.jpeg"),
    os.path.join(IMG, "imagenes", "eventos", "WhatsApp Image 2026-03-09 at 12.58.04.jpeg"),
]


# =============================================================================
# AFICHE 16 — "Romance B&W"  1080x1080
# Foto B&W novios full-bleed, overlay oscuro sutil, tipografia delicada blanca
# =============================================================================
def afiche16():
    W, H = 1080, 1080
    canvas = load_bw(FOTO_BW, (W, H))
    canvas = grad_v(canvas, a0=10, a1=210, color=DARK)
    # Suave velo dorado encima
    canvas = colored_ov(canvas, (184, 147, 90), alpha=18)
    draw   = ImageDraw.Draw(canvas)

    corner_frame(draw, 38, 38, W-38, H-38, color=GOLD_D, size=55, w=1)
    corner_frame(draw, 52, 52, W-52, H-52, color=GOLD,   size=38, w=2)

    # Texto superior
    hline(draw, 100, 110, W-100, GOLD_L, w=1)
    ct(draw, W//2, 148, "MATRIMONIOS", fnt(SEGOE_SB, 18), GOLD, anchor="mm")
    hline(draw, 100, 176, W-100, GOLD_L, w=1)

    # Texto inferior
    ct(draw, W//2, H-360, NOMBRE1,     fnt(PALATINO_I,  58), WHITE)
    ct(draw, W//2, H-284, NOMBRE2,     fnt(PALATINO_BI, 76), GOLD)
    hline(draw, 160, H-232, W-160, GOLD, w=2)
    ct(draw, W//2, H-192, BODA_TAG,    fnt(PALATINO_I,  26), CREAM_ALT)
    hline(draw, 160, H-156, W-160, GOLD_L, w=1)
    ct(draw, W//2, H-116, UBICACION,   fnt(SEGOE_L, 20), CREAM_ALT)
    ct(draw, W//2, H- 76, PARQUE,      fnt(SEGOE_L, 18), MUTED)
    hline(draw, 160, H- 46, W-160, GOLD, w=1)
    ct(draw, W//2, H- 18, IG + "  *  " + WA, fnt(SEGOE, 16), GOLD_L)

    save(canvas, "afiche16_romance_bw")


# =============================================================================
# AFICHE 17 — "Split elegante"  1080x1080
# Izquierda: B&W foto novios | Derecha: fondo oscuro con texto dorado
# =============================================================================
def afiche17():
    W, H = 1080, 1080
    canvas = Image.new("RGB", (W, H), DARK)

    # Mitad izquierda: foto B&W
    bw = load_bw(FOTO_BW, (532, H))
    canvas.paste(bw, (0, 0))

    # Gradiente de transicion
    tr = grad_h(Image.new("RGB", (220, H), DARK), a0=0, a1=255, color=DARK)
    canvas.paste(tr, (312, 0))

    draw = ImageDraw.Draw(canvas)

    # Separador dorado vertical
    draw.rectangle([534, 0, 542, H], fill=GOLD)

    # Panel derecho
    RX  = 562
    RW  = W - RX
    RC  = RX + RW // 2

    hline(draw, RX+30, 80,  W-30, GOLD,   w=1)
    hline(draw, RX+30, 86,  W-30, GOLD_L, w=1)

    ct(draw, RC, 148, "Celebra tu",   fnt(PALATINO_I,  40), CREAM_ALT)
    ct(draw, RC, 202, "Matrimonio",   fnt(PALATINO_BI, 58), GOLD)
    ct(draw, RC, 258, "aqui.",        fnt(PALATINO_I,  40), CREAM_ALT)

    hline(draw, RX+30, 296, W-30, GOLD_L, w=1)

    ct(draw, RC, 344, NOMBRE1,        fnt(PALATINO_I, 32), GOLD_L)
    ct(draw, RC, 388, NOMBRE2,        fnt(PALATINO_B, 40), GOLD)

    hline(draw, RX+30, 422, W-30, GOLD_D, w=1)

    items = [
        ("Parque centenario", "privado y exclusivo"),
        ("Casona historica",  "diseno frances"),
        ("Acceso facil",      UBICACION),
        ("Capacidad",         "hasta 200 personas"),
    ]
    y = 456
    for t, s in items:
        draw.rectangle([RX+30, y, RX+34, y+40], fill=GOLD)
        ct(draw, RX+48, y+10, t, fnt(PALATINO_B, 20), CREAM_ALT, anchor="lm")
        ct(draw, RX+48, y+34, s, fnt(SEGOE_L,   16), MUTED,     anchor="lm")
        y += 64

    hline(draw, RX+30, y+10, W-30, GOLD, w=2)
    ct(draw, RC, y+48, IG,  fnt(SEGOE_B, 20), GOLD)
    ct(draw, RC, y+82, WA,  fnt(SEGOE,   20), CREAM_ALT)
    ct(draw, RC, y+114,WEB, fnt(SEGOE_L, 17), MUTED)

    hline(draw, RX+30, H-50, W-30, GOLD_L, w=1)
    hline(draw, RX+30, H-44, W-30, GOLD,   w=1)

    save(canvas, "afiche17_split_elegante")


# =============================================================================
# AFICHE 18 — "Minimalista crema"  1080x1080
# Fondo crema, foto B&W en circulo central, borde dorado, muy limpio
# =============================================================================
def afiche18():
    W, H = 1080, 1080
    canvas = Image.new("RGB", (W, H), CREAM)
    draw   = ImageDraw.Draw(canvas)

    # Patron de fondo muy sutil
    for x in range(0, W, 40):
        draw.line([(x,0),(x,H)], fill=(*GOLD_L, 15), width=1)
    for y in range(0, H, 40):
        draw.line([(0,y),(W,y)], fill=(*GOLD_L, 15), width=1)

    # Franja dorada superior e inferior
    draw.rectangle([0, 0,    W, 16],   fill=GOLD)
    draw.rectangle([0, H-16, W, H  ],  fill=GOLD)

    # Foto B&W en rectangulo centrado con borde dorado
    PH_W, PH_H = 680, 440
    PH_X = (W - PH_W) // 2
    PH_Y = 120

    bw = load_bw(FOTO_BW, (PH_W, PH_H))
    canvas.paste(bw, (PH_X, PH_Y))

    # Marco dorado
    draw.rectangle([PH_X-4, PH_Y-4, PH_X+PH_W+4, PH_Y+PH_H+4],
                   outline=GOLD_D, width=1)
    draw.rectangle([PH_X-8, PH_Y-8, PH_X+PH_W+8, PH_Y+PH_H+8],
                   outline=GOLD, width=2)

    # Ornamento entre foto y texto
    ct(draw, W//2, PH_Y + PH_H + 42, "* * *", fnt(SEGOE, 20), GOLD_D)

    ct(draw, W//2, PH_Y + PH_H + 94,  NOMBRE1, fnt(PALATINO_I,  54), TEXT_C)
    ct(draw, W//2, PH_Y + PH_H + 158, NOMBRE2, fnt(PALATINO_BI, 68), GOLD)

    hline(draw, 180, PH_Y + PH_H + 202, W-180, GOLD, w=2)

    ct(draw, W//2, PH_Y + PH_H + 244, BODA_TAG,  fnt(GEORGIA_I, 24), TEXT_C)
    ct(draw, W//2, PH_Y + PH_H + 284, UBICACION, fnt(SEGOE_L,   18), MUTED)

    hline(draw, 180, PH_Y + PH_H + 316, W-180, GOLD_L, w=1)

    ct(draw, W//2, PH_Y + PH_H + 352, IG,  fnt(SEGOE_B, 20), GOLD)
    ct(draw, W//2, PH_Y + PH_H + 386, WA,  fnt(SEGOE,   18), TEXT_C)
    ct(draw, W//2, PH_Y + PH_H + 416, WEB, fnt(SEGOE_L, 16), MUTED)

    save(canvas, "afiche18_minimalista_crema")


# =============================================================================
# AFICHE 19 — "Diptych B&W + parque"  1080x1080
# Mitad superior: foto parque a color | Mitad inferior: foto B&W novios
# Con franja dorada separadora y texto superpuesto
# =============================================================================
def afiche19():
    W, H = 1080, 1080
    canvas = Image.new("RGB", (W, H), DARK)

    # Mitad superior: foto parque/casona a color
    top = load(PARQUE_FOTOS[1], (W, H//2))  # quienes-somos
    top = grad_v(top, a0=0, a1=120, color=DARK)
    canvas.paste(top, (0, 0))

    # Mitad inferior: foto B&W novios
    bot = load_bw(FOTO_BW, (W, H//2))
    bot = grad_v(bot, a0=60, a1=220, color=DARK)
    canvas.paste(bot, (0, H//2))

    draw = ImageDraw.Draw(canvas)

    # Franja dorada central
    draw.rectangle([0, H//2 - 4, W, H//2 + 4], fill=GOLD)

    # Texto sobre foto superior (casona)
    ct(draw, W//2, 100, NOMBRE1, fnt(PALATINO_I,  54), WHITE)
    ct(draw, W//2, 168, NOMBRE2, fnt(PALATINO_BI, 70), GOLD)
    hline(draw, 120, 220, W-120, GOLD_L, w=1)
    ct(draw, W//2, 262, TAGLINE.upper(), fnt(SEGOE_L, 24), CREAM_ALT)
    ct(draw, W//2, 300, UBICACION,       fnt(SEGOE_L, 20), MUTED)

    # Label en la franja
    bx, bw_lbl = W//2 - 200, 400
    draw.rectangle([bx, H//2 - 28, bx + bw_lbl, H//2 + 28], fill=DARK)
    ct(draw, W//2, H//2, "MATRIMONIOS EN EL PARQUE",
       fnt(SEGOE_SB, 16), GOLD, anchor="mm")

    # Texto sobre foto inferior (novios)
    ct(draw, W//2, H//2 + 90,  BODA_TAG,  fnt(PALATINO_I, 32), WHITE)
    hline(draw, 200, H//2 + 136, W-200, GOLD_L, w=1)
    ct(draw, W//2, H//2 + 188, PARQUE,    fnt(SEGOE_L, 20), CREAM_ALT)
    ct(draw, W//2, H//2 + 226, DESDE,     fnt(SEGOE_L, 18), MUTED)

    hline(draw, 160, H - 120, W-160, GOLD, w=2)
    ct(draw, W//2, H - 80,  IG,  fnt(SEGOE_B, 20), GOLD)
    ct(draw, W//2, H - 44,  WA,  fnt(SEGOE,   18), CREAM_ALT)

    save(canvas, "afiche19_diptych_parque_novios")


# =============================================================================
# AFICHE 20 — "Story boda"  1080x1920
# Story vertical con foto B&W novios dominante + detalles parque
# =============================================================================
def afiche20():
    W, H = 1080, 1920
    canvas = Image.new("RGB", (W, H), DARK)

    # Foto B&W novios (80% del alto)
    bw = load_bw(FOTO_BW, (W, 1540))
    bw = grad_v(bw, a0=0, a1=240, color=DARK)
    canvas.paste(bw, (0, 0))

    # Oscurecer la parte superior para el header
    top_ov = Image.new("RGB", (W, 280), DARK)
    for i in range(280):
        a = int(220 * (1 - i/280))
        ImageDraw.Draw(top_ov).line([(0,i),(W,i)],
                                    fill=tuple(int(c*(1-a/220)+255*(a/220))
                                               for c in DARK))
    # simpler: just paste with alpha blend
    ov2 = Image.new("RGBA", (W, 280), (0,0,0,0))
    d2  = ImageDraw.Draw(ov2)
    for i in range(280):
        a = int(200 * (1 - i / 280))
        d2.line([(0,i),(W,i)], fill=(*DARK, a))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), ov2.resize((W,H),
             resample=Image.NEAREST)).convert("RGB")
    # Re-paste the main bw image to fix
    canvas2 = Image.new("RGB", (W, H), DARK)
    bw2 = load_bw(FOTO_BW, (W, 1540))
    bw2 = grad_v(bw2, a0=0, a1=255, color=DARK)
    # Top fade
    for i in range(300):
        a = int(255 * (1 - i/300))
        ImageDraw.Draw(bw2).line([(0,i),(W,i)], fill=(*DARK, a))
    canvas2.paste(bw2, (0, 0))
    canvas = canvas2

    draw = ImageDraw.Draw(canvas)

    # Header superior
    corner_frame(draw, 44, 44, W-44, H-44, color=GOLD_D, size=65, w=1)

    hline(draw, 80, 90,  W-80, GOLD,   w=2)
    ct(draw, W//2, 136, NOMBRE1, fnt(PALATINO_I,  60), GOLD_L)
    ct(draw, W//2, 210, NOMBRE2, fnt(PALATINO_BI, 82), GOLD)
    hline(draw, 80, 266, W-80, GOLD,   w=2)
    ct(draw, W//2, 312, "MATRIMONIOS", fnt(SEGOE_SB, 22), WHITE)
    ct(draw, W//2, 360, UBICACION,     fnt(SEGOE_L,  22), CREAM_ALT)

    # Zona texto inferior
    ct(draw, W//2, 1370, BODA_TAG,     fnt(PALATINO_I, 40), WHITE)
    hline(draw, 100, 1424, W-100, GOLD, w=2)

    ct(draw, W//2, 1478, "* " + PARQUE,     fnt(SEGOE_L, 26), CREAM_ALT)
    ct(draw, W//2, 1524, "* " + DESDE,      fnt(SEGOE_L, 26), CREAM_ALT)
    ct(draw, W//2, 1570, "* Hasta 200 personas", fnt(SEGOE_L, 26), CREAM_ALT)

    hline(draw, 100, 1618, W-100, GOLD_L, w=1)

    # Fotos pequenas del parque/casona
    mini_paths = [PARQUE_FOTOS[0], PARQUE_FOTOS[2], PARQUE_FOTOS[4]]
    MW, MH = W//3 - 6, 160
    for i, path in enumerate(mini_paths):
        mx = i * (MW + 6)
        mi = load(path, (MW, MH))
        canvas.paste(mi, (mx, 1636))
        draw = ImageDraw.Draw(canvas)
        draw.rectangle([mx, 1636, mx+MW, 1636+MH], outline=GOLD_D, width=2)

    draw = ImageDraw.Draw(canvas)
    hline(draw, 80, 1808, W-80, GOLD, w=2)

    ct(draw, W//2, 1856, IG,  fnt(SEGOE_B, 30), GOLD)
    ct(draw, W//2, 1906, WA,  fnt(SEGOE,   26), CREAM_ALT)
    ct(draw, W//2, 1882+62, WEB, fnt(SEGOE_L, 20), MUTED)

    save(canvas, "afiche20_story_boda")


# =============================================================================
# AFICHE 21 — "Gran Collage boda"  1080x1080
# 3 tiras verticales: parque | foto B&W novios (ancha) | evento
# Con banda de texto oscura en la base
# =============================================================================
def afiche21():
    W, H = 1080, 1080
    canvas = Image.new("RGB", (W, H), DARK)

    BAND_H = 200
    FOTO_H = H - BAND_H
    GAP    = 5

    # Anchos proporcionales: 28% | 44% | 28%
    W1 = int(W * 0.28)
    W2 = W - 2*W1 - 2*GAP
    W3 = W1

    # Tira 1: foto parque
    f1 = load(PARQUE_FOTOS[3], (W1, FOTO_H))
    f1 = dark_ov(f1, 30)
    canvas.paste(f1, (0, 0))

    # Tira 2 (central, mas ancha): foto B&W novios
    f2 = load_bw(FOTO_BW, (W2, FOTO_H))
    canvas.paste(f2, (W1+GAP, 0))

    # Tira 3: foto evento
    f3 = load(EVENTOS_FOTOS[0], (W3, FOTO_H))
    f3 = dark_ov(f3, 30)
    canvas.paste(f3, (W1+W2+2*GAP, 0))

    draw = ImageDraw.Draw(canvas)

    # Separadores dorados
    draw.rectangle([W1, 0, W1+GAP, FOTO_H], fill=(*GOLD_D,))
    draw.rectangle([W1+W2+GAP, 0, W1+W2+2*GAP, FOTO_H], fill=(*GOLD_D,))

    # Labels sobre tiras laterales
    ct(draw, W1//2, FOTO_H-30, "PARQUE",   fnt(SEGOE_SB, 13), GOLD, anchor="mm")
    ct(draw, W1+W2+GAP+W3//2, FOTO_H-30, "EVENTOS", fnt(SEGOE_SB, 13), GOLD, anchor="mm")

    # Banda oscura inferior
    draw.rectangle([0, FOTO_H, W, H], fill=DARK)
    hline(draw, 60, FOTO_H + 6, W-60, GOLD, w=2)

    ct(draw, W//2, FOTO_H + 58,  NOMBRE1,  fnt(PALATINO_I,  44), GOLD_L)
    ct(draw, W//2, FOTO_H + 112, NOMBRE2,  fnt(PALATINO_BI, 56), GOLD)
    hline(draw, 160, FOTO_H + 148, W-160, GOLD_L, w=1)
    ct(draw, W//2, FOTO_H + 174, UBICACION,    fnt(SEGOE_L, 18), CREAM_ALT)
    ct(draw, W//2, FOTO_H + 198, IG + "  *  " + WA, fnt(SEGOE, 16), GOLD_L)

    save(canvas, "afiche21_collage_tiras")


# =============================================================================
# AFICHE 22 — "Editorial oscuro"  1080x1080
# Fondo negro, foto B&W novios centrada a 60%, tipografia editorial minima
# =============================================================================
def afiche22():
    W, H = 1080, 1080
    canvas = Image.new("RGB", (W, H), BLACK)
    draw   = ImageDraw.Draw(canvas)

    # Foto B&W centrada (60% del ancho, 70% del alto)
    PW, PH_px = int(W * 0.72), int(H * 0.72)
    PX = (W - PW) // 2
    PY = int(H * 0.06)

    bw = load_bw(FOTO_BW, (PW, PH_px))
    # Vignetado suave en los bordes de la foto
    vig = Image.new("RGBA", (PW, PH_px), (0,0,0,0))
    vd  = ImageDraw.Draw(vig)
    for i in range(80):
        a = int(180 * (1 - i/80))
        vd.rectangle([i, i, PW-i, PH_px-i], outline=(0,0,0,a), width=1)
    bw_rgba = Image.alpha_composite(bw.convert("RGBA"), vig)
    canvas.paste(bw_rgba.convert("RGB"), (PX, PY))

    # Borde blanco fino alrededor de la foto
    draw.rectangle([PX-2, PY-2, PX+PW+2, PY+PH_px+2], outline=WHITE, width=1)

    # Texto superior minimalista (estilo editorial)
    ct(draw, W//2, PY//2 - 10, NOMBRE1.upper() + "  " + NOMBRE2.upper(),
       fnt(SEGOE_L, 18), WHITE, anchor="mm")

    # Linea dorada muy fina debajo del texto superior
    hline(draw, W//4, PY//2 + 14, 3*W//4, GOLD_D, w=1)

    # Texto inferior
    TY = PY + PH_px
    ct(draw, W//2, TY + 44,  BODA_TAG,   fnt(GEORGIA_I, 28), WHITE)
    hline(draw, 220, TY + 80, W-220, GOLD_D, w=1)
    ct(draw, W//2, TY + 114, UBICACION,  fnt(SEGOE_L, 18), MUTED)
    hline(draw, 220, TY + 148, W-220, GOLD_D, w=1)
    ct(draw, W//2, TY + 186, IG,         fnt(SEGOE_SB, 18), GOLD)
    ct(draw, W//2, TY + 216, WA,         fnt(SEGOE_L,  17), WHITE)

    save(canvas, "afiche22_editorial_oscuro")


# =============================================================================
# AFICHE 23 — "Banner boda horizontal"  1200x628
# Foto B&W novios derecha + texto poético izquierda sobre oscuro
# =============================================================================
def afiche23():
    W, H = 1200, 628
    canvas = Image.new("RGB", (W, H), DARK)

    # Foto B&W lado derecho (50%)
    SPLIT  = W // 2
    bw     = load_bw(FOTO_BW, (SPLIT + 80, H))
    bw     = grad_h(bw, a0=255, a1=0, color=DARK)  # fade toward left
    canvas.paste(bw, (SPLIT - 80, 0))

    draw = ImageDraw.Draw(canvas)

    # Panel izquierdo texto
    hline(draw, 44, 50, SPLIT - 60, GOLD,   w=1)
    hline(draw, 44, 56, SPLIT - 60, GOLD_L, w=1)

    ct(draw, SPLIT//2, 120, "Tu historia",  fnt(PALATINO_I,  48), CREAM_ALT, anchor="mm")
    ct(draw, SPLIT//2, 178, "merece un",    fnt(PALATINO_I,  48), CREAM_ALT, anchor="mm")
    ct(draw, SPLIT//2, 248, "lugar unico.", fnt(PALATINO_BI, 56), GOLD,      anchor="mm")

    hline(draw, 44, 296, SPLIT - 60, GOLD_L, w=1)

    ct(draw, SPLIT//2, 340, NOMBRE1 + " " + NOMBRE2, fnt(PALATINO_I, 28), GOLD_L, anchor="mm")
    ct(draw, SPLIT//2, 380, UBICACION,                fnt(SEGOE_L,   18), MUTED,   anchor="mm")
    ct(draw, SPLIT//2, 416, PARQUE,                   fnt(SEGOE_L,   16), SAGE,    anchor="mm")

    hline(draw, 44, 450, SPLIT - 60, GOLD, w=2)

    ct(draw, SPLIT//2, 492, IG,  fnt(SEGOE_B, 20), GOLD,      anchor="mm")
    ct(draw, SPLIT//2, 528, WA,  fnt(SEGOE,   18), CREAM_ALT, anchor="mm")

    hline(draw, 44, 568, SPLIT - 60, GOLD_L, w=1)
    hline(draw, 44, 574, SPLIT - 60, GOLD,   w=1)

    save(canvas, "afiche23_banner_boda")


# =============================================================================
# AFICHE 24 — "Magazine portrait boda"  1080x1350  (4:5 Instagram)
# Foto B&W novios como hero + casilla inset del parque + texto lujo
# =============================================================================
def afiche24():
    W, H = 1080, 1350

    # Fondo: foto B&W novios
    bg = load_bw(FOTO_BW, (W, H))
    bg = grad_v(bg, a0=0, a1=240, color=DARK)
    bg = dark_ov(bg, 50)
    canvas = bg
    draw   = ImageDraw.Draw(canvas)

    # Cabecera tipo revista
    draw.rectangle([0, 0, W, 120], fill=(*DARK, 220))
    hline(draw, 0, 120, W, GOLD, w=3)
    ct(draw, W//2, 42, NOMBRE1.upper() + "  *  " + NOMBRE2.upper(),
       fnt(PALATINO_B, 30), GOLD, anchor="mm")
    ct(draw, W//2, 90, "MATRIMONIOS  *  LOS ANDES  *  CHILE",
       fnt(SEGOE_L,   16), GOLD_L, anchor="mm")

    # Inset foto parque (casona exterior)
    INS_W, INS_H = 500, 300
    ins = load(PARQUE_FOTOS[0], (INS_W, INS_H))  # hero.jpg (casona)
    IX  = (W - INS_W) // 2
    IY  = 160
    canvas.paste(ins, (IX, IY))
    draw.rectangle([IX-3, IY-3, IX+INS_W+3, IY+INS_H+3], outline=GOLD, width=3)
    # Label inset
    draw.rectangle([IX, IY+INS_H-36, IX+INS_W, IY+INS_H], fill=(*DARK, 200))
    ct(draw, IX + INS_W//2, IY+INS_H-18, "LA CASONA  *  EL PARQUE",
       fnt(SEGOE_SB, 14), GOLD, anchor="mm")

    # Texto principal
    ct(draw, W//2, 560, BODA_TAG,  fnt(PALATINO_I,  40), WHITE)
    ct(draw, W//2, 616, "en un entorno irrepetible.", fnt(PALATINO_I, 40), GOLD_L)

    hline(draw, 120, 668, W-120, GOLD, w=2)

    ct(draw, W//2, 714, UBICACION, fnt(SEGOE_L, 24), CREAM_ALT)
    ct(draw, W//2, 756, PARQUE,    fnt(SEGOE_L, 20), SAGE)
    ct(draw, W//2, 796, DESDE,     fnt(SEGOE_L, 20), MUTED)

    # Mini grilla de 4 fotos
    MINI_W = (W - 60) // 4 - 6
    MINI_H = 170
    mgrid  = [PARQUE_FOTOS[1], PARQUE_FOTOS[4], EVENTOS_FOTOS[0], EVENTOS_FOTOS[2]]
    for i, path in enumerate(mgrid):
        mx = 30 + i * (MINI_W + 8)
        my = 866
        mi = load(path, (MINI_W, MINI_H))
        canvas.paste(mi, (mx, my))
        draw.rectangle([mx, my, mx+MINI_W, my+MINI_H], outline=GOLD_D, width=2)

    hline(draw, 80, 1060, W-80, GOLD, w=2)

    ct(draw, W//2, 1112, IG,  fnt(SEGOE_B, 28), GOLD)
    ct(draw, W//2, 1160, WA,  fnt(SEGOE,   26), CREAM_ALT)
    ct(draw, W//2, 1204, WEB, fnt(SEGOE_L, 20), MUTED)

    hline(draw, 80, 1248, W-80, GOLD_L, w=1)

    ct(draw, W//2, 1296, "Reservas y consultas al WhatsApp",
       fnt(PALATINO_I, 26), CREAM_ALT)

    save(canvas, "afiche24_magazine_boda")


# =============================================================================
print("=" * 60)
print("  CASONA EL CASTILLO - Afiches Tanda 3 (Matrimonios)")
print("=" * 60)
print()

afiche16()
afiche17()
afiche18()
afiche19()
afiche20()
afiche21()
afiche22()
afiche23()
afiche24()

print()
print("LISTO - Archivos en:", OUT)
print("=" * 60)
