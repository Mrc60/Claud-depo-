import json
exec(open('arastirma/126_k.py').read())
w=json.load(open('/tmp/w/w126.json'))
FIX={"''Üzerime":"“Üzerime","evlenmeyeceksin''":"evlenmeyeceksin”","''Senin":"“Senin","olsun.''":"olsun.”","''Gülbahar'dan":"“Gülbahar'dan",
     "nikaha,":"nikâha","nikahın":"nikâhın","inkar":"inkâr","Aile":"aile","Kanunu":"kanunu","şuydu.":"şuydu:","verdirdiler.":"verdirdiler:"}
EK=[FIX.get(x[2],x[2]) for x in w]
for i in range(len(EK)-1):
    if EK[i]=="Üsküdar" and EK[i+1]=="da": EK[i]="Üsküdar'da"; EK[i+1]=""
D=82.68
S=[(0,'nik'),(7.38,'gel'),(12.6,'car'),(17.5,'tur'),(22.2,'lit'),(26.88,'ank'),(31.48,'usk'),(36.86,'usm'),(44.74,'har'),(51.22,'kon'),(58.44,'cam'),(68.82,'koy')]
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
    segs.append({"say":cap.replace("'",""),"caption":cap,"key":[],"scene":"photo","gorunen":gor,"bolumler":bol,
      "image":{"local":B+p,"fit":"doldur","hiz":1.0,"kirp":kirp(f),"baslik":bs,"kaynak":kay,"lisans":lis,**({"onay":on} if on else {})}})
    kes.append([[round(bas,2),round(bit,2)]])
ep={"series":"Sıradan Değil","voice":"ana","takip_cagrisi":False,"episode":126,"slug":"kuma","title":"Osmanlı'da kuma şartı","youtube_title":"","youtube_description":"",
"sources":["Atasoy 2024","Kılıç 2025","Midilli 2022","TDV Hukuk-ı Aile Kararnamesi"],"acilis":"Kocası evlenirse\nyeni gelin boş sayılacaktı",
"dis_ses":{"file":"assets/ses/126_kuma.mp3","kesimler":kes},"surum":1,"segments":segs}
json.dump(ep,open('episodes/126_kuma.json','w'),ensure_ascii=False,indent=1)
for s,k in zip(segs,kes): print(k[0], round(k[0][1]-k[0][0],1), s['image']['local'][16:], s['image']['kirp'], '|', s['caption'][:80])
