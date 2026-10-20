"""v18: the plant ladder is dropped (the client bought a plant stand); new: TV backlight sync, cushions, a plant uplight, a rug pad.
Next round (the client, "put in next run"): somewhere to keep the dining chairs, only if it's easy without changing the table much.
v17: ideas for later. These are suggestions only: they're not in the plan, the buy list or the costs. The viewer's Ideas tab, the
3D room's "Ideas (not in the plan)" buttons (all off by default) and the plan PDF's appendix all read this list.
Client (round 11): ideas welcome, but "small enough for this room" (the glass cabinet worry), so nothing here stands on the floor
bigger than a side table. Sizes are our own suggestions, in cm; positions are room coordinates (x from the side wall, z negative
into the room), as in geometry.py."""
import geometry as G

WZ = G.WINDOW_Z

# (id, title, size, rough cost £, why it suits the room, where it goes, in 3D)
IDEAS = [
    ("case", "A slim glass display case on the chimney breast",
     "90 wide × 50 tall × 12 deep", (60, 120),
     "For the hats or collectibles, lit from inside, without a cabinet on the floor: 12 deep, so it stands no further out than a picture "
     "ledge. Oak frame from the offcuts, a 4 mm toughened glass front that lifts off, an LED strip under the top on the strips' app. "
     "It takes the place of the two framed LPs, above the “now playing” ledge.",
     "On the breast, centred, from 137 to 187 (just clear of the sleeves on the “now playing” ledge); with the table by the stairs only.", True),
    ("glass", "Glass plant shelves across the window reveal",
     "two 10 mm toughened shelves, 235 × 18, at 130 and 170", (120, 200),
     "Your deep sill already takes a row of plants; two glass shelves above it make the window a green screen that still lets the light "
     "through. Studs into the reveal's sides, and a slim steel rod down from the head at the middle so a 235 span can't sag.",
     "Inside the window's 22 cm reveal, in front of the glass, clear of the curtains.", True),
    ("ctable", "An oak C-shaped side table for the sofa's open end",
     "top 45 × 30, 60 tall", (25, 60),
     "The ottoman end has no arm to put a drink on. A C-table's top slides over the end of the seat and its foot sits flat on the floor "
     "beside it, so drinks and pads are at hand and it moves away when someone lies along the seat. Made from the oak offcuts.",
     "At the sofa's open end, towards the TV.", True),
    ("sync", "TV backlight that follows the picture",
     "a sync box on the HDMI line and a strip behind the TV (in place of the plain bias light)", (60, 130),
     "The wall behind the TV glows with the colours on screen, in the same app as the bars and strips, so a film can tint the room.",
     "Behind the TV, on the bias light's place; the box sits by the HDMI switch in bay 1.", False),
    ("cushions", "Cushions and a throw in the rug's rust and ochre",
     "two or three 45 × 45 cushions and a throw", (40, 90),
     "They tie the blue corduroy sofa to the rug and the oak, and soften the ottoman end.", "The sofa.", False),
    ("plantlight", "A small uplight under the plant stand's bottom tier",
     "a plug-in spot, about 10 cm", (10, 20),
     "Throws the leaves' shadows up the wall at night, so the plants are part of the evening lighting even with their grow bars off.",
     "On the floor, under the stand.", False),
    ("rugpad", "A non-slip pad under the rug",
     "220 × 150, trimmed to fit", (15, 30),
     "Keeps the rug flat and square on the carpet where the sofa's open end and the coffee table push it.", "Under the rug.", False),
    ("button", "A smart scene button by the door",
     "a small wireless button, about 5 × 5", (15, 25),
     "One press for the General scene coming in, a long press for everything off, in the same app as the bars' bulbs and the strips.",
     "On the wall beside the door's light switch.", False),
    ("night", "A motion nightlight on the stairs",
     "battery LED strips under the treads' noses, or a single motion light", (15, 30),
     "A soft glow on the stairs at night with nothing to wire; it turns itself off.", "The stairs.", False),
    ("clean", "A record-cleaning tray in the pads drawer",
     "a small tray, about 30 × 15", (10, 20),
     "The carbon brush, a stylus brush and a cleaning fluid kept together next to the deck.", "Bay 3's pads drawer.", False),
]

# where each 3D idea is drawn (room cm)
CASE = dict(x=((G.BREAST_X[0] + G.BREAST_X[1]) / 2 - 45.0, (G.BREAST_X[0] + G.BREAST_X[1]) / 2 + 45.0), y=(137.0, 187.0), d=12.0, frame=2.0)
GLASS = dict(x=G.WINDOW_X, ys=(130.0, 170.0), d=18.0, t=1.0)
CTABLE = dict(x=(40.0, 85.0), top=60.0, depth=30.0, over=16.0, t=2.0)   # "over": how far the top reaches over the seat's end
SPOTS = dict(case=CASE, glass=GLASS, ctable=CTABLE)   # v18: the plant ladder is dropped: your new plant stand does its job


def low_high():
    return sum(i[3][0] for i in IDEAS), sum(i[3][1] for i in IDEAS)


def pdf_html():
    """The plan PDF's appendix: one paragraph per idea."""
    lo, hi = low_high()
    rows = "".join(f"<tr><td><b>{t}</b><br><span class='note'>{size}</span></td><td>{why} <i>{where}</i></td><td class='num'>{c[0]}–{c[1]}</td></tr>"
                   for _, t, size, c, why, where, _3d in IDEAS)
    return (f"<p>Suggestions only, for later: they aren't in the plan, the buy list or the costs (all of them together would be about "
            f"£{lo}–{hi}). The first three can be seen in the 3D room with the “Ideas (not in the plan)” buttons, all off until you turn them on.</p>"
            f"<table class='tight'><tr><th>Idea</th><th>Why, and where</th><th>About £</th></tr>{rows}</table>")
