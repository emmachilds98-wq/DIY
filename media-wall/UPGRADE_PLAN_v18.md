# v18 upgrade plan (round 12, 20 Oct 2026)

## The client's words (keep them)
- "PC internals still not visible, there is a clear side panel so we should see te graphics card etc."
- "ive bought a plant shelf something very similar to this image attached" (a bamboo plant stand, two columns, four tiers, with LED grow
  light bars under the top two tiers: `inputs/photo_plant_stand_bought.webp`) "and i could keep the vinyl shelf i have in images shown before
  too. 4 trays in 2x2 square wood shelf."
- "add more things to improvements and design options."
- "HD with shadows sometimes crashes also."
- "also try to add function for moving things around in a dolls house like fashion, edit mode. add things i could add in and make things
  removable and adjustable. colours adjustable too maybe so we can get rid of some of the menus. optimising user function"

## The work
1. **PC glass side** (`render.wrap`): the case as five panels plus a glass side (`url(#glass)`), so the 2D renders and the 3D room show the
   graphics card, cooler, RAM and fans. Done first.
2. **The plant stand and the 2×2 record shelf** (`geometry.PLANT_STAND`, `geometry.RECORD_SHELF`, `fit.py`, `questions.py`):
   - Sizes are assumptions until measured: the stand about 90 × 30 × 120 (two columns, four tiers, grow bars under the top two); the
     record shelf at IKEA KALLAX 2×2's 77 × 39 × 77 (four trays, face-out). Two new questions ask for both.
   - Two layouts (a design option, a 3D button group "Plants and records"):
     - **A, recommended:** the plant stand in the window's west corner (x 345–435, against the window wall, daylight plus its grow
       lights), the record shelf on the chimney breast under the “now playing” ledge, beside the turntable.
     - **B:** the record shelf in the window corner (where it is today), the plant stand on the breast (the ledge comes off).
   - The red lamp's default spot moves to the sofa's west end (the corner is taken either way). The plant-ladder idea is dropped: the
     real stand does its job.
   - 2D main render: the record shelf on the breast (layout A). Buy list: a smart plug with a schedule for the grow lights, drip trays.
3. **Edit mode in the 3D room** (`room3d.js`, `room3d_page.py`): an "Edit room" button over the canvas switches to the dolls' house view.
   - Tap a thing to select it: drag it across the floor, turn it 45°, change its colour, remove it. Movable: the plant stand, the
     record shelf, the red lamp, the coffee table, the rug, the C-table idea, and anything added.
   - "Add" puts in a catalogue piece: armchair, side table, tall floor plant, slim bookcase, beanbag, footstool, floor cushion, record crate.
   - Tap a wall, the ceiling or the skirting to paint it (a colour picker plus the three Farrow & Ball greens): the ceiling and skirting
     menus go, and "Where the red lamp stands" goes (drag the lamp).
   - "Reset layout" puts everything back. Positions are saved per device (`S.layout`, `S.added`).
   - The sliders fold away under "Fine-tune each light".
4. **HD shadows crash**: at most four spotlights cast shadows (the brightest), never more than the GPU's texture units allow; the saved HD
   picture uses at most six; a lost WebGL context drops to Fast and offers to reload instead of leaving a dead canvas; phones save at
   2560 × 1440.
5. **More improvements and design options**: new idea cards (and the plan's later-ideas list).
6. Rebuild, QA at 390/1280, publish (71ff if reachable), PR into main, merge, HANDOFF.
