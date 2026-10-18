"""v10 fit proof: every item's size with its source, the space it gets, and what's left.
Used by build_doc.py so the numbers in the plan's tables come from one place."""

# Sources, numbered as they appear in the plan's Sources list
SOURCES = {
    "sketch": "Your measured sketch of the living room (all mm): alcove 1860 × 380, chimney breast 1175, room 4670 × 3470, ceiling 2350, skirting 60 × 20",
    "lgc6": "LG OLED55C6 specifications: 122.2 × 70.3–70.4 × 4.51 cm without stand, 122.2 × 75.7 × 23 cm with stand, stand 47 cm wide, 14.1 / 15.9 kg, VESA 300 × 200 (cinemaconfig.com/products/tv/lg-oled55c6pua; Courts SG OLED55C6PSA; ee.ge OLED55C6RLA)",
    "ax5100g": "Hisense AX5100G: soundbar 92 × 6 × 9 cm (Euronics HISAX5100G); subwoofer 21.4 W × 29.4 H × 30.4 D cm (EE device page; Hisense SA: 8.4 × 11.6 × 12 in); rears 9.1 × 14.5 × 10.9 cm (Hisense SA: 3.6 × 5.7 × 4.3 in)",
    "seriesx": "Xbox Series X 15.1 × 15.1 × 30.1 cm (Wikipedia: Xbox Series X and Series S); Microsoft: at least 4 in / 10 cm all round and 4 cm above on an open stand (purexbox.com, Nov 2020)",
    "besta": "IKEA BESTÅ frame 60 × 40 × 64 cm, 20 kg per shelf (ikea.com BESTÅ frame 102.473.79; BESTÅ shelf 56 × 36)",
    "deco": "TP-Link Deco X1500: 11 × 11 × 11.4 cm, 2 gigabit ports (Laptop Outlet 3-pack listing; tp-link.com)",
    "sg108": "TP-Link TL-SG108: 15.8 × 10.1 × 2.5 cm (tp-link.com datasheet; retailer listings)",
    "consoles": "Console sizes: PS1 27.0 × 18.8 × 6.0, PS2 30.2 × 18.3 × 7.8, PS3 32.5 × 27.4 × 9.8, Xbox 360 30.9 × 25.8 × 8.3, Xbox One 33.3 × 27.4 × 7.9 cm (Wikipedia comparison pages; Neowin)",
    "bricks": "Power bricks: Xbox One about 17 × 7.4 × 5.2 cm (OEM replacement listing); Xbox 360 203 W about 21 × 7.7 × 5.5 cm (Akyga AK-PD-14 listing)",
    "lp120": "Audio-Technica AT-LP120XUSB: 45.2 × 35.2 × 14.2 cm with the lid closed (Greentoe; audiokauppa.fi; hifidiprinzio.it)",
    "media": "LP sleeve 31.4 cm (12⅜ in); 7-inch sleeve 18.3–18.4 cm; DVD keep case (PS2, Xbox 360) 19 × 13.5 × 1.4 cm; Xbox One case 17 × 13.5 × 1.1–1.2 cm (Wikipedia: Keep case; Walvis; videogamecasesize.info)",
    "hdmisw": "5-in-1 4K60 HDMI switches with remote: 16.0–17.8 × 5.8–6.9 × 1.4–2.0 cm (Digitus, iVisions USW510, Techly HDMI-4K51 datasheets)",
    "rt6x": "RetroTINK-6X CE: needs any USB supply of 5 V 2 A, no plug in the box (retrotink.com shop page). Its size isn't published: the plan keeps the 23 × 23 × 8 cm reserved since v6",
    "wolston": "Dunelm Elements Wolston 4-light spotlight bar: £49, 84 × 16 cm, 22.4 cm drop, E14 6 W max, adjustable heads (dunelm.com product 1000189449)",
    "runners": "Emuca heavy-duty full-extension runners, 400 mm, 68 kg per pair; Accuride DZ3832EC 350 mm, 43 kg; Screwfix 964VN 350 mm, 40 kg",
}
ORDER = list(SOURCES)

def ref(key):
    return f'<sup class="ref">{ORDER.index(key) + 1}</sup>'

# Each zone: (zone title, note, rows). A row: (item, size of the item, space it gets, spare, ok, source keys)
# All sizes in cm, width × depth × height unless the row says otherwise.
FIT = [
    ("Above the worktop, in the alcove (186 wide, 38 deep, worktop 76 to ceiling 235)", "", [
        ("TV between the uprights", "122.2 wide", "126.5 clear (uprights at 25.25–29.75 and 156.25–160.75)", "2.15 each side", True, ["lgc6", "sketch"]),
        ("TV height on LG's stand", "75.7 tall with stand: screen 81.4–151.8", "worktop 76 to the ledge underside at 153", "1.2 above the screen", True, ["lgc6"]),
        ("Series X on its fan stand, left zone", "stand 20.5 × 20.5 (reserved), console 15.1 wide, 36.6 tall in all", "25.25 wide × 30 deep, 76 tall to the shelf at 152", "2.4 each side; 39.4 above (Microsoft: 4+ on an open stand)", True, ["seriesx"]),
        ("Right zone: this month's game on an oak easel", "17 × 9 × 20", "25.25 wide × 30 deep", "4 each side", True, ["media"]),
        ("Soundbar at the front edge", "92 × 9 × 6", "worktop 42 deep; TV stand 23.1 deep behind it", "7 between the bar and the stand", True, ["ax5100g", "lgc6"]),
        ("Record ledge: four LPs face-out", "4 × 31.4 = 125.6", "126.5 between the uprights", "0.9 (snug)", True, ["media"]),
        ("LPs on the ledge, leaning 8°", "to 186.5", "high shelf underside at 196", "9.5 above", True, ["media"]),
        ("High shelf: books", "up to 30 tall, 15–17 deep", "35 to the ceiling, 30 deep", "5 above", True, []),
        ("High shelf: Deco B, right end", "11 × 11 × 11.4", "25.25 wide × 30 deep × 35", "Wi-Fi up high, clear of metal", True, ["deco"]),
        ("A 65-inch TV instead (for comparison)", "about 145 wide", "126.5 between the uprights", "doesn't fit", False, []),
    ]),
    ("The base in the alcove (3 + 60 + 60 + 60 + 3 = 186)", "BESTÅ frames on a 9 cm plinth; bay 3 a ply carcass. 4 cm channel + 40 frame + 2 face frame = 46 from the back wall, so the front stands 8 cm proud of the breast.", [
        ("Bays and fillers across the alcove", "3 + 60 + 60 + 60 + 3", "186", "0: the 3 cm fillers are scribed to the walls", True, ["besta", "sketch"]),
        ("Bay 1, top row: Xbox One + brick", "33.3 × 27.4 × 7.9; brick 17 × 7.4 × 5.2", "56.8 × 40 × 16", "8.1 above; 23.5 beside for the brick", True, ["consoles", "bricks"]),
        ("Bay 1, middle: Xbox 360 + brick", "30.9 × 25.8 × 8.3; brick 21 × 7.7 × 5.5", "56.8 × 40 × 16", "7.7 above; 25.9 beside", True, ["consoles", "bricks"]),
        ("Bay 1, bottom: game drawer", "case 19 × 13.5 × 1.4, about 18.5 tall leaning in a bin", "box 54.3 × 35 in a 25.2 row", "about 3 above the bins; about 48 games", True, ["media", "runners"]),
        ("Bay 2, top: PS3 + controller basket", "32.5 × 27.4 × 9.8; basket 17.5 × 16 × 10", "56.8 × 40 × 23.7", "13.9 above; 6.8 beside", True, ["consoles"]),
        ("Bay 2, middle: PS2 + HDMI switch", "30.2 × 18.3 × 7.8; switch up to 17.8 × 6.9 × 2", "56.8 × 40 × 16.5", "8.7 above; 8.8 beside", True, ["consoles", "hdmisw"]),
        ("Bay 2, bottom: PS1 + RetroTINK", "27 × 18.8 × 6; RetroTINK 23 × 23 × 8 reserved", "56.8 × 40 × 17", "9 above; 6.8 beside", True, ["consoles", "rt6x"]),
        ("Bay 3: subwoofer on a 5 cm riser", "21.4 × 30.4 × 29.4, 34.4 tall on the riser", "56.4 × 40 × 38.2 (ply base 1.8 to the shelf at 40)", "3.8 above; 9.6 behind for its port", True, ["ax5100g"]),
        ("Bay 3 shelf: pad dock, spare pads, cables", "dock 22 × 9; basket 24 × 18 × 11", "56.4 × 38 × 23.8 (41.8 to 65.6)", "about 10 above", True, []),
        ("Bay 3: hidden slim drawer", "box 53.9 × 30 × 4.5", "under the carcass top, 65.6–71.2", "300 mm runners", True, ["runners"]),
        ("Channel: Switch 2 standing on edge", "15.8 × 2.5 thick × 10.1 tall", "4 cm channel", "1.5", True, ["sg108"]),
    ]),
    ("The vinyl cabinet on the chimney breast (100 × 44 × 76)", "Breast face 117.5 wide. The cabinet stands 2 cm clear of the reveal and 2 cm off the breast for the skirting.", [
        ("Cabinet on the breast", "100 wide", "117.5", "2 at the reveal, 15.5 to the west jamb", True, ["sketch"]),
        ("Bay A: two record trays", "tray 53.9 × 40 on 1.25 runners each side", "56.4 × 40 inside the ply", "0 (as the runners specify)", True, ["runners"]),
        ("Upper tray: LPs leaning 10°", "sleeve 31.4, stands 30.9", "base top 38.2 to the top panel at 71.2", "2.1 finger room", True, ["media"]),
        ("Lower tray", "the same", "base top 3.5 to the upper tray at 37.0", "2.6 finger room", True, ["media"]),
        ("LP trough / singles trough", "31.4 / 18.3–18.4", "32.6 / 18.9", "1.2 / 0.5–0.6", True, ["media"]),
        ("Bay B: preamp, stylus, brush, kit", "preamp about 12 × 11 × 3.2", "38.2 × 38 shelf, 32.4 above it", "plenty", True, []),
        ("Bay B, lower: overflow singles spine-out", "7-inch sleeve 18.3", "38.2 × 40 × 35.2", "about 120 a row, two rows deep", True, ["media"]),
        ("On top: LP browser + turntable", "44 × 24 + 45.2 × 35.2", "100 × 45 oak top", "10.8 across; 9.8 behind the deck", True, ["lp120"]),
        ("Turntable lid open", "about 40 above the deck: to about 131", "LP frames start at 140", "9", True, ["lp120"]),
    ]),
    ("The room", "", [
        ("Eyes to screen from the sofa", "eyes 0.65 m off the window wall; screen 0.2 m into the alcove", "3.47 m window wall to the alcove back", "about 2.6–2.7 m: a 55-inch fills about 26°", True, ["sketch"]),
        ("TV centre against seated eyes", "116.6", "eyes about 105–110 seated", "2–3° above: comfortable", True, []),
        ("Spot bar headroom", "22.4 drop", "235 ceiling", "lowest shade about 212.6", True, ["wolston", "sketch"]),
        ("Sofa against the window wall", "about 205 × 92 (to confirm)", "radiator 1.58–2.95 m from the east wall", "10 cm gap behind; starts 22 cm off the east wall", True, ["sketch"]),
    ]),
]


def fit_tables():
    out = []
    for title, note, rows in FIT:
        out.append(f"<h4>{title}</h4>")
        if note:
            out.append(f"<p class='note'>{note}</p>")
        out.append("<table class='tight fit'><tr><th>Item</th><th>Item size</th><th>Space</th><th>Spare</th><th></th></tr>")
        for item, size, space, spare, ok, srcs in rows:
            refs = "".join(ref(k) for k in srcs)
            mark = "<span class='pass'>fits</span>" if ok else "<span class='fail'>no</span>"
            out.append(f"<tr><td>{item}</td><td>{size}{refs}</td><td>{space}</td><td>{spare}</td><td>{mark}</td></tr>")
        out.append("</table>")
    return "\n".join(out)


def source_list():
    return "\n".join(f"<li>{SOURCES[k]}</li>" for k in ORDER)
