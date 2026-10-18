# Notes for Claude and other agents

- Start with `media-wall/HANDOFF.md`: it holds the current state, the client's decisions, the true room geometry and the next tasks in order.
- The client (Emma, with Dave) iterates in short messages and expects a full updated plan (PDF), labelled HD renders and the viewer artifact each round. Keep their words: "face-out", "spine-up", "artisan oak", "tray".
- Accurate room measurements are in `media-wall/inputs/room_sketch_accurate_mm.png` and summarised in HANDOFF section 1. They override every earlier assumption (225 × 50 alcove, 220 ceiling).
- Every item's size in the plan must come from a cited source; add it to the plan's Sources list.
- Back up `render.py` / `build_doc.py` before large edits; regenerate outputs rather than hand-editing PNGs.
- Don't scrape Rightmove (robots-blocked); ask the client for screenshots instead.
