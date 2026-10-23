"""Builds the revised plan as HTML, then PDF via headless Chromium."""
import base64, pathlib
from diagrams import network, front, drawer, sound, game_drawer, av, power, routes, pc_shelf, section, joints, house, living_plan
PARTS = pathlib.Path(__file__).parent / 'parts'

HERE = pathlib.Path(__file__).parent

def img(name, alt=""):
    data = base64.b64encode((HERE / name).read_bytes()).decode()
    return f'<img src="data:image/png;base64,{data}" alt="{alt}">'

# ---------------------------------------------------------------- tracker data
# (status, item, phase, qty, lo, hi)  lo/hi None = no cost
TRACK = [
    ("To do", "Put the Virgin Hub 5 into modem mode", "Network", "", None, None),
    ("To do", "Set up Deco A, Switch 1 and both PCs", "Network", "", None, None),
    ("To do", "Add Deco B and C; speed-test each room and the Xbox", "Network", "", None, None),
    ("To buy", "Cat6 patch leads, 0.5–2 m", "Network", "11", 15, 20),
    ("To buy", "TP-Link TL-SG108 8-port switch: one for the living room, one to replace the 5-port upstairs <b>(new)</b>", "Network", "2", 36, 50),
    ("To do", "Book one electrician visit: both Cat6 runs plus a spare each (Deco B's through the ceiling in the alcove's right corner), swap the single socket on the side wall in front of bay 1 for a double (or move it 40 cm back into the alcove, behind the unit) <b>(changed)</b>, a socket by the sofa for the rear speakers if there isn't one, a socket under the PC shelf, a switched fused spur for the LED drivers, and an LED-compatible dimmer for the ceiling light <b>(new)</b>", "Cabling and power", "", None, None),
    ("To buy", "Cat6 solid pure copper, round (not CCA)", "Cabling and power", "2 runs", 30, 50),
    ("To buy", "6-way surge-protected extension with individually switched sockets, for Deco B, the 8-port switch, turntable, preamp and RetroTINK (your 10-gang takes the rest)", "Cabling and power", "1", 25, 40),
    ("To buy", "4-port USB charger, 5V 2A per port (HDMI switch, Xbox fan stand, controller dock)", "Cabling and power", "1", 10, 20),
    ("To buy", "USB plug, 5V 2A or more, for the RetroTINK on the switched strip <b>(new)</b>", "Cabling and power", "1", 5, 10),
    ("To buy", "Cable kit: brush grommets, velcro ties, labels, corner trunking", "Cabling and power", "1", 20, 30),
    ("To buy", "Two-compartment trunking for the service channel, about 2 m", "Cabling and power", "1", 10, 20),
    ("To buy", "Slim paintable trunking for the PC drop and skirting run, about 3 m", "Cabling and power", "1", 15, 30),
    ("To buy", "DC extension lead for the Deco adapter, if its lead won't reach down the upright's groove to the 6-way (match the plug)", "Cabling and power", "1", 5, 10),
    ("To buy", "PC tidy kit: braided sleeve, right-angle C13 power lead, shelf-notch grommet <b>(new)</b>", "Cabling and power", "1", 10, 20),
    ("To do", "Sample Farrow & Ball Card Room Green No. 79 on an A4 board; check by day and with the LED strip on <b>(changed)</b>", "Decorating", "", None, None),
    ("To buy", "Farrow & Ball Card Room Green No. 79: Estate (or Modern) Emulsion for walls, ceiling and alcove; Estate Eggshell for skirting, door, frame and trunking; primer/undercoat <b>(changed)</b>", "Decorating", "", 200, 500),
    ("To buy", "Woodwork primer, sanding pads and sugar soap for the white skirting and door <b>(new)</b>", "Decorating", "1", 20, 40),
    ("To do", "Paint the whole room, alcove included, before the unit goes in; skirting and door from white to Card Room Green eggshell", "Decorating", "", None, None),
    ("Done", "Check the alcove back wall for the shelf fixings (solid)", "Media wall", "", None, None),
    ("To do", "Check the left wall where the PC shelf goes: solid, or plasterboard on studs <b>(new)</b>", "Media wall", "", None, None),
    ("To buy", "Two IKEA BESTÅ 60×40×64 frames, white stained oak effect, for bays 1–2 <b>(changed: bay 3 is now custom)</b>", "Media wall", "2", 70, 200),
    ("To buy", "Plinth for bays 1–2: 18 mm ply ladder frame 120 × 38 × 9 cm, plus shims <b>(new)</b>", "Media wall", "1", 15, 30),
    ("To buy", "Bay 3 carcass: 18 mm birch ply cut to size (sides 73 × 40, top and bottom 56.4 × 40, two back rails), connector bolts <b>(new)</b>", "Media wall", "1", 60, 110),
    ("To buy", "Felt-lined battens for the worktop over the sub bay", "Media wall", "1", 5, 10),
    ("To buy", "BESTÅ shelves, 56 × 36 cm (20 kg max each), two each for bays 1 and 2", "Media wall", "4", 12, 32),
    ("To buy", "Anti-tip wall brackets and 10 cm spacer blocks for the two frames and the bay 3 carcass", "Media wall", "1 set", 15, 25),
    ("To buy", "Two face-out record tray kits: 12 mm and 9 mm birch ply cut to size, 6 mm oak dividers, 15 mm oak lips, raked rests, felt, two pairs of 400 mm runners rated 68–70 kg <b>(changed: thinner, singles face-out)</b>", "Media wall", "2", 150, 240),
    ("To do", "Measure about ten games of each kind (PS2, Xbox 360, Xbox One) before cutting the game drawer <b>(new)</b>", "Media wall", "", None, None),
    ("To buy", "Game drawer kit: 12 mm birch ply cut to size, 350 mm full-extension soft-close runners (35–49 kg), oak lip, follower block, felt <b>(new)</b>", "Media wall", "1", 50, 90),
    ("To buy", "Hidden cleats for the shelf ends on the side walls, 44 × 22 mm planed softwood, about 3 m", "Media wall", "1", 15, 25),
    ("To buy", "Bookends for the high shelf <b>(new)</b>", "Media wall", "2", 10, 20),
    ("To buy", "Lidded box for cables and controllers on the high shelf", "Media wall", "1", 10, 20),
    ("To buy", "LP browser for the worktop under the deck: oak base, low front rail and side, 44 × 24 cm", "Media wall", "1", 30, 60),
    ("To buy", "Kit shelf over the sub: oak or ply 44 × 30 cm on battens, top at 38.8 cm, with rubber pads", "Media wall", "1", 15, 30),
    ("To buy", "Hidden slim drawer under the worktop in the sub bay: oak front 44 × 7.4 cm, 12 mm ply box 40 × 28 × 6 cm, 250 mm full-extension runners <b>(new)</b>", "Media wall", "1", 25, 45),
    ("To buy", "PC shelf rebuilt as a box with a keyboard and mouse tray: oak, 300 mm light runners, French cleat <b>(new)</b>", "Media wall", "1", 25, 50),
    ("To buy", "Oak for the PC shelf box: 27 mm top 65 × 32, 18 mm sides; French cleat and 2 steel brackets rated 25 kg+", "Media wall", "1", 30, 70),
    ("To buy", "Compact isolation riser for the sub (about 30 × 35 cm, 4–6 cm tall), plus isolation feet for the turntable", "Media wall", "1", 30, 60),
    ("To do", "Build the plinth and bay 3 carcass, fix everything to the wall; set rows to the fit check heights; fit the game drawer and both record trays; place the TV, soundbar, Series X and sub", "Media wall", "", None, None),
    ("To buy", "5-in-1 4K60 HDMI switch, auto-switching, with remote", "TV and consoles", "1", 20, 35),
    ("To do", "Measure the PC-to-TV cable route (estimated 4–5 m)", "TV and consoles", "", None, None),
    ("To buy", "Active optical HDMI cable for the PC, certified Ultra High Speed (48 Gbps), about 5–7.5 m", "TV and consoles", "1", 20, 60),
    ("To buy", "High Speed HDMI leads, 1–2 m", "TV and consoles", "5", 20, 30),
    ("To buy", "RetroTINK-6X CE upscaler for the PS2 and PS1 (order on restock; UK price includes VAT and import fees)", "TV and consoles", "1", 200, 240),
    ("To buy", "PS2 component video cable, good quality", "TV and consoles", "1", 10, 20),
    ("To buy", "Optical (TOSLINK) cable, 2 m, PS2 straight to the soundbar", "TV and consoles", "1", 5, 10),
    ("To buy", "RGB SCART cable for the PS1", "TV and consoles", "1", 8, 15),
    ("To do", "Connect the TV inputs; set up the PS2 and RetroTINK", "TV and consoles", "", None, None),
    ("To buy", "Replacement stylus for the slim turntable", "Vinyl", "1", 15, 40),
    ("To buy", "External phono preamp (only if the deck has a PHONO/LINE switch)", "Vinyl", "1", 40, 100),
    ("To buy", "RCA-to-3.5 mm lead", "Vinyl", "1", 5, 10),
    ("To buy", "Carbon-fibre record brush", "Vinyl", "1", 10, 15),
    ("To do", "Set tracking weight and soundbar Music mode", "Vinyl", "", None, None),
    ("To do", "Turn on HDMI-CEC (SIMPLINK); PS3 Control for HDMI off", "Finishing", "", None, None),
    ("To do", "Deco app: prioritise Series X and PC, guest Wi-Fi, auto firmware", "Finishing", "", None, None),
    ("To do", "Label each switched socket and HDMI switch input with the console's name", "Finishing", "", None, None),
    ("To do", "Set the sub and rear speaker levels from the sofa", "Finishing", "", None, None),
    ("To buy", "Two solid oak uprights, 150 × 30 × 4.5 cm, quarter-sawn if possible <b>(new: main plan)</b>", "Oak joinery and lighting", "2", 150, 300),
    ("To buy", "Solid oak for the shelves: high shelf in three lengths (128.9, 45.7, 46.2 × 30 × 4), left shelf 51 × 25 × 4, turntable shelf 51.5 × 45 × 4, record ledge 128.9 × 7 × 2.4", "Oak joinery and lighting", "1 set", 200, 350),
    ("To buy", "Oak wedges, 10 mm oak dowel for pegs and dowels, concealed upright brackets", "Oak joinery and lighting", "1", 15, 30),
    ("To buy", "Solid oak worktop, full stave, cut to 225 × 40 × 3 cm, chamfered edge (the offcut makes the LP browser base)", "Oak joinery and lighting", "1", 200, 400),
    ("To buy", "Oak face frame, 20 mm, stiles and rails", "Oak joinery and lighting", "1", 80, 180),
    ("To buy", "Cane screen for the PC: oak frame and pre-woven cane, 26 × 48 cm", "Oak joinery and lighting", "1", 20, 40),
    ("To buy", "LED for the upright grooves: 2700K strip, two aluminium channels, driver; 6500K bias light for the TV", "Oak joinery and lighting", "1", 40, 90),
    ("To buy", "Ceiling light: Dunelm Elements Wolston 4-light spotlight bar (£49), in the multicoloured style, plus four warm-white (2700K) dimmable E14 LED bulbs, 6 W max <b>(changed)</b>", "Oak joinery and lighting", "1", 60, 80),
    ("To buy", "Later: aluminium channel and opal diffuser for the existing ceiling LED strip (optional)", "Oak joinery and lighting", "1", 0, 80),
    ("To do", "Cut the joints, fit the uprights, shelves, ledge and face frame, notch the uprights for the ceiling strip, and wire the LEDs (see the build guide)", "Oak joinery and lighting", "", None, None),
]
PHASES = ["Network", "Cabling and power", "Decorating", "Media wall", "TV and consoles", "Vinyl", "Oak joinery and lighting"]
BIGGEST = {"Oak joinery and lighting": "solid oak worktop and shelves", "Network": "two 8-port switches", "Cabling and power": "Cat6 cable and trunking", "Decorating": "paint",
           "Media wall": "record trays and the bay 3 carcass", "TV and consoles": "RetroTINK-6X CE", "Vinyl": "phono preamp"}

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
    for st, item, ph, q, lo, hi in TRACK:
        box = "☑" if st == "Done" else "☐"
        est = money(lo, hi) if lo is not None else ("Quote" if "electrician" in item else "")
        out.append(f"<tr><td class='st'>{box} {st}</td><td>{item}</td><td>{ph}</td><td class='num'>{q}</td><td class='num'>{est}</td><td class='paid'></td></tr>")
    return "\n".join(out)

UPGRADE = [("Oak acoustic slat panels, 4 × 240 × 60 cm (one bought early for the PC screen)", 200, 320), ("Battens 25 × 50 mm (about 14 m), fixings and adhesive", 30, 60),
           ("MDF face frame and filler strips, primed and finished in the room's soft green eggshell", 60, 150),
           ("LED strips, aluminium channels, drivers and bias light, including under the PC shelf", 60, 140),
           ("Cane or mesh fronts for the two console bays (optional)", 0, 270)]

def upgrade_rows():
    lo = sum(u[1] for u in UPGRADE); hi = sum(u[2] for u in UPGRADE)
    rows = "\n".join(f"<tr><td>{a}</td><td class='num'>{money(b, c)}</td></tr>" for a, b, c in UPGRADE)
    rows += f"<tr class='total'><td>Total</td><td class='num'>about {money(lo, hi)}, plus any electrician work</td></tr>"
    return rows, lo, hi


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
    urows, ul, uh = upgrade_rows()
    css = (HERE / "doc.css").read_text()
    html = f"""<!doctype html><html><head><meta charset="utf-8"><title>Home Network &amp; Media Wall Plan</title>
<style>{css}</style></head><body>

<h1>Home Network &amp; Media Wall Plan</h1>
<p class="byline">Revised Oct 18, 2026 · @emma · version 9</p>

<h2>The plan</h2>
<p>One plan for the whole house: a three-unit Deco mesh wired by Cat6, and a built-in media wall in the 225 × 220 cm living room alcove, set in a room painted top to bottom in Farrow &amp; Ball Card Room Green. The Virgin Hub 5 becomes a plain modem and the main Deco takes over as router. The PC and Series X plug straight into the LG C6, and every other console shares one input through an HDMI switch. A RetroTINK upscaler makes PS2 games look their best on the 55-inch screen. Every LP and most singles are face-out, in two pull-out trays, a browser under the turntable and a ledge above the TV, and games live in a roll-out drawer with every title visible. It all costs about £{money(tl, th)} plus the electrician, tracked item by item below. Above the worktop, solid oak uprights carry the shelves on joints left on show, with warm light from the ceiling strip, the uprights and a paper lantern; the slat wall is kept as the alternative.</p>

<h3>Recommendations at a glance</h3>
<table><tr><th>Area</th><th>Recommendation</th><th>Why</th></tr>
<tr><td>Internet</td><td>Virgin Hub 5 in modem mode; Deco A becomes the router</td><td>One router: Open NAT for the Xbox, and HomeShield and parental controls work</td></tr>
<tr><td>Mesh</td><td>One Deco per floor, each wired back to an 8-port Switch 1 by Cat6</td><td>Full speed on every floor; dual-band Decos slow down over wireless hops</td></tr>
<tr><td>Living room network</td><td>8-port switch wiring the Series X, Xbox One, Xbox 360, PS3, PC and TV</td><td>Lowest lag for games, phones get the Wi-Fi to themselves, one port spare</td></tr>
<tr><td>Room colour</td><td>Colour-drench the room in Farrow &amp; Ball Card Room Green No. 79: matt walls and ceiling, the same colour in Estate Eggshell on the skirting (now white), door and trunking</td><td>The media wall becomes part of the room; a soft grey-green that lets the oak and the records lead</td></tr>
<tr><td>Lighting</td><td>Keep the LED strip round the ceiling (upgrade to a diffused channel later), LED grooves in the oak uprights, and a four-head cone spotlight bar on the existing ceiling rose, all 2700K and dimmable</td><td>Warm, layered light that suits the hand-made oak and keeps glare off the OLED</td></tr>
<tr><td>TV inputs</td><td>HDMI 1 PC, HDMI 2 soundbar (eARC), HDMI 3 Series X, HDMI 4 five-way switch</td><td>PC and Series X keep 120Hz+ and VRR; every other console shares one input</td></tr>
<tr><td>PS2 and PS1</td><td>RetroTINK-6X CE: PS2 by component and optical, PS1 by RGB SCART, powered with the retro consoles</td><td>Motion-adaptive deinterlacing keeps PS2 games clean on a 55" OLED; optical carries 5.1 where games have it</td></tr>
<tr><td>Vinyl</td><td>New stylus; turntable → phono preamp (on a shelf over the sub) → soundbar AUX, in Music mode; about 230 LPs, every one face-out, and about 310 singles: two thinner trays in bay 3, a browser under the deck and a ledge above the TV</td><td>Biggest sound gain for the money, and the collection is on display right where you play it</td></tr>
<tr><td>Media wall</td><td>Artisan oak: two solid oak uprights with pegged and through-tenoned shelves above a solid oak worktop at 76 cm; below, two BESTÅ frames on a 9 cm plinth, a ply bay for the records and an open sub bay behind one oak face frame. Xbox bay left with a roll-out game drawer, PlayStation bay centre, vinyl bay right with two face-out record drawers</td><td>Every console fits even at its largest version, each zone sits under the kit it belongs to, and every game title and record cover is visible</td></tr>
<tr><td>Sound</td><td>Sub in the alcove's right corner facing the sofa; soundbar centred; rears either side of the sofa, linked by a cable behind it</td><td>A corner gives the most bass; the surround is built around the seats opposite the TV</td></tr>
<tr><td>Power</td><td>The low socket on the side wall in front of bay 1 becomes a double: your 10-gang behind the TV (side A left on, side B the retro switch) and a 6-way with a switch per socket, which keeps Deco B always on</td><td>Retro gear fully off between sessions; the TV stays in standby for OLED care</td></tr>
<tr><td>PC</td><td>Oak wall shelf on the left wall, glass to the room, back screened by an oak frame with woven cane, keyboard tray underneath; active optical HDMI cable for the 4–5 m route</td><td>On show without losing 4K at 120Hz+, and no cable mess facing the sofa</td></tr>
<tr><td>Sound</td><td>Every source plays through the Hisense: HDMI sources via the TV's eARC, vinyl, PS2 and phones straight in</td><td>One volume control and full 5.1 wherever a source has it</td></tr>
</table>

<h3>Build tracker</h3>
<p>Every purchase and job in build order comes to about £{money(tl, th)}, plus the electrician's quote. Tick items off as you go and write in what you paid. Estimates are approximate UK prices. New items are marked.</p>
<table class="tight"><tr><th>Phase</th><th>Estimate (£)</th><th>Biggest item</th></tr>{ptot}</table>
<p class="note">Already owned: Virgin Hub 5, three Deco X1500s, two TL-SG105S switches (both become spares), LG OLED C6 55" with its stand, a 10-gang extension with a switch per five-socket side, Hisense AX5100G-class 5.1 soundbar, the Series X fan stand, the slim turntable and all the consoles.</p>
<table class="tracker"><thead><tr><th>Status</th><th>Item</th><th>Phase</th><th>Qty</th><th>Estimate (£)</th><th>Paid (£)</th></tr></thead><tbody>
{tracker_rows()}</tbody></table>

<h2 class="pb">Network</h2>
<figure>{network()}</figure>
<p>The hub feeds Deco A, and Switch 1 sends a Cat6 run down to each of the other Decos. In the living room, Deco B feeds the 8-port switch, which gives every networked console, the PC and the TV its own cable. Each Deco X1500 has two gigabit ports, so one takes the incoming cable and the other feeds the switch.</p>
<h3>Around the house</h3>
<figure>{house()}</figure>
<ul>
<li><b>Deco A and Switch 1</b> stay upstairs with the Hub 5 and both PCs. Both Cat6 runs go to the airing cupboard on the landing, which sits right over the media wall's right-hand corner, and drop through its floor, often beside the existing pipes.</li>
<li><b>Run 1 to Deco B</b> comes down through the living room ceiling in the alcove's right corner, straight to Deco B on the high shelf. Only a short length shows, between the ceiling and the shelf.</li>
<li><b>Run 2 to Deco C</b> follows run 1 down the groove behind the right upright to the cable channel, then through the floor into the kitchen below, where the brick cupboard sits under the chimney breast. Fix Deco C on the outside of the cupboard, up high on the kitchen side: inside the brick it would lose much of its Wi-Fi.</li>
<li><b>Lengths:</b> roughly 6–9 m for run 1 and 9–13 m for run 2, depending on where the Hub 5 is; measure the real route and add 2–3 m to each.</li>
<li><b>Sloped ceilings:</b> the bathroom and bedroom 2 slope down towards the back wall. Keep any Deco, switch or desk in bedroom 2 on the high side, and run cables along the floor there, not the ceiling.</li>
</ul>
<h3>What each part does</h3>
<table><tr><th>Part</th><th>Job</th><th>Why it's needed</th></tr>
<tr><td>Virgin Hub 5, modem mode</td><td>Brings the internet into the house, nothing else</td><td>Stops two routers fighting (double NAT), which breaks Xbox online play. Its Wi-Fi switches off, so it no longer clutters the airwaves.</td></tr>
<tr><td>Deco A, top floor (main)</td><td>The router: runs the network, Wi-Fi, parental controls and HomeShield</td><td>Everything starts here. HomeShield and parental controls only work when the Deco is the router.</td></tr>
<tr><td>Switch 1, top floor, 8-port</td><td>Turns Deco A's one spare port into seven</td><td>Feeds both PCs plus the two cables down to the other floors, with three ports left for later.</td></tr>
<tr><td>Deco B, living room</td><td>Wi-Fi for the middle floor, and the wired point for the TV area</td><td>Fixes the 5GHz dead side of the living room.</td></tr>
<tr><td>Switch 2, living room, 8-port</td><td>Turns Deco B's spare port into seven</td><td>The Series X, Xbox One, Xbox 360, PS3, PC and TV each get a cable, with one port spare.</td></tr>
<tr><td>Deco C, kitchen</td><td>Wi-Fi for the bottom floor</td><td>The kitchen currently gets poor signal on every band.</td></tr>
<tr><td>Cat6 runs between floors</td><td>Wired link between Decos ("Ethernet backhaul")</td><td>Without it, Decos relay each other over the same 5GHz phones use, losing speed at each hop.</td></tr>
</table>
<h3>How to set it up</h3>
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
<h3>Cabling rules</h3>
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

<h2 class="pb">Media wall proposal</h2>
<p>The main plan is now the artisan oak build: oak used as furniture and joinery against a wall painted in Farrow &amp; Ball Card Room Green. Below the worktop is one full-width unit: bays 1 and 2 are IKEA BESTÅ 60×40×64 frames on a 9 cm plinth, bay 3 is a custom plywood carcass with two face-out record trays, and the 45 cm bay at the right stays open for the subwoofer, all behind one oak face frame under a 3 cm solid oak worktop at 76 cm. Above it, two solid oak uprights frame the TV and carry the shelves on joints left on show: wedged through-tenons, pegged housings and a record ledge above the screen. Each bay holds one family: Xbox under the Series X, PlayStation under the TV, vinyl under the turntable. Every console fits even at its largest version, every record and single is face-out, and every cable drops into a hidden channel.</p>
<figure class="render">{img("render_v8_join_key_scene.png", "Render with numbered parts")}
<figcaption>The artisan oak media wall in Farrow &amp; Ball Card Room Green, drawn to the real measurements in a one-point perspective, with the game drawer and the lower record tray rolled out 30 cm and an inset of each from above. The view now takes in the ceiling: the existing LED strip round the room's edge and the new spotlight bar on the existing rose. Dashed lines show what's hidden: gold for Deco B's leads and the 10-gang, coral for mains from the double socket on the side wall. The numbers match the key below.</figcaption></figure>
{key_table()}
<figure class="render">{img("render_v8_join_clean.png", "Render, drawers closed")}
<figcaption>The same view with every drawer closed. The front covers of the two game bins, the front LP and single in each record tray, the browser's front record and the four LPs on the ledge stay on show. Full-resolution copies of both renders come with this plan.</figcaption></figure>

<h3>Built to your alcove: 225 cm wide, 50 cm deep, floor to ceiling (220 cm)</h3>
<ul>
<li><b>Bays 1 and 2:</b> two BESTÅ frames, each 60 × 40 × 64 cm, stand on a 9 cm plywood plinth, so their tops are at 73 cm. Back panels off. The oak face frame's bottom rail covers the plinth, so it never shows.</li>
<li><b>Bay 3:</b> a custom carcass in 18 mm birch ply, 60 × 40 × 73 cm, standing on the floor with its top level with the frames. Inside it is 56.4 cm wide and 69.4 cm tall: exactly two face-out tiers of 34.7 cm. The drawer runners screw straight into the ply sides, so it needs no liners.</li>
<li><b>Fixing:</b> the frames and carcass are bolted to each other, stand 10 cm off the back wall on spacer blocks, and are fixed to it with anti-tip brackets. With two trays of about 32 kg each, the anti-tip brackets on bay 3 are essential, and only one record tray should be open at a time.</li>
<li><b>Worktop:</b> solid oak, full stave or wide board, 225 × 40 × 3 cm with a chamfered front edge, flush with the fronts, top at 76 cm. The 10 cm left open behind it is the slot for cables and rising warm air.</li>
<li><b>Oak uprights:</b> two, 4.5 × 30 cm, from the worktop to the ceiling at 44.5–49 and 175.5–180 cm from the left wall, about 2 cm clear of the TV each side. They carry the high shelf, the record ledge, the left shelf and the turntable shelf (see "The oak joinery").</li>
<li><b>Power:</b> everything runs from the wall socket on the side wall just in front of bay 1, about 30 cm up, swapped from a single to a double: one socket for your 10-gang behind the TV, one for the 6-way at the back of the sub bay. The two leads drop to the floor, enter the unit through a small notch at the left end of the face frame's bottom rail, run back through the plinth and along the mains side of the channel. If the electrician is changing the socket anyway, moving it about 40 cm back into the alcove, behind bay 1, hides it and the plugs completely.</li>
<li><b>Inside bays 1 and 2:</b> about 56.8 cm wide, 38–40 cm deep with the back open, and 60.8 cm high, exactly as before: every row and console just sits 9 cm higher. The game drawer's base is now 11.6 cm off the floor, easier to reach.</li>
<li><b>Matching fronts:</b> the game drawer and both record trays have oak lips with a hand-cut finger pull (6.5 cm on the game drawer, a slimmer 5 cm on the record trays), so the bottom of the unit reads as one sideboard, with covers on show in each.</li>
<li><b>TV:</b> on LG's own stand (base 47 × 23 cm), set towards the back of the worktop. The bottom of the screen is about 5.4 cm above the worktop (about 81.4 cm), its centre at about 116.5 cm and its top just under the record ledge. The C6's HDMI ports are on the left as you face it, the same side as the Series X and the PC's cable.</li>
<li><b>Soundbar:</b> about 92 × 9 × 6 cm at the front edge, 8 cm in front of the TV stand. From the sofa you look down over it, so it stays below the picture, and the TV's remote sensor still works.</li>
<li><b>Series X:</b> upright on its fan stand at the left end of the worktop, about 15 cm from the wall and the TV. Console and stand stand about 37 cm tall (to 112.4 cm), with open air above.</li>
<li><b>Turntable:</b> on a 45 cm-deep oak shelf with its top at 113 cm in the right-hand gap, big enough for a deck as large as the Audio-Technica AT-LP120X (45 × 35 cm). It is carried by a wedged through-tenon in the right upright and a hidden cleat on the right-hand wall, clear of the unit below. Keep about 40 cm clear above the deck: the lid opens to about 165 cm.</li>
<li><b>LP browser:</b> on the worktop under the turntable shelf, 33 cm clear (worktop 76 to the shelf's underside at 109). A 31.4 cm sleeve leaning back 10° stands about 31.7 cm on the browser's base, leaving 1.3 cm. At 44 × 24 cm, clear of the right upright, it holds about 50 LPs face-out, about 13 kg, which the worktop carries over the sub bay.</li>
<li><b>Sub bay:</b> open from the floor. The sub stands on a 5 cm riser (its top at 34.4 cm) under a kit shelf with its top at 38.8 cm. The shelf holds the preamp, spare stylus, cleaning kit and brush on the left and about 70 singles spines-out on the right, with 26.8 cm clear up to the hidden drawer.</li>
<li><b>Hidden slim drawer:</b> under the worktop in the sub bay, an oak front 44 × 7.4 cm (65.6–73 cm) with a finger pull underneath, on a ply box 40 × 28 × 6 cm and 250 mm runners. Remotes, batteries, styli, spare cables.</li>
<li><b>PC:</b> on an oak wall shelf about 65 × 32 cm, top at 110 cm, on the left wall about 1.3–2 m forward of the alcove, glass to the room, the back ports towards the sofa behind an oak frame with a woven cane panel, keyboard tray underneath. See "The PC shelf".</li>
<li><b>High shelf:</b> solid oak, 30 × 4 cm in three lengths housed into the uprights, top at 192 cm, wall to wall, with 28 cm to the ceiling: books up to 26 cm, a box for cables, a print and Deco B. The left shelf sits at 156 cm and the record ledge at 155.4 cm.</li>
<li><b>Deco B, powered:</b> on the right end of the high shelf. The Cat6 from the top floor comes in through the ceiling in the corner; its 12 V lead and the patch lead down to Switch 2 run along the back of the shelf into a groove routed in the back of the right upright, down to the cable slot and on to an always-on socket of the 6-way. Its light shows solid green once it's online.</li>
</ul>
<figure>{front()}</figure>
<figure>{living_plan()}</figure>
<p><b>From the sofa:</b> with the sofa against the window wall, your eyes are about 2.7–3.2 m from the screen, depending on whether the agent's 3.65 m runs to the chimney breast or to the back of the alcove. At that distance the TV's centre at 116.5 cm is about 2° above a seated eye line, which is comfortable. A 55-inch screen fills about 22–25° of your view: fine for TV and games, on the small side for films, and the most that fits between the oak uprights (a 65-inch is about 145 cm wide, the gap is 126.5). The sofa will sit in front of the radiator under the window, so leave a 10 cm gap behind it.</p>

<h3>Why the unit is 76 cm tall</h3>
<p>Two face-out drawers stacked need more height than a BESTÅ frame has inside, and the worktop has to stay level across the alcove because the TV spans bays 1 to 3. So the whole unit goes up 9 cm, from 67 to about 76 cm.</p>
<table class="tight"><tr><th>One face-out tier</th><th>cm</th></tr>
<tr><td>Gap under the box</td><td>0.5</td></tr>
<tr><td>Drawer base</td><td>1.8</td></tr>
<tr><td>12-inch sleeve leaning back 10° (31.4 × cos 10°)</td><td>30.9</td></tr>
<tr><td>Finger room above</td><td>1.5</td></tr>
<tr class="total"><td>One tier · two tiers · carcass with 18 mm top and bottom</td><td>34.7 · 69.4 · 73.0</td></tr>
</table>
<p><b>The trade-off:</b> the TV's centre is about 116.5 cm instead of 108, about 2° higher from the sofa. That still sits close to seated eye height, the soundbar in front stops it going any lower even on a wall mount, and in return every record in the wall is face-out (about 230 LPs and 310 singles). Once the floor plan gives the sofa distance, the plan will confirm the viewing angle.</p>

<h3>Fit check, sized for the largest version of each console</h3>
<table class="tight"><tr><th>Zone</th><th>What goes there</th><th>Space (W × D × H, cm)</th><th>Largest version (cm)</th><th>Spare</th></tr>
<tr><td>Worktop, left</td><td>Series X on its fan stand</td><td>51 wide, open above</td><td>20.5 × 20.5 footprint, 37 tall</td><td>About 15 cm each side</td></tr>
<tr><td>Worktop, centre</td><td>TV on LG's stand at the back, soundbar at the front edge</td><td>122 wide, 40 deep</td><td>Stand base 47 × 23; soundbar 92 × 9 × 6</td><td>8 cm spare in depth</td></tr>
<tr><td>Worktop, right</td><td>LP browser under the turntable shelf</td><td>44 × 24 × 33</td><td>LP sleeve 31.4, about 31.7 tall leaning on the base</td><td>1.3 cm above; about 50 LPs</td></tr>
<tr><td>Oak shelf, right</td><td>Turntable, shelf top at 113</td><td>45 × 45, 40 clear above</td><td>AT-LP120X: 45 × 35 × 14</td><td>Just fits; most decks are 42–43 wide</td></tr>
<tr><td>Bay 1, top row</td><td>Xbox One and its power brick</td><td>56 × 40 × 16</td><td>One original: 33.3 × 27.4 × 7.9</td><td>8.1 above; 23 beside for the brick</td></tr>
<tr><td>Bay 1, middle</td><td>Xbox 360 and its power brick</td><td>56 × 40 × 16</td><td>360 original: 30.9 × 25.8 × 8.3</td><td>7.7 above; 25 beside for the brick</td></tr>
<tr><td>Bay 1, bottom</td><td>Roll-out game drawer</td><td>56 × 40 × 25.2</td><td>PS2/360 case 19 × 13.5 × 1.4; leaning in a bin about 18.5 tall</td><td>About 3 cm above the bins; about 48 games</td></tr>
<tr><td>Bay 2, top row</td><td>PS3 and a controller basket</td><td>56 × 40 × 23.7</td><td>PS3 original: 32.5 × 27.4 × 9.8</td><td>13.9 above; 24 beside</td></tr>
<tr><td>Bay 2, middle</td><td>PS2, HDMI switch at the front edge</td><td>56 × 40 × 16.5</td><td>PS2 original: 30.2 × 18.3 × 7.8</td><td>8.7 above; 26 beside</td></tr>
<tr><td>Bay 2, bottom</td><td>PS1 and RetroTINK</td><td>56 × 40 × 17</td><td>PS1 27 × 18.8 × 6; RetroTINK up to 23 × 23 × 8</td><td>9 above; 6 beside</td></tr>
<tr><td>Bay 3, upper tray</td><td>LPs face-out leaning 10°, 7-inch singles face-out beside them</td><td>56.4 × 40 × 34.2 (37.0 to 71.2)</td><td>LP sleeve 31.4, 30.9 tall leaning; single 18.3, 18.0 tall</td><td>2.1 cm above; about 90 LPs + 120 singles</td></tr>
<tr><td>Bay 3, lower tray</td><td>The same</td><td>56.4 × 40 × 35.2 (1.8 to 37.0)</td><td>The same</td><td>2.6 cm to the upper tray; about 90 LPs + 120 singles</td></tr>
<tr><td>Sub bay, upper</td><td>Kit shelf: preamp, stylus, cleaning kit, brush, spare inner sleeves; singles spines-out</td><td>44 × 30, 26.8 high</td><td>7-inch sleeve 18.3; cleaning kit about 12</td><td>8.5 cm above the singles; about 70 singles</td></tr>
<tr><td>Sub bay, lower</td><td>Subwoofer on a 5 cm riser, facing the sofa, open in front</td><td>45 × 50 × 37</td><td>AX5100G sub 21.4 × 30.4 × 29.4</td><td>2.6 cm above; 13.6 cm behind for its port</td></tr>
<tr><td>Sub bay, top</td><td>Hidden slim drawer</td><td>40 × 28 × 6 box</td><td>Remotes, batteries, styli</td><td>—</td></tr>
<tr><td>High shelf</td><td>Books, a cable box, print, Deco B</td><td>225 × 30, top at 192</td><td>Books up to 26 tall</td><td>2 cm above the tallest books</td></tr>
</table>
<p>The PS3 keeps the top row of bay 2 because it runs far hotter than the others, so its heat rises out under the worktop and through the open back. The games sit below the Xbox 360, so warm air rises away from them. The records have their own plywood carcass, away from the PS3, and stand on drawer bases on runners screwed into 18 mm ply, never on a BESTÅ shelf (20 kg limit).</p>

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

<h2 class="pb">The oak joinery</h2>
<p>Above the worktop the wall is furniture rather than cladding: two solid oak uprights, shelves carried on joints you can see, and the Card Room Green wall left to show between them. Slatted panels are the look of the moment and will date with it; joinery like this won't.</p>
<ul>
<li><b>Two oak uprights frame the TV:</b> solid oak, 4.5 × 30 cm and about 144 cm long, from the worktop (76) to the ceiling, about 2 cm clear of each side of the screen. They stand on the worktop on two dowels each, are scribed to the ceiling and held to the solid back wall with concealed brackets.</li>
<li><b>Wedged through-tenons:</b> the left shelf (top 156) and the turntable shelf (top 113) pass through the uprights on two tenons each and show 2 cm on the TV side, held with oak wedges. They are the joints you see first, so they're the ones worth cutting by hand.</li>
<li><b>Housed and pegged:</b> the high shelf, in three lengths at 192, and the record ledge are housed into the uprights and pinned with 10 mm oak pegs. The pegs show as dark dots on the uprights' faces.</li>
<li><b>Record ledge above the TV:</b> 7 cm deep with a 1.5 cm lip, top at 155.4, holding four LPs face-out against the wall up to about 186.5, just under the high shelf. The rotating "now playing" wall.</li>
<li><b>LED grooves:</b> a routed groove in each upright's inner face holds a 2700K strip that washes the green wall either side of the TV.</li>
<li><b>Cane screen for the PC:</b> an oak frame with a woven cane panel instead of slats; it hides the ports and lets the exhaust breathe.</li>
<li><b>Solid oak where you touch it:</b> a 3 cm solid oak worktop with a chamfered edge (top at about 76), the face frame in oak rather than painted, so the base reads as one sideboard, and drawer fronts with hand-cut finger pulls.</li>
<li><b>The green wall stays visible</b> behind the TV and between the shelves, so the oak reads as furniture against the colour, not a covering.</li>
<li><b>Notch for the ceiling strip:</b> a 2 × 1.5 cm notch in the back top corner of each upright lets the existing LED strip run straight past.</li>
<li><b>Finish:</b> hardwax oil throughout. A lightly limed or smoked oak for the uprights keeps away from the bright orange "new oak" look.</li>
<li><b>Hidden cables:</b> a 2 × 1.5 cm groove routed down the back of the right-hand upright carries Deco B's 12 V lead and its patch lead to Switch 2, from the high shelf to the cable slot. The TV's leads drop straight into the slot.</li>
</ul>
<figure>{joints()}</figure>
<h3>Joinery cut list</h3>
<table class="tight"><tr><th>Part</th><th>Material</th><th>Finished size (cm)</th><th>Joints</th><th>Qty</th></tr>
<tr><td>Uprights</td><td>Solid oak, quarter-sawn if you can</td><td>144 × 30 × 4.5 (buy 150 and scribe)</td><td>2 mortises each for the through-tenons, housings for the high shelf and ledge, LED groove inside, cable groove at the back of the right one</td><td>2</td></tr>
<tr><td>High shelf, centre</td><td>Solid oak</td><td>128.9 × 30 × 4</td><td>Housed 1.2 into both uprights, stub tenons, pegged</td><td>1</td></tr>
<tr><td>High shelf, left and right ends</td><td>Solid oak</td><td>45.7 and 46.2 × 30 × 4</td><td>Housed into one upright, on a cleat on the side wall</td><td>2</td></tr>
<tr><td>Record ledge</td><td>Solid oak</td><td>128.9 × 7 × 2.4, lip 126.5 × 1.5 × 0.9</td><td>Housed and pegged</td><td>1</td></tr>
<tr><td>Left shelf</td><td>Solid oak</td><td>51 × 25 × 4 (44.5 + 4.5 through + 2 proud)</td><td>Two through-tenons 7 × 2.4, wedged; cleat on the left wall</td><td>1</td></tr>
<tr><td>Turntable shelf</td><td>Solid oak</td><td>51.5 × 45 × 4 (45 + 4.5 through + 2 proud)</td><td>Two through-tenons 7 × 2.4 within the upright's 30 cm depth, wedged; cleat on the right wall</td><td>1</td></tr>
<tr><td>Wedges</td><td>Oak, contrasting if you like</td><td>7 × 3, tapering 4 to 0.5 mm</td><td>Glued into saw kerfs</td><td>4 + spares</td></tr>
<tr><td>Pegs</td><td>10 mm oak dowel, riven if possible</td><td>5 long</td><td>Driven from the front edge, trimmed flush</td><td>6</td></tr>
<tr><td>Worktop</td><td>Solid oak, full stave or wide board</td><td>225 × 40 × 3</td><td>Chamfered front edge; cut edges sealed</td><td>1</td></tr>
<tr><td>Face frame</td><td>Oak, 20 mm</td><td>Stiles about 5 wide, rails 2.6 and 2 tall, 225 long</td><td>Glued and pinned; end stiles scribed</td><td>1 set</td></tr>
<tr><td>PC screen</td><td>Oak frame 2 × 3 section, pre-woven cane</td><td>26 × 48</td><td>Cane in a groove with a spline</td><td>1</td></tr>
</table>
<table class="tight"><tr><th>Compared with the slat wall</th><th>Estimate (£)</th></tr>
<tr><td>Two solid oak uprights, 150 × 30 × 4.5 cm, with the joints cut</td><td class="num">150–300</td></tr>
<tr><td>Solid oak worktop instead of laminate</td><td class="num">150–300 more</td></tr>
<tr><td>Oak face frame instead of painted MDF</td><td class="num">20–30 more</td></tr>
<tr><td>No slat panels or battens</td><td class="num">230–380 less</td></tr>
</table>
<p>Overall it costs about the same as the slat wall, a little more with the solid worktop, and it's a more permanent piece of furniture. If a joiner cuts the joints, add their time. Every cost is in the build tracker under "Oak joinery and lighting".</p>

<h2 class="pb">The record trays</h2>
<p>Bay 3, under the turntable, is two roll-out trays stacked, and everything in them is face-out. LPs stand in a trough on the left of each tray, leaning back about 10° like a record shop browser; 7-inch singles stand the same way in a narrower trough on the right, where the singles and spare sleeves used to stand spine-up. With a tray shut, the room sees the front LP and the front single above a slim oak lip. Pull it out and flip through both rows of covers from the front.</p>
<figure>{drawer()}</figure>
<h3>What changed, and why</h3>
<ul>
<li><b>Thinner trays:</b> 9 mm birch ply sides, front and back instead of 12 mm, a 12 mm base instead of 18 mm, a 6 mm oak divider, and a slimmer oak lip, 5 cm tall and 15 mm thick. It looks lighter from the room and shows more of each front cover.</li>
<li><b>What the slimmer build buys:</b> 4.2 cm more width inside each tray, enough to turn the singles to face-out (a 7-inch sleeve is 18.3 cm), and 6 mm more finger room above every row.</li>
<li><b>Spare inner sleeves</b> move to the kit shelf or the hidden drawer.</li>
</ul>
<h3>How the system works</h3>
<ul>
<li><b>LP trough:</b> 32.6 cm wide, so a bare 31.4 cm sleeve has 6 mm each side. Records lean back 10° against each other; the last one leans on a raked oak rest at the back.</li>
<li><b>Singles trough:</b> 18.9 cm wide, the same lean, a smaller rest at the back.</li>
<li><b>Capacity:</b> the inside is 38.2 cm deep. The lean takes about 5.5 cm for LPs, leaving about 31 cm of stack: about 90 LPs at about 3.3 mm each, allowing for gatefolds. Singles lean less far, leaving about 34 cm: about 120 at about 2.8 mm. Two trays: about 180 LPs and 240 singles.</li>
<li><b>Outer plastic sleeves:</b> if most of your LPs live in thick outer sleeves (up to about 32.3 cm), widen the LP trough to 33.4 cm; the singles trough then drops to 18.1 cm, too narrow for face-out singles, so they go back to spine-up.</li>
<li><b>Runners:</b> 400 mm full-extension ball-bearing runners rated 68–70 kg per pair (45 kg is the minimum), screwed straight into the carcass's 18 mm ply sides. The whole tray clears the unit, so the back records are as easy to reach as the front.</li>
<li><b>Weight and safety:</b> about 32 kg per full tray. The carcass must be fixed to the wall with anti-tip brackets before the trays are loaded, and only one tray opened at a time.</li>
</ul>
<h3>Sizes</h3>
<table class="tight"><tr><th>Dimension</th><th>Figure</th><th>How it adds up</th></tr>
<tr><td>Carcass</td><td>60 × 40 × 73 outside, 56.4 × 69.4 inside</td><td>18 mm birch ply sides, top and bottom; back open to the cable channel</td></tr>
<tr><td>Tray width</td><td>53.9 outside, 52.1 inside</td><td>56.4 opening − 2 × 1.25 runners; 9 mm sides</td></tr>
<tr><td>Tray depth</td><td>40 outside, 38.2 inside</td><td>9 mm front and back panels</td></tr>
<tr><td>Inside layout</td><td>32.6 + 0.6 + 18.9</td><td>LP trough, oak divider, singles trough</td></tr>
<tr><td>Lower tray</td><td>Underside 2.3, base top 3.5, sleeves to 34.4</td><td>Lip from 2.3 to 7.3; 2.6 cm finger room under the upper tray</td></tr>
<tr><td>Upper tray</td><td>Underside 37.0, base top 38.2, sleeves to 69.1</td><td>Lip from 37.0 to 42.0; 2.1 cm finger room under the top panel at 71.2</td></tr>
<tr><td>Capacity</td><td>About 90 LPs and 120 singles per tray</td><td>About 31 cm of LP stack ÷ 3.3 mm; about 34 cm of singles ÷ 2.8 mm</td></tr>
<tr><td>Weight</td><td>About 32 kg per tray, full</td><td>90 × about 0.23 kg + 120 × about 0.045 kg + about 5 kg of tray</td></tr>
</table>
<h3>Cut list</h3>
<table class="tight"><tr><th>Part</th><th>Material</th><th>Size (cm)</th><th>Qty</th></tr>
<tr><td>Carcass sides</td><td>18 mm birch ply</td><td>73 × 40</td><td>2</td></tr>
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
<h3>How to build them</h3>
<ol>
<li><b>Build the carcass:</b> glue and screw the top and bottom between the sides, square, with the two back rails. Have the merchant cut the ply to the list.</li>
<li><b>Set it in place</b> beside bay 2 on a flat floor, shim it level with the frames' tops at 73, bolt it to bay 2's frame, and fix it to the wall with anti-tip brackets.</li>
<li><b>Fit the runners</b> straight onto the ply sides, level, every screw hole used: the lower pair so the tray's underside sits at 2.3 cm, the upper pair at 37.0 cm. Make the tray width exactly what the runner instructions specify (normally the opening less 25 mm).</li>
<li><b>Build the trays:</b> sides, back and low front panel glued and pinned to each other, then glued and screwed down onto the 12 mm base. Glue the oak divider 32.6 cm in from the left inside face, fit the two raked rests, and glue the felt down.</li>
<li><b>Hang the trays</b> and check they run true empty.</li>
<li><b>Fit the oak lips</b> from inside the tray, with a hand-cut finger pull at the top centre, 2–3 mm clear of the face frame.</li>
<li><b>Load gradually,</b> one tray at a time, and check both still run smoothly full.</li>
</ol>

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
<h2>Storage: every record face-out</h2>
<p>With PS1 games out of the unit, the vinyl side is set up so every LP and single shows its cover.</p>
<table class="tight"><tr><th>Where</th><th>What</th><th>How many</th><th>Notes</th></tr>
<tr><td>Bay 3, upper tray</td><td>LPs and singles, face-out</td><td>About 90 LPs + 120 singles</td><td>Front covers on show above the lip</td></tr>
<tr><td>Bay 3, lower tray</td><td>LPs and singles, face-out</td><td>About 90 LPs + 120 singles</td><td>The same, at floor level</td></tr>
<tr><td>Under the turntable</td><td>Oak LP browser, face-out</td><td>About 50 LPs</td><td>Shelf at 113 leaves 33 cm clear; the front record is on show beside the TV</td></tr>
<tr><td>Above the TV</td><td>Oak record ledge</td><td>4 LPs</td><td>The "now playing" wall</td></tr>
<tr><td>Sub bay, kit shelf</td><td>Preamp, stylus, cleaning kit, brush, inner sleeves; singles spines-out</td><td>About 70 singles</td><td>Shelf top at 38.8, over the sub</td></tr>
<tr><td>Sub bay, top</td><td>Hidden slim drawer</td><td>—</td><td>Remotes, cables, batteries, styli</td></tr>
<tr><td>High shelf</td><td>Books, a box for cables and controllers</td><td>About 40–50 books</td><td>Books up to 26 cm; LPs are too heavy up here (about 70 kg per metre)</td></tr>
<tr><td><b>Total in the wall</b></td><td></td><td><b>About 230 LPs, all face-out, and about 310 singles</b></td><td>240 of the singles face-out</td></tr>
</table>
<h3>If the collection grows</h3>
<ul>
<li><b>Overflow cube unit:</b> a 1 × 4 or 2 × 4 cube unit such as IKEA KALLAX (cubes about 33 cm inside, 39 cm deep) holds about 60–70 LPs per cube. On its side behind the sofa or under a window, a 2 × 4 holds about 500 LPs and gives you a second display top.</li>
<li><b>Tighter packing:</b> each tray takes about 95 LPs packed tight, at the cost of an easy flip.</li>
<li><b>LP browser depth:</b> keep it face-out at 24 cm deep. A deeper rack under the turntable would weigh about 35 kg over the sub bay, more than the worktop should carry there.</li>
</ul>

<h2 class="pb">Paint: Farrow &amp; Ball Card Room Green</h2>
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
<h3>Skirting: paint it Card Room Green too</h3>
<figure>{img("skirting_options.png", "Three skirting options with Card Room Green walls")}</figure>
<ul>
<li><b>Recommended: Card Room Green in Estate Eggshell.</b> The wall colour with a soft sheen. It completes the drench, so the room's edges disappear and the oak base and records are what you notice, and it hides scuffs from feet and the hoover far better than white.</li>
<li><b>Darker option: Green Smoke.</b> A deeper Farrow &amp; Ball grey-green with a hint of blue, for a defined edge that grounds the room. It draws the eye down, so keep it to the skirting and door.</li>
<li><b>Keeping a light trim:</b> swap the brilliant white for a soft off-white. Bright white next to a muted grey-green looks cold and stark.</li>
<li><b>Painting over white gloss or satin:</b> wash, key with a fine sanding pad, prime with a woodwork primer, then two coats of eggshell. Do the door, frame and window board at the same time.</li>
<li><b>Behind the unit:</b> where the base meets the side wall inside the alcove, cut the skirting back so the oak end stile sits flush, or scribe the stile over it.</li>
</ul>

<h2 class="pb">Lighting</h2>
<p>Three layers, all warm: the LED strip you already have round the ceiling, light built into the oak, and a spotlight bar on the existing ceiling rose in the middle of the room.</p>
<h3>Now: the LED strip round the ceiling</h3>
<ul>
<li><b>What you have:</b> a strip stuck to the ceiling (not the wall) round the whole edge of the room, facing down, as in your photo. In the renders it runs along the left wall, into the alcove, across its back wall and reveal, and across the chimney breast, washing the top of every wall.</li>
<li><b>Where it meets the oak:</b> the uprights run up to the ceiling against the back wall, so the strip would stop at each one. Cut a small notch, about 2 × 1.5 cm, in the back top corner of each upright so the strip runs straight through.</li>
<li><b>Keep it warm:</b> 2700K, on a dimmer, so it matches the rest.</li>
</ul>
<h3>Later: upgrading the strip</h3>
<table class="tight"><tr><th>Upgrade</th><th>What it does</th><th>Effort</th></tr>
<tr><td>Aluminium channel with an opal diffuser, in the same place</td><td>Hides the individual LED dots and gives a clean line; cools the strip so it lasts longer</td><td>Easy: stick or clip the channel up, re-lay the strip</td></tr>
<tr><td>LED coving or a shadow-gap cornice</td><td>Hides the strip completely and throws light up across the ceiling instead of down the walls: softer, no glare from the sofa</td><td>Medium: fixed and painted Card Room Green with the walls</td></tr>
<tr><td>Strip in the uprights' grooves only, on a separate circuit</td><td>Light the media wall on its own for films, with the room strip off</td><td>Planned already; needs the fused spur for the driver</td></tr>
</table>
<h3>Built into the oak</h3>
<ul>
<li><b>Upright grooves:</b> a 2700K strip in an aluminium channel in a groove on each upright's inner face, washing the green wall either side of the TV.</li>
<li><b>Bias light:</b> a 6500K strip on the back of the TV, from its USB port, which is easier on the eyes in a dark room.</li>
</ul>
<h3>The ceiling light: a four-head spotlight bar</h3>
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
<li><b>Headroom:</b> with a 22.4 cm drop on a 220 cm ceiling, the lowest shade sits at about 198 cm. Tilted heads hang a little lower, so if it's over the walkway, angle them up rather than down at the front. Measure the room's ceiling before buying.</li>
<li><b>Fitting:</b> it replaces the bare pendant on the existing rose; have the electrician wire it and the dimmer on the same visit.</li>
</ul>

<h2>Sound layout</h2>
<figure>{sound()}</figure>
<p>With the sofa directly opposite the TV at the left of the room, the sub fires straight at the seats, and nothing sits in the walkway by the door.</p>
<ul>
<li><b>Subwoofer:</b> wireless, in the alcove's right-hand corner, facing the sofa. A corner gives the most bass, and deep bass spreads in every direction, so it blends in from there. Keep 10–15 cm between the sub and the wall behind it. A 5 cm riser lifts it off the floor so the bass stays tight.</li>
<li><b>Rear speakers:</b> one each side of the sofa, at about seated ear height or slightly above, level with or just behind your heads, angled towards the seats. On the AX5100G they're joined by a cable and only the link to the soundbar is wireless: run that cable behind the sofa along the skirting, and plan one socket for them.</li>
<li><b>Soundbar:</b> centred in front of the TV, pointing straight at the sofa.</li>
<li><b>Tuning:</b> sit on the sofa and set the sub and rear levels with the soundbar's remote or app. If the bass booms, turn the sub down rather than moving it.</li>
<li><b>Open room:</b> the sofa area is the left part of a larger space, so bass can sound a little lighter at the seats than in a closed room. The corner sub helps make up for it.</li>
</ul>

<h3>Storage without crowding</h3>
<ul>
<li><b>Inside the unit:</b> about 180 LPs and 240 singles face-out in the two record trays, about 70 singles and the vinyl kit over the sub, about 48 games in the game drawer (12 face-out, the rest spine-up), and a controller basket beside the PS3.</li>
<li><b>On the worktop and ledge:</b> about 50 LPs in the browser under the turntable and 4 on the ledge above the TV, so about 230 LPs in all, every one face-out.</li>
<li><b>High shelf:</b> about a metre of books between oak bookends, one lidded box for spare cables and controllers, a print and Deco B.</li>
<li><b>Left of the alcove:</b> the oak shelf through-tenoned into the left upright, top at 156 cm, above the Series X, for display or favourite games.</li>
<li><b>Keep clear:</b> the band around the TV, the 40 cm above the turntable for its lid, the air above the Series X, and the front of the sub.</li>
<li><b>Maximum storage:</b> if you need more, swap the high shelf for shallow wall cabinets across the left two-thirds, keeping the right end open for Deco B. It adds a lot of hidden space but makes the wall look heavier.</li>
</ul>

<h3>Build options</h3>
<table><tr><th>Option</th><th>How</th><th>Good</th><th>Watch out</th></tr>
<tr><td>Frames on a plinth + custom record bay + full-width top (recommended)</td><td>Two IKEA BESTÅ 60×40×64 frames on a 9 cm plinth, an 18 mm ply carcass for bay 3, and a solid oak worktop cut to 225 × 40 cm, resting on felt-lined battens over the open sub bay, all behind an oak face frame</td><td>Built-in look, mostly flat-pack, shelves on pins, room for two face-out record trays</td><td>Top at about 76 cm, so the TV sits 9 cm higher; back panels off; oil the worktop all over</td></tr>
<tr><td>Kallax 4×2 on its side</td><td>Cube unit plus side fillers</td><td>Cheapest; cubes are about 33.5 cm square inside, so LPs and single consoles fit</td><td>147 cm wide leaves a gap even after the sub bay; no room for the record drawers</td></tr>
<tr><td>Custom built-in</td><td>18 mm board carcasses built to the alcove</td><td>Exact fit throughout</td><td>Most work, and permanent</td></tr>
</table>

<h3>Easy use and access</h3>
<ul>
<li>Disc trays, power buttons and front USB ports at the front edge of each bay.</li>
<li>Every drawer and tray runs on full-extension runners with a finger pull in the oak lip; no push-to-open at floor level. Open one record tray at a time.</li>
<li>Label each switched socket and each HDMI switch input with the same console name.</li>
<li>The controller basket holds the TV and HDMI switch remotes plus a charging dock for the Xbox and PlayStation pads, powered from the USB charger.</li>
<li>Keep console bays open, or use cane or mesh fronts, so air and the HDMI switch remote both get through.</li>
</ul>

<h3>Cables, power and airflow</h3>
<ul>
<li><b>Service channel:</b> with the unit 10 cm off the wall, every cable drops through the 10 cm slot at the back of the worktop into two-compartment trunking: mains on one side, HDMI, Cat6 and audio on the other. Fit brush grommets at the back of each bay, and velcro-tie and label every cable.</li>
<li><b>To the TV:</b> it stands on the worktop, so its power, four HDMI leads (PC, Series X, HDMI switch, soundbar eARC) and Ethernet drop straight down behind it. No socket behind the TV is needed.</li>
<li><b>To Deco B:</b> a patch lead runs in slim corner trunking from the high shelf down to the 8-port switch. The switch is 10.1 cm deep, just too deep to lie flat in the 10 cm channel, so stand it on its edge or screw it to the back of the unit using its wall-mount slots.</li>
<li><b>Power bricks:</b> the original Xbox 360 and Xbox One bricks sit on the free half of their console's row in bay 1, where air reaches them.</li>
<li><b>Turntable:</b> its leads drop through a grommet at the back of the worktop, behind the browser, straight to the preamp on the kit shelf below; the preamp's output runs along the data side of the trunking to the soundbar's AUX input. Keep them away from the power bricks and the sub's mains lead.</li>
<li><b>To Deco B:</b> the Cat6 from the top floor comes in through the ceiling in the alcove's right corner. Its 12 V lead and the patch lead to Switch 2 run along the back of the high shelf into the groove behind the right upright, down to the slot, and to an always-on socket of the 6-way at the back of the sub bay. If the adapter's lead won't reach, add a DC extension with the same plug rather than a mains extension up at the shelf.</li>
<li><b>To the subwoofer:</b> its power lead runs along the channel to the always-on strip. Put felt or rubber pads where the worktop rests on its wall batten, so bass doesn't rattle it.</li>
<li><b>PC on the left wall:</b> HDMI and Cat6 drop through the shelf notch, down the trunking and along the skirting into the service channel. Over 3 m, use an active optical HDMI cable; these work one way round only, so the end marked "source" goes into the PC.</li>
<li><b>Power:</b> the wall socket on the side wall just in front of bay 1, swapped from a single to a double, feeds your 10-gang and the 6-way, one per socket, never one plugged into the other. You won't need to reach it day to day: the strips' own switches do that. See the power map below.</li>
<li><b>OLED care:</b> keep the TV on the always-on strip. It runs its pixel refresh while in standby, so don't switch it off at the wall.</li>
<li><b>Airflow:</b> no doors on the console bays (use mesh or slatted fronts if you want them), open backs, and at least 4 cm, ideally 10 cm, clear around the Series X.</li>
</ul>

<h3>Power map</h3>
<figure>{power()}</figure>
<ul>
<li><b>Where the 10-gang goes:</b> lying flat on the worktop behind the TV, switches up, with side B's switch at the left end. From the left, reach in through the 15 cm gap between the Series X and the TV. From the sofa, the soundbar and the TV's bottom edge hide it.</li>
<li><b>Leads up to it:</b> console leads rise through the slot behind the worktop; label each plug at the strip end.</li>
<li><b>The 6-way:</b> screwed to the back of the sub bay, just under the kit shelf, so its switches are in reach and its leads are short to the deck, preamp and Deco lead.</li>
</ul>
<h3>Cable routes</h3>
<figure>{routes()}</figure>

<h2 class="pb">The PC shelf</h2>
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

<h2 class="pb">Alternative: the slat wall</h2>
<p>Kept for reference. The base, drawers, records and consoles are identical; above the worktop, oak acoustic slat panels on battens run from the worktop to the ceiling instead of the uprights, the shelves sit on hidden cleats, and the face frame is painted. It's quicker to fit, hides cables in the batten gap and softens sound, but it follows a current trend.</p>
<figure class="render">{img("render_v8_slat_key_scene.png", "Slat wall alternative with numbered parts")}
<figcaption>The slat wall alternative in the same Card Room Green; numbers follow its own key, which comes with the full-resolution renders.</figcaption></figure>
<ul>
<li><b>What changes:</b> four 240 × 60 cm slat panels on 25 × 50 mm battens (about £230–380), a laminate worktop instead of solid oak, an MDF face frame painted Card Room Green eggshell, and the shelves on cleats with no joints on show.</li>
<li><b>What stays:</b> every height, the record trays, the power and network routes and the lighting, except that the LED wash comes from strips under each shelf instead of the upright grooves.</li>
</ul>

<h2 class="pb">Build guide: the whole wall</h2>
<p>Everything needed to build the unit, the oak joinery, the trays and drawers, and the PC shelf. Sizes are finished sizes in centimetres. Measure your own alcove first: walls are rarely square, so take its width at the floor, at 76 cm, at 192 cm and at the ceiling, and cut the worktop and shelves to the smallest.</p>
<figure>{section()}</figure>
<h3>What it's made of</h3>
<table class="tight"><tr><th>Element</th><th>Made from</th><th>Finished size</th><th>Fixing</th></tr>
<tr><td>Plinth (bays 1–2)</td><td>18 mm ply ladder frame: front and back rails, four cross rails</td><td>120 × 38 × 9</td><td>Shimmed level on the floor; frames screwed down onto it from inside</td></tr>
<tr><td>Bays 1–2</td><td>2 × IKEA BESTÅ frame, white stained oak effect, back panels off</td><td>Each 60 × 40 × 64, tops at 73</td><td>Joined to each other, 10 cm spacer blocks to the wall, 2 anti-tip brackets each</td></tr>
<tr><td>Bay 3 carcass</td><td>18 mm birch ply, back open</td><td>60 × 40 × 73</td><td>On the floor, bolted to bay 2, 10 cm spacers and 2 anti-tip brackets</td></tr>
<tr><td>Internal shelves</td><td>4 × BESTÅ shelf (20 kg each)</td><td>56 × 36</td><td>On pins at the fit-check heights</td></tr>
<tr><td>Worktop</td><td>Solid oak, full stave or wide board, chamfered front edge</td><td>225 × 40 × 3, top at 76</td><td>Screwed up through the frame and carcass tops in slotted holes so it can move; on felt-lined battens over the sub bay</td></tr>
<tr><td>Uprights</td><td>Solid oak</td><td>144 × 30 × 4.5 (scribed)</td><td>Two 10 mm dowels into the worktop, two concealed brackets each into the back wall</td></tr>
<tr><td>Sub bay battens</td><td>44 × 22 mm planed softwood, felt-lined</td><td>40 (right wall) + 44 (back)</td><td>Into the wall, top at 73</td></tr>
<tr><td>Kit shelf</td><td>18 mm oak-veneered ply or oak</td><td>44.4 × 30</td><td>On two 30 cm battens, top at 38.8; rubber pads</td></tr>
<tr><td>Record trays</td><td>9 and 12 mm birch ply, oak dividers and lips, 400 mm runners</td><td>Trays 53.9 × 40 × 13.2</td><td>Runners straight into the bay 3 carcass (cut list above)</td></tr>
<tr><td>Game drawer</td><td>Birch ply, oak lip, 350 mm runners</td><td>Box 54.3 × 35 × 16.4</td><td>Runners on bay 1's sides (cut list above)</td></tr>
<tr><td>Hidden drawer</td><td>12 mm birch ply box, 20 mm oak front</td><td>Box 40 × 28 × 6; front 44 × 7.4 at 65.6–73</td><td>250 mm runners on a ply cheek against the bay 3 carcass and a batten on the right wall, just under the worktop</td></tr>
<tr><td>LP browser</td><td>Oak offcut base, 20 mm oak front rail and side</td><td>44 × 24, rail 4 tall, side 9 tall</td><td>Loose on the worktop, rubber feet</td></tr>
<tr><td>High shelf</td><td>Solid oak, three lengths</td><td>30 × 4, top at 192</td><td>Housed and pegged into the uprights; the end lengths also on cleats on the side walls</td></tr>
<tr><td>Record ledge</td><td>Solid oak</td><td>128.9 × 7 × 2.4, top 155.4</td><td>Housed and pegged into the uprights</td></tr>
<tr><td>Turntable shelf</td><td>Solid oak</td><td>51.5 × 45 × 4, top at 113</td><td>Wedged through-tenons in the right upright, cleat on the right wall; clear of the unit</td></tr>
<tr><td>Left shelf</td><td>Solid oak</td><td>51 × 25 × 4, top at 156</td><td>Wedged through-tenons in the left upright, cleat on the left wall</td></tr>
<tr><td>PC shelf box</td><td>27 mm oak top, 18 mm oak sides</td><td>65 × 32, box 9 deep</td><td>French cleat plus 2 steel brackets (25 kg+)</td></tr>
<tr><td>Keyboard tray</td><td>12 mm birch ply, oak lip</td><td>About 46 × 30</td><td>300 mm light-duty runners in the box</td></tr>
<tr><td>PC screen</td><td>Oak frame with a woven cane panel</td><td>26 × 48</td><td>Screwed to the shelf from below</td></tr>
<tr><td>Face frame</td><td>20 mm oak</td><td>Stiles about 5 wide, rails 2.6 and 2 tall, 225 long, 73 tall overall</td><td>Glued and pinned to the frame and carcass fronts; end stiles scribed to the walls</td></tr>
</table>
<h3>Tools</h3>
<ul>
<li>Drill-driver and an SDS or hammer drill for the masonry, with masonry bits and plugs.</li>
<li>Spirit level (a cross-line laser makes the shelf heights quick), tape, combination square, stud and cable detector.</li>
<li>Track or circular saw for the worktop and ply (or have the timber merchant cut the ply and oak to the cut lists), jigsaw for notches.</li>
<li>For the joints: a sharp set of chisels (6, 12 and 25 mm), a marking gauge, a tenon saw, a router with a straight bit for the housings and grooves, a 10 mm drill bit for the pegs, and a mallet.</li>
<li>Router with a cove bit for the finger pulls (or buy lips with the pull routed), clamps, sander, wood glue.</li>
<li>Dust mask, eye and ear protection.</li>
</ul>
<h3>Order of work</h3>
<ol>
<li><b>Check and measure:</b> ceiling height, alcove width at four heights, the walls for plumb, the floor for level across the alcove, and your records and games.</li>
<li><b>Electrician:</b> Cat6 runs (the one for Deco B through the ceiling in the alcove's right corner), swap the single socket in front of bay 1 for a double (or move it back into the alcove), sockets by the sofa and under the PC shelf, the fused spur for the LED drivers, and the spotlight bar and its dimmer. Mark every cable route on the wall before painting.</li>
<li><b>Paint the room</b> in Card Room Green, skirting and door in eggshell, alcove included, and let it cure for a few days before fixing anything to it.</li>
<li><b>Mark heights</b> on the walls with a level or laser: 73 (worktop battens), 37 (kit shelf battens), 109 (turntable shelf underside), 152 (left shelf underside), 188 (high shelf underside), and the uprights' lines at 44.5–49 and 175.5–180 cm from the left wall.</li>
<li><b>Fix the cleats and battens</b> on the side walls for the shelf ends and the sub bay, into the masonry, level. Cut the skirting back where the base meets the walls.</li>
<li><b>Build the plinth</b> and set it against the spacer blocks, shimmed dead level: it decides whether the worktop sits flat.</li>
<li><b>Assemble the frames</b> with their back panels off, stand them on the plinth, join them with BESTÅ connectors and screw them down to it.</li>
<li><b>Build the bay 3 carcass,</b> set it beside bay 2, shim it so its top is level with the frames at 73, bolt it to bay 2, and fit the anti-tip brackets on all three.</li>
<li><b>Fit the worktop:</b> scribe the ends to the walls, oil it all over (underside too, so it stays flat), and screw up through the frame and carcass tops in slotted holes (short screws that can't come through). Felt pads on the sub-bay battens.</li>
<li><b>Fit the trunking</b> in the channel behind the unit, mains on one side and data on the other, and run the cables in.</li>
<li><b>Fit the internal shelves</b> in bays 1 and 2 at the fit-check heights.</li>
<li><b>Build and fit the trays and drawers:</b> both record trays in bay 3, then the game drawer in bay 1 (steps in their sections).</li>
<li><b>Fit the kit shelf and the hidden drawer</b> in the sub bay, and put the sub on its riser.</li>
<li><b>Cut the joints and fit the oak:</b> dry-fit each upright with its shelves on the bench, then stand the uprights on their dowels, fix the concealed brackets, and fit the shelves, ledge, wedges and pegs (see "The oak joinery"). Lay the Deco leads in the right upright's groove before it goes up.</li>
<li><b>Build the PC shelf box,</b> fit the keyboard tray runners, hang it on its cleat and brackets, fit the screen and the trunking down to the skirting.</li>
<li><b>Make the LP browser,</b> fit the oak face frame, and finish all the oak with hardwax oil.</li>
<li><b>Place and connect everything,</b> label each plug and HDMI input, and test.</li>
</ol>

<h3>Then: lighting</h3>
<ol>
<li><b>Upright grooves:</b> aluminium channel and a 2700K strip in each upright's inner groove, wired down the back groove to a driver on the fused spur in the sub bay.</li>
<li><b>Ceiling strip:</b> re-stick the existing strip through the notches at the top of the uprights; add the channel and diffuser whenever you upgrade it.</li>
<li><b>Bias light</b> on the back of the TV, from its USB port.</li>
<li><b>Spotlight bar:</b> fit it on the existing rose, parallel to the media wall, then aim the heads and set the dimmer.</li>
</ol>
<h2 class="pb">Living room AV</h2>
<p>The TV's four HDMI 2.1 ports cover everything. The PC and Series X get their own ports for 120Hz+ and VRR (the C6's 165Hz mode is for PCs), the soundbar takes eARC, and the other five consoles share HDMI 4 through a switch. The C6 has no analogue inputs, so the PS2 and PS1 go through the RetroTINK first.</p>
<figure>{av()}</figure>
<h3>How each source reaches the Hisense</h3>
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
<h3>TV and console settings</h3>
<ul>
<li>Rename each TV input, with HDMI 4 as "Retro", and turn on HDMI Ultra HD Deep Colour for HDMI 1, 3 and 4.</li>
<li>Use Game Optimiser on the console inputs for the lowest lag.</li>
<li>Set sound output to HDMI eARC, with digital audio on Auto or Passthrough.</li>
<li>Set the PS3, 360 and Xbox One to output 5.1 over HDMI.</li>
<li>On the PS3, turn off "Control for HDMI" so it doesn't grab the TV input.</li>
<li>For the PC at 4K above 120Hz, use a cable certified Ultra High Speed (48 Gbps), which includes the active optical one.</li>
</ul>
<h3>PS2 and retro on the 55-inch</h3>
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
<h3>Vinyl: through the soundbar, done properly</h3>
<ul>
<li><b>Setup:</b> slim turntable with a new stylus, set to PHONO → external phono preamp on the shelf over the sub → soundbar AUX input, using an RCA-to-3.5 mm lead.</li>
<li><b>Check first:</b> the external preamp only helps if the deck has a PHONO/LINE switch. With no switch, its built-in preamp can't be bypassed, so skip the external one and plug the deck straight into the soundbar AUX.</li>
<li><b>Why the external preamp:</b> a slim deck's built-in preamp is its weakest part. A proper one gives fuller bass, clearer highs and less hiss.</li>
<li><b>Soundbar settings:</b> Music mode, bass up, and surround effects, night mode and dialogue mode off. Turn the sub down slightly from your film setting if bass gets boomy.</li>
<li><b>No Bluetooth:</b> always use the AUX cable, as Bluetooth loses quality.</li>
<li><b>Stylus:</b> buy the exact replacement for the deck's model, and set the tracking weight to the cartridge maker's figure.</li>
<li><b>Records:</b> clean them with a carbon-fibre brush before playing, and keep a few spare inner sleeves in the drawer's side compartment.</li>
</ul>
<h3>Upgrade path for vinyl</h3>
<p>Start with the soundbar route. Step up only if you want more. The old hi-fi and its built-in deck can be retired.</p>
<ol>
<li><b>Best for vinyl (about £200–450):</b> a stereo amp with phono input and sub output, the hi-fi's wired speakers, and a powered subwoofer. Fully analogue, loud and bassy. The Hisense sub can't be reused, as it only pairs with the soundbar.</li>
<li><b>Best for the whole room (about £500+):</b> an AV receiver with phono input and HDMI eARC, replacing the soundbar and driving real 5.1 speakers. Pure stereo for vinyl, proper surround for films.</li>
</ol>

<h2 class="pb">Why we chose this option</h2>
<p>Wired where it matters, wireless everywhere else. The devices that need speed and stability are on cable, and the Wi-Fi is left free for phones.</p>
<ul>
<li><b>Wired gaming and streaming:</b> the Xboxes, PS3, TV and PCs get full gigabit with the lowest latency and no dropouts, whatever the walls or neighbours do.</li>
<li><b>Phones get uncrowded Wi-Fi:</b> with heavy users on cable, phones aren't competing with a 4K stream or game download.</li>
<li><b>Dual-band Decos need cables to shine:</b> the X1500 has no dedicated band for unit-to-unit traffic. Cabling the links gives every floor the same strength as the top floor.</li>
<li><b>Star layout:</b> each Deco has its own cable from the top floor, so the kitchen doesn't depend on the living room kit being on.</li>
<li><b>Switches cost nothing in speed:</b> every port runs at full speed at once, with no setup. They're simply extra ports, about £18–25 each.</li>
<li><b>Zones that match the kit above them:</b> the Xbox bay under the Series X, the PlayStation bay under the TV, and the records under the turntable, so cables stay short and everything lives where it's used.</li>
</ul>
<h3>Options we rejected</h3>
<table><tr><th>Option</th><th>Why not</th></tr>
<tr><td>Keep the Virgin hub as router, Decos in access point mode</td><td>Loses HomeShield and parental controls</td></tr>
<tr><td>All-wireless mesh</td><td>Works, but speed drops with each wireless hop, worst in the kitchen</td></tr>
<tr><td>Powerline adapters</td><td>Slower and less stable than Cat6; fallback only if cabling is impossible</td></tr>
<tr><td>2.5Gb switches</td><td>Decos and PCs top out at 1Gb, so no gain for the extra cost</td></tr>
<tr><td>Keeping the 5-port switch upstairs</td><td>Full on day one; any new device upstairs would need another switch</td></tr>
<tr><td>Plugging devices straight into Decos</td><td>Only one spare port per Deco: not enough for 2 PCs upstairs or 6 devices downstairs</td></tr>
<tr><td>Games upright, two lines deep</td><td>The back line is hidden and you pull out the front ones to reach it</td></tr>
<tr><td>Games lying flat in stacks</td><td>Hard to pick from, and long-term flat storage can bow discs in a warm room</td></tr>
<tr><td>Records on an open shelf in bay 1</td><td>Far from the deck, spines only, and too heavy for a BESTÅ shelf; the drawer puts them under the turntable with the art on show</td></tr>
<tr><td>A green feature wall only</td><td>Leaves the alcove looking applied; the drench ties the room together</td></tr>
<tr><td>White skirting</td><td>Cuts a bright line round the room and breaks the drench; Card Room Green eggshell or a soft off-white sits better</td></tr>
<tr><td>A paper lantern for the ceiling</td><td>Replaced by the spotlight bar you chose: aimable light for the shelves, and it sits higher</td></tr>
<tr><td>A long pendant drop</td><td>On a 220 cm ceiling it would hang into the walkway; a flattened shade on a short drop keeps headroom</td></tr>
<tr><td>Keeping the deep forest green</td><td>Still a good option for the darkest picture at night, but you asked for softer; the grey-green keeps the drench and feels lighter by day</td></tr>
<tr><td>Singles spine-up beside the LPs</td><td>Thinner trays free enough width to show them face-out too, and hold twice as many</td></tr>
<tr><td>Records spine-up in one drawer</td><td>Held slightly fewer and showed only a handful of covers; two face-out drawers show every one, at the cost of a TV 9 cm higher</td></tr>
<tr><td>RetroTINK-2X Pro</td><td>Now a legacy model, won't accept 480p, and has simpler deinterlacing than the 6X CE</td></tr>
<tr><td>Cheap PS2-to-HDMI adapters</td><td>Soft, washed-out picture that a 55" OLED makes obvious</td></tr>
<tr><td>Bluetooth from the turntable</td><td>Compresses the sound; the AUX cable keeps full quality</td></tr>
</table>

<h2>Later ideas</h2>
<ul>
<li><b>Dave and Emma's watch log:</b> a shared movie and TV area, like a Spotify Blend for what you watch. Log each film or episode, mark whether you watched it together or one of you on your own, and give it a simple rating. It could live on the TV (a small web app on the LG's browser) or on your phones, and later suggest what to watch together next. First thought only; to be shaped up separately.</li>
</ul>

<h2>Still to confirm</h2>
<ul class="checks">
<li class="done">Alcove: 225 cm wide, about 50 cm deep, floor to ceiling.</li>
<li class="done">Every record face-out: two trays in bay 3, unit raised to 76 cm; thinner trays with singles face-out.</li>
<li class="done">Paint: Farrow &amp; Ball Card Room Green No. 79; skirting to match in eggshell.</li>
<li class="done">Floor plans and room photos: alcove on the right of the hall-side wall, LED strip on the ceiling, rose in the middle of the room.</li>
<li class="done">Main build: the artisan oak version.</li>
<li class="done">Power: one socket on the side wall just in front of bay 1, becoming a double.</li>
<li class="done">Lighting: LED strip round the ceiling now; one ceiling light in the middle of the room.</li>
<li>Ceiling height: the plan assumes 220 cm (the alcove's measured height). Check it at a few points before cutting the uprights, and in the middle of the room for the pendant's headroom.</li>
<li>The socket's height (drawn at about 30 cm) and its distance in front of the alcove, and whether you'd like it moved back behind the unit while the electrician is there.</li>
<li>Living room depth: does the agent's 3.65 m run to the chimney breast or to the back of the alcove? And the chimney breast's width (drawn at about 85 cm).</li>
<li>The brick cupboard in the kitchen: its size, and whether a Cat6 cable can come down into it from behind the media wall.</li>
<li>Which room the Hub 5 is in upstairs, and the height of the low side of the sloped ceilings in the bathroom and bedroom 2.</li>
<li class="done">The Xbox 360 has an HDMI port, and the black box is the Xbox One.</li>
<li class="done">The PC connects by HDMI cable, and Cat6 runs between floors are possible.</li>
<li class="done">The Series X uses its fan stand, on the left; the turntable is raised on the right.</li>
<li class="done">Room: sofa directly opposite the TV at the left of the room; door about 2 m right of the alcove, with the stairs beside it; sub at the far right.</li>
<li class="done">The alcove back wall is solid, which suits the shelf cleats and battens.</li>
<li class="done">The TV's remote sensor works with the soundbar in front, so LG's own stand stays.</li>
<li class="done">Kitchen cable: straight from the top floor, now that Switch 1 has spare ports.</li>
<li class="done">Power: your 10-gang has a switch for each five-socket side.</li>
<li>PC case: confirm the window is on its left side (as standard), so the back faces the sofa.</li>
<li>10-gang: check it's surge-protected, and where its two switches sit.</li>
<li>Deco B: check its adapter lead reaches from the high shelf to the back of the sub bay (about 2.2 m); if not, a DC extension with the same plug.</li>
<li>Soundbar model: the plan assumes the AX5100G (3.5 mm AUX, optical and coax inputs, wireless sub, rears linked by cable). Confirm yours.</li>
<li>Rear speakers: is there a socket near the sofa, and a route behind it for the link cable?</li>
<li>Left wall where the PC shelf goes: solid or plasterboard? It decides the fixings.</li>
<li>Paint: Card Room Green after sampling, and the room's wall and ceiling area for quantities.</li>
<li>Floor in the alcove: carpet or hard floor? The plinth and the bay 3 carcass stand on it and must sit level.</li>
<li>Records: roughly how many LPs and singles, and are most LPs in thick outer sleeves? The wall holds about 230 LPs and 310 singles; outer sleeves need a wider LP trough.</li>
<li>Games: roughly how many PS2, Xbox 360 and Xbox One games? Past about 48, plan overflow (see the game drawer options).</li>
<li class="done">PS1 games: stored outside this unit.</li>
<li>Turntable: a modern deck usually has a small PHONO/LINE switch on the back. Check for it, and that the deck is under 45 cm wide.</li>
<li>Console model numbers (on the label underneath), to tighten the row heights. The plan assumes the largest version of each.</li>
<li>RetroTINK: order on restock, then check its size against the 23 × 23 × 8 cm reserved.</li>
<li>Check the PC cable route before buying the HDMI cable; it's estimated at 4–5 m, so active optical.</li>
</ul>

<h2>Sources</h2>
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
</body></html>"""
    (HERE / "plan.html").write_text(html)
    print("totals", tl, th, "upgrade", ul, uh)


def pdf():
    from playwright.sync_api import sync_playwright
    footer = ('<div style="width:100%;font-family:Inter,sans-serif;font-size:8px;color:#8a867e;padding:0 18mm;'
              'display:flex;justify-content:space-between"><span>Home Network &amp; Media Wall Plan · v9</span>'
              '<span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>')
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto((HERE / "plan.html").resolve().as_uri())
        pg.wait_for_timeout(500)
        pg.pdf(path=str(HERE.parent / "out" / "Home_Network_Plan_v9.pdf"), format="A4", print_background=True,
               margin={"top": "16mm", "bottom": "18mm", "left": "18mm", "right": "18mm"},
               display_header_footer=True, header_template="<div></div>", footer_template=footer)
        b.close()


if __name__ == "__main__":
    build()
    pdf()
    print("pdf ok")
