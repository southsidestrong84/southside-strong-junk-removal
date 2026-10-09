"""State and federal rules quoted on the service pages, from research/FACTS-VERIFIED.md (every statement
traced to an opened page with the sentence quoted there; five of them re-checked against the live pages
on 2026-10-09). `status` is "verified" once that is true. build.py refuses to drop noindex while any entry
is "pending". `until` hides a dated item after that day. Text is plain-language; `sources` are (label, url)."""

SRC = {
  "epa608": ("US EPA: Section 608 safe disposal requirements", "https://www.epa.gov/section608/stationary-refrigeration-safe-disposal-requirements"),
  "white_goods": ("Illinois law: 415 ILCS 5/22.28 (white goods)", "https://www.ilga.gov/Documents/legislation/ilcs/documents/041500050K22.28.htm"),
  "ced_ban": ("Illinois law: 415 ILCS 151/1-83 (electronics landfill ban)", "https://www.ilga.gov/ftp/ILCS/Ch%200415/Act%200151/041501510K1-83.html"),
  "iepa_e": ("Illinois EPA: electronics recycling", "https://epa.illinois.gov/topics/waste-management/materials-management/electronics-recycling1.html"),
  "iepa_e_faq": ("Illinois EPA: electronics recycling FAQ", "https://epa.illinois.gov/topics/waste-management/materials-management/electronics-recycling1/faqs.html"),
  "charm": ("Cook County: CHaRM recycling center", "https://www.cookcountyil.gov/CHaRMCenter"),
  "landscape": ("Illinois law: 415 ILCS 5/22.22 (landscape waste)", "https://www.ilga.gov/Documents/legislation/ilcs/documents/041500050K22.22.htm"),
  "mrc": ("Mattress Recycling Council FAQ", "https://byebyemattress.com/faq/"),
  "angi": ("Angi: How much does junk removal cost? (2026 data)", "https://www.angi.com/articles/how-much-does-junk-removal-cost.htm"),
  "iepa_hhw": ("Illinois EPA: household hazardous waste collections", "https://epa.illinois.gov/topics/waste-management/waste-disposal/household-hazardous-waste/collections.html"),
  "iepa_hhw_main": ("Illinois EPA: household hazardous waste", "https://epa.illinois.gov/topics/waste-management/waste-disposal/household-hazardous-waste.html"),
  "cook_green": ("Cook County Green Guide", "https://www.cookcountyil.gov/content/green-guide-library"),
  "chi_hccrf": ("City of Chicago: Household Chemicals & Computer Recycling Facility", "https://www.chicago.gov/city/en/depts/env/supp_info/environmental-permitting-and-inspection/hccrf.html"),
}

FACTS = {
  "appliance_rules": {
    "status": "verified",
    "html": """<p>Household refrigerators, freezers and window air conditioners usually still hold their refrigerant when they are thrown out. Federal rules make the last stop in the disposal chain, such as a scrap metal recycler or a landfill, responsible for making sure that refrigerant is recovered first. Illinois law adds that nobody may collect appliances for landfill disposal until the "white good components" are removed: refrigerant, mercury switches and parts that may contain PCBs.</p>
<p>That is why an old fridge cannot ride along with the garbage. We take appliances where they can be handled properly.</p>""",
    "sources": [SRC["epa608"], SRC["white_goods"]],
  },
  "electronics_rules": {
    "status": "verified",
    "html": """<p>In Illinois it is illegal to throw TVs, computers, monitors, printers and a list of other electronics in the trash. State law bans them from landfills, and Illinois EPA's current list, effective January 1, 2026, also covers home audio such as speakers, stereos and amps. The ban applies to businesses as well as households. These devices have to be recycled instead.</p>
<p>If you would rather drop electronics off yourself, Cook County's CHaRM recycling center at 15800 State St. in South Holland takes TVs, monitors and other electronics from residential customers, and many towns run their own collection, listed on our town pages where we could confirm it.</p>""",
    "sources": [SRC["iepa_e"], SRC["iepa_e_faq"], SRC["ced_ban"], SRC["charm"]],
  },
  "yard_rules": {
    "status": "verified",
    "html": """<p>Since July 1, 1990, Illinois law has kept landscape waste (leaves, grass clippings and brush) out of landfill-bound garbage. Yard waste is collected separately, and each town sets its own season and bag or sticker rules. Your town's rules are on its page in our <a href="{u:/service-area/}">service area</a> where we could confirm them. When the pile is bigger than a few bags, or it is mixed with fencing, a swing set or other junk, we haul the whole thing in one trip.</p>""",
    "sources": [SRC["landscape"]],
  },
  "debris_rules": {
    "status": "verified",
    "html": """<p>Whether your regular garbage service takes remodeling debris depends on your town and your hauler. Where we could confirm the rule, it is on your town's page in our <a href="{u:/service-area/}">service area</a>.</p>""",
    "sources": [],
  },
  "mattress_rules": {
    "status": "verified",
    "html": """<p>Illinois has no mattress recycling law. According to the Mattress Recycling Council, only California, Connecticut, Oregon and Rhode Island have one. Cook County's CHaRM recycling center lists mattresses as not accepted.</p>""",
    "sources": [SRC["mrc"], SRC["charm"]],
  },
  "pricing_national": {
    "status": "verified",
    "html": """<h2>What junk removal costs nationally</h2>
<p>For context only, these are national figures, not our prices. Angi's 2026 cost guide puts the national average for junk removal at $241, with most people paying between $133 and $372. It lists an eighth of a truckload at $75 to $125 and a full truckload at $600 to $800, and puts the average hot tub removal at $400. Your price depends on your job, so text us a photo for yours.</p>""",
    "sources": [SRC["angi"]],
  },
  "hhw_where": {
    "status": "verified",
    "html": """<h3>Where hazardous waste can go</h3>
<ul>
{event:iepa_lockport}
<li><b>Naperville household hazardous waste facility</b>, 156 Fort Hill Dr., Naperville. Saturdays and Sundays, 9 a.m. to 2 p.m. Cook County lists it as open to Illinois residents and suggests calling first: 630-420-6095.</li>
<li><b>Chicago residents:</b> the city's Household Chemicals &amp; Computer Recycling Facility, 1150 N. North Branch St. (Tuesday 7 a.m. to noon, Thursday 2 to 7 p.m., first Saturday of the month 8 a.m. to 3 p.m.). It does not take latex paint.</li>
<li><b>Latex paint:</b> the City of Chicago's advice is to dry it out with kitty litter, shredded paper or sawdust, then throw the dried paint and the can away.</li>
<li><b>Car batteries:</b> Illinois requires stores that sell lead-acid batteries to take used ones back, one for each new battery sold.</li>
</ul>""",
    "sources": [SRC["iepa_hhw"], SRC["iepa_hhw_main"], SRC["cook_green"], SRC["chi_hccrf"]],
    "events": {
      "iepa_lockport": {"until": "2026-10-31",
                        "html": "<li><b>Illinois EPA one-day collection, Saturday, October 31, 2026</b>, Shiloh Baptist Church, 18101 West Oak Avenue, Lockport, 8 a.m. to 3 p.m. Free and open to all Illinois residents; pre-registration is required. Explosives, propane tanks, fire extinguishers, smoke detectors, agricultural chemicals and business waste are not accepted.</li>"},
    },
  },
  "donation_list": {
    "status": "verified",
    "html": "{donations:all}",
    "sources": [("Habitat for Humanity ReStore locator", "https://www.habitat.org/local/restore?zip=60415"),
                ("The Salvation Army, Oak Lawn", "https://www.salvationarmyusa.org/il/oak-lawn/"),
                ("Goodwill locations", "https://www.goodwillgreatermc.org/locations/all-locations")],
  },
}
