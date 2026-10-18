"""v12 fit proof (v11 layout; v12 adds the six- and eight-seat checks against the sub): every item that goes in the wall, its size and where the size comes from, the space it goes
into, what's left, and a verdict. Spares are computed from geometry.py, so the tables can't drift from the
renders and diagrams. build_doc.py turns ZONES into one table per zone and SOURCES into the numbered list."""
import geometry as G

# ---------------------------------------------------------------- sources (numbered in the plan)
SOURCES = {
    "room": "Your hand-measured sketch of the living room, in mm (alcove 1860 × 380, chimney breast 1175, ceiling 2350)",
    "lg": "LG: OLED55C6 specifications: 1222 × 703 × 45.1 mm without stand, 1222 × 757 × 230 mm with stand, stand 470 × 230 mm, 14.1/15.9 kg, VESA 300 × 200 (lg.com, OLED55C6 product pages)",
    "hisense": "Trusted Reviews and Expert Reviews, Hisense AX5100G reviews: soundbar 920 × 60 × 90 mm, subwoofer 214 × 294 × 304 mm (W × H × D) with a rear-firing port, rear speakers 90 × 144 × 109 mm",
    "xbox": "Wikipedia, Xbox Series X: 151 × 151 × 301 mm; Pure Xbox (Nov 2020) quoting Microsoft: at least 4 cm clear above the console on an open stand, 10–15 cm recommended on all sides",
    "besta": "IKEA: BESTÅ frame 60 × 40 × 64 cm (10247379); BESTÅ shelf 56 × 36 cm, 20 kg maximum load",
    "sg108": "TP-Link: TL-SG108 specifications, 158 × 101 × 25 mm (tp-link.com)",
    "deco": "Laptop Outlet: TP-Link Deco X1500 3-pack listing, 110 × 110 × 114 mm per unit",
    "atlp120": "Audio-Technica: AT-LP120XUSB specifications, 452 × 352 × 141.6 mm, 8 kg without dust cover (audio-technica.com)",
    "rt6x": "RetroTINK: RetroTINK-6X CE shop page (power 5 V 2 A by USB; no size published)",
    "ugreen": "UGREEN: 5-in-1 4K60 HDMI switch CM568 (90512), 127 × 59 × 25 mm",
    "xb1psu": "Original Xbox One power supply: 17 × 7.5 × 4.8 cm (6.69 × 2.96 × 1.88 in), as listed by several replacement-PSU sellers",
    "consoles": "Wikipedia: Comparison of PlayStation consoles (PS1 270 × 188 × 60, PS2 302 × 183 × 78, PS3 325 × 274 × 98 mm); Xbox One (333 × 274 × 79 mm); Neowin: official Xbox 360 dimensions (309 × 258 × 83 mm)",
    "media": "Record and case sizes: LP sleeve 31.4 cm (12⅜ in); 7-inch sleeve 18.3–18.4 cm; DVD-style keep case 19 × 13.5 × 1.4 cm; Xbox One case 17 × 13.5 × 1.1–1.2 cm (videogamecasesize.info; Walvis Products; Wikipedia: Keep case)",
    "wolston": "Dunelm: Elements Wolston 4-light spotlight bar, £49: 84 × 16 cm, 22.4 cm drop, shades 15 cm, E14 6 W max (dunelm.com, product 1000189449)",
    "runners": "Emuca heavy-duty full-extension runners, 400 mm, 68 kg per pair; Accuride DZ3832EC 350 mm, 43 kg; runner fitting allowance 12.5 mm a side",
    "x360psu": "Xbox 360 original 203 W power supply: no Microsoft size published; Akyga's 203 W replacement for it (AK-PD-14) is 210 × 77 × 55 mm (b2b.akyga.com), so an allowance of 21 × 10 × 6 cm is used here (measure yours)",
    "lid": "Turntable Lab: Audio-Technica replacement dust cover for the AT-LP120XUSB (705-140XP-1815), 17.375 × 13.625 × 2.75 in (44.1 × 34.6 × 7.0 cm)",
    "hebgo": "Häfele UK, Technology catalogue 2023, p. 7.206: Hebgo heavy-duty folding bracket 287.43.428, arm 580 mm, height 220 mm, 500 kg per pair, locks automatically when raised; up to 800 mm between brackets (Häfele 287.43.419 listing)",
    "liftoff": "Screwfix: Union PowerLoad lift-off hinges, 100 × 88 mm, 3-pack (5938T), 120 kg maximum door weight",
    "legs": "Emuca: table legs Ø60 mm, 710 mm, height adjustable 710–730 mm, 50 kg per leg, screw-on mounting plate (set of 4)",
    "terje": "IKEA: TERJE folding chair, 43 W × 49 D × 78 H cm, seat height 48 cm, tested for 110 kg",
    "dining": "Book a Builder UK, small dining room ideas: 600 mm of table edge per diner; table edge to a wall 600 mm tight minimum, 750 mm to aim for, 1000–1100 mm to walk behind; dining height about 750 mm",
    "sofa": "M&S: Easy Velvet left corner sofa, 247 W × 168 D × 80 H cm: a typical corner sofa, used until yours is measured",
}
ORDER = list(SOURCES)


def ref(*keys):
    return "<sup>" + ",".join(str(ORDER.index(k) + 1) for k in keys) + "</sup>"


# ---------------------------------------------------------------- the zones
PASS, TIGHT, CHECK, NO = "Fits", "Fits, tight", "Check", "Doesn't fit"


def r1(x):
    if abs(x - G.TV_CENTRE) < 1e-6:
        return "116.5"            # 116.55: quoted as 116.5 throughout the plan
    return f"{x:.2f}".rstrip("0").rstrip(".")


def zones():
    g = G
    sx, sh, sd = g.SERIES_X
    fx, fy, fz = g.FAN_STAND
    eye_lo, eye_hi = g.EYE_HEIGHT
    sight = lambda e: g.TV_BOTTOM + (e - g.TV_BOTTOM) * 24.0 / g.VIEW_DIST
    sb_top = g.WORKTOP + g.SOUNDBAR[1]
    lp4 = 4 * g.LP
    deck_side = (g.RZ_W - g.DECK[0]) / 2
    sx_side = (g.RZ_W - fx) / 2
    pre_bottom = g.RZ_SHELF_TOP - g.RZ_SHELF_T - g.PREAMP[1]
    wrap_len = g.WRAP_Z[0] - g.WRAP_Z[1]
    pc_len = g.PC_SHELF_Z[0] - g.PC_SHELF_Z[1]
    under = g.PC_SHELF_TOP - g.PC_SHELF_T
    drawer_out = g.BASE_FRONT_Z - 35.0
    tw, td, tt = g.TABLE
    six_edge, eight_edge = tw / 2, (tw + g.LEAF[0]) / 3
    free_breast = -g.FREE_Z[0]
    free_window = g.FREE_Z[1] - g.WINDOW_Z
    eight_wall = g.ROOM_W - g.EIGHT_X[1]
    six_wall = g.ROOM_W - g.SIX_X[1]
    eight_sofa = g.FREE_Z[1] - g.SOFA_FRONT_Z
    four_sofa = g.TABLE_Z[1] - g.SOFA_FRONT_Z
    weight = tw * td * tt * 0.72 / 1000
    cw, cd = g.CHAIR[0], g.CHAIR[1]
    six_cx = sum(g.SIX_X) / 2
    six_sub_gap = (six_cx - 27.5 - cw / 2) - g.SUB_POS["x"][1]          # breast-side chair's east edge to the sub's west end
    e_first = g.EIGHT_X[0] + (g.EIGHT_X[1] - g.EIGHT_X[0]) / 6           # first breast-side chair's centre, three a side
    e_overlap = min(e_first + cw / 2, g.SUB_POS["x"][1]) - max(e_first - cw / 2, g.SUB_POS["x"][0])
    e_back = g.FREE_Z[0] + cd                                            # its back, at the table's edge
    return [
        ("The TV between the uprights", f"{r1(g.TV_GAP)} between the oak uprights, the left one now a corner post on the side wall; the ledge's underside at {r1(g.LEDGE_UNDER)}", [
            ("LG OLED C6 55 in, on its stand", f"{r1(g.TV_W)} × {r1(g.TV_H)} × {r1(g.TV_D)} panel; {r1(g.TV_STAND_H)} tall on the stand", ref("lg"), f"{r1(g.TV_GAP)} wide", f"{r1(g.TV_CLEAR)} each side", PASS),
            ("Top of the screen", f"{r1(g.TV_TOP)} (bottom {r1(g.TV_BOTTOM)}, centre {r1(g.TV_CENTRE)})", ref("lg"), f"ledge at {r1(g.LEDGE_UNDER)}", f"{r1(g.LEDGE_UNDER - g.TV_TOP)}", PASS),
            ("LG stand base", f"{r1(g.TV_STAND_W)} × {r1(g.TV_STAND_D)}", ref("lg"), f"worktop {r1(g.BASE_D)} deep", "set 2 cm off the wall: 11 cm in front of it for the soundbar's leads", PASS),
            ("Soundbar, Hisense AX5100G, centred under the TV", f"{r1(g.SOUNDBAR[0])} × {r1(g.SOUNDBAR[2])} × {r1(g.SOUNDBAR[1])} tall", ref("hisense"), f"x {r1(g.TV_CX - 46)}–{r1(g.TV_CX + 46)}, top {r1(sb_top)}", f"the sightline to the screen's bottom passes {r1(sight(eye_lo))}–{r1(sight(eye_hi))} over it", PASS),
            ("The TV's HDMI plugs, with the screen 2.15 from the corner post", "C6 sockets face sideways on the back panel", ref("lg"), "behind the screen", "plugs stay behind the panel; if a stiff lead pushes out, use 90° HDMI adapters", CHECK),
        ]),
        ("The turntable zone, right of the TV", f"{r1(g.RZ_W)} wide × {r1(g.BASE_D)} deep, worktop {r1(g.WORKTOP)} to the Series X shelf's underside at {r1(g.LID_CLEAR_TO)}", [
            ("Turntable, AT-LP120X size (worst case)", f"{r1(g.DECK[0])} × {r1(g.DECK[2])} × {r1(g.DECK[1])} with its lid", ref("atlp120"), f"{r1(g.RZ_W)} wide", f"{r1(deck_side)} each side", TIGHT),
            ("Its depth, with room behind for the lid's hinges", f"{r1(g.DECK[2])}, front 2 cm in from the worktop's edge", ref("atlp120"), f"{r1(g.BASE_D)} deep", f"{r1(g.ALC_D - g.DECK_Z[1])} behind it", PASS),
            ("Lid open", f"cover {r1(g.LID[0])} × {r1(g.LID[1])}; standing up, its top at about {r1(round(g.LID_TOP_OPEN))}", ref("lid"), f"shelf underside {r1(g.LID_CLEAR_TO)}", f"about {r1(round(g.LID_CLEAR_TO - g.LID_TOP_OPEN))}", PASS),
            ("Phono preamp, hung under the shelf at the back", f"about {r1(g.PREAMP[0])} × {r1(g.PREAMP[2])} × {r1(g.PREAMP[1])}", "", f"{r1(pre_bottom)}–{r1(g.LID_CLEAR_TO)}, at the back", f"{r1(pre_bottom - g.LID_TOP_OPEN)} over the open lid's edge; lift the lid gently", TIGHT),
            ("Series X fan stand on the shelf", f"{r1(fx)} × {r1(fz)} (assumed; model to confirm)", "", f"{r1(g.RZ_W)} × {r1(g.RZ_SHELF_D)} shelf", f"{r1(sx_side)} each side", PASS),
            ("Xbox Series X, standing", f"{r1(sx)} × {r1(sd)} × {r1(sh)} tall", ref("xbox"), f"top at {r1(g.SX_TOP)}", f"{r1(g.HIGH_UNDER - g.SX_TOP)} clear above (Microsoft's minimum is 4); 15 each side, inside the 10–15 it recommends", PASS),
            ("Deco B on the high shelf, right", "11 × 11 × 11.4", ref("deco"), f"{r1(g.RZ_W)} wide, {r1(g.CEIL - g.HIGH_TOP)} to the ceiling", "beside the framed 7-inch, 27 clear above", PASS),
        ]),
        ("Shelves above the TV", f"ledge top {r1(g.LEDGE_TOP)}, 7 deep; high shelf top {r1(g.HIGH_TOP)}, {r1(g.HIGH_D)} deep; ceiling {r1(g.CEIL)}", [
            ("Four LPs on the record ledge", f"4 × {r1(g.LP)} = {r1(lp4)} wide", ref("media"), f"{r1(g.TV_GAP)} long", f"{r1(g.TV_GAP - lp4)}: snug, as drawn", PASS),
            ("Ledge LPs leaning back 8°", f"tops at {r1(g.LEDGE_LP_TOP)}", ref("media"), f"high shelf underside {r1(g.HIGH_UNDER)}", f"{r1(g.HIGH_UNDER - g.LEDGE_LP_TOP)} to lift one out over the 1.5 lip", PASS),
            ("Books on the high shelf", "up to 30 tall", "", f"{r1(g.CEIL - g.HIGH_TOP)} to the ceiling", "9 over the tallest", PASS),
            ("Oak uprights", f"{r1(g.UPRIGHT_LEN)} long (worktop to ceiling)", ref("room"), f"{r1(g.CEIL)} ceiling", "buy 165 and scribe to the ceiling", PASS),
        ]),
        ("Bay 1, Xbox (BESTÅ frame on the 9 cm plinth)", "56.8 wide inside, 40 deep, rows as in v9", [
            ("Xbox One, original, and its brick", "33.3 × 27.4 × 7.9; brick 17 × 7.5 × 4.8", ref("consoles", "xb1psu"), "16 tall row", "8.1 above; 21.5 beside the console for the brick", PASS),
            ("Xbox 360, original, and its brick", "30.9 × 25.8 × 8.3; brick about 21 × 10 × 6", ref("consoles", "x360psu"), "16 tall row", "7.7 above; 25.9 beside for the brick", PASS),
            ("Game drawer", "box 54.3 × 35 on 350 mm runners; cases 19 × 13.5 × 1.4", ref("runners", "media"), "25.2 tall row, 40 deep", "about 3 above the leaning cases; 5 behind the box", PASS),
            ("Depth with the leads", "console 27.4 + HDMI plug about 5", ref("consoles"), "40 deep, back open", "about 7.6, then the 4 cm channel", PASS),
        ]),
        ("Bay 2, PlayStation (BESTÅ frame on the plinth)", "56.8 wide inside, 40 deep", [
            ("PS3, original, + controller basket", "32.5 × 27.4 × 9.8", ref("consoles"), "23.7 tall row", "13.9 above; 24.3 beside for the basket", PASS),
            ("PS2, original, + HDMI switch", "30.2 × 18.3 × 7.8; switch 12.7 × 5.9 × 2.5", ref("consoles", "ugreen"), "16.5 tall row", "8.7 above; 26.6 beside", PASS),
            ("PS1, original, + RetroTINK-6X CE", "27 × 18.8 × 6; RetroTINK size not published", ref("consoles", "rt6x"), "17 tall row", "29.8 beside the PS1 reserved for it; measure it when it arrives", CHECK),
            ("Hidden slim drawer in the plinth", f"box {r1(g.PLINTH_DRAWER['box'][0])} × {r1(g.PLINTH_DRAWER['box'][1])} × {r1(g.PLINTH_DRAWER['box'][2])}, push-to-open 300 mm runners", ref("runners"), "9 cm plinth, 120 wide", "about 2 above and below the box", PASS),
            ("Switch 2 (TL-SG108) and the retro 6-way in the channel", "15.8 × 10.1 × 2.5; 6-way about 34 × 6 × 4", ref("sg108"), "4 cm channel", "on their edges", TIGHT),
        ]),
        ("Bay 3, the records (18 mm ply carcass from the floor)", "56.4 wide × 40 deep × 69.4 tall inside, under the turntable", [
            ("Two face-out record trays", "trays 53.9 × 40 on 400 mm runners, 68–70 kg pairs", ref("runners", "media"), "56.4 inside", "exact: 53.9 + 2 × 1.25 runner allowance = 56.4", PASS),
            ("Tray heights", "lower sleeves to 34.4, upper to 69.1", ref("media"), "top panel underside 71.2", "2.6 and 2.1 finger room", PASS),
            ("LP trough · singles trough", "32.6 for 31.4 sleeves · 18.9 for 18.3–18.4", ref("media"), "52.1 inside each tray", "0.6 each side · 0.25–0.3 each side", PASS),
        ]),
        ("The side wall: the ledge wraps the corner, the PC shelf", f"one oak line at {r1(g.LEDGE_TOP)}: ledge {r1(wrap_len)} long × 7, then a shelf {r1(pc_len)} × {r1(g.PC_SHELF_D)}", [
            ("Four more LPs on the wrap ledge", f"4 × {r1(g.LP)} + gaps = {r1(4 * g.LP + 3 * 1.4)}", ref("media"), f"{r1(wrap_len)} long", f"{r1(wrap_len - 4 * g.LP - 3 * 1.4 - 1.5)}", PASS),
            ("The PC on its shelf", f"{r1(g.PC_CASE[0])} × {r1(g.PC_CASE[2])} × {r1(g.PC_CASE[1])} tall (a typical mid-tower; model to confirm)", "", f"{r1(g.PC_SHELF_D)} × {r1(pc_len)}", "2.5 off the wall, the cane screen and pad dock beyond it", CHECK),
            ("Air above the PC", f"top at {r1(g.PC_SHELF_TOP + g.PC_CASE[1])}", "", f"{r1(g.CEIL)} ceiling", f"{r1(g.CEIL - g.PC_SHELF_TOP - g.PC_CASE[1])} for the top exhaust", PASS),
            ("Shelf over the end of the sofa", f"underside {r1(under)}", ref("sofa"), f"sofa back {r1(g.SOFA_H)}", f"{r1(under - g.SOFA_H)}; the shelf covers only the 28 cm nearest the wall", PASS),
            ("Out of the TV's sightlines", "PC about 54° left of the line to the screen from the sofa", ref("room"), "—", "v10's PC sat at the screen's left edge", PASS),
        ]),
        ("The dining wall on the chimney breast", f"breast {r1(g.BREAST_W)} wide; the table {r1(tw)} × {r1(td)} × {r1(tt)} solid oak, about {weight:.0f} kg", [
            ("Table on the breast", f"{r1(tw)} wide", ref("room"), f"{r1(g.BREAST_W)}", f"{r1((g.BREAST_W - tw) / 2)} each side", PASS),
            ("Folded up", f"about {r1(g.FOLDED_D)} off the breast, top edge {r1(g.FOLDED_TOP)}", ref("liftoff"), f"framed LPs from {r1(g.FRAMES_Y)}", f"{r1(g.FRAMES_Y - g.FOLDED_TOP)}", PASS),
            ("Two Hebgo brackets under it", f"arms {r1(g.HEBGO[0])}, {r1(g.HEBGO_X[1] - g.HEBGO_X[0])} apart; 500 kg a pair", ref("hebgo"), f"a {r1(td)} deep top", f"{r1(td - g.HEBGO[0])} beyond the arms; spacing inside Häfele's 80", PASS),
            ("Three lift-off hinges on the backboard", "100 × 88, rated for a 120 kg door", ref("liftoff"), f"a {weight:.0f} kg top", "slide it 5 cm sideways to lift it off", PASS),
            ("Four at the wall: two on the room side", f"{r1(tw)} of edge", ref("dining"), f"{r1(g.DINE_W)} each recommended", f"{r1(tw / 2)} each", TIGHT),
            ("Four at the wall: room to the sofa", f"table edge {r1(-g.TABLE_Z[1])} out", ref("dining", "sofa"), "sofa front", f"{r1(four_sofa)} (walk behind: 100+)", PASS),
            ("The west end chair and the door", f"chair {r1(g.CHAIR[0])} × {r1(g.CHAIR[1])}", ref("terje"), "the door's swing, if it opens in", "they overlap: keep the door shut while you eat, or confirm it opens outwards", CHECK),
            ("Six: lifted off onto four legs", f"top at {r1(g.LEG_H + tt)}–{r1(73 + tt)}", ref("legs"), f"dining height about {r1(75)}", "within 1.3", PASS),
            ("Six: two a side", f"{r1(tw)} long", ref("dining"), f"{r1(g.DINE_W)} each", f"{r1(six_edge)} each", TIGHT),
            ("Six and eight: to the breast and the window", f"table {r1(free_breast)}–{r1(-g.FREE_Z[1])} out", ref("dining"), f"{r1(g.CLEAR_MIN)} minimum", f"{r1(free_breast)} to the breast (tight minimum); {r1(free_window)} to the window", TIGHT),
            ("Six: the west end", f"table end at {r1(g.SIX_X[1])}", ref("dining"), f"west wall at {r1(g.ROOM_W)}", f"{r1(six_wall)}", PASS),
            ("Eight: with the 60 × 80 leaf", f"{r1(tw + g.LEAF[0])} long, three a side", ref("dining", "legs"), f"{r1(g.DINE_W)} each", f"{r1(eight_edge)} each", TIGHT),
            ("Eight: the west end and the sofa", f"table {r1(g.EIGHT_X[0])}–{r1(g.EIGHT_X[1])}", ref("dining", "sofa"), f"{r1(g.CLEAR_OK)} to aim for", f"{r1(eight_wall)} to the wall; {r1(eight_sofa)} to the sofa's front at the east end", TIGHT),
            ("Six: the breast-side chairs and the sub", f"chairs {r1(cw)} wide at the table's edge, backs at {r1(-(g.FREE_Z[0] + cd))} from the breast", ref("terje", "hisense"), f"sub at x {r1(g.SUB_POS['x'][0])}–{r1(g.SUB_POS['x'][1])}, {r1(-g.SUB_POS['z'][0])} out", f"{r1(six_sub_gap)} beside it: pushed back, a chair passes the sub instead of hitting it", TIGHT),
            ("Eight: the breast-side end chair and the sub", f"chair at x {r1(e_first - cw / 2)}–{r1(e_first + cw / 2)}, back at {r1(-e_back)} from the breast", ref("terje", "hisense"), f"sub {r1(-g.SUB_POS['z'][0])} out from the breast", f"they overlap {r1(e_overlap)} across and {r1(-g.SUB_POS['z'][0] + e_back)} deep: for eight, lift the sub out to the end of the base first (it's wireless; leave 1 m of slack in its lead)", CHECK),
            ("Sub under the dining wall, on its side", f"{r1(g.SUB[2])} long × {r1(g.SUB[0])} out × {r1(g.SUB[1])} tall, on a 5 cm riser", ref("hisense"), f"between the bracket arms, {r1(g.HEBGO_X[1] - g.HEBGO_X[0])} apart", f"{r1(g.SUB_POS['x'][0] - g.HEBGO_X[0] - 1.4)} to the east arm; {r1(g.HEBGO_X[1] - 1.4 - g.SUB_POS['x'][1])} behind the rear port", PASS),
            ("Feet under the table, four at the wall", f"sub {r1(-g.SUB_POS['z'][0] + 2)} out from the breast", ref("terje"), f"table {r1(td)} deep", f"{r1(td + g.RAIL[2] - (-g.SUB_POS['z'][0] + 2))} of legroom in front of it on the room side; the end seats are clear", PASS),
            ("Chairs at the table", f"seat {r1(g.CHAIR[3])}", ref("terje"), f"top {r1(g.TABLE_TOP)}", f"{r1(g.TABLE_TOP - g.CHAIR[3])} seat to top, the usual 25–30", PASS),
        ]),
        ("The room", f"{r1(g.ROOM_W)} × {r1(g.ROOM_D)}, ceiling {r1(g.CEIL)}", [
            ("Eyes to screen from the sofa", "the L-sofa's long side against the window wall, 10 off the radiator", ref("room", "sofa"), f"{r1(g.SCREEN_FROM_WINDOW)} window wall to screen", f"about {g.VIEW_DIST / 100:.2f} m; a 55-inch fills about 26°", PASS),
            ("From the end of the sofa's return", f"sitting up at its end, {r1(g.TV_PANEL_Z[0] - g.CHAISE_EYES_Z)} from the screen", ref("sofa"), "straight ahead of the TV", "the TV's move puts it square on to this seat", PASS),
            ("TV centre against seated eyes", f"{r1(g.TV_CENTRE)}", ref("lg"), f"eyes at {r1(eye_lo)}–{r1(eye_hi)}", "about 1–2.5° above the eye line", PASS),
            ("Both spotlight bars under the ceiling", f"{r1(g.BAR[2])} drop", ref("wolston"), f"{r1(g.CEIL)} ceiling", f"lowest shade at {r1(g.CEIL - g.BAR[2])}", PASS),
        ]),
    ]


def status_class(s):
    return {PASS: "ok", TIGHT: "tight", CHECK: "check", NO: "no"}[s]


def tables_html():
    out = []
    for title, space, rows in zones():
        out.append(f"<div class='zonebox'><h4>{title}</h4><p class='zone'>{space}</p>")
        out.append("<table class='fit'><tr><th>Item</th><th>Size (cm)</th><th>Space</th><th>Spare (cm)</th><th>Result</th></tr>")
        for item, size, src, sp, spare, st in rows:
            out.append(f"<tr><td>{item}</td><td>{size}{src}</td><td>{sp}</td><td>{spare}</td><td class='res {status_class(st)}'>{st}</td></tr>")
        out.append("</table></div>")
    return "\n".join(out)


def counts():
    c = {PASS: 0, TIGHT: 0, CHECK: 0, NO: 0}
    for _, _, rows in zones():
        for r in rows:
            c[r[-1]] += 1
    return c


def sources_html(extra=()):
    items = [SOURCES[k] for k in ORDER] + list(extra)
    return "<ol class='sources'>" + "".join(f"<li>{s}</li>" for s in items) + "</ol>"


if __name__ == "__main__":
    for title, space, rows in zones():
        print("==", title, "|", space)
        for r in rows:
            print("  ", r[0], "|", r[1], "|", r[3], "|", r[4], "|", r[5])
    print(counts())
