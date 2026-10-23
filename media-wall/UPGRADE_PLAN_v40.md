# v40 upgrade plan

Client (23 Oct): "Focusing on more HD realistic plants, better rendering and graphics as well as adding more options where you see
fit in the current room plan as well as any further optimisations in design or build."

Starts from `main` at v39 (round 33). The standing rules hold: the core plan (`geometry.FIRM`) gets the full build; options are to
look at in the 3D room, one line each in the plan; say less; no new shaders while the room is in use (v35); never write the cap's poem.

## 1. HD plants

**Today:** every leaf is a squashed sphere in one flat green, pots are plain cylinders with no soil. It reads as a toy.

**New:** a small plant library in `room3d.js`, shared by every plant in the room:

- **Leaves with real outlines:** each leaf is a shaped mesh (a grid along a profile per kind), folded along its midrib and curled
  towards its tip, with a painted texture (a lighter midrib, veins, a gradient from the stem, variegation where the plant has it)
  and a slightly different green per leaf (vertex colour), so no two match.
- **Six kinds**, picked to suit each spot: golden pothos (heart-shaped, trailing: the hanging plant, the sill's trailers, the stand's
  trailers), snake plant (upright banded blades), monstera (split leaves on long stalks: the stand's big middle plant), Boston fern
  (arching fronds), spider plant (arching striped blades) and calathea (oval patterned leaves).
- **Pots:** a turned profile with a rolled rim, soil showing at the top, terracotta with a fired texture, glazed ceramic and matte
  stone; a saucer under the terracotta.
- **Cheaper to draw:** each group's leaves merge into one mesh per kind and its pots into one per finish (today every plant is its
  own mesh), so the plant stand drops from about 40 draw calls to under 12.

## 2. Rendering

- **Ambient occlusion** (three's GTAO): the soft darkening where things meet (the sofa on the floor, the books on the shelf, the
  corners). On in **Save as HD picture** and on capable graphics cards in HD; the warm-up draws its parts the same way, so turning it
  on costs one compile, at the quality switch, never mid-use. The cutaway clips its depth pass too.
- **Sharper stills:** 2048 shadow maps with softer edges, and the leaves cast and catch shadows.
- **Checks:** `qa.py` (errors, the shader count unchanged while used), `R3D.perf()` before and after, test stills before and after.

## 3. More options (look only, one line each)

- **Plant style** in Look: your mix (the plan) / lush (more trailing, a large monstera) / easy care (snake plants and pothos).
- **Pot finish** in Look: as now / all terracotta / white ceramic / matte black.
- **Self-watering pots** on the stand and the sill (an option line with a source; no build).

## 4. Optimisations

- The plants' draw calls (above).
- **Dead code:** the flip-top and sliding cabinet paths left after v39 (site A/B, `buildOptC` remains) where they can no longer be
  reached; each removal checked with `qa.py` and `taptest.py`.

## 5. Order

1, 2, 3, 4; then rebuild (`make_images`, `export3d`, `build_doc`, `build_viewer`), QA, HANDOFF round 34, README, a PR into `main`.
