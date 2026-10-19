"""v13.2 fit proof (v13: no slatted panel; v13.2: the sub under an oak cover with no sides, six at the 170 × 80 table with its leaf) (v11 layout; v12 adds the six- and eight-seat checks against the sub): every item that goes in the wall, its size and where the size comes from, the space it goes
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
    "sofa": "Your photo of the sofa (18 Oct 2026): a black jumbo-cord L-sofa, the long side under the window ending in line with the breast's reveal, about 188 cm; the return's 168 is a typical corner-sofa size until measured",
    "subport": "Klipsch subwoofer placement guidance, as quoted by Cloudspress and TechYorker (2026): leave about 6–12 in (15–30 cm) between a rear-firing port and the nearest obstruction",
    "psuplace": "Xbox Support (Microsoft), About the Xbox One power supply (archived): don't block its vents, don't put it in a confined space such as a bookcase, rack or stereo cabinet unless the space is well ventilated, don't stack devices on it, and lay it flat on its four rubber pads; the Xbox 360 brick's advice is the same",
    "x360place": "Xbox Support (Microsoft), Xbox 360 placement tips, as quoted on Gaming Stack Exchange: an open, well-ventilated area, a hard surface, and away from high-vibrating sources such as subwoofers",
    "case": "Corsair 4000D Airflow, a typical mid-tower gaming case: 453 × 230 × 466 mm (TechPowerUp review)",
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
    six_len = tw + g.LEAF[0] if g.SIX_LEAF else tw
    six_edge, eight_edge = six_len / 2, (tw + g.LEAF[0]) / 3
    free_breast = -g.FREE_Z[0]
    free_window = g.FREE_Z[1] - g.WINDOW_Z
    eight_wall = g.ROOM_W - g.EIGHT_X[1]
    six_wall = g.ROOM_W - g.SIX_X[1]
    eight_sofa = g.FREE_Z[1] - g.SOFA_FRONT_Z
    four_sofa = g.TABLE_Z[1] - g.SOFA_FRONT_Z
    weight = tw * td * tt * 0.72 / 1000
    cw, cd = g.CHAIR[0], g.CHAIR[1]
    six_cx = sum(g.SIX_X) / 2
    SB = g.SUB_HOOD                                                      # v13.2: the sub's oak cover under the dining wall
    import math
    tip_rise = math.hypot(g.SUB[0], g.SUB[1]) - g.SUB[1]                 # how far the sub's top corner rises before it tips
    over_sub = SB["h"] - SB["top"] - SB["feet"] - SB["base"] - g.SUB[1]  # the gap from the sub's top to the cover
    six_first = g.SIX_X[0] + (g.SIX_X[1] - g.SIX_X[0]) / 4                # first breast-side chair's centre, two a side
    six_sub_gap = (six_first - cw / 2) - (SB["x"][1] + SB["over"])                      # its east edge to the box's west end
    chair_back = -(g.FREE_Z[0] + cd - 8)                                 # breast-side chair backs, tucked 8 under the table
    box_front = -(SB["z"][0] - SB["over"])                               # the box's top overhang, out from the breast
    east_end = g.SIX_X[0] - cd                                           # the east-end diner's chair, pushed back
    cof_gap = (sum(g.FREE_Z) / 2 - cw / 2) - g.COFFEE["z"][1]             # that chair's side to the coffee table's near edge (z)
    port_gap = (g.HEBGO_X[1] - 1.4) - g.SUB_POS["x"][1]                  # the port (west end) to the west bracket arm
    drv_gap = g.SUB_POS["x"][0] - (g.HEBGO_X[0] + 1.4)                   # the driver (east end) to the east bracket arm
    e_first = g.EIGHT_X[0] + (g.EIGHT_X[1] - g.EIGHT_X[0]) / 6           # first breast-side chair's centre, three a side
    e_overlap = min(e_first + cw / 2, SB["x"][1]) - max(e_first - cw / 2, SB["x"][0])
    panel = 0.0 if g.PLAIN else g.RZ_SLATS[2]
    e_back = g.FREE_Z[0] + cd                                            # its back, at the table's edge
    sc = g.SUB_COL[1] - g.SUB_COL[0]
    pc_ = g.PS_COL[1] - g.PS_COL[0]
    if g.SUB_IN_WALL:   # v13.5: the bricks at the back of their rows; the sub in bay 2's lower left
        bay1 = ("Bay 1, Xbox (BESTÅ frame on the 9 cm plinth)", "56.8 wide inside, 40 deep; the bricks lie at the back of their rows", [
            ("Xbox One, original, + HDMI switch", "33.3 × 27.4 × 7.9; switch 12.7 × 5.9 × 2.5", ref("consoles", "ugreen"), "16 tall row", "8.1 above; the switch in the 23.5 beside it, at the front for its remote", PASS),
            ("Xbox 360, original, + RetroTINK-6X CE", "30.9 × 25.8 × 8.3; RetroTINK allowed 23 × 23 × 8 (no size published)", ref("consoles", "rt6x"), "16 tall row", "7.7 above; 25.9 beside it for the RetroTINK: measure it when it arrives", CHECK),
            ("Both bricks, flat at the back of their rows", "Xbox One 17 × 7.5 × 4.8; Xbox 360 allowed 21 × 10 × 6", ref("xb1psu", "x360psu", "psuplace"), "behind the switch and the RetroTINK, by the channel's power leads", "23 + 10 = 33 of the 40 depth for the RetroTINK and the 360's brick; on their rubber pads, nothing on top, open to the channel; 2 cm or more from the consoles' rear vents", PASS),
            ("Game drawer", "box 54.3 × 35 on 350 mm runners; cases 19 × 13.5 × 1.4", ref("runners", "media"), "25.2 tall row, 40 deep", "about 3 above the leaning cases; 5 behind the box", PASS),
            ("Depth with the leads", "console 27.4 + HDMI plug about 5", ref("consoles"), "40 deep, back open", "about 7.6, then the 4 cm channel", PASS),
        ])
        bay2 = ("Bay 2, PlayStation and the sub (BESTÅ frame on the plinth)", f"56.8 wide inside, 40 deep; under the PS3's shelf, the sub's column {r1(sc)} wide, a 12 mm ply divider, then {r1(pc_)} for the PS2 over the PS1", [
            ("PS3, original, + controller basket", "32.5 × 27.4 × 9.8", ref("consoles"), "23.7 tall row, full width", "13.9 above; 24.3 beside for the basket", PASS),
            ("The sub in its column", f"{r1(g.SUB[0])} × {r1(g.SUB[2])} × {r1(g.SUB[1])} tall, on a {r1(g.SUB_RISER_H)} isolation riser", ref("hisense"), f"{r1(sc)} wide × {r1(g.SUB_COL_TOP - g.SUB_COL_FLOOR)} tall", f"1 each side, {r1(g.SUB_COL_TOP - g.SUB_IN['y'][1])} above; it mustn't touch the divider or the frame", TIGHT),
            ("The sub's driver and port", "front-firing driver, rear port; its front flush with the face frame", ref("hisense", "subport"), f"{r1(g.SUB_PORT_GAP)} from the port to the wall, through the open back and the channel", "inside the 15–30 advised for a rear port, at its low end: keep the channel behind bay 2 clear (Switch 2 and the retro 6-way go behind bay 1)", TIGHT),
            ("PS2, original, over the PS1", "30.2 × 18.3 × 7.8 · 27 × 18.8 × 6", ref("consoles"), f"{r1(pc_)} wide; 16.5 and 17 rows on a part shelf", f"PS2 {r1((pc_ - 30.2) / 2)} each side, 8.7 above; PS1 {r1((pc_ - 27) / 2)} each side, 11 above; both open front and back", TIGHT),
            ("Vibration: the consoles and the deck share the base with the sub", "Microsoft: keep the Xbox 360 away from high-vibrating sources such as subwoofers", ref("x360place"), "the sub on its riser, clear of the divider and the frame; the deck on isolation feet", "the 360 is a bay away, the PS2 and PS1 a divider away: play a disc game and a record at film volume; if anything skips, turn the sub down for that source, or put it back under the dining wall", CHECK),
            ("Hidden slim drawer in the plinth", f"box {r1(g.PLINTH_DRAWER['box'][0])} × {r1(g.PLINTH_DRAWER['box'][1])} × {r1(g.PLINTH_DRAWER['box'][2])}, 300 mm full-extension runners, a finger-pull groove (no push-to-open at floor level)", ref("runners"), "9 cm plinth, 120 wide", "about 2 above and below the box; felt its runners, it's under the sub", PASS),
            ("Switch 2 (TL-SG108) and the retro 6-way in the channel", "15.8 × 10.1 × 2.5; 6-way about 34 × 6 × 4", ref("sg108"), "4 cm channel, behind bay 1", "on their edges, clear of the sub's port", TIGHT),
        ])
    else:
        bay1 = ("Bay 1, Xbox (BESTÅ frame on the 9 cm plinth)", "56.8 wide inside, 40 deep, rows as in v9", [
            ("Xbox One, original, and its brick", "33.3 × 27.4 × 7.9; brick 17 × 7.5 × 4.8", ref("consoles", "xb1psu"), "16 tall row", "8.1 above; 21.5 beside the console for the brick", PASS),
            ("Xbox 360, original, and its brick", "30.9 × 25.8 × 8.3; brick about 21 × 10 × 6", ref("consoles", "x360psu"), "16 tall row", "7.7 above; 25.9 beside for the brick", PASS),
            ("Game drawer", "box 54.3 × 35 on 350 mm runners; cases 19 × 13.5 × 1.4", ref("runners", "media"), "25.2 tall row, 40 deep", "about 3 above the leaning cases; 5 behind the box", PASS),
            ("Depth with the leads", "console 27.4 + HDMI plug about 5", ref("consoles"), "40 deep, back open", "about 7.6, then the 4 cm channel", PASS),
        ])
        bay2 = ("Bay 2, PlayStation (BESTÅ frame on the plinth)", "56.8 wide inside, 40 deep", [
            ("PS3, original, + controller basket", "32.5 × 27.4 × 9.8", ref("consoles"), "23.7 tall row", "13.9 above; 24.3 beside for the basket", PASS),
            ("PS2, original, + HDMI switch", "30.2 × 18.3 × 7.8; switch 12.7 × 5.9 × 2.5", ref("consoles", "ugreen"), "16.5 tall row", "8.7 above; 26.6 beside", PASS),
            ("PS1, original, + RetroTINK-6X CE", "27 × 18.8 × 6; RetroTINK size not published", ref("consoles", "rt6x"), "17 tall row", "29.8 beside the PS1 reserved for it; measure it when it arrives", CHECK),
            ("Hidden slim drawer in the plinth", f"box {r1(g.PLINTH_DRAWER['box'][0])} × {r1(g.PLINTH_DRAWER['box'][1])} × {r1(g.PLINTH_DRAWER['box'][2])}, 300 mm full-extension runners, a finger-pull groove (no push-to-open at floor level)", ref("runners"), "9 cm plinth, 120 wide", "about 2 above and below the box", PASS),
            ("Switch 2 (TL-SG108) and the retro 6-way in the channel", "15.8 × 10.1 × 2.5; 6-way about 34 × 6 × 4", ref("sg108"), "4 cm channel", "on their edges", TIGHT),
        ])
    zs = [
        ("The TV between the uprights", f"{r1(g.TV_GAP)} between the oak uprights, the left one now a corner post on the side wall; the ledge's underside at {r1(g.LEDGE_UNDER)}", [
            ("LG OLED C6 55 in, on its stand", f"{r1(g.TV_W)} × {r1(g.TV_H)} × {r1(g.TV_D)} panel; {r1(g.TV_STAND_H)} tall on the stand", ref("lg"), f"{r1(g.TV_GAP)} wide", f"{r1(g.TV_CLEAR)} each side", PASS),
            ("Top of the screen", f"{r1(g.TV_TOP)} (bottom {r1(g.TV_BOTTOM)}, centre {r1(g.TV_CENTRE)})", ref("lg"), f"ledge at {r1(g.LEDGE_UNDER)}", f"{r1(g.LEDGE_UNDER - g.TV_TOP)}", PASS),
            ("LG stand base", f"{r1(g.TV_STAND_W)} × {r1(g.TV_STAND_D)}", ref("lg"), f"worktop {r1(g.BASE_D)} deep", "set 2 cm off the wall: 11 cm in front of it for the soundbar's leads", PASS),
            ("Soundbar, Hisense AX5100G, centred under the TV", f"{r1(g.SOUNDBAR[0])} × {r1(g.SOUNDBAR[2])} × {r1(g.SOUNDBAR[1])} tall", ref("hisense"), f"x {r1(g.TV_CX - 46)}–{r1(g.TV_CX + 46)}, top {r1(sb_top)}", f"the sightline to the screen's bottom passes {r1(sight(eye_lo))}–{r1(sight(eye_hi))} over it", PASS),
            ("The TV's HDMI plugs, with the screen 2.15 from the corner post", "C6 sockets face sideways on the back panel", ref("lg"), "behind the screen", "plugs stay behind the panel; if a stiff lead pushes out, use 90° HDMI adapters", CHECK),
        ]),
        ("The turntable zone, right of the TV", f"{r1(g.RZ_W)} wide × {r1(g.BASE_D)} deep, worktop {r1(g.WORKTOP)} to the Series X shelf's underside at {r1(g.LID_CLEAR_TO)}", [
            ("Turntable, AT-LP120X size (worst case)", f"{r1(g.DECK[0])} × {r1(g.DECK[2])} × {r1(g.DECK[1])} with its lid", ref("atlp120"), f"{r1(g.RZ_W)} wide", f"{r1(deck_side)} each side", TIGHT),
            ("Its depth, with room behind for the lid's hinges", f"{r1(g.DECK[2])}, front 2 cm in from the worktop's edge", ref("atlp120"), f"{r1(g.BASE_D)} deep, to the painted wall" if g.PLAIN else f"{r1(g.BASE_D)} deep, less the {r1(panel)} slatted panel", f"{r1(g.ALC_D - panel - g.DECK_Z[1])} behind it", TIGHT if g.ALC_D - panel - g.DECK_Z[1] < 8 else PASS),
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
        bay1,
        bay2,
        ("Bay 3, the records (18 mm ply carcass from the floor)", "56.4 wide × 40 deep × 69.4 tall inside, under the turntable", [
            ("Two face-out record trays", "trays 53.9 × 40 on 400 mm runners, 68–70 kg pairs", ref("runners", "media"), "56.4 inside", "exact: 53.9 + 2 × 1.25 runner allowance = 56.4", PASS),
            ("Tray heights", "lower sleeves to 34.4, upper to 69.1", ref("media"), "top panel underside 71.2", "2.6 and 2.1 finger room", PASS),
            ("LP trough · singles trough", "32.6 for 31.4 sleeves · 18.9 for 18.3–18.4", ref("media"), "52.1 inside each tray", "0.6 each side · 0.25–0.3 each side", PASS),
        ]),
        ("The side wall: the ledge wraps the corner, the PC shelf", f"one oak line at {r1(g.LEDGE_TOP)}: ledge {r1(wrap_len)} long × 7, then a shelf {r1(pc_len)} × {r1(g.PC_SHELF_D)}", [
            ("Four more LPs on the wrap ledge", f"4 × {r1(g.LP)} + gaps = {r1(4 * g.LP + 3 * 1.4)}", ref("media"), f"{r1(wrap_len)} long", f"{r1(wrap_len - 4 * g.LP - 3 * 1.4 - 1.5)}", PASS),
            ("The PC on its shelf", f"{r1(g.PC_CASE[0])} × {r1(g.PC_CASE[2])} × {r1(g.PC_CASE[1])} tall (an average gaming case, e.g. Corsair 4000D)", ref("case"), f"{r1(g.PC_SHELF_D)} × {r1(pc_len)}", "2.5 off the wall, the brush grommet and pad dock beyond it; height 46.6 under the 79.6 to the ceiling", PASS),
            ("Air above the PC", f"top at {r1(g.PC_SHELF_TOP + g.PC_CASE[1])}", "", f"{r1(g.CEIL)} ceiling", f"{r1(g.CEIL - g.PC_SHELF_TOP - g.PC_CASE[1])} for the top exhaust", PASS),
            ("Shelf over the end of the sofa", f"underside {r1(under)}", ref("sofa"), f"sofa back {r1(g.SOFA_H)}", f"{r1(under - g.SOFA_H)}; the shelf covers only the 28 cm nearest the wall", PASS),
            ("Keyboard tray under the PC shelf (v6.1)", f"{r1(g.KB_TRAY['h'])} cm housing, tray rolls {r1(g.KB_TRAY['out'])} out on {r1(g.KB_TRAY['runners'] * 10)} mm runners", ref("runners"), f"sofa back {r1(g.SOFA_H)}", f"{r1(under - g.KB_TRAY['h'] - g.SOFA_H)} over the sofa's back; pulled out, its front edge is {r1(g.PC_SHELF_D + g.KB_TRAY['out'])} from the wall, still over the return's seat", PASS),
            ("Out of the TV's sightlines", "PC about 54° left of the line to the screen from the sofa", ref("room"), "—", "v10's PC sat at the screen's left edge", PASS),
        ]),
        ("The dining wall on the chimney breast", f"breast {r1(g.BREAST_W)} wide; the table {r1(tw)} × {r1(td)} × {r1(tt)} solid oak, about {weight:.0f} kg", [
            ("Table on the breast", f"{r1(tw)} wide", ref("room"), f"{r1(g.BREAST_W)}", f"{r1((g.BREAST_W - tw) / 2)} each side", PASS),
            ("Folded up", f"about {r1(g.FOLDED_D)} off the breast, top edge {r1(g.FOLDED_TOP)}", ref("liftoff"), f"framed LPs from {r1(g.FRAMES_Y)}", f"{r1(g.FRAMES_Y - g.FOLDED_TOP)}", PASS),
            ("Two Hebgo brackets under it", f"arms {r1(g.HEBGO[0])}, {r1(g.HEBGO_X[1] - g.HEBGO_X[0])} apart; 500 kg a pair", ref("hebgo"), f"a {r1(td)} deep top", f"{r1(td - g.HEBGO[0])} beyond the arms; spacing inside Häfele's 80", PASS),
            ("Three lift-off hinges on the backboard", "100 × 88, rated for a 120 kg door", ref("liftoff"), f"a {weight:.0f} kg top", "slide it 5 cm sideways to lift it off", PASS),
            ("Four at the wall: two on the room side", f"{r1(tw)} of edge", ref("dining"), f"{r1(g.DINE_W)} each recommended", f"{r1(tw / 2)} each", TIGHT),
            ("Four at the wall: room to the sofa", f"table edge {r1(-g.TABLE_Z[1])} out", ref("dining", "sofa"), "sofa front", f"{r1(four_sofa)} (walk behind: 100+)", PASS),
            ("The door and the dining chairs", "door 83 wide, hinged on the breast side, opens in (you confirmed)", ref("room"), "its swing reaches about 44 out from the recess wall", "the west-end chair (four) and the breast-side chairs (six, eight) sit in its swing: keep it shut while you eat, or have it rehung to open into the hall", TIGHT),
            ("Six and eight: lifted off onto legs, with the leaf", f"table {r1(tw)} + leaf {r1(g.LEAF[0])} = {r1(six_len)} × {r1(td)}, top at {r1(g.LEG_H + tt)}–{r1(73 + tt)}", ref("legs"), f"dining height about {r1(75)}", "within 1.3; four legs under the table, four under the leaf, joined by two dowels and two clips", PASS),
            ("Six: two a side, one at each end", f"{r1(six_len)} of edge each long side, {r1(td)} at each end", ref("dining"), f"{r1(g.DINE_W)} each", f"{r1(six_edge)} each on the sides (25 spare); {r1(td)} at the ends", PASS),
            ("Eight: three a side, one at each end", f"{r1(tw + g.LEAF[0])} long", ref("dining", "legs"), f"{r1(g.DINE_W)} each", f"{r1(eight_edge)} each", TIGHT),
            ("Six and eight: to the breast and the window", f"table {r1(free_breast)}–{r1(-g.FREE_Z[1])} out", ref("dining"), f"{r1(g.CLEAR_OK)} to aim for", f"{r1(free_breast)} to the breast; {r1(free_window)} to the window", PASS if free_breast >= g.CLEAR_OK else TIGHT),
            ("Six and eight: the west end", f"table end at {r1(g.SIX_X[1])}", ref("dining"), f"west wall at {r1(g.ROOM_W)}", f"{r1(six_wall)} for the end diner (60 is the tight minimum; the stairs are behind the breast-side corner, clear of it)", PASS if six_wall >= g.CLEAR_OK else TIGHT),
            ("Six and eight: the east end and the coffee table", f"end chair at x {r1(east_end)}–{r1(g.SIX_X[0])}", ref("dining", "sofa"), "coffee table and sofa", f"{r1(cof_gap)} to the coffee table's edge: slide it towards the window first; the sofa ends at {r1(g.SOFA_X[1])}, clear of the chair ({r1(eight_sofa)} to its front line)", TIGHT),
            ("Six: the breast-side chairs and the sub's cover", f"chairs at x {r1(six_first - cw / 2)}–{r1(six_first + cw / 2)} and on, backs at {r1(chair_back)} from the breast", ref("terje"), f"cover x {r1(SB['x'][0] - SB['over'])}–{r1(SB['x'][1] + SB['over'])}, {r1(box_front)} out", f"{r1(six_sub_gap)} beside it and {r1(chair_back - box_front)} in front of it: chairs and cover don't meet", (CHECK if min(six_sub_gap, chair_back - box_front) < 0 else TIGHT if min(six_sub_gap, chair_back - box_front) < 10 else PASS)),
            ("Eight: the breast-side end chair and the sub's cover", f"chair at x {r1(e_first - cw / 2)}–{r1(e_first + cw / 2)}", ref("terje"), f"cover x {r1(SB['x'][0])}–{r1(SB['x'][1])}", (f"they overlap {r1(e_overlap)} across, so that chair can push back only {r1(chair_back - box_front)} before it meets the cover: for eight, lift the cover off its two keyhole screws and stand the sub at the end of the base (it's wireless; leave 1 m of slack in its lead)" if e_overlap > 0 else f"{r1(-e_overlap)} clear"), CHECK if e_overlap > 0 else PASS),
            ("Sub under its oak cover, under the dining wall", f"sub {r1(g.SUB[2])} long × {r1(g.SUB[0])} out × {r1(g.SUB[1])} tall, standing sideways: driver east, port west", ref("hisense"), f"cover {r1(SB['x'][1] - SB['x'][0] + 2 * SB['over'])} × {r1(-SB['z'][0] + SB['over'])} at {r1(SB['h'])} on a backboard, between the folded arms", f"{r1(SB['x'][0] - g.HEBGO_X[0] - 1.4)} clear of the east arm, {r1(g.HEBGO_X[1] - 1.4 - SB['x'][1])} of the west; {r1(over_sub)} over the sub", PASS),
            ("The sound: no sides, no front", "the driver fires east, the port west, the room side is open", ref("subport", "hisense"), f"{r1(g.SUB_PORT_MIN)} for the port", f"port {r1(port_gap)} to the nearest thing (the west arm), driver {r1(drv_gap)}; only the cover is over it, and nothing faces the driver or the port", PASS if port_gap >= g.SUB_PORT_MIN else TIGHT),
            ("Spills", f"solid oak cover {r1(SB['top'])} thick, {r1(SB['over'])} overhang with a drip groove underneath", "", "a drink knocked off the table", "it lands on the cover and runs off its edge in front of the sub, never onto it", PASS),
            ("Knocks: it can't fall over", f"the sub's top corner rises {r1(tip_rise)} before it would tip", ref("hisense"), f"cover {r1(over_sub)} over it; tray lip {r1(SB['lip'])}", f"the cover stops it {r1(tip_rise - over_sub)} short of tipping; the lip stops it sliding; the backboard hangs on two keyhole screws in the solid breast", PASS if over_sub < tip_rise else CHECK),
            ("Feet under the table, four at the wall", f"the cover {r1(box_front)} out from the breast", ref("terje"), f"table {r1(td)} deep", f"{r1(td + g.RAIL[2] - box_front)} of legroom in front of it on the room side; the end seats are clear", PASS),
            ("Chairs at the table", f"seat {r1(g.CHAIR[3])}", ref("terje"), f"top {r1(g.TABLE_TOP)}", f"{r1(g.TABLE_TOP - g.CHAIR[3])} seat to top, the usual 25–30", PASS),
        ]),
        ("The room", f"{r1(g.ROOM_W)} × {r1(g.ROOM_D)}, ceiling {r1(g.CEIL)}", [
            ("Eyes to screen from the sofa", "the L-sofa's long side against the window wall, 10 off the radiator", ref("room", "sofa"), f"{r1(g.SCREEN_FROM_WINDOW)} window wall to screen", f"about {g.VIEW_DIST / 100:.2f} m; a 55-inch fills about 26°", PASS),
            ("From the end of the sofa's return", f"sitting up at its end, {r1(g.TV_PANEL_Z[0] - g.CHAISE_EYES_Z)} from the screen", ref("sofa"), "straight ahead of the TV", "the TV's move puts it square on to this seat", PASS),
            ("TV centre against seated eyes", f"{r1(g.TV_CENTRE)}", ref("lg"), f"eyes at {r1(eye_lo)}–{r1(eye_hi)}", "about 1–2.5° above the eye line", PASS),
            ("Both spotlight bars under the ceiling", f"{r1(g.BAR[2])} drop", ref("wolston"), f"{r1(g.CEIL)} ceiling", f"lowest shade at {r1(g.CEIL - g.BAR[2])}", PASS),
        ]),
    ]
    if g.SUB_IN_WALL:   # v13.5: nothing under the dining wall now
        gone = ("the sub's cover", "Sub under its oak cover", "The sound: no sides", "Spills", "Knocks: it can't", "Feet under the table")
        for zi_, (title, space, rows) in enumerate(zs):
            if title.startswith("The dining wall"):
                rows = [r for r in rows if not any(k in r[0] for k in gone)]
                rows.append(("Feet under the table, four at the wall", "nothing under it: the sub is in the alcove base", ref("terje"), f"table {r1(td)} deep", f"{r1(td)} of clear legroom along the breast; eight need no cover lifted off", PASS))
                zs[zi_] = (title, space, rows)
    return zs


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
