# v38 upgrade plan (for the next agent)

Read `media-wall/HANDOFF.md` first (START HERE, then round 31). Don't write the cap's poem out anywhere (round 31).

## First: the client's picks from v36 and v37
- Which bar: D built in beside the cabinet (v37), A under the glass case, B the trolley, C by the sofa, or none. A chosen one moves into
  `build_doc.TRACK` (with a `costs.SHORT` name) and out of `OPTION_GROUPS`/`ideas.SUGGEST`; its fit rows into a counted zone.
- The storage picks (v36 and v37), the window corner (seat, bench, cupboard or the plant stand as now), the blankets' home.
- Measure: the black shelf's stairs end (35 past the stair box as drawn; if 41, the shelf is about 194 long, the 10 gap stays); the
  door's architrave (the shelf over the door); the ottoman's inside depth.
- Still open from v35/v36: the error log (ArtifactData `errors` on the deck, or `R3D.errors()`), the deck (still at v32 from this
  account), the waiting items in `UPGRADE_PLAN_v36.md`.

## Ideas
- The step drawers and a bar or cupboards under the new stairs, drawn once the stairs are known.
- The hall: if the client sends its measurements, model a slice of it so the bench with cubbies, the shoe cabinets and the hook rail
  can be shown where they'd really go.

## The 3D room (carried)
Draw calls (~450 in Fast; target ≤ 120; v37 added the bar's bottles and glasses, the storage pieces: merge or instance them), suggestions
built on first show, textures ≤ 1024².

## Rebuild and ship
With `THREE_LOCAL` set: `cd media-wall/src && python3 make_images.py && python3 export3d.py && python3 shot3d.py && python3 build_doc.py
&& python3 build_viewer.py`; QA at 390 and 1280 (`python3 qa.py <dir>`, `python3 taptest.py <dir>`); HANDOFF and README; PR into
`main` and merge.
