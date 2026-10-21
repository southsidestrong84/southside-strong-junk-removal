"""Job photos from the business's own Facebook page and Reels (Eddie, 2026-10-09: "use their logo and photos that you
found on their fb"). Captured from the page viewer, trimmed and converted in ../_source-photos (gitignored).
Edits: the swing set's family name sign is blurred; the attic shot is cropped.
Captions describe what the photo shows, never a town or a customer. Before and after shots are NOT pairs of the
same room, so they are never shown side by side as a pair."""

PHOTOS = {
  "garage-cleanout-before": {"alt": "Cluttered garage with ladders, a wheelbarrow and bags of junk before a cleanout", "cap": "Garage cleanout, before"},
  "basement-cleanout-before": {"alt": "Wood-paneled basement corner stacked with bins, boxes and an old neon sign", "cap": "Basement cleanout, before"},
  "room-cleanout-before": {"alt": "Spare room filled with boxes, bags and old belongings", "cap": "Whole-room cleanout, before"},
  "attic-cleanout-before": {"alt": "Attic floor covered in boxes and cardboard", "cap": "Attic cleanout, before"},
  "closet-cleanout-before": {"alt": "Closet packed with bins, clothes and boxes", "cap": "Closet cleanout, before"},
  "room-after-cleanout": {"alt": "Empty room with a bare plywood floor after a cleanout", "cap": "Room cleared out, after"},
  "remodel-debris-pile": {"alt": "Pile of broken drywall, lumber and remodel debris on a garage floor", "cap": "Remodel debris, before pickup"},
  "swing-set-before": {"alt": "Wooden swing set in a backyard", "cap": "A swing set job"},
  "dump-trailer-curbside": {"alt": "Southside Strong's black dump trailer parked at the curb on a city street", "cap": "Our dump trailer on a job"},
  "dump-trailer-sign": {"alt": "Southside Strong Junk Removal sign with the phone number (708) 247-6440 on the side of the trailer", "cap": "The sign on our trailer", "pos": "center 20%"},
  "dump-trailer-loaded": {"alt": "Inside the dump trailer, loaded with boards, boxes and household junk", "cap": "A load headed out"},
}

HOME_GALLERY = ["garage-cleanout-before", "dump-trailer-curbside", "basement-cleanout-before", "room-after-cleanout",
                "remodel-debris-pile", "dump-trailer-loaded", "room-cleanout-before", "swing-set-before"]
ABOUT_GALLERY = ["dump-trailer-sign", "dump-trailer-curbside", "dump-trailer-loaded", "room-after-cleanout"]
