# Makes the pictures for De-Koi's page (de-koi/) from the De-Koi repo:
# the icon, the screenshots (as smaller WebP files), the phone home-screen
# icon and the link-preview card.
#
#   python branding/make_de_koi_page.py [path to the De-Koi repo]
#
# The De-Koi repo defaults to C:\Projects\TheKoiPond\De-Koi\De-Koi. Rerun this
# when De-Koi's icon or README screenshots change. It needs Pillow and
# Inkscape 1.4 at the path below.
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

INKSCAPE = r"C:\Program Files\Inkscape\bin\inkscape.com"
SITE = Path(__file__).resolve().parents[1]
OUT = SITE / "de-koi"
DE_KOI = Path(sys.argv[1] if len(sys.argv) > 1 else r"C:\Projects\TheKoiPond\De-Koi\De-Koi")
ICON = DE_KOI / "branding" / "de-koi-icon" / "de-koi-icon.svg"
SHOTS = DE_KOI / "docs" / "screenshots" / "readme"

# The page's light colours (branding/BRAND.md, since 2026-11-04): tea-rice,
# ink, koi vermilion (De-Koi's Pond theme). Cream is what De-Koi's own app
# icons sit on.
RICE_PAPER = "#f3f6f4"
INK = "#1a2a2e"
LACQUER = "#b8341c"
CREAM = "#fef6ed"

OUT.mkdir(exist_ok=True)
shutil.copyfile(ICON, OUT / "de-koi.svg")

# Screenshots: WebP is about a third of the size at the same look. Kept
# 1440px wide, sharp on high-density screens at the page's 680px column.
for name in ["conversation.png", "roleplay.jpg", "fanfic-request.png", "fanfic-reader.png", "phone.jpg"]:
    picture = Image.open(SHOTS / name).convert("RGB")
    picture.save(OUT / (Path(name).stem + ".webp"), quality=82, method=6)
    print(f"{name}: {picture.width}x{picture.height}")


def render(size):
    """The icon at size x size pixels, see-through around it (light version)."""
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "icon.png"
        subprocess.run(
            [INKSCAPE, str(ICON), "--export-type=png", f"--export-filename={out}",
             f"--export-width={size}", f"--export-height={size}", "--export-background-opacity=0"],
            check=True, capture_output=True,
        )
        return Image.open(out).convert("RGBA")


# Phone home screens need a solid square: the icon on cream, like De-Koi's
# own app icons.
touch = Image.new("RGBA", (180, 180), CREAM)
touch.alpha_composite(render(144), (18, 18))
touch.convert("RGB").save(OUT / "apple-touch-icon.png")

# The link-preview card (1200x630, PNG because preview services don't take
# SVG): the icon, the name in Pond Pebbles and the tagline, like Bentotachi's.
card = Image.new("RGBA", (1200, 630), RICE_PAPER)
card.alpha_composite(render(260), (470, 44))
draw = ImageDraw.Draw(card)


def centred(y, text, font, colour, spacing=0):
    """Text centred across the card, with extra space between letters."""
    widths = [draw.textlength(ch, font=font) for ch in text]
    x = (card.width - sum(widths) - spacing * (len(text) - 1)) / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=colour)
        x += w + spacing


centred(312, "De-Koi", ImageFont.truetype(str(SITE / "font" / "PondPebbles.otf"), 170), INK)
centred(522, "CHAT • ROLEPLAY • FANFIC • ANY MODEL", ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 34),
        LACQUER, spacing=4)
card.convert("RGB").save(OUT / "og-card.png")
print("wrote", ", ".join(sorted(p.name for p in OUT.iterdir())))
