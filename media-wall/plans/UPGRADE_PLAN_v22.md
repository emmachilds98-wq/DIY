# v22 upgrade plan (for the next agent)

Read `media-wall/HANDOFF.md` first (START HERE, then round 15). The client-facing plan is `media-wall/plans/optimisation_v21.html`
(published as an artifact; the final reply of round 15 has its link). Its "v22" list, in order, unless the client answers otherwise:

1. **3D controls in five drawers** (room3d_page `controls()`): Layout (table, chairs, plant stand), Lights, Look (paint, decor), Extras
   (ideas, suggestions), Views. One open at a time; on phones keep the stage in sight (sticky stage, the drawer scrolling under it).
2. **Build steps one at a time** (build_viewer's Build tab, instructions.py): each step folded to its title and tick, one open, "next step",
   progress at the top from the saved ticks.
3. **3D speed:** a poster (`3d_room` still) until `R3D.ready`; merge static furniture per material (like `BUCKET`) to get under 150 draw
   calls; in Fast, one light per spot bar and about eight lights in all (keep the count fixed while toggling so programs don't recompile).
4. **The deck's pictures in its asset store** (the deck already declares `assets`): load the `artifact-capabilities` skill, upload
   `src/art/*`, reference by the returned URLs, publish without inlining (about 2 MB instead of 10.8).
5. **"Your picks":** the ideas, suggestions and decor switched on, their costs added up, and a "send as a note" for the next round.

Also waiting on the client: the chair cupboard (four or six), the window corner gap, the stairs photo, and the plan's three questions
(the first view, what to do first, the backup files).

## Rebuild and ship
`cd media-wall/src && python3 make_images.py && python3 export3d.py && python3 shot3d.py && python3 build_doc.py && python3 build_viewer.py`
QA at 390 and 1280 px, update HANDOFF and README, PR into `main`, merge once checked (the client views Pages), publish the deck.
