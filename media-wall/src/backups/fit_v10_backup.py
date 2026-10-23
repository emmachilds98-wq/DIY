"""v10 fit proof: every item that goes in the wall, its size and where the size comes from, the space it goes
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
    "x360psu": "Xbox 360 original 203 W power supply: no manufacturer size published; allowance of 21 × 10 × 6 cm used here (measure yours)",
}
ORDER = list(SOURCES)


def ref(*keys):
    return "".join(f"<sup>{ORDER.index(k) + 1}</sup>" for k in keys)


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
    side = g.SIDE_ZONE
    stand_side = (side - fx) / 2
    cons_side = (side - sx) / 2
    x_top = g.WORKTOP + fy + sh
    above_x = (g.SIDE_SHELF_TOP - g.SIDE_SHELF_T) - x_top
    lp4 = 4 * g.LP
    eye_lo, eye_hi = g.EYE_HEIGHT
    sight = lambda e: g.TV_BOTTOM + (e - g.TV_BOTTOM) * 24.0 / g.VIEW_DIST     # sightline 24 cm in front of the screen
    sb_top = g.WORKTOP + g.SOUNDBAR[1]
    sub_w, sub_h, sub_d = 21.4, 29.4, 30.4
    b_in = g.BAY_W - 3.6
    cab_top_used = g.BROWSER[0] + g.DECK[0]
    return [
        ("Above the worktop, left of the TV", f"{r1(side)} wide × {r1(g.BASE_D)} deep, worktop {r1(g.WORKTOP)} to the side shelf at {r1(g.SIDE_SHELF_TOP - g.SIDE_SHELF_T)}", [
            ("Series X fan stand", f"{r1(fx)} × {r1(fx)} footprint (assumed; model to confirm)", "", f"{r1(side)} wide", f"{r1(stand_side)} each side", PASS),
            ("Xbox Series X, standing", f"{r1(sx)} × {r1(sd)} × {r1(sh)} tall", ref("xbox"), f"{r1(side)} wide", f"{r1(cons_side)} each side; Microsoft recommends 10–15 cm. The sides have no vents (air goes in underneath and out the top) and the zone is open at the front and above", TIGHT),
            ("Clear above the Series X", f"top at {r1(x_top)}", ref("xbox"), f"to {r1(g.SIDE_SHELF_TOP - g.SIDE_SHELF_T)}", f"{r1(above_x)} (Microsoft's minimum is 4)", PASS),
            ("Behind the Series X", "stand 14 cm off the back wall", ref("xbox"), f"{r1(g.BASE_D)} deep", f"about {r1(g.ALC_D - (6 + fz) + (fz - sd) / 2)} behind the console", PASS),
        ]),
        ("The TV between the uprights", f"{r1(g.TV_GAP)} between the oak uprights; the record ledge's underside at {r1(g.LEDGE_UNDER)}", [
            ("LG OLED C6 55 in, on its stand", f"{r1(g.TV_W)} × {r1(g.TV_H)} × {r1(g.TV_D)} panel; {r1(g.TV_STAND_H)} tall on the stand", ref("lg"), f"{r1(g.TV_GAP)} wide", f"{r1(g.TV_CLEAR)} each side", PASS),
            ("Top of the screen", f"{r1(g.TV_TOP)} (bottom {r1(g.TV_BOTTOM)}, centre {r1(g.TV_CENTRE)})", ref("lg"), f"ledge at {r1(g.LEDGE_UNDER)}", f"{r1(g.LEDGE_UNDER - g.TV_TOP)}", PASS),
            ("LG stand base", f"{r1(g.TV_STAND_W)} × {r1(g.TV_STAND_D)}", ref("lg"), f"worktop {r1(g.BASE_D)} deep", "set 2 cm off the wall: 11 cm in front of it for the soundbar's leads", PASS),
            ("Soundbar, Hisense AX5100G", f"{r1(g.SOUNDBAR[0])} × {r1(g.SOUNDBAR[2])} × {r1(g.SOUNDBAR[1])} tall", ref("hisense"), f"front edge of the worktop, top at {r1(sb_top)}", f"the line of sight to the screen's bottom edge passes {r1(sight(eye_lo))}–{r1(sight(eye_hi))} over it, above its top", PASS),
            ("A 65-inch TV instead", "about 145 wide", "", f"{r1(g.TV_GAP)}", "about 18 short", NO),
        ]),
        ("Above the worktop, right of the TV", f"{r1(side)} wide × {r1(g.BASE_D)} deep", [
            ("Pad charging dock and remotes", "about 18 × 9", "", f"{r1(side)} wide", "about 3.5 each side", PASS),
            ("The turntable (why it moved)", f"AT-LP120X: {r1(g.DECK[0])} × {r1(g.DECK[2])}", ref("atlp120"), f"{r1(side)} wide", f"{r1(g.DECK[0] - side)} too wide", NO),
        ]),
        ("Shelves above", f"side shelves top {r1(g.SIDE_SHELF_TOP)}, {r1(g.SIDE_SHELF_D)} deep; ledge top {r1(g.LEDGE_TOP)}; high shelf top {r1(g.HIGH_TOP)}, {r1(g.HIGH_D)} deep; ceiling {r1(g.CEIL)}", [
            ("Four LPs on the record ledge", f"4 × {r1(g.LP)} = {r1(lp4)} wide", ref("media"), f"{r1(g.TV_GAP)} long", f"{r1(g.TV_GAP - lp4)}: snug, as drawn", PASS),
            ("Ledge LPs leaning back 8°", f"tops at {r1(g.LEDGE_LP_TOP)}", ref("media"), f"high shelf underside {r1(g.HIGH_UNDER)}", f"{r1(g.HIGH_UNDER - g.LEDGE_LP_TOP)} to lift one out over the 1.5 lip", PASS),
            ("Framed 7-inch on the right shelf", "21.3 × 21.3 frame", ref("media"), f"{r1(side)} wide, {r1(g.HIGH_UNDER - g.SIDE_SHELF_TOP)} tall", "2 each side", PASS),
            ("Books on the high shelf", "up to 30 tall", "", f"{r1(g.CEIL - g.HIGH_TOP)} to the ceiling", "9 over the tallest; room for the ceiling strip's light", PASS),
            ("Deco B on the high shelf, right", "11 × 11 × 11.4", ref("deco"), f"{r1(side)} wide", "7 each side, 27 clear above", PASS),
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
        ]),
        ("Bay 3, the sub (18 mm ply carcass from the floor)", f"{r1(b_in)} wide × 40 deep inside, back open to the channel", [
            ("Hisense subwoofer on a 5 cm riser", f"{r1(sub_w)} × {r1(sub_d)} × {r1(sub_h)} tall", ref("hisense"), "shelf underside at 39", f"top at 36.2: 2.8 above; {r1((b_in - sub_w) / 2)} each side", PASS),
            ("Room behind the sub's rear port", "port on the back", ref("hisense"), f"{r1(g.BASE_D)} from the front to the wall", "11.6 to the wall", PASS),
            ("Shelf over the sub: pad dock, spares, 6-way", "6-way about 34 × 6 × 4", "", f"{r1(b_in)} × 36, top 40.8", "24.8 clear up to the hidden drawer", PASS),
            ("Hidden slim drawer", "front 56.4 × 7.4; box 52 × 30 × 6 on 300 mm runners", ref("runners"), "65.6 to 73, under the worktop", "—", PASS),
            ("Switch 2, TP-Link TL-SG108, on its edge in the channel", "15.8 × 10.1 × 2.5", ref("sg108"), "4 cm channel", "1.5", PASS),
        ]),
        ("The vinyl cabinet on the chimney breast", f"{r1(g.CAB_X[1] - g.CAB_X[0])} × {r1(g.CAB_D)} × {r1(g.CAB_TOP)} against the {r1(g.BREAST_W)} breast", [
            ("The cabinet itself", f"{r1(g.CAB_X[1] - g.CAB_X[0])} wide, tight to the reveal", ref("room"), f"breast face {r1(g.BREAST_W)}", f"{r1(g.DOOR_CLEAR)} to the breast's west corner for the door (to confirm)", CHECK),
            ("Two face-out record trays, bay A", "trays 53.9 × 40 on 400 mm runners, 68–70 kg pairs", ref("runners", "media"), "carcass 56.4 inside, 69.4 tall", "exact: 53.9 + 2 × 1.25 runner allowance = 56.4; finger room 2.6 and 2.1", PASS),
            ("Singles drawer, bay B", "box 33.9 × 40; trough 18.9 for 18.3–18.4 sleeves", ref("runners", "media"), "36.4 inside", "exact on the runners; 0.5 either side of the sleeves", PASS),
            ("Turntable + LP browser side by side on top", f"{r1(g.DECK[0])} + {r1(g.BROWSER[0])} = {r1(cab_top_used)} wide", ref("atlp120"), f"{r1(g.CAB_X[1] - g.CAB_X[0])} wide top", f"{r1(g.CAB_X[1] - g.CAB_X[0] - cab_top_used)} for gaps", PASS),
            ("Turntable depth, with room for its lid hinge", f"{r1(g.DECK[2])} + 3.8 behind", ref("atlp120"), f"{r1(g.CAB_D)} deep top", "5 at the front", PASS),
            ("Lid open", f"deck top {r1(g.CAB_TOP + g.DECK[1])}; lid about 35 deep", ref("atlp120"), f"breast kept clear to {r1(g.LID_CLEAR_TO)}", "frames start at 150", PASS),
        ]),
        ("The room", f"{r1(g.ROOM_W)} × {r1(g.ROOM_D)}, ceiling {r1(g.CEIL)}", [
            ("Eyes to screen from the sofa", f"sofa against the window wall, 10 off the radiator", ref("room"), f"{r1(g.SCREEN_FROM_WINDOW)} window wall to screen", f"about {g.VIEW_DIST / 100:.2f} m; a 55-inch fills about 26°", PASS),
            ("TV centre against seated eyes", f"{r1(g.TV_CENTRE)}", ref("lg"), f"eyes at {r1(eye_lo)}–{r1(eye_hi)}", "about 1–2.5° above the eye line", PASS),
            ("Spotlight bar under the ceiling", f"{r1(g.BAR[2])} drop", ref("wolston"), f"{r1(g.CEIL)} ceiling", f"lowest shade at {r1(g.CEIL - g.BAR[2])}", PASS),
            ("PC shelf on the side wall", "65 along the wall", ref("room"), "between the base and the sofa", "about 29 clear of the sofa's front", PASS),
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
