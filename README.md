# DIY

Home projects for Emma and Dave's house (Portsmouth Close).

## Media wall and dining wall, v49: the real sun (the window faces north-north-east), the 25 m garden

The artisan oak media wall in Farrow & Ball Card Room Green, drawn to the measured room (alcove 186 × 38 cm, ceiling 235),
with the compact dining cabinet under your shelf by the stairs: the table and the six chairs in two oak boxes, 147 cm long and 23 deep. It's the only table now. Everything below shows here on GitHub; nothing needs downloading. **Open the plan:** https://emmachilds98-wq.github.io/DIY/ (GitHub Pages: everything, including the room in 3D; ticks stay on that device)

![The media wall, main view](media-wall/out/Media%20wall%20v49%20-%20artisan%20oak%20-%20Card%20Room%20Green,%20table%20by%20the%20stairs%20(HD).png)

**The garden through the window, from one floor up** (from your photos of the view): from across the room you see the trees at the end of the garden, the roofs and the hill opposite; walk up to the glass and the lawn is below you. Day, and dusk in the evening.

**New in v49** ("This is the rear side of 13 Portsmouth close facing Darnley road ... Roughly 25m long")
- **The back of the house faces 14° east of north.** The sun only comes in on spring and summer mornings, low from the right, and never reaches the TV. The 3D room's daytime sun is now 7 am in June: it lays the window's bars across the dining cabinet.
- **The garden runs 25 m** to the far fence; the view through the window ends there.
- **The shared page loads quicker:** its pictures are stored with it, not packed into the page (about 4 MB down to 1.8 MB).

**New in v48** ("improving the renders graphics and quality of the render even further", "It's a floor up so take perspective into account")
- **The garden as you see it**, from one floor up: built from your photos of the view, with the lawn below the sill and the trees and roofs beyond; the real window (three sections, top lights, Georgian bars).
- **The sun by day** comes through the window and lays the bars' shadows across the room.
- **By evening** the room reflects itself (the TV, the glass case, the window at night), and the lights have a soft glow, on a PC with a graphics card.
- **Save as HD picture** is sharper: drawn at twice the size, with finer shadows.

**New in v46** ("drill down into tasks for each piece of the room when I click on them or look in the plans", "default view could balance lighting throughout the room using all fixtures")
- **The room, piece by piece, any order:** six places (the media wall, the side wall and PC, the chimney breast and door, the dining wall, the sofa, the window corner). Tap a place's label in the 3D room to see its pieces; tap a piece (or find it in Build) for its card: **Check · Buy · Cut · Build**, a tick for each task and each thing to buy, and a ring showing how much is done. No more "step 1 of 14".
- **Easy to read on a phone or a PC:** on a PC the pieces sit two across and the open one takes the row; both PDFs have clickable contents and bookmarks, the build guide is grouped by place and piece, and each PDF has a **phone edition** (a narrow page, bigger type).
- **Fits a phone:** nothing scrolls sideways. Drawings and cutting layouts fit the screen (tap one for full screen, pinch to zoom); wide tables turn into one card per row on a phone, in the page and in the phone PDFs.
- **Evening light by default:** every fixture on and balanced (the ceiling strip, the uprights, all eight spot heads, the lamp and a new **Accents** layer: the glass case, the bar's strip, the PC). Measured in pictures of the room: the brightest part is under three times the darkest, on a PC and on a phone (phones were six times before). **Brightness** and **Warmth** set the whole room in two moves.


Earlier versions (v9 to v44) and what each changed are in [`media-wall/HANDOFF.md`](media-wall/HANDOFF.md) and the git history.

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
![Every drawer out](media-wall/out/Media%20wall%20v49%20-%20every%20drawer%20out%20(HD).png)

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
- **The full plan:** [`media-wall/out/Home_Network_Plan_v49.pdf`](media-wall/out/Home_Network_Plan_v49.pdf) (35 pages, your plan only, with clickable contents and bookmarks); for a phone, [`Home_Network_Plan_v49_phone.pdf`](media-wall/out/Home_Network_Plan_v49_phone.pdf)
- **The build guide:** [`media-wall/out/Build_Guide_v49.pdf`](media-wall/out/Build_Guide_v49.pdf) (66 pages, by place and piece: each with Check, Buy, Cut and Build; the jobs; the merchant's cutting list); for a phone, [`Build_Guide_v49_phone.pdf`](media-wall/out/Build_Guide_v49_phone.pdf)
- **All renders and plans:** [`media-wall/out/`](media-wall/out/) (the previous version in `v48/`; older ones are in the git history)
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
