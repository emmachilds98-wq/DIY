"""Builds the plan page (v13.3): the whole plan in tabs (overview, 3D views, media wall, dining, paint and light, network and
power, build steps, buy list with cost by phase, questions, checks), the sections borrowed from build_doc.py, with
answers, photos, buy ticks and step ticks saved for both of you. Images live in art/.
python3 build_viewer.py  -> media_wall_viewer.html (published as the Claude artifact with art/ and files/ alongside it)
                            and ../../index.html, the same page for GitHub Pages (plain download links; answers and
                            the tracker fall back to this device, with a copy-your-answers button)
On claude.ai the page declares: db (answers/, tracker/), user (who saved what), assets (photos, editors), downloads."""
import hashlib, html, json, pathlib, re, urllib.parse
import geometry as G
import fit
from build_doc import TRACK, money, phase_totals, plan_sections, steps, GUIDE_RULES, GUIDE_TIME, GUIDE_TECHNIQUES, GUIDE_PITFALLS, guide_tools, cuts_html, cuts_text, need_html, full_html, DIAGRAMS, PARTS, PHASE_PART, part_chip

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent / "out"
VERSION = "14"
DOWNLOADS_ON_GITHUB = True   # v13: the artifact refuses PDFs (and some large images) from an editor outside its organisation
GITHUB_OUT = "https://github.com/emmachilds98-wq/DIY/blob/claude/sharp-franklin-lrray1/media-wall/out/"  # v13.8: the branch that carries every round (PR #4); switch to main once it merges
LPS = 2 * G.TRAY_LPS + G.LEDGE_LPS + G.WRAP_LPS
SINGLES = 2 * G.TRAY_SINGLES

# ---------------------------------------------------------------- the open questions, most consequential first
# (id, question, why it matters, how to check, a photo helps)
from questions import QUESTIONS   # v13.6: one list, shared with the plan PDF
import room3d_page                 # v14: the room in 3D
from shot3d import SHOTS as SHOTS3D


def _plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def track_rows():
    rows = []
    for st, item, ph, q, lo, hi in TRACK:
        key = hashlib.sha1((ph + "|" + re.sub(r"\(changed[^)]*\)|\(new\)|\(moved[^)]*\)", "", _plain(item))).encode()).hexdigest()[:12]
        est = money(lo, hi) if lo is not None else ""
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
    for p in sorted(OUT.glob("*plan*.png")) + sorted(OUT.glob("Dining layouts*.png")) + sorted(OUT.glob("Storage options*.png")) + sorted(OUT.glob("Drawer layouts*.png")) + sorted(OUT.glob("Sub cover*.png")):
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
header { display: grid; gap: 10px; min-width: 0; }
h1 { font-family: var(--display); font-weight: 700; font-size: clamp(2rem, 5vw, 3.1rem); line-height: 1.05; margin: 0; letter-spacing: -0.01em; text-wrap: balance; }
.lede { color: var(--muted); margin: 0; max-width: 64ch; }
.change { margin: 0; max-width: 72ch; background: var(--note); border-left: 3px solid var(--oak); border-radius: 6px; padding: 10px 14px; }
nav.jump { display: flex; flex-wrap: wrap; gap: 6px 16px; font-size: 14.5px; }
a { color: var(--oak); text-underline-offset: 2px; }
a:focus-visible, summary:focus-visible, button:focus-visible, input:focus-visible, textarea:focus-visible { outline: 2px solid var(--oak); outline-offset: 2px; }
.viewer { display: grid; gap: 14px; }
.frame { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; overflow: hidden; }
.frame img { display: block; width: 100%; height: auto; }
.shotwrap { position: relative; }
[hidden] { display: none !important; }
.shotwrap .dims { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }
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
/* v13.3: the plan in tabs. A sticky tab bar under the title; each tab is one panel of the plan, drawings on paper cards. */
:root { --paper: #fbfaf5; --paper-line: #e2ded2; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --paper: #ebe8de; --paper-line: #c9c4b4; } }
:root[data-theme="dark"] { --paper: #ebe8de; --paper-line: #c9c4b4; }
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 10; background: var(--bg); }
.eyebrow { margin: 0; font-family: var(--mono); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); }
.tabs { min-width: 0; position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; background: var(--bg); border-bottom: 1px solid var(--line); margin-top: -12px; }
.tabs .tl { display: flex; gap: 4px; overflow-x: auto; padding-block: 8px; scrollbar-width: thin; }
.tabs button { font: inherit; font-size: 14.5px; white-space: nowrap; background: none; border: 0; border-radius: 999px; padding: 7px 13px; color: var(--muted); cursor: pointer; flex: none; }
.tabs button:hover { color: var(--ink); background: var(--chip); }
.tabs button[aria-selected="true"] { background: var(--ink); color: var(--bg); }
.tabs button:focus-visible { outline: 2px solid var(--oak); outline-offset: 2px; }
.panel { display: grid; gap: 22px; min-width: 0; }
.panel > * { min-width: 0; }
.panel h2, .panel h3, .panel h4 { scroll-margin-top: calc(64px + env(safe-area-inset-top, 0px)); }
.ptitle { margin: 0; }
h2.ptitle { font-size: 1.6rem; font-weight: 700; }
h3.ptitle { font-family: var(--display); font-size: 1.25rem; font-weight: 700; }
.block { display: grid; gap: 12px; min-width: 0; }
.toc { display: flex; flex-wrap: wrap; gap: 6px; }
.chip { font: inherit; font-size: 13.5px; color: var(--ink); background: var(--chip); border: 0; border-radius: 999px; padding: 4px 11px; cursor: pointer; text-decoration: none; display: inline-flex; gap: 6px; align-items: center; }
.chip.h2 { background: var(--note); font-weight: 700; }
a.chip:hover, button.chip:hover { box-shadow: inset 0 0 0 1px var(--oak); }
/* plan text borrowed from the PDF */
.doc { min-width: 0; max-width: 100%; }
.doc > h2:first-child { margin-top: 0; }
.doc h2 { font-family: var(--display); font-weight: 700; font-size: 1.6rem; margin: 34px 0 10px; text-wrap: balance; }
.doc h3 { font-family: var(--display); font-weight: 700; font-size: 1.22rem; margin: 26px 0 8px; text-wrap: balance; }
.doc h4 { font-size: 1rem; margin: 18px 0 6px; }
.doc p, .doc ul, .doc ol { margin: 0 0 12px; max-width: 78ch; }
.doc ul, .doc ol { padding-left: 1.3rem; }
.doc li { margin-bottom: 5px; }
.doc sup { color: var(--muted); font-size: 10.5px; margin-left: 1px; }
.doc .note { color: var(--muted); font-size: 14.5px; }
.doc .notice { margin-bottom: 14px; }
.tscroll { overflow-x: auto; margin: 0 0 16px; border: 1px solid var(--line); border-radius: 8px; background: var(--surface); }
.tscroll table { border-collapse: collapse; width: 100%; min-width: 560px; font-size: 14.5px; }
.tscroll th { text-align: left; font-family: var(--mono); font-size: 11.5px; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); font-weight: 500; padding: 8px 10px; border-bottom: 1px solid var(--line); vertical-align: bottom; }
.tscroll td { padding: 8px 10px; border-bottom: 1px solid var(--line); vertical-align: top; font-variant-numeric: tabular-nums; }
.tscroll tr:last-child td { border-bottom: 0; }
.tscroll td.num { white-space: nowrap; }
.tscroll tr.total td { font-weight: 700; background: var(--note); }
.tscroll tr.ph td, .tscroll td.kg { background: var(--chip); font-family: var(--mono); font-size: 11.5px; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); }
.tscroll td.kn { width: 2rem; text-align: center; font-weight: 700; background: var(--note); }
.keycols { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 0 16px; align-items: start; }
.keycols .tscroll table { min-width: 0; }
.doc figure { margin: 0 0 18px; }
.doc figure img { display: block; width: 100%; height: auto; border-radius: 10px; border: 1px solid var(--line); background: var(--chip); }
.lightbox { position: fixed; inset: 0; z-index: 20; background: var(--bg); display: grid; grid-template-rows: auto 1fr;
  padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
.lbbar { display: flex; gap: 12px; align-items: center; justify-content: space-between; padding: 10px max(16px, env(safe-area-inset-right, 0px)) 10px max(16px, env(safe-area-inset-left, 0px)); border-bottom: 1px solid var(--line); }
.lbscroll { overflow: auto; cursor: grab; touch-action: pan-x pan-y pinch-zoom; }
.lbscroll:active { cursor: grabbing; }
.lbwrap { position: relative; width: 1650px; max-width: none; }
.lbwrap img { display: block; width: 1650px; max-width: none; height: auto; user-select: none; -webkit-user-drag: none; }
.lbwrap #lb-dims { position: absolute; inset: 0; }
.doc figure.dia { background: var(--paper); border: 1px solid var(--paper-line); border-radius: 10px; padding: 12px; overflow-x: auto; }
.doc figure.dia svg { display: block; width: 100%; min-width: 640px; height: auto; }
.doc figcaption { color: var(--muted); font-size: 14px; margin-top: 8px; max-width: 78ch; }
.doc .decision, .doc .why, .doc .callout { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 12px 16px; margin: 0 0 16px; max-width: 78ch; }
.doc .callout ul, .doc .why ul { margin: 8px 0 0; }
.doc .confirm { background: var(--note); border-radius: 8px; padding: 10px 14px; font-size: 15px; }
.doc ul.checks, .doc ul.agreed { list-style: none; padding-left: 0; }
.doc ul.checks li, .doc ul.agreed li { padding-left: 1.5rem; position: relative; }
.doc ul.agreed li::before { content: "✓"; position: absolute; left: 0; color: var(--ok); font-weight: 700; }
.doc ol.sources { font-size: 14px; color: var(--muted); }
.doc .hero { display: grid; grid-template-columns: minmax(0, 2fr) minmax(220px, 1fr); gap: 16px; align-items: start; margin-bottom: 16px; }
.doc .hero figure { margin: 0; }
.doc .summary { display: grid; gap: 10px; }
.doc .summary div { background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; }
.doc .summary b { display: block; font-family: var(--display); font-size: 1.45rem; line-height: 1.15; font-variant-numeric: tabular-nums; }
.doc .summary span { font-size: 13.5px; color: var(--muted); }
@media (max-width: 720px) { .doc .hero { grid-template-columns: 1fr; } }
details.changes { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; }
details.changes > summary { cursor: pointer; padding: 10px 14px; font-weight: 700; }
details.changes > .doc { padding: 4px 14px 2px; }
/* how the build runs */
.runlist { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 8px; }
.runlist li { background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 8px 12px; display: grid; gap: 2px; min-width: 0; }
.runlist a { color: var(--ink); text-decoration: none; font-weight: 700; display: flex; gap: 10px; align-items: baseline; }
.runlist a:hover { color: var(--oak); }
.runlist .rn, .sn { font-family: var(--display); font-weight: 700; font-variant-numeric: tabular-nums; }
.runlist .rn { color: var(--oak); min-width: 1.4rem; }
.runlist .rm { font-size: 13.5px; color: var(--muted); padding-left: 2.0rem; }
/* v13.6: part labels and the one-part filter */
.part { display: inline-flex; align-items: center; gap: 5px; font-family: var(--mono); font-size: 11.5px; letter-spacing: 0.04em; text-transform: uppercase;
  line-height: 1.3; padding: 2px 8px; border-radius: 999px; color: var(--ink); white-space: nowrap; vertical-align: middle;
  background: color-mix(in srgb, var(--pc) 13%, transparent); border: 1px solid color-mix(in srgb, var(--pc) 50%, transparent); margin-right: 4px; }
.part::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: var(--pc); flex: none; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .part::before { background: color-mix(in srgb, var(--pc) 60%, white); } }
:root[data-theme="dark"] .part::before { background: color-mix(in srgb, var(--pc) 60%, white); }
.sparts { margin: 0 0 3px; display: flex; flex-wrap: wrap; gap: 4px; }
.runlist .rp { padding-left: 2.0rem; display: flex; flex-wrap: wrap; gap: 4px; align-items: center; }
.runlist li { align-content: start; }
summary .part { font-weight: 400; }
.pfilter { margin: 4px 0 14px; display: grid; gap: 6px; }
.pfilter .seg { flex-wrap: wrap; }
.step[hidden] { display: none; }
/* v13.7: lighting scenes */
.scenes { display: grid; grid-template-columns: minmax(0, 1fr); gap: 10px; margin: 8px 0 18px; }
.scenes > * { min-width: 0; }
.scenes .seg { flex-wrap: wrap; }
.scene[hidden] { display: none; }
.scene ul { margin: 6px 0 0; }
/* build steps */
.steps-list { list-style: none; margin: 0; padding: 0; display: grid; gap: 14px; }
.step { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 14px 16px; display: grid; gap: 10px; min-width: 0; scroll-margin-top: calc(64px + env(safe-area-inset-top, 0px)); }
.step > * { min-width: 0; }
.step.done { border-color: var(--ok); }
.shead { display: grid; grid-template-columns: 2.6rem minmax(0, 1fr) auto; gap: 12px; align-items: center; }
.sn { width: 2.6rem; height: 2.6rem; border-radius: 50%; background: var(--chip); display: grid; place-items: center; font-size: 1.15rem; }
.step.done .sn { background: var(--ok); color: var(--surface); }
.shead h3 { margin: 0; font-family: var(--display); font-size: 1.2rem; font-weight: 700; }
.smeta { font-size: 13.5px; color: var(--muted); }
.sdone { display: inline-flex; gap: 6px; align-items: center; font-size: 14.5px; cursor: pointer; }
.sdone input { width: 18px; height: 18px; accent-color: var(--ok); }
.sbuy { margin: 0; display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.sbuy .label { margin-right: 4px; }
.sbuy .chip { background: var(--tight-bg); }
.sdo { margin: 0; padding-left: 1.3rem; display: grid; gap: 6px; max-width: 80ch; }
.scheck { margin: 0; background: var(--ok-bg); border-radius: 8px; padding: 8px 12px; font-size: 15px; max-width: 80ch; }
.ssee { margin: 0; font-size: 14px; color: var(--muted); }
.need { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px 18px; background: var(--note); border-radius: 8px; padding: 10px 14px; }
.need h5 { margin: 0 0 4px; font-family: var(--mono); font-size: 11.5px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); font-weight: 500; }
.need ul { margin: 0; padding-left: 1.1rem; display: grid; gap: 3px; font-size: 14.5px; }
details.sdraw > summary { cursor: pointer; font-size: 14px; color: var(--oak); font-weight: 700; padding: 2px 0; }
details.sdraw figure.dia { margin: 8px 0 0; background: var(--paper); border: 1px solid var(--paper-line); border-radius: 10px; padding: 10px; overflow-x: auto; }
details.sdraw figure.dia svg { display: block; width: 100%; min-width: 640px; height: auto; }
.sfull { display: grid; gap: 4px; max-width: 80ch; }
.sfull h5 { margin: 10px 0 2px; font-family: var(--display); font-size: 1.02rem; font-weight: 700; }
.sfull ol { margin: 0; padding-left: 1.6rem; display: grid; gap: 6px; }
.sfull li::marker { font-variant-numeric: tabular-nums; color: var(--muted); }
/* cost by phase */
.chart { display: grid; gap: 10px; background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 14px 16px; }
.crow { display: grid; grid-template-columns: minmax(8rem, 13rem) minmax(0, 1fr) 9.5rem; gap: 4px 14px; align-items: center; }
.cl { color: var(--ink); text-decoration: none; font-size: 14.5px; font-weight: 700; display: grid; line-height: 1.25; }
.cl:hover { color: var(--oak); }
.cl small, .cv small { font-weight: 400; font-size: 12.5px; color: var(--muted); display: block; }
.ctrack { position: relative; height: 22px; background-image: linear-gradient(to right, var(--line) 1px, transparent 1px); background-size: calc(100% / var(--n)) 100%; border-right: 1px solid var(--line); }
.clo, .chi { position: absolute; top: 2px; height: 13px; background: var(--oak); }
.clo { left: 0; border-radius: 3px 0 0 3px; }
.chi { opacity: 0.35; border-radius: 0 3px 3px 0; }
.cpaid { position: absolute; left: 0; top: 17px; height: 4px; border-radius: 2px; background: var(--ok); }
.cv { font-size: 14px; font-variant-numeric: tabular-nums; text-align: right; }
.crow.axis { margin-top: -4px; }
.caxis { position: relative; height: 16px; font-family: var(--mono); font-size: 11px; color: var(--muted); font-variant-numeric: tabular-nums; }
.caxis span { position: absolute; top: 0; transform: translateX(-50%); white-space: nowrap; }
.caxis span:first-child { transform: none; }
.caxis span:last-child { transform: translateX(-100%); }
.legend { margin: 4px 0 0; display: flex; flex-wrap: wrap; gap: 6px 18px; font-size: 13px; color: var(--muted); }
.legend span { display: inline-flex; gap: 6px; align-items: center; }
.legend i { width: 18px; height: 10px; border-radius: 2px; background: var(--oak); display: inline-block; }
.legend i.k-hi { opacity: 0.35; } .legend i.k-pd { background: var(--ok); height: 4px; }
@media (max-width: 620px) {
  .crow { grid-template-columns: minmax(0, 1fr) auto; }
  .ctrack, .caxis { grid-column: 1 / -1; grid-row: 2; }
  .crow.axis > span { display: none; }
  .caxis span:nth-child(even) { display: none; }
}
#tracker { display: grid; gap: 10px; }
#tracker.f-left li.done, #tracker.f-left li[data-kind="job"], #tracker.f-jobs li[data-kind="buy"] { display: none; }
summary .pf a { color: var(--oak); }
/* v14: tab groups, the overview's dashboard, the table's two options, the 3D room and its gallery */
.tabs .tg { flex: none; align-self: center; font-family: var(--mono); font-size: 10.5px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted);
  padding: 0 4px 0 12px; margin-left: 6px; border-left: 1px solid var(--line); }
.tabs .tg:first-child { border-left: 0; margin-left: 0; padding-left: 2px; }
.dash { display: grid; grid-template-columns: minmax(0, 1.6fr) repeat(3, minmax(0, 1fr)); gap: 12px; }
.dcard { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 12px 14px; display: grid; gap: 6px; align-content: start; min-width: 0; }
.dcard strong { font-family: var(--display); font-size: 1.6rem; line-height: 1.1; font-variant-numeric: tabular-nums; }
.dcard a.caption { color: var(--oak); text-decoration: none; }
.dcard a.caption:hover { text-decoration: underline; }
.dbar { height: 8px; border-radius: 4px; background: var(--chip); overflow: hidden; }
.dbar i { display: block; height: 100%; width: 0; background: var(--ok); }
.d3d { position: relative; padding: 0; overflow: hidden; text-decoration: none; color: #fff; min-height: 150px; background: #0d100e; }
.d3d img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.d3d span { position: absolute; left: 0; right: 0; bottom: 0; padding: 26px 14px 10px; font-family: var(--display); font-weight: 700; font-size: 1.15rem;
  background: linear-gradient(transparent, rgba(0,0,0,0.72)); }
.d3d:hover span { text-decoration: underline; }
@media (max-width: 860px) { .dash { grid-template-columns: repeat(3, minmax(0, 1fr)); } .d3d { grid-column: 1 / -1; aspect-ratio: 16 / 7; } }
@media (max-width: 520px) { .dash { grid-template-columns: minmax(0, 1fr); } }
.opts { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 14px; }
.opt { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; overflow: hidden; display: grid; grid-template-rows: auto 1fr; min-width: 0; }
.opt img { display: block; width: 100%; aspect-ratio: 16 / 9; object-fit: cover; background: #0d100e; }
.opt .ob { padding: 12px 14px 14px; display: grid; gap: 8px; align-content: start; }
.opt h3 { margin: 0; font-family: var(--display); font-size: 1.2rem; }
.opt ul { margin: 0; padding-left: 1.2rem; display: grid; gap: 4px; font-size: 14.5px; }
.opt li::marker { content: "+  "; color: var(--ok); font-weight: 700; }
.opt li.minus::marker { content: "\u2212  "; color: var(--tight); }
.opt .btn { justify-self: start; }
.gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 12px; }
.gallery figure { margin: 0; display: grid; gap: 6px; }
.gallery button { padding: 0; border: 1px solid var(--line); border-radius: 10px; overflow: hidden; cursor: zoom-in; background: #0d100e; }
.gallery img { display: block; width: 100%; aspect-ratio: 16 / 9; object-fit: cover; }
.gallery figcaption { font-size: 13.5px; color: var(--muted); }
""" + room3d_page.CSS + """
</style>"""


TABS = [("overview", "Overview"), ("room", "Room in 3D"), ("views", "Drawn views"), ("wall", "Media wall"), ("dining", "Dining table"), ("paint", "Paint & light"),
        ("network", "Network & power"), ("build", "Build steps"), ("buy", "Buy & costs"), ("questions", "Questions"), ("checks", "Checks & sources")]
TAB_GROUPS = {"overview": "See it", "wall": "The plan", "build": "Do it", "questions": "Your input"}   # v14: the tab bar in four groups
CAP3D = {"3d_window_A_folded": "From the window, everyday evening: the table folded on the chimney breast",
         "3d_window_B_four": "Option B from the window: the table down for four under your shelf by the stairs, set for dinner",
         "3d_wall_tv": "The media wall on TV night: bias light on, bar 1 off, the lamp on",
         "3d_sofa_records": "From the sofa, the records scene: light on the deck, the ledge and the trays",
         "3d_B_folded": "Option B folded: about 6 cm deep under your shelf, everyday evening",
         "3d_stairs_A_four": "From the stairs: the table down for four on the breast",
         "3d_dining_A_four": "Option A: down for four on the chimney breast",
         "3d_dining_B_four": "Option B: down for four under the shelf, bar 2 right over it",
         "3d_six_day": "Out for six with the leaf, in daylight",
         "3d_pc_day": "The PC side wall in daylight",
         "3d_plan_B": "Bird\u2019s eye, option B set for four",
         "3d_doll_A": "Dolls\u2019 house view, option A"}


def options_card():
    """v14: the table's two places side by side, with a way into the 3D room for each."""
    g = G
    south, north = g.STAIRS_WALL_Z[0] - g.TABLE_B_Z[0], g.TABLE_B_Z[1] - g.WINDOW_Z
    def btn(opts, lab):
        return f"<button type=\"button\" class=\"btn\" data-r3d='{json.dumps(opts)}'>{lab}</button>"
    a = btn({"site": "A", "dining": "four", "view": "dining", "scene": "dinner"}, "See A in 3D")
    b = btn({"site": "B", "dining": "four", "view": "dining", "scene": "dinner"}, "See B in 3D")
    return f"""<div class="opts">
  <article class="opt"><img data-art="3d_dining_A_four" alt="Option A in 3D: the table down for four on the chimney breast" loading="lazy">
    <div class="ob"><span class="label">Option A · the plan so far</span><h3>On the chimney breast</h3>
    <ul><li>Bar 1 and bar 2 already planned round it; the framed LPs over it.</li><li>Solid breast: plugs and screws, no surprises.</li>
    <li class="minus">The west-end chair sits in the door's swing.</li></ul>{a}</div></article>
  <article class="opt"><img data-art="3d_dining_B_four" alt="Option B in 3D: the table down for four under the shelf by the stairs" loading="lazy">
    <div class="ob"><span class="label">Option B · new in v14</span><h3>Under your shelf, by the stairs</h3>
    <ul><li>Out of the door's swing; the pendant point is right over it.</li><li>Frees the breast; the dresser goes, the lamp moves.</li>
    <li class="minus">End chairs tight: {south - g.CHAIR[1]:.0f} and {north - g.CHAIR[1]:.0f} cm behind them.</li><li class="minus">Wall's build unknown: knock first.</li></ul>{b}</div></article>
</div>"""


def gallery3d():
    figs = "".join(f'<figure><button type="button" class="g3d" data-full="{k}"><img data-art="{k}" alt="{html.escape(CAP3D[k])}" loading="lazy"></button>'
                   f'<figcaption>{html.escape(CAP3D[k])}</figcaption></figure>' for k, *_ in SHOTS3D)
    return f'<div class="gallery">{figs}</div>'

TABNAME = dict(TABS)
SEC_TAB = {"1": "overview", "2": "overview", "3": "wall", "4": "wall", "5": "dining", "6": "wall", "7": "wall", "8": "paint",
           "9": "network", "10": "build", "11": "buy", "12": "checks"}


def _tablink(tab):
    return f'<a href="#{tab}" data-go="{tab}">{TABNAME[tab]}</a> tab'


def scenes_block():
    """v13.7: the lighting scenes as buttons: one scene's drawing and notes at a time."""
    import scenes as SC
    import diagrams as D
    btns = "".join(f'<button type="button" data-scene="{k}" aria-pressed="{"true" if i == 0 else "false"}">{html.escape(name)}</button>'
                   for i, (k, name, *_r) in enumerate(SC.SCENES))
    panes = "".join(f'<div class="scene" data-sc="{k}"{"" if i == 0 else " hidden"}><figure><svg-placeholder/>{D.light_scene(k)}</figure>'
                    f'<ul>{"".join(f"<li>{x}</li>" for x in notes)}</ul></div>'
                    for i, (k, name, desc, lv, notes) in enumerate(SC.SCENES))
    return (f'<div class="scenes"><div class="seg" role="group" aria-label="Lighting scene" id="scene-btns">{btns}</div>{panes}</div>').replace("<svg-placeholder/>", "")


def deck_section(html_):
    """A plan section made fit for a tab: cross-references become tab links, wide tables scroll, drawings sit on paper."""
    html_ = re.sub(r"<!--fit-->.*?<!--/fit-->", f'<p class="notice">Every zone\'s checks, with a filter for the tight ones, are in the {_tablink("checks")}.</p>', html_, flags=re.S)
    html_ = re.sub(r"<!--confirm-->.*?<!--/confirm-->", "", html_, flags=re.S)
    html_ = re.sub(r"<!--scenes-->.*?<!--/scenes-->", lambda m: scenes_block(), html_, flags=re.S)
    html_ = html_.replace("Full-resolution renders come with this plan.", f"Switch views and greens in the {_tablink('views')}.")
    html_ = html_.replace("need a check on site (section 3)", f"need a check on site ({_tablink('checks')})")
    html_ = re.sub(r"\(section (\d+)\)", lambda m: "(" + _tablink(SEC_TAB[m.group(1)]) + ")", html_)
    html_ = re.sub(r"\bsection (\d+)\b", lambda m: "the " + _tablink(SEC_TAB[m.group(1)]), html_)
    html_ = html_.replace("<figure><svg", '<figure class="dia"><svg')
    html_ = html_.replace("<table", '<div class="tscroll"><table').replace("</table>", "</table></div>")
    return html_


def phase_data(rows):
    phases = []
    for r in rows:
        if r["phase"] not in [p["name"] for p in phases]:
            phases.append({"name": r["phase"], "lo": 0, "hi": 0, "n": 0})
        p = next(p for p in phases if p["name"] == r["phase"])
        p["lo"] += r["lo"]; p["hi"] += r["hi"]; p["n"] += 1
    first = {}
    for s in steps():
        for ph in s["buy"]:
            first.setdefault(ph, s["n"])
    run_lo = run_hi = 0
    for i, p in enumerate(phases):
        run_lo += p["lo"]; run_hi += p["hi"]
        p.update(idx=i, step=first.get(p["name"]), run=(run_lo, run_hi), label=re.sub(r"^\d+ ", "", p["name"]))
    return phases


def cost_chart(phases):
    step = 200
    top = step * -(-max(p["hi"] for p in phases) // step)
    pct = lambda v: f"{100 * v / top:.2f}%"
    rows = []
    for p in phases:
        val = f"£{money(p['lo'], p['hi'])}" if p["hi"] else "no cost"
        rows.append(
            f'<div class="crow" data-ph="{p["idx"]}"><a class="cl" href="#buy" data-go="buy" data-phase="{p["idx"]}">{html.escape(p["label"])}'
            f'<small>{"before step " + str(p["step"]) if p["step"] else ""}</small></a>'
            f'<div class="ctrack" style="--n:{top // step}"><span class="clo" style="width:{pct(p["lo"])}"></span>'
            f'<span class="chi" style="left:{pct(p["lo"])};width:{pct(p["hi"] - p["lo"])}"></span><span class="cpaid" style="width:0"></span></div>'
            f'<span class="cv">{val}<small class="cpv"></small></span></div>')
    ticks = "".join(f'<span style="left:{pct(v)}">£{v:,}</span>' for v in range(0, top + 1, step))
    return (f'<div class="chart" role="img" aria-label="Estimated cost of each build phase, low to high, on one scale from £0 to £{top:,}, with the amount paid so far">'
            + "".join(rows) + f'<div class="crow axis" aria-hidden="true"><span></span><div class="caxis">{ticks}</div><span></span></div>'
            '<p class="legend"><span><i class="k-lo"></i>Low estimate</span><span><i class="k-hi"></i>Up to the high estimate</span><span><i class="k-pd"></i>Paid so far</span></p></div>')


def uniq_svgs(html_):
    """Give every inline drawing its own ids: the same drawing can appear twice (in its tab and in a build step), and a
    pattern or gradient defined in a hidden tab doesn't paint in a visible one."""
    count = [0]
    def one(m):
        count[0] += 1
        svg, tag = m.group(0), f"d{count[0]}"
        for i in set(re.findall(r'id="([^"]+)"', svg)):
            svg = (svg.replace(f'id="{i}"', f'id="{tag}-{i}"').replace(f"url(#{i})", f"url(#{tag}-{i})")
                   .replace(f'href="#{i}"', f'href="#{tag}-{i}"'))
        return svg
    return re.sub(r"<svg\b.*?</svg>", one, html_, flags=re.S)


def page(site=False):
    import diagrams as D
    prefix = "media-wall/src/" if site else ""
    imgs = {k: f"{prefix}art/{k}.webp" for k in [f"art_{s}_{p}" for s in ("join", "four", "six", "side", "drawers") for p in ("card_room", "deep", "sage", "treron")] + ["key_join", "doc_paint", "doc_skirt"]}
    imgs.update({f"dims_{v}": f"{prefix}art/dims_{v}.webp" for v in ("join", "four", "six", "drawers", "side")})
    imgs.update({k: f"{prefix}art/{k}.webp" for k, *_ in SHOTS3D})
    rows = track_rows()
    phases = phase_data(rows)
    _, lo_tot, hi_tot = phase_totals()
    fit_head, fit_body, fc = fit_html()
    nfit = sum(fc.values())
    sec = {k: deck_section(v) for k, v in plan_sections().items()}
    pre = sec["pre"]
    decision = re.search(r'<div class="decision">(.*?)</div>', pre, re.S).group(1)
    s1 = re.sub(r"</div>\s*$", "", sec["1"].strip())
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
    for p in phases:
        items = [r for r in rows if r["phase"] == p["name"]]
        lis = "".join(
            f'<li data-t="{r["id"]}" data-kind="{r["kind"]}"><input type="checkbox" id="c-{r["id"]}" aria-label="Done"><label class="txt" for="c-{r["id"]}">{r["item"]}'
            f'<span class="meta">{"Qty " + html.escape(r["qty"]) + " · " if r["qty"] else ""}{"Estimate £" + r["est"] if r["est"] and r["est"] != "Quote" else ("Quote" if r["est"] else "Job")}</span></label>'
            + (f'<span class="paid"><label for="p-{r["id"]}">Paid £</label><input id="p-{r["id"]}" type="number" min="0" step="0.01" inputmode="decimal"></span>' if r["kind"] == "buy" or r["est"] == "Quote" else "<span></span>")
            + "</li>" for r in items)
        when = f' · <a href="#build" data-go="build" data-step="{p["step"]}">before step {p["step"]}</a>' if p["step"] else ""
        cost = f"£{money(p['lo'], p['hi'])}" if p["hi"] else "jobs only"
        ph_html.append(f'<details class="phase" id="ph-{p["idx"]}" data-ph="{html.escape(p["name"])}"{" open" if p["idx"] == 0 else ""}><summary><span>{part_chip(PHASE_PART[p["name"]])} {html.escape(p["name"])}</span>'
                       f'<span class="pf"><span>{cost}{when}</span><span class="pd">0 of {len(items)} done</span></span></summary><ul class="items">{lis}</ul></details>')
    step_cards = []
    for s in steps():
        buy = "".join(f'<a class="chip" href="#buy" data-go="buy" data-phase="{p["idx"]}">{html.escape(p["label"])} · {"£" + money(p["lo"], p["hi"]) if p["hi"] else "jobs"}</a>'
                      for p in phases if p["name"] in s["buy"])
        see = " · ".join(f'<a href="#{t}" data-go="{t}" data-find="{html.escape(lab)}">{html.escape(lab)}</a>' for t, lab in s["see"])
        step_cards.append(
            f'<li class="step" id="step-{s["n"]}" data-s="{s["n"]}" data-parts="{html.escape("|".join(s["part"]))}"><div class="shead"><span class="sn">{s["n"]}</span>'
            f'<div><p class="sparts">{part_chip(s["part"])}</p><h3>{html.escape(s["title"])}</h3><span class="smeta">{html.escape(s["who"])} · {html.escape(s["time"])}</span></div>'
            f'<label class="sdone" for="sd-{s["n"]}"><input type="checkbox" id="sd-{s["n"]}"> Done</label></div>'
            + (f'<p class="sbuy"><span class="label">Buy first</span>{buy}</p>' if buy else "")
            + need_html(s)
            + ("<details class=\"sdraw\" open><summary>" + ("Drawing" if len(s.get("draw", [])) == 1 else "Drawings") + " for this step</summary>"
               + "".join(f'<figure class="dia">{getattr(D, DIAGRAMS[d])()}</figure>' for d in s["draw"]) + "</details>" if s.get("draw") else "")
            + f'<div class="sfull">{full_html(s)}</div>'
            f'<p class="scheck"><b>Check before moving on:</b> {s["check"]}</p>'
            f'<p class="ssee">Also see: {see}</p></li>')
    run_list = "".join(
        f'<li><a href="#build" data-go="build" data-step="{s["n"]}"><span class="rn">{s["n"]}</span>{html.escape(s["title"])}</a><span class="rp">{part_chip(s["part"])}</span>'
        f'<span class="rm">{html.escape(s["time"])}{"".join(" · " + html.escape(p["label"]) + (" £" + money(p["lo"], p["hi"]) if p["hi"] else "") for p in phases if p["name"] in s["buy"])}</span></li>'
        for s in steps())
    data = {"img": imgs, "q": qs, "track": [{k: r[k] for k in ("id", "phase", "lo", "hi", "done", "kind")} for r in rows],
            "phases": [{k: p[k] for k in ("name", "idx", "lo", "hi")} for p in phases], "top": 200 * -(-max(p["hi"] for p in phases) // 200),
            "steps": len(steps()), "tabs": [t for t, _ in TABS]}
    used = [k for k in PARTS if any(k in st["part"] for st in steps())]
    part_buttons = "".join(f'<button type="button" data-part="{html.escape(k)}" aria-pressed="false"><span class="dot" style="background:{PARTS[k]}"></span>{html.escape(k)}</button>' for k in used)
    tabs = "".join((f'<span class="tg" aria-hidden="true">{TAB_GROUPS[t]}</span>' if t in TAB_GROUPS else "")
                   + f'<button type="button" role="tab" id="tb-{t}" aria-controls="{t}" aria-selected="{"true" if t == "overview" else "false"}"{"" if t == "overview" else " tabindex=\"-1\""}>{lab}</button>' for t, lab in TABS)
    files_line = (f'Print copies of this plan (PDF) and the HD renders are also kept in the project folder on '
                  f'<a href="{GITHUB_OUT}" target="_blank" rel="noopener">GitHub, media-wall/out/</a>; you don\'t need them to use this page.')
    return uniq_svgs(f"""<title>Portsmouth Close Media Wall</title>
{room3d_page.IMPORTMAP}
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Atkinson+Hyperlegible:wght@400;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
{STYLE}
<div class="wrap">
  <header>
    <p class="eyebrow">Portsmouth Close · living room · v{VERSION} · 20 Oct 2026</p>
    <h1>Media Wall &amp; Home Network Plan</h1>
    <p class="lede">The whole plan in one place: the artisan oak wall in Card Room Green, the fold-down dining table (now with a second place to put it), the network and power, step-by-step build instructions and the buy list. Walk round it all in the <a href="#room" data-go="room">3D room</a>. Ticks, amounts and answers save for both of you.</p>
  </header>
  <nav class="tabs" aria-label="Plan sections"><div class="tl" role="tablist">{tabs}</div></nav>

  <section class="panel" id="overview" role="tabpanel" aria-labelledby="tb-overview">
    <div class="dash">
      <a class="dcard d3d" href="#room" data-go="room"><img data-art="3d_window_A_folded" alt="The room in 3D, from the window" loading="lazy"><span>Walk round your room in 3D \u2192</span></a>
      <div class="dcard"><span class="label">Build</span><strong id="d-steps">0 of {len(steps())}</strong><span class="dbar"><i id="d-steps-bar"></i></span><a class="caption" id="d-next" href="#build" data-go="build">Start with step 1</a></div>
      <div class="dcard"><span class="label">Buy list</span><strong id="d-buy">0 bought</strong><span class="dbar"><i id="d-buy-bar"></i></span><span class="caption" id="d-paid">\u00a30 paid so far, of about \u00a3{money(lo_tot, hi_tot)}</span></div>
      <div class="dcard"><span class="label">Your answers</span><strong id="d-q">0 of {len(QUESTIONS)}</strong><span class="dbar"><i id="d-q-bar"></i></span><a class="caption" href="#questions" data-go="questions">Answer what we still need</a></div>
    </div>
    <div class="block"><div class="qhead"><h2>Two places for the table</h2><a class="btn" href="#dining" data-go="dining" data-find="Two places">Compare them in full</a></div>
      <p class="caption">Same table, same build: it hangs on the chimney breast (A) or on the wall going up the stairs, under your 2 m shelf (B). Everything else can move round it.</p>
      {options_card()}</div>
    <div class="doc">
      <h2>The plan on a page</h2>
      {s1}
    </div>
    <div class="block">
      <div class="qhead"><h2>How the build runs</h2><a class="btn" href="#build" data-go="build">Open the build steps</a></div>
      <p class="caption">Thirteen steps in order, each labelled with its part of the house, with what to buy before each. Total about £{money(lo_tot, hi_tot)}, with no electrician on top: the electrics are your own job (steps 3 and 12). The cost of each phase is charted in the {_tablink("buy")}.</p>
      <ol class="runlist">{run_list}</ol>
    </div>
    <details class="changes"><summary>What changed: v{VERSION}, and every round before it</summary><div class="doc">
      <p>{decision}</p>
      <p><b>On this page:</b> the plan, every drawing, the build steps and the buy list now live here in tabs, with the cost of each phase charted against what you've paid, so nothing needs downloading from GitHub.</p>
    </div></details>
    <div class="doc"><h2>The room</h2>{sec["2"]}</div>
  </section>

  <section class="panel" id="room" role="tabpanel" aria-labelledby="tb-room" hidden>
    <div class="qhead"><h2 class="ptitle">Your room in 3D</h2><span class="caption">Drag to look round · scroll or pinch to zoom · right-drag or two fingers to slide</span></div>
    <p class="caption">Built from the plan's own measurements: every shelf, drawer, console and record in the wall is the HD renders' geometry, in your real room (alcove 186 \u00d7 38, ceiling 235). Choose where the table goes and how it's set, the lighting scene, the paint (or any colour), where the floor lamp stands (it stays; it's on or off) and whether the drawers are out, then pick a camera or move your own. Save any view as an HD picture.</p>
    {room3d_page.section()}
    <h3 class="ptitle">HD pictures from the 3D room</h3>
    <p class="caption">Rendered at 2560 \u00d7 1440; tap one to see it full size. The same set is in the project folder.</p>
    {gallery3d()}
  </section>

  <section class="panel" id="views" role="tabpanel" aria-labelledby="tb-views" hidden>
  <div class="viewer">
    <div class="frame shotwrap"><img id="shot" alt="Render of the media wall" width="3300" height="2100"><img id="dims" class="dims" alt="" width="3300" height="2100" hidden></div>
    <div class="controls">
      <div class="group"><span class="label" id="l-style">View</span>
        <div class="seg" role="group" aria-labelledby="l-style">
          <button id="s-join" data-style="join" aria-pressed="true">Artisan oak (main)</button>
          <button id="s-four" data-style="four" aria-pressed="false">Dining, four at the wall</button>
          <button id="s-six" data-style="six" aria-pressed="false">Dining, six in the room</button>
          <button id="s-side" data-style="side" aria-pressed="false">PC side wall</button>
          <button id="s-drawers" data-style="drawers" aria-pressed="false">Drawers open</button>
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
          <button id="k-dims" aria-pressed="false">Show measurements</button>
        </div></div>
      <div class="group"><span class="label" id="l-zoom">HD</span>
        <div class="seg" role="group" aria-labelledby="l-zoom">
          <button id="k-full" type="button">View full size</button>
        </div></div>
    </div>
    <p class="caption" id="cap"></p>
  </div>
  <div class="lightbox" id="lightbox" hidden role="dialog" aria-modal="true" aria-label="The render at full size">
    <div class="lbbar"><span class="caption" id="lb-cap">Full size: drag or scroll to look round. Pinch to zoom on a phone.</span><button class="btn" id="lb-close" type="button">Close</button></div>
    <div class="lbscroll" id="lb-scroll"><div class="lbwrap"><img id="lb-img" alt=""><img id="lb-dims" alt="" hidden></div></div>
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
      <p class="caption">The numbered key works on the main view. Measurements are rough, in pale yellow, for checking against the real room; the drawings in the other tabs are the exact ones.</p>
    </section>
  </div>
  </section>

  <section class="panel" id="wall" role="tabpanel" aria-labelledby="tb-wall" hidden>
    <nav class="toc" aria-label="On this tab"></nav>
    <div class="doc"><h2>The media wall</h2>{sec["3"]}<h2>The records and the turntable</h2>{sec["4"]}<h2>The side wall</h2>{sec["6"]}<h2>The oak joinery</h2>{sec["7"]}</div>
  </section>

  <section class="panel" id="dining" role="tabpanel" aria-labelledby="tb-dining" hidden>
    <nav class="toc" aria-label="On this tab"></nav>
    <div class="block"><h2 class="ptitle">Two places for the table</h2>{options_card()}</div>
    <div class="doc"><h2>The dining wall</h2>{sec["5"]}</div>
  </section>

  <section class="panel" id="paint" role="tabpanel" aria-labelledby="tb-paint" hidden>
    <div class="doc"><h2>Paint and light</h2>{sec["8"]}</div>
  </section>

  <section class="panel" id="network" role="tabpanel" aria-labelledby="tb-network" hidden>
    <nav class="toc" aria-label="On this tab"></nav>
    <div class="doc"><h2>Power, cables and network</h2>{sec["9"]}</div>
  </section>

  <section class="panel" id="build" role="tabpanel" aria-labelledby="tb-build" hidden>
    <div class="doc"><h2>Build steps, for a first-time builder</h2>{GUIDE_RULES}</div>
    <div class="qhead"><h2>The order of work</h2><div class="meter"><span class="bar"><i id="s-bar"></i></span><span id="s-count">0 of {len(steps())} steps done</span></div></div>
    <p class="caption" id="s-note">Tick each step when it's done; it saves for both of you. "Buy first" opens that part of the buy list.</p>
    <div class="group pfilter"><span class="label" id="l-part">Show one part</span>
      <div class="seg" role="group" aria-labelledby="l-part" id="part-filter"><button type="button" data-part="" aria-pressed="true">All parts</button>{part_buttons}</div>
      <p class="caption" id="pf-note" aria-live="polite"></p></div>
    <ol class="steps-list">{"".join(step_cards)}</ol>
    <div class="block" id="cuts">
      <div class="qhead"><h2 class="ptitle">Cutting list for the timber merchant</h2><div class="row"><button class="btn" id="copy-cuts" type="button">Copy as text</button><span class="caption" id="cuts-st" aria-live="polite"></span></div></div>
      <textarea id="cuts-box" class="caption" rows="8" hidden readonly aria-label="The cutting list as text">{html.escape(cuts_text())}</textarea>
      <div class="doc">{deck_section(cuts_html())}</div>
    </div>
    <div class="doc">{GUIDE_TIME}{guide_tools()}{GUIDE_TECHNIQUES}{GUIDE_PITFALLS}</div>
  </section>

  <section class="panel" id="buy" role="tabpanel" aria-labelledby="tb-buy" hidden>
    <h2 class="ptitle">Buy guide and costs</h2>
    <div class="tiles">
      <div><strong>£{money(lo_tot, hi_tot)}</strong><span>the whole plan; no electrician on top</span></div>
      <div><strong id="t-left">£{money(lo_tot, hi_tot)}</strong><span>still to buy: the items not ticked yet</span></div>
      <div><strong id="t-paid">£0</strong><span>paid so far, from the amounts you enter</span></div>
      <div><strong id="t-done">0 of {len(rows)}</strong><span>items and jobs ticked off</span></div>
    </div>
    <h3 class="ptitle">Cost by phase</h3>
    {cost_chart(phases)}
    <div class="qhead"><h3 class="ptitle">The buy list, in build order</h3>
      <div class="seg" role="group" aria-label="Show">
        <button type="button" data-filter="all" aria-pressed="true">Everything</button>
        <button type="button" data-filter="left" aria-pressed="false">Still to buy</button>
        <button type="button" data-filter="jobs" aria-pressed="false">Jobs only</button>
      </div></div>
    <p class="caption" id="t-note">Each phase says which build step it's needed for. Tick each item off and write in what you paid; it saves for both of you.</p>
    <div id="tracker">{"".join(ph_html)}</div>
    <p class="notice">Already owned: Virgin Hub 5, three Deco X1500s, two TL-SG105S switches (both become spares), LG OLED C6 55" and its stand, a 10-gang, the Hisense AX5100G 5.1 soundbar, the Series X fan stand, the turntable, the L-sofa and all the consoles. Estimates are approximate UK prices.</p>
  </section>

  <section class="panel" id="questions" role="tabpanel" aria-labelledby="tb-questions" hidden>
    <div class="qhead"><h2 class="ptitle">What we still need from you</h2><div class="meter"><span class="bar"><i id="q-bar"></i></span><span id="q-count">0 of {len(QUESTIONS)} answered</span></div></div>
    <p class="caption">{len(QUESTIONS)} things only you can tell us, the ones that change the drawings first. Answers saved here reach both of you and the next round of the plan. A photo is often quicker than words.</p>
    <p class="notice" id="q-local" hidden>Answers can't be saved for both of you from this view: they're kept on this device. When you're done, use Copy all answers and paste them into a message.</p>
    <p class="notice" id="q-ro" hidden>You can read the answers here but not change them. Ask Emma to give you Contributor access in the Share menu.</p>
    <ul class="qs">
{q_items}
    </ul>
    <div class="row"><button class="btn" id="copy-all" type="button">Copy all answers</button><span class="caption" id="copy-st" aria-live="polite"></span></div>
    <textarea id="copy-box" class="caption" rows="6" hidden readonly aria-label="All answers as text"></textarea>
  </section>

  <section class="panel" id="checks" role="tabpanel" aria-labelledby="tb-checks" hidden>
    <h2 class="ptitle">Fit proof</h2>
    <p class="caption">Every item in the wall against its published size: {fc[fit.PASS]} of {nfit} fit outright, {fc[fit.TIGHT]} are tight and {fc[fit.CHECK]} need a check on site. Source numbers refer to the Sources list below.</p>
    <div class="qhead">{fit_head}<button class="btn" id="fit-only" type="button" aria-pressed="false">Show only tight and to-check</button></div>
    <div id="fit-zones">{fit_body}</div>
    <div class="doc"><p class="notice">Still to confirm: the open questions, with a box for each answer, are in the {_tablink("questions")}.</p>{sec["12"]}<h2>Options we set aside</h2>{sec["appendix"]}<p class="note">{files_line}</p></div>
  </section>
</div>
<script>
const DATA = {json.dumps(data)};
const SITE = {json.dumps(site)};
const use = n => (window.claude && window.claude.use) ? window.claude.use(n) : Promise.resolve(null);
const $ = (s, el = document) => el.querySelector(s), $$ = (s, el = document) => [...el.querySelectorAll(s)];
const store = {{ get(k, d) {{ try {{ const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; }} catch (e) {{ return d; }} }},
                set(k, v) {{ try {{ localStorage.setItem(k, JSON.stringify(v)); }} catch (e) {{}} }} }};

/* ---------- pictures borrowed from the viewer's set (each embedded once) */
$$("img[data-art]").forEach(im => {{ const u = DATA.img[im.dataset.art]; if (u) im.src = u; }});

/* ---------- tabs */
const tabBtns = $$('[role="tab"]');
function showTab(id, focus) {{
  if (!DATA.tabs.includes(id)) id = "overview";
  tabBtns.forEach(b => {{ const on = b.getAttribute("aria-controls") === id; b.setAttribute("aria-selected", String(on)); b.tabIndex = on ? 0 : -1; if (on && focus) b.focus(); if (on) b.scrollIntoView({{ block: "nearest", inline: "nearest" }}); }});
  DATA.tabs.forEach(t => {{ document.getElementById(t).hidden = t !== id; }});
  store.set("mw13-tab", id);
  try {{ history.replaceState(null, "", "#" + id); }} catch (e) {{}}
}}
tabBtns.forEach((b, i) => {{
  b.addEventListener("click", () => {{ showTab(b.getAttribute("aria-controls")); window.scrollTo({{ top: 0 }}); }});
  b.addEventListener("keydown", e => {{
    const k = {{ ArrowRight: 1, ArrowLeft: -1 }}[e.key];
    if (k) {{ e.preventDefault(); showTab(tabBtns[(i + k + tabBtns.length) % tabBtns.length].getAttribute("aria-controls"), true); }}
  }});
}});
function jumpTo(el) {{ if (el) requestAnimationFrame(() => el.scrollIntoView({{ block: "start" }})); }}
document.addEventListener("click", e => {{
  const a = e.target.closest("[data-go]");
  if (!a) return;
  e.preventDefault();
  const tab = a.dataset.go;
  showTab(tab);
  const panel = document.getElementById(tab);
  if (a.dataset.step) {{ jumpTo(document.getElementById("step-" + a.dataset.step)); return; }}
  if (a.dataset.phase) {{ const d = document.getElementById("ph-" + a.dataset.phase); d.open = true; jumpTo(d); return; }}
  if (a.dataset.find) {{ const h = $$("h2, h3, h4", panel).find(h => h.textContent.includes(a.dataset.find)); if (h) {{ jumpTo(h); return; }} }}
  window.scrollTo({{ top: 0 }});
}});
/* on-this-tab chips for the long tabs */
$$(".toc").forEach(nav => {{
  const hs = $$(".doc h2, .doc h3", nav.parentElement);
  hs.forEach((h, i) => {{
    const b = document.createElement("button"); b.type = "button"; b.className = "chip" + (h.tagName === "H2" ? " h2" : "");
    b.textContent = h.textContent.replace(/:.*$/, ""); b.addEventListener("click", () => jumpTo(h));
    nav.appendChild(b);
  }});
}});
showTab((location.hash || "").slice(1) || store.get("mw13-tab", "overview"));

/* ---------- the render viewer */
const NAMES = {{ card_room: "Farrow & Ball Card Room Green No. 79, the chosen colour", treron: "Farrow & Ball Treron No. 292", sage: "Little Greene Sage Green No. 80", deep: "the deep forest green from earlier versions" }};
const VIEWS = {{ join: "Artisan oak media wall", four: "The dining wall, down and set for four", six: "The table and its leaf set for six, with both spot bars", side: "The PC side wall, seen from the room", drawers: "Every drawer out" }};
const view = Object.assign({{ style: "join", paint: "card_room", key: false, dims: false }}, store.get("mw13-view", {{}}));
const shot = $("#shot"), cap = $("#cap"), keyBtn = $("#k-key"), dims = $("#dims"), dimsBtn = $("#k-dims");
function draw() {{
  if (!VIEWS[view.style]) view.style = "join";
  if (view.style !== "join") view.key = false;
  shot.src = view.key ? DATA.img["key_" + view.style] : DATA.img["art_" + view.style + "_" + view.paint];
  shot.alt = VIEWS[view.style] + (view.key ? " with numbered key" : " in " + NAMES[view.paint]);
  $$("[data-style]").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.style === view.style)));
  $$("[data-paint]").forEach(b => {{ b.setAttribute("aria-pressed", String(!view.key && b.dataset.paint === view.paint)); b.disabled = view.key; }});
  keyBtn.setAttribute("aria-pressed", String(view.key));
  keyBtn.disabled = view.style !== "join";
  dims.src = DATA.img["dims_" + view.style];
  dims.hidden = !view.dims || view.key;
  dimsBtn.setAttribute("aria-pressed", String(view.dims && !view.key));
  dimsBtn.disabled = view.key;
  cap.textContent = view.key
    ? ("Full numbered key for the artisan oak build, in Card Room Green. Game drawer and lower record tray pulled out 30 cm. Dashed lines are hidden: gold for data, audio and low-voltage leads, coral for mains. The numbers are listed in the Media wall tab.")
    : view.style === "six" ? "The table and its leaf (170 × 80) on legs, 75 cm off the breast, set for six, in " + NAMES[view.paint] + ". The camera stands in line with the alcove's edge so both spot bars show; the stairs go up beside the door; their direction is drawn roughly until you send a photo."
    : view.style === "drawers" ? "Every drawer out, in " + NAMES[view.paint] + ": the game drawer and the upper record tray 30 cm out, the hidden plinth drawer 25 cm out. In use, open one record tray at a time."
    : view.style === "side" ? "The PC side wall in " + NAMES[view.paint] + ": the ledge round the corner, the PC on its shelf with the keyboard tray, its leads inside the wall, the sofa below; dashed, the chimney breast's outline and the alcove's depth: 38 of the 46 cm base inside it, 8 proud; the media wall end-on at the right (the breast cut away)."
    : VIEWS[view.style] + ", shown in " + NAMES[view.paint] + ". Evening light, drawn to the measured room.";
  store.set("mw13-view", view);
}}
$$("[data-style]").forEach(b => b.addEventListener("click", () => {{ view.style = b.dataset.style; draw(); }}));
$$("[data-paint]").forEach(b => b.addEventListener("click", () => {{ view.paint = b.dataset.paint; draw(); }}));
keyBtn.addEventListener("click", () => {{ view.key = !view.key; draw(); }});
dimsBtn.addEventListener("click", () => {{ view.dims = !view.dims; draw(); }});
draw();

/* ---------- full size (HD) */
const lb = $("#lightbox"), lbImg = $("#lb-img"), lbDims = $("#lb-dims"), lbScroll = $("#lb-scroll");
$("#k-full").addEventListener("click", () => {{
  lbImg.src = shot.src; lbImg.alt = shot.alt;
  lbDims.src = dims.src; lbDims.hidden = dims.hidden;
  lb.hidden = false; document.body.style.overflow = "hidden";
  requestAnimationFrame(() => {{ lbScroll.scrollLeft = (lbScroll.scrollWidth - lbScroll.clientWidth) / 2; lbScroll.scrollTop = (lbScroll.scrollHeight - lbScroll.clientHeight) / 2; }});
  $("#lb-close").focus();
}});
function closeLb() {{ lb.hidden = true; document.body.style.overflow = ""; $("#k-full").focus(); }}
$("#lb-close").addEventListener("click", closeLb);
document.addEventListener("keydown", e => {{ if (e.key === "Escape" && !lb.hidden) closeLb(); }});
let drag = null;
lbScroll.addEventListener("pointerdown", e => {{ if (e.pointerType === "mouse") {{ drag = {{ x: e.clientX, y: e.clientY, l: lbScroll.scrollLeft, t: lbScroll.scrollTop }}; lbScroll.setPointerCapture(e.pointerId); }} }});
lbScroll.addEventListener("pointermove", e => {{ if (drag) {{ lbScroll.scrollLeft = drag.l - (e.clientX - drag.x); lbScroll.scrollTop = drag.t - (e.clientY - drag.y); }} }});
lbScroll.addEventListener("pointerup", () => {{ drag = null; }});

/* ---------- fit proof filter */
$("#fit-only").addEventListener("click", e => {{
  const on = e.currentTarget.getAttribute("aria-pressed") !== "true";
  e.currentTarget.setAttribute("aria-pressed", String(on));
  $("#fit-zones").classList.toggle("fitonly", on);
  $$("#fit-zones details.zone").forEach(d => {{ if (on && d.querySelector("tr.r-tight, tr.r-check")) d.open = true; }});
}});

/* ---------- v14: the overview's dashboard, read from the page's own state */
function dash() {{
  const st = $$(".step"), sd = $$(".step.done"), next = st.find(x => !x.classList.contains("done"));
  $("#d-steps").textContent = sd.length + " of " + st.length + " steps";
  $("#d-steps-bar").style.width = (100 * sd.length / Math.max(1, st.length)) + "%";
  const nx = $("#d-next");
  if (next) {{ nx.textContent = "Next: " + next.dataset.s + ". " + $("h3", next).textContent; nx.dataset.step = next.dataset.s; }}
  else {{ nx.textContent = "Every step done"; delete nx.dataset.step; }}
  const bi = $$("#tracker li[data-kind=buy]"), bd = bi.filter(x => x.classList.contains("done"));
  $("#d-buy").textContent = bd.length + " of " + bi.length + " bought";
  $("#d-buy-bar").style.width = (100 * bd.length / Math.max(1, bi.length)) + "%";
  const paid = $$("#tracker .paid input").reduce((a, i) => a + (parseFloat(i.value) || 0), 0);
  $("#d-paid").textContent = "\u00a3" + Math.round(paid).toLocaleString("en-GB") + " paid so far";
  const qa = $$(".q.answered").length;
  $("#d-q").textContent = qa + " of " + DATA.q.length + " answered";
  $("#d-q-bar").style.width = (100 * qa / Math.max(1, DATA.q.length)) + "%";
}}
let dashQ = false;
const dashSoon = () => {{ if (!dashQ) {{ dashQ = true; requestAnimationFrame(() => {{ dashQ = false; dash(); }}); }} }};
new MutationObserver(dashSoon).observe($(".wrap"), {{ subtree: true, attributes: true, attributeFilter: ["class"] }});
document.addEventListener("input", dashSoon);
dash();
/* links into the 3D room with its options set */
document.addEventListener("click", e => {{
  const b = e.target.closest("[data-r3d]");
  if (!b) return;
  const o = JSON.parse(b.dataset.r3d);
  showTab("room"); window.scrollTo({{ top: 0 }});
  if (window.R3D) window.dispatchEvent(new CustomEvent("r3d-set", {{ detail: o }})); else window.__r3dPending = o;
}});
/* the 3D gallery opens in the full-size viewer */
$$(".g3d").forEach(b => b.addEventListener("click", () => {{
  const im = $("img", b);
  lbImg.src = im.src; lbImg.alt = im.alt; lbDims.hidden = true;
  lb.hidden = false; document.body.style.overflow = "hidden"; $("#lb-close").focus();
}}));

/* ---------- shared state: answers, photos, tracker, build steps */
let db = null, assets = null, user = null, myId = null, readOnly = false;
const remote = {{}};            // answers/<id> bodies as saved
const tstate = {{}};            // tracker/<id> bodies as saved
const sstate = {{}};            // steps/<n> bodies as saved
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
function lockInputs() {{ $$(".q textarea, .q .save, .items input, .sdone input").forEach(el => el.disabled = true); $$(".upl").forEach(el => el.hidden = true); }}
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

$("#copy-cuts").addEventListener("click", async () => {{
  const box = $("#cuts-box"), st = $("#cuts-st");
  try {{ await navigator.clipboard.writeText(box.value); st.textContent = "Copied. Paste it into an email to the timber merchant."; box.hidden = true; }}
  catch (e) {{ box.hidden = false; box.focus(); box.select(); st.textContent = "Select the text below and copy it."; }}
}});

/* tracker and the cost chart */
const local = store.get("mw12-tracker", {{}});
const money = v => "£" + (Math.round(v * 100) / 100).toLocaleString(undefined, {{ minimumFractionDigits: v % 1 ? 2 : 0, maximumFractionDigits: 2 }});
function tget(id) {{ return (db ? tstate[id] : local[id]) || null; }}
function paintTracker() {{
  let done = 0, paid = 0, leftLo = 0, leftHi = 0;
  const phPaid = {{}};
  DATA.track.forEach(r => {{
    const s = tget(r.id), isDone = s ? !!s.done : r.done;
    const li = document.querySelector('[data-t="' + r.id + '"]'), cb = li.querySelector("input[type=checkbox]"), pd = li.querySelector("input[type=number]");
    cb.checked = isDone; li.classList.toggle("done", isDone);
    if (pd && document.activeElement !== pd) pd.value = s && typeof s.paid === "number" ? s.paid : "";
    if (isDone) done++; else {{ leftLo += r.lo; leftHi += r.hi; }}
    if (s && typeof s.paid === "number") {{ paid += s.paid; phPaid[r.phase] = (phPaid[r.phase] || 0) + s.paid; }}
  }});
  $$("details.phase").forEach(d => {{
    const lis = $$(".items li", d), n = lis.filter(li => li.classList.contains("done")).length;
    $(".pd", d).textContent = n + " of " + lis.length + " done";
  }});
  DATA.phases.forEach(p => {{
    const row = document.querySelector('.crow[data-ph="' + p.idx + '"]'), v = phPaid[p.name] || 0;
    $(".cpaid", row).style.width = Math.min(100, 100 * v / DATA.top) + "%";
    $(".cpv", row).textContent = v ? "paid " + money(v) : "";
  }});
  $("#t-done").textContent = done + " of " + DATA.track.length;
  $("#t-paid").textContent = money(paid);
  $("#t-left").textContent = leftHi ? money(leftLo) + "–" + money(leftHi).slice(1) : "£0";
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
$$("[data-filter]").forEach(b => b.addEventListener("click", () => {{
  $$("[data-filter]").forEach(x => x.setAttribute("aria-pressed", String(x === b)));
  const t = $("#tracker");
  t.classList.toggle("f-left", b.dataset.filter === "left");
  t.classList.toggle("f-jobs", b.dataset.filter === "jobs");
  if (b.dataset.filter !== "all") $$("details.phase", t).forEach(d => d.open = true);
}}));
paintTracker();

/* build steps */
const slocal = store.get("mw13-steps", {{}});
function sget(n) {{ return (db ? sstate["s" + n] : slocal["s" + n]) || null; }}
function paintSteps() {{
  let done = 0;
  $$(".step").forEach(li => {{
    const s = sget(li.dataset.s), on = !!(s && s.done), cb = $(".sdone input", li);
    cb.checked = on; li.classList.toggle("done", on);
    if (on) done++;
  }});
  $("#s-count").textContent = done + " of " + DATA.steps + " steps done";
  $("#s-bar").style.width = (100 * done / DATA.steps) + "%";
}}
$$(".step").forEach(li => {{
  $(".sdone input", li).addEventListener("change", e => {{
    const body = {{ done: e.target.checked }};
    if (!db) {{ slocal["s" + li.dataset.s] = body; store.set("mw13-steps", slocal); paintSteps(); return; }}
    body.by = myId; body.at = new Date().toISOString();
    sstate["s" + li.dataset.s] = body; paintSteps();
    write("steps/s" + li.dataset.s, body).catch(err => onWriteError(err, null));
  }});
}});
paintSteps();

/* light up what this view can do */
(async () => {{
  const [d, u, a] = await Promise.all([use("db"), use("user"), use("assets")]);
  user = u;
  if (!d) {{
    $("#q-local").hidden = false;
    $("#t-note").textContent = "Each phase says which build step it's needed for. Ticks and amounts are kept on this device only from this view.";
    $("#s-note").textContent = "Tick each step when it's done; from this view the ticks are kept on this device only.";
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
  db.collection("steps").onSnapshot(snap => {{
    snap.docChanges().forEach(ch => {{ if (ch.type === "removed") delete sstate[ch.doc.id]; else sstate[ch.doc.id] = ch.doc.data(); }});
    paintSteps();
  }}, () => {{}});
}})();
(() => {{
  // v13.7: lighting scene buttons
  const sb = document.getElementById("scene-btns");
  if (!sb) return;
  sb.addEventListener("click", e => {{
    const b = e.target.closest("button[data-scene]"); if (!b) return;
    sb.querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", String(x === b)));
    document.querySelectorAll(".scene").forEach(d => {{ d.hidden = d.dataset.sc !== b.dataset.scene; }});
  }});
}})();
(() => {{
  // v13.6: show one part of the build at a time
  const bar = document.getElementById("part-filter");
  if (!bar) return;
  const note = document.getElementById("pf-note");
  const pick = part => {{
    bar.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.part === part)));
    let shown = 0;
    document.querySelectorAll(".steps-list > li.step").forEach(li => {{
      const on = !part || li.dataset.parts.split("|").includes(part);
      li.hidden = !on; if (on) shown++;
    }});
    note.textContent = part ? ("Showing " + shown + " of " + DATA.steps + " steps: " + part + ".") : "";
    try {{ localStorage.setItem("mw-part", part); }} catch (e) {{}}
  }};
  bar.addEventListener("click", e => {{ const b = e.target.closest("button[data-part]"); if (b) pick(b.dataset.part); }});
  document.addEventListener("click", e => {{
    const a = e.target.closest("[data-step]");
    if (a) {{ const li = document.getElementById("step-" + a.dataset.step); if (li && li.hidden) pick(""); }}
  }}, true);
  let saved = "";
  try {{ saved = localStorage.getItem("mw-part") || ""; }} catch (e) {{}}
  if (saved && bar.querySelector('button[data-part="' + saved.replace(/"/g, "") + '"]')) pick(saved);
}})();
</script>
""")


def site():
    """The same page for GitHub Pages at the repo root: a full document, paths into media-wall/, plain download links."""
    body = page(site=True).replace("body { background", "body { margin: 0; background", 1)
    head, rest = body.split("</style>", 1)
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + head + "</style>\n</head>\n<body>" + rest + "</body>\n</html>\n")


def publish_files():
    """{published path: source} for the Artifact publish: the viewer images and the downloads."""
    files = {f"art/{p.name}": str(p) for p in sorted((HERE / "art").glob("*.webp"))}
    if not DOWNLOADS_ON_GITHUB:
        files.update({published_name(p): str(p) for p, _, kind in downloads_list() if kind != "PDF"})
    return files


def inline_images(html_):
    """The artifact refuses some image uploads from an editor outside its organisation (false "cpio archive" sniffs), so the
    published copy carries its images as data URIs: media_wall_viewer_inline.html (gitignored), about 5 MB."""
    import base64
    for p in sorted((HERE / "art").glob("*.webp")):
        mime = "webp"
        uri = f"data:image/{mime};base64," + base64.b64encode(p.read_bytes()).decode()
        html_ = html_.replace(f"art/{p.name}", uri)
    return html_


def doc_images():
    """The two plan images that aren't renders, as JPEGs in art/ so the page carries each once."""
    from PIL import Image
    for src, key in (("paint_grid.png", "doc_paint"), ("skirting_options.png", "doc_skirt")):
        im = Image.open(HERE / src).convert("RGB")
        if im.width > 2400:
            im = im.resize((2400, round(im.height * 2400 / im.width)))
        im.save(HERE / "art" / f"{key}.webp", "WEBP", quality=86, method=6)


if __name__ == "__main__":
    doc_images()
    (HERE / "media_wall_viewer.html").write_text(page())
    (HERE / "media_wall_viewer_inline.html").write_text(inline_images(page()))
    (HERE.parent.parent / "index.html").write_text(site())
    (HERE / "publish_files.json").write_text(json.dumps(publish_files(), indent=1))
    print("viewer ok", len(publish_files()), "files")
