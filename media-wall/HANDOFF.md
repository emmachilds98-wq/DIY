# Handoff: Home Network & Media Wall Plan

## START HERE (next agent)
- **Branch:** `claude/sharp-franklin-lrray1`, restarted from `main` (v14.1) in round 9 after PR #4 merged; work there and open a PR into `main`.
- **`main` is published with GitHub Pages: https://emmachilds98-wq.github.io/DIY/** (the root `index.html` is `build_viewer.site()`; `.nojekyll`
  skips Jekyll). The client wants the latest version on main so they can view it there: work on the branch, open a PR into `main`, merge it
  once checked so Pages stays current.
- **Viewer artifact (the shared deck): https://claude.ai/artifact/71ffwf5PRLhoLj6G5KTvm2**, owned by Emma's account (the one this repo's
  sessions run as). Update it in place: `python3 build_viewer.py`, then publish `src/media_wall_viewer_inline.html` (images inlined) to that URL
  with no files map, omitting `capabilities` (it keeps db + user + assets + downloads). **Read the client's answers first:** ArtifactData
  `list` on `answers` (and `tracker`, `steps`). The QRfYUvbPVQpSHFgaDN4YMU deck belongs to another account: don't use it.
- **Rebuild:** `cd media-wall/src && python3 make_images.py && python3 export3d.py && python3 shot3d.py && python3 build_doc.py && python3 build_viewer.py`
  (shot3d renders 12 stills headless in SwiftShader WebGL: about 10 minutes; `SHOT3D_DIR=<scratch> python3 shot3d.py test <name>` makes quick
  1280 × 720 ones).
- **Every number lives in `src/geometry.py`**; the fit proof is `src/fit.py` (cite a source for every size). Open questions: `src/questions.py`
  (one list feeds the PDF, the overview's "To confirm" line and the viewer's Questions tab).

## Update 20 Oct 2026, round 9: v15 (the room as it really is, smart lights, one oak run on the side wall)
- Client: "my sofa goes to around 40cm before the end of the window ... 2 seats then corner ... blue corduroy and you can remove the white
  cushion. the lamp is bright red, it has rgb lights mainly stay on green on top then pink then purple going down. either add my hat there or
  give it a wallstand ... make the hanging plant on the wall shelf actually hang and add my small laser from the middle. on the left of that
  shelf is my ikea light box. ... vinyl large only no extra small slot ... look better especially on the left wall side ... bar lights to run
  in the other direction ie tv to window on both fixtures ... make lighting less spotty ... slide lighting strength via slider ... smart rgb
  ... colour adjustors for not only wall paint but ceiling paint and skirting paint ... curtains (photo to come) ... soft grey carpet and a
  nice design rug that fits".
- Geometry (v15 block at the end of `geometry.py`): `SOFA_W` 266 (x 2..268), `SOFA_SEATS`, `SOFA_CORD`, `SOFA_CUSHION`; `TRAY_SINGLES` 0,
  `TRAY_LP_ONLY`, `TRAY_INSIDE`; `BAR_AXIS = "z"`, `BAR1_HEADS` (one list for renders, plans and 3D), `bar_head_xz()`; `SMART_BARS`,
  `BULB_E14` (the Wolston takes E14, 6 W max per Dunelm; WiZ Colour P45 4.9 W 4.5 × 10.1, Hue lustre 5.1 W 4.5 × 7.7; source `e14`);
  `LAMP_BODY`, `LAMP_HEADS_RGB`; the side run `SIDE_RUN_Z`, `SIDE_RUN_T`, `SIDE_SWEEP`, `side_run_depth(z)`, `SIDE_GLOW`; `CARPET_COL`,
  `RUG`, `RUG_COLS`, `CURTAIN`, `LIGHTBOX`, `LASER`, `PLANT_B`, `HAT_PEG`.
- Drawn renders: `render.side_run()` (one board, convex quads so the 3D fan triangulation works), `rug()`, `curtains()` (side view),
  `sofa_solid()` rewritten, LP-only `record_tier`, `spot_bar()` along z with wider, fainter pools; grey floor gradient.
- 3D (`room3d.js`, backup `room3d_v14_1_backup.js`): state key `mw15-3d`; `S.lv` per-layer levels (scene buttons fill them) × `S.master`;
  `S.col` colours for bar1/bar2/lamp0-2 (smart bulbs; glow discs follow); spot cones 0.66 rad, penumbra 1; paint channels wall/ceil/trim
  (`chHex`, `S.ceil`, `S.skirt`); grey carpet + pile bump, `RUG_TEX`, corduroy bump, curtains, light box (`LBOX_TEX`), laser dots
  (`THREE.Points`, `S.laser`), trailing plant (tubes + leaves), oak hat peg with a felt hat, red lamp with per-head colours, the side run's LED
  strip + a RectAreaLight wash (in the uprights layer). Controls in `room3d_page.py` (`LIGHTS`, `CEIL_PRESETS`, `SKIRT_PRESETS`).
- Docs: buy list (no dimmers; 8 smart E14 bulbs £100–360; side-run LED; optional smart button; rug £120–300; hat peg), step 10 (cut the run
  from one 225 × 30 × 4 board to a template), step 12 and its instructions (no dimmers, set up the app), section 8 lighting, section 9
  electrics, scenes.py (layers' controls; lamp levels dimmable). Questions: dropped `lamp` (answered); new `hat`, `lightbox`. The deck's db: `answers/sofa` (v2) and `answers/lamp` written from the client's notes.
- Fit proof 70: 51 fit, 14 tight, 5 check. New checks: the six-seat window-side chair backs onto the sofa's longer arm; option B's walk
  behind the chairs is 67 (TIGHT). Rows for the sweep, the bars turned, the smart bulbs.
- Then the client's photo (20 Oct, `inputs/photo_room_curtains_evening.jpg`, evening, purple RGB light): the curtains are long pencil-pleat panels
  to the floor, oatmeal, on a rail just under the ceiling strip (`CURTAIN` redone; 3D toggle `S.curtains`); the carpet is already soft grey.
  Questions 18 (curtains and carpet answered and dropped). Still to come: the hat's photo, the light box's name.
- Then: "hessian curtains from dunelm with a wood rail" (`CURTAIN` col/pole/finials; 3D `HESSIAN` weave, wooden pole, rings, finials; source
  `curtains`) and "an improved table design that could maybe stay attached to the wall and maybe even seat more people": the **flip-top
  gate-leg table** (`TABLE_STYLE = "fliptop"`, `FLIP`, `FLIP_SPACER`, `RAIL` now 10.3 deep with its hinge rail, `OPEN_Z`, `OPEN_LEN`,
  `GATE_LEG_H`, `TABLE_B_OPEN_X`). The half hinges on three Lee Valley 40574 flip-top hinges (source `fliphinge`; their 40208 needs a 30 mm
  edge). `render.fliptop_wall()`, `dining_chairs()` (2 or 3 a side), `table_settings(n_side=)`; DINING states folded / four (open, 2 a side)
  / six (open, 3 a side); the free-standing table and the leaf's leg case are kept behind `TABLE_STYLE` but unused. export3d rotates the
  chairs to B for every state. `fit.fliptop_zones()` replaces the dining zone and `stairs_zone()` (A: up to 6, no end seat (sofa: CHECK);
  B: up to 7). `diagrams.fliptop()` (section, folded/open) replaces `dining_section()` and `leaf_case()` in the plan; `seating()` and
  `dining_sites()` redrawn. Section 5, step 11 + its instructions, buy list and cut lists rewritten. Fit proof 69: 50 fit, 14 tight, 5 check.
- Full rebuild done (total £2,965–5,992; plan 62 pages, build guide 41); QA at 390 and 1280 px, no console errors. Published v15 to 71ff
  (version 15, id 1792466792-e7af) over the v14.1 deck another session had put up; v15 contains v14.1, and the tracker had no ticks to lose
  (13 buy/step lines changed text, so their tick ids changed). v14 outputs moved to `out/v14/`.

## Update 20 Oct 2026, round 8b: v14.1 (a faster 3D room, GitHub Pages)
- Client: "ive activated pages on github, do another full upgrade wherever necessary. it runs very slow on the renders but it looks great so
  far. improve everything wherever possible"; then "put the latest version on main where i can view it via the pages link". PRs #6 and #4
  merged, so main = v14.1.
- 3D speed (`room3d.js`, backup `room3d_v14_backup.js`): built only when the Room tab first opens; shadow maps redrawn only when the room
  changes (`shadowMap.autoUpdate = false`, `reshadow()`); half resolution while dragging, full again 180 ms after; PCF shadows interactively,
  PCF-soft for saved pictures; HD pixel ratio capped at 1.5; the shell's small parts merged per material; the 4 upward strip area lights
  replaced by an emissive glow map on the ceiling; Fast mode drops all area lights (the costliest) and lifts the fill; phones start on Fast
  and any device that takes >70 ms over a full HD frame drops to Fast unless you picked. SwiftShader bench: HD 2.8 s → 1.56 s a frame,
  Fast 1.8 s → 0.70 s, before the 4× saving while moving. `R3D.bench(n)` and `R3D._dbg` are there for tuning.
- Realism: `render.art_on()` now records sleeve art in 3D, so the framed LPs, the ledges and the trays show their covers; the sofa is
  upholstered (RoundedBoxGeometry, matte fabric).
- Page: pictures load per tab; header buttons for the 3D room and both PDFs; a Downloads list (Checks tab) that links straight into
  `media-wall/out/` on Pages; the Pages copy says its ticks stay on the device and links the deck; dashboard 2-up on phones.

## Update 20 Oct 2026, round 8: v14 (the table by the stairs, the room in 3D, the page reorganised)
- Client (with two photos of the west wall): "see all the latest work … merge any not in your version … full review of the format and layout
  … full upgrade. I want customisable HD realistic renders to show my options as well as more views of around the room … what if the table
  was on the wall going up the stairs under my shelf which is 2m long … all other furniture can move, the lamp is only 100% and we can still
  shift location". Merge: this session's duplicate v13.6 work was dropped; v13.6–v13.8 (other sessions) are the base. Read "the lamp is
  only 100%" as "the lamp definitely stays" (and it's drawn on/off only anyway); asked in the `lamp` question to be sure.
- **Option B, the table on the stairs wall:** geometry `STAIRS_WALL_Z` (−41 … −309), `SHELF_B` (2 m black floating shelf, top ~200, 25 deep,
  z −93 … −293, scaled from the photos at ~4.5 px/cm), `TABLE_B_*` (centred z −180: 84 to the stair box, 74 to the window), `DINING_SITE(S)`,
  `FLOOR_LAMP(_SPOTS)`; `BAR2` moved to (412, −143), the existing pendant point in the photo. `fit.stairs_zone()` (8 rows: 2 tight end chairs,
  1 check on the wall's build) → fit proof 66: 49 fit, 13 tight, 4 check. `diagrams.dining_sites()` (A vs B mini plans) and a "Two places for
  the table" subsection in plan section 5. Questions now 17: new `site`, `westwall`, `lamp`; `westend` and `point2` rewritten from the photos.
- **The room in 3D** (`src/room3d.js`, `room3d_page.py`, `export3d.py`, `shot3d.py`): render.py records every box, polygon and face frame
  it draws (`REC`, `P3`), in room coordinates; export3d groups them by state (unit in/out, A/B × folded/four/six; B = A turned 90° onto the
  west wall) into `scene3d.json`. The shell, shelf B, the lamp, the spot bars (real spotlights aimed as in `SPOT_HEADS`), the strip
  (RectAreaLights), bias light and the TV picture are built in the browser. Three.js 0.160.0 from jsDelivr by importmap. Options: table
  site and state, lighting scene (+ daytime), paint (+ any colour), lamp spot, drawers, quality; 9 cameras plus orbit; "Save HD"
  (3840 × 2160 PNG via the downloads capability). Headless stills: 12 in `out/Media wall v14 - 3D - *.png`, art/3d_*.webp, and three in the PDF.
- **Page:** tabs grouped (See it / The plan / Do it / Your input); new Room in 3D tab with a gallery; "3D views" renamed "Drawn views";
  the overview opens with a dashboard (steps done and next step, bought and paid, answers) and an A-vs-B options card, also on the Dining tab;
  buttons on each option open the 3D room set to it.
- `out/`: v13 files moved to `out/v13/`; drawn HD renders renamed v14. Backups `*_v13_8_backup.py`, `build_viewer_v14_pre_layout_backup.py`.

## Update 19 Oct 2026, round 7i: v13.8 (back on the deck, summaries that follow the data)
- Client: "view this chat and continue … improve anything you need to and publish". That session wasn't visible from here, so it was picked
  up from git (v13.7, `f5a48b3`) and its HANDOFF; full rebuild ran clean; phone (390) and desktop (1280) checked on every tab: no overflow,
  no console errors.
- Fixed: the overview's "To confirm" line still listed the PC case (answered v12.1); it's now `questions.summary_line()` (new `SHORT`
  labels). The fit-proof intro named four "check on site" items (PC case, door) for three checks and an old tight list; it now names the
  three real checks (TV plugs, RetroTINK size, sub vibration) and all eleven tight ones. README fit numbers (were v13.2's) corrected.
- `GITHUB_OUT` now points at this branch (switch to `main` after PR #4 merges).
- Published v13.8 to 71ff (version 12); the open stairwell comment thread was answered (stairs go up since v13) and resolved.
- Backups: `build_doc_v13_7_backup.py`, `build_viewer_v13_7_backup.py`, `questions_v13_7_backup.py`.
- Still offered, not done: daytime renders; furniture options (waits on the sofa's return). Bar 2's position waits on `point2`.

## Update 19 Oct 2026, round 7h: v13.7 (lighting scenes)
- Upgrade picked from the offered three: lighting scenes. Why: the client is now fitting the dimmers and bars themselves (step 12), so a
  setting for each control per occasion is immediately usable, and it doesn't wait on an open question. (Furniture options wait on the
  sofa return's length; daytime renders matter less now the paint is chosen and sampling is in step 4.)
- `src/scenes.py` (LAYERS, SCENES: TV night, dinner, records, everyday evening), `diagrams.light_scene(key)` (room plan with each light's
  glow and a level bar per layer), `build_doc.scenes_html()` in section 8 (table + four figures between `<!--scenes-->` markers),
  `build_viewer.scenes_block()` turns them into buttons in the Paint & light tab. The uprights' LED driver now has an inline dimmer.
- Found while drawing it: bar 2's point is assumed 35 cm from the west wall, but the 84 cm bar parallel to the media wall would reach
  past it (433 + 42 = 475 > 467). Added to the `point2` question; if confirmed, hang it turned along the west wall.
- **Deck conflict:** v13.6 was published as QRfYUvbPVQpSHFgaDN4YMU (version 1) at about 20:53Z; at 20:55Z another session or agent
  published a different build to the same artifact (eyebrow v13.3, total £2,784–5,297, `.p-prep` part classes). v13.7 was NOT
  published over it; the client was asked which to keep. Git was unaffected (branch head was this session's own commit).

## Update 19 Oct 2026, round 7g: v13.6 (leg case in the leaf, electrics as your own job, part labels, one questions list)
Redone from the brief after the previous session hit its limit before committing.
- Client: "include legs on the table build or make it more easy to get out and assembled ... store them as a part of the tables build
  maybe in a box"; "we will also be doing electrics ourselves other than maybe changing a view fixtures for lights and sockets. make the
  build plan easy to tell how to find which part ie network/media wall/table etc"; "update what you still need from me too".
- Legs: `geometry.LEAF_FRAME` (insets 3/1.5, rails 1.8 × 5.5 → outside 54 × 77, inside 50.4 × 73.4), `LEG` 4.5→3 oak, `LEG_BOLT`,
  `LEG_CLIP` (RS PRO 45 mm, source `clip`), `LEG_PITCH` 6, `LEAF_LEG_IN` (7.5, 6.5). Oak legs only now (steel option dropped).
  `render.free_table()` draws tapered oak legs and the frame; new `diagrams.leaf_case()` (A underside, B section, C steps) in section 5,
  step 11 and its instructions. Fit proof 58: 44 fit, 11 tight, 3 check (two leaf rows: storage, knees 17.5 above the seat).
- Electrics: phase "2 Electrician and cabling" renamed "2 Cables and power" (its tracker ids changed; the db was new anyway). No
  electrician, no new socket behind the sofa (`SOCKET2` = an existing one IF there is one, drawn dashed), no fused spur (plug-in LED driver).
  PC on the 10-gang (load ~1.55 kW) via its own 25 mm conduit beside a 38 mm data conduit. Steps 3 and 12 rewritten with the safe
  routine and a stop list; section 9 "Electrics: your own job" cites GOV.UK Approved Document P + IET + Planning Portal. Tools and
  a GS38 tester on the buy list. If there's no socket by the sofa, a 12-way strip (0–60) gives the rears a way.
- Parts: `build_doc.PARTS`, `PHASE_PART`, `part_chip()`; every step has `part`; chips on step cards, the overview run list, buy phases,
  PDF steps and phase tables; Build steps tab has a "Show one part" filter (remembered per device).
- `src/questions.py`: the one list (15) for the PDF's "Still to confirm" and the viewer's Questions tab; new `electrics`, `retrotink`;
  dropped door/walls/pc (answered) and the leaf/legs part of `chairs`.
- Total £2,764–5,317 (was 2,589–4,897 plus an electrician). Backups `*_v13_5_backup.py`. Viewer: the new artifact above, version 1.

## Update 19 Oct 2026, round 7f: v13.5 (sub back in the media wall, every step in full, HD renders)
- Client: "adjust the media wall unit to still include the sub somewhere; the consoles' battery packs can be stored behind near
  power cables. Re-assess, research, validate sizing"; "full build instructions step by step for the wall and the dining table";
  "integrated in the one deck we are using, we should not be splitting info apart"; "improve the renders to HD".
- `geometry.SUB_IN_WALL = True`: the Xbox bricks lie flat at the back of their rows (Microsoft PSU guidance, source `psuplace`);
  the RetroTINK and HDMI switch move to bay 1's fronts; bay 2 below the PS3 shelf = sub column 23.4 wide (`SUB_COL`), 12 mm
  divider, PS2 over PS1 in 32.2 (`PS_COL`). Sub on a 3 cm isolation riser, front flush with the face frame, port 15.6 cm from the
  wall (`SUB_PORT_GAP`; Klipsch 15–30). The retro 6-way and Switch 2 move behind bay 1. `SUB_POS` follows the sub, so the plans
  move with it; the dining wall's cover is gone (the old code paths are kept behind `not SUB_IN_WALL`).
- Fit proof: 56 checks, 42 fit, 11 tight, 3 check (TV plugs, RetroTINK size, vibration: Microsoft says keep the 360 away from
  subwoofers, source `x360place`; test on site, fallback is the dining wall). 
- `src/instructions.py`: full instructions per step (parts, hardware, tools, drawings, numbered sub-assemblies); merged into
  `build_doc.steps()`; the page's step cards show them with their drawings inline; the build guide PDF prints them in full.
  Fixes on the way: table centre panel ordered 101 long (2.5 tongues), 8 leg inserts (the leaf has four), bay 2 divider/part shelf/riser.
- HD: page images are WebP at 1.5 × (3300 wide, `make_images.ART_SCALE`), overlays WebP with alpha, a "View full size" lightbox.
  Inline page ~5 MB. `build_viewer.uniq_svgs()` prefixes ids per inline drawing (patterns in hidden tabs don't paint).
- Viewer version 11.

## Update 19 Oct 2026, round 7e: v13.4 (cutting list)
- Viewer version 10. `cuts()` in build_doc.py: every made part grouped by stock (solid oak; birch ply 18, 12, 9, 6 mm;
  hardware), from the section 3/5/7 cut lists and v6.1's game drawer. New size: record tray sides 8 cm tall. Shown in the Build
  steps tab (with Copy as text) and at the end of the build guide PDF. Step 6 now starts with ordering from it.
- Still offered, not done: daytime renders (needs relighting in render.py), lighting-scene buttons, furniture options.

## Update 19 Oct 2026, round 7d: v13.3 (the plan in tabs on the viewer, step-by-step build, cost by phase)
- The client asked for the whole plan inside the viewer (no fetching PNGs or PDFs from GitHub), in tabs or pages, with a clear
  build plan, buy guide, cost by phase, the table, and the network/power plan (they sent their v6.1 PDF as the reference for
  network and power: `Home_Network_Plan_v6_1.pdf`, its "What each part does" table and two setup stages are now in section 9).
- Viewer version 9, ~5.5 MB inline. Tabs: overview, views, wall, dining, paint, network, build, buy, questions, checks (bare
  `#token` deep links; last tab remembered per device).
- `build_doc.py`: `_plan(deck=True)` renders the plan with images as `data-art` keys (`DECK_ART`) and markers around the fit tables
  and the still-to-confirm list; `plan_sections()` splits it at the h2s; `build_viewer.deck_section()` turns "section N" into tab links,
  wraps tables to scroll and puts SVGs on paper cards. Edit content in build_doc.py once; the PDF and the page both pick it up.
- `steps()` in build_doc.py is the order of work (13 steps, each with substeps, a check, its time, and `buy`: the buy-list phases
  needed before it). The PDF table and the page's step cards both come from it. Step ticks save to db `steps/s<n>`.
- Buy tab: cost-by-phase range chart (one £ scale, 200 steps), paid per phase from the tracker, a still-to-buy total, filters.
- `art/doc_paint.jpg`, `art/doc_skirt.jpg` are made by `build_viewer.doc_images()` from the two PNGs.

## Update 19 Oct 2026, round 7c: v13.2 (sub cover, drawers view, measurement overlays, stairwell opening, sofa)
- Viewer version 8 (publish `src/media_wall_viewer_inline.html`, ~7 MB, images inlined).
- Sub: `SUB_HOOD` is now a cover (no sides, no front): 1.5 backboard on two keyhole screws, 2 cm top with drip groove 3 cm over the
  sub, tray with a 2 cm lip all round. Tip check in fit.py: the sub's corner would rise 7 cm to tip; the cover stops it 4 cm short.
- New view "drawers" (`CAM_DRAWERS`, `plinth_drawer()`, `PLINTH_OPEN`): game drawer and upper tray 30 out, plinth drawer 25 out.
- Measurement overlays: `measure_layer(kind)` / `measure_side()` draw rough sizes in pale yellow (`MC`); `build(..., measure=kind)`
  returns only that layer; make_images renders them transparent (`shot.py` 6th job field) to `art/dims_<view>.png`; the viewer's
  "Show measurements" button lays the one for the current view over the picture.
- Stairwell: the ceiling opening now runs from just after the door (`DOOR_X[1]`) over the banister to the west wall, from the stair's
  front edge back; seen through it, the stairwell walls and a landing balustrade; the LED strip follows the opening's edge.
- Sofa (side view): `sofa_solid()` redrawn as the black jumbo-cord L-sofa: plinth, seat bases, plump seat and back cushions with cord
  channels, arms, the grey faux-fur cushion.
- Fit proof: 59 checks, 47 fit, 9 tight, 3 check, 0 fail.

## Update 19 Oct 2026, round 7b: v13.1 (sub safety box, six with the leaf, side view dimensioned)
- **Publishing:** the artifact refuses some JPEG uploads from this (cross-org) session as "cpio archive" (false sniff, unpredictable),
  so `build_viewer.py` also writes `src/media_wall_viewer_inline.html` (images as data URIs, ~6 MB, gitignored). Publish **that file**
  to https://claude.ai/artifact/71ffwf5PRLhoLj6G5KTvm2 with no `files` (version 7). Downloads link to GitHub.
- Client: "something that increases the safety of the sub… a box with an open front… not restrict sound… stop spills or knocking it
  over". The AX5100G's driver fires out of its front, the port out of its back (Trusted/Expert Reviews), and it stands sideways under
  the table, so `SUB_HOOD` (x 214–249, 28.2 out, 37.4 tall) is open at both ENDS, solid top (drip groove, 1 cm overhang) and front,
  base tray with 2 cm lips, hung on a cleat. Port to the west arm 36.7 (15–30 advised: new source `subport`). `render.subwoofer()`,
  new `diagrams.sub_box()` (plan, viewer #subbox, `out/Sub box - ….png`). Fit rows for sound, spills/knocks, chairs.
- Client: "ensure measurements of the table are correct and would fit even when seating 6". 110 × 80 alone gave six 55 cm each
  (< 60). Now `SIX_LEAF`: six use the leaf (170 × 80) at `SIX_X` 232–402, `FREE_Z` −75…−155 (75 to the breast, 154 to the window,
  65 to the west wall), 85 a diner on the long sides; breast-side chairs 4 cm beside / 4.8 in front of the sub's box. Eight = same
  table, three a side (56.7, tight); lift the box off for eight (CHECK). `free_table()` draws the leaf and eight legs.
- Client: "in the side view of the pc wall ensure it's clear how much of the alcove covers the media wall". `side_alcove()` ghosts the
  cut-away breast and dimensions: alcove 38, base 46 (38 inside, 8 proud in gold), uprights/shelves 30 all inside.
- Fit proof: 58 checks, 46 fit, 9 tight, 3 check, 0 fail.

## Update 18 Oct 2026, round 7: v13 (less cladding, stairs up, drawer layouts)
**Branch:** `claude/eloquent-johnson-pgmnud` (built on v12.1, `claude/sharp-franklin-lrray1`). Viewer artifact updated in place:
https://claude.ai/artifact/71ffwf5PRLhoLj6G5KTvm2 (version 6). This session is an editor from outside the artifact's organisation: the
publish **refuses PDFs and some large images** (and the db/answers can't be read from here), so `build_viewer.DOWNLOADS_ON_GITHUB = True`
links every download to `media-wall/out/` on GitHub and `publish_files.json` holds only `art/*.jpg`. `art/zz_house.jpg` was refused as a
"cpio archive" (false sniff) and left as v12's copy (unchanged drawing).

Client, round 7: "less cladding all over the place, improve and upgrade design again. stairs also go up not down as i said. show the drawer layouts too".
- `geometry.PLAIN = True` switches off every v12 slat: the PC's slatted screen, the slatted cable spine and its skirting trunking, the
  slat panel behind the turntable (`rz_slats()`), the slatted sub box (sub now on `SUB_RISER`, plain oak, 5 cm) and the reeded table
  (`FOLDED_D` drops 1 cm; plain oiled underside, brass leg inserts kept). PC leads: brush grommet in the shelf + 25 mm conduit chased into
  the solid side wall (electrician, same visit). The slat-wall alternative is retired (no renders, no viewer button; appendix is now
  "Options we set aside").
- Stairs: `STAIRS_UP`, `STAIR_RISE`/`STAIR_GOING`; `west_end()` draws a flight rising away from the room (towards the hall) through an
  opening in the ceiling, closed string and raking banister on the door side; the part beyond the recess wall is clipped to the
  openings. **Direction is a guess**: question `stairs` now asks which way it runs (photo).
- New `diagrams.drawer_layouts()`: base elevation with drawers A–D, then each drawer from above at 5 px/cm. In the plan (section 3), the
  viewer (#drawers) and `out/Drawer layouts - ….png`.
- Fit proof: 56 checks, 45 fit, 8 tight, 3 check, 0 fail. Outputs v13; v12's moved to `out/v12/`. Backups: `*_v12_backup.py`.
- The open stairwell comment thread on the artifact can't be replied to from this session (cross-org); tell the client in chat.

## Update 18 Oct 2026, round 6b: v12.1, the client's answers
- Sofa (photo `inputs/photo_sofa_window_wall.webp`): black jumbo-cord L-sofa; the long side under the window ends in line with the
  breast's reveal → `SOFA_W = 188` (was 247). Return along the side wall still assumed 168, footstool at its end. Ask its length.
- Door: hinged on the chimney-breast side, opens into the room (`DOOR_HINGE`, `DOOR_OPENS_IN`); the fit row says keep it shut while
  eating (west-end and breast-side chairs sit in its swing) or rehang it to open into the hall.
- Walls: side wall and breast solid (`WALLS_SOLID`): masonry plugs and screws; the "check the walls" tracker item is Done.
- PC: "average gaming case" → `PC_CASE = (23, 46.6, 45.3)` (Corsair 4000D, 453 × 230 × 466 mm, TechPowerUp); the check now passes.
- Fit proof: 57 checks, 44 fit, 10 tight, 3 check, 0 fail. Answers written to the viewer's db (`answers/sofa|door|walls|pc`).
- Still open: sofa return length, west-end sizes, stairs up or down, LP/single/game counts, turntable and fan-stand models, 10-gang
  length and surge protection, second ceiling point position, chairs, the 23 × 22 box, wired ports, console models.


## Update 18 Oct 2026, round 6: v12 delivered (the v11 layout, upgraded)
**Delivered:** `out/Home_Network_Plan_v12.pdf` (45 pages), `out/Build_Guide_v12.pdf` (9 pages), HD renders in `out/` (v11 outputs
moved to `out/v11/`), the viewer artifact **https://claude.ai/artifact/71ffwf5PRLhoLj6G5KTvm2** (the client's copy of the v11 viewer on
this account; update this one in place), and `index.html`. The root `README.md` now carries the key renders, heights, storage sheet and
open questions so the client can read them on GitHub without downloading.

**What changed (the client's list from the session that hit its limit, their comments, and their v6.1 upgrades)**
- Sub in a slatted oak box (`SUB_BOX`, `sub_box()`): 52 × 30 × 42 between the folded arms; sub moved to x 214.5–244.9 inside it.
- Oak slats: PC screen (v6.1: 2.1 slats, 1.2 gaps, open top), a slatted cable spine (`SPINE`), a slatted panel behind the turntable
  zone (`rz_slats()`, preamp moved 2.2 forward; deck now 6.6 from the panel: tight).
- Folded table: reeded underside (`REED`), brass inserts instead of leg plates (client comment).
- Camera: default pulled back (`CAM_DEFAULT` = eye 120, X0 290, S 3.4, shift 150; v11's is `CAM_V11`) so bar 2 shows (client
  comment). The west end is an open stairwell with a wooden banister (`west_end()`, client comment; up/down asked, drawn going down).
- New views: dining for six (`CAM_SIX`), the PC side wall (`build_side()`, `VIEW = "side"`; `box()` now culls faces against
  `cam_pos()` in both views; the side view draws the media wall as massing in `media_end_on()` and leaves the breast out).
- `diagrams.storage()`: every space to one scale with counts and overflow options (high shelf spine-out ≈380 LPs; a second
  bay-3 unit west of the sofa).
- From v6.1: keyboard tray (`KB_TRAY`), lamp by the sofa, plinth-drawer finger pull, conduit to TV height, questions on games
  count, 10-gang surge protection, console models.
- Viewer (`build_viewer.py`): views join/four/six/side/slats × 4 paints; open questions with answers and photos saved to the artifact's
  db (`answers/<id>`, photos via assets); shared buy tracker (`tracker/<id>`); fit proof; downloads (published under `files/`).
  Read the client's answers with ArtifactData `list` on `answers` next round.
- Fit proof: 57 checks, 42 fit, 10 tight, 5 check, 0 fail.

**Next:** read the answers in the viewer's db; fix the stairwell direction; sofa size → PC shelf and clearances; walls solid or not → fixings.


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
