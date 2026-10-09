"""Google'ın Türkçe Chirp 3 HD seslerinden örnek üretir, seçim yapmak için.

Çıktı: out_sesler/ses_ornekleri.mp3 (sırayla 1, 2, 3... numaralı örnekler)
       out_sesler/ses_listesi.txt (numara -> ses adı)
"""
import base64, os, re, subprocess, sys
import requests

KEY = os.environ["GOOGLE_TTS_API_KEY"]
OUT = "out_sesler"
SAMPLE = ("Bunu her gün görüyorsun ama hikâyesini bilmiyorsun. "
          "On dokuzuncu yüzyılda Osmanlıya ulaşan bu koku, evlerimizde gül suyunun yerini aldı.")
os.makedirs(OUT, exist_ok=True)

r = requests.get("https://texttospeech.googleapis.com/v1/voices", params={"key": KEY, "languageCode": "tr-TR"}, timeout=30)
if r.status_code != 200: sys.exit(f"ses listesi hatası {r.status_code}: {r.text[:300]}")
voices = sorted(v["name"] for v in r.json().get("voices", []) if "Chirp3-HD" in v["name"])
print(f"{len(voices)} Chirp 3 HD Türkçe ses bulundu")

def synth(text, voice, path):
    body = {"input": {"text": text}, "voice": {"languageCode": "tr-TR", "name": voice},
            "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": 24000, "speakingRate": 1.05}}
    rr = requests.post("https://texttospeech.googleapis.com/v1/text:synthesize", params={"key": KEY}, json=body, timeout=60)
    if rr.status_code != 200:
        print("  atlandı", voice, rr.status_code); return False
    open(path, "wb").write(base64.b64decode(rr.json()["audioContent"])); return True

parts, lines = [], []
announcer = voices[0] if voices else None
for n, v in enumerate(voices, 1):
    intro, body = f"{OUT}/i{n:02d}.wav", f"{OUT}/s{n:02d}.wav"
    if not synth(f"Ses {n}.", announcer, intro) or not synth(SAMPLE, v, body): continue
    parts += [intro, body]
    lines.append(f"{n}. {v}")
    print(f"  {n}. {v}")

lst = f"{OUT}/liste.txt"
with open(lst, "w") as f:
    for p in parts: f.write(f"file '{os.path.basename(p)}'\nfile 'gap.wav'\n")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", "0.7", f"{OUT}/gap.wav"], check=True)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-ar", "44100", "-b:a", "128k",
                f"{OUT}/ses_ornekleri.mp3"], check=True)
for f in os.listdir(OUT):
    if f.endswith(".wav") or f == "liste.txt": os.remove(os.path.join(OUT, f))
open(f"{OUT}/ses_listesi.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("Hazır:", f"{OUT}/ses_ornekleri.mp3")
