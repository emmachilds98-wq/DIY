"""Diagrams for the plan (v10: drawn from geometry.py, the measured room), as standalone SVG strings (Inter, light theme)."""
import geometry as G


INK = "#1f1f1f"; MUTED = "#6b6862"; LINE = "#cfcabf"; BOXF = "#f6f5f2"; BAND = "#efeeea"
BLUE = "#2a73d9"
GAME_F, GAME_S = "#e3ecfb", "#5b8ad6"
VIN_F, VIN_S = "#fbe6da", "#e07b4f"
SND_F, SND_S = "#dcf2e8", "#2fa47a"
FONT = 'font-family="Inter, sans-serif"'


def t(x, y, s, size=12, anchor="start", weight=400, fill=INK, extra=""):
    return f'<text x="{x}" y="{y}" {FONT} font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>'


def rect(x, y, w, h, fill=BOXF, stroke=LINE, rx=6, sw=1.2, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def node(x, y, w, h, title, sub=None, bold=True, fill="#fff", stroke=LINE):
    o = [rect(x, y, w, h, fill, stroke)]
    if sub:
        o.append(t(x + w / 2, y + h / 2 - 2, title, 12.5, "middle", 600 if bold else 400))
        o.append(t(x + w / 2, y + h / 2 + 13, sub, 10.5, "middle", 400, MUTED))
    else:
        o.append(t(x + w / 2, y + h / 2 + 4.5, title, 12.5, "middle", 600 if bold else 400))
    return "\n".join(o)


def wire(points, color=LINE, sw=1.4, dash=None):
    d = "M" + " L".join(f"{a},{b}" for a, b in points)
    da = f'stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" {da}/>'


def svg(w, h, body, title=None, sub=None):
    head = []
    top = 0
    if title:
        head.append(t(0, 16, title, 14.5, "start", 650))
        top = 22
    if sub:
        head.append(t(0, top + 16, sub, 11.5, "start", 400, MUTED))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%">'
            + "\n".join(head) + body + "</svg>")



def _fmt(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


# ------------------------------------------------------------------ network
def network():
    o = []
    W = 760
    bands = [("Top floor · bedroom 3 and the landing", 56, 178), ("Living room", 246, 214), ("Kitchen", 472, 74)]
    for name, y, h in bands:
        o.append(rect(0, y, W, h, BAND, "#e2e0da", 8))
        o.append(t(14, y + 20, name, 11.5, "start", 500, MUTED))
    o.append(node(14, 84, 128, 42, "Virgin Hub 5", "modem mode"))
    o.append(node(170, 84, 128, 42, "Deco A (main)", "router + Wi-Fi"))
    o.append(node(326, 84, 136, 42, "Switch 1", "8-port gigabit · new"))
    o.append(wire([(142, 105), (170, 105)]))
    o.append(wire([(298, 105), (326, 105)]))
    ends = [("PC 1", 72, False), ("PC 2", 108, False), ("Projector, master · optional", 144, True), ("Music room, bedroom 2 · optional", 180, True)]
    for name, y, opt in ends:
        o.append(node(530, y - 13, 220, 26, name, bold=False, fill="#fff" if not opt else "#fbfaf7"))
        o.append(wire([(462, 105 if not opt else 118), (505, 105 if not opt else 118), (505, y), (530, y)], LINE if not opt else BLUE, 1.4 if not opt else 1.8, None if not opt else "5 3"))
    o.append(t(710, 222, "1 port spare", 10.5, "end", 400, MUTED))
    o.append(node(170, 350, 128, 42, "Deco B", f"high shelf, {G.HIGH_TOP:g} cm"))
    o.append(node(326, 350, 136, 42, "Switch 2", "8-port, in the channel"))
    devs = ["Xbox Series X", "Xbox One", "Xbox 360", "PS3", "PC (side wall)", "LG C6 TV"]
    for i, d in enumerate(devs):
        y = 264 + i * 30
        o.append(node(560, y, 150, 24, d, bold=False))
        o.append(wire([(462, 371), (520, 371), (520, y + 12), (560, y + 12)]))
    o.append(t(710, 454, "1 port spare", 10.5, "end", 400, MUTED))
    o.append(wire([(298, 371), (326, 371)]))
    o.append(node(170, 496, 128, 40, "Deco C", "kitchen Wi-Fi"))
    o.append(wire([(380, 126), (380, 220), (234, 220), (234, 350)], BLUE, 2.4))
    o.append(t(244, 242, "Cat6 run 1", 10.5, "start", 500, BLUE))
    o.append(wire([(410, 126), (410, 210), (740, 210), (740, 516), (298, 516)], BLUE, 2.4))
    o.append(t(730, 506, "Cat6 run 2 (straight to the kitchen)", 10.5, "end", 500, BLUE))
    o.append(wire([(0, 570), (28, 570)], BLUE, 2.4)); o.append(t(36, 574, "Cat6 run between rooms", 11, "start", 400, MUTED))
    o.append(wire([(220, 570), (248, 570)])); o.append(t(256, 574, "short Cat6 patch lead", 11, "start", 400, MUTED))
    o.append(wire([(420, 570), (448, 570)], BLUE, 1.8, "5 3")); o.append(t(456, 574, "optional run, if you want it wired", 11, "start", 400, MUTED))
    return svg(W, 584, "\n".join(o), "Every floor has its own Cat6 link back to bedroom 3",
               "Deco A and Switch 1 live with the Hub 5 and the gaming PCs in bedroom 3; two spare ports can wire the projector and the music room")


# ------------------------------------------------------------------ front elevation
def front():
    s = 2.05
    W, H = 860, 640
    ox, oy = 104, 568
    X = lambda cm: ox + cm * s
    Y = lambda cm: oy - cm * s
    g = G
    o = []
    o.append(f'<rect x="{X(0)}" y="{Y(g.CEIL)}" width="{g.ALC_W*s}" height="{g.CEIL*s}" fill="#f8f7f4" stroke="{LINE}" stroke-width="1.2"/>')
    o.append(f'<rect x="{X(g.ALC_W)}" y="{Y(g.CEIL)}" width="{g.BREAST_W*s}" height="{g.CEIL*s}" fill="#f1efe9" stroke="{LINE}" stroke-width="1.2"/>')
    o.append(t(X(g.ALC_W + g.BREAST_W / 2), Y(g.CEIL) + 15, f"chimney breast, {_fmt(g.BREAST_W)} wide,", 10, "middle", 500, MUTED))
    o.append(t(X(g.ALC_W + g.BREAST_W / 2), Y(g.CEIL) + 28, f"{_fmt(g.ALC_D)} in front of the alcove", 10, "middle", 400, MUTED))
    o.append(t(X(g.ALC_W / 2), Y(g.CEIL) - 6, f"alcove {_fmt(g.ALC_W)} wide, {_fmt(g.ALC_D)} deep, ceiling {_fmt(g.CEIL)}", 10.5, "middle", 500, MUTED))
    o.append(f'<line x1="{X(-25)}" y1="{oy}" x2="{X(312)}" y2="{oy}" stroke="#b9b4a8" stroke-width="1.4"/>')
    # height scale
    hx = g.BREAST_X[1] + 3
    o.append(f'<line x1="{X(hx)}" y1="{Y(0)}" x2="{X(hx)}" y2="{Y(g.CEIL)}" stroke="#cfcabf"/>')
    for h, lab, dy in [(0, "0", 4), (9, "9 plinth", 6), (76, "76 worktop + cabinet top", 0), (116.55, "116.5 TV centre", 4),
                       (130, "130 clear above deck", 4), (156, "156 side shelves", 4), (196, "196 high shelf", 4), (235, "235", 4)]:
        o.append(f'<line x1="{X(hx)-3}" y1="{Y(h)}" x2="{X(hx)+3}" y2="{Y(h)}" stroke="#9a958b"/>')
        o.append(t(X(hx) + 6, Y(h) + dy, lab, 9.5, "start", 400, MUTED))
    # high shelf, books, box, print, Deco B
    o.append(rect(X(0), Y(g.HIGH_TOP), g.ALC_W * s, g.HIGH_T * s, "#e9dccb", "#c9b79f", 1))
    o.append(rect(X(1.5), Y(g.HIGH_TOP + 26), 22 * s, 26 * s, "#ecebe7", LINE, 2))
    o.append(rect(X(31), Y(g.HIGH_TOP + 28), 59 * s, 28 * s, "#ecebe7", LINE, 2))
    o.append(t(X(60), Y(g.HIGH_TOP + 12), "books, up to 30 tall", 9.5, "middle", 400, MUTED))
    o.append(rect(X(97), Y(g.HIGH_TOP + 22.5), 30 * s, 22.5 * s, "#ecebe7", LINE, 2))
    o.append(t(X(112), Y(g.HIGH_TOP + 9), "box", 9.5, "middle", 400, MUTED))
    dx = g.UP_R[1] + (g.ALC_W - g.UP_R[1] - 11) / 2
    o.append(rect(X(dx), Y(g.HIGH_TOP + 11.4), 11 * s, 11.4 * s, "#fff", LINE, 8))
    o.append(t(X(dx + 5.5), Y(g.HIGH_TOP + 16), "Deco B", 9.5, "middle", 600))
    o.append(wire([(X(g.ALC_W - 2), Y(g.CEIL)), (X(g.ALC_W - 2), Y(g.HIGH_TOP + 15)), (X(dx + 9), Y(g.HIGH_TOP + 9))], BLUE, 1.6))
    # uprights, ledge, side shelves
    for (a, b) in (g.UP_L, g.UP_R):
        o.append(f'<rect x="{X(a)}" y="{Y(g.CEIL)}" width="{g.UP_T*s}" height="{(g.CEIL-g.WORKTOP)*s}" fill="#e9d3b4" stroke="#b88a55"/>')
    o.append(rect(X(g.UP_L[1]), Y(g.LEDGE_TOP), g.TV_GAP * s, (g.LEDGE_TOP - g.LEDGE_UNDER) * s, "#e9dccb", "#b88a55", 1))
    for i in range(4):
        o.append(f'<rect x="{X(g.UP_L[1] + 0.45 + i * g.LP)}" y="{Y(g.LEDGE_LP_TOP)}" width="{g.LP*s}" height="{31.1*s}" fill="{VIN_F}" stroke="{VIN_S}" stroke-opacity="0.6"/>')
    o.append(t(X(g.TV_CX), Y(172), f"record ledge, top {_fmt(g.LEDGE_TOP)} · 4 LPs face-out", 9.5, "middle", 500, VIN_S))
    for (a, b) in ((0, g.UP_L[0]), (g.UP_R[1], g.ALC_W)):
        o.append(rect(X(a), Y(g.SIDE_SHELF_TOP), (b - a) * s, g.SIDE_SHELF_T * s, "#e9dccb", "#c9b79f", 1))
    o.append(rect(X(2), Y(g.SIDE_SHELF_TOP + 19), 9.6 * s, 19 * s, GAME_F, GAME_S, 1))
    o.append(rect(X(g.UP_R[1] + 2), Y(g.SIDE_SHELF_TOP + 21.3), 21.3 * s, 21.3 * s, VIN_F, VIN_S, 1))
    o.append(t(X(g.UP_R[1] + 12.6), Y(g.SIDE_SHELF_TOP + 9), "7-inch", 8.5, "middle", 500, VIN_S))
    # TV
    o.append(rect(X(g.TV_X[0]), Y(g.TV_TOP), g.TV_W * s, g.TV_H * s, "#ebeae6", "#c9c5bb", 4))
    o.append(t(X(g.TV_CX), Y(122), "LG OLED C6 55 in", 12.5, "middle", 650))
    o.append(t(X(g.TV_CX), Y(122) + 15, f"{_fmt(g.TV_W)} × {_fmt(g.TV_H)} · on LG's stand · centre 116.5", 10, "middle", 400, MUTED))
    o.append(t(X(g.TV_CX), Y(122) + 29, f"{_fmt(g.TV_CLEAR)} clear of each upright", 10, "middle", 400, MUTED))
    o.append(rect(X(g.TV_CX - 23.5), Y(g.WORKTOP + 1.6), 47 * s, 1.6 * s, "#d8d5ce", "#bdb8ad", 1))
    # Series X, soundbar, dock, 10-gang
    fx = g.FAN_STAND[0]; sx0 = (g.SIDE_ZONE - fx) / 2
    o.append(rect(X(sx0), Y(g.WORKTOP + 6.5), fx * s, 6.5 * s, GAME_F, GAME_S, 2))
    cx0 = sx0 + (fx - 15.1) / 2
    o.append(rect(X(cx0), Y(g.WORKTOP + 36.6), 15.1 * s, 30.1 * s, GAME_F, GAME_S, 3))
    o.append(t(X(g.SIDE_ZONE / 2), Y(100), "Series X", 9.5, "middle", 650))
    o.append(t(X(g.SIDE_ZONE / 2), Y(100) + 11, "fan stand", 8.5, "middle", 400, MUTED))
    o.append(rect(X(g.TV_CX - 46), Y(g.WORKTOP + 6), 92 * s, 6 * s, SND_F, SND_S, 2))
    o.append(rect(X(g.UP_R[1] + 3), Y(g.WORKTOP + 8), 18 * s, 8 * s, "#f1f0ec", LINE, 2))
    o.append(t(X(g.UP_R[1] + 12), Y(g.WORKTOP + 8) - 4, "pad dock", 8.5, "middle", 400, MUTED))
    o.append(f'<rect x="{X(70)}" y="{Y(80.5)}" width="{56*s}" height="{4.5*s}" fill="none" stroke="{VIN_S}" stroke-dasharray="4 3"/>')
    # worktop
    o.append(rect(X(0), Y(g.WORKTOP), g.ALC_W * s, 3 * s, "#e9dccb", "#c9b79f", 1))
    def cell(x1, x2, y1, y2, label, sub, kind):
        f, st = {"g": (GAME_F, GAME_S), "v": (VIN_F, VIN_S), "s": (SND_F, SND_S), "n": ("#f6f5f2", "#bdb8ad")}[kind]
        o.append(f'<rect x="{X(x1)}" y="{Y(y2)}" width="{(x2-x1)*s}" height="{(y2-y1)*s}" fill="{f}" stroke="{st}" stroke-opacity="0.55" stroke-width="1"/>')
        cy = (Y(y2) + Y(y1)) / 2
        o.append(t((X(x1) + X(x2)) / 2, cy - 1, label, 10, "middle", 600))
        if sub:
            o.append(t((X(x1) + X(x2)) / 2, cy + 11, sub, 8.5, "middle", 400, MUTED))
    P_ = g.PLINTH
    (b1a, b1b), (b2a, b2b), (b3a, b3b) = g.BAYS
    o.append(f'<rect x="{X(0)}" y="{Y(P_)}" width="{b2b*s}" height="{P_*s}" fill="#efece6" stroke="#bdb8ad"/>')
    o.append(t(X(b2b / 2), Y(P_) + 13, "9 cm plinth (face frame covers it)", 8.5, "middle", 400, MUTED))
    i1, i2 = b1a + 1.6, b1b - 1.6
    cell(i1, i2, P_ + 46.4, P_ + 62.4, "Xbox One + brick", "16 row", "g")
    cell(i1, i2, P_ + 28.6, P_ + 44.6, "Xbox 360 + brick", "16 row", "g")
    cell(i1, i2, P_ + 1.6, P_ + 26.8, "Game drawer", "~48 games", "g")
    i1, i2 = b2a + 1.6, b2b - 1.6
    cell(i1, i2, P_ + 38.7, P_ + 62.4, "PS3 + controllers", "23.7 row", "g")
    cell(i1, i2, P_ + 20.4, P_ + 36.9, "PS2 + HDMI switch", "16.5 row", "g")
    cell(i1, i2, P_ + 1.6, P_ + 18.6, "PS1 + RetroTINK", "17 row", "g")
    i1, i2 = b3a + 1.8, b3b - 1.8
    cell(i1, i2, 65.6, 73, "hidden drawer", None, "v")
    cell(i1, i2, 40.8, 65.6, "Shelf", "pad dock, 6-way", "n")
    o.append(rect(X(i1), Y(40.8), (i2 - i1) * s, 1.8 * s, "#e9dccb", "#c9b79f", 1))
    cxs = (b3a + b3b) / 2
    o.append(rect(X(cxs - 15), Y(6.8), 30 * s, 5 * s, SND_F, SND_S, 2))
    o.append(rect(X(cxs - 10.7), Y(36.2), 21.4 * s, 29.4 * s, SND_F, SND_S, 4))
    o.append(f'<circle cx="{X(cxs)}" cy="{Y(21.5)}" r="{7.5*s}" fill="none" stroke="{SND_S}" stroke-width="1.2"/>')
    o.append(t(X(cxs), Y(21.5) + 3, "sub", 9.5, "middle", 600))
    for a in (b1a, b2a):
        o.append(f'<rect x="{X(a)}" y="{Y(73)}" width="{60*s}" height="{64*s}" fill="none" stroke="#8f8a80" stroke-width="1.3"/>')
    o.append(f'<rect x="{X(b3a)}" y="{Y(73)}" width="{60*s}" height="{73*s}" fill="none" stroke="#8f8a80" stroke-width="1.3"/>')
    for a, b, lab in [(b1a, b1b, "60 · BESTÅ"), (b2a, b2b, "60 · BESTÅ"), (b3a, b3b, "60 · ply, sub")]:
        o.append(t((X(a) + X(b)) / 2, oy + 16, lab, 9.5, "middle", 400, MUTED))
    # the vinyl cabinet
    (xa0, xa1), (xb0, xb1) = g.CAB_BAY_A, g.CAB_BAY_B
    o.append(rect(X(xa0), Y(g.CAB_TOP), (xb1 - xa0) * s, 3 * s, "#e9dccb", "#c9b79f", 1))
    cell(xa0 + 1.8, xa1 - 1.8, 37.0, 71.2, "Upper record tray", "~90 LPs + ~120 singles", "v")
    cell(xa0 + 1.8, xa1 - 1.8, 1.8, 35.0, "Lower record tray", "~90 LPs + ~120 singles", "v")
    cell(xb0 + 1.8, xb1 - 1.8, 37.0, 71.2, "Cubby", "preamp, kit", "v")
    cell(xb0 + 1.8, xb1 - 1.8, 1.8, 35.0, "Singles", "~110 face-out", "v")
    for a, b in ((xa0, xa1), (xb0, xb1)):
        o.append(f'<rect x="{X(a)}" y="{Y(73)}" width="{(b-a)*s}" height="{73*s}" fill="none" stroke="#8f8a80" stroke-width="1.3"/>')
    o.append(t((X(xa0) + X(xa1)) / 2, oy + 16, "60 · trays", 9.5, "middle", 400, MUTED))
    o.append(t((X(xb0) + X(xb1)) / 2, oy + 16, "40", 9.5, "middle", 400, MUTED))
    o.append(t((X(xb1) + X(g.BREAST_X[1])) / 2, oy + 16, _fmt(g.DOOR_CLEAR), 9.5, "middle", 400, MUTED))
    o.append(rect(X(g.BROWSER_X[0]), Y(g.CAB_TOP + 32.5), g.BROWSER[0] * s, 32.5 * s, VIN_F, VIN_S, 3))
    o.append(t(X(g.BROWSER_X[0] + 22), Y(g.CAB_TOP + 18), "LP browser", 9.5, "middle", 600))
    o.append(t(X(g.BROWSER_X[0] + 22), Y(g.CAB_TOP + 18) + 11, "~50 face-out", 8.5, "middle", 400, MUTED))
    o.append(rect(X(g.DECK_X[0]), Y(g.CAB_TOP + g.DECK[1]), g.DECK[0] * s, g.DECK[1] * s, VIN_F, VIN_S, 3))
    o.append(t(X(g.DECK_X[0] + g.DECK[0] / 2), Y(g.CAB_TOP + 5), "Turntable", 9.5, "middle", 600))
    o.append(f'<rect x="{X(g.DECK_X[0])}" y="{Y(g.LID_CLEAR_TO)}" width="{g.DECK[0]*s}" height="{(g.LID_CLEAR_TO-g.CAB_TOP-g.DECK[1])*s}" fill="none" stroke="#b9b4a8" stroke-dasharray="4 3"/>')
    o.append(t(X(g.DECK_X[0] + g.DECK[0] / 2), Y(118), "lid clear", 9, "middle", 400, MUTED))
    cxc = (g.CAB_X[0] + g.CAB_X[1]) / 2
    for i in range(2):
        x0 = cxc - 4 - 34 + i * 42
        o.append(rect(X(x0), Y(184), 34 * s, 34 * s, "#fff", "#8f8a80", 1))
    o.append(t(X(cxc), Y(192), "framed LPs", 9.5, "middle", 400, MUTED))
    # the socket on the side wall (shown just outside the alcove)
    o.append(f'<rect x="{X(-6)}" y="{Y(34.3)}" width="{3.5*s}" height="{8.6*s}" rx="1" fill="#fff" stroke="#d0573b" stroke-width="1.3"/>')
    o.append(t(X(-8), Y(42), "double socket", 8.5, "end", 600, "#d0573b"))
    o.append(t(X(-8), Y(42) + 10, "on the side wall", 8.5, "end", 600, "#d0573b"))
    ly = H - 12
    for i, (lab, f, st) in enumerate([("Gaming", GAME_F, GAME_S), ("Vinyl", VIN_F, VIN_S), ("Sound", SND_F, SND_S)]):
        o.append(rect(i * 100, ly - 11, 14, 14, f, st, 3)); o.append(t(i * 100 + 20, ly + 1, lab, 11, "start", 400, MUTED))
    o.append(f'<line x1="300" y1="{ly-4}" x2="326" y2="{ly-4}" stroke="#b9b4a8" stroke-dasharray="4 3"/>')
    o.append(t(332, ly + 1, "keep clear / hidden", 11, "start", 400, MUTED))
    return svg(W, H, "\n".join(o), "The media wall from the front, to scale",
               "Oak uprights and pegged shelves above a 186 cm base in the alcove; the vinyl cabinet stands against the chimney breast. Heights in cm")


# ------------------------------------------------------------------ record drawers detail
def drawer():
    import math
    W, H = 860, 590
    o = []
    s = 5.0
    ox, oy = 268, 520
    Z = lambda cm: ox + cm * s
    Y = lambda cm: oy - cm * s
    o.append(t(0, 62, "Side section through bay A", 12, "start", 600))
    o.append(f'<line x1="{Z(-36)}" y1="{oy}" x2="{Z(52)}" y2="{oy}" stroke="#b9b4a8" stroke-width="1.4"/>')
    o.append(f'<rect x="{Z(44)}" y="{Y(86)}" width="12" height="{86*s}" fill="#e4ddd0"/>')
    o.append(t(Z(44) + 16, Y(84), "chimney", 10, "start", 400, MUTED))
    o.append(t(Z(44) + 16, Y(84) + 12, "breast", 10, "start", 400, MUTED))
    o.append(t(Z(41.5), Y(60), "2 cm", 9, "middle", 400, MUTED))
    o.append(t(Z(41.5), Y(60) + 11, "cable gap", 9, "middle", 400, MUTED))
    o.append(f'<rect x="{Z(0)}" y="{Y(73)}" width="{40*s}" height="{1.8*s}" fill="#efe2c8" stroke="#c9a77a"/>')
    o.append(f'<rect x="{Z(0)}" y="{Y(1.8)}" width="{40*s}" height="{1.8*s}" fill="#efe2c8" stroke="#c9a77a"/>')
    o.append(f'<rect x="{Z(0)}" y="{Y(73)}" width="{40*s}" height="{73*s}" fill="none" stroke="#8f8a80" stroke-width="1.3"/>')
    o.append(f'<rect x="{Z(-2)}" y="{Y(76)}" width="{44*s}" height="{3*s}" fill="#e9dccb" stroke="#c9b79f"/>')
    o.append(t(Z(20), Y(76) - 5, "oak top 3, at 76, level with the alcove worktop", 9.5, "middle", 500))
    lean = math.radians(10); hgt = 31.4 * math.cos(lean); dzl = 31.4 * math.sin(lean)
    def tier(yb, ghost=0.0):
        oz = -ghost
        op = 0.55 if ghost else 1
        da = 'stroke-dasharray="4 3"' if ghost else ""
        o.append(f'<rect x="{Z(oz)}" y="{Y(yb + 12)}" width="{40*s}" height="{12*s}" fill="none" stroke="#c9a77a" stroke-width="0.9" opacity="{op}" {da}/>')
        o.append(f'<rect x="{Z(oz)}" y="{Y(yb + 1.2)}" width="{40*s}" height="{1.2*s}" fill="#f1dfc4" stroke="#c9a77a" opacity="{op}"/>')
        for i in range(11):
            zb = oz + 2.6 + i * 2.6
            o.append(f'<line x1="{Z(zb)}" y1="{Y(yb + 1.2)}" x2="{Z(zb + dzl)}" y2="{Y(yb + 1.2 + hgt)}" stroke="{VIN_S}" stroke-width="{2.4 if i == 0 else 1.1}" opacity="{op}"/>')
        o.append(f'<rect x="{Z(oz - 0.6)}" y="{Y(yb + 5.0)}" width="{1.5*s}" height="{5.0*s}" fill="#e9c9a4" stroke="{VIN_S}" opacity="{op}"/>')
    tier(2.3); tier(37.0); tier(37.0, ghost=30)
    o.append(t(Z(-12), Y(37 + 36), "pulls out 30+ cm", 10, "middle", 600, VIN_S))
    o.append(t(Z(21), Y(20), "~90 LPs face-out,", 10.5, "middle", 650))
    o.append(t(Z(21), Y(20) + 13, "leaning back 10°", 10, "middle", 400, MUTED))
    xx = Z(-27)
    o.append(f'<line x1="{xx}" y1="{Y(0)}" x2="{xx}" y2="{Y(76)}" stroke="#cfcabf"/>')
    for h in (0, 3.5, 34.4, 38.2, 69.1, 76):
        o.append(f'<line x1="{xx - 4}" y1="{Y(h)}" x2="{xx + 4}" y2="{Y(h)}" stroke="#9a958b"/>')
    for h, lab, dy in [(0, "0 floor", 4), (3.5, "3.5 lower base", -1), (34.4, "34.4 sleeves", 9), (38.2, "38.2 upper base", -2), (69.1, "69.1 sleeves", 9), (76, "76 top", 0)]:
        o.append(t(xx - 7, Y(h) + dy, lab, 9, "end", 400, MUTED))
    o.append(t(Z(18), oy + 18, "carcass 18 mm birch ply, 60 × 40 × 73, back open · trays 40 deep on 400 mm runners", 10, "middle", 400, MUTED))
    o.append(t(Z(18), oy + 32, "12 mm base, 9 mm sides, 5 cm oak lip · 2.6 and 2.1 cm finger room (top panel at 71.2)", 10, "middle", 400, MUTED))
    k = 4.5
    px0, py0 = 588, 110
    PX = lambda c: px0 + c * k
    PY = lambda c: py0 + (40 - c) * k
    o.append(t(px0 - 20, 62, "Top view of one tray", 12, "start", 600))
    o.append(f'<rect x="{PX(-1.25)}" y="{PY(40)}" width="{56.4*k}" height="{40*k}" fill="none" stroke="#8f8a80" stroke-width="1.3"/>')
    o.append(t(PX(26.95), PY(40) - 8, "ply carcass, 56.4 cm inside", 10, "middle", 400, MUTED))
    for x0_ in (-1.25, 53.9):
        o.append(f'<rect x="{PX(x0_)}" y="{PY(39.5)}" width="{1.25*k}" height="{39.5*k}" fill="#e4e4e4" stroke="#999" stroke-width="0.8"/>')
    o.append(f'<rect x="{PX(0)}" y="{PY(40)}" width="{53.9*k}" height="{40*k}" fill="{VIN_F}" stroke="{VIN_S}"/>')
    o.append(f'<rect x="{PX(0.9)}" y="{PY(39.1)}" width="{52.1*k}" height="{38.2*k}" fill="#fff7f1" stroke="{VIN_S}" stroke-opacity="0.4"/>')
    for i in range(26):
        zz = 2.6 + i * 1.2
        o.append(f'<rect x="{PX(1.5)}" y="{PY(zz + 0.4)}" width="{31.4*k}" height="{0.5*k}" fill="{VIN_S}" opacity="{0.75 - i*0.02}"/>')
    o.append(f'<rect x="{PX(33.5)}" y="{PY(39.1)}" width="{0.6*k}" height="{38.2*k}" fill="#c48c57"/>')
    for i in range(30):
        zz = 2.6 + i * 1.1
        o.append(f'<rect x="{PX(34.4)}" y="{PY(zz + 0.3)}" width="{18.3*k}" height="{0.4*k}" fill="#6f86a8" opacity="{0.8 - i*0.015}"/>')
    o.append(t(PX(17.2), PY(22), "LP trough 32.6", 11, "middle", 650))
    o.append(t(PX(17.2), PY(22) + 13, "~90 face-out", 10, "middle", 400, MUTED))
    o.append(t(PX(43.5), PY(22), "singles 18.9", 10.5, "middle", 650))
    o.append(t(PX(43.5), PY(22) + 13, "~120 face-out", 10, "middle", 400, MUTED))
    o.append(f'<rect x="{PX(-1.45)}" y="{PY(0)}" width="{56.8*k}" height="{1.5*k}" fill="#e9c9a4" stroke="{VIN_S}"/>')
    o.append(t(PX(26.95), PY(0) + 26, "tray 53.9 × 40 outside, 52.1 × 38.2 inside", 10, "middle", 400, MUTED))
    o.append(t(PX(26.95), PY(0) + 40, "9 mm sides · 6 mm oak divider · 5 cm oak lip", 10, "middle", 400, MUTED))
    o.append(t(PX(26.95), PY(0) + 54, "about 32 kg full: open one tray at a time", 10, "middle", 500, VIN_S))
    return svg(W, H, "\n".join(o), "The record trays: every LP and single face-out, two tiers in the vinyl cabinet",
               "Bay A of the oak cabinet on the chimney breast. Section left, plan right. Pull a tray and flip through the covers like a record shop browser")


def sound():
    W, H = 760, 540
    o = []
    rx, ry, rw, rh = 10, 150, 740, 375
    o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" fill="#fff" stroke="{LINE}" stroke-width="1.4"/>')
    # south wall at the top: the alcove (right as you face it = left on this plan? no: east is right on a plan with north at the bottom)
    o.append(t(rx + 4, ry - 66, "Media wall (south)", 10.5, "start", 500, MUTED))
    ax0 = rx + rw - 230
    o.append(f'<rect x="{ax0}" y="{ry-40}" width="230" height="40" fill="#fbfbfa" stroke="{LINE}" stroke-width="1.4"/>')
    o.append(f'<rect x="{ax0-146}" y="{ry-6}" width="146" height="6" fill="#ece7dc" stroke="{LINE}"/>')
    o.append(t(ax0 - 73, ry - 12, "chimney breast", 9.5, "middle", 400, MUTED))
    o.append(rect(ax0 - 124, ry, 124, 52, VIN_F, VIN_S, 3))
    o.append(t(ax0 - 62, ry + 30, "vinyl cabinet", 10, "middle", 600))
    o.append(f'<rect x="{ax0+35}" y="{ry-20}" width="152" height="5" fill="{INK}"/>')
    o.append(rect(ax0 + 54, ry - 10, 114, 8, SND_F, SND_S, 2))
    o.append(rect(ax0 + 158, ry - 34, 26, 26, SND_F, SND_S, 4))
    o.append(t(ax0 + 115, ry - 46, "TV + soundbar", 10.5, "middle", 500, MUTED))
    o.append(t(ax0 + 225, ry + 96, "sub in bay 3, under the TV", 10.5, "end", 600))
    o.append(wire([(ax0 + 171, ry - 8), (ax0 + 171, ry + 70)], BLUE, 2))
    o.append(f'<path d="M{ax0+165},{ry+64} L{ax0+171},{ry+76} L{ax0+177},{ry+64}Z" fill="{BLUE}"/>')
    o.append(t(ax0 + 140, ry + 60, "faces the sofa", 10, "end", 400, MUTED))
    # door + stairs at the west end
    o.append(t(rx + 120, ry + 26, "Door", 11, "middle", 400, MUTED))
    o.append(f'<path d="M{rx+80},{ry} A 70 70 0 0 0 {rx+150},{ry+70}" fill="none" stroke="#c9c5bb" stroke-dasharray="4 3"/>')
    for i in range(4):
        o.append(f'<rect x="{rx+i*16}" y="{ry}" width="16" height="44" fill="none" stroke="#dcd8cf"/>')
    o.append(t(rx + 34, ry + 60, "stair box", 9.5, "middle", 400, MUTED))
    # PC shelf on the east wall
    o.append(f'<rect x="{rx+rw-10}" y="{ry+120}" width="10" height="56" fill="#eceae4" stroke="{LINE}"/>')
    o.append(t(rx + rw - 16, ry + 152, "PC shelf", 10.5, "end", 400, MUTED))
    # sofa + rears against the window wall (north, bottom)
    sx0 = ax0 + 111 - 85
    o.append(rect(sx0, ry + rh - 62, 170, 52, "#fbfbfa", "#c9c5bb", 12))
    o.append(t(sx0 + 85, ry + rh - 31, "Sofa", 12, "middle", 650))
    o.append(rect(sx0 - 34, ry + rh - 56, 22, 22, SND_F, SND_S, 4))
    o.append(rect(sx0 + 180, ry + rh - 56, 22, 22, SND_F, SND_S, 4))
    o.append(t(sx0 - 23, ry + rh - 62, "Rear", 10.5, "middle", 400, MUTED))
    o.append(t(sx0 + 191, ry + rh - 62, "Rear", 10.5, "middle", 400, MUTED))
    o.append(wire([(sx0 - 23, ry + rh - 34), (sx0 - 23, ry + rh - 6), (sx0 + 191, ry + rh - 6), (sx0 + 191, ry + rh - 34)], VIN_S, 1.6, "5 3"))
    o.append(t(sx0 + 60, ry + rh + 12, "speaker link cable behind the sofa, along the skirting", 10, "middle", 500, VIN_S))
    o.append(t(rx + 4, ry + rh + 12, "Window wall (north)", 10.5, "start", 500, MUTED))
    o.append(wire([(ax0 + 115, ry + 6), (ax0 + 115, ry + rh - 70)], "#d0ccc2", 1, "4 4"))
    o.append(t(ax0 + 108, ry + 170, "about 2.65 m eyes to screen", 10.5, "end", 400, MUTED))
    o.append(f'<path d="M{ax0+115},{ry-8} Q {sx0-60},{ry+150} {sx0-24},{ry+rh-60}" fill="none" stroke="{SND_S}" stroke-dasharray="1 5" stroke-width="2" stroke-linecap="round"/>')
    o.append(t(sx0 - 50, ry + 160, "wireless", 9.5, "end", 400, SND_S))
    return svg(W, H, "\n".join(o), "The sub fires down the room at the sofa",
               "From above, not to scale, media wall at the top. The sub sits in bay 3 under the TV; the rears share one socket and a cable behind the sofa")


def game_drawer():
    import math
    W, H = 860, 590
    o = []
    s = 6.0
    ox, oy = 250, 470
    Z = lambda cm: ox + cm * s
    Y = lambda cm: oy - (cm + 9) * s      # frame stands on the 9 cm plinth
    o.append(t(0, 70, "Side section through bay 1", 12, "start", 600))
    o.append(f'<rect x="{Z(2)}" y="{Y(0)}" width="{36*s}" height="{9*s}" fill="#efe2c8" stroke="#c9a77a"/>')
    o.append(t(Z(20), Y(-4.5) + 4, "9 cm plinth", 10, "middle", 500))
    o.append(f'<line x1="{Z(-34)}" y1="{oy}" x2="{Z(52)}" y2="{oy}" stroke="#b9b4a8" stroke-width="1.4"/>')
    o.append(f'<line x1="{Z(44)}" y1="{oy}" x2="{Z(44)}" y2="{Y(48)}" stroke="#b9b4a8" stroke-width="2"/>')
    o.append(t(Z(44) + 4, Y(44), "wall", 10, "start", 400, MUTED))
    o.append(f'<rect x="{Z(0)}" y="{Y(46)}" width="{40*s}" height="{46*s}" fill="none" stroke="#8f8a80" stroke-width="1.3"/>')
    o.append(f'<rect x="{Z(1)}" y="{Y(28.6)}" width="{36*s}" height="{1.8*s}" fill="#e7e2d6" stroke="#bdb8ad"/>')
    o.append(rect(Z(6), Y(36.9), 25.8 * s, 8.3 * s, GAME_F, GAME_S, 3))
    o.append(t(Z(19), Y(33.6), "Xbox 360 above (16 cm row)", 10, "middle", 500))
    o.append(f'<rect x="{Z(0)}" y="{Y(1.6)}" width="{40*s}" height="{1.6*s}" fill="#e7e2d6" stroke="#bdb8ad"/>')
    # drawer box 35 deep
    o.append(f'<rect x="{Z(0)}" y="{Y(18.1)}" width="{35*s}" height="{15.5*s}" fill="none" stroke="#c9a77a" stroke-width="1.2"/>')
    o.append(f'<rect x="{Z(0)}" y="{Y(3.5)}" width="{35*s}" height="{0.9*s}" fill="#f1dfc4" stroke="#c9a77a"/>')
    o.append(f'<rect x="{Z(1)}" y="{Y(11)}" width="{33*s}" height="{3.5*s}" fill="none" stroke="#7a7a7a" stroke-dasharray="3 2"/>')
    o.append(f'<rect x="{Z(-0.6)}" y="{Y(9.1)}" width="{2*s}" height="{6.5*s}" fill="#e9c9a4" stroke="{VIN_S}"/>')
    lean = math.radians(13); hgt = 19 * math.cos(lean); dzl = 19 * math.sin(lean)
    for i in range(6):
        zb = 2.4 + i * 1.45
        o.append(f'<line x1="{Z(zb)}" y1="{Y(3.5)}" x2="{Z(zb + dzl)}" y2="{Y(3.5 + hgt)}" stroke="{GAME_S}" stroke-width="{2.2 if i == 0 else 1.2}"/>')
    o.append(f'<rect x="{Z(14.2)}" y="{Y(12.5)}" width="{0.6*s}" height="{9*s}" fill="#e9c9a4" stroke="#c9a77a"/>')
    o.append(f'<rect x="{Z(14.9)}" y="{Y(17)}" width="{19*s}" height="{13.5*s}" fill="{GAME_F}" stroke="{GAME_S}"/>')
    o.append(f'<rect x="{Z(14.9)}" y="{Y(17)}" width="{19*s}" height="{1.4*s}" fill="{GAME_S}"/>')
    o.append(t(Z(24.4), Y(10.5), "case on its edge,", 10, "middle", 500))
    o.append(t(Z(24.4), Y(10.5) + 13, "spine (title) on top", 10, "middle", 400, MUTED))
    o.append(t(Z(24.4), Y(17) - 6, "you read here", 10, "middle", 600, GAME_S))
    o.append(t(Z(-13), Y(13), "display bin:", 10, "middle", 600))
    o.append(t(Z(-13), Y(13) + 12, "covers face out", 9.5, "middle", 400, MUTED))
    # ghost pulled out
    o.append(f'<rect x="{Z(-30)}" y="{Y(18.1)}" width="{35*s}" height="{15.5*s}" fill="none" stroke="{GAME_S}" stroke-dasharray="4 3" opacity="0.6"/>')
    o.append(t(Z(-24), Y(18.1) - 6, "rolls out 30 cm", 10, "middle", 600, GAME_S))
    o.append(f'<line x1="{Z(-3)}" y1="{Y(1.6)}" x2="{Z(-3)}" y2="{Y(26.8)}" stroke="{MUTED}" stroke-width="1"/>')
    o.append(t(Z(-4), Y(24), "25.2 cm", 10, "end", 400, MUTED))
    o.append(t(Z(-4), Y(24) + 12, "row", 10, "end", 400, MUTED))
    o.append(t(Z(-4), Y(24) + 26, "base 11.6", 10, "end", 400, MUTED))
    o.append(t(Z(-4), Y(24) + 38, "from floor", 10, "end", 400, MUTED))
    o.append(t(Z(18), oy + 18, "box 35 cm deep on 350 mm full-extension soft-close runners", 10, "middle", 400, MUTED))
    o.append(t(Z(18), oy + 32, "5 cm free behind the box, then the 4 cm cable channel", 10, "middle", 400, MUTED))
    o.append(t(Z(18), oy + 46, "bins: 19 cm cases leaning 13°, about 18.5 cm tall", 10, "middle", 400, MUTED))
    # plan view
    k = 5.2
    px0, py0 = 548, 112
    PX = lambda c: px0 + c * k
    PY = lambda c: py0 + (35 - c) * k
    o.append(t(px0 - 20, 70, "Top view, drawer pulled out", 12, "start", 600))
    o.append(f'<rect x="{PX(0)}" y="{PY(35)}" width="{54.3*k}" height="{35*k}" fill="#f1dfc4" stroke="#c9a77a"/>')
    o.append(f'<rect x="{PX(1.2)}" y="{PY(33.8)}" width="{51.9*k}" height="{32.6*k}" fill="#fbfaf7" stroke="#e6e3dc"/>')
    x = 1.5
    for kind, n, tt, ln, f, st in [("PS2", 15, 1.4, 19, "#dfe6f7", "#3a5fb8"), ("360", 12, 1.4, 19, "#e3f3e2", "#3f9a4c"),
                                    ("f", 1, 2.0, 19, "#e9c9a4", VIN_S), ("One", 9, 1.2, 17, "#d7efdc", "#2a7c3f")]:
        x0 = x
        for i in range(n):
            o.append(f'<rect x="{PX(x)}" y="{PY(14.9+ln)}" width="{tt*k}" height="{ln*k}" fill="{f}" stroke="{st}" stroke-width="0.7"/>')
            x += tt + (0.1 if kind == "f" else 0)
        if kind != "f":
            o.append(t((PX(x0) + PX(x)) / 2, PY(14.9 + ln) - 6, kind, 10.5, "middle", 600))
    o.append(t(PX(36.4), PY(14.9) + 26, "", 1))
    o.append(f'<rect x="{PX(1.2)}" y="{PY(14.8)}" width="{51.9*k}" height="{0.6*k}" fill="#e9c9a4"/>')
    for (a, b, lab) in [(1.2, 17.2, "Xbox bin"), (37.1, 53.1, "PS2 bin")]:
        o.append(f'<rect x="{PX(a)}" y="{PY(14.2)}" width="{(b-a)*k}" height="{12.6*k}" fill="{GAME_F}" stroke="{GAME_S}" stroke-opacity="0.5"/>')
        o.append(t(PX((a + b) / 2), PY(8.5), lab, 10.5, "middle", 600))
        o.append(t(PX((a + b) / 2), PY(8.5) + 12, "6 face out", 9.5, "middle", 400, MUTED))
    o.append(t(PX(27.15), PY(8.5), "tray", 10.5, "middle", 600))
    o.append(t(PX(27.15), PY(8.5) + 12, "cards, pads", 9.5, "middle", 400, MUTED))
    o.append(f'<rect x="{PX(-1.3)}" y="{PY(1.4)}" width="{56.9*k}" height="{2*k}" fill="#e9c9a4" stroke="{VIN_S}"/>')
    o.append(t(PX(27.15), PY(0) + 24, "front: oak lip with finger pull, matching the record drawer", 10, "middle", 400, MUTED))
    o.append(t(PX(27.15), PY(0) + 38, "back row: 15 PS2 + 12 Xbox 360 + follower block + 9 Xbox One", 10, "middle", 400, MUTED))
    o.append(t(PX(27.15), PY(0) + 52, "box 54.3 × 35 cm outside · 51.9 cm inside · 16 cm bins, 18.7 cm tray", 10, "middle", 400, MUTED))
    return svg(W, H, "\n".join(o), "The game drawer: covers on show at the front, every title readable from above at the back",
               "Bay 1, bottom row. Section left, plan right. Nothing stands behind anything else")


AUD = "#d9822b"

def arrow(x1, y1, x2, y2, col=LINE, w=1.4, dash=None):
    da = f'stroke-dasharray="{dash}"' if dash else ""
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 7 * math.cos(ang), y2 - 7 * math.sin(ang)
    px, py = 3.5 * math.sin(ang), -3.5 * math.cos(ang)
    return (f'<line x1="{x1}" y1="{y1}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="{col}" stroke-width="{w}" {da}/>'
            f'<path d="M{x2},{y2} L{hx+px:.1f},{hy+py:.1f} L{hx-px:.1f},{hy-py:.1f}Z" fill="{col}"/>')


def path_arrow(points, col=LINE, w=1.4, dash=None):
    out = wire(points[:-1] + [points[-1]], col, w, dash)
    (x1, y1), (x2, y2) = points[-2], points[-1]
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 7 * math.cos(ang), y2 - 7 * math.sin(ang)
    px, py = 3.5 * math.sin(ang), -3.5 * math.cos(ang)
    return out + f'<path d="M{x2},{y2} L{hx+px:.1f},{hy+py:.1f} L{hx-px:.1f},{hy-py:.1f}Z" fill="{col}"/>'


def av():
    W, H = 760, 560
    o = []
    G = "#9a958b"
    src = [("PC", None, 70), ("Xbox Series X", None, 112), ("Xbox One", None, 168), ("Xbox 360", None, 206),
           ("PS3", None, 244), ("PS2", "component + optical", 300), ("PS1", "RGB SCART", 348),
           ("Turntable", None, 420), ("Phone", None, 476)]
    for name, sub, y in src:
        o.append(node(0, y - 16, 128, 32, name, sub, bold=(sub is not None)))
    o.append(node(196, 166, 120, 100, "HDMI switch", "5-in-1, auto"))
    o.append(node(196, 300, 120, 62, "RetroTINK", "6X CE"))
    o.append(node(196, 404, 120, 32, "Phono preamp", bold=False))
    o.append(rect(392, 50, 130, 230, "#efeeea", "#d6d2c8", 8))
    o.append(t(457, 150, "LG OLED C6", 12.5, "middle", 650))
    o.append(t(457, 166, "55 in", 10.5, "middle", 400, MUTED))
    for lab, y in [("HDMI 1", 70), ("HDMI 3", 112), ("HDMI 4", 216), ("HDMI 2 eARC", 260)]:
        o.append(t(400, y + 4, lab, 10, "start", 500, MUTED))
    o.append(rect(590, 214, 170, 290, SND_F, SND_S, 8))
    o.append(t(675, 240, "Hisense 5.1 soundbar", 12, "middle", 650))
    o.append(t(675, 255, "+ wireless sub and rears", 10, "middle", 400, MUTED))
    for lab, y in [("HDMI eARC (from TV)", 280), ("Optical in", 318), ("AUX 3.5 mm in", 422), ("Bluetooth", 476)]:
        o.append(t(600, y + 4, lab, 10, "start", 500, INK))
    o.append(t(675, 360, "no HDMI inputs, so", 9.5, "middle", 400, MUTED))
    o.append(t(675, 372, "picture goes via the TV", 9.5, "middle", 400, MUTED))
    # picture paths (grey)
    o.append(arrow(128, 70, 392, 70, G)); o.append(t(260, 64, "4K up to 165 Hz", 10, "middle", 400, MUTED))
    o.append(arrow(128, 112, 392, 112, G)); o.append(t(260, 106, "4K 120 Hz", 10, "middle", 400, MUTED))
    for y in (168, 206, 244):
        o.append(arrow(128, y, 196, y if y != 244 else 244, G))
    o.append(arrow(128, 300, 196, 318, G))
    o.append(arrow(128, 348, 196, 344, G))
    o.append(arrow(256, 300, 256, 266, G)); o.append(t(262, 288, "HDMI", 9.5, "start", 400, MUTED))
    o.append(arrow(316, 216, 392, 216, G))
    o.append(arrow(128, 420, 196, 420, AUD))
    # sound paths (orange)
    o.append(path_arrow([(522, 260), (556, 260), (556, 280), (590, 280)], AUD, 1.8))
    o.append(path_arrow([(128, 292), (160, 292), (160, 284), (370, 284), (370, 318), (590, 318)], AUD, 1.8))
    o.append(t(380, 312, "PS2 optical straight to the soundbar (5.1)", 9.5, "start", 500, AUD))
    o.append(path_arrow([(316, 420), (590, 422)], AUD, 1.8))
    o.append(path_arrow([(128, 476), (590, 476)], AUD, 1.4, "5 4"))
    o.append(t(360, 470, "Bluetooth, phones only", 9.5, "middle", 400, AUD))
    o.append(wire([(0, 540), (28, 540)], G, 1.4)); o.append(t(36, 544, "picture (HDMI, sound travels with it)", 11, "start", 400, MUTED))
    o.append(wire([(300, 540), (328, 540)], AUD, 1.8)); o.append(t(336, 544, "sound straight to the soundbar", 11, "start", 400, MUTED))
    return svg(W, H, "\n".join(o), "Everything sounds through the Hisense: directly where it can, via the TV where it can't",
               "The soundbar has no HDMI inputs, so HDMI sources reach it over eARC; vinyl, PS2 audio and phones go straight in")


def power():
    W, H = 860, 654
    o = []
    # wall socket
    o.append(node(0, 90, 150, 46, "Double socket", "side wall, by bay 1"))
    # 10-gang
    o.append(rect(196, 70, 330, 300, "#fbfaf7", LINE, 8))
    o.append(t(361, 92, "Your 10-gang, behind the TV", 12.5, "middle", 650))
    o.append(t(361, 107, "lying flat; switch ends reachable from the left", 10, "middle", 400, MUTED))
    o.append(rect(206, 120, 152, 238, SND_F, SND_S, 6))
    o.append(t(282, 140, "Side A · leave on", 11, "middle", 650))
    for i, it in enumerate(["LG C6 TV (pixel refresh)", "Soundbar", "Subwoofer", "Xbox Series X", "USB charger (HDMI switch,", "  fan stand, pad dock)"]):
        o.append(t(216, 166 + i * 22, it, 10.5, "start", 400, INK))
    o.append(rect(364, 120, 152, 238, GAME_F, GAME_S, 6))
    o.append(t(440, 140, "Side B · retro switch", 11, "middle", 650))
    for i, it in enumerate(["Xbox One", "Xbox 360", "PS3", "PS2", "PS1", "", "off between sessions"]):
        o.append(t(374, 166 + i * 22, it, 10.5, "start", 400, INK if i < 5 else MUTED))
    # 6-way
    o.append(rect(546, 70, 300, 300, "#fbfaf7", LINE, 8))
    o.append(t(696, 92, "6-way, each socket switched", 12.5, "middle", 650))
    o.append(t(696, 107, "on the shelf in bay 3, over the sub", 10, "middle", 400, MUTED))
    items = [("Deco B (12 V lead in the upright groove)", "always on"), ("8-port switch", "always on"), ("Turntable", "on when playing"),
             ("Phono preamp", "on when playing"), ("RetroTINK USB plug (5 V 2 A)", "with side B"), ("Spare", "")]
    for i, (a, b) in enumerate(items):
        y = 136 + i * 36
        o.append(rect(558, y, 276, 28, VIN_F if i in (2, 3) else (GAME_F if i == 4 else SND_F), LINE, 4))
        o.append(t(568, y + 18, a, 10.5, "start", 500, INK))
        o.append(t(824, y + 18, b, 9.5, "end", 400, MUTED))
    o.append(wire([(150, 113), (175, 113), (175, 220), (196, 220)], VIN_S, 1.8))
    o.append(wire([(150, 120), (165, 120), (165, 386), (696, 386), (696, 370)], VIN_S, 1.8))
    o.append(t(430, 402, "one strip per socket, never one plugged into another", 10, "middle", 500, VIN_S))
    # notes
    notes = ["The socket on the side wall by bay 1 is a single today: swap it for a double, one strip per socket.",
             "PC: its own wall socket by the PC shelf (it can draw 500–850 W); keep it off these strips.",
             "Rear speakers: one socket by the sofa.",
             "The deck and preamp in the vinyl cabinet plug into the 6-way: their leads pass through the back of bay 3 (about 1.5 m).",
             "Load check: side A about 0.6 kW, side B up to about 0.8 kW with a launch PS3 running; well under the 13 A (3 kW) limit.",
             "Check the 10-gang is surge-protected; if not, use a surge-protected one for the TV and consoles.",
             "Label both switch ends: “A: leave on” and “B: retro”."]
    for i, n in enumerate(notes):
        o.append(t(0, 442 + i * 22, "• " + n, 10.5, "start", 400, INK))
    return svg(W, H, "\n".join(o), "Power map: your 10-gang plus one small switched strip",
               "Fifteen things need power; the 10-gang takes ten, a 6-way with individual switches takes the rest")


def routes():
    W, H = 860, 610
    o = []
    s = 1.9
    ox, oy = 236, 560
    X = lambda cm: ox + cm * s
    Y = lambda cm: oy - cm * s
    g = G
    o.append(f'<rect x="{X(0)}" y="{Y(g.CEIL)}" width="{g.ALC_W*s}" height="{g.CEIL*s}" fill="#f8f7f4" stroke="{LINE}"/>')
    o.append(f'<rect x="{X(g.ALC_W)}" y="{Y(g.CEIL)}" width="{g.BREAST_W*s}" height="{g.CEIL*s}" fill="#f1efe9" stroke="{LINE}"/>')
    o.append(f'<line x1="{X(-115)}" y1="{oy}" x2="{X(310)}" y2="{oy}" stroke="#b9b4a8" stroke-width="1.4"/>')
    o.append(rect(X(0), Y(76), g.ALC_W * s, 3 * s, "#e9dccb", "#c9b79f", 1))
    o.append(rect(X(0), Y(73), g.ALC_W * s, 73 * s, "#fbfaf7", "#d6d2c8", 1))
    for a, b in g.BAYS:
        o.append(f'<rect x="{X(a)}" y="{Y(73)}" width="{(b-a)*s}" height="{73*s}" fill="none" stroke="#e2ded5"/>')
    o.append(rect(X(g.CAB_X[0]), Y(76), 100 * s, 76 * s, "#fbf3ec", "#e0c9b4", 1))
    o.append(t(X(g.CAB_X[0] + 50), Y(10), "vinyl cabinet", 9.5, "middle", 600, VIN_S))
    o.append(rect(X(g.TV_X[0]), Y(g.TV_TOP), g.TV_W * s, g.TV_H * s, "#ebeae6", "#c9c5bb", 3))
    o.append(t(X(g.TV_CX), Y(119), "TV", 11, "middle", 600, MUTED))
    o.append(rect(X(0), Y(g.HIGH_TOP), g.ALC_W * s, 4 * s, "#e9dccb", "#c9b79f", 1))
    dxd = g.UP_R[1] + 7
    o.append(rect(X(dxd), Y(g.HIGH_TOP + 11.4), 11 * s, 11.4 * s, "#fff", LINE, 8))
    o.append(t(X(dxd + 5.5), Y(g.HIGH_TOP + 15), "Deco B", 9, "middle", 500))
    for (a, b) in (g.UP_L, g.UP_R):
        o.append(f'<rect x="{X(a)}" y="{Y(g.CEIL)}" width="{g.UP_T*s}" height="{(g.CEIL-76)*s}" fill="#f1e1c8" stroke="#b88a55"/>')
    o.append(rect(X(70), Y(80.5), 56 * s, 4.5 * s, VIN_F, VIN_S, 2))
    o.append(t(X(98), Y(73) + 14, "10-gang", 9.5, "middle", 600, VIN_S))
    b3 = g.BAYS[2]
    o.append(rect(X(b3[0] + 13), Y(45), 34 * s, 4.2 * s, VIN_F, VIN_S, 2))
    o.append(t(X(b3[0] + 30), Y(45) - 4, "6-way", 9.5, "middle", 600, VIN_S))
    o.append(rect(X(g.DECK_X[0]), Y(90.2), g.DECK[0] * s, 14.2 * s, VIN_F, VIN_S, 2))
    o.append(t(X(g.DECK_X[0] + 22), Y(90.2) - 4, "deck", 9.5, "middle", 600, VIN_S))
    o.append(rect(X(g.CAB_BAY_B[0] + 4), Y(42), 11 * s, 4.5 * s, "#fff", VIN_S, 2))
    o.append(t(X(g.CAB_BAY_B[0] + 22), Y(48), "preamp", 9, "middle", 600, VIN_S))
    # PC on the side wall, folded flat
    o.append(f'<line x1="{X(-2)}" y1="{Y(0)}" x2="{X(-2)}" y2="{Y(g.CEIL)}" stroke="#d6d2c8" stroke-dasharray="3 3"/>')
    o.append(t(X(-58), Y(226), "side wall, folded flat", 10, "middle", 400, MUTED))
    o.append(rect(X(-110), Y(110), 65 * s, 4 * s, "#e9dccb", "#c9b79f", 1))
    o.append(rect(X(-103), Y(157), 45 * s, 47 * s, GAME_F, GAME_S, 4))
    o.append(t(X(-80), Y(135), "PC", 11, "middle", 650))
    DATA = BLUE; MAINS = VIN_S; DC = "#2fa47a"; AUD = "#b07a1f"
    o.append(wire([(X(-106), Y(106)), (X(-106), Y(8)), (X(-2), Y(8)), (X(4), Y(8))], DATA, 2.2))
    o.append(t(X(-104), Y(64), "HDMI (active optical)", 9, "start", 500, DATA))
    o.append(t(X(-104), Y(64) + 11, "+ Cat6 down the trunking,", 9, "start", 400, MUTED))
    o.append(t(X(-104), Y(64) + 22, "along the skirting", 9, "start", 400, MUTED))
    gx = g.UP_R[0] + 2.25
    o.append(wire([(X(dxd), Y(g.HIGH_TOP + 2)), (X(gx), Y(g.HIGH_TOP + 2)), (X(gx), Y(76)), (X(b3[0] + 30), Y(45))], DC, 2.2, "6 3"))
    o.append(wire([(X(gx - 1.5), Y(g.HIGH_TOP + 2)), (X(gx - 1.5), Y(76)), (X(b3[0] + 4), Y(6)), (X(100), Y(6))], DATA, 1.6))
    o.append(t(X(g.UP_R[0]) - 4, Y(170), "Deco 12 V lead +", 9, "end", 500, DC))
    o.append(t(X(g.UP_R[0]) - 4, Y(170) + 11, "patch lead to Switch 2,", 9, "end", 500, DATA))
    o.append(t(X(g.UP_R[0]) - 4, Y(170) + 22, "in the groove behind", 9, "end", 400, MUTED))
    o.append(t(X(g.UP_R[0]) - 4, Y(170) + 33, "the right upright", 9, "end", 400, MUTED))
    o.append(wire([(X(g.ALC_W - 2), Y(g.CEIL)), (X(g.ALC_W - 2), Y(g.HIGH_TOP + 14)), (X(dxd + 9), Y(g.HIGH_TOP + 9))], DATA, 1.6))
    o.append(t(X(g.ALC_W + 3), Y(g.CEIL) + 14, "Cat6 in through the ceiling", 9, "start", 500, DATA))
    # vinyl audio: deck -> preamp -> back of cabinet -> bay 3 -> channel -> soundbar AUX
    o.append(wire([(X(g.DECK_X[0] + 30), Y(76)), (X(g.DECK_X[0] + 30), Y(60)), (X(g.CAB_BAY_B[0] + 10), Y(46))], AUD, 1.8))
    o.append(wire([(X(g.CAB_BAY_B[0] + 6), Y(40)), (X(g.CAB_BAY_B[0] + 6), Y(24)), (X(b3[1] - 6), Y(24)), (X(118), Y(70)), (X(118), Y(78)), (X(g.TV_CX + 40), Y(80))], AUD, 1.8))
    o.append(t(X(g.CAB_X[0] + 52), Y(28), "preamp → soundbar AUX", 9, "middle", 500, AUD))
    o.append(rect(X(-14), Y(34.3), 8 * s, 8.6 * s, "#fff", MAINS, 2))
    o.append(t(X(-10), Y(34.3) - 4, "socket", 9, "middle", 600, MAINS))
    o.append(wire([(X(-10), Y(25.7)), (X(-10), Y(3)), (X(100), Y(3)), (X(100), Y(76))], MAINS, 1.8))
    o.append(wire([(X(100), Y(3)), (X(b3[0] + 30), Y(3)), (X(b3[0] + 30), Y(41))], MAINS, 1.8))
    o.append(wire([(X(b3[0] + 47), Y(43)), (X(g.CAB_BAY_B[0] + 2), Y(20)), (X(g.CAB_BAY_B[0] + 2), Y(74)), (X(g.DECK_X[0] + 36), Y(77))], MAINS, 1.4))
    for x in (30, 90):
        o.append(wire([(X(x), Y(58)), (X(x), Y(72)), (X(x + 40) if x == 30 else X(96), Y(76))], MAINS, 1.2))
    for i, (c, lab, d) in enumerate([(DATA, "HDMI / Cat6", None), (MAINS, "mains leads", None), (DC, "12 V DC lead", "6 3"), (AUD, "vinyl audio", None)]):
        o.append(wire([(i * 210, 600), (i * 210 + 28, 600)], c, 2.2, d)); o.append(t(i * 210 + 36, 604, lab, 10.5, "start", 400, MUTED))
    return svg(W, H + 10, "\n".join(o), "Cable routes: everything ends in the channel behind the base",
               "Front view, schematic. The side wall is folded flat so the PC's route shows; the vinyl cabinet's leads pass through the back of bay 3")


def pc_shelf():
    W, H = 860, 470
    o = []
    s = 3.8
    # plan view (from above). Wall on the left, north (alcove) at the top.
    ox, oy = 110, 90
    X = lambda cm: ox + cm * s          # distance from the wall
    Y = lambda cm: oy + cm * s          # distance from the north end of the shelf
    o.append(t(0, 70, "From above", 12, "start", 600))
    o.append(f'<line x1="{X(0)}" y1="{Y(-8)}" x2="{X(0)}" y2="{Y(76)}" stroke="#8f8a80" stroke-width="3"/>')
    o.append(t(X(-2), Y(-2), "left wall", 10, "end", 400, MUTED))
    o.append(t(X(16), Y(-4), "↑ alcove / TV", 10, "middle", 500, MUTED))
    o.append(t(X(16), Y(74), "↓ sofa", 10, "middle", 500, MUTED))
    o.append(rect(X(0), Y(0), 32 * s, 65 * s, "#f1e4d2", "#c9a77a", 2))
    o.append(rect(X(4.5), Y(5), 23 * s, 45 * s, GAME_F, GAME_S, 3))
    o.append(t(X(16), Y(20), "PC", 12, "middle", 650))
    o.append(t(X(16), Y(20) + 14, "front faces", 9.5, "middle", 400, MUTED))
    o.append(t(X(16), Y(20) + 26, "the alcove", 9.5, "middle", 400, MUTED))
    o.append(f'<line x1="{X(27.5)}" y1="{Y(5)}" x2="{X(27.5)}" y2="{Y(50)}" stroke="#2fa47a" stroke-width="4"/>')
    o.append(t(X(30), Y(28), "glass", 9.5, "start", 600, "#2fa47a"))
    o.append(t(X(30), Y(28) + 11, "to room", 9.5, "start", 400, MUTED))
    o.append(rect(X(3), Y(63.5), 26 * s, 1.5 * s, "#d9b48a", VIN_S, 1))
    o.append(t(X(16), Y(68), "slatted screen, open top", 9.5, "middle", 500, VIN_S))
    o.append(arrow(X(12), Y(51), X(12), Y(61), "#c0574a", 1.6))
    o.append(t(X(14), Y(57), "exhaust", 9, "start", 400, "#c0574a"))
    o.append(rect(X(0.3), Y(55), 5 * s, 8 * s, "#fff", INK, 1, 1.2, 'stroke-dasharray="3 2"'))
    o.append(t(X(-1), Y(58), "cable", 9.5, "end", 500, BLUE))
    o.append(t(X(-1), Y(58) + 11, "notch", 9.5, "end", 500, BLUE))
    o.append(rect(X(32), Y(3), 25 * s, 58 * s, "none", "#9a958b", 1, 1.2, 'stroke-dasharray="5 4"'))
    o.append(t(X(44.5), Y(32), "tray pulled", 9.5, "middle", 500, MUTED))
    o.append(t(X(44.5), Y(32) + 11, "out 25 cm", 9.5, "middle", 400, MUTED))
    o.append(t(X(16), Y(80), "shelf 65 × 32 · case 45 deep · 13 cm air behind it", 10, "middle", 400, MUTED))
    # elevation (looking at the left wall from the room): north on the right
    ex, ey = 520, 400
    E = lambda cm: ex + (65 - cm) * 4.4
    V = lambda cm: ey - (cm - 90) * 4.4 if cm >= 90 else ey + (90 - cm) * 0.9
    o.append(t(ex, 70, "From the room (side view)", 12, "start", 600))
    o.append(rect(E(65), V(110), 65 * 4.4, 4 * 4.4, "#e9dccb", "#c9b79f", 1))
    o.append(rect(E(53), V(106), 52 * 4.4, 6.5 * 4.4, "#f1e4d2", "#c9a77a", 1))
    o.append(t((E(53) + E(1)) / 2, V(106) + 18, "keyboard + mouse tray (rolls out towards you)", 9.5, "middle", 500))
    o.append(rect(E(50), V(157), 45 * 4.4, 47 * 4.4, GAME_F, GAME_S, 3))
    o.append(t((E(50) + E(5)) / 2, V(135), "PC, glass side", 11, "middle", 650))
    o.append(rect(E(65), V(158), 1.5 * 4.4, 48 * 4.4, "#d9b48a", VIN_S, 1))
    o.append(t(E(65) - 4, V(150), "screen", 9.5, "end", 500, VIN_S))
    o.append(t(E(0) + 4, V(150), "→ alcove", 9.5, "start", 500, MUTED))
    o.append(rect(E(62), V(99.5), 4 * 4.4, 89.5 * 0.9, "#cfe0f7", BLUE, 1))
    o.append(t(E(62) + 22, V(60), "trunking from the notch down to the skirting, painted green", 9.5, "start", 500, BLUE))
    o.append(t(E(0) + 4, V(110) + 5, "110", 9.5, "start", 400, MUTED))
    o.append(t(E(0) + 4, V(157) + 5, "157", 9.5, "start", 400, MUTED))
    return svg(W, H, "\n".join(o), "The PC shelf: glass to the room, ports and cables screened from the sofa",
               "A standard case has its window on the left, so with the glass facing the room the back ports face the sofa")


def section():
    """A: through the middle of the alcove. B: through the vinyl cabinet. Both to scale, room on the left."""
    W, H = 860, 710
    o = []
    s = 2.3
    g = G
    oy = 650
    Y = lambda cm: oy - cm * s
    # ---- A: through the alcove at the TV's centre line
    ox = 742
    Z = lambda cm: ox - cm * s      # cm in front of the alcove's back wall
    o.append(t(Z(150), 76, "A · Through the middle of the alcove", 12, "start", 600))
    o.append(f'<line x1="{Z(-6)}" y1="{Y(0)}" x2="{Z(150)}" y2="{Y(0)}" stroke="#8f8a80" stroke-width="1.6"/>')
    o.append(f'<line x1="{Z(-6)}" y1="{Y(g.CEIL)}" x2="{Z(150)}" y2="{Y(g.CEIL)}" stroke="#8f8a80" stroke-width="1.6"/>')
    o.append(f'<rect x="{Z(0)}" y="{Y(g.CEIL)}" width="14" height="{g.CEIL*s}" fill="#dcd8cf"/>')
    o.append(t(Z(0) + 18, Y(120), "back wall", 9.5, "start", 400, MUTED))
    o.append(f'<line x1="{Z(g.ALC_D)}" y1="{Y(0)}" x2="{Z(g.ALC_D)}" y2="{Y(g.CEIL)}" stroke="#c9b6a4" stroke-dasharray="6 4"/>')
    o.append(t(Z(g.ALC_D) - 3, Y(g.CEIL) + 14, f"breast face, {_fmt(g.ALC_D)} out", 9, "end", 500, "#9a7b62"))
    o.append(t(Z(150), Y(g.CEIL) - 6, f"ceiling {_fmt(g.CEIL)}", 9.5, "start", 400, MUTED))
    o.append(f'<rect x="{Z(g.UP_D)}" y="{Y(g.CEIL)}" width="{g.UP_D*s}" height="{(g.CEIL-g.WORKTOP)*s}" fill="#f1e1c8" stroke="#b88a55" stroke-dasharray="5 3"/>')
    o.append(t(Z(15), Y(176), "oak upright", 9.5, "middle", 600, "#9c6a3f"))
    o.append(t(Z(15), Y(176) + 12, "beyond, 30 deep", 9, "middle", 400, MUTED))
    o.append(f'<line x1="{Z(1.5)}" y1="{Y(g.CEIL-2)}" x2="{Z(1.5)}" y2="{Y(78)}" stroke="#2fa47a" stroke-width="2" stroke-dasharray="4 3"/>')
    o.append(f'<line x1="{Z(1.5)}" y1="{Y(g.CEIL-0.6)}" x2="{Z(4)}" y2="{Y(g.CEIL-0.6)}" stroke="#e0a43a" stroke-width="3"/>')
    o.append(rect(Z(g.HIGH_D), Y(g.HIGH_TOP), g.HIGH_D * s, g.HIGH_T * s, "#e9dccb", "#c9a77a", 1))
    o.append(t(Z(g.HIGH_D) - 4, Y(g.HIGH_TOP) + 4, f"high shelf {_fmt(g.HIGH_D)} deep, top {_fmt(g.HIGH_TOP)}", 9.5, "end", 500))
    o.append(rect(Z(18), Y(g.HIGH_TOP + 28), 17 * s, 28 * s, GAME_F, GAME_S, 2))
    o.append(rect(Z(g.LEDGE_D), Y(g.LEDGE_TOP), g.LEDGE_D * s, (g.LEDGE_TOP - g.LEDGE_UNDER) * s, "#e9dccb", "#c9a77a", 1))
    o.append(f'<line x1="{Z(4.6)}" y1="{Y(g.LEDGE_TOP)}" x2="{Z(0.3)}" y2="{Y(g.LEDGE_LP_TOP)}" stroke="{VIN_S}" stroke-width="3"/>')
    o.append(t(Z(g.LEDGE_D) - 4, Y(g.LEDGE_TOP) + 4, f"record ledge 7 deep, top {_fmt(g.LEDGE_TOP)}", 9.5, "end", 500))
    pz0, pz1 = g.ALC_D - g.TV_PANEL_Z[1], g.ALC_D - g.TV_PANEL_Z[0]
    o.append(rect(Z(pz1), Y(g.TV_TOP), (pz1 - pz0) * s, g.TV_H * s, "#e3e2de", "#b9b4a8", 2))
    o.append(rect(Z(25), Y(g.WORKTOP + 1.6), 23 * s, 1.6 * s, "#d8d5ce", "#bdb8ad", 1))
    o.append(t(Z(pz1) - 4, Y(119), "TV on its stand, centre 116.5", 9.5, "end", 500))
    o.append(rect(Z(45), Y(g.WORKTOP + 6), 9 * s, 6 * s, SND_F, SND_S, 2))
    o.append(t(Z(40.5), Y(g.WORKTOP + 6) - 4, "soundbar", 9, "middle", 500))
    o.append(rect(Z(g.BASE_D), Y(g.WORKTOP), g.BASE_D * s, 3 * s, "#e9dccb", "#c9a77a", 1))
    o.append(t(Z(g.BASE_D) - 4, Y(g.WORKTOP) + 3, f"oak worktop {_fmt(g.BASE_D)} deep, top 76", 9.5, "end", 500))
    o.append(t(Z(g.BASE_D) - 4, Y(g.WORKTOP) + 15, "slot behind the TV for its leads", 9, "end", 400, MUTED))
    fz0 = g.CHAN
    o.append(f'<rect x="{Z(fz0 + g.FRAME_D)}" y="{Y(73)}" width="{g.FRAME_D*s}" height="{64*s}" fill="#fbfaf7" stroke="#8f8a80" stroke-width="1.3"/>')
    o.append(f'<rect x="{Z(fz0 + 38)}" y="{Y(9)}" width="{36*s}" height="{9*s}" fill="#efe2c8" stroke="#c9a77a"/>')
    o.append(t(Z(fz0 + 20), Y(4.5) + 3.5, "9 cm plinth", 9, "middle", 500))
    o.append(t(Z(fz0 + 20), Y(44), "BESTÅ frame", 10, "middle", 600))
    o.append(t(Z(fz0 + 20), Y(44) + 12, "60 × 40 × 64", 9.5, "middle", 400, MUTED))
    o.append(t(Z(fz0 + 20), Y(44) + 24, "back panel off", 9.5, "middle", 400, MUTED))
    o.append(f'<line x1="{Z(fz0)}" y1="{Y(67)}" x2="{Z(0)}" y2="{Y(67)}" stroke="#555" stroke-width="2.5"/>')
    o.append(rect(Z(3.2), Y(34), 2.6 * s, 26 * s, "#eef2fb", BLUE, 1, 1, 'stroke-dasharray="3 2"'))
    o.append(rect(Z(g.BASE_D), Y(73), g.FACE * s, 73 * s, "#ecd3ae", "#b88a55", 0))
    o.append(t(Z(g.BASE_D) - 4, Y(36), "oak face frame 2;", 9.5, "end", 500, "#9c6a3f"))
    o.append(t(Z(g.BASE_D) - 4, Y(36) + 12, "its bottom rail hides", 9.5, "end", 400, MUTED))
    o.append(t(Z(g.BASE_D) - 4, Y(36) + 24, "the plinth", 9.5, "end", 400, MUTED))
    for yy, lab, col in [(67, "anti-tip bracket", INK), (22, "4 cm channel", BLUE)]:
        o.append(f'<line x1="{Z(0.5)}" y1="{Y(yy)}" x2="{Z(-3)}" y2="{Y(yy)}" stroke="#b9b4a8"/>')
        o.append(t(Z(-3) + 3, Y(yy) + 3.5, lab, 9, "start", 500, col))
    o.append(f'<line x1="{Z(0)}" y1="{Y(-8)}" x2="{Z(g.BASE_D)}" y2="{Y(-8)}" stroke="{MUTED}"/>')
    o.append(t((Z(0) + Z(g.BASE_D)) / 2, Y(-8) + 14, f"{_fmt(g.BASE_D)}: {_fmt(g.BASE_PROUD)} proud of the breast", 9.5, "middle", 400, MUTED))
    # ---- B: through the vinyl cabinet
    bx = 300
    Q = lambda cm: bx - cm * s      # cm in front of the chimney breast's face
    o.append(t(10, 76, "B · Through the vinyl cabinet", 12, "start", 600))
    o.append(f'<line x1="{Q(-6)}" y1="{Y(0)}" x2="{Q(110)}" y2="{Y(0)}" stroke="#8f8a80" stroke-width="1.6"/>')
    o.append(f'<line x1="{Q(-6)}" y1="{Y(g.CEIL)}" x2="{Q(110)}" y2="{Y(g.CEIL)}" stroke="#8f8a80" stroke-width="1.6"/>')
    o.append(f'<rect x="{Q(0)}" y="{Y(g.CEIL)}" width="14" height="{g.CEIL*s}" fill="#e4ddd0"/>')
    o.append(t(Q(0) + 18, Y(120), "chimney", 9.5, "start", 400, MUTED))
    o.append(t(Q(0) + 18, Y(120) + 12, "breast", 9.5, "start", 400, MUTED))
    o.append(f'<rect x="{Q(42)}" y="{Y(73)}" width="{40*s}" height="{73*s}" fill="#fbf3ec" stroke="#8f8a80" stroke-width="1.3"/>')
    o.append(rect(Q(g.CAB_D), Y(g.CAB_TOP), g.CAB_D * s, 3 * s, "#e9dccb", "#c9a77a", 1))
    o.append(rect(Q(g.CAB_D), Y(73), 2 * s, 73 * s, "#ecd3ae", "#b88a55", 0))
    for yb in (2.3, 37.0):
        o.append(f'<rect x="{Q(42)}" y="{Y(yb + 12)}" width="{40*s}" height="{12*s}" fill="none" stroke="#c9a77a"/>')
        o.append(f'<line x1="{Q(38)}" y1="{Y(yb + 1.2)}" x2="{Q(33)}" y2="{Y(yb + 31)}" stroke="{VIN_S}" stroke-width="2.2"/>')
    o.append(t(Q(22), Y(56), "upper tray", 9.5, "middle", 600))
    o.append(t(Q(22), Y(20), "lower tray", 9.5, "middle", 600))
    dz0 = 3.8
    o.append(rect(Q(dz0 + g.DECK[2]), Y(g.CAB_TOP + g.DECK[1]), g.DECK[2] * s, g.DECK[1] * s, VIN_F, VIN_S, 2))
    o.append(t(Q(dz0 + g.DECK[2] / 2), Y(g.CAB_TOP + 5), "deck", 9.5, "middle", 600))
    o.append(f'<path d="M{Q(dz0)},{Y(g.CAB_TOP + g.DECK[1])} L{Q(dz0 + 2)},{Y(g.LID_CLEAR_TO - 4)}" stroke="#9a958b" stroke-width="1.6" stroke-dasharray="4 3"/>')
    o.append(f'<rect x="{Q(g.CAB_D)}" y="{Y(g.LID_CLEAR_TO)}" width="{g.CAB_D*s}" height="{(g.LID_CLEAR_TO-g.CAB_TOP-g.DECK[1])*s}" fill="none" stroke="#b9b4a8" stroke-dasharray="4 3"/>')
    o.append(t(Q(g.CAB_D) - 4, Y(118), "lid opens into", 9, "end", 400, MUTED))
    o.append(t(Q(g.CAB_D) - 4, Y(118) + 11, f"this space: keep the", 9, "end", 400, MUTED))
    o.append(t(Q(g.CAB_D) - 4, Y(118) + 22, f"breast clear to {_fmt(g.LID_CLEAR_TO)}", 9, "end", 400, MUTED))
    o.append(rect(Q(2.2), Y(184), 2 * s, 34 * s, "#333", "#111", 0))
    o.append(t(Q(3) - 4, Y(170), "framed LPs, 150–184", 9, "end", 500))
    o.append(t(Q(g.CAB_D) - 4, Y(g.CAB_TOP) + 3, f"oak top, {_fmt(g.CAB_D)} deep, at 76", 9.5, "end", 500))
    o.append(t(Q(1), Y(30), "2 cm", 8.5, "middle", 400, MUTED))
    o.append(t(Q(1), Y(30) + 10, "gap", 8.5, "middle", 400, MUTED))
    o.append(f'<line x1="{Q(0)}" y1="{Y(-8)}" x2="{Q(g.CAB_D)}" y2="{Y(-8)}" stroke="{MUTED}"/>')
    o.append(t((Q(0) + Q(g.CAB_D)) / 2, Y(-8) + 14, f"{_fmt(g.CAB_D)} in front of the breast", 9.5, "middle", 400, MUTED))
    return svg(W, H, "\n".join(o), "How the wall goes together, layer by layer",
               "Side sections to scale, room on the left. Dashed: the upright and the breast's face beyond the cut")


# ------------------------------------------------------------------ joinery details (artisan oak version)
def joints():
    W, H = 860, 500
    o = []
    OAKF, OAKS, END = "#ecd3ae", "#b88a55", "#d7b483"
    k = 7.0
    ax, ay = 40, 110
    PX = lambda c: ax + 60 + c * k
    PZ = lambda c: ay + c * k
    o.append(t(0, 70, "A · Wedged through-tenons, from above", 12, "start", 600))
    o.append(f'<line x1="{PX(-9)}" y1="{PZ(0)}" x2="{PX(14)}" y2="{PZ(0)}" stroke="#8f8a80" stroke-width="3"/>')
    o.append(t(PX(14) + 4, PZ(0) + 4, "wall", 10, "start", 400, MUTED))
    o.append(rect(PX(-9), PZ(0), 9 * k, 25 * k, OAKF, OAKS, 0))
    o.append(t(PX(-4.5), PZ(5), "side shelf", 10, "middle", 500))
    o.append(t(PX(-4.5), PZ(5) + 12, "25 deep", 9.5, "middle", 400, MUTED))
    o.append(t(PX(-4.5), PZ(25) + 14, "room ↓", 9.5, "middle", 400, MUTED))
    o.append(rect(PX(0), PZ(0), 4.5 * k, 30 * k, "#f4e3c6", OAKS, 0))
    o.append(t(PX(2.25), PZ(33), "upright", 10, "middle", 500))
    o.append(t(PX(2.25), PZ(33) + 12, "4.5 × 30", 9.5, "middle", 400, MUTED))
    o.append(rect(PX(3.3), PZ(0), 1.2 * k, 7 * k, OAKF, OAKS, 0, 0.8, 'stroke-dasharray="2 2"'))
    o.append(rect(PX(4.5), PZ(0), 2.5 * k, 7 * k, "#e9dccb", OAKS, 0, 0.8))
    o.append(t(PX(7.5), PZ(3) + 3, "ledge housed here,", 9, "start", 500))
    o.append(t(PX(7.5), PZ(3) + 14, "0–7 from the wall", 9, "start", 400, MUTED))
    for zc in (12.0, 20.0):
        o.append(rect(PX(0), PZ(zc - 3), 6.5 * k, 6 * k, END, OAKS, 0, 1, 'fill-opacity="0.85"'))
        o.append(f'<line x1="{PX(4.5)}" y1="{PZ(zc)}" x2="{PX(6.5)}" y2="{PZ(zc)}" stroke="#4a2f19" stroke-width="2"/>')
    o.append(t(PX(7.3), PZ(12) + 4, "tenons 6 wide, 2.4 thick,", 9.5, "start", 500))
    o.append(t(PX(7.3), PZ(12) + 16, "at 12 and 20 from the wall", 9.5, "start", 400, MUTED))
    o.append(t(PX(7.3), PZ(20) + 10, "2 cm proud, chamfered,", 9.5, "start", 500))
    o.append(t(PX(7.3), PZ(20) + 22, "clear of the ledge", 9.5, "start", 400, MUTED))
    bx = 330
    FX = lambda c: bx + 60 + c * k
    FY = lambda c: ay + 120 - c * k
    o.append(t(bx, 70, "B · The same joint from the front", 12, "start", 600))
    o.append(rect(FX(0), FY(14), 4.5 * k, 28 * k, "#f4e3c6", OAKS, 0))
    o.append(rect(FX(-11), FY(2), 11 * k, 4 * k, OAKF, OAKS, 0))
    o.append(f'<path d="M{FX(0)},{FY(1.2)} L{FX(3)},{FY(1.2)} L{FX(4.5)},{FY(1.55)} L{FX(6.5)},{FY(1.55)} L{FX(6.5)},{FY(-1.55)} L{FX(4.5)},{FY(-1.55)} L{FX(3)},{FY(-1.2)} L{FX(0)},{FY(-1.2)}Z" fill="{END}" stroke="{OAKS}"/>')
    o.append(f'<line x1="{FX(2.2)}" y1="{FY(0)}" x2="{FX(6.5)}" y2="{FY(0)}" stroke="#4a2f19" stroke-width="1.6"/>')
    o.append(f'<path d="M{FX(6.5)},{FY(0.35)} L{FX(2.6)},{FY(0)} L{FX(6.5)},{FY(-0.35)}Z" fill="#7a4e2b"/>')
    o.append(t(FX(8), FY(0) + 4, "oak wedge in a saw kerf,", 9.5, "start", 500))
    o.append(t(FX(8), FY(0) + 16, "glued and driven home", 9.5, "start", 400, MUTED))
    o.append(t(FX(8), FY(4.2), "mortise flared 3–4 mm", 9.5, "start", 500))
    o.append(t(FX(8), FY(4.2) + 12, "top and bottom, outside face", 9.5, "start", 400, MUTED))
    o.append(t(FX(-5.5), FY(2) - 8, "shelf, 4 thick", 9.5, "middle", 500))
    o.append(t(FX(2.25), FY(14) - 8, "upright", 9.5, "middle", 500))
    o.append(t(bx, FY(-14) + 22, "The kerf runs flat, so the wedge spreads", 9.5, "start", 400, MUTED))
    o.append(t(bx, FY(-14) + 34, "the tenon up and down, along the upright's", 9.5, "start", 400, MUTED))
    o.append(t(bx, FY(-14) + 46, "grain, and can't split it.", 9.5, "start", 400, MUTED))
    cx = 640
    QX = lambda c: cx + 40 + c * k
    o.append(t(cx - 20, 70, "C · Housed shelf, pegged", 12, "start", 600))
    o.append(f'<line x1="{QX(-8)}" y1="{PZ(0)}" x2="{QX(12)}" y2="{PZ(0)}" stroke="#8f8a80" stroke-width="3"/>')
    o.append(rect(QX(-8), PZ(0), 9.2 * k, 30 * k, OAKF, OAKS, 0))
    o.append(rect(QX(0), PZ(0), 4.5 * k, 30 * k, "#f4e3c6", OAKS, 0, 1, 'fill-opacity="0.9"'))
    o.append(rect(QX(0), PZ(0.5), 1.2 * k, 29.5 * k, OAKF, OAKS, 0, 0.8, 'stroke-dasharray="2 2"'))
    o.append(rect(QX(1.2), PZ(19), 1.3 * k, 8 * k, END, OAKS, 0))
    o.append(f'<rect x="{QX(1.1)}" y="{PZ(24.5)}" width="{1.0*k}" height="{5.5*k}" fill="#7a4e2b"/>')
    o.append(t(QX(5.5), PZ(4) + 4, "housing 1.2 deep,", 9.5, "start", 500))
    o.append(t(QX(5.5), PZ(4) + 16, "full depth", 9.5, "start", 400, MUTED))
    o.append(t(QX(5.5), PZ(20) + 4, "stub tenon 2.5", 9.5, "start", 500))
    o.append(t(QX(5.5), PZ(26.5) + 4, "10 mm oak peg", 9.5, "start", 500))
    o.append(t(QX(5.5), PZ(26.5) + 16, "from the front edge", 9.5, "start", 400, MUTED))
    o.append(t(QX(-4), PZ(33), "high shelf / ledge", 10, "middle", 500))
    o.append(t(QX(-4), PZ(33) + 12, "seen from above", 9.5, "middle", 400, MUTED))
    notes = [f"Through-tenons (A, B): both side shelves (top {G.SIDE_SHELF_TOP:g}) pass through their upright, 2 cm proud on the TV side, 12 and 20 cm from the wall.",
             f"Housed and pegged (C): the three lengths of the high shelf (top {G.HIGH_TOP:g}) and the record ledge (top {G.LEDGE_TOP:g}). The peg shows as a dark dot on the upright's face.",
             f"Uprights: {G.UPRIGHT_LEN:g} long, worktop to ceiling, each on two 10 mm dowels into the worktop, scribed to the ceiling, with two concealed brackets into the solid back wall."]
    for i, n in enumerate(notes):
        o.append(t(0, 420 + i * 22, "• " + n, 10, "start", 400, INK))
    return svg(W, H, "\n".join(o), "Artisan oak: how the joints work",
               "Drawn to scale at 7 px per cm. The joints carry the load and are left on show, finished in hardwax oil")




# ------------------------------------------------------------------ house plan (v9, from the Rightmove floor plans, corrected)
WALL = "#3a3a38"; ROOMF = "#fbfaf6"; HATCH = "#c9c3b5"

def house():
    """Three floors side by side, to scale (about 52 px per m), traced from the agent's plan, with the measured
    living room features, the chimney breast, the kitchen brick cupboard and the sloped ceilings added."""
    W, H = 860, 620
    k = 52.0
    o = []
    defs = ('<defs><pattern id="slope" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            '<line x1="0" y1="0" x2="0" y2="8" stroke="#b8b1a2" stroke-width="2"/></pattern>'
            '<pattern id="brick" width="10" height="6" patternUnits="userSpaceOnUse"><rect width="10" height="6" fill="#d9a48a"/>'
            '<path d="M0,3 H10 M5,0 V3 M0,3 V6 M10,3 V6" stroke="#b5785e" stroke-width="0.8"/></pattern></defs>')
    o.append(defs)
    def floor(ox, oy, title, sub):
        o.append(t(ox, oy - 30, title, 12.5, "start", 650))
        o.append(t(ox, oy - 15, sub, 10, "start", 400, MUTED))
        return (lambda m: ox + m * k), (lambda m: oy + m * k)
    def room(X, Y, x1, y1, x2, y2, name=None, dims=None, fill=ROOMF):
        o.append(f'<rect x="{X(x1):.1f}" y="{Y(y1):.1f}" width="{(x2-x1)*k:.1f}" height="{(y2-y1)*k:.1f}" fill="{fill}" stroke="{WALL}" stroke-width="2.2"/>')
        if name:
            cx, cy = (X(x1) + X(x2)) / 2, (Y(y1) + Y(y2)) / 2
            o.append(t(cx, cy - (4 if dims else -4), name, 10, "middle", 650))
            if dims:
                o.append(t(cx, cy + 9, dims, 8.5, "middle", 400, MUTED))
    def deco(X, Y, x, y, lab, anchor="start", dx=9):
        o.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="6" fill="#fff" stroke="{BLUE}" stroke-width="2.2"/>')
        o.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="2" fill="#4fd17a"/>')
        o.append(t(X(x) + (dx if anchor == "start" else -dx), Y(y) + 3.5, lab, 9.5, anchor, 650, BLUE))
    X, Y = floor(14, 92, "Lower ground floor", "kitchen, WC · about 34 m²")
    room(X, Y, 0, 0, 1.04, 1.9, "WC", None, "#eaf2f4")
    room(X, Y, 0, 1.9, 1.04, 3.69, None)
    o.append(t(X(0.52), Y(2.9), "stairs", 8.5, "middle", 400, MUTED))
    room(X, Y, 1.04, 0, 4.81, 3.69, "Kitchen", "3.79 × 3.66 m", "#fdf6e3")
    room(X, Y, 0, 3.69, 1.77, 5.5, "Store")
    o.append(f'<rect x="{X(1.77):.1f}" y="{Y(3.69):.1f}" width="{(4.81-1.77)*k:.1f}" height="{(8.15-3.69)*k:.1f}" fill="#e6e3dc" stroke="{WALL}" stroke-width="2.2"/>')
    o.append(t(X(3.3), Y(5.9), "under the garage", 8.5, "middle", 400, MUTED))
    o.append(f'<rect x="{X(1.92):.1f}" y="{Y(3.10):.1f}" width="{1.175*k:.1f}" height="{0.59*k:.1f}" fill="url(#brick)" stroke="#8f5b45" stroke-width="1.4"/>')
    o.append(t(X(2.5), Y(3.02), "brick cupboard", 8.5, "middle", 650, "#8f5b45"))
    deco(X, Y, 3.3, 2.95, "Deco C", "start")
    o.append(t(X(3.45), Y(2.6), "on the outside of the", 8, "start", 400, MUTED))
    o.append(t(X(3.45), Y(2.6) + 10, "cupboard, up high", 8, "start", 400, MUTED))
    o.append(f'<circle cx="{X(3.2):.1f}" cy="{Y(3.55):.1f}" r="4" fill="{BLUE}"/>')
    o.append(t(X(3.3), Y(3.55) + 4, "Cat6 from above", 8, "start", 600, BLUE))
    # ground floor: the agent's outline, the measured living room features
    X, Y = floor(300, 92, "Ground floor", "living room (measured 4.67 × 3.47 m), hall, garage")
    LW, LD = 4.95, 3.65
    room(X, Y, 0, 0, LW, LD, None, None, "#fdf6e3")
    e = lambda m: LW - m               # distance from the east wall -> x on this plan
    ax0 = e(G.ALC_W / 100)
    bx0 = e((G.ALC_W + G.BREAST_W) / 100)
    o.append(f'<rect x="{X(bx0):.1f}" y="{Y(LD - G.ALC_D/100):.1f}" width="{G.BREAST_W/100*k:.1f}" height="{G.ALC_D/100*k:.1f}" fill="url(#brick)" stroke="{WALL}" stroke-width="2"/>')
    o.append(f'<rect x="{X(ax0):.1f}" y="{Y(LD - G.BASE_D/100):.1f}" width="{G.ALC_W/100*k:.1f}" height="{G.BASE_D/100*k:.1f}" fill="#e9d3b4" stroke="#b88a55" stroke-width="1.2"/>')
    o.append(f'<rect x="{X(e(G.CAB_X[1]/100)):.1f}" y="{Y(LD - (G.ALC_D + G.CAB_D)/100):.1f}" width="{1.0*k:.1f}" height="{G.CAB_D/100*k:.1f}" fill="#f4e0cc" stroke="#b88a55" stroke-width="1.2"/>')
    o.append(t(X(ax0 + 0.93), Y(LD - 0.62), "media wall", 8.5, "middle", 650, "#7a5130"))
    o.append(t(X(e(2.36)), Y(LD - 0.95), "vinyl", 8, "middle", 650, "#7a5130"))
    o.append(t(X(1.1), Y(1.0), "Living room", 10, "middle", 650))
    o.append(t(X(1.1), Y(1.0) + 13, "4.67 × 3.47 m measured", 8.5, "middle", 400, MUTED))
    o.append(f'<rect x="{X(e(3.08)):.1f}" y="{Y(-0.06):.1f}" width="{2.35*k:.1f}" height="5" fill="#cfe3f2" stroke="#7aa6c8"/>')
    o.append(t(X(e(1.9)), Y(0.0) + 14, "window", 8, "middle", 400, MUTED))
    room(X, Y, 0, LD, 1.96, 7.3, "Hall")
    room(X, Y, 1.96, LD, 5.05, 8.15, "Garage")
    room(X, Y, 0, 7.3, 0.5, 8.15)
    room(X, Y, 1.25, 7.3, 1.96, 8.15)
    dx_ = bx0 - 0.12
    o.append(f'<path d="M{X(dx_):.1f},{Y(LD):.1f} A{0.8*k},{0.8*k} 0 0 1 {X(dx_ - 0.8):.1f},{Y(LD - 0.8):.1f}" fill="none" stroke="#9a958b" stroke-dasharray="3 2"/>')
    o.append(t(X(dx_ - 0.45), Y(LD - 0.15), "door?", 8, "middle", 400, MUTED))
    deco(X, Y, e(1.73), LD - 0.2, "Deco B", "start", 9)
    o.append(f'<circle cx="{X(e(G.PEND_X/100)):.1f}" cy="{Y(1.735):.1f}" r="4" fill="#e8b53f" stroke="#8a6a1a"/>')
    o.append(t(X(e(G.PEND_X/100)) - 8, Y(1.735) + 4, "spot bar", 8, "end", 500, "#8a6a1a"))
    for i in range(int(LW * 4)):
        o.append(f'<circle cx="{X(0.12 + i*0.25):.1f}" cy="{Y(0.06):.1f}" r="1" fill="#e0a43a"/>')
    # 1st floor
    X, Y = floor(590, 92, "1st floor", "bedrooms, bathroom · about 40 m²")
    room(X, Y, 0, 0, 1.96, 2.36, "Bathroom", "2.04 × 2.38 m", "#eaf2f4")
    room(X, Y, 1.96, 0, 5.05, 3.69, None, None, "#fdf3d6")
    o.append(t(X(3.5), Y(2.2), "Bedroom 2", 10, "middle", 650)); o.append(t(X(3.5), Y(2.2) + 13, "spare · music room", 8.5, "middle", 400, MUTED))
    room(X, Y, 0, 2.36, 1.96, 5.95, "Landing")
    room(X, Y, 1.96, 3.69, 5.05, 8.15, None, None, "#fdf3d6")
    o.append(t(X(3.9), Y(6.0), "Master", 10, "middle", 650)); o.append(t(X(3.9), Y(6.0) + 13, "projector", 8.5, "middle", 400, MUTED))
    room(X, Y, 1.96, 3.69, 2.96, 4.75, None, None, "#ece8df")
    o.append(t(X(2.46), Y(4.12), "airing", 8, "middle", 650))
    o.append(t(X(2.46), Y(4.12) + 10, "cupboard", 8, "middle", 650))
    room(X, Y, 0, 5.95, 1.96, 8.15, None, None, "#fdf3d6")
    o.append(t(X(0.98), Y(7.55), "Bedroom 3", 10, "middle", 650)); o.append(t(X(0.98), Y(7.55) + 13, "gaming PCs, Hub 5", 8.5, "middle", 400, MUTED))
    for (x1, x2) in ((0, 1.96), (1.96, 5.05)):
        o.append(f'<rect x="{X(x1):.1f}" y="{Y(0):.1f}" width="{(x2-x1)*k:.1f}" height="{0.9*k:.1f}" fill="url(#slope)" opacity="0.8"/>')
    o.append(t(X(2.5), Y(0.55), "sloped ceiling, low at the back wall", 8, "middle", 600, "#6b6455"))
    deco(X, Y, 0.55, 6.75, "Deco A + Switch 1", "start", 10)
    o.append(wire([(X(0.55), Y(6.75)), (X(0.55), Y(4.25)), (X(2.4), Y(4.25))], BLUE, 2.4))
    o.append(f'<circle cx="{X(2.4):.1f}" cy="{Y(4.25):.1f}" r="4" fill="{BLUE}"/>')
    o.append(t(X(0.62), Y(5.3), "Cat6 across the landing,", 8.5, "start", 600, BLUE))
    o.append(t(X(0.62), Y(5.3) + 11, "down through the", 8.5, "start", 600, BLUE))
    o.append(t(X(0.62), Y(5.3) + 22, "airing cupboard floor", 8.5, "start", 600, BLUE))
    o.append(wire([(X(2.7), Y(4.6)), (X(3.4), Y(5.6))], BLUE, 1.8, "5 3"))
    o.append(wire([(X(2.7), Y(3.85)), (X(3.3), Y(2.9))], BLUE, 1.8, "5 3"))
    o.append(t(X(3.45), Y(5.75), "optional", 8, "start", 500, BLUE))
    o.append(t(X(3.35), Y(2.75), "optional", 8, "start", 500, BLUE))
    ly = H - 36
    o.append(f'<circle cx="8" cy="{ly - 4}" r="6" fill="#fff" stroke="{BLUE}" stroke-width="2.2"/>'); o.append(t(20, ly, "Deco unit", 10, "start", 400, MUTED))
    o.append(wire([(100, ly - 4), (128, ly - 4)], BLUE, 2.4)); o.append(t(134, ly, "Cat6 run", 10, "start", 400, MUTED))
    o.append(wire([(200, ly - 4), (228, ly - 4)], BLUE, 1.8, "5 3")); o.append(t(234, ly, "optional run", 10, "start", 400, MUTED))
    o.append(f'<rect x="318" y="{ly - 10}" width="16" height="12" fill="url(#brick)"/>'); o.append(t(340, ly, "chimney breast / brick cupboard", 10, "start", 400, MUTED))
    o.append(f'<rect x="530" y="{ly - 10}" width="16" height="12" fill="url(#slope)"/>'); o.append(t(552, ly, "sloped ceiling", 10, "start", 400, MUTED))
    o.append(f'<circle cx="650" cy="{ly - 4}" r="2" fill="#e0a43a"/><circle cx="658" cy="{ly - 4}" r="2" fill="#e0a43a"/>'); o.append(t(668, ly, "LED strip round the ceiling", 10, "start", 400, MUTED))
    o.append(t(0, H - 12, "Outline traced from the agent's plan (north, the window side, at the top). The living room's alcove, chimney breast and windows are placed from your measurements.", 9, "start", 400, MUTED))
    return svg(W, H, "\n".join(o), "The house: where the Decos and Cat6 runs go",
               "Deco A and Switch 1 move to bedroom 3 with the Hub 5. Both Cat6 runs drop through the airing cupboard, right over the media wall's corner")


def living_plan():
    """The living room from above, to scale, from the measured sketch. North (the window) at the top, east on the right."""
    W, H = 860, 600
    k = 120.0
    ox, oy = 150, 78
    g = G
    RW, RD = g.ROOM_W / 100, g.ROOM_D / 100
    X = lambda e: ox + (RW - e) * k          # e = metres from the east wall
    Y = lambda n: oy + n * k                 # n = metres from the window wall
    o = []
    o.append('<defs><pattern id="brick2" width="10" height="6" patternUnits="userSpaceOnUse"><rect width="10" height="6" fill="#d9a48a"/>'
             '<path d="M0,3 H10 M5,0 V3 M0,3 V6 M10,3 V6" stroke="#b5785e" stroke-width="0.8"/></pattern>'
             '<pattern id="hatch2" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="#c9c3b5" stroke-width="2"/></pattern></defs>')
    alc, bw, bd = g.ALC_W / 100, g.BREAST_W / 100, g.ALC_D / 100
    face = RD - bd                           # the breast's face, from the window wall
    rec_d = g.BREAST_D_WEST / 100
    stair_w, stair_d = 0.66, 0.79           # to confirm
    pts_ = [(X(0), Y(0)), (X(RW), Y(0)), (X(RW), Y(RD - stair_d)), (X(RW - stair_w), Y(RD - stair_d)), (X(RW - stair_w), Y(RD)),
            (X(alc + bw), Y(RD)), (X(alc + bw), Y(face)), (X(alc), Y(face)), (X(alc), Y(RD)), (X(0), Y(RD))]
    o.append('<polygon points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts_) + f'" fill="#fbfaf6" stroke="{WALL}" stroke-width="3"/>')
    o.append(f'<rect x="{X(alc + bw):.1f}" y="{Y(face):.1f}" width="{bw*k:.1f}" height="{bd*k:.1f}" fill="url(#brick2)" stroke="{WALL}" stroke-width="2"/>')
    o.append(t(X(alc + bw / 2), Y(face) + 26, "chimney breast", 9.5, "middle", 650, "#8f5b45"))
    o.append(f'<rect x="{X(RW):.1f}" y="{Y(RD - stair_d):.1f}" width="{stair_w*k:.1f}" height="{stair_d*k:.1f}" fill="url(#hatch2)" stroke="#9a958b"/>')
    o.append(t(X(RW - stair_w / 2), Y(RD - stair_d) - 6, "stair box (to confirm)", 9, "middle", 400, MUTED))
    # window, radiator, the box in the NW corner
    o.append(f'<rect x="{X(g.WINDOW_X[1]/100):.1f}" y="{Y(0) - 4:.1f}" width="{(g.WINDOW_X[1]-g.WINDOW_X[0])/100*k:.1f}" height="8" fill="#cfe3f2" stroke="#7aa6c8"/>')
    o.append(t(X((g.WINDOW_X[0] + g.WINDOW_X[1]) / 200), Y(0) - 10, f"window {_fmt(g.WINDOW_X[1]-g.WINDOW_X[0])}", 9.5, "middle", 400, MUTED))
    o.append(f'<rect x="{X(g.RADIATOR_X[1]/100):.1f}" y="{Y(0) + 5:.1f}" width="{(g.RADIATOR_X[1]-g.RADIATOR_X[0])/100*k:.1f}" height="7" fill="#eceae4" stroke="#b9b4a8"/>')
    o.append(t(X(g.RADIATOR_X[0] / 100) + 6, Y(0) + 22, "radiator 137", 8.5, "start", 400, MUTED))
    o.append(f'<rect x="{X(RW):.1f}" y="{Y(0):.1f}" width="{g.NW_BOX[0]/100*k:.1f}" height="{g.NW_BOX[1]/100*k:.1f}" fill="url(#hatch2)" stroke="#9a958b"/>')
    o.append(t(X(RW) + 4, Y(0.22) + 12, "box 23 × 22?", 8.5, "start", 400, MUTED))
    # media wall base, uprights, TV; vinyl cabinet
    bpd = g.BASE_D / 100
    o.append(f'<rect x="{X(alc):.1f}" y="{Y(RD - bpd):.1f}" width="{alc*k:.1f}" height="{bpd*k:.1f}" fill="#e9d3b4" stroke="#b88a55" stroke-width="1.4"/>')
    for (a, b) in (g.UP_L, g.UP_R):
        o.append(f'<rect x="{X(b/100):.1f}" y="{Y(RD - g.UP_D/100):.1f}" width="{g.UP_T/100*k:.1f}" height="{g.UP_D/100*k:.1f}" fill="#b88a55"/>')
    pz = (g.ALC_D - g.TV_PANEL_Z[1]) / 100
    o.append(f'<rect x="{X(g.TV_X[1]/100):.1f}" y="{Y(RD - pz - 0.045):.1f}" width="{g.TV_W/100*k:.1f}" height="{0.045*k:.1f}" fill="#222"/>')
    o.append(t(X(alc / 2), Y(RD - bpd) + 22, "media wall base, 46 deep", 9, "middle", 650, "#7a5130"))
    o.append(f'<rect x="{X(g.CAB_X[1]/100):.1f}" y="{Y(face - g.CAB_D/100):.1f}" width="{(g.CAB_X[1]-g.CAB_X[0])/100*k:.1f}" height="{g.CAB_D/100*k:.1f}" fill="#f4e0cc" stroke="#b88a55" stroke-width="1.4"/>')
    o.append(t(X((g.CAB_X[0] + g.CAB_X[1]) / 200), Y(face - g.CAB_D / 100) + 20, "vinyl cabinet", 9, "middle", 650, "#7a5130"))
    # door (position to confirm)
    hx = alc + bw + 0.10
    o.append(f'<path d="M{X(hx + 0.8):.1f},{Y(RD):.1f} A{0.8*k},{0.8*k} 0 0 1 {X(hx):.1f},{Y(RD - 0.8):.1f}" fill="none" stroke="#9a958b" stroke-dasharray="3 2"/>')
    o.append(f'<line x1="{X(hx):.1f}" y1="{Y(RD):.1f}" x2="{X(hx):.1f}" y2="{Y(RD - 0.8):.1f}" stroke="#9a958b" stroke-width="1.5"/>')
    o.append(t(X(hx + 0.42), Y(RD) - 6, "door: which side hinges?", 9, "middle", 600, "#d0573b"))
    # sofa, coffee table, rears
    sx0, sx1 = g.SOFA_X[0] / 100, g.SOFA_X[1] / 100
    o.append(rect(X(sx1), Y(0.10), (sx1 - sx0) * k, g.SOFA[1] / 100 * k, "#ecebe6", "#b9b4a8", 10))
    o.append(t(X((sx0 + sx1) / 2), Y(0.62), "Sofa (about 2.0 × 0.95)", 10, "middle", 650))
    o.append(rect(X(1.5), Y(1.35), 0.95 * k, 0.5 * k, "#f3efe6", "#c9c5bb", 6))
    o.append(t(X(1.025), Y(1.64), "coffee table", 8.5, "middle", 400, MUTED))
    o.append(rect(X(0.12), Y(0.30), 0.12 * k, 0.15 * k, SND_F, SND_S, 3))          # left rear, on the east wall
    o.append(rect(X(sx1 + 0.23), Y(0.30), 0.15 * k, 0.15 * k, SND_F, SND_S, 3))   # right rear, past the sofa's end
    o.append(t(X(sx1 + 0.15), Y(0.30) - 4, "rear", 8, "middle", 400, MUTED))
    # PC shelf and socket on the east wall
    z2n = lambda z: (g.ALC_D - z) / 100     # render z -> metres in front of the alcove back... from the window wall:
    pn1, pn2 = RD - z2n(g.PC_SHELF_Z[0]), RD - z2n(g.PC_SHELF_Z[1])
    o.append(rect(X(0.32), Y(pn2), 0.32 * k, (pn1 - pn2) * k, GAME_F, GAME_S, 3))
    o.append(t(X(0.16), Y(pn2) - 6, "PC shelf", 9, "middle", 600))
    sn = RD - z2n(g.SOCKET["z"])
    o.append(rect(X(0) - 7, Y(sn) - 8, 7, 16, "#fff", "#d0573b", 1))
    o.append(t(X(0) + 10, Y(sn) + 4, "double socket", 9, "start", 600, "#d0573b"))
    # spot bar on the rose
    rn = -g.WINDOW_Z + g.PEND_Z
    rx_, ry_ = X(g.PEND_X / 100), Y(rn / 100)
    o.append(f'<rect x="{rx_ - 0.42*k:.1f}" y="{ry_ - 2:.1f}" width="{0.84*k:.1f}" height="4" fill="#ddd9d0" stroke="#999"/>')
    for dx, col, stem, tgt in [(-31.5, "#a9c7ab", 0, (60, 30)), (-10.5, "#a7d0d8", 0, (93, 34)), (10.5, "#e8b53f", 0, (105, -150)), (31.5, "#e79c95", 0, (240, -24))]:
        hx_ = X((g.PEND_X + dx) / 100)
        tx, ty = X(tgt[0] / 100), Y((g.ROOM_D - g.ALC_D + tgt[1]) / 100)
        ln = ((tx - hx_) ** 2 + (ty - ry_) ** 2) ** 0.5
        ex, ey = hx_ + (tx - hx_) / ln * 52, ry_ + (ty - ry_) / ln * 52
        o.append(f'<circle cx="{hx_:.1f}" cy="{ry_:.1f}" r="5" fill="{col}" stroke="#555" stroke-width="0.6"/>')
        o.append(arrow(hx_, ry_, ex, ey, col, 1.4))
    o.append(t(rx_ - 0.48 * k, ry_ + 4, "spot bar on the existing rose", 9, "end", 600, "#8a6a1a"))
    # LED strip round the ceiling
    o.append('<polygon points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts_) + '" fill="none" stroke="#e0a43a" stroke-width="1.4" stroke-dasharray="1 4" stroke-linecap="round" transform="translate(0,0)"/>')
    # viewing line
    vx = X(g.TV_CX / 100)
    o.append(f'<line x1="{vx:.1f}" y1="{Y(g.EYES_FROM_WINDOW/100):.1f}" x2="{vx:.1f}" y2="{Y(g.SCREEN_FROM_WINDOW/100):.1f}" stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="5 3"/>')
    o.append(t(vx - 6, Y(2.2), "eyes to screen", 9.5, "end", 650, BLUE))
    o.append(t(vx - 6, Y(2.2) + 12, f"about {g.VIEW_DIST/100:.2f} m", 9.5, "end", 400, BLUE))
    # dimensions
    def hdim(e1, e2, n, lab, below=True):
        o.append(f'<line x1="{X(e1):.1f}" y1="{n:.1f}" x2="{X(e2):.1f}" y2="{n:.1f}" stroke="{MUTED}"/>')
        for e_ in (e1, e2):
            o.append(f'<line x1="{X(e_):.1f}" y1="{n-4:.1f}" x2="{X(e_):.1f}" y2="{n+4:.1f}" stroke="{MUTED}"/>')
        o.append(t((X(e1) + X(e2)) / 2, n + (13 if below else -5), lab, 9.5, "middle", 400, MUTED))
    hdim(0, RW, Y(RD) + 46, f"{_fmt(g.ROOM_W*10)} mm, east to west")
    hdim(0, alc, Y(RD) + 24, f"alcove {_fmt(g.ALC_W*10)}")
    hdim(alc, alc + bw, Y(RD) + 24, f"breast {_fmt(g.BREAST_W*10)}")
    hdim(alc + bw, RW - stair_w, Y(RD) + 24, "about 950–1045 (to confirm)")
    hdim(0, g.WINDOW_X[0] / 100, Y(0) - 26, "730", False)
    o.append(f'<line x1="{X(RW) - 30:.1f}" y1="{Y(0):.1f}" x2="{X(RW) - 30:.1f}" y2="{Y(RD):.1f}" stroke="{MUTED}"/>')
    o.append(t(X(RW) - 36, Y(RD / 2), f"{_fmt(g.ROOM_D*10)} mm", 9.5, "end", 400, MUTED))
    o.append(t(X(RW) - 36, Y(RD / 2) + 12, "window to alcove back", 9, "end", 400, MUTED))
    o.append(t(X(0) + 10, Y(0.3), "east wall", 9, "start", 400, MUTED))
    o.append(t(ox, H - 10, f"Ceiling {_fmt(g.CEIL*10)} mm. Skirting 60 × 20. The west end (stair box, door, recess) is drawn roughly until you confirm it.", 9, "start", 400, MUTED))
    return svg(W, H, "\n".join(o), "The living room from above, as you measured it",
               "To scale, north at the top. Vinyl cabinet against the chimney breast; spot bar heads aimed at the shelves, the coffee table and the vinyl corner")


def why_layout():
    W, H = 860, 400
    s = 2.55
    ox = 20
    X = lambda cm: ox + cm * s
    o = []
    def strip(y, segs, h=34):
        for a, b, lab, kind in segs:
            f, st = {"g": (GAME_F, GAME_S), "v": (VIN_F, VIN_S), "s": (SND_F, SND_S), "o": ("#e9d3b4", "#b88a55"), "w": ("#f1efe9", "#bdb8ad"), "x": ("#fbe2dd", "#d0573b")}[kind]
            o.append(f'<rect x="{X(a)}" y="{y}" width="{(b-a)*s}" height="{h}" fill="{f}" stroke="{st}" stroke-width="1"/>')
            if lab:
                o.append(t((X(a) + X(b)) / 2, y + h / 2 + 4, lab, 9.5, "middle", 500))
    o.append(t(0, 62, "What we drew in v9: an alcove 225 wide", 12, "start", 650))
    strip(74, [(0, 44.5, "Series X 44.5", "g"), (44.5, 49, "", "o"), (49, 175.5, "TV gap 126.5", "w"), (175.5, 180, "", "o"), (180, 225, "turntable 45", "v")])
    strip(112, [(0, 60, "Xbox 60", "g"), (60, 120, "PlayStation 60", "g"), (120, 180, "record trays 60", "v"), (180, 225, "sub 45", "s")])
    o.append(t(X(225) + 8, 95, "above the worktop", 9.5, "start", 400, MUTED))
    o.append(t(X(225) + 8, 133, "below the worktop", 9.5, "start", 400, MUTED))
    g = G
    o.append(t(0, 172, f"What you measured: {_fmt(g.ALC_W)} wide, then the chimney breast", 12, "start", 650))
    strip(198, [(0, g.SIDE_ZONE, "Series X", "g"), (g.UP_L[0], g.UP_L[1], "", "o"), (g.UP_L[1], g.UP_R[0], f"TV gap {_fmt(g.TV_GAP)}", "w"),
                (g.UP_R[0], g.UP_R[1], "", "o"), (g.UP_R[1], g.ALC_W, "dock", "w")])
    strip(236, [(0, 3, "", "w"), (3, 63, "Xbox 60", "g"), (63, 123, "PlayStation 60", "g"), (123, 183, "sub 60", "s"), (183, 186, "", "w")])
    strip(198, [(g.ALC_W, g.BREAST_X[1], "", "w")], 72)
    strip(236, [(g.CAB_X[0], g.CAB_BAY_A[1], "trays 60", "v"), (g.CAB_BAY_B[0], g.CAB_X[1], "kit 40", "v")])
    strip(198, [(g.DECK_X[0], g.DECK_X[1], "deck", "v"), (g.BROWSER_X[0], g.BROWSER_X[1], "browser", "v")])
    o.append(f'<rect x="{X(g.UP_R[1])}" y="{198 - 5}" width="{g.DECK[0]*s}" height="{44}" fill="none" stroke="#d0573b" stroke-width="1.6" stroke-dasharray="5 3"/>')
    o.append(t(X(g.UP_R[1]), 188, f"turntable {_fmt(g.DECK[0])} wide: doesn't fit in {_fmt(g.SIDE_ZONE)}", 9.5, "start", 600, "#d0573b"))
    o.append(t((X(g.ALC_W) + X(g.BREAST_X[1])) / 2, 290, f"chimney breast {_fmt(g.BREAST_W)}: the new vinyl cabinet", 9.5, "middle", 600, VIN_S))
    o.append(f'<line x1="{X(0)}" y1="290" x2="{X(g.ALC_W)}" y2="290" stroke="{MUTED}"/>')
    o.append(t(X(g.ALC_W / 2), 304, f"alcove {_fmt(g.ALC_W)}: 3 + 60 + 60 + 60 + 3", 9.5, "middle", 400, MUTED))
    notes = [f"The alcove is {_fmt(225 - g.ALC_W)} cm narrower than drawn. With the TV still framed by two uprights, each side is only {_fmt(g.SIDE_ZONE)} cm: enough for the Series X, not a turntable.",
             "Below, three 60 cm bays still fit. Bay 3 takes the sub (under the TV is good for bass), and the record trays move with the deck.",
             "The deck, the LP browser and both trays go into one oak cabinet against the chimney breast, at the same 76 cm height: the whole vinyl corner in one place."]
    for i, n in enumerate(notes):
        o.append(t(0, 334 + i * 20, "• " + n, 10, "start", 400, INK))
    return svg(W, H, "\n".join(o), "Why the layout changed",
               "To scale, from the side wall. Top: what v9 assumed. Bottom: the room as you measured it")

if __name__ == "__main__":
    for name, fn in [("network", network), ("front", front), ("drawer", drawer), ("sound", sound), ("game", game_drawer), ("av", av), ("power", power), ("routes", routes), ("pcshelf", pc_shelf), ("section", section), ("joints", joints), ("house", house), ("living", living_plan), ("why", why_layout)]:
        open(f"d_{name}.svg", "w").write(fn().replace('width="100%"', 'width="860"'))
    print("ok")
