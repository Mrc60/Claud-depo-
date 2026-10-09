"""Gerçek fotoğraflar: Wikimedia Commons'tan, sadece serbest lisanslı görseller.

Her segmentteki "image" alanı için:
  {"file": "File:Tam_dosya_adı.jpg"}  -> o dosyayı birebir indirir (en güvenli yol)
  {"query": "arama terimi"}           -> aramadaki ilk uygun fotoğrafı seçer
Sonuç: build/<bölüm>/img_XX.jpg + images.json (kaynak/lisans bilgisi)
       + credits.txt (YouTube açıklamasına eklenecek atıf satırları)
Kullanım: python3 images.py episodes/001_kolonya.json build/001
"""
import json, os, re, sys, time
import requests

API = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "SiradanDegilShorts/1.0 (YouTube Shorts kanalı; atıf açıklamada)"}
ALLOWED = re.compile(r"^(public domain|pd|cc0|cc[ -]by(-sa)?([ -]\d\.\d)?|cc[ -]by(-sa)? \d\.\d)", re.I)
MIN_W = 900

def api(**params):
    params.update(format="json", formatversion=2)
    for attempt in range(4):
        r = requests.get(API, params=params, headers=HEADERS, timeout=30)
        if r.status_code == 200: return r.json()
        time.sleep(2 ** attempt)
    r.raise_for_status()

def info(titles):
    d = api(action="query", prop="imageinfo", titles="|".join(titles),
            iiprop="url|size|mime|extmetadata", iiurlwidth=1600)
    return d.get("query", {}).get("pages", [])

def strip_html(s): return re.sub(r"<[^>]+>", "", s or "").strip()

def usable(p):
    ii = (p.get("imageinfo") or [{}])[0]
    if ii.get("mime") not in ("image/jpeg", "image/png"): return None
    if ii.get("width", 0) < MIN_W: return None
    meta = ii.get("extmetadata", {})
    lic = strip_html(meta.get("LicenseShortName", {}).get("value"))
    if not ALLOWED.match(lic): return None
    return {"title": p["title"], "url": ii.get("thumburl") or ii["url"], "page": ii.get("descriptionurl"),
            "license": lic, "artist": strip_html(meta.get("Artist", {}).get("value"))[:80] or "Bilinmiyor"}

def find(spec):
    if "file" in spec:
        pages = info([spec["file"]])
        return usable(pages[0]) if pages else None
    d = api(action="query", list="search", srsearch=spec["query"] + " filetype:bitmap",
            srnamespace=6, srlimit=15)
    titles = [h["title"] for h in d.get("query", {}).get("search", [])]
    if not titles: return None
    by_title = {p["title"]: p for p in info(titles)}
    for t in titles:  # arama sırasını koru
        u = usable(by_title.get(t, {}))
        if u: return u
    return None

ep = json.load(open(sys.argv[1], encoding="utf-8"))
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
result, credits = {}, []
for i, seg in enumerate(ep["segments"]):
    spec = seg.get("image")
    if not spec: continue
    hit = find(spec)
    if not hit:
        print(f"  seg {i}: uygun fotoğraf bulunamadı ({spec}) -> çizim kullanılacak")
        continue
    path = os.path.join(out, f"img_{i:02d}.jpg")
    img = requests.get(hit["url"], headers=HEADERS, timeout=60)
    img.raise_for_status()
    open(path, "wb").write(img.content)
    hit["path"] = path
    result[str(i)] = hit
    credits.append(f"{hit['title'].replace('File:', '')} — {hit['artist']} ({hit['license']}) {hit['page']}")
    print(f"  seg {i}: {hit['title']} [{hit['license']}]")
json.dump(result, open(os.path.join(out, "images.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(os.path.join(out, "credits.txt"), "w", encoding="utf-8").write(
    "Fotoğraflar (Wikimedia Commons):\n" + "\n".join("- " + c for c in credits) + "\n")
print(f"Fotoğraflar tamam: {len(result)} adet")
