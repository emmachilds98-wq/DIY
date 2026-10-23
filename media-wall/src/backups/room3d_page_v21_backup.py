"""v14: the 3D room's piece of the plan page: its controls, its data and its script (room3d.js), plus a standalone copy for
the headless stills (shot3d.py). Three.js comes from jsDelivr, pinned."""
import html, json, pathlib
import scenes
import ideas
import render as R
import geometry as G

HERE = pathlib.Path(__file__).parent
THREE = "https://cdn.jsdelivr.net/npm/three@0.160.0/"
IMPORTMAP = ('<script type="importmap">' + json.dumps({"imports": {"three": THREE + "build/three.module.js",
                                                                   "three/addons/": THREE + "examples/jsm/"}}) + "</script>")

VIEWS = [("room", "The whole room"), ("window", "From the window"), ("wall", "The media wall"), ("sofa", "From the sofa"), ("door", "From the door"),
         ("stairs", "From the stairs"), ("dining", "The dining table"), ("chairs", "The chair cupboard"), ("breast", "The chimney breast"),
         ("windowwall", "The window wall"), ("pc", "The PC side wall"), ("plan", "Bird’s eye"), ("doll", "Dolls’ house")]   # v21: the whole room first

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
.r3d-size { font-size: 12px; color: #e9e4da; margin: 0 6px; font-variant-numeric: tabular-nums; }
.r3d-cap { position: absolute; left: 10px; bottom: 10px; right: 96px; margin: 0; color: #f3efe6; font-size: 12.5px; line-height: 1.35;
  text-shadow: 0 1px 3px #000c; pointer-events: none; }
.r3d-tools { position: absolute; right: 8px; bottom: 8px; display: flex; gap: 6px; }
.r3d-tools button { background: #000a; color: #fff; border: 1px solid #fff4; border-radius: 8px; padding: 6px 9px; font: inherit; font-size: 12px; cursor: pointer; }
/* v18: edit mode over the canvas: the Edit button, its bar (add, reset, a hint) and the panel for what you've picked */
.r3d-edit { position: absolute; top: 8px; left: 8px; right: 128px; display: grid; gap: 6px; justify-items: start; pointer-events: none; }
.r3d-edit > * { pointer-events: auto; }
.r3d-edit button, .r3d-edit .chip { background: #000b; color: #fff; border: 1px solid #fff5; border-radius: 8px; padding: 6px 10px; font: inherit; font-size: 13px; cursor: pointer; }
.r3d-edit button[aria-pressed=true] { background: #c9893f; border-color: #c9893f; color: #111; }
.r3d-editbar, .r3d-sel, .r3d-addlist { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; background: #0009; padding: 6px; border-radius: 10px; max-width: 100%; }
.r3d-editbar[hidden], .r3d-sel[hidden], .r3d-addlist[hidden], .r3d-sel [hidden] { display: none; }
.r3d-hint { color: #f3efe6; font-size: 12.5px; line-height: 1.3; max-width: 34em; }
.r3d-sel b { color: #fff; font-size: 13.5px; margin-right: 4px; }
.r3d-sel label { color: #fff; font-size: 13px; display: inline-flex; gap: 6px; align-items: center; }
.r3d-sel input[type=color] { width: 34px; height: 28px; padding: 0; border: 1px solid #fff5; border-radius: 6px; background: none; }
.r3d-sel .dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; vertical-align: -1px; }
.r3d.editing canvas { cursor: pointer; }
@media (max-width: 600px) { .r3d-edit button, .r3d-edit .chip { padding: 5px 8px; font-size: 12px; } .r3d-hint { display: none; }
  .r3d.editing .r3d-edit { right: 8px; } .r3d.editing .r3d-pad, .r3d.editing .r3d-cap { display: none; }
  .r3d-addlist, .r3d-sel { flex-wrap: nowrap; overflow-x: auto; scrollbar-width: none; } .r3d-addlist > *, .r3d-sel > * { flex: none; } }
details.r3d-more > summary { cursor: pointer; font-size: 14px; color: var(--muted); padding: 4px 0; }
details.r3d-more[open] > summary { margin-bottom: 8px; }
/* v17: walk buttons over the canvas (keys: WASD or arrows to move, Q and E to turn) */
.r3d-pad { position: absolute; top: 8px; right: 8px; display: grid; grid-template-columns: repeat(3, 32px); grid-auto-rows: 32px; gap: 4px; }
.r3d-pad button { background: #000a; color: #fff; border: 1px solid #fff4; border-radius: 8px; padding: 0; font: inherit; font-size: 15px; line-height: 1; cursor: pointer; touch-action: manipulation; }
.r3d-pad button:active { background: #000d; }
.r3d.nogl .r3d-pad { display: none; }
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
.r3d-decrow { display: grid; grid-template-columns: 9.5em 1fr; gap: 8px; align-items: center; }
.r3d-decrow > span { font-size: 13px; opacity: .8; }
@media (max-width: 560px) { .r3d-decrow { grid-template-columns: 1fr; gap: 4px; } }
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


LIGHTS = [("strip", "Ceiling LED strip", None), ("uprights", "Upright grooves and the side shelf (smart colour strips)", "strips"), ("bias", "TV bias light", None),
          ("bar1", "Bar 1, TV to window (smart colour)", "bar1"), ("bar2", "Bar 2, by the stairs (smart colour)", "bar2"),
          ("lamp", "Red lamp: top, middle, bottom", "lamp")]
CEIL_PRESETS = [("match", "Same as the walls"), ("#f2f0ea", "White")]
SKIRT_PRESETS = [("match", "Same as the walls"), ("#ece8dd", "Off-white"), ("#5e6a5b", "Green Smoke")]
SUGG_SHORT = {"floorplant": "Tall floor plant", "sidetable": "Round side table", "pouffe": "Knitted pouffe", "art": "Print over the sofa",
              "clock": "Clock over the door", "tray": "Coffee-table tray"}   # v21: the buttons' words for ideas.SUGGEST
# v20: decor to try in the 3D room (room3d.js S.decor; the keys match its RUG_LOOKS, CUSHION_COLS, CURTAIN_COLS, the case's PRESETS, CASE_FRAMES)
DECOR = [("rug", "Rug", [("yours", "Arches (the plan's)"), ("jute", "Jute flatweave"), ("blue", "Deep blue"), ("stripes", "Sage stripes"), ("none", "No rug")]),
         ("cushions", "Sofa cushions", [("none", "None"), ("rust", "Rust and ochre"), ("blues", "Blues"), ("sage", "Sage and cream")]),
         ("curtains", "Curtains", [("hessian", "Your hessian"), ("linen", "White linen"), ("sage", "Sage"), ("blue", "Deep blue"), ("rust", "Rust")]),
         ("fill", "In the glass case", [("collect", "Collectibles"), ("games", "Retro games"), ("singles", "7-inch singles and tapes"), ("plants", "Plants and ceramics"), ("mixed", "A bit of each")]),
         ("frame", "The case's frame", [("oak", "Oak"), ("black", "Black"), ("white", "White")])]


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
              '<details class="r3d-more"><summary>Fine-tune each light: sliders and bulb colours</summary>'
              f'<div class="r3d-lvs"><div class="r3d-lv r3d-master"><label for="lv-master">All lights</label><input type="range" id="lv-master" min="0" max="100" step="1" data-lv="master"><output data-lvout="master">100%</output><span></span></div>'
              + "".join(rows) + '</div></details>'
              '<div class="seg" role="group" aria-label="Light box, laser and curtains"><button type="button" data-tog="lbox" aria-pressed="false">IKEA light box on</button>'
              '<button type="button" data-tog="laser" aria-pressed="false">Laser on</button>'
              '<button type="button" data-tog="pc" aria-pressed="false">PC lit</button>'
              '<button type="button" data-tog="curtains" aria-pressed="false">Curtains drawn</button></div></div>'
              # v17: the ideas (ideas.py), all off by default: suggestions, not in the plan
              '<div class="grp"><span class="label">Ideas (not in the plan): off until you turn them on</span>'
              '<div class="seg" role="group" aria-label="Ideas, not in the plan"><button type="button" data-idea="case" aria-pressed="false">Glass case on the breast</button>'
              '<button type="button" data-idea="glass" aria-pressed="false">Glass plant shelves</button>'
              '<button type="button" data-idea="ctable" aria-pressed="false">Sofa C-table</button>''</div></div>'
              # v20, client: "give more decor variation and options": the rug, cushions, curtains, the glass case's fill and frame
              '<div class="grp r3d-wide r3d-decor"><span class="label">Decor: try a look (only the case and cushions are in the ideas, not the plan)</span>'
              + "".join(f'<div class="r3d-decrow"><span>{html.escape(lab)}</span><div class="seg" role="group" aria-label="{html.escape(lab)}">'
                        + "".join(f'<button type="button" data-decor="{k}:{v}" aria-pressed="false">{html.escape(n)}</button>' for v, n in opts) + '</div></div>'
                        for k, lab, opts in DECOR) + '</div>'
              # v21: suggested furniture and decor (ideas.SUGGEST), each on or off, all off to start
              '<div class="grp r3d-wide"><span class="label">Suggested furniture and decor: turn each on or off (not in the plan)</span>'
              '<div class="seg" role="group" aria-label="Suggested furniture and decor">'
              + "".join(f'<button type="button" data-sugg="{k}" aria-pressed="false" title="{html.escape(size)}">{html.escape(SUGG_SHORT[k])}</button>' for k, _t, size, *_ in ideas.SUGGEST)
              + '<button type="button" class="chip" data-suggall="on">All on</button><button type="button" class="chip" data-suggall="off">All off</button></div></div>')
    return "".join([
        seg("site", [("B", "Under the shelf, by the stairs"), ("A", "On the chimney breast")], "Where the table goes"),
        seg("dining", [("folded", "Folded on the wall"), ("four", "Open, four"), ("six", "Open, six")], "The flip-top table"),
        seg("chairs", [("cupboard", "Chair cupboard, shut"), ("open", "Chair cupboard, open"), ("hooks", "Open hooks instead"), ("away", "In the garage")], "Chairs, with the table folded"),
        # v18: your plant stand and record shelf, two layouts; the lamp, the ceiling and the skirting menus went: in "Edit room" you
        # drag the lamp, and tap the ceiling or the skirting to paint it
        seg("plants", [(k, v["name"]) for k, v in G.PLANT_LAYOUTS.items()], "Your plant stand and vinyl stand"),
        lights,
        seg("paint", paints, "Wall paint (or tap a wall in Edit room)", picker("r3d-custom", "#899081", "Any colour")),
        seg("drawers", [("in", "Shut"), ("out", "Pulled out")], "Drawers"),
        seg("quality", [("hd", "HD, with shadows"), ("fast", "Fast")], "Quality"),
    ])


def section():
    views = "".join(f'<button type="button" class="chip" data-view="{k}" aria-pressed="false">{v}</button>' for k, v in VIEWS)
    data = json.dumps(json.loads((HERE / "scene3d.json").read_text()), separators=(",", ":"))
    return f"""<div class="r3d" id="r3d">
  <div class="r3d-views" role="group" aria-label="Camera">{views}</div>
  <div class="r3d-stage"><canvas tabindex="0" aria-label="The living room in 3D: drag to look round, scroll or pinch to zoom; WASD or the arrow keys walk, Q and E turn"></canvas>
    <div class="r3d-edit"><button type="button" id="r3d-editbtn" aria-pressed="false" title="Move, turn, recolour, remove and add things; tap a wall to paint it">✎ Edit room</button>
      <div class="r3d-editbar" id="r3d-editbar" hidden><button type="button" id="r3d-add">+ Add</button><button type="button" id="r3d-undo" disabled title="Undo (Ctrl+Z)">↶ Undo</button><button type="button" id="r3d-layreset">Reset layout</button>
        <button type="button" class="r3d-share" id="r3d-share" hidden title="Save this layout so Emma and Dave both see it">Save for both of you</button><button type="button" class="r3d-share" id="r3d-useshared" hidden>Use the shared layout</button><span class="r3d-hint" id="r3d-sharest" aria-live="polite"></span>
        <span class="r3d-hint">Drag a thing to move it (it snaps to a wall within 5 cm); tap it to turn, recolour, copy or remove it. Tap a wall, the ceiling or the skirting to paint it.</span></div>
      <div class="r3d-addlist" id="r3d-addlist" hidden></div>
      <div class="r3d-sel" id="r3d-sel" hidden><b id="r3d-selname"></b><span class="r3d-size" id="r3d-selsize"></span><button type="button" data-sel="turn">⟳ Turn</button>
        <label>Colour <input type="color" id="r3d-selcol" value="#888888"></label><span id="r3d-swatches" hidden></span>
        <button type="button" data-sel="copy" hidden>Copy</button><button type="button" data-sel="remove">Remove</button><button type="button" data-sel="done">Done</button></div></div>
    <div class="r3d-pad" role="group" aria-label="Walk"><button type="button" data-walk="tl" title="Turn left (Q)" aria-label="Turn left">↺</button><button type="button" data-walk="f" title="Forward (W)" aria-label="Forward">▲</button><button type="button" data-walk="tr" title="Turn right (E)" aria-label="Turn right">↻</button><button type="button" data-walk="l" title="Step left (A)" aria-label="Step left">◀</button><button type="button" data-walk="b" title="Back (S)" aria-label="Back">▼</button><button type="button" data-walk="r" title="Step right (D)" aria-label="Step right">▶</button></div>
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
