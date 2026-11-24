import json,sys,re
sys.path.insert(0,'arastirma'); from importlib import import_module; kirp=import_module('120_kirp').kirp
w=json.load(open('/tmp/w120.json'))
EKRAN=("Ekmeği eksik çıkaran fırıncının boynuna kocaman bir tahta geçirildi. Ekmekleri de o tahtaya asıldı. "
"Peki, Osmanlı'da hile yapan esnafa neden böyle bir ceza veriliyordu? "
"Bu cezanın adı teşhirdi. Yani suçluyu halkın önünde rezil etmek. Amaç, herkese ibret olması ve hilenin tekrarlanmamasıydı. "
"Kanunnamelerde hileli esnafın cezası tek tek yazılıydı. Yoğurda ya da sirkeye su katan teşhir edilir, ya da başına tahta külah geçirilirdi. "
"Terazide eksik tartanın boynuna tahta bir halka geçirilip gezdirilmesi bile kanunda vardı. "
"Kayıtlarda gerçek örnekler de var. Eksik ekmek çıkaran fırıncıların ekmekleri boyunlarına asıldı, yüzlerine mürekkep sürüldü. İnsanları aldatanlar eşeğe bindirilip çarşıda dolaştırıldı. "
"Yalancı şahit de kurtulamazdı. Tanındığı çarşıda ilan edilirdi: \"Bu adam yalancı şahittir, ondan sakının.\" "
"Sizce bugün hile yapan esnafa böyle bir ceza verilse, hile biter miydi? "
"Düşüncelerinizi yorumlarda paylaşın. Kaynaklar video açıklamasında. Beğenmeyi ve takip etmeyi lütfen unutmayalım.").split()
assert len(EKRAN)==len(w),(len(EKRAN),len(w))
SES=open('arastirma/120_teshir_senaryo.txt').read().split('\n')
K={
'firinci_ceza_gravur':("Fiyatı şişiren fırıncının cezası (gravür)","Commons: Punishment of a price-gouging baker.jpg","Kamu malı","Boynuna tahta geçirilmiş, tahtaya ekmekler asılmış sarıklı fırıncı (gravür)"),
'esnaf_dukkani_sebah':("Osmanlı esnafı dükkânı önünde, Sébah & Joaillier","Sébah & Joaillier, LOC, Commons","Kamu malı","Dükkânının önünde oturan ve ayakta duran sarıklı esnaf, raflarda mallar"),
'sokak_kalabalik_gravur':("İstanbul'da bir çarşı sokağı (gravür, 1897)","The Innocents Abroad (1897), Internet Archive, Commons","Telif kısıtlaması yok","Kalabalık çarşı sokağı, çarşaflı kadınlar, tablalı satıcı (gravür)"),
'carsi_1880':("İstanbul çarşısı, 1880'ler","Catsimpoolas, DPLA, Commons","Kamu malı","Üstü asma kaplı çarşı sokağı, dükkânlar ve oturan esnaf"),
'divan_dohsson':("Osmanlı'da resmî daire, d'Ohsson 1790 (gravür)","Mouradgea d'Ohsson, Tableau général, Commons","Kamu malı","Divan sedirlerinde oturan kalabalık memurlar, büyük salon (gravür)"),
'su_saticisi':("Seyyar satıcı, Sébah & Joaillier","Sébah & Joaillier, DPLA, Commons","Kamu malı","Sırtında yük taşıyan, elinde kaplar olan seyyar satıcı"),
'pabuccu_carsi':("Çarşıda pabuççu dükkânı","Catsimpoolas, DPLA, Commons","Kamu malı","Duvarı pabuçlarla dolu dükkânda oturan iki esnaf"),
'kapalicarsi_gravur1':("Kapalıçarşı, pamuk çarşısı (gravür, 1878)","De Amicis, Costantinopoli (1878), Commons","Kamu malı","Kemerli uzun çarşı koridoru, yük taşıyan insanlar (gravür)"),
'pazar_bauer':("Cami önünde pazar, Marius Bauer (gravür)","Marius Bauer, Commons","Kamu malı","Cami avlusunda yere serili pazar, kalabalık (gravür)"),
'kapalicarsi_gravur3':("Kapalıçarşı'da bir dükkân (gravür, 1878)","De Amicis, Costantinopoli (1878), Commons","Kamu malı","Sedefli eşyalar arasında oturan dükkân sahibi ve müşteri (gravür)"),
'kapalicarsi_gravur4':("Kapalıçarşı'da kumaş satıcısı (gravür, 1878)","De Amicis, Costantinopoli (1878), Commons","Kamu malı","Perdeli dükkânda kumaş seçen çarşaflı kadınlar (gravür)"),
'kapalicarsi_gravur2':("Kapalıçarşı'da kumaşçı (gravür, 1878)","De Amicis, Costantinopoli (1878), Commons","Kamu malı","Dükkânında uzanmış nargile içen esnaf (gravür)"),
}
S=[(0,'firinci_ceza_gravur'),(14,'esnaf_dukkani_sebah'),(24,'sokak_kalabalik_gravur'),(34,'carsi_1880'),(41,'divan_dohsson'),(49,'su_saticisi'),(62,'pabuccu_carsi'),(74,'kapalicarsi_gravur1'),(89,'pazar_bauer'),(99,'kapalicarsi_gravur3'),(109,'kapalicarsi_gravur4'),(121,'kapalicarsi_gravur2')]
D=71.47
# ses metninden sahne "say" metni: ses kelimelerini ekran kelime sayısına göre böl
ses_tok=re.sub(r'\[[a-z ]+\]','',' '.join(SES)).split()
tags_full=' '.join(SES).split()
segs=[];kes=[];
for j,(i0,f) in enumerate(S):
    i1=S[j+1][0] if j+1<len(S) else len(w)
    bas=0.0 if j==0 else w[i0][0]; bit=w[i1][0] if i1<len(w) else D
    cap=' '.join(EKRAN[i0:i1])
    bol=[];i=i0
    while i<i1:
        m=min(4,i1-i)
        if i1-i-m==1: m+=1
        st=w[i][0] if i>i0 else bas
        en=w[i+m][0] if i+m<i1 else min(bit,w[i1-1][1]+0.6)
        bol.append({"start":round(st,2),"end":round(en,2),"n":m});i+=m
    bs,kay,lis,gor=K[f]
    segs.append({"say":' '.join(ses_tok[i0:i1]),"caption":cap,"key":[],"scene":"photo","gorunen":gor,"bolumler":bol,
      "image":{"local":f"assets/belgeler/120_{f}.jpg","fit":"doldur","hiz":(0.7 if ("gravur" in f or "bauer" in f or "dohsson" in f) else 1.0),"kirp":kirp(f),"baslik":bs,"kaynak":kay,"lisans":lis}})
    kes.append([[round(bas,2),round(bit,2)]])
ep={"series":"Sıradan Değil","voice":"ana","takip_cagrisi":False,"episode":120,"slug":"teshir","title":"Hileli esnafın cezası: teşhir","youtube_title":"","youtube_description":"",
"sources":["Kılınç 2015","Koç 2019","Şahin 2022","Erdoğan 2024","Artukoğlu 2025","Kılınç 2007"],"acilis":"Hileli esnafa\nne yapılırdı?",
"dis_ses":{"file":"assets/ses/120_teshir.mp3","kesimler":kes},"surum":1,"segments":segs}
json.dump(ep,open('episodes/120_teshir.json','w'),ensure_ascii=False,indent=1)
for s,k in zip(segs,kes): print(k[0], round(k[0][1]-k[0][0],2), s['image']['local'][20:], '|', s['caption'][:50])
