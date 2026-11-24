from PIL import Image
D='assets/belgeler/'
C={'firinci_ceza_gravur':(.5,.45),'esnaf_dukkani_sebah':(.52,.5),'sokak_kalabalik_gravur':(.45,.55),'divan_dohsson':(.5,.5),'carsi_1880':(.5,.5),'pabuccu_carsi':(.5,.6),'kapalicarsi_gravur1':(.5,.45),'su_saticisi':(.5,.5),'pazar_bauer':(.5,.6),'kapalicarsi_gravur2':(.5,.5),'kapalicarsi_gravur3':(.5,.5),'kapalicarsi_gravur4':(.5,.5)}
B={'sokak_kalabalik_gravur':.93,'divan_dohsson':.9,'carsi_1880':.92,'kapalicarsi_gravur1':.9,'kapalicarsi_gravur2':.9,'kapalicarsi_gravur3':.9,'kapalicarsi_gravur4':.92,'firinci_ceza_gravur':.95,'pazar_bauer':.95}
def kirp(n):
    im=Image.open(D+f'120_{n}.jpg');W,H=im.size;cx,cy=C[n];b=B.get(n,1.0);Hb=H*b
    if W/Hb>9/16:
        w=Hb*9/16/W; x0=min(max(cx-w/2,0),1-w); return [round(x0,3),0,round(x0+w,3),b]
    h=W*16/9/H
    if h>1: # çok dar: tam yükseklik, kenar payı yok
        return [0,0,1,1]
    y0=min(max(cy-h/2,0),1-h); return [0,round(y0,3),1,round(y0+h,3)]
if __name__=='__main__':
    P=Image.new('RGB',(7*200,2*370),'white')
    for i,n in enumerate(C):
        im=Image.open(D+f'120_{n}.jpg').convert('RGB');W,H=im.size;k=kirp(n)
        c=im.crop((int(k[0]*W),int(k[1]*H),int(k[2]*W),int(k[3]*H))).resize((196,348))
        P.paste(c,((i%7)*200+2,(i//7)*370+2))
    P.save('/tmp/v120/kirp_pano.jpg',quality=85); print({n:kirp(n) for n in C})
