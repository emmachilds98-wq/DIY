# v20 upgrade plan (for the next agent)

Read `media-wall/HANDOFF.md` first (START HERE, then round 13). v19 is built and merged into `main` (GitHub Pages:
https://emmachilds98-wq.github.io/DIY/), and published to the shared deck (https://claude.ai/artifact/71ffwf5PRLhoLj6G5KTvm2).

## Waiting on the client
1. **Chairs:** how many, whether they fold, and a photo of the side of the stairs by the door. If the space under the stairs is open, draw
   it (`CHAIR_STORE["under_stairs"]`), add a fit row that passes, and a 3D view. If they want more than two on hooks, a third hook fits only
   if the chairs hang behind each other (18 deep): check against the folded table's 13.3.
2. **The window corner:** the taped gap between the pipe boxing and the curtains' stack. If it's under 98 + 2, offer the curtain pole's
   west end in (and redraw `CURTAIN["ext"]`), or layout B.
3. **HD crash:** if it still crashes, drop the RectAreaLights in HD when `SMALL` (room3d.js `applyLight`: `area = hd && !SMALL ? 1 : 0`)
   and say so in the 3D tab's caption.

## Then, if there's time
- Edit mode: a "Save as a picture" of the plan from above (the bird's-eye view, lines on), and the layout's undo kept across reloads.
- The shared layout: if Emma and Dave use it, show who saved it (the `user` capability's profiles).

## Rebuild and ship
`cd media-wall/src && python3 make_images.py && python3 export3d.py && python3 shot3d.py && python3 build_doc.py && python3 build_viewer.py`
QA at 390 and 1280 px, update HANDOFF and README, PR into `main`, merge once checked (the client views Pages), publish the deck.
