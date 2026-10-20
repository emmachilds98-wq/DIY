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
    "legs": "Emuca: table legs Ø60 mm, 710 mm, height adjustable 710–730 mm, 50 kg per leg (set of 4): 710 is the standard dining leg; the plan's oak legs are made to the same 71 cm",
    "clip": "RS PRO 45 mm steel spring clip (RS 175-3588): 42.1 × 56 × 12.7 mm, packs of 10 (uk.rs-online.com)",
    "terje": "IKEA: TERJE folding chair, 43 W × 49 D × 78 H cm, seat height 48 cm, tested for 110 kg",
    "dining": "Book a Builder UK, small dining room ideas: 600 mm of table edge per diner; table edge to a wall 600 mm tight minimum, 750 mm to aim for, 1000–1100 mm to walk behind; dining height about 750 mm",
    "sofa": "Your photo of the sofa (18 Oct 2026) and your note (21 Oct): a blue corduroy L-sofa, two seats then the corner on the long side, which ends about 40 cm short of the window's west end (about 266 cm long); the return's 168 is a typical corner-sofa size until measured",
    "subport": "Klipsch subwoofer placement guidance, as quoted by Cloudspress and TechYorker (2026): leave about 6–12 in (15–30 cm) between a rear-firing port and the nearest obstruction",
    "psuplace": "Xbox Support (Microsoft), About the Xbox One power supply (archived): don't block its vents, don't put it in a confined space such as a bookcase, rack or stereo cabinet unless the space is well ventilated, don't stack devices on it, and lay it flat on its four rubber pads; the Xbox 360 brick's advice is the same",
    "x360place": "Xbox Support (Microsoft), Xbox 360 placement tips, as quoted on Gaming Stack Exchange: an open, well-ventilated area, a hard surface, and away from high-vibrating sources such as subwoofers",
    "photo20": "Your two photos of the west end (20 Oct 2026): the 2 m black shelf on the wall beside the stairs, scaled from its 2 m: it starts about 41 cm past the stair box and stops about 16 cm short of the window corner, top about 200; the pendant hangs about 55 cm out from the wall, a quarter of the way along it",
    "case": "Corsair 4000D Airflow, a typical mid-tower gaming case: 453 × 230 × 466 mm (TechPowerUp review)",
    "fliphinge": "Lee Valley: 40574 narrow flip-top hinges, solid brass, 1/2 in × 2 3/4 in (1.27 × 7.0 cm), for card and flip-top tables (leevalley.com); their 40208 card-table hinge is 1 3/16 in (3.0 cm) wide, too wide for a 27 mm edge",
    "curtains": "Your photo (20 Oct) and note: Dunelm hessian pencil-pleat curtains; Dunelm pencil-pleat drops run 137, 182 and 228 cm with a 3 in header; Dunelm 28 mm wooden poles, 120–360 cm, rings included (one per 10 cm), finials up to 8 cm more (dunelm.com)",
    "plantstand": "Your plant stand, from your photo (20 Oct): bamboo, two columns, four slatted tiers, LED grow bars under the top two. Drawn at 90 × 30 × 120 (W × D × H), the usual size of a two-column four-tier bamboo stand (e.g. VIVOSUN's 4-tier bamboo stand, 47.2 in = 120 cm tall: homedepot.com); please measure yours",
    "kallax": "IKEA: KALLAX shelving unit 2 × 2, 77 × 39 × 77 cm, cubes 33 × 33 inside (ikea.com). Your 2 × 2 wooden record shelf with four trays is drawn at this size until you measure it",
    "obegransad": "IKEA: OBEGRÄNSAD LED wall lamp, black (your 905.262.63; 005.262.48 and others by country): 52 × 36 × 6 cm, 5 W, five lighting programmes, hangs landscape or portrait, runs on a 5 V USB-A adapter sold separately (ikea.com); its face is a 16 × 16 grid of white LEDs. From the Swedish House Mafia collection (IKEA press kit, Sept 2022)",
    "pads": "Sony: DualSense controller 160 × 66 × 106 mm (W × H × D); Microsoft: Xbox Wireless Controller 153 × 61 × 104 mm",
    "crate": "Record-shop browser crates and LP storage boxes are made about 32.5–33 cm inside for 31.4 cm sleeves (31.8–32.4 in outer sleeves), flipped by the sleeves' top edges",
    "strips": "Philips Hue Lightstrip Plus V4: 2 m base kit, cuttable every 33 cm, extendable with 1 m; WiZ Wi-Fi LED strip, 2 m starter kit, cuttable; both RGB and tunable white, in the same apps as the bars' bulbs (philips-hue.com; wizconnected.com)",
    "e14": "Smart colour E14 bulbs for the bars: WiZ Colour P45 E14, 4.9 W, 4.5 × 10.1 cm, Wi-Fi, no hub (Philips UK specification sheet, 8719514437333); Philips Hue White and Colour Ambiance E14 lustre, 5.1 W, 45 × 77 mm (Philips Hue; Lampmasters)",
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


def stairs_zone():
    """v14: the dining table's second site, on the stairs wall under the client's 2 m shelf."""
    g = G
    tw, td, tt = g.TABLE
    cd = g.CHAIR[1]
    south = g.STAIRS_WALL_Z[0] - g.TABLE_B_Z[0]
    north = g.TABLE_B_Z[1] - g.WINDOW_Z
    under = g.SHELF_B["top"] - g.SHELF_B["t"]
    room_side = g.TABLE_B_X[0] - cd
    swing = g.BREAST_D_WEST - g.DOOR_SWING
    bar_over = g.TABLE_B_X[0] <= g.BAR2_X <= g.TABLE_B_X[1] and g.TABLE_B_Z[1] <= g.BAR2_Z <= g.TABLE_B_Z[0]
    return ("Option: the table under the shelf, by the stairs", f"the same {r1(tw)} × {r1(td)} fold-down table on the west wall, centred {r1(-g.TABLE_B_CZ)} from the breast's face line", [
        ("The wall beside the stairs", f"table {r1(tw)} long", ref("photo20", "room"), f"{r1(g.STAIRS_WALL_Z[0] - g.WINDOW_Z)} from the stair box to the window wall",
         f"{r1(south)} to the stair box, {r1(north)} to the window wall", PASS),
        ("Folded, under the shelf", f"top edge {r1(g.FOLDED_TOP)}", ref("photo20"), f"shelf's underside about {r1(under)}", f"{r1(under - g.FOLDED_TOP)}: the shelf and what's on it stay", PASS),
        ("Down for four: the room side", f"table edge {r1(g.ROOM_W - g.TABLE_B_X[0])} out from the wall; chairs to x {r1(room_side)}", ref("dining", "terje"),
         f"the sofa's end at x {r1(g.SOFA_X[1])}", f"{r1(room_side - g.SOFA_X[1])} to walk behind the chairs (100+ is the aim, 60 the minimum){'' if room_side - g.SOFA_X[1] >= 100 else ': the walk is between the sofa’s arm and the chairs'}",
         PASS if room_side - g.SOFA_X[1] >= 100 else TIGHT if room_side - g.SOFA_X[1] >= 60 else CHECK),
        ("The stair end's chair", f"{r1(cd)} deep at the table's south end", ref("terje"), f"{r1(south)} to the stair box", f"{r1(south - cd)} behind it: tuck it in after a meal so the stair's foot stays clear", TIGHT),
        ("The window end's chair", f"{r1(cd)} deep at the north end", ref("terje"), f"{r1(north)} to the window wall", f"{r1(north - cd)} behind it", TIGHT),
        ("The door's swing", f"the door opens in, {r1(g.DOOR_SWING)} wide", ref("room"), f"its edge reaches {r1(swing)}", f"{r1(swing - g.TABLE_B_Z[0])} clear of the table: unlike the breast, nobody sits in its swing", PASS),
        ("Light over the table", "the existing pendant point, for bar 2", ref("photo20"), f"point about ({r1(g.BAR2_X)}, {r1(g.BAR2_Z)})",
         "right over the table's stair end: the bar's heads light the table directly" if bar_over else "beside the table: aim two heads at it", PASS),
        ("Fixing the brackets", "500 kg a pair, into the wall", ref("hebgo"), "the west wall's build isn't known yet", "solid (plugs and screws) or studwork (fix into studs): knock and look before choosing this site", CHECK),
    ])


def fliptop_zones():
    """v15: the flip-top gate-leg table, on the breast (A) and on the stairs wall (B): it stays on the wall, opens to 110 × 160."""
    g = G
    tw, td, tt = g.TABLE
    cw, cd = g.CHAIR[0], g.CHAIR[1]
    lw_, ld_, lt_ = g.FLIP["leaf"]
    z0, z1 = g.OPEN_Z
    tuck = 8.0
    kg_top = tw * td * tt * 0.72 / 1000
    kg_half = lw_ * ld_ * lt_ * 0.72 / 1000
    kg_gate = 2 * g.GATE_LEG_H * ((g.LEG[0] + g.LEG[1]) / 2) ** 2 * 0.72 / 1000 + (tw - 2 * g.FLIP["inset"]) * g.FLIP["apron"][0] * g.FLIP["apron"][1] * 0.72 / 1000
    leg_room = ld_ - g.FLIP["hinge_in"] - g.LEG[0] / 2              # how much of the half the folded legs can lie along
    side4, side6 = g.OPEN_LEN / 2, g.OPEN_LEN / 3
    arm_y = g.RAIL_TOP - 2.4
    common = [
        ("Open: 110 × 160, still on the wall", f"the top {r1(tw)} × {r1(td)} on its brackets, the half {r1(lw_)} × {r1(ld_)} on the gate leg", ref("hebgo", "fliphinge"), "nothing comes off the wall; no leaf to store",
         f"the table runs {r1(-z1)} out from the wall", PASS),
        ("Three flip-top hinges at the joint", f"{r1(g.FLIP['hinge'][0])} × {r1(g.FLIP['hinge'][1])}, set into both edges", ref("fliphinge"), f"a {r1(tt)} edge", f"{r1((tt - g.FLIP["hinge"][0]) / 2)} of oak either side of each hinge; they open to 180°, so the half lies flat on the top to fold", PASS),
        ("The gate leg folds inside the half", f"legs {r1(g.GATE_LEG_H)} long, hinged {r1(g.FLIP['hinge_in'])} in from the far edge", ref("legs"), f"{r1(leg_room)} of the half for them to lie along", f"{r1(leg_room - g.GATE_LEG_H)} spare", PASS if leg_room - g.GATE_LEG_H >= 0.5 else TIGHT),
        ("Folded on the wall", f"the top, the half and its gate: {r1(g.FOLDED_D)} off the wall, top edge {r1(g.FOLDED_TOP)}", ref("liftoff"), "a 7.3 hinge rail makes room for the half and gate behind the top",
         f"about {r1(g.FOLDED_D - 6.3)} deeper than v14's; the room still sees the plain oak underside", PASS),
        ("Folding it up", f"top {kg_top:.0f} kg + half {kg_half:.0f} kg + gate {kg_gate:.0f} kg", ref("liftoff", "hebgo"), "lift-off hinges for a 120 kg door; brackets 500 kg a pair",
         f"about {kg_top + kg_half + kg_gate:.0f} kg to swing up: two people, one at each corner; turn buttons hold it", TIGHT),
        ("Knees by the brackets", f"each arm {r1((tw - (g.HEBGO_X[1] - g.HEBGO_X[0])) / 2)} in from the side edge, at {r1(arm_y)}", ref("hebgo", "terje"), f"knees at about 60 over a {r1(g.CHAIR[3])} seat",
         "the first chair each side has the arm above its knees, not in them", PASS),
        ("Four: two down each side", f"{r1(side4)} of edge each", ref("dining"), f"{r1(g.DINE_W)} each", f"{r1(side4 - g.DINE_W)} spare each", PASS),
        ("Six: three down each side", f"{r1(side6)} of edge each", ref("dining"), f"{r1(g.DINE_W)} each, 55 at a squeeze", f"{r1(side6)} each: elbows in", TIGHT),
    ]
    # A: on the breast, running towards the window
    end_back_a = z1 - cd + tuck
    sofa_gap_a = z1 - g.SOFA_FRONT_Z
    east_back = g.TABLE_X[0] - cd + tuck
    third_z = z0 - side6 * 2.5                                      # the six layout's last chair down each side
    cof_clash = east_back < g.COFFEE["x"][1] and (third_z - cw / 2) < g.COFFEE["z"][1] and (third_z + cw / 2) > g.COFFEE["z"][0]
    hinge_x, hinge_z = g.DOOR_X[0], g.BREAST_D_WEST
    first6 = z0 - side6 / 2
    corner = ((g.TABLE_X[1] - tuck + cd - hinge_x) ** 2 + (first6 + cw / 2 - hinge_z) ** 2) ** 0.5
    zone_a = ("Option A: the flip-top table on the chimney breast", f"110 × 160 open, running from the breast towards the window, {r1(-z1)} out", common + [
        ("Its end and the sofa", f"the table ends {r1(-z1)} out", ref("sofa"), f"the sofa's front at {r1(-g.SOFA_FRONT_Z)}",
         f"{r1(sofa_gap_a)} between them: no chair at that end (it would need {r1(cd - tuck)}), and the way round is down the sides", CHECK if sofa_gap_a < cd - tuck else TIGHT),
        ("The coffee table", f"east-side chairs back to x {r1(east_back)}", ref("terje"), f"coffee table x {r1(g.COFFEE['x'][0])}–{r1(g.COFFEE['x'][1])}",
         "for six, slide the coffee table towards the TV before you sit down" if cof_clash else "clear", TIGHT if cof_clash else PASS),
        ("The door's swing", "door 83 wide, opens in, hinged by the breast", ref("room"), f"its edge sweeps {r1(g.DOOR_SWING)} round the hinge",
         f"the west side's first chair is {r1(corner)} from the hinge: in its swing, so keep the door shut while you eat (or rehang it to open into the hall)", TIGHT if corner < g.DOOR_SWING else PASS),
    ])
    # B: on the stairs wall, running into the room
    bz0, bz1 = g.TABLE_B_Z                                          # its long sides (south: stairs, north: window)
    bx_end = g.TABLE_B_OPEN_X[0]
    south_back = bz0 + cd - tuck
    north_back = bz1 - cd + tuck
    lamp = g.FLOOR_LAMP_SPOTS["corner"][1]
    end_lo = g.TABLE_B_CZ - cw / 2
    zone_b = ("The flip-top table under your shelf, by the stairs (B, the default)", f"110 × 160 open, running from the stairs wall into the room, its end at x {r1(bx_end)}", common + [
        ("The stair side's chairs", f"backs at z {r1(south_back)} when pulled out", ref("terje", "photo20"), f"the stair box's face at {r1(g.STAIRS_WALL_Z[0])}",
         f"{r1(g.STAIRS_WALL_Z[0] - south_back)} behind them: tuck them in after a meal so the stair's foot stays clear", TIGHT),
        ("The window side's chairs", f"backs at z {r1(north_back)}", ref("terje"), f"the window wall at {r1(g.WINDOW_Z)}",
         f"{r1(north_back - g.WINDOW_Z)} behind them; your red lamp moves from the window corner to the sofa's end or by the breast while it's open", TIGHT),
        ("A seat at its end", f"one chair at x {r1(bx_end - cd + tuck)}–{r1(bx_end + tuck)}", ref("terje", "sofa"), f"the sofa's arm ends at x {r1(g.SOFA_X[1])}, front z {r1(g.SOFA_FRONT_Z)}",
         (f"one chair, centred on the table, clears the sofa's front by {r1(end_lo - g.SOFA_FRONT_Z)}" if end_lo >= g.SOFA_FRONT_Z else
          f"one chair, centred on the table, meets the sofa's front ({r1(g.SOFA_FRONT_Z - end_lo)} over, with the sofa 13 off the wall since v17): tuck it 2 cm further under the table")
         + ": seven with three a side (a second end chair would hit the arm)", PASS if end_lo - g.SOFA_FRONT_Z >= 0 else TIGHT),
        ("Folded, under the shelf", f"top edge {r1(g.FOLDED_TOP)}, {r1(g.FOLDED_D)} off the wall", ref("photo20"), f"shelf's underside about {r1(g.SHELF_B['top'] - g.SHELF_B['t'])}",
         f"{r1(g.SHELF_B['top'] - g.SHELF_B['t'] - g.FOLDED_TOP)}: the shelf and what's on it stay", PASS),
        ("Light over the table", "the existing pendant point, for bar 2", ref("photo20"), f"point about ({r1(g.BAR2_X)}, {r1(g.BAR2_Z)})", "over the open table's stair side: the bar runs along it", PASS),
        ("Your shelf and the pipe boxing (v16)", f"the shelf {r1(g.SHELF_B['z'][0] - g.SHELF_B['z'][1])} long", ref("photo20", "room"), f"the boxing's face at z {r1(g.PIPE_BOX['z'][1])}, {r1(g.PIPE_BOX['x'][1] - g.PIPE_BOX['x'][0])} out",
         f"drawn {r1(g.SHELF_B['z'][1] - g.PIPE_BOX['z'][1])} short of it, {r1(g.SHELF_B['z'][0] - g.STAIRS_WALL_Z[0])} past the stair box (your photo: about 41)", PASS),
        ("The OBEGRÄNSAD panel on the shelf (v16)", f"{r1(g.LIGHTBOX['z'][0] - g.LIGHTBOX['z'][1])} × {r1(g.LIGHTBOX['h'])} × {r1(g.LIGHTBOX['d'])}, standing landscape at the stair end", ref("obegransad"), f"shelf top {r1(g.SHELF_B['top'])} to the {r1(g.CEIL)} ceiling",
         f"{r1(g.CEIL - g.SHELF_B['top'] - g.LIGHTBOX['h'])} over it: this needs the shelf at 198 or lower (measure it); higher, hang the panel on the wall beside the shelf instead", CHECK),
        ("The window side's chairs and the pipe boxing", f"backs at z {r1(north_back)}", ref("terje", "room"), f"the boxing's face at z {r1(g.PIPE_BOX['z'][1])} (x {r1(g.PIPE_BOX['x'][0])} to the wall)",
         f"{r1(north_back - g.PIPE_BOX['z'][1])} clear of the boxing", PASS if north_back > g.PIPE_BOX["z"][1] else TIGHT),
        ("Fixing the brackets", "500 kg a pair, into the wall", ref("hebgo"), "the west wall's build isn't known yet", "solid (plugs and screws) or studwork (fix into studs): knock and look before choosing this site", CHECK),
    ])
    return zone_a, zone_b


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
    fi = g.LEAF_FRAME
    kit_kg = 0.7 / 1000 * (g.LEAF[0] * g.LEAF[1] * g.LEAF[2] + 2 * fi["t"] * fi["h"] * (g.LEAF_FRAME_OUT[0] + g.LEAF_FRAME_IN[1])
                           + 8 * g.LEG_H * ((g.LEG[0] + g.LEG[1]) / 2) ** 2)
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
    win_first = g.SIX_X[0] + (g.SIX_X[1] - g.SIX_X[0]) / 4               # v15: the first window-side chair's centre (two a side)
    win_overlap = g.SOFA_X[1] - (win_first - cw / 2)                     # how far the sofa's end reaches past that chair's east edge
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
            ("The TV's remote receiver, bottom centre of the screen's frame (v17 check)", f"screen bottom {r1(g.TV_BOTTOM)}", ref("lg"), f"soundbar top {r1(sb_top)}, in front of the stand's foot", f"{r1(sb_top - g.TV_BOTTOM)} over the frame's edge: sit the bar on the worktop 2 cm proud of the stand's foot, not against it, so the remote's beam from the sofa clears it; if a button stutters, pair LG's Magic Remote (it talks to the TV by radio)", CHECK),
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
        ("Bay 3: the LP crates and the slim game column (v16)", f"56.4 wide × 40 deep × 69.4 tall inside the ply carcass, split by a 12 mm divider", [
            ("Across the bay", f"slim drawer {r1(g.SLIM_BOX_X[1] - g.SLIM_BOX_X[0])} + divider 1.2 + LP crate {r1(g.TRAY_BOX[0])}, each drawer with 1.27 runners a side", ref("runners"), f"{r1(g.B3_IN[1] - g.B3_IN[0])} inside",
             f"exact: {r1(g.SLIM_BOX_X[1] - g.SLIM_BOX_X[0])} + 2.54 + 1.2 + {r1(g.TRAY_BOX[0])} + 2.54 = 56.4; nothing left over", PASS),
            ("LPs in the crate", f"{r1(g.LP)} sleeves face-out, leaning back 10°", ref("media", "crate"), f"{r1(g.TRAY_INSIDE)} trough", f"{r1((g.TRAY_INSIDE - g.LP) / 2)} each side: snug like a shop crate; outer sleeves up to 32.4 still fit", TIGHT),
            ("Crate heights", "lower sleeves to 34.4, upper to 69.1", ref("media"), "top panel underside 71.2", "2.6 and 2.1 to lift a sleeve", PASS),
            ("Games in the slim drawers, face-out", f"DVD-size cases {r1(g.GAME_CASE[0])} wide, {r1(g.GAME_CASE[1])} tall, leaning back 10°", ref("media"), f"{r1(g.SLIM_INSIDE)} inside (6 mm ply sides)",
             f"{r1(g.SLIM_INSIDE - g.GAME_CASE[0])} spare: they flip like the records; about {g.SLIM_DRAWERS[0]['n']} a drawer in 40 deep", TIGHT),
            ("The game drawers' height", f"cases stand {r1(g.GAME_CASE[1] * 0.985)} on a 1.2 base", ref("media"), f"{r1(g.SLIM_DRAWERS[1]['yb'] - g.SLIM_DRAWERS[0]['yb'])} from one drawer to the next",
             f"{r1(g.SLIM_DRAWERS[1]['yb'] - g.SLIM_DRAWERS[0]['yb'] - 1.2 - g.GAME_CASE[1] * 0.985)} clear over the cases", PASS),
            ("Pads in the top slim drawer", f"4 pads on edge, two side by side: 2 × {r1(g.PAD[2])} = {r1(2 * g.PAD[2])} across, {r1(g.PAD[0])} long", ref("pads"), f"{r1(g.SLIM_INSIDE)} wide, {r1(g.TRAY_TOP_PANEL - g.SLIM_DRAWERS[2]['yb'] - 1.2)} tall",
             f"{r1(g.SLIM_INSIDE - 2 * g.PAD[2])} across; {r1(g.PAD[1])} tall in {r1(g.TRAY_TOP_PANEL - g.SLIM_DRAWERS[2]['yb'] - 1.2)}; the remotes in front", TIGHT),
        ]),
        ("The side wall: one oak run from the corner to the PC", f"one board line at {r1(g.LEDGE_TOP)}, {r1(g.SIDE_RUN_T)} thick, {r1(g.SIDE_RUN_Z[0] - g.SIDE_RUN_Z[1])} long: 7 deep along the LPs, sweeping out to {r1(g.PC_SHELF_D)} under the PC (v15)", [
            ("The sweep from the ledge to the PC shelf", f"front edge 7 → {r1(g.PC_SHELF_D)} over {r1(g.SIDE_SWEEP[0] - g.SIDE_SWEEP[1])} (z {r1(g.SIDE_SWEEP[0])} to {r1(g.SIDE_SWEEP[1])})", "", f"the last wrap LP ends at z {r1(g.WRAP_Z[0] - 1.5 - 4 * g.LP - 3 * 1.4)}; the PC starts at z {r1(g.PC_Z[0])}",
             f"the LP stands on the start of the curve; {r1(g.SIDE_SWEEP[1] - g.PC_Z[0])} between the full depth and the case", PASS),
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
            ("Six and eight: lifted off onto legs, with the leaf", f"table {r1(tw)} + leaf {r1(g.LEAF[0])} = {r1(six_len)} × {r1(td)}, top at {r1(g.LEG_H + tt)} on the oak legs", ref("legs"), f"dining height about {r1(75)}", "within 1.3; felt glides take up an uneven floor; four legs under the table, four under the leaf, joined by two dowels and two clips", PASS),
            ("The eight legs, stored in the leaf's frame (v13.6)", f"8 legs {r1(g.LEG[0])} square in clips {r1(g.LEG_CLIP[1])} wide at {r1(g.LEG_PITCH)} centres = {r1(g.LEG_STORE_W)} across; each {r1(g.LEG_H)} + {r1(g.LEG_BOLT)} bolt long", ref("clip", "legs"), f"inside the frame {r1(g.LEAF_FRAME_IN[0])} × {r1(g.LEAF_FRAME_IN[1])}, {r1(g.LEAF_FRAME['h'])} deep", f"{r1((g.LEAF_FRAME_IN[0] - g.LEG_STORE_W) / 2)} each side, {r1(g.LEAF_FRAME_IN[1] - g.LEG_H - g.LEG_BOLT)} along, {r1(g.LEAF_FRAME['h'] - g.LEG[0])} below the legs; leaf, frame and legs about {kit_kg:.0f} kg together", PASS),
            ("Knees under the leaf's frame", f"frame underside at {r1(g.LEG_H - g.LEAF_FRAME['h'])} with the table on its legs", ref("terje"), f"chair seat {r1(g.CHAIR[3])}", f"{r1(g.LEG_H - g.LEAF_FRAME['h'] - g.CHAIR[3])} above the seat, like an ordinary table's apron; the 110 top has no frame ({r1(g.LEG_H - g.CHAIR[3])})", PASS),
            ("Six: two a side, one at each end", f"{r1(six_len)} of edge each long side, {r1(td)} at each end", ref("dining"), f"{r1(g.DINE_W)} each", f"{r1(six_edge)} each on the sides (25 spare); {r1(td)} at the ends", PASS),
            ("Eight: three a side, one at each end", f"{r1(tw + g.LEAF[0])} long", ref("dining", "legs"), f"{r1(g.DINE_W)} each", f"{r1(eight_edge)} each", TIGHT),
            ("Six and eight: to the breast and the window", f"table {r1(free_breast)}–{r1(-g.FREE_Z[1])} out", ref("dining"), f"{r1(g.CLEAR_OK)} to aim for", f"{r1(free_breast)} to the breast; {r1(free_window)} to the window", PASS if free_breast >= g.CLEAR_OK else TIGHT),
            ("Six and eight: the west end", f"table end at {r1(g.SIX_X[1])}", ref("dining"), f"west wall at {r1(g.ROOM_W)}", f"{r1(six_wall)} for the end diner (60 is the tight minimum; the stairs are behind the breast-side corner, clear of it)", PASS if six_wall >= g.CLEAR_OK else TIGHT),
            ("Six and eight: the east end and the coffee table", f"end chair at x {r1(east_end)}–{r1(g.SIX_X[0])}", ref("dining", "sofa"), "coffee table and sofa", f"{r1(cof_gap)} to the coffee table's edge: slide it towards the window first; the sofa ends at {r1(g.SOFA_X[1])}, clear of the chair ({r1(eight_sofa)} to its front line)", TIGHT),
            ("Six and eight: the window side and the sofa (v15)", f"window-side chairs from x {r1(win_first - cw / 2)}, backs reach z {r1(g.FREE_Z[1] - cd)} pushed out", ref("terje", "sofa"),
             f"the sofa now runs to x {r1(g.SOFA_X[1])}, its front at z {r1(g.SOFA_FRONT_Z)}",
             (f"the first window-side chair overlaps the sofa's end by {r1(win_overlap)} and has {r1(g.FREE_Z[1] - cd - g.SOFA_FRONT_Z)} behind it: that diner sits with the sofa's arm at their back. Fine for a meal; or use the table by the stairs (option B), which stands clear of the sofa"
              if win_overlap > 0 else f"{r1(-win_overlap)} clear of the sofa's end"), CHECK if win_overlap > 0 and g.FREE_Z[1] - cd - g.SOFA_FRONT_Z < 15 else PASS),
            ("Six: the breast-side chairs and the sub's cover", f"chairs at x {r1(six_first - cw / 2)}–{r1(six_first + cw / 2)} and on, backs at {r1(chair_back)} from the breast", ref("terje"), f"cover x {r1(SB['x'][0] - SB['over'])}–{r1(SB['x'][1] + SB['over'])}, {r1(box_front)} out", f"{r1(six_sub_gap)} beside it and {r1(chair_back - box_front)} in front of it: chairs and cover don't meet", (CHECK if min(six_sub_gap, chair_back - box_front) < 0 else TIGHT if min(six_sub_gap, chair_back - box_front) < 10 else PASS)),
            ("Eight: the breast-side end chair and the sub's cover", f"chair at x {r1(e_first - cw / 2)}–{r1(e_first + cw / 2)}", ref("terje"), f"cover x {r1(SB['x'][0])}–{r1(SB['x'][1])}", (f"they overlap {r1(e_overlap)} across, so that chair can push back only {r1(chair_back - box_front)} before it meets the cover: for eight, lift the cover off its two keyhole screws and stand the sub at the end of the base (it's wireless; leave 1 m of slack in its lead)" if e_overlap > 0 else f"{r1(-e_overlap)} clear"), CHECK if e_overlap > 0 else PASS),
            ("Sub under its oak cover, under the dining wall", f"sub {r1(g.SUB[2])} long × {r1(g.SUB[0])} out × {r1(g.SUB[1])} tall, standing sideways: driver east, port west", ref("hisense"), f"cover {r1(SB['x'][1] - SB['x'][0] + 2 * SB['over'])} × {r1(-SB['z'][0] + SB['over'])} at {r1(SB['h'])} on a backboard, between the folded arms", f"{r1(SB['x'][0] - g.HEBGO_X[0] - 1.4)} clear of the east arm, {r1(g.HEBGO_X[1] - 1.4 - SB['x'][1])} of the west; {r1(over_sub)} over the sub", PASS),
            ("The sound: no sides, no front", "the driver fires east, the port west, the room side is open", ref("subport", "hisense"), f"{r1(g.SUB_PORT_MIN)} for the port", f"port {r1(port_gap)} to the nearest thing (the west arm), driver {r1(drv_gap)}; only the cover is over it, and nothing faces the driver or the port", PASS if port_gap >= g.SUB_PORT_MIN else TIGHT),
            ("Spills", f"solid oak cover {r1(SB['top'])} thick, {r1(SB['over'])} overhang with a drip groove underneath", "", "a drink knocked off the table", "it lands on the cover and runs off its edge in front of the sub, never onto it", PASS),
            ("Knocks: it can't fall over", f"the sub's top corner rises {r1(tip_rise)} before it would tip", ref("hisense"), f"cover {r1(over_sub)} over it; tray lip {r1(SB['lip'])}", f"the cover stops it {r1(tip_rise - over_sub)} short of tipping; the lip stops it sliding; the backboard hangs on two keyhole screws in the solid breast", PASS if over_sub < tip_rise else CHECK),
            ("Feet under the table, four at the wall", f"the cover {r1(box_front)} out from the breast", ref("terje"), f"table {r1(td)} deep", f"{r1(td + g.RAIL[2] - box_front)} of legroom in front of it on the room side; the end seats are clear", PASS),
            ("Chairs at the table", f"seat {r1(g.CHAIR[3])}", ref("terje"), f"top {r1(g.TABLE_TOP)}", f"{r1(g.TABLE_TOP - g.CHAIR[3])} seat to top, the usual 25–30", PASS),
        ]),
        stairs_zone(),
        ("The room", f"{r1(g.ROOM_W)} × {r1(g.ROOM_D)}, ceiling {r1(g.CEIL)}", [
            ("Eyes to screen from the sofa", "the L-sofa's long side against the window wall, 10 off the radiator", ref("room", "sofa"), f"{r1(g.SCREEN_FROM_WINDOW)} window wall to screen", f"about {g.VIEW_DIST / 100:.2f} m; a 55-inch fills about 26°", PASS),
            ("From the end of the sofa's return", f"sitting up at its end, {r1(g.TV_PANEL_Z[0] - g.CHAISE_EYES_Z)} from the screen", ref("sofa"), "straight ahead of the TV", "the TV's move puts it square on to this seat", PASS),
            ("TV centre against seated eyes", f"{r1(g.TV_CENTRE)}", ref("lg"), f"eyes at {r1(eye_lo)}–{r1(eye_hi)}", "about 1–2.5° above the eye line", PASS),
            ("Both spotlight bars under the ceiling", f"{r1(g.BAR[2])} drop", ref("wolston"), f"{r1(g.CEIL)} ceiling", f"lowest shade at {r1(g.CEIL - g.BAR[2])}", PASS),
            ("Both bars turned to run TV to window (v15)", f"{r1(g.BAR[0])} long along the room", ref("wolston", "photo20"), f"bar 2 at {r1(g.ROOM_W - g.BAR2_X)} from the west wall",
             f"bar 1 spans z {r1(g.PEND_Z + 42)} to {r1(g.PEND_Z - 42)}; bar 2 now runs along the wall, so its end no longer reaches past the west wall (v13.7's worry)", PASS),
            ("Smart colour bulbs in the bars (v15)", f"8 × E14: WiZ P45 {r1(g.BULB_E14['wiz'][1])} W, {r1(g.BULB_E14['wiz'][2][0])} × {r1(g.BULB_E14['wiz'][2][1])}; or Hue lustre {r1(g.BULB_E14['hue'][1])} W, {r1(g.BULB_E14['hue'][2][0])} × {r1(g.BULB_E14['hue'][2][1])}", ref("wolston", "e14"),
             f"the bar's {r1(g.BAR_MAX_W)} W a lamp; 15 cm shades", f"{r1(g.BAR_MAX_W - g.BULB_E14['wiz'][1])} W under; the WiZ's 10.1 sits inside a 15 shade with its holder; if it shows below the rim, the Hue's 7.7 doesn't", PASS),
        ]),
    ]
    if g.TABLE_STYLE == "fliptop":   # v15: the flip-top replaces the fold-down-and-lift-off table on both walls
        za, zb_ = fliptop_zones()
        L = g.NOW_LEDGE
        gap = (L["x"][1] - L["x"][0] - L["n"] * g.LP) / (L["n"] + 1)
        lp_top = L["top"] + g.LP * 0.99
        breast = ("The chimney breast, with the table by the stairs (v16)", f"breast {r1(g.BREAST_W)} wide; the “now playing” ledge {r1(L['x'][1] - L['x'][0])} × {r1(L['d'])}, top {r1(L['top'])}", [
            ("Three LPs on the ledge", f"3 × {r1(g.LP)} = {r1(3 * g.LP)}", ref("media"), f"{r1(L['x'][1] - L['x'][0])} long", f"{r1(gap)} between and at the ends", PASS),
            ("Leaning back 8°, under the framed LPs", f"tops at {r1(lp_top)}", ref("media"), f"frames from {r1(g.FRAMES_Y)}", f"{r1(g.FRAMES_Y - lp_top)} between", PASS),
            ("Beside the turntable", f"ledge {r1(L['top'])} up, {r1(L['d'])} deep", ref("atlp120"), f"the deck's top at about {r1(g.WORKTOP + g.DECK[1])}, an arm's reach to the left",
             "sleeve off the ledge, record on, sleeve back: the base stands 8 proud of the breast, the ledge 7", PASS),
            ("If you choose option A instead", "the flip-top folds on the breast", ref("liftoff"), "the ledge's place", "the ledge comes off its two screws; the frames stay", PASS),
        ])
        out = []
        for (title, space, rows) in zs:
            if title.startswith("The dining wall"):
                out += [zb_, breast]
            elif title.startswith("Option: the table under the shelf"):
                out.append(za)
            else:
                out.append((title, space, rows))
        return out
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


# v18: the client's plant stand and their 2 x 2 record shelf, in either layout
_zones_v17 = zones


def plants_zone():
    g = G
    P_, R_ = g.PLANT_STAND, g.RECORD_SHELF
    curt = g.WINDOW_X[1] + g.CURTAIN["ext"]                     # the curtains' west stack ends here
    box_x = g.PIPE_BOX["x"][0]
    cx, cz, _f = g.PLANT_LAYOUTS["corner"]["plants"]
    px0, px1 = cx - P_["w"] / 2, cx + P_["w"] / 2
    bw = g.BREAST_X[1] - g.BREAST_X[0]
    ledge_under = g.NOW_LEDGE["top"] - g.NOW_LEDGE["t"]
    rx = g.PLANT_LAYOUTS["breast"]["records"][0]
    return ("Your plant stand and your record shelf (v18)", f"the window wall's west end, {r1(box_x - curt)} between the curtains' stack and the pipe boxing; the chimney breast, {r1(bw)} wide", [
        ("A: the plant stand in the window corner (recommended)", f"{r1(P_['w'])} × {r1(P_['d'])} × {r1(P_['h'])}", ref("plantstand"), f"x {r1(curt)} to {r1(box_x)}",
         f"x {r1(px0)}–{r1(px1)}: {r1(px0 - curt)} from the curtains, {r1(box_x - px1)} from the boxing; daylight from the window beside it, its grow bars for the rest", TIGHT),
        ("A: the 2 × 2 record shelf on the breast", f"{r1(R_['w'])} × {r1(R_['d'])} × {r1(R_['h'])}, four trays", ref("kallax"), f"breast {r1(bw)} wide, the “now playing” ledge's underside at {r1(ledge_under)}",
         f"{r1((bw - R_['w']) / 2)} each side, {r1(ledge_under - R_['h'])} under the ledge; a step from the turntable", PASS),
        ("A: records in the 2 × 2", f"four trays, face-out, about {R_['lps_each']} LPs each", ref("kallax", "media"), "33 × 33 cubes", f"about {4 * R_['lps_each']} more LPs, flipped like the crates", PASS),
        ("B: the record shelf in the window corner, as today", f"{r1(R_['w'])} wide", ref("kallax"), f"{r1(box_x - curt)} between the curtains and the boxing", f"{r1(box_x - curt - R_['w'])} to spare", PASS),
        ("B: the plant stand on the breast", f"{r1(P_['w'])} wide, {r1(P_['h'])} tall", ref("plantstand"), f"breast {r1(bw)}", f"{r1((bw - P_['w']) / 2)} each side; the “now playing” ledge comes off (the plants stand above its height), the frames stay above", TIGHT),
        ("Power for the grow bars", "a USB or mains lead from the stand", ref("plantstand"), "the nearest socket", "A: your photo shows an extension lead in that corner today; put the grow bars on a smart plug with a schedule (about 12 hours a day). B: the double socket by bay 1 is a few steps away", CHECK),
        ("Your red lamp", "28 base", ref("room"), "the window corner is taken in A and B", f"it moves to the sofa's west end (in the 3D room, drag it anywhere)", PASS),
    ])


def zones():
    return _zones_v17() + [plants_zone()]


if __name__ == "__main__":
    for title, space, rows in zones():
        print("==", title, "|", space)
        for r in rows:
            print("  ", r[0], "|", r[1], "|", r[3], "|", r[4], "|", r[5])
    print(counts())
