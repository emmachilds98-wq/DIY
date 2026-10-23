"""v32, client: "please also add a cost overview that shows each piece and list breakdown of shopping items. ie the media wall. 2 x cabinet
from ikea, 2 x 1.8m wood etc ... i need clear buy list and estimated cost without incorporating large explanations".

Every "To buy" row of build_doc.TRACK, by piece, with a short name. The estimates are the buy list's own (TRACK's lo and hi), so the
totals always match it. A row is matched on the start of its text; one nobody named lands in "Other", under its first clause."""
import re

# (piece, the row's text starts with, quantity shown, short name); pieces in this order
PIECES = ["The media wall", "The side wall and the PC", "The dining cabinet", "The chimney breast", "Lighting", "Paint",
          "Network", "Electrics (your own job)", "Power and cables", "TV, consoles and AV", "Vinyl kit", "Finishing touches"]
SHORT = [
    ("The media wall", "Two IKEA BESTÅ 60×40×64 frames", "2", "IKEA BESTÅ frame, 60 × 40 × 64"),
    ("The media wall", "BESTÅ shelves, 56 × 36", "4", "IKEA BESTÅ shelf, 56 × 36"),
    ("The media wall", "Plinth for bays 1–2", "1", "Plinth frame, 18 mm ply"),
    ("The media wall", "Hidden plinth drawer", "1", "Plinth drawer: oak front, ply box, runners"),
    ("The media wall", "Bay 3 carcass", "1", "Bay 3 carcass, 18 mm birch ply"),
    ("The media wall", "Two face-out LP crates", "2", "Face-out LP crate: ply, oak lip, runners"),
    ("The media wall", "Three slim drawers for the game column", "3", "Slim game drawer: ply, oak lip, runners"),
    ("The media wall", "Game drawer kit", "1", "Game drawer: ply, soft-close runners"),
    ("The media wall", "The sub in bay 2", "1", "Sub riser and ply divider"),
    ("The media wall", "Anti-tip brackets", "1 set", "Anti-tip brackets and spacers"),
    ("The media wall", "Two solid oak uprights", "2", "Solid oak upright, 165 × 30 × 4.5"),
    ("The media wall", "Solid oak for the shelves", "1 set", "Solid oak for the shelves and the side-wall run"),
    ("The media wall", "One solid oak worktop", "1", "Solid oak worktop, 300 × 62"),
    ("The media wall", "Oak face frame", "1", "Oak face frame, 186 cm"),
    ("The media wall", "Oak wedges, 10 mm oak dowel", "1 set", "Oak wedges, dowel, concealed brackets"),
    ("The side wall and the PC", "Keyboard tray for the PC shelf", "1", "Keyboard tray: oak housing, ply tray, runners"),
    ("The side wall and the PC", "Conduit: 38 mm and 25 mm oval", "1 set", "Oval conduit, 38 and 25 mm, and a 5 m C13 lead"),
    ("The side wall and the PC", "For the chase", "1", "Wall chaser for a day, and filler"),
    ("The side wall and the PC", "PC tidy kit", "1", "PC tidy kit: sleeve, grommet"),
    ("The side wall and the PC", "A powered USB 3 hub", "1", "Powered 4-port USB 3 hub"),
    ("The side wall and the PC", "A remote power button for the PC", "1", "Remote PC power button"),
    ("The side wall and the PC", "A magnetic mesh dust filter", "1", "Magnetic dust filter"),
    ("The dining cabinet", "The dining cabinet: oak-faced ply", "1 set", "Oak-faced ply, cut to size: two boxes, two doors"),
    ("The dining cabinet", "Solid oak for the table", "1 set", "Solid oak for the table, two 92.5 × 90 halves"),
    ("The dining cabinet", "Oak for the cabinet's hinge rail", "1 set", "Oak: hinge rail, aprons, four legs, door stops"),
    ("The dining cabinet", "Altro continuous piano hinge, 1800 × 50", "1", "Piano hinge, 1800 × 50 (the table)"),
    ("The dining cabinet", "The doors' hinges and catches", "1 set", "Two door piano hinges, catches, magnet, hooks"),
    ("The dining cabinet", "Folding, self-locking table-leg brackets", "1 set", "Folding leg brackets (4), tabletop fasteners (16)"),
    ("The dining cabinet", "Three Lee Valley 40574", "3", "Lee Valley flip-top hinge"),
    ("The dining cabinet", "Folding chairs, IKEA FRÖSVI", "6", "IKEA FRÖSVI folding chair, beech"),
    ("The dining cabinet", "Six tie-on seat pads", "6", "Dunelm Esme tie-on seat pad"),
    ("The chimney breast", "Two LP frames", "2", "LP frame"),
    ("The chimney breast", "The “now playing” ledge", "1", "“Now playing” oak ledge and brackets"),
    ("Lighting", "Two Dunelm Elements Wolston", "2", "Dunelm Wolston 4-light spot bar"),
    ("Lighting", "Eight smart colour E14 bulbs", "8", "Smart colour E14 bulb"),
    ("Lighting", "Smart colour strips", "1 set", "Smart colour LED strip, 4.5 m, with channels"),
    ("Lighting", "Optional: a smart button", "1", "Smart scene button (optional)"),
    ("Lighting", "Later: aluminium channel", "1", "Ceiling strip channel and diffuser (later)"),
    ("Paint", "Card Room Green", "1 lot", "Farrow & Ball Card Room Green: emulsion, eggshell, primer"),
    ("Paint", "Woodwork primer", "1 set", "Woodwork primer, sanding pads, sugar soap"),
    ("Network", "TP-Link TL-SG108", "2", "TP-Link TL-SG108 8-port switch"),
    ("Network", "Cat6 patch leads", "11", "Cat6 patch lead, 0.5–2 m"),
    ("Network", "Cat6 solid pure copper", "2–4 runs", "Cat6 solid copper cable"),
    ("Network", "Cat6 tools", "1 set", "Cat6 tools: punch-down, keystones, tester, draw rods"),
    ("Electrics (your own job)", "A double socket", "1", "Double socket and back box"),
    ("Electrics (your own job)", "Electrical safety kit", "1 set", "Safety kit: GS38 tester, lock-off, socket tester"),
    ("Electrics (your own job)", "Insulated (VDE) screwdrivers", "1 set", "Insulated screwdrivers, strippers, cutters"),
    ("Power and cables", "6-way surge-protected extension", "1", "6-way surge-protected extension"),
    ("Power and cables", "4-port USB charger", "1", "4-port USB charger"),
    ("Power and cables", "USB plug, 5 V 2 A", "1", "USB plug, 5 V 2 A"),
    ("Power and cables", "Cable kit", "1 set", "Cable kit: grommets, velcro ties, labels"),
    ("Power and cables", "Flat two-compartment trunking", "1", "Flat trunking, 2 m"),
    ("TV, consoles and AV", "RetroTINK-6X CE upscaler", "1", "RetroTINK-6X upscaler"),
    ("TV, consoles and AV", "5-in-1 4K60 HDMI switch", "1", "5-in-1 4K HDMI switch"),
    ("TV, consoles and AV", "Active optical HDMI cable", "1", "Active optical HDMI cable, 5 m"),
    ("TV, consoles and AV", "High Speed HDMI leads", "5 + 2", "HDMI lead, 1–2 m, and 90° adapters"),
    ("TV, consoles and AV", "PS2 component video cable", "1", "PS2 component cable"),
    ("TV, consoles and AV", "Optical (TOSLINK) cable", "1", "Optical cable, 2 m"),
    ("TV, consoles and AV", "RGB SCART cable", "1", "PS1 RGB SCART cable"),
    ("Vinyl kit", "Replacement stylus", "1", "Replacement stylus"),
    ("Vinyl kit", "External phono preamp", "1", "Phono preamp (only if needed)"),
    ("Vinyl kit", "RCA-to-3.5 mm lead", "1", "RCA to 3.5 mm lead, 2 m"),
    ("Vinyl kit", "Isolation feet for the turntable", "1 set", "Isolation feet and a record brush"),
    ("Finishing touches", "A rug about 230 × 160", "1", "Rug, about 230 × 160"),
    ("Finishing touches", "Drip trays or a waterproof mat", "1", "Drip trays for the plant stand"),
    ("Finishing touches", "Felt pads under the vinyl stand", "1 set", "Felt pads"),
]


def _plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def overview(track):
    """[(piece, lo, hi, [(qty, name, lo, hi)])] in PIECES order, every "To buy" row of track exactly once."""
    out = {p: [] for p in PIECES}
    order = {pre: i for i, (_p, pre, _q, _n) in enumerate(SHORT)}
    for st, item, ph, q, lo, hi in track:
        if st != "To buy":
            continue
        t = _plain(item)
        hit = next((s for s in SHORT if t.startswith(s[1])), None)
        if hit:
            out[hit[0]].append((order[hit[1]], hit[2], hit[3], lo or 0, hi or 0))
        else:
            out.setdefault("Other", []).append((999, q or "1", re.split(r"[:;(]", t)[0].strip(), lo or 0, hi or 0))
    res = []
    for p, rows in out.items():
        if rows:
            rows.sort(key=lambda r: r[0])
            res.append((p, sum(r[3] for r in rows), sum(r[4] for r in rows), [r[1:] for r in rows]))
    return res


def qty(q):
    q = (q or "").strip()
    return (q + " ×") if re.match(r"^\d+$", q) else q


def text(track, money):
    """The overview as a plain shopping list, to copy."""
    lines = []
    for p, lo, hi, rows in overview(track):
        lines += ["", f"{p.upper()} (about £{money(lo, hi)})"] + [f"- {qty(q)} {n}: £{money(a, b)}" for q, n, a, b in rows]
    tl = sum(r[1] for r in overview(track)); th = sum(r[2] for r in overview(track))
    return f"Shopping list, about £{money(tl, th)} in all" + "\n".join(lines)
