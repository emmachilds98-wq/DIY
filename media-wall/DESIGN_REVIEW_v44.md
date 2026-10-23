## Design critique: the plan page's Plan, Build and Buy sheets (phone, 390 wide, v43)

### Overall impression
The sheets have everything, warmly styled and well labelled. The biggest opportunity is **length and repetition**: Build runs about
19 screens of near-identical step cards, and Plan and Buy each say the same thing twice. You have to scroll past a lot before reaching
the thing you came for.

### Usability
| Finding | Severity | Recommendation |
|---|---|---|
| Build is ordered by work step (1–14), but you make one *thing* at a time; its buy list, cuts and steps sit in three places | 🔴 Critical | One card per thing you make (the guide's chapters), each with Buy · Cut · Build tabs; the jobs in their own smaller cards |
| Every step card has three buttons (Done, Open/Close, "Build day: this step on one screen"): 42 buttons before the cutting list | 🔴 Critical | One Done tick on each card's header; tap the card to open it; Build day only inside the open card |
| The merchant's whole cutting list is open at the bottom of Build (about 6 screens of table on a phone) | 🟡 Moderate | Close it by default under "For the timber merchant", with Copy |
| Plan says "what's next" twice (the next three cards, then "Up next" with its own Done) | 🟡 Moderate | Keep the next three; drop the Up next card |
| Plan still shows the 90 vs 80 table comparison, with two big pictures, though the 90 is decided | 🟡 Moderate | Drop it from Plan; it's one line in the options |
| Buy lists the costs by piece, then again by phase in build order; neither says how to make the piece | 🟡 Moderate | By piece first, each with How to make it; the build-order list (with ticks and Paid) in one fold below |
| The PDFs are only under Downloads at the bottom of the chapter grid | 🟢 Minor | One "Download the PDF" button at the top of Plan and of Build |

### Visual hierarchy
- **What draws the eye first:** on Plan, the greeting and the next three cards: correct. On Build, a row of tiny coloured dots and a
  chip row ("All parts", "Prep", "Network"…) before anything you can act on: not correct. On Buy, the totals: correct.
- **Reading flow:** Plan wanders: decisions, money, checks, up next, before/after, chapters, fit proof, downloads, then the table
  comparison. Build is a flat list with no grouping by what you're making.
- **Emphasis:** the step cards' Done circles and orange Open buttons carry the same weight on every card, so nothing stands out.

### Consistency
| Element | Issue | Recommendation |
|---|---|---|
| Buttons | The same action is styled three ways: pill "Open", text link "Open it", chip "Build day" | One primary button style per sheet; secondary actions as text links |
| Section heads | "Chapters", "Where the money goes" and "Cost overview" use different sizes | One heading size for sheet sections |
| Cost text | "£1,177–2,202" right-aligned in Buy, inline "£51–70 ·" in phases | Right-aligned cost on every card |

### Accessibility
- **Colour contrast:** pastel chapter cards with dark text pass. The grey meta text ("You · 2 h", "before step 2") on cream is borderline;
  darken it to the body's muted tone.
- **Touch targets:** the Done circles (about 36 px) and the "Open" pills are fine; the dot strip at the top of Build is decorative but
  looks tappable.
- **Text readability:** body at 15–16 px is good; the cutting list's 12 px table on a phone is hard to read (moving it into a fold
  helps).

### What works well
- Warm, consistent palette with a colour per part, carried from the room to the sheets.
- The plan home's next three cards: one action each, clearly labelled.
- Buy's cost overview by piece reads at a glance.

### Priority recommendations
1. **Build as one card per thing you make** (Buy · Cut · Build), the jobs separate, the merchant list folded. This takes Build from
   about 19 screens to about 4 closed.
2. **Remove the repeats:** Up next and the 90/80 comparison from Plan; the build-order list into a fold on Buy.
3. **Link the three:** How to make it from Buy and from a piece in the room straight to its Build card; one PDF button on Plan and
   Build.
