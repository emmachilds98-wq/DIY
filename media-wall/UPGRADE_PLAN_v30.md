# v30 upgrade plan (for the next agent)

Read `media-wall/HANDOFF.md` first (START HERE, then round 23).

## Waiting on the client
- How they like the upgraded dining cabinet (two sliding doors, 185 table, folding chairs), and the doors' finish: plain oak (drawn),
  or fluted/reeded oak, or painted in the wall colour with oak ends.
- The ottoman's height (`SOFA_POUF["h"]`), the window corner's floor gap, and the open questions on the Ask sheet.
- When the Slido track arrives: its section, against the 5 cm allowed (fit row "The doors' depth").

## Ideas (only if the client wants them)
- An LED strip inside the cabinet's top, on a door switch, so the bays light when a door slides.
- The 2D renderer (render.py) still has no dining cabinet: a drawn elevation of the stairs wall in the "Drawn views" set.
- Animate the doors sliding in the 3D room.

## Rebuild and ship
`cd media-wall/src && python3 make_images.py && python3 export3d.py && python3 shot3d.py && python3 build_doc.py && python3 build_viewer.py`
then upload `src/deck_assets_todo.txt` to the deck's asset store, record them in `src/deck_assets.json`, run build_viewer again, QA at
390 and 1280 px, update HANDOFF and README, PR into `main`, merge, publish the deck.
