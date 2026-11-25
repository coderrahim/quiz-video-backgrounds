# Production Pipeline & QC

## Tool options
- **Stills:** Midjourney (`--ar 16:9 --style raw`, use `--sref`/`--cref` of master for recolours), Flux/Ideogram, or GPT-image / Gemini image *edit* mode for recolours (best consistency).
- **Animation:** image-to-video (Runway, Kling, Luma, Veo) from each still, **or** build motion procedurally in After Effects / Remotion for guaranteed loops and pixel-identical layouts across colours (recommended for designs 1, 2, 6, 8).
- **Upscale** to 1920×1080 if needed (Topaz / Real-ESRGAN), then run `scripts/loop_encode.sh`.

## Per-design steps (repeat 10×)
1. Generate 4–8 candidates of the **Blue** still; pick the best, lock the seed.
2. Check safe-zone (centre 60 % clean) and text-readability (overlay white + dark sample text).
3. Create Green/Purple/Orange/Pink via the *recolour prompt* with the master as reference. Reject any where layout shifts.
4. Animate each still (video prompt); generate ≥ 22 s or ping-pong a shorter clip.
5. `scripts/loop_encode.sh in.mp4 out.mp4` → 21 s, 1080p, 30 fps, crossfaded seamless loop, light grain.
6. QC (below), name `QB{NN}_{slug}_{color}.mp4`.

## Consistency cheat-sheet
Same seed + same reference image + hex codes in every prompt; keep luminance structure identical (desaturate-compare the 5 versions); animation prompt identical across colours.

## QC checklist (each of 50)
- [ ] 1920×1080, 16:9, 21.0 s, H.264 yuv420p
- [ ] Loop point invisible (play 3× in a row)
- [ ] No text/logos/watermarks/artifacts/warping
- [ ] Centre clean; text placed over it stays readable
- [ ] Motion subtle, no flicker/flash
- [ ] Same layout as its 4 siblings; palette matches `docs/01-design-system.md`
- [ ] No banding in gradients (check at 100 %)

## Delivery
```
deliverables/
  01_neon-arena/ QB01_neon-arena_green.mp4 ... _pink.mp4
  ...
  10_crystal-cubes/
```
Plus a contact sheet (one thumbnail per file) for client review.

## Regenerating docs
Edit `scripts/data.py`, then `python3 scripts/generate.py`.
