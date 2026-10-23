"""Builds the interactive viewer page (v10): style × paint × key, with the images in art/.
python3 build_viewer.py  -> media_wall_viewer.html (images referenced as art/*.jpg, published alongside it)"""
import json, pathlib
import geometry as G
import fit

HERE = pathlib.Path(__file__).parent
LPS = 2 * G.TRAY_LPS + G.BROWSER_LPS + G.LEDGE_LPS
SINGLES = 2 * G.TRAY_SINGLES + G.BAYB_SINGLES

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


def page():
    c = fit.counts()
    total = sum(c.values())
    imgs = {k: f"art/{k}.jpg" for k in [f"art_{s}_{p}" for s in ("join", "slats") for p in ("card_room", "deep", "sage", "treron")] + ["key_join", "key_slats"]}
    return f"""<title>Media Wall v10</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Atkinson+Hyperlegible:wght@400;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
{STYLE}
<div class="wrap">
  <header>
    <h1>Media Wall v10</h1>
    <p class="lede">The artisan oak build in Farrow &amp; Ball Card Room Green, now drawn to the room as you measured it. Compare it with the slat wall, try the other greens, or turn on the numbered key.</p>
    <p class="change"><b>What changed:</b> the alcove is {G.ALC_W:g} × {G.ALC_D:g} cm with a {G.CEIL:g} cm ceiling, not 225 × 50 × 220. The TV, the Series X and three bays still fit; a turntable doesn't, so the deck, the LP browser and both record trays move into a matching oak cabinet against the chimney breast.</p>
  </header>

  <div class="viewer">
    <div class="frame"><img id="shot" alt="Render of the media wall" width="1804" height="1148"></div>
    <div class="controls">
      <div class="group"><span class="label" id="l-style">Version</span>
        <div class="seg" role="group" aria-labelledby="l-style">
          <button id="s-join" data-style="join" aria-pressed="true">Artisan oak (main)</button>
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
        <li><b>{G.HIGH_TOP:g}</b><span>High shelf: books up to 30 cm, a box, a print, Deco B</span></li>
        <li><b>{G.SIDE_SHELF_TOP:g}</b><span>Side shelves · record ledge at {G.LEDGE_TOP:g}</span></li>
        <li><b>{G.LID_CLEAR_TO:g}</b><span>Chimney breast kept clear to here for the deck's lid</span></li>
        <li><b>116.5</b><span>TV centre, LG C6 55in on its stand</span></li>
        <li><b>{G.WORKTOP:g}</b><span>Oak worktop and the vinyl cabinet's top</span></li>
        <li><b>{G.PLINTH:g}</b><span>Plinth under the two BESTÅ bays</span></li>
      </ul>
    </section>
    <section>
      <h2>In the wall</h2>
      <div class="counts">
        <div><strong>~{LPS}</strong><span>LPs, all face-out</span></div>
        <div><strong>~{SINGLES}</strong><span>singles, all face-out</span></div>
        <div><strong>~48</strong><span>games, every title visible</span></div>
      </div>
      <ul class="plain">
        <li>Alcove: the TV between two oak uprights, the Series X on its fan stand to the left, three 60 cm bays below for the Xbox consoles, the PlayStations and the sub.</li>
        <li>Vinyl cabinet, 100 × 44 × 76 cm: two face-out record trays, a singles drawer and a preamp cubby, with the deck and the LP browser on top.</li>
        <li>Fit proof: {c[fit.PASS]} of {total} checks fit outright against published sizes; the Series X's sides are tight, and the RetroTINK and the door get a check on site.</li>
        <li>Power: the socket on the side wall in front of bay 1 becomes a double; Deco B runs from an always-on socket via the groove behind the right upright.</li>
      </ul>
    </section>
    <section>
      <h2>Lighting</h2>
      <ul class="plain">
        <li>The LED strip you have now, on the ceiling round the whole room, facing down.</li>
        <li>A four-head cone spotlight bar on the existing rose, Wolston style: sage and blue on the shelves and ledge, mustard on the coffee table, pink on the vinyl corner. None at the TV.</li>
        <li>LED grooves in the oak uprights and a bias light behind the TV.</li>
      </ul>
    </section>
  </div>
  <section class="plans">
    <h2>The living room and the house</h2>
    <div class="frame"><img src="art/zz_living.jpg" alt="Living room plan drawn from the measured sketch, with the media wall, vinyl cabinet, sofa, spotlight bar, socket and viewing distance" width="2064" height="1440"></div>
    <div class="frame"><img src="art/zz_house.jpg" alt="Three floor plans with the Decos, Cat6 runs, chimney breast, brick cupboard and sloped ceilings" width="2064" height="1488"></div>
    <p class="caption">The living room is drawn from your measurements; the house outline is traced from the agent's plans. Deco A and Switch 1 sit in bedroom 3 with the Hub 5, and both Cat6 runs drop through the airing cupboard, right over the media wall's corner.</p>
  </section>
</div>
<script>
const IMG = {json.dumps(imgs)};
const NAMES = {{ card_room: "Farrow & Ball Card Room Green No. 79, the chosen colour", treron: "Farrow & Ball Treron No. 292", sage: "Little Greene Sage Green No. 80", deep: "the deep forest green from earlier versions" }};
const state = {{ style: "join", paint: "card_room", key: false }};
try {{ const s = JSON.parse(localStorage.getItem("mw10") || "{{}}"); Object.assign(state, s); }} catch (e) {{}}
const shot = document.getElementById("shot"), cap = document.getElementById("cap");
function draw() {{
  shot.src = state.key ? IMG["key_" + state.style] : IMG["art_" + state.style + "_" + state.paint];
  shot.alt = (state.style === "slats" ? "Slat wall" : "Artisan oak") + " version" + (state.key ? " with numbered key" : " in " + NAMES[state.paint]);
  document.querySelectorAll("[data-style]").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.style === state.style)));
  document.querySelectorAll("[data-paint]").forEach(b => {{ b.setAttribute("aria-pressed", String(!state.key && b.dataset.paint === state.paint)); b.disabled = state.key; }});
  document.getElementById("k-key").setAttribute("aria-pressed", String(state.key));
  cap.textContent = state.key
    ? (state.style === "slats" ? "Numbered key for the slat wall alternative, in Card Room Green. Game drawer and lower record tray pulled out 30 cm." : "Full numbered key for the artisan oak build, in Card Room Green. Dashed lines are hidden: gold for data, audio and low-voltage leads, coral for mains.")
    : "Shown in " + NAMES[state.paint] + ". Evening light, drawn to the measured room.";
  try {{ localStorage.setItem("mw10", JSON.stringify(state)); }} catch (e) {{}}
}}
document.querySelectorAll("[data-style]").forEach(b => b.addEventListener("click", () => {{ state.style = b.dataset.style; draw(); }}));
document.querySelectorAll("[data-paint]").forEach(b => b.addEventListener("click", () => {{ state.paint = b.dataset.paint; draw(); }}));
document.getElementById("k-key").addEventListener("click", () => {{ state.key = !state.key; draw(); }});
draw();
</script>
"""


if __name__ == "__main__":
    (HERE / "media_wall_viewer.html").write_text(page())
    print("viewer ok")
