# thekoipond.dev (The Koi Pond's home page)

The studio home page for The Koi Pond: one hand-written HTML page that
introduces the studio and links to its apps. Right now it has two app
cards: Bentotachi, at `/bentotachi/`, and De-Koi, at `/de-koi/`. Each
app's page is a folder in this repo.

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
- **Every app's page lives here, in a folder named after its address**
  (`bentotachi/`, `de-koi/`), not in the app's own repo. Bentotachi's page
  moved here from the `bentotachi` repo's `site/` folder on 2026-11-03, for
  consistency. Its address didn't change.
- Never turn on GitHub Pages in an app's own repo: a repo with Pages on
  takes over the address with its name (`thekoipond.dev/<repo>/`) and
  hides the folder here.
- `bentotachi/privacy.html` is Bentotachi's privacy policy, linked from
  Google Play: keep its address. When the app starts doing something new
  with people's data, its policy changes here, in a separate commit from
  the app's. Never delete `bentotachi/google11869a0aeef0ff1c.html` (or its
  copy in `bento/`): it's the Search Console ownership check, and Google
  re-checks it.
- The `bento/` folder only redirects Bentotachi's old address (see
  `README.md`).
- **The one exception to "no JavaScript, nothing stored":** Bentotachi's
  tester pages, `bentotachi/join/` (signup) and `bentotachi/testers/` (next
  steps and feedback), post their forms to a Cloudflare Worker at
  `api.thekoipond.dev`. Its code is `workers/bentotachi-testers/` (its
  `README.md` has the commands and how to test it); it saves to a D1
  database in Xel's Cloudflare account, and Xel reads the lists at
  `api.thekoipond.dev/bentotachi/admin` with a password. The pages still
  have no JavaScript: the Worker sends people back to `#welcome`,
  `#thanks` or `#oops`, and CSS `:target` shows the right note. Deploying
  the Worker (`npx wrangler@4 deploy`) publishes, like a push: Xel's
  go-ahead first. No emails or IP addresses are collected, on purpose.

## Preview locally

From this folder:

```
python -m http.server 8000
```

Then open http://localhost:8000/. Check dark mode by switching the
OS or browser theme (the page uses `prefers-color-scheme`). Test in Firefox
too: it's Xel's browser.

## Where things are

- `index.html`: the whole page (HTML and CSS).
- `404.html`: the page GitHub shows for any address that doesn't exist (with
  screaming Ben). Every link and file in it starts with `/`, because it's
  served at whatever address was missing.
- `deki.svg`: Deki, the mascot. `favicon.ico` and `apple-touch-icon.png` are
  Deki for old browsers and phone home screens.
- `deki-steady.svg`: Deki gently squishing nonstop, made from `deki.svg` by
  `branding/make_deki_steady.py` (rerun it if `deki.svg` changes). The home
  page shows it in a `<picture>` that swaps in the still `deki.svg` for
  people with reduced motion turned on, because Firefox ignores the SVG's
  own reduced-motion rule inside an `<img>`. It has a little room around
  Deki to squish into, so it's shown 116px wide (the still one 110px) for
  Deki to look the same size.
- `thekoipond-title.svg` / `thekoipond-title-dark.svg`: the drawn studio
  name, light and dark versions, swapped with `<picture>`.
- `onigiri.svg` (Ben, on the app card) and `ben-scream.svg` (the 404 page):
  copies of Bentotachi's art, made by the scripts in the `bentotachi` repo.
- `de-koi/`: De-Koi's page. `index.html` holds its HTML and CSS, in
  De-Koi's own colours (from De-Koi's `DESIGN.md`), with Deki-senpai
  telling you about the app in chat bubbles. Its pictures (`de-koi.svg`,
  the `.webp` screenshots, `apple-touch-icon.png`, `og-card.png`) are made by
  `branding/make_de_koi_page.py` from the De-Koi repo's icon
  (`branding/de-koi-icon/`) and README screenshots: rerun it when those
  change, don't edit them by hand. The home page's De-Koi card uses
  `de-koi/de-koi.svg` too. The page's facts (platforms, features, the
  Marinara Engine notice) come from De-Koi's `README.md`; check them against
  it when De-Koi changes.
- `og-card.png`: the 1200x630 picture link previews show (Bluesky, Discord,
  messages). Preview services don't accept SVG, so it's a PNG.
- `robots.txt` and `sitemap.xml`: for search engines. **Add each new app
  page to `sitemap.xml`.**
- `font/`: Pond Pebbles, the studio's own display font. `PondPebbles.woff2`
  is what the page loads; `.otf` is the download for desktop use (both are
  published); `make_font.py` rebuilds both from the drawn sheets in
  `font/sheets/`.
- `branding/`: source PNGs, the SVG tracing scripts, `make_de_koi_page.py`
  and `BRAND.md`.
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
