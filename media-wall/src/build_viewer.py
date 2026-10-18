"""Builds the interactive viewer page (v13): view × paint × key, plus the open questions (answers and photos saved for
both of you), a shared buy tracker, the fit proof and downloads. Images live in art/.
python3 build_viewer.py  -> media_wall_viewer.html (published as the Claude artifact with art/ and files/ alongside it)
                            and ../../index.html, the same page for GitHub Pages (plain download links; answers and
                            the tracker fall back to this device, with a copy-your-answers button)
On claude.ai the page declares: db (answers/, tracker/), user (who saved what), assets (photos, editors), downloads."""
import hashlib, html, json, pathlib, re, urllib.parse
import geometry as G
import fit
from build_doc import TRACK, money, phase_totals

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent / "out"
VERSION = "13"
DOWNLOADS_ON_GITHUB = True   # v13: the artifact refuses PDFs (and some large images) from an editor outside its organisation
GITHUB_OUT = "https://github.com/emmachilds98-wq/DIY/blob/claude/eloquent-johnson-pgmnud/media-wall/out/"
LPS = 2 * G.TRAY_LPS + G.LEDGE_LPS + G.WRAP_LPS
SINGLES = 2 * G.TRAY_SINGLES

# ---------------------------------------------------------------- the open questions, most consequential first
# (id, question, why it matters, how to check, a photo helps)
QUESTIONS = [
    ("sofa", "Your L-sofa's size, and which way its return points",
     f"The plan assumes {G.SOFA_W:g} × {G.SOFA_D:g} cm, {G.SOFA_H:g} high, with the return along the side wall. It sets the PC shelf, the walkway and the dining clearances.",
     "Overall width, overall depth with the return, back height, seat depth.", False),
    ("door", "The door to the hall: which side it hinges, and does it open into the room?",
     "If it swings in, the west-end dining chair sits in its path.", "Stand in the room facing the door: hinges on the left or the right?", True),
    ("westend", "The west end's sizes: which of 935, 1045, 660 and 820 are the recess, the door and the stair box?",
     "The stair box and the door are drawn roughly until we know.", "A photo of that end of the room, or the sketch with each number pointed at.", True),
    ("walls", "The side wall and the chimney breast: solid, or plasterboard?",
     "The ledge, the PC shelf and the dining brackets fix to them; plasterboard needs different fixings.", "Knock: a hollow sound is plasterboard. Or look at an existing hole.", False),
    ("records", "Roughly how many LPs and singles, and are most in thick outer sleeves?",
     f"The wall holds about {LPS} LPs and {SINGLES} singles, all face-out. Thick sleeves need a wider trough.", "A rough count is fine.", False),
    ("turntable", "The turntable's make and model, and does it have a PHONO/LINE switch?",
     "The zone takes up to 45.2 × 35.2 cm; a switch decides whether you need the separate preamp.", "The model is usually on the plinth or underneath.", True),
    ("pc", "The PC case's make and model, and which side its glass panel is on",
     f"The shelf allows {G.PC_CASE[0]:g} × {G.PC_CASE[2]:g} cm, {G.PC_CASE[1]:g} tall, with the glass facing the room.", "Or measure width, depth and height.", True),
    ("fanstand", "The Series X fan stand's make and model",
     "The shelf takes a footprint up to about 30 cm wide; the plan assumes 20.5 × 20.5.", "A photo of the stand is enough.", True),
    ("tengang", "The 10-gang extension's length",
     f"It lies flat on the worktop behind the TV; the plan allows {G.TEN_GANG[0]:g} cm.", "End to end, plug sockets only.", False),
    ("point2", "The second ceiling point's exact spot",
     "The plan puts it about 35 cm in from the west wall and 2.3 m from the window.", "Measure from the west wall, and from the window wall.", False),
    ("chairs", "Dining chairs: ones you have, or four folding ones? And where would the leaf and legs live?",
     "The plan draws IKEA TERJE (seat 48); any chair with a 45–48 cm seat works.", "Seat height of yours, and a spot for the leaf (the garage?).", False),
    ("box", "The 23 × 22 cm box in the window's west corner: what is it?",
     "If it's pipe boxing it stays; if not, it might go.", "A photo is quickest.", True),
    ("ports", "Wired ports for the projector (master) and the music room (bedroom 2)?",
     "Each is one more Cat6 run on the electrician's visit; cheaper now than later.", "Yes or no for each.", False),
    ("stairs", "The stairs by the door go up (thanks). Which way does the flight run?",
     "v13 draws them going up, rising away from the room towards the hall, behind the wooden banister.", "A photo from the room, or a line: rising towards the hall, or towards the window?", True),
    ("games", "Roughly how many PS2, Xbox 360 and Xbox One games? (from your v6.1 plan)",
     "The game drawer holds about 48, 12 of them face-out; more needs an overflow spot.", "A count of each is plenty.", False),
    ("surge", "Is the 10-gang surge-protected, and where are its two switches? (from v6.1)",
     "It feeds the TV and the modern consoles; if not, swap it for one that is.", "Look for 'surge' on the label.", False),
    ("models", "Console model numbers, from the labels underneath (optional, from v6.1)",
     "The rows assume the largest version of each console; real models may free up height.", "Photos of the labels are fine.", True),
]


def _plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def track_rows():
    rows = []
    for st, item, ph, q, lo, hi in TRACK:
        key = hashlib.sha1((ph + "|" + re.sub(r"\(changed[^)]*\)|\(new\)|\(moved[^)]*\)", "", _plain(item))).encode()).hexdigest()[:12]
        est = money(lo, hi) if lo is not None else ("Quote" if "electrician" in item.lower() else "")
        rows.append({"id": "t" + key, "phase": ph, "item": item, "qty": q, "est": est, "lo": lo or 0, "hi": hi or 0, "done": st == "Done",
                     "kind": "job" if st == "To do" or st == "Done" and lo is None else "buy"})
    return rows


def fit_html():
    out = []
    c = fit.counts()
    for title, space, rows in fit.zones():
        n_t = sum(1 for r in rows if r[-1] == fit.TIGHT)
        n_c = sum(1 for r in rows if r[-1] == fit.CHECK)
        flags = "".join(f'<span class="pill {k}">{n} {lab}</span>' for n, k, lab in ((n_t, "tight", "tight"), (n_c, "check", "to check")) if n)
        body = []
        for item, size, src, sp, spare, st in rows:
            cls = fit.status_class(st)
            body.append(f'<tr class="r-{cls}"><td>{item}</td><td>{size}{src}</td><td>{sp}</td><td>{spare}</td><td><span class="pill {cls}">{st}</span></td></tr>')
        out.append(f'<details class="zone"><summary><span class="zt">{title}</span><span class="zf">{len(rows)} checks {flags}</span></summary>'
                   f'<p class="caption">{space}</p><div class="scroll"><table class="fit"><thead><tr><th>Item</th><th>Size (cm)</th><th>Space</th>'
                   f'<th>Spare (cm)</th><th>Result</th></tr></thead><tbody>{"".join(body)}</tbody></table></div></details>')
    head = (f'<div class="fitsum"><span class="pill ok">{c[fit.PASS]} fit</span><span class="pill tight">{c[fit.TIGHT]} tight</span>'
            f'<span class="pill check">{c[fit.CHECK]} to check on site</span><span class="pill no">{c[fit.NO]} don\'t fit</span></div>')
    return head, "\n".join(out), c


def downloads_list():
    """Files offered for download: the plan, the build guide and the HD renders, from ../out."""
    items = []
    for p in sorted(OUT.glob(f"Home_Network_Plan_v{VERSION}.pdf")) + sorted(OUT.glob(f"Build_Guide_v{VERSION}.pdf")):
        label = "The full plan" if p.name.startswith("Home") else "The build guide"
        items.append((p, f"{label}, v{VERSION}", "PDF"))
    for p in sorted(OUT.glob(f"Media wall v{VERSION} - *.png")):
        items.append((p, p.stem.replace(f"Media wall v{VERSION} - ", "").replace(" (HD)", "") + " (HD render)", "PNG"))
    for p in sorted(OUT.glob("*plan*.png")) + sorted(OUT.glob("Dining layouts*.png")) + sorted(OUT.glob("Storage options*.png")) + sorted(OUT.glob("Drawer layouts*.png")):
        items.append((p, p.stem, "PNG"))
    return items


def published_name(p):
    return "files/" + re.sub(r"[^A-Za-z0-9._-]+", "_", p.name)


STYLE = """<style>
/* Layout: one column. The render is the hero with its controls under it; facts in a band; then the open questions,
   the buy tracker, the fit proof, the plans and the downloads, each a full-width section reached from the nav. */
:root {
  --bg: #eef0ea; --surface: #ffffff; --ink: #1d241e; --muted: #5b6457; --line: #d4d9cd; --oak: #9a6634; --chip: #e3e7dd; --note: #f5efe3;
  --ok: #2f7a4a; --ok-bg: #e2f0e5; --tight: #8a5a12; --tight-bg: #f6ead2; --check: #2b5f8f; --check-bg: #e1ecf6; --no: #a3352b; --no-bg: #f7e1de;
  --display: "Bricolage Grotesque", "Segoe UI", system-ui, sans-serif;
  --body: "Atkinson Hyperlegible", "Segoe UI", system-ui, sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #151a16; --surface: #1d231e; --ink: #e7ebe3; --muted: #9ba596; --line: #2f3830; --oak: #d9a46c; --chip: #262d27; --note: #262219;
  --ok: #8fd3a2; --ok-bg: #1f3325; --tight: #e8c07a; --tight-bg: #3a2f1a; --check: #9cc4ec; --check-bg: #1c2b3a; --no: #f0a59c; --no-bg: #3d211e; color-scheme: dark } }
:root[data-theme="dark"] { --bg: #151a16; --surface: #1d231e; --ink: #e7ebe3; --muted: #9ba596; --line: #2f3830; --oak: #d9a46c; --chip: #262d27; --note: #262219;
  --ok: #8fd3a2; --ok-bg: #1f3325; --tight: #e8c07a; --tight-bg: #3a2f1a; --check: #9cc4ec; --check-bg: #1c2b3a; --no: #f0a59c; --no-bg: #3d211e; color-scheme: dark }
body { background: var(--bg); color: var(--ink); font-family: var(--body); font-size: 16px; line-height: 1.55; }
.wrap { max-width: 1120px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 28px 56px; display: grid; gap: 32px; }
header { display: grid; gap: 10px; }
h1 { font-family: var(--display); font-weight: 700; font-size: clamp(2rem, 5vw, 3.1rem); line-height: 1.05; margin: 0; letter-spacing: -0.01em; text-wrap: balance; }
.lede { color: var(--muted); margin: 0; max-width: 64ch; }
.change { margin: 0; max-width: 72ch; background: var(--note); border-left: 3px solid var(--oak); border-radius: 6px; padding: 10px 14px; }
nav.jump { display: flex; flex-wrap: wrap; gap: 6px 16px; font-size: 14.5px; }
a { color: var(--oak); text-underline-offset: 2px; }
a:focus-visible, summary:focus-visible, button:focus-visible, input:focus-visible, textarea:focus-visible { outline: 2px solid var(--oak); outline-offset: 2px; }
.viewer { display: grid; gap: 14px; }
.frame { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; overflow: hidden; }
.frame img { display: block; width: 100%; height: auto; }
.controls { display: flex; flex-wrap: wrap; gap: 14px 28px; align-items: flex-start; }
.group { display: grid; gap: 6px; min-width: 0; }
.label { font-family: var(--mono); font-size: 11.5px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); }
.seg { display: flex; flex-wrap: wrap; gap: 6px; }
.seg button, .btn { font: inherit; font-size: 14.5px; color: var(--ink); background: var(--chip); border: 1px solid transparent; border-radius: 999px; padding: 6px 14px; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; }
.seg button[aria-pressed="true"] { background: var(--surface); border-color: var(--oak); box-shadow: inset 0 0 0 1px var(--oak); }
.seg button:disabled, .btn:disabled { opacity: 0.45; cursor: not-allowed; }
.btn.primary { background: var(--oak); color: var(--surface); }
.dot { width: 14px; height: 14px; border-radius: 50%; border: 1px solid rgba(0,0,0,0.2); flex: none; }
.caption { color: var(--muted); font-size: 14px; margin: 0; }
.band { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 28px; }
.band > section { min-width: 0; display: grid; gap: 10px; align-content: start; }
section.block { display: grid; gap: 14px; min-width: 0; scroll-margin-top: 16px; }
section.block > *, #fit-zones > * { min-width: 0; }
h2 { font-family: var(--display); font-weight: 500; font-size: 1.35rem; margin: 0; }
section.block > h2 { font-size: 1.6rem; font-weight: 700; }
.heights { list-style: none; margin: 0; padding: 0; border-left: 2px solid var(--line); }
.heights li { display: grid; grid-template-columns: 4.2rem 1fr; gap: 12px; padding: 5px 0 5px 12px; position: relative; }
.heights li::before { content: ""; position: absolute; left: -2px; top: 50%; width: 8px; height: 2px; background: var(--muted); }
.heights b { font-family: var(--mono); font-weight: 500; font-variant-numeric: tabular-nums; text-align: right; }
.counts { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.counts div { background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; min-width: 0; }
.counts strong { display: block; font-family: var(--display); font-size: 1.7rem; font-weight: 700; line-height: 1.1; font-variant-numeric: tabular-nums; }
.counts span { font-size: 13.5px; color: var(--muted); }
ul.plain, ol.plain { margin: 0; padding-left: 1.3rem; display: grid; gap: 8px; max-width: 80ch; }
.plans { display: grid; gap: 14px; }
.notice { background: var(--note); border-radius: 8px; padding: 10px 14px; margin: 0; font-size: 15px; }
.notice[hidden] { display: none; }
/* open questions */
.qhead { display: flex; flex-wrap: wrap; gap: 10px 18px; align-items: center; justify-content: space-between; }
.meter { display: flex; align-items: center; gap: 10px; font-size: 14.5px; color: var(--muted); }
.meter .bar { width: 140px; height: 8px; border-radius: 4px; background: var(--chip); overflow: hidden; }
.meter .bar i { display: block; height: 100%; width: 0; background: var(--ok); }
.qs { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 14px; }
.q { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 14px; display: grid; gap: 8px; align-content: start; min-width: 0; }
.q.answered { border-color: var(--ok); }
.q h3 { margin: 0; font-size: 16px; line-height: 1.35; display: grid; grid-template-columns: 1.8rem 1fr; gap: 6px; }
.q h3 .n { font-family: var(--mono); font-size: 13px; color: var(--muted); padding-top: 2px; }
.q p { margin: 0; font-size: 14px; color: var(--muted); }
.q textarea { font: inherit; font-size: 15px; width: 100%; box-sizing: border-box; min-height: 64px; resize: vertical; border: 1px solid var(--line); border-radius: 8px; padding: 8px 10px; background: var(--bg); color: var(--ink); }
.q .row { display: flex; flex-wrap: wrap; gap: 8px 12px; align-items: center; }
.q .st { font-size: 13px; color: var(--muted); }
.q .st.ok { color: var(--ok); }
.q .st.err { color: var(--no); }
.photos { display: flex; flex-wrap: wrap; gap: 8px; }
.photos figure { margin: 0; position: relative; }
.photos img { width: 76px; height: 76px; object-fit: cover; border-radius: 6px; border: 1px solid var(--line); background: var(--chip); display: block; }
.photos button { position: absolute; top: 2px; right: 2px; font: inherit; font-size: 11px; line-height: 1; padding: 3px 5px; border-radius: 4px; border: 0; background: var(--surface); color: var(--ink); cursor: pointer; }
.upl { font-size: 14px; color: var(--oak); cursor: pointer; display: inline-flex; align-items: center; gap: 6px; }
.upl input { position: absolute; width: 1px; height: 1px; opacity: 0; }
.upl:focus-within { outline: 2px solid var(--oak); outline-offset: 2px; border-radius: 4px; }
/* tracker */
.tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; }
.tiles div { background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; }
.tiles strong { display: block; font-family: var(--display); font-size: 1.5rem; font-weight: 700; font-variant-numeric: tabular-nums; }
.tiles span { font-size: 13.5px; color: var(--muted); }
details.phase, details.zone { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; }
details.phase > summary, details.zone > summary { cursor: pointer; padding: 10px 14px; display: flex; flex-wrap: wrap; gap: 6px 14px; justify-content: space-between; align-items: center; font-weight: 700; }
details[open] > summary { border-bottom: 1px solid var(--line); }
summary .zf, summary .pf { font-weight: 400; font-size: 14px; color: var(--muted); display: inline-flex; gap: 8px; align-items: center; flex-wrap: wrap; font-variant-numeric: tabular-nums; }
.items { list-style: none; margin: 0; padding: 4px 0; }
.items li { display: grid; grid-template-columns: 28px 1fr auto; gap: 4px 10px; padding: 8px 14px; align-items: start; border-top: 1px solid var(--line); }
.items li:first-child { border-top: 0; }
.items li.done .txt { color: var(--muted); }
.items input[type=checkbox] { width: 18px; height: 18px; margin-top: 3px; accent-color: var(--ok); }
.items .txt { min-width: 0; font-size: 15px; }
.items .meta { display: block; font-size: 13px; color: var(--muted); font-variant-numeric: tabular-nums; }
.items .paid { display: flex; align-items: center; gap: 4px; font-size: 14px; color: var(--muted); }
.items .paid input { font: inherit; font-size: 14px; width: 5.5rem; padding: 3px 6px; border: 1px solid var(--line); border-radius: 6px; background: var(--bg); color: var(--ink); font-variant-numeric: tabular-nums; }
@media (max-width: 520px) { .items li { grid-template-columns: 28px 1fr; } .items .paid { grid-column: 2; } }
/* fit proof */
.fitsum { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.pill { display: inline-block; font-size: 12.5px; font-weight: 700; border-radius: 999px; padding: 2px 9px; white-space: nowrap; }
.pill.ok { color: var(--ok); background: var(--ok-bg); } .pill.tight { color: var(--tight); background: var(--tight-bg); }
.pill.check { color: var(--check); background: var(--check-bg); } .pill.no { color: var(--no); background: var(--no-bg); }
details.zone .caption { padding: 10px 14px 0; }
.scroll { overflow-x: auto; padding: 8px 14px 14px; }
table.fit { border-collapse: collapse; width: 100%; min-width: 640px; font-size: 14px; }
table.fit th { text-align: left; font-family: var(--mono); font-size: 11.5px; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); font-weight: 500; padding: 6px 8px; border-bottom: 1px solid var(--line); }
table.fit td { padding: 7px 8px; border-bottom: 1px solid var(--line); vertical-align: top; font-variant-numeric: tabular-nums; }
table.fit sup { color: var(--muted); font-size: 10px; }
.fitonly table.fit tr.r-ok { display: none; }
.dl { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 8px; }
.dl li { display: flex; justify-content: space-between; gap: 10px; align-items: center; background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 8px 12px; min-width: 0; }
.dl li span { min-width: 0; font-size: 15px; }
.dl li small { color: var(--muted); font-family: var(--mono); font-size: 12px; }
@media (prefers-reduced-motion: no-preference) { .frame img { transition: opacity .18s ease; } .meter .bar i { transition: width .3s ease; } }
</style>"""


def page(site=False):
    prefix = "media-wall/src/" if site else ""
    imgs = {k: f"{prefix}art/{k}.jpg" for k in [f"art_{s}_{p}" for s in ("join", "four", "six", "side") for p in ("card_room", "deep", "sage", "treron")] + ["key_join"]}
    rows = track_rows()
    _, lo_tot, hi_tot = phase_totals()
    phases = []
    for r in rows:
        if r["phase"] not in phases:
            phases.append(r["phase"])
    fit_head, fit_body, fc = fit_html()
    nfit = sum(fc.values())
    qs = [{"id": i, "q": q, "why": w, "how": h, "photo": ph} for i, q, w, h, ph in QUESTIONS]
    q_items = "\n".join(
        f'<li class="q" id="q-{i}" data-q="{i}"><h3><span class="n">{n:02d}</span><span>{html.escape(q)}</span></h3>'
        f'<p>{html.escape(w)}</p><p><b>How:</b> {html.escape(h)}</p>'
        f'<label class="label" for="a-{i}">Your answer</label><textarea id="a-{i}" rows="2" placeholder="Type here"></textarea>'
        f'<div class="row"><button class="btn primary save" type="button" data-q="{i}">Save</button>'
        f'<label class="upl" hidden>Add a photo<input type="file" accept="image/*" multiple data-q="{i}" id="f-{i}"></label>'
        f'<span class="st" aria-live="polite"></span></div><div class="photos"></div></li>'
        for n, (i, q, w, h, ph) in enumerate(QUESTIONS, 1))
    ph_html = []
    for ph in phases:
        items = [r for r in rows if r["phase"] == ph]
        lis = "".join(
            f'<li data-t="{r["id"]}"><input type="checkbox" id="c-{r["id"]}" aria-label="Done"><label class="txt" for="c-{r["id"]}">{r["item"]}'
            f'<span class="meta">{"Qty " + html.escape(r["qty"]) + " · " if r["qty"] else ""}{"Estimate £" + r["est"] if r["est"] and r["est"] != "Quote" else ("Quote" if r["est"] else "Job")}</span></label>'
            + (f'<span class="paid"><label for="p-{r["id"]}">Paid £</label><input id="p-{r["id"]}" type="number" min="0" step="0.01" inputmode="decimal"></span>' if r["kind"] == "buy" or r["est"] == "Quote" else "<span></span>")
            + "</li>" for r in items)
        ph_html.append(f'<details class="phase" data-ph="{html.escape(ph)}"{" open" if ph == phases[0] else ""}><summary><span>{html.escape(ph)}</span>'
                       f'<span class="pf"><span class="pd">0 of {len(items)} done</span></span></summary><ul class="items">{lis}</ul></details>')
    if site:
        dl_items = "".join(f'<li><span>{html.escape(lab)}</span><a href="media-wall/out/{urllib.parse.quote(p.name)}">{kind}</a></li>' for p, lab, kind in downloads_list())
        dl_note = "Straight from the project folder. This page and the Claude viewer update together each round."
    else:
        # PDFs can't be published to the artifact by an editor outside its organisation: link them on GitHub instead
        dl_items = "".join((f'<li><span>{html.escape(lab)}</span><a class="btn" href="{GITHUB_OUT}{urllib.parse.quote(p.name)}">{kind} on GitHub</a></li>'
                            if DOWNLOADS_ON_GITHUB or kind == "PDF" else
                            f'<li><span>{html.escape(lab)}</span><button class="btn get" type="button" data-file="{published_name(p)}" data-name="{html.escape(p.name)}">{kind}</button></li>')
                           for p, lab, kind in downloads_list())
        dl_note = ("Each link opens the file in the project's GitHub folder, media-wall/out/, where the download button saves it." if DOWNLOADS_ON_GITHUB
                   else "Each one asks you where to save it. If the buttons don't respond here, the same files are in the project's GitHub folder, media-wall/out/.")
    data = {"img": imgs, "q": qs, "track": [{k: r[k] for k in ("id", "phase", "lo", "hi", "done", "kind")} for r in rows]}
    return f"""<title>Portsmouth Close Media Wall</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Atkinson+Hyperlegible:wght@400;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
{STYLE}
<div class="wrap">
  <header>
    <h1>Media Wall v{VERSION}</h1>
    <p class="lede">The artisan oak build in Farrow &amp; Ball Card Room Green, drawn to the room as you measured it. Switch views and greens, turn on the numbered key, answer the open questions, and tick off the buy list as you go.</p>
    <p class="change"><b>What changed in v{VERSION}:</b> less cladding, as you asked. The slatted spine, the slatted PC screen, the slat panel behind the turntable, the slatted sub box and the reeded table are all gone; the PC's leads run in conduit chased into the solid wall, the sub stands on a plain oak riser and the folded table is a plain oak panel. The stairs now go up to the first floor. And the drawer layouts: every drawer to scale, with what goes in it.</p>
    <nav class="jump" aria-label="On this page"><a href="#next">New in v13</a><a href="#drawers">Drawer layouts</a><a href="#answers">What we need from you</a><a href="#tracker">Buy list and tracker</a><a href="#fit">Fit proof</a><a href="#plans">Plans</a><a href="#downloads">Downloads</a></nav>
  </header>

  <div class="viewer">
    <div class="frame"><img id="shot" alt="Render of the media wall" width="1804" height="1148"></div>
    <div class="controls">
      <div class="group"><span class="label" id="l-style">View</span>
        <div class="seg" role="group" aria-labelledby="l-style">
          <button id="s-join" data-style="join" aria-pressed="true">Artisan oak (main)</button>
          <button id="s-four" data-style="four" aria-pressed="false">Dining, four at the wall</button>
          <button id="s-six" data-style="six" aria-pressed="false">Dining, six in the room</button>
          <button id="s-side" data-style="side" aria-pressed="false">PC side wall</button>
        </div></div>
      <div class="group"><span class="label" id="l-paint">Paint</span>
        <div class="seg" role="group" aria-labelledby="l-paint">
          <button id="p-card" data-paint="card_room" aria-pressed="true"><span class="dot" style="background:#899081"></span>Card Room Green (chosen)</button>
          <button id="p-sage" data-paint="sage" aria-pressed="false"><span class="dot" style="background:#77815c"></span>Sage Green</button>
          <button id="p-treron" data-paint="treron" aria-pressed="false"><span class="dot" style="background:#8b8a77"></span>Treron</button>
          <button id="p-deep" data-paint="deep" aria-pressed="false"><span class="dot" style="background:#2c5643"></span>Deep green</button>
        </div></div>
      <div class="group"><span class="label" id="l-key">Labels</span>
        <div class="seg" role="group" aria-labelledby="l-key">
          <button id="k-key" aria-pressed="false">Show numbered key</button>
        </div></div>
    </div>
    <p class="caption" id="cap"></p>
  </div>

  <div class="band">
    <section>
      <h2>Heights, from the floor</h2>
      <ul class="heights">
        <li><b>{G.CEIL:g}</b><span>Ceiling, as measured</span></li>
        <li><b>{G.HIGH_TOP:g}</b><span>High shelf: books, a box, a print, the “now playing” single, Deco B</span></li>
        <li><b>{G.LEDGE_TOP:g}</b><span>Record ledges over the TV and round the corner; the PC shelf on the side wall</span></li>
        <li><b>{G.FOLDED_TOP:g}</b><span>Top of the dining table, folded up</span></li>
        <li><b>{G.RZ_SHELF_TOP:g}</b><span>Series X shelf, over the turntable (its lid has to {G.LID_CLEAR_TO:g})</span></li>
        <li><b>116.5</b><span>TV centre, LG C6 55in on its stand</span></li>
        <li><b>{G.WORKTOP:g}</b><span>Oak worktop, and the dining table when it's down</span></li>
        <li><b>{G.PLINTH:g}</b><span>Plinth under the two BESTÅ bays, with a hidden drawer</span></li>
      </ul>
    </section>
    <section>
      <h2>In the wall</h2>
      <div class="counts">
        <div><strong>~{LPS}</strong><span>LPs, all face-out</span></div>
        <div><strong>~{SINGLES}</strong><span>singles, all face-out</span></div>
        <div><strong>4–8</strong><span>at the dining table</span></div>
      </div>
      <ul class="plain">
        <li>Alcove: the TV between two oak uprights, {G.TV_SHIFT:.0f} cm nearer the side wall; the turntable on the worktop to its right with the Series X on a shelf above; three 60 cm bays below for the Xbox consoles, the PlayStations and the two face-out record trays.</li>
        <li>Side wall: the record ledge wraps the corner with four more LPs, then an oak shelf for the PC above the end of the sofa, with the pad dock beside it.</li>
        <li>Chimney breast: a 110 × 80 cm solid oak table with pegged breadboard ends, folded flat every day, down on two steel brackets for four, lifted off onto legs for six or eight. The sub stands under it on an oak riser.</li>
      </ul>
    </section>
    <section>
      <h2>Lighting</h2>
      <ul class="plain">
        <li>The LED strip you have now, on the ceiling round the whole room, facing down.</li>
        <li>Two four-head cone spotlight bars, Wolston style, both on your existing ceiling points. The first, on the rose between the TV and the sofa, lights the shelves, the ledge, the coffee table and the turntable. The second, between the door and the west wall, lights the table and the framed LPs: see it in the six-seat view.</li>
        <li>LED grooves in the oak uprights and a bias light behind the TV. No spot ever points at the screen.</li>
      </ul>
    </section>
  </div>

  <section class="block" id="next">
    <h2>New in v13</h2>
    <ul class="plain">
      <li><b>Less cladding.</b> Gone: the slatted cable spine on the side wall, the slatted PC screen, the slat panel behind the turntable, the slatted box round the sub and the reeded underside of the table. The slat-wall alternative is retired too.</li>
      <li><b>Cables you can't see.</b> Your side wall is solid, so the electrician chases a 25 mm conduit into it on the same visit: the PC's leads drop through a brush grommet in the shelf, down inside the wall and behind the skirting to the base. No spine, no trunking.</li>
      <li><b>Plain oak where it was slatted.</b> The sub stands on a low oak riser between the folded brackets; the folded table is plain oiled oak between its pegged breadboard ends, under the two framed LPs.</li>
      <li><b>The stairs go up.</b> The flight beside the door now rises to the first floor behind the wooden banister, through an opening in the ceiling. Tell us which way it runs and we'll match it.</li>
      <li><b>The drawer layouts</b>, below: where each of the four drawers sits in the base, and each one from above, to scale, with what goes in it and how many.</li>
      <li>Fit proof: {fc[fit.PASS]} of {nfit} checks fit outright, {fc[fit.TIGHT]} are tight, {fc[fit.CHECK]} need a check on site, none fail.</li>
    </ul>
  </section>

  <section class="block" id="drawers">
    <h2>Drawer layouts</h2>
    <p class="caption">A: the game drawer in bay 1. B: the hidden plinth drawer under bay 2. C and D: the two face-out record trays in bay 3. Top: where each drawer is in the base. Bottom: each one from above, front at the bottom, to scale.</p>
    <div class="frame"><img src="{prefix}art/zz_drawers.jpg" alt="Drawer layouts: the alcove base from the front with the four drawers marked A to D, and each drawer from above to scale with its compartments and contents" width="2688" height="1968" loading="lazy"></div>
  </section>

  <section class="block" id="answers">
    <div class="qhead"><h2>What we still need from you</h2><div class="meter"><span class="bar"><i id="q-bar"></i></span><span id="q-count">0 of {len(QUESTIONS)} answered</span></div></div>
    <p class="caption">{len(QUESTIONS)} things only you can tell us, the ones that change the drawings first. Answers saved here reach both of you and the next round of the plan. A photo is often quicker than words.</p>
    <p class="notice" id="q-local" hidden>Answers can't be saved for both of you from this view: they're kept on this device. When you're done, use Copy all answers and paste them into a message.</p>
    <p class="notice" id="q-ro" hidden>You can read the answers here but not change them. Ask Emma to give you Contributor access in the Share menu.</p>
    <ul class="qs">
{q_items}
    </ul>
    <div class="row"><button class="btn" id="copy-all" type="button">Copy all answers</button><span class="caption" id="copy-st" aria-live="polite"></span></div>
    <textarea id="copy-box" class="caption" rows="6" hidden readonly aria-label="All answers as text"></textarea>
  </section>

  <section class="block" id="tracker">
    <h2>Buy list and tracker</h2>
    <div class="tiles">
      <div><strong>£{money(lo_tot, hi_tot)}</strong><span>estimate, plus the electrician's quote</span></div>
      <div><strong id="t-paid">£0</strong><span>paid so far, from the amounts you enter</span></div>
      <div><strong id="t-done">0 of {len(rows)}</strong><span>items and jobs ticked off</span></div>
    </div>
    <p class="caption" id="t-note">In build order, as in section 11 of the plan. Tick each one off and write in what you paid; it saves for both of you.</p>
    {"".join(ph_html)}
  </section>

  <section class="block" id="fit">
    <h2>Fit proof</h2>
    <p class="caption">Every item in the wall against its published size: {fc[fit.PASS]} of {nfit} fit outright, {fc[fit.TIGHT]} are tight and {fc[fit.CHECK]} need a check on site. Source numbers refer to the plan's Sources list.</p>
    <div class="qhead">{fit_head}<button class="btn" id="fit-only" type="button" aria-pressed="false">Show only tight and to-check</button></div>
    <div id="fit-zones">{fit_body}</div>
  </section>

  <section class="block plans" id="plans">
    <h2>The living room, the dining layouts, storage and the house</h2>
    <div class="frame"><img src="{prefix}art/zz_living.jpg" alt="Living room plan drawn from the measured sketch: media wall, side-wall shelf and PC over the L-sofa, the dining wall, both spotlight bars, socket and viewing distance" width="2064" height="1464" loading="lazy"></div>
    <div class="frame"><img src="{prefix}art/zz_seating.jpg" alt="Three small plans of the dining table: four at the wall, six and eight with the table lifted off and pulled into the room" width="2064" height="1200" loading="lazy"></div>
    <div class="frame"><img src="{prefix}art/zz_storage.jpg" alt="Storage options: every space in the wall drawn to scale with what fits and how many, and the overflow options" width="2160" height="2592" loading="lazy"></div>
    <div class="frame"><img src="{prefix}art/zz_house.jpg" alt="Three floor plans with the Decos, Cat6 runs, chimney breast, brick cupboard and sloped ceilings" width="2064" height="1488" loading="lazy"></div>
    <p class="caption">The living room is drawn from your measurements; the L-sofa from your photo: its long side ends in line with the breast's reveal (about {G.SOFA_W:g} cm), the return drawn at {G.SOFA_D:g}. The house outline is traced from the agent's plans.</p>
  </section>

  <section class="block" id="downloads">
    <h2>Downloads</h2>
    <ul class="dl">{dl_items}</ul>
    <p class="caption" id="dl-note">{dl_note}</p>
  </section>
</div>
<script>
const DATA = {json.dumps(data)};
const SITE = {json.dumps(site)};
const use = n => (window.claude && window.claude.use) ? window.claude.use(n) : Promise.resolve(null);
const $ = (s, el = document) => el.querySelector(s), $$ = (s, el = document) => [...el.querySelectorAll(s)];
const store = {{ get(k, d) {{ try {{ const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; }} catch (e) {{ return d; }} }},
                set(k, v) {{ try {{ localStorage.setItem(k, JSON.stringify(v)); }} catch (e) {{}} }} }};

/* ---------- the render viewer */
const NAMES = {{ card_room: "Farrow & Ball Card Room Green No. 79, the chosen colour", treron: "Farrow & Ball Treron No. 292", sage: "Little Greene Sage Green No. 80", deep: "the deep forest green from earlier versions" }};
const VIEWS = {{ join: "Artisan oak media wall", four: "The dining wall, down and set for four", six: "The table lifted off and set for six, with both spot bars", side: "The PC side wall, seen from the room" }};
const view = Object.assign({{ style: "join", paint: "card_room", key: false }}, store.get("mw13-view", {{}}));
const shot = $("#shot"), cap = $("#cap"), keyBtn = $("#k-key");
function draw() {{
  if (!VIEWS[view.style]) view.style = "join";
  if (view.style === "four" || view.style === "six" || view.style === "side") view.key = false;
  shot.src = view.key ? DATA.img["key_" + view.style] : DATA.img["art_" + view.style + "_" + view.paint];
  shot.alt = VIEWS[view.style] + (view.key ? " with numbered key" : " in " + NAMES[view.paint]);
  $$("[data-style]").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.style === view.style)));
  $$("[data-paint]").forEach(b => {{ b.setAttribute("aria-pressed", String(!view.key && b.dataset.paint === view.paint)); b.disabled = view.key; }});
  keyBtn.setAttribute("aria-pressed", String(view.key));
  keyBtn.disabled = view.style === "four" || view.style === "six" || view.style === "side";
  cap.textContent = view.key
    ? ("Full numbered key for the artisan oak build, in Card Room Green. Game drawer and lower record tray pulled out 30 cm. Dashed lines are hidden: gold for data, audio and low-voltage leads, coral for mains.")
    : view.style === "six" ? "The table lifted off onto four legs, 60 cm off the breast, set for six, in " + NAMES[view.paint] + ". The camera stands in line with the alcove's edge so both spot bars show; the stairs go up beside the door; their direction is drawn roughly until you send a photo."
    : view.style === "side" ? "The PC side wall in " + NAMES[view.paint] + ": the ledge round the corner, the PC on its shelf with the keyboard tray, its leads inside the wall, the sofa below, the media wall end-on at the right (the breast cut away)."
    : VIEWS[view.style] + ", shown in " + NAMES[view.paint] + ". Evening light, drawn to the measured room.";
  store.set("mw13-view", view);
}}
$$("[data-style]").forEach(b => b.addEventListener("click", () => {{ view.style = b.dataset.style; draw(); }}));
$$("[data-paint]").forEach(b => b.addEventListener("click", () => {{ view.paint = b.dataset.paint; draw(); }}));
keyBtn.addEventListener("click", () => {{ view.key = !view.key; draw(); }});
draw();

/* ---------- fit proof filter */
$("#fit-only").addEventListener("click", e => {{
  const on = e.currentTarget.getAttribute("aria-pressed") !== "true";
  e.currentTarget.setAttribute("aria-pressed", String(on));
  $("#fit-zones").classList.toggle("fitonly", on);
  $$("#fit-zones details.zone").forEach(d => {{ if (on && d.querySelector("tr.r-tight, tr.r-check")) d.open = true; }});
}});

/* ---------- shared state: answers, photos, tracker */
let db = null, assets = null, user = null, myId = null, readOnly = false;
const remote = {{}};            // answers/<id> bodies as saved
const tstate = {{}};            // tracker/<id> bodies as saved
const chains = {{}};            // one write at a time per document
const names = {{}};
const fmtTime = iso => {{ try {{ return new Date(iso).toLocaleString(undefined, {{ day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" }}); }} catch (e) {{ return ""; }} }};
function write(path, body) {{
  const run = () => db.doc(path).set(body);
  chains[path] = (chains[path] || Promise.resolve()).then(run, run);
  return chains[path];
}}
function onWriteError(e, stEl) {{
  if (e && e.code === "invalid_argument") {{ readOnly = true; $("#q-ro").hidden = false; lockInputs(); }}
  if (stEl) {{ stEl.textContent = e && e.code === "quota_exceeded" ? "The page's storage is full; tell Claude." : "Couldn't save. Try again in a moment."; stEl.className = "st err"; }}
}}
function lockInputs() {{ $$(".q textarea, .q .save, .items input").forEach(el => el.disabled = true); $$(".upl").forEach(el => el.hidden = true); }}
async function nameOf(id) {{
  if (!id) return "";
  if (id === myId) return "you";
  if (names[id] !== undefined) return names[id];
  names[id] = "";
  try {{ const ps = await user.profiles([id]); names[id] = (ps[id] && ps[id].name) || ""; }} catch (e) {{}}
  return names[id];
}}

/* answers */
const drafts = store.get("mw12-drafts", {{}});
function cardFor(id) {{ return document.getElementById("q-" + id); }}
function answeredCount() {{
  return DATA.q.filter(q => ((remote[q.id] && remote[q.id].text) || (!db && drafts[q.id]) || "").trim() || (remote[q.id] && (remote[q.id].photos || []).length)).length;
}}
function meter() {{
  const n = answeredCount(), t = DATA.q.length;
  $("#q-count").textContent = n + " of " + t + " answered";
  $("#q-bar").style.width = (100 * n / t) + "%";
}}
async function paintAnswer(id) {{
  const card = cardFor(id), body = remote[id];
  if (!card) return;
  const st = $(".st", card), ta = $("textarea", card);
  if (body && document.activeElement !== ta && !card.dataset.dirty) ta.value = body.text || "";
  card.classList.toggle("answered", !!(body && ((body.text || "").trim() || (body.photos || []).length)));
  if (body && body.at) {{
    const who = await nameOf(body.by);
    st.textContent = "Saved " + fmtTime(body.at) + (who ? " by " + who : "");
    st.className = "st ok";
  }}
  const box = $(".photos", card);
  box.textContent = "";
  for (const p of (body && body.photos) || []) {{
    if (!/^[0-9a-f]{{32}}$/.test(p.id || "")) continue;
    const fig = document.createElement("figure");
    const im = document.createElement("img");
    im.src = "/_blob/" + p.id; im.alt = p.name || "Photo"; im.loading = "lazy";
    im.onerror = () => {{ im.removeAttribute("src"); im.alt = "Photo unavailable"; }};
    fig.appendChild(im);
    if (db && !readOnly) {{
      const rm = document.createElement("button"); rm.type = "button"; rm.textContent = "Remove"; rm.setAttribute("aria-label", "Remove this photo from the answer");
      rm.addEventListener("click", () => {{
        const b = Object.assign({{ text: "" }}, remote[id]);
        b.photos = (b.photos || []).filter(x => x.id !== p.id); b.by = myId; b.at = new Date().toISOString();
        write("answers/" + id, b).catch(e => onWriteError(e, st));
      }});
      fig.appendChild(rm);
    }}
    box.appendChild(fig);
  }}
  meter();
}}
DATA.q.forEach(q => {{
  const card = cardFor(q.id), ta = $("textarea", card), st = $(".st", card);
  if (drafts[q.id]) ta.value = drafts[q.id];
  ta.addEventListener("input", () => {{ card.dataset.dirty = "1"; drafts[q.id] = ta.value; store.set("mw12-drafts", drafts); if (!db) meter(); st.textContent = db ? "Not saved yet" : "Kept on this device"; st.className = "st"; }});
  $(".save", card).addEventListener("click", async () => {{
    if (!db) {{ st.textContent = "Kept on this device. Copy all answers to send them."; st.className = "st"; return; }}
    const body = Object.assign({{ photos: [] }}, remote[q.id], {{ text: ta.value.trim().slice(0, 4000), by: myId, at: new Date().toISOString() }});
    st.textContent = "Saving…"; st.className = "st";
    try {{ await write("answers/" + q.id, body); delete card.dataset.dirty; delete drafts[q.id]; store.set("mw12-drafts", drafts); }}
    catch (e) {{ onWriteError(e, st); }}
  }});
  $(".upl input", card).addEventListener("change", async ev => {{
    const files = [...ev.target.files].slice(0, 6);
    ev.target.value = "";
    if (!assets || !files.length) return;
    st.textContent = "Uploading " + files.length + (files.length > 1 ? " photos…" : " photo…"); st.className = "st";
    const added = [];
    for (const f of files) {{
      try {{ const r = await assets.upload(f); added.push({{ id: r.id, name: (f.name || "photo").slice(0, 80) }}); }}
      catch (e) {{ st.textContent = e && e.code === "too_large" ? "That photo is over 20 MB; try a smaller one." : e && e.code === "unsupported_type" ? "That file type isn't supported; use a JPEG or PNG." : "Couldn't upload. Try again."; st.className = "st err"; }}
    }}
    if (!added.length) return;
    const body = Object.assign({{ text: "" }}, remote[q.id]);
    body.photos = (body.photos || []).concat(added); body.by = myId; body.at = new Date().toISOString();
    try {{ await write("answers/" + q.id, body); }} catch (e) {{ onWriteError(e, st); }}
  }});
}});
meter();

$("#copy-all").addEventListener("click", async () => {{
  const lines = DATA.q.map((q, i) => {{
    const t = (cardFor(q.id).querySelector("textarea").value || "").trim();
    return (i + 1) + ". " + q.q + "\\n" + (t || "(not answered yet)");
  }});
  const text = "Media wall: our answers\\n\\n" + lines.join("\\n\\n");
  const box = $("#copy-box"), st = $("#copy-st");
  try {{ await navigator.clipboard.writeText(text); st.textContent = "Copied. Paste it into a message."; box.hidden = true; }}
  catch (e) {{ box.value = text; box.hidden = false; box.focus(); box.select(); st.textContent = "Select the text below and copy it."; }}
}});

/* tracker */
const local = store.get("mw12-tracker", {{}});
const money = v => "£" + (Math.round(v * 100) / 100).toLocaleString(undefined, {{ minimumFractionDigits: v % 1 ? 2 : 0, maximumFractionDigits: 2 }});
function tget(id) {{ return (db ? tstate[id] : local[id]) || null; }}
function paintTracker() {{
  let done = 0, paid = 0;
  DATA.track.forEach(r => {{
    const s = tget(r.id), isDone = s ? !!s.done : r.done;
    const li = document.querySelector('[data-t="' + r.id + '"]'), cb = li.querySelector("input[type=checkbox]"), pd = li.querySelector("input[type=number]");
    cb.checked = isDone; li.classList.toggle("done", isDone);
    if (pd && document.activeElement !== pd) pd.value = s && typeof s.paid === "number" ? s.paid : "";
    if (isDone) done++;
    if (s && typeof s.paid === "number") paid += s.paid;
  }});
  $$("details.phase").forEach(d => {{
    const lis = $$(".items li", d), n = lis.filter(li => li.classList.contains("done")).length;
    $(".pd", d).textContent = n + " of " + lis.length + " done";
  }});
  $("#t-done").textContent = done + " of " + DATA.track.length;
  $("#t-paid").textContent = money(paid);
}}
function saveTrack(id, patch) {{
  const r = DATA.track.find(x => x.id === id);
  const cur = tget(id) || {{ done: r.done, paid: null }};
  const body = Object.assign({{}}, cur, patch);
  if (!db) {{ local[id] = body; store.set("mw12-tracker", local); paintTracker(); return; }}
  body.by = myId; body.at = new Date().toISOString();
  tstate[id] = body; paintTracker();
  write("tracker/" + id, body).catch(e => onWriteError(e, null));
}}
DATA.track.forEach(r => {{
  const li = document.querySelector('[data-t="' + r.id + '"]');
  li.querySelector("input[type=checkbox]").addEventListener("change", e => saveTrack(r.id, {{ done: e.target.checked }}));
  const pd = li.querySelector("input[type=number]");
  if (pd) pd.addEventListener("change", e => {{
    const v = e.target.value === "" ? null : Math.max(0, Math.round(parseFloat(e.target.value) * 100) / 100);
    saveTrack(r.id, {{ paid: Number.isFinite(v) ? v : null }});
  }});
}});
paintTracker();

/* downloads (claude.ai): fetch the published file, then hand it to the viewer's save prompt */
let downloads = null;
$$(".get").forEach(b => b.addEventListener("click", async () => {{
  const st = $("#dl-note"), label = b.textContent;
  if (!downloads) {{ st.textContent = "Downloads aren't available in this view. The same files are in the project's GitHub folder, media-wall/out/."; return; }}
  b.disabled = true; b.textContent = "…";
  try {{
    const res = await fetch(b.dataset.file);
    if (!res.ok) throw {{ code: "fetch" }};
    await downloads.save({{ filename: b.dataset.name, data: await res.blob() }});
    st.textContent = "Saved " + b.dataset.name + ".";
  }} catch (e) {{
    st.textContent = e && e.code === "declined" ? "Not saved." : e && e.code === "rate_limited" ? "Another save is open; finish that one first." : "Couldn't fetch that file here. It's also in the project's GitHub folder, media-wall/out/.";
  }} finally {{ b.disabled = false; b.textContent = label; }}
}}));

/* light up what this view can do */
(async () => {{
  const [d, u, a, dl] = await Promise.all([use("db"), use("user"), use("assets"), use("downloads")]);
  downloads = dl;
  if (!SITE && !dl && $$(".get").length) {{ $$(".get").forEach(b => b.disabled = true); $("#dl-note").textContent = "Downloads aren't available in this view. The same files are in the project's GitHub folder, media-wall/out/."; }}
  user = u;
  if (!d) {{
    $("#q-local").hidden = false;
    $("#t-note").textContent = "In build order, as in section 11 of the plan. Ticks and amounts are kept on this device only from this view.";
    return;
  }}
  db = d;
  try {{ myId = u ? await u.id() : null; }} catch (e) {{ myId = null; }}
  let canWrite = null;
  try {{ canWrite = u ? await u.can("data.write") : null; }} catch (e) {{}}
  if (canWrite === false) {{ readOnly = true; $("#q-ro").hidden = false; lockInputs(); }}
  else if (a) {{ assets = a; $$(".upl").forEach(el => el.hidden = false); }}
  $$(".q .st").forEach(st => {{ if (st.textContent === "Kept on this device") st.textContent = "Not saved yet"; }});
  db.collection("answers").onSnapshot(snap => {{
    snap.docChanges().forEach(ch => {{
      if (ch.type === "removed") delete remote[ch.doc.id]; else remote[ch.doc.id] = ch.doc.data();
      paintAnswer(ch.doc.id);
    }});
    meter();
  }}, () => {{}});
  db.collection("tracker").onSnapshot(snap => {{
    snap.docChanges().forEach(ch => {{ if (ch.type === "removed") delete tstate[ch.doc.id]; else tstate[ch.doc.id] = ch.doc.data(); }});
    paintTracker();
  }}, () => {{}});
}})();
</script>
"""


def site():
    """The same page for GitHub Pages at the repo root: a full document, paths into media-wall/, plain download links."""
    body = page(site=True).replace("body { background", "body { margin: 0; background", 1)
    head, rest = body.split("</style>", 1)
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + head + "</style>\n</head>\n<body>" + rest + "</body>\n</html>\n")


def publish_files():
    """{published path: source} for the Artifact publish: the viewer images and the downloads."""
    files = {f"art/{p.name}": str(p) for p in sorted((HERE / "art").glob("*.jpg"))}
    if not DOWNLOADS_ON_GITHUB:
        files.update({published_name(p): str(p) for p, _, kind in downloads_list() if kind != "PDF"})
    return files


if __name__ == "__main__":
    (HERE / "media_wall_viewer.html").write_text(page())
    (HERE.parent.parent / "index.html").write_text(site())
    (HERE / "publish_files.json").write_text(json.dumps(publish_files(), indent=1))
    print("viewer ok", len(publish_files()), "files")
