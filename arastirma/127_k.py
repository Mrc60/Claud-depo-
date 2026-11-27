B='assets/belgeler/'
T={"tekrar":"TEK1 27.11 11:46 (görsel planı: Tamam yap)"}
K={
'dua':('127_dua_cemaat.jpg',"Dua eden cemaat, 1920'ler","Wikimedia Commons","Kamu malı","Fesli ve sarıklı adamlar ayakta ellerini açmış dua ediyor",(0.189,0.611,0,1),.4,T),
'das':('127_ayasofya_1935_dassonville.jpg',"Ayasofya'nın içi, 1935, avizeler yanıyor","Achille Dassonville, MMSH Phonothèque (MédiHAL 4161210), Commons","Licence Ouverte","Ayasofya'nın içinde yanan avizeler ve kemerler",(.05,.95,.04,.88),.5,None),
'kap':('127_cami_kapisi.jpg',"Bir caminin son cemaat yeri, 19. yüzyıl","Wikimedia Commons","Kamu malı","Cami kapısı önünde merdivenlerde oturan ve duran adamlar",(0,1,0,1),.55,T),
'sah':('127_sultanahmet.jpg',"Sultanahmet Camii ve meydanı, 19. yüzyıl sonu","Sébah & Joaillier, Commons","Kamu malı","Sultanahmet Camii minareleri ve önündeki geniş meydanda yürüyen insanlar",(0.283,0.717,0,1),.5,T),
'seb':('127_ayasofya_sebah_b.jpg',"Ayasofya'nın içi, 1888","Sébah & Joaillier, Library of Congress (LCCN2003680775)","Kamu malı","Ayasofya'nın içinde mermer sütunlar, kemerler ve hat levhası",(.04,.96,.04,.93),.45,None),
'kal':('127_kalabalik.jpg',"İstanbul'da kalabalık, 20. yüzyıl başı","Wikimedia Commons","Kamu malı","Sokakta fesli ve şapkalı kalabalık bir halk",(0,1,0,.94),.5,T),
'nef':('127_ayasofya_sebah_nef.jpg',"Ayasofya'nın içi, 1888","Sébah & Joaillier, Library of Congress (LCCN2003680779)","Kamu malı","Ayasofya'nın büyük kubbesi, kemerleri ve hat levhaları",(.04,.96,.04,.92),.5,None),
'a15':('127_ayasofya_1915.jpg',"Ayasofya'nın içi, 1915","Library of Congress, Commons","Kamu malı","Ayasofya'nın içinde hat levhaları ve sarkan avizeler",(0.084,0.916,0,1),.5,T),
'rad':('127_radyo_dinleyenler.jpg',"Radyo dinleyen gençler (dergi kapağı, 1940'lar)","Basın Yayın Genel Müdürlüğü, Commons","Kamu malı (bilinen kısıtlama yok)","Bir radyonun başında toplanmış gülümseyen gençler",(0,1,0,1),.5,T),
'sul':('127_suleymaniye.jpg',"Süleymaniye Camii, 20. yüzyıl başı","Library of Congress, Commons","Kamu malı","Süleymaniye Camii'nin kubbeleri ve minareleri, önünde Haliç",(0,1,.05,.93),.45,T),
'min':('127_ayasofya_minber.jpg',"Ayasofya'nın minberi, 19. yüzyıl","Cornell University Library, Commons","Kamu malı (bilinen kısıtlama yok)","Ayasofya'da uzun merdivenli mermer minber ve hat levhaları",(.03,.97,.03,.95),.55,None),
'bur':('127_bursa_ulucami_minber.jpg',"Bursa Ulu Cami minberi, 19. yüzyıl sonu","Sébah & Joaillier, Commons","Kamu malı","Oymalı ahşap minber ve duvarda hat yazıları",(0.19,0.81,0.05,0.86),.5,T),
'aic':('127_ayasofya_ic.jpg',"Ayasofya'nın içi, 1900'ler","Sébah & Joaillier, Library of Congress","Kamu malı","Ayasofya'nın içinde yuvarlak hat levhası, kemerler ve avizeler",(0,1,0,1),.5,T),
'bay':('127_bayezid.jpg',"Beyazıt Camii ve meydanı, 1912","Commons","Kamu malı","Beyazıt Camii minaresi ve meydanda yürüyen insanlar",(0,1,.04,.91),.45,T),
'kul':('127_suleymaniye_kulliye.jpg',"Süleymaniye külliyesi, 19. yüzyıl sonu","Sébah & Joaillier, Commons","Kamu malı","Taş kemerli külliye binaları ve önünde boş sokak",(.04,.96,.04,.94),.5,T),
}
from PIL import Image
def kirp(f):
    p,_,_,_,_,(x0,x1,y0,y1),cx,_=K[f]
    W,H=Image.open(B+p).size
    rw,rh=(x1-x0)*W,(y1-y0)*H
    if rw/rh>9/16:
        cw=rh*9/16/W; a=min(max(cx-cw/2,x0),x1-cw); return [round(a,3),y0,round(a+cw,3),y1]
    ch=rw*16/9/H; c=(y0+y1)/2; b=min(max(c-ch/2,y0),y1-ch); return [x0,round(b,3),x1,round(b+ch,3)]
