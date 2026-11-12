# How The Koi Pond's apps look

This is the shared look for The Koi Pond's apps and website. It isn't a
strict design system. Each app keeps its own personality. This page says
which parts the apps share, so they look like they come from the same place.

Read it before changing an app's colours, fonts, logo or mascot. If an
app's own design notes disagree with this page, raise it rather than
quietly picking one.

## The idea: calm water, silly fish

- **Calm water** is what the apps share: backgrounds, cards, buttons,
  borders, spacing and how things move. Keep it quiet, readable and
  polished. It's what makes the apps look related.
- **Silly fish** is what each app keeps for itself: its mascot, empty and
  loading screens, the wording on buttons and messages, and one signature
  thing of its own. This is where the jokes go.

A screaming onigiri is welcome. A screaming settings page isn't.

## The pond colours

The palette comes from Deki (jade fins, koi spots) and the water. There
are two moods. **Daytime** is light mode and **pond at night** is dark
mode. (Koihongo's "Night Water" theme is a different, colder set of
colours; see its row below.)

| Name | Used for | Light | Dark |
|---|---|---|---|
| Tea-rice / Pond at night | Page background | `#F3F6F4` | `#141B1B` |
| Paper | Cards, sheets, panels | `#FFFFFF` | `#202928` |
| Ink | Main text | `#2B2420` | `#F1EBE5` |
| Mist | Quieter text (hints, dates, captions) | `#5F6B67` | `#A9B3AE` |
| Line | Borders and dividers | `#D8DDDB` | `#34403E` |
| Koi vermilion | Main buttons, links, the selected thing | `#B8341C` | `#F7694A` |
| Jade | A second colour for calmer highlights | `#3F7668` | `#7FBFAE` |
| Danger (crimson) | Errors, delete buttons | `#B0213A` | `#FF6470` |

**Changed on 2026-11-04.** Until then the daytime palette was a cream
background (`#FAF6F1`) with a clay "koi orange" (`#B4532A`, dark
`#E07A4F`), which is the look people now recognise as AI-made (see "Our
own look, not the default one" below and
`C:\Projects\TheKoiPond\AI-DESIGN-TELLS.md`). The background became a
near-white with a hint of jade, and the orange a clearer, redder vermilion,
like a red koi. Chosen side by side in
`C:\Projects\TheKoiPond\AI-DESIGN-TELLS-colours.html`.

Who uses what: thekoipond.dev and De-Koi's Pond theme use vermilion
(De-Koi's danger crimson came from there). **Bentotachi has its own
accent**: umeboshi plum (`#A82D4A`, dark `#EE7D92`) on the same tea-rice,
with its own danger colours, because the plum is its title's filling; its
exact colours are in its `docs/VISION.md`.

**De-Koi has its own, tealer night** (Xel's pick, 2026-11-04). On a chat
app's big dark screens `#141B1B` read as grey, so De-Koi's Pond theme uses
a deeper teal at the same steps: background `#041719`, paper `#112527`,
line `#233B3E` (plus `#001012` for its sidebars). Its daytime colours are
the ones above. Exact values and contrasts are in De-Koi's `DESIGN.md`,
section 7.

In light mode, put white text on vermilion buttons. In dark mode, put the
dark background colour on them.

Colours for drawings (logos, mascots) are a little different, because
art doesn't have to work as text:

| Name | Colour | Where |
|---|---|---|
| Art ink (outlines, drawn letters) | `#361F17`, or `#F1EBE5` on dark | Logos and titles |
| Ben's ink | `#2E201B` | Ben's outline and nori (`onigiri.svg` and his moods) |
| Chopstick wood | `#A87A43` (shine `#D4B07C`) | Ben's chopsticks and the Bentotachi title's underline (orange `#C8643A` until 2026-11-04) |
| Art jade | `#5A9A8A` | The ripple, the curl in "Koi" |
| Deki's cream / blush / spots | `#FEF6ED` / `#FED7CA` / `#FD9E82` | `deki.svg` |
| Deki's jade (light, shade) / outline | `#A1CDC1`, `#7FB3A8` / `#623A2D` | `deki.svg` |

### Readability

Checked on 2026-11-04. The usual minimum for normal-size text is 4.5:1.

| Text | On | Ratio |
|---|---|---|
| Ink `#2B2420` | Tea-rice `#F3F6F4` | 14.0 |
| Mist `#5F6B67` | Tea-rice | 5.10 |
| Koi vermilion `#B8341C` | Tea-rice | 5.44 |
| White | Koi vermilion `#B8341C` | 5.92 |
| Jade `#3F7668` | Tea-rice | 4.82 |
| Danger `#B0213A` | Tea-rice | 6.18 |
| White | Danger `#B0213A` | 6.72 |
| Ink `#F1EBE5` | Pond at night `#141B1B` | 14.8 |
| Mist `#A9B3AE` | Pond at night | 8.11 |
| Koi vermilion `#F7694A` | Pond at night | 5.88 |
| Jade `#7FBFAE` | Pond at night | 8.29 |
| Danger `#FF6470` | Pond at night | 6.08 |
| Ink `#F1EBE5` | Dark Paper `#202928` | 12.6 |
| Mist `#A9B3AE` | Dark Paper | 6.92 |
| Koi vermilion `#F7694A` | Dark Paper | 5.02 |
| Danger `#FF6470` | Dark Paper | 5.19 |
| Pond-at-night text `#141B1B` | Dark-mode vermilion button `#F7694A` | 5.88 |
| Pond-at-night text `#141B1B` | Dark-mode danger button `#FF6470` | 6.08 |

Jade on tea-rice and dark vermilion on Dark Paper are the closest to the
line. Don't make them any lighter.

### Colour rules

- **Vermilion is earned.** Use it for actions, the selected thing and
  moments that matter. Don't fill whole panels with it. The pond should
  breathe. (This rule comes from De-Koi.)
- **Danger isn't the accent.** Errors and delete buttons use crimson
  (table above), plus an icon or words. Vermilion and the old danger red
  were nearly the same colour in light mode, so danger moved towards pink
  (hue 350–355°), while vermilion leans orange. An app whose accent is
  pink or plum (Bentotachi) keeps a redder or more orange danger instead.
- **Apps may add colours for meaning.** An app can have its own colours
  for its own categories, like Koihongo's kana, component, kanji and word
  colours. Text on them must still reach 4.5:1, and they shouldn't be
  orange or red, so they don't get mixed up with actions or danger. The
  exception is warnings: a level that really is a warning may use red or
  amber, always with words (Bentotachi's pantry shows "1 out" in red and
  "1 low" in amber).
- **Colour is never the only signal.** Pair it with a label, an icon or a
  shape, for colour-blind people.

### Pond at night (decided 2026-11-01)

Dark mode is the pond at night: a teal-tinted near-black, `#141B1B`.
Bentotachi, its website and thekoipond.dev all use it. It replaced a warm
stone, `#1C1917`, which is just as bright, so every contrast ratio stayed
the same. It also moves the dark mode away from the warm-cream-and-
terracotta look AI tools tend to produce by default (see "Our own look,
not the default one" below). De-Koi's own near-black teal, `#05090D`, is
the same idea, only darker.

The soft tints behind highlighted things are tinted to match:

| Name | Used for | Dark |
|---|---|---|
| Vermilion tint | Behind selected and highlighted things | `#2D2D2A` (vermilion text on it: 4.65; anything warmer drops below 4.5) |
| Jade tint | Calm notes, "good" boxes | `#1D3330` |

In light mode the vermilion tint is `#F8EBE8` (vermilion text on it: 5.09)
and the jade tint `#E2EFEB`.

Text that sits on a coloured button or badge in dark mode is the pond-
at-night colour, `#141B1B`.

## Type

- **Pond Pebbles** is The Koi Pond's own font (`font/`, made by
  `font/make_font.py`). It's for the studio name, app names and big
  titles only, which includes a website's section headings (the
  Bentotachi site uses it for those). Never use it for body text.
- **Body text** uses a plain, readable font. The website uses the
  system's own font (Segoe UI on Windows, Roboto on Android).
- Each app may have **one display font of its own** for its personality:
  Koihongo's pixel fonts, DeKoi's Shippori Mincho serif, or Bentotachi's
  drawn title.

## Shape and motion

- **Corners:** 12px for cards and panels, 4 to 8px for small controls,
  fully round for icon-only buttons. An app may make its buttons, chips
  and tags fully round pills instead (Bentotachi does, everywhere), as
  long as it does so consistently. Pixel-art apps like Koihongo may use
  their own corners (a pill-shaped Start button, rounder banners).
- **Motion behaves like water:** drift, ripple, glide. Something you can
  click may lift 2px when you point at it. No bouncing, spinning or
  flashing.
- **Reduced motion:** when the device asks for less motion, everything
  holds still. A still version should still look designed, not just
  paused.

## Pixel art on dark backgrounds

Koihongo is pixel art on a dark page, so "calm water" means something a
little different there:

- **Glows are soft and few.** A glow marks something special (the Start
  button, a level-up), not every panel. Keep it close to its edge.
- **Shadows are hard blocks**, offset in whole pixels, never blurry.
- **Dithering** (a checkerboard of two colours) is how pixel art blends
  between colours. Use it in scenery, not behind text.
- **Text sits on solid colour**, never straight on scenery or stars.
- **Sizes follow the pixel grid.** Pixel fonts drawn on an 8px grid use
  sizes in multiples of 8.

## Our own look, not the default one

Warm cream backgrounds, a terracotta accent and serif headings are the
look AI tools fall back on when nobody steers them. Our daytime palette
was close to it until 2026-11-04, when the cream became tea-rice and the
clay orange became vermilion (and plum for Bentotachi). Don't drift back
towards it; `C:\Projects\TheKoiPond\AI-DESIGN-TELLS.md` lists the other
tells to avoid:

- **What makes the apps related is the motifs:** Deki, the ripple, the
  fish ring, Pond Pebbles and the "A Koi Pond app" credit. They don't
  have to share page colours. Koihongo keeps its own palette.
- **Lean on the specific things:** each app's mascot, drawn lettering and
  signature details. They say more about who made the app than any
  background colour does.
- **Bentotachi never gets serif headings.** Its type is the drawn title,
  Pond Pebbles and the system font.
- **Jade can do more than it does now,** so the palette reads as "koi
  pond", not just "warm".

## Shared motifs

- **Deki** (`deki.svg`, traced from `branding/Deki.png`) is The Koi
  Pond's mascot. It appears on the website, on each app's About screen,
  and as Deki-senpai in Koihongo and De-Koi. Deki is a genderless mythical
  mer-koi: write about them as "they". Asked what gender they are,
  Deki says: "I am a fish."
- **The ripple** is the wavy jade line under "The Koi Pond" in the logo.
  Use it as a divider, or as a gentle loading motif.
- **The fish ring** is a few koi swimming slow circles around a centre,
  with still rings and the odd ripple. The original is DeKoi's home
  screen (`DeKoi\DeKoi\src\features\shell\pond\hero\PondEye.tsx` and
  `PondEye.css`, written by Xel, plain CSS and SVG with no libraries).
  Rules: at most one per app, on a home or welcome screen, never as a
  spinner or button. Orbits take tens of seconds. Three to six koi in koi
  orange, jade, amber, or classic white with orange spots (which stand
  out best on dark water). With reduced motion, the koi stop in a composed
  arrangement. In a pixel-art app, the koi are pixel sprites.
- **"A Koi Pond app"** with a small Deki, linking to thekoipond.dev,
  goes in each app's About screen or footer.

## Each app's silly fish

| App | Its own personality | Where it stands |
|---|---|---|
| Bentotachi | Ben, the screaming onigiri on chopsticks, and his moods; the drawn title with the umeboshi | Its own accent since 2026-11-04: umeboshi plum on a "tea-rice" background, and Ben's chopsticks became plain wood; dark mode is pond at night (since 2026-11-01). Pill-shaped buttons and chips. "A Koi Pond app" credit at the bottom of its ⋮ menu. |
| Koihongo | Pixel art, sparkles, pixel fonts, Deki-senpai | Three themes to choose from in Settings (since 2026-11-01): "That tasted purple!" (the original navy, periwinkle and pink), **Night Water** (cold teal-black pond, moonlit) and **Lantern Dusk** (warm dusk with paper lanterns, built on the pond-at-night colours). |
| De-Koi | Visual-novel atmosphere, sprites, the "Koi Pond at Dusk" look | Its new Pond theme uses the pond colours: vermilion `#F7694A` / `#B8341C`, crimson danger, one teal hue for the water (De-Koi PR #1591). The older Default theme keeps ember orange `#F06F3F`. Its own rules are in its `DESIGN.md`. |
| DeKoi | The fish ring, sumi-e brush motifs, serif titles | Shelved. Its `DESIGN.md` is the most detailed design writing we have, and worth borrowing from. |

## Where things live

All paths are under `C:\Projects\TheKoiPond\` on Xel's PC.

- Deki, the studio logo and Pond Pebbles: `the-koi-pond.github.io\`
  (see its `README.md` for how they're made).
- Ben, the Bentotachi title and app icons: `bentotachi\branding\` (see its
  `README.md`).
- The fish ring: DeKoi, path above.

## Still to decide

- **Pixel koi for the fish ring:** Xel makes the art with AI tools such
  as PixelLab and ChatGPT, rather than drawing it by hand, so don't ask
  Xel to draw the koi. Until there are sprites, use simple placeholders
  made in code. Needed: left- and right-facing at least, plus more
  directions if the ring goes all the way round.

(Koihongo's two pond themes were settled here too. Night Water and
Lantern Dusk shipped on 2026-11-01, next to "That tasted purple!".)
