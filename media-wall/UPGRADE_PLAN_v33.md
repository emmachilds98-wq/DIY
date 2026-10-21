# v33 upgrade plan (for the next agent)

Read `media-wall/HANDOFF.md` first (START HERE, then round 26).

## Waiting on the client
- Still open from v31: the option beside the cabinet (clear, the mirror, the trolley, the low oak shelf), the seat pads' colour, the
  80-wide table, one measured FRÖSVI folded (IKEA publishes only its 9 cm package).
- Which of the ideas and suggestions they'd like in the plan: each is on its own card with a render now. A chosen one moves into the buy
  list (`build_doc.TRACK`, with a short name in `costs.SHORT` so the cost overview names it) and out of the ideas.
- Where the light switch by the door really is: the scene button idea is drawn on the chimney breast's side, beside the door frame.

## Checks on site (fit proof CHECK rows)
- The table door on its piano hinges: hang it, open it flat, check its far end doesn't drop before loading the cabinet.
- The trailing plant: the open table door ends 5.7 short of its pot; the trolley reaches 5.5 into its longest strands.

## Ideas
- "Watch it open" for the flip-top (the alternative) too, if the client still looks at it.
- Tap-to-work for more things (the blind up and down, the vinyl stand, the beside options).
- The Edit room stand-ins (`room3d.js` CATALOGUE) are simple shapes at real sizes; give the armchair, beanbag and bookcase more detail
  if the client wants their renders closer to real pieces.

## Rebuild and ship
`cd media-wall/src && python3 make_images.py && python3 export3d.py && python3 shot3d.py && python3 build_doc.py && python3 build_viewer.py`
(shot3d now renders the item stills too: `item_shots.py`, one per idea, suggestion and Add-list piece; their cameras are `item_shots.AIM`,
tuned by eye). Then upload `src/deck_assets_todo.txt` to the deck's asset store, record them in `src/deck_assets.json`, run build_viewer
again, QA at 390 and 1280 px (`python3 qa.py <shots dir>`, `python3 taptest.py <shots dir>`; check the PDFs' page counts and sizes),
update HANDOFF and README, PR into `main`, merge, publish the deck.
