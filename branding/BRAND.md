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

The palette is Deki's: a cream body, koi-orange spots, jade fins and a
brown outline. There are two moods. **Daytime** is light mode and
**pond at night** is dark mode. (Koihongo's "Night Water" theme is a
different, colder set of colours; see its row below.)

| Name | Used for | Light | Dark |
|---|---|---|---|
| Rice / Pond at night | Page background | `#FAF6F1` | `#141B1B` |
| Paper | Cards, sheets, panels | `#FFFFFF` | `#202928` |
| Ink | Main text | `#2B2420` | `#F1EBE5` |
| Mist | Quieter text (hints, dates, captions) | `#7A6D64` | `#A89A8F` |
| Line | Borders and dividers | `#E6DDD3` | `#34403E` |
| Koi orange | Main buttons, links, the selected thing | `#B4532A` | `#E07A4F` |
| Jade | A second colour for calmer highlights | `#3F7668` | `#7FBFAE` |
| Danger | Errors, delete buttons | `#B3261E` | `#F2827A` |

These are the colours Bentotachi and thekoipond.dev already use. In light
mode, put white text on koi-orange buttons. In dark mode, put the dark
background colour on them.

Colours for drawings (logos, mascots) are a little different, because
art doesn't have to work as text:

| Name | Colour | Where |
|---|---|---|
| Art ink (outlines, drawn letters) | `#361F17`, or `#F1EBE5` on dark | Logos and titles |
| Ben's ink | `#2E201B` | Ben's outline and nori (`onigiri.svg` and his moods) |
| Art orange | `#C8643A` | Ben's chopsticks |
| Art jade | `#5A9A8A` | The ripple, the curl in "Koi" |
| Deki's cream / blush / spots | `#FEF6ED` / `#FED7CA` / `#FD9E82` | `deki.svg` |
| Deki's jade (light, shade) / outline | `#A1CDC1`, `#7FB3A8` / `#623A2D` | `deki.svg` |

### Readability

Checked on 2026-11-01. The usual minimum for normal-size text is 4.5:1.

| Text | On | Ratio |
|---|---|---|
| Ink `#2B2420` | Rice `#FAF6F1` | 14.2 |
| Mist `#7A6D64` | Rice | 4.65 |
| Koi orange `#B4532A` | Rice | 4.63 |
| White | Koi orange `#B4532A` | 4.99 |
| Jade `#3F7668` | Rice | 4.88 |
| Ink `#F1EBE5` | Pond at night `#141B1B` | 14.8 |
| Mist `#A89A8F` | Pond at night | 6.39 |
| Koi orange `#E07A4F` | Pond at night | 5.88 |
| Jade `#7FBFAE` | Pond at night | 8.29 |
| Ink `#F1EBE5` | Dark Paper `#202928` | 12.6 |
| Mist `#A89A8F` | Dark Paper | 5.45 |
| Koi orange `#E07A4F` | Dark Paper | 5.01 |
| Pond-at-night text `#141B1B` | Dark-mode orange button `#E07A4F` | 5.88 |

Light Mist and light koi orange are only just over the line. Don't make
them any lighter.

### Colour rules

- **Orange is earned.** Use koi orange for actions, the selected thing
  and moments that matter. Don't fill whole panels with it. The pond
  should breathe. (This rule comes from De-Koi.)
- **Danger isn't orange.** The accent is already orange, so errors and
  delete buttons use Danger red (table above), plus an icon or words.
  It's 6.07 on Rice, 6.54 under white button text, and 6.86 on pond at
  night in dark mode (Bentotachi's values).
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
| Orange tint | Behind selected and highlighted things | `#302A25` (orange text on it: 4.76) |
| Jade tint | Calm notes, "good" boxes | `#1D3330` |

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
is close to it. It has real reasons (Deki's cream body and koi spots,
Bentotachi's rice), but the apps shouldn't drift further towards it:

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
  and as Deki-senpai in Koihongo.
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
| Bentotachi | Ben, the screaming onigiri on chopsticks, and his moods; the drawn title with the umeboshi | Uses the pond colours; dark mode is pond at night (since 2026-11-01). Pill-shaped buttons and chips. "A Koi Pond app" credit at the bottom of its ⋮ menu. |
| Koihongo | Pixel art, sparkles, pixel fonts, Deki-senpai | Navy, periwinkle and pink for now. Getting three themes to choose from: "That tasted purple!" (today's look), **Night Water** (cold teal-black pond, moonlit) and **Lantern Dusk** (warm dusk with paper lanterns, built on the pond-at-night colours). |
| De-Koi | Visual-novel atmosphere, sprites, the "Koi Pond at Dusk" look | Already close: ember orange `#F06F3F`, lotus teal, parchment text. Its own rules are in its `DESIGN.md`. |
| DeKoi | The fish ring, sumi-e brush motifs, serif titles | Shelved. Its `DESIGN.md` is the most detailed design writing we have, and worth borrowing from. |

## Where things live

All paths are under `C:\Projects\TheKoiPond\` on Xel's PC.

- Deki, the studio logo and Pond Pebbles: `the-koi-pond.github.io\`
  (see its `README.md` for how they're made).
- Ben, the Bentotachi title and app icons: `bento\branding\` (see its
  `README.md`).
- The fish ring: DeKoi, path above.

## Still to decide

1. **Koihongo's two pond themes:** the exact colours, tuned in the real
   app. Decided on 2026-11-01: Night Water and Lantern Dusk, both kept
   as options next to "That tasted purple!". The hills and bushes get
   recoloured; the blossoms stay as they are.
2. **Pixel koi for the fish ring:** Xel draws them (left- and
   right-facing at least; more directions if the ring goes all the way
   round).
