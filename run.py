"""Bir bölümü baştan sona üretir: fotoğraflar -> seslendirme -> video -> YouTube metni.

Kullanım: python3 run.py episodes/001_kolonya.json
Çıktılar out/ klasörüne: <bölüm>.mp4 ve <bölüm>_youtube.txt (başlık + açıklama + atıflar)
"""
import json, os, subprocess, sys

ep_path = sys.argv[1]
ep = json.load(open(ep_path, encoding="utf-8"))
name = f"{ep['episode']:03d}_{ep['slug']}"
build, out = os.path.join("build", name), "out"
os.makedirs(out, exist_ok=True)
py = sys.executable

def step(title, *cmd):
    print(f"\n== {title} ==", flush=True)
    subprocess.run([py, *cmd], check=True)

step("Fotoğraflar (Wikimedia Commons)", "images.py", ep_path, build)
step("Seslendirme (Google TTS)", "tts_google.py", ep_path, build)
step("Video", "render.py", build, os.path.join(out, f"{name}.mp4"))

credits = open(os.path.join(build, "credits.txt"), encoding="utf-8").read()
txt = f"BAŞLIK:\n{ep['youtube_title']}\n\nAÇIKLAMA:\n{ep['youtube_description']}\n\n{credits}"
open(os.path.join(out, f"{name}_youtube.txt"), "w", encoding="utf-8").write(txt)
print(f"\nHazır: out/{name}.mp4 ve out/{name}_youtube.txt")
