"""Builds the viewer artifact page (media_wall_viewer.html) from the v10 renders.
python3 build_viewer.py   (after python3 render.py)"""
import base64, json, pathlib, subprocess
from PIL import Image
import diagrams

HERE = pathlib.Path(__file__).parent
ART = HERE / "art"
PAINTS = ["card_room", "sage", "treron", "deep"]


def shot(svg, png, w, h, scale):
    subprocess.run(["python3", "shot.py", svg, png, str(w), str(h), str(scale)], cwd=HERE, check=True, capture_output=True)


def jpg(png, out, width, quality=82):
    im = Image.open(HERE / png).convert("RGB")
    im = im.resize((width, round(im.size[1] * width / im.size[0])), Image.LANCZOS)
    im.save(ART / out, quality=quality, optimize=True)


def make_art():
    ART.mkdir(exist_ok=True)
    for p in PAINTS:
        shot(f"v10_paint_{p}.svg", f"p_{p}.png", 1900, 1300, 1)
        jpg(f"p_{p}.png", f"art_join_{p}.jpg", 1800)
        shot(f"v10_slats_{p}.svg", f"s_{p}.png", 1900, 1300, 1)
        jpg(f"s_{p}.png", f"art_slats_{p}.jpg", 1800)
    shot("v10_join_key.svg", "k_join.png", 2540, 1300, 1)
    jpg("k_join.png", "key_join.jpg", 2400, 85)
    for name, fn in (("zz_living", diagrams.living_plan), ("zz_house", diagrams.house)):
        (HERE / f"{name}.html").write_text('<html><body style="margin:0;background:#fff;width:860px">' + fn() + "</body></html>")
        shot(f"{name}.html", f"{name}.png", 860, 640 if name == "zz_house" else 600, 2)
        jpg(f"{name}.png", f"{name}.jpg", 1600, 85)
        (HERE / f"{name}.html").unlink()


def uri(name):
    return "data:image/jpeg;base64," + base64.b64encode((ART / name).read_bytes()).decode()


BODY = """<div class="wrap">
  <header>
    <h1>Media Wall v10</h1>
    <p class="lede">Re-fitted to your measured room: a 186 cm alcove, 38 deep, with a 235 cm ceiling. The artisan oak wall in Farrow &amp; Ball Card Room Green, and the vinyl corner on the chimney breast beside it. Compare the slat wall, try the other greens, or turn on the numbered key.</p>
  </header>
  <div class="wait"><p><b>One decision for you:</b> the real alcove is 39 cm narrower than we'd assumed, so the turntable and the two record trays can't sit beside the TV any more. This version moves them to a matching oak cabinet against the chimney breast. Happy with that?</p></div>

  <div class="viewer">
    <div class="frame"><img id="shot" alt="Render of the media wall" width="1800" height="1232"></div>
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
        <li><b>235</b><span>Ceiling, measured</span></li>
        <li><b>200</b><span>High shelf: books up to 30 cm, box, print, Deco B</span></li>
        <li><b>156</b><span>Side shelves · record ledge at 155.4</span></li>
        <li><b>140</b><span>LP frames on the breast, clear of the deck's lid</span></li>
        <li><b>116.6</b><span>TV centre, LG C6 55in on its stand</span></li>
        <li><b>76</b><span>Oak worktop 186 × 42 · vinyl cabinet top</span></li>
        <li><b>9</b><span>Plinth under the two BESTÅ bays</span></li>
      </ul>
    </section>
    <section>
      <h2>What fits</h2>
      <div class="counts">
        <div><strong>~234</strong><span>LPs, all face-out</span></div>
        <div><strong>~240</strong><span>singles face-out, plus overflow</span></div>
        <div><strong>~48</strong><span>games, every title visible</span></div>
      </div>
      <ul class="plain">
        <li>The TV fits between the oak uprights with 2 cm to spare each side; the Series X on its fan stand has 2.4 cm each side in the left gap.</li>
        <li>Base: 3 + 60 + 60 + 60 + 3 = 186. Xbox bay with the game drawer, PlayStation bay, and an open bay for the sub with a hidden drawer.</li>
        <li>Vinyl cabinet 100 × 44 × 76 on the breast: the two face-out trays, the preamp, the deck and the LP browser on top.</li>
      </ul>
    </section>
    <section>
      <h2>Lighting</h2>
      <ul class="plain">
        <li>Your LED strip round the ceiling, facing down, as now.</li>
        <li>The four-head Wolston-style spotlight bar on the existing rose. With the 235 ceiling the lowest shade hangs at about 212 cm.</li>
        <li>LED grooves in the oak uprights and a bias light behind the TV.</li>
      </ul>
    </section>
  </div>
  <section class="plans">
    <h2>The living room and the house</h2>
    <div class="frame"><img src="@@LIVING@@" alt="Living room from above, from the measured sketch"></div>
    <div class="frame"><img src="@@HOUSE@@" alt="House plan with the Decos and Cat6 runs"></div>
    <p class="caption">The living room is redrawn from your sketch. Deco A and Switch 1 now sit in bedroom 3 with the Hub 5; both Cat6 runs cross the landing and drop through the airing cupboard, over the alcove's corner.</p>
  </section>
</div>
<script>
const IMG = @@IMG@@;
const NAMES = { card_room: "Farrow & Ball Card Room Green No. 79, the chosen colour", treron: "Farrow & Ball Treron No. 292", sage: "Little Greene Sage Green No. 80", deep: "the deep forest green from earlier versions" };
const state = { style: "join", paint: "card_room", key: false };
try { const s = JSON.parse(localStorage.getItem("mw10") || "{}"); Object.assign(state, s); } catch (e) {}
const shot = document.getElementById("shot"), cap = document.getElementById("cap");
function draw() {
  if (state.key) state.style = "join";
  shot.src = state.key ? IMG.key_join : IMG["art_" + state.style + "_" + state.paint];
  shot.alt = (state.style === "slats" ? "Slat wall" : "Artisan oak") + " version" + (state.key ? " with numbered key" : " in " + NAMES[state.paint]);
  document.querySelectorAll("[data-style]").forEach(b => { b.setAttribute("aria-pressed", String(b.dataset.style === state.style)); b.disabled = state.key && b.dataset.style === "slats"; });
  document.querySelectorAll("[data-paint]").forEach(b => { b.setAttribute("aria-pressed", String(!state.key && b.dataset.paint === state.paint)); b.disabled = state.key; });
  document.getElementById("k-key").setAttribute("aria-pressed", String(state.key));
  cap.textContent = state.key
    ? "Full numbered key for the artisan oak build, in Card Room Green, with the game drawer and lower record tray pulled out 30 cm. Dashed lines are hidden: gold for data, audio and low-voltage leads, coral for mains."
    : "Shown in " + NAMES[state.paint] + ". Rendered in evening light, to your measurements.";
  try { localStorage.setItem("mw10", JSON.stringify(state)); } catch (e) {}
}
document.querySelectorAll("[data-style]").forEach(b => b.addEventListener("click", () => { state.style = b.dataset.style; draw(); }));
document.querySelectorAll("[data-paint]").forEach(b => b.addEventListener("click", () => { state.paint = b.dataset.paint; draw(); }));
document.getElementById("k-key").addEventListener("click", () => { state.key = !state.key; draw(); });
draw();
</script>
"""


def build():
    head = (HERE / "viewer_head.html").read_text().replace("<title>Media Wall v9</title>", "<title>Media Wall v10</title>")
    imgs = {f"art_{s}_{p}": uri(f"art_{s}_{p}.jpg") for s in ("join", "slats") for p in PAINTS}
    imgs["key_join"] = uri("key_join.jpg")
    body = BODY.replace("@@IMG@@", json.dumps(imgs)).replace("@@LIVING@@", uri("zz_living.jpg")).replace("@@HOUSE@@", uri("zz_house.jpg"))
    (HERE / "media_wall_viewer.html").write_text(head + "\n" + body)


if __name__ == "__main__":
    make_art()
    build()
    print("viewer ok", (HERE / "media_wall_viewer.html").stat().st_size)
