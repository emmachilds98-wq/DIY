# DIY

Home projects for Emma and Dave's house (Portsmouth Close).

## media-wall/
The living room media wall and whole-house network plan: an artisan oak wall in Farrow & Ball Card Room Green,
face-out record trays, a Deco mesh wired by Cat6, AV and power plans, and a build guide.

- **Latest plan:** [`media-wall/out/Home_Network_Plan_v10.pdf`](media-wall/out/Home_Network_Plan_v10.pdf) (v9 and its renders are kept in `media-wall/out/v9/`)
- **Latest renders:** [`media-wall/out/`](media-wall/out/)
- **Where things stand and what's next:** [`media-wall/HANDOFF.md`](media-wall/HANDOFF.md) (read this first)
- **Client inputs** (accurate room sketch, floor plans, photos): [`media-wall/inputs/`](media-wall/inputs/)

> **Status:** v10 is drawn to the measured room (alcove **186 × 38 cm**, ceiling **235 cm**, chimney breast 117.5 cm).
> The vinyl corner moved to an oak cabinet against the chimney breast; every item is checked against its published
> size in the plan's fit proof. Open questions for the client are at the top of `HANDOFF.md`.

### Rebuilding the plan and renders
Requires Python 3.10+ and Chromium via Playwright.

```bash
cd media-wall
pip install -r requirements.txt && playwright install chromium
cd src
python3 geometry.py                     # prints the derived layout numbers (the one source of truth)
python3 fit.py                          # prints the fit proof, zone by zone
python3 make_images.py                  # every render, montage and viewer image (HD copies into ../out/)
python3 build_doc.py                    # builds plan.html and the PDF into ../out/
python3 build_viewer.py                 # the interactive viewer page (images in art/)
```

| File | What it does |
|---|---|
| `src/geometry.py` | Every room and wall dimension (cm), from the measured sketch; everything else reads from it |
| `src/fit.py` | The fit proof: item sizes with sources, spaces, spares and verdicts, plus the numbered source list |
| `src/render.py` | One-point perspective renderer drawn in real centimetres (`P(x, y, z)`, `place()` for offsets); the media wall, vinyl cabinet, room, lighting, keys |
| `src/diagrams.py` | Plan diagrams as SVG: elevation, sections, drawers, joints, power, network, house and room plans |
| `src/build_doc.py` | The plan text, tracker and tables; builds HTML then PDF |
| `src/parts/` | Section text spliced into `build_doc.py` in earlier rounds (reference) |
| `src/shot.py` | Rasterises SVG/HTML to PNG with headless Chromium (`shots()` batches many) |
| `src/make_images.py` | Builds all renders, the paint and skirting montages, HD outputs and viewer images |
| `src/media_wall_viewer.html` | The interactive viewer page (style × paint × key), built by `build_viewer.py`, images from `src/art/` |

## Working on it
- Branch from `main`, keep changes small, and open a pull request describing what changed in the plan.
- Keep every dimension consistent across renders, diagrams, tables and text; when a number moves, search for it everywhere.
- Add a line to the top of `media-wall/HANDOFF.md` saying what you changed and what's next.
