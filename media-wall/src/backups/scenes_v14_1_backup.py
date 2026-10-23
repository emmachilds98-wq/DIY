"""v13.7: lighting scenes. Four ways to set the room's six light layers, each on the control it already has (no smart kit):
the ceiling LED strip on its own controller, the uprights' grooves on their plug-in driver's inline dimmer, the bias light
with the TV, bar 1 and bar 2 each on its LED dimmer (one per bar: the heads stay aimed as in the Paint and light table),
and the lamp by the sofa. Levels are 0-100 (a dimmer's travel, roughly). Used by diagrams.light_scene(), the plan's
section 8 and the viewer's scene buttons."""

LAYERS = [("strip", "Ceiling LED strip", "its own controller"), ("uprights", "Uprights' LED grooves", "the inline dimmer on its driver's lead"),
          ("bias", "TV bias light", "comes on with the TV"), ("bar1", "Bar 1, between the TV and the sofa", "its wall dimmer"),
          ("bar2", "Bar 2, by the door", "its wall dimmer"), ("lamp", "Lamp by the sofa", "its own switch")]

SCENES = [
    ("tv", "TV night", "Films and games: the screen is the brightest thing in the room, with a little warm light round it so your eyes don't strain.",
     {"strip": 10, "uprights": 15, "bias": 100, "bar1": 0, "bar2": 10, "lamp": 100},
     ["Bar 1 off: its heads hang in front of the screen, and even tilted away they'd catch it.",
      "The bias light behind the TV and the lamp by the sofa do the work: the lamp is the one to leave on for a film.",
      "Bar 2 just glowing on the framed LPs, so the far end of the room isn't a black hole."]),
    ("dinner", "Dinner", "The table is the bright spot, the media wall steps back.",
     {"strip": 25, "uprights": 30, "bias": 0, "bar1": 15, "bar2": 80, "lamp": 0},
     ["Bar 2 up: for four its heads light the table at the wall; for six, the table stands right under it (point blue and mustard straight down).",
      "Bar 1 low, so the coffee table end isn't dark; the TV off.",
      "The uprights low: the shelves read as a backdrop, not a stage."]),
    ("records", "Records", "Pick a record, read the sleeve: light on the deck, the ledge and the trays.",
     {"strip": 35, "uprights": 60, "bias": 0, "bar1": 60, "bar2": 15, "lamp": 100},
     ["Bar 1 up: its pink head is on the turntable and the Series X, blue on the record ledge.",
      "The uprights' grooves up, washing the wall either side of the (switched-off) TV and the ledge LPs.",
      "The lamp on for reading sleeves on the sofa."]),
    ("everyday", "Everyday evening", "Everything on at a comfortable level, for tidying, chatting and finding the remote.",
     {"strip": 70, "uprights": 50, "bias": 0, "bar1": 70, "bar2": 40, "lamp": 100},
     ["The ceiling strip does most of it; both bars fill in the shelves and the table.",
      "Turn the strip down first as the evening goes on: it's the flattest light in the room."]),
]


def level_word(v):
    return "off" if v == 0 else ("on" if v == 100 else f"{v}%")
