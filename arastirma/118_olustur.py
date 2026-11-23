import json,sys
sys.path.insert(0,'arastirma'); from importlib import import_module; kirp=import_module('118_kirp').kirp
w=json.load(open('/tmp/w118.json'))
tok=[]
for a,b,t in w:
    if t.startswith("'") and tok: tok[-1]=[tok[-1][0],b,tok[-1][2]+t]
    elif t.startswith("Sanremo"): m=(a+b)/2; tok+= [[a,m,"San"],[m,b,"Remo"+t[7:]]]
    else: tok.append([a,b,t])
D=72.2
S=[ # bitiş, say, caption, görsel, başlık, kaynak, lisans, görünen
(6.4,"[serious] Vahdettin... Osmanlının son padişahı, başkentinden bir İngiliz zırhlısıyla ayrıldı.","Vahdettin... Osmanlı'nın son padişahı, başkentinden bir İngiliz zırhlısıyla ayrıldı.","portre_sebah","Sultan Vahdettin (VI. Mehmed), Sébah & Joaillier","Sébah & Joaillier, Commons","Kamu malı","Oturan, nişanlı ve fesli Sultan Vahdettin portresi"),
(11.4,"[short pause] Peki, bu bir kaçış mıydı, yoksa başka çaresi mi kalmamıştı? [short pause]","Peki, bu bir kaçış mıydı, yoksa başka çaresi mi kalmamıştı?","yakin_portre","Sultan Vahdettin","Bain News Service, Commons","Kamu malı","Gözlüklü, fesli, askerî ceketli Vahdettin yakın portresi"),
(15.9,"[calm] 1 Kasım 1922de Meclis saltanatı kaldırdı.","1 Kasım 1922'de Meclis saltanatı kaldırdı.","tbmm_dua","Ankara, Büyük Millet Meclisi önünde dua","Commons","Kamu malı","Meclis binası önünde ellerini açıp dua eden kalabalık, sarıklı ve kalpaklı kişiler"),
(20.45,"Vahdettinin elinde sadece halifelik unvanı kaldı.","Vahdettin'in elinde sadece halifelik unvanı kaldı.","dua","Sultan Vahdettin dua ederken","Commons","Kamu malı","Vahdettin ve yanındakiler ellerini açmış dua ediyor, yanında sarıklı din adamları"),
(25.0,"16 Kasımda İstanbuldaki İngiliz komutanı General Haringtona bir mektup yazdı:","16 Kasım'da İstanbul'daki İngiliz komutanı General Harington'a bir mektup yazdı:","harington","General Charles Harington","Bassano Ltd, Commons","Kamu malı","Üniformalı, şapkalı, oturan İngiliz General Harington"),
(32.1,"\"İstanbulda hayatımı tehlikede görüyorum. İngiltereye sığınıyor, beni hemen başka bir yere götürmenizi istiyorum.\"","\"İstanbul'da hayatımı tehlikede görüyorum. İngiltere'ye sığınıyor, beni hemen başka bir yere götürmenizi istiyorum.\"","portre_bnf","Sultan Vahdettin, Agence Rol","Agence Rol, BnF Gallica, Commons","Kamu malı","Fesli, takım elbiseli Vahdettin profil portresi"),
(36.6,"[serious] Ertesi sabah Yıldız Sarayının arka kapısından sessizce çıktı.","Ertesi sabah Yıldız Sarayı'nın arka kapısından sessizce çıktı.","yildiz_cami_cikis","Yıldız, Vahdettin Hamidiye Camii'nden çıkarken","Commons","Kamu malı","Yıldız'da cami kapısından çıkan padişah ve onu selamlayan askerler"),
(41.1,"Ambulans ve otomobillerle Tophaneye götürüldü, oradan bir motorla","Ambulans ve otomobillerle Tophane'ye götürüldü. Oradan bir motorla","tophane_panorama","Tophane ve Boğaz, Guillaume Berggren, 1880'ler","Guillaume Berggren, Commons","Kamu malı","Tophane semti evleri, kıyı ve Boğaz, uzakta camiler"),
(45.6,"Malaya zırhlısına geçti. Gemi onu Maltaya götürdü.","Malaya zırhlısına geçti. Gemi onu Malta'ya götürdü.","malta_varis","Vahdettin Malta'ya varıyor, Kasım 1922","Grand Studio Malta, Commons","Kamu malı","Bastonlu Vahdettin, yanında fesli adamlarla Malta'da rıhtımdan çıkıyor"),
(50.1,"Ertesi gün Meclis, Abdülmecid Efendiyi yeni halife seçti.","Ertesi gün Meclis, Abdülmecid Efendi'yi yeni halife seçti.","abdulmecid","Halife Abdülmecid Efendi","Commons","Kamu malı","Fesli, papyonlu, takım elbiseli Abdülmecid Efendi portresi"),
(56.3,"[thoughtful] Vahdettin önce Mekkeye, sonra İtalyada San Remoya gitti. Bir daha İstanbula dönemedi.","Vahdettin önce Mekke'ye, sonra İtalya'da San Remo'ya gitti. Bir daha İstanbul'a dönemedi.","gemiden_inis","Sultan Vahdettin gemiden inerken","Commons","Kamu malı","Paltolu, fesli Vahdettin bir vapurun iskelesinden iniyor"),
(60.8,"1926da San Remoda öldü ve Şama gömüldü.","1926'da San Remo'da öldü ve Şam'a gömüldü.","tekkiye_eski","Şam, Süleymaniye Külliyesi (Tekkiye)","Commons","Kamu malı","İki minareli, kubbeli Şam Süleymaniye Külliyesi ve önündeki havuz"),
(65.3,"[calm] Sizce son padişah gitmek zorunda mıydı, yoksa kaçtı mı? [short pause]","Sizce son padişah gitmek zorunda mıydı, yoksa kaçtı mı?","fayton","Sultan Vahdettin faytonda","Commons","Kamu malı","Faytonda oturan askerî kıyafetli Vahdettin, yanında fesli görevliler"),
(D,"Düşüncelerinizi yorumlarda paylaşın. Kaynaklar video açıklamasında. Beğenmeyi ve takip etmeyi lütfen unutmayalım.","Düşüncelerinizi yorumlarda paylaşın. Kaynaklar video açıklamasında. Beğenmeyi ve takip etmeyi lütfen unutmayalım.","malaya_iwm","HMS Malaya zırhlısı","Ernest Hopkins, IWM, Commons","Kamu malı","Denizde gri İngiliz zırhlısı HMS Malaya"),
]
segs=[];kes=[];bas=0.0;ti=0
for bit,say,cap,f,bs,kay,lis,gor in S:
    cw=cap.split(); n=len(cw)
    mine=tok[ti:ti+n]; ti+=n
    assert all(x[0]<bit+0.05 for x in mine),(cap,mine[-1])
    bol=[];i=0
    while i<n:
        m=min(4,n-i)
        if n-i-m==1: m+=1
        st=mine[i][0] if i else min(bas,mine[0][0])
        end=mine[i+m][0] if i+m<n else min(bit,mine[-1][1]+0.6)
        bol.append({"start":round(st,2),"end":round(end,2),"n":m});i+=m
    segs.append({"say":say,"caption":cap,"key":[],"scene":"photo","gorunen":gor,"bolumler":bol,
      "image":{"local":f"assets/belgeler/118_{f}.jpg","fit":"doldur","hiz":1.0,"kirp":kirp(f),"baslik":bs,"kaynak":kay,"lisans":lis}})
    kes.append([[bas,bit]]);bas=bit
assert ti==len(tok),(ti,len(tok),tok[ti:])
ep={"series":"Sıradan Değil","voice":"ana","takip_cagrisi":False,"episode":118,"slug":"vahdettin","title":"Son padişah kaçtı mı?","youtube_title":"","youtube_description":"",
"sources":["Çelik 2016, ÇTTAD","Mengeş 2024, Atatürk Yolu","Akman 2019","Küçük 2003, TDV İA"],"acilis":"Son padişah\nkaçtı mı?",
"dis_ses":{"file":"assets/ses/118_vahdettin.mp3","kesimler":kes},"surum":1,"segments":segs}
json.dump(ep,open('episodes/118_vahdettin.json','w'),ensure_ascii=False,indent=1)
for s in segs: print(s['bolumler'][0]['start'],s['bolumler'][-1]['end'],s['image']['local'][19:])
