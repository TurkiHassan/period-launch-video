# soundtrack: the song enters on its hit at config.song.enterAt; every SFX is placed so its *measured peak*
# lands on its event. Events are tied to beat-table names (timeline.json), so retiming index.html moves the sound too.
# Output: out/mix.wav, two-pass loudnorm to -14 LUFS / -1 dBTP.
import json, subprocess, numpy as np, wave, re, os
SR, LEN = 48000, 24.0; N = int(SR * LEN)
cfg = json.loads(re.sub(r"^\s*window\.CONFIG\s*=\s*|;\s*$", "", open("config.js").read().strip()))
tl = json.load(open("timeline.json")); T = tl["T"]
peaks = json.load(open("assets/sfx/peaks.json"))
song = cfg["song"]; P = song["enterAt"]; beat = 60 / song["bpm"]
mix = np.zeros((N, 2), np.float32)
def load(name):
    w = wave.open(f"assets/sfx/{name}.wav"); return np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32) / 32768
def put(name, t, vol=0.5):
    a = load(name) * vol; s = int(round((t - peaks[name]["peak"]) * SR))
    if s < 0: a, s = a[-s:], 0
    e = min(N, s + len(a)); mix[s:e] += a[: e - s]
def at(key, off=0.0): return (T[key] if isinstance(key, str) else key) + off
EV = [  # (sfx, beat-table key or seconds, offset, volume)
  ("card-slide-1", "lettersIn", .40, .45), ("card-shove-1", "irisOpen", .35, .55),
  ("rollover2", "line1In", .35, .35), ("rollover2", "line2In", .35, .35),
  ("impactGlass_light_001", "pillIn", .02, .55), ("mouseclick1", "click1", 0, .7), ("card-slide-2", "toInput", .33, .30),
  ("click_002", "send", 0, .7), ("select_008", "send", .02, .4), ("card-slide-3", "toDot", .28, .28), ("drop_002", "ripple", 0, .55),
  ("card-fan-1", "scan", .5, .35), ("cards-pack-open-1", "pour", .5, .45),
  ("mouseclick1", "save", 0, .7), ("switch_005", "save", .05, .45),
  ("impactGlass_medium_000", "orb", .40, .38), ("rollover4", "sleepIn", .40, .35),
  ("switch7", "clock1", .3, .35), ("switch7", "clock2", .3, .35), ("switch7", "clock3", .3, .35),
  ("impactSoft_heavy_000", "blackFlood", .45, .45),
  ("impactPunch_medium_000", "split", .05, .50), ("drop_003", "split", .35, .40),
  ("drop_001", "check1", .25, .45), ("drop_001", "check2", .25, .40), ("drop_001", "check3", .25, .38),
  ("impactSoft_medium_001", "merge", .65, .50), ("card-shove-2", "toScreen", .35, .45),
  ("bong_001", "n1", .40, .40), ("impactGlass_light_002", "n2", .40, .35), ("impactGlass_light_002", "n3", .40, .30),
  ("click_003", "tap", 0, .6), ("mouseclick1", "tap", 0, .5), ("card-slide-5", "open", .28, .35), ("card-slide-3", "toCard", .35, .28),
  ("card-place-1", "tiles", .30, .30), ("card-place-2", "tiles", .39, .28), ("card-place-3", "tiles", .48, .28), ("card-place-4", "tiles", .57, .28), ("card-place-1", "tiles", .66, .26),
  ("rollover1", "hover", .35, .30), ("card-slide-2", "toChart", .30, .30), ("card-fan-2", "line", .50, .25),
  ("impactSoft_heavy_000", "flood", .35, .45), ("mouseclick1", "ctaClick", 0, .7),
  ("drop_002", "toEnd", .50, .45), ("card-shove-1", "irisClose", .45, .45), ("card-slide-1", "lettersOut", .40, .40),
  ("impactSoft_medium_001", "irisClose", .80, .35),
]
for name, key, off, vol in EV: put(name, at(key, off), vol)
keys = [f"key-{i:02d}" for i in (1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23)]
J, Bd = tl["JOB"], tl["BODY"]
for i, ch in enumerate(J):                                   # user typing, one key per glyph
    if ch != " ": put(keys[i % 12], T["typeA"] + (T["typeB"] - T["typeA"]) * (i + 1) / len(J), .55)
for i in range(0, len(Bd), 2):                               # agent typing, every other glyph
    put(keys[(i * 7) % 12], T["typeC"] + (T["typeD"] - T["typeC"]) * (i + 1) / len(Bd), .35)
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(song["hit"]), "-t", str(LEN - P), "-i", song["file"], "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
m = np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
fo = int(0.8 * SR); m[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
m[: int(.004 * SR)] *= np.linspace(0, 1, int(.004 * SR))[:, None]
s = int(P * SR); mix[s:s + len(m)] += m[: N - s] * 0.85
os.makedirs("out", exist_ok=True)
w = wave.open("out/mix-raw.wav", "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
# two-pass loudnorm → -14 LUFS, then trim to land exactly
st = subprocess.run(["ffmpeg", "-hide_banner", "-y", "-i", "out/mix-raw.wav", "-af", "loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
d = json.loads(st[st.rindex("{"):st.rindex("}") + 1])
af = f"loudnorm=I=-14:TP=-1.0:LRA=11:measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}:linear=true,aresample=48000"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "out/mix-raw.wav", "-af", af, "-c:a", "pcm_s16le", "out/mix-ln.wav"], check=True)
meas = subprocess.run(["ffmpeg", "-hide_banner", "-i", "out/mix-ln.wav", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", meas)[-1])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "out/mix-ln.wav", "-af", f"volume={-14 - I:.2f}dB", "-c:a", "pcm_s16le", "out/mix.wav"], check=True)
print(f"out/mix.wav  ({len(EV)} sfx events, loudness corrected by {-14 - I:+.2f} dB)")
