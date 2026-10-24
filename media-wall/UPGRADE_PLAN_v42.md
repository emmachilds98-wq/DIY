# v42 upgrade plan: one chapter per thing you make, shorter PDFs, an easier page

Client (23 Oct): "Make no reference to Claude as being the editor or viewing there and then optimise PDFs in there to be more
concise for what I need. Each thing I'm making will need a buy list, clear image diagram with cuttings and clear build instructions.
Then review the areas in the site to make it better for user flow. Add to plan and continue. Ensure plan is available in GitHub at
all times."

Starts from `main` at v41. The standing rules hold: the core plan (`geometry.FIRM`) gets the full build; options stay one line each;
say less; every size from a cited source.

## 0. The plan on GitHub, always

- This file and every round's PDFs go to `main` as soon as they're written, so the plan, the build guide and the page on
  GitHub Pages are always the latest. Work in progress is merged in small steps, never left on a branch.

## 1. No mention of Claude

- **The page:** the line "To share them, use the plan page on Claude" goes (ticks stay on your device); "The page's storage is
  full; tell Claude" becomes "tell us"; comments in the page's code that name Claude are reworded.
- **The README:** the links to the Claude plan page go; GitHub Pages is the one place to open the plan.
- **The PDFs:** checked page by page; none mention Claude today, and a check in `qa.py` keeps it that way (the page and both
  PDFs).

## 2. The build guide: one chapter per thing you make

Today the guide is 65 pages in order of work: the steps, then one cutting list for everything, then a sheet layout per page. You
have to hop between three places to make one thing. **New layout, each chapter on its own pages:**

| Chapter | What it covers |
|---|---|
| **Start here** (2 pages) | What you're making, with page, time and cost for each; the order; tools; the measuring sheet; safety in five lines |
| **1. The media wall base** | the plinth, the BESTÅ frames, bay 3's carcass, the drawers and crates, the face frame |
| **2. The worktop** | the template, the cut-outs, fixing |
| **3. The oak uprights and shelves** | the uprights, the shelves, the record ledge, the "now playing" ledge |
| **4. The side-wall run and the PC shelf** | the cleats, the run, the PC shelf and its keyboard tray |
| **5. The dining cabinet and table** | the two boxes, the doors, the table halves, the legs, the hinges |
| **6. The bar** | the cupboard beside the cabinet, the ENHET frame and mirror over it |
| **7. The glass case** | the oak frame, the back, the glass |
| **8. The record table** | two KALLAX on their backs, the ply base, castors, the oak lid |
| **9. Bought and fitted** | the alcove shelves, the wall cabinets, the shelf over the door and its boxes (fixing heights, no cutting) |
| **Jobs** | the network, the cables and the socket, paint, lighting, connecting up: what to buy and the steps, one page each |
| **For the merchant** | the whole cutting list and the sheet layouts, two sheets to a page, at the back |

**Every chapter has the same four parts:**
1. **The picture:** the finished thing, with its overall size.
2. **Buy:** only what that thing needs, with quantity, rough price and where from (the same rows as the buy list, so the totals still
   match).
3. **Cut:** a clear diagram of every part drawn to scale with its size and name, the part count, and which board it comes from
   (that chapter's sheet layout).
4. **Build:** numbered steps, short, grouped by sub-assembly, then **Check before moving on**.

Target: about 40 pages, every page with a picture or a diagram; no history ("v16", "changed:") in the text.

## 3. The plan PDF: shorter

Today it's 76 pages. Cut to what you need to decide and buy:
- **Keep:** the plan on a page, the room, each piece (one picture, its size, its cost, one paragraph), the costs, the options (one line
  each), Sources.
- **Move or cut:** the detailed fit proof becomes one table (piece, result, what to check); the console sizes table, the step-by-step
  build (now only in the guide), the repeated wiring plan and the lighting presets' long text go.
- Target: about 35 pages.

## 4. The page: an easier flow

From a review of the page at phone and desktop size:
- **Build follows the guide's chapters:** "Things to make" (one card each: Buy · Cut · Build, and its cost and time) and "Jobs".
  A card opens on its buy list, its cutting diagram and its steps; Done ticks it off.
- **From the room to the build:** tapping a piece you make offers **How to make it**, straight to its chapter.
- **Buy links back:** each piece in the cost overview opens its chapter.
- **The PDFs in one place:** Plan and Build each get one "Download the PDF" button at the top.
- **Plan home:** the next three cards stay; the rings become one line under them.
- **Words:** the text budget stays at 0 over; `qa.py` adds the Claude check.

## 5. Order

1. This plan, merged to `main`.
2. Claude references out (page, README, comments), merged.
3. The guide in chapters (`build_doc.py`, `instructions.py`, a new parts diagram), then the shorter plan PDF.
4. The page's flow (Build in chapters, How to make it, Buy links, the PDF buttons).
5. Rebuild, `qa.py`, `taptest.py`, HANDOFF round 38, README, merged to `main`.

**Done 24 Oct (v42, round 38):** all of the above, merged to `main` stage by stage. The guide came to 60 pages, not 40: every chapter
keeps its full steps and its drawings to scale. The plan PDF is 46 pages.
