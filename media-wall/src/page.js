const use = n => (window.claude && window.claude.use) ? window.claude.use(n) : Promise.resolve(null);
const $ = (s, el = document) => el.querySelector(s), $$ = (s, el = document) => [...el.querySelectorAll(s)];
const store = { get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
                set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} } };

/* ---------- pictures borrowed from the viewer's set (each embedded once); each sheet's pictures load when it opens */
function arts(el) { if (el) $$("img[data-art]:not([src])", el).forEach(im => { const u = DATA.img[im.dataset.art]; if (u) im.src = u; }); }
function jumpTo(el) { if (el) requestAnimationFrame(() => el.scrollIntoView({ block: "start", behavior: REDUCED ? "auto" : "smooth" })); }

/* v24: chips for the sections in a long chapter (a sidebar on wide screens) */
$$(".toc").forEach(nav => {
  const hs = $$(".doc h2, .doc h3, .block > h2.ptitle, .block > .qhead > h2.ptitle", nav.parentElement), bs = [];
  nav.parentElement.classList.add("has-toc");                  // v24: a sticky sidebar on wide screens
  hs.forEach((h, i) => {
    const b = document.createElement("button"); b.type = "button"; b.className = "chip" + (h.tagName === "H2" ? " h2" : "");
    b.textContent = h.textContent.replace(/:.*$/, ""); b.addEventListener("click", () => jumpTo(h));
    nav.appendChild(b); bs.push(b);
  });
  if ("IntersectionObserver" in window) {                     // the section you're reading is marked
    const io = new IntersectionObserver(es => { es.forEach(e => { if (e.isIntersecting) { const k = hs.indexOf(e.target); bs.forEach((b, j) => b.classList.toggle("on", j === k)); } }); },
      { root: null, rootMargin: "-80px 0px -70% 0px" });
    hs.forEach(h => io.observe(h));
  }
});
/* ---------- the render viewer */
const NAMES = { card_room: "Farrow & Ball Card Room Green No. 79, the chosen colour", treron: "Farrow & Ball Treron No. 292", sage: "Little Greene Sage Green No. 80", deep: "the deep forest green from earlier versions" };
const VIEWS = { join: "Artisan oak media wall", four: "The alternative: the flip-top open and set for four", six: "The alternative: the flip-top open and set for six, with both spot bars", side: "The PC side wall, seen from the room", drawers: "Every drawer out" };
const view = Object.assign({ style: "join", paint: "card_room", key: false, dims: false }, store.get("mw13-view", {}));
const shot = $("#shot"), cap = $("#cap"), keyBtn = $("#k-key"), dims = $("#dims"), dimsBtn = $("#k-dims");
function draw() {
  if (!VIEWS[view.style]) view.style = "join";
  if (view.style !== "join") view.key = false;
  shot.src = view.key ? DATA.img["key_" + view.style] : DATA.img["art_" + view.style + "_" + view.paint];
  shot.alt = VIEWS[view.style] + (view.key ? " with numbered key" : " in " + NAMES[view.paint]);
  $$("[data-style]").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.style === view.style)));
  $$("[data-paint]").forEach(b => { b.setAttribute("aria-pressed", String(!view.key && b.dataset.paint === view.paint)); b.disabled = view.key; });
  keyBtn.setAttribute("aria-pressed", String(view.key));
  keyBtn.disabled = view.style !== "join";
  dims.src = DATA.img["dims_" + view.style];
  dims.hidden = !view.dims || view.key;
  dimsBtn.setAttribute("aria-pressed", String(view.dims && !view.key));
  dimsBtn.disabled = view.key;
  cap.textContent = view.key
    ? ("Full numbered key for the artisan oak build, in Card Room Green. Game drawer and lower record tray pulled out 30 cm. Dashed lines are hidden: gold for data, audio and low-voltage leads, coral for mains. The numbers are listed in the Media wall tab.")
    : view.style === "six" ? "The flip-top open on its gate leg (110 × 160), still on the wall, set for six (three a side), in " + NAMES[view.paint] + ". The camera stands in line with the alcove's edge so both spot bars show."
    : view.style === "drawers" ? "Every drawer out, in " + NAMES[view.paint] + ": the game drawer and the upper record tray 30 cm out, the hidden plinth drawer 25 cm out. In use, open one record tray at a time."
    : view.style === "side" ? "The PC side wall in " + NAMES[view.paint] + ": the ledge round the corner, the PC on its shelf with the keyboard tray, its leads inside the wall, the sofa below; dashed, the chimney breast's outline and the alcove's depth: 38 of the 46 cm base inside it, 8 proud; the media wall end-on at the right (the breast cut away)."
    : VIEWS[view.style] + ", shown in " + NAMES[view.paint] + ". Evening light, drawn to the measured room.";
  store.set("mw13-view", view);
}
$$("[data-style]").forEach(b => b.addEventListener("click", () => { view.style = b.dataset.style; draw(); }));
$$("[data-paint]").forEach(b => b.addEventListener("click", () => { view.paint = b.dataset.paint; draw(); }));
keyBtn.addEventListener("click", () => { view.key = !view.key; draw(); });
dimsBtn.addEventListener("click", () => { view.dims = !view.dims; draw(); });
draw();

/* ---------- full size (HD) */
const lb = $("#lightbox"), lbImg = $("#lb-img"), lbDims = $("#lb-dims"), lbScroll = $("#lb-scroll");
$("#k-full").addEventListener("click", () => {
  lbImg.src = shot.src; lbImg.alt = shot.alt;
  lbDims.src = dims.src; lbDims.hidden = dims.hidden;
  lb.hidden = false; document.body.style.overflow = "hidden";
  requestAnimationFrame(() => { lbScroll.scrollLeft = (lbScroll.scrollWidth - lbScroll.clientWidth) / 2; lbScroll.scrollTop = (lbScroll.scrollHeight - lbScroll.clientHeight) / 2; });
  $("#lb-close").focus();
});
function closeLb() { lb.hidden = true; document.body.style.overflow = ""; $("#k-full").focus(); }
$("#lb-close").addEventListener("click", closeLb);
document.addEventListener("keydown", e => { if (e.key === "Escape" && !lb.hidden) closeLb(); });
let drag = null;
lbScroll.addEventListener("pointerdown", e => { if (e.pointerType === "mouse") { drag = { x: e.clientX, y: e.clientY, l: lbScroll.scrollLeft, t: lbScroll.scrollTop }; lbScroll.setPointerCapture(e.pointerId); } });
lbScroll.addEventListener("pointermove", e => { if (drag) { lbScroll.scrollLeft = drag.l - (e.clientX - drag.x); lbScroll.scrollTop = drag.t - (e.clientY - drag.y); } });
lbScroll.addEventListener("pointerup", () => { drag = null; });

/* ---------- fit proof filter */
$("#fit-only").addEventListener("click", e => {
  const on = e.currentTarget.getAttribute("aria-pressed") !== "true";
  e.currentTarget.setAttribute("aria-pressed", String(on));
  $("#fit-zones").classList.toggle("fitonly", on);
  $$("#fit-zones details.zone").forEach(d => { if (on && d.querySelector("tr.r-tight, tr.r-check")) d.open = true; });
});

/* ---------- v25: the Plan sheet's opening view, read from the page's own state: three rings, Up next, the build bar */
function ring(id, n, t) { const a = document.getElementById(id), c = a && a.querySelector(".vl"); if (!c) return; const L = 2 * Math.PI * 34; c.style.strokeDasharray = L; c.style.strokeDashoffset = L * (1 - (t ? n / t : 0)); }
function dash() {
  const st = $$(".step"), sd = $$(".step.done"), next = st.find(x => !x.classList.contains("done"));
  $("#d-steps").textContent = sd.length + "/" + st.length; ring("d-steps-bar", sd.length, st.length);
  $$("#segbar i").forEach(i => i.classList.toggle("on", !!document.querySelector("#step-" + i.dataset.s + ".done")));
  const nx = $("#d-next"), nb = $("#d-nextdone");
  if (next) { nx.textContent = $("h3", next).textContent; $("#d-nextn").textContent = next.dataset.s; $("#d-nextmeta").textContent = $(".smeta", next).textContent; nb.hidden = false; nb.dataset.s = next.dataset.s; $("#d-nextgo").dataset.step = next.dataset.s; }
  else { nx.textContent = "Every step done"; $("#d-nextn").textContent = "✓"; $("#d-nextmeta").textContent = "The build is finished: enjoy the room."; nb.hidden = true; }
  const bi = $$("#tracker li[data-kind=buy]"), bd = bi.filter(x => x.classList.contains("done"));
  $("#d-buy").textContent = bd.length + "/" + bi.length; ring("d-buy-bar", bd.length, bi.length);
  const paid = $$("#tracker .paid input").reduce((a, i) => a + (parseFloat(i.value) || 0), 0);
  $("#d-paid").textContent = "\u00a3" + Math.round(paid).toLocaleString("en-GB") + " paid so far";
}
let dashQ = false;
const dashSoon = () => { if (!dashQ) { dashQ = true; requestAnimationFrame(() => { dashQ = false; dash(); }); } };
["#steps-ol", "#tracker"].forEach(s => { const el = $(s); if (el) new MutationObserver(dashSoon).observe(el, { subtree: true, attributes: true, attributeFilter: ["class"] }); });
document.addEventListener("input", dashSoon);
$("#d-nextdone").addEventListener("click", e => { const cb = document.getElementById("sd-" + e.currentTarget.dataset.s); if (cb && !cb.checked && !cb.disabled) { cb.checked = true; cb.dispatchEvent(new Event("change", { bubbles: true })); } });
/* links into the 3D room with its options set */
document.addEventListener("click", e => {
  const b = e.target.closest("[data-r3d]");
  if (!b) return;
  const o = JSON.parse(b.dataset.r3d);
  closeSheets();                 // v25: the room is the home screen
  if (window.R3D) window.dispatchEvent(new CustomEvent("r3d-set", { detail: o })); else window.__r3dPending = o;
});
/* the 3D gallery opens in the full-size viewer */
$$(".g3d").forEach(b => b.addEventListener("click", () => {
  const im = $("img", b);
  lbImg.src = im.src; lbImg.alt = im.alt; lbDims.hidden = true;
  lb.hidden = false; document.body.style.overflow = "hidden"; $("#lb-close").focus();
}));

/* ---------- shared state: tracker, build steps (v30: the questions and their answers are gone) */
let db = null, user = null, myId = null, readOnly = false;
const tstate = {};            // tracker/<id> bodies as saved
const sstate = {};            // steps/<n> bodies as saved
const chains = {};            // one write at a time per document
function write(path, body) {
  const run = () => db.doc(path).set(body);
  chains[path] = (chains[path] || Promise.resolve()).then(run, run);
  return chains[path];
}
function onWriteError(e, stEl) {
  if (e && e.code === "invalid_argument") { readOnly = true; lockInputs(); }
  if (stEl) { stEl.textContent = e && e.code === "quota_exceeded" ? "The page's storage is full; tell Claude." : "Couldn't save. Try again in a moment."; stEl.className = "st err"; }
}
function lockInputs() { $$(".items input, .sdone input").forEach(el => el.disabled = true); }

$("#copy-cuts").addEventListener("click", async () => {
  const box = $("#cuts-box"), st = $("#cuts-st");
  try { await navigator.clipboard.writeText(box.value); st.textContent = "Copied. Paste it into an email to the timber merchant."; box.hidden = true; }
  catch (e) { box.hidden = false; box.focus(); box.select(); st.textContent = "Select the text below and copy it."; }
});

/* tracker and the cost chart */
const local = store.get("mw12-tracker", {});
const money = v => "£" + (Math.round(v * 100) / 100).toLocaleString(undefined, { minimumFractionDigits: v % 1 ? 2 : 0, maximumFractionDigits: 2 });
function tget(id) { return (db ? tstate[id] : local[id]) || null; }
function paintTracker() {
  let done = 0, paid = 0, leftLo = 0, leftHi = 0;
  const phPaid = {};
  DATA.track.forEach(r => {
    const s = tget(r.id), isDone = s ? !!s.done : r.done;
    const li = document.querySelector('[data-t="' + r.id + '"]'), cb = li.querySelector("input[type=checkbox]"), pd = li.querySelector("input[type=number]");
    cb.checked = isDone; li.classList.toggle("done", isDone);
    if (pd && document.activeElement !== pd) pd.value = s && typeof s.paid === "number" ? s.paid : "";
    if (isDone) done++; else { leftLo += r.lo; leftHi += r.hi; }
    if (s && typeof s.paid === "number") { paid += s.paid; phPaid[r.phase] = (phPaid[r.phase] || 0) + s.paid; }
  });
  $$("details.phase").forEach(d => {
    const lis = $$(".items li", d), n = lis.filter(li => li.classList.contains("done")).length;
    $(".pd", d).textContent = n + " of " + lis.length + " done";
  });
  DATA.phases.forEach(p => {
    const row = document.querySelector('.crow[data-ph="' + p.idx + '"]'), v = phPaid[p.name] || 0;
    $(".cpaid", row).style.width = Math.min(100, 100 * v / DATA.top) + "%";
    $(".cpv", row).textContent = v ? "paid " + money(v) : "";
  });
  $("#t-done").textContent = done + " of " + DATA.track.length;
  $("#t-paid").textContent = money(paid);
  $("#t-left").textContent = leftHi ? money(leftLo) + "–" + money(leftHi).slice(1) : "£0";
}
function saveTrack(id, patch) {
  const r = DATA.track.find(x => x.id === id);
  const cur = tget(id) || { done: r.done, paid: null };
  const body = Object.assign({}, cur, patch);
  if (!db) { local[id] = body; store.set("mw12-tracker", local); paintTracker(); return; }
  body.by = myId; body.at = new Date().toISOString();
  tstate[id] = body; paintTracker();
  write("tracker/" + id, body).catch(e => onWriteError(e, null));
}
DATA.track.forEach(r => {
  const li = document.querySelector('[data-t="' + r.id + '"]');
  li.querySelector("input[type=checkbox]").addEventListener("change", e => saveTrack(r.id, { done: e.target.checked }));
  const pd = li.querySelector("input[type=number]");
  if (pd) pd.addEventListener("change", e => {
    const v = e.target.value === "" ? null : Math.max(0, Math.round(parseFloat(e.target.value) * 100) / 100);
    saveTrack(r.id, { paid: Number.isFinite(v) ? v : null });
  });
});
$$("[data-filter]").forEach(b => b.addEventListener("click", () => {
  $$("[data-filter]").forEach(x => x.setAttribute("aria-pressed", String(x === b)));
  const t = $("#tracker");
  t.classList.toggle("f-left", b.dataset.filter === "left");
  t.classList.toggle("f-jobs", b.dataset.filter === "jobs");
  if (b.dataset.filter !== "all") $$("details.phase", t).forEach(d => d.open = true);
}));
paintTracker();

/* build steps */
const slocal = store.get("mw13-steps", {});
function sget(n) { return (db ? sstate["s" + n] : slocal["s" + n]) || null; }
function paintSteps() {
  let done = 0;
  $$(".step").forEach(li => {
    const s = sget(li.dataset.s), on = !!(s && s.done), cb = $(".sdone input", li);
    cb.checked = on; li.classList.toggle("done", on);
    if (on) done++;
  });
  $("#s-count").textContent = done + " of " + DATA.steps + " steps done";
  $("#s-bar").style.width = (100 * done / DATA.steps) + "%";
}
$$(".step").forEach(li => {
  $(".sdone input", li).addEventListener("change", e => {
    const body = { done: e.target.checked };
    if (!db) { slocal["s" + li.dataset.s] = body; store.set("mw13-steps", slocal); paintSteps(); return; }
    body.by = myId; body.at = new Date().toISOString();
    sstate["s" + li.dataset.s] = body; paintSteps();
    write("steps/s" + li.dataset.s, body).catch(err => onWriteError(err, null));
  });
});
paintSteps();

/* light up what this view can do */
(async () => {
  const [d, u] = await Promise.all([use("db"), use("user")]);
  user = u;
  if (!d) {
    $("#t-note").textContent = "Each phase says which build step it's needed for. Ticks and amounts are kept on this device only from this view.";
    $("#s-note").textContent = "Tick each step when it's done; from this view the ticks are kept on this device only.";
    return;
  }
  db = d;
  try { myId = u ? await u.id() : null; } catch (e) { myId = null; }
  let canWrite = null;
  try { canWrite = u ? await u.can("data.write") : null; } catch (e) {}
  if (canWrite === false) { readOnly = true; lockInputs(); }
  db.collection("tracker").onSnapshot(snap => {
    snap.docChanges().forEach(ch => { if (ch.type === "removed") delete tstate[ch.doc.id]; else tstate[ch.doc.id] = ch.doc.data(); });
    paintTracker();
  }, () => {});
  db.collection("steps").onSnapshot(snap => {
    snap.docChanges().forEach(ch => { if (ch.type === "removed") delete sstate[ch.doc.id]; else sstate[ch.doc.id] = ch.doc.data(); });
    paintSteps();
  }, () => {});
})();
(() => {
  // v13.7: lighting scene buttons
  const sb = document.getElementById("scene-btns");
  if (!sb) return;
  sb.addEventListener("click", e => {
    const b = e.target.closest("button[data-scene]"); if (!b) return;
    sb.querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", String(x === b)));
    document.querySelectorAll(".scene").forEach(d => { d.hidden = d.dataset.sc !== b.dataset.scene; });
  });
})();
(() => {
  // v13.6: show one part of the build at a time
  const bar = document.getElementById("part-filter");
  if (!bar) return;
  const note = document.getElementById("pf-note");
  const pick = part => {
    bar.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.part === part)));
    let shown = 0;
    document.querySelectorAll(".steps-list > li.step").forEach(li => {
      const on = !part || li.dataset.parts.split("|").includes(part);
      li.hidden = !on; if (on) shown++;
    });
    note.textContent = part ? ("Showing " + shown + " of " + DATA.steps + " steps: " + part + ".") : "";
    try { localStorage.setItem("mw-part", part); } catch (e) {}
  };
  bar.addEventListener("click", e => { const b = e.target.closest("button[data-part]"); if (b) pick(b.dataset.part); });
  document.addEventListener("click", e => {
    const a = e.target.closest("[data-step]");
    if (a) { const li = document.getElementById("step-" + a.dataset.step); if (li && li.hidden) pick(""); }
  }, true);
  let saved = "";
  try { saved = localStorage.getItem("mw-part") || ""; } catch (e) {}
  if (saved && bar.querySelector('button[data-part="' + saved.replace(/"/g, "") + '"]')) pick(saved);
})();

/* ---------- v25: the celebration: a dark pill toast, and an 18-dot confetti burst (no burst, and no springs, with reduced motion) */
const toastEl = document.getElementById("toast"), DOTS = [50, 165, 300, 95, 235, 345, 25, 70, 125];
let toastT = 0;
function cheer(msg, from) {
  toastEl.textContent = msg; toastEl.classList.add("on"); clearTimeout(toastT); toastT = setTimeout(() => toastEl.classList.remove("on"), 2200);
  if (REDUCED) return;
  const r = from && from.getBoundingClientRect ? from.getBoundingClientRect() : { left: innerWidth / 2, top: innerHeight - 140, width: 0, height: 0 };
  const box = document.createElement("div"); box.className = "confetti"; box.setAttribute("aria-hidden", "true");
  box.style.left = (r.left + r.width / 2) + "px"; box.style.top = (r.top + r.height / 2) + "px";
  for (let i = 0; i < 18; i++) { const d = document.createElement("i"), a = (i / 18) * Math.PI * 2, R = 60 + Math.random() * 70;
    d.style.background = `oklch(0.78 0.14 ${DOTS[i % DOTS.length]})`; d.style.setProperty("--dx", Math.cos(a) * R + "px"); d.style.setProperty("--dy", Math.sin(a) * R - 30 + "px"); box.appendChild(d); }
  document.body.appendChild(box); setTimeout(() => box.remove(), 1000);
}
document.addEventListener("change", e => {
  const t = e.target; if (t.type !== "checkbox" || !t.checked) return;
  const step = t.closest(".step");
  if (step && t.closest(".sdone")) { const left = $$(".step").filter(s => !s.classList.contains("done") && s !== step).length;
    cheer(left ? `Step ${step.dataset.s} done! ${left} to go` : "Every step done!", t); return; }
  if (t.closest("#tracker")) cheer("Ticked off!", t);
});

/* v32: the cost overview: copy it as a shopping list, open every piece */
document.addEventListener("click", e => {
  const b = e.target.closest("#co-copy, #co-all"); if (!b) return;
  if (b.id === "co-all") { const all = $$(".cpiece"), open = all.some(d => !d.open); all.forEach(d => d.open = open); b.textContent = open ? "Close them all" : "Open them all"; return; }
  const t = $("#co-text").value, st = $("#co-st"), done = () => { st.textContent = "Copied: paste it into a note or a message."; };
  if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(done, () => { prompt("Copy the list:", t); });
  else prompt("Copy the list:", t);
});
