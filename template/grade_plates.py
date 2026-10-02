# assets/gen/{day,night,dawn,outside}-src.(png|jpg) → assets/img/<plate>.jpg (1440²) + <plate>-blur.jpg for glass.
# Night is pushed darker so white glass UI reads; a gentle vignette on all plates. Missing dawn → blended from day+night.
from PIL import Image, ImageFilter
import numpy as np, glob, sys
def src(n):
    f = sorted(glob.glob(f"assets/gen/{n}-src.*"))
    return Image.open(f[0]).convert("RGB") if f else None
def sq(im):   # center-crop to square, resize to 1440
    w, h = im.size; s = min(w, h); im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))
    return im.resize((1440, 1440), Image.LANCZOS)
arr = lambda im: np.asarray(im).astype(np.float32) / 255
img = lambda a: Image.fromarray((np.clip(a, 0, 1) * 255 + .5).astype(np.uint8))
yy, xx = np.mgrid[0:1440, 0:1440] / 1439.0
vig = 1 - 0.5 * (((xx - .5) ** 2 + (yy - .5) ** 2) * 2.0)
day, night, dawn, out = (src(n) for n in ("day", "night", "dawn", "outside"))
if day is None or night is None or out is None: sys.exit("need assets/gen/day-src, night-src and outside-src")
day, night, out = arr(sq(day)), arr(sq(night)), arr(sq(out))
dawn = arr(sq(dawn)) if dawn is not None else np.clip((day * 0.75 + night * 0.25) * [1.12, 0.88, 0.70], 0, 1)
plates = {"night": night ** 1.25 * 0.78 * vig[..., None] ** 1.2, "dawn": dawn * vig[..., None] ** 0.5,
          "day": day * vig[..., None] ** 0.3, "outside": out * vig[..., None] ** 0.2}
for k, a in plates.items():
    im = img(a); im.save(f"assets/img/{k}.jpg", quality=93)
    im.filter(ImageFilter.GaussianBlur(34)).save(f"assets/img/{k}-blur.jpg", quality=90)
sh = Image.new("RGB", (1440, 360))
for i, k in enumerate(plates): sh.paste(Image.open(f"assets/img/{k}.jpg").resize((360, 360)), (i * 360, 0))
sh.save("out/plates.jpg") if __import__("os").makedirs("out", exist_ok=True) is None else None
print("plates → assets/img/*.jpg  (preview out/plates.jpg)")
