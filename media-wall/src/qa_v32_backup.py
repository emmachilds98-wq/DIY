"""v29.1 (v30: no questions sheet; the compact cabinet's step 11 and both cabinets' states): QA for the page (the GitHub Pages index.html), at 390 × 844 and 1280 × 800: console errors, sideways scroll, the version
label, the PDF links, every sheet and Plan chapter with every fold opened (anything poking past the screen's right edge that isn't in
a scroller), step 11 open, the dining cabinet's states in the 3D room.
    python3 qa.py [screenshot folder]       serves the repo itself; prints a JSON report, "fails" and "errors" should be empty
"""
import json, sys, threading, functools, http.server, pathlib, urllib.request
from playwright.sync_api import sync_playwright
from build_doc import VERSION

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
BASE = ""
CHAPTERS = ["c-room", "views", "wall", "records", "side", "joinery", "dining", "paint", "network", "fit", "downloads"]
SHEETS = ["plan", "build", "buy", "ideas"]   # v30: the questions sheet is gone
ARGS = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--enable-webgl"]

OVER = """sel => { const el = sel ? document.querySelector(sel) : document.scrollingElement;
  return el ? [el.scrollWidth, el.clientWidth] : null; }"""
# visible elements poking out past the viewport's right edge (inside the open sheet)
POKE = """sel => { const root = document.querySelector(sel); if (!root) return [];
  const W = innerWidth, out = [];
  for (const e of root.querySelectorAll('*')) { const r = e.getBoundingClientRect();
    if (r.width && r.height && r.right > W + 1 && !e.closest('.tscroll, .scroll, figure.dia, .lbscroll, .r3d-gal, .toc, .seg'))
      out.push((e.tagName + '.' + e.className).slice(0, 60) + ' ' + Math.round(r.right)); }
  return out.slice(0, 6); }"""


def run(p, w, h):
    rep = {"viewport": f"{w}x{h}", "errors": [], "fails": [], "notes": []}
    try:
        b = p.chromium.launch(args=ARGS)
    except Exception:
        b = p.chromium.launch(args=ARGS, executable_path="/opt/pw-browsers/chromium")
    ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
    pg = ctx.new_page()
    pg.on("pageerror", lambda e: rep["errors"].append("pageerror: " + str(e)[:200]))
    pg.on("console", lambda m: rep["errors"].append("console: " + m.text[:200]) if m.type == "error" else None)
    pg.goto(BASE)
    pg.wait_for_function("window.R3D && window.R3D.ready", timeout=180000)
    pg.wait_for_timeout(800)
    fail = rep["fails"].append
    ver = pg.eval_on_selector(".ver", "e => e.textContent")
    rep["notes"].append(f"version label {ver!r}")
    if ver != "v" + VERSION:
        fail(f"version label {ver!r}")
    sw, cw = pg.evaluate(OVER, None)
    if sw > cw:
        fail(f"page scrolls sideways {sw} > {cw}")
    pg.screenshot(path=f"{OUT}/qa_{w}_room.png")
    for s in SHEETS:
        pg.evaluate("s => { location.hash = '#' + s; }", s)
        pg.wait_for_timeout(500)
        if not pg.evaluate("s => document.getElementById('sh-' + s).classList.contains('open')", s):
            fail(f"sheet {s} didn't open")
        pg.evaluate("""s => { const r = document.getElementById('sh-' + s);
          r.querySelectorAll('details').forEach(d => d.open = true); r.querySelectorAll('.sbody').forEach(b => b.hidden = false); }""", s)
        pg.wait_for_timeout(300)
        poke = pg.evaluate(POKE, f"#sh-{s}")
        if poke:
            fail(f"sheet {s} overflows: {poke}")
    for ch in CHAPTERS:
        pg.evaluate("c => { location.hash = '#' + c; }", ch)
        pg.wait_for_timeout(400)
        vis = pg.evaluate("c => { const e = document.getElementById('ch-' + c); return !!e && !e.hidden && e.offsetHeight > 0; }", ch)
        if not vis:
            fail(f"chapter {ch} not shown")
        pg.evaluate("c => document.getElementById('ch-' + c).querySelectorAll('details').forEach(d => d.open = true)", ch)
        poke = pg.evaluate(POKE, f"#ch-{ch}")
        if poke:
            fail(f"chapter {ch} overflows: {poke}")
        if ch == "dining":
            pg.screenshot(path=f"{OUT}/qa_{w}_dining.png")
    # step 11, its body open
    pg.evaluate("() => { location.hash = '#step-11'; }")
    pg.wait_for_timeout(700)
    st = pg.evaluate("""() => { const e = document.getElementById('step-11'); if (!e) return null;
      const b = e.querySelector('.sbody'); return {open: e.classList.contains('open'), body: !!b && !b.hidden, text: e.innerText}; }""")
    if not st or not st["open"] or not st["body"]:
        fail(f"step 11 not open: {st and {k: v for k, v in st.items() if k != 'text'}}")
    else:
        t = st["text"]
        for bad in ("170°", "Lid stays", "linen flap", "Slido", "sliding door"):
            if bad in t:
                fail(f"step 11 still says {bad!r}")
        rep["notes"].append("step 11 mentions: " + ", ".join(k for k in ("Hang the two doors", "piano hinge", "flush magnet", "two boxes") if k in t))
    pg.screenshot(path=f"{OUT}/qa_{w}_step11.png")
    # back to the room; the cabinet's states
    pg.evaluate("() => { location.hash = '#room'; }")
    pg.wait_for_timeout(400)
    for opts in ({"site": "C", "cab": "sliding", "dining": "six", "view": "dining"}, {"site": "C", "cab": "compact", "dining": "folded", "tdoor": True, "view": "dining"},
                 {"site": "C", "dining": "six", "view": "dining"}, {"site": "C", "dining": "folded", "chairs": "open", "view": "chairs"},
                 {"site": "C", "dining": "folded", "view": "room"}, {"site": "B", "dining": "four"}, {"site": "C", "dining": "six", "view": "room"}):
        pg.evaluate("o => window.R3D.set(o)", opts)
        pg.wait_for_timeout(700)
    pg.screenshot(path=f"{OUT}/qa_{w}_room_six.png")
    sw, cw = pg.evaluate(OVER, None)
    if sw > cw:
        fail(f"page scrolls sideways after the 3D states {sw} > {cw}")
    has_tour = pg.evaluate("() => !!document.querySelector('[data-tour], #r3d-tour')")
    rep["notes"].append(f"tour control present: {has_tour}")
    b.close()
    return rep


def links():
    bad = []
    for f in (f"media-wall/out/Home_Network_Plan_v{VERSION}.pdf", f"media-wall/out/Build_Guide_v{VERSION}.pdf"):
        try:
            with urllib.request.urlopen(urllib.request.Request(BASE + f, method="HEAD")) as r:
                if r.status != 200:
                    bad.append(f"{f} {r.status}")
        except Exception as e:
            bad.append(f"{f} {e}")
    return bad


if __name__ == "__main__":
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    BASE = f"http://127.0.0.1:{srv.server_address[1]}/"
    res = {"links": links()}
    with sync_playwright() as p:
        res["runs"] = [run(p, 390, 844), run(p, 1280, 800)]
    print(json.dumps(res, indent=1))
