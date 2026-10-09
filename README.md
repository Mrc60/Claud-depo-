# Sıradan Değil — Shorts üretim sistemi

Her bölüm `episodes/` klasöründe bir JSON dosyası. Sistem şunları otomatik yapar:

1. **Fotoğraflar:** Wikimedia Commons'tan sadece serbest lisanslı (kamu malı / CC) gerçek fotoğrafları indirir.
2. **Ses:** Google Cloud Chirp 3 HD Türkçe sesiyle seslendirir.
3. **Video:** 1080×1920 dikey video, kelime kelime altyazı, müzik, fotoğraf atıfları.
4. **YouTube metni:** Başlık, açıklama, kaynaklar ve fotoğraf atıfları hazır gelir.

Hiçbir şey otomatik yayınlanmaz. Video, sen indirip onaylayana kadar sadece GitHub'da durur.

---

## Kurulum (bir kez, ~15 dakika)

### A) Google ses anahtarı

1. https://console.cloud.google.com adresine gir, üstten **Yeni proje** oluştur (ör. `siradan-degil`).
2. **Faturalandırma**yı etkinleştir. Google kart ister, ancak Chirp 3 HD seslerde ayda 1 milyon karakter ücretsiz. Bu kanal ayda yaklaşık 36 bin karakter kullanır.
   Güvenlik için: Faturalandırma → **Bütçeler ve uyarılar** → 1 $'lık bir bütçe uyarısı kur.
3. Arama çubuğuna **Cloud Text-to-Speech API** yaz ve **Etkinleştir**'e bas.
4. **API'ler ve Hizmetler → Kimlik bilgileri → Kimlik bilgisi oluştur → API anahtarı**.
5. Oluşan anahtarı **kısıtla**: "API kısıtlamaları" bölümünden sadece *Cloud Text-to-Speech API*'yi seç. Anahtarı bir yere kopyala.

### B) GitHub

1. https://github.com adresinde hesap aç (yoksa).
2. **New repository** → ad: `siradan-degil` → **Private** seç → Create.
3. Bu klasördeki dosyaları yükle: **Add file → Upload files**, zip'ten çıkan her şeyi sürükle.
   > Not: `.github` klasörü bazı bilgisayarlarda gizli görünür ve yüklenmeyebilir. Yüklenmediyse
   > **Add file → Create new file** de, ad kısmına `.github/workflows/video-uret.yml` yaz ve
   > aynı isimli dosyanın içeriğini yapıştır.
4. **Settings → Secrets and variables → Actions → New repository secret**
   - Name: `GOOGLE_TTS_API_KEY`
   - Secret: A adımında kopyaladığın anahtar

## Video üretme

1. Repoda **Actions** sekmesi → solda **Video üret** → **Run workflow**.
2. Bölüm dosyası olarak `001_kolonya.json` kalsın → **Run workflow**.
3. 3-5 dakika sonra işin içine gir, en altta **Artifacts → video** → indir.
   İçinde video (`.mp4`) ve YouTube metni (`_youtube.txt`) var.

## Ayarlar

- **Ses değiştirmek:** Settings → Secrets and variables → Actions → **Variables** sekmesi →
  `TTS_VOICE` = örn. `tr-TR-Chirp3-HD-Charon` (erkek), `tr-TR-Chirp3-HD-Kore` (kadın),
  `tr-TR-Chirp3-HD-Puck`, `tr-TR-Chirp3-HD-Leda`.
- **Belirli bir fotoğraf seçmek:** Bölüm dosyasında `"image": {"query": "..."}` yerine
  `"image": {"file": "File:Tam_dosya_adı.jpg"}` yaz (Commons'taki dosya adı).
- Fotoğraf bulunamazsa o sahne kodla çizilmiş grafikle devam eder; video yine üretilir.

## Dosyalar

| Dosya | Görev |
|---|---|
| `run.py` | Hepsini sırayla çalıştırır |
| `images.py` | Wikimedia Commons fotoğrafları + lisans/atıf |
| `tts_google.py` | Google Türkçe seslendirme |
| `render.py` | Video, altyazı, müzik |
| `episodes/*.json` | Bölüm senaryoları |
| `fonts/` | Inter ve Lora yazı tipleri (SIL Open Font License) |
