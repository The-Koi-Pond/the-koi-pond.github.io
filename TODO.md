# To do

Open, optional improvements for thekoipond.dev, from a site review on
2026-11-01 (everything else from that review was fixed in f5dd162). Not
published on the website (`_config.yml` excludes this file).

## The app card's link text is long

- **Where:** `index.html`, the `<a class="project">` card.
- **What:** the whole card is one link, so a screen reader reads the full
  description as the link's name ("Bentotachi A recipe box, meal plan, ...
  Visit"). "Bentotachi" is already a heading, so jumping by headings works.
- **When it matters:** once there are several app cards, listing the page's
  links gets long and samey.
- **Fix:** keep the link's name to the heading (`aria-labelledby` pointing
  at the `<h2>`, with `aria-describedby` for the description), or make only
  "Visit Bentotachi" the link.

## The card's border is very faint

- **Where:** `index.html`, `.project` uses `border: 1px solid var(--border)`.
- **What:** the border is 1.25:1 against the page in light mode (`#e6ddd3`
  on `#faf6f1`) and 1.62:1 in dark mode (`#34403e` on `#141b1b`). The
  accessibility guideline for outlines of clickable things is 3:1.
- **Why it's minor:** the white card fill and the orange "Visit →" already
  say "this is clickable".
- **Fix:** a darker border for the card only, or a light resting shadow.
  Check `branding/BRAND.md`'s Line colour before changing the shared
  `--border`, since the footer's line uses it too.

## The traced SVGs could be about half the size

- **Where:** `deki.svg` (37 KB), `ben-scream.svg` (26 KB), `onigiri.svg`
  (26 KB), `thekoipond-title.svg` and `-dark.svg` (25 KB each).
- **What:** the traced paths keep 4 to 5 decimal places (like `-26.86189`),
  far more than a 110px picture needs.
- **Why it's low value:** the page is already fast, and GitHub compresses
  text files.
- **Fix:** round coordinates to 1 decimal place in the tracing scripts
  (`branding/make_svg_*.py`, and Bentotachi's for Ben), then re-trace, so
  the saving survives future re-traces.
