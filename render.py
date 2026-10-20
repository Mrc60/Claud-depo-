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
        # her kelimenin zamanı: soru sonrası duraklama varsa her parça kendi süresine dağıtılır
        parts = seg.get("bolumler") or [{"start": seg["start"], "end": seg["end"], "n": len(words)}]
        if sum(p["n"] for p in parts) != len(words):
            parts = [{"start": seg["start"], "end": seg["end"], "n": len(words)}]
        times, k = [], 0
        for p in parts:
            pw = words[k:k + p["n"]]; k += p["n"]
            total = sum(len(w) + 2 for w in pw) or 1
            t = p["start"]; span = p["end"] - p["start"]
            for w in pw:
                dt = span * (len(w) + 2) / total
                times.append((t, t + dt)); t += dt
        k = 0
        for ch in chunks:
            ws = []
            for w in ch:
                t0, t1 = times[k]; k += 1
                ws.append({"w": w, "t0": t0, "t1": t1, "key": w in keys})
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
_WM = None
def chrome(frame, t):
    d = ImageDraw.Draw(frame)
    # üst marka çubuğu
    # hareketli marka şeridi: kenarda dikey yazı, aşağıdan yukarı yavaşça yürür; her geçişte sol/sağ kenar değişir
    global _WM
    txt = f"{EP['series'].upper()}  ·  #{EP['episode']}"
    if "_WM" not in globals() or _WM is None:
        f = F_UI(30); bb = f.getbbox(txt); tw, th = bb[2] + 8, bb[3] + 8
        spr = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        ImageDraw.Draw(spr).text((4, 4), txt, font=f, fill=(255, 255, 255, 95), stroke_width=2, stroke_fill=(0, 0, 0, 55))
        _WM = spr.rotate(90, expand=True)
    PERIYOT = 24.0
    u = (t % PERIYOT) / PERIYOT
    cy = lerp(H - 260, 260, u)
    sol = int(t // PERIYOT) % 2 == 0
    cx = 58 if sol else W - 58
    frame.alpha_composite(_WM, (int(cx - _WM.width / 2), int(cy - _WM.height / 2)))
    # İlerleme çubuğu kullanılmıyor (TEK1'in tercihi: hiçbir videoda olmasın)

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
        W2, H2 = int(W * 1.12), int(H * 1.12)
        spec = (SEGS[int(k)].get("image") or {}) if int(k) < len(SEGS) else {}
        if spec.get("kirp"):  # [x0, y0, x1, y1] oran olarak: gravürün kâğıt kenarını/yazısını kes
            x0, y0, x1, y1 = spec["kirp"]
            im = im.crop((int(im.width * x0), int(im.height * y0), int(im.width * x1), int(im.height * y1)))
        if spec.get("fit") == "tam":
            # Fotoğrafın tamamı görünsün: arkada bulanık kopya, önde net ve kırpılmamış fotoğraf
            sc = max(W2 / im.width, H2 / im.height)
            bg = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
            bg = bg.crop(((bg.width - W2) // 2, (bg.height - H2) // 2, (bg.width - W2) // 2 + W2, (bg.height - H2) // 2 + H2))
            bg = bg.filter(ImageFilter.GaussianBlur(40))
            bg = Image.blend(bg, Image.new("RGB", bg.size, (6, 10, 16)), 0.45)
            fw = int(W2 * 0.96); fh = int(im.height * fw / im.width)
            max_h = int(H2 * 0.58)  # dikey fotoğraflar da üstten/alttan kesilmesin
            if fh > max_h:
                fh = max_h; fw = int(im.width * fh / im.height)
            fg = im.resize((fw, fh), Image.LANCZOS)
            bg.paste(fg, ((W2 - fw) // 2, max(int(H2 * 0.09), int(H2 * 0.36 - fh / 2))))
            im = bg
        else:
            # ekranı kaplayacak şekilde ölçekle (+%12 hareket payı)
            sc = max(W2 / im.width, H2 / im.height)
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
    z = lerp(1.0, 1.056, u)                       # yavaş yakınlaştırma
    cw, ch = W / z, H / z
    span_x, span_y = im.width - cw, im.height - ch
    d = -1 if seg_idx % 2 else 1                 # sahneler sırayla sola/sağa kayar
    x = span_x * (0.5 + d * lerp(-0.36, 0.36, u))
    y = span_y * 0.45
    # alt piksel hassas kırpma: tam sayıya yuvarlama her karede 1 px oynayıp titreme yapıyordu
    crop = im.resize((W, H), Image.BICUBIC, box=(x, y, x + cw, y + ch))
    layer.paste(crop.convert("RGBA"), (0, 0))
    layer.alpha_composite(SHADE)
    seg = SEGS[seg_idx]
    d2 = ImageDraw.Draw(layer)
    k = 1.0 if seg_idx == 0 else ease((lt - 0.25) / 0.45)  # açılış başlığı ilk kareden ekranda
    if seg.get("subtitle"):
        sy = 1075 + 14 * (1 - k)
        bx = d2.textbbox((W / 2, sy), seg["subtitle"], font=F_UI(40), anchor="mm")
        d2.rounded_rectangle([bx[0] - 22, bx[1] - 14, bx[2] + 22, bx[3] + 14], radius=14,
                             fill=(10, 12, 16, int(200 * k)))   # açık renkli fotoğraf üstünde okunabilsin
        d2.text((W / 2, sy), seg["subtitle"], font=F_UI(40), fill=with_alpha(AMBER, k), anchor="mm")
    if seg.get("title"):
        size = 150
        while size > 70 and d2.textlength(seg["title"], font=F_SERIF(size)) > W - 120: size -= 6
        d2.text((W / 2, 1195 + 24 * (1 - k)), seg["title"], font=F_SERIF(size), fill=with_alpha(CREAM, k), anchor="mm",
                stroke_width=3, stroke_fill=(4, 8, 14, int(200 * k)))
    # Fotoğraf atıfları videoda gösterilmez; YouTube açıklamasında yer alır.

# ---------- hareketli grafikler (gerçek fotoğrafın üstünde) ----------
def _txt(layer, xy, txt, font=None, fill=(255, 255, 255, 255), anchor="mm"):
    if len(fill) == 4 and fill[3] <= 2: return
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ov).text(xy, txt, font=font, fill=fill, anchor=anchor)
    layer.alpha_composite(ov)

def _card(layer, box, a):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ov).rounded_rectangle(box, radius=48, fill=(6, 11, 18, int(205 * a)),
                                         outline=with_alpha(AMBER, 0.35 * a), width=3)
    layer.alpha_composite(ov)

def _person(d, cx, cy, r, fill, a):
    d.ellipse([cx - r * 0.42, cy - r * 0.95, cx + r * 0.42, cy - r * 0.11], fill=with_alpha(fill, a))
    d.pieslice([cx - r * 0.8, cy - r * 0.05, cx + r * 0.8, cy + r * 1.45], 180, 360, fill=with_alpha(fill, a))

def anim_bolusme(layer, spec, lt, dur):
    """Bir araba, koltuklar tek tek dolar, ücret çubuğu yolcu sayısına bölünür."""
    a = ease(lt / 0.5)
    _card(layer, [70, 250, W - 70, 1010], a)
    d = ImageDraw.Draw(layer)
    n = int(spec.get("kisi", 4))
    _txt(layer, (W / 2, 330), spec.get("ust", "AYNI YÖNE GİDEN YOLCULAR"), font=F_UI(40), fill=with_alpha(AMBER, a), anchor="mm")
    # araba (sade çizgi ikon)
    cx, cy = W / 2, 560
    bw, bh = 760, 200
    lw = 9
    col = with_alpha(CREAM, a)
    d.rounded_rectangle([cx - bw / 2, cy - bh / 2 + 40, cx + bw / 2, cy + bh / 2 + 40], radius=60, outline=col, width=lw)
    d.rounded_rectangle([cx - bw * 0.30, cy - bh / 2 - 80, cx + bw * 0.30, cy - bh / 2 + 52], radius=50, outline=col, width=lw)
    for wx in (cx - bw * 0.30, cx + bw * 0.30):
        d.ellipse([wx - 62, cy + bh / 2 + 2, wx + 62, cy + bh / 2 + 126], fill=(6, 11, 18, int(255 * a)), outline=col, width=lw)
    # yolcular sırayla biner
    xs = [cx - bw * 0.33 + i * (bw * 0.66) / max(1, n - 1) for i in range(n)]
    t0 = 0.7; step = min(0.55, max(0.3, (dur * 0.45) / n))
    for i, x in enumerate(xs):
        k = ease((lt - t0 - i * step) / 0.25)
        _person(d, x, cy + 12 + 30 * (1 - k), 58, AMBER if k > 0.5 else MUTED, max(0.25 * a, k))
    # ücret çubuğu
    fill_t = t0 + n * step + 0.2
    kb = ease((lt - fill_t) / 0.35)
    bx0, bx1, by = 150, W - 150, 830
    _txt(layer, (W / 2, by - 50), spec.get("cubuk", "TAKSİ ÜCRETİ"), font=F_UI(38), fill=with_alpha(MUTED, a), anchor="mm")
    if kb < 1:
        d.rounded_rectangle([bx0, by, bx1, by + 70], radius=20, fill=with_alpha(CREAM, a * 0.9))
    gap = 24 * kb
    seg_w = (bx1 - bx0 - gap * (n - 1)) / n
    if kb > 0:
        for i in range(n):
            x0 = bx0 + i * (seg_w + gap)
            d.rounded_rectangle([x0, by, x0 + seg_w, by + 70], radius=20, fill=with_alpha(AMBER, a))
            _txt(layer, (x0 + seg_w / 2, by + 35), f"1/{n}", font=F_CAP(40), fill=(6, 11, 18, int(255 * kb)), anchor="mm")
    ke = ease((lt - fill_t - 0.6) / 0.4)
    if spec.get("alt"):
        _txt(layer, (W / 2, 960), spec["alt"], font=F_SERIF(64), fill=with_alpha(CREAM, ke), anchor="mm")

def anim_zaman(layer, spec, lt, dur):
    """Dikey zaman çizelgesi: çizgi aşağı doğru çizilir, noktalar sırayla belirir."""
    a = ease(lt / 0.5)
    items = spec.get("maddeler", [])
    _card(layer, [70, 250, W - 70, 1060], a)
    d = ImageDraw.Draw(layer)
    x, y0, y1 = 210, 340, 980
    n = max(1, len(items))
    ys = [y0 + i * (y1 - y0) / max(1, n - 1) for i in range(n)]
    per = max(0.6, (dur - 1.2) / n)
    prog = clamp((lt - 0.3) / (per * n))
    d.line([x, y0, x, y0 + (y1 - y0) * ease_io(prog)], fill=with_alpha(AMBER, a), width=8)
    for i, (it, y) in enumerate(zip(items, ys)):
        k = ease((lt - 0.3 - i * per) / 0.35)
        if k <= 0: continue
        cur = i == min(n - 1, int((lt - 0.3) / per))
        r = 22 + (8 if cur else 0)
        d.ellipse([x - r, y - r, x + r, y + r], fill=with_alpha(AMBER if cur else CREAM, k),
                  outline=(6, 11, 18, int(255 * k)), width=5)
        _txt(layer, (x + 70 + 30 * (1 - k), y - 28), it.get("yil", ""), font=F_SERIF(70), fill=with_alpha(AMBER, k), anchor="lm")
        _txt(layer, (x + 72 + 30 * (1 - k), y + 36), it.get("yazi", ""), font=F_UI(44), fill=with_alpha(CREAM, k), anchor="lm")

def anim_hafta(layer, spec, lt, dur):
    """Haftanın günleri listesi: önceki sahnelerde açılanlar sönük durur, bu sahnenin günleri sırayla parlar."""
    a = ease(lt / 0.4)
    gunler = spec.get("gunler", [])
    aktif = spec.get("aktif", [])          # bu sahnede açılan satırlar
    acik = spec.get("acik", 0)             # daha önce açılmış satır sayısı (sönük gösterilir)
    _card(layer, [70, 250, W - 70, 1070], a)
    d = ImageDraw.Draw(layer)
    y0, row = 320, 110
    per = max(0.5, (dur - 0.6) / max(1, len(aktif)))
    for i, g in enumerate(gunler):
        y = y0 + i * row
        if i in aktif:
            j = aktif.index(i)
            k = ease((lt - 0.25 - j * per) / 0.35)
            hl = k
        elif (i in acik if isinstance(acik, list) else i < acik):
            k, hl = 1.0, 0.0
        else:
            k, hl = 0.0, 0.0
        # gün adı her zaman görünür (sönük); anlamı açılınca gelir
        base = 0.35 + 0.65 * hl
        if hl > 0.01:
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(ov).rounded_rectangle([100, y - 48, W - 100, y + 48], radius=24,
                                                 fill=with_alpha(AMBER, 0.16 * hl * a))
            layer.alpha_composite(ov)
        _txt(layer, (130, y), g[0], font=F_SERIF(62), fill=with_alpha(AMBER if hl > 0.5 else CREAM, base * a), anchor="lm")
        if k > 0.01:
            _txt(layer, (W - 130 - 20 * (1 - k), y), g[1], font=F_UI(38),
                 fill=with_alpha(CREAM, (0.55 + 0.45 * hl) * k * a), anchor="rm")

def anim_takvim(layer, spec, lt, dur):
    """1917 takvim atlaması. tur2="ok": 15 ŞUBAT -> 1 MART; tur2="izgara": Şubat'ın 16-28 tarihleri tek tek üstü çizilir."""
    a = ease(lt / 0.45)
    _card(layer, [70, 250, W - 70, 1010], a)
    d = ImageDraw.Draw(layer)
    RED = (226, 84, 70)
    _txt(layer, (W / 2, 320), spec.get("ust", "RUMİ TAKVİM · 1917"), font=F_UI(40), fill=with_alpha(AMBER, a), anchor="mm")
    if spec.get("tur2") == "ok":
        k1 = ease((lt - 0.3) / 0.4); k2 = ease((lt - 1.3) / 0.5)
        for cx, top, alt, k in ((W / 2 - 220, "15", "ŞUBAT", k1), (W / 2 + 220, "1", "MART", k2)):
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
            od.rounded_rectangle([cx - 170, 430, cx + 170, 820], radius=30, fill=with_alpha(CREAM, 0.95 * k))
            od.rectangle([cx - 170, 430, cx + 170, 520], fill=with_alpha(RED, k))
            layer.alpha_composite(ov)
            _txt(layer, (cx, 475), alt, font=F_UI(48), fill=(255, 255, 255, int(255 * k)), anchor="mm")
            _txt(layer, (cx, 670), top, font=F_SERIF(190), fill=(10, 14, 20, int(255 * k)), anchor="mm")
        ka = ease((lt - 0.9) / 0.4)
        if ka > 0:
            x0, x1 = W / 2 - 40, W / 2 - 40 + 80 * ka
            d.line([x0, 625, x1, 625], fill=with_alpha(AMBER, ka), width=12)
            if ka > 0.9: d.polygon([(x1 + 30, 625), (x1 - 4, 600), (x1 - 4, 650)], fill=with_alpha(AMBER, ka))
        ke = ease((lt - 2.0) / 0.4)
        _txt(layer, (W / 2, 920), spec.get("alt", "ERTESİ GÜN"), font=F_SERIF(64), fill=with_alpha(CREAM, ke), anchor="mm")
        return
    # izgara: Şubat 1-28
    cols, x0, y0, cw, rh = 7, 150, 420, (W - 300) / 7, 120
    _txt(layer, (W / 2, 375), "ŞUBAT", font=F_UI(44), fill=with_alpha(CREAM, a), anchor="mm")
    per = max(0.12, (dur * 0.6) / 13)
    for n in range(1, 29):
        i = n - 1; cx = x0 + (i % cols + 0.5) * cw; cy = y0 + (i // cols + 0.5) * rh
        if n < 16:
            _txt(layer, (cx, cy), str(n), font=F_SERIF(64), fill=with_alpha(CREAM, a), anchor="mm")
        else:
            k = ease((lt - 0.5 - (n - 16) * per) / 0.25)
            _txt(layer, (cx, cy), str(n), font=F_SERIF(64), fill=with_alpha(CREAM, a * (1 - 0.7 * k)), anchor="mm")
            if k > 0:
                d.line([cx - 42, cy + 30, cx - 42 + 84 * k, cy - 30], fill=with_alpha(RED, k), width=9)
    ke = ease((lt - 0.5 - 13 * per - 0.2) / 0.4)
    _txt(layer, (W / 2, 930), spec.get("alt", "13 TARİH ATLANDI"), font=F_SERIF(70), fill=with_alpha(AMBER, ke), anchor="mm")

def anim_kart(layer, spec, lt, dur):
    """Bilgi kartı: fotoğrafı kapatmasın diye alt bölümde, içeriğe göre boyutlanan kompakt kart.
    Küçük üst yazı, büyük başlık, maddeler sırayla belirir."""
    a = ease(lt / 0.45)
    items = spec.get("maddeler", [])
    h = 215 + (len(items) * 72 + 25 if items else 0)
    bottom = 1290; top = bottom - h
    _card(layer, [60, top, W - 60, bottom], a)
    _txt(layer, (W / 2, top + 48), spec.get("ust", ""), font=F_UI(38), fill=with_alpha(AMBER, a), anchor="mm")
    kb = ease((lt - 0.25) / 0.45)
    bas = spec.get("baslik", "")
    size = 112
    d = ImageDraw.Draw(layer)
    while size > 60 and d.textlength(bas, font=F_SERIF(size)) > W - 200: size -= 6
    _txt(layer, (W / 2, top + 140 + 16 * (1 - kb)), bas, font=F_SERIF(size), fill=with_alpha(CREAM, kb), anchor="mm")
    t0 = float(spec.get("bekle", 0.9)); per = max(0.35, (dur - t0 - 0.6) / max(1, len(items)))
    for i, it in enumerate(items):
        k = ease((lt - t0 - i * per) / 0.35)
        if k <= 0: continue
        y = top + 250 + i * 72
        d.ellipse([170 - 11, y - 11, 170 + 11, y + 11], fill=with_alpha(AMBER, k))
        _txt(layer, (205 + 20 * (1 - k), y), it, font=F_UI(48), fill=with_alpha(CREAM, k), anchor="lm")

def anim_rota(layer, spec, lt, dur):
    """İstanbul -> Pire şematik rota: yol çizilir, gemi noktası ilerler, sefer sayacı artar."""
    a = ease(lt / 0.45)
    _card(layer, [70, 250, W - 70, 1010], a)
    d = ImageDraw.Draw(layer)
    _txt(layer, (W / 2, 320), spec.get("ust", ""), font=F_UI(40), fill=with_alpha(AMBER, a), anchor="mm")
    A, B = (790, 450), (300, 800)   # İstanbul (kuzeydoğu), Pire (güneybatı) - şematik, ölçeksiz
    C = (720, 760)                  # Ege'ye doğru kavis
    def pt(u):
        return ((1-u)**2*A[0] + 2*(1-u)*u*C[0] + u**2*B[0], (1-u)**2*A[1] + 2*(1-u)*u*C[1] + u**2*B[1])
    n = int(spec.get("sayac", 1))
    span = max(0.25, (dur - 0.9) / n)
    tt = max(0.0, lt - 0.3)
    k_i = min(n - 1, int(tt / span)); u = clamp((tt - k_i * span) / (span * 0.85))
    if n == 1: u = clamp(tt / max(0.6, dur - 1.0))
    steps = 60
    for j in range(steps):
        u0, u1 = j / steps, (j + 0.5) / steps
        col = with_alpha(CREAM, 0.25 * a) if u1 > u else with_alpha(AMBER, a)
        d.line([pt(u0), pt(u1)], fill=col, width=7)
    for (x, y), ad, anc in ((A, spec.get("bas", "İSTANBUL"), "rm"), (B, spec.get("son", "PİRE"), "rm")):
        d.ellipse([x - 20, y - 20, x + 20, y + 20], fill=with_alpha(CREAM, a), outline=(6, 11, 18, int(255 * a)), width=5)
        _txt(layer, (x + (40 if anc == "lm" else -40), y), ad, font=F_UI(46), fill=with_alpha(CREAM, a), anchor=anc)
    x, y = pt(u)
    d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=with_alpha(AMBER, a))
    if n > 1:
        son = tt >= n * span
        _txt(layer, (W / 2, 920), f"{n} SEFER" if son else f"{k_i + 1}. SEFER", font=F_SERIF(78), fill=with_alpha(AMBER, a), anchor="mm")
    elif spec.get("alt"):
        ke = ease((lt - 0.8) / 0.4)
        _txt(layer, (W / 2, 920), spec["alt"], font=F_SERIF(70), fill=with_alpha(AMBER, ke), anchor="mm")

ANIMS = {"bolusme": anim_bolusme, "zaman": anim_zaman, "hafta": anim_hafta, "takvim": anim_takvim, "kart": anim_kart, "rota": anim_rota}

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
            an = SEGS[si].get("anim")
            if an and an.get("tur") in ANIMS:
                ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))  # ayrı katman: yarı saydam yazılar delik açmasın
                ANIMS[an["tur"]](ov, an, lt, en - st)
                layer.alpha_composite(ov)
            fade = min(1.0 if st == 0 else ease(lt / 0.22), ease((en - t) / 0.18))  # ilk kare siyah olmasın
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
