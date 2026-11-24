import json,re
from PIL import Image
w0=json.load(open('/tmp/w121.json'))
# kesme ekli parçaları önceki kelimeye birleştir
w=[];orig=[]
for i,(a,b,t) in enumerate(w0):
    if t.startswith("'") and w:
        w[-1]=[w[-1][0],b,w[-1][2]+t]
    else:
        w.append([a,b,t]); orig.append(i)
idx={o:n for n,o in enumerate(orig)}
EKRAN=("Eyüp Sultan'a gidip bir Fatiha okumak… Bugün ne kadar sıradan, değil mi? "
"Oysa bir dönem bu kapılar 25 yıl boyunca kapalı kaldı. Üstelik açmaya kalkana hapis cezası vardı. "
"1925'te Meclis bir kanun çıkardı. Tekkeler ve türbeler kapatıldı. "
"Devlet, buraları batıl inançların kaynağı olarak görüyordu. "
"Kanun açıktı: Kapalı bir türbeyi açana en az üç ay hapis ve elli lira para cezası. "
"Ama halk vazgeçmedi. Kapılar kilitliydi; insanlar dışarıda durup dua etti. Adaklarını adamaya devam etti. "
"Bakımsız kalan türbelerin birçoğu yıllar içinde harap oldu. "
"1949'da Başbakan Şemsettin Günaltay, İstanbul'da Mimar Sinan'ın türbesini ziyaret etmek istedi. "
"Vali, türbenin kapalı olduğunu söyleyince şu cevabı verdi: “Sinan'ın türbesi kapalı olur mu?” Bu söz, değişimin habercisiydi. "
"Ertesi bahar karar çıktı. Fatih, Kanuni, Yavuz ve Hacı Bayram türbeleri sırayla açılmaya başladı. "
"Eyüp Sultan da eylülde açıldı. İnsanlar, 25 yıl sonra yeniden o kapılardan içeri girdi. "
"Sizce türbeleri 25 yıl kapalı tutan bu yasak doğru muydu? "
"Düşüncelerinizi yorumlarda paylaşın. Kaynaklar video açıklamasında. Beğenmeyi ve takip etmeyi lütfen unutmayalım.").split()
assert len(EKRAN)==len(w),(len(EKRAN),len(w))
for e,x in zip(EKRAN,w):
    if re.sub(r'\W','',e.lower())[:3]!=re.sub(r'\W','',x[2].lower())[:3]: print('fark:',e,x[2])
SES=open('arastirma/121_turbe_senaryo.txt').read()
ses_tok=re.sub(r'\[[a-z ]+\]','',SES).split()
L="Kamu malı"
K={
'kanuni_hurrem_turbe_gravur_1853':("Süleymaniye'de Kanuni ve Hürrem türbeleri (gravür, Flandin 1853)","Eugène Flandin, 1853, Commons","Kamu malı","Ağaçlar arasında kubbeli türbe, arkada Süleymaniye Camii, önde gezen insanlar (gravür)",(.56,.5)),
'valide_turbe_lccn':("İstanbul'da bir türbe, 19. yüzyıl","LOC LCCN92513540, Commons","Kamu malı","Kubbeli türbe ve demir parmaklıklı pencereli duvarlar, boş meydan",(.25,.5)),
'ayasofya_turbe_ic':("Ayasofya türbelerinin içi","W. H. Goodyear, Brooklyn Museum, Commons","Kamu malı","Türbe içinde yan yana sandukalar, sarık başlıklı mezarlar, ahşap korkuluk",(.45,.5)),
'turbe_sandukalar_1903':("Bir türbede şehzade sandukaları, 1903","Brooklyn Museum, Flickr, Commons","Telif kısıtlaması yok","Sıra sıra örtülü sandukalar, üstlerinde beyaz sarıklar",(.5,.5)),
'mahmud_turbe_ic_1870':("II. Mahmud türbesinde sanduka, 1870-1920","Digital Commonwealth, Commons","Kamu malı","Gümüş parmaklıklı, işlemeli örtülü sanduka, yanında rahle ve şamdan",(.5,.5)),
'selim2_turbe_giris_1913':("Ayasofya'da II. Selim türbesinin girişi, 1913","Hermann Barth, 1913, Commons","Kamu malı","Çinili türbe kapısının önünde duran bir adam, merdivenler",(.42,.5)),
'selim_turbe_ic':("Bir türbede sanduka","Brooklyn Museum, Commons","Telif kısıtlaması yok","Büyük örtülü sanduka, şamdan ve sarık, loş türbe içi",(.4,.5)),
'kanuni_hurrem_turbe_clement':("Süleymaniye'de Kanuni ve Hürrem türbeleri, 1895","C. Clement, Constantinople (1895), Commons","Kamu malı","Sekizgen kubbeli türbe ve arkasında ikinci türbe, avlu duvarı",(.28,.5)),
'kanuni_turbe_gravur_1817':("Kanuni türbesi, Süleymaniye (gravür, Pertusier 1817)","Charles Pertusier, 1817, Commons","Kamu malı","Ağaçlar arasında kubbeli türbe ve revaklı avlu, önde insanlar (gravür)",(.5,.5)),
'mahmud_turbe_dis':("II. Mahmud türbesi, Divanyolu","LOC LCCN92513539, Commons","Kamu malı","Kubbeli türbe ve yanındaki kemerli avlu duvarı, toprak cadde",(.38,.5)),
'murad2_turbe_bursa':("Bursa'da II. Murad türbesinin içi, Abdullah Frères","Abdullah Frères, DPLA, Commons","Kamu malı","Türbe içinde sanduka, büyük şamdanlar, ahşap zemin",(.5,.5)),
'mahmud_turbe_ic_clement':("II. Mahmud ve Abdülaziz'in sandukaları, 1895","C. Clement, Constantinople (1895), Commons","Kamu malı","Parmaklıklı iki sanduka, önünde rahle başında dua eden bir adam",(.55,.5)),
}
S=[(0,'kanuni_hurrem_turbe_gravur_1853'),(13,'valide_turbe_lccn'),(29,'ayasofya_turbe_ic'),(38,'turbe_sandukalar_1903'),(47,'mahmud_turbe_ic_1870'),(61,'selim2_turbe_giris_1913'),(75,'selim_turbe_ic'),(83,'kanuni_hurrem_turbe_clement'),(95,'kanuni_turbe_gravur_1817'),(113,'mahmud_turbe_dis'),(127,'murad2_turbe_bursa'),(141,'mahmud_turbe_ic_clement')]
S=[(idx[o],f) for o,f in S]
D=83.64
def kirp(f):
    im=Image.open(f'assets/belgeler/121_{f}.jpg');W,H=im.size;cx,cy=K[f][4]
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
    segs.append({"say":' '.join(ses_tok[i0:i1]),"caption":' '.join(EKRAN[i0:i1]),"key":[],"scene":"photo","gorunen":gor,"bolumler":bol,
      "image":{"local":f"assets/belgeler/121_{f}.jpg","fit":"doldur","hiz":(0.5 if ("gravur" in f or f=="kanuni_hurrem_turbe_clement") else 1.0),"kirp":kirp(f),"baslik":bs,"kaynak":kay,"lisans":lis}})
    kes.append([[round(bas,2),round(bit,2)]])
ep={"series":"Sıradan Değil","voice":"ana","takip_cagrisi":False,"episode":121,"slug":"turbe","title":"Türbeler 25 yıl neden kilitli kaldı?","youtube_title":"","youtube_description":"",
"sources":["Dinç 2017","Dokuyan 2022","Gündoğdu 2024","Hakyemez 2014","Apaydın 2017","Tanyu 1961"],"acilis":"Türbeler neden\n25 yıl kilitli kaldı?",
"dis_ses":{"file":"assets/ses/121_turbe.mp3","kesimler":kes},"surum":1,"segments":segs}
json.dump(ep,open('episodes/121_turbe.json','w'),ensure_ascii=False,indent=1)
for s,k in zip(segs,kes): print(k[0], round(k[0][1]-k[0][0],2), s['image']['local'][20:], s['image']['kirp'], '|', s['caption'][:45])
