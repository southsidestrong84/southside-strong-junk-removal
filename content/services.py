"""Service pages. Every claim about the business traces to its own words (Facebook bio, its current site)
or to its Google reviews. Rules and laws come from research/FACTS-VERIFIED.md; the `sources` on each
service list the pages a statement relies on. No prices, no same-day promise, no claims nobody made.

Fields: slug, name (nav/card), icon, card (one line), title (<= 60 chars), desc (meta), h1, lede,
body (list of (h2, html)), takes (what we haul), faqs [(q, a_html)], review_words (pick related reviews),
related (other service slugs)."""

SERVICES = [
  {
    "slug": "furniture-removal", "name": "Furniture removal", "icon": "sofa",
    "card": "Couches, sectionals, recliners, dressers, beds, desks. We take it apart if it won't fit through the door.",
    "title": "Furniture Removal in Chicago Ridge & Oak Lawn",
    "desc": "Couch, sectional and furniture removal in Chicago Ridge, Oak Lawn and the southwest suburbs. We carry it out, take it apart if needed, and clean up.",
    "h1": "Furniture removal, carried out from any room",
    "lede": "Old couch in the basement, a sectional that came in before the stairs were redone, a bedroom set nobody wants. We carry it out from wherever it sits, take it apart when that is the safer way out, and leave the room clean.",
    "body": [
      ("What we take", """<ul class="checks cols">
<li>Couches, loveseats and sleeper sofas</li><li>Sectionals and reclining sofas, including power recliners</li>
<li>Recliners and lift chairs</li><li>Dressers, chests and nightstands</li><li>Bed frames, headboards and bunk beds</li>
<li>Dining tables and chairs</li><li>Desks, file cabinets and office chairs</li><li>Entertainment centers and bookcases</li>
<li>Patio furniture</li><li>Cribs, toy chests and kids' furniture</li></ul>"""),
      ("Taking it apart beats taking off the door frame", """<p>A lot of furniture went into a house before a remodel, a new railing or a tighter stairwell. Reclining sofas with metal rails are the classic one. Instead of forcing it and gouging the walls, we take the piece apart and carry it out in sections.</p>
<p>One of our customers put it this way after we pulled a large leather reclining sofa and chair out of a tight space: Steve "took the time to disassemble" them first, which "made for an easier way to get it out of the house."</p>"""),
      ("Basements, attics and second floors", """<p>You do not have to drag anything to the curb. Tell us where it is: the basement rec room, a finished attic, a second-floor bedroom, the back of the garage. We bring the dollies and the straps, protect the corners on the way out, and sweep up when the room is empty.</p>"""),
      ("When the village pickup is not enough", """<p>Most towns around Chicago Ridge collect some bulk items with the weekly garbage, usually with limits on how many pieces and where they have to sit. That works for one chair at the curb. It does not work for a basement full of furniture, or for anyone who cannot carry a sleeper sofa up a flight of stairs. Check your own town's rules on our <a href="{u:/service-area/}">service area pages</a>, then call us for the rest.</p>"""),
    ],
    "faqs": [
      ("Do I need to move the furniture to the curb or garage first?", "<p>No. We pick it up where it is, inside or out. Just make sure there is a clear path, and point us to anything that needs extra care on the way out.</p>"),
      ("Can you take apart a sectional or a reclining sofa?", "<p>Yes. Taking a piece apart is often the safest way to get it out without damage, and it is part of the job, not an afterthought.</p>"),
      ("Do you take just one piece?", "<p>Yes. A single couch or a single mattress is a normal call. The estimate is free, so ask.</p>"),
    ],
    "review_words": ["sofa", "chair", "furniture", "disassemble", "walls", "floors"],
    "related": ["mattress-removal", "basement-cleanouts", "estate-cleanouts"],
  },
  {
    "slug": "appliance-removal", "name": "Appliance removal", "icon": "fridge",
    "card": "Refrigerators, freezers, washers, dryers, stoves and water heaters, hauled out and handled the right way.",
    "title": "Appliance Removal & Fridge Haul Away | Chicago Ridge",
    "desc": "Refrigerator, freezer, washer, dryer and stove removal in Chicago Ridge, Oak Lawn and the southwest suburbs, carried out from any floor and handled properly.",
    "h1": "Appliance removal: fridges, washers, dryers and more",
    "lede": "Old refrigerator in the garage, a washer and dryer that just got replaced, a freezer that died in the basement. Appliances are heavy, awkward and come with disposal rules. We carry them out and make sure they go where they are supposed to.",
    "body": [
      ("What we take", """<ul class="checks cols">
<li>Refrigerators and freezers, including chest freezers</li><li>Washers and dryers</li><li>Stoves, ranges and ovens</li>
<li>Dishwashers</li><li>Microwaves</li><li>Water heaters</li><li>Window air conditioners and dehumidifiers</li>
<li>Grills (empty the propane tank first)</li><li>Treadmills and exercise machines</li></ul>"""),
      ("Why a fridge is not just scrap metal", """{fact:appliance_rules}"""),
      ("Disconnecting first", """<p>We haul appliances that are already disconnected. If a gas range, a gas dryer or a hard-wired water heater is still hooked up, have a plumber or electrician shut it off and cap it before we arrive. Water lines on washers and fridges should be shut off and drained so nothing leaks on the way out.</p>"""),
      ("From the basement or the second floor", """<p>Basement chest freezers and second-floor laundry machines are where people get hurt. We bring the equipment to move them safely and protect floors and stairs on the way out.</p>"""),
    ],
    "faqs": [
      ("Do I need to defrost the freezer first?", "<p>Please do, the day before if you can. Empty it, unplug it and leave the door open so it drains. It keeps water off your floors on the way out.</p>"),
      ("Will my village pick up an old refrigerator?", "<p>Some towns do, often with a sticker, a fee or a phone call first, and some do not take items that hold refrigerant at all. Look up your town on our <a href=\"{u:/service-area/}\">service area pages</a> for the exact rule, or call us and we will take it from wherever it sits.</p>"),
    ],
    "review_words": ["appliance", "fridge", "refrigerator", "washer", "dryer"],
    "related": ["electronics-removal", "garage-cleanouts", "basement-cleanouts"],
  },
  {
    "slug": "mattress-removal", "name": "Mattress removal", "icon": "bed",
    "card": "Mattresses, box springs and bed frames, from any bedroom, carried out and hauled away.",
    "title": "Mattress & Box Spring Removal | Chicago Ridge, IL",
    "desc": "Mattress, box spring and bed frame removal in Chicago Ridge, Oak Lawn and the southwest suburbs. One mattress or a whole house, carried out and hauled away.",
    "h1": "Mattress and box spring removal",
    "lede": "A new mattress showed up and the old one is leaning in the hallway. Or you are clearing out a rental with a mattress in every room. Either way, we carry them out and haul them away.",
    "body": [
      ("What we take", """<ul class="checks cols">
<li>Mattresses of any size, including memory foam and pillow tops</li><li>Box springs and foundations</li>
<li>Adjustable bed bases</li><li>Bed frames, headboards and footboards</li><li>Bunk beds and daybeds</li><li>Futons and futon frames</li></ul>"""),
      ("Why mattresses are a hassle to get rid of", """<p>Mattresses are bulky, floppy and hard to carry down a staircase alone, and garbage programs often limit bulk items. Check your town's rule on our <a href="{u:/service-area/}">service area pages</a>, or skip the rules and let us carry it out.</p>
{fact:mattress_rules}"""),
      ("One mattress or a dozen", """<p>We take a single mattress, and we take a house full of them, from landlord turnovers with a bed in every unit to estate cleanouts where every bedroom needs to be emptied. Tell us how many and where they are, and we will give you a price before we start.</p>"""),
    ],
    "faqs": [
      ("Do you take a single mattress?", "<p>Yes. Call or text a photo and we will tell you the price.</p>"),
    ],
    "review_words": ["mattress", "bed"],
    "related": ["furniture-removal", "estate-cleanouts", "commercial-junk-removal"],
  },
  {
    "slug": "hot-tub-removal", "name": "Hot tub removal", "icon": "tub",
    "card": "Old hot tubs and spas cut down or hauled out whole, and the pad left clean.",
    "title": "Hot Tub & Spa Removal | Chicago Ridge & Oak Lawn",
    "desc": "Hot tub and spa removal in Chicago Ridge, Oak Lawn and the southwest suburbs. Cut down if it will not fit through the gate, hauled away, pad swept clean.",
    "h1": "Hot tub and spa removal",
    "lede": "A dead hot tub takes up half the patio and no garbage truck will touch it. We take it out, through the gate or in pieces, haul it away and leave the pad clean.",
    "body": [
      ("How hot tub removal works", """<ol>
<li><b>Power off first.</b> Have an electrician disconnect the spa at the panel and the disconnect box before we come. We do not do electrical work.</li>
<li><b>Drain it.</b> Most spas have a drain spout or can be pumped out. Drain it a day or two ahead if you can.</li>
<li><b>We remove it.</b> If it fits through the gate on a dolly, it goes out whole. If it does not, we cut it down into sections on site.</li>
<li><b>We clean up.</b> Steps, cover, cover lifter and the debris all go with us, and we sweep the pad.</li></ol>"""),
      ("What a hot tub is made of", """<p>A hot tub is a shell, a wooden or composite cabinet, a frame, pumps, a heater and a lot of foam insulation. It weighs hundreds of pounds empty and it does not fold. That is why village garbage programs do not take them and why most homeowners cannot move one alone.</p>"""),
      ("Getting the yard back", """<p>Once it is gone, the concrete pad or deck under it is ready for a grill, a fire pit or new pavers. If the deck around the spa is coming out too, we can take that as well. See <a href="{u:/light-demolition/}">light demolition</a>.</p>"""),
    ],
    "faqs": [
      ("Do I have to disconnect the power?", "<p>Yes. Have a licensed electrician disconnect it before we arrive. Safety first, and we do not touch live electrical.</p>"),
      ("Will you cut it up in my yard?", "<p>Only when it cannot come out in one piece. We clean up all the debris before we leave.</p>"),
    ],
    "review_words": ["hot tub", "spa"],
    "related": ["above-ground-pool-removal", "light-demolition", "yard-waste-removal"],
  },
  {
    "slug": "above-ground-pool-removal", "name": "Above-ground pool removal", "icon": "pool",
    "card": "Above-ground pools taken down, hauled away and the area cleaned up with no debris left.",
    "title": "Above-Ground Pool Removal | Chicago Ridge & Oak Lawn",
    "desc": "Above-ground pool removal in Chicago Ridge, Oak Lawn and the southwest suburbs. We take it down, haul away the walls, liner and frame, and clean up.",
    "h1": "Above-ground pool removal",
    "lede": "The pool has had its last summer. We take it down, haul away the walls, liner, frame, ladder and pump, and leave the area clean. One customer summed it up: the area \"was cleaned up with no debris left.\"",
    "body": [
      ("What comes out", """<ul class="checks cols">
<li>Steel or resin walls and top rails</li><li>Uprights and bottom track</li><li>Liner</li><li>Ladders and steps</li>
<li>Pump, filter and hoses</li><li>Pool decks and stairs around the pool (see <a href="{u:/light-demolition/}">light demolition</a>)</li></ul>"""),
      ("Before we come", """<p>Drain the pool. Many towns have rules on where pool water can go, so check with your village before you pump it into the street or a neighbor's yard. Shut off and unplug the pump, and have an electrician disconnect it if it is hard-wired.</p>"""),
      ("What customers said", """{reviews:pool}"""),
      ("After it is gone", """<p>You are left with a ring of bare ground and maybe some sand. We take the pool and its parts; regrading and seeding is a job for a landscaper, and we are happy to tell you when the area is clear so they can start.</p>"""),
    ],
    "faqs": [
      ("Do I need to drain it first?", "<p>Yes, please drain it before we arrive, and follow your village's rules on where the water can go.</p>"),
      ("Do you take the deck around the pool too?", "<p>We can. Tell us about it when you ask for the estimate so we plan the time and the truck space.</p>"),
    ],
    "review_words": ["pool"],
    "related": ["hot-tub-removal", "light-demolition", "yard-waste-removal"],
  },
  {
    "slug": "yard-waste-removal", "name": "Yard and outdoor cleanup", "icon": "leaf",
    "card": "Brush, branches, old fencing, swing sets and whatever has piled up behind the garage.",
    "title": "Yard Waste Removal & Outdoor Cleanup | Chicago Ridge",
    "desc": "Yard waste removal and outdoor cleanup in Chicago Ridge, Oak Lawn and nearby: brush, branches, old fencing, swing sets and backyard junk, hauled away.",
    "h1": "Yard waste removal and outdoor cleanup",
    "lede": "Brush piles, storm branches, a rotted fence, a swing set the kids outgrew and everything else that collected behind the garage. We clear it, load it and haul it away.",
    "body": [
      ("What we haul from yards", """<ul class="checks cols">
<li>Brush, branches and storm debris</li><li>Bagged leaves and yard waste</li><li>Old fencing and posts</li>
<li>Swing sets and playsets</li><li>Trampolines</li><li>Old sheds (see <a href="{u:/light-demolition/}">light demolition</a>)</li>
<li>Landscape timbers, pavers and edging</li><li>Outdoor furniture and grills</li></ul>"""),
      ("Swing sets and playsets", """<p>Wooden playsets are built to stay put. We take them apart, pull the hardware and haul the lumber, slide and canopy away. A customer in our reviews hired us to remove a swing set and called the whole thing "easy." That is the goal.</p>"""),
      ("Yard waste has its own rules", """{fact:yard_rules}"""),
    ],
    "faqs": [
      ("Do you take bagged leaves and grass?", "<p>Yes, as part of a cleanup. If all you have is a few bags of leaves in season, your village's yard waste program may be the cheaper route; check your town's page.</p>"),
      ("Can you take down a swing set?", "<p>Yes. We take it apart, haul it away and leave the area clean.</p>"),
    ],
    "review_words": ["swing set", "outside", "yard", "deck"],
    "related": ["light-demolition", "above-ground-pool-removal", "construction-debris-removal"],
  },
  {
    "slug": "light-demolition", "name": "Light demolition", "icon": "hammer",
    "card": "Sheds, decks, fences and kitchen or basement tear-outs, torn out and hauled away together.",
    "title": "Light Demolition: Sheds, Decks & Tear-Outs | Chicago Ridge",
    "desc": "Light demolition in Chicago Ridge, Oak Lawn and the southwest suburbs: sheds, decks, fences and kitchen or basement tear-outs, hauled away in one trip.",
    "h1": "Light demolition and tear-outs",
    "lede": "Some junk is attached. A rotted shed, an old deck, a fence line, the cabinets and paneling in a basement you are about to redo. We tear it out and haul it away in the same trip, so you are not paying one crew to demo and another to haul.",
    "body": [
      ("What we tear out", """<ul class="checks cols">
<li>Sheds (wood, metal and resin)</li><li>Decks and deck stairs</li><li>Fences</li><li>Kitchen cabinets and countertops</li>
<li>Basement paneling, drop ceilings and carpet</li><li>Old built-ins and shelving</li><li>Above-ground pool decks</li></ul>"""),
      ("What customers said", """{reviews:demo}"""),
      ("What light demolition is not", """<p>We do not take out load-bearing walls, structural framing, foundations, or anything that needs a structural permit or an engineer. Plumbing, gas and electrical need to be disconnected by licensed trades before we start. Some towns require a permit even to demolish a shed, so check with your village's building department first.</p>"""),
    ],
    "faqs": [
      ("Do I need a permit to take down a shed?", "<p>It depends on your town. Some villages require a demolition or accessory structure permit. Call your village's building department before the job, and we will work to whatever they require.</p>"),
      ("Do you haul away the debris too?", "<p>Yes. Tearing it out and hauling it away is one job, with one price.</p>"),
    ],
    "review_words": ["demo", "kitchen", "basement", "deck", "remodel"],
    "related": ["construction-debris-removal", "hot-tub-removal", "yard-waste-removal"],
  },
  {
    "slug": "construction-debris-removal", "name": "Construction debris removal", "icon": "debris",
    "card": "Scrap wood, drywall, cabinets, flooring and leftover materials from a remodel or project.",
    "title": "Construction Debris Removal | Chicago Ridge & Oak Lawn",
    "desc": "Remodel and construction debris removal in Chicago Ridge, Oak Lawn and nearby: scrap wood, drywall, cabinets and flooring, loaded and hauled away.",
    "h1": "Construction and remodel debris removal",
    "lede": "The project is done and the leftovers are not. Scrap lumber from the new deck, old drywall, torn-out cabinets, a pile of flooring in the garage. We load it and haul it away, no dumpster sitting in the driveway for a week.",
    "body": [
      ("What we haul", """<ul class="checks cols">
<li>Scrap lumber and deck boards</li><li>Drywall and plaster</li><li>Old cabinets, vanities and countertops</li>
<li>Carpet, pad, vinyl and laminate</li><li>Doors, windows and trim</li><li>Tile and small amounts of masonry</li>
<li>Packaging and leftover materials</li></ul>"""),
      ("A truck instead of a dumpster", """<p>A rented dumpster sits on your driveway for days, may need a permit on the street, and you do the loading. When we haul it, we do the loading and the debris leaves when we do. For small and medium projects that is often simpler.</p>
<p>One customer had us pick up scrap wood from a deck project and said the crew "arrived early, was very efficient, very communicative."</p>"""),
      ("Contractors and property managers", """<p>If you are a contractor, a landlord or a property manager with regular cleanup, call us about ongoing work. See <a href="{u:/commercial-junk-removal/}">commercial junk removal</a>.</p>"""),
      ("Construction debris and regular garbage", """{fact:debris_rules}"""),
    ],
    "faqs": [
      ("Can my garbage hauler take remodeling debris?", "<p>Usually only in small amounts, if at all, and the rules change from town to town. Check your town on our <a href=\"{u:/service-area/}\">service area pages</a>.</p>"),
      ("Do you take paint and solvents?", "<p>No. Wet paint, solvents and chemicals are household hazardous waste. See <a href=\"{u:/what-we-take/}\">what we take</a> for where they can go.</p>"),
    ],
    "review_words": ["scrap wood", "deck", "remodel", "demo", "construction"],
    "related": ["light-demolition", "commercial-junk-removal", "garage-cleanouts"],
  },
  {
    "slug": "garage-cleanouts", "name": "Garage cleanouts", "icon": "garage",
    "card": "Get the car back in the garage. We clear it out, shelf to shelf, and sweep the floor.",
    "title": "Garage Cleanouts in Chicago Ridge & Oak Lawn, IL",
    "desc": "Garage cleanouts in Chicago Ridge, Oak Lawn and the southwest suburbs. We sort with you, haul away the junk, and leave a swept floor so the car fits again.",
    "h1": "Garage cleanouts",
    "lede": "The car has not been in the garage in years. Old paint cans, a broken mower, boxes from the last move, a workbench nobody uses. We clear it out with you, haul the junk away and sweep the floor.",
    "body": [
      ("How a garage cleanout goes", """<ol>
<li><b>Walk through.</b> You show us what stays and what goes. Mark the keep pile or just tell us as we work.</li>
<li><b>We load.</b> We carry out everything that goes, including the heavy stuff: old freezers, mowers, workbenches, shelving.</li>
<li><b>We sweep.</b> When the junk is gone, the floor gets swept and you get your parking spot back.</li></ol>"""),
      ("What we take from garages", """<ul class="checks cols">
<li>Old mowers, snowblowers and tools</li><li>Shelving, cabinets and workbenches</li><li>Bikes, sports gear and toys</li>
<li>Old freezers and fridges</li><li>Boxes, bins and old storage</li><li>Tires (ask us first)</li><li>Scrap metal</li></ul>"""),
      ("What has to go another way", """<p>Garages collect the things we cannot put in a truck: half-full cans of paint, motor oil, pesticides, pool chemicals and propane tanks. Set them aside and see <a href="{u:/what-we-take/}">what we take</a> for where they can go. Everything else, we handle.</p>"""),
    ],
    "faqs": [
      ("Do I have to sort everything before you come?", "<p>No. Show us what stays. We can work through the rest with you on the spot.</p>"),
      ("Do you take gas mowers and snowblowers?", "<p>Yes. Drain the gas and oil first if you can, or tell us and we will plan for it.</p>"),
    ],
    "review_words": ["garage", "cleanup", "junk"],
    "related": ["basement-cleanouts", "estate-cleanouts", "yard-waste-removal"],
  },
  {
    "slug": "basement-cleanouts", "name": "Basement cleanouts", "icon": "stairs",
    "card": "Decades of storage carried up the stairs: furniture, boxes, old appliances and more.",
    "title": "Basement Cleanouts in Chicago Ridge & Oak Lawn, IL",
    "desc": "Basement cleanouts in Chicago Ridge, Oak Lawn and the southwest suburbs. We carry everything up the stairs, protect the walls and leave it swept.",
    "h1": "Basement cleanouts",
    "lede": "The basement is where everything goes when nobody knows what to do with it. Old furniture, a dead freezer, the boxes from three moves. Everything has to come up the stairs, and that is the part we do.",
    "body": [
      ("The stairs are the job", """<p>Basement stairs in a lot of older homes around here are steep and narrow, and some turn at the bottom. That is where walls get gouged and backs get hurt. We bring the right equipment, take furniture apart when it will not make the turn, and protect the walls and floors on the way up. One customer wrote that Steve "can remove junk without scratching walls or floors and he does not leave a mess."</p>"""),
      ("Wet basements and water damage", """<p>After a flood or a backup, soaked carpet, pad, boxes and furniture need to go fast before mold sets in. We haul the damaged contents and the torn-out carpet. Get your insurance adjuster's photos first if you plan to file a claim.</p>"""),
      ("Tear-outs before a remodel", """<p>Redoing the basement? We can tear out paneling, drop ceilings, carpet and old built-ins and haul it all away in one trip. See <a href="{u:/light-demolition/}">light demolition</a>. A customer had us do the demo on a kitchen and a basement, haul the leftover furniture and clean up the mess.</p>"""),
    ],
    "faqs": [
      ("Do you carry things up from the basement?", "<p>Yes. That is most of the job. You do not need to bring anything upstairs first.</p>"),
      ("Can you take water-damaged carpet and drywall?", "<p>Yes. Let us know about the water damage when you ask for the estimate.</p>"),
    ],
    "review_words": ["basement", "walls", "floors"],
    "related": ["garage-cleanouts", "light-demolition", "estate-cleanouts"],
  },
  {
    "slug": "estate-cleanouts", "name": "Estate and whole-house cleanouts", "icon": "house",
    "card": "Downsizing, a move, or a loved one's home. Room by room, at your pace, until it is empty.",
    "title": "Estate Cleanouts & Whole-House Cleanouts | Chicago Ridge",
    "desc": "Estate and whole-house cleanouts in Chicago Ridge, Oak Lawn and the southwest suburbs. Room by room, at your pace, and the house left broom clean.",
    "h1": "Estate cleanouts and whole-house cleanouts",
    "lede": "Clearing out a parent's home, getting a house ready to sell, or moving out of a place you lived in for forty years. It is a lot of stuff and usually a lot of feelings. We work room by room, keep what you are keeping safe, and leave the house broom clean.",
    "body": [
      ("How we work through a whole house", """<ol>
<li><b>You decide what stays.</b> Family takes what they want first. Mark the keep items, or put them in one room we will not touch.</li>
<li><b>We go room by room.</b> Furniture, closets, kitchen, basement, garage and yard. If we come across anything that looks important, like papers, photos or jewelry, we set it aside and tell you.</li>
<li><b>Broom clean.</b> When the last load leaves, the house is swept and ready for a realtor, an estate sale company, a buyer or the next family.</li></ol>"""),
      ("Working with realtors, executors and families out of town", """<p>If you are handling a house from out of state, or you are the executor juggling a dozen other tasks, we can work with your realtor or a family member on site. Tell us who has the keys and how you want to get updates.</p>"""),
      ("Heavy cleanouts", """<p>Some homes are much harder than a normal cleanout: years of accumulation, spoiled food, pests, or conditions that are not safe to live in. We handle those too, without judgment. One customer, cleaning out a client's home, called it "practically a health hazard" and said it "was done quickly." If the home has biohazards like human waste or needles, tell us up front so we can plan for the right help.</p>"""),
    ],
    "faqs": [
      ("Do I need to be there for the whole cleanout?", "<p>No. Many families walk through with us at the start, then let us work. We will call or text with questions and when we are done.</p>"),
      ("What happens to things that are still usable?", "<p>Ask us when you get your estimate. If you would rather donate items yourself first, our <a href=\"{u:/what-we-take/}\">what we take</a> page lists drop-off spots near Chicago Ridge.</p>"),
    ],
    "review_words": ["health", "client", "cleanup", "everything", "entire"],
    "related": ["basement-cleanouts", "garage-cleanouts", "furniture-removal"],
  },
  {
    "slug": "commercial-junk-removal", "name": "Commercial junk removal", "icon": "building",
    "card": "Businesses, landlords, property managers and contractors. Turnovers, office cleanouts and repeat work.",
    "title": "Commercial Junk Removal for Businesses & Landlords",
    "desc": "Commercial junk removal for businesses, landlords and property managers in Chicago Ridge, Oak Lawn and nearby: office cleanouts and unit turnovers.",
    "h1": "Commercial junk removal for businesses and landlords",
    "lede": "Office furniture from a move, a storefront getting ready to open, an apartment a tenant left full, leftovers from a renovation. Businesses, landlords and property managers use us for one-time cleanouts and repeat work.",
    "body": [
      ("A good fit for", """<ul class="checks cols">
<li>Landlords and property managers (unit turnovers, evictions, common areas)</li><li>Realtors getting a listing ready</li>
<li>Offices and storefronts (moves, closings, openings)</li><li>Contractors and remodelers (debris haul-away)</li>
</ul>"""),
      ("What customers said", """{reviews:commercial}"""),
      ("Scheduling around your business", """<p>Tell us your hours, your loading area and who has keys. We will schedule around customers and tenants and keep you posted from the first call to the last load.</p>"""),
    ],
    "faqs": [
      ("Do you do repeat pickups for property managers?", "<p>Yes. Call us to set up how you want turnovers handled.</p>"),
    ],
    "review_words": ["commercial", "business", "client", "remodeling", "multiple"],
    "related": ["construction-debris-removal", "estate-cleanouts", "furniture-removal"],
  },
  {
    "slug": "electronics-removal", "name": "TV and electronics removal", "icon": "tv",
    "card": "Old TVs, computers, monitors and printers kept out of the landfill, as Illinois law requires.",
    "title": "TV & Electronics Removal | Chicago Ridge & Oak Lawn",
    "desc": "TV, computer and electronics removal in Chicago Ridge, Oak Lawn and the southwest suburbs. Illinois bans these from landfills; we keep them out.",
    "h1": "TV and electronics removal",
    "lede": "Old tube TVs, flat screens with a cracked panel, a closet of dead computers and printers. In Illinois these cannot go in the garbage. We carry them out and keep them out of the landfill.",
    "body": [
      ("What we take", """<ul class="checks cols">
<li>Tube TVs and flat-screen TVs</li><li>Computers, laptops and monitors</li><li>Printers, fax machines and scanners</li>
<li>Game consoles and DVD players</li><li>Stereos and speakers</li><li>Cords, keyboards and accessories</li></ul>"""),
      ("Why electronics cannot go in the trash", """{fact:electronics_rules}"""),
      ("Your data", """<p>Wipe or remove hard drives from computers before we take them. If you are not sure how, pull the drive out and keep it; that is the surest way to protect your files.</p>"""),
    ],
    "faqs": [
      ("Will you take an old tube TV?", "<p>Yes. Old tube TVs are heavy and awkward, and they are exactly what people get stuck with. We carry them out.</p>"),
      ("Can I put a TV out with the garbage?", "<p>Not in Illinois. Covered electronics like TVs and monitors are banned from landfills. See the rule above, or check your town's electronics drop-off on our service area pages.</p>"),
    ],
    "review_words": ["tv", "electronics", "computer"],
    "related": ["appliance-removal", "garage-cleanouts", "estate-cleanouts"],
  },
]
