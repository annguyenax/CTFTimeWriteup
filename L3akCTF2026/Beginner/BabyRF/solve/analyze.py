#!/usr/bin/env python3
"""
BabyRF (L3akCTF 2026 - Beginner/hardware-rf) analysis.

The 96 kHz mono WAV packs SIX parts using different techniques, each in its own
time/frequency slot, with broadband noise added to look "RF-like". This script
reproduces every decode we obtained offline and extracts the two speech segments
that still need to be transcribed by ear.

Run:  python analyze.py <path-to-BabyRF.wav>

Findings (see writeup):
  * Morse (OOK @ ~11.6 kHz, 6-16 s)          -> "R3QU1RES"   (all uppercase)
  * Spectrogram text  (8-14 kHz, ~24-30 s)   -> "Pr0c3ss1ng" (read on REVERSED audio)
  * Spectrogram digits(8-14 kHz, ~31-41 s)   -> "3851642"    (read on FORWARD audio)
  * Spectrogram text  (26-33 kHz, ~44-47 s)  -> "31337"      (read on FORWARD audio)
  * Speech segment 1  (0-4 kHz, 0-22 s)      -> voice, needs listening (speech1_clean.wav)
  * Speech segment 2  (0-4 kHz, 42-51 s)     -> voice, needs listening (speech2_clean.wav)
"""
import sys, wave
import numpy as np

path = sys.argv[1] if len(sys.argv) > 1 else "files/BabyRF.wav"
w = wave.open(path, "rb")
fr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)

# ---------- 1. Morse decode (OOK tone at 11.6 kHz) ----------
MORSE = {'.-':'A','-...':'B','-.-.':'C','-..':'D','.':'E','..-.':'F','--.':'G',
'....':'H','..':'I','.---':'J','-.-':'K','.-..':'L','--':'M','-.':'N','---':'O',
'.--.':'P','--.-':'Q','.-.':'R','...':'S','-':'T','..-':'U','...-':'V','.--':'W',
'-..-':'X','-.--':'Y','--..':'Z','-----':'0','.----':'1','..---':'2','...--':'3',
'....-':'4','.....':'5','-....':'6','--...':'7','---..':'8','----.':'9','..--.-':'_'}

seg = x[int(5.5*fr):int(16.5*fr)]
t = np.arange(len(seg))/fr
demod = seg*np.exp(-2j*np.pi*11600.0*t)
win = int(0.003*fr)
env = np.abs(np.convolve(demod, np.ones(win)/win, "same")); env /= env.max()
on = env > 0.25
runs = []; cur = on[0]; cnt = 0
for v in on:
    if v == cur: cnt += 1
    else: runs.append((cur, cnt/fr*1000)); cur = v; cnt = 1
runs.append((cur, cnt/fr*1000))
merged = []
for s, d in runs:
    if merged and d < 8:
        ps, pd = merged[-1]; merged[-1] = (ps, pd+d)
    else:
        merged.append((s, d))
while merged and not merged[0][0]: merged.pop(0)
while merged and not merged[-1][0]: merged.pop()
groups = []; sym = ""
for s, d in merged:
    if s: sym += "." if d < 150 else "-"
    elif d >= 150:
        groups.append(sym); sym = ""
if sym: groups.append(sym)
morse_text = "".join(MORSE.get(g, "?") for g in groups)
print("[Morse @11.6kHz] ->", morse_text)

# ---------- 2. Extract cleaned speech segments (for listening) ----------
def lowpass(sig, cut):
    N = len(sig); S = np.fft.rfft(sig); f = np.fft.rfftfreq(N, 1/fr)
    S[f > cut] = 0
    return np.fft.irfft(S, N)

def save_speech(t0, t1, name):
    seg = lowpass(x[int(t0*fr):int(t1*fr)], 3800)
    seg = seg/np.max(np.abs(seg))*30000
    step = fr//16000
    y = seg[::step].astype(np.int16)
    o = wave.open(name, "wb"); o.setnchannels(1); o.setsampwidth(2)
    o.setframerate(16000); o.writeframes(y.tobytes()); o.close()
    print("[speech] saved", name)

save_speech(0.0, 22.5, "speech1_clean.wav")
save_speech(41.5, 51.2, "speech2_clean.wav")

print("\nSpectrogram-drawn parts (read visually, see writeup):")
print("  reversed 24-30s -> Pr0c3ss1ng | forward 31-41s -> 3851642 | forward 44-47s -> 31337")
print("Remaining: transcribe speech1_clean.wav & speech2_clean.wav by ear.")
