"""v14: the 3D room's piece of the plan page: its controls, its data and its script (room3d.js), plus a standalone copy for
the headless stills (shot3d.py). Three.js comes from jsDelivr, pinned."""
import html, json, pathlib
import scenes
import render as R
import geometry as G

HERE = pathlib.Path(__file__).parent
THREE = "https://cdn.jsdelivr.net/npm/three@0.160.0/"
IMPORTMAP = ('<script type="importmap">' + json.dumps({"imports": {"three": THREE + "build/three.module.js",
                                                                   "three/addons/": THREE + "examples/jsm/"}}) + "</script>")

VIEWS = [("window", "From the window"), ("wall", "The media wall"), ("sofa", "From the sofa"), ("door", "From the door"),
         ("stairs", "From the stairs"), ("dining", "The dining table"), ("pc", "The PC side wall"), ("plan", "Bird’s eye"),
         ("doll", "Dolls’ house")]

CSS = """
.r3d { display: grid; grid-template-columns: minmax(0, 1fr); gap: 12px; min-width: 0; }
.r3d > * { min-width: 0; }
.r3d-stage { position: relative; background: #0d100e; border-radius: 14px; overflow: hidden; aspect-ratio: 16 / 9; }
@media (max-width: 600px) { .r3d-stage { aspect-ratio: 4 / 3; } }
.r3d-stage:fullscreen { border-radius: 0; aspect-ratio: auto; }
.r3d-stage canvas { display: block; width: 100%; max-width: 100%; height: 100%; touch-action: none; cursor: grab; }
.r3d-stage canvas:active { cursor: grabbing; }
.r3d-msg { position: absolute; inset: 0; display: grid; place-items: center; padding: 24px; text-align: center; color: #e7ebe3; font-size: 15px; }
.r3d-msg a { color: #d9a46c; }
.r3d-msg[hidden] { display: none; }
.r3d-cap { position: absolute; left: 10px; bottom: 10px; right: 96px; margin: 0; color: #f3efe6; font-size: 12.5px; line-height: 1.35;
  text-shadow: 0 1px 3px #000c; pointer-events: none; }
.r3d-tools { position: absolute; right: 8px; bottom: 8px; display: flex; gap: 6px; }
.r3d-tools button { background: #000a; color: #fff; border: 1px solid #fff4; border-radius: 8px; padding: 6px 9px; font: inherit; font-size: 12px; cursor: pointer; }
.r3d-views { display: flex; gap: 6px; overflow-x: auto; padding-bottom: 2px; scrollbar-width: thin; }
.r3d-views button { flex: none; }
.r3d-ui { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 10px 18px; }
.r3d-ui .grp { min-width: 0; }
.r3d-ui .label { display: block; margin-bottom: 6px; }
.r3d-ui .seg { flex-wrap: wrap; }
.r3d-ui input[type=color] { width: 34px; height: 30px; padding: 0; border: 1px solid var(--line); border-radius: 8px; background: none; vertical-align: middle; }
.r3d-save { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
.r3d.nogl .r3d-ui, .r3d.nogl .r3d-views { display: none; }
.r3d-wide { grid-column: 1 / -1; display: grid; gap: 10px; }
.r3d-lvs { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 8px 22px; }
.r3d-lv { display: grid; grid-template-columns: minmax(0, 1fr) auto; grid-template-areas: "lab out" "range range" "cols cols"; gap: 2px 10px; align-items: center; min-width: 0; }
.r3d-lv label { grid-area: lab; font-size: 14px; }
.r3d-lv input[type=range] { grid-area: range; width: 100%; accent-color: var(--oak, #9a6634); }
.r3d-lv output { grid-area: out; font-variant-numeric: tabular-nums; font-size: 13px; color: var(--muted); }
.r3d-lv .r3d-cols { grid-area: cols; display: flex; gap: 6px; align-items: center; flex-wrap: wrap; }
.r3d-lv .r3d-cols:empty { display: none; }
.r3d-lv input[type=color] { width: 34px; height: 26px; }
.r3d-master label { font-weight: 700; }
.r3d-pick { padding: 4px 8px !important; }
"""


def scenes_json():
    return json.dumps({k: {"name": n, "levels": lv} for k, n, _, lv, _ in scenes.SCENES})


LIGHTS = [("strip", "Ceiling LED strip", None), ("uprights", "Upright grooves and the side shelf", None), ("bias", "TV bias light", None),
          ("bar1", "Bar 1, TV to window (smart colour)", "bar1"), ("bar2", "Bar 2, by the stairs (smart colour)", "bar2"),
          ("lamp", "Red lamp: top, middle, bottom", "lamp")]
CEIL_PRESETS = [("match", "Same as the walls"), ("#f2f0ea", "White")]
SKIRT_PRESETS = [("match", "Same as the walls"), ("#ece8dd", "Off-white"), ("#5e6a5b", "Green Smoke")]


def controls():
    seg = lambda attr, items, lab, extra="": (f'<div class="grp"><span class="label">{lab}</span><div class="seg" role="group" aria-label="{html.escape(lab)}">'
                                              + "".join(f'<button type="button" data-{attr}="{k}" aria-pressed="false">{v}</button>' for k, v in items) + extra + "</div></div>")
    paints = [(k, f'<span class="dot" style="background:{h}"></span>{html.escape(n.split(" No.")[0].replace("Farrow & Ball ", "").replace("Little Greene ", ""))}')
              for k, (h, n) in R.PAINTS.items()]
    picker = lambda pid, val, lab: f'<label class="btn r3d-pick">{lab} <input type="color" id="{pid}" value="{val}" aria-label="{html.escape(lab)}"></label>'
    # v15: every light on a slider, the smart bars and the lamp's three bulbs in any colour; the scene buttons fill the sliders in
    rows = []
    for k, lab, col in LIGHTS:
        cols = ""
        if col == "lamp":
            cols = "".join(f'<input type="color" data-col="lamp{i}" value="{c}" aria-label="Lamp bulb {n} colour">' for i, (c, n) in enumerate(zip(G.LAMP_HEADS_RGB, ("top", "middle", "bottom"))))
        elif col:
            cols = f'<input type="color" data-col="{col}" value="#ffe2b8" aria-label="{html.escape(lab)} colour"><button type="button" class="chip" data-colreset="{col}">Warm white</button>'
        rows.append(f'<div class="r3d-lv"><label for="lv-{k}">{html.escape(lab)}</label><input type="range" id="lv-{k}" min="0" max="100" step="1" data-lv="{k}">'
                    f'<output data-lvout="{k}">0%</output><span class="r3d-cols">{cols}</span></div>')
    lights = (f'<div class="grp r3d-wide"><span class="label">Lights: pick a scene, then slide any light</span>'
              f'<div class="seg" role="group" aria-label="Lighting scene">' + "".join(f'<button type="button" data-scene="{k}" aria-pressed="false">{n}</button>' for k, n, *_ in scenes.SCENES)
              + '<button type="button" data-scene="day" aria-pressed="false">Daytime</button></div>'
              f'<div class="r3d-lvs"><div class="r3d-lv r3d-master"><label for="lv-master">All lights</label><input type="range" id="lv-master" min="0" max="100" step="1" data-lv="master"><output data-lvout="master">100%</output><span></span></div>'
              + "".join(rows) + '</div>'
              '<div class="seg" role="group" aria-label="On the stairs-wall shelf"><button type="button" data-tog="lbox" aria-pressed="false">IKEA light box on</button>'
              '<button type="button" data-tog="laser" aria-pressed="false">Laser on</button></div></div>')
    return "".join([
        seg("site", [("A", "On the chimney breast"), ("B", "Under the shelf, by the stairs")], "Where the table goes"),
        seg("dining", [("folded", "Folded"), ("four", "Down for four"), ("six", "Out for six")], "The table"),
        lights,
        seg("paint", paints, "Wall paint", picker("r3d-custom", "#899081", "Any colour")),
        seg("ceil", CEIL_PRESETS, "Ceiling paint", picker("r3d-ceil", "#f2f0ea", "Any colour")),
        seg("skirt", SKIRT_PRESETS, "Skirting, door and radiator", picker("r3d-skirt", "#ece8dd", "Any colour")),
        seg("lamp", [(k, v[0]) for k, v in G.FLOOR_LAMP_SPOTS.items()], "Where the red lamp stands"),
        seg("drawers", [("in", "Shut"), ("out", "Pulled out")], "Drawers"),
        seg("quality", [("hd", "HD, with shadows"), ("fast", "Fast")], "Quality"),
    ])


def section():
    views = "".join(f'<button type="button" class="chip" data-view="{k}" aria-pressed="false">{v}</button>' for k, v in VIEWS)
    data = json.dumps(json.loads((HERE / "scene3d.json").read_text()), separators=(",", ":"))
    return f"""<div class="r3d" id="r3d">
  <div class="r3d-views" role="group" aria-label="Camera">{views}</div>
  <div class="r3d-stage"><canvas aria-label="The living room in 3D: drag to look round, scroll or pinch to zoom"></canvas>
    <div class="r3d-msg" id="r3d-msg">Loading the 3D room…</div>
    <p class="r3d-cap" id="r3d-cap"></p>
    <div class="r3d-tools"><button type="button" id="r3d-reset" title="Back to this view">Reset</button><button type="button" id="r3d-full" title="Full screen">Full screen</button></div></div>
  <div class="r3d-ui">{controls()}</div>
  <div class="r3d-save"><button class="btn primary" type="button" id="r3d-save">Save this view as an HD picture</button><span class="caption" id="r3d-savest" aria-live="polite">3840 × 2160 PNG, with shadows</span></div>
</div>
<script type="application/json" id="scene3d-data">{data}</script>
<script type="application/json" id="scenes-data">{scenes_json()}</script>
<script type="module">{(HERE / "room3d.js").read_text()}</script>
<script>setTimeout(() => {{ const r = document.getElementById("r3d"), m = document.getElementById("r3d-msg");
  if (r && !r.classList.contains("ready") && !r.classList.contains("nogl")) m.innerHTML = 'The 3D room needs a moment, or your connection blocked its 3D library. The <a href="#views" data-go="views">drawn views</a> show every option.'; }}, 20000);</script>"""


def standalone(path=HERE / "room3d_test.html"):
    css = ":root{--line:#d4d9cd;--muted:#5b6457}body{margin:0;background:#eef0ea;font:15px system-ui}.wrap{max-width:1600px;margin:auto;padding:12px}" \
          ".seg{display:flex;gap:6px}.btn,.seg button,.chip{border:1px solid #ccc;background:#fff;border-radius:8px;padding:6px 10px;font:inherit}" \
          ".seg button[aria-pressed=true],.chip[aria-pressed=true]{background:#2f4f3a;color:#fff}.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}.label{font-weight:700;font-size:12px}"
    path.write_text(f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                    f'<title>Room in 3D</title>{IMPORTMAP}<style>{css}{CSS}</style></head><body><div class="wrap">{section()}</div></body></html>')
    return path


if __name__ == "__main__":
    print(standalone())
