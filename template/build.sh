#!/bin/zsh
# full pipeline after approval: frames (4 workers) → jump scans → audio → encode
set -e
cd "${0:A:h}"
OUT=${1:-out/launch.mp4}
rm -rf out/frames
node render.mjs 0 360 & node render.mjs 360 720 & node render.mjs 720 1080 & node render.mjs 1080 1440 & wait
python3 scan.py
python3 scan_local.py
node timeline.mjs && python3 audio.py
ffmpeg -v error -y -framerate 60 -i out/frames/f%05d.png -i out/mix.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 15 \
  -pix_fmt yuv420p -profile:v high -tune film -c:a aac -b:a 320k -ar 48000 -t 24 -movflags +faststart "$OUT"
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,nb_frames -of compact "$OUT"
ffmpeg -hide_banner -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tail -2
