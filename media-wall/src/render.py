"""Media wall render, v10: drawn to the client's hand-measured room (inputs/room_sketch_accurate_mm.png)
in real cm, with a simple one-point perspective.
Usage: python3 render.py  -> v10_*.svg (rasterise with shot.py)

Coordinates: x runs from the east (left) wall towards the west, y up from the floor, z from the chimney
breast's face (z = 0) back into the alcove (+z, back wall at z = 38) and out into the room (-z).
"""
import math, random

W, H = 1900, 1300
SHIFT = 0           # v10: the camera itself is framed to take in the ceiling and the spotlight bar
S = 3.6             # px per cm at the breast-face plane (z = 0)
X0, Y0 = 376, 1038  # px of the east wall / floor at the breast-face plane
EYE_X, EYE_Y = 140.0, 112.0   # camera: between the alcove and the breast, seated eye height
VX = X0 + EYE_X * S
VY = Y0 - EYE_Y * S
D = 505.0           # camera distance from the breast-face plane, cm (a cutaway: the window wall is at z = -309)

XOFF = YOFF = ZOFF = 0.0   # offsets applied by P(), used to place whole groups
RAISE = 9.0         # plinth under the two BESTÅ frames: their tops at 73, worktop top at 76

# ---------------------------------------------------------------- the real room (cm), v10
ALC_W, ALC_D, CEIL = 186.0, 38.0, 235.0     # TV alcove: east wall to chimney breast, depth, floor to ceiling
BREAST_W = 117.5                            # chimney breast face
BR_X2 = ALC_W + BREAST_W                    # 303.5: the breast's west jamb
REC_D = 39.0                                # west recess depth (breast projects 390 on that side)
ROOM_D = 347.0                              # window wall to the alcove's back wall
WIN_Z = ALC_D - ROOM_D                      # -309: the window wall
SKIRT_H, SKIRT_T = 6.0, 2.0
# the base in the alcove: 3 + 60 + 60 + 60 + 3
BAYS = [(3.0, 63.0), (63.0, 123.0), (123.0, 183.0)]
BASE_F = -8.0       # front of the oak face frame: 8 cm proud of the breast
CARC_F = -6.0       # front of the frames and carcass (40 deep)
CARC_B = 34.0       # back of the frames: a 4 cm cable channel to the wall at 38
WT = 76.0           # worktop top
WT_TH = 3.0
# above the worktop
UPL, UPR = (25.25, 29.75), (156.25, 160.75)   # oak uprights, 4.5 thick, 126.5 clear between
UP_D = 30.0
UP_Z = ALC_D - UP_D                         # uprights' front face, z = 8
TV_W, TV_H, TV_D = 122.2, 70.4, 4.6
TV_CX = (UPL[1] + UPR[0]) / 2               # 93.0
TV_Y = WT + 5.4                             # bottom of the screen on LG's stand: 81.4
HS_TOP, HS_TH = 200.0, 4.0                  # high shelf top (35 cm to the ceiling)
SH_TOP = 156.0                              # left and right shelves
LEDGE_Y, LEDGE_TOP = 153.0, 155.4           # record ledge underside / top
# the vinyl cabinet against the chimney breast
CAB_X1, CAB_X2 = 188.0, 288.0
CAB_F = -44.0       # face frame front; carcass 40 deep, 2 cm off the breast for the skirting
CAB_TOP = 76.0


def at3(dx, dy, dz, fn, *a, **kw):
    """Draw fn with every point shifted by (dx, dy, dz) cm."""
    global XOFF, YOFF, ZOFF
    old = (XOFF, YOFF, ZOFF)
    XOFF, YOFF, ZOFF = old[0] + dx, old[1] + dy, old[2] + dz
    try:
        return fn(*a, **kw)
    finally:
        XOFF, YOFF, ZOFF = old

def at(off, fn, *a, **kw):
    return at3(0, off, 0, fn, *a, **kw)

def P(x, y, z):
    x, y, z = x + XOFF, y + YOFF, z + ZOFF
    k = D / (D + z)
    return (VX + (X0 + x * S - VX) * k, VY + (Y0 - y * S - VY) * k)

def pts(*p):
    return " ".join(f"{a:.1f},{b:.1f}" for a, b in p)

def poly(points, fill, extra=""):
    return f'<polygon points="{pts(*points)}" fill="{fill}" {extra}/>'

def quad_front(x, y, z, w, h, fill, extra=""):
    return poly([P(x, y, z), P(x + w, y, z), P(x + w, y + h, z), P(x, y + h, z)], fill, extra)

def box(x, y, z, w, h, d, front, top=None, side=None, bottom=None, extra=""):
    """Axis-aligned box. (x,y,z) = front-bottom-left; extends +x, +y (up), +z (back).
    Faces are culled against the camera using the offset (world) position."""
    top = top or front
    side = side or front
    bottom = bottom or side
    out = []
    wx, wy = x + XOFF, y + YOFF
    if wx + w < EYE_X:   # right face visible
        out.append(poly([P(x + w, y, z), P(x + w, y, z + d), P(x + w, y + h, z + d), P(x + w, y + h, z)], side, extra))
    if wx > EYE_X:       # left face visible
        out.append(poly([P(x, y, z), P(x, y, z + d), P(x, y + h, z + d), P(x, y + h, z)], side, extra))
    if wy + h < EYE_Y:   # top visible
        out.append(poly([P(x, y + h, z), P(x + w, y + h, z), P(x + w, y + h, z + d), P(x, y + h, z + d)], top, extra))
    if wy > EYE_Y:       # underside visible
        out.append(poly([P(x, y, z), P(x + w, y, z), P(x + w, y, z + d), P(x, y, z + d)], bottom, extra))
    out.append(quad_front(x, y, z, w, h, front, extra))
    return "\n".join(out)

def ellipse_flat(cx, y, cz, rx, rz, fill, extra="", n=48):
    """Horizontal ellipse/circle on the plane at height y."""
    p = [P(cx + rx * math.cos(t), y, cz + rz * math.sin(t)) for t in [2 * math.pi * i / n for i in range(n)]]
    return poly(p, fill, extra)

def text(x, y, s, size=13, anchor="start", weight=500, fill="#f3ead8", op=1.0, extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter, sans-serif" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" fill-opacity="{op}" text-anchor="{anchor}" '
            f'paint-order="stroke" stroke="#10241b" stroke-opacity="0.55" stroke-width="3" '
            f'stroke-linejoin="round" {extra}>{s}</text>')

# ---------------------------------------------------------------- palette
G_WALL   = "#2f5b46"   # deep green, lit wall facing camera
G_LEFT0  = "#21443a"   # left wall, near camera (darker)
G_LEFT1  = "#2a5141"   # left wall, near alcove
G_REVR   = "#28503e"
G_REVT   = "#1d3d30"
G_FELT   = "#16271f"
G_FRAME  = "#2d5a44"
G_FRAME_T = "#3a6b53"
G_FRAME_S = "#244a38"
GH = 'filter="url(#grainH)"'; GV = 'filter="url(#grainV)"'
OAK = "#c48c57"; OAK_T = "#d9a46c"; OAK_S = "#9c6a3f"; OAK_D = "#a87443"
BLK = "#18191a"; BLK_T = "#2a2c2e"; BLK_S = "#0e0f10"
WHT = "#ece9e2"; WHT_T = "#f7f5f0"; WHT_S = "#cfcac0"


def defs():
    return f'''<defs>
  <linearGradient id="leftwall" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{G_LEFT0}"/><stop offset="1" stop-color="{G_LEFT1}"/></linearGradient>
  <linearGradient id="backwall" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#2c5643"/><stop offset="1" stop-color="#2a5340"/></linearGradient>
  <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#7d776e"/><stop offset="1" stop-color="#5d5850"/></linearGradient>
  <linearGradient id="screen" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#1b1638"/><stop offset="0.45" stop-color="#4a2d5e"/>
    <stop offset="0.72" stop-color="#c0566a"/><stop offset="0.88" stop-color="#f2a65e"/>
    <stop offset="1" stop-color="#f6c97c"/></linearGradient>
  <radialGradient id="sun" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#fff2c4" stop-opacity="1"/><stop offset="0.35" stop-color="#ffd68a" stop-opacity="0.7"/>
    <stop offset="1" stop-color="#ffb070" stop-opacity="0"/></radialGradient>
  <radialGradient id="bias" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#eef3ff" stop-opacity="0.55"/><stop offset="0.6" stop-color="#d9e4ff" stop-opacity="0.18"/>
    <stop offset="1" stop-color="#d9e4ff" stop-opacity="0"/></radialGradient>
  <linearGradient id="ledDown" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffcf8a" stop-opacity="0.55"/><stop offset="1" stop-color="#ffcf8a" stop-opacity="0"/></linearGradient>
  <linearGradient id="bayLight" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f6dcae"/><stop offset="1" stop-color="#b99c74"/></linearGradient>
  <linearGradient id="bayLightW" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f4f1ea"/><stop offset="1" stop-color="#cdc7bb"/></linearGradient>
  <linearGradient id="bayBack" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#3b3226"/><stop offset="1" stop-color="#1c1813"/></linearGradient>
  <linearGradient id="seriesGlow" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#3dff8a" stop-opacity="0.55"/><stop offset="1" stop-color="#3dff8a" stop-opacity="0"/></linearGradient>
  <linearGradient id="pot" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#b8603c"/><stop offset="1" stop-color="#d0794f"/></linearGradient>
  <linearGradient id="art1" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#e9b44c"/><stop offset="0.5" stop-color="#e2683c"/><stop offset="1" stop-color="#7a2e5a"/></linearGradient>
  <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#ffffff" stop-opacity="0.22"/><stop offset="1" stop-color="#ffffff" stop-opacity="0.05"/></linearGradient>
  <radialGradient id="pcglow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#40e0b0" stop-opacity="0.35"/><stop offset="1" stop-color="#40e0b0" stop-opacity="0"/></radialGradient>
  <radialGradient id="warmpool" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#ffc77a" stop-opacity="0.35"/><stop offset="1" stop-color="#ffc77a" stop-opacity="0"/></radialGradient>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>
  <filter id="grainV" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.55 0.012" numOctaves="2" seed="4" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.30  0 0 0 0 0.16  0 0 0 0 0.06  1.5 0 0 0 -0.62" result="s"/>
    <feComposite in="s" in2="SourceGraphic" operator="in" result="c"/><feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="c"/></feMerge></filter>
  <filter id="grainH" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.010 0.5" numOctaves="2" seed="7" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.30  0 0 0 0 0.16  0 0 0 0 0.06  1.5 0 0 0 -0.62" result="s"/>
    <feComposite in="s" in2="SourceGraphic" operator="in" result="c"/><feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="c"/></feMerge></filter>
  <linearGradient id="shadeDown" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0.30"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>
  <linearGradient id="shadeL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity="0.22"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>
  <linearGradient id="shadeR" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#000" stop-opacity="0.22"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>
  <linearGradient id="ledWash" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe3b3" stop-opacity="0.42"/><stop offset="1" stop-color="#ffe3b3" stop-opacity="0"/></linearGradient>
  <radialGradient id="lantern" cx="0.5" cy="0.55" r="0.5"><stop offset="0" stop-color="#fffaf0"/><stop offset="0.7" stop-color="#fbeed6"/><stop offset="1" stop-color="#ecd7b0"/></radialGradient>
  <radialGradient id="lanternGlow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#ffd896" stop-opacity="0.55"/><stop offset="1" stop-color="#ffd896" stop-opacity="0"/></radialGradient>
  <filter id="softer" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
</defs>'''



SKIRT = None   # None = painted in the wall colour (eggshell); or a 5-tuple of colours
STYLE = "joinery"    # "joinery" (main) or "slats" (alternative)
FAR = -470.0         # nearest wall/floor depth drawn (P() breaks at z <= -505)

def room():
    """The room shell, v10: alcove 186 wide x 38 deep on the east end of the south wall, the chimney breast
    (117.5 wide) beside it, the west recess (39 deep) beyond, one 235 cm ceiling, 6 cm skirting."""
    o = []
    o.append(f'<rect x="0" y="-60" width="{W}" height="{H + 120}" fill="url(#backwall)"/>')
    XR = 640.0      # draw the recess and floor well past the frame's right edge
    # floor (walls drawn over it hide the parts behind them)
    a, b = P(0, 0, ALC_D), P(XR, 0, ALC_D)
    o.append(poly([a, b, (W + 10, b[1]), (W + 10, H + 10), P(0, 0, FAR)], "url(#floor)"))
    # ceiling, one plane at 235
    a, b = P(0, CEIL, ALC_D), P(XR, CEIL, ALC_D)
    o.append(poly([a, b, (W + 10, b[1]), (W + 10, -70), (-10, -70), P(0, CEIL, FAR)], "#33604a"))
    # west recess back wall, alcove back wall, alcove floor, reveal, chimney breast face
    o.append(quad_front(BR_X2, 0, REC_D, XR - BR_X2, CEIL, "#2a5340"))
    o.append(quad_front(0, 0, ALC_D, ALC_W, CEIL, "#244a39"))
    o.append(poly([P(0, 0, 0), P(ALC_W, 0, 0), P(ALC_W, 0, ALC_D), P(0, 0, ALC_D)], "#4f4a43"))
    o.append(poly([P(ALC_W, 0, 0), P(ALC_W, CEIL, 0), P(ALC_W, CEIL, ALC_D), P(ALC_W, 0, ALC_D)], G_REVR))
    o.append(quad_front(ALC_W, 0, 0, BREAST_W, CEIL, G_WALL))
    # east (left) wall, from the room into the alcove
    o.append(poly([P(0, CEIL, FAR), P(0, CEIL, ALC_D), P(0, 0, ALC_D), P(0, 0, FAR)], "url(#leftwall)"))
    for (p, q) in [(P(ALC_W, CEIL, 0), P(BR_X2, CEIL, 0)), (P(0, CEIL, ALC_D), P(ALC_W, CEIL, ALC_D)),
                   (P(BR_X2, CEIL, REC_D), P(XR, CEIL, REC_D))]:
        o.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="#264c3a" stroke-width="1.5"/>')
    # skirting, 6 high x 2 thick, painted in the wall colour: breast face, recess, east wall
    sk = SKIRT or ("#346650", "#3d7259", "#2b5643", "#2d5a46", "#3b6e56")
    o.append(box(BR_X2, 0, REC_D - SKIRT_T, XR - BR_X2, SKIRT_H, SKIRT_T, sk[0], sk[1], sk[2]))
    o.append(box(ALC_W, 0, -SKIRT_T, BREAST_W, SKIRT_H, SKIRT_T, sk[0], sk[1], sk[2]))
    o.append(poly([P(0, 0, BASE_F), P(0, SKIRT_H, BASE_F), P(0, SKIRT_H, FAR), P(0, 0, FAR)], sk[3]))
    o.append(poly([P(0, SKIRT_H, BASE_F), P(SKIRT_T, SKIRT_H, BASE_F), P(SKIRT_T, SKIRT_H, FAR), P(0, SKIRT_H, FAR)], sk[4]))
    # rug in front of the wall
    o.append(poly([P(18, 0.1, -62), P(262, 0.1, -62), P(262, 0.1, -300), P(18, 0.1, -300)], "#8a7f70", 'opacity="0.55"'))
    return "\n".join(o)


def slats():
    """Slat wall alternative: oak slats on battens on the alcove's back wall, worktop to ceiling."""
    o = []
    y0, y1 = WT, CEIL
    o.append(quad_front(0, y0, ALC_D, ALC_W, y1 - y0, G_FELT))
    x = 1.0
    rnd = random.Random(4)
    while x < ALC_W - 1:
        c = rnd.choice(["#bf8853", "#c58f59", "#b98250", "#c99560", "#b57d4b"])
        o.append(quad_front(x, y0, ALC_D, 2.6, y1 - y0, c))
        o.append(quad_front(x + 2.1, y0, ALC_D, 0.5, y1 - y0, "#9b6a3e", 'opacity="0.6"'))
        x += 4.0
    return "\n".join(o)


def high_shelf():
    """High shelf, top 200 (35 cm to the ceiling): solid oak 30 x 4, wall to wall, housed into both uprights.
    Books up to about 30 cm in the middle, a lidded box, a print; Deco B on the right end."""
    o = []
    y = HS_TOP - HS_TH
    zf = ALC_D - 30
    o.append(poly([P(0, y - 34, ALC_D - 0.1), P(ALC_W, y - 34, ALC_D - 0.1), P(ALC_W, y, ALC_D - 0.1), P(0, y, ALC_D - 0.1)],
                  "url(#ledDown)", 'opacity="0.45"' if STYLE == "joinery" else ""))
    o.append(box(0, y, zf, ALC_W, HS_TH, 30, OAK, OAK_T, OAK_S, "#8e6038", GH))
    if STYLE == "joinery":   # chamfered front edge
        a_, b_ = P(0, y + HS_TH - 0.4, zf - 0.01), P(ALC_W, y + HS_TH - 0.4, zf - 0.01)
        o.append(f'<line x1="{a_[0]:.1f}" y1="{a_[1]:.1f}" x2="{b_[0]:.1f}" y2="{b_[1]:.1f}" stroke="#e9bd86" stroke-width="1.2"/>')
    cols = ["#2f3e5c", "#c8452f", "#e0b43a", "#1f6f8b", "#efe6d2", "#3a3a3a", "#6a8f5a", "#b3307a", "#d27a2e", "#14806d"]
    # left end: a short stack of books lying flat and a small pot
    for i, (bw, bh, c) in enumerate([(19, 3.0, "#2f3e5c"), (17.5, 2.6, "#e0b43a"), (18.5, 3.4, "#c8452f")]):
        yy = HS_TOP + sum(v[1] for v in [(19, 3.0), (17.5, 2.6), (18.5, 3.4)][:i])
        o.append(box(3 + i * 0.6, yy, 20, bw, bh, 15, c, side="#222"))
    o.append(box(8, HS_TOP + 9.0, 24, 9, 9, 9, "#c76d45", "#d98a62", "#a85a38"))
    o.append(ellipse_flat(12.5, HS_TOP + 18.1, 28.5, 4.6, 4.6, "#3a8f4a"))
    # centre: books (hardbacks and paperbacks, up to 30 cm), then an oak bookend
    rnd = random.Random(9)
    x = UPL[1] + 2.0
    while x < 88:
        tw = rnd.choice([2.2, 2.6, 3.0, 3.4, 4.0, 2.0])
        th_ = rnd.choice([21.6, 23.4, 24.0, 19.8, 25.0, 24.0, 28.5, 29.5])
        col = rnd.choice(cols)
        o.append(box(x, HS_TOP, 21, tw, th_, rnd.choice([15.5, 16, 17]), col, side="#222"))
        o.append(box(x + tw * 0.2, HS_TOP + th_ * 0.62, 20.99, tw * 0.6, 1.0, 0.1, "#f2efe6"))
        x += tw + 0.1
    o.append(box(x + 0.3, HS_TOP, 21, 1.8, 16, 15, OAK, OAK_T, OAK_S))
    # one lidded storage box for cables and controllers
    bx = 96.0
    o.append(box(bx, HS_TOP, 12, 32, 21, 25, "#a7a29a", "#bcb7ae", "#8f8a82"))
    o.append(box(bx, HS_TOP + 21, 12, 32, 1.5, 25, "#b3aea6", "#c4bfb6", "#9a958c"))
    a, b = P(bx + 12, HS_TOP + 13, 12), P(bx + 20, HS_TOP + 13, 12)
    o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#77736b" stroke-width="2"/>')
    # framed print leaning on the wall, and a small vase
    o.append(box(131, HS_TOP, 34, 22, 27, 2, "url(#art1)", side="#555"))
    o.append(box(146, HS_TOP, 26, 6, 13, 6, "#e8e2d6", "#f3eee5", "#cfc8bb"))
    # Deco B on the right end (11 x 11 x 11.4), the Cat6 dropping in from the ceiling in the corner
    dx0 = 168.5
    o.append(box(dx0, HS_TOP, 22, 11, 11.4, 11, WHT, WHT_T, WHT_S, extra='rx="6"'))
    o.append(ellipse_flat(dx0 + 5.5, HS_TOP + 11.45, 27.5, 1.6, 1.6, "#4fd17a"))          # solid green = online
    o.append(ellipse_flat(dx0 + 5.5, HS_TOP + 11.5, 27.5, 3.2, 3.2, "#4fd17a", 'opacity="0.25"'))
    st = P(dx0 + 10.5, HS_TOP + 4, 32); en = P(183.5, CEIL, 36.5)
    o.append(f'<path d="M{st[0]:.1f},{st[1]:.1f} Q{en[0]:.1f},{st[1]-4:.1f} {en[0]:.1f},{en[1]:.1f}" stroke="#7d8c84" stroke-width="2" fill="none" opacity="0.85"/>')
    if STYLE == "joinery":   # Deco's 12 V lead and patch lead along the back of the shelf into the groove behind the right upright
        a_, c_ = P(dx0 + 1, HS_TOP + 0.3, 31.5), P(UPR[0] + 2.2, HS_TOP + 0.3, ALC_D - 0.3)
        o.append(f'<path d="M{a_[0]:.1f},{a_[1]:.1f} L{c_[0]:.1f},{c_[1]:.1f}" stroke="#2b2b2b" stroke-width="2.2" fill="none"/>')
    return "\n".join(o)


def side_shelves():
    """Left and right oak shelves, top 156, 25 deep: through-tenoned into the uprights (joinery) or on cleats (slats)."""
    o = []
    th = 4.0
    z0 = ALC_D - 25
    for (x1, x2) in ((0.0, UPL[0]), (UPR[1], ALC_W)):
        o.append(poly([P(x1 + 1, SH_TOP - th - 30, ALC_D - 0.1), P(x2 - 1, SH_TOP - th - 30, ALC_D - 0.1),
                       P(x2 - 1, SH_TOP - th, ALC_D - 0.1), P(x1 + 1, SH_TOP - th, ALC_D - 0.1)], "url(#ledDown)"))
        o.append(box(x1, SH_TOP - th, z0, x2 - x1, th, 25, OAK, OAK_T, OAK_S, extra=GH))
    # left: a few favourite games standing, and a small red speaker
    cols = ["#1d7a3a", "#2b2b2b", "#1f5fa8", "#c23b2e", "#e0b43a", "#2f8f4e"]
    x = 3.0
    for c in cols:
        o.append(box(x, SH_TOP, 22, 1.5, 19, 13.5, c, side="#111"))
        x += 1.6
    o.append(box(14.0, SH_TOP, 24, 9, 10, 9, "#c84b34", "#d8634b", "#a83d2a"))
    # right: a 7-inch single in a small frame and a trailing plant
    o.append(box(UPR[1] + 3, SH_TOP, 33, 20, 20, 1.6, "#1b1b1b", side="#111"))
    o.append(quad_front(UPR[1] + 4.2, SH_TOP + 1.2, 32.9, 17.6, 17.6, "#e9b44c"))
    o.append(quad_front(UPR[1] + 6.5, SH_TOP + 3.5, 32.8, 13, 13, "#c8452f"))
    c = P(UPR[1] + 13, SH_TOP + 10, 32.7)
    o.append(f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="5" fill="#1b1b1b"/>')
    o.append(box(UPR[1] + 13, SH_TOP, 20, 9, 8, 9, "#e7e1d4", "#f2ede3", "#cbc4b6"))
    p = P(UPR[1] + 17.5, SH_TOP + 8, 24)
    for i, (dx, dy) in enumerate([(-14, 40), (-4, 62), (8, 48)]):
        o.append(f'<path d="M{p[0]:.1f},{p[1]:.1f} q {dx/2:.1f},{dy/3:.1f} {dx:.1f},{dy:.1f}" stroke="#2f6f3a" stroke-width="2" fill="none"/>')
        for t in range(4):
            lx, ly = p[0] + dx * (t + 1) / 4, p[1] + dy * (t + 1) / 4
            o.append(f'<ellipse cx="{lx:.1f}" cy="{ly:.1f}" rx="5" ry="3" fill="#3a8f4a" transform="rotate({-30 + i * 25} {lx:.1f} {ly:.1f})"/>')
    return "\n".join(o)


def tv():
    """LG OLED C6 55in (122.2 x 70.4 x 4.6) on LG's stand (47 x 23.1), centred between the uprights."""
    o = []
    x, y, z, w, h = TV_CX - TV_W / 2, TV_Y, 18.0, TV_W, TV_H
    o.append(box(TV_CX - 23.5, WT, 9.0, 47, 1.6, 23.1, "#2a2a2c", "#3a3a3d", "#202022"))
    o.append(box(TV_CX - 6, WT + 1.6, 18.5, 12, TV_Y - WT - 1.6 + 1, 3, "#232325"))
    o.append(box(x, y, z, w, h, TV_D, "#0d0d0f", "#202022", "#151517"))
    a, b = P(x + 0.6, y + h - 0.6, z), P(x + w - 0.6, y + 0.6, z)
    sx, sy, sw, sh = a[0], a[1], b[0] - a[0], b[1] - a[1]
    o.append(f'<svg x="{sx:.1f}" y="{sy:.1f}" width="{sw:.1f}" height="{sh:.1f}" viewBox="0 0 100 57.6" preserveAspectRatio="none">'
             f'<rect width="100" height="57.6" fill="url(#screen)"/>'
             f'<circle cx="62" cy="40" r="22" fill="url(#sun)"/>'
             f'<path d="M0,44 L10,36 L19,41 L30,30 L41,39 L52,33 L60,38 L71,28 L82,37 L92,32 L100,36 L100,57.6 L0,57.6Z" fill="#3a2550" opacity="0.95"/>'
             f'<path d="M0,49 L12,43 L25,47 L38,41 L50,46 L63,42 L76,48 L88,43 L100,47 L100,57.6 L0,57.6Z" fill="#24183a"/>'
             f'<path d="M0,53 L20,50 L40,53 L58,50 L80,54 L100,51 L100,57.6 L0,57.6Z" fill="#150f24"/>'
             f'</svg>')
    return "\n".join(o)

def _line(a, b, col, w=1.2, extra=""):
    return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{col}" stroke-width="{w}" {extra}/>'


def xbox360(x, y, z):
    """Original Xbox 360 lying flat: 30.9 W x 8.3 H x 25.8 D. White body, grey vent panel on top,
    concave front with disc tray slot, ring-of-light power button at the right."""
    o = [box(x, y, z, 30.9, 8.3, 25.8, "#ecebe6", "#f5f4f0", "#d6d4ce")]
    # grey vent panel on the top surface (the side intake when stood upright)
    o.append(poly([P(x + 2.5, y + 8.31, z + 3), P(x + 28.4, y + 8.31, z + 3), P(x + 28.4, y + 8.31, z + 23), P(x + 2.5, y + 8.31, z + 23)], "#b9b8b3"))
    for i in range(9):
        zz = z + 4.5 + i * 2.0
        o.append(_line(P(x + 3.5, y + 8.32, zz), P(x + 27.4, y + 8.32, zz), "#9c9b96", 0.8))
    # concave front: slightly darker inset band, disc tray slot, ring of light, eject, USB flap
    o.append(quad_front(x + 1.0, y + 0.9, z - 0.01, 28.9, 6.5, "#e3e2dc"))
    o.append(quad_front(x + 2.0, y + 5.2, z - 0.02, 20.5, 0.45, "#7d7c78"))
    c = P(x + 26.6, y + 4.6, z - 0.03)
    r = 1.6 * S * D / (D + z)
    o.append(f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{r:.1f}" fill="#f7f7f4" stroke="#b5b4af" stroke-width="1"/>')
    o.append(f'<path d="M{c[0]:.1f},{c[1]-r*0.8:.1f} A{r*0.8:.1f},{r*0.8:.1f} 0 0 1 {c[0]+r*0.8:.1f},{c[1]:.1f}" fill="none" stroke="#61d04f" stroke-width="2"/>')
    o.append(quad_front(x + 23.0, y + 4.1, z - 0.03, 1.4, 0.9, "#cfcec9"))
    o.append(quad_front(x + 22.2, y + 1.4, z - 0.03, 6.0, 1.6, "#dad9d4"))
    return "\n".join(o)


def xboxone(x, y, z):
    """Original Xbox One: 33.3 W x 7.9 H x 27.4 D. Black; glossy left of the top, vented right;
    slot-loading drive at the front left, white Xbox button at the front right."""
    o = [box(x, y, z, 33.3, 7.9, 27.4, "#161718", "#1b1c1e", "#0e0f10")]
    o.append(poly([P(x + 0.3, y + 7.91, z + 0.3), P(x + 19, y + 7.91, z + 0.3), P(x + 19, y + 7.91, z + 27), P(x + 0.3, y + 7.91, z + 27)], "#2e3033"))
    for i in range(12):
        xx = x + 20 + i * 1.1
        o.append(_line(P(xx, y + 7.92, z + 1.5), P(xx, y + 7.92, z + 26), "#0b0b0c", 0.9))
    o.append(quad_front(x + 2.5, y + 4.8, z - 0.01, 14.5, 0.35, "#050505"))
    c = P(x + 31.0, y + 4.3, z - 0.02)
    o.append(f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="3.4" fill="#f4f4f4" opacity="0.92"/>')
    o.append(quad_front(x + 26.0, y + 1.6, z - 0.02, 1.4, 0.5, "#3a3b3e"))
    return "\n".join(o)


def ps1(x, y, z):
    """Original PlayStation: 27 W x 6 H x 18.8 D. Grey; round disc lid on the top left with three
    round buttons beside it; two controller ports and two memory card slots on the front."""
    o = [box(x, y, z, 27, 6.0, 18.8, "#c3c1bc", "#d2d0cb", "#a9a7a1")]
    # lid (raised round area) and its ring
    o.append(ellipse_flat(x + 10, y + 6.01, z + 10.2, 6.6, 6.6, "#b9b7b2"))
    o.append(ellipse_flat(x + 10, y + 6.02, z + 10.2, 5.6, 5.6, "#c8c6c1"))
    o.append(ellipse_flat(x + 10, y + 6.03, z + 10.2, 1.0, 1.0, "#8f8d88"))
    for (bx_, bz_) in [(x + 21.5, z + 5.0), (x + 21.5, z + 9.5), (x + 21.5, z + 14.0)]:
        o.append(ellipse_flat(bx_, y + 6.03, bz_, 1.1, 1.1, "#9e9c97"))
    # front: memory card slots above, controller ports below
    for xx in (x + 3.0, x + 9.5):
        o.append(quad_front(xx, y + 3.9, z - 0.01, 4.6, 0.45, "#4a4945"))
        o.append(quad_front(xx + 0.4, y + 1.2, z - 0.01, 3.8, 1.6, "#3a3936"))
    o.append(quad_front(x + 17.0, y + 0.6, z - 0.01, 9.5, 0.25, "#a9a7a1"))
    return "\n".join(o)


def ps2(x, y, z):
    """Original ('fat') PS2 lying flat: 30.2 W x 7.8 H x 18.3 D. Black; disc tray across the upper
    front, ports at the lower left, reset/eject at the right, blue PS logo strip."""
    o = [box(x, y, z, 30.2, 7.8, 18.3, "#141416", "#1d1e21", "#0c0c0d")]
    for i in range(10):     # ribbed top
        zz = z + 1.5 + i * 1.6
        o.append(_line(P(x + 1.0, y + 7.81, zz), P(x + 29.2, y + 7.81, zz), "#0a0a0b", 0.8))
    o.append(quad_front(x + 0.6, y + 4.0, z - 0.01, 29.0, 3.2, "#1c1d20"))     # tray face
    o.append(quad_front(x + 0.6, y + 3.9, z - 0.02, 29.0, 0.15, "#000"))
    o.append(quad_front(x + 2.0, y + 4.6, z - 0.02, 0.8, 2.0, "#2c4bb0"))     # vertical logo strip
    for xx in (x + 4.0, x + 8.4):
        o.append(quad_front(xx, y + 2.3, z - 0.02, 3.4, 0.35, "#050505"))   # memory card slots
        o.append(quad_front(xx + 0.2, y + 0.6, z - 0.02, 3.0, 1.2, "#050505"))  # controller ports
    o.append(quad_front(x + 25.0, y + 1.4, z - 0.02, 1.5, 0.9, "#2e7d3c"))   # reset (green)
    o.append(quad_front(x + 27.0, y + 1.4, z - 0.02, 1.5, 0.9, "#2b55c8"))   # eject (blue)
    return "\n".join(o)


def ps3(x, y, z):
    """Original PS3: 32.5 W x 9.8 H x 27.4 D. Glossy black with a silver band and slot drive."""
    o = [box(x, y, z, 32.5, 9.8, 27.4, "#121214", "#2f3035", "#0a0a0b")]
    o.append(poly([P(x + 1, y + 9.81, z + 1), P(x + 31.5, y + 9.81, z + 1), P(x + 31.5, y + 9.81, z + 11), P(x + 1, y + 9.81, z + 11)], "#3a3b41", 'opacity="0.6"'))
    o.append(quad_front(x + 0.4, y + 3.0, z - 0.01, 31.7, 0.35, "#8e9096"))     # silver band
    o.append(quad_front(x + 4.0, y + 6.4, z - 0.02, 16.0, 0.3, "#000"))       # disc slot
    o.append(quad_front(x + 27.0, y + 6.2, z - 0.02, 1.0, 0.5, "#3c3d42"))
    o.append(quad_front(x + 29.0, y + 6.2, z - 0.02, 1.0, 0.5, "#3c3d42"))
    return "\n".join(o)


def singles(xa, xb, y0):
    """7-inch singles (18.3 cm sleeves), spines out, two rows; the back row on a 3 cm step."""
    o = []
    rnd = random.Random(13)
    cols = ["#e9e3d3", "#2f3e5c", "#c8452f", "#f0c24b", "#1f1f1f", "#6a8f5a", "#3a6ea5", "#b3307a",
            "#d27a2e", "#14806d", "#f2f0ea", "#8a5a3c"]
    def row(yb, z):
        x = xa + 0.5
        while x < xb - 0.8:
            t = rnd.choice([0.22, 0.25, 0.25, 0.3, 0.35])
            c = rnd.choice(cols)
            o.append(box(x, yb, z, t, 18.3, 18.3, c, None, c, extra='stroke="#00000033" stroke-width="0.3"'))
            x += t + 0.01
    row(y0 + 3.0, 20.0)
    o.append(box(xa, y0, 19.5, xb - xa, 3.0, 19.0, "#d8c39f", "#e6d2ae", "#b99e78"))   # step
    row(y0, 1.0)
    return "\n".join(o)



PLY, PLY_T, PLY_S = "#d9c09a", "#e8d3b0", "#b99e78"
SIDE_L, SIDE_R, FLOOR_C = "#d9c29b", "#b89b72", "#cbb085"

def bay(x1, x2, y1, y2, d=40):
    """Open bay interior seen from the front (sides, floor and a dark open back), front at z = 0."""
    b = [quad_front(x1, y1, d, x2 - x1, y2 - y1, "url(#bayBack)"),
         poly([P(x1, y1, 0), P(x1, y1, d), P(x1, y2, d), P(x1, y2, 0)], SIDE_L),
         poly([P(x2, y1, 0), P(x2, y1, d), P(x2, y2, d), P(x2, y2, 0)], SIDE_R),
         poly([P(x1, y1, 0), P(x2, y1, 0), P(x2, y1, d), P(x1, y1, d)], FLOOR_C)]
    return "\n".join(b)


def face_frame(x1, x2, holes, top=73.0):
    """Oak face frame (or painted, slat version) with openings (a, b, bottom); openings run up to 71."""
    outer = [P(x1, 0, 0), P(x2, 0, 0), P(x2, top, 0), P(x1, top, 0)]
    d = "M" + " L".join(f"{p[0]:.1f},{p[1]:.1f}" for p in outer) + " Z"
    for (a, b, yb) in holes:
        h = [P(a, yb, 0), P(b, yb, 0), P(b, top - 2.0, 0), P(a, top - 2.0, 0)]
        d += " M" + " L".join(f"{p[0]:.1f},{p[1]:.1f}" for p in h) + " Z"
    oak = STYLE == "joinery"
    return (f'<path d="{d}" fill="{OAK if oak else G_FRAME}" fill-rule="evenodd" {GH if oak else ""}/>\n'
            f'<path d="{d}" fill="none" stroke="#000" stroke-opacity="0.18" stroke-width="1"/>')


def bays12():
    """Bays 1-2: the v7-v9 BESTÅ contents, unchanged (drawn in frame coordinates: x from bay 1's left side,
    z from the face frame, y from the top of the plinth)."""
    q = []
    for (a, b) in [(1.6, 58.4), (61.6, 118.4)]:
        q.append(bay(a, b, 1.6, 62.4))
        q.append(poly([P(a, 62.4, 2), P(b, 62.4, 2), P(b, 40, 2), P(a, 40, 2)], "url(#warmpool)", 'opacity="0.9"'))
    def shelf(x1, x2, y):
        return box(x1, y, 1.0, x2 - x1, 1.8, 36, "#d8c39f", "#e6d2ae", "#b99e78")
    q.append(shelf(1.6, 58.4, 26.8)); q.append(shelf(1.6, 58.4, 44.6))
    q.append(xbox360(5, 28.6, 6)); q.append(box(38.5, 28.6, 9, 18, 6.2, 10, "#262628", "#333336", "#1a1a1c"))
    q.append(xboxone(5, 46.4, 6)); q.append(box(40.5, 46.4, 9, 16, 5.6, 9, "#262628", "#333336", "#1a1a1c"))
    q.append(shelf(61.6, 118.4, 18.6)); q.append(shelf(61.6, 118.4, 36.9))
    q.append(ps1(63.5, 1.6, 6))
    q.append(box(93.5, 1.6, 8, 20, 4.5, 15, "#2a2b2e", "#3a3b3f", "#1a1b1d")); q.append(box(95, 3.4, 7.99, 1.6, 0.6, 0.1, "#79b8ff"))
    q.append(ps2(63.5, 20.4, 6))
    q.append(box(97, 20.4, 3, 13, 2.4, 7, "#1f1f22", "#303034")); q.append(box(98, 21.2, 2.99, 1, 0.5, 0.1, "#ff5a4a"))
    q.append(ps3(63.5, 38.7, 6))
    q.append(box(99, 38.7, 4, 17.5, 10, 16, "#c9a26a", "#d8b480", "#a98455"))
    for i in range(5):
        q.append(box(99.2, 39.5 + i * 2, 3.99, 17.1, 0.25, 0.1, "#a8834f"))
    if GAME_OPEN == 0:
        q.append(game_drawer(0))
    return "\n".join(q)


def sub_bay():
    """Bay 3: an open 18 mm ply carcass 60 x 40 x 73 from the floor (front at the face frame, z = 0 here).
    Subwoofer on a 5 cm riser on the floor, a shelf above for the controller dock and spares, the 6-way at the
    back, and the hidden slim drawer under the worktop."""
    o = []
    x1, x2 = BAYS[2][0] + 1.8, BAYS[2][1] - 1.8      # 124.8 .. 181.2
    o.append(bay(x1, x2, 1.8, 71.2))
    o.append(poly([P(x1, 71.2, 2), P(x2, 71.2, 2), P(x2, 48, 2), P(x1, 48, 2)], "url(#warmpool)", 'opacity="0.9"'))
    # 6-way surge strip, each socket switched, screwed to the back under the shelf
    o.append(box(x1 + 4, 33.0, 38.5, 34, 4.2, 1.5, WHT, WHT_T, WHT_S))
    for i in range(6):
        o.append(box(x1 + 6 + i * 5.3, 35.4, 38.49, 1.6, 1.2, 0.05, "#ff7a45" if i < 5 else "#9a9a9a"))
    # shelf, top 41.8 (3.8 cm over the sub): Xbox and PlayStation pads on a charging dock, a basket of spare pads and cables
    o.append(box(x1, 40.0, 1.0, x2 - x1, 1.8, 36, OAK, OAK_T, OAK_S))
    o.append(box(x1 + 3, 41.8, 8, 22, 2.6, 9, "#1d1e21", "#2b2c30", "#141416"))
    for i, col in enumerate(("#f2f1ec", "#1b1c1e")):
        cx = x1 + 8 + i * 11
        o.append(box(cx - 4.5, 44.4, 11, 9, 6.2, 4.5, col, side="#00000055"))
        p = P(cx, 48.5, 10.99)
        o.append(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="2.6" fill="{"#3fae54" if i == 0 else "#2c4bb0"}"/>')
    o.append(box(x1 + 29, 41.8, 6, 24, 11, 18, "#c9a26a", "#d8b480", "#a98455"))
    for i in range(4):
        o.append(box(x1 + 29.2, 42.6 + i * 2.4, 5.99, 23.6, 0.25, 0.1, "#a8834f"))
    # riser and subwoofer (Hisense AX5100G sub 21.4 W x 29.4 H x 30.4 D), facing the sofa
    sx = (x1 + x2) / 2 - 10.7
    o.append(box(sx - 4.3, 1.8, 3, 30, 5, 34, "#3c3c3e", "#4a4a4d", "#2d2d2f"))
    o.append(box(sx, 6.8, 4, 21.4, 29.4, 30.4, "#1a1a1b", "#2b2b2d", "#111112"))
    c = P(sx + 10.7, 21.5, 3.99)
    o.append(f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{7.6 * S * D / (D + BASE_F + 4):.1f}" fill="#0c0c0c" stroke="#3a3a3c" stroke-width="2"/>')
    o.append(f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{2.5 * S * D / (D + BASE_F + 4):.1f}" fill="#2a2a2c"/>')
    return "\n".join(o)


def unit():
    """The base in the alcove, v10: 3 + 60 + 60 + 60 + 3 = 186. Bays 1-2 are BESTÅ 60x40x64 frames on a 9 cm
    plinth, bay 3 an open ply carcass for the sub. 4 cm cable channel behind, 2 cm oak face frame in front,
    so the front sits 8 cm proud of the chimney breast. Solid oak worktop 186 x 42 x 3, top at 76."""
    o = []
    o.append(poly([P(-1, 0.05, BASE_F), P(ALC_W, 0.05, BASE_F), P(ALC_W, 0.05, BASE_F - 10), P(-1, 0.05, BASE_F - 10)],
                  "#000", 'opacity="0.18" filter="url(#soft)"'))
    o.append(at3(BAYS[0][0], RAISE, BASE_F, bays12))
    o.append(at3(0, 0, BASE_F, sub_bay))
    holes = [(5.6, 60.4, 11.6), (65.6, 120.4, 11.6), (125.6, 180.4, 2.6)]
    o.append(at3(0, 0, BASE_F, face_frame, 0, ALC_W, holes))
    a_, b_ = P(0, 9, BASE_F - 0.02), P(123, 9, BASE_F - 0.02)
    o.append(f'<line x1="{a_[0]:.1f}" y1="{a_[1]:.1f}" x2="{b_[0]:.1f}" y2="{b_[1]:.1f}" stroke="#000" stroke-opacity="0.2" stroke-width="1"/>')
    o.append(at3(BAYS[0][0], RAISE, BASE_F, lambda: game_drawer(GAME_OPEN) if GAME_OPEN > 0 else game_drawer(0, "lip")))
    # hidden slim drawer under the worktop in bay 3: oak front 54.8 x 5.4 with a finger pull underneath
    o.append(box(125.6, 65.6, BASE_F - 0.6, 54.8, 5.4, 2.0, OAK, OAK_T, OAK_S))
    a_, b_ = P(146, 65.6, BASE_F - 0.61), P(160, 65.6, BASE_F - 0.61)
    o.append(f'<line x1="{a_[0]:.1f}" y1="{a_[1]+1:.1f}" x2="{b_[0]:.1f}" y2="{b_[1]+1:.1f}" stroke="#6b4527" stroke-width="2.5"/>')
    # solid oak worktop 186 x 42 x 3 (front at the face frame, 4 cm slot behind for cables)
    o.append(box(0, WT - WT_TH, BASE_F, ALC_W, WT_TH, CARC_B - BASE_F, OAK, OAK_T, OAK_D, extra=GH))
    if STYLE == "joinery":
        a_, b_ = P(0, WT - 0.4, BASE_F - 0.01), P(ALC_W, WT - 0.4, BASE_F - 0.01)
        o.append(f'<line x1="{a_[0]:.1f}" y1="{a_[1]:.1f}" x2="{b_[0]:.1f}" y2="{b_[1]:.1f}" stroke="#ecc28c" stroke-width="1.4"/>')
    return "\n".join(o)

REC_OPEN = 0.0      # lower record drawer
REC_OPEN_UP = 0.0   # upper record drawer

def record_tier(yb, open_cm, part="all"):
    """v8 face-out record tray in the bay-3 carcass. Box 53.9 x 40 on 400 mm runners screwed to the 18 mm ply.
    Thinner build: 9 mm sides, 12 mm base, 6 mm oak divider, 5 cm oak lip. LP trough 32.6 wide on the left,
    7-inch singles face-out in an 18.9 cm trough on the right, both leaning back 10 degrees."""
    o = []
    oz = -open_cm
    LIP_H = 5.0
    if part == "lip":
        o.append(box(121.6, yb, oz - 0.6, 56.8, LIP_H, 1.5, OAK, OAK_T, OAK_S, extra=GH))
        a, b = P(143, yb + LIP_H, oz - 0.61), P(157, yb + LIP_H, oz - 0.61)
        o.append(f'<path d="M{a[0]:.1f},{a[1]:.1f} Q{(a[0]+b[0])/2:.1f},{a[1]+7:.1f} {b[0]:.1f},{b[1]:.1f}Z" fill="#7a5130"/>')
        return "\n".join(o)
    bx1, bx2 = 123.07, 176.93
    ix1, ix2 = bx1 + 0.9, bx2 - 0.9
    yt = yb + 1.2
    PLY, PLY_T, PLY_S = "#d9c09a", "#e8d3b0", "#b99e78"
    if open_cm > 0:
        o.append(poly([P(bx1, 0.05, oz), P(bx2 + 3, 0.05, oz), P(bx2 + 3, 0.05, oz + 34), P(bx1, 0.05, oz + 34)], "#000", 'opacity="0.2" filter="url(#soft)"'))
    o.append(box(bx1, yb, oz + 39.1, bx2 - bx1, 12, 0.9, PLY, PLY_T, PLY_S))            # back
    o.append(box(bx1, yb, oz, 0.9, 12, 40, PLY, PLY_T, "#ead7b6"))                      # left side
    o.append(box(bx1, yb, oz, bx2 - bx1, 1.2, 40, "#cdb38a", "#5a5148"))               # base, felt top
    lean = math.radians(10)
    dx = ix1 + 32.6                                                                     # divider
    # singles trough: 7-inch sleeves face-out, leaning back
    sh, sdz = 18.3 * math.cos(lean), 18.3 * math.sin(lean)
    s1, s2 = dx + 0.6 + 0.3, dx + 0.6 + 0.3 + 18.3
    scols = ["#1f1f1f", "#e9e3d3", "#c8452f", "#3a6ea5", "#f0c24b", "#6a8f5a", "#b3307a", "#2f3e5c", "#d27a2e", "#efe6d2", "#14806d", "#2c2c2c"]
    for i, col in enumerate(scols):
        zb = oz + 33.0 - i * 2.5
        q = [P(s1, yt, zb), P(s2, yt, zb), P(s2, yt + sh, zb + sdz), P(s1, yt + sh, zb + sdz)]
        o.append(poly(q, col, 'stroke="#000" stroke-opacity="0.25" stroke-width="0.5"'))
    zf = oz + 2.6
    sq = [P(s1, yt, zf), P(s2, yt, zf), P(s2, yt + sh, zf + sdz), P(s1, yt + sh, zf + sdz)]
    def Lq(q, u, v):
        bl, br, tr, tl = q
        bx_ = bl[0] + (br[0] - bl[0]) * u; by_ = bl[1] + (br[1] - bl[1]) * u
        tx_ = tl[0] + (tr[0] - tl[0]) * u; ty_ = tl[1] + (tr[1] - tl[1]) * u
        return (bx_ + (tx_ - bx_) * v, by_ + (ty_ - by_) * v)
    sart = ([("#2f3e5c", 0, 1, 0, 1), ("#f0c24b", 0.1, 0.9, 0.1, 0.9), ("#c8452f", 0.32, 0.68, 0.32, 0.68)] if yb < 10 else
            [("#efe6d2", 0, 1, 0, 1), ("#14806d", 0, 1, 0, 0.35), ("#1f1f1f", 0.2, 0.8, 0.5, 0.85)])
    for (c, u1, u2, v1, v2) in sart:
        o.append(poly([Lq(sq, u1, v1), Lq(sq, u2, v1), Lq(sq, u2, v2), Lq(sq, u1, v2)], c))
    o.append(poly(sq, "none", 'stroke="#000" stroke-opacity="0.3" stroke-width="0.7"'))
    o.append(box(dx, yt, oz + 0.9, 0.6, 10, 38.2, OAK, OAK_T, OAK_S))                     # oak divider
    # LP trough
    hgt, dzl = 31.4 * math.cos(lean), 31.4 * math.sin(lean)
    x1, x2 = ix1 + 0.6, ix1 + 0.6 + 31.4
    cols = ["#2c2c2c", "#e9e3d3", "#3a6ea5", "#c8452f", "#f0c24b", "#1f1f1f", "#6a8f5a", "#b3307a", "#efe6d2", "#2f3e5c", "#d27a2e"]
    for i, col in enumerate(cols):
        zb = oz + 31.0 - i * 2.6
        q = [P(x1, yt, zb), P(x2, yt, zb), P(x2, yt + hgt, zb + dzl), P(x1, yt + hgt, zb + dzl)]
        o.append(poly(q, col, 'stroke="#000" stroke-opacity="0.25" stroke-width="0.6"'))
    zf = oz + 2.6
    fq = [P(x1, yt, zf), P(x2, yt, zf), P(x2, yt + hgt, zf + dzl), P(x1, yt + hgt, zf + dzl)]
    art = ([("#f1e7d0", 0, 1, 0, 1), ("#e8603c", 0.08, 0.92, 0.55, 0.92), ("#24427a", 0.08, 0.58, 0.12, 0.5), ("#f1b83f", 0.62, 0.92, 0.12, 0.5)]
           if yb < 10 else
           [("#1f3a52", 0, 1, 0, 1), ("#e9b44c", 0, 1, 0, 0.42), ("#d8613e", 0.12, 0.88, 0.5, 0.9), ("#f5e6c6", 0.35, 0.65, 0.58, 0.82)])
    for (c, u1, u2, v1, v2) in art:
        o.append(poly([Lq(fq, u1, v1), Lq(fq, u2, v1), Lq(fq, u2, v2), Lq(fq, u1, v2)], c))
    o.append(poly(fq, "none", 'stroke="#000" stroke-opacity="0.3" stroke-width="0.8"'))
    if yb < 10:
        cc = Lq(fq, 0.5, 0.71)
        o.append(f'<circle cx="{cc[0]:.1f}" cy="{cc[1]:.1f}" r="10" fill="#1b1b1b"/>')
        o.append(f'<circle cx="{cc[0]:.1f}" cy="{cc[1]:.1f}" r="3.6" fill="#e8603c"/>')
    o.append(box(ix2, yb, oz, 0.9, 12, 40, PLY, PLY_T, PLY_S))                          # right side
    o.append(box(bx1, yb, oz, bx2 - bx1, 4.5, 0.9, PLY, PLY_T, PLY_S))                  # low front panel
    if open_cm > 0:
        a, b = P(bx2 + 0.05, yb + 6, oz + 1), P(bx2 + 0.05, yb + 6, oz + 38)
        o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#9aa0a6" stroke-width="5"/>')
        o.append(record_tier(yb, open_cm, "lip"))
    return "\n".join(o)


GAME_OPEN = 0.0

def game_drawer(open_cm, part="all"):
    """Bay 1 roll-out game drawer: two front-facing display bins + centre tray, spine-up rows behind.
    Box 54.3 wide x 35 deep (350 mm runners on the BESTÅ sides), base at 2.6 cm."""
    o = []
    oz = -open_cm
    bx1, bx2 = 2.87, 57.13
    if part == "lip":
        o.append(box(1.6, 2.6, oz - 0.6, 56.8, 6.5, 2.0, OAK, OAK_T, OAK_S))
        a, b = P(24, 2.6 + 6.5, oz - 0.61), P(34, 2.6 + 6.5, oz - 0.61)
        o.append(f'<path d="M{a[0]:.1f},{a[1]:.1f} Q{(a[0]+b[0])/2:.1f},{a[1]+9:.1f} {b[0]:.1f},{b[1]:.1f}Z" fill="#7a5130"/>')
        return "\n".join(o)
    ix1, ix2 = bx1 + 1.2, bx2 - 1.2
    yb, yt = 2.6, 3.5          # box base bottom / top
    side_h = 15.5
    PLY, PLY_T, PLY_S = "#d9c09a", "#e8d3b0", "#b99e78"
    if open_cm > 0:
        o.append(poly([P(bx1, 0.05, oz), P(bx2 + 3, 0.05, oz), P(bx2 + 3, 0.05, oz + 30), P(bx1, 0.05, oz + 30)], "#000", 'opacity="0.22" filter="url(#soft)"'))
    # back panel, left side (inner face shows), base
    o.append(box(bx1, yb, oz + 33.8, bx2 - bx1, side_h, 1.2, PLY, PLY_T, PLY_S))
    o.append(box(bx1, yb, oz, 1.2, side_h, 35, PLY, PLY_T, "#ead7b6"))
    o.append(box(ix1, yb, oz, ix2 - ix1, 0.9, 33.8, "#cdb38a", "#5a5148"))   # base with dark felt top
    # ---- back zone: spine-up cases, lengthwise front-to-back, titles on top
    z0 = oz + 14.9
    x = ix1 + 0.3
    groups = [("ps2", 15, 1.4), ("x360", 12, 1.4), ("follower", 1, 2.0), ("one", 9, 1.2)]
    rnd = random.Random(21)
    for kind, n, t in groups:
        for i in range(n):
            if kind == "follower":
                o.append(box(x, yt, z0, t, 12, 19, "#c79a63", "#d9ad75", "#a87d4a"))
                x += t + 0.1
                continue
            if kind == "ps2":
                front, top = "#1d2f6b", rnd.choice(["#0f0f12", "#e9e6df", "#121722"])
                band = "#2c4bb0"
            elif kind == "x360":
                front, top, band = "#2c8f3e", "#f2f1ec", "#5ab845"
            else:
                front, top, band = "#1f7a37", rnd.choice(["#f2f1ec", "#1c1c1c"]), "#3fae54"
            h = 13.5
            o.append(box(x, yt, z0, t * 0.97, h, 19 if kind != "one" else 17, front, top, front))
            # title strip + console band on the spine (seen from above)
            ln = 19 if kind != "one" else 17
            o.append(poly([P(x + 0.35, yt + h + 0.01, z0 + 2.5), P(x + t * 0.97 - 0.35, yt + h + 0.01, z0 + 2.5),
                           P(x + t * 0.97 - 0.35, yt + h + 0.01, z0 + ln - 5.5), P(x + 0.35, yt + h + 0.01, z0 + ln - 5.5)],
                          "#8d8a84" if top.startswith("#f") or top.startswith("#e") else "#d8d4cc", 'opacity="0.75"'))
            o.append(poly([P(x, yt + h + 0.02, z0 + ln - 3.2), P(x + t * 0.97, yt + h + 0.02, z0 + ln - 3.2),
                           P(x + t * 0.97, yt + h + 0.02, z0 + ln), P(x, yt + h + 0.02, z0 + ln)], band))
            x += t
    # divider between back zone and front bins
    o.append(box(ix1, yt, oz + 14.2, ix2 - ix1, 9, 0.6, PLY, PLY_T, PLY_S))
    # ---- front zone: two display bins (16 wide) + centre tray
    lb, rb = (ix1, ix1 + 16.0), (ix2 - 16.0, ix2)
    o.append(box(lb[1], yt, oz + 1.2, 0.6, 9, 13, PLY, PLY_T, PLY_S))
    o.append(box(rb[0] - 0.6, yt, oz + 1.2, 0.6, 9, 13, PLY, PLY_T, PLY_S))
    # centre tray: memory cards, a pad, a few manuals
    o.append(box(lb[1] + 2, yt, oz + 3, 6, 1.5, 5, "#2b2b2e", "#3a3a3e"))
    o.append(box(lb[1] + 9.5, yt, oz + 3.5, 6.5, 1.2, 4, "#e8e5de", "#f4f2ec"))
    o.append(box(lb[1] + 2, yt, oz + 9, 15, 4.5, 4, "#1b1c1e", "#2a2b2e", "#111"))
    lean = math.radians(13)
    hgt, dzl = 19 * math.cos(lean), 19 * math.sin(lean)
    def bin_cases(xa, xb, palette, art):
        cx = (xa + xb) / 2
        x1, x2 = cx - 6.75, cx + 6.75
        n = 6
        for i in range(n - 1, -1, -1):
            zb = oz + 2.4 + i * 1.45
            c = palette[i % len(palette)]
            q = [P(x1, yt, zb), P(x2, yt, zb), P(x2, yt + hgt, zb + dzl), P(x1, yt + hgt, zb + dzl)]
            o.append(poly(q, c, 'stroke="#000" stroke-opacity="0.3" stroke-width="0.6"'))
            if i == 0:
                def L(u, v):
                    bl, br, tr, tl = q
                    bx_ = bl[0] + (br[0] - bl[0]) * u; by_ = bl[1] + (br[1] - bl[1]) * u
                    tx_ = tl[0] + (tr[0] - tl[0]) * u; ty_ = tl[1] + (tr[1] - tl[1]) * u
                    return (bx_ + (tx_ - bx_) * v, by_ + (ty_ - by_) * v)
                for (u1, u2, v1, v2, col) in art:
                    o.append(poly([L(u1, v1), L(u2, v1), L(u2, v2), L(u1, v2)], col))
    xbox_art = [(0, 1, 0.86, 1, "#3fae54"), (0.08, 0.92, 0.1, 0.8, "#1a2a3a"), (0.2, 0.8, 0.45, 0.72, "#e0b43a"),
                (0.3, 0.7, 0.18, 0.4, "#c84b34")]
    ps2_art = [(0, 1, 0.88, 1, "#0f0f12"), (0.06, 0.94, 0.1, 0.84, "#2a5aa6"), (0.15, 0.85, 0.5, 0.78, "#f1e7d0"),
               (0.25, 0.75, 0.16, 0.44, "#e8603c")]
    bin_cases(*lb, ["#2c8f3e", "#1f7a37", "#2c8f3e"], xbox_art)
    bin_cases(*rb, ["#1d2f6b", "#13214f"], ps2_art)
    # right side (outer face + runner)
    o.append(box(ix2, yb, oz, 1.2, side_h, 35, PLY, PLY_T, PLY_S))
    if open_cm > 0:
        a, b = P(bx2 + 0.05, 9.5, oz + 1), P(bx2 + 0.05, 9.5, oz + 34)
        o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#9aa0a6" stroke-width="5"/>')
    # oak front lip with finger pull (overlay front)
    o.append(box(1.6, yb, oz - 0.6, 56.8, 6.5, 2.0, OAK, OAK_T, OAK_S))
    a, b = P(24, yb + 6.5, oz - 0.61), P(34, yb + 6.5, oz - 0.61)
    o.append(f'<path d="M{a[0]:.1f},{a[1]:.1f} Q{(a[0]+b[0])/2:.1f},{a[1]+9:.1f} {b[0]:.1f},{b[1]:.1f}Z" fill="#7a5130"/>')
    return "\n".join(o)



def worktop_items():
    """On the worktop: Series X on its fan stand in the left zone, the soundbar centred at the front edge,
    and a 'now playing' game on a small oak easel in the right zone."""
    o = []
    # Series X fan stand (20.5 square reserved, about 6.5 tall), console 15.1 x 15.1 x 30.1: 2.4 cm clear each side
    sx = (UPL[0] - 20.5) / 2
    o.append(box(sx, WT, 10, 20.5, 6.5, 20.5, "#1c1d1f", "#2a2b2d", "#141516"))
    o.append(poly([P(sx, WT + 6.5, 10), P(sx + 20.5, WT + 6.5, 10), P(sx + 20.5, WT, 10), P(sx, WT, 10)], "url(#seriesGlow)", 'opacity="0.9"'))
    o.append(box(sx + 0.2, WT + 0.05, 9.9, 20.1, 0.9, 0.1, "#3dff8a", extra='opacity="0.85"'))
    cx = sx + 10.25
    o.append(box(cx - 7.55, WT + 6.5, 12.7, 15.1, 30.1, 15.1, "#151617", "#1f2a22", "#0d0e0f"))
    o.append(ellipse_flat(cx, WT + 36.65, 20.25, 6.2, 6.2, "#0b2a17"))
    o.append(ellipse_flat(cx, WT + 36.7, 20.25, 4.6, 4.6, "#2fbf62", 'opacity="0.55"'))
    p = P(cx - 5.8, WT + 34.2, 12.69)
    o.append(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="2.0" fill="#f1f1f1"/>')
    # soundbar at the front edge, Hisense AX5100G 92 x 6 x 9
    o.append(box(TV_CX - 46, WT, BASE_F + 1, 92, 6, 9, "#1b1c1e", "#2a2b2d", "#121314"))
    for i in range(40):
        o.append(box(TV_CX - 44.5 + i * 2.25, WT + 0.8, BASE_F + 0.99, 0.9, 4.4, 0.05, "#26272a"))
    # right zone: an oak easel with this month's game, face-out
    ex = UPR[1] + (ALC_W - UPR[1]) / 2
    o.append(box(ex - 8.5, WT, 14, 17, 1.2, 9, OAK, OAK_T, OAK_S))
    lean = math.radians(14)
    hh, dz = 19 * math.cos(lean), 19 * math.sin(lean)
    q = [P(ex - 6.75, WT + 1.2, 16), P(ex + 6.75, WT + 1.2, 16), P(ex + 6.75, WT + 1.2 + hh, 16 + dz), P(ex - 6.75, WT + 1.2 + hh, 16 + dz)]
    o.append(poly(q, "#2c8f3e", 'stroke="#000" stroke-opacity="0.3" stroke-width="0.8"'))
    def L(u, v):
        bl, br, tr, tl = q
        bx_ = bl[0] + (br[0] - bl[0]) * u; by_ = bl[1] + (br[1] - bl[1]) * u
        tx_ = tl[0] + (tr[0] - tl[0]) * u; ty_ = tl[1] + (tr[1] - tl[1]) * u
        return (bx_ + (tx_ - bx_) * v, by_ + (ty_ - by_) * v)
    for (u1, u2, v1, v2, col) in [(0.08, 0.92, 0.1, 0.82, "#1a2a3a"), (0.2, 0.8, 0.45, 0.72, "#e0b43a"), (0.3, 0.7, 0.18, 0.4, "#c84b34"), (0, 1, 0.86, 1, "#3fae54")]:
        o.append(poly([L(u1, v1), L(u2, v1), L(u2, v2), L(u1, v2)], col))
    o.append(box(ex - 8.5, WT + 1.2, 14.6, 17, 2.2, 1.2, OAK, OAK_T, OAK_S))
    return "\n".join(o)


def lp_art(q, art, ring=False):
    """Fill a projected quad (bl, br, tr, tl) with blocks of colour: original sleeve designs."""
    o = []
    def L(u, v):
        bl, br, tr, tl = q
        bx_ = bl[0] + (br[0] - bl[0]) * u; by_ = bl[1] + (br[1] - bl[1]) * u
        tx_ = tl[0] + (tr[0] - tl[0]) * u; ty_ = tl[1] + (tr[1] - tl[1]) * u
        return (bx_ + (tx_ - bx_) * v, by_ + (ty_ - by_) * v)
    for (c, u1, u2, v1, v2) in art:
        o.append(poly([L(u1, v1), L(u2, v1), L(u2, v2), L(u1, v2)], c))
    o.append(poly(q, "none", 'stroke="#000" stroke-opacity="0.3" stroke-width="0.8"'))
    return "\n".join(o)


def browser(bx0, y0, zf, bw=44.0, n=11):
    """Oak LP browser, 44 x 24: about 50 LPs face-out leaning back 10 degrees, a low front rail and an end."""
    o = []
    rx0 = bx0 + (bw - 31.4) / 2
    o.append(box(bx0, y0, zf + 0.8, bw, 0.8, 24, "#c79a63", "#d9ad75", "#a87d4a"))
    lean = math.radians(10); hgt = 31.4 * math.cos(lean); dz = 31.4 * math.sin(lean)
    cols = ["#e9e3d3", "#2f3e5c", "#c8452f", "#f0c24b", "#1f1f1f", "#6a8f5a", "#3a6ea5", "#b3307a", "#efe6d2", "#2c2c2c", "#d24a3a"]
    for i, col in enumerate(cols[:n]):
        zz = zf + 19.8 - i * 1.6
        q = [P(rx0, y0 + 0.8, zz - dz), P(rx0 + 31.4, y0 + 0.8, zz - dz), P(rx0 + 31.4, y0 + 0.8 + hgt, zz), P(rx0, y0 + 0.8 + hgt, zz)]
        o.append(poly(q, col, 'stroke="#000" stroke-opacity="0.25" stroke-width="0.6"'))
    z1 = zf + 3.4
    fq = [P(rx0, y0 + 0.8, z1 - dz), P(rx0 + 31.4, y0 + 0.8, z1 - dz), P(rx0 + 31.4, y0 + 0.8 + hgt, z1), P(rx0, y0 + 0.8 + hgt, z1)]
    o.append(poly(fq, "#1f3a52"))
    o.append(lp_art(fq, [("#e9b44c", 0.0, 1.0, 0.0, 0.42), ("#d8613e", 0.12, 0.88, 0.5, 0.9), ("#f5e6c6", 0.35, 0.65, 0.58, 0.82)]))
    o.append(box(bx0, y0, zf, bw, 4.0, 1.2, OAK, OAK_T, OAK_S))           # low front rail
    o.append(box(bx0, y0, zf + 0.8, 1.2, 9, 24, OAK, OAK_T, OAK_S))       # end
    return "\n".join(o)


def deck(x0, y0, z0, w=45.0, d=35.0):
    """Turntable, allowing for a deck as big as the Audio-Technica AT-LP120X (45.2 x 35.2 x 14.2), lid closed."""
    o = []
    kx = w / 42.0
    X = lambda u: x0 + u * kx          # positions from the v9 drawing (42 wide), stretched to w
    for fx in (2, 37):
        o.append(box(X(fx), y0, z0 + 2, 3, 1.2, 3, "#3a3a3a"))
    o.append(box(x0, y0 + 1.2, z0, w, 9.5, d, "#1c1c1e", "#2c2c2f", "#121213"))
    pc = (X(16), z0 + 17)
    o.append(ellipse_flat(pc[0], y0 + 10.8, pc[1], 15, 15, "#3a3a3d"))
    o.append(ellipse_flat(pc[0], y0 + 11.4, pc[1], 15, 15, "#0b0b0c"))
    o.append(ellipse_flat(pc[0], y0 + 11.5, pc[1], 4.5, 4.5, "#d4553f"))
    a, b = P(X(36), y0 + 12.5, z0 + 23), P(X(26), y0 + 12.5, z0 + 6)
    o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#cfcfd2" stroke-width="2.5"/>')
    o.append(box(X(34.5), y0 + 10.7, z0 + 20, 4, 2.5, 4, "#9a9aa0"))
    o.append(box(x0, y0 + 10.7, z0, w, 6, d, "url(#glass)", "url(#glass)", "url(#glass)", extra='stroke="#ffffff" stroke-opacity="0.25" stroke-width="1"'))
    return "\n".join(o)


def cabinet_inner():
    """The vinyl cabinet's carcass, drawn with z = 0 at its face frame (world z = -44).
    Bay A (60, 18 mm ply): the two face-out record trays, unchanged from v9, on 400 mm runners.
    Bay B (40): phono preamp, stylus, brush and cleaning kit on a shelf; overflow singles below."""
    o = []
    o.append(poly([P(CAB_X1 - 1, 0.05, 0), P(CAB_X2 + 1, 0.05, 0), P(CAB_X2 + 1, 0.05, -10), P(CAB_X1 - 1, 0.05, -10)],
                  "#000", 'opacity="0.18" filter="url(#soft)"'))
    # outer left side, oak
    o.append(poly([P(CAB_X1, 0, 0), P(CAB_X1, 0, 42), P(CAB_X1, 73, 42), P(CAB_X1, 73, 0)], "#b98450", GV))
    ax1, ax2 = CAB_X1 + 1.8, CAB_X1 + 58.2          # bay A inside 56.4, as the v9 bay 3
    o.append(bay(ax1, ax2, 1.8, 71.2))
    o.append(poly([P(ax1, 71.2, 2), P(ax2, 71.2, 2), P(ax2, 48, 2), P(ax1, 48, 2)], "url(#warmpool)", 'opacity="0.9"'))
    dx = CAB_X1 - 120.0                              # v9's bay 3 carcass started at x = 120
    if REC_OPEN_UP == 0:
        o.append(at3(dx, 0, 0, record_tier, 37.0, 0))
    if REC_OPEN == 0:
        o.append(at3(dx, 0, 0, record_tier, 2.3, 0))
    bx1, bx2 = CAB_X1 + 60.0, CAB_X2 - 1.8           # bay B inside 38.2
    o.append(bay(bx1, bx2, 1.8, 71.2))
    o.append(poly([P(bx1, 71.2, 2), P(bx2, 71.2, 2), P(bx2, 48, 2), P(bx1, 48, 2)], "url(#warmpool)", 'opacity="0.9"'))
    o.append(box(bx1, 37.0, 1.0, bx2 - bx1, 1.8, 38, OAK, OAK_T, OAK_S))     # shelf, top 38.8
    o.append(box(bx1 + 2.5, 38.8, 9, 12, 3.2, 11, "#202022", "#343437"))     # phono preamp
    o.append(box(bx1 + 3.3, 40.0, 8.99, 1.2, 0.8, 0.1, "#ff9a3c"))
    o.append(box(bx1 + 3.0, 42.0, 12, 8, 2.5, 4, "#1d1d1f", "#2e2e31"))      # stylus box
    o.append(box(bx1 + 17, 38.8, 10, 7, 5, 8, "#e7e1d4", "#f2ede3", "#cbc4b6"))   # cleaning kit
    o.append(box(bx1 + 26, 38.8, 8, 10, 14, 18, "#efe9dc", "#f7f3ea", "#d8d0bf"))  # spare inner sleeves
    o.append(singles(bx1 + 0.3, bx2 - 0.3, 1.8))                              # overflow singles
    o.append(face_frame(CAB_X1, CAB_X2, [(CAB_X1 + 2.6, CAB_X1 + 57.4, 2.6), (CAB_X1 + 62.6, CAB_X2 - 2.6, 2.6)]))
    if REC_OPEN_UP > 0:
        o.append(at3(dx, 0, 0, record_tier, 37.0, REC_OPEN_UP))
    else:
        o.append(at3(dx, 0, 0, record_tier, 37.0, 0, "lip"))
    if REC_OPEN > 0:
        o.append(at3(dx, 0, 0, record_tier, 2.3, REC_OPEN))
    else:
        o.append(at3(dx, 0, 0, record_tier, 2.3, 0, "lip"))
    return "\n".join(o)


def vinyl_cabinet():
    """v10: the vinyl corner moves to the chimney breast. A matching oak cabinet 100 wide x 44 deep x 76 high,
    with the turntable and the LP browser on top and LP frames on the breast above (40 cm left clear for the lid)."""
    o = [at3(0, 0, CAB_F, cabinet_inner)]
    o.append(box(CAB_X1, 73, CAB_F - 1, CAB_X2 - CAB_X1, 3, -CAB_F + 1, OAK, OAK_T, OAK_D, extra=GH))
    if STYLE == "joinery":
        a_, b_ = P(CAB_X1, CAB_TOP - 0.4, CAB_F - 1.01), P(CAB_X2, CAB_TOP - 0.4, CAB_F - 1.01)
        o.append(f'<line x1="{a_[0]:.1f}" y1="{a_[1]:.1f}" x2="{b_[0]:.1f}" y2="{b_[1]:.1f}" stroke="#ecc28c" stroke-width="1.4"/>')
    o.append(browser(CAB_X1 + 3, CAB_TOP, CAB_F + 1))
    o.append(deck(CAB_X2 - 47, CAB_TOP, CAB_F + 5))
    return "\n".join(o)


LP_FRAMES = [
    [("#efe6d2", 0, 1, 0, 1), ("#2f3e5c", 0.1, 0.9, 0.55, 0.9), ("#c8452f", 0.3, 0.7, 0.15, 0.45)],
    [("#14806d", 0, 1, 0, 1), ("#f0c24b", 0.2, 0.8, 0.2, 0.8), ("#1f1f1f", 0.42, 0.58, 0.42, 0.58)],
    [("#2c2c2c", 0, 1, 0, 1), ("#e8603c", 0.08, 0.92, 0.1, 0.3), ("#efe6d2", 0.08, 0.92, 0.66, 0.9)],
]

def breast_frames():
    """Three LP frames on the chimney breast above the deck, bottoms at 140 (the lid needs up to about 132)."""
    o = []
    for i, art in enumerate(LP_FRAMES):
        x0 = CAB_X1 + 4 + i * 35.0
        o.append(box(x0, 140, -1.6, 32.5, 32.5, 1.6, "#1d1a17", "#2a2622", "#141210"))
        q = [P(x0 + 0.55, 140.55, -1.61), P(x0 + 31.95, 140.55, -1.61), P(x0 + 31.95, 171.95, -1.61), P(x0 + 0.55, 171.95, -1.61)]
        o.append(lp_art(q, art))
    return "\n".join(o)

def left_wall_items():
    o = []
    def frame(z1, z2, y1, y2, blocks):
        f = [P(0.5, y1, z1), P(0.5, y1, z2), P(0.5, y2, z2), P(0.5, y2, z1)]
        o.append(poly(f, "#141414"))
        m = 1.6
        inner = [P(0.6, y1 + m, z1 - m), P(0.6, y1 + m, z2 + m), P(0.6, y2 - m, z2 + m), P(0.6, y2 - m, z1 - m)]
        o.append(poly(inner, "#efe9dc"))
        m2 = 4
        def q(u1, u2, v1, v2, c):
            za = z1 - m2 + (z2 - z1 + 2 * m2) * u1; zb = z1 - m2 + (z2 - z1 + 2 * m2) * u2
            ya = y1 + m2 + (y2 - y1 - 2 * m2) * v1; yb = y1 + m2 + (y2 - y1 - 2 * m2) * v2
            o.append(poly([P(0.7, ya, za), P(0.7, ya, zb), P(0.7, yb, zb), P(0.7, yb, za)], c))
        for b in blocks:
            q(*b)
    frame(-140, -158, 166, 192, [(0, 0.5, 0, 1, "#1f6f8b"), (0.5, 1, 0, 0.55, "#14806d"), (0.5, 1, 0.55, 1, "#e0b43a")])
    frame(-163, -182, 162, 190, [(0, 1, 0, 0.33, "#c23b2e"), (0, 0.5, 0.33, 0.66, "#e0b43a"), (0.5, 1, 0.33, 0.66, "#2f3e5c"), (0, 1, 0.66, 1, "#d27a2e")])
    frame(-187, -198, 166, 186, [(0, 0.5, 0, 0.5, "#7a3fd1"), (0.5, 1, 0, 0.5, "#e0b43a"), (0, 1, 0.5, 1, "#1f6f8b")])
    zN, zS = -130, -195          # shelf runs along the wall, north (alcove) end to south (sofa) end
    # cable trunking, painted the wall green, from the shelf's back-corner notch down to the skirting
    o.append(poly([P(0.3, 10, -186), P(0.3, 10, -190), P(0.3, 106, -190), P(0.3, 106, -186)], "#3a6d55"))
    o.append(poly([P(1.8, 10, -186), P(1.8, 10, -190), P(1.8, 106, -190), P(1.8, 106, -186)], "#335f4a"))
    # skirting trunking run back towards the alcove (sits on top of the skirting)
    o.append(poly([P(0.3, 10, -190), P(0.3, 13, -190), P(0.3, 13, 0), P(0.3, 10, 0)], "#3a6d55"))
    o.append(poly([P(0.3, 13, -190), P(2.0, 13, -190), P(2.0, 13, 0), P(0.3, 13, 0)], "#447a60"))
    # keyboard tray housing under the shelf (7 cm deep box), tray rolled out 12 cm towards the room
    o.append(box(0, 99.5, zS + 12, 32, 6.5, (zN - zS) - 13, OAK_S, OAK_T, "#8e6038"))
    tray_out = 12
    o.append(box(tray_out, 100.2, zS + 13.5, 30, 0.8, (zN - zS) - 16, "#cdb38a", "#dcc39b", "#a8875a"))
    o.append(box(tray_out + 4, 101.0, zS + 20, 13, 1.8, 44, "#1d1e21", "#2b2c30", "#141416"))  # keyboard
    for i in range(6):
        zz = zS + 22 + i * 7
        a, b = P(tray_out + 5, 102.81, zz), P(tray_out + 16, 102.81, zz)
        o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#3a3b40" stroke-width="1"/>')
    o.append(box(tray_out + 6, 101.0, zS + 15, 6, 2.2, 4, "#1d1e21", "#2f3034"))                 # mouse
    o.append(box(tray_out + 30, 100.2, zS + 13.5, 2.0, 4.6, (zN - zS) - 16, OAK, OAK_T, OAK_S))  # tray front lip
    # the shelf: 65 along the wall x 32 deep, top at 110
    o.append(box(0, 106, zS, 32, 4, zN - zS, OAK, OAK_T, OAK_S, extra=GH))
    # PC case 23 W x 47 H x 45 D: front faces the alcove (north), back ports face the sofa (south),
    # glass panel (the case's left side) faces the room
    cx1, cfront, cback = 4.5, -135, -180
    o.append(box(cx1, 110, cback, 23, 47, cfront - cback, "#121314", "#1d1f21", "#0d0e0f"))
    side = [P(27.5, 111, cback + 1), P(27.5, 111, cfront - 1), P(27.5, 156, cfront - 1), P(27.5, 156, cback + 1)]
    o.append(poly(side, "#0c1714"))
    for (yy, zz) in [(146, -140.5), (133.5, -140.5), (121, -140.5)]:          # front intake fans (glowing)
        pc = P(27.5, yy, zz); k = D / (D + zz)
        o.append(f'<ellipse cx="{pc[0]:.1f}" cy="{pc[1]:.1f}" rx="{4.6 * S * k * 0.42:.1f}" ry="{5.4 * S * k:.1f}" fill="none" stroke="#3fe3b0" stroke-width="3" opacity="0.9"/>')
    pc = P(27.5, 145, -172); k = D / (D - 172)                                # rear exhaust fan
    o.append(f'<ellipse cx="{pc[0]:.1f}" cy="{pc[1]:.1f}" rx="{3.6 * S * k * 0.42:.1f}" ry="{4.2 * S * k:.1f}" fill="none" stroke="#8b7cf0" stroke-width="2.5"/>')
    a, b = P(27.5, 128, -150), P(27.5, 128, -170)                              # GPU
    o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#8b7cf0" stroke-width="3"/>')
    o.append(box(27.4, 111, cback + 1.5, 0.1, 7, 18, "#222326"))              # PSU shroud
    o.append(poly(side, "url(#glass)", 'stroke="#2c3b36" stroke-width="1.5"'))
    # rear cable screen: oak slats 13 cm behind the case, open top so exhaust escapes
    zsc = zS + 0.5
    if STYLE == "joinery":
        # oak frame with woven cane panel: hides the ports, breathes, no slats
        o.append(box(3, 110, zsc, 26, 48, 2.0, OAK, OAK_T, OAK_S))
        q = [P(6, 113, zsc - 0.01), P(26, 113, zsc - 0.01), P(26, 155, zsc - 0.01), P(6, 155, zsc - 0.01)]
        o.append(poly(q, "#d9c08f"))
        for i in range(1, 14):
            u = i / 14
            a = (q[0][0] + (q[1][0] - q[0][0]) * u, q[0][1] + (q[1][1] - q[0][1]) * u)
            b = (q[3][0] + (q[2][0] - q[3][0]) * u, q[3][1] + (q[2][1] - q[3][1]) * u)
            o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#a88a55" stroke-width="0.8"/>')
        for i in range(1, 28):
            v = i / 28
            a = (q[0][0] + (q[3][0] - q[0][0]) * v, q[0][1] + (q[3][1] - q[0][1]) * v)
            b = (q[1][0] + (q[2][0] - q[1][0]) * v, q[1][1] + (q[2][1] - q[1][1]) * v)
            o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#a88a55" stroke-width="0.6"/>')
    else:
        o.append(box(3, 110, zsc, 26, 48, 1.2, "#1d1a17", "#1d1a17", "#16130f"))
        for i in range(8):
            xx = 3.2 + i * 3.25
            o.append(box(xx, 110, zsc - 0.2, 2.1, 48, 1.6, OAK, OAK_T, OAK_S))
    return "\n".join(o)



def plant():
    """A big leafy plant in the west recess, beyond the vinyl cabinet."""
    o = []
    base = P(345, 0, 4)
    k = D / (D + 4)
    s = S * k
    x, y = base
    pw_top, pw_bot, ph = 30 * s, 23 * s, 28 * s
    o.append(f'<ellipse cx="{x:.1f}" cy="{y + 2:.1f}" rx="{pw_bot * 0.7:.1f}" ry="{6 * k:.1f}" fill="#000" opacity="0.25" filter="url(#soft)"/>')
    rnd = random.Random(11)
    leaves = []
    for i in range(34):
        ang = rnd.uniform(-2.7, -0.45)
        r = rnd.uniform(25, 85) * k
        lx = x + math.cos(ang) * r * 1.35
        ly = y - ph - 6 * k + math.sin(ang) * r
        rot = math.degrees(ang) + rnd.uniform(-25, 25)
        col = rnd.choice(["#2f7a3f", "#3a8f4a", "#24683a", "#4aa35a", "#2c6f3a"])
        leaves.append(f'<ellipse cx="{lx:.1f}" cy="{ly:.1f}" rx="{rnd.uniform(16, 26) * k:.1f}" ry="{rnd.uniform(6, 9) * k:.1f}" fill="{col}" transform="rotate({rot:.1f} {lx:.1f} {ly:.1f})"/>')
    for i in range(12):
        lx = x + rnd.uniform(-20, 20) * k; ly = y - ph - rnd.uniform(0, 40) * k
        o.append(f'<line x1="{x:.1f}" y1="{y - ph:.1f}" x2="{lx:.1f}" y2="{ly:.1f}" stroke="#2a5a2e" stroke-width="2"/>')
    o.extend(leaves)
    o.append(f'<path d="M{x - pw_top / 2:.1f},{y - ph:.1f} L{x + pw_top / 2:.1f},{y - ph:.1f} L{x + pw_bot / 2:.1f},{y:.1f} L{x - pw_bot / 2:.1f},{y:.1f}Z" fill="url(#pot)"/>')
    o.append(f'<rect x="{x - pw_top / 2 - 3:.1f}" y="{y - ph - 4:.1f}" width="{pw_top + 6:.1f}" height="{9 * k:.1f}" fill="#c76d45"/>')
    return "\n".join(o)


def glow_overlays():
    """Bias light behind the TV (6500K)."""
    c = P(TV_CX, TV_Y + TV_H / 2, ALC_D - 0.5)
    return f'<ellipse cx="{c[0]:.1f}" cy="{c[1]:.1f}" rx="300" ry="205" fill="url(#bias)"/>'


# ------------------------------------------------------------- dimensions
LC = "#f3e9d4"

def dim_line(a, b, label=None, lpos=None, tick=7, size=13, anchor="middle", op=0.75):
    out = [f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{LC}" stroke-opacity="{op}" stroke-width="1.2"/>']
    ang = math.atan2(b[1] - a[1], b[0] - a[0]) + math.pi / 2
    for p in (a, b):
        dx, dy = math.cos(ang) * tick / 2, math.sin(ang) * tick / 2
        out.append(f'<line x1="{p[0] - dx:.1f}" y1="{p[1] - dy:.1f}" x2="{p[0] + dx:.1f}" y2="{p[1] + dy:.1f}" stroke="{LC}" stroke-opacity="{op}" stroke-width="1.2"/>')
    if label:
        lx, ly = lpos if lpos else ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 7)
        out.append(text(lx, ly, label, size=size, anchor=anchor, op=0.92))
    return "\n".join(out)



def uprights():
    """Joinery version: two solid oak uprights, worktop to ceiling (159 long), 4.5 thick, 30 deep, against the
    back wall, 2 cm clear of the screen each side. The high shelf and the record ledge are housed and pegged;
    the left and right shelves pass through as wedged through-tenons; LED grooves on the inner faces."""
    o = []
    UP, UP_T, UP_S, UP_IN = "#c08a52", "#d6a26a", "#a06c3a", "#b17d47"
    for (x1, x2), side in ((UPL, 1), (UPR, -1)):
        xe = x2 if side == 1 else x1
        a, b = P(xe, WT + 3, ALC_D - 0.2), P(xe + side * 20, HS_TOP - 8, ALC_D - 0.2)
        o.append(f'<rect x="{min(a[0], b[0]):.1f}" y="{b[1]:.1f}" width="{abs(b[0]-a[0]):.1f}" height="{a[1]-b[1]:.1f}" fill="#ffd9a0" opacity="0.10" filter="url(#softer)"/>')
    # record ledge between the uprights: 126.5 long, 7 deep, top at 155.4, 1.5 cm lip; four LPs face-out (125.6)
    lz = ALC_D - 7
    o.append(box(UPL[1], LEDGE_Y, lz, UPR[0] - UPL[1], LEDGE_TOP - LEDGE_Y, 7, UP, UP_T, UP_S, extra=GH))
    lean = math.radians(8); hgt = 31.4 * math.cos(lean); dzl = 31.4 * math.sin(lean)
    arts = [
        [("#1f3a52", 0, 1, 0, 1), ("#e9b44c", 0, 1, 0, 0.42), ("#d8613e", 0.12, 0.88, 0.5, 0.9)],
        [("#efe6d2", 0, 1, 0, 1), ("#2f3e5c", 0.1, 0.9, 0.55, 0.9), ("#c8452f", 0.3, 0.7, 0.15, 0.45)],
        [("#14806d", 0, 1, 0, 1), ("#f0c24b", 0.2, 0.8, 0.2, 0.8), ("#1f1f1f", 0.42, 0.58, 0.42, 0.58)],
        [("#2c2c2c", 0, 1, 0, 1), ("#e8603c", 0.08, 0.92, 0.1, 0.3), ("#efe6d2", 0.08, 0.92, 0.66, 0.9)],
    ]
    for i, art in enumerate(arts):
        x0 = UPL[1] + 0.45 + i * 31.42
        zb = ALC_D - 4.5
        q = [P(x0, LEDGE_TOP, zb), P(x0 + 31.4, LEDGE_TOP, zb), P(x0 + 31.4, LEDGE_TOP + hgt, zb + dzl), P(x0, LEDGE_TOP + hgt, zb + dzl)]
        o.append(lp_art(q, art))
    o.append(box(UPL[1], LEDGE_TOP, lz, UPR[0] - UPL[1], 1.5, 0.9, UP, UP_T, UP_S))          # lip
    for (x1, x2) in (UPL, UPR):
        o.append(box(x1, WT, UP_Z, x2 - x1, CEIL - WT, UP_D, UP, UP_T, UP_IN, extra=GV))
        a, b = P(x1 + 0.5, WT, UP_Z - 0.02), P(x1 + 0.5, CEIL, UP_Z - 0.02)
        o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#e7b57c" stroke-width="1"/>')
        a, b = P(x2 - 0.5, WT, UP_Z - 0.02), P(x2 - 0.5, CEIL, UP_Z - 0.02)
        o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#8f5e33" stroke-width="1"/>')
        for yy in (HS_TOP - 2.0, LEDGE_Y + 1.2):          # oak pegs: high shelf and ledge
            p = P((x1 + x2) / 2, yy, UP_Z - 0.03)
            o.append(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="2.3" fill="#5e3d22"/>')
            o.append(f'<circle cx="{p[0]-0.6:.1f}" cy="{p[1]-0.6:.1f}" r="0.9" fill="#8a5c36"/>')
    for xe in (UPL[1], UPR[0]):                          # LED grooves on the inner faces
        a, b = P(xe, WT + 3, UP_Z + 14), P(xe, HS_TOP - 7, UP_Z + 14)
        o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#ffe2b0" stroke-width="2" opacity="0.85"/>')
    def tenon(xface, dirn, ytop, zcs):
        th_t = 2.4
        for zc in zcs:
            x_a, x_b = (xface, xface + 2.0) if dirn == 1 else (xface - 2.0, xface)
            o.append(box(x_a, ytop - 0.8 - th_t, zc - 3.5, x_b - x_a, th_t, 7, "#a8743f", "#c9935a", "#7e5128"))
            xe = x_b if dirn == 1 else x_a
            ym = ytop - 0.8 - th_t / 2      # flat kerf: the wedge spreads the tenon along the upright's grain
            p1, p2 = P(xe, ym, zc - 3.0), P(xe, ym, zc + 3.0)
            o.append(f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="#4a2f19" stroke-width="1.6"/>')
    tenon(UPL[1], 1, SH_TOP, (19.5, 31.5))       # left shelf, through the left upright
    tenon(UPR[0], -1, SH_TOP, (19.5, 31.5))      # right shelf, through the right upright
    return "\n".join(o)


def led_lines():
    """Slat version: warm LED strips under the shelves."""
    o = []
    for (x1, x2, y, z) in [(1, ALC_W - 1, HS_TOP - HS_TH, 10), (2, UPL[0] - 1, SH_TOP - 4, 15), (UPR[1] + 1, ALC_W - 2, SH_TOP - 4, 15)]:
        a, b = P(x1, y - 0.1, z), P(x2, y - 0.1, z)
        o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#ffe2b0" stroke-width="2.2" opacity="0.9"/>')
    return "\n".join(o)


def dimensions():
    o = ['<g id="dims">']
    a, b = P(0, CEIL - 6, -2), P(ALC_W, CEIL - 6, -2)
    o.append(dim_line(a, b, "alcove 186 wide × 38 deep, floor to ceiling", ((a[0] + b[0]) / 2, a[1] - 9)))
    a, b = P(ALC_W, CEIL - 6, -2), P(BR_X2, CEIL - 6, -2)
    o.append(dim_line(a, b, "chimney breast 117.5", ((a[0] + b[0]) / 2, a[1] - 9)))
    lx = BR_X2 + 8
    a, b = P(lx, 0, 0), P(lx, CEIL, 0)
    o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{LC}" stroke-opacity="0.6" stroke-width="1.2"/>')
    ticks = [(0, "0 floor"), (WT, "76 worktop + cabinet top"), (TV_Y + TV_H / 2, "116.6 TV centre"), (140, "140 LP frames"),
             (SH_TOP, "156 side shelves · 155.4 ledge"), (HS_TOP, "200 high shelf, 30 deep"), (CEIL, "235 ceiling")]
    for h, lab in ticks:
        p = P(lx, h, 0)
        o.append(f'<line x1="{p[0] - 5:.1f}" y1="{p[1]:.1f}" x2="{p[0] + 5:.1f}" y2="{p[1]:.1f}" stroke="{LC}" stroke-opacity="0.75" stroke-width="1.2"/>')
        o.append(text(p[0] + 10, p[1] + 4.5, lab, size=12.5))
    o.append(text(P(lx, 0, 0)[0] + 10, P(lx, CEIL, 0)[1] - 22, "height, cm", size=11.5, op=0.7))
    # widths along the floor in front of the base
    zf = BASE_F - (40 if GAME_OPEN > 0 else 6)
    edges = [0, 3, 63, 123, 183, ALC_W]
    a, b = P(0, 0, zf), P(ALC_W, 0, zf)
    o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{LC}" stroke-opacity="0.7" stroke-width="1.2"/>')
    labels = [None, "60 · Xbox bay + game drawer", "60 · PlayStation bay", "60 · sub bay", None]
    for i, e in enumerate(edges):
        p = P(e, 0, zf)
        o.append(f'<line x1="{p[0]:.1f}" y1="{p[1] - 5:.1f}" x2="{p[0]:.1f}" y2="{p[1] + 5:.1f}" stroke="{LC}" stroke-opacity="0.75" stroke-width="1.2"/>')
        if i < 5 and labels[i]:
            m = P((e + edges[i + 1]) / 2, 0, zf)
            o.append(text(m[0], m[1] + 19, labels[i], size=12.5, anchor="middle"))
    zc = CAB_F - (36 if REC_OPEN > 0 else 6)
    a, b = P(CAB_X1, 0, zc), P(CAB_X2, 0, zc)
    o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{LC}" stroke-opacity="0.7" stroke-width="1.2"/>')
    for e in (CAB_X1, CAB_X1 + 60, CAB_X2):
        p = P(e, 0, zc)
        o.append(f'<line x1="{p[0]:.1f}" y1="{p[1] - 5:.1f}" x2="{p[0]:.1f}" y2="{p[1] + 5:.1f}" stroke="{LC}" stroke-opacity="0.75" stroke-width="1.2"/>')
    m = P(CAB_X1 + 30, 0, zc); o.append(text(m[0], m[1] + 19, "60 · two record trays", size=12.5, anchor="middle"))
    m = P(CAB_X1 + 80, 0, zc); o.append(text(m[0], m[1] + 19, "40 · preamp + kit", size=12.5, anchor="middle"))
    if GAME_OPEN > 0:
        a, b = P(BAYS[0][0] + 58.4, RAISE + 0.2, BASE_F - 0.6), P(BAYS[0][0] + 58.4, RAISE + 0.2, BASE_F - GAME_OPEN - 0.6)
        o.append(dim_line(a, b, op=0.75))
        o.append(text(b[0] + 12, b[1] - 2, "rolls out 30 cm", size=11.5, anchor="start"))
    # 40 cm lid clearance over the deck
    p1, p2 = P(CAB_X2 - 47, CAB_TOP + 15, CAB_F + 5), P(CAB_X2 - 2, CAB_TOP + 55, CAB_F + 5)
    o.append(f'<rect x="{p1[0]:.1f}" y="{p2[1]:.1f}" width="{p2[0] - p1[0]:.1f}" height="{p1[1] - p2[1]:.1f}" fill="none" stroke="{LC}" stroke-opacity="0.5" stroke-width="1.1" stroke-dasharray="5 4"/>')
    o.append(text((p1[0] + p2[0]) / 2, p2[1] + 18, "40 cm lid clearance", size=11, anchor="middle", op=0.8))
    o.append('</g>')
    return "\n".join(o)


def ceiling_leds():
    """The existing LED strip: stuck to the ceiling facing down, right round the room's edge
    (east wall, into the alcove, along its back wall and reveal, across the chimney breast, round the recess)."""
    o = []
    y = CEIL - 0.6
    runs = [((0.8, y, -300), (0.8, y, ALC_D - 0.8)), ((0.8, y, ALC_D - 0.8), (ALC_W - 0.8, y, ALC_D - 0.8)),
            ((ALC_W - 0.8, y, ALC_D - 0.8), (ALC_W - 0.8, y, 0.8)), ((ALC_W - 0.8, y, -0.8), (BR_X2 + 0.8, y, -0.8)),
            ((BR_X2 + 0.8, y, -0.8), (BR_X2 + 0.8, y, REC_D - 0.8)), ((BR_X2 + 0.8, y, REC_D - 0.8), (700, y, REC_D - 0.8))]
    def band(x0, z0, x1, z1):
        q = [P(x0, CEIL, z0), P(x1, CEIL, z1), P(x1, CEIL - 26, z1), P(x0, CEIL - 26, z0)]
        return poly(q, "#ffe3b3", 'opacity="0.20" filter="url(#softer)"')
    o.append(band(0.1, -300, 0.1, ALC_D - 0.1))
    o.append(band(0, ALC_D - 0.1, ALC_W, ALC_D - 0.1))
    o.append(band(ALC_W - 0.1, ALC_D, ALC_W - 0.1, 0))
    o.append(band(ALC_W, -0.1, BR_X2, -0.1))
    o.append(band(BR_X2, REC_D - 0.1, 700, REC_D - 0.1))
    for a, b in runs:
        pa, pb = P(*a), P(*b)
        o.append(f'<line x1="{pa[0]:.1f}" y1="{pa[1]:.1f}" x2="{pb[0]:.1f}" y2="{pb[1]:.1f}" stroke="#ffe7bd" stroke-width="7" opacity="0.45" filter="url(#soft)"/>')
        o.append(f'<line x1="{pa[0]:.1f}" y1="{pa[1]:.1f}" x2="{pb[0]:.1f}" y2="{pb[1]:.1f}" stroke="#fff6e2" stroke-width="2.2"/>')
    return "\n".join(o)


def wall_shadows():
    """Soft contact shadows on the wall under each oak shelf, and a little shade in the alcove's corners."""
    o = [quad_front(0, WT, ALC_D - 0.05, 7, CEIL - WT, "url(#shadeL)"), quad_front(ALC_W - 7, WT, ALC_D - 0.05, 7, CEIL - WT, "url(#shadeR)")]
    for (x1, x2, yu, dh) in [(0, ALC_W, HS_TOP - HS_TH, 7), (0, UPL[0], SH_TOP - 4, 6), (UPR[1], ALC_W, SH_TOP - 4, 6),
                             (UPL[1], UPR[0], LEDGE_Y, 5)]:
        o.append(quad_front(x1, yu - dh, ALC_D - 0.1, x2 - x1, dh, "url(#shadeDown)"))
    return "\n".join(o)


# the existing rose: in line with the breast's reveal (186 from the east wall), 173.5 from the window wall
PEND_X, PEND_Z = ALC_W, WIN_Z + 173.5

def _hull(pts_):
    pts_ = sorted(set((round(x, 2), round(y, 2)) for x, y in pts_))
    if len(pts_) < 3:
        return pts_
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts_:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts_):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def _norm(v):
    l = math.sqrt(sum(c * c for c in v)); return tuple(c / l for c in v)


def _cone(apex, d, length, r0, r1, n=28):
    """Projected silhouette of a cone frustum along unit vector d from apex; returns (hull, mouth ring, mouth centre)."""
    d = _norm(d)
    a = (0.0, 1.0, 0.0) if abs(d[1]) < 0.9 else (1.0, 0.0, 0.0)
    u = _norm((a[1] * d[2] - a[2] * d[1], a[2] * d[0] - a[0] * d[2], a[0] * d[1] - a[1] * d[0]))
    w = (d[1] * u[2] - d[2] * u[1], d[2] * u[0] - d[0] * u[2], d[0] * u[1] - d[1] * u[0])
    m = tuple(apex[i] + d[i] * length for i in range(3))
    ring0 = [P(*[apex[i] + r0 * (math.cos(t) * u[i] + math.sin(t) * w[i]) for i in range(3)]) for t in [2 * math.pi * k / n for k in range(n)]]
    ring1 = [P(*[m[i] + r1 * (math.cos(t) * u[i] + math.sin(t) * w[i]) for i in range(3)]) for t in [2 * math.pi * k / n for k in range(n)]]
    return _hull(ring0 + ring1), ring1, m


SPOT_HEADS = [   # x offset on the bar, shade colour, stem colour, aim (unit-ish vector: +z is towards the media wall)
    (-31.5, "#a9c7ab", "#8db59c", (-0.35, -0.55, 0.76)),    # sage green: books and left shelf
    (-10.5, "#a7d0d8", "#7fbfc8", (0.05, -0.62, 0.78)),     # pale blue: record ledge and high shelf
    (10.5, "#e8b53f", "#dca52f", (0.30, -0.92, -0.25)),     # mustard: down into the room
    (31.5, "#e79c95", "#d9877f", (0.55, -0.72, -0.42)),     # dusty pink: down towards the sofa
]

def pendant():
    """v9 ceiling light: a 4-head semi-flush spotlight bar in the style of Dunelm's Wolston: white bar, conical
    shades in four colours with light-wood toppers, about 84 cm long with a 22 cm drop, on the existing rose."""
    o = []
    cx, cz = PEND_X, PEND_Z
    cam = (EYE_X, EYE_Y, -D)
    # light pools where the two back heads land on the alcove wall / high shelf
    for dx, col, stem, d in SPOT_HEADS:
        d = _norm(d)
        if d[2] > 0:
            ap = (cx + dx, CEIL - 6.5, cz)
            t = (ALC_D - 0.1 - ap[2]) / d[2]
            hit = (ap[0] + d[0] * t, ap[1] + d[1] * t, ALC_D - 0.1)
            c = P(*hit)
            o.append(f'<ellipse cx="{c[0]:.1f}" cy="{c[1]:.1f}" rx="95" ry="70" fill="#fff1d2" opacity="0.16" filter="url(#softer)"/>')
    # ceiling plate and bar
    o.append(ellipse_flat(cx, CEIL - 0.05, cz, 6.5, 6.5, "#f3f1ec", 'stroke="#d8d4cc" stroke-width="1"'))
    o.append(box(cx - 6, CEIL - 2.6, cz - 6, 12, 2.5, 12, "#efede8", "#f7f5f0", "#dcd8d0"))
    o.append(box(cx - 42, CEIL - 3.8, cz - 1.1, 84, 1.3, 2.2, "#f2f0eb", "#fbfaf6", "#d9d5cc"))
    heads = sorted(SPOT_HEADS, key=lambda h: -(PEND_Z + h[3][2]))     # far heads first
    for dx, col, stem, d in heads:
        x0 = cx + dx
        a_, b_ = P(x0, CEIL - 3.8, cz), P(x0, CEIL - 6.5, cz)
        o.append(f'<line x1="{a_[0]:.1f}" y1="{a_[1]:.1f}" x2="{b_[0]:.1f}" y2="{b_[1]:.1f}" stroke="{stem}" stroke-width="3.2" stroke-linecap="round"/>')
        apex = (x0, CEIL - 6.5, cz)
        dn = _norm(d)
        # wood topper (short, slightly flared), then the conical shade
        th, _, tm = _cone(apex, dn, 3.8, 1.1, 1.9)
        sh, ring, m = _cone(tm, dn, 13.0, 1.9, 7.5)
        tomouth = _norm(tuple(cam[i] - m[i] for i in range(3)))
        facing = sum(dn[i] * tomouth[i] for i in range(3)) > 0.05
        o.append(poly(sh, col, 'stroke="#00000022" stroke-width="0.8"'))
        if facing:
            o.append(poly(ring, "#fffaf0", f'stroke="{col}" stroke-width="1.2"'))
            cc = P(*m)
            o.append(f'<circle cx="{cc[0]:.1f}" cy="{cc[1]:.1f}" r="16" fill="#fff4dc" opacity="0.55" filter="url(#soft)"/>')
        o.append(poly(th, "#d6a873", 'stroke="#a8784a" stroke-width="0.6"'))
    return "\n".join(o)



SOCKET_Z = (-29.3, -14.7)   # on the east wall just in front of the base (bay 1), about 30 cm up

def wall_socket():
    """The room's socket: on the east (side) wall just in front of bay 1, about 30 cm up; becomes a double."""
    o = []
    z1, z2, y1, y2 = SOCKET_Z[0], SOCKET_Z[1], 25.7, 34.3
    o.append(poly([P(0.4, y1, z1), P(0.4, y1, z2), P(0.4, y2, z2), P(0.4, y2, z1)], "#f4f2ed", 'stroke="#c9c5bc" stroke-width="1"'))
    for zc in (z1 + 3.8, z2 - 3.8):
        o.append(poly([P(0.9, 27.5, zc - 1.6), P(0.9, 27.5, zc + 1.6), P(0.9, 32.0, zc + 1.6), P(0.9, 32.0, zc - 1.6)], "#e9e6df", 'stroke="#b9b4aa" stroke-width="0.8"'))
        a_, b_, c_ = P(1.2, 27.5, zc), P(1.6, 6, zc + 2), P(1.2, 3, BASE_F - 0.5)
        o.append(f'<path d="M{a_[0]:.1f},{a_[1]:.1f} Q{b_[0]:.1f},{b_[1]:.1f} {c_[0]:.1f},{c_[1]:.1f}" stroke="#f0eee8" stroke-width="2.6" fill="none"/>')
    return "\n".join(o)


def services(show_hidden):
    """Hidden routes, drawn dashed in the numbered views. Gold: data, audio and low-voltage. Coral: mains."""
    if not show_hidden:
        return ""
    o = []
    GOLD, CORAL = "#ffd37a", "#ff9b7a"
    def path(pts_, col, w=2.4):
        q = [P(*p) for p in pts_]
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in q)
        return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-dasharray="7 5" opacity="0.95"/>'
    gx = UPR[0] + 2.2 if STYLE == "joinery" else ALC_W - 2
    # Cat6 down from the ceiling to Deco B; Deco's leads along the shelf's back, down the groove, into the channel
    o.append(path([(183.5, CEIL, 36.5), (183.5, HS_TOP + 6, 36.5), (178, HS_TOP + 4, 33)], GOLD))
    o.append(path([(170, HS_TOP + 0.5, 34), (gx, HS_TOP + 0.5, 37.3), (gx, WT, 37.3), (gx, 40, 36), (150, 36, 36)], GOLD))
    # vinyl: deck leads down through a grommet to the preamp in bay B; preamp -> soundbar AUX across to the alcove
    o.append(path([(CAB_X2 - 20, CAB_TOP, -12), (CAB_X2 - 20, 42, -12), (CAB_X1 + 72, 42, -30)], GOLD))
    o.append(path([(CAB_X1 + 66, 40, -30), (CAB_X1 + 4, 4, -30), (CAB_X1 - 1, 4, -4), (ALC_W - 4, 4, -4), (170, 4, 34), (150, 74, 35), (TV_CX + 40, WT + 1, 2)], GOLD, 2.0))
    # mains from the side-wall socket: in through a notch at the left end of the plinth, back through it to the channel
    o.append(path([(1.5, 4, BASE_F + 1), (4, 4, 10), (4, 4, 36), (60, 6, 36.5), (100, 6, 36.5), (100, WT + 1, 32)], CORAL, 2.0))
    o.append(path([(100, 6, 36.5), (150, 34, 36.5)], CORAL, 2.0))
    o.append(path([(150, 30, 36.5), (178, 3, 30), (ALC_W + 1, 3, -5), (CAB_X1 + 4, 3, -30), (CAB_X1 + 70, 30, -30)], CORAL, 2.0))
    # the 10-gang behind the TV
    p1, p2 = P(TV_CX - 30, WT, 26), P(TV_CX + 30, WT + 4.5, 26)
    o.append(f'<rect x="{p1[0]:.1f}" y="{p2[1]:.1f}" width="{p2[0]-p1[0]:.1f}" height="{p1[1]-p2[1]:.1f}" fill="{GOLD}" fill-opacity="0.15" stroke="{GOLD}" stroke-width="2" stroke-dasharray="6 4"/>')
    return "\n".join(o)

def plate(title, sub, x=24, y=None, w=640):
    """Label plate on the plain renders."""
    title, sub = title.replace("&", "&amp;"), sub.replace("&", "&amp;")
    y = H - 24 - 66 if y is None else y
    return (f'<rect x="{x}" y="{y}" width="{w}" height="66" rx="10" fill="#f4efe4" opacity="0.94"/>'
            f'<text x="{x + 20}" y="{y + 29}" font-family="Inter, sans-serif" font-size="18" font-weight="700" fill="#14261d">{title}</text>'
            f'<text x="{x + 20}" y="{y + 51}" font-family="Inter, sans-serif" font-size="13" fill="#5f5a50">{sub}</text>')



H_ = "H"
JOIN_KEY = [
    (H_, "Oak joinery"),
    (1, (UPL[0] + 2.25, 128, UP_Z), "Solid oak uprights, worktop to ceiling, 4.5 × 30 × 159"),
    (2, (UPL[1] + 3.5, 150.5, 19.5), "Wedged through-tenons: side shelves, top 156"),
    (3, (UPR[0] + 2.25, HS_TOP - 2, UP_Z), "Oak pegs where the high shelf and ledge are housed"),
    (4, (60, HS_TOP + 14, 21), "High shelf, top 200: books up to 30 cm"),
    (5, (TV_CX, 172, ALC_D - 3), "Record ledge above the TV: 4 LPs face-out"),
    (6, (UPL[1], 186, UP_Z + 14), "LED groove in each upright washes the wall"),
    (H_, "On the worktop"),
    (7, (48, 138, 18), "LG OLED C6 55in on its stand · centre 116.6"),
    (8, (TV_CX - 32, WT + 3, BASE_F + 1), "Soundbar · eARC, optical and AUX inputs"),
    (9, (12.6, 104, 12.7), "Series X on its fan stand · 2.4 clear each side"),
    (10, (ALC_W - 12.6, 97, 15), "Right zone: this month's game on an oak easel"),
    (11, (12, WT - 1.4, BASE_F), "Solid oak worktop 186 × 42 × 3, top at 76"),
    (H_, "In the base (alcove)"),
    (12, (93, 4.6, BASE_F), "Oak face frame, 8 cm proud of the breast"),
    (13, (23, 59.4, -2), "Xbox One + power brick · bay 1 top row"),
    (14, (23, 41.6, -2), "Xbox 360 + power brick · bay 1 middle row"),
    (15, (15, 24, None), "Game drawer: 2 face-out bins, spine-up rows behind"),
    (16, (83, 52.5, -2), "PS3 + controller basket · bay 2 top row"),
    (17, (83, 33.3, -2), "PS2 + HDMI switch · bay 2 middle row"),
    (18, (78, 13.5, -2), "PS1 + RetroTINK · bay 2 bottom row"),
    (19, (153, 22, -4), "Subwoofer on a 5 cm riser · bay 3"),
    (20, (171, 52, -4), "Bay 3 shelf: controller dock, spare pads"),
    (21, (138, 68.3, BASE_F - 0.7), "Hidden slim drawer under the worktop"),
    (H_, "Vinyl corner (chimney breast)"),
    (22, (CAB_X1 + 4, 36, CAB_F), "Oak vinyl cabinet, 100 × 44 × 76"),
    (23, (CAB_X1 + 30, 56, CAB_F + 3), "Upper record tray: ~90 LPs + ~120 singles, face-out"),
    (24, (CAB_X1 + 30, 22, "rec"), "Lower record tray: the same, shown pulled out"),
    (25, (CAB_X1 + 80, 50, CAB_F + 9), "Bay B: preamp, stylus, brush; singles below"),
    (26, (CAB_X2 - 25, 97, CAB_F + 22), "Turntable on top · 40 cm clear for the lid"),
    (27, (CAB_X1 + 25, 103, CAB_F + 4.4), "LP browser · about 50 LPs face-out"),
    (28, (CAB_X1 + 56, 168, -1.7), "LP frames on the breast, from 140 up"),
    (H_, "Power, network and light"),
    (29, (174, HS_TOP + 16, 22), "Deco B: leads in the groove behind the upright"),
    (30, (183.5, 224, 36.5), "Cat6 from upstairs, through the ceiling"),
    (31, (0.3, 34, -22), "Double socket on the side wall, in front of bay 1"),
    (32, (TV_CX, WT + 3, 26), "10-gang extension, hidden behind the TV"),
    (33, (150, 37, 30), "6-way switched strip at the back of bay 3"),
    (34, (0.8, CEIL - 0.6, -60), "LED strip round the ceiling edge (as now)"),
    (35, (PEND_X, CEIL - 22, PEND_Z), "Ceiling light: 4-spot cone bar on the rose"),
    (H_, "PC corner"),
    (36, (27.5, 128, -152), "PC, glass side to the room · shelf top 110"),
    (37, (16, 134, -194.9), "Oak frame with woven cane hides the ports"),
    (38, (34, 102.5, -158), "Keyboard + mouse tray, rolls out 25 cm"),
    (39, (0.4, 55, -188), "PC cables: shelf notch → trunking → skirting"),
]

KEYW = 640

def key_panel2(x0, items, title, sub, step=26.5):
    o = [f'<rect x="{x0}" y="0" width="{KEYW}" height="{H}" fill="#f4efe4"/>',
         f'<text x="{x0 + 36}" y="54" font-family="Inter, sans-serif" font-size="24" font-weight="700" fill="#14261d">{title}</text>',
         f'<text x="{x0 + 36}" y="78" font-family="Inter, sans-serif" font-size="13" fill="#5f5a50">{sub}</text>']
    y = 104
    for it in items:
        if it[0] == H_:
            y += 10
            o.append(f'<text x="{x0 + 36}" y="{y + 4}" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" letter-spacing="1.2" fill="#6b6455">{it[1].upper()}</text>')
            o.append(f'<line x1="{x0 + 36}" y1="{y + 11}" x2="{x0 + KEYW - 36}" y2="{y + 11}" stroke="#d8d0bf" stroke-width="1"/>')
            y += 28
            continue
        n, _, label = it
        o.append(f'<circle cx="{x0 + 50}" cy="{y - 5}" r="12" fill="#fff" stroke="#14261d" stroke-width="1.4"/>')
        o.append(f'<text x="{x0 + 50}" y="{y - 0.7}" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#14261d" text-anchor="middle">{n}</text>')
        o.append(f'<text x="{x0 + 74}" y="{y}" font-family="Inter, sans-serif" font-size="14" fill="#1f1f1f">{label}</text>')
        y += step
    o.append(f'<text x="{x0 + 36}" y="{H - 28}" font-family="Inter, sans-serif" font-size="12" fill="#6b6455">Dashed lines are hidden: gold for data and low-voltage leads, coral for mains.</text>')
    return "\n".join(o)


def callouts(items=None):
    items = items or CALLOUTS
    o = ['<g id="callouts">']
    for it in items:
        if it[0] == "H":
            continue
        n, (x, y, z), _ = it
        if z is None:
            z = BASE_F - GAME_OPEN + 4
        elif z == "back":
            z = BASE_F - GAME_OPEN + 22
        elif z == "rec":
            z = CAB_F - REC_OPEN + 1
        cx, cy = P(x, y, z)
        o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="15" fill="#000" opacity="0.25" filter="url(#soft)"/>')
        o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="13.5" fill="#f7f1e3" stroke="#10241b" stroke-width="1.6"/>')
        o.append(f'<text x="{cx:.1f}" y="{cy + 4.6:.1f}" font-family="Inter, sans-serif" font-size="13" font-weight="700" fill="#10241b" text-anchor="middle">{n}</text>')
    o.append('</g>')
    return "\n".join(o)


def key_panel(x0, items=None, title="Key", sub="Numbers match the plan · sizes in cm", step=32.2):
    items = items or CALLOUTS
    o = [f'<rect x="{x0}" y="0" width="560" height="{H}" fill="#f4efe4"/>',
         f'<text x="{x0 + 36}" y="58" font-family="Inter, sans-serif" font-size="24" font-weight="700" fill="#14261d">{title}</text>',
         f'<text x="{x0 + 36}" y="84" font-family="Inter, sans-serif" font-size="13" fill="#5f5a50">{sub}</text>']
    y = 116
    for n, _, label in items:
        o.append(f'<circle cx="{x0 + 50}" cy="{y - 5}" r="13" fill="#fff" stroke="#14261d" stroke-width="1.4"/>')
        o.append(f'<text x="{x0 + 50}" y="{y - 0.5}" font-family="Inter, sans-serif" font-size="12.5" font-weight="700" fill="#14261d" text-anchor="middle">{n}</text>')
        o.append(f'<text x="{x0 + 76}" y="{y}" font-family="Inter, sans-serif" font-size="14" fill="#1f1f1f">{label}</text>')
        y += step
    return "\n".join(o)


def drawer_inset(x0=24, y0=852, num=16):
    """Top-down detail of the game drawer, drawn as a card on the floor area."""
    k = 5.4
    w, h = 345, 285
    o = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="10" fill="#f4efe4" opacity="0.96"/>',
         f'<circle cx="{x0 + 24}" cy="{y0 + 24}" r="12" fill="#fff" stroke="#14261d" stroke-width="1.4"/>',
         f'<text x="{x0 + 24}" y="{y0 + 28.5}" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#14261d" text-anchor="middle">{num}</text>',
         f'<text x="{x0 + 44}" y="{y0 + 29}" font-family="Inter, sans-serif" font-size="13.5" font-weight="600" fill="#14261d">Game drawer from above, pulled out</text>']
    ox, oy = x0 + (w - 54.3 * k) / 2, y0 + 50
    X = lambda c: ox + c * k
    Y = lambda c: oy + (35 - c) * k   # z=0 (front) at the bottom
    o.append(f'<rect x="{X(0)}" y="{Y(35)}" width="{54.3*k}" height="{35*k}" fill="#d9c09a" stroke="#a88a62"/>')
    o.append(f'<rect x="{X(1.2)}" y="{Y(33.8)}" width="{51.9*k}" height="{32.6*k}" fill="#5a5148"/>')
    rnd = random.Random(21)
    x = 1.5
    for kind, n, t, ln in [("ps2", 15, 1.4, 19), ("x360", 12, 1.4, 19), ("f", 1, 2.0, 19), ("one", 9, 1.2, 17)]:
        for i in range(n):
            if kind == "f":
                o.append(f'<rect x="{X(x)}" y="{Y(14.9+ln)}" width="{t*k}" height="{ln*k}" fill="#c79a63"/>')
                x += t + 0.1; continue
            col = {"ps2": rnd.choice(["#0f0f12", "#e9e6df", "#121722"]), "x360": "#f2f1ec", "one": rnd.choice(["#f2f1ec", "#1c1c1c"])}[kind]
            band = {"ps2": "#2c4bb0", "x360": "#5ab845", "one": "#3fae54"}[kind]
            o.append(f'<rect x="{X(x)}" y="{Y(14.9+ln)}" width="{t*k*0.92}" height="{ln*k}" fill="{col}" stroke="#00000033" stroke-width="0.5"/>')
            o.append(f'<rect x="{X(x)}" y="{Y(14.9+ln)}" width="{t*k*0.92}" height="{3*k}" fill="{band}"/>')
            tc = "#8d8a84" if col.startswith("#f") or col.startswith("#e") else "#d8d4cc"
            o.append(f'<rect x="{X(x)+2}" y="{Y(14.9+ln-4.5)}" width="{max(t*k*0.92-4,1)}" height="{(ln-9)*k}" fill="{tc}" opacity="0.7"/>')
            x += t
    o.append(f'<rect x="{X(1.2)}" y="{Y(14.8)}" width="{51.9*k}" height="{0.6*k}" fill="#d9c09a"/>')
    for (a, b, lab, col) in [(1.2, 17.2, "Xbox bin", "#2c8f3e"), (37.1, 53.1, "PS2 bin", "#1d2f6b")]:
        o.append(f'<rect x="{X(a)}" y="{Y(14.2)}" width="{(b-a)*k}" height="{12.6*k}" fill="#e9dcc5"/>')
        for j in range(6):
            o.append(f'<rect x="{X((a+b)/2-6.75)}" y="{Y(2.6+j*1.45+1.3)}" width="{13.5*k}" height="{1.25*k}" fill="{col}" opacity="{1 - j*0.1}"/>')
        o.append(f'<text x="{X((a+b)/2)}" y="{Y(12.2)}" font-family="Inter, sans-serif" font-size="10.5" fill="#3d382f" text-anchor="middle">{lab}</text>')
    o.append(f'<rect x="{X(17.8)}" y="{Y(14.2)}" width="{18.7*k}" height="{12.6*k}" fill="#efe6d4"/>')
    o.append(f'<text x="{X(27.15)}" y="{Y(7.5)}" font-family="Inter, sans-serif" font-size="10.5" fill="#3d382f" text-anchor="middle">tray</text>')
    o.append(f'<rect x="{X(-1.3)}" y="{Y(1.4)}" width="{56.9*k}" height="{2*k}" fill="#c48c57"/>')
    o.append(f'<text x="{X(27.15)}" y="{Y(24.3)}" font-family="Inter, sans-serif" font-size="11" font-weight="600" fill="#f4efe4" text-anchor="middle" paint-order="stroke" stroke="#14261d" stroke-width="3">spines up · ~36 games</text>')
    o.append(f'<text x="{x0 + w/2}" y="{y0 + h - 12}" font-family="Inter, sans-serif" font-size="11" fill="#5f5a50" text-anchor="middle">front ↓ · box 54 × 35 cm · 350 mm runners</text>')
    return "\n".join(o)


def record_inset(x0=1545, y0=330, num=26):
    k = 3.9
    w, h = 245, 236
    o = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="10" fill="#f4efe4" opacity="0.96"/>',
         f'<circle cx="{x0 + 24}" cy="{y0 + 24}" r="12" fill="#fff" stroke="#14261d" stroke-width="1.4"/>',
         f'<text x="{x0 + 24}" y="{y0 + 28.5}" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#14261d" text-anchor="middle">{num}</text>',
         f'<text x="{x0 + 42}" y="{y0 + 29}" font-family="Inter, sans-serif" font-size="12.5" font-weight="600" fill="#14261d">Record tray from above</text>']
    ox, oy = x0 + (w - 53.9 * k) / 2, y0 + 44
    X = lambda c: ox + c * k
    Y = lambda c: oy + (40 - c) * k
    o.append(f'<rect x="{X(0)}" y="{Y(40)}" width="{53.9*k}" height="{40*k}" fill="#d9c09a" stroke="#a88a62"/>')
    o.append(f'<rect x="{X(0.9)}" y="{Y(39.1)}" width="{52.1*k}" height="{38.2*k}" fill="#5a5148"/>')
    cols = ["#e9e3d3", "#2f3e5c", "#c8452f", "#f0c24b", "#1f1f1f", "#6a8f5a", "#3a6ea5", "#b3307a"]
    for i in range(40):
        zz = 3.0 + i * 0.78
        o.append(f'<rect x="{X(1.5)}" y="{Y(zz + 0.5)}" width="{31.4*k}" height="{max(0.5*k - 0.3, 0.8)}" fill="{cols[i % 8]}"/>')
    o.append(f'<rect x="{X(33.5)}" y="{Y(39.1)}" width="{0.6*k}" height="{38.2*k}" fill="#c48c57"/>')
    for i in range(46):
        zz = 3.0 + i * 0.72
        o.append(f'<rect x="{X(34.4)}" y="{Y(zz + 0.4)}" width="{18.3*k}" height="{max(0.4*k - 0.3, 0.7)}" fill="{cols[(i*3) % 8]}"/>')
    o.append(f'<rect x="{X(-1.45)}" y="{Y(1.4)}" width="{56.8*k*0.95}" height="{1.5*k}" fill="#c48c57"/>')
    o.append(f'<text x="{X(17)}" y="{Y(22)}" font-family="Inter, sans-serif" font-size="10.5" font-weight="600" fill="#f4efe4" text-anchor="middle" paint-order="stroke" stroke="#14261d" stroke-width="3">~90 LPs</text>')
    o.append(f'<text x="{X(43.5)}" y="{Y(22)}" font-family="Inter, sans-serif" font-size="10.5" font-weight="600" fill="#f4efe4" text-anchor="middle" paint-order="stroke" stroke="#14261d" stroke-width="3">~120 singles</text>')
    o.append(f'<text x="{x0 + w/2}" y="{y0 + h - 22}" font-family="Inter, sans-serif" font-size="10" fill="#5f5a50" text-anchor="middle">all face-out · LPs left, singles right</text>')
    o.append(f'<text x="{x0 + w/2}" y="{y0 + h - 9}" font-family="Inter, sans-serif" font-size="10" fill="#5f5a50" text-anchor="middle">9 mm sides · 400 mm runners</text>')
    return "\n".join(o)

# ------------------------------------------------------------- paint
# v8: softer green. Every wall-paint shade in the drawing is remapped from the old deep forest green
# to a soft grey-green (close to Farrow & Ball Card Room Green No. 79), keeping the same light and shade.
PAINT_OLD = ["#16271f", "#1d3d30", "#21443a", "#22432f", "#244a38", "#244a39", "#264c3a", "#28503e", "#2a5141",
             "#2a5340", "#2b5643", "#2c5643", "#2d5a44", "#2d5a46", "#2f5b46", "#315c48", "#335f4a", "#33604a",
             "#346650", "#3a6b53", "#3a6d55", "#3b6e56", "#3d7259", "#447a60"]
PAINT = "soft"          # "soft" (v8) or "deep" (v7)
SOFT_HUE, SOFT_S, SOFT_L = 98 / 360, 0.135, 0.505   # base wall, lit, in evening light

def set_paint(hexcode, sat_boost=1.4, light=0.95):
    """Derive the lit-wall base from a paint's screen colour. Screen colours of paints are approximate,
    and the render's warm evening light pushes them a touch greener and darker."""
    import colorsys
    global SOFT_HUE, SOFT_S, SOFT_L, PAINT
    r, g, b = [int(hexcode[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    SOFT_HUE, SOFT_S, SOFT_L, PAINT = h, s * sat_boost, l * light, "soft"

PAINTS = {   # approximate screen colours (pontata.com)
    "card_room": ("#899081", "Farrow & Ball Card Room Green No. 79"),
    "treron": ("#8b8a77", "Farrow & Ball Treron No. 292"),
    "sage": ("#77815c", "Little Greene Sage Green No. 80"),
}
MAIN_PAINT = "card_room"   # v9: the client's choice (top right of the v8 grid)

def _soft(h):
    import colorsys
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    _, l, s = colorsys.rgb_to_hls(r, g, b)
    nl = min(0.80, SOFT_L * (l / 0.25) ** 0.8)
    ns = SOFT_S * (s / 0.32)
    nr, ng, nb = colorsys.hls_to_rgb(SOFT_HUE, nl, ns)
    return "#%02x%02x%02x" % (round(nr * 255), round(ng * 255), round(nb * 255))

def repaint(svg):
    if PAINT != "soft":
        return svg
    for h in PAINT_OLD:
        svg = svg.replace(h, _soft(h)).replace(h.upper(), _soft(h))
    return svg


def build(with_dims=True, numbered=False, game_open=0.0, rec_open=0.0, style="joinery", rec_open_up=0.0, label=None):
    global GAME_OPEN, REC_OPEN, STYLE, REC_OPEN_UP
    REC_OPEN_UP, STYLE, GAME_OPEN, REC_OPEN = rec_open_up, style, game_open, rec_open
    kw = KEYW if numbered else 0
    width = W + kw
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{H}" viewBox="0 0 {width} {H}">', defs(),
         f'<svg x="0" y="0" width="{W}" height="{H}" viewBox="0 0 {W} {H}" overflow="hidden">',
         f'<g transform="translate(0,{SHIFT})">', room(), ceiling_leds()]
    o.append(wall_shadows() if STYLE == "joinery" else slats())
    o.append(glow_overlays())
    o.append(high_shelf())
    o.append(side_shelves())
    if STYLE != "joinery":
        o.append(led_lines())
    o.append(tv())
    if STYLE == "joinery":
        o.append(uprights())
    o.append(breast_frames())
    o.append(plant())
    o.append(unit())
    o.append(worktop_items())
    o.append(vinyl_cabinet())
    o.append(left_wall_items())
    o.append(wall_socket())
    o.append(services(numbered))
    o.append(pendant())
    if with_dims:
        o.append(dimensions())
    if numbered:
        x0_, y0_, sc_ = INSET_DRAWER
        o.append(f'<g transform="translate({x0_},{y0_}) scale({sc_}) translate({-x0_},{-y0_})">' + drawer_inset(x0_, y0_, num=15) + '</g>')
        o.append(record_inset(*INSET_RECORD, num=23))
        o.append(callouts(JOIN_KEY))
    o.append('</g>')
    if label:
        o.append(plate(*label))
    o.append('</svg>')
    if numbered:
        o.append(key_panel2(W, JOIN_KEY, "Key: artisan oak media wall, v10", "Fitted to your measured room · numbers match the plan · cm", step=23.4))
    o.append('</svg>')
    return repaint("\n".join(o))


INSET_DRAWER = (14, 1000, 0.84)
INSET_RECORD = (1645, 1040)

if __name__ == "__main__":
    set_paint(PAINTS[MAIN_PAINT][0])
    sub = "Farrow & Ball Card Room Green No. 79 · fitted to your measured room, evening light"
    open("v10_join_key.svg", "w").write(build(with_dims=True, numbered=True, game_open=30, rec_open=30))
    open("v10_join_clean.svg", "w").write(build(with_dims=False, label=("Artisan oak media wall · main plan, v10", sub)))
    open("v10_slat_clean.svg", "w").write(build(with_dims=False, style="slats", label=("Slat wall · alternative, v10", sub)))
    for k, (hx, name) in list(PAINTS.items()):
        set_paint(hx)
        open(f"v10_paint_{k}.svg", "w").write(build(with_dims=False, label=(name + (" · chosen" if k == MAIN_PAINT else ""), "Artisan oak version · walls, ceiling and skirting in the one colour")))
        open(f"v10_slats_{k}.svg", "w").write(build(with_dims=False, style="slats", label=(name + " · slat wall", "Slat wall alternative · walls, ceiling and skirting in the one colour")))
    PAINT = "deep"
    open("v10_paint_deep.svg", "w").write(build(with_dims=False, label=("Deep forest green · earlier colour, for comparison", "Artisan oak version")))
    open("v10_slats_deep.svg", "w").write(build(with_dims=False, style="slats", label=("Deep forest green · slat wall", "Slat wall alternative")))
    print("ok")
