import json,re
w=json.load(open('/tmp/w116.json'))
tok=[]
for a,b,t in w:
    if t.startswith("'") and tok: tok[-1]=[tok[-1][0],b,tok[-1][2]+t]
    else: tok.append([a,b,t])
D=82.68
K="Commons, kamu malı"
P=lambda f,t,y: {"local":f"assets/belgeler/116_{f}.jpg","fit":"doldur","hiz":y,"kirp":None,"baslik":t}
S=[ # bitiş sn, say, caption, görsel, kırp, hız, başlık, kaynak/lisans, görünen
(6.5,"[serious] Osmanlıdan kalan borcu Türkiye üstlendi. [short pause] Peki bu borcun kapanması kaç yıl sürdü?","Osmanlı'dan kalan borcu Türkiye üstlendi. Peki bu borcun kapanması kaç yıl sürdü?","abdulaziz2",[0.03,0,0.88,1],1.0,"Sultan Abdülaziz, 1860'lar","W. & D. Downey, Commons","Kamu malı","Ayakta duran Osmanlı padişahı Abdülaziz, fesli, uzun ceketli"),
(12.9,"[short pause] Tam yüz yıl. [calm] Her şey 1854 yılında, Kırım Savaşı sırasında başladı.","Tam 100 yıl. Her şey 1854 yılında, Kırım Savaşı sırasında başladı.","kirim1",[0.12,0,0.71,1],1.0,"Kırım Savaşı'nda Osmanlı askerleri, 1855","Roger Fenton, Commons","Kamu malı","Kırım Savaşı'nda tüfekli Osmanlı askerleri, yerde oturan ve ayakta duranlar"),
(18.1,"Savaşın masrafları büyüyünce Osmanlı, ilk kez Avrupadan borç aldı.","Savaşın masrafları büyüyünce Osmanlı, ilk kez Avrupa'dan borç aldı.","tahvil_bagdat",[0.135,0,0.865,1],0.5,"Osmanlı devlet borcu tahvili (Bağdat Demiryolu)","Commons","Kamu malı","Osmanlı İmparatorluğu borç tahvili, üstte tuğra ve Devlet-i Aliyye-i Osmaniyye yazısı"),
(23.0,"Ancak ardından borç üstüne borç geldi.","Ancak ardından borç üstüne borç geldi.","abdulaziz_gravur",[0.268,0.08,0.732,0.62],1.0,"Sultan Abdülaziz, gravür","Rijksmuseum, Commons","CC0","Üniformalı, nişanlı Sultan Abdülaziz gravür portresi"),
(28.0,"1875te devlet ödemelerini yapamadı ve iflasını resmen ilan etti.","1875'te devlet ödemelerini yapamadı ve iflasını resmen ilan etti.","abdulaziz",[0.135,0,0.862,1],1.0,"Sultan Abdülaziz, Abdullah Frères","Abdullah Frères, Commons","Kamu malı","Oturan Sultan Abdülaziz, elleri kavuşturulmuş, göğsünde nişanlar"),
(33.5,"[serious] 1881de Düyun-u Umumiye, yani Genel Borçlar İdaresi kuruldu.","1881'de Düyun-u Umumiye, yani Genel Borçlar İdaresi kuruldu.","tahvil_anadolu",[0.07,0,0.927,1],0.5,"Anadolu Demiryolu tahvili, 1893","EDHAC e.V., Commons","Kamu malı","Osmanlı Anadolu Demiryolu Şirketi tahvili, 1893"),
(38.7,"Tütün, tuz ve ipek gibi gelirler artık alacaklıların kontrolündeydi.","Tütün, tuz ve ipek gibi gelirler artık alacaklıların kontrolündeydi.","tahvil_selanik",[0.18,0,0.589,1],0.5,"Selanik-İstanbul demiryolu tahvili, 1893","Commons","Kamu malı","Selanik-İstanbul demiryolu tahvili, Obligation de 500 Francs yazısı"),
(46.6,"Osmanlı yıkıldı ama borçlar bitmedi. Lozanda bu borçlar, Osmanlıdan ayrılan ülkeler arasında paylaştırıldı.","Osmanlı yıkıldı ama borçlar bitmedi. Lozan'da bu borçlar, Osmanlı'dan ayrılan ülkeler arasında paylaştırıldı.","tahvil1933",[0.42,0,0.858,1],0.5,"Paylaştırılmış Osmanlı borcu makbuzu, 1933","Commons","Kamu malı","Eski Osmanlı İmparatorluğunun paylaştırılmış borcu idaresinin 1933 tarihli tahvil makbuzu"),
(51.3,"En büyük payı, yaklaşık yüzde altmış beşini Türkiye üstlendi.","En büyük payı, yaklaşık yüzde 65'ini Türkiye üstlendi.","meclis1928",[0.32,0,0.671,1],0.5,"TBMM binası, 1928 (Servet-i Fünun)","Servet-i Fünun, Commons","Kamu malı","1928 Türkiye Büyük Millet Meclisi binasında döşenmiş salon"),
(57.9,"[thoughtful] 1929 Dünya Ekonomik Buhranıyla ödemeler zorlaştı ve borç yeniden görüşüldü.","1929 Dünya Ekonomik Buhranı'yla ödemeler zorlaştı ve borç yeniden görüşüldü.","ziraat_ankara1",[0.05,0,0.801,1],1.0,"Ankara, Bankalar Caddesi, Ziraat Bankası, 1930'lar","Basın Yayın Genel Müdürlüğü, Commons","Bilinen telif kısıtlaması yok","1930'larda Ankara'da Ziraat Bankası binası ve demir kapısı"),
(63.0,"Ve 25 Mayıs 1954te son ödeme yapıldı.","Ve 25 Mayıs 1954'te son ödeme yapıldı.","istanbul1950",[0.12,0,0.494,1],1.0,"İstanbul, 1950'ler","Harry Pot, Anefo, Commons","CC0","1950'lerde İstanbul'da sahil yolunda bir otomobil, arkada cami"),
(68.1,"İlk borcun alınmasından tam yüz yıl sonra, Osmanlının borcu tamamen kapandı.","İlk borcun alınmasından tam 100 yıl sonra, Osmanlı'nın borcu tamamen kapandı.","kirim2",[0.28,0,0.723,1],1.0,"Kırım Savaşı, 1855 (ilk borcun alındığı savaş)","Roger Fenton, Commons","Kamu malı","Kırım Savaşı'nda çadırların önünde toplanmış askerler"),
(75.0,"[calm] Peki, bir imparatorluktan kalan borcun yeni bir devlet tarafından ödendiğini daha önce biliyor muydunuz? [short pause]","Peki, bir imparatorluktan kalan borcun yeni bir devlet tarafından ödendiğini daha önce biliyor muydunuz?","kirim4",[0.25,0,0.65,1],1.0,"Kırım Savaşı, 1855","Commons","Kamu malı","Kırım Savaşı'nda bir binanın önünde subaylar ve askerler"),
(D,"Düşüncelerinizi yorumlarda paylaşın. Kaynaklar video açıklamasında. Beğenmeyi ve takip etmeyi lütfen unutmayalım.","Düşüncelerinizi yorumlarda paylaşın. Kaynaklar video açıklamasında. Beğenmeyi ve takip etmeyi lütfen unutmayalım.","kirim5",[0.2,0,0.815,1],1.0,"Kırım Savaşı, 1855","Roger Fenton, Commons","Kamu malı","Kırım Savaşı'nda bir evin önünde oturan ve ayakta duran subaylar"),
]
segs=[];kes=[];bas=0.0;ti=0
for bit,say,cap,f,k,hz,bs,kay,lis,gor in S:
    cw=cap.split(); n=len(cw)
    mine=tok[ti:ti+n]; ti+=n
    assert all(x[0]<bit+0.05 for x in mine),(cap,mine[-1])
    bol=[];i=0;st=bas
    while i<n:
        m=min(4,n-i)
        if n-i-m==1: m+=1
        end=mine[i+m][0] if i+m<n else bit
        bol.append({"start":round(st,2),"end":round(end,2),"n":m});st=end;i+=m
    segs.append({"say":say,"caption":cap,"key":[],"scene":"photo","gorunen":gor,"bolumler":bol,
      "image":{"local":f"assets/belgeler/116_{f}.jpg","fit":"doldur","hiz":hz,"kirp":k,"baslik":bs,"kaynak":kay,"lisans":lis}})
    kes.append([[bas,bit]]);bas=bit
assert ti==len(tok),(ti,len(tok),tok[ti:])
ep={"series":"Sıradan Değil","voice":"ana","takip_cagrisi":False,"episode":116,"slug":"osmanli_borcu","title":"Osmanlı borcunu kim ödedi","youtube_title":"","youtube_description":"",
"sources":["Aysal 2013, Atatürk Yolu 53","Aşcı 2016, İTOBİAD 5/6","Dikmen 2005"],"acilis":"Osmanlı'nın borcunu\nkim ödedi?",
"dis_ses":{"file":"assets/ses/116_osmanli_borcu.mp3","kesimler":kes},"surum":2,"segments":segs}
json.dump(ep,open('episodes/116_osmanli_borcu.json','w'),ensure_ascii=False,indent=1)
for s in segs: print(s['bolumler'][0]['start'],s['bolumler'][-1]['end'],s['image']['local'][19:])
