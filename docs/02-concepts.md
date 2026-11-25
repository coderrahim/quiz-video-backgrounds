# 10 Design Concepts

Each concept has a distinct layout *and* visual identity (perspective, radial, diagonal, organic, technical, playful, circular, layered, isometric).

| # | Name | Layout family | Mood |
|---|---|---|---|
| 01 | [Neon Arena](../designs/01-neon-arena/README.md) | One-point perspective | Esports / gaming |
| 02 | [Hex Pulse](../designs/02-hex-pulse/README.md) | Tessellation, edge-masked | Tech / sci-fi |
| 03 | [Spotlight Stage](../designs/03-spotlight-stage/README.md) | Radial sunburst | TV game show |
| 04 | [Diagonal Slash](../designs/04-diagonal-slash/README.md) | Diagonal bands | Sports broadcast |
| 05 | [Liquid Orbs](../designs/05-liquid-orbs/README.md) | Soft mesh + spheres | Calm premium |
| 06 | [Circuit Flow](../designs/06-circuit-flow/README.md) | Orthogonal traces | Futuristic data |
| 07 | [Memphis Pop](../designs/07-memphis-pop/README.md) | Scattered confetti | Fun / kids / family |
| 08 | [Radar Rings](../designs/08-radar-rings/README.md) | Concentric circles | Radar / suspense |
| 09 | [Paper Waves](../designs/09-paper-waves/README.md) | Layered curves | Soft modern |
| 10 | [Crystal Cubes](../designs/10-crystal-cubes/README.md) | Isometric clusters | 3D / puzzle |

## 01. Neon Arena
Esports-stage perspective grid with corner light beams.

- **Composition:** One-point perspective. A glowing grid floor recedes from the bottom third toward a soft horizon glow behind the centre; two tall light beams rise from the lower corners and cross diagonally outward; a thin neon frame hugs the edges. Centre 60% is a smooth dark-to-primary gradient.
- **Shapes:** Thin neon lines, perspective grid cells, tall translucent light beams, small corner brackets and chevrons.
- **Pattern:** Square grid in perspective with every 4th line brighter.
- **Lighting:** Horizon glow, additive beams, soft bloom on grid intersections.
- **Gradient:** Vertical: base -> primary at horizon -> base at top; accent only on lines.
- **Animation:** Grid lines scroll slowly toward camera (one cell per 3.5 s, loops exactly); beams breathe in opacity on a 10.5 s sine; a few particles drift up (21 s path).

## 02. Hex Pulse
Honeycomb tech pattern that fades out toward the centre.

- **Composition:** Hexagon cells densely packed in the four corners and along top/bottom edges, fading out radially so the centre 60% is empty. A few hexes are filled with glowing gradient; most are thin outlines.
- **Shapes:** Regular hexagons of 3 sizes, outlined and filled, small dot clusters.
- **Pattern:** Honeycomb tessellation with radial opacity falloff (mask).
- **Lighting:** Soft inner glow on filled hexes, gentle vignette.
- **Gradient:** Diagonal base -> primary background; hex fills use primary -> accent.
- **Animation:** Random hex cells softly pulse in brightness in a fixed 21 s sequence; whole pattern drifts 1% diagonally and returns.

## 03. Spotlight Stage
Classic TV game-show stage with sunburst rays and bokeh.

- **Composition:** Radial sunburst of soft rays emanating from a point just below centre; a curved glossy stage rim across the bottom; rows of out-of-focus bokeh lights along the bottom and upper corners; two spotlight cones from the top corners.
- **Shapes:** Wedge-shaped rays, circular bokeh discs, curved stage arcs, light cones.
- **Pattern:** Alternating ray wedges with low contrast; bokeh in 3 sizes.
- **Lighting:** Warm-key spotlights, glossy reflection on stage rim, bokeh glow.
- **Gradient:** Radial: primary at the ray origin -> base at the corners.
- **Animation:** Rays rotate one full turn per 21 s; bokeh twinkles on 3.5 s / 7 s cycles; spotlight cones sway +-3 deg on a 10.5 s sine.

## 04. Diagonal Slash
Bold angled colour bands in a dynamic sports-broadcast style.

- **Composition:** Layered diagonal parallelogram bands slice the top-left and bottom-right corners at roughly 25 deg; thin accent stripes run parallel; the central diagonal channel remains a clean gradient.
- **Shapes:** Skewed parallelograms, thin parallel stripes, small triangles at stripe ends.
- **Pattern:** Parallel stripe sets with different widths; subtle halftone dots on one band.
- **Lighting:** Flat-shaded with soft drop shadows between layers and a glossy edge highlight.
- **Gradient:** Each band uses a different primary<->secondary gradient; background base.
- **Animation:** Bands slide 40 px along their diagonal and back (21 s ease in-out); stripes shimmer with a light sweep once per 21 s.

## 05. Liquid Orbs
Soft glassy spheres and blurred gradient blobs, calm and premium.

- **Composition:** Large translucent glass spheres at two diagonal corners (partly cropped), smaller orbs scattered near edges, big blurred gradient blobs behind. Centre is a calm smooth mesh gradient.
- **Shapes:** Spheres with glass refraction, organic blobs, small bubbles.
- **Pattern:** None; fine film-grain overlay for smoothness.
- **Lighting:** Soft rim lights, specular highlights, depth-of-field blur.
- **Gradient:** Mesh gradient: primary, secondary and accent blended over base.
- **Animation:** Orbs float on small 21 s Lissajous paths (+-30 px); blobs morph slowly; highlights glint once.

## 06. Circuit Flow
Glowing circuit traces with data pulses along the borders.

- **Composition:** PCB-style traces run from each corner and along the top/bottom edges, ending in glowing nodes and rings. Traces avoid the central area completely; a faint dot grid fills the base.
- **Shapes:** 45/90-degree lines, nodes, rings, chip-like rectangles, small vias.
- **Pattern:** Faint dot grid + trace bundles of 3-5 parallel lines.
- **Lighting:** Neon glow on lines, node bloom, dark matte base.
- **Gradient:** Base-to-primary vignette; accent on traces.
- **Animation:** Light pulses travel along traces on 7 s / 10.5 s loops; nodes blink at fixed offsets.

## 07. Memphis Pop
Playful confetti shapes for fun, family-friendly quizzes.

- **Composition:** A loose frame of geometric confetti: triangles, circles, squiggles, plus signs, dot clusters and half-circles, denser in corners and sparse near the middle edges. Flat bright shapes on a smooth gradient.
- **Shapes:** Triangles, rings, squiggles, crosses, dot grids, half-circles, zig-zags.
- **Pattern:** Scattered 'confetti' with minimum spacing; no overlap with centre.
- **Lighting:** Flat vector look with a soft long-shadow or subtle grain.
- **Gradient:** Simple linear base -> primary; shapes in secondary/accent/highlight/pop.
- **Animation:** Shapes bob and rotate slowly (one full rotation per 21 s or less, integer fractions); squiggles wiggle on a 3.5 s loop.

## 08. Radar Rings
Concentric rings and ripples radiating from the centre.

- **Composition:** Concentric thin rings and dotted arcs centred on the frame, visible mostly in the outer 25% as they fade toward the middle; tick marks along the rings; small crosshair marks at the four corners.
- **Shapes:** Circles, dashed/dotted arcs, ticks, crosshairs, small arrow chevrons.
- **Pattern:** Rings spaced on a geometric progression; ticks every 5 deg on one ring.
- **Lighting:** Faint glow on rings, soft central halo kept dark and subtle.
- **Gradient:** Radial: base at centre -> primary in the mid ring zone -> base at corners.
- **Animation:** Ripples expand outward and fade, a new one every 3.5 s (6 per loop); one dotted ring rotates once per 21 s.

## 09. Paper Waves
Layered paper-cut ribbons with real depth.

- **Composition:** Three to five stacked wavy paper layers sweep across the bottom and curl up the left and right sides; a thinner ribbon stack curves across the top. Each layer casts a soft shadow on the next. Centre is open.
- **Shapes:** Smooth sine-like ribbons, sweeping curves, soft cut edges.
- **Pattern:** Optional fine dot or line texture on one layer.
- **Lighting:** Soft ambient occlusion shadows between layers, subtle top light.
- **Gradient:** Each layer a tint step from primary to base; top ribbon uses accent.
- **Animation:** Layers drift horizontally at different speeds with a sine wave phase shift (period 21 s); parallax feel.

## 10. Crystal Cubes
Isometric cubes and low-poly crystal shards in the corners.

- **Composition:** Clusters of isometric cubes and faceted low-poly crystals stacked in the four corners at different scales with depth blur; sparse tiny cubes float toward the middle edges. Centre is a clean gradient with faint isometric grid.
- **Shapes:** Isometric cubes, low-poly facets, triangular shards, small diamonds.
- **Pattern:** Faint isometric grid lines; facet shading in 3 tones.
- **Lighting:** 3-tone facet shading, rim light on top edges, soft glow underneath.
- **Gradient:** Background base -> primary; cube faces light/mid/dark of the palette.
- **Animation:** Cubes bob 12 px on staggered 7 s cycles; crystals glint with a light sweep every 10.5 s.

