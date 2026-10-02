# Craft notes: direction, beat map, gotchas

## The direction (what the template implements)

- A square video, 1440×1440 at 60fps, **24 s**, 2D only, one continuous take that **loops** (last frame = first frame).
- **The whole video happens inside the period of the wordmark.** Outside is daytime: the sunny photo behind a black wordmark. Inside is the night photo under iOS-style glass panels.
- Nothing cuts. Every scene grows out of the previous one: shapes morph, dots fly, colours change under *floods*. Every morph glides **0.8 s on cubic-bezier(.45,0,.15,1)**, and the camera zoom rides the same curve.
- The real macOS pointer, plus a second purple "agent" pointer with a label. Soft shadows grow with each shape's height.
- **Banned:** flat or gradient backgrounds made in code, camera zooms into tiny points, hard cuts, crossfades between scenes, bouncy springs, particles, glows, holds longer than 1 s, and cropped type.

## Beat map (beat k = enterAt + k × 60/BPM)

| beat | what |
|---|---|
| Open (before the song) | Letters (and the icon) slide into the period. The period glides to the center and opens like an iris onto the night. Two lines roll through a mask band. |
| Ask: B0, the song's hit | A glass pill grows in. The pointer clicks it at B1.5, it glides into an input, and the job types out. The pointer clicks send at B4.5. |
| Find | The input shrinks to a dot that ripples into a 23×15 grid. A scan sweeps right→left (RTL), `lit` dots light up, and a counter counts them. |
| Write: B9 | The lit dots pour into a glass composer. The purple agent pointer types a line, then clicks save at B13.5, and the counter runs to total. |
| Night: B14.5 | The composer becomes a glass orb with a progress ring. A clock chip rolls through 4 times. The sky relights night→dawn→day, and the sleep line rolls in. |
| Results: **B20** | The orb floods black and goo-splits into 3 result pills, and the checks pop. |
| Morning | The pills goo-merge into a Dynamic Island, which grows into a phone. The lock screen floods on from the island, then the bezel, date and time, and 3 notifications. The pointer taps the first one, which opens like iOS. |
| Proof | The screen becomes the app's library card (5 rows pop in, hover tooltip), then morphs into a chart (counter plus line drawing RTL, a hover follows the tip). A black flood from the line end becomes the CTA, and the pointer clicks it. |
| Out | The CTA shrinks to a dot, the iris closes onto it, the period glides home, the letters and icon slide out, and the tagline rises. |

All of this lives in the `T` table in `index.html`. Retiming means editing one value there, then rerunning `node timeline.mjs` so the audio follows.

## Gotchas already solved in the template (don't reintroduce)

- **Open the period; never zoom into it.** A camera zoom toward an off-centre dot swings sideways and spikes.
- **Ease the iris by area** (`irisR`), not by radius, or its first frames jump.
- **The world rides with the period:** draw the inside world at `(dx−C, dy−C)` so the closing iris stays on the CTA dot while the dot glides home.
- Every helper uses `save/restore` and multiplies `globalAlpha`, so it never overwrites the caller's alpha (otherwise fading cards pop).
- **Counters and typing read the frame's time** (`ft`), not the subframe's, otherwise digits smear in the motion blur. Round counters so they *land exactly* on the final value: the first render ended at 12,500 instead of 12,480 because it rounded to hundreds.
- **Hero hand-offs:** where the hero hides and another layer takes over (input dot → grid centre dot, orb → goo, goo → island, opened note → hero card), size, colour and alpha must match at that instant. Goo blur σ must return to exactly 0 at each hand-off, and all goo legs must finish at the same time.
- `rr(c,…,keep=true)` adds a sub-path without `beginPath`. The bezel's even-odd ring needs it. Without it, the whole screen fills black.
- The lock-screen wallpaper must differ from the world behind the phone (use the outside plate), or the phone looks transparent.
- The scanners flag counters and typed glyphs, which change discretely by design, and they flag moving iris edges in the loose pass. Judge each hit by its time and tile, not by its count.

## Lessons from the first real run (مستخرج PDF, Oct 2026)

- **Identity comes from the *published* build.** Old web assets in `public/` were rejected. Use the App Store screenshots, the iOS asset catalog (icon and colors) and the app's sample data. If unsure which version is live, ask.
- **The final frame (= first frame) carries the app icon** next to the wordmark: [icon][name][.] in RTL. The icon slides into and out of the period together with the letters.
- **Honesty check:** a "while you sleep" story implies overnight batch processing. Flag it to the user before rendering if the product doesn't actually do that, and offer neutral lines ("في ثوانٍ").
- Keep numbers consistent across beats: lit dots = composer total = results = notifications = library = chart.
- zsh: `"$VAR:l…"` is parsed as a modifier (`:l` = lowercase). Write `${VAR}` before a colon.
- `codex exec -i` takes several files, so it swallows a prompt that comes right after it. Put another flag between them (handled in `codex_image.sh`).
