"""Rasterise SVG/HTML files to PNG with headless Chromium.
python3 shot.py in.svg out.png width height [scale]
From Python: shots([(in, out, w, h, scale), ...]) renders many with one browser."""
import sys, glob, pathlib
from playwright.sync_api import sync_playwright


def _launch(p):
    try:
        return p.chromium.launch()
    except Exception:   # Playwright's own browser missing: use any preinstalled Chromium
        exe = sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"))
        return p.chromium.launch(executable_path=exe[-1])


def shots(jobs):
    with sync_playwright() as p:
        b = _launch(p)
        for src, out, w, h, scale in jobs:
            pg = b.new_page(viewport={"width": int(w), "height": int(h)}, device_scale_factor=float(scale))
            pg.goto(pathlib.Path(src).resolve().as_uri())
            pg.wait_for_timeout(300)
            pg.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": int(w), "height": int(h)})
            pg.close()
            print(out)
        b.close()


if __name__ == "__main__":
    a = sys.argv[1:]
    shots([(a[0], a[1], int(a[2]), int(a[3]), float(a[4]) if len(a) > 4 else 1.5)])
