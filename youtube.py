"""YouTube kanal işlemleri (YouTube Data API v3).

Kullanım:
  python3 youtube.py kontrol            -> kanalı sadece okur (ad, id, abone, açıklama)
  python3 youtube.py kanal              -> kanal.json'daki açıklama/anahtar kelime/kapak görselini uygular
Ortam: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN
Çıktı: out_yt/sonuc.txt
"""
import json, os, sys
import requests

OUT = "out_yt"; os.makedirs(OUT, exist_ok=True)
lines = []
def log(*a):
    s = " ".join(str(x) for x in a); print(s); lines.append(s)
def save():
    open(f"{OUT}/sonuc.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")

def env(name):
    raw = os.environ.get(name, "")
    v = raw.strip().strip('"').strip("'")
    return raw, v

def teshis():
    # Gizli değerleri GÖSTERMEDEN biçimlerini kontrol eder
    for n in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"):
        raw, v = env(n)
        bilgi = f"uzunluk={len(v)}"
        if raw != v: bilgi += " · baş/sonda boşluk/tırnak vardı (temizlendi)"
        if any(c.isspace() for c in v): bilgi += " · İÇİNDE BOŞLUK VAR"
        if n == "YT_CLIENT_ID": bilgi += " · sonu doğru" if v.endswith(".apps.googleusercontent.com") else " · SONU .apps.googleusercontent.com DEĞİL"
        if n == "YT_CLIENT_SECRET": bilgi += " · GOCSPX- ile başlıyor" if v.startswith("GOCSPX-") else " · GOCSPX- ile başlamıyor"
        if n == "YT_REFRESH_TOKEN":
            bilgi += " · 1// ile başlıyor (doğru tür)" if v.startswith("1//") else (" · ya29. ile başlıyor: BU ACCESS TOKEN, refresh token değil" if v.startswith("ya29.") else " · beklenmeyen başlangıç")
        log(f"  {n}: {bilgi}")

def token():
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": env("YT_CLIENT_ID")[1], "client_secret": env("YT_CLIENT_SECRET")[1],
        "refresh_token": env("YT_REFRESH_TOKEN")[1], "grant_type": "refresh_token"}, timeout=30)
    if r.status_code != 200:
        log("TOKEN HATASI", r.status_code, r.text[:500]); log("Teşhis:"); teshis(); save(); sys.exit(1)
    return r.json()["access_token"]

def api(method, path, tok, **kw):
    r = requests.request(method, "https://www.googleapis.com/youtube/v3/" + path,
                         headers={"Authorization": f"Bearer {tok}"}, timeout=60, **kw)
    if r.status_code >= 300:
        log("API HATASI", method, path, r.status_code, r.text[:800]); save(); sys.exit(1)
    return r.json()

def my_channel(tok):
    d = api("GET", "channels", tok, params={"part": "snippet,brandingSettings,statistics,status", "mine": "true"})
    items = d.get("items", [])
    if not items: log("Bu hesapta YouTube kanalı bulunamadı."); save(); sys.exit(1)
    if len(items) > 1: log("UYARI: birden fazla kanal döndü, ilki kullanılıyor")
    return items[0]

def show(ch):
    sn, st, br = ch["snippet"], ch.get("statistics", {}), ch.get("brandingSettings", {}).get("channel", {})
    log("Kanal adı:", sn.get("title"))
    log("Kanal id:", ch["id"], "· @", sn.get("customUrl", "-"))
    log("Abone:", st.get("subscriberCount", "?"), "· Video:", st.get("videoCount", "?"), "· İzlenme:", st.get("viewCount", "?"))
    log("Açıklama:", (br.get("description") or sn.get("description") or "(boş)")[:300])
    log("Anahtar kelimeler:", br.get("keywords", "(boş)"))
    log("Ülke:", br.get("country", "-"), "· Dil:", br.get("defaultLanguage", "-"))
    log("Kapak:", ch.get("brandingSettings", {}).get("image", {}).get("bannerExternalUrl", "(yok)"))

mode = sys.argv[1] if len(sys.argv) > 1 else "kontrol"
tok = token()
ch = my_channel(tok)
log("== ÖNCE ==" if mode == "kanal" else "== KANAL ==")
show(ch)

if mode == "videolar":
    up = api("GET", "channels", tok, params={"part": "contentDetails", "mine": "true"})["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    items = api("GET", "playlistItems", tok, params={"part": "contentDetails", "playlistId": up, "maxResults": 10}).get("items", [])
    ids = ",".join(i["contentDetails"]["videoId"] for i in items)
    log("== VİDEOLAR ==")
    if ids:
        for v in api("GET", "videos", tok, params={"part": "snippet,status,statistics,contentDetails", "id": ids}).get("items", []):
            sn, stt, sta = v["snippet"], v["status"], v.get("statistics", {})
            log(f"- {sn['title']}")
            log(f"  id={v['id']} · görünürlük={stt.get('privacyStatus')} · yükleme={stt.get('uploadStatus')} · süre={v['contentDetails'].get('duration')}")
            log(f"  izlenme={sta.get('viewCount','0')} · beğeni={sta.get('likeCount','0')} · yorum={sta.get('commentCount','0')} · çocuklar için={stt.get('madeForKids')}")
            log(f"  açıklama ilk satır: {sn.get('description','').splitlines()[0] if sn.get('description') else '(boş)'}")
            log(f"  açıklamada atıf var mı: {'Fotoğraflar' in sn.get('description','')}")
    else:
        log("Kanalda video bulunamadı.")

if mode == "kanal":
    cfg = json.load(open("kanal.json", encoding="utf-8"))
    branding = ch.get("brandingSettings", {})
    branding.setdefault("channel", {})
    branding["channel"]["description"] = cfg["aciklama"]
    branding["channel"]["keywords"] = " ".join(f'"{k}"' if " " in k else k for k in cfg["anahtar_kelimeler"])
    branding["channel"]["country"] = cfg.get("ulke", "TR")
    branding["channel"]["defaultLanguage"] = cfg.get("dil", "tr")
    if cfg.get("kapak"):
        with open(cfg["kapak"], "rb") as f:
            r = requests.post("https://www.googleapis.com/upload/youtube/v3/channelBanners/insert",
                              params={"uploadType": "media"}, data=f.read(),
                              headers={"Authorization": f"Bearer {tok}", "Content-Type": "image/png"}, timeout=120)
        if r.status_code >= 300:
            log("KAPAK YÜKLEME HATASI", r.status_code, r.text[:600])
        else:
            branding.setdefault("image", {})["bannerExternalUrl"] = r.json()["url"]
            log("Kapak görseli yüklendi.")
    api("PUT", "channels", tok, params={"part": "brandingSettings"},
        json={"id": ch["id"], "brandingSettings": branding})
    log("== SONRA ==")
    show(my_channel(tok))
save()
