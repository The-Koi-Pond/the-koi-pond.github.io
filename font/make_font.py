# Builds Pond Pebbles, The Koi Pond's display font, from Xel's drawn sheets
# (font/sheets/*.png, made with ChatGPT): PondPebbles.otf and
# PondPebbles.woff2 (for websites). For headings and special touches, not
# paragraphs.
#
# Each sheet is enlarged, smoothed and traced in one go with Inkscape 1.4's
# tracer; the traced outlines are sorted into characters by where they sit.
# Every row is measured (baseline, capital height), so all characters share
# one baseline and size: capitals and digits 700 units tall, of 1000.
#
#   python make_font.py   (needs Pillow, numpy, scipy, fontTools, brotli, Inkscape)
import os
import re
import subprocess
import tempfile

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
from fontTools.agl import UV2AGL
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
INKSCAPE = r"C:\Program Files\Inkscape\bin\inkscape.com"
S = 4  # enlarge by this much before tracing
CAP = 700  # capital and digit height, in font units (of 1000)
SIDE = 36  # space either side of each character
NAME = "Pond Pebbles"

# Each sheet's rows, left to right. On the first sheet Aa, Cc and Ee are
# drawn fused together (one shape each), so they're skipped there and come
# from the fix sheet instead, where they stand apart.
SHEETS = {
    "A-M": ["AaBbCcDdEeFfGg", "HhIiJjKkLlMm"],
    "N-Z": ["NnOoPpQqRrSsTt", "UuVvWwXxYyZz"],
    "numbers": ["0123456789", ".,!?:;\u2019\u201d-&()"],
    "symbols": ["@#/%+=*"],
    "fix": ["AaCcEe"],
}
FUSED = {"Aa", "Cc", "Ee"}
# Characters that sit on the baseline: lined up exactly on it. Everything
# else (tails, quotes, dashes, brackets) keeps its place against its row.
ON_BASELINE = set("ABCDEFGHIKLMNOPRSTUVWXYZabcdehiklmnorstuvwxz0123456789.!?:&#/%")
# Which characters set a row's size: its capitals, or digits, or the #.
SIZERS = set("ABCDEFGHIKLMNOPRSTUVWXYZ0123456789#")
# Extra keys that type the drawn characters.
ALSO = {"'": "\u2019", '"': "\u201d", "\u2018": "\u2019", "\u201c": "\u201d", "\u2013": "-"}

tmp = tempfile.mkdtemp()


def rows_of(ink, count_per_row):
    """Each row's characters as boxes (left, top, right, bottom), left to right."""
    labels, _ = ndimage.label(ink)
    boxes = [(s[1].start, s[0].start, s[1].stop, s[0].stop) for s in ndimage.find_objects(labels)]
    boxes = [b for b in boxes if (b[2] - b[0]) * (b[3] - b[1]) > 30]
    # Rows: split where the vertical middles jump.
    middles = sorted((b[1] + b[3]) / 2 for b in boxes)
    cuts = [m for m, n in zip(middles, middles[1:]) if n - m > 120]
    rows = [[] for _ in count_per_row]
    for b in boxes:
        rows[sum((b[1] + b[3]) / 2 > c for c in cuts)].append(list(b))
    out = []
    for glyphs, count in zip(rows, count_per_row):
        glyphs.sort(key=lambda b: b[0])
        tall = np.median([b[3] - b[1] for b in glyphs])
        # Join a small piece (a dot, a colon half, a % circle) to what it overlaps.
        joined = True
        while joined:
            joined = False
            for i in range(len(glyphs)):
                for j in range(i + 1, len(glyphs)):
                    g, h = glyphs[i], glyphs[j]
                    overlap = min(g[2], h[2]) - max(g[0], h[0])
                    small = min(g[3] - g[1], h[3] - h[1]) < 0.45 * tall
                    if overlap > 0.4 * min(g[2] - g[0], h[2] - h[0]) and small:
                        glyphs[i] = [min(g[0], h[0]), min(g[1], h[1]), max(g[2], h[2]), max(g[3], h[3])]
                        del glyphs[j]
                        joined = True
                        break
                if joined:
                    break
        # Still too many (the two marks of ”): join the closest neighbours.
        while len(glyphs) > count:
            k = int(np.argmin([glyphs[i + 1][0] - glyphs[i][2] for i in range(len(glyphs) - 1)]))
            g, h = glyphs[k], glyphs[k + 1]
            glyphs[k] = [min(g[0], h[0]), min(g[1], h[1]), max(g[2], h[2]), max(g[3], h[3])]
            del glyphs[k + 1]
        assert len(glyphs) == count, (len(glyphs), count)
        out.append(glyphs)
    return out


def trace(name, ink):
    """The whole sheet traced into one path (in enlarged pixels)."""
    img = Image.fromarray(np.where(ink, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(S * 0.7))
    img.point(lambda v: 0 if v < 128 else 255).save(os.path.join(tmp, name + ".png"))
    w, h = img.size
    with open(os.path.join(tmp, "in.svg"), "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" '
                f'height="{h}"><image id="img" x="0" y="0" width="{w}" height="{h}" xlink:href="{name}.png"/></svg>')
    subprocess.run([INKSCAPE, "--actions=select-by-id:img;object-trace:2,false,false,true,20,1.0,0.2;"
                    "export-plain-svg;export-filename:out.svg;export-do", "in.svg"],
                   check=True, capture_output=True, cwd=tmp)
    paths = re.findall(r'<path[^>]*?\sd="([^"]+)"', open(os.path.join(tmp, "out.svg")).read())
    assert len(paths) == 1, (name, len(paths))
    return paths[0]


def contours(d):
    """A traced path's outlines, each as recorded pen calls (absolute points)."""
    pen = RecordingPen()
    parse_path(d, pen)
    found, current = [], []
    for op, args in pen.value:
        current.append((op, args))
        if op in ("closePath", "endPath"):
            found.append(current)
            current = []
    return found


def points(contour):
    return [p for _, args in contour for p in args]


def area(pts):
    """Signed area (positive: counter-clockwise when y points up)."""
    xs, ys = np.array([p[0] for p in pts]), np.array([p[1] for p in pts])
    return 0.5 * float(np.dot(xs, np.roll(ys, -1)) - np.dot(ys, np.roll(xs, -1)))


def inside(pt, pts):
    x, y = pt
    hit = False
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            hit = not hit
    return hit


glyphs = {}  # character: (list of contours in font units, advance width)
for sheet, rows in SHEETS.items():
    im = Image.open(os.path.join(HERE, "sheets", sheet + ".png")).convert("L")
    small_ink = np.asarray(im).astype(float) < 110
    big = np.asarray(im.resize((im.width * S, im.height * S), Image.LANCZOS)).astype(float)
    ink = ndimage.median_filter(big < 128, size=5)
    names_per_row = []
    for chars in rows:
        names, i = [], 0
        while i < len(chars):
            pair = chars[i:i + 2]
            fused = sheet == "A-M" and pair in FUSED
            names.append(pair if fused else chars[i])
            i += 2 if fused else 1
        names_per_row.append(names)
    boxes = rows_of(small_ink, [len(n) for n in names_per_row])
    placed = []  # (character, box in enlarged pixels, row number)
    for r, (names, row_boxes) in enumerate(zip(names_per_row, boxes)):
        for name, b in zip(names, row_boxes):
            if len(name) == 2:
                continue  # a fused pair: taken from the fix sheet instead
            placed.append((name, [b[0] * S - 2 * S, b[1] * S - 2 * S, b[2] * S + 2 * S, b[3] * S + 2 * S], r))
    # Each row's baseline (where its on-baseline characters end) and size.
    row_base, row_scale = {}, {}
    for r in range(len(rows)):
        mine = [(c, b) for c, b, rr in placed if rr == r]
        base = float(np.median([b[3] for c, b in mine if c in ON_BASELINE]))
        row_base[r] = base
        sizers = [base - b[1] for c, b in mine if c in SIZERS]
        row_scale[r] = sizers and CAP / float(np.median(sizers))
    # A row with nothing to size it by (the punctuation) uses its sheet's.
    sheet_scale = np.median([s for s in row_scale.values() if s])
    traced = contours(trace(sheet, ink))
    for ch, b, r in placed:
        k = row_scale[r] or sheet_scale
        bottom = b[3] if ch in ON_BASELINE else row_base[r]
        mine = [c for c in traced if b[0] <= np.mean([p[0] for p in points(c)]) <= b[2]
                and b[1] <= np.mean([p[1] for p in points(c)]) <= b[3]]
        assert mine, ch
        left = min(p[0] for c in mine for p in points(c))
        right = max(p[0] for c in mine for p in points(c))
        # Into font units: from the character's left edge and its baseline, y up.
        transform = (k, 0, 0, -k, SIDE - left * k, bottom * k)
        moved = []
        for c in mine:
            rec = RecordingPen()
            for op, args in c:
                getattr(TransformPen(rec, transform), op)(*args)
            moved.append(rec.value)
        glyphs[ch] = (moved, round((right - left) * k + 2 * SIDE))


def glyph_name(ch):
    return UV2AGL.get(ord(ch), f"uni{ord(ch):04X}")


order = [".notdef", "space"] + [glyph_name(ch) for ch in glyphs]
cmap = {32: "space", **{ord(ch): glyph_name(ch) for ch in glyphs}}
cmap.update({ord(k): glyph_name(v) for k, v in ALSO.items()})
charstrings, metrics = {}, {}
for name, (outline, width) in [(".notdef", ([], 500)), ("space", ([], 230))] + [
        (glyph_name(ch), glyphs[ch]) for ch in glyphs]:
    # Outer outlines counter-clockwise, holes clockwise (what fonts expect).
    pen = T2CharStringPen(width, None)
    polys = [points(c) for c in outline]
    for c, pts in zip(outline, polys):
        depth = sum(inside(pts[0], other) for other in polys if other is not pts)
        clockwise = area(pts) < 0
        target = pen if clockwise == bool(depth % 2) else ReverseContourPen(pen)
        for op, args in c:
            getattr(target, op)(*args)
    charstrings[name] = pen.getCharString()
    bounds = BoundsPen(None)
    for c in outline:
        for op, args in c:
            getattr(bounds, op)(*args)
    metrics[name] = (width, round(bounds.bounds[0]) if bounds.bounds else 0)

fb = FontBuilder(1000, isTTF=False)
fb.setupGlyphOrder(order)
fb.setupCharacterMap(cmap)
fb.setupCFF("PondPebbles-Regular", {"FullName": NAME}, charstrings, {})
fb.setupHorizontalMetrics(metrics)
fb.setupHorizontalHeader(ascent=980, descent=-320)
fb.setupNameTable({"familyName": NAME, "styleName": "Regular", "uniqueFontIdentifier": "PondPebbles-Regular",
                   "fullName": NAME, "psName": "PondPebbles-Regular",
                   "copyright": "Copyright 2026 Xelvanis (The Koi Pond)"})
fb.setupOS2(sTypoAscender=980, sTypoDescender=-320, sTypoLineGap=0, usWinAscent=1050, usWinDescent=360,
            sCapHeight=CAP, sxHeight=round(CAP * 0.59), achVendID="KOIP")
fb.setupPost()
otf = os.path.join(HERE, "PondPebbles.otf")
fb.save(otf)
web = TTFont(otf)
web.flavor = "woff2"
web.save(os.path.join(HERE, "PondPebbles.woff2"))
print("wrote", otf, "with", len(glyphs), "characters")
