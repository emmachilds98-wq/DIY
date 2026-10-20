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
VERSION = "26"
DOWNLOADS_ON_GITHUB = True   # v13: the artifact refuses PDFs (and some large images) from an editor outside its organisation
PAGES = "https://emmachilds98-wq.github.io/DIY/"                  # v14.1: main is published with GitHub Pages
GITHUB_OUT = PAGES + "media-wall/out/"
DECK_URL = "https://claude.ai/artifact/71ffwf5PRLhoLj6G5KTvm2"
LPS = G.ALL_LPS   # v19: 291, the wall's 191 and the vinyl stand's 100
SINGLES = 2 * G.TRAY_SINGLES

# ---------------------------------------------------------------- the open questions, most consequential first
# (id, question, why it matters, how to check, a photo helps)
from questions import QUESTIONS   # v13.6: one list, shared with the plan PDF
import room3d_page                 # v14: the room in 3D
from shot3d import SHOTS as SHOTS3D


def _plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


# v25: rows whose words changed keep the id their old words made, so ticks and amounts saved against them still show
TRACK_KEEP_ID = {"Set up the smart bulbs in their app": "tdd8f66e8a569"}


def track_rows():
    rows = []
    for st, item, ph, q, lo, hi in TRACK:
        key = hashlib.sha1((ph + "|" + re.sub(r"\(changed[^)]*\)|\(new\)|\(moved[^)]*\)", "", _plain(item))).encode()).hexdigest()[:12]
        key = next((v[1:] for k, v in TRACK_KEEP_ID.items() if _plain(item).startswith(k)), key)
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
    for p in sorted(OUT.glob(f"Media wall v{VERSION} - *.png"), key=lambda p: (" - 3D - " not in p.name, p.name)):
        lab = p.stem.replace(f"Media wall v{VERSION} - ", "").replace(" (HD)", "")
        items.append((p, (lab.replace("3D - ", "") + " (3D, HD)") if lab.startswith("3D - ") else lab + " (drawn, HD)", "PNG"))
    for p in sorted(OUT.glob("*plan*.png")) + sorted(OUT.glob("Dining layouts*.png")) + sorted(OUT.glob("Storage options*.png")) + sorted(OUT.glob("Drawer layouts*.png")) + sorted(OUT.glob("Sub cover*.png")):
        items.append((p, p.stem, "PNG"))
    return items


def downloads_html(site):
    """v14.1: the PDFs and HD pictures as a list of links: straight to the files on GitHub Pages, to GitHub from the deck."""
    base = "media-wall/out/" if site else GITHUB_OUT
    lis = "".join(f'<li><a href="{base}{urllib.parse.quote(p.name)}" target="_blank" rel="noopener">{html.escape(label)}</a><small>{kind}</small></li>'
                  for p, label, kind in downloads_list())
    return f'<ul class="dl">{lis}</ul>'


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
  /* v23, client: "make the page itself a better colour background and some customisations to make it more appealing": four page looks
     (data-skin on the root, chosen in the header, kept on each device), a header band, and larger text. Card Room is the default. */
  --bg: #e4eadd; --bg-top: #d3decb; --surface: #fbfaf5; --line: #ccd5c3; --chip: #dbe3d2;
  --hero: #2f4a3c; --hero-ink: #f3f0e6; --hero-muted: #c9d6c6; --hero-chip: #ffffff1f; --hero-link: #f0c58e; --hero-note: #ffffff14;
}
:root[data-skin="oak"] { --bg: #f1ebe0; --bg-top: #e7dcc8; --surface: #fffdf8; --line: #ddd2bf; --chip: #ebe2d2; --note: #f7efe1;
  --hero: #6b4a2b; --hero-ink: #fbf5ea; --hero-muted: #e6d3bb; --hero-chip: #ffffff22; --hero-link: #ffd9a8; --hero-note: #ffffff17; }
:root[data-skin="blue"] { --bg: #e5e9f0; --bg-top: #d3dbe8; --surface: #fbfcfe; --line: #cbd3e0; --chip: #dce2ec; --note: #eef1f7;
  --hero: #2c4466; --hero-ink: #f1f4fa; --hero-muted: #c7d2e5; --hero-chip: #ffffff1f; --hero-link: #f3c58f; --hero-note: #ffffff14; }
:root[data-skin="plain"] { --bg: #eef0ea; --bg-top: #eef0ea; --surface: #ffffff; --line: #d4d9cd; --chip: #e3e7dd;
  --hero: transparent; --hero-ink: #1d241e; --hero-muted: #5b6457; --hero-chip: #e3e7dd; --hero-link: #9a6634; --hero-note: #f5efe3; }
:root.bigtext { font-size: 112.5%; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #151a16; --surface: #1d231e; --ink: #e7ebe3; --muted: #9ba596; --line: #2f3830; --oak: #d9a46c; --chip: #262d27; --note: #262219;
  --ok: #8fd3a2; --ok-bg: #1f3325; --tight: #e8c07a; --tight-bg: #3a2f1a; --check: #9cc4ec; --check-bg: #1c2b3a; --no: #f0a59c; --no-bg: #3d211e; color-scheme: dark;
  --bg-top: #1b231d; --hero: #22352b; --hero-ink: #eef1ea; --hero-muted: #aebcad; --hero-chip: #ffffff1a; --hero-link: #e8b57c; --hero-note: #ffffff12; } }
:root[data-theme="dark"] { --bg: #151a16; --surface: #1d231e; --ink: #e7ebe3; --muted: #9ba596; --line: #2f3830; --oak: #d9a46c; --chip: #262d27; --note: #262219;
  --ok: #8fd3a2; --ok-bg: #1f3325; --tight: #e8c07a; --tight-bg: #3a2f1a; --check: #9cc4ec; --check-bg: #1c2b3a; --no: #f0a59c; --no-bg: #3d211e; color-scheme: dark;
  --bg-top: #1b231d; --hero: #22352b; --hero-ink: #eef1ea; --hero-muted: #aebcad; --hero-chip: #ffffff1a; --hero-link: #e8b57c; --hero-note: #ffffff12; }
body { background: linear-gradient(180deg, var(--bg-top) 0, var(--bg) 520px) no-repeat, var(--bg); color: var(--ink); font-family: var(--body); font-size: 16px; line-height: 1.55; }
.wrap { max-width: 1120px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 28px 56px; display: grid; gap: 32px; }
header { display: grid; gap: 10px; min-width: 0; background: var(--hero); color: var(--hero-ink); border-radius: 22px;
  padding: clamp(18px, 3.2vw, 34px); position: relative; overflow: hidden; }
:root[data-skin="plain"] header { padding: 0; border-radius: 0; }
header::after { content: ""; position: absolute; inset: auto -60px -90px auto; width: 300px; height: 300px; border-radius: 50%;
  background: radial-gradient(circle, var(--hero-chip), transparent 70%); pointer-events: none; }
header .eyebrow, header .lede, header .caption { color: var(--hero-muted); }
header a:not(.btn) { color: var(--hero-link); }
header .notice { background: var(--hero-note); color: var(--hero-ink); }
header .hlinks a.btn { background: var(--hero-chip); color: var(--hero-ink); }
header .hlinks a.btn:first-child { background: var(--oak); color: var(--surface); }
:root[data-skin="plain"] header .hlinks a.btn:not(:first-child) { background: var(--chip); color: var(--ink); }
.skin { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; font-size: 13.5px; color: var(--hero-muted); position: relative; z-index: 1; }
.skin button { font: inherit; font-size: 13px; border: 1px solid #ffffff33; background: transparent; color: var(--hero-ink); border-radius: 999px; padding: 4px 10px 4px 6px; cursor: pointer; display: inline-flex; gap: 6px; align-items: center; }
.skin button[aria-pressed="true"] { background: var(--hero-chip); border-color: var(--hero-link); }
.skin button i { width: 14px; height: 14px; border-radius: 50%; display: inline-block; border: 1px solid #ffffff55; }
:root[data-skin="plain"] .skin button { border-color: var(--line); }
.skin label { display: inline-flex; gap: 6px; align-items: center; cursor: pointer; margin-left: 6px; }
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
/* v22: build steps one at a time: the head (number, title, who and how long, Done) always shows; the rest opens */
.shead { cursor: pointer; }
.sopen { font: inherit; font-size: 14px; border: 1px solid var(--line); background: var(--chip); color: var(--ink); border-radius: 999px; padding: 5px 12px; cursor: pointer; }
.sopen:focus-visible { outline: 2px solid var(--oak); outline-offset: 2px; }
.sbody { display: grid; gap: 10px; min-width: 0; }
.sbody[hidden] { display: none; }
.step:not(.open) { padding-block: 10px; }
.snext { margin: 0; }
.sall { display: flex; flex-wrap: wrap; gap: 6px 14px; align-items: center; margin: 4px 0 10px; }
@media (max-width: 560px) { .shead { grid-template-columns: 2.2rem minmax(0, 1fr); } .shead .sdone, .shead .sopen { grid-column: 2; justify-self: start; } .shead .sopen { margin-top: -4px; } }
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
.hlinks { display: flex; flex-wrap: wrap; gap: 8px; margin: 2px 0 0; }
.hlinks a.btn { text-decoration: none; }
.hlinks a.btn:first-child { background: var(--oak); color: var(--surface); }
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
@media (max-width: 860px) { .dash { grid-template-columns: repeat(3, minmax(0, 1fr)); } .d3d { grid-column: 1 / -1; aspect-ratio: 16 / 7; min-height: 0; } }
@media (max-width: 520px) { .dash { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; } .dcard { padding: 10px 12px; } .dcard strong { font-size: 1.2rem; }
  .dash .dcard:last-child { grid-column: 1 / -1; } }
.opts { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 14px; }
.opt { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; overflow: hidden; display: grid; grid-template-rows: auto 1fr; min-width: 0; }
.opt img { display: block; width: 100%; aspect-ratio: 16 / 9; object-fit: cover; background: #0d100e; }
.opt .ob { padding: 12px 14px 14px; display: grid; gap: 8px; align-content: start; }
.opt h3 { margin: 0; font-family: var(--display); font-size: 1.2rem; }
.opt ul { margin: 0; padding-left: 1.2rem; display: grid; gap: 4px; font-size: 14.5px; }
.opt li::marker { content: "+  "; color: var(--ok); font-weight: 700; }
.opt li.minus::marker { content: "\u2212  "; color: var(--tight); }
.opt .btn { justify-self: start; }
.opt.noimg { grid-template-rows: 1fr; }
.opt p { margin: 0; font-size: 14.5px; }
.gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 12px; }
.gallery figure { margin: 0; display: grid; gap: 6px; }
.gallery button { padding: 0; border: 1px solid var(--line); border-radius: 10px; overflow: hidden; cursor: zoom-in; background: #0d100e; }
.gallery img { display: block; width: 100%; aspect-ratio: 16 / 9; object-fit: cover; }
.gallery figcaption { font-size: 13.5px; color: var(--muted); }
""" + room3d_page.CSS + """

/* v24, client: "give it a better overall design and ui": one card per long read, quieter headings with an oak rule, a floating
   tab bar, tables that read as tables, a contents sidebar on wide screens, folded captions, a footer */
:root { --tab-on: var(--hero); --tab-on-ink: var(--hero-ink); --shadow: 0 1px 2px #0000000a, 0 10px 28px -18px #00000040; }
:root[data-skin="plain"] { --tab-on: var(--ink); --tab-on-ink: var(--bg); }
.wrap { max-width: 1180px; gap: 28px; }
.tabs { background: color-mix(in srgb, var(--bg) 82%, transparent); -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px); border-bottom: 0; margin-top: -8px; }
.tabs .tl { padding: 5px; margin-block: 8px; background: var(--surface); border: 1px solid var(--line); border-radius: 999px; box-shadow: var(--shadow); }
.tabs button[aria-selected="true"] { background: var(--tab-on); color: var(--tab-on-ink); }
.panel { gap: 24px; }
.panel > .doc { background: var(--surface); border: 1px solid var(--line); border-radius: 20px; padding: clamp(18px, 3.2vw, 40px); box-shadow: var(--shadow); }
.panel > .doc > h2:first-child { margin-top: 0; }
.doc h2 { font-size: 1.55rem; letter-spacing: -0.005em; }
.doc h2::before { content: ""; display: block; width: 34px; height: 3px; border-radius: 2px; background: var(--oak); margin-bottom: 12px; }
.panel > .doc h2:not(:first-child) { margin-top: 48px; padding-top: 30px; border-top: 1px solid var(--line); }
.doc h3 { font-size: 1.15rem; margin-top: 30px; }
.doc p, .doc li { line-height: 1.62; }
.doc figure { margin-bottom: 22px; }
.doc figure img, .doc figure.dia { border-radius: 14px; }
.doc .decision, .doc .why, .doc .callout { border-radius: 14px; }
.ptitle::before { content: ""; display: block; width: 28px; height: 3px; border-radius: 2px; background: var(--oak); margin-bottom: 10px; }
.qhead .ptitle::before { display: none; }
.tscroll { border-radius: 14px; box-shadow: var(--shadow); }
.tscroll th { background: var(--chip); position: sticky; top: 0; }
.tscroll tr:nth-child(even) td { background: color-mix(in srgb, var(--chip) 38%, transparent); }
.dcard, .opt, details.phase, details.zone, details.changes, .step { border-radius: 16px; box-shadow: var(--shadow); }
.opt img { transition: transform .4s ease; }
.opt:hover img { transform: scale(1.02); }
@media (prefers-reduced-motion: reduce) { .opt img { transition: none; } .opt:hover img { transform: none; } }
button.more { font: inherit; font-size: inherit; color: var(--oak); background: none; border: 0; padding: 0 1px; cursor: pointer; text-decoration: underline; text-underline-offset: 2px; }
button.more:focus-visible { outline: 2px solid var(--oak); outline-offset: 2px; }
/* the contents: a sticky sidebar on wide screens, one scrolling row of section links on narrow ones */
.toc { scrollbar-width: none; }
@media (min-width: 1100px) {
  .panel.has-toc { grid-template-columns: 200px minmax(0, 1fr); column-gap: 30px; align-items: start; }
  .panel.has-toc > .toc { grid-column: 1; grid-row: 1 / span 40; position: sticky; top: calc(78px + env(safe-area-inset-top, 0px));
    display: grid; gap: 1px; max-height: calc(100vh - 110px); overflow: auto; padding: 4px 2px 12px; }
  .panel.has-toc > :not(.toc) { grid-column: 2; }
  .toc .chip { background: none; border-radius: 8px; padding: 5px 10px; justify-content: flex-start; text-align: left; font-size: 13.5px; color: var(--muted); line-height: 1.3; }
  .toc .chip.h2 { color: var(--ink); font-weight: 700; background: none; margin-top: 10px; }
  .toc .chip.h2:first-child { margin-top: 0; }
  .toc .chip.on { background: var(--chip); color: var(--ink); box-shadow: inset 2px 0 0 var(--oak); }
}
@media (max-width: 1099px) {
  .toc { flex-wrap: nowrap; overflow-x: auto; padding-bottom: 2px; }
  .toc .chip { flex: none; }
  .toc .chip:not(.h2) { display: none; }
}
footer.foot { display: flex; flex-wrap: wrap; gap: 6px 18px; justify-content: space-between; align-items: center; color: var(--muted); font-size: 14px;
  border-top: 1px solid var(--line); padding-top: 18px; }
footer.foot a { color: var(--oak); }
</style>"""


def _drop_blocks(css, head):
    """Take every block that starts with head (and its nested braces) out of css."""
    out, i = [], 0
    while True:
        j = css.find(head, i)
        if j < 0:
            out.append(css[i:]); return "".join(out)
        out.append(css[i:j]); k, depth = css.index("{", j), 0
        for m in range(k, len(css)):
            depth += css[m] == "{"; depth -= css[m] == "}"
            if depth == 0:
                break
        i = m + 1


# v25: light only (no dark mode, no page looks); the v25 tokens and components go on the end
STYLE_V25 = re.sub(r':root\[data-(?:theme="dark"|skin="[a-z]+")\][^{]*\{[^}]*\}', "", _drop_blocks(STYLE, "@media (prefers-color-scheme: dark)")).replace("</style>", (HERE / "page.css").read_text() + "</style>")


TABS = [("overview", "Overview"), ("room", "Room in 3D"), ("views", "Drawn views"), ("ideas", "Ideas"), ("wall", "Media wall"), ("dining", "Dining table"), ("paint", "Paint & light"),
        ("network", "Network & power"), ("build", "Build steps"), ("buy", "Buy & costs"), ("questions", "Questions"), ("checks", "Checks & sources")]
TAB_GROUPS = {"overview": "See it", "wall": "The plan", "build": "Do it", "questions": "Your input"}   # v14: the tab bar in four groups
CAP3D = {"3d_room": "The whole room (v21, the 3D room's first view): from above the window side with the window wall cut away, so the media wall, the breast, the door, the stairs, the table's wall, the PC wall and the sofa are all in one picture",
         "3d_window_B_folded": "From the window, the Bright preset: the table folded under your shelf by the stairs, the breast free",
         "3d_window_B_four": "Option B from the window: the table down for four under your shelf by the stairs, set for dinner",
         "3d_wall_film": "The media wall with the Film preset: bias light on, bar 1 off, the strips low",
         "3d_wall_drawers": "Every drawer out, the Cosy preset: the LP crates under the turntable, a slim game drawer beside them",
         "3d_sofa_cosy": "From the sofa, the Cosy preset: light on the deck, the ledge and the LP crates",
         "3d_chairs": "The chair cupboard (v20) beside the folded table, doors open: four folded chairs inside, two on its floor and two on its shelf (plant stand and lamp hidden for the view)",
         "3d_chairs_shut": "The stairs wall packed away (v20): the table folded under your shelf and the oak chair cupboard shut beside it, flush with the pipe boxing",
         "3d_B_folded": "The stairs wall: your shelf with the black OBEGRÄNSAD panel, the laser (off) and the plant hanging at the end by the pipe boxing, the red lamp, the table folded under it",
         "3d_stairs_A_four": "From the stairs: the table down for four on the breast",
         "3d_dining_A_four": "Option A: down for four on the chimney breast",
         "3d_dining_B_four": "Option B: down for four under the shelf, bar 2 right over it",
         "3d_six_day": "The flip-top open for six, in daylight: three a side, your hessian curtains on their wooden pole",
         "3d_pc_day": "The side wall in daylight: one oak run sweeping out to the PC, your blue sofa, the curtains",
         "3d_plan_B": "Bird\u2019s eye, option B set for four",
         "3d_doll_A": "Dolls\u2019 house view, option A",
         "3d_window_bright": "The Bright preset: every spot head straight down, evenly spread, the strips and the lamp filling in",
         "3d_pc_lit": "The Film preset with the PC lit: its fans and the RGB strip glowing behind the glass side",
         "3d_plants_corner": "Your plant stand (98 \u00d7 29.5 \u00d7 158) in the window's west corner (layout A, recommended): two towers of five tiers and a taller plant in the open middle",
         "3d_records_breast": "Your vinyl stand (70 \u00d7 32 \u00d7 78) on the chimney breast (layout A): two face-out bays on top, LPs between the wires below, under the \u201cnow playing\u201d ledge",
         "3d_plants_breast": "Layout B: the plant stand on the breast instead (the ledge comes off, the frames go up), the vinyl stand back in the window corner",
         "3d_ideas_window": "Idea, not in the plan: glass plant shelves across the window's reveal, beside your plant stand in the west corner",
         "3d_ideas_ctable": "Idea, not in the plan: the oak C-table over the sofa's open end",
         "3d_ideas_breast": "Idea, not in the plan: the tall glass display case (v20: 85 tall, three glass shelves) on the chimney breast, oak, with collectibles, above the \u201cnow playing\u201d ledge",
         "3d_case_mixed": "The same case with a black frame and a bit of everything: 7-inch singles, a cap and figures, small plants, boxed games",
         "3d_case_singles": "The same case with a white frame, 7-inch singles face-out and a stack of tapes, in the Cosy preset",
         "3d_decor": "Decor to try (v20): sage-stripe rug, rust and ochre cushions and a throw on the sofa, white linen curtains",
         "3d_suggest": "Suggested furniture and decor, all of them on: a floor plant, side table and knit throw at the sofa's open end, a pouffe, floor cushions, a print, a clock, an arched mirror, fairy lights, candles, a lantern and more",
         "3d_seat": "Option (v23): the fold-down oak seat at the stair end, down, beside the folded table; your sofa's ottoman on the rug",
         "3d_c_folded": "Option C, the dining cabinet, packed away: one oak cabinet under your shelf, the table standing up in its bay over a drawer, eight chairs behind the doors",
         "3d_c_eight": "Option C open for eight: the table 225 long, four on the stair side, three on the window side, one at the end",
         "3d_c_chairs": "Option C's chair bay open: eight folded chairs, two across and two deep, four on the floor and four on the shelf",
         "3d_c_plan": "Bird\u2019s eye, option C open for eight",
         "3d_look": "Look to try: walnut on every new oak piece, oak floorboards, your shelf in oak and white linen curtains (option C packed away)"}
IDEA_SHOT = {"case": "3d_ideas_breast", "glass": "3d_ideas_window", "ctable": "3d_ideas_ctable", "cushions": "3d_decor"}
IDEA_VIEW = {"case": "breast", "glass": "windowwall", "ctable": "pc", "cushions": "door"}
IDEA_OPTS = {"cushions": {"decor": {"cushions": "rust"}}}   # v20: the cushions are a Decor choice, not an idea toggle


def ideas_panel():
    """v17: the ideas for later (ideas.py), a card each, with a way to see the first three in the 3D room."""
    import ideas as I
    cards = []
    for k, title, size, cost, why, where, in3d in I.IDEAS:
        im = (f'<img data-art="{IDEA_SHOT[k]}" alt="{html.escape(CAP3D[IDEA_SHOT[k]])}" loading="lazy">' if in3d else "")
        opts = json.dumps(dict({"site": "B", "view": IDEA_VIEW.get(k, "window")}, **IDEA_OPTS.get(k, {"ideas": {k: True}})))
        b = f"<button type='button' class='btn' data-r3d='{opts}'>See it in the 3D room</button>" if in3d else ""
        cards.append(f'<article class="opt{"" if in3d else " noimg"}">{im}<div class="ob"><span class="label">{html.escape(size)} · about £{cost[0]}–{cost[1]}</span>'
                     f'<h3>{html.escape(title)}</h3><p>{html.escape(why)}</p><p class="caption">{html.escape(where)}</p>{b}</div></article>')
    lo, hi = I.low_high()
    return (f'<div class="qhead"><h2 class="ptitle">Ideas for later</h2><span class="caption">Suggestions only: not in the plan, the buy list or the costs</span></div>'
            f'<p class="caption">Small enough for this room: nothing new on the floor bigger than a side table. The first three are in the 3D room, under “Ideas (not in the plan)”, all off until you turn them on; the cushions are under “Decor”. All of them together would be about £{lo}–{hi}.</p>'
            f'<div class="opts">{"".join(cards)}</div>' + suggest_block() + decor_block())


def suggest_block():
    """v21, client: "i also want expansion of the suggested furniture and decor making sure i can choose to have it or not"."""
    import ideas as I
    allon = {k: True for k, *_ in I.SUGGEST}
    rows = "".join(
        f'<article class="opt noimg"><div class="ob"><span class="label">{html.escape(size)} · about £{c[0]}–{c[1]}</span><h3>{html.escape(t)}</h3>'
        f'<p>{html.escape(why)}</p><p class="caption">{html.escape(where)}</p>'
        f"<button type='button' class='btn' data-r3d='{json.dumps({'site': 'B', 'view': 'door', 'sugg': {k: True}})}'>See it in the 3D room</button></div></article>"
        for k, t, size, c, why, where in I.SUGGEST)
    lo, hi = I.suggest_low_high()
    return (f'<div class="qhead"><h2 class="ptitle">Suggested furniture and decor</h2><span class="caption">Each one on or off, in the 3D room: none are in the plan or the costs</span></div>'
            f'<figure><button type="button" class="g3d" data-full="3d_suggest"><img data-art="3d_suggest" alt="{html.escape(CAP3D["3d_suggest"])}" loading="lazy"></button>'
            f'<figcaption>{html.escape(CAP3D["3d_suggest"])}</figcaption></figure>'
            f'<p class="caption">Under “Suggested furniture and decor” in the 3D room each piece has its own button, all off to start; the floor pieces move in Edit room. '
            f'All {len(I.SUGGEST)} together would be about £{lo}–{hi}. Edit room\'s Add list also has a rattan armchair, an oak blanket ladder, an oak bench and an arc floor lamp (v21).</p>'
            f'<div class="opts">{rows}</div>'
            f"<button type='button' class='btn' data-r3d='{json.dumps({'site': 'B', 'view': 'door', 'sugg': allon})}'>See them all in the 3D room</button>")


def decor_block():
    """v20, client: "give more decor variation and options": what the 3D room's Decor buttons do, with three looks."""
    import room3d_page as RP
    rows = "".join(f'<li><b>{html.escape(lab)}:</b> {html.escape(", ".join(n for _, n in opts))}</li>' for _, lab, opts in RP.DECOR)
    figs = "".join(f'<figure><button type="button" class="g3d" data-full="{k}"><img data-art="{k}" alt="{html.escape(CAP3D[k])}" loading="lazy"></button>'
                   f'<figcaption>{html.escape(CAP3D[k])}</figcaption></figure>' for k in ("3d_case_mixed", "3d_case_singles", "3d_decor"))
    b = ("<button type='button' class='btn' data-r3d='" + json.dumps({"site": "B", "view": "door", "decor": {"rug": "stripes", "cushions": "rust", "curtains": "linen"}})
         + "'>Try decor in the 3D room</button>")
    return (f'<div class="qhead"><h2 class="ptitle">Decor to try</h2><span class="caption">In the 3D room, under “Decor”: your choices are kept on this device</span></div>'
            f'<ul>{rows}</ul><p class="caption">Picking what goes in the glass case turns the case on (it hangs with the table by the stairs). '
            f'In Edit room, “Add” now has a floor vase with grasses, a knitted pouffe, a seagrass basket for throws, an oak floor mirror and a lantern, as well as the armchair, bookcase and the rest.</p>'
            f'<div class="gallery">{figs}</div>{b}')


def chairs_card():
    """v20, client: "is it not possible to build the chair storage into the table setup. i want it to be a fully pack away setup": the chair
    cupboard built in beside the table, flush with the pipe boxing; the open hooks stay as the cheap way; chairs five and six."""
    g = G
    CB = g.CHAIR_STORE["cupboard"]
    w = CB["z"][0] - CB["z"][1]
    sh = json.dumps({'site': 'B', 'dining': 'folded', 'chairs': 'cupboard', 'view': 'dining', 'scene': 'bright'})
    op = json.dumps({'site': 'B', 'dining': 'folded', 'chairs': 'open', 'view': 'chairs', 'scene': 'bright'})
    return f"""<div class="opts">
  <article class="opt"><img data-art="3d_chairs_shut" alt="{html.escape(CAP3D['3d_chairs_shut'])}" loading="lazy">
    <div class="ob"><span class="label">1 · the plan (v20) · about £120–240</span><h3>A chair cupboard, built in beside the table</h3>
    <ul><li>Oak, {w:.0f} wide × {CB['d']:.0f} deep × {CB['h']:.0f} tall, in the gap at the table's window end, flush with the pipe boxing and under your shelf.</li>
    <li>Four folded chairs inside: two on its floor, two on its shelf, one behind the other. Two doors on push latches.</li>
    <li>The table and its chairs pack away together: the wall reads as one built-in piece.</li>
    <li class="minus">Six fit if it's built {CB['d6']:.0f} deep: it then stands {CB['d6'] - CB['d']:.0f} cm proud of the boxing.</li></ul>
    <button type="button" class="btn" data-r3d='{sh}'>See it shut in 3D</button> <button type="button" class="btn" data-r3d='{op}'>See it open</button></div></article>
  <article class="opt"><img data-art="3d_chairs" alt="{html.escape(CAP3D['3d_chairs'])}" loading="lazy">
    <div class="ob"><span class="label">Using it</span><h3>Doors open, four chairs inside</h3>
    <ul><li>Its doors are hinged on the table's side and open right back (165°), so the chairs come straight out to the table.</li>
    <li>Open the table first, then take the chairs out; fold the table last.</li>
    <li class="minus">The open hooks (about £8–15) still work if you'd rather not build it.</li></ul></div></article>
  <article class="opt noimg"><div class="ob"><span class="label">More ways (v23) · options</span><h3>Behind the folded top, or a fold-down seat</h3>
    <ul><li>Four more chairs can hang behind the folded top on a backboard {g.BEHIND_TOP['gap']:.0f} cm deeper: with the cupboard, all six (or eight) pack away.</li>
    <li>A fold-down oak seat in the {g.CHAIR_STORE['stair_gap'][0] - g.CHAIR_STORE['stair_gap'][1]:.0f} cm gap at the stair end: a fifth place that's always there.</li>
    <li class="minus">Behind the top, the table stands {g.BEHIND_TOP['gap']:.0f} cm further into the room. Under the stairs is brick: chairs five and six otherwise go in the garage.</li></ul>
    <button type="button" class="btn" data-r3d='{json.dumps({"site": "B", "dining": "folded", "view": "dining", "seat": "down"})}'>See the seat in 3D</button></div></article>
</div>"""


def options_card():
    """v14: the table's two places side by side, with a way into the 3D room for each (v26: and option C, the dining cabinet)."""
    g = G
    south, north = g.STAIRS_WALL_Z[0] - g.TABLE_B_Z[0], g.TABLE_B_Z[1] - g.WINDOW_Z
    def btn(opts, lab):
        return f"<button type=\"button\" class=\"btn\" data-r3d='{json.dumps(opts)}'>{lab}</button>"
    a = btn({"site": "A", "dining": "four", "view": "dining", "scene": "bright"}, "See A in 3D")
    b = btn({"site": "B", "dining": "four", "view": "dining", "scene": "bright"}, "See B in 3D")
    c = btn({"site": "C", "dining": "eight", "view": "dining", "scene": "bright"}, "See C in 3D")   # v26
    return f"""<div class="opts">
  <article class="opt"><img data-art="3d_dining_B_four" alt="Option B in 3D: the table down for four under the shelf by the stairs" loading="lazy">
    <div class="ob"><span class="label">Option B · up to seven · the default (v16)</span><h3>Under your shelf, by the stairs</h3>
    <ul><li>Opens into the room: three a side and one at the end.</li><li>Out of the door's swing, under the pendant point; frees the breast for the “now playing” ledge.</li>
    <li class="minus">Side chairs tight: {south - g.CHAIR[1] + 8:.0f} and {north - g.CHAIR[1] + 8:.0f} cm behind them; the lamp moves while it's open.</li><li class="minus">Wall's build unknown: knock first.</li></ul>{b}</div></article>
  <article class="opt"><img data-art="3d_dining_A_four" alt="Option A in 3D: the table down for four on the chimney breast" loading="lazy">
    <div class="ob"><span class="label">Option A · up to six · the alternative</span><h3>On the chimney breast</h3>
    <ul><li>The flip-top opens towards the window: four with room, six elbows-in.</li><li>Solid breast: plugs and screws, no surprises.</li>
    <li class="minus">No seat at its end (the sofa); one chair in the door's swing.</li></ul>{a}</div></article>
  <article class="opt"><img data-art="3d_c_eight" alt="{html.escape(CAP3D['3d_c_eight'])}" loading="lazy">
    <div class="ob"><span class="label">Option C · up to eight · a second option</span><h3>The dining cabinet</h3>
    <ul><li>One oak cabinet under the shelf: the table stands up in one bay, all {g.OPTC['chairs']} chairs fold into the other.</li>
    <li>Opens to {g.OPTC['len']:g} × {g.OPTC['top'][0]:g}: eight at a squeeze, six in comfort.</li>
    <li class="minus">Costs more than the flip-top and the chair cupboard; the ottoman moves aside while it's out.</li></ul>{c}</div></article>
</div>"""


def gallery3d():
    figs = "".join(f'<figure><button type="button" class="g3d" data-full="{k}"><img data-art="{k}" alt="{html.escape(CAP3D[k])}" loading="lazy"></button>'
                   f'<figcaption>{html.escape(CAP3D[k])}</figcaption></figure>' for k, *_ in SHOTS3D if not k.startswith(("3d_ideas_", "3d_case_", "3d_decor", "3d_suggest", "3d_seat")))
    return f'<div class="gallery">{figs}</div>'

TABNAME = dict(TABS)
SEC_TAB = {"1": "overview", "2": "overview", "3": "wall", "4": "wall", "5": "dining", "6": "wall", "7": "wall", "8": "paint",
           "9": "network", "10": "build", "11": "buy", "12": "checks"}


LINKNAME = {"overview": "plan", "room": "3D room", "views": "Drawn views chapter", "ideas": "Ideas", "wall": "Media wall chapter", "dining": "Dining wall chapter",
            "paint": "Paint & light chapter", "network": "Network & power chapter", "build": "Build steps", "buy": "Buy list", "questions": "Ask list", "checks": "Fit proof"}


def _tablink(tab):
    return f'<a href="#{tab}" data-go="{tab}">{LINKNAME[tab]}</a>'


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
    """v24: the page without round markers in its text (tidy.strip_versions) and with long captions folded (tidy.shorten_captions)."""
    import tidy
    return tidy.shorten_captions(tidy.strip_versions(_page(site)))


def _ph(rows, *names):
    """Low and high for buy-list phases, by name."""
    lo = sum(r["lo"] for r in rows if r["phase"] in names); hi = sum(r["hi"] for r in rows if r["phase"] in names)
    return f"£{money(lo, hi)}"


# v25: the Plan sheet's chapters: (key, title, icon, hue, one line for the tile)
CHAPTERS = [("c-room", "The room", "home", 50, "Sizes, the door, the stairs, the window"),
            ("wall", "The media wall", "tv", 300, "Heights, the TV, the bays"),
            ("records", "Records & turntable", "album", 345, "LPs, crates, the vinyl stand"),
            ("side", "The side wall", "desktop_windows", 235, "One oak run out to the PC"),
            ("joinery", "Oak joinery", "carpenter", 70, "Joints, the cutting list"),
            ("dining", "The dining wall", "table_restaurant", 50, "The flip-top and the chairs"),
            ("paint", "Paint & light", "palette", 165, "Card Room Green, three presets"),
            ("network", "Network & power", "router", 25, "Decos, switches, the electrics"),
            ("views", "Drawn views", "draw", 125, "Every view in four greens"),
            ("fit", "Fit proof", "straighten", 95, "Every item against its size"),
            ("downloads", "Downloads", "download", 165, "The PDFs and every HD picture")]
PAGE_PART = {"Prep": 95, "Network": 235, "Power & cables": 25, "Paint": 165, "Media wall": 300, "Dining table": 70, "Lighting": 125, "AV": 345}


def chapter_facts(rows, fc, nfit):
    """v25: four to six key facts for each chapter, from geometry, fit, the buy list and ideas, so they follow the next round."""
    import scenes as SC
    import render as RR
    g = G
    chips = lambda *xs: '<ul class="facts">' + "".join(f"<li>{x}</li>" for x in xs) + "</ul>"
    heights = [(g.CEIL, "Ceiling"), (g.HIGH_TOP, "High shelf"), (g.LEDGE_TOP, "Record ledges, the PC shelf"), (g.FOLDED_TOP, "The table, folded"),
               (g.RZ_SHELF_TOP, "Series X shelf"), (116.5, "TV centre"), (g.NOW_LEDGE["top"], "“Now playing” ledge"), (g.WORKTOP, "Oak worktop"), (g.PLINTH, "Plinth")]
    flist = '<ul class="flist">' + "".join(f"<li><b>{v:g}</b><span>{html.escape(t)}</span></li>" for v, t in sorted(heights, key=lambda x: -x[0])) + "</ul>"
    paints = "".join(f'<li><span style="display:inline-block;width:14px;height:14px;border-radius:50%;background:{h};vertical-align:-2px;margin-right:6px"></span>{html.escape(n.replace("Farrow & Ball ", "").replace("Little Greene ", ""))}{" (chosen)" if k == "card_room" else ""}</li>'
                     for k, (h, n) in RR.PAINTS.items())
    return {
        "c-room": chips(f"<b>{g.CEIL:g}</b> ceiling", f"<b>{g.ALC_W:g} × {g.ALC_D:g}</b> alcove", "Door hinged on the breast side, opens in",
                        "A straight stair flight, rising towards the door", f"<b>{g.WINDOW_REVEAL + g.SILL['nose']:g}</b> window ledge ({g.WINDOW_REVEAL:g} reveal + {g.SILL['nose']:g} nose)", "Soft grey carpet"),
        "wall": flist + chips('LG C6 55" on its stand', "Artisan oak in Card Room Green", "Steps 6–10", _ph(rows, "4 Base unit", "5 Oak joinery")),
        "records": chips(f"<b>~{g.ALL_LPS}</b> LPs", f"<b>{g.WALL_LPS}</b> face-out in the wall", f"<b>{g.STAND_LPS}</b> in the vinyl stand (70 × 32 × 78)",
                         "Two snug LP crates (33 cm trough) in bay 3", f"Game drawers: about <b>{48 + g.SLIM_GAMES}</b> games", f"Series X shelf at {g.RZ_SHELF_TOP:g}; the lid opens to {g.LID_CLEAR_TO:g}"),
        "side": chips("One oak run sweeping out to the PC", f"PC shelf at <b>{g.LEDGE_TOP:g}</b>", "Leads through a brush grommet into conduit in the wall", "A warm LED strip underneath", "Step 10"),
        "joinery": chips("The cutting list (copy it for the timber merchant)", "Housings, mortises and pegs: the joints drawing", "Worktop: step 7", "Uprights: step 9",
                         "Oak joinery " + _ph(rows, "5 Oak joinery")),
        "dining": chips(f"Flip-top gate-leg, <b>{g.TABLE[0]:g} × {g.TABLE[1]:g}</b> opening to {g.TABLE[0]:g} × {2 * g.TABLE[1]:g}", "Four with room, six elbows-in, seven by the stairs",
                        "Häfele brackets, 500 kg a pair", f"Folds under the shelf, its top at {g.FOLDED_TOP:g}",
                        f"Chair cupboard: four ({g.CHAIR_STORE['cupboard']['d']:g} deep) or six ({g.CHAIR_STORE['cupboard']['d6']:g} deep)", "Dining wall " + _ph(rows, "6 Dining wall"),
                        f"<b>Option C</b>: one oak cabinet, a {g.OPTC['len']:g} × {g.OPTC['top'][0]:g} table and {g.OPTC['chairs']} chairs inside; up to eight"),   # v26
        "paint": f'<ul class="facts">{paints}</ul>' + chips(*[f"<b>{n}</b> {html.escape(SC.COLOURS[k])}" for k, n, *_ in SC.SCENES])
                 + chips("Smart E14 bulbs in both bars, no dimmers", "Paint " + _ph(rows, "3 Paint"), "Lighting " + _ph(rows, "7 Lighting")),
        "network": chips("Virgin Hub 5 in modem mode", "Three Deco X1500s", "Two TL-SG108 switches", "Cat6 runs on step 3",
                         "The electrics are your own job: like for like, not notifiable under Part P, with the stop-and-call list", "The 10-gang feeds the PC"),
        "views": chips("5 views × 4 greens", "A numbered key", "Measurements over any view", "Full size, to pan and zoom"),
        "fit": chips(f"<b>{nfit}</b> checks", f"<b>{fc[fit.PASS]}</b> fit", f"<b>{fc[fit.TIGHT]}</b> tight", f"<b>{fc[fit.CHECK]}</b> to check on site", f"<b>{fc[fit.NO]}</b> don't fit"),
        "downloads": chips(f"The plan, v{VERSION} (PDF)", f"The build guide, v{VERSION} (PDF)", "Every HD picture, 3D and drawn", "On GitHub Pages and the shared plan page"),
    }


def preset_cards():
    """v25: the three lighting presets as cards (levels, colour, notes) and the two rules, for the Paint & light chapter."""
    import scenes as SC
    icons = {"bright": "light_mode", "cosy": "local_fire_department", "film": "movie"}
    cards = "".join(
        f'<article class="opt noimg" style="background:oklch(0.94 0.07 95) !important"><div class="ob"><span class="label"><span class="ms" aria-hidden="true">{icons[k]}</span> Preset</span><h3>{html.escape(n)}</h3>'
        f'<p>{html.escape(d)}</p><p class="caption">{html.escape(SC.COLOURS[k])}</p>'
        f'<ul class="facts" style="--h:95">' + "".join(f"<li>{html.escape(lab.split(',')[0].replace(' and the side shelf', ''))}: {SC.level_word(lv[lk])}</li>" for lk, lab, _c in SC.LAYERS) + "</ul>"
        f'<ul>' + "".join(f"<li>{html.escape(x)}</li>" for x in notes) + '</ul>'
        f"<button type='button' class='btn' data-r3d='{json.dumps({'scene': k, 'view': 'room'})}'>Try it in the room</button></div></article>"
        for k, n, d, lv, notes in SC.SCENES)
    rules = '<div class="notice"><b>Two rules</b><ul>' + "".join(f"<li>{html.escape(r)}</li>" for r in SC.RULES) + "</ul></div>"
    return f'<div class="opts">{cards}</div>{rules}'


def ring(key, hue, label, go):
    k = "steps" if key == "build" else key
    return (f'<a class="ring" id="d-{k}-bar" href="#{go}" data-go="{go}" style="--h:{hue}"><svg viewBox="0 0 80 80" aria-hidden="true"><circle class="tr" cx="40" cy="40" r="34"/>'
            f'<circle class="vl" cx="40" cy="40" r="34"/></svg><b id="d-{k}">0</b><span>{label}</span></a>')


def _page(site=False):
    """v25 (Demma Home Improvements, option 1c "Room as map"): the 3D room is the home screen; a rail (a bottom bar on phones) opens
    the Plan, Build, Buy, Ideas and Ask sheets over it; the Tools button holds every 3D control. Every v24 panel id, data-* hook and
    saved key is kept: the panels live inside the sheets now."""
    import diagrams as D
    import questions as QM
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
    facts = chapter_facts(rows, fc, nfit)
    qs = [{"id": i, "q": q, "why": w, "how": h, "photo": ph} for i, q, w, h, ph in QUESTIONS]
    QH = [235, 300, 50, 165, 345, 95, 70, 125, 25]
    def qrows(i):
        out = []
        for lab, choices in QM.OPTS.get(i, []):
            bs = "".join((f'<button type="button" class="qc" data-photo="1"><span class="ms" aria-hidden="true">photo_camera</span>{html.escape(c)}</button>' if c.startswith("Add a photo")
                          else f'<button type="button" class="qc" data-v="{html.escape(c)}" aria-pressed="false">{html.escape(c)}</button>') for c in choices)
            out.append(f'<div class="qrow" data-label="{html.escape(lab or "")}">' + (f'<span class="label">{html.escape(lab)}</span>' if lab else "")
                       + f'<div class="qchips" role="group" aria-label="{html.escape(lab or "Your answer")}">{bs}</div></div>')
        return "".join(out)
    q_items = "\n".join(
        f'<li class="q" id="q-{i}" data-q="{i}" style="--h:{QH[n % len(QH)]}"><h3><span class="n">{n:02d}</span><span>{html.escape(q)}</span></h3>'
        f'{qrows(i)}<p class="qans" aria-live="polite"></p>'
        f'<details class="qwhy"><summary>Why we ask</summary><p>{html.escape(w)}</p><p><b>How:</b> {html.escape(h)}</p></details>'
        # the answer box and Save stay (hidden): the quick taps write through them, so answers/<id> and the drafts on this device are as before
        f'<div class="qin" hidden><label class="label" for="a-{i}">Your answer</label><textarea id="a-{i}" rows="2" placeholder="Type here"></textarea>'
        f'<button class="btn primary save" type="button" data-q="{i}">Save</button></div>'
        f'<div class="row"><label class="upl btn" hidden>Add a photo<input type="file" accept="image/*" multiple data-q="{i}" id="f-{i}"></label>'
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
            f'<label class="sdone" for="sd-{s["n"]}"><input type="checkbox" id="sd-{s["n"]}"> Done</label>'
            f'<button type="button" class="sopen" aria-expanded="true" aria-controls="sb-{s["n"]}">Close</button></div>'
            f'<div class="sbody" id="sb-{s["n"]}">'
            + (f'<p class="sbuy"><span class="label">Buy first</span>{buy}</p>' if buy else "")
            + need_html(s)
            + ("<details class=\"sdraw\" open><summary>" + ("Drawing" if len(s.get("draw", [])) == 1 else "Drawings") + " for this step</summary>"
               + "".join(f'<figure class="dia">{getattr(D, DIAGRAMS[d])()}</figure>' for d in s["draw"]) + "</details>" if s.get("draw") else "")
            + f'<details class="readmore sfullwrap" style="--h:50"><summary>Read the full step <span class="ms" aria-hidden="true">expand_more</span></summary><div class="sfull">{full_html(s)}</div></details>'
            f'<p class="scheck"><b>Check before moving on:</b> {s["check"]}</p>'
            f'<p class="ssee">Also see: {see}</p>'
            f'<p class="snext"><button type="button" class="btn" data-next="{s["n"]}">Next step →</button></p></div></li>')
    data = {"img": imgs, "q": qs, "track": [{k: r[k] for k in ("id", "phase", "lo", "hi", "done", "kind")} for r in rows],
            "phases": [{k: p[k] for k in ("name", "idx", "lo", "hi")} for p in phases], "top": 200 * -(-max(p["hi"] for p in phases) // 200),
            "steps": len(steps()), "tabs": [t for t, _ in TABS]}
    used = [k for k in PARTS if any(k in st["part"] for st in steps())]
    part_buttons = "".join(f'<button type="button" data-part="{html.escape(k)}" aria-pressed="false"><span class="dot" style="background:{PARTS[k]}"></span>{html.escape(k)}</button>' for k in used)
    segbar = "".join(f'<i data-s="{s["n"]}" style="--pc:{PARTS[s["part"][0]]}" title="{s["n"]}. {html.escape(s["title"])}"></i>' for s in steps())
    base = "media-wall/out/" if site else GITHUB_OUT
    TILE_ID = {"views": "tb-views", "wall": "tb-wall", "dining": "tb-dining", "paint": "tb-paint", "network": "tb-network", "fit": "tb-checks"}
    tiles = "".join(f'<button type="button" class="ctile"{(" id=" + chr(34) + TILE_ID[k] + chr(34)) if k in TILE_ID else ""} data-go="{k}" style="--h:{h}"><i class="ms" aria-hidden="true">{ic}</i><span>{html.escape(t)}<br><small>{html.escape(sub)}</small></span></button>'
                    for k, t, ic, h, sub in CHAPTERS)
    def chapter(k, inner):
        _k, t, ic, h, _s = next(c for c in CHAPTERS if c[0] == k)
        return (f'<section class="chapter" id="ch-{k}" data-ch="{k}" style="--h:{h}" hidden><button type="button" class="chback" data-go="overview"><span class="ms" aria-hidden="true">arrow_back</span>All chapters</button>'
                f'<div class="chhead"><i class="ms" aria-hidden="true">{ic}</i><h2>{html.escape(t)}</h2></div>{facts[k]}{inner}</section>')
    more = lambda body, lab="Read the full chapter": f'<details class="readmore"><summary>{lab} <span class="ms" aria-hidden="true">expand_more</span></summary>{body}</details>'
    nav = [("plan", "Plan", "map", 300), ("build", "Build", "construction", 50), ("buy", "Buy", "shopping_bag", 165), ("ideas", "Ideas", "lightbulb", 95), ("questions", "Ask", "forum", 235)]
    badge = f'<span class="badge ask-badge">{len(QUESTIONS)}</span>'
    rail = (f'<nav class="rail" aria-label="Sections"><button type="button" id="tb-room" data-nav="room" aria-current="true" style="--h:25"><i class="ms" aria-hidden="true">view_in_ar</i>Room</button>'
            + "".join(f'<button type="button" id="tb-{"overview" if k == "plan" else k}" data-nav="{k}" aria-current="false" style="--h:{h}"><i class="ms" aria-hidden="true">{ic}</i>{n}{badge if k == "questions" else ""}</button>' for k, n, ic, h in nav) + '</nav>')
    bbar = (f'<nav class="bbar" aria-label="Sections"><button type="button" class="toolsb" data-tools-toggle aria-expanded="false" aria-controls="r3d-panel"><i class="ms" aria-hidden="true">tune</i>Tools</button>'
            + "".join(f'<button type="button" data-nav="{k}" aria-current="false" style="--h:{h}"><i class="ms" aria-hidden="true">{ic}</i>{n}{badge if k == "questions" else ""}</button>' for k, n, ic, h in nav) + '</nav>')
    def sheet(k, title, ic, h, body):
        return (f'<div class="sheet" id="sh-{k}" role="dialog" aria-modal="true" aria-labelledby="sh-{k}-h" aria-hidden="true" style="--h:{h}">'
                f'<div class="shd"><span class="grab" aria-hidden="true"></span><h2 id="sh-{k}-h"><i class="ms" aria-hidden="true">{ic}</i><span>{title}</span></h2>'
                f'<button type="button" class="close" data-close aria-label="Close {title}"><span class="ms" aria-hidden="true">close</span></button></div>'
                f'<div class="sbd">{body}</div></div>')
    sugg_chips = ('<div class="seg" role="group" aria-label="Suggestions in the room">'
                  + "".join(f'<button type="button" data-sproxy="{k}" aria-pressed="false">{html.escape(room3d_page.SUGG_SHORT[k])}</button>' for k, *_ in __import__("ideas").SUGGEST)
                  + '<button type="button" class="chip" data-sproxyall="on">All on</button><button type="button" class="chip" data-sproxyall="off">All off</button></div>')
    notice = (f'<p class="notice">Ticks and amounts on this page stay on this device. To share them, use <a href="{DECK_URL}" target="_blank" rel="noopener">the plan page on Claude</a>.</p>' if site
              else f'<p class="caption">Also on <a href="{PAGES}" target="_blank" rel="noopener">GitHub Pages</a>.</p>')

    plan_home = f"""<div class="plan-home" id="plan-home"><div class="panel" id="overview">
      <div><p class="hello" id="hello">Evening, Emma &amp; Dave</p><p>The artisan oak media wall in Card Room Green, the fold-down table, the network and power: about £{money(lo_tot, hi_tot)} in all.</p></div>
      <div class="rings">{ring("build", 50, "build steps", "build")}{ring("buy", 165, "bought", "buy")}{ring("q", 235, "answered", "questions")}</div>
      <p class="caption" id="d-paid">£0 paid so far</p>
      <div class="upnext"><span class="n" id="d-nextn">1</span><div><span class="label">Up next</span><h3 id="d-next">Measure and count</h3></div>
        <button type="button" class="done-btn" id="d-nextdone" data-s="1"><span class="ms" aria-hidden="true">check_circle</span>Done</button>
        <p><span id="d-nextmeta"></span> · <a href="#build" data-go="build" data-step="1" id="d-nextgo">Open it</a></p></div>
      <div class="sec-h"><h2>Chapters</h2></div>
      <div class="tilegrid">{tiles}</div>
      <div class="sec-h"><h2>Two places for the table</h2><a class="btn" href="#dining" data-go="dining" data-find="Two places">Compare them in full</a></div>
      {options_card()}
      <details class="fold"><summary>The plan on a page</summary><div class="doc">{s1}</div></details>
      <!--keep--><details class="fold changes"><summary>What changed in v{VERSION}</summary><div class="doc"><p>{decision}</p></div></details><!--/keep-->
    </div></div>"""
    chapters = "".join([
        chapter("c-room", more(f'<div class="doc">{sec["2"]}</div>')),
        chapter("wall", more(f'<div class="panel" id="wall"><nav class="toc" aria-label="In this chapter"></nav><div class="doc">{sec["3"]}</div></div>')),
        chapter("records", more(f'<div class="doc">{sec["4"]}</div>')),
        chapter("side", more(f'<div class="doc">{sec["6"]}</div>')),
        chapter("joinery", '<p><a class="btn" href="#build" data-go="build" data-find="Cutting list">Open the cutting list (copy it as text)</a></p>' + more(f'<div class="doc">{sec["7"]}</div>')),
        chapter("dining", f'<div class="panel" id="dining"><nav class="toc" aria-label="In this chapter"></nav><div class="block"><h2 class="ptitle">Two places for the table</h2>{options_card()}</div>'
                          f'<div class="block"><h2 class="ptitle">Keeping the chairs: a cupboard built in beside the table</h2><p class="caption">The table doesn\'t change. Folded chairs are about {G.CHAIR_FOLDED[0]:g} × {G.CHAIR_FOLDED[1]:g} × {G.CHAIR_FOLDED[2]:g}; the full fit check is in the Fit proof.</p>{chairs_card()}</div>'
                          + more(f'<div class="doc">{sec["5"]}</div>') + '</div>'),
        chapter("paint", f'<div class="panel" id="paint">{preset_cards()}' + more(f'<div class="doc">{sec["8"]}</div>') + '</div>'),
        chapter("network", more(f'<div class="panel" id="network"><nav class="toc" aria-label="In this chapter"></nav><div class="doc">{sec["9"]}</div></div>')),
        chapter("views", f"""<div class="panel" id="views"><div class="viewer">
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
        <div class="seg" role="group" aria-labelledby="l-zoom"><button id="k-full" type="button">View full size</button></div></div>
    </div>
    <p class="caption" id="cap"></p>
  </div>
  <div class="band">
    <section><h2>Heights, from the floor</h2>
      <ul class="heights">
        <li><b>{G.CEIL:g}</b><span>Ceiling, as measured</span></li>
        <li><b>{G.HIGH_TOP:g}</b><span>High shelf: books, a box, a print, the “now playing” single, Deco B</span></li>
        <li><b>{G.LEDGE_TOP:g}</b><span>Record ledges over the TV and round the corner; the PC shelf on the side wall</span></li>
        <li><b>{G.FOLDED_TOP:g}</b><span>Top of the dining table, folded up</span></li>
        <li><b>{G.RZ_SHELF_TOP:g}</b><span>Series X shelf, over the turntable (its lid has to {G.LID_CLEAR_TO:g})</span></li>
        <li><b>116.5</b><span>TV centre, LG C6 55in on its stand</span></li>
        <li><b>{G.WORKTOP:g}</b><span>Oak worktop, and the dining table when it's down</span></li>
        <li><b>{G.PLINTH:g}</b><span>Plinth under the two BESTÅ bays, with a hidden drawer</span></li>
      </ul></section>
    <section><h2>In the wall</h2>
      <div class="counts">
        <div><strong>~{LPS}</strong><span>LPs: {G.WALL_LPS} face-out in the wall, {G.STAND_LPS} in your vinyl stand</span></div>
        <div><strong>LPs</strong><span>only, in the trays: room to flip</span></div>
        <div><strong>4–7</strong><span>at the dining table; two spare chairs hang by it</span></div>
      </div>
      <p class="caption">The numbered key works on the main view. Measurements are rough, in pale yellow, for checking against the real room; the drawings in the chapters are the exact ones.</p></section>
  </div></div>"""),
        chapter("fit", f"""<div class="panel" id="checks">
    <p class="caption">Every item in the wall against its published size: {fc[fit.PASS]} of {nfit} fit outright, {fc[fit.TIGHT]} are tight and {fc[fit.CHECK]} need a check on site. Source numbers refer to the Sources list below.</p>
    <div class="qhead">{fit_head}<button class="btn" id="fit-only" type="button" aria-pressed="false">Show only tight and to-check</button></div>
    <div id="fit-zones">{fit_body}</div>
    <div class="doc">{sec["12"]}<!--keep--><h2>Options we set aside</h2>{sec["appendix"]}<details><summary>Earlier rounds (v13 to v14)</summary>{sec["earlier"]}</details><!--/keep--></div></div>"""),
        chapter("downloads", f'<div class="block"><p class="caption">The full plan and the build guide as PDFs for printing, and every HD picture, 3D and drawn.</p>'
                             f'<p><a class="btn primary" href="{base}Home_Network_Plan_v{VERSION}.pdf" target="_blank" rel="noopener">The plan (PDF)</a> '
                             f'<a class="btn" href="{base}Build_Guide_v{VERSION}.pdf" target="_blank" rel="noopener">Build guide (PDF)</a></p>{downloads_html(site)}{notice}'
                             f'<p class="caption">Demma Home Improvements · Portsmouth Close · living room · v{VERSION}</p></div>'),
    ])
    build_body = f"""<section class="panel" id="build">
    <div class="qhead"><div class="meter"><span class="bar"><i id="s-bar"></i></span><span id="s-count">0 of {len(steps())} steps done</span></div></div>
    <div class="segbar" id="segbar" style="--n:{len(steps())}" aria-hidden="true">{segbar}</div>
    <p class="caption" id="s-note">Tick each step when it's done; it saves for both of you. "Buy first" opens that part of the buy list.</p>
    <div class="group pfilter"><span class="label" id="l-part">Show one part</span>
      <div class="seg" role="group" aria-labelledby="l-part" id="part-filter"><button type="button" data-part="" aria-pressed="true">All parts</button>{part_buttons}</div>
      <p class="caption" id="pf-note" aria-live="polite"></p></div>
    <div class="row sall"><label class="sdone" for="s-all"><input type="checkbox" id="s-all"> Show all steps open</label><span class="caption">One step at a time otherwise: it opens on the first one not done.</span></div>
    <ol class="steps-list" id="steps-ol">{"".join(step_cards)}</ol>
    <div class="block" id="cuts">
      <div class="qhead"><h2 class="ptitle">Cutting list for the timber merchant</h2><div class="row"><button class="btn" id="copy-cuts" type="button">Copy as text</button><span class="caption" id="cuts-st" aria-live="polite"></span></div></div>
      <textarea id="cuts-box" class="caption" rows="8" hidden readonly aria-label="The cutting list as text">{html.escape(cuts_text())}</textarea>
      <div class="doc">{deck_section(cuts_html())}</div>
    </div>
    <details class="fold"><summary>Before you start: how the guide works, time, tools, techniques and pitfalls</summary><div class="doc">{GUIDE_RULES}{GUIDE_TIME}{guide_tools()}{GUIDE_TECHNIQUES}{GUIDE_PITFALLS}</div></details>
  </section>"""
    buy_body = f"""<section class="panel" id="buy">
    <div class="tiles">
      <div><strong>£{money(lo_tot, hi_tot)}</strong><span>the whole plan; no electrician on top</span></div>
      <div><strong id="t-left">£{money(lo_tot, hi_tot)}</strong><span>still to buy: the items not ticked yet</span></div>
      <div><strong id="t-paid">£0</strong><span>paid so far, from the amounts you enter</span></div>
      <div><strong id="t-done">0 of {len(rows)}</strong><span>items and jobs ticked off</span></div>
    </div>
    <div class="qhead"><h3 class="ptitle">The buy list, in build order</h3>
      <div class="seg" role="group" aria-label="Show">
        <button type="button" data-filter="all" aria-pressed="true">Everything</button>
        <button type="button" data-filter="left" aria-pressed="false">Still to buy</button>
        <button type="button" data-filter="jobs" aria-pressed="false">Jobs only</button>
      </div></div>
    <p class="caption" id="t-note">Each phase says which build step it's needed for. Tick each item off and write in what you paid; it saves for both of you.</p>
    <div id="tracker">{"".join(ph_html)}</div>
    <details class="fold"><summary>Cost by phase, low to high</summary>{cost_chart(phases)}</details>
    <p class="notice">Already owned: Virgin Hub 5, three Deco X1500s, two TL-SG105S switches (both become spares), LG OLED C6 55" and its stand, a 10-gang, the Hisense AX5100G 5.1 soundbar, the Series X fan stand, the turntable, the L-sofa and all the consoles. Estimates are approximate UK prices.</p>
  </section>"""
    ideas_body = f"""<section class="panel" id="ideas">
    <div class="block"><h2 class="ptitle">Suggestions in the room</h2><p class="caption">Each one switches the room too: close this to see them.</p>{sugg_chips}</div>
    {ideas_panel()}
  </section>"""
    ask_body = f"""<section class="panel" id="questions">
    <p class="caption">{len(QUESTIONS)} things only you can tell us, the ones that change the drawings first. Tap an answer; a photo is often quicker than words.</p>
    <div class="meter"><span id="q-count">0 of {len(QUESTIONS)} answered</span></div>
    <div class="qprog" aria-hidden="true"><i id="q-bar"></i></div>
    <p class="notice" id="q-local" hidden>Answers can't be saved for both of you from this view: they're kept on this device. When you're done, use Copy all answers and paste them into a message.</p>
    <p class="notice" id="q-ro" hidden>You can read the answers here but not change them. Ask Emma to give you Contributor access in the Share menu.</p>
    <ul class="qs" id="qs-list">
{q_items}
    </ul>
    <div class="row"><button class="btn" id="copy-all" type="button">Copy all answers</button><span class="caption" id="copy-st" aria-live="polite"></span></div>
    <textarea id="copy-box" class="caption" rows="6" hidden readonly aria-label="All answers as text"></textarea>
  </section>"""
    page = f"""<title>Demma Home Improvements</title>
{room3d_page.IMPORTMAP}
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700&family=Fredoka:wght@500;600&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,500,1,0&display=block">
{STYLE_V25}
<button type="button" class="skip" data-tools-toggle>Open the room's controls</button>
<div class="brand"><span class="mark" aria-hidden="true"><i style="background:var(--peach)"></i><i style="background:var(--mint)"></i><i style="background:var(--lilac)"></i><i style="background:var(--butter)"></i></span>
  <span><b>Demma</b><small>Home Improvements</small></span></div>
{rail}
<main id="room" aria-label="Your room in 3D">{room3d_page.section(gallery3d())}</main>
{sheet("plan", "Your plan", "map", 300, plan_home + chapters)}
{sheet("build", "Build", "construction", 50, build_body)}
{sheet("buy", "Buy", "shopping_bag", 165, buy_body)}
{sheet("ideas", "Ideas", "lightbulb", 95, ideas_body)}
{sheet("questions", "Ask", "forum", 235, ask_body)}
{bbar}
<div class="lightbox" id="lightbox" hidden role="dialog" aria-modal="true" aria-label="The picture at full size">
  <div class="lbbar"><span class="caption" id="lb-cap">Full size: drag or scroll to look round. Pinch to zoom on a phone.</span><button class="btn" id="lb-close" type="button">Close</button></div>
  <div class="lbscroll" id="lb-scroll"><div class="lbwrap"><img id="lb-img" alt=""><img id="lb-dims" alt="" hidden></div></div>
</div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>
const DATA = {json.dumps(data)};
const SITE = {json.dumps(site)};
""" + (HERE / "page.js").read_text() + """
</script>
<script>""" + STEP_JS + """</script>
<script>""" + __import__("tidy").MORE_JS + """</script>
<script>""" + (HERE / "page_router.js").read_text() + """</script>
"""
    # the build parts in the page's pastels (the PDF keeps its own colours)
    for name, hue in PAGE_PART.items():
        page = page.replace(f"--pc:{PARTS[name]}", f"--pc:oklch(0.78 0.12 {hue})").replace(f"background:{PARTS[name]}\"></span>{html.escape(name)}", f"background:oklch(0.78 0.12 {hue})\"></span>{html.escape(name)}")
    return uniq_svgs(page)


# v23: the page looks (the header's "Page look" buttons) and larger text, kept on each device
SKINS = [("card", "Card Room", "#2f4a3c"), ("oak", "Oak & linen", "#6b4a2b"), ("blue", "Sofa blue", "#2c4466"), ("plain", "Plain", "#eef0ea")]
SKIN_BTNS = "".join(f'<button type="button" data-skin="{k}" aria-pressed="false"><i style="background:{c}"></i>{n}</button>' for k, n, c in SKINS)
SKIN_JS = r"""(() => {
  const d = document.documentElement, bs = [...document.querySelectorAll(".skin [data-skin]")], big = document.getElementById("big-text");
  const sync = () => bs.forEach(b => b.setAttribute("aria-pressed", String(b.dataset.skin === (d.dataset.skin || "card"))));
  bs.forEach(b => b.addEventListener("click", () => { d.dataset.skin = b.dataset.skin; try { localStorage.setItem("mw23-skin", b.dataset.skin); } catch (e) {} sync(); }));
  if (big) { big.checked = d.classList.contains("bigtext");
    big.addEventListener("change", () => { d.classList.toggle("bigtext", big.checked); try { localStorage.setItem("mw23-big", big.checked ? "1" : "0"); } catch (e) {} }); }
  sync();
})();"""


# v22: the build steps one at a time (the plan's review: 67 phone screens long). The head always shows; one step opens; "Next step"
# opens the next shown step; links to a step (the overview's "Next", the buy list's "before step n") open it; "Show all steps open" reads straight through.
STEP_JS = r"""(() => {
  const lis = $$(".steps-list > li.step"), all = document.getElementById("s-all"); if (!lis.length) return;
  let cur = store.get("mw22-step", null), showAll = !!store.get("mw22-steps-all", false);
  const set = n => { cur = n == null ? null : String(n); store.set("mw22-step", cur);
    lis.forEach(li => { const on = showAll || li.dataset.s === cur, b = $(".sopen", li);
      li.classList.toggle("open", on); $(".sbody", li).hidden = !on; b.setAttribute("aria-expanded", String(on)); b.textContent = on ? "Close" : "Open"; b.hidden = showAll; }); };
  const firstTodo = () => (lis.find(li => !li.hidden && !li.classList.contains("done")) || lis[0]).dataset.s;
  const go = n => { set(n); const li = document.getElementById("step-" + n); if (li) jumpTo(li); };
  lis.forEach(li => {
    $(".sopen", li).addEventListener("click", e => { e.stopPropagation(); set(li.classList.contains("open") ? null : li.dataset.s); });
    $(".shead", li).addEventListener("click", e => { if (e.target.closest("label, input, button, a")) return; if (!li.classList.contains("open")) go(li.dataset.s); });
    $("[data-next]", li).addEventListener("click", () => { const i = lis.indexOf(li), nx = lis.slice(i + 1).find(x => !x.hidden); if (nx) go(nx.dataset.s); });
  });
  document.addEventListener("click", e => { const a = e.target.closest("[data-step]"); if (a && !showAll) set(a.dataset.step); }, true);
  all.checked = showAll;
  all.addEventListener("change", () => { showAll = all.checked; store.set("mw22-steps-all", showAll); set(cur); });
  set(cur && lis.some(li => li.dataset.s === cur) ? cur : null);
  if (!cur && !showAll) setTimeout(() => { if (!cur) set(firstTodo()); }, 1500);   // after the saved ticks have loaded
  $$(".step:last-child [data-next]").forEach(b => b.closest(".snext").hidden = true);
})();"""


def site():
    """The same page for GitHub Pages at the repo root: a full document, paths into media-wall/, plain download links."""
    body = page(site=True).replace("body { background", "body { margin: 0; background", 1)
    head, rest = body.split("</style>", 1)
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 16 16%22%3E%3Crect width=%2216%22 height=%2216%22 rx=%223%22 fill=%22%239a6634%22/%3E%3C/svg%3E">\n'
            + head + "</style>\n</head>\n<body>" + rest + "</body>\n</html>\n")


def publish_files():
    """{published path: source} for the Artifact publish: the viewer images and the downloads."""
    files = {f"art/{p.name}": str(p) for p in sorted((HERE / "art").glob("*.webp"))}
    if not DOWNLOADS_ON_GITHUB:
        files.update({published_name(p): str(p) for p, _, kind in downloads_list() if kind != "PDF"})
    return files


DECK_ASSETS = HERE / "deck_assets.json"   # v22: art/ files uploaded to the deck's asset store: {name: {"sha": ..., "url": "/_blob/..."}}


def art_sha(p):
    import hashlib
    return hashlib.sha256(p.read_bytes()).hexdigest()


def deck_assets_todo():
    """v22: the art/ files the deck's asset store doesn't hold yet (new, or changed since they were uploaded)."""
    have = json.loads(DECK_ASSETS.read_text()) if DECK_ASSETS.exists() else {}
    return [p for p in sorted((HERE / "art").glob("*.webp")) if have.get(p.name, {}).get("sha") != art_sha(p)]


def inline_images(html_):
    """The copy published to the shared deck (media_wall_viewer_inline.html, gitignored). v22: each picture already in the deck's
    asset store (deck_assets.json, matched by its sha256) is linked by its /_blob/ url; any other is carried as a data URI, so the
    page always works. With everything uploaded the page is about 2 MB instead of 10.8. (Uploads through `files` were refused in
    v13 with false "cpio archive" sniffs; the asset store takes them.)"""
    import base64
    have = json.loads(DECK_ASSETS.read_text()) if DECK_ASSETS.exists() else {}
    for p in sorted((HERE / "art").glob("*.webp")):
        a = have.get(p.name)
        uri = a["url"] if a and a.get("sha") == art_sha(p) else "data:image/webp;base64," + base64.b64encode(p.read_bytes()).decode()
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
    todo = deck_assets_todo()
    print("viewer ok", len(publish_files()), "files;", len(todo), "pictures not yet in the deck's asset store" + (" (inlined)" if todo else ""))
    (HERE / "deck_assets_todo.txt").write_text("".join(str(p) + "\n" for p in todo))
