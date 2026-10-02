---
name: period-launch-video
description: Make a 24-second square (1440², 60fps) looping product launch video where the whole story happens *inside the period of the wordmark* — iris opens onto a night photo, glass UI morphs ask → find → write → night → results → phone lock screen → proof → CTA, then closes back into the period beside the app icon. One canvas, pure seek(t), Playwright render with motion blur, beat-synced SFX, -14 LUFS. Arabic RTL template (Geist + Thmanyah when present, else IBM Plex Sans Arabic), config-driven. Use this whenever the user asks for "the night-shift video", "نفس فيديو النقطة", "فيديو إطلاق مربع", "إعلان يحدث داخل النقطة", a launch/promo video like the مستخرج one, or pastes a brief with "inside the period of the wordmark" / iOS glass panels / goo-split pills — even if they don't name this skill. Also covers getting the matched night/day photos (Higgsfield, local Codex image_gen, or ready prompts for Gemini/ChatGPT).
---

# Period launch video

A 24 s loop in which the product's whole job plays out inside the period of its wordmark. Everything ships in `template/`: the renderer (`index.html`, all content in `config.js`), the render, scan and audio scripts, fonts, the real macOS pointer, and peak-measured SFX. Your work is mostly **choosing content and photos, then running the pipeline**. Read `references/craft.md` once before changing any motion. It holds the direction, the beat map, and the gotchas that are already solved.

## Workflow

### 1 · Set up
```bash
~/.claude/skills/period-launch-video/scripts/new_project.sh <project>/brag-output/<slug>
```
Put the output inside the user's project. Use a gitignored folder such as `brag-output/` if it exists. The script also copies the real macOS pointer from this Mac (`make_pointers.py`, not redistributed) and installs Playwright. To match the original look, drop Thmanyah Sans woff2 files (`thmanyah-sans-{400,500,700}.woff2`) into `assets/fonts/`. Without them, IBM Plex Sans Arabic is used.

### 2 · Gather inputs from the project (ask only for what's missing)
- **Identity from the published version.** Use the App Store screenshots, the iOS asset catalog (icon, colors) and the app's own sample data and copy. Ignore stale web assets. If you can't tell which version is live, ask. This was the main correction from the first run.
- **Icon:** copy the square app icon to `assets/img/icon.png`. The template applies the iOS corner mask itself.
- **Song:** use the project's existing track if there is one; otherwise ask. Run `python3 find_hit.py assets/music/song.mp3` and set `config.song.hit` (≈ the reported hit − 0.04) and `bpm`. `enterAt` (default 3.10) is when the hit lands, at the first pill. Keep `enterAt + 20 beats` around 13.5 s so Results lands on beat 20.
- **Copy:** fill in `config.js`: name (one word, it becomes the black wordmark plus the period), tagline, two open lines, the ask pill, the job, find/write/night labels, 3 results, notifications, 5 library rows, the chart value, and the CTA. Keep every number consistent across beats. Western digits. Keep it strict JSON, because `audio.py` parses it.
- **Honesty check:** if the story implies something the product doesn't do (overnight batch work, for example), say so before rendering and offer neutral wording.

### 3 · Photos (four plates)
Follow `references/image-prompts.md`. Pick the route by what's available:
1. **Higgsfield MCP with credits.** Day first, then night and dawn as *edits* of the day job, plus outside. Preflight cost first.
2. **Local Codex** (`which codex`). `scripts/codex_image.sh` uses Codex's built-in image_gen on the user's ChatGPT subscription.
3. **No credits and no Codex.** Give the user the four filled-in prompts (Gemini for the edits) and wait for the files.

Then:
```bash
python3 check_align.py      # night/dawn must be shift (0,0) vs day
python3 grade_plates.py     # → assets/img/*.jpg + blurred copies; preview out/plates.jpg
```

### 4 · Beat map + six stills → approval before rendering
```bash
node stills.mjs 1.30 7.35 10.10 14.60 17.30 23.25     # open, find, write, results, phone, out
python3 sheet.py out/review-sheet.jpg out/stills/t{1.30,7.35,10.10,14.60,17.30,23.25}.png
```
Look at every still yourself first: text fits, nothing cropped, glass readable over the plate. Then show the user the sheet (SendUserFile) and a beat-map table built from `T` in `index.html`. Render only after they approve.

### 5 · Render, verify, deliver
```bash
./build.sh out/<slug>-launch.mp4     # 4 render workers → scan.py + scan_local.py → timeline + audio → H.264/AAC
```
- `scan.py` must report a seam diff of about 0 (a clean loop) and no spikes or steps.
- `scan_local.py` hits are fine when they are counters or typing. Anything else is a real pop: find which hand-off caused it and fix it. Then re-render just those frames with `node render.mjs a b` and re-encode with the ffmpeg line from `build.sh`.
- Pull a frame at the end of each counter and confirm it shows the exact final number.
- Report the specs (1440², 60fps, 1440 frames, 24.0 s, LUFS, peak), any open honesty flags, and the file path.

## Adapting beyond the defaults
- **Retime:** edit `T` in `index.html` (keep 0.8 s glides), then rerun `node timeline.mjs && python3 audio.py`.
- **Library rows** are fixed at 5 by the layout. The chart axis has 3 labels (start, middle, end).
- **LTR products** (English wordmark): the template is laid out RTL. The period sits at the left end, rows and pills anchor right, and scans and charts run right→left. For LTR, mirror those anchors (`align`, the `R`/`L` edges, `scanX`, `cpt`) and put the icon on the left. Allow time for this and check every still.
