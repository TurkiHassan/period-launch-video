#!/bin/zsh
# usage: new_project.sh <target-dir>   — copies the template and installs Playwright (Chromium is reused if cached)
set -e
SK="${0:A:h:h}"; DST="$1"
[[ -z "$DST" ]] && { echo "usage: new_project.sh <target-dir>"; exit 1; }
[[ -e "$DST/index.html" ]] && { echo "refusing: $DST already has an index.html"; exit 1; }
mkdir -p "$DST"; cp -R "$SK/template/." "$DST/"; mkdir -p "$DST/out" "$DST/assets/gen" "$DST/assets/music"
cd "$DST"; python3 make_pointers.py || true
npm install --silent >/dev/null 2>&1 && npx playwright install chromium >/dev/null 2>&1 || true
echo "ready: $DST"
echo "next: assets/img/icon.png (square app icon), assets/music/song.mp3, assets/gen/{day,night,dawn,outside}-src.png, edit config.js"
