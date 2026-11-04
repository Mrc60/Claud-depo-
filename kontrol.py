#!/usr/bin/env python3
"""Sıradan Değil teslim öncesi kontrol (iki hesap için ortak).

Kullanım:
  python3 kontrol.py metin  senaryo.txt          # ElevenLabs metni
  python3 kontrol.py bolum  episodes/NNN_x.json   # bölüm JSON'u (görsel, süre)
  python3 kontrol.py set    set.txt               # yükleme seti

Yükleme seti dosya biçimi: her alan "=== AD ===" satırıyla başlar. Adlar:
  YT_BASLIK, YT_ACIKLAMA, YT_ETIKET, YT_SABIT, TT_ACIKLAMA, TT_SABIT,
  FBIG_ACIKLAMA (Facebook, 6 etiket), IG_ACIKLAMA (Instagram, 5 etiket), FBIG_SABIT, X_ACIKLAMA

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
ETIKETLER = {"serious", "thoughtful", "calm", "sad", "short pause", "long pause"}
SON_CUMLE = ("Böyle az bilinen tarih ve kültür hikâyeleri için videomuzu "
             "beğenmeyi ve takip etmeyi lütfen unutmayalım.")
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
    if "Kaynakları video açıklamasında bulabilirsiniz" not in duz:
        hata("kapanışta 'Kaynakları video açıklamasında bulabilirsiniz.' yok")
    if SON_CUMLE not in duz:
        hata("sabit son cümle yok ya da farklı yazılmış")
    if "dede" in duz.lower():
        uyari("'dede' çerçevesi geçiyor (her videoda kullanma)")
    kelime = len(duz.split())
    sn = kelime / 2.3
    print(f"kelime: {kelime}, tahmini süre: {sn:.0f} sn")
    if sn > 75:
        uyari(f"tahmini süre {sn:.0f} sn (75 üstü; TEK1 isterse sorun değil)")


# ---------------- BÖLÜM ----------------
def md5(yol):
    return hashlib.md5(open(yol, "rb").read()).hexdigest()


def bolum_kontrol(yol):
    d = json.load(open(yol, encoding="utf-8"))
    no = os.path.basename(yol)[:3]
    if not d.get("acilis"):
        hata("'acilis' (ilk 3 sn merak yazısı) yok")
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
            if sure < 6:
                uyari(f"sahne {i}: görsel {sure:.1f} sn ekranda (<6 sn)")
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
    print("not: aynı fotoğraf farklı kırpımla indirildiyse md5 yakalamaz; panoda göz kontrolü yap")


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
    # FBIG_ACIKLAMA = Facebook metni (6 etiket); IG_ACIKLAMA = Instagram (en fazla 5, IG sınırı)
    for ad, hedef in (("FBIG_ACIKLAMA", (6, 6)), ("IG_ACIKLAMA", (5, 5))):
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


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("metin", "bolum", "set"):
        print(__doc__)
        sys.exit(2)
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
