"""Günlük istatistik: Zernio API'den son 28 günün gönderi sayıları + takipçiler.
Çıktı: out_ist/gunluk/YYYY-MM-DD.json, out_ist/ozet.md (platform ve konu özeti).
Anahtar: ortam değişkeni ZERNIO_API_KEY (GitHub secret). Anahtar dosyaya yazılmaz."""
import os, json, time, datetime, urllib.request, urllib.parse, glob
KEY = os.environ.get("ZERNIO_API_KEY", "")
BASE = "https://zernio.com/api/v1"
def get(path, **q):
    url = BASE + path + ("?" + urllib.parse.urlencode(q) if q else "")
    for t in range(4):
        try:
            r = urllib.request.Request(url, headers={"Authorization": "Bearer " + KEY, "User-Agent": "SiradanDegilStats/1.0"})
            return json.loads(urllib.request.urlopen(r, timeout=90).read())
        except Exception as e:
            print("tekrar", path, str(e)[:80]); time.sleep(10 * (t + 1))
    return {}
bugun = datetime.date.today(); bas = bugun - datetime.timedelta(days=28)
posts, page = [], 1
while page < 20:
    d = get("/analytics", fromDate=str(bas), toDate=str(bugun), limit=100, page=page)
    p = d.get("posts", [])
    posts += p
    if len(p) < 100: break
    page += 1; time.sleep(1)
alan = ["views", "reach", "likes", "comments", "shares", "saves", "follows", "completionRate", "igReelsAvgWatchTime", "engagementRate"]
kayit = []
for p in posts:
    a = p.get("analytics") or {}
    kayit.append(dict(platform=p.get("platform"), hesap=p.get("accountId") or (p.get("platforms") or [{}])[0].get("accountId"),
        tarih=p.get("publishedAt"), metin=(p.get("content") or "")[:70].replace("\n", " "), url=p.get("platformPostUrl"),
        **{k: a.get(k) for k in alan}))
tk = get("/accounts/follower-stats", fromDate=str(bas), granularity="daily")
takip = {a.get("platform") + ":" + (a.get("username") or ""): a.get("currentFollowers") for a in tk.get("accounts", [])}
os.makedirs("out_ist/gunluk", exist_ok=True)
json.dump(dict(tarih=str(bugun), takipci=takip, gonderiler=kayit), open(f"out_ist/gunluk/{bugun}.json", "w"), ensure_ascii=False, indent=0)
# özet
L = [f"# İstatistik özeti ({bugun}, son 28 gün)", "", "## Takipçi", ""]
L += [f"- {k}: {v}" for k, v in sorted(takip.items())]
for pl in sorted({k["platform"] for k in kayit if k["platform"]}):
    ks = sorted([k for k in kayit if k["platform"] == pl], key=lambda k: -(k["views"] or 0))
    top = sum(k["views"] or 0 for k in ks)
    L += ["", f"## {pl}: {len(ks)} gönderi, toplam {top:,} görüntüleme".replace(",", "."), "", "| Tarih | Görüntüleme | Beğeni | Paylaşım | Takip | Metin |", "|---|---|---|---|---|---|"]
    for k in ks[:15]:
        L.append(f"| {(k['tarih'] or '')[:10]} | {k['views'] or 0} | {k['likes'] or 0} | {k['shares'] or 0} | {k['follows'] or 0} | {k['metin'][:45]} |")
open("out_ist/ozet.md", "w").write("\n".join(L) + "\n")
print("gönderi:", len(kayit), "takip:", takip)
