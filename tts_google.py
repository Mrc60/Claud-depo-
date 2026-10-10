"""Seslendirme (Google Cloud Text-to-Speech, Chirp 3 HD Türkçe).

Her segmenti ayrı seslendirir, süreleri timeline.json'a, birleşik sesi voice.wav'a yazar.
Kullanım: python3 tts_google.py episodes/001_kolonya.json build/001
Ortam değişkenleri:
  GOOGLE_TTS_API_KEY  (zorunlu)  Google Cloud API anahtarı
  TTS_VOICE           (isteğe bağlı) tüm bölümler için tek ses zorlar; boşsa kanal ses düzeni
  TTS_RATE            (isteğe bağlı) konuşma hızı, varsayılan 1.08
"""
import base64, io, json, os, re, subprocess, sys, time, wave
import requests

KEY = os.environ["GOOGLE_TTS_API_KEY"]

# Kanalın ses düzeni (TEK1'in seçimi):
#   ana   = 23 Sadachbia (erkek, öncelikli)
#   erkek2 = 11 Enceladus, erkek3 = 20 Puck (ara sıra)
#   kadin = 14 Gacrux (ara sıra, konuya uygun bölümlerde)
SESLER = {"ana": "tr-TR-Chirp3-HD-Sadachbia", "erkek2": "tr-TR-Chirp3-HD-Enceladus",
          "erkek3": "tr-TR-Chirp3-HD-Puck", "kadin": "tr-TR-Chirp3-HD-Gacrux"}

def pick_voice(ep):
    # 1) Bölüm dosyasında "voice" varsa o (ör. "kadin" ya da tam ses adı)
    v = ep.get("voice")
    if v: return SESLER.get(v, v)
    # 2) Yoksa 10 bölümlük düzen: 7 ana, 1'er erkek2 / erkek3 / kadın
    n = int(ep.get("episode", 1)) % 10
    return {4: SESLER["erkek2"], 7: SESLER["erkek3"], 0: SESLER["kadin"]}.get(n, SESLER["ana"])
RATE = float(os.environ.get("TTS_RATE", "1.08"))
URL = "https://texttospeech.googleapis.com/v1/text:synthesize"
GAP = 0.28
SR = 24000

from sayilar import temizle as clean  # kesme işareti + sayıları yazıya çevirir

def synth(text):
    body = {"input": {"text": clean(text)},
            "voice": {"languageCode": "tr-TR", "name": VOICE},
            "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": SR, "speakingRate": RATE}}
    for attempt in range(4):
        r = requests.post(URL, params={"key": KEY}, json=body, timeout=60)
        if r.status_code == 200:
            return base64.b64decode(r.json()["audioContent"])
        if r.status_code in (429, 500, 503):
            time.sleep(2 ** attempt); continue
        sys.exit(f"Google TTS hatası {r.status_code}: {r.text[:400]}")
    sys.exit("Google TTS: tekrar denemeler başarısız")

ep = json.load(open(sys.argv[1], encoding="utf-8"))
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
VOICE = os.environ.get("TTS_VOICE") or pick_voice(ep)

# Kanal kuralı: her videonun son cümlesi takip çağrısı (bölüm dosyasında "takip_cagrisi": false ile kapatılabilir)
CTA = "Daha fazlası için takip et."
if ep.get("takip_cagrisi", True) and ep["segments"]:
    son = ep["segments"][-1]
    if CTA not in son["say"]:
        son["say"] = son["say"].rstrip() + " " + CTA
        son["caption"] = son["caption"].rstrip() + " " + CTA
        son["key"] = list(son.get("key", [])) + ["takip"]

timeline, parts, t = [], [], 0.35
for i, seg in enumerate(ep["segments"]):
    wav_path = os.path.join(out, f"seg{i:02d}.wav")
    data = synth(seg["say"])
    # LINEAR16 yanıtı WAV başlığıyla gelir; yine de güvenli şekilde yeniden yaz
    try:
        with wave.open(io.BytesIO(data)) as w:
            frames, rate = w.readframes(w.getnframes()), w.getframerate()
    except wave.Error:
        frames, rate = data, SR
    with wave.open(wav_path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(frames)
    dur = len(frames) / 2 / rate
    timeline.append({**seg, "start": round(t, 3), "end": round(t + dur, 3)})
    parts.append((wav_path, t))
    t += dur + GAP
    print(f"  seg {i}: {dur:.1f} sn")

total = t + 1.2
json.dump({"episode": ep, "segments": timeline, "duration": round(total, 3), "voice": VOICE},
          open(os.path.join(out, "timeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

inputs, filters = [], []
for k, (wav_path, start) in enumerate(parts):
    inputs += ["-i", wav_path]
    ms = int(start * 1000)
    filters.append(f"[{k}:a]adelay={ms}|{ms}[a{k}]")
mix = "".join(f"[a{k}]" for k in range(len(parts)))
filters.append(f"{mix}amix=inputs={len(parts)}:normalize=0,apad=whole_dur={total}[v]")
subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filters),
                "-map", "[v]", "-ar", "44100", "-ac", "1", os.path.join(out, "voice.wav")], check=True)
print(f"Seslendirme tamam: {len(parts)} segment, {total:.1f} sn, ses: {VOICE}")
