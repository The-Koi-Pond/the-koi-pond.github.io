# Turns the drawn "The Koi Pond" wordmark (TheKoiPond.png, Xel's, made with
# ChatGPT) into clean SVGs: thekoipond-title.svg (brown letters) and
# thekoipond-title-dark.svg (cream letters, for dark mode). The curl on the
# "i" and the ripple underneath are jade in both.
#
# The letters and the jade parts are traced with Inkscape 1.4's tracer from
# masks that are enlarged and smoothed first, so the curves come out smooth.
#
#   python make_svg_wordmark.py TheKoiPond.png <output folder>
import os
import re
import subprocess
import sys
import tempfile
import xml.dom.minidom

import numpy as np
from PIL import Image, ImageFilter

INKSCAPE = r"C:\Program Files\Inkscape\bin\inkscape.com"
S = 6  # enlarge by this much before tracing (the picture is small)
src, out = sys.argv[1], sys.argv[2]

im = Image.open(src).convert("RGB")
w, h = im.size
a = np.asarray(im.resize((w * S, h * S), Image.LANCZOS)).astype(float)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
lum = 0.299 * r + 0.587 * g + 0.114 * b
parts = {
    "letters": lum < 100,
    "jade": (g - r > 20) & (lum < 200),  # the curl on the "i" and the ripple
}
tmp = tempfile.mkdtemp()


def trace(name, mask):
    img = Image.fromarray(np.where(mask, 0, 255).astype(np.uint8))
    img = img.filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(S * 0.8))
    img.point(lambda v: 0 if v < 128 else 255).save(os.path.join(tmp, name + ".png"))
    with open(os.path.join(tmp, "in.svg"), "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                f'width="{w * S}" height="{h * S}"><image id="img" x="0" y="0" width="{w * S}" '
                f'height="{h * S}" xlink:href="{name}.png"/></svg>')
    # Two colour scans, background removed: just the black shape is left.
    subprocess.run([INKSCAPE, "--actions=select-by-id:img;object-trace:2,false,false,true,60,1.0,0.2;"
                    "export-plain-svg;export-filename:out.svg;export-do", "in.svg"],
                   check=True, capture_output=True, cwd=tmp)
    paths = re.findall(r'<path[^>]*?\sd="([^"]+)"', open(os.path.join(tmp, "out.svg")).read())
    assert len(paths) == 1, (name, len(paths))
    return paths[0]


traced = {name: trace(name, mask) for name, mask in parts.items()}
ys, xs = np.nonzero(parts["letters"] | parts["jade"])
pad = 3 * S
box = f"{xs.min() - pad} {ys.min() - pad} {xs.max() - xs.min() + 2 * pad} {ys.max() - ys.min() + 2 * pad}"

for name, letters in [("thekoipond-title", "#361f17"), ("thekoipond-title-dark", "#f1ebe5")]:
    path = os.path.join(out, name + ".svg")
    with open(path, "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}" role="img" aria-label="The Koi Pond">\n'
                f'<title>The Koi Pond</title>\n'
                f'<path d="{traced["letters"]}" fill="{letters}"/>\n'
                f'<path d="{traced["jade"]}" fill="#5a9a8a"/>\n</svg>\n')
    xml.dom.minidom.parse(path)  # must be valid XML, or browsers show nothing
print("wrote", out)
