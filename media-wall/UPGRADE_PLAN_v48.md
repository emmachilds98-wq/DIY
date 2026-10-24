# v48 upgrade plan: a more real room, and the garden seen from one floor up

Client (24 Oct): "Can we now plan on improving the renders graphics and quality of the render even further for the next upgrade. It's a
floor up so take perspective into account." And: "Eventually we're going to build the whole house so keep any info you need": the house's
facts are now in `house/HOUSE.md` (floors, rooms, the back of the house, the garden, what we still need).

Starts from `main` at v47.2. The standing rules hold: the core plan gets the full build; options stay one line each; say less. The phone
(Fast) must stay as quick as now; the bigger changes go into HD and into Save as HD picture.

## What the review found (stills at 1280, HD and Fast, day and evening)

1. **The garden is a flat photo at eye level.** From the sofa you look straight at the lawn, as if the room were on the ground. The room is
   about 2.6 m above the lawn: from the sofa the sill hides the whole lawn and you see the treetops, the neighbours' roofs and the sky;
   only close to the glass do you look down onto the lawn. The photo also doesn't move as you move (no depth).
2. **The glass is empty.** By day it has no reflection; in the evening a real window turns into a dark mirror of the lit room, and ours
   doesn't.
3. **Reflections come from a stock room, not ours.** The TV, the glass case, the bar's glass and the oak show a generic grey room.
4. **Surfaces are plain colours.** The oak has no grain, the sofa's velvet and the curtains no weave, the walls and ceiling no texture;
   up close everything looks like plastic.
5. **Lights don't glow.** The LED strip, the lamp's shades and the spot heads are bright but have no soft halo, and the spots throw a
   hard-edged even pool, not a beam.
6. **No sun.** By day the light through the window is a flat fill; nothing casts the window's bars onto the floor.
7. **Save as HD picture** is the live HD view at a larger size, with the same limits.

## 1. The garden from one floor up (perspective)

- **A real garden outside, not a picture on a wall.** The lawn as a ground 2.6 m below the room's floor, the fences on both sides, the
  trees at the far end, the neighbours' backs of houses beyond, and a sky. Sizes from `house/HOUSE.md`; the garden's length we ask for.
- **The photo laid onto it from where it was taken** (the dormer, one storey above the room): the lawn, path and plants land on the ground
  and the trees stand up at the end, so the view is right from every place in the room: treetops and sky from the sofa, the lawn when
  you walk to the window. It moves with you (depth), day and dusk.
- **Checked with the client's own video frame** (taken in the room): the same spot in the room should show the same view.

## 2. Glass that behaves like glass

- **Evening:** the window reflects the lit room faintly over the dusk garden, as real glass does; the curtains closed hide it.
- **Day:** a light sky sheen on the glass; the glass case and the bar's glass reflect the room.

## 3. The room's own reflections

- One capture of the room itself (once when it changes, not every frame) replaces the stock room in reflections: the TV, the glass
  case and the oak's sheen show the room's own lights.

## 4. Real surfaces

- **Artisan oak** with grain and a satin sheen, the **velvet** and **curtains** with a weave, **walls** with a fine matt texture, the
  **ceiling** as it is now (Artex), the **floor** with its pile. Made by our scripts (no downloads), small files, HD only on a phone.
- The dining cabinet, the table and the shelves keep the colours you chose; only their surfaces change.

## 5. Light that glows

- A soft **glow** round the LED strip, the lamp's shades and the lit spot heads (HD).
- The **spots** throw a beam with a soft edge and a brighter centre (the real heads' pattern), not an even disc.
- The presets (Evening, Bright, Cosy, Film) rechecked so nothing washes out.

## 6. The sun (day)

- Daylight comes in through the window and casts the window's bars and the plants on the sill onto the floor and the sofa, softly.
  Its direction needs one answer from you (which way the back of the house faces). Off in the evening.

## 7. Save as HD picture: near-photo quality

- **Save as HD picture** takes a few seconds longer and traces the light properly (soft shadows, light bouncing off the walls, glass
  and reflections): the nearest thing to a photo of the finished room. A progress ring shows while it works; the live view is
  unchanged. If a phone can't do it, it saves the picture as now.

## 8. Ready for the whole house

- The garden, the heights and the window's design come from one place (`house/HOUSE.md` and `geometry.py`), so the next room (the
  kitchen below, a bedroom above) reuses the same garden and the same outside.

**Section 1 done 24 Oct (v48.1)** from the client's three photos of the view (taken upstairs, rebuilt 2.6 m lower).

## Questions for you (each makes one part right; we can start without them)

1. About how long is the garden from the house to the far fence (steps are fine)? The photos put it near 15 m.
2. Which way does the back of the house face (for the sun)? A compass reading at the window is enough.

## Order

1. This plan and `house/HOUSE.md`, merged.
2. Section 1 (the garden from one floor up), merged.
3. Sections 2 and 3 (glass, the room's reflections), merged.
4. Sections 4 and 5 (surfaces, glow), merged.
5. Sections 6 and 7 (sun, HD picture), then rebuild, checks (phone speed checked against now), HANDOFF, README, merged.
