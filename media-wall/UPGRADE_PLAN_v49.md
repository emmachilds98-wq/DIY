# v49 upgrade plan: the real sun, the 25 m garden, a lighter page

Client (24 Oct): "This is the rear side of 13 Portsmouth close facing Darnley road. Me2 2qy. Roughly 25m long. Continue any other upgrades"

Starts from `main` at v48. The standing rules hold: the core plan gets the full build; options stay one line each; say less.

## What the address tells us

- **The back of the house faces 14° east of north** (north-north-east), towards Darnley Road: the terrace at the head of Portsmouth Close,
  its long walls on a bearing of 104° (OpenStreetMap buildings and roads; ME2 2QY at 51.391 N, 0.468 E, postcodes.io).
- **The sun through the living room window** (the sun's path at 51.39 N): only from late March to mid September, and only early in the
  morning (05:30–08:30 BST at midsummer), low (5–30° up) and from the right, 45–80° off straight out; at midsummer a last grazing
  minute from the left around 20:00. From the autumn to the spring equinox, never.
- **So:** no sun on the TV or the screen wall, ever; even, cool north light by day; the plants on the sill want shade-tolerant kinds
  (they are already).

## 1. The sun as it is

- `geometry.SUN`: 7 am in June (61° to the right of straight out, 18° up), the morning the room gets its most sun. The 3D room's daytime
  shows that: a low beam from the right across the room, the bars on the left wall and the floor.
- `house/HOUSE.md`: the house's direction, the sun's times, the sources.

## 2. The garden 25 m long

- `house/HOUSE.md`: about 25 m to the far fence (the client); the photos see the lawn to the trees at about 17 m.
- `garden_window.py`: the far end 25 m out (was 30 m); rebuild the day and dusk views.

## 3. The plan

- The room's facts: the window faces north-north-east; one line on the sun and the TV. "What changed" for v49.

## 4. A lighter page

- The viewer's 29 inlined pictures go into the artifact's asset store (`src/deck_assets_todo.txt`), so the shared page loads quicker.

## 5. Rebuild, checks, HANDOFF, README, publish

- `clash.py`, `qa.py`, `taptest.py` at 390 and 1280; HANDOFF round 44; README; the viewer republished; merged to `main`.

## Still to ask

- Path-traced "near-photo" pictures (minutes each in the browser): yes or no.
- Save each set-up: on the shared page's database, or on Firebase if they set it up.
- The side-wall socket's distance and height.
