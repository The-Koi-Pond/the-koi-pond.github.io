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
**night water** is dark mode.

| Name | Used for | Light | Dark |
|---|---|---|---|
| Rice | Page background | `#FAF6F1` | see "Night water" below |
| Paper | Cards, sheets, panels | `#FFFFFF` | `#27221F` |
| Ink | Main text | `#2B2420` | `#F1EBE5` |
| Mist | Quieter text (hints, dates, captions) | `#7A6D64` | `#A89A8F` |
| Line | Borders and dividers | `#E6DDD3` | `#3D3530` |
| Koi orange | Main buttons, links, the selected thing | `#B4532A` | `#E07A4F` |
| Jade | A second colour for calmer highlights | `#3F7668` | `#7FBFAE` |

These are the colours Bentotachi and thekoipond.dev already use. In light
mode, put white text on koi-orange buttons. In dark mode, put the dark
background colour on them.

Colours for drawings (logos, mascots) are a little different, because
art doesn't have to work as text:

| Name | Colour | Where |
|---|---|---|
| Art ink (outlines, drawn letters) | `#361F17`, or `#F1EBE5` on dark | Logos and titles |
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
| Ink `#F1EBE5` | Dark background `#1C1917` | 14.8 |
| Mist `#A89A8F` | `#1C1917` | 6.40 |
| Koi orange `#E07A4F` | `#1C1917` | 5.88 |
| Jade `#7FBFAE` | `#1C1917` | 8.30 |

Light Mist and light koi orange are only just over the line. Don't make
them any lighter.

### Colour rules

- **Orange is earned.** Use koi orange for actions, the selected thing
  and moments that matter. Don't fill whole panels with it. The pond
  should breathe. (This rule comes from De-Koi.)
- **Danger isn't orange.** The accent is already orange, so errors and
  delete buttons need a clearly different red, plus an icon or words.
- **Colour is never the only signal.** Pair it with a label, an icon or a
  shape, for colour-blind people.

### Night water (undecided)

Right now the dark modes don't agree:

- Bentotachi and thekoipond.dev use warm stone, `#1C1917`.
- De-Koi uses near-black pond teal, `#05090D`.

The suggestion is to tint the stone toward teal, so the dark modes read
as the same pond at night. `#141B1B` is about as bright as `#1C1917`, so
every ratio in the table above stays the same: 14.8 for text, 6.39 for
Mist, 5.88 for orange and 8.29 for jade. A matching card colour would be
around `#202928`, where text is 12.6, Mist 5.45 and orange 5.01. These
are candidates. Try them in Bentotachi before deciding.

## Type

- **Pond Pebbles** is The Koi Pond's own font (`font/`, made by
  `font/make_font.py`). It's for the studio name, app names and big
  titles only. Never use it for body text.
- **Body text** uses a plain, readable font. The website uses the
  system's own font (Segoe UI on Windows, Roboto on Android).
- Each app may have **one display font of its own** for its personality:
  Koihongo's pixel fonts, DeKoi's Shippori Mincho serif, or Bentotachi's
  drawn title.

## Shape and motion

- **Corners:** 12px for cards and panels, 4 to 8px for small controls,
  fully round for icon-only buttons.
- **Motion behaves like water:** drift, ripple, glide. Something you can
  click may lift 2px when you point at it. No bouncing, spinning or
  flashing.
- **Reduced motion:** when the device asks for less motion, everything
  holds still. A still version should still look designed, not just
  paused.

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
  orange, jade and amber. With reduced motion, the koi stop in a composed
  arrangement.
- **"A Koi Pond app"** with a small Deki, linking to thekoipond.dev,
  goes in each app's About screen or footer.

## Each app's silly fish

| App | Its own personality | Where it stands |
|---|---|---|
| Bentotachi | Ben, the screaming onigiri on chopsticks, and his moods; the drawn title with the umeboshi | Uses the pond colours. Dark mode may move to night water. |
| Koihongo | Pixel art, sparkles, pixel fonts, Deki-senpai | Navy, periwinkle and pink for now. To be saved as the theme "That tasted purple!", with a pond theme added beside it. |
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

1. **Night water:** whether Bentotachi and the website move their dark
   mode from `#1C1917` to the teal-tinted candidate above.
2. **Koihongo's pond theme:** the colours for a pixel-art "pond at
   night", and whether its scenery art is recoloured or redrawn. Its
   colours are mostly typed straight into the stylesheet (about 285 of
   them), so they need turning into named colour variables before a
   second theme can work.
3. **The fish ring in Koihongo:** DeKoi's koi are smooth drawings, which
   would look out of place next to pixel art. They would need redrawing
   as small pixel sprites.
