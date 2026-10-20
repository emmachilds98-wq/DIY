"""The full build instructions (v13.5): for each step of the order of work, what you need (parts, hardware, tools), the
drawings to have open, and every instruction in order, grouped by sub-assembly. Sizes are finished sizes in cm and come
from geometry.py, the fit proof and the cutting list (build_doc.cuts), so the instructions move when the plan does.
build_doc.steps() merges these in: the PDF prints them after the order-of-work table, and the plan page shows them in
each step's card."""
import geometry as G


def n(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


def full():
    g = G
    up_h = lambda y: n(y - g.WORKTOP)                       # a height on the wall, measured up an upright from its foot
    tenon = (g.RZ_SHELF_TOP - g.RZ_SHELF_T + (g.RZ_SHELF_T - 2.4) / 2, g.RZ_SHELF_TOP - (g.RZ_SHELF_T - 2.4) / 2)
    sub_col_w = g.SUB_COL[1] - g.SUB_COL[0]
    ps_w = g.PS_COL[1] - g.PS_COL[0]
    breast_l = lambda x: n(x - g.BREAST_X[0])               # a position on the breast, from its alcove-side corner
    return {
        1: dict(
            tools=["Tape measure", "Spirit level, 120 cm", "Notebook or the Questions tab"],
            draw=[]),
        2: dict(
            parts=["Two TP-Link TL-SG108 8-port switches", "Cat6 patch leads, 0.5–2 m (11)"],
            tools=["A phone with the Deco app", "A laptop for the hub's settings page"],
            draw=["network"]),
        3: dict(
            parts=["Cat6 solid pure copper (not CCA), 2–4 runs", "RJ45 keystones and two surface boxes, or RJ45 plugs",
                   "A double socket in the same finish, and a deeper back box if the old one is shallow",
                   "Conduit: 38 mm and 25 mm oval, about 4 m each, two draw wires", "A 5 m C13 lead with a rewireable 13 A plug, for the PC", "One-coat filler"],
            hardware=["Cable clips for the Cat6 in the loft space or under the boards", "Brown wall plugs and 4 × 30 screws for the conduit clips"],
            tools=["Two-pole voltage tester (GS38) and its proving unit", "MCB lock-off and padlock", "Plug-in socket tester", "Insulated screwdrivers, wire strippers, side cutters",
                   "Cat6 punch-down tool (or crimper) and a cable tester", "Draw rods", "Wall chaser with dust extraction, or a bolster and club hammer",
                   "Cable and pipe detector", "SDS drill", "Safety glasses, ear defenders, FFP2 masks", "A helper"],
            draw=["power", "routes"],
            parts_full=[
                ("Before you start: the stop list", [
                    "Stop and call an electrician if: the tester shows anything live after you've isolated; the wiring is old (rubber or fabric sheath, or red and black with no earth); there are more wires than you can match to your photo; there are scorch marks or the old socket is loose or hot; the consumer unit has rewireable fuses or no RCD; or the job grows into a new circuit.",
                    "Nothing in this step is notifiable in England: the socket is a like-for-like swap on an existing circuit, outside a bathroom. It must still be done to the wiring regulations, which is what this routine is for.",
                ]),
                ("The Cat6 runs (low voltage: no isolation needed)", [
                    "Measure each route on the house plan and add 2–3 m: bedroom 3, across the landing, down through the airing cupboard.",
                    "Lift a floorboard in the airing cupboard. Drill a 20 mm hole through the plate below (detector first), and feed a draw rod down to the alcove's right corner. Tape both Cat6 cables and a spare to it and pull them through. Pull the kitchen run on down the same way, past the right upright's groove.",
                    "Keep the Cat6 away from mains: cross at right angles, never run alongside in the same hole. Clip it every 30 cm; never staple through it or kink it.",
                    "Punch each end down onto a keystone in a surface box (or crimp a plug), to the T568B colours on both ends. Label both ends.",
                    "Test each run with the cable tester: all eight lights in order. Re-terminate any that don't.",
                ]),
                ("Isolate the socket circuit", [
                    "Tell everyone in the house you're working on the electrics.",
                    "At the consumer unit, switch off the breaker for the side-wall socket's circuit (usually a ring marked \"sockets\"). If the labels aren't clear, switch off the main switch instead.",
                    "Fit the MCB lock-off and padlock to that breaker, keep the key in your pocket, and tape a note on the board: \"Working on this circuit, do not switch on\".",
                    "Prove your voltage tester on its proving unit: it must light.",
                    "At the socket, with it pulled forward on its cables, test between every pair: live and neutral, live and earth, neutral and earth. No reading on any of them.",
                    "Prove the tester on the proving unit again. Only now is it safe to touch.",
                ]),
                ("Swap the single socket for a double", [
                    "Unscrew the old socket and ease it out. Photograph the wiring before you undo anything.",
                    "Check the stop list against what you see: an earth (green-and-yellow) wire present and sleeved, no scorching, the cable sheath into the box.",
                    "If the double needs a bigger box, chop the plaster out round the old box to the new box's outline and fit the new box with plugs and screws, the cables through its grommets.",
                    "Connect wire for wire: brown (or red) to L, blue (or black) to N, green-and-yellow to the earth terminal. Two cables in the old box go into the same terminals together. Strip only enough so no copper shows outside a terminal, and tighten every screw firmly.",
                    "Fold the cables in neatly without trapping them, and screw the socket on level.",
                    "Remove the lock-off, switch on, and plug the socket tester into each outlet: it should show correct wiring on both.",
                ]),
                ("The PC's two conduits in the side wall", [
                    "Mark the route from behind the PC shelf's back corner straight down to skirting height, then along behind the skirting to the base's plinth. Run the detector along it: move it if anything shows. Never chase near the socket's cables, which run straight up, down or across from it.",
                    "Chase two channels side by side, 5 cm apart: one for the 38 mm oval conduit (data: HDMI and Cat6), one for the 25 mm (the PC's mains lead). Vertical only on the wall, no deeper than the conduit needs. Wear the mask: the dust is silica.",
                    "Take the skirting off along the route, fix both conduits with a draw wire inside each, and refit the skirting over them.",
                    "Fill the chase with one-coat filler, sand flush, and photograph the route with a tape measure in the shot before you paint.",
                ]),
                ("Finish", [
                    "Mark every route on the plan, and keep the photos with it.",
                ]),
            ]),
        4: dict(
            parts=["Card Room Green emulsion and eggshell, primer and undercoat", "Sugar soap, sanding pads, woodwork primer"],
            tools=["Roller, tray and extension pole", "25 and 50 mm brushes", "Dust sheets, masking tape", "Step ladder"],
            draw=[]),
        5: dict(
            tools=["Cross-line laser level", "Tape measure", "Pencil and masking tape", "Cable and pipe detector", "Spirit level, 120 cm"],
            draw=["front"],
            parts_full=[
                ("Set up a datum", [
                    "Find the floor's highest point across the alcove (you measured its level in step 1). Every height in this plan is measured from there.",
                    "Stand the laser in the middle of the room, level it, and mark a line at exactly 100 cm above that high point on the alcove's back wall, both side walls and the chimney breast.",
                    "Measure every other height up or down from the 100 line, not up from the floor: the floor is the thing that isn't level.",
                ]),
                ("The alcove's heights", [
                    "Put a strip of masking tape down each side wall and the back wall of the alcove and mark these heights on it:",
                    f"{n(g.CARCASS_TOP)}: the tops of the frames and bay 3 (the worktop's underside).",
                    f"{n(g.WORKTOP)}: the worktop's top.",
                    f"{n(g.RZ_SHELF_TOP - g.RZ_SHELF_T)} and {n(g.RZ_SHELF_TOP)}: the Series X shelf, underside and top.",
                    f"{n(g.LEDGE_UNDER)} and {n(g.LEDGE_TOP)}: the record ledge and the wrap ledge, underside and top.",
                    f"{n(g.HIGH_UNDER)} and {n(g.HIGH_TOP)}: the high shelf, underside and top.",
                    f"Carry the {n(g.LEDGE_UNDER)} and {n(g.LEDGE_TOP)} lines along the side wall to {n(g.ALC_D - g.PC_SHELF_Z[1])} cm out from the alcove's back wall, for the wrap ledge and the PC shelf.",
                ]),
                ("Across the back wall", [
                    f"Mark the uprights' positions from the side wall: the left one {n(g.UP_L[0])}–{n(g.UP_L[1])}, the right one {n(g.UP_R[0])}–{n(g.UP_R[1])}. Turn the laser to its vertical line and draw both lines from the worktop line to the ceiling.",
                    f"Mark the base from the side wall along the floor: filler 0–{n(g.FILLER)}, bay 1 {n(g.BAYS[0][0])}–{n(g.BAYS[0][1])}, bay 2 {n(g.BAYS[1][0])}–{n(g.BAYS[1][1])}, bay 3 {n(g.BAYS[2][0])}–{n(g.BAYS[2][1])}, filler to {n(g.ALC_W)}.",
                ]),
                ("On the chimney breast", [
                    f"Find the breast's centre: {n(g.BREAST_W / 2)} cm from its alcove-side corner. Draw it plumb from the floor to 170.",
                    f"Mark the backboard: {n(g.RAIL[0] / 2)} cm either side of the centre line, from {n(g.RAIL_TOP - g.RAIL[1])} to {n(g.RAIL_TOP)} high.",
                    f"Mark the two bracket centres {n((g.HEBGO_X[1] - g.HEBGO_X[0]) / 2)} cm either side of the centre line.",
                    f"Mark the folded table's top edge at {n(g.FOLDED_TOP)}, and the framed LPs' bottom edges at {n(g.FRAMES_Y)}.",
                ]),
                ("Check for cables", [
                    "Run the detector along every line where you'll drill: the cleats, the spacer blocks, the upright brackets, the backboard and the PC shelf.",
                    "Mark anything it finds in red, and compare with your own photos from step 3. Move a fixing 5 cm rather than drill near a cable.",
                ]),
            ]),
        6: dict(
            parts=["Two IKEA BESTÅ frames 60 × 40 × 64", "18 mm birch ply: bay 3 sides 73 × 40 (2), top and bottom 56.4 × 40 (2); plinth rails 120 × 9 (2), cross-pieces 34.4 × 9 (3)",
                   "Four 4 cm spacer blocks (ply offcuts, 4 × 10 × 1.8)", "Anti-tip brackets: two per bay (6)", "Flat two-compartment trunking, about 2 m",
                   "Plastic shims", "Four connector bolts (furniture joint connectors)"],
            hardware=["4 × 40 and 4 × 50 mm wood screws", "5 × 60 mm screws and brown wall plugs", "Wood glue"],
            tools=["Drill-driver with pilot and countersink bits", "SDS drill with a 7 mm masonry bit", "Spirit level, 60 and 120 cm", "Combination square", "Clamps", "Tape measure"],
            draw=["front", "section"],
            parts_full=[
                ("The plinth under bays 1 and 2", [
                    "Lay the two 120 × 9 rails on edge, 38 cm apart outside, and stand the three 34.4 × 9 cross-pieces between them: one at each end and one in the middle, at 60.",
                    "Pre-drill, glue and screw through the rails into each cross-piece end with two 4 × 40 screws.",
                    "Measure both diagonals: when they're equal the frame is square. The plinth is 120 × 38 × 9. The opening between 60 and 120 stays clear: it's the hidden drawer's bay.",
                    f"Stand it in the alcove {n(g.FILLER)} cm from the side wall and {n(g.CHAN)} cm off the back wall. Level it with shims, side to side and front to back.",
                ]),
                ("The BESTÅ frames", [
                    "Assemble both frames to IKEA's instructions, but leave the back panels off: the open backs are how the cables and the sub's port breathe.",
                    "Join the two frames side by side with IKEA's connectors.",
                    "Stand them on the plinth, their backs flush with its back edge, so their fronts sit 2 cm proud of the plinth (the face frame covers the step).",
                ]),
                ("Bay 3, the record carcass", [
                    "While the sides are flat, mark the runner lines on their inner faces: 2.3 and 37.0 cm up from the bottom edge, for the two trays' undersides.",
                    "Stand the bottom panel between the two sides, flush with their bottom edges, and the top panel flush with their top edges. Pre-drill, countersink, glue and screw with four 4 × 50 screws a joint.",
                    "Check the diagonals for square. The carcass is 60 × 40 × 73, open at the back.",
                    f"Stand it in its place, {n(g.BAYS[2][0])}–{n(g.BAYS[2][1])} from the side wall, its top level with the frames' tops at {n(g.CARCASS_TOP)}. Shim under it if the floor drops away.",
                    "Clamp it to bay 2 and fit two connector bolts at the front and two at the back.",
                ]),
                ("Fix it to the wall", [
                    f"Screw a 4 cm spacer block to the back wall behind the top of each bay, at {n(g.CARCASS_TOP - 5)} high, with plugs.",
                    "Push the whole base back against the blocks.",
                    "Fit two anti-tip brackets per bay through the blocks into the wall. Do this before anything heavy goes in: a full record tray pulled out is about 32 kg in front of the unit.",
                    "Lay a level across all three tops: within 1 mm over 186 cm. Shim and re-check.",
                ]),
                ("The cable channel", [
                    "Lay the flat two-compartment trunking on the floor in the 4 cm channel behind the base: mains on the wall side, data on the other.",
                    "Run the leads in now: the two mains leads from the side-wall socket enter through the plinth's left end, the Cat6 and Deco B's lead come down the right-hand corner.",
                    "Keep the channel behind bay 2 empty: the sub's port breathes into it. Switch 2 and the retro 6-way stand on edge behind bay 1.",
                ]),
            ]),
        7: dict(
            parts=["One solid oak worktop, 300 × 62 × 3, full stave", "A 60 mm brush strip and a 35 mm brush grommet"],
            hardware=["4 × 30 mm screws with washers (9)", "Hardwax oil"],
            tools=["Hardboard or cardboard, 190 × 50, for the template", "Compass or a pencil on a block, for scribing", "Track saw or circular saw with a guide",
                   "Jigsaw", "Router with a straight bit", "Random-orbit sander, 120 and 180 grit", "Drill-driver", "A helper"],
            draw=["section"],
            parts_full=[
                ("Make a template", [
                    f"Cut the hardboard to about 190 × 50 and push it into the alcove at worktop height, its back edge against the back wall.",
                    "Set the compass to the widest gap at one end and run it down the side wall, so the pencil copies the wall's line onto the board. Cut to the line. Do the other end the same way.",
                    f"Mark the front edge at {n(g.BASE_D)} cm from the back wall all along. The template is now the worktop's exact shape.",
                ]),
                ("Cut the oak", [
                    "Lay the board best face up, grain running along its length. Lay the template on it and draw round it.",
                    "Cut just outside the line with the track saw, then sand or plane to the line.",
                    f"From the offcut, cut the dining wall's backboard: {n(g.RAIL[0])} × {n(g.RAIL[1])} × {n(g.RAIL[2])}.",
                    "Chamfer the worktop's top front edge with a 3 mm chamfer, sanded by hand.",
                ]),
                ("Cut the openings", [
                    f"The TV slot: 3 cm wide, from 1 to 4 cm in from the back edge, running {n(g.TV_CX - 40)}–{n(g.TV_CX + 40)} from the side wall. Clamp a batten as a guide and rout it in passes, or drill each end and jigsaw between. Push the brush strip in.",
                    f"The grommet hole behind the deck: 35 mm, its centre 2.5 cm from the back edge and {n((g.DECK_X[0] + g.DECK_X[1]) / 2)} from the side wall.",
                ]),
                ("Finish and fix", [
                    "Sand to 120, then 180. Oil every face: top, underside, both ends and the cut edges of the slot. Two coats, a night between them.",
                    "Two of you lift it in and push it back to the wall. It should touch both side walls along their length.",
                    "Inside each bay, drill three 5 mm holes up through the top panel, elongated front to back to about 12 mm long, so the oak can move with the seasons.",
                    "Screw up through them into the worktop with 4 × 30 screws and washers. They must not come out through the top: check the length against a scrap.",
                ]),
            ]),
        8: dict(
            parts=["Four BESTÅ shelves 56 × 36", "Game drawer: 12 mm ply sides 35 × 15.5 (2), back 51.9 × 15.5, front panel 51.9 × 6; 9 mm base 52.5 × 34.4; 6 mm divider 51.9 × 9, bin walls 12.6 × 9 (2), bin floors 16 × 12.6 (2); oak lip 56.8 × 6.5 × 2; follower blocks",
                   "Record trays (×2): 12 mm base 53.9 × 40; 9 mm sides 40 × 8 and ends 52.1 × 8; 6 mm oak divider 38.2 × 8; oak lip about 56 × 5 × 1.5; felt",
                   "Plinth drawer: 12 mm sides 34 × 4.4 and ends 49.6 × 4.4, 6 mm base 52 × 34, oak front 54 × 6 × 2",
                   f"Bay 2: 12 mm divider 35.3 × 38, part shelf {n(ps_w)} × 36, the sub's isolation riser about 22 × 28 × 3",
                   "The oak face frame, 2 cm thick: stiles about 5 wide, rails; 186 × 73 overall"],
            hardware=["Runners: two pairs of 400 mm (68–70 kg), one pair of 350 mm soft-close, one pair of 300 mm", "3.5 × 16 mm screws for the runners (every hole)",
                      "Four shelf pins for the part shelf", "Two small steel angle brackets for the divider", "Panel pins, wood glue, felt"],
            tools=["Drill-driver", "Router with a 6 mm straight bit (the game drawer's base groove)", "Combination square", "Spirit level", "Clamps", "Mitre saw or tenon saw"],
            draw=["drawer_layouts", "game_drawer", "drawer", "storage"],
            parts_full=[
                ("The console shelves", [
                    "Bay 1, from the top: rows of 16 (Xbox One), 16 (Xbox 360), then the game drawer's 25.2. Put the shelves on the pin holes nearest those heights.",
                    "Bay 2: the PS3's row of 23.7 at the top, on a full-width shelf. Below it, the PS2 and the PS1 sit beside the sub (next part).",
                ]),
                ("Bay 2's sub column", [
                    f"Stand the 12 mm divider on the bay's floor, {n(sub_col_w)} cm from the bay's left inner face, tight under the PS3 shelf. Check it's plumb.",
                    "Fix it with one small angle bracket at the bottom (into the frame's bottom panel) and one at the top (into the PS3 shelf's underside).",
                    "Drill two 5 mm pin holes in the divider's right face at the height of the frame's pin holes for the PS2/PS1 shelf. Fit the part shelf on four pins.",
                    "Pair the sub with the soundbar now: its PAIR button is on the back, and it's hard to reach once it's in.",
                    "Lay the isolation riser on the column's floor, its front edge flush with the frame's front.",
                    "Stand the sub on it with the grille facing the room, centred: 1 cm to the divider, 1 cm to the frame's side. Slide it forward until its front is flush with the face frame's front (2 cm proud of the frame). Run its lead out of the back.",
                    "Check it touches nothing but the riser. If it does, a sheet of felt between, or nudge it.",
                ]),
                ("The game drawer (bay 1, bottom row)", [
                    "Fit the 350 mm runners to the frame's sides, level, so the drawer's base will sit about 1 cm above the frame's bottom panel. Drill pilot holes: BESTÅ sides are particleboard. If a screw won't hold, glue a 12 mm ply packer behind the runner.",
                    "Rout a 6 mm deep groove 1 cm up from the bottom on the inner faces of the sides, back and front panel, 9 mm wide, for the base.",
                    "Glue and screw the box together round the base: outside 54.3 × 35. Check the width against the runner maker's figure (usually the opening less 25.4 mm) before the glue sets.",
                    "Fit the cross divider 13 cm back from the front, and the two bin walls 16 cm in from each side. Glue in the bin floors with a slight back-rake, so the cases lean about 13°.",
                    "Felt the base and make the follower blocks.",
                    "Fit the runners' inner members to the box, hang it, and check it runs true empty.",
                ]),
                ("The record trays (bay 3)", [
                    "Screw the 400 mm runners to bay 3's sides with their bottom edges on the lines at 2.3 and 37.0 cm. Use every hole: a full tray is about 32 kg.",
                    "For each tray, glue and pin the two 40 × 8 sides and two 52.1 × 8 ends on top of the 53.9 × 40 base, round its edge.",
                    "Fit the 6 mm oak divider 32.6 cm from the left side's inner face: the LP trough on the left, the singles trough on the right.",
                    "Glue a raked rest (an oak offcut) at the back of each trough, so the sleeves lean back about 10°. Felt the troughs.",
                    "Fit the runners' inner members, hang the tray, and run it in and out empty, then with ten records.",
                ]),
                ("The hidden plinth drawer", [
                    "Make the box: the two 34 × 4.4 sides, the two 49.6 × 4.4 ends between them, the 6 mm base screwed underneath. It's 52 × 34 × 5.",
                    "Pack the plinth's inner faces under bay 2 with ply strips so the 300 mm runners sit the box's width plus their allowance apart, and fit the runners with the box 1.6 cm off the floor.",
                    "Felt the runners: the drawer sits under the sub.",
                ]),
                ("The face frame and the drawer fronts", [
                    "Cut the stiles (about 5 wide) and the rails from 2 cm oak. The bottom rail covers the plinth, 9 tall under bays 1–2, with an opening 54 × 6 for the plinth drawer, 1.6 up, under bay 2.",
                    "Scribe the two end stiles to the walls, then glue and pin the frame to the frames' fronts and bay 3. Notch the bottom rail's left end for the two socket leads.",
                    "Screw the oak lips onto the game drawer, the two trays and the plinth drawer from inside each box, with a 2–3 mm gap all round to the face frame.",
                    "Cut each finger pull underneath its lip: a cove routed along the back of the bottom edge.",
                ]),
            ]),
        9: dict(
            parts=["Two oak uprights, 165 × 30 × 4.5 (cut to fit)", "High shelf: 128.9 × 30 × 4 and 51.7 × 30 × 4", "Record ledge 128.9 × 7 × 2.4 and its lip",
                   "Series X shelf 55 × 30 × 4", "Two oak cleats for the reveal, 30 long", "Oak wedges (2 + spares), 10 mm oak dowel for pegs and the uprights' dowels"],
            hardware=["Four concealed upright brackets", "5 × 60 mm screws and plugs", "Wood glue", "LED strip in its aluminium channel (from the lighting phase)"],
            tools=["Router with a straight bit and a guide batten", "Chisels 6, 12 and 25 mm, and a mallet", "Japanese pull saw", "Drill with a 10 mm brad-point bit and a 20 mm bit",
                   "Dowel jig or dowel centres", "Combination square, marking knife", "Spirit level and laser", "Clamps", "A helper"],
            draw=["joints", "section"],
            parts_full=[
                ("Cut the uprights to length", [
                    f"Measure from the worktop to the ceiling at each upright's position. The plan says {n(g.UPRIGHT_LEN)}; ceilings vary.",
                    "Cut each upright 2 mm under its measurement, then scribe its top to the ceiling as you did the worktop.",
                    "Mark each upright's faces: which side faces the TV, and the back edge that goes against the wall.",
                ]),
                ("The housings (both uprights)", [
                    f"Measure from each upright's foot (the end on the worktop). The high shelf's housing is {up_h(g.HIGH_UNDER)}–{up_h(g.HIGH_TOP)} up, the full 30 depth, 1.2 deep, on the TV-side face of both uprights.",
                    f"The record ledge's housing is {up_h(g.LEDGE_UNDER)}–{up_h(g.LEDGE_TOP)} up, 0–7 from the back edge, 1.2 deep, on the TV-side face of both.",
                    f"On the right upright's other face (the turntable side), a second high shelf housing at {up_h(g.HIGH_UNDER)}–{up_h(g.HIGH_TOP)}, full depth, for the short length.",
                    "Clamp a straight batten as a guide, set the router 4 mm deep and rout, then step down to 12 mm in passes. Square the ends with a chisel. Practise on an offcut first.",
                ]),
                ("The through-mortises (right upright)", [
                    f"Two mortises, each 6 wide and 2.4 tall, at {up_h(tenon[0])}–{up_h(tenon[1])} up from the foot, 12–18 and 20–26 cm from the back edge.",
                    "Mark them on both faces with a square and a knife. Drill most of each out with the 20 mm bit, halfway from each face, then chisel to the lines.",
                    "On the TV-side face, flare the top and bottom of each mortise outwards 3–4 mm, for the wedges.",
                ]),
                ("The tenons (Series X shelf)", [
                    "On the shelf's west end (the end that goes through the upright), mark two tenons 6 wide and 2.4 thick, centred in its 4 cm thickness, 12–18 and 20–26 from its back edge, 4.5 long.",
                    "Saw the shoulders and cheeks, and cut away the rest of the end back to the shoulder line.",
                    "Saw a kerf 3 cm deep across the middle of each tenon, parallel to the shelf's faces.",
                    "Test-fit through the mortises: snug, pushed in by hand.",
                ]),
                ("The grooves", [
                    "On each upright's TV-side face, rout a groove for the LED channel (usually about 1.7 wide × 0.8 deep: check yours), 2 cm in from the front edge, from 2 cm above the worktop to just under the high shelf's housing.",
                    "On the right upright's back edge, rout a 2 × 1.5 cable groove the full length, for Deco B's 12 V and patch leads, the Series X's HDMI and power, and the vinyl lead.",
                    "Notch both uprights' tops for the ceiling LED strip.",
                ]),
                ("Dry-fit, then fix", [
                    "Lay each upright on the floor with its shelves in their housings. Check every joint closes before any glue.",
                    "Drill two 10 mm holes 3 cm deep in each upright's foot, and matching holes in the worktop at the marked positions (dowel centres make this exact). Glue the dowels into the uprights only, so they can come out.",
                    "Lay Deco B's leads and the other cables into the right upright's back groove.",
                    "Stand the left upright on its dowels against the side wall. Screw it to the side wall through three countersunk holes, with plugs, and plug the holes with oak.",
                    "Stand the right upright on its dowels, check it's plumb with the laser, and fix it to the back wall with the concealed brackets.",
                    "Slide the long high shelf and the record ledge into their housings from the front.",
                    "Screw a 30 cm cleat to the breast's side face (the reveal) for the short high shelf, and another at the Series X shelf's underside height. Slide the short high shelf in from the front onto its cleat and into its housing.",
                    "Feed the Series X shelf's tenons through the mortises from the turntable side, onto its cleat. Glue the wedges and drive them into the kerfs from the TV side. When dry, saw them flush and plane: proud, they'd touch the TV.",
                    "Pegs: drill 10 mm through each upright's face into the housed shelf ends, 4 cm deep, about 4 cm from the front edge. Glue in a peg and saw it flush.",
                ]),
            ]),
        10: dict(
            parts=["Wrap ledge 134 × 7 × 2.4 and its lip", f"PC shelf {n(g.PC_SHELF_Z[0] - g.PC_SHELF_Z[1])} × {n(g.PC_SHELF_D)} × 4", "Two oak cleats, 2 cm",
                   "Keyboard tray: oak housing 70 × 28 × 7 (sides 7 × 2), 12 mm ply tray 54 × 26 with an oak lip"],
            hardware=["Two concealed shelf brackets rated 40 kg+ a pair", "300 mm light-duty runners, one pair", "An oak-coloured brush grommet", "10 mm dowels (2)", "5 × 60 mm screws and plugs"],
            tools=["SDS drill", "Drill-driver", "Dowel jig", "Spirit level and laser", "Jigsaw", "Clamps"],
            draw=["pc_shelf"],
            parts_full=[
                ("The cleats", [
                    f"Screw the first cleat to the side wall with its top on the {n(g.LEDGE_UNDER)} line, from the left upright's front edge ({n(g.UP_D)} cm out from the back wall) to {n(g.ALC_D - g.WRAP_Z[1])} cm out. Plugs every 25 cm.",
                    f"Screw the second with its top at {n(g.PC_SHELF_TOP - g.PC_SHELF_T)} (the PC shelf's underside), from {n(g.ALC_D - g.PC_SHELF_Z[0])} to {n(g.ALC_D - g.PC_SHELF_Z[1])} cm out.",
                ]),
                ("The wrap ledge", [
                    "Drill two 10 mm dowel holes in the ledge's end and matching holes in the left upright's front edge, using the jig.",
                    "Glue the dowels, push the ledge onto them and down onto its cleat, and screw up through the cleat into it.",
                    "Glue the lip along its front edge.",
                ]),
                ("The PC shelf and its tray", [
                    "Fit the concealed brackets into the wall at the shelf's height, through the cleat, to the maker's instructions.",
                    "Cut the grommet hole in the shelf's back corner, over the top of the chased conduit.",
                    "Screw the keyboard tray's housing to the shelf's underside, stopping 12 cm short of the sofa end so the cables drop past it. Fit the runners inside it and slide the tray in.",
                    "Slide the shelf onto its brackets and down onto the cleat. Lean on it: it shouldn't move.",
                ]),
                ("The PC's leads", [
                    "Fit the brush grommet. Pull the HDMI (active optical: the end marked \"source\" at the PC) and the Cat6 down the 38 mm conduit with its draw wire.",
                    "Take the plug off the C13 lead, feed its bare end down the 25 mm conduit, and at the bottom fit the rewireable plug: brown to L, blue to N, green-and-yellow to E, the cord grip on the outer sheath, a 13 A fuse.",
                    "At the bottom, all three run behind the skirting into the plinth's notch and the channel; the mains lead goes on to the 10-gang behind the TV.",
                ]),
            ]),
        11: dict(   # v15: the flip-top gate-leg table, which stays on the wall
            parts=["Solid oak: two panels, each a centre 101 × 80 × 2.7 (edge-glued staves) with two breadboard ends 80 × 7 × 2.7: the top and the half; the backboard 110 × 22 × 3 and the hinge rail 110 × 4 × 7.3 (from step 7), two turn buttons 6 × 2.5 × 2.2",
                   f"The gate leg: two tapered oak legs {n(g.GATE_LEG_H)} × 4.5 to 3 and an apron {n(g.TABLE[0] - 2 * g.FLIP['inset'])} × 7 × 2"],
            hardware=["Two Häfele Hebgo 287.43.428 folding brackets", "Union PowerLoad 100 × 88 lift-off hinges, one 3-pack, all the same hand",
                      "Three Lee Valley 40574 narrow flip-top hinges (1.27 × 7.0) and their screws", "Two 75 mm steel butt hinges and two folding locking stays for the gate",
                      "A magnetic catch", "5 × 70 mm screws and brown plugs", "Felt pads", "Hardwax oil, glue, 10 mm oak dowel for pegs"],
            tools=["Router with a straight bit and a guide", "Drill with a 10 mm brad-point bit", "Jigsaw and sander", "Chisels", "SDS drill", "Spirit level", "Clamps", "A helper"],
            draw=["fliptop", "seating"],
            parts_full=[
                ("Order the oak", [
                    "Ask the timber merchant for two centre panels as edge-glued staves, 101 × 80 × 2.7 each: 96 between the shoulders plus a 2.5 tongue at each end. Most will also cut the four breadboard ends and radius the half's two free corners.",
                ]),
                ("The breadboard ends (both panels)", [
                    "On each end of each centre panel, rout a tongue 2.5 long and 0.9 thick, centred in its thickness: take 0.9 off each face with the router against a batten.",
                    "In each breadboard end's inner edge, rout a groove 0.9 wide and 2.6 deep, centred, full length.",
                    "Dry-fit: the breadboard ends flush with the panel's long edges, flat across the joint.",
                    "Drill three 10 mm peg holes down through each breadboard end and the tongue in it: one at the centre and one 8 cm in from each long edge, 1.3 cm from the breadboard's inner edge.",
                    "Take the ends off. Elongate the two outer holes in each tongue to 16 mm long, along the panel's width: the panel moves with the seasons, the breadboard doesn't.",
                    "Glue only the middle 10 cm of each tongue and groove, clamp the ends on, and drive the pegs. Glue the outer pegs into the breadboard only, not the tongue. Saw flush and sand.",
                ]),
                ("Shape and finish", [
                    "Radius the half's two free corners to 5 cm (the top's corners meet the wall and the half, so they stay square): jigsaw outside the line, then sand to it.",
                    "Chamfer the underside edges 1 cm, except the two that meet at the joint, so it reads slim.",
                    "Sand both to 180. Oil both faces of both panels equally, every edge too: a panel oiled on one side cups.",
                ]),
                ("The joint: three flip-top hinges", [
                    "Lay the top and the half face up, their meeting edges together, flush across the top. Mark three hinges: one in the middle and one 15 cm in from each side.",
                    "Each hinge's two leaves set into the two edges; rout the recesses to the hinge's depth with a guide, square them with a chisel, and screw the hinges in. The pin sits so the half swings over onto the top through 180° and lies flat on it.",
                    "Swing it: open, the two tops are flush; folded, the half lies flat on the top with nothing proud.",
                ]),
                ("The gate leg", [
                    f"Tenon the two legs into the ends of the apron, the legs {n(g.FLIP['inset'])} cm in from the half's sides, square. Glue and clamp.",
                    f"Screw the two butt hinges along the apron's top edge and up into the half's underside, {n(g.FLIP['hinge_in'])} cm in from its far edge, so the gate swings down to stand upright and up to lie flat along the half's 80 cm.",
                    "Fit a folding locking stay from each leg to the half's underside: upright, they lock; push the knuckle to fold.",
                    f"Stand it on the floor upside down and check: folded, the legs lie flat with {g.FLIP['leaf'][1] - g.FLIP['hinge_in'] - g.LEG[0] / 2 - g.GATE_LEG_H:.1f} cm to spare before the joint.",
                ]),
                ("The backboard and hinge rail", [
                    f"Glue and screw the hinge rail along the backboard's top edge, flush at the back, so it stands {n(g.RAIL[2] - 3)} cm proud of the backboard's face.",
                    f"Hold the backboard on its marks: centred on the wall, the rail's top at {n(g.RAIL_TOP)}, level.",
                    "Drill through it and into the wall every 20 cm in two rows, 3 cm from its top and bottom edges. Plug, then fix with 5 × 70 countersunk screws.",
                ]),
                ("The brackets", [
                    f"Screw the two Hebgo brackets to the backboard's face, {n(g.HEBGO_X[1] - g.HEBGO_X[0])} cm apart centre to centre ({n((g.RAIL[0] - (g.HEBGO_X[1] - g.HEBGO_X[0])) / 2)} cm in from each end), their arm tops level with the rail's top.",
                    "Use long screws through the backboard into plugs in the wall, as many as the bracket's holes take: the 500 kg rating depends on the fixing.",
                    "Raise both arms until they click and lock. Lay a level across them.",
                ]),
                ("Hang the table", [
                    "Screw the three lift-off hinges along the rail's front edge, 10 cm from each end and one in the middle, pin halves on the rail.",
                    "Screw the other halves to the underside of the top's back edge (the long edge that meets the wall) at the same spacing, all the same hand.",
                    "With your helper, lower the top onto the pins and let it rest on the arms: at 76, level, in line with the alcove's worktop.",
                    "Flip the half out and lower its gate leg: it should stand level with the top all along. Adjust with felt glides if the floor isn't flat.",
                ]),
                ("Folded", [
                    "Fold the gate flat, flip the half back over onto the top, then lift the pair to vertical together: two people, one at each corner (about 37 kg).",
                    f"Its top edge is at {n(g.FOLDED_TOP)}. Screw the two oak turn buttons to the wall just above it, 15 cm in from each end. Fit the magnetic catch behind the top edge.",
                    "Open and fold it three times: it shouldn't bind, both arms should click, the gate's stays should lock, and nothing should move when you lean on it open.",
                ]),
            ]),
        12: dict(
            parts=["Both Wolston-style spot bars and eight smart colour E14 bulbs under 6 W (WiZ Colour P45 4.9 W, or Hue E14 lustre 5.1 W)",
                   "2700K LED strip (about 4.5 m), three aluminium channels, a plug-in driver with an inline dimmer", "6500K bias light for the TV", "Your red lamp, with its colour bulbs"],
            hardware=["Connector block or lever connectors (if the bar's flex needs them)", "Earth sleeving, insulating tape"],
            tools=["Two-pole voltage tester (GS38) and its proving unit", "MCB lock-off and padlock", "Insulated screwdrivers, wire strippers", "Step ladder", "A helper to hold the bar"],
            draw=[],
            parts_full=[
                ("Before you start", [
                    "No dimmers: smart bulbs need full power, so leave the light switches as they are and keep them on. A dimmer in front of a smart bulb makes it flicker and can damage it.",
                    "The same stop list as step 3. Here, also stop if a ceiling point has no earth (the bars need one), or the rose has more wires than you can match to your photo.",
                ]),
                ("Isolate the lighting circuit", [
                    "Tell everyone in the house you're working on the electrics.",
                    "At the consumer unit, switch off the breaker for the lighting circuit (usually marked \"lights\", 6 A). If the labels aren't clear, switch off the main switch instead.",
                    "Fit the MCB lock-off and padlock to that breaker, keep the key in your pocket, and tape a note on the board: \"Working on this circuit, do not switch on\".",
                    "Prove your voltage tester on its proving unit: it must light.",
                    "At each switch and each ceiling point, with the cover off, test between every pair: live and neutral, live and earth, neutral and earth. No reading on any of them.",
                    "Prove the tester on the proving unit again. Only now is it safe to touch.",
                ]),
                ("Take down the old fittings, hang the bars", [
                    "Unscrew each old fitting's cover. Prove dead again at its terminals. Photograph the wiring, mark the switched live (the wire from the switch) with tape, then disconnect and take the fitting down.",
                    "Fix bar 1's mounting plate to the ceiling over the rose between the TV and the sofa, the bar running from the TV towards the window (v15), with screws into the joist or the plate's fixings. Bar 2's goes on the pendant point by the stairs, running the same way, along the west wall.",
                    "Connect earth first (green-and-yellow to the bar's earth), then neutral to N and the switched live to L, in the bar's terminal block; any loop wires go back together exactly as they were. Tighten, tuck, and fit the canopy.",
                    "Fit the smart colour bulbs and aim the heads: the table in the Paint and light tab says which goes where. Never at the TV. If a WiZ bulb shows below its shade's rim, use the shorter Hue lustre there.",
                ]),
                ("Power on and test", [
                    "Remove the lock-off and switch on, wall switches on. In the bulbs' app, add all eight, group them as bar 1 and bar 2, set warm white at about half, then save the four scenes from the Paint and light tab (levels, and colours if you want them). Your red lamp's colour bulbs go in the same scenes.",
                ]),
                ("The low-voltage lights (nothing to isolate)", [
                    "Press the 2700K strip into each upright's groove in its aluminium channel; take its lead down the groove to the plug-in driver on the 10-gang.",
                    "The side-wall shelf's strip (v15): in its channel in the groove under the run's front edge, 1.5 cm back from the edge, the full 220 cm; its lead drops with the PC's through the brush grommet into the conduit, to the same driver.",
                    "Clip the ceiling strip through its notches in the uprights; stick the bias light round the back of the TV on its USB port.",
                    "Stand your red lamp in its spot (the 3D room shows the three), its bulbs green, pink and purple, top to bottom.",
                ]),
            ]),
        13: dict(
            parts=["HDMI switch, RetroTINK, HDMI leads, optical and SCART cables, the active optical HDMI for the PC", "Stylus, preamp, RCA-to-3.5 mm lead, record brush", "Labels"],
            tools=["Phone with the Deco app", "Velcro ties"],
            draw=["av", "power", "network"]),
    }
