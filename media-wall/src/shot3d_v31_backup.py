"""v14 (v16: the table by the stairs leads): stills from the 3D room, rendered headless (SwiftShader WebGL), for the PDF, the plan page and ../out.

python3 shot3d.py            -> the full set (HD PNGs in ../out, WebPs in art/ for the page, PNGs here for the PDF)
python3 shot3d.py test       -> a quick 1280 x 720 contact set in the scratch folder given by $SHOT3D_DIR (or here)
python3 shot3d.py force      -> every still again, even the ones that haven't changed

v28, from the optimisation plan: "only re-render the stills that changed". Each still has a fingerprint (its options and size, and
what the room is built from: room3d.js, scene3d.json, the lighting presets and the suggestions' versions), kept in
shot3d_prints.json. A still whose fingerprint matches is skipped; if only the version in its file names moved on, last round's
files are copied to the new names (from where they were, or from out/vNN/ once they've been moved there).
"""
import base64, hashlib, io, json, os, pathlib, shutil, sys
from playwright.sync_api import sync_playwright
import room3d_page

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent / "out"
ART = HERE / "art"
from build_doc import VERSION   # v28: the same number as the plan
PRINTS = HERE / "shot3d_prints.json"

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
    # v26: option C, the dining cabinet; v27: the plan, for six; v30: the compact cabinet is the plan, the sliding one the alternative
    ("3d_c_folded", dict(view="dining", site="C", dining="folded", scene="bright"), "THE COMPACT DINING CABINET - packed away - bright"),
    ("3d_c_six", dict(view="dining", site="C", dining="six", scene="bright"), "THE COMPACT DINING CABINET - open for six, the table door back flat - bright, table rule"),
    ("3d_window_c_six", dict(view="window", site="C", dining="six", scene="bright"), "THE COMPACT DINING CABINET - from the window, open for six - bright, table rule"),
    ("3d_c_tdoor", dict(view="dining", site="C", dining="folded", scene="bright", tdoor=True),
     "THE COMPACT DINING CABINET - the table door open - the folded table, the pads on the door, two chairs in the base - bright"),
    ("3d_c_chairs", dict(view="chairs", site="C", dining="folded", scene="bright", chairs="open", layout={"plants": {"off": True}, "lamp": {"off": True}}),
     "THE COMPACT DINING CABINET - the chair door open, four chairs inside (plant stand and lamp hidden) - bright"),
    ("3d_c_plan", dict(view="plan", site="C", dining="six", scene="bright", tod="day", master=0), "THE COMPACT DINING CABINET - birds eye, open for six"),
    # v31: the camera's new views, the floor the open table needs, and what could stand beside the compact cabinet
    ("3d_c_sit", dict(view="sit", site="C", dining="six", scene="bright", tod="day"), "THE COMPACT DINING CABINET - sitting at the table, open for six - daytime"),
    ("3d_c_foot", dict(view="plan", site="C", dining="folded", scene="bright", tod="day", master=0, foot=True), "THE COMPACT DINING CABINET - birds eye, folded, the floor it needs open"),
    ("3d_beside_mirror", dict(view="beside", site="C", dining="folded", scene="bright", beside="mirror"), "BESIDE THE CABINET - a tall mirror - bright"),
    ("3d_beside_trolley", dict(view="beside", site="C", dining="folded", scene="bright", beside="trolley"), "BESIDE THE CABINET - a slim trolley - bright"),
    ("3d_beside_dresser", dict(view="beside", site="C", dining="folded", scene="bright", beside="dresser"), "BESIDE THE CABINET - a low oak shelf - bright"),
    ("3d_s_folded", dict(view="dining", site="C", cab="sliding", dining="folded", scene="bright"), "THE SLIDING CABINET (the alternative) - packed away - bright"),
    ("3d_s_six", dict(view="dining", site="C", cab="sliding", dining="six", scene="bright"), "THE SLIDING CABINET (the alternative) - open for six - bright, table rule"),
    ("3d_s_chairs", dict(view="chairs", site="C", cab="sliding", dining="folded", scene="bright", chairs="open", layout={"plants": {"off": True}, "lamp": {"off": True}}),
     "THE SLIDING CABINET (the alternative) - the chair bay open, six chairs inside (plant stand and lamp hidden) - bright"),
    ("3d_look", dict(view="room", site="C", dining="folded", scene="bright", decor=dict(oak="walnut", floor="boards", shelf="oak", curtains="linen")),
     "LOOK to try - walnut on the new oak pieces, oak floorboards, your shelf in oak, white linen curtains - bright"),
]


BASE = {"drawers": False, "ideas": {}, "pc": True, "plants": "corner", "layout": {}, "added": [], "grow": True, "chairs": "cupboard", "decor": {},
        "sugg": {}, "svar": {}, "seat": "off", "tod": "evening", "master": 100, "cab": "compact", "tdoor": False, "foot": False, "beside": "clear"}   # v30: the compact cabinet; v31: the floor outline, beside it


def room_print():
    """What every still is built from."""
    h = hashlib.sha256()
    for part in ((HERE / "room3d.js").read_bytes(), (HERE / "scene3d.json").read_bytes(), room3d_page.scenes_json().encode(),
                 room3d_page.rules_json().encode(), room3d_page.svar_json().encode()):
        h.update(hashlib.sha256(part).digest())
    return h.hexdigest()


def shot_print(room, opts, w, h):
    return hashlib.sha256(json.dumps([room, dict(BASE, **opts, quality="hd"), w, h], sort_keys=True).encode()).hexdigest()[:24]


def targets(stem, title):
    return [OUT / f"Media wall v{VERSION} - 3D - {title} (HD).png", ART / f"{stem}.webp", HERE / f"render_v{VERSION}_{stem}.png"]


def _find(old):
    """Last round's file: where it was, or moved into out/vNN/."""
    old = pathlib.Path(old)
    if old.exists():
        return old
    for d in sorted(OUT.glob("v*/"), reverse=True):
        if (d / old.name).exists():
            return d / old.name
    return None


def reuse(rec, stem, title):
    """Copy last round's files to this round's names; False if any is missing."""
    new = targets(stem, title)
    olds = [_find(o) for o in rec.get("files", [])]
    if len(olds) != 3 or not all(olds):
        return False
    for o, n in zip(olds, new):
        if o.resolve() != n.resolve():
            shutil.copy2(o, n)
    return True


def run(test=False, only=None, force=False):
    page_file = room3d_page.standalone()
    dest = pathlib.Path(os.environ.get("SHOT3D_DIR", HERE)) if test else HERE
    w, h = (1280, 720) if test else (2560, 1440)
    from PIL import Image
    room = room_print()
    prints = json.loads(PRINTS.read_text()) if PRINTS.exists() else {}
    todo = []
    for stem, opts, title in SHOTS:
        if only and only not in stem:
            continue
        rec = prints.get(stem, {})
        rec_files = [HERE.parent / f for f in rec.get("files", [])]
        if not test and not force and not only and rec.get("print") == shot_print(room, opts, w, h) and reuse(dict(rec, files=rec_files), stem, title):
            if rec_files != targets(stem, title):
                prints[stem] = dict(rec, files=[str(x.relative_to(HERE.parent)) for x in targets(stem, title)])
            print(stem, "unchanged")
            continue
        todo.append((stem, opts, title))
    if not test:
        PRINTS.write_text(json.dumps(prints, indent=1, sort_keys=True) + "\n")
    print(f"{len(todo)} of {len(SHOTS)} stills to render")
    if not todo:
        return
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
        for stem, opts, title in todo:
            pg.evaluate("o => window.R3D.set(o)", dict(BASE, **opts, quality="hd"))
            url = pg.evaluate(f"() => window.R3D.still({w}, {h})")
            im = Image.open(io.BytesIO(base64.b64decode(url.split(",", 1)[1]))).convert("RGB")
            if test:
                im.save(dest / f"{stem}.png")
            else:
                t = targets(stem, title)
                im.save(t[0])
                im.resize((1920, 1080), Image.LANCZOS).save(t[1], quality=86)
                im.resize((1600, 900), Image.LANCZOS).save(t[2])
                prints[stem] = {"print": shot_print(room, opts, w, h), "files": [str(x.relative_to(HERE.parent)) for x in t]}
                PRINTS.write_text(json.dumps(prints, indent=1, sort_keys=True) + "\n")   # after each one, so a stopped run keeps what it made
            print(stem, "ok")
        if errs:
            print("console:", errs[:8])
        b.close()


if __name__ == "__main__":
    run(test="test" in sys.argv, force="force" in sys.argv, only=next((a for a in sys.argv[1:] if a not in ("test", "force")), None))
