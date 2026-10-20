"""v13.7: lighting scenes. Four ways to set the room's six light layers: the ceiling LED strip on its own controller, the
uprights' grooves and the side-wall shelf's strip (smart colour since v16, in the bulbs' app), the bias light with the
TV, and (v15) bar 1, bar 2 and the red lamp on smart colour bulbs, set in their app (v17: every head straight down). Levels are 0-100. Used by diagrams.light_scene(), the plan's
section 8 and the viewer's scene buttons."""

LAYERS = [("strip", "Ceiling LED strip", "its own controller"), ("uprights", "Uprights' grooves and the side shelf", "the strips' app (smart colour since v16)"),
          ("bias", "TV bias light", "comes on with the TV"), ("bar1", "Bar 1, between the TV and the sofa", "smart bulbs: the app"),
          ("bar2", "Bar 2, by the stairs", "smart bulbs: the app"), ("lamp", "Your red lamp", "its colour bulbs: the app")]

SCENES = [
    ("general", "General", "An even light over the whole room: every head straight down, the strips and the lamp filling in. The default (v17).",
     {"strip": 55, "uprights": 45, "bias": 0, "bar1": 60, "bar2": 60, "lamp": 45},
     ["All eight heads point straight down, spread a little along each bar, so the pools overlap instead of spotlighting the walls.",
      "The ceiling strip and the uprights fill the edges; the lamp adds a low warm layer.",
      "Tilt a head only if its pool lands badly (on the TV's screen, or in someone's eyes)."]),
    ("tv", "TV night", "Films and games: the screen is the brightest thing in the room, with a little warm light round it so your eyes don't strain.",
     {"strip": 10, "uprights": 15, "bias": 100, "bar1": 0, "bar2": 10, "lamp": 70},
     ["Bar 1 off: its heads hang in front of the screen, and even tilted away they'd catch it.",
      "The bias light behind the TV and your red lamp do the work: the lamp is the one to leave on for a film (down to about 70).",
      "Bar 2 just glowing on the framed LPs, so the far end of the room isn't a black hole."]),
    ("dinner", "Dinner", "The table is the bright spot, the media wall steps back.",
     {"strip": 25, "uprights": 30, "bias": 0, "bar1": 15, "bar2": 80, "lamp": 0},
     ["Bar 2 up: for four its heads light the table at the wall; for six, the table stands right under it (point blue and mustard straight down).",
      "Bar 1 low, so the coffee table end isn't dark; the TV off.",
      "The uprights low: the shelves read as a backdrop, not a stage."]),
    ("records", "Records", "Pick a record, read the sleeve: light on the deck, the ledge and the trays.",
     {"strip": 35, "uprights": 60, "bias": 0, "bar1": 60, "bar2": 15, "lamp": 80},
     ["Bar 1 up: its pink head is on the turntable and the Series X, blue on the record ledge.",
      "The uprights' grooves up, washing the wall either side of the (switched-off) TV and the ledge LPs.",
      "The lamp up for reading sleeves on the sofa."]),
    ("everyday", "Everyday evening", "Everything on at a comfortable level, for tidying, chatting and finding the remote.",
     {"strip": 70, "uprights": 50, "bias": 0, "bar1": 55, "bar2": 40, "lamp": 60},
     ["The ceiling strip does most of it; both bars fill in the shelves and the table.",
      "Turn the strip down first as the evening goes on: it's the flattest light in the room."]),
]


def level_word(v):
    return "off" if v == 0 else ("on" if v == 100 else f"{v}%")
