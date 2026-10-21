# v31 upgrade plan (for the next agent)

Read `media-wall/HANDOFF.md` first (START HERE, then round 24).

## Waiting on the client
- Which cabinet they want: the compact one (the plan, 144 long, hinged doors) or the sliding one (198, the alternative). If they
  pick the sliding one, its buy rows are `build_doc.SLIDE_ROWS` and its cutting list and step 11 are in `build_doc_v29_1_backup.py`
  and `instructions_v29_1_backup.py`: swap them back in (keep the `TRACK_KEEP_ID` entries so their ticks stay).
- The doors' finish: plain oak (drawn), fluted or reeded oak, or painted in the wall colour with oak ends.
- The ottoman's height (`SOFA_POUF["h"]`) and the window corner's floor gap, if they ever say.

## Checks on site (fit proof CHECK rows)
- The table door on its piano hinge: hang it, open it flat and check its far end doesn't drop before loading the cabinet.
- The trailing plant on the shelf: the open table door ends 5.7 short of its pot (tuck the strands aside or slide the pot along).

## Ideas (only if the client wants them)
- An LED strip inside each box's top, on a door switch.
- Tap-to-work for more things in the 3D room (the windows' blinds, the vinyl stand's records).
- The 2D renderer (render.py) still has no dining cabinet: a drawn elevation of the stairs wall in the "Drawn views" set.

## Rebuild and ship
`cd media-wall/src && python3 make_images.py && python3 export3d.py && python3 shot3d.py && python3 build_doc.py && python3 build_viewer.py`
then upload `src/deck_assets_todo.txt` to the deck's asset store, record them in `src/deck_assets.json`, run build_viewer again, QA at
390 and 1280 px (`python3 qa.py <shots dir>`: "fails" and "errors" empty; check the PDFs' page counts too), update HANDOFF and README, PR into `main`, merge, publish the deck.
