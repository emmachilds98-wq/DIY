"""Rasterise SVG/HTML files to PNG with headless Chromium.
python3 shot.py in.svg out.png width height [scale]"""
import sys, pathlib, os
from playwright.sync_api import sync_playwright


def launch(p):
    """Headless Chromium; falls back to a preinstalled browser when Playwright's own build is missing."""
    try:
        return p.chromium.launch()
    except Exception:
        return p.chromium.launch(executable_path=os.environ.get("CHROMIUM", "/opt/pw-browsers/chromium"))


if __name__ == "__main__":
    src, out, w, h = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 1.5
    url = pathlib.Path(src).resolve().as_uri()
    with sync_playwright() as p:
        b = launch(p)
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale)
        pg.goto(url)
        pg.wait_for_timeout(300)
        pg.screenshot(path=out, clip={"x": 0, "y": 0, "width": w, "height": h})
        b.close()
    print(out)
