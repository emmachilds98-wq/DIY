# v19 upgrade plan (for the next agent)

Read `media-wall/HANDOFF.md` first (START HERE, then rounds 12 and 12b). v18.1 is built and merged into `main` (GitHub Pages:
https://emmachilds98-wq.github.io/DIY/). Work on a branch from `main`, open a PR into `main`, and merge it when the client asks.

## Where things stand
- The plan PDF has 72 pages and the build guide 48. Total £3,103–6,323. The fit proof has 87 checks: 59 fit, 21 tight, 7 to check on
  site, none fail. There are 14 open questions in `src/questions.py`.
- The client's plant stand (98 × 29.5 × 158) and vinyl stand (70 × 32 × 78) are drawn from their listings. There are two layouts
  (`geometry.PLANT_LAYOUTS`):
  - **A (recommended):** the plant stand in the window corner, the vinyl stand on the breast.
  - **B:** the other way round.
- The 3D room has an edit mode. You can move, turn, recolour, remove and add things, and tap a surface to paint it. Layouts are saved
  per device in localStorage (`S.layout`, `S.added`).
- The shared deck (https://claude.ai/artifact/71ffwf5PRLhoLj6G5KTvm2) has been "not found" from this account since round 11. It is still
  on v16.

## The work, in order
1. **Dining chair storage** (the client: "chair storage can be added somewhere also for the dining chairs, optional not essential unless
   easily done to the original table without many changes ... put in next run"). Don't redesign the flip-top. Options to draw and
   compare, cheapest first:
   - **Folding chairs on wall hooks** on the stairs wall. Use the 51 cm between the table's window end (z −235) and the pipe boxing
     (z −286), or the 41 cm between the stair box (z −84) and the table's other end (z −125). Folded chairs are about 45 × 80 × 5:
     check a real model and cite it. A slim oak rail with two or three hooks is about £20–40.
   - **Under the stairs** (the open side by the door) if there's room. Ask for a photo.
   - **The garage** (no change to the room). Say what that costs in convenience.
   Add `geometry.CHAIR_STORE`, a fit zone, a buy-list row, the drawing in `render.west_end` / the 3D (folded chairs as boxes), a
   question (how many chairs, folding or not; the `chairs` question already exists, so extend it), and a "See it in 3D" button if it's
   drawn.
2. **LP counts:** the vinyl stand adds about 100 LPs. The overview row ("Every LP face-out: about {LPS}"), `questions.LPS`, the README and
   the records section still count only the wall's 191. Add `RECORD_SHELF["lps_top"] + ["lps_bottom"]` in both layouts.
3. **The window corner is tight:** the plant stand has 4.5 cm a side between the curtains' stack (x 338) and the pipe boxing (x 445).
   Ask the client to tape that gap at floor level. If it's short, offer to slide the curtain pole's west end in, or swap to layout B.
4. **Edit mode follow-ups** (the client asked for "optimising user function"):
   - Undo (the last 10 moves).
   - Snap to walls: hold a thing's back against the nearest wall when within 5 cm.
   - A "Copy" button for added things.
   - Show each thing's size in the panel.
   - Let the sofa be moved as well: it's in export3d's `fixed` group today, so give it its own group.
   - If the deck can be reached again, save layouts in its db (the `db` capability) so Emma and Dave share one layout. Load the
     `artifact-capabilities` skill first.
5. **HD crash:** v18 caps shadowed spotlights at 4, saves phone pictures at 2560 × 1440, and handles a lost WebGL context. Ask the client
   whether HD still crashes, and on which device. If it does, drop the RectAreaLights in HD on phones: they are the costliest shader
   inputs.
6. **The deck:** ask the client to open the 71ff link and say whether it still exists, then reshare it or confirm it's gone. Only
   publish a new artifact with their say-so: their saved answers live in the old one.

## Then
1. Rebuild: `cd media-wall/src && python3 make_images.py && python3 export3d.py && python3 shot3d.py && python3 build_doc.py && python3 build_viewer.py`
   (shot3d is about 5 minutes now).
2. QA the page at 390 and 1280 px (`/tmp` scripts aren't kept: open each tab, check `scrollWidth`, check for console errors, start the 3D
   room and try Edit room).
3. Update HANDOFF (round 13, v19) and the README. Commit, push, PR into `main`, and merge when the client asks.

## Keep
The client's words ("face-out", "spine-up", "artisan oak", "tray", "deck"). Use plain language. Cite a source for every size. Back up
before large edits, and regenerate outputs rather than hand-editing PNGs. Before every push: fetch, and check the branch head is yours.
