"""Sıradan Değil — Shorts renderer.

timeline.json + voice.wav  ->  1080x1920 / 30fps MP4
Kullanım: python3 render.py build/001 out/001_kolonya.mp4
Segmentin images.json'da fotoğrafı varsa: tam ekran gerçek fotoğraf + yavaş kaydırma/yakınlaştırma.
Yoksa: kodla çizilmiş sahne (yedek).
"""
import json, math, os, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

W, H, FPS = 1080, 1920, 30
build, out_path = sys.argv[1], sys.argv[2]
TL = json.load(open(os.path.join(build, "timeline.json"), encoding="utf-8"))
SEGS, DUR = TL["segments"], TL["duration"]
EP = TL["episode"]

# ---------- marka ----------
BG_TOP, BG_BOT = (13, 24, 38), (6, 12, 20)
CREAM = (246, 239, 227)
AMBER = (242, 181, 68)
MUTED = (150, 165, 180)
TEAL = (64, 170, 160)
ROSE = (226, 112, 128)

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
INTER = FONT_DIR + "/"
LORA = os.path.join(FONT_DIR, "Lora-Variable.ttf")
LORA_I = os.path.join(FONT_DIR, "Lora-Italic-Variable.ttf")
_fc = {}
def font(path, size, var=None):
    k = (path, size, var)
    if k not in _fc:
        f = ImageFont.truetype(path, size)
        if var:
            try: f.set_variation_by_name(var)
            except Exception: pass
        _fc[k] = f
    return _fc[k]
F_CAP = lambda s: font(INTER + "InterDisplay-Black.otf", s)
F_UI = lambda s: font(INTER + "Inter-SemiBold.otf", s)
F_SERIF = lambda s: font(LORA, s, "Bold")
F_SERIF_I = lambda s: font(LORA_I, s, "Italic")

# ---------- yardımcılar ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_io(x): x = clamp(x); return x * x * (3 - 2 * x)
def lerp(a, b, t): return a + (b - a) * t
def with_alpha(c, a): return (*c[:3], int(255 * clamp(a)))

def text_center(d, xy, txt, f, fill, anchor="mm"):
    d.text(xy, txt, font=f, fill=fill, anchor=anchor)

def paste_center(base, sprite, cx, cy, scale=1.0, alpha=1.0, rot=0.0):
    if alpha <= 0.003: return
    s = sprite
    if scale != 1.0:
        s = s.resize((max(1, int(s.width * scale)), max(1, int(s.height * scale))), Image.LANCZOS)
    if rot: s = s.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1:
        a = s.getchannel("A").point(lambda v: int(v * alpha))
        s = s.copy(); s.putalpha(a)
    base.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))

def aa_layer(w, h, draw_fn, ss=3):
    """Süper örnekleme ile kenarı yumuşak sprite."""
    im = Image.new("RGBA", (w * ss, h * ss), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(im), ss)
    return im.resize((w, h), Image.LANCZOS)

# ---------- arka plan ----------
def make_bg():
    y = np.linspace(0, 1, H)[:, None]
    x = np.linspace(-1, 1, W)[None, :]
    top, bot = np.array(BG_TOP), np.array(BG_BOT)
    g = top[None, None, :] * (1 - y[..., None]) + bot[None, None, :] * y[..., None]
    # sıcak hale (ışık) üstte
    r = np.sqrt((x * 0.9) ** 2 + ((y - 0.32) * 1.6) ** 2)
    glow = np.clip(1 - r, 0, 1)[..., None] ** 2.2
    g = g + glow * np.array([38, 26, 6])
    return Image.fromarray(np.clip(g, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
BG = make_bg()
rng = np.random.default_rng(7)
GRAIN = [Image.fromarray((rng.normal(0, 7, (H // 2, W // 2)) + 128).clip(0, 255).astype(np.uint8), "L")
         .resize((W, H), Image.NEAREST) for _ in range(6)]

# ---------- sprite'lar ----------
def draw_bottle(d, s):
    # Klasik kolonya şişesi: omuzlu gövde, ince boyun, kapak, etiket
    cx = 210 * s
    body = [cx - 150 * s, 330 * s, cx + 150 * s, 820 * s]
    d.rounded_rectangle(body, radius=70 * s, fill=(198, 226, 214, 120), outline=(230, 245, 238, 230), width=5 * s)
    # sıvı
    d.rounded_rectangle([cx - 136 * s, 430 * s, cx + 136 * s, 806 * s], radius=58 * s, fill=(236, 214, 120, 150))
    d.rectangle([cx - 136 * s, 430 * s, cx + 136 * s, 446 * s], fill=(250, 236, 170, 200))
    # omuz + boyun
    d.polygon([(cx - 120 * s, 345 * s), (cx - 48 * s, 250 * s), (cx + 48 * s, 250 * s), (cx + 120 * s, 345 * s)],
              fill=(198, 226, 214, 110))
    d.rectangle([cx - 46 * s, 175 * s, cx + 46 * s, 262 * s], fill=(198, 226, 214, 130), outline=(230, 245, 238, 220), width=4 * s)
    # kapak
    d.rounded_rectangle([cx - 62 * s, 70 * s, cx + 62 * s, 185 * s], radius=16 * s, fill=AMBER)
    for i in range(5):
        xx = cx - 44 * s + i * 22 * s
        d.line([(xx, 82 * s), (xx, 174 * s)], fill=(200, 140, 40), width=4 * s)
    # etiket
    d.rounded_rectangle([cx - 112 * s, 520 * s, cx + 112 * s, 700 * s], radius=14 * s, fill=CREAM)
    d.ellipse([cx - 36 * s, 538 * s, cx + 36 * s, 600 * s], fill=(245, 205, 60))  # limon
    d.ellipse([cx + 14 * s, 546 * s, cx + 34 * s, 560 * s], fill=(110, 170, 80))  # yaprak
    lf = font(LORA, 34 * s, "Bold")
    d.text((cx, 650 * s), "KOLONYA", font=lf, fill=(30, 40, 50), anchor="mm")
    # parlama
    d.rounded_rectangle([cx - 118 * s, 380 * s, cx - 92 * s, 760 * s], radius=12 * s, fill=(255, 255, 255, 70))
BOTTLE = aa_layer(420, 860, draw_bottle)

def draw_cathedral(d, s):
    # Köln Katedrali'ni andıran ikiz gotik kuleli siluet
    c = (226, 214, 190, 255)
    base_y = 900 * s
    for cx in (210, 470):
        x = cx * s
        d.rectangle([x - 70 * s, 300 * s, x + 70 * s, base_y], fill=c)
        d.polygon([(x - 70 * s, 300 * s), (x, 0), (x + 70 * s, 300 * s)], fill=c)
        for k in range(4):  # pencereler
            yy = (380 + k * 120) * s
            d.rounded_rectangle([x - 22 * s, yy, x + 22 * s, yy + 80 * s], radius=22 * s, fill=(30, 44, 60))
    d.rectangle([280 * s, 520 * s, 400 * s, base_y], fill=c)
    d.polygon([(280 * s, 520 * s), (340 * s, 430 * s), (400 * s, 520 * s)], fill=c)
    d.rounded_rectangle([310 * s, 720 * s, 370 * s, base_y], radius=30 * s, fill=(30, 44, 60))
    d.ellipse([300 * s, 570 * s, 380 * s, 650 * s], outline=(30, 44, 60), width=8 * s)
    d.rectangle([60 * s, base_y - 6 * s, 620 * s, base_y + 10 * s], fill=c)
CATHEDRAL = aa_layer(680, 920, draw_cathedral)

def draw_rose(d, s):
    cx, cy = 200 * s, 200 * s
    for ring, (rad, n, col) in enumerate([(150, 7, (214, 96, 118)), (110, 6, (232, 122, 140)), (68, 5, (246, 156, 168))]):
        for i in range(n):
            a = 2 * math.pi * i / n + ring * 0.5
            px, py = cx + math.cos(a) * rad * 0.45 * s, cy + math.sin(a) * rad * 0.45 * s
            r = rad * 0.62 * s
            d.ellipse([px - r, py - r, px + r, py + r], fill=(*col, 235))
    d.ellipse([cx - 30 * s, cy - 30 * s, cx + 30 * s, cy + 30 * s], fill=(190, 70, 92))
ROSE_SPR = aa_layer(400, 400, draw_rose)

def draw_drop(d, s):
    d.polygon([(40 * s, 0), (8 * s, 70 * s), (72 * s, 70 * s)], fill=(250, 236, 170, 230))
    d.ellipse([4 * s, 40 * s, 76 * s, 112 * s], fill=(250, 236, 170, 230))
DROP = aa_layer(80, 116, draw_drop)

# ---------- altyazı ----------
def build_captions():
    caps = []
    for seg in SEGS:
        words = seg["caption"].split()
        keys = set(seg.get("key", []))
        # ≤3 kelime / ≤16 karakterlik parçalar
        chunks, cur = [], []
        for w in words:
            if cur and (len(cur) >= 3 or len(" ".join(cur + [w])) > 16):
                chunks.append(cur); cur = []
            cur.append(w)
            if w.endswith((".", "?", ":", "!")):
                chunks.append(cur); cur = []
        if cur: chunks.append(cur)
        total = sum(len(w) + 2 for w in words)
        t = seg["start"]; span = seg["end"] - seg["start"]
        for ch in chunks:
            ws = []
            for w in ch:
                dt = span * (len(w) + 2) / total
                ws.append({"w": w, "t0": t, "t1": t + dt, "key": w in keys}); t += dt
            caps.append({"t0": ws[0]["t0"], "t1": ws[-1]["t1"], "words": ws})
    for i in range(len(caps) - 1):  # boşlukta bir önceki parça ekranda kalsın
        caps[i]["show_until"] = caps[i + 1]["t0"]
    caps[-1]["show_until"] = caps[-1]["t1"] + 0.6
    return caps
CAPS = build_captions()

def draw_caption(frame, t):
    cur = next((c for c in CAPS if c["t0"] - 0.04 <= t < c["show_until"]), None)
    if not cur: return
    f = F_CAP(92)
    d = ImageDraw.Draw(frame)
    widths = [d.textlength(w["w"], font=f) for w in cur["words"]]
    gap = 26
    total = sum(widths) + gap * (len(widths) - 1)
    pop = ease((t - cur["t0"]) / 0.12)
    y = 1470 - 10 * (1 - pop)
    x = W / 2 - total / 2
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for w, wd in zip(cur["words"], widths):
        active = w["t0"] <= t < w["t1"] + 0.05
        col = AMBER if (w["key"] or active and False) else CREAM
        if active and not w["key"]: col = (255, 255, 255)
        a = 1.0 if t >= w["t0"] - 0.02 else 0.35
        ld.text((x, y), w["w"], font=f, fill=with_alpha(col, a * pop), anchor="lm",
                stroke_width=7, stroke_fill=(5, 10, 18, int(230 * pop)))
        if active:
            ld.rounded_rectangle([x, y + 58, x + wd, y + 66], radius=4, fill=with_alpha(AMBER, pop))
        x += wd + gap
    frame.alpha_composite(layer)

# ---------- sahneler ----------
def chrome(frame, t):
    d = ImageDraw.Draw(frame)
    # üst marka çubuğu
    d.text((W / 2, 150), f"{EP['series'].upper()}  ·  #{EP['episode']}", font=F_UI(34), fill=with_alpha(MUTED, 0.95), anchor="mm")
    # ilerleme çubuğu
    p = clamp(t / DUR)
    d.rounded_rectangle([90, 96, W - 90, 104], radius=4, fill=(255, 255, 255, 40))
    d.rounded_rectangle([90, 96, 90 + (W - 180) * p, 104], radius=4, fill=AMBER)

def sc_hook(f, lt, dur, t):
    a = ease(lt / 0.5)
    sway = math.sin(t * 1.6) * 2.2
    paste_center(f, BOTTLE, W / 2, 780 + 40 * (1 - a), scale=lerp(0.92, 1.05, ease_io(lt / dur)), alpha=a, rot=sway)

def sc_everyday(f, lt, dur, t):
    d = ImageDraw.Draw(f)
    items = ["Bayramda", "Otobüste", "Misafirlikte"]
    for i, w in enumerate(items):
        k = ease((lt - i * 0.55) / 0.35)
        y = 420 + i * 150
        d.text((W / 2 - 330 + 30 * (1 - k), y), "—", font=F_SERIF(64), fill=with_alpha(AMBER, k), anchor="lm")
        d.text((W / 2 - 250 + 30 * (1 - k), y), w, font=F_SERIF(84), fill=with_alpha(CREAM, k), anchor="lm")
    k = ease((lt - 1.9) / 0.4)
    paste_center(f, BOTTLE, W / 2, 1040, scale=0.55 + 0.05 * k, alpha=k)
    # damlalar
    for j in range(3):
        ph = (t * 0.9 + j / 3) % 1
        paste_center(f, DROP, W / 2 + (j - 1) * 70, lerp(1240, 1330, ph), scale=0.5, alpha=k * (1 - ph))

def sc_city(f, lt, dur, t):
    a = ease(lt / 0.6)
    paste_center(f, CATHEDRAL, W / 2, 760 + 60 * (1 - a), scale=0.95 + 0.04 * ease_io(lt / dur), alpha=a * 0.95)
    d = ImageDraw.Draw(f)
    k = ease((lt - 0.9) / 0.4)
    d.text((W / 2, 250), "ALMANYA", font=F_UI(40), fill=with_alpha(TEAL, k), anchor="mm")
    k2 = ease((lt - 1.3) / 0.35)
    fs = int(lerp(240, 200, k2))
    d.text((W / 2, 1290), "Köln", font=F_SERIF(fs), fill=with_alpha(AMBER, k2), anchor="mm",
           stroke_width=6, stroke_fill=(6, 12, 20, int(255 * k2)))

def sc_name(f, lt, dur, t):
    d = ImageDraw.Draw(f)
    k1 = ease(lt / 0.4)
    d.text((W / 2, 430), "Köln", font=F_SERIF(110), fill=with_alpha(CREAM, k1), anchor="mm")
    d.text((W / 2, 545), "Fransızca:", font=F_UI(40), fill=with_alpha(MUTED, k1), anchor="mm")
    d.text((W / 2, 660), "Cologne", font=F_SERIF_I(130), fill=with_alpha(AMBER, k1), anchor="mm")
    k2 = ease((lt - 2.0) / 0.45)
    d.line([(W / 2 - 220, 790), (W / 2 + 220, 790)], fill=with_alpha(MUTED, 0.5 * k2), width=3)
    d.text((W / 2, 900), "Eau de Cologne", font=F_SERIF_I(92), fill=with_alpha(CREAM, k2), anchor="mm")
    k3 = ease((lt - 3.2) / 0.4)
    bw = 560 * k3
    d.rounded_rectangle([W / 2 - bw / 2, 1010, W / 2 + bw / 2, 1150], radius=70, fill=with_alpha(AMBER, k3))
    if k3 > 0.6:
        d.text((W / 2, 1080), "= Köln suyu", font=F_SERIF(76), fill=with_alpha((20, 24, 30), (k3 - 0.6) / 0.4), anchor="mm")

def sc_farina(f, lt, dur, t):
    d = ImageDraw.Draw(f)
    k = ease_io(lt / 1.4)
    year = int(lerp(1650, 1709, k))
    d.text((W / 2, 520), str(year), font=F_SERIF(260), fill=AMBER, anchor="mm")
    k2 = ease((lt - 1.2) / 0.4)
    d.text((W / 2, 720), "Johann Maria Farina", font=F_SERIF(78), fill=with_alpha(CREAM, k2), anchor="mm")
    d.text((W / 2, 800), "İtalyan bir parfümcü", font=F_UI(40), fill=with_alpha(MUTED, k2), anchor="mm")
    k3 = ease((lt - 2.4) / 0.6)
    # İtalya -> Köln oku
    x0, x1 = W / 2 - 300, W / 2 + 300
    d.text((x0, 960), "İtalya", font=F_UI(48), fill=with_alpha(CREAM, k3), anchor="mm")
    d.text((x1, 960), "Köln", font=F_UI(48), fill=with_alpha(AMBER, k3), anchor="mm")
    xe = lerp(x0 + 110, x1 - 100, k3)
    d.line([(x0 + 110, 962), (xe, 962)], fill=with_alpha(AMBER, k3), width=6)
    if k3 > 0.95:
        d.polygon([(x1 - 100, 962), (x1 - 128, 946), (x1 - 128, 978)], fill=AMBER)
    k4 = ease((lt - 4.8) / 0.5)
    paste_center(f, BOTTLE, W / 2, 1210, scale=0.34, alpha=k4)

def sc_route(f, lt, dur, t):
    d = ImageDraw.Draw(f)
    # nokta ızgarası (soyut harita)
    for gx in range(120, W - 100, 60):
        for gy in range(380, 1180, 60):
            d.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=(255, 255, 255, 28))
    pts = {"Köln": (300, 520), "Paris": (230, 640), "Viyana": (560, 600), "İstanbul": (840, 1020)}
    a = ease(lt / 0.4)
    for name in ("Paris", "Viyana"):
        x, y = pts[name]; k = ease((lt - 0.6) / 0.4)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=with_alpha(MUTED, k))
        d.text((x + 22, y), name, font=F_UI(34), fill=with_alpha(MUTED, k), anchor="lm")
    x, y = pts["Köln"]
    d.ellipse([x - 14, y - 14, x + 14, y + 14], fill=with_alpha(AMBER, a))
    d.text((x + 26, y - 4), "Köln", font=F_UI(44), fill=with_alpha(CREAM, a), anchor="lm")
    d.text((W / 2, 300), "Avrupa sarayları", font=F_SERIF_I(60), fill=with_alpha(CREAM, ease((lt - 0.5) / 0.4)), anchor="mm")
    # Köln -> İstanbul kesik çizgi eğrisi
    k = ease_io((lt - 2.3) / 1.6)
    (x0, y0), (x2, y2) = pts["Köln"], pts["İstanbul"]
    cx, cy = 820, 560
    n = 60
    for i in range(int(n * k)):
        if i % 2: continue
        u0, u1 = i / n, (i + 1) / n
        p = lambda u: ((1 - u) ** 2 * x0 + 2 * (1 - u) * u * cx + u * u * x2, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * cy + u * u * y2)
        d.line([p(u0), p(u1)], fill=AMBER, width=7)
    if k > 0.98:
        kk = ease((lt - 3.9) / 0.4)
        r = 16 + 10 * kk
        d.ellipse([x2 - r, y2 - r, x2 + r, y2 + r], fill=with_alpha(AMBER, kk))
        d.text((x2, y2 + 70), "İstanbul", font=F_SERIF(66), fill=with_alpha(CREAM, kk), anchor="mm")
        d.text((x2, y2 + 130), "19. yüzyıl", font=F_UI(36), fill=with_alpha(MUTED, kk), anchor="mm")

def sc_rose(f, lt, dur, t):
    d = ImageDraw.Draw(f)
    k = ease(lt / 0.4)
    out = ease((lt - 1.0) / 0.6)
    paste_center(f, ROSE_SPR, W / 2 - 230 * out, 760, scale=lerp(1.0, 0.65, out), alpha=k * lerp(1, 0.45, out))
    d.text((W / 2 - 230 * out, 1010), "Gül suyu", font=F_SERIF(64), fill=with_alpha(ROSE, k * lerp(1, 0.6, out)), anchor="mm")
    if out > 0.2:
        cx = W / 2 - 230 * out
        d.line([(cx - 120, 1010), (cx + 120, 1010)], fill=with_alpha(CREAM, out), width=6)
    kb = ease((lt - 1.3) / 0.5)
    paste_center(f, BOTTLE, W / 2 + 240, 760 + 40 * (1 - kb), scale=0.5, alpha=kb)
    d.text((W / 2 + 240, 1010), "Kolonya", font=F_SERIF(64), fill=with_alpha(AMBER, kb), anchor="mm")
    ka = ease((lt - 1.6) / 0.3)
    d.text((W / 2 + 5, 770), "→", font=F_UI(80), fill=with_alpha(CREAM, ka), anchor="mm")

def sc_today(f, lt, dur, t):
    d = ImageDraw.Draw(f)
    k = ease_io(lt / 1.6)
    n = int(lerp(0, 317, k))
    d.text((W / 2, 520), f"{n}", font=F_SERIF(280), fill=AMBER, anchor="mm")
    d.text((W / 2, 700), "yıldır aynı tarif", font=F_SERIF_I(72), fill=with_alpha(CREAM, ease((lt - 1.0) / 0.4)), anchor="mm")
    k2 = ease((lt - 2.2) / 0.5)
    d.rounded_rectangle([W / 2 - 300, 820, W / 2 + 300, 940], radius=60, outline=with_alpha(TEAL, k2), width=4)
    d.text((W / 2, 880), "1709 → bugün", font=F_UI(50), fill=with_alpha(CREAM, k2), anchor="mm")
    k3 = ease((lt - 3.0) / 0.5)
    paste_center(f, BOTTLE, W / 2, 1180, scale=0.32, alpha=k3, rot=math.sin(t * 1.4) * 2)

def sc_outro(f, lt, dur, t):
    d = ImageDraw.Draw(f)
    k = ease(lt / 0.45)
    d.text((W / 2, 520), "Sıradaki?", font=F_SERIF(170), fill=with_alpha(AMBER, k), anchor="mm")
    k2 = ease((lt - 0.8) / 0.4)
    for i, w in enumerate(["Çay bardağı", "Simit", "Nazar boncuğu"]):
        kk = ease((lt - 0.8 - i * 0.25) / 0.35)
        y = 720 + i * 110
        d.rounded_rectangle([W / 2 - 280, y - 44, W / 2 + 280, y + 44], radius=44, outline=with_alpha(MUTED, 0.6 * kk), width=3)
        d.text((W / 2, y), w + "?", font=F_UI(46), fill=with_alpha(CREAM, kk), anchor="mm")
    k3 = ease((lt - 2.0) / 0.4)
    d.text((W / 2, 1110), "Yorumlara yaz", font=F_SERIF_I(64), fill=with_alpha(CREAM, k3), anchor="mm")
    bob = math.sin(t * 5) * 10
    d.polygon([(W / 2 - 26, 1180 + bob), (W / 2 + 26, 1180 + bob), (W / 2, 1215 + bob)], fill=with_alpha(AMBER, k3))

SCENES = {"hook": sc_hook, "everyday": sc_everyday, "city": sc_city, "name": sc_name, "farina": sc_farina,
          "route": sc_route, "rose": sc_rose, "today": sc_today, "outro": sc_outro}

# Sahne pencereleri: her sahne kendi seslendirmesinden hemen önce başlar, bir sonrakine kadar sürer
WIN = []
for i, s in enumerate(SEGS):
    st = 0.0 if i == 0 else s["start"] - 0.15
    en = SEGS[i + 1]["start"] - 0.15 if i + 1 < len(SEGS) else DUR
    WIN.append((st, en, s["scene"], i))

# ---------- gerçek fotoğraflar ----------
PHOTOS = {}
_img_json = os.path.join(build, "images.json")
if os.path.exists(_img_json):
    for k, v in json.load(open(_img_json, encoding="utf-8")).items():
        try:
            im = ImageOps.exif_transpose(Image.open(v["path"])).convert("RGB")
        except Exception as e:
            print("fotoğraf açılamadı:", v.get("path"), e); continue
        # ekranı kaplayacak şekilde ölçekle (+%12 hareket payı)
        sc = max(W * 1.12 / im.width, H * 1.12 / im.height)
        im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
        own = v.get("license") == "Kanalın kendi çekimi"
        PHOTOS[int(k)] = {"img": im, "credit": "" if own else f"Foto: {v['artist']} · {v['license']} · Wikimedia Commons"}

def make_shade():
    a = np.zeros((H, W), np.float32)
    y = np.arange(H)[:, None].astype(np.float32)
    a += np.clip((380 - y) / 380, 0, 1) * 0.55             # üst: marka çubuğu okunsun
    a += np.clip((y - 880) / 700, 0, 1) ** 1.2 * 0.88       # alt: başlık + altyazı okunsun
    a = np.clip(a + 0.12, 0, 0.92)
    out = np.zeros((H, W, 4), np.uint8); out[..., 3] = (a * 255).astype(np.uint8)
    out[..., :3] = (4, 8, 14)
    return Image.fromarray(out, "RGBA")
SHADE = make_shade()

def photo_for(seg_idx):
    """Sahnenin kendi fotoğrafı; yoksa en yakın sahnenin gerçek fotoğrafı (çizim yok)."""
    if seg_idx in PHOTOS: return seg_idx
    if not PHOTOS: return None
    return min(PHOTOS, key=lambda k: (abs(k - seg_idx), k > seg_idx))

def photo_scene(layer, seg_idx, lt, dur):
    p = PHOTOS[photo_for(seg_idx)]; im = p["img"]
    u = ease_io(lt / max(dur, 0.1))
    z = lerp(1.0, 1.07, u)                       # yavaş yakınlaştırma
    cw, ch = W / z, H / z
    span_x, span_y = im.width - cw, im.height - ch
    d = -1 if seg_idx % 2 else 1                 # sahneler sırayla sola/sağa kayar
    x = span_x * (0.5 + d * lerp(-0.45, 0.45, u))
    y = span_y * 0.45
    crop = im.crop((int(x), int(y), int(x + cw), int(y + ch))).resize((W, H), Image.BILINEAR)
    layer.paste(crop.convert("RGBA"), (0, 0))
    layer.alpha_composite(SHADE)
    seg = SEGS[seg_idx]
    d2 = ImageDraw.Draw(layer)
    k = ease((lt - 0.25) / 0.45)
    if seg.get("subtitle"):
        d2.text((W / 2, 1075 + 14 * (1 - k)), seg["subtitle"], font=F_UI(40), fill=with_alpha(AMBER, k), anchor="mm")
    if seg.get("title"):
        size = 150
        while size > 70 and d2.textlength(seg["title"], font=F_SERIF(size)) > W - 120: size -= 6
        d2.text((W / 2, 1195 + 24 * (1 - k)), seg["title"], font=F_SERIF(size), fill=with_alpha(CREAM, k), anchor="mm",
                stroke_width=3, stroke_fill=(4, 8, 14, int(200 * k)))
    if p["credit"]:
        d2.text((W / 2, 1868), p["credit"], font=F_UI(22), fill=with_alpha(CREAM, 0.55), anchor="mm")

def render_frame(t, idx):
    f = BG.copy()
    for st, en, name, si in WIN:
        if st <= t < en:
            lt = t - st
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            if photo_for(si) is not None:
                photo_scene(layer, si, lt, en - st)
            else:
                SCENES[name](layer, lt, en - st, t)
            fade = min(ease(lt / 0.22), ease((en - t) / 0.18))
            if fade < 1:
                a = layer.getchannel("A").point(lambda v: int(v * fade)); layer.putalpha(a)
            f.alpha_composite(layer)
    chrome(f, t)
    draw_caption(f, t)
    rgb = f.convert("RGB")
    # hafif film greni
    g = GRAIN[idx % len(GRAIN)]
    rgb = Image.blend(rgb, Image.merge("RGB", (g, g, g)), 0.035)
    return rgb

# ---------- müzik + efekt (kodla üretilir, telifsiz) ----------
def make_music(path, dur, sr=44100):
    n = int(dur * sr); t = np.arange(n) / sr
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G
    mus = np.zeros(n)
    bar = 3.2
    for b in range(int(dur / bar) + 1):
        notes = chords[b % 4]
        s0, s1 = int(b * bar * sr), int(min(dur, (b + 1) * bar + 0.6) * sr)
        if s0 >= n: break
        tt = t[s0:s1] - b * bar
        env = np.minimum(1, tt / 0.8) * np.exp(-np.maximum(0, tt - bar) * 3)
        for m in notes:
            fq = 440 * 2 ** ((m - 69) / 12)
            mus[s0:s1] += env * (np.sin(2 * np.pi * fq * tt) + 0.25 * np.sin(2 * np.pi * 2 * fq * tt)) * 0.06
        # pluck arpej
        for k, m in enumerate(notes + [notes[0] + 12]):
            p0 = s0 + int(k * bar / 4 * sr); ln = int(0.9 * sr)
            if p0 + ln > n: continue
            pt = np.arange(ln) / sr
            fq = 440 * 2 ** ((m + 12 - 69) / 12)
            mus[p0:p0 + ln] += np.sin(2 * np.pi * fq * pt) * np.exp(-pt * 5) * 0.05
    # sahne geçiş "whoosh"
    rng2 = np.random.default_rng(3)
    for st, en, name, _ in WIN[1:]:
        p0, ln = int(max(0, st - 0.1) * sr), int(0.35 * sr)
        if p0 + ln > n: continue
        noise = rng2.normal(0, 1, ln)
        noise = np.convolve(noise, np.ones(30) / 30, mode="same")
        env = np.sin(np.linspace(0, np.pi, ln)) ** 2
        mus[p0:p0 + ln] += noise * env * 0.12
    fade = np.minimum(1, np.minimum(t / 0.5, (dur - t) / 1.5))
    mus = np.clip(mus * fade, -1, 1)
    import wave
    with wave.open(path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((mus * 32767).astype(np.int16).tobytes())

def main():
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    music = os.path.join(build, "music.wav")
    make_music(music, DUR)
    silent = os.path.join(build, "video_silent.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                          "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
    nf = int(DUR * FPS)
    for i in range(nf):
        p.stdin.write(render_frame(i / FPS, i).tobytes())
        if i % 150 == 0: print(f"kare {i}/{nf}", flush=True)
    p.stdin.close(); p.wait()
    voice = os.path.join(build, "voice.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", voice, "-i", music,
                    "-filter_complex",
                    "[1:a]highpass=f=80,acompressor=threshold=-18dB:ratio=3,volume=1.6,asplit=2[v][vsc];"
                    "[2:a]volume=0.55[m];[m][vsc]sidechaincompress=threshold=0.03:ratio=6:release=300[md];"
                    "[v][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-ar", "44100", "-movflags", "+faststart", "-shortest", out_path], check=True)
    print("hazır:", out_path)

if __name__ == "__main__":
    if len(sys.argv) > 3 and sys.argv[3] == "--stills":
        for tt in [float(x) for x in sys.argv[4].split(",")]:
            render_frame(tt, 0).save(os.path.join(os.path.dirname(out_path), f"still_{tt:05.1f}.png"))
    else:
        main()
