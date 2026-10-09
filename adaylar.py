"""Görsel araştırma: her sorgu için Wikimedia Commons'tan aday fotoğrafları toplar,
numaralı küçük resim panoları (contact sheet) üretir. Doğru fotoğraf elle seçilir.

Girdi:  aday_sorgular.json  {"bolum": "...", "sorgular": ["...", ...]}
Çıktı:  out_adaylar/pano_XX.jpg  + adaylar.json (numara -> tam dosya adı, lisans)
"""
import io, json, os, re, time
import requests
from PIL import Image, ImageDraw, ImageFont

API = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "SiradanDegilShorts/1.0 (https://github.com/Mrc60/Claud-depo-; image research)"}
ALLOWED = re.compile(r"^(public domain|pd|cc0|cc[ -]by(-sa)?([ -]\d\.\d)?|cc[ -]by(-sa)? \d\.\d)", re.I)
OUT = "out_adaylar"
os.makedirs(OUT, exist_ok=True)
FONT = ImageFont.truetype("fonts/Inter-SemiBold.otf", 18)
FONT_B = ImageFont.truetype("fonts/InterDisplay-Black.otf", 34)

def api(**p):
    p.update(format="json", formatversion=2)
    for a in range(4):
        try:
            r = requests.get(API, params=p, headers=HEADERS, timeout=30)
            if r.status_code == 200: return r.json()
        except Exception: pass
        time.sleep(2 ** a)
    return {}

def strip(s): return re.sub(r"<[^>]+>", "", s or "").strip()

cfg = json.load(open("aday_sorgular.json", encoding="utf-8"))
seen, cands = set(), []
for q in cfg["sorgular"]:
    d = api(action="query", list="search", srsearch=q + " filetype:bitmap", srnamespace=6, srlimit=12)
    titles = [h["title"] for h in d.get("query", {}).get("search", []) if h["title"] not in seen]
    if not titles: print("sonuç yok:", q); continue
    pages = api(action="query", prop="imageinfo", titles="|".join(titles),
                iiprop="url|size|mime|extmetadata", iiurlwidth=320).get("query", {}).get("pages", [])
    for p in pages:
        ii = (p.get("imageinfo") or [{}])[0]
        lic = strip(ii.get("extmetadata", {}).get("LicenseShortName", {}).get("value"))
        if ii.get("mime") not in ("image/jpeg", "image/png") or ii.get("width", 0) < 800 or not ALLOWED.match(lic):
            continue
        seen.add(p["title"])
        cands.append({"no": len(cands) + 1, "q": q, "title": p["title"], "thumb": ii.get("thumburl"),
                      "license": lic, "w": ii.get("width"), "h": ii.get("height")})
    print(f"{q}: toplam aday {len(cands)}")

# 4x3 panolar
TW, TH, COLS, ROWS = 320, 300, 4, 3
for start in range(0, len(cands), COLS * ROWS):
    grp = cands[start:start + COLS * ROWS]
    sheet = Image.new("RGB", (COLS * TW, ROWS * (TH + 50)), (25, 25, 25))
    d = ImageDraw.Draw(sheet)
    for k, c in enumerate(grp):
        x, y = (k % COLS) * TW, (k // COLS) * (TH + 50)
        try:
            im = Image.open(io.BytesIO(requests.get(c["thumb"], headers=HEADERS, timeout=30).content)).convert("RGB")
            im.thumbnail((TW - 8, TH - 8)); sheet.paste(im, (x + (TW - im.width) // 2, y + (TH - im.height) // 2))
        except Exception:
            d.text((x + 10, y + 10), "indirilemedi", font=FONT, fill="red")
        d.rectangle([x + 4, y + 4, x + 70, y + 46], fill=(240, 180, 60))
        d.text((x + 10, y + 6), str(c["no"]), font=FONT_B, fill=(0, 0, 0))
        d.text((x + 6, y + TH + 4), c["title"].replace("File:", "")[:34], font=FONT, fill=(230, 230, 230))
        d.text((x + 6, y + TH + 26), c["q"][:34], font=FONT, fill=(140, 160, 180))
    sheet.save(f"{OUT}/pano_{start // (COLS * ROWS) + 1:02d}.jpg", quality=85)
json.dump(cands, open(f"{OUT}/adaylar.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("pano sayısı:", (len(cands) + COLS * ROWS - 1) // (COLS * ROWS))
