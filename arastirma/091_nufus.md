# 091 Nüfus: "Ölen kardeşinin kimliğiyle yaşayanlar" (Claude raporu, Hesap 2, 15.11.2026)

## ÖZET (en üstte)
- GÖRSEL: kullanılabilir siyah-beyaz 5 (SMVK 1905-1907 köy/kervan/saban/fırın; DGPI Ballıkpınar köylüleri 1930'lar) | TEK1 onayına bağlı 9 (SMVK 1960'lar renkli köy fotoğrafı 6 → siyah-beyaza çevrilecek: bebekli anneler 4, köy kadınları, köy çocukları; renkli harita 2; kimlik cüzdanı 1) | erişilemeyen LOC 12 (Cloudflare) | kontrol.py gorsel: 20 SMVK adayı 0 hata | gereken ~17 (89 sn / 5 sn). Eksik ~3.
- Eksik sahneler: eski köy mezarlığı, nüfus kütüğü/defter, mahkeme/adliye (eski), 1934 taraması.
- DOĞRULAMA: 8 iddia, 8'i 2+ kaynakla doğrulandı (mahkeme örnekleri karar metninin kendisi + ikinci kayıt). Kaynak sayısı 9. Tek kaynaklı cümle yok.
- KONU: TEK1 fikri "Yaşarsa nüfusa yazdırırız"ın belgelenebilen hâli. "Bilerek geç yazdırma" iddiası akademik kaynakta bulunamadı; belgelenen hikâye: bebek ölümü bildirilmez, sonraki çocuk ölen kardeşin kaydıyla yaşar (saklı nüfus).
- DİZİN: #28 "1 Ocak, 1 Temmuz" ile örtüşme yok (git grep "saklı nüfus|ölen kardeş": 0 sonuç).

## Yeni kaynaklar (saklı nüfus; hepsini ben okudum)
A. Anayasa Mahkemesi, Başvuru 2013/2414: 1970 Adana doğumlu başvurucu, 1963'te doğup aynı yıl ölen ağabeyi "L."nin kaydıyla yaşadı; saklı nüfus talebi idari yola ait.
B. Resmî Gazete 01.12.2011, Yargıtay 18. HD kararı (Midyat): Miray, doğumundan önce 28.11.1959'da ölen ablası Meryem'in (d. 08.01.1956) kaydını kullandı.
C. Yargıtay 18. HD 2011/208 E. (avukat sitesinde alıntı): 18.04.1971 doğumlu, 2-3 aylıkken ölen ağabeyinin kaydı, kayıtta 18.04.1967 (4 yaş büyük).
D. Yargıtay 2. HD 2021/5971 (benzer olay).
E. Nüfus Hizmetleri Uygulama Yönetmeliği 2006/11081 m.35(4)(ç): "Kendisinden önce doğup ölen kardeşinin kimliğini kullandığının iddia edilmesi"; m.73: hastane/defin/okul kayıtlarıyla ispat.
F. Nüfus Hizmetleri Uygulama Yönetmeliği 2020 m.4(jj) saklı nüfus tanımı, m.17 valilik/kaymakamlık başvurusu.
G. NVİ 2021 açıklaması (saklı nüfus başvurusu).
H. TÜİK ve NAS raporu: doğup kısa sürede ölen bebeklerin doğum ve ölümü kayda geçmeyebilir.

## Senaryo (s91b.txt; kontrol.py metin: 0 hata, 1 uyarı, ~89 sn)
(sohbette verildi)

## Kaynaklar (okuma durumu, eski taslaktan; 2 ve 3 kullanılıyor)
1. Torun & Tumen, The empirical content of season-of-birth effects, Demographic Research 37/57, 2017 (ben okudum, ilgili bölümler): nüfusun ~%20'si Ocak doğumlu; 60+ yaşta ~%35; kışın köyden gidilemez, muhtar kış doğumlarını baharda topluca bildirir, 1 Ocak yazılır; bugün hastane belgesi şart.
2. Fevzi Çakmak, 1934 Yılı Nüfus Taraması, Turkish Studies 8/7, 2013 (ben okudum, ilgili bölümler): 15.640.019 kayıtlı nüfusa karşı 2.504.289 gizli doğum, 1.532.959 gizli ölüm, 669.784 gizli evlenme; muhtar defterleri, memurlar halkın ayağına; 2576 sayılı Gizli Nüfusların Yazımı Hakkında Kanun (5.7.1934); Medeni Kanun: doğum 1 ay içinde bildirilir.
3. TBMM Zabıt Ceridesi, Devre 4, Cilt 25 (1934), 2576 sayılı kanunun süre uzatma lâyihası (birincil, arama özetinden okudum): 15 Ekim 1934'e kadar 2.865.216 gizli doğum, 1.726.701 gizli ölüm, 890.593 gizli evlenme yazıldı.
4. Keskin, Çağatay, Türkyılmaz, ADNKS'deki yaş yığılmaları, Ahi Evran Üni. SBE Dergisi 10/2, 2024 (özet okudum): eski kuşaklarda yaşlar çoğunlukla yanlış kaydedilmiş.
5. Keskin & Çavlin, Unregistered Births of Adolescent Mothers in Turkey, Comparative Population Studies 45, 2020 (özet ve yöntem okudum): kanuna göre doğum 30 gün içinde kaydedilir.
6. TÜİK, Vital Statistics sunumu (UNESCAP 2023) (okudum): 5490 sayılı kanun, doğum 30 gün içinde; hastanede doğum belgesi verilir.
7. Sağlık Bakanlığı, Türkiye'de Bebek Ölümleri Durum Raporu 2021 (okudum): 1960'ların ortasında bebek ölüm hızı binde 163 (senaryoda kullanılmadı).

## Senaryo taslağı (kontrol.py metin: 0 hata, 0 uyarı, ~74 sn)
(sohbette verildi; s91.txt)

## Görsel adayları
- Kullanılabilir: Residents of Ballıkpınar Village, movie screening, 1930s (DGPI, Commons) [tekrar taraması yapılacak]
- Onaya bağlı: T.C. Nüfus Hüviyet Cüzdanı.JPG (renkli, CC BY-SA 3.0); 1927 ve 1935 Genel Nüfus Sayımı yoğunluk haritaları (renkli harita, CC BY-SA 4.0)
- LOC (erişilemedi): 2010648359 Sekili'de karda yalınayak köylü kızlar 1921; 2010647214 Ceritmüminli köy çocukları 1920; 2010647238 Alaca köy meydanı 1921; 2010648447 Cerit Müminli köylüleri; 2010647237 Yozgat yakını; 2010647236 Sekili; 2010647240 Çorum; 2016651973 Zıpkıcı köyü anneler ve bebekler 1964; 2016651976 Ceylanköy kuyu 1962; 2010648360 köy misafirhanesi; 2010648363 jandarmalar; 2010647229 han
- SMVK (CC0, erişim için collections.smvk.se izni gerek): Trabzon-Erzurum arası Türk köyü 1905; Konya kuzeyi kürklü kervancı 1907; Kapadokya köy ve çocuk fotoğrafları (0884 serisi); Yörükler kış kampı
