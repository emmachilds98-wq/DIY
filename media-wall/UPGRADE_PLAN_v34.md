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

## The 3D room: crashes, errors and lag (client, 21 Oct: "it currently still crashes in the claude version and has some errors in the web mode when trying to make changes. it also is a bit slow on the render sometimes becoming HD")

### What we measured (v33, `index.html` at 1280 × 800, headless SwiftShader while the stills rendered: the milliseconds are inflated, the counts are real)
| | Now | Target |
|---|---|---|
| Meshes · draw calls · triangles | 1,027 · 277 · 86k | ≤ 120 draw calls |
| Lights in the scene · on in Fast · on in HD | 32 · 9 · 21 (11 spots, 4 casting shadows) | ≤ 8 on, the same count always |
| Shadow maps (HD) | 4 × 1024² (saves: up to 6 × 2048²) | ≤ 2, and only redrawn when something moves |
| Shader programs | 69 at load → 87 after the first lighting change | the same after load (0 recompiles) |
| A lighting change (Film) · opening the table for six | 16 s · 55 s | < 0.1 s |
| Edit room: add a piece · turn · drag | ~5 s · ~2 s · 10–12 s | < 0.1 s each |
| Startup (JS build) | 3.5 s (38 s to the first frame in SwiftShader) | first frame < 3 s on a mid phone |
| Console | "THREE.Color: Unknown color glass / art" warnings | none |

**The cause of the "sometimes becoming HD" stall:** three.js keys every material's shader on the number of visible lights (and which cast
shadows). `applyLight()` toggles `light.visible` and `castShadow` whenever a level reaches 0 or a rule changes (a lighting scene, the
table rule turning bar 2 up when the table opens, a suggestion's light), and `MATS.forEach(m => m.needsUpdate = true)` follows the HD
switch, so every one of ~70 materials recompiles. On a laptop GPU that's a visible freeze; on a phone, or in the Claude app's frame, it can
run out of memory (the crash).

### The plan, in order (each step measured with `R3D.perf()`, below, before and after)
1. **No more recompiles** (biggest win, smallest change). Never toggle `light.visible` or `castShadow` at run time: a light that's "off"
   gets `intensity = 0`; the shadow set is chosen once per quality (`capShadows`) and kept. Only the Fast ↔ HD switch may recompile, and
   then once, behind a short "Switching to HD…" note, using `gl.compileAsync(scene, camera)`. Precompile both qualities' programs during
   the loading message. Check: `gl.info.programs.length` is the same after every scene, table and suggestion change.
2. **Fewer lights** (21 → ≤ 8 in HD, ≤ 4 in Fast). The LED strips, uprights, TV bias, PC glow, cabinet bars and fairy lights become
   emissive materials plus, at most, one soft fill (a `RectAreaLight` or the hemisphere's colour) instead of point lights each. Each spot
   bar: one `SpotLight` for its four heads (the heads stay emissive). Lights belonging to ideas and suggestions are created only when that
   item is first shown, and then kept (intensity 0 when hidden), so the count never changes while you use the room.
3. **Shadows.** At most two shadow-casting spots in HD (bar 1 and bar 2), 1024², and `gl.shadowMap.autoUpdate = false` with
   `needsUpdate = true` only when something that casts moves (a door, the table, a dragged piece), not every frame. Small things stop
   casting (`castShadow = false` on plates, chairs' buttons, LPs, plants' leaves, records, cables). Fast keeps no shadow maps; a soft
   contact-shadow texture (a blurred dark ellipse) under the sofa, the cabinet, the table and each Edit-room piece gives them weight.
   Saves (`still()`) keep the bigger maps but build them once and dispose them after.
4. **Draw calls 277 → ≤ 120.** `mergeStatic` the cabinet's carcass, the media wall's `unit_in`/`unit_out`, the stairs, the shelves and
   frames; `InstancedMesh` for what repeats: the LP sleeves and game cases, the plant stand's leaves and pots, the stair spindles, the
   chairs (six identical: one instanced mesh per part, animated by instance matrices), the plates, the buttons. Ideas, suggestions and the
   Edit room's catalogue are built lazily on first show (today all 31 are built at load, hidden).
5. **Resolution.** Fast: pixel ratio 0.75–1; HD: `Math.min(devicePixelRatio, 1.5)` on a laptop, 1.25 on a phone; while you drag, 0.5
   (the `lowRes` path exists). Add an adaptive step: if the median of 30 frames is over 25 ms, step the ratio down 0.15 (never below 0.6);
   back up after 3 s under 12 ms. **Start in Fast everywhere** and move to HD only after three good frames (today it starts in HD on a
   laptop and drops if slow: the first impression is the slow one).
6. **The Claude-app crash.** Reproduce it first: ask the client which device and what they see (a blank frame, "ran out of graphics
   memory", or the app reloading), and open the deck 71ff on a phone and in the desktop app with DevTools' Performance monitor (JS heap,
   GPU memory). Likely causes, all fixed above: HD with 4 shadow maps at start, ~90 programs, 1,000 meshes, plus the page's images. Also:
   create the WebGL renderer only when the Room is on screen (the deck opens on it, but the Plan sheet shouldn't keep it rendering:
   pause `frame()` while a sheet covers the room), handle `webglcontextrestored` (rebuild materials and carry on in Fast instead of asking
   for a reload), dispose render targets and the save's 2048² maps after `still()`.
7. **The errors when making changes.** **Found (src/edit_probe.py, 1280 × 800):** after Look → walnut and Look → floorboards, the dock's
   **Lights and Extras bubbles and the Film scene button couldn't be clicked** (Playwright: the element resolved but something else took
   the click for 4 s+). Something covers the dock after a Look change: check the open panel's box, the toast, `.r3d-phone`, the sticker
   layer and the `measureShift` cover with `document.elementFromPoint` at the bubble's centre, fix it first and add the check to qa.py.
   Otherwise headless, Edit room's add / turn / recolour / drag / undo / remove / paint and the Look, Lights and
   Extras panels raised no page errors, only the colour warnings, but every change was slow (the recompiles and the shadow redraws
   above), which reads as broken on a phone. To catch what the client sees: a global trap (`window.onerror`, `unhandledrejection`, and
   `console.error` wrapped) that shows a small toast ("Something went wrong: …, it's been noted") and writes the message, the stack, the
   state `S` and the device (UA, DPR, GPU renderer string) to the deck's db (`errors/<time>`) and `localStorage`; read them with
   ArtifactData next round. Fix the warning: `boxGeo` / `softGeo` / `frameGeo` build vertex colours from the fill name, so "glass" and
   "art" (kinds, not colours) go to `THREE.Color`; use white for any fill that isn't `#rrggbb`.
8. **The frame loop.** It's already allocation-free (`_p`, `PX` reused) and only renders when something changed (`need`). Two leaks of
   time: `placeStickers()` reads `offsetWidth`/`offsetHeight` after writing `style.left/top` in the same loop (a forced layout per
   sticker per frame): cache each sticker's size on resize and font load; and `updateCut()` / `clampRoom()` run every frame even when the
   camera hasn't moved: skip them when `!active`.
9. **Textures.** 19 textures: the oak grain canvases (`OAK_TEX`, `OAK_TEX_V`), the sky (day/night), the mirror sheen, the LED panel: keep
   each ≤ 1024² and power-of-two, `generateMipmaps` on, `anisotropy` ≤ 4; the sky can be 512 × 256.
10. **Measure it every round.** `R3D.perf()` returns `gl.info` (calls, triangles, geometries, textures, programs), the visible and
    shadow-casting light counts, the pixel ratio, and the median frame time of the last 60 frames; `?perf` in the URL shows a small
    overlay (fps, calls, programs) the client can screenshot. `qa.py` records these at 390 and 1280 and fails if programs grow after a
    lighting change, an Edit-room add or a table open, or if draw calls go over the target.

Work in this order (1, then 7's trap, then 2–5), push after each, and re-render the stills only once at the end (any change to
`room3d.js` re-renders all of them: about 90 stills).
