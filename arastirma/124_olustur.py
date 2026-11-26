import json
from PIL import Image
w0=json.load(open('/tmp/w/w124.json'))
w=[];orig=[]
for i,(a,b,t) in enumerate(w0):
    if t.startswith("'") and w: w[-1]=[w[-1][0],b,w[-1][2]+t]
    else: w.append([a,b,t]); orig.append(i)
idx={o:n for n,o in enumerate(orig)}
FIX={"Ahmet":"Ahmed","Ahmet'ten":"Ahmed'den","5":"beş"}
EK=[FIX.get(x[2],x[2]) for x in w]
B='assets/belgeler/'
K={
'pc':('124_peceli_kadin_1913c.jpg',"Peçeli bir Türk kadını, 1913","Zeyneb Hanım, A Turkish Woman's European Impressions (1913), Commons","Kamu malı","Peçeli, uzun pardösülü, ayakta duran bir kadın",(.08,.92,.05,.95),.5),
'pazar':('124_pazar_yeri_1913.jpg',"İstanbul'da bir meydan, 1913","R. Hichens, The Near East (1913), Internet Archive Book Images, Commons","Kamu malı","Ağaçlı bir meydanda oturan çarşaflı kadınlar ve yürüyen insanlar",(.03,.97,.03,.93),.4),
'bartlett':('124_bartlett_cesme_gravur.jpg',"İstanbul'da çeşme başı (gravür, 1839)","W. H. Bartlett / J. Pardoe, Constantinople (1839), Commons","Kamu malı","Çeşme önünde kadınlar, öküz arabası ve kalabalık (gravür)",(0,1,0,1),.6),
'pb':('124_peceli_kadin_1913b.jpg',"Peçeli bir Türk kadını, 1913","Zeyneb Hanım, A Turkish Woman's European Impressions (1913), Commons","Kamu malı","Yüzü peçeyle örtülü, başlıklı bir kadının portresi",(.08,.92,.05,.95),.5),
'pa':('124_peceli_kadin_1913a.jpg',"Peçeli bir Türk kadını, 1913","Zeyneb Hanım, A Turkish Woman's European Impressions (1913), Commons","Kamu malı","Peçeli, açık renk pelerinli bir kadın, arkada halılar ve çerçeveler",(.08,.92,.05,.95),.5),
'pd':('124_peceli_kadinlar_1913d.jpg',"Peçeli iki Türk kadını, 1913","Zeyneb Hanım, A Turkish Woman's European Impressions (1913), Commons","Kamu malı","Oval çerçevede peçeli iki kadın",(.1,.9,.1,.9),.35),
'hapis':('124_hapishane_kapisi.jpg',"Osmanlı hapishanesi kapısı, Kudüs (1898-1914)","American Colony Photo Dept., Library of Congress matpc.06801, Commons","Kamu malı","Taş kemerli kapı önünde fesli gardiyanlar ve memurlar",(0,1,0,1),.5),
'kisla':('124_kisla_hapis.jpg',"İstanbul'da hapishane olarak kullanılan kışla","Agence Rol, Bibliothèque nationale de France, Commons","Kamu malı","Tepede büyük bir kışla binası, önünde yol ve yamaç",(.02,.98,.05,.93),.5),
'rob':('124_robertson_kadin.jpg',"Sokak kıyafetli bir Türk kadını (siyah-beyaza çevrildi)","James Robertson, J. Paul Getty Museum, Commons","Kamu malı","Yüzü ince yaşmakla örtülü, ferace giymiş bir kadın",(.05,.95,.1,.95),.5),
}
OT={"tekrar":"TEK1 26.11 (seçim panosundan 13, 14, 15 kullanılsın dedi)"}
K['uc']=('087_uc_kadin1914.jpg',"Çarşaflı kadınlar, 1914","Six and One Abroad (1914), Internet Archive Book Images, Commons","Kamu malı","Ağaç altında yan yana duran çarşaflı üç kadın",(0,1,0,1),.5)
K['sokak']=('087_pera_sokak1913.jpg',"İstanbul'da bir yokuş, 1913","R. Hichens, The Near East (1913), Internet Archive Book Images, Commons","Kamu malı","Kalabalık, yokuş bir İstanbul caddesi, iki yanda binalar",(0,1,0,1),.5)
K['falaka']=('124_falaka_baku_sb.jpg',"Bakü'de bir mektepte falaka cezası, kartpostal, 1896 (siyah-beyaza çevrildi)","Alexandre Michon, Commons","Kamu malı","Sopayla ayakları tutulan çocuk ve çevresinde duran çocuklar (falaka)",(0,1,0,1),.5)
S=[(0,'uc'),(13,'pc'),(25,'sokak'),(38,'falaka'),(47,'bartlett'),(59,'pa'),(73,'pazar'),(85,'hapis'),(96,'kisla'),(111,'pb'),(123,'rob')]
S=[(idx[o],f) for o,f in S]
D=71.81
def kirp(f):
    p,_,_,_,_,(x0,x1,y0,y1),cx=K[f]
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
    p,bs,kay,lis,gor,_,_=K[f]
    cap=' '.join(EK[i0:i1])
    segs.append({"say":cap.replace("'",""),"caption":cap,"key":[],"scene":"photo","gorunen":gor,"bolumler":bol,
      "image":{"local":B+p,"fit":"doldur","hiz":(0.5 if f in ("bartlett","kisla") else 1.0),"kirp":kirp(f),"baslik":bs,"kaynak":kay,"lisans":lis,**({"onay":OT} if f in ("uc","sokak","falaka") else {}),**({"onay":{"renkli":"TEK1 26.11 (siyah-beyaza çevrildiği söylendi, 9 numarayı seçti)"}} if f=="rob" else {}),}})
    kes.append([[round(bas,2),round(bit,2)]])
ep={"series":"Sıradan Değil","voice":"ana","takip_cagrisi":False,"episode":124,"slug":"lafatma","title":"Osmanlı'da kadına laf atmanın cezası","youtube_title":"","youtube_description":"",
"sources":["Cıkay 2021","Imber/Midilli 2017","Örsten Esirgen 2016","Acıduman vd. 2019","Bucknill 1913"],"acilis":"Kadına laf atmanın\nOsmanlıdaki cezası",
"dis_ses":{"file":"assets/ses/124_lafatma.mp3","kesimler":kes},"surum":1,"segments":segs}
json.dump(ep,open('episodes/124_lafatma.json','w'),ensure_ascii=False,indent=1)
for s,k in zip(segs,kes): print(k[0], round(k[0][1]-k[0][0],1), s['image']['local'][16:], s['image']['kirp'], '|', s['caption'][:60])
