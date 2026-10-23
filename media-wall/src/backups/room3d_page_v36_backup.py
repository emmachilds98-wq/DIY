"""v14: the 3D room's piece of the plan page: its controls, its data and its script (room3d.js), plus a standalone copy for
the headless stills (shot3d.py). Three.js comes from jsDelivr, pinned."""
import html, json, pathlib
import scenes
import ideas
import render as R
import geometry as G

HERE = pathlib.Path(__file__).parent
THREE = "https://cdn.jsdelivr.net/npm/three@0.160.0/"
IMPORTMAP = ('<script type="importmap">' + json.dumps({"imports": {"three": THREE + "build/three.module.js",
                                                                   "three/addons/": THREE + "examples/jsm/"}}) + "</script>")

VIEWS = [("room", "The whole room"), ("window", "From the window"), ("wall", "The media wall"), ("sofa", "From the sofa"), ("door", "From the door"),
         ("stairs", "From the stairs"), ("dining", "The dining cabinet"), ("chairs", "Where the chairs live"), ("sit", "Sitting at the table"),
         ("beside", "Beside the cabinet"), ("breast", "The chimney breast"),
         ("windowwall", "The window wall"), ("pc", "The PC side wall"), ("plan", "Bird’s eye"), ("doll", "Dolls’ house")]   # v21: the whole room first; v31: sitting down, beside the cabinet

CSS = """
/* v25 (Demma, option 1c): the room is the home screen, full screen; one Tools pill holds every control; numbered stickers sit on
   the room. Tokens come from build_viewer's STYLE (with fallbacks here, for the standalone page the stills use). */
.r3d { --cream: #fbf6ec; --ink: #2b2638; --mut: #645d73; --soft: #f1ebde; --shade: 0 14px 34px -12px #000a;
  --spring: cubic-bezier(.3,1.6,.5,1); font-family: Figtree, system-ui, sans-serif; }
.r3d-stage { position: fixed; inset: 0; height: 100vh; height: 100dvh; background: #0c0a10; overflow: hidden; z-index: 0; }
.r3d-stage canvas { display: block; width: 100%; height: 100%; touch-action: none; cursor: grab; outline: none; }
.r3d-stage canvas:active { cursor: grabbing; }
.r3d-msg { position: absolute; inset: 0; display: grid; place-items: center; padding: 24px; text-align: center; color: #f4efe6; font-size: 15px; text-shadow: 0 1px 4px #000; }
.r3d-msg a { color: oklch(0.9 0.08 70); }
.r3d-msg[hidden] { display: none; }
.r3d-poster { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: .75; pointer-events: none; }
.r3d.ready .r3d-poster, .r3d-poster:not([src]) { display: none; }
.sr-only { position: absolute !important; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
.ms { font-family: "Material Symbols Rounded"; font-weight: normal; font-style: normal; font-size: 22px; line-height: 1; display: inline-block;
  font-variation-settings: "FILL" 1, "wght" 500; -webkit-font-smoothing: antialiased; text-transform: none; letter-spacing: 0; white-space: nowrap; direction: ltr; }
/* the stickers on the room and the popover under the one you tap */
.r3d-stickers { position: absolute; inset: 0; pointer-events: none; }
.stk { position: absolute; left: 0; top: 0; transform: translate(-50%, -50%) rotate(var(--tilt, -2deg)); pointer-events: auto; display: inline-flex; align-items: center; gap: 8px;
  border: 0; border-radius: 999px; padding: 6px 14px 6px 6px; background: oklch(0.92 0.06 var(--h)); color: var(--ink); font: 600 14px Fredoka, system-ui, sans-serif;
  box-shadow: var(--shade); cursor: pointer; transition: opacity .25s, transform .3s var(--spring); min-height: 44px; }
.stk b { display: grid; place-items: center; width: 30px; height: 30px; border-radius: 50%; background: oklch(0.8 0.11 var(--h)); font-weight: 600; }
.stk:hover, .stk[aria-expanded=true] { transform: translate(-50%, -50%) rotate(0deg) scale(1.06); }
.stk.behind { opacity: .35; }
.stk[hidden] { display: none; }
.r3d.editing .r3d-stickers, .r3d.nogl .r3d-stickers { display: none; }
.r3d-pop { position: absolute; width: 290px; background: var(--cream); color: var(--ink); border-radius: 24px; padding: 16px 16px 14px; box-shadow: var(--shade); z-index: 6; }
.r3d-pop[hidden] { display: none; }
.r3d-pop::before { content: ""; position: absolute; top: -7px; left: var(--ax, 50%); width: 16px; height: 16px; background: var(--cream); transform: translateX(-50%) rotate(45deg); border-radius: 3px; }
.r3d-pop h3 { margin: 0 34px 8px 0; font: 600 19px Fredoka, system-ui, sans-serif; }
.r3d-pop .facts { display: flex; flex-wrap: wrap; gap: 6px; margin: 0 0 12px; padding: 0; list-style: none; }
.r3d-pop .facts li { background: oklch(0.92 0.06 var(--h)); border-radius: 999px; padding: 5px 11px; font-size: 13px; font-weight: 600; }
.r3d-pop .acts { display: flex; gap: 8px; }
.r3d-pop .acts button { flex: 1; min-height: 44px; border: 0; border-radius: 999px; font: 600 14px Fredoka, system-ui, sans-serif; cursor: pointer; background: var(--soft); color: var(--ink); }
.r3d-pop .acts button.go { background: oklch(0.8 0.11 var(--h)); }
.r3d-pop .x { position: absolute; top: 10px; right: 10px; width: 36px; height: 36px; border: 0; border-radius: 50%; background: var(--soft); color: var(--ink); cursor: pointer; display: grid; place-items: center; }
/* v30: the card for an item you tap in the room: what it is, how it is now, and its controls */
.r3d-act { width: 300px; --h: 50; }
.r3d-act .st { margin: -2px 34px 12px 0; font-size: 13.5px; color: var(--mut); }
.r3d-act .acts { flex-wrap: wrap; }
.r3d-act .acts button { flex: 1 1 calc(50% - 4px); padding: 0 12px; }
.r3d-act .acts button[aria-pressed=true] { background: var(--ink); color: var(--cream); }
.r3d-act.above::before { top: auto; bottom: -7px; }
.r3d.editing .r3d-act { display: none; }
/* the tools and their panel. v32, client: "make tools always appear in 3D view": the six buttons are always on the room, in a pill;
   tapping one opens its panel, tapping it again closes it */
.r3d-dock { position: fixed; left: 50%; bottom: 18px; transform: translateX(-50%); display: flex; gap: 10px; align-items: center; z-index: 30;
  padding: 6px 12px 4px; border-radius: 999px; background: color-mix(in oklab, var(--cream) 92%, transparent); box-shadow: var(--shade); }
.r3d-toolsbtn { display: inline-flex; align-items: center; gap: 8px; min-height: 52px; padding: 0 22px 0 16px; border: 0; border-radius: 999px; background: var(--cream); color: var(--ink);
  font: 600 17px Fredoka, system-ui, sans-serif; box-shadow: var(--shade); cursor: pointer; transition: transform .3s var(--spring); }
.r3d-toolsbtn:hover { transform: scale(1.05); }
.r3d-bubbles { display: flex; gap: 8px; }
.r3d-toolsbtn { display: none; }
.r3d-bub { display: grid; justify-items: center; gap: 2px; width: 58px; padding: 0; border: 0; background: none; color: var(--ink); font: 600 11.5px Figtree, system-ui, sans-serif; cursor: pointer; }
.r3d-bub i { display: grid; place-items: center; width: 46px; height: 46px; border-radius: 50%; background: oklch(0.92 0.06 var(--h)); color: var(--ink); transition: transform .3s var(--spring), background .2s; font-style: normal; }
.r3d-bub:hover i { transform: translateY(-3px) scale(1.06); }
.r3d-bub[aria-selected=true] i, .r3d-bub[aria-pressed=true] i { background: oklch(0.8 0.11 var(--h)); }
.r3d-panel { position: fixed; left: 50%; bottom: 96px; transform: translateX(-50%); width: min(430px, calc(100vw - 24px)); max-height: min(560px, calc(100dvh - 140px));
  display: flex; flex-direction: column; overflow: hidden; background: var(--cream); color: var(--ink); border-radius: 30px; box-shadow: var(--shade); z-index: 29; }
.r3d-panel[hidden] { display: none; }
/* v26: the title and the foot stay put; only the middle scrolls (and it starts at the top on every tab) */
.r3d-pscroll { flex: 1 1 auto; min-height: 0; overflow: auto; overscroll-behavior: contain; padding: 0 18px 8px; scrollbar-width: thin; }
.r3d-panel h2 { position: sticky; top: 0; z-index: 2; margin: 0 -18px 2px; padding: 16px 60px 10px 18px; background: var(--cream); font: 600 20px Fredoka, system-ui, sans-serif; }
/* v26: the labels switch, top right of the room (left of the panel when it's docked on a laptop) */
.r3d-lbl { position: fixed; top: 16px; right: 16px; z-index: 31; display: inline-flex; align-items: center; gap: 6px; min-height: 44px; padding: 0 16px 0 12px; border: 0; border-radius: 999px;
  background: var(--cream); color: var(--ink); font: 600 14px Fredoka, system-ui, sans-serif; box-shadow: var(--shade); cursor: pointer; transition: transform .3s var(--spring), right .3s; }
.r3d-lbl:hover { transform: scale(1.05); }
.r3d-lbl .ms { font-size: 20px; }
.r3d.nogl .r3d-lbl, .r3d.editing .r3d-lbl { display: none; }
@media (min-width: 900px) { .r3d.tools-open .r3d-lbl { right: calc(min(420px, 38vw) + 32px); } }
@media (max-width: 899px) { .r3d-lbl { top: 12px; right: 12px; min-height: 44px; }
  .stk { font-size: 12.5px; gap: 6px; padding: 4px 11px 4px 4px; min-height: 40px; white-space: nowrap; } .stk b { width: 28px; height: 28px; flex: none; } }
.r3d-px { position: absolute; top: 10px; right: 10px; z-index: 3; width: 40px; height: 40px; border: 0; border-radius: 50%; background: var(--soft); color: var(--ink); cursor: pointer; display: grid; place-items: center; }
.r3d-px:hover { background: #e9dfcc; }
.r3d-panel .r3d-gal { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 6px; }
.r3d-panel .r3d-gal figure { gap: 0; }
.r3d-panel .r3d-gal button { border: 0; border-radius: 14px; }
.r3d-panel .r3d-gal figcaption { display: none; }
.r3d-dpanel[hidden] { display: none; }
.r3d-dpanel { display: grid; gap: 14px; }
.r3d-ui .grp { display: grid; gap: 6px; min-width: 0; }
.r3d-ui .label { font: 600 13px Figtree, system-ui, sans-serif; color: var(--mut); }
.r3d-ui .seg { display: flex; flex-wrap: wrap; gap: 6px; }
.r3d-ui .seg button, .r3d-ui .chip, .r3d-ui .btn, .r3d-foot button { min-height: 40px; border: 0; border-radius: 999px; padding: 8px 14px; background: var(--soft); color: var(--ink);
  font: 500 14px Figtree, system-ui, sans-serif; cursor: pointer; transition: transform .25s var(--spring), background .2s; }
.r3d-ui .seg button:hover, .r3d-ui .chip:hover { transform: scale(1.04); }
.r3d-ui .seg button[aria-pressed=true], .r3d-ui .chip[aria-pressed=true] { background: var(--ink); color: var(--cream); }
.r3d-ui .btn.primary { background: oklch(0.8 0.11 235); color: var(--ink); font-weight: 700; }
.r3d-views { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
.r3d-views .chip { background: oklch(0.92 0.06 235); text-align: left; }
.r3d-views .chip[aria-pressed=true] { background: oklch(0.8 0.11 235); color: var(--ink); font-weight: 700; }
.r3d-hint2, .r3d-ui .caption { font-size: 13px; color: var(--mut); }
.r3d-gal { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }
.r3d-gal figure { margin: 0; }
.r3d-gal button { padding: 0; border: 0; border-radius: 14px; overflow: hidden; cursor: zoom-in; background: #0c0a10; display: block; width: 100%; }
.r3d-gal img { display: block; width: 100%; aspect-ratio: 16 / 9; object-fit: cover; }
.r3d-gal figcaption { display: none; }
/* Lights: three big tiles, the time-of-day switch, the table rule, the sliders folded */
.r3d-tiles { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.r3d-tiles button { display: grid; gap: 4px; justify-items: start; text-align: left; min-height: 96px; padding: 12px; border: 0; border-radius: 22px; background: oklch(0.94 0.07 95); color: var(--ink);
  cursor: pointer; transition: transform .3s var(--spring); font: 500 12.5px Figtree, system-ui, sans-serif; }
.r3d-tiles button .ms { font-size: 26px; }
.r3d-tiles button b { font: 600 17px Fredoka, system-ui, sans-serif; }
.r3d-tiles button[aria-pressed=true] { background: oklch(0.8 0.11 95); box-shadow: inset 0 0 0 2px var(--ink); }
.r3d-tiles button.adjusted b::after { content: " · adjusted"; font: 500 12px Figtree, system-ui, sans-serif; color: var(--mut); }
.r3d-tiles button:hover { transform: translateY(-2px); }
.r3d-boost { margin: 0; padding: 8px 12px; border-radius: 16px; background: oklch(0.92 0.06 50); font-size: 13.5px; }
.r3d-boost[hidden] { display: none; }
details.r3d-more > summary { cursor: pointer; font-weight: 600; font-size: 14px; padding: 6px 0; list-style: none; }
details.r3d-more > summary::before { content: "+ "; }
details.r3d-more[open] > summary::before { content: "– "; }
.r3d-lvs { display: grid; gap: 10px; }
.r3d-lv { display: grid; grid-template-columns: minmax(0, 1fr) auto; grid-template-areas: "lab out" "range range" "cols cols"; gap: 2px 10px; align-items: center; min-width: 0; }
.r3d-lv label { grid-area: lab; font-size: 13.5px; }
.r3d-lv input[type=range] { grid-area: range; width: 100%; accent-color: oklch(0.7 0.13 95); }
.r3d-lv output { grid-area: out; font-variant-numeric: tabular-nums; font-size: 13px; color: var(--mut); }
.r3d-lv .r3d-cols { grid-area: cols; display: flex; gap: 6px; align-items: center; flex-wrap: wrap; }
.r3d-lv .r3d-cols:empty { display: none; }
.r3d-ui input[type=color] { width: 40px; height: 32px; padding: 0; border: 0; border-radius: 10px; background: none; cursor: pointer; }
.r3d-master label { font-weight: 700; }
/* Look: the paints as round swatches */
.r3d-swatches { display: flex; flex-wrap: wrap; gap: 10px; }
.r3d-swatches button, .r3d-swatches label { display: grid; justify-items: center; gap: 4px; width: 64px; border: 0; background: none; padding: 0; cursor: pointer; font: 500 12px Figtree, system-ui, sans-serif; color: var(--ink); text-align: center; }
.r3d-swatches i { width: 46px; height: 46px; border-radius: 50%; background: var(--c); box-shadow: inset 0 0 0 3px #fff8; transition: transform .3s var(--spring); }
.r3d-swatches button[aria-pressed=true] i { box-shadow: 0 0 0 3px var(--cream), 0 0 0 5px var(--ink); }
.r3d-swatches label i { position: relative; overflow: hidden; background: conic-gradient(oklch(0.8 0.11 25), oklch(0.8 0.11 95), oklch(0.8 0.11 165), oklch(0.8 0.11 235), oklch(0.8 0.11 300), oklch(0.8 0.11 25)); }
.r3d-swatches label input { position: absolute; inset: 0; opacity: 0; cursor: pointer; width: 100%; height: 100%; }
.r3d-decrow { display: grid; gap: 4px; }
.r3d-anycol { display: inline-flex; align-items: center; gap: 8px; }
.r3d-anycol input { width: 28px; height: 24px; }
.r3d-decrow > span { font-size: 13px; color: var(--mut); font-weight: 600; }
.r3d-picklist { margin: 0; font-size: 14px; }
.r3d-cost { font-size: 13px; color: var(--mut); font-variant-numeric: tabular-nums; }
.r3d-foot { flex: none; display: flex; gap: 8px; justify-content: flex-end; margin: 0 18px; padding: 10px 0 14px; border-top: 2px dashed #e5dccb; flex-wrap: wrap; align-items: center; }
.r3d-foot .r3d-litst { margin-right: auto; font-size: 13px; color: var(--mut); }
.r3d.nogl .r3d-dock, .r3d.nogl .r3d-panel { display: none; }
/* Edit room: the bar, the add list and the selection panel over the canvas, as cream pills */
.r3d-edit { position: absolute; top: 84px; left: 50%; transform: translateX(-50%); width: min(760px, calc(100% - 24px)); display: grid; gap: 8px; justify-items: center; pointer-events: none; z-index: 5; }
.r3d-edit > * { pointer-events: auto; }
.r3d-edit button, .r3d-edit .chip { min-height: 40px; border: 0; border-radius: 999px; padding: 8px 14px; background: var(--soft); color: var(--ink); font: 500 14px Figtree, system-ui, sans-serif; cursor: pointer; }
.r3d-edit button[aria-pressed=true] { background: var(--ink); color: var(--cream); }
.r3d-edit button.primary { background: var(--ink); color: var(--cream); font-weight: 600; }
.r3d-edit button:disabled { opacity: .5; cursor: default; }
.r3d-editbar, .r3d-sel, .r3d-addlist { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; justify-content: center; background: var(--cream); color: var(--ink); padding: 8px; border-radius: 26px; box-shadow: var(--shade); max-width: 100%; }
.r3d-editbar[hidden], .r3d-sel[hidden], .r3d-addlist[hidden], .r3d-sel [hidden], .r3d-share[hidden] { display: none; }
.r3d-hint { color: var(--mut); font-size: 12.5px; line-height: 1.3; max-width: 34em; }
.r3d-sel b { font: 600 16px Fredoka, system-ui, sans-serif; margin: 0 4px 0 8px; }
.r3d-sel label { font-size: 13px; display: inline-flex; gap: 6px; align-items: center; }
.r3d-sel .dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; vertical-align: -1px; }
.r3d-size { font-size: 12.5px; color: var(--mut); font-variant-numeric: tabular-nums; }
.r3d.editing canvas { cursor: pointer; }
@media (min-width: 900px) {
  .r3d-panel { left: auto; right: 16px; top: 16px; bottom: 104px; transform: none; width: min(420px, 38vw); max-height: none; }
}
@media (max-width: 899px) {
  .r3d-dock { left: 8px; right: 8px; transform: none; bottom: max(8px, env(safe-area-inset-bottom)); justify-content: center; padding: 6px 4px 4px; border-radius: 28px; }
  .r3d-bubbles { gap: 2px; width: 100%; justify-content: space-between; }
  .r3d-bub { width: auto; flex: 1; min-width: 0; }
  .r3d-bub i { width: 42px; height: 42px; }
  .r3d-panel { left: 12px; right: 12px; transform: none; width: auto; bottom: calc(max(8px, env(safe-area-inset-bottom)) + 78px); max-height: calc(50dvh - 20px); border-radius: 26px; }
  .r3d-edit { top: 74px; }
  .r3d-hint { display: none; }
  .r3d-addlist, .r3d-sel { flex-wrap: nowrap; overflow-x: auto; scrollbar-width: none; justify-content: flex-start; } .r3d-addlist > *, .r3d-sel > * { flex: none; }
  .r3d-pop { left: 12px !important; right: 12px; top: auto !important; bottom: calc(max(8px, env(safe-area-inset-bottom)) + 82px); width: auto; }
  .r3d-pop::before { display: none; }
  body.sheet-open .r3d-stickers, body.tools-open .r3d-stickers { display: none; }
}
/* v33, the phone home ("On a phone the room is small and buried"): numbered pins, the places in a strip, the set-ups as chips, Menu in the dock */
.r3d-phone, .r3d-menub { display: none !important; }
@media (max-width: 599px) {
  .stk { padding: 4px; gap: 0; min-height: 44px; min-width: 44px; justify-content: center; } .stk b { width: 34px; height: 34px; font-size: 15px; } .stk .t { display: none; }
  .r3d-lbl { padding: 0; width: 44px; justify-content: center; } .r3d-lbl .t { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
  .r3d-phone { display: grid !important; position: fixed; left: 0; right: 0; bottom: calc(max(8px, env(safe-area-inset-bottom)) + 76px); z-index: 5; gap: 6px; pointer-events: none; }
  .r3d-moms, .r3d-places { display: flex; gap: 6px; overflow-x: auto; scrollbar-width: none; padding: 2px 10px; pointer-events: auto; }
  .r3d-moms::-webkit-scrollbar, .r3d-places::-webkit-scrollbar { display: none; }
  .r3d-moms button, .r3d-places button { flex: none; display: inline-flex; align-items: center; gap: 6px; min-height: 40px; padding: 0 13px 0 8px; border: 0; border-radius: 999px;
    background: var(--cream); color: var(--ink); font: 600 13px Fredoka, system-ui, sans-serif; box-shadow: var(--shade); cursor: pointer; }
  .r3d-moms button { background: rgba(43, 38, 56, .82); color: var(--cream); padding: 0 13px 0 10px; } .r3d-moms .ms { font-size: 17px; }
  .r3d-places b { display: grid; place-items: center; width: 26px; height: 26px; border-radius: 50%; background: oklch(0.8 0.11 var(--h)); font-weight: 600; }
  .r3d-places button[aria-pressed=true] { background: oklch(0.92 0.06 var(--h)); box-shadow: 0 0 0 2px var(--ink); }
  .r3d-menub:not([hidden]) { display: grid !important; }
  .r3d-pop { bottom: calc(max(8px, env(safe-area-inset-bottom)) + 76px) !important; z-index: 7; }
  body:not(.sheet-open) .rail:not(.open) { display: none; }
  body:not(.sheet-open) .rail.open { top: auto; bottom: calc(max(8px, env(safe-area-inset-bottom)) + 80px); left: 8px; }
  body:not(.sheet-open) .rail.open .rail-tog { display: none; }
  body:not(.sheet-open) .rail.open .rail-list { border-top: 0; padding-top: 0; }
  .r3d.tools-open .r3d-phone, body.sheet-open .r3d-phone, .r3d.touring .r3d-phone, .r3d.editing .r3d-phone, .r3d.nogl .r3d-phone, .r3d.popped .r3d-phone, .r3d:has(.r3d-act:not([hidden])) .r3d-phone { display: none !important; }
}
/* v28: the tour's card, the link's toast, the versions */
.r3d-tour { position: fixed; left: 50%; bottom: 104px; transform: translateX(-50%); width: min(520px, calc(100vw - 24px)); z-index: 32; background: var(--cream); color: var(--ink);
  border-radius: 26px; padding: 14px 18px 16px; box-shadow: var(--shade); display: grid; gap: 6px; }
.r3d-tour[hidden] { display: none; }
.r3d-tourn { font: 600 12.5px Figtree, system-ui, sans-serif; color: var(--mut); }
.r3d-tour h3 { margin: 0; font: 600 20px Fredoka, system-ui, sans-serif; }
.r3d-tour p { margin: 0; font-size: 14.5px; line-height: 1.4; }
.r3d-tour .acts { display: flex; gap: 6px; align-items: center; margin-top: 4px; }
.r3d-tour .acts button { min-width: 44px; min-height: 44px; border: 0; border-radius: 999px; background: var(--soft); color: var(--ink); cursor: pointer; display: grid; place-items: center; font: 600 14px Fredoka, system-ui, sans-serif; }
.r3d-tour .acts button.end { margin-left: auto; padding: 0 16px; background: oklch(0.8 0.11 235); }
.r3d-tourbar { display: block; height: 5px; border-radius: 999px; background: var(--soft); overflow: hidden; }
.r3d-tourbar b { display: block; height: 100%; width: 0; background: oklch(0.8 0.11 235); }
.r3d.touring .r3d-dock, .r3d.touring .r3d-lbl { visibility: hidden; }
.r3d-toast { position: fixed; left: 50%; top: 18px; transform: translateX(-50%); z-index: 40; background: var(--ink); color: var(--cream); border-radius: 999px; padding: 10px 18px;
  font: 600 14px Fredoka, system-ui, sans-serif; box-shadow: var(--shade); max-width: calc(100vw - 24px); }
.r3d-toast[hidden] { display: none; }
.r3d-sub { margin: 6px 0 -4px; font: 600 16px Fredoka, system-ui, sans-serif; color: var(--ink); }
/* v36: Extras' option rows: a row per need, its mode tag, a line between rows */
.r3d-optrow { padding: 8px 0 6px; border-top: 1px solid var(--line, rgba(0,0,0,.08)); }
.r3d-optrow:first-of-type { border-top: 0; }
.r3d-optmode { margin-left: 6px; padding: 1px 8px; border-radius: 999px; font: 500 11.5px/1.6 system-ui, sans-serif; letter-spacing: .02em;
  background: var(--chip, rgba(0,0,0,.06)); color: var(--muted, #6b6560); vertical-align: 2px; }
.r3d-opthow { margin: 2px 0 6px; }
.r3d-moments button .ms, .r3d-ui .chip .ms { font-size: 18px; vertical-align: -4px; }
/* v31: the camera: its height, and the move buttons on the room (hold one to keep moving) */
.r3d-eyerow { display: grid; grid-template-columns: auto 1fr 5.5em; gap: 10px; align-items: center; font-size: 14px; }
.r3d-eyerow input { width: 100%; accent-color: oklch(0.55 0.12 235); }
.r3d-eyerow output { font-variant-numeric: tabular-nums; color: var(--mut); text-align: right; }
.r3d-pad { position: fixed; left: 16px; bottom: 22px; z-index: 30; display: grid; grid-template-columns: repeat(3, 44px) 44px; gap: 6px; padding: 8px;
  border-radius: 22px; background: color-mix(in oklab, var(--cream) 88%, transparent); box-shadow: var(--shade); touch-action: none; user-select: none; }
.r3d-pad[hidden] { display: none; }
.r3d-pad button { width: 44px; height: 44px; border: 0; border-radius: 14px; background: var(--soft); color: var(--ink); cursor: pointer; display: grid; place-items: center; }
.r3d-pad button:nth-child(4), .r3d-pad button:nth-child(8) { background: oklch(0.92 0.06 235); }
.r3d-pad button:active { background: var(--ink); color: var(--cream); }
.r3d-pad .ms { font-size: 22px; }
@media (min-width: 900px) { .r3d-pad { bottom: 104px; } }
@media (max-width: 899px) { .r3d-pad { left: 10px; bottom: calc(max(8px, env(safe-area-inset-bottom)) + 84px); } .r3d.tools-open .r3d-pad { display: none; } }
.r3d.editing .r3d-pad { display: none; }
@media (max-width: 899px) { .r3d-toast { top: 132px; max-width: calc(100vw - 32px); text-align: center; } }   /* v32: under the Menu button too */   /* v30: under the brand pill and the labels switch on a phone */
.r3d-tourgo .btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; min-height: 48px; font-size: 16px; }
.r3d-ui .chip .ms, .r3d-ui .btn .ms { font-size: 19px; vertical-align: -4px; }
.r3d-svars [hidden] { display: none; }
.r3d-linkbox { width: 100%; margin-top: 4px; min-height: 40px; border: 0; border-radius: 12px; padding: 6px 10px; background: var(--soft); color: var(--ink); font: 500 13px Figtree, system-ui, sans-serif; }
@media (max-width: 899px) { .r3d-tour { left: 12px; right: 12px; transform: none; width: auto; bottom: 92px; } }
@media (prefers-reduced-motion: reduce) { .r3d *, .stk { transition: none !important; } }
"""


def scenes_json():
    return json.dumps({k: {"name": n, "levels": lv} for k, n, _, lv, _ in scenes.SCENES})


def rules_json():
    """v25: the table rule and where the old scene keys went (room3d.js maps saved choices with it)."""
    return json.dumps({"boost": scenes.TABLE_BOOST, "old": scenes.OLD_TO_NEW})


LIGHTS = [("strip", "Ceiling LED strip", None), ("uprights", "Upright grooves and the side shelf (smart colour strips)", "strips"), ("bias", "TV bias light", None),
          ("bar1", "Bar 1, TV to window (smart colour)", "bar1"), ("bar2", "Bar 2, by the stairs (smart colour)", "bar2"),
          ("lamp", "Red lamp: top, middle, bottom", "lamp")]
CEIL_PRESETS = [("match", "Same as the walls"), ("#f2f0ea", "White")]
SKIRT_PRESETS = [("match", "Same as the walls"), ("#ece8dd", "Off-white"), ("#5e6a5b", "Green Smoke")]
# v25: the five Tools tabs (were v22's drawers): (key, name, icon, hue)
DRAWERS = [("views", "Views", "photo_camera", 235), ("layout", "Layout", "chair", 50), ("lights", "Lights", "lightbulb", 95), ("look", "Look", "palette", 165), ("extras", "Extras", "auto_awesome", 300)]
# One Tools button holds every 3D control: the pill (on a laptop) or the bottom bar's Tools button (on a phone, [data-tools-toggle])
# opens the bubble row; a bubble opens its panel. The last tab is remembered (mw22-drawer); Esc and the pill close it.
DRAWER_JS = """(() => { const r = document.getElementById("r3d"); if (!r) return;
  const K = "mw22-drawer", tabs = [...r.querySelectorAll("[data-drawer]")], panel = document.getElementById("r3d-panel"), btns = [...document.querySelectorAll("[data-tools-toggle]")];
  let cur = "layout", shown = ""; try { cur = localStorage.getItem(K) || "layout"; } catch (e) {}
  if (!tabs.some(t => t.dataset.drawer === cur)) cur = "layout";
  const sync = open => { r.classList.toggle("tools-open", open); document.body.classList.toggle("tools-open", open);
    document.querySelectorAll("[data-tools-toggle]").forEach(b => { b.setAttribute("aria-expanded", String(open)); const i = b.querySelector(".ms"); if (i) i.textContent = open ? "close" : "tune"; }); };
  const showing = () => !panel.hidden;
  const show = k => { cur = k; tabs.forEach(t => { const on = t.dataset.drawer === k; t.setAttribute("aria-selected", String(on)); t.tabIndex = on || panel.hidden ? 0 : -1;
      document.getElementById("r3d-dp-" + t.dataset.drawer).hidden = !on; });
    const sc = panel.querySelector(".r3d-pscroll"); if (sc && k !== shown) sc.scrollTop = 0; shown = k;
    if (typeof arts === "function") arts(document.getElementById("r3d-dp-" + k));
    panel.hidden = false; panel.setAttribute("aria-labelledby", "r3d-dt-" + k); try { localStorage.setItem(K, k); } catch (e) {} };
  const open = k => { sync(true); show(k || cur); window.dispatchEvent(new CustomEvent("demma-tools", { detail: true })); };
  const close = () => { sync(false); panel.hidden = true; tabs.forEach(t => { t.setAttribute("aria-selected", "false"); t.tabIndex = 0; }); window.dispatchEvent(new CustomEvent("demma-tools", { detail: false })); };
  window.DemmaTools = { open, close, toggle() { r.classList.contains("tools-open") ? close() : open(); }, isOpen: () => r.classList.contains("tools-open") };
  document.addEventListener("click", e => { if (e.target.closest("[data-tools-toggle]")) window.DemmaTools.toggle(); });   // the phone's bottom bar comes later in the page
  // v32: the bubbles are always on the room: one opens its panel (and marks the tools open), the open one again closes it
  tabs.forEach((t, i) => { t.addEventListener("click", () => { if (showing() && cur === t.dataset.drawer) close(); else open(t.dataset.drawer); });
    t.addEventListener("keydown", e => { const d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0; if (!d) return;
      const n = tabs[(i + d + tabs.length) % tabs.length]; n.focus(); show(n.dataset.drawer); }); });
  document.addEventListener("keydown", e => { if (e.key === "Escape" && r.classList.contains("tools-open") && !document.body.classList.contains("sheet-open")) close(); });
  sync(false); panel.hidden = true;
})();"""
SUGG_SHORT = {"floorplant": "Tall floor plant", "sidetable": "Round side table", "pouffe": "Knitted pouffe", "art": "Print over the sofa",
              "clock": "Clock over the door", "tray": "Coffee-table tray",
              "fairy": "Fairy lights on the pole", "hanger": "Hanging plant in the window", "trail": "Trailing plant, top shelf",
              "throw": "Knit throw on the sofa", "pclamp": "Mushroom lamp, PC shelf", "basket": "Seagrass basket",
              "candles": "LED candles on the shelf", "runner": "Table runner and vase", "floorcush": "Floor cushions",
              "lantern": "Rattan floor lantern", "mirror": "Arched mirror", "shelfled": "LED strip under the shelf",
              "barcase": "Drinks cabinet, breast", "bartrolley": "Drinks trolley", "blind": "Blackout blind", "cablights": "Lights in the cabinet",
              "barside": "Drinks cabinet, by the sofa", "blanketbasket": "Blanket basket", "liftcoffee": "Lift-top coffee table", "doorshelf": "Shelf over the door",
              "shelfboxes": "Boxes on your shelf", "plantshelf": "Plant shelf, 10 off the wall"}   # v36   # v32   # v26   # v23   # v21: the buttons' words for ideas.SUGGEST
IDEA_SHORT = {"case": "Glass case on the breast", "glass": "Glass plant shelves", "ctable": "Sofa C-table", "sync": "TV backlight, picture sync",
              "cushions": "Cushions and a throw", "plantlight": "Uplight under the plants", "rugpad": "Rug pad (corner turned back)",
              "button": "Scene button by the door", "night": "Stair nightlights", "clean": "Record-care caddy"}   # v32: every idea in the room
# v20: decor to try in the 3D room (room3d.js S.decor; the keys match its RUG_LOOKS, CUSHION_COLS, CURTAIN_COLS, the case's PRESETS, CASE_FRAMES)
DECOR = [("rug", "Rug", [("yours", "Arches (the plan's)"), ("jute", "Jute flatweave"), ("blue", "Deep blue"), ("stripes", "Sage stripes"), ("none", "No rug")]),
         ("cushions", "Sofa cushions", [("none", "None"), ("rust", "Rust and ochre"), ("blues", "Blues"), ("sage", "Sage and cream")]),
         ("curtains", "Curtains", [("hessian", "Your hessian"), ("linen", "White linen"), ("sage", "Sage"), ("blue", "Deep blue"), ("rust", "Rust")]),
         ("fill", "In the glass case", [("collect", "Collectibles"), ("games", "Retro games"), ("singles", "7-inch singles and tapes"), ("plants", "Plants and ceramics"), ("mixed", "A bit of each")]),
         ("frame", "The case's frame", [("oak", "Oak"), ("black", "Black"), ("white", "White")]),
         # v26: more to try: the oak's finish (every new oak piece), the floor, your black shelf
         ("oak", "The oak, on everything new", [("artisan", "Artisan oak (the plan)"), ("pale", "Pale, white-oiled"), ("smoked", "Smoked oak"), ("walnut", "Walnut")]),
         ("floor", "The floor", [("carpet", "Your grey carpet"), ("oatmeal", "Oatmeal carpet"), ("boards", "Oak floorboards")]),
         ("shelf", "Your shelf by the stairs", [("black", "Black (yours)"), ("oak", "Oak"), ("white", "White")]),
]   # v33: the tie-on seat pads went with the FRÖSVI (your padded chairs need none)
DECOR_GROUPS = [("Wood and floor", ("oak", "floor", "shelf")), ("Soft things", ("rug", "cushions", "curtains")), ("The glass case on the breast", ("fill", "frame"))]


def tour():
    """v28, from the optimisation plan: "a guided tour": the room's main views in turn, a caption each (numbers from geometry, so they
    follow the next round). set: choices shown for that stop only (put back after it)."""
    g = G
    s = g.summary()
    return [
        dict(view="room", title="The whole room", text=f"From above the window, the near wall cut away: the media wall, the breast, the door, the stairs and the dining cabinet, under a {g.CEIL:g} ceiling."),
        dict(view="wall", title="The media wall", text=f"Artisan oak in Card Room Green across the {g.ALC_W:g} cm alcove: the TV centred at {g.TV_CENTRE:.1f}, the turntable on the right, the consoles and the LP crates below."),
        dict(view="pc", title="The PC side wall", text=f"One oak run sweeps round the corner to the PC shelf at {g.PC_SHELF_TOP:g}, its leads inside the wall and a warm strip underneath."),
        dict(view="breast", title="The chimney breast", text=f"Your vinyl stand with {g.STAND_LPS} LPs and the “now playing” ledge at {g.NOW_LEDGE['top']:g}: about {g.ALL_LPS} LPs in the room in all."),
        dict(view="dining", title="The dining cabinet, open", set={"site": "C", "dining": "six", "cab": "compact"},
             text=f"The table door swings back flat and the table folds down to {g.CAB['len_open']:g} × {g.CAB['top'][0]:g} for six. Folded, the table and all six chairs pack into {g.CAB['len']:.0f} cm of wall."),
        dict(view="sit", title="Sitting at the table", set={"site": "C", "dining": "six", "cab": "compact"},
             text=f"At the table's far end, at a seated eye height: three a side with {g.CAB['len_open'] / 3:.0f} cm of edge each, the table door folded back flat behind them."),
        dict(view="sofa", title="From the sofa", text=f"About {s['view_dist'] / 100:.2f} m from the screen: the 55-inch fills about {s['view_angle']:.0f}° of your view, right for films and games."),
        dict(view="window", title="From the window", text="The whole wall in one look, over the sofa's back: your plants on the sill behind you."),
        dict(view="plan", title="From above", text="Everything to scale from the plan's own measurements. Drag to look round when the tour ends."),
    ]


PAGES_URL = "https://emmachilds98-wq.github.io/DIY/"   # v28: "Copy link to this view" always gives a link anyone can open


def svar_json():
    """v28: each suggestion's versions for room3d.js (colours) and Your picks (names)."""
    return json.dumps({k: [[v, n, c] for v, n, c in vs] for k, vs in ideas.SUGG_VARS.items()}, separators=(",", ":"))


def controls(gallery=""):
    """v25: the Tools panels. Same data-* hooks as v24's drawers (room3d.js binds to them), new containers: pill rows, preset tiles,
    round paint swatches. gallery: the HD pictures (build_viewer.gallery3d), shown under Views."""
    seg = lambda attr, items, lab, extra="": (f'<div class="grp"><span class="label">{lab}</span><div class="seg" role="group" aria-label="{html.escape(lab)}">'
                                              + "".join(f'<button type="button" data-{attr}="{k}" aria-pressed="false">{v}</button>' for k, v in items) + extra + "</div></div>")
    rows = []
    for k, lab, col in LIGHTS:
        cols = ""
        if col == "lamp":
            cols = "".join(f'<input type="color" data-col="lamp{i}" value="{c}" aria-label="Lamp bulb {n} colour">' for i, (c, n) in enumerate(zip(G.LAMP_HEADS_RGB, ("top", "middle", "bottom"))))
        elif col:
            cols = f'<input type="color" data-col="{col}" value="#ffe2b8" aria-label="{html.escape(lab)} colour"><button type="button" class="chip" data-colreset="{col}">Warm white</button>'
        rows.append(f'<div class="r3d-lv"><label for="lv-{k}">{html.escape(lab)}</label><input type="range" id="lv-{k}" min="0" max="100" step="1" data-lv="{k}">'
                    f'<output data-lvout="{k}">0%</output><span class="r3d-cols">{cols}</span></div>')
    TILE_SUB = {"bright": "Everything on, even", "cosy": "Low and warm", "film": "Films and games"}   # v26: the tiles' second line, whole
    icons = {"bright": "light_mode", "cosy": "local_fire_department", "film": "movie"}
    tiles = "".join(f'<button type="button" data-scene="{k}" aria-pressed="false"><span class="ms" aria-hidden="true">{icons.get(k, "lightbulb")}</span><b>{html.escape(n)}</b>'
                    f'<span>{html.escape(TILE_SUB.get(k, d.split(":")[0].split(",")[0]))}</span></button>' for k, n, d, *_ in scenes.SCENES)
    lights = (f'<div class="grp"><span class="label">Three presets: tap one (tap it again to undo your changes)</span><div class="r3d-tiles" role="group" aria-label="Lighting presets">{tiles}</div></div>'
              f'<p class="r3d-boost" id="r3d-boost" hidden><span class="ms" aria-hidden="true">restaurant</span> The table\'s open, so bar 2 lights it.</p>'
              + seg("tod", scenes.TOD, "Time of day")
              + '<details class="r3d-more"><summary>Fine-tune each light</summary>'
              f'<div class="r3d-lvs"><div class="r3d-lv r3d-master"><label for="lv-master">All lights</label><input type="range" id="lv-master" min="0" max="100" step="1" data-lv="master"><output data-lvout="master">100%</output><span></span></div>'
              + "".join(rows) + '</div></details>'
              '<div class="grp"><span class="label">Switch on or off</span><div class="seg" role="group" aria-label="Light box, laser, PC and curtains"><button type="button" data-tog="lbox" aria-pressed="false">IKEA light box</button>'
              '<button type="button" data-tog="laser" aria-pressed="false">Laser</button>'
              '<button type="button" data-tog="pc" aria-pressed="false">PC lit</button>'
              '<button type="button" data-tog="curtains" aria-pressed="false">Curtains drawn</button></div></div>')
    ideas_g = ('<div class="grp"><span class="label">Ideas (not in the plan)</span>'
               '<div class="seg" role="group" aria-label="Ideas, not in the plan">'
               + "".join(f'<button type="button" data-idea="{k}" aria-pressed="false" title="{html.escape(size)}">{html.escape(IDEA_SHORT[k])}</button>'
                         for k, _t, size, *_ in ideas.IDEAS if k != "cushions")      # the cushions are Decor's
               + '</div></div>')
    dec = {k: (lab, opts) for k, lab, opts in DECOR}
    decor_g = "".join('<div class="grp r3d-decor"><span class="label">' + html.escape(title) + '</span>'
               + "".join(f'<div class="r3d-decrow"><span>{html.escape(dec[k][0])}</span><div class="seg" role="group" aria-label="{html.escape(dec[k][0])}">'
                         + "".join(f'<button type="button" data-decor="{k}:{v}" aria-pressed="false">{html.escape(n)}</button>' for v, n in dec[k][1]) + '</div></div>'
                         for k in keys) + '</div>' for title, keys in DECOR_GROUPS)
    # v26: the ceiling and the skirting (with the door and its frame) back in Look: the walls' colour, white, or any colour
    trims = "".join(f'<div class="grp"><span class="label">{lab}</span><div class="seg" role="group" aria-label="{lab}">'
                    f'<button type="button" data-{key}="match" aria-pressed="false">Same as the walls</button><button type="button" data-{key}="#f2efe8" aria-pressed="false">White</button>'
                    f'<label class="chip r3d-anycol">Any colour <input type="color" id="r3d-{key}" value="#f2efe8" aria-label="{lab}: any colour"></label></div></div>'
                    for key, lab in (("ceil", "The ceiling"), ("skirt", "Skirting, the door and its frame")))
    sugg_g = ('<div class="grp"><span class="label">Every suggestion, one by one (not in the plan)</span>'
              '<div class="seg" role="group" aria-label="Suggested furniture and decor">'
              + "".join(f'<button type="button" data-sugg="{k}" aria-pressed="false" title="{html.escape(size)}">{html.escape(SUGG_SHORT[k])}</button>' for k, _t, size, *_ in ideas.SUGGEST)
              + '<button type="button" class="chip" data-suggall="on">All on</button><button type="button" class="chip" data-suggall="off">All off</button></div></div>'
              # v28: two or three versions of each, a row for every suggestion that's switched on
              '<div class="grp r3d-svars" id="r3d-svars"><span class="label">Choose a version</span>'
              '<p class="caption" id="r3d-svnone">Switch a suggestion on and its versions show here.</p>'
              + "".join(f'<div class="r3d-decrow" data-svrow="{k}" hidden><span>{html.escape(SUGG_SHORT[k])}</span><div class="seg" role="group" aria-label="{html.escape(SUGG_SHORT[k])}: version">'
                        + "".join(f'<button type="button" data-svar="{k}:{v}" aria-pressed="false">{html.escape(n)}</button>' for v, n, _c in ideas.SUGG_VARS[k]) + '</div></div>'
                        for k, *_ in ideas.SUGGEST)
              + '</div>'
              '<div class="grp"><span class="label">Something of your own</span><div class="seg"><button type="button" class="chip" id="r3d-addfrom">'
              '<span class="ms" aria-hidden="true">add</span> Add a piece of furniture</button></div>'
              '<span class="caption">Opens Edit room with its list: an armchair, a bookcase, a bench and more. Drag it where you like.</span></div>')
    views = "".join(f'<button type="button" class="chip" data-view="{k}" aria-pressed="false">{v}</button>' for k, v in VIEWS)
    # v31, client: "explore what could go next to the dining cabinet in the compact version": the wall between it and the pipe boxing
    BESIDE_SEG = ('<h3 class="r3d-sub">Beside the cabinet</h3>'
                  + seg("beside", [(k, v["name"]) for k, v in G.BESIDE["opts"].items()], f"The {G.BESIDE['len']:.0f} cm of wall by the pipe boxing")
                  + '<p class="caption">The open table door lies back over this wall while you eat, so anything here stays slim: '
                  f'{G.BESIDE["depth"]:g} cm deep at most. <button type="button" class="chip" data-view="beside">See it</button></p>')
    picks = ('<div class="grp r3d-picks" id="r3d-picks"><span class="label">Your picks</span>'
             '<p class="r3d-picklist" id="r3d-picklist" aria-live="polite">Nothing switched on yet: turn on an idea, a suggestion or a decor choice and it shows here.</p>'
             '<div class="seg"><button type="button" class="chip" id="r3d-pickcopy">Copy as a note</button>'
             '<button type="button" class="chip" id="r3d-picksave" hidden>Save for the next round</button><span class="r3d-hint2" id="r3d-pickst" aria-live="polite"></span></div></div>')
    paints = [(k, h, n.split(" No.")[0].replace("Farrow & Ball ", "").replace("Little Greene ", "")) for k, (h, n) in R.PAINTS.items()]
    swatches = ('<div class="grp"><span class="label">Wall paint (or tap a wall in Edit room)</span><div class="r3d-swatches" role="group" aria-label="Wall paint">'
                + "".join(f'<button type="button" data-paint="{k}" aria-pressed="false"><i style="--c:{h}"></i>{html.escape(n)}</button>' for k, h, n in paints)
                + '<button type="button" data-paintcustom="#2c5643" aria-pressed="false"><i style="--c:#2c5643"></i>Deep green</button>'
                '<label><i><input type="color" id="r3d-custom" value="#899081" aria-label="Any colour for the walls"></i>Any colour</label></div></div>')
    return {
        "views": '<div class="grp r3d-tourgo"><button class="btn primary" type="button" id="r3d-tourbtn"><span class="ms" aria-hidden="true">play_circle</span> Take the tour</button>'
                 f'<span class="caption">{len(tour())} stops round the room, about a minute; tap the room to stop.</span></div>'
                 + f'<div class="grp"><span class="label">Where you look from</span><div class="r3d-views" role="group" aria-label="Camera">{views}</div></div>'
                 # v31, client: "make camera movement easier within the 3d render. being able to adjust height would be good"
                 + '<div class="grp r3d-move"><span class="label">Move round</span>'
                 '<div class="r3d-eyerow"><label for="r3d-eye">Eye height</label><input type="range" id="r3d-eye" min="40" max="220" step="5" value="160">'
                 '<output id="r3d-eyeout" for="r3d-eye">160 cm</output></div>'
                 '<div class="seg" role="group" aria-label="Eye height"><button type="button" data-eye="115">Sitting, 115</button><button type="button" data-eye="160">Standing, 160</button>'
                 '<button type="button" data-eye="210">High, 210</button><button type="button" data-level="1">Level the view</button></div></div>'
                 + seg("cam", [("orbit", "Circle round a spot"), ("look", "Look round from here")], "Dragging the room")
                 + seg("pad", [("on", "Show"), ("off", "Hide")], "Move buttons on the room")
                 + seg("labels", [("on", "Show"), ("off", "Hide")], "The numbered labels on the room")
                 + '<div class="grp r3d-sharegrp"><span class="label">Share this view</span><div class="seg"><button type="button" class="chip" id="r3d-link"><span class="ms" aria-hidden="true">link</span> Copy link to this view</button></div>'
                 '<span class="caption" id="r3d-linkst" aria-live="polite">The link opens the room on this view, with your table, lights, paint, decor and suggestions.</span></div>'
                 + '<div class="grp r3d-save"><button class="btn primary" type="button" id="r3d-save">Save as HD picture</button>'
                 '<span class="caption" id="r3d-savest" aria-live="polite">3840 × 2160, with shadows</span></div>'
                 + (f'<div class="grp"><span class="label">HD pictures (tap one to see it big)</span>{gallery.replace(chr(34) + "gallery" + chr(34), chr(34) + "gallery r3d-gal" + chr(34), 1)}</div>' if gallery else "")
                 + '<p class="caption"><b>Tap something in the room to work it:</b> the dining cabinet opens, folds and shows how it opens; the drawers pull out; the lamp, the spot bars, the TV, the curtains, the light box and the PC switch; the blind rolls up; your vinyl stand\'s front records lift out; the trolley beside the cabinet wheels to the table; and any idea or suggestion you\'ve switched on changes version or goes.</p>'
                 + '<p class="caption">Drag to look round, pinch or scroll to zoom (looking round from where you stand, scrolling walks you forward and back). '
                 'On a keyboard: W A S D or the arrows walk, Q and E turn, R and F go up and down. Lost? Pick a view above, or Reset view.</p>',
        # v31, client: "upgrade the views and layouts area of the site to ensure it reflects our recent upgrades": grouped, the compact cabinet
        # first, with what goes beside it, how it opens, the floor it needs, and ready-made set-ups to try
        "layout": "".join([
            '<h3 class="r3d-sub">The dining cabinet</h3>',
            # v33, client: "The compact cabinet is our only choice for the table now or any upgraded more compact version for this"
            seg("cabw", [("90", f"{G.CAB['top'][0]:g} wide, {G.CAB['len']:.1f} long, six chairs inside (the plan)"),
                         ("80", f"{G.CAB80['top'][0]:g} wide, {G.CAB80['len']:.1f} long, four chairs inside")], "The compact cabinet: its table's width"),
            seg("dining", [("folded", "Folded"), ("four", "Open, four"), ("six", "Open, six")], "Folded or open"),
            seg("tdoor", [("shut", "Shut"), ("open", "Open")], "The table door, with the table folded"),
            seg("chairs", [("cupboard", "Shut"), ("open", "Open")], "The chair door, with the table folded"),
            '<div class="grp"><span class="label">See how it works</span><div class="seg"><button type="button" class="chip" data-showopen="1"><span class="ms" aria-hidden="true">play_arrow</span> Watch it open</button></div>'
            '<span class="caption">Slowly, step by step: the doors, the chairs, then the table unfolding joint by joint, about 40 seconds. '
            'Pause it or step back and on; you can look round while it plays.</span></div>',
            seg("foot", [("off", "Hide"), ("on", "Show")], "The floor it needs when it's open (table, chairs, the door's swing)"),
            '<div class="grp"><span class="label">Try a set-up</span><div class="seg r3d-moments">'
            '<button type="button" data-moment="dinner"><span class="ms" aria-hidden="true">dinner_dining</span> Dinner for six</button>'
            '<button type="button" data-moment="four"><span class="ms" aria-hidden="true">lunch_dining</span> Lunch for four</button>'
            '<button type="button" data-moment="film"><span class="ms" aria-hidden="true">movie</span> Film night</button>'
            '<button type="button" data-moment="morning"><span class="ms" aria-hidden="true">wb_sunny</span> Everyday morning</button></div>'
            '<span class="caption">Each sets the table, the lights and the curtains together, then shows you the room.</span></div>',
            BESIDE_SEG,
            '<h3 class="r3d-sub">Around the room</h3>',
            seg("plants", [(k, v["name"]) for k, v in G.PLANT_LAYOUTS.items()], "Plant stand and vinyl stand"),
            seg("drawers", [("in", "Shut"), ("out", "Pulled out")], "The media wall's drawers"),
            '<p class="caption">Or tap the cabinet in the room: its card opens it for four or six, folds it, opens either door and swaps the table\'s width.</p>']),
        "lights": lights + seg("quality", [("hd", "HD, with shadows"), ("fast", "Fast")], "Quality"),
        "look": swatches + trims + decor_g,
        "extras": opts_html() + picks + ideas_g + sugg_g,
    }


def opts_json():
    """v36: the option groups (ideas.OPTION_GROUPS) with what each item is, where it goes, its size and cost, and where to look."""
    import item_shots
    sug = {k: (t, size, c, where) for k, t, size, c, _why, where in ideas.SUGGEST}
    B = G.BESIDE
    extra = {"rail": ("An oak blanket rail beside the dining cabinet", f"{B['rail']['w']:g} wide, four 28 mm oak rails, 12 off the wall", (25, 45),
                      "On the wall beside the dining cabinet, under your black shelf: the open table door lies back over it while you eat."),
             "on": ("Your storage ottoman, the lid on", "76 × 76 × 45", None, "On the rug by the coffee table."),
             "off": ("Your storage ottoman, the lid off", f"{G.OTTO_GAMES['games']} square games and the cards inside", None, "On the rug by the coffee table.")}
    view = {"rail": dict(view="beside"), "on": dict(eye=[300, 150, -60], at=[238, 30, -157], fov=50), "off": dict(eye=[300, 150, -60], at=[238, 30, -157], fov=50)}
    groups = []
    for key, title, mode, note, items in ideas.OPTION_GROUPS:
        its = []
        for v, label, setv in items:
            t, size, cost, where = sug[v] if v in sug else extra[v]
            a = item_shots.AIM.get(f"3d_sg_{v}")
            aim = view.get(v) or (dict(eye=a[0], at=a[1], fov=a[2]) if a else None)
            its.append(dict(v=v, label=label, set=setv, title=t, size=size, cost=list(cost) if cost else None, where=where, aim=aim))
        groups.append(dict(k=key, title=title, mode=mode, note=note, items=its))
    return json.dumps(dict(groups=groups), separators=(",", ":"))


def opts_html():
    """v36, client: "make sure its clear how to manage all these options in the 3D room": Extras opens on one row per need."""
    rows = ""
    for key, title, mode, note, items in ideas.OPTION_GROUPS:
        btns = ('<button type="button" data-opt="%s:none" aria-pressed="false">None</button>' % key) if mode == "one" else ""
        btns += "".join(f'<button type="button" data-opt="{key}:{v}" aria-pressed="false">{html.escape(label)}</button>' for v, label, _s in items)
        btns += f'<button type="button" class="chip" data-optsee="{key}"><span class="ms" aria-hidden="true">visibility</span> See it</button>'
        how = {"one": "Pick one", "any": "Switch on any", "lid": "Open or shut"}[mode]
        rows += (f'<div class="r3d-optrow" data-optgrp="{key}"><h3 class="r3d-sub">{html.escape(title)} <span class="r3d-optmode">{how}</span></h3>'
                 f'<div class="seg" role="group" aria-label="{html.escape(title)}">{btns}</div>'
                 f'<p class="caption" data-optcap="{key}" aria-live="polite">{html.escape(note)}</p></div>')
    return ('<div class="grp r3d-opts" id="r3d-opts"><span class="label">Storage and a bar: your options</span>'
            '<p class="caption r3d-opthow"><b>How it works:</b> pick an option and the room shows it and takes you to it; <b>None</b> takes it away; '
            '<b>See it</b> takes you back. Tap a piece in the room for its colours, to move it or to take it away. What you pick shows in '
            '<b>Your picks</b> below with a rough cost, and goes with <b>Copy link to this view</b> (Views).</p>' + rows + '</div>')


def picks_json():
    """v22: what "Your picks" needs to name and cost what's switched on (ideas.IDEAS and ideas.SUGGEST)."""
    out = {"ideas": {k: [t, c[0], c[1]] for k, t, _s, c, *_ in ideas.IDEAS},
           "sugg": {k: [t, c[0], c[1]] for k, t, _s, c, *_ in ideas.SUGGEST},
           "decor": {k: [lab, dict(opts)] for k, lab, opts in DECOR},
           "svar": {k: {v: n for v, n, _c in vs} for k, vs in ideas.SUGG_VARS.items()}}   # v28
    return json.dumps(out, separators=(",", ":"))


def _money(lo, hi):
    return f"£{lo:,}–{hi:,}"


def hotspots():
    """v25: the six numbered stickers on the room. at: the anchor in room cm; n: the wall's normal (room coords, the side the camera
    must be on to see it face on; None for the sofa); cut: the dolls'-house cutaway that opens that wall (room3d.js updateCut);
    view: Fly here; chapter: Open in the plan. Facts come from geometry, ideas and the buy list, so they follow the next round."""
    import build_doc as B
    def ph(*names):
        lo = sum(r[4] for r in B.TRACK if r[2] in names and r[4] is not None); hi = sum(r[5] for r in B.TRACK if r[2] in names and r[5] is not None)
        return _money(lo, hi)
    g = G
    pc_z = (g.PC_Z[0] + g.PC_Z[1]) / 2
    rug_w, rug_d = g.RUG["x"][1] - g.RUG["x"][0], g.RUG["z"][1] - g.RUG["z"][0]
    pl = g.PLANT_LAYOUTS["corner"]["plants"]
    PS = g.PLANT_STAND
    return [
        dict(id="wall", short="Media wall", n=1, name="The media wall", hue=300, at=[g.ALC_W / 2, 150, g.ALC_D - 26], nrm=[0, -1], cut="wall", view="wall", chapter="wall",
             facts=['LG C6 55" at 116.5', "Artisan oak in Card Room Green", "Steps 6–10", ph("4 Base unit", "5 Oak joinery")]),
        dict(id="pc", short="PC wall", n=2, name="The PC side wall", hue=235, at=[8, g.PC_SHELF_TOP + 32, pc_z], nrm=[1, 0], cut="pc", view="pc", chapter="side",
             facts=[f"PC shelf at {g.PC_SHELF_TOP:g}", "Leads inside the wall", "Warm LED strip underneath", "Step 10"]),
        dict(id="breast", short="Breast", n=3, name="Chimney breast", hue=345, at=[(g.BREAST_X[0] + g.BREAST_X[1]) / 2, 120, -6], nrm=[0, -1], cut="", view="breast", chapter="records",
             facts=[f"Vinyl stand, {g.STAND_LPS} LPs", f"“Now playing” ledge at {g.NOW_LEDGE['top']:g}", "Two framed LPs", "Vinyl kit " + ph("9 Vinyl kit")]),
        dict(id="dining", short="Cabinet", n=4, name="Dining cabinet", hue=50, at=[g.ROOM_W - 12, 110, g.CAB["cz"]], nrm=[-1, 0], cut="stairs", view="dining", chapter="dining",
             facts=[f"Table {g.CAB['len_open']:g} × {g.CAB['top'][0]:g}, six in comfort", f"{g.CAB['len']:.1f} long, six chairs inside", f"Or {g.CAB80['top'][0]:g} wide: {g.CAB80['len']:.1f} long, four chairs inside", "Tap it to open it", "Step 11", ph("6 Dining wall")]),
        dict(id="window", short="Window", n=5, name="Window & plants", hue=165, at=[pl[0], PS["h"] - 20, pl[1] + 8], nrm=[0, 1], cut="win", view="windowwall", chapter="c-room",
             facts=[f"Plant stand {PS['w']:g} × {PS['d']:g} × {PS['h']:g}", f"Window ledge {g.WINDOW_REVEAL + g.SILL['nose']:g} deep", "Hessian curtains"]),
        dict(id="sofa", short="Sofa", n=6, name="Sofa & rug", hue=95, at=[(g.SOFA_X[0] + g.SOFA_X[1]) / 2, 70, g.SOFA_BACK_Z + 55], nrm=None, cut="", view="sofa", chapter="c-room",
             facts=["Blue corduroy L-sofa", f"Rug {rug_w:g} × {rug_d:g}", "Ottoman end"]),
    ]


def section(gallery=""):
    """v25: the room as the home screen. The stage fills the screen; the stickers sit on it; the Tools pill (laptop) or the bottom
    bar's Tools button (phone, in build_viewer) opens the five panels; Edit room is a bubble beside them."""
    panels = controls(gallery)
    bubbles = "".join(f'<button type="button" class="r3d-bub" role="tab" id="r3d-dt-{k}" aria-controls="r3d-dp-{k}" aria-selected="false" data-drawer="{k}" style="--h:{h}">'
                      f'<i class="ms" aria-hidden="true">{ic}</i>{html.escape(n)}</button>' for k, n, ic, h in DRAWERS)
    drawers = "".join(f'<div class="r3d-ui r3d-dpanel" role="tabpanel" id="r3d-dp-{k}" aria-labelledby="r3d-dt-{k}" hidden><h2>{html.escape(n)}</h2>{panels[k]}</div>' for k, n, *_ in DRAWERS)
    stickers = "".join(f'<button type="button" class="stk" data-hot="{h["id"]}" style="--h:{h["hue"]};--tilt:{(-3, 2, -1, 3, -2, 1)[h["n"] - 1]}deg" aria-expanded="false" aria-controls="r3d-pop" aria-label="{h["n"]}, {html.escape(h["name"])}" hidden>'
                       f'<b>{h["n"]}</b><span class="t">{html.escape(h["name"])}</span></button>' for h in hotspots())
    # v33, the phone home: a strip of the places (tap one to fly there and open its card) and the set-ups as chips, under the room
    places = "".join(f'<button type="button" data-place="{h["id"]}" style="--h:{h["hue"]}"><b>{h["n"]}</b>{html.escape(h.get("short", h["name"]))}</button>' for h in hotspots())
    moments = "".join(f'<button type="button" data-moment="{k}"><span class="ms" aria-hidden="true">{ic}</span>{t}</button>'
                      for k, ic, t in (("dinner", "dinner_dining", "Dinner for six"), ("four", "lunch_dining", "Lunch for four"), ("film", "movie", "Film night"), ("morning", "wb_sunny", "Morning")))
    data = json.dumps(json.loads((HERE / "scene3d.json").read_text()), separators=(",", ":"))
    return f"""<div class="r3d" id="r3d">
  <div class="r3d-stage"><canvas tabindex="0" aria-label="The living room in 3D: drag to look round, scroll or pinch to zoom; WASD or the arrow keys walk, Q and E turn"></canvas>
    <img class="r3d-poster" data-art="3d_room" alt="" aria-hidden="true">
    <div class="r3d-msg" id="r3d-msg">Loading the 3D room…</div>
    <p class="r3d-cap sr-only" id="r3d-cap"></p>
    <div class="r3d-stickers" id="r3d-stickers">{stickers}</div>
    <div class="r3d-phone"><div class="r3d-moms" role="group" aria-label="Try a set-up">{moments}</div>
      <div class="r3d-places" role="group" aria-label="Places in the room">{places}</div></div>
    <div class="r3d-tour" id="r3d-tour" role="region" aria-label="Tour of the room" aria-live="polite" hidden><span class="r3d-tourn" id="r3d-tourn"></span><h3 id="r3d-tourh"></h3><p id="r3d-tourp"></p>
      <div class="acts"><button type="button" data-tour="prev" aria-label="Back one stop"><span class="ms" aria-hidden="true">skip_previous</span></button><button type="button" data-tour="pause" aria-label="Pause"><span class="ms" aria-hidden="true">pause</span></button><button type="button" data-tour="next" aria-label="Next stop"><span class="ms" aria-hidden="true">skip_next</span></button><button type="button" class="end" data-tour="stop">End the tour</button></div>
      <i class="r3d-tourbar"><b id="r3d-tourbar"></b></i></div>
    <div class="r3d-tour r3d-show" id="r3d-show" role="region" aria-label="Watch it open" aria-live="polite" hidden><span class="r3d-tourn" id="r3d-shown"></span><h3 id="r3d-showh"></h3><p id="r3d-showp"></p>
      <div class="acts"><button type="button" data-show="prev" aria-label="Back a step"><span class="ms" aria-hidden="true">skip_previous</span></button><button type="button" data-show="pause" aria-label="Pause"><span class="ms" aria-hidden="true">pause</span></button><button type="button" data-show="next" aria-label="Next step"><span class="ms" aria-hidden="true">skip_next</span></button><button type="button" class="end" data-show="stop">Stop</button></div>
      <i class="r3d-tourbar"><b id="r3d-showbar"></b></i></div>
    <div class="r3d-toast" id="r3d-toast" role="status" hidden></div>
    <div class="r3d-pad" id="r3d-pad" role="group" aria-label="Move the camera (hold a button to keep moving)" hidden><button type="button" data-walk="tl" aria-label="Turn left" title="Turn left"><span class="ms" aria-hidden="true">rotate_left</span></button><button type="button" data-walk="f" aria-label="Walk forward" title="Walk forward"><span class="ms" aria-hidden="true">arrow_upward</span></button><button type="button" data-walk="tr" aria-label="Turn right" title="Turn right"><span class="ms" aria-hidden="true">rotate_right</span></button><button type="button" data-walk="u" aria-label="Up" title="Up"><span class="ms" aria-hidden="true">keyboard_arrow_up</span></button><button type="button" data-walk="l" aria-label="Step left" title="Step left"><span class="ms" aria-hidden="true">arrow_back</span></button><button type="button" data-walk="b" aria-label="Walk back" title="Walk back"><span class="ms" aria-hidden="true">arrow_downward</span></button><button type="button" data-walk="r" aria-label="Step right" title="Step right"><span class="ms" aria-hidden="true">arrow_forward</span></button><button type="button" data-walk="dn" aria-label="Down" title="Down"><span class="ms" aria-hidden="true">keyboard_arrow_down</span></button></div>
    <button type="button" class="r3d-lbl" id="r3d-lbl" aria-pressed="true" title="Show or hide the numbered labels on the room"><span class="ms" aria-hidden="true">label_off</span><span class="t">Hide labels</span></button>
    <div class="r3d-pop" id="r3d-pop" role="dialog" aria-modal="false" aria-labelledby="r3d-pop-h" hidden><button type="button" class="x" aria-label="Close"><span class="ms" aria-hidden="true">close</span></button>
      <h3 id="r3d-pop-h"></h3><ul class="facts"></ul><div class="acts"><button type="button" class="go" data-popgo="plan">Open in the plan</button><button type="button" data-popgo="fly">Fly here</button></div></div>
    <div class="r3d-pop r3d-act" id="r3d-act" role="dialog" aria-modal="false" aria-labelledby="r3d-act-h" hidden><button type="button" class="x" aria-label="Close"><span class="ms" aria-hidden="true">close</span></button>
      <h3 id="r3d-act-h"></h3><p class="st" id="r3d-act-st" aria-live="polite"></p><div class="acts" id="r3d-acts"></div></div>
    <div class="r3d-edit">
      <div class="r3d-editbar" id="r3d-editbar" hidden><button type="button" id="r3d-editdone" class="primary">✓ Done</button><button type="button" id="r3d-add">+ Add</button><button type="button" id="r3d-undo" disabled title="Undo (Ctrl+Z)">↶ Undo</button><button type="button" id="r3d-layreset">Reset layout</button>
        <button type="button" class="r3d-share" id="r3d-share" hidden title="Save this layout so Emma and Dave both see it">Save for both of you</button><button type="button" class="r3d-share" id="r3d-useshared" hidden>Use the shared layout</button><span class="r3d-hint" id="r3d-sharest" aria-live="polite"></span>
        <span class="r3d-hint">Drag a thing to move it (it snaps to a wall within 15 cm); tap it to turn, recolour, copy or remove it. Tap a wall, the ceiling or the skirting to paint it.</span></div>
      <div class="r3d-addlist" id="r3d-addlist" hidden></div>
      <div class="r3d-sel" id="r3d-sel" hidden><b id="r3d-selname"></b><span class="r3d-size" id="r3d-selsize"></span><button type="button" data-sel="turn" title="A quarter turn; against a wall it stays against it">⟳ Turn</button><button type="button" data-sel="turn45" title="An eighth of a turn">45°</button><button type="button" data-sel="wall" title="Push it to the nearest wall, its back to the wall">⇥ Back to the wall</button>
        <label>Colour <input type="color" id="r3d-selcol" value="#888888"></label><span id="r3d-swatches" hidden></span>
        <button type="button" data-sel="copy" hidden>Copy</button><button type="button" data-sel="remove">Remove</button><button type="button" data-sel="done">Done</button></div></div>
  </div>
  <div class="r3d-dock"><button type="button" class="r3d-toolsbtn" data-tools-toggle aria-expanded="false" aria-controls="r3d-panel"><span class="ms" aria-hidden="true">tune</span>Tools</button>
    <div class="r3d-bubbles" role="tablist" aria-label="3D room controls"><button type="button" class="r3d-bub r3d-menub" id="r3d-menub" aria-expanded="false" aria-controls="rail-list" style="--h:280" hidden><i class="ms" aria-hidden="true">menu</i>Menu</button>{bubbles}
      <button type="button" class="r3d-bub" id="r3d-editbtn" aria-pressed="false" style="--h:25" title="Move, turn, recolour, remove and add things; tap a wall to paint it"><i class="ms" aria-hidden="true">edit</i>Edit</button></div></div>
  <div class="r3d-panel" id="r3d-panel" role="region" aria-label="3D room controls" hidden><button type="button" class="r3d-px" data-tools-toggle aria-label="Close the tools"><span class="ms" aria-hidden="true">close</span></button>
    <div class="r3d-pscroll">{drawers}</div>
    <div class="r3d-foot"><span class="r3d-litst" id="r3d-litst"></span><button type="button" id="r3d-reset">Reset view</button><button type="button" id="r3d-full">Full screen</button></div></div>
</div>
<script type="application/json" id="picks-data">{picks_json()}</script>
<script type="application/json" id="scene3d-data">{data}</script>
<script type="application/json" id="scenes-data">{scenes_json()}</script>
<script type="application/json" id="lightrules-data">{rules_json()}</script>
<script type="application/json" id="svar-data">{svar_json()}</script>
<script type="application/json" id="opt-data">{opts_json()}</script>
<script type="application/json" id="tour-data">{json.dumps(dict(stops=tour(), pages=PAGES_URL), separators=(",", ":"))}</script>
<script type="application/json" id="hotspots-data">{json.dumps(hotspots(), separators=(",", ":"))}</script>
<script type="module">{(HERE / "room3d.js").read_text()}</script>
<script>{DRAWER_JS}</script>
<script>setTimeout(() => {{ const r = document.getElementById("r3d"), m = document.getElementById("r3d-msg");
  if (r && !r.classList.contains("ready") && !r.classList.contains("nogl")) m.innerHTML = 'The 3D room needs a moment, or your connection blocked its 3D library. The <a href="#plan" data-go="views">drawn views</a> show every option.'; }}, 20000);</script>"""


def standalone(path=HERE / "room3d_test.html"):
    css = "body{margin:0;background:#fbf6ec;font:15px system-ui}"
    path.write_text(f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                    f'<title>Room in 3D</title>{IMPORTMAP}<style>{css}{CSS}</style></head><body><div class="wrap">{section()}</div></body></html>')
    return path


if __name__ == "__main__":
    print(standalone())
