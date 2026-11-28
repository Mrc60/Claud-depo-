B='assets/belgeler/'
R={"renkli":"TEK1 28.11 00:57 (kitabenin renkli fotoğrafı siyah-beyaz: Geç onaylıyorum)"}
K={
'pilk':('128_proje_ilk.jpg',"Anıtkabir'in ilk proje çizimi (Onat ve Arda, 1942)","Emin Onat ve Orhan Arda, Commons","Kamu malı","Anıtkabir'in sütunlu cephesini gösteren proje çizimi",(0,1,0,1),.5,None),
'etn':('128_etnografya_a.jpg',"Etnografya Müzesi'nin revakları, 1930'lar","Basın Yayın Genel Müdürlüğü, Commons","Kamu malı (bilinen kısıtlama yok)","Etnografya Müzesi'nin sütunlu revakı ve arkada Ankara",(0,1,0,1),.5,None),
'kor':('128_cenaze_kortej.jpg',"Atatürk'ün cenaze korteji, Ankara 1938","MEB Fotoğraflarla Atatürk koleksiyonu, Commons","Kamu malı","Ağaçlı bir caddede uzanan cenaze korteji ve kalabalık",(0,1,0,1),.5,None),
'a763':('128_album_763.jpg',"Cenaze töreninde İsmet İnönü, 1938","Hataylı Ramazan Çeltik, Ebedi Şefimiz albümü, Commons","Kamu malı","Tabutun başında İsmet İnönü ve askerler",(0,1,0,1),.62,None),
'kit':('128_kitabe_2005.jpg',"Etnografya Müzesi'ndeki geçici kabrin kitabesi","Dosseman, Commons","CC BY-SA 4.0","Mermer zeminde geçici kabrin kitabesi ve çerçeveli eski fotoğraf",(0,1,.2,1),.5,R),
'pgen':('128_proje_genel.jpg',"Anıtkabir projesi, tepeden görünüş (çizim)","Emin Onat ve Orhan Arda, Commons","Kamu malı","Bir tepenin üstünde Anıtkabir yapılarının proje çizimi",(0,1,0,1),.55,None),
'ins1':('128_insaat_1951.jpg',"Anıtkabir inşaatı, 1951","Commons","Kamu malı","İskeleler arasında yükselen Anıtkabir binası",(0,1,0,1),.33,None),
'pser':('128_proje_seref.jpg',"Şeref Holü'nün ilk proje çizimi","Emin Onat ve Orhan Arda, Commons","Kamu malı","Kemerli tonozlu bir salon ve ortada lahit çizimi",(0,1,0,1),.5,None),
'ins2':('128_insaat_1951.jpg',"Anıtkabir inşaatı, 1951","Commons","Kamu malı","İnşaat alanında işçiler ve yan binalar",(0,1,0,1),.78,{"tekrar":"TEK1 28.11 (aynı görseli 2 kez)"}),
'pust':('128_proje_ilk.jpg',"Anıtkabir'in ilk projesi: Şeref Holü'nün üstünde yükselen bölüm (çizim)","Emin Onat ve Orhan Arda, Commons","Kamu malı","Sütunlu binanın üstünde yükselen kabartmalı blok",(.3,.7,.1,.9),.5,{"tekrar":"TEK1 28.11 (aynı görseli 2 kez)"}),
'kit2':('128_kitabe_2005.jpg',"Etnografya Müzesi'ndeki geçici kabrin kitabesi","Dosseman, Commons","CC BY-SA 4.0","Geçici kabrin yazıtı ve mermer zemin",(0,1,0,.8),.5,{"tekrar":"TEK1 28.11 (aynı görseli 2 kez)"}),
'hey':('128_1953_heyet.jpg',"Naaşın Anıtkabir'e nakil töreni, 10 Kasım 1953","Mehmet Sürenkök, Commons","Kamu malı","Frak giymiş devlet adamları törende yürüyor",(0,1,0,1),.55,None),
'cer':('128_muze_cerceve_1938.jpg',"Etnografya Müzesi'nde sergilenen 1938 cenaze fotoğrafı","Dosseman, Commons","CC BY-SA 4.0","Cami önünde toplanmış kalabalığı gösteren eski fotoğraf",(.06,.94,.03,.97),.5,None),
'kal':('128_cenaze_kalabalik.jpg',"Atatürk'ün cenaze töreni, 1938","Türkçe Vikipedi, Commons","Kamu malı","Bayrağa sarılı tabut ve arkasında büyük kalabalık",(0,1,0,1),.4,None),
}
from PIL import Image
def kirp(f):
    p,_,_,_,_,(x0,x1,y0,y1),cx,_=K[f]
    W,H=Image.open(B+p).size
    rw,rh=(x1-x0)*W,(y1-y0)*H
    if rw/rh>9/16:
        cw=rh*9/16/W; a=min(max(cx-cw/2,x0),x1-cw); return [round(a,3),y0,round(a+cw,3),y1]
    ch=rw*16/9/H; c=(y0+y1)/2; b=min(max(c-ch/2,y0),y1-ch); return [x0,round(b,3),x1,round(b+ch,3)]
