# v36 upgrade plan (for the next agent)

Read `media-wall/HANDOFF.md` first (START HERE, then round 29).

## First: what the client sees now
- Read the error log before anything else: ArtifactData `list` on `errors` on the deck (each doc has the message, stack, state, device
  and GPU), or ask the client to open the room and run `R3D.errors()` in the console, or to send a screenshot of the room with `?perf`
  added to its address (quality, frames a second, draw calls, shaders, lights). Ask which device and app the crash was on, if it's back.
- If an error is in the log, fix it first; add the case to `qa.py` or `edit_probe.py`.

## The 3D room, the rest of the lighter plan (from `UPGRADE_PLAN_v34.md`'s list; steps 1, 3's shadow set, 5's start-in-Fast, 6's
## context loss and pause, 7, 8, 10 are done)
1. **Draw calls ~450 in Fast → ≤ 120.** `BufferGeometryUtils.mergeGeometries` the static oak per material (the media wall's carcass
   and shelves, the stairs, the cabinet's carcass); `InstancedMesh` for what repeats (LP sleeves, game cases, spindles, the six chairs
   one mesh per part animated by instance matrices, plates, the plant stand's pots and leaves). Keep each `HOTS`/tap target pickable
   (a merged mesh needs an id per part: a vertex attribute or a box list).
2. **Build ideas, suggestions and the Edit room's catalogue on first show** (today all are built at load and hidden): a shorter
   start and a smaller warm-up queue. `precompile()` already handles parts that appear later (call it after building one).
3. **Contact shadows in Fast** (a blurred dark ellipse under the sofa, the cabinet, the table, each Edit-room piece).
4. **Textures ≤ 1024², anisotropy ≤ 4**, the rug's 1150 × 800 canvases to 1024 × 512; the sky 512 × 256.
5. **Adaptive resolution** (step 5's second half): median of 30 frames over 25 ms steps the ratio down 0.15 (not below 0.6), back up
   after 3 s under 12 ms. Watch it doesn't resize the canvas often (each resize reallocates the drawing buffer: round 29's profile).
6. Re-measure with `perf_probe.py` and `edit_probe.py` (both with `THREE_LOCAL`), and `R3D.perf()`.

## The deck
- Still at v32 (round 28 and 29's sessions couldn't open https://claude.ai/artifact/71ffwf5PRLhoLj6G5KTvm2 from their account). From
  Emma's account: upload `src/deck_assets_todo.txt` (Artifact `asset: true`, 25 a call), record them in `src/deck_assets.json`, run
  `python3 build_viewer.py`, publish `src/media_wall_viewer_inline.html` to it. The error trap writes to its db (`errors/`) once it's v35.

## Waiting on the client (unchanged from `UPGRADE_PLAN_v35.md`)
- Decide: beside the cabinet, 90 or 80 wide, the light switch's place (and the box above the switch on the stairs wall).
- The bar: A (drinks cabinet under the case), B (the trolley), both or neither.
- The storage ottoman: the ISTOOLS 76's height and price, or the Dunelm 62.
- The Technics SL-220's open-lid height (swap `geometry.DECK`, with a source).
- The padded chairs' price, one chair's open depth and folded size.

## Rebuild and ship
With `THREE_LOCAL` set: `cd media-wall/src && python3 make_images.py && python3 export3d.py && python3 shot3d.py && python3 build_doc.py
&& python3 build_viewer.py`; QA at 390 and 1280 (`python3 qa.py <dir>`, `python3 taptest.py <dir>`); HANDOFF and README; PR into
`main`; the deck.
