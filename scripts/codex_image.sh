#!/bin/zsh
# Generate (or edit) one image through the local Codex CLI's built-in image_gen tool — runs on the user's
# ChatGPT subscription, no API key. Typical time 60–120 s per image; output is ~1254 px square PNG.
#
# usage: codex_image.sh <out.png> "<prompt>" [reference.png]
#   with a reference, Codex EDITS that image (keep composition) — use this for night/dawn from the day plate.
set -e
OUT="${1:A}"; PROMPT="$2"; REF="$3"
[[ -z "$OUT" || -z "$PROMPT" ]] && { echo 'usage: codex_image.sh <out.png> "<prompt>" [reference.png]'; exit 1; }
command -v codex >/dev/null || { echo "codex CLI not found (brew install codex / npm i -g @openai/codex)"; exit 2; }
WORK=$(mktemp -d "${TMPDIR:-/tmp}/codex-img.XXXXXX")
ARGS=(exec --skip-git-repo-check --ephemeral -C "$WORK" -s workspace-write -o "$WORK/last.txt")
if [[ -n "$REF" ]]; then
  cp "${REF:A}" "$WORK/ref.png"
  # -i takes several values, so it must not sit right before the prompt
  ARGS=(exec --skip-git-repo-check -i ref.png --ephemeral -C "$WORK" -s workspace-write -o "$WORK/last.txt")
  TASK="Use your built-in image_gen tool (imagegen skill, built-in mode — not the CLI) to EDIT the attached image ref.png. Keep the identical composition, camera, framing and every object in exactly the same place and size. Change only this: $PROMPT"
else
  TASK="Use your built-in image_gen tool (imagegen skill, built-in mode — not the CLI) to generate a square image: $PROMPT"
fi
TASK="$TASK. Then copy the generated PNG from \$CODEX_HOME/generated_images/... into this folder as result.png. Reply with only the absolute path of result.png."
codex "${ARGS[@]}" "$TASK" > "$WORK/log.txt" 2>&1 || { tail -20 "$WORK/log.txt"; exit 3; }
[[ -f "$WORK/result.png" ]] || { echo "codex finished but no result.png — log: $WORK/log.txt"; tail -20 "$WORK/log.txt"; exit 4; }
mkdir -p "${OUT:h}"; cp "$WORK/result.png" "$OUT"; echo "$OUT"
