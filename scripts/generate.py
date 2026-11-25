#!/usr/bin/env python3
"""Generate docs, per-design prompt files and all_prompts.{json,csv} from data.py."""
import csv, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from data import *

ROOT = pathlib.Path(__file__).parent.parent
def w(path, text):
    p = ROOT / path; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text)

def fname(d, c): return f"QB{d['id']:02d}_{d['slug']}_{c}"

def still_prompt(d, c):
    p = PALETTES[c]
    return (f"{d['body']} Colour scheme ({c.upper()}): {p['words']}. Exact hex palette: background base {p['base']}, "
            f"primary {p['primary']}, secondary {p['secondary']}, accent glow {p['accent']}, highlights {p['highlight']}, "
            f"tiny sparks {p['pop']}. Style: {COMMON_STYLE}. {COMPOSITION_RULES}. "
            f"Negative prompt: {NEGATIVE}.")

def recolor_prompt(d, c):
    p = PALETTES[c]
    return (f"Using the attached master image of design '{d['name']}' as the exact reference, keep the composition, shapes, positions, "
            f"lighting and level of detail IDENTICAL. Change ONLY the colour scheme to {c.upper()}: {p['words']} "
            f"(base {p['base']}, primary {p['primary']}, secondary {p['secondary']}, accent {p['accent']}, highlight {p['highlight']}, "
            f"spark {p['pop']}). Preserve the same brightness/contrast structure so text stays readable. "
            f"Negative prompt: {NEGATIVE}.")

def video_prompt(d, c):
    return (f"Animate this exact image as a seamless 21-second loop, locked-off camera, no zoom or pan. Motion: {d['animation']} "
            f"All motion is slow, smooth and subtle; the first and last frames must match so the loop is seamless; "
            f"the central area stays still and clean. Keep the {c} colour palette unchanged. Do not add text, logos or new objects.")

rows = []
for d in DESIGNS:
    for c in COLORS:
        rows.append(dict(file=fname(d, c), design=d['name'], color=c, still_prompt=still_prompt(d, c),
                         recolor_prompt=recolor_prompt(d, c), video_prompt=video_prompt(d, c)))
w("prompts/all_prompts.json", json.dumps(rows, indent=2))
with open(ROOT / "prompts/all_prompts.csv", "w", newline="") as f:
    cw = csv.DictWriter(f, fieldnames=list(rows[0])); cw.writeheader(); cw.writerows(rows)

# per-design docs
for d in DESIGNS:
    t = f"# {d['id']:02d} · {d['name']}\n\n_{d['tagline']}_\n\n"
    t += f"## Visual composition\n{d['composition']}\n\n## Design details\n"
    for k, lab in [("shapes","Shapes"),("pattern","Pattern"),("lighting","Lighting"),("gradient","Gradients"),("animation","Animation (21 s loop)")]:
        t += f"- **{lab}:** {d[k]}\n"
    t += ("\n## Workflow\n1. Generate the **master** in **Blue** with the still prompt (iterate until approved; save the seed).\n"
          "2. Generate the other four colours with the *recolor prompt* using the master as image reference (image-to-image / edit mode), "
          "or by re-running the still prompt with the same seed + layout reference.\n"
          "3. Animate each still with its video prompt, then run `scripts/loop_encode.sh`.\n\n## Prompts\n")
    for c in COLORS:
        r = next(x for x in rows if x['file'] == fname(d, c))
        t += (f"### {c.capitalize()} — `{r['file']}.mp4`\n**Still prompt**\n```\n{r['still_prompt']}\n```\n"
              f"**Recolour prompt (from master)**\n```\n{r['recolor_prompt']}\n```\n**Video prompt**\n```\n{r['video_prompt']}\n```\n\n")
    w(f"designs/{d['id']:02d}-{d['slug']}/README.md", t)

# concepts overview
t = "# 10 Design Concepts\n\nEach concept has a distinct layout *and* visual identity (perspective, radial, diagonal, organic, technical, playful, circular, layered, isometric).\n\n"
t += "| # | Name | Layout family | Mood |\n|---|---|---|---|\n"
moods = ["Esports / gaming","Tech / sci-fi","TV game show","Sports broadcast","Calm premium","Futuristic data","Fun / kids / family","Radar / suspense","Soft modern","3D / puzzle"]
fam = ["One-point perspective","Tessellation, edge-masked","Radial sunburst","Diagonal bands","Soft mesh + spheres","Orthogonal traces","Scattered confetti","Concentric circles","Layered curves","Isometric clusters"]
for d, m, f_ in zip(DESIGNS, moods, fam):
    t += f"| {d['id']:02d} | [{d['name']}](../designs/{d['id']:02d}-{d['slug']}/README.md) | {f_} | {m} |\n"
t += "\n"
for d in DESIGNS:
    t += f"## {d['id']:02d}. {d['name']}\n{d['tagline']}\n\n- **Composition:** {d['composition']}\n- **Shapes:** {d['shapes']}\n- **Pattern:** {d['pattern']}\n- **Lighting:** {d['lighting']}\n- **Gradient:** {d['gradient']}\n- **Animation:** {d['animation']}\n\n"
w("docs/02-concepts.md", t)

# design system
t = "# Design System\n\n## Colour roles\nEvery variation uses the same 6 roles; only values change. Layout, geometry, light placement and contrast structure never change.\n\n"
t += "| Role | Use | " + " | ".join(c.capitalize() for c in COLORS) + " |\n|---|---|" + "---|"*5 + "\n"
for role, use in [("base","Darkest background, vignette"),("primary","Dominant shapes, mid gradients"),("secondary","Analogous support, second gradient stop"),("accent","Neon edges, glows, light beams"),("highlight","Sparkles, rim light, specular"),("pop","Complementary sparks, ≤3% of area")]:
    t += f"| {role} | {use} | " + " | ".join(f"`{PALETTES[c][role]}`" for c in COLORS) + " |\n"
t += """
## Global rules
- **Safe zone:** centre 60% (x 20–80 %, y 15–85 %) stays smooth, low-contrast, luminance within ±10 % of local average, so white or dark text both work. All detail lives in the outer 20–25 %.
- **Luminance structure:** same value map across all five colours (check by desaturating — the five should be near-identical greyscale).
- **Density:** edge detail covers max ~35 % of frame; no element sharper/brighter than the accent.
- **No** text, logos, watermarks, people, or topic-specific imagery.
- **Motion:** max drift ~1–3 % of frame; periods divide 21 s (21, 10.5, 7, 5.25, 3.5, 3, 2.1, 1.5 s); no flashes, no camera movement.
- **Quality:** crisp geometry, no banding (add 1–2 % grain), consistent bloom strength, consistent corner treatment.
- **Naming:** `QB{NN}_{slug}_{color}.mp4`, e.g. `QB01_neon-arena_blue.mp4`.
"""
w("docs/01-design-system.md", t)
print(len(rows), "prompts written")
