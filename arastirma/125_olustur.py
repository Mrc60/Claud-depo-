import json,sys
from PIL import Image
w=json.load(open('/tmp/w/w125.json'))
# whisper ek birleştirme: "'na", "'a" gibi ayrı gelen ekleri önceki kelimeye ekle
w2=[];orig=[]
for i,(a,b,t) in enumerate(w):
    if t.startswith("'") and w2: w2[-1]=[w2[-1][0],b,w2[-1][2]+t]
    else: w2.append([a,b,t]); orig.append(i)
idx={o:n for n,o in enumerate(orig)}
w=w2
FIX={"nah":"narh","uymuyansa":"uymayan","ise":"ise","4.":"Dördüncü","Murat,":"Murad,","mahkum":"mahkûm","Kadısını":"kadısını","Adası'na":"adasına"}
EK=[FIX.get(x[2],x[2]) for x in w]
# "Narha uymuyansa" -> "Narha uymayan ise"
B='assets/belgeler/'
R={"renkli":"TEK1 26.11 23:01 (Siyah beyazla devam)"}
K={
'sa':('125_sokak_satici_a.jpg',"İstanbul'da bir sokak satıcısı","W. H. Goodyear, Brooklyn Museum, Commons","Kamu malı","Başında yeşillik dolu sepet taşıyan, önlüklü bir sokak satıcısı",(.1,.9,.05,.95),.45,None),
'sb':('125_sokak_satici_b.jpg',"İstanbul'da sırtında fıçı taşıyan bir satıcı","W. H. Goodyear, Brooklyn Museum, Commons","Kamu malı","Sırtında tahta fıçı taşıyan, eğilmiş bir sokak satıcısı, arkada Haliç",(.1,.9,.05,.95),.5,None),
'kz':('125_kazasker_rijks.jpg',"Kazasker, yani en üst rütbeli kadı (tablo, 18. yüzyıl)","J. B. Vanmour, Rijksmuseum, Commons","Kamu malı","Kürklü uzun kaftan ve büyük sarıklı, ayakta duran yaşlı bir kadı (tablo)",(0,1,0,1),.5,R),
'rv':('125_rycaut_vezir.jpg',"Atlı sadrazam ve maiyeti (gravür, 1678)","P. Rycaut, Monarchia Turecka (1678), Commons","Kamu malı","Atın üstünde sorguçlu sadrazam, yanında yürüyen görevliler (gravür)",(.03,.97,.05,.95),.6,None),
'li':('125_limonataci_loc.jpg',"İstanbul'da limonata ve su satıcısı","Library of Congress, Commons","Kamu malı","Fesli bir satıcı bardağa limonata dolduruyor, yanında fesli bir çocuk",(.03,.97,.03,.93),.55,None),
'pn':('125_panorama_berggren.jpg',"Haliç ve iskeleler, 1880'ler","G. Berggren, Commons","Kamu malı","Yukarıdan Haliç, iskeleler, gemiler ve kıyıdaki evler",(0,1,.1,.95),.5,None),
'sk':('125_seddulbahir_kartpostal.jpg',"Seddülbahir Kalesi, Çanakkale (1915 civarı)","Daily Telegraph, Commons","Kamu malı","Kıyıda kemerli taş kale duvarları, önünde iskele ve deniz",(0,1,.05,1),.6,None),
'kh':('125_kayiklar_halic_deamicis.jpg',"Haliç'te kayıklar (gravür, 1883)","E. De Amicis, Costantinopoli (1883), Commons","Kamu malı","Haliç'te kürek çeken kayıklar ve arkada yelkenli gemiler (gravür)",(0,1,.05,.92),.5,None),
'gk':('125_galata_kitap.jpg',"Galata Köprüsü'nde kalabalık","L. P. Benezet, The Story of the Map of Europe (1916), Commons","Kamu malı","Köprüde yürüyen kalabalık, arkada camiler",(0,1,0,.97),.5,None),
'lo':('125_lorck_atli.jpg',"Sarıklı bir Osmanlı atlısı (gravür, 1581)","Melchior Lorck, Statens Museum for Kunst, Commons","Kamu malı","Katıra binmiş, büyük sarıklı yaşlı bir adam (gravür)",(.05,.95,.05,.93),.5,None),
'm4':('125_murad4_young.jpg',"Padişah Dördüncü Murad (gravür, 1815)","John Young, Commons","Kamu malı","Sorguçlu sarıklı, yeşil kaftanlı padişah portresi (gravür)",(.15,.85,.08,.95),.5,R),
'mg':('125_magosa_1878.jpg',"Magosa, Kıbrıs, 1878","John Thomson, Wellcome Collection, Commons","CC BY 4.0","Otlar arasında yıkık taş kemerler ve uzakta eski bir kilise",(.03,.97,.12,.93),.72,None),
'gb':('125_galata_koprusu.jpg',"Galata Köprüsü, 1890'lar","Photochrom Print Collection, Library of Congress, Commons","Kamu malı","Köprüde yürüyen insanlar, arkada Yeni Cami ve Haliç",(0,1,0,.93),.4,R),
}
S=[(0,'sa'),(8,'sb'),(21,'kz'),(29,'rv'),(38,'li'),(49,'pn'),(58,'sk'),(68,'kh'),(80,'gk'),(93,'lo'),(104,'m4'),(115,'mg'),(125,'gb')]
S=[(idx[o],f) for o,f in S]
D=79.15
def kirp(f):
    p,_,_,_,_,(x0,x1,y0,y1),cx,_=K[f]
    W,H=Image.open(B+p).size
    rw,rh=(x1-x0)*W,(y1-y0)*H
    if rw/rh>9/16:
        cw=rh*9/16/W; a=min(max(cx-cw/2,x0),x1-cw); return [round(a,3),y0,round(a+cw,3),y1]
    ch=rw*16/9/H; c=(y0+y1)/2; b=min(max(c-ch/2,y0),y1-ch); return [x0,round(b,3),x1,round(b+ch,3)]
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
    p,bs,kay,lis,gor,_,_,on=K[f]
    cap=' '.join(EK[i0:i1]).replace("Narha uymayan bedelini","Narha uymayan ise bedelini")
    segs.append({"say":cap.replace("'",""),"caption":cap,"key":[],"scene":"photo","gorunen":gor,"bolumler":bol,
      "image":{"local":B+p,"fit":"doldur","hiz":(0.5 if f in ("sk","kh") else 1.0),"kirp":kirp(f),"baslik":bs,"kaynak":kay,"lisans":lis,**({"onay":on} if on else {})}})
    kes.append([[round(bas,2),round(bit,2)]])
ep={"series":"Sıradan Değil","voice":"ana","takip_cagrisi":False,"episode":125,"slug":"narh","title":"Osmanlı'da fahiş fiyatın cezası","youtube_title":"","youtube_description":"",
"sources":["Kütükoğlu, TDV Narh","Köktaş 2016","Öztel 2012","TDV Karaçelebizâde"],"acilis":"Malı saklayıp pahalı satana\nOsmanlı ne yapardı?",
"dis_ses":{"file":"assets/ses/125_narh.mp3","kesimler":kes},"surum":1,"segments":segs}
json.dump(ep,open('episodes/125_narh.json','w'),ensure_ascii=False,indent=1)
for s,k in zip(segs,kes): print(k[0], round(k[0][1]-k[0][0],1), s['image']['local'][16:], s['image']['kirp'], '|', s['caption'][:70])
