# The four photo plates — how to get them

The video needs four photos. Three of them must be the **same shot** (pixel-aligned), so that crossfading them reads as a real sunrise:

| file in `assets/gen/` | what | how |
|---|---|---|
| `day-src.png` | the inside world, morning | generate first |
| `night-src.png` | the same shot at deep night | **edit** of day |
| `dawn-src.png` | the same shot at sunrise (optional, but much better) | **edit** of day |
| `outside-src.png` | sunny daytime photo behind the black wordmark | generate |

Always generate day first, then make night and dawn as *edits of the day image*. A fresh generation never lines up. Run `python3 check_align.py` afterwards: it must say `shift (0,0)` for night and dawn.

## Choosing the scene

- Match the product's **published** palette and mood. Read it from the App Store screenshots or the asset catalog, not from old web images.
- Put **sky in the frame** (a window or a landscape). The night→dawn→day relight is the emotional peak of the video, and it only works if the light source is visible.
- Keep the **center calm and uncluttered**. The pill, grid, composer, orb and phone all sit at the center, and busy texture there fights the glass.
- Choose a symmetrical, front-on composition. The camera never moves sideways, so symmetry reads as intentional.
- The outside photo needs a large bright, empty area in the middle for a black wordmark. A sunlit wall with leaf or window shadows works well.

## Prompt templates

Fill in `{SCENE}` and `{PALETTE}`. Keep the prompts in English, since image models follow English best.

**1 · DAY** (new image, square 1:1, ≥1440 px):
```
Photorealistic photograph, square format, symmetrical front-on composition. {SCENE}. The center of the frame is calm and uncluttered. Bright clear morning daylight, soft natural light, gentle shadows. Muted palette of {PALETTE}. Editorial photography, 35mm lens, high detail, no people, no text, no logos.
```

**2 · NIGHT** (edit; attach the day image):
```
Edit this exact photograph: keep the identical composition, camera position, framing and every object in exactly the same place and size. Only change the time of day to deep night: a dark navy night sky with faint stars and a thin crescent moon, the landscape as dark silhouettes, the scene lit only by soft cool blue moonlight, deep shadows. No lamps, no artificial light, no added objects, no text. Photorealistic, quiet, calm.
```

**3 · DAWN** (edit; attach the day image):
```
Edit this exact photograph: keep the identical composition, camera position, framing and every object in exactly the same place and size. Only change the time to sunrise: the sun just rising on the horizon, a glowing warm peach and soft gold sky with pink clouds, long low golden light washing the scene, soft long shadows. No added objects, no text. Photorealistic, serene.
```

**4 · OUTSIDE** (new image):
```
Photorealistic photograph, square, front-on. A warm {WALL COLOR} plaster wall bathed in bright midday sunlight, with soft dappled shadows of leaves and a window frame cast across it. {ONE OR TWO SMALL BRAND-COLORED PROPS AT THE EDGES}. The large central area of the wall is calm, bright and empty. Muted palette of {PALETTE}, fresh sunny daytime mood. Editorial interior photography, no people, no text, no logos.
```

Worked example (مستخرج PDF, ivory/sage Studio palette):
`{SCENE}` = "A calm minimal study: a large arched window centered in the frame fills the upper two thirds, warm ivory plaster walls around it, sage green linen curtains gathered at both sides. Through the window: gentle rolling hills with a few olive trees and a wide open sky with soft scattered clouds. In the lower third, a light oak desk in front of the window holds a neat stack of printed paper documents, a closed linen notebook and a small sage green ceramic vase with an olive branch"
`{PALETTE}` = "ivory, cream, sage green and warm wood"

## Route A: Higgsfield MCP (when the account has credits)

1. Check `balance`, then preflight with `get_cost: true`. `gpt_image_*` models need a paid plan. On the free plan, `nano_banana_pro` at 2k is about 2 credits per image and is excellent at alignment-preserving edits.
2. Generate DAY. Then generate NIGHT and DAWN with `medias: [{value: <day job_id>, role: "image_references"}]`. Generate OUTSIDE as a new image.
3. Download each `result_url` with curl into `assets/gen/<name>-src.png`.

If the balance can't cover 4 images (8 credits on nano_banana_pro), go to route B or C. Don't silently drop the dawn plate. Tell the user that `grade_plates.py` will fake dawn from day and night if they choose to skip it.

## Route B: local Codex CLI (ChatGPT subscription, no API key)

`scripts/codex_image.sh` drives `codex exec` with Codex's built-in `image_gen` tool. Each image takes about 60–120 s and comes out around 1254 px (grading upscales it to 1440).

```bash
S=~/.claude/skills/period-launch-video/scripts
$S/codex_image.sh assets/gen/day-src.png "<DAY prompt>"
# night and dawn are edits of the day plate; the two can run in parallel
$S/codex_image.sh assets/gen/night-src.png "<NIGHT change, e.g. deep night with a thin crescent moon…>" assets/gen/day-src.png &
$S/codex_image.sh assets/gen/dawn-src.png  "<DAWN change>" assets/gen/day-src.png &
$S/codex_image.sh assets/gen/outside-src.png "<OUTSIDE prompt>" &
wait
```

When a reference is given, the script already wraps the prompt in "keep the identical composition…", so pass only the change. Check `which codex` first. If it isn't installed or isn't logged in (`codex login`), fall back to route C. This was tested on codex-cli 0.154: the day→night edit came back at shift (0,0).

## Route C: give the user the prompts (Gemini / ChatGPT web)

When there are no credits and no Codex, hand the user the four filled-in prompts plus these steps, written in their language:

1. **Gemini** (Nano Banana) is the best choice for the night and dawn edits, because it keeps composition exactly. ChatGPT is fine for day and outside.
2. Day: open a new chat, paste prompt 1 and ask for a square 1:1 image. Download it.
3. Night: in the **same chat** (or a new one with the day image attached), paste prompt 2. Do the same for dawn with prompt 3.
4. Outside: prompt 4, in any chat.
5. Save them as `day-src.png`, `night-src.png`, `dawn-src.png` and `outside-src.png` in `<project>/assets/gen/`, then tell Claude.

Then run `check_align.py`. If night or dawn is misaligned, ask for that edit again with the day image attached.
