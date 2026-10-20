"""v20: answered and dropped: hdcrash ("no crashes"); chairs now six ideally, four fine; the ledge is 25 (as drawn).
v18.1: answered by the listings the client sent and dropped: the plant stand (98 × 29.5 × 158) and the vinyl stand (70 × 32 × 78).
v15: answered by the client's notes (20 Oct) and dropped: the lamp (it stays: bright red, colour bulbs green, pink, purple).
New: hat, lightbox. The curtains and the carpet came with the client's photo the same day (asked and answered).
v14: answered by the client's photos (20 Oct) and dropped: the stairs' direction (a straight flight rising towards the door).
New: site, westwall, lamp.
v13.6: ONE list of what we still need from Emma and Dave, most consequential first. The plan PDF's "Still to confirm"
(build_doc.py) and the viewer's Questions tab (build_viewer.py) both read it, so they can't drift apart.
Ids are kept from earlier rounds: answers already saved in the viewer's db stay attached to their question.
Answered and dropped in v13.6: the door, the walls, the PC case (v12.1), and where the leaf and legs live (the leaf carries them)."""
import geometry as G

LPS = G.ALL_LPS   # v19: 291: the wall's 191 (all face-out) and the vinyl stand's 100
SINGLES = 2 * G.TRAY_SINGLES


def _n(x):
    return f"{x:g}"


# (id, question, why it matters, how to check, a photo helps)
QUESTIONS = [
    ("westwall", "The stairs wall under your shelf: solid, or plasterboard on studs?",
     "The table goes there now (v16, the default): its brackets are rated 500 kg a pair, and the fixings depend on the wall.",
     "Knock along it: a hollow sound is plasterboard. Or look at how the shelf is fixed.", False),
    ("electrics", "The electrics: are you swapping the two light fittings and the socket yourselves?",
     "The plan has both as your own job (like for like, not notifiable), with the safe routine and the stop list. Since v15 there are no dimmers to fit: the bars take smart bulbs. If you'd rather an electrician did the fittings, say so and we'll add that visit back.",
     "Yes, all ours; or: an electrician for the fittings only.", False),
    ("sofa", "Your L-sofa's return: how far does it run along the side wall?",
     f"The long side is about {_n(G.SOFA_W)} from your photo; the return, with its open ottoman-style end towards the TV (v16), is drawn at {_n(G.SOFA_D)}, the sofa standing {_n(G.SOFA_BACK_Z - G.WINDOW_Z)} off the window wall (v17). It sets the PC shelf, the walkway and the dining clearances.",
     "Overall depth with the return, from the window wall; back height and seat depth too if you can.", False),
    ("westend", "The stairs wall's sizes: its length, and where your shelf sits on it",
     "Your photos give about 257–268 cm from the stair box to the window corner, the shelf starting about 41 cm from the stairs; it's drawn stopping 2 short of the pipe boxing, its top at 196. Your OBEGRÄNSAD (36 tall) only stands on it under the 235 ceiling if the top is 198 or lower. The table under it is drawn from these.",
     "Tape along the wall at floor level; the shelf's two ends from the corner, and its height from the floor.", True),
    ("turntable", "The turntable's make and model, and does it have a PHONO/LINE switch?",
     "The zone takes up to 45.2 × 35.2 cm; the switch decides whether you need the separate preamp.", "The model is usually on the plinth or underneath.", True),
    ("fanstand", "The Series X fan stand's make and model",
     f"The shelf takes a footprint up to about 30 cm wide; the plan assumes {_n(G.FAN_STAND[0])} × {_n(G.FAN_STAND[2])}.", "A photo of the stand is enough.", True),
    ("chairs", "The chair cupboard: four chairs (22 deep, flush) or six (31 deep)?",
     f"v20: the chair cupboard beside the table holds four folded chairs at {_n(G.CHAIR_STORE['cupboard']['d'])} deep, flush with the pipe boxing, or six at {_n(G.CHAIR_STORE['cupboard']['d6'])} deep, standing {_n(G.CHAIR_STORE['cupboard']['d6'] - G.CHAIR_STORE['cupboard']['d'])} cm proud of it. With four inside, chairs five and six go in the garage, or under the stairs if the side by the door is open (inside the room the flight is only about {_n(G.CHAIR_STORE['under_stairs']['h'])} cm high).",
     "Four or six, and a photo of the side of the stairs by the door if five and six might go under them.", True),
    ("records", "Roughly how many LPs?",
     f"About {LPS} in all (v19): {G.WALL_LPS} in the wall, all face-out (two snug LP crates in bay 3 since v16), and {G.STAND_LPS} in your vinyl stand ({G.RECORD_SHELF['lps_top']} face-out on top, {G.RECORD_SHELF['lps_bottom']} spine-up between the wires). If there are more, the neatest overflow is another LP column like bay 3's.", "A rough count is fine.", False),
    ("games", "Roughly how many PS2, Xbox 360 and Xbox One games?",
     f"The game drawer in bay 1 holds about 48 and the two slim drawers in bay 3 about {G.SLIM_GAMES} more, face-out (v16): about {48 + G.SLIM_GAMES} in all.", "A count of each is plenty.", False),
    ("ports", "Wired ports for the projector (master) and the music room (bedroom 2)?",
     "Each is one more Cat6 run on the same day as the other two (step 3); easier now than later.", "Yes or no for each.", False),
    ("surge", "The 10-gang: is it surge-protected, where are its two switches, and how long is it?",
     f"It now feeds the PC as well as the TV and the modern consoles; if it isn't surge-protected, swap it for one that is. The plan allows {_n(G.TEN_GANG[0])} cm.",
     "Look for 'surge' on the label; end to end, sockets only.", True),
    ("models", "Console model numbers, from the labels underneath",
     "The rows assume the largest version of each console; real models may free up height.", "Photos of the labels are fine.", True),
    ("point2", "The pendant point by the stairs wall: its exact spot",
     "From your photo it hangs about 55 cm out from the stairs wall, a quarter of the way along the shelf from the stair end. Bar 2 goes on it, over the table if you choose that spot.",
     "Measure from the stairs wall and from the window wall.", False),
    ("cornergap", "The window corner at floor level: from the pipe boxing to the curtains",
     f"Thanks for the 25 cm: that's the window ledge, and it's drawn 25 deep (a 22 cm reveal and a 3 cm nose). The one still needed is lower down: your plant stand ({_n(G.PLANT_STAND['w'])} wide) is drawn with only {_n((G.PIPE_BOX['x'][0] - G.WINDOW_X[1] - G.CURTAIN['ext'] - G.PLANT_STAND['w']) / 2)} cm a side between the pipe boxing and the curtains when they're open. If it's short, the curtain pole's west end can come in, or swap to layout B.",
     "Tape along the window wall at the floor, from the pipe boxing's face to where the curtains bunch when they're open.", True),
    ("retrotink", "The RetroTINK-6X CE's size, when it arrives",
     "RetroTINK publishes no size; bay 1 allows 23 × 23 × 8 beside the Xbox 360.", "Width, depth and height, or a photo with a tape measure.", True),
]

# a short line for the plan PDF's "Still to confirm" list, by id
PDF_LINE = {
    "westwall": "The stairs wall: solid, or plasterboard on studs? It decides the table's bracket fixings.",
    "electrics": "The electrics: you're swapping the two light fittings and the socket yourselves (as planned; no dimmers since v15), or an electrician for the fittings?",
    "sofa": f"The sofa's return: how far it runs along the side wall (the long side is about {_n(G.SOFA_W)} from your photo; the return is drawn at {_n(G.SOFA_D)}).",
    "westend": "The stairs wall's length and your shelf's height (drawn at 196: the OBEGRÄNSAD needs 198 or lower to stand on it).",
    "turntable": "The turntable's model (the zone takes up to 45.2 × 35.2 cm) and whether it has a PHONO/LINE switch.",
    "fanstand": "The Series X fan stand's model: the shelf takes a footprint up to about 30 cm wide.",
    "chairs": "The chair cupboard by the table (v20): four chairs at 22 deep, flush with the pipe boxing, or six at 31 deep (9 proud)? And a photo of the side of the stairs by the door, if five and six might go there.",
    "cornergap": "The window corner at floor level: from the pipe boxing to the curtains when open (the ledge's 25 cm is in; the plant stand is drawn with 4.5 cm a side).",
    "records": f"Records: roughly how many LPs (the wall and the vinyl stand hold about {LPS}: {G.WALL_LPS} in the wall, all face-out, and {G.STAND_LPS} in the stand)?",
    "games": f"Games: roughly how many PS2, Xbox 360 and Xbox One games? The drawers hold about {48 + G.SLIM_GAMES}.",
    "ports": "Wired ports for the projector (master) and the music room (bedroom 2)?",
    "surge": "The 10-gang: is it surge-protected, where are its two switches, and how long is it? It now feeds the PC too.",
    "models": "Console model numbers, from the labels underneath, to tighten the row heights; the plan assumes the largest version of each.",
    "point2": "The pendant point by the stairs wall (the photo gives about 55 cm out, a quarter of the way along the shelf).",
    "retrotink": "The RetroTINK-6X CE's size when it arrives (bay 1 allows 23 × 23 × 8).",
}
assert set(PDF_LINE) == {q[0] for q in QUESTIONS}


def pdf_items():
    return "\n".join(f"<li>{PDF_LINE[q[0]]}</li>" for q in QUESTIONS)

# v13.8: a few words per question for the plan's one-page summary ("To confirm"), so it follows this list too
SHORT = {
    "westwall": "the stairs wall's build",
    "electrics": "that you're swapping the light fittings yourselves",
    "sofa": "the sofa's return length",
    "westend": "the shelf's height",
    "turntable": "the turntable's model",
    "fanstand": "the fan stand's model",
    "chairs": "the chair cupboard: four or six",
    "cornergap": "the window corner at floor level",
    "records": "record counts",
    "games": "game counts",
    "ports": "extra wired ports",
    "surge": "the 10-gang",
    "models": "console model numbers",
    "point2": "the pendant point",
    "retrotink": "the RetroTINK's size",
}
assert set(SHORT) == {q[0] for q in QUESTIONS}


def summary_line():
    return " · ".join(SHORT[q[0]] for q in QUESTIONS)
