import json
exec(open('arastirma/127_k.py').read())
w=json.load(open('/tmp/w/w127.json'))
FIX={"6":"altı","'ındaysa":"","Kur":"Kur'an","Camii":"Camii","Mevlid":"mevlit","Saadettin":"Sadettin","yayınlandı.":"yayımlandı.","okunurken,":"okunurken","Ekber!":"Ekber.","Ramazan":"Ramazanında ise","gecesinde":"Gecesinde"}
EK=[FIX.get(x[2],x[2]) for x in w]
# eklenen parçalar ('an, 'ün, 'nde, 'ın) önceki kelimeye bitişir
for i in range(len(EK)):
    if EK[i].startswith("'") and i>0:
        EK[i-1]=EK[i-1]+EK[i] if EK[i-1]!="Kur'an" else EK[i-1]; EK[i]=""
EK=[x.replace("Kur'an'an","Kur'an") for x in EK]
for i,x in enumerate(EK):
    if x=="Camii" and i+1<len(w) and w[i+1][2].startswith("'nde"): EK[i]="Camii'nde"
    if x=="Hafız" and i+1<len(w) and w[i+1][2]=="'ın": EK[i]="hafızın"
    if x=="Atatürk" and i+1<len(w) and w[i+1][2]=="'ün": EK[i]="Atatürk'ün"
    if x=="Kur'an" and i+2<len(w) and w[i+2][2]=="'ın": EK[i]="Kur'an'ın"
CAPFIX=[("altı yıl sonra ise","Altı yıl sonra ise"),("Camii doldu","Cami doldu"),("Hafız'ın","hafızın"),("Kur'an'ın 'ın","Kur'an'ın"),("Kadir Gecesinde","Kadir Gecesi'nde")]
D=87.48
S=[(0,'dua'),(5.48,'das'),(14.0,'kap'),(18.6,'sah'),(27.26,'seb'),(32.98,'kal'),(38.24,'nef'),(42.9,'a15'),(47.48,'rad'),(52.22,'sul'),(57.92,'min'),(63.82,'bur'),(69.8,'aic'),(76.0,'bay'),(82.56,'kul')]
segs=[];kes=[]
for j,(bas,f) in enumerate(S):
    bit=S[j+1][0] if j+1<len(S) else D
    ids=[i for i,x in enumerate(w) if bas-0.05<=x[0]<bit-0.05 and EK[i]]
    bol=[];k=0
    while k<len(ids):
        m=min(4,len(ids)-k)
        if len(ids)-k-m==1: m+=1
        st=w[ids[k]][0] if k>0 else bas
        en=w[ids[k+m]][0] if k+m<len(ids) else min(bit,w[ids[-1]][1]+0.6)
        bol.append({"start":round(st,2),"end":round(en,2),"n":m});k+=m
    p,bs,kay,lis,gor,_,_,on=K[f]
    cap=' '.join(EK[i] for i in ids)
    for a,b in CAPFIX: cap=cap.replace(a,b)
    segs.append({"say":cap.replace("'",""),"caption":cap,"key":[],"scene":"photo","gorunen":gor,"bolumler":bol,
      "image":{"local":B+p,"fit":"doldur","hiz":1.0,"kirp":kirp(f),"baslik":bs,"kaynak":kay,"lisans":lis,**({"onay":on} if on else {})}})
    kes.append([[round(bas,2),round(bit,2)]])
ep={"series":"Sıradan Değil","voice":"ana","takip_cagrisi":False,"episode":127,"slug":"turkce_kuran","title":"1932'de camide Türkçe Kur'an ve hutbe","youtube_title":"","youtube_description":"",
"sources":["Dikici 2006","Erdoğan 2021","TDV Hutbe"],"acilis":"İmam görevden alındı\n6 yıl sonra Ayasofya'da Türkçe tekbir",
"dis_ses":{"file":"assets/ses/127_turkce_kuran.mp3","kesimler":kes},"surum":1,"segments":segs}
json.dump(ep,open('episodes/127_turkce_kuran.json','w'),ensure_ascii=False,indent=1)
for s,k in zip(segs,kes): print(k[0], round(k[0][1]-k[0][0],1), s['image']['local'][16:40], '|', s['caption'][:90])
