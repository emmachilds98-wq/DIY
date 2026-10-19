"""v13.6: ONE list of what we still need from Emma and Dave, most consequential first. The plan PDF's "Still to confirm"
(build_doc.py) and the viewer's Questions tab (build_viewer.py) both read it, so they can't drift apart.
Ids are kept from earlier rounds: answers already saved in the viewer's db stay attached to their question.
Answered and dropped in v13.6: the door, the walls, the PC case (v12.1), and where the leaf and legs live (the leaf carries them)."""
import geometry as G

LPS = 2 * G.TRAY_LPS + G.LEDGE_LPS + G.WRAP_LPS
SINGLES = 2 * G.TRAY_SINGLES


def _n(x):
    return f"{x:g}"


# (id, question, why it matters, how to check, a photo helps)
QUESTIONS = [
    ("electrics", "The electrics: are you swapping the light fittings, the dimmers and the socket yourselves?",
     "v13.6 plans all three as your own job (like for like, not notifiable), with the safe routine and the stop list. You said \"other than maybe changing a few fixtures\": if you'd rather an electrician did just the fittings, say so and we'll add that visit back.",
     "Yes, all ours; or: an electrician for the fittings only.", False),
    ("sofa", "Your L-sofa's return: how far does it run along the side wall?",
     f"The long side is about {_n(G.SOFA_W)} from your photo; the return is drawn at {_n(G.SOFA_D)}. It sets the PC shelf, the walkway and the dining clearances.",
     "Overall depth with the return, from the window wall; back height and seat depth too if you can.", False),
    ("westend", "The west end's sizes: which of 935, 1045, 660 and 820 are the recess, the door and the stair box?",
     "The stair box and the door are drawn roughly until we know.", "A photo of that end of the room, or the sketch with each number pointed at.", True),
    ("stairs", "The stairs by the door go up (thanks). Which way does the flight run?",
     "v13 draws them rising away from the room towards the hall, behind the wooden banister.", "A photo from the room settles it.", True),
    ("turntable", "The turntable's make and model, and does it have a PHONO/LINE switch?",
     "The zone takes up to 45.2 × 35.2 cm; the switch decides whether you need the separate preamp.", "The model is usually on the plinth or underneath.", True),
    ("fanstand", "The Series X fan stand's make and model",
     f"The shelf takes a footprint up to about 30 cm wide; the plan assumes {_n(G.FAN_STAND[0])} × {_n(G.FAN_STAND[2])}.", "A photo of the stand is enough.", True),
    ("chairs", "Dining chairs: ones you have, or four folding ones? And where will they be kept?",
     "The plan draws IKEA TERJE (seat 48); any chair with a 45–48 cm seat works. The leaf, with all eight legs inside it, stores with the chairs.",
     "Seat height of yours, and the spot you have in mind (the garage?).", False),
    ("box", "The 23 × 22 cm box in the window's west corner: what is it?",
     "If it's pipe boxing it stays; if not, it might go.", "A photo is quickest.", True),
    ("records", "Roughly how many LPs and singles, and are most in thick outer sleeves?",
     f"The wall holds about {LPS} LPs and {SINGLES} singles, all face-out. Thick sleeves need a wider trough.", "A rough count is fine.", False),
    ("games", "Roughly how many PS2, Xbox 360 and Xbox One games?",
     "The game drawer holds about 48, 12 of them face-out; more needs an overflow spot.", "A count of each is plenty.", False),
    ("ports", "Wired ports for the projector (master) and the music room (bedroom 2)?",
     "Each is one more Cat6 run on the same day as the other two (step 3); easier now than later.", "Yes or no for each.", False),
    ("surge", "The 10-gang: is it surge-protected, where are its two switches, and how long is it?",
     f"It now feeds the PC as well as the TV and the modern consoles; if it isn't surge-protected, swap it for one that is. The plan allows {_n(G.TEN_GANG[0])} cm.",
     "Look for 'surge' on the label; end to end, sockets only.", True),
    ("models", "Console model numbers, from the labels underneath",
     "The rows assume the largest version of each console; real models may free up height.", "Photos of the labels are fine.", True),
    ("point2", "The second ceiling point's exact spot",
     "The plan puts it about 35 cm in from the west wall and 2.3 m from the window.", "Measure from the west wall, and from the window wall.", False),
    ("retrotink", "The RetroTINK-6X CE's size, when it arrives",
     "RetroTINK publishes no size; bay 1 allows 23 × 23 × 8 beside the Xbox 360.", "Width, depth and height, or a photo with a tape measure.", True),
]

# a short line for the plan PDF's "Still to confirm" list, by id
PDF_LINE = {
    "electrics": "The electrics: you're swapping the light fittings, the dimmers and the socket yourselves (as planned), or an electrician for the fittings only?",
    "sofa": f"The sofa's return: how far it runs along the side wall (the long side is about {_n(G.SOFA_W)} from your photo; the return is drawn at {_n(G.SOFA_D)}).",
    "westend": "The west end's sizes: which of 935, 1045, 660 and 820 are the recess, the door and the stair box.",
    "stairs": "The stairs go up (thanks): which way does the flight run, away from the room towards the hall, or towards the window? A photo settles it.",
    "turntable": "The turntable's model (the zone takes up to 45.2 × 35.2 cm) and whether it has a PHONO/LINE switch.",
    "fanstand": "The Series X fan stand's model: the shelf takes a footprint up to about 30 cm wide.",
    "chairs": "Dining chairs: use ones you have (seat 45–48), or four folding ones? And where they'll be kept: the leaf, legs inside, goes with them.",
    "box": "The 23 × 22 cm box in the window's west corner.",
    "records": f"Records: roughly how many LPs and singles (the wall holds about {LPS} and {SINGLES}), and are most in thick outer sleeves?",
    "games": "Games: roughly how many PS2, Xbox 360 and Xbox One games? The drawer holds about 48.",
    "ports": "Wired ports for the projector (master) and the music room (bedroom 2)?",
    "surge": "The 10-gang: is it surge-protected, where are its two switches, and how long is it? It now feeds the PC too.",
    "models": "Console model numbers, from the labels underneath, to tighten the row heights; the plan assumes the largest version of each.",
    "point2": "The second ceiling point's exact spot (the plan puts it about 35 cm in from the west wall, 2.3 m from the window).",
    "retrotink": "The RetroTINK-6X CE's size when it arrives (bay 1 allows 23 × 23 × 8).",
}
assert set(PDF_LINE) == {q[0] for q in QUESTIONS}


def pdf_items():
    return "\n".join(f"<li>{PDF_LINE[q[0]]}</li>" for q in QUESTIONS)
