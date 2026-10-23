# v41 upgrade plan: a better build, a calmer page

Client (23 Oct): "continue on from v40 now. Improve the build further and optimise the ui design. Review and write a plan for this
upgrade." Starts from `main` at v40. The standing rules hold: the core plan (`geometry.FIRM`) gets the full build; options stay
one line each; say less; no HD stills; no new shaders while the room is in use.

## What the review found

**The build**
1. **Your picks have no build steps.** The bar beside the cabinet, the record table, the wall cabinets, the alcove shelves, the shelf
   over the door, the shelf boxes and the step drawers are in the buy list (£4,374–8,245 includes them), but none of the guide's 13
   steps tells you how to make or fit them, and their ply isn't in the cutting list or the sheet layout.
2. **The fit proof has stale rows.** Two describe the sliding cabinet's doors (gone since v33), one says your trailing plant is 1.3 short
   of the pot (the strands have hung through the shelf's gap since v38; the clash check is clear), and one checks the glass case
   against layout B (an option). They read as open problems when they aren't.
3. **Thirteen checks are open.** Most need a tape measure or the real item: the side-wall socket, the ottoman's height, the shelf's
   stairs end, the architrave over the door, the RetroTINK. They're spread through 10 pages of the fit proof.
4. **The step drawers depend on the new stairs.** They need a joiner (a bearer under each tread), and you've said the stairs will
   change, so they're a cost in the plan with no date.
5. **"Finishing touches" is £854–1,508**, the third-biggest line, mostly picks bought last (the ottoman, rug, record table, step
   drawers), with no order or "nice to have later" split.

**The page** (phone 390 × 844 and desktop, screenshots in the PR)
6. **Three layers stacked at the bottom** on a phone: the plan pill, Try options and the dock. The room gets the middle third.
7. **Every drawer repeats a footer** (the scene's name, Reset view, Full screen): three copies of the same three controls.
8. **Look's wall picker takes seven chips** before you reach a paint; its label is 13 words.
9. **The Plan and Buy sheets repeat the same counts:** rings on Plan (steps, things bought, choices), four tiles on Buy (total,
   things bought, paid, jobs). The jobs tile says "2 of 31 done" on a fresh device: check that count.
10. **Build opens on instructions, not steps:** a progress line, two sentences, nine filter chips in three rows, a toggle and another
    sentence before step 1.
11. **19 texts over the word budget** (16 captions of 21–27 words), and the first-visit tip covers the room.

## 1. The build

- **A new step, "Your picks"**, after the dining cabinet. One part each, with sizes, fixings, tools and time: the bar (scribed
  between the cabinet and your shelf, the ENHET frame and mirror over it), the record table (KALLAX on its back, ply base, castors,
  the oak lid on its hinge), the two EKET cabinets (rail into the solid wall, heights), the alcove shelves (concealed brackets,
  load), the shelf over the door (brackets, the architrave check), the boxes. The step drawers get one line: "with the new
  stairs, by the joiner", plus what to ask for.
- **Their parts in the cutting list and the sheet layout** (`nest.py`): the bar's and the record table's ply go on the same boards
  as the base and the cabinet, so we see whether they need a sheet of their own or fit in the offcuts.
- **Buy and adapt first, again** for each pick: e.g., a ready-made unit that could replace the bar's carcass, with what to change.
- **The fit proof cleaned:** stale rows out, the plant row recomputed against the gap, the layout B row moved to the options.
- **One measuring sheet for everything open** (the 13 checks, each with where to measure and a box to write it in), first in the
  guide and in Decide, so one session with a tape closes most of them.
- **Finishing touches split** into "for move-in" and "can wait" (the ottoman, the rug, the step drawers), with the subtotal of each,
  so the total shows what's needed now.
- **Build days rechecked:** the times per step against the new step (the plan says 16–20 days; it will say what the picks add).

## 2. The page

- **One bottom bar on a phone:** the dock carries the plan total in a slim strip above its four buttons; Try options moves into
  Room (where the options are). The room gets back about 60 px.
- **No drawer footers:** the scene's name, Reset view and Full screen go to one small menu (⋯) on the room, top right.
- **Look starts on paint:** the swatches first; "All walls ▾" opens the wall picker only when you want one wall. Label: "Paint".
- **Plan home, one summary:** a single progress line (steps · bought · £ paid · choices) replaces the rings and the tiles; Buy
  starts on the list with the same line. The jobs count fixed or explained.
- **Build opens on the steps:** the filter chips in one scrolling row, the explanations gone (a "?" opens them), "all steps open"
  as a small switch beside the count.
- **Words:** the 19 long captions cut to 20 words or fewer; the first-visit tip shorter and placed clear of the room, shown once.
- **Desktop:** the same changes; the drawers stay as side panels.
- **Checks:** `qa.py` (no overflow, no errors, the text budget 0 over), `taptest.py`, before and after screenshots at 390 and 1280.

## 3. Order

1. The fit proof cleaned and the measuring sheet (quick, and it makes the rest easier to check).
2. The picks' step, its cutting list and buy-and-adapt lines; finishing touches split.
3. The page: the bottom bar, the footers, Look, Plan/Buy, Build, the words.
4. Rebuild (`make_images`, `export3d`, `build_doc`, `build_viewer`), QA, HANDOFF round 35, README, a PR into `main`, merged.

## Questions for you (none block the start)

- The side-wall socket: its distance from the alcove's back wall and its height (Decide has asked since v38).
- When the stairs change, do you want the step drawers built with them, or dropped from the plan's total until then?
- Is there anything on the page you use most that should stay exactly where it is?
