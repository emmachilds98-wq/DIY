"""Diagrams for the revised plan, as standalone SVG strings (Inter, light theme)."""

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


# ------------------------------------------------------------------ network
def network():
    o = []
    W = 760
    # bands
    bands = [("Top floor", 56, 128), ("Living room", 196, 214), ("Kitchen", 422, 74)]
    for name, y, h in bands:
        o.append(rect(0, y, W, h, BAND, "#e2e0da", 8))
        o.append(t(14, y + 20, name, 11.5, "start", 500, MUTED))
    # top floor
    o.append(node(14, 84, 128, 42, "Virgin Hub 5", "modem mode"))
    o.append(node(170, 84, 128, 42, "Deco A (main)", "router + Wi-Fi"))
    o.append(node(326, 84, 136, 42, "Switch 1", "8-port gigabit · new"))
    o.append(node(560, 70, 120, 30, "PC 1", bold=False))
    o.append(node(560, 112, 120, 30, "PC 2", bold=False))
    o.append(t(690, 152, "3 ports spare", 10.5, "end", 400, MUTED))
    o.append(wire([(142, 105), (170, 105)]))
    o.append(wire([(298, 105), (326, 105)]))
    o.append(wire([(462, 98), (520, 98), (520, 85), (560, 85)]))
    o.append(wire([(462, 112), (520, 112), (520, 127), (560, 127)]))
    # living room
    o.append(node(170, 300, 128, 42, "Deco B", "high shelf, 192 cm"))
    o.append(node(326, 300, 136, 42, "Switch 2", "8-port gigabit"))
    devs = ["Xbox Series X", "Xbox One", "Xbox 360", "PS3", "PC (left wall)", "LG C6 TV"]
    for i, d in enumerate(devs):
        y = 214 + i * 30
        o.append(node(560, y, 150, 24, d, bold=False))
        o.append(wire([(462, 321), (520, 321), (520, y + 12), (560, y + 12)]))
    o.append(t(710, 404, "1 port spare", 10.5, "end", 400, MUTED))
    o.append(wire([(298, 321), (326, 321)]))
    # kitchen
    o.append(node(170, 446, 128, 40, "Deco C", "kitchen Wi-Fi"))
    # Cat6 runs (blue)
    o.append(wire([(380, 126), (380, 170), (234, 170), (234, 300)], BLUE, 2.4))
    o.append(t(244, 192, "Cat6 run 1", 10.5, "start", 500, BLUE))
    o.append(wire([(410, 126), (410, 160), (740, 160), (740, 466), (298, 466)], BLUE, 2.4))
    o.append(t(730, 456, "Cat6 run 2 (straight to the kitchen)", 10.5, "end", 500, BLUE))
    # legend
    o.append(wire([(0, 520), (28, 520)], BLUE, 2.4)); o.append(t(36, 524, "Cat6 run between floors", 11, "start", 400, MUTED))
    o.append(wire([(220, 520), (248, 520)])); o.append(t(256, 524, "short Cat6 patch lead", 11, "start", 400, MUTED))
    return svg(W, 534, "\n".join(o), "Every floor has its own Cat6 link back to the top floor",
               "Revised: an 8-port switch upstairs leaves room to grow, and the Xbox 360 is wired too")


# ------------------------------------------------------------------ front elevation
def front():
    s = 2.3
    W, H = 860, 690
    ox, oy = 215, 600    # alcove left / floor in px
    X = lambda cm: ox + cm * s
    Y = lambda cm: oy - cm * s
    o = []
    o.append(f'<rect x="{X(0)}" y="{Y(220)}" width="{225*s}" height="{220*s}" fill="#f8f7f4" stroke="{LINE}" stroke-width="1.2"/>')
    o.append(f'<line x1="{X(-80)}" y1="{oy}" x2="{X(260)}" y2="{oy}" stroke="#b9b4a8" stroke-width="1.4"/>')
    o.append(t(X(-6), Y(110), "220 cm, floor to ceiling", 10.5, "middle", 400, MUTED, f'transform="rotate(-90 {X(-6)} {Y(110)})"'))
    o.append(t(X(-70), Y(214), "Left wall", 11.5, "start", 400, MUTED))
    # height scale on the right
    for h in (0, 9, 73, 76, 113, 116.5, 156, 192, 220):
        o.append(f'<line x1="{X(229)}" y1="{Y(h)}" x2="{X(233)}" y2="{Y(h)}" stroke="#9a958b"/>')
    o.append(f'<line x1="{X(231)}" y1="{Y(0)}" x2="{X(231)}" y2="{Y(220)}" stroke="#cfcabf"/>')
    for h, lab, dy in [(0, "0", 4), (9, "9 plinth", 6), (76, "76 worktop", 0), (113, "113 turntable shelf", 9),
                       (116.5, "116.5 TV centre", -4), (156, "156 left shelf", 4), (192, "192 high shelf", 4), (220, "220", 4)]:
        o.append(t(X(235), Y(h) + dy, lab, 9.5, "start", 400, MUTED))
    # high shelf + items
    o.append(rect(X(0), Y(192), 225 * s, 4 * s, "#e9dccb", "#c9b79f", 1))
    o.append(rect(X(3), Y(216), 100 * s, 24 * s, "#ecebe7", LINE, 2))
    o.append(t(X(53), Y(203), "books", 10, "middle", 400, MUTED))
    o.append(rect(X(108), Y(214.5), 32 * s, 22.5 * s, "#ecebe7", LINE, 2))
    o.append(rect(X(196), Y(203.4), 11 * s, 11.4 * s, "#fff", LINE, 10))
    o.append(t(X(201.5), Y(206), "Deco B", 10, "middle", 500, INK))
    o.append(wire([(X(224), Y(220)), (X(224), Y(209)), (X(207), Y(198))], BLUE, 1.6))
    o.append(t(X(222), Y(215), "Cat6 from top floor", 9.5, "end", 400, BLUE))
    o.append(wire([(X(197), Y(193)), (X(178), Y(193)), (X(178), Y(76)), (X(190), Y(34))], VIN_S, 1.6, "5 3"))
    o.append(t(X(182), Y(184), "Deco power +", 8.5, "start", 500, VIN_S))
    o.append(t(X(182), Y(184) + 10, "patch lead in the", 8.5, "start", 500, VIN_S))
    o.append(t(X(182), Y(184) + 20, "upright's groove", 8.5, "start", 500, VIN_S))
    # oak uprights, worktop to ceiling, and the record ledge between them
    for ux in (44.5, 175.5):
        o.append(f'<rect x="{X(ux)}" y="{Y(220)}" width="{4.5*s}" height="{(220-76)*s}" fill="#e9d3b4" stroke="#b88a55"/>')
    o.append(rect(X(49), Y(155.4), 126.5 * s, 2.4 * s, "#e9dccb", "#b88a55", 1))
    for lx in (54, 86, 118, 150):
        o.append(f'<rect x="{X(lx)}" y="{Y(186.5)}" width="{31.4*s}" height="{31*s}" fill="{VIN_F}" stroke="{VIN_S}" stroke-opacity="0.6"/>')
    o.append(t(X(112), Y(172), "record ledge, top 155.4 · 4 LPs face-out", 9.5, "middle", 500, VIN_S))
    # left shelf, through-tenoned into the left upright
    o.append(rect(X(0), Y(156), 51 * s, 4 * s, "#e9dccb", "#c9b79f", 1))
    o.append(t(X(22), Y(156) - 6, "left shelf, 156", 10, "middle", 400, MUTED))
    # TV: bottom 81.2, top 151.7, centre 116.5
    o.append(rect(X(51), Y(151.7), 122.5 * s, 70.5 * s, "#ebeae6", "#c9c5bb", 4))
    o.append(t(X(112.25), Y(121), "LG OLED C6 55 in", 12.5, "middle", 650))
    o.append(t(X(112.25), Y(121) + 16, "122.5 × 70.5 cm · on LG's stand · centre ≈ 116.5 cm", 10.5, "middle", 400, MUTED))
    o.append(rect(X(112.25 - 23.5), Y(77.4), 47 * s, 1.6 * s, "#d8d5ce", "#bdb8ad", 1))
    # Series X
    o.append(rect(X(15), Y(82.3), 20.5 * s, 6.5 * s, GAME_F, GAME_S, 2))
    o.append(rect(X(17.7), Y(112.4), 15.1 * s, 30.1 * s, GAME_F, GAME_S, 3))
    o.append(t(X(25.3), Y(99), "Series X", 11, "middle", 600))
    o.append(t(X(25.3), Y(99) + 13, "on fan stand", 10, "middle", 400, MUTED))
    o.append(t(X(25.3), Y(112.4) - 5, "37 tall", 10, "middle", 400, MUTED))
    # soundbar
    o.append(rect(X(66.5), Y(81.8), 92 * s, 6 * s, SND_F, SND_S, 2))
    o.append(t(X(64), Y(78.5), "Soundbar", 10.5, "end", 400, INK))
    # turntable shelf + deck (top 113)
    o.append(rect(X(176.5), Y(113), 48 * s, 4 * s, "#e9dccb", "#c9b79f", 1))
    o.append(rect(X(179), Y(124.5), 42 * s, 10.5 * s, VIN_F, VIN_S, 3))
    o.append(t(X(200), Y(117.6), "Turntable", 11, "middle", 600))
    o.append(f'<rect x="{X(179)}" y="{Y(165)}" width="{42*s}" height="{40*s}" fill="none" stroke="#b9b4a8" stroke-dasharray="4 3"/>')
    o.append(t(X(200), Y(149), "keep 40 cm", 10, "middle", 400, MUTED))
    o.append(t(X(200), Y(149) + 12, "clear for lid", 10, "middle", 400, MUTED))
    # LP browser on the worktop (33.2 clear under the shelf)
    o.append(rect(X(176.5), Y(107.5), 48 * s, 31.7 * s, VIN_F, VIN_S, 3))
    o.append(t(X(200.5), Y(96), "LP browser", 10.5, "middle", 600))
    o.append(t(X(200.5), Y(96) + 12, "~50 face-out", 9.5, "middle", 400, MUTED))
    o.append(t(X(200.5), Y(96) + 24, "33.2 cm clear", 9.5, "middle", 400, MUTED))
    # 10-gang behind the TV (hidden)
    o.append(f'<rect x="{X(84)}" y="{Y(80)}" width="{56*s}" height="{4.2*s}" fill="none" stroke="{VIN_S}" stroke-dasharray="4 3"/>')
    o.append(t(X(112), Y(85), "10-gang behind the TV", 9, "middle", 500, VIN_S))
    # worktop 73-75.8
    o.append(rect(X(0), Y(76), 225 * s, 3 * s, "#e9dccb", "#c9b79f", 1))
    def cell(x1, x2, y1, y2, label, sub, kind):
        f, st = {"g": (GAME_F, GAME_S), "v": (VIN_F, VIN_S), "s": (SND_F, SND_S)}[kind]
        o.append(f'<rect x="{X(x1)}" y="{Y(y2)}" width="{(x2-x1)*s}" height="{(y2-y1)*s}" fill="{f}" stroke="{st}" stroke-opacity="0.55" stroke-width="1"/>')
        cy = (Y(y2) + Y(y1)) / 2
        o.append(t((X(x1) + X(x2)) / 2, cy - 1, label, 11, "middle", 600))
        o.append(t((X(x1) + X(x2)) / 2, cy + 12, sub, 9.5, "middle", 400, MUTED))
    P = 9.0   # plinth under bays 1-2
    # plinth
    o.append(f'<rect x="{X(0)}" y="{Y(P)}" width="{120*s}" height="{P*s}" fill="#efece6" stroke="#bdb8ad"/>')
    o.append(t(X(60), Y(P) + 15, "9 cm plinth (face frame covers it)", 9.5, "middle", 400, MUTED))
    # Bay 1 Xbox
    cell(1.6, 58.4, P + 46.4, P + 62.4, "Xbox One + brick", "16 cm row", "g")
    cell(1.6, 58.4, P + 28.6, P + 44.6, "Xbox 360 + brick", "16 cm row", "g")
    cell(1.6, 58.4, P + 1.6, P + 26.8, "Game drawer", "25.2 cm row · ~48 games", "g")
    o.append(t((X(1.6) + X(58.4)) / 2, (Y(P + 26.8) + Y(P + 1.6)) / 2 + 24, "2 bins + spine-up rows", 9.5, "middle", 400, MUTED))
    # Bay 2 PlayStation
    cell(61.6, 118.4, P + 38.7, P + 62.4, "PS3 + controllers", "23.7 cm row", "g")
    cell(61.6, 118.4, P + 20.4, P + 36.9, "PS2 + HDMI switch", "16.5 cm row", "g")
    cell(61.6, 118.4, P + 1.6, P + 18.6, "PS1 + RetroTINK", "17 cm row", "g")
    # Bay 3: custom ply carcass, two face-out record drawers
    cell(121.8, 178.2, 37.0, 71.2, "Upper record tray", "~90 LPs face-out", "v")
    o.append(t((X(121.8) + X(178.2)) / 2, (Y(71.2) + Y(37.0)) / 2 + 23, "+ ~120 singles face-out", 9.5, "middle", 400, MUTED))
    cell(121.8, 178.2, 1.8, 35.0, "Lower record tray", "~90 LPs face-out", "v")
    o.append(t((X(121.8) + X(178.2)) / 2, (Y(35.0) + Y(1.8)) / 2 + 23, "+ ~120 singles face-out", 9.5, "middle", 400, MUTED))
    o.append(t(150, 0, "", 1))
    # Sub bay
    o.append(f'<rect x="{X(181)}" y="{Y(73)}" width="{43*s}" height="{73*s}" fill="#fbfbfa" stroke="{LINE}"/>')
    o.append(rect(X(181.5), Y(73), 42 * s, 7.4 * s, VIN_F, VIN_S, 1))
    o.append(t(X(202.5), Y(68), "hidden drawer", 9, "middle", 600))
    o.append(f'<rect x="{X(180.5)}" y="{Y(65.6)}" width="{44*s}" height="{26.8*s}" fill="{VIN_F}" stroke="{VIN_S}" stroke-opacity="0.55"/>')
    o.append(t(X(202.5), Y(55), "Kit shelf", 10.5, "middle", 600))
    o.append(t(X(202.5), Y(55) + 12, "preamp, brush,", 9.5, "middle", 400, MUTED))
    o.append(t(X(202.5), Y(55) + 24, "~70 singles", 9.5, "middle", 400, MUTED))
    o.append(rect(X(180.5), Y(38.8), 44 * s, 1.8 * s, "#e9dccb", "#c9b79f", 1))
    o.append(rect(X(187.2), Y(5), 30 * s, 5 * s, SND_F, SND_S, 2))
    o.append(rect(X(191.5), Y(34.4), 21.4 * s, 29.4 * s, SND_F, SND_S, 4))
    o.append(f'<circle cx="{X(202.2)}" cy="{Y(20)}" r="{7.5*s}" fill="none" stroke="{SND_S}" stroke-width="1.2"/>')
    o.append(t(X(202.2), Y(20) + 3, "sub", 9.5, "middle", 600))
    o.append(t(X(202.2), Y(5) - 3, "5 cm riser", 8.5, "middle", 400, MUTED))
    # carcass outlines
    for a in (0, 60):
        o.append(f'<rect x="{X(a)}" y="{Y(73)}" width="{60*s}" height="{64*s}" fill="none" stroke="#8f8a80" stroke-width="1.3"/>')
    o.append(f'<rect x="{X(120)}" y="{Y(73)}" width="{60*s}" height="{73*s}" fill="none" stroke="#8f8a80" stroke-width="1.3"/>')
    # widths
    for a, b, lab in [(0, 60, "60 · BESTÅ"), (60, 120, "60 · BESTÅ"), (120, 180, "60 · ply carcass"), (180, 225, "45 · open")]:
        o.append(t((X(a) + X(b)) / 2, oy + 18, lab, 10.5, "middle", 400, MUTED))
    o.append(t(X(112.5), oy + 40, "225 cm wide · solid oak worktop 225 × 40 × 3, top at 76 · unit 10 cm off the wall, 10 cm cable slot behind the worktop", 10.5, "middle", 400, MUTED))
    # PC on left wall
    o.append(rect(X(-74), Y(157), 46, 47 * s, GAME_F, GAME_S, 6))
    o.append(rect(X(-82), Y(110), 66, 4 * s, "#e9dccb", "#c9b79f", 1))
    o.append(t(X(-74) + 23, Y(140), "PC", 12, "middle", 650))
    o.append(t(X(-74) + 23, Y(110) + 22, "wall shelf", 9.5, "middle", 400, MUTED))
    o.append(t(X(-74) + 23, Y(110) + 34, "top 110 cm", 9.5, "middle", 400, MUTED))
    o.append(wire([(X(-60), Y(104)), (X(-60), Y(6)), (X(-2), Y(6))], "#9a958b", 1.2, "4 3"))
    o.append(t(X(-58), Y(60), "HDMI + Cat6", 9.5, "start", 400, MUTED))
    o.append(t(X(-58), Y(60) + 12, "in trunking", 9.5, "start", 400, MUTED))
    ly = H - 12
    for i, (lab, f, st) in enumerate([("Gaming", GAME_F, GAME_S), ("Vinyl", VIN_F, VIN_S), ("Sound", SND_F, SND_S)]):
        o.append(rect(i * 100, ly - 11, 14, 14, f, st, 3)); o.append(t(i * 100 + 20, ly + 1, lab, 11, "start", 400, MUTED))
    o.append(f'<line x1="300" y1="{ly-4}" x2="326" y2="{ly-4}" stroke="#b9b4a8" stroke-dasharray="4 3"/>')
    o.append(t(332, ly + 1, "optional, or keep clear", 11, "start", 400, MUTED))
    # the double socket, low on the back wall behind bay 1
    o.append(f'<rect x="{X(-4)}" y="{Y(34.3)}" width="{3.5*s}" height="{8.6*s}" rx="1" fill="#fff" stroke="#d0573b" stroke-width="1.3"/>')
    o.append(t(X(-6), Y(30), "double socket on the", 8.5, "end", 600, "#d0573b"))
    o.append(t(X(-6), Y(30) + 10, "side wall, in front", 8.5, "end", 600, "#d0573b"))
    return svg(W, H, "\n".join(o), "The artisan oak wall: every console fits, every record faces out",
               "Front view to scale. Oak uprights and pegged shelves above; bays 1–2 on a 9 cm plinth, a ply bay with two face-out record trays, open sub bay below. Heights in cm")


# ------------------------------------------------------------------ record drawers detail
def drawer():
    import math
    W, H = 860, 590
    o = []
    s = 5.0
    ox, oy = 200, 520
    Z = lambda cm: ox + cm * s           # distance back from the unit front
    Y = lambda cm: oy - cm * s
    o.append(t(0, 62, "Side section through bay 3", 12, "start", 600))
    o.append(f'<line x1="{Z(-36)}" y1="{oy}" x2="{Z(52)}" y2="{oy}" stroke="#b9b4a8" stroke-width="1.4"/>')
    o.append(f'<line x1="{Z(50)}" y1="{Y(0)}" x2="{Z(50)}" y2="{Y(86)}" stroke="#b9b4a8" stroke-width="2"/>')
    o.append(t(Z(50) + 4, Y(84), "wall", 10, "start", 400, MUTED))
    # carcass: 18 mm ply, 73 tall, 40 deep, back open
    o.append(f'<rect x="{Z(0)}" y="{Y(73)}" width="{40*s}" height="{1.8*s}" fill="#efe2c8" stroke="#c9a77a"/>')
    o.append(f'<rect x="{Z(0)}" y="{Y(1.8)}" width="{40*s}" height="{1.8*s}" fill="#efe2c8" stroke="#c9a77a"/>')
    o.append(f'<rect x="{Z(0)}" y="{Y(73)}" width="{40*s}" height="{73*s}" fill="none" stroke="#8f8a80" stroke-width="1.3"/>')
    o.append(f'<rect x="{Z(0)}" y="{Y(76)}" width="{40*s}" height="{3*s}" fill="#e9dccb" stroke="#c9b79f"/>')
    o.append(t(Z(20), Y(76) - 5, "oak worktop 3, top at 76", 9.5, "middle", 500))
    lean = math.radians(10); hgt = 31.4 * math.cos(lean); dzl = 31.4 * math.sin(lean)
    def tier(yb, ghost=0.0, label=True):
        oz = -ghost
        op = 0.55 if ghost else 1
        da = 'stroke-dasharray="4 3"' if ghost else ""
        o.append(f'<rect x="{Z(oz)}" y="{Y(yb + 12)}" width="{40*s}" height="{12*s}" fill="none" stroke="#c9a77a" stroke-width="0.9" opacity="{op}" {da}/>')
        o.append(f'<rect x="{Z(oz)}" y="{Y(yb + 1.2)}" width="{40*s}" height="{1.2*s}" fill="#f1dfc4" stroke="#c9a77a" opacity="{op}"/>')
        for i in range(11):
            zb = oz + 2.6 + i * 2.6
            o.append(f'<line x1="{Z(zb)}" y1="{Y(yb + 1.2)}" x2="{Z(zb + dzl)}" y2="{Y(yb + 1.2 + hgt)}" stroke="{VIN_S}" stroke-width="{2.4 if i == 0 else 1.1}" opacity="{op}"/>')
        o.append(f'<rect x="{Z(oz - 0.6)}" y="{Y(yb + 5.0)}" width="{1.5*s}" height="{5.0*s}" fill="#e9c9a4" stroke="{VIN_S}" opacity="{op}"/>')
    tier(2.3)
    tier(37.0)
    tier(37.0, ghost=30)
    o.append(t(Z(-12), Y(37 + 36) , "pulls out 30+ cm", 10, "middle", 600, VIN_S))
    o.append(t(Z(21), Y(20), "~90 LPs face-out,", 10.5, "middle", 650))
    o.append(t(Z(21), Y(20) + 13, "leaning back 10°", 10, "middle", 400, MUTED))
    # dimension chain on the right of the carcass
    xx = Z(44.5)
    o.append(f'<line x1="{xx}" y1="{Y(0)}" x2="{xx}" y2="{Y(76)}" stroke="#cfcabf"/>')
    for h in (0, 1.8, 3.5, 34.4, 37.0, 38.2, 69.1, 71.2, 76):
        o.append(f'<line x1="{xx - 4}" y1="{Y(h)}" x2="{xx + 4}" y2="{Y(h)}" stroke="#9a958b"/>')
    for h, lab, dy in [(0, "0 floor", 4), (3.5, "3.5 lower base", -1), (34.4, "34.4 sleeves", 9), (38.2, "38.2 upper base", -2),
                       (69.1, "69.1 sleeves", 9), (76, "76 worktop", 0)]:
        o.append(t(xx + 7, Y(h) + dy, lab, 9, "start", 400, MUTED))
    o.append(t(Z(18), oy + 18, "carcass 18 mm birch ply, 60 × 40 × 73, back open · trays 40 deep on 400 mm runners", 10, "middle", 400, MUTED))
    o.append(t(Z(18), oy + 32, "thinner trays: 12 mm base, 9 mm sides, 5 cm oak lip · 2.6 and 2.1 cm finger room (top panel at 71.2)", 10, "middle", 400, MUTED))
    # plan view of one drawer
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
    return svg(W, H, "\n".join(o), "The record trays: every LP and single face-out, two tiers in one bay",
               "Bay 3. Section left, plan right. Pull a tray and flip through the covers like a record shop browser")


def sound():
    W, H = 760, 540
    o = []
    rx, ry, rw, rh = 10, 140, 740, 385
    o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" fill="#fff" stroke="{LINE}" stroke-width="1.4"/>')
    # alcove at top-left
    o.append(f'<rect x="{rx}" y="{ry-48}" width="{230}" height="{48}" fill="#fbfbfa" stroke="{LINE}" stroke-width="1.4"/>')
    o.append(f'<rect x="{rx+60}" y="{ry-28}" width="{120}" height="5" fill="{INK}"/>')
    o.append(rect(rx + 75, ry - 16, 90, 7, SND_F, SND_S, 2))
    o.append(rect(rx + 196, ry - 40, 26, 26, SND_F, SND_S, 4))
    o.append(t(rx + 236, ry - 22, "Subwoofer (wireless)", 11, "start", 600))
    o.append(t(rx + 120, ry - 54, "TV + soundbar", 11, "middle", 500, MUTED))
    o.append(wire([(rx + 209, ry - 12), (rx + 209, ry + 70)], BLUE, 2))
    o.append(f'<path d="M{rx+203},{ry+64} L{rx+209},{ry+76} L{rx+215},{ry+64}Z" fill="{BLUE}"/>')
    o.append(t(rx + 218, ry + 50, "faces the sofa", 10.5, "start", 400, MUTED))
    # door + stairs
    o.append(t(rx + 470, ry + 22, "Door", 11, "middle", 400, MUTED))
    o.append(f'<path d="M{rx+430},{ry} A 70 70 0 0 0 {rx+500},{ry+70}" fill="none" stroke="#c9c5bb" stroke-dasharray="4 3"/>')
    o.append(t(rx + 640, ry - 20, "Stairs", 11, "middle", 400, MUTED))
    for i in range(8):
        o.append(f'<rect x="{rx+560+i*20}" y="{ry-44}" width="20" height="40" fill="none" stroke="#dcd8cf"/>')
    # PC shelf
    o.append(f'<rect x="{rx}" y="{ry+150}" width="10" height="56" fill="#eceae4" stroke="{LINE}"/>')
    o.append(t(rx + 18, ry + 182, "PC shelf", 10.5, "start", 400, MUTED))
    # sofa + rears
    o.append(rect(rx + 60, ry + 290, 200, 52, "#fbfbfa", "#c9c5bb", 12))
    o.append(t(rx + 160, ry + 321, "Sofa", 12, "middle", 650))
    o.append(rect(rx + 22, ry + 296, 22, 22, SND_F, SND_S, 4))
    o.append(rect(rx + 276, ry + 296, 22, 22, SND_F, SND_S, 4))
    o.append(t(rx + 33, ry + 288, "Rear L", 10.5, "middle", 400, MUTED))
    o.append(t(rx + 287, ry + 288, "Rear R", 10.5, "middle", 400, MUTED))
    # link cable behind the sofa
    o.append(wire([(rx + 33, ry + 318), (rx + 33, ry + 356), (rx + 287, ry + 356), (rx + 287, ry + 318)], VIN_S, 1.6, "5 3"))
    o.append(t(rx + 160, ry + 374, "speaker link cable behind the sofa, along the skirting", 10, "middle", 500, VIN_S))
    o.append(f'<circle cx="{rx+305}" cy="{ry+332}" r="5" fill="#fff" stroke="{INK}"/>')
    o.append(t(rx + 314, ry + 336, "one socket for the rears", 10, "start", 400, MUTED))
    # viewing axis
    o.append(wire([(rx + 120, ry + 6), (rx + 120, ry + 282)], "#d0ccc2", 1, "4 4"))
    o.append(t(rx + 128, ry + 150, "viewing area", 10.5, "start", 400, MUTED))
    o.append(t(rx + 520, ry + 200, "Rest of the room", 11, "middle", 400, MUTED))
    # wireless hints from bar to rears
    o.append(f'<path d="M{rx+120},{ry-8} Q {rx+60},{ry+150} {rx+36},{ry+292}" fill="none" stroke="{SND_S}" stroke-dasharray="1 5" stroke-width="2" stroke-linecap="round"/>')
    o.append(t(rx + 52, ry + 120, "wireless", 9.5, "start", 400, SND_S))
    return svg(W, H, "\n".join(o), "The sub fires down the room at the sofa",
               "Living room from above, not to scale. Revised: the AX5100G rears are joined by a cable, so plan one socket and a run behind the sofa")


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
    o.append(f'<line x1="{Z(50)}" y1="{oy}" x2="{Z(50)}" y2="{Y(48)}" stroke="#b9b4a8" stroke-width="2"/>')
    o.append(t(Z(50) + 4, Y(44), "wall", 10, "start", 400, MUTED))
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
    o.append(t(Z(18), oy + 32, "5 cm free behind the box, then the 10 cm cable channel", 10, "middle", 400, MUTED))
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
    W, H = 860, 632
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
    o.append(t(696, 107, "fixed at the back of the sub bay", 10, "middle", 400, MUTED))
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
             "Load check: side A about 0.6 kW, side B up to about 0.8 kW with a launch PS3 running; well under the 13 A (3 kW) limit.",
             "Check the 10-gang is surge-protected; if not, use a surge-protected one for the TV and consoles.",
             "Label both switch ends: “A: leave on” and “B: retro”."]
    for i, n in enumerate(notes):
        o.append(t(0, 442 + i * 22, "• " + n, 10.5, "start", 400, INK))
    return svg(W, H, "\n".join(o), "Power map: your 10-gang plus one small switched strip",
               "Fifteen things need power; the 10-gang takes ten, a 6-way with individual switches takes the rest")


def routes():
    W, H = 860, 600
    o = []
    s = 2.3
    ox, oy = 250, 560
    X = lambda cm: ox + cm * s
    Y = lambda cm: oy - cm * s
    o.append(f'<rect x="{X(0)}" y="{Y(220)}" width="{225*s}" height="{220*s}" fill="#f8f7f4" stroke="{LINE}"/>')
    o.append(f'<line x1="{X(-110)}" y1="{oy}" x2="{X(235)}" y2="{oy}" stroke="#b9b4a8" stroke-width="1.4"/>')
    o.append(rect(X(0), Y(76), 225 * s, 3 * s, "#e9dccb", "#c9b79f", 1))
    o.append(rect(X(0), Y(73), 225 * s, 73 * s, "#fbfaf7", "#d6d2c8", 1))
    o.append(rect(X(51), Y(151.7), 122.5 * s, 70.5 * s, "#ebeae6", "#c9c5bb", 3))
    o.append(t(X(112), Y(119), "TV", 11, "middle", 600, MUTED))
    o.append(rect(X(0), Y(192), 225 * s, 4 * s, "#e9dccb", "#c9b79f", 1))
    o.append(rect(X(196), Y(203.4), 11 * s, 11.4 * s, "#fff", LINE, 8))
    o.append(t(X(201.5), Y(206), "Deco B", 9.5, "middle", 500))
    o.append(rect(X(84), Y(80), 56 * s, 4.2 * s, VIN_F, VIN_S, 2))
    o.append(t(X(112), Y(73) + 14, "10-gang", 9.5, "middle", 600, VIN_S))
    o.append(rect(X(183), Y(36), 30 * s, 10 * s, VIN_F, VIN_S, 2))
    o.append(t(X(198), Y(26) + 12, "6-way", 9.5, "middle", 600, VIN_S))
    # left wall PC (shown folded out to the left)
    o.append(f'<line x1="{X(-2)}" y1="{Y(0)}" x2="{X(-2)}" y2="{Y(220)}" stroke="#d6d2c8" stroke-dasharray="3 3"/>')
    o.append(t(X(-55), Y(214), "left wall, folded flat", 10, "middle", 400, MUTED))
    o.append(rect(X(-95), Y(110), 65 * s, 4 * s, "#e9dccb", "#c9b79f", 1))
    o.append(rect(X(-88), Y(157), 45 * s, 47 * s, GAME_F, GAME_S, 4))
    o.append(t(X(-65), Y(135), "PC", 11, "middle", 650))
    o.append(rect(X(-95), Y(158), 2 * s, 48 * s, "#d9b48a", VIN_S, 1))
    o.append(t(X(-94), Y(158) - 4, "screen", 9, "middle", 400, MUTED))
    # routes
    DATA = BLUE; MAINS = VIN_S; DC = "#2fa47a"
    # PC: down at the south end, along the skirting to the alcove, into the channel
    o.append(wire([(X(-91), Y(106)), (X(-91), Y(11)), (X(-2), Y(11)), (X(4), Y(11))], DATA, 2.2))
    o.append(t(X(-89), Y(60), "HDMI (active optical) + Cat6", 9.5, "start", 500, DATA))
    o.append(t(X(-89), Y(60) + 12, "down the trunking, then", 9.5, "start", 400, MUTED))
    o.append(t(X(-89), Y(60) + 24, "along the skirting", 9.5, "start", 400, MUTED))
    # Deco: DC lead + Cat6 down the right side to the slot
    for ux in (44.5, 175.5):
        o.append(f'<rect x="{X(ux)}" y="{Y(220)}" width="{4.5*s}" height="{(220-76)*s}" fill="#f1e1c8" stroke="#b88a55"/>')
    o.append(wire([(X(200), Y(198)), (X(178), Y(194)), (X(178), Y(76)), (X(196), Y(36))], DC, 2.2, "6 3"))
    o.append(wire([(X(176.5), Y(194)), (X(176.5), Y(76)), (X(224), Y(10)), (X(160), Y(10))], DATA, 1.6))
    o.append(t(X(183), Y(170), "Deco 12 V lead", 9.5, "start", 500, DC))
    o.append(t(X(183), Y(170) + 12, "+ patch lead to Switch 2,", 9.5, "start", 500, DATA))
    o.append(t(X(183), Y(170) + 24, "in the groove behind", 9.5, "start", 400, MUTED))
    o.append(t(X(183), Y(170) + 36, "the right upright", 9.5, "start", 400, MUTED))
    o.append(wire([(X(224), Y(220)), (X(207), Y(203))], DATA, 1.6))
    o.append(t(X(222), Y(214), "Cat6 in through the ceiling", 9, "end", 500, DATA))
    o.append(rect(X(-14), Y(34.3), 8 * s, 8.6 * s, "#fff", MAINS, 2))
    o.append(t(X(-10), Y(34.3) - 4, "socket (side wall)", 9, "middle", 600, MAINS))
    o.append(wire([(X(-10), Y(25.7)), (X(-10), Y(3)), (X(84), Y(3)), (X(84), Y(76))], MAINS, 1.8))
    o.append(wire([(X(84), Y(3)), (X(183), Y(3)), (X(183), Y(36))], MAINS, 1.8))
    # consoles up through the slot to the 10-gang
    for x in (30, 90):
        o.append(wire([(X(x), Y(49)), (X(x), Y(71)), (X(x + 60) if x == 30 else X(105), Y(75))], MAINS, 1.4))
    # legend
    for i, (c, lab, d) in enumerate([(DATA, "HDMI / Cat6 (data side of trunking)", None), (MAINS, "mains leads (mains side)", None), (DC, "low-voltage DC lead", "6 3")]):
        o.append(wire([(i * 280, 590), (i * 280 + 28, 590)], c, 2.2, d)); o.append(t(i * 280 + 36, 594, lab, 10.5, "start", 400, MUTED))
    return svg(W, H + 10, "\n".join(o), "Cable routes: everything ends in the channel behind the unit",
               "Front view, schematic. The left wall is folded flat so the PC's route is visible")


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
    """Side section through the whole wall (centre line), showing every layer."""
    W, H = 860, 700
    o = []
    s = 2.3
    ox, oy = 520, 640
    Z = lambda cm: ox - cm * s        # z: distance in front of the alcove back wall (wall at ox, room to the left)
    Y = lambda cm: oy - cm * s
    o.append(f'<line x1="{Z(-4)}" y1="{Y(0)}" x2="{Z(150)}" y2="{Y(0)}" stroke="#8f8a80" stroke-width="1.6"/>')
    o.append(f'<line x1="{Z(-4)}" y1="{Y(220)}" x2="{Z(150)}" y2="{Y(220)}" stroke="#8f8a80" stroke-width="1.6"/>')
    o.append(f'<rect x="{Z(0)}" y="{Y(220)}" width="18" height="{220*s}" fill="#dcd8cf"/>')
    o.append(t(Z(0) + 24, Y(120), "alcove back wall (solid)", 10, "start", 400, MUTED))
    o.append(t(Z(150), Y(220) - 6, "ceiling 220", 10, "start", 400, MUTED))
    o.append(t(Z(150), Y(0) + 16, "floor", 10, "start", 400, MUTED))
    # battens + slats from the worktop to the ceiling
    o.append(f'<rect x="{Z(30)}" y="{Y(220)}" width="{30*s}" height="{(220-76)*s}" fill="#f1e1c8" stroke="#b88a55" stroke-dasharray="5 3"/>')
    o.append(t(Z(15), Y(178), "oak upright", 9.5, "middle", 600, "#9c6a3f"))
    o.append(t(Z(15), Y(178) + 12, "30 deep, beside the TV", 9, "middle", 400, MUTED))
    o.append(f'<line x1="{Z(1)}" y1="{Y(218)}" x2="{Z(1)}" y2="{Y(78)}" stroke="#2fa47a" stroke-width="2" stroke-dasharray="4 3"/>')
    o.append(t(Z(-2), Y(150), "cable groove in the back", 9, "start", 500, "#2fa47a"))
    o.append(t(Z(-2), Y(150) + 11, "of the right upright", 9, "start", 400, MUTED))
    o.append(f'<line x1="{Z(1.5)}" y1="{Y(219.4)}" x2="{Z(4)}" y2="{Y(219.4)}" stroke="#e0a43a" stroke-width="3"/>')
    o.append(t(Z(-2), Y(214), "LED strip on the ceiling", 9, "start", 500, "#c07f1a"))
    # high shelf (30 deep) at 188-192
    o.append(rect(Z(34.6), Y(192), 30 * s, 4 * s, "#e9dccb", "#c9a77a", 1))

    o.append(t(Z(36), Y(192) + 4, "high shelf 30 deep, top 192:", 9.5, "end", 500))
    o.append(t(Z(36), Y(192) + 16, "housed into the uprights, cleats on the side walls", 9.5, "end", 400, MUTED))
    o.append(rect(Z(34), Y(218), 16 * s, 26 * s, GAME_F, GAME_S, 2))
    o.append(t(Z(26), Y(204), "books", 9.5, "middle", 500))
    # turntable shelf (dashed, it's off to the right of this section)
    o.append(rect(Z(49.6), Y(113), 45 * s, 4 * s, "none", "#9a958b", 1, 1.2, 'stroke-dasharray="4 3"'))
    o.append(t(Z(50) - 4, Y(111), "turntable shelf 45 deep, top 113 (beside the TV)", 9.5, "end", 400, MUTED))
    # TV on stand
    o.append(rect(Z(24), Y(151.7), 4 * s, 70.5 * s, "#e3e2de", "#b9b4a8", 2))
    o.append(rect(Z(34), Y(77.4), 23 * s, 1.6 * s, "#d8d5ce", "#bdb8ad", 1))
    o.append(t(Z(27), Y(119), "TV on its stand, centre 116.5", 9.5, "end", 500))
    # soundbar at front edge
    o.append(rect(Z(50), Y(81.8), 9 * s, 6 * s, SND_F, SND_S, 2))
    o.append(t(Z(45.5), Y(81.8) - 4, "soundbar", 9, "middle", 500))
    # worktop 40 deep, front flush with the frames at 50 from the wall
    o.append(rect(Z(50), Y(76), 40 * s, 3 * s, "#e9dccb", "#c9a77a", 1))
    o.append(t(Z(52), Y(76) + 2, "solid oak worktop 3 thick, 40 deep, top 76", 9.5, "end", 500))
    o.append(t(Z(52), Y(76) + 14, "10 cm cable slot behind it", 9.5, "end", 400, MUTED))
    # frame 40 deep from z=10 to 50 (front at 50 cm from the wall)
    o.append(f'<rect x="{Z(50)}" y="{Y(73)}" width="{40*s}" height="{64*s}" fill="#fbfaf7" stroke="#8f8a80" stroke-width="1.3"/>')
    o.append(f'<rect x="{Z(48)}" y="{Y(9)}" width="{36*s}" height="{9*s}" fill="#efe2c8" stroke="#c9a77a"/>')
    o.append(t(Z(30), Y(4.5) + 3.5, "9 cm plinth", 9, "middle", 500))
    o.append(t(Z(30), Y(41), "BESTÅ frame", 10, "middle", 600))
    o.append(t(Z(30), Y(41) + 12, "60 × 40 × 64", 9.5, "middle", 400, MUTED))
    o.append(t(Z(30), Y(41) + 24, "back panel off", 9.5, "middle", 400, MUTED))
    o.append(rect(Z(10), Y(57), 10 * s, 6 * s, "#f1dfc4", "#c9a77a", 1))

    o.append(f'<line x1="{Z(10)}" y1="{Y(67)}" x2="{Z(0)}" y2="{Y(67)}" stroke="#555" stroke-width="2.5"/>')
    o.append(rect(Z(8), Y(34), 6 * s, 30 * s, "#eef2fb", BLUE, 1, 1, 'stroke-dasharray="3 2"'))
    for yy, lab, col in [(67, "anti-tip bracket into the wall", INK), (54, "10 cm spacer block", INK), (18, "two-compartment trunking (mains | data)", BLUE)]:
        o.append(f'<line x1="{Z(1)}" y1="{Y(yy)}" x2="{Z(-12)}" y2="{Y(yy)}" stroke="#b9b4a8"/>')
        o.append(t(Z(-13), Y(yy) + 3.5, lab, 9.5, "start", 500, col))
    # face frame + drawer lip (stage 2)
    o.append(rect(Z(52), Y(73), 2 * s, 73 * s, "#ecd3ae", "#b88a55", 0))
    o.append(t(Z(53) - 4, Y(40), "oak face frame 20 mm, 0–73;", 9.5, "end", 500, "#9c6a3f"))
    o.append(t(Z(53) - 4, Y(40) + 12, "its bottom rail hides the plinth", 9.5, "end", 400, MUTED))
    # dims
    o.append(f'<line x1="{Z(0)}" y1="{Y(-8)}" x2="{Z(50)}" y2="{Y(-8)}" stroke="{MUTED}"/>')
    o.append(t((Z(0) + Z(50)) / 2, Y(-8) + 14, "50 cm: wall to the frame and worktop fronts (the alcove opening)", 9.5, "middle", 400, MUTED))
    return svg(W, H, "\n".join(o), "How the wall goes together, layer by layer",
               "Side section through the centre of the alcove, to scale. Room on the left")


# ------------------------------------------------------------------ joinery details (artisan oak version)
def joints():
    W, H = 860, 490
    o = []
    OAKF, OAKS, END = "#ecd3ae", "#b88a55", "#d7b483"
    k = 7.0
    # ---- A: through-tenon from above
    ax, ay = 40, 110            # top-left of the drawing area (wall line)
    PX = lambda c: ax + 60 + c * k      # x: across the alcove (upright at 0..4.5)
    PZ = lambda c: ay + c * k           # z: distance from the back wall
    o.append(t(0, 70, "A · Wedged through-tenon, from above", 12, "start", 600))
    o.append(f'<line x1="{PX(-9)}" y1="{PZ(0)}" x2="{PX(10)}" y2="{PZ(0)}" stroke="#8f8a80" stroke-width="3"/>')
    o.append(t(PX(10) + 4, PZ(0) + 4, "wall", 10, "start", 400, MUTED))
    o.append(rect(PX(-9), PZ(0), 9 * k, 25 * k, OAKF, OAKS, 0))
    o.append(t(PX(-4.5), PZ(12), "shelf", 10, "middle", 500))
    o.append(t(PX(-4.5), PZ(12) + 12, "25 deep", 9.5, "middle", 400, MUTED))
    o.append(t(PX(-4.5), PZ(25) + 14, "room ↓", 9.5, "middle", 400, MUTED))
    o.append(rect(PX(0), PZ(0), 4.5 * k, 30 * k, "#f4e3c6", OAKS, 0))
    o.append(t(PX(2.25), PZ(33), "upright", 10, "middle", 500))
    o.append(t(PX(2.25), PZ(33) + 12, "4.5 × 30", 9.5, "middle", 400, MUTED))
    for zc in (6.5, 18.5):
        o.append(rect(PX(0), PZ(zc - 3.5), 6.5 * k, 7 * k, END, OAKS, 0, 1, 'fill-opacity="0.85"'))
        o.append(f'<line x1="{PX(4.5)}" y1="{PZ(zc)}" x2="{PX(6.5)}" y2="{PZ(zc)}" stroke="#4a2f19" stroke-width="2"/>')
    o.append(t(PX(7.3), PZ(6.5) + 4, "tenon 7 wide,", 9.5, "start", 500))
    o.append(t(PX(7.3), PZ(6.5) + 16, "2.4 thick", 9.5, "start", 400, MUTED))
    o.append(t(PX(7.3), PZ(18.5) + 4, "2 cm proud,", 9.5, "start", 500))
    o.append(t(PX(7.3), PZ(18.5) + 16, "chamfered", 9.5, "start", 400, MUTED))
    # ---- B: through-tenon from the front
    bx = 330
    FX = lambda c: bx + 60 + c * k
    FY = lambda c: ay + 120 - c * k
    o.append(t(bx, 70, "B · The same joint from the front", 12, "start", 600))
    o.append(rect(FX(0), FY(14), 4.5 * k, 28 * k, "#f4e3c6", OAKS, 0))
    o.append(rect(FX(-11), FY(2), 11 * k, 4 * k, OAKF, OAKS, 0))
    # tenon through the mortise (2.4 thick, 0.8 shoulders), mortise flared on the outer face
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
    # ---- C: housed shelf with stub tenon and peg
    cx = 640
    QX = lambda c: cx + 40 + c * k
    o.append(t(cx - 20, 70, "C · Housed shelf, pegged", 12, "start", 600))
    o.append(f'<line x1="{QX(-8)}" y1="{PZ(0)}" x2="{QX(12)}" y2="{PZ(0)}" stroke="#8f8a80" stroke-width="3"/>')
    o.append(rect(QX(-8), PZ(0), 9.2 * k, 30 * k, OAKF, OAKS, 0))
    o.append(rect(QX(0), PZ(0), 4.5 * k, 30 * k, "#f4e3c6", OAKS, 0, 1, 'fill-opacity="0.9"'))
    o.append(rect(QX(0), PZ(0.5), 1.2 * k, 29.5 * k, OAKF, OAKS, 0, 0.8, 'stroke-dasharray="2 2"'))
    o.append(rect(QX(1.2), PZ(19), 1.3 * k, 8 * k, END, OAKS, 0))
    c_ = (QX(1.6), PZ(27.5))
    o.append(f'<rect x="{QX(1.1)}" y="{PZ(24.5)}" width="{1.0*k}" height="{5.5*k}" fill="#7a4e2b"/>')
    o.append(t(QX(5.5), PZ(4) + 4, "housing 1.2 deep,", 9.5, "start", 500))
    o.append(t(QX(5.5), PZ(4) + 16, "full depth", 9.5, "start", 400, MUTED))
    o.append(t(QX(5.5), PZ(20) + 4, "stub tenon 2.5", 9.5, "start", 500))
    o.append(t(QX(5.5), PZ(26.5) + 4, "10 mm oak peg", 9.5, "start", 500))
    o.append(t(QX(5.5), PZ(26.5) + 16, "from the front edge", 9.5, "start", 400, MUTED))
    o.append(t(QX(-4), PZ(33), "high shelf / ledge", 10, "middle", 500))
    o.append(t(QX(-4), PZ(33) + 12, "seen from above", 9.5, "middle", 400, MUTED))
    notes = ["Through-tenons (A, B): the left shelf (top 156) and the turntable shelf (top 113) pass through the uprights and show 2 cm on the TV side.",
             "Housed and pegged (C): the three lengths of the high shelf (top 192) and the record ledge (top 155.4). The peg shows as a dark dot on the upright's face.",
             "Uprights stand on the worktop on two 10 mm dowels each, scribed to the ceiling, with two concealed brackets each into the solid back wall."]
    for i, n in enumerate(notes):
        o.append(t(0, 420 + i * 20, "• " + n, 10, "start", 400, INK))
    return svg(W, H, "\n".join(o), "Artisan oak: how the joints work",
               "Drawn to scale at 7 px per cm. The joints carry the load and are left on show, finished in hardwax oil")


if __name__ == "__main__":
    for name, fn in [("network", network), ("front", front), ("drawer", drawer), ("sound", sound), ("game", game_drawer), ("av", av), ("power", power), ("routes", routes), ("pcshelf", pc_shelf), ("section", section)]:
        open(f"d_{name}.svg", "w").write(fn())
    print("ok")


# ------------------------------------------------------------------ house plan (v9, from the Rightmove floor plans, corrected)
WALL = "#3a3a38"; ROOMF = "#fbfaf6"; HATCH = "#c9c3b5"

def house():
    """Three floors side by side, to scale (about 52 px per m), traced from the agent's plan with the
    alcoves, chimney breast, kitchen brick cupboard and sloped ceilings added."""
    W, H = 860, 610
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
        X = lambda m: ox + m * k
        Y = lambda m: oy + m * k
        return X, Y
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
    # lower ground floor
    X, Y = floor(14, 92, "Lower ground floor", "kitchen, WC · about 34 m²")
    room(X, Y, 0, 0, 1.04, 1.9, "WC", None, "#eaf2f4")
    room(X, Y, 0, 1.9, 1.04, 3.69, None)
    o.append(t(X(0.52), Y(2.9), "stairs", 8.5, "middle", 400, MUTED))
    room(X, Y, 1.04, 0, 4.81, 3.69, "Kitchen", "3.79 × 3.66 m", "#fdf6e3")
    room(X, Y, 0, 3.69, 1.77, 5.5, "Store")
    o.append(f'<rect x="{X(1.77):.1f}" y="{Y(3.69):.1f}" width="{(4.81-1.77)*k:.1f}" height="{(8.15-3.69)*k:.1f}" fill="#e6e3dc" stroke="{WALL}" stroke-width="2.2"/>')
    o.append(t(X(3.3), Y(5.9), "under the garage", 8.5, "middle", 400, MUTED))
    # brick cupboard: bottom middle of the kitchen, under the living room chimney breast (size to confirm)
    o.append(f'<rect x="{X(1.90):.1f}" y="{Y(3.10):.1f}" width="{0.85*k:.1f}" height="{0.59*k:.1f}" fill="url(#brick)" stroke="#8f5b45" stroke-width="1.4"/>')
    o.append(t(X(2.32), Y(3.02), "brick cupboard", 8.5, "middle", 650, "#8f5b45"))
    deco(X, Y, 2.95, 2.95, "Deco C", "start")
    o.append(t(X(3.1), Y(2.6), "on the outside of the", 8, "start", 400, MUTED))
    o.append(t(X(3.1), Y(2.6) + 10, "cupboard, up high", 8, "start", 400, MUTED))
    o.append(f'<circle cx="{X(2.85):.1f}" cy="{Y(3.55):.1f}" r="4" fill="{BLUE}"/>')
    o.append(t(X(2.95), Y(3.55) + 4, "Cat6 drops in from the media wall above", 8, "start", 600, BLUE))
    o.append(t(X(1.05), Y(4.3), "", 8))
    # ground floor
    X, Y = floor(300, 92, "Ground floor", "living room, hall, garage · about 39 m²")
    room(X, Y, 0, 0, 4.95, 3.65, None, None, "#fdf6e3")
    # chimney breast projecting into the room from the south wall, alcove to its east
    o.append(f'<rect x="{X(1.85):.1f}" y="{Y(3.15):.1f}" width="{0.85*k:.1f}" height="{0.5*k:.1f}" fill="url(#brick)" stroke="{WALL}" stroke-width="2"/>')
    o.append(f'<rect x="{X(2.70):.1f}" y="{Y(3.15):.1f}" width="{2.25*k:.1f}" height="{0.5*k:.1f}" fill="#e9d3b4" stroke="#b88a55" stroke-width="1.2"/>')
    o.append(t(X(4.3), Y(3.45), "media wall", 8.5, "middle", 650, "#7a5130"))
    o.append(t(X(1.1), Y(1.0), "Living room", 10, "middle", 650))
    o.append(t(X(1.1), Y(1.0) + 13, "4.95 × 3.65 m", 8.5, "middle", 400, MUTED))
    o.append(f'<rect x="{X(2.16):.1f}" y="{Y(-0.06):.1f}" width="{1.57*k:.1f}" height="5" fill="#cfe3f2" stroke="#7aa6c8"/>')
    o.append(t(X(2.95), Y(-0.06) - 4, "window", 8, "middle", 400, MUTED))
    room(X, Y, 0, 3.65, 1.96, 7.3, "Hall")
    room(X, Y, 1.96, 3.65, 5.05, 8.15, "Garage")
    room(X, Y, 0, 7.3, 0.5, 8.15)
    room(X, Y, 1.25, 7.3, 1.96, 8.15)
    o.append(f'<path d="M{X(1.0):.1f},{Y(3.65):.1f} A{0.8*k:.1f},{0.8*k:.1f} 0 0 0 {X(1.8):.1f},{Y(2.85):.1f}" fill="none" stroke="#9a958b" stroke-dasharray="3 2"/>')
    o.append(t(X(1.0), Y(3.2), "door", 8, "start", 400, MUTED))
    deco(X, Y, 2.94, 3.55, "Deco B", "start", 9)
    o.append(f'<circle cx="{X(2.70):.1f}" cy="{Y(1.45):.1f}" r="4" fill="#e8b53f" stroke="#8a6a1a"/>')
    o.append(t(X(2.62), Y(1.62) + 10, "spot bar", 8, "end", 500, "#8a6a1a"))
    for i in range(int(4.95 * 4)):
        o.append(f'<circle cx="{X(0.12 + i*0.25):.1f}" cy="{Y(0.06):.1f}" r="1" fill="#e0a43a"/>')
    # 1st floor
    X, Y = floor(590, 92, "1st floor", "bedrooms, bathroom · about 40 m²")
    room(X, Y, 0, 0, 1.96, 2.36, "Bathroom", "2.04 × 2.38 m", "#eaf2f4")
    room(X, Y, 1.96, 0, 5.05, 3.69, "Bedroom 2", "2.91 × 3.65 m", "#fdf3d6")
    room(X, Y, 0, 2.36, 1.96, 5.95, "Landing")
    room(X, Y, 1.96, 3.69, 5.05, 8.15, None, None, "#fdf3d6")
    o.append(t(X(3.9), Y(5.6), "Master", 10, "middle", 650)); o.append(t(X(3.9), Y(5.6) + 13, "2.91 × 4.45 m", 8.5, "middle", 400, MUTED))
    room(X, Y, 1.96, 3.69, 2.96, 4.75, None, None, "#ece8df")
    o.append(t(X(2.46), Y(4.12), "airing", 8, "middle", 650))
    o.append(t(X(2.46), Y(4.12) + 10, "cupboard", 8, "middle", 650))
    room(X, Y, 0, 5.95, 1.96, 8.15, "Bedroom 3", "2.04 × 2.17 m", "#fdf3d6")
    for (x1, x2) in ((0, 1.96), (1.96, 5.05)):
        o.append(f'<rect x="{X(x1):.1f}" y="{Y(0):.1f}" width="{(x2-x1)*k:.1f}" height="{0.9*k:.1f}" fill="url(#slope)" opacity="0.8"/>')
    o.append(t(X(2.5), Y(0.55), "sloped ceiling, low at the back wall", 8, "middle", 600, "#6b6455"))
    deco(X, Y, 4.05, 6.6, "Deco A + Switch 1", "end", 10)
    o.append(t(X(4.0), Y(6.6) + 14, "where the Hub 5 is", 8, "end", 400, MUTED))
    o.append(t(X(4.0), Y(6.6) + 24, "(room to confirm)", 8, "end", 400, MUTED))
    o.append(wire([(X(4.05), Y(6.6)), (X(4.05), Y(5.0)), (X(2.8), Y(5.0)), (X(2.8), Y(4.0))], BLUE, 2.4))
    o.append(f'<circle cx="{X(2.8):.1f}" cy="{Y(4.0):.1f}" r="4" fill="{BLUE}"/>')
    o.append(t(X(1.9), Y(5.2), "Cat6 down through the", 8.5, "end", 600, BLUE))
    o.append(t(X(1.9), Y(5.2) + 11, "airing cupboard floor", 8.5, "end", 600, BLUE))
    # legend
    ly = H - 34
    o.append(f'<circle cx="8" cy="{ly - 4}" r="6" fill="#fff" stroke="{BLUE}" stroke-width="2.2"/>'); o.append(t(20, ly, "Deco unit", 10, "start", 400, MUTED))
    o.append(wire([(100, ly - 4), (128, ly - 4)], BLUE, 2.4)); o.append(t(134, ly, "Cat6 run", 10, "start", 400, MUTED))
    o.append(f'<rect x="200" y="{ly - 10}" width="16" height="12" fill="url(#brick)"/>'); o.append(t(222, ly, "chimney breast / brick cupboard (sizes to confirm)", 10, "start", 400, MUTED))
    o.append(f'<rect x="490" y="{ly - 10}" width="16" height="12" fill="url(#slope)"/>'); o.append(t(512, ly, "sloped ceiling", 10, "start", 400, MUTED))
    o.append(f'<circle cx="610" cy="{ly - 4}" r="2" fill="#e0a43a"/><circle cx="618" cy="{ly - 4}" r="2" fill="#e0a43a"/>'); o.append(t(628, ly, "LED strip round the ceiling", 10, "start", 400, MUTED))
    o.append(t(0, H - 10, "Traced from the agent's plan (north, the window side, at the top), which leaves out the alcoves, the chimney breast, the brick cupboard and the slopes; those are added here from your notes and photos.", 9, "start", 400, MUTED))
    return svg(W, H, "\n".join(o), "The house: where the Decos and Cat6 runs go",
               "Each floor drawn to the same scale. Both Cat6 runs drop through the airing cupboard, which sits right over the media wall's corner")


def living_plan():
    """The living room from above, to scale (90 px per m), with the new layout."""
    W, H = 860, 520
    k = 90.0
    ox, oy = 150, 70
    X = lambda m: ox + m * k
    Y = lambda m: oy + m * k
    o = []
    o.append('<defs><pattern id="brick2" width="10" height="6" patternUnits="userSpaceOnUse"><rect width="10" height="6" fill="#d9a48a"/>'
             '<path d="M0,3 H10 M5,0 V3 M0,3 V6 M10,3 V6" stroke="#b5785e" stroke-width="0.8"/></pattern></defs>')
    o.append(f'<rect x="{X(0)}" y="{Y(0)}" width="{4.95*k}" height="{3.65*k}" fill="#fbfaf6" stroke="{WALL}" stroke-width="3"/>')
    # window and radiator on the north wall
    o.append(f'<rect x="{X(2.16)}" y="{Y(0) - 4}" width="{1.57*k}" height="8" fill="#cfe3f2" stroke="#7aa6c8"/>')
    o.append(t(X(2.95), Y(0) - 10, "window, radiator under it", 9.5, "middle", 400, MUTED))
    # chimney breast and alcove
    o.append(f'<rect x="{X(1.85)}" y="{Y(3.15)}" width="{0.85*k}" height="{0.5*k}" fill="url(#brick2)" stroke="{WALL}" stroke-width="2"/>')
    o.append(t(X(2.27), Y(3.15) - 6, "chimney breast", 9, "middle", 600, "#8f5b45"))
    # media unit (225 x 40 base, 10 cm off the back wall) and uprights
    o.append(f'<rect x="{X(2.70)}" y="{Y(3.15)}" width="{2.25*k}" height="{0.40*k}" fill="#e9d3b4" stroke="#b88a55" stroke-width="1.4"/>')
    for ux in (2.70 + (2.25 - 0.445 - 0.045), 2.70 + (2.25 - 1.755 - 0.045)):
        o.append(f'<rect x="{X(ux)}" y="{Y(3.35)}" width="{0.045*k}" height="{0.30*k}" fill="#b88a55"/>')
    o.append(f'<rect x="{X(3.215)}" y="{Y(3.38)}" width="{1.225*k}" height="{0.04*k}" fill="#222"/>')
    o.append(t(X(3.83), Y(3.15) + 13, "media wall", 9.5, "middle", 650, "#7a5130"))
    # sofa opposite the TV, against the window wall
    o.append(rect(X(2.55), Y(0.08), 2.05 * k, 0.92 * k, "#ecebe6", "#b9b4a8", 10))
    o.append(t(X(3.58), Y(0.6), "Sofa", 11, "middle", 650))
    o.append(rect(X(3.25), Y(1.35), 0.95 * k, 0.5 * k, "#f3efe6", "#c9c5bb", 6))
    o.append(t(X(3.72), Y(1.66), "coffee table", 8.5, "middle", 400, MUTED))
    # PC shelf and socket on the east wall
    o.append(rect(X(4.95) - 0.32 * k, Y(1.20), 0.32 * k, 0.65 * k, GAME_F, GAME_S, 3))
    o.append(t(X(4.95) - 0.16 * k, Y(1.20) - 6, "PC shelf", 9, "middle", 600))
    o.append(rect(X(4.95) - 6, Y(2.86), 6, 0.15 * k, "#fff", "#d0573b", 1))
    o.append(t(X(4.95) + 8, Y(2.93) + 3, "double socket, about 30 cm up", 9, "start", 600, "#d0573b"))
    # door
    o.append(f'<path d="M{X(1.0)},{Y(3.65)} A{0.8*k},{0.8*k} 0 0 0 {X(1.8)},{Y(2.85)}" fill="none" stroke="#9a958b" stroke-dasharray="3 2"/>')
    o.append(t(X(1.4), Y(3.65) + 16, "door to the hall", 9, "middle", 400, MUTED))
    # rear speakers and sub
    o.append(rect(X(2.30), Y(0.20), 0.18 * k, 0.18 * k, SND_F, SND_S, 3)); o.append(rect(X(4.66), Y(0.20), 0.18 * k, 0.18 * k, SND_F, SND_S, 3))
    o.append(t(X(2.39), Y(0.5) + 6, "rear", 8, "middle", 400, MUTED)); o.append(t(X(4.75), Y(0.5) + 6, "rear", 8, "middle", 400, MUTED))
    # spot bar on the existing rose, heads aimed
    o.append(f'<rect x="{X(2.28)}" y="{Y(1.44)}" width="{0.84*k}" height="4" fill="#ddd9d0" stroke="#999"/>')
    for dx, col, ax, ay in [(0.315, "#a9c7ab", 0.35, 0.76), (0.105, "#a7d0d8", -0.05, 0.78), (-0.105, "#e8b53f", -0.3, -0.25), (-0.315, "#e79c95", -0.55, -0.42)]:
        cx = X(2.70 + dx); cy = Y(1.46)
        o.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="{col}" stroke="#555" stroke-width="0.6"/>')
        o.append(arrow(cx, cy, cx + ax * 60, cy + ay * 60, col, 1.4))
    o.append(t(X(2.0), Y(1.45) + 4, "spotlight bar on the existing rose", 9, "end", 600, "#8a6a1a"))
    # LED strip round the ceiling
    o.append(f'<rect x="{X(0) + 5}" y="{Y(0) + 5}" width="{4.95*k - 10}" height="{3.65*k - 10}" fill="none" stroke="#e0a43a" stroke-width="1.6" stroke-dasharray="1 4" stroke-linecap="round"/>')
    # viewing distance
    o.append(f'<line x1="{X(3.83)}" y1="{Y(0.72)}" x2="{X(3.83)}" y2="{Y(3.38)}" stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="5 3"/>')
    o.append(t(X(3.83) + 6, Y(2.35), "eyes to screen", 9.5, "start", 650, BLUE))
    o.append(t(X(3.83) + 6, Y(2.35) + 12, "about 2.7–3.2 m", 9.5, "start", 400, BLUE))
    # dims
    o.append(f'<line x1="{X(0)}" y1="{Y(3.65) + 34}" x2="{X(4.95)}" y2="{Y(3.65) + 34}" stroke="{MUTED}"/>')
    o.append(t(X(2.47), Y(3.65) + 48, "4.95 m (agent's plan)", 9.5, "middle", 400, MUTED))
    o.append(f'<line x1="{X(0) - 26}" y1="{Y(0)}" x2="{X(0) - 26}" y2="{Y(3.65)}" stroke="{MUTED}"/>')
    o.append(t(X(0) - 32, Y(1.82), "3.65 m", 9.5, "end", 400, MUTED))
    o.append(t(X(0) - 32, Y(1.82) + 12, "+ 0.5 alcove?", 9, "end", 400, MUTED))
    o.append(t(X(4.95) + 8, Y(0.3), "east wall", 9, "start", 400, MUTED))
    return svg(W, H, "\n".join(o), "The living room from above, with the new layout",
               "To scale. Sofa opposite the TV against the window wall; the two back spots light the books and records, the two front ones the room, none at the screen")
