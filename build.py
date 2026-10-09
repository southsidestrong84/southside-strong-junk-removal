#!/usr/bin/env python3
"""
Southside Strong Junk Removal: static site generator.

    python3 build.py

Do not hand-edit the HTML; every build rewrites it. Copy lives in content/, research in ../research/.

VOICE. The owner's own words set the tone: "Built by the SouthSide. Ready to work!", "Locally owned, honest
pricing, and no-nonsense service.", "Built on Truth. Work Hard. Stay Southside Strong." Short, plain,
blue-collar. No agency gloss, no superlatives outside customer quotes.

TRUTH. Anything said about the business traces to its Facebook page, its current site (sosidejunk.com) or
its Google reviews. State and village rules trace to an official page with the sentence quoted
(research/FACTS-VERIFIED.md, research/towns/facts-group*.json). No prices, no same-day promise, and never
the name of the franchise brand the business used to operate under.

PREVIEW. NOINDEX stays True until the owner approves the copy and the CONFIRM list in ../CLIENT-BRIEF.md.
SITE and BASE point at the GitHub Pages address and change the day the custom domain is pointed here.
"""
import glob, hashlib, html, json, math, os, re, shutil, sys, unicodedata
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
RESEARCH = os.path.normpath(os.path.join(HERE, "..", "research"))
sys.path.insert(0, HERE)
from content.services import SERVICES
from content.facts import FACTS
from content import towns as T

BRAND = "Southside Strong Junk Removal"
SHORT = "Southside Strong"
PHONE = "(708) 247-6440"
PHONE_E164 = "+17082476440"
EMAIL = "southsidestrong84@gmail.com"
BASE = "/southside-strong-junk-removal"          # "" once a custom domain points at this repo
SITE = "https://ogeddiesmith.github.io" + BASE
NOINDEX = True
ASSET_V = "4"
FACEBOOK = "https://www.facebook.com/profile.php?id=61576515234106"
PLACE_ID = "ChIJhbWVU5cHPGQR6F34P4rSmgw"
GOOGLE_REVIEWS = f"https://search.google.com/local/reviews?placeid={PLACE_ID}"
GOOGLE_MAPS = f"https://www.google.com/maps/place/?q=place_id:{PLACE_ID}"
MOTTO = "Built on Truth. Work Hard. Stay Southside Strong."
RATING, RATING_COUNT, RATING_ASOF = "5.0", 34, "October 2026"   # Google Business Profile, read 2026-10-09
LOGO = "/assets/img/mark.svg"                    # placeholder mark until the owner's logo file is approved for use

esc = lambda s: html.escape(str(s), quote=True)
u = lambda p: BASE + p
absu = lambda p: SITE + p
TEL, SMS = f"tel:{PHONE_E164}", f"sms:{PHONE_E164}"
PAGES = {}       # path -> html
META = {}        # path -> dict(title, desc)

# ---------------------------------------------------------------- icons (inline SVG, stroke style)
def ico(name):
    p = {
      "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
      "msg": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
      "check": '<path d="M20 6 9 17l-5-5"/>',
      "star6": '<path fill="currentColor" stroke="none" d="M12 1.8 14.7 7.2 20.8 6.9 17.3 12 20.8 17.1 14.7 16.8 12 22.2 9.3 16.8 3.2 17.1 6.7 12 3.2 6.9 9.3 7.2Z"/>',
      "sofa": '<path d="M4 11V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v3"/><path d="M2 13a2 2 0 0 1 4 0v2h12v-2a2 2 0 0 1 4 0v5H2z"/><path d="M5 18v2M19 18v2"/>',
      "fridge": '<rect x="6" y="2" width="12" height="20" rx="2"/><path d="M6 10h12M9 5v2M9 13v3"/>',
      "bed": '<path d="M2 18V6M2 12h20v6M22 18v-4a3 3 0 0 0-3-3H10v4"/><circle cx="6.5" cy="10" r="1.5"/>',
      "tub": '<path d="M3 11h18v3a6 6 0 0 1-6 6H9a6 6 0 0 1-6-6z"/><path d="M7 7c0-1 1-1 1-2M11 7c0-1 1-1 1-2M15 7c0-1 1-1 1-2"/>',
      "pool": '<path d="M2 18c2 0 2-1.5 4-1.5S8 18 10 18s2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 4-1.5"/><path d="M7 15V5a2 2 0 0 1 4 0M13 15V5a2 2 0 0 1 4 0M7 9h6M7 12h6"/>',
      "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10Z"/><path d="M2 21c0-3 1.9-5.4 5.2-6"/>',
      "hammer": '<path d="m15 12-8.4 8.4a2 2 0 0 1-2.8-2.8L12.2 9"/><path d="M17.6 15 22 10.6 13.4 2 9 6.4l2.6 2.6"/>',
      "debris": '<path d="M3 20h18M5 20l3-8 4 3 3-7 4 12"/>',
      "garage": '<path d="M3 21V9l9-6 9 6v12"/><path d="M7 21v-8h10v8M7 16h10"/>',
      "stairs": '<path d="M3 21h4v-4h4v-4h4V9h4V5h2"/>',
      "house": '<path d="M3 11 12 3l9 8v10H3z"/><path d="M9 21v-6h6v6"/>',
      "building": '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M8 7h2M14 7h2M8 11h2M14 11h2M8 15h2M14 15h2M11 21v-3h2v3"/>',
      "tv": '<rect x="2" y="5" width="20" height="13" rx="2"/><path d="M8 21h8M12 18v3"/>',
      "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
      "pin": '<path d="M12 21s7-6.2 7-11a7 7 0 0 0-14 0c0 4.8 7 11 7 11Z"/><circle cx="12" cy="10" r="2.5"/>',
      "shield": '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/>',
      "tag": '<path d="M20 12 12 20l-9-9V3h8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
    }[name]
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'

STAR = ico("star6")

# ---------------------------------------------------------------- reviews (Google, via research/serp)
NAME_FIX = {"Leo the Construction guy": "Leo", "Cebuana": "Cebuana", "Liezel Largo (Zhell)": "Liezel L."}
EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\u200D\U0001F3FB-\U0001F3FF\u2B50]")

def load_reviews():
    out, seen = [], set()
    for f in sorted(glob.glob(os.path.join(RESEARCH, "serp", "reviews_ss*.json"))):
        for r in json.load(open(f, encoding="utf-8")).get("reviews", []):
            rid = r.get("review_id") or r.get("link")
            if rid in seen:
                continue
            seen.add(rid)
            text = re.sub(r"\s+", " ", EMOJI.sub("", r.get("snippet") or "")).strip()
            if not text:
                continue
            raw = (r.get("user") or {}).get("name", "").strip()
            if raw in NAME_FIX:
                name = NAME_FIX[raw]
            else:
                parts = [p for p in re.sub(r"\(.*?\)", "", raw).split() if p]
                name = (parts[0].capitalize() + (f" {parts[-1][0].upper()}." if len(parts) > 1 else "")) if parts else "Google reviewer"
            iso = (r.get("iso_date") or "")[:10]
            when = date.fromisoformat(iso).strftime("%b %Y") if iso else ""
            out.append({"id": hashlib.sha1(rid.encode()).hexdigest()[:10], "name": name, "text": text, "when": when,
                        "iso": iso, "rating": r.get("rating", 5), "link": r.get("link") or GOOGLE_REVIEWS})
    out.sort(key=lambda x: x["iso"], reverse=True)
    return out

REVIEWS = load_reviews()
RID = {r["id"]: r for r in REVIEWS}

def review_card(r):
    stars = "\u2605" * int(round(r["rating"]))
    return (f'<blockquote class="review" data-quote><span class="stars" aria-label="{r["rating"]} out of 5 stars">{stars}</span>'
            f'<p>&ldquo;{esc(r["text"])}&rdquo;</p><footer>{esc(r["name"])}, <a href="{esc(r["link"])}" rel="nofollow noopener" target="_blank">Google review</a>, {esc(r["when"])}</footer></blockquote>')

def reviews_matching(words, n, exclude=()):
    hits = [r for r in REVIEWS if r["id"] not in exclude and any(w in r["text"].lower() for w in words)]
    return hits[:n]

def review_block(rs, three=False):
    return f'<div class="reviews{" three" if three else ""}">' + "".join(review_card(r) for r in rs) + "</div>"

TOPICS = {"pool": ["pool"], "demo": ["demo", "deck", "scrap wood", "remodel"], "commercial": ["commercial", "business", "buisness", "client"]}

# ---------------------------------------------------------------- data
CENSUS = json.load(open(os.path.join(RESEARCH, "towns", "towns-census.json"), encoding="utf-8"))["towns"]
OVERRIDES = json.load(open(os.path.join(RESEARCH, "towns", "overrides.json"), encoding="utf-8"))
OUTLETS = json.load(open(os.path.join(RESEARCH, "towns", "donation-outlets.json"), encoding="utf-8"))["outlets"]
TOWN_FACTS = {}
for f in sorted(glob.glob(os.path.join(RESEARCH, "towns", "facts-group*.json"))):
    try:
        for row in json.load(open(f, encoding="utf-8")):
            ov = OVERRIDES.get(row["slug"], {})
            for k in ov.get("drop", []):
                if k in row["facts"]:
                    row["facts"][k] = {"status": "unknown", "dropped": True}
            for k, v in ov.get("display", {}).items():
                if row["facts"].get(k, {}).get("status") == "verified":
                    row["facts"][k]["value"] = v
            row["contact"] = ov.get("contact")
            row["caveat"] = ov.get("caveat")
            TOWN_FACTS[row["slug"]] = row
    except Exception as e:
        print(f"warning: could not read {os.path.basename(f)}: {e}")

# ---------------------------------------------------------------- placeholder fill
def fill(s):
    s = re.sub(r"\{u:(/[^}]*)\}", lambda m: u(m.group(1)), s)
    def fact(m):
        f = FACTS[m.group(1)]
        src = "".join(f'<li><a href="{esc(url)}" rel="nofollow noopener" target="_blank">{esc(label)}</a></li>' for label, url in f.get("sources", []))
        return f["html"] + (f'<p class="note">Sources:</p><ul class="note">{src}</ul>' if src else "")
    s = re.sub(r"\{fact:([a-z_]+)\}", fact, s)
    def event(m):
        for f in FACTS.values():
            ev = (f.get("events") or {}).get(m.group(1))
            if ev:
                return ev["html"] if date.today().isoformat() <= ev["until"] else ""
        return ""
    s = re.sub(r"\{event:([a-z_]+)\}", event, s)
    s = s.replace("{donations:all}", donations_html(OUTLETS))
    s = re.sub(r"\{reviews:([a-z]+)\}", lambda m: review_block(reviews_matching(TOPICS[m.group(1)], 2)), s)
    s = re.sub(r"\{reviewcards:([a-f0-9,]+)\}", lambda m: review_block([RID[i] for i in m.group(1).split(",") if i in RID]), s)
    return fill(s) if re.search(r"\{(u|fact|reviews|reviewcards|event|donations):", s) else s

def donations_html(items, miles=None):
    rows = []
    for i, o in enumerate(items):
        d = f" About {miles[i]:.1f} miles away." if miles else ""
        ph = f" {esc(o['phone'])}." if o.get("phone") else ""
        rows.append(f"<li><b>{esc(o['name'])}</b>, {esc(o['street'])}, {esc(o['city'])}.{ph}{d}</li>")
    return "<ul>" + "".join(rows) + "</ul><p class=\"note\">Call ahead to check what each one accepts and when.</p>"

# ---------------------------------------------------------------- layout
NAV = [("/services/", "Services"), ("/service-area/", "Service area"), ("/pricing/", "Pricing"),
       ("/reviews/", "Reviews"), ("/about/", "About"), ("/contact/", "Free estimate")]

def schema_tag(objs):
    return "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False, separators=(",", ":"))}</script>' for o in objs)

def crumbs_html(trail):
    last = len(trail) - 1
    items = "".join(f'<li aria-current="page">{esc(n)}</li>' if i == last else f'<li><a href="{u(p)}">{esc(n)}</a></li>' for i, (n, p) in enumerate(trail))
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{items}</ol></nav>'

def crumbs_schema(trail, path):
    els = []
    for i, (n, p) in enumerate(trail, 1):
        els.append({"@type": "ListItem", "position": i, "name": n, "item": absu(p or path)})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": els}

BUSINESS_ID = absu("/#business")
def business_schema():
    areas = [{"@type": "City", "name": f"{t}, IL"} for _, t in T.WAVE1] + [{"@type": "City", "name": f"{t}, IL"} for t in T.LISTED_FARTHER] + [{"@type": "City", "name": "Chicago, IL"}]
    return {"@context": "https://schema.org", "@type": "LocalBusiness", "@id": BUSINESS_ID, "name": BRAND, "url": absu("/"),
            "telephone": "+1-708-247-6440", "email": EMAIL, "image": absu("/assets/img/og.jpg"), "logo": absu(LOGO),
            "description": "Locally owned junk removal company based in Chicago Ridge, IL, serving the southwest suburbs and Chicago's Southwest Side.",
            "slogan": MOTTO, "address": {"@type": "PostalAddress", "addressLocality": "Chicago Ridge", "addressRegion": "IL", "postalCode": "60415", "addressCountry": "US"},
            "areaServed": areas, "sameAs": [FACEBOOK, GOOGLE_MAPS]}

def page(path, title, desc, main, schema=(), trail=None, active=None, hero=None):
    robots = '<meta name="robots" content="noindex, nofollow">' if NOINDEX else '<meta name="robots" content="index, follow, max-image-preview:large">'
    canon = absu(path)
    cur = ' aria-current="page"'
    nav = "".join(f'<li><a href="{u(p)}"{cur if active == p else ""}>{esc(n)}</a></li>' for p, n in NAV)
    objs = list(schema) + ([crumbs_schema(trail, path)] if trail else [])
    head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canon)}">
{robots}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(BRAND)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canon)}">
<meta property="og:image" content="{absu('/assets/img/og.jpg')}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Southside Strong Junk Removal, Chicago Ridge, IL. Call or text {PHONE}.">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0e2340">
<link rel="icon" href="{u('/assets/img/favicon.svg')}" type="image/svg+xml">
<link rel="icon" href="{u('/assets/img/favicon-32.png')}" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{u('/assets/img/apple-touch-icon.png')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Oswald:wght@500;600;700&display=swap">
<link rel="stylesheet" href="{u('/assets/style.css')}?v={ASSET_V}">
{schema_tag(objs)}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap"><span><span class="stars" aria-hidden="true">&#10038; &#10038; &#10038; &#10038;</span> Locally owned in Chicago Ridge, IL</span><span>Call or text <a href="{TEL}">{PHONE}</a></span></div></div>
<header class="site"><div class="wrap">
<a class="brand" href="{u('/')}"><img src="{u(LOGO)}" alt="" width="48" height="48"><span class="word"><b>Southside Strong</b><i>Junk Removal</i></span></a>
<nav class="main" aria-label="Main"><ul>{nav}</ul></nav>
<div class="head-cta"><a class="btn btn-red btn-sm btn-call" href="{TEL}">{ico('phone')}<span class="long">{PHONE}</span><span class="sr">Call</span></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="Menu">{ico('menu')}</button></div>
</div>
<nav class="mobile-nav" id="mobile-nav" aria-label="Mobile"><ul>{nav}<li><a href="{SMS}">Text us a photo</a></li></ul></nav>
</header>
<main id="main">
"""
    hero_html = ""
    if hero:
        hero_html = hero if isinstance(hero, str) else sub_hero(*hero, trail=trail, key=path)
    foot_services = "".join(f'<li><a href="{u("/" + s["slug"] + "/")}">{esc(s["name"])}</a></li>' for s in SERVICES[:8])
    foot_towns = "".join(f'<li><a href="{u(T.page_path(s))}">{esc(t)}</a></li>' for s, t in T.WAVE1[:8])
    foot = f"""</main>
<footer class="site"><div class="wrap">
<div class="cols4">
<div><h2>{esc(BRAND)}</h2><p>Chicago Ridge, IL 60415<br>Call or text <a href="{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p class="motto">{esc(MOTTO)}</p><p><a href="{FACEBOOK}" rel="noopener" target="_blank">Facebook</a> &middot; <a href="{GOOGLE_REVIEWS}" rel="noopener" target="_blank">Google reviews</a></p></div>
<div><h2>Services</h2><ul>{foot_services}<li><a href="{u('/services/')}">All services</a></li></ul></div>
<div><h2>Service area</h2><ul>{foot_towns}<li><a href="{u('/service-area/')}">All towns</a></li></ul></div>
</div>
<p class="legal">&copy; {date.today().year} {esc(BRAND)}. Locally owned. <a href="{u('/what-we-take/')}">What we take</a> &middot; <a href="{u('/faq/')}">FAQ</a> &middot; <a href="{u('/privacy/')}">Privacy</a></p>
</div></footer>
<div class="callbar"><a class="btn btn-red" href="{TEL}">{ico('phone')}Call</a><a class="btn btn-ghost" href="{SMS}">{ico('msg')}Text a photo</a></div>
<script src="{u('/assets/app.js')}?v={ASSET_V}" defer></script>
</body>
</html>
"""
    doc = head + hero_html + fill(main) + foot
    PAGES[path] = doc
    META[path] = {"title": title, "desc": desc}

SHORT_REVIEWS = [r for r in REVIEWS if 70 <= len(r["text"]) <= 240]

def hero_aside(key):
    """One real review per page, chosen by the page path, shown beside the hero on wide screens."""
    r = SHORT_REVIEWS[int(hashlib.sha1(key.encode()).hexdigest(), 16) % len(SHORT_REVIEWS)]
    return (f'<aside class="hero-card" aria-label="A customer review"><blockquote class="review" data-quote>'
            f'<span class="stars" aria-label="5 out of 5 stars">\u2605\u2605\u2605\u2605\u2605</span><p>&ldquo;{esc(r["text"])}&rdquo;</p>'
            f'<footer>{esc(r["name"])}, Google review. {RATING} stars from {RATING_COUNT} reviews.</footer></blockquote></aside>')

def sub_hero(h1, lede, trail=None, ctas=True, key=""):
    c = (f'<div class="ctas"><a class="btn btn-red" href="{TEL}">{ico("phone")}Call {PHONE}</a>'
         f'<a class="btn btn-ghost" href="{SMS}">{ico("msg")}Text a photo</a></div>') if ctas else ""
    return (f'<section class="hero sub"><div class="wrap hero-grid"><div>{crumbs_html(trail) if trail else ""}<h1>{esc(h1)}</h1>'
            f'<p class="lede">{fill(lede)}</p>{c}</div>{hero_aside(key or h1)}</div></section>')

def cta_band(h="Ready to get rid of it?", p="Call or text a photo of what needs to go. The estimate is free."):
    return (f'<section class="cta-band"><div class="wrap"><div><h2>{esc(h)}</h2><p>{esc(p)}</p></div>'
            f'<div class="ctas"><a class="btn btn-red" href="{TEL}">{ico("phone")}Call {PHONE}</a>'
            f'<a class="btn btn-ghost" href="{SMS}">{ico("msg")}Text a photo</a></div></div></section>')

def faq_html(faqs):
    return '<div class="faq">' + "".join(f"<details><summary>{esc(q)}</summary><div class=\"a\">{fill(a)}</div></details>" for q, a in faqs) + "</div>"

def faq_schema(faqs):
    strip = lambda h: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fill(h)))).strip()
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faqs]}

def section(h2, inner, cls="band", kicker=None, sub=None):
    k = f'<p class="kicker">{esc(kicker)}</p>' if kicker else ""
    s = f"<p>{sub}</p>" if sub else ""
    return f'<section class="{cls}"><div class="wrap"><div class="section-head">{k}<h2>{esc(h2)}</h2>{s}</div>{inner}</div></section>'

def service_cards(items, cols="g3"):
    return f'<div class="grid {cols}">' + "".join(
        f'<a class="card" href="{u("/" + s["slug"] + "/")}"><div class="icon">{ico(s["icon"])}</div><h3>{esc(s["name"])}</h3><p>{esc(s["card"])}</p><span class="more">See how it works</span></a>'
        for s in items) + "</div>"

def towns_list(items):
    return '<ul class="towns">' + "".join(f'<li><a href="{u(T.page_path(s))}">{esc(t)}<span>{d}</span></a></li>' for s, t, d in items) + "</ul>"

def wave1_with_miles():
    rows = []
    for s, t in T.WAVE1:
        m = CENSUS[t]["miles_from_chicago_ridge"]
        rows.append((s, t, "home base" if m == 0 else f"{m:g} mi"))
    return sorted(rows, key=lambda r: CENSUS[r[1]]["miles_from_chicago_ridge"])

# ---------------------------------------------------------------- home
def build_home():
    hero = f"""<section class="hero"><div class="wrap hero-grid"><div>
<div class="stars-row">{STAR*4}</div>
<h1>Junk removal in Chicago Ridge and the southwest suburbs</h1>
<p class="lede">Locally owned, honest pricing and no-nonsense service. Steve and his crew carry it out from wherever it sits, haul it away and leave the place clean.</p>
<div class="ctas"><a class="btn btn-red" href="{TEL}">{ico('phone')}Call {PHONE}</a><a class="btn btn-ghost" href="{SMS}">{ico('msg')}Text us a photo</a><a class="btn btn-ghost" href="{u('/contact/')}">Free estimate</a></div>
<ul class="proof"><li>{ico('check')}{RATING} stars on Google from {RATING_COUNT} reviews</li><li>{ico('check')}Free estimates</li><li>{ico('check')}Licensed and insured</li><li>{ico('check')}Based in Chicago Ridge</li></ul>
</div>{hero_aside("/")}</div></section>"""
    steps = f"""<ol class="steps">
<li><b>Call or text</b>Tell us what needs to go and where it is, or text a few photos to {PHONE}.</li>
<li><b>Get your price</b>We look at the job and give you a straight price before we lift anything.</li>
<li><b>We haul it and clean up</b>We carry it out, load it, and leave the space swept. You do not lift a thing.</li></ol>"""
    top = REVIEWS[:6]
    rev = (f'<div class="rating-line"><span class="big">{RATING}</span><span class="stars" aria-hidden="true">\u2605\u2605\u2605\u2605\u2605</span>'
           f'<span>{RATING_COUNT} Google reviews, as of {RATING_ASOF}. <a href="{GOOGLE_REVIEWS}" rel="noopener" target="_blank">See them on Google</a></span></div>'
           + review_block(top, three=True) + f'<p class="center" style="margin-top:18px"><a class="btn btn-line" href="{u("/reviews/")}">Read all {len(REVIEWS)} written reviews</a></p>')
    about = f"""<div class="two"><div class="prose">
<p>{SHORT} is a local junk removal company based in Chicago Ridge. Steve runs the jobs with his son, and Nicole keeps the schedule and the phone in the office. Customers bring up the communication again and again in their reviews.</p>
<p>We take one couch or a whole house. Furniture, appliances, mattresses, hot tubs, above-ground pools, swing sets, yard waste, remodeling debris and full cleanouts for homeowners, landlords, property managers and businesses.</p>
<p><a href="{u('/about/')}">More about us</a></p></div>
<div class="card"><p class="kicker">Our motto</p><h3>{esc(MOTTO)}</h3><p class="muted">From Bridgeport to Beverly to the Burbs.</p></div></div>"""
    near = wave1_with_miles()
    area = (towns_list(near) + f'<p style="margin-top:14px">Also on Chicago\'s Southwest Side: <a href="{u(T.page_path("chicago"))}">Beverly, Mount Greenwood and Morgan Park</a>. '
            f'Farther out, we also serve {", ".join(T.LISTED_FARTHER[:-1])} and {T.LISTED_FARTHER[-1]}. <a href="{u("/service-area/")}">Full service area</a></p>')
    faqs = [
      ("How much does junk removal cost?", f"<p>It depends on how much there is, what it is, and how hard it is to get out. Call or text a photo to {PHONE} and we will give you a straight price before we start. See <a href=\"{{u:/pricing/}}\">how pricing works</a>.</p>"),
      ("Do I have to bring everything outside?", "<p>No. We carry it out from wherever it is: basement, attic, upstairs, garage or backyard.</p>"),
      ("What do you not take?", "<p>Household hazardous waste like wet paint, solvents, chemicals, motor oil and propane tanks. See <a href=\"{u:/what-we-take/}\">what we take</a> for the full list and where those items can go.</p>"),
      ("Do you take just one item?", "<p>Yes. A single couch, mattress or fridge is a normal call.</p>"),
      ("Which towns do you serve?", "<p>Chicago Ridge and the southwest suburbs, plus Chicago's Southwest Side. See the <a href=\"{u:/service-area/}\">service area</a> for every town.</p>"),
    ]
    main = (section("What we haul", service_cards(SERVICES), cls="band", kicker="Services", sub="If it is not hazardous, we can probably take it. Pick a job to see how it works.")
            + section("How it works", steps, cls="band alt", kicker="Three steps")
            + section("What customers say", rev, cls="band", kicker="Reviews")
            + section("Built by the Southside", about, cls="band sky", kicker="About us")
            + section("Where we work", area, cls="band", kicker="Service area", sub="Based in Chicago Ridge. Here is how far each town is from our base.")
            + section("Questions people ask", faq_html(faqs), cls="band alt", kicker="FAQ")
            + cta_band())
    page("/", "Junk Removal Chicago Ridge, IL | Southside Strong Junk Removal",
         "Locally owned junk removal in Chicago Ridge, Oak Lawn and the southwest suburbs. Furniture, appliances, cleanouts, hot tubs and pools. Free estimates.",
         main, schema=[business_schema(), {"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "url": absu("/")}, faq_schema(faqs)], hero=hero)

# ---------------------------------------------------------------- services
def build_services():
    trail0 = [("Home", "/"), ("Services", None)]
    main = (section("Every job we do", service_cards(SERVICES), kicker="Services",
                    sub="Not sure where your job fits? Call or text a photo and ask.")
            + section("Also on our list", f"""<div class="prose"><ul class="checks"><li>Trash and junk pickup for one-time cleanups</li><li>Trailer rental: call {PHONE} to ask about it</li></ul></div>""", cls="band alt")
            + cta_band())
    page("/services/", "Junk Removal Services | Southside Strong, Chicago Ridge",
         "Junk removal services in Chicago Ridge and the southwest suburbs: furniture, appliances, mattresses, hot tubs, pools, yard waste, debris and cleanouts.",
         main, trail=[("Home", "/"), ("Services", "/services/")], active="/services/",
         hero=("Junk removal services", "Furniture to full cleanouts. If it is not hazardous, we can probably take it."))
    for s in SERVICES:
        path = f"/{s['slug']}/"
        trail = [("Home", "/"), ("Services", "/services/"), (s["name"], None)]
        body = "".join(f'<h2>{esc(h)}</h2>{b}' for h, b in s["body"])
        used = set(re.findall(r"\{reviews:([a-z]+)\}", body))
        pool_ids = set()
        for t in used:
            pool_ids |= {r["id"] for r in reviews_matching(TOPICS[t], 2)}
        rel_reviews = reviews_matching(s["review_words"], 2, exclude=pool_ids) or REVIEWS[:2]
        related = [x for x in SERVICES if x["slug"] in s["related"]]
        near = wave1_with_miles()[:8]
        aside = (f'<div class="card"><h3>Get a free estimate</h3><p>Call or text a photo of what needs to go.</p>'
                 f'<p><a class="btn btn-red" href="{TEL}">{ico("phone")}{PHONE}</a></p><p class="muted">Based in Chicago Ridge, serving the southwest suburbs and Chicago\'s Southwest Side.</p></div>')
        main = (f'<section class="band"><div class="wrap"><div class="two"><div class="prose">{body}</div><div>{aside}</div></div></div></section>'
                + section("What customers say", review_block(rel_reviews), cls="band alt")
                + section(f"{s['name']} questions", faq_html(s["faqs"]), cls="band")
                + section(f"{s['name']} near you", towns_list(near) + f'<p style="margin-top:12px"><a href="{u("/service-area/")}">See every town we serve</a></p>', cls="band sky")
                + section("Related services", service_cards(related), cls="band")
                + cta_band())
        svc = {"@context": "https://schema.org", "@type": "Service", "name": s["name"].capitalize(), "serviceType": s["name"].capitalize(),
               "provider": {"@id": BUSINESS_ID}, "areaServed": [{"@type": "City", "name": f"{t}, IL"} for _, t in T.WAVE1], "url": absu(path)}
        page(path, s["title"], s["desc"], main, schema=[svc, faq_schema(s["faqs"])], trail=[(n, p if p else path) for n, p in trail], active="/services/",
             hero=(s["h1"], s["lede"]))

# ---------------------------------------------------------------- towns
def build_towns():
    meta = T.WAVE1 + [("chicago", "Chicago")]
    for slug, town in meta:
        facts = TOWN_FACTS.get(slug)
        d = T.compose(slug, town, CENSUS, facts, T.WAVE1, REVIEWS, esc, PHONE, OUTLETS, donations_html)
        path = T.page_path(slug)
        trail = [("Home", "/"), ("Service area", "/service-area/"), (d["place"], path)]
        body = "".join(section(h, inner, cls="band" + (" alt" if i % 2 else "")) for i, (h, inner) in enumerate(d["sections"]))
        near = d["nearby"]
        near_html = towns_list([(s, t, f"{m:.1f} mi" if m is not None else "") for s, t, m in near])
        svc_links = "<p>" + " &middot; ".join(f'<a href="{u("/" + sl + "/")}">{esc(nm)}</a>' for sl, nm in d["services"]) + f' &middot; <a href="{u("/services/")}">every service</a></p>'
        main = (body + section(f"Junk removal questions from {d['place']}", faq_html(d["faqs"]), cls="band")
                + section(f"Jobs we do in {d['place']}", svc_links, cls="band alt")
                + section("Nearby towns we serve", near_html, cls="band sky")
                + cta_band(f"Junk removal in {d['place']}", f"Call or text {PHONE}. Free estimates."))
        area = ({"@type": "City", "name": "Chicago, IL"} if slug == "chicago" else {"@type": "City", "name": f"{town}, IL"})
        svc = {"@context": "https://schema.org", "@type": "Service", "name": f"Junk removal in {d['place']}", "serviceType": "Junk removal",
               "provider": {"@id": BUSINESS_ID}, "areaServed": area, "url": absu(path)}
        page(path, d["title"], d["desc"], main, schema=[svc, faq_schema(d["faqs"])], trail=trail, active="/service-area/",
             hero=(d["h1"], d["lede"]))

def build_area():
    rows = wave1_with_miles()
    ring = lambda lo, hi: [r for r in rows if lo <= CENSUS[r[1]]["miles_from_chicago_ridge"] < hi]
    inner = (f"<h3>Home base and next door</h3>{towns_list(ring(0, 4))}"
             f"<h3 style=\"margin-top:22px\">Four to eight miles</h3>{towns_list(ring(4, 8))}"
             f"<h3 style=\"margin-top:22px\">Eight miles and up</h3>{towns_list(ring(8, 99))}"
             f"<h3 style=\"margin-top:22px\">Chicago's Southwest Side</h3>{towns_list([('chicago', 'Beverly, Mount Greenwood, Morgan Park', '')])}"
             f"<p style=\"margin-top:18px\">We also serve {', '.join(T.LISTED_FARTHER[:-1])} and {T.LISTED_FARTHER[-1]}. Call to ask about your town.</p>")
    page("/service-area/", "Service Area: Chicago Ridge & the Southwest Suburbs",
         "Junk removal in Chicago Ridge, Oak Lawn, Orland Park, Tinley Park, the southwest suburbs and Chicago's Southwest Side. See your town's pickup rules.",
         section("Towns we serve", inner, kicker="Service area", sub="Every town page lists what that town's own garbage pickup will take, so you know when you need us and when you do not.") + cta_band(),
         trail=[("Home", "/"), ("Service area", "/service-area/")], active="/service-area/",
         hero=("Where we work", "Based in Chicago Ridge. From Bridgeport to Beverly to the Burbs."))

# ---------------------------------------------------------------- about, pricing, what we take, reviews, contact, faq, privacy, 404
def build_about():
    rv = reviews_matching(["son", "father", "nicole", "steve"], 4)
    body = f"""<div class="two"><div class="prose">
<p>{SHORT} is a locally owned junk removal company in Chicago Ridge, built by the Southside and ready to work. Our bio puts it plainly: we bring grit and pride to every haul, with honest pricing and no-nonsense service.</p>
<h2>Who shows up</h2>
<p>Steve owns the company and runs the jobs. His son works them with him, and Nicole runs the office, keeps the schedule and keeps you posted. Customers notice: "Steve was great and his son too," one wrote, and another called us a "father and son duo."</p>
<h2>What we do</h2>
<p>We help homeowners, landlords, property managers and businesses clear out unwanted junk. A single item, a garage cleanout or a full property cleanout: we do the heavy lifting and get the job done right. See <a href="{u('/services/')}">every service</a>.</p>
<h2>How we work</h2>
<ul class="checks"><li>Straight, upfront pricing before we start</li><li>We show up when we say we will, and we keep you posted</li><li>We protect walls and floors on the way out</li><li>We clean up before we leave</li><li>Licensed and insured</li></ul>
</div><div><div class="card"><p class="kicker">Our motto</p><h3>{esc(MOTTO)}</h3><p class="muted">From Bridgeport to Beverly to the Burbs.</p></div></div></div>"""
    page("/about/", "About Southside Strong Junk Removal | Chicago Ridge, IL",
         "Southside Strong is a locally owned, father-and-son junk removal company based in Chicago Ridge, IL. Honest pricing and no-nonsense service.",
         f'<section class="band"><div class="wrap">{body}</div></section>' + section("In customers' words", review_block(rv), cls="band alt") + cta_band(),
         trail=[("Home", "/"), ("About", "/about/")], active="/about/",
         hero=("Built by the Southside. Ready to work.", "A locally owned, father-and-son junk removal company based in Chicago Ridge."))

def build_pricing():
    body = f"""<div class="prose">
<p>Every junk removal job is priced a little differently, because every pile is different. Here is what goes into the price, and how to get yours.</p>
<h2>What sets the price</h2>
<ul class="checks">
<li><b>How much there is.</b> Most junk removal is priced by how much space the load takes up in the truck.</li>
<li><b>What it is.</b> Some items cost more to dispose of properly than others, such as appliances that hold refrigerant, mattresses, tires and hot tubs.</li>
<li><b>How hard it is to get out.</b> Stairs, tight turns, long carries and pieces that have to be taken apart all take time.</li>
<li><b>Tear-out work.</b> Taking down a shed, a deck or a pool is labor on top of the hauling.</li></ul>
<h2>How to get your price</h2>
<p>Call or text {PHONE}. The fastest way is to text a few photos of what needs to go and tell us where it is (basement, upstairs, garage, yard). We will give you a straight price before we start. Customers mention it in their reviews: "They are upfront with their pricing."</p>
<h2>Ways to keep the cost down</h2>
<ul class="checks">
<li>If you only have one or two small items, check your village's bulk pickup first. Each town page in our <a href="{u('/service-area/')}">service area</a> lists the rules we could confirm.</li>
<li>Set aside paint, chemicals and propane tanks before we come. We cannot take them; see <a href="{u('/what-we-take/')}">what we take</a>.</li>
<li>Donate the things that are still good before the job. Drop-off spots near Chicago Ridge are on the same page.</li>
<li>Bundle jobs. The garage and the basement in one trip usually costs less than two trips.</li></ul>
{{fact:pricing_national}}
</div>"""
    page("/pricing/", "How Junk Removal Pricing Works | Southside Strong",
         "How junk removal is priced in Chicago Ridge and the southwest suburbs: volume, item type and labor. Text a photo for a free, upfront estimate.",
         f'<section class="band"><div class="wrap">{body}</div></section>' + cta_band("Get your price", "Text a photo to " + PHONE + ". The estimate is free."),
         trail=[("Home", "/"), ("Pricing", "/pricing/")], active="/pricing/",
         hero=("How junk removal pricing works", "Straight prices, before we start. Here is what goes into one."))

def build_what_we_take():
    body = f"""<div class="two"><div class="prose">
<h2>What we take</h2>
<ul class="checks cols"><li>Furniture of every kind</li><li>Appliances</li><li>Mattresses and box springs</li><li>TVs and electronics</li>
<li>Hot tubs and above-ground pools</li><li>Swing sets, playsets and trampolines</li><li>Yard waste and brush</li><li>Sheds, decks and fencing</li>
<li>Remodeling debris</li><li>Garage, basement and attic junk</li><li>Office furniture and equipment</li><li>Exercise equipment</li></ul>
<h2>What we cannot take</h2>
<p>Household hazardous waste does not go in a junk truck. Please set these aside before we come:</p>
<ul class="crosses cols"><li>Wet paint, stains and solvents</li><li>Pesticides, pool and lawn chemicals</li><li>Motor oil, gasoline and antifreeze</li><li>Propane tanks and other gas cylinders</li>
<li>Asbestos</li><li>Medical waste and needles</li><li>Ammunition and fireworks</li></ul>
{{fact:hhw_where}}
<h2>Where things go after pickup</h2>
<p>We recycle what can be recycled and dispose of the rest properly. Electronics go to recyclers, since Illinois keeps them out of landfills. Metal goes to scrap. If you would rather donate usable items yourself before we arrive, these drop-off spots are close to Chicago Ridge:</p>
{{fact:donation_list}}
</div><div><div class="card"><h3>Not sure about an item?</h3><p>Text a photo to <a href="{SMS}">{PHONE}</a> and ask.</p></div></div></div>"""
    page("/what-we-take/", "What We Take & What We Can't | Southside Strong Junk Removal",
         "What Southside Strong Junk Removal takes, what no junk hauler can take, and where hazardous waste and donations can go near Chicago Ridge, IL.",
         f'<section class="band"><div class="wrap">{body}</div></section>' + cta_band(),
         trail=[("Home", "/"), ("What we take", "/what-we-take/")],
         hero=("What we take, and what we can't", "If it is not hazardous, we can probably take it."))

def build_reviews():
    rev = (f'<div class="rating-line"><span class="big">{RATING}</span><span class="stars" aria-hidden="true">\u2605\u2605\u2605\u2605\u2605</span>'
           f'<span>{RATING_COUNT} Google reviews, as of {RATING_ASOF}. <a href="{GOOGLE_REVIEWS}" rel="noopener" target="_blank">Read or leave one on Google</a></span></div>'
           + review_block(REVIEWS, three=True))
    page("/reviews/", "Reviews | Southside Strong Junk Removal, Chicago Ridge",
         f"Read what customers say about Southside Strong Junk Removal in Chicago Ridge and the southwest suburbs: {RATING} stars on Google from {RATING_COUNT} reviews.",
         section("Every written review, newest first", rev, kicker="Google reviews", sub="Copied word for word from our Google Business Profile. Reviews with stars but no text are counted in the rating and not shown here.") + cta_band(),
         trail=[("Home", "/"), ("Reviews", "/reviews/")], active="/reviews/",
         hero=("What customers say", f"{RATING} stars on Google from {RATING_COUNT} reviews."))

def build_contact():
    opts = "".join(f"<option>{esc(t)}</option>" for _, t in sorted(T.WAVE1, key=lambda x: x[1])) + "<option>Chicago (Southwest Side)</option><option>Other town</option>"
    form = f"""<form class="estimate" data-phone="{PHONE_E164}" data-email="{EMAIL}">
<div class="row2"><div><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required></div>
<div><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div></div>
<div><label for="f-town">Town</label><select id="f-town" name="town"><option value="">Choose your town</option>{opts}</select></div>
<div><label for="f-items">What needs to go, and where is it?</label><textarea id="f-items" name="items" placeholder="Example: a sectional and a dresser in the basement, plus an old fridge in the garage" required></textarea></div>
<div class="how" role="radiogroup" aria-label="Best way to reach you"><label><input type="radio" name="how" value="text" checked> Text me</label><label><input type="radio" name="how" value="call"> Call me</label><label><input type="radio" name="how" value="email"> Email me</label></div>
<button class="btn btn-red" type="submit">Send my estimate request</button>
<p class="fine">On a phone this opens your texting app with your request filled in, so you can add photos. On a computer it opens your email. Nothing is stored on this website.</p>
<p class="fine done" hidden>Your message app should be open now. If it is not, call or text {PHONE}.</p>
</form>"""
    side = f"""<div class="card"><h3>Call or text</h3><p><a class="btn btn-red" href="{TEL}">{ico('phone')}{PHONE}</a></p><p><a class="btn btn-line" href="{SMS}">{ico('msg')}Text a photo</a></p>
<p>Email: <a href="mailto:{EMAIL}">{EMAIL}</a></p><p class="muted">Based in Chicago Ridge, IL 60415.</p></div>"""
    page("/contact/", "Free Junk Removal Estimate | Southside Strong, Chicago Ridge",
         f"Get a free junk removal estimate in Chicago Ridge and the southwest suburbs. Call or text {PHONE}, or send a photo of what needs to go.",
         f'<section class="band"><div class="wrap"><div class="two"><div>{form}</div><div>{side}</div></div></div></section>',
         trail=[("Home", "/"), ("Free estimate", "/contact/")], active="/contact/",
         hero=("Get a free estimate", "Tell us what needs to go. Photos help. We will get back to you with a price."))

GENERAL_FAQ = [
  ("How much does junk removal cost?", "<p>It depends on how much there is, what it is and how hard it is to get out. Text a photo to " + PHONE + " for a free, upfront price. See <a href=\"{u:/pricing/}\">how pricing works</a>.</p>"),
  ("Do I need to be home?", "<p>Not always. If the items are outside or in an open garage, tell us and we can work it out. For anything inside, someone needs to let us in.</p>"),
  ("Do you take things from inside the house?", "<p>Yes. Basements, attics, bedrooms, garages and yards. You do not need to carry anything out.</p>"),
  ("Will you take apart furniture that will not fit?", "<p>Yes. Taking a piece apart is often the safest way out, and it protects your walls and doorways.</p>"),
  ("Do you take appliances?", "<p>Yes: refrigerators, freezers, washers, dryers, stoves, water heaters and more. They need to be disconnected first. See <a href=\"{u:/appliance-removal/}\">appliance removal</a>.</p>"),
  ("Do you take hot tubs and pools?", "<p>Yes. See <a href=\"{u:/hot-tub-removal/}\">hot tub removal</a> and <a href=\"{u:/above-ground-pool-removal/}\">above-ground pool removal</a>.</p>"),
  ("What can't you take?", "<p>Household hazardous waste: wet paint, solvents, chemicals, motor oil, propane tanks, asbestos and medical waste. See <a href=\"{u:/what-we-take/}\">what we take</a>.</p>"),
  ("Are you licensed and insured?", "<p>Yes.</p>"),
  ("Do you work with landlords and businesses?", "<p>Yes. See <a href=\"{u:/commercial-junk-removal/}\">commercial junk removal</a>.</p>"),
  ("Which towns do you serve?", "<p>Chicago Ridge and the southwest suburbs, plus Chicago's Southwest Side. See the <a href=\"{u:/service-area/}\">service area</a>.</p>"),
]

def build_faq():
    page("/faq/", "Junk Removal FAQ | Southside Strong, Chicago Ridge, IL",
         "Answers to common junk removal questions: pricing, what we take, appliances, hot tubs, pools and the towns we serve around Chicago Ridge, IL.",
         section("Frequently asked questions", faq_html(GENERAL_FAQ)) + cta_band(),
         schema=[faq_schema(GENERAL_FAQ)], trail=[("Home", "/"), ("FAQ", "/faq/")],
         hero=("Junk removal questions, answered", "Still wondering about something? Call or text " + PHONE + "."))

def build_privacy():
    body = f"""<div class="prose"><p>This website does not use cookies, analytics or tracking scripts, and it does not store anything you type. The estimate form only fills in a text message or an email in your own app; nothing is sent until you press send there.</p>
<p>If you call, text or email us, we use your information to answer you and to schedule and do the job. We do not sell it. Questions: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>"""
    page("/privacy/", "Privacy | Southside Strong Junk Removal", "How the Southside Strong Junk Removal website handles your information: no cookies, no tracking, and nothing you type is stored on the site.",
         f'<section class="band"><div class="wrap">{body}</div></section>', trail=[("Home", "/"), ("Privacy", "/privacy/")],
         hero=("Privacy", "Short version: we do not track you."))

def build_404():
    page("/404.html", "Page not found | Southside Strong Junk Removal", "That page is not here.",
         section("That page is not here", f'<p>Try the <a href="{u("/")}">home page</a>, <a href="{u("/services/")}">services</a> or the <a href="{u("/service-area/")}">service area</a>, or call {PHONE}.</p>'),
         hero=("Page not found", "Nothing to haul here."))

# ---------------------------------------------------------------- write + gates
def visible(doc, main_only=True, drop_official=False):
    s = doc
    if drop_official:
        # Village and city rules are quoted from official pages; their words are not claims about the business.
        s = re.sub(r'(?is)<div class="fact">.*?</div>', " ", s)
        s = re.sub(r'(?is)<details><summary>[^<]*</summary><div class="a"><p>[^<]*</p>', "<details>", s)
    if main_only:
        m = re.search(r'<main id="main">(.*)</main>', s, re.S)
        s = m.group(1) if m else s
    s = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", s)
    s = re.sub(r"(?is)<blockquote class=\"review\".*?</blockquote>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()

def write_all():
    keep = {".git", "assets", "content", "build.py", "README.md", "CNAME", ".nojekyll", "__pycache__", "tools"}
    for name in os.listdir(HERE):
        if name in keep:
            continue
        p = os.path.join(HERE, name)
        if os.path.isdir(p) and os.path.exists(os.path.join(p, "index.html")):
            shutil.rmtree(p)
        elif name in ("index.html", "404.html", "sitemap.xml", "robots.txt"):
            os.remove(p)
    for path, doc in PAGES.items():
        out = os.path.join(HERE, "404.html") if path == "/404.html" else os.path.join(HERE, path.strip("/"), "index.html") if path != "/" else os.path.join(HERE, "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(doc)
    urls = [p for p in PAGES if p != "/404.html"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{absu(p)}</loc><lastmod>{date.today().isoformat()}</lastmod></url>\n" for p in urls) + "</urlset>\n"
    open(os.path.join(HERE, "sitemap.xml"), "w").write(sm)
    open(os.path.join(HERE, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {absu('/sitemap.xml')}\n")
    open(os.path.join(HERE, ".nojekyll"), "w").write("")

def ngrams(text, n=5):
    w = re.findall(r"[a-z0-9']+", text.lower())
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}

def gates():
    fails, warns = [], []
    for path, doc in PAGES.items():
        if re.search("[\u2013\u2014]|&mdash;|&ndash;|&#821[12];", doc):
            fails.append(f"{path}: em or en dash")
        if re.search(r"j\s*-?\s*dog", doc, re.I):
            fails.append(f"{path}: the old franchise name appears")
        own = visible(doc, drop_official=True)
        for bad in (r"same[- ]day", r"guarantee", r"\bbonded\b", r"certified", r"veteran", r"#1\b", r"number one", r"cheapest", r"lowest price", r"24/7", r"\bbest\b", r"eco-friendly"):
            if re.search(bad, own, re.I):
                fails.append(f"{path}: claim word outside customer quotes: {bad}")
        for uk in (r"colour", r"favour", r"organis", r"recognis", r"\bcentre\b", r"licence", r"neighbour", r"cheque"):
            if re.search(uk, own, re.I):
                fails.append(f"{path}: UK spelling {uk}")
        if len(re.findall(r"<h1\b", doc)) != 1:
            fails.append(f"{path}: needs exactly one h1")
        for href in re.findall(r'href="(' + re.escape(BASE) + r'/[^"#?]*)', doc):
            rel = href[len(BASE):]
            target = os.path.join(HERE, rel.strip("/"), "index.html") if rel.endswith("/") else os.path.join(HERE, rel.strip("/"))
            if rel != "/" and rel not in PAGES and not os.path.exists(target) and not rel.startswith("/assets/"):
                fails.append(f"{path}: broken internal link {rel}")
        if re.search(r"\{(u|fact|reviews|reviewcards|event|donations):", doc):
            fails.append(f"{path}: unfilled placeholder")
        t, d = META[path]["title"], META[path]["desc"]
        if len(t) > 65: warns.append(f"{path}: title {len(t)} chars")
        if not 110 <= len(d) <= 160 and path != "/404.html": warns.append(f"{path}: description {len(d)} chars")
    pend = [k for k, v in FACTS.items() if v["status"] != "verified"]
    if pend:
        (fails if not NOINDEX else warns).append(f"facts not yet verified: {', '.join(pend)}")
    # Town page overlap (5-gram Jaccard over the main column, customer quotes excluded).
    town_paths = [T.page_path(s) for s, _ in T.WAVE1] + [T.page_path("chicago")]
    grams = {p: ngrams(visible(PAGES[p])) for p in town_paths}
    worst = sorted(((len(grams[a] & grams[b]) / max(1, len(grams[a] | grams[b])), a, b)
                    for i, a in enumerate(town_paths) for b in town_paths[i + 1:]), reverse=True)
    svc_paths = [f"/{s['slug']}/" for s in SERVICES]
    sg = {p: ngrams(visible(PAGES[p])) for p in svc_paths}
    sworst = max((len(sg[a] & sg[b]) / max(1, len(sg[a] | sg[b])), a, b) for i, a in enumerate(svc_paths) for b in svc_paths[i + 1:])
    return fails, warns, worst, sworst

if __name__ == "__main__":
    build_home(); build_services(); build_towns(); build_area(); build_about(); build_pricing(); build_what_we_take()
    build_reviews(); build_contact(); build_faq(); build_privacy(); build_404()
    write_all()
    fails, warns, worst, sworst = gates()
    verified_towns = sum(1 for s, _ in T.WAVE1 + [("chicago", "")] if TOWN_FACTS.get(s))
    print(f"pages: {len(PAGES)} | reviews shown: {len(REVIEWS)} | towns with fact files: {verified_towns} of {len(T.WAVE1) + 1} | noindex: {NOINDEX}")
    print(f"town overlap, worst pairs (limit 0.30): " + "; ".join(f"{a.strip('/')} ~ {b.strip('/')} {s:.3f}" for s, a, b in worst[:3]))
    print(f"service overlap, worst pair: {sworst[1].strip('/')} ~ {sworst[2].strip('/')} {sworst[0]:.3f}")
    if worst and worst[0][0] > 0.30:
        fails.append(f"town pages too alike: {worst[0][1]} ~ {worst[0][2]} {worst[0][0]:.3f}")
    for w in warns: print("warn:", w)
    for f in fails: print("FAIL:", f)
    sys.exit(1 if fails else 0)
