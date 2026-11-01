# Turns Deki (Deki.png, The Koi Pond's mascot) into a clean SVG, deki.svg,
# with a see-through background.
#
# Each colour is cut out as a mask, enlarged and smoothed, and traced with
# Inkscape 1.4's tracer. The soft shadow under Deki, the faint shading on the
# body and the gloss on the curl are left out, so it stays crisp when small.
#
#   python make_svg_deki.py Deki.png <output folder>
import os
import re
import subprocess
import sys
import tempfile
import xml.dom.minidom

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

INKSCAPE = r"C:\Program Files\Inkscape\bin\inkscape.com"
S = 2  # enlarge by this much before tracing
src, out = sys.argv[1], sys.argv[2]

im = Image.open(src).convert("RGB")
w, h = im.size
a = np.asarray(im.resize((w * S, h * S), Image.LANCZOS)).astype(float)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
lum = 0.299 * r + 0.587 * g + 0.114 * b
rows = np.arange(h * S)[:, None] / S

dark = lum < 110  # the outline and the eyes
# Everything not dark that the picture's edge can reach is background (the
# shadow too); the rest is Deki.
labels, _ = ndimage.label(~dark)
edge = set(np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))) - {0}
deki = ~np.isin(labels, list(edge))
inside = deki & ~dark
jade = inside & (g - r > 20)
coral = inside & (r > 220) & (g < 175) & (b < 155) & (r - g > 60)


def biggest(mask, count):
    """Only the `count` biggest spots of a mask."""
    labels, n = ndimage.label(mask)
    sizes = ndimage.sum(mask, labels, range(1, n + 1))
    return np.isin(labels, np.argsort(sizes)[::-1][:count] + 1)


# The body's faint shading is blush-coloured too: keep the two cheeks only.
blush = biggest(inside & (r > 240) & (g > 195) & (g < 228) & (b > 185) & (b < 215) & (rows > 740), 2)
parts = {
    # The cream fill stops a little inside the outline: two smoothed edges in
    # the same place leave a pale rim, which shows on dark pages.
    "deki": ndimage.binary_erosion(deki, iterations=4 * S),
    "jade": jade,
    "jade-dark": jade & (lum < 175),  # the curl's shaded side, the fin creases
    "patches": coral & (rows <= 760),
    "blush": blush,
    "lines": coral & (rows > 760),  # the mouth and the blush marks
    "dark": dark & deki,
}
COLOURS = {"deki": "#fef6ed", "jade": "#a1cdc1", "jade-dark": "#7fb3a8", "patches": "#fd9e82",
           "blush": "#fed7ca", "lines": "#ef7a68", "dark": "#623a2d"}

tmp = tempfile.mkdtemp()


def trace(name, mask):
    img = Image.fromarray(np.where(mask, 0, 255).astype(np.uint8))
    img = img.filter(ImageFilter.MedianFilter(3)).filter(ImageFilter.GaussianBlur(S * 0.8))
    img.point(lambda v: 0 if v < 128 else 255).save(os.path.join(tmp, name + ".png"))
    with open(os.path.join(tmp, "in.svg"), "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                f'width="{w * S}" height="{h * S}"><image id="img" x="0" y="0" width="{w * S}" '
                f'height="{h * S}" xlink:href="{name}.png"/></svg>')
    # Two colour scans, background removed: just the black shape is left.
    subprocess.run([INKSCAPE, "--actions=select-by-id:img;object-trace:2,false,false,true,20,1.0,0.2;"
                    "export-plain-svg;export-filename:out.svg;export-do", "in.svg"],
                   check=True, capture_output=True, cwd=tmp)
    paths = re.findall(r'<path[^>]*?\sd="([^"]+)"', open(os.path.join(tmp, "out.svg")).read())
    assert len(paths) == 1, (name, len(paths))
    return paths[0]


layers = "\n".join(f'<path id="{name}" d="{trace(name, mask)}" fill="{COLOURS[name]}" fill-rule="evenodd"/>'
                   for name, mask in parts.items())
ys, xs = np.nonzero(deki)
pad = 8 * S
box = f"{xs.min() - pad} {ys.min() - pad} {xs.max() - xs.min() + 2 * pad} {ys.max() - ys.min() + 2 * pad}"
path = os.path.join(out, "deki.svg")
with open(path, "w") as f:
    f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}" role="img" aria-label="Deki">\n'
            f'<title>Deki</title>\n{layers}\n</svg>\n')
xml.dom.minidom.parse(path)  # must be valid XML, or browsers show nothing
print("wrote", path)
