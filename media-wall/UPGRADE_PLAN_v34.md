# v34 upgrade plan (for the next agent)

Read `media-wall/HANDOFF.md` first (START HERE, then round 27).

## Waiting on the client
- Their picks in Decide (plan page, Plan home → "Waiting on you"): what goes beside the cabinet, 90 or 80 wide, where the light
  switch is. On the deck they're in the db's `picks` collection (`decide`, `short`: `{v, by, at}`); ask the client to paste them if
  ArtifactData can't read the deck's db from here.
- The padded chairs' price (the buy list estimates £80–130 a pair) and one chair's open depth: over 52.3 deep, the stair side's backs
  reach the door's swing while seated (a fit CHECK); under it, nothing to do.
- If they pick the 80-wide table, make it the plan: `geometry.CAB = _make_cab(80.0)`, the cutting list, step 11's sizes and the buy
  list's rows follow from it; check `fit.cab80_zone()` rows move into the main cabinet zone, and say where the other two chairs live.
- One padded chair measured folded: the listing says 90 × 10 × 47, and the cabinet allows 0.5 at each end of the base and 0.4 per chair in depth.
- The ideas they move into the plan ("Add to plan"): each chosen one moves into `build_doc.TRACK` (with a `costs.SHORT` name) and out
  of the ideas, so the one count stays one count.

## Ideas
- Decide could set the switch's real place in the 3D room (tap the wall) and move the scene button idea there.
- Build day for the media wall's steps could get its own "Watch this step" (the drawers, the uprights going up), like step 11's.
- The places strip could carry each place's own still (the pins' card has facts only).

## Rebuild and ship
`cd media-wall/src && python3 make_images.py && python3 export3d.py && python3 shot3d.py && python3 build_doc.py && python3 build_viewer.py`.
Then upload `src/deck_assets_todo.txt` to the deck's asset store, record them in `src/deck_assets.json`, run build_viewer again, QA at
390 and 1280 px (`python3 qa.py <shots dir>`, `python3 taptest.py <shots dir>`; check the PDFs' page counts and sizes), update HANDOFF
and README, PR into `main` (merge only when the client says), publish the deck.
