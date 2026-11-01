# thekoipond.dev

The Koi Pond's home page, served by GitHub Pages at
[thekoipond.dev](https://thekoipond.dev). Project sites show up under it
automatically, like [thekoipond.dev/bentotachi](https://thekoipond.dev/bentotachi) from
the `bentotachi` repository.

`bento/` keeps Bentotachi's old address working: it was thekoipond.dev/bento
until the repository was renamed (2026-11-02), so these pages send old links
on to /bentotachi/, and the Search Console ownership file is kept there too.
Only served because no repository is called `bento` any more.

`CNAME` holds the domain; the DNS records for it are at Cloudflare.

`deki.svg` is Deki, The Koi Pond's mascot, traced from `branding/Deki.png`
(Xel's, made with ChatGPT):

```
python branding/make_svg_deki.py branding/Deki.png .
```

It needs Python with Pillow, numpy and scipy, and Inkscape 1.4. It leaves
out the picture's shadow, body shading and curl gloss, so Deki stays crisp
when small.

`thekoipond-title.svg` (brown letters) and `thekoipond-title-dark.svg`
(cream letters, for dark mode) are the drawn name, traced from
`branding/TheKoiPond.png`:

```
python branding/make_svg_wordmark.py branding/TheKoiPond.png .
```

Colours, shared with Bentotachi: letters #361F17 (dark mode #F1EBE5), jade
#5A9A8A for the curl and ripple, cream background #FAF6F1.
