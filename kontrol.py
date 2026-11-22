#!/usr/bin/env python3
"""Sıradan Değil teslim öncesi kontrol (iki hesap için ortak).

Kullanım:
  python3 kontrol.py metin  senaryo.txt          # ElevenLabs metni
  python3 kontrol.py bolum  episodes/NNN_x.json   # bölüm JSON'u (görsel, süre)
  python3 kontrol.py set    set.txt               # yükleme seti
  python3 kontrol.py gorsel a.jpg b.jpg ...       # aday/kapak görseli: eski görsellerle aynı fotoğraf mı
  python3 kontrol.py video  episodes/NNN_x.json NNN_x.mp4   # üretilen video: kare panosu + kenarlık/koyuluk

Yükleme seti dosya biçimi: her alan "=== AD ===" satırıyla başlar. Adlar:
  YT_BASLIK, YT_ACIKLAMA, YT_ETIKET, YT_SABIT, TT_ACIKLAMA, TT_SABIT,
  FBIG_ACIKLAMA (Facebook, 4 etiket), IG_ACIKLAMA (Instagram, 5 etiket), FBIG_SABIT, X_ACIKLAMA

HATA = teslim etme, düzelt. UYARI = TEK1'e bir cümleyle bildir.
Süre 75 sn'yi geçerse sadece UYARI (TEK1 bazen bilerek uzun istiyor).
"""
import glob
import hashlib
import json
import os
import re
import sys

KOK = os.path.dirname(os.path.abspath(__file__))
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⬀-⯿️‍]")
ETIKETLER = {"serious", "thoughtful", "calm", "sad", "short pause", "long pause", "laughs"}  # laughs: TEK1 izni 13.11.2026
# TEK1 kararı 13.11.2026: kapanış kısaltıldı
SON_CUMLE = "Kaynaklar video açıklamasında. Beğenmeyi ve takip etmeyi lütfen unutmayalım."
CAGRI = re.compile(r"\b(beğen\w*|paylaş\w*|etiketle\w*|takip et\w*)", re.I)
LINK = re.compile(r"(https?://|www\.|\.com\b|\.gov\b|\.org\b)", re.I)

hatalar, uyarilar = [], []


def hata(m):
    hatalar.append(m)


def uyari(m):
    uyarilar.append(m)


def kesme_isareti(metin, yer):
    # Türkçe ek ayrımı: Harf + ' + küçük harf (Çanakkale'ye)
    for m in re.finditer(r"\w+['’]\w+", metin):
        hata(f"{yer}: kesme işareti var ({m.group()}); ek bitişik yazılmalı")


# Ekranda okunan yazı (altyazı, açılış) ve açıklamalar doğru Türkçe yazılır:
# sayıya ve özel ada gelen ek kesmeyle ayrılır (1936'ya, Lozan'da).
# Bitişik yazım SADECE ElevenLabs ses metni (say / senaryo) içindir. (12.11.2026)
EK = r"(?:[ıiuü]n(?:da|de|ta|te|dan|den|tan|ten)|d[ae]n?|t[ae]n?|[yn]?[ıiuüae]|l[ae]r\w*|l[ıiuü]\w*|nc[ıiuü]\w*)"
SAYI_EK = re.compile(r"\b\d+" + EK + r"\b")
OZEL_EK = re.compile(r"(?<=[a-zçğıöşü,] )([A-ZÇĞİÖŞÜ][a-zçğıöşü]{2,}(?<!st)(?<!l[ae]r)(?:d[ae]n?|t[ae]n?|y[ae]|[ıiuü]n))\b")


def kesme_eksik(metin, yer):
    duz = re.sub(r"#\w+", " ", metin)
    for m in SAYI_EK.finditer(duz):
        hata(f"{yer}: sayıya gelen ek kesmesiz ({m.group()}); doğrusu örn. 1936'ya")
    for m in OZEL_EK.finditer(duz):
        w = m.group(1)
        if re.search(r"(stan|iye|ye|l[ae]r\w*)$", w):  # Yunanistan, Türkiye, Rumların: kök/çoğul, atla
            continue
        uyari(f"{yer}: özel ada ek kesmesiz olabilir ({m.group(1)}); özel adsa örn. Lozan'da")


# ---------------- METİN ----------------
def metin_kontrol(yol):
    t = open(yol, encoding="utf-8").read()
    for et in re.findall(r"\[([^\]]+)\]", t):
        if et.strip().lower() not in ETIKETLER:
            hata(f"izinsiz ElevenLabs etiketi: [{et}]")
    kesme_isareti(t, "metin")
    for m in re.finditer(r"\?(?!\s*\[short pause\])", t):
        hata(f"sorudan sonra [short pause] yok: ...{t[max(0, m.start()-40):m.start()+1]}")
    duz = re.sub(r"\[[^\]]+\]", " ", t)
    ilk = duz.strip().split("\n")[0]
    if re.match(r"\s*\d{3,4}", ilk):
        hata("metin tarihle açılıyor")
    if re.search(r"\bölü\b|\bölüler", duz, re.I):
        uyari("'ölü' geçiyor; şehit ise 'şehit' yaz")
    for k in ("ilk ", "icat"):
        if k in duz.lower():
            uyari(f"'{k.strip()}' geçiyor: güçlü kanıt var mı?")
    if "Düşüncelerinizi yorumlarda paylaşın" not in duz:
        uyari("kapanışta yorum daveti yok")
    if SON_CUMLE not in duz:
        hata("sabit son cümle yok ya da farklı yazılmış")
    if "dede" in duz.lower():
        uyari("'dede' çerçevesi geçiyor (her videoda kullanma)")
    kelime = len(duz.split())
    sn = kelime / 1.7  # gerçek ElevenLabs hızı (061: 174 kelime = 101,7 sn), 03.11.2026
    print(f"kelime: {kelime}, tahmini süre: {sn:.0f} sn")
    if sn > 75:
        uyari(f"tahmini süre {sn:.0f} sn (75 üstü; TEK1 isterse sorun değil)")


# ---------------- GÖRSEL BENZERLİĞİ (15.11.2026, #90 hatası) ----------------
# Aynı fotoğraf başka adla / başka kırpımla indirilince md5 ve ad kontrolü yakalamıyordu
# (#68, #87, #90). Burada resmin kendisi karşılaştırılır (ORB özellik eşleşmesi + RANSAC).
# Skor = ortak nokta sayısı. Ölçüm: aynı fotoğraf 139-675; farklı fotoğraf ~10, aynı kitap çerçevesindeki farklı fotoğraf 41 (yanlış alarm, bu yüzden HATA 60).
BENZER_HATA, BENZER_UYARI = 60, 20


def _cv():
    try:
        import cv2  # noqa
        return cv2
    except Exception:
        hata("görsel benzerlik kontrolü çalışmadı: OpenCV yok. Kur: pip install --break-system-packages opencv-python-headless")
        return None


def _ozellik(cv2, yol, orb):
    im = cv2.imread(yol, cv2.IMREAD_GRAYSCALE)
    if im is None:
        return None
    s = 600 / max(im.shape)
    if s < 1:
        im = cv2.resize(im, None, fx=s, fy=s)
    return orb.detectAndCompute(im, None)


def _skor(cv2, a, b, bf):
    import numpy as np
    if not a or not b or a[1] is None or b[1] is None or len(a[0]) < 10 or len(b[0]) < 10:
        return 0
    m = bf.knnMatch(a[1], b[1], k=2)
    g = [x[0] for x in m if len(x) == 2 and x[0].distance < 0.75 * x[1].distance]
    if len(g) < 12:
        return 0
    src = np.float32([a[0][x.queryIdx].pt for x in g])
    dst = np.float32([b[0][x.trainIdx].pt for x in g])
    _, mask = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
    return int(mask.sum()) if mask is not None else 0


def benzerlik_kontrol(yeni, haric_onek=None, etiket=None):
    """yeni: [(etiket, yol)]. Her biri assets/belgeler'deki TÜM eski görsellerle ve birbirleriyle karşılaştırılır."""
    cv2 = _cv()
    if not cv2:
        return
    orb = cv2.ORB_create(1000)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    yeni_yollar = {os.path.abspath(y) for _, y in yeni}
    eski = {}
    # assets/onizleme: yerel kopyası olmayan eski bölüm görsellerinin küçük önizlemeleri (oniz_NNN_*.jpg)
    adaylar = glob.glob(os.path.join(KOK, "assets", "belgeler", "*")) + glob.glob(os.path.join(KOK, "assets", "onizleme", "*"))
    for p in adaylar:
        if not p.lower().endswith((".jpg", ".jpeg", ".png")) or os.path.abspath(p) in yeni_yollar:
            continue
        b = os.path.basename(p)
        if haric_onek and (b.startswith(haric_onek) or b.startswith("oniz_" + haric_onek)):
            continue
        f = _ozellik(cv2, p, orb)
        if f:
            eski[p] = f
    yf = [(e, y, _ozellik(cv2, y, orb)) for e, y in yeni]
    for e, y, f in yf:
        en = max(((_skor(cv2, f, g, bf), p) for p, g in eski.items()), default=(0, ""))
        if en[0] >= BENZER_HATA:
            hata(f"{e}: ESKİ GÖRSELLE AYNI FOTOĞRAF -> {os.path.relpath(en[1], KOK)} (skor {en[0]})")
        elif en[0] >= BENZER_UYARI:
            uyari(f"{e}: eski görsele benziyor -> {os.path.relpath(en[1], KOK)} (skor {en[0]}), panoda gözle bak")
    for i in range(len(yf)):
        for j in range(i + 1, len(yf)):
            if os.path.abspath(yf[i][1]) == os.path.abspath(yf[j][1]):
                continue
            s = _skor(cv2, yf[i][2], yf[j][2], bf)
            if s >= BENZER_HATA:
                hata(f"{yf[i][0]} ve {yf[j][0]}: aynı fotoğraf (skor {s}), videoda tek kez olsun")
    print(f"görsel benzerliği: {len(yf)} görsel, {len(eski)} eski görselle karşılaştırıldı")


def ad_kontrol(segs, no):
    """Commons dosya adı ve LCCN numarası başka bölümde / DIZIN'de geçiyor mu."""
    metin = ""
    for f in glob.glob(os.path.join(KOK, "episodes", "*.json")):
        if os.path.basename(f)[:3] != no:
            metin += open(f, encoding="utf-8").read()
    dz = os.path.join(KOK, "DIZIN.md")
    for i, s in enumerate(segs, 1):
        img = s.get("image") or {}
        alan = " ".join(str(img.get(k, "")) for k in ("file", "kaynak", "baslik", "commons")) + " " + str(s.get("file", ""))
        for lccn in set(re.findall(r"LCCN\s?\d{8,}", alan)):
            if lccn.replace(" ", "") in metin.replace(" ", ""):
                hata(f"sahne {i}: {lccn} başka bölümde kullanılmış")
        for fn in set(re.findall(r"File:[^\"|]+?\.(?:jpg|jpeg|png|tif)", alan, re.I)):
            if fn in metin:
                hata(f"sahne {i}: {fn[:70]} başka bölümde kullanılmış")



# ---------------- GÖRSELİN İÇİ (22.11.2026, TEK1: "eklenecekleri hepsini ekle, hata istemiyorum") ----------------
# Bu denetimler dosya adına/ayara değil, görüntünün kendisine bakar.
# KENARLIK: #111'de banknotu ortaya koyup üstü/altı gri bulanık doldurulunca FB "Videonda kenarlık var" dedi
# (4. kez). Ölçüm (Laplace kenar şiddeti, 270x480): bulanık/düz bant 0-1,1; gerçek fotoğraf kenarı 5-100.
# Belge kenarına konan beyaz pay da bant sayılır (0,0). Düşük ayrıntılı fotoğrafta yanlış alarm olmasın diye eşik
# min(2,5, orta*0,25). 1263 eski görselde denendi: #51/#54 banknot kolajları, #75-#87 belge payları yakalandı.
# RENKLİ: sepya (ton 5-25) sayılmaz; doygun ve sepya dışı piksel oranı >%5 ise renkli (#80 dia fotoğrafları %18-21).
# KOYU: ortalama parlaklık <60 uyarı, açılış sahnesinde <70 HATA ("açılış karesi asla koyu görünmesin").
YAZI_KELIME = re.compile(r"gazete|\bbelge|tutanak|resm[iî] gazete|kanun|ferman|mektup|sayfa|manşet|ilan|dilekçe|kimlik|tezkere|nüfus", re.I)
LISANS_YASAK = re.compile(r"\bSALT\b|SALT Araştırma|\bCC[- ]?BY[- ]?NC|\bCC[- ]?BY[- ]?ND|-NC\b|-ND\b|\bNC-|\bND-|non-?commercial|no ?deriv|blogspot|wordpress|\bblog\b|\bforum\b|tarihtarih|arastiralim", re.I)


def _bolge(cv2, yol, kirp=None):
    """Render'ın ekranda göstereceği 9:16 bölgeyi yaklaşık verir (kirp + ortadan 9:16)."""
    im = cv2.imread(yol, cv2.IMREAD_COLOR)
    if im is None:
        return None
    h, w = im.shape[:2]
    if kirp:
        x0, y0, x1, y1 = kirp
        im = im[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)]
        h, w = im.shape[:2]
    if w / h > 9 / 16:
        nw = int(h * 9 / 16); x = (w - nw) // 2; im = im[:, x:x + nw]
    else:
        nh = int(w * 16 / 9); y = (h - nh) // 2; im = im[y:y + nh]
    return cv2.resize(im, (270, 480), interpolation=cv2.INTER_AREA)


def kenar_bant(cv2, im):
    """Bulanık/düz kenar bandı (letterbox, çerçeve) var mı: (var_mı, ölçümler)."""
    import numpy as np
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    L = np.abs(cv2.Laplacian(g, cv2.CV_32F))
    m = {"ust": float(L[:48].mean()), "alt": float(L[-48:].mean()), "sol": float(L[:, :24].mean()),
         "sag": float(L[:, -24:].mean()), "orta": float(L[120:360, 40:230].mean())}
    e = min(2.5, 0.25 * m["orta"])
    var = (m["ust"] < e and m["alt"] < e) or (m["sol"] < e and m["sag"] < e)
    return var, m


def renk_orani(cv2, im):
    h = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    H, S, V = h[..., 0], h[..., 1], h[..., 2]
    renkli = (S > 70) & (V > 50) & ~((H >= 5) & (H <= 25))
    return float(renkli.mean()) * 100


def parlaklik(cv2, im):
    return float(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).mean())


def yazi_yogunlugu(cv2, im):
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    return float((cv2.Canny(g, 80, 200) > 0).mean()) * 100


def icerik_kontrol(i, yol, img, seg):
    cv2 = _cv()
    if not cv2:
        return
    im = _bolge(cv2, yol, img.get("kirp"))
    if im is None:
        hata(f"sahne {i}: görsel açılamadı ({yol})")
        return
    var, m = kenar_bant(cv2, im)
    if var:
        hata(f"sahne {i}: KENARLIK/BULANIK BANT var (üst {m['ust']:.1f}, alt {m['alt']:.1f}, sol {m['sol']:.1f}, sağ {m['sag']:.1f}; "
             f"orta {m['orta']:.1f}). FB 'kenarlık' der. Görsel 9:16'yı kendisi doldursun ya da keskin fotoğrafın üstüne kart (≤%66) olsun")
    r = renk_orani(cv2, im)
    if r > 5:
        hata(f"sahne {i}: RENKLİ görsel (renkli piksel %{r:.0f}). Siyah-beyaz ara; yoksa TEK1'e sor, onay gelirse image.onay.renkli yaz")
    b = parlaklik(cv2, im)
    if i == 1 and b < 70:
        hata(f"sahne 1 (açılış): görsel koyu (parlaklık {b:.0f}/255); açılış karesi koyu olmaz")
    elif b < 60:
        uyari(f"sahne {i}: görsel koyu (parlaklık {b:.0f}/255), karede bak")
    hiz = img.get("hiz", 1.0)
    metin = " ".join(str(img.get(k, "")) for k in ("baslik", "kaynak")) + " " + os.path.basename(str(img.get("local", "")))
    if YAZI_KELIME.search(metin) and (hiz or 0) > 0:
        hata(f"sahne {i}: yazılı belge/gazete görünüyor ama kamera hareketli (hiz {hiz}); yazı titrer, hiz 0 ver")
    elif yazi_yogunlugu(cv2, im) > 22 and (hiz or 0) > 0.6:
        uyari(f"sahne {i}: çok ayrıntılı/yazılı görsel, hiz {hiz} titreyebilir; karede bak")
    lis = " ".join(str(img.get(k, "")) for k in ("lisans", "kaynak", "sayfa", "baslik"))
    mm = LISANS_YASAK.search(lis)
    if mm:
        hata(f"sahne {i}: lisans/kaynak yasak listede ('{mm.group()}'): SALT, NC/ND, blog/forum kullanılmaz")
    if not str(seg.get("gorunen", "")).strip():
        hata(f"sahne {i}: 'gorunen' alanı boş. Sahnede ne göründüğünü yaz ve altyazıyla eşleştir (ses-görsel uyumu)")


ONAY_ESLES = {
    "tekrar": ("bölümünde kullanılmış", "ESKİ GÖRSELLE AYNI", "başka bölümde"),
    "renkli": ("RENKLİ",),
    "benzer": ("aynı fotoğraf (skor",),
    "sure": ("ekranda (<4,5",),
}


def onay_uygula(segs):
    """TEK1'in onayladığı istisnalar: image.onay = {"tekrar": "TEK1 21.11", ...}. KENARLIK onaylanamaz."""
    global hatalar
    kalan = []
    for h_ in hatalar:
        sahneler = [int(x) for x in re.findall(r"sahne (\d+)", h_)]
        tasindi = False
        for tur, kaliplar in ONAY_ESLES.items():
            if not any(k in h_ for k in kaliplar) or not sahneler:
                continue
            onaylar = [((segs[n - 1].get("image") or {}).get("onay") or {}).get(tur) if 0 < n <= len(segs) else None for n in sahneler]
            if all(onaylar):
                uyarilar.append(f"{h_}  [TEK1 onaylı: {onaylar[0]}]")
                tasindi = True
                break
        if not tasindi:
            kalan.append(h_)
    hatalar[:] = kalan


# ---------------- BÖLÜM ----------------
def md5(yol):
    return hashlib.md5(open(yol, "rb").read()).hexdigest()


def bolum_kontrol(yol):
    d = json.load(open(yol, encoding="utf-8"))
    no = os.path.basename(yol)[:3]
    if not d.get("acilis"):
        hata("'acilis' (ilk 3 sn merak yazısı) yok")
    kesme_eksik(d.get("acilis", ""), "açılış yazısı")
    segs = d.get("segments", [])
    kes = (d.get("dis_ses") or {}).get("kesimler") or []
    if kes:
        son = kes[-1][-1][1]
        print(f"ses süresi: {son:.1f} sn, sahne: {len(segs)}")
        if son > 75:
            uyari(f"süre {son:.1f} sn (75 üstü; TEK1 isterse sorun değil)")
        if len(kes) != len(segs):
            hata(f"kesim sayısı ({len(kes)}) sahne sayısıyla ({len(segs)}) uyuşmuyor")
        for i, k in enumerate(kes, 1):
            sure = sum(b - a for a, b in k)
            if sure < 4.5:  # TEK1 kararı 15.11.2026: görsel ~5 sn, daha kısası çok hızlı
                hata(f"sahne {i}: görsel {sure:.1f} sn ekranda (<4,5 sn; hedef 5 sn, sahneyi birleştir)")
            elif sure > 7:
                uyari(f"sahne {i}: görsel {sure:.1f} sn ekranda (hedef 5 sn, ikinci görsel ekle)")
    if segs and re.match(r"\s*\d{3,4}", segs[0].get("say", "")):
        hata("ilk sahne tarihle açılıyor")

    # diğer bölümlerin görselleri (md5 + ad)
    diger = {}
    for f in glob.glob(os.path.join(KOK, "episodes", "*.json")):
        if os.path.basename(f)[:3] == no:
            continue
        try:
            e = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for s in e.get("segments", []):
            loc = (s.get("image") or {}).get("local")
            p = os.path.join(KOK, loc) if loc else None
            if p and os.path.exists(p):
                diger.setdefault(md5(p), os.path.basename(f)[:3])

    gorulen = {}
    try:
        from PIL import Image
    except Exception:
        Image = None
    for i, s in enumerate(segs, 1):
        kesme_isareti(s.get("say", ""), f"sahne {i} say")
        kesme_eksik(s.get("caption", ""), f"sahne {i} altyazı")
        img = s.get("image") or {}
        loc = img.get("local")
        if not loc:
            hata(f"sahne {i}: görsel yok")
            continue
        p = os.path.join(KOK, loc)
        if not os.path.exists(p):
            hata(f"sahne {i}: dosya yok ({loc})")
            continue
        h = md5(p)
        if h in gorulen:
            hata(f"sahne {i}: görsel sahne {gorulen[h]} ile aynı (tekli olsun)")
        gorulen.setdefault(h, i)
        if h in diger:
            hata(f"sahne {i}: görsel #{diger[h]} bölümünde kullanılmış ({loc})")
        if img.get("fit") != "doldur":
            hata(f"sahne {i}: fit 'doldur' değil (küçük pencere olur)")
        if not (img.get("kaynak") or img.get("baslik")):
            uyari(f"sahne {i}: künye/kaynak boş")
        if Image:
            try:
                w, hgt = Image.open(p).size
                if w < 720:
                    uyari(f"sahne {i}: görsel küçük ({w}x{hgt}), bulanık görünebilir")
            except Exception:
                pass
        if "atatürk" in (img.get("baslik", "") + img.get("kaynak", "")).lower():
            uyari(f"sahne {i}: Atatürk görseli (az kullan)")
        icerik_kontrol(i, p, img, s)
    ad_kontrol(segs, no)
    yeni = [(f"sahne {i}", os.path.join(KOK, (s.get("image") or {}).get("local")))
            for i, s in enumerate(segs, 1)
            if (s.get("image") or {}).get("local") and os.path.exists(os.path.join(KOK, s["image"]["local"]))]
    benzerlik_kontrol(yeni, haric_onek=no + "_")
    onay_uygula(segs)


# ---------------- YÜKLEME SETİ ----------------
def set_kontrol(yol):
    t = open(yol, encoding="utf-8").read()
    alan = {}
    for m in re.finditer(r"^===\s*(\w+)\s*===\s*\n(.*?)(?=^===|\Z)", t, re.M | re.S):
        alan[m.group(1).upper()] = m.group(2).strip()
    gerekli = ["YT_BASLIK", "YT_ACIKLAMA", "YT_ETIKET", "YT_SABIT",
               "TT_ACIKLAMA", "TT_SABIT", "FBIG_ACIKLAMA", "IG_ACIKLAMA", "FBIG_SABIT", "X_ACIKLAMA"]
    for g in gerekli:
        if not alan.get(g):
            hata(f"{g} eksik (set tek seferde eksiksiz verilir)")
    for ad, v in alan.items():
        sabit = ad.endswith("_SABIT")
        if ad != "YT_ETIKET":
            kesme_eksik(v, ad)
        if not sabit and EMOJI.search(v):
            hata(f"{ad}: emoji var (sadece sabit yorumda serbest)")
        if "·" in v:
            hata(f"{ad}: '·' işareti var")
        if sabit:
            if v.count("?") != 1:
                hata(f"{ad}: tek soru olmalı ('?' sayısı {v.count('?')})")
            if LINK.search(v) or "kaynak" in v.lower():
                hata(f"{ad}: sabit yorumda kaynak/link olmaz")
            if len(v) > 120:
                uyari(f"{ad}: sabit yorum uzun ({len(v)} karakter)")
        if ad in ("TT_ACIKLAMA", "FBIG_ACIKLAMA", "IG_ACIKLAMA", "X_ACIKLAMA"):
            if LINK.search(v):
                hata(f"{ad}: link var")
            if CAGRI.search(v):
                hata(f"{ad}: çağrı kelimesi var ({CAGRI.search(v).group()})")
            if "kaynak" not in v.lower():
                hata(f"{ad}: kaynak listesi yok")
            if "youtube" in v.lower():
                hata(f"{ad}: 'kaynaklar YouTube'da' gibi yönlendirme olmaz")
        if ad == "YT_ACIKLAMA" and CAGRI.search(v):
            uyari(f"YT_ACIKLAMA: çağrı kelimesi var ({CAGRI.search(v).group()})")
    # FBIG_ACIKLAMA = Facebook metni (4 etiket); IG_ACIKLAMA = Instagram (en fazla 5, IG sınırı)
    for ad, hedef in (("FBIG_ACIKLAMA", (4, 4)), ("IG_ACIKLAMA", (5, 5))):
        fb = alan.get(ad, "")
        if not fb:
            continue
        b, k = len(fb.encode()), len(fb)
        ne = len(re.findall(r"#\w+", fb))
        print(f"{ad}: {b} bayt, {k} karakter, {ne} etiket")
        if b > 370:
            hata(f"{ad} {b} bayt (en fazla 370)")
        if k >= 400:
            hata(f"{ad} {k} karakter (400 altı olmalı)")
        if not (hedef[0] <= ne <= hedef[1]):
            hata(f"{ad} {ne} etiket ({hedef[0]} olmalı)")
    xa = alan.get("X_ACIKLAMA", "")
    if xa:
        print(f"X açıklama: {len(xa)} karakter")
        if len(xa) > 250:
            hata(f"X_ACIKLAMA {len(xa)} karakter (en fazla 250; ücretsiz X sınırı 280)")
        ne = len(re.findall(r"#\w+", xa))
        if ne != 2:
            hata(f"X_ACIKLAMA {ne} etiket (2 olmalı)")
    yb = alan.get("YT_BASLIK", "")
    if yb and not re.search(r"#SıradanDeğil \d+$", yb):
        hata("YT_BASLIK biçimi '<cümle> #SıradanDeğil N' değil")
    if yb and len(yb) > 100:
        hata(f"YT_BASLIK {len(yb)} karakter (YouTube sınırı 100)")
    et = alan.get("YT_ETIKET", "")
    if et and len(et) > 500:
        hata(f"YT_ETIKET {len(et)} karakter (YouTube sınırı 500)")
    for ad in ("YT_ACIKLAMA", "TT_ACIKLAMA", "FBIG_ACIKLAMA"):
        v = alan.get(ad, "")
        if v and "CC BY" not in v and "Görseller" not in v:
            uyari(f"{ad}: görsel atfı satırı yok (CC BY/BY-SA görsel varsa ekle)")
    sorular = {alan.get(a, "").replace("👇", "").strip() for a in ("YT_SABIT", "TT_SABIT", "FBIG_SABIT")} - {""}
    if len(sorular) > 1:
        uyari("sabit yorumlar platformlar arasında farklı (kapanış sorusuyla aynı olmalı)")


def gorsel_kontrol(yollar):
    """Aday ya da kapak görsellerini sunmadan önce: python3 kontrol.py gorsel a.jpg b.jpg ..."""
    benzerlik_kontrol([(os.path.basename(y), y) for y in yollar])


# ---------------- HAZIR VİDEO (22.11.2026) ----------------
def video_kontrol(json_yol, mp4):
    """Üretilen videodan her sahnenin başı/ortası/sonu karesini alır; kenarlık, koyuluk ve kenardan taşma için
    tarar, tek panoya koyar. Pano GÖZLE de açılır: python3 kontrol.py video episodes/NNN_x.json NNN_x.mp4"""
    import subprocess, tempfile
    cv2 = _cv()
    if not cv2:
        return
    import numpy as np
    d = json.load(open(json_yol, encoding="utf-8"))
    kes = (d.get("dis_ses") or {}).get("kesimler") or []
    try:
        sure = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4],
                                    capture_output=True, text=True).stdout.strip())
    except Exception:
        hata("video okunamadı (ffprobe)"); return
    if kes and abs(sure - kes[-1][-1][1]) > 2.5:
        uyari(f"video süresi {sure:.1f} sn, ses {kes[-1][-1][1]:.1f} sn")
    tmp = tempfile.mkdtemp()
    kareler = []
    for i, k in enumerate(kes, 1):
        a, b = k[0][0], k[-1][1]
        for oran in (0.12, 0.5, 0.88):
            ts = a + (b - a) * oran
            f = os.path.join(tmp, f"s{i:02d}_{int(oran*100)}.jpg")
            subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{ts:.2f}", "-i", mp4, "-frames:v", "1", "-y", f])
            im = cv2.imread(f)
            if im is None:
                hata(f"sahne {i}: {ts:.1f}. sn karesi alınamadı"); continue
            k_ = cv2.resize(im, (270, 480), interpolation=cv2.INTER_AREA)
            # altyazı ve etiket alt/yan kenarda olduğundan bant ölçümü üst kenar + iki yan kenarla yapılır
            g = cv2.cvtColor(k_, cv2.COLOR_BGR2GRAY).astype(np.float32)
            L = np.abs(cv2.Laplacian(g, cv2.CV_32F))
            # Ölçüm (#111): gri bantlı v5 karelerinde üst 0,7-1,3 ve alt (altyazının altı) 1,0-2,2; temiz v7'de en az biri ≥4,8.
            ust, alt = L[:48].mean(), L[400:470, 30:240].mean()
            sol, sag, orta = L[60:300, :24].mean(), L[60:300, -24:].mean(), L[120:300, 40:230].mean()
            e = min(3.0, 0.3 * orta)
            if (ust < e and alt < e) or (sol < e and sag < e):
                hata(f"sahne {i} ({ts:.1f}. sn): karede KENARLIK/BULANIK BANT (üst {ust:.1f}, alt {alt:.1f}, sol {sol:.1f}, sağ {sag:.1f})")
            if i == 1 and oran == 0.12 and g.mean() < 70:
                hata(f"açılış karesi koyu (parlaklık {g.mean():.0f})")
            kareler.append(k_)
    if kareler:
        sut = 9
        satir = (len(kareler) + sut - 1) // sut
        pano = np.full((satir * 484, sut * 274, 3), 255, np.uint8)
        for n, k_ in enumerate(kareler):
            r, c = divmod(n, sut)
            pano[r * 484:r * 484 + 480, c * 274:c * 274 + 270] = k_
        cik = os.path.splitext(mp4)[0] + "_pano.jpg"
        cv2.imwrite(cik, pano)
        print(f"kare panosu: {cik} (her sahne başı/ortası/sonu; GÖZLE aç: kenardan taşma, yarım yüz, sesle uyum)")


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "gorsel":
        gorsel_kontrol(sys.argv[2:])
    elif len(sys.argv) == 4 and sys.argv[1] == "video":
        video_kontrol(sys.argv[2], sys.argv[3])
    elif len(sys.argv) != 3 or sys.argv[1] not in ("metin", "bolum", "set"):
        print(__doc__)
        sys.exit(2)
    else:
        {"metin": metin_kontrol, "bolum": bolum_kontrol, "set": set_kontrol}[sys.argv[1]](sys.argv[2])
    for m in hatalar:
        print("HATA  :", m)
    for m in uyarilar:
        print("UYARI :", m)
    print(f"SONUÇ: {len(hatalar)} hata, {len(uyarilar)} uyarı"
          + (" -> TESLİM EDİLEBİLİR" if not hatalar else " -> DÜZELTMEDEN TESLİM ETME"))
    sys.exit(1 if hatalar else 0)


if __name__ == "__main__":
    main()
