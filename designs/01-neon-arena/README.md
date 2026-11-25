# 01 · Neon Arena

_Esports-stage perspective grid with corner light beams._

## Visual composition
One-point perspective. A glowing grid floor recedes from the bottom third toward a soft horizon glow behind the centre; two tall light beams rise from the lower corners and cross diagonally outward; a thin neon frame hugs the edges. Centre 60% is a smooth dark-to-primary gradient.

## Design details
- **Shapes:** Thin neon lines, perspective grid cells, tall translucent light beams, small corner brackets and chevrons.
- **Pattern:** Square grid in perspective with every 4th line brighter.
- **Lighting:** Horizon glow, additive beams, soft bloom on grid intersections.
- **Gradients:** Vertical: base -> primary at horizon -> base at top; accent only on lines.
- **Animation (21 s loop):** Grid lines scroll slowly toward camera (one cell per 3.5 s, loops exactly); beams breathe in opacity on a 10.5 s sine; a few particles drift up (21 s path).

## Workflow
1. Generate the **master** in **Blue** with the still prompt (iterate until approved; save the seed).
2. Generate the other four colours with the *recolor prompt* using the master as image reference (image-to-image / edit mode), or by re-running the still prompt with the same seed + layout reference.
3. Animate each still with its video prompt, then run `scripts/loop_encode.sh`.

## Prompts
### Green — `QB01_neon-arena_green.mp4`
**Still prompt**
```
Esports arena background, 16:9. A glowing neon perspective grid floor in the bottom third receding to a soft glowing horizon, two tall translucent light beams rising from the lower left and lower right corners, thin neon corner brackets, subtle bloom on grid intersections, smooth dark gradient sky above. Large clean empty dark-gradient area in the centre. Colour scheme (GREEN): deep forest-emerald, vivid emerald green, teal, neon mint, pale mint-white, tiny lemon-yellow sparks. Exact hex palette: background base #03231A, primary #0E9F6E, secondary #14B8A6, accent glow #34F5A5, highlights #D5FFEC, tiny sparks #FFE45C. Style: professional quiz-show and gaming video background, modern, polished, high-end motion-graphics look, smooth gradients, crisp geometry, subtle bloom, 16:9 widescreen, 1920x1080, ultra sharp, no banding. IMPORTANT composition rules: keep the central 60% of the frame (roughly x 20-80%, y 15-85%) clean, smooth and low-contrast so quiz text can be placed on top; put all detail around edges and corners; balanced, not overcrowded. Negative prompt: text, letters, numbers, words, logos, watermark, signature, people, faces, hands, animals, objects, topic-specific illustrations, icons of real brands, clutter in the centre, harsh noise, blur artifacts, low resolution, cropped borders.
```
**Recolour prompt (from master)**
```
Using the attached master image of design 'Neon Arena' as the exact reference, keep the composition, shapes, positions, lighting and level of detail IDENTICAL. Change ONLY the colour scheme to GREEN: deep forest-emerald, vivid emerald green, teal, neon mint, pale mint-white, tiny lemon-yellow sparks (base #03231A, primary #0E9F6E, secondary #14B8A6, accent #34F5A5, highlight #D5FFEC, spark #FFE45C). Preserve the same brightness/contrast structure so text stays readable. Negative prompt: text, letters, numbers, words, logos, watermark, signature, people, faces, hands, animals, objects, topic-specific illustrations, icons of real brands, clutter in the centre, harsh noise, blur artifacts, low resolution, cropped borders.
```
**Video prompt**
```
Animate this exact image as a seamless 21-second loop, locked-off camera, no zoom or pan. Motion: Grid lines scroll slowly toward camera (one cell per 3.5 s, loops exactly); beams breathe in opacity on a 10.5 s sine; a few particles drift up (21 s path). All motion is slow, smooth and subtle; the first and last frames must match so the loop is seamless; the central area stays still and clean. Keep the green colour palette unchanged. Do not add text, logos or new objects.
```

### Purple — `QB01_neon-arena_purple.mp4`
**Still prompt**
```
Esports arena background, 16:9. A glowing neon perspective grid floor in the bottom third receding to a soft glowing horizon, two tall translucent light beams rising from the lower left and lower right corners, thin neon corner brackets, subtle bloom on grid intersections, smooth dark gradient sky above. Large clean empty dark-gradient area in the centre. Colour scheme (PURPLE): deep midnight violet, vivid royal purple, orchid, neon lavender, pale lilac-white, tiny golden-yellow sparks. Exact hex palette: background base #150836, primary #7C3AED, secondary #A855F7, accent glow #C084FC, highlights #F1E6FF, tiny sparks #FFD23F. Style: professional quiz-show and gaming video background, modern, polished, high-end motion-graphics look, smooth gradients, crisp geometry, subtle bloom, 16:9 widescreen, 1920x1080, ultra sharp, no banding. IMPORTANT composition rules: keep the central 60% of the frame (roughly x 20-80%, y 15-85%) clean, smooth and low-contrast so quiz text can be placed on top; put all detail around edges and corners; balanced, not overcrowded. Negative prompt: text, letters, numbers, words, logos, watermark, signature, people, faces, hands, animals, objects, topic-specific illustrations, icons of real brands, clutter in the centre, harsh noise, blur artifacts, low resolution, cropped borders.
```
**Recolour prompt (from master)**
```
Using the attached master image of design 'Neon Arena' as the exact reference, keep the composition, shapes, positions, lighting and level of detail IDENTICAL. Change ONLY the colour scheme to PURPLE: deep midnight violet, vivid royal purple, orchid, neon lavender, pale lilac-white, tiny golden-yellow sparks (base #150836, primary #7C3AED, secondary #A855F7, accent #C084FC, highlight #F1E6FF, spark #FFD23F). Preserve the same brightness/contrast structure so text stays readable. Negative prompt: text, letters, numbers, words, logos, watermark, signature, people, faces, hands, animals, objects, topic-specific illustrations, icons of real brands, clutter in the centre, harsh noise, blur artifacts, low resolution, cropped borders.
```
**Video prompt**
```
Animate this exact image as a seamless 21-second loop, locked-off camera, no zoom or pan. Motion: Grid lines scroll slowly toward camera (one cell per 3.5 s, loops exactly); beams breathe in opacity on a 10.5 s sine; a few particles drift up (21 s path). All motion is slow, smooth and subtle; the first and last frames must match so the loop is seamless; the central area stays still and clean. Keep the purple colour palette unchanged. Do not add text, logos or new objects.
```

### Orange — `QB01_neon-arena_orange.mp4`
**Still prompt**
```
Esports arena background, 16:9. A glowing neon perspective grid floor in the bottom third receding to a soft glowing horizon, two tall translucent light beams rising from the lower left and lower right corners, thin neon corner brackets, subtle bloom on grid intersections, smooth dark gradient sky above. Large clean empty dark-gradient area in the centre. Colour scheme (ORANGE): deep burnt-umber brown, vivid tangerine orange, amber, glowing apricot, pale cream-white, tiny cyan sparks. Exact hex palette: background base #2B0E02, primary #F97316, secondary #F59E0B, accent glow #FFB347, highlights #FFF1D6, tiny sparks #38BDF8. Style: professional quiz-show and gaming video background, modern, polished, high-end motion-graphics look, smooth gradients, crisp geometry, subtle bloom, 16:9 widescreen, 1920x1080, ultra sharp, no banding. IMPORTANT composition rules: keep the central 60% of the frame (roughly x 20-80%, y 15-85%) clean, smooth and low-contrast so quiz text can be placed on top; put all detail around edges and corners; balanced, not overcrowded. Negative prompt: text, letters, numbers, words, logos, watermark, signature, people, faces, hands, animals, objects, topic-specific illustrations, icons of real brands, clutter in the centre, harsh noise, blur artifacts, low resolution, cropped borders.
```
**Recolour prompt (from master)**
```
Using the attached master image of design 'Neon Arena' as the exact reference, keep the composition, shapes, positions, lighting and level of detail IDENTICAL. Change ONLY the colour scheme to ORANGE: deep burnt-umber brown, vivid tangerine orange, amber, glowing apricot, pale cream-white, tiny cyan sparks (base #2B0E02, primary #F97316, secondary #F59E0B, accent #FFB347, highlight #FFF1D6, spark #38BDF8). Preserve the same brightness/contrast structure so text stays readable. Negative prompt: text, letters, numbers, words, logos, watermark, signature, people, faces, hands, animals, objects, topic-specific illustrations, icons of real brands, clutter in the centre, harsh noise, blur artifacts, low resolution, cropped borders.
```
**Video prompt**
```
Animate this exact image as a seamless 21-second loop, locked-off camera, no zoom or pan. Motion: Grid lines scroll slowly toward camera (one cell per 3.5 s, loops exactly); beams breathe in opacity on a 10.5 s sine; a few particles drift up (21 s path). All motion is slow, smooth and subtle; the first and last frames must match so the loop is seamless; the central area stays still and clean. Keep the orange colour palette unchanged. Do not add text, logos or new objects.
```

### Blue — `QB01_neon-arena_blue.mp4`
**Still prompt**
```
Esports arena background, 16:9. A glowing neon perspective grid floor in the bottom third receding to a soft glowing horizon, two tall translucent light beams rising from the lower left and lower right corners, thin neon corner brackets, subtle bloom on grid intersections, smooth dark gradient sky above. Large clean empty dark-gradient area in the centre. Colour scheme (BLUE): deep navy, vivid cobalt blue, sky blue, neon cyan, pale ice-white, tiny orange sparks. Exact hex palette: background base #041030, primary #2563EB, secondary #0EA5E9, accent glow #38D5FF, highlights #DDF4FF, tiny sparks #FF8A3D. Style: professional quiz-show and gaming video background, modern, polished, high-end motion-graphics look, smooth gradients, crisp geometry, subtle bloom, 16:9 widescreen, 1920x1080, ultra sharp, no banding. IMPORTANT composition rules: keep the central 60% of the frame (roughly x 20-80%, y 15-85%) clean, smooth and low-contrast so quiz text can be placed on top; put all detail around edges and corners; balanced, not overcrowded. Negative prompt: text, letters, numbers, words, logos, watermark, signature, people, faces, hands, animals, objects, topic-specific illustrations, icons of real brands, clutter in the centre, harsh noise, blur artifacts, low resolution, cropped borders.
```
**Recolour prompt (from master)**
```
Using the attached master image of design 'Neon Arena' as the exact reference, keep the composition, shapes, positions, lighting and level of detail IDENTICAL. Change ONLY the colour scheme to BLUE: deep navy, vivid cobalt blue, sky blue, neon cyan, pale ice-white, tiny orange sparks (base #041030, primary #2563EB, secondary #0EA5E9, accent #38D5FF, highlight #DDF4FF, spark #FF8A3D). Preserve the same brightness/contrast structure so text stays readable. Negative prompt: text, letters, numbers, words, logos, watermark, signature, people, faces, hands, animals, objects, topic-specific illustrations, icons of real brands, clutter in the centre, harsh noise, blur artifacts, low resolution, cropped borders.
```
**Video prompt**
```
Animate this exact image as a seamless 21-second loop, locked-off camera, no zoom or pan. Motion: Grid lines scroll slowly toward camera (one cell per 3.5 s, loops exactly); beams breathe in opacity on a 10.5 s sine; a few particles drift up (21 s path). All motion is slow, smooth and subtle; the first and last frames must match so the loop is seamless; the central area stays still and clean. Keep the blue colour palette unchanged. Do not add text, logos or new objects.
```

### Pink — `QB01_neon-arena_pink.mp4`
**Still prompt**
```
Esports arena background, 16:9. A glowing neon perspective grid floor in the bottom third receding to a soft glowing horizon, two tall translucent light beams rising from the lower left and lower right corners, thin neon corner brackets, subtle bloom on grid intersections, smooth dark gradient sky above. Large clean empty dark-gradient area in the centre. Colour scheme (PINK): deep plum-magenta, vivid hot pink, rose, neon bubblegum pink, pale blush-white, tiny aqua sparks. Exact hex palette: background base #2A0620, primary #EC4899, secondary #F472B6, accent glow #FF7AC6, highlights #FFE4F3, tiny sparks #5EEAD4. Style: professional quiz-show and gaming video background, modern, polished, high-end motion-graphics look, smooth gradients, crisp geometry, subtle bloom, 16:9 widescreen, 1920x1080, ultra sharp, no banding. IMPORTANT composition rules: keep the central 60% of the frame (roughly x 20-80%, y 15-85%) clean, smooth and low-contrast so quiz text can be placed on top; put all detail around edges and corners; balanced, not overcrowded. Negative prompt: text, letters, numbers, words, logos, watermark, signature, people, faces, hands, animals, objects, topic-specific illustrations, icons of real brands, clutter in the centre, harsh noise, blur artifacts, low resolution, cropped borders.
```
**Recolour prompt (from master)**
```
Using the attached master image of design 'Neon Arena' as the exact reference, keep the composition, shapes, positions, lighting and level of detail IDENTICAL. Change ONLY the colour scheme to PINK: deep plum-magenta, vivid hot pink, rose, neon bubblegum pink, pale blush-white, tiny aqua sparks (base #2A0620, primary #EC4899, secondary #F472B6, accent #FF7AC6, highlight #FFE4F3, spark #5EEAD4). Preserve the same brightness/contrast structure so text stays readable. Negative prompt: text, letters, numbers, words, logos, watermark, signature, people, faces, hands, animals, objects, topic-specific illustrations, icons of real brands, clutter in the centre, harsh noise, blur artifacts, low resolution, cropped borders.
```
**Video prompt**
```
Animate this exact image as a seamless 21-second loop, locked-off camera, no zoom or pan. Motion: Grid lines scroll slowly toward camera (one cell per 3.5 s, loops exactly); beams breathe in opacity on a 10.5 s sine; a few particles drift up (21 s path). All motion is slow, smooth and subtle; the first and last frames must match so the loop is seamless; the central area stays still and clean. Keep the pink colour palette unchanged. Do not add text, logos or new objects.
```

