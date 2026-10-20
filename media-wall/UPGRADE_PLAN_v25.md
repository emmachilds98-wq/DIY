# v25 upgrade plan (for the next agent)

Read `media-wall/HANDOFF.md` first (START HERE, then round 18).

## Waiting on the client
1. **The chairs:** the cupboard for four (22 deep) or six (31 deep); yes or no to four behind the folded top (`BEHIND_TOP`) and to
   the fold-down seat (`WALL_SEAT`). See UPGRADE_PLAN_v24.md for what each answer changes.
2. **The ottoman's height** (`SOFA_POUF["h"]`, drawn 44), the window corner's floor gap, the optimisation plan's three questions.

## Then, from the optimisation plan (still to do)
- A guided tour and "copy link to this view" in the 3D room.
- Choices for each suggestion (two or three versions, like the decor rows).
- Only re-render the stills that changed (a fingerprint per shot in shot3d.py).
- Text: the long reference paragraphs left (Network's Part P note, the paint tab's scenes, the plant stand) could become short lists.

## Rebuild and ship
`cd media-wall/src && python3 make_images.py && python3 export3d.py && python3 shot3d.py && python3 build_doc.py && python3 build_viewer.py`
then upload `src/deck_assets_todo.txt` to the deck's asset store, record them in `src/deck_assets.json`, run build_viewer again,
QA at 390 and 1280 px (light and dark), update HANDOFF and README, PR into `main`, merge once checked, publish the deck.
