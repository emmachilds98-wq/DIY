"""Builds the plan (v10) as HTML, then PDF via headless Chromium.
v10: re-fitted to the client's measured room (alcove 186 x 38, ceiling 235) and reordered to read as one plan."""
import base64, pathlib
from diagrams import network, front, drawer, game_drawer, av, power, routes, pc_shelf, section, joints, house, living_plan
from specs import fit_tables, source_list, ref

HERE = pathlib.Path(__file__).parent
VERSION = "10"

def img(name, alt=""):
    data = base64.b64encode((HERE / name).read_bytes()).decode()
    kind = "jpeg" if name.endswith(".jpg") else "png"
    return f'<img src="data:image/{kind};base64,{data}" alt="{alt}">'

# ---------------------------------------------------------------- tracker data
# (status, item, phase, qty, lo, hi)  lo/hi None = no cost
TRACK = [
    ("To do", "Put the Virgin Hub 5 into modem mode", "Network", "", None, None),
    ("To do", "Set up Deco A and Switch 1 in bedroom 3 with the Hub 5 and both gaming PCs <b>(changed)</b>", "Network", "", None, None),
    ("To do", "Add Deco B and C; speed-test each room and the Xbox", "Network", "", None, None),
    ("To buy", "Cat6 patch leads, 0.5–2 m", "Network", "11", 15, 20),
    ("To buy", "TP-Link TL-SG108 8-port switch: one for the living room, one to replace the 5-port upstairs", "Network", "2", 36, 50),
    ("To do", "Book one electrician visit: both Cat6 runs from bedroom 3 across the landing and down through the airing cupboard (Deco B's through the ceiling in the alcove's right corner), optional runs to the master (projector) and bedroom 2 (music room), swap the single socket on the side wall in front of bay 1 for a double, a socket by the sofa for the rear speakers, a socket under the PC shelf, a switched fused spur for the LED drivers, and the spotlight bar with an LED-compatible dimmer <b>(changed)</b>", "Cabling and power", "", None, None),
    ("To buy", "Cat6 solid pure copper, round (not CCA): two runs, plus two optional", "Cabling and power", "2–4 runs", 30, 70),
    ("To buy", "6-way surge-protected extension with individually switched sockets, for Deco B, the 8-port switch, turntable, preamp and RetroTINK (your 10-gang takes the rest)", "Cabling and power", "1", 25, 40),
    ("To buy", "4-port USB charger, 5V 2A per port (HDMI switch, Xbox fan stand, pad dock)", "Cabling and power", "1", 10, 20),
    ("To buy", "USB plug, 5V 2A or more, for the RetroTINK on the switched strip", "Cabling and power", "1", 5, 10),
    ("To buy", "Cable kit: brush grommets (incl. two for the end panels between the base and the cabinet), velcro ties, labels", "Cabling and power", "1", 20, 30),
    ("To buy", "Flat two-compartment trunking for the 4 cm channel, about 2 m <b>(changed)</b>", "Cabling and power", "1", 10, 20),
    ("To buy", "Slim paintable trunking for the PC drop and skirting run, about 3 m", "Cabling and power", "1", 15, 30),
    ("To buy", "DC extension lead for the Deco adapter, if its lead won't reach down the upright's groove to the 6-way (match the plug)", "Cabling and power", "1", 5, 10),
    ("To buy", "PC tidy kit: braided sleeve, right-angle C13 power lead, shelf-notch grommet", "Cabling and power", "1", 10, 20),
    ("To buy", "Phono lead long enough for preamp → soundbar AUX via the floor grommets: RCA-to-3.5 mm, about 3 m <b>(changed)</b>", "Cabling and power", "1", 8, 15),
    ("To do", "Sample Farrow & Ball Card Room Green No. 79 on an A4 board; check by day and with the LED strip on", "Decorating", "", None, None),
    ("To buy", "Farrow & Ball Card Room Green No. 79: Estate (or Modern) Emulsion for walls, ceiling and alcove; Estate Eggshell for skirting, door, frame and trunking; primer/undercoat", "Decorating", "", 200, 500),
    ("To buy", "Woodwork primer, sanding pads and sugar soap for the white skirting and door", "Decorating", "1", 20, 40),
    ("To do", "Paint the whole room, alcove and chimney breast included, before anything goes in; skirting and door from white to Card Room Green eggshell", "Decorating", "", None, None),
    ("Done", "Measure the room accurately (your sketch): alcove 186 × 38, breast 117.5, ceiling 235", "Media wall", "", None, None),
    ("Done", "Check the alcove back wall for the shelf fixings (solid)", "Media wall", "", None, None),
    ("To do", "Check the side wall where the PC shelf goes: solid, or plasterboard on studs", "Media wall", "", None, None),
    ("To buy", "Two IKEA BESTÅ 60×40×64 frames, white stained oak effect, for bays 1–2", "Media wall", "2", 70, 200),
    ("To buy", "Plinth for bays 1–2: 18 mm ply ladder frame 120 × 38 × 9 cm, plus shims", "Media wall", "1", 15, 30),
    ("To buy", "Bay 3 carcass (sub bay): 18 mm birch ply, sides 73 × 40, top and bottom 56.4 × 40, shelf 56.4 × 38, back rails, connector bolts <b>(changed)</b>", "Media wall", "1", 50, 90),
    ("To buy", "Two 3 cm filler strips for the ends of the base, scribed to the walls, and an oak return for the 8 cm proud end beside the breast <b>(new)</b>", "Media wall", "1", 10, 25),
    ("To buy", "BESTÅ shelves, 56 × 36 cm (20 kg max each), two each for bays 1 and 2", "Media wall", "4", 12, 32),
    ("To buy", "Anti-tip wall brackets and 4 cm spacer blocks for the two frames, bay 3 and the vinyl cabinet <b>(changed)</b>", "Media wall", "1 set", 15, 30),
    ("To do", "Measure about ten games of each kind (PS2, Xbox 360, Xbox One) before cutting the game drawer", "Media wall", "", None, None),
    ("To buy", "Game drawer kit: 12 mm birch ply cut to size, 350 mm full-extension soft-close runners (35–49 kg), oak lip, follower block, felt", "Media wall", "1", 50, 90),
    ("To buy", "Hidden slim drawer in bay 3: 12 mm ply box 53.9 × 30 × 4.5, oak front 54.8 × 5.4, 300 mm runners <b>(changed)</b>", "Media wall", "1", 25, 45),
    ("To buy", "Compact isolation riser for the sub (about 30 × 34 cm, 5 cm tall), plus isolation feet for the turntable", "Media wall", "1", 30, 60),
    ("To buy", "Pad charging dock for the bay 3 shelf, and a basket for spare pads and cables", "Media wall", "1", 15, 35),
    ("To buy", "Bookends for the high shelf; a lidded box for cables and controllers", "Media wall", "1", 20, 40),
    ("To buy", "PC shelf box with a keyboard and mouse tray: oak 27 mm top 65 × 32, 18 mm sides, 300 mm light runners, French cleat, 2 steel brackets rated 25 kg+", "Media wall", "1", 55, 120),
    ("To do", "Build the plinth and bay 3, fix everything to the wall; set rows to the fit-proof heights; fit the game drawer; place the TV, soundbar, Series X and sub", "Media wall", "", None, None),
    ("To buy", "Vinyl cabinet carcass: 18 mm birch ply for bay A (sides 73 × 40, top and bottom 56.4 × 40) and bay B (side 73 × 40, top and bottom 38.2 × 40, shelf 38.2 × 38), connector bolts <b>(new)</b>", "Vinyl corner", "1", 70, 120),
    ("To buy", "Two face-out record tray kits: 12 mm and 9 mm birch ply cut to size, 6 mm oak dividers, 15 mm oak lips, raked rests, felt, two pairs of 400 mm runners rated 68–70 kg", "Vinyl corner", "2", 150, 240),
    ("To buy", "LP browser for the cabinet top: oak base, low front rail and end, 44 × 24 cm", "Vinyl corner", "1", 30, 60),
    ("To buy", "Three LP frames (about 32.5 cm square) for the breast above the deck <b>(new)</b>", "Vinyl corner", "3", 30, 60),
    ("To buy", "Replacement stylus for the turntable", "Vinyl corner", "1", 15, 40),
    ("To buy", "External phono preamp (only if the deck has a PHONO/LINE switch)", "Vinyl corner", "1", 40, 100),
    ("To buy", "Carbon-fibre record brush", "Vinyl corner", "1", 10, 15),
    ("To do", "Build the vinyl cabinet, fix it to the breast, hang both trays, set the deck level, tracking weight and soundbar Music mode", "Vinyl corner", "", None, None),
    ("To buy", "5-in-1 4K60 HDMI switch, auto-switching, with remote", "TV and consoles", "1", 20, 35),
    ("To do", "Measure the PC-to-TV cable route (estimated 4–5 m)", "TV and consoles", "", None, None),
    ("To buy", "Active optical HDMI cable for the PC, certified Ultra High Speed (48 Gbps), about 5–7.5 m", "TV and consoles", "1", 20, 60),
    ("To buy", "High Speed HDMI leads, 1–2 m", "TV and consoles", "5", 20, 30),
    ("To buy", "RetroTINK-6X CE upscaler for the PS2 and PS1 (order on restock; UK price includes VAT and import fees)", "TV and consoles", "1", 200, 240),
    ("To buy", "PS2 component video cable, good quality", "TV and consoles", "1", 10, 20),
    ("To buy", "Optical (TOSLINK) cable, 2 m, PS2 straight to the soundbar", "TV and consoles", "1", 5, 10),
    ("To buy", "RGB SCART cable for the PS1", "TV and consoles", "1", 8, 15),
    ("To do", "Connect the TV inputs; set up the PS2 and RetroTINK", "TV and consoles", "", None, None),
    ("To do", "Turn on HDMI-CEC (SIMPLINK); PS3 Control for HDMI off", "Finishing", "", None, None),
    ("To do", "Deco app: prioritise Series X and PC, guest Wi-Fi, auto firmware", "Finishing", "", None, None),
    ("To do", "Label each switched socket and HDMI switch input with the console's name", "Finishing", "", None, None),
    ("To do", "Set the sub and rear speaker levels from the sofa", "Finishing", "", None, None),
    ("To buy", "Two solid oak uprights, buy 165 × 30 × 4.5 cm and scribe to 159, quarter-sawn if possible <b>(changed)</b>", "Oak joinery and lighting", "2", 160, 320),
    ("To buy", "Solid oak for the shelves: high shelf in three lengths (128.9 centre, 26.45 × 2 ends, all 30 × 4), side shelves 31.75 × 25 × 4 × 2, record ledge 128.9 × 7 × 2.4 <b>(changed)</b>", "Oak joinery and lighting", "1 set", 160, 300),
    ("To buy", "Oak wedges, 10 mm oak dowel for pegs and dowels, concealed upright brackets", "Oak joinery and lighting", "1", 15, 30),
    ("To buy", "Solid oak worktop, full stave: 186 × 42 × 3 for the base and 100 × 45 × 3 for the vinyl cabinet, chamfered fronts (the offcut makes the easel and browser base) <b>(changed)</b>", "Oak joinery and lighting", "1", 220, 420),
    ("To buy", "Oak face frames, 20 mm: the base (186 × 73) and the cabinet (100 × 73), plus the 8 cm oak return <b>(changed)</b>", "Oak joinery and lighting", "1", 100, 210),
    ("To buy", "Cane screen for the PC: oak frame and pre-woven cane, 26 × 48 cm", "Oak joinery and lighting", "1", 20, 40),
    ("To buy", "LED for the upright grooves: 2700K strip, two aluminium channels, driver; 6500K bias light for the TV", "Oak joinery and lighting", "1", 40, 90),
    ("To buy", "Ceiling light: Dunelm Elements Wolston 4-light spotlight bar (£49) plus four warm-white (2700K) dimmable E14 LED bulbs, 6 W max", "Oak joinery and lighting", "1", 60, 80),
    ("To buy", "Later: aluminium channel and opal diffuser for the existing ceiling LED strip (optional)", "Oak joinery and lighting", "1", 0, 80),
    ("To do", "Cut the joints, fit the uprights, shelves, ledge and face frames, notch the uprights for the ceiling strip, and wire the LEDs (see the build guide)", "Oak joinery and lighting", "", None, None),
]
PHASES = ["Network", "Cabling and power", "Decorating", "Media wall", "Vinyl corner", "TV and consoles", "Oak joinery and lighting"]
BIGGEST = {"Oak joinery and lighting": "solid oak worktops, uprights and shelves", "Network": "two 8-port switches", "Cabling and power": "Cat6 cable and the 6-way",
           "Decorating": "paint", "Media wall": "BESTÅ frames and the game drawer", "Vinyl corner": "record trays and the cabinet carcass", "TV and consoles": "RetroTINK-6X CE"}

def money(a, b):
    return f"{a:,}–{b:,}"

def phase_totals():
    rows, tl, th = [], 0, 0
    for ph in PHASES:
        lo = sum(r[4] for r in TRACK if r[2] == ph and r[4] is not None)
        hi = sum(r[5] for r in TRACK if r[2] == ph and r[5] is not None)
        tl += lo; th += hi
        extra = ", plus electrician" if ph == "Cabling and power" else ""
        rows.append(f"<tr><td>{ph}</td><td class='num'>{money(lo, hi)}{extra}</td><td>{BIGGEST[ph]}</td></tr>")
    rows.append(f"<tr class='total'><td>Total</td><td class='num'>{money(tl, th)}, plus electrician</td><td></td></tr>")
    return "\n".join(rows), tl, th

def tracker_rows():
    out = []
    for ph in PHASES + ["Finishing"]:
        out.append(f"<tr><td colspan='6' style='background:#eef0e8;font-weight:650'>{ph}</td></tr>")
        for st, item, p, q, lo, hi in TRACK:
            if p != ph:
                continue
            box = "☑" if st == "Done" else "☐"
            est = money(lo, hi) if lo is not None else ("Quote" if "electrician" in item else "")
            out.append(f"<tr><td class='st'>{box} {st}</td><td>{item}</td><td>{p}</td><td class='num'>{q}</td><td class='num'>{est}</td><td class='paid'></td></tr>")
    return "\n".join(out)


def key_table():
    from render import JOIN_KEY
    groups, cur = [], None
    for it in JOIN_KEY:
        if it[0] == "H":
            cur = [it[1], []]; groups.append(cur)
        else:
            cur[1].append(it)
    left = groups[:3]; right = groups[3:]
    def col(gs):
        out = []
        for name, items in gs:
            out.append(f"<tr><td colspan='2' class='kg'>{name}</td></tr>")
            out += [f"<tr><td class='kn'>{n}</td><td>{lab}</td></tr>" for n, _, lab in items]
        return "<table class='key'>" + "".join(out) + "</table>"
    return "<div class='keycols'>" + col(left) + col(right) + "</div>"

def build():
    ptot, tl, th = phase_totals()
    css = (HERE / "doc.css").read_text()
    html = f"""<!doctype html><html><head><meta charset="utf-8"><title>Home Network &amp; Media Wall Plan</title>
<style>{css}</style></head><body>
<h1>Home Network &amp; Media Wall Plan</h1>
<p class="byline">Revised Oct 18, 2026 · @emma · version 10, fitted to your measured room</p>

<h2>The plan at a glance</h2>
<div class="decision"><b>One decision for you:</b> your sketch shows the alcove is 186 cm wide and 38 cm deep, not the 225 × 50 the plan assumed, so the turntable and the record trays no longer fit in it beside the TV. This plan moves them to a matching oak vinyl cabinet against the chimney breast, right next to the media wall. Everything else you chose stays. Say if you'd rather keep the vinyl in the alcove and we'll show what that costs (see "Why this layout").</div>
<figure class="render">{img("render_v10_join_clean.png", "The media wall and vinyl cabinet, v10")}
<figcaption>The artisan oak media wall in the 186 cm alcove, with the vinyl cabinet on the chimney breast beside it, in Farrow &amp; Ball Card Room Green. Drawn to your measurements, from the sofa side of the room.</figcaption></figure>
<h3>The key decisions</h3>
<table><tr><th>Area</th><th>Plan</th></tr>
<tr><td>Room</td><td>Re-fitted to your sketch: alcove 186 × 38, chimney breast 117.5, ceiling 235. Colour-drenched in Farrow &amp; Ball Card Room Green No. 79, skirting to match in eggshell.</td></tr>
<tr><td>Media wall</td><td>Artisan oak, as you chose: two oak uprights 126.5 cm apart frame the 55-inch TV (2 cm clear each side), with a record ledge above it, side shelves and a high shelf at 200 on through-tenons and pegs. Series X on its fan stand in the left gap.</td></tr>
<tr><td>The base</td><td>3 + 60 + 60 + 60 + 3 = 186: the Xbox bay with the game drawer, the PlayStation bay, and an open bay for the sub with a hidden drawer. Solid oak worktop at 76, oak face frame, 8 cm proud of the breast.</td></tr>
<tr><td>Vinyl corner</td><td>New: an oak cabinet 100 × 44 × 76 on the chimney breast. Your two face-out record trays (unchanged) in one bay, the preamp and kit in the other, the turntable and LP browser on top, LP frames above.</td></tr>
<tr><td>Records and games</td><td>About 234 LPs, every one face-out, and about 240 singles face-out (plus overflow); about 48 games, every title visible.</td></tr>
<tr><td>Light</td><td>Your LED strip round the ceiling, LED grooves in the uprights, a bias light, and the four-head Wolston-style spotlight bar on the existing rose.</td></tr>
<tr><td>Network</td><td>Hub 5 in modem mode, Deco A and Switch 1 in bedroom 3 with the gaming PCs, Cat6 down through the airing cupboard to Deco B (living room) and Deco C (kitchen); spare ports for the projector and the music room.</td></tr>
<tr><td>Power and AV</td><td>The side-wall socket becomes a double: your 10-gang behind the TV and a 6-way in bay 3. Everything plays through the Hisense soundbar; PS2 and PS1 through a RetroTINK-6X CE.</td></tr>
</table>
<p>It all comes to about <b>£{money(tl, th)}</b> plus the electrician, item by item in the buy list. Still to confirm, briefly: the door's position and hinge side, the turntable, PC case and fan stand models, the 10-gang's length, and the small box in the window corner (full list at the end).</p>
<p class="note">Contents: The plan at a glance · The room · The media wall (renders, key, fit proof, why this layout) · The game drawer · The vinyl corner · The oak joinery · Paint and light · Power, cables and network · Build guide · Buy list and tracker · Still to confirm, later ideas, sources · Appendix: the slat wall.</p>

<h2 class="pb">The room</h2>
<p>Everything in this plan now comes from your hand-measured sketch, which replaces every earlier assumption (225 × 50 alcove, 220 ceiling). North is the window wall; the media wall is the south wall, shared with the hall and garage.</p>
<figure>{living_plan()}</figure>
<table class="tight"><tr><th>From your sketch</th><th>Size (cm)</th></tr>
<tr><td>Room, along the window × window wall to the alcove's back wall</td><td>467 × 347</td></tr>
<tr><td>Ceiling</td><td>235, everywhere</td></tr>
<tr><td>TV alcove, east end of the south wall</td><td>186 wide × 38 deep, floor to ceiling</td></tr>
<tr><td>Chimney breast</td><td>117.5 wide, 38 proud (39 on its west side)</td></tr>
<tr><td>West recess, breast to the stair box</td><td>about 104.5 × 39</td></tr>
<tr><td>Window (north wall), radiator under it</td><td>235 wide from 73 off the east wall; radiator 137 long, about 158–295 from the east wall</td></tr>
<tr><td>Skirting</td><td>6 high × 2 thick</td></tr>
<tr><td>Stair box and doorway, west end</td><td>about 82 × 66–79, from the window wall 268 (several figures unclear: to confirm)</td></tr>
<tr><td>Small box in the window's west corner</td><td>23 × 22 (pipe boxing?)</td></tr>
</table>
<p><b>From the sofa:</b> against the window wall, 10 cm off the radiator, your eyes are about 0.65 m from the window wall and the screen sits about 20 cm back in the alcove, so you're about <b>2.6–2.7 m</b> from the screen. A 55-inch fills about 26° of your view there, right for TV and games, and the screen's centre at 116.6 cm is 2–3° above your seated eye line. A 2 m sofa can't be centred on the TV (its centre is only 93 cm from the east wall), so it starts about 22 cm off the east wall, room for the rear speaker, about 30 cm west of centre: barely noticeable from the seats.</p>
<p><b>Ceiling light:</b> the existing rose is about 186 cm from the east wall (in line with the breast's reveal) and 173.5 cm from the window wall. With the 235 ceiling, the spotlight bar's lowest shade hangs at about 212 cm, so headroom isn't a concern.</p>
<h3>The house</h3>
<figure>{house()}</figure>
<ul>
<li><b>Bedroom 3</b> has the gaming PCs and the Hub 5, so Deco A and Switch 1 live there. Both Cat6 runs cross the landing to the airing cupboard, which sits over the alcove's right-hand corner, and drop through its floor.</li>
<li><b>Master bedroom:</b> the projector. <b>Bedroom 2:</b> the spare room, planned as a music room; its ceiling slopes down to the back (north) wall, so keep a Deco or desk on the high side.</li>
<li><b>Kitchen:</b> the brick cupboard in the middle of the back wall sits under the chimney breast. Deco C goes on its outside, up high.</li>
</ul>

<h2 class="pb">The media wall</h2>
<p>The artisan oak build, re-fitted to the real alcove. Above the worktop, two solid oak uprights frame the TV with 2 cm to spare each side, carrying a record ledge above the screen, a short shelf each side at 156 and a high shelf at 200 (35 cm under the ceiling now). Below it, one oak-fronted base fills the 186 cm exactly: the Xbox bay with the game drawer, the PlayStation bay, and an open bay for the subwoofer under the right of the TV, on a solid oak worktop at 76. The vinyl moves next door, to a matching cabinet on the chimney breast.</p>
<figure class="render">{img("render_v10_join_key_scene.png", "Render with numbered parts")}
<figcaption>Numbered view, with the game drawer and the lower record tray pulled out 30 cm and an inset of each from above. Dashed lines show what's hidden: gold for data, audio and Deco B's leads, coral for mains. The numbers match the key below.</figcaption></figure>
{key_table()}
<figure>{front()}</figure>

<h3>What goes where</h3>
<ul>
<li><b>Uprights:</b> solid oak, 4.5 × 30 × 159, worktop to ceiling, at 25.25–29.75 and 156.25–160.75 cm from the east wall, against the back wall. 126.5 cm clear between them for a 122.2 cm screen.</li>
<li><b>Left gap (25.25 wide):</b> the Series X upright on its fan stand. With a 20.5 cm stand it has 2.4 cm each side and nearly 40 cm of open air above it, more than Microsoft's 4 cm for an open stand{ref("seriesx")}. If your stand is wider than 21 cm, the TV can shift a few cm right: say which stand it is.</li>
<li><b>Right gap (25.25 wide):</b> too narrow for a turntable now, so it holds "this month's game" face-out on a small oak easel, with Deco B above it on the high shelf.</li>
<li><b>TV:</b> the LG C6 55" on its own stand (47 × 23.1){ref("lgc6")}, centred, screen from 81.4 to 151.8, centre 116.6, 1.2 cm under the record ledge.</li>
<li><b>Soundbar:</b> 92 × 9 × 6 at the front edge of the worktop, 7 cm in front of the TV's stand{ref("ax5100g")}.</li>
<li><b>Record ledge:</b> 126.5 × 7, top at 155.4, four LPs face-out (125.6 cm of sleeves: snug), leaning to about 186.5, 9.5 cm under the high shelf.</li>
<li><b>Side shelves:</b> 25 deep, top 156, one each side, through-tenoned into the uprights: favourite games on the left, a framed single and a trailing plant on the right.</li>
<li><b>High shelf:</b> 30 × 4, top 200, wall to wall in three lengths: books up to 30 cm, a lidded box, a print, Deco B on the right end where the Cat6 drops in from the ceiling.</li>
<li><b>Worktop:</b> solid oak 186 × 42 × 3, top at 76, flush with the face frame; a 4 cm slot behind it for cables and warm air.</li>
<li><b>Bays 1 and 2:</b> BESTÅ 60 × 40 × 64 frames on a 9 cm plinth{ref("besta")}, back panels off, every row exactly as before (fit proof below).</li>
<li><b>Bay 3:</b> an open 18 mm ply carcass 60 × 40 × 73: the sub on a 5 cm riser, a shelf at 41.8 for the pad dock and spares, the hidden slim drawer under the worktop, and the 6-way at the back.</li>
<li><b>Depth:</b> 4 cm channel + 40 frames + 2 cm face frame = 46 cm from the back wall, so the base stands 8 cm proud of the breast. The 8 cm end showing beside the breast is returned in oak.</li>
</ul>
<figure>{section()}</figure>

<h3>Fit proof: every item, its source, its space</h3>
<p>Each size below comes from a cited source (numbers refer to the Sources list at the end); the space is from your measurements. "Spare" is what's left.</p>
{fit_tables()}

<div class="callout"><b>Why this layout</b>
<p>The v9 wall was 225 wide: Series X zone 44.5, TV between uprights 126.5, turntable zone 45. At 186 the TV and its uprights still fit exactly, which leaves 50.5 cm, about 25 each side: enough for the Series X, not for a turntable (45 × 35) and its lid. The base loses one bay the same way: 3 × 60 + two 3 cm fillers.</p>
<ul>
<li><b>Chosen:</b> vinyl to a matching cabinet on the chimney breast. The trays keep their tested design, the deck gets a full-size top with 40 cm clear for its lid, and it's a metre from the sub instead of above it.</li>
<li><b>Rejected: turntable on a shelf in the right gap.</b> 25 cm wide against a 45 cm deck.</li>
<li><b>Rejected: TV off-centre with one upright.</b> Frees about 30 cm on one side, still short of 45, and loses the framed look you liked.</li>
<li><b>Rejected: Series X lying in a base bay.</b> Takes a whole bay, loses the fan stand, and still leaves no room for the deck.</li>
<li><b>Rejected: custom 36 cm-deep carcasses, flush with the breast.</b> The record trays need 40 cm (400 mm runners) and the game drawer 35 cm plus its lip; at 36 both would shrink and lose capacity, so the base stays 8 cm proud.</li>
</ul></div>

<h3>Console sizes, every version</h3>
<p>The bays are sized for the largest version of each console. The model number is on the label underneath; a smaller version just leaves more room.</p>
<table class="tight"><tr><th>Console</th><th>Version</th><th>W × D × H (cm)</th><th>Power</th></tr>
<tr><td>PS1</td><td>Original (largest)</td><td>27.0 × 18.8 × 6.0</td><td>Built in</td></tr>
<tr><td>PS1</td><td>PS one</td><td>19.3 × 14.4 × 3.8</td><td>External adapter</td></tr>
<tr><td>PS2</td><td>Original (largest)</td><td>30.2 × 18.3 × 7.8</td><td>Built in</td></tr>
<tr><td>PS2</td><td>Slim</td><td>23.1 × 15.2 × 2.8</td><td>External brick</td></tr>
<tr><td>PS3</td><td>Original (largest)</td><td>32.5 × 27.4 × 9.8</td><td>Built in</td></tr>
<tr><td>PS3</td><td>Slim</td><td>29.0 × 29.0 × 6.5</td><td>Built in</td></tr>
<tr><td>PS3</td><td>Super Slim</td><td>29.0 × 23.0 × 6.0</td><td>Built in</td></tr>
<tr><td>Xbox 360</td><td>Original (largest)</td><td>30.9 × 25.8 × 8.3</td><td>Large external brick</td></tr>
<tr><td>Xbox 360</td><td>S</td><td>about 27.0 × 26.4 × 7.5</td><td>External brick</td></tr>
<tr><td>Xbox 360</td><td>E</td><td>about 25.4 × 26.4 × 6.7</td><td>External brick</td></tr>
<tr><td>Xbox One</td><td>Original (largest)</td><td>33.3 × 27.4 × 7.9</td><td>External brick</td></tr>
<tr><td>Xbox One</td><td>S</td><td>29.5 × 22.9 × 6.4</td><td>Built in</td></tr>
<tr><td>Xbox One</td><td>X</td><td>30.0 × 24.0 × 6.0</td><td>Built in</td></tr>
<tr><td>Xbox Series X</td><td>Standing</td><td>15.1 × 15.1 footprint, 30.1 tall</td><td>Built in</td></tr>
</table>


<h2 class="pb">The game drawer</h2>
<p>The bottom row of bay 1 becomes a roll-out drawer for Xbox 360, Xbox One and PS2 games. At the front, two display bins hold games face-out, leaning back slightly like the record trays, so the front cover of each is on show even with the drawer shut: Xbox on the left, PS2 on the right, with a small tray between them. Behind them, the rest of the collection stands on its long edge with the spine on top. Roll the drawer out and every title faces up at you, in rows you can read without moving anything, and any game lifts straight out.</p>
<figure>{game_drawer()}</figure>
<h3>The cases it's built for</h3>
<table class="tight"><tr><th>Console</th><th>Case (height × width × thickness)</th><th>Spine-up, it stands</th><th>Where it goes</th></tr>
<tr><td>PS2 (PAL)</td><td>19 × 13.5 × 1.4 cm (DVD-size keep case)</td><td>13.5 tall, 19 long</td><td>Back row left; PS2 display bin</td></tr>
<tr><td>Xbox 360</td><td>19 × 13.5 × 1.4 cm, same as PS2</td><td>13.5 tall, 19 long</td><td>Back row centre; Xbox display bin</td></tr>
<tr><td>Xbox One</td><td>17 × 13.5 × 1.1–1.2 cm</td><td>13.5 tall, 17 long</td><td>Back row right, behind the follower block; Xbox display bin</td></tr>
<tr><td>PS1 (PAL)</td><td>14.3 × 13 × 1.74 cm, much fatter</td><td>—</td><td>Not in this unit</td></tr>
</table>
<p>Measure about ten of your own games of each kind before cutting: cases vary by 1–3 mm between publishers and replacement cases, and steelbooks are slightly bigger.</p>
<h3>Sizes and capacity</h3>
<ul>
<li><b>Box:</b> about 54.3 cm wide and 35 cm deep outside, on 350 mm runners screwed to the BESTÅ sides (the same way IKEA's own BESTÅ drawers fix). With 12 mm ply sides that leaves about 51.9 cm inside. Sides about 15 cm tall, with a 9 mm base lined in felt.</li>
<li><b>Front (13 cm deep):</b> two bins 16 cm wide, each taking one column of cases leaning back 13°, about six per bin, so 12 games are on display and you flip through them from the front. A removable 2 cm block in the Xbox bin lifts the shorter Xbox One cases level with the 360 ones. The 18.7 cm tray between them holds memory cards, a pad or manuals.</li>
<li><b>Back (about 19.5 cm deep):</b> one transverse row of cases standing on their opening edge, spine up, each 19 cm case running front to back. About 37 PS2 or 360 games fit across at 1.4 cm each, or about 43 Xbox One at 1.2 cm. A sliding follower block keeps a part-full row upright and divides the consoles. As drawn: 15 PS2, 12 Xbox 360 and 9 Xbox One.</li>
<li><b>In total</b> about 48 games, roughly 5–6 kg with the drawer about 10 kg. That's fewer than the 80 the old two-deep upright row held, but none are hidden.</li>
<li><b>Height:</b> a 25.2 cm row. Base clearance, the drawer base and a leaning 19 cm case come to about 22 cm, leaving about 3 cm to get fingers in.</li>
<li><b>Is spine-up safe?</b> Yes. The disc still stands vertically, as in book-style shelving, which archival guidance prefers over lying flat. Don't pack the row so tight the cases bow, and keep the covers out of direct sun.</li>
</ul>
<h3>Runners</h3>
<table class="tight"><tr><th>Runner, 350 mm</th><th>Type</th><th>Rating</th><th>Note</th></tr>
<tr><td>Accuride DZ3832EC (premium)</td><td>Full extension, soft-close, side-mount</td><td>43 kg</td><td>About 30 cm of travel exposes the whole back row</td></tr>
<tr><td>Screwfix Essentials 964VN (value)</td><td>Full extension, self-closing, ball-bearing</td><td>40 kg</td><td>Easy to buy locally</td></tr>
<tr><td>IKEA BESTÅ drawer runners</td><td>Soft-close or push-open</td><td>—</td><td>Not recommended: reported as not full extension, and push-open fires from a stray foot</td></tr>
</table>
<p>At about 10 kg, any of the first two has at least four times the load it needs.</p>
<h3>Cut list</h3>
<table class="tight"><tr><th>Part</th><th>Material</th><th>Size (cm)</th><th>Qty</th></tr>
<tr><td>Box sides</td><td>12 mm birch ply</td><td>35 × 15.5</td><td>2</td></tr>
<tr><td>Box back and front panel</td><td>12 mm birch ply</td><td>51.9 × 15.5 (back), 51.9 × 6 (front)</td><td>1 + 1</td></tr>
<tr><td>Base, in a 6 mm groove</td><td>9 mm birch ply</td><td>52.5 × 34.4</td><td>1</td></tr>
<tr><td>Cross divider</td><td>6 mm ply</td><td>51.9 × 9</td><td>1</td></tr>
<tr><td>Bin walls</td><td>6 mm ply</td><td>12.6 × 9</td><td>2</td></tr>
<tr><td>Bin floors (raked)</td><td>6 mm ply</td><td>16 × 12.6</td><td>2</td></tr>
<tr><td>Follower blocks</td><td>20 mm oak offcut, felted</td><td>19 × 12</td><td>2</td></tr>
<tr><td>Xbox One lift block</td><td>20 mm offcut</td><td>15 × 12</td><td>1</td></tr>
<tr><td>Oak lip (front)</td><td>20 mm oak</td><td>56.8 × 6.5</td><td>1</td></tr>
<tr><td>Runners</td><td>Full extension, soft-close, side mount</td><td>350 mm</td><td>1 pair</td></tr>
</table>
<h3>How to build it</h3>
<ol>
<li><b>Fix the frames to the wall first</b>, on their plinth, as for the record trays.</li>
<li><b>Fit the runners</b> to the frame sides, level, with the drawer base about 1 cm above the frame's bottom panel; drill pilot holes, as BESTÅ sides are particleboard. Use the frame's pre-drilled holes or short chipboard screws; if a screw won't hold, add a 12 mm ply packer.</li>
<li><b>Build the box</b> from 12 mm birch ply: sides and back about 15 cm tall, a 9 mm base in a groove, glued and screwed. Make its width exactly what the runners specify.</li>
<li><b>Add the dividers:</b> a cross divider 13 cm back from the front, and two bin walls 16 cm in from each side. Fit the two bin floors with a slight back-rake so cases lean about 13°.</li>
<li><b>Make the follower block</b> from a 2 cm offcut, 12 cm tall and 19 cm long, felted underneath so it slides; one or two of them separate the consoles.</li>
<li><b>Fit the front:</b> a 6.5 cm oak lip with a hand-cut finger pull, in the same oak as the record trays, overlaying the face frame with a 2–3 mm gap.</li>
</ol>
<div class="callout"><b>Options</b><ul>
<li><b>PS1 games:</b> stored outside this unit. PAL cases are about 14.3 × 13 × 1.74 cm, about 57 per metre of shelf.</li>
<li><b>More games:</b> past about 48, keep the overflow spine-up in a high-shelf box, rotating favourites into the drawer.</li>
<li><b>Sorting:</b> label the follower blocks by console, and keep the bins for what you're playing now.</li></ul></div>


<h2 class="pb">The vinyl corner</h2>
<p>A new oak cabinet against the chimney breast, beside the media wall and matching it: the same oak face frame and a 3 cm solid oak top at 76. Bay A (60) holds the two face-out record trays from v9, unchanged. Bay B (40) holds the phono preamp, stylus, brush, cleaning kit and spare inner sleeves on a shelf, with overflow singles below. On top, the LP browser and the turntable side by side; above them on the breast, three LP frames from 140 cm up, clear of the deck's lid.</p>
<ul>
<li><b>Size:</b> 100 wide × 44 deep × 76 high: 18 mm ply carcass 40 deep standing 2 cm off the breast (over the skirting), 2 cm oak face frame, oak top 100 × 45 × 3 scribed to the wall. It stands 2 cm clear of the reveal and ends 15.5 cm short of the breast's west jamb.</li>
<li><b>Door:</b> the cabinet's west end comes out 44 cm. Check the door to the hall clears it when open (tell us where it hinges).</li>
<li><b>Turntable:</b> on the right of the top, over bay B, allowing for a deck as big as the Audio-Technica AT-LP120X (45.2 × 35.2 × 14.2){ref("lp120")}; most decks are smaller. Keep 40 cm clear above it for the lid: nothing on the breast below about 135.</li>
<li><b>LP browser:</b> 44 × 24 on the left of the top, about 50 LPs face-out leaning back 10°, its front LP on show.</li>
<li><b>Preamp and leads:</b> the deck's leads drop through a grommet behind it to the preamp in bay B. Its output runs through grommets low in the cabinet's and the base's end panels, across the 2 cm gap at floor level and up the channel to the soundbar's AUX input. Power comes the same way from the 6-way in bay 3.</li>
<li><b>Fixing:</b> two anti-tip brackets into the breast before the trays are loaded; only one tray open at a time.</li>
<li><b>Away from the sub:</b> the deck is now about a metre from the subwoofer, on its own cabinet, which helps keep bass out of the stylus.</li>
</ul>
<h3>The record trays</h3>
<p>Two roll-out trays stacked in bay A, and everything in them is face-out: LPs in a trough on the left leaning back about 10°, like a record shop browser, 7-inch singles the same way on the right. With a tray shut you see the front LP and the front single above a slim oak lip; pull it out and flip through both rows of covers.</p>
<figure>{drawer()}</figure>
<h4>The tray design (unchanged from v9)</h4>
<ul>
<li><b>Thinner trays:</b> 9 mm birch ply sides, front and back instead of 12 mm, a 12 mm base instead of 18 mm, a 6 mm oak divider, and a slimmer oak lip, 5 cm tall and 15 mm thick. It looks lighter from the room and shows more of each front cover.</li>
<li><b>What the slimmer build buys:</b> 4.2 cm more width inside each tray, enough to turn the singles to face-out (a 7-inch sleeve is 18.3 cm), and 6 mm more finger room above every row.</li>
<li><b>Spare inner sleeves</b> live in bay B beside the preamp.</li>
</ul>
<h4>How the system works</h4>
<ul>
<li><b>LP trough:</b> 32.6 cm wide, so a bare 31.4 cm sleeve has 6 mm each side. Records lean back 10° against each other; the last one leans on a raked oak rest at the back.</li>
<li><b>Singles trough:</b> 18.9 cm wide, the same lean, a smaller rest at the back.</li>
<li><b>Capacity:</b> the inside is 38.2 cm deep. The lean takes about 5.5 cm for LPs, leaving about 31 cm of stack: about 90 LPs at about 3.3 mm each, allowing for gatefolds. Singles lean less far, leaving about 34 cm: about 120 at about 2.8 mm. Two trays: about 180 LPs and 240 singles.</li>
<li><b>Outer plastic sleeves:</b> if most of your LPs live in thick outer sleeves (up to about 32.3 cm), widen the LP trough to 33.4 cm; the singles trough then drops to 18.1 cm, too narrow for face-out singles, so they go back to spine-up.</li>
<li><b>Runners:</b> 400 mm full-extension ball-bearing runners rated 68–70 kg per pair (45 kg is the minimum), screwed straight into the carcass's 18 mm ply sides. The whole tray clears the unit, so the back records are as easy to reach as the front.</li>
<li><b>Weight and safety:</b> about 32 kg per full tray. The cabinet must be fixed to the breast with anti-tip brackets before the trays are loaded, and only one tray opened at a time.</li>
</ul>
<h4>Sizes</h4>
<table class="tight"><tr><th>Dimension</th><th>Figure</th><th>How it adds up</th></tr>
<tr><td>Bay A carcass</td><td>60 × 40 × 73 outside, 56.4 × 69.4 inside</td><td>18 mm birch ply sides, top and bottom; back open; 2 cm off the breast</td></tr>
<tr><td>Tray width</td><td>53.9 outside, 52.1 inside</td><td>56.4 opening − 2 × 1.25 runners; 9 mm sides</td></tr>
<tr><td>Tray depth</td><td>40 outside, 38.2 inside</td><td>9 mm front and back panels</td></tr>
<tr><td>Inside layout</td><td>32.6 + 0.6 + 18.9</td><td>LP trough, oak divider, singles trough</td></tr>
<tr><td>Lower tray</td><td>Underside 2.3, base top 3.5, sleeves to 34.4</td><td>Lip from 2.3 to 7.3; 2.6 cm finger room under the upper tray</td></tr>
<tr><td>Upper tray</td><td>Underside 37.0, base top 38.2, sleeves to 69.1</td><td>Lip from 37.0 to 42.0; 2.1 cm finger room under the top panel at 71.2</td></tr>
<tr><td>Capacity</td><td>About 90 LPs and 120 singles per tray</td><td>About 31 cm of LP stack ÷ 3.3 mm; about 34 cm of singles ÷ 2.8 mm</td></tr>
<tr><td>Weight</td><td>About 32 kg per tray, full</td><td>90 × about 0.23 kg + 120 × about 0.045 kg + about 5 kg of tray</td></tr>
</table>
<h4>Cut list</h4>
<table class="tight"><tr><th>Part</th><th>Material</th><th>Size (cm)</th><th>Qty</th></tr>
<tr><td>Bay A sides (one shared with bay B)</td><td>18 mm birch ply</td><td>73 × 40</td><td>2</td></tr>
<tr><td>Carcass top and bottom (between the sides)</td><td>18 mm birch ply</td><td>56.4 × 40</td><td>2</td></tr>
<tr><td>Carcass back rails (top and bottom, back open between)</td><td>18 mm birch ply</td><td>56.4 × 8</td><td>2</td></tr>
<tr><td>Tray bases</td><td>12 mm birch ply</td><td>53.9 × 40</td><td>2</td></tr>
<tr><td>Tray sides</td><td>9 mm birch ply</td><td>40 × 12</td><td>4</td></tr>
<tr><td>Tray backs</td><td>9 mm birch ply</td><td>52.1 × 12</td><td>2</td></tr>
<tr><td>Tray front panels (low, so the covers show)</td><td>9 mm birch ply</td><td>52.1 × 4.5</td><td>2</td></tr>
<tr><td>Dividers</td><td>6 mm oak</td><td>38.2 × 10</td><td>2</td></tr>
<tr><td>Raked back rests (10°)</td><td>20 mm oak offcut</td><td>32.6 × 12 and 18.9 × 8</td><td>2 + 2</td></tr>
<tr><td>Oak lips (fronts)</td><td>15 mm oak</td><td>56.8 × 5</td><td>2</td></tr>
<tr><td>Felt or cork liner</td><td>2 mm</td><td>52 × 38</td><td>2</td></tr>
<tr><td>Runners</td><td>Full extension, side mount, 12.5 mm, 68–70 kg pair</td><td>400 mm</td><td>2 pairs</td></tr>
</table>
<p>The 12 mm base carries about 27 kg of records. Glue and screw it under the sides, front and back all round, and glue the oak divider down to it: the divider stiffens the middle, so the base doesn't sag over time.</p>
<h4>How to build them</h4>
<ol>
<li><b>Build the cabinet:</b> bay A and bay B as one carcass, glued and screwed square, with back rails. Have the merchant cut the ply to the list.</li>
<li><b>Set it in place</b> against the breast on 2 cm spacers over the skirting, 2 cm clear of the reveal, shimmed level with its top at 73, and fix it to the breast with anti-tip brackets.</li>
<li><b>Fit the runners</b> straight onto the ply sides, level, every screw hole used: the lower pair so the tray's underside sits at 2.3 cm, the upper pair at 37.0 cm. Make the tray width exactly what the runner instructions specify (normally the opening less 25 mm).</li>
<li><b>Build the trays:</b> sides, back and low front panel glued and pinned to each other, then glued and screwed down onto the 12 mm base. Glue the oak divider 32.6 cm in from the left inside face, fit the two raked rests, and glue the felt down.</li>
<li><b>Hang the trays</b> and check they run true empty.</li>
<li><b>Fit the oak lips</b> from inside the tray, with a hand-cut finger pull at the top centre, 2–3 mm clear of the face frame.</li>
<li><b>Load gradually,</b> one tray at a time, and check both still run smoothly full.</li>
</ol>

<h3>Every record face-out: where they live</h3>
<table class="tight"><tr><th>Where</th><th>What</th><th>How many</th></tr>
<tr><td>Vinyl cabinet, upper tray</td><td>LPs and singles, face-out</td><td>About 90 LPs + 120 singles</td></tr>
<tr><td>Vinyl cabinet, lower tray</td><td>LPs and singles, face-out</td><td>About 90 LPs + 120 singles</td></tr>
<tr><td>On the cabinet</td><td>Oak LP browser, face-out</td><td>About 50 LPs</td></tr>
<tr><td>Above the TV</td><td>Oak record ledge, the "now playing" wall</td><td>4 LPs</td></tr>
<tr><td>Bay B, lower</td><td>Overflow singles, spine-out</td><td>About 120 a row (240 two deep)</td></tr>
<tr><td>On the breast</td><td>LP frames</td><td>3 LPs (rotate them)</td></tr>
<tr class="total"><td>In all</td><td></td><td>About 234 LPs and 240 singles face-out, plus overflow</td></tr>
</table>
<p><b>If the collection grows:</b> a 2 × 4 cube unit (IKEA KALLAX, cubes about 33 cm inside) holds about 500 LPs on its side under the window or behind the sofa; each tray also takes about 95 LPs packed tight, at the cost of an easy flip.</p>

<h2 class="pb">The oak joinery</h2>
<p>Above the worktop the wall is furniture rather than cladding: two solid oak uprights, shelves carried on joints you can see, and the Card Room Green wall showing between them.</p>
<ul>
<li><b>Two uprights frame the TV:</b> solid oak, 4.5 × 30 × 159 (worktop 76 to ceiling 235), 2 cm clear of each side of the screen. They stand on the worktop on two dowels each, are scribed to the ceiling and held to the solid back wall with concealed brackets.</li>
<li><b>Wedged through-tenons:</b> the side shelves (top 156) pass through the uprights on two tenons each and show 2 cm on the TV side, held with oak wedges: the joints you see first.</li>
<li><b>Housed and pegged:</b> the high shelf, in three lengths at 200, and the record ledge are housed into the uprights and pinned with 10 mm oak pegs, which show as dark dots.</li>
<li><b>Record ledge:</b> 7 cm deep with a 1.5 cm lip, top 155.4, four LPs face-out.</li>
<li><b>LED grooves:</b> a routed groove in each upright's inner face holds a 2700K strip that washes the wall either side of the TV.</li>
<li><b>Cable groove:</b> 2 × 1.5 cm down the back of the right upright for Deco B's 12 V lead and patch lead.</li>
<li><b>Notch for the ceiling strip:</b> 2 × 1.5 cm in the back top corner of each upright so the existing LED strip runs straight past.</li>
<li><b>Oak where you touch it:</b> 3 cm solid oak worktops on the base and the vinyl cabinet, chamfered fronts, oak face frames, hand-cut finger pulls.</li>
<li><b>Finish:</b> hardwax oil throughout; a lightly limed or smoked oak keeps away from the bright orange "new oak" look.</li>
</ul>
<figure>{joints()}</figure>
<h3>Joinery cut list</h3>
<table class="tight"><tr><th>Part</th><th>Material</th><th>Finished size (cm)</th><th>Joints</th><th>Qty</th></tr>
<tr><td>Uprights</td><td>Solid oak, quarter-sawn if you can</td><td>159 × 30 × 4.5 (buy 165 and scribe)</td><td>2 mortises each for the through-tenons, housings for the high shelf and ledge, LED groove inside, cable groove at the back of the right one</td><td>2</td></tr>
<tr><td>High shelf, centre</td><td>Solid oak</td><td>128.9 × 30 × 4</td><td>Housed 1.2 into both uprights, stub tenons, pegged</td><td>1</td></tr>
<tr><td>High shelf, ends</td><td>Solid oak</td><td>26.45 × 30 × 4</td><td>Housed into one upright, on a cleat on the side wall or reveal</td><td>2</td></tr>
<tr><td>Record ledge</td><td>Solid oak</td><td>128.9 × 7 × 2.4, lip 126.5 × 1.5 × 0.9</td><td>Housed and pegged</td><td>1</td></tr>
<tr><td>Side shelves</td><td>Solid oak</td><td>31.75 × 25 × 4 (25.25 + 4.5 through + 2 proud)</td><td>Two through-tenons 7 × 2.4, wedged; cleat on the wall</td><td>2</td></tr>
<tr><td>Wedges</td><td>Oak</td><td>7 × 3, tapering 4 to 0.5 mm</td><td>Glued into saw kerfs</td><td>4 + spares</td></tr>
<tr><td>Pegs</td><td>10 mm oak dowel</td><td>5 long</td><td>Driven from the front edge, trimmed flush</td><td>6</td></tr>
<tr><td>Worktop, base</td><td>Solid oak, full stave</td><td>186 × 42 × 3</td><td>Chamfered front; cut edges sealed</td><td>1</td></tr>
<tr><td>Top, vinyl cabinet</td><td>Solid oak, same board</td><td>100 × 45 × 3</td><td>Chamfered front, scribed to the breast</td><td>1</td></tr>
<tr><td>Face frames</td><td>Oak, 20 mm</td><td>Base 186 × 73; cabinet 100 × 73; stiles 2.6–5.6 wide, rails 2.6 and 2</td><td>Glued and pinned; end stiles scribed</td><td>2 sets</td></tr>
<tr><td>Oak return, base end beside the breast</td><td>Oak, 20 mm</td><td>8 × 73</td><td>Glued to the end stile</td><td>1</td></tr>
<tr><td>Easel, right gap</td><td>Oak offcut</td><td>17 × 9, with a 2 cm lip</td><td>Glued</td><td>1</td></tr>
<tr><td>PC screen</td><td>Oak frame 2 × 3, pre-woven cane</td><td>26 × 48</td><td>Cane in a groove with a spline</td><td>1</td></tr>
</table>

<h2 class="pb">Paint and light</h2>
<h3>Paint: Farrow &amp; Ball Card Room Green</h3>
<p>The room is colour-drenched in Farrow &amp; Ball Card Room Green No. 79, your pick from the last grid: walls, ceiling, alcove, skirting, door and frame, radiator and the PC trunking, all one colour. It's a soft, neutral grey-green, calm without feeling cold, a little lighter and greyer than Sage Green. The oak, the records and the colours of the spotlight bar do the contrast work.</p>
<figure>{img("paint_grid.png", "The artisan oak render in four greens")}
<figcaption>The artisan oak version in Card Room Green (top left, chosen) beside Sage Green, Treron and the earlier deep green. Screen colours are approximate and the renders are lit as in the evening, so judge from painted samples.</figcaption></figure>
<ul>
<li><b>Finishes:</b> Estate Emulsion (chalky, flat) or Modern Emulsion (more wipeable) on walls, ceiling and alcove; Estate Eggshell in the same colour on skirting, door, frame, radiator and trunking. Modern Eggshell is the tougher choice for the skirting if it takes knocks.</li>
<li><b>Ceiling:</b> the same colour keeps the drench seamless and makes the LED strip's wash read as one soft band.</li>
<li><b>For the OLED:</b> Card Room Green is a mid-tone (LRV about 27): matt and muted enough that the screen keeps its contrast in the evening. Turn the spots down while watching and keep the bias light behind the TV.</li>
<li><b>Choosing:</b> paint an A4 board and look at it by day and with the LED strip on: warm LEDs push greys towards green, cool daylight towards grey.</li>
<li><b>Order:</b> paint before building anything, alcove included, so nothing needs cutting in around the uprights and shelves.</li>
<li><b>How much:</b> measure walls and ceiling. A mid-tone over pale walls usually covers in two coats; over the old white gloss on the woodwork, prime first.</li>
</ul>
<h4>Skirting: paint it Card Room Green too</h4>
<figure>{img("skirting_options.png", "Three skirting options with Card Room Green walls")}</figure>
<ul>
<li><b>Recommended: Card Room Green in Estate Eggshell.</b> The wall colour with a soft sheen. It completes the drench, so the room's edges disappear and the oak base and records are what you notice, and it hides scuffs from feet and the hoover far better than white.</li>
<li><b>Darker option: Green Smoke.</b> A deeper Farrow &amp; Ball grey-green with a hint of blue, for a defined edge that grounds the room. It draws the eye down, so keep it to the skirting and door.</li>
<li><b>Keeping a light trim:</b> swap the brilliant white for a soft off-white. Bright white next to a muted grey-green looks cold and stark.</li>
<li><b>Painting over white gloss or satin:</b> wash, key with a fine sanding pad, prime with a woodwork primer, then two coats of eggshell. Do the door, frame and window board at the same time.</li>
<li><b>Behind the unit:</b> where the base meets the side wall inside the alcove, cut the skirting back so the oak end stile sits flush, or scribe the stile over it.</li>
</ul>

<h3>Lighting</h3>
<p>Three layers, all warm: the LED strip you already have round the ceiling, light built into the oak, and a spotlight bar on the existing ceiling rose in the middle of the room.</p>
<h4>Now: the LED strip round the ceiling</h4>
<ul>
<li><b>What you have:</b> a strip stuck to the ceiling (not the wall) round the whole edge of the room, facing down, as in your photo. In the renders it runs along the side wall, into the alcove, across its back wall and reveal, across the chimney breast and round the recess, washing the top of every wall.</li>
<li><b>Where it meets the oak:</b> the uprights run up to the ceiling against the back wall, so the strip would stop at each one. Cut a small notch, about 2 × 1.5 cm, in the back top corner of each upright so the strip runs straight through.</li>
<li><b>Keep it warm:</b> 2700K, on a dimmer, so it matches the rest.</li>
</ul>
<h4>Later: upgrading the strip</h4>
<table class="tight"><tr><th>Upgrade</th><th>What it does</th><th>Effort</th></tr>
<tr><td>Aluminium channel with an opal diffuser, in the same place</td><td>Hides the individual LED dots and gives a clean line; cools the strip so it lasts longer</td><td>Easy: stick or clip the channel up, re-lay the strip</td></tr>
<tr><td>LED coving or a shadow-gap cornice</td><td>Hides the strip completely and throws light up across the ceiling instead of down the walls: softer, no glare from the sofa</td><td>Medium: fixed and painted Card Room Green with the walls</td></tr>
<tr><td>Strip in the uprights' grooves only, on a separate circuit</td><td>Light the media wall on its own for films, with the room strip off</td><td>Planned already; needs the fused spur for the driver</td></tr>
</table>
<h4>Built into the oak</h4>
<ul>
<li><b>Upright grooves:</b> a 2700K strip in an aluminium channel in a groove on each upright's inner face, washing the green wall either side of the TV.</li>
<li><b>Bias light:</b> a 6500K strip on the back of the TV, from its USB port, which is easier on the eyes in a dark room.</li>
</ul>
<h4>The ceiling light: a four-head spotlight bar</h4>
<p>On the existing ceiling rose, in the middle of the room in line with the alcove's right-hand edge, in the style of Dunelm's Elements Wolston bar: a slim white bar with four conical shades on short stems, each with a light-wood topper, in your photo's colours of sage green, pale blue, mustard and dusty pink. The colours pick up the record sleeves, the wood toppers echo the oak, and against Card Room Green the pastel shades read as soft colour rather than clutter.</p>
<table class="tight"><tr><th>Wolston 4-light spotlight bar</th><th>Figure</th></tr>
<tr><td>Price</td><td>£49 at Dunelm</td></tr>
<tr><td>Size</td><td>84 cm long, 16 cm deep, 22.4 cm drop; shades 15 cm across</td></tr>
<tr><td>Build</td><td>Steel, adjustable heads, wood-effect toppers; semi-flush on a ceiling plate</td></tr>
<tr><td>Bulbs</td><td>4 × E14 (small screw), 6 W max each, not included; dimmable with compatible E14 LED bulbs</td></tr>
<tr><td>Rating</td><td>IP20 (indoors), Class 1: needs wiring in to the ceiling rose</td></tr>
</table>
<ul>
<li><b>Which way it runs:</b> parallel to the media wall, as drawn, so all four heads can reach their targets.</li>
<li><b>Aiming:</b> the two heads nearest the wall (sage and blue) light the books, the record ledge and the high shelf; the other two (mustard and pink) point down into the room and the coffee table. Never point a head at the TV, and tilt the front pair so the shades hide the bulbs from the sofa.</li>
<li><b>Bulbs:</b> four warm-white (2700K) dimmable E14 LED bulbs, 4–6 W each, so they match the strip and the uprights.</li>
<li><b>Dimmer:</b> swap the wall switch for an LED-compatible dimmer; turn the spots right down for films.</li>
<li><b>Headroom:</b> with a 22.4 cm drop on the 235 cm ceiling, the lowest shade sits at about 212 cm: no headroom concern, even with the heads tilted.</li>
<li><b>Fitting:</b> it replaces the bare pendant on the existing rose; have the electrician wire it and the dimmer on the same visit.</li>
</ul>


<h2 class="pb">Power, cables and network</h2>
<h3>Sound layout</h3>
<ul>
<li><b>Subwoofer:</b> in bay 3, under the right of the TV, facing the sofa on a 5 cm riser, with 9.6 cm behind it for its port. Under the TV it blends with the soundbar; if the bass booms, turn it down rather than moving it.</li>
<li><b>Rear speakers</b> (9.1 × 14.5 × 10.9){ref("ax5100g")}: one each side of the sofa at about ear height, joined by a cable behind it along the skirting, with one socket for them.</li>
<li><b>Soundbar:</b> centred under the TV, pointing at the sofa.</li>
</ul>
<h3>Easy use and access</h3>
<ul>
<li>Disc trays, power buttons and front USB ports at the front edge of each bay.</li>
<li>Every drawer and tray runs on full-extension runners with a finger pull in the oak lip; no push-to-open at floor level. Open one record tray at a time.</li>
<li>Label each switched socket and each HDMI switch input with the same console name.</li>
<li>The controller basket beside the PS3 holds the TV and HDMI switch remotes; the pad charging dock sits on bay 3's shelf, powered from the USB charger.</li>
<li>Keep console bays open, or use cane or mesh fronts, so air and the HDMI switch remote both get through.</li>
</ul>

<h3>Cables, power and airflow</h3>
<ul>
<li><b>Service channel:</b> with the base 4 cm off the back wall, every cable drops through the 4 cm slot at the back of the worktop into flat two-compartment trunking: mains on one side, HDMI, Cat6 and audio on the other. Fit brush grommets at the back of each bay, and velcro-tie and label every cable.</li>
<li><b>To the TV:</b> it stands on the worktop, so its power, four HDMI leads (PC, Series X, HDMI switch, soundbar eARC) and Ethernet drop straight down behind it. No socket behind the TV is needed.</li>
<li><b>To Deco B:</b> a patch lead runs in slim corner trunking from the high shelf down to the 8-port switch. The switch is 15.8 × 10.1 × 2.5 cm, so it stands on its long edge in the 4 cm channel, or screws to the back of a frame by its wall-mount slots.</li>
<li><b>Power bricks:</b> the original Xbox 360 and Xbox One bricks sit on the free half of their console's row in bay 1, where air reaches them.</li>
<li><b>Turntable:</b> its leads drop through a grommet in the cabinet top, behind the deck, straight to the preamp in bay B; the preamp's output runs through the grommets low in the two end panels and along the data side of the trunking to the soundbar's AUX input. Keep them away from the power bricks and the sub's mains lead.</li>
<li><b>To Deco B:</b> the Cat6 from the top floor comes in through the ceiling in the alcove's right corner. Its 12 V lead and the patch lead to Switch 2 run along the back of the high shelf into the groove behind the right upright, down to the slot, and to an always-on socket of the 6-way at the back of bay 3. If the adapter's lead won't reach, add a DC extension with the same plug rather than a mains extension up at the shelf.</li>
<li><b>To the subwoofer:</b> its power lead runs along the channel to the always-on strip. Put felt or rubber pads where the worktop rests on its wall batten, so bass doesn't rattle it.</li>
<li><b>PC on the side wall:</b> HDMI and Cat6 drop through the shelf notch, down the trunking and along the skirting into the service channel. Over 3 m, use an active optical HDMI cable; these work one way round only, so the end marked "source" goes into the PC.</li>
<li><b>Power:</b> the wall socket on the side wall just in front of bay 1, swapped from a single to a double, feeds your 10-gang and the 6-way, one per socket, never one plugged into the other. You won't need to reach it day to day: the strips' own switches do that. See the power map below.</li>
<li><b>OLED care:</b> keep the TV on the always-on strip. It runs its pixel refresh while in standby, so don't switch it off at the wall.</li>
<li><b>Airflow:</b> no doors on the console bays (use mesh or slatted fronts if you want them), open backs, and at least 4 cm, ideally 10 cm, clear around the Series X.</li>
</ul>

<h3>Power map</h3>
<figure>{power()}</figure>
<ul>
<li><b>Where the 10-gang goes:</b> lying flat on the worktop behind the TV, switches up, with side B's switch at the left end. From the left, reach in through the 15 cm gap between the Series X and the TV. From the sofa, the soundbar and the TV's bottom edge hide it.</li>
<li><b>Leads up to it:</b> console leads rise through the slot behind the worktop; label each plug at the strip end.</li>
<li><b>The 6-way:</b> screwed to the back of bay 3, just under its shelf, so its switches are in reach; the deck and preamp leads run from it through the floor-level grommets into the cabinet.</li>
</ul>
<h3>Cable routes</h3>
<figure>{routes()}</figure>

<h3>The PC shelf</h3>
<p>A standard PC case has its glass window on its left side. With that glass facing the room, the front of the case points at the alcove and the back, with all its ports and leads, faces the sofa. The design hides that back without blocking the hot air leaving it, and parks the keyboard and mouse underneath.</p>
<figure>{pc_shelf()}</figure>
<ul>
<li><b>Layout on the shelf:</b> the shelf runs 65 cm along the wall and 32 cm out. The 45 cm-deep case sits 5 cm from the alcove end, leaving 13 cm behind it, then an oak frame with a woven cane panel at the sofa end, 26 cm wide and 48 cm tall, the height of the case.</li>
<li><b>Airflow:</b> the screen's top is open and the cane breathes, so the rear exhaust fan's air rises out of the 13 cm gap instead of being trapped. Keep the front (alcove end) and the glass side clear for intake.</li>
<li><b>Cables:</b> a 6 × 8 cm notch in the shelf's back corner, against the wall at the sofa end, with a brush grommet. Every lead (power, HDMI, Cat6) goes from the ports into a braided sleeve, through the notch, and down slim trunking painted the wall green to the skirting. A right-angle C13 power lead keeps the plug flat to the case.</li>
<li><b>Power:</b> ideally a socket under the shelf, added on the electrician's visit, so the PC's 500–850 W stays off the media wall strips. Then only HDMI and Cat6 travel along the skirting.</li>
<li><b>Keyboard and mouse tray:</b> build the shelf as a 9 cm-deep oak box: the shelf on top, and a 7 cm housing underneath with a tray on 300 mm light-duty runners that rolls 25 cm out towards the room. It holds a full-size wireless keyboard and mouse. The housing stops 12 cm short of the sofa end so the cables can drop past it. Pull it out, lift the keyboard onto your lap, and park it again after.</li>
<li><b>Fixing:</b> hang the box on a French cleat plus two steel brackets rated 25 kg or more; the PC weighs about 10–18 kg. Into masonry, use plugs and screws; on plasterboard, fix into studs or use heavy-duty cavity fixings rated for the load.</li>
</ul>

<h3>Living room AV</h3>
<p>The TV's four HDMI 2.1 ports cover everything. The PC and Series X get their own ports for 120Hz+ and VRR (the C6's 165Hz mode is for PCs), the soundbar takes eARC, and the other five consoles share HDMI 4 through a switch. The C6 has no analogue inputs, so the PS2 and PS1 go through the RetroTINK first.</p>
<figure>{av()}</figure>
<h4>How each source reaches the Hisense</h4>
<table class="tight"><tr><th>Source</th><th>Picture</th><th>Sound</th><th>Soundbar input</th></tr>
<tr><td>PC</td><td>TV HDMI 1</td><td>Via the TV over eARC</td><td>HDMI ARC</td></tr>
<tr><td>Xbox Series X</td><td>TV HDMI 3</td><td>Via the TV over eARC, 5.1 or Atmos</td><td>HDMI ARC</td></tr>
<tr><td>Xbox One, Xbox 360, PS3</td><td>HDMI switch → TV HDMI 4</td><td>Via the TV over eARC, 5.1</td><td>HDMI ARC</td></tr>
<tr><td>PS2</td><td>Component → RetroTINK → switch → TV</td><td>Optical, straight to the soundbar, 5.1 where the game has it</td><td>Optical</td></tr>
<tr><td>PS1</td><td>RGB SCART → RetroTINK → switch → TV</td><td>Stereo through the RetroTINK and the TV's eARC (no digital out)</td><td>HDMI ARC</td></tr>
<tr><td>Turntable</td><td>—</td><td>Preamp → AUX, straight in</td><td>AUX</td></tr>
<tr><td>Phone or tablet</td><td>—</td><td>Bluetooth, straight in</td><td>Bluetooth</td></tr>
<tr><td>TV apps</td><td>Built in</td><td>eARC</td><td>HDMI ARC</td></tr>
</table>
<p>The soundbar has no HDMI inputs, so anything with an HDMI lead has to reach it through the TV; eARC carries the full 5.1. Everything that can skip the TV does: vinyl on AUX, the PS2 on optical and phones on Bluetooth. Pick the input on the soundbar's remote when you switch to the deck or the PS2; it wakes by itself when a signal arrives. If PS2 sound ever runs slightly ahead of the picture, nudge the soundbar's audio delay or AV sync setting if it has one.</p>
<h4>TV and console settings</h4>
<ul>
<li>Rename each TV input, with HDMI 4 as "Retro", and turn on HDMI Ultra HD Deep Colour for HDMI 1, 3 and 4.</li>
<li>Use Game Optimiser on the console inputs for the lowest lag.</li>
<li>Set sound output to HDMI eARC, with digital audio on Auto or Passthrough.</li>
<li>Set the PS3, 360 and Xbox One to output 5.1 over HDMI.</li>
<li>On the PS3, turn off "Control for HDMI" so it doesn't grab the TV input.</li>
<li>For the PC at 4K above 120Hz, use a cable certified Ultra High Speed (48 Gbps), which includes the active optical one.</li>
</ul>
<h4>PS2 and retro on the 55-inch</h4>
<ul>
<li><b>Upscaler:</b> the RetroTINK-6X CE, $230 in the US; RetroTINK's international prices include VAT and import fees. Its motion-adaptive deinterlacing suits PS2 games, which mostly run interlaced, and it outputs up to 1440p for the TV to finish scaling to 4K.</li>
<li><b>Stock:</b> the September run sold out and the next restock is estimated for October to November, so order as soon as it's back.</li>
<li><b>Why not the 2X Pro:</b> RetroTINK now lists it as a legacy model, and it won't accept the 480p mode some PS2 games use.</li>
<li><b>Wiring:</b> component cable from the PS2 into the RetroTINK's rear RCA input for the picture, and a 2 m optical cable from the PS2 straight to the soundbar's optical input, which carries 5.1 in games that support it. The component lead's stereo plugs can still go to the RetroTINK as a fallback.</li>
<li><b>Power:</b> it comes with a USB-A to USB-C lead but no plug, and needs at least 5V 2A. Use a USB plug on its own switched socket of the 6-way, and switch it with side B.</li>
<li><b>PS2 settings:</b> set System Configuration → Component Video Out to Y Cb/Pb Cr/Pr, or you may get no picture. Turn the digital (optical) audio out on.</li>
<li><b>PAL games:</b> choose the 60 Hz mode when a game offers it at start-up, for smoother motion.</li>
<li><b>PS1:</b> an RGB SCART cable into the RetroTINK's SCART input. PS1 discs also play on the PS2 if you'd rather keep that console boxed.</li>
<li><b>Sharper still:</b> PCSX2 on the PC renders PS2 games at native 4K, with widescreen patches for many. Use your own discs and a BIOS copied from your own PS2.</li>
<li><b>Premium option:</b> the RetroTINK-4K CE ($475) outputs true 4K with the same processing, and a 6X Pro is due in the coming months. Only worth it if picture quality becomes a hobby.</li>
<li><b>OLED care:</b> 4:3 games leave black bars at the sides. Mix in full-screen viewing, and leave the TV in standby so it runs its pixel refresh.</li>
</ul>
<h4>Vinyl: through the soundbar, done properly</h4>
<ul>
<li><b>Setup:</b> slim turntable with a new stylus, set to PHONO → external phono preamp in the vinyl cabinet's bay B → soundbar AUX input, using an RCA-to-3.5 mm lead.</li>
<li><b>Check first:</b> the external preamp only helps if the deck has a PHONO/LINE switch. With no switch, its built-in preamp can't be bypassed, so skip the external one and plug the deck straight into the soundbar AUX.</li>
<li><b>Why the external preamp:</b> a slim deck's built-in preamp is its weakest part. A proper one gives fuller bass, clearer highs and less hiss.</li>
<li><b>Soundbar settings:</b> Music mode, bass up, and surround effects, night mode and dialogue mode off. Turn the sub down slightly from your film setting if bass gets boomy.</li>
<li><b>No Bluetooth:</b> always use the AUX cable, as Bluetooth loses quality.</li>
<li><b>Stylus:</b> buy the exact replacement for the deck's model, and set the tracking weight to the cartridge maker's figure.</li>
<li><b>Records:</b> clean them with a carbon-fibre brush before playing, and keep a few spare inner sleeves in bay B.</li>
</ul>
<h4>Upgrade path for vinyl</h4>
<p>Start with the soundbar route. Step up only if you want more. The old hi-fi and its built-in deck can be retired.</p>
<ol>
<li><b>Best for vinyl (about £200–450):</b> a stereo amp with phono input and sub output, the hi-fi's wired speakers, and a powered subwoofer. Fully analogue, loud and bassy. The Hisense sub can't be reused, as it only pairs with the soundbar.</li>
<li><b>Best for the whole room (about £500+):</b> an AV receiver with phono input and HDMI eARC, replacing the soundbar and driving real 5.1 speakers. Pure stereo for vinyl, proper surround for films.</li>
</ol>

<h3>The network</h3>
<figure>{network()}</figure>
<p>The hub feeds Deco A in bedroom 3, and Switch 1 sends a Cat6 run to each of the other Decos. In the living room, Deco B feeds Switch 2, which gives every networked console, the PC and the TV its own cable. Switch 1 keeps three spare ports: the projector in the master bedroom and the music room in bedroom 2 can each have a run on the same electrician visit.</p>
<ul>
<li><b>Run 1 to Deco B:</b> from bedroom 3 across the landing, down through the airing cupboard floor and the living room ceiling in the alcove's right corner, straight to Deco B on the high shelf; only a few cm show.</li>
<li><b>Run 2 to Deco C:</b> follows run 1 down the groove behind the right upright to the channel, then through the floor into the kitchen below, onto the outside of the brick cupboard, up high.</li>
<li><b>Lengths:</b> measure the real route and add 2–3 m; roughly 7–10 m for run 1 and 10–14 m for run 2.</li>
<li><b>Bedroom 2's Wi-Fi:</b> the slope makes it the weakest room upstairs. A wired port there lets a fourth Deco (or a wired desk) go on the high side later.</li>
</ul>
<h4>What each part does</h4>
<table><tr><th>Part</th><th>Job</th><th>Why it's needed</th></tr>
<tr><td>Virgin Hub 5, modem mode</td><td>Brings the internet into the house, nothing else</td><td>Stops two routers fighting (double NAT), which breaks Xbox online play. Its Wi-Fi switches off, so it no longer clutters the airwaves.</td></tr>
<tr><td>Deco A, top floor (main)</td><td>The router: runs the network, Wi-Fi, parental controls and HomeShield</td><td>Everything starts here. HomeShield and parental controls only work when the Deco is the router.</td></tr>
<tr><td>Switch 1, top floor, 8-port</td><td>Turns Deco A's one spare port into seven</td><td>Feeds both PCs plus the two cables down to the other floors, with three ports left for later.</td></tr>
<tr><td>Deco B, living room</td><td>Wi-Fi for the middle floor, and the wired point for the TV area</td><td>Fixes the 5GHz dead side of the living room.</td></tr>
<tr><td>Switch 2, living room, 8-port</td><td>Turns Deco B's spare port into seven</td><td>The Series X, Xbox One, Xbox 360, PS3, PC and TV each get a cable, with one port spare.</td></tr>
<tr><td>Deco C, kitchen</td><td>Wi-Fi for the bottom floor</td><td>The kitchen currently gets poor signal on every band.</td></tr>
<tr><td>Cat6 runs between floors</td><td>Wired link between Decos ("Ethernet backhaul")</td><td>Without it, Decos relay each other over the same 5GHz phones use, losing speed at each hop.</td></tr>
</table>
<h4>How to set it up</h4>
<p>The build runs in two stages: get the mesh working now, then add the cables between floors when they're run.</p>
<p><b>Stage 1: mesh up today (no cables between floors yet)</b></p>
<ol>
<li>Unplug everything from the hub. Log in at 192.168.0.1 with the password on its base, then choose Super Hub → Modem Mode → Enable Modem Mode → Apply Changes. Afterwards its settings page moves to 192.168.100.1.</li>
<li>Connect hub port 1 to Deco A and set it up in the Deco app, reusing the old Wi-Fi name and password. Virgin's guide doesn't name the port, so if the Deco shows no internet, try another port and restart the hub.</li>
<li>Plug the new 8-port Switch 1 into Deco A's other port, then both PCs into Switch 1.</li>
<li>Add Deco B on the living room's high shelf. Connect the 8-port switch to it, then the Series X, Xbox One, Xbox 360, PS3, PC and TV.</li>
<li>Add Deco C in the kitchen, on the side nearest the living room. For now it links over Wi-Fi.</li>
<li>Check the Xbox network settings show NAT: Open.</li>
</ol>
<p><b>Stage 2: add the Cat6 runs</b></p>
<ol>
<li>Run Cat6 from Switch 1 to Deco B, and a second run from Switch 1 straight to Deco C.</li>
<li>Plug each run into the Deco's free port. On Deco B, Switch 2 stays in the other port.</li>
<li>In the Deco app, confirm Deco B and Deco C show as "Ethernet".</li>
<li>Move each Deco to the centre of its floor for best coverage. They no longer need to see each other.</li>
<li>In the Deco app, give the Series X and PC high priority under QoS.</li>
</ol>
<h4>Cabling rules</h4>
<ul>
<li><b>Cable type:</b> solid pure-copper Cat6, round. Avoid "CCA" (copper-clad aluminium) and flat cable for long runs.</li>
<li><b>Length:</b> measure the actual route, not the straight line, and add 2–3 m spare. Anything under 100 m runs at full gigabit.</li>
<li><b>Routing:</b> go through the floor beside pipes, along skirting, or down an outside wall with outdoor-rated cable. Cross mains cables at right angles rather than running alongside them.</li>
<li><b>Separation:</b> in the media wall's service channel, mains goes in one compartment of the trunking and HDMI, Cat6 and the turntable leads in the other.</li>
<li><b>Handling:</b> no kinks or tight folds, never staple through the cable, and label both ends.</li>
<li><b>No loops:</b> never connect two cables between the same pair of devices. A loop can take the whole network down.</li>
</ul>
<div class="callout"><b>Done when</b><ul>
<li>Deco app shows Deco B and Deco C as "Ethernet"</li>
<li>Each PC's network status shows 1.0 Gbps (100 Mbps means a bad cable: swap it)</li>
<li>Xbox shows NAT: Open</li>
<li>Phones hold a strong signal in the kitchen and on both sides of the living room</li></ul></div>
<h4>Why we chose this option</h4>
<p>Wired where it matters, wireless everywhere else. The devices that need speed and stability are on cable, and the Wi-Fi is left free for phones.</p>
<ul>
<li><b>Wired gaming and streaming:</b> the Xboxes, PS3, TV and PCs get full gigabit with the lowest latency and no dropouts, whatever the walls or neighbours do.</li>
<li><b>Phones get uncrowded Wi-Fi:</b> with heavy users on cable, phones aren't competing with a 4K stream or game download.</li>
<li><b>Dual-band Decos need cables to shine:</b> the X1500 has no dedicated band for unit-to-unit traffic. Cabling the links gives every floor the same strength as the top floor.</li>
<li><b>Star layout:</b> each Deco has its own cable from the top floor, so the kitchen doesn't depend on the living room kit being on.</li>
<li><b>Switches cost nothing in speed:</b> every port runs at full speed at once, with no setup. They're simply extra ports, about £18–25 each.</li>
<li><b>Zones that match the kit above them:</b> the Xbox bay under the Series X, the PlayStation bay under the TV, and the records under the turntable, so cables stay short and everything lives where it's used.</li>
</ul>
<h4>Options we rejected</h4>
<table><tr><th>Option</th><th>Why not</th></tr>
<tr><td>Keep the Virgin hub as router, Decos in access point mode</td><td>Loses HomeShield and parental controls</td></tr>
<tr><td>All-wireless mesh</td><td>Works, but speed drops with each wireless hop, worst in the kitchen</td></tr>
<tr><td>Powerline adapters</td><td>Slower and less stable than Cat6; fallback only if cabling is impossible</td></tr>
<tr><td>2.5Gb switches</td><td>Decos and PCs top out at 1Gb, so no gain for the extra cost</td></tr>
<tr><td>Keeping the 5-port switch upstairs</td><td>Full on day one; any new device upstairs would need another switch</td></tr>
<tr><td>Plugging devices straight into Decos</td><td>Only one spare port per Deco: not enough for 2 PCs upstairs or 6 devices downstairs</td></tr>
<tr><td>Games upright, two lines deep</td><td>The back line is hidden and you pull out the front ones to reach it</td></tr>
<tr><td>Games lying flat in stacks</td><td>Hard to pick from, and long-term flat storage can bow discs in a warm room</td></tr>
<tr><td>Records on an open shelf in bay 1</td><td>Far from the deck, spines only, and too heavy for a BESTÅ shelf; the trays put them under the turntable with the art on show</td></tr>
<tr><td>Turntable in the alcove beside the TV</td><td>The real alcove is 186, not 225: the gap beside the uprights is 25 cm; see "Why this layout"</td></tr>
<tr><td>A green feature wall only</td><td>Leaves the alcove looking applied; the drench ties the room together</td></tr>
<tr><td>White skirting</td><td>Cuts a bright line round the room and breaks the drench; Card Room Green eggshell or a soft off-white sits better</td></tr>
<tr><td>A paper lantern for the ceiling</td><td>Replaced by the spotlight bar you chose: aimable light for the shelves, and it sits higher</td></tr>
<tr><td>Keeping the deep forest green</td><td>Still a good option for the darkest picture at night, but you asked for softer; the grey-green keeps the drench and feels lighter by day</td></tr>
<tr><td>Singles spine-up beside the LPs</td><td>Thinner trays free enough width to show them face-out too, and hold twice as many</td></tr>
<tr><td>Records spine-up in one drawer</td><td>Held slightly fewer and showed only a handful of covers; two face-out trays show every one</td></tr>
<tr><td>RetroTINK-2X Pro</td><td>Now a legacy model, won't accept 480p, and has simpler deinterlacing than the 6X CE</td></tr>
<tr><td>Cheap PS2-to-HDMI adapters</td><td>Soft, washed-out picture that a 55" OLED makes obvious</td></tr>
<tr><td>Bluetooth from the turntable</td><td>Compresses the sound; the AUX cable keeps full quality</td></tr>
</table>


<h2 class="pb">Build guide</h2>
<p>One sequence, from the electrician to the last lead. Sizes are finished sizes in cm. Walls are rarely square: measure the alcove at the floor, 76, 156, 200 and the ceiling, and cut the worktop and shelves to the smallest.</p>
<h3>Materials</h3>
<table class="tight"><tr><th>Element</th><th>Made from</th><th>Finished size</th><th>Fixing</th></tr>
<tr><td>Plinth (bays 1–2)</td><td>18 mm ply ladder frame</td><td>120 × 38 × 9</td><td>Shimmed level; frames screwed down onto it</td></tr>
<tr><td>Bays 1–2</td><td>2 × IKEA BESTÅ frame, back panels off</td><td>Each 60 × 40 × 64, tops at 73</td><td>Joined, 4 cm spacers to the wall, 2 anti-tip brackets each</td></tr>
<tr><td>Bay 3</td><td>18 mm birch ply, back open</td><td>60 × 40 × 73, shelf 56.4 × 38 at 40–41.8</td><td>On the floor, bolted to bay 2, 4 cm spacers, 2 anti-tip brackets</td></tr>
<tr><td>Fillers</td><td>Oak or ply</td><td>3 × 73, one each end</td><td>Scribed to the walls</td></tr>
<tr><td>Internal shelves</td><td>4 × BESTÅ shelf (20 kg each)</td><td>56 × 36</td><td>On pins at the fit-proof heights</td></tr>
<tr><td>Worktop</td><td>Solid oak, chamfered front</td><td>186 × 42 × 3, top at 76</td><td>Screwed up through the frame and carcass tops in slotted holes</td></tr>
<tr><td>Face frame</td><td>20 mm oak</td><td>186 × 73, with an 8 cm return beside the breast</td><td>Glued and pinned to the fronts</td></tr>
<tr><td>Uprights</td><td>Solid oak</td><td>159 × 30 × 4.5</td><td>Two 10 mm dowels into the worktop, two concealed brackets each into the back wall</td></tr>
<tr><td>High shelf, ledge, side shelves</td><td>Solid oak</td><td>see the joinery cut list</td><td>Housed and pegged / through-tenoned; cleats on the side walls</td></tr>
<tr><td>Hidden drawer</td><td>12 mm ply box, 20 mm oak front</td><td>Box 53.9 × 30 × 4.5; front 54.8 × 5.4</td><td>300 mm runners on bay 3's sides, just under its top</td></tr>
<tr><td>Vinyl cabinet</td><td>18 mm birch ply carcass, oak face frame and top</td><td>100 × 44 × 76</td><td>2 cm spacers over the skirting, 2 anti-tip brackets into the breast</td></tr>
<tr><td>Record trays</td><td>9 and 12 mm birch ply, oak dividers and lips</td><td>53.9 × 40 × 13.2</td><td>400 mm runners in bay A (see "The vinyl corner")</td></tr>
<tr><td>Game drawer</td><td>Birch ply, oak lip, 350 mm runners</td><td>Box 54.3 × 35 × 16.4</td><td>Runners on bay 1's sides</td></tr>
<tr><td>PC shelf box</td><td>27 mm oak top, 18 mm sides</td><td>65 × 32, 9 deep</td><td>French cleat plus 2 steel brackets (25 kg+)</td></tr>
</table>
<h3>Tools</h3>
<ul>
<li>Drill-driver and an SDS or hammer drill with masonry bits and plugs; spirit level or cross-line laser, tape, square, stud and cable detector.</li>
<li>Track or circular saw (or have the merchant cut the ply and oak), jigsaw, router with straight and cove bits, clamps, sander, wood glue.</li>
<li>For the joints: chisels (6, 12, 25 mm), marking gauge, tenon saw, 10 mm bit for the pegs, mallet.</li>
<li>Dust mask, eye and ear protection.</li>
</ul>
<h3>Order of work</h3>
<ol>
<li><b>Check and measure:</b> the alcove's width at five heights, plumb and level, the door's swing past the breast, your records and games.</li>
<li><b>Electrician (one visit):</b> Cat6 from bedroom 3 down through the airing cupboard (Deco B's through the ceiling in the alcove's right corner, Deco C's on to the kitchen), optional runs to the master and bedroom 2, the side-wall socket to a double, sockets by the sofa and under the PC shelf, the fused spur for the LED drivers, the spotlight bar and dimmer. Mark every route before painting.</li>
<li><b>Paint the room</b> in Card Room Green, skirting and door in eggshell, alcove and breast included; let it cure a few days.</li>
<li><b>Mark heights and lines:</b> 73 (worktop), 152 (side shelves' underside), 153 (ledge underside), 196 (high shelf underside), the uprights at 25.25–29.75 and 156.25–160.75 from the east wall, and the cabinet's outline on the breast.</li>
<li><b>Fix the cleats</b> for the shelf ends on the side wall and the reveal, level.</li>
<li><b>Build the plinth,</b> set it on 4 cm spacers, shimmed dead level.</li>
<li><b>Assemble the frames</b> (backs off), stand them on the plinth, join them and screw them down.</li>
<li><b>Build bay 3,</b> bolt it to bay 2 with its top level at 73, fit the fillers and anti-tip brackets on all three.</li>
<li><b>Fit the trunking</b> in the 4 cm channel, mains on one side and data on the other; stand Switch 2 on edge; run the cables in.</li>
<li><b>Fit the worktop:</b> scribe, oil all over (underside too), screw up through slotted holes. Fit the internal shelves at the fit-proof heights.</li>
<li><b>Fit the game drawer</b> in bay 1, the shelf, riser, sub and hidden drawer in bay 3.</li>
<li><b>Build the vinyl cabinet,</b> set it 2 cm off the breast and 2 cm clear of the reveal, fix it, drill the grommets in both end panels, hang both trays and check they run true empty.</li>
<li><b>Cut the joints and fit the oak:</b> dry-fit each upright with its shelves on the bench, lay the Deco leads in the right upright's groove, stand the uprights on their dowels, fix the brackets, then the shelves, ledge, wedges and pegs.</li>
<li><b>Fit the face frames</b> and the oak return, then the oak top on the cabinet; finish all the oak with hardwax oil.</li>
<li><b>Build and hang the PC shelf,</b> fit its screen and the trunking down to the skirting.</li>
<li><b>Lighting:</b> strips in the upright grooves to a driver on the fused spur, the ceiling strip through the uprights' notches, the bias light, then aim the spotlight bar and set the dimmer.</li>
<li><b>Place and connect:</b> TV, soundbar, Series X, deck, browser, LP frames; label every plug and HDMI input; test; then load the record trays one at a time.</li>
</ol>

<h2 class="pb">Buy list and tracker</h2>
<p>Every purchase and job, grouped by phase, comes to about £{money(tl, th)}, plus the electrician's quote. Tick items off and write in what you paid. Estimates are approximate UK prices; changed and new items are marked.</p>
<table class="tight"><tr><th>Phase</th><th>Estimate (£)</th><th>Biggest item</th></tr>{ptot}</table>
<p class="note">Already owned: Virgin Hub 5, three Deco X1500s, two TL-SG105S switches (both become spares), LG OLED C6 55" with its stand, a 10-gang extension with a switch per five-socket side, Hisense AX5100G soundbar with sub and rears, the Series X fan stand, the turntable and all the consoles.</p>
<table class="tracker"><thead><tr><th>Status</th><th>Item</th><th>Phase</th><th>Qty</th><th>Estimate (£)</th><th>Paid (£)</th></tr></thead><tbody>
{tracker_rows()}</tbody></table>

<h2 class="pb">Still to confirm</h2>
<ul class="checks">
<li class="done">Room: measured (your sketch): alcove 186 × 38, breast 117.5, ceiling 235, room 467 × 347.</li>
<li class="done">Main build: artisan oak; paint Card Room Green; skirting to match; spotlight bar; every record face-out.</li>
<li><b>The vinyl corner:</b> happy for the turntable and record trays to move to the oak cabinet on the chimney breast?</li>
<li><b>The door:</b> where it is and which side it hinges, so the cabinet's west end clears it; and the stair box figures (935, 1045, 660, 820, 130, 140) on the sketch.</li>
<li><b>Models:</b> the turntable, the PC case (window on its left?), the Series X fan stand (its footprint decides the left gap), and the 10-gang's length (it lies behind the TV, about 60 cm allowed).</li>
<li><b>The 23 × 22 box</b> in the window's west corner: pipe boxing, or something to keep clear?</li>
<li><b>Wired ports</b> for the projector (master) and the music room (bedroom 2)?</li>
<li>Socket height (drawn at about 30 cm) and its distance in front of the alcove.</li>
<li>Floor in the alcove and in front of the breast: carpet or hard floor? The plinth, bay 3 and the cabinet must sit level.</li>
<li>Side wall where the PC shelf goes: solid or plasterboard?</li>
<li>Records and games: roughly how many LPs, singles, and PS2 / Xbox 360 / Xbox One games? Most LPs in thick outer sleeves?</li>
<li>Turntable: a PHONO/LINE switch on the back (for the external preamp)?</li>
<li>Rear speakers: a socket near the sofa, and a route behind it for the link cable?</li>
<li>Deco B: does its adapter lead reach from the high shelf to bay 3 (about 2.2 m)?</li>
<li>Console model numbers, to tighten the row heights; the RetroTINK's size when it arrives.</li>
</ul>
<h2>Later ideas</h2>
<ul>
<li><b>Dave and Emma's watch log:</b> a shared movie and TV area, like a Spotify Blend for what you watch. Log each film or episode, mark whether you watched it together or one of you on your own, and give it a simple rating. It could live on the TV (a small web app on the LG's browser) or on your phones, and later suggest what to watch together next. First thought only; to be shaped up separately.</li>
</ul>

<h2>Sources</h2>
<p class="note">Numbered sources are cited in the fit proof and the text.</p>
<ol class="sources">
{source_list()}
</ol>
<ul class="sources">
<li>Virgin Media: Hub modem mode</li>
<li>RetroTINK-6X CE shop page (stock, power, box contents): retrotink.com/shop/retrotink-6x-ce</li>
<li>Introducing the RetroTINK-6X CE (inputs incl. TOSLINK, deinterlacing): retrotink.com/blog/introducing-the-retrotink-6x-ce</li>
<li>RetroTINK-2X Pro, listed as legacy; RetroTINK-4K CE</li>
<li>Expert Reviews: LG C6 OLED review (HDMI 2.1 ×4, one eARC, ports on the left): expertreviews.co.uk/technology/tvs-home-cinema/lg-c6-oled-review</li>
<li>JB Hi-Fi: LG C6 specifications (165Hz mode for PC sources)</li>
<li>Hisense AX5100G spec sheet (inputs, sub size, auto power-on): assets.hisense-usa.com</li>
<li>JB Hi-Fi Business: Hisense AX5100G (rears linked by cable, wireless to the soundbar)</li>
<li>IKEA: BESTÅ shelf 56×36 cm, max load 20 kg; BESTÅ frame, white stained oak effect</li>
<li>TP-Link Deco X1500 specifications (2 gigabit ports per unit)</li>
<li>Glorious Vinyl Vault specifications (80 LPs and 24.5 kg per drawer), a check on the face-out drawer capacity</li>
<li>Emuca: heavy-duty full-extension runners, 400 mm, 68 kg per pair</li>
<li>Game case sizes: videogamecasesize.info; coverstitch.io/dimensions; Walvis Products (Xbox 360 14 mm, Xbox One 11 mm cases); Wikipedia: Keep case</li>
<li>NIST SP 500-252 / CLIR pub121: Care and Handling of CDs and DVDs (store upright, book style)</li>
<li>Screwfix: Essentials 964VN 350 mm runners; Metrol: Accuride DZ3832EC; IKEA: BESTÅ drawer runners</li>
<li>Can-Am, mmdesign (DiscSox): spine-up media drawer capacities</li>
<li>Sony PS3 and Microsoft Xbox 360 S manuals: ventilation and disc storage; IKEA UK: secure it</li>
<li>Ideal Home: living room paint ideas (colour drenching, double drenching); The Paint Shed: colour drenching with Farrow &amp; Ball</li>
<li>Pontata: Card Room Green vs Little Greene Sage Green (approximate screen colours): pontata.com/compare/fb-card-room-green/lg-sage-green</li>
<li>Dunelm: Elements Wolston 4 Light Semi Flush Spotlight Bar (£49; 84 × 16 cm, 22.4 cm drop; E14, 6 W max; adjustable heads): dunelm.com/product/wolston-4-light-spotlight-bar-1000189449</li>
<li>Homebase and NC Tiles: Farrow &amp; Ball Card Room Green No. 79 in Modern Eggshell and Estate Eggshell</li>
<li>Haart Medway: floor plans and listing photos for the house (Portsmouth Close)</li>
<li>Livingetc: the best sage green paint shades, according to designers (Card Room Green, Treron, Sage Green, Green Smoke)</li>
<li>Wikipedia: Comparison of PlayStation consoles, Xbox One and Xbox Series X; Neowin: official Xbox 360 dimensions</li>
<li>Pure Xbox: Microsoft's Series X ventilation guidance; Xbox Support on clearance</li>
<li>Audio-Technica AT-LP120XUSB; TP-Link TL-SG108; ConsoleMods: PS2 Component Video Out setting</li>
</ul>


<h2 class="pb">Appendix: the slat wall</h2>
<p>Kept for reference, re-fitted to the real alcove. The base, the vinyl cabinet and every height are the same; above the worktop, oak slats on battens run from the worktop to the ceiling instead of the uprights, the shelves sit on hidden cleats, and the face frames are painted. Quicker to fit and good for sound, but it follows a trend; no ledge above the TV.</p>
<figure class="render">{img("render_v10_slat_clean.png", "Slat wall alternative")}</figure>
</body></html>
"""
    (HERE / "plan.html").write_text(html)
    print("totals", tl, th)


def pdf():
    from playwright.sync_api import sync_playwright
    footer = ('<div style="width:100%;font-family:Inter,sans-serif;font-size:8px;color:#8a867e;padding:0 18mm;'
              f'display:flex;justify-content:space-between"><span>Home Network &amp; Media Wall Plan · v{VERSION}</span>'
              '<span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>')
    with sync_playwright() as p:
        from shot import launch
        b = launch(p)
        pg = b.new_page()
        pg.goto((HERE / "plan.html").resolve().as_uri())
        pg.wait_for_timeout(500)
        pg.pdf(path=str(HERE.parent / "out" / f"Home_Network_Plan_v{VERSION}.pdf"), format="A4", print_background=True,
               margin={"top": "16mm", "bottom": "18mm", "left": "18mm", "right": "18mm"},
               display_header_footer=True, header_template="<div></div>", footer_template=footer)
        b.close()


if __name__ == "__main__":
    build()
    pdf()
    print("pdf ok")
