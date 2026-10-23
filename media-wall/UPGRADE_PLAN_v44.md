# v44 upgrade plan: clearer Plan, Build and Buy; a sharper 3D room

Starts from `main` at v43. Finishes v42's open items (the page's flow, the shorter plan PDF) and adds the client's ask.

The client (23 Oct): "continue on from the v42 build with plans we have and my instruction to review the full plans, build and buy
areas to read more clearly and be easier to follow while still having everything I need, use design functions where needed to
improve. Increase render quality of 3D room wherever you can".

Standing rules: the core plan (`geometry.FIRM`) gets the full build. Options are one line each. Say less. No HD stills. No mention of
Claude in the page, the README or the PDFs. Every size has a cited source.

## 1. What the review found (phone, 390 wide)

- **Plan** is about 9 screens.
  - "What's next" appears twice: the next three cards and an "Up next" card.
  - It still has the 90 vs 80 table comparison, which is an option.
  - The rings, the decisions and the money table all compete with the next three.
- **Build** is about 19 screens.
  - Fourteen step cards, each with three buttons (Done, Open, "Build day").
  - Then the merchant's whole cutting list.
  - It doesn't follow the guide's chapters, so making one thing means hopping between steps.
- **Buy** gives the costs twice: by piece (the cost overview), then again by phase. Neither links to how to make the piece.
- **The plan PDF** is 46 pages. The fit proof, the console sizes, the wiring plan and the lighting presets repeat what the guide or the
  page already has.
- **The guide** is in chapters (v42), but the C-table has no chapter of its own.

## 2. Build: one card per thing you make

- **Top:** one line for the order of work (Network → Cables → Paint → Mark the heights → 1 … 10) and "n of 15 done".
- **Things to make**, ten cards, one per guide chapter including **the C-table**. Each card shows:
  - the picture, the time and the cost;
  - a Done tick;
  - when opened, three tabs: **Buy · Cut · Build**, the same as the PDF's chapter.
- **Jobs**, five smaller cards (Network, Cables and the socket, Paint, Lighting, Connect), each with Buy · Do.
- **For the timber merchant:** the cutting list and the sheet layouts, closed by default, with Copy.
- **One "Download the build guide (PDF)" button** at the top.
- The old ticks carry over: a step's Done ticks its chapter.

## 3. Plan and Buy

- **Plan:**
  - The next three stay, with the rings as one line under them.
  - The "Up next" card goes.
  - The 90 vs 80 comparison goes; it's one line in the options.
  - One "Download the plan (PDF)" button at the top.
- **Buy:**
  - By piece first: each piece's cost, what to buy for it, and **How to make it** (its chapter in Build).
  - The shopping list in build order, with its ticks and amounts paid, under one fold below.
- **From the room:** tapping a piece you make offers **How to make it**, straight to its card in Build.

The design pass: a structured design critique of each sheet at 390 and 1280 before and after (hierarchy, scanning, repetition, touch
targets, contrast), with the findings and what changed recorded in HANDOFF.

## 4. The plan PDF: about 35 pages

- Keep: the plan on a page, the room, each piece (picture, size, cost, one paragraph), the costs, the options (one line each),
  Sources.
- The fit proof becomes one summary table (the full proof stays on the page). The console sizes table, the wiring plan (it's in the
  guide's Cables chapter), the long lighting presets text and the step-by-step build (the guide's) go.

## 5. The 3D room, sharper

- **Colour:** test AgX tone mapping against today's ACES on the plan's paint colours; keep whichever shows Card Room Green and the oak
  truer.
- **HD on a real graphics card:**
  - draw at up to 2× pixel density (1.5× today);
  - soft shadows live (2048 maps) instead of only in saved pictures;
  - multisampled anti-aliasing through the ambient-occlusion pass;
  - textures sharpened at a slant (anisotropy to the card's maximum).
- **Materials:** reflections from the room's environment tuned per surface (glass, the TV, gloss pots, the oak's sheen).
- **Phones and Fast** stay as they are (v39's speed work). Every change is checked for frame time and errors in `qa.py`.

## 6. Order

1. This plan, merged to `main`.
2. The C-table's chapter in the guide.
3. The page:
   - Build in cards;
   - Plan and Buy;
   - How to make it from the room;
   - the design critique before and after.

   Merged.
4. The shorter plan PDF. Merged.
5. The 3D room's quality. Merged.
6. Rebuild, `qa.py`, `taptest.py`, `clash.py`, HANDOFF round 39, README. Merged.
