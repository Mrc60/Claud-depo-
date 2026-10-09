"""Seslendirme için Türkçe metin temizliği.

- Kesme işaretlerini kaldırır (ses kelimeyi bölmesin: "Osmanlı'ya" -> "Osmanlıya")
- Sayıları yazıya çevirir: "1935'ten" -> "bin dokuz yüz otuz beşten",
  "19. yüzyıl" -> "on dokuzuncu yüzyıl", "%80" -> "yüzde seksen"
"""
import re

BIR = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
ON = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]

def yaziyla(n):
    n = int(n)
    if n == 0: return "sıfır"
    parts = []
    for val, name in ((10**9, "milyar"), (10**6, "milyon")):
        if n >= val:
            parts += [yaziyla(n // val), name]; n %= val
    if n >= 1000:
        k = n // 1000
        parts += (["bin"] if k == 1 else [yaziyla(k), "bin"]); n %= 1000
    if n >= 100:
        y = n // 100
        parts += (["yüz"] if y == 1 else [BIR[y], "yüz"]); n %= 100
    if n >= 10: parts.append(ON[n // 10]); n %= 10
    if n: parts.append(BIR[n])
    return " ".join(p for p in parts if p)

SIRA = {"bir": "birinci", "iki": "ikinci", "üç": "üçüncü", "dört": "dördüncü", "beş": "beşinci",
        "altı": "altıncı", "yedi": "yedinci", "sekiz": "sekizinci", "dokuz": "dokuzuncu", "on": "onuncu",
        "yirmi": "yirminci", "otuz": "otuzuncu", "kırk": "kırkıncı", "elli": "ellinci", "altmış": "altmışıncı",
        "yetmiş": "yetmişinci", "seksen": "sekseninci", "doksan": "doksanıncı", "yüz": "yüzüncü",
        "bin": "bininci", "milyon": "milyonuncu", "milyar": "milyarıncı"}

def sirayla(n):
    w = yaziyla(n).split()
    w[-1] = SIRA[w[-1]]
    return " ".join(w)

APOS = "'’ʼ"

def temizle(text):
    t = text
    t = re.sub(r"%\s*(\d+)", lambda m: "yüzde " + yaziyla(m.group(1)), t)
    # Sıra sayısı: "19. yüzyıl" (nokta + boşluk + küçük harf)
    t = re.sub(r"\b(\d+)\.(?=\s+[a-zçğıöşü])", lambda m: sirayla(m.group(1)), t)
    # Sayı + ek: "1935'ten", "1935ten", "1935"
    t = re.sub(r"\b(\d+)[" + APOS + r"]?([a-zçğıöşü]*)", lambda m: yaziyla(m.group(1)) + m.group(2), t)
    t = re.sub("[" + APOS + "]", "", t)
    return re.sub(r"\s+", " ", t).strip()

if __name__ == "__main__":
    for s in ["Şişecam, 1935ten beri üretiyor.", "İlk kanun 1924'te çıktı, fabrika 1947de açıldı.",
              "19. yüzyılda Osmanlı'ya ulaştı.", "1709'da Köln'e yerleşti.", "%80'i alkol", "317 yıldır", "2. bölüm"]:
        print(s, "->", temizle(s))
