# The real macOS pointer is an Apple system asset, so it is not redistributed: copy it from this Mac
# and derive the purple "agent" variant. Runs automatically from new_project.sh.
import shutil, sys, os
import numpy as np
from PIL import Image
SYS = "/System/Library/PrivateFrameworks/AccessibilitySupport.framework/Versions/A/Frameworks/AccessibilityFoundation.framework/Versions/A/Resources/Cursors-macOS16/default-pointer-3.png"
if os.path.exists("assets/img/pointer.png") and os.path.exists("assets/img/pointer-purple.png"): sys.exit(0)
if not os.path.exists(SYS): sys.exit("macOS pointer not found — place a 280×400 pointer PNG (tip at 50,49) at assets/img/pointer.png")
shutil.copy(SYS, "assets/img/pointer.png")
a = np.asarray(Image.open("assets/img/pointer.png").convert("RGBA")).astype(float)
agent = sys.argv[1] if len(sys.argv) > 1 else "#7C5CFF"
rgb = np.array([int(agent[i:i + 2], 16) for i in (1, 3, 5)], float)
mix = (1 - a[..., :3].mean(2) / 255)[..., None]
a[..., :3] = a[..., :3] * (1 - mix) + rgb * mix
Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save("assets/img/pointer-purple.png")
print("pointers → assets/img/pointer.png, pointer-purple.png")
