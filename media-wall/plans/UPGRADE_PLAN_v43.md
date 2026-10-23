# v43 upgrade plan: the C-table in the plan, the sill's plants as you have them, the room reviewed

Starts from `main` at v42 (round 37 and the v42 plan in HANDOFF). Read `media-wall/HANDOFF.md` first. Never write the cap's poem out in code, text or commit messages.

The client's brief (23 Oct 2026):
- "I want the c table in the current main plan and then review the room and suggest improvements and more item options."
- "Make the plants better definition and more real we have taller ones in the middle, spider plants on the right and some smaller
  ones on left", then: "I meant for the window sill, the plant shelf is not built yet give it what you think will look best".

Standing rules: the core plan (`geometry.FIRM`) gets the full build, buy list and fit proof. Options are one line each and are only for
looking at in the 3D room. Say less. No HD stills.

## 1. The C-table joins the plan

**What:** the oak C-table at the sofa's open end, its top reaching over the seat for a drink, a pad or a laptop.

**Why we build it rather than buy it:** most C-tables, bought or home-made (e.g. a 48 × 61 × 30 one at about £26, or GVAwood's
50 × 30 × 65 in oak), steady themselves by sliding their foot under the sofa. Yours sits flat on the floor (your photo), so no foot can go
under it. Ours stands its upright out past the sofa's end and weighs its foot down instead.

**Size and fit:**
- Top 45 × 30 at 62, so it's 8 clear of the seat cushion (top 52).
- It reaches 12 over the seat. The upright stands 18 out from the sofa's end, on a foot 21 deep.
- A 400 × 200 × 6 mm steel plate (£3.57, PlazCutz) screwed under the foot, felt under that.
- It holds about 14 kg on its far edge before it would tip: drinks, a pad or a laptop, not leaning on.
- Its foot sits at x 40–85, 9 cm clear of the blanket basket (x 2–31).

**Materials:** 18 mm oak from the second board in the Snowdon pack (the record table uses one of the three): the top 45 × 30, the
upright 45 × 60.2, the foot 45 × 21. Glued and screwed, rounded corners, hardwax oil.

**Changes:**
- `geometry.FIRM["ideas"] = ["ctable"]`, so the 3D room opens with it.
- `ideas.CTABLE` gets the new numbers.
- The 3D model gets the longer foot and the plate.
- Two TRACK rows, one buy and one to do.
- Cut-list rows.
- A fit zone: the seat, the basket, the walkway, the tip load.
- A clash box.
- A short plan section beside the record table.
- The "Small ideas" line in section 12 drops it.
- Sources: `plazcutz` (the plate) and `ctablebuy` (the bought C-tables we compared).

## 2. The plants: the sill as you have it, the stand our pick

v40 gave every plant real leaves (the leaf library: pothos, snake plant, monstera, fern, spider plant, calathea, ficus). This round
sets which plant goes where; each pot already takes a kind (`potPlant(..., { kind })`).

- **Window sill, from the room:**
  - Smaller plants on the left: a calathea, a fern and a small pothos trailing over the nose.
  - Taller ones in the middle: a snake plant and a ficus, about 35–45 tall.
  - Spider plants on the right: three, their leaves arching over the sill's nose.
  - No pot behind the right rear speaker (x 250–275).
- **The plant stand (not built yet, so our pick for the best look):**
  - Trailing pothos and spider plants on the top tiers, spilling down the towers' fronts.
  - A monstera in the tall open middle, a snake plant on the shelf above it.
  - Calathea and fern on the lower tiers, one plant a tier so each reads clearly.

## 3. The room, reviewed

**Fixes:** the sill row had a pot behind the right rear speaker; the new row leaves the speaker spots clear.

**New options** (look only; one line each in section 12, a switch in the 3D room). Each one's size and price come from a source:
- Grow-light bars under the plant stand's tiers, as in the stand's listing photo.
- Motorised curtains, so Film night closes them.
- Two picture ledges for LPs face-out over the vinyl stand.
- A cordless table lamp on the C-table.

## 4. Order of work

1. This plan on GitHub (main).
2. Item 2, the plants.
3. Item 1, the C-table (its build in the guide's record-table style; when the guide moves to one chapter per thing (v42), the
   C-table gets its own chapter).
4. Item 3, the new options.
5. Rebuild the PDFs and the page (`make_images.py && export3d.py && build_doc.py && build_viewer.py`), then `qa.py`, `taptest.py`
   and `clash.py`; HANDOFF round 38 and README.
6. PR into main and merge; publish the shared plan page.
