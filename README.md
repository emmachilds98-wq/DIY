# DIY

Home projects for Emma and Dave's house (Portsmouth Close).

## Media wall and dining wall, v12

The artisan oak media wall in Farrow & Ball Card Room Green, drawn to the measured room (alcove 186 × 38 cm, ceiling 235),
with a fold-down oak dining table on the chimney breast. Everything below shows here on GitHub; nothing needs downloading.

![The media wall, main view](media-wall/out/Media%20wall%20v12%20-%20artisan%20oak%20-%20Card%20Room%20Green%20(HD).png)

**New in v12** (the layout is v11's, as agreed)
- The sub sits in a **slatted oak box** (52 × 30 × 42): about 40% open on three sides so the sound and the rear port's air get out, with a solid top. Hands and feet stay out. It lifts off when eight sit at the table.
- **Oak slats** on the PC screen (open top for the exhaust, as in v6.1), a slatted spine over the PC's cable drop, and a slatted panel behind the turntable zone.
- The folded table gets a **reeded oak underside**, so folded up it reads as a fluted oak panel. Brass inserts for the legs replace the black plates.
- The main view shows **both spot bars** and the **open stairwell** with its wooden banister.
- New views of the **table set for six** and the **PC side wall**, and a **storage sheet** drawn to scale.
- From the v6.1 plan: the **roll-out keyboard tray**, a **2700K lamp** by the sofa, a **finger pull** on the plinth drawer (no push-to-open at floor level) and an optional **conduit to TV height**.
- Fit proof: 57 checks, 42 fit, 10 tight, 5 to check on site, none fail.

| The table set for six, both spot bars | The PC side wall |
|---|---|
| ![Six at the table](media-wall/out/Media%20wall%20v12%20-%20table%20set%20for%20six,%20both%20spot%20bars%20(HD).png) | ![PC side wall](media-wall/out/Media%20wall%20v12%20-%20the%20PC%20side%20wall%20(HD).png) |

![Numbered key](media-wall/out/Media%20wall%20v12%20-%20artisan%20oak%20-%20numbered%20key%20(HD).png)

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

### What fits where
![Storage options](media-wall/out/Storage%20options%20-%20what%20fits%20each%20space.png)

### The room and the dining layouts
![Living room plan](media-wall/out/Living%20room%20plan%20-%20L-sofa%20and%20dining.png)
![Dining layouts](media-wall/out/Dining%20layouts%20-%20four,%20six%20and%20eight.png)

### Still to confirm (answer in the viewer's form, or in a message)
The sofa's size · the door's hinge and the west end's sizes · the stairs: up or down? · side wall and breast: solid or plasterboard? ·
how many LPs, singles and games · turntable, PC case and fan stand models · the 10-gang's length and surge protection · the second
ceiling point's exact spot · chairs, and where the leaf and legs live · the 23 × 22 cm box by the window · wired ports for the projector
and music room · console model numbers (optional).

### Documents
- **The full plan:** [`media-wall/out/Home_Network_Plan_v12.pdf`](media-wall/out/Home_Network_Plan_v12.pdf) (45 pages: room, media wall and fit proof, records, dining wall, side wall, joinery, paint and light, power and network, build guide, buy list, sources)
- **The build guide:** [`media-wall/out/Build_Guide_v12.pdf`](media-wall/out/Build_Guide_v12.pdf) (tools, techniques, order of work, step by step)
- **All renders and plans:** [`media-wall/out/`](media-wall/out/) (earlier versions in `v9/`, `v10/`, `v11/`)
- **Interactive viewer:** the Claude artifact (views × paints × key, answers and photos, a shared buy tracker, the fit proof). `index.html` at the root is the same page for GitHub Pages.
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
