---
name: "yorum-cevapla"
description: "Sıradan Değil kanalının TikTok, Instagram, Facebook ve YouTube yorumlarına cevap taslağı hazırlar ve gönderir. TEK1 yorum yapıştırdığında ya da 'Yorum:' dediğinde kullan."
---

# Yorum cevaplama — Sıradan Değil

Depo: /home/claude/claud-depo- (yoksa github.com/Mrc60/Claud-depo- klonla). Önce CLAUDE.md bölüm 8'i oku; bu beceri onun uygulamasıdır, çelişirse CLAUDE.md geçerli.

## 1. Hangi video?
- TEK1 platform ve videoyu yazdıysa onu kullan.
- Yazmadıysa yorumun içeriğinden tahmin et ve başlıkta "(tahmin)" yaz. Tahmin edemiyorsan tek kısa soru sor.

## 2. Bilgi kartı
- `episodes/NNN_*.json` dosyasındaki segments[].say metinlerini birleştir (python ile, sadece `say` alanı). Video açıklamasındaki kaynaklar da karta dahil.
- Cevaplar SADECE bu karttaki bilgiye dayanır. Kartta olmayan bilgi uydurulmaz.

## 3. Yorumları getirme (sadece Zernio ile çekilen IG/TikTok için)
- Instagram hesabı 6ade30e2924b817a8f5f9a8a, TikTok hesabı 6ade311b2981fad19e1d90f3.
- Sadece en yeni 20–30 ana yorumu çek. Büyük çıktıyı dosyaya kaydet, gereken alanları python/jq ile çıkar.
- Çift cevap önleme: `yorumlar/defter.json` (sinir_notu = zaman sınırı), @isim kontrolü, defterdeki yorum_id kontrolü. Sadece ANA yorumlara cevap ver.
- Facebook ve TikTok/IG'de TEK1 yorumu kendisi yapıştırdıysa çekme yapma, cevabı da TEK1 gönderir.

## 4. Taslak listesi formatı
- En başa: `Platform · Video · Hesap` (örn. "Facebook · Okuma videosu · Sıradan Değil").
- Zernio'dan çekilen listede: en yeniden eskiye sırala ve bunu belirt. TEK1'in ekran görüntüsünde: ekrandaki sırayı koru (yukarıdan aşağı).
- Her madde: kullanıcı adı, yorumun TAM metni (kısaltma yok, "…" yok), altında kopyalanabilir blokta TEK cevap.
- Atlananlar yerinde "atlandı" + tek satır sebep.

## 5. Cevap kuralları (göstermeden önce HER taslağı bu listeyle kontrol et)
- [ ] Soru YOK (dolaylı soru da yok: "merak ettik", "paylaşırsanız seviniriz" gibi).
- [ ] Kısa: 1–2 cümle, en fazla 3.
- [ ] Teşekkür sadece yorumcu naziksе. Her cevapta teşekkür yok.
- [ ] Kalp emojisi sadece yorumcu kullandıysa. 🙏 kullanılabilir.
- [ ] "Kaynaklarda" demek yok; kaynak sadece sorulursa.
- [ ] Cevaplar birbirine benzemiyor.
- [ ] Kartta olmayan bilgi yok; yorumcunun kartta olmayan iddiasını doğrulama ya da reddetme.
- [ ] Tek taslak ver, alternatif seçenekler sunma.

Yorum türüne göre:
- Kendi hikâyesini anlatan: dinleyen biri gibi kısa, uygunsa karttan bir bilgiyle bağla.
- Soru soran: sadece karttaki bilgiyle cevapla; kartta yoksa nazikçe teşekkür et.
- Yanlış bilgi veren / suçlayan ("yalan" diyen): tartışma, savunmaya geçme; karttaki doğru bilgiyi yumuşakça söyle.
- "Bizde de vardı" diyen: onaylama/reddetme, teşekkür et.
- Gergin ama konuyla ilgili: savunmacı olmayan, yumuşak, kısa.
- Konu dışı, siyasi, alaycı-kışkırtıcı, hakaret, kullanıcılar arası tartışma: atlandı.
- Kanalın kendi yorumu ya da TEK1'in hesabı (ör. WANENS profilli): atlandı.
- Şehitler için "ölü" değil "şehit".

## 6. Gönderme (sadece Zernio, sadece TEK1 onayından sonra)
- Onay sadece gösterilen taslakları kapsar.
- Göndermeden hemen önce yeniden kontrol et (son 10 dk önbellekte görünmeyebilir, bunu belirt).
- Bir seferde en fazla 10 cevap, aralarında birkaç saniye.
- Her gönderimde comment_id ver, dönüşte isReply: true kontrol et.
- Her gönderilen cevabı defter.json'a yaz: {yorum_id, kullanici, yorum, cevap_id, tarih}.
- Instagram'da beğeni yok. Profillere girme, kimseyi takip etme.

## 7. Rapor
Ne gönderildi, ne atlandı, ne kontrol edilemedi (ör. önbellek), onay gereken bir şey var mı. Kısa, Türkçe.