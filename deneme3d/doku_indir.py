"""Dünya dokusunu (NASA Blue Marble, kamu malı) Wikimedia Commons'tan indirir, lisansı yazdırır."""
import requests, re, sys
API = "https://commons.wikimedia.org/w/api.php"
H = {"User-Agent": "SiradanDegilShorts/1.0 (https://github.com/Mrc60/Claud-depo-)"}
ADAY = ["File:Land shallow topo 8192.tif", "File:Land shallow topo 2048.jpg", "File:Whole world - land and oceans.jpg"]
for t in ADAY:
    r = requests.get(API, params=dict(action="query", format="json", formatversion=2, prop="imageinfo", titles=t,
                     iiprop="url|extmetadata|size", iiurlwidth=8192), headers=H, timeout=60).json()
    p = r["query"]["pages"][0]
    if "imageinfo" not in p: print("yok:", t); continue
    ii = p["imageinfo"][0]; em = ii.get("extmetadata", {})
    lic = re.sub("<[^>]+>", "", em.get("LicenseShortName", {}).get("value", ""))
    art = re.sub("<[^>]+>", "", em.get("Artist", {}).get("value", ""))[:100]
    print("seçildi:", t, "|", lic, "|", art, "|", ii["width"], "x", ii["height"], "|", ii["descriptionurl"])
    if not re.match(r"(public domain|pd|cc0)", lic, re.I): print("lisans uygun değil, atlandı"); continue
    url = ii.get("thumburl") or ii["url"]
    open(sys.argv[1], "wb").write(requests.get(url, headers=H, timeout=180).content)
    open(sys.argv[1] + ".kunye.txt", "w").write(f"{t} | {lic} | {art} | {ii['descriptionurl']}\n")
    sys.exit(0)
sys.exit("HATA: doku bulunamadı")
