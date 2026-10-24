"""v47.1: the garden through the 3D room's window: art/garden_day.webp and art/garden_dusk.webp from inputs/photo_garden_summer_24oct.jpg.
Run it again with a new photo (change the crop) to update the view."""
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageChops
import numpy as np
src = Image.open("/home/user/DIY/media-wall/inputs/photo_garden_summer_24oct.jpg").convert("RGB")
crop = src.crop((0, 560, 1449, 2370)); CW, H = crop.size; W = 2 * H; side = (W - CW) // 2
pano = Image.new("RGB", (W, H)); pano.paste(crop, (side, 0))
lstrip = crop.crop((0, 0, 420, H)).transpose(Image.FLIP_LEFT_RIGHT).resize((side, H)).filter(ImageFilter.GaussianBlur(4))
rstrip = crop.crop((CW - 420, 0, CW, H)).transpose(Image.FLIP_LEFT_RIGHT).resize((side, H)).filter(ImageFilter.GaussianBlur(4))
pano.paste(lstrip, (0, 0)); pano.paste(rstrip, (side + CW, 0))
a = np.asarray(pano).astype(np.float32); blur = np.asarray(pano.filter(ImageFilter.GaussianBlur(10))).astype(np.float32)
x = np.arange(W)[None, :, None]
m = np.clip(1 - np.minimum(abs(x - side), abs(x - (side + CW))) / 36.0, 0, 1)
a = a * (1 - m) + blur * m
v = 1 - 0.22 * (abs(x - W / 2) / (W / 2)) ** 2
dayim = Image.fromarray(np.clip(a * v, 0, 255).astype(np.uint8))
dayim = ImageEnhance.Color(ImageEnhance.Contrast(dayim).enhance(1.08)).enhance(1.06)
dayim.resize((2048, 1024), Image.LANCZOS).save("/home/user/DIY/media-wall/src/art/garden_day.webp", quality=84)
# dusk: blue hour. Exposure down, cooler, less colour; the sky a deep blue fading to dusky lilac at the horizon; the room's own light
# on the patio
d = np.asarray(dayim).astype(np.float32) / 255
L = 0.2126 * d[..., 0] + 0.7152 * d[..., 1] + 0.0722 * d[..., 2]
grey = L[..., None]
d2 = grey + (d - grey) * 0.55                                      # less colour
d2 = np.power(np.clip(d2, 0, 1), 1.25) * 0.56 * np.array([0.84, 0.93, 1.16])[None, None, :] + np.array([0.015, 0.02, 0.04])
yy = np.linspace(0, 1, H)[:, None]
sat = d.max(-1) - d.min(-1)
sky = np.clip((L - 0.70) / 0.16, 0, 1) * np.clip((0.5 - yy) / 0.2, 0, 1) * np.clip((0.22 - sat) / 0.12, 0, 1)
sky = np.asarray(Image.fromarray((sky * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))).astype(np.float32) / 255
top, low = np.array([0.13, 0.17, 0.33]), np.array([0.40, 0.38, 0.52])
t = np.clip(yy / 0.5, 0, 1)[..., None]
skyc = top * (1 - t) + low * t
out = d2 * (1 - sky[..., None]) + skyc * sky[..., None]
im = Image.fromarray(np.clip(out * 255, 0, 255).astype(np.uint8))
glow = Image.new("L", (W, H), 0); ImageDraw.Draw(glow).ellipse([side - 300, int(H * 0.68), side + CW + 300, int(H * 1.3)], fill=140)
glow = glow.filter(ImageFilter.GaussianBlur(110))
im = Image.composite(ImageChops.screen(im, Image.new("RGB", (W, H), (255, 186, 110))), im, glow.point(lambda p: int(p * 0.42)))
im.resize((2048, 1024), Image.LANCZOS).save("/home/user/DIY/media-wall/src/art/garden_dusk.webp", quality=84)

