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
TRAY_BOX = (53.9, 40.0)
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
SOFA_BACK_Z = WINDOW_Z + 10.0              # -299: 10 cm off the window wall and radiator
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
CHAIR = (43.0, 49.0, 78.0, 48.0)           # IKEA TERJE folding chair: W, D, H, seat height
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
SOCKET2 = dict(x=0.0, z=-205.0, y=30.0)    # v13.6: an existing socket by the sofa, IF there is one (rears); no new socket


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
SHELF_B = dict(z=(STAIRS_WALL_Z[0] - 52.0, STAIRS_WALL_Z[0] - 252.0), top=200.0, t=5.0, d=25.0)   # -93 .. -293
DINING_SITES = {"breast": "On the chimney breast", "stairs": "Under the shelf, by the stairs"}
DINING_SITE = "breast"                              # the plan's default; both are drawn, checked and costed
TABLE_B_CZ = -180.0                                # the table's centre along the stairs wall: 84 to the stair box, 74 to the window
TABLE_B_Z = (TABLE_B_CZ + TABLE[0] / 2, TABLE_B_CZ - TABLE[0] / 2)    # -125 .. -235
TABLE_B_X = (ROOM_W - RAIL[2] - TABLE[1], ROOM_W - RAIL[2])          # the inner top, down
TABLE_B_OPEN_X = (ROOM_W + OPEN_Z[1], ROOM_W + OPEN_Z[0])            # v15: 296.7 .. 456.7 open, out from the stairs wall
FLOOR_LAMP = dict(h=165.0, base=28.0, heads=3)      # the client's three-headed floor lamp (keeps; it can move): drawn, not measured
FLOOR_LAMP_SPOTS = {"corner": ("By the window, west corner", (ROOM_W - 22.0, WINDOW_Z + 30.0)),
                    "sofa": ("At the sofa's west end", (SOFA_X[1] + 20.0, SOFA_BACK_Z + 20.0)),
                    "breast": ("Beside the chimney breast", (BREAST_X[1] + 22.0, -22.0))}


# ---------------------------------------------------------------- v15 (21 Oct): the client's notes on the room as it really is
# "my sofa goes to around 40cm before the end of the window ... it has 2 seats then corner. it is also blue corduroy and you can remove
# the white cushion" -> SOFA_W above; the long side is an arm, two seats and the corner seat, then the return along the side wall.
SOFA_SEATS = 2                               # seat cushions on the long side, west of the corner seat
SOFA_CORD = ("#34507f", "#40609a", "#283f68", "#1f3354")   # blue corduroy: face, top, side, the cord's channels
SOFA_CUSHION = False                         # the white/grey cushion is gone

# "i'd like the media wall drawers for vinyl to be for vinyl large only": one trough the tray's full width, the LPs centred in it with
# finger room either side to flip with both hands (LP 31.4 in 52.1 inside: 10.3 each side); no divider, no singles.
TRAY_LP_ONLY = True
TRAY_INSIDE = TRAY_BOX[0] - 2 * 0.9         # 52.1 between the 9 mm sides

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
CURTAIN = dict(rail_y=CEIL - 7.0, drop_to=1.5, stack=44.0, ext=30.0, col="#b9a47f", folds=11, pole=2.8, finial=7.0, pole_col="#a9794b")
                                            # the client's curtains (photo 20 Oct, inputs/photo_room_curtains_evening.jpg; "hessian curtains
                                            # from dunelm with a wood rail"): natural hessian, pencil pleat, to the floor (Dunelm's pencil-pleat
                                            # drops run to 228, header 3"), on a 28 mm wooden pole with rings and ball finials (Dunelm sells them
                                            # 120-360 long, rings included, finials up to 8 more), running 30 past the window each side: a 300 pole
# shelf B (the 2 m shelf on the stairs wall): "make the hanging plant on the wall shelf actually hang and add my small laser from the middle.
# on the left of that shelf is my ikea light box"
LIGHTBOX = dict(z=(SHELF_B["z"][0] - 4.0, SHELF_B["z"][0] - 60.0), h=42.0, d=12.0)   # the box in the photo, at the shelf's stair (left) end
LASER = dict(z=sum(SHELF_B["z"]) / 2, size=(9.0, 6.0, 9.0))   # a small star/laser projector in the middle of the shelf
PLANT_B = dict(z=SHELF_B["z"][1] + 48.0, pot=14.0, trail=(55.0, 110.0), strands=7)   # a trailing plant towards the window end, hanging down, clear of the lamp
# "either add my hat there or give it a wallstand or something to display it": an oak hat peg on the stairs wall by the lamp
HAT_PEG = dict(z=STAIRS_WALL_Z[0] - 26.0, y=165.0, d=9.0)   # -67: between the stair box and the shelf's stair end, clear of table B

# the heads along each bar (offset along the bar from its centre, + towards the media wall / door), shade colour, stem colour, aim
SAGE, BLUE, MUSTARD, PINK = ("#a9c7ab", "#8db59c"), ("#a7d0d8", "#7fbfc8"), ("#e8b53f", "#dca52f"), ("#e79c95", "#d9877f")
BAR1_HEADS = [(31.5, *SAGE, (40.0, 212.0, 30.0)),                 # the media-wall end: books and the left of the high shelf
              (10.5, *BLUE, (TV_CX, 172.0, 34.0)),                # the record ledge above the TV
              (-10.5, *PINK, (160.0, 95.0, 8.0)),                 # the turntable and the Series X
              (-31.5, *MUSTARD, (148.0, 45.0, -169.0))]           # the window end: down onto the coffee table


def bar_head_xz(bx, bz, off):
    """Where a head hangs: bars run along z since v15 (TV to window), along x before."""
    return (bx, bz + off) if BAR_AXIS == "z" else (bx + off, bz)
