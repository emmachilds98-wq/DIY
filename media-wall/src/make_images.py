"""Builds every render and diagram image the plan, the out/ folder and the viewer use (v10).
python3 make_images.py          -> SVGs here, PNGs for the PDF here, HD PNGs in ../out, viewer JPGs in art/
"""
import pathlib, re
from PIL import Image, ImageDraw, ImageFont
import render as R, diagrams as D, shot

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent / "out"
ART = HERE / "art"
FONT = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
FONT_R = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"


def svgs():
    names = R.all_svgs()
    for n, s in names.items():
        (HERE / f"{n}.svg").write_text(s)
    return names


def main():
    svgs()
    W, H, KW = R.W, R.H, R.W + R.KEYW
    jobs = [
        # for the PDF
        ("v10_join_key.svg", "render_v10_join_key_scene.png", W, H, 1.1),
        ("v10_join_clean.svg", "render_v10_join_clean.png", W, H, 1.1),
        ("v10_slat_clean.svg", "render_v10_slat_clean.png", W, H, 0.9),
        # HD, labelled, for the client
        ("v10_join_clean.svg", OUT / "Media wall v10 - artisan oak - Card Room Green (HD).png", W, H, 2.0),
        ("v10_join_key.svg", OUT / "Media wall v10 - artisan oak - numbered key (HD).png", KW, H, 2.0),
        ("v10_join_dims.svg", OUT / "Media wall v10 - artisan oak - heights and widths (HD).png", W, H, 2.0),
        ("v10_slat_key.svg", OUT / "Media wall v10 - slat wall alternative - numbered key.png", KW, H, 1.25),
        ("v10_slat_clean.svg", OUT / "Media wall v10 - slat wall alternative.png", W, H, 1.25),
    ]
    for k in ("card_room", "sage", "treron", "deep"):
        jobs.append((f"v10_paint_{k}_joinery.svg", f"p_{k}.png", W, H, 0.5))
        for st, tag in (("joinery", "join"), ("slats", "slats")):
            jobs.append((f"v10_paint_{k}_{st}.svg", f"art_{tag}_{k}.png", W, H, 0.82))
    for k in R.SKIRT_OPTIONS:
        jobs.append((f"v10_skirt_{k}.svg", f"skirt_{k}.png", W, H, 1.0))
    jobs.append(("v10_join_key.svg", "art_key_join.png", KW, H, 0.82))
    jobs.append(("v10_slat_key.svg", "art_key_slats.png", KW, H, 0.82))
    # plan diagrams as images for out/ and the viewer
    for name, fn, label in [("house", D.house, "House plan - Decos and Cat6"), ("living", D.living_plan, "Living room plan - as measured")]:
        s = fn()
        vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', s)
        w, h = int(vb.group(1)), int(vb.group(2))
        (HERE / f"d_{name}.svg").write_text(s.replace('width="100%"', f'width="{w}"'))
        jobs.append((f"d_{name}.svg", OUT / f"{label}.png", w, h, 2.4))
    shot.shots([(HERE / a if isinstance(a, str) else a, HERE / b if isinstance(b, str) else b, w, h, sc) for a, b, w, h, sc in jobs])

    # paint grid: the oak version in four greens
    tiles = [("card_room", "Farrow & Ball Card Room Green No. 79 (chosen)"), ("sage", "Little Greene Sage Green No. 80"),
             ("treron", "Farrow & Ball Treron No. 292"), ("deep", "Deep forest green (earlier versions)")]
    tw, th, gap = 1100, 700, 24
    grid = Image.new("RGB", (2 * tw + 3 * gap, 2 * (th + 44) + 3 * gap), "#f4efe4")
    f = ImageFont.truetype(FONT, 26)
    for i, (k, lab) in enumerate(tiles):
        im = Image.open(HERE / f"p_{k}.png").convert("RGB").resize((tw, th))
        x, y = gap + (i % 2) * (tw + gap), gap + (i // 2) * (th + 44 + gap)
        grid.paste(im, (x, y + 44))
        ImageDraw.Draw(grid).text((x, y + 6), lab, font=f, fill="#14261d")
    grid.save(HERE / "paint_grid.png")
    grid.save(OUT / "Paint options - four greens.png")

    # skirting options: the same corner of the room in three skirting colours
    crop = (110, 990, 1010, 1400)
    labs = {"card_room": "Card Room Green, Estate Eggshell (recommended)", "green_smoke": "Green Smoke (darker edge)", "off_white": "Soft off-white"}
    cw, ch = crop[2] - crop[0], crop[3] - crop[1]
    strip = Image.new("RGB", (3 * cw + 4 * gap, ch + 60 + 2 * gap), "#f4efe4")
    for i, k in enumerate(R.SKIRT_OPTIONS):
        im = Image.open(HERE / f"skirt_{k}.png").convert("RGB").crop(crop)
        x = gap + i * (cw + gap)
        strip.paste(im, (x, gap + 52))
        ImageDraw.Draw(strip).text((x, gap + 8), labs[k], font=f, fill="#14261d")
    strip.save(HERE / "skirting_options.png")
    strip.save(OUT / "Skirting options with Card Room Green.png")

    # viewer images
    ART.mkdir(exist_ok=True)
    for p in HERE.glob("art_*.png"):
        Image.open(p).convert("RGB").save(ART / (p.stem.replace("art_key_", "key_") + ".jpg"), quality=86, optimize=True)
        p.unlink()
    for name, label in (("zz_house", "House plan - Decos and Cat6"), ("zz_living", "Living room plan - as measured")):
        Image.open(OUT / f"{label}.png").convert("RGB").save(ART / f"{name}.jpg", quality=88, optimize=True)
    for p in list(HERE.glob("p_*.png")) + list(HERE.glob("skirt_*.png")):
        p.unlink()
    print("images ok")


if __name__ == "__main__":
    main()
