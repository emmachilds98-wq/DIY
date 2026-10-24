# v46 upgrade plan: easier to read, and everything fitted, on a phone and a PC

Starts from `main` at v45. The client (24 Oct): "Review for further upgrades and ways we can make the information read easier and
clearer for understanding. Fitting everything correctly in mobile and pc views".

## 1. What the review found (every sheet and chapter at 390 and 1280)

- **Wide tables on a phone.** The fit proof (about 20 tables), the network, the lighting levels and the console sizes have 4–6
  columns; at 390 they squeeze to a few words a line and the right-hand columns scroll off sideways ("Spare", "Result" unseen).
- **Plan's chapter tiles on a phone:** eleven tiles one per row, about 3 screens before "The plan on a page".
- **Build on a PC:** the cards run one per row across the whole sheet, the Done tick far from the name.
- **A stale fact:** the media wall's heights still list "153.3 The table, folded" (the old fold-up table; the dining cabinet is 189).
- **Fine as they are:** Buy at both sizes, the laptop chapters, nothing off the right edge (`qa.py`).

## 2. The changes

- **Tables become cards on a phone:** under 600 px every table of four or more columns shows each row as a small card, its first
  column as the title and the others as "Size: …", "Space: …" lines, the result as its coloured chip. No sideways scrolling. The PC
  keeps the tables.
- **Chapter tiles two to a row on a phone**, shorter (icon beside the name), so all eleven fit in about one screen.
- **Build on a PC:** the cards two to a row (Things to make and Jobs); an open card spans the row.
- **The heights:** "153.3 The table, folded" becomes "189 The dining cabinet's top".
- **Checks:** before and after screenshots of every sheet and chapter at 390 and 1280, `qa.py`, `taptest.py`; how many phone screens
  each chapter takes, before and after, in HANDOFF.

## 3. Order

1. This plan, merged.
2. The changes, rebuild, checks, HANDOFF round 41, README, merged; the viewer republished.
