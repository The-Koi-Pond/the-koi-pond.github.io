# Makes the pictures for Bentotachi's page (bentotachi/) that aren't plain
# copies of the app's SVGs: the link-preview card (og-card.png, 1200x630:
# Ben, the title and the tagline) and the phone home-screen icon
# (apple-touch-icon.png, 180x180: Ben on the page background).
#
#   python branding/make_bentotachi_page.py [path to the Bentotachi repo]
#
# The Bentotachi repo defaults to C:\Projects\TheKoiPond\bentotachi. Rerun
# this when Ben, the title or Bentotachi's colours change (copy the SVGs into
# bentotachi/ first; see the Bentotachi repo's branding/README.md). It needs
# Pillow, Inkscape 1.4 at the path below, and Segoe UI Italic (Windows).
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

INKSCAPE = r"C:\Program Files\Inkscape\bin\inkscape.com"
SITE = Path(__file__).resolve().parents[1]
OUT = SITE / "bentotachi"
BENTO = Path(sys.argv[1] if len(sys.argv) > 1 else r"C:\Projects\TheKoiPond\bentotachi")
ASSETS = BENTO / "web" / "src" / "assets"
ITALIC = r"C:\Windows\Fonts\segoeuii.ttf"

# Bentotachi's light colours (its docs/VISION.md): tea-rice and its text.
BG = "#f3f6f4"
TEXT = "#2b2420"


def render(svg, width):
    """The SVG at the given width, see-through around it, cropped to its art."""
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "art.png"
        subprocess.run([INKSCAPE, str(svg), "--export-type=png", f"--export-filename={out}",
                        f"--export-width={width}", "--export-background-opacity=0"],
                       check=True, capture_output=True)
        image = Image.open(out).convert("RGBA")
        return image.crop(image.getbbox())


def fit(image, width):
    return image.resize((width, round(image.height * width / image.width)), Image.LANCZOS)


# Link-preview card: Ben, the title under him, then the tagline, letter-spaced.
card = Image.new("RGBA", (1200, 630), BG)
ben = fit(render(ASSETS / "onigiri.svg", 1200), 300)
card.alpha_composite(ben, ((1200 - ben.width) // 2, 80))
title = fit(render(ASSETS / "bentotachi-title.svg", 2400), 640)
card.alpha_composite(title, ((1200 - title.width) // 2, 320))

# The tagline as a plain sentence (Bentotachi's VISION.md, 2026-11-04: no
# letter-spaced capitals with dots between them).
draw = ImageDraw.Draw(card)
font = ImageFont.truetype(ITALIC, 36)
text = "Because dinner insists on happening every day."
draw.text(((1200 - draw.textlength(text, font=font)) / 2, 516), text, font=font, fill=TEXT)
card.convert("RGB").save(OUT / "og-card.png", optimize=True)

# Phone home screens need a solid square: Ben on the page background.
touch = Image.new("RGBA", (180, 180), BG)
small = fit(render(ASSETS / "onigiri.svg", 720), 150)
touch.alpha_composite(small, ((180 - small.width) // 2, (180 - small.height) // 2))
touch.convert("RGB").save(OUT / "apple-touch-icon.png", optimize=True)
print("wrote bentotachi/og-card.png and bentotachi/apple-touch-icon.png")
