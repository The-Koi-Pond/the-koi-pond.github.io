# thekoipond.dev (The Koi Pond's home page)

The studio home page for The Koi Pond: one hand-written HTML page that
introduces the studio and links to its apps. Right now it has two app
cards: Bentotachi, at `/bentotachi/`, and De-Koi, which links to its GitHub
repository (it has no Pages site).

## How it's built and deployed

- No build step, no JavaScript, no package manager. `index.html` holds all
  the HTML and CSS (in a `<style>` block). Edit it directly.
- GitHub Pages serves the `main` branch, root folder, using the "legacy"
  (branch) build: GitHub runs Jekyll over the repo on every push. Jekyll
  turns Markdown files into web pages and publishes every other file.
- `_config.yml` keeps files off the website (they stay in the repo):
  `README.md`, `CLAUDE.md`, `TODO.md`, `branding/`, `font/sheets/` and
  `font/make_font.py`. **Any new file that isn't for visitors goes in its
  `exclude` list**, or it's published. Jekyll also skips names starting with
  `_` or `.`.
- Pushing to `main` publishes the site within a minute or two. Don't push
  without Xel's go-ahead. To see when it's live:
  `gh api repos/The-Koi-Pond/the-koi-pond.github.io/pages/builds/latest --jq .status`
  (`built` means done).
- `CNAME` holds the domain `thekoipond.dev`. DNS is at Cloudflare. HTTPS is
  enforced in the Pages settings; `www.` and `http://` redirect to
  `https://thekoipond.dev/`.
- `/bentotachi/` is not in this repo. It is the `bentotachi` repository's own
  Pages site (`C:\Projects\TheKoiPond\bentotachi\`: its `site/` folder,
  published by its `.github/workflows/pages.yml`), which GitHub mounts under
  this domain. Same for any future app repo with
  Pages turned on. The `bento/` folder *here* only redirects Bentotachi's old
  address (see `README.md`).

## Preview locally

From this folder:

```
python -m http.server 8000
```

Then open http://localhost:8000/. The `/bentotachi/` link will 404 locally,
because that page lives in the other repo. Check dark mode by switching the
OS or browser theme (the page uses `prefers-color-scheme`). Test in Firefox
too: it's Xel's browser.

## Where things are

- `index.html`: the whole page (HTML and CSS).
- `404.html`: the page GitHub shows for any address that doesn't exist (with
  screaming Ben). Every link and file in it starts with `/`, because it's
  served at whatever address was missing.
- `deki.svg`: Deki, the mascot. `favicon.ico` and `apple-touch-icon.png` are
  Deki for old browsers and phone home screens.
- `thekoipond-title.svg` / `thekoipond-title-dark.svg`: the drawn studio
  name, light and dark versions, swapped with `<picture>`.
- `onigiri.svg` (Ben, on the app card) and `ben-scream.svg` (the 404 page):
  copies of Bentotachi's art, made by the scripts in the `bentotachi` repo.
- `de-koi.png` (De-Koi's card): De-Koi's logo (`public/logo.png` in the
  `De-Koi` repo) on a dark round disc in De-Koi's own `#05090D`, because the
  cream koi vanishes on a white card. 176px, shown at 64px.
- `og-card.png`: the 1200x630 picture link previews show (Bluesky, Discord,
  messages). Preview services don't accept SVG, so it's a PNG.
- `robots.txt` and `sitemap.xml`: for search engines. **Add each new app
  page to `sitemap.xml`.**
- `font/`: Pond Pebbles, the studio's own display font. `PondPebbles.woff2`
  is what the page loads; `.otf` is the download for desktop use (both are
  published); `make_font.py` rebuilds both from the drawn sheets in
  `font/sheets/`.
- `branding/`: source PNGs, the SVG tracing scripts, and `BRAND.md`.
- `README.md`: how the SVGs are made, the `bento/` redirect, and the domain.
- `TODO.md`: open, optional improvements, and things decided against. It's
  local only: listed in `.git/info/exclude`, never committed, so it isn't on
  GitHub. (`_config.yml` still excludes it, in case it's ever committed by
  mistake.)

## Conventions

- Read `branding/BRAND.md` before changing colours, fonts, the logo or the
  mascot. It is the shared look for all Koi Pond apps and the website.
- Colours are CSS variables in `:root` at the top of `index.html`, with a
  dark-mode block ("pond at night") under
  `@media (prefers-color-scheme: dark)`. `404.html` repeats the ones it uses.
  Use the variables; don't type new hex values. Light-mode `--muted` and
  `--accent` are only just above the 4.5:1 readable-contrast minimum, so
  never make them lighter.
- Pond Pebbles is for the studio name, app names and big titles only, never
  body text. Body text uses the system font stack.
- Cards: 12px corners (`--radius`). Hover/focus lift is 2px, and is turned
  off under `prefers-reduced-motion`.
- Everything on the page is centred on purpose, and the page fills the
  window (footer at the bottom on tall screens).
- CSS comments explain *why* in plain words. Keep that style.
- Commit messages are plain-English sentences, e.g. "Home page: centred
  footer, Bentotachi in Pond Pebbles".
- Regenerating SVGs or the font needs Python (Pillow, numpy, scipy; the font
  also needs fontTools and brotli) and Inkscape 1.4 at
  `C:\Program Files\Inkscape\bin\inkscape.com` (path hard-coded in the
  scripts). Commands are in `README.md`.

## Gotchas

- Images have `width`/`height` attributes matching each SVG's `viewBox`
  shape, so the layout doesn't jump while loading. If you replace an SVG,
  update those numbers.
- The `h1` has an explicit flex width because Firefox squeezes an
  image-only flex item to nothing (see the CSS comment). Test in Firefox
  after layout changes.
- Decorative images use `alt=""` on purpose (the text next to them says the
  same thing). The wordmark has `alt="The Koi Pond"` because it *is* the
  heading text. Decorative symbols (→, ♡) are wrapped in
  `<span aria-hidden="true">`.
- Each app card is one big link. Keep the default focus outline visible. Its
  `aria-labelledby` points at the card's `<h2>` and `aria-describedby` at
  its text and "Visit" line, so a screen reader names the link after the app
  instead of reading the whole card. A new card needs its own `id`s for
  these.
- The `<footer>` sits outside `<main>` on purpose (screen readers treat it as
  the page footer), with its own width rules to line up with `main`.
- The email address in the footer is public on purpose.
