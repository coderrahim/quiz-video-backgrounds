#!/usr/bin/env python3
"""Procedural renderer: exact 21 s seamless loops, 1920x1080, 30 fps.
Usage: render.py DESIGN COLOR OUT.mp4 [--frame T_SECONDS OUT.png]
Every animated term is periodic in 21 s (integer cycles), so the loop is seamless by construction."""
import sys, subprocess, pathlib, numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "scripts")); sys.path.insert(0, str(pathlib.Path(__file__).parent))
from data import PALETTES

W, H, FPS, DUR = 1920, 1080, 30, 21
Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
CX, CY = W / 2, H / 2
TAU = np.float32(2 * np.pi)
rng = np.random.default_rng(7)
GRAIN = (rng.standard_normal((H, W, 1)).astype(np.float32) * 0.006)

def hexc(h): return np.array([int(h[i:i+2], 16) for i in (1, 3, 5)], np.float32) / 255
def smooth(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)
REF_BLUE = dict(stops=[(0.0, "#0cbef5"), (0.34, "#0089da"), (0.66, "#085abe"), (1.0, "#00219f"), (1.17, "#000a91")],
                pattern="#0a78d6")
def pal(c):
    if c == "blue-ref":
        P = pal("blue"); P["stops"] = [(a, hexc(b)) for a, b in REF_BLUE["stops"]]; P["patcol"] = hexc(REF_BLUE["pattern"]); return P
    if c.startswith("grad:"):                      # e.g. grad:#00bbf6:#000890  (centre colour : edge colour)
        _, c0, c1 = c.split(":"); a, b = hexc(c0), hexc(c1)
        P = pal("blue"); P["stops"] = [(0.0, a), (1.0, b), (1.3, b)]; P["patcol"] = a * 0.68 + b * 0.32; P["c0"], P["c1"] = a, b; return P
    P = {k: hexc(v) for k, v in PALETTES[c].items() if k != "words"}; P["name"] = c; return P

def backdrop(P, glow=0.55):
    """Soft diagonal gradient + gentle centre glow (hybrid look, like the client demos)."""
    d = (X / W * 0.6 + Y / H * 0.4)[..., None]
    img = P["base"] * (1 - d * 0.0) * 1.0
    g = smooth(0.0, 1.0, 1 - np.hypot((X - CX) / (W * 0.62), (Y - CY) / (H * 0.8)))[..., None]
    img = P["base"] + (P["primary"] * 0.55 - P["base"]) * g
    gl = np.exp(-(((X - CX) / (W * 0.28)) ** 2 + ((Y - CY) / (H * 0.34)) ** 2))[..., None]
    img = img + (P["secondary"] * 0.35) * gl * glow
    return img

def edge_mask(inner=0.42, outer=0.9):
    r = np.hypot((X - CX) / (W / 2), (Y - CY) / (H / 2))
    return smooth(inner, outer, r)[..., None]

# ---------------- Design 02: Hex Pulse ----------------
S = 78.0                     # hex circumradius (px)
HW, HH = np.sqrt(3) * S, 1.5 * S
def hex_cell(px, py):
    """pointy-top hex grid via two interleaved rectangular lattices. Returns (px distance to border, cell hash)."""
    w, v = np.sqrt(3) * S, 3.0 * S
    ia, ja = np.round(px / w), np.round(py / v)
    ib, jb = np.floor(px / w), np.floor((py - 1.5 * S) / v + 0.5)
    ax, ay = ia * w, ja * v
    bx, by = (np.round(px / w - 0.5) + 0.5) * w, np.round((py - 1.5 * S) / v) * v + 1.5 * S
    da = (px - ax) ** 2 + (py - ay) ** 2; db = (px - bx) ** 2 + (py - by) ** 2
    useA = da <= db
    cxp = np.where(useA, ax, bx); cyp = np.where(useA, ay, by)
    ox, oy = px - cxp, py - cyp
    inr = S * np.sqrt(3) / 2
    a_ = np.abs(ox); b_ = np.abs(ox * 0.5 + oy * np.sqrt(3) / 2); c_ = np.abs(ox * 0.5 - oy * np.sqrt(3) / 2)
    d = inr - np.maximum(np.maximum(a_, b_), c_)
    cid = np.round(cxp / (w / 2)) * 131.0 + np.round(cyp / (1.5 * S)) * 17.0
    h = np.sin(cid * 12.9898) * 43758.5453
    return d.astype(np.float32), (h - np.floor(h)).astype(np.float32)

def hex_pulse(t, P):
    mask = edge_mask(0.38, 0.85)
    ph = t / DUR
    d, h = hex_cell(X + HW * ph, Y)        # drift = exactly one lattice period over the loop
    line = np.exp(-(np.maximum(d, 0) / 1.6) ** 2)
    k = 1 + np.floor(h * 3)                # 1..3 integer cycles per loop
    pulse = 0.5 + 0.5 * np.sin(TAU * (k * ph + h * 7))
    bright = (h > 0.82)
    img = backdrop(P)
    tint = (0.10 + 0.14 * h)[..., None] * (d > 1.5)[..., None]      # faint per-cell tint
    img = img + P["secondary"] * tint * mask
    glowfill = np.where(bright, 0.18 + 0.42 * pulse, 0) * (d > 1.5) * (0.75 + 0.25 * smooth(0, 40, d))
    t_ = (Y / H)[..., None]
    img = img + (P["primary"] * (1 - t_) + P["accent"] * t_) * glowfill[..., None] * mask * 0.9
    img = img + P["accent"] * (line * (0.22 + 0.5 * np.where(bright, pulse, 0.15)))[..., None] * mask
    return img

# ---------------- Design 08: Radar Rings ----------------
def radar_rings(t, P):
    ph = t / DUR
    r = np.hypot(X - CX, Y - CY); th = np.arctan2(Y - CY, X - CX)
    mask = edge_mask(0.30, 0.85)
    img = backdrop(P, glow=0.4)
    Rmax = np.hypot(CX, CY) * 1.02
    # static geometric rings
    rad = 150 * 1.32 ** np.arange(0, 9)
    ring = np.zeros_like(r)
    for i, R in enumerate(rad):
        ring += np.exp(-((r - R) / 1.6) ** 2) * (0.55 if i % 2 else 0.9)
    # 6 expanding ripples per loop (period 3.5 s)
    rip = np.zeros_like(r)
    for i in range(6):
        pos = ((ph * 6 + i / 6) % 1.0)
        R = pos * Rmax
        rip += np.exp(-((r - R) / 7.0) ** 2) * (1 - pos) ** 1.3 * smooth(0, 0.12, pos)
    # dotted rotating ring (one full turn per loop)
    dr = 520
    dots = (np.cos(th * 90 - TAU * ph) > 0.55).astype(np.float32)
    dotted = np.exp(-((r - dr) / 2.2) ** 2) * dots
    dr2 = 760
    dash = (np.cos(th * 36 + TAU * ph) > 0.2).astype(np.float32)
    dotted += np.exp(-((r - dr2) / 1.8) ** 2) * dash * 0.8
    # tick marks on a ring
    tick = (np.abs(((th / TAU * 120) % 1.0) - 0.5) > 0.46).astype(np.float32)
    ticks = tick * ((r > 600) & (r < 616)) * 0.8
    # corner crosshairs
    def cross(cx, cy, s=26, w=1.6):
        a = ((np.abs(X - cx) < w) & (np.abs(Y - cy) < s)) | ((np.abs(Y - cy) < w) & (np.abs(X - cx) < s))
        return a.astype(np.float32)
    ch = sum(cross(x, y) for x, y in [(60, 60), (W - 60, 60), (60, H - 60), (W - 60, H - 60)])
    # halo
    halo = np.exp(-((r - 0) / 260) ** 2)[..., None]
    img = img + P["accent"] * (ring * 0.28 + dotted * 0.6 + ticks * 0.6)[..., None] * mask
    img = img + P["secondary"] * (rip * 0.5)[..., None] * mask
    img = img + P["highlight"] * (ch * 0.55)[..., None]
    img = img + P["secondary"] * halo * 0.04
    return img


# ---------------- Design 11: Geo Tiles (tiled silhouette wallpaper, like client demo) ----------------
from PIL import Image, ImageDraw
import math
TP = 540          # tile period (px). Pattern drifts exactly one tile per loop -> seamless.
_MOSAIC = None
def _motif_tile():
    K = 4; N = TP * K
    im = Image.new("L", (N, N), 0); d = ImageDraw.Draw(im)
    def star(cx, cy, r, a=0, v=255, inner=0.28):
        pts = []
        for i in range(8):
            rr = r if i % 2 == 0 else r * inner; ang = a + i * math.pi / 4 - math.pi / 2
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        d.polygon(pts, fill=v)
    def pinwheel(cx, cy, r, v=150):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=v)
        for i in range(10):
            a0 = i * math.pi / 5
            d.pieslice([cx - r * .86, cy - r * .86, cx + r * .86, cy + r * .86], math.degrees(a0), math.degrees(a0 + math.pi / 10), fill=v + 40)
    def ring(cx, cy, r, w, v=255):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=v, width=w)
    def tri(cx, cy, r, a, v=170):
        d.polygon([(cx + r * math.cos(a + i * 2.0944), cy + r * math.sin(a + i * 2.0944)) for i in range(3)], fill=v)
    def squiggle(cx, cy, L, amp, w, a=0, v=255):
        pts = []
        for i in range(61):
            u = i / 60 - .5; x = u * L; y = amp * math.sin(u * 6.2832 * 2)
            pts.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
        d.line(pts, fill=v, width=w, joint="curve")
        for q in (pts[0], pts[-1]): d.ellipse([q[0] - w / 2, q[1] - w / 2, q[0] + w / 2, q[1] + w / 2], fill=v)
    def plus(cx, cy, r, w, v=255):
        d.rectangle([cx - r, cy - w / 2, cx + r, cy + w / 2], fill=v); d.rectangle([cx - w / 2, cy - r, cx + w / 2, cy + r], fill=v)
    def half(cx, cy, r, a, v=170):
        d.pieslice([cx - r, cy - r, cx + r, cy + r], a, a + 180, fill=v)
    def dia(cx, cy, r, v=170):
        d.polygon([(cx, cy - r), (cx + r * .7, cy), (cx, cy + r), (cx - r * .7, cy)], fill=v)
    u = K * TP / 420.0 * 1.0
    # staggered layout inside one tile (coordinates in 420-px space)
    pinwheel(90 * u, 90 * u, 52 * u)
    star(235 * u, 70 * u, 30 * u, v=230)
    squiggle(345 * u, 110 * u, 110 * u, 14 * u, int(10 * u), a=-0.5)
    ring(60 * u, 235 * u, 28 * u, int(9 * u))
    tri(165 * u, 225 * u, 38 * u, 0.3, v=160)
    plus(285 * u, 225 * u, 22 * u, int(10 * u))
    half(375 * u, 255 * u, 36 * u, 200, v=160)
    dia(80 * u, 345 * u, 40 * u)
    squiggle(205 * u, 360 * u, 120 * u, 14 * u, int(10 * u), a=0.25)
    star(335 * u, 355 * u, 38 * u, a=0.4, v=170)
    for (x, y, r) in [(165, 140, 6), (30, 160, 5), (290, 150, 6), (130, 300, 6), (250, 290, 5), (400, 20, 6), (20, 395, 5)]:
        d.ellipse([(x - r) * u, (y - r) * u, (x + r) * u, (y + r) * u], fill=200)
    return im.resize((TP, TP), Image.LANCZOS)

def _mosaic():
    global _MOSAIC
    if _MOSAIC is None:
        t = np.asarray(_motif_tile(), np.float32) / 255
        nx, ny = W // TP + 3, H // TP + 3
        rows = [np.tile(np.roll(t, TP // 2 if r % 2 else 0, axis=1), (1, nx)) for r in range(ny)]
        _MOSAIC = Image.fromarray((np.vstack(rows) * 255).astype(np.uint8))
    return _MOSAIC

def ref_gradient(P, ph):
    """Radial gradient sampled from the client's reference frame (elliptical: fades faster horizontally)."""
    u = (X - CX) / (W / 2); v = (Y - CY) / (H / 2)
    r = np.hypot(u, v * 0.57) * (1 + 0.025 * np.sin(TAU * ph))      # gentle breathing, 1 cycle / loop
    xs = [a for a, _ in P["stops"]]
    return np.stack([np.interp(r, xs, [c[i] for _, c in P["stops"]]) for i in range(3)], -1).astype(np.float32)

def geo_tiles(t, P):
    ph = t / DUR
    dx = TP * ph                       # drift one full tile left per loop
    m = _mosaic().transform((W, H), Image.AFFINE, (1, 0, dx + TP * 0.3, 0, 1, TP * 0.2), resample=Image.BICUBIC)
    pat = (np.asarray(m, np.float32) / 255)[..., None]
    if "stops" in P:
        img = ref_gradient(P, ph)
        quiet = 1 - 0.12 * np.exp(-(((X - W / 2) / (W * 0.25)) ** 2 + ((Y - H / 2) / (H * 0.28)) ** 2))[..., None]
        return img + (P["patcol"] - img) * pat * 0.60 * quiet
    breathe = 1 + 0.10 * np.sin(TAU * ph)                      # glow breathes once per loop
    cxg, cyg = W * 0.36, H * 0.42
    gl = np.exp(-(((X - cxg) / (W * 0.30)) ** 2 + ((Y - cyg) / (H * 0.42)) ** 2))[..., None]
    wide = smooth(0, 1, 1 - np.hypot((X - W * 0.45) / (W * 0.75), (Y - H * 0.5) / (H * 0.95)))[..., None]
    img = P["base"] + (P["primary"] * 0.8 - P["base"]) * wide
    img = img + P["accent"] * 0.30 * gl * breathe
    quiet = 1 - 0.30 * np.exp(-(((X - W / 2) / (W * 0.28)) ** 2 + ((Y - H / 2) / (H * 0.30)) ** 2))[..., None]   # a bit calmer under text
    tint = P["highlight"] * 0.55 + P["secondary"] * 0.45
    img = img + (tint - img) * pat * 0.20 * quiet
    return img

# ---------------- Canva-matched gradient ----------------
def canva_radial(c0, c1):
    """Exact match of the client's Canva 'background clip': circular radial (in pixels), linear from c0 at centre to c1 at the corners."""
    r = np.hypot(X - CX, Y - CY) / np.hypot(CX, CY)
    return c0 + (c1 - c0) * r[..., None]

# ---------------- Design 12: Bokeh Sparkle ----------------
_PARTS = None
def _particles():
    global _PARTS
    if _PARTS is None:
        g = np.random.default_rng(21); out = []
        while len(out) < 70:
            x, y = g.uniform(-40, W + 40), g.uniform(-40, H + 40)
            e = np.hypot((x - CX) / (W / 2), (y - CY) / (H / 2))
            if g.uniform() > smooth(0.35, 0.95, e) * 0.95 + 0.05: continue      # mostly near edges/corners
            kind = "spark" if g.uniform() < 0.28 else "bokeh"
            out.append(dict(x=x, y=y, kind=kind, r=g.uniform(14, 34) if kind == "spark" else g.uniform(10, 70) ** 1.0,
                            a=g.uniform(0.25, 0.75), ph=g.uniform(0, 1), k=int(g.integers(1, 4)), amp=g.uniform(8, 22)))
        _PARTS = out
    return _PARTS

def bokeh_sparkle(t, P, base):
    ph = t / DUR
    lay = np.zeros((H, W), np.float32); spk = np.zeros((H, W), np.float32)
    for q in _particles():
        x = q["x"] + q["amp"] * 0.6 * np.cos(TAU * (ph + q["ph"]))
        y = q["y"] + q["amp"] * np.sin(TAU * (ph + q["ph"]))          # gentle float, 1 cycle per loop
        R = q["r"]; m = int(R * 2.2) + 2
        x0, x1 = max(int(x) - m, 0), min(int(x) + m, W); y0, y1 = max(int(y) - m, 0), min(int(y) + m, H)
        if x0 >= x1 or y0 >= y1: continue
        xx, yy = X[y0:y1, x0:x1] - x, Y[y0:y1, x0:x1] - y
        tw = 0.5 + 0.5 * np.sin(TAU * (q["k"] * ph + q["ph"]))         # integer twinkle cycles
        if q["kind"] == "bokeh":
            d = np.hypot(xx, yy)
            disc = smooth(R, R - 2.5, d) * (0.55 + 0.45 * smooth(R * 0.2, R, d))   # soft disc with brighter rim
            lay[y0:y1, x0:x1] += disc * q["a"] * (0.6 + 0.4 * tw)
        else:
            ax, ay = np.abs(xx), np.abs(yy)
            star = np.exp(-ax / (R * 0.06)) * smooth(R, 0, ay) + np.exp(-ay / (R * 0.06)) * smooth(R, 0, ax)
            core = np.exp(-(xx ** 2 + yy ** 2) / (R * 0.18) ** 2)
            spk[y0:y1, x0:x1] += (star * 0.8 + core) * q["a"] * (0.25 + 0.75 * tw)
    img = base
    img = img + (P["highlight"] * 0.6 + P["accent"] * 0.4 - img) * np.clip(lay, 0, 1)[..., None] * 0.22
    img = img + P["highlight"] * np.clip(spk, 0, 1.5)[..., None] * 0.55
    return img

# ---------------- Design 13: Doodle Play (line-art gaming doodles) ----------------
import doodles
_DMOS = None
def _dmosaic():
    global _DMOS
    if _DMOS is None:
        t = np.asarray(doodles.tile(), np.float32) / 255; T = doodles.TILE
        nx, ny = W // T + 4, H // T + 4
        rows = [np.tile(t, (1, nx)) for r in range(ny)]
        _DMOS = Image.fromarray((np.vstack(rows) * 255).astype(np.uint8))
    return _DMOS

import colorsys
def _hue_shift_stops(ref, h_centre, h_edge):
    """Keep the reference's saturation/value structure exactly; only re-map hue from centre to edge."""
    out = []
    for i, (a, c) in enumerate(ref):
        r, g, b = hexc(c); _, sat, val = colorsys.rgb_to_hsv(r, g, b)
        h = (h_centre + (h_edge - h_centre) * min(a, 1.0)) % 360 / 360
        out.append((a, "#%02x%02x%02x" % tuple(int(round(x * 255)) for x in colorsys.hsv_to_rgb(h, sat, val))))
    return out

PURPLE_REF = [(0.0, "#fc56d9"), (0.47, "#a332ad"), (0.89, "#4c0c83"), (1.0, "#380479")]
def stops_radial(stops, ph=0.0):
    r = np.hypot(X - CX, Y - CY) / np.hypot(CX, CY) * (1 + 0.02 * np.sin(TAU * ph))
    xs = [a for a, _ in stops]; cs = [hexc(c) for _, c in stops]
    return np.stack([np.interp(r, xs, [c[i] for c in cs]) for i in range(3)], -1).astype(np.float32)

DOODLE_STOPS = {
    "purple": PURPLE_REF,                                                    # client reference image
    "blue":   [(0.0, "#00bbf6"), (1.0, "#000990")],                          # client's Canva gradient
    "green":  _hue_shift_stops(PURPLE_REF, 95, 150),                         # lime centre -> emerald edge
    "orange": [(0.0, "#ffd24a"), (0.47, "#f08a1c"), (0.89, "#b8400c"), (1.0, "#952c06")],   # golden centre -> burnt-orange edge
    "pink":   [(0.0, "#ff5cae"), (0.47, "#d0338a"), (0.89, "#860e5a"), (1.0, "#6e0a4c")],   # rose centre -> deep raspberry edge
}

DOODLE_DIR = {"green": (0, -1),    # bottom -> top
              "purple": (0, 1),    # top -> bottom
              "orange": (1, 0),    # left -> right
              "blue": (-1, 0),     # right -> left
              "pink": (1, -1)}     # bottom-left -> top-right (diagonal)

def doodle_play(t, P):
    ph = t / DUR; T = doodles.TILE
    # scroll exactly one tile per loop (seamless); each colour gets its own direction (dx, dy) in tiles
    dx, dy = DOODLE_DIR.get(P.get("name"), (0, -1))
    c = T + 0.25 * T - dx * T * ph        # content moves +x when dx > 0
    f = T + 0.10 * T - dy * T * ph        # content moves +y (down) when dy > 0
    m = _dmosaic().transform((W, H), Image.AFFINE, (1, 0, c, 0, 1, f), resample=Image.BICUBIC)
    pat = (np.asarray(m, np.float32) / 255)[..., None]
    img = stops_radial(DOODLE_STOPS.get(P.get("name"), PURPLE_REF), ph)
    tint = np.float32([1, 1, 1]) * 0.55 + img * 0.45
    return img + (tint - img) * pat * 0.21

# ---------------- Design 14: Quiz Doodles ----------------
_QMOS = None
def _qmosaic():
    global _QMOS
    if _QMOS is None:
        t = np.asarray(doodles.tile(doodles.QUIZ_LAYOUT), np.float32) / 255; T = doodles.TILE
        nx, ny = W // T + 4, H // T + 4
        _QMOS = Image.fromarray((np.tile(t, (ny, nx)) * 255).astype(np.uint8))
    return _QMOS

QUIZ_STOPS = {"green": [(0.0, "#a2f25a"), (0.45, "#3cbd3c"), (0.88, "#0d7a3a"), (1.0, "#075f30")]}

QUIZ_DIR = {"green": (0, -1),      # bottom -> top
            "purple": (1, -1),    # bottom-left -> top-right
            "orange": (1, 1),     # top-left -> bottom-right
            "blue": (-1, 1),      # top-right -> bottom-left
            "pink": (-1, -1)}     # bottom-right -> top-left

def quiz_doodles(t, P):
    ph = t / DUR; T = doodles.TILE
    dx, dy = QUIZ_DIR.get(P.get("name"), (0, -1))
    m = _qmosaic().transform((W, H), Image.AFFINE, (1, 0, T * 1.2 - dx * T * ph, 0, 1, T * 1.05 - dy * T * ph), resample=Image.BICUBIC)
    pat = (np.asarray(m, np.float32) / 255)[..., None]
    img = stops_radial(QUIZ_STOPS.get(P.get("name"), DOODLE_STOPS.get(P.get("name"), PURPLE_REF)), ph)
    tint = np.float32([1, 1, 1]) * 0.55 + img * 0.45
    return img + (tint - img) * pat * 0.21

# ---------------- Design 03: Spotlight Stage (TV game-show) ----------------
STAGE_RAYS, STAGE_SWAY_DEG, STAGE_SWAY_CYC, STAGE_RIM = 3, 8, 3, 3   # motion speed (integer cycles per 21 s loop)
_STAGE_BOKEH = None
def _stage_bokeh():
    global _STAGE_BOKEH
    if _STAGE_BOKEH is None:
        g = np.random.default_rng(3); out = []
        for i in range(34):            # row of lights along the stage rim
            x = (i + 0.5) / 34 * W + g.uniform(-15, 15)
            y = H - 175 - 70 * (1 - ((x - CX) / CX) ** 2) * 0 + g.uniform(-30, 30) - 40 * np.cos((x - CX) / CX * 1.4)
            out.append((x, y, g.uniform(10, 26), g.uniform(0.35, 0.8), g.uniform(0, 1), int(g.integers(1, 5))))
        for corner in [(0, 0), (W, 0)]:  # clusters in the top corners
            for _ in range(10):
                x = corner[0] + (1 if corner[0] == 0 else -1) * g.uniform(20, 420); y = g.uniform(15, 260)
                out.append((x, y, g.uniform(8, 30), g.uniform(0.25, 0.6), g.uniform(0, 1), int(g.integers(1, 5))))
        _STAGE_BOKEH = out
    return _STAGE_BOKEH

STAGE_DIR = {"green": (-1, 1),     # top-right -> bottom-left
             "purple": (1, -1),    # bottom-left -> top-right
             "orange": (1, 1),     # top-left -> bottom-right
             "pink": (-1, -1)}     # bottom-right -> top-left   (blue: no sweep, as approved)

def spotlight_stage(t, P):
    ph = t / DUR
    name = P.get("name")
    img = stops_radial(QUIZ_STOPS.get(name, DOODLE_STOPS.get(name, PURPLE_REF)), ph)
    sdir = STAGE_DIR.get(name)
    light = np.float32([1, 1, 1]) * 0.6 + P["accent"] * 0.4
    # sunburst rays from just below centre; rotate exactly one ray period per loop (seamless, very slow)
    ox, oy = CX, CY + 60
    th = np.arctan2(Y - oy, X - ox); N = 20
    spin = -1 if (sdir and sdir[0] < 0) else 1
    ray = smooth(0.15, 0.55, 0.5 + 0.5 * np.cos(N * th - spin * TAU * STAGE_RAYS * ph))
    rn = np.hypot((X - ox) / (W / 2), (Y - oy) / (H / 2))
    ray *= smooth(0.38, 0.95, rn)                     # keep centre clean
    img = img + (light - img) * (ray * 0.07)[..., None]
    # two spotlight cones from top corners, gentle sway (+-3 deg, 1 cycle per loop)
    for sx, base in [(-60, 52), (W + 60, 128)]:
        sy = -80
        ang = np.degrees(np.arctan2(Y - sy, X - sx))
        a0 = base + STAGE_SWAY_DEG * np.sin(TAU * STAGE_SWAY_CYC * ph + (0 if sx < 0 else np.pi))
        cone = np.exp(-((ang - a0) / 9.0) ** 2) * smooth(1700, 300, np.hypot(X - sx, Y - sy))
        cone *= 1 - 0.75 * np.exp(-(((X - CX) / (W * 0.24)) ** 2 + ((Y - CY) / (H * 0.26)) ** 2))
        img = img + (light - img) * (cone * 0.22)[..., None]
    # curved glossy stage rim + darker floor at the bottom
    e = np.hypot((X - CX) / 1300, (Y - (H + 640)) / 830)
    floor = smooth(1.0, 0.985, e)
    img = img * (1 - 0.35 * floor[..., None])
    rim = np.exp(-((e - 1.0) / 0.0035) ** 2); rim2 = np.exp(-((e - 0.965) / 0.002) ** 2)
    sweep = 0.55 + 0.45 * np.cos(TAU * STAGE_RIM * ph - (X - CX) / W * 3.0)   # light travelling along the rim
    img = img + (light - img) * ((rim * 0.55 * sweep + rim2 * 0.25))[..., None]
    refl = floor * np.exp(-((X - CX) / (W * 0.3)) ** 2) * smooth(0.985, 0.93, e) * 0.10
    img = img + (light - img) * refl[..., None]
    # bokeh lights
    bk = np.zeros((H, W), np.float32)
    for x, y, r, a, p0, k in _stage_bokeh():
        m = int(r * 1.6) + 2
        x0, x1, y0, y1 = max(int(x) - m, 0), min(int(x) + m, W), max(int(y) - m, 0), min(int(y) + m, H)
        if x0 >= x1 or y0 >= y1: continue
        d = np.hypot(X[y0:y1, x0:x1] - x, Y[y0:y1, x0:x1] - y)
        tw = 0.35 + 0.65 * (0.5 + 0.5 * np.sin(TAU * ((k + 1) * ph + p0)))
        bk[y0:y1, x0:x1] += smooth(r, r * 0.55, d) * a * tw
    img = img + (light - img) * np.clip(bk, 0, 1)[..., None] * 0.55
    if sdir:   # soft diagonal shine band sweeping across, STAGE_RIM passes per loop (periodic -> seamless)
        ux, uy = sdir[0] / np.sqrt(2), sdir[1] / np.sqrt(2)
        L = abs(ux) * W + abs(uy) * H + 700
        u = ((X - CX) * ux + (Y - CY) * uy) / L
        band = np.cos(np.pi * (u - STAGE_RIM * ph)) ** 40          # one narrow band per period L
        band *= 1 - 0.7 * np.exp(-(((X - CX) / (W * 0.26)) ** 2 + ((Y - CY) / (H * 0.28)) ** 2))
        img = img + (light - img) * (band * 0.16)[..., None]
    return img

# ---------------- Design 01: Neon Arena (esports stage) ----------------
ARENA_CELLS_PER_LOOP = 6        # grid rolls toward camera 6 cells per 21 s (one per 3.5 s)
def _aa_line(v, w=1.2):
    """anti-aliased line at integer values of field v (screen-space width ~w px)."""
    gy, gx = np.gradient(v)
    fw = np.hypot(gx, gy) + 1e-6
    d = np.abs(v - np.round(v)) / fw
    return np.clip(1 - (d - w * 0.5), 0, 1)

# floating neon quiz icons for Neon Arena (edges/corners only)
_ARENA_ICONS = None
def _arena_icons():
    global _ARENA_ICONS
    if _ARENA_ICONS is None:
        from PIL import ImageFilter
        D = doodles
        spec = [  # fn, centre x, centre y, size px, rotation
            (D.qmark, 250, 210, 150, -12), (D.bulb, 520, 120, 120, 8), (D.stopwatch, 1420, 120, 120, -8),
            (D.qmark, 1690, 230, 170, 14), (D.buzzer, 140, 470, 130, 0), (D.check, 400, 400, 95, 0),
            (D.bubble, 1530, 420, 140, -6), (D.cross, 1800, 520, 95, 0), (D.trophy, 330, 640, 115, -6),
            (D.star, 1650, 650, 95, 12), (D.exclaim, 820, 90, 80, 10), (D.puzzle, 1110, 95, 95, -10),
        ]
        out = []
        for fn, x, y, size, rot in spec:
            im = fn().rotate(rot, resample=Image.BICUBIC, expand=True)
            sc = size * 1.25 / max(im.size); im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
            im = im.filter(ImageFilter.MaxFilter(3))          # bolder neon line
            a = np.asarray(im, np.float32) / 255
            pad = 24; a = np.pad(a, pad)
            glow = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(11)), np.float32) / 255
            out.append((x, y, a, glow))
        _ARENA_ICONS = out
    return _ARENA_ICONS

def arena_icon_layer(ph):
    line = np.zeros((H, W), np.float32); glow = np.zeros((H, W), np.float32)
    for i, (x, y, a, g) in enumerate(_arena_icons()):
        ox = 10 * np.sin(TAU * (2 * ph + i * 0.37)); oy = 14 * np.sin(TAU * (3 * ph + i * 0.21))   # gentle float
        h, w = a.shape
        x0, y0 = int(round(x + ox - w / 2)), int(round(y + oy - h / 2))
        xa, ya, xb, yb = max(x0, 0), max(y0, 0), min(x0 + w, W), min(y0 + h, H)
        if xa >= xb or ya >= yb: continue
        line[ya:yb, xa:xb] = np.maximum(line[ya:yb, xa:xb], a[ya - y0:yb - y0, xa - x0:xb - x0])
        glow[ya:yb, xa:xb] = np.maximum(glow[ya:yb, xa:xb], g[ya - y0:yb - y0, xa - x0:xb - x0])
    return line, glow

def neon_arena(t, P):
    ph = t / DUR; name = P.get("name")
    img = stops_radial(QUIZ_STOPS.get(name, DOODLE_STOPS.get(name, PURPLE_REF)), ph)
    light = np.float32([1, 1, 1]) * 0.45 + P["accent"] * 0.55
    yh = H * 0.70                                   # horizon
    below = Y > yh + 1
    dy = np.maximum(Y - yh, 1.0)
    z = 260.0 / dy                                   # depth
    u = (X - CX) * z / 120.0                         # world x in cells
    v = z * 2.2 + ARENA_CELLS_PER_LOOP * ph          # world depth in cells (scrolls toward camera)
    lines = np.maximum(_aa_line(u, 1.6), _aa_line(v, 1.6))
    major = np.maximum(_aa_line(u / 4, 2.4), 0)      # every 4th column brighter
    fog = smooth(0, 160, dy)                         # fade into horizon
    grid = (lines * 0.55 + major * 0.45) * fog * below
    floor = smooth(yh - 2, yh + 30, Y)
    img = img * (1 - 0.45 * floor[..., None])        # darker floor
    img = img + (light - img) * (grid * 0.65)[..., None]
    # horizon glow
    hg = np.exp(-((Y - yh) / 26) ** 2) * (0.55 + 0.45 * np.exp(-((X - CX) / (W * 0.35)) ** 2))
    img = img + (light - img) * (hg * 0.55)[..., None]
    # light beams rising from the bottom corners, crossing outward
    for bx, angs in [(-40, (-62, -78)), (W + 40, (-118, -102))]:
        by = H + 40
        ang = np.degrees(np.arctan2(Y - by, X - bx))
        for i, a in enumerate(angs):
            a0 = a + 4 * np.sin(TAU * (2 * ph + i * 0.25))
            beam = np.exp(-((ang - a0) / 2.6) ** 2) * smooth(1500, 200, np.hypot(X - bx, Y - by))
            beam *= 1 - 0.85 * np.exp(-(((X - CX) / (W * 0.25)) ** 2 + ((Y - CY) / (H * 0.3)) ** 2))
            img = img + (light - img) * (beam * 0.30)[..., None]
    # neon corner brackets
    br = np.zeros((H, W), np.float32); m, L, w = 46, 150, 3
    for cx_, cy_, sx, sy in [(m, m, 1, 1), (W - m, m, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)]:
        hx = (np.abs(Y - cy_) < w / 2 + 0.5) & ((X - cx_) * sx >= 0) & ((X - cx_) * sx < L)
        vy = (np.abs(X - cx_) < w / 2 + 0.5) & ((Y - cy_) * sy >= 0) & ((Y - cy_) * sy < L * 0.6)
        br = np.maximum(br, (hx | vy).astype(np.float32))
    pulse = 0.75 + 0.25 * np.sin(TAU * 3 * ph)
    glow = np.asarray(Image.fromarray((br * 255).astype(np.uint8)).filter(__import__("PIL.ImageFilter", fromlist=["x"]).GaussianBlur(8)), np.float32) / 255
    img = img + (light - img) * (np.clip(br + glow * 1.6, 0, 1) * 0.8 * pulse)[..., None]
    # rising particles near the sides (each wraps once per loop)
    g = np.random.default_rng(11); pt = np.zeros((H, W), np.float32)
    for _ in range(46):
        side = g.uniform() < 0.5
        x = g.uniform(30, W * 0.22) if side else g.uniform(W * 0.78, W - 30)
        y = (g.uniform(0, 1) - ph * int(g.integers(1, 3))) % 1.0 * (H + 40) - 20
        r = g.uniform(1.5, 3.5); a = g.uniform(0.3, 0.9)
        x0, x1, y0, y1 = int(max(x - 8, 0)), int(min(x + 8, W)), int(max(y - 8, 0)), int(min(y + 8, H))
        if x0 < x1 and y0 < y1:
            pt[y0:y1, x0:x1] += np.exp(-((X[y0:y1, x0:x1] - x) ** 2 + (Y[y0:y1, x0:x1] - y) ** 2) / r ** 2) * a
    img = img + (light - img) * np.clip(pt, 0, 1)[..., None] * 0.8
    ln, gl = arena_icon_layer(ph)
    flick = 0.85 + 0.15 * np.sin(TAU * 3 * ph)
    img = img + (light - img) * np.clip(gl * 1.4, 0, 1)[..., None] * 0.45 * flick
    img = img + (light - img) * ln[..., None] * 0.75 * flick
    return img

# ---------------- Design 15: Quiz Pop (dense quiz icons, centre faded) ----------------
_PMOS = None
def _pmosaic():
    global _PMOS
    if _PMOS is None:
        t = np.asarray(doodles.tile(doodles.QUIZPOP_LAYOUT), np.float32) / 255; T = doodles.TILE
        nx, ny = W // T + 4, H // T + 4
        _PMOS = Image.fromarray((np.tile(t, (ny, nx)) * 255).astype(np.uint8))
    return _PMOS

QUIZPOP_DIR = {"blue": (-1, 1),     # top-right -> bottom-left
               "purple": (1, -1),   # bottom-left -> top-right
               "orange": (1, 1),    # top-left -> bottom-right
               "pink": (-1, -1),    # bottom-right -> top-left
               "green": (1, -1)}    # bottom-left -> top-right (only 4 diagonals exist)

def quiz_pop(t, P):
    ph = t / DUR; T = doodles.TILE; name = P.get("name")
    dx, dy = QUIZPOP_DIR.get(name, (1, -1))
    m = _pmosaic().transform((W, H), Image.AFFINE, (1, 0, T * 1.2 - dx * T * ph, 0, 1, T * 1.05 - dy * T * ph), resample=Image.BICUBIC)
    pat = (np.asarray(m, np.float32) / 255)[..., None]
    img = stops_radial(QUIZ_STOPS.get(name, DOODLE_STOPS.get(name, PURPLE_REF)), ph)
    clear = 1 - 0.75 * np.exp(-(((X - CX) / (W * 0.24)) ** 2 + ((Y - CY) / (H * 0.27)) ** 2))[..., None]   # centre stays readable
    tint = np.float32([1, 1, 1]) * 0.5 + img * 0.5
    return img + (tint - img) * pat * 0.30 * clear

DESIGNS = {"hex-pulse": hex_pulse, "radar-rings": radar_rings, "geo-tiles": geo_tiles, "doodle-play": doodle_play, "quiz-doodles": quiz_doodles, "spotlight-stage": spotlight_stage, "neon-arena": neon_arena, "quiz-pop": quiz_pop,
           "bokeh-sparkle": lambda t, P: bokeh_sparkle(t, P, canva_radial(P["c0"], P["c1"]) if "c0" in P else backdrop(P))}

def frame(design, color, t):
    P = pal(color)
    img = DESIGNS[design](t, P)
    vig = 1 if ('stops' in P or design in ('doodle-play', 'quiz-doodles', 'spotlight-stage', 'neon-arena', 'quiz-pop')) else 1 - 0.28 * smooth(0.55, 1.15, np.hypot((X - CX) / (W / 2), (Y - CY) / (H / 2)))[..., None]
    img = np.clip(img * vig + GRAIN, 0, 1)
    return (img * 255 + 0.5).astype(np.uint8)

if __name__ == "__main__":
    a = sys.argv
    design, color, out = a[1], a[2], a[3]
    if "--frame" in a:
        from PIL import Image
        Image.fromarray(frame(design, color, float(a[a.index("--frame") + 1]))).save(a[a.index("--frame") + 2]); sys.exit()
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
        "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(FPS * DUR):
        p.stdin.write(frame(design, color, i / FPS).tobytes())
    p.stdin.close(); p.wait()
