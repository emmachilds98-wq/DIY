# Notes for Claude and other agents

- Start with `media-wall/HANDOFF.md`: it holds the current state, the client's decisions, the true room geometry and the next tasks in order.
- The client (Emma, with Dave) iterates in short messages and expects an updated plan (PDF) and the viewer artifact each round. **No HD stills** (client, 23 Oct 2026: "we dont need the hd still i can take them in the site"): `shot3d.py` is no longer part of the rebuild; the plan uses the newest still made (`build_doc.latest`), and the client takes pictures with Save as HD picture in the room. Keep their words: "face-out", "spine-up", "artisan oak", "tray".
- **Core plan vs options (client, 23 Oct 2026):** "We want the core plan build and info then the additional items are just for looking at possible other designs and we don't need full build unless I say." The core plan (`geometry.FIRM`, see `UPGRADE_PLAN_v38.md`) gets the full build, buy list and fit proof. Options are only to look at in the 3D room, with one line each (what, where, size, rough cost, source): no build steps, no buy rows, no guide pages, unless the client asks for one by name.
- **Say less, everywhere:** "make sure we're not overfilling the text everywhere". Short captions, cards and toasts; plan sections say what, where, size, cost and how, then stop. History stays in HANDOFF and git, not in the plan or the page. Keep improving the page's design and flow each round (fewer buttons, clearer paths), not only adding to it.
- Accurate room measurements are in `media-wall/inputs/room_sketch_accurate_mm.png` and summarised in HANDOFF section 1. They override every earlier assumption (225 × 50 alcove, 220 ceiling).
- Every item's size in the plan must come from a cited source; add it to the plan's Sources list.
- Back up `render.py` / `build_doc.py` before large edits; regenerate outputs rather than hand-editing PNGs.
- Don't scrape Rightmove (robots-blocked); ask the client for screenshots instead.
