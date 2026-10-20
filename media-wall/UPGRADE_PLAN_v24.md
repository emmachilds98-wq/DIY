# v24 upgrade plan (for the next agent)

Read `media-wall/HANDOFF.md` first (START HERE, then round 17).

## Waiting on the client
1. **The chairs:** the cupboard for four (22 deep) or six (31 deep); yes or no to four behind the folded top (`BEHIND_TOP`: the
   table then stands 22 further out; if yes, move `RAIL`/`TABLE_B_*` out, redraw the folded table in render.py and the 3D room) and to
   the fold-down seat (`WALL_SEAT`: if yes, add it to the buy list, the cut list and a build step).
2. **The ottoman's height** (`SOFA_POUF["h"]`, drawn 44).
3. **The window corner's floor gap** and the optimisation plan's three questions.

## Then, from the optimisation plan (v23 list, still to do)
- A guided tour and "copy link to this view" in the 3D room.
- Contents lists in the long tabs (Media wall, Checks, Dining, Network).
- Choices for each suggestion (two or three versions, like the decor rows).
- Only re-render the stills that changed (a fingerprint per shot in shot3d.py).

## Rebuild and ship
`cd media-wall/src && python3 make_images.py && python3 export3d.py && python3 shot3d.py && python3 build_doc.py && python3 build_viewer.py`
then upload `src/deck_assets_todo.txt` to the deck's asset store, record them in `src/deck_assets.json`, run build_viewer again,
QA at 390 and 1280 px, update HANDOFF and README, PR into `main`, merge once checked (the client views Pages), publish the deck.
