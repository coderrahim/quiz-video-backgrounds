# Quiz Video Backgrounds — 10 designs × 5 colours = 50

Planning kit and AI-generation prompts for 50 looping 21 s, 1920×1080 quiz-video backgrounds
(Word Association, Guess the Logo Sound, Build Your Dream House, trivia, etc.).

| Doc | What's in it |
|---|---|
| [docs/01-design-system.md](docs/01-design-system.md) | Colour roles, 5 palettes (hex), global rules |
| [docs/02-concepts.md](docs/02-concepts.md) | The 10 concepts: composition, shapes, lighting, gradients, animation |
| [docs/03-production-pipeline.md](docs/03-production-pipeline.md) | Workflow, tools, QC checklist, delivery |
| [designs/](designs) | One folder per design with all 5 still / recolour / video prompts |
| [prompts/all_prompts.csv](prompts/all_prompts.csv) · [json](prompts/all_prompts.json) | All 50 prompts, machine readable |
| [scripts/loop_encode.sh](scripts/loop_encode.sh) | ffmpeg: exact 21 s, 1080p, seamless crossfade loop |

Colours: Green · Purple · Orange · Blue · Pink. Designs: Neon Arena, Hex Pulse, Spotlight Stage, Diagonal Slash, Liquid Orbs, Circuit Flow, Memphis Pop, Radar Rings, Paper Waves, Crystal Cubes.

Docs are generated: edit `scripts/data.py`, run `python3 scripts/generate.py`.

## Rendered designs (code-generated, exact 21 s seamless loops)
`render/render.py DESIGN COLOR OUT.mp4` (or `--frame SECONDS OUT.png` for a still). Colours: green, purple, orange, blue, pink.

| Code | Design | Notes |
|---|---|---|
| QB02 | `hex-pulse` | Honeycomb edges, pulsing cells, drifts one lattice period per loop |
| QB08 | `radar-rings` | Concentric rings, ripple every 3.5 s, rotating dotted rings |
| QB11 | `geo-tiles` | Tiled abstract shapes (client demo style); `blue-ref` / `grad:#c0:#c1` gradients |
| QB12 | `bokeh-sparkle` | Floating bokeh + twinkling sparkles on client's Canva gradient |
| QB13 | `doodle-play` | Line-art gaming doodles; per-colour gradient + scroll direction (green ↑, purple ↓, orange →, blue ←, pink ↗) |

Videos are written to `samples/` (git-ignored because of size; deliver via Drive/Fiverr).
