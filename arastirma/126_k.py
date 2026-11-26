B='assets/belgeler/'
R={"renkli":"TEK1 27.11 00:33 (seçim panosundan seçti)"}
T={"tekrar":"TEK1 27.11 00:33 (seçim panosundan seçti)"}
K={
'usk':('126_uskudar_sokak.jpg',"Üsküdar'da bir sokak, 1890'lar (renkli baskı, siyah-beyaza çevrildi)","Photochrom Print Collection, Library of Congress, Commons","Kamu malı","Ahşap evler, minare ve taş döşeli yokuş sokak, yürüyen insanlar ve at arabası",(.04,.96,0,.95),.55,R),
'gel':('126_dugun_gelin.jpg',"Bir düğünde gelin ve kadınlar, 1930'lar","Wikimedia Commons","Kamu malı","Duvaklı beyaz gelinlikli gelin ve yanında uzun elbiseli kadınlar",(.162,.566,0,1),.364,T),
'car':('126_carsafli.jpg',"İstanbullu kadınlar, 20. yüzyıl başı","Library of Congress, Commons","Kamu malı","Çarşaflı, peçeli kadınlar demir parmaklık önünde oturuyor",(0,1,0,1),.5,T),
'tur':('126_nikah_turkistan.jpg',"Nikâh töreni, Orta Asya, 1865-1872 (Türkistan Albümü)","Library of Congress, Commons","Kamu malı","Sarıklı, sakallı yaşlı adamlar yerde oturuyor, önlerinde terlikler",(0,1,0,1),.5,T),
'lit':('126_iki_kadin_litografi.jpg',"Evde iki kadın (taş baskı, 19. yüzyıl)","J. F. Lewis, British Museum, Commons","Kamu malı","Sedirde yan yana oturmuş, başörtülü iki kadın (taş baskı)",(.03,.97,.04,.96),.68,None),
'ank':('126_ankara_kadinlar_1873.jpg',"Ankara kıyafetli kadınlar, 1873","P. Sébah, Elbise-i Osmaniyye (1873), Library of Congress","Kamu malı","Yerel kıyafetli ve başlıklı üç kadın ayakta duruyor",(.30,.82,.20,.74),.50,None),
'nik':('126_noter_nikah_rorbye.jpg',"Bir kadı nikâh sözleşmesi yazıyor (tablo, 1837; siyah-beyaza çevrildi)","Martinus Rørbye, Commons","Kamu malı","Sarıklı kadı ve kâtip kâğıt yazıyor, karşılarında çarşaflı kadınlar oturuyor (tablo)",(0,1,0,1),.50,R),
'usm':('126_uskudar_mezarlik.jpg',"Üsküdar'da çarşaflı kadınlar, 1909","Library of Congress, Commons","Kamu malı","Ağaçlar altında taş sekide oturan çarşaflı kadınlar",(0,1,0,1),.5,T),
'kon':('126_konsolosluk_bosanma_davasi.jpg',"İstanbul'da bir boşanma davası (ABD konsolosluk mahkemesi, 20. yüzyıl başı)","Commons","Kamu malı","Avizeli salonda masa başında oturan yargıçlar ve önlerinde ayakta duran adamlar",(.03,.97,.03,.9),.5,None),
'har':('126_harem_araba.jpg',"Kâğıthane'ye giden kadınlar, 1920 civarı","Library of Congress, Commons","Kamu malı","Süslü at arabasında oturan kadınlar",(0,1,0,1),.5,T),
'cam':('126_cami_aileler.jpg',"Bir camide barınan aileler, 1919","Library of Congress, Commons","Kamu malı","Büyük taş sütunlar arasında ipe asılı çamaşırlar ve yerde oturan insanlar",(0,1,0,1),.5,T),
'koy':('126_koy_kadinlar.jpg',"Köy kadınları ve çocuklar, Türkiye, 1960'lar (siyah-beyaza çevrildi)","Etnografiska museet (SMVK), CC0","CC0","Başörtülü köy kadınları ve çocuklar ayakta, arkada kale",(.05,.95,0,1),.42,T),
}
from PIL import Image
def kirp(f):
    p,_,_,_,_,(x0,x1,y0,y1),cx,_=K[f]
    W,H=Image.open(B+p).size
    rw,rh=(x1-x0)*W,(y1-y0)*H
    if rw/rh>9/16:
        cw=rh*9/16/W; a=min(max(cx-cw/2,x0),x1-cw); return [round(a,3),y0,round(a+cw,3),y1]
    ch=rw*16/9/H; c=(y0+y1)/2; b=min(max(c-ch/2,y0),y1-ch); return [x0,round(b,3),x1,round(b+ch,3)]
