# v46 upgrade plan: the room piece by piece, easy to read anywhere, balanced light

Client (24 Oct): "review design and info in there. Further upgrades the plans and build info to be more optimised for viewing in mobile
and pc. I want to be able to understand and read this easily from any view. With clear path of use as I go through. I think I don't
need step by step what item to do first ie cabinet then table then x then x but I need to be able to drill down into tasks for each piece
of the room when I click on them or look in the plans." And: "Lighting needs improving too, default view could balance lighting
throughout the room using all fixtures and making a good setting then optimise and upgrade settings. Do all other areas for review and
give me your plan then upgrade."

Starts from `main` at v45. The standing rules hold: the core plan gets the full build; options stay one line each; say less.

## What the review found (v45, phone 390 and PC 1280)

1. **The path runs on an order you don't need.** Plan's "Your next three" and Build's "Next" both point at "Step 1 of 14"; ticks live
   in a 14-step list. Things to make are cards, but you can't tick anything inside one.
2. **The room's three labels lead to the plan, not to the work.** Media wall, Dining wall and The sofa open a card with facts and "Open in
   the plan". The side wall and PC, the chimney breast and the window corner have no label. Tapping a piece (the cabinet, the PC)
   offers How to make it, but the pieces you fit (shelves, cabinets) mostly don't.
3. **The PC view wastes the screen.** Build and Plan are one narrow column in the middle of a wide sheet.
4. **The PDFs are A4 only**, with no clickable contents or bookmarks: hard to read on a phone and slow to find a piece on a PC.
5. **The default light is uneven.** In Cosy the rug and the middle of the floor are the brightest things in the room; the sofa, the
   window corner and the dining wall fall away. The glass case, the bar's LED and the PC glow sit outside every scene at one fixed level,
   so no setting uses all the fixtures.
6. **Light settings are six sliders and three presets**, with no way to make the whole room brighter or warmer in one move.

## 1. The room, piece by piece (no fixed order)

- **Places → pieces → tasks.** Six places in the room: the media wall, the side wall and PC, the chimney breast, the dining wall, the
  window corner, the sofa. Each place lists its pieces (for example the dining wall: the cabinet and table, the bar, your black shelf's
  boxes). Each piece opens one card.
- **A piece's card is its whole job**, in the same order every time: **Check** (what to measure first), **Buy** (its things, ticked as
  you buy), **Cut** (its parts drawn to scale) and **Build** (its tasks, each with a tick; tap a task for its numbered steps). A ring shows
  "5 of 12 done". Things the piece depends on (paint first, the socket before the base) show as one line at the top, not an order.
- **From the room:** each place has a label (six, tidy, hidden with Hide labels); tap a label for its pieces, tap a piece in 3D for its card.
- **From the plans:** Plan's home becomes "Your room": the six places with each piece's progress; Build is the same pieces and the jobs;
  Buy's pieces open their cards. "Next step" and the step list go; ticks are per task (your old step ticks carry over).

## 2. Easy to read on a phone and a PC

- **Phone:** one column, big ticks, the card's four parts as tabs that stay put while you scroll.
- **PC:** Build and Plan use the width: the pieces on the left, the open card on the right; Buy's lists in columns.
- **PDFs:** clickable contents and bookmarks in both, the guide grouped by place and piece (no order-of-work list), and a **phone
  edition** of each (a narrow page with bigger type) beside the A4 ones.

## 3. Light: balanced by default, every fixture used

- **A new default, Evening:** every fixture on and balanced: the ceiling strip, the uprights, the eight spot heads aimed across the
  room's zones, the lamp, and a new **Accents** layer (the glass case, the bar's LED, the PC glow; the cabinet and shelf lights when you
  add them). Tuned by measuring each zone's brightness in stills (the media wall, the sofa, the dining wall, the window corner, the
  stairs) so no zone is more than about three times another and nothing washes out.
- **Presets rechecked the same way:** Evening (default), Bright, Cosy, Film; the table rule keeps the oak from washing out.
- **Settings:** one **Brightness** and one **Warmth** slider for the whole room, then each fixture's slider under More. The plan's
  lighting section says the same.

## 4. Smaller fixes from the review

- The room's tip and the drawers' text checked against the text budget; Fly here and Open in the plan stay on each place's card.
- `qa.py` also checks that each piece's card opens from the room and from Plan, and that no text names the assistant.

## 5. Order

1. This plan, merged.
2. Section 3 (light), merged.
3. Section 1 and the phone/PC layout of section 2, merged.
4. The PDFs (section 2), rebuild, checks, HANDOFF, README, merged.
