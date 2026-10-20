# v21 upgrade plan (for the next agent)

Read `media-wall/HANDOFF.md` first (START HERE, then round 14). v20 is built and merged into `main` (GitHub Pages:
https://emmachilds98-wq.github.io/DIY/), and published to the shared deck (https://claude.ai/artifact/71ffwf5PRLhoLj6G5KTvm2).

## Waiting on the client
1. **The chair cupboard: four or six.** Four: as drawn (22 deep, flush with the pipe boxing). Six: set `CHAIR_STORE["cupboard"]["d"]`
   to `d6` (31), redraw `diagrams.chair_storage()` with three deep, re-check the window-end chair with the table open (`fit.chairs_zone`)
   and the 3D `chairsIn` (three deep a level).
2. **The window corner at floor level** (`cornergap`): if it's under 98 + 2, offer the curtain pole's west end in or layout B.
3. **The side of the stairs by the door** (only if five and six should live there): draw it if it's open.

## Then, if there's time
- Decor: let a picked look be saved to the plan's shared layout too (`layouts/shared` already carries the layout; add `S.decor`).
- The glass case: if the client takes it up, move it from `ideas.py` into the plan (a buy row, a cut list, a fit row with cited glass).

## Rebuild and ship
`cd media-wall/src && python3 make_images.py && python3 export3d.py && python3 shot3d.py && python3 build_doc.py && python3 build_viewer.py`
QA at 390 and 1280 px, update HANDOFF and README, PR into `main`, merge once checked (the client views Pages), publish the deck.
