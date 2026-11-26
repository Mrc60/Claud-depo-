import json
from PIL import Image
w0=json.load(open('/tmp/w/w123.json'))
w=[];orig=[]
for i,(a,b,t) in enumerate(w0):
    if t.startswith("'") and w: w[-1]=[w[-1][0],b,w[-1][2]+t]
    else: w.append([a,b,t]); orig.append(i)
idx={o:n for n,o in enumerate(orig)}
FIX={"İstanbullu":"İstanbul'u","Cerdet":"Cevdet","ekiminde":"Ekim'inde"}
EK=[FIX.get(x[2],x[2]) for x in w]
B='assets/belgeler/'
# id: (dosya, baslik, kaynak, lisans, gorunen, (x0,x1,y0,y1) bölge, cx)
K={
'genel1':('123_kahn_ankara_genel1.jpg',"Bozkırdan Ankara ve kale, 1923","Frédéric Gadmer, Musée Albert-Kahn A37033, Commons (siyah-beyaza çevrildi)","CC BY-SA 4.0","Düz bozkır ovası, uzakta tepede kale ve küçük şehir",(0,1,.05,.95),.62),
'lindsay':('123_lindsay_1929.jpg',"İngiliz büyükelçisi Sir Ronald Lindsay, 1929","The Associated Press, Commons","Kamu malı","Bıyıklı, takım elbiseli bir adamın portresi (gazete baskısı)",(.08,.92,.09,.96),.5),
'isgal':('123_isgal_galata.jpg',"İşgal altındaki İstanbul: Galata'da İngiliz askerleri, 1919-1920","Commons (Occupation of Istanbul - British troops in Galata)","Kamu malı","Raylı caddede sıra halinde dizilmiş İngiliz askerleri ve subaylar",(0,1,0,1),.78),
'komisyon':('123_kahn_komisyon_binasi.jpg',"Ankara'da Komisyonlar binası, 1923","Frédéric Gadmer, Musée Albert-Kahn A36956, Commons (siyah-beyaza çevrildi)","CC BY-SA 4.0","Ahşap çitle çevrili iki katlı resmî bina, önünde ağaç",(.03,.97,.05,.95),.42),
'meclis':('123_meclis_1921.jpg',"Büyük Millet Meclisi'nde oturum, 1 Mart 1921","Esad Nedim, Commons","Kamu malı","Kalabalık bir salon, sıralarda oturan mebuslar ve kürsü",(0,1,0,1),.55),
'abd':('123_abd_elciligi_istanbul.jpg',"İstanbul'daki ABD elçiliği binası","Harris & Ewing, Library of Congress hec.14216","Kamu malı","Bahçeli, sütunlu büyük bir elçilik binası",(.13,.87,.1,.8),.5),
'yol':('123_bnf_angora_yol.jpg',"Ankara'ya giden yol, 1920'ler","Agence Rol, Bibliothèque nationale de France, Commons","Kamu malı","Toprak yol, yürüyen bir adam, arkada kale ve birkaç bina",(.05,.95,.2,.9),.5),
'insaat':('123_ankara_insaat_sfa.jpg',"Ankara'da yeni bir bina inşaatı, 1920'ler","Nationaal Archief SFA022824254, Commons","Kamu malı","İnşaat halinde beyaz bir bina, iskele ve toprak yol",(0,1,0,1),.45),
'sovyet':('123_kahn_sovyet_elcilik1.jpg',"Ankara'da Sovyet elçiliği, 1923","Frédéric Gadmer, Musée Albert-Kahn A37080, Commons (siyah-beyaza çevrildi)","CC BY-SA 4.0","Bayraklı, iki katlı elçilik binası ve önünde toprak yol",(.03,.97,.05,.95),.45),
'belediye':('123_kahn_belediye.jpg',"Ankara belediye binası, 1923","Frédéric Gadmer, Musée Albert-Kahn A36966, Commons (siyah-beyaza çevrildi)","CC BY-SA 4.0","Büyük bir ağaç ve arkasında iki katlı belediye binası, boş meydan",(.05,.95,.04,.96),.55),
'varis':('123_lindsay_varis_1930.jpg',"Büyükelçi Lindsay ve eşi istasyonda (Washington, 1930)","Harris & Ewing, Library of Congress LCCN2016889632","Kamu malı","Paltolu, şapkasını eline almış gülümseyen adam ve kürklü eşi istasyonda",(.02,1,.02,.94),.62),
}
S=[(0,'genel1'),(9,'lindsay'),(23,'isgal'),(33,'komisyon'),(46,'yol'),(63,'meclis'),(74,'abd'),(83,'varis'),(98,'insaat'),(108,'sovyet'),(126,'belediye')]
S=[(idx[o],f) for o,f in S]
D=74.27
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
      "image":{"local":B+p,"fit":"doldur","hiz":(0.5 if f=="lindsay" else 1.0),"kirp":kirp(f),"baslik":bs,"kaynak":kay,"lisans":lis,**({"onay":{"renkli":"TEK1 26.11 (Kahn otokromları siyah-beyaza çevrilsin dedi)"}} if 'kahn' in p else {})}})
    kes.append([[round(bas,2),round(bit,2)]])
ep={"series":"Sıradan Değil","voice":"ana","takip_cagrisi":False,"episode":123,"slug":"baskent","title":"Başkent neden İstanbul değil de Ankara?","youtube_title":"","youtube_description":"",
"sources":["TBMM Zabıt Ceridesi D.2 C.2 13.10.1923","Şimşir 1991","Erdem 2017","Kılıç 2008","Karabulut 2012"],"acilis":"Başkent neden\nİstanbul değil?",
"dis_ses":{"file":"assets/ses/123_baskent.mp3","kesimler":kes},"surum":1,"segments":segs}
json.dump(ep,open('episodes/123_baskent.json','w'),ensure_ascii=False,indent=1)
for s,k in zip(segs,kes): print(k[0], round(k[0][1]-k[0][0],1), s['image']['local'][16:], s['image']['kirp'], '|', s['caption'][:60])
