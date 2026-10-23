"""Builds the interactive viewer page (v11): view × paint × key, with the images in art/.
python3 build_viewer.py  -> media_wall_viewer.html (images referenced as art/*.jpg, published alongside it)
                            and ../../index.html, the same page for GitHub Pages"""
import json, pathlib
import geometry as G

HERE = pathlib.Path(__file__).parent
LPS = 2 * G.TRAY_LPS + G.LEDGE_LPS + G.WRAP_LPS
SINGLES = 2 * G.TRAY_SINGLES

STYLE = """<style>
/* Layout: one column, the render as the hero with its controls directly under it; facts in a two-column band below */
:root {
  --bg: #eef0ea; --surface: #ffffff; --ink: #1d241e; --muted: #5b6457; --line: #d4d9cd; --oak: #9a6634; --chip: #e3e7dd; --note: #f5efe3;
  --display: "Bricolage Grotesque", "Segoe UI", system-ui, sans-serif;
  --body: "Atkinson Hyperlegible", "Segoe UI", system-ui, sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #151a16; --surface: #1d231e; --ink: #e7ebe3; --muted: #9ba596; --line: #2f3830; --oak: #d9a46c; --chip: #262d27; --note: #262219; color-scheme: dark } }
:root[data-theme="dark"] { --bg: #151a16; --surface: #1d231e; --ink: #e7ebe3; --muted: #9ba596; --line: #2f3830; --oak: #d9a46c; --chip: #262d27; --note: #262219; color-scheme: dark }
body { background: var(--bg); color: var(--ink); font-family: var(--body); font-size: 16px; line-height: 1.55; }
.wrap { max-width: 1120px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 28px 56px; display: grid; gap: 28px; }
header { display: grid; gap: 10px; }
h1 { font-family: var(--display); font-weight: 700; font-size: clamp(2rem, 5vw, 3.1rem); line-height: 1.05; margin: 0; letter-spacing: -0.01em; text-wrap: balance; }
.lede { color: var(--muted); margin: 0; max-width: 64ch; }
.change { margin: 0; max-width: 72ch; background: var(--note); border-left: 3px solid var(--oak); border-radius: 6px; padding: 10px 14px; }
.viewer { display: grid; gap: 14px; }
.frame { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; overflow: hidden; }
.frame img { display: block; width: 100%; height: auto; }
.controls { display: flex; flex-wrap: wrap; gap: 14px 28px; align-items: flex-start; }
.group { display: grid; gap: 6px; min-width: 0; }
.label { font-family: var(--mono); font-size: 11.5px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); }
.seg { display: flex; flex-wrap: wrap; gap: 6px; }
.seg button { font: inherit; font-size: 14.5px; color: var(--ink); background: var(--chip); border: 1px solid transparent; border-radius: 999px; padding: 6px 14px; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; }
.seg button[aria-pressed="true"] { background: var(--surface); border-color: var(--oak); box-shadow: inset 0 0 0 1px var(--oak); }
.seg button:disabled { opacity: 0.45; cursor: not-allowed; }
.seg button:focus-visible { outline: 2px solid var(--oak); outline-offset: 2px; }
.dot { width: 14px; height: 14px; border-radius: 50%; border: 1px solid rgba(0,0,0,0.2); flex: none; }
.caption { color: var(--muted); font-size: 14px; margin: 0; }
.band { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 28px; }
.band > section { min-width: 0; display: grid; gap: 10px; align-content: start; }
h2 { font-family: var(--display); font-weight: 500; font-size: 1.35rem; margin: 0; }
.heights { list-style: none; margin: 0; padding: 0; border-left: 2px solid var(--line); }
.heights li { display: grid; grid-template-columns: 4.2rem 1fr; gap: 12px; padding: 5px 0 5px 12px; position: relative; }
.heights li::before { content: ""; position: absolute; left: -2px; top: 50%; width: 8px; height: 2px; background: var(--muted); }
.heights b { font-family: var(--mono); font-weight: 500; font-variant-numeric: tabular-nums; text-align: right; }
.counts { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.counts div { background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; min-width: 0; }
.counts strong { display: block; font-family: var(--display); font-size: 1.7rem; font-weight: 700; line-height: 1.1; font-variant-numeric: tabular-nums; }
.counts span { font-size: 13.5px; color: var(--muted); }
ul.plain { margin: 0; padding-left: 1.1rem; display: grid; gap: 6px; }
.plans { display: grid; gap: 14px; }
@media (prefers-reduced-motion: no-preference) { .frame img { transition: opacity .18s ease; } }
</style>"""


def fit_line():
    try:
        import fit
        c = fit.counts()
        total = sum(c.values())
        return (f"<li>Fit proof: {c[fit.PASS]} of {total} checks fit outright against published sizes; "
                f"{c[fit.TIGHT]} are tight and {c[fit.CHECK]} get a check on site (the full table is in the plan).</li>")
    except Exception:
        return ""


def page(prefix="", downloads=""):
    plans = (HERE / "art" / "zz_seating.jpg").exists()
    imgs = {k: f"{prefix}art/{k}.jpg" for k in [f"art_{s}_{p}" for s in ("join", "slats", "four") for p in ("card_room", "deep", "sage", "treron")] + ["key_join", "key_slats"]}
    plan_html = ""
    if plans:
        plan_html = f"""
  <section class="plans">
    <h2>The living room, the dining layouts and the house</h2>
    <div class="frame"><img src="{prefix}art/zz_living.jpg" alt="Living room plan drawn from the measured sketch: media wall, side-wall shelf and PC over the L-sofa, the dining wall, both spotlight bars, socket and viewing distance" width="2064" height="1464"></div>
    <div class="frame"><img src="{prefix}art/zz_seating.jpg" alt="Three small plans of the dining table: four at the wall, six and eight with the table lifted off and pulled into the room" width="2064" height="1200"></div>
    <div class="frame"><img src="{prefix}art/zz_house.jpg" alt="Three floor plans with the Decos, Cat6 runs, chimney breast, brick cupboard and sloped ceilings" width="2064" height="1488"></div>
    <p class="caption">The living room is drawn from your measurements; the L-sofa is drawn at a typical 247 × 168 cm until you measure yours. The house outline is traced from the agent's plans.</p>
  </section>"""
    return f"""<title>Portsmouth Close Media Wall</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Atkinson+Hyperlegible:wght@400;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
{STYLE}
<div class="wrap">
  <header>
    <h1>Media Wall v11</h1>
    <p class="lede">The artisan oak build in Farrow &amp; Ball Card Room Green, drawn to the room as you measured it. Switch between the media wall, the slat wall and the dining wall set for four, try the other greens, or turn on the numbered key.</p>
    <p class="change"><b>What changed in v11:</b> the TV moves {G.TV_SHIFT:.0f} cm nearer the side wall, so the turntable fits in the alcove with the Series X on a shelf above it and the record trays in the bay below. The record ledge wraps round onto the side wall, with the PC on a shelf above the end of the L-sofa. The chimney breast gets a fold-down oak dining table for four (six or eight with it lifted off), a second spotlight bar goes on your existing point by the door, and the sub moves under the dining wall, on the front wall beside the TV.</p>
  </header>

  <div class="viewer">
    <div class="frame"><img id="shot" alt="Render of the media wall" width="1804" height="1148"></div>
    <div class="controls">
      <div class="group"><span class="label" id="l-style">View</span>
        <div class="seg" role="group" aria-labelledby="l-style">
          <button id="s-join" data-style="join" aria-pressed="true">Artisan oak (main)</button>
          <button id="s-four" data-style="four" aria-pressed="false">Dining wall, set for four</button>
          <button id="s-slats" data-style="slats" aria-pressed="false">Slat wall</button>
        </div></div>
      <div class="group"><span class="label" id="l-paint">Paint</span>
        <div class="seg" role="group" aria-labelledby="l-paint">
          <button id="p-card" data-paint="card_room" aria-pressed="true"><span class="dot" style="background:#899081"></span>Card Room Green (chosen)</button>
          <button id="p-sage" data-paint="sage" aria-pressed="false"><span class="dot" style="background:#77815c"></span>Sage Green</button>
          <button id="p-treron" data-paint="treron" aria-pressed="false"><span class="dot" style="background:#8b8a77"></span>Treron</button>
          <button id="p-deep" data-paint="deep" aria-pressed="false"><span class="dot" style="background:#2c5643"></span>Deep green</button>
        </div></div>
      <div class="group"><span class="label" id="l-key">Labels</span>
        <div class="seg" role="group" aria-labelledby="l-key">
          <button id="k-key" aria-pressed="false">Show numbered key</button>
        </div></div>
    </div>
    <p class="caption" id="cap"></p>
  </div>

  <div class="band">
    <section>
      <h2>Heights, from the floor</h2>
      <ul class="heights">
        <li><b>{G.CEIL:g}</b><span>Ceiling, as measured</span></li>
        <li><b>{G.HIGH_TOP:g}</b><span>High shelf: books, a box, a print, the “now playing” single, Deco B</span></li>
        <li><b>{G.LEDGE_TOP:g}</b><span>Record ledges over the TV and round the corner; the PC shelf on the side wall</span></li>
        <li><b>{G.FOLDED_TOP:g}</b><span>Top of the dining table, folded up</span></li>
        <li><b>{G.RZ_SHELF_TOP:g}</b><span>Series X shelf, over the turntable (its lid has to {G.LID_CLEAR_TO:g})</span></li>
        <li><b>116.5</b><span>TV centre, LG C6 55in on its stand</span></li>
        <li><b>{G.WORKTOP:g}</b><span>Oak worktop, and the dining table when it's down</span></li>
        <li><b>{G.PLINTH:g}</b><span>Plinth under the two BESTÅ bays, with a hidden drawer</span></li>
      </ul>
    </section>
    <section>
      <h2>In the wall</h2>
      <div class="counts">
        <div><strong>~{LPS}</strong><span>LPs, all face-out</span></div>
        <div><strong>~{SINGLES}</strong><span>singles, all face-out</span></div>
        <div><strong>4–8</strong><span>at the dining table</span></div>
      </div>
      <ul class="plain">
        <li>Alcove: the TV between two oak uprights, now {G.TV_SHIFT:.0f} cm nearer the side wall; the turntable on the worktop to its right with the Series X on a shelf above; three 60 cm bays below for the Xbox consoles, the PlayStations and the two face-out record trays.</li>
        <li>Side wall: the record ledge wraps the corner with four more LPs, then an oak shelf for the PC above the end of the sofa, with the pad dock beside it.</li>
        <li>Chimney breast: a 110 × 80 cm solid oak table with pegged breadboard ends, folded flat every day, down on two steel brackets for four, lifted off onto legs for six or eight.</li>
        {fit_line()}
      </ul>
    </section>
    <section>
      <h2>Lighting</h2>
      <ul class="plain">
        <li>The LED strip you have now, on the ceiling round the whole room, facing down.</li>
        <li>Two four-head cone spotlight bars, Wolston style. The first, on the existing rose between the TV and the sofa, lights the shelves, the ledge, the coffee table and the turntable. The second, on the existing point between the door and the wall, lights the table and the framed LPs above it.</li>
        <li>LED grooves in the oak uprights and a bias light behind the TV. No spot ever points at the screen.</li>
      </ul>
    </section>
  </div>{plan_html}{downloads}
</div>
<script>
const IMG = {json.dumps(imgs)};
const NAMES = {{ card_room: "Farrow & Ball Card Room Green No. 79, the chosen colour", treron: "Farrow & Ball Treron No. 292", sage: "Little Greene Sage Green No. 80", deep: "the deep forest green from earlier versions" }};
const VIEWS = {{ join: "Artisan oak media wall", four: "The dining wall, down and set for four", slats: "Slat wall alternative" }};
const state = {{ style: "join", paint: "card_room", key: false }};
try {{ const s = JSON.parse(localStorage.getItem("mw11") || "{{}}"); Object.assign(state, s); }} catch (e) {{}}
const shot = document.getElementById("shot"), cap = document.getElementById("cap"), keyBtn = document.getElementById("k-key");
function draw() {{
  if (state.style === "four") state.key = false;
  shot.src = state.key ? IMG["key_" + state.style] : IMG["art_" + state.style + "_" + state.paint];
  shot.alt = VIEWS[state.style] + (state.key ? " with numbered key" : " in " + NAMES[state.paint]);
  document.querySelectorAll("[data-style]").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.style === state.style)));
  document.querySelectorAll("[data-paint]").forEach(b => {{ b.setAttribute("aria-pressed", String(!state.key && b.dataset.paint === state.paint)); b.disabled = state.key; }});
  keyBtn.setAttribute("aria-pressed", String(state.key));
  keyBtn.disabled = state.style === "four";
  cap.textContent = state.key
    ? (state.style === "slats" ? "Numbered key for the slat wall alternative, in Card Room Green. Game drawer and lower record tray pulled out 30 cm." : "Full numbered key for the artisan oak build, in Card Room Green. Game drawer and lower record tray pulled out 30 cm. Dashed lines are hidden: gold for data, audio and low-voltage leads, coral for mains.")
    : VIEWS[state.style] + ", shown in " + NAMES[state.paint] + ". Evening light, drawn to the measured room.";
  try {{ localStorage.setItem("mw11", JSON.stringify(state)); }} catch (e) {{}}
}}
document.querySelectorAll("[data-style]").forEach(b => b.addEventListener("click", () => {{ state.style = b.dataset.style; draw(); }}));
document.querySelectorAll("[data-paint]").forEach(b => b.addEventListener("click", () => {{ state.paint = b.dataset.paint; draw(); }}));
keyBtn.addEventListener("click", () => {{ state.key = !state.key; draw(); }});
draw();
</script>
"""


def site():
    """The same page for GitHub Pages at the repo root: a full document, paths into media-wall/, and downloads."""
    import urllib.parse
    out = HERE.parent / "out"
    pdfs = sorted(out.glob("Home_Network_Plan_v*.pdf")) + sorted(out.glob("Build_Guide_v*.pdf"))
    def link(path, label):
        return f'<li><a href="media-wall/out/{urllib.parse.quote(path.name)}">{label}</a></li>'
    items = [link(p_, p_.stem.replace("_", " ").replace("Home Network Plan", "The full plan,") + " (PDF)") for p_ in pdfs]
    items += [link(p_, p_.stem) for p_ in sorted(out.glob("*.png"))]
    dl = ('\n  <section class="plans"><h2>Downloads</h2><ul class="plain">' + "".join(items) +
          '</ul><p class="caption">The PDF and the full-resolution renders, straight from the project folder. '
          'This page and the Claude viewer update together each round.</p></section>')
    body = page(prefix="media-wall/src/", downloads=dl)
    css_extra = "a { color: var(--oak); text-underline-offset: 2px; } a:focus-visible { outline: 2px solid var(--oak); outline-offset: 2px; }\n"
    body = body.replace("</style>", css_extra + "</style>", 1).replace("body { background", "body { margin: 0; background", 1)
    head, rest = body.split("</style>", 1)
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + head + "</style>\n</head>\n<body>" + rest + "</body>\n</html>\n")


if __name__ == "__main__":
    (HERE / "media_wall_viewer.html").write_text(page())
    (HERE.parent.parent / "index.html").write_text(site())
    print("viewer ok")
