# v29 upgrade plan (for the next agent)

Read `media-wall/HANDOFF.md` first (START HERE, then round 22). Everything in `UPGRADE_PLAN_v25.md` and `UPGRADE_PLAN_v25_UI.md` is done.

## Waiting on the client
- The ottoman's height (`SOFA_POUF["h"]`, drawn 44), the window corner's floor gap, the optimisation plan's three questions, and the
  open questions on the Ask sheet (15).
- Whether they like the tour's stops and captions, and the suggestions' versions (`ideas.SUGG_VARS`): easy to add or rename.

## Ideas for the next round (only if the client wants them)
- The tour from a sticker's popover ("Show me round from here"), or a short tour of just the dining cabinet opening.
- A "copy link" for a Plan chapter (the router already has a hash for each).
- Save several looks by name (the deck's db, `layouts/`), each with its link.

## Rebuild and ship
`cd media-wall/src && python3 make_images.py && python3 export3d.py && python3 shot3d.py && python3 build_doc.py && python3 build_viewer.py`
(shot3d skips the stills that haven't changed; `force` renders all) then upload `src/deck_assets_todo.txt` to the deck's asset store,
record them in `src/deck_assets.json`, run build_viewer again, QA at 390 and 1280 px, update HANDOFF and README, PR into `main`, merge
once checked, publish the deck.
