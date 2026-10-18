"""Builds the plan (v11) as HTML, then PDF via headless Chromium, plus the beginner's build guide as its own PDF.
The plan reads in build order: decision, room, media wall and fit proof, records and turntable, dining wall, side wall,
joinery, paint and light, power and network, build guide, buy list, then what's left to confirm.
Numbers come from geometry.py and fit.py."""
import base64, pathlib
import geometry as G
import fit
from diagrams import (network, front, drawer, sound, game_drawer, av, power, routes, pc_shelf, section, joints, house,
                      living_plan, why_layout, seating, dining_section)

HERE = pathlib.Path(__file__).parent
VERSION = "11"
PDF_NAME = f"Home_Network_Plan_v{VERSION}.pdf"
GUIDE_NAME = f"Build_Guide_v{VERSION}.pdf"


def img(name, alt=""):
    p = HERE / name
    mime = "jpeg" if p.suffix.lower() in (".jpg", ".jpeg") else "png"
    return f'<img src="data:image/{mime};base64,{base64.b64encode(p.read_bytes()).decode()}" alt="{alt}">'


def n(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


LPS = 2 * G.TRAY_LPS + G.LEDGE_LPS + G.WRAP_LPS             # 188
SINGLES = 2 * G.TRAY_SINGLES                               # 240

# ---------------------------------------------------------------- buy list and jobs, in build order
# (status, item, phase, qty, lo, hi)  lo/hi None = no cost
TRACK = [
    ("To do", "Put the Virgin Hub 5 into modem mode", "1 Network, now", "", None, None),
    ("To do", "Set up Deco A, Switch 1 and the PCs in bedroom 3", "1 Network, now", "", None, None),
    ("To do", "Add Deco B and Deco C over Wi-Fi for now; speed-test each room and the Xbox", "1 Network, now", "", None, None),
    ("To buy", "Cat6 patch leads, 0.5–2 m", "1 Network, now", "11", 15, 20),
    ("To buy", "TP-Link TL-SG108 8-port switch: one for the living room, one to replace the 5-port in bedroom 3", "1 Network, now", "2", 36, 50),
    ("To do", "Book one electrician visit: Cat6 from bedroom 3 down through the airing cupboard to the alcove's right corner (Deco B) and on to the kitchen (Deco C), a spare pulled with each, and the optional runs to the master and bedroom 2; swap the side-wall socket for a double <b>at the same spot</b>; a new double socket low on the side wall behind the sofa for the PC and the rear speakers <b>(new)</b>; a new ceiling point by the stairs for the second spot bar, with a two-gang LED dimmer by the door <b>(new)</b>; a fused spur for the LED drivers; fit both spot bars", "2 Electrician and cabling", "", None, None),
    ("To buy", "Cat6 solid pure copper, round (not CCA): two runs, four with the optional ones", "2 Electrician and cabling", "2–4 runs", 30, 60),
    ("To buy", "6-way surge-protected extension for the retro set (Xbox One, 360, PS3, PS2, PS1, RetroTINK) <b>(changed: switched at the wall)</b>", "2 Electrician and cabling", "1", 20, 35),
    ("To buy", "4-port USB charger, 5 V 2 A per port (HDMI switch, fan stand, pad dock, bias light)", "2 Electrician and cabling", "1", 10, 20),
    ("To buy", "USB plug, 5 V 2 A or more, for the RetroTINK on the retro 6-way", "2 Electrician and cabling", "1", 5, 10),
    ("To buy", "Cable kit: brush grommets, velcro ties, labels", "2 Electrician and cabling", "1", 20, 30),
    ("To buy", "Flat two-compartment trunking for the 4 cm channel behind the base, about 2 m", "2 Electrician and cabling", "1", 10, 20),
    ("To buy", "Slim paintable trunking: the PC drop from the shelf to the skirting and along it to the base, about 4 m <b>(changed: longer)</b>", "2 Electrician and cabling", "1", 20, 35),
    ("To buy", "PC tidy kit: braided sleeve, right-angle C13 lead, shelf-notch grommet", "2 Electrician and cabling", "1", 10, 20),
    ("To do", "Sample Farrow & Ball Card Room Green No. 79 on an A4 board; check it by day and with the LED strip on", "3 Paint", "", None, None),
    ("To buy", "Card Room Green: Estate (or Modern) Emulsion for walls, ceiling, alcove and chimney breast; Estate Eggshell for skirting, door, frame and trunking; primer and undercoat", "3 Paint", "", 200, 500),
    ("To buy", "Woodwork primer, sanding pads and sugar soap for the white skirting and door", "3 Paint", "1", 20, 40),
    ("To do", "Paint the whole room before anything is fixed: alcove and breast included; skirting and door from white to eggshell", "3 Paint", "", None, None),
    ("Done", "Check the alcove back wall for fixings (solid)", "4 Base unit", "", None, None),
    ("To do", "Measure the alcove's width at the floor, 76, 134, 155 and 196 and the ceiling, and the floor's level across it", "4 Base unit", "", None, None),
    ("To do", "Check the side wall where the ledge and PC shelf go, and the chimney breast where the dining wall goes: solid, or plasterboard on studs <b>(new)</b>", "4 Base unit", "", None, None),
    ("To buy", "Two IKEA BESTÅ 60×40×64 frames, white stained oak effect, for bays 1–2", "4 Base unit", "2", 70, 200),
    ("To buy", "Plinth for bays 1–2: 18 mm ply ladder frame 120 × 38 × 9 cm with a clear bay under bay 2, plus shims", "4 Base unit", "1", 15, 30),
    ("To buy", "Hidden plinth drawer: oak front 54 × 6, 12 mm ply box 52 × 34 × 5, 300 mm push-to-open runners <b>(moved from bay 3)</b>", "4 Base unit", "1", 30, 50),
    ("To buy", "Bay 3 carcass for the records: 18 mm birch ply, 60 × 40 × 73 cm from the floor, connector bolts <b>(changed: holds the trays)</b>", "4 Base unit", "1", 45, 80),
    ("To buy", "Two face-out record tray kits: 12 and 9 mm birch ply cut to size, 6 mm oak dividers, 15 mm oak lips, raked rests, felt, two pairs of 400 mm runners rated 68–70 kg", "4 Base unit", "2", 150, 240),
    ("To buy", "BESTÅ shelves, 56 × 36 cm (20 kg max each), two each for bays 1 and 2", "4 Base unit", "4", 12, 32),
    ("To buy", "Anti-tip brackets and 4 cm spacer blocks: both frames and bay 3", "4 Base unit", "1 set", 15, 25),
    ("To do", "Measure about ten games of each kind (PS2, Xbox 360, Xbox One) before cutting the game drawer", "4 Base unit", "", None, None),
    ("To buy", "Game drawer kit: 12 mm birch ply cut to size, 350 mm full-extension soft-close runners (35–49 kg), oak lip, follower block, felt", "4 Base unit", "1", 50, 90),
    ("To buy", "Compact isolation riser for the sub, about 30 × 35 cm, 4–6 cm tall", "4 Base unit", "1", 20, 40),
    ("To do", "Build the plinth and bay 3, fix everything to the wall, fit the shelves, drawers and trays; place the TV and soundbar", "4 Base unit", "", None, None),
    ("To buy", "Two solid oak uprights, 165 × 30 × 4.5 cm (cut to 159), quarter-sawn if possible", "5 Oak joinery", "2", 150, 300),
    ("To buy", "Solid oak for the shelves: high shelf in two lengths (128.9 and 51.7 × 30 × 4), Series X shelf 55 × 30 × 4, record ledge 128.9 × 7 × 2.4, wrap ledge 134 × 7 × 2.4, PC shelf 82 × 28 × 4, lips <b>(changed)</b>", "5 Oak joinery", "1 set", 200, 340),
    ("To buy", "Oak wedges, 10 mm oak dowel for pegs and dowels, concealed upright brackets; two concealed shelf brackets for the PC shelf, rated 40 kg+ a pair", "5 Oak joinery", "1", 30, 60),
    ("To buy", "One solid oak worktop, 300 × 62 cm, full stave: the alcove top (186 × 46) and the dining wall's backboard (110 × 22) from the offcut, chamfered fronts <b>(changed)</b>", "5 Oak joinery", "1", 250, 450),
    ("To buy", "Oak face frame, 20 mm, 186 cm for the base", "5 Oak joinery", "1", 60, 120),
    ("To buy", "Cane screen for the PC: oak frame and pre-woven cane, 26 × 48 cm", "5 Oak joinery", "1", 20, 40),
    ("To do", "Cut the joints and fit the uprights, shelves, ledges and face frame; notch the uprights for the ceiling strip", "5 Oak joinery", "", None, None),
    ("To buy", "Solid oak table top 110 × 80 × 2.7 and a 60 × 80 × 2.7 leaf (edge-glued staves from a timber merchant, or cut from a 90 cm deep oak worktop) <b>(new)</b>", "6 Dining wall", "1 set", 200, 380),
    ("To buy", "Two Häfele Hebgo heavy-duty folding brackets, 287.43.428 (580 arm, 500 kg a pair) <b>(new)</b>", "6 Dining wall", "2", 70, 120),
    ("To buy", "Union PowerLoad lift-off hinges, 100 × 88, one 3-pack (all the same hand) <b>(new)</b>", "6 Dining wall", "1", 16, 20),
    ("To buy", "Eight Emuca Ø60 × 710 mm screw-in table legs with plates (two sets of four): four for the top, four for the leaf <b>(new)</b>", "6 Dining wall", "2 sets", 70, 140),
    ("To buy", "Two oak turn buttons, two leaf-alignment dowels and two table clips for the leaf, felt pads <b>(new)</b>", "6 Dining wall", "1", 10, 20),
    ("To buy", "Four folding chairs, IKEA TERJE or similar (skip if yours fit: seat about 45–48) <b>(new)</b>", "6 Dining wall", "4", 100, 160),
    ("To buy", "Two LP frames for the chimney breast, hung from 165 cm", "6 Dining wall", "2", 20, 40),
    ("To do", "Fix the backboard to the breast, hang the brackets and the top, check it folds and locks; set the legs to the right height", "6 Dining wall", "", None, None),
    ("To buy", "LED for the upright grooves: 2700K strip, two aluminium channels, driver; 6500K bias light for the TV", "7 Lighting", "1", 40, 90),
    ("To buy", "Two Dunelm Elements Wolston 4-light spotlight bars (£49 each), plus eight warm-white (2700K) dimmable E14 LED bulbs, 6 W max <b>(changed: two)</b>", "7 Lighting", "2", 120, 160),
    ("To buy", "Later: aluminium channel and opal diffuser for the existing ceiling LED strip (optional)", "7 Lighting", "1", 0, 80),
    ("To buy", "5-in-1 4K60 HDMI switch with remote", "8 TV, consoles and AV", "1", 20, 35),
    ("To do", "Measure the PC-to-TV cable route (about 4–5 m along the skirting)", "8 TV, consoles and AV", "", None, None),
    ("To buy", "Active optical HDMI cable for the PC, certified Ultra High Speed (48 Gbps), about 5 m", "8 TV, consoles and AV", "1", 20, 60),
    ("To buy", "High Speed HDMI leads, 1–2 m; two 90° HDMI adapters in case the TV's plugs need them", "8 TV, consoles and AV", "5 + 2", 25, 40),
    ("To buy", "RetroTINK-6X CE upscaler for the PS2 and PS1 (order on restock; UK price includes VAT and import fees)", "8 TV, consoles and AV", "1", 200, 240),
    ("To buy", "PS2 component video cable, good quality", "8 TV, consoles and AV", "1", 10, 20),
    ("To buy", "Optical (TOSLINK) cable, 2 m, PS2 straight to the soundbar", "8 TV, consoles and AV", "1", 5, 10),
    ("To buy", "RGB SCART cable for the PS1", "8 TV, consoles and AV", "1", 8, 15),
    ("To do", "Connect the TV inputs; set up the PS2 and RetroTINK", "8 TV, consoles and AV", "", None, None),
    ("To buy", "Replacement stylus for the turntable (exact match for its model)", "9 Vinyl kit", "1", 15, 40),
    ("To buy", "External phono preamp (only if the deck has a PHONO/LINE switch)", "9 Vinyl kit", "1", 40, 100),
    ("To buy", "RCA-to-3.5 mm lead, 2 m: preamp under the Series X shelf to the soundbar's AUX <b>(changed: shorter)</b>", "9 Vinyl kit", "1", 5, 10),
    ("To buy", "Isolation feet for the turntable; a carbon-fibre record brush", "9 Vinyl kit", "1", 20, 40),
    ("To do", "Set the tracking weight; soundbar in Music mode", "9 Vinyl kit", "", None, None),
    ("To do", "Turn on HDMI-CEC (SIMPLINK); PS3 Control for HDMI off", "10 Finishing", "", None, None),
    ("To do", "Deco app: prioritise the Series X and PC, guest Wi-Fi, automatic firmware", "10 Finishing", "", None, None),
    ("To do", "Label both outlets of the double socket (left: everything, right: retro) and each HDMI switch input", "10 Finishing", "", None, None),
    ("To do", "Set the sub and rear speaker levels from the sofa", "10 Finishing", "", None, None),
]
PHASES = []
for r in TRACK:
    if r[2] not in PHASES:
        PHASES.append(r[2])
BIGGEST = {"1 Network, now": "two 8-port switches", "2 Electrician and cabling": "Cat6 and trunking", "3 Paint": "paint",
           "4 Base unit": "record trays and the BESTÅ frames", "5 Oak joinery": "the solid oak worktop", "6 Dining wall": "the oak table top",
           "7 Lighting": "two spot bars", "8 TV, consoles and AV": "RetroTINK-6X CE", "9 Vinyl kit": "phono preamp", "10 Finishing": "—"}


def money(a, b):
    return f"{a:,}–{b:,}"


def phase_totals():
    rows, tl, th = [], 0, 0
    for ph in PHASES:
        lo = sum(r[4] for r in TRACK if r[2] == ph and r[4] is not None)
        hi = sum(r[5] for r in TRACK if r[2] == ph and r[5] is not None)
        tl += lo; th += hi
        extra = ", plus the electrician" if ph.startswith("2 ") else ""
        rows.append(f"<tr><td>{ph}</td><td class='num'>{money(lo, hi) if hi else '—'}{extra}</td><td>{BIGGEST[ph]}</td></tr>")
    rows.append(f"<tr class='total'><td>Total</td><td class='num'>{money(tl, th)}, plus the electrician</td><td></td></tr>")
    return "\n".join(rows), tl, th


def tracker_rows():
    out, cur = [], None
    for st, item, ph, q, lo, hi in TRACK:
        if ph != cur:
            out.append(f"<tr class='ph'><td colspan='5'>{ph}</td></tr>")
            cur = ph
        box = "☑" if st == "Done" else "☐"
        est = money(lo, hi) if lo is not None else ("Quote" if "electrician" in item else "")
        out.append(f"<tr><td class='st'>{box} {st}</td><td>{item}</td><td class='num'>{q}</td><td class='num'>{est}</td><td class='paid'></td></tr>")
    return "\n".join(out)


def key_table():
    from render import JOIN_KEY
    groups, cur = [], None
    for it in JOIN_KEY:
        if it[0] == "H":
            cur = [it[1], []]; groups.append(cur)
        else:
            cur[1].append(it)
    left, right = groups[:3], groups[3:]
    def col(gs):
        out = []
        for name, items in gs:
            out.append(f"<tr><td colspan='2' class='kg'>{name}</td></tr>")
            out += [f"<tr><td class='kn'>{num}</td><td>{lab}</td></tr>" for num, _, lab in items]
        return "<table class='key'>" + "".join(out) + "</table>"
    return "<div class='keycols'>" + col(left) + col(right) + "</div>"


OTHER_SOURCES = [
    "Virgin Media: Hub 5 modem mode",
    "RetroTINK: Introducing the RetroTINK-6X CE (inputs including TOSLINK, deinterlacing); RetroTINK-2X Pro listed as legacy; RetroTINK-4K CE",
    "Expert Reviews: LG C6 OLED review (4 × HDMI 2.1, one eARC, ports on the left); JB Hi-Fi: LG C6 specifications (165 Hz mode for PC sources)",
    "Hisense AX5100G spec sheet (inputs, auto power-on); JB Hi-Fi Business: AX5100G (rears linked by cable, wireless to the soundbar)",
    "TP-Link: Deco X1500 specifications (two gigabit ports per unit)",
    "Glorious Vinyl Vault specifications (80 LPs and 24.5 kg per drawer), a check on the tray capacity",
    "Screwfix: Essentials 964VN 350 mm runners; Metrol: Accuride DZ3832EC; IKEA: BESTÅ drawer runners",
    "NIST SP 500-252 / CLIR pub121: Care and Handling of CDs and DVDs (store upright, book style)",
    "Sony PS3 and Microsoft Xbox 360 S manuals: ventilation; IKEA UK: secure it",
    "Ideal Home: colour drenching; The Paint Shed: colour drenching with Farrow &amp; Ball; Livingetc: sage green shades (Card Room Green, Treron, Sage Green, Green Smoke)",
    "Pontata: Card Room Green vs Little Greene Sage Green (approximate screen colours)",
    "Homebase and NC Tiles: Farrow &amp; Ball Card Room Green No. 79 in Modern Eggshell and Estate Eggshell",
    "haart Medway: floor plans and listing photos for the house (Portsmouth Close)",
    "ConsoleMods: PS2 Component Video Out setting",
    "GOV.UK, Approved Document P (electrical safety, dwellings): which electrical work is notifiable",
]


# ---------------------------------------------------------------- the beginner's build guide (in the plan and as its own PDF)
TOOLS = [
    ("Measure and mark", [
        ("Tape measure (5 m) and a steel rule", "every cut and every height", "Buy", "10–15"),
        ("Combination square", "squaring lines across boards and checking corners", "Buy", "10–15"),
        ("Spirit level, 60 cm and 120 cm", "levelling the base, the shelves and the table", "Buy", "15–30"),
        ("Cross-line laser level", "marking all the heights round the alcove in one go", "Buy or borrow", "30–60"),
        ("Cable and pipe detector", "checking every wall before you drill: non-negotiable", "Buy", "15–30"),
        ("Pencil, masking tape, a marking knife", "marking cuts (tape stops oak splintering)", "Buy", "5"),
    ]),
    ("Cut", [
        ("Track saw, or a circular saw with a straight-edge guide", "the worktop, the table top and the long shelves", "Hire or borrow", "25–40 a day"),
        ("Jigsaw", "notches and the cable slot", "Buy or borrow", "40–70"),
        ("Tenon saw (Japanese pull saw is easiest)", "the tenons and the wedge kerfs", "Buy", "15–25"),
        ("Sharp chisels, 6, 12 and 25 mm, and a mallet", "cleaning out mortises and housings", "Buy", "30–50"),
    ]),
    ("Drill and fix", [
        ("Cordless drill-driver (18 V)", "pilot holes and screws; most of the job", "Buy or borrow", "60–120"),
        ("SDS or hammer drill with masonry bits", "plugs into the brick walls and the chimney breast", "Hire or borrow", "15–25 a day"),
        ("Dowel jig and 10 mm brad-point bit", "the dowels under the uprights and at the wrap ledge", "Buy", "20–35"),
        ("Clamps: four 60 cm sash or F-clamps, four small", "glue-ups and holding work while you fix it", "Buy", "40–60"),
        ("Stud finder (if any wall is plasterboard)", "finding studs to fix into", "Buy", "15"),
    ]),
    ("Shape and finish", [
        ("Router (1/4 in is enough) with a straight bit and a guide", "the housings, the LED grooves and the cable groove", "Hire, borrow or buy", "60–120"),
        ("Random-orbit sander, 120 and 180 grit", "smoothing the oak before oiling", "Buy or borrow", "40–70"),
        ("Hardwax oil, lint-free cloths, a brush", "finishing the oak", "Buy", "25–35"),
    ]),
    ("Safety", [
        ("Safety glasses, ear defenders, FFP2 dust masks", "every cut, every sanding job; oak dust is an irritant", "Buy", "15–25"),
        ("Work gloves; a first-aid kit", "handling boards and sheet goods", "Buy", "10"),
        ("A sturdy step ladder", "the high shelf, the ceiling and the PC shelf", "Borrow", "—"),
    ]),
]


def tools_html():
    out = ["<table class='tight tools'><tr><th>Tool</th><th>What it's for</th><th>Get it</th><th>About £</th></tr>"]
    for grp, items in TOOLS:
        out.append(f"<tr class='ph'><td colspan='4'>{grp}</td></tr>")
        out += [f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td class='num'>{d}</td></tr>" for a, b, c, d in items]
    out.append("</table>")
    return "\n".join(out)


def guide_html():
    g = G
    return f"""
<p>This guide assumes you've hung shelves and put flat-pack together, but haven't cut a joint before. Every step says what to do,
what to check before moving on, and roughly how long it takes the first time. Where a step is a job for a professional, it says so.
Sizes are finished sizes in centimetres.</p>

<div class="callout"><b>Before you start: five rules</b><ul>
<li><b>Check every wall before you drill.</b> Run the cable and pipe detector over the spot, and never drill straight above, below or beside a socket or switch: cables run vertically and horizontally from them.</li>
<li><b>Measure twice, mark once, cut once.</b> Walls are rarely square: measure the alcove at the floor, 76, 134, 155, 196 and the ceiling, and cut to the smallest.</li>
<li><b>Two people for anything over 15 kg</b>: the uprights, the worktop, the table top, the TV.</li>
<li><b>Mains wiring is the electrician's.</b> Swapping the socket, the new socket behind the sofa and the new ceiling point are all theirs. Adding to existing circuits like this isn't normally notifiable under Part P, but a registered electrician certifies it either way.</li>
<li><b>Dry-fit everything</b> (assemble without glue or screws) before the final fix.</li>
</ul></div>

<h3>Tools</h3>
<p>You don't need a workshop. Hire the two big tools for a weekend (a track saw and an SDS drill), or ask the timber merchant to cut the oak and ply to the cut lists: most will, for a small charge, and that removes the hardest cuts.</p>
{tools_html()}

<h3>Six techniques you'll use</h3>
<ol>
<li><b>Fixing into brick.</b> Detect, mark, drill with the SDS on hammer setting, clear the dust, push in a brown (7 mm) wall plug and drive a 5 × 60 mm screw. In plasterboard, find a stud, or use heavy-duty plasterboard fixings rated for the load.</li>
<li><b>Cutting oak cleanly.</b> Put masking tape over the cut line, score it with a knife, cut with the good face down (circular or track saw) or up (jigsaw). Clamp a straight edge as a guide.</li>
<li><b>Routing a housing</b> (a shallow slot a shelf sits in). Clamp a straight batten as a guide, set the bit 4 mm deep, rout, then step down to 12 mm in passes. Practise on an offcut first.</li>
<li><b>A wedged through-tenon.</b> Mark the 6 × 2.4 cm mortise on both faces of the upright and drill most of it out with a 20 mm bit from each side. Chisel it to the line. Saw the tenon on the shelf's end. Saw a kerf down its middle, glue it, tap it home, then drive a glued oak wedge into the kerf. When it's dry, saw it flush and plane it.</li>
<li><b>Dowelling.</b> Use a dowel jig to drill matching 10 mm holes 3 cm deep in both parts, glue the dowels, clamp.</li>
<li><b>Oiling.</b> Sand to 180 grit, wipe off the dust, rub on a thin coat of hardwax oil, wipe off the excess after 15 minutes, let it dry overnight, give it a second coat. Do the undersides too, so the boards don't cup.</li>
</ol>

<h3>The order of work</h3>
<table class="tight steps"><tr><th>#</th><th>Stage</th><th>What to do</th><th>Check before moving on</th><th>Time</th></tr>
<tr><td>1</td><td>Measure</td><td>The alcove's width at six heights, the floor's level, the breast's flatness, the door's swing, the sofa's size; count your records and games.</td><td>Numbers within 1 cm of the plan, or tell me and I'll redraw.</td><td>2 h</td></tr>
<tr><td>2</td><td>Network, stage 1</td><td>Hub in modem mode; Decos and switches over Wi-Fi.</td><td>Internet in every room.</td><td>2 h</td></tr>
<tr><td>3</td><td>Electrician</td><td>Cat6 runs, the double socket, the socket behind the sofa, the second ceiling point and dimmer, the fused spur. Mark every cable route on the wall.</td><td>The certificate, and photos of where the cables run.</td><td>1–2 days (theirs)</td></tr>
<tr><td>4</td><td>Paint</td><td>The whole room in Card Room Green; skirting and door in eggshell. Let it cure a week before fixing anything.</td><td>Two even coats; no white showing at the edges.</td><td>2–3 days</td></tr>
<tr><td>5</td><td>Mark the heights</td><td>With the laser: 73 and 76 (worktop), 130 and 134 (Series X shelf), 153 and 155.4 (ledges), 192 and 196 (high shelf); the uprights at {n(g.UP_L[0])}–{n(g.UP_L[1])} and {n(g.UP_R[0])}–{n(g.UP_R[1])} from the side wall; the dining wall's backboard at {n(g.RAIL_TOP - g.RAIL[1])}–{n(g.RAIL_TOP)}, centred on the breast.</td><td>Lines level end to end; the uprights' lines plumb.</td><td>1 h</td></tr>
<tr><td>6</td><td>Base</td><td>Build the plinth (with the drawer bay under bay 2), level it with shims, stand the two BESTÅ frames on it; build bay 3 from ply and bolt it on. Spacers to the wall, anti-tip brackets, trunking in the channel, cables run in.</td><td>The tops level within 1 mm across 186; nothing rocks.</td><td>1 day</td></tr>
<tr><td>7</td><td>Worktop</td><td>Scribe the worktop to the walls, cut the TV slot and the grommet hole, oil all over, screw it up through the tops in slotted holes.</td><td>Tight to the walls; the slot over the channel.</td><td>½ day</td></tr>
<tr><td>8</td><td>Inside the base</td><td>Shelves at the fit-proof heights; the game drawer; the record trays' runners at 2.3 and 37.0, then the trays; the plinth drawer.</td><td>Every drawer runs smoothly; trays clear each other by 2 cm.</td><td>1–2 days</td></tr>
<tr><td>9</td><td>Uprights and shelves</td><td>Cut the housings and mortises on the bench. Dry-fit each upright with its shelves. Lay Deco B's leads in the groove behind the right upright. Stand the uprights on their dowels and fix the brackets, then fit the high shelf, the ledge, the Series X shelf (wedge the tenons) and the pegs.</td><td>Uprights plumb; shelves level; the TV slides between with 2 cm each side.</td><td>2–3 days</td></tr>
<tr><td>10</td><td>Side wall</td><td>The oak cleat for the wrap ledge and the PC shelf; dowel the wrap ledge to the left upright's front edge; the concealed PC brackets; the cane screen; the trunking down to the skirting.</td><td>One level line with the ledge over the TV; the PC shelf takes your weight leaning on it.</td><td>1 day</td></tr>
<tr><td>11</td><td>Dining wall</td><td>Screw the backboard to the breast (plugs every 20 cm). Fit the two Hebgo brackets on its face, 80 apart, arm tops level with its top. Screw the lift-off hinges to its top edge and the table's back edge. Hang the table, fit the turn buttons at the top, fit the leg plates underneath.</td><td>Folds up and down without binding; brackets lock both sides; it doesn't move when you lean on it.</td><td>1 day</td></tr>
<tr><td>12</td><td>Lighting</td><td>LED in the upright grooves, the ceiling strip through its notches, the bias light; aim both spot bars.</td><td>No head shines at the screen or into your eyes from the sofa.</td><td>½ day</td></tr>
<tr><td>13</td><td>Connect</td><td>TV, soundbar, consoles, deck, PC; network stage 2; label every plug and input.</td><td>The "done when" list in the network section.</td><td>1 day</td></tr>
</table>
<p>Roughly 12–15 working days spread over a few weekends, plus the electrician and the paint drying. Steps 6–11 can be split: the base and dining wall first, the oak joinery once you're confident.</p>

<h3>Where beginners usually go wrong</h3>
<ul>
<li><b>Cutting the worktop to the tape instead of to a template.</b> Make a cardboard template of the alcove first; walls are rarely square.</li>
<li><b>Skipping the dry-fit.</b> Gluing a tenon that doesn't fit is the one mistake you can't undo.</li>
<li><b>Oil on one side only.</b> The board cups within a week.</li>
<li><b>Loading the trays before the anti-tip brackets go in.</b> A full tray weighs about 32 kg.</li>
<li><b>Folding the table up with something on it.</b> Clear it first, every time, and keep both turn buttons turned when it's up.</li>
</ul>
"""


def build():
    ptot, tl, th = phase_totals()
    c = fit.counts()
    nfit = sum(c.values())
    css = (HERE / "doc.css").read_text()
    s = G.summary()
    g = G
    html = f"""<!doctype html><html><head><meta charset="utf-8"><title>Home Network &amp; Media Wall Plan</title>
<style>{css}</style></head><body>

<div class="p1">
<h1>Home Network &amp; Media Wall Plan</h1>
<p class="byline">Revised Oct 18, 2026 · @emma · version {VERSION}, drawn to your measurements</p>

<div class="decision"><b>What changed in v11.</b> The TV moves <b>{n(g.TV_SHIFT)} cm nearer the side wall</b>. The two narrow gaps beside it become one {n(g.RZ_W)} cm zone, so the <b>turntable comes back into the alcove</b>, with the Series X on an oak shelf above it and both record trays in the bay below. The record ledge <b>wraps round onto the side wall</b>, with the PC on a shelf above the end of the L-sofa. The chimney breast gets a <b>fold-down oak dining table</b> for four (six or eight with it lifted off), and a <b>second spotlight bar</b> hangs over it by the stairs.</div>

<h2>1 · The plan on a page</h2>
<div class="hero">
<figure class="render">{img("render_v11_join_clean.png", "The artisan oak media wall in Card Room Green with the dining wall folded")}
<figcaption>Drawn to your measurements, in Card Room Green: the alcove with the turntable zone on the right, the dining wall folded on the chimney breast, both spot bars. Full-resolution renders come with this plan.</figcaption></figure>
<div class="summary">
<div><b>£{money(tl, th)}</b><span>plus the electrician, item by item in section 11</span></div>
<div><b>{c[fit.PASS]} of {nfit}</b><span>fit checks pass outright; {c[fit.TIGHT]} are tight, {c[fit.CHECK]} need a check on site (section 3)</span></div>
<div><b>{LPS} · {SINGLES} · 4–8</b><span>LPs and singles, all face-out · seats at the table</span></div>
</div></div>
<table><tr><th>Area</th><th>Decision</th></tr>
<tr><td>Alcove</td><td>The TV between two oak uprights, the left one now a corner post on the side wall; on the right, the turntable on the worktop and the Series X on a shelf at {n(g.RZ_SHELF_TOP)}; below, three 60 cm bays: the Xbox consoles, the PlayStations and the two record trays.</td></tr>
<tr><td>Side wall</td><td>The record ledge wraps the corner with four more LPs, then an oak shelf for the PC above the end of the sofa, clear of the TV's sightlines; the sub on the floor by the wall.</td></tr>
<tr><td>Dining wall</td><td>A 110 × 80 solid oak table on an oak backboard: folded flat every day, down on two Häfele Hebgo brackets for four, lifted off onto legs for six, with a leaf for eight.</td></tr>
<tr><td>Records</td><td>Every record face-out: about {LPS} LPs (180 in the trays, 8 on the two ledges) and {SINGLES} singles.</td></tr>
<tr><td>Heights</td><td>Worktop and table {n(g.WORKTOP)} · TV centre 116.5 · Series X shelf {n(g.RZ_SHELF_TOP)} · ledges and PC shelf {n(g.LEDGE_TOP)} · high shelf {n(g.HIGH_TOP)}, {n(g.CEIL - g.HIGH_TOP)} under the {n(g.CEIL)} ceiling.</td></tr>
<tr><td>Colour and light</td><td>Card Room Green No. 79, colour-drenched. The ceiling LED strip, LED grooves in the uprights, a bias light, and two Wolston-style spot bars: one on the existing rose, one on a new point over the dining area.</td></tr>
<tr><td>Power and network</td><td>The side-wall socket becomes a double: left for the 10-gang (everything modern), right for the retro set, switched at the wall. A new socket behind the sofa for the PC and the rears. Deco A in bedroom 3, Cat6 down the airing cupboard.</td></tr>
</table>
<p class="confirm"><b>To confirm (full list in section 12):</b> the L-sofa's size · where the door to the hall hinges, and the west end's sizes · the turntable, PC case and fan stand models · chairs you already have · where the leaf and legs live · the 23 × 22 cm box by the window.</p>
</div>

<h2 class="pb">2 · The room</h2>
<p>Everything is drawn from your hand-measured sketch; where the agent's floor plan disagrees, your tape wins. The L-sofa is drawn at a typical {n(g.SOFA_W)} × {n(g.SOFA_D)} cm (a corner sofa of that size<sup>{fit.ORDER.index("sofa") + 1}</sup>) until you measure yours.</p>
<figure>{living_plan()}</figure>
<table class="tight"><tr><th>From your sketch</th><th>mm</th><th>Notes</th></tr>
<tr><td>Room, east to west along the window</td><td class="num">{n(g.ROOM_W*10)}</td><td>The media wall is the south wall, shared with the hall and garage</td></tr>
<tr><td>Window wall to the alcove's back wall</td><td class="num">{n(g.ROOM_D*10)}</td><td>To the chimney breast's face: {n((g.ROOM_D - g.ALC_D)*10)}</td></tr>
<tr><td>Ceiling</td><td class="num">{n(g.CEIL*10)}</td><td></td></tr>
<tr><td>TV alcove, east wall to the breast</td><td class="num">{n(g.ALC_W*10)} × {n(g.ALC_D*10)}</td><td>Floor to ceiling</td></tr>
<tr><td>Chimney breast</td><td class="num">{n(g.BREAST_W*10)}</td><td>Projects 380 on the alcove side, 390 on the west side: the dining wall</td></tr>
<tr><td>Window and radiator (north wall)</td><td class="num">2350 · 1370</td><td>Window starts 730 from the east wall; radiator ends 130 inside its west end</td></tr>
<tr><td>Skirting</td><td class="num">60 × 20</td><td>White now; Card Room Green eggshell in the plan</td></tr>
<tr><td>West end: recess, door, stair box</td><td class="num">935 / 1045 / 660 / 820</td><td>Drawn roughly: please confirm which is which</td></tr>
</table>
<p><b>From the sofa:</b> from the middle of the long side your eyes are about {s["view_dist"]/100:.2f} m from the screen, which a 55-inch fills at about {s["view_angle"]:.0f}°: right for TV and games. With the TV {n(g.TV_SHIFT)} cm nearer the side wall, it now sits square on to the end of the sofa's return ({n(s["chaise_dist"])} cm away), and only about {s["sofa_mid_off_axis_deg"]:.0f}° off-centre from the middle of the long side. The screen's centre at 116.5 cm is 1–2.5° above a seated eye line. Both spot bars hang {n(g.BAR[2])} cm, so the lowest shade is at {n(g.CEIL - g.BAR[2])} cm: no headroom worries.</p>
<h3>The house</h3>
<figure>{house()}</figure>
<p>Deco A and Switch 1 sit with the Hub 5 and the gaming PCs in bedroom 3; both Cat6 runs go across the landing and drop through the airing cupboard, which sits over the alcove's corner (section 9).</p>

<h2 class="pb">3 · The media wall</h2>
<figure>{why_layout()}</figure>
<div class="why"><b>Why this layout, and what we ruled out</b>
<ul>
<li><b>The TV in the middle (v10):</b> left two {n(25.25)} cm gaps either side, too narrow for a turntable, so the vinyl had to move out to the chimney breast. Moving the TV joins them into one {n(g.RZ_W)} cm zone.</li>
<li><b>The turntable with the Series X beside it:</b> 45.2 + 20.5 cm won't go in 50.5. The Series X goes up on a shelf instead, above the lid's swing, where it gets more air than it had in v10 (15 cm each side, 21 above).</li>
<li><b>The vinyl cabinet on the breast as well as a table:</b> a table needs the breast's full width, and a cabinet in front would put the diners 44 cm further into the room.</li>
<li><b>A gateleg table in the recess:</b> it would block the door; the breast is the only clear wall.</li>
</ul></div>
<figure class="render">{img("render_v11_join_key_scene.png", "Render with numbered parts")}
<figcaption>Numbered view: the game drawer and the lower record tray are pulled out 30 cm, with a view of each from above. Dashed lines show what's hidden: gold for data, audio and low-voltage leads, coral for mains. The sofa isn't drawn so the base stays in view; the room plan shows it.</figcaption></figure>
{key_table()}

<h3>Built to your alcove: {n(g.ALC_W)} wide, {n(g.ALC_D)} deep, {n(g.CEIL)} to the ceiling</h3>
<ul>
<li><b>Base:</b> 3 cm filler, three 60 cm bays, 3 cm filler. Bays 1 and 2 are IKEA BESTÅ 60×40×64 frames on a 9 cm plinth (tops at 73, back panels off); bay 3 is an 18 mm ply carcass 60 × 40 × 73 from the floor, for the record trays. One oak face frame runs across all three; its bottom rail hides the plinth and a push-to-open hidden drawer under bay 2.</li>
<li><b>Depth:</b> 40 cm frames, a 4 cm cable channel behind and the 2 cm face frame make {n(g.BASE_D)} cm from the back wall, {n(g.BASE_PROUD)} cm proud of the chimney breast.</li>
<li><b>Worktop:</b> solid oak, {n(g.ALC_W)} × {n(g.BASE_D)} × 3, top at 76, with a brush-lined slot behind the TV and a grommet behind the deck.</li>
<li><b>Oak uprights:</b> 4.5 × 30 cm, {n(g.UPRIGHT_LEN)} cm from the worktop to the ceiling. The left one stands against the side wall at {n(g.UP_L[0])}–{n(g.UP_L[1])}, a corner post that frames the TV and carries the wrap ledge. The right one is at {n(g.UP_R[0])}–{n(g.UP_R[1])}. That leaves {n(g.TV_GAP)} cm between them, {n(g.TV_CLEAR)} cm clear of the TV each side.</li>
<li><b>TV:</b> centre {n(g.TV_CX)} cm from the side wall (it was 93), on LG's stand set 2 cm off the back wall: bottom {n(g.TV_BOTTOM)}, centre 116.5, top {n(g.TV_TOP)}. The soundbar sits centred under it at the worktop's front edge.</li>
<li><b>The turntable zone:</b> {n(g.RZ_W)} cm between the right upright and the breast. The deck sits on the worktop with {n((g.RZ_W - g.DECK[0]) / 2)} cm each side and its lid opens to about {n(round(g.LID_TOP_OPEN))}. Above it is an oak shelf at {n(g.RZ_SHELF_TOP)}, through-tenoned into the upright, carrying the Series X on its fan stand; the phono preamp hangs underneath at the back.</li>
<li><b>Shelves above:</b> the record ledge at 155.4 between the uprights, four LPs face-out; the high shelf at 196, wall to wall in two lengths, with books, a box, a print, the framed "now playing" 7-inch and Deco B.</li>
<li><b>Power:</b> the side-wall socket in front of bay 1 becomes a double. Its two leads enter through a notch at the left end of the face frame's bottom rail and run back through the plinth to the channel.</li>
</ul>
<figure>{front()}</figure>
<figure>{section()}</figure>

<h3>The fit proof: every item against its published size</h3>
<p>Each zone below lists what goes in it, its size and where that size comes from (numbered sources, section 12), the space, what's left and a verdict. {c[fit.PASS]} of the {nfit} checks fit outright and none fail. {c[fit.TIGHT]} are tight: the deck's 2.65 cm sides, the preamp over the open lid, the dining seats at 55–57 cm each, and the clearances for six and eight. {c[fit.CHECK]} need a check on site: the TV's plugs by the corner post, the RetroTINK's size, the PC case, and the door's swing.</p>
{fit.tables_html()}

<h3>Console sizes, every version</h3>
<p>The bays are sized for the largest version of each console. The model number is on the label underneath; a smaller version just leaves more room.</p>
<table class="tight"><tr><th>Console</th><th>Version</th><th>W × D × H (cm)</th><th>Power</th></tr>
<tr><td>PS1</td><td>Original (largest) · PS one</td><td>27.0 × 18.8 × 6.0 · 19.3 × 14.4 × 3.8</td><td>Built in · external adapter</td></tr>
<tr><td>PS2</td><td>Original (largest) · Slim</td><td>30.2 × 18.3 × 7.8 · 23.1 × 15.2 × 2.8</td><td>Built in · external brick</td></tr>
<tr><td>PS3</td><td>Original (largest) · Slim · Super Slim</td><td>32.5 × 27.4 × 9.8 · 29.0 × 29.0 × 6.5 · 29.0 × 23.0 × 6.0</td><td>Built in</td></tr>
<tr><td>Xbox 360</td><td>Original (largest) · S · E</td><td>30.9 × 25.8 × 8.3 · about 27.0 × 26.4 × 7.5 · 25.4 × 26.4 × 6.7</td><td>External brick</td></tr>
<tr><td>Xbox One</td><td>Original (largest) · S · X</td><td>33.3 × 27.4 × 7.9 · 29.5 × 22.9 × 6.4 · 30.0 × 24.0 × 6.0</td><td>External brick · built in</td></tr>
<tr><td>Xbox Series X</td><td>Standing</td><td>15.1 × 15.1 footprint, 30.1 tall</td><td>Built in</td></tr>
</table>

<h3>The game drawer (bay 1, bottom row)</h3>
<p>Unchanged. Two display bins at the front show covers face-out even with the drawer shut (Xbox left, PS2 right, a small tray between them); behind them the rest of the games stand on edge with the spine on top, so every title faces up when you roll it out.</p>
<figure>{game_drawer()}</figure>
<ul>
<li><b>Box:</b> about 54.3 × 35 cm outside on 350 mm full-extension soft-close runners screwed to the BESTÅ sides; sides 15 cm; 9 mm base lined in felt. About 48 games.</li>
<li><b>Runners:</b> Accuride DZ3832EC (43 kg) or Screwfix Essentials 964VN (40 kg); not IKEA's BESTÅ runners, which aren't full extension.</li>
<li><b>The sub:</b> it now sits on the floor by the side wall; with the drawer pulled right out there's still {n((g.BASE_FRONT_Z - 35.0) - g.SUB_POS["z"][1])} cm between them.</li>
</ul>

<h2 class="pb">4 · The records and the turntable</h2>
<p>The vinyl is back in one place, in the alcove: the deck on the worktop, the records in the two trays right underneath it, the preamp tucked under the shelf above. You can pull a tray, pick a record and play it without crossing the room.</p>
<figure>{drawer()}</figure>
<h3>How the record trays work</h3>
<ul>
<li><b>LP trough:</b> 32.6 cm wide, so a bare 31.4 cm sleeve has 6 mm each side. Records lean back 10° like a record shop browser; the last one leans on a raked oak rest.</li>
<li><b>Singles trough:</b> 18.9 cm wide, the same lean.</li>
<li><b>Capacity:</b> about 90 LPs and 120 singles per tray; two trays, about 180 LPs and 240 singles.</li>
<li><b>Runners:</b> 400 mm full extension, 68–70 kg per pair, screwed straight into bay 3's 18 mm ply sides. A full tray weighs about 32 kg: open one at a time, and fit the anti-tip brackets before loading.</li>
<li><b>Outer sleeves:</b> if most LPs live in thick outer sleeves (up to 32.3 cm), widen the LP trough to 33.4 cm; the singles trough then drops to 18.1, too narrow for face-out singles.</li>
</ul>
<table class="tight"><tr><th>Dimension</th><th>Figure</th><th>How it adds up</th></tr>
<tr><td>Bay 3 carcass</td><td>60 × 40 × 73 outside, 56.4 × 69.4 inside</td><td>18 mm birch ply; back open to the channel</td></tr>
<tr><td>Tray</td><td>53.9 × 40 outside, 52.1 × 38.2 inside</td><td>56.4 − 2 × 1.25 runners; 9 mm sides and ends</td></tr>
<tr><td>Inside layout</td><td>32.6 + 0.6 + 18.9</td><td>LP trough, oak divider, singles trough</td></tr>
<tr><td>Lower tray · upper tray</td><td>Undersides 2.3 · 37.0; sleeves to 34.4 · 69.1</td><td>2.6 and 2.1 cm finger room; top panel at 71.2</td></tr>
</table>
<h3>The turntable zone</h3>
<ul>
<li><b>The deck:</b> on isolation feet, 2 cm back from the worktop's front edge, with {n(g.ALC_D - g.DECK_Z[1])} cm behind it for the lid's hinges. The zone takes a deck up to the size of an AT-LP120X (45.2 × 35.2 cm); most decks are smaller.</li>
<li><b>The lid:</b> AT's cover is 44.1 × 34.6 cm<sup>{fit.ORDER.index("lid") + 1}</sup>, so standing open its top edge is at about {n(round(g.LID_TOP_OPEN))}; the shelf's underside is at {n(g.LID_CLEAR_TO)}.</li>
<li><b>Bass:</b> the sub is on the floor by the side wall, a separate piece of furniture from the deck; isolation feet under the deck take care of the rest.</li>
<li><b>Signal path:</b> turntable set to PHONO → the preamp under the shelf → a 2 m RCA-to-3.5 mm lead down the groove behind the right upright and along the back of the worktop to the soundbar's AUX. If the deck has no PHONO/LINE switch, plug it straight into the AUX.</li>
<li><b>Soundbar:</b> Music mode, bass up, surround, night and dialogue modes off. Always the AUX cable, never Bluetooth.</li>
</ul>
<h3>Where every record lives</h3>
<table class="tight"><tr><th>Where</th><th>What</th><th>How many</th></tr>
<tr><td>Bay 3, upper and lower trays</td><td>LPs and singles, face-out</td><td>About 180 LPs + 240 singles</td></tr>
<tr><td>Above the TV</td><td>Oak record ledge, the "now playing" wall</td><td>4 LPs</td></tr>
<tr><td>Side wall</td><td>The ledge wrapped round the corner</td><td>4 LPs</td></tr>
<tr><td>High shelf, right</td><td>A framed 7-inch</td><td>1</td></tr>
<tr class="total"><td>Total</td><td></td><td>About {LPS} LPs and {SINGLES} singles, every one face-out</td></tr>
</table>
<p>That's fewer than v10's cabinet held (it had a 50-LP browser and a singles drawer). If the collection is bigger than this, tell me the counts. The neatest overflow is a matching face-out tray unit under the window at the end of the sofa.</p>

<h2 class="pb">5 · The dining wall</h2>
<p>The chimney breast becomes the dining wall. A solid oak table, {n(g.TABLE[0])} × {n(g.TABLE[1])} cm, hangs on lift-off hinges on an oak backboard. Every day it stands folded flat against the breast, about {n(g.FOLDED_D)} cm deep. Down, it's a table for four at the same 76 cm as the alcove's worktop. Lifted off onto four legs, it seats six in the room, or eight with a matching leaf.</p>
<figure class="render">{img("render_v11_dining_four.png", "The dining wall down and set for four")}
<figcaption>Down and set for four: two on the room side, one at each end. The second spot bar lights the table and the framed LPs above it.</figcaption></figure>
<figure>{dining_section()}</figure>
<h3>How it works</h3>
<ul>
<li><b>Backboard:</b> oak, {n(g.RAIL[0])} × {n(g.RAIL[1])} × {n(g.RAIL[2])}, from the worktop's offcut, screwed to the breast with plugs every 20 cm, top at {n(g.RAIL_TOP)}.</li>
<li><b>Brackets:</b> two Häfele Hebgo heavy-duty folding brackets (287.43.428: 580 mm arm, 500 kg a pair<sup>{fit.ORDER.index("hebgo") + 1}</sup>), {n(g.HEBGO_X[1] - g.HEBGO_X[0])} cm apart on the backboard's face. Raised, they lock on their own; a light lift on the arm releases them, and they fold flat down the breast.</li>
<li><b>Hinges:</b> three 100 mm lift-off hinges<sup>{fit.ORDER.index("liftoff") + 1}</sup>, all the same hand, along the backboard's top edge. Slide the table 5 cm sideways and it comes off.</li>
<li><b>Folded:</b> two oak turn buttons on the breast hold the top edge at {n(g.FOLDED_TOP)}. The underside faces the room, so it's oiled like the top; the four leg plates show as small dark discs.</li>
<li><b>For six or eight:</b> lift it off (two people, about 18 kg), screw four Emuca 710 mm legs<sup>{fit.ORDER.index("legs") + 1}</sup> into the plates (each adjusts to 730), and stand it in the room. For eight, butt the 60 × 80 leaf, on its own four legs, against one end, joined by two alignment dowels and two table clips.</li>
<li><b>Chairs:</b> drawn at IKEA TERJE size (43 × 49, seat 48<sup>{fit.ORDER.index("terje") + 1}</sup>), which folds flat. Any dining chair with a 45–48 cm seat works.</li>
</ul>
<figure>{seating()}</figure>
<table class="tight"><tr><th>Seats</th><th>Where the table stands</th><th>Per diner</th><th>Clearances</th></tr>
<tr><td>Four</td><td>Down at the wall, on its brackets</td><td>55 on the room side (60 is ideal); the ends are 80 wide</td><td>{n(g.TABLE_Z[1] - g.SOFA_FRONT_Z)} to the sofa: room to walk behind</td></tr>
<tr><td>Six</td><td>Lifted off, centred at about {n((g.SIX_X[0] + g.SIX_X[1]) / 2)} from the side wall, 60 off the breast</td><td>55, two a side</td><td>60 to the breast (the tight minimum), {n(g.FREE_Z[1] - g.WINDOW_Z)} to the window, {n(g.ROOM_W - g.SIX_X[1])} to the west wall</td></tr>
<tr><td>Eight</td><td>Plus the leaf: 170 × 80</td><td>57, three a side</td><td>{n(g.ROOM_W - g.EIGHT_X[1])} to the west wall, {n(g.FREE_Z[1] - g.SOFA_FRONT_Z)} to the sofa at the east end: tight but fine for a dinner</td></tr>
</table>
<p>Clearances from a UK planning guide: 60 cm of table edge per diner, 60 cm from the table to a wall as a tight minimum, 75 to aim for, 100–110 to walk behind someone seated<sup>{fit.ORDER.index("dining") + 1}</sup>. For six or eight, slide the coffee table to the window first, and keep the door to the hall shut while you eat if it opens into the room: the chairs on that side sit in its swing.</p>
<h3>Cut list and hardware</h3>
<table class="tight"><tr><th>Part</th><th>Material</th><th>Size (cm)</th><th>Qty</th></tr>
<tr><td>Table top · leaf</td><td>Solid oak, edge-glued staves</td><td>110 × 80 × 2.7 · 60 × 80 × 2.7</td><td>1 · 1</td></tr>
<tr><td>Backboard</td><td>Solid oak, from the worktop offcut</td><td>110 × 22 × 3</td><td>1</td></tr>
<tr><td>Turn buttons</td><td>Oak offcut</td><td>6 × 2.5 × 2.2, on a single screw</td><td>2</td></tr>
<tr><td>Folding brackets</td><td>Häfele Hebgo 287.43.428</td><td>arm 58, height 22</td><td>2</td></tr>
<tr><td>Lift-off hinges</td><td>Union PowerLoad, 100 × 88</td><td>one 3-pack, same hand</td><td>3</td></tr>
<tr><td>Legs</td><td>Emuca Ø60 steel, 710–730 mm, with plates</td><td>—</td><td>8</td></tr>
<tr><td>Leaf joint</td><td>Alignment dowels, table clips</td><td>—</td><td>2 + 2</td></tr>
</table>
<p class="note">Safety: never fold it up with anything on it, keep both turn buttons turned when it's up, and check the brackets have locked (a click each side) before you load it.</p>

<h2 class="pb">6 · The side wall</h2>
<p>One oak line at {n(g.LEDGE_TOP)} cm runs from the ledge over the TV, round the corner on the left upright, and along the side wall: first a 7 cm record ledge with four more LPs face-out, then an oak shelf for the PC over the end of the sofa. It ties the alcove to the rest of the room and moves the PC out of the TV's sightlines.</p>
<figure>{pc_shelf()}</figure>
<ul>
<li><b>Wrap ledge:</b> 134 × 7 × 2.4 cm with a 1.5 cm lip, on an oak cleat screwed to the side wall, butt-jointed to the left upright's front edge on two 10 mm dowels.</li>
<li><b>PC shelf:</b> {n(g.PC_SHELF_Z[0] - g.PC_SHELF_Z[1])} × {n(g.PC_SHELF_D)} × 4 cm, on an oak cleat with two concealed heavy-duty brackets (40 kg+ a pair), {n(g.PC_SHELF_TOP - g.PC_SHELF_T - g.SOFA_H)} cm above the sofa's back. The case sits with its glass to the room and its front towards the alcove. The ports face the window behind an oak frame with a woven cane panel, open at the top for the exhaust. The pad dock sits beyond the screen.</li>
<li><b>Cables:</b> through a notch at the shelf's back corner, down slim trunking painted Card Room Green, along the skirting behind the sofa and into the plinth. The HDMI is an active optical cable (about 5 m), "source" end at the PC.</li>
<li><b>Power:</b> a new double socket low on the side wall behind the sofa (electrician) takes the PC and the rear speakers, so the PC's 500–850 W stays off the media wall's strips.</li>
<li><b>Keyboard and mouse:</b> no tray over the sofa; a wireless set on a lap board lives on the shelf or in the plinth drawer.</li>
<li><b>Headroom:</b> the shelf's underside is at {n(g.PC_SHELF_TOP - g.PC_SHELF_T)}, and it covers only the 28 cm of the sofa nearest the wall.</li>
<li><b>Sub:</b> on its riser on the floor by the side wall, between the base and the sofa, firing across the room, 10 cm off the wall for its rear port.</li>
</ul>

<h2 class="pb">7 · The oak joinery</h2>
<p>Above the worktop the wall is furniture rather than cladding: two solid oak uprights, shelves carried on joints you can see, and the Card Room Green wall showing between them.</p>
<ul>
<li><b>Uprights:</b> solid oak, 4.5 × 30 cm, {n(g.UPRIGHT_LEN)} cm long, each on two 10 mm dowels into the worktop, scribed to the ceiling and held to the back wall with concealed brackets; the left one also screws to the side wall.</li>
<li><b>Wedged through-tenons:</b> the Series X shelf (top {n(g.RZ_SHELF_TOP)}) passes through the right upright on two tenons, 6 cm wide and 2.4 thick, 12 and 20 cm from the wall. They're wedged and planed flush: standing proud, they'd touch the TV.</li>
<li><b>Housed and pegged:</b> the high shelf (two lengths, top 196) and the record ledge (top 155.4) are housed 1.2 cm into the uprights and pinned with 10 mm oak pegs, which show as dark dots.</li>
<li><b>LED grooves:</b> a routed groove on each upright's inner face holds a 2700K strip that washes the wall either side of the TV.</li>
<li><b>Hidden cables:</b> a 2 × 1.5 cm groove down the back of the right upright carries Deco B's 12 V lead and patch lead, the Series X's HDMI and power, and the vinyl lead.</li>
<li><b>Finish:</b> hardwax oil throughout; lightly limed or smoked oak avoids the bright orange "new oak" look.</li>
</ul>
<figure>{joints()}</figure>
<h3>Joinery cut list</h3>
<table class="tight"><tr><th>Part</th><th>Material</th><th>Finished size (cm)</th><th>Joints</th><th>Qty</th></tr>
<tr><td>Uprights</td><td>Solid oak, quarter-sawn if you can</td><td>{n(g.UPRIGHT_LEN)} × 30 × 4.5 (buy 165 and scribe)</td><td>Housings for the high shelf and ledge; mortises for the Series X shelf in the right one; LED groove inside; cable groove at the back of the right one</td><td>2</td></tr>
<tr><td>High shelf</td><td>Solid oak</td><td>128.9 × 30 × 4 and 51.7 × 30 × 4</td><td>Housed 1.2 into the uprights, pegged; the short length on a cleat on the reveal</td><td>2</td></tr>
<tr><td>Record ledge · wrap ledge</td><td>Solid oak</td><td>128.9 × 7 × 2.4 · 134 × 7 × 2.4; lips 0.9 × 1.5</td><td>Housed and pegged · cleat and two dowels</td><td>1 · 1</td></tr>
<tr><td>Series X shelf</td><td>Solid oak</td><td>55 × 30 × 4 ({n(g.RZ_W)} + 4.5 through)</td><td>Two through-tenons 6 × 2.4, wedged flush; cleat on the reveal</td><td>1</td></tr>
<tr><td>PC shelf</td><td>Solid oak</td><td>{n(g.PC_SHELF_Z[0] - g.PC_SHELF_Z[1])} × {n(g.PC_SHELF_D)} × 4</td><td>Oak cleat and two concealed brackets</td><td>1</td></tr>
<tr><td>Worktop and backboard</td><td>One solid oak worktop, 300 × 62</td><td>{n(g.ALC_W)} × {n(g.BASE_D)} × 3 and 110 × 22 × 3</td><td>Chamfered fronts; cut edges sealed</td><td>1 board</td></tr>
<tr><td>Face frame</td><td>Oak, 20 mm</td><td>186 × 73, stiles about 5 wide</td><td>Glued and pinned; end stiles scribed</td><td>1 set</td></tr>
<tr><td>Wedges · pegs · dowels</td><td>Oak · 10 mm oak dowel</td><td>6 × 3, tapering · 5 long</td><td>Glued</td><td>2 + spares · 6 · 8</td></tr>
<tr><td>PC screen</td><td>Oak frame 2 × 3, pre-woven cane</td><td>26 × 48</td><td>Cane in a groove with a spline</td><td>1</td></tr>
</table>

<h2 class="pb">8 · Paint and light</h2>
<h3>Paint: Farrow &amp; Ball Card Room Green No. 79</h3>
<p>The room is colour-drenched in Card Room Green: walls, ceiling, alcove, chimney breast, skirting, door and frame, radiator and the trunking. It's a soft grey-green that lets the oak and the records lead.</p>
<figure>{img("paint_grid.png", "The artisan oak render in four greens")}
<figcaption>The v11 wall in Card Room Green (chosen) beside Sage Green, Treron and the earlier deep green. Screen colours are approximate and the renders are lit as in the evening: judge from painted samples.</figcaption></figure>
<ul>
<li><b>Finishes:</b> Estate or Modern Emulsion on walls, ceiling, alcove and breast; Estate Eggshell in the same colour on skirting, door, frame, radiator and trunking (Modern Eggshell if the skirting takes knocks).</li>
<li><b>Order:</b> paint before anything is fixed, so nothing needs cutting in round the uprights, shelves or the dining wall.</li>
</ul>
<h3>Skirting: Card Room Green too</h3>
<figure>{img("skirting_options.png", "Three skirting options")}</figure>
<p>Recommended: Card Room Green in Estate Eggshell, which completes the drench and hides scuffs far better than white. Darker option: Green Smoke. Over the white gloss: wash, key, woodwork primer, two coats of eggshell.</p>
<h3>Light, in three warm layers</h3>
<ul>
<li><b>The LED strip on the ceiling</b> (as now): round the room's edge, into the alcove and across the breast; 2700K on a dimmer.</li>
<li><b>Built into the oak:</b> a 2700K strip in each upright's groove, on a driver on the fused spur; a 6500K bias light on the back of the TV from its USB port.</li>
<li><b>Two spot bars</b> in the style of Dunelm's Wolston (£49 each; 84 × 16 cm, 22.4 cm drop; 4 × E14, 6 W max<sup>{fit.ORDER.index("wolston") + 1}</sup>), parallel to the media wall. One hangs on the existing rose; the second hangs on a new ceiling point by the stairs, over the dining area. A two-gang LED dimmer by the door runs them separately.</li>
</ul>
<table class="tight"><tr><th>Head</th><th>Bar 1, on the existing rose</th><th>Bar 2, over the dining area</th></tr>
<tr><td>Sage</td><td>The books and the left of the high shelf</td><td>The framed LPs above the table</td></tr>
<tr><td>Pale blue</td><td>The record ledge above the TV</td><td>The table (the folded top, when it's up)</td></tr>
<tr><td>Mustard</td><td>Down onto the coffee table</td><td>The table</td></tr>
<tr><td>Dusty pink</td><td>The turntable and the Series X</td><td>The door and the stairs</td></tr>
</table>
<p>Never point a head at the TV. For six or eight, swing bar 2's blue and mustard heads onto the table where it stands. Use warm-white (2700K) dimmable E14 LED bulbs throughout.</p>

<h2 class="pb">9 · Power, cables and network</h2>
<h3>Power</h3>
<figure>{power()}</figure>
<ul>
<li><b>The socket:</b> the single on the side wall just in front of bay 1, about 30 cm up, becomes a double at the same spot. The left outlet feeds the 10-gang; the right one feeds the retro 6-way, so its own switch is now the retro switch. The 10-gang's switches sit behind the TV, 2 cm from the corner post, where you can't reach them any more.</li>
<li><b>10-gang:</b> lying flat on the worktop behind the TV, both sides left on: TV, soundbar, sub, Series X, USB charger, Deco B, Switch 2, the deck and the preamp.</li>
<li><b>Retro 6-way:</b> in the channel behind bay 2: Xbox One, Xbox 360, PS3, PS2, PS1, RetroTINK.</li>
<li><b>OLED care:</b> leave the TV in standby so it runs its pixel refresh.</li>
</ul>
<h3>Cable routes</h3>
<figure>{routes()}</figure>
<ul>
<li><b>The channel:</b> 4 cm behind the frames, flat two-compartment trunking: mains on one side, HDMI, Cat6 and audio on the other. Switch 2 and the retro 6-way stand on edge in it.</li>
<li><b>The groove behind the right upright:</b> Deco B's 12 V and patch leads, the Series X's HDMI and power, and the vinyl lead, down to the worktop's slot.</li>
<li><b>The PC:</b> down the trunking at the far end of its shelf, along the skirting behind the sofa and into the plinth notch.</li>
<li><b>The sub:</b> its mains lead from the 10-gang runs down the slot, along the channel and out at the plinth notch, along the skirting to the sub.</li>
<li><b>Airflow:</b> console bays stay open-backed; the Series X has 15 cm each side and 21 above.</li>
</ul>
<h3>Network</h3>
<figure>{network()}</figure>
<ul>
<li><b>Bedroom 3:</b> the Hub 5 (in modem mode), Deco A and Switch 1 sit together with the gaming PCs. Switch 1's eight ports: the uplink, two PCs, the two Cat6 runs down to Deco B and Deco C, and, if you want them, the projector in the master and the music room in bedroom 2.</li>
<li><b>The route down:</b> across the landing to the airing cupboard, which sits over the alcove's corner, and down through its floor. Run 1 comes through the living room ceiling in the alcove's right corner to Deco B; run 2 follows the right upright's groove down and through the floor to the kitchen, where Deco C goes on the outside of the brick cupboard, up high.</li>
<li><b>Sloped ceilings:</b> bedroom 2 and the bathroom slope down to the back wall; keep any Deco or desk in bedroom 2 on the high side.</li>
</ul>
<p><b>Stage 1, mesh up today:</b> unplug everything from the hub, log in at 192.168.0.1 and turn on Modem Mode (its page then moves to 192.168.100.1); set up Deco A with the old Wi-Fi name and password; Switch 1 into Deco A's other port and the PCs into Switch 1; add Deco B and Deco C over Wi-Fi for now; check the Xbox shows NAT: Open.</p>
<p><b>Stage 2, after the cables:</b> plug each Cat6 run into its Deco, confirm Deco B and C show as "Ethernet" in the app, and give the Series X and PC high priority under QoS.</p>
<div class="callout"><b>Cabling rules</b><ul>
<li>Solid pure-copper Cat6, round; not CCA or flat cable for the long runs. Measure the real route and add 2–3 m.</li>
<li>Cross mains at right angles; never staple through a cable; no kinks; label both ends. Never two cables between the same two devices.</li>
<li><b>Done when:</b> Deco B and C show "Ethernet", each PC shows 1.0 Gbps, the Xbox shows NAT: Open, and phones hold a strong signal in the kitchen and across the living room.</li></ul></div>
<h3>AV: everything sounds through the Hisense</h3>
<figure>{av()}</figure>
<table class="tight"><tr><th>Source</th><th>Picture</th><th>Sound</th></tr>
<tr><td>PC · Xbox Series X</td><td>TV HDMI 1 · HDMI 3</td><td>Via the TV over eARC (5.1 or Atmos)</td></tr>
<tr><td>Xbox One, Xbox 360, PS3</td><td>HDMI switch → TV HDMI 4</td><td>Via the TV over eARC, 5.1</td></tr>
<tr><td>PS2</td><td>Component → RetroTINK → switch → TV</td><td>Optical straight to the soundbar</td></tr>
<tr><td>PS1</td><td>RGB SCART → RetroTINK → switch → TV</td><td>Stereo through the RetroTINK and eARC</td></tr>
<tr><td>Turntable · phone</td><td>—</td><td>Preamp → AUX · Bluetooth</td></tr>
</table>
<p>TV settings: rename the inputs (HDMI 4 "Retro"), Deep Colour on HDMI 1, 3 and 4, Game Optimiser on the console inputs, sound out to HDMI eARC. RetroTINK-6X CE: a 5 V 2 A USB plug on the retro 6-way; the PS2's Component Video Out set to Y Cb/Pb Cr/Pr; RGB SCART for the PS1.</p>
<h3>Sound layout</h3>
<figure>{sound()}</figure>
<ul>
<li><b>Sub:</b> wireless, on its riser on the floor by the side wall, firing across the room; turn it down rather than moving it if the bass booms.</li>
<li><b>Rears:</b> one on the side wall at seated ear height behind the sofa's corner, one on a stand past the sofa's west end; linked by a cable behind the sofa, powered from the new socket.</li>
</ul>

<h2 class="pb">10 · Build guide, for a first-time builder</h2>
{guide_html()}

<h2 class="pb">11 · Buy list and tracker</h2>
<p>Every purchase and job, in build order, comes to about £{money(tl, th)} plus the electrician's quote. Estimates are approximate UK prices; changed and new items are marked. Tick items off and write in what you paid.</p>
<table class="tight"><tr><th>Phase</th><th>Estimate (£)</th><th>Biggest item</th></tr>{ptot}</table>
<p class="note">Already owned: Virgin Hub 5, three Deco X1500s, two TL-SG105S switches (both become spares), LG OLED C6 55" and its stand, a 10-gang, the Hisense AX5100G 5.1 soundbar, the Series X fan stand, the turntable, the L-sofa and all the consoles.</p>
<table class="tracker"><thead><tr><th>Status</th><th>Item</th><th>Qty</th><th>Estimate (£)</th><th>Paid (£)</th></tr></thead><tbody>
{tracker_rows()}</tbody></table>

<h2 class="pb">12 · Still to confirm, later ideas, sources</h2>
<h3>Still to confirm</h3>
<ul class="checks">
<li>The L-sofa's size (the plan uses {n(g.SOFA_W)} × {n(g.SOFA_D)} × {n(g.SOFA_H)} high) and which way its return points.</li>
<li>The door to the hall: which side it hinges, and whether it opens into the room (the dining chairs on that side sit in its swing).</li>
<li>The west end's sizes: which of 935, 1045, 660 and 820 are the recess, the door and the stair box.</li>
<li>The turntable's model (the zone takes up to 45.2 × 35.2 cm) and whether it has a PHONO/LINE switch.</li>
<li>The PC case's model (the shelf allows {n(g.PC_CASE[0])} × {n(g.PC_CASE[2])} × {n(g.PC_CASE[1])} tall) and that its window is on the left.</li>
<li>The Series X fan stand's model: the shelf takes a footprint up to about 30 cm wide.</li>
<li>Dining chairs: use ones you have (seat 45–48), or four folding ones? And where the leaf and the legs live (the garage?).</li>
<li>The side wall and the chimney breast: solid, or plasterboard? The ledge, PC shelf and dining wall all fix to them.</li>
<li>The 23 × 22 cm box in the window's west corner.</li>
<li>Records: roughly how many LPs and singles (the wall holds about {LPS} and {SINGLES}), and are most in thick outer sleeves?</li>
<li>Wired ports for the projector (master) and the music room (bedroom 2)?</li>
<li class="done">The TV {n(g.TV_SHIFT)} cm nearer the side wall, the turntable in the alcove, the Series X above it, the records below.</li>
<li class="done">A fold-down oak dining table on the chimney breast; a second spot bar by the stairs.</li>
<li class="done">The ledge wrapping round onto the side wall, with the PC above the sofa.</li>
<li class="done">Artisan oak, Card Room Green with matching eggshell skirting, every record face-out, the game drawer as designed.</li>
</ul>
<h3>Later ideas</h3>
<ul>
<li><b>Dave and Emma's watch log:</b> a shared film and TV log, like a Spotify Blend for what you watch: log each film or episode, mark whether you watched it together, rate it, and later get suggestions for what to watch next. To be shaped up separately.</li>
</ul>
<h3>Sources</h3>
<p class="note">Numbered sources are the item sizes used in the fit proof (section 3).</p>
{fit.sources_html(OTHER_SOURCES)}

<h2 class="pb">Appendix · The slat wall alternative</h2>
<p>Kept for reference, drawn to the v11 layout. The base, the records, the consoles, the side wall and the dining wall are identical. Above the worktop, oak slat panels on battens run from the worktop to the ceiling instead of the uprights; the shelves sit on hidden cleats and the light comes from strips under each shelf. Quicker to fit, but it loses the record ledge over the TV and the joints on show.</p>
<figure class="render small">{img("render_v11_slat_clean.png", "Slat wall alternative")}</figure>
<h3>Options we rejected along the way</h3>
<table class="tight"><tr><th>Option</th><th>Why not</th></tr>
<tr><td>The vinyl cabinet on the chimney breast (v10)</td><td>The breast is the only clear wall for a table; the turntable fits in the alcove now</td></tr>
<tr><td>A keyboard tray under the PC shelf</td><td>The shelf is over the sofa; a wireless set on a lap board instead</td></tr>
<tr><td>Hub as router, Decos as access points</td><td>Loses HomeShield and parental controls</td></tr>
<tr><td>All-wireless mesh · powerline</td><td>Speed drops at each hop · slower and less stable than Cat6</td></tr>
<tr><td>Records spine-up in one drawer</td><td>Showed only a handful of covers; face-out trays show every one</td></tr>
<tr><td>A green feature wall only · white skirting</td><td>The drench ties the room together; white cuts a bright line round it</td></tr>
<tr><td>Bluetooth from the turntable</td><td>Compresses the sound; the AUX lead keeps full quality</td></tr>
</table>
</body></html>"""
    (HERE / "plan.html").write_text(html)
    guide = f"""<!doctype html><html><head><meta charset="utf-8"><title>Build Guide</title><style>{css}</style></head><body>
<h1>Media Wall &amp; Dining Wall: Build Guide</h1>
<p class="byline">Version {VERSION} · Oct 18, 2026 · for Emma and Dave · sizes in cm; the full plan has the drawings and the fit proof</p>
<figure class="render small">{img("render_v11_join_clean.png", "The finished wall")}</figure>
{guide_html()}
<h2 class="pb">Shopping list</h2>
<p>About £{money(tl, th)} plus the electrician, in build order.</p>
<table class="tracker"><thead><tr><th>Status</th><th>Item</th><th>Qty</th><th>Estimate (£)</th><th>Paid (£)</th></tr></thead><tbody>
{tracker_rows()}</tbody></table>
</body></html>"""
    (HERE / "guide.html").write_text(guide)
    print("totals", tl, th, "fit", c)


def pdf():
    from playwright.sync_api import sync_playwright
    from shot import _launch
    def footer(name):
        return ('<div style="width:100%;font-family:Inter,sans-serif;font-size:8px;color:#8a867e;padding:0 18mm;'
                f'display:flex;justify-content:space-between"><span>{name} · v{VERSION}</span>'
                '<span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>')
    with sync_playwright() as p:
        b = _launch(p)
        for src, out, name in (("plan.html", PDF_NAME, "Home Network &amp; Media Wall Plan"), ("guide.html", GUIDE_NAME, "Build Guide")):
            pg = b.new_page()
            pg.goto((HERE / src).resolve().as_uri())
            pg.wait_for_timeout(500)
            pg.pdf(path=str(HERE.parent / "out" / out), format="A4", print_background=True,
                   margin={"top": "16mm", "bottom": "18mm", "left": "18mm", "right": "18mm"},
                   display_header_footer=True, header_template="<div></div>", footer_template=footer(name))
            pg.close()
        b.close()


if __name__ == "__main__":
    build()
    pdf()
    print("pdf ok")
