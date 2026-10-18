# Handoff: Home Network & Media Wall Plan

## Update 18 Oct 2026, round 5: v11 delivered (turntable back in the alcove, dining wall, side-wall wrap)
**Delivered:** `out/Home_Network_Plan_v11.pdf` (40 pages), `out/Build_Guide_v11.pdf` (8 pages, beginner-friendly, with tool list
and shopping list), HD renders in `out/` (v10 outputs in `out/v10/`), the viewer artifact
https://claude.ai/artifact/42PUQjJwfafV93mrjeFYX9 (update this one in place; it is the account this repo's sessions use) and
`index.html` at the repo root, the same viewer for GitHub Pages (Settings → Pages → deploy from this branch, root).
PR: https://github.com/emmachilds98-wq/DIY/pull/2 (contains v10's commit too). Note: an earlier session drafted v11 but never
committed it; this round rebuilt it from the client's agreed layout.

**The v11 layout (all numbers in `src/geometry.py`)**
- TV shifted 25.25 cm towards the side wall (centre 67.75). Left upright = corner post at x 0–4.5; right upright 131–135.5.
- Right-hand zone 135.5–186 (50.5): turntable on the worktop (AT-LP120X size, 2.65 each side, lid top ≈121), Series X on an
  oak shelf at 134 (underside 130), flush wedged tenons through the right upright (proud ones would touch the TV), 15 cm air
  each side, 21.4 above; phono preamp hung under the shelf at the back.
- Base: bay 1 Xbox, bay 2 PlayStation (unchanged), bay 3 = the two v9/v10 face-out record trays. Hidden slim drawer moved into
  the plinth under bay 2 (push to open). Sub under the dining wall between the Hebgo arms (x 232–262.4, on its side, driver east, oak riser) — round-5 feedback.
- Side wall: record ledge wraps the corner (7 deep, z 8 → −126, 4 LPs), then the PC shelf (82 × 28 at 155.4, z −130 → −212)
  over the end of the L-sofa; cane screen, pad dock, trunking down to the skirting. No keyboard tray (over the sofa).
- Dining wall on the breast: oak backboard 110 × 22 × 3, a 110 × 80 × 2.7 oak top on three lift-off hinges, two Häfele Hebgo
  287.43.428 brackets 80 apart. Folded: ≈7 cm deep, top edge 153.3. Four at the wall; six lifted off onto Emuca 710 legs
  (table at x 255–365, z −60…−140); eight with a 60 × 80 leaf (x 220–390). Clearances checked in `fit.py`.
- Spot bars on the client's two existing ceiling points: bar 1 straight out from the TV unit halfway to the sofa (93, −106); bar 2 between the door and the west wall (433, −80, to confirm; just out of the render's frame). Dimmers only, no new point. Table: pegged 7 cm breadboard ends, 5 cm radius corners, oak or Emuca legs. Double socket: left → 10-gang (always on),
  right → retro 6-way, so the wall switch is the retro switch. New socket behind the sofa for the PC and rears.
- L-sofa assumed 247 × 168 × 80 (M&S Easy Velvet corner size) with the return along the side wall; **ask for the real size**.
- Records: ~188 LPs (180 trays + 4 + 4) and ~240 singles face-out (v10 had 234/350 with the browser and singles drawer).
- Fit proof: 52 checks, 40 fit, 8 tight, 4 check on site, none fail.

**Code**
- `render.py`: camera moved to EYE_X 120; new `rz_shelf()`, `series_x()`, `wrap()`, `dining_wall()` (DINING "folded"/"four"),
  `chair()`, `table_settings()`, `subwoofer()`, `spot_bar()` (two bars), `sofa()` (see-through; off by default, it read as
  if in front of the base). The key numbers itself (`_numbered`).
- `diagrams.py`: `_room()`/`_sofa()`/`_side_wall()` helpers; new `seating()`, `dining_section()`; v11 `front`, `section`
  (A TV, B turntable zone), `routes`, `pc_shelf`, `sound`, `power`, `living_plan`, `why_layout` (what moved in v11).
- `build_doc.py` writes `plan.html` + `guide.html` and both PDFs. `build_viewer.py` writes the viewer and `../../index.html`.
- `make_images.py renders` skips the diagrams (handy mid-edit). Backups: `*_v10_backup.py`.

**Questions for the client (ask together)**
1. The L-sofa's size, and that its return runs along the side wall.
2. The door to the hall: which side it hinges, and does it open into the room? (The dining chairs on that side sit in its swing.)
3. Models: turntable, PC case, Series X fan stand.
4. Chairs: theirs, or four folding ones? Where do the leaf and the legs live?
5. Are the side wall and the chimney breast solid or plasterboard?
6. Roughly how many LPs and singles? (Capacity fell to ~188 / ~240.)
7. Still open from v10: the west end sizes, the 23 × 22 box, wired ports for the projector and music room.

---

## Update 18 Oct 2026, round 4: v10 delivered (drawn to the measured room)
**Delivered:** `out/Home_Network_Plan_v10.pdf` (34 pages, restructured: plan on a page → room → media wall + fit proof →
vinyl corner → joinery → paint and light → power/cables/network → build guide → buy list → confirm/sources; slat wall
in an appendix), HD renders in `out/` (v9 outputs moved to `out/v9/`), and the viewer page rebuilt from `src/art/`.

**What changed in the code**
- `src/geometry.py` (new) holds every dimension; `render.py`, `diagrams.py`, `fit.py` and `build_doc.py` read from it.
  Change a number there and rebuild: `python3 make_images.py && python3 build_doc.py && python3 build_viewer.py`.
- `src/fit.py` (new) is the fit proof: 39 checks with numbered sources (34 fit, 1 tight, 2 check on site, 2 don't fit).
- `src/render.py` was rebuilt for the real room: `P()` now honours `XOFF/YOFF/ZOFF` via `place(dx, dy, dz, fn)`, and
  `box()` culls faces in world coordinates. New: `vinyl_cabinet()`, `singles_drawer()`, `browser()`, `deck()`,
  `breast_frames()`, `side_shelves()`, the recess and door in `room()`. The v9 drawings of consoles, trays and the
  game drawer are unchanged. Backups: `render_v9_backup.py`, `diagrams_v9_backup.py`, `build_doc_v9_backup.py`.
- New diagram `why_layout()`; `living_plan()`, `house()`, `front()`, `section()` (now A alcove + B vinyl cabinet),
  `routes()`, `network()`, `sound()`, `joints()` and `drawer()` redrawn for v10.

**Design decisions taken this round (all in the plan)**
- Alcove: uprights at 25.25–29.75 and 156.25–160.75, TV gap 126.5, side zones 25.25 (Series X left, pad dock right).
  Base 3 + 60 + 60 + 60 + 3: BESTÅ bays 1–2 on the 9 cm plinth, bay 3 a ply carcass for the sub (sub 2 cm forward of
  v9's spot: 11.6 cm behind it for the rear port), hidden slim drawer 56.4 wide. Base 46 deep (40 + 4 channel + 2 face
  frame), 8 cm proud of the breast; the vinyl cabinet's oak end panel covers that step.
- Heights: worktop 76; side shelves 156 both sides; ledge 155.4; high shelf moved to **196** (39 cm to the 235 ceiling,
  5.5 cm above the ledge LPs).
- **Joinery fix:** the side shelves' through-tenons now sit 12 and 20 cm from the wall (6 wide), clear of the ledge's
  7 cm housing. In v9 they collided with the ledge housing (hidden by draw order).
- Vinyl cabinet 100 × 44 × 76 at x 186–286, tight to the reveal, 17.5 cm short of the breast's west corner. Bay A:
  the two v9 trays. Bay B (40): preamp cubby over a new face-out singles drawer (~110). Top: browser left, deck right
  (AT-LP120X size allowed), breast clear to 130, two LP frames from 150. Totals: ~234 LPs, ~350 singles, all face-out.
- Spot bar on the rose at x 186, 173.5 from the window: pink head now aims at the vinyl cabinet; lowest shade 212.6.
- PC shelf moved 20 cm towards the alcove (z −110 to −175) to clear an assumed 2.0 × 0.95 m sofa.
- Deco A + Switch 1 in bedroom 3; optional Cat6 to the master (projector) and bedroom 2 (music room).
- Series X fit is **tight** on the sides (5 cm vs Microsoft's recommended 10–15 cm); offered option: shift the TV and
  uprights 5 cm right (left zone 30.25, right 20.25).

**Questions sent to the client (await answers before v11)**
1. OK to move the vinyl corner to the oak cabinet on the chimney breast?
2. Where does the door hinge, and which of 935 / 1045 / 660 / 820 are the recess, door and stair box?
3. Models: turntable, PC case, Series X fan stand; the 10-gang's length.
4. What's the 230 × 220 box in the window corner?
5. Wired ports for the projector and the music room?
6. Keep the TV centred, or shift it 5 cm right to give the Series X more air?
7. Sofa size (the plan assumes about 2.0 × 0.95 m) and where the rear speakers can go.

**Viewer artifact:** the old viewer link (9cB8xgi6Pt22gT4GUNNQEk) couldn't be opened from this account, so v10 was
published as a new viewer artifact: https://claude.ai/artifact/D9y2P2ve6WveMJwyWrTNLQ (built from `src/media_wall_viewer.html` + `src/art/`). Update that one in place next time. The client's "Media Wall Build
Tracker" artifact (4sWMHkRn3XhmwqJgG7NU3x) is still the first-round version (225 × 220 × 50); offered to refresh it.

---

# Earlier brief for v10 (kept for reference)

**Read this first.** The client (Emma, with Dave) has now sent an accurate hand-measured sketch of the living room
(`inputs/room_sketch_accurate_mm.png`). It changes the core geometry: everything since v6 assumed an alcove
225 × 50 cm with a 220 cm ceiling. The real alcove is **186 × 38 cm** and the ceiling is **235 cm**. Your job is
to produce the final, accurate plan (v10): re-fit the design to the real room, prove every item fits using
researched dimensions with sources, re-render in HD and restructure the PDF so it reads as one flowing plan.

The client iterates fast in short messages, reads renders closely, and wants complete deliverables each round:
the PDF plan, HD renders (labelled), and the viewer artifact updated in place. Keep their words: "face-out",
"spine-up", "artisan oak", "tray".

---

## 1. The real room (from the sketch, all mm; sketch is not to scale, trust the numbers)

Orientation used throughout (matches the agent's plan, north at the top of `inputs/agent_floor_plans.png`):
the **window wall is north**, the **media wall is the south wall** (shared with hall and garage), east end has the
TV alcove, west end has the stairs box and the door to the hall.

| Item | Size / position |
|---|---|
| Room | 4670 (east–west, along the window) × 3470 (north–south, window wall to the alcove's back wall) |
| Ceiling | 2350 |
| Skirting | 60 high × 20 thick (white now; recommended painted to match, eggshell) |
| Window (north wall) | 2350 wide, starting 730 from the east wall |
| Radiator (under window) | 1370 long, ending 130 inside the window's west end (≈ 1580–2950 from the east wall) |
| Small box in the NW corner | 230 × 220, probably pipe boxing (ask) |
| **TV alcove** (south wall, east end) | **1860 wide** (east wall → chimney breast) × **380 deep** (breast projection), floor to ceiling 2350 |
| **Chimney breast** | **1175 wide**, projects 380 (390 on its west side) into the room |
| West recess (breast → stair box) | about 1045 long × 390 deep |
| West end | stair box / bulkhead (hatched in the sketch, ~820 × ~660) and the doorway; dims 935 / 1045 / 660 / 130 / 820 / 140 are ambiguous, **ask before relying on them** |
| Bottom (west) wall | 2680 from the window wall to the stair box |

Confirmed by the client's photos (`inputs/photo_current_living_room.png`, `photo_listing_living_room.png`): the TV sits
in the alcove on the right when facing the east end, with the breast's reveal at its right; the LED strip is stuck to the
**ceiling** round the whole room, facing down (`photo_ceiling_led_strip.png`); the existing ceiling rose is mid-room.
The client said the ceiling light hangs "where the alcove starts on the right, in the middle of the room" →
rose ≈ 1860 from the east wall (in line with the breast reveal), ≈ 1735 from the window wall.

Socket: single wall socket, about 30 cm up, **on the east (side) wall just in front of bay 1** (the client: "just in front of
the xbox game drawer, raised off the ground"); becoming a double. Feeds the 10-gang and the 6-way.

House (agent plan + client):
- Lower ground: kitchen 3.79 × 3.66; brick cupboard in the middle of the kitchen's back (south) wall, probably the base of the chimney breast above; Deco C goes on its outside, up high.
- Ground: living room (above), hall + stairs (west), garage (east, under master bedroom).
- 1st floor: **bedroom 3 has the gaming PCs and the Virgin Hub 5** (so Deco A + Switch 1 live there); **bedroom 1 (master) has a projector**; **bedroom 2 is the spare room / planned music room** (sloped ceiling, low at the back/north wall); bathroom also sloped. Airing cupboard (off the landing) sits over the alcove's corner: use it as the Cat6 riser.
- New network implications to add: Cat6 route from bedroom 3 across the landing to the airing cupboard; consider spare Switch 1 ports for the projector (master) and the music room (bedroom 2); Wi-Fi for bedroom 2's slope.

## 2. What the client has chosen (keep)
- **Artisan oak build is the main plan** (oak uprights, wedged through-tenons, pegged housings, record ledge above the TV, oak face frame, solid oak worktop, cane PC screen). Slat wall stays only as a short alternative.
- **Paint: Farrow & Ball Card Room Green No. 79**, colour-drenched; skirting/door/trunking in the same colour, Estate Eggshell (Modern Eggshell if it takes knocks). Darker skirting option: Green Smoke.
- **Ceiling light: four-head cone spotlight bar in the style of Dunelm Elements Wolston** (`inputs/spotlight_bar_style_wolston.png`: white bar, cones in sage / pale blue / mustard / dusty pink, light-wood toppers). Verified: £49, 84 × 16 cm, 22.4 cm drop, E14 6 W max, adjustable heads, dimmable with compatible LEDs, IP20.
- **Every record face-out** in thinner trays: 9 mm sides, 12 mm base, 6 mm oak divider, 5 cm × 15 mm oak lip; LP trough 32.6 + singles trough 18.9 face-out; ~90 LPs + ~120 singles per tray; 400 mm runners 68–70 kg; one tray open at a time; anti-tip brackets.
- Game drawer (bay 1): 2 face-out bins + tray, spine-up rows behind, ~48 games, 350 mm runners.
- Existing LED ceiling strip stays (upgrade path: channel + diffuser, or LED coving); LED grooves in the uprights; bias light behind the TV.
- Deco B on the high shelf, powered from an always-on 6-way socket via a groove routed in the back of the right upright; Cat6 in through the ceiling at the alcove's right corner.
- Network/AV/power plans from earlier versions stand (Hub 5 modem mode, Deco A router, 8-port switches, Cat6 star, eARC to the Hisense AX5100G, RetroTINK-6X CE, 10-gang side A always-on / side B retro).
- Later idea: "Dave and Emma's watch log" (keep under Later ideas).

## 3. The re-fit: what has to change, and the recommended answer

The old wall was 225 wide (Series X zone 44.5 | upright | TV 126.5 | upright | turntable zone 45) over a base of
3 × 60 bays + 45 sub bay. It no longer fits 186. Work it through and present the reasoning in the plan.

**Recommended layout (my analysis, verify the arithmetic):**

Above the worktop, inside the alcove (186):
- Keep two oak uprights framing the TV, 4.5 thick, 2 cm clear of the 122.2 cm screen: inner gap 126.2–126.5, so the two side zones total ≈ 50.5 → ≈ 25 each if symmetric.
- **Left zone: Xbox Series X on its fan stand** (stand ≈ 20.5 square, console 15.1 × 15.1 × 30.1): ≈ 2.4 cm each side. Microsoft's only stated requirement is **≥ 4 cm clear above** the console on an open stand (Pure Xbox article), so this works with open air above (left shelf at 156 leaves plenty). Optionally offset the TV a few cm right to give the Series X more side room.
- **Right zone (~25): no turntable fits here any more.** Use it for a small display/controller dock; Deco B sits above it on the high shelf.
- Record ledge between the uprights (126.5 long, 4 LPs = 125.6, snug), left and right shelves at 156 (through-tenons), high shelf: with a 235 ceiling, top at about **200** (books up to ~30 cm, 35 cm to the ceiling) or keep 192; uprights ≈ 159 long (76 → 235).

Below the worktop, inside the alcove (186 = 3 + 60 + 60 + 60 + 3 fillers):
- Bay 1 BESTÅ: Xbox One, Xbox 360, game drawer (unchanged rows).
- Bay 2 BESTÅ: PS3, PS2 + HDMI switch, PS1 + RetroTINK (unchanged rows).
- **Bay 3 (ply carcass, open): subwoofer on its riser at the bottom, shelf above (controller dock / spares), hidden slim drawer under the worktop, 6-way at the back.** Sub under the TV is good for sound and far from the turntable.
- Depth: BESTÅ frames are 40 deep. With a 4 cm cable channel behind (flat two-compartment trunking; the TL-SG108 switch stands on edge) and a 2 cm oak face frame, the base front sits ≈ 46 from the back wall, **≈ 8 cm proud of the breast face (38)**; finish the exposed 8 cm return at the reveal end in oak. Worktop ≈ 186 × 42–46, top 76. (Alternative: custom 36-deep carcasses flush with the breast, but the record trays and game drawer then don't fit; explain why it was rejected.)
- Plinth 9 cm under bays 1–2 as before; TV centre stays ≈ 116.5.

**The vinyl corner moves to the chimney breast face (1175 wide):** a matching oak cabinet ≈ 100 wide × 44 deep × 76 high standing against the breast, west of the alcove:
- Bay A (60, ply carcass): the **two face-out record trays** (unchanged design, 400 mm runners, box 53.9 × 40).
- Bay B (~40): phono preamp, stylus, brush, cleaning kit, spare inner sleeves; overflow singles.
- On top: the **turntable** (allow up to 45 × 35, AT-LP120X as worst case) and the **LP browser** (44 × 24, ~50 LPs face-out) side by side (89 cm + gaps within 100).
- Keep 40 cm clear above the deck for the lid (nothing on the breast face below ~130 cm); above that, a framed print or LP frames.
- Check the door swing at the breast's west jamb clears the cabinet's west end (ask the client where the door hinges).
- Totals become: about 180 LPs in trays + 50 in the browser + 4 on the ledge ≈ 234 LPs, all face-out; ≈ 240 singles face-out in trays (the old 70-single kit shelf is gone unless bay B takes them).

Alternatives to mention briefly (and why rejected): turntable on a shelf in a narrow right zone (too narrow);
Series X inside a base bay (horizontal; loses the fan stand look, takes a bay); TV off-centre with one upright.
**Raise the decision with the client in one line** at the top of the plan and in your reply: the vinyl corner moves
to the breast because the alcove is 39 cm narrower than assumed.

Viewing: sofa against the window wall opposite the TV (it will sit in front of the radiator, leave 10 cm). Eyes ≈ 0.65 m
from the window wall; screen ≈ 3.47 − 0.38 + (TV set back ≈ 0.25) → eyes-to-screen ≈ 2.6–2.7 m. 55" ≈ 26° wide at that
distance; TV centre 116.5 ≈ 2–3° above seated eye height. 65" (≈ 145 wide) would not fit between the uprights.

Spotlight bar: on the existing rose (≈ 1860 from east wall, ≈ 1735 from window wall), parallel to the media wall;
with the **235 ceiling** the lowest shade sits ≈ 212 cm (headroom is no longer a concern; update the text).
Back two heads (sage, blue) on the shelves/ledge, front two (mustard, pink) on the room; none at the TV.

## 4. Verified dimensions so far (cite these in the fit-proof section)

| Item | Size | Source |
|---|---|---|
| LG OLED C6 55" (OLED55C6) | 122.2 W × 70.4 H × 4.6 D cm without stand; 75.7 H × 23.1 D with stand; stand 47 cm wide; 14.1 kg / 15.9 kg; VESA 300×200; 4× HDMI 2.1, 1 eARC | cinemaconfig.com/products/tv/lg-oled55c6pua |
| Hisense AX5100G soundbar | 92 W × 6 H × 9 D cm | Euronics HISAX5100G page (sub and rears not listed: earlier plan used sub 21.4 × 30.4 × 29.4 from the Hisense USA spec sheet; re-verify) |
| TP-Link Deco X1500 | 11 × 11 × 11.4 cm | Laptop Outlet Deco X1500 3-pack page |
| Xbox Series X | 15.1 × 15.1 × 30.1 cm; Microsoft: ≥ 4 cm clear above on an open stand | Wikipedia (earlier); purexbox.com 2020 article quoting Microsoft |
| IKEA BESTÅ frame 60×40×64 | 60 W × 40 D × 64 H; 20 kg per horizontal surface | ikea.com BESTÅ frame 10247379 |
| Dunelm Wolston 4-light bar | 84 W × 16 D × 22.4 H cm, shades 15 cm, E14 6 W max | dunelm.com product 1000189449 |
| Consoles (from the v6–v9 plan's Sources, re-verify quickly) | PS1 27.0×18.8×6.0; PS2 fat 30.2×18.3×7.8; PS3 fat 32.5×27.4×9.8; Xbox 360 orig 30.9×25.8×8.3; Xbox One orig 33.3×27.4×7.9 | Wikipedia comparison pages, Neowin |
| Media | LP sleeve 31.4 cm (12⅜"); 7" sleeve 18.3–18.4 cm; DVD/PS2/360 keep case 19 × 13.5 × 1.4; Xbox One case 17 × 13.5 × 1.1–1.2 | earlier Sources (videogamecasesize.info, Walvis, Wikipedia keep case) |

Still to research and cite: RetroTINK-6X CE size (earlier plan reserved 23 × 23 × 8, search results didn't give it; check retrotink.com), TL-SG108 (15.8 × 10.1 × 2.5 cm, verify on tp-link.com), Hisense AX5100G sub and rear sizes (Hisense spec sheet), AT-LP120X(USB) size (45 × 35.2 × 15.7, verify), original Xbox One and 360 power bricks, a typical 5-in-1 4K HDMI switch, PS3 controller basket. Ask the client for: the turntable model, the PC case model, the 10-gang's length, the Series X fan stand model.

## 5. Restructure the PDF so it reads as one flowing plan (v10)

Current v9 has grown by accretion (47 pages, network first, tracker on page 2, sections added round by round). Reorder:

1. **The plan on a page**: one render, the 6–8 key decisions, total cost, what's still to confirm.
2. **The room**: accurate floor plan of the living room (redraw `diagrams.living_plan()` from the sketch: 4.67 × 3.47, alcove 1.86 × 0.38, breast 1.175, window, radiator, socket, rose, sofa, door/stair box) + the house plan (`diagrams.house()`; move Deco A to **bedroom 3**, label rooms: master/projector, bedroom 2/music room).
3. **The media wall**: renders (HD, labelled, full key), the front elevation to scale (`front()`), side section (`section()`), and **the fit proof**: one table per zone with item size (sourced), space, spare, pass/fail; plus a "why this layout" box (the 186 vs 225 story, vinyl corner on the breast).
4. **The vinyl corner**: record trays (keep v8/v9 tray section, diagrams), turntable, browser, preamp.
5. **Joinery**: joints diagram, joinery cut list, finishing.
6. **Paint and light**: Card Room Green, skirting, LED strip + upgrades, spotlight bar (aim, bulbs, dimmer), upright grooves, bias light.
7. **Power, cables and network**: socket double, power map, cable routes, the Deco/Cat6 plan for the house (including projector + music room ports), AV routing, settings.
8. **Build guide**: materials, tools, order of work (one sequence across electrician → paint → base → joinery → vinyl cabinet → lighting → connect).
9. **Buy list / tracker**: grouped by phase with totals; keep "paid" column.
10. **Still to confirm, later ideas, sources.**
Remove the slat wall to a half-page appendix. Avoid repeating the same facts in several sections; link by section name.

## 6. Renderer work (`src/render.py`)

All geometry is hard-coded for 225/50/220. Do a proper parameter pass rather than patching:
- Constants: `ALC_W = 186`, `ALC_D = 38`, `CEIL = 235`, `BREAST_W = 117.5`; recentre the camera (`EYE_X` ≈ 140 so the alcove and the breast cabinet both show; `X0`/`S` as needed), keep `SHIFT` so the ceiling and spot bar show (bar at x ≈ 186, z ≈ −136 from the breast face).
- Rewrite `room()` (alcove back at z = 38, reveal at x = 186, breast face z = 0 from x 186 to 303.5, west recess beyond), `unit()` (3 bays + fillers, bay 3 = sub bay; base front at z ≈ −8, exposed oak return at the reveal), `uprights()` (positions 25.25–29.75 and 156.25–160.75, height to 235), `high_shelf()`, `left_shelf()` + mirrored right shelf, record ledge, `worktop_items()` (Series X in the left zone; soundbar 92 wide centred under the TV at x ≈ 93), TV centred at x 93, `ceiling_leds()` (follow the alcove, reveal and breast face), `pendant()` (spot bar), `services()` (socket on the east wall, routes), `wall_socket()`, dimensions/callouts/key (`JOIN_KEY`).
- New `vinyl_cabinet()` against the breast face (x ≈ 190–290, z −44..0) with the two `record_tier()` trays (reuse as is, re-based on x), turntable and browser on top (reuse `turntable()` parts), preamp bay.
- Skirting 6 cm high now (was 10); colour via `SKIRT`/repaint.
- Keep `MAIN_PAINT = "card_room"`, oak grain filters, plates (escape `&`), HD export via `shot.py` at scale 2.2.
- Back up first (`render_v9_backup.py` etc.). The `render_v*_backup.py` files are older stages.
- Gotchas: `P()` breaks for z ≤ −505; `box()` face culling depends on `EYE_X`/`EYE_Y`, so recheck side faces after moving the camera; `repaint()` only maps the hexes listed in `PAINT_OLD`; build() wraps the scene in `translate(0, SHIFT)`.

## 7. Diagrams (`src/diagrams.py`) and doc (`src/build_doc.py`)
- Update to the real dimensions: `front()`, `section()`, `routes()`, `drawer()` (unchanged trays, new location), `living_plan()`, `house()`, `power()` (socket on the side wall), `network()` (Deco A in bedroom 3; optional ports to master/projector and bedroom 2).
- Add a fit-proof table generator (item, source, size, space, spare) so numbers stay consistent.
- `build_doc.py` builds HTML then the PDF via Playwright (`python3 build_doc.py`); new text sections live in `src/parts/*.html` (already spliced into build_doc.py; edit build_doc.py directly or restructure into parts). Change the output to `Home_Network_Plan_v10.pdf`.
- Viewer artifact (claude.ai artifact 9cB8xgi6Pt22gT4GUNNQEk) is built from `src/media_wall_viewer.html` with images in `src/art/` (regenerate per style × paint). Update it in place.

## 8. Open questions for the client (ask together, briefly)
1. OK to move the turntable and record trays to an oak cabinet against the chimney breast (alcove too narrow for both)?
2. Where does the door hinge, and what exactly are the stair box dims at the west end (935 / 1045 / 660 / 820)?
3. Turntable model, PC case model, Series X fan stand model, 10-gang length.
4. What's the 230 × 220 box in the window corner?
5. Should the projector (master) and music room (bedroom 2) get wired ports?

## 9. Files
- `inputs/` client sketch, floor plans, photos, the Wolston style photo, and the v7 oak render they liked.
- `out/Home_Network_Plan_v9.pdf` latest delivered plan (geometry superseded); `out/*.png` latest renders.
- `src/` all code: `render.py`, `diagrams.py`, `build_doc.py`, `doc.css`, `shot.py`, `parts/`, `art/`.

---

# Earlier handoff notes (history)

## Update 18 Oct 2026, round 3 (version 9 delivered)
- **Paint: Farrow & Ball Card Room Green No. 79** (`MAIN_PAINT = "card_room"`), skirting to match in Estate Eggshell; darker option Green Smoke (approximate colour in `skirting_options.png`).
- **Ceiling light: 4-head cone spotlight bar** in the style of Dunelm Elements Wolston (£49, 84 × 16 cm, 22.4 cm drop, E14 6 W max, adjustable). `pendant()` now draws it (`SPOT_HEADS`: sage/blue aimed at shelves, mustard/pink into the room) on the existing rose at x 225, z -170, parallel to the media wall. Canvas widened to W = 1900 so the whole bar fits.
- **Socket:** on the side (left/east) wall just in front of bay 1, ~30 cm up (`wall_socket()`), single → double; leads enter via a notch in the face frame's bottom rail at the left end and run back through the plinth. Option: electrician moves it into the alcove.
- **Floor plans received** (haart Medway, Portsmouth Close). Living room 4.95 × 3.65; alcove at the east end of the south (hall/garage) wall; chimney breast drawn ~85 cm wide x 1.85–2.70 (to confirm); kitchen brick cupboard under it; airing cupboard on the 1st floor sits over the alcove's right corner = Cat6 riser for both runs; Deco C on the outside of the brick cupboard. Sloped ceilings in bathroom + bedroom 2 (low at the back/north wall). `diagrams.house()` and `diagrams.living_plan()` added; eyes-to-screen ≈ 2.7–3.2 m depending on whether 3.65 is to the breast or the alcove back.
- Photos: LED strip is on the ceiling round the room; existing rose mid-room.
- Plan builds to `out/Home_Network_Plan_v9.pdf`. Viewer artifact updated (v3).

---

For the next agent picking this up. Read this first, then `src/build_doc.py` (plan text) and `src/render.py` (renders).

## The client and the project
- UK house (Europe/London). Living room alcove media wall + whole-house Deco mesh network.
- Deliverable is a PDF plan (built from HTML with headless Chromium) plus concept renders (SVG → PNG).
- The client iterates fast, in short messages, and wants a full updated plan + renders each round. Keep their words: "face-out", "spine-up", "artisan oak", "less clad".

## Current state (where I stopped)
| Item | State |
|---|---|
| `out/Home_Network_Plan_v6_1.pdf` | Latest plan. Change log removed (client asked). **Text and its embedded renders still describe the v6 geometry: worktop at 67 cm, one spine-up record drawer.** |
| `out/Media_wall_render_v7_raised*.png` | **New raised design (v7)**, slat-wall version, with and without numbered key. Not yet in the PDF. |
| `out/Media_wall_render_v7_artisan_oak*.png` | v7 raised design, artisan oak joinery version (client asked to "improve less clad wall design"), with and without key. Not yet in the PDF. |
| Rightmove floor plan | Client sent https://www.rightmove.co.uk/house-prices/details/907eb9f6-da61-4d2d-95fe-145d9842ca5a . WebFetch is blocked by robots; do not work around it. **Ask the client to attach a screenshot of the floor plan.** They say it's rough: it misses the alcoves, a brick cupboard in the bottom middle of the kitchen, and sloped ceilings in the first-floor bathroom and bedroom 2. |

## Next tasks, in order
1. **Update the plan text to the v7 raised geometry** (spec below) and swap in the v7 renders. Every height above the worktop moves. Search `build_doc.py` for: `67`, `66.8`, `104`, `108`, `100 cm`, `150`, `190`, `140 LPs`, `spine-up`, `350 singles`, `193`, `190 LPs`, `record drawer`, `225 × 40 × 2.8`, `BESTÅ frames` (bay 3 is now a custom carcass), the fit-check table, the storage table, the build guide cut list and order of work, the tracker (add plinth + bay-3 carcass + second record drawer; remove singles step), and `diagrams.py` (`front()`, `drawer()`, `section()`, `routes()`, `power()` use old heights).
2. Replace the "All records face-out: what it would take" section: it is now the plan, not an option. Keep a short note on the trade-off (TV ~9 cm higher).
3. Update the artisan oak section with the v7 joinery render + key (`JOIN_CALLOUTS` in `render.py`) and the new details: wedged through-tenons, oak pegs, record ledge above the TV (4 LPs face-out), LED grooves in the uprights, cane-panel PC screen, solid oak 3 cm worktop. Consider a joint-detail diagram and a joinery cut list.
4. When the floor plan arrives: room sizes, sofa-to-TV distance (check TV centre ~116 cm is OK), Cat6 routes between floors, Deco C placement (kitchen brick cupboard), sloped ceilings. Add a house plan diagram to the Network section.
5. Rebuild, check every page visually (contact sheets), deliver PDF + renders.

## v7 raised geometry (source of truth: `src/render.py`)
- **Why:** client wants every record face-out, which needs two stacked face-out drawers in bay 3. Each tier needs 34.7 cm (0.5 gap + 1.8 base + 30.9 sleeve leaning 10° + 1.5 finger room) → 69.4 cm inside → 72.6 cm carcass. Rounded to a 9 cm raise (`RAISE = 9.0`).
- **Bays 1–2:** IKEA BESTÅ 60×40×64 frames (back panels off) on a **9 cm plinth** → tops at 73. Contents unchanged inside, all +9 cm (game drawer, Xbox One/360, PS1/PS2/PS3).
- **Bay 3:** custom 18 mm ply carcass 60 × 40 × 73 from the floor, inside 56.4 × 69.4. Runners screw straight into the ply sides (no liners).
  - Lower record drawer: box underside 2.3, base top 4.1, sleeves to 35.0; lip 2.3–8.8.
  - Upper record drawer: box underside 37.0, base top 38.8, sleeves to 69.7; top panel underside 71.2; lip 37.0–43.5.
  - Each box 53.9 × 40 outside, 51.5 inside: LP trough 33 wide on the left (face-out, 10° lean, ~85 LPs, 90 packed tight), 1.2 divider, 16 cm compartment on the right for 7-inch singles spine-up (~60 per drawer) + inner sleeves. 400 mm full-extension runners (45 kg+; 68–70 kg pair preferred). ~30 kg per full drawer; open one at a time; anti-tip brackets essential.
- **Sub bay (180–225):** open from the floor. Sub on 5 cm riser on the floor (top 34.4). Kit shelf underside 37 / top 38.8 (preamp, stylus, cleaning kit, brush on the left; ~70 singles spines-out on the right). **Hidden slim drawer** under the worktop: oak front 44 × 7.4 at 65.6–73, box 40 × 28 × 6, 250 mm runners, finger pull underneath.
- **Face frame:** full width 0–73; openings bays 1–2 from 11.6 (bottom rail covers the plinth), bay 3 and sub bay from 2.6; top rail 71–73. Green eggshell (slat version) or oak (joinery version).
- **Worktop:** 225 × 40, top at 75.8 (laminate 2.8) or ~76 (solid oak 3.0, joinery). 10 cm cable slot behind (5.4 with slats).
- **Above the worktop:** TV on LG stand, centre ~116.5 (bottom 81.2, top 151.7). Soundbar 75.8–81.8. Series X to 112.4. Turntable shelf top **113** (`TT + RAISE`), LP browser underneath (33.2 clear), lid opens to ~165. Left shelf top **156**. High shelf top **192** (moved +2 so the joinery record ledge fits; books up to 26 cm, 28 cm to the 220 ceiling).
- **Joinery version:** oak uprights 4.5 × 30 at x 44.5–49 and 175.5–180, worktop to ceiling. Record ledge between them: underside 153, top 155.4, 7 deep, 1.5 lip; LPs to ~186.5 under the high shelf (underside 188). Turntable shelf 45 wide (180–225); left shelf 44.5 wide.
- **Vinyl totals, v7:** ~170 LPs face-out in bay 3 + ~50 in the browser = **~220 LPs, all face-out** (joinery adds 4 on the ledge); ~190 singles (120 in drawers + 70 on kit shelf).
- **Unchanged:** PC shelf on the left wall (top 110, glass to room, slatted/cane screen, keyboard tray), power plan (10-gang behind TV: side A always on, side B retro switch; 6-way switched for Deco/switch/turntable/preamp/RetroTINK), AV routing (all sound to Hisense AX5100G via eARC; vinyl AUX, PS2 optical, phones BT), network (Hub 5 modem mode, Deco A router, 8-port switches up and down, Cat6 star), colour drench in deep green, PS1 games stored outside the unit.

## Client decisions so far (keep)
- Room colour-drenched in the alcove's deep green; alcove 225 wide, ~50 deep, floor to ceiling (assumed 220 cm, to confirm).
- Game drawer (bay 1): PS2/Xbox 360/Xbox One; 2 face-out bins + tray at the front, spine-up rows behind, 350 mm runners, ~48 games.
- No tapestry stage: slat wall, face frame, lighting are part of the main build.
- Slat version stays the main plan; artisan oak joinery offered as the alternative they are developing.
- Hidden slim drawer wanted (done: sub bay under worktop).
- They later want "Dave and Emma's watch log" (shared film/TV log like a Spotify Blend) as a separate future idea — listed under Later ideas.

## Files
- `src/build_doc.py` – plan HTML + PDF builder (`python3 build_doc.py` → `out/Home_Network_Plan_v6_1.pdf`). Tracker data in `TRACK`; phases in `PHASES`. Change output name when you bump the version.
- `src/doc.css` – plan styles. `src/diagrams.py` – SVG diagrams (network, front, drawer, sound, game, av, power, routes, pcshelf, section).
- `src/render.py` – one-point perspective renderer in real cm. `P(x, y, z)` projects; `at(off, fn)` lifts a group by `off` cm; `RAISE`, `CEIL`, `TT`, `STYLE` ("slats"/"joinery"), `CALLOUTS`, `JOIN_CALLOUTS`. `python3 render.py` writes `v7_*.svg`.
- `src/shot.py` – rasterise: `python3 shot.py in.svg out.png width height scale` (key renders are 2360 × 1150, plain 1800 × 1150).
- Backups of earlier stages: `src/render_v*_backup.py`, `src/build_doc_v*.py`, `src/diagrams_v4.py`.
- Research notes are folded into the plan's Sources list (RetroTINK-6X CE stock/power, LG C6 ports, AX5100G rears/inputs, BESTÅ shelf 20 kg, Deco X1500 ports, game case sizes, Glorious Vinyl Vault, runners).

## Gotchas
- `P()` breaks for z ≤ −505 (behind the camera); keep room geometry at z ≥ −470.
- `replace_func` style patches: the next `def` after a function may swallow module-level constants placed between functions; check after patching.
- The client reads renders closely (they caught a PS1 that looked like an Xbox One S). Draw consoles to real shapes and sizes.
- Keep every dimension consistent across render, diagrams, tables and text; re-run the arithmetic when anything moves.
