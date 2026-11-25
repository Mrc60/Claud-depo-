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
K={
'lorck_serseri':("16. yüzyıl İstanbul'u (Melchior Lorck gravürü, 1576)","Melchior Lorck, Wolgerissene und geschnittene Figuren, Commons","Kamu malı","Kalkan ve mızrak taşıyan, arkası dönük bir adam; arkada evler (gravür)",(.5,.5)),
'kadiasker_gravur':("Kadıasker, Osmanlı yargıcı (gravür, 19. yüzyıl başı)","Travels in Turkey, Asia Minor, Syria..., Commons","Kamu malı","Kürk kaftanlı, sarıklı bir Osmanlı yargıcı ayakta (gravür)",(.5,.5)),
'lorck_koylu':("Köylü (Melchior Lorck gravürü, 1581)","Melchior Lorck, The Turkish Publication 1581, Commons","Kamu malı","Elinde orak tutan uzun cübbeli bir köylü (gravür)",(.5,.5)),
'beyazit_meydani':("İstanbul'da hayvan pazarı, Beyazıt (kartpostal, 1900'ler)","Marché des moutons à Seraskierat, Flickr/SALT dışı arşiv, Commons","Bilinen telif kısıtlaması yok","Meydanda koyun sürüleri ve kalabalık, arkada Seraskerlik kapısı ve kule",(.45,.5)),
'lorck_muhafiz':("Saray muhafızı (Melchior Lorck gravürü, 1576)","Melchior Lorck, Commons","Kamu malı","Sorguçlu başlıklı, yay taşıyan süslü giysili bir muhafız (gravür)",(.5,.5)),
'lorck_yuk_ati':("Yük atı (Melchior Lorck gravürü, 1576)","Melchior Lorck, British Museum 1871,0812.4638, Commons","Kamu malı","Sırtında iki büyük yük çantası olan at, arkada türbe (gravür)",(.62,.5)),
'lorck_asker':("Osmanlı askeri (Melchior Lorck gravürü, 1576)","Melchior Lorck, Commons","Kamu malı","Kılıç ve tüfek taşıyan, tüylü başlıklı bir asker (gravür)",(.5,.5)),
'kazasker_gravur_metropolitan':("Kazasker, ordunun yüksek yargıcı (gravür, 18. yüzyıl)","Le Cadi-leskier, Metropolitan Museum DP887282, Commons","CC0","Büyük kavuklu, düşünceli duran bir yargıç (gravür)",(.5,.5)),
'zincirli_kurekciler_gemide':("Türk mahkûmlar gemide, 1878 (gravür)","The Graphic, Wellcome V0041227, Commons","Kamu malı","Gemi güvertesinde oturan mahkûmlar ve başlarında bekçi (gravür)",(.45,.5)),
'tersane_pardoe_gravur':("Pera'dan Tersane (W. H. Bartlett gravürü, 1838)","Julia Pardoe, The Beauties of the Bosphorus, Commons","Kamu malı","Haliç kıyısında tersane, gemiler ve servi ağaçları (gravür)",(.55,.5)),
'lorck_sipahi_atli':("Atlı sipahi (Melchior Lorck gravürü, 1576)","Melchior Lorck, Commons","Kamu malı","Mızraklı ve yaylı, at üstünde bir sipahi (gravür)",(.5,.5)),
}
S=[(0,'lorck_serseri'),(17,'kadiasker_gravur'),(28,'lorck_koylu'),(48,'lorck_muhafiz'),(72,'lorck_yuk_ati'),(89,'lorck_asker'),(103,'kazasker_gravur_metropolitan'),(127,'zincirli_kurekciler_gemide'),(137,'tersane_pardoe_gravur'),(152,'lorck_sipahi_atli')]
S=[(idx[o],f) for o,f in S]
D=94.67
def kirp(f):
    im=Image.open(f'assets/belgeler/122_{f}.jpg');W,H=im.size;cx,cy=K[f][4]
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
    bs,kay,lis,gor,_=K[f]
    cap=' '.join(EK[i0:i1])
    segs.append({"say":cap.replace("'",""),"caption":cap,"key":[],"scene":"photo","gorunen":gor,"bolumler":bol,
      "image":{"local":f"assets/belgeler/122_{f}.jpg","fit":"doldur","hiz":0.5,"kirp":kirp(f),"baslik":bs,"kaynak":kay,"lisans":lis}})
    kes.append([[round(bas,2),round(bit,2)]])
ep={"series":"Sıradan Değil","voice":"ana","takip_cagrisi":False,"episode":122,"slug":"hirsiz","title":"Osmanlı'da hırsızın eli kesilir miydi?","youtube_title":"","youtube_description":"",
"sources":["Baytimur 2018","Baba 2013","Osmanağaoğlu-Karahasanoğlu","Koç 2019","Okur Gümrükçüoğlu 2024","Yücetürk 2024"],"acilis":"Hırsızın eli\ngerçekten kesilir miydi?",
"dis_ses":{"file":"assets/ses/122_hirsiz.mp3","kesimler":kes},"surum":1,"segments":segs}
json.dump(ep,open('episodes/122_hirsiz.json','w'),ensure_ascii=False,indent=1)
for s,k in zip(segs,kes): print(k[0], round(k[0][1]-k[0][0],1), s['image']['local'][20:], s['image']['kirp'], '|', s['caption'][:50])
