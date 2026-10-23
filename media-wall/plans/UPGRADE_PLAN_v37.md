# v37 upgrade plan (for the next agent)

Read `media-wall/HANDOFF.md` first (START HERE, then round 30).

## First: the client's picks from v36
- Which bar (A under the glass case, B the trolley, C by the sofa, or none), which home for the blankets (the tall basket or the oak
  rail), which of the lift-top coffee table, the shelf over the door and the boxes on the black shelf, and the plant shelf. Each chosen
  one moves into `build_doc.TRACK` (with a `costs.SHORT` name) and out of `ideas.SUGGEST` / `OPTION_GROUPS`, so the one count stays one
  count; its fit rows move from `fit.storage_zone()` into a counted zone. C's build goes into the appendix's A build (or step 9).
- The plant shelf: confirm "10 cm gap from the wall" (as drawn: the shelf's back 10 off the wall) or a 10-deep shelf against it; and
  whether the stairs end of the stairs wall is the place they meant.
- The ottoman: its real inside depth when it comes (12 games assume 28 deep); the door's architrave (the shelf over the door assumes 7).
- Still from v35/v36: the error log (ArtifactData `errors` on the deck, or `R3D.errors()` from the client), a `?perf` screenshot, the
  deck (still at v32 from this account), and the waiting items in `UPGRADE_PLAN_v36.md` (Decide, SL-220 lid, chairs).

## Ideas
- A "Games night" set-up in Layout's "Try a set-up": the ottoman's lid off, the coffee table's top up, Cosy.
- The blanket basket and the floor plant share a corner: offer the floor plant a second spot (by the window corner) so both can be on.
- Under the new stairs: a bar or cupboards, drawn once the stairs are known.

## The 3D room (carried from `UPGRADE_PLAN_v36.md`)
Draw calls (~450 in Fast; target ≤ 120), suggestions built on first show, contact shadows in Fast, textures ≤ 1024², adaptive resolution.

## Rebuild and ship
With `THREE_LOCAL` set: `cd media-wall/src && python3 make_images.py && python3 export3d.py && python3 shot3d.py && python3 build_doc.py
&& python3 build_viewer.py`; QA at 390 and 1280 (`python3 qa.py <dir>`, `python3 taptest.py <dir>`); HANDOFF and README; PR into
`main` and merge (the client: "make sure it goes on main and is merged when ready").
