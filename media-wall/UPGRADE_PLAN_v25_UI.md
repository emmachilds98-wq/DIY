# v25 UI upgrade: Demma Home Improvements, option 1c "Room as map" (for the building agent)

Read `media-wall/HANDOFF.md` and `CLAUDE.md` first. This round changes the plan page (`src/build_viewer.py`, `src/room3d_page.py`, `src/room3d.js`) and the lighting presets everywhere (`src/scenes.py`, `src/diagrams.py`, `src/build_doc.py`, `src/shot3d.py`). Otherwise the plan PDF and build guide stay as they are.
Reference designs (Claude design project): `Demma Home.dc.html` option **1c**, `Room Tools.dc.html` (the Tools panel), `Plan Sheet.dc.html` (the sheets), `Current Plan Page.dc.html` (v24 as it is).

## 1. What Emma and Dave asked for
- A new app feel: "should not resemble the old build in design or formatting in any way", with all of the old data kept.
- Phone and laptop equally. **The 3D room is the home screen**, full screen, and everything else slides up over it.
- **One Tools button** holds every 3D control. No rows of buttons and sliders on the main page.
- Bright pastels (peach, mint, lilac, butter) on warm cream. No Card Room green or oak in the interface. The paints stay as choices in the room.
- Cheerful and bouncy: rounded shapes, and a small celebration when something is ticked off.
- Long text becomes cards with key facts and checklists; the full text goes behind "Read more".
- Questions are answered on the page with quick taps and photo buttons, not typing.
- Name: **Demma Home Improvements** ("Demma" on phones).
- **Three main lighting presets** instead of six scene buttons (section 6).

## 2. Ground rules
1. **Lose nothing.** Every piece of content, control, saved key and anchor in v24 has a home (section 5). The data modules stay as they are, apart from `scenes.py` (section 6).
2. **Keep the saved state:** the localStorage keys (`mw13-view`, `mw22-drawer`, `mw23-*`), the deck db paths (`answers/`, `tracker/`), tracker ids `t<sha>`, question ids and step numbers. Ticks and answers saved before the upgrade must still show.
3. **Keep room3d.js's hooks.** It binds to `data-view`, `data-site`, `data-dining`, `data-chairs`, `data-plants`, `data-seat`, `data-drawers`, `data-scene`, `data-lv`, `data-col`, `data-tog`, `data-quality`, `data-paint`, `data-decor`, `data-idea`, `data-sugg`, `data-suggall`, the `#r3d-*` ids and `aria-pressed`. The new buttons carry the same attributes, so only containers and styling change.
4. Back up `build_viewer.py`, `room3d_page.py`, `room3d.js`, `scenes.py`, `diagrams.py`, `build_doc.py` and `shot3d.py` as `*_v24_backup.py` / `room3d_v24_backup.js` first.
5. Text no smaller than 12px. Tap targets at least 44px on phones. Contrast 4.5:1 (ink on pastel passes; never white on pastel).

## 3. Design system (a new `STYLE` in build_viewer.py; `room3d_page.CSS` follows it)
- Page `#fbf6ec`, ink `#2b2638`, muted `#645d73` / `#4c4558`, soft fill `#f1ebde`, dashed rule `#e5dccb`. The room stage behind the canvas is `#0c0a10`.
- Pastels: `oklch(0.92 0.06 H)`. "On" fills: `oklch(0.8 0.11 H)`. Butter is `oklch(0.94 0.07 95)`. Badge red: `oklch(0.7 0.16 25)`. Tools button: `oklch(0.8 0.13 25)`.
- Hues: peach 50 · mint 165 · lilac 300 · butter 95 · sky 235 · pink 345 · coral 25 · apricot 70 · lime 125.
- Sections: Room coral · Plan lilac · Build peach · Buy mint · Ideas butter · Ask sky.
- Build parts: Prep butter · Network sky · Power & cables coral · Paint mint · Media wall lilac · Dining table apricot · Lighting lime · AV pink. Keep the `PARTS` names; only the colours in the page change. Leave the PDF's colours as they are.
- Tools tabs: Views sky · Layout peach · Lights butter · Look mint · Extras lilac.
- Type: **Fredoka** 500/600 for headings, numbers and buttons on the room; **Figtree** 400–700 for text. Icons: **Material Symbols Rounded**, filled. Remove Bricolage, Atkinson and Plex Mono.
- Shape: pills (999px) for buttons and chips; 22–32px radius for cards, sheets and popovers; no hairline borders. Floating things get `box-shadow: 0 14px 34px -12px #000a`.
- Motion: sheets use `transform` with `cubic-bezier(.3,1.25,.5,1)` .5s; hovers and switches use `cubic-bezier(.3,1.6,.5,1)`. Celebration: a dark pill toast ("Step 2 done! 11 to go", "Ticked off!", "Thanks! 12 left") with an 18-dot confetti burst (`@keyframes dmBurst` / `dmPop` in `Plan Sheet.dc.html`). Under `prefers-reduced-motion`, keep the toast and drop the burst and the springs.

## 4. The 1c layout
**Room stage:** the canvas fills `100dvh`; `3d_room.webp` is the poster while it loads. Remove the walk pad, the caption strip and the Reset/Full screen buttons on the canvas. Keep WASD/QE and drag.

**Brand pill** top left: a 2×2 grid of four pastel dots on an ink square (radius 14), then "Demma" (Fredoka 600 18px) over "Home Improvements" (Figtree 600 12px, muted). On phones show "Demma" only.

**Section rail.** On a laptop (≥ 900px) it's a vertical cream capsule on the left, centred: Room, Plan, Build, Buy, Ideas, Ask. Each is a 36px pastel circle icon with an 11.5px label; the active one gets the deeper fill. Ask shows a red badge with the number of questions still unanswered. On a phone it's a bottom bar: the Tools button (58px, radius 22) on the left, then Plan, Build, Buy, Ideas, Ask.

**Room stickers.** Six numbered pastel pills sit on the room, each tilted a degree or three:
1 The media wall (lilac) · 2 The PC side wall (sky) · 3 Chimney breast (pink) · 4 Dining table (peach) · 5 Window & plants (mint) · 6 Sofa & rug (butter).
- Each has a 3D anchor point in room coordinates (add `HOTSPOTS` to `room3d_page.py`, read from `geometry.py`: wall centre at TV height, PC shelf, breast centre at 120, table centre, plant stand, sofa seat). In `room3d.js`, project each one every frame the camera moves (`v.clone().project(camera)` → CSS `left/top`), hide any sticker behind the camera or outside the frame, and fade stickers that sit behind a wall (a raycast to the anchor, or a simple dot-product test against the wall's normal).
- Tapping a sticker opens a popover under it (290px, cream, radius 24, with a small arrow). It holds the name in Fredoka 19px, 2–3 fact chips in the sticker's colour (from `geometry`/`ideas`, e.g. "Flip-top, up to seven · Chair cupboard · Step 11 · £696–1,330"), **Open in the plan** (opens the Plan sheet at that chapter) and **Fly here** (moves the camera to the matching view: wall, pc, breast, dining, windowwall, sofa). On phones the popover becomes a card above the bottom bar.
- Stickers hide while Edit room is on, and while a sheet or the Tools panel is open on phones.

**Tools.** On a laptop, a cream pill at the bottom centre with "Tools" (`tune` icon; it turns into `close` when open). Opening it shows five round pastel bubbles beside it (Views, Layout, Lights, Look, Extras) and an Edit bubble; the chosen tab's panel floats above (430px, radius 30, max-height 560, scrolls). On a phone the bubble row sits above the bottom bar and the panel is a card above it, leaving the top half of the room in view. Panel contents are in section 5. **Edit room** keeps the existing editbar, add list and selection panel over the canvas, restyled as cream pills.

**Sheets.** Plan, Build, Buy, Ideas and Ask slide up over the room. On a laptop the sheet fills the space right of the rail with a 16px inset and radius 32; on a phone it's full width under the status bar. Each has a close button; swipe down closes it on phones, and Esc closes it on a laptop. Focus is trapped while it's open. Each sheet has its own hash (`#plan`, `#build`, `#buy`, `#ideas`, `#questions`, plus the existing `#step-N`, `#q-<id>`, `#ph-N`) and Back closes it. Wire the old `data-go`, `data-step`, `data-phase` and `data-find` links to open the right sheet. "See it in 3D" buttons (`data-r3d`) close the sheet and apply the view.

## 5. Where everything goes (v24 → 1c)
| v24 | 1c |
|---|---|
| Header, page looks, Larger text, GitHub Pages link | Brand pill. Skins and Larger text are removed (they're design choices that are no longer needed). The Pages / Claude deck note moves to the bottom of the Plan sheet's Downloads |
| Overview dashboard | Plan sheet opens on "Evening, Emma & Dave": three progress rings (build, buy list, answers), the **Up next** step with a Done button, the two table places as image cards with + / – chips, and "What changed" folded |
| How the build runs, The room text | Build sheet (the list itself); The room → the Plan sheet's first chapter |
| Room in 3D + its 24-picture gallery | The home screen; the gallery goes under Tools → Views → "HD pictures" |
| Drawn views (render viewer, paints, key, measurements, lightbox, heights, counts) | Plan sheet → "Drawn views" chapter |
| Ideas tab (ideas, suggestions, decor) | Ideas sheet: four image cards, small ideas, the 12 suggestions as toggle chips (they switch the room too), decor |
| Media wall, Dining table (incl. chairs card), Paint & light, Network & power | Plan sheet chapters (10 pastel tiles). Each opens on key facts pulled from `geometry` (e.g. the heights list); "Read the full chapter" shows the `plan_sections()` HTML untouched, with the contents sidebar kept inside it |
| Build steps | Build sheet: 13-segment progress bar in part colours, part filter chips, steps as rows with a round 44px tick. The next not-done step is open. "Read the full step" shows need_html, drawings, full_html, the check and see-also. Keep STEP_JS (one open, Next step, Show all). Cutting list with Copy as text; Guide rules, time, tools, techniques and pitfalls under "Before you start" |
| Buy & costs | Buy sheet: four tiles, filter (Everything / Still to buy / Jobs only), 10 phase rows with low/high bars in part colours, each opening to its items with tick and Paid £. "Already owned" note |
| Questions | Ask sheet (section 7) |
| Checks & sources, Downloads, footer | Plan sheet: "Fit proof" chapter (summary pills, zones, Show only tight and to-check, sources, options set aside, earlier rounds) and a "Downloads" chapter |
| 3D drawers: Views | Tools → Views: the 13 cameras in a 2-column grid of pastel chips, Save as HD picture (3840 × 2160), HD pictures gallery, a walk hint |
| Layout | Tools → Layout: table place, flip-top, chairs, plant/vinyl layout, fold-down seat, drawers (pill rows, ink when on) |
| Lights | Tools → Lights (section 6) |
| Look | Tools → Look: five paint swatches (46px circles: Card Room, Sage, Treron, Deep green, Any colour) and the five decor rows |
| Extras | Tools → Extras: Your picks (count, cost, Copy as a note, Save for the next round), ideas, suggestions, All on / All off |
| Edit room, Reset, Full screen | The Edit bubble in the Tools row; Reset view and Full screen at the foot of the Tools panel |

## 6. Lighting: three main presets
Emma's note: the presets aren't great. Six buttons (General, TV night, Dinner, Records, Everyday evening, Daytime) mix three different things: moods, an activity that depends on the table, and the time of day. Split them like this:

**Three presets**, shown as three big tiles (Lights tab, and the light switch in the room):

| Preset | Replaces | strip | uprights | bias | bar1 | bar2 | lamp | Colour |
|---|---|---|---|---|---|---|---|---|
| **Bright** (`bright`) | General + Everyday evening | 70 | 50 | 0 | 60 | 60 | 50 | bars warm white 3000 K, every head straight down |
| **Cosy** (`cosy`) | Records + low evenings | 20 | 55 | 0 | 45 | 30 | 75 | bars 2700 K, lamp's three colour bulbs on (green, pink, purple) |
| **Film** (`film`) | TV night | 10 | 15 | 100 | 0 | 10 | 60 | bias light cool white behind the TV, lamp low |

**Two automatic rules** replace the other buttons:
- **Table open → dinner light.** When the flip-top is open for four or six (`S.dining !== "folded"`), on top of whichever preset is on, bar 2 goes to at least 80, bar 1 to at most 15 and the TV bias light goes off. Show it as a line under the tiles: "The table's open, so bar 2 lights it."
- **Time of day is its own switch** (Evening / Daytime) in the Lights tab, not a preset. Daytime is the old `day` sun and window light, and it works with any preset.

**Fine-tune each light** stays folded under the tiles: the master slider, six sliders and the colour pickers. Moving a slider marks the tile "Bright · adjusted"; tapping the tile again resets it.

**In code:**
- `scenes.py`: replace `SCENES` with the three presets above, in the same tuple shape `(key, name, description, levels, notes)` so every reader keeps working. Add `TABLE_BOOST = {"bar2_min": 80, "bar1_max": 15, "bias": 0}` and `TOD = [("evening", "Evening"), ("day", "Daytime")]`. Move the old five to `SCENES_V24` with a comment (for the appendix only).
- Notes for each preset (3 lines each, in the existing voice):
  - Bright: "All eight heads straight down, spread a little along each bar, so the pools overlap." / "The ceiling strip and the uprights fill the edges; the lamp adds a low warm layer." / "Turn the strip down first as the evening goes on: it's the flattest light in the room."
  - Cosy: "Bar 1's pink head on the turntable and the Series X, blue on the record ledge." / "The uprights' grooves up, washing the wall either side of the TV." / "The lamp up for reading sleeves on the sofa; the ceiling strip nearly off."
  - Film: "Bar 1 off: its heads hang in front of the screen, and even tilted away they'd catch it." / "The bias light and your red lamp do the work." / "Bar 2 just glowing on the framed LPs, so the far end of the room isn't a black hole."
- `room3d.js`: `data-scene` takes `bright | cosy | film`; apply TABLE_BOOST whenever the dining state changes; add `data-tod="evening|day"`. Map saved old scene keys on load: general/everyday → bright, records → cosy, tv → film, dinner → bright plus the table boost, day → bright with `tod=day`.
- Plan sheet → Paint & light chapter: the three presets as cards with their level tables and notes, then the two rules.
- **The plan PDF follows now (Emma agreed):**
  - `diagrams.light_scene(k)` draws the three presets, plus one extra drawing, `light_scene("bright", table=True)`, that shows the table boost over the open table.
  - Plan section 8 ("Lighting scenes", the `<!--scenes-->` block in `build_doc.py`): three scene pages instead of five. Each has its drawing, its level table (from `level_word()`) and its notes. Add a short "Two rules" box (table open → bar 2; day/evening is a switch).
  - Step 12 in the build guide: "set the scenes in the app" lists the three presets and the table rule.
  - Search `build_doc.py`, `HANDOFF.md` and `README.md` for "TV night", "Dinner", "Records", "Everyday evening" and "General" and update every mention. Keep the old names only in the appendix ("Options we set aside: the five scenes of v13.7–v24").
  - `shot3d.py`: the stills named after scenes become `bright`, `cosy` and `film` ("everyday evening" → bright, "records" → cosy, "TV night" → film, "dinner" → bright with the table open). Regenerate the stills and rename the HD files in `out/` to match.

## 7. Questions with quick taps
Add an optional `opts` field to each entry in `questions.py`, used by the page only; the PDF ignores it. Each is a list of rows: `(label or None, [choices])`. A choice starting "Add a photo" shows the `.upl` upload again (it's still in the DOM, just hidden). The answer is saved as plain text in the same `answers/<id>` record, e.g. "Cupboard: For six, 31 deep · Behind the top: No · Fold-down seat: Yes". Each card turns its pastel colour once answered; there's a counter and a gradient progress bar; "Why we ask" folds the why and how text; Copy all answers stays. Suggested choices are in `Plan Sheet.dc.html` (`QS`). Check the wording with Emma when you show it.

## 8. Order of work
1. Backups, then the tokens and fonts in `STYLE`. Remove the header, skins and tab bar.
2. The full-screen stage, brand pill and section rail / bottom bar.
3. The Tools pill, bubbles and panel, rebuilt from `room3d_page.controls()` with the same `data-*` hooks. Check that every v24 control still drives the room.
4. The lighting presets and rules (section 6).
5. The sheet component (hash, Back, Esc, swipe, focus), then the Plan opening view.
6. Build, Buy, Ask, Ideas, then the Plan chapters with Read more.
7. Stickers: `HOTSPOTS`, projection, occlusion fade, popover, Fly here.
8. The celebration toast and confetti, and the reduced-motion version.
9. The text pass from the optimisation plan: Network's Part P note, the paint tab's scenes and the plant stand become short lists.
10. QA at 390 × 844 and 1280 × 800 (Chrome, Safari iOS):
    - Every control from the v22 drawers works.
    - Old ticks, paid amounts and answers still show.
    - Every v24 `id=` and `data-` key still exists in the new page (grep the v24 `index.html` against v25).
    - The stickers follow the camera and hide behind walls.
    - The sheets work with the keyboard and a screen reader.
    - Contrast passes.
    - Then the usual ship: `make_images.py`, `export3d.py`, `shot3d.py`, `build_doc.py`, `build_viewer.py`; upload new art to the deck's asset store; update HANDOFF and README ("New in v25"); PR into `main`; publish the deck.

## 9. Key facts for each Plan chapter
Each chapter tile opens on 4–6 facts as pastel chips or a small list, then "Read the full chapter". Build every number from `geometry.py`, `fit.py`, `build_doc.py` and `ideas.py` (never type them in), so they follow the next round.

| Chapter | Facts (with the source to read them from) |
|---|---|
| The room | ceiling `G.CEIL` (235) · alcove 186 × 38 · door hinged on the breast side, opens in · straight stair flight rising towards the door · window ledge 25 (22 reveal + 3 nose) · soft grey carpet |
| The media wall | the heights list (`G.CEIL`, `G.HIGH_TOP`, `G.LEDGE_TOP`, `G.FOLDED_TOP`, `G.RZ_SHELF_TOP`, 116.5 TV centre, 104 "now playing" ledge, `G.WORKTOP`, `G.PLINTH`) · LG C6 55" on its stand · artisan oak in Card Room Green · steps 6–10 |
| Records & turntable | ~`G.ALL_LPS` LPs: `G.WALL_LPS` face-out in the wall, `G.STAND_LPS` in the vinyl stand (70 × 32 × 78) · two snug LP crates (33 cm trough) in bay 3 · game drawers ~`48 + G.SLIM_GAMES` · "now playing" ledge · Series X shelf, lid opens to `G.LID_CLEAR_TO` |
| The side wall | one oak run sweeping out to the PC · PC shelf at `G.LEDGE_TOP` · leads through a brush grommet into conduit in the wall · warm LED strip underneath · step 10 |
| Oak joinery | the cutting list (Copy as text) · joints drawing · worktop step 7, uprights step 9 · Oak joinery phase £745–1,355 (`phase_data`) |
| The dining wall | flip-top gate-leg, 110 × 80 opening to 110 × 160 · four with room, six elbows-in, seven by the stairs · Häfele brackets, 500 kg a pair · folds under the shelf, top at `G.FOLDED_TOP` · chair cupboard for four (22 deep) or six (31 deep) · Dining wall £696–1,330 |
| Paint & light | Card Room Green No. 79 (chosen) and the three alternatives as swatches · the three presets · smart E14 bulbs in both bars, no dimmers · Paint £220–540, Lighting £288–795 |
| Network & power | Virgin Hub 5 in modem mode · three Deco X1500s · two TL-SG108 switches · Cat6 runs on step 3 · the electrics are your own job (like for like, not notifiable under Part P) with the stop-and-call list · the 10-gang feeds the PC |
| Drawn views | 5 views × 4 paints · numbered key · measurements overlay · full-size lightbox |
| Fit proof | `fit.counts()`: checks, fit, tight, to check on site, don't fit · "Show only tight and to-check" |
| Downloads | the plan PDF and the build guide PDF for v25 · every HD picture · the GitHub Pages and shared-deck links |

## 10. Decided
- Option 1c.
- Three lighting presets on the page **and** in the plan PDF this round.
- Light only: no dark mode or page looks this round.
- Questions with quick taps and photo buttons, saved to the same answer records.
