# flag single-frame jumps: a frame that differs from both neighbours far more than they differ from each other,
# and step discontinuities: a frame-to-frame change far above its local neighbourhood. Includes the loop seam.
import numpy as np, glob, sys
from PIL import Image
fs = sorted(glob.glob("out/frames/f*.png")); n = len(fs)
F = np.stack([np.asarray(Image.open(f).convert("L").resize((240, 240), Image.BILINEAR), np.float32) for f in fs])
d = np.array([np.abs(F[i] - F[i - 1]).mean() for i in range(n)])          # d[0] = seam 1439→0
spikes, steps = [], []
for i in range(n):
    a, b2 = F[i - 1], F[(i + 1) % n]
    skip = np.abs(b2 - a).mean()
    if d[i] > 1.2 and np.abs(F[i] - b2).mean() > 1.2 and d[i] > 2.5 * max(skip, 0.3): spikes.append((i, round(d[i], 2), round(skip, 2)))
    nb = np.r_[d[max(0, i - 4):i], d[i + 1:i + 5]]
    if d[i] > 1.5 and d[i] > 4 * max(np.median(nb), 0.25): steps.append((i, round(d[i], 2), round(float(np.median(nb)), 2)))
print("frames", n, "seam diff", round(d[0], 3), "max diff", round(d.max(), 2), "at", int(d.argmax()))
print("single-frame spikes:", spikes)
print("step jumps:", steps)
np.save("out/diffs.npy", d)
