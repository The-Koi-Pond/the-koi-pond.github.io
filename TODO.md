# To do

Open, optional improvements for thekoipond.dev, from a site review on
2026-11-01 (everything else from that review was fixed in 50e20ee). Not
published on the website (`_config.yml` excludes this file).

Nothing open right now.

## Decided against (for now)

These came up in the same review and were skipped on purpose in 50e20ee.
Kept here so nobody redoes them by accident; revisit only if the reason
stops holding.

- **The card's border is faint.** It's 1.25:1 against the page in light
  mode (`#e6ddd3` on `#faf6f1`) and 1.62:1 in dark mode (`#34403e` on
  `#141b1b`), under the 3:1 guideline for outlines of clickable things.
  Skipped because the card is already clear from its white fill, its
  heading and the orange "Visit →".
- **The traced SVGs could be about half the size** (`deki.svg` 37 KB, the
  wordmarks, `onigiri.svg` and `ben-scream.svg` 25-26 KB each), by rounding
  coordinates in the tracing scripts. Skipped because re-tracing risks
  bringing back the old rim problems, and the page is already fast.
