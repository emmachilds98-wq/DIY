# v38 upgrade plan

Read `media-wall/HANDOFF.md` first (START HERE, then round 31). Never write the cap's poem out in code, text or commit messages
(round 31: it tripped the session's safety filter twice).

The client's brief (22 Oct 2026, after v37): change each wall's colour on its own; edit orientation and adjust the lights' individual
lamps; the stairs solid up to the landing (they clip); move the vinyl and the Xbox to the left of the media wall so the TV is more
central to the sofa, the games in line with the TV, the vinyl on the left with the player; make what's saved on the GitHub page the firm
version (the dining cabinet with the bar beside it) and fix the door hitting the plant shelf; cheap existing items in the build and buy
guides where possible, a full build where not; a better blanket basket; keep the storage shelves on the wall; a more unique storage
coffee table; everything fits and is accurate; keep the other options but don't HD-render them or write guides for them; slim the whole
thing down to what they need, using Claude Design to make the flow easier. Then: "include option to view ceiling Alcatrazes in
differing designs so we can decide if we want it in future" (item 12).

## 0. The client's answers, and two still open

1. **Your saved picks (answered, 23 Oct):** pasted from the 3D room's **Copy as a note**:
   - the tall lidded blanket basket at the sofa's open end (natural seagrass), £90–110
   - drawers in the bottom three steps (oak fronts), £180–320
   - two wall cabinets over the sofa's corner (walnut effect), £70–100
   - two oak alcove shelves in the window corner (oak), £70–110
   - two lidded boxes on your black shelf (white), £20–30
   - an oak shelf over the hall door with two lidded boxes (white), £35–60
   - a lift-top coffee table (oak effect), £39–80
   - the rug in sage stripes (Decor)

   Plus, from the brief, **the bar built in beside the dining cabinet**. "Your picks" doesn't list what stands beside the cabinet, which
   is why it isn't in the note; make Your picks name the beside choice too (item 11).
2. **"Edit orientation" (answered, 23 Oct):** "Turning the light fixture as a whole as well as the light heads": each fixture turns
   as a whole (the two spot bars on their ceiling roses, the red lamp on its base), and each head turns and tilts on its own (item 6).
3. **"The storage shelves on the wall" (answered by the picks):** all four stay: the alcove shelves, the wall cabinets, the shelf
   over the door and the boxes on your black shelf.
4. **One measurement for the media wall swap (open):** how far the socket on the side wall is from the alcove's back wall, and how
   high it is (it was "about 30 cm up, just in front of the Xbox game drawer"). The record trays would pull out beside it.

## 1. The firm version (the plan) and the options

- **The firm version** is the compact cabinet at 90 with **the bar built in beside it (D)**, made as in item 2; the media wall
  swapped as in item 3; **your picks above**; and everything already in the plan (the glass case, the storage ottoman, the plant stand
  in the window corner, your shelf 10 cm off the boxing). Each piece moves into `build_doc.TRACK` (with a `costs.SHORT` name), gets its
  build step and its fit rows in a counted zone, and leaves `ideas.SUGGEST` / `OPTION_GROUPS`. Where a pick and the brief overlap:
  - **The blanket basket:** you picked the Cotswold one and asked for a better one, so item 8's choice takes its place at the same spot.
    The Cotswold basket stays as the fallback.
  - **The coffee table:** you picked the Homelife lift-top and asked for something more unique, so item 9's table takes its place,
    with the lift-top as the fallback. Both fit the same 90 × 50.
  - **The step drawers:** built into item 4's solid stairs, sized to its risers. The stairs will change, so they're drawn on today's
    flight, and the build note says to have them made with the new stairs (each tread needs a bearer once its riser is cut).
  - **The rug, sage stripes:** today it's a decor colourway, not a product. Find a real flat-weave rug about 230 × 160 (the rug's
    place: x 100 to 330, z -198 to -38) in sage and cream stripes, with a source and a price for the buy list.
  - **The wall storage:** the alcove shelves sit over the plant stand (20.2 clear); the wall cabinets just past the PC shelf's end;
    the shelf over the door needs your architrave's height (CHECK); the boxes stand 1 over your black shelf's front.
- **The plan's total goes up** by about £600–1,000 for these, plus the rug, before item 8 and 9's swaps (worked out properly when the
  rows go into `TRACK`).
- **Options stay** in the 3D room as switches: the other three bars, the 80-wide table, the window corner's seat, bench and
  cupboard, the shoe cabinets, the hook rail, the other decor and so on. They get **no HD stills, no build steps and no plan pages**:
  one line each in a short "Other options" table (what, where, size, rough cost, source). The 3D room is how you look at them.
- `geometry.FIRM` (a dict of the picks) becomes the single source: export3d sends it, room3d.js opens on it (and **Reset to my plan**
  returns to it), build_doc and fit read it.

## 2. The dining cabinet and the bar: the door hitting the plant

**What's wrong (measured).** The table door is 90.5 wide and swings round its hinge at the cabinet's window end (x 443.45, z -178.65)
until it lies back over the wall beside the cabinet. In v37 your black shelf moved 8 cm towards the stairs to keep its 10 cm gap from
the boxing, and the hanging plant moved with it, to z -267. Its strands hang 26 cm off the wall, 88.4 cm from the hinge, so the door's
edge now sweeps through them. Before v37 they were 96 cm away and clear. v37 caused this.

**The fix (no new joinery):** let the strands hang **through the 10 cm gap** between the shelf's end and the boxing. That's what the
gap is good for, and the strands are then 102.6 cm from the hinge, 12 cm outside the swing. The pot sits at the shelf's very end, its
strands trained over the end, not the front.

**The bar (D), made to suit:** it currently runs right to the boxing, so it would sit under those strands. Shorten it to end flush
with the shelf's end: **42.5 wide** (z -233.5 to -276), leaving the 10 cm column from floor to shelf free for the strands. Bottles:
four across, two rows, two shelves = 16. Keep the counter at 90 and its 22.4 depth (1.0 behind the open door's line). Re-check the
glass rail (a 300 rail, three or four glasses) and the display shelf.

**Check every swing (new, see item 10):** the table door's arc and the chair door's arc against the bar (its counter, shaker, tray and
glasses), the plant stand (corner 1.3 clear of the trolley path today), the black shelf (the door's top edge 187 against the shelf's
underside 191), the strands in the gap, the lamp at the sofa's west end, and the chairs when they're out.

**Cheap first:** look for a ready-made carcass at most 22 deep and 42.5 wide for the bar's base: IKEA ENHET wall frames (15 deep,
30 or 40 wide), BESTÅ 60 × 20 frames (too wide unless cut), TRONES-type 18-deep units. A 70 cl bottle (35 tall) must stand in it.
If none fits, the full build stays (oak-faced ply, the v37 cut list resized), with its cut list, fixings and buy rows.

## 3. The media wall swapped: the TV central to the sofa

**Why it helps:** the TV's centre is at 67.75 from the side wall and the sofa's main run is centred at 135, so the screen sits 67 cm
to the side of the middle seat. Mirroring the wall (the turntable zone to the left, by the side wall, and the TV to the right, against
the breast's reveal) puts the TV's centre at **118.25, 17 cm off the sofa's middle**. That's as far as the 186 alcove allows.

**Above the worktop:** the left zone (0 to 50.5) takes the turntable on the worktop and the Series X on its oak shelf above (lid
clearance to 130, as now); an upright at 50.5 to 55; the TV between 55 and 181.5; the right upright becomes the corner post against the
breast. The record ledge over the TV, the high shelf, the LED grooves and the bias light move with the TV. The ledge that wraps onto the
side wall stays (check: the Series X's top at 170.6 near the corner, against LPs leaning on the wrap above 155).

**Below (the games in line with the TV, the vinyl on the left):** bay 1 (left, under the turntable) becomes the **LP crates**
(the two face-out record trays and the slim game column); bays 2 and 3 (under the TV) take the **consoles and the game drawer**
(Xbox One, 360 and the game drawer in bay 2; the PlayStations, the HDMI switch, the RetroTINK and the sub in bay 3). The sub stays at
the far end from the turntable, which is better for vibration. The soundbar re-centres under the TV.

**To check:** the side wall's socket against the record trays' pull-out (question 4); the cable channel's route (shorter HDMI runs; the
phono lead now at the far end from the soundbar's input); Deco B and the 6-way (the groove now in the right corner post); the Cat6 at the
alcove's right corner; the PC shelf and the oak run on the side wall; the viewing angle and the TV's height (unchanged at 116.5).

**This is the biggest job.** Everything starts in `geometry.py` (`UP_L`, `UP_R`, `RZ`, `TV_X`, `DECK_X`, `SX_X`, `BAYS`, `BAY_NAMES`), then
an audit for hard-coded x positions in `render.py`, `diagrams.py`, `make_images.py`, `instructions.py` (steps 6 to 10), `export3d.py`,
`room3d.js` (the TV picture, the drawers, the labels' anchors, `hotspots()`), `fit.py` (the bay zones), `build_doc.py` (the key table,
the cut list) and `scenes.py` (the bars' aims at the shelves). Do it on its own branch first, render the main HD view and the drawers,
then carry on.

## 4. The stairs: solid up to the landing

**What's wrong:** the flight is eleven separate treads on boxes. From above (Dolls' house, the whole room) the steps past the
ceiling line float with nothing under them, and the cutaway clips them in slices.

**The fix:** draw the flight as **one solid**: a stepped profile extruded across its 59 width, with closed strings on both sides (the
brick side wall below the string on the door side), up to **a landing at first-floor level** (13 risers of 19.5 = 253.5, against a
235 ceiling plus a floor of about 20: confirm the count). The stairwell's walls run solid to the landing; the landing is a floor slab
with the banister's newel. The cutaway leaves the stairs alone (or cuts them cleanly at the landing, with the cut face filled). The
nightlight idea, the step drawers and the hat peg follow the new numbers. The client has said the stairs will change, so this stays a
stand-in shape: say so in its card.

## 5. Each wall its own colour

**Today** one paint covers every wall; tapping a wall in Edit room repaints them all. **New:** the walls are named surfaces, each with
its own material: **the media wall** (the alcove's back and reveals), **the chimney breast** (its face and returns), **the door wall** (the
recess), **the stairs wall** (on up the stairwell), **the window wall** (and the window's reveals), **the PC wall** (the side wall) and
the pipe boxing (with the window wall unless split). `S.walls = {id: "match" | colour}`. Look gets **All walls** plus a row per wall (the
paints and Any colour); in Edit room a tap paints only that wall, with **Same as the others** to undo. The link and the saved
layout carry it. The plan's paint section and buy list work out each colour's area from the geometry (less the window and the
door) and the tins it needs (two coats).

## 6. The lights: each fixture and each lamp, turned and set on its own

**Today:** sliders per group (strips, uprights, bias, bar 1, bar 2, the red lamp), a colour per group; the bars are fixed "TV to
window" (since v15) and the heads aimed by the plan.

**New**, from the client's answer ("Turning the light fixture as a whole as well as the light heads"): tap a spot bar or the red
lamp and its card has two parts.

- **The fixture:** a **turn** dial for the whole fixture. Spot bar 1 and bar 2 turn on their ceiling roses (the 84 bar's ends sweep a
  42 circle), in 15° steps, or freely with a key held; the red lamp turns on its base, its three heads with it, and still moves in Edit
  room. **Reset** puts the fixture back to the plan's angle.
- **Each head:** on/off, brightness, colour and its **aim** (turn and tilt sliders, with a line on the floor showing where it lands; or
  drag the line). The bars' heads are adjustable on the real fitting (Dunelm Wolston: "adjustable heads"); the red lamp's three heads
  likewise.
- **Checks:** a turned bar must clear what's near it: bar 2 runs close to the stairs wall and its shelf, and over the table it lifts
  for dinner. The clash check (item 10) covers each bar's sweep circle at its height, with a warning on the card if an angle hits the
  wall, the shelf or the open table door. The plan's lighting section and its drawings say the bars' angles if they change from "TV to
  window".
- **The rules that stay:** the presets still set everything ("adjusted" shows when you've changed something); v35's fixed set of
  lights holds (off means turned down, a turn moves the fixture's group and its lights' targets), so the graphics card makes no new
  shaders (`qa.py` checks it). Stills, the saved layout and **Copy link to this view** carry every fixture's angle and every head's
  settings.

**Furniture too (an extra):** Edit room's selection gets the same turn dial (15° steps, free with a key held) beside ⟳ and 45°.

## 7. Cheap existing items first: the build and buy guides

For every built piece in the firm version (the bar, the coffee table, the shelves, the cabinet's fittings), the guide shows **"Buy this
and adapt it"** first: the product, its size and price with a source, and what to change (cut, re-face, add a top). It shows **"Build it"**
only where nothing fits: the cut list, the materials, the tools and the steps. The buy list gets one row per item with a link,
the price checked, and a "check before you buy" note where the size is unconfirmed. Retailer sites are blocked from this sandbox: take
sizes from search results, and ask the client for a screenshot where a listing can't be read.

## 8. A better blanket basket

**Brief:** five throws folded about 38 × 33 × 8, stacked about 40 high; at the sofa's open end against the side wall (about 45 × 45
of floor: check it against the bar C and floor-plant spots); a lid or a fold-over top so it looks tidy; handles; in natural or dark
weave to go with the oak and the navy; cheaper than the Cotswold basket (£99), which is plain and bulky.

**To look at (check sizes and lids on the listing):** Dibor's Lakelyn water hyacinth lined basket, large (59 high × 51 × 29, £42, lined,
no lid listed): it's taller and slimmer, so it takes less floor, with the throws standing on edge. Argos's cotton rope basket
(40 × 40 × 25, £14) is too low for five. Also worth finding: a lidded water hyacinth or rattan trunk about 50 × 35 × 45 that doubles as a
side table at the sofa's end. Pick one, and keep one alternative as an option.

## 9. A more unique storage coffee table

**The space:** the coffee table's spot is 90 × 50 (x 103 to 193, z -191 to -141), with only 10 cm to the sofa's front, 6 to the chaise
and 7 to the ottoman. So at most about 90 × 50, 45 to 50 high, and it must not grow towards the sofa.

**Recommended idea: a record-browsing coffee table.** An IKEA KALLAX two-cube unit (about 77 × 42, 39 deep: check the listing) laid on
its back on low castors, with an oak top about 90 × 50 overhanging it, and LPs standing in the two cubes (33 × 33, an LP is 31.4) to flick
through from the sofa: about 80 records, cheap, and on theme with your vinyl. A shallow drawer or a lift-up section of the top can hold
the remotes and the controllers. Alternatives to show as options: a vintage teak record coffee table (Mustard Vintage's was 120 × 44 × 60:
too big here, so only something like it at 90 × 50), or keeping the Homelife lift-top.

## 10. Everything fits: a clash check

New `fit.clash()`: every placed and built piece as a 3D box from `geometry.py` (the firm version, then each option on its own), plus
what moves: the two cabinet doors' swing arcs, the table and the chairs when out, the drawers and record trays pulled out, the trolley's
path, the ottoman's lid, the lift-top. It reports any overlap and any gap under 1 cm, and `qa.py` fails on one. It would have caught the
door and the plant. Every size in the firm version keeps a cited source (CLAUDE.md); re-check the v37 sources that came from search
results.

## 11. Slimmer: the page, the plan and the renders

**The page (the user flow).** First a design pass with **Claude Design** (an Artifact design canvas: today's screens next to the
proposed ones) for the client to approve before any code. The proposal to start from:

- The room opens on **your plan** (the firm version), with one **Try options** switch. Options show only while it's on, and **Back to my
  plan** puts everything back.
- Four dock buttons instead of six: **View** (cameras, the tour, the lights), **Room** (the layout and the options, grouped by place:
  the dining wall, the media wall, the sofa, the window corner), **Look** (each wall's colour, decor) and **Edit**. Menu folds into the
  page's own header.
- Extras' long lists (34 suggestions, 9 ideas, versions, picks) go. Each option lives in its place's group in Room, and Your picks
  becomes a small chip ("3 options on · £…") that opens the list.
- The sheets: **Plan**, **Build** and **Buy**. The Ideas sheet folds into Room.
- On a phone: no numbered labels by default, and one row of set-ups.

**The plan PDF:** the firm version only. Target about 45 pages (116 now). The history appendix and the "what changed" boxes from
earlier rounds leave the PDF (they're in HANDOFF and git), and the options become a 2-page table without stills. **The build guide**
covers only the firm version's steps.

**The renders:** HD stills for the firm version only, about 30 (104 now). `shot3d.SHOTS` gets a `firm` flag; option stills are dropped
from the plan and the page (the live 3D room shows them). This also cuts a full rebuild from about 25 minutes to under 10.

**The code:** remove what's unreachable since v33 (the flip-top, the sliding cabinet, site A and B paths) and the plant shelf's
leftovers; merge the static oak and instance repeats to cut draw calls (469 in Fast at 390 now; target 150 or fewer).

## 12. Ceiling designs to try (for later: an option, not the plan)

The client: "include option to view ceiling Alcatrazes in differing designs so we can decide if we want it in future". We've read this
as **Artex** (your ceiling is textured in your photos); confirm, or say what you meant. In Look, a **Ceiling** row shows each design
in the live 3D room, in any paint colour:

- **As it is:** your current textured ceiling.
- **Smooth:** skimmed flat (what most people do with old Artex).
- **Artex patterns:** stipple, swirl, fan and basket weave.
- **Feature ceilings:** oak-effect beams across the room; a shallow coffered grid; a recessed LED cove round the edge (the "LED coving"
  upgrade path for your ceiling strip, noted since round 4).

**How:** the textures are bump maps drawn on a canvas, swapped on the ceiling's material, so the graphics card makes no new shaders
(the v35 trick: the material always has a bump map; "none" is a flat one). The beams, coffers and cove are hidden groups, warmed up off
screen like the other options. Each design's card gives a rough cost and what it involves, each with a source (skimming over Artex,
asbestos testing first for a pre-2000 ceiling, faux beams, an LED cove kit), and the clash check makes sure the beams and cove
clear the spot bars, the rose and the door. **No HD stills or guide pages** (it's an option), except one comparison picture in the
plan's options table if you want it.

## 13. Order of work

1. `geometry.FIRM` from section 0's picks (ask the one open question, the socket, with the design canvas in step 6).
2. Item 10's clash check first, so every later change is checked as it's made.
3. Item 2 (the door and the bar), then item 3 (the media wall swap, on its own branch, the main view checked before carrying on).
4. Items 4, 5 and 6 (the stairs, the walls, the lights), then item 12 (the ceiling designs).
5. Items 8 and 9 (the basket and the coffee table), with sources and "buy and adapt" builds.
6. Item 11's design canvas to the client; after approval, the page and the slimmer PDF, guide and stills.
7. Rebuild, `qa.py` and `taptest.py` at 390 and 1280 plus the clash check, HANDOFF and README, then a PR into `main` and the merge.
