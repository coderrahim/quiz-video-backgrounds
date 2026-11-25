# Design System

## Colour roles
Every variation uses the same 6 roles; only values change. Layout, geometry, light placement and contrast structure never change.

| Role | Use | Green | Purple | Orange | Blue | Pink |
|---|---|---|---|---|---|---|
| base | Darkest background, vignette | `#03231A` | `#150836` | `#2B0E02` | `#041030` | `#2A0620` |
| primary | Dominant shapes, mid gradients | `#0E9F6E` | `#7C3AED` | `#F97316` | `#2563EB` | `#EC4899` |
| secondary | Analogous support, second gradient stop | `#14B8A6` | `#A855F7` | `#F59E0B` | `#0EA5E9` | `#F472B6` |
| accent | Neon edges, glows, light beams | `#34F5A5` | `#C084FC` | `#FFB347` | `#38D5FF` | `#FF7AC6` |
| highlight | Sparkles, rim light, specular | `#D5FFEC` | `#F1E6FF` | `#FFF1D6` | `#DDF4FF` | `#FFE4F3` |
| pop | Complementary sparks, ≤3% of area | `#FFE45C` | `#FFD23F` | `#38BDF8` | `#FF8A3D` | `#5EEAD4` |

## Global rules
- **Safe zone:** centre 60% (x 20–80 %, y 15–85 %) stays smooth, low-contrast, luminance within ±10 % of local average, so white or dark text both work. All detail lives in the outer 20–25 %.
- **Luminance structure:** same value map across all five colours (check by desaturating — the five should be near-identical greyscale).
- **Density:** edge detail covers max ~35 % of frame; no element sharper/brighter than the accent.
- **No** text, logos, watermarks, people, or topic-specific imagery.
- **Motion:** max drift ~1–3 % of frame; periods divide 21 s (21, 10.5, 7, 5.25, 3.5, 3, 2.1, 1.5 s); no flashes, no camera movement.
- **Quality:** crisp geometry, no banding (add 1–2 % grain), consistent bloom strength, consistent corner treatment.
- **Naming:** `QB{NN}_{slug}_{color}.mp4`, e.g. `QB01_neon-arena_blue.mp4`.
