"""Line-art 'doodle' gaming icon tile (original drawings, no text)."""
import math, numpy as np
from PIL import Image, ImageDraw

SS = 4.5          # px per layout unit while drawing (3x supersample x 1.5 scale)
LW = 3.2          # line width at 1x

from PIL import ImageFilter
def _canvas(sz):
    im = Image.new("L", (int(sz * SS), int(sz * SS)), 0); return im, ImageDraw.Draw(im)

def _ln(d, pts, w=LW, v=255):
    pts = [(x * SS, y * SS) for x, y in pts]
    d.line(pts, fill=v, width=int(w * SS), joint="curve")
    for x, y in (pts[0], pts[-1]):
        r = w * SS / 2; d.ellipse([x - r, y - r, x + r, y + r], fill=v)

def _rr(d, box, r, w=LW, fill=None, v=255):
    b = [c * SS for c in box]
    d.rounded_rectangle(b, radius=r * SS, outline=v, width=int(w * SS), fill=fill)

def _el(d, box, w=LW, fill=None, v=255):
    d.ellipse([c * SS for c in box], outline=v, width=int(w * SS), fill=fill)

def _poly(d, pts, w=LW, fill=None, v=255):
    p = [(x * SS, y * SS) for x, y in pts]
    if fill is not None: d.polygon(p, fill=fill)
    _ln(d, pts + [pts[0]], w, v)

def _arc(d, box, a0, a1, w=LW, v=255):
    d.arc([c * SS for c in box], a0, a1, fill=v, width=int(w * SS))

def _arcp(d, cx, cy, rx, ry, a0, a1, w=LW):
    n = 40; _ln(d, [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)], w)

def _outline_shape(im, shape, w=LW):
    """shape: L image of a filled union -> paste soft fill + clean outline."""
    k = int(w * SS) | 1
    inner = shape.filter(ImageFilter.MinFilter(k))
    sa, ia = np.asarray(shape, np.float32), np.asarray(inner, np.float32)
    out = np.maximum(np.asarray(im, np.float32), np.maximum(sa - ia, ia * F / 255))
    return Image.fromarray(out.astype(np.uint8))

def _curve(d, p0, p1, p2, p3, w=LW):
    pts = []
    for i in range(41):
        t = i / 40; u = 1 - t
        pts.append((u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0], u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1]))
    _ln(d, pts, w)

F = 70   # soft fill level for 'filled' doodles

def gamepad():
    im, d = _canvas(160)
    sh, ds = _canvas(160)
    ds.rounded_rectangle([20 * SS, 48 * SS, 140 * SS, 98 * SS], radius=25 * SS, fill=255)
    ds.ellipse([12 * SS, 62 * SS, 62 * SS, 128 * SS], fill=255); ds.ellipse([98 * SS, 62 * SS, 148 * SS, 128 * SS], fill=255)
    im = _outline_shape(im, sh); d = ImageDraw.Draw(im)
    _ln(d, [(42, 62), (42, 88)]); _ln(d, [(29, 75), (55, 75)])
    for (x, y) in [(115, 64), (127, 75), (103, 75), (115, 86)]: _el(d, [x - 5, y - 5, x + 5, y + 5])
    _ln(d, [(70, 74), (77, 74)]); _ln(d, [(84, 74), (91, 74)])
    _curve(d, (80, 48), (80, 25), (120, 35), (140, 12))
    return im

def headphones():
    im, d = _canvas(160)
    _arcp(d, 80, 75, 54, 56, 180, 360)
    _rr(d, [18, 72, 46, 128], 12, fill=F); _rr(d, [114, 72, 142, 128], 12, fill=F)
    _el(d, [24, 86, 40, 114]); _el(d, [120, 86, 136, 114])
    _curve(d, (32, 128), (30, 145), (55, 150), (70, 140)); _el(d, [68, 134, 80, 146], fill=255)
    return im

def trophy():
    im, d = _canvas(160)
    _poly(d, [(45, 25), (115, 25), (108, 80), (80, 95), (52, 80)], fill=F)
    _arc(d, [22, 30, 58, 70], 90, 270); _arc(d, [102, 30, 138, 70], 270, 90)
    _ln(d, [(80, 95), (80, 120)]); _rr(d, [55, 120, 105, 138], 4)
    _poly(d, [(80, 42), (85, 54), (97, 54), (88, 62), (91, 74), (80, 67), (69, 74), (72, 62), (63, 54), (75, 54)])
    return im

def joystick():
    im, d = _canvas(160)
    _rr(d, [35, 105, 125, 135], 10, fill=F)
    _ln(d, [(80, 105), (80, 50)]); _el(d, [62, 22, 98, 58], fill=F)
    _el(d, [100, 112, 114, 126]); _arc(d, [70, 25, 92, 47], 200, 260)
    return im

def handheld():
    im, d = _canvas(160)
    _rr(d, [42, 10, 118, 150], 12, fill=F)
    _rr(d, [52, 22, 108, 72], 4)
    _ln(d, [(62, 98), (62, 118)]); _ln(d, [(52, 108), (72, 108)])
    _el(d, [90, 96, 102, 108]); _el(d, [100, 110, 112, 122])
    _ln(d, [(70, 136), (78, 132)]); _ln(d, [(84, 136), (92, 132)])
    _ln(d, [(60, 40), (75, 30)]); _ln(d, [(60, 52), (88, 32)])
    return im

def bolt():
    im, d = _canvas(120)
    _poly(d, [(62, 8), (30, 64), (56, 64), (42, 112), (90, 46), (62, 46), (78, 8)], fill=F)
    return im

def heart():
    im, d = _canvas(100)
    pts = []
    for i in range(60):
        t = i / 60 * 2 * math.pi
        pts.append((50 + 2.2 * 16 * math.sin(t) ** 3, 48 - 2.2 * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))))
    _poly(d, pts)
    return im

def play():
    im, d = _canvas(130)
    _el(d, [12, 12, 118, 118]); _poly(d, [(52, 40), (52, 90), (92, 65)], fill=F)
    _arc(d, [24, 24, 106, 106], 200, 250)
    return im

def star():
    im, d = _canvas(110)
    p = []
    for i in range(10):
        r = 46 if i % 2 == 0 else 20; a = -math.pi / 2 + i * math.pi / 5
        p.append((55 + r * math.cos(a), 57 + r * math.sin(a)))
    _poly(d, p); return im

def dpad():
    im, d = _canvas(130)
    a, b = 45, 85
    _poly(d, [(a, 12), (b, 12), (b, a), (118, a), (118, b), (b, b), (b, 118), (a, 118), (a, b), (12, b), (12, a), (a, a)], fill=F)
    _el(d, [56, 56, 74, 74])
    return im

def arrow():
    im, d = _canvas(120)
    _ln(d, [(100, 60), (20, 60)]); _ln(d, [(45, 35), (20, 60), (45, 85)])
    for x in (105, 115): pass
    return im

def vr():
    im, d = _canvas(170)
    sh, ds = _canvas(170)
    ds.rounded_rectangle([20 * SS, 45 * SS, 150 * SS, 115 * SS], radius=26 * SS, fill=255)
    ds.ellipse([62 * SS, 96 * SS, 108 * SS, 136 * SS], fill=0)          # nose notch
    im = _outline_shape(im, sh); d = ImageDraw.Draw(im)
    _rr(d, [34, 58, 78, 98], 14); _rr(d, [92, 58, 136, 98], 14)
    _ln(d, [(20, 72), (6, 66)]); _ln(d, [(150, 72), (164, 66)])
    return im

def coin():
    im, d = _canvas(100)
    _el(d, [10, 10, 90, 90], fill=F); _el(d, [24, 24, 76, 76]); _ln(d, [(50, 36), (50, 64)])
    return im

def speaker():
    im, d = _canvas(140)
    _rr(d, [30, 8, 110, 132], 6, fill=F); _el(d, [50, 24, 90, 64]); _el(d, [44, 76, 96, 126]); _el(d, [62, 92, 78, 108])
    return im

def dice():
    im, d = _canvas(110)
    _rr(d, [15, 15, 95, 95], 14, fill=F)
    for x, y in [(35, 35), (75, 35), (55, 55), (35, 75), (75, 75)]: _el(d, [x - 6, y - 6, x + 6, y + 6], fill=255)
    return im

def dots(n=3):
    im, d = _canvas(70)
    for i in range(n): r = 5 + i * 2; _el(d, [10 + i * 18 - r / 2, 35 - r / 2, 10 + i * 18 + r / 2, 35 + r / 2])
    return im

def cable():
    im, d = _canvas(160)
    _curve(d, (10, 120), (40, 20), (110, 150), (150, 40)); return im

def sparkle():
    im, d = _canvas(60)
    _ln(d, [(30, 8), (30, 52)]); _ln(d, [(8, 30), (52, 30)]); return im

# (icon fn, x, y, rotation deg) inside a 640 x 640 tile
LAYOUT = [
    (gamepad, 70, 60, -12), (headphones, 300, 40, 8), (trophy, 510, 70, -6),
    (bolt, 210, 190, 10), (handheld, 400, 200, -10), (heart, 560, 250, 12),
    (joystick, 40, 270, 6), (play, 230, 330, -8), (vr, 450, 390, 5),
    (dpad, 70, 470, 14), (speaker, 290, 470, -4), (coin, 590, 520, 0),
    (star, 170, 560, 18), (dice, 470, 560, -14),
    (dots, 150, 140, 0), (sparkle, 380, 330, 0), (cable, 600, 160, 20), (arrow, 360, 600, 0), (sparkle, 20, 380, 0),
]
TILE = 960        # px at 1x (layout units are 640 -> x1.5)
U = 1.5

def tile(layout=None):
    layout = layout or LAYOUT
    T = TILE * 3
    big = np.zeros((T, T), np.float32)
    for fn, x, y, rot in layout:
        ic = fn().rotate(rot, resample=Image.BICUBIC, expand=True)
        a = np.asarray(ic, np.float32) / 255
        h, w = a.shape
        x0, y0 = int(x * SS - w / 2), int(y * SS - h / 2)   # SS == 3 * U
        for ox in (-T, 0, T):
            for oy in (-T, 0, T):
                X0, Y0 = x0 + ox, y0 + oy
                xa, ya = max(X0, 0), max(Y0, 0); xb, yb = min(X0 + w, T), min(Y0 + h, T)
                if xa < xb and ya < yb:
                    big[ya:yb, xa:xb] = np.maximum(big[ya:yb, xa:xb], a[ya - Y0:yb - Y0, xa - X0:xb - X0])
    return Image.fromarray((big * 255).astype(np.uint8)).resize((TILE, TILE), Image.LANCZOS)


# ======================= Quiz Doodles (design 14) =======================
def qmark(scale=1.0):
    im, d = _canvas(130)
    _arcp(d, 65, 45, 28, 26, 200, 360 + 40)
    _curve(d, (65 + 28 * math.cos(math.radians(40)), 45 + 26 * math.sin(math.radians(40))), (72, 75), (64, 72), (64, 92), w=LW * 1.6)
    _el(d, [58, 104, 70, 116], fill=255)
    return im

def exclaim():
    im, d = _canvas(90)
    _poly(d, [(38, 12), (54, 12), (50, 60), (42, 60)], fill=F); _el(d, [40, 68, 52, 80], fill=255)
    return im

def bulb():
    im, d = _canvas(140)
    sh, ds = _canvas(140)
    ds.ellipse([35 * SS, 18 * SS, 105 * SS, 88 * SS], fill=255)
    ds.polygon([(50 * SS, 78 * SS), (90 * SS, 78 * SS), (84 * SS, 100 * SS), (56 * SS, 100 * SS)], fill=255)
    im = _outline_shape(im, sh); d = ImageDraw.Draw(im)
    _ln(d, [(57, 108), (83, 108)]); _ln(d, [(60, 117), (80, 117)])
    _ln(d, [(62, 92), (62, 70), (70, 62), (78, 70), (78, 92)], w=2.4)
    for a in (-150, -120, -90, -60, -30):
        r0, r1 = 46, 58; c = math.radians(a)
        _ln(d, [(70 + r0 * math.cos(c), 53 + r0 * math.sin(c)), (70 + r1 * math.cos(c), 53 + r1 * math.sin(c))])
    return im

def stopwatch():
    im, d = _canvas(140)
    _el(d, [25, 32, 115, 122], fill=F); _el(d, [38, 45, 102, 109])
    _rr(d, [60, 12, 80, 24], 3); _ln(d, [(70, 24), (70, 32)]); _ln(d, [(104, 34), (112, 26)])
    _ln(d, [(70, 77), (70, 55)]); _ln(d, [(70, 77), (86, 86)]); _el(d, [66, 73, 74, 81], fill=255)
    return im

def buzzer():
    im, d = _canvas(150)
    _rr(d, [22, 88, 128, 122], 8, fill=F)
    sh, ds = _canvas(150)
    ds.pieslice([38 * SS, 48 * SS, 112 * SS, 122 * SS], 180, 360, fill=255)
    ds.rectangle([38 * SS, 84 * SS, 112 * SS, 89 * SS], fill=255)
    im = _outline_shape(im, sh); d = ImageDraw.Draw(im)
    _arcp(d, 75, 84, 24, 20, 215, 260, w=2.4)
    for a in (-140, -90, -40):
        c = math.radians(a); _ln(d, [(75 + 48 * math.cos(c), 80 + 48 * math.sin(c)), (75 + 60 * math.cos(c), 80 + 60 * math.sin(c))])
    return im

def check():
    im, d = _canvas(110)
    _el(d, [10, 10, 100, 100], fill=F); _ln(d, [(32, 56), (48, 72), (78, 38)], w=LW * 1.5)
    return im

def cross():
    im, d = _canvas(110)
    _el(d, [10, 10, 100, 100]); _ln(d, [(37, 37), (73, 73)], w=LW * 1.4); _ln(d, [(73, 37), (37, 73)], w=LW * 1.4)
    return im

def bubble():
    im, d = _canvas(160)
    sh, ds = _canvas(160)
    ds.rounded_rectangle([14 * SS, 22 * SS, 146 * SS, 108 * SS], radius=30 * SS, fill=255)
    ds.polygon([(40 * SS, 100 * SS), (34 * SS, 138 * SS), (70 * SS, 104 * SS)], fill=255)
    im = _outline_shape(im, sh); d = ImageDraw.Draw(im)
    for x in (55, 80, 105): _el(d, [x - 7, 58, x + 7, 72], fill=255)
    return im

def puzzle():
    im, d = _canvas(140)
    sh, ds = _canvas(140)
    ds.rectangle([28 * SS, 38 * SS, 102 * SS, 112 * SS], fill=255)
    ds.ellipse([52 * SS, 18 * SS, 78 * SS, 44 * SS], fill=255)      # top knob
    ds.ellipse([96 * SS, 62 * SS, 122 * SS, 88 * SS], fill=255)     # right knob
    ds.ellipse([52 * SS, 100 * SS, 78 * SS, 126 * SS], fill=0)      # bottom socket
    im = _outline_shape(im, sh)
    return im

def magnifier():
    im, d = _canvas(140)
    _el(d, [20, 20, 90, 90], fill=F); _arcp(d, 55, 55, 24, 24, 200, 260, w=2.4)
    _ln(d, [(82, 82), (118, 118)], w=LW * 2.6)
    return im

def pencil():
    im, d = _canvas(150)
    _poly(d, [(30, 120), (36, 98), (108, 26), (124, 42), (52, 114)], fill=F)
    _ln(d, [(96, 38), (112, 54)]); _ln(d, [(36, 98), (52, 114)])
    return im

def medal():
    im, d = _canvas(130)
    _poly(d, [(40, 8), (58, 8), (70, 48), (52, 48)]); _poly(d, [(90, 8), (72, 8), (60, 48), (78, 48)])
    _el(d, [33, 50, 97, 114], fill=F); _el(d, [46, 63, 84, 101])
    return im

QUIZ_LAYOUT = [
    (qmark, 70, 70, -14), (bulb, 260, 60, 8), (stopwatch, 470, 80, -6),
    (check, 600, 220, 0), (bubble, 380, 230, -4), (exclaim, 190, 200, 12),
    (buzzer, 70, 300, 4), (puzzle, 250, 380, 10), (qmark, 480, 370, 16),
    (magnifier, 80, 500, -10), (pencil, 330, 520, 0), (medal, 560, 500, 8),
    (cross, 190, 590, -8), (star, 460, 590, 14),
    (dots, 160, 130, 0), (sparkle, 340, 140, 0), (sparkle, 600, 360, 0), (heart, 620, 620, 10), (dots, 400, 610, 0),
]


# ======================= Quiz Pop (design 15) extra icons =======================
def flag():
    im, d = _canvas(150)
    _ln(d, [(30, 140), (30, 18)], w=LW * 1.3)
    # waving flag outline
    top = [(30 + i * 1.0, 20 + 8 * math.sin(i / 90 * 2 * math.pi)) for i in range(0, 91, 5)]
    bot = [(30 + i * 1.0, 78 + 8 * math.sin(i / 90 * 2 * math.pi)) for i in range(90, -1, -5)]
    pts = top + bot
    p = [(x * SS, y * SS) for x, y in pts]
    d.polygon(p, fill=F)
    # checker squares
    for r in range(4):
        for c in range(6):
            if (r + c) % 2 == 0:
                x0 = 30 + c * 15; yo = 8 * math.sin((c * 15 + 7.5) / 90 * 2 * math.pi)
                y0 = 20 + r * 14.5 + yo
                d.polygon([((x0) * SS, (y0) * SS), ((x0 + 15) * SS, (y0) * SS), ((x0 + 15) * SS, (y0 + 14.5) * SS), (x0 * SS, (y0 + 14.5) * SS)], fill=255)
    _ln(d, pts + [pts[0]])
    return im

def qbubble():
    im, d = _canvas(150)
    sh, ds = _canvas(150)
    ds.rounded_rectangle([14 * SS, 18 * SS, 136 * SS, 104 * SS], radius=28 * SS, fill=255)
    ds.polygon([(96 * SS, 96 * SS), (120 * SS, 132 * SS), (70 * SS, 102 * SS)], fill=255)
    im = _outline_shape(im, sh); d = ImageDraw.Draw(im)
    _arcp(d, 75, 48, 15, 14, 200, 400, w=LW * 1.4)
    _ln(d, [(75 + 15 * math.cos(math.radians(40)), 48 + 14 * math.sin(math.radians(40))), (75, 68), (75, 74)], w=LW * 1.4)
    _el(d, [71, 82, 79, 90], fill=255)
    return im

def burst():
    im, d = _canvas(90)
    for a in (-60, -30, 0):
        c = math.radians(a - 90); _ln(d, [(45 + 14 * math.cos(c), 70 + 14 * math.sin(c)), (45 + 44 * math.cos(c), 70 + 44 * math.sin(c))], w=LW * 1.3)
    return im

def ring():
    im, d = _canvas(60)
    _el(d, [12, 12, 48, 48], w=LW * 1.2); return im

def bigq():
    im, d = _canvas(140)
    _arcp(d, 70, 48, 30, 28, 200, 400, w=LW * 2.4)
    _curve(d, (70 + 30 * math.cos(math.radians(40)), 48 + 28 * math.sin(math.radians(40))), (72, 80), (70, 84), (70, 96), w=LW * 2.4)
    _el(d, [62, 108, 78, 124], fill=255)
    return im

QUIZPOP_LAYOUT = [
    (bigq, 60, 60, -14), (bulb, 220, 70, 10), (flag, 380, 60, -12), (qbubble, 560, 90, 6),
    (stopwatch, 120, 230, -10), (star, 260, 200, 15), (trophy, 420, 240, 4), (burst, 560, 230, -20),
    (flag, 70, 400, 10), (qbubble, 230, 380, -8), (bigq, 400, 420, 12), (bulb, 560, 400, -8),
    (trophy, 120, 560, -6), (stopwatch, 300, 580, 8), (star, 470, 560, -10), (flag, 600, 590, 6),
    (ring, 170, 140, 0), (ring, 480, 330, 0), (ring, 30, 300, 0), (sparkle, 330, 320, 0), (sparkle, 620, 300, 0),
    (dots, 340, 130, 0), (burst, 30, 480, 30), (ring, 380, 500, 0), (sparkle, 200, 480, 0),
]


# ======================= Icon Frame (design 16) extra icons =======================
def rocket():
    im, d = _canvas(150)
    sh, ds = _canvas(150)
    body = [(75, 10), (98, 40), (100, 100), (50, 100), (52, 40)]
    ds.polygon([(x * SS, y * SS) for x, y in body], fill=255)
    ds.ellipse([50 * SS, 10 * SS, 100 * SS, 70 * SS], fill=255)
    im2 = _outline_shape(Image.new("L", im.size, 0), sh); a = np.asarray(im2, np.float32); a[a < 200] = 0
    im = Image.fromarray(a.astype(np.uint8)); d = ImageDraw.Draw(im)
    _el(d, [64, 46, 86, 68])
    _poly(d, [(52, 72), (32, 104), (52, 98)]); _poly(d, [(98, 72), (118, 104), (98, 98)])
    _ln(d, [(66, 108), (62, 128)]); _ln(d, [(75, 108), (75, 136)]); _ln(d, [(84, 108), (88, 128)])
    return im

def target():
    im, d = _canvas(150)
    for r in (56, 38, 20): _el(d, [70 - r, 80 - r, 70 + r, 80 + r])
    _el(d, [66, 76, 74, 84], fill=255)
    _ln(d, [(70, 80), (128, 22)]); _ln(d, [(116, 22), (128, 22), (128, 34)]); _ln(d, [(112, 16), (122, 28)])
    return im

def gear():
    im, d = _canvas(140)
    pts = []; n = 8
    for i in range(n):
        c = i / n * 2 * math.pi; tw = math.pi / n * 0.42
        for ang, r in [(c - tw * 1.35, 44), (c - tw, 58), (c + tw, 58), (c + tw * 1.35, 44)]:
            pts.append((70 + r * math.cos(ang), 70 + r * math.sin(ang)))
        mid = c + math.pi / n
        pts.append((70 + 44 * math.cos(mid), 70 + 44 * math.sin(mid)))
    _poly(d, pts); _el(d, [52, 52, 88, 88])
    return im

def plane():
    im, d = _canvas(150)
    _poly(d, [(14, 70), (136, 20), (96, 128), (74, 88)])
    _ln(d, [(74, 88), (136, 20)]); _ln(d, [(74, 88), (70, 118), (84, 100)])
    return im

def palette():
    im, d = _canvas(150)
    sh, ds = _canvas(150)
    ds.ellipse([15 * SS, 25 * SS, 135 * SS, 125 * SS], fill=255)
    ds.ellipse([86 * SS, 78 * SS, 112 * SS, 104 * SS], fill=0)
    im2 = _outline_shape(Image.new("L", im.size, 0), sh); a = np.asarray(im2, np.float32); a[a < 200] = 0
    im = Image.fromarray(a.astype(np.uint8)); d = ImageDraw.Draw(im)
    for x, y in [(45, 70), (62, 48), (90, 48), (48, 98)]: _el(d, [x - 9, y - 9, x + 9, y + 9])
    return im

def hexa():
    im, d = _canvas(120)
    _poly(d, [(60 + 46 * math.cos(math.radians(a)), 60 + 46 * math.sin(math.radians(a))) for a in range(0, 360, 60)]); return im

def tri():
    im, d = _canvas(110)
    _poly(d, [(55, 14), (98, 90), (12, 90)]); return im

def square():
    im, d = _canvas(110)
    _rr(d, [20, 20, 90, 90], 6); return im

def diamond():
    im, d = _canvas(110)
    _poly(d, [(55, 10), (100, 55), (55, 100), (10, 55)]); return im

def zigzag():
    im, d = _canvas(130)
    _ln(d, [(10 + i * 18, 70 + (-16 if i % 2 else 16)) for i in range(7)]); return im

def xcross():
    im, d = _canvas(80)
    _ln(d, [(22, 22), (58, 58)]); _ln(d, [(58, 22), (22, 58)]); return im

def blob():
    im, d = _canvas(120)
    pts = [(60 + (40 + 6 * math.cos(4 * a)) * math.cos(a), 60 + (40 + 6 * math.cos(4 * a)) * math.sin(a)) for a in [i / 40 * 2 * math.pi for i in range(40)]]
    _poly(d, pts); return im

def dashed_path():
    im, d = _canvas(160)
    pts = []
    for i in range(61):
        t = i / 60; pts.append((20 + 120 * t, 140 - 120 * t + 50 * math.sin(t * math.pi)))
    for i in range(0, 60, 6): _ln(d, pts[i:i + 3])
    return im

def bigring():
    im, d = _canvas(120)
    _el(d, [14, 14, 106, 106]); return im
