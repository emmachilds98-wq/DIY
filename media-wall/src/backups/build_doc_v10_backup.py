"""Builds the plan (v10) as HTML, then PDF via headless Chromium.
The plan reads in build order: decision, room, wall and fit proof, vinyl corner, joinery, paint and light,
power and network, build guide, buy list, then what's left to confirm. Numbers come from geometry.py and fit.py."""
import base64, pathlib
import geometry as G
import fit
from diagrams import network, front, drawer, sound, game_drawer, av, power, routes, pc_shelf, section, joints, house, living_plan, why_layout

HERE = pathlib.Path(__file__).parent
VERSION = "10"
PDF_NAME = f"Home_Network_Plan_v{VERSION}.pdf"


def img(name, alt=""):
    p = HERE / name
    mime = "jpeg" if p.suffix.lower() in (".jpg", ".jpeg") else "png"
    return f'<img src="data:image/{mime};base64,{base64.b64encode(p.read_bytes()).decode()}" alt="{alt}">'


def n(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


LPS = 2 * G.TRAY_LPS + G.BROWSER_LPS + G.LEDGE_LPS          # 234
SINGLES = 2 * G.TRAY_SINGLES + G.BAYB_SINGLES               # 350

# ---------------------------------------------------------------- buy list and jobs, in build order
# (status, item, phase, qty, lo, hi)  lo/hi None = no cost
TRACK = [
    ("To do", "Put the Virgin Hub 5 into modem mode", "1 Network, now", "", None, None),
    ("To do", "Set up Deco A, Switch 1 and the PCs in bedroom 3", "1 Network, now", "", None, None),
    ("To do", "Add Deco B and Deco C over Wi-Fi for now; speed-test each room and the Xbox", "1 Network, now", "", None, None),
    ("To buy", "Cat6 patch leads, 0.5–2 m", "1 Network, now", "11", 15, 20),
    ("To buy", "TP-Link TL-SG108 8-port switch: one for the living room, one to replace the 5-port in bedroom 3", "1 Network, now", "2", 36, 50),
    ("To do", "Book one electrician visit: Cat6 from bedroom 3 across the landing and down through the airing cupboard, one run to the alcove's right corner (Deco B) and one on to the kitchen (Deco C), a spare pulled with each; if you want them, runs to the master (projector) and bedroom 2 (music room); swap the single socket on the side wall in front of bay 1 for a double (or move it into the alcove behind bay 1); a socket by the sofa for the rear speakers if there isn't one; a socket under the PC shelf; a fused spur for the LED drivers; fit the spotlight bar and an LED-compatible dimmer <b>(changed: route from bedroom 3, optional runs)</b>", "2 Electrician and cabling", "", None, None),
    ("To buy", "Cat6 solid pure copper, round (not CCA): two runs, four with the optional ones", "2 Electrician and cabling", "2–4 runs", 30, 60),
    ("To buy", "6-way surge-protected extension with a switch per socket: Deco B, Switch 2, turntable, preamp, RetroTINK", "2 Electrician and cabling", "1", 25, 40),
    ("To buy", "4-port USB charger, 5 V 2 A per port (HDMI switch, Xbox fan stand, pad dock)", "2 Electrician and cabling", "1", 10, 20),
    ("To buy", "USB plug, 5 V 2 A or more, for the RetroTINK on the switched strip", "2 Electrician and cabling", "1", 5, 10),
    ("To buy", "Cable kit: brush grommets, velcro ties, labels", "2 Electrician and cabling", "1", 20, 30),
    ("To buy", "Flat two-compartment trunking for the 4 cm channel behind the base, about 2 m <b>(changed: flat)</b>", "2 Electrician and cabling", "1", 10, 20),
    ("To buy", "Slim paintable trunking for the PC drop and the skirting run, about 2.5 m", "2 Electrician and cabling", "1", 15, 30),
    ("To buy", "DC extension lead for the Deco adapter, only if its lead won't reach the 6-way in bay 3 (match the plug)", "2 Electrician and cabling", "1", 5, 10),
    ("To buy", "PC tidy kit: braided sleeve, right-angle C13 lead, shelf-notch grommet", "2 Electrician and cabling", "1", 10, 20),
    ("To do", "Sample Farrow & Ball Card Room Green No. 79 on an A4 board; check it by day and with the LED strip on", "3 Paint", "", None, None),
    ("To buy", "Card Room Green: Estate (or Modern) Emulsion for walls, ceiling, alcove and chimney breast; Estate Eggshell for skirting, door, frame and trunking; primer and undercoat", "3 Paint", "", 200, 500),
    ("To buy", "Woodwork primer, sanding pads and sugar soap for the white skirting and door", "3 Paint", "1", 20, 40),
    ("To do", "Paint the whole room before anything is fixed: alcove and breast included; skirting and door from white to eggshell", "3 Paint", "", None, None),
    ("Done", "Check the alcove back wall for fixings (solid)", "4 Base unit", "", None, None),
    ("To do", "Measure the alcove's width at the floor, 76, 156, 196 and the ceiling, and the floor's level across it <b>(new)</b>", "4 Base unit", "", None, None),
    ("To do", "Check the side wall where the PC shelf goes: solid, or plasterboard on studs", "4 Base unit", "", None, None),
    ("To buy", "Two IKEA BESTÅ 60×40×64 frames, white stained oak effect, for bays 1–2", "4 Base unit", "2", 70, 200),
    ("To buy", "Plinth for bays 1–2: 18 mm ply ladder frame 120 × 38 × 9 cm, plus shims", "4 Base unit", "1", 15, 30),
    ("To buy", "Bay 3 carcass for the sub: 18 mm birch ply, 60 × 40 × 73 cm from the floor, a shelf, connector bolts <b>(changed: holds the sub now)</b>", "4 Base unit", "1", 50, 90),
    ("To buy", "BESTÅ shelves, 56 × 36 cm (20 kg max each), two each for bays 1 and 2", "4 Base unit", "4", 12, 32),
    ("To buy", "Anti-tip brackets and 4 cm spacer blocks: both frames, bay 3 and the vinyl cabinet <b>(changed)</b>", "4 Base unit", "1 set", 20, 30),
    ("To do", "Measure about ten games of each kind (PS2, Xbox 360, Xbox One) before cutting the game drawer", "4 Base unit", "", None, None),
    ("To buy", "Game drawer kit: 12 mm birch ply cut to size, 350 mm full-extension soft-close runners (35–49 kg), oak lip, follower block, felt", "4 Base unit", "1", 50, 90),
    ("To buy", "Hidden slim drawer for bay 3: oak front 56.4 × 7.4 cm, 12 mm ply box 52 × 30 × 6 cm, 300 mm runners <b>(changed: wider)</b>", "4 Base unit", "1", 30, 50),
    ("To buy", "Compact isolation riser for the sub, about 30 × 35 cm, 4–6 cm tall", "4 Base unit", "1", 20, 40),
    ("To buy", "PC shelf box: 27 mm oak top 65 × 32, 18 mm oak sides, keyboard tray on 300 mm runners, French cleat, two steel brackets rated 25 kg+", "4 Base unit", "1", 55, 120),
    ("To do", "Build the plinth and bay 3, fix everything to the wall, fit the shelves and drawers; place the TV, soundbar, Series X and sub", "4 Base unit", "", None, None),
    ("To buy", "Two solid oak uprights, 165 × 30 × 4.5 cm (cut to 159), quarter-sawn if possible <b>(changed: longer)</b>", "5 Oak joinery", "2", 150, 300),
    ("To buy", "Solid oak for the shelves: high shelf in three lengths (26.45, 128.9, 26.45 × 30 × 4), two side shelves 31.75 × 25 × 4, record ledge 128.9 × 7 × 2.4 <b>(changed: no turntable shelf)</b>", "5 Oak joinery", "1 set", 170, 300),
    ("To buy", "Oak wedges, 10 mm oak dowel for pegs and dowels, concealed upright brackets", "5 Oak joinery", "1", 15, 30),
    ("To buy", "One solid oak worktop, 300 × 62 cm, full stave: cut into the alcove top (186 × 46) and the cabinet top (100 × 44), chamfered fronts; offcuts for lips and the browser's rail <b>(changed)</b>", "5 Oak joinery", "1", 250, 450),
    ("To buy", "Oak face frames, 20 mm: 186 cm for the base, 100 cm for the vinyl cabinet <b>(changed)</b>", "5 Oak joinery", "1", 100, 200),
    ("To buy", "Cane screen for the PC: oak frame and pre-woven cane, 26 × 48 cm", "5 Oak joinery", "1", 20, 40),
    ("To do", "Cut the joints and fit the uprights, shelves, ledge and face frame; notch the uprights for the ceiling strip", "5 Oak joinery", "", None, None),
    ("To buy", "Vinyl cabinet carcass: 18 mm birch ply for bay A (60 × 40 × 73) and bay B (40 × 40 × 73) with a shared middle side, bay B's shelf, connector bolts; oak-veneered end panel for the side you see <b>(new)</b>", "6 Vinyl cabinet", "1", 90, 160),
    ("To buy", "Two face-out record tray kits: 12 and 9 mm birch ply cut to size, 6 mm oak dividers, 15 mm oak lips, raked rests, felt, two pairs of 400 mm runners rated 68–70 kg", "6 Vinyl cabinet", "2", 150, 240),
    ("To buy", "Singles drawer for bay B: ply box 33.9 × 40 × 13, oak divider and lip, 400 mm runners rated 45 kg+ <b>(new)</b>", "6 Vinyl cabinet", "1", 40, 70),
    ("To buy", "LP browser for the cabinet top: 18 mm oak base 44 × 24, low front rail and one side", "6 Vinyl cabinet", "1", 15, 35),
    ("To buy", "Isolation feet for the turntable", "6 Vinyl cabinet", "1", 10, 25),
    ("To buy", "Two LP frames for the chimney breast, hung from 150 cm <b>(new)</b>", "6 Vinyl cabinet", "2", 20, 40),
    ("To do", "Build the cabinet, check the door clears it, fix it to the breast with anti-tip brackets, fit the trays and the singles drawer", "6 Vinyl cabinet", "", None, None),
    ("To buy", "LED for the upright grooves: 2700K strip, two aluminium channels, driver; 6500K bias light for the TV", "7 Lighting", "1", 40, 90),
    ("To buy", "Ceiling light: Dunelm Elements Wolston 4-light spotlight bar (£49), plus four warm-white (2700K) dimmable E14 LED bulbs, 6 W max", "7 Lighting", "1", 60, 80),
    ("To buy", "Later: aluminium channel and opal diffuser for the existing ceiling LED strip (optional)", "7 Lighting", "1", 0, 80),
    ("To buy", "5-in-1 4K60 HDMI switch with remote", "8 TV, consoles and AV", "1", 20, 35),
    ("To do", "Measure the PC-to-TV cable route (about 3–4 m)", "8 TV, consoles and AV", "", None, None),
    ("To buy", "Active optical HDMI cable for the PC, certified Ultra High Speed (48 Gbps), about 5 m", "8 TV, consoles and AV", "1", 20, 60),
    ("To buy", "High Speed HDMI leads, 1–2 m", "8 TV, consoles and AV", "5", 20, 30),
    ("To buy", "RetroTINK-6X CE upscaler for the PS2 and PS1 (order on restock; UK price includes VAT and import fees)", "8 TV, consoles and AV", "1", 200, 240),
    ("To buy", "PS2 component video cable, good quality", "8 TV, consoles and AV", "1", 10, 20),
    ("To buy", "Optical (TOSLINK) cable, 2 m, PS2 straight to the soundbar", "8 TV, consoles and AV", "1", 5, 10),
    ("To buy", "RGB SCART cable for the PS1", "8 TV, consoles and AV", "1", 8, 15),
    ("To do", "Connect the TV inputs; set up the PS2 and RetroTINK", "8 TV, consoles and AV", "", None, None),
    ("To buy", "Replacement stylus for the turntable (exact match for its model)", "9 Vinyl kit", "1", 15, 40),
    ("To buy", "External phono preamp (only if the deck has a PHONO/LINE switch)", "9 Vinyl kit", "1", 40, 100),
    ("To buy", "RCA-to-3.5 mm lead, 3 m: preamp in the cabinet to the soundbar's AUX <b>(changed: longer)</b>", "9 Vinyl kit", "1", 6, 12),
    ("To buy", "Carbon-fibre record brush", "9 Vinyl kit", "1", 10, 15),
    ("To do", "Set the tracking weight; soundbar in Music mode", "9 Vinyl kit", "", None, None),
    ("To do", "Turn on HDMI-CEC (SIMPLINK); PS3 Control for HDMI off", "10 Finishing", "", None, None),
    ("To do", "Deco app: prioritise the Series X and PC, guest Wi-Fi, automatic firmware", "10 Finishing", "", None, None),
    ("To do", "Label each switched socket and HDMI switch input with the console's name", "10 Finishing", "", None, None),
    ("To do", "Set the sub and rear speaker levels from the sofa", "10 Finishing", "", None, None),
]
PHASES = []
for r in TRACK:
    if r[2] not in PHASES:
        PHASES.append(r[2])
BIGGEST = {"1 Network, now": "two 8-port switches", "2 Electrician and cabling": "Cat6 and the switched 6-way", "3 Paint": "paint",
           "4 Base unit": "BESTÅ frames and the PC shelf", "5 Oak joinery": "the solid oak worktop", "6 Vinyl cabinet": "record trays and the carcass",
           "7 Lighting": "spotlight bar and LED", "8 TV, consoles and AV": "RetroTINK-6X CE", "9 Vinyl kit": "phono preamp", "10 Finishing": "—"}


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
    "Can-Am, mmdesign (DiscSox): spine-up media drawer capacities",
    "Sony PS3 and Microsoft Xbox 360 S manuals: ventilation; IKEA UK: secure it",
    "Ideal Home: colour drenching; The Paint Shed: colour drenching with Farrow &amp; Ball; Livingetc: sage green shades (Card Room Green, Treron, Sage Green, Green Smoke)",
    "Pontata: Card Room Green vs Little Greene Sage Green (approximate screen colours)",
    "Homebase and NC Tiles: Farrow &amp; Ball Card Room Green No. 79 in Modern Eggshell and Estate Eggshell",
    "haart Medway: floor plans and listing photos for the house (Portsmouth Close)",
    "ConsoleMods: PS2 Component Video Out setting",
]


def build():
    ptot, tl, th = phase_totals()
    c = fit.counts()
    nfit = sum(c.values())
    css = (HERE / "doc.css").read_text()
    s = G.summary()
    html = f"""<!doctype html><html><head><meta charset="utf-8"><title>Home Network &amp; Media Wall Plan</title>
<style>{css}</style></head><body>

<div class="p1">
<h1>Home Network &amp; Media Wall Plan</h1>
<p class="byline">Revised Oct 18, 2026 · @emma · version {VERSION}, drawn to your measurements</p>

<div class="decision"><b>The one big change.</b> Your tape says the alcove is <b>{n(G.ALC_W)} cm wide and {n(G.ALC_D)} cm deep</b> with a <b>{n(G.CEIL)} cm</b> ceiling, not the 225 × 50 × 220 the last plan assumed. The TV, the Series X and the three bays below still fit; a turntable no longer does. So the whole vinyl corner (deck, LP browser and both face-out record trays) moves into a matching oak cabinet against the chimney breast, right beside the alcove. Everything else you chose stays.</div>

<h2>1 · The plan on a page</h2>
<div class="hero">
<figure class="render">{img("render_v10_join_clean.png", "The artisan oak media wall in Card Room Green, drawn to the measured room")}
<figcaption>Drawn to your measurements, in Card Room Green: the alcove, the vinyl cabinet against the chimney breast, the door to the hall beyond. Full-resolution renders come with this plan.</figcaption></figure>
<div class="summary">
<div><b>£{money(tl, th)}</b><span>plus the electrician, item by item in section 9</span></div>
<div><b>{c[fit.PASS]} of {nfit}</b><span>fit checks pass outright; {c[fit.TIGHT]} is tight, {c[fit.CHECK]} need a check on site (section 3)</span></div>
<div><b>{LPS} · {SINGLES}</b><span>LPs and singles, all face-out</span></div>
</div></div>
<table><tr><th>Area</th><th>Decision</th></tr>
<tr><td>Layout</td><td>Alcove: the TV between two oak uprights, the Series X on its fan stand to the left, a pad dock to the right; three 60 cm bays below for the Xbox consoles, the PlayStations and the sub. Chimney breast: an oak vinyl cabinet, 100 × 44 × 76 cm, deck and LP browser on top, record trays inside.</td></tr>
<tr><td>Records</td><td>Every LP face-out, about {LPS}: 180 in two trays, 50 in the browser, 4 on the ledge over the TV. Every single face-out, about {SINGLES}: 240 in the trays, about {G.BAYB_SINGLES} in a new singles drawer.</td></tr>
<tr><td>Build</td><td>Artisan oak: solid oak uprights with wedged through-tenons and pegged housings, oak face frames, one 3 m solid oak worktop cut for both tops.</td></tr>
<tr><td>Heights</td><td>Worktop and cabinet top {n(G.WORKTOP)} · TV centre 116.5 · side shelves and ledge {n(G.SIDE_SHELF_TOP)} · high shelf {n(G.HIGH_TOP)}, {n(G.CEIL - G.HIGH_TOP)} cm under the {n(G.CEIL)} ceiling.</td></tr>
<tr><td>Colour</td><td>Card Room Green No. 79, colour-drenched; skirting, door and trunking in Estate Eggshell.</td></tr>
<tr><td>Light</td><td>The ceiling LED strip as now, LED grooves in the uprights, a bias light, and a Wolston-style four-spot bar on the rose: sage and blue on the shelves, mustard on the coffee table, pink on the vinyl corner.</td></tr>
<tr><td>Network</td><td>Hub 5 in modem mode; Deco A and Switch 1 in bedroom 3; Cat6 down through the airing cupboard to Deco B and Deco C; spare ports for the projector and the music room.</td></tr>
<tr><td>Power</td><td>The side-wall socket becomes a double: the 10-gang behind the TV (A always on, B retro) and a switched 6-way in bay 3 that also feeds the deck and preamp.</td></tr>
</table>
<p class="confirm"><b>To confirm (full list in section 10):</b> the vinyl corner moving to the chimney breast · where the door to the hall hinges, and the west end's sizes · the turntable, PC case and fan stand models, and the 10-gang's length · the 23 × 22 cm box by the window · wired ports for the projector and the music room.</p>
</div>

<h2 class="pb">2 · The room</h2>
<p>Everything in this plan is now drawn from your hand-measured sketch. Where the agent's floor plan disagrees (it gives the living room as 4.95 × 3.65 m), your tape wins.</p>
<figure>{living_plan()}</figure>
<table class="tight"><tr><th>From your sketch</th><th>mm</th><th>Notes</th></tr>
<tr><td>Room, east to west along the window</td><td class="num">{n(G.ROOM_W*10)}</td><td>The media wall is the south wall, shared with the hall and garage</td></tr>
<tr><td>Window wall to the alcove's back wall</td><td class="num">{n(G.ROOM_D*10)}</td><td>To the chimney breast's face: {n((G.ROOM_D - G.ALC_D)*10)}</td></tr>
<tr><td>Ceiling</td><td class="num">{n(G.CEIL*10)}</td><td>15 cm more than v9 assumed</td></tr>
<tr><td>TV alcove, east wall to the breast</td><td class="num">{n(G.ALC_W*10)} × {n(G.ALC_D*10)}</td><td>Floor to ceiling</td></tr>
<tr><td>Chimney breast</td><td class="num">{n(G.BREAST_W*10)}</td><td>Projects 380 on the alcove side, 390 on the west side</td></tr>
<tr><td>Window and radiator (north wall)</td><td class="num">2350 · 1370</td><td>Window starts 730 from the east wall; radiator ends 130 inside its west end</td></tr>
<tr><td>Skirting</td><td class="num">60 × 20</td><td>White now; Card Room Green eggshell in the plan</td></tr>
<tr><td>West end: recess, door, stair box</td><td class="num">935 / 1045 / 660 / 820</td><td>Drawn roughly: please confirm which is which</td></tr>
<tr><td>Box in the window's west corner</td><td class="num">230 × 220</td><td>Pipe boxing? To confirm</td></tr>
</table>
<p><b>From the sofa:</b> with the sofa against the window wall, 10 cm off the radiator, your eyes are about {s["view_dist"]/100:.2f} m from the screen. A 55-inch fills about {s["view_angle"]:.0f}° of your view, which suits TV and games, and the screen's centre at 116.5 cm sits about 1–2.5° above a seated eye line: comfortable. A 65-inch (about 145 cm wide) wouldn't fit between the uprights. The ceiling light hangs on the existing rose, in line with the breast's corner and {n(-G.WINDOW_Z + G.PEND_Z)} cm from the window wall; at {n(G.CEIL)} cm the lowest shade is at {n(G.CEIL - G.BAR[2])} cm, so headroom is no longer a worry.</p>
<h3>The house</h3>
<figure>{house()}</figure>
<p>Deco A and Switch 1 now sit with the Hub 5 and the gaming PCs in bedroom 3. Both Cat6 runs go across the landing to the airing cupboard, which sits over the alcove's corner, and drop through its floor; section 7 has the details, including the optional runs to the master (projector) and bedroom 2 (music room).</p>

<h2 class="pb">3 · The media wall</h2>
<figure>{why_layout()}</figure>
<div class="why"><b>Why this layout, and what we ruled out</b>
<ul>
<li><b>Turntable on a shelf in the right-hand gap:</b> the gap is {n(G.SIDE_ZONE)} cm; an AT-LP120X is {n(G.DECK[0])} cm wide. Even a slim deck would overhang the upright and leave no room for the lid.</li>
<li><b>One upright, TV off-centre:</b> frees one wider gap, but loses the framed look, the second through-tenon and half the record ledge, and still leaves under 50 cm for a deck beside a 55-inch screen.</li>
<li><b>Series X inside a base bay:</b> it would lie flat, lose the fan stand and take the bay the sub needs.</li>
<li><b>Custom 36 cm carcasses flush with the breast:</b> a cleaner line, but the game drawer's 35 cm box would leave no room for plugs or a cable channel, and the BESTÅ frames couldn't be used. The base stands {n(G.BASE_PROUD)} cm proud of the breast instead, and the vinyl cabinet's oak end covers that step.</li>
</ul></div>
<figure class="render">{img("render_v10_join_key_scene.png", "Render with numbered parts")}
<figcaption>Numbered view: the game drawer and the lower record tray are pulled out 30 cm, with a view of each from above. Dashed lines show what's hidden: gold for data, audio and low-voltage leads, coral for mains. The numbers match the key below.</figcaption></figure>
{key_table()}

<h3>Built to your alcove: {n(G.ALC_W)} wide, {n(G.ALC_D)} deep, {n(G.CEIL)} to the ceiling</h3>
<ul>
<li><b>Base:</b> 3 cm filler, three 60 cm bays, 3 cm filler. Bays 1 and 2 are IKEA BESTÅ 60×40×64 frames on a 9 cm plinth (tops at 73, back panels off); bay 3 is an 18 mm ply carcass 60 × 40 × 73 standing on the floor. One oak face frame runs across all three; its bottom rail hides the plinth.</li>
<li><b>Depth:</b> 40 cm frames, a 4 cm cable channel behind them (flat two-compartment trunking) and the 2 cm face frame make {n(G.BASE_D)} cm from the back wall, so the base stands {n(G.BASE_PROUD)} cm proud of the chimney breast. The vinyl cabinet's oak end panel closes that step on the right.</li>
<li><b>Worktop:</b> solid oak, {n(G.ALC_W)} × {n(G.BASE_D)} × 3, top at 76, with a brush-lined slot behind the TV for its leads and a grommet behind the Series X.</li>
<li><b>Oak uprights:</b> two, 4.5 × 30 cm, {n(G.UPRIGHT_LEN)} cm from the worktop to the ceiling, at {n(G.UP_L[0])}–{n(G.UP_L[1])} and {n(G.UP_R[0])}–{n(G.UP_R[1])} cm from the side wall: {n(G.TV_GAP)} cm between them, {n(G.TV_CLEAR)} cm clear of the TV each side.</li>
<li><b>Either side of the TV:</b> {n(G.SIDE_ZONE)} cm. The Series X stands on its fan stand on the left, with about 39 cm of air above it; the right side holds a pad charging dock and the remotes.</li>
<li><b>Shelves above:</b> oak side shelves at 156 either side, through-tenoned into the uprights; the record ledge at 155.4 between them, four LPs face-out; the high shelf at 196, wall to wall in three lengths, with books up to 30 cm, a box, a print and Deco B.</li>
<li><b>TV:</b> on LG's stand set 2 cm off the back wall: the screen's bottom at {n(G.TV_BOTTOM)}, centre 116.5, top {n(G.TV_TOP)}, 1.3 cm under the ledge. The soundbar sits at the worktop's front edge; from the sofa you look over it.</li>
<li><b>Bay 3:</b> the sub on a 5 cm riser, facing the sofa, with 11.6 cm behind it for its rear port; a shelf above it for the pad dock and spares, with the switched 6-way at its back; a hidden slim drawer under the worktop.</li>
<li><b>Power:</b> the side-wall socket in front of bay 1 becomes a double; its two leads enter through a notch at the left end of the face frame's bottom rail and run back through the plinth to the channel.</li>
</ul>
<figure>{front()}</figure>
<figure>{section()}</figure>

<h3>The fit proof: every item against its published size</h3>
<p>Each zone below lists what goes in it, its size and where that size comes from (numbered sources, section 10), the space, what's left and a verdict. {c[fit.PASS]} of the {nfit} checks fit outright. One is tight (the Series X's sides). Two need a check on site: the RetroTINK, whose maker publishes no size, and the door's swing past the vinyl cabinet. Two don't fit, and they're the reasons the layout changed.</p>
{fit.tables_html()}

<h3>Console sizes, every version</h3>
<p>The bays are sized for the largest version of each console. The model number is on the label underneath; a smaller version just leaves more room.</p>
<table class="tight"><tr><th>Console</th><th>Version</th><th>W × D × H (cm)</th><th>Power</th></tr>
<tr><td>PS1</td><td>Original (largest)</td><td>27.0 × 18.8 × 6.0</td><td>Built in</td></tr>
<tr><td>PS1</td><td>PS one</td><td>19.3 × 14.4 × 3.8</td><td>External adapter</td></tr>
<tr><td>PS2</td><td>Original (largest)</td><td>30.2 × 18.3 × 7.8</td><td>Built in</td></tr>
<tr><td>PS2</td><td>Slim</td><td>23.1 × 15.2 × 2.8</td><td>External brick</td></tr>
<tr><td>PS3</td><td>Original (largest)</td><td>32.5 × 27.4 × 9.8</td><td>Built in</td></tr>
<tr><td>PS3</td><td>Slim · Super Slim</td><td>29.0 × 29.0 × 6.5 · 29.0 × 23.0 × 6.0</td><td>Built in</td></tr>
<tr><td>Xbox 360</td><td>Original (largest)</td><td>30.9 × 25.8 × 8.3</td><td>Large external brick</td></tr>
<tr><td>Xbox 360</td><td>S · E</td><td>about 27.0 × 26.4 × 7.5 · 25.4 × 26.4 × 6.7</td><td>External brick</td></tr>
<tr><td>Xbox One</td><td>Original (largest)</td><td>33.3 × 27.4 × 7.9</td><td>External brick</td></tr>
<tr><td>Xbox One</td><td>S · X</td><td>29.5 × 22.9 × 6.4 · 30.0 × 24.0 × 6.0</td><td>Built in</td></tr>
<tr><td>Xbox Series X</td><td>Standing</td><td>15.1 × 15.1 footprint, 30.1 tall</td><td>Built in</td></tr>
</table>

<h3>The game drawer (bay 1, bottom row)</h3>
<p>Unchanged from v9. Two display bins at the front show covers face-out even with the drawer shut (Xbox left, PS2 right, a small tray between them); behind them the rest of the games stand on edge with the spine on top, so every title faces up when you roll it out.</p>
<figure>{game_drawer()}</figure>
<ul>
<li><b>Box:</b> about 54.3 × 35 cm outside on 350 mm full-extension soft-close runners screwed to the BESTÅ sides; 51.9 cm inside; sides 15 cm; 9 mm base lined in felt.</li>
<li><b>Capacity:</b> about 48 games (12 face-out in the bins, about 36 spine-up), 5–6 kg of games and about 10 kg in all. Past about 48, keep the overflow spine-up in the box on the high shelf.</li>
<li><b>Cases:</b> PS2 and Xbox 360 19 × 13.5 × 1.4 cm; Xbox One 17 × 13.5 × 1.1–1.2 cm. Measure about ten of yours before cutting: cases vary by a few millimetres.</li>
<li><b>Runners:</b> Accuride DZ3832EC (43 kg) or Screwfix Essentials 964VN (40 kg); not IKEA's BESTÅ runners, which aren't full extension.</li>
<li><b>Cut list:</b> 12 mm birch ply sides 35 × 15.5 (2), back 51.9 × 15.5, front 51.9 × 6; 9 mm base 52.5 × 34.4 in a groove; 6 mm ply cross divider 51.9 × 9, bin walls 12.6 × 9 (2), raked bin floors 16 × 12.6 (2); oak follower blocks 19 × 12 (2); 20 mm oak lip 56.8 × 6.5.</li>
</ul>

<h3>The PC corner</h3>
<p>The oak PC shelf stays on the side wall, moved 20 cm towards the alcove ({n(-G.PC_SHELF_Z[0] + G.ALC_D)}–{n(-G.PC_SHELF_Z[1] + G.ALC_D)} cm from the alcove's back wall) so it clears the front of the sofa by about 29 cm.</p>
<figure>{pc_shelf()}</figure>
<ul>
<li><b>Layout:</b> 65 cm along the wall, 32 cm out, top at 110. The case's glass faces the room; its back ports face the sofa behind an oak frame with a woven cane panel, open at the top for the exhaust.</li>
<li><b>Cables:</b> through a notch in the shelf's back corner, down slim trunking painted Card Room Green, and along the skirting into the base's channel. Over 3 m, use an active optical HDMI cable, "source" end at the PC.</li>
<li><b>Power:</b> ideally its own socket under the shelf (added on the electrician's visit), so the PC's 500–850 W stays off the media wall strips.</li>
<li><b>Keyboard and mouse:</b> a tray on 300 mm runners in a 7 cm housing under the shelf rolls 25 cm out towards the room.</li>
<li><b>Fixing:</b> a French cleat plus two steel brackets rated 25 kg or more; plugs and screws into masonry, or into studs on plasterboard.</li>
</ul>

<h2 class="pb">4 · The vinyl corner</h2>
<p>An oak cabinet against the chimney breast holds the whole vinyl collection and the deck in one place, at the same 76 cm as the alcove's worktop so the two read as one run of furniture. It's 100 cm wide, tight to the alcove, 44 cm deep and 76 cm tall: an 18 mm ply carcass behind an oak face frame, with an oak end panel on the side you see and a 2 cm gap at the back for its leads.</p>
<ul>
<li><b>Bay A, 60 cm:</b> the two face-out record trays from v9, unchanged: about 90 LPs and 120 singles each, all face-out.</li>
<li><b>Bay B, 40 cm:</b> an open cubby for the phono preamp, spare stylus, brush, cleaning fluid and inner sleeves; below it, a new singles drawer with about {G.BAYB_SINGLES} singles face-out beside the cleaning kit.</li>
<li><b>On top:</b> the LP browser (44 × 24, about 50 LPs face-out) on the left, the turntable on the right on isolation feet. The top takes a deck up to the size of an AT-LP120X (45.2 × 35.2 cm), with 3.8 cm behind it for the lid hinges.</li>
<li><b>Lid:</b> keep the chimney breast clear up to 130 cm so the lid opens fully. Above that, two framed LPs from 150 cm.</li>
<li><b>The door:</b> the cabinet stops {n(G.DOOR_CLEAR)} cm short of the breast's west corner. If the door to the hall hinges on the breast side and opens into the room, check its handle clears the cabinet's end before building.</li>
<li><b>Safety:</b> two loaded trays weigh about 32 kg each. Fix the cabinet to the breast with anti-tip brackets before loading it, and open one tray at a time.</li>
<li><b>Sound:</b> the deck is about a metre from the sub, on a separate cabinet, so bass doesn't feed back into the stylus; isolation feet help further.</li>
</ul>
<figure>{drawer()}</figure>
<h3>How the record trays work</h3>
<ul>
<li><b>LP trough:</b> 32.6 cm wide, so a bare 31.4 cm sleeve has 6 mm each side. Records lean back 10° like a record shop browser; the last one leans on a raked oak rest.</li>
<li><b>Singles trough:</b> 18.9 cm wide, the same lean, a smaller rest at the back.</li>
<li><b>Capacity:</b> 38.2 cm inside. About 31 cm of LP stack at about 3.3 mm each (gatefolds allowed for): about 90. About 34 cm of singles at about 2.8 mm: about 120. Two trays: about 180 LPs and 240 singles.</li>
<li><b>Outer sleeves:</b> if most LPs live in thick outer sleeves (up to 32.3 cm), widen the LP trough to 33.4 cm; the singles trough then drops to 18.1 cm, too narrow for face-out singles.</li>
<li><b>Runners:</b> 400 mm full extension, 68–70 kg per pair, screwed straight into the 18 mm ply.</li>
</ul>
<table class="tight"><tr><th>Dimension</th><th>Figure</th><th>How it adds up</th></tr>
<tr><td>Bay A carcass</td><td>60 × 40 × 73 outside, 56.4 × 69.4 inside</td><td>18 mm birch ply; back open to the cable gap</td></tr>
<tr><td>Tray width</td><td>53.9 outside, 52.1 inside</td><td>56.4 opening − 2 × 1.25 runners; 9 mm sides</td></tr>
<tr><td>Tray depth</td><td>40 outside, 38.2 inside</td><td>9 mm front and back panels</td></tr>
<tr><td>Inside layout</td><td>32.6 + 0.6 + 18.9</td><td>LP trough, oak divider, singles trough</td></tr>
<tr><td>Lower tray</td><td>Underside 2.3, base top 3.5, sleeves to 34.4</td><td>Lip 2.3 to 7.3; 2.6 cm finger room under the upper tray</td></tr>
<tr><td>Upper tray</td><td>Underside 37.0, base top 38.2, sleeves to 69.1</td><td>Lip 37.0 to 42.0; 2.1 cm under the top panel at 71.2</td></tr>
<tr><td>Weight</td><td>About 32 kg per tray, full</td><td>90 × 0.23 kg + 120 × 0.045 kg + about 5 kg of tray</td></tr>
</table>
<h3>The singles drawer (bay B)</h3>
<p>Bay B is 40 cm wide outside and 36.4 cm inside, which takes a 33.9 cm drawer box on the same 400 mm runners. One 18.9 cm trough holds about {G.BAYB_SINGLES} singles face-out, leaning back 10°; the 13 cm beside it takes the cleaning kit and spare inner sleeves. Its 5 cm oak lip matches the trays. The cubby above it is open, so the preamp's light shows and its leads are easy to reach.</p>
<h3>Cut list</h3>
<table class="tight"><tr><th>Part</th><th>Material</th><th>Size (cm)</th><th>Qty</th></tr>
<tr><td>Carcass sides (ends and the shared middle)</td><td>18 mm birch ply</td><td>73 × 40</td><td>3</td></tr>
<tr><td>Top and bottom panels, bay A · bay B</td><td>18 mm birch ply</td><td>56.4 × 40 · 36.4 × 40</td><td>2 + 2</td></tr>
<tr><td>Back rails, bay A · bay B</td><td>18 mm birch ply</td><td>56.4 × 8 · 36.4 × 8</td><td>2 + 2</td></tr>
<tr><td>Bay B shelf</td><td>18 mm birch ply</td><td>36.4 × 38, top at 37</td><td>1</td></tr>
<tr><td>End panel (the side you see)</td><td>Oak-veneered ply or solid oak</td><td>76 × 44</td><td>1</td></tr>
<tr><td>Face frame</td><td>20 mm oak</td><td>100 × 73, stiles about 5 wide</td><td>1 set</td></tr>
<tr><td>Top</td><td>Solid oak, from the worktop board</td><td>100 × 44 × 3, chamfered front</td><td>1</td></tr>
<tr><td>Record trays (each)</td><td>12 mm ply base 53.9 × 40; 9 mm ply sides 40 × 12, back 52.1 × 12, front 52.1 × 4.5; 6 mm oak divider 38.2 × 10; raked rests; 15 mm oak lip 56.8 × 5; felt</td><td>—</td><td>2</td></tr>
<tr><td>Singles drawer</td><td>12 mm ply base 33.9 × 40; 9 mm ply sides 40 × 12, back 32.1 × 12, front 32.1 × 4.5; 6 mm oak divider; 15 mm oak lip 36.8 × 5</td><td>—</td><td>1</td></tr>
<tr><td>Runners</td><td>400 mm full extension, side mount, 12.5 mm; 68–70 kg pairs for the trays, 45 kg+ for the singles</td><td>—</td><td>3 pairs</td></tr>
</table>
<h3>How to build it</h3>
<ol>
<li><b>Check the door</b> swings clear of where the cabinet's west end will be, and that the breast's face is flat (scribe the back edge if not).</li>
<li><b>Build the carcass:</b> glue and screw the three sides, the top and bottom panels and the back rails, square; fit bay B's shelf at 37.</li>
<li><b>Set it in place</b> tight to the alcove's base, shimmed level so its top meets the alcove worktop at 73, and fix it to the breast with anti-tip brackets through the 2 cm gap.</li>
<li><b>Fit the runners:</b> the trays' lower pair so the tray underside sits at 2.3, the upper pair at 37.0; the singles drawer's at 2.3.</li>
<li><b>Build and hang the trays and the drawer</b> (glue and screw the bases under the sides; glue the oak dividers down to stiffen them), then fit the oak lips 2–3 mm clear of the face frame.</li>
<li><b>Fit the face frame, end panel and top,</b> oil the oak, and load one tray at a time.</li>
</ol>
<h3>Vinyl through the soundbar, done properly</h3>
<ul>
<li><b>Signal path:</b> turntable set to PHONO → external phono preamp in bay B's cubby → a 3 m RCA-to-3.5 mm lead along the cabinet's back gap, through bay 3 and the channel to the soundbar's AUX input.</li>
<li><b>Check first:</b> the external preamp only helps if the deck has a PHONO/LINE switch. With no switch, plug the deck straight into the soundbar's AUX.</li>
<li><b>Soundbar:</b> Music mode, bass up, surround, night and dialogue modes off. Always the AUX cable, never Bluetooth.</li>
<li><b>Stylus:</b> the exact replacement for the deck's model, tracking weight set to the cartridge maker's figure. Brush records before playing.</li>
<li><b>Upgrade path:</b> a stereo amp with a phono input and sub output plus passive speakers (about £200–450), or an AV receiver with phono and eARC in place of the soundbar (£500+).</li>
</ul>
<h3>Where every record lives</h3>
<table class="tight"><tr><th>Where</th><th>What</th><th>How many</th></tr>
<tr><td>Vinyl cabinet, upper and lower trays</td><td>LPs and singles, face-out</td><td>About 180 LPs + 240 singles</td></tr>
<tr><td>Vinyl cabinet, singles drawer</td><td>Singles, face-out</td><td>About {G.BAYB_SINGLES}</td></tr>
<tr><td>On the cabinet</td><td>LP browser, face-out</td><td>About 50 LPs</td></tr>
<tr><td>Above the TV</td><td>Oak record ledge, the "now playing" wall</td><td>4 LPs</td></tr>
<tr><td>Right shelf</td><td>A framed 7-inch</td><td>1</td></tr>
<tr class="total"><td>Total</td><td></td><td>About {LPS} LPs and {SINGLES} singles, every one face-out</td></tr>
</table>
<p>If the collection grows past that, a 2 × 4 cube unit (about 33 cm cubes, 39 cm deep) holds about 500 LPs on its side behind the sofa.</p>

<h2 class="pb">5 · The oak joinery</h2>
<p>Above the worktop the wall is furniture rather than cladding: two solid oak uprights, shelves carried on joints you can see, and the Card Room Green wall left showing between them.</p>
<ul>
<li><b>Two uprights frame the TV:</b> solid oak, 4.5 × 30 cm, {n(G.UPRIGHT_LEN)} cm long from the worktop to the ceiling, each on two 10 mm dowels, scribed to the ceiling and held to the solid back wall with concealed brackets.</li>
<li><b>Wedged through-tenons:</b> each side shelf (top 156) passes through its upright on two tenons, 6 cm wide and 2.4 thick, showing 2 cm on the TV side with an oak wedge. They sit 12 and 20 cm from the wall, in front of the ledge's housing, so the two joints never meet.</li>
<li><b>Housed and pegged:</b> the high shelf, in three lengths at 196, and the record ledge at 155.4 are housed 1.2 cm into the uprights and pinned with 10 mm oak pegs, which show as dark dots.</li>
<li><b>Record ledge:</b> 7 cm deep with a 1.5 cm lip; four LPs lean against the wall up to about {n(G.LEDGE_LP_TOP)}, {n(G.HIGH_UNDER - G.LEDGE_LP_TOP)} cm under the high shelf.</li>
<li><b>LED grooves:</b> a routed groove on each upright's inner face holds a 2700K strip that washes the wall either side of the TV.</li>
<li><b>Hidden cables:</b> a 2 × 1.5 cm groove down the back of the right upright carries Deco B's 12 V lead and patch lead to the worktop slot. A small notch at the top of each upright lets the ceiling LED strip run straight past.</li>
<li><b>Finish:</b> hardwax oil throughout; lightly limed or smoked oak on the uprights avoids the bright orange "new oak" look.</li>
</ul>
<figure>{joints()}</figure>
<h3>Joinery cut list</h3>
<table class="tight"><tr><th>Part</th><th>Material</th><th>Finished size (cm)</th><th>Joints</th><th>Qty</th></tr>
<tr><td>Uprights</td><td>Solid oak, quarter-sawn if you can</td><td>{n(G.UPRIGHT_LEN)} × 30 × 4.5 (buy 165 and scribe)</td><td>Two mortises each for the side shelf, housings for the high shelf and ledge, LED groove inside, cable groove at the back of the right one</td><td>2</td></tr>
<tr><td>High shelf, centre</td><td>Solid oak</td><td>128.9 × 30 × 4</td><td>Housed 1.2 into both uprights, stub tenons, pegged</td><td>1</td></tr>
<tr><td>High shelf, ends</td><td>Solid oak</td><td>26.45 × 30 × 4</td><td>Housed into one upright, on a cleat on the side wall or the reveal</td><td>2</td></tr>
<tr><td>Record ledge</td><td>Solid oak</td><td>128.9 × 7 × 2.4, lip 126.5 × 1.5 × 0.9</td><td>Housed and pegged</td><td>1</td></tr>
<tr><td>Side shelves</td><td>Solid oak</td><td>31.75 × 25 × 4 ({n(G.SIDE_ZONE)} + 4.5 through + 2 proud)</td><td>Two through-tenons 6 × 2.4, wedged; cleat on the wall</td><td>2</td></tr>
<tr><td>Wedges · pegs</td><td>Oak · 10 mm oak dowel</td><td>6 × 3, tapering 4 to 0.5 mm · 5 long</td><td>Glued into saw kerfs · driven from the front edge</td><td>4 + spares · 6</td></tr>
<tr><td>Worktop and cabinet top</td><td>One solid oak worktop, 300 × 62</td><td>{n(G.ALC_W)} × {n(G.BASE_D)} and 100 × 44, 3 thick</td><td>Chamfered fronts; cut edges sealed</td><td>1 board</td></tr>
<tr><td>Face frames</td><td>Oak, 20 mm</td><td>Base 186 × 73; cabinet 100 × 73; stiles about 5 wide</td><td>Glued and pinned; end stiles scribed</td><td>2 sets</td></tr>
<tr><td>PC screen</td><td>Oak frame 2 × 3 section, pre-woven cane</td><td>26 × 48</td><td>Cane in a groove with a spline</td><td>1</td></tr>
</table>
<p>A standard solid oak worktop (3 m long, 62 cm deep) covers both tops: 186 + 100 cm end to end leaves 14 cm, and the long offcut strips make the trays' lips and the browser's rail. Stock worktops come 27 or 40 mm thick: either works; a 40 mm top lifts everything above it by 1 cm.</p>

<h2 class="pb">6 · Paint and light</h2>
<h3>Paint: Farrow &amp; Ball Card Room Green No. 79</h3>
<p>The room is colour-drenched in Card Room Green: walls, ceiling, alcove, chimney breast, skirting, door and frame, radiator and the PC trunking. It's a soft, neutral grey-green that lets the oak and the records lead; the spotlight bar's colours and the sleeves do the contrast work.</p>
<figure>{img("paint_grid.png", "The artisan oak render in four greens")}
<figcaption>The v10 wall in Card Room Green (chosen) beside Sage Green, Treron and the earlier deep green. Screen colours are approximate and the renders are lit as in the evening: judge from painted samples.</figcaption></figure>
<ul>
<li><b>Finishes:</b> Estate or Modern Emulsion on walls, ceiling, alcove and breast; Estate Eggshell in the same colour on skirting, door, frame, radiator and trunking (Modern Eggshell if the skirting takes knocks).</li>
<li><b>For the OLED:</b> a matt mid-tone (LRV about 27) keeps the screen's contrast in the evening. Turn the spots down for films and keep the bias light on.</li>
<li><b>Order:</b> paint before anything is fixed, so nothing needs cutting in round the uprights, shelves or cabinet.</li>
</ul>
<h3>Skirting: Card Room Green too</h3>
<figure>{img("skirting_options.png", "Three skirting options")}</figure>
<ul>
<li><b>Recommended: Card Room Green, Estate Eggshell.</b> Completes the drench, so the room's edges disappear and the oak and records stand out; hides scuffs far better than white.</li>
<li><b>Darker option: Green Smoke</b> for a defined edge that grounds the room. <b>Lighter:</b> a soft off-white rather than brilliant white.</li>
<li><b>Over the white gloss:</b> wash, key, woodwork primer, then two coats of eggshell; do the door and frame at the same time. Cut the skirting back where the base and the cabinet meet the walls.</li>
</ul>
<h3>Light, in three warm layers</h3>
<ul>
<li><b>The LED strip on the ceiling</b> (as now): it runs round the room's edge, into the alcove and across the breast. Keep it 2700K on a dimmer. Later, an aluminium channel with an opal diffuser hides the dots, or LED coving throws the light across the ceiling instead.</li>
<li><b>Built into the oak:</b> a 2700K strip in each upright's groove, on a driver on the fused spur in bay 3; a 6500K bias light on the back of the TV from its USB port.</li>
<li><b>The ceiling light:</b> a four-head cone spotlight bar in the style of Dunelm's Wolston (£49; 84 × 16 cm, 22.4 cm drop; 4 × E14, 6 W max; IP20), on the existing rose, parallel to the media wall.</li>
</ul>
<table class="tight"><tr><th>Head</th><th>Aim</th></tr>
<tr><td>Sage</td><td>The books and the left of the high shelf</td></tr>
<tr><td>Pale blue</td><td>The record ledge above the TV</td></tr>
<tr><td>Mustard</td><td>Down onto the coffee table</td></tr>
<tr><td>Dusty pink</td><td>The vinyl cabinet: the deck and the browser <b>(new)</b></td></tr>
</table>
<p>Never point a head at the TV, and tilt the front pair so the shades hide the bulbs from the sofa. Use four warm-white (2700K) dimmable E14 LED bulbs and an LED-compatible dimmer, both fitted on the electrician's visit. With the {n(G.CEIL)} cm ceiling the lowest shade is at about {n(G.CEIL - G.BAR[2])} cm.</p>

<h2 class="pb">7 · Power, cables and network</h2>
<h3>Power</h3>
<figure>{power()}</figure>
<ul>
<li><b>The socket:</b> on the side wall just in front of bay 1, about 30 cm up, becomes a double: one socket for the 10-gang, one for the 6-way, never one plugged into the other. Moving it 40 cm back into the alcove behind bay 1 hides it completely, if the electrician is there anyway.</li>
<li><b>10-gang:</b> lying flat on the worktop behind the TV, side B's switch at the left end, reached past the Series X. Side A stays on (TV, soundbar, sub, Series X, USB charger); side B switches the five retro consoles.</li>
<li><b>6-way:</b> on the shelf in bay 3, at the back. Always on: Deco B and Switch 2. Switched: the turntable, the preamp and the RetroTINK.</li>
<li><b>OLED care:</b> leave the TV in standby so it runs its pixel refresh.</li>
</ul>
<h3>Cable routes</h3>
<figure>{routes()}</figure>
<ul>
<li><b>The channel:</b> 4 cm behind the frames, flat two-compartment trunking: mains on one side, HDMI, Cat6 and audio on the other. Switch 2 (15.8 × 10.1 × 2.5 cm) stands on its edge in it.</li>
<li><b>To the TV:</b> its leads drop through the brush-lined slot in the worktop behind it; no socket behind the TV is needed.</li>
<li><b>Deco B:</b> the Cat6 comes through the ceiling in the alcove's right corner; its 12 V lead and patch lead run along the back of the high shelf, down the groove behind the right upright and through the worktop to the 6-way and Switch 2.</li>
<li><b>Vinyl cabinet:</b> its mains and audio leads run along its 2 cm back gap, through the end of the base into bay 3, and on along the channel.</li>
<li><b>Airflow:</b> console bays stay open-backed; at least 4 cm (ideally 10) of air round the Series X; the power bricks on the free half of their console's row.</li>
</ul>
<h3>Network</h3>
<figure>{network()}</figure>
<ul>
<li><b>Bedroom 3:</b> the Hub 5 (in modem mode), Deco A and Switch 1 sit together with the gaming PCs. Switch 1's eight ports: the uplink, two PCs, the two Cat6 runs down to Deco B and Deco C, and, if you want them, the projector in the master and the music room in bedroom 2, leaving one spare.</li>
<li><b>The route down:</b> from bedroom 3 across the landing to the airing cupboard, which sits over the alcove's corner, and down through its floor, often beside the existing pipes. Run 1 comes through the living room ceiling in the alcove's right corner to Deco B; run 2 follows it down the right upright's groove and through the floor to the kitchen, where Deco C goes on the outside of the brick cupboard, up high.</li>
<li><b>Optional runs:</b> the master (projector) and bedroom 2 (music room) are both next to the airing cupboard, so short runs along the landing are cheap to add on the same visit. Wired, the projector streams without buffering; the music room gets a solid link for a computer or audio interface.</li>
<li><b>Sloped ceilings:</b> bedroom 2 and the bathroom slope down to the back wall. Keep any Deco, switch or desk in bedroom 2 on the high side, and run cables along the floor there.</li>
<li><b>Lengths:</b> roughly 6–9 m for run 1 and 9–13 m for run 2; measure the real route and add 2–3 m to each.</li>
</ul>
<p><b>Stage 1, mesh up today:</b> unplug everything from the hub, log in at 192.168.0.1 and turn on Modem Mode (its page then moves to 192.168.100.1); connect Deco A and set it up in the Deco app with the old Wi-Fi name and password; plug Switch 1 into Deco A's other port and the PCs into Switch 1; add Deco B on the high shelf with Switch 2 behind it, and Deco C in the kitchen over Wi-Fi for now; check the Xbox shows NAT: Open.</p>
<p><b>Stage 2, after the cables:</b> plug each Cat6 run into its Deco's free port, confirm Deco B and C show as "Ethernet" in the app, move each to the centre of its floor, and give the Series X and PC high priority under QoS.</p>
<div class="callout"><b>Cabling rules</b><ul>
<li>Solid pure-copper Cat6, round; not CCA or flat cable for the long runs. Measure the real route and add 2–3 m.</li>
<li>Cross mains at right angles; never staple through a cable; no kinks; label both ends. Never two cables between the same two devices (a loop takes the network down).</li>
<li><b>Done when:</b> Deco B and C show "Ethernet", each PC shows 1.0 Gbps, the Xbox shows NAT: Open, and phones hold a strong signal in the kitchen and across the living room.</li></ul></div>
<h3>AV: everything sounds through the Hisense</h3>
<figure>{av()}</figure>
<table class="tight"><tr><th>Source</th><th>Picture</th><th>Sound</th></tr>
<tr><td>PC · Xbox Series X</td><td>TV HDMI 1 · HDMI 3</td><td>Via the TV over eARC (5.1 or Atmos)</td></tr>
<tr><td>Xbox One, Xbox 360, PS3</td><td>HDMI switch → TV HDMI 4</td><td>Via the TV over eARC, 5.1</td></tr>
<tr><td>PS2</td><td>Component → RetroTINK → switch → TV</td><td>Optical straight to the soundbar, 5.1 where the game has it</td></tr>
<tr><td>PS1</td><td>RGB SCART → RetroTINK → switch → TV</td><td>Stereo through the RetroTINK and eARC</td></tr>
<tr><td>Turntable · phone</td><td>—</td><td>Preamp → AUX · Bluetooth</td></tr>
</table>
<ul>
<li><b>TV:</b> rename the inputs (HDMI 4 "Retro"), Deep Colour on HDMI 1, 3 and 4, Game Optimiser on the console inputs, sound out to HDMI eARC with digital audio on Auto or Passthrough. PS3, 360 and Xbox One output 5.1 over HDMI; PS3 "Control for HDMI" off.</li>
<li><b>RetroTINK-6X CE:</b> motion-adaptive deinterlacing suits the PS2's mostly interlaced games, up to 1440p for the TV to finish to 4K. It needs a 5 V 2 A USB plug (none in the box) on its own switched socket of the 6-way. Set the PS2's Component Video Out to Y Cb/Pb Cr/Pr, choose 60 Hz where a game offers it, and use RGB SCART for the PS1.</li>
<li><b>Sharper still:</b> PCSX2 on the PC renders PS2 games at native 4K from your own discs and BIOS.</li>
</ul>
<h3>Sound layout</h3>
<figure>{sound()}</figure>
<ul>
<li><b>Sub:</b> in bay 3 under the TV, on its riser, facing the sofa; turn it down rather than moving it if the bass booms.</li>
<li><b>Rears:</b> either side of the sofa at about seated ear height, angled in; on the AX5100G they're linked by a cable, so one socket and a run behind the sofa. The left one can hang on the side wall by its keyhole.</li>
<li><b>Tuning:</b> set the sub and rear levels from the sofa with the soundbar's remote.</li>
</ul>

<h2 class="pb">8 · Build guide</h2>
<p>Sizes are finished sizes in centimetres. Walls are rarely square: measure the alcove's width at the floor, 76, 156, 196 and the ceiling, and cut the worktop and shelves to the smallest.</p>
<h3>What it's made of</h3>
<table class="tight"><tr><th>Element</th><th>Made from</th><th>Finished size</th><th>Fixing</th></tr>
<tr><td>Plinth (bays 1–2)</td><td>18 mm ply ladder frame</td><td>120 × 38 × 9</td><td>Shimmed level; frames screwed down onto it</td></tr>
<tr><td>Bays 1–2</td><td>2 × IKEA BESTÅ frame, back panels off</td><td>60 × 40 × 64 each, tops at 73</td><td>Joined, 4 cm spacers to the wall, 2 anti-tip brackets each</td></tr>
<tr><td>Bay 3</td><td>18 mm birch ply, back open</td><td>60 × 40 × 73</td><td>Bolted to bay 2, 4 cm spacers, 2 anti-tip brackets</td></tr>
<tr><td>Internal shelves</td><td>4 × BESTÅ shelf (20 kg each); 1 ply shelf in bay 3</td><td>56 × 36</td><td>On pins at the fit-proof heights</td></tr>
<tr><td>Alcove worktop</td><td>Solid oak</td><td>{n(G.ALC_W)} × {n(G.BASE_D)} × 3, top 76</td><td>Screwed up through the tops in slotted holes; brush-lined slot behind the TV</td></tr>
<tr><td>Uprights</td><td>Solid oak</td><td>{n(G.UPRIGHT_LEN)} × 30 × 4.5</td><td>Two 10 mm dowels into the worktop, two concealed brackets each</td></tr>
<tr><td>Side shelves</td><td>Solid oak</td><td>31.75 × 25 × 4, top 156</td><td>Wedged through-tenons, cleat on the wall</td></tr>
<tr><td>Record ledge</td><td>Solid oak</td><td>128.9 × 7 × 2.4, top 155.4</td><td>Housed and pegged</td></tr>
<tr><td>High shelf</td><td>Solid oak, three lengths</td><td>30 × 4, top 196</td><td>Housed and pegged; end lengths also on cleats</td></tr>
<tr><td>Vinyl cabinet</td><td>18 mm birch ply carcass, oak face frame, end panel and top</td><td>100 × 44 × 76</td><td>Anti-tip brackets into the breast</td></tr>
<tr><td>Record trays · singles drawer</td><td>9 and 12 mm birch ply, oak dividers and lips</td><td>53.9 × 40 · 33.9 × 40</td><td>400 mm runners into the ply</td></tr>
<tr><td>Game drawer · hidden drawer</td><td>Birch ply, oak lips</td><td>54.3 × 35 · 52 × 30 × 6</td><td>350 mm · 300 mm runners</td></tr>
<tr><td>PC shelf box</td><td>27 mm oak top, 18 mm oak sides</td><td>65 × 32, box 9 deep</td><td>French cleat and 2 steel brackets</td></tr>
<tr><td>Face frames</td><td>20 mm oak</td><td>186 × 73 and 100 × 73</td><td>Glued and pinned; end stiles scribed</td></tr>
</table>
<h3>Tools</h3>
<ul>
<li>Drill-driver, SDS or hammer drill with masonry bits; spirit level (a cross-line laser makes the heights quick); tape, combination square, cable detector.</li>
<li>Track or circular saw for the worktop (or have the merchant cut the ply and oak to the cut lists), jigsaw for notches.</li>
<li>For the joints: sharp chisels (6, 12, 25 mm), marking gauge, tenon saw, router with a straight bit for the housings and grooves, 10 mm bit for the pegs, mallet; a cove bit for the finger pulls.</li>
<li>Clamps, sander, wood glue; dust mask, eye and ear protection.</li>
</ul>
<h3>Order of work</h3>
<ol>
<li><b>Measure and check:</b> the alcove's width at five heights, plumb and level, the ceiling, the door's swing, and your records and games.</li>
<li><b>Network stage 1</b> (any time): hub in modem mode, Decos and switches set up over Wi-Fi.</li>
<li><b>Electrician:</b> the Cat6 runs from bedroom 3 (and the optional ones), the double socket, sockets by the sofa and under the PC shelf, the fused spur, the spotlight bar and dimmer. Mark every cable route before painting.</li>
<li><b>Paint</b> the whole room in Card Room Green, skirting and door in eggshell, and let it cure for a few days.</li>
<li><b>Mark the heights</b> with a level or laser: 73 (worktop), 152 (side shelf undersides), 153 (ledge), 192 (high shelf underside), and the uprights' lines at {n(G.UP_L[0])}–{n(G.UP_L[1])} and {n(G.UP_R[0])}–{n(G.UP_R[1])} from the side wall.</li>
<li><b>Base:</b> the plinth, then the frames on it, then bay 3; spacers, anti-tip brackets, the trunking in the channel, and the cables run in.</li>
<li><b>Worktop:</b> scribe, oil all over (underside too), screw up through the tops in slotted holes, cut the slot behind the TV.</li>
<li><b>Inside the base:</b> shelves at the fit-proof heights, the game drawer, bay 3's shelf, the hidden drawer, the sub on its riser.</li>
<li><b>Oak joinery:</b> dry-fit each upright with its shelves on the bench; lay the Deco leads in the right upright's groove; stand the uprights on their dowels, fix the brackets, fit the shelves, ledge, wedges and pegs.</li>
<li><b>Vinyl cabinet:</b> build it, check the door, fix it to the breast, fit the trays and the singles drawer, then the face frame, end panel and top.</li>
<li><b>PC shelf:</b> the box, the tray, the cleat and brackets, the cane screen, the trunking to the skirting.</li>
<li><b>Lighting:</b> LED in the upright grooves, the ceiling strip through its notches, the bias light, then aim the spot bar.</li>
<li><b>Connect:</b> place everything, network stage 2, label every plug and HDMI input, and test.</li>
</ol>

<h2 class="pb">9 · Buy list and tracker</h2>
<p>Every purchase and job, in build order, comes to about £{money(tl, th)} plus the electrician's quote. Estimates are approximate UK prices; changed and new items are marked. Tick items off and write in what you paid.</p>
<table class="tight"><tr><th>Phase</th><th>Estimate (£)</th><th>Biggest item</th></tr>{ptot}</table>
<p class="note">Already owned: Virgin Hub 5, three Deco X1500s, two TL-SG105S switches (both become spares), LG OLED C6 55" and its stand, a 10-gang with a switch per side, Hisense AX5100G 5.1 soundbar, the Series X fan stand, the turntable and all the consoles.</p>
<table class="tracker"><thead><tr><th>Status</th><th>Item</th><th>Qty</th><th>Estimate (£)</th><th>Paid (£)</th></tr></thead><tbody>
{tracker_rows()}</tbody></table>

<h2 class="pb">10 · Still to confirm, later ideas, sources</h2>
<h3>Still to confirm</h3>
<ul class="checks">
<li>The vinyl corner moving to an oak cabinet on the chimney breast (because the alcove is 39 cm narrower than assumed).</li>
<li>The door to the hall: which side it hinges, and that it opens clear of the cabinet's west end ({n(G.DOOR_CLEAR)} cm from the breast's corner).</li>
<li>The west end's sizes: which of 935, 1045, 660 and 820 are the recess, the door and the stair box.</li>
<li>The turntable's model (the top allows up to 45.2 × 35.2 cm) and whether it has a PHONO/LINE switch.</li>
<li>The Series X fan stand's model: the left gap fits a footprint up to about 24 cm.</li>
<li>The PC case's model, and that its window is on the left (so the back faces the sofa).</li>
<li>The 10-gang's length and whether it's surge-protected.</li>
<li>The 23 × 22 cm box in the window's west corner.</li>
<li>Wired ports for the projector (master) and the music room (bedroom 2)?</li>
<li>The RetroTINK's size when it arrives (bay 2's bottom row reserves about 30 cm beside the PS1).</li>
<li>Records: roughly how many LPs and singles, and are most in thick outer sleeves?</li>
<li>Games: roughly how many PS2, Xbox 360 and Xbox One? Past about 48, plan overflow.</li>
<li>The floor in the alcove and at the breast: carpet or hard floor (the plinth and cabinets must sit level).</li>
<li>The side wall where the PC shelf goes: solid or plasterboard?</li>
<li class="done">The real room: alcove {n(G.ALC_W)} × {n(G.ALC_D)}, chimney breast {n(G.BREAST_W)}, ceiling {n(G.CEIL)}, skirting 60 × 20.</li>
<li class="done">Artisan oak is the main build; Card Room Green with matching eggshell skirting; the Wolston-style spot bar on the existing rose.</li>
<li class="done">Every record face-out; the game drawer as designed; the LED strip on the ceiling stays.</li>
<li class="done">Power: the side-wall socket in front of bay 1 becomes a double.</li>
</ul>
<h3>Later ideas</h3>
<ul>
<li><b>Dave and Emma's watch log:</b> a shared film and TV log, like a Spotify Blend for what you watch: log each film or episode, mark whether you watched it together, rate it, and later get suggestions for what to watch next. It could live on the TV's browser or your phones. To be shaped up separately.</li>
</ul>
<h3>Sources</h3>
<p class="note">Numbered sources are the item sizes used in the fit proof (section 3).</p>
{fit.sources_html(OTHER_SOURCES)}

<h2 class="pb">Appendix · The slat wall alternative</h2>
<p>Kept for reference, now drawn to the measured room. The base, the vinyl cabinet, the records and the consoles are identical; above the worktop, oak slat panels on battens run from the worktop to the ceiling instead of the uprights, the shelves sit on hidden cleats, the face frame is painted Card Room Green, and the light comes from strips under each shelf. Quicker to fit and good for sound, but it follows a current trend, and it loses the record ledge and the joints on show.</p>
<figure class="render small">{img("render_v10_slat_clean.png", "Slat wall alternative")}</figure>
<h3>Options we rejected along the way</h3>
<table class="tight"><tr><th>Option</th><th>Why not</th></tr>
<tr><td>Hub as router, Decos as access points</td><td>Loses HomeShield and parental controls</td></tr>
<tr><td>All-wireless mesh · powerline</td><td>Speed drops at each hop · slower and less stable than Cat6</td></tr>
<tr><td>2.5 Gb switches</td><td>The Decos and PCs top out at 1 Gb</td></tr>
<tr><td>Games two deep, or lying flat</td><td>The back row is hidden; flat stacks are hard to pick from</td></tr>
<tr><td>Records spine-up in one drawer</td><td>Showed only a handful of covers; face-out trays show every one</td></tr>
<tr><td>A green feature wall only · white skirting</td><td>The drench ties the room together; white cuts a bright line round it</td></tr>
<tr><td>A paper lantern or long pendant</td><td>Replaced by the spot bar you chose</td></tr>
<tr><td>RetroTINK-2X Pro · cheap PS2-to-HDMI adapters</td><td>Legacy, no 480p · soft, washed-out picture on a 55" OLED</td></tr>
<tr><td>Bluetooth from the turntable</td><td>Compresses the sound; the AUX lead keeps full quality</td></tr>
</table>
</body></html>"""
    (HERE / "plan.html").write_text(html)
    print("totals", tl, th, "fit", c)


def pdf():
    from playwright.sync_api import sync_playwright
    from shot import _launch
    footer = ('<div style="width:100%;font-family:Inter,sans-serif;font-size:8px;color:#8a867e;padding:0 18mm;'
              f'display:flex;justify-content:space-between"><span>Home Network &amp; Media Wall Plan · v{VERSION}</span>'
              '<span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>')
    with sync_playwright() as p:
        b = _launch(p)
        pg = b.new_page()
        pg.goto((HERE / "plan.html").resolve().as_uri())
        pg.wait_for_timeout(500)
        pg.pdf(path=str(HERE.parent / "out" / PDF_NAME), format="A4", print_background=True,
               margin={"top": "16mm", "bottom": "18mm", "left": "18mm", "right": "18mm"},
               display_header_footer=True, header_template="<div></div>", footer_template=footer)
        b.close()


if __name__ == "__main__":
    build()
    pdf()
    print("pdf ok")
