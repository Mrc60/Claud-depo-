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
HEADERS = {"User-Agent": "SiradanDegilShorts/1.0 (https://github.com/Mrc60/Claud-depo-; YouTube Shorts, credits in description)"}
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

def clean_artist(a):
    a = re.sub(r"\s+", " ", a or "").strip()
    if not a or re.fullmatch(r"(?i)(unknown author\s*)+|unknown|anonymous", a): return "Bilinmeyen fotoğrafçı"
    a = re.sub(r"(?i)(unknown author)(\s*unknown author)+", r"\1", a)
    return a[:80]

def usable(p):
    ii = (p.get("imageinfo") or [{}])[0]
    if ii.get("mime") not in ("image/jpeg", "image/png"): return None
    if ii.get("width", 0) < MIN_W: return None
    meta = ii.get("extmetadata", {})
    lic = strip_html(meta.get("LicenseShortName", {}).get("value"))
    if not ALLOWED.match(lic): return None
    return {"title": p["title"], "url": ii["url"], "page": ii.get("descriptionurl"),
            "license": lic, "artist": clean_artist(strip_html(meta.get("Artist", {}).get("value")))}

USED = set()

def search(q):
    d = api(action="query", list="search", srsearch=q + " filetype:bitmap", srnamespace=6, srlimit=20)
    titles = [h["title"] for h in d.get("query", {}).get("search", []) if h["title"] not in USED]
    if not titles: return None
    by_title = {p["title"]: p for p in info(titles)}
    for t in titles:  # arama sırasını koru
        u = usable(by_title.get(t, {}))
        if u: return u
    return None

def find(spec):
    if "file" in spec:
        pages = info([spec["file"]])
        return usable(pages[0]) if pages else None
    for q in spec.get("queries") or [spec["query"]]:  # sırayla dene, ilk uygun olanı al
        u = search(q)
        if u: return u
    return None

ep = json.load(open(sys.argv[1], encoding="utf-8"))
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
result, credits = {}, []
for i, seg in enumerate(ep["segments"]):
    spec = seg.get("image")
    if not spec: continue
    # Kanalın kendi çekimi (assets/ klasörü) her zaman önceliklidir
    local = spec.get("local")
    if local and os.path.exists(local):
        path = os.path.join(out, f"img_{i:02d}" + os.path.splitext(local)[1].lower())
        open(path, "wb").write(open(local, "rb").read())
        result[str(i)] = {"title": local, "path": path, "license": "Kanalın kendi çekimi", "artist": "Sıradan Değil", "page": ""}
        print(f"  seg {i}: kendi çekimimiz {local}")
        continue
    try:
        hit = find(spec)
    except Exception as e:
        print(f"  seg {i}: arama hatası ({e}) -> başka sahnenin fotoğrafı kullanılacak")
        hit = None
    if not hit:
        print(f"  seg {i}: uygun fotoğraf bulunamadı ({spec}) -> başka sahnenin fotoğrafı kullanılacak")
        continue
    path = os.path.join(out, f"img_{i:02d}.jpg")
    try:
        img = requests.get(hit["url"], headers=HEADERS, timeout=60)
        img.raise_for_status()
    except Exception as e:
        print(f"  seg {i}: indirme hatası ({e}) -> başka sahnenin fotoğrafı kullanılacak")
        continue
    open(path, "wb").write(img.content)
    USED.add(hit["title"])
    hit["path"] = path
    result[str(i)] = hit
    credits.append(f"{hit['title'].replace('File:', '')} — {hit['artist']} ({hit['license']}) {hit['page']}")
    print(f"  seg {i}: {hit['title']} [{hit['license']}]")
json.dump(result, open(os.path.join(out, "images.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(os.path.join(out, "credits.txt"), "w", encoding="utf-8").write(
    "Fotoğraflar (Wikimedia Commons):\n" + "\n".join("- " + c for c in credits) + "\n")
print(f"Fotoğraflar tamam: {len(result)} adet")
