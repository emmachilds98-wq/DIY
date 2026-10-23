"""v30: taps things in the 3D room (the cabinet, its doors, both versions, the media wall, the lamp, the curtains, the flip-top) at 1280 and 390
and prints what each card offers and what each button did.  python3 taptest.py [screenshot folder]"""
import sys, json, threading, functools, http.server, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = sys.argv[1] if len(sys.argv) > 1 else "."
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Q, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{srv.server_address[1]}/"
ARGS = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--enable-webgl"]
PROJ = """([x, y, z]) => { const { camera, THREE } = R3D._dbg; camera.updateMatrixWorld(); const v = new THREE.Vector3(-x / 100, y / 100, z / 100).project(camera);
  const r = document.querySelector('#r3d canvas').getBoundingClientRect(); return [r.left + (v.x + 1) / 2 * r.width, r.top + (1 - v.y) / 2 * r.height]; }"""
def run(w, h):
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch(args=ARGS, executable_path="/opt/pw-browsers/chromium")
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.on("pageerror", lambda e: errs.append(str(e)[:200])); pg.on("console", lambda m: errs.append(m.text[:200]) if m.type == "error" else None)
        pg.goto(BASE); pg.wait_for_function("window.R3D && window.R3D.ready", timeout=180000)
        pg.evaluate("() => document.querySelectorAll('.stk').forEach(s => s.style.pointerEvents = 'none')")   # the stickers sit over things
        def tap(pt, label):
            pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
            x, y = pg.evaluate(PROJ, pt); pg.mouse.click(x, y); pg.wait_for_timeout(400)
            vis = pg.evaluate("() => !document.getElementById('r3d-act').hidden")
            t = pg.evaluate("() => document.getElementById('r3d-act-h').textContent") if vis else None
            bs = pg.evaluate("() => [...document.querySelectorAll('#r3d-acts button')].map(b => b.textContent)") if vis else []
            print(f"  tap {label} at ({x:.0f},{y:.0f}) -> {t!r} {bs} errs={errs[-3:]}")
            return t
        def press(text):
            pg.locator("#r3d-acts button", has_text=text).first.click(); pg.wait_for_timeout(900)
        def S(k): return pg.evaluate(f"() => R3D._dbg.S.{k}")
        print(f"== {w}x{h}")
        pg.evaluate("() => R3D.set({site: 'C', cab: 'compact', dining: 'folded', chairs: 'cupboard', tdoor: false, view: 'dining'})"); pg.wait_for_timeout(600)
        tap([444, 45, -150], "the cabinet"); press("Open for six"); print("   dining:", S("dining")); pg.screenshot(path=f"{OUT}/tap_{w}_six.png")
        pg.wait_for_timeout(800); tap([444, 150, -200], "the cabinet again"); press("Fold it away"); print("   dining:", S("dining"))
        tap([444, 45, -205], "the chair door"); press("Open the chair door"); print("   chairs:", S("chairs")); pg.screenshot(path=f"{OUT}/tap_{w}_chairs.png")
        tap([444, 45, -150], "the cabinet"); press("Show the sliding one"); print("   cab:", S("cab")); pg.screenshot(path=f"{OUT}/tap_{w}_sliding.png")
        pg.evaluate("() => R3D.set({cab: 'compact', view: 'wall', drawers: false})"); pg.wait_for_timeout(600)
        tap([60, 30, 12], "the media wall's base"); press("Pull the drawers out"); print("   drawers:", S("drawers"))
        pg.evaluate("() => R3D.set({view: 'room'})"); pg.wait_for_timeout(600)
        lampxy = pg.evaluate("() => { const { MOV, THREE } = R3D._dbg; const b = new THREE.Box3().setFromObject(MOV.lamp.pivot), p = b.getCenter(new THREE.Vector3()); return [-p.x * 100, p.y * 100, p.z * 100]; }")
        tap(lampxy, "the lamp"); press("Turn it")
        print("   lamp level:", pg.evaluate("() => R3D._dbg.S.lv.lamp"))
        pg.evaluate("() => R3D.set({view: 'door'})"); pg.wait_for_timeout(600)
        cxy = pg.evaluate("() => { const { scene, THREE } = R3D._dbg; let best = null; scene.traverse(o => { if (o.isMesh && o.visible && o.parent && o.parent.visible && o.material && o.material.color && o.material.color.getHexString() === 'b9a47f' && !best) best = o; }); if (!best) return null; const c = new THREE.Box3().setFromObject(best).getCenter(new THREE.Vector3()); return [-c.x * 100, c.y * 100, c.z * 100]; }")
        print("   curtain centre:", cxy)
        if cxy and tap(cxy, "the curtains"): press("Draw them"); print("   curtains:", S("curtains"))
        else: print("   curtains: hidden from this view, skipped"); pg.keyboard.press("Escape")
        pg.screenshot(path=f"{OUT}/tap_{w}_curtains.png")
        pg.evaluate("() => R3D.set({site: 'B', dining: 'folded', view: 'dining'})"); pg.wait_for_timeout(600)
        tap([462, 76, -160], "the flip-top"); press("Open for four"); print("   site/dining:", S("site"), S("dining"))
        pg.evaluate("() => R3D.set({site: 'C', dining: 'folded', view: 'room'})")
        print("  errors:", errs[:5])
        b.close()
run(1280, 800); run(390, 844)
