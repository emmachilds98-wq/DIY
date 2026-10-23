# v45 upgrade plan: stipple ceiling, Cosy first, a softer table light, two small room buttons, a final tidy

Starts from `main` at v44. The client (23 Oct): "I want [Artex] stipple ceiling as default and cosy lighting that still allows nice view
of the room and stop over lighting the dining table it flushes it out too much. Then do a final review and upgrade of the repo. Make
whole room and remove labels button smaller buttons on the room not a part of the navigations tab buttons".

## 1. The room opens as you'd live in it

- **Artex stipple ceiling by default** (`decor.ceiling: "stipple"`, also in `geometry.FIRM`, so Back to my plan keeps it). The other
  designs stay in Look. The plan's ceiling line stays an option with its cost and the asbestos test.
- **Cosy by default** (evening). Cosy gets a little more light where it helps you see the room: the ceiling strip and bar 2 up a
  touch, the uprights and the lamp as they are. Checked against stills of the whole room and the media wall.
- **Saved settings:** a one-time switch moves an existing saved room to Cosy and the stipple ceiling, once; after that your own
  choices stay.

## 2. The dining table no longer washed out

- The table rule raised bar 2 to at least 80 over the table. New rule: bar 2 between 45 and 60 with the table open, bar 1 down as now.
  Checked with stills of the table open for six, in Cosy and Bright, by the oak top's brightness (no white patches).
- The plan's lighting text (`scenes.py`) says the new rule and that Cosy is the default.

## 3. Two small buttons on the room

- **Whole room** leaves the dock (the dock keeps View, Room, Look, Edit).
- **Labels** comes back (hidden since v39) as **Hide labels / Show labels**.
- Both are small pills on the room itself, bottom right above the dock (icon only on a phone), not tabs.

## 4. A final review and tidy of the repo

- Checks: `qa.py`, `taptest.py`, `clash.py`, the text budget, broken links in the README.
- **README** to what's needed now: what it is, open the plan, what's new in v45, the documents, how to rebuild. Older "New in"
  notes stay in HANDOFF and git.
- **HANDOFF's START HERE** down to the current state and the next tasks.
- **The 385 backup files** in `src/` move into `src/backups/` (git keeps them too); nothing imports them.
- **Old upgrade plans** (v17–v43) move into `media-wall/plans/`.
- **Size:** `media-wall/out/v9`–`v42` hold about 4.2 GB of old renders and PDFs (the published site carries all of it). Removing them
  from the working tree (they stay in git history) is recommended but left to the client to say yes.

## 5. Order

1. This plan, merged.
2. Sections 1–3, rebuild, checks, merged.
3. Section 4, HANDOFF round 40, README, merged; the viewer republished.
