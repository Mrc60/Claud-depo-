# Kamera hızı notu (TEK1, 28 Ekim 2026)

Durum: SADECE NOT. TEK1 "şimdi işlem yapma, kaydet" dedi. Uygulamak için TEK1'in ayrı onayı gerekir.

## Tespit (TEK1'in analizi)
Kamera hızı sabit değil. Fotoğrafın şekline ve ekranda kalma süresine göre 30 kata kadar değişiyor.
"Bazı yerler akıcı, bazı yerler takılıyor" durumunun asıl sebebi bu.

Eski koddaki ayar (render.py, photo_scene):
- Yakınlaşma: her sahnede %5,6 (1.0 → 1.056).
- Kayma: fotoğrafın ekrana sığmayan kısmının %72'si kadar yana kayma. Mesafe sabit değil, fotoğraf genişliğine bağlı.
- Hareket eğrisi: ease_io (yavaş başlar, ortada hızlanır, yavaş biter; başta ve sonda hız sıfıra iner).
- Video: 30 kare/saniye.

Hesaplanan ortalama hızlar (kare başına piksel):

| Fotoğraf şekli | 7 sn sahne | 12 sn sahne |
|---|---|---|
| Dikey (9:16) | 0,4 | 0,3 (takılma burada) |
| Dikey (3:4) | 1,8 | 1,1 |
| Kare (1:1) | 3,7 | 2,1 |
| Yatay (4:3) | 6,1 | 3,6 |
| Yatay (16:9) | 9,4 | 5,5 (akıcı) |

Kare başına 1 pikselin altındaki hareketi göz "kayma" değil "takılma" olarak algılıyor.
Sıkıştırma da bu küçük farkları yutuyor. Yatay fotoğraflarda hız yüksek olduğu için sorun olmuyor.

## Önerilen çözüm (Claude Code'a verilecek talimat)
render.py photo_scene(): Kamera hızı fotoğrafın şekline göre 0,3 ile 9 px/kare arasında değişiyor.
Dikey fotoğraflarda 1 px/karenin altına düştüğü için takılma yapıyor. Düzelt:

1) Kayma mesafesini fotoğraf genişliğine değil süreye bağla.
   Hedef: sabit 1,5 px/kare (45 px/sn).
   pan_px = min(span_x, 45 * dur), x merkezden ±pan_px/2 kaysın.
   Fotoğraf dar olup yeterli kayma payı yoksa (span_x küçükse), hızı yakınlaşmayla tamamla:
   z_end = 1 + max(0.056, (45*dur - span_x) / W), üst sınır 1.15.
2) Hareket eğrisini doğrusal yap: u = clamp(lt/dur). ease_io kullanma, başta ve sonda kamera durmasın.
3) Kodlama: "-preset","slow","-crf","16","-tune","film","-x264-params","deadzone-inter=0:deadzone-intra=0:aq-mode=3"
4) Test: 048_hatay'ı yeniden üret (dikey "Hatay Kurtuldu" fotoğrafı ilk sahnede).
   Yavaş sahneden ardışık 30 kare çıkar, ardışık iki aynı kare olmamalı. TEK1'e telefonda izlemesi için gönder.

Hedef hız (1,5 px/kare) ayarlanabilir: şu anki yatay fotoğraflardan daha yavaş, dikeylerden 4–5 kat hızlı.
TEK1 akıcı bulduğu sahnelere göre "biraz daha hızlı / yavaş" derse sayı değiştirilir.

## Kayıt anındaki kod durumu (ccr-114296c0-jptwmw dalı, commit f64b655)
- Madde 2 (doğrusal eğri) UYGULANDI.
- Madde 3 (kodlama ayarı) UYGULANDI.
- Madde 1 (süreye bağlı sabit hız) UYGULANMADI. Önceki talimat "kamera hızını değiştirme" dediği için
  zoom 1.0 → 1.056 ve kayma ±%36 (toplam %72) olarak geri alındı.
- Ek: fotoğraflar 2 kat çözünürlükte işleniyor (SS = 2). Titremeyi gidermişti, TEK1 onayladı.
- Madde 4 (048_hatay testi) YAPILMADI. Önceki test 045_mubadele ve 049_musul ile yapıldı: donan kare yok.
- Bu ayarlarla üretilen 049_musul videosunu TEK1 "düzeldi" diye onayladı.
- Not: Daha önce bu oturumda benzer bir sabit hız denemesi (45 px/sn, zoom üst sınırı 1.12) yapılmış,
  sonra talimat gereği geri alınmıştı (commit fc282f6).
