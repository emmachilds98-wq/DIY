"""v14: stills from the 3D room, rendered headless (SwiftShader WebGL), for the PDF, the plan page and ../out.

python3 shot3d.py            -> the full set (HD PNGs in ../out, WebPs in art/ for the page, PNGs here for the PDF)
python3 shot3d.py test       -> a quick 1280 x 720 contact set in the scratch folder given by $SHOT3D_DIR (or here)
"""
import base64, io, os, pathlib, sys
from playwright.sync_api import sync_playwright
import room3d_page

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent / "out"
ART = HERE / "art"

# (file stem, options, title for ../out)
SHOTS = [
    ("3d_window_A_folded", dict(view="window", site="A", dining="folded", scene="everyday"), "from the window - table on the breast, folded - everyday evening"),
    ("3d_window_B_four", dict(view="window", site="B", dining="four", scene="dinner"), "from the window - table by the stairs, down for four - dinner"),
    ("3d_wall_tv", dict(view="wall", site="A", dining="folded", scene="tv"), "the media wall - TV night"),
    ("3d_sofa_records", dict(view="sofa", site="A", dining="folded", scene="records"), "from the sofa - records"),
    ("3d_B_folded", dict(view="dining", site="B", dining="folded", scene="everyday"), "the stairs wall - table folded under the shelf - everyday evening"),
    ("3d_stairs_A_four", dict(view="stairs", site="A", dining="four", scene="dinner"), "from the stairs - table on the breast, down for four - dinner"),
    ("3d_dining_A_four", dict(view="dining", site="A", dining="four", scene="dinner"), "the dining table on the breast, down for four - dinner"),
    ("3d_dining_B_four", dict(view="dining", site="B", dining="four", scene="dinner"), "the dining table by the stairs, down for four - dinner"),
    ("3d_six_day", dict(view="door", site="A", dining="six", scene="day"), "from the door - out for six - daytime"),
    ("3d_pc_day", dict(view="pc", site="A", dining="folded", scene="day"), "the PC side wall - daytime"),
    ("3d_plan_B", dict(view="plan", site="B", dining="four", scene="day"), "birds eye - table by the stairs, down for four"),
    ("3d_doll_A", dict(view="doll", site="A", dining="folded", scene="day"), "dolls house - table on the breast"),
]


def run(test=False, only=None):
    page_file = room3d_page.standalone()
    dest = pathlib.Path(os.environ.get("SHOT3D_DIR", HERE)) if test else HERE
    w, h = (1280, 720) if test else (2560, 1440)
    from PIL import Image
    with sync_playwright() as p:
        args = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--enable-webgl"]
        try:
            b = p.chromium.launch(args=args)
        except Exception:   # Playwright's own browser missing: use the preinstalled Chromium
            b = p.chromium.launch(args=args, executable_path="/opt/pw-browsers/chromium")
        pg = b.new_page(viewport={"width": 1400, "height": 1000})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.goto(page_file.as_uri())
        try:
            pg.wait_for_function("window.R3D && window.R3D.ready", timeout=120000)
        except Exception:
            print("3D room didn't start:", errs)
            raise
        for stem, opts, title in SHOTS:
            if only and only not in stem:
                continue
            pg.evaluate("o => window.R3D.set(o)", dict(opts, quality="hd"))
            url = pg.evaluate(f"() => window.R3D.still({w}, {h})")
            im = Image.open(io.BytesIO(base64.b64decode(url.split(",", 1)[1]))).convert("RGB")
            if test:
                im.save(dest / f"{stem}.png")
            else:
                im.save(OUT / f"Media wall v15 - 3D - {title} (HD).png")
                im.resize((1920, 1080), Image.LANCZOS).save(ART / f"{stem}.webp", quality=86)
                im.resize((1600, 900), Image.LANCZOS).save(HERE / f"render_v15_{stem}.png")
            print(stem, "ok")
        if errs:
            print("console:", errs[:8])
        b.close()


if __name__ == "__main__":
    run(test="test" in sys.argv, only=next((a for a in sys.argv[1:] if a != "test"), None))
