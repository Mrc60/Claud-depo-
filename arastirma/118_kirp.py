from PIL import Image
import json,sys
D='/tmp/v118img/'
# görsel, cx, cy (kırpım merkezi, 0-1)
C={'portre_sebah':(.5,.42),'yakin_portre':(.5,.4),'tbmm_dua':(.56,.5),'dua':(.4,.5),'harington':(.5,.45),
'portre_bnf':(.5,.45),'yildiz_cami_cikis':(.45,.5),'tophane_panorama':(.55,.5),'malta_varis':(.38,.5),
'abdulmecid':(.5,.45),'gemiden_inis':(.62,.5),'tekkiye_eski':(.5,.5),'fayton':(.55,.5),'malaya_iwm':(.55,.5)}
def kirp(n):
    im=Image.open(D+f'118_{n}.jpg');W,H=im.size;cx,cy=C[n]
    if W/H>9/16:
        w=H*9/16/W; x0=min(max(cx-w/2,0),1-w); return [round(x0,3),0,round(x0+w,3),1]
    h=W*16/9/H; y0=min(max(cy-h/2,0),1-h); return [0,round(y0,3),1,round(y0+h,3)]
if __name__=='__main__':
    P=Image.new('RGB',(7*200,2*370),'white')
    for i,n in enumerate(C):
        im=Image.open(D+f'118_{n}.jpg').convert('RGB');W,H=im.size;k=kirp(n)
        c=im.crop((int(k[0]*W),int(k[1]*H),int(k[2]*W),int(k[3]*H))).resize((196,348))
        P.paste(c,((i%7)*200+2,(i//7)*370+2))
    P.save('/tmp/b118/kirp_pano.jpg',quality=85)
    print({n:kirp(n) for n in C})
