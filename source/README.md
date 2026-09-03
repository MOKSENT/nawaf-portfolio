# source/ — how this site is built

`index.html` (Arabic) and `en/index.html` (English) at the repo root are **generated
files**, ~6 MB each because every image is inlined as a data URI. Do not hand-edit them.
Edit the light template here and rebuild.

Requirements: Python 3 with Pillow (`pip install pillow`). No network needed.

## Build order

```bash
cd source
python3 build_en.py           # artifact-ar.html          -> artifact-en.html
python3 build_and_inject.py   # both templates + images   -> build/*.build.html
python3 deploy.py             # build/*.build.html        -> ../index.html, ../en/index.html
```

Then commit and push. The repo is connected to Vercel, so a push to `main`
deploys to production automatically (nawaf-alshareif.vercel.app).

The build is deterministic: the same inputs always produce byte-identical output,
so `git diff` after a rebuild shows only what you actually changed.

One exception, once: the two site files currently committed were produced before the
build was made deterministic, so your first rebuild will also show a small diff inside
a few base64 `data:image/svg+xml` strings. Those are the generated placeholder covers
(bar widths in the illustrative artwork) and nothing else. Every real screenshot
reproduces byte-identically. Commit that diff once and it will not come back.

## Files

| file | role |
|---|---|
| `artifact-ar.html` | **the template you edit.** Arabic markup, CSS and JS, with `__TOKEN__` placeholders where images go |
| `build_en.py` | derives the English template: structural swaps (dir, lang, font order), then a longest-key-first Arabic to English string map. Add new strings to the `T` dict |
| `artifact-en.old.html` | reference the EN build reads for the archive list and case data. Do not delete |
| `artifact-en.html` | generated. Overwritten by `build_en.py` |
| `build_and_inject.py` | resolves every `__TOKEN__` to a data URI: real screenshots, generated placeholder covers, portrait, avatar |
| `deploy.py` | wraps a build in doctype/head/body, rewrites the language links to `/` and `/en/`, writes the two site files |
| `prefix_ar.txt`, `prefix_en.txt` | the `<head>` block prepended by `deploy.py`: meta description, theme-color, favicon |
| `assets/work/` | client and product screenshots, already downscaled to the pipeline width (1100 px) so the build re-encodes them without a second resize |
| `assets/siyanah/` | elevator maintenance system screenshots, client identity blurred |
| `assets/img/` | portrait photo, used for both the nav avatar and the About section |
| `build/` | generated intermediates, gitignored |

## Rules that must not be broken

- The elevator maintenance client stays anonymous: no company name, no logo, no staff
  names, no system URL. The screenshots in `assets/siyanah/` are already blurred where
  needed, and all data in them is demo data.
- Never present figures from demo data as real scale, and never call the running cost
  permanently zero. Current wording: "تكلفتها الحالية صفر وتتوسع مع نمو البيانات".
- The word حراج must not appear anywhere on the site.
- Arabic copy follows `my-writing-style`: no word-initial hamza, few commas, no dashes
  or arrows in prose, Latin numerals.
- Every image on the site must open full size in the lightbox. Keep that behaviour when
  adding new galleries.

## Adding a work to the Selected work grid

1. Put the screenshots in `assets/work/`, downscaled to 1100 px wide.
2. Register tokens for them in the `tokens` dict in `build_and_inject.py`
   (`__WORK_PN__` for the card cover, `__G_PN_1__`… for the gallery).
3. Add a `.wcard` button in `artifact-ar.html` inside `.wgrid`, plus the matching
   entry in the `#case-data` block.
4. Add the English strings to the `T` dict in `build_en.py`.
5. Rebuild, check `git diff --stat`, push.
