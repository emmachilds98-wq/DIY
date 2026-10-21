"""v13.2: the one source of truth for the room, the media wall, the side wall and the dining wall, in cm.

Every number the renders, diagrams, fit-proof tables and plan text use comes from here, so a change
in one place moves everything. Room measurements are from the client's hand-measured sketch
(inputs/room_sketch_accurate_mm.png); item sizes are in fit.py with their sources.

Axes used everywhere (matches render.py):
  x  across the media wall, from the east (side) wall, which is on the LEFT when you face the TV
  y  height from the floor
  z  depth: 0 is the face of the chimney breast (the alcove's opening line); +z goes back into the
     alcove (its back wall is at z = ALC_D); -z comes out into the room (the window wall is at z = -ROOM_D + ALC_D)

v11 changes against v10: the TV moves 25 cm towards the side wall so the turntable fits in the alcove's
right-hand zone (Series X on a shelf above it, records in bay 3 below); the record ledge wraps round the
corner onto the side wall, with the PC on a shelf above the L-sofa; the chimney breast takes a fold-down
oak dining table instead of the vinyl cabinet; a second spotlight bar hangs over the dining area.
"""

# ---------------------------------------------------------------- the room (from the sketch)
ROOM_W = 467.0        # east wall to west wall, along the window
ROOM_D = 347.0        # window wall to the alcove's back wall
CEIL = 235.0
SKIRT_H, SKIRT_T = 6.0, 2.0
WINDOW_X = (73.0, 308.0)          # on the north (window) wall, measured from the east wall
RADIATOR_X = (158.0, 295.0)       # under the window, ends 13 cm inside the window's west end
NW_BOX = (23.0, 22.0)             # small box in the window wall's west corner (pipe boxing? to confirm)

ALC_W = 186.0         # alcove: east wall to the chimney breast
ALC_D = 38.0          # breast projection on the alcove side
BREAST_W = 117.5
BREAST_X = (ALC_W, ALC_W + BREAST_W)      # 186 to 303.5
BREAST_D_WEST = 39.0                      # 390 on its west side
RECESS_W = 104.5      # breast to the stair box, about (to confirm)
STAIR_X = (BREAST_X[1] + RECESS_W, ROOM_W)  # 408 .. 467, the stair box in the south-west corner (to confirm)
STAIR_STRING = 24.0                          # v23: the closed string's board, along the rake; below it the brick side wall (client)
STAIR_D = 79.0        # from the alcove's back-wall line into the room (to confirm)
STAIRS_UP = True      # v13, client: the stairs by the door go UP to the first floor (v12 drew them going down)
STAIR_RISE, STAIR_GOING = 19.5, 22.0      # typical UK domestic stair (Approved Document K: rise up to 22, going at least 22)
DOOR_X = (BREAST_X[1] + 12.0, BREAST_X[1] + 95.0)   # 315.5 .. 398.5 in the recess (drawn where the agent's plan shows it)
DOOR_SWING = 83.0     # if it opens into the room
WINDOW_Z = ALC_D - ROOM_D                 # -309: the window wall in render coordinates

# ---------------------------------------------------------------- the base unit in the alcove
FRAME_D = 40.0        # IKEA BESTÅ frame depth
FACE = 2.0            # oak face frame
CHAN = 4.0            # cable channel behind the frames (flat two-compartment trunking)
BASE_D = FRAME_D + FACE + CHAN            # 46 from the alcove back wall
BASE_PROUD = BASE_D - ALC_D               # 8: the base stands 8 cm proud of the breast face
BASE_FRONT_Z = -BASE_PROUD                # -8
PLINTH = 9.0
FRAME_H = 64.0
CARCASS_TOP = PLINTH + FRAME_H            # 73
WT = 3.0                                  # solid oak worktop
WORKTOP = CARCASS_TOP + WT                # 76
FILLER = 3.0
BAY_W = 60.0
BAYS = [(FILLER + i * BAY_W, FILLER + (i + 1) * BAY_W) for i in range(3)]   # (3,63) (63,123) (123,183)
BAY_NAMES = ["Bay 1 · Xbox", "Bay 2 · PlayStation", "Bay 3 · records"]
PLINTH_DRAWER = dict(x=(BAYS[1][0] + 3.0, BAYS[1][1] - 3.0), y=(1.6, 7.6), box=(52.0, 34.0, 5.0))   # hidden, push to open

# ---------------------------------------------------------------- above the worktop: the TV 25 cm nearer the side wall
UP_T, UP_D = 4.5, 30.0                    # oak uprights, against the back wall
TV_W, TV_H, TV_D = 122.2, 70.3, 4.5       # LG OLED55C6 without stand (LG UK/SG spec)
TV_STAND_H = 75.7                          # height with stand
TV_STAND_W, TV_STAND_D = 47.0, 23.0
TV_CLEAR = 2.15                           # each side of the screen, inside the uprights
TV_GAP = TV_W + 2 * TV_CLEAR              # 126.5 between the uprights
UP_L = (0.0, UP_T)                        # the left upright is now a corner post against the side wall
UP_R = (UP_T + TV_GAP, 2 * UP_T + TV_GAP) # 131 .. 135.5
TV_CX = UP_L[1] + TV_GAP / 2              # 67.75
TV_SHIFT = ALC_W / 2 - TV_CX              # 25.25 nearer the side wall than v10
TV_X = (TV_CX - TV_W / 2, TV_CX + TV_W / 2)
TV_BOTTOM = WORKTOP + (TV_STAND_H - TV_H)  # 81.4
TV_TOP = TV_BOTTOM + TV_H                  # 151.7
TV_CENTRE = (TV_BOTTOM + TV_TOP) / 2       # 116.55
TV_PANEL_Z = (26.0, 26.0 + TV_D)           # panel 12 cm off the back wall, on its stand
UPRIGHT_LEN = CEIL - WORKTOP               # 159
SIDE_ZONE = 0.0                            # v10's left zone is gone

# the right-hand zone: the turntable on the worktop, the Series X on an oak shelf above it
RZ = (UP_R[1], ALC_W)                      # 135.5 .. 186
RZ_W = RZ[1] - RZ[0]                       # 50.5
DECK = (45.2, 14.2, 35.2)                  # Audio-Technica AT-LP120XUSB, worst case (W, H with lid, D)
DECK_X = (RZ[0] + (RZ_W - DECK[0]) / 2, RZ[0] + (RZ_W + DECK[0]) / 2)   # 138.15 .. 183.35
DECK_Z = (BASE_FRONT_Z + 2.0, BASE_FRONT_Z + 2.0 + DECK[2])           # -6 .. 29.2 (front .. back)
DECK_BODY_H = 10.5                         # plinth top, where the lid hinges (lid adds the rest)
LID = (44.1, 34.6, 7.0)                    # official replacement cover: 17.375 × 13.625 × 2.75 in
LID_TOP_OPEN = WORKTOP + DECK_BODY_H + LID[1]   # about 121: the open lid's top edge, standing upright
LID_CLEAR_TO = 130.0                       # the shelf's underside: lid plus a hand's width
RZ_SHELF_T, RZ_SHELF_D = 4.0, 30.0
RZ_SHELF_TOP = LID_CLEAR_TO + RZ_SHELF_T   # 134
SERIES_X = (15.1, 30.1, 15.1)              # W, H, D standing
FAN_STAND = (20.5, 6.5, 20.5)              # assumed fan stand footprint and height (model to confirm)
SX_X = (RZ[0] + (RZ_W - FAN_STAND[0]) / 2, RZ[0] + (RZ_W + FAN_STAND[0]) / 2)   # 150.5 .. 171
SX_TOP = RZ_SHELF_TOP + FAN_STAND[1] + SERIES_X[1]                               # 170.6
PREAMP = (11.0, 4.5, 11.0)                 # typical external phono preamp, hung under the Series X shelf at the back

LEDGE_UNDER, LEDGE_TOP, LEDGE_D, LEDGE_LIP = 153.0, 155.4, 7.0, 1.5
LP = 31.4                                  # 12-inch sleeve
LEDGE_LP_TOP = LEDGE_TOP + 31.1            # leaning 8 degrees: 186.5
HIGH_TOP, HIGH_T, HIGH_D = 196.0, 4.0, 30.0
HIGH_UNDER = HIGH_TOP - HIGH_T             # 192

SOUNDBAR = (92.0, 6.0, 9.0)                # W, H, D  (Hisense AX5100G)
SUB = (21.4, 29.4, 30.4)                   # W, H, D  (Hisense AX5100G subwoofer, rear port)
TEN_GANG = (56.0, 4.5, 6.0)                # assumed, lying flat behind the TV (length to confirm)

# ---------------------------------------------------------------- records (the v9/v10 trays, now in bay 3 under the deck)
TRAY_LOWER = (2.3, 3.5, 34.4)              # box underside, base top, sleeve tops
TRAY_UPPER = (37.0, 38.2, 69.1)
TRAY_TOP_PANEL = 71.2
TRAY_LPS, TRAY_SINGLES = 90, 0             # v15 client: "vinyl large only, no extra small slot": LP-only trays (were 90 LPs + 120 singles each)
LEDGE_LPS, WRAP_LPS = 4, 4

# ---------------------------------------------------------------- the side (east) wall: the ledge wraps the corner, the PC above the sofa
WRAP_Z = (ALC_D - UP_D, -126.0)           # from the left upright's front edge (z 8) to -126: 134 long
WRAP_D = LEDGE_D                           # 7 deep, same as the ledge over the TV, top 155.4
PC_SHELF_Z = (-130.0, -212.0)              # an oak shelf 82 long over the chaise end of the sofa
PC_SHELF_D, PC_SHELF_T = 28.0, 4.0
PC_SHELF_TOP = LEDGE_TOP                   # one line with the ledge
PC_CASE = (23.0, 46.6, 45.3)               # W (off the wall), H, D (along the wall): client: 'average gaming case' = a mid-tower like the Corsair 4000D, 230 × 466 × 453 mm
PC_Z = (-134.0, -134.0 - PC_CASE[2])       # front faces the alcove
PAD_DOCK = (18.0, 2.2, 9.0)
PC_SCREEN_SLAT = (2.1, 1.2)                # v6.1's slatted screen: oak slats 2.1 wide, 1.2 gaps, open top
KB_TRAY = dict(h=7.0, out=25.0, runners=30.0)   # v6.1's roll-out keyboard tray: 7 cm housing under the PC shelf, rolls 25 cm out
SPINE = (6.0, 6.0)                          # slatted oak spine over the PC's cable drop: off the wall, along the wall
RZ_SLATS = (2.5, 1.5, 2.2)                  # v12's slatted panel behind the turntable zone (gone in v13: PLAIN)
PLAIN = True                                # v13, client: "less cladding all over the place": no slatted spine, PC screen,
                                            # turntable panel or sub box, no reeded table; cables chased into the solid walls

# ---------------------------------------------------------------- the L-sofa (assumed until measured) and the sub
SOFA_W, SOFA_D, SOFA_SEAT_D, SOFA_H = 266.0, 168.0, 95.0, 80.0   # v15 client: "my sofa goes to around 40cm before the end of the window" (window ends at 308, so 268 from the side wall: 266 long from x 2); the return along the side wall (168) still assumed
DOOR_HINGE, DOOR_OPENS_IN = "breast", True  # v12.1 client: hinged on the chimney-breast side, opens into the room
WALLS_SOLID = True                          # v12.1 client: the side wall and the chimney breast are solid
SOFA_X = (2.0, 2.0 + SOFA_W)               # 2 .. 249 along the window wall
SOFA_BACK_Z = WINDOW_Z + 13.0              # -296: v17 13 off the window wall (was 10), clear of the curtains at 11
SOFA_FRONT_Z = SOFA_BACK_Z + SOFA_SEAT_D   # -204: the main run's front
CHAISE_X = (SOFA_X[0], SOFA_X[0] + SOFA_SEAT_D)   # 2 .. 97 along the side wall
CHAISE_END_Z = SOFA_BACK_Z + SOFA_D        # -131
SUB_BOX = dict(x=(207.5, 259.5), z=(-30.0, 0.0), h=42.0)   # v12: slatted oak box over the sub and its riser, between the folded arms
SUB_RISER = dict(x=(212.5, 247.0), z=(-25.4, 0.0), h=5.0)   # v13: the sub on a plain oak riser (replaced in v13.1 by SUB_HOOD)
# v13.1, client: "a box with an open front or something that won't restrict the sound but stops people spilling on it or knocking
# it over". The AX5100G's driver fires out of its front and its port out of its back (Trusted/Expert Reviews), and it stands sideways
# under the table, so the box is open at both ENDS (the driver and the port fire straight out), with a solid oak top (spill shield,
# 1 cm overhang and a drip groove), a solid oak front (takes the kicks) and a base tray with a 2 cm lip; it hangs on a cleat on the breast.
SUB_HOOD = dict(x=(214.0, 249.0), z=(-25.4, 0.0), h=37.4, top=2.0, front=0.0, back=1.5, base=2.0, feet=1.0, lip=2.0, over=1.0)
# v13.2, client: "a sub box that has no sides, just a cover encasing": no front and no ends. A 1.5 cm oak backboard screwed to the
# breast carries a solid 2 cm oak top cantilevered over the sub (spill shield, drip groove) and a base tray with a 2 cm lip all round.
# The top sits 3 cm over the sub, so the sub can't tip: rocking over its edge would lift its far corner about 7 cm, and the top stops it.
SUB_PORT_MIN = 15.0                         # port to the nearest obstruction: 6–12 in (15–30 cm) for rear-ported subs (Klipsch guidance)
SUB_BOX_SLAT = (2.0, 1.4, 1.5)             # slat width, gap, thickness: about 40% open on the front and both ends; solid oak top
SUB_POS = dict(x=(216.3, 216.3 + SUB[2]), z=(-2.0 - SUB[0], -2.0))   # v13.1: standing sideways in its box, driver east, port west   # inside the box: driver east 7 cm from the slats, rear port 14.6 cm from them
# v13.5, client: "adjust the media wall unit to still include the sub somewhere; the consoles' battery packs can be stored
# behind, near the power cables". The Xbox bricks lie flat at the back of their rows (Microsoft: flat, on their pads, in a
# ventilated space), the RetroTINK and the HDMI switch take the fronts those rows free, and the sub takes the lower left of
# bay 2, under the TV, in its own column beside the PS2 and PS1. The dining wall keeps no sub (the oak cover goes).
SUB_IN_WALL = True
BAY_IN = 1.6                                # BESTÅ panels: 56.8 inside a 60 frame, 60.8 inside its 64 height
SUB_RISER_H = 3.0                           # isolation riser (dense foam or sorbothane) the size of the sub's footprint
SUB_DIV_T = 1.2                             # 12 mm ply divider between the sub's column and the PlayStation column
SUB_COL = (BAYS[1][0] + BAY_IN, BAYS[1][0] + BAY_IN + 23.4)   # 64.6 .. 88: the sub's column, 1 cm each side of it
PS_COL = (SUB_COL[1] + SUB_DIV_T, BAYS[1][1] - BAY_IN)       # 89.2 .. 121.4: 32.2 wide, PS2 over PS1
SUB_COL_FLOOR = PLINTH + BAY_IN             # 10.6: bay 2's floor
SUB_COL_TOP = PLINTH + 36.9                 # 45.9: the PS3 shelf's underside (rows 17 + 16.5 and one 1.8 shelf)
SUB_IN = dict(x=(SUB_COL[0] + 1.0, SUB_COL[0] + 1.0 + SUB[0]),
              y=(SUB_COL_FLOOR + SUB_RISER_H, SUB_COL_FLOOR + SUB_RISER_H + SUB[1]),
              z=(BASE_FRONT_Z, BASE_FRONT_Z + SUB[2]))      # front flush with the face frame: the driver faces the room
SUB_PORT_GAP = ALC_D - SUB_IN["z"][1]       # 15.6: the rear port to the alcove's back wall, through the open back and channel
if SUB_IN_WALL:
    SUB_POS = dict(x=SUB_IN["x"], z=SUB_IN["z"])   # the plans draw the sub where it now stands, in bay 2
COFFEE = dict(x=(103.0, 193.0), z=(SOFA_FRONT_Z + 10.0, SOFA_FRONT_Z + 60.0))   # 90 × 50, 10 in front of the sofa

# ---------------------------------------------------------------- the dining wall on the chimney breast
TABLE = (110.0, 80.0, 2.7)                 # W, D, thickness: solid oak
BREADBOARD = 7.0                           # oak breadboard ends, each, pegged; corners radiused 5, underside chamfered
TABLE_CX = (BREAST_X[0] + BREAST_X[1]) / 2 # 244.75
TABLE_X = (TABLE_CX - TABLE[0] / 2, TABLE_CX + TABLE[0] / 2)   # 189.75 .. 299.75
TABLE_TOP = WORKTOP                        # 76 at the wall, on one line with the alcove worktop
# v15, client: "an improved table design that could maybe stay attached to the wall and maybe even seat more people if possible":
# a FLIP-TOP GATE-LEG wall table. The 110 × 80 oak top stays on its hinges and brackets; a second 110 × 80 oak half is hinged to its
# front edge on three brass flip-top hinges (Lee Valley 40574 narrow flip-top hinge, 1.27 × 7.0 cm, made for card and flip-top
# tables; their wider 40208 needs a 30 mm edge and the top is 27) and flips out to make a 110 × 160 table
# running into the room, its far end on a folding oak gate leg (two tapered legs and an apron, hinged under it). To fold: gate up,
# flip the half back onto the top, fold the pair up to the wall. Nothing comes off the wall and there's no leaf to store.
TABLE_STYLE = "fliptop"
FLIP = dict(leaf=(110.0, 80.0, 2.7), hinge=(1.27, 7.0), hinges=3, gate_t=4.6, apron=(7.0, 2.0), inset=8.0, hinge_in=3.0, kg=None)
FLIP_SPACER = FLIP["gate_t"] + FLIP["leaf"][2]   # 7.3: the hinge rail stands this far proud so the folded half and gate fit behind the top
RAIL = (TABLE[0], 22.0, 3.0 + (FLIP_SPACER if TABLE_STYLE == "fliptop" else 0.0))   # oak backboard (3) and its hinge rail on the breast:
                                            # L, H, D; the top hinges on the rail's front edge, brackets on the backboard's face
RAIL_TOP = TABLE_TOP - TABLE[2]            # 73.3
TABLE_Z = (-RAIL[2], -RAIL[2] - TABLE[1])  # -3 .. -83 when down at the wall
FOLDED_TOP = RAIL_TOP + TABLE[1]           # 153.3: the folded table's top edge
REED = (2.0, 1.0, 1.0)                     # v12: reeded underside, oak strips 2 wide, 1 apart, 1 thick, between the breadboard ends
FOLDED_D = RAIL[2] + TABLE[2] + (0.0 if PLAIN else REED[2]) + 0.3   # v15 flip-top: about 13 off the breast (was 6)
OPEN_Z = (TABLE_Z[0], TABLE_Z[1] - FLIP["leaf"][1])   # -10.3 .. -170.3: the table open, 160 long, out from the breast
OPEN_LEN = OPEN_Z[0] - OPEN_Z[1]                 # 160
GATE_LEG_H = TABLE_TOP - FLIP["leaf"][2]          # 73.3: the gate's legs, floor to the half's underside
HEBGO = (58.0, 22.0)                       # Häfele Hebgo 287.43.428: arm 580, height 220; 500 kg a pair
HEBGO_X = (TABLE_CX - 40.0, TABLE_CX + 40.0)   # 80 apart (Häfele: up to 800 between brackets)
LEG_H = 71.0                               # v13.6: tapered oak legs, 71 long (the standard 710 dining leg), on M8 hanger bolts into brass inserts
LEG = (4.5, 3.0)                           # v13.6: oak legs, 4.5 square at the top tapering to 3 at the foot (two inside faces)
LEG_BOLT = 1.5                             # the M8 hanger bolt's exposed length when the leg is off
LEAF = (60.0, 80.0, 2.7)                   # the extra leaf for six and eight, on four more legs
# v13.6, client: "include legs on the table build ... store them as a part of the table's build, maybe in a box". The leaf
# carries all eight legs: a slim oak frame under it (it also stiffens the leaf), the legs lying side by side inside it, each
# with its bolt in a hole in the frame's end rail and its foot in a sprung clip. Nothing extra on the folded table or in the room.
LEAF_FRAME = dict(inset_x=3.0, inset_z=1.5, t=1.8, h=5.5)   # set in from the leaf's 60 and 80 edges; rails 1.8 thick, 5.5 deep
LEAF_FRAME_OUT = (LEAF[0] - 2 * LEAF_FRAME["inset_x"], LEAF[1] - 2 * LEAF_FRAME["inset_z"])          # 54 × 77
LEAF_FRAME_IN = (LEAF_FRAME_OUT[0] - 2 * LEAF_FRAME["t"], LEAF_FRAME_OUT[1] - 2 * LEAF_FRAME["t"])  # 50.4 × 73.4
LEG_CLIP = (4.21, 5.6, 1.27)                # RS PRO 45 mm steel spring clip: 42.1 × 56 × 12.7 mm (grips the leg near its foot)
LEG_CLIP_FROM_FOOT = 8.0                    # the leg is about 3.2 square there: diagonal 4.5, the clip's size
LEG_PITCH = 6.0                             # the stored legs' centres across the frame
LEG_STORE_W = 7 * LEG_PITCH + LEG_CLIP[1]   # 47.6 across, clips included
LEAF_LEG_IN = (7.5, 6.5)                    # the leaf's own four inserts: in from its 60 and 80 edges, clear inside the frame's corners
LEAF_KIT_KG = None                          # computed in fit.py
CHAIR = (44.0, 51.0, 77.0, 46.0)           # W, D, H, seat height. v31: IKEA FRÖSVI in solid beech, slatted seat, no cushion (v15–v30: 43 × 49 × 78, seat 48: TERJE, and FRÖSVI's padded version)
DINE_W = 60.0                              # table edge per diner (UK guide)
CLEAR_MIN, CLEAR_OK, CLEAR_WALK = 60.0, 75.0, 100.0   # table edge to wall: tight minimum, aim, walk behind
FREE_Z = (-75.0, -155.0)                   # v13.1: where the table stands for six or eight: 75 off the breast (the figure to aim for)
SIX_LEAF = True                            # v13.1: six use the leaf too (170 × 80): 85 of edge each on the long sides, 80 at each end
SIX_X = (232.0, 402.0)                     # clear of the sub's box (x 217–252) on the breast side, 65 to the west wall
SIX_CHAIR_BACK = CHAIR[1]                   # breast-side chairs at the table's edge: their backs reach 49 of the 60 cm to the breast
EIGHT_X = SIX_X                            # eight: the same 170 × 80, three a side

FRAMES_Y = 165.0                           # two framed LPs on the breast above the folded table

# ---------------------------------------------------------------- lighting and viewing
PEND_X = ALC_W / 2                         # the existing rose: straight out from the TV unit...
PEND_Z = (BASE_FRONT_Z + SOFA_FRONT_Z) / 2 # ...halfway to the sofa: -106
BAR = (84.0, 16.0, 22.4)                   # Wolston-style bar: length, depth, drop
BAR2_X, BAR2_Z = 412.0, -143.0             # v14: the existing pendant point, from the client's photo (20 Oct): about 55 out from the west wall,
                                           # a quarter of the way along the 2 m shelf from its stair end (was 433, -80, assumed)
EYES_FROM_WINDOW = 70.0
EYE_HEIGHT = (105.0, 112.0)
SCREEN_FROM_WINDOW = ROOM_D - (ALC_D - TV_PANEL_Z[0])   # 335
VIEW_DIST = SCREEN_FROM_WINDOW - EYES_FROM_WINDOW        # 265
CHAISE_EYES_Z = CHAISE_END_Z - 60.0        # sitting up at the chaise's end
SOCKET = dict(x=0.0, z=-22.0, y=30.0)      # on the east wall, just in front of bay 1
# v23, client: "switchs are 1 in the corner in front of the left xbox game drawer. 2 behind the sofas shorter side slightly to the left
# and down of the PC. and 2 behind the plant shelf when its in the corner near the lamp not on chimney": the room's sockets (switched,
# drawn at socket height, 30 up). The first is SOCKET above (one, which the plan swaps for a double); the other two are doubles.
SOCKET2 = dict(x=0.0, z=-140.0, y=30.0)    # behind the sofa's return, a little nearer the media wall than the PC (-134 .. -179): the rears, the PC
SOCKET3 = dict(x=WINDOW_X[1] + 44.0, z=WINDOW_Z, y=30.0)   # 352: on the window wall behind the plant stand (layout A), near the lamp
SOCKETS = [dict(SOCKET, gang=1, wall="x", name="in the corner in front of the left Xbox game drawer"),
           dict(SOCKET2, gang=2, wall="x", name="behind the sofa's short side, left of and below the PC"),
           dict(SOCKET3, gang=2, wall="z", name="behind the plant stand in the window corner, near the lamp")]


def summary():
    import math
    ang = 2 * math.degrees(math.atan(TV_W / 2 / VIEW_DIST))
    up = [math.degrees(math.atan((TV_CENTRE - e) / VIEW_DIST)) for e in EYE_HEIGHT]
    sofa_mid = (SOFA_X[0] + SOFA_X[1]) / 2
    off = math.degrees(math.atan((sofa_mid - TV_CX) / VIEW_DIST))
    chaise_dist = TV_PANEL_Z[0] - CHAISE_EYES_Z
    return {
        "tv_shift": TV_SHIFT, "tv_gap": TV_GAP, "uprights": (UP_L, UP_R), "tv_x": TV_X, "rz": RZ, "rz_w": RZ_W,
        "tv_bottom": TV_BOTTOM, "tv_top": TV_TOP, "tv_centre": TV_CENTRE, "upright_len": UPRIGHT_LEN,
        "base_depth": BASE_D, "base_proud": BASE_PROUD, "view_dist": VIEW_DIST, "view_angle": ang,
        "tv_above_eye_deg": up, "sofa_mid_off_axis_deg": off, "chaise_dist": chaise_dist,
        "lid_top_open": LID_TOP_OPEN, "sx_top": SX_TOP, "sx_sides": (RZ_W - FAN_STAND[0]) / 2,
        "sx_above": HIGH_UNDER - SX_TOP, "pend_z": PEND_Z, "lowest_shade": CEIL - BAR[2],
        "ledge_lp_top": LEDGE_LP_TOP, "above_ledge_lps": HIGH_UNDER - LEDGE_LP_TOP, "to_ceiling": CEIL - HIGH_TOP,
        "table_x": TABLE_X, "folded_top": FOLDED_TOP, "walk_base_to_chaise": BASE_FRONT_Z - CHAISE_END_Z,
        "pc_top": PC_SHELF_TOP + PC_CASE[1], "pc_shelf_under": PC_SHELF_TOP - PC_SHELF_T,
    }


if __name__ == "__main__":
    for k, v in summary().items():
        print(f"{k:22} {v}")


# ---------------------------------------------------------------- v14: the stairs wall, and the dining table's second site
# Client, 20 Oct, with two photos: "what if the table was on the wall going up the stairs under my shelf which is 2m long ...
# all other furniture can move". The west wall north of the stair box: their black floating shelf (2 m) high on it, the dresser,
# the three-headed floor lamp and the record crate below. Scaled from the photo by the shelf's 2 m (about 4.5 px a cm on the wall):
# the shelf starts about 41 cm past the stair box and stops about 16 cm short of the window corner, top about 200.
STAIRS_WALL_Z = (ALC_D - STAIR_D, WINDOW_Z)        # -41 .. -309: the stair box's face to the window wall, 268 long
# v16, client: "the small alcove in that exists on the edge of that wall, it's like 20x20 out, covers pipes, its hollow": the pipe boxing in
# the window corner (sketch: 230 along this wall, 220 out), floor to ceiling. The shelf can't run into it, so it stops 2 short of it, 200 long;
# its top is put at 196 (the photo gave about 200) so the IKEA OBEGRÄNSAD panel (36 tall) stands on it under the 235 ceiling.
PIPE_BOX = dict(x=(ROOM_W - NW_BOX[1], ROOM_W), z=(WINDOW_Z, WINDOW_Z + NW_BOX[0]), hollow=True)   # x 445 .. 467, z -309 .. -286
SHELF_B = dict(z=(PIPE_BOX["z"][1] + 202.0, PIPE_BOX["z"][1] + 2.0), top=196.0, t=5.0, d=25.0)   # -84 .. -284
DINING_SITES = {"breast": "On the chimney breast", "stairs": "Under the shelf, by the stairs"}
DINING_SITE = "stairs"                              # v16, client: "table by the stairs should be default view now": the plan's default
TABLE_B_CZ = -180.0                                # the table's centre along the stairs wall: 84 to the stair box, 74 to the window
TABLE_B_Z = (TABLE_B_CZ + TABLE[0] / 2, TABLE_B_CZ - TABLE[0] / 2)    # -125 .. -235
TABLE_B_X = (ROOM_W - RAIL[2] - TABLE[1], ROOM_W - RAIL[2])          # the inner top, down
TABLE_B_OPEN_X = (ROOM_W + OPEN_Z[1], ROOM_W + OPEN_Z[0])            # v15: 296.7 .. 456.7 open, out from the stairs wall
FLOOR_LAMP = dict(h=165.0, base=28.0, heads=3)      # the client's three-headed floor lamp (keeps; it can move): drawn, not measured
FLOOR_LAMP_SPOTS = {"corner": ("By the window, west corner", (ROOM_W - 62.0, WINDOW_Z + 34.0)),   # v16: clear of the pipe box and the plant
                    "sofa": ("At the sofa's west end", (SOFA_X[1] + 20.0, SOFA_BACK_Z + 20.0)),
                    "breast": ("Beside the chimney breast", (BREAST_X[1] + 22.0, -22.0))}


# ---------------------------------------------------------------- v15 (21 Oct): the client's notes on the room as it really is
# "my sofa goes to around 40cm before the end of the window ... it has 2 seats then corner. it is also blue corduroy and you can remove
# the white cushion" -> SOFA_W above; the long side is an arm, two seats and the corner seat, then the return along the side wall.
SOFA_SEATS = 2                               # seat cushions on the long side, west of the corner seat
SOFA_CORD = ("#34507f", "#40609a", "#283f68", "#1f3354")   # blue corduroy: face, top, side, the cord's channels
SOFA_CUSHION = False                         # the white/grey cushion is gone
SOFA_OTTOMAN = 20.0                          # v17, client: "the end sofa seat closest to the tv ... has the seat cushion wrap around the back
                                             # at the end there and towards the wall making that ottoman 'feet out' type space. it then just has
                                             # no end open sofa about 20cm after that": the last 20 cm of the return has no back

# "i'd like the media wall drawers for vinyl to be for vinyl large only": one trough the tray's full width, the LPs centred in it with
# finger room either side to flip with both hands (LP 31.4 in 52.1 inside: 10.3 each side); no divider, no singles.
TRAY_LP_ONLY = True

# v16, client: "vinyl drawer adjusted but lots of empty space in that drawer now ... a better use of space for something else. i want the
# ideal media wall now you have the specs and info". Bay 3 splits in two with a 12 mm ply divider: on the right, under the turntable,
# the LP column: two snug face-out LP crates (the 33 cm trough record shops use: 31.4 sleeves with a little play, flipped by their top
# edges); on the left, a slim column of three drawers: two face-out game drawers (DVD-size cases, 13.5 wide) and a drawer for the pads
# and remotes with a charging lead. Every drawer 400 mm deep on 12.7 mm side runners.
RUN = 1.27                                   # side-mount runner clearance each side
B3_IN = (BAYS[2][0] + 1.8, BAYS[2][1] - 1.8)               # 124.8 .. 181.2 inside the 18 mm ply carcass
B3_DIV = (B3_IN[0] + 17.8, B3_IN[0] + 19.0)                # 142.6 .. 143.8: the 12 mm ply divider
REC_BOX_X = (B3_DIV[1] + RUN, B3_IN[1] - RUN)              # 145.07 .. 179.93: the LP crates, 34.86 wide
TRAY_BOX = (REC_BOX_X[1] - REC_BOX_X[0], 40.0)
TRAY_INSIDE = TRAY_BOX[0] - 2 * 0.9         # 33.06 between the 9 mm sides: 0.8 play each side of a 31.4 sleeve
SLIM_BOX_X = (B3_IN[0] + RUN, B3_DIV[0] - RUN)             # 126.07 .. 141.33: the slim drawers, 15.26 wide
SLIM_SIDE = 0.6                                            # 6 mm birch-ply sides and back
SLIM_INSIDE = SLIM_BOX_X[1] - SLIM_BOX_X[0] - 2 * SLIM_SIDE   # 14.06
GAME_CASE = (13.5, 19.0, 1.4)                # DVD-size game case (PS2, Xbox 360, PS3): W, H, T; Xbox One's are 17 tall
PAD = (16.0, 10.6, 6.6)                      # DualSense, the larger pad: W, D, H (Xbox Series pad 15.3 x 10.4 x 6.1)
SLIM_DRAWERS = [dict(yb=2.3, kind="games", n=22), dict(yb=25.1, kind="games", n=22), dict(yb=47.9, kind="pads", n=4)]
SLIM_GAMES = sum(d["n"] for d in SLIM_DRAWERS if d["kind"] == "games")    # 44
FACE_STILE = (B3_DIV[0] - 0.4, B3_DIV[1] + 0.4)            # the face frame's stile over the divider: 142.2 .. 144.2

# v16: with the table by the stairs (the default), the chimney breast beside the turntable takes a "now playing" ledge: a 7 cm oak ledge
# for the sleeve of what's on and the next two, under the two framed LPs
NOW_LEDGE = dict(x=(BREAST_X[0] + 6.0, BREAST_X[1] - 6.0), top=104.0, d=7.0, t=2.4, lip=1.5, n=3)

# "i'd like the bar lights to run in the other direction ie tv to window on both fixtures": both bars turn 90°, so they run along z
# (from the media wall towards the window); their heads are spaced along the bar the same 21 cm apart.
BAR_AXIS = "z"
# "make these lights also smart rgb because they will be": the Wolston bar takes 4 × E14 (SES) bulbs, 6 W max (Dunelm). Smart colour E14
# bulbs: WiZ Colour P45 E14, 4.9 W, 4.5 × 10.1 cm (Philips/WiZ), or the shorter Philips Hue E14 lustre, 5.1 W, 4.5 × 7.7 cm. Smart bulbs
# need full power, so the two wall dimmers are dropped: the wall switches stay on and the app (or a smart button) sets level and colour.
SMART_BARS = True
BULB_E14 = {"wiz": ("WiZ Colour P45 E14", 4.9, (4.5, 10.1)), "hue": ("Philips Hue White and Colour E14 lustre", 5.1, (4.5, 7.7))}
BAR_MAX_W = 6.0
# the lamp: "bright red, it has rgb lights mainly stay on green on top then pink then purple going down"
LAMP_BODY = "#c8102e"
LAMP_HEADS_RGB = ("#3ddc84", "#ff5fb0", "#8a4dff")   # top, middle, bottom

# "i want it to look better especially on the left wall side": the ledge and the PC shelf become one oak run on one line (top 155.4,
# 4 thick all along), its front edge sweeping out from the 7 cm LP ledge to the 28 cm PC shelf over 16 cm, with a 5 cm radius on the
# end, like the table's corners; a warm LED strip in a groove under the front edge washes the wall below it (on the uprights' driver).
SIDE_RUN_Z = (WRAP_Z[0], PC_SHELF_Z[1])     # 8 .. -212: 220 long, one board line (two boards, scarf-jointed at the sweep)
SIDE_RUN_T = PC_SHELF_T                     # 4 all along (the ledge part was 2.4)
SIDE_SWEEP = (PC_SHELF_Z[0] + 12.0, PC_SHELF_Z[0] - 2.0)   # -118 .. -132: the front edge eases from 7 out to 28, under the last LP
SIDE_END_R = 5.0
SIDE_GLOW = True                            # LED strip under the run's front edge


def side_run_depth(z):
    """The run's depth off the wall at z (cm): 7 along the LPs, an S-curve out to 28 under the PC."""
    import math
    a, b = SIDE_SWEEP
    if z >= a:
        return WRAP_D
    if z <= b:
        return PC_SHELF_D
    t = (a - z) / (a - b)
    return WRAP_D + (PC_SHELF_D - WRAP_D) * (0.5 - 0.5 * math.cos(math.pi * t))


# soft furnishings: "make it soft grey carpet and add a nice design rug that fits", "add my curtains also which ill add a photo of"
CARPET_COL = "#8f9194"                      # soft cool grey
RUG = dict(x=(100.0, 330.0), z=(-198.0, -38.0), border=8.0)   # 230 × 160: from the return's seat to past the breast, sofa front to 30 short of the base
RUG_COLS = ("#efe7d8", "#c7643a", "#d9a441", "#2f4a6e", "#7a8a6a")   # cream ground, rust, ochre, deep blue (the sofa), sage
CURTAIN = dict(rail_y=CEIL - 7.0, drop_to=1.5, stack=44.0, ext=30.0, col="#b9a47f", folds=11, pole=2.8, finial=7.0, pole_col="#a9794b",
               z=ALC_D - ROOM_D + 11.0)          # v17: the panels hang 11 in front of the wall, clear of the sill's nose and the radiator
# v17, client: "curtains should not render going through the window sill, i also have deep window sills that allow for lots of plants".
WINDOW_Y = (88.0, 212.0)                    # the window's opening, sill to head
WINDOW_REVEAL = 22.0                        # the frame sits back in the wall: a deep reveal
SILL = dict(nose=3.0, t=3.0, y=WINDOW_Y[0]) # a white sill across the reveal, 3 proud of the wall, plants along it
                                            # the client's curtains (photo 20 Oct, inputs/photo_room_curtains_evening.jpg; "hessian curtains
                                            # from dunelm with a wood rail"): natural hessian, pencil pleat, to the floor (Dunelm's pencil-pleat
                                            # drops run to 228, header 3"), on a 28 mm wooden pole with rings and ball finials (Dunelm sells them
                                            # 120-360 long, rings included, finials up to 8 more), running 30 past the window each side: a 300 pole
# shelf B (the 2 m shelf on the stairs wall): "make the hanging plant on the wall shelf actually hang and add my small laser from the middle.
# on the left of that shelf is my ikea light box"
# v16, client: "lightbox is also black not white. it makes black and white print basic images in blocks like pharmacy LED ads": the IKEA
# OBEGRÄNSAD LED wall lamp (black, 52 x 36 x 6, a 16 x 16 grid of white LEDs, five programmes), standing landscape at the left end
LIGHTBOX = dict(z=(SHELF_B["z"][0] - 2.0, SHELF_B["z"][0] - 54.0), h=36.0, d=6.0, grid=16, name="IKEA OBEGRÄNSAD")
LASER = dict(z=sum(SHELF_B["z"]) / 2, size=(9.0, 6.0, 9.0), on=False)   # v16: "the laser lights should not be on, i was just saying that it is on that shelf"
PLANT_B = dict(z=SHELF_B["z"][1] + 9.0, pot=14.0, trail=(55.0, 110.0), strands=7)   # v16: "move plant to edge of the shelf": the window end
# "either add my hat there or give it a wallstand or something to display it": an oak hat peg on the stairs wall by the lamp
HAT_PEG = None                                       # v16: "youve put a random hat on the wall, ill resend the picture": off until the photo
# v16, the client's photo ("Hat"): the hats hang on the red lamp: a black graduation cap on the pole's top, a navy baseball cap with a poem
# printed under its peak hung on the pole below the top head
HATS = dict(board=24.0, cap_y=FLOOR_LAMP["h"] - 26.0, cap_col="#1f2a44")

# the heads along each bar (offset along the bar from its centre, + towards the media wall / door), shade colour, stem colour, aim
SAGE, BLUE, MUSTARD, PINK = ("#a9c7ab", "#8db59c"), ("#a7d0d8", "#7fbfc8"), ("#e8b53f", "#dca52f"), ("#e79c95", "#d9877f")
BAR1_HEADS = [(31.5, *SAGE, (40.0, 212.0, 30.0)),                 # (v15 aims, kept for reference; v17 replaces them just below)
              (10.5, *BLUE, (TV_CX, 172.0, 34.0)),
              (-10.5, *PINK, (160.0, 95.0, 8.0)),
              (-31.5, *MUSTARD, (148.0, 45.0, -169.0))]
# v17, client: "make all the ceilings lamps just face downward and give the room a general average lighting on the whole room as the default":
# every head straight down, spread a little along the bar, so the pools overlap into an even light
HEAD_SPREAD = 1.6
BAR1_HEADS = [(off, col, stem, (PEND_X, 0.0, PEND_Z + off * HEAD_SPREAD)) for off, col, stem, _ in BAR1_HEADS]


def bar_head_xz(bx, bz, off):
    """Where a head hangs: bars run along z since v15 (TV to window), along x before."""
    return (bx, bz + off) if BAR_AXIS == "z" else (bx + off, bz)


# ---------------------------------------------------------------- v18 (20 Oct): the client's plant stand and their 2 x 2 record shelf
# "ive bought a plant shelf something very similar to this image" (a bamboo stand, two columns, four tiers, LED grow bars under the top two)
# "and i could keep the vinyl shelf i have ... 4 trays in 2x2 square wood shelf". v18.1: both now from the listings the client sent.
PLANT_STAND = dict(w=98.0, d=29.5, h=158.0, cols=(33.5, 31.0, 33.5), post=2.4, col="#8a5a36",   # v18.1: the client's listing, 98 x 29.5 x 158
                   tower=(3.0, 41.0, 79.0, 117.0, 155.0), middle=(22.0, 98.0), lights=())       # five tiers each side, two in the open middle
# v18.1: the "vinyl stand" from the client's listing: 70 x 32 x 78, a black steel frame and rustic wood; two face-out bays on top
# (32.3 each, split by a wooden divider, LPs leaning on a sloped back), a bottom shelf with four wire dividers 19.5 tall
RECORD_SHELF = dict(w=70.0, d=32.0, h=78.0, bay=32.3, shelf_y=46.0, lip=10.0, frame_top=63.0, bottom_y=8.0, wire_h=19.5, wires=4,
                    col="#7a5232", steel="#1c1c1e", lps_top=50, lps_bottom=50)
# where each goes, by layout: (centre x, centre z, facing: +1 = faces into the room from the window wall, -1 = from the breast)
_BREAST_CX = (BREAST_X[0] + BREAST_X[1]) / 2
PLANT_LAYOUTS = {
    "corner": dict(name="Plants in the window corner, vinyl stand on the breast", plants=(391.5, WINDOW_Z + 1.0 + PLANT_STAND["d"] / 2, 1),
                   records=(_BREAST_CX, -1.0 - RECORD_SHELF["d"] / 2, -1)),
    "breast": dict(name="Vinyl stand in the window corner, plants on the breast", plants=(_BREAST_CX, -1.0 - PLANT_STAND["d"] / 2, -1),
                   records=(383.5, WINDOW_Z + 1.0 + RECORD_SHELF["d"] / 2, 1)),
}
PLANT_LAYOUT = "corner"          # the recommendation: daylight for the plants, the records beside the turntable
LAMP_DEFAULT = "sofa"            # v18: the window corner is taken either way, so the red lamp starts at the sofa's west end

# ---------------------------------------------------------------- v19 (20 Oct): LP totals and storing the dining chairs
WALL_LPS = 2 * TRAY_LPS + LEDGE_LPS + WRAP_LPS + NOW_LEDGE["n"]   # 191 in the media wall, all face-out
STAND_LPS = RECORD_SHELF["lps_top"] + RECORD_SHELF["lps_bottom"]  # 100 in the vinyl stand (either layout): 50 face-out, 50 spine-up
ALL_LPS = WALL_LPS + STAND_LPS                                    # 291
# The client: "chair storage can be added somewhere also for the dining chairs, optional not essential unless easily done to the original
# table without many changes". The table isn't changed. The chairs are IKEA FRÖSVI (TERJE's UK successor, the same 43 x 49 x 78), which
# fold flat and have a hole in the back made to hang on a hook; folded they're about 43 W x 9 D x 89 H (their flat-pack size).
CHAIR_FOLDED = (44.0, 9.0, 89.0)            # v31: the beech FRÖSVI's flat pack, 44 × 9 × 89 (IKEA publishes no folded size: measure one)
HOOK = (3.0, 20.0, 20.0)                     # v20: a 200 x 200 mm steel storage hook (Smith & Locke, Screwfix 8882J, 60 kg): two chairs on each
_hook_top = SHELF_B["top"] - SHELF_B["t"]    # the shelf's underside, 191
CHAIR_STORE = dict(
    # the window end of the stairs wall: from the table's end (z -235) to the pipe boxing's face (z -286), two chairs one above the other
    # v20, client: "ideally 6 folding chairs but 4 is fine": two chairs on each hook, one behind the other, so four hang here
    hooks=dict(z=(TABLE_B_Z[1], PIPE_BOX["z"][1]), x=ROOM_W, chairs=4, per_hook=2,
               chair_y=((3.0, 3.0 + CHAIR_FOLDED[2]), (96.0, 96.0 + CHAIR_FOLDED[2])), hook_y=(86.0, 179.0), under_shelf=_hook_top),
    # the stair end: from the shelf's start (z -84, past it the stair's foot has to stay clear) to the table's other end (z -125)
    stair_gap=(SHELF_B["z"][0], TABLE_B_Z[0]),
    # under the stairs, inside the room: the flight rises from z -35 to the door wall at z 39, so it's only about 78 tall there
    owned=(4, 6),                            # four on the wall; a fifth and sixth (for six at the table) in the garage, or under the stairs
    # v20, client: "is it not possible to build the chair storage into the table setup. i want it to be a fully pack away setup": an oak
    # chair cupboard built in beside the table, in the same window-end gap, flush with the pipe boxing's face; the chairs hang inside it on
    # the two hooks, two deep; a door on the table's side closes it. The 31-deep version takes three deep: six chairs.
    cupboard=dict(z=(TABLE_B_Z[1], PIPE_BOX["z"][1]), d=PIPE_BOX["x"][1] - PIPE_BOX["x"][0], d6=31.0, h=SHELF_B["top"] - SHELF_B["t"] - 2.0,
                  t=1.8, door=1.8, back=0.6, plinth=3.0, shelf_y=93.0, lip=3.0, hinge="table"),
    under_stairs=dict(x=STAIR_X, z=(ALC_D - STAIR_D + 6.0, BREAST_D_WEST), h=round((BREAST_D_WEST - (ALC_D - STAIR_D + 6.0)) // STAIR_GOING + 1) * STAIR_RISE),
)


# ---------------------------------------------------------------- v23 (20 Oct): more ways to build the chairs in; the sofa's ottoman
# client: "explore any further ways we can build the chairs into the table build". Two that go with the chair cupboard:
# four folded chairs hung behind the folded top, on a backboard 22 deeper (two side by side, two deep, on two hooks), a 10 cm oak
# upstand under the folded top hiding their feet; and a fold-down oak seat on two folding bench brackets in the 41 gap at the stair end.
BEHIND_TOP = dict(gap=22.0, hook=3.0, upstand=10.0, rail=RAIL[2] + 21.0)
WALL_SEAT = dict(w=38.0, d=33.0, t=2.7, h=46.0, fold=5.0, z=(CHAIR_STORE["stair_gap"][0] - 1.5, CHAIR_STORE["stair_gap"][1] + 1.5))
# client: "the sofa has a ottoman poufe type thing that is the size of a chair on the sofa, its square, blue corduroy matching the sofa"
SOFA_POUF = dict(w=75.0, d=75.0, h=44.0, x=(200.5, 275.5), z=(-195.0, -120.0))   # on the rug beside the coffee table, a footrest


# ---------------------------------------------------------------- v26 (20 Oct): option C, the dining cabinet; v27: the plan, for six
# client (v26): "exploire other table config that looks more tidy and includes the chairs", "assess the max number of seatings you can fit".
# client (v27): "use the cabinet version as our primary table model now and improve on its current design to have a seating of 6, i would
# like the chairs to exist within the same thing the table is built into". One flush oak cabinet under your shelf (the stair's foot stays
# clear), 24 deep like the pipe boxing:
#  - at the stair end, the table bay: a 180 × 90 solid-oak top made of two 90 × 90 halves joined by flip-top hinges (v26's were 112.5 long,
#    for eight). Folded, the halves lie face to face and stand up in the bay (a fold-down table, hinged at its foot on a piano hinge); its
#    oak underside is the bay's front. Lower it onto its folding legs, flip the outer half over onto its own: 180 × 90, out from the wall,
#    three a side in comfort. A drawer under it for the mats; over it, where v26's longer halves stood, a lift-up flap for the cloth.
#  - at the window end, the chair bay behind two doors: the six FRÖSVI folded, four on the floor (two across, two deep) and two on the
#    shelf, with the shelf's front half free for the seat pads and the runner.
_cb_z0, _cb_z1 = SHELF_B["z"]                                   # -84 .. -284: the shelf's length (the stair's foot stays clear)
OPTC = dict(
    # v29, client: "i asked for a full upgrade of the tables design". Two oak sliding doors across the whole front (Häfele Slido Classic
    # 40 IF C, inset, bypassing): shut, it's one tidy run of oak with nothing on show; slide one over the other to open either bay.
    # Hinged doors can't work here: at the stair end there is nowhere for a door to fold back without standing in the first chair.
    # d: the wall to the doors' face (v27: 24, no doors on the table bay); slide: the doors' zone in front of the inside (two 18 mm doors
    # on the double track); inside 19.2, two folded chairs deep (18). The window side's chairs stop at the sofa's arm, so the doors' face
    # can't come further out than this and still seat three in comfort.
    z=(_cb_z0 - 2.0, _cb_z1), d=24.8, slide=5.0, h=SHELF_B["top"] - SHELF_B["t"] - 2.0, t=1.8, t_top=1.9, door=1.8, back=0.6, plinth=3.0, shelf_y=93.0,
    top=(90.0, 92.5, 2.7),                                      # each half: width along the wall, length out from it, thickness (v29: 92.5, so 185 open)
    apron=4.6,                                                  # the frame under each half that the folded legs lie inside
    leg=(6.5, 4.5),                                             # oak legs, 6.5 × 4.5 (the folding brackets want 6.4 at the top)
    drawer_h=16.0,                                              # the drawer under the folded table
    chairs=6,                                                   # v27: six (v26: eight)
    shelf_chairs=2,                                             # v27: two of the six on the shelf, at the back; four on the floor
)
_c = OPTC
OPTC["front"] = ROOM_W - _c["d"]                                # 442.2: the doors' face
OPTC["inner"] = OPTC["front"] + _c["slide"]                     # 447.2: the inside's front line, behind the doors (the hinge rail, the folded table, the drawer)
OPTC["in_d"] = _c["d"] - _c["slide"] - _c["back"]               # 19.2 inside
OPTC["bay_t"] = (_c["z"][0] - _c["t"], _c["z"][0] - _c["t"] - _c["top"][0] - 1.0)          # the table bay inside: 91 wide
OPTC["bay_c"] = (OPTC["bay_t"][1] - _c["t"], _c["z"][1] + _c["t"])                        # the chair bay inside
OPTC["cz"] = (OPTC["bay_t"][0] + OPTC["bay_t"][1]) / 2                                     # the table's centre line
OPTC["tz"] = (OPTC["cz"] + _c["top"][0] / 2, OPTC["cz"] - _c["top"][0] / 2)               # its long sides when open
OPTC["pivot"] = (OPTC["inner"] + _c["apron"], TABLE_TOP - _c["top"][2])                   # the piano hinge: x, height (the top's underside)
OPTC["len"] = 2 * _c["top"][1]                                                              # 180 open
OPTC["tx"] = (OPTC["pivot"][0] - OPTC["len"], OPTC["pivot"][0])                           # open: x 267.6 .. 447.6
OPTC["joint_x"] = OPTC["pivot"][0] - _c["top"][1]
OPTC["folded_top"] = OPTC["pivot"][1] + _c["top"][1]                                       # 163.3: the halves standing up
OPTC["flap"] = (OPTC["folded_top"] + 1.0 + _c["t"], _c["h"] - _c["t_top"])               # the linen shelf over the folded table (its floor's top face, the top's underside)
OPTC["stack"] = 2 * _c["apron"] + 2 * _c["top"][2] + 0.3                                   # 14.9 deep folded
OPTC["leg_h"] = TABLE_TOP - _c["top"][2] - _c["apron"]                                     # 68.7: floor to the apron's underside
# v29: the two sliding doors. A (the stair end) runs on the front track, B (the window end) on the back one; they overlap 3 in the middle.
# Shut: A over the table bay, B over the chair bay. The table: A slides over B. The chairs: B slides behind A.
_lin = _c["z"][0] - _c["z"][1] - 2 * _c["t"]                    # 194.4 between the ends
OPTC["door_w"] = (_lin + 3.0) / 2                               # 98.7
OPTC["door_h"] = _c["h"] - _c["t_top"] - _c["plinth"] - 0.8    # 183.3: 5 mm under the top track, 3 over the bottom guide
_za, _zb = _c["z"][0] - _c["t"], _c["z"][1] + _c["t"]          # the inside's ends: -87.8, -282.2
OPTC["doors"] = {"A": dict(track="front", shut=(_za, _za - OPTC["door_w"]), slid=(_zb + OPTC["door_w"], _zb)),
                 "B": dict(track="back", shut=(_zb + OPTC["door_w"], _zb), slid=(_za, _za - OPTC["door_w"]))}
OPTC["door_x"] = {"front": (OPTC["front"], OPTC["front"] + _c["door"]), "back": (OPTC["front"] + _c["door"] + 0.6, OPTC["front"] + 2 * _c["door"] + 0.6)}
OPTC["open_t"] = (_za, _zb + OPTC["door_w"])                    # the table bay's opening with A slid away: -87.8 .. -183.5
OPTC["open_c"] = (_za - OPTC["door_w"], _zb)                    # the chair bay's opening with B slid behind A: -186.5 .. -282.2
OPTC["chair_z"] = [round((OPTC["open_c"][0] + OPTC["open_c"][1]) / 2 + s * (CHAIR_FOLDED[0] / 2 + 1.0), 2) for s in (1, -1)]   # two across, centred in that opening
OPTC["door_kg"] = OPTC["door_w"] * OPTC["door_h"] * _c["door"] * 0.70 / 1000      # oak-faced ply about 700 kg/m³
del _c, _cb_z0, _cb_z1, _lin, _za, _zb
DINE_SQUEEZE = 55.0                                             # table edge per diner at a squeeze (UK guide: 60 to aim for)
DINE_COMFORT = 58.0                                             # v27: near the guide's 60: what we call "in comfort" here
CHAIR_TUCK = 8.0                                                # chairs pushed 8 under the edge: their backs 41 behind it (as for A and B)
# Legs and seats. The inner half's legs stand near the joint, 32 in from each side, so knees miss them; the outer half's pair in the far
# end's corners. Seats: chairs centred 16.5 out from the edge (49 deep, tucked 8), facing the table, spread evenly along each side.
_o = OPTC
# v27: each leg stands inside its apron, against the end rail (the rails are 2 thick, 3 in from the ends and 4 in from the sides):
# its centre 3 + 2 + 6.5 / 2 = 8.25 from the half's end; the outer pair in the corners (8.25 in from the sides), the inner pair 32 in.
OPTC["leg_in"] = 3.0 + 2.0 + _o["leg"][0] / 2
OPTC["legs"] = [(_o["joint_x"] + OPTC["leg_in"], _o["cz"] + s * 13.0) for s in (1, -1)] + \
               [(_o["tx"][0] + OPTC["leg_in"], _o["cz"] + s * (_o["top"][0] / 2 - 4.0 - 2.0 - _o["leg"][1] / 2)) for s in (1, -1)]
_sz, _wz = _o["tz"][0] + CHAIR[1] / 2 - CHAIR_TUCK, _o["tz"][1] - CHAIR[1] / 2 + CHAIR_TUCK
_sl, _wl = _o["front"] - _o["tx"][0], _o["front"] - max(_o["tx"][0], SOFA_X[1])
_stair = lambda n: [round(_o["front"] - _sl + _sl / n * (i + 0.5), 1) for i in range(n)]
_window = lambda n: [round(_o["front"] - _wl + _wl / n * (i + 0.5), 1) for i in range(n)]
OPTC["seats"] = {   # (x, z, the way the chair faces: "n" ... as room3d.js reads it: the chair's back away from the table)
    "four": [(x, _sz, "n") for x in _stair(2)] + [(x, _wz, "w") for x in _window(2)],
    "six": [(x, _sz, "n") for x in _stair(3)] + [(x, _wz, "w") for x in _window(3)],
}
del _o, _sz, _wz, _sl, _wl, _stair, _window


# ---------------------------------------------------------------- v30: the compact dining cabinet (the plan); OPTC above is the alternative
# client: "is there anyway you can optimise the dining cabinet build to fit the chairs in a better way so the cabinet doesnt have to be
# so big", then "show me both versions". The same table and the same six FRÖSVI chairs, packed tighter: four in a bay one chair wide
# (two deep on its floor, two deep on its shelf) and two lying on their sides in the table bay's base, under the folded table, where the
# drawer was. Two carcasses screwed side by side: the table box at the stair end (where the table always was, so the seats don't move)
# and the chair box beside it. Sliding doors would each need a door's width to park in, so these are hinged: inset, each on a full-height
# piano hinge whose knuckle sits on the front, so it opens 180° and lies back flat. The table door swings towards the window over the
# chair door and the bare wall beyond it; the chair door swings towards the stairs over the table door. The six seat pads hang on the
# table door's back, so the folded table stands 4 back from it. 54 cm shorter than the sliding cabinet, 1.8 shallower; 56 cm of wall comes back by the
# pipe boxing.
# v33, client: "I'd also like these chairs or similar, make adjustments and decisions as required", then the listing's own words: "2PCS
# Wooden Folding Dining Chair with Cushion, Padded Seat, Grey Breathable Linen Fabric, 6.5cm Thick Cushion, 110° Backrest, 168kg Capacity,
# No Assembly ... a generously sized 47×47cm seat ... 90×10×47cm" (Brayden Studio on Wayfair UK). 90 × 10 × 47 is the chair folded: 90
# tall, 10 thick, 47 wide. They're the plan's chairs now, and the cabinet is drawn round them; the FRÖSVI (CHAIR, CHAIR_FOLDED) stays for
# the earlier tables' drawings. The open chair's depth, height and seat height aren't in the listing's words: drawn at a like-for-like
# chair's (Costway 53981642: 61 deep, 78.7 tall, the seat at 44.5).
CHAIR_PADDED = dict(w=47.0, d=61.0, h=78.7, seat_h=44.5, seat=(47.0, 47.0), cushion=6.5, back_deg=110, kg=168,
                    folded=(47.0, 10.0, 90.0))   # W, thick, tall


def _make_cab(table_w=90.0):
    """v33: the compact cabinet built round a table table_w wide: 90 (the plan) or 80 (the more compact version, 10 shorter;
    its base is then too narrow for the two chairs lying on their sides, so four chairs go inside, not six)."""
    _cf_w, _cf_t, _cf_len = CHAIR_PADDED["folded"]   # v33: the grey padded chairs, folded 47 × 10 × 90
    CAB = dict(
        z0=OPTC["z"][0],              # -86: the stair end, where it always was (45 short of the stair box: the stairs' foot stays clear)
        d=23.4,                       # the wall to the doors' faces; v31: 22, flush with the pipe boxing (the FRÖSVI, 9 thick); v33: 23.4, two padded chairs (10) deep
        h=OPTC["h"], t=1.8, t_top=1.8, door=1.8, back=0.6, plinth=3.0,
        gap=0.2,                      # behind the inset doors (a stop), and round them
        hinge_gap=0.3,                # the hinge side's gap: the piano hinge's two leaves sit in it
        bay_t=table_w + 1.0,          # the table box inside: the top (90 in the plan) and 0.5 a side
        bay_c=49.0,                   # the chair box inside: v33, a 47 chair and 1 a side
        shelf_y=94.0,                 # the chair box's shelf (its top face 95.8): v33, a 90 chair under it and over it
        pads=4.0,                     # v31: room for seat pads on the table door's back; v33: the chairs are padded, so it's the cloth bag's hook and some air
        pad=(40.0, 40.0, 3.0),        # v31: Dunelm Esme tie-on seat pads (the beech FRÖSVI's); not needed with the padded chairs
    )
    _k = CAB
    CAB["front"] = ROOM_W - _k["d"]                                  # 444.0: the doors' faces and the carcass's front edges
    CAB["inner"] = CAB["front"] + _k["door"] + _k["gap"]             # 446.0: the inside's front line
    CAB["in_d"] = _k["d"] - _k["door"] - _k["gap"] - _k["back"]      # 20.4 inside
    CAB["z_t"] = (_k["z0"], _k["z0"] - 2 * _k["t"] - _k["bay_t"])     # the table box: -86 .. -180.6
    CAB["z_c"] = (CAB["z_t"][1], CAB["z_t"][1] - 2 * _k["t"] - _k["bay_c"])   # the chair box: -180.6 .. -230.2
    CAB["z"] = (_k["z0"], CAB["z_c"][1])
    CAB["len"] = CAB["z"][0] - CAB["z"][1]                            # 144.2
    CAB["bay_tz"] = (CAB["z_t"][0] - _k["t"], CAB["z_t"][1] + _k["t"])    # the table bay inside: -87.8 .. -178.8 (as the sliding cabinet's)
    CAB["bay_cz"] = (CAB["z_c"][0] - _k["t"], CAB["z_c"][1] + _k["t"])    # the chair bay inside: -182.4 .. -228.4
    CAB["freed"] = CAB["z"][1] - PIPE_BOX["z"][1]                    # 55.8: wall back by the pipe boxing
    CAB["top"] = (table_w, OPTC["top"][1], OPTC["top"][2])            # the same table: two halves 92.5 long, 90 wide (80: v33), 2.7 thick
    CAB["apron"], CAB["leg"], CAB["leg_in"] = OPTC["apron"], OPTC["leg"], OPTC["leg_in"]
    CAB["cz"] = (CAB["bay_tz"][0] + CAB["bay_tz"][1]) / 2             # -133.3: the table's centre line (unchanged)
    CAB["tz"] = (CAB["cz"] + _k["top"][0] / 2, CAB["cz"] - _k["top"][0] / 2)
    CAB["pivot"] = (CAB["inner"] + _k["pads"] + _k["apron"], TABLE_TOP - _k["top"][2])     # the piano hinge under the inner half: 454.6, 73.3
    CAB["len_open"] = 2 * _k["top"][1]                                # 185 open
    CAB["tx"] = (CAB["pivot"][0] - CAB["len_open"], CAB["pivot"][0])
    CAB["joint_x"] = CAB["pivot"][0] - _k["top"][1]
    CAB["folded_top"] = CAB["pivot"][1] + _k["top"][1]                # 165.8
    CAB["stack"] = OPTC["stack"]                                      # 14.9 deep folded
    CAB["rail"] = (CAB["pivot"][1] - 7.0, CAB["pivot"][1])            # the hinge rail: 66.3 .. 73.3
    CAB["rail_x"] = (CAB["inner"] + _k["pads"], ROOM_W - _k["back"])  # v31: its front set back with the folded table's, so the pads hang down past it
    CAB["pad_zone"] = (CAB["rail"][0], _k["h"] - _k["t_top"])         # v31: where the pads hang on the door: 66.3 .. 187.2, three rows of 40
    CAB["linen"] = (CAB["folded_top"] + 1.0 + _k["t"], _k["h"] - _k["t_top"])   # the linen shelf's top face .. the top's underside: 168.6 .. 187.2
    CAB["linen_d"] = CAB["in_d"] - _k["pads"]                         # v31: the linen shelf set back behind the pads too
    CAB["base"] = (_k["plinth"], CAB["rail"][0])                      # under the hinge rail: 3 .. 66.3, two chairs lying on their sides
    CAB["leg_h"] = TABLE_TOP - _k["top"][2] - _k["apron"]             # 68.7
    # the doors, inset between the top and the floor: the table door one piece (two leaves can't fold flat over the chair door: the outer
    # one would end up behind the inner one), on the table box's window end; the chair door on the chair box's stair end
    CAB["door_h"] = _k["h"] - _k["t_top"] - _k["plinth"] - 2 * _k["gap"]                 # 183.8
    CAB["door_t"] = (CAB["bay_tz"][0] - _k["gap"], CAB["bay_tz"][1] + _k["hinge_gap"])   # the table door: z -88.0 .. -178.5, hinged at -178.5
    CAB["door_c"] = (CAB["bay_cz"][0] - _k["hinge_gap"], CAB["bay_cz"][1] + _k["gap"])   # the chair door: z -182.7 .. -228.2, hinged at -182.7
    CAB["door_tw"] = CAB["door_t"][0] - CAB["door_t"][1]              # 90.5
    CAB["door_cw"] = CAB["door_c"][0] - CAB["door_c"][1]              # 45.5
    CAB["knuckle"] = 0.25                                             # the hinge pin's centre in front of the doors' faces
    CAB["door_kg"] = (CAB["door_tw"] * CAB["door_h"] * _k["door"] * 0.70 / 1000, CAB["door_cw"] * CAB["door_h"] * _k["door"] * 0.70 / 1000)
    # open, a door turns 180° about its knuckle and lies back in front of its neighbour: the table door's far end then reaches
    CAB["door_t_open"] = (CAB["door_t"][1] - _k["hinge_gap"], CAB["door_t"][1] - _k["hinge_gap"] - CAB["door_tw"])   # -178.8 .. -269.3
    CAB["door_t_face"] = CAB["front"] - 2 * _k["knuckle"] - _k["door"]                    # its room-side face lying open: x 441.7
    # the six chairs: two lying in the base, four standing in the chair bay, two deep on its floor and two deep on its shelf
    CAB["chairs_base"] = 2 if _k["bay_t"] >= _cf_len + 1.0 else 0   # v33: a folded chair (90 long) lies across the base with 0.5 at each end: the 91 bay, not the 81
    CAB["chair_z"] = (CAB["bay_cz"][0] + CAB["bay_cz"][1]) / 2         # the standing chairs' centre line
    _cf = (_cf_w, _cf_t, _cf_len)
    CAB["chair_x"] = [ROOM_W - _k["back"] - 0.3 - _cf[1] * (j + 1) - 0.3 * j for j in range(2)]   # their room-side faces, back first
    # seats: as for the sliding cabinet, the window side from the sofa's arm (or the table's end) to the doors' faces
    _sz, _wz = CAB["tz"][0] + CHAIR_PADDED["d"] / 2 - CHAIR_TUCK, CAB["tz"][1] - CHAIR_PADDED["d"] / 2 + CHAIR_TUCK
    _sl, _wl = CAB["front"] - CAB["tx"][0], CAB["front"] - max(CAB["tx"][0], SOFA_X[1])
    _stair = lambda n: [round(CAB["front"] - _sl + _sl / n * (i + 0.5), 1) for i in range(n)]
    _window = lambda n: [round(CAB["front"] - _wl + _wl / n * (i + 0.5), 1) for i in range(n)]
    CAB["seats"] = {"four": [(x, _sz, "n") for x in _stair(2)] + [(x, _wz, "w") for x in _window(2)],
                    "six": [(x, _sz, "n") for x in _stair(3)] + [(x, _wz, "w") for x in _window(3)]}
    CAB["legs"] = [(CAB["joint_x"] + CAB["leg_in"], CAB["cz"] + s * 13.0) for s in (1, -1)] + \
                  [(CAB["tx"][0] + CAB["leg_in"], CAB["cz"] + s * (_k["top"][0] / 2 - 4.0 - 2.0 - _k["leg"][1] / 2)) for s in (1, -1)]
    return CAB


CAB = _make_cab(90.0)                 # the plan: 144.2 long, six chairs inside
CAB80 = _make_cab(80.0)               # v33, client: "the compact cabinet is our only choice ... or any upgraded more compact version": 134.2 long, four chairs inside

# ---------------------------------------------------------------- v31 (21 Oct): beside the compact cabinet
# client: "explore what could go next to the dining cabinet in the compact version which is now our primary option". The wall from the
# cabinet's window end to the pipe boxing's face, under your shelf. The open table door lies back over most of it (to door_t_open[1]),
# standing CAB["d"] off the wall, so whatever goes here is no deeper than the cabinet; your trailing plant hangs over its far end.
BESIDE = dict(z=(CAB["z"][1], PIPE_BOX["z"][1]), depth=CAB["d"], door_end=CAB["door_t_open"][1],
              strands=SHELF_B["top"] - SHELF_B["t"] - PLANT_B["trail"][1])           # 81: the longest strands' ends above the floor
BESIDE["len"] = BESIDE["z"][0] - BESIDE["z"][1]                                       # 55.8
BESIDE["mirror"] = dict(w=40.0, h=150.0, t=2.5, y0=30.0)        # IKEA NISSEDAL 40 × 150, black, on the wall 30 up (its top at 180)
BESIDE["dresser"] = dict(w=CAB["bay_c"] + 2 * CAB["t"], d=CAB["d"], h=76.0, t=1.8, shelf=40.0)   # a low open box, the chair box's width,
                                                                 # table height: its top under the longest strands
BESIDE["trolley"] = dict(w=43.2, d=20.0, h=86.5, tiers=(10.0, 34.0, 58.0, 84.0), col="#e9e4da")   # VASAGLE slim trolley, 4 tiers, 20 × 43.2 × 86.5
BESIDE["opts"] = {"clear": dict(name="Left clear (the plan)"), "mirror": dict(name="A tall mirror"),
                  "trolley": dict(name="A slim trolley"), "dresser": dict(name="A low oak shelf")}


# ---------------------------------------------------------------- v27 (20 Oct): your rear speakers, standing behind the sofa
# client: "add my surround speakers to the build that exist standing behind the sofa ill send a photo". The AX5100G's rears
# (90 × 144 × 109 mm, Hisense) on slim floor stands. v27.1, from your photos and your answer ("they are directly behind the sofa
# on the left and right ends"): both stand in the 13 cm gap behind the sofa's long side, one at each end; the speakers sit just
# above the sofa's back (scaled against the 80 cm back in your photo).
REAR_SPK = (9.0, 14.4, 10.9)                   # W, H, D
REAR_STAND = dict(base=(11.0, 11.0, 1.5), pole=2.5, top=96.0)   # a weighted base, a pole, the speaker on a plate at 96
REAR_SPOTS = [(SOFA_X[0] + REAR_STAND["base"][0] / 2, SOFA_BACK_Z - 6.5),    # left: behind the sofa's corner end, in the corner
              (SOFA_X[1] - REAR_STAND["base"][0] / 2, SOFA_BACK_Z - 6.5)]    # right: behind the sofa's window end
