import json,re
from PIL import Image
w0=json.load(open('/tmp/w122.json'))
w=[];orig=[]
for i,(a,b,t) in enumerate(w0):
    if t.startswith("'") and w: w[-1]=[w[-1][0],b,w[-1][2]+t]
    else: w.append([a,b,t]); orig.append(i)
idx={o:n for n,o in enumerate(orig)}
EK=[x[2] for x in w]
EK=[{'fakirse':'fakir','çoğuysa':'çoğu'}.get(e,e) for e in EK]
# "fakirse" -> "fakir ise" tek kelimede: ekranda "fakirse" kalsın (ses böyle)
EK=[x[2] for x in w]
OT={"tekrar":"TEK1 26.11 (eski bölüm fotoğrafları 1,3,4,5,6,7,8 kullanılsın dedi)"}
K={
'carsi_1880':('assets/belgeler/120_carsi_1880.jpg',"İstanbul çarşısı, 1880'ler","Catsimpoolas, DPLA, Commons","Kamu malı","Üstü asma kaplı çarşı sokağı, dükkânlar ve oturan esnaf",(.5,.46),OT),
'amasya_koylu':('assets/belgeler/102_amasya_koylu.jpg',"Amasya'da köylüler, 1904-1907","Guillaume de Jerphanion, Archives Jésuites, Commons","CC BY-SA 4.0","Tarlada çalışan köylüler, arkada tepeler",(.5,.45),OT),
'hamal_berggren':('assets/belgeler/122_hamal_berggren_1875.jpg',"Sırtında sandık taşıyan hamal, İstanbul, 1875 civarı","G. Berggren, Digital Commonwealth, Commons","Kamu malı","Sırtında büyük sandık taşıyan, eğilmiş bir hamal",(.45,.5),None),
'galata_hamal':('assets/belgeler/110_galata_hamal.jpg',"Galata Köprüsü'nde hamallar, 1923","Library of Congress, Commons","Kamu malı","Köprüde sırtında küfe taşıyan hamallar ve yürüyen insanlar",(.5,.5),OT),
'esnaf_dukkani':('assets/belgeler/120_esnaf_dukkani_sebah.jpg',"Osmanlı esnafı dükkânı önünde, 19. yüzyıl sonu","Sébah & Joaillier, LOC, Commons","Kamu malı","Dükkânının önünde oturan ve ayakta duran sarıklı esnaf, raflarda mallar",(.52,.5),OT),
'karakol':('assets/belgeler/113_karakol.jpg',"Selamsız Karakolu, İstanbul, 1880-1893","Abdullah Frères, II. Abdülhamid albümleri, LOC","Kamu malı","İki katlı bir karakol binası ve önünde budanmış ağaçlar",(.45,.5),OT),
'mahkum':('assets/belgeler/122_zincirli_kurekciler_gemide.jpg',"Türk mahkûmlar gemide, 1878 (gravür)","The Graphic, Wellcome V0041227, Commons","Kamu malı","Gemi güvertesinde oturan mahkûmlar ve başlarında bekçi (gravür)",(.45,.5),None),
'tersane':('assets/belgeler/122_tersane_pardoe_gravur.jpg',"Pera'dan Tersane (W. H. Bartlett gravürü, 1838)","Julia Pardoe, The Beauties of the Bosphorus, Commons","Kamu malı","Haliç kıyısında tersane, gemiler ve servi ağaçları (gravür)",(.55,.5),None),
'kadiasker':('assets/belgeler/122_kadiasker_gravur.jpg',"Kadıasker, Osmanlı yargıcı (gravür, 19. yüzyıl başı)","Travels in Turkey, Asia Minor, Syria..., Commons","Kamu malı","Kürk kaftanlı, sarıklı bir Osmanlı yargıcı ayakta (gravür)",(.5,.5),None),
'kazasker':('assets/belgeler/122_kazasker_gravur_metropolitan.jpg',"Kazasker, ordunun yüksek yargıcı (gravür, 18. yüzyıl)","Le Cadi-leskier, Metropolitan Museum DP887282, Commons","CC0","Büyük kavuklu, düşünceli duran bir yargıç (gravür)",(.5,.5),None),
'dukkan2':('assets/belgeler/066_dukkan2.jpg',"İstanbul'da bir çarşı dükkânı, 20. yüzyıl başı","Underwood & Underwood, Library of Congress","Kamu malı","Çarşıda dükkân önünde duran esnaf ve köpekler",(.5,.5),OT),
}
S=[(0,'carsi_1880'),(17,'kadiasker'),(28,'amasya_koylu'),(48,'hamal_berggren'),(62,'galata_hamal'),(89,'esnaf_dukkani'),(103,'kazasker'),(113,'karakol'),(127,'mahkum'),(137,'tersane'),(152,'dukkan2')]
S=[(idx[o],f) for o,f in S]
D=94.67
YR={'carsi_1880':(0,.92),'amasya_koylu':(.03,.84),'karakol':(.17,.83)}
def kirp(f):
    im=Image.open(K[f][0]);W,H=im.size;cx,cy=K[f][5]
    if f in YR:
        y0,y1=YR[f]; w_=(y1-y0)*H*9/16/W; x0=min(max(cx-w_/2,0),1-w_); return [round(x0,3),y0,round(x0+w_,3),y1]
    w_=H*9/16/W
    if w_<=1:
        x0=min(max(cx-w_/2,0),1-w_); return [round(x0,3),0,round(x0+w_,3),1]
    h=W*16/9/H; y0=min(max(cy-h/2,0),1-h); return [0,round(y0,3),1,round(y0+h,3)]
segs=[];kes=[]
for j,(i0,f) in enumerate(S):
    i1=S[j+1][0] if j+1<len(S) else len(w)
    bas=0.0 if j==0 else w[i0][0]; bit=w[i1][0] if i1<len(w) else D
    bol=[];i=i0
    while i<i1:
        m=min(4,i1-i)
        if i1-i-m==1: m+=1
        st=w[i][0] if i>i0 else bas
        en=w[i+m][0] if i+m<i1 else min(bit,w[i1-1][1]+0.6)
        bol.append({"start":round(st,2),"end":round(en,2),"n":m});i+=m
    loc,bs,kay,lis,gor,_,on=K[f]
    cap=' '.join(EK[i0:i1])
    segs.append({"say":cap.replace("'",""),"caption":cap,"key":[],"scene":"photo","gorunen":gor,"bolumler":bol,
      "image":{"local":loc,"fit":"doldur","hiz":(0.5 if "gravür" in bs else 1.0),"kirp":kirp(f),"baslik":bs,"kaynak":kay,"lisans":lis,**({"onay":on} if on else {})}})
    kes.append([[round(bas,2),round(bit,2)]])
ep={"series":"Sıradan Değil","voice":"ana","takip_cagrisi":False,"episode":122,"slug":"hirsiz","title":"Osmanlı'da hırsızın eli kesilir miydi?","youtube_title":"","youtube_description":"",
"sources":["Baytimur 2018","Baba 2013","Osmanağaoğlu-Karahasanoğlu","Koç 2019","Okur Gümrükçüoğlu 2024","Yücetürk 2024"],"acilis":"Hırsızın eli\ngerçekten kesilir miydi?",
"dis_ses":{"file":"assets/ses/122_hirsiz.mp3","kesimler":kes},"surum":3,"segments":segs}
json.dump(ep,open('episodes/122_hirsiz.json','w'),ensure_ascii=False,indent=1)
for s,k in zip(segs,kes): print(k[0], round(k[0][1]-k[0][0],1), s['image']['local'][20:], s['image']['kirp'], '|', s['caption'][:50])
