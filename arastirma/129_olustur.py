import json
exec(open('arastirma/129_k.py').read())
w=json.load(open('/tmp/w129.json'))
EK=[x[2] for x in w]
for i in range(len(EK)):
    if EK[i].startswith("'") and i>0: EK[i-1]=EK[i-1]+EK[i]; EK[i]=""
MAP={}
EK=[MAP.get(x,x) for x in EK]
CAPFIX=[("anayasayı bir de biz görelim","\"Anayasayı bir de biz görelim\""),("ya aynı üslupla cevap verecektim ya da çıkacaktım","\"Ya aynı üslupla cevap verecektim ya da çıkacaktım\""),("ben bir esnafım","\"Ben bir esnafım\""),("Peki siz","Peki, siz")]
D=111.39
S=[(0,'e02'),(5.3,'di'),(13.2,'spu'),(18.9,'sp'),(26.3,'oz'),(31.6,'e02b'),(36.7,'e00'),(45.2,'ds'),(51.6,'bo'),(59.2,'m1'),(67.9,'em'),(73.7,'c5o'),(79.8,'em2'),(84.9,'m20'),(91.6,'d01'),(99.1,'c5a'),(104.1,'di2')]
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
    p,bs,kay,lis,gor,_,_,on,hz=K[f]
    cap=' '.join(EK[i] for i in ids)
    for a,b in CAPFIX: cap=cap.replace(a,b)
    hiz=hz
    segs.append({"say":cap.replace("'",""),"caption":cap,"key":[],"scene":"photo","gorunen":gor,"bolumler":bol,
      "image":{"local":B+p,"fit":"doldur","hiz":hiz,"kirp":kirp(f),"baslik":bs,"kaynak":kay,"lisans":lis,**({"onay":on} if on else {})}})
    kes.append([[round(bas,2),round(bit,2)]])
ep={"series":"Sıradan Değil","voice":"ana","takip_cagrisi":False,"episode":129,"slug":"kriz","title":"2001 krizi: bir kitapçık ve dolar","youtube_title":"","youtube_description":"",
"sources":["TCMB","IMF 2001","AA","bianet"],"acilis":"Kitapçık uçtu,\ndolar %40 fırladı",
"dis_ses":{"file":"assets/ses/129_kriz.mp3","kesimler":kes},"surum":1,"segments":segs}
json.dump(ep,open('episodes/129_kriz.json','w'),ensure_ascii=False,indent=1)
for s,k in zip(segs,kes): print(k[0], round(k[0][1]-k[0][0],1), s['image']['local'][16:40], '|', s['caption'])
