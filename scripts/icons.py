import sys
from PIL import Image, ImageDraw
out = sys.argv[1]
def door(size, pad):
    S = size * 4
    im = Image.new("RGBA", (S, S), (122, 171, 69, 255))
    d = ImageDraw.Draw(im)
    # sky band + hill
    d.rectangle([0, 0, S, S * .42], fill=(223, 240, 242, 255))
    d.ellipse([-S * .3, S * .28, S * 1.3, S * 1.9], fill=(122, 171, 69, 255))
    c, r = S / 2, (S / 2) * (1 - pad)
    cy = S * .58
    d.ellipse([c - r, cy - r, c + r, cy + r], fill=(185, 154, 107, 255))
    r2 = r * .84
    d.ellipse([c - r2, cy - r2, c + r2, cy + r2], fill=(47, 107, 58, 255))
    w = max(2, int(S * .012))
    import math
    for k in (-.6, -.3, 0, .3, .6):
        x = c + r2 * k
        h = math.sqrt(max(0, r2 * r2 - (r2 * k) ** 2))
        d.line([x, cy - h, x, cy + h], fill=(36, 88, 48, 255), width=w)
    kr = r2 * .11
    d.ellipse([c - kr, cy - kr, c + kr, cy + kr], fill=(201, 149, 43, 255), outline=(138, 100, 20, 255), width=w)
    return im.resize((size, size), Image.LANCZOS)
for size, pad, name in [(192, .38, "icon-192.png"), (512, .38, "icon-512.png"), (512, .5, "maskable-512.png"), (180, .38, "apple-touch-icon.png"), (32, .3, "favicon-32.png")]:
    im = door(size, pad)
    if name == "apple-touch-icon.png": im = im.convert("RGB")
    im.save(f"{out}/{name}")
