#!/usr/bin/env python3
"""
Afiches tanda 4 — solo JPG, alto contraste, enfoque experiencia parque + matrimonios
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

BASE    = r"c:\Users\jpriv\OneDrive\Documentos\casona-el-castillo"
IMG     = os.path.join(BASE, "assets", "images")
OUT     = os.path.join(BASE, "marketing")
FOTO_BW = os.path.join(BASE, "assets", "image.png")
os.makedirs(OUT, exist_ok=True)

# ── PALETA ────────────────────────────────────────────────────────────────────
DARK      = (30,  23,  16)
GOLD      = (184, 147, 90)
GOLD_L    = (212, 180, 131)
GOLD_D    = (120, 90,  44)
CREAM     = (250, 247, 243)
CREAM_ALT = (243, 235, 224)
SAGE      = (107, 122, 92)
MUTED     = (138, 128, 119)
WHITE     = (255, 255, 255)
BLACK     = (0,   0,   0)

# ── COPY ──────────────────────────────────────────────────────────────────────
N1       = "Casona Fundo"
N2       = "El Castillo"
UBI      = "A 8 minutos de Enjoy Santiago"
IG       = "@casonafundoelcastillo"
WA       = "+56 9 9779 4301"
WEB      = "casonafundoelcastillo.cl"

FRASES = [
    "Una experiencia que no se olvida.",
    "Donde la naturaleza es el escenario.",
    "El parque que siempre sonaste.",
    "Historia, elegancia y naturaleza.",
    "Tu celebracion merece algo unico.",
    "80 anos de historia te esperan.",
    "El lugar donde todo es posible.",
    "Vive lo extraordinario.",
]

# ── FONTS ─────────────────────────────────────────────────────────────────────
F  = r"C:\Windows\Fonts"
PI = os.path.join(F, "palai.ttf")
PB = os.path.join(F, "palab.ttf")
PBI= os.path.join(F, "palabi.ttf")
PA = os.path.join(F, "pala.ttf")
SL = os.path.join(F, "segoeuil.ttf")
SR = os.path.join(F, "segoeui.ttf")
SB = os.path.join(F, "segoeuib.ttf")
SS = os.path.join(F, "seguisb.ttf")
GI = os.path.join(F, "georgiai.ttf")
GB = os.path.join(F, "georgiab.ttf")

def fnt(path, size):
    try:    return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

# ── IMAGENES ──────────────────────────────────────────────────────────────────
PARQUE_F = [
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
    os.path.join(IMG, "img3.jpg"),
]
EV_F = [
    os.path.join(IMG, "imagenes","eventos","WhatsApp Image 2026-03-09 at 13.03.52.jpeg"),
    os.path.join(IMG, "imagenes","eventos","WhatsApp Image 2026-03-09 at 13.03.53.jpeg"),
    os.path.join(IMG, "imagenes","eventos","WhatsApp Image 2026-03-09 at 13.04.50.jpeg"),
    os.path.join(IMG, "imagenes","eventos","WhatsApp Image 2026-03-09 at 12.58.04.jpeg"),
]

# ── HELPERS CORE ──────────────────────────────────────────────────────────────
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

def bw(path, size, crop=True, contrast=1.2, brightness=1.0):
    img = load(path, size, crop)
    img = ImageOps.grayscale(img).convert("RGB")
    img = ImageEnhance.Contrast(img).enhance(contrast)
    if brightness != 1.0:
        img = ImageEnhance.Brightness(img).enhance(brightness)
    return img

def grad_v(img, a0=0, a1=220, color=DARK):
    ov = Image.new("RGBA", img.size, (0,0,0,0))
    d  = ImageDraw.Draw(ov)
    w, h = img.size
    for i in range(h):
        a = int(a0 + (a1-a0)*i/max(h-1,1))
        d.line([(0,i),(w,i)], fill=(*color,a))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

def grad_h(img, a0=0, a1=220, color=DARK):
    ov = Image.new("RGBA", img.size, (0,0,0,0))
    d  = ImageDraw.Draw(ov)
    w, h = img.size
    for i in range(w):
        a = int(a0 + (a1-a0)*i/max(w-1,1))
        d.line([(i,0),(i,h)], fill=(*color,a))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

def dark_ov(img, alpha=140):
    ov = Image.new("RGBA", img.size, (0,0,0,alpha))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

def color_ov(img, color, alpha):
    ov = Image.new("RGBA", img.size, (*color, alpha))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

# ── HELPERS TEXTO CON CONTRASTE ───────────────────────────────────────────────
def shadow_text(draw, x, y, text, font, fill, anchor="mm", shadow_alpha=160, blur_r=6):
    """Texto con sombra difuminada para maximo contraste."""
    # Medir texto
    bb = draw.textbbox((0,0), text, font=font, anchor=anchor)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    PAD = blur_r * 3
    # Crear capa de sombra
    layer = Image.new("RGBA", (tw + PAD*2, th + PAD*2), (0,0,0,0))
    ld    = ImageDraw.Draw(layer)
    ld.text((PAD - bb[0], PAD - bb[1]), text, font=font,
            fill=(0,0,0,shadow_alpha), anchor="lt")
    layer = layer.filter(ImageFilter.GaussianBlur(blur_r))
    # Pegar sombra en el canvas destino
    # Necesitamos pegar en la imagen base — usamos un truco: retornamos la sombra
    # para pegarla manualmente. En lugar de eso, simplificamos: doble texto.
    # Primero sombra offset
    draw.text((x+2, y+2), text, font=font, fill=(0,0,0,shadow_alpha), anchor=anchor)
    draw.text((x+1, y+1), text, font=font, fill=(0,0,0,shadow_alpha), anchor=anchor)
    # Luego texto real
    draw.text((x, y), text, font=font, fill=fill, anchor=anchor)

def pill(draw, cx, cy, text, font, text_color, bg_color, pad_x=28, pad_y=12):
    """Texto con fondo solido (pill/badge)."""
    bb = draw.textbbox((0,0), text, font=font, anchor="mm")
    hw = (bb[2]-bb[0])//2 + pad_x
    hh = (bb[3]-bb[1])//2 + pad_y
    draw.rounded_rectangle([cx-hw, cy-hh, cx+hw, cy+hh],
                            radius=hh, fill=bg_color)
    draw.text((cx, cy), text, font=font, fill=text_color, anchor="mm")

def block_text(draw, x, y, text, font, text_color, bg_color, pad_x=20, pad_y=10, anchor="mm"):
    """Texto con fondo rectangular solido."""
    bb = draw.textbbox((0,0), text, font=font, anchor=anchor)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    if anchor == "mm":
        rx1, ry1 = x - tw//2 - pad_x, y - th//2 - pad_y
        rx2, ry2 = x + tw//2 + pad_x, y + th//2 + pad_y
    elif anchor == "lm":
        rx1, ry1 = x - pad_x, y - th//2 - pad_y
        rx2, ry2 = x + tw + pad_x, y + th//2 + pad_y
    else:
        rx1, ry1 = x - tw//2 - pad_x, y - pad_y
        rx2, ry2 = x + tw//2 + pad_x, y + th + pad_y
    draw.rectangle([rx1, ry1, rx2, ry2], fill=bg_color)
    draw.text((x, y), text, font=font, fill=text_color, anchor=anchor)

def ct(draw, x, y, text, font, fill, anchor="mm"):
    draw.text((x, y), text, font=font, fill=fill, anchor=anchor)

def sct(draw, x, y, text, font, fill, anchor="mm"):
    """Texto con sombra simple."""
    draw.text((x+2, y+2), text, font=font, fill=(0,0,0,180), anchor=anchor)
    draw.text((x,   y  ), text, font=font, fill=fill,         anchor=anchor)

def hline(draw, x1, y, x2, fill=GOLD, w=2):
    draw.line([(x1,y),(x2,y)], fill=fill, width=w)

def vline(draw, x, y1, y2, fill=GOLD, w=2):
    draw.line([(x,y1),(x,y2)], fill=fill, width=w)

def corner_frame(draw, x1, y1, x2, y2, color=GOLD, size=50, w=2):
    for (cx,cy),(sx,sy) in zip([(x1,y1),(x2,y1),(x1,y2),(x2,y2)],
                                [(1,1),(-1,1),(1,-1),(-1,-1)]):
        draw.line([(cx,cy),(cx+sx*size,cy)], fill=color, width=w)
        draw.line([(cx,cy),(cx,cy+sy*size)], fill=color, width=w)

def save(img, name):
    img.convert("RGB").save(os.path.join(OUT, name+".jpg"), "JPEG", quality=95, dpi=(300,300))
    print(f"  OK {name}.jpg")


# =============================================================================
# AFICHE 25 — "Experiencia parque"  1080x1080
# Foto parque de fondo, copy experiencial, texto con pill dorada + sombras
# =============================================================================
def afiche25():
    W, H = 1080, 1080
    canvas = load(PARQUE_F[1], (W, H))       # quienes-somos: foto parque bella
    canvas = dark_ov(canvas, 110)
    canvas = color_ov(canvas, DARK, 60)
    draw   = ImageDraw.Draw(canvas)

    corner_frame(draw, 34, 34, W-34, H-34, GOLD_D, size=60, w=1)

    # Badge superior
    pill(draw, W//2, 90, "PARQUE CENTENARIO PRIVADO",
         fnt(SS, 17), DARK, GOLD)

    # Frase experiencial grande
    sct(draw, W//2, 320, "Una experiencia", fnt(PI, 72), WHITE)
    sct(draw, W//2, 408, "que no se olvida.", fnt(PBI, 80), GOLD)

    hline(draw, 140, 468, W-140, GOLD, w=2)

    sct(draw, W//2, 516, "Parque de mas de 100 anos,", fnt(PI, 30), CREAM_ALT)
    sct(draw, W//2, 560, "solo para ti y tus invitados.", fnt(PI, 30), CREAM_ALT)

    hline(draw, 140, 604, W-604+140+140, GOLD_D, w=1)  # linea corta
    hline(draw, 140, 604, W-140, GOLD_D, w=1)

    # Foto BW novios — inset pequeño esquina inferior derecha
    inset_bw = bw(FOTO_BW, (320, 210))
    inset_bw = dark_ov(inset_bw, 20)
    IX, IY   = W - 340, 640
    canvas.paste(inset_bw, (IX, IY))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([IX-3, IY-3, IX+320+3, IY+210+3], outline=GOLD, width=2)
    ct(draw, IX+160, IY+210+18, "MATRIMONIOS", fnt(SS, 13), GOLD_L, anchor="mm")

    # Info izquierda
    sct(draw, 200, 680, N1, fnt(PI, 36), WHITE)
    sct(draw, 200, 726, N2, fnt(PB, 44), GOLD)
    hline(draw, 60, 764, 400, GOLD, w=1)
    sct(draw, 200, 798, UBI,    fnt(SL, 18), CREAM_ALT)
    sct(draw, 200, 828, "80+ anos de historia", fnt(SL, 16), MUTED)

    # Footer
    draw.rectangle([0, H-96, W, H], fill=(*DARK, 230))
    hline(draw, 0, H-96, W, GOLD, w=2)
    ct(draw, W//2, H-60, IG + "   *   " + WA + "   *   " + WEB,
       fnt(SR, 18), GOLD_L)

    save(canvas, "afiche25_experiencia_parque")


# =============================================================================
# AFICHE 26 — "Luxury dark full BW"  1080x1080
# La foto BW ocupa todo, texto sobre bloque oscuro semitransparente central
# =============================================================================
def afiche26():
    W, H = 1080, 1080
    canvas = bw(FOTO_BW, (W, H), contrast=1.25, brightness=0.95)
    canvas = color_ov(canvas, GOLD_D, 12)   # tinte dorado sutil
    draw   = ImageDraw.Draw(canvas)

    # Bloque central oscuro semitransparente
    BH = 380
    BY = (H - BH) // 2
    block = Image.new("RGBA", (W, BH), (*DARK, 210))
    canvas = Image.alpha_composite(canvas.convert("RGBA"),
             Image.new("RGBA", (W,H),(0,0,0,0)))
    canvas = canvas.convert("RGB")
    canvas_rgba = canvas.convert("RGBA")
    block_layer = Image.new("RGBA", (W, H), (0,0,0,0))
    block_layer.paste(block, (0, BY))
    canvas = Image.alpha_composite(canvas_rgba, block_layer).convert("RGB")

    draw = ImageDraw.Draw(canvas)
    hline(draw, 80,  BY+16, W-80, GOLD,   w=2)
    hline(draw, 80,  BY+22, W-80, GOLD_L, w=1)

    ct(draw, W//2, BY+80,  N1, fnt(PI,  52), GOLD_L)
    ct(draw, W//2, BY+148, N2, fnt(PBI, 70), GOLD)

    hline(draw, 200, BY+200, W-200, GOLD_L, w=1)
    ct(draw, W//2, BY+240, "El parque que siempre sonaste.", fnt(GI, 28), WHITE)
    ct(draw, W//2, BY+282, UBI,                               fnt(SL, 20), CREAM_ALT)
    hline(draw, 200, BY+316, W-200, GOLD_L, w=1)
    ct(draw, W//2, BY+350, IG + "   *   " + WA,               fnt(SR, 18), GOLD)

    hline(draw, 80, BY+BH-22, W-80, GOLD_L, w=1)
    hline(draw, 80, BY+BH-16, W-80, GOLD,   w=2)

    # Badge superior esquina
    pill(draw, 160, 52, "MATRIMONIOS", fnt(SS, 16), DARK, GOLD)
    # Badge inferior esquina
    pill(draw, W-160, H-52, "PARQUE CENTENARIO", fnt(SS, 14), DARK, GOLD_L)

    save(canvas, "afiche26_luxury_dark_bw")


# =============================================================================
# AFICHE 27 — "Verde y oro"  1080x1080
# Foto parque (tono verde-sage), bloque crema abajo con texto oscuro
# Muy diferente: claro, aireado, luxury editorial
# =============================================================================
def afiche27():
    W, H = 1080, 1080
    FOTO_H = 640
    TEXT_H = H - FOTO_H

    canvas = Image.new("RGB", (W, H), CREAM)

    # Foto parque arriba con tono sage
    top = load(PARQUE_F[4], (W, FOTO_H))   # img16: parque verde
    top = ImageEnhance.Color(top).enhance(0.85)  # desaturar levemente
    top = grad_v(top, a0=0, a1=80, color=CREAM)  # fade suave al crema abajo
    canvas.paste(top, (0, 0))

    # Inset foto BW novios - esquina superior derecha sobre la foto
    INS_W, INS_H = 290, 390
    ins = bw(FOTO_BW, (INS_W, INS_H))
    canvas.paste(ins, (W - INS_W - 40, 40))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([W-INS_W-43, 37, W-37, 37+INS_H], outline=GOLD, width=3)

    # Separador horizontal dorado
    draw.rectangle([0, FOTO_H-3, W, FOTO_H+3], fill=GOLD)

    # Zona crema inferior
    draw = ImageDraw.Draw(canvas)
    ct(draw, W//2 - 80, FOTO_H + 56,  N1, fnt(PI,  50), DARK,   anchor="mm")
    ct(draw, W//2 - 80, FOTO_H + 120, N2, fnt(PBI, 64), GOLD,   anchor="mm")

    # Linea vertical dorada en el texto
    vline(draw, W//2 + 100, FOTO_H+20, H-20, GOLD, w=1)

    # Columna derecha del bloque texto
    RX = W//2 + 120
    RC = RX + (W - RX - 30)//2
    ct(draw, RC, FOTO_H + 50,  "Parque centenario",  fnt(SS, 16), GOLD,    anchor="mm")
    ct(draw, RC, FOTO_H + 82,  "privado y exclusivo",fnt(SL, 18), MUTED,   anchor="mm")
    hline(draw, RX, FOTO_H+108, W-30, GOLD_D, w=1)
    ct(draw, RC, FOTO_H + 140, "80+ anos de historia",fnt(SL, 17), DARK,   anchor="mm")
    ct(draw, RC, FOTO_H + 170, UBI,                   fnt(SL, 17), SAGE,   anchor="mm")
    hline(draw, RX, FOTO_H+196, W-30, GOLD_D, w=1)
    ct(draw, RC, FOTO_H + 228, IG,                    fnt(SB, 18), GOLD,   anchor="mm")
    ct(draw, RC, FOTO_H + 260, WA,                    fnt(SR, 17), DARK,   anchor="mm")

    # Frase grande izquierda
    hline(draw, 40, FOTO_H + 160, W//2+80, GOLD_D, w=1)
    ct(draw, 40, FOTO_H + 195, "Donde la naturaleza",  fnt(GI, 24), DARK, anchor="lm")
    ct(draw, 40, FOTO_H + 230, "es el escenario.",      fnt(GI, 24), GOLD_D, anchor="lm")

    # Badge parque sobre foto
    pill(draw, 160, 56, "EL PARQUE", fnt(SS, 16), WHITE, (*DARK, 200))

    save(canvas, "afiche27_verde_y_oro")


# =============================================================================
# AFICHE 28 — "Tipografico bold"  1080x1080
# Tipografia dominante, foto BW de fondo muy oscura, copy en blanco grande
# =============================================================================
def afiche28():
    W, H = 1080, 1080
    canvas = bw(FOTO_BW, (W, H), contrast=1.1, brightness=0.7)
    canvas = dark_ov(canvas, 130)
    draw   = ImageDraw.Draw(canvas)

    # Grilla sutil
    for x in range(0, W, 120):
        draw.line([(x,0),(x,H)], fill=(*GOLD_D, 20), width=1)

    # Texto muy grande — el copy ES el diseño
    sct(draw, W//2, 130, "UN PARQUE",     fnt(GB, 80), WHITE)
    sct(draw, W//2, 224, "QUE TIENE",     fnt(GB, 80), WHITE)
    sct(draw, W//2, 318, "MAS DE",        fnt(GB, 80), WHITE)

    # Numero grande dorado
    sct(draw, W//2, 470, "80",  fnt(PBI, 240), GOLD)

    sct(draw, W//2, 650, "ANOS DE",       fnt(GB, 80), WHITE)
    sct(draw, W//2, 744, "HISTORIA.",     fnt(GB, 80), GOLD)

    hline(draw, 60, 810, W-60, GOLD, w=3)

    ct(draw, W//2, 858, N1.upper() + " " + N2.upper(), fnt(SS, 24), GOLD_L)
    ct(draw, W//2, 898, UBI,                            fnt(SL, 20), CREAM_ALT)

    draw.rectangle([0, H-80, W, H], fill=(*DARK, 220))
    hline(draw, 0, H-80, W, GOLD, w=2)
    ct(draw, W//2, H-40, IG + "   *   " + WA, fnt(SR, 18), GOLD)

    save(canvas, "afiche28_tipografico_bold")


# =============================================================================
# AFICHE 29 — "Duotono verde-dorado"  1080x1080
# Efecto duotono sobre foto BW: sombras en verde sage, luces en dorado
# =============================================================================
def afiche29():
    W, H = 1080, 1080

    # Foto BW base
    gray = ImageOps.grayscale(load(FOTO_BW, (W, H))).convert("RGB")
    gray = ImageEnhance.Contrast(gray).enhance(1.2)

    # Duotono: mapear pixel gris -> interpolacion sage-gold
    r_ch, g_ch, b_ch = gray.split()
    import array

    def make_lut(c0, c1):
        return bytes([int(c0 + (c1-c0)*i/255) for i in range(256)])

    lut_r = make_lut(SAGE[0], GOLD[0])
    lut_g = make_lut(SAGE[1], GOLD[1])
    lut_b = make_lut(SAGE[2], GOLD[2])

    r_new = r_ch.point(lut_r)
    g_new = g_ch.point(lut_g)
    b_new = b_ch.point(lut_b)
    duo   = Image.merge("RGB", (r_new, g_new, b_new))
    duo   = ImageEnhance.Brightness(duo).enhance(0.82)

    canvas = duo
    canvas = grad_v(canvas, a0=0, a1=200, color=DARK)
    draw   = ImageDraw.Draw(canvas)

    # Marco de esquinas en crema
    corner_frame(draw, 36, 36, W-36, H-36, CREAM_ALT, size=55, w=1)

    # Badge
    pill(draw, W//2, 78, "EXPERIENCIA UNICA EN LOS ANDES", fnt(SS, 15), DARK, CREAM)

    # Texto
    sct(draw, W//2, 240, N1,  fnt(PI,  64), CREAM_ALT)
    sct(draw, W//2, 322, N2,  fnt(PBI, 82), WHITE)
    hline(draw, 160, 378, W-160, (*CREAM_ALT, 200), w=1)
    sct(draw, W//2, 424, "Historia, elegancia", fnt(GI, 34), CREAM_ALT)
    sct(draw, W//2, 470, "y naturaleza.",        fnt(GI, 34), WHITE)

    # Zona inferior
    sct(draw, W//2, H-296, "Parque centenario privado",  fnt(SL, 22), CREAM_ALT)
    sct(draw, W//2, H-258, UBI,                           fnt(SL, 20), (*CREAM_ALT,))
    hline(draw, 160, H-224, W-160, (*CREAM_ALT,200), w=1)
    sct(draw, W//2, H-180, IG,  fnt(SB, 22), WHITE)
    sct(draw, W//2, H-140, WA,  fnt(SR, 20), CREAM_ALT)
    sct(draw, W//2, H-100, WEB, fnt(SL, 17), (*CREAM_ALT,))
    hline(draw, 160, H-68,  W-160, (*CREAM_ALT,200), w=1)

    save(canvas, "afiche29_duotono_sage_gold")


# =============================================================================
# AFICHE 30 — "Antes y despues"  1080x1080
# Grilla asimetrica: parque (grande, color) + foto BW novios (grande)
# Con texto superpuesto en cada mitad
# =============================================================================
def afiche30():
    W, H = 1080, 1080
    canvas = Image.new("RGB", (W, H), DARK)
    GAP    = 5

    # Superior izquierda: parque grande
    TW, TH = W - 400 - GAP, H//2 - GAP//2
    top_l  = load(PARQUE_F[0], (TW, TH))
    top_l  = dark_ov(top_l, 60)
    canvas.paste(top_l, (0, 0))

    # Superior derecha: foto BW pequeña
    bw_s = bw(FOTO_BW, (400, TH))
    canvas.paste(bw_s, (TW+GAP, 0))

    # Inferior izquierda: foto BW grande
    BW_W = 400
    bot_l = bw(FOTO_BW, (BW_W, H//2 - GAP//2))
    canvas.paste(bot_l, (0, H//2+GAP//2))

    # Inferior derecha: foto evento
    bot_r = load(EV_F[0], (W-BW_W-GAP, H//2 - GAP//2))
    bot_r = dark_ov(bot_r, 80)
    canvas.paste(bot_r, (BW_W+GAP, H//2+GAP//2))

    draw = ImageDraw.Draw(canvas)

    # Separadores dorados
    draw.rectangle([TW, 0, TW+GAP, H], fill=GOLD_D)
    draw.rectangle([0, H//2-1, W, H//2+GAP], fill=GOLD)
    draw.rectangle([BW_W, H//2+GAP, BW_W+GAP, H], fill=GOLD_D)

    # Textos con sombra sobre cada cuadrante
    # Superior izquierda: parque
    sct(draw, TW//2, TH-80, "El parque",         fnt(PI,  38), WHITE)
    sct(draw, TW//2, TH-36, "que te enamora.",   fnt(PBI, 44), GOLD)

    # Superior derecha: novios pequeño
    sct(draw, TW+GAP+200, 90, "TU DIA", fnt(SS, 20), GOLD)

    # Inferior izquierda: BW novios
    sct(draw, BW_W//2, H//2+GAP//2+70, "Tu amor,",      fnt(PI,  34), WHITE, anchor="mm")
    sct(draw, BW_W//2, H//2+GAP//2+112,"nuestro lugar.", fnt(PBI, 38), GOLD,  anchor="mm")

    # Inferior derecha: evento
    RC = BW_W+GAP + (W-BW_W-GAP)//2
    BH = H//2 - GAP//2
    sct(draw, RC, H//2+GAP//2 + BH-80, N1, fnt(PI,  32), WHITE)
    sct(draw, RC, H//2+GAP//2 + BH-40, N2, fnt(PB,  40), GOLD)

    # Footer
    draw.rectangle([0, H-70, W, H], fill=(*DARK, 230))
    hline(draw, 0, H-70, W, GOLD, w=2)
    ct(draw, W//2, H-35, UBI + "   *   " + IG + "   *   " + WA,
       fnt(SR, 16), GOLD_L)

    save(canvas, "afiche30_antes_y_despues")


# =============================================================================
# AFICHE 31 — "Noche de gala"  1080x1080
# Fondo muy oscuro casi negro, foto BW novios en diagonal/recortada,
# detalles en dorado, feel de cartel de gala nocturna
# =============================================================================
def afiche31():
    W, H = 1080, 1080

    # Fondo: foto parque muy oscurecida + viñeta
    bg = load(PARQUE_F[2], (W, H))
    bg = dark_ov(bg, 195)
    bg = color_ov(bg, DARK, 80)
    canvas = bg
    draw   = ImageDraw.Draw(canvas)

    # Viñeta circular
    for r in range(0, 300, 12):
        alpha = int(120 * r / 300)
        draw.ellipse([r, r, W-r, H-r], outline=(0,0,0,alpha), width=12)

    # Foto BW novios — enmarcada con borde dorado, centrada horizontalmente
    BW_W, BW_H = 540, 360
    BX = (W - BW_W)//2
    BY = 120
    bw_img = bw(FOTO_BW, (BW_W, BW_H))
    canvas.paste(bw_img, (BX, BY))
    draw = ImageDraw.Draw(canvas)
    # Marco dorado doble
    draw.rectangle([BX-5, BY-5, BX+BW_W+5, BY+BW_H+5], outline=GOLD_D, width=1)
    draw.rectangle([BX-12,BY-12,BX+BW_W+12,BY+BW_H+12], outline=GOLD, width=2)

    # Ornamento sobre la foto
    ct(draw, W//2, BY-50, "* * * * *", fnt(SR, 20), GOLD_D)

    # Texto principal
    ct(draw, W//2, BY+BW_H+70,  N1,              fnt(PI,  60), GOLD_L)
    ct(draw, W//2, BY+BW_H+142, N2,              fnt(PBI, 78), GOLD)

    hline(draw, 120, BY+BW_H+198, W-120, GOLD, w=2)

    ct(draw, W//2, BY+BW_H+244, "Vive lo extraordinario.",  fnt(GI,  30), WHITE)
    ct(draw, W//2, BY+BW_H+286, "Parque centenario privado.",fnt(SL,  21), CREAM_ALT)

    hline(draw, 120, BY+BW_H+320, W-120, GOLD_D, w=1)

    ct(draw, W//2, BY+BW_H+358, UBI,  fnt(SL, 20), MUTED)

    # Footer dorado
    draw.rectangle([0, H-90, W, H], fill=GOLD)
    ct(draw, W//2, H-56, N1.upper() + " " + N2.upper(), fnt(PB, 22), DARK)
    ct(draw, W//2, H-24, IG + "   *   " + WA, fnt(SR, 17), DARK)

    save(canvas, "afiche31_noche_de_gala")


# =============================================================================
# AFICHE 32 — "Story dorado"  1080x1920
# Vertical premium: foto BW novios top + parque bottom + copy centrado fuerte
# =============================================================================
def afiche32():
    W, H = 1080, 1920
    canvas = Image.new("RGB", (W, H), DARK)

    # Zona superior: foto BW (50%)
    top = bw(FOTO_BW, (W, 960))
    top = grad_v(top, a0=0, a1=255, color=DARK)
    canvas.paste(top, (0, 0))

    # Zona inferior: parque (50%)
    bot = load(PARQUE_F[1], (W, 960))
    bot = grad_v(bot, a0=60, a1=220, color=DARK)
    canvas.paste(bot, (0, 960))

    draw = ImageDraw.Draw(canvas)

    # Linea dorada central
    draw.rectangle([0, 956, W, 964], fill=GOLD)

    # Marca en cinta central sobre la línea
    draw.rectangle([W//2-260, 938, W//2+260, 982], fill=DARK)
    ct(draw, W//2, 960, "CASONA FUNDO EL CASTILLO", fnt(SS, 18), GOLD, anchor="mm")

    # Header zona superior (sobre foto BW)
    # Bloque oscuro header
    draw.rectangle([0, 0, W, 200], fill=(*DARK, 200))
    hline(draw, 0, 200, W, GOLD, w=3)

    ct(draw, W//2, 68,  N1,  fnt(PI,  58), GOLD_L)
    ct(draw, W//2, 148, N2,  fnt(PBI, 78), GOLD)

    # Texto zona superior (foto BW)
    sct(draw, W//2, 700, "Tu amor merece",          fnt(PI,  48), WHITE)
    sct(draw, W//2, 758, "el escenario perfecto.",   fnt(PBI, 52), GOLD)
    hline(draw, 100, 812, W-100, GOLD, w=2)
    sct(draw, W//2, 856, UBI, fnt(SL, 26), CREAM_ALT)
    sct(draw, W//2, 900, "Parque centenario privado", fnt(SL, 22), MUTED)

    # Texto zona inferior (parque)
    sct(draw, W//2, 1040, "80 anos de historia",     fnt(PI,  42), WHITE)
    sct(draw, W//2, 1096, "al alcance de tu mano.",  fnt(PI,  42), GOLD_L)
    hline(draw, 120, 1148, W-120, GOLD_D, w=1)
    sct(draw, W//2, 1198, "* Matrimonios",           fnt(SL, 26), CREAM_ALT)
    sct(draw, W//2, 1242, "* Eventos corporativos",  fnt(SL, 26), CREAM_ALT)
    sct(draw, W//2, 1286, "* Celebraciones privadas",fnt(SL, 26), CREAM_ALT)
    sct(draw, W//2, 1330, "* Hasta 200 personas",    fnt(SL, 26), CREAM_ALT)

    # 3 mini fotos del parque
    MW = W//3 - 8
    MH = 180
    minis = [PARQUE_F[3], PARQUE_F[6], PARQUE_F[9]]
    for i, path in enumerate(minis):
        mx = i*(MW+8)
        mi = load(path, (MW, MH))
        canvas.paste(mi, (mx, 1410))
        draw = ImageDraw.Draw(canvas)
        draw.rectangle([mx, 1410, mx+MW, 1410+MH], outline=GOLD_D, width=2)

    draw = ImageDraw.Draw(canvas)

    # Footer
    draw.rectangle([0, 1608, W, H], fill=(*DARK, 240))
    hline(draw, 0, 1608, W, GOLD, w=3)

    ct(draw, W//2, 1678, IG,  fnt(SB, 32), GOLD)
    ct(draw, W//2, 1730, WA,  fnt(SR, 28), CREAM_ALT)
    ct(draw, W//2, 1778, WEB, fnt(SL, 22), MUTED)
    hline(draw, 80, 1820, W-80, GOLD_D, w=1)
    ct(draw, W//2, 1862, UBI, fnt(SL, 22), SAGE)
    ct(draw, W//2, 1908, "Reservas al WhatsApp", fnt(PI, 26), GOLD_L)

    save(canvas, "afiche32_story_dorado")


# =============================================================================
# AFICHE 33 — "Tres momentos"  1080x1080
# Tres fotos horizontales apiladas (parque / BW novios / evento)
# Con texto encima en zona oscura izquierda
# =============================================================================
def afiche33():
    W, H = 1080, 1080
    TEXT_W = 380
    FOTO_W = W - TEXT_W
    ROW_H  = H // 3

    canvas = Image.new("RGB", (W, H), DARK)

    # Tres filas de foto a la derecha
    rows = [
        (PARQUE_F[0],  "Parque centenario"),
        (FOTO_BW,      "Matrimonios"),   # BW
        (EV_F[1],      "Celebraciones"),
    ]
    for i, (path, label) in enumerate(rows):
        y = i * ROW_H
        if path == FOTO_BW:
            foto = bw(path, (FOTO_W, ROW_H))
        else:
            foto = load(path, (FOTO_W, ROW_H))
            foto = dark_ov(foto, 50)
        canvas.paste(foto, (TEXT_W, y))

    draw = ImageDraw.Draw(canvas)

    # Separadores horizontales
    for i in range(1, 3):
        draw.rectangle([TEXT_W, i*ROW_H-2, W, i*ROW_H+2], fill=GOLD)

    # Labels sobre fotos
    for i, (_, label) in enumerate(rows):
        ly = i*ROW_H + ROW_H - 28
        block_text(draw, TEXT_W + FOTO_W//2, ly, label.upper(),
                   fnt(SS, 14), DARK, GOLD, pad_x=18, pad_y=7)

    # Panel izquierdo: texto
    vline(draw, TEXT_W, 0, H, GOLD, w=2)

    hline(draw, 24, 60, TEXT_W-24, GOLD, w=1)

    ct(draw, TEXT_W//2, 110, N1,   fnt(PI,  36), GOLD_L)
    ct(draw, TEXT_W//2, 158, N2,   fnt(PBI, 46), GOLD)

    hline(draw, 24, 194, TEXT_W-24, GOLD_D, w=1)

    ct(draw, TEXT_W//2, 240, "El lugar", fnt(GI, 26), WHITE)
    ct(draw, TEXT_W//2, 276, "donde todo", fnt(GI, 26), WHITE)
    ct(draw, TEXT_W//2, 312, "es posible.", fnt(GI, 26), GOLD_L)

    hline(draw, 24, 350, TEXT_W-24, GOLD_D, w=1)

    items = [
        "80+ anos de",
        "historia",
        "",
        "Parque",
        "centenario",
        "privado",
        "",
        UBI,
    ]
    y = 388
    for it in items:
        if it:
            ct(draw, TEXT_W//2, y, it, fnt(SL, 16), CREAM_ALT)
        y += 30

    hline(draw, 24, y+10, TEXT_W-24, GOLD, w=1)
    ct(draw, TEXT_W//2, y+44, IG,  fnt(SB, 14), GOLD)
    ct(draw, TEXT_W//2, y+72, WA,  fnt(SR, 13), CREAM_ALT)
    ct(draw, TEXT_W//2, y+96, WEB, fnt(SL, 12), MUTED)

    hline(draw, 24, H-40, TEXT_W-24, GOLD_L, w=1)

    save(canvas, "afiche33_tres_momentos")


# =============================================================================
# AFICHE 34 — "Cartel poético"  1080x1080
# Fondo: foto BW novios muy oscura. Copy largo poético, estilo quote card.
# Muy shareable para IG.
# =============================================================================
def afiche34():
    W, H = 1080, 1080
    canvas = bw(FOTO_BW, (W, H), contrast=1.15, brightness=0.6)
    canvas = color_ov(canvas, DARK, 100)
    draw   = ImageDraw.Draw(canvas)

    corner_frame(draw, 44, 44, W-44, H-44, GOLD_D, size=65, w=1)
    corner_frame(draw, 60, 60, W-60, H-60, GOLD,   size=44, w=2)

    # Ornamento superior
    ct(draw, W//2, 120, "* * *", fnt(PA, 28), GOLD_D)

    # Quote grande central
    lines_up = [
        ("Hay lugares",   fnt(GI, 54),  CREAM_ALT),
        ("que no se",     fnt(GI, 54),  CREAM_ALT),
        ("describen.",    fnt(PBI, 62), GOLD),
    ]
    y = 220
    for text, f, color in lines_up:
        sct(draw, W//2, y, text, f, color)
        y += f.size + 10  # aproximado

    y = 220
    for text, f, color in lines_up:
        bb = draw.textbbox((0,0), text, font=f, anchor="mm")
        y += (bb[3]-bb[1]) + 14

    sct(draw, W//2, y+20, "Solo se viven.", fnt(PBI, 62), GOLD)

    hline(draw, 160, y+82, W-160, GOLD, w=2)

    sct(draw, W//2, y+126, "Parque centenario de Los Andes.",   fnt(PI,  30), WHITE)
    sct(draw, W//2, y+170, "El parque que siempre sonaste.",    fnt(PI,  30), CREAM_ALT)

    hline(draw, 160, y+208, W-160, GOLD_D, w=1)

    sct(draw, W//2, y+252, N1 + " " + N2,  fnt(PB,  28), GOLD_L)
    sct(draw, W//2, y+292, UBI,             fnt(SL,  20), CREAM_ALT)

    hline(draw, 160, y+326, W-160, GOLD_D, w=1)

    sct(draw, W//2, y+360, IG,  fnt(SB, 20), GOLD)
    sct(draw, W//2, y+394, WA,  fnt(SR, 19), CREAM_ALT)

    ct(draw, W//2, H-80, "* * *", fnt(PA, 28), GOLD_D)

    save(canvas, "afiche34_cartel_poetico")


# =============================================================================
print("=" * 60)
print("  CASONA EL CASTILLO - Afiches Tanda 4")
print("  Alto contraste | Parque experiencia | Solo JPG")
print("=" * 60)
print()

afiche25()
afiche26()
afiche27()
afiche28()
afiche29()
afiche30()
afiche31()
afiche32()
afiche33()
afiche34()

print()
print("LISTO - Archivos en:", OUT)
print("=" * 60)
