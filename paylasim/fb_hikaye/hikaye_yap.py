from PIL import Image,ImageDraw,ImageFont
import textwrap
B='/home/claude/claud-depo-/assets/belgeler/';S='/tmp/claude-0/hk/src/'
F=[
("01",B+"081_pera.jpg","1859'da Beyoğlu'nda çöpü, çöp arabası gelmeden kapının önüne koymak yasaktı.","Grande Rue de Pera, 1912 (Library of Congress)","Türkmen 2024; Öztürk 2011"),
("02",B+"081_rue1.jpg","1913'te İstanbul'da sokakta ve kaldırımda odun kesmek yasaklandı.","İstanbul'da bir sokak, 1870-1900 (Library of Congress)","Türkmen 2024; Akan 2020"),
("03",B+"084_emirgan.jpg","1847 kurallarına göre hoca öğrenciye ancak velinin izniyle, yasemin çubuğu gibi yumuşak bir dalla hafifçe vurabilirdi.","Emirgân Kız Rüştiyesi öğrencileri, 1880-1893 (Library of Congress)","Akyüz 1994; Şimşek 2004"),
("04",S+"h_avariz1642.jpg","Osmanlı'da savaş için istenen geçici bir vergi zamanla her yıl alınır oldu. Adı avarızdı.","Pazahbun köyü avarız defteri, 1642 (kamu malı)","TDV İslâm Ansiklopedisi; Karazeybek 2025"),
("05",B+"081_rue3.jpg","1913'te İstanbul'da kasapların eti dükkânın dışına asması yasaklandı.","İstanbul'da bir sokak, 1870-1900 (Library of Congress)","Türkmen 2024; Akan 2020"),
("06",S+"h_vapur1966.jpg","1999'da SSK hastanelerinde muayene sırası için sabaha karşı kuyruğa girilirdi. Numaralar ancak 07.30'da dağıtılırdı.","Vapur bekleyenler, İstanbul, 1966 (W. Peloquin, CC BY 2.0)","Yeni Şafak 29.06.1999; Sabah 04.01.2005"),
("07",B+"081_rue4.jpg","1913'te İstanbul'da açıkta işkembe ve ciğer satmak yasaktı.","İstanbul'da bir sokak, 1870-1900 (Library of Congress)","Türkmen 2024; Okta 2017"),
("08",B+"084_davutpasa.jpg","Eskiden veliler çocuğu okula başlatırken önce ona hocanın elini öptürürdü.","Davutpaşa Rüştiyesi öğrencileri, 1880-1893 (Library of Congress)","Şimşek 2004; Açıkel 2023"),
("09",B+"081_stamboul1904.jpg","1913'te İstanbul'da yiyecek satan dükkânlara camekân zorunlu oldu.","İstanbul'da bir sokak, 1904 (Library of Congress)","Türkmen 2024; Akan 2020; Okta 2017"),
("10",S+"h_avariz1642.jpg","Bazı köyler avarız vergisini parayla değil, donanmaya kürek çekecek adam göndererek öderdi.","Pazahbun köyü avarız defteri, 1642 (kamu malı)","TDV İslâm Ansiklopedisi; Karazeybek 2025"),
("11",B+"081_galata.jpg","1913'te İstanbul'da kaldırıma sandalye koymak yasaktı.","Galata Kulesi ve tramvay, 1920 civarı (Library of Congress)","Türkmen 2024; Akan 2020"),
("12",S+"h_cemil.jpg","Bu yasakları getiren İstanbul şehremini Cemil Paşa aslında bir cerrahtı.","Cemil (Topuzlu) Paşa (kamu malı)","Akan 2020; Okta 2017"),
("13",B+"081_stamboul1901.jpg","1913'te İstanbul sokaklarında hayvan katarıyla yük taşımak yasaklandı.","Stamboul'da bir sokak, 1901 (Library of Congress)","Türkmen 2024; Akan 2020"),
("14",S+"h_avariz1642.jpg","Avarız vergisi evlere tek tek değil, birkaç haneden oluşan avarızhanelere yazılırdı.","Pazahbun köyü avarız defteri, 1642 (kamu malı)","TDV İslâm Ansiklopedisi; Karazeybek 2025"),
("15",B+"081_sulama.jpg","1859'da Beyoğlu için çıkarılan sokak nizamnamesi tam 103 maddeydi. Sokakların hangi saatte sulanacağı bile yazılıydı.","İstanbul'da sulama arabaları, 1920 (Library of Congress)","Türkmen 2024; Öztürk 2011"),
("16",B+"079_kadin1935.jpg","Yol ve geçit bekleyen derbentçi köyleri avarız vergisinde farklı tutulurdu.","Kapadokya'da köylü bir kadın, 1935 (Library of Congress)","TDV İslâm Ansiklopedisi; Karazeybek 2025"),
("17",B+"081_sokak1906.jpg","1859'da Beyoğlu'nda sokağa süprüntü bırakan ya da suyu dışarı döken ceza öderdi.","İstanbul'da bir cadde, 1906 (Library of Congress)","Öztürk 2011; Türkmen 2024"),
("18",S+"h_avariz1642.jpg","Yüzyıllar süren avarız vergisi Tanzimat ile kaldırıldı.","Pazahbun köyü avarız defteri, 1642 (kamu malı)","TDV İslâm Ansiklopedisi; Karazeybek 2025"),
]
fb='/usr/share/fonts/truetype/dejavu/'
H1=ImageFont.truetype(fb+'DejaVuSans-Bold.ttf',50);TX=ImageFont.truetype(fb+'DejaVuSerif-Bold.ttf',56)
SM=ImageFont.truetype(fb+'DejaVuSans.ttf',30);SB=ImageFont.truetype(fb+'DejaVuSans-Bold.ttf',32)
PAPER=(237,228,211);INK=(38,30,24);RED=(140,28,28);GREY=(95,85,75)
crops={'01':.5,'04':.3,'10':.55,'14':.8,'18':.5}
for n,img,fact,cap,src in F:
    im=Image.open(img).convert('RGB');W,H=1080,1100
    w,h=im.size;s=max(W/w,H/h);im=im.resize((int(w*s)+1,int(h*s)+1),Image.LANCZOS)
    cx=crops.get(n,.5) if 'avariz' in img else .5
    l=int((im.width-W)*cx);t=int((im.height-H)*(.35 if 'avariz' not in img else cx));t=int((im.height-H)*.45) if 'sulama' in img else t;im=im.crop((l,t,l+W,t+H))
    c=Image.new('RGB',(1080,1920),PAPER);c.paste(im,(0,0));d=ImageDraw.Draw(c)
    d.text((540,H+12),cap,font=SM,fill=GREY,anchor='ma')
    y=H+80;d.text((540,y),"BUNU BİLİYOR MUYDUNUZ?",font=H1,fill=RED,anchor='ma');y+=95
    for line in textwrap.wrap(fact,30):
        d.text((540,y),line,font=TX,fill=INK,anchor='ma');y+=74
    d.text((540,1790),"Kaynak: "+src,font=SM,fill=GREY,anchor='ma')
    d.text((540,1840),"Sıradan Değil",font=SB,fill=RED,anchor='ma')
    assert y<1770,(n,y)
    c.save(f'/tmp/claude-0/hk/out/hikaye_{n}.jpg',quality=90)
b=Image.new('RGB',(9*200,2*360),(30,30,30))
for i in range(18):
    x=Image.open(f'/tmp/claude-0/hk/out/hikaye_{i+1:02d}.jpg');x.thumbnail((196,350));b.paste(x,((i%9)*200+2,(i//9)*360+4))
b.save('/tmp/claude-0/hk/pano.jpg')
