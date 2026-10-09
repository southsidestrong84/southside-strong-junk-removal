"""Town pages, modeled on the Fair Value Investments and sellinheritedhouse.ai location pages, on a tighter
radius around Chicago Ridge.

Two rules carried over from the FVI build:
1. Every municipal fact is rendered from research/towns/facts-group*.json, verified with a quote from an
   official page. The copy never states a town rule the file does not hold.
2. The blind-guard rule: a fact we could not verify is not mentioned on its own. It joins one closing
   line that says to ask the village. A checked town and an unchecked one must not read alike.

Everything else on the page is either this town's Census numbers (research/towns/towns-census.json), its
distance from Chicago Ridge, or links. build.py measures 5-gram overlap across every pair of town pages."""
import hashlib, math

WAVE1 = [
  ("chicago-ridge", "Chicago Ridge"), ("oak-lawn", "Oak Lawn"), ("worth", "Worth"), ("palos-hills", "Palos Hills"),
  ("hickory-hills", "Hickory Hills"), ("bridgeview", "Bridgeview"), ("burbank", "Burbank"), ("evergreen-park", "Evergreen Park"),
  ("alsip", "Alsip"), ("merrionette-park", "Merrionette Park"), ("palos-heights", "Palos Heights"), ("justice", "Justice"),
  ("blue-island", "Blue Island"), ("crestwood", "Crestwood"), ("midlothian", "Midlothian"), ("oak-forest", "Oak Forest"),
  ("orland-park", "Orland Park"), ("tinley-park", "Tinley Park"), ("country-club-hills", "Country Club Hills"),
  ("calumet-city", "Calumet City"),
]
# Towns on the business's own Facebook service-area list that are past this radius. Listed on the hub, no page yet.
LISTED_FARTHER = ["Frankfort", "Lockport", "Bolingbrook", "Brookfield", "Joliet", "Naperville", "Aurora"]

FACT_ORDER = [
  ("hauler", "Who collects the garbage"),
  ("bulk_pickup", "Furniture and bulk items"),
  ("appliances", "Appliances and anything with refrigerant"),
  ("yard_waste", "Yard waste"),
  ("electronics", "TVs and electronics"),
  ("construction_debris", "Remodeling and construction debris"),
  ("hhw", "Paint, chemicals and other hazardous waste"),
]
TOPIC_WORDS = {"hauler": "who collects the garbage", "bulk_pickup": "bulk items", "appliances": "appliances",
               "yard_waste": "yard waste", "electronics": "electronics", "construction_debris": "remodeling debris",
               "hhw": "hazardous waste"}


def page_path(slug):
    return "/junk-removal-southwest-side-chicago/" if slug == "chicago" else f"/junk-removal-{slug}-il/"


def pick(seq, key, n):
    """Deterministic choice of n items, different per town, stable across builds."""
    order = sorted(range(len(seq)), key=lambda i: hashlib.sha1(f"{key}:{i}".encode()).hexdigest())
    return [seq[i] for i in order[:n]]


def usdate(iso):
    from datetime import date
    try:
        d = date.fromisoformat(iso)
        return d.strftime("%b ") + str(d.day) + d.strftime(", %Y")
    except Exception:
        return iso


def pct(x):
    return f"{round(x * 100)}%"


def glance_paragraphs(town, c, home):
    """Plain statements read straight off the Census numbers, plus a link where the number points at a service."""
    out = []
    y, pre60, sfd, own, old = c["median_year_built"], c["built_before_1960_share"], c["single_family_detached_share"], c["owner_occupied_share"], c["age_65_plus_share"]
    if y and y <= 1958:
        out.append(f"{town} has some of the oldest housing near us. The median home was built in {y}, and {pct(pre60)} of homes went up before 1960.")
    elif y and y <= 1968:
        out.append(f"The median home in {town} was built in {y}. About {pct(pre60)} of the town's homes are older than 1960.")
    elif y and y <= 1980:
        out.append(f"The median home in {town} dates to {y}, and only {pct(pre60)} of homes predate 1960.")
    elif y:
        out.append(f"{town} is newer than most of the towns around Chicago Ridge. The median home was built in {y}.")
    else:
        out.append(f"The Census does not publish a median build year for {town}, but {pct(pre60)} of its homes were built before 1960.")
    houses = round(c["housing_units"] * sfd / 100) * 100 if c.get("housing_units") and sfd else None
    if sfd and sfd >= 0.65 and houses:
        out.append(f"About {houses:,} of {town}'s homes are detached single-family houses ({pct(sfd)}). If yours has a garage or a basement that has been filling up for years, see <a href=\"{{u:/garage-cleanouts/}}\">garage cleanouts</a> and <a href=\"{{u:/basement-cleanouts/}}\">basement cleanouts</a>.")
    elif sfd and sfd < 0.45:
        out.append(f"Only {pct(sfd)} of {town}'s homes are detached houses; the rest are apartments, condos, townhomes and two-flats, where stairs, elevators and shared hallways shape how a job goes.")
    if own is not None and own < 0.6:
        out.append(f"About {pct(1 - own)} of occupied homes in {town} are rented. Landlords and property managers call us for move-outs and unit turnovers; see <a href=\"{{u:/commercial-junk-removal/}}\">commercial junk removal</a>.")
    if old is not None and old >= 0.2:
        out.append(f"{pct(old)} of {town} residents are 65 or older. If you are helping a parent downsize or clearing out a family home, see <a href=\"{{u:/estate-cleanouts/}}\">estate cleanouts</a>.")
    return out


def miles_between(a, b):
    R = 3958.8
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def compose(slug, town, census, facts, towns_meta, reviews, esc, phone, outlets, donations_html):
    """Returns dict(title, desc, h1, lede, sections[(h2, html)], faqs[(q, a)], nearby[(slug, town, miles)])."""
    is_home = slug == "chicago-ridge"
    is_chicago = slug == "chicago"
    c = census.get(town) if not is_chicago else None
    f = (facts or {}).get("facts", {})
    verified = {k: v for k, v in f.items() if isinstance(v, dict) and v.get("status") == "verified" and v.get("value")}
    unknown = [k for k, _ in FACT_ORDER if k not in verified]
    hauler = verified.get("hauler", {}).get("value")
    contact = (facts or {}).get("contact")
    caveat = (facts or {}).get("caveat")
    place = "Chicago's Southwest Side" if is_chicago else town
    in_place = "on Chicago's Southwest Side" if is_chicago else f"in {town}"
    service_of = "the City of Chicago's" if is_chicago else f"{town}'s"
    miles = 0 if is_home else (c["miles_from_chicago_ridge"] if c else None)

    if is_chicago:
        title = "Junk Removal Chicago, Southwest Side | Beverly & Morgan Park"
        desc = "Junk removal in Beverly, Mount Greenwood, Morgan Park and the rest of Chicago's Southwest Side, from a locally owned crew based in Chicago Ridge. Free estimates."
        h1 = "Junk removal on Chicago's Southwest Side"
        lede = ("Beverly, Mount Greenwood, Morgan Park and the neighborhoods around them are right next door to our base in "
                "Chicago Ridge. Our bio says it plainly: from Bridgeport to Beverly to the Burbs.")
    elif is_home:
        title = "Junk Removal in Chicago Ridge, IL | Southside Strong"
        desc = "Junk removal in Chicago Ridge, IL from a locally owned crew based right here. Furniture, appliances, cleanouts, hot tubs and pools. Free estimates."
        h1 = "Junk removal in Chicago Ridge, IL"
        lede = ("Chicago Ridge is home. Southside Strong is based here, so for most jobs in town we are only minutes away. "
                "Furniture, appliances, cleanouts, hot tubs, pools and light demolition, carried out from wherever they sit.")
    else:
        title = f"Junk Removal in {town}, IL | Southside Strong"
        desc = f"Junk removal in {town}, IL from a locally owned crew {miles:g} miles away in Chicago Ridge. Furniture, appliances, cleanouts, hot tubs and pools."
        h1 = f"Junk removal in {town}, IL"
        lede = (f"{town} is about {miles:g} miles from our base in Chicago Ridge. Furniture, appliances, cleanouts, hot tubs, "
                f"pools and light demolition, carried out from wherever they sit and hauled away.")
    if len(desc) > 158:
        desc = desc.replace(" Free estimates.", "")

    sections = []
    # 1. The town's own pickup rules, verified only.
    rule_cards = []
    for key, label in FACT_ORDER:
        v = verified.get(key)
        if not v:
            continue
        src = v.get("url", "")
        quote = (v.get("quote") or "").strip()
        q_html = f'<p class="note">Exact wording: &ldquo;{esc(quote)}&rdquo;</p>' if quote and len(quote) <= 400 else ""
        rule_cards.append(f'<div class="fact"><h3>{esc(label)}</h3><p>{esc(v["value"])}</p>{q_html}'
                          f'<p class="src">Source: <a href="{esc(src)}" rel="nofollow noopener" target="_blank">{esc(src.split("/")[2] if "//" in src else src)}</a>, checked {usdate(v.get("accessed", ""))}</p></div>')
    who = "the city" if is_chicago else "the village"
    if contact:
        ask = f"Ask {esc(contact)},"
    else:
        ask = f"Ask {who}"
    if rule_cards:
        intro = (f"<p>Before you pay anyone to haul something away, it is worth knowing what {service_of} regular garbage service will take. "
                 f"Here is what we could confirm on {who}'s own pages.</p>")
        tail = ""
        if unknown:
            topics = ", ".join(TOPIC_WORDS[k] for k in unknown)
            tail = f'<p class="note">We could not confirm {service_of} current rules on {topics}. {ask} before you set those out.</p>'
        who_card = ""
        if contact:
            pw = verified.get("public_works_contact", {})
            who_card = (f'<div class="fact"><h3>Who to call {esc("in Chicago" if is_chicago else in_place)}</h3><p>{esc(contact)}</p>'
                        + (f'<p class="src">Source: <a href="{esc(pw.get("url", ""))}" rel="nofollow noopener" target="_blank">{esc(pw.get("url", "").split("/")[2] if "//" in pw.get("url", "") else "")}</a>, checked {usdate(pw.get("accessed", ""))}</p>' if pw.get("url") else "")
                        + "</div>")
        cav = f'<p class="callout">{esc(caveat)}</p>' if caveat else ""
        close = "<p>More than the pickup allows, anything inside the house, hot tubs, pools, sheds and whole cleanouts: that is where we come in.</p>"
        sections.append((("What Chicago's city garbage pickup will take" if is_chicago else f"What {place}'s garbage pickup will take"), intro + cav + f'<div class="facts">{"".join(rule_cards)}{who_card}</div>' + tail + close))
    else:
        sections.append((f"Before you set it at the curb in {place}",
                         f"<p>We have not yet confirmed {place}'s rules for bulk items, appliances, yard waste and electronics. {ask} what the regular garbage service takes, and call us for anything it does not.</p>"))

    # 3. At a glance (Census).
    if c:
        rows = [("People", f'{c["population"]:,}'), ("Homes", f'{c["housing_units"]:,}'),
                ("Median year built", str(c["median_year_built"]) if c["median_year_built"] else "not published"),
                ("Homes built before 1960", pct(c["built_before_1960_share"])),
                ("Detached single-family homes", pct(c["single_family_detached_share"])),
                ("Owner-occupied homes", pct(c["owner_occupied_share"])),
                ("Residents 65 and older", pct(c["age_65_plus_share"])),
                ("Distance from our Chicago Ridge base", "home base" if is_home else f'about {c["miles_from_chicago_ridge"]:g} miles')]
        table = '<table class="glance"><tbody>' + "".join(f"<tr><th scope=\"row\">{esc(a)}</th><td>{esc(b)}</td></tr>" for a, b in rows) + "</tbody></table>"
        paras = "".join(f"<p>{p}</p>" for p in glance_paragraphs(town, c, None))
        sections.append((f"{town} at a glance", f'<div class="two"><div>{paras}</div><div>{table}<p class="note">Source: US Census Bureau, American Community Survey 2020 to 2024 5-year estimates. Distance is a straight line between town centers.</p></div></div>'))

    # 4. Where things can go: the two nearest verified donation drop-offs, by straight-line distance.
    origin = (c["lat"], c["lon"]) if c else (41.7406, -87.6853)   # Chicago: Beverly, near 95th and Western
    ranked = sorted(outlets, key=lambda o: miles_between(origin, (o["lat"], o["lon"])))[:2]
    dist = [miles_between(origin, (o["lat"], o["lon"])) for o in ranked]
    sections.append((f"Donating first? Closest drop-offs to {place}",
                     f"<p>If some of it is still good, you can donate it before we come. These are the two drop-off spots we could confirm closest to {place}:</p>"
                     + donations_html(ranked, dist)
                     + '<p>Paint, chemicals and propane tanks cannot go in a junk truck or a donation bin. See <a href="{u:/what-we-take/}">what we take</a> for where they can go.</p>'))

    # 5. Reviews: two, rotated per town. Never implies the reviewer lives in this town.
    chosen = pick(reviews, slug, 2)
    sections.append(("What customers say", "{reviewcards:" + ",".join(r["id"] for r in chosen) + "}"
                     + '<p><a href="{u:/reviews/}">Read all our Google reviews</a></p>'))

    # FAQs from verified facts first.
    faqs = []
    if "bulk_pickup" in verified:
        faqs.append((f"Will the garbage service pick up furniture {in_place}?",
                     f"<p>{esc(verified['bulk_pickup']['value'])}</p><p>For more than that, or for anything inside the house, call or text us at {phone}.</p>"))
    if "appliances" in verified:
        faqs.append((f"How do I get rid of an old refrigerator {in_place}?",
                     f"<p>{esc(verified['appliances']['value'])}</p><p>We can also carry it out from the kitchen, garage or basement and take it where appliances are handled properly.</p>"))
    if "yard_waste" in verified:
        faqs.append((f"How does yard waste pickup work {in_place}?", f"<p>{esc(verified['yard_waste']['value'])}</p>"))
    if "construction_debris" in verified:
        faqs.append((f"Can remodeling debris go out with the garbage {in_place}?",
                     f"<p>{esc(verified['construction_debris']['value'])}</p>"))
    if is_home:
        faqs.append(("Where are you located?", "<p>We are based in Chicago Ridge, IL 60415, and we work all over the southwest suburbs and Chicago's Southwest Side.</p>"))
    elif miles is not None:
        faqs.append((f"How far is {place} from you?", f"<p>About {miles:g} miles from our base in Chicago Ridge, measured as a straight line between town centers.</p>"))
    faqs.append((f"Do you give free estimates {in_place}?", f"<p>Yes. Call or text {phone}, or send a photo of what needs to go, and we will give you a price.</p>"))

    # Nearby towns with pages, by straight-line distance between town centers.
    nearby = []
    if c:
        import math
        def d(a, b):
            R = 3958.8
            la1, lo1, la2, lo2 = map(math.radians, (a["lat"], a["lon"], b["lat"], b["lon"]))
            h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
            return 2 * R * math.asin(math.sqrt(h))
        others = [(s, t, d(c, census[t])) for s, t in towns_meta if t != town and t in census]
        nearby = sorted(others, key=lambda x: x[2])[:6]
    else:
        nearby = [(s, t, None) for s, t in towns_meta if s in ("evergreen-park", "merrionette-park", "oak-lawn", "blue-island", "alsip", "chicago-ridge")]
    svc = []
    if c:
        if c["built_before_1960_share"] >= 0.3 or (c["median_year_built"] or 2000) <= 1966: svc.append(("basement-cleanouts", "Basement cleanouts"))
        if c["single_family_detached_share"] >= 0.6: svc.append(("garage-cleanouts", "Garage cleanouts"))
        if c["age_65_plus_share"] >= 0.18: svc.append(("estate-cleanouts", "Estate and whole-house cleanouts"))
        if c["owner_occupied_share"] < 0.65: svc.append(("commercial-junk-removal", "Landlord and commercial junk removal"))
        if (c["median_year_built"] or 0) >= 1975: svc.append(("hot-tub-removal", "Hot tub removal"))
    for extra in (("furniture-removal", "Furniture removal"), ("appliance-removal", "Appliance removal"), ("above-ground-pool-removal", "Above-ground pool removal")):
        if len(svc) < 5: svc.append(extra)
    return {"in_place": in_place, "services": svc, "title": title, "desc": desc, "h1": h1, "lede": lede, "sections": sections, "faqs": faqs, "nearby": nearby,
            "verified_count": len(verified), "place": place}
