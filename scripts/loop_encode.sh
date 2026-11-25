#!/usr/bin/env bash
# Usage: loop_encode.sh input.mp4 output.mp4
# Makes a clip exactly 21 s, 1920x1080, 30 fps, and seamless: the last 1 s cross-fades into the first 1 s.
set -euo pipefail
in="$1"; out="$2"; F=1   # crossfade seconds
# input should be >= 22 s (21 + F). If shorter, ping-pong first: see docs.
ffmpeg -y -i "$in" -filter_complex "\
[0:v]scale=1920:1080:flags=lanczos,fps=30,setsar=1,split[a][b];\
[a]trim=start=0:end=$F,setpts=PTS-STARTPTS[head];\
[b]trim=start=$F:end=$((21+F)),setpts=PTS-STARTPTS[body];\
[body]split[b1][b2];\
[b1]trim=start=0:end=$((21-F)),setpts=PTS-STARTPTS[main];\
[b2]trim=start=$((21-F)):end=21,setpts=PTS-STARTPTS[tail];\
[tail][head]xfade=transition=fade:duration=$F:offset=0[blend];\
[main][blend]concat=n=2:v=1:a=0,noise=alls=2:allf=t,format=yuv420p[v]" \
 -map "[v]" -t 21 -c:v libx264 -crf 14 -preset slow -pix_fmt yuv420p -movflags +faststart -an "$out"
