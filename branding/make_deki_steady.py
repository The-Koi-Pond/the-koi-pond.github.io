# Makes deki-steady.svg: Deki (deki.svg) gently squishing, nonstop, like a
# soft mochi breathing. Used on the home page.
#
#   python branding/make_deki_steady.py deki.svg .
#
# The animation is CSS inside the SVG, so a plain <img> plays it. Firefox
# ignores the SVG's own reduced-motion rule when it's shown as an <img>, so
# pages must also swap in the still deki.svg for people who ask for less
# motion (a <picture> with a prefers-reduced-motion source; see index.html).
# Rerun this after deki.svg changes.
import re
import sys
import xml.dom.minidom
from pathlib import Path

src, out = Path(sys.argv[1]), Path(sys.argv[2])
svg = src.read_text(encoding="utf-8")
x, y, w, h = (float(v) for v in re.search(r'viewBox="([^"]+)"', svg).group(1).split())

# How much Deki squashes wide and stretches tall (1.05 = 5% more), and how
# long one squish takes.
WIDE, TALL, SECONDS = 1.05, 1.03, 1.6

# deki.svg has almost no room around Deki, so add what the squish needs:
# half the extra width each side (it squishes about the middle), all the
# extra height on top (it squishes from where it sits).
pad_x, pad_top = w * (WIDE - 1) / 2, h * (TALL - 1)
box = f"{x - pad_x:.0f} {y - pad_top:.0f} {w + 2 * pad_x:.0f} {h + pad_top:.0f}"

style = f"""<style>
.squish {{
  transform-box: fill-box;
  transform-origin: 50% 100%;
  animation: squish {SECONDS}s ease-in-out infinite;
}}
@keyframes squish {{
  0%, 100% {{ transform: scale({WIDE}, {2 - WIDE:.2f}); }}
  50% {{ transform: scale({2 - TALL:.2f}, {TALL}); }}
}}
@media (prefers-reduced-motion: reduce) {{
  .squish {{ animation: none; }}
}}
</style>"""

opening = re.search(r"<svg[^>]*>", svg).group(0)
body = svg.replace(opening, re.sub(r'viewBox="[^"]+"', f'viewBox="{box}"', opening) + "\n" + style + '\n<g class="squish">', 1)
body = body.replace("</svg>", "</g>\n</svg>")
path = out / "deki-steady.svg"
path.write_text(body, encoding="utf-8", newline="\n")
xml.dom.minidom.parse(str(path))  # must be valid XML, or browsers show nothing
print("wrote", path, "viewBox", box)
