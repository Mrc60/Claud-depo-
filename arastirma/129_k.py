B='assets/belgeler/'
RN="TEK1 28.11 (2001 renkli olsun sorun yok)"
TK="TEK1 28.11 (kullan istediklerini)"
R={"renkli":RN}; RT={"renkli":RN,"tekrar":TK}
K={
'e02':('129_ecevit_2002.jpg',"Bülent Ecevit, 2002","ABD Ulusal Arşivi, Commons","Kamu malı","Ecevit ve heyet ayakta konuşuyor",(0,1,0,1),.2,R,1.0),
'e02b':('129_ecevit_2002.jpg',"Bülent Ecevit, 2002","ABD Ulusal Arşivi, Commons","Kamu malı","Takım elbiseli heyet bir broşüre bakıyor",(0,1,0,1),.62,RT,1.0),
'sp':('129_sezer_portre.jpg',"Ahmet Necdet Sezer, 2004","MRE / Agência Brasil, Commons","CC BY 3.0 BR","Ahmet Necdet Sezer portre",(0,1,0,1),.5,R,1.0),
'spu':('129_sezer_putin.jpg',"Ahmet Necdet Sezer, 2004","Kremlin.ru, Commons","CC BY 4.0","Sezer koltukta oturuyor, resmî görüşme odası",(0,1,0,1),.27,R,1.0),
'oz':('129_ozkan.jpg',"Hüsamettin Özkan (günümüz)","Yildiray Kanli, Commons","CC0","Hüsamettin Özkan ayakta",(0,1,0,1),.5,R,1.0),
'e00':('129_ecevit_davos2000.jpg',"Bülent Ecevit, Davos 2000","WEF Davos, Commons","CC BY-SA 2.0","Ecevit kürsüde oturuyor",(0,1,0,1),.5,R,1.0),
'ds':('129_doviz_sarp2011.jpg',"Döviz bürosu (2011)","Özgür Esen, Commons","CC BY-SA 4.0","Döviz bürosu kapısı ve kur tabelası",(0,1,0,1),.6,R,1.0),
'bo':('129_borsa_bina.jpg',"İstanbul Menkul Kıymetler Borsası binası (2007)","Thomas Steiner, Commons","CC BY-SA 2.5","Borsa binasının girişi",(0,1,0,1),.45,R,1.0),
'm1':('129_1milyon.jpg',"1 milyon lira banknot","Commons","CC0","Bir milyon liralık banknot",(0,1,0,1),.25,R,0.5),
'em':('129_eminonu_kalabalik.jpg',"Eminönü (2009)","Donnyhoca, Commons","CC BY 3.0","Kalabalık bir çarşı caddesi",(0,1,0,1),.35,R,1.0),
'c5o':('129_5000_on.jpg',"5000 lira madeni para","Darphane, Commons","Kamu malı","5000 lira yazan madeni para",(0,1,0,1),.5,R,0.5),
'em2':('129_eminonu_kalabalik.jpg',"Eminönü (2009)","Donnyhoca, Commons","CC BY 3.0","Dükkânlar ve önünde kalabalık",(0,1,0,1),.75,RT,1.0),
'm20':('129_20milyon.jpg',"20 milyon lira banknot (numune)","Merkez Bankası, Commons","Kamu malı","Yirmi milyon liralık banknot",(0,1,0,1),.47,R,0.5),
'd01':('129_dervis_2001.jpg',"Kemal Derviş, 2001","IMF, Commons","Kamu malı","Kemal Derviş gülümsüyor",(0,1,0,1),.5,R,1.0),
'c5a':('129_5000_arka.jpg',"5000 lira madeni para","Darphane, Commons","Kamu malı","Madeni paranın arka yüzü",(0,1,0,1),.5,R,0.5),
'di':('129_doviz_ist2018.jpg',"Döviz bürosu tabelası (2018)","Mark Lowen, Commons","CC BY-SA 4.0","Döviz kurları tabelası",(0,1,0,1),.5,R,1.0),
'di2':('129_doviz_ist2018.jpg',"Döviz bürosu tabelası (2018)","Mark Lowen, Commons","CC BY-SA 4.0","Döviz kurları tabelası",(0,1,.1,.9),.5,RT,1.0),
}
from PIL import Image
def kirp(f):
    p,_,_,_,_,(x0,x1,y0,y1),cx,_,_=K[f]
    W,H=Image.open(B+p).size
    rw,rh=(x1-x0)*W,(y1-y0)*H
    if rw/rh>9/16:
        cw=rh*9/16/W; a=min(max(cx-cw/2,x0),x1-cw); return [round(a,3),y0,round(a+cw,3),y1]
    ch=rw*16/9/H; c=(y0+y1)/2; b=min(max(c-ch/2,y0),y1-ch); return [x0,round(b,3),x1,round(b+ch,3)]
