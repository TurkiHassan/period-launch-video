# edge-correlation alignment check of night/dawn against day. Needs shift (0,0) — any offset makes the sunrise "swim".
from PIL import Image
import numpy as np, glob
def edges(p):
    a = np.asarray(Image.open(p).convert("L").resize((512, 512))).astype(float)
    return np.abs(np.diff(a, axis=1))[:-1] + np.abs(np.diff(a, axis=0))[:, :-1]
d = edges(glob.glob("assets/gen/day-src.*")[0])
for n in ("night", "dawn"):
    f = glob.glob(f"assets/gen/{n}-src.*")
    if not f: print(n, "missing"); continue
    e = edges(f[0]); best = None
    for dx in range(-10, 11):
        for dy in range(-10, 11):
            c = np.corrcoef(np.roll(np.roll(e, dy, 0), dx, 1)[12:-12, 12:-12].ravel(), d[12:-12, 12:-12].ravel())[0, 1]
            if best is None or c > best[0]: best = (round(c, 3), dx, dy)
    ok = best[1] == 0 and best[2] == 0 and best[0] > 0.6
    print(f"{n}: corr {best[0]} shift ({best[1]},{best[2]}) @512px → {'OK' if ok else 'MISALIGNED — regenerate as an edit of day'}")
