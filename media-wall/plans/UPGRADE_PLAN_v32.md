# v32 upgrade plan (for the next agent)

Read `media-wall/HANDOFF.md` first (START HERE, then round 25).

## Waiting on the client
- Which option beside the cabinet they'd like (clear, the mirror, the trolley, the low oak shelf); put the chosen one in the buy list.
- The seat pads' colour (olive drawn, honey or ivory) and whether they'd rather have ÄNGSFRÄKEN (no ties) or BRÄMÖN (thinner).
- Whether they want the 80-wide table (10 cm off the cabinet's length) offered in the review.
- One measured FRÖSVI, folded: IKEA publishes only its 9 cm package. Over 9 and two won't stand two deep: the Habitat chair folds to 7.

## Checks on site (fit proof CHECK rows)
- The table door on its piano hinges: hang it, open it flat, check its far end doesn't drop before loading the cabinet.
- The trailing plant: the open table door ends 5.7 short of its pot; the trolley reaches 5.5 into its longest strands.

## Ideas
- Tap-to-work for more things (the window blinds, the vinyl stand, the beside options).
- A live mirror (three's Reflector) on HD only, if the sheen texture doesn't convince.

## Rebuild and ship
`cd media-wall/src && python3 make_images.py && python3 export3d.py && python3 shot3d.py && python3 build_doc.py && python3 build_viewer.py`
then upload `src/deck_assets_todo.txt` to the deck's asset store, record them in `src/deck_assets.json`, run build_viewer again, QA at
390 and 1280 px (`python3 qa.py <shots dir>`, `python3 taptest.py <shots dir>`; check the PDFs' page counts), update HANDOFF and README,
PR into `main`, merge, publish the deck.
