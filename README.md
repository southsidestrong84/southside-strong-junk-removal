# Southside Strong Junk Removal

Static site for Southside Strong Junk Removal, Chicago Ridge, IL. Preview, not launched: every page carries
`noindex, nofollow` until the owner approves the copy.

**Preview:** https://ogeddiesmith.github.io/southside-strong-junk-removal/

Built by `build.py` into `docs/`, the only folder GitHub Pages publishes (branch main, folder /docs). Do not hand-edit
the HTML; the next build overwrites it.

    python3 build.py

- `content/services.py`: service pages. `content/towns.py`: town pages. `content/facts.py`: state and federal rules, each with its source.
  `content/photos.py`: the business's job photos (from its Facebook page) with alt text and captions.
- Town pages render only verified village facts (quoted from official pages, kept in the agency's research folder).
  A town gets a page only once its facts file exists.
- The build refuses to publish on: em or en dashes, the former franchise name, claim words outside customer quotes,
  UK spellings, a page without exactly one H1, broken internal links, unfilled placeholders, or town pages that read
  too much alike (5-gram overlap above 0.30).
- `SITE` and `BASE` in `build.py` point at the GitHub Pages address. Change both the day the custom domain points here.
- Deploy with `../deploy-site.sh` (agency folder): it builds, runs the render check (every page at 360, 375, 390 and
  1280 px, menu open and closed, no sideways scroll), then commits and pushes.
- The generator, `content/`, the source `assets/` and this README are not published. At launch the custom domain's
  `CNAME` file goes in `docs/` (the build keeps it).
