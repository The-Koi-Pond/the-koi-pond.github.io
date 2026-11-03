# thekoipond.dev

The Koi Pond's home page, served by GitHub Pages at
[thekoipond.dev](https://thekoipond.dev). Each app's page is a folder
here: [thekoipond.dev/bentotachi](https://thekoipond.dev/bentotachi/) is
`bentotachi/` (moved from the `bentotachi` repository on 2026-11-03), and
[thekoipond.dev/de-koi](https://thekoipond.dev/de-koi/) is `de-koi/`.
Bentotachi's pictures there come from the scripts in the `bentotachi`
repository (its `branding/README.md`).

`bento/` keeps Bentotachi's old address working: it was thekoipond.dev/bento
until the repository was renamed (2026-11-02), so these pages send old links
on to /bentotachi/, and the Search Console ownership file is kept there too.
Only served because no repository is called `bento` any more.

`CNAME` holds the domain; the DNS records for it are at Cloudflare.

Bentotachi's tester signup (`bentotachi/join/`) and testers' page
(`bentotachi/testers/`) send their forms to a small Cloudflare Worker at
api.thekoipond.dev; its code and commands are in
`workers/bentotachi-testers/`.

`deki.svg` is Deki, The Koi Pond's mascot, traced from `branding/Deki.png`
(Xel's, made with ChatGPT):

```
python branding/make_svg_deki.py branding/Deki.png .
```

It needs Python with Pillow, numpy and scipy, and Inkscape 1.4. It leaves
out the picture's shadow, body shading and curl gloss, so Deki stays crisp
when small.

`deki-steady.svg` is the same Deki, gently squishing nonstop (the home
page's big Deki):

```
python branding/make_deki_steady.py deki.svg .
```

`thekoipond-title.svg` (brown letters) and `thekoipond-title-dark.svg`
(cream letters, for dark mode) are the drawn name, traced from
`branding/TheKoiPond.png`:

```
python branding/make_svg_wordmark.py branding/TheKoiPond.png .
```

Colours, shared with Bentotachi: letters #361F17 (dark mode #F1EBE5), jade
#5A9A8A for the curl and ripple, cream background #FAF6F1.

`de-koi/` is De-Koi's page. Its pictures (the icon, the screenshots, the phone icon and the
link-preview card) come from the De-Koi repository:

```
python branding/make_de_koi_page.py C:\Projects\TheKoiPond\De-Koi\De-Koi
```

It needs Pillow and Inkscape 1.4, and the De-Koi checkout must have the
new icon (`branding/de-koi-icon/de-koi-icon.svg`).
