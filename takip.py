"""Takip et animasyonu (video ortasında bir kez).
Kullanım: draw_takip(frame_rgba, tt)  -> tt: animasyon başından beri geçen sn (0..SURE)
Akış: kapsül alttan kayarak gelir -> imleç gelir -> tıklar (dalga) -> düğme "TAKİP EDİLDİ" olur -> kapsül iner.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
SURE = 5.0
KOK = os.path.dirname(os.path.abspath(__file__))
F_UI = lambda s: ImageFont.truetype(os.path.join(KOK, "fonts", "Inter-SemiBold.otf"), s)
F_B = lambda s: ImageFont.truetype(os.path.join(KOK, "fonts", "InterDisplay-Black.otf"), s)
KIRMIZI = (214, 40, 40)
GRI = (58, 63, 71)
KREM = (246, 239, 227)
AMBER = (242, 181, 68)

def _c(x): return max(0.0, min(1.0, x))
def _ease(x): x = _c(x); return 1 - (1 - x) ** 3
def _back(x):                     # hafif taşmalı yerleşme
    x = _c(x); c1 = 1.4; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def _io(x): x = _c(x); return x * x * (3 - 2 * x)

_cache = {}
def _avatar(d):
    k = ("av", d)
    if k not in _cache:
        p = os.path.join(KOK, "assets", "kanal", "logo_takip.png")
        im = Image.open(p).convert("RGBA").resize((d * 3, d * 3), Image.LANCZOS)
        m = Image.new("L", (d * 3, d * 3), 0); ImageDraw.Draw(m).ellipse([0, 0, d * 3 - 1, d * 3 - 1], fill=255)
        im.putalpha(m); _cache[k] = im.resize((d, d), Image.LANCZOS)
    return _cache[k]

def _imlec(s=1.0):
    k = ("im", s)
    if k not in _cache:
        ss = 4; w, h = int(58 * s), int(84 * s)
        im = Image.new("RGBA", (w * ss, h * ss), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        pts = [(0, 0), (0, 64), (16, 50), (28, 76), (38, 71), (27, 46), (48, 46)]
        P = [(4 * ss + x * s * ss, 4 * ss + y * s * ss) for x, y in pts]
        d.polygon(P, fill=(255, 255, 255, 255), outline=(10, 10, 10, 255), width=int(4 * s * ss))
        im = im.resize((w, h), Image.LANCZOS)
        gol = Image.new("RGBA", im.size, (0, 0, 0, 0)); gol.putalpha(im.getchannel("A").point(lambda v: v * 0.45))
        gol = gol.filter(ImageFilter.GaussianBlur(4))
        out = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0)); out.alpha_composite(gol, (5, 6)); out.alpha_composite(im, (0, 0))
        _cache[k] = out
    return _cache[k]

def _tik(d, cx, cy, r, renk, kal):
    d.line([(cx - r, cy), (cx - r * 0.3, cy + r * 0.7), (cx + r, cy - r * 0.75)], fill=renk, width=kal, joint="curve")

def draw_takip(frame, tt, y_merkez=1170):
    if tt < 0 or tt > SURE: return
    giris = _back(tt / 0.9)
    cikis = _io((tt - (SURE - 0.7)) / 0.7)
    alfa = _io(tt / 0.6) * (1 - cikis)
    if alfa <= 0.01: return
    dy = (1 - giris) * 110 + cikis * 100

    tik_an = 2.75                               # tıklama anı
    basili = tt >= tik_an + 0.08
    bas = 1.0
    if tik_an <= tt < tik_an + 0.16: bas = 0.92 + 0.08 * abs((tt - tik_an - 0.08) / 0.08)

    # --- kapsül ---
    KW, KH = 760, 150
    ss = 3
    kat = Image.new("RGBA", (KW * ss, KH * ss), (0, 0, 0, 0)); d = ImageDraw.Draw(kat)
    d.rounded_rectangle([0, 0, KW * ss - 1, KH * ss - 1], radius=KH * ss // 2, fill=(12, 18, 28, 225),
                        outline=(255, 255, 255, 40), width=2 * ss)
    kat = kat.resize((KW, KH), Image.LANCZOS)
    d = ImageDraw.Draw(kat)
    av = _avatar(108); kat.alpha_composite(av, (22, (KH - 108) // 2))
    d.text((150, KH / 2 - 20), "Sıradan Değil", font=F_B(40), fill=KREM, anchor="lm")
    d.text((150, KH / 2 + 24), "Tarihin gündelik hikâyeleri", font=F_UI(26), fill=(170, 182, 196), anchor="lm")

    # --- düğme ---
    BW, BH = 250, 84
    yazi = "TAKİP EDİLDİ" if basili else "+ TAKİP ET"
    renk = GRI if basili else KIRMIZI
    dug = Image.new("RGBA", (BW * ss, BH * ss), (0, 0, 0, 0)); dd = ImageDraw.Draw(dug)
    dd.rounded_rectangle([0, 0, BW * ss - 1, BH * ss - 1], radius=18 * ss, fill=renk)
    if basili:
        _tik(dd, 34 * ss, BH * ss / 2, 11 * ss, AMBER, 5 * ss)
        dd.text((BW * ss / 2 + 16 * ss, BH * ss / 2), yazi, font=F_UI(27 * ss), fill=(235, 235, 235), anchor="mm")
    else:
        dd.text((BW * ss / 2, BH * ss / 2), yazi, font=F_UI(31 * ss), fill=(255, 255, 255), anchor="mm")
    dug = dug.resize((int(BW * bas), int(BH * bas)), Image.LANCZOS)
    bx = KW - 24 - BW // 2; by = KH // 2
    kat.alpha_composite(dug, (int(bx - dug.width / 2), int(by - dug.height / 2)))

    # tıklama dalgası
    if tik_an <= tt < tik_an + 0.7:
        p = (tt - tik_an) / 0.7
        dal = Image.new("RGBA", kat.size, (0, 0, 0, 0)); ddl = ImageDraw.Draw(dal)
        r = 20 + 110 * _ease(p)
        ddl.ellipse([bx - r, by - r, bx + r, by + r], outline=(255, 255, 255, int(170 * (1 - p))), width=5)
        kat.alpha_composite(dal)

    # kapsülü kareye koy
    if alfa < 1:
        a = kat.getchannel("A").point(lambda v: int(v * alfa)); kat.putalpha(a)
    kx = (W - KW) // 2; ky = int(y_merkez - KH / 2 + dy)
    frame.alpha_composite(kat, (kx, ky))

    # --- imleç ---
    hedef = (kx + bx + 10, ky + by + 6)
    bas_nokta = (W + 40, H * 0.80)
    if tt >= 1.2:
        m = _io((tt - 1.2) / 1.3)
        x = bas_nokta[0] + (hedef[0] - bas_nokta[0]) * m
        y = bas_nokta[1] + (hedef[1] - bas_nokta[1]) * m - 60 * (4 * m * (1 - m))   # hafif yay
        olc = 0.88 if tik_an <= tt < tik_an + 0.14 else 1.0
        im = _imlec(1.25 * olc)
        ia = alfa * (1 - _c((tt - 3.9) / 0.5))
        if ia > 0.01:
            if ia < 1:
                im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * ia)))
            frame.alpha_composite(im, (int(x), int(y)))
