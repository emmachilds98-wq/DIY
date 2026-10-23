# DIY

Home projects for Emma and Dave's house (Portsmouth Close).

## Media wall and dining wall, v45: the stipple ceiling, Cosy lighting, a softer light over the table

The artisan oak media wall in Farrow & Ball Card Room Green, drawn to the measured room (alcove 186 × 38 cm, ceiling 235),
with the compact dining cabinet under your shelf by the stairs: the table and the six chairs in two oak boxes, 147 cm long and 23 deep. It's the only table now. Everything below shows here on GitHub; nothing needs downloading. **Open the plan:** https://emmachilds98-wq.github.io/DIY/ (GitHub Pages: everything, including the room in 3D; ticks stay on that device)

![The media wall, main view](media-wall/out/Media%20wall%20v45%20-%20artisan%20oak%20-%20Card%20Room%20Green,%20table%20by%20the%20stairs%20(HD).png)

**New in v45** ("stipple ceiling as default and cosy lighting that still allows nice view of the room", "stop over lighting the dining table")
- **The room opens as you'd live in it:** Cosy lighting in the evening, with an Artex stipple ceiling. Cosy has a little more light (the ceiling strip and bar 2 up a touch), so you can still see the whole room. The other ceilings are still in Look.
- **The dining table isn't washed out:** with the table open, bar 2 sits at 45–55 (it used to jump to 80) and the ceiling strip stays at 40 or less, so the oak top reads as oak.
- **Whole room** and **Hide labels** are small buttons on the room, under Plan, Build and Buy; the bottom bar is View, Room, Look and Edit.
- **A tidier repo:** old files are gone (the outputs of v9 to v43, about 920 replaced 3D pictures, old backups): about 5.4 GB less, and still in the git history if ever needed. Backups go in `media-wall/src/backups/`, old upgrade plans in `media-wall/plans/`.

**New in v44** ("read more clearly and be easier to follow while still having everything I need", "increase render quality")
- **Build, one card per thing you make:** the media wall base, the worktop, the uprights, the side wall, the dining cabinet, the bar, the glass case, the record table, the C-table and the fitted pieces, each with **Buy · Cut · Build** tabs, plus five Jobs (network, cables, paint, lighting, connect). The 14 step ticks sit in one fold with a Next line; the merchant's cutting list is folded. About 3 phone screens closed (was 19).
- **How to make it** from a piece's cost in Buy, or from the piece itself in the 3D room, opens its card.
- **Plan and Buy say each thing once:** Up next and the 90/80 comparison are gone; the build-order shopping list is in one fold under the costs by piece.
- **The plan PDF is 34 pages** (was 46): what the guide already has comes out, the pictures are smaller, the costs and sources run in two columns. **The C-table has its own chapter** in the build guide.
- **A sharper 3D room:** truer colour (the wall nearer Card Room Green, the glass case and window no longer blown out); on a PC graphics card, HD at up to 2× sharpness, soft shadows as you look round and crisper textures; reflections by surface.

Earlier versions (v9 to v43) and what each changed are in [`media-wall/HANDOFF.md`](media-wall/HANDOFF.md) and the git history.

### Key heights (cm from the floor)
| Height | What |
|---|---|
| 235 | Ceiling |
| 196 | High shelf (books, box, print, a small framed sleeve, Deco B); your shelf by the stairs (drawn at 196) |
| 155.4 | Record ledges over the TV and round the corner; the PC shelf |
| 189 | The dining cabinet's top (the table and six chairs inside) |
| 104 | The "now playing" ledge on the breast (v16) |
| 134 | Series X shelf over the turntable (lid opens to 121) |
| 116.5 | TV centre (LG C6 55" on its stand) |
| 76 | Oak worktop |
| 9 | Plinth under bays 1–2, with a hidden drawer |

### The drawer layouts
![Drawer layouts](media-wall/out/Drawer%20layouts%20-%20where%20each%20drawer%20is%20and%20what%20goes%20in%20it.png)

### Every drawer out
![Every drawer out](media-wall/out/Media%20wall%20v45%20-%20every%20drawer%20out%20(HD).png)

### What fits where
![Storage options](media-wall/out/Storage%20options%20-%20what%20fits%20each%20space.png)

### The room and the dining layouts
![Living room plan](media-wall/out/Living%20room%20plan%20-%20L-sofa%20and%20dining.png)
![Dining layouts](media-wall/out/Dining%20layouts%20-%20four,%20six%20and%20eight.png)

### Still to confirm (answer in the viewer's form, or in a message)
That you're doing the light fittings, dimmers and socket yourselves · the sofa's return length · the west end's sizes ·
which way the stairs run · turntable model and PHONO/LINE switch · the fan stand model · chairs, and where they'll be kept ·
the 23 × 22 cm box by the window · how many LPs, singles and games · wired ports for the projector and music room · the 10-gang's
surge protection, switches and length · console model numbers · the second ceiling point's exact spot · the RetroTINK's size on arrival.

### Documents
- **The full plan:** [`media-wall/out/Home_Network_Plan_v45.pdf`](media-wall/out/Home_Network_Plan_v45.pdf) (34 pages, your plan only: room, media wall and fit proof, records, dining wall, side wall, joinery, paint and light, power and network, the costs by piece, other options and sources)
- **The build guide:** [`media-wall/out/Build_Guide_v45.pdf`](media-wall/out/Build_Guide_v45.pdf) (61 pages: one chapter per thing you make, each with Buy, Cut and Build; the jobs; the merchant's cutting list and the sheets at the back)
- **All renders and plans:** [`media-wall/out/`](media-wall/out/) (the previous version in `v44/`; older ones are in the git history)
- **Interactive viewer:** https://emmachilds98-wq.github.io/DIY/ (`index.html` at the root): the room in 3D, the plan's chapters, build steps, buy tracker.
- **Where things stand:** [`media-wall/HANDOFF.md`](media-wall/HANDOFF.md)

### Rebuilding the plan and renders
Requires Python 3.10+ and Chromium via Playwright.

```bash
cd media-wall
pip install -r requirements.txt && playwright install chromium
cd src
python3 geometry.py      # the derived layout numbers (the one source of truth)
python3 fit.py           # the fit proof, zone by zone
python3 make_images.py   # every render, montage, diagram image and viewer image (HD copies into ../out/)
python3 export3d.py      # the 3D room's data (scene3d.json)
python3 build_doc.py     # the plan and the build guide PDFs into ../out/
python3 build_viewer.py  # the page (images in art/) and ../../index.html
python3 clash.py         # nothing in the room overlaps
python3 qa.py OUT        # the page at phone and laptop width: errors, overflow, sheets, chapters, step 11's card
python3 taptest.py OUT   # taps on the 3D room's pieces, each card and its buttons
```

| File | What it does |
|---|---|
| `src/geometry.py` | Every room and wall dimension (cm), from the measured sketch; everything else reads from it |
| `src/fit.py` | The fit proof: item sizes with sources, spaces, spares and verdicts, plus the numbered source list |
| `src/render.py` | Perspective renderer in real centimetres: front view (`build`), dining for six, and the side-wall view (`build_side`) |
| `src/diagrams.py` | Plan diagrams as SVG: elevation, sections, drawers, joints, power, network, house and room plans, storage sheet |
| `src/build_doc.py` | The plan text, tracker and tables; builds HTML then PDF |
| `src/chapters.py` | The build guide's chapters (one per thing you make: Buy, Cut, Build) and the page's Build cards |
| `src/costs.py` | The cost overview, piece by piece |
| `src/scenes.py` | The three lighting presets (Cosy the default) and the table rule |
| `src/ideas.py` | The options to look at in the 3D room (one line each in the plan) and the C-table |
| `src/room3d.js`, `src/room3d_page.py` | The 3D room (three.js) and its controls |
| `src/export3d.py` | The 3D room's data from geometry |
| `src/clash.py`, `src/taptest.py` | Overlap check for the room; tap test for the 3D room's cards |
| `src/build_viewer.py` | The interactive viewer page and `index.html` |
| `src/make_images.py` | Builds all renders, montages, HD outputs and viewer images |
| `src/qa.py` | Checks the page at 390 and 1280 px (serves the repo itself): console errors, anything off the right edge, every sheet and chapter |
