# v23 upgrade plan (for the next agent)

Read `media-wall/HANDOFF.md` first (START HERE, then round 16). The client-facing plan is `media-wall/plans/optimisation_v21.html`
(https://claude.ai/artifact/P7D81ZQuuVKBvh8hX2k5w6); its "v23" list, in order, unless the client answers otherwise:

1. **A guided tour and "copy link to this view"** (room3d.js): a Tour button that tweens through room, wall, sofa, dining, chairs and
   pc with a caption each; a link that carries the view and the choices (the page can only read a plain `#token` hash, so keep a few
   named looks, or save the look to the deck's db and link its id).
2. **Contents lists in the long tabs** (build_viewer): Media wall, Checks, Dining and Network get a short list of their sections at the top.
3. **Choices for each suggestion** (ideas.SUGGEST, room3d.js `buildSuggest`): two or three versions each, like the decor rows.
4. **Only re-render the stills that changed** (shot3d.py): a fingerprint of each shot's opts + room3d.js + scene3d.json; skip matches.

Also waiting on the client: the chair cupboard (four or six), the window corner gap, the stairs photo, the plan's three questions.

## Rebuild and ship
`cd media-wall/src && python3 make_images.py && python3 export3d.py && python3 shot3d.py && python3 build_doc.py && python3 build_viewer.py`
then upload `src/deck_assets_todo.txt` to the deck's asset store, record them in `src/deck_assets.json`, run build_viewer again,
QA at 390 and 1280 px, update HANDOFF and README, PR into `main`, merge once checked (the client views Pages), publish the deck.
