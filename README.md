# DIY

Home projects for Emma and Dave's house (Portsmouth Close).

## media-wall/
The living room media wall and whole-house network plan: an artisan oak wall in Farrow & Ball Card Room Green,
face-out record trays, a Deco mesh wired by Cat6, AV and power plans, and a build guide.

- **Latest plan:** [`media-wall/out/Home_Network_Plan_v9.pdf`](media-wall/out/Home_Network_Plan_v9.pdf)
- **Latest renders:** [`media-wall/out/`](media-wall/out/)
- **Where things stand and what's next:** [`media-wall/HANDOFF.md`](media-wall/HANDOFF.md) (read this first)
- **Client inputs** (accurate room sketch, floor plans, photos): [`media-wall/inputs/`](media-wall/inputs/)

> **Status:** v9 was drawn for an alcove of 225 × 50 cm and a 220 cm ceiling. The accurate measurements
> (`inputs/room_sketch_accurate_mm.png`) show **186 × 38 cm** and **235 cm**, so v10 re-fits the design. The plan
> for v10 is in `HANDOFF.md`, sections 3–8.

### Rebuilding the plan and renders
Requires Python 3.10+ and Chromium via Playwright.

```bash
cd media-wall
pip install -r requirements.txt && playwright install chromium
cd src
python3 render.py                       # writes the render SVGs (v8_*.svg)
python3 shot.py v8_join_key.svg render_v8_join_key.png 2540 1300 1.1   # SVG -> PNG
python3 build_doc.py                    # builds plan.html and the PDF into ../out/
```

| File | What it does |
|---|---|
| `src/render.py` | One-point perspective renderer drawn in real centimetres (`P(x, y, z)`); the media wall, room, lighting, keys |
| `src/diagrams.py` | Plan diagrams as SVG: elevation, sections, drawers, joints, power, network, house and room plans |
| `src/build_doc.py` | The plan text, tracker and tables; builds HTML then PDF |
| `src/parts/` | Section text spliced into `build_doc.py` in earlier rounds (reference) |
| `src/shot.py` | Rasterises an SVG to PNG with headless Chromium |
| `src/media_wall_viewer.html` | The interactive viewer page (style × paint), images from `src/art/` |

## Working on it
- Branch from `main`, keep changes small, and open a pull request describing what changed in the plan.
- Keep every dimension consistent across renders, diagrams, tables and text; when a number moves, search for it everywhere.
- Add a line to the top of `media-wall/HANDOFF.md` saying what you changed and what's next.
