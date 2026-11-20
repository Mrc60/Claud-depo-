import json,re,difflib,copy,sys
S='/tmp/claude-0/-home-claude/209ca83c-1182-5705-a2dd-8cb28d4188fa/scratchpad/'
t=open(S+'s97.txt').read()
paras=[re.sub(r'\s+',' ',re.sub(r'\[[^\]]+\]','',p)).strip() for p in t.split('\n\n') if p.strip()]
sp=[re.split(r'(?<=[.?!:,…])\s+',p) for p in paras]
j=json.load(open(S+'wt_push/episodes/093_galatasaray.json'));K=json.load(open(S+'cap97.json'))
plan=json.loads(sys.argv[1]);ANIMS=json.loads(sys.argv[3])
segs=[]
for refs,img,key in plan:
    txt=' '.join(sp[int(r.split('.')[0])][int(r.split('.')[1])] for r in refs)
    seg={'say':txt,'caption':txt,'key':key,'image':{'local':'assets/belgeler/'+img+'.jpg','fit':'doldur','baslik':K[img],'lisans':'','kaynak':K[img],'sayfa':'','hiz':1.0},'scene':'photo'}
    segs.append(seg)
assert ' '.join(s['say'] for s in segs).split()==' '.join(paras).split()
W=json.load(open(S+'w97.json'));M=[]
for a,b,w in W:
    if M and w[:1] in "'’": M[-1]=[M[-1][0],b,M[-1][2]+w]
    else: M.append([a,b,w])
norm=lambda s: re.sub(r"[^\wçğıöşüâî]","",s.lower().replace('i̇','i').replace("'","").replace("’","").replace('â','a'))
sw=[w for s in segs for w in s['caption'].split()]
A=[norm(w) for w in sw];B=[norm(x[2]) for x in M];T=[None]*len(A)
for tag,i1,i2,j1,j2 in difflib.SequenceMatcher(None,A,B,autojunk=False).get_opcodes():
    if tag=='equal' or (tag=='replace' and i2-i1==j2-j1):
        for k in range(i2-i1): T[i1+k]=(M[j1+k][0],M[j1+k][1])
    elif tag=='replace':
        a0,b0=M[j1][0],M[j2-1][1];n=i2-i1
        for k in range(n): T[i1+k]=(a0+(b0-a0)*k/n,a0+(b0-a0)*(k+1)/n)
    elif tag!='equal': print(tag,A[i1:i2],B[j1:j2])
END=float(sys.argv[2])
for i in range(len(T)):
    if T[i] is None:
        p=next((T[k][1] for k in range(i-1,-1,-1) if T[k]),0.05);q=next((T[k][0] for k in range(i+1,len(T)) if T[k]),END-0.2)
        T[i]=(p,max(q,p+0.1));print('boşluk',sw[i])
k=0
for s in segs:
    bl=[]
    for _ in s['caption'].split(): a,b=T[k];k+=1;bl.append(dict(start=round(a,2),end=round(max(b,a+0.08),2),n=1))
    s['bolumler']=bl
cuts=[0]+[round(min((segs[i-1]['bolumler'][-1]['end']+segs[i]['bolumler'][0]['start'])/2,segs[i-1]['bolumler'][-1]['end']+0.12),2) for i in range(1,len(segs))]+[END]
j['dis_ses']['kesimler']=[[[cuts[i],cuts[i+1]]] for i in range(len(segs))]
def at(i,word):
    s=segs[i];return round(next(b['start'] for w,b in zip(s['caption'].split(),s['bolumler']) if w.startswith(word))-cuts[i],2)
KIRP={'097_meydan':[0.08,0.12,0.62,0.9],'097_trebizond1915':[0.28,0.47,0.62,0.93],'097_liman':[0,0.25,0.6,1],'097_danistay':[0.35,0.08,0.78,1],'097_avniaker':[0.18,0.12,0.82,1],'097_ozyazici_stad':[0.08,0.28,0.92,1],'097_muze':[0.1,0.04,0.9,1],'097_kafile':[0.18,0.0,0.99,1],'097_kupa':[0.12,0.42,0.88,1],'097_arena':[0.2,0.15,0.8,0.95],'097_arena2':[0.3,0.2,0.85,0.85]}
AP={'Trabzonsporu':"Trabzonspor'u",'Trabzonda':"Trabzon'da",'1966da':"1966'da",'Lige':"Lig'e",'Danıştaya':"Danıştay'a",'1967de':"1967'de",'1974te':"1974'te",'1976da':"1976'da",'Trabzonsporun':"Trabzonspor'un"}
for i,s in enumerate(segs):
    L=s['image']['local'];nm=L.split('/')[-1][:-4]
    if nm in KIRP: s['image']['kirp']=KIRP[nm]
    s['caption']=' '.join(AP.get(w,w) for w in s['caption'].split())
    A=ANIMS.get(nm)
    if A:
        u,bas,mad,bw,zw=A
        s['anim']={"tur":"kart","ust":u,"baslik":bas,"bekle":0.6,"maddeler":mad,"basla":max(0.15,round(at(i,bw)-0.1,2)),"zamanlar":[at(i,z) for z in zw]}
j.update(episode=97,slug='trabzonspor',title='Trabzonspor Nasıl Kuruldu',youtube_title='',acilis='İki ezeli rakip\ntek kulüp oldu');j['dis_ses']['file']='assets/ses/097_trabzonspor.mp3';j['segments']=segs;json.dump(j,open(S+'wt_push/episodes/097_trabzonspor.json','w'),ensure_ascii=False,indent=1)
for i,s in enumerate(segs): print(i+1,s['image']['local'].split('/')[-1],cuts[i],round(cuts[i+1]-cuts[i],1),s.get('anim',{}).get('zamanlar'),s['caption'][:50])
for i,s in enumerate(segs): print(i+1,s['image']['local'].split('/')[-1],cuts[i],round(cuts[i+1]-cuts[i],1),s.get('anim',{}).get('zamanlar'),s['caption'][:40])
