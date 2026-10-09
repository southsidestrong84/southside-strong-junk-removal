# Southside Strong Junk Removal

Static site for Southside Strong Junk Removal, Chicago Ridge, IL. Preview, not launched: every page carries
`noindex, nofollow` until the owner approves the copy.

**Preview:** https://ogeddiesmith.github.io/southside-strong-junk-removal/

Built by `build.py`. Do not hand-edit the HTML; the next build overwrites it.

    python3 build.py

- `content/services.py`: service pages. `content/towns.py`: town pages. `content/facts.py`: state and federal rules, each with its source.
- Town pages render only verified village facts (quoted from official pages, kept in the agency's research folder).
- The build refuses to publish on: em or en dashes, the former franchise name, claim words outside customer quotes,
  UK spellings, a page without exactly one H1, broken internal links, unfilled placeholders, or town pages that read
  too much alike (5-gram overlap above 0.30).
- `SITE` and `BASE` in `build.py` point at the GitHub Pages address. Change both the day the custom domain points here.
