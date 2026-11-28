import json
exec(open('arastirma/128_k.py').read())
w=json.load(open('/tmp/w128v3.json'))
EK=[x[2] for x in w]
for i in range(len(EK)):
    if EK[i].startswith("'") and i>0: EK[i-1]=EK[i-1]+EK[i]; EK[i]=""
MAP={"anıtkabir":"Anıtkabir","etnografya":"Etnografya","müzesinde":"Müzesi'nde","müzesindeki":"Müzesi'ndeki","Tabut":"tabut","Müze'den":"müzeden","anıtkabire":"Anıtkabir'e","içinde":"için de","ama":"Ama","4":"dört"}
EK=[MAP.get(x,x) for x in EK]
CAPFIX=[("anıt mezar","anıtmezar"),("Rasat Tepe","Rasattepe,"),("Anıt Tepe","Anıttepe"),("Kasım'ında Tabut","Kasım'ında tabut"),("şeref holünün","Şeref Holü'nün"),("Önce kazı","önce kazı"),("vardı. önce","vardı, önce")]
D=89.23
S=[(0,'pilk'),(4.9,'etn'),(11.3,'kor'),(16.8,'a763'),(21.9,'kit'),(27.4,'pgen'),(37.7,'ins1'),(43.4,'pser'),(50.0,'ins2'),(58.7,'pust'),(67.4,'hey'),(75.9,'kit2'),(81.5,'kal')]
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
    hiz=1.0
    segs.append({"say":cap.replace("'",""),"caption":cap,"key":[],"scene":"photo","gorunen":gor,"bolumler":bol,
      "image":{"local":B+p,"fit":"doldur","hiz":hiz,"kirp":kirp(f),"baslik":bs,"kaynak":kay,"lisans":lis,**({"onay":on} if on else {})}})
    kes.append([[round(bas,2),round(bit,2)]])
ep={"series":"Sıradan Değil","voice":"ana","takip_cagrisi":False,"episode":128,"slug":"naas","title":"Atatürk'ün naaşı 15 yıl Etnografya Müzesi'nde","youtube_title":"","youtube_description":"",
"sources":["Boran 2011","Dokuyan 2014","TDV Ankara Etnografya Müzesi"],"acilis":"Naaşı 15 yıl\nbir müzede bekledi",
"dis_ses":{"file":"assets/ses/128_naas.mp3","kesimler":kes},"surum":3,"segments":segs}
json.dump(ep,open('episodes/128_naas.json','w'),ensure_ascii=False,indent=1)
for s,k in zip(segs,kes): print(k[0], round(k[0][1]-k[0][0],1), s['image']['local'][16:40], '|', s['caption'])
