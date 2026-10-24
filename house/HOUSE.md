# The whole house: what we know

The living room's media wall is the first project (`media-wall/`). The client plans to do the whole house in time
("Eventually we're going to build the whole house so keep any info you need", 24 Oct 2026). This file keeps every fact about the
house in one place so later rooms start from it. Sizes are the agent's unless marked; the living room's own measured sizes win
over the agent's (they are in `media-wall/HANDOFF.md` section 1 and `media-wall/src/geometry.py`).

## Where it is (the client, 24 Oct 2026)

**13 Portsmouth Close, Strood, ME2 2QY**; the back faces Darnley Road. The terrace at the head of the close: its long walls run on a
bearing of 104°, so **the back of the house faces 14° east of north** (north-north-east; OpenStreetMap buildings and roads, the
postcode at 51.391 N, 0.468 E from postcodes.io).

- **Sun through the back windows** (the sun's path at 51.39 N): only from late March to mid September, early in the morning (05:30–08:30
  BST at midsummer), low (5–30° up) and from the right, 45–80° off straight out; at midsummer a last grazing few minutes from the left
  about 20:00. From the autumn to the spring equinox, none. The front (south-south-west) gets the sun the rest of the day.
- The living room: no sun on the TV or the screen wall, ever; by day even, cool north light. The 3D room's daytime sun is 7 am in June
  (`geometry.SUN`, 61° right of straight out, 18° up).

## Sources

| File | What it is |
|---|---|
| `media-wall/inputs/agent_floor_plans.png` | The selling agent's floor plans, three floors, 1224 sq ft (113.8 m²) in all |
| `media-wall/inputs/photo_house_rear_24oct.jpg` | The agent's photo of the back of the house and the garden |
| `media-wall/inputs/photo_garden_summer_24oct.jpg` | The garden in summer, taken from the dormer (1449 × 2576) |
| `media-wall/inputs/photo_garden_window_24oct.jpg` | A frame of the client's video through the living room window |
| `media-wall/inputs/photo_view_full_24oct.jpg` | The whole view out of the back from upstairs (ultra-wide, overcast, spring): the best one |
| `media-wall/inputs/photo_view_wide_24oct.jpg`, `photo_view_centre_24oct.jpg`, `photo_view_right_24oct.jpg` | The same view: wide, centre (looking down) and right |
| `media-wall/inputs/room_sketch_accurate_mm.png` | The client's measured sketch of the living room (mm) |
| `media-wall/inputs/photo_stairs_*`, `room_photo_*`, `photo_current_living_room.png` | The living room and the stairs up from it |

## Floors (the agent's plans)

The house is built into a slope: the garden is at the **lower ground floor**, so the **living room (the agent's ground floor) is one
storey above the garden**, and the bedrooms are above that, with dormers in the roof.

| Floor | Area | Rooms (agent's sizes) |
|---|---|---|
| Lower ground (garden level) | 369 sq ft | Kitchen 3.79 × 3.66 m (12'5" × 12'0"); WC 1.64 × 1.88 m; landing and stairs up; store; door to the garden; a large unexcavated area |
| Ground (the street door) | 424 sq ft | **Living room** 4.95 × 3.65 m (16'3" × 12'0"), rear window; entrance hall and stairs; garage; two stores |
| First | 431 sq ft | Master bedroom 2.91 × 4.45 m; bedroom 2 2.91 × 3.65 m; bedroom 3 2.04 × 2.17 m; bathroom 2.04 × 2.38 m; landing; airing cupboard |

The living room measured: 467 wide along the window, 347 from the window to the alcove's back wall, ceiling 235 (cm; the client's sketch).

## The back of the house (the agent's photo, left and right as seen from the garden)

- Red brick, a tiled roof with a dormer of four casements; white uPVC windows with Georgian bars throughout.
- **Lower ground:** a window and a glazed door to the garden (the kitchen), a small window to the right.
- **Living room:** the middle window, three sections (0.24 / 0.52 / 0.24 of its width), a row of top lights, Georgian bars
  (`geometry.WINDOW_DESIGN`). Measured: 235 wide, 124 tall, sill 88 above the floor.
- **The living room floor stands about 2.6 m above the lawn** (estimated from the photo: the lower ground floor's door and windows
  under it, one storey of about 2.4 m plus the floor). Seen from the room, the garden is looked down on: the near lawn sits below the
  sill and only shows from close to the glass.
- A downpipe on the right corner; a gate in the gap on the left side; the neighbours' conservatory is on the right.

## The garden (left and right as seen from the house)

- A lawn about the width of the house, running away from it; a paved path down the left side.
- Cordylines (cabbage palms) by the path, a big clump near the house; a patio by the house with a round table and chairs.
- The left-hand neighbour: a gravel garden with pots and a lawn beyond; a low brown fence between.
- Close-board fences on both sides; tall trees with fine, divided leaves (ash-like) fill the far end in summer; the neighbour's
  trampoline over the right fence.
- The summer photo was taken from the dormer (the roof's tiles at its foot): one storey higher than the living room, so it looks down
  more steeply than the room does. The video frame is from the living room itself.
- Summer: green and full (the summer photo); spring: bare trees (the video, the view photos).
- **About 25 m long** to the far fence (the client, 24 Oct). The photos see the lawn to the trees at about 17 m (the camera's direction
  from the fences, its height from the man on the lawn; the neighbour's shed fronts line up with it); the rest is under the trees. A birch clump and a conifer at the end.
- **Beyond:** a long low building with grey roofs behind the end fences, then a valley and a hill of terraced houses opposite, a little
  above the living room's eye level. The right-hand neighbour has a shed with a shingle roof at the end (a trampoline, a rotary dryer).
- **Camera heights** (from the view photos, `media-wall/src/garden_window.py`): upstairs window about 6.7 m above the lawn; the living
  room's standing eye about 4.1 m.

## Not known yet (ask the client when a room needs it)

- Ceiling heights other than the living room's; floor-to-floor heights; wall thicknesses.
- The garden's width.
- The kitchen's layout; where the stairs sit on each floor beyond the living room's stair box.
- Window sizes for every room but the living room.
