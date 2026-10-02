# localized jump detector on 12×12 tiles (each tile = 120px of the 1440 frame)
#  pop  : frame i differs from both neighbours, while the neighbours match each other
#  step : a big change in one frame with near-stillness in the frames on either side (an instant cut/pop-on)
import numpy as np, glob
from PIL import Image
fs = sorted(glob.glob("out/frames/f*.png")); n = len(fs)
F = np.stack([np.asarray(Image.open(f).convert("L").resize((240, 240), Image.BILINEAR), np.float32) for f in fs])
T = lambda X: np.abs(X).reshape(n, 12, 20, 12, 20).mean((2, 4))
Dp = T(F - np.roll(F, 1, 0))           # f[i]-f[i-1]
Dn = np.roll(Dp, -1, 0)                # f[i+1]-f[i]
Sk = T(np.roll(F, -1, 0) - np.roll(F, 1, 0))
pops = np.argwhere((np.minimum(Dp, Dn) > 3) & (Sk < 0.35 * np.minimum(Dp, Dn)))
Dpp = np.roll(Dp, 1, 0)                # f[i-1]-f[i-2]
steps = np.argwhere((Dp > 4) & (Dpp < 0.15 * Dp) & (Dn < 0.15 * Dp))
print("pops:", [(int(i), round(i / 60, 3), int(y), int(x), round(float(Dp[i, y, x]), 1)) for i, y, x in pops][:40])
print("steps:", [(int(i), round(i / 60, 3), int(y), int(x), round(float(Dp[i, y, x]), 1)) for i, y, x in steps][:40])
