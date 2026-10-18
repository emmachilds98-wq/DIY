# DIY

Home projects for Emma and Dave's house (Portsmouth Close).

## Media wall and dining wall, v13

The artisan oak media wall in Farrow & Ball Card Room Green, drawn to the measured room (alcove 186 × 38 cm, ceiling 235),
with a fold-down oak dining table on the chimney breast. Everything below shows here on GitHub; nothing needs downloading.

![The media wall, main view](media-wall/out/Media%20wall%20v13%20-%20artisan%20oak%20-%20Card%20Room%20Green%20(HD).png)

**New in v13** (you asked for less cladding, the stairs going up, and the drawer layouts)
- **Less cladding.** Gone: the slatted cable spine, the slatted PC screen, the slat panel behind the turntable, the slatted sub box and the reeded table. The slat-wall alternative is retired too.
- **Cables you can't see.** The side wall is solid, so the PC's leads drop through a brush grommet in its shelf into a conduit chased into the wall (electrician, same visit): no spine, no trunking.
- **Plain oak where it was slatted.** The sub stands on a low oak riser; the folded table is plain oiled oak between its pegged breadboard ends.
- **The stairs go up** to the first floor beside the door, behind the wooden banister. Drawn rising away from the room: tell us if they run the other way.
- **The drawer layouts:** every drawer in the base, to scale, with what goes in it (below).
- Fit proof: 56 checks, 45 fit, 8 tight, 3 to check on site, none fail.
- **Your answers (v12.1):** the sofa's long side ends in line with the breast's reveal (about 188 cm, from your photo); the door hinges on the breast side and opens in; the side wall and breast are solid; the PC is an average gaming case.

| The table set for six, both spot bars | The PC side wall |
|---|---|
| ![Six at the table](media-wall/out/Media%20wall%20v13%20-%20table%20set%20for%20six,%20both%20spot%20bars%20(HD).png) | ![PC side wall](media-wall/out/Media%20wall%20v13%20-%20the%20PC%20side%20wall%20(HD).png) |

![Numbered key](media-wall/out/Media%20wall%20v13%20-%20artisan%20oak%20-%20numbered%20key%20(HD).png)

### Key heights (cm from the floor)
| Height | What |
|---|---|
| 235 | Ceiling |
| 196 | High shelf (books, box, print, the "now playing" 7-inch, Deco B) |
| 155.4 | Record ledges over the TV and round the corner; the PC shelf |
| 153.3 | Dining table, folded up |
| 134 | Series X shelf over the turntable (lid opens to 121) |
| 116.5 | TV centre (LG C6 55" on its stand) |
| 76 | Oak worktop, and the dining table when it's down |
| 9 | Plinth under bays 1–2, with a hidden drawer |

### The drawer layouts
![Drawer layouts](media-wall/out/Drawer%20layouts%20-%20where%20each%20drawer%20is%20and%20what%20goes%20in%20it.png)

### What fits where
![Storage options](media-wall/out/Storage%20options%20-%20what%20fits%20each%20space.png)

### The room and the dining layouts
![Living room plan](media-wall/out/Living%20room%20plan%20-%20L-sofa%20and%20dining.png)
![Dining layouts](media-wall/out/Dining%20layouts%20-%20four,%20six%20and%20eight.png)

### Still to confirm (answer in the viewer's form, or in a message)
The sofa's return length · the west end's sizes · which way the stairs run ·
how many LPs, singles and games · turntable and fan stand models · the 10-gang's length and surge protection · the second
ceiling point's exact spot · chairs, and where the leaf and legs live · the 23 × 22 cm box by the window · wired ports for the projector
and music room · console model numbers (optional).

### Documents
- **The full plan:** [`media-wall/out/Home_Network_Plan_v13.pdf`](media-wall/out/Home_Network_Plan_v13.pdf) (48 pages: room, media wall and fit proof, records, dining wall, side wall, joinery, paint and light, power and network, build guide, buy list, sources)
- **The build guide:** [`media-wall/out/Build_Guide_v13.pdf`](media-wall/out/Build_Guide_v13.pdf) (tools, techniques, order of work, step by step)
- **All renders and plans:** [`media-wall/out/`](media-wall/out/) (earlier versions in `v9/` to `v12/`)
- **Interactive viewer:** the Claude artifact, https://claude.ai/artifact/71ffwf5PRLhoLj6G5KTvm2 (views × paints × key, drawer layouts, answers and photos, a shared buy tracker, the fit proof). `index.html` at the root is the same page for GitHub Pages.
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
python3 build_doc.py     # the plan and the build guide PDFs into ../out/
python3 build_viewer.py  # the viewer page (images in art/) and ../../index.html
```

| File | What it does |
|---|---|
| `src/geometry.py` | Every room and wall dimension (cm), from the measured sketch; everything else reads from it |
| `src/fit.py` | The fit proof: item sizes with sources, spaces, spares and verdicts, plus the numbered source list |
| `src/render.py` | Perspective renderer in real centimetres: front view (`build`), dining for six, and the side-wall view (`build_side`) |
| `src/diagrams.py` | Plan diagrams as SVG: elevation, sections, drawers, joints, power, network, house and room plans, storage sheet |
| `src/build_doc.py` | The plan text, tracker and tables; builds HTML then PDF |
| `src/build_viewer.py` | The interactive viewer page and `index.html` |
| `src/make_images.py` | Builds all renders, montages, HD outputs and viewer images |
