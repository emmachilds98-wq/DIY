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

## Design review of v32 (21 Oct): six upgrades, with mockups
The mockups are on a design canvas: https://claude.ai/artifact/SWtnzbiJgb3bhH2EFCXygE (private to Emma's account; share it from its
Share menu). Reviewed from the live page at 1280 and 390 px. Keep: the room as the home screen, the tools always on, tap the cabinet to
work it, Watch it open, the cost overview, a render for every idea. To upgrade, in order of what the client feels most:

1. **Phone home (board 1).** On a 390 screen the room sits small in the middle and the six labels stack into a column over it (the
   push-apart in `placeStickers` moves each one down until it's clear, so on a narrow screen they become a list), with the tip on top.
   Proposal: the camera frames the room tighter in portrait; the labels become numbered pins (no text) with a Places strip and a
   docked card for the picked place below the room (its facts, Watch it open, In the plan); the set-ups (`MOMENTS`: dinner for six,
   lunch for four, film night, morning) as chips under the room instead of deep in Layout; Menu joins the tool dock.
2. **One count (board 2).** The plan's ring says 0 of 66 bought; the Buy sheet says "2 of 91 items and jobs ticked off", and "still to
   buy" equals the whole plan. Use one model (66 things to buy, 13 steps, the choices) everywhere, and say which of the 91 are jobs.
   The plan home gets "Waiting on you" (the open choices), "Checks on site" (the two CHECK rows) and "Where the money goes" (the 12
   pieces from `costs.overview`, as ranges), filling the empty space beside the rings.
3. **Decide (board 3).** Since the Ask sheet went, the open choices (beside the cabinet, the pads' colour, the 80-wide table, where the
   light switch is) live only in this file. A short flow, one choice per screen with the renders already made (`3d_beside_*`), saved
   to the deck's db so both see it, and the buy list follows the pick.
4. **Ideas shortlist (board 4).** 31 ideas can be tried in the room but not chosen. Add "+ Add to plan" on each card, a running
   "+£x–y" and the plan's new total; a chosen idea moves into `build_doc.TRACK` (with a `costs.SHORT` name) as this plan already says.
   Filter chips (Light, Plants, Soft things) instead of 21 chips in a wall.
5. **Compare (board 5).** The compact cabinet, the sliding cabinet and the flip-top side by side: size on the wall, wall left free,
   seats (comfort and squeeze), chairs packed away, cost, the one thing to watch, Show in the room. The flip-top's cost needs
   re-pricing (last priced in v26, before the beech FRÖSVI).
6. **Build day (board 6).** A step as a phone screen: the room showing it with Watch this step, the step's tasks to tick (from
   `steps()[n]["do"]`), the tools to hand, the parts to buy, Done. Step 11 drawn; the same for every step.
