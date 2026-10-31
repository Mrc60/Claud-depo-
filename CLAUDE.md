# SIRADAN DEĞİL — DEVİR NOTU (TEK1)

Her oturumda önce bu dosyayı oku ve kurallara uy.

## 1. KİM, NE
- Kullanıcı: TEK1. Sadece telefon ve tablet kullanır, bilgisayar gerektiren adım verme.
- Kanal: "Sıradan Değil", Türk tarihi ve kültürü Shorts.
  - YouTube: @siradan.degil
  - TikTok: @siradan.degil
  - Instagram: @siradandegill
  - Facebook
- Repo: github.com/Mrc60/Claud-depo-
- Günde 2 video: sabah ve akşam 18:00.
- İletişim Türkçe, kısa ve sade. Emin değilsen "emin değilim" de, hatanı kendin söyle.

## 2. GENEL ÇALIŞMA KURALLARI
- TEK1'in açık onayı olmadan hiçbir şey yapma. Onay sadece söylenen işi kapsar.
- Ücretli işlemden önce maliyeti söyle, onay al, varsa ücretsiz alternatifi belirt.
- Şifre ve API anahtarı isteme, gösterme.
- Metinleri sohbette kopyalanabilir bloklarla ver. İstenmedikçe .txt dosyası gönderme.
- Hatanı TEK1 bulmadan söyle: hata, sebep, önlem.
- Kanıtın desteklediğini söyle, TEK1'in duymak istediğini değil.
- Tahmini doğrulanmış bilgiden ayır. Dosya gerçekten oluşmadan "hazır" deme.
- İş bitince şunları raporla: ne yapıldı, ne kontrol edildi, ne kontrol edilemedi, onay gerekiyor mu.
- Yeni sohbet açmayı önerme.
- PROAKTİF OL (TEK1 kararı, 30.10.2026): Yönlendirme bekleme. TEK1'in ana hedefi para kazanmak ve kanalı büyütmek; bunu her işte aklında tut. Fırsat, risk ya da daha iyi bir yol görürsen kendin söyle ve "bunu böyle yapalım" diye gerekçeli öneri getir. Öneri getirmek serbest; uygulamak yine TEK1'in onayına bağlı.
- Diğer yapay zekâlara (GPT, Manus, Perplexity) prompt yazarken sonuna şunu ekle: "Cevabını bana kopyalanabilir formatta ver."
- RAPOR ADI (TEK1 kararı, 31.10.2026): Her araştırma raporunun EN BAŞINDA hangi uygulamanın yazdığı yazsın: "Claude raporu", "Manus raporu", "GPT raporu", "Perplexity raporu" vb. Diğer yapay zekâlara yazılan her araştırma promptuna şunu ekle: "Cevabının en başına '[Uygulama adın] raporu' yaz." Kendi raporlarımı "Claude raporu" diye başlat.

## 2a. İKİ HESAP, TEK BEYİN (TEK1 kararı, 31.10.2026)
TEK1 iki Claude hesabıyla çalışır; ikisi de bu repoyu kullanır. Ortak hafıza GitHub'dadır.
- Oturum başında oku: CLAUDE.md, HAFIZA.md (kalıcı tercihler, birinci hesabın hafıza kopyası), DURUM.md (şu anki işler). Yorum işi için beceriler/yorum-cevapla/SKILL.md.
- Her iş başında `git pull`; yorum cevaplamadan hemen önce yorumlar/defter.json'u yeniden çek ve oku (iki hesap aynı yoruma yazmasın).
- Aynı anda iki hesap çalışmaz. İş bitince DURUM.md'yi güncelle ve (TEK1 onayıyla) GitHub'a gönder ki diğer hesap görsün.
- Yeni kalıcı tercih/ders öğrenince HAFIZA.md ve CLAUDE.md'ye yaz.
- Bağlantılar (Zernio, Buffer, vidIQ, ElevenLabs) ve hatırlatmalar hesaba bağlıdır; ikinci hesapta ayrıca bağlanır/kurulur.
- HESAP ETİKETİ: Her kayıt mesajının sonuna `Hesap: 1` ya da `Hesap: 2` satırı ekle (birinci hesap = Claude Code bulut oturumu, ilk kurulan). Böylece kimin ne yaptığı belli olur.
- MESAJLAR.md: Hesaplar arası not defteri (bilgi, iş, hata, soru). Oturum başında önce bunu oku, sana yazılanı cevapla.
- KARŞILIKLI DENETİM: Oturum başında diğer hesabın son kontrolden beri yaptığı kayıtları (`git log`) incele: kaynak, senaryo, yükleme seti kuralları, yorum cevapları, defter. Hata bulursan TEK1'e söyle ve MESAJLAR.md'ye HATA olarak yaz. Düzeltmeyi TEK1 onayıyla yap.
- GECE KONTROLÜ (TEK1 kararı, 31.10.2026): Her gün Hesap 1 ~04:30, Hesap 2 ~05:30 (İstanbul) zamanlanmış görevle çalışır: repo'yu çeker, MESAJLAR.md ve diğer hesabın son kayıtlarını denetler, bulguları MESAJLAR.md'ye, durumu DURUM.md'ye yazar ve SADECE bu iki dosyayı main'e gönderir (TEK1 bu gönderime genel onay verdi). Başka hiçbir iş yapmaz (yorum cevabı, video, yayın yok). Karar her zaman TEK1'in.

## 2b. KULLANIM TASARRUFU (TEK1 kararı, 29.10.2026)
Kalite ve doğrulama kurallarından ödün verme; sadece boşuna harcamayı kes.
- Yorumlar: sadece en yeni 20–30 ana yorumu çek. Tam tarama yapma; zaman sınırını defter.json'daki "sinir_notu"ndan al. Tam tarama sadece ilk kez bakılan videoda bir kez yapılır, sınır deftere yazılır.
- Büyük araç çıktılarını sohbete dökme; dosyaya kaydet, python/jq ile sadece gereken alanları çıkar.
- Görseller: aday fotoğrafları ve video karelerini tek pano görselinde incele, tek tek açma.
- Değişmemiş dosyayı/veriyi boşuna tekrar okuma; sadece gereken kısmı oku. AMA şu durumlarda mutlaka yeniden oku/kontrol et: dosya değiştiyse; geri alınamaz işten önce (yorum göndermeden önce son kontrol, main'e push); kaynak doğrulamada; emin olmadığında.
- Video beklemesi: arka plan komutu (bkz. bölüm 9), ara kontrol yok.
- Araştırma: ağır taramayı GPT/Manus/Perplexity yapsın, sen kontrol et. Doğrulama protokolü (bölüm 4) aynen geçerli.
- Mesajlar kısa ve net. Model değiştirme önerme.

## 3. KONU SEÇİMİ
- KANAL DİZİNİ: DIZIN.md (python3 dizin.py ile güncelle). Konu ve görsel tekrarını önce buradan kontrol et; yeni bölüm eklenince dizini yenile. Not: aynı fotoğraf farklı dosya adıyla indirildiyse dizin yakalamaz, Commons dosya adını/LCCN numarasını da grep'le.
- Konu önermeden önce episodes/ klasörüne bak, tekrar olmasın.
- Konuyu TEK1 onaylamadan seçme. Seçenekleri karşılaştırıp gerekçeli öneri ver.
- 15 yaştan en yaşlıya, kadın ve erkek herkese hitap etsin. Çocukça olmasın.
- Unutulmuş, derin, çarpıcı bilgiler: eski kurallar, yasaklar, geçmişten dersler.
- İzleyici gurur duysun ve kendi hayatını videoda bulsun.
- Her videoda "dede" çerçevesi kullanma. Atatürk görselini az kullan.

## 4. DOĞRULAMA PROTOKOLÜ (EN ÖNEMLİ)
- Her önemli iddia en az 2 bağımsız, güvenilir kaynakla doğrulanacak: akademik, resmî veya birincil kaynak. Aynı iddianın kopyaları ayrı kaynak sayılmaz. Popüler web siteleri ve Wikipedia tek başına yetmez.
- Okumadığın kaynağı kontrol edilmiş gibi gösterme. "Ben okudum" ve "Manus okudu" ayrımını yaz.
- Kaynaklar bir ayrıntıda çelişiyorsa o ayrıntıyı yeniden yazma, metinden çıkar.
  - Örnek: Musul'daki %10 petrol payından "500 bin sterline vazgeçildi" bilgisi tartışmalıydı. Çoşar-Demirci 2004'e göre Türkiye 1931–1952 arasında ödeme aldı.
- "İlk", "icat etti" gibi iddialar güçlü kanıt ister, yoksa çıkar.
- Zayıf iddiayı "tartışmalı" diye getirme. Daralt, çıkar ya da konuyu değiştir.

## 5. SENARYO KURALLARI
- Her senaryoyla birlikte cümle–kaynak tablosu ver: cümle | kaynak | kaynaktaki birebir ifade.
  - Kaynağı olmayan cümleleri "anlatım" diye işaretle.
  - Kaynakta olmayan dramatik ayrıntı (sahne, duygu, olay sırası) ekleme.
- Hikâyede zorluk, engel ve mücadele olsun. Düz rapor gibi anlatma.
- Senaryo net ve kolay anlaşılır olsun, izleyicinin alacağı bir amaç olsun.
- Teknik terimleri açıkla. Örneğin "mübadele = zorunlu nüfus değişimi".
- Tarihle açılış yapma ("1923'te…" gibi). Olayla ya da soruyla aç.
- İlk saniye izleyiciyi yakalamalı.
- Ekler bitişik yazılır, kesme işareti yok: "Tarsusta", "Türkiyeye". ElevenLabs kesme işaretinde hata yapıyor.
- ElevenLabs etiketleri tek kelime: [serious] [thoughtful] [calm] [sad] [short pause] [long pause]. Birleşik ya da başka etiket ([confident], [emphatic] vb.) kullanma.
- Sorudan sonra [short pause] koy (yaklaşık 0,7 sn).
- Kapanış:
  - Konuya özel bir soru sor.
  - Yorumlara davet et: "Düşüncelerinizi yorumlarda paylaşın."
  - Sonra: "Kaynakları video açıklamasında bulabilirsiniz."
  - Sabit son cümle: "Böyle az bilinen tarih ve kültür hikâyeleri için videomuzu beğenmeyi ve takip etmeyi lütfen unutmayalım."
- TEK1 senaryoyu onaylamadan ses üretme. Sesi TEK1 ElevenLabs'te kendisi alıp mp3 gönderir.
- Şehitler için "ölü" değil "şehit" de. Ceset fotoğrafı kullanma.
- Senaryo teslimi: A) yayına hazır metin, B) kaynak tablosu ve bağlantılar, C) sahne sahne görsel planı, D) sadece yapılan kontrolleri içeren doğrulama raporu, E) yayın kararı.

## 6. GÖRSEL KURALLARI
- Eski siyah-beyaz gerçek fotoğraflar kullan, ne kadar eski o kadar iyi. Renkli görsel ciddi durmaz.
- Yapay zekâ ile yeniden çizim yapma. Tablo, gravür ve harita varsa altyazıda öyle belirt.
- Belge taraması az olsun, izleyici belge okumaz.
- Görsel konuşulan konuyu göstermeli.
- Her görsel en az 6 sn ekranda kalsın. Konu değişince görsel de değişsin.
- Görsel ekranı doldurmalı (fit "doldur" + kirp). Küçük pencere olmamalı.
- Yazı kutularının koyu gölgesi fotoğrafı kapatmasın.
- Kamera hareketi yavaş olsun.
- "Sıradan Değil · #N" etiketi kenarda yavaşça hareket etsin, ekranın ortasından geçmesin.
- Her zamanki arka plan müziğini kullan.
- Lisans:
  - Kamu malı veya CC olmalı.
  - NC/ND (ticari kullanım yasak) olanları kullanma, örneğin SALT Araştırma.
  - Kaynağı blog veya forum olan Commons dosyalarını kullanma.
- Kapak: Kapağı TEK1 ChatGPT'de kendisi yapar. Sen sadece 2–3 arka plan fotoğrafı ve başlık fikri verirsin. Eski kapak tarzı istenir, yıpranma efekti hafif olsun.

## 7. YÜKLEME SETİ
- Video yapılıp TEK1 onayladıktan sonra tüm seti tek seferde ver. Her alan ayrı kopyalanabilir blokta olsun.
  - YouTube: başlık, açıklama, etiketler, sabit yorum, diğer alanlar (kategori Eğitim, dil Türkçe, çocuklara yönelik değil)
  - TikTok: açıklama, sabit yorum
  - Instagram: açıklama, sabit yorum
  - Facebook: metin, sabit yorum
- Her platformun açıklamasında kendi kaynak listesi olsun. "Kaynaklar YouTube'da" yazma.
- FB/IG AÇIKLAMA BAYT SINIRI (30.10.2026, doğrulandı): Facebook "10-400 karakter" uyarısında karakteri değil UTF-8 BAYTI sayıyor (Türkçe harf 2, emoji 4 bayt). Açıklama en fazla 370 BAYT olsun, her seferinde python ile `len(t.encode())` ölç. 📚 emojisi ve · işareti kullanma. (Banker 410 bayt 8/9 → 356 bayt 9/9; Altı Sıfır ve Ege aynı.) Uyarı erişimi öldürmüyor ama 9/9 hedef.
- EMOJİ YOK (TEK1 kararı, 31.10.2026): Sabit yorum HARİÇ hiçbir alanda emoji yok: başlık, açıklama, etiket; YouTube, TikTok, Instagram, Facebook hepsi. Sabit yorumda emoji serbest (ör. Banker IG sabit yorumu 👇 ile bitiyordu). Facebook ve TikTok açıklamasında emoji sorun çıkarıyor.
- SABİT YORUM = merak cümlesi (videodaki en çarpıcı doğrulanmış bilgi) + videonun kapanış sorusu + kaynaklar (YouTube'da kaynaklar açıklamada olduğu için yorumda gerekmez). Kuru kaynak listesi ya da açıklamanın tekrarı olmaz.
- Soru videonun kendi kapanış sorusuyla aynı olsun; "büyükleriniz ne anlatırdı" gibi zorlama soru yok.
- TESLİMDEN ÖNCE ZORUNLU KONTROL: Seti göndermeden önce tüm blokları python ile tara: emoji var mı, · var mı, FB/IG açıklaması ≤370 bayt mı, açıklamada link/"beğen"/"paylaş" var mı. Sonucu teslimde tek satırla yaz. Seti TEK SEFERDE, tüm alanlar eksiksiz ver; parça parça düzeltme gönderme.
- Açıklamalarda (özellikle FB) link, "beğen", "paylaş", "etiketle" gibi çağrı olmasın (FB "engagement bait" sayıp erişimi düşürür). Videodaki sesli kapanış cümlesi buna dahil değil.
- Facebook + Instagram (30.10.2026'dan itibaren): TEK1 ikisini AYRI ayrı paylaşır (Meta Business Suite'te IG kapağı konamıyor; IG uygulamadan atılır). Açıklama ikisinde aynı, tek ortak metin ver: açıklama en fazla 350 karakter (kısa kaynak adları dahil), sonra etiketler; toplam 400 karakterin altında. Bağlantılı tam kaynak listesi sabit yorumda.

## 8. YORUM CEVAPLARI
- Listenin başına platform, video ve hesap yaz: "Instagram · Gelin videosu · @siradandegill".
- Ekrandaki sırayı koru (yukarıdan aşağı). Atlananları yerinde işaretle.
- Yorumun tam metnini kısaltmadan, taslak cevabın yanında göster.
- Çizgi: saygılı, ölçülü, tarafsız. Siyasi ve hakaret içeren yorumları atla.
- Cevaplarda soru sorma. Kısa ve net yaz.
- Yorumcu kalp kullanmadıysa kalp koyma. 🙏 kullanılabilir.
- Kanalın zaten cevap verdiği yorumlara cevap verme. Aynı kişiye iki kez cevap verme.
- Profillere girme, kimseyi takip etme.
- Taslakları göster, TEK1 onaylamadan gönderme. Zernio'da beğeni yapma.
- Cevaptan önce videonun bilgi kartını hazırla (episodes/NNN_*.json metni + açıklamadaki kaynaklar). Cevaplar bu karta bağlı kalsın, insan gibi doğal ve konuya uygun olsun.
  - Kendi hikâyesini anlatana: dinleyen biri gibi kısa cevap, uygunsa karttan bir bilgiyle bağla.
  - Soru sorana: sadece karttaki bilgiyle cevap ver. Kartta yoksa bilgi uydurma, nazikçe teşekkür et.
  - Yanlış bilgi verene: tartışma, karttaki doğru bilgiyi yumuşakça söyle.
  - Başka yöre/topluluk anlatana ("bizde de vardı"): onaylama ya da reddetme, teşekkür et. Kaynakta olmayan yeri doğrulama.
  - Konu dışı, siyasi, hakaret: cevap yok, listede "atlandı" diye işaretle.
- Teşekkürü her cevaba koyma. Yorumcu nazik ise teşekkür et, değilse sadece yoruma karşılık ver. Cevaplar birbirine benzemesin.
- Bir seferde en fazla 10 cevap, aralarına birkaç saniye (toplu gönderim spam riski).
- Listeyi en yeniden eskiye ver ve bunu listenin başında belirt (Instagram ekran sırası herkese aynı değil).
- Öncelik: soru soranlar ve en yeni yorumlar.
- Kullanıcıların birbiriyle tartışmasına (etnik köken, siyaset vb.) hiç girme.
- Cevaplarda sürekli "kaynaklarda" deme. Kaynağı sadece soran olursa söyle. Az empati, abartma yok.
- ÇİFT CEVAP ÖNLEME (TEK1 ekran görüntüsü vermez, sistem kendisi çözmeli):
  - Instagram API'si kanalın eski cevaplarının çoğunu "hangi yoruma" bilgisi olmadan, ana listede ayrı yorum olarak verir. replyCount güvenilmez. Kanal yorumunun (sabit yorum) altındaki yanıtların bir kısmı comment_id ile de gelmez.
  - Kurallar her video için ayrı çalışır:
    1. Zaman sınırı: Tüm sayfaları tara. Kime yazıldığı belli olmayan (@isim yok, defterde yok) en son kanal yorumunu bul. Ondan önceki yorumlara cevap verme.
    2. İsim kontrolü: "@kullanıcı" ile başlayan kanal yorumu olan kişinin o yorumuna tekrar yazma.
    3. Defter: yorumlar/defter.json. Gönderilen her cevabı (yorum_id, kullanıcı, yorum, cevap_id) kaydet. Defterdeki yoruma tekrar yazma.
  - Aynı kişi aynı videoya FARKLI yeni bir yorum yazarsa ona cevap verilebilir.
  - Göndermeden hemen önce tekrar kontrol et. Son 10 dakikayı (önbellek) göremeyebilirsin, bunu belirt.
  - SADECE ANA YORUMLARA cevap ver (TEK1 kararı, 29.10.2026). Yanıtlara (sabit yorum altındaki konuşmalar dahil) cevap verme; Instagram 3. katı açmaz, cevap listenin sonuna düşer.
  - Her gönderimde comment_id ver ve dönüşte isReply: true olduğunu kontrol et.
- Instagram'da yorum beğenisi API ile yapılamaz (canLike: false). Beğeniyi TEK1 isterse kendisi yapar.

## 8b. GÜNLÜK 3 YORUM HİKÂYESİ (TEK1 kararı, 30.10.2026)
- Her gün o gün yayınlanan İKİ videonun yorumlarından toplam 3 güzel yorum seçilir, ertesi gün hikâyede paylaşılır.
- TEK1 "dünün yorumları" der. IG yorumlarını Zernio ile çek; FB yorumlarını TEK1 yapıştırır.
- Seçim: kendi hikâyesini/büyüklerinden duyduğunu anlatan, saygılı, siyaset ve kavga içermeyen. Önce 3 yorumu göster, onaydan sonra kanal tarzında (eski kâğıt, siyah-beyaz) hikâye görseli hazırla; her yorumun altında hangi videoya yazıldığı küçük yazsın.
- Duyuru metni: "Her gün iki videomuza yazılan en güzel 3 yorumu ertesi gün hikâyemizde paylaşıyoruz. Düşüncelerinizi yorumlarda yazın 👇"

## 9. TEKNİK ALTYAPI
- GitHub Actions. Tetiklemek için (gh varsa): gh api -X POST repos/Mrc60/Claud-depo-/actions/workflows/X.yml/dispatches -f ref=main
  - belge-indir.yml: belgeler.txt → 'belgeler' dalı. Çıktı rapor.txt ve .txt dosyaları. Ağ izni olmayan PDF'leri böyle indir.
  - gorsel-arastirma.yml: aday_sorgular.json → 'adaylar' dalı.
    - Girdi: {bolum, min_w, sorgular[], incele[], indir[{file, ad}]}
    - Çıktı: pano_*.jpg, adaylar.json, incele.json, paket/ + kunyeler.txt
    - Not: Her çalışma bir öncekini siler.
  - transkript.yml: transkript.txt (ses yolu) → 'transkript' dalı words.json. Format [[başlangıç, bitiş, kelime], …]
  - video-uret.yml: main dalında episodes/ klasörüne push yapınca → 'videolar' dalı NNN_slug.mp4
- Bölüm JSON'u episodes/NNN_slug.json:
  - dis_ses: {file, kesimler: [[[bas, bit]], …]}
  - segments: [{say, caption, key[], image:{local, fit:"doldur", kirp:[x0,y0,x1,y1], baslik, kaynak}, scene:"photo"}]
  - Görseller assets/belgeler/NNN_*.jpg, ses assets/ses/NNN_slug.mp3
  - "acilis": "Satır 1\nSatır 2" → ilk 3 sn üstte büyük merak yazısı (render.py draw_acilis). Her yeni bölümde kullan (TikTok verisi: izleyicilerin çoğu 3. sn'de ayrılıyor, 29.10.2026).
- Hedef video süresi 60–75 sn (TikTok'ta 105–120 sn videoların sonuna kadar izlenme oranı %2'nin altında).
- DENEME (30.10.2026): Bekârlıktan sonraki ilk video 60 sn altında olacak; FB tamamlanma oranı önceki videolarla (%1,9) karşılaştırılacak.
- Kenarlık uyarısı: sebebi kenardaki koyu gölgeydi, Devrim'de azaltıldı (Devrim ve Bekârlık 9/9). Gölgeyi tekrar koyulaştırma.
- Bekleme (TEK1 kararı, 29.10.2026): 10 sn arayla kontrol ETME. Videoyu gönderdikten sonra arka planda çalışan tek bir komut başlat (run_in_background): önce 5 dk bekler, sonra run "completed" olana kadar 1 dk arayla kendisi kontrol eder ve bitince haber verir. Bu sırada ayrıca kontrol yapma (kullanım harcar).
- Kare kontrolü: kareleri tek tek değil, tek bir pano görselinde toplu kontrol et.
- Video bitince kareleri çıkarıp kontrol et (ffmpeg), sonra gönder.
- Zernio (yorum cevabı):
  - Instagram hesabı 6ade30e2924b817a8f5f9a8a, TikTok hesabı 6ade311b2981fad19e1d90f3
  - Instagram'da beğeni yok.
  - TikTok: cevap gönderme test edildi (29.10.2026, Lozan 7700989622838480146). Yanıtlar doğru yorumun altında gelir, replyCount güvenilir. Lozan/Musul yorumları çoğunlukla gergin ve siyasi: savunmacı olmayan, yumuşak, kısa cevap.
  - Post ID'leri: gelin 18020789228731773, okuma 18129154627891169
  - Sonuçlar 10 dakika önbellekte kalabilir.
- Buffer (bağlı, ücretsiz plan, yorum cevabı yok):
  - Organizasyon 6ade039fa8e025d067c17969
  - Facebook 6ade0bd02f1f5ed648c8ec0b, TikTok 6ade0ae12f1f5ed648c8d4c6, Instagram 6ade04652f1f5ed648c8a6e9
- PostProxy: Ücretsiz kota bitti, 23 Kasım 2026'da yenilenir.

### Claude Code bulut oturumu notları
- Yerel depo yolu oturuma göre değişir (ör. /home/user/Claud-depo-).
- Her oturumun kendi çalışma dalı olur (ccr-...). video-uret.yml sadece main dalındaki push ile otomatik çalışır.
- main dalına push yapmak için TEK1'in o iş için açık izni gerekir.
- Bulut oturumunda gh CLI yerine GitHub MCP araçları kullanılır (iş akışı tetikleme: actions_run_trigger).

## 10. YAPILANLAR
- #42 Gelin: video bitti. Açılış düzeltildi ("Gelininin kendisiyle bir kez olsun konuşmasını").
- #43 Okuma (Millet Mektepleri): video bitti.
- #44 Arzuhalci: video, yükleme seti ve kapak görselleri bitti.
- #45 Mübadele (Giritli Müslümanlar, Karamanlılar): video ve yükleme seti bitti.
- #46 Lozan: video, yükleme seti ve kapak görselleri bitti. Bilgiler doğrulandı.
  - Not: Sisam sahnesi bulanık, TEK1 olduğu gibi bıraktı. Seste "vazgeçtik" deniyor.
- #47 Türkiye'nin Sınırları: video, yükleme seti, kapak görselleri, başlık fikirleri ve sabit yorum bitti. Petrol payı cümlesi düzeltildi.
- #48 Hatay: video, yükleme seti ve kapak görselleri bitti.
  - Not: 1936 cümlesi tek kaynaklı (Yamaç). 3711 sayılı kanun doğrulanmadığı için çıkarıldı.
- Zernio test cevabı gönderildi: okuma videosu, @sahin_urfa9208.

## 11. YAPILACAKLAR / AÇIK İŞLER
- Gelin videosu, Instagram yorumları: yorumları yeniden çek, TEK1'in zaten cevapladıklarını çıkar, taslak göster, onay al, Zernio ile gönder, beğenme.
- İsteğe bağlı: arzuhalci videosundaki Osman Hamdi tablosunu siyah-beyaz yap (teklif edildi, cevap yok).
- Kurulmuş hatırlatmalar: Sarıkamış (19 Aralık), Erzincan depremi (24 Aralık), KKTC videosu (13 Kasım).
- PLANLI: 15 Kasım KKTC yıl dönümü videosu: "Bir ada nasıl iki devlet oldu? Neden KKTC, neden Rum kesimi?" Akış: 1960 ortak cumhuriyet (garantörler TR, YU, İng) → ortaklığın bozulması (1963 "çıkarıldı/çekildi" tartışmalı, yazma) → 15 Temmuz 1974 darbe, 20 Temmuz müdahale → 1975 Federe Devlet, 15 Kasım 1983 KKTC → BMGK 541, sadece TR tanıyor, Rum tarafı 2004 AB. Tarafsız, belgeli olaylar. Diğer Kıbrıs fikirleri: Yeşil Hat, 1878 devir, Kanlı Noel (21 Aralık), Kıbrıs Türklerinin göçü, Kıbrıs Türkçesi.
- Sıradaki konu: TEK1 karar verecek. Önce episodes/ klasörünü kontrol et (son bölüm: 048_hatay).
- Bilinmiyor, TEK1'e sor: #45–#48 videoları yayınlandı mı?

## 12. DERSLER (kendi hatalarım; 30.10.2026 gözden geçirme)
- Görsel önermeden önce fotoğrafı AÇ (pano). Künyeye bakıp önerdim; düğün fotoğrafında Atatürk vardı.
- Yorum taslağı: TEK taslak ver, soru yok (dolaylı da yok: "merak ettik", "paylaşırsanız seviniriz"). Göstermeden önce kontrol listesinden geçir.
- Zernio gönderimi: cevapları TEK TEK sırayla gönder, toplu/paralel gönderme.
- Yorum taraması: sınırı "son kanal cevabının saati" değil "taramanın yapıldığı saat" olarak deftere yaz; yeni taramada önceki sınıra yakın, işaretlenmemiş yorumları da kontrol et (Devrim'de mstfksk28 kaçtı).
- Senaryo: hikâyenin SONUCU olmalı ("paralar ne oldu?"). Sonuçsuz bırakma; kaynaklarda sonucu ara.
- Senaryo dili: rapor gibi değil konuşur gibi, geçişlerde soru ("Peki, bankerler ne yapıyordu?"). TEK1'in yazdığı akış daha iyiydi.
- İzleyiciyi karıştıran teknik ayrıntıyı (ör. mevduat sertifikası kapsamı) sona koyma; net sonuç cümlesi kullan.
- Aşırı temkin de hata: "kaçtı" için elimdeki kaynakları (Çukurova, Wikipedia, Sözcü) taramadan "çıktı" dedim. Karar vermeden önce mevcut kaynaklarda ara.
- Diğer yapay zekâların (GPT, Manus) söylediği kaynak değildir; kaynağı kendim açıp okurum.
- Uzun metin yazarken karakterleri kontrol et (beceri metnine Kiril harf karıştı).
- Videodan önce süreyi hesapla: hedef ≤60 sn deneme; ~2,3 kelime/sn.
- SENARYO DİLİ (TEK1 iki kez GPT'ye düzeltti): Rapor gibi resmî yazma. Önce bilgileri doğrula, sonra metni "bir arkadaşa anlatır gibi" yeniden yaz: kısa cümle, günlük dil, bugünden başlayan açılış ("Bugün markette…"). Zorlama soru sorma ("büyükleriniz tuzu nereden alırdı" gibi); kapanış sorusu videonun en şaşırtıcı bilgisine bağlansın. Zor birimi benzetmeyle aç (okka → "bir kilo tuz için beş on kilo buğday").
- GÖRSEL TEKRARI: Görsel seçmeden önce `grep` ile episodes/ içinde daha önce kullanılmış mı kontrol et (Tuz'da Lakaplar videosunun köylü fotoğrafı tekrar kullanıldı).
- KARARTMA YOK: Küçük/düşük çözünürlüklü görsellerde arka planı KOYULAŞTIRMA (brightness düşürme yok); sadece hafif bulanık bırak, görseli tam genişliğe büyüt. Açılış karesi asla koyu görünmesin.
- GÖNDERİM: `git push HEAD:main` bekleyen TÜM kayıtları gönderir. Push'tan önce `git log origin/main..HEAD` ile bak; onaylanmamış kayıt varsa önce onay al.
- Kareleri kontrol ederken sadece "küçük pencere" değil, parlaklık/karartma da raporla.
