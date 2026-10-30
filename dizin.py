"""Kanal dizini: episodes/*.json -> DIZIN.md (konu + görsel tekrar kontrolü).
Çalıştır: python3 dizin.py"""
import json, glob, os, collections
rows=[]; used=collections.defaultdict(list)
for p in sorted(glob.glob("episodes/*.json")):
    try: d=json.load(open(p,encoding="utf-8"))
    except Exception: continue
    no=os.path.basename(p).split("_")[0]; t=d.get("title",""); slug=d.get("slug","")
    imgs=[]
    for s in d.get("segments",[]):
        i=(s.get("image") or {}); f=i.get("local") or i.get("file") or ""
        if f:
            b=os.path.basename(f)
            if b not in imgs: imgs.append(b)
            if no not in used[b]: used[b].append(no)
    rows.append((no,t,slug,d.get("acilis","").replace("\n"," / "),imgs))
L=["# KANAL DİZİNİ (otomatik: python3 dizin.py)","","Yeni konu/görsel seçmeden önce buraya bak: konu tekrarı ve görsel tekrarı.","","## Bölümler","","| No | Başlık | Açılış | Görsel sayısı |","|---|---|---|---|"]
L+=[f"| {n} | {t} | {a} | {len(i)} |" for n,t,s,a,i in rows]
L+=["","## Birden fazla bölümde kullanılan görseller",""]
rep=[(b,e) for b,e in used.items() if len(e)>1]
L+=[f"- {b}: {', '.join(e)}" for b,e in sorted(rep)] or ["- (yok)"]
L+=["","## Bölüm başına görseller",""]
for n,t,s,a,i in rows: L.append(f"- **{n} {t}**: "+", ".join(i))
open("DIZIN.md","w",encoding="utf-8").write("\n".join(L)+"\n")
print(len(rows),"bölüm,",len(used),"görsel,",len(rep),"tekrar")
