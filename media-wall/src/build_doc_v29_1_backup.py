"""Builds the plan (v13) as HTML, then PDF via headless Chromium, plus the beginner's build guide as its own PDF.
The plan reads in build order: decision, room, media wall and fit proof, records and turntable, dining wall, side wall,
joinery, paint and light, power and network, build guide, buy list, then what's left to confirm.
Numbers come from geometry.py and fit.py."""
import base64, pathlib
import geometry as G
import fit
import questions
import ideas
import tidy
from diagrams import (light_scene, leaf_case, fliptop, sub_box, drawer_layouts, storage, network, front, drawer, sound, game_drawer, av, power, routes, pc_shelf, section, joints, house,
                      living_plan, why_layout, seating, dining_section, dining_sites, chair_storage, chair_options,
                      option_c_elevation, option_c_section, option_c_plan, option_c_carcass, option_c_halves)

HERE = pathlib.Path(__file__).parent
VERSION = "29"
REVISION = "29.1: the dining cabinet upgraded: two sliding oak doors, a 185 table, proper folding chairs; the whole plan around it; step 11's cut list matches the doors"
PDF_NAME = f"Home_Network_Plan_v{VERSION}.pdf"
GUIDE_NAME = f"Build_Guide_v{VERSION}.pdf"


DECK = False   # True while the plan page (build_viewer.py) borrows these sections: images become art/ keys
DECK_ART = {"render_v13_join_clean.png": "art_join_card_room", "render_v13_join_key_scene.png": "key_join",
            "render_v13_drawers.png": "art_drawers_card_room", "render_v13_dining_four.png": "art_four_card_room",
            "render_v13_dining_six.png": "art_six_card_room", "render_v13_side.png": "art_side_card_room",
            "paint_grid.png": "doc_paint", "skirting_options.png": "doc_skirt",
            "render_v29_3d_window_B_folded.png": "3d_window_B_folded", "render_v29_3d_dining_B_four.png": "3d_dining_B_four",
            "render_v29_3d_B_folded.png": "3d_B_folded", "render_v29_3d_ideas_window.png": "3d_ideas_window", "render_v29_3d_ideas_breast.png": "3d_ideas_breast",
            "render_v29_3d_plants_corner.png": "3d_plants_corner", "render_v29_3d_records_breast.png": "3d_records_breast", "render_v29_3d_plants_breast.png": "3d_plants_breast",
            "render_v29_3d_chairs.png": "3d_chairs", "render_v29_3d_chairs_shut.png": "3d_chairs_shut",
            "render_v29_3d_room.png": "3d_room", "render_v29_3d_suggest.png": "3d_suggest", "render_v29_3d_seat.png": "3d_seat",
            "render_v29_3d_case_mixed.png": "3d_case_mixed", "render_v29_3d_case_singles.png": "3d_case_singles", "render_v29_3d_decor.png": "3d_decor",
            "render_v29_3d_c_folded.png": "3d_c_folded", "render_v29_3d_c_six.png": "3d_c_six", "render_v29_3d_window_c_six.png": "3d_window_c_six", "render_v29_3d_c_chairs.png": "3d_c_chairs", "render_v29_3d_c_plan.png": "3d_c_plan"}


def img(name, alt=""):
    if DECK:
        return f'<img data-art="{DECK_ART[name]}" alt="{alt}" loading="lazy">'
    p = HERE / name
    mime = "jpeg" if p.suffix.lower() in (".jpg", ".jpeg") else "png"
    return f'<img src="data:image/{mime};base64,{base64.b64encode(p.read_bytes()).decode()}" alt="{alt}">'


def n(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


LPS = G.ALL_LPS                                            # v19: 291, the wall's 191 and the vinyl stand's 100
SINGLES = 2 * G.TRAY_SINGLES                               # 0 since v15: LPs only

# ---------------------------------------------------------------- buy list and jobs, in build order
# (status, item, phase, qty, lo, hi)  lo/hi None = no cost
TRACK = [
    ("To do", "Put the Virgin Hub 5 into modem mode", "1 Network, now", "", None, None),
    ("To do", "Set up Deco A, Switch 1 and the PCs in bedroom 3", "1 Network, now", "", None, None),
    ("To do", "Add Deco B and Deco C over Wi-Fi for now; speed-test each room and the Xbox", "1 Network, now", "", None, None),
    ("To buy", "Cat6 patch leads, 0.5–2 m", "1 Network, now", "11", 15, 20),
    ("To buy", "TP-Link TL-SG108 8-port switch: one for the living room, one to replace the 5-port in bedroom 3", "1 Network, now", "2", 36, 50),
    ("To do", "Cat6, your own job: two runs from bedroom 3, across the landing and down through the airing cupboard, one to the alcove's right corner (Deco B) and one on to the kitchen (Deco C), a spare pulled with each, and the optional runs to the master and bedroom 2 <b>(changed: no electrician)</b>", "2 Cables and power", "", None, None),
    ("To buy", "Cat6 solid pure copper, round (not CCA): two runs, four with the optional ones", "2 Cables and power", "2–4 runs", 30, 60),
    ("To buy", "Cat6 tools: a punch-down tool, RJ45 keystones and two surface boxes (or plugs and a crimper), a cable tester, a draw-rod set <b>(new: you run the Cat6 yourselves)</b>", "2 Cables and power", "1 set", 30, 60),
    ("To do", "Swap the single socket on the side wall for a double at the same spot: like for like, not notifiable; step 3 has the safe way to do it <b>(changed: your own job)</b>", "2 Cables and power", "", None, None),
    ("To buy", "A double socket in the same finish, and a deeper back box if the old one is shallow <b>(new)</b>", "2 Cables and power", "1", 5, 15),
    ("To buy", "Electrical safety kit: a two-pole voltage tester to GS38 with its proving unit, an MCB lock-off and padlock, a plug-in socket tester <b>(new: for doing it yourselves)</b>", "2 Cables and power", "1 set", 45, 90),
    ("To buy", "Insulated (VDE) screwdrivers, wire strippers and side cutters <b>(new)</b>", "2 Cables and power", "1 set", 20, 40),
    ("To buy", "6-way surge-protected extension for the retro set (Xbox One, 360, PS3, PS2, PS1, RetroTINK) <b>(changed: switched at the wall)</b>", "2 Cables and power", "1", 20, 35),
    ("To buy", "4-port USB charger, 5 V 2 A per port (HDMI switch, fan stand, pad dock, bias light)", "2 Cables and power", "1", 10, 20),
    ("To buy", "USB plug, 5 V 2 A or more, for the RetroTINK on the retro 6-way", "2 Cables and power", "1", 5, 10),
    ("To buy", "Cable kit: brush grommets, velcro ties, labels", "2 Cables and power", "1", 20, 30),
    ("To buy", "Flat two-compartment trunking for the 4 cm channel behind the base, about 2 m", "2 Cables and power", "1", 10, 20),
    ("To do", "Chase two conduits into the solid side wall for the PC, from behind the PC shelf down to skirting height and behind the skirting to the base's plinth: 38 mm oval for the HDMI and Cat6, 25 mm oval for the PC's mains lead; make good and paint <b>(changed: your own job; the PC now runs from the 10-gang)</b>", "2 Cables and power", "", None, None),
    ("To buy", "Conduit: 38 mm and 25 mm oval, about 4 m each, two draw wires, one oak-coloured brush grommet; a 5 m C13 lead with a rewireable 13 A plug for the PC <b>(changed)</b>", "2 Cables and power", "1", 15, 35),
    ("To buy", "For the chase: a wall chaser with dust extraction for a day (or a bolster chisel and club hammer), one-coat filler <b>(new)</b>", "2 Cables and power", "1", 20, 45),
    ("To buy", "PC tidy kit: braided sleeve, shelf-notch grommet", "2 Cables and power", "1", 5, 15),
    ("To buy", "A powered USB 3 hub, 4-port with its own adapter, screwed under the side run's front edge below the PC: pads, the keyboard and a stick within reach of the sofa <b>(new in v17)</b>", "2 Cables and power", "1", 15, 30),
    ("To buy", "A remote power button for the PC: a wireless switch on the motherboard's power header (card in a spare slot), its push button on the wrap ledge <b>(new in v17)</b>", "2 Cables and power", "1", 10, 30),
    ("To buy", "A magnetic mesh dust filter cut to the PC's top exhaust <b>(new in v17)</b>", "2 Cables and power", "1", 5, 10),
    ("To do", "Sample Farrow & Ball Card Room Green No. 79 on an A4 board; check it by day and with the LED strip on", "3 Paint", "", None, None),
    ("To buy", "Card Room Green: Estate (or Modern) Emulsion for walls, ceiling, alcove and chimney breast; Estate Eggshell for skirting and radiator (the door and its frame stay white, v20); primer and undercoat", "3 Paint", "", 200, 500),
    ("To buy", "Woodwork primer, sanding pads and sugar soap for the white skirting and door", "3 Paint", "1", 20, 40),
    ("To do", "Paint the whole room before anything is fixed: alcove and breast included; skirting and door from white to eggshell", "3 Paint", "", None, None),
    ("Done", "Check the alcove back wall for fixings (solid)", "4 Base unit", "", None, None),
    ("To do", "Measure the alcove's width at the floor, 76, 134, 155 and 196 and the ceiling, and the floor's level across it", "4 Base unit", "", None, None),
    ("Done", "Check the side wall where the ledge and PC shelf go, and the chimney breast where the dining wall goes: solid (you confirmed) <b>(new)</b>", "4 Base unit", "", None, None),
    ("To buy", "Two IKEA BESTÅ 60×40×64 frames, white stained oak effect, for bays 1–2", "4 Base unit", "2", 70, 200),
    ("To buy", "Plinth for bays 1–2: 18 mm ply ladder frame 120 × 38 × 9 cm with a clear bay under bay 2, plus shims", "4 Base unit", "1", 15, 30),
    ("To buy", "Hidden plinth drawer: oak front 54 × 6 with a finger-pull groove underneath, 12 mm ply box 52 × 34 × 5, 300 mm full-extension runners <b>(changed: no push-to-open at floor level, as v6.1 said)</b>", "4 Base unit", "1", 30, 50),
    ("To buy", "Bay 3 carcass: 18 mm birch ply, 60 × 40 × 73 cm from the floor, connector bolts, and a 12 mm birch-ply divider 38 × 69.4 that splits it into the slim game column and the LP column <b>(changed in v16: the divider)</b>", "4 Base unit", "1", 50, 90),
    ("To buy", "Two face-out LP crates, 34.9 × 40 (a 33 cm trough): 12 and 9 mm birch ply cut to size, 15 mm oak lips, raked rests, felt, two pairs of 400 mm runners rated 68–70 kg <b>(changed in v16: snug crates, no dead space)</b>", "4 Base unit", "2", 120, 200),
    ("To buy", "Three slim drawers for the game column, 15.3 × 40: 6 mm birch ply sides and backs, 12 mm bases, oak lips, felt, three pairs of 400 mm runners (light duty is enough); a 2 m USB-C lead and a grommet for the pads drawer <b>(new in v16)</b>", "4 Base unit", "3", 70, 130),
    ("To buy", "BESTÅ shelves, 56 × 36 cm (20 kg max each), two each for bays 1 and 2", "4 Base unit", "4", 12, 32),
    ("To buy", "The sub in bay 2: an isolation riser for it (dense foam or sorbothane, about 22 × 28 × 3), 12 mm birch ply for the divider (35.3 × 38) and the part shelf (32.2 × 36), four shelf pins, felt pads <b>(new in v13.5: the sub moves into the media wall)</b>", "4 Base unit", "1", 25, 45),
    ("To buy", "Anti-tip brackets and 4 cm spacer blocks: both frames and bay 3", "4 Base unit", "1 set", 15, 25),
    ("To do", "Measure about ten games of each kind (PS2, Xbox 360, Xbox One) before cutting the game drawer", "4 Base unit", "", None, None),
    ("To buy", "Game drawer kit: 12 mm birch ply cut to size, 350 mm full-extension soft-close runners (35–49 kg), oak lip, follower block, felt", "4 Base unit", "1", 50, 90),
    ("To do", "Build the plinth and bay 3, fix everything to the wall, fit the shelves, drawers and trays; place the TV and soundbar", "4 Base unit", "", None, None),
    ("To buy", "Two solid oak uprights, 165 × 30 × 4.5 cm (cut to 159), quarter-sawn if possible", "5 Oak joinery", "2", 150, 300),
    ("To buy", "Solid oak for the shelves: high shelf in two lengths (128.9 and 51.7 × 30 × 4), Series X shelf 55 × 30 × 4, record ledge 128.9 × 7 × 2.4, the side-wall run from one board 225 × 30 × 4 (cut to its sweep), lips <b>(changed in v15: one run for the ledge and the PC shelf)</b>", "5 Oak joinery", "1 set", 230, 380),
    ("To buy", "Oak wedges, 10 mm oak dowel for pegs and dowels, concealed upright brackets; two concealed shelf brackets for the PC shelf, rated 40 kg+ a pair", "5 Oak joinery", "1", 30, 60),
    ("To buy", "One solid oak worktop, 300 × 62 cm, full stave: the alcove top (186 × 46), chamfered front; keep the offcut <b>(changed in v29: no backboard, the table's in its cabinet)</b>", "5 Oak joinery", "1", 250, 450),
    ("To buy", "Oak face frame, 20 mm, 186 cm for the base", "5 Oak joinery", "1", 60, 120),
    ("To buy", "Keyboard tray for the PC shelf: 7 cm oak housing under it, 12 mm ply tray 54 × 26 with an oak lip, 300 mm light-duty runners <b>(new: back from v6.1)</b>", "5 Oak joinery", "1", 25, 45),
    ("To do", "Cut the joints and fit the uprights, shelves, ledges and face frame; notch the uprights for the ceiling strip", "5 Oak joinery", "", None, None),
    ("To buy", "Solid oak for the table: two halves 90 × 92.5 × 2.7, each a centre 78.5 × 90 of edge-glued staves with two pegged breadboard ends (the cutting list) <b>(changed in v29: 185 open)</b>", "6 Dining wall", "1 set", 265, 460),
    ("To buy", "The dining cabinet: oak-faced ply cut to size, 18 mm for its two ends, floor, partition, chair shelf, linen floor, the drawer front and the two sliding doors (98.7 × 183.3), 19 mm for the top (it carries the track); a 6 mm ply back; 12 mm ply for the drawer box (the cutting list) <b>(changed in v29: two sliding doors across the front)</b>", "6 Dining wall", "1 set", 300, 540),
    ("To buy", "Oak for the cabinet's hinge rail (91 × 19.2 × 7), the eight apron rails and the four tapered legs (6.5 × 4.5) <b>(changed in v29)</b>", "6 Dining wall", "1", 35, 70),
    ("To buy", "Altro continuous piano hinge, 1800 × 50, cut to 90: the table's foot <b>(new in v27)</b>", "6 Dining wall", "1", 16, 20),
    ("To buy", "Folding, self-locking table-leg brackets, a set of four, and sixteen figure-8 tabletop fasteners for the aprons <b>(new in v27)</b>", "6 Dining wall", "1", 60, 75),
    ("To buy", "The doors' sliding gear: Häfele Slido Classic 40 IF C, the fitting set for two doors with soft close (402.33.027), a 2.5 m double top track for a groove (402.33.652) and a bottom guide track (402.30.802), both cut to 194.4; a pair of 150 mm drawer runners, two magnetic catches and a knob for the folded table, two steel angle brackets for the wall <b>(changed in v29: sliding doors, so no door hinges or door knobs)</b>", "6 Dining wall", "1", 110, 190),
    ("To buy", "Folding chairs, IKEA FRÖSVI (TERJE's successor, the same size) or similar, six, and six seat pads; they live in the cabinet (skip any you already have: seat about 45–48) <b>(changed in v27: six)</b>", "6 Dining wall", "6", 150, 260),
    ("To buy", "Three Lee Valley 40574 narrow flip-top hinges (solid brass, 1.27 × 7.0 cm) for the joint <b>(new in v15)</b>", "6 Dining wall", "3", 25, 45),
    ("To buy", "Two LP frames for the chimney breast, hung from 165 cm", "6 Dining wall", "2", 20, 40),
    ("To buy", "The “now playing” ledge on the breast, with the table by the stairs: oak 105.5 × 7 × 2.4 with a 1.5 lip (from the shelf board's offcut), two concealed brackets <b>(new in v16)</b>", "6 Dining wall", "1", 10, 25),
    ("To do", "Build the dining cabinet: the carcass with its track grooves, stand it and fix it to the wall, the hinge rail, the two table halves on their aprons and legs, hang the table on its piano hinge, then the drawer and the two sliding doors (step 11) <b>(changed in v29)</b>", "6 Dining wall", "", None, None),
    ("To do", "Open the table, level it at 76 and trim the legs to the floor; load the six chairs (four on the floor, two on the shelf) and the seat pads <b>(new in v27)</b>", "6 Dining wall", "", None, None),
    ("To do", "Swap both ceiling fittings for the spot bars, turned to run from the TV towards the window: like for like, your own job; step 12 has the safe way. The light switches stay as they are (smart bulbs need full power) <b>(changed in v15: no dimmers)</b>", "7 Lighting", "", None, None),
    ("To buy", "Eight smart colour E14 bulbs for the bars: WiZ Colour P45 E14, 4.9 W (Wi-Fi, no hub), or Philips Hue White and Colour E14 lustre, 5.1 W, if a WiZ shows below its shade; both under the bar's 6 W <b>(new in v15)</b>", "7 Lighting", "8", 100, 360),
    ("To buy", "Smart colour strips for the upright grooves and under the side-wall run, in the same app as the bulbs: about 4.5 m of RGB and tunable-white strip (Philips Hue Lightstrip Plus, or WiZ's strip kits, cut at their marks), three aluminium channels with opal diffusers, plug-in power on the 10-gang (no fused spur); a 6500K bias light for the TV stays plain white <b>(changed in v16: smart colour, so the whole wall changes with a scene)</b>", "7 Lighting", "1", 90, 220),
    ("To buy", "Two Dunelm Elements Wolston 4-light spotlight bars, £49 each (bulbs above) <b>(changed: two)</b>", "7 Lighting", "2", 98, 110),
    ("To buy", "Optional: a smart button for the bars, so a scene is one press rather than the app (WiZ remote or Hue dimmer switch) <b>(new in v15)</b>", "7 Lighting", "1", 0, 25),
    ("To do", "Set up the smart bulbs in their app: group them as bar 1 and bar 2, then save the three presets (Bright, Cosy, Film; Paint and light) with their levels and colours, and the table rule; your red lamp's bulbs go in the same scenes <b>(new in v15)</b>", "7 Lighting", "", None, None),
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
    ("To buy", "Drip trays or a waterproof mat under the pots on the plant stand's slatted tiers; if you add clip-on grow lights later, a smart plug with a schedule <b>(new in v18)</b>", "10 Finishing", "1", 10, 20),
    ("To buy", "Felt pads under the vinyl stand's feet, so it slides out from the breast without marking the floor <b>(new in v18)</b>", "10 Finishing", "1", 3, 6),
    ("To buy", "A rug about 230 × 160 in front of the sofa: cream with deep blue, rust and ochre goes with the green, the oak and the blue sofa (the plan draws one as a guide) <b>(new in v15)</b>", "10 Finishing", "1", 120, 300),
]
PHASES = []
for r in TRACK:
    if r[2] not in PHASES:
        PHASES.append(r[2])
BIGGEST = {"1 Network, now": "two 8-port switches", "2 Cables and power": "the electrical safety kit and Cat6", "3 Paint": "paint",
           "4 Base unit": "record trays and the BESTÅ frames", "5 Oak joinery": "the solid oak worktop", "6 Dining wall": "the oak table top",
           "7 Lighting": "the eight smart bulbs", "8 TV, consoles and AV": "RetroTINK-6X CE", "9 Vinyl kit": "phono preamp", "10 Finishing": "the rug"}


# v13.6, client: "make the build plan easy to tell how to find which part ie network/media wall/table etc".
# Every step and every buy-list phase carries one or more of these coloured part labels.
PARTS = {"Prep": "#6b6862", "Network": "#2a73d9", "Power & cables": "#c4482c", "Paint": "#4f7a52",
         "Media wall": "#8a5a32", "Dining table": "#b0700f", "Lighting": "#8f7a00", "AV": "#7a4fb0"}
PHASE_PART = {"1 Network, now": ["Network"], "2 Cables and power": ["Power & cables", "Network"], "3 Paint": ["Paint"],
              "4 Base unit": ["Media wall"], "5 Oak joinery": ["Media wall"], "6 Dining wall": ["Dining table"], "7 Lighting": ["Lighting"],
              "8 TV, consoles and AV": ["AV"], "9 Vinyl kit": ["AV"], "10 Finishing": ["AV", "Network"]}


def part_chip(parts):
    if isinstance(parts, str):
        parts = [parts]
    return "".join(f'<span class="part" style="--pc:{PARTS[x]}">{x}</span>' for x in parts)


def scenes_html():
    """v25: the three lighting presets (scenes.py): a table of every layer's level, then each preset on its own with its drawing,
    its colours and its notes, the table rule drawn over the open table, and the two rules. In the viewer the figures become
    buttons (build_viewer replaces the part between the markers)."""
    import scenes as SC
    head = "<tr><th>Light</th><th>Control</th>" + "".join(f"<th>{s[1]}</th>" for s in SC.SCENES) + "</tr>"
    rows = "".join(f"<tr><td>{name}</td><td>{ctl}</td>" + "".join(f"<td class='num'>{SC.level_word(s[3][k])}</td>" for s in SC.SCENES) + "</tr>"
                   for k, name, ctl in SC.LAYERS)
    figs = "".join(f"<h4>{s[1]}</h4><p>{s[2]} <i>Colour: {SC.COLOURS[s[0]]}.</i></p><figure>{light_scene(s[0])}</figure><ul>"
                   + "".join(f"<li>{x}</li>" for x in s[4]) + "</ul>" for s in SC.SCENES)
    figs += f"<h4>With the table open</h4><figure>{light_scene('bright', table=True)}</figure>"
    rules = "<div class='why'><b>Two rules</b><ul>" + "".join(f"<li>{r}</li>" for r in SC.RULES) + "</ul></div>"
    return (f"<table class='tight'>{head}{rows}</table>"
            "<p class='note'>Levels are brightness in the app for the smart bars and the lamp, and roughly how far up the strip's controller and the uprights' inline dimmer go. A preset changes how bright the heads are (and their colour), not where they point.</p>"
            + rules + f"<!--scenes-->{figs}<!--/scenes-->")


def scenes_v24_html():
    """v25: the five scenes of v13.7 to v24, for the appendix."""
    import scenes as SC
    head = "<tr><th>Light</th>" + "".join(f"<th>{s[1]}</th>" for s in SC.SCENES_V24) + "</tr>"
    rows = "".join(f"<tr><td>{name}</td>" + "".join(f"<td class='num'>{SC.level_word(s[3][k])}</td>" for s in SC.SCENES_V24) + "</tr>" for k, name, _c in SC.LAYERS)
    where = "; ".join(f"{s[1]} → {dict((k, n) for k, n, *_ in SC.SCENES)[SC.OLD_TO_NEW[s[0]]]}" for s in SC.SCENES_V24)
    return (f"<h3>The five lighting scenes</h3><p>Six buttons (these five and Daytime) mixed moods, an activity that depends on the table, and the time of day. "
            f"They became three presets and two rules. Where each went: {where}, with the table rule for dinner; Daytime is now a switch.</p>"
            f"<table class='tight'>{head}{rows}</table>")


# v27: the flip-top's rows (v15–v26), out of the buy list since the dining cabinet became the plan; section 5 costs the alternative with them
FLIPTOP_ROWS = [
    ("To buy", "Solid oak for the flip-top: two panels 110 × 80 × 2.7 with pegged breadboard ends, the top and the half (edge-glued staves from a timber merchant, who can also radius the corners) <b>(changed in v15: the half replaces the leaf)</b>", "6 Dining wall", "1 set", 280, 480),
    ("To buy", "Two Häfele Hebgo heavy-duty folding brackets, 287.43.428 (580 arm, 500 kg a pair) <b>(new)</b>", "6 Dining wall", "2", 70, 120),
    ("To buy", "Union PowerLoad lift-off hinges, 100 × 88, one 3-pack (all the same hand) <b>(new)</b>", "6 Dining wall", "1", 16, 20),
    ("To buy", "The gate leg: two tapered oak legs 73.3 × 4.5 to 3 and a 94 × 7 × 2 oak apron (from the cutting list), two 75 mm butt hinges, two folding locking stays <b>(new in v15: instead of eight legs and the leaf's leg case)</b>", "6 Dining wall", "1", 40, 90),
    ("To buy", "Oak for the hinge rail (110 × 4 × 7.3), two oak turn buttons, a magnetic catch, felt pads <b>(changed in v15)</b>", "6 Dining wall", "1", 15, 30),
    ("To buy", "Folding chairs, IKEA FRÖSVI (TERJE's successor, the same size) or similar with a hole in the back for a hook, four, or six for six at the table (skip if yours fit: seat about 45–48) <b>(changed in v20)</b>", "6 Dining wall", "4–6", 100, 240),
    ("To buy", "The chair cupboard beside the table: oak (or oak-faced ply) for its two sides, top, floor and shelf and two doors (cutting list), a 6 mm back, four concealed soft-close hinges, two push latches, two screws and plugs for its top rail <b>(new in v20)</b>", "6 Dining wall", "1", 120, 240),
    ("To do", "Fix the backboard and hinge rail, hang the brackets and the top, fit the half on its flip-top hinges and the gate leg under it; check it opens, locks, folds and folds up", "6 Dining wall", "", None, None),
    ("To do", "Build the chair cupboard and stand it in the gap between the table's window end and the pipe boxing: level it, screw its top rail to the wall, hang the doors to swing towards the table; stand two folded chairs on its floor and two on its shelf <b>(new in v20)</b>", "6 Dining wall", "", None, None),
]


def fliptop_cost():
    """The flip-top's cost (v15–v26 rows), with the three flip-top hinges it shares with the cabinet's buy list."""
    rows = FLIPTOP_ROWS + [r for r in TRACK if _plain_txt(r[1]).startswith("Three Lee Valley 40574")]
    return sum(r[4] or 0 for r in rows), sum(r[5] or 0 for r in rows)


def cabinet_rows():
    """The buy list's rows for the dining cabinet: the "6 Dining wall" purchases, less the breast's LP frames and ledge."""
    return [r for r in TRACK if r[2] == "6 Dining wall" and r[4] is not None and not _plain_txt(r[1]).startswith(("Two LP frames", "The “now playing” ledge"))]


def _plain_txt(x):
    import re
    return re.sub(r"<[^>]+>", "", x)


def cabinet_html():
    """v27: the dining cabinet as the plan, in section 5: what it is, using it, how many sit down, the drawings, the cut list."""
    import fit as F
    C = G.OPTC
    st = F.optc_seats()
    seats = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{d}</td><td>{e}</td></tr>" for a, b, _s, d, e, _r in F.max_seats_zone()[2])
    rows = cabinet_rows()
    lo, hi = sum(r[4] for r in rows), sum(r[5] for r in rows)
    kg_half = C["top"][0] * C["top"][1] * C["top"][2] * 0.72 / 1000
    L = C["z"][0] - C["z"][1]
    return f"""
<p><b>The dining cabinet is the plan:</b> one oak cabinet under your shelf with the table and all six chairs inside it, as you asked: "a seating of 6", with "the chairs to exist within the same thing the table is built into". Shut, it's two tall oak <b>sliding doors</b> between two oak ends, {n(L)} × {n(C['d'])} × {n(C['h'])}, barely prouder than the pipe boxing, with the stairs' foot left clear: no table, no legs, no chairs on show. Open, the table is {n(C['len'])} × {n(C['top'][0])} and six sit in comfort, three a side.</p>
<figure class="render">{img("render_v29_3d_c_folded.png", "The dining cabinet packed away: one oak cabinet under the shelf")}
<figcaption>Packed away, in the 3D room: two sliding doors, the grain upright, a routed finger slot in each, a shadow line at the foot.</figcaption></figure>
<ul>
<li><b>Two sliding doors, not hinged ones.</b> Door A covers the table bay, door B the chair bay; they run on a Häfele Slido double track<sup>{F.ORDER.index("slido") + 1}</sup> between the ends, with soft close. Slide A over B and the table bay is open; slide B behind A and the chairs are. Nothing ever swings into the room: at the stair end a hinged door would have nowhere to fold back except where the first chair sits.</li>
<li><b>The table bay, at the stair end.</b> A {n(C['len'])} × {n(C['top'][0])} solid oak top in two {n(C['top'][1])} × {n(C['top'][0])} halves stands up inside it, folded face to face, on its hinge rail. Under it, a drawer for the mats; over it, the <b>linen shelf</b> for the cloth, the napkins, the runner and the candles.</li>
<li><b>The chair bay, at the window end.</b> Six slatted folding chairs (FRÖSVI or similar) stand folded: four on the floor, two side by side and two deep, and two on the shelf, with their six seat pads on edge in front of them.</li>
<li><b>The table itself:</b> the two halves meet flush on three brass flip-top hinges, each a centre of staves between pegged breadboard ends, the corners eased; four tapered oak legs fold flat inside the aprons. Each half is about {kg_half:.0f} kg.</li>
</ul>
<h3>Using it</h3>
<ol>
<li><b>Opening:</b> clear the floor in front of it and push the ottoman to the sofa. Take the chairs out first (slide door B behind door A), then slide door A over door B. Pull the knob at the top of the folded table and lower it halfway; unfold the inner half's two legs until each clicks<sup>{F.ORDER.index("legbracket") + 1}</sup>, then lower it onto them. It turns on the piano hinge at its foot<sup>{F.ORDER.index("pianohinge") + 1}</sup>.</li>
<li>Lift the outer half up and over on its flip-top hinges<sup>{F.ORDER.index("fliphinge") + 1}</sup>, unfold its two legs until they click, and lower it. The table is now {n(C['len'])} long, its top at {n(G.TABLE_TOP)}, level with the media wall's worktop.</li>
<li>Seat pads on the chairs: the top two chairs came out first, then the four on the floor.</li>
<li><b>Folding away:</b> the other way round: the outer half's legs folded and the half flipped back onto the inner one, the inner legs folded, then swing it up until the catches take it and slide door A back. Then door B across, the chairs and pads back in, both doors shut. Two hands; never with anything on the table.</li>
</ol>
<p class="note">The idea is a proven one: fold-down tables built into wall units are made this way<sup>{F.ORDER.index("foldtable") + 1}</sup>. The cabinet stands on the floor and is screwed to the wall at the top so it can't tip.</p>
<figure>{option_c_elevation()}</figure>
<figure>{option_c_section()}</figure>
<figure class="render">{img("render_v29_3d_c_chairs.png", "The dining cabinet: the chair bay open, six chairs inside")}
<figcaption>The chair bay open, door B slid behind door A: four folded chairs on the floor, two side by side and two deep; two on the shelf, the seat pads on edge in front of them.</figcaption></figure>
<h3>How many sit down</h3>
<p><b>Six, all in comfort:</b> three on the stair side ({st['stair'][1]:.1f} cm of edge each) and three on the window side ({st['window'][1]:.1f} each, from the sofa's arm to the cabinet). The coffee table stays where it is; a seventh chair fits at the far end if you bring one.</p>
<figure>{option_c_plan()}</figure>
<figure class="render">{img("render_v29_3d_c_six.png", "The dining cabinet open for six")}
<figcaption>Open for six in the 3D room: door A slid over door B, the linen shelf behind it; three a side, bar 2 turned up over it by the table rule.</figcaption></figure>
<table class="tight"><tr><th>Table</th><th>Seats</th><th>How</th><th>Notes</th></tr>{seats}</table>
<h3>How it's built</h3>
<p>Step 11 of the build guide builds it in order, with every size: the track grooves, the carcass, fixing it to the wall, the hinge rail, the two halves with their aprons and legs, the joint, hanging the table, the drawer, then the tracks and the two sliding doors. The two drawings below are the ones to have open on the bench.</p>
<figure>{option_c_carcass()}</figure>
<figure>{option_c_halves()}</figure>
<ul>
<li><b>The carcass:</b> oak-faced ply, cut to size by the merchant. Two ends {n(C['h'])} tall and {n(C['d'])} deep; the 19 mm top (the top track sits in a groove under it), the floor (the bottom guide in a groove in it) and the 6 mm back between them; inside, set {n(C['slide'])} back for the doors, a partition making the table bay {n(C['bay_t'][0] - C['bay_t'][1])} wide, the chair shelf and the linen floor; a plinth set back under it, a shadow line at the foot.</li>
<li><b>The doors:</b> two {n(C['door_w'])} × {n(C['door_h'])} panels of 18 mm oak-faced ply, about {C['door_kg']:.0f} kg each (the gear takes 40), grain upright, a finger slot routed near each outer end.</li>
<li><b>The hinge rail:</b> solid oak, 7 tall, across the table bay with its top at {n(C['pivot'][1])}: it carries the piano hinge, and the table's whole weight when it's open.</li>
<li><b>The halves:</b> edge-glued oak with pegged breadboard ends, each on an apron frame 2 thick and {n(C['apron'])} deep; the legs fold flat inside the frames on self-locking brackets.</li>
<li><b>The joint:</b> three brass flip-top hinges set into the meeting edges; open, the halves are flush; folded, the outer half lies flat on the inner one.</li>
</ul>
<p>It costs about £{money(lo, hi)}, the chairs included: the "6 Dining wall" rows of the buy list (section 11).</p>
<p class="note">Safety: never swing it up or down with anything on it; check all four legs have clicked before you load it; let the catches take it when it's folded; the cabinet is screwed to the wall at the top.</p>
"""


def money(a, b):
    return f"{a:,}–{b:,}"


def phase_totals():
    rows, tl, th = [], 0, 0
    for ph in PHASES:
        lo = sum(r[4] for r in TRACK if r[2] == ph and r[4] is not None)
        hi = sum(r[5] for r in TRACK if r[2] == ph and r[5] is not None)
        tl += lo; th += hi
        rows.append(f"<tr><td>{part_chip(PHASE_PART[ph])} {ph}</td><td class='num'>{money(lo, hi) if hi else '—'}</td><td>{BIGGEST[ph]}</td></tr>")
    rows.append(f"<tr class='total'><td>Total</td><td class='num'>{money(tl, th)}</td><td>no electrician: the electrics are your own job (section 9)</td></tr>")
    return "\n".join(rows), tl, th


def tracker_rows():
    out, cur = [], None
    for st, item, ph, q, lo, hi in TRACK:
        if ph != cur:
            out.append(f"<tr class='ph'><td colspan='5'>{part_chip(PHASE_PART[ph])} {ph}</td></tr>")
            cur = ph
        box = "☑" if st == "Done" else "☐"
        est = money(lo, hi) if lo is not None else ""
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
    "GOV.UK: Electrical safety, Approved Document P (2013 edition, for use in England): notifiable work is a new circuit, a replacement consumer unit, or an addition or alteration to a circuit in a special location (round a bath or shower); like-for-like replacements and additions to existing circuits elsewhere are not notifiable (gov.uk/government/publications/electrical-safety-approved-document-p)",
    "IET Electrical: Part P, England and Wales (notifiable and non-notifiable work); Planning Portal: Electrics, Building Regulations (non-notifiable work must still meet the regulations, BS 7671)",
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
    ("Electrics (your own: steps 3 and 12)", [
        ("Two-pole voltage tester to GS38, with its proving unit", "proving every wire dead before you touch it: non-negotiable", "Buy", "35–70"),
        ("MCB lock-off and a small padlock", "keeping the circuit off while you work on it", "Buy", "8–15"),
        ("Plug-in socket tester", "checking the new double socket is wired the right way round", "Buy", "8–15"),
        ("Insulated (VDE) screwdrivers, wire strippers, side cutters", "the socket and the ceiling fittings", "Buy", "20–40"),
        ("Wall chaser with dust extraction (or a bolster and club hammer)", "the PC's two conduits in the side wall", "Hire", "25–45 a day"),
        ("Cat6 punch-down tool and a cable tester", "terminating and checking the Cat6 runs", "Buy", "20–35"),
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



def steps():
    """The order of work, one dict per step: used by the PDF's table and the plan page's step cards.
    buy: the buy-list phases to have in before the step starts (each phase listed at the first step that needs it)."""
    g = G
    import instructions
    extra = instructions.full()
    return [dict(st, **extra.get(st["n"], {})) for st in [
        dict(n=1, part=["Prep"], title="Measure and count", who="You", time="2 h", buy=[], see=[("overview", "The room")],
             do=["The alcove's width at the floor, 76, 134, 155 and 196 cm and at the ceiling: cut everything to the smallest.",
                 "The floor's level across the alcove, and the chimney breast's flatness with a long level.",
                 "The door's swing, and the sofa: overall width, depth with the return, back height.",
                 "Count the LPs and games (PS2, Xbox 360, Xbox One), and measure ten cases of each.",
                 "Make a cardboard template of the alcove at worktop height: walls are rarely square."],
             check="Every figure within 1 cm of the plan. If not, send the numbers and the drawings are redone first."),
        dict(n=2, part=["Network"], title="Network, stage 1", who="You", time="2 h", buy=["1 Network, now"], see=[("network", "Network")],
             do=["Unplug everything from the Hub 5. Log in at 192.168.0.1 with the password on its base, then Modem Mode → Enable Modem Mode → Apply. Its page moves to 192.168.100.1.",
                 "Connect a hub port to Deco A in bedroom 3 and set it up in the Deco app, reusing the old Wi-Fi name and password. If it shows no internet, try another hub port and restart the hub.",
                 "Plug the new 8-port Switch 1 into Deco A's other port, then the PCs into Switch 1.",
                 "Add Deco B in the living room and Deco C in the kitchen. For now they link over Wi-Fi.",
                 "Speed-test each room, and check the Xbox's network settings show NAT: Open."],
             check="Internet in every room, and NAT: Open on the Xbox."),
        dict(n=3, part=["Power & cables", "Network"], title="Cables and the socket, your own job", who="You + a helper", time="2–3 days", buy=["2 Cables and power"], see=[("network", "Electrics: your own job"), ("network", "Power and cables")],
             do=["The Cat6: two runs from bedroom 3, across the landing and down through the airing cupboard, one to the alcove's right corner for Deco B, one on to the kitchen for Deco C, a spare pulled with each; the optional runs to the master and bedroom 2 if you want them. Low voltage: no rules beyond care.",
                 "The socket: swap the single on the side wall for a double at the same spot, with the circuit isolated, locked off and proved dead (the safe routine is in this step). Like for like, so not notifiable.",
                 "The PC's two conduits: chase them into the solid side wall from behind the PC shelf to skirting height and behind the skirting to the base, 38 mm oval for the HDMI and Cat6, 25 mm for the PC's mains lead, a draw wire in each. Make good.",
                 "Stop and call an electrician if anything on the stop list turns up (old wiring, no earth, a reading where there should be none, anything you can't match).",
                 "Before you fill a chase, photograph it with a tape measure in shot, and mark every route on the plan."],
             check="The socket tester shows correct wiring on both outlets, both Cat6 runs test good end to end, and every route is photographed."),
        dict(n=4, part=["Paint"], title="Paint", who="You", time="2–3 days, then a week to cure", buy=["3 Paint"], see=[("paint", "Paint and light")],
             do=["Paint an A4 board in Card Room Green and look at it by day and with the LED strip on.",
                 "Wash the skirting and door with sugar soap, sand to a key, and prime them.",
                 "Two coats of emulsion on the walls, ceiling, alcove and chimney breast.",
                 "Two coats of eggshell in the same green on the skirting and radiator (the door and its frame stay white).",
                 "Leave it a week to cure before fixing anything to it."],
             check="Two even coats, and no white showing at the edges or behind the radiator."),
        dict(n=5, part=["Prep"], title="Mark the heights", who="You", time="1 h", buy=[], see=[("wall", "Front view")],
             do=["With the laser level: 73 and 76 for the worktop, 130 and 134 for the Series X shelf, 153 and 155.4 for the ledges, 192 and 196 for the high shelf.",
                 f"The uprights at {n(g.UP_L[0])}–{n(g.UP_L[1])} and {n(g.UP_R[0])}–{n(g.UP_R[1])} cm from the side wall.",
                 f"On the breast: the “now playing” ledge's top at {n(g.NOW_LEDGE['top'])} and the framed LPs' bottom edges at {n(g.FRAMES_Y)}, centred.",
                 "Run the cable detector along every line you will drill, and mark anything it finds."],
             check="Every line level end to end, and the uprights' lines plumb."),
        dict(n=6, part=["Media wall"], title="Build the base", who="You", time="1 day", buy=["4 Base unit"], see=[("build", "Cutting list"), ("wall", "Drawer layouts")],
             do=["Order the oak and ply from the cutting list (below the steps), a week or two ahead: most merchants cut to size for a small charge.",
                 "Build the 9 cm plinth for bays 1–2, with the open bay for the hidden drawer under bay 2. Level it with shims.",
                 "Assemble the two BESTÅ frames with their back panels left off and stand them on the plinth.",
                 "Build bay 3 from 18 mm ply, 60 × 40 × 73, and bolt it to bay 2.",
                 "Screw the 4 cm spacer blocks to the wall, push the base against them and fit the anti-tip brackets.",
                 "Lay the flat two-compartment trunking in the channel behind (mains one side, data the other) and run the cables in."],
             check="The tops level within 1 mm across 186 cm, and nothing rocks."),
        dict(n=7, part=["Media wall"], title="Fit the worktop", who="You + a helper", time="½ day", buy=["5 Oak joinery"], see=[("build", "Cutting list"), ("wall", "Built to your alcove")],
             do=["Cut the worktop from the 300 × 62 oak board, using the template from step 1; keep the offcut.",
                 "Scribe the ends to the walls; cut the TV slot over the channel and the grommet hole behind the deck.",
                 "Oil it on every face, undersides and cut ends included.",
                 "Screw it up through the frame tops in slotted holes, so the oak can move."],
             check="Tight to both walls, and the slot sits over the channel."),
        dict(n=8, part=["Media wall"], title="Fit out the base", who="You", time="1–2 days", buy=[], see=[("wall", "Drawer layouts"), ("wall", "The records")],
             do=["Shelves on their pins at the fit-proof heights for the consoles.",
                 "The game drawer in bay 1: runners on the frame's sides, then the box (its cut list is with this step).",
                 "Bay 3: the 12 mm divider first (17.8 cm in from the left side), then the LP crates' runners at 2.3 and 37.0 cm on the right and the three slim drawers' at 2.3, 25.1 and 47.9 on the left, then each box.",
                 "The hidden plinth drawer under bay 2.",
                 "Bay 2: the divider and the part shelf, then the sub on its riser, its front flush with the face frame."],
             check="Every drawer runs smoothly, the two crates clear each other by 2 cm, and the slim drawers by 2.8."),
        dict(n=9, part=["Media wall"], title="Uprights and shelves", who="You + a helper", time="2–3 days", buy=[], see=[("wall", "The oak joinery")],
             do=["On the bench: cut the housings and the mortises in both uprights, and the LED groove and cable groove.",
                 "Dry-fit each upright with its shelves before any glue.",
                 "Lay Deco B's leads in the groove behind the right upright.",
                 "Stand the uprights on their dowels and fix the concealed brackets to the back wall.",
                 "Fit the high shelf and the ledge, then the Series X shelf: wedge its tenons, and peg the housings.",
                 "On the chimney breast: the “now playing” ledge, its top at 104, on two concealed brackets, 6 cm in from each side of the breast (with the table by the stairs)."],
             check="Uprights plumb, shelves level, the TV slides in with 2 cm each side, and the “now playing” ledge is level with an LP standing on it."),
        dict(n=10, part=["Media wall"], title="The side-wall run and the PC end", who="You", time="1 day", buy=[], see=[("wall", "The side wall")],
             do=["Cut the run from its 225 × 30 × 4 board: mark the front edge from the full-size template (7 cm deep along the LPs, sweeping out to 28 under the PC, a 5 cm radius on the end), jigsaw just outside the line and rout to it with a bearing-guided bit; rout the LED groove under the front edge.",
                 "Screw the oak cleat along the side wall and fit the concealed brackets for the PC end.",
                 "Lift the run on, dowel its end to the left upright's front edge, and screw it down to the cleat from above (plugged).",
                 "Screw the keyboard tray's housing under it and fit its runners.",
                 "Fit the brush grommet and pull the PC's leads down the two chased conduits with the draw wires: data in the big one, its mains lead in the small one.",
                 "The PC's extras (v17): screw the powered USB hub under the run's front edge below the PC, fit the remote power button's card and stick its button under the wrap ledge by the sofa, and lay the magnetic filter on the top exhaust."],
             check="One level line with the ledge over the TV, the sweep runs smooth with no flat spots, and the PC end holds your weight leaning on it."),
        dict(n=11, part=["Dining table"], title="The dining cabinet: the table and the six chairs in one", who="You + a helper", time="3–4 days", buy=["6 Dining wall"], see=[("dining", "The dining wall")],
             do=["Check the gap under your shelf (191 or more), mark the footprint and oil every oak part first.",
                 "Rout the tracks' grooves in the top and the floor, then build the carcass on the floor: the two ends, top and floor, the partition, the chair shelf and the linen floor set 5 back for the doors, then the 6 mm back to square it.",
                 "Stand it on its marks, shim it level and screw it to the wall at the top; fit the oak hinge rail across the table bay at 73.3.",
                 "On the bench: the two halves with their breadboard ends, the apron frames, the legs on their folding brackets, and the three flip-top hinges at the joint.",
                 "Hang the table on the piano hinge, fit the catches and the drawer, then the tracks and the two sliding doors; level the table and trim the legs; load the six chairs."],
             check="The table swings down and up without touching the bay's sides, all four legs click, the top is level at 76 both ways, the catches hold it folded, and both doors slide end to end, soft-close and meet straight with an even 3 mm under the top."),
        dict(n=12, part=["Lighting"], title="Lighting: smart spot bars and the LED strips, your own job", who="You + a helper", time="1 day", buy=["7 Lighting"], see=[("network", "Electrics: your own job"), ("paint", "Light")],
             do=["Isolate the lighting circuit at the consumer unit, lock it off and prove it dead at each ceiling point.",
                 "Take down the two old fittings. The light switches stay as they are: the smart bulbs need full power, so no dimmers.",
                 "Hang bar 1 on the rose between the TV and the sofa and bar 2 on the pendant point by the stairs, earth first, both running from the TV towards the window; fit the smart colour bulbs and point every head straight down, evenly spread; tilt one only if its pool lands badly.",
                 "The LED strips in the uprights' grooves and under the side-wall shelf on their plug-in driver (on the 10-gang), the ceiling strip through its notches, the bias light on the TV; your red lamp in its spot.",
                 "Power back on, switches on: add the eight bulbs to the app, group them as bar 1 and bar 2, and save the three presets (Paint and light): Bright, Cosy and Film. With the table open, bar 2 comes up to 80 and bar 1 down to 15 (the table rule)."],
             check="Every bulb answers the app, the presets recall, and from the sofa no spot head shows in the screen or shines in your eyes."),
        dict(n=13, part=["AV", "Network"], title="Connect and finish", who="You", time="1 day", buy=["8 TV, consoles and AV", "9 Vinyl kit", "10 Finishing"], see=[("network", "AV"), ("network", "Network")],
             do=["TV inputs: HDMI 1 the PC, HDMI 2 the soundbar (eARC), HDMI 3 the Series X, HDMI 4 the HDMI switch (Xbox One, 360, PS3, RetroTINK).",
                 "The PS2 by component into the RetroTINK and by optical to the soundbar; the PS1 by RGB SCART.",
                 "The deck to the preamp, the preamp to the soundbar's AUX; set the tracking weight; soundbar in Music mode for vinyl.",
                 "Network stage 2: plug each Cat6 run into its Deco, check Deco B and C show \"Ethernet\", and give the Series X and PC high priority.",
                 "Label both outlets of the double socket and each HDMI switch input; set the sub and rear levels from the sofa."],
             check="Everything on the network's \"done when\" list, and every source plays through the soundbar."),
    ]]


DIAGRAMS = {"front": "front", "section": "section", "drawer_layouts": "drawer_layouts", "game_drawer": "game_drawer", "drawer": "drawer",
            "storage": "storage", "joints": "joints", "pc_shelf": "pc_shelf", "dining_section": "dining_section", "seating": "seating",
            "av": "av", "power": "power", "network": "network", "routes": "routes", "leaf_case": "leaf_case", "fliptop": "fliptop",
            "optc_carcass": "option_c_carcass", "optc_halves": "option_c_halves", "optc_section": "option_c_section", "optc_elevation": "option_c_elevation", "optc_plan": "option_c_plan"}   # v27


def need_html(st):
    cols = [(lab, st.get(k, [])) for k, lab in (("parts", "Parts"), ("hardware", "Hardware and fixings"), ("tools", "Tools"))]
    cols = [(lab, items) for lab, items in cols if items]
    if not cols:
        return ""
    return ("<div class='need'>" + "".join(f"<div><h5>{lab}</h5><ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul></div>" for lab, items in cols)
            + "</div>")


def full_html(st):
    """Every instruction for one step, numbered straight through its sub-assemblies."""
    if not st.get("parts_full"):
        return "<ol>" + "".join(f"<li>{d}</li>" for d in st["do"]) + "</ol>"
    out, k = [], 1
    for head, items in st["parts_full"]:
        out.append(f"<h5>{head}</h5><ol start='{k}'>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>")
        k += len(items)
    return "".join(out)


# v17: the build guide PDF stands alone. Each cut-list part belongs to one step (matched on the start of its name),
# and each step's "see" link becomes the picture it pointed to in the plan.
CUT_STEP = {"Uprights": 9, "High shelf": 9, "Series X shelf": 9, "Record ledge": 9, "“Now playing”": 9, "Wedges": 9, "Ledge lips": 9,
            "Side-wall run": 10, "Keyboard tray": 10, "Concealed brackets": 10, "Plinth drawer and keyboard": 8,
            "Worktop": 7, "Face frame": 6, "Bay 3 sides": 6, "Bay 3 top": 6, "Plinth rails": 6, "Plinth cross": 6,
            "Dining": 11, "Table top": 11, "Breadboard": 11, "Gate": 11, "Turn buttons": 11, "Häfele": 11, "Lift-off": 11, "Flip-top": 11,
            "Cabinet": 11, "Table halves": 11, "Apron": 11, "Table legs": 11, "Hinge rail": 11, "Piano": 11, "Leg brackets": 11, "Tabletop": 11, "Drawer box": 11,
            "Sliding doors": 11, "Drawer front (the cabinet)": 11, "Sliding door gear": 11, "Drawer runners": 11}   # v27; v29.1: the doors' rows
SEE_FIG = {("wall", "Front view"): ("render_v13_join_key_scene.png", "The media wall with its parts numbered"),
           ("wall", "Drawer layouts"): ("render_v13_drawers.png", "Every drawer out, in place"),
           ("wall", "Built to your alcove"): ("render_v13_join_clean.png", "The finished media wall"),
           ("wall", "The side wall"): ("render_v13_side.png", "The side-wall run and the PC end"),
           ("dining", "The dining wall"): ("render_v29_3d_c_six.png", "The dining cabinet open for six"),
           ("overview", "The room"): ("render_v29_3d_room.png", "The whole room")}


def step_cuts(k):
    """The cut-list rows for step k (parts not matched elsewhere are the base's fit-out, step 8)."""
    rows = []
    for grp, note, items in cuts():
        for r in items:
            hit = next((v for pre, v in CUT_STEP.items() if r[0].startswith(pre)), 8 if r[4] == "Media wall" else None)
            if hit == k:
                rows.append((grp,) + r[:4])
    return rows


def step_cuts_html(k):
    rows = step_cuts(k)
    if not rows:
        return ""
    return ("<h5>Cut list for this step</h5><table class='tight cuts'><tr><th>Part</th><th>From</th><th>Size (cm)</th><th>Qty</th><th>Notes</th></tr>"
            + "".join(f"<tr><td>{a}</td><td>{g}</td><td class='num'>{b}</td><td class='num'>{c}</td><td>{d}</td></tr>" for g, a, b, c, d in rows)
            + "</table>")


def full_steps_html(pdf=False):
    """The PDF's step-by-step section: each step with what you need, its drawings and every instruction.
    pdf=True (the build guide PDF, v17): each step also carries its cut list and the picture its "see" link points to."""
    import diagrams as D
    out = []
    for st in steps():
        out.append(f"<div class='fstep'><h3 class='pb'>Step {st['n']} · {st['title']} <span class='note'>· {st['who']} · {st['time']}</span></h3><p>{part_chip(st['part'])}</p>")
        if st["buy"]:
            out.append(f"<p class='note'>Buy first: {', '.join(st['buy'])} (the buy list).</p>")
        out.append(need_html(st))
        if pdf:
            out.append("".join(f"<figure class='render small'>{img(SEE_FIG[k][0], SEE_FIG[k][1])}<figcaption>{SEE_FIG[k][1]}.</figcaption></figure>"
                               for k in st.get("see", []) if k in SEE_FIG))
        out.append("".join(f"<figure>{getattr(D, DIAGRAMS[d])()}</figure>" for d in st.get("draw", [])))
        if pdf:
            out.append(step_cuts_html(st["n"]))
        out.append(full_html(st))
        out.append(f"<p class='callout'><b>Check before moving on:</b> {st['check']}</p></div>")
    return "\n".join(out)


def steps_table_html():
    rows = "".join(f"<tr><td>{s['n']}</td><td>{part_chip(s['part'])}<br>{s['title']}</td><td>{' '.join(s['do'])}</td><td>{s['check']}</td><td>{s['time']}</td></tr>" for s in steps())
    return ("<table class=\"tight steps\"><tr><th>#</th><th>Stage</th><th>What to do</th><th>Check before moving on</th><th>Time</th></tr>"
            + rows + "</table>")


GUIDE_RULES = """
<p>For anyone who's hung shelves and built flat-pack but not cut a joint. Each step: what to do, what to check, and how long it takes.
Steps 3 and 12 are the electrics, with the point to stop and call an electrician. Finished sizes, in cm.</p>

<div class="callout"><b>Before you start: five rules</b><ul>
<li><b>Check every wall before you drill.</b> Run the cable and pipe detector over the spot, and never drill straight above, below or beside a socket or switch: cables run vertically and horizontally from them.</li>
<li><b>Measure twice, mark once, cut once.</b> Walls are rarely square: measure the alcove at the floor, 76, 134, 155, 196 and the ceiling, and cut to the smallest.</li>
<li><b>Two people for anything over 15 kg</b>: the uprights, the worktop, the table top, the TV.</li>
<li><b>The electrics are yours, within limits.</b> Swapping the socket for a double and the two ceiling fittings are like-for-like jobs, not notifiable under Part P in England, as long as they meet the wiring regulations. Isolate, lock off and prove dead every time. Anything new (a new circuit, the consumer unit, work by a bath or shower) is an electrician's, and so is anything on the stop list in section 9.</li>
<li><b>Dry-fit everything</b> (assemble without glue or screws) before the final fix.</li>
</ul></div>
"""


def guide_tools():
    return f"""<h3>Tools</h3>
<p>You don't need a workshop. Hire the two big tools for a weekend (a track saw and an SDS drill), or ask the timber merchant to cut the oak and ply to the cut lists: most will, for a small charge, and that removes the hardest cuts.</p>
{tools_html()}"""


GUIDE_TECHNIQUES = """<h3>Six techniques you'll use</h3>
<ol>
<li><b>Fixing into brick.</b> Detect, mark, drill with the SDS on hammer setting, clear the dust, push in a brown (7 mm) wall plug and drive a 5 × 60 mm screw. In plasterboard, find a stud, or use heavy-duty plasterboard fixings rated for the load.</li>
<li><b>Cutting oak cleanly.</b> Put masking tape over the cut line, score it with a knife, cut with the good face down (circular or track saw) or up (jigsaw). Clamp a straight edge as a guide.</li>
<li><b>Routing a housing</b> (a shallow slot a shelf sits in). Clamp a straight batten as a guide, set the bit 4 mm deep, rout, then step down to 12 mm in passes. Practise on an offcut first.</li>
<li><b>A wedged through-tenon.</b> Mark the 6 × 2.4 cm mortise on both faces of the upright and drill most of it out with a 20 mm bit from each side. Chisel it to the line. Saw the tenon on the shelf's end. Saw a kerf down its middle, glue it, tap it home, then drive a glued oak wedge into the kerf. When it's dry, saw it flush and plane it.</li>
<li><b>Dowelling.</b> Use a dowel jig to drill matching 10 mm holes 3 cm deep in both parts, glue the dowels, clamp.</li>
<li><b>Oiling.</b> Sand to 180 grit, wipe off the dust, rub on a thin coat of hardwax oil, wipe off the excess after 15 minutes, let it dry overnight, give it a second coat. Do the undersides too, so the boards don't cup.</li>
</ol>
"""

GUIDE_TIME = "<p>Roughly 16–20 working days spread over a few weekends, the electrics and the Cat6 included, plus the paint drying. Steps 6–11 can be split: the base and the dining cabinet first, the oak joinery once you're confident.</p>"

GUIDE_PITFALLS = """<h3>Where beginners usually go wrong</h3>
<ul>
<li><b>Cutting the worktop to the tape instead of to a template.</b> Make a cardboard template of the alcove first; walls are rarely square.</li>
<li><b>Skipping the dry-fit.</b> Gluing a tenon that doesn't fit is the one mistake you can't undo.</li>
<li><b>Oil on one side only.</b> The board cups within a week.</li>
<li><b>Loading the LP crates before the anti-tip brackets go in.</b> A full crate weighs about 30 kg.</li>
<li><b>Folding the table up with something on it.</b> Clear it first, every time, and keep both turn buttons turned when it's up.</li>
</ul>
"""


def cuts():
    """Every made part in one cutting list, grouped by what the timber merchant cuts it from (sizes in cm, L × W × T).
    Rows: (part, size, qty, notes, where it goes). Drawn from the cut lists in sections 3, 5 and 7 and v6.1's game drawer."""
    g = G
    pc_len = g.PC_SHELF_Z[0] - g.PC_SHELF_Z[1]
    return [
        ("Solid oak, hardwax oil", "Ask for it planed all round; scribe the uprights and worktop on site", [
            ("Uprights", f"{n(g.UPRIGHT_LEN)} × 30 × 4.5", "2", "Buy 165 long and scribe to the ceiling; housings, mortises, LED and cable grooves cut on the bench", "Media wall"),
            ("High shelf, long length", "128.9 × 30 × 4", "1", "Housed 1.2 into both uprights and pegged", "Media wall"),
            ("High shelf, short length", "51.7 × 30 × 4", "1", "Housed into the right upright; cleat on the reveal", "Media wall"),
            ("Series X shelf", "55 × 30 × 4", "1", "Two through-tenons 6 × 2.4, wedged flush", "Media wall"),
            ("Record ledge", "128.9 × 7 × 2.4", "1", "Housed and pegged", "Media wall"),
            ("Side-wall run (v15)", f"{n(g.SIDE_RUN_Z[0] - g.SIDE_RUN_Z[1])} long × 7 sweeping to {n(g.PC_SHELF_D)} × {n(g.SIDE_RUN_T)}, from one 225 × 30 × 4 board", "1", "On an oak cleat, concealed brackets under the PC end, dowelled to the left upright; LED groove under the front edge", "Media wall"),
            ("Ledge lips", f"128.9 × 1.5 × 0.9 · {n(G.WRAP_Z[0] - G.SIDE_SWEEP[0])} × 1.5 × 0.9", "1 · 1", "Glued along the ledge's and the run's front edges", "Media wall"),
            ("Keyboard tray housing", "70 × 28 × 7, sides 7 × 2", "1", "Screwed under the PC shelf", "Media wall"),
            ("Worktop", f"{n(g.ALC_W)} × {n(g.BASE_D)} × 3", "1", "From one 300 × 62 full-stave worktop; chamfered front", "Media wall"),
            ("Face frame", "186 × 73 overall, 2 thick, stiles about 5 wide", "1 set", "End stiles scribed to the walls", "Media wall"),
            ("Drawer fronts", "game drawer 56.8 × 6.5 × 2 · plinth drawer 54 × 6 × 2", "1 · 1", "Finger pull cut underneath", "Media wall"),
            ("LP crate lips · slim drawer lips", "36.3 × 5 × 1.5 · 16.5 × 5 × 1.5", "2 · 3", "Cut to the face frame's openings, less 3 mm (v16)", "Media wall"),
            ("“Now playing” ledge", f"{n(g.NOW_LEDGE['x'][1] - g.NOW_LEDGE['x'][0])} × 7 × 2.4, lip 1.5", "1", "On the breast at 104, two concealed brackets (v16; with the table by the stairs)", "Media wall"),
            ("Follower blocks · Xbox One lift block", "19 × 12 × 2 · 15 × 12 × 2", "2 · 1", "Offcuts, felted underneath", "Media wall"),
            ("Wedges · pegs · dowels", "6 × 3, tapering · 10 mm dowel, 5 long · 10 mm dowel", "2 + spares · 6 + 6 · 8", "Glued", "Media wall"),
            # v27: the dining cabinet (geometry.OPTC): the table halves, aprons, legs and hinge rail in solid oak
            ("Table halves, centres", f"{n(G.OPTC['top'][1] - 14 + 5)} × {n(G.OPTC['top'][0])} × {n(G.OPTC['top'][2])}", "2", f"Edge-glued staves: {n(G.OPTC['top'][1] - 14)} between the shoulders, plus a 2.5 tongue each end", "Dining table"),
            ("Breadboard ends", f"{n(G.OPTC['top'][0])} × 7 × {n(G.OPTC['top'][2])}", "4", "Pegged with three 10 mm pegs each, in slotted holes", "Dining table"),
            ("Apron rails", f"outer half {n(G.OPTC['top'][1] - 6)} and {n(G.OPTC['top'][0] - 12)} · inner half {n(G.OPTC['top'][1] - 7.6)} and {n(G.OPTC['top'][0] - 12)}, all × {n(G.OPTC['apron'])} × 2",
             "2 + 2 · 2 + 2", "A frame under each half, held on figure-8 fasteners", "Dining table"),
            ("Table legs", f"{n(G.OPTC['leg'][0])} × {n(G.OPTC['leg'][1])}, cut 70 long", "4", "Tapered on the two inside faces from 25 cm down to 4.5 × 3.5 at the foot; trimmed to the floor once the table's hung and level", "Dining table"),
            ("Hinge rail", f"{n(G.OPTC['bay_t'][0] - G.OPTC['bay_t'][1])} × {n(G.OPTC['in_d'])} × 7", "1", f"Across the table bay, top at {n(G.OPTC['pivot'][1])}, its front {n(G.OPTC['slide'])} back from the cabinet's front edges", "Dining table"),
        ]),
        # v29: the doors run between the ends, so the ends, the top and the floor are the full depth; everything inside stands behind the doors
        ("Oak-faced ply, 18 mm and 19 mm (the dining cabinet)", "Ask the merchant to cut it to size and edge the visible edges with oak lipping", [
            ("Cabinet ends", f"{n(G.OPTC['h'])} × {n(G.OPTC['d'])}", "2", "Full height and depth; the doors run between them", "Dining table"),
            ("Cabinet top (19 mm) · floor", f"{n(G.OPTC['z'][0] - G.OPTC['z'][1] - 2 * G.OPTC['t'])} × {n(G.OPTC['d'])}", "1 · 1", f"Between the ends; a 16 mm groove under the top and a 6 mm groove in the floor for the tracks; the floor's top face at {n(G.OPTC['plinth'])}", "Dining table"),
            ("Cabinet partition", f"{n(G.OPTC['h'] - G.OPTC['t_top'] - G.OPTC['plinth'])} × {n(G.OPTC['in_d'])}", "1", f"Makes the table bay {n(G.OPTC['bay_t'][0] - G.OPTC['bay_t'][1])} inside; set {n(G.OPTC['slide'])} back from the front", "Dining table"),
            ("Cabinet chair shelf · linen floor", f"{n(G.OPTC['bay_c'][0] - G.OPTC['bay_c'][1])} × {n(G.OPTC['in_d'])} · {n(G.OPTC['bay_t'][0] - G.OPTC['bay_t'][1])} × {n(G.OPTC['in_d'])}",
             "1 · 1", f"Top faces at {n(G.OPTC['shelf_y'] + G.OPTC['t'])} and {n(G.OPTC['flap'][0])}", "Dining table"),
            ("Sliding doors", f"{n(G.OPTC['door_w'])} × {n(G.OPTC['door_h'])}", "2", "Oak-faced both sides, grain upright, all four edges lipped; a finger slot routed near the outer end of each", "Dining table"),
            ("Drawer front (the cabinet)", f"{n(G.OPTC['bay_t'][0] - G.OPTC['bay_t'][1] - 0.3)} × {n(G.OPTC['pivot'][1] - 7 - G.OPTC['plinth'] - 0.6)}", "1", "Inside, under the folded table; a finger slot in its middle", "Dining table"),
        ]),
        ("Birch ply, 18 mm", "", [
            ("Bay 3 sides", "73 × 40", "2", "The record carcass, standing on the floor", "Media wall"),
            ("Bay 3 top and bottom", "56.4 × 40", "2", "Between the sides; back left open to the channel", "Media wall"),
            ("Plinth rails", "120 × 9", "2", "Front and back of the ladder frame under bays 1–2", "Media wall"),
            ("Plinth cross-pieces", "34.4 × 9", "3", "At both ends and under the bay 1–bay 2 joint, so the bay under bay 2 stays clear for the drawer", "Media wall"),
        ]),
        ("Birch ply, 12 mm", "", [
            ("Drawer box (the cabinet)", f"sides 16 × {n(G.OPTC['pivot'][1] - 7 - G.OPTC['plinth'] - 0.6 - 8)} · back and front {n(G.OPTC['bay_t'][0] - G.OPTC['bay_t'][1] - 2.6 - 2.4)} × {n(G.OPTC['pivot'][1] - 7 - G.OPTC['plinth'] - 0.6 - 8)}; a 6 mm base {n(G.OPTC['bay_t'][0] - G.OPTC['bay_t'][1] - 2.6)} × 16", "2 · 2 · 1", "Under the folded table: mats and coasters", "Dining table"),
            ("Game drawer sides", "35 × 15.5", "2", "", "Media wall"),
            ("Game drawer back · front panel", "51.9 × 15.5 · 51.9 × 6", "1 · 1", "", "Media wall"),
            ("LP crate bases · slim drawer bases", "34.9 × 40 · 15.3 × 40", "2 · 3", "The sides and ends stand on them (v16)", "Media wall"),
            ("Bay 3 divider", "69.4 × 38", "1", "17.8 in from the left side, the full height inside (v16)", "Media wall"),
            ("Plinth drawer sides · ends", "34 × 4.4 · 49.6 × 4.4", "2 · 2", "A 52 × 34 × 5 box", "Media wall"),
            ("Bay 2 divider · part shelf", "35.3 × 38 · 32.2 × 36", "1 · 1", "The sub's column on the left; the PS2 over the PS1 on the right", "Media wall"),
            ("Keyboard tray", "54 × 26", "1", "Oak lip on its front edge", "Media wall"),
        ]),
        ("Birch ply, 9 mm", "", [
            ("Game drawer base", "52.5 × 34.4", "1", "In a 6 mm groove", "Media wall"),
            ("LP crate sides · ends", "40 × 8 · 33.1 × 8", "4 · 4", "Two of each per crate: a 33 cm trough (v16)", "Media wall"),
        ]),
        ("Birch ply, 6 mm", "", [
            ("Cabinet back", f"{n(G.OPTC['z'][0] - G.OPTC['z'][1] - 2 * G.OPTC['t'])} × {n(G.OPTC['h'] - G.OPTC['plinth'] + G.OPTC['t'] - G.OPTC['t_top'])}", "1", "Glued and pinned across the back, between the ends, the floor and the top", "Dining table"),
            ("Game drawer cross divider", "51.9 × 9", "1", "13 cm back from the front", "Media wall"),
            ("Game drawer bin walls · bin floors", "12.6 × 9 · 16 × 12.6", "2 · 2", "Floors raked so the cases lean about 13°", "Media wall"),
            ("Plinth drawer base", "52 × 34", "1", "Screwed under the box", "Media wall"),
            ("Slim drawer sides · backs and fronts", "40 × 10 · 14.1 × 10", "6 · 6", "Three boxes 15.3 wide, 14.1 inside (v16)", "Media wall"),
        ]),
        ("Hardware", "Runners are sold in pairs", [
            ("LP crate runners · slim drawer runners", "400 mm full extension, 68–70 kg a pair · 400 mm light duty", "2 pairs · 3 pairs", "Into bay 3's sides and the divider (v16)", "Media wall"),
            ("Game drawer runners", "350 mm full extension, soft-close", "1 pair", "Accuride DZ3832EC or Screwfix 964VN", "Media wall"),
            ("Plinth drawer and keyboard tray runners", "300 mm full extension · 300 mm light duty", "1 pair · 1 pair", "", "Media wall"),
            ("Flip-top hinges", "Lee Valley 40574, solid brass, 1.27 × 7.0", "3", "Routed into the meeting edges of the two halves, 10 in from each side and the middle", "Dining table"),
            ("Piano hinge", "Altro continuous, 1800 × 50, cut to 90", "1", "The table's foot, on the hinge rail's top face (v27)", "Dining table"),
            ("Leg brackets · tabletop fasteners", "folding, self-locking · figure-8", "4 · 16", "The legs fold inside the aprons; the fasteners hold the aprons to the tops", "Dining table"),
            ("Sliding door gear", "Häfele Slido Classic 40 IF C, soft close", "1 set",
             f"The fitting set for two doors (402.33.027), a double top track (402.33.652) and a bottom guide (402.30.802), both cut to {n(G.OPTC['z'][0] - G.OPTC['z'][1] - 2 * G.OPTC['t'])}: the track in the top's groove, the guide in the floor's", "Dining table"),
            ("Drawer runners · catches · knob", "150 mm side-mount · magnetic", "1 pair · 2 · 1",
             "The runners for the drawer under the table; the two catches hold the folded table upright and the knob on its apron brings it down", "Dining table"),
            ("Sub isolation riser", "dense foam or sorbothane, about 22 × 28 × 3", "1", "Under the sub in bay 2", "Media wall"),
            ("Concealed brackets", "for the uprights; two for the PC shelf, 40 kg+ a pair", "1 set", "", "Media wall"),
        ]),
    ]


def cuts_html():
    out = ["<p>Every made part in one list, grouped by what it's cut from, for the timber merchant. Sizes are finished sizes in cm, length × width × thickness. The cut lists in the other sections say how each part joins; this list is for ordering.</p>"]
    for grp, note, rows in cuts():
        out.append(f"<h4>{grp}</h4>" + (f"<p class='note'>{note}</p>" if note else ""))
        out.append("<table class='tight cuts'><tr><th>Part</th><th>Size (cm)</th><th>Qty</th><th>Notes</th><th>Section</th></tr>"
                   + "".join(f"<tr><td>{a}</td><td class='num'>{b}</td><td class='num'>{c}</td><td>{d}</td><td>{e}</td></tr>" for a, b, c, d, e in rows)
                   + "</table>")
    return "\n".join(out)


def cuts_text():
    lines = ["Cutting list: media wall and dining wall (finished sizes in cm, length x width x thickness)"]
    for grp, note, rows in cuts():
        lines += ["", grp.upper() + (f" ({note})" if note else "")]
        lines += [f"- {a}: {b}, qty {c}" + (f" ({d})" if d else "") for a, b, c, d, e in rows]
    return "\n".join(lines)


def guide_html():
    return (GUIDE_RULES + guide_tools() + GUIDE_TECHNIQUES + "<h3>The order of work</h3>" + steps_table_html()
            + GUIDE_TIME + GUIDE_PITFALLS + "<h3>The cutting list</h3>" + cuts_html())


def guide_pdf_html():
    """The build guide PDF: the guide, then every step in full."""
    return guide_html() + "<h2 class='pb'>Step by step, in full</h2>" + full_steps_html(pdf=True)


def _plan(deck=False):
    """The plan as one HTML document. deck=True: images as art/ keys and markers kept, for the plan page's tabs."""
    global DECK
    DECK = deck
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
<p class="byline">Revised Oct 21, 2026 · @emma · version {VERSION} (revision {REVISION}), drawn to your measurements</p>

<div class="decision"><b>What changed in v29: the dining cabinet, upgraded.</b> You asked for a full upgrade of the table's design. Shut, the cabinet is now <b>two tall oak sliding doors</b> between oak ends, on a soft-close Häfele track, with nothing of the table or the chairs on show: slide door A over door B and the table comes down; slide B behind A and the chairs come out. Hinged doors couldn't work here: at the stair end a door has nowhere to fold back except where the first chair sits. The <b>table</b> is {n(G.OPTC["len"])} × {n(G.OPTC["top"][0])} (two halves {n(G.OPTC["top"][1])} long), flush at the joint, with breadboard ends, eased corners and tapered legs; six still sit in comfort and a seventh at the end. The six chairs are <b>slatted folding chairs</b> with sage seat pads, folded in the chair bay; the drawer and the linen shelf are inside, behind door A. The drawings, the cutting list, the buy list (your ticks kept) and step 11's instructions are redone for it, and nowhere in the plan is the flip-top the default any more: it's the alternative in section 5.<br><b>v28: the 3D room shows itself round, and shares.</b> Under Tools → Views, <b>Take the tour</b> flies round the room in {len(__import__("room3d_page").tour())} stops, a line about each: the whole room, the media wall, the PC wall, the breast, the dining cabinet opened for six, the sofa, the window and the view from above. <b>Copy link to this view</b> gives a link that opens the room just as you have it: where you're looking from, the table, the lights, the paint, the decor and the suggestions. Every suggestion now comes in <b>two or three versions</b> (a cream, terracotta or black pot; an oak, black or brass rim; mustard, sage or cream), chosen under Tools → Extras once it's switched on, and named in Your picks. The plan page's PDF buttons work again. The plan itself doesn't change.</div>
<div class="decision"><b>What changed in v18: your plant stand and your record shelf, and a room you can rearrange.</b> <b>Your new plant stand</b> (98 × 29.5 × 158: two five-tier towers and an open middle) and <b>your vinyl stand</b> (70 × 32 × 78: two face-out bays on top, wire dividers below) are in, at the sizes on the listings you sent (v18.1), with two layouts to choose from (section 4): <b>A, recommended</b>, the plant stand in the window's west corner, where it gets daylight from the window beside it, and the vinyl stand on the chimney breast under the “now playing” ledge, a step from the turntable; or <b>B</b>, the other way round. Your red lamp moves to the sofa's end either way. <b>The PC's clear side</b> now shows its graphics card, cooler, memory and fans. In the 3D room, <b>Edit room</b> lets you drag things around like a dolls' house, turn them, recolour them, take them out and add new ones (an armchair, a bookcase, a floor plant and more), and paint a wall, the ceiling or the skirting by tapping it; the menus are shorter for it. <b>HD with shadows</b> no longer asks more of the graphics card than it has, and if a phone does give up, the room comes back in Fast. More ideas for later (appendix). Fit proof {nfit} checks, none fail.<br><b>v17: the room finished round your notes.</b> <b>The sofa's open end</b> is now a proper ottoman end: the seat wraps round to the back as one long cushion and the frame stops 20 short, and the sofa stands 13 cm off the window wall, as in your photo. <b>The window</b> has its real deep sill, 22 cm into the reveal, with your plants along it (3D room), and the <b>curtains</b> now hang clear of it. <b>Even light by default:</b> every spot head points straight down, evenly spread, and a new <b>General</b> scene comes first; tilt a head only if its pool lands badly. Your <b>red lamp's top (green) head</b> lights the wall with your shelf. <b>The flip-top</b> is drawn as built: pegged breadboard ends and three brass hinges. <b>The stairs:</b> one wall all the way up in one colour, the living room ceiling's edge where it cuts off the view, and the banister on the room side only, as you said. <b>The PC</b> is drawn with its insides, and lights up in the 3D room (the "PC lit" button); the plan adds a <b>USB hub</b> by the sofa, a <b>remote power button</b> and a <b>dust filter</b> (section 6), and checks the soundbar against the TV's remote (section 3). Your <b>OBEGRÄNSAD</b> (905.262.63) is confirmed at IKEA's 52 × 36 × 6. The build guide PDF now <b>stands on its own</b>: each step has its own cut list and pictures. New <b>ideas</b>, off the plan and the costs, are in their own tab and in the 3D room's buttons, all off until you turn them on (appendix). Fit proof {nfit} checks, none fail.<br><b>v16: the whole wall, redesigned round everything we now know.</b> <b>No dead space in the record bay:</b> with LPs only, bay 3 splits in two. Under the turntable, two <b>snug LP crates</b> (a 33 cm trough, the width record shops use) still hold about {2 * g.TRAY_LPS} LPs face-out; beside them a <b>slim column</b> of three drawers: <b>two face-out game drawers</b> (about {g.SLIM_GAMES} DVD-size cases, flipped like the records) and a drawer for the <b>pads and remotes</b> with a charging lead, so nothing lies on the worktop (section 4). <b>The table by the stairs is now the default</b>, so the chimney breast is free: it takes a <b>“now playing” oak ledge</b> beside the turntable for the sleeve of what's on and the next two, under the two framed LPs. <b>Smart colour strips</b> in the upright grooves and under the side-wall run, in the same app as the bars' bulbs, so one scene sets the whole wall. On your shelf by the stairs: your <b>IKEA OBEGRÄNSAD</b>, black, its 16 × 16 white LEDs drawn showing a pixel music note; <b>the laser is there but off</b>; the <b>plant hangs from the shelf's window end</b>; and the <b>hollow pipe boxing</b> in the window corner (about 23 × 22, floor to ceiling) is drawn in, the shelf stopping just short of it. <b>Your hats</b> are on your red lamp, as in your photo: the graduation cap on top of the pole, the navy cap with its poem hung below the top head. <b>The sofa's end towards the TV is open</b>: no arm, one long seat cushion wrapping round to the back, an ottoman-style end. Fit proof {nfit} checks, none fail. Earlier rounds are in the appendix.</div>

<h2>1 · The plan on a page</h2>
<div class="hero">
<figure class="render">{img("render_v13_join_clean.png", "The artisan oak media wall in Card Room Green, the table by the stairs")}
<figcaption>Drawn to your measurements, in Card Room Green: the alcove with the turntable zone on the right and bay 3 split into the slim game column and the LP crates; the chimney breast free, with its “now playing” ledge (the table is by the stairs, behind this view); both spot bars. Full-resolution renders come with this plan.</figcaption></figure>
<div class="summary">
<div><b>£{money(tl, th)}</b><span>the whole plan, item by item in section 11; no electrician on top</span></div>
<div><b>{c[fit.PASS]} of {nfit}</b><span>fit checks pass outright; {c[fit.TIGHT]} are tight, {c[fit.CHECK]} need a check on site (section 3)</span></div>
<div><b>{LPS} · 6</b><span>LPs ({g.WALL_LPS} in the wall, {g.STAND_LPS} in your vinyl stand) · seats at the table, the chairs kept inside it</span></div>
</div></div>
<table><tr><th>Area</th><th>Decision</th></tr>
<tr><td>Alcove</td><td>The TV between two oak uprights, the left one now a corner post on the side wall; on the right, the turntable on the worktop and the Series X on a shelf at {n(g.RZ_SHELF_TOP)}; below, three 60 cm bays: the Xbox consoles, the PlayStations with the sub, and (v16) two snug LP crates beside a slim column of game and pad drawers.</td></tr>
<tr><td>Side wall</td><td>One oak run from the corner: a 7 cm ledge with four more LPs that sweeps out into the PC's shelf above the sofa's open end, a smart colour strip underneath, clear of the TV's sightlines.</td></tr>
<tr><td>Dining</td><td>The dining cabinet under your shelf by the stairs: one oak cabinet with the table and the six chairs inside it. The table swings down and opens to {n(g.OPTC['len'])} × {n(g.OPTC['top'][0])}, six in comfort; packed away it's a flush run of oak. The chimney breast keeps a “now playing” ledge and two framed LPs. The flip-top (by the stairs or on the breast) is the alternative (section 5).</td></tr>
<tr><td>Records and games</td><td>About {LPS} LPs: {g.WALL_LPS} in the wall, every one face-out ({2 * g.TRAY_LPS} in the LP crates, 8 on the two ledges, 3 on the “now playing” ledge), and {g.STAND_LPS} in your vinyl stand ({g.RECORD_SHELF["lps_top"]} face-out on top, {g.RECORD_SHELF["lps_bottom"]} spine-up between its wires). Games: about {48 + g.SLIM_GAMES} face-out or spine-up in the game drawers, and 32 PS1 games in the plinth drawer.</td></tr>
<tr><td>Heights</td><td>Worktop and table {n(g.WORKTOP)} · TV centre 116.5 · Series X shelf {n(g.RZ_SHELF_TOP)} · ledges and PC shelf {n(g.LEDGE_TOP)} · high shelf {n(g.HIGH_TOP)}, {n(g.CEIL - g.HIGH_TOP)} under the {n(g.CEIL)} ceiling.</td></tr>
<tr><td>Colour and light</td><td>Card Room Green No. 79, colour-drenched. The ceiling LED strip, smart colour strips in the uprights and under the side run, a bias light, and two Wolston-style spot bars with smart colour bulbs on your two existing ceiling points; one app, one scene for the lot.</td></tr>
<tr><td>Power and network</td><td>Your own job: the side-wall socket becomes a double, left for the 10-gang (everything modern, the PC included), right for the retro set, switched at the wall. Deco A in bedroom 3, Cat6 down the airing cupboard.</td></tr>
</table>
<p class="confirm"><b>To confirm (section 12):</b> {questions.summary_line()}.</p>
</div>

<h2 class="pb">2 · The room</h2>
<p>Everything is drawn from your hand-measured sketch; where the agent's floor plan disagrees, your tape wins. The L-sofa is drawn from your photo<sup>{fit.ORDER.index("sofa") + 1}</sup>: its long side ends in line with the breast's reveal (about {n(g.SOFA_W)} cm); the return along the side wall is a typical {n(g.SOFA_D)} until you measure it. Since v17 its end towards the TV is an <b>ottoman end</b> (no arm; the seat wraps round, the back stops {n(g.SOFA_OTTOMAN)} short) and it stands {n(g.SOFA_BACK_Z - g.WINDOW_Z)} cm off the window wall, clear of the curtains. The window has a <b>deep sill</b>, {n(g.WINDOW_REVEAL)} cm into the reveal at {n(g.SILL["y"])} from the floor, with your plants along it.</p>
<figure>{living_plan()}</figure>
<figure class="render">{img("render_v29_3d_room.png", "The whole room in 3D, the Bright preset")}
<figcaption>The whole room in 3D, from above the window side, the dining cabinet packed away by the stairs: your blue sofa with its open end, the rug, the bars running towards the window, the “now playing” ledge on the breast. On the plan page you can walk round it, switch the table's wall, slide every light, colour the smart bulbs, paint the walls, ceiling and skirting separately, and save any view in HD.</figcaption></figure>
<table class="tight"><tr><th>From your sketch</th><th>mm</th><th>Notes</th></tr>
<tr><td>Room, east to west along the window</td><td class="num">{n(g.ROOM_W*10)}</td><td>The media wall is the south wall, shared with the hall and garage</td></tr>
<tr><td>Window wall to the alcove's back wall</td><td class="num">{n(g.ROOM_D*10)}</td><td>To the chimney breast's face: {n((g.ROOM_D - g.ALC_D)*10)}</td></tr>
<tr><td>Ceiling</td><td class="num">{n(g.CEIL*10)}</td><td></td></tr>
<tr><td>TV alcove, east wall to the breast</td><td class="num">{n(g.ALC_W*10)} × {n(g.ALC_D*10)}</td><td>Floor to ceiling</td></tr>
<tr><td>Chimney breast</td><td class="num">{n(g.BREAST_W*10)}</td><td>Projects 380 on the alcove side, 390 on the west side: the dining wall</td></tr>
<tr><td>Window and radiator (north wall)</td><td class="num">2350 · 1370</td><td>Window starts 730 from the east wall; radiator ends 130 inside its west end; the glass from {n(g.WINDOW_Y[0]*10)} to {n(g.WINDOW_Y[1]*10)} up, set {n(g.WINDOW_REVEAL*10)} back in its reveal over a deep sill (v17, from your note; the depth is drawn, please check it)</td></tr>
<tr><td>Skirting</td><td class="num">60 × 20</td><td>White now; Card Room Green eggshell in the plan</td></tr>
<tr><td>West end: recess, door, stair box</td><td class="num">935 / 1045 / 660 / 820</td><td>Drawn roughly: please confirm which is which</td></tr>
<tr><td>Stairs, beside the door</td><td class="num">820 wide</td><td>They go <b>up</b> to the first floor (you confirmed), behind a wooden banister; drawn rising away from the room until you send a photo</td></tr>
</table>
<p><b>From the sofa:</b> from the middle of the long side your eyes are about {s["view_dist"]/100:.2f} m from the screen, which a 55-inch fills at about {s["view_angle"]:.0f}°: right for TV and games. With the TV {n(g.TV_SHIFT)} cm nearer the side wall, it now sits square on to the end of the sofa's return ({n(s["chaise_dist"])} cm away), and only about {s["sofa_mid_off_axis_deg"]:.0f}° off-centre from the middle of the long side. The screen's centre at 116.5 cm is 1–2.5° above a seated eye line. Both spot bars hang {n(g.BAR[2])} cm, so the lowest shade is at {n(g.CEIL - g.BAR[2])} cm: no headroom worries.</p>
<h3>The house</h3>
<figure>{house()}</figure>
<p>Deco A and Switch 1 sit with the Hub 5 and the gaming PCs in bedroom 3; both Cat6 runs go across the landing and drop through the airing cupboard, which sits over the alcove's corner (section 9).</p>

<h2 class="pb">3 · The media wall</h2>

<figure class="render">{img("render_v13_join_key_scene.png", "Render with numbered parts")}
<figcaption>Numbered view: the game drawer and the lower LP crate are pulled out 30 cm, with a view of each from above. Dashed lines show what's hidden: gold for data, audio and low-voltage leads, coral for mains. The sofa isn't drawn so the base stays in view; the room plan shows it.</figcaption></figure>
{key_table()}

<h3>Built to your alcove: {n(g.ALC_W)} wide, {n(g.ALC_D)} deep, {n(g.CEIL)} to the ceiling</h3>
<ul>
<li><b>Base:</b> 3 cm filler, three 60 cm bays, 3 cm filler. Bays 1 and 2 are IKEA BESTÅ 60×40×64 frames on a 9 cm plinth (tops at 73, back panels off); bay 3 is an 18 mm ply carcass 60 × 40 × 73 from the floor, split by a 12 mm divider into the slim game column (two face-out game drawers and the pads drawer) and the LP column (two face-out LP crates) under the turntable. One oak face frame runs across all three; its bottom rail hides the plinth and a hidden drawer under bay 2 with a finger pull (no push-to-open at floor level).</li>
<li><b>Depth:</b> 40 cm frames, a 4 cm cable channel behind and the 2 cm face frame make {n(g.BASE_D)} cm from the back wall, {n(g.BASE_PROUD)} cm proud of the chimney breast.</li>
<li><b>Worktop:</b> solid oak, {n(g.ALC_W)} × {n(g.BASE_D)} × 3, top at 76, with a brush-lined slot behind the TV and a grommet behind the deck.</li>
<li><b>Oak uprights:</b> 4.5 × 30 cm, {n(g.UPRIGHT_LEN)} cm from the worktop to the ceiling. The left one stands against the side wall at {n(g.UP_L[0])}–{n(g.UP_L[1])}, a corner post that frames the TV and carries the wrap ledge. The right one is at {n(g.UP_R[0])}–{n(g.UP_R[1])}. That leaves {n(g.TV_GAP)} cm between them, {n(g.TV_CLEAR)} cm clear of the TV each side.</li>
<li><b>TV:</b> centre {n(g.TV_CX)} cm from the side wall (it was 93), on LG's stand set 2 cm off the back wall: bottom {n(g.TV_BOTTOM)}, centre 116.5, top {n(g.TV_TOP)}. The soundbar sits centred under it at the worktop's front edge.</li>
<li><b>The turntable zone:</b> {n(g.RZ_W)} cm between the right upright and the breast. The deck sits on the worktop with {n((g.RZ_W - g.DECK[0]) / 2)} cm each side and its lid opens to about {n(round(g.LID_TOP_OPEN))}. Above it is an oak shelf at {n(g.RZ_SHELF_TOP)}, through-tenoned into the upright, carrying the Series X on its fan stand; the phono preamp hangs underneath at the back.</li>
<li><b>Shelves above:</b> the record ledge at 155.4 between the uprights, four LPs face-out; the high shelf at 196, wall to wall in two lengths, with books, a box, a print, a small framed sleeve and Deco B.</li>
<li><b>Bay 2 with the sub (v13.5):</b> the PS3 keeps the top row. Below its shelf the bay splits: on the left the sub's column, {n(g.SUB_COL[1] - g.SUB_COL[0])} cm wide, then a 12 mm ply divider, then {n(g.PS_COL[1] - g.PS_COL[0])} cm for the PS2 over the PS1 on a part shelf. The sub stands on a {n(g.SUB_RISER_H)} cm isolation riser with 1 cm each side and {n(g.SUB_COL_TOP - g.SUB_IN["y"][1])} above. Its front is flush with the face frame, so its driver faces the room and its rear port has {n(g.SUB_PORT_GAP)} cm to the wall.</li>
<li><b>Power:</b> the side-wall socket in front of bay 1 becomes a double. Its two leads enter through a notch at the left end of the face frame's bottom rail and run back through the plinth to the channel.</li>
</ul>
<div class="why"><b>The media wall, looked over again (v17)</b>
<ul>
<li><b>The TV's remote:</b> the soundbar's top is 0.6 above the screen's bottom edge, right where LG puts the remote's receiver. Sit the bar 2 cm proud of the stand's foot so the beam from the sofa clears it; LG's Magic Remote works by radio once paired, so it doesn't mind either way (a check in the fit proof).</li>
<li><b>Heat:</b> every console bay is open front and back, the bricks lie flat at the back with nothing on top, and the Series X has 15 cm each side and 21 above.</li>
<li><b>One remote for most of it:</b> HDMI-CEC (SIMPLINK) lets the TV's remote work the soundbar and the modern consoles (step 13); the HDMI switch has its own remote for the retro side.</li>
</ul></div>
<figure>{front()}</figure>
<figure>{section()}</figure>
<h3>The sub in the media wall</h3>
<p>You asked for the sub back in the unit, with the Xbox bricks moved behind. It fits, and it sits in the best spot for it: under the TV, beside the soundbar, so the bass comes from the same place as the picture. Here's how the base makes room, and what was checked.</p>
<ul>
<li><b>The bricks go to the back.</b> The Xbox One's brick (17 × 7.5 × 4.8<sup>{fit.ORDER.index("xb1psu") + 1}</sup>) and the Xbox 360's (allowed 21 × 10 × 6<sup>{fit.ORDER.index("x360psu") + 1}</sup>) lie flat at the back of their shelves, by the channel's power leads. Microsoft asks for a ventilated space, flat on the rubber pads, with nothing on top<sup>{fit.ORDER.index("psuplace") + 1}</sup>; the bays are open front and back.</li>
<li><b>That frees bay 1's fronts</b> beside the two Xboxes, so the HDMI switch (beside the Xbox One, where its remote reaches it) and the RetroTINK (beside the Xbox 360) move up from bay 2.</li>
<li><b>Bay 2's lower half becomes two columns:</b> the sub on the left, under the TV, and the PS2 over the PS1 on the right. The sub is {n(g.SUB[0])} × {n(g.SUB[2])} × {n(g.SUB[1])}<sup>{fit.ORDER.index("hisense") + 1}</sup>; its column is {n(g.SUB_COL[1] - g.SUB_COL[0])} wide and {n(g.SUB_COL_TOP - g.SUB_COL_FLOOR)} tall.</li>
<li><b>The port:</b> the sub's front sits flush with the face frame, so its rear port is {n(g.SUB_PORT_GAP)} cm from the wall through the open back and the channel. That's inside the 15–30 cm advised for a rear port<sup>{fit.ORDER.index("subport") + 1}</sup>, at the low end, so the channel behind bay 2 stays clear: Switch 2 and the retro 6-way move behind bay 1.</li>
<li><b>Vibration, the one thing to test:</b> Microsoft advises keeping the Xbox 360 away from subwoofers<sup>{fit.ORDER.index("x360place") + 1}</sup>, and the deck shares the worktop. The 360 is a whole bay away, the sub stands on an isolation riser without touching the divider or the frame, and the deck has isolation feet. Once it's built, play a disc game and a record at film volume. If anything skips, turn the sub down for that source; if it still does, the sub can go back under the dining wall.</li>
<li><b>The dining wall is clear underneath:</b> no cover to make, and nothing to move for eight at the table.</li>
</ul>

<h3>The fit proof: every item against its published size</h3>
<p>Each zone lists what goes in it, its size and its source (section 12), the space, what's left and a verdict. {c[fit.PASS]} of the {nfit} checks fit outright and none fail; {c[fit.TIGHT]} are tight, most of them snug by design; {c[fit.CHECK]} need a check on site (the TV's plugs, the RetroTINK's size, the sub's vibration, the soundbar and the TV's remote eye, the stairs wall, your shelf's height and, for option A, the flip-top's end on the breast).</p>
<!--fit-->{fit.tables_html()}<!--/fit-->

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

<h3>The drawer layouts</h3>
<p>Seven drawers in the alcove base, all drawn to scale from above: <b>A</b> the game drawer (bay 1), <b>B</b> the hidden plinth drawer under bay 2, <b>C</b> and <b>D</b> the two face-out LP crates and <b>E</b> to <b>G</b> the slim drawers beside them (bay 3). Each one shows its compartments, what goes in them and how many, and its runners. Every front is a plain oak lip with a finger pull cut underneath.</p>
<figure>{drawer_layouts()}</figure>
<figure class="render">{img("render_v13_drawers.png", "Every drawer out: the game drawer, the upper LP crate, a slim game drawer and the plinth drawer")}
<figcaption>Every drawer out, in place: the game drawer, the upper LP crate and the middle slim game drawer 30 cm out, the plinth drawer 25 cm out. In use, open one LP crate at a time (a full one is about 30 kg).</figcaption></figure>
<h3>The game drawer (bay 1, bottom row)</h3>
<p>Unchanged. Two display bins at the front show covers face-out even with the drawer shut (Xbox left, PS2 right, a small tray between them); behind them the rest of the games stand on edge with the spine on top, so every title faces up when you roll it out.</p>
<figure>{game_drawer()}</figure>
<ul>
<li><b>Box:</b> about 54.3 × 35 cm outside on 350 mm full-extension soft-close runners screwed to the BESTÅ sides; sides 15 cm; 9 mm base lined in felt. About 48 games.</li>
<li><b>Runners:</b> Accuride DZ3832EC (43 kg) or Screwfix Essentials 964VN (40 kg); not IKEA's BESTÅ runners, which aren't full extension.</li>
<li><b>The bricks:</b> both Xbox bricks lie flat at the back of their shelves, on their rubber pads, beside the channel's power leads, with nothing on top. Microsoft only asks that the space is ventilated<sup>{fit.ORDER.index("psuplace") + 1}</sup>, and these bays are open at the front and the back.</li>
</ul>

<h2 class="pb">4 · The records and the turntable</h2>
<h3>Your plant stand and your vinyl stand (v18)</h3>
<ul>
<li><b>Your plant stand:</b> 98 × 29.5 × 158. Two slatted towers of five tiers, with an open middle holding two shelves for taller plants.</li>
<li><b>Your vinyl stand:</b> 70 × 32 × 78. A black steel frame and rustic wood: two face-out bays on top, LPs standing between wire dividers below.</li>
<li><b>Sizes</b> from the listings you sent<sup>{fit.ORDER.index("plantstand") + 1},{fit.ORDER.index("vinylstand") + 1}</sup>.</li>
<li><b>Two good places:</b> the window's west corner and the chimney breast (free now the table is by the stairs), so two layouts. In the 3D room, Tools › Layout switches between them; in Edit room you can drag either anywhere.</li>
</ul>
<ul>
<li><b>A, recommended: plants in the window corner, records on the breast.</b><ul>
<li>The plant stand goes against the window wall, between the curtains' stack and the pipe boxing: {n(g.PIPE_BOX["x"][0] - g.WINDOW_X[1] - g.CURTAIN["ext"])} cm for its 98, so 4.5 each side. Measure before it goes in; if it's tight, open the curtains' stack a little towards the window.</li>
<li>Its plants get daylight from the window beside them; at 158 it leaves 77 to the ceiling.</li>
<li>The vinyl stand goes on the breast, centred, under the “now playing” ledge ({n(g.NOW_LEDGE["top"] - g.NOW_LEDGE["t"] - g.RECORD_SHELF["h"])} cm clear). Pick a record from its top bays, play it on the deck an arm's reach away, stand its sleeve on the ledge.</li>
<li>About {g.RECORD_SHELF["lps_top"] + g.RECORD_SHELF["lps_bottom"]} more LPs.</li></ul></li>
<li><b>B: records in the window corner, as today, plants on the breast.</b><ul>
<li>The plants become the breast's display, 9.75 cm clear each side.</li>
<li>At 158 tall the stand comes up past the two frames, so the frames go up above it (or elsewhere) and the “now playing” ledge comes off.</li></ul></li>
<li><b>Either way:</b><ul>
<li>Your red lamp moves from the window corner to the sofa's west end.</li>
<li>Drip trays or a waterproof mat under the pots protect the slats and the carpet.</li>
<li>Felt pads under the vinyl stand.</li></ul></li>
</ul>
<figure class="render">{img("render_v29_3d_plants_corner.png", "Layout A: your plant stand in the window corner")}
<figcaption>Layout A, from the 3D room: your plant stand in the window's west corner, its towers and open middle full of plants.</figcaption></figure>
<figure class="render">{img("render_v29_3d_records_breast.png", "Layout A: your vinyl stand on the breast")}
<figcaption>Layout A: your vinyl stand on the chimney breast, under the “now playing” ledge, beside the turntable.</figcaption></figure>
<figure class="render">{img("render_v29_3d_plants_breast.png", "Layout B: the plant stand on the breast")}
<figcaption>Layout B: the plant stand on the breast instead; the vinyl stand goes back to the window corner.</figcaption></figure>
<p>The vinyl is in one place, in the alcove: the deck on the worktop, the records in the two LP crates right underneath it, the preamp tucked under the shelf above, and (v16) the “now playing” ledge on the breast an arm's reach away. Pull a crate, pick a record, play it, and stand its sleeve on the ledge.</p>
<figure>{drawer()}</figure>
<h3>How bay 3 works (v16)</h3>
<ul>
<li><b>Why it changed:</b> with LPs only, v15's trays had about 10 cm of empty width each side. Now a 12 mm divider splits the bay: the LP crates take only the width LPs need, and the rest becomes a slim column that does a job.</li>
<li><b>The LP crates:</b> a {n(g.TRAY_INSIDE)} cm trough, the snug width record shops use<sup>{fit.ORDER.index("crate") + 1}</sup>: the sleeves stand with a little play and you flip them by their top edges. They lean back 10°; the last one leans on a raked oak rest. Outer sleeves up to 32.4 still fit.</li>
<li><b>Capacity:</b> about {g.TRAY_LPS} LPs per crate; two crates, about {2 * g.TRAY_LPS} LPs, the same as before.</li>
<li><b>The slim column:</b> three drawers {n(g.SLIM_BOX_X[1] - g.SLIM_BOX_X[0])} wide, {n(g.SLIM_INSIDE)} inside. The bottom two hold DVD-size game cases face-out (13.5 wide), about {g.SLIM_DRAWERS[0]["n"]} each, flipped like the records. The top one holds four pads on edge<sup>{fit.ORDER.index("pads") + 1}</sup>, the TV, soundbar and streaming remotes, and a USB-C lead fed from the 10-gang to charge a pad in the drawer.</li>
<li><b>Runners:</b> 400 mm full extension everywhere; 68–70 kg a pair under the crates. A full crate weighs about 30 kg: open one at a time, and fit the anti-tip brackets before loading.</li>
</ul>
<table class="tight"><tr><th>Dimension</th><th>Figure</th><th>How it adds up</th></tr>
<tr><td>Bay 3 carcass</td><td>60 × 40 × 73 outside, 56.4 × 69.4 inside</td><td>18 mm birch ply; back open to the channel; a 12 mm divider 17.8 in from the left</td></tr>
<tr><td>Across the bay</td><td>15.26 + 2.54 + 1.2 + 34.86 + 2.54 = 56.4</td><td>Slim drawer, its runners, the divider, the LP crate, its runners: nothing left over</td></tr>
<tr><td>LP crate</td><td>34.86 × 40 outside, 33.06 × 38.2 inside</td><td>9 mm sides and ends; 0.8 either side of a 31.4 sleeve</td></tr>
<tr><td>Slim drawers</td><td>15.26 × 40 outside, 14.06 inside</td><td>6 mm sides; bases at 2.3, 25.1 and 47.9</td></tr>
<tr><td>Lower crate · upper crate</td><td>Undersides 2.3 · 37.0; sleeves to 34.4 · 69.1</td><td>2.6 and 2.1 cm finger room; top panel at 71.2</td></tr>
</table>
<h3>The turntable zone</h3>
<ul>
<li><b>The deck:</b> on isolation feet, 2 cm back from the worktop's front edge, with {n(g.ALC_D - g.DECK_Z[1])} cm behind it for the lid's hinges. The zone takes a deck up to the size of an AT-LP120X (45.2 × 35.2 cm); most decks are smaller.</li>
<li><b>The lid:</b> AT's cover is 44.1 × 34.6 cm<sup>{fit.ORDER.index("lid") + 1}</sup>, so standing open its top edge is at about {n(round(g.LID_TOP_OPEN))}; the shelf's underside is at {n(g.LID_CLEAR_TO)}.</li>
<li><b>Bass:</b> the sub is in bay 2, in the same base the deck sits on. It stands on an isolation riser, clear of the divider and the frame, and the deck stands on isolation feet. If a record skips or hums at film volume, turn the sub down for vinyl.</li>
<li><b>Signal path:</b> turntable set to PHONO → the preamp under the shelf → a 2 m RCA-to-3.5 mm lead down the groove behind the right upright and along the back of the worktop to the soundbar's AUX. If the deck has no PHONO/LINE switch, plug it straight into the AUX.</li>
<li><b>Soundbar:</b> Music mode, bass up, surround, night and dialogue modes off. Always the AUX cable, never Bluetooth.</li>
</ul>
<h3>Storage options, to scale</h3>
<figure>{storage()}</figure>
<h3>Where every record lives</h3>
<table class="tight"><tr><th>Where</th><th>What</th><th>How many</th></tr>
<tr><td>Bay 3, the two LP crates</td><td>LPs, face-out</td><td>About {2 * g.TRAY_LPS} LPs</td></tr>
<tr><td>The breast (v16)</td><td>The “now playing” ledge</td><td>3 LPs, the one that's on and the next two</td></tr>
<tr><td>Above the TV</td><td>Oak record ledge, the "now playing" wall</td><td>4 LPs</td></tr>
<tr><td>Side wall</td><td>The oak run round the corner</td><td>4 LPs</td></tr>
<tr><td>Your vinyl stand (v18.1)</td><td>LPs, face-out on top, spine-up below</td><td>About {g.STAND_LPS} LPs ({g.RECORD_SHELF["lps_top"]} + {g.RECORD_SHELF["lps_bottom"]})</td></tr>
<tr class="total"><td>Total</td><td></td><td>About {LPS} LPs: {g.WALL_LPS} in the wall, every one face-out, and {g.STAND_LPS} in the stand</td></tr>
</table>
<p>If the collection is bigger than this, tell me the count. The neatest overflow is another LP column like bay 3's (40 wide, two crates, 180 LPs), or LPs spine-out on the high shelf.</p>

<h2 class="pb">5 · The dining wall</h2>
{cabinet_html()}
<h3>The alternative: the flip-top, by the stairs (B) or on the breast (A)</h3>
<p>Before the cabinet, the plan was a flip-top table. It stays here, drawn, checked and costed, in case you'd rather: with its chair cupboard it comes to about £{money(*fliptop_cost())}, against the cabinet's £{money(sum(r[4] for r in cabinet_rows()), sum(r[5] for r in cabinet_rows()))}. It's a <b>flip-top gate-leg table that never leaves the wall</b>. A solid oak top, {n(g.TABLE[0])} × {n(g.TABLE[1])} cm, hangs on lift-off hinges on an oak backboard and rests on two folding brackets. A second {n(g.FLIP['leaf'][0])} × {n(g.FLIP['leaf'][1])} oak half is hinged to its front edge on three brass flip-top hinges<sup>{fit.ORDER.index("fliphinge") + 1}</sup>: flip it out and the table runs {n(g.OPEN_LEN)} cm into the room, its far end on a folding oak gate leg, at the same {n(g.TABLE_TOP)} cm as the worktop. Four sit with room to spare, six elbows-in; by the stairs a seventh sits at its end. Every day it folds flat against the wall, about {n(g.FOLDED_D)} cm deep. Nothing comes off the wall.</p>
<figure class="render">{img("render_v13_dining_four.png", "Option A: the flip-top open and set for four on the chimney breast")}
<figcaption>Option A, open on the breast and set for four: the top on its brackets, the half flipped out beyond it on its gate leg, two down each side. Bar 2, on the pendant point by the stairs just out of view, lights the table and the framed LPs.</figcaption></figure>
<figure class="render">{img("render_v13_dining_six.png", "The flip-top open and set for six, with both spot bars")}
<figcaption>Set for six, three down each side ({n(g.OPEN_LEN / 3)} cm each: elbows in). The camera stands back in line with the alcove's edge, so both spot bars show. The table's end stops {n(g.OPEN_Z[1] - g.SOFA_FRONT_Z)} cm short of the sofa, so on the breast nobody sits at its end.</figcaption></figure>
<figure>{fliptop()}</figure>
<h3>The flip-top's two places: under your shelf by the stairs (B), or the chimney breast (A)</h3>
<p>You asked (v14) what it would look like on the wall going up the stairs, under your 2 m shelf. Your photos put that wall at about {n(g.STAIRS_WALL_Z[0] - g.WINDOW_Z)} cm from the stair box to the window corner, with the shelf about {n(g.SHELF_B['top'])} cm up. The flip-top works on either wall: only the backboard's fixings change. Both are drawn in the 3D room on the plan page, folded and open, from every angle and in each lighting scene.</p>
<figure>{dining_sites()}</figure>
<figure class="render">{img("render_v29_3d_dining_B_four.png", "Option B in 3D: the flip-top open under the shelf by the stairs")}
<figcaption>Option B in the 3D room, set for dinner: the flip-top open into the room under your shelf, bar 2 on the existing pendant point over it, the stairs behind the first chairs.</figcaption></figure>
<figure class="render">{img("render_v29_3d_B_folded.png", "Option B folded under the shelf")}
<figcaption>Option B folded on an everyday evening: {n(g.FOLDED_D)} cm deep against the wall, {n(g.SHELF_B['top'] - g.SHELF_B['t'] - g.FOLDED_TOP)} cm under the shelf with your black OBEGRÄNSAD panel, the laser (off) and the plant hanging from the window end beside the pipe boxing; your red lamp in the corner.</figcaption></figure>
<ul>
<li><b>A, on the breast (the alternative): up to six.</b> It opens towards the window, {n(-g.OPEN_Z[1])} cm out, three a side. Its end stops {n(g.OPEN_Z[1] - g.SOFA_FRONT_Z)} cm short of the sofa, so there's no seat at the end; for six, slide the coffee table towards the TV first; the west side's first chair sits in the door's swing, so keep the door shut while you eat (or rehang it to open into the hall).</li>
<li><b>B, by the stairs: up to seven.</b> It opens into the room from the stairs wall, three a side and one at the end, right under the existing pendant point and out of the door's swing; it frees the chimney breast. The side chairs are tight ({n(g.STAIRS_WALL_Z[0] - g.TABLE_B_Z[0] - g.CHAIR[1] + 8)} cm to the stair box behind the stair side, {n(g.TABLE_B_Z[1] - g.WINDOW_Z - g.CHAIR[1] + 8)} to the window wall), so tuck them in after a meal; your red lamp moves from the window corner while it's open. The west wall's build is unknown: knock on it before choosing (solid takes plugs; studwork means fixing the backboard into the studs).</li>
<li><b>What moves for B:</b> the dresser goes (its turntable and records already have homes in the media wall, all face-out); the sofa stays where it is.</li>
</ul>
<h3>The flip-top's chairs: a chair cupboard built in beside it (B)</h3>
<p>You asked for "a fully pack away setup", with "ideally 6 folding chairs but 4 is fine". So the chairs get their own oak cupboard, built in beside the table, in the {n(g.CHAIR_STORE["cupboard"]["z"][0] - g.CHAIR_STORE["cupboard"]["z"][1])} cm gap between the table's window end and the pipe boxing. The table itself doesn't change or move. Folded, the table and the cupboard read as one run of plain oiled oak under your shelf, with nothing left out. The chairs drawn are IKEA FRÖSVI, TERJE's successor at the same size<sup>{fit.ORDER.index("frosvi") + 1}</sup>: they fold to about {n(g.CHAIR_FOLDED[0])} × {n(g.CHAIR_FOLDED[1])} × {n(g.CHAIR_FOLDED[2])}.</p>
<figure>{chair_storage()}</figure>
<figure class="render">{img("render_v29_3d_chairs.png", "The chair cupboard beside the folded table, doors open, four chairs inside")}
<figcaption>In the 3D room, doors open: two folded chairs stand on the cupboard's floor and two on its shelf, each pair one behind the other. Doors shut, it's a plain oak column flush with the pipe boxing.</figcaption></figure>
<ul>
<li><b>The cupboard:</b> {n(g.CHAIR_STORE["cupboard"]["z"][0] - g.CHAIR_STORE["cupboard"]["z"][1])} wide × {n(g.CHAIR_STORE["cupboard"]["d"])} deep × {n(g.CHAIR_STORE["cupboard"]["h"])} tall, in oak (or oak-faced ply) like the table. At {n(g.CHAIR_STORE["cupboard"]["d"])} deep it stands no further out than the pipe boxing beside it, and it stops 2 cm under your shelf. A fixed shelf at {n(g.CHAIR_STORE["cupboard"]["shelf_y"])} has a 3 cm lip. Two doors, upper and lower, are hinged on the table's side. About £120–240 with the hinges and latches. It's in the cutting list.</li>
<li><b>Four inside:</b> two chairs stand on the floor and two on the shelf, each pair one behind the other: 2.2 cm a side and 1.6 cm to spare in the depth, so they can't rattle. The floor takes their weight; two screws through the top rail into the wall stop the cupboard tipping.</li>
<li><b>Six inside, if you'd rather:</b> build it {n(g.CHAIR_STORE["cupboard"]["d6"])} deep and the chairs go three deep, so all six pack away. It then stands {n(g.CHAIR_STORE["cupboard"]["d6"] - g.CHAIR_STORE["cupboard"]["d"])} cm proud of the boxing's face. With the {n(g.CHAIR_STORE["cupboard"]["d"])}-deep one, chairs five and six go in the garage (v23: under the stairs is a brick side wall with plasterboard beneath, so there's no way in from the room).</li>
<li><b>Using it:</b> open the doors and take the chairs out, then open the table. With the table open, the window side's first chair starts where the cupboard ends. That changes nothing for four; six are elbows-in on that side.</li>
<li><b>The cheaper option:</b> two 200 mm storage hooks<sup>{fit.ORDER.index("slhook") + 1}</sup> in the same gap hold the same four, two on each, for £8–15. The chairs stay on show.</li>
<li><b>Not at the stair end:</b> that gap is {n(g.CHAIR_STORE["stair_gap"][0] - g.CHAIR_STORE["stair_gap"][1])} cm, too narrow for a {n(g.CHAIR_FOLDED[0])} cm chair, and the foot of the stairs has to stay clear. It takes a fold-down seat, though (below).</li>
</ul>
<h3>More ways to keep the chairs with the flip-top (B)</h3>
<p>You asked us to "explore any further ways we can build the chairs into the table build". With the flip-top, the cupboard is the way; these two go with it or instead of it, and both are in the fit proof (section 3).</p>
<figure>{chair_options()}</figure>
<figure class="render">{img("render_v29_3d_seat.png", "The fold-down seat at the stair end, down")}
<figcaption>Option 3 in the 3D room (Layout, "Fold-down seat at the stair end"): the seat down beside the folded table.</figcaption></figure>
<ul>
<li><b>Behind the folded top:</b> make the table's backboard {n(g.BEHIND_TOP["gap"])} cm deeper and four folded chairs hang behind the folded top on two hooks, two across and two deep, with a {n(g.BEHIND_TOP["upstand"])} cm oak upstand under the top hiding their feet. Folded, nothing shows; open the table and they're right there. The cost: the table stands {n(g.BEHIND_TOP["rail"] + g.TABLE[2])} cm off the wall instead of {n(g.RAIL[2] + g.TABLE[2])}, {n(g.BEHIND_TOP["gap"])} cm further into the room, folded and open. With the cupboard as well, all six chairs (or eight) pack away. About £40–80.</li>
<li><b>A fold-down seat at the stair end:</b> an oak seat {n(g.WALL_SEAT["w"])} × {n(g.WALL_SEAT["d"])} on two folding bench brackets<sup>{fit.ORDER.index("fbracket") + 1}</sup> (330 mm, 150 kg a pair) in the {n(g.CHAIR_STORE["stair_gap"][0] - g.CHAIR_STORE["stair_gap"][1])} cm gap. Folded it's {n(g.WALL_SEAT["fold"] + g.WALL_SEAT["t"])} cm proud, flatter than the table beside it; down, it's a seat at {n(g.WALL_SEAT["h"])} at the table's south end, so a fifth place is always there without a chair to fetch. About £50–90; knock the wall first for the fixings. In the 3D room: Layout, "Fold-down seat".</li>
<li><b>Ones we looked at and set aside:</b> stools stored in the gate leg's frame (the frame is only {n(g.FLIP["gate_t"])} cm deep); a storage bench under the table (it would stop the table folding flat); chairs under the stairs (a brick side wall, v23).</li>
</ul>
<h3>How the flip-top works</h3>
<ul>
<li><b>The top and the half:</b> solid oak with <b>pegged breadboard ends</b>, 7 cm oak strips across each end on a tongue, pinned with three oak pegs in slotted holes so the boards can move. They stop the panels cupping when they live upright, and they frame them like the uprights frame the TV. Rounded 5 cm corners on the half's free end, 1 cm chamfers underneath so it reads slim.</li>
<li><b>Backboard and hinge rail:</b> oak, {n(g.RAIL[0])} × {n(g.RAIL[1])} × 3 from the worktop's offcut, screwed to the wall with plugs every 20 cm; along its top, a {n(g.RAIL[0])} × 4 × {n(g.RAIL[2] - 3)} oak hinge rail stands it out so the folded half and its gate fit behind the top. The rail's top is flush with the open table, at {n(g.RAIL_TOP)} under the top.</li>
<li><b>Brackets:</b> two Häfele Hebgo heavy-duty folding brackets (287.43.428: 580 mm arm, 500 kg a pair<sup>{fit.ORDER.index("hebgo") + 1}</sup>), {n(g.HEBGO_X[1] - g.HEBGO_X[0])} cm apart on the backboard's face, under the top. Raised, they lock on their own; a light lift on the arm releases them.</li>
<li><b>Hinges:</b> three 100 mm lift-off hinges<sup>{fit.ORDER.index("liftoff") + 1}</sup> along the rail's front edge carry the top; three brass flip-top hinges, {n(g.FLIP['hinge'][0])} × {n(g.FLIP['hinge'][1])} cm, set into the meeting edges of the top and the half, open to 180°, so the half lies flat on the top to fold and flush with it open.</li>
<li><b>The gate leg:</b> two tapered oak legs ({n(g.LEG[0])} to {n(g.LEG[1])} cm, {n(g.GATE_LEG_H)} long<sup>{fit.ORDER.index("legs") + 1}</sup>) joined by a 7 cm oak apron, hinged under the half {n(g.FLIP['hinge_in'])} cm in from its far edge on two butt hinges, with a folding stay each side to lock it upright. It folds flat inside the half, along its 80 cm.</li>
<li><b>Folded:</b> two oak turn buttons on the wall, plus a magnetic catch, hold the top edge at {n(g.FOLDED_TOP)}. The top's underside faces the room: plain oiled oak between the pegged breadboard ends, so folded up it reads as a calm oak panel under the two framed LPs. It's about {g.TABLE[0] * g.TABLE[1] * g.TABLE[2] * 0.72 / 500 + 3:.0f} kg to swing up or down: two people, one at each corner.</li>
<li><b>Chairs:</b> drawn at IKEA TERJE size (43 × 49, seat 48<sup>{fit.ORDER.index("terje") + 1}</sup>), now sold in the UK as FRÖSVI at the same size<sup>{fit.ORDER.index("frosvi") + 1}</sup>; it folds flat and hangs on a hook (above). Any dining chair with a 45–48 cm seat works.</li>
</ul>
<figure>{seating()}</figure>
<table class="tight"><tr><th>Seats</th><th>Where</th><th>Per diner</th><th>Clearances</th></tr>
<tr><td>Four</td><td>Either wall, open: two down each side</td><td>{n(g.OPEN_LEN / 2)} each</td><td>On the breast its end is {n(g.OPEN_Z[1] - g.SOFA_FRONT_Z)} from the sofa; by the stairs the side chairs tuck in</td></tr>
<tr><td>Six</td><td>Either wall, open: three down each side</td><td>{n(g.OPEN_LEN / 3)} each (55 is a squeeze)</td><td>On the breast slide the coffee table towards the TV and keep the door shut</td></tr>
<tr><td>Seven</td><td>By the stairs only: three a side and one at the end</td><td>{n(g.OPEN_LEN / 3)} each; the end has the full 110</td><td>The end chair clears the sofa's front; the lamp moves</td></tr>
</table>
<p>Clearances from a UK planning guide: 60 cm of table edge per diner, 60 cm from the table to a wall as a tight minimum, 75 to aim for, 100–110 to walk behind someone seated<sup>{fit.ORDER.index("dining") + 1}</sup>.</p>
<h3>The flip-top's cut list and hardware</h3>
<table class="tight"><tr><th>Part</th><th>Material</th><th>Size (cm)</th><th>Qty</th></tr>
<tr><td>Table top · the half</td><td>Solid oak, edge-glued staves</td><td>96 × 80 × 2.7 centre + two 7 × 80 breadboard ends (110 overall), each</td><td>1 · 1</td></tr>
<tr><td>Breadboard pegs</td><td>10 mm oak dowel, slotted holes in the tongue</td><td>3 per end</td><td>12</td></tr>
<tr><td>Gate legs · apron</td><td>Solid oak, the legs tapered on two inside faces</td><td>{n(g.GATE_LEG_H)} × 4.5 tapering to 3 · {n(g.TABLE[0] - 2 * g.FLIP['inset'])} × 7 × 2</td><td>2 · 1</td></tr>
<tr><td>Backboard · hinge rail</td><td>Solid oak, from the worktop offcut</td><td>110 × 22 × 3 · 110 × 4 × {n(g.RAIL[2] - 3)}</td><td>1 · 1</td></tr>
<tr><td>Turn buttons</td><td>Oak offcut</td><td>6 × 2.5 × 2.2, on a single screw</td><td>2</td></tr>
<tr><td>Folding brackets</td><td>Häfele Hebgo 287.43.428</td><td>arm 58, height 22</td><td>2</td></tr>
<tr><td>Lift-off hinges</td><td>Union PowerLoad, 100 × 88</td><td>one 3-pack, same hand</td><td>3</td></tr>
<tr><td>Flip-top hinges</td><td>Lee Valley 40574, solid brass</td><td>{n(g.FLIP['hinge'][0])} × {n(g.FLIP['hinge'][1])}</td><td>3</td></tr>
<tr><td>Gate hinges · stays</td><td>Steel butt hinges, 75 mm · folding (locking) stays</td><td>—</td><td>2 · 2</td></tr>
</table>
<p class="note">Safety: never fold it up with anything on it, keep both turn buttons turned when it's up, check the brackets have locked (a click each side) and the gate's stays are locked before you load it.</p>

<h2 class="pb">6 · The side wall</h2>
<p>One oak line at {n(g.LEDGE_TOP)} cm runs from the ledge over the TV, round the corner on the left upright, and along the side wall. New in v15, the side wall's part is <b>one run</b>, {n(g.SIDE_RUN_T)} cm thick all along: a 7 cm record ledge with four more LPs face-out that <b>sweeps out in one smooth curve</b> to the 28 cm shelf the PC sits on, ending in a 5 cm radius like the table's corners. A warm LED strip in a groove under its front edge washes the wall below it, on the uprights' driver and dimmer. Two separate shelves at two depths become one piece of furniture, and it moves the PC out of the TV's sightlines.</p>
<figure class="render">{img("render_v13_side.png", "The PC side wall")}
<figcaption>The side wall from the room: the oak run round the corner with its four LPs, sweeping out under the PC, the keyboard tray's housing underneath and the LED's glow below it, the curtains at the window, and nothing else on the wall: the leads run inside it, the sofa below (drawn from your photo), and the media wall end-on at the right. The chimney breast is cut away so the wall reads end-on; its outline is dashed, with the depths marked: the alcove is 38 deep, so 38 of the 46 cm base sits inside it and 8 stands proud (picked out in gold), and the 30 cm uprights and shelves sit wholly inside.</figcaption></figure>
<figure>{pc_shelf()}</figure>
<ul>
<li><b>The run:</b> {n(g.SIDE_RUN_Z[0] - g.SIDE_RUN_Z[1])} cm long, {n(g.SIDE_RUN_T)} thick, cut from one 225 × 30 × 4 oak board to a full-size template: 7 deep along the LPs (with a 1.5 cm lip), easing out to {n(g.PC_SHELF_D)} over {n(g.SIDE_SWEEP[0] - g.SIDE_SWEEP[1])} cm just past the last LP. It sits on an oak cleat screwed to the side wall, dowelled to the left upright's front edge.</li>
<li><b>The PC end:</b> {n(g.PC_SHELF_Z[0] - g.PC_SHELF_Z[1])} × {n(g.PC_SHELF_D)} cm, on two concealed heavy-duty brackets (40 kg+ a pair) as well as the cleat, {n(g.PC_SHELF_TOP - g.PC_SHELF_T - g.SOFA_H)} cm above the sofa's back. The case sits with its glass to the room and its front towards the alcove. The ports face the window and stay open to the air (v13: no screen, so nothing traps the exhaust); from the sofa you look at the glass side, not the ports. The pad dock sits beyond the case.</li>
<li><b>Cables:</b> through a brush grommet at the shelf's back corner straight into a 25 mm conduit chased into the side wall (it's solid, as you confirmed), down to skirting height and behind the skirting to the base's plinth; you chase it yourselves in step 3, with a second, smaller conduit beside it for the PC's mains lead, then it's filled and painted, so nothing shows. A draw wire left in it pulls the next lead through. The HDMI is an active optical cable (about 5 m), "source" end at the PC.</li>
<li><b>Power:</b> the PC plugs into the 10-gang behind the TV: its lead (a 5 m C13 lead with a rewireable plug, fed down bare and the plug fitted at the bottom) runs in its own 25 mm conduit beside the data one. The 10-gang's load check, with the PC, is in section 9. No new socket.</li>
<li><b>Keyboard tray (back from v6.1):</b> the shelf sits on a 7 cm oak housing with a tray on 300 mm light-duty runners that rolls 25 cm out towards the room. It holds a full-size wireless keyboard and mouse: pull it out, lift the keyboard onto your lap, park it again. The housing stops 12 cm short of the sofa end so the cables drop past it; its underside is {n(g.PC_SHELF_TOP - g.PC_SHELF_T - g.KB_TRAY["h"])}, {n(g.PC_SHELF_TOP - g.PC_SHELF_T - g.KB_TRAY["h"] - g.SOFA_H)} above the sofa's back.</li>
<li><b>Headroom:</b> the shelf's underside is at {n(g.PC_SHELF_TOP - g.PC_SHELF_T)}, and it covers only the 28 cm of the sofa nearest the wall.</li>
</ul>
<div class="why"><b>The PC end, looked over again (v17)</b>
<ul>
<li><b>Air:</b> a mid-tower draws in at the front (towards the alcove) and blows out at the back and top. Both stay open: the case's top is at {n(g.PC_SHELF_TOP + g.PC_CASE[1])}, {n(g.CEIL - g.PC_SHELF_TOP - g.PC_CASE[1])} clear of the ceiling; a magnetic dust filter on the top exhaust keeps the dust out while it's off.</li>
<li><b>Reach from the sofa:</b> the PC's own power button is on its top, behind your head. A remote power button (a small card on the motherboard's power pins and a push button under the wrap ledge by the sofa end) starts it from the seat, and a powered USB 3 hub under the run's front edge puts pads, the keyboard's dongle and a stick within reach.</li>
<li><b>Lit, and seen:</b> the glass side faces the room, so its fans and lights read as part of the wall at night (the 3D view's "PC lit" button shows it). Keep its lights on a slow single colour if they pull the eye from the TV.</li>
<li><b>Leads:</b> labelled at both ends (step 13), all three down the chased conduits; nothing hangs below the shelf.</li>
</ul></div>

<h2 class="pb">7 · The oak joinery</h2>
<p>Above the worktop the wall is furniture rather than cladding: two solid oak uprights, shelves carried on joints you can see, and the Card Room Green wall showing between them.</p>
<ul>
<li><b>Uprights:</b> solid oak, 4.5 × 30 cm, {n(g.UPRIGHT_LEN)} cm long, each on two 10 mm dowels into the worktop, scribed to the ceiling and held to the back wall with concealed brackets; the left one also screws to the side wall.</li>
<li><b>Wedged through-tenons:</b> the Series X shelf (top {n(g.RZ_SHELF_TOP)}) passes through the right upright on two tenons, 6 cm wide and 2.4 thick, 12 and 20 cm from the wall. They're wedged and planed flush: standing proud, they'd touch the TV.</li>
<li><b>Housed and pegged:</b> the high shelf (two lengths, top 196) and the record ledge (top 155.4) are housed 1.2 cm into the uprights and pinned with 10 mm oak pegs, which show as dark dots.</li>
<li><b>LED grooves:</b> a routed groove on each upright's inner face holds a smart colour strip (v16) that washes the wall either side of the TV: warm white day to day, any colour for a scene.</li>
<li><b>Hidden cables:</b> a 2 × 1.5 cm groove down the back of the right upright carries Deco B's 12 V lead and patch lead, the Series X's HDMI and power, and the vinyl lead.</li>
<li><b>Finish:</b> hardwax oil throughout; lightly limed or smoked oak avoids the bright orange "new oak" look.</li>
</ul>
<figure>{joints()}</figure>
<h3>Joinery cut list</h3>
<table class="tight"><tr><th>Part</th><th>Material</th><th>Finished size (cm)</th><th>Joints</th><th>Qty</th></tr>
<tr><td>Uprights</td><td>Solid oak, quarter-sawn if you can</td><td>{n(g.UPRIGHT_LEN)} × 30 × 4.5 (buy 165 and scribe)</td><td>Housings for the high shelf and ledge; mortises for the Series X shelf in the right one; LED groove inside; cable groove at the back of the right one</td><td>2</td></tr>
<tr><td>High shelf</td><td>Solid oak</td><td>128.9 × 30 × 4 and 51.7 × 30 × 4</td><td>Housed 1.2 into the uprights, pegged; the short length on a cleat on the reveal</td><td>2</td></tr>
<tr><td>Record ledge</td><td>Solid oak</td><td>128.9 × 7 × 2.4; lip 0.9 × 1.5</td><td>Housed and pegged</td><td>1</td></tr>
<tr><td>Series X shelf</td><td>Solid oak</td><td>55 × 30 × 4 ({n(g.RZ_W)} + 4.5 through)</td><td>Two through-tenons 6 × 2.4, wedged flush; cleat on the reveal</td><td>1</td></tr>
<tr><td>Side-wall run (v15)</td><td>Solid oak, one 225 × 30 × 4 board</td><td>{n(g.SIDE_RUN_Z[0] - g.SIDE_RUN_Z[1])} long, 7 deep sweeping to {n(g.PC_SHELF_D)}, {n(g.SIDE_RUN_T)} thick; lip 0.9 × 1.5 along the 7 cm part</td><td>Cleat, two concealed brackets under the PC end, two dowels to the left upright; LED groove under the front edge</td><td>1</td></tr>
<tr><td>Worktop</td><td>One solid oak worktop, 300 × 62</td><td>{n(g.ALC_W)} × {n(g.BASE_D)} × 3</td><td>Chamfered front; cut edges sealed; keep the offcut</td><td>1 board</td></tr>
<tr><td>Face frame</td><td>Oak, 20 mm</td><td>186 × 73, stiles about 5 wide</td><td>Glued and pinned; end stiles scribed</td><td>1 set</td></tr>
<tr><td>Wedges · pegs · dowels</td><td>Oak · 10 mm oak dowel</td><td>6 × 3, tapering · 5 long</td><td>Glued</td><td>2 + spares · 6 · 8</td></tr>
<tr><td>Keyboard tray</td><td>Oak housing sides 7 × 2, ply tray, oak lip</td><td>70 × 28 × 7; tray 54 × 26</td><td>Housing screwed under the shelf; 300 mm runners</td><td>1</td></tr>
</table>

<h2 class="pb">8 · Paint and light</h2>
<h3>Paint: Farrow &amp; Ball Card Room Green No. 79</h3>
<p>The room is colour-drenched in Card Room Green: walls, ceiling, alcove, chimney breast, skirting and the radiator. The door and its frame stay white, as they are (v20): a crisp edge to the green, like the window. There's no trunking left to paint. It's a soft grey-green that lets the oak and the records lead.</p>
<figure>{img("paint_grid.png", "The artisan oak render in four greens")}
<figcaption>The wall in Card Room Green (chosen) beside Sage Green, Treron and the earlier deep green. Screen colours are approximate and the renders are lit as in the evening: judge from painted samples.</figcaption></figure>
<ul>
<li><b>Finishes:</b> Estate or Modern Emulsion on walls, ceiling, alcove and breast; Estate Eggshell in the same colour on skirting and radiator (the door stays white) (Modern Eggshell if the skirting takes knocks).</li>
<li><b>Order:</b> paint before anything is fixed, so nothing needs cutting in round the uprights, shelves or the dining wall.</li>
</ul>
<h3>Skirting: Card Room Green too</h3>
<figure>{img("skirting_options.png", "Three skirting options")}</figure>
<p>Recommended: Card Room Green in Estate Eggshell, which completes the drench and hides scuffs far better than white. Darker option: Green Smoke. Over the white gloss: wash, key, woodwork primer, two coats of eggshell.</p>
<h3>Light, in three warm layers</h3>
<ul>
<li><b>The LED strip on the ceiling</b> (as now): round the room's edge, into the alcove and across the breast; 2700K on a dimmer.</li>
<li><b>Built into the oak (v16: smart colour):</b> an RGB and tunable-white strip in each upright's groove and one under the side-wall run's front edge<sup>{fit.ORDER.index("strips") + 1}</sup>, in the same app as the bars' bulbs, so each scene sets them too; on their plug-in power on the 10-gang (no fused spur). The 6500K bias light on the back of the TV stays plain white: it's there for the picture, not the mood.</li>
<li><b>Your red lamp:</b> the three-headed floor lamp you have, its colour bulbs green at the top, pink in the middle and purple at the bottom. A deep green room needs a low layer as well as the light from above; it's also the one to leave on for a film. It can stand in any of the three spots in the 3D room.</li>
<li><b>Two spot bars</b> in the style of Dunelm's Wolston (£49 each; 84 × 16 cm, 22.4 cm drop; 4 × E14, 6 W max<sup>{fit.ORDER.index("wolston") + 1}</sup>) on your two existing ceiling points, <b>both running from the TV towards the window</b> (v15). Bar 1 hangs on the rose straight out from the TV unit, halfway to the sofa; bar 2 on the pendant point by the stairs, along the west wall, so its end no longer comes near that wall. <b>Smart colour bulbs</b> (v15): eight E14 bulbs under the bar's 6 W, the WiZ Colour P45 (4.9 W, 4.5 × 10.1 cm) or, if it shows below a shade, the shorter Philips Hue lustre (5.1 W, 4.5 × 7.7 cm)<sup>{fit.ORDER.index("e14") + 1}</sup>. Smart bulbs need full power, so <b>no dimmers</b>: the wall switches stay as they are and stay on; level and colour come from the app (or an optional smart button). </li>
</ul>
<p><b>Where the heads point (v17):</b> all eight heads straight down, evenly spread along each bar, so their pools overlap into one even light over the room: that's the <b>Bright</b> preset, the default. Tilt a head only if its pool lands badly (in the TV's screen from the sofa, or in someone's eyes). Set the bulbs to warm white (3000K) for Bright, 2700K for Cosy, and save colours for the presets you want them in.</p>
<h3>Three lighting presets</h3>
<p>Three presets instead of six buttons: <b>Bright</b> (the default), <b>Cosy</b> and <b>Film</b>, each set on the strip's controller, the inline dimmer on the uprights' LED driver, and the bars' and the lamp's smart bulbs in their app. Save the three as scenes in the app (and on the smart button if you get one). In the 3D room the Lights tab has the three tiles, the evening or daytime switch, and every light's slider folded under them.</p>
{scenes_html()}

<h2 class="pb">9 · Power, cables and network</h2>
<h3>Power</h3>
<figure>{power()}</figure>
<ul>
<li><b>The socket:</b> the single on the side wall just in front of bay 1, about 30 cm up, becomes a double at the same spot. The left outlet feeds the 10-gang; the right one feeds the retro 6-way, so its own switch is now the retro switch. The 10-gang's switches sit behind the TV, 2 cm from the corner post, where you can't reach them any more.</li>
<li><b>10-gang:</b> lying flat on the worktop behind the TV, both sides left on: TV, soundbar, sub, Series X, USB charger, Deco B, Switch 2, the deck, the preamp and now the PC. With everything running that's about 1.55 kW (the PC's 850 W at most), under the strip's 13 A (3 kW).</li>
<li><b>Retro 6-way:</b> in the channel behind bay 1 (bay 2's back is the sub's port): Xbox One, Xbox 360, PS3, PS2, PS1, RetroTINK.</li>
<li><b>OLED care:</b> leave the TV in standby so it runs its pixel refresh.</li>
</ul>
<h4>Socket by socket</h4>
<table class="tight"><tr><th>Socket</th><th>Feeds</th><th>On or off</th></tr>
<tr><td>Side wall, double, left outlet</td><td>The 10-gang behind the TV: TV, soundbar, sub, Series X, USB charger (fan stand, pad dock, bias light, HDMI switch), Deco B, Switch 2, the turntable, the preamp, the PC and the uprights' LED driver</td><td>Always on: about 1.55 kW with everything running, PC included</td></tr>
<tr><td>Side wall, double, right outlet</td><td>The retro 6-way in the channel: Xbox One, Xbox 360, PS3, PS2, PS1, the RetroTINK's USB plug</td><td>The wall switch is the retro switch: off between sessions; up to about 0.8 kW with a launch PS3</td></tr>
<tr><td>Behind the sofa's short side, double (yours, v23)</td><td>The rear speakers; a spare outlet for a phone charger or a lamp by the sofa</td><td>On</td></tr>
<tr><td>Window wall behind the plant stand, double (yours, v23)</td><td>Your red lamp and the plant stand's grow lights: both within reach of it, layout A</td><td>On; the grow lights on a plug-in timer</td></tr>
<tr><td>Ceiling points 1 and 2</td><td>The two spot bars, with smart colour bulbs (v15)</td><td>Switches left on; level and colour from the app</td></tr>
</table>
<p class="note">One strip per outlet, never one plugged into another, and each under its 13 A (3 kW) limit: about 1.55 kW on the 10-gang and up to 0.8 kW on the retro 6-way, about 10 A together.</p>
<h3>Electrics: your own job</h3>
<p>You're doing the electrics yourselves. In England, Part P of the Building Regulations decides what needs an electrician or building control.</p>
<ul>
<li><b>Notifiable (not for you):</b> a new circuit, a replacement consumer unit, or any change to a circuit round a bath or shower.</li>
<li><b>Not notifiable (yours):</b> the socket swapped for a double, and the two spot bars in place of the old fittings. Like for like, so no electrician and no building control.</li>
<li><b>Still to the wiring regulations</b> (BS 7671), every time.</li>
<li><b>The light switches stay:</b> the bars' smart bulbs need full power, so there are no dimmers to fit.</li>
<li><b>Not mains work at all:</b> the Cat6 and the conduits.</li>
</ul>
<div class="callout"><b>The safe routine, every time</b><ol>
<li><b>Isolate:</b> switch off that circuit's breaker at the consumer unit (the lighting circuit for the bars, the socket circuit for the socket). If the labels aren't clear, switch off the main switch.</li>
<li><b>Lock off:</b> fit the MCB lock-off and padlock, keep the key in your pocket, and tape a note on the board.</li>
<li><b>Prove dead:</b> check the tester lights on its proving unit, test between every pair of terminals (live–neutral, live–earth, neutral–earth), then check the tester on the proving unit again.</li>
<li><b>Photograph</b> the wiring before you disconnect anything, and connect the new one wire for wire: brown (or red) to L, blue (or black) to N, green-and-yellow to earth, sleeved, no copper showing, every screw tight.</li>
<li><b>Test:</b> power back on, then the socket tester in both outlets; each bar's four bulbs come on and join the app.</li></ol></div>
<div class="callout"><b>Stop and call an electrician if…</b><ul>
<li>the tester shows anything live after you've isolated;</li>
<li>the wiring is old (rubber or fabric sheath, or red and black with no earth), or there's no earth at a ceiling point (the spot bars need one);</li>
<li>there are more wires than you can match to your photo (two-way switching, a loop in a ceiling rose you can't follow), or scorch marks, or a loose, hot or crumbling fitting;</li>
<li>the consumer unit has rewireable fuses or no RCD;</li>
<li>a job grows into a new circuit, consumer unit work, or anything by the bath or shower.</li></ul></div>
<h3>Cable routes</h3>
<figure>{routes()}</figure>
<ul>
<li><b>The channel:</b> 4 cm behind the frames, flat two-compartment trunking: mains on one side, HDMI, Cat6 and audio on the other. Switch 2 and the retro 6-way stand on edge in it.</li>
<li><b>The groove behind the right upright:</b> Deco B's 12 V and patch leads, the Series X's HDMI and power, and the vinyl lead, down to the worktop's slot.</li>
<li><b>The PC:</b> through the shelf's brush grommet into two conduits chased into the side wall (the HDMI and Cat6 in a 38 mm one, its mains lead in a 25 mm one), behind the skirting and into the plinth notch; the mains lead goes on to the 10-gang.</li>
<li><b>The sub:</b> its mains lead from the 10-gang drops through the slot behind the TV to the back of bay 2, about 1 m. Keep the channel behind the sub clear: its port needs the air.</li>
<li><b>Airflow:</b> console bays stay open-backed; the Series X has 15 cm each side and 21 above.</li>
</ul>
<h3>Network</h3>
<figure>{network()}</figure>
<ul>
<li><b>Bedroom 3:</b> the Hub 5 (in modem mode), Deco A and Switch 1 sit together with the gaming PCs. Switch 1's eight ports: the uplink, two PCs, the two Cat6 runs down to Deco B and Deco C, and, if you want them, the projector in the master and the music room in bedroom 2.</li>
<li><b>The route down:</b> across the landing to the airing cupboard, which sits over the alcove's corner, and down through its floor. Run 1 comes through the living room ceiling in the alcove's right corner to Deco B; run 2 follows the right upright's groove down and through the floor to the kitchen, where Deco C goes on the outside of the brick cupboard, up high.</li>
<li><b>Sloped ceilings:</b> bedroom 2 and the bathroom slope down to the back wall; keep any Deco or desk in bedroom 2 on the high side.</li>
</ul>
<h4>What each part does</h4>
<table class="tight"><tr><th>Part</th><th>Where</th><th>Job</th><th>Why it's needed</th></tr>
<tr><td>Virgin Hub 5, in modem mode</td><td>Bedroom 3</td><td>Brings the internet in, nothing else</td><td>Two routers fighting (double NAT) breaks Xbox online play; its Wi-Fi switches off</td></tr>
<tr><td>Deco A (main)</td><td>Bedroom 3</td><td>The router: Wi-Fi, parental controls, HomeShield</td><td>HomeShield and parental controls only work when the Deco is the router</td></tr>
<tr><td>Switch 1, 8-port</td><td>Bedroom 3</td><td>Turns Deco A's spare port into seven</td><td>The two PCs, both Cat6 runs down, and the optional projector and music-room runs</td></tr>
<tr><td>Deco B</td><td>Living room, high shelf at {n(g.HIGH_TOP)}</td><td>Wi-Fi for the living room, and the wired point for the wall</td><td>Fixes the living room's weak 5 GHz side</td></tr>
<tr><td>Switch 2, 8-port</td><td>Standing on edge in the channel behind the base</td><td>Turns Deco B's spare port into seven</td><td>The Series X, Xbox One, Xbox 360, PS3, PC and TV each get a cable, one port spare</td></tr>
<tr><td>Deco C</td><td>Kitchen, high on the outside of the brick cupboard</td><td>Wi-Fi for the kitchen</td><td>The kitchen gets poor signal on every band today</td></tr>
<tr><td>Cat6 runs 1 and 2</td><td>Bedroom 3 → airing cupboard → alcove corner, and on to the kitchen</td><td>The wired link between Decos ("Ethernet backhaul")</td><td>Without it the Decos relay each other over the 5 GHz band the phones use, losing speed at each hop</td></tr>
</table>
<h4>Stage 1: the mesh up today, before any cables</h4>
<ol>
<li>Unplug everything from the hub. Log in at 192.168.0.1 with the password on its base, then Modem Mode → Enable Modem Mode → Apply. Its settings page moves to 192.168.100.1.</li>
<li>Connect a hub port to Deco A and set it up in the Deco app, reusing the old Wi-Fi name and password. If it shows no internet, try another port and restart the hub.</li>
<li>Plug Switch 1 into Deco A's other port, then the PCs into Switch 1.</li>
<li>Add Deco B in the living room and Deco C in the kitchen. For now they link over Wi-Fi.</li>
<li>Check the Xbox's network settings show NAT: Open.</li>
</ol>
<h4>Stage 2: after your Cat6 runs (step 3)</h4>
<ol>
<li>Plug run 1 into Deco B's free port (Switch 2 stays in the other) and run 2 into Deco C.</li>
<li>In the Deco app, check Deco B and Deco C show as "Ethernet".</li>
<li>Plug the Series X, Xbox One, Xbox 360, PS3, PC and TV into Switch 2.</li>
<li>Under QoS, give the Series X and the PC high priority; turn on guest Wi-Fi and automatic firmware.</li>
</ol>
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
<li><b>Sub:</b> wireless, in bay 2 under the TV, its driver facing the room and its rear port {n(g.SUB_PORT_GAP)} cm from the wall through the open back (15–30 is advised<sup>{fit.ORDER.index("subport") + 1}</sup>). Next to the soundbar, its bass blends with the bar instead of coming from behind you, and it's off the floor where feet and drinks are. If the bass booms, turn it down rather than moving it.</li>
<li><b>Rears:</b> the soundbar's own two rears, on slim floor stands directly behind the sofa (v27.1, from your photos): one at each end of its long side, in the {n(g.SOFA_BACK_Z - g.WINDOW_Z)} cm gap between the sofa's back and the window wall, the <b>left</b> one in the corner and the <b>right</b> one at the window end, where the curtains hang in the same gap: closed, they fall over it and muffle it, so keep that end open when you watch. Both speakers sit just above the sofa's back, at about seated ear height ({n(g.REAR_STAND['top'])}–{n(g.REAR_STAND['top'] + g.REAR_SPK[1])}), facing the room. They're linked by a cable along the skirting behind the sofa and powered from your double socket behind the sofa's short side. In the 3D room they move in Edit room.</li>
</ul>

<h2 class="pb">10 · Build guide, for a first-time builder</h2>
{guide_html()}

<h2 class="pb">11 · Buy list and tracker</h2>
<p>Every purchase and job, in build order, comes to about £{money(tl, th)}, with no electrician on top: the electrics are your own job, and the tools for them are on the list. Each phase carries its part's coloured label. Estimates are approximate UK prices; changed and new items are marked. Tick items off and write in what you paid.</p>
<table class="tight"><tr><th>Phase</th><th>Estimate (£)</th><th>Biggest item</th></tr>{ptot}</table>
<p class="note">Already owned: Virgin Hub 5, three Deco X1500s, two TL-SG105S switches (both become spares), LG OLED C6 55" and its stand, a 10-gang, the Hisense AX5100G 5.1 soundbar, the Series X fan stand, the turntable, the L-sofa and all the consoles.</p>
<table class="tracker"><thead><tr><th>Status</th><th>Item</th><th>Qty</th><th>Estimate (£)</th><th>Paid (£)</th></tr></thead><tbody>
{tracker_rows()}</tbody></table>

<h2 class="pb">12 · Still to confirm, later ideas, sources</h2>
<!--confirm--><h3>Still to confirm</h3>
<ul class="checks">
{questions.pdf_items()}
</ul>
<p class="note">Easiest way to answer: the viewer page has a box for each of these and takes photos; or reply in a message, a line each.</p><!--/confirm-->
<h3>Agreed so far</h3>
<ul class="agreed">
<li>From your v13.6 message: the legs store as part of the table (in the leaf's frame); the electrics are your own job; each step labelled with its part.</li>
<li>From your v13 message: less cladding (done: no slats, spine, sub box or reeding; cables chased into the wall); the stairs go up; the drawer layouts drawn.</li>
<li>From your answers (v12.1): the sofa's long side ends in line with the breast's reveal; the door hinges on the breast side and opens in; the side wall and breast are solid (plugs and screws, no stud fixings); the PC is an average gaming case (allowed for at 23 × 45.3 × 46.6).</li>
<li>Artisan oak, Card Room Green with matching eggshell skirting, every record face-out, the game drawer as designed.</li>
<li>The TV {n(g.TV_SHIFT)} cm nearer the side wall, the turntable in the alcove, the Series X above it, the records below.</li>
<li>The ledge wrapping round onto the side wall, with the PC above the sofa.</li>
<li>A fold-down oak dining table on the chimney breast; the spot bars on the existing ceiling points; the sub back in the media wall, in bay 2 (v13.5).</li>
</ul>
<h3>Later ideas</h3>
<ul>
<li><b>For the room (v17):</b> a glass display case on the breast, glass plant shelves in the window, a C-table for the sofa's open end, and small ones (v18: TV backlight that follows the picture, cushions in the rug's colours, a plant uplight, a rug pad): see the appendix “Ideas for later”, and the Ideas tab and buttons in the 3D room.</li>
<li><b>Dave and Emma's watch log:</b> a shared film and TV log, like a Spotify Blend for what you watch: log each film or episode, mark whether you watched it together, rate it, and later get suggestions for what to watch next. To be shaped up separately.</li>
</ul>
<h3>Sources</h3>
<p class="note">Numbered sources are the item sizes used in the fit proof (section 3).</p>
{fit.sources_html(OTHER_SOURCES)}

<h2 class="pb">Appendix · Ideas for later (not in the plan or the costs)</h2>
{ideas.pdf_html()}
<figure class="render">{img("render_v29_3d_ideas_window.png", "Idea: glass plant shelves in the window")}
<figcaption>Idea only, from the 3D room: glass plant shelves across the window's reveal, beside your plant stand in the west corner.</figcaption></figure>
<figure class="render">{img("render_v29_3d_ideas_breast.png", "Idea: the tall glass display case on the breast")}
<figcaption>Idea only: the tall glass display case (v20: 85 tall, three glass shelves) on the chimney breast, lit inside, above the “now playing” ledge: oak, with collectibles.</figcaption></figure>
<figure class="render">{img("render_v29_3d_case_mixed.png", "The case with a black frame and a bit of each")}
<figcaption>The same case with a black frame and a bit of everything: 7-inch singles, a cap and figures, small plants, boxed games. A white frame, and singles and tapes, are in the 3D room's Decor buttons.</figcaption></figure>
<h3>Suggested furniture and decor (v21): each on or off in the 3D room</h3>
{ideas.suggest_html()}
<figure class="render">{img("render_v29_3d_suggest.png", "Suggested furniture and decor, all on")}
<figcaption>All six suggestions switched on (3D room, “Suggested furniture and decor”): the floor plant and side table at the sofa's open end, the pouffe, the print over the sofa, the clock over the door, the coffee-table tray.</figcaption></figure>
<figure class="render">{img("render_v29_3d_decor.png", "Decor to try: rug, cushions, curtains")}
<figcaption>Decor to try (3D room, Decor): a sage-stripe rug, rust and ochre cushions with a throw on the arm, white linen curtains. Also: a jute or deep blue rug, blue or sage cushions, sage, blue or rust curtains.</figcaption></figure>

<!--keep--><h2 class="pb">Appendix · Earlier rounds</h2>
<div class="decision"><b>v27: the dining cabinet is the plan, made for six.</b> You asked to use the cabinet as the main table, for six, with the chairs inside it. It now leads section 5: one oak cabinet under your shelf, a {n(g.OPTC['len'])} × {n(g.OPTC['top'][0])} table that swings down out of its bay, <b>six in comfort</b>, three a side, with the coffee table left where it is, and <b>all six chairs inside it</b> (four on the floor, two on the shelf, the seat pads beside them). The halves are shorter than v26's (90 instead of 112.5), so each is lighter and there's room over the folded table for a <b>linen flap</b>. <b>Step 11 of the build guide</b> is now the cabinet's build, in sixteen stages with every size, with two new drawings: the carcass from the front, and the table's halves from underneath. The buy list carries the cabinet; the flip-top stays in section 5 as the alternative. <b>Your rear speakers</b> are drawn where they stand (section 9, from your photos): directly behind the sofa, one at each end of its long side, both just above the sofa's back. The brick under the stairs is drawn painted, as it has a wall in front of it. On the plan page the 3D room opens on the cabinet, the flip-top's chair cupboard can come off the wall in Edit room, and Edit room clips things to walls more easily: a quarter turn keeps a piece against its wall, and <b>Back to the wall</b> pushes it there.<br><b>v26: option C, the dining cabinet, and up to eight at the table.</b> A second way to build the stairs wall, beside the flip-top (which stays the plan): <b>one oak cabinet</b> under your shelf, with the table standing up in one bay and all eight chairs folded in the other, so nothing shows when it's packed away. Open, the table is {n(g.OPTC['len'])} × {n(g.OPTC['top'][0])}: <b>eight at a squeeze, six in comfort</b>, the most this room takes (section 5 shows why a ninth won't fit). It costs more than the flip-top and the chair cupboard; it isn't in the totals unless you choose it. On the plan page, the 3D room's Tools panel is tidier (its title and buttons stay put, every tab opens at the top, and on a laptop it docks to the right with the room beside it); a <b>Hide labels</b> button takes the numbered stickers off the room; and Look and Extras have more to try.<br><b>v25: Demma Home Improvements, and three lighting presets.</b> The plan page is a new app: your room in 3D is the home screen, with numbered stickers on it (tap one for its key facts, to open its chapter, or to fly there), one <b>Tools</b> button for every 3D control, and the plan, the build steps, the buy list, the ideas and the questions sliding up over the room. Questions are answered with a tap or a photo. <b>The lights</b> have three presets instead of six buttons: <b>Bright</b>, <b>Cosy</b> and <b>Film</b> (section 8). Dinner is now a rule (the table open lifts bar 2 over it) and daytime a switch, so they work with any preset; step 12 sets the three in the app. The plan itself doesn't change.<br><b>v24: less to read, and a cleaner page.</b> The round numbers are out of the text (the history stays here and in the appendix), long captions fold behind <b>More</b>, and the notes on how the media wall's layout was chosen moved to the appendix. The plan page has a new look: each section in its own card, a contents list down the side on a computer (a row of chips on a phone) that follows where you are, a floating tab bar, clearer tables, and a footer with the downloads. The plan itself doesn't change.<br><b>v23: more ways to build the chairs in, and the room as it really is.</b> <b>Chairs built into the table</b> (section 5): as well as the chair cupboard, four chairs can hang <b>behind the folded top</b> on a deeper backboard, out of sight, and a <b>fold-down oak seat</b> can go in the gap at the stair end, a fifth place that's always there. Both are options for you to choose, and both are in the fit proof. <b>Under the stairs</b> is a brick side wall with plasterboard beneath, as you said: drawn in brick, so chairs five and six go in the garage. <b>Your sofa's ottoman</b>, square, blue corduroy, the size of one of its seats, is on the rug beside the coffee table (and moves in Edit room). <b>Your sockets</b> are drawn where they are: the single in the corner in front of the left Xbox game drawer (the one the plan makes a double), a double behind the sofa's short side, below and left of the PC, which now powers the rear speakers (the 12-way strip is off the buy list), and a double behind the plant stand in the window corner, for your lamp and the grow lights. The floating <b>banister end at the top of the stairs</b> is gone. The plan page has a <b>new colour</b> and four <b>page looks</b> (Card Room, Oak &amp; linen, Sofa blue, Plain) and larger text to choose from; the questions are a list now, with no answer boxes; and the 3D room has <b>six more suggestions</b> to switch on or off (twelve in all).</div>
<div class="decision"><b>v22: the plan page is quicker to use.</b> The first round of the optimisation plan: under the 3D room the controls are now in <b>five drawers</b> (Views, Layout, Lights, Look, Extras), one open at a time, and on a phone the picture stays in sight while you choose. <b>Your picks</b> (in Extras) lists every idea, suggestion and decor choice you've switched on with their rough cost added up, to copy as a note or save for the next round. The <b>build steps</b> open one at a time, starting at the first one not done, with a Next step button, or all at once if you'd rather read straight through: on a phone the tab is under a third as long. The <b>3D room</b> draws less each frame (about half as many draws; your plant stand alone went from 152 pieces to 7) and shows a picture while it loads; in Fast each spot bar lights with two of its heads. The shared plan page links its pictures instead of carrying them, so it opens much faster. The plan itself doesn't change.<br><b>v21: the 3D room opens on the whole room, and suggestions you can turn on or off.</b> You asked for the first 3D view "at the best viewing to see most if not all the room without clipping or obstruction": it now opens on <b>The whole room</b>, from above the window side with the wall nearest you <b>cut away</b> like a dolls' house, so the media wall, the breast, the door, the stairs, the table's wall, the PC wall and the sofa are all in one picture. Every view was checked: <b>From the window</b> no longer stands behind your red lamp; the chair cupboard, the dining table, the sofa, the bird's eye and the dolls' house views were re-aimed; the chimney breast and the window wall have their own buttons; and on a phone each view now takes in as much of the room across as on a computer. <b>Suggested furniture and decor</b> (appendix), each with its own on/off button in the 3D room and all off to start: a tall floor plant and a round side table at the sofa's open end, a knitted pouffe, a large print over the sofa, a clock over the door and a tray for the coffee table. Edit room's Add list gains a rattan armchair, a blanket ladder, an oak bench and an arc floor lamp. The plan itself doesn't change.<br><b>v20: the table packs away with its chairs, a taller glass case, and decor to try.</b> You asked "is it not possible to build the chair storage into the table setup. i want it to be a fully pack away setup": it is. <b>An oak chair cupboard</b> is built in at the table's window end, {n(g.CHAIR_STORE["cupboard"]["z"][0] - g.CHAIR_STORE["cupboard"]["z"][1])} wide × {n(g.CHAIR_STORE["cupboard"]["d"])} deep × {n(g.CHAIR_STORE["cupboard"]["h"])} tall, flush with the pipe boxing and under your shelf, with <b>four folded chairs inside</b> (two on its floor, two on its shelf) behind two doors on push latches (about £120–240; section 5). Fold the table and shut the doors and the whole wall is packed away. <b>Six</b> fit if it's built {n(g.CHAIR_STORE["cupboard"]["d6"])} deep; otherwise chairs five and six go in the garage. Thanks for the <b>25 cm</b> window ledge: that matches the drawing (22 into the reveal and 3 of nose). <b>The door and its frame are white</b>, as you said, in every drawing and the 3D room. No HD crashes, so the HD question is gone. <b>The glass display case</b> idea is now <b>85 tall</b> with three glass shelves (90 wide, 12 deep), and in the 3D room a new <b>Decor</b> group tries five things inside it (collectibles, retro games, 7-inch singles and tapes, plants and ceramics, a bit of each), three frames (oak, black, white), four rugs, three cushion colourways and five curtain colours; Edit room's Add list has a floor vase, a pouffe, a basket, a floor mirror and a lantern. Fit proof {nfit} checks, none fail.<br><b>v19: somewhere for the chairs, every LP counted, and a better edit mode.</b> First, <b>two folded chairs on hooks</b> in the {n(g.CHAIR_STORE["hooks"]["z"][0] - g.CHAIR_STORE["hooks"]["z"][1])} cm gap at the table's window end (still the cheap way, about £8–15). The gap at the stair end is {n(g.CHAIR_FOLDED[0] - (g.CHAIR_STORE["stair_gap"][0] - g.CHAIR_STORE["stair_gap"][1]))} cm too narrow; under the stairs and the garage are the other two places. The LP count now includes your vinyl stand: <b>about {LPS} LPs</b>, {g.WALL_LPS} in the wall, all face-out, and {g.STAND_LPS} in the stand. In the 3D room's Edit room: <b>undo</b>, things <b>snap to a wall</b> within 5 cm, <b>copy</b> what you've added, each thing shows its <b>size</b>, the <b>sofa moves</b> too, and on the shared plan page one layout can be <b>saved for both of you</b>.</div>
<div class="decision"><b>v15.</b> Your notes on the room as it really is: <b>your sofa</b> is drawn in blue corduroy, two seats then the corner, its long side running to about 40 cm short of the window's end, with no cushion; <b>your red lamp</b> with its colour bulbs (green on top, pink, then purple); on your shelf by the stairs, <b>your IKEA light box</b> at the left end, <b>your laser</b> in the middle (its dots on the ceiling) and the <b>plant hanging</b> down off the shelf; <b>your hat</b> on an oak peg by the stairs; <b>soft grey carpet</b> (your photo shows it already is), a <b>designed rug</b> that fits in front of the sofa (230 × 160), and <b>your curtains</b> from your photo: long hessian pencil-pleat panels to the floor on a wooden pole just under the ceiling strip (open or drawn in the 3D room). The <b>record trays take LPs only</b>: one trough the full width, with room to flip with both hands. The <b>side wall</b> looks better: the ledge and the PC shelf become <b>one oak run</b> that sweeps out in a curve to the PC, with a warm LED glow underneath. <b>Both spot bars now run from the TV towards the window</b> and take <b>smart colour bulbs</b> (E14, under the bar's 6 W), so there are no dimmers to fit; the light is set softer and aimed at walls and shelves, for less spotty light. In the 3D room every light has a <b>slider</b>, the bars and the lamp a <b>colour</b>, and the <b>walls, ceiling and skirting</b> each have their own paint colour. And a <b>new dining table that stays on the wall and seats more</b>: a flip-top gate-leg table. Its second half flips out on brass hinges to make 110 × 160, on a folding oak gate leg: four with room, six elbows-in, seven by the stairs; no lifting off, no leaf or legs to store (section 5). Your <b>curtains</b> are Dunelm hessian on a wooden pole with rings and ball finials.<br><b>v13.</b> You asked for less cladding all over the place, so it's gone: no slatted cable spine, no slatted PC screen, no slat panel behind the turntable, no slatted sub box, no reeded table. The PC's leads now run in conduit <b>chased into the solid side wall</b>, so there's no trunking either; the sub stands under a <b>plain oak cover</b> (below); the folded table is a <b>plain oiled oak panel</b> between its pegged breadboard ends. The oak that's left is the joinery that does a job: the uprights, the shelves, the ledges, the worktop, the face frame and the table. The <b>stairs go up</b> to the first floor (drawn rising away from the room; tell us if they run the other way). New: <b>the drawer layouts</b>, every drawer to scale with what goes in it (section 3). The slat-wall alternative is retired.<br><b>v13.1–13.2:</b> the sub gets a <b>plain oak cover</b> with no sides: spills run off it, the sub can't tip, and nothing blocks its driver or port (section 5). A new render shows <b>every drawer out</b>, and the viewer can lay <b>rough measurements</b> over any view. The <b>stairwell opening</b> now starts just after the door, over the banister, and the sofa is drawn as yours. <b>Six at the table</b> now use the leaf too: 170 × 80, {n((g.TABLE[0] + g.LEAF[0]) / 2)} cm a diner on the long sides and {n(-g.FREE_Z[0])} cm off the breast, every clearance checked. The <b>side view</b> now shows how deep the alcove is round the wall: 38 of the 46 cm base inside it, 8 proud, the uprights and shelves wholly inside.<br><b>v13.3:</b> the build guide is now step by step, each step with what to buy before it and what to check after it; the buy list shows what each phase costs; and the network and power section lists what each part does, both setup stages and what plugs into every socket (section 9).<br><b>v13.5:</b> the sub is back in the media wall. The two Xbox bricks lie flat at the back of their shelves by the power leads, the RetroTINK and the HDMI switch move into the space that frees in bay 1, and the sub takes the lower left of bay 2, under the TV, on an isolation riser beside the PS2 and PS1 (section 3). The dining wall has nothing under it now, so eight can sit down without moving anything.<br><b>v13.7:</b> four <b>lighting scenes</b> (TV night, dinner, records, everyday evening), each drawn on the room plan with every light's level, so you know where to set each dimmer (section 8).<br><b>v13.8:</b> the whole plan is back on your own deck (the one you can edit, with your saved answers), and the summaries now follow the fit proof and the questions list, so they can't fall out of date: the PC case is answered and off the list, and the three checks on site are the TV's plugs, the RetroTINK's size and the sub's vibration.<br><b>v13.6:</b> the <b>leaf carries the legs</b>: a slim oak frame underneath holds all eight oak legs in clips, so the folded table stays a plain panel, nothing new stands in the room, and the leaf goes wherever the chairs are kept (section 5). <b>The electrics are your own job</b>: swapping the socket for a double, the two dimmers and the two spot bars are like-for-like and not notifiable in England, so there's no electrician's visit; there is a safe routine and a clear point to stop and call one (section 9). The PC now runs from the 10-gang. Every step and every buy-list phase carries a <b>coloured label</b> for its part (Network, Media wall, Dining table and so on), and one list says what we still need from you.<br><b>v14:</b> a <b>second place for the table</b>: on the wall by the stairs, under your 2 m shelf (section 5 compares the two). The plan page now has a <b>3D room</b> you can walk round: switch the table's wall, fold it or set it for four or six, change the paint, the lighting scene and where the floor lamp stands, and save any view as an HD picture.</div>

<h2 class="pb">Appendix · Options we set aside</h2>
<!--keep-->{scenes_v24_html()}<!--/keep-->
<h3>How the media wall's layout was chosen</h3>
<figure>{why_layout()}</figure>
<div class="why"><b>Why this layout, and what we ruled out</b>
<ul>
<li><b>The TV in the middle (v10):</b> left two {n(25.25)} cm gaps either side, too narrow for a turntable, so the vinyl had to move out to the chimney breast. Moving the TV joins them into one {n(g.RZ_W)} cm zone.</li>
<li><b>The turntable with the Series X beside it:</b> 45.2 + 20.5 cm won't go in 50.5. The Series X goes up on a shelf instead, above the lid's swing, where it gets more air than it had in v10 (15 cm each side, 21 above).</li>
<li><b>The vinyl cabinet on the breast as well as a table:</b> a table needs the breast's full width, and a cabinet in front would put the diners 44 cm further into the room.</li>
<li><b>A gateleg table in the recess:</b> it would block the door; the breast is the only clear wall.</li>
</ul></div>
<h3>Options we rejected along the way</h3>
<table class="tight"><tr><th>Option</th><th>Why not</th></tr>
<tr><td>Slatted oak cladding: cable spine, PC screen, turntable panel, sub box, reeded table (v12)</td><td>You asked for less cladding: the chased conduit and plain oak do the same jobs more quietly</td></tr>
<tr><td>The slat wall alternative (v7–v12)</td><td>Cladding over the whole alcove; the oak uprights won</td></tr>
<tr><td>The vinyl cabinet on the chimney breast (v10)</td><td>The breast is the only clear wall for a table; the turntable fits in the alcove now</td></tr>
<tr><td>Hub as router, Decos as access points</td><td>Loses HomeShield and parental controls</td></tr>
<tr><td>All-wireless mesh · powerline</td><td>Speed drops at each hop · slower and less stable than Cat6</td></tr>
<tr><td>Records spine-up in one drawer</td><td>Showed only a handful of covers; face-out trays show every one</td></tr>
<tr><td>A green feature wall only · white skirting</td><td>The drench ties the room together; white cuts a bright line round it</td></tr>
<tr><td>Bluetooth from the turntable</td><td>Compresses the sound; the AUX lead keeps full quality</td></tr>
<tr><td>Lifting the table off onto eight legs, with a 60 cm leaf that stores the legs (v13.1–v14)</td><td>You wanted it to stay on the wall and seat more: the flip-top's half and gate leg do both (v15)</td></tr>
<tr><td>Folding legs fixed under the table · a box for the legs under the dining wall · the plinth drawer (v13.6)</td><td>They'd show on the folded panel and stand it 5 cm off the wall · it sits where the chairs push back with six · too short for 71 cm legs. The leaf carries them instead.</td></tr>
<tr><td>An electrician's visit for the socket, dimmers and fittings (v13.6)</td><td>You're doing them yourselves: like-for-like, not notifiable; a new socket behind the sofa and a fused spur are dropped</td></tr>
</table>
<!--/keep--></body></html>"""
    DECK = False
    html = tidy.strip_versions(html).replace("<!--keep-->", "").replace("<!--/keep-->", "")   # v24: no round markers in the text
    return html, tl, th, c, css


def plan_sections():
    """The plan split at its h2s, for the plan page: {"pre": the title block, "1".."12", "appendix": html}."""
    import re
    html = _plan(deck=True)[0]
    body = html.split("<body>", 1)[1].rsplit("</body>", 1)[0]
    parts = re.split(r'(?=<h2[ >])', body)
    out = {"pre": parts[0]}
    for part in parts[1:]:
        m = re.match(r'<h2[^>]*>(\d+|Appendix) · ([^<]+)</h2>', part)
        key = ("earlier" if m.group(2).startswith("Earlier") else "ideas" if m.group(2).startswith("Ideas") else m.group(1).lower()) if m else "x"
        out[key] = part[m.end():] if m else part
    return out


def build():
    html, tl, th, c, css = _plan()
    (HERE / "plan.html").write_text(html)
    guide = f"""<!doctype html><html><head><meta charset="utf-8"><title>Build Guide</title><style>{css}</style></head><body>
<h1>Media Wall &amp; Dining Wall: Build Guide</h1>
<p class="byline">Version {VERSION} · Oct 21, 2026 · for Emma and Dave · sizes in cm</p>
<figure class="render small">{img("render_v13_join_clean.png", "The finished wall")}</figure>
{guide_pdf_html()}
<h2 class="pb">Shopping list</h2>
<p>About £{money(tl, th)}, in build order; no electrician on top.</p>
<table class="tracker"><thead><tr><th>Status</th><th>Item</th><th>Qty</th><th>Estimate (£)</th><th>Paid (£)</th></tr></thead><tbody>
{tracker_rows()}</tbody></table>
</body></html>"""
    (HERE / "guide.html").write_text(tidy.strip_versions(guide))
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
