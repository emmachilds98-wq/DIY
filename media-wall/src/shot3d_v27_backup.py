"""v14 (v16: the table by the stairs leads): stills from the 3D room, rendered headless (SwiftShader WebGL), for the PDF, the plan page and ../out.

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
    ("3d_room", dict(view="room", site="C", dining="folded", scene="bright"), "the whole room - from above the window side, cut away - bright"),   # v21: the new default view
    ("3d_window_B_folded", dict(view="window", site="B", dining="folded", scene="bright"), "B, THE FLIP-TOP - from the window - table by the stairs, folded - bright"),
    ("3d_window_B_four", dict(view="window", site="B", dining="four", scene="bright"), "B, THE FLIP-TOP - from the window - down for four - bright, table rule"),
    ("3d_wall_film", dict(view="wall", site="C", dining="folded", scene="film"), "the media wall - film"),
    ("3d_wall_drawers", dict(view="wall", site="C", dining="folded", scene="cosy", drawers=True), "the media wall - every drawer out - cosy"),
    ("3d_sofa_cosy", dict(view="sofa", site="C", dining="folded", scene="cosy"), "from the sofa - cosy"),
    ("3d_B_folded", dict(view="dining", site="B", dining="folded", scene="bright"), "B, THE FLIP-TOP - the stairs wall - table folded under the shelf - bright"),
    ("3d_chairs", dict(view="chairs", site="B", dining="folded", scene="bright", chairs="open", layout={"plants": {"off": True}, "lamp": {"off": True}}), "B, THE FLIP-TOP - the chair cupboard beside the table, doors open, four chairs inside (plant stand and lamp hidden) - bright"),
    ("3d_chairs_shut", dict(view="dining", site="B", dining="folded", scene="bright", chairs="cupboard", layout={}), "B, THE FLIP-TOP - packed away - the table folded and the chair cupboard shut - bright"),
    ("3d_stairs_A_four", dict(view="stairs", site="A", dining="four", scene="bright"), "from the stairs - table on the breast, down for four - bright, table rule"),
    ("3d_dining_A_four", dict(view="dining", site="A", dining="four", scene="bright"), "the dining table on the breast, down for four - bright, table rule"),
    ("3d_dining_B_four", dict(view="dining", site="B", dining="four", scene="bright"), "B, THE FLIP-TOP - by the stairs, down for four - bright, table rule"),
    ("3d_six_day", dict(view="door", site="A", dining="six", scene="bright", tod="day", master=0), "from the door - out for six - daytime"),
    ("3d_pc_day", dict(view="pc", site="C", dining="folded", scene="bright", tod="day", master=0), "the PC side wall - daytime"),
    ("3d_plan_B", dict(view="plan", site="B", dining="four", scene="bright", tod="day", master=0), "B, THE FLIP-TOP - birds eye, down for four"),
    ("3d_doll_A", dict(view="doll", site="A", dining="folded", scene="bright", tod="day", master=0), "dolls house - table on the breast"),
    # v17: the bright preset (was General), the lit PC, and the ideas (not in the plan)
    ("3d_window_bright", dict(view="window", site="C", dining="folded", scene="bright"), "from the window - bright, every head straight down"),
    ("3d_pc_lit", dict(view="pc", site="C", dining="folded", scene="film", pc=True), "the PC side wall - PC lit - film"),
    # v18: your plant stand and your vinyl stand, both layouts
    ("3d_plants_corner", dict(view="windowwall", site="C", dining="folded", scene="bright"), "your plant stand in the window corner - layout A - bright"),
    ("3d_records_breast", dict(view="breast", site="C", dining="folded", scene="cosy"), "your vinyl stand on the breast - layout A - cosy"),
    ("3d_plants_breast", dict(view="breast", site="C", dining="folded", scene="bright", plants="breast"), "layout B - your plant stand on the breast - bright"),
    ("3d_ideas_window", dict(view="windowwall", site="C", dining="folded", scene="bright", ideas=dict(glass=True)), "IDEAS (not in the plan) - the window wall - glass plant shelves beside your plant stand"),
    ("3d_ideas_ctable", dict(view="pc", site="C", dining="folded", scene="bright", ideas=dict(ctable=True)), "IDEAS (not in the plan) - the C-table at the sofa's open end"),
    ("3d_ideas_breast", dict(view="breast", site="C", dining="folded", scene="bright", ideas=dict(case=True)), "IDEAS (not in the plan) - the tall glass case on the breast, oak, collectibles"),
    # v20: the taller case with other things in it, and decor to try
    ("3d_case_mixed", dict(view="breast", site="C", dining="folded", scene="bright", ideas=dict(case=True), decor=dict(fill="mixed", frame="black")),
     "IDEAS (not in the plan) - the tall glass case, black frame, a bit of each"),
    ("3d_case_singles", dict(view="breast", site="C", dining="folded", scene="cosy", ideas=dict(case=True), decor=dict(fill="singles", frame="white")),
     "IDEAS (not in the plan) - the tall glass case, white frame, 7-inch singles and tapes - cosy"),
    ("3d_decor", dict(view="door", site="C", dining="folded", scene="bright", decor=dict(rug="stripes", cushions="rust", curtains="linen")),
     "DECOR to try - sage-stripe rug, rust and ochre cushions, white linen curtains - bright"),
    # v21: the suggested furniture and decor, all on
    ("3d_suggest", dict(view="door", site="C", dining="folded", scene="bright", sugg={k: True for k, *_ in __import__("ideas").SUGGEST}),
     "SUGGESTED furniture and decor, all of them on - bright"),
    ("3d_seat", dict(view="dining", site="B", dining="folded", scene="bright", seat="down"), "B, THE FLIP-TOP - the fold-down seat at the stair end, down - bright"),
    # v26: option C, the dining cabinet; v27: the plan, for six
    ("3d_c_folded", dict(view="dining", site="C", dining="folded", scene="bright"), "THE DINING CABINET - packed away - bright"),
    ("3d_c_six", dict(view="dining", site="C", dining="six", scene="bright"), "THE DINING CABINET - open for six - bright, table rule"),
    ("3d_window_c_six", dict(view="window", site="C", dining="six", scene="bright"), "THE DINING CABINET - from the window, open for six - bright, table rule"),
    ("3d_c_chairs", dict(view="chairs", site="C", dining="folded", scene="bright", chairs="open", layout={"plants": {"off": True}, "lamp": {"off": True}}),
     "THE DINING CABINET - the chair bay open, six chairs inside (plant stand and lamp hidden) - bright"),
    ("3d_c_plan", dict(view="plan", site="C", dining="six", scene="bright", tod="day", master=0), "THE DINING CABINET - birds eye, open for six"),
    ("3d_look", dict(view="room", site="C", dining="folded", scene="bright", decor=dict(oak="walnut", floor="boards", shelf="oak", curtains="linen")),
     "LOOK to try - walnut on the new oak pieces, oak floorboards, your shelf in oak, white linen curtains - bright"),
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
            pg.evaluate("o => window.R3D.set(o)", dict({"drawers": False, "ideas": {}, "pc": True, "plants": "corner", "layout": {}, "added": [], "grow": True, "chairs": "cupboard", "decor": {}, "sugg": {}, "seat": "off", "tod": "evening", "master": 100}, **opts, quality="hd"))
            url = pg.evaluate(f"() => window.R3D.still({w}, {h})")
            im = Image.open(io.BytesIO(base64.b64decode(url.split(",", 1)[1]))).convert("RGB")
            if test:
                im.save(dest / f"{stem}.png")
            else:
                im.save(OUT / f"Media wall v27 - 3D - {title} (HD).png")
                im.resize((1920, 1080), Image.LANCZOS).save(ART / f"{stem}.webp", quality=86)
                im.resize((1600, 900), Image.LANCZOS).save(HERE / f"render_v27_{stem}.png")
            print(stem, "ok")
        if errs:
            print("console:", errs[:8])
        b.close()


if __name__ == "__main__":
    run(test="test" in sys.argv, only=next((a for a in sys.argv[1:] if a != "test"), None))
