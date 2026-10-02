# find "big hit" candidates in a song: strong bass onsets right after a quieter stretch (drops), in the first N seconds.
# usage: python3 find_hit.py assets/music/song.mp3 [seconds=45]
import subprocess, numpy as np, sys
f = sys.argv[1]; L = float(sys.argv[2]) if len(sys.argv) > 2 else 45; sr = 22050
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-t", str(L), "-i", f, "-ac", "1", "-ar", str(sr), "-af", "lowpass=f=150", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
h = int(sr * 0.01); env = np.array([np.abs(x[i:i + h]).max() for i in range(0, len(x) - h, h)])
c = []
for i in range(150, len(env) - 50):
    before = env[i - 150:i - 5].mean(); after = env[i:i + 50].mean()
    if env[i] > 0.4 * env.max() and env[i - 6:i].max() < 0.15 * env.max(): c.append((after / max(before, 1e-3), i * 0.01))
c.sort(reverse=True); seen = []
for r, t in c:
    if all(abs(t - s) > 1.0 for s in seen): seen.append(t); print(f"hit at {t:6.2f}s  (energy jump ×{r:.2f})")
    if len(seen) >= 6: break
print("→ use the strongest early one; set config.song.hit ≈ hit − 0.04 (the threshold fires slightly after the transient starts)")
