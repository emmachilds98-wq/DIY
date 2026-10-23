# Upgrade plan: v17 (written 20 Oct 2026, round 11, not started)

v16 is live: the deck at https://claude.ai/artifact/71ffwf5PRLhoLj6G5KTvm2 (version 16) and main / GitHub Pages
(PR #8 merged). The client sent the notes below while v16 was finishing. Nothing in this plan is built yet. Work on
`claude/sharp-franklin-lrray1`, restarted from main if PR #8's merge left it behind:
`git fetch origin main && git checkout -B claude/sharp-franklin-lrray1 origin/main`.

Before large edits, back up each file you touch as `*_v16_backup.*`. Afterwards, move the v16 outputs to `out/v16/` (with `git mv`, as
round 10 did for v15). Then bump `v16` to `v17` in `make_images.py`, `shot3d.py`, `room3d.js` (`stillName`), `build_doc.py`
(`VERSION`, `REVISION`, the `render_v16_` names) and `build_viewer.py` (`VERSION`).

## The client's words (keep them)
1. Sofa: "the end sofa seat closest to the tv against the wall has the seat cushion wrap around the back at the end there and towards the
   wall making that ottoman 'feet out' type space. it then just has no end open sofa about 20cm after that." Photo:
   `inputs/photo_sofa_window_wall.webp`. It gives the scale of both the window and the sofa.
2. "curtains should not render going through the window sill, i also have deep window sills that allow for lots of plants there."
3. "make all the ceilings lamps just face downward and give the room a general average lighting on the whole room as the default."
4. "green lamp should face down more slightly, its looking at the ceiling, face at the shelf wall."
5. "improve accuracy of table to our build plan design, improve if needed."
6. "bannister could be improved", and "stair tops also glitch and flash showing green under parts".
7. "assess all of the media wall inc computer and tell me if you can improve it at all", and "add a lit up PC internals to make it clear
   of what it is, it has a clear side window".
8. "review the pack itself for improvements. ensure any changes have been reflected in build guide and clear instructions on how to do
   everything step by step are inside, i should not have to download more files."
9. "suggest some additional things to add now we have the base of the room, we've discussed a display cabinet (glass) before but im
   afraid it would be too big ... only give suggested dont add to main render. add a designs for improvement tab maybe with a render",
   and "or build into the existing button changes like moving the lamp".
10. "make camera navigation easier, i want to be able to move around easier without clipping out of the room".
11. Hat photo (already done in v16): both hats hang on the red lamp.

## The work, file by file

### 1. Sofa: the ottoman end (`render.sofa_solid`, `geometry.py`)
- Add `SOFA_OTTOMAN = 20.0` to geometry. For the last 20 cm of the return (z from `CHAISE_END_Z - 20` to `CHAISE_END_Z`), stop
  the side-wall back frame and the back cushion. In that strip, run the seat base and the seat cushion back to the wall
  (x from `SOFA_X[0]`), so the cushion wraps round the back. The end stays open, with no arm (as in v16).
- Concretely:
  - The back frame box along the side wall runs z `zb` → `ze - OTT`.
  - The back cushion runs to `ze - OTT - 1`.
  - Add a seat-height box at `x0 .. x0 + bk + 16`, z `ze - OTT .. ze - 1`, top at `st`, with cord ribs on its +z face (the cushion's
    wrap).
  - Remove v16's 5 cm "wrap" box.
- The 3D copy follows automatically: `sofa_solid` is recorded by `export3d.py`.
- Update the `sofa` source text in `fit.py`, the `sofa` question in `questions.py` and the sofa line in the docs.

### 2. Window, deep sill, plants, curtains (`room3d.js` shell, `render.curtains`, `geometry.py`)
- Geometry: add `WINDOW_REVEAL = 22.0` (the frame set back in the wall) and `SILL = dict(nose=3.0, t=3.0, y=WINDOW_Y[0])`.
  The sill runs from z `WINDOW_Z - REVEAL` to `WINDOW_Z + 3`, along x `WINDOW_X ± 4`.
- 3D, in the shell's window block:
  - Move the frame and glass to `WZ - REVEAL - 4`, and the view plane further back.
  - Add the reveal's two jambs and its head (wall paint, `wallP`), and the deep sill board (white).
  - Add 6 to 8 potted plants along the sill: reuse the trailing-plant code as a helper, plus a few upright pots, of varied heights.
- Curtains must clear the sill and the radiator (the radiator runs z `WZ+3 .. WZ+10`):
  - Set `CURTAIN["z"] = WINDOW_Z + 11`, and use it in the 3D curtain panels and pole, and in `render.curtains`.
  - Move the sofa out 3 cm: `SOFA_BACK_Z = WINDOW_Z + 13` (was +10).
  - Re-run `fit.py` and check the A-table end gap and the coffee-table rows.
- Docs: mention the deep sill with your plants in the room section.

### 3. Lighting default: heads straight down, a "General" scene (`geometry.BAR1_HEADS`, `render.spot_heads2`, `export3d` bar2, `scenes.py`, `room3d.js`)
- Bar 1: change each head's target to straight down with a slight spread along the bar:
  `(PEND_X, 0, PEND_Z + off * 1.6)` for `off` in (31.5, 10.5, -10.5, -31.5).
- Bar 2: `render.spot_heads2()` and the B-site override in `export3d.scene()` take the same pattern,
  `(BAR2_X, 0, BAR2_Z + off * 1.6)`, for every dining state.
- Keep the head colours.
- Remove the per-head aim text in the docs (section 8's aim table, step 12's "aim the heads"). Replace it with: "all heads straight
  down, evenly spread; tilt one only if a pool lands badly".
- `scenes.py`: add a first scene, `("general", "General", "An even light over the whole room ...", {"strip": 55, "uprights": 45,
  "bias": 0, "bar1": 60, "bar2": 60, "lamp": 45}, [...notes])`.
- `room3d.js`: set `DEF.scene` to `"general"` and bump the store key to `mw17-3d`.
- `shot3d` stills that use `everyday` can stay as they are. Add `general` to the window still.
- The diagram `light_scene` arrows will follow the new targets.

### 4. The red lamp's top (green) head (`room3d.js buildLamp`)
- Today `aims[0]` points up (+110), at the ceiling.
- Aim it at the stairs (shelf) wall, slightly down: target `(R.W, R.LAMP.h - 30, clamp(spot.z + 30, SHELF_B.z[1], SHELF_B.z[0]))`, using the
  wall point rather than an offset from `toward`.
- The middle and bottom heads stay as they are.

### 5. The flip-top, matching the build plan (`render.fliptop_wall`)
- Lines (`_line`) are not recorded for 3D, so the joint and the breadboard lines vanish in the 3D room. Fix:
  - Open: draw each panel's two breadboard ends as boxes 0.05 proud (OAK_D, 7 wide × 80), with three dark peg dots (small boxes)
    each.
  - Draw the joint as a 0.6 cm dark box across the top at `zj`.
  - Add the three brass flip-top hinges as small brass boxes across the joint (`FLIP["hinge"]` 1.27 × 7.0, at x0+12, centre,
    x1-12), as the Lee Valley hinges show on top.
  - Folded: draw the breadboard lines and pegs on the underside as thin boxes, not lines.
- Check against `diagrams.fliptop()`:
  - The hinge rail is 7.3 deep (`RAIL[2]`).
  - The gate leg sits `FLIP["hinge_in"]` in from the far edge, with its apron between the tapered legs.
  - The Hebgo arms fold down flat, and lock under the top when open.
- Re-shoot `3d_dining_B_four` and look at it closely.

### 6. Banister and the stair glitch (`render.west_end`)
- The glitch: each step's riser box (`box(sx0, 0, z0, ..., y1, going, "#2d5a46", "#c48c57", "#244a38")`) has its top at `y1`, the
  same height as the tread's top. They z-fight, and the green side shows through.
- Fix: the riser box's height becomes `y1 - 2.2`, so it ends under the tread; keep the tread's 1.5 cm nosing overhang.
- Check the string poly (at `sx0 - 0.1`) doesn't fight the riser boxes' side at `sx0`: move the string to `sx0 - 0.6`.
- Banister:
  - Handrail: replace the flat `rail()` poly with a solid rail of three convex quads (top, outer face, inner face), 6.5 wide × 5.5
    deep, at 90 over the nosings.
  - Add a base rail (5 × 3) capping the string.
  - Balusters: 3.2 square at 10.5 cm centres (UK: a 10 cm sphere mustn't pass).
  - Newels: 9 × 9, with an 11 × 11 × 3 cap and a low pyramid top (a poly). Do the bottom newel and the one by the wall.
- Polys must be convex quads (the 3D builder fans each polygon from its first point).

### 7. Media wall and PC review, and the lit PC (`render.wrap` / PC drawing, `room3d.js`)
- Lit internals behind a clear side window, facing the room (+x side of `PC_CASE` at `PC_Z`):
  - In `render`, draw (recorded for 3D) a dark motherboard plate, a GPU box (about 30 × 12 × 4) across the middle, a tower cooler
    with a fan, 4 RAM sticks, the PSU shroud at the bottom, and 3 front fans and 1 rear fan with rings.
  - In `room3d.js`, after the furniture, add emissive (`MeshBasicMaterial`, `toneMapped: false`) fan rings and an RGB strip in
    `R.LAMP_RGB`-style colours, at the PC's position from `R` (export `PC_CASE`, `PC_Z`, `PC_SHELF_TOP` in `room_spec`).
  - Add a small `PointLight` inside (k about 3, distance 60), so the glass reads lit.
  - Add a "PC lit" toggle beside the light box and laser (`S.pc`, default true).
- Review of the media wall (put the findings in the reply, and in the plan's section 3 as "v17 review"). Suggested small
  improvements to build in:
  1. A powered USB 3 hub on the side run's front edge under the PC (the case's front I/O is about 200 up, over the sofa): a short
     extension to the hub. Add it to the buy list (about £15–30) and step 10.
  2. A remote power button for the PC: a wired power-button extension to the run's edge, or a PCIe Wi-Fi power switch card. Buy list:
     about £10–30.
  3. A magnetic dust filter on the PC's top exhaust (dust falls in at that height). About £8.
  4. A label for every lead at both ends (already in step 13: keep).
  5. Check the soundbar sits 2 cm proud of the TV stand's foot, so the IR receiver isn't blocked (fit row).
- Keep the bays as they are: v16's bay 3 split is the right call.

### 8. Review the pack, and make the build guide self-contained (`build_doc.py` `steps()`, `instructions.py`, `guide_pdf_html`)
- The build guide PDF must stand alone: no "see the Media wall tab".
  - In `guide_pdf_html()`, render each step's `see=` links as the actual figures. Each step's `draw=` list already names diagrams
    (`drawer_layouts`, `game_drawer`, `drawer`, `storage`, `fliptop`, ...): embed those SVGs inline in that step in the guide PDF.
  - Embed the step's cut-list rows (filter `cuts()` by where each part goes).
  - Replace the word "tab" in the guide with "below" or "page N".
- Add a step for the new bits: the "now playing" ledge (step 11 or 13), the USB hub and power button (step 10), the sill plants (none).
- Re-read every step for v16/v17 truth:
  - Step 8 has bay 3's divider and the slim drawers (done in v16).
  - Step 12 is smart strips and heads straight down.
  - Step 11 has the B site's fixing into the stairs wall (knock test first).
- Pack-wide pass:
  - Remove remaining "v13" labels in captions.
  - Check that every figure has a caption, and that every number cites `fit.SOURCES`.
  - Shorten the "What changed" box to the last 3 rounds, with older rounds in a collapsible appendix (the viewer already folds them).

### 9. Ideas (suggestions only, off by default): a new tab, plus 3D toggles
- Don't add them to the main renders. The client also suggested putting them in the existing 3D buttons (like moving the lamp): add a
  group "Ideas (not in the plan)" with a toggle per idea, all off by default (`S.ideas = {}`), and build each idea's meshes in
  `room3d.js`.
- Ideas, small enough for this room (the glass cabinet worry):
  1. A slim glass display case on the chimney breast: oak frame, 90 × 50 × 12, toughened 4 mm glass front, LED strip inside; for
     the hats or collectibles. It replaces the two frames when on. Not a floor cabinet: 12 deep.
  2. Glass plant shelves across the window reveal: two 6 mm toughened shelves at about 130 and 170, on reveal studs, for trailing
     plants. They use the deep sill.
  3. An oak C-shaped side table that slides over the sofa's open ottoman end: 45 × 30, 60 tall, for drinks and pads.
  4. A slim oak plant ladder in the window corner past the sofa's arm (x 268–308).
  5. Ideas with no render: a smart scene button by the door; a motion nightlight on the stairs; a record-cleaning kit tray in the pads
     drawer.
- Viewer: add a tab ("ideas", "Ideas") in `TABS`, under the "See it" group. It holds a short card per idea (size, rough cost, why
  it suits the room, the toggle to see it in 3D), and 3D stills shot with `ideas` on (add `SHOTS` entries in `shot3d.py` with
  `ideas: {...}` in opts; reset `ideas` between shots the way `drawers` is reset).
- PDF: an appendix, "Ideas for later (not in the plan or the costs)".

### 10. Camera: easier, and never outside the room (`room3d.js`)
- Clamp every frame, inside the OrbitControls change handler:
  - `camera.position` stays inside the room's box: x 4..W−4, y 20..CEIL−8, z WZ+6..AD−4; keep x ≤ ALC_W while z > 0 (the alcove).
  - `controls.target` follows the same clamp.
  - `controls.maxDistance` about 6 m; `minDistance` 0.3 m.
- Walk controls:
  - Keys: WASD/arrows move the camera and target together on the floor plane; Q and E turn.
  - On-screen buttons for phones: forward, back, left, right, turn left, turn right, as a small d-pad over the canvas.
  - The move step is about 15 cm per tap.
- `controls.screenSpacePanning = false`, so right-drag slides along the floor.
- Keep the named views (they already sit inside the room).
- Check `dolls`/`plan` views: those are deliberately outside, so skip the clamp while `VIEWS[S.view].above` is true and the user hasn't
  moved.

## Then
1. Rebuild: `cd media-wall/src && python3 make_images.py && python3 export3d.py && python3 shot3d.py && python3 build_doc.py && python3 build_viewer.py`.
2. QA the page at 390 and 1280 px, with no console errors. In the 3D room check: the walk buttons, the clamp, the ideas toggles, the
   lit PC, the stairs with no flicker, and the curtains clear of the sill.
3. Publish `src/media_wall_viewer_inline.html` to the 71ff deck: no files map, capabilities omitted. Read first if a newer version is
   live.
4. Commit, push, open a PR into main, merge it (the client's standing request), and update the HANDOFF.
5. Reply with the media wall/PC review findings (item 7) and the ideas list (item 9).
