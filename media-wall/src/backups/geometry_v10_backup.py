"""v10: the one source of truth for the room and the media wall, in cm.

Every number the renders, diagrams, fit-proof tables and plan text use comes from here, so a change
in one place moves everything. Measurements are from the client's hand-measured sketch
(inputs/room_sketch_accurate_mm.png); item sizes are in fit.py with their sources.

Axes used everywhere (matches render.py):
  x  across the media wall, from the east (side) wall, which is on the LEFT when you face the TV
  y  height from the floor
  z  depth: 0 is the face of the chimney breast (the alcove's opening line); +z goes back into the
     alcove (its back wall is at z = ALC_D); -z comes out into the room (the window wall is at z = -ROOM_D + ALC_D)
"""

# ---------------------------------------------------------------- the room (from the sketch)
ROOM_W = 467.0        # east wall to west wall, along the window
ROOM_D = 347.0        # window wall to the alcove's back wall
CEIL = 235.0
SKIRT_H, SKIRT_T = 6.0, 2.0
WINDOW_X = (73.0, 308.0)          # on the north (window) wall, measured from the east wall
RADIATOR_X = (158.0, 295.0)       # under the window, ends 13 cm inside the window's west end
NW_BOX = (23.0, 22.0)             # small box in the window wall's west corner (pipe boxing? to confirm)
WINDOW_Z = ALC_BACK_FROM_WINDOW = None   # set below

ALC_W = 186.0         # alcove: east wall to the chimney breast
ALC_D = 38.0          # breast projection on the alcove side
BREAST_W = 117.5
BREAST_X = (ALC_W, ALC_W + BREAST_W)      # 186 to 303.5
BREAST_D_WEST = 39.0                      # 390 on its west side
RECESS_W = 104.5      # breast to the stair box, about (to confirm)
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
BAY_NAMES = ["Bay 1 · Xbox", "Bay 2 · PlayStation", "Bay 3 · sub"]

# ---------------------------------------------------------------- above the worktop
UP_T, UP_D = 4.5, 30.0                    # oak uprights, against the back wall
TV_W, TV_H, TV_D = 122.2, 70.3, 4.5       # LG OLED55C6 without stand (LG UK/SG spec)
TV_STAND_H = 75.7                          # height with stand
TV_STAND_W, TV_STAND_D = 47.0, 23.0
TV_CLEAR = 2.15                           # each side of the screen, inside the uprights
TV_GAP = TV_W + 2 * TV_CLEAR              # 126.5 between the uprights
SIDE_ZONE = (ALC_W - TV_GAP - 2 * UP_T) / 2   # 25.25 each side
UP_L = (SIDE_ZONE, SIDE_ZONE + UP_T)              # 25.25 .. 29.75
UP_R = (ALC_W - SIDE_ZONE - UP_T, ALC_W - SIDE_ZONE)   # 156.25 .. 160.75
TV_CX = ALC_W / 2                          # 93
TV_X = (TV_CX - TV_W / 2, TV_CX + TV_W / 2)
TV_BOTTOM = WORKTOP + (TV_STAND_H - TV_H)  # 81.4
TV_TOP = TV_BOTTOM + TV_H                  # 151.7
TV_CENTRE = (TV_BOTTOM + TV_TOP) / 2       # 116.55
TV_PANEL_Z = (26.0, 26.0 + TV_D)           # panel 12 cm off the back wall, on its stand
UPRIGHT_LEN = CEIL - WORKTOP               # 159

LEDGE_UNDER, LEDGE_TOP, LEDGE_D, LEDGE_LIP = 153.0, 155.4, 7.0, 1.5
LP = 31.4                                  # 12-inch sleeve
LEDGE_LP_TOP = LEDGE_TOP + 31.1            # leaning 8 degrees: 186.5
SIDE_SHELF_TOP, SIDE_SHELF_T, SIDE_SHELF_D = 156.0, 4.0, 25.0
HIGH_TOP, HIGH_T, HIGH_D = 196.0, 4.0, 30.0
HIGH_UNDER = HIGH_TOP - HIGH_T             # 192

SOUNDBAR = (92.0, 6.0, 9.0)                # W, H, D  (Hisense AX5100G)
SERIES_X = (15.1, 30.1, 15.1)              # W, H, D standing
FAN_STAND = (20.5, 6.5, 20.5)              # assumed fan stand footprint and height (model to confirm)

# ---------------------------------------------------------------- the vinyl cabinet on the chimney breast
CAB_X = (ALC_W, ALC_W + 100.0)             # 186 .. 286, tight to the reveal
CAB_D = 44.0                               # 40 carcass + 2 face frame + 2 cable gap at the back
CAB_FRONT_Z = -CAB_D                       # -44
CAB_TOP = WORKTOP                          # same 76 as the alcove worktop
CAB_BAY_A = (CAB_X[0], CAB_X[0] + 60.0)    # two face-out record trays
CAB_BAY_B = (CAB_X[0] + 60.0, CAB_X[1])    # preamp cubby over a singles drawer
DOOR_CLEAR = BREAST_X[1] - CAB_X[1]        # 17.5 from the cabinet's west end to the breast's corner
DECK = (45.2, 14.2, 35.2)                  # Audio-Technica AT-LP120XUSB, worst case (W, H, D)
DECK_X = (CAB_X[1] - 2.5 - DECK[0], CAB_X[1] - 2.5)
BROWSER = (44.0, 24.0)                     # W, D on the cabinet top, ~50 LPs face-out
BROWSER_X = (CAB_X[0] + 3.0, CAB_X[0] + 3.0 + BROWSER[0])
LID_CLEAR_TO = 130.0                       # keep the breast clear up to here for the deck's lid

# ---------------------------------------------------------------- record trays (unchanged design, now in bay A)
TRAY_BOX = (53.9, 40.0)
TRAY_LOWER = (2.3, 3.5, 34.4)              # box underside, base top, sleeve tops
TRAY_UPPER = (37.0, 38.2, 69.1)
TRAY_TOP_PANEL = 71.2
TRAY_LPS, TRAY_SINGLES = 90, 120
BROWSER_LPS, LEDGE_LPS = 50, 4
BAYB_SINGLES = 110

# ---------------------------------------------------------------- lighting and viewing
PEND_X = ALC_W                             # the existing rose: in line with the breast's corner...
PEND_Z = WINDOW_Z + 173.5                  # ...and 173.5 from the window wall: -135.5
BAR = (84.0, 16.0, 22.4)                   # Wolston-style bar: length, depth, drop
SOFA = (200.0, 95.0)                       # assumed; against the window wall, 10 cm off the radiator
SOFA_X = (2.0, 2.0 + SOFA[0])
EYES_FROM_WINDOW = 70.0
EYE_HEIGHT = (105.0, 112.0)
SCREEN_FROM_WINDOW = ROOM_D - (ALC_D - TV_PANEL_Z[0])   # 335
VIEW_DIST = SCREEN_FROM_WINDOW - EYES_FROM_WINDOW        # 265
SOCKET = dict(x=0.0, z=-22.0, y=30.0)      # on the east wall, just in front of bay 1
PC_SHELF_Z = (-110.0, -175.0)              # along the east wall (moved 20 cm towards the alcove to clear the sofa)


def summary():
    import math
    ang = 2 * math.degrees(math.atan(TV_W / 2 / VIEW_DIST))
    up = [math.degrees(math.atan((TV_CENTRE - e) / VIEW_DIST)) for e in EYE_HEIGHT]
    return {
        "side_zone": SIDE_ZONE, "tv_gap": TV_GAP, "uprights": (UP_L, UP_R), "tv_x": TV_X,
        "tv_bottom": TV_BOTTOM, "tv_top": TV_TOP, "tv_centre": TV_CENTRE, "upright_len": UPRIGHT_LEN,
        "base_depth": BASE_D, "base_proud": BASE_PROUD, "view_dist": VIEW_DIST, "view_angle": ang,
        "tv_above_eye_deg": up, "door_clear": DOOR_CLEAR, "pend_z": PEND_Z,
        "lowest_shade": CEIL - BAR[2], "ledge_lp_top": LEDGE_LP_TOP, "above_ledge_lps": HIGH_UNDER - LEDGE_LP_TOP,
        "to_ceiling": CEIL - HIGH_TOP,
    }


if __name__ == "__main__":
    for k, v in summary().items():
        print(f"{k:18} {v}")
