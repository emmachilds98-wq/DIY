/* v14: the room in 3D. The furniture is the plan's own geometry (export3d.py records every box, polygon and face frame the
   HD renderer draws); the shell, the lights, the TV picture, shelf B and the floor lamp are built here from the same numbers.
   Room coordinates are cm: x from the side (east) wall, y up, z from the room (negative) to the alcove's back. Three.js uses
   metres with x mirrored so the picture isn't flipped. */
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { RectAreaLightUniformsLib } from "three/addons/lights/RectAreaLightUniformsLib.js";
import { mergeGeometries } from "three/addons/utils/BufferGeometryUtils.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";

const root = document.getElementById("r3d");
const SC = JSON.parse(document.getElementById("scene3d-data").textContent);
const R = SC.room;
const M = 0.01;
const v3 = (x, y, z) => new THREE.Vector3(-x * M, y * M, z * M);
const qs = s => root.querySelector(s), qsa = s => [...root.querySelectorAll(s)];
const msg = qs("#r3d-msg");

const store = { get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
                set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} } };
const SMALL = window.matchMedia && matchMedia("(pointer: coarse), (max-width: 700px)").matches;   // phones and tablets start on Fast
const WARM = "#ffe2b8";
const DEF = { site: "C", dining: "folded",   // v27: the dining cabinet is the plan
              scene: "bright", tod: "evening", paint: "card_room", custom: "#899081", lamp: "corner", drawers: false,
              quality: SMALL ? "fast" : "hd", view: "room",   // v21: the whole room first
              // v15: every light on a slider (the scenes fill them in), the smart bars and the lamp in any colour, ceiling and skirting paints
              lv: null, master: 100, col: { strips: WARM, bar1: WARM, bar2: WARM, lamp0: R.LAMP_RGB[0], lamp1: R.LAMP_RGB[1], lamp2: R.LAMP_RGB[2] },
              ceil: "match", skirt: "match", laser: false, lbox: true, curtains: false, pc: true, ideas: {},   // v17: ideas all off
              // v18: the plant stand and the record shelf's layout, your own moves (edit mode) and the things you've added; the grow lights
              plants: "corner", layout: {}, added: [], grow: true,
              chairs: "cupboard",   // v20: the chair cupboard beside the table (doors shut); "open", "hooks" or "away" (the garage)
              // v20, client: "give more decor variation and options": the rug, sofa cushions, the curtains, what's in the glass case and its frame
              decor: { rug: "yours", cushions: "none", curtains: "hessian", fill: "collect", frame: "oak", oak: "artisan", floor: "carpet", shelf: "black", pads: "olive" },   // v26: the oak, the floor, your shelf; v31: the seat pads
              sugg: {},     // v21: the suggested furniture and decor, all off
              seat: "off",
              cab: "compact", tdoor: false,
              cam: "orbit", pad: false, foot: false, beside: "clear" };   // v31: what's beside the compact cabinet   // v31: a drag circles round a spot or looks round from where you stand; the move buttons on the room   // v30: the compact cabinet (the plan) or the sliding one; the table door open with the table folded   // v23: the fold-down seat at the stair end (an option): "off", "up" (folded) or "down"   // v20: the chair cupboard beside the table (doors shut); "open", "hooks" or "away" (the garage)
DEF.lamp = R.LAMP_DEFAULT || "sofa";   // v18: the window corner holds the plant stand or the record shelf   // v16: the table by the stairs by default; the laser off
const KEY = "mw18-3d";
const S = Object.assign({}, DEF, store.get(KEY, {}));
S.col = Object.assign({}, DEF.col, S.col || {});
if (!S.ideas || typeof S.ideas !== "object") S.ideas = {};
if (!S.sugg || typeof S.sugg !== "object") S.sugg = {};
if (!S.svar || typeof S.svar !== "object" || Array.isArray(S.svar)) S.svar = {};   // v28: each suggestion's version (its first by default)
S.decor = Object.assign({}, DEF.decor, (S.decor && typeof S.decor === "object") ? S.decor : {});
if (!S.layout || typeof S.layout !== "object" || Array.isArray(S.layout)) S.layout = {};
if (!Array.isArray(S.added)) S.added = [];
if (!(S.plants in R.PLANT_LAYOUTS)) S.plants = DEF.plants;
S.edit = false;
if (!S.seen21) { S.view = "room"; S.seen21 = true; }   // v21: everyone starts once on the new whole-room view
if (!S.seen27) { if (S.site === "B") S.site = "C"; S.seen27 = true; }   // v27: the dining cabinet is the plan now: the old default moves to it once
if (S.dining === "eight") S.dining = "six";                              // v27: the cabinet seats six (v26 had eight)
if (!(S.paint in R.PAINTS) && S.paint !== "custom") S.paint = DEF.paint;

/* ---------------------------------------------------------------- the lighting presets (scenes.py) and their two rules
   v25: three presets (bright, cosy, film); dinner is a rule (the table open lifts bar 2), daytime a switch (S.tod) that works with any
   preset. Saved choices from the old six buttons map across once. */
const SCENES = JSON.parse(document.getElementById("scenes-data").textContent);
const LIGHT_RULES = JSON.parse((document.getElementById("lightrules-data") || {}).textContent || '{"boost":{"bar2_min":80,"bar1_max":15,"bias":0},"old":{}}');
const OLD_SCENE = LIGHT_RULES.old || {};
function oldScene(o) {               // an old scene key in o (saved state, a link, a still) becomes a preset, with daytime as a switch
  if (o.scene && !(o.scene in SCENES) && o.scene in OLD_SCENE) { if (o.scene === "day") o.tod = "day"; o.scene = OLD_SCENE[o.scene]; if (o === S) S.lv = null; }
  return o;
}
oldScene(S);
if (!(S.scene in SCENES)) S.scene = DEF.scene;
if (S.tod !== "day") S.tod = "evening";
const LAYERS = ["strip", "uprights", "bias", "bar1", "bar2", "lamp"];
if (!S.lv) S.lv = Object.assign({}, SCENES[S.scene].levels);
const tableOpen = () => S.dining && S.dining !== "folded";
function lvl(k) {                     // a layer's level: the slider, the table rule when the flip-top is open, then the master slider
  let v = S.lv[k] ?? 0;
  if (tableOpen()) { const B = LIGHT_RULES.boost; if (k === "bar2") v = Math.max(v, B.bar2_min); else if (k === "bar1") v = Math.min(v, B.bar1_max); else if (k === "bias") v = B.bias; }
  return Math.max(0, Math.min(100, v * S.master / 100));
}

/* ---------------------------------------------------------------- renderer */
let canvas = qs("canvas");
let gl;
try {
  gl = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: "high-performance" });
} catch (e) {
  root.classList.add("nogl");
  msg.innerHTML = 'Your browser can’t show the 3D room here (no WebGL). The <a href="#views" data-go="views">drawn views</a> show every option.';
  throw e;
}
gl.outputColorSpace = THREE.SRGBColorSpace;
gl.toneMapping = THREE.ACESFilmicToneMapping;
gl.shadowMap.type = THREE.PCFShadowMap;   // v14.1: PCF while you look round; the saved HD pictures use soft shadows
gl.shadowMap.autoUpdate = false;          // v14.1: shadows don't move with the camera, so they're redrawn only when the room changes
const reshadow = () => { gl.shadowMap.needsUpdate = true; };
RectAreaLightUniformsLib.init();

const scene = new THREE.Scene();
scene.background = new THREE.Color("#0d100e");
const camera = new THREE.PerspectiveCamera(50, 16 / 9, 0.05, 60);
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.dampingFactor = 0.09;
controls.maxDistance = 6;          // v17: 6 m inside the room (the views from above lift it), never closer than 30 cm
controls.minDistance = 0.3;
controls.screenSpacePanning = false;   // v17: a right-drag slides along the floor
// v31, client: "make camera movement easier ... sometimes the movement is quite uncontrollable": it stops soon after you let go,
// and a drag, a pinch or a scroll moves it about half as far
controls.dampingFactor = 0.2;
controls.rotateSpeed = 0.55; controls.zoomSpeed = 0.6; controls.panSpeed = 0.6;
controls.addEventListener("change", () => { dirty(); if (typeof syncEye === "function") syncEye(); });

/* ---------------------------------------------------------------- textures, made here so nothing loads */
function canvasTex(w, h, draw, srgb = true) {
  const c = document.createElement("canvas"); c.width = w; c.height = h;
  draw(c.getContext("2d"), w, h);
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  if (srgb) t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = Math.min(8, gl.capabilities.getMaxAnisotropy());
  return t;
}
function rnd(seed) { return () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }; }
/* oak: long streaks along u, with a few cathedral arcs and pores; drawn near white so it tints by the part's colour */
const OAK_TEX = canvasTex(1024, 512, (g, w, h) => {
  const r = rnd(11);
  g.fillStyle = "#e9e1d6"; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 420; i++) {
    const y = r() * h, a = 0.05 + r() * 0.12, th = 0.6 + r() * 2.6;
    g.strokeStyle = r() < 0.75 ? `rgba(92,58,28,${a})` : `rgba(255,248,235,${a})`;
    g.lineWidth = th; g.beginPath(); g.moveTo(0, y);
    for (let x = 0; x <= w; x += 32) g.lineTo(x, y + Math.sin(x / (90 + r() * 60) + i) * (1 + r() * 2.5));
    g.stroke();
  }
  for (let k = 0; k < 7; k++) {          // cathedral figure
    const cx = r() * w, cy = r() * h, s = 40 + r() * 80;
    for (let j = 0; j < 9; j++) {
      g.strokeStyle = `rgba(110,70,35,${0.05 + r() * 0.07})`; g.lineWidth = 1.2;
      g.beginPath(); g.ellipse(cx, cy, s * 3 + j * 14, s * 0.35 + j * 5, 0, 0, Math.PI * 2); g.stroke();
    }
  }
  for (let i = 0; i < 2600; i++) { g.fillStyle = `rgba(70,40,15,${0.08 + r() * 0.12})`; g.fillRect(r() * w, r() * h, 2 + r() * 5, 0.8); }
});
const OAK_TEX_V = (() => { const tx = OAK_TEX.clone(); tx.rotation = Math.PI / 2; tx.center.set(0.5, 0.5); tx.needsUpdate = true; return tx; })();   // v29: upright grain, for tall doors

const OAK_BUMP = canvasTex(512, 256, (g, w, h) => {
  const r = rnd(5);
  g.fillStyle = "#808080"; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 900; i++) { g.fillStyle = `rgba(0,0,0,${0.1 + r() * 0.2})`; g.fillRect(r() * w, r() * h, 3 + r() * 9, 0.7); }
}, false);
const CARPET = canvasTex(512, 512, (g, w, h) => {   // v15: "soft grey carpet": a cool grey with a soft, fine pile
  const r = rnd(3);
  g.fillStyle = R.CARPET; g.fillRect(0, 0, w, h);
  const im = g.getImageData(0, 0, w, h), d = im.data;
  for (let i = 0; i < d.length; i += 4) { const n = (r() - 0.5) * 22; d[i] += n; d[i + 1] += n; d[i + 2] += n * 1.04; }
  g.putImageData(im, 0, 0);
});
CARPET.repeat.set(7, 7);
/* v26: Look's floors: an oatmeal carpet and oak boards, besides your grey carpet */
const OATMEAL = canvasTex(512, 512, (g, w, h) => {
  const r = rnd(5); g.fillStyle = "#cdbfa8"; g.fillRect(0, 0, w, h);
  const im = g.getImageData(0, 0, w, h), d = im.data;
  for (let i = 0; i < d.length; i += 4) { const n = (r() - 0.5) * 26; d[i] += n; d[i + 1] += n * 0.95; d[i + 2] += n * 0.85; }
  g.putImageData(im, 0, 0);
});
OATMEAL.repeat.set(7, 7);
const BOARDS = canvasTex(1024, 1024, (g, w, h) => {   // 14 cm boards, staggered joints, a little colour from board to board
  const r = rnd(12), bw = w / 8;
  for (let i = 0; i < 8; i++) {
    let y = -r() * h;
    while (y < h) { const len = h * (0.35 + r() * 0.4), t = r();
      g.fillStyle = `rgb(${152 + t * 30},${104 + t * 22},${64 + t * 16})`; g.fillRect(i * bw + 1, y + 1, bw - 2, len - 2);
      g.globalAlpha = 0.12; for (let k = 0; k < 9; k++) { g.fillStyle = r() < 0.5 ? "#7a5232" : "#e8c79c"; g.fillRect(i * bw + 2 + r() * (bw - 6), y, 1 + r() * 2, len); } g.globalAlpha = 1;
      y += len; }
  }
});
BOARDS.repeat.set(3.4, 2.5);
const PILE = canvasTex(256, 256, (g, w, h) => {      // the carpet's pile, for its bump
  const r = rnd(8); const im = g.createImageData(w, h), d = im.data;
  for (let i = 0; i < d.length; i += 4) { const n = 110 + r() * 40; d[i] = d[i + 1] = d[i + 2] = n; d[i + 3] = 255; }
  g.putImageData(im, 0, 0);
}, false);
PILE.repeat.set(14, 14);
const CORD = canvasTex(64, 256, (g, w, h) => {      // v15: the sofa's corduroy: soft vertical ribs
  for (let x = 0; x < w; x++) { const v = 128 + 70 * Math.cos(x / w * Math.PI * 2 * 4); g.fillStyle = `rgb(${v},${v},${v})`; g.fillRect(x, 0, 1, h); }
}, false);
CORD.repeat.set(36, 1);
/* v15: "a nice design rug that fits": cream ground, a deep blue border, big mid-century arches in rust, ochre and sage, a row of dots */
const RUG_TEX = canvasTex(1150, 800, (g, w, h) => {
  const [cream, rust, ochre, blue, sage] = R.RUG.cols, k = w / (R.RUG.x[1] - R.RUG.x[0]), b = R.RUG.border * k;
  g.fillStyle = blue; g.fillRect(0, 0, w, h);
  g.fillStyle = cream; g.fillRect(b, b, w - 2 * b, h - 2 * b);
  g.strokeStyle = ochre; g.lineWidth = 3; g.strokeRect(b + 14, b + 14, w - 2 * b - 28, h - 2 * b - 28);
  g.save(); g.beginPath(); g.rect(b, b, w - 2 * b, h - 2 * b); g.clip();
  const base = h - b - 90;
  for (const [cx, r, col] of [[0.27, 230, rust], [0.56, 290, ochre], [0.75, 200, sage], [0.49, 150, blue]]) {
    g.strokeStyle = col; g.lineCap = "butt";
    g.lineWidth = 44; g.beginPath(); g.arc(cx * w, base, r, Math.PI, 0); g.stroke();
    g.lineWidth = 18; g.beginPath(); g.arc(cx * w, base, r - 75, Math.PI, 0); g.stroke();
  }
  g.fillStyle = rust; g.fillRect(b + 30, base + 40, w - 2 * b - 60, 14);
  g.fillStyle = ochre; for (let i = 0; i < 9; i++) { g.beginPath(); g.arc(b + 90 + i * (w - 2 * b - 180) / 8, b + 120, 14, 0, Math.PI * 2); g.fill(); }
  g.restore();
  const r = rnd(21), im = g.getImageData(0, 0, w, h), d = im.data;   // wool: a little noise
  for (let i = 0; i < d.length; i += 4) { const n = (r() - 0.5) * 18; d[i] += n; d[i + 1] += n; d[i + 2] += n; }
  g.putImageData(im, 0, 0);
});
RUG_TEX.wrapS = RUG_TEX.wrapT = THREE.ClampToEdgeWrapping;
/* v20: other rugs to try (Decor), drawn when first picked: a flatweave jute, a deep blue with a cream border, sage and cream stripes */
const RUG_LOOKS = {
  jute: { edge: "#8f7650", draw(g, w, h) {
    g.fillStyle = "#b89a6c"; g.fillRect(0, 0, w, h);
    const r = rnd(33);
    for (let y = 0; y < h; y += 6) { g.fillStyle = `rgba(${90 + r() * 40},${70 + r() * 30},${40 + r() * 20},0.35)`; g.fillRect(0, y, w, 3); }
    for (let x = 0; x < w; x += 6) { g.fillStyle = "rgba(240,225,190,0.12)"; g.fillRect(x, 0, 2, h); }
    g.strokeStyle = "#8f7650"; g.lineWidth = 26; g.strokeRect(13, 13, w - 26, h - 26); } },
  blue: { edge: "#22385a", draw(g, w, h) {
    g.fillStyle = "#2a4266"; g.fillRect(0, 0, w, h);
    g.strokeStyle = "#e9e0cc"; g.lineWidth = 10; g.strokeRect(40, 40, w - 80, h - 80); g.lineWidth = 3; g.strokeRect(62, 62, w - 124, h - 124);
    g.strokeStyle = "rgba(233,224,204,0.35)"; g.lineWidth = 3;
    for (let x = 140; x < w - 120; x += 90) for (let y = 140; y < h - 120; y += 90) { g.beginPath(); g.moveTo(x, y - 18); g.lineTo(x + 18, y); g.lineTo(x, y + 18); g.lineTo(x - 18, y); g.closePath(); g.stroke(); } } },
  stripes: { edge: "#5f6f52", draw(g, w, h) {
    g.fillStyle = "#ece4d2"; g.fillRect(0, 0, w, h);
    const band = [["#66775a", 95], ["#ece4d2", 28], ["#c7643a", 12], ["#ece4d2", 28], ["#66775a", 40], ["#ece4d2", 44]];
    let x = 0; while (x < w) for (const [c, bw] of band) { g.fillStyle = c; g.fillRect(x, 0, bw, h); x += bw; }
    g.fillStyle = "#5f6f52"; g.fillRect(0, 0, w, 16); g.fillRect(0, h - 16, w, 16); } },
};
function rugTex(k) {
  const L = RUG_LOOKS[k]; if (!L) return RUG_TEX;
  if (!L.tex) {
    L.tex = canvasTex(1150, 800, (g, w, h) => { L.draw(g, w, h);
      const r = rnd(22), im = g.getImageData(0, 0, w, h), d = im.data;
      for (let i = 0; i < d.length; i += 4) { const n = (r() - 0.5) * 16; d[i] += n; d[i + 1] += n; d[i + 2] += n; }
      g.putImageData(im, 0, 0); });
    L.tex.wrapS = L.tex.wrapT = THREE.ClampToEdgeWrapping;
  }
  return L.tex;
}
const WALL_BUMP = canvasTex(256, 256, (g, w, h) => {
  const r = rnd(9); const im = g.createImageData(w, h), d = im.data;
  for (let i = 0; i < d.length; i += 4) { const n = 120 + r() * 20; d[i] = d[i + 1] = d[i + 2] = n; d[i + 3] = 255; }
  g.putImageData(im, 0, 0);
}, false);
WALL_BUMP.repeat.set(6, 6);
const SCREEN_TEX = canvasTex(1024, 576, (g, w, h) => {   // the TV's picture: the same dusk as the drawn renders
  const sky = g.createLinearGradient(0, 0, 0, h);
  [["#1b1638", 0], ["#4a2d5e", 0.45], ["#c0566a", 0.72], ["#f2a65e", 0.88], ["#f6c97c", 1]].forEach(([c, o]) => sky.addColorStop(o, c));
  g.fillStyle = sky; g.fillRect(0, 0, w, h);
  const sun = g.createRadialGradient(w * 0.62, h * 0.69, 0, w * 0.62, h * 0.69, w * 0.22);
  sun.addColorStop(0, "rgba(255,242,196,1)"); sun.addColorStop(0.35, "rgba(255,214,138,0.7)"); sun.addColorStop(1, "rgba(255,176,112,0)");
  g.fillStyle = sun; g.fillRect(0, 0, w, h);
  const hills = [["#3a2550", [0, 44, 10, 36, 19, 41, 30, 30, 41, 39, 52, 33, 60, 38, 71, 28, 82, 37, 92, 32, 100, 36]],
                 ["#24183a", [0, 49, 12, 43, 25, 47, 38, 41, 50, 46, 63, 42, 76, 48, 88, 43, 100, 47]],
                 ["#150f24", [0, 53, 20, 50, 40, 53, 58, 50, 80, 54, 100, 51]]];
  for (const [c, p] of hills) {
    g.fillStyle = c; g.beginPath(); g.moveTo(0, h);
    for (let i = 0; i < p.length; i += 2) g.lineTo(p[i] / 100 * w, p[i + 1] / 57.6 * h);
    g.lineTo(w, h); g.closePath(); g.fill();
  }
});
const ART_TEX = canvasTex(256, 256, (g, w, h) => {
  const gr = g.createLinearGradient(0, 0, w, h);
  gr.addColorStop(0, "#e9b44c"); gr.addColorStop(0.5, "#e2683c"); gr.addColorStop(1, "#7a2e5a");
  g.fillStyle = gr; g.fillRect(0, 0, w, h);
});
const HESSIAN = canvasTex(256, 256, (g, w, h) => {   // v15: hessian's coarse, open weave
  const r = rnd(31);
  g.fillStyle = "#cfc4ae"; g.fillRect(0, 0, w, h);
  for (let i = 0; i < w; i += 4) { g.fillStyle = `rgba(90,70,40,${0.12 + r() * 0.14})`; g.fillRect(i, 0, 1.6, h); }
  for (let j = 0; j < h; j += 4) { g.fillStyle = `rgba(255,248,230,${0.08 + r() * 0.12})`; g.fillRect(0, j, w, 1.4); }
}, true);
HESSIAN.repeat.set(3, 9);
// v16: the client's light box is an IKEA OBEGRÄNSAD: a black panel with a 16 x 16 grid of white LEDs that shows blocky black-and-white
// pictures, "like pharmacy LED ads". Drawn showing a pixel music note; the unlit LEDs are dark grey dots on the black face.
// v16: the navy cap's poem, printed in pale lines under its peak
const POEM_TEX = canvasTex(256, 140, (g, w, h) => {
  g.fillStyle = "#1f2a44"; g.fillRect(0, 0, w, h);
  g.fillStyle = "#d9d2b8";
  for (let i = 0; i < 9; i++) { const lw = 150 + ((i * 37) % 70); g.fillRect((w - lw) / 2, 12 + i * 13, lw, 4); }
});
const NOTE = ["................", "......#######...", "......#######...", "......##....#...", "......#.....#...", "......#.....#...",
              "......#.....#...", "......#.....#...", "......#.....#...", "..####....####..", ".######..######.", ".######..######.",
              "..####....####..", "................", "................", "................"];
const LBOX_TEX = canvasTex(416, 416, (g, w, h) => {
  g.fillStyle = "#0b0b0c"; g.fillRect(0, 0, w, h);
  const n = 16, c = w / n;
  for (let r = 0; r < n; r++) for (let k = 0; k < n; k++) {
    const on = NOTE[r][k] === "#";
    if (on) { g.fillStyle = "rgba(255,255,255,0.16)"; g.beginPath(); g.arc((k + 0.5) * c, (r + 0.5) * c, c * 0.62, 0, 7); g.fill(); }
    g.fillStyle = on ? "#ffffff" : "#26262a"; g.beginPath(); g.arc((k + 0.5) * c, (r + 0.5) * c, c * 0.3, 0, 7); g.fill();
  }
});
function skyTex(day) {
  return canvasTex(512, 256, (g, w, h) => {
    const s = g.createLinearGradient(0, 0, 0, h);
    if (day) { s.addColorStop(0, "#c9d9e8"); s.addColorStop(0.7, "#e8eef2"); s.addColorStop(1, "#b8c2b4"); }
    else { s.addColorStop(0, "#0a1024"); s.addColorStop(0.75, "#1a2240"); s.addColorStop(1, "#2b2a35"); }
    g.fillStyle = s; g.fillRect(0, 0, w, h);
    g.fillStyle = day ? "#9aa596" : "#141418";               // the houses opposite
    for (let x = 0; x < w; x += 70) g.fillRect(x, h * 0.62 + (x % 140 ? 8 : 0), 62, h);
    if (!day) { g.fillStyle = "#f5c46a"; for (let x = 18; x < w; x += 70) if (x % 3) g.fillRect(x, h * 0.72, 10, 8); }
  });
}
const SKY = { day: skyTex(true), night: skyTex(false) };

/* ---------------------------------------------------------------- materials */
const MATS = [];
/* v21: the dolls'-house cutaway. From outside the room (the views from above), whatever stands along the wall nearest the camera (curtains,
   the window frame, the plant stand, the stairs) is cut off above CUT_H, like a section drawing, so nothing blocks the room. Every material
   carries the same two planes; clipIntersection cuts only where both agree (near that wall AND above CUT_H); updateCut() moves plane 0. */
const CUT_H = 95, CUT_IN = 32;
const CLIP = [new THREE.Plane(new THREE.Vector3(0, 0, 1), 1e3), new THREE.Plane(new THREE.Vector3(0, -1, 0), CUT_H * 0.01)];
const clipMat = m => { m.clippingPlanes = CLIP; m.clipIntersection = true; m.clipShadows = true; return m; };
const reg = m => (MATS.push(clipMat(m)), m);
const OAKS = new Set(["#c48c57", "#d9a46c", "#9c6a3f", "#a87443", "#cfa575", "#ddb78a", "#b08756", "#c79a6b", "#d8ad80", "#a37a50",
  "#b07a46", "#c89060", "#8a5c33", "#c08a52", "#c9a26a", "#c79a63", "#a8834f", "#d8c39f", "#e6d2ae", "#b99e78", "#cdb38a", "#d9c09a"]);
const PAINT_OLD = new Set(R.PAINT_OLD);
const lum = h => { const c = new THREE.Color(h); const o = {}; c.getHSL(o); return o.l; };
const BASE_L = lum(R.PAINT_BASE);
const paintMats = new Map();
function paintHex() { return S.paint === "custom" ? S.custom : R.PAINTS[S.paint].hex; }
/* v15: three paints: the walls, the ceiling, and the skirting with the door, its frame and the radiator ("match" = the walls' colour) */
function chHex(ch) {
  if (ch === "ceil" && S.ceil !== "match") return S.ceil;
  if (ch === "trim" && S.skirt !== "match") return S.skirt;
  return paintHex();
}
function paintColour(ratio, ch = "wall") {
  const c = new THREE.Color(chHex(ch)); const o = {}; c.getHSL(o);
  return new THREE.Color().setHSL(o.h, o.s, Math.min(0.94, o.l * Math.pow(ratio, 0.6)));
}
function paintMat(ratio, eggshell, both, ch = "wall") {
  const k = ratio.toFixed(2) + (eggshell ? "e" : "") + (both ? "d" : "") + ch;
  if (!paintMats.has(k)) paintMats.set(k, reg(new THREE.MeshStandardMaterial({ color: paintColour(ratio, ch), roughness: eggshell ? 0.45 : 0.92,
    bumpMap: eggshell ? null : WALL_BUMP, bumpScale: 0.6, side: both ? THREE.DoubleSide : THREE.FrontSide, userData: { ratio, ch } })));
  return paintMats.get(k);
}
function repaint() { paintMats.forEach(m => m.color.copy(paintColour(m.userData.ratio, m.userData.ch))); reshadow(); }
const KIND = {};
/* v23: the stairs' side wall is brick (client): 0.6 m a repeat (GRAIN), eight 7.5 cm courses of 20 cm bricks, stretcher bond */
const BRICK_TEX = canvasTex(256, 256, (g, w, h) => {
  g.fillStyle = "#cbbca6"; g.fillRect(0, 0, w, h);
  const r = rnd(17), ch = h / 8, bw = w / 3;
  for (let row = 0; row < 8; row++) for (let k = -1; k < 4; k++) {
    const x = k * bw + (row % 2 ? bw / 2 : 0), t = r();
    g.fillStyle = `rgb(${150 + t * 30},${78 + t * 18},${55 + t * 12})`; g.fillRect(x + 2, row * ch + 2, bw - 4, ch - 4);
  }
});
function kindOf(fill, flags, size) {
  if (fill === "glass") return "glass";
  if (fill === "art") return "art";
  if (fill === "brick") return "brick";   // v23: the stairs' brick side wall
  if ((flags || "").includes("s") && ((flags || "").includes("g") || OAKS.has(fill))) return "stairs";   // v26: the stairs' wood keeps its own colour
  if (PAINT_OLD.has(fill)) return "paint";
  if ((flags || "").includes("o")) return "trans";
  const c = new THREE.Color(fill), o = {}; c.getHSL(o);
  if (size !== undefined && size < 1.6 && o.s > 0.6 && o.l > 0.45) return "led";
  if ((flags || "").includes("g") || OAKS.has(fill)) return "oak";
  return o.l < 0.12 ? "dark" : "plain";
}
function kindMat(kind) {
  if (KIND[kind]) return KIND[kind];
  const m = {
    oak: () => new THREE.MeshStandardMaterial({ vertexColors: true, map: OAK_TEX, bumpMap: OAK_BUMP, bumpScale: 0.35, roughness: 0.58 }),
    stairs: () => Object.assign(new THREE.MeshStandardMaterial({ vertexColors: true, map: OAK_TEX, bumpMap: OAK_BUMP, bumpScale: 0.35, roughness: 0.58 }), { userData: { noTint: true } }),
    plain: () => new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.72 }),
    dark: () => new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.42, metalness: 0.05 }),
    fabric: () => new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.9, bumpMap: CORD, bumpScale: 0.9 }),
    led: () => new THREE.MeshBasicMaterial({ vertexColors: true, toneMapped: false }),
    glass: () => new THREE.MeshPhysicalMaterial({ color: "#ffffff", roughness: 0.04, transmission: 0, transparent: true, opacity: 0.16, depthWrite: false }),
    art: () => new THREE.MeshStandardMaterial({ map: ART_TEX, roughness: 0.5 }),
    brick: () => new THREE.MeshStandardMaterial({ map: BRICK_TEX, bumpMap: BRICK_TEX, bumpScale: 0.6, roughness: 0.92, side: THREE.DoubleSide }),
    trans: () => new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.7, transparent: true, opacity: 0.85 }),
  }[kind]();
  return KIND[kind] = reg(m);
}

/* ---------------------------------------------------------------- geometry from the plan's records */
const GRAIN = 0.6;   // metres of oak per texture repeat
function colAttr(geo, cols) { geo.setAttribute("color", new THREE.Float32BufferAttribute(cols, 3)); }
const SOFT = new Set([R.SOFA_CORD[0]]);   // v15: the blue corduroy sofa, upholstered rather than boxy
function softGeo(b) {
  const [, x, y, z, w, h, d, f] = b, r = Math.min(4, Math.min(w, h, d) / 2.6);
  const g = new RoundedBoxGeometry(w * M, h * M, d * M, 3, r * M);
  g.translate(-(x + w / 2) * M, (y + h / 2) * M, (z + d / 2) * M);
  const c = new THREE.Color(f), cols = [];
  for (let i = 0; i < g.attributes.position.count; i++) cols.push(c.r, c.g, c.b);
  colAttr(g, cols);
  return g;
}
function boxGeo(b) {
  const [, x, y, z, w, h, d, f, t, s] = b;
  if (SOFT.has(f)) return softGeo(b);
  const g = new THREE.BoxGeometry(Math.max(w, 0.05) * M, Math.max(h, 0.05) * M, Math.max(d, 0.05) * M);
  g.translate(-(x + w / 2) * M, (y + h / 2) * M, (z + d / 2) * M);
  const uv = g.attributes.uv, span = [[d, h], [d, h], [w, d], [w, d], [w, h], [w, h]];
  for (let face = 0; face < 6; face++) {
    const [su, sv] = span[face].map(v => v * M / GRAIN), rot = span[face][1] > span[face][0];
    const ox = ((x * 7.3 + z * 3.1) % 1), oy = ((y * 5.7 + face) % 1);
    for (let k = 0; k < 4; k++) {
      const i = face * 4 + k, u = uv.getX(i), v = uv.getY(i);
      if (rot) uv.setXY(i, v * sv + ox, u * su + oy); else uv.setXY(i, u * su + ox, v * sv + oy);
    }
  }
  const front = new THREE.Color(f);
  const hue = c => { const o = {}; c.getHSL(o); return o; };
  const differs = c2 => { if (!c2) return false; const a = hue(front), b2 = hue(new THREE.Color(c2)); return Math.abs(a.h - b2.h) > 0.07 || Math.abs(a.s - b2.s) > 0.3; };
  const top = differs(t) ? new THREE.Color(t) : front, side = differs(s) ? new THREE.Color(s) : front;
  const faceCol = [side, side, top, top, front, front], cols = [];
  for (let face = 0; face < 6; face++) for (let k = 0; k < 4; k++) cols.push(faceCol[face].r, faceCol[face].g, faceCol[face].b);
  colAttr(g, cols);
  return g;
}
function polyGeo(p) {
  const c = p[1], n = c.length / 3, pts = [];
  for (let i = 0; i < n; i++) pts.push(v3(c[3 * i], c[3 * i + 1], c[3 * i + 2]));
  const pos = [], uvs = [], cols = [], col = new THREE.Color(p[2] && p[2][0] === "#" ? p[2] : "#ffffff");
  const nrm = new THREE.Vector3().crossVectors(pts[1].clone().sub(pts[0]), pts[2].clone().sub(pts[0]));
  const ax = Math.abs(nrm.x) > Math.abs(nrm.y) && Math.abs(nrm.x) > Math.abs(nrm.z) ? ["z", "y"] : Math.abs(nrm.y) > Math.abs(nrm.z) ? ["x", "z"] : ["x", "y"];
  const uvOf = q => [q[ax[0]] / GRAIN, q[ax[1]] / GRAIN];
  for (let i = 1; i < n - 1; i++) for (const q of [pts[0], pts[i], pts[i + 1]]) { pos.push(q.x, q.y, q.z); uvs.push(...uvOf(q)); cols.push(col.r, col.g, col.b); }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute("uv", new THREE.Float32BufferAttribute(uvs, 2));
  colAttr(g, cols);
  g.computeVertexNormals();
  return g;
}
function frameMesh(f) {
  const [, x1, x2, top, z, holes, fill] = f;
  const sh = new THREE.Shape([new THREE.Vector2(-x1 * M, 0), new THREE.Vector2(-x2 * M, 0), new THREE.Vector2(-x2 * M, top * M), new THREE.Vector2(-x1 * M, top * M)]);
  for (const [a, b, yb] of holes) sh.holes.push(new THREE.Path([new THREE.Vector2(-a * M, yb * M), new THREE.Vector2(-a * M, (top - 2) * M), new THREE.Vector2(-b * M, (top - 2) * M), new THREE.Vector2(-b * M, yb * M)]));
  const g = new THREE.ExtrudeGeometry(sh, { depth: 2 * M, bevelEnabled: false });
  const uv = g.attributes.uv; for (let i = 0; i < uv.count; i++) uv.setXY(i, uv.getX(i) / GRAIN, uv.getY(i) / GRAIN);
  g.translate(0, 0, z * M);
  const c = new THREE.Color(fill), cols = []; for (let i = 0; i < g.attributes.position.count; i++) cols.push(c.r, c.g, c.b);
  colAttr(g, cols);
  return new THREE.Mesh(g, kindMat(kindOf(fill, "g")));
}
function buildGroup(items, name) {
  const grp = new THREE.Group(); grp.name = name;
  const above = new THREE.Group(); above.name = "above"; grp.add(above);
  const buckets = {};
  for (const it of items) {
    if (it[0] === "f") { const m = frameMesh(it); shadow(m); grp.add(m); continue; }
    let geo, kind, fill = it[0] === "b" ? it[7] : it[2], flags = it[0] === "b" ? it[10] : it[3];
    if (fill === "screen" || fill === null) continue;
    if (it[0] === "b") { kind = SOFT.has(fill) ? "fabric" : kindOf(fill, flags, Math.max(it[4], it[5], it[6])); geo = boxGeo(it); }
    else { kind = kindOf(fill, flags); geo = polyGeo(it); }
    const high = it[0] === "p" && Math.min(...it[1].filter((_, i) => i % 3 === 1)) >= R.CEIL - 0.5;
    if (kind === "paint") {
      const m = new THREE.Mesh(geo, paintMat(lum(fill) / BASE_L, it[0] === "b", it[0] === "p"));
      shadow(m); (high ? above : grp).add(m); continue;
    }
    const key = kind + (it[0] === "p" ? "p" : "") + (high ? "h" : "");
    (buckets[key] = buckets[key] || { kind, poly: it[0] === "p", high, geos: [] }).geos.push(geo);
  }
  for (const b of Object.values(buckets)) {
    const geo = mergeGeometries(b.geos.map(g => g.index ? g.toNonIndexed() : g));
    let mat = kindMat(b.kind);
    if (b.poly) { mat = mat.clone(); mat.side = THREE.DoubleSide; reg(mat); }
    const m = new THREE.Mesh(geo, mat); shadow(m, b.kind !== "glass" && b.kind !== "led");
    (b.high ? above : grp).add(m);
  }
  return grp;
}
function shadow(m, cast = true) { m.castShadow = cast; m.receiveShadow = true; return m; }

/* ---------------------------------------------------------------- the room's shell */
const shell = new THREE.Group(); scene.add(shell);
const aboveAll = [];
function rect(cx, cy, cz, w, h, normal, mat) {     // a wall patch w × h (cm) centred at (cx, cy, cz), facing `normal` (room coords)
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w * M, h * M), mat);
  m.position.copy(v3(cx, cy, cz));
  const n = new THREE.Vector3(-normal[0], normal[1], normal[2]);
  m.lookAt(m.position.clone().add(n));
  m.receiveShadow = true;
  const uv = m.geometry.attributes.uv; for (let i = 0; i < uv.count; i++) uv.setXY(i, uv.getX(i) * w / 100, uv.getY(i) * h / 100);
  shell.add(m); return m;
}
/* a wall on the plane axis = c, spanning u0..u1 along the other horizontal axis and y0..y1, with rectangular holes */
function wall(axis, c, u0, u1, y0, y1, normal, mat, holes = []) {
  const cuts = [...new Set([u0, u1, ...holes.flatMap(h => [h[0], h[1]])])].filter(u => u >= u0 && u <= u1).sort((a, b) => a - b);
  for (let i = 0; i < cuts.length - 1; i++) {
    const a = cuts[i], b = cuts[i + 1], mid = (a + b) / 2;
    const hs = holes.filter(h => h[0] <= mid && h[1] >= mid).sort((p, q) => p[2] - q[2]);
    let y = y0; const spans = [];
    for (const h of hs) { if (h[2] > y) spans.push([y, h[2]]); y = Math.max(y, h[3]); }
    if (y < y1) spans.push([y, y1]);
    for (const [ya, yb] of spans) {
      if (axis === "x") rect(c, (ya + yb) / 2, mid, b - a, yb - ya, normal, mat);
      else rect(mid, (ya + yb) / 2, c, b - a, yb - ya, normal, mat);
    }
  }
}
const BUCKET = new Map();   // v14.1: the shell's small parts, merged into one mesh per material
function cube(x, y, z, w, h, d, mat, cast = true) {
  const g = new THREE.BoxGeometry(w * M, h * M, d * M);
  g.translate(-(x + w / 2) * M, (y + h / 2) * M, (z + d / 2) * M);
  const k = mat.uuid + (cast ? "c" : "");
  if (!BUCKET.has(k)) BUCKET.set(k, { mat, cast, geos: [] });
  BUCKET.get(k).geos.push(g);
  return null;
}
function flushCubes(parent) {
  for (const b of BUCKET.values()) parent.add(shadow(new THREE.Mesh(mergeGeometries(b.geos), b.mat), b.cast));
  BUCKET.clear();
}
function buildShell() {
  const wallP = paintMat(lum("#2d5a46") / BASE_L), recP = paintMat(lum("#264c3a") / BASE_L), ceilP = paintMat(lum("#33604a") / BASE_L, false, false, "ceil");
  const egg = paintMat(lum("#346650") / BASE_L, true, false, "trim");
  const C = R.CEIL, Wd = R.W, A = R.ALC_W, AD = R.ALC_D, [B0, B1] = R.BREAST_X, RZ = R.RECESS_Z, WZ = R.WINDOW_Z;
  const [dx0, dx1] = R.DOOR_X, [sx0, sx1] = R.STAIR_X, [wx0, wx1] = R.WINDOW_X, [wy0, wy1] = R.WINDOW_Y;
  wall("x", 0, WZ, AD, 0, C, [1, 0, 0], wallP);                                   // the side (east) wall, into the alcove
  wall("z", AD, 0, A, 0, C, [0, 0, -1], wallP);                                   // the alcove's back
  wall("x", B0, 0, AD, 0, C, [-1, 0, 0], recP);                                    // the breast's reveal
  wall("z", 0, B0, B1, 0, C, [0, 0, -1], wallP);                                   // the chimney breast
  wall("x", B1, 0, RZ, 0, C, [1, 0, 0], recP);                                     // the recess's side
  wall("z", RZ, B1, Wd, 0, C, [0, 0, -1], recP, [[dx0, dx1, 0, R.DOOR_H], [sx0, Wd, 0, C]]);   // the door wall, open over the stairs
  wall("x", Wd, WZ, RZ, 0, C, [-1, 0, 0], wallP);                                  // the stairs (west) wall
  wall("z", WZ, 0, Wd, 0, C, [0, 0, 1], wallP, [[wx0, wx1, wy0, wy1]]);            // the window wall
  // v16: the hollow pipe boxing in the window's west corner, floor to ceiling, painted with the walls
  const PX = R.PIPE_BOX;
  cube(PX.x[0], 0, PX.z[0], PX.x[1] - PX.x[0], C, PX.z[1] - PX.z[0], wallP);
  // floor (carpet) and ceiling (painted, with the opening over the stairs)
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(Wd * M, (RZ - WZ) * M), floorMat = reg(new THREE.MeshStandardMaterial({ map: CARPET, roughness: 1, bumpMap: PILE, bumpScale: 0.5 })));
  floor.rotation.x = -Math.PI / 2; floor.position.copy(v3(Wd / 2, 0, (RZ + WZ) / 2)); floor.receiveShadow = true; shell.add(floor);
  const wx = R.WELL_X0, front = R.STAIR_FRONT;
  ceilGlow = canvasTex(512, 512, (g, w, h) => {     // the strip's glow on the ceiling, brightest at the edges
    g.fillStyle = "#2c261f"; g.fillRect(0, 0, w, h);    // the bounce over the whole ceiling, then the glow along each edge
    const e = 150;
    for (const [x0, y0, x1, y1, gx0, gy0, gx1, gy1] of [[0, 0, w, e, 0, 0, 0, e], [0, h - e, w, h, 0, h, 0, h - e], [0, 0, e, h, 0, 0, e, 0], [w - e, 0, w, h, w, 0, w - e, 0]]) {
      const gr = g.createLinearGradient(gx0, gy0, gx1, gy1); gr.addColorStop(0, "rgba(255,226,190,0.9)"); gr.addColorStop(1, "rgba(255,226,190,0)");
      g.globalCompositeOperation = "lighter"; g.fillStyle = gr; g.fillRect(x0, y0, x1 - x0, y1 - y0);
    }
  });
  ceilGlow.wrapS = ceilGlow.wrapT = THREE.ClampToEdgeWrapping;
  ceilMat = ceilP.clone(); ceilMat.emissiveMap = ceilGlow; ceilMat.emissive = new THREE.Color("#ffe2c0"); ceilMat.userData = { ratio: ceilP.userData.ratio, ch: "ceil" };
  paintMats.set("ceilglow", reg(ceilMat));
  for (const [xa, xb, za, zb] of [[0, wx, WZ, RZ], [wx, Wd, WZ, front]]) {
    const m = new THREE.Mesh(new THREE.PlaneGeometry((xb - xa) * M, (zb - za) * M), ceilMat);
    m.rotation.x = Math.PI / 2; m.position.copy(v3((xa + xb) / 2, C, (za + zb) / 2)); m.receiveShadow = true; shell.add(m);
  }
  // skirting, eggshell in the wall colour
  const sk = R.SKIRT_H, st = 2;
  [[0, WZ, st, sk, AD - WZ], [B1, 0, st, sk, RZ]].forEach(([x, z, w, h, d]) => cube(x, 0, z, w, h, d, egg, false));
  [[0, AD - st, A], [B0, -st, B1 - B0], [B1, RZ - st, dx0 - 6 - B1], [dx1 + 6, RZ - st, sx0 - dx1 - 6], [0, WZ, Wd]].forEach(([x, z, w]) => cube(x, 0, z, w, sk, st, egg, false));
  cube(Wd - st, 0, WZ, st, sk, R.STAIR_FRONT - WZ, egg, false);
  // the door, shut, with its frame and handle
  // v20, client: "door of room is also white": the door and its frame stay white satin, not the wall colour
  const doorW = reg(new THREE.MeshStandardMaterial({ color: "#efece5", roughness: 0.35 })), frameW = reg(new THREE.MeshStandardMaterial({ color: "#f3f1eb", roughness: 0.4 }));
  cube(dx0 - 6, 0, RZ - 1.5, 6, R.DOOR_H + 6, 2, frameW); cube(dx1, 0, RZ - 1.5, 6, R.DOOR_H + 6, 2, frameW);
  cube(dx0 - 6, R.DOOR_H, RZ - 1.5, dx1 - dx0 + 12, 6, 2, frameW);
  cube(dx0, 0, RZ + 1, dx1 - dx0, R.DOOR_H, 4, doorW);
  for (const [y0, y1] of [[14, 98], [112, 186]]) cube(dx0 + 9, y0, RZ + 0.6, dx1 - dx0 - 18, y1 - y0, 0.5, doorW);
  const brass = reg(new THREE.MeshStandardMaterial({ color: "#c9b58a", metalness: 0.9, roughness: 0.3 }));
  cube(dx1 - 12, 100, RZ - 1.6, 9, 1.4, 2.6, brass);
  // the window: white frame, glass, a sill, the view out
  const white = reg(new THREE.MeshStandardMaterial({ color: "#f1efe9", roughness: 0.45 }));
  const fw = 6, mid = (wx0 + wx1) / 2;
  // v17: the frame sits back in a deep reveal (the jambs and head in the wall paint), with a deep white sill for the plants
  const REV = R.WINDOW_REVEAL, FZ = WZ - REV;
  [[wx0, wy0, fw, wy1 - wy0], [wx1 - fw, wy0, fw, wy1 - wy0], [wx0, wy0, wx1 - wx0, fw], [wx0, wy1 - fw, wx1 - wx0, fw], [mid - 3, wy0, 6, wy1 - wy0],
   [wx0, wy0 + 0.68 * (wy1 - wy0), wx1 - wx0, 5]].forEach(([x, y, w, h]) => cube(x, y, FZ - 4, w, h, 7, white));
  cube(wx0 - 2, wy0, FZ, 2, wy1 - wy0, REV, wallP); cube(wx1, wy0, FZ, 2, wy1 - wy0, REV, wallP);   // the reveal's jambs
  cube(wx0 - 2, wy1, FZ, wx1 - wx0 + 4, 2, REV, wallP);                                          // ... and its head
  const SL = R.SILL;
  cube(wx0 - 4, SL.y - SL.t, FZ - 1, wx1 - wx0 + 8, SL.t, REV + 1 + SL.nose, white);              // the deep sill
  const glass = reg(new THREE.MeshPhysicalMaterial({ color: "#dfe8ee", roughness: 0.02, transparent: true, opacity: 0.12, depthWrite: false }));
  const pane = new THREE.Mesh(new THREE.PlaneGeometry((wx1 - wx0) * M, (wy1 - wy0) * M), glass);
  pane.position.copy(v3(mid, (wy0 + wy1) / 2, FZ - 1)); shell.add(pane);
  view = new THREE.Mesh(new THREE.PlaneGeometry(40, 14), new THREE.MeshBasicMaterial({ map: SKY.night, toneMapped: false }));
  view.position.copy(v3(mid, 300, FZ - 900)); shell.add(view);
  sillPlants(wx0, wx1, SL.y, FZ + 2, WZ + SL.nose - 1);
  // the radiator under the window, painted in
  const [rx0, rx1] = R.RADIATOR_X, [ry0, ry1] = R.RADIATOR_Y, radP = paintMat(lum("#3b6e56") / BASE_L, true, false, "trim");
  for (let x = rx0; x < rx1 - 2; x += 5) cube(x, ry0, WZ + 3, 3.4, ry1 - ry0, 7, radP);
  // the coffee table (its footprint from the plan; drawn as a plain low table)
  const cof = R.COFFEE, cofM = reg(new THREE.MeshStandardMaterial({ color: "#2c2a28", roughness: 0.5 }));
  { const cw = cof.x[1] - cof.x[0], cd = cof.z[1] - cof.z[0], g = coffeeG = new THREE.Group();     // v18: movable in edit mode
    lb(g, 0, 38, 0, cw, 4, cd, cofM);
    for (const [x, z] of [[-cw / 2 + 5, -cd / 2 + 5], [cw / 2 - 5, -cd / 2 + 5], [-cw / 2 + 5, cd / 2 - 5], [cw / 2 - 5, cd / 2 - 5]]) lb(g, x, 0, z, 4, 38, 4, cofM);
    movable("coffee", "Coffee table", g, () => ({ x: (cof.x[0] + cof.x[1]) / 2, z: (cof.z[0] + cof.z[1]) / 2, rot: 0 }), cw, cd, [cofM]); }   // v27: it stays put (v26 moved it for an eighth seat)
  // v15: the rug, 230 × 160 in front of the sofa (geometry.RUG), with its design and a little thickness
  const RG = R.RUG, rugW = RG.x[1] - RG.x[0], rugD = RG.z[1] - RG.z[0];
  const rug = new THREE.Mesh(new THREE.BoxGeometry(rugW * M, 0.008, rugD * M),
    [0, 1, 2, 3, 4, 5].map(i => i === 2 ? reg(new THREE.MeshStandardMaterial({ map: RUG_TEX, roughness: 0.97, bumpMap: PILE, bumpScale: 0.35 }))
                                        : reg(new THREE.MeshStandardMaterial({ color: RG.cols[3], roughness: 1 }))));
  rug.position.y = 0.004; rug.rotation.y = Math.PI; rug.receiveShadow = true; rugMesh = rug;
  { const g = new THREE.Group(); g.add(rug);
    movable("rug", "Rug", g, () => ({ x: (RG.x[0] + RG.x[1]) / 2, z: (RG.z[0] + RG.z[1]) / 2, rot: 0 }), rugW, rugD, [], true); }
  // v15: the curtains, from the client's photo: long pencil-pleat panels to the floor in oatmeal, on a rail just under the ceiling strip
  // running 30 past the window each side; open (stacked either side) or drawn across (S.curtains)
  // "hessian curtains from dunelm with a wood rail": a coarse natural weave, on a 28 mm wooden pole with rings and ball finials
  const CU = R.CURTAIN, cloth = curtCloth = reg(new THREE.MeshStandardMaterial({ color: CU.col, roughness: 1, side: THREE.DoubleSide, map: HESSIAN, bumpMap: HESSIAN, bumpScale: 0.8 }));
  const wood = reg(new THREE.MeshStandardMaterial({ color: CU.pole_col, map: OAK_TEX, roughness: 0.5 }));  wood.userData.noTint = true;   // v26: yours, not the new oak
  const poleL = wx1 - wx0 + 2 * CU.ext, pole = new THREE.Mesh(new THREE.CylinderGeometry(CU.pole / 2 * M, CU.pole / 2 * M, poleL * M, 16), wood);
  pole.rotation.z = Math.PI / 2; pole.position.copy(v3((wx0 + wx1) / 2, CU.rail_y + CU.pole / 2, CU.z + 1)); shell.add(shadow(pole));
  for (const xf of [wx0 - CU.ext - CU.finial / 2, wx1 + CU.ext + CU.finial / 2]) {
    const f = new THREE.Mesh(new THREE.SphereGeometry(CU.finial / 2 * M, 16, 12), wood); f.position.copy(v3(xf, CU.rail_y + CU.pole / 2, CU.z + 1)); shell.add(shadow(f));
  }
  { const rings = [];                                                     // rings, one every 10 cm (v22: one mesh)
    for (let x = wx0 - CU.ext + 3; x < wx1 + CU.ext - 2; x += 10) {
      const g = new THREE.TorusGeometry(0.02, 0.0035, 6, 16); g.rotateY(Math.PI / 2); const q = v3(x, CU.rail_y + CU.pole / 2, CU.z + 1); g.translate(q.x, q.y, q.z); rings.push(g); }
    shell.add(new THREE.Mesh(mergeGeometries(rings), wood)); }
  const panel = (x0, w, folds) => {
    const g = new THREE.PlaneGeometry(w * M, (CU.rail_y - CU.drop_to) * M, Math.round(folds * 8), 1), pos = g.attributes.position;
    for (let i = 0; i < pos.count; i++) pos.setZ(i, Math.sin(pos.getX(i) / (w * M) * Math.PI * 2 * folds / 2) * 0.026);
    g.computeVertexNormals();
    const m = new THREE.Mesh(g, cloth); m.position.copy(v3(x0 + w / 2, (CU.rail_y + CU.drop_to) / 2, CU.z)); m.rotation.y = Math.PI;
    return shadow(m);
  };
  curtOpen = new THREE.Group(); curtShut = new THREE.Group();
  curtOpen.add(panel(wx0 - CU.ext, CU.stack, CU.folds), panel(wx1 + CU.ext - CU.stack, CU.stack, CU.folds));
  const half = (wx1 - wx0) / 2 + CU.ext;
  curtShut.add(panel(wx0 - CU.ext, half, CU.folds * 2.2), panel(wx0 - CU.ext + half, half, CU.folds * 2.2));
  shell.add(curtOpen, curtShut);
  // shelf B: the client's 2 m black floating shelf on the stairs wall
  const sb = R.SHELF_B, black = shelfMat = reg(new THREE.MeshStandardMaterial({ color: "#1a1a1b", roughness: 0.55 }));
  cube(Wd - sb.d, sb.top - sb.t, sb.z[1], sb.d, sb.t, sb.z[0] - sb.z[1], black);
  // v16: "on the left of that shelf is my ikea light box" ... "black not white": the OBEGRÄNSAD panel, black, standing landscape against
  // the wall at the shelf's stair end; its 16 x 16 LEDs fill a square in the middle of the face
  const LB = R.LIGHTBOX, lbBlack = reg(new THREE.MeshStandardMaterial({ color: "#121213", roughness: 0.5 }));
  cube(Wd - 1 - LB.d, sb.top, LB.z[1], LB.d, LB.h, LB.z[0] - LB.z[1], lbBlack);
  const lbS = LB.h - 4;
  lboxFace = new THREE.Mesh(new THREE.PlaneGeometry(lbS * M, lbS * M), new THREE.MeshBasicMaterial({ map: LBOX_TEX, toneMapped: false }));
  lboxFace.position.copy(v3(Wd - 1 - LB.d - 0.15, sb.top + LB.h / 2, (LB.z[0] + LB.z[1]) / 2)); lboxFace.rotation.y = Math.PI / 2; shell.add(lboxFace);   // v16: faces the room (it faced the wall)
  // v15: "add my small laser from the middle": a small star projector on the shelf; its dots land on the ceiling over the room
  const LZ = R.LASER, [lw, lh, ld] = LZ.size;
  cube(Wd - 6 - lw, sb.top, LZ.z - ld / 2, lw, lh, ld, reg(new THREE.MeshStandardMaterial({ color: "#202124", roughness: 0.35, metalness: 0.3 })));
  const dots = [], dcol = [], rr = rnd(17), gcol = new THREE.Color("#39ff7a"), bcol = new THREE.Color("#4d7dff"), rcol = new THREE.Color("#ff3b5c");
  for (let i = 0; i < 260; i++) {                 // a fan of dots from the projector, over the ceiling and the top of the walls
    const a = (rr() - 0.5) * 2.4, d = 60 + Math.pow(rr(), 0.6) * 340;
    let x = Wd - 10 - Math.cos(a) * d, z = LZ.z + Math.sin(a) * d * 1.2, y = C - 0.4;
    if (x < 2 || z < WZ + 2 || z > AD - 2) continue;
    dots.push(-x * M, y * M, z * M);
    const c = rr() < 0.7 ? gcol : rr() < 0.5 ? bcol : rcol; dcol.push(c.r, c.g, c.b);
  }
  const dg = new THREE.BufferGeometry(); dg.setAttribute("position", new THREE.Float32BufferAttribute(dots, 3)); dg.setAttribute("color", new THREE.Float32BufferAttribute(dcol, 3));
  laserDots = new THREE.Points(dg, new THREE.PointsMaterial({ size: 0.018, vertexColors: true, toneMapped: false, transparent: true, opacity: 0.9, depthWrite: false }));
  shell.add(laserDots);
  // v15: "make the hanging plant on the wall shelf actually hang": a pot at the window end, its strands trailing down off the shelf
  const PB = R.PLANT_B, pot = reg(new THREE.MeshStandardMaterial({ color: "#e9e4da", roughness: 0.7 })), leaf = reg(new THREE.MeshStandardMaterial({ color: "#3f7a3a", roughness: 0.65, side: THREE.DoubleSide }));
  const vine = reg(new THREE.MeshStandardMaterial({ color: "#4f6b3a", roughness: 0.8 }));
  const potM = new THREE.Mesh(new THREE.CylinderGeometry(PB.pot / 2 * M, PB.pot * 0.38 * M, 0.12, 24), pot); potM.position.copy(v3(Wd - sb.d / 2 - 1, sb.top + 6, PB.z)); shell.add(shadow(potM));
  const r = rnd(4), leaves = [], vines = [];
  for (let k = 0; k < PB.strands; k++) {
    const len = PB.trail[0] + r() * (PB.trail[1] - PB.trail[0]), z0 = PB.z + (r() - 0.5) * 12, x0 = Wd - sb.d - 1 - r() * 3;
    const pts = [v3(Wd - sb.d / 2 - 2 + (r() - 0.5) * 6, sb.top + 10, z0), v3(x0 + 2, sb.top + 2, z0 + (r() - 0.5) * 4)];
    for (let j = 1; j <= 5; j++) pts.push(v3(x0 - j * 0.6 - r() * 1.5, sb.top - len * j / 5, z0 + Math.sin(j + k) * 4));
    const curve = new THREE.CatmullRomCurve3(pts);
    vines.push(new THREE.TubeGeometry(curve, 32, 0.0025, 5, false));
    for (let t = 0.06; t < 1; t += 0.055 + r() * 0.03) {
      const q = curve.getPoint(t), g = new THREE.SphereGeometry(0.026 + r() * 0.01, 8, 6);
      g.scale(1, 0.18, 0.8); g.rotateZ((r() - 0.5) * 1.2); g.rotateY(r() * Math.PI); g.translate(q.x - 0.012, q.y, q.z); leaves.push(g);
    }
  }
  for (let i = 0; i < 18; i++) { const g = new THREE.SphereGeometry(0.03, 8, 6); g.scale(1, 0.3, 1); const q = v3(Wd - sb.d / 2 - 1 + (r() - 0.5) * 12, sb.top + 13 + r() * 6, PB.z + (r() - 0.5) * 14); g.translate(q.x, q.y, q.z); leaves.push(g); }
  shell.add(shadow(new THREE.Mesh(mergeGeometries(leaves), leaf))); shell.add(new THREE.Mesh(mergeGeometries(vines), vine));
  // v15: "either add my hat there or give it a wallstand": an oak peg on the stairs wall with the hat on it. v16: off until the photo
  if (R.HAT_PEG) {
  const HP = R.HAT_PEG, oakM = reg(new THREE.MeshStandardMaterial({ color: "#c48c57", map: OAK_TEX, roughness: 0.55 }));
  const peg = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.017, HP.d * M, 20), oakM); peg.rotation.z = Math.PI / 2; peg.position.copy(v3(Wd - HP.d / 2, HP.y, HP.z)); shell.add(shadow(peg));
  const rose = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.012, 24), oakM); rose.rotation.z = Math.PI / 2; rose.position.copy(v3(Wd - 0.6, HP.y, HP.z)); shell.add(rose);
  const felt = reg(new THREE.MeshStandardMaterial({ color: "#6b5a48", roughness: 0.95 })), band = reg(new THREE.MeshStandardMaterial({ color: "#2b2622", roughness: 0.6 }));
  const hat = new THREE.Group();
  const brim = new THREE.Mesh(new THREE.CylinderGeometry(0.175, 0.175, 0.008, 40), felt);
  const crown = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.09, 0.11, 32), felt); crown.position.y = 0.058;
  const ribbon = new THREE.Mesh(new THREE.CylinderGeometry(0.0905, 0.0915, 0.022, 32), band); ribbon.position.y = 0.016;
  hat.add(shadow(brim), shadow(crown), ribbon);
  // resting on the peg, crown up and tipped a little towards the room, as a hat sits on a hook
  hat.rotation.z = -0.22; hat.position.copy(v3(Wd - 15, HP.y + 1.5, HP.z)); shell.add(hat);
  }
  // ceiling LED strip: an emissive line round the room's edge
  ledMat = new THREE.MeshBasicMaterial({ color: "#ffd9a8", toneMapped: false });
  const ly = R.LED_Y - 0.8;
  [[0.5, WZ + 1, 1, AD - WZ - 2], [Wd - 1.5, WZ + 1, 1, front - WZ - 2]].forEach(([x, z, w, d]) => cube(x, ly, z, w, 0.8, d, ledMat, false));
  [[1, WZ + 0.5, Wd - 2], [1, AD - 1.5, A - 2], [B0, -1.5, B1 - B0], [B1, RZ - 1.5, wx - B1]].forEach(([x, z, w]) => cube(x, ly, z, w, 0.8, 1, ledMat, false));
  // v15: the side run's LED strip, under its front edge (on the uprights' driver)
  runLed = new THREE.MeshBasicMaterial({ color: "#ffd9a8", toneMapped: false });
  const SR = R.SIDE_RUN;
  for (let i = 0; i < SR.edge.length - 1; i++) {
    const [d1, z1] = SR.edge[i], [d2, z2] = SR.edge[i + 1];
    cube(Math.min(d1, d2) - 2, SR.under - 0.5, z2, Math.abs(d1 - d2) + 0.8, 0.5, z1 - z2, runLed, false);
  }
  pcLit();
  buildIdeas();
  buildPlantsAndRecords();
  buildChairStore(); [chairCab, chairsIn, chairsHook].forEach(g => g && mergeStatic(g));   // v22: fewer draws
  buildOptC(); buildCab(); buildBeside();                                                      // v26; v30: the compact cabinet; v31: beside it
  flushCubes(shell);
}
/* v19: folded FRÖSVI chairs off the table. v20 ("a fully pack away setup"): an oak chair cupboard built in beside the table's window
   end, flush with the pipe boxing, four chairs inside (two on its floor, two on its shelf, each pair two deep), two doors hinged on the
   table's side. S.chairs: "cupboard" (doors shut), "open" (doors open), "hooks" (the cheaper open hooks), "away" (the garage). */
let chairStore = null, chairCab = null, chairDoors = [], chairsIn = null, chairsHook = null;
function buildChairStore() {
  const CS = R.CHAIR_STORE, H = CS.hooks, CB = CS.cupboard, [cw, cdep, ch] = R.CHAIR_FOLDED;
  const wood = reg(new THREE.MeshStandardMaterial({ color: "#b07f50", map: OAK_TEX, roughness: 0.6 }));
  const pad = reg(new THREE.MeshStandardMaterial({ color: "#77736b", roughness: 0.92 }));
  const alu = reg(new THREE.MeshStandardMaterial({ color: "#b9bcc0", roughness: 0.35, metalness: 0.8 }));
  const oak = reg(new THREE.MeshStandardMaterial({ color: "#c48c57", map: OAK_TEX, roughness: 0.55 }));
  const bx = (g, x, y, z, w, h, d, m) => { const me = new THREE.Mesh(new THREE.BoxGeometry(w * M, h * M, d * M), m); me.position.copy(v3(x + w / 2, y + h / 2, z + d / 2)); g.add(shadow(me)); return me; };
  const chair = (g, x0, y0, cz) => {                                                         // one folded chair, its face towards the room
    for (const sd of [-1, 1]) bx(g, x0, y0, cz + sd * (cw / 2 - 1.5) - 1.5, cdep, ch, 3, wood);   // the frames, legs folded together
    bx(g, x0 + 1.5, y0 + 28, cz - (cw / 2 - 3), 2.2, 38, cw - 6, pad);                             // the seat, folded up
    bx(g, x0 + 4, y0 + ch - 27, cz - (cw / 2 - 3), 3, 22, cw - 6, pad);                            // the padded back
    bx(g, x0 + 2, y0 + 12, cz - (cw / 2 - 3), 1.8, 3, cw - 6, wood);                               // a stretcher low down
  };
  const W = R.W, z0 = CB.z[1], z1 = CB.z[0], cz = (z0 + z1) / 2, t = CB.t, xf = W - CB.d;   // the gap along the wall; xf = its front face
  // the cupboard: sides, top, floor, the shelf and its lip, the back
  chairCab = new THREE.Group(); chairCab.name = "chaircab";
  bx(chairCab, xf + CB.door, 0, z0, CB.d - CB.door, CB.h, t, oak); bx(chairCab, xf + CB.door, 0, z1 - t, CB.d - CB.door, CB.h, t, oak);
  bx(chairCab, xf + CB.door, CB.h - t, z0 + t, CB.d - CB.door, t, z1 - z0 - 2 * t, oak);
  bx(chairCab, xf + CB.door, CB.plinth - t, z0 + t, CB.d - CB.door, t, z1 - z0 - 2 * t, oak);
  bx(chairCab, xf + CB.door, CB.shelf_y, z0 + t, CB.d - CB.door, t, z1 - z0 - 2 * t, oak);
  bx(chairCab, xf + CB.door, CB.shelf_y + t, z0 + t, t, CB.lip, z1 - z0 - 2 * t, oak);
  bx(chairCab, W - CB.back, CB.plinth, z0 + t, CB.back, CB.h - CB.plinth - t, z1 - z0 - 2 * t, oak);
  bx(chairCab, xf + CB.door + 1, 0, z0 + t, CB.d - CB.door - 2, CB.plinth - t, z1 - z0 - 2 * t, oak);       // the plinth
  // two doors, hinged on the table's side (z1): each a pivot at the hinge line on the cupboard's front
  chairDoors = [];
  for (const [ya, yb] of [[0, CB.shelf_y + t / 2 - 0.15], [CB.shelf_y + t / 2 + 0.15, CB.h]]) {
    const piv = new THREE.Group(); piv.position.copy(v3(xf, 0, z1));
    const d = new THREE.Mesh(new THREE.BoxGeometry(CB.door * M, (yb - ya) * M, (z1 - z0 - 0.3) * M), oak);
    d.position.set(-CB.door / 2 * M, (ya + yb) / 2 * M, -(z1 - z0) / 2 * M);   // its room face on the hinge line (three's x is the room's, mirrored)
    piv.add(shadow(d));
    const knob = new THREE.Mesh(new THREE.CylinderGeometry(0.009, 0.009, 0.02, 12), alu); knob.rotation.z = Math.PI / 2;
    knob.position.set(0.01, (ya + yb) / 2 * M, -(z1 - z0 - 5) * M); piv.add(knob);
    chairCab.add(piv); chairDoors.push(piv);
  }
  scene.add(chairCab);
  // v27, client: "ensure i can also take the chair cupboard that exists currently off the wall when im customising": in Edit room it can be
  // selected and removed (and put back from + Add); it stays on its wall (no dragging or turning: it's built in)
  chairCab.userData.movId = "chaircab";
  MOV.chaircab = { id: "chaircab", label: "The flip-top's chair cupboard", pivot: chairCab, def: () => ({ x: 0, z: 0, rot: 0 }), w: CB.d, d: z1 - z0, mats: [],
                   base: [], fixed: true, when: () => S.site !== "C" && (S.chairs === "cupboard" || S.chairs === "open" || !S.chairs) };
  // the four chairs inside (two on the floor, two on the shelf, each pair one behind the other)
  chairsIn = new THREE.Group(); chairsIn.name = "chairs";
  for (const y0 of [CB.plinth, CB.shelf_y + t]) for (let j = 0; j < 2; j++) chair(chairsIn, W - CB.back - 0.4 - cdep - j * (cdep + 0.3), y0, cz);
  scene.add(chairsIn);
  // the cheaper option: the same four on two open hooks, two on each
  chairsHook = new THREE.Group(); chairsHook.name = "chairs";
  const hz = (H.z[0] + H.z[1]) / 2;
  H.chair_y.forEach(([y0], i) => {
    for (let j = 0; j < (H.per_hook || 1); j++) chair(chairsHook, H.x - 1.5 - cdep - j * (cdep + 0.4), y0 - j * 0.8, hz);
    bx(chairsHook, H.x - R.HOOK[1], H.hook_y[i] - 1, hz - R.HOOK[0] / 2, R.HOOK[1], 1.6, R.HOOK[0], alu);
  });
  scene.add(chairsHook);
  chairStore = chairsIn;
}
function placeChairs() {
  if (!chairCab) return;
  const mode = S.chairs || "cupboard", folded = S.dining === "folded";
  placeOptC();
  if (S.site === "C") { chairCab.visible = chairsIn.visible = chairsHook.visible = false; return; }   // v26: the cabinet keeps its chairs in its own bay
  chairCab.visible = (mode === "cupboard" || mode === "open") && !(S.layout.chaircab || {}).off;   // v27: or it's been taken off the wall
  chairDoors.forEach(d => { d.rotation.y = mode === "open" ? -2.88 : 0; });   // 165° hinges: open, the doors fold back against the folded table
  chairsIn.visible = chairCab.visible && folded;                 // with the table open, they're round it
  chairsHook.visible = mode === "hooks" && folded;
}

/* v26: option C, the dining cabinet; v27: the plan, made for six; v29: two sliding doors (OPTC). v30, client: "is there anyway you can
   optimise the dining cabinet build to fit the chairs in a better way so the cabinet doesnt have to be so big", "show me both versions":
   the compact cabinet (CAB) is the plan, the sliding one the alternative. S.site "C"; S.cab "compact" / "sliding"; S.dining folded /
   four / six; S.chairs "open" opens the chair door (the table folded); S.tdoor opens the table door with the table still folded.
   The doors move by tween (cabTween), so a tap in the room swings or slides them; a still (R3D.set) snaps them. */
const cabC = () => (S.cab === "sliding" ? R.OPTC : R.CAB);   // v30: the cabinet on show
let CK = null;
function cabKit() {      // the parts both cabinets share: materials, the table standing up and open, the chairs round it and folded
  if (CK) return CK;
  const mat = o => reg(new THREE.MeshStandardMaterial(o));
  const K = {
    oak: mat({ color: "#c48c57", map: OAK_TEX, roughness: 0.55 }),
    oakV: mat({ color: "#c48c57", map: OAK_TEX_V, roughness: 0.55 }),     // the doors and the ends: the grain upright
    oakIn: mat({ color: "#b5845a", map: OAK_TEX, roughness: 0.65 }),
    oakEnd: mat({ color: "#b98250", map: OAK_TEX, roughness: 0.55 }),     // the breadboard ends, a touch darker
    dark: mat({ color: "#241f1b", roughness: 0.9 }),
    beech: mat({ color: "#d4b58c", map: OAK_TEX, roughness: 0.6 }),       // the folding chairs
    pad: mat({ color: "#8e9a80", roughness: 0.95 }),                      // sage linen seat pads
    alu: mat({ color: "#b9bcc0", roughness: 0.35, metalness: 0.8 }),
    steel: mat({ color: "#c9cbcd", roughness: 0.3, metalness: 0.9 }),     // v30: the piano hinges' knuckles
    plate: mat({ color: "#f4f1ea", roughness: 0.35 }),
    cloth: ["#efe7d8", "#8e9a80", "#c7643a"].map(c => mat({ color: c, roughness: 0.95 })),
  };
  K.bx = (g, x, y, z, w, h, d, m) => { const me = new THREE.Mesh(new THREE.BoxGeometry(w * M, h * M, d * M), m); me.position.copy(v3(x + w / 2, y + h / 2, z + d / 2)); g.add(shadow(me)); return me; };
  K.rbx = (g, x, y, z, w, h, d, m, r = 0.6) => { const me = new THREE.Mesh(new RoundedBoxGeometry(w * M, h * M, d * M, 2, Math.min(r, Math.min(w, h, d) / 2.2) * M), m); me.position.copy(v3(x + w / 2, y + h / 2, z + d / 2)); g.add(shadow(me)); return me; };
  // the table folded: standing up on its hinge rail, the inner half's apron to the room, the legs folded inside it
  K.tableFold = C => {
    const g = new THREE.Group(), [tw, tl, tt] = C.top, [tz0, tz1] = C.tz, ap = C.apron, [px, py] = C.pivot, xa = px - ap;
    K.bx(g, px, py, tz1, tt, tl, tw, K.oak);
    K.bx(g, px + tt + 0.3, py, tz1, tt, tl, tw, K.oakEnd);
    for (const [a, b] of [[tz1, tz1 + 2], [tz0 - 2, tz0]]) K.bx(g, xa, py, a, ap, tl, b - a, K.oakIn);
    for (const y of [py, py + tl - 2]) K.bx(g, xa, y, tz1 + 2, ap, 2, tw - 4, K.oakIn);
    for (const z of [C.cz - 15, C.cz + 11]) K.bx(g, xa + 0.6, py + 5, z, C.leg[1], tl - 12, 4, K.oakIn);
    return g;
  };
  // the table open: two halves flush at the joint, each a centre of staves between two breadboard ends, the corners eased; its aprons;
  // four tapered legs
  K.tableOpen = C => {
    const g = new THREE.Group(), [tw, , tt] = C.top, [tz0, tz1] = C.tz, ap = C.apron, py = C.pivot[1], [tx0, tx1] = C.tx, jx = C.joint_x;
    for (const [a, b] of [[jx, tx1], [tx0, jx - 0.15]]) {
      K.rbx(g, a + 7, py, tz1, b - a - 14, tt, tw, K.oak, 0.5);
      for (const e of [a, b - 7]) K.rbx(g, e, py, tz1, 7, tt, tw, K.oakEnd, 0.6);
    }
    for (const [a, b] of [[jx + 0.2, tx1 - ap], [tx0 + 3, jx - 3]]) {
      for (const z of [tz1 + 4, tz0 - 6]) K.bx(g, a, py - ap, z, b - a, ap, 2, K.oakIn);
      for (const x of [a, b - 2]) K.bx(g, x, py - ap, tz1 + 6, 2, ap, tw - 12, K.oakIn);
    }
    const legGeo = (() => { const lg = new THREE.CylinderGeometry(3.9 * M, 2.7 * M, C.leg_h * M, 4, 1); lg.rotateY(Math.PI / 4); lg.scale(C.leg[0] / 5.5, 1, C.leg[1] / 5.5); return lg; })();
    for (const [lx, lz] of C.legs) { const l = new THREE.Mesh(legGeo, K.oakIn); l.position.copy(v3(lx, C.leg_h / 2, lz)); g.add(shadow(l)); }
    return g;
  };
  // the chairs at the table: slatted beech folding chairs with sage pads, the back legs rising to a two-rail back; a plate at each
  K.seats = C => {
    const out = {}, [tz0, tz1] = C.tz, tx0 = C.tx[0], py = C.pivot[1], tt = C.top[2];
    const chairOpen = (g, x, z, face) => {
      const c = new THREE.Group(), sw = R.CHAIR[0], sd = R.CHAIR[1], sh = R.CHAIR[3], bh = R.CHAIR[2];
      for (let i = 0; i < 4; i++) lb(c, 0, sh - 2.2, -sd / 2 + 6 + i * 9.4, sw - 4, 2.2, 8.2, K.beech);         // the seat's slats
      for (const xx of [-sw / 2 + 1.5, sw / 2 - 1.5]) {
        const back = lb(c, xx, 0, sd / 2 - 5, 2.6, bh, 3, K.beech); back.rotation.x = -0.06;              // the back legs, rising to the back
        lb(c, xx, 0, -sd / 2 + 4, 2.6, sh - 2.2, 2.6, K.beech);                                           // the front legs
        lb(c, xx, sh - 5, 0, 2.2, 3, sd - 6, K.beech);                                                    // the seat's side rails
      }
      for (const y of [bh - 9, bh - 21]) lb(c, 0, y, sd / 2 - 5.5, sw - 3, 7, 1.8, K.beech);             // two back rails
      lb(c, 0, 14, -sd / 2 + 4, sw - 5, 2.2, 2.2, K.beech);                                               // the stretcher
      const [pw, , pt] = R.CAB.pad;                                                                      // v31: a 40 × 40 tie-on pad, tied to the back legs
      const p = new THREE.Mesh(new RoundedBoxGeometry(pw * M, pt * M, pw * M, 2, 0.012), K.pad); p.position.copy(v3(0, sh + pt / 2, -1)); c.add(shadow(p));
      for (const xx of [-sw / 2 + 1.5, sw / 2 - 1.5]) lb(c, xx, sh - 7, sd / 2 - 7.5, 1.4, 8, 1.4, K.pad);   // the ties round the back legs
      c.position.copy(v3(x, 0, z));
      c.rotation.y = { n: 0, w: Math.PI, e: Math.PI / 2 }[face] || 0;                                     // the back away from the table (local +z is the back)
      g.add(c);
    };
    for (const [k, list] of Object.entries(C.seats)) {
      const g = new THREE.Group();
      for (const [x, z, f] of list) {
        chairOpen(g, x, z, f);
        const pz = f === "n" ? tz0 - 16 : f === "w" ? tz1 + 16 : C.cz, pxp = f === "e" ? tx0 + 16 : x;
        const pl = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.008, 28), K.plate); pl.position.copy(v3(pxp, py + tt + 0.4, pz)); g.add(pl);
      }
      out[k] = g;
    }
    return out;
  };
  // a folded chair standing up, its room-side face at x0 (cz its centre along the wall)
  K.fchair = (g, x0, y0, cz) => {
    const [cw, cdep, ch] = R.CHAIR_FOLDED;
    for (const sd of [-1, 1]) {
      K.bx(g, x0 + cdep - 3, y0, cz + sd * (cw / 2 - 1.3) - 1.3, 2.6, ch, 2.6, K.beech);                // the back legs
      K.bx(g, x0 + 0.4, y0 + 2, cz + sd * (cw / 2 - 4) - 1.3, 2.6, ch - 14, 2.6, K.beech);             // the front legs, folded up against them
    }
    for (let i = 0; i < 4; i++) K.bx(g, x0 + 3.2, y0 + 30 + i * 9.4, cz - (cw / 2 - 5), 2.2, 8.2, cw - 10, K.beech);   // the seat, folded up
    for (const y of [ch - 9, ch - 21]) K.bx(g, x0 + cdep - 3.4, y0 + y, cz - (cw / 2 - 3), 1.8, 7, cw - 6, K.beech);  // the back rails
  };
  // v30: a folded chair lying on its side (the compact cabinet's base): its length along the wall, its room-side face at x0
  K.fchairLying = (g, x0, y0, cz) => {
    const [cw, cdep, ch] = R.CHAIR_FOLDED, zA = cz - ch / 2;
    for (const sd of [-1, 1]) {
      K.bx(g, x0 + cdep - 3, y0 + cw / 2 + sd * (cw / 2 - 1.3) - 1.3, zA, 2.6, 2.6, ch, K.beech);        // the back legs, along the wall
      K.bx(g, x0 + 0.4, y0 + cw / 2 + sd * (cw / 2 - 4) - 1.3, zA + 2, 2.6, 2.6, ch - 14, K.beech);
    }
    for (let i = 0; i < 4; i++) K.bx(g, x0 + 3.2, y0 + 5, zA + 30 + i * 9.4, 2.2, cw - 10, 8.2, K.beech);
    for (const z of [ch - 9, ch - 21]) K.bx(g, x0 + cdep - 3.4, y0 + 3, zA + z, 1.8, cw - 6, 7, K.beech);
  };
  CK = K;
  return K;
}

let optC = null, optCFold = null, optCOpen = null, optCChairsIn = null, optCDoors = {}, optCSeats = {};
function buildOptC() {
  /* v29, client: "i asked for a full upgrade of the tables design". Shut, the cabinet is one tidy run of oak: two sliding doors between
     its ends (Häfele Slido Classic 40 IF C), a shadow-gap plinth, nothing of the table or the chairs on show. Door A (the stair end, front
     track) slides over door B to open the table bay; B slides behind A to open the chair bay. Inside: the table standing up on its hinge
     rail, the drawer under it, the linen shelf over it; six folding chairs and their pads beside it. v30: the alternative. */
  const C = R.OPTC; if (!C) return;
  const K = cabKit(), bx = K.bx;
  const [cw, cdep] = R.CHAIR_FOLDED, W = R.W, xf = C.front, xi = C.inner, t = C.t;
  const z0 = C.z[1], z1 = C.z[0], span = z1 - z0 - 2 * t, deepIn = W - C.back - xi;   // the window end, the stair end (z0 < z1)
  optC = new THREE.Group(); optC.name = "optc";
  // the carcass: two ends the full depth (the doors run between them), the 19 mm top with the track in its groove, the floor on a
  // plinth set 2.5 back (a shadow line), the back
  bx(optC, xf, 0, z0, C.d, C.h, t, K.oakV); bx(optC, xf, 0, z1 - t, C.d, C.h, t, K.oakV);
  bx(optC, xf, C.h - C.t_top, z0 + t, C.d, C.t_top, span, K.oak);
  bx(optC, xf, C.plinth - t, z0 + t, C.d, t, span, K.oak);
  bx(optC, xf + 2.5, 0, z0 + t, C.d - 2.5, C.plinth - t, span, K.dark);
  bx(optC, W - C.back, C.plinth, z0 + t, C.back, C.h - C.plinth - C.t_top, span, K.oakIn);
  bx(optC, xf + 0.3, C.h - C.t_top - 0.7, z0 + t, C.slide - 0.6, 0.7, span, K.alu);            // the double top track
  bx(optC, xf + 0.3, C.plinth, z0 + t, C.slide - 0.6, 0.25, span, K.alu);                      // the bottom guide track
  // inside, behind the doors: the partition, the chair shelf, the linen shelf, the hinge rail, the drawer
  const [bt0, bt1] = C.bay_t, [bc0, bc1] = C.bay_c;
  bx(optC, xi, C.plinth, bt1 - t, deepIn, C.h - C.t_top - C.plinth, t, K.oakIn);
  bx(optC, xi, C.shelf_y, bc1, deepIn, t, bc0 - bc1, K.oakIn);
  bx(optC, xi, C.flap[0] - t, bt1, deepIn, t, bt0 - bt1, K.oakIn);
  const rail = C.pivot[1] - 7;
  bx(optC, xi, rail, bt1, deepIn, 7, bt0 - bt1, K.oak);
  bx(optC, xi, C.plinth + 0.3, bt1 + 0.15, t, rail - C.plinth - 0.6, bt0 - bt1 - 0.3, K.oak);   // the drawer's front, inside
  bx(optC, xi - 0.6, (C.plinth + rail) / 2 - 0.8, C.cz - 6, 0.6, 1.6, 12, K.dark);              // its finger slot
  [[0, 0], [1, 1], [2, 2]].forEach(([i, c]) => bx(optC, xi + 3 + i * 0.4, C.flap[0] + i * 3.2, bt1 + 8 + i * 6, deepIn - 6, 3, 34, K.cloth[c]));   // the cloth, napkins and runner
  // the two sliding doors: A on the front track over the table bay, B on the back track over the chair bay; a routed finger slot near
  // each one's outer end. Each is a group placed at its stair-side edge (placeOptC slides it).
  optCDoors = {};
  for (const k of ["A", "B"]) {
    const D = C.doors[k], [dx0] = C.door_x[D.track], g = new THREE.Group();
    bx(g, dx0, C.plinth + 0.3, -C.door_w, C.door, C.door_h, C.door_w, K.oakV);
    const zs = k === "A" ? -7 : -C.door_w + 4;
    bx(g, dx0 - 0.05, 92, zs, 0.12, 26, 3, K.dark);
    optC.add(g); optCDoors[k] = g;
  }
  optCFold = K.tableFold(C); optC.add(optCFold);
  optCOpen = K.tableOpen(C); optC.add(optCOpen);
  optCSeats = K.seats(C); Object.values(optCSeats).forEach(g => optC.add(g));
  // six chairs folded in the chair bay: two across, two deep on the floor and one deep on the shelf; the six pads on edge in front of
  // the two on the shelf
  optCChairsIn = new THREE.Group();
  for (const cz of C.chair_z) {
    for (let j = 0; j < 2; j++) K.fchair(optCChairsIn, W - C.back - 0.3 - cdep - j * (cdep + 0.3), C.plinth, cz);
    K.fchair(optCChairsIn, W - C.back - 0.3 - cdep, C.shelf_y + t, cz);
    for (let k = 0; k < 3; k++) bx(optCChairsIn, xi + 0.6 + k * 3.1, C.shelf_y + t, cz - 19, 3, 38, 38, K.pad);
  }
  optC.add(optCChairsIn);
  scene.add(optC);
}

/* v30: the compact cabinet, two boxes side by side: the table box at the stair end (the table on its hinge rail, two chairs lying on
   their sides in the base under it, the linen shelf over it, the six seat pads on the door's back) and the chair box (four chairs, two
   deep on its floor and two deep on its shelf). Inset doors, each on a full-height piano hinge with its knuckle on the front: the table
   door turns 180° towards the window and lies back over the chair door and the wall beyond; the chair door turns 180° towards the
   stairs and lies back over the table door. */
let cab = null, cabFold = null, cabOpen = null, cabSeats = {}, cabIn = null, cabDoor = {}, cabPads = null;
function buildCab() {
  const C = R.CAB; if (!C) return;
  const K = cabKit(), bx = K.bx, W = R.W, t = C.t, xf = C.front, xi = C.inner, deepIn = C.in_d;
  const [cw, cdep] = R.CHAIR_FOLDED;
  cab = new THREE.Group(); cab.name = "cab";
  // two carcasses: each two ends, a top, a floor on a plinth set 2.5 back (a shadow line), a back; the boxes screwed together
  for (const [a, b] of [C.z_t, C.z_c]) {
    const span = a - b - 2 * t;
    bx(cab, xf, 0, b, C.d, C.h, t, K.oakV); bx(cab, xf, 0, a - t, C.d, C.h, t, K.oakV);
    bx(cab, xf, C.h - C.t_top, b + t, C.d, C.t_top, span, K.oak);
    bx(cab, xf, C.plinth - t, b + t, C.d, t, span, K.oak);
    bx(cab, xf + 2.5, 0, b + t, C.d - 2.5, C.plinth - t, span, K.dark);
    bx(cab, W - C.back, C.plinth, b + t, C.back, C.h - C.plinth - C.t_top, span, K.oakIn);
  }
  const [bt0, bt1] = C.bay_tz, [bc0, bc1] = C.bay_cz;
  bx(cab, C.rail_x[0], C.rail[0], bt1, C.rail_x[1] - C.rail_x[0], 7, bt0 - bt1, K.oak);         // the hinge rail (v31: set back behind the pads)
  bx(cab, xi + C.pads, C.linen[0] - t, bt1, C.linen_d, t, bt0 - bt1, K.oakIn);                    // the linen shelf (v31: the same)
  bx(cab, xi, C.shelf_y, bc1, deepIn, t, bc0 - bc1, K.oakIn);                                     // the chair bay's shelf
  [[0, 0], [1, 1], [2, 2]].forEach(([i, c]) => bx(cab, xi + C.pads + 1 + i * 0.4, C.linen[0] + i * 3.2, bt1 + 8 + i * 6, deepIn - C.pads - 2, 3, 34, K.cloth[c]));   // the cloth, napkins, runner
  // the chairs: two lying in the base, two deep; four standing in the chair bay, two deep on its floor and on its shelf
  cabIn = new THREE.Group();
  for (let j = 0; j < C.chairs_base; j++) K.fchairLying(cabIn, xi + 0.3 + j * (cdep + 0.3), C.base[0], C.cz);
  for (const x0 of C.chair_x) for (const y0 of [C.plinth, C.shelf_y + t]) K.fchair(cabIn, x0, y0, C.chair_z);
  cab.add(cabIn);
  cabFold = K.tableFold(C); cab.add(cabFold);
  cabOpen = K.tableOpen(C); cab.add(cabOpen);
  cabSeats = K.seats(C); Object.values(cabSeats).forEach(g => cab.add(g));
  // the doors: each a group at its hinge's axis, so turning it is a rotation; the door panel, a routed finger slot near its free edge,
  // the piano hinge's knuckle; the table door carries the six seat pads on its back (a child of the door, so they swing with it)
  cabDoor = {};
  const ax = xf - C.knuckle;
  const door = (key, z0, z1, hz) => {
    const g = new THREE.Group(); g.position.copy(v3(ax, 0, hz));
    const loc = (x, z) => [x - ax, z - hz];                                       // room cm to the door's own frame (x into the cabinet, z along it)
    const [lx, lz0] = loc(xf, Math.min(z0, z1)), lz1 = loc(xf, Math.max(z0, z1))[1];
    bx(g, lx, C.plinth + C.gap, lz0, C.door, C.door_h, lz1 - lz0, K.oakV);
    const free = Math.abs(z0 - hz) > Math.abs(z1 - hz) ? z0 : z1, sz = free > hz ? -1 : 1;
    bx(g, lx - 0.05, 92, loc(xf, free + sz * 5 - (sz < 0 ? 0 : 2.5))[1], 0.12, 26, 2.5, K.dark);   // the finger slot, 5 in from its free edge
    const kn = new THREE.Mesh(new THREE.CylinderGeometry(0.28 * M, 0.28 * M, 180 * M, 8), K.steel); kn.position.copy(v3(0, C.plinth + C.gap + C.door_h / 2, 0)); g.add(kn);
    cab.add(g); cabDoor[key] = g; return g;
  };
  door("T", C.door_t[0], C.door_t[1], C.door_t[1] - C.hinge_gap / 2);
  door("C", C.door_c[0], C.door_c[1], C.door_c[0] + C.hinge_gap / 2);
  // the six pads on the table door's back, two across and three high, from the hinge rail's underside up (v31: 40 × 40 tie-on pads,
  // their ties hanging; the rail and the linen shelf stand back so they can)
  cabPads = new THREE.Group();
  const hzT = C.door_t[1] - C.hinge_gap / 2, mid = (C.door_t[0] + C.door_t[1]) / 2, [pw, ph, pt] = C.pad;
  for (let r = 0; r < 3; r++) for (const s of [-1, 1]) {
    const y0 = C.pad_zone[0] + 0.3 + r * (ph + 0.2), z0 = mid + s * (pw / 2 + 0.2) - pw / 2 - hzT;
    K.rbx(cabPads, xf + C.door + 0.4 - ax, y0, z0, pt, ph, pw, K.pad, 1.2);
    for (const e of [0.2, 0.8]) bx(cabPads, xf + C.door + 0.4 - ax, y0 + ph - 1, z0 + pw * e - 0.6, 0.4, 9, 1.2, K.pad);   // its two ties, on the hook
  }
  cabDoor.T.add(cabPads);
  scene.add(cab);
}
/* the doors' tween: each entry eases its object's rotation.y or position.z to a target; a still snaps them (cabSnap) */
const CAB_TW = new Map();
let cabSnap = false;
function twTo(obj, prop, target) {
  if (!obj) return;
  const cur = prop === "ry" ? obj.rotation.y : obj.position.z;
  if (cabSnap || REDUCE_M || Math.abs(cur - target) < 1e-4) { if (prop === "ry") obj.rotation.y = target; else obj.position.z = target; CAB_TW.delete(obj); return; }
  CAB_TW.set(obj, { prop, from: cur, to: target, t0: performance.now(), dur: 700 });
}
function cabTween(now) {     // from the frame loop: true while anything is still moving
  if (!CAB_TW.size) return false;
  for (const [o, w] of CAB_TW) {
    const k = Math.min(1, (now - w.t0) / w.dur), e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2, v = w.from + (w.to - w.from) * e;
    if (w.prop === "ry") o.rotation.y = v; else o.position.z = v;
    if (k >= 1) CAB_TW.delete(o);
  }
  reshadow();
  return true;
}
const REDUCE_M = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
function cabDoors() {        // which doors stand open: the table door with the table out (or S.tdoor), the chair door with S.chairs "open"
  const folded = S.dining === "folded";
  return { table: !folded || !!S.tdoor, chairs: folded && S.chairs === "open" && !S.tdoor };
}
function placeOptC() {
  const on = S.site === "C", sliding = S.cab === "sliding", folded = S.dining === "folded", n = S.dining === "six" ? "six" : "four";
  const dr = cabDoors();
  if (optC) {
    const C = R.OPTC, vis = on && sliding;
    optC.visible = vis;
    if (vis) {
      optCFold.visible = folded; optCOpen.visible = !folded;
      for (const [k, g] of Object.entries(optCSeats)) g.visible = !folded && k === n;
      optCChairsIn.visible = folded;
      // v29: the doors slide: the table out, door A over door B; the chairs out (the table folded), door B behind door A
      twTo(optCDoors.A, "pz", v3(0, 0, (dr.table ? C.doors.A.slid : C.doors.A.shut)[0]).z);
      twTo(optCDoors.B, "pz", v3(0, 0, (dr.chairs ? C.doors.B.slid : C.doors.B.shut)[0]).z);
    }
  }
  if (cab) {
    const vis = on && !sliding;
    cab.visible = vis;
    if (vis) {
      cabFold.visible = folded; cabOpen.visible = !folded;
      for (const [k, g] of Object.entries(cabSeats)) g.visible = !folded && k === n;
      cabIn.visible = folded;
      cabPads.visible = folded;                          // with the table out, the pads are on the chairs
      // v30: each door turns 180° about its knuckle: the table door towards the window (z falls), the chair door towards the stairs
      twTo(cabDoor.T, "ry", dr.table ? Math.PI : 0);
      twTo(cabDoor.C, "ry", dr.chairs ? -Math.PI : 0);
    }
  }
  placeFoot(); placeBeside();
}
/* v31: beside the compact cabinet (Layout, "Beside the cabinet"): left clear, a tall mirror, a slim trolley or a low oak shelf. All of
   them stand no deeper than the cabinet, behind the open table door's line */
let beside = null;
const BES = {};
function buildBeside() {
  const B = R.BESIDE; if (!B) return;
  const K = cabKit(), bx = K.bx, mat = o => reg(new THREE.MeshStandardMaterial(o)), W = R.W;
  beside = new THREE.Group(); beside.name = "beside"; scene.add(beside);
  const zc = (B.z[0] + B.z[1]) / 2;
  // the mirror: IKEA NISSEDAL, black frame, on the wall, centred in the gap
  if (B.mirror) {
    const m = B.mirror, g = new THREE.Group(); g.name = "mirror"; BES.mirror = g; beside.add(g);
    bx(g, W - m.t, m.y0, zc - m.w / 2, m.t, m.h, m.w, K.dark);
    // the glass: no live reflection (it would draw the room twice), a soft daylight sheen with two diagonal highlights reads as a mirror
    const sheen = canvasTex(128, 512, (c, w, h) => {
      const gr = c.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#eef3f4"); gr.addColorStop(0.55, "#cdd8db"); gr.addColorStop(1, "#aab7bb");
      c.fillStyle = gr; c.fillRect(0, 0, w, h); c.globalAlpha = 0.35; c.fillStyle = "#ffffff";
      for (const [y, t] of [[90, 60], [230, 26]]) { c.beginPath(); c.moveTo(0, y); c.lineTo(w, y - 70); c.lineTo(w, y - 70 + t); c.lineTo(0, y + t); c.fill(); }
    });
    const glass = new THREE.Mesh(new THREE.PlaneGeometry((m.w - 4) * M, (m.h - 4) * M), mat({ color: "#ffffff", map: sheen, roughness: 0.12, metalness: 0.25 }));
    glass.rotation.y = Math.PI / 2; glass.position.copy(v3(W - m.t - 0.05, m.y0 + m.h / 2, zc)); g.add(glass);
  }
  // the low oak shelf: the chair box's width, table height, open to the room: plates face-out, bowls, glasses, a few bottles
  if (B.dresser) {
    const d = B.dresser, g = new THREE.Group(); g.name = "dresser"; BES.dresser = g; beside.add(g);
    const z0 = B.z[0] - d.w, x0 = W - d.d, t = d.t;
    bx(g, x0, 0, z0, d.d, d.h, t, K.oakV); bx(g, x0, 0, B.z[0] - t, d.d, d.h, t, K.oakV);        // the two ends
    bx(g, x0, d.h - t, z0 + t, d.d, t, d.w - 2 * t, K.oak); bx(g, x0, 1.2, z0 + t, d.d, t, d.w - 2 * t, K.oakIn);   // the top and the floor
    bx(g, W - 0.6, 3, z0 + t, 0.6, d.h - t - 3, d.w - 2 * t, K.oakIn);                            // the back
    bx(g, x0 + 0.5, d.shelf, z0 + t, d.d - 1.1, t, d.w - 2 * t, K.oakIn);                         // the shelf
    for (let i = 0; i < 6; i++) {                                                                  // six plates on edge, one behind the other
      const pl = new THREE.Mesh(new THREE.CylinderGeometry(13.5 * M, 13.5 * M, 1.2 * M, 32), K.plate);
      pl.rotation.z = Math.PI / 2; pl.position.copy(v3(x0 + 3 + i * 2.4, d.shelf + t + 13.7, zc + 2)); g.add(shadow(pl));
    }
    const glassM = mat({ color: "#dfe9ee", roughness: 0.05, metalness: 0.1, transparent: true, opacity: 0.45 });
    for (let i = 0; i < 4; i++) { const gl2 = new THREE.Mesh(new THREE.CylinderGeometry(3.6 * M, 3 * M, 11 * M, 18), glassM); gl2.position.copy(v3(x0 + 5 + (i % 2) * 9, 3 + 5.5 + 1.8, z0 + 8 + Math.floor(i / 2) * 9)); g.add(gl2); }
    const bottle = mat({ color: "#2f4a2c", roughness: 0.2, metalness: 0.2 });
    for (let i = 0; i < 3; i++) { const b = new THREE.Mesh(new THREE.CylinderGeometry(3.7 * M, 3.7 * M, 30 * M, 18), bottle); b.position.copy(v3(x0 + 10, 3 + 15 + 1.8, B.z[0] - 9 - i * 8.5)); g.add(shadow(b)); }
    const carafe = new THREE.Mesh(new THREE.CylinderGeometry(4 * M, 5 * M, 24 * M, 20), glassM); carafe.position.copy(v3(x0 + 11, d.h + 12, zc + 6)); g.add(carafe);
  }
  // the slim trolley: three trays on a frame, four castors; it parks along the wall and wheels out to the table's far end
  if (B.trolley) {
    const tr = B.trolley, g = new THREE.Group(); g.name = "trolley"; BES.trolley = g; beside.add(g);
    const body = mat({ color: tr.col || "#2b2b2b", roughness: 0.5, metalness: 0.3 }), x0 = W - 1.5 - tr.d, z0 = zc - tr.w / 2;
    for (const [xx, zz] of [[x0, z0], [x0 + tr.d - 1.2, z0], [x0, z0 + tr.w - 1.2], [x0 + tr.d - 1.2, z0 + tr.w - 1.2]]) bx(g, xx, 4, zz, 1.2, tr.h - 4, 1.2, body);
    for (const y of tr.tiers) { bx(g, x0, y, z0, tr.d, 0.8, tr.w, body); bx(g, x0, y, z0, tr.d, 4, 0.6, body); bx(g, x0, y, z0 + tr.w - 0.6, tr.d, 4, 0.6, body); }
    for (const [xx, zz] of [[x0 + 1, z0 + 1], [x0 + tr.d - 1, z0 + 1], [x0 + 1, z0 + tr.w - 1], [x0 + tr.d - 1, z0 + tr.w - 1]]) {
      const w = new THREE.Mesh(new THREE.CylinderGeometry(2 * M, 2 * M, 1.5 * M, 14), K.dark); w.rotation.x = Math.PI / 2; w.position.copy(v3(xx, 2, zz)); g.add(w); }
    const cup = mat({ color: "#efe7d8", roughness: 0.5 });
    for (let i = 0; i < 3; i++) { const c = new THREE.Mesh(new THREE.CylinderGeometry(4 * M, 3.4 * M, 9 * M, 16), cup); c.position.copy(v3(x0 + tr.d / 2, tr.tiers[tr.tiers.length - 1] + 5.3, z0 + 8 + i * (tr.w - 16) / 2)); g.add(c); }
  }
  clipGroup(beside);
}
function placeBeside() {
  if (!beside) return;
  const on = S.site === "C" && S.cab === "compact";
  for (const [k, g] of Object.entries(BES)) g.visible = on && S.beside === k;
}
/* v31: "Show the space it needs, open": with the table folded, the floor it takes when it's out for six: the table, the six chairs
   and (the compact one) the table door's swing, drawn flat on the floor */
let foot = null, footKey = "";
function buildFoot(C) {
  const g = new THREE.Group(); g.name = "foot";
  const mat = (c, o) => new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: o, depthWrite: false, side: THREE.DoubleSide });
  const edge = new THREE.LineBasicMaterial({ color: "#1f4a38" });
  const flat = (geo, m, x, z, y = 0.6) => { const p = new THREE.Mesh(geo, m); p.rotation.x = -Math.PI / 2; p.position.copy(v3(x, y, z)); p.renderOrder = 2; g.add(p); return p; };
  const rect = (x0, x1, z0, z1, m, y) => { const p = flat(new THREE.PlaneGeometry(Math.abs(x1 - x0) * M, Math.abs(z1 - z0) * M), m, (x0 + x1) / 2, (z0 + z1) / 2, y);
    const e = new THREE.LineSegments(new THREE.EdgesGeometry(p.geometry), edge); e.rotation.copy(p.rotation); e.position.copy(p.position); g.add(e); };
  if (C.door_tw) {   // the compact cabinet: the table door turns through a half circle in front of the boxes as it opens
    const hz = C.door_t[1] - C.hinge_gap / 2, hx = C.front - C.knuckle;
    flat(new THREE.CircleGeometry(C.door_tw * M, 48, -Math.PI / 2, Math.PI), mat("#34507f", 0.16), hx, hz, 0.4);
  }
  rect(C.tx[0], C.tx[1], C.tz[1], C.tz[0], mat("#2f7d5b", 0.32), 0.7);
  const cm = mat("#c7643a", 0.26), [cw, cd] = R.CHAIR;
  for (const [x, z] of C.seats.six) rect(x - cw / 2, x + cw / 2, z - cd / 2, z + cd / 2, cm, 0.8);
  return g;
}
function placeFoot() {
  const want = !!S.foot && S.site === "C" && S.dining === "folded";
  if (want && footKey !== S.cab) { if (foot) scene.remove(foot); foot = buildFoot(cabC()); clipGroup(foot); scene.add(foot); footKey = S.cab; }
  if (foot) foot.visible = want;
}
function clipGroup(g) { g.traverse(o => { if (o.isMesh || o.isLine) [].concat(o.material).forEach(m => m && !m.clippingPlanes && clipMat(m)); }); }
/* v31: suggested set-ups (Layout): several choices at once, then a flight to the view that shows them */
const MOMENTS = {
  dinner:  { set: { site: "C", dining: "six", tdoor: false, scene: "cosy", tod: "evening", curtains: true }, view: "dining",
             say: "Dinner for six: the table out, the curtains drawn, the lights low, bar 2 up over the table" },
  four:    { set: { site: "C", dining: "four", tdoor: false, scene: "bright", tod: "day", curtains: false }, view: "sit",
             say: "Lunch for four: the table out, two a side, from your seat at the end" },
  film:    { set: { dining: "folded", tdoor: false, chairs: "cupboard", scene: "film", tod: "evening", curtains: true }, view: "sofa",
             say: "Film night: everything packed away, the lights down" },
  morning: { set: { dining: "folded", tdoor: false, chairs: "cupboard", scene: "bright", tod: "day", curtains: false }, view: "room",
             say: "An everyday morning: the cabinet shut, the room clear" },
};
function playMoment(k) {
  const m = MOMENTS[k]; if (!m) return;
  showStop(); Object.assign(S, m.set);
  if (m.set.scene) { S.lv = Object.assign({}, SCENES[m.set.scene].levels); S.master = 100; }
  applyState(); syncButtons(); setView(m.view); toast(m.say);
}
/* v31: "Watch it open": the cabinet opens step by step, a line about each step */
let showT = [];
function showStop() { showT.forEach(clearTimeout); showT = []; }
function showOpen() {
  showStop();
  const sl = S.cab === "sliding";
  const steps = [
    [0, { site: "C", dining: "folded", tdoor: false, chairs: "cupboard" }, "chairs", "Packed away: the table and all six chairs inside"],
    [1800, { chairs: "open" }, null, sl ? "1 · Slide door B behind door A: the chairs and their pads" : "1 · Open the chair door: four chairs, two on the floor and two on the shelf"],
    [4600, { chairs: "cupboard", tdoor: true }, "dining", sl ? "2 · Slide door A over door B: the table, folded" : "2 · Shut it and open the table door: the six pads and two more chairs"],
    [8000, { dining: "six", tdoor: false }, null, "3 · Lower the table and flip its half over: six sit down"],
  ];
  for (const [t, o, v, say] of steps) showT.push(setTimeout(() => { Object.assign(S, o); applyState(); syncButtons(); if (v) setView(v); toast(say); }, t));
}
/* v17: the ideas (ideas.py), each its own group, all hidden until its button is on */
const IDEA_G = {};
let ideaLed;
/* v20: the decor to try (S.decor): set by applyDecor() */
let rugMesh, curtCloth, caseFrameM, cushG, coffeeG, floorMat, shelfMat;
/* v21: suggested furniture and decor (ideas.SUGGEST, the same keys), each on or off (S.sugg); the floor pieces move in Edit room */
const SUGG_G = {};
/* v28: the suggestions' versions (ideas.SUGG_VARS): colour i goes on SVAR_MATS[k][i], a material or a light of that piece's own */
const SVAR = JSON.parse((document.getElementById("svar-data") || {}).textContent || "{}");
const SVAR_MATS = {};
const svarOf = k => (SVAR[k] && SVAR[k].some(x => x[0] === S.svar[k])) ? S.svar[k] : (SVAR[k] ? SVAR[k][0][0] : "");
function applySvar() {
  for (const [k, mats] of Object.entries(SVAR_MATS)) {
    const ver = (SVAR[k] || []).find(x => x[0] === svarOf(k)); if (!ver) continue;
    const it = MOV["sg_" + k];
    mats.forEach((m, i) => { const c = ver[2][Math.min(i, ver[2].length - 1)]; m.color.set(c);
      const j = it ? it.mats.indexOf(m) : -1; if (j >= 0) it.base[j] = c; });   // a floor piece: placeAll recolours it (and Edit room's colour still wins)
  }
}
const PRINT_TEX = canvasTex(720, 500, (g, w, h) => {      // a mid-century print: an ochre sun, a rust hill, a sage arch on cream
  g.fillStyle = "#efe7d8"; g.fillRect(0, 0, w, h);
  g.fillStyle = "#d9a441"; g.beginPath(); g.arc(w * 0.68, h * 0.34, 82, 0, Math.PI * 2); g.fill();
  g.fillStyle = "#c7643a"; g.beginPath(); g.ellipse(w * 0.36, h, 260, 230, 0, Math.PI, 0); g.fill();
  g.strokeStyle = "#7a8a6a"; g.lineWidth = 34; g.beginPath(); g.arc(w * 0.74, h, 150, Math.PI, 0); g.stroke();
  g.fillStyle = "#2f4a6e"; g.fillRect(0, h - 26, w, 26);
});
function buildSuggest() {
  const oak = reg(new THREE.MeshStandardMaterial({ color: "#c48c57", map: OAK_TEX, roughness: 0.55 }));
  const leaf = reg(new THREE.MeshStandardMaterial({ color: "#3f7a3a", roughness: 0.6, side: THREE.DoubleSide }));
  const mat = c => reg(new THREE.MeshStandardMaterial({ color: c, roughness: 0.7 }));
  // the floor pieces: movable, shown only while switched on
  const floor = (k, label, w, d, x, z, build, mats = []) => { const g = new THREE.Group(); build(g); SUGG_G[k] = movable("sg_" + k, label, g, () => ({ x, z, rot: 0 }), w, d, mats, false, { when: () => !!S.sugg[k] }); };
  const ownOak = () => reg(new THREE.MeshStandardMaterial({ color: "#c48c57", map: OAK_TEX, roughness: 0.55 }));   // v28: each piece's own, for its versions
  const ownGlow = c => new THREE.MeshBasicMaterial({ color: c, toneMapped: false });
  { const pot = mat("#d8cfc0"); SVAR_MATS.floorplant = [pot];
    floor("floorplant", "Floor plant (suggested)", 40, 40, 24, -92, g => {
      const p = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.12, 0.32, 24), pot); p.position.y = 0.16; g.add(shadow(p));
      const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.016, 1.0, 8), mat("#6b5238")); trunk.position.y = 0.8; g.add(trunk);
      const r = rnd(61), gs = [];
      for (let i = 0; i < 34; i++) { const y = 0.62 + r() * 0.85, a = r() * Math.PI * 2, rr = 0.06 + r() * 0.2 * (1.5 - (y - 0.6));
        const lg = new THREE.SphereGeometry(0.075 + r() * 0.03, 8, 6); lg.scale(1, 0.25, 0.75); lg.rotateZ((r() - 0.5) * 0.9); lg.rotateY(a);
        lg.translate(Math.cos(a) * rr, y, Math.sin(a) * rr); gs.push(lg); }
      g.add(shadow(new THREE.Mesh(mergeGeometries(gs), leaf))); }, [pot]); }
  { const oak = ownOak(); SVAR_MATS.sidetable = [oak];
  floor("sidetable", "Side table (suggested)", 40, 40, 76, -108, g => {
    const top = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.025, 32), oak); top.position.y = 0.4875; g.add(shadow(top));
    const col = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.035, 0.475, 16), oak); col.position.y = 0.2375; g.add(shadow(col));
    const foot = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.16, 0.02, 32), oak); foot.position.y = 0.01; g.add(shadow(foot)); }, [oak]); }
  { const knit = mat("#d9a441"); SVAR_MATS.pouffe = [knit];
    floor("pouffe", "Pouffe (suggested)", 50, 50, 175, -95, g => {
      const b = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.25, 0.4, 32), knit); b.position.y = 0.2; g.add(shadow(b));
      const t = new THREE.Mesh(new THREE.TorusGeometry(0.235, 0.02, 8, 32), knit); t.rotation.x = Math.PI / 2; t.position.y = 0.39; g.add(t); }, [knit]); }
  // on the walls and the coffee table: fixed, shown only while switched on
  { const g = SUGG_G.art = new THREE.Group(), z0 = -298, oak = ownOak(); SVAR_MATS.art = [oak];
    ibox(g, 0, 110, z0, 3, 55, 80, oak);
    const print = reg(new THREE.MeshStandardMaterial({ map: PRINT_TEX, roughness: 0.8 }));
    const pl = new THREE.Mesh(new THREE.PlaneGeometry(0.72, 0.47), print); pl.position.copy(v3(3.1, 137.5, z0 + 40)); pl.rotation.y = -Math.PI / 2; g.add(pl);
    shell.add(g); }
  { const g = SUGG_G.clock = new THREE.Group(), cx = (R.DOOR_X[0] + R.DOOR_X[1]) / 2, cy = R.DOOR_H + (R.CEIL - R.DOOR_H) / 2, zf = R.RECESS_Z;
    const face = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 0.03, 40), mat("#f3f1eb")); face.rotation.x = Math.PI / 2; face.position.copy(v3(cx, cy, zf - 1.5)); g.add(face);
    const rimM = SVAR_MATS.clock = [ownOak()], rim = new THREE.Mesh(new THREE.TorusGeometry(0.15, 0.008, 8, 40), rimM[0]); rim.position.copy(v3(cx, cy, zf - 3)); g.add(rim);
    const ink = mat("#1f1f21");
    for (const [len, a] of [[10, 0.6], [7, 2.4]]) { const h = new THREE.Mesh(new THREE.BoxGeometry(0.006, len * M, 0.003), ink);
      h.geometry.translate(0, len * M / 2, 0); h.position.copy(v3(cx, cy, zf - 3.2)); h.rotation.z = a; g.add(h); }
    shell.add(g); }
  { const g = SUGG_G.tray = new THREE.Group(), oak = ownOak(); SVAR_MATS.tray = [oak];
    lb(g, 12, 42, 0, 40, 1.6, 26, oak);
    lb(g, 18, 43.6, 0, 22, 3, 16, mat("#2f4a6e")); lb(g, 18, 46.6, 0, 20, 2.4, 15, mat("#c7643a"));
    const c = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.09, 20), reg(new THREE.MeshStandardMaterial({ color: "#f3ecdc", roughness: 0.8, emissive: "#ffb35a", emissiveIntensity: 0.12 })));
    c.position.copy(v3(2, 43.6 + 4.5, 2)); g.add(shadow(c));
    (coffeeG || shell).add(g); }
  // v23: six more
  const glow = new THREE.MeshBasicMaterial({ color: "#ffd59a", toneMapped: false });
  { const g = SUGG_G.fairy = new THREE.Group(), CU = R.CURTAIN, [wx0, wx1] = R.WINDOW_X, x0 = wx0 - CU.ext + 2, x1 = wx1 + CU.ext - 2, gs = [];
    for (let x = x0; x <= x1; x += 6) { const sp = new THREE.SphereGeometry(0.0045, 6, 4), q = v3(x, CU.rail_y + CU.pole / 2 - 1.6 - 1.2 * Math.abs(Math.sin((x - x0) / 23)), CU.z + 2.6); sp.translate(q.x, q.y, q.z); gs.push(sp); }
    SVAR_MATS.fairy = [ownGlow("#ffd59a")]; g.add(new THREE.Mesh(mergeGeometries(gs), SVAR_MATS.fairy[0])); shell.add(g); }
  { const g = SUGG_G.hanger = new THREE.Group(), CU = R.CURTAIN, x = R.WINDOW_X[0] + 34, z = CU.z + 1, yp = CU.rail_y - 72;
    const cord = mat("#e9e1cf");
    for (const a of [0, 2.1, 4.2]) { const c = new THREE.Mesh(new THREE.CylinderGeometry(0.002, 0.002, 0.7, 4), cord);
      c.position.copy(v3(x + Math.cos(a) * 4, yp + 46, z + Math.sin(a) * 4)); c.rotation.z = Math.cos(a) * 0.08; c.rotation.x = Math.sin(a) * 0.08; g.add(c); }
    SVAR_MATS.hanger = [mat("#c46c45")]; potPlant(g, x, yp, z, 7, 8, 3, rnd(81), SVAR_MATS.hanger[0], leaf); shell.add(g); }
  { const g = SUGG_G.trail = new THREE.Group(); SVAR_MATS.trail = [mat("#ece6da")]; potPlant(g, 172, 196, 22, 7, 10, 4, rnd(83), SVAR_MATS.trail[0], leaf); shell.add(g); }
  { const g = SUGG_G.throw = new THREE.Group(), knit = reg(new THREE.MeshStandardMaterial({ color: "#efe7d8", roughness: 1, bumpMap: HESSIAN, bumpScale: 1.4 })); SVAR_MATS.throw = [knit];
    const ze = R.SOFA.end;
    ibox(g, 22, 52, ze - 46, 70, 2.2, 46, knit);                 // folded over the seat at the open end
    ibox(g, 22, 18, ze - 0.2, 70, 36, 2.2, knit);                // and hanging over the end
    shell.add(g); }
  { const g = SUGG_G.pclamp = new THREE.Group(), y = R.PC_SHELF_TOP, z = -198, x = 13;
    const pm = SVAR_MATS.pclamp = [mat("#e8e2d4"), reg(new THREE.MeshStandardMaterial({ color: "#f3e7cf", emissive: "#ffcf8a", emissiveIntensity: 0.6, roughness: 0.6 }))];
    const base = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.05, 0.2, 20), pm[0]); base.position.copy(v3(x, y + 10, z)); g.add(shadow(base));
    const shade = new THREE.Mesh(new THREE.SphereGeometry(0.11, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), pm[1]);
    shade.position.copy(v3(x, y + 19, z)); g.add(shadow(shade)); shell.add(g); }
  // v26: six more
  { const g = SUGG_G.candles = new THREE.Group(), sb = R.SHELF_B, wax = reg(new THREE.MeshStandardMaterial({ color: "#f3ecdc", roughness: 0.8, emissive: "#ffb35a", emissiveIntensity: 0.18 })); SVAR_MATS.candles = [wax];
    [[10, -262], [12.5, -252], [15, -243]].forEach(([h, z]) => { const c = new THREE.Mesh(new THREE.CylinderGeometry(0.0375, 0.0375, h * M, 20), wax); c.position.copy(v3(R.W - sb.d / 2 - 2, sb.top + h / 2, z)); g.add(shadow(c));
      const f = new THREE.Mesh(new THREE.SphereGeometry(0.008, 8, 6), glow); f.scale.y = 1.8; f.position.copy(v3(R.W - sb.d / 2 - 2, sb.top + h + 1.2, z)); g.add(f); });
    shell.add(g); }
  { const g = SUGG_G.runner = new THREE.Group(), linen = mat("#e6dccb"); SVAR_MATS.runner = [linen];
    lb(g, 0, 0, 0, 180, 0.4, 33, linen);
    const v = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.04, 0.2, 18), reg(new THREE.MeshStandardMaterial({ color: "#7a8a6a", roughness: 0.35 }))); v.position.copy(v3(0, 10.4, 0)); g.add(shadow(v));
    for (let i = 0; i < 5; i++) { const st = new THREE.Mesh(new THREE.CylinderGeometry(0.002, 0.002, 0.18, 4), leaf); st.position.copy(v3((i - 2) * 1.2, 27, (i % 2) * 1.5)); st.rotation.z = (i - 2) * 0.12; g.add(st);
      const fl = new THREE.Mesh(new THREE.SphereGeometry(0.014, 8, 6), mat(["#efe7d8", "#d9a441", "#c7643a"][i % 3])); fl.position.copy(v3((i - 2) * 3.4, 36, (i % 2) * 1.5)); g.add(fl); }
    shell.add(g); }
  { const a = mat("#d9a441"), b = mat("#c7643a"); SVAR_MATS.floorcush = [a, b];
    floor("floorcush", "Floor cushions (suggested)", 60, 60, 118, -98, g => {
      const c1 = new THREE.Mesh(new RoundedBoxGeometry(0.6, 0.12, 0.6, 3, 0.04), a); c1.position.y = 0.06; g.add(shadow(c1));
      const c2 = new THREE.Mesh(new RoundedBoxGeometry(0.58, 0.12, 0.58, 3, 0.04), b); c2.position.y = 0.18; c2.rotation.y = 0.2; g.add(shadow(c2)); }, [a, b]); }
  { const rattan = mat("#b98f5c"), weave = reg(new THREE.MeshStandardMaterial({ color: "#b98f5c", roughness: 0.9, transparent: true, opacity: 0.82, side: THREE.DoubleSide }));
    SVAR_MATS.lantern = [rattan, weave];
    floor("lantern", "Rattan lantern (suggested)", 30, 30, 325, -283, g => {
      const body = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.13, 0.48, 24, 1, true), weave);
      body.position.y = 0.26; g.add(body);
      const top = new THREE.Mesh(new THREE.ConeGeometry(0.16, 0.07, 24), rattan); top.position.y = 0.535; g.add(shadow(top));
      const c = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.12, 16), reg(new THREE.MeshStandardMaterial({ color: "#f3ecdc", emissive: "#ffb35a", emissiveIntensity: 0.9 }))); c.position.y = 0.08; g.add(c); }, [rattan, weave]); }
  { const g = SUGG_G.mirror = new THREE.Group(), z = R.WINDOW_Z + 1.2, x0 = 14, w = 50, y0 = 108, h = 90;
    const glass = reg(new THREE.MeshStandardMaterial({ color: "#cfdbe0", roughness: 0.05, metalness: 0.6 }));
    const sh = new THREE.Shape(); sh.moveTo(0, 0); sh.lineTo(w, 0); sh.lineTo(w, h - w / 2); sh.absarc(w / 2, h - w / 2, w / 2, 0, Math.PI, false); sh.lineTo(0, 0);
    SVAR_MATS.mirror = [ownOak()]; const fr = new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: 2.2, bevelEnabled: false }), SVAR_MATS.mirror[0]); fr.scale.set(-M, M, M); fr.position.copy(v3(x0, y0, z)); g.add(shadow(fr));
    const inner = new THREE.Shape(); const iw = w - 6, ih = h - 6; inner.moveTo(0, 0); inner.lineTo(iw, 0); inner.lineTo(iw, ih - iw / 2); inner.absarc(iw / 2, ih - iw / 2, iw / 2, 0, Math.PI, false); inner.lineTo(0, 0);
    const gl_ = new THREE.Mesh(new THREE.ShapeGeometry(inner), glass); gl_.scale.set(-M, M, M); gl_.position.copy(v3(x0 + 3, y0 + 3, z + 2.4)); g.add(gl_);
    shell.add(g); }
  { const g = SUGG_G.shelfled = new THREE.Group(), sb = R.SHELF_B;
    SVAR_MATS.shelfled = [ownGlow("#ffd59a")]; const strip = new THREE.Mesh(new THREE.BoxGeometry(0.01, 0.004, (sb.z[0] - sb.z[1] - 4) * M), SVAR_MATS.shelfled[0]); strip.position.copy(v3(R.W - sb.d + 2, sb.top - sb.t - 0.3, (sb.z[0] + sb.z[1]) / 2)); g.add(strip);
    const pl = new THREE.PointLight("#ffd29a", 1.2, 2.2, 2); SVAR_MATS.shelfled.push(pl); pl.position.copy(v3(R.W - sb.d / 2, sb.top - sb.t - 8, (sb.z[0] + sb.z[1]) / 2)); g.add(pl);
    shell.add(g); }
  SVAR_MATS.basket = [mat("#b89a6c")];
  floor("basket", "Seagrass basket (suggested)", 40, 40, 322, -70, g => {
    const sea = SVAR_MATS.basket[0], b = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.17, 0.4, 28, 1, true), sea); sea.side = THREE.DoubleSide; b.position.y = 0.2; g.add(shadow(b));
    lb(g, 0, 0, 0, 32, 1, 32, sea);
    const roll = new THREE.Mesh(new THREE.SphereGeometry(0.15, 16, 12), mat("#7a8a6a")); roll.scale.set(1, 0.6, 1); roll.position.y = 0.41; g.add(shadow(roll)); }, SVAR_MATS.basket);
}
/* v23: the fold-down oak seat in the gap at the stair end (an option, geometry.WALL_SEAT), and your sofa's square ottoman */
let seatUp = null, seatDown = null;
function buildSeatAndPouf() {
  const S_ = R.WALL_SEAT, W = R.W, [za, zb] = S_.z, w = za - zb;
  const oak = reg(new THREE.MeshStandardMaterial({ color: "#c48c57", map: OAK_TEX, roughness: 0.55 }));
  const steel = reg(new THREE.MeshStandardMaterial({ color: "#7c7a74", roughness: 0.5, metalness: 0.5 }));
  seatUp = new THREE.Group(); seatDown = new THREE.Group();
  for (const z of [zb + 6, za - 6 - 8.2]) {
    ibox(seatUp, W - S_.fold, S_.h - 20, z, S_.fold, 30, 8.2, steel);
    ibox(seatDown, W - S_.fold, S_.h - 32, z, S_.fold, 29, 8.2, steel);          // the bracket's wall plate, under the seat
    const A = v3(W - 0.5, S_.h - 28, z + 4.1), B = v3(W - S_.d + 4, S_.h - S_.t, z + 4.1), dv = B.clone().sub(A);   // the bracket's arm: wall to the seat's front
    const arm = new THREE.Mesh(new THREE.BoxGeometry(dv.length(), 0.025, 0.025), steel);
    arm.position.copy(A.clone().add(B).multiplyScalar(0.5)); arm.rotation.z = Math.atan2(dv.y, dv.x); seatDown.add(arm);
  }
  ibox(seatUp, W - S_.fold - S_.t, S_.h - 2, zb, S_.t, S_.d, w, oak);                  // folded: standing up against its brackets
  ibox(seatDown, W - S_.d, S_.h - S_.t, zb, S_.d - 0.5, S_.t, w, oak);                // down: a seat at 46
  shell.add(seatUp, seatDown);
  // the ottoman: blue corduroy like the sofa, movable in Edit room
  const P_ = R.SOFA_POUF, cord = reg(new THREE.MeshStandardMaterial({ color: R.SOFA_CORD[0], roughness: 0.9, bumpMap: CORD, bumpScale: 0.9 }));
  const g = new THREE.Group(), body = new THREE.Mesh(new RoundedBoxGeometry(P_.w * M, (P_.h - 4) * M, P_.d * M, 4, 0.04), cord);
  body.position.y = (P_.h - 4) / 2 * M + 0.04; g.add(shadow(body));
  for (const [x, z] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) lb(g, x * (P_.w / 2 - 6), 0, z * (P_.d / 2 - 6), 4, 4, 4, reg(new THREE.MeshStandardMaterial({ color: "#1b1c1f", roughness: 0.5 })));
  movable("pouf", "Your sofa's ottoman", g, () => ({ x: (P_.x[0] + P_.x[1]) / 2, z: (P_.z[0] + P_.z[1]) / 2, rot: 0 }), P_.w, P_.d, [cord], false,
          { when: () => !(S.site === "C" && S.dining !== "folded") });   // v26: it moves aside while the cabinet's table is out
  // v27, client: "add my surround speakers to the build that exist standing behind the sofa": the soundbar's two rears on slim stands
  // behind the sofa's long side, movable in Edit room (drawn to the AX5100G's published size until your photo)
  if (R.REAR_SPK) {
    const [sw, sh, sd] = R.REAR_SPK, ST = R.REAR_STAND, blk = reg(new THREE.MeshStandardMaterial({ color: "#1d1e21", roughness: 0.6 }));
    const grille = reg(new THREE.MeshStandardMaterial({ color: "#2b2c30", roughness: 0.95 })), steel = reg(new THREE.MeshStandardMaterial({ color: "#2a2a2c", roughness: 0.4, metalness: 0.6 }));
    R.REAR_SPOTS.forEach(([x, z], i) => {
      const g = new THREE.Group();
      lb(g, 0, 0, 0, ST.base[0], ST.base[2], ST.base[1], steel);                     // the weighted base
      lb(g, 0, ST.base[2], 0, ST.pole, ST.top - ST.base[2] - 0.8, ST.pole, steel);   // the pole
      lb(g, 0, ST.top - 0.8, 0, sw + 1, 0.8, sd, steel);                             // the top plate
      lb(g, 0, ST.top, 0, sw, sh, sd, blk);                                          // the speaker
      lb(g, 0, ST.top + 0.8, sd / 2 - 0.2, sw - 1.2, sh - 1.6, 0.6, grille);         // its grille, facing the room
      movable("rear" + (i + 1), i ? "Rear speaker, right" : "Rear speaker, left", g, () => ({ x, z, rot: 0 }), Math.max(ST.base[0], sw), Math.max(ST.base[1], sd), [blk]);
    });
  }
}
function applySuggest() {
  if (seatUp) { seatUp.visible = S.seat === "up" && S.site !== "C"; seatDown.visible = S.seat === "down" && S.site !== "C"; }
  for (const k of ["art", "clock", "tray", "fairy", "hanger", "trail", "throw", "pclamp", "candles", "mirror", "shelfled"]) if (SUGG_G[k]) SUGG_G[k].visible = !!S.sugg[k];
  // v26: the runner lies down the middle of whichever table is open
  const rn = SUGG_G.runner;
  if (rn) {
    rn.visible = !!S.sugg.runner && S.dining !== "folded";
    const y = 76.3;
    if (S.site === "C") { const C = cabC(); rn.position.copy(v3((C.tx[0] + C.tx[1]) / 2, y, C.cz)); rn.rotation.y = 0; rn.scale.set((C.len_open || C.len) / 225, 1, 1); }
    else if (S.site === "B") { rn.position.copy(v3((R.TABLE_B_OPEN_X[0] + R.TABLE_B_OPEN_X[1]) / 2, y, R.TABLE_B.cz)); rn.rotation.y = 0; rn.scale.set(0.78, 1, 1); }
    else { rn.position.copy(v3(R.TABLE_A.cx, y, (R.OPEN_Z[0] + R.OPEN_Z[1]) / 2)); rn.rotation.y = Math.PI / 2; rn.scale.set(0.78, 1, 1); }
  }
}
const CASE_FILLS = {}, cushM = [];
const CUSHION_COLS = { rust: ["#c7643a", "#d9a441", "#efe7d8"], blues: ["#2f4a6e", "#9fb4cc", "#e9e3d3"], sage: ["#7a8a6a", "#efe7d8", "#b9a47f"] };
const PAD_COLS = { olive: "#7c7a4c", honey: "#c99a4c", ivory: "#e8e0cd", blue: "#6d8cac" };   // v31: the seat pads
const CURTAIN_COLS = { hessian: R.CURTAIN.col, linen: "#e6e0d2", sage: "#8b9878", blue: "#34507f", rust: "#a65a38" };
const CASE_FRAMES = { oak: ["#c48c57", true, 0.55], black: ["#1f1f21", false, 0.45], white: ["#eeebe4", false, 0.5] };
function pillow(w, h, t) {          // a plump cushion: a box whose faces swell in the middle and pinch at the seams
  const g = new THREE.BoxGeometry(w * M, h * M, t * M, 10, 10, 2), p = g.attributes.position;
  for (let i = 0; i < p.count; i++) { const u = p.getX(i) / (w * M / 2), v = p.getY(i) / (h * M / 2); p.setZ(i, p.getZ(i) * (1 - 0.7 * Math.max(u * u, v * v))); }
  g.computeVertexNormals(); return g;
}
function buildCushions(sofa) {      // three scatter cushions and a throw over the arm, in the colourway picked (or none)
  const so = R.SOFA, zf = so.back + 36, st = 52;
  cushG = new THREE.Group(); cushM.length = 0;
  for (let i = 0; i < 3; i++) cushM.push(reg(new THREE.MeshStandardMaterial({ color: "#c7643a", roughness: 0.95, map: HESSIAN })));
  const put = (x, z, col, ry, tilt) => { const m = new THREE.Mesh(pillow(42, 42, 14), cushM[col]); m.position.copy(v3(x, st + 19, z));
    m.rotation.order = "YXZ"; m.rotation.y = ry; m.rotation.x = tilt; cushG.add(shadow(m)); };
  put(so.chaise_x[1] + 26, zf + 6, 0, 0, -0.32); put(so.chaise_x[1] + 72, zf + 6, 1, 0.12, -0.3);   // the long side's two seats
  put(so.x[1] - 48, zf + 6, 2, -0.1, -0.3);
  put(so.x[0] + 45, (zf + so.front) / 2 + 30, 1, -Math.PI / 2, -0.32);                                // the corner, leaning on the return's back
  const th = new THREE.Mesh(new THREE.BoxGeometry(24 * M, 0.012, 46 * M), cushM[2]); th.position.copy(v3(so.x[1] - 10, 62.6, so.back + 50)); cushG.add(shadow(th));
  const hang = new THREE.Mesh(new THREE.BoxGeometry(0.012, 30 * M, 46 * M), cushM[2]); hang.position.copy(v3(so.x[1] + 0.8, 48, so.back + 50)); cushG.add(shadow(hang));
  sofa.add(cushG);
}
function applyDecor() {
  const D = S.decor;
  if (rugMesh) { rugMesh.visible = D.rug !== "none"; const top = rugMesh.material[2], t = rugTex(D.rug), edge = (RUG_LOOKS[D.rug] || {}).edge || R.RUG.cols[3];
    if (top.map !== t) { top.map = t; top.needsUpdate = true; } rugMesh.material.forEach((m, i) => { if (i !== 2) m.color.set(edge); }); }
  if (curtCloth) curtCloth.color.set(CURTAIN_COLS[D.curtains] || CURTAIN_COLS.hessian);
  if (cushG) { const c = CUSHION_COLS[D.cushions]; cushG.visible = !!c; if (c) cushM.forEach((m, i) => m.color.set(c[i])); }
  if (CK) CK.pad.color.set(PAD_COLS[D.pads] || PAD_COLS.olive);                                   // v31: the chairs' tie-on pads (Dunelm Esme's colours)
  applySuggest();
  for (const [k, g] of Object.entries(CASE_FILLS)) g.visible = k === (D.fill in CASE_FILLS ? D.fill : "collect");
  if (caseFrameM) { const [col, oakMap, ro] = CASE_FRAMES[D.frame] || CASE_FRAMES.oak, mp = oakMap ? OAK_TEX : null;
    caseFrameM.color.set(col); caseFrameM.roughness = ro; if (caseFrameM.map !== mp) { caseFrameM.map = mp; caseFrameM.needsUpdate = true; } }
  // v26: the oak's finish on every new oak piece (not your plant stand, vinyl stand, curtain pole or the stairs)
  const tint = OAK_TINTS[D.oak] || OAK_TINTS.artisan;
  for (const m of MATS) if ((m.map === OAK_TEX || m.map === OAK_TEX_V) && !m.userData.noTint && m !== caseFrameM) {
    if (!m.userData.oakBase) m.userData.oakBase = m.color.clone();
    m.color.copy(m.userData.oakBase).multiply(tint);
  }
  if (floorMat) { const f = FLOORS[D.floor] || FLOORS.carpet; if (floorMat.map !== f[0]) { floorMat.map = f[0]; floorMat.bumpMap = f[1]; floorMat.roughness = f[2]; floorMat.needsUpdate = true; } }
  if (shelfMat) { const [c, ro, oakM] = SHELF_COLS[D.shelf] || SHELF_COLS.black, mp = oakM ? OAK_TEX : null;
    shelfMat.color.set(c).multiply(oakM ? tint : new THREE.Color(1, 1, 1)); shelfMat.roughness = ro; if (shelfMat.map !== mp) { shelfMat.map = mp; shelfMat.needsUpdate = true; } }
}
const srgb = (r, g, b) => new THREE.Color().setRGB(r, g, b, THREE.SRGBColorSpace);   // the tints as you'd see them, not in linear light
const OAK_TINTS = { artisan: srgb(1, 1, 1), pale: srgb(1.12, 1.09, 1.03), smoked: srgb(0.66, 0.57, 0.5), walnut: srgb(0.55, 0.42, 0.34) };
const FLOORS = { carpet: [CARPET, PILE, 1], oatmeal: [OATMEAL, PILE, 1], boards: [BOARDS, null, 0.55] };
const SHELF_COLS = { black: ["#1a1a1b", 0.55, false], oak: ["#c48c57", 0.55, true], white: ["#eeebe4", 0.5, false] };
function ibox(grp, x, y, z, w, h, d, mat, cast = true) {
  const m = new THREE.Mesh(new THREE.BoxGeometry(w * M, h * M, d * M), mat);
  m.position.copy(v3(x + w / 2, y + h / 2, z + d / 2)); grp.add(shadow(m, cast)); return m;
}
function buildIdeas() {
  const I = R.IDEAS, oak = reg(new THREE.MeshStandardMaterial({ color: "#c48c57", map: OAK_TEX, roughness: 0.55 }));
  const glassM = reg(new THREE.MeshPhysicalMaterial({ color: "#dfeef0", roughness: 0.04, transparent: true, opacity: 0.22, depthWrite: false }));
  const steel = reg(new THREE.MeshStandardMaterial({ color: "#9a9ea3", metalness: 0.8, roughness: 0.35 }));
  const leaf = reg(new THREE.MeshStandardMaterial({ color: "#4a8640", roughness: 0.65, side: THREE.DoubleSide }));
  const potM = reg(new THREE.MeshStandardMaterial({ color: "#e4ddcf", roughness: 0.7 })), potT = reg(new THREE.MeshStandardMaterial({ color: "#b5643f", roughness: 0.75 }));
  const r = rnd(41);
  const plant = (grp, x, y, z, rad, trail) => {          // a pot with leaves on top, and a few trailing strands if asked
    const p = new THREE.Mesh(new THREE.CylinderGeometry(rad * M, rad * 0.78 * M, rad * 1.6 * M, 16), r() < 0.5 ? potM : potT);
    p.position.copy(v3(x, y + rad * 0.8, z)); grp.add(shadow(p));
    const gs = [];
    for (let k = 0; k < 10; k++) { const g = new THREE.SphereGeometry((0.018 + r() * 0.01), 7, 5); g.scale(0.7, 0.5, 0.3); g.rotateY(r() * 3);
      const q = v3(x + (r() - 0.5) * rad * 1.8, y + rad * 1.6 + 1 + r() * 7, z + (r() - 0.5) * rad * 1.4); g.translate(q.x, q.y, q.z); gs.push(g); }
    for (let s = 0; s < trail; s++) { const zz = z + (r() - 0.5) * rad, xx = x + (r() - 0.5) * rad * 1.6, len = 14 + r() * 22;
      for (let t = 0; t < len; t += 3.2) { const g = new THREE.SphereGeometry(0.014, 6, 4); g.scale(0.8, 0.45, 0.4); g.rotateY(r() * 3);
        const q = v3(xx + Math.sin(t / 5 + s) * 1.5, y + rad * 1.4 - t, zz + rad * 0.9); g.translate(q.x, q.y, q.z); gs.push(g); } }
    grp.add(shadow(new THREE.Mesh(mergeGeometries(gs), leaf)));
  };
  // 1. the tall glass display case on the breast (it faces the room: the breast's face is z = 0). v20, client: "make glass display
  // cabinet on wall taller and give more decor variation and options": 85 tall (was 50), three glass shelves, five things to put in
  // it and three frame finishes (Decor), each fill built once and shown on its own
  { const g = IDEA_G.case = new THREE.Group(), C = I.case, [x0, x1] = C.x, [y0, y1] = C.y, d = C.d, f = C.frame, z0 = -d;
    caseFrameM = reg(new THREE.MeshStandardMaterial({ color: "#c48c57", map: OAK_TEX, roughness: 0.55 }));
    ibox(g, x0, y0, -1, x1 - x0, y1 - y0, 1, caseFrameM);                            // the back
    ibox(g, x0, y0, z0, f, y1 - y0, d - 1, caseFrameM); ibox(g, x1 - f, y0, z0, f, y1 - y0, d - 1, caseFrameM);
    ibox(g, x0, y0, z0, x1 - x0, f, d - 1, caseFrameM); ibox(g, x0, y1 - f, z0, x1 - x0, f, d - 1, caseFrameM);
    for (const y of C.shelves) ibox(g, x0 + f, y - 0.3, z0 + 1, x1 - x0 - 2 * f, 0.6, d - 2, glassM, false);   // three 6 mm glass shelves
    ibox(g, x0, y0, z0 - 0.4, x1 - x0, y1 - y0, 0.4, glassM, false);                       // the toughened glass front
    ideaLed = new THREE.MeshBasicMaterial({ color: "#fff1d6", toneMapped: false });
    ibox(g, x0 + f, y1 - f - 0.5, z0 + 2, x1 - x0 - 2 * f, 0.5, 1.2, ideaLed, false);
    const pal = ["#1d2a4a", "#a33b2b", "#e2c35a", "#2f6b5a", "#d9d4c7", "#d0682f", "#6c4a8a", "#1b1c1f", "#f2efe6", "#3a78b5"]
      .map(c => reg(new THREE.MeshStandardMaterial({ color: c, roughness: 0.6 })));
    const glaze = ["#e8e2d4", "#9bb0a0", "#c7643a", "#2f4a6e", "#d9a441"].map(c => reg(new THREE.MeshStandardMaterial({ color: c, roughness: 0.3 })));
    const disc = reg(new THREE.MeshStandardMaterial({ color: "#121214", roughness: 0.35 }));
    const xa = x0 + f + 1.5, xb = x1 - f - 1.5, bases = [y0 + f, ...C.shelves.map(y => y + 0.3)];
    const tops = [...C.shelves.map(y => y - 0.3), y1 - f - 0.6], zb = -2, rr = rnd(77);
    const cyl = (grp, x, y, z, rt, rb, h, mat, seg = 18) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(rt * M, rb * M, h * M, seg), mat); m.position.copy(v3(x, y + h / 2, z)); grp.add(shadow(m)); return m; };
    const ball = (grp, x, y, z, rad, mat, sy = 1) => { const m = new THREE.Mesh(new THREE.SphereGeometry(rad * M, 16, 12), mat); m.scale.y = sy; m.position.copy(v3(x, y + rad * sy, z)); grp.add(shadow(m)); return m; };
    const TIER = {
      figs(grp, yb, h, i) {             // boxed figures and a few out of their boxes
        let x = xa + 2; for (let k = 0; x < xb - 10; k++) { const w = 7 + (k % 3) * 2, hh = Math.min(h - 2, 11 + ((k + i) % 3) * 3);
          if (k % 2) { ibox(grp, x, yb, z0 + 3, w, hh, 5, pal[(k + i) % 10]); ibox(grp, x + 1, yb + 2, z0 + 2.9, w - 2, hh - 5, 0.1, glassM, false); }
          else { cyl(grp, x + w / 2, yb, -6, 2.4, 2.8, hh - 5, pal[(k + i + 3) % 10]); ball(grp, x + w / 2, yb + hh - 5, -6, 2.4, pal[4]); }
          x += w + 4; } },
      cap(grp, yb, h, i) {              // a cap on its button top, and two figures
        const cap = new THREE.Mesh(new THREE.SphereGeometry(0.07, 20, 10, 0, Math.PI * 2, 0, Math.PI / 2), pal[0]); cap.position.copy(v3(xa + 16, yb, -6.5)); grp.add(shadow(cap));
        const brim = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.006, 0.05), pal[0]); brim.position.copy(v3(xa + 16, yb + 0.3, z0 + 3)); grp.add(brim);
        for (const [x, c] of [[xa + 42, 1], [xa + 58, 3]]) { cyl(grp, x, yb, -6, 2.6, 3, 9, pal[c]); ball(grp, x, yb + 9, -6, 2.6, pal[4]); }
        ibox(grp, xa + 68, yb, z0 + 3, 12, 14, 5, pal[2]); },
      games(grp, yb, h, i) {            // boxed games face-out on little stands, a label band on each
        let x = xa + 1; for (let k = 0; x < xb - 14; k++) { const c = pal[(k * 3 + i) % 10];
          const m = ibox(grp, x, yb, -5.5, 13.5, Math.min(h - 1.5, 17), 1.6, c); m.rotation.x = -0.12;
          ibox(grp, x + 1, yb + 12, -5.65, 11.5, 2.4, 0.1, pal[k % 2 ? 8 : 7], false); x += 16.5; } },
      console(grp, yb, h, i) {          // a handheld, its cartridges, a pad
        ibox(grp, xa + 6, yb, -7, 9, 15, 3, pal[4]); ibox(grp, xa + 7.5, yb + 8, -7.1, 6, 5, 0.1, disc, false);
        for (let k = 0; k < 6; k++) ibox(grp, xa + 22 + k * 6.5, yb, -8, 5.7, 6.5, 0.8, pal[(k + 1) % 10]);
        ibox(grp, xa + 64, yb, -9, 15, 3, 6, pal[7]); ball(grp, xa + 66, yb + 1, -6, 2.4, pal[7], 0.6); ball(grp, xa + 76, yb + 1, -6, 2.4, pal[7], 0.6); },
      singles(grp, yb, h, i) {          // 7-inch singles face-out, a record peeking out of one
        for (let k = 0; k < 4; k++) { const x = xa + 1 + k * 21.5, m = ibox(grp, x, yb, -5, 18, 18, 0.4, pal[(k * 2 + i * 3 + 1) % 10]); m.rotation.x = -0.1;
          if ((k + i) % 3 === 0) { const r = new THREE.Mesh(new THREE.CylinderGeometry(0.0875, 0.0875, 0.002, 28), disc); r.rotation.x = Math.PI / 2; r.position.copy(v3(x + 13, yb + 9.4, -3.6)); grp.add(r); } } },
      tapes(grp, yb, h, i) {            // cassettes stacked flat and a row stood up, and a small speaker
        for (let s = 0; s < 3; s++) for (let k = 0; k < 6 - s; k++) ibox(grp, xa + 2 + s * 13, yb + k * 1.75, -9, 11, 1.7, 7, pal[(k + s * 2) % 10]);
        for (let k = 0; k < 6; k++) ibox(grp, xa + 44 + k * 2, yb, -8, 1.7, 11, 7, pal[(k + 5) % 10]);
        ibox(grp, xa + 62, yb, -9, 14, 14, 7, pal[7]); cyl(grp, xa + 69, yb + 4, -9.1, 3.5, 3.5, 0.2, pal[4]); },
      plants(grp, yb, h, i) {           // small pots, two trailing over the shelf's edge
        [0.08, 0.3, 0.55, 0.78, 0.95].forEach((t, k) => plant(grp, xa + 4 + t * (xb - xa - 8), yb, -6, 3.2 + (k % 2), k === 0 || k === 4 ? 1 : 0)); },
      ceramics(grp, yb, h, i) {         // vases, a bud vase and a bowl in mixed glazes
        let x = xa + 4; for (let k = 0; x < xb - 6; k++) { const gz = glaze[(k + i) % glaze.length], kind = (k + i) % 3;
          if (kind === 0) { cyl(grp, x + 3, yb, -6, 2.2, 3.4, Math.min(h - 2, 14), gz); x += 12; }
          else if (kind === 1) { ball(grp, x + 4, yb, -6, 4, gz, 1.1); cyl(grp, x + 4, yb + 8.4, -6, 1, 1.2, 3, gz); x += 13; }
          else { cyl(grp, x + 5, yb, -6, 5, 3, 4, gz); x += 14; } } },
    };
    const PRESETS = { collect: ["figs", "cap", "figs", "ceramics"], games: ["console", "games", "games", "games"], singles: ["tapes", "singles", "singles", "singles"],
                      plants: ["ceramics", "plants", "ceramics", "plants"], mixed: ["singles", "cap", "plants", "games"] };
    for (const [k, tiers] of Object.entries(PRESETS)) {
      const fg = CASE_FILLS[k] = new THREE.Group();
      tiers.forEach((t, i) => TIER[t](fg, bases[i], tops[i] - bases[i], i));
      fg.visible = k === "collect"; g.add(fg);
    }
    shell.add(g); }
  // 2. glass plant shelves across the window's reveal, on studs and a slim rod from the head
  { const g = IDEA_G.glass = new THREE.Group(), GL = I.glass, [wx0, wx1] = GL.x, FZ = R.WINDOW_Z - R.WINDOW_REVEAL, wz = R.WINDOW_Z, mid = (wx0 + wx1) / 2;
    for (const y of GL.ys) {
      ibox(g, wx0, y - GL.t, wz - GL.d, wx1 - wx0, GL.t, GL.d - 0.5, glassM, false);
      for (const x of [wx0 + 0.5, wx1 - 1.5]) ibox(g, x, y - GL.t - 0.8, wz - GL.d / 2 - 1, 1, 0.8, 2, steel, false);
      [0.12, 0.3, 0.52, 0.7, 0.88].forEach((t, i) => plant(g, wx0 + 8 + t * (wx1 - wx0 - 16), y, wz - GL.d / 2, 4 + (i % 2) * 1.5, i % 2 ? 3 : 1));
    }
    const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.004, 0.004, (R.WINDOW_Y[1] - GL.ys[0] + GL.t) * M, 8), steel);
    rod.position.copy(v3(mid, (R.WINDOW_Y[1] + GL.ys[0] - GL.t) / 2, wz - GL.d + 1.5)); g.add(rod);
    shell.add(g); }
  // 3. the oak C-table over the sofa's open end: its top reaches over the seat, its foot on the floor beside it
  { const g = IDEA_G.ctable = new THREE.Group(), T = I.ctable, [x0, x1] = T.x, ze = R.SOFA.end, t = T.t;
    const zo = ze + T.depth - T.over;                                               // the upright's outer face, out from the sofa's end
    ibox(g, x0, T.top - t, ze - T.over, x1 - x0, t, T.depth, oak);                // the top
    ibox(g, x0, 0, zo - t, x1 - x0, T.top - t, t, oak);                           // the upright
    ibox(g, x0, 0, ze - 3, x1 - x0, 1.6, zo - ze + 3 - t, oak);                    // the foot, just under the plinth's 3 cm inset
    const glassCup = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.03, 0.1, 16), glassM); glassCup.position.copy(v3(x0 + 14, T.top + 5, ze - 2)); g.add(glassCup);
    ibox(g, x1 - 20, T.top, ze - 6, 15, 4, 10, reg(new THREE.MeshStandardMaterial({ color: "#1b1c1f", roughness: 0.5 })));   // a pad
    shell.add(g); }
  Object.values(IDEA_G).forEach(gr => gr.visible = false);
}
let view, ledMat, ceilGlow, ceilMat, lboxFace, laserDots, runLed, curtOpen, curtShut, pcGlow, pcLight;
// v17: the PC lit up behind its clear side window: glowing fan rings (three front, one rear), an RGB strip along the top, a light inside
function pcLit() {
  const [cw, ch, cd] = R.PC_CASE, [cz1, cz0] = R.PC_Z, st = R.PC_SHELF_TOP, x = 2.5 + cw - 4.2;
  pcGlow = new THREE.Group();
  const ringM = new THREE.MeshBasicMaterial({ color: "#3fe3b0", toneMapped: false }), rgbM = new THREE.MeshBasicMaterial({ color: "#b46cff", toneMapped: false });
  const ring = (y, z, r) => { const m = new THREE.Mesh(new THREE.TorusGeometry(r * M, 0.0035, 8, 32), ringM); m.position.copy(v3(x, y, z)); m.rotation.y = Math.PI / 2; pcGlow.add(m); };
  for (const y of [st + 11, st + 23.5, st + 36]) ring(y, cz1 - 2.6, 5.2);
  ring(st + 36, cz0 + 2.2, 4.8);
  const strip = new THREE.Mesh(new THREE.BoxGeometry(0.004, 0.006, (cd - 6) * M), rgbM); strip.position.copy(v3(2.5 + cw - 1.5, st + ch - 2, (cz0 + cz1) / 2)); pcGlow.add(strip);
  const ramM = new THREE.MeshBasicMaterial({ color: "#ff5ad1", toneMapped: false });
  for (let k = 0; k < 4; k++) { const r = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.004, 0.007), ramM); r.position.copy(v3(4.5, st + 37.2, cz0 + 21.85 + k * 1.3)); pcGlow.add(r); }
  shell.add(pcGlow);
  pcLight = new THREE.PointLight("#9d7bff", 3, 0.6, 2); pcLight.position.copy(v3(2.5 + cw / 2, st + ch / 2, (cz0 + cz1) / 2)); shell.add(pcLight);
}
// v17: "i also have deep window sills that allow for lots of plants there": a row of pots along the sill, upright and trailing
function sillPlants(x0, x1, y, zBack, zFront) {
  const r = rnd(29), pots = [], leaves = [], vines = [];
  const potCols = ["#d8cfc0", "#b5643f", "#2f2f2f", "#e9e4da", "#8a9a7b"], potMs = potCols.map(c => reg(new THREE.MeshStandardMaterial({ color: c, roughness: 0.7 })));
  const leaf = reg(new THREE.MeshStandardMaterial({ color: "#3f7a3a", roughness: 0.65, side: THREE.DoubleSide })), leaf2 = reg(new THREE.MeshStandardMaterial({ color: "#5d8f45", roughness: 0.65, side: THREE.DoubleSide }));
  const vine = reg(new THREE.MeshStandardMaterial({ color: "#4f6b3a", roughness: 0.8 }));
  const n = 7, zc = (zBack + zFront) / 2, step = (x1 - x0 - 30) / (n - 1), leaves2 = [];
  for (let i = 0; i < n; i++) {
    const x = x0 + 15 + i * step + (r() - 0.5) * 6, rad = 5 + r() * 4, h = 9 + r() * 6, z = zc + (r() - 0.5) * 6;
    const p = new THREE.Mesh(new THREE.CylinderGeometry(rad * M, rad * 0.78 * M, h * M, 20), potMs[i % potMs.length]);
    p.position.copy(v3(x, y + h / 2, z)); shell.add(shadow(p));
    const tall = i % 3 !== 1, top = y + h;
    if (tall) {                 // an upright plant: a cluster of leaves on short stems
      const H = 14 + r() * 26;
      for (let k = 0; k < 16; k++) {
        const t = k / 16, g = new THREE.SphereGeometry((0.022 + r() * 0.012) * (1.2 - t * 0.5), 8, 6); g.scale(0.55, 1.3, 0.25);
        g.rotateZ((r() - 0.5) * 1.1); g.rotateY(r() * Math.PI);
        const q = v3(x + (r() - 0.5) * rad * 1.6, top + 3 + t * H, z + (r() - 0.5) * rad * 1.2); g.translate(q.x, q.y, q.z);
        (k % 2 ? leaves : leaves2).push(g);
      }
    } else {                    // a trailing one, hanging a little over the sill's nose
      for (let k = 0; k < 5; k++) {
        const z0 = z + (r() - 0.5) * 6, len = 10 + r() * 14;
        const pts = [v3(x + (r() - 0.5) * 4, top + 2, z0), v3(x + (r() - 0.5) * 6, top, zFront + 1)];
        for (let j = 1; j <= 4; j++) pts.push(v3(x + (r() - 0.5) * 8, y - len * j / 4, zFront + 1.5 + j * 0.4));
        const curve = new THREE.CatmullRomCurve3(pts);
        vines.push(new THREE.TubeGeometry(curve, 24, 0.002, 5, false));
        for (let t = 0.1; t < 1; t += 0.09 + r() * 0.04) {
          const q = curve.getPoint(t), g = new THREE.SphereGeometry(0.02 + r() * 0.008, 8, 6); g.scale(1, 0.2, 0.8); g.rotateY(r() * Math.PI); g.translate(q.x, q.y, q.z); leaves.push(g);
        }
      }
    }
  }
  if (leaves.length) shell.add(shadow(new THREE.Mesh(mergeGeometries(leaves), leaf)));
  if (leaves2.length) shell.add(shadow(new THREE.Mesh(mergeGeometries(leaves2), leaf2)));
  if (vines.length) shell.add(new THREE.Mesh(mergeGeometries(vines), vine));
}

/* ---------------------------------------------------------------- lights */
const lights = { strip: [], uprights: [], bias: [], bar1: [], bar2: [], lamp: [], tv: [] };
const hemi = new THREE.HemisphereLight("#e2e0da", "#b39a7c", 0.05); scene.add(hemi);
function area(color, w, h, pos, look) {
  const l = new THREE.RectAreaLight(color, 1, w * M, h * M);
  l.position.copy(v3(...pos)); l.lookAt(v3(...look)); scene.add(l); return l;
}
function buildLights() {
  const C = R.CEIL, Wd = R.W, WZ = R.WINDOW_Z, AD = R.ALC_D;
  const warm = "#ffe0bf";
  // the strip washes each wall from the ceiling's edge
  lights.strip.push(area(warm, AD - WZ, 6, [4, C - 4, (AD + WZ) / 2], [4, 0, (AD + WZ) / 2]));
  lights.strip.push(area(warm, Wd, 6, [Wd / 2, C - 4, WZ + 4], [Wd / 2, 0, WZ + 4]));
  lights.strip.push(area(warm, R.STAIR_FRONT - WZ, 6, [Wd - 4, C - 4, (R.STAIR_FRONT + WZ) / 2], [Wd - 4, 0, (R.STAIR_FRONT + WZ) / 2]));
  lights.strip.push(area(warm, R.WELL_X0, 6, [R.WELL_X0 / 2, C - 4, -4], [R.WELL_X0 / 2, 0, -4]));
  lights.strip.forEach(l => l.userData.k = 520);
  // the uprights' grooves wash the wall either side of the TV
  for (const x of [2.25, 133.25]) { const l = area("#ffcf96", 2, 112, [x, 134, 22], [x, 134, 40]); l.userData.k = 3500; l.userData.colKey = "strips"; lights.uprights.push(l); }
  // v15: the side run's strip washes the side wall below it
  const SR = R.SIDE_RUN, zr0 = SR.edge[0][1], zr1 = SR.edge[SR.edge.length - 1][1];
  const sw = area("#ffcf96", zr0 - zr1, 3, [9, SR.under - 1, (zr0 + zr1) / 2], [0, SR.under - 60, (zr0 + zr1) / 2]); sw.userData.k = 260; sw.userData.colKey = "strips"; lights.uprights.push(sw);
  // bias light behind the TV, onto the wall
  const [tx0, tx1] = R.TV_X, [ty0, ty1] = R.TV_Y;
  const b = area("#e9efff", tx1 - tx0 - 10, ty1 - ty0 - 10, [(tx0 + tx1) / 2, (ty0 + ty1) / 2, R.TV_Z + 5], [(tx0 + tx1) / 2, (ty0 + ty1) / 2, 60]);
  b.userData.k = 90; lights.bias.push(b);
  // the TV's own light into the room when it's on
  const tvl = area("#ff9d7a", tx1 - tx0, ty1 - ty0, [(tx0 + tx1) / 2, (ty0 + ty1) / 2, R.TV_Z - 0.5], [(tx0 + tx1) / 2, (ty0 + ty1) / 2, -300]);
  tvl.userData.k = 60; lights.tv.push(tvl);
  // the window's daylight (north light, no sun) and the night sky's faint blue
  win = area("#dfe9ff", R.WINDOW_X[1] - R.WINDOW_X[0], R.WINDOW_Y[1] - R.WINDOW_Y[0], [(R.WINDOW_X[0] + R.WINDOW_X[1]) / 2, 150, WZ + 1], [(R.WINDOW_X[0] + R.WINDOW_X[1]) / 2, 140, 0]);
}
let win;
const fixtures = new THREE.Group(); scene.add(fixtures);
const white = new THREE.MeshStandardMaterial({ color: "#f2f0eb", roughness: 0.4 });
const toppers = new THREE.MeshStandardMaterial({ color: "#d6a873", roughness: 0.5, map: OAK_TEX });
const HEADS = {};
function headMat(col) { return HEADS[col] || (HEADS[col] = reg(new THREE.MeshStandardMaterial({ color: col, roughness: 0.5, side: THREE.DoubleSide }))); }
function spotHead(group, apex, dir, col, lightList, kSpot, colKey, shadeMat) {
  const shade = new THREE.Mesh(new THREE.CylinderGeometry(0.019, 0.075, 0.13, 28, 1, true), shadeMat || headMat(col));
  const cap = new THREE.Mesh(new THREE.CylinderGeometry(0.011, 0.019, 0.038, 16), shadeMat || toppers);
  const glow = new THREE.Mesh(new THREE.CircleGeometry(0.06, 24), new THREE.MeshBasicMaterial({ color: "#fff3dc", toneMapped: false }));   // one each: it dims with its own light
  const head = new THREE.Group();
  shade.position.y = -0.065 - 0.038; cap.position.y = -0.019; glow.position.y = -0.155; glow.rotation.x = Math.PI / 2;
  head.add(shade, cap, glow); shadow(shade); shadow(cap, true);
  head.position.copy(apex);
  head.quaternion.setFromUnitVectors(new THREE.Vector3(0, -1, 0), dir);
  group.add(head);
  // v15: "make lighting less spotty": a wider beam with a fully soft edge (was 0.42 rad, penumbra 0.85)
  const sp = new THREE.SpotLight(WARM, 1, 0, 0.66, 1.0, 2);
  sp.position.copy(apex.clone().add(dir.clone().multiplyScalar(0.14)));
  sp.target.position.copy(apex.clone().add(dir.clone().multiplyScalar(3)));
  sp.shadow.mapSize.set(1024, 1024); sp.shadow.bias = -0.0004; sp.shadow.normalBias = 0.02; sp.shadow.camera.near = 0.05; sp.shadow.radius = 6;
  sp.userData = { k: kSpot, glow, colKey };
  scene.add(sp, sp.target); lightList.push(sp);
}
function buildBar(spec, list, colKey) {   // v15: the bar runs along z (TV to window) when spec.axis is "z"
  const g = new THREE.Group(); g.name = "bar";
  const C = R.CEIL, along = spec.axis === "z";
  const at = dx => along ? [spec.x, spec.z + dx] : [spec.x + dx, spec.z];
  const rose = new THREE.Mesh(new THREE.CylinderGeometry(0.065, 0.065, 0.025, 28), white); rose.position.copy(v3(spec.x, C - 1.25, spec.z)); g.add(rose);
  const barM = new THREE.Mesh(along ? new THREE.BoxGeometry(0.022, 0.013, 0.84) : new THREE.BoxGeometry(0.84, 0.013, 0.022), white);
  barM.position.copy(v3(spec.x, C - 3.2, spec.z)); g.add(shadow(barM));
  for (const h of spec.heads) {
    const [hx, hz] = at(h.dx);
    const apex = v3(hx, C - 6.5, hz), tgt = v3(...h.tgt);
    const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.004, 0.004, 0.03, 8), headMat(h.stem));
    stem.position.copy(v3(hx, C - 5, hz)); g.add(stem);
    spotHead(g, apex, tgt.clone().sub(apex).normalize(), h.col, list, 140, colKey);
  }
  fixtures.add(g); return g;
}
let lamp;
const LAMP_RED = new THREE.MeshStandardMaterial({ color: R.LAMP_BODY, roughness: 0.28, metalness: 0.35 });   // v15: "the lamp is bright red"
function buildLamp() {   // three adjustable heads on a red pole, with colour bulbs: green on top, pink, then purple going down
  if (lamp) drop(lamp, lights.lamp);
  const L = S.layout.lamp || {}, d0 = R.LAMP_SPOTS[S.lamp] || R.LAMP_SPOTS[DEF.lamp];
  const spot = { x: L.x ?? d0.x, z: L.z ?? d0.z };                                    // v18: wherever you've dragged it
  const g = new THREE.Group(); lamp = g; g.userData.movId = "lamp"; g.visible = !L.off;
  const red = LAMP_RED;
  const base = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.15, 0.025, 32), red); base.position.copy(v3(spot.x, 1.25, spot.z)); g.add(shadow(base));
  const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.011, 0.011, R.LAMP.h * M, 12), red); pole.position.copy(v3(spot.x, R.LAMP.h / 2, spot.z)); g.add(shadow(pole));
  const toward = new THREE.Vector3(...[233 - spot.x, 0, -135 - spot.z]).normalize();      // the room's middle, in room coords
  // v17, client: "green lamp should face down more slightly, its looking at the ceiling, face at the shelf wall": the top head aims at a
  // point on the stairs wall 30 below its own height, along the shelf (it was aimed 110 up, at the ceiling)
  const sbz = R.SHELF_B.z, wz = Math.min(Math.max(spot.z + 30, Math.min(sbz[0], sbz[1])), Math.max(sbz[0], sbz[1]));
  const aims = [[R.LAMP.h - 8, [R.W - spot.x, -22, wz - spot.z]], [R.LAMP.h - 45, [toward.x * 160, -40, toward.z * 160]], [R.LAMP.h - 80, [toward.x * 90, -110, toward.z * 90]]];
  aims.forEach(([y, off], i) => {
    const apex = v3(spot.x + toward.x * 9, y, spot.z + toward.z * 9);
    const tgt = v3(spot.x + off[0], y + off[1], spot.z + off[2]);
    const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 0.1, 8), red); arm.position.copy(v3(spot.x + toward.x * 5, y, spot.z + toward.z * 5));
    arm.rotation.z = Math.PI / 2; arm.rotation.y = Math.atan2(toward.z, -toward.x); g.add(arm);
    spotHead(g, apex, tgt.clone().sub(apex).normalize(), R.LAMP_BODY, lights.lamp, 55, "lamp" + i, red);
  });
  // v16, the client's photo ("Hat"): the hats live on the lamp: the graduation cap sits on the pole's top, tipped, and the navy cap with
  // the poem printed under its peak hangs on the pole below the top head, peak down, crown out
  if (R.HATS) {
    const H = R.HATS, felt = reg(new THREE.MeshStandardMaterial({ color: "#16171b", roughness: 0.85 }));
    const mb = new THREE.Group();
    const skull = new THREE.Mesh(new THREE.CylinderGeometry(0.085, 0.09, 0.07, 28), felt); skull.position.y = -0.035;
    const board = new THREE.Mesh(new THREE.BoxGeometry(H.board * M, 0.008, H.board * M), felt); board.rotation.y = Math.PI / 4;
    const button = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.006, 12), felt); button.position.y = 0.007;
    const tassel = new THREE.Mesh(new THREE.CylinderGeometry(0.003, 0.006, 0.11, 8), reg(new THREE.MeshStandardMaterial({ color: "#1d1e22", roughness: 0.9 })));
    tassel.position.set(0.1, -0.05, 0.02);
    mb.add(shadow(skull), shadow(board), button, tassel);
    mb.position.copy(v3(spot.x, R.LAMP.h + 5, spot.z)); mb.rotation.z = -0.22; mb.rotation.x = 0.12; g.add(mb);
    const perp = new THREE.Vector3(-toward.z, 0, toward.x);                         // room coords: across the heads
    const out = new THREE.Vector3(-perp.x, 0, perp.z).normalize(), up = new THREE.Vector3(0, 1, 0);   // world
    const cap = new THREE.Group(), navy = reg(new THREE.MeshStandardMaterial({ color: H.cap_col, roughness: 0.8 }));
    const crown = new THREE.Mesh(new THREE.SphereGeometry(0.095, 28, 14, 0, Math.PI * 2, 0, Math.PI / 2), navy); crown.scale.set(1, 0.85, 1.08);
    const peak = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 0.006, 28, 1, false, -Math.PI * 0.32, Math.PI * 0.64), navy);
    peak.position.set(0, 0.0, -0.055); peak.scale.set(1, 1, 0.9);
    const poem = new THREE.Mesh(new THREE.PlaneGeometry(0.11, 0.06), new THREE.MeshStandardMaterial({ map: POEM_TEX, roughness: 0.9 }));
    poem.rotation.x = Math.PI / 2; poem.position.set(0, -0.004, -0.115);
    cap.add(shadow(crown), shadow(peak), poem);
    const xAxis = new THREE.Vector3().crossVectors(out, up);
    cap.quaternion.setFromRotationMatrix(new THREE.Matrix4().makeBasis(xAxis, out, up));
    cap.position.copy(v3(spot.x, H.cap_y, spot.z)).add(out.clone().multiplyScalar(0.02)); g.add(cap);
  }
  fixtures.add(g);
}

/* ---------------------------------------------------------------- the furniture, by state */
const G = {};
let tvScreen;
function buildFurniture() {
  for (const [k, v] of Object.entries(SC.groups)) { G[k] = buildGroup(v, k); G[k].visible = false; scene.add(G[k]); }
  G.fixed.visible = G.frames.visible = true;
  const [tx0, tx1] = R.TV_X, [ty0, ty1] = R.TV_Y;
  tvScreen = new THREE.Mesh(new THREE.PlaneGeometry((tx1 - tx0 - 1.2) * M, (ty1 - ty0 - 1.2) * M), new THREE.MeshStandardMaterial({ color: "#050506", roughness: 0.12, metalness: 0.2 }));
  tvScreen.position.copy(v3((tx0 + tx1) / 2, (ty0 + ty1) / 2, R.TV_Z - 0.1)); tvScreen.rotation.y = Math.PI; scene.add(tvScreen);
  if (G.sofa) {      // v19: the sofa moves too: its group recentred on its footprint and handed to edit mode
    const so = R.SOFA, cx = (so.x[0] + so.x[1]) / 2, cz = (so.back + so.end) / 2, g = G.sofa;
    buildCushions(g);                                                                // v20: cushions to try (Decor), off by default
    scene.remove(g); g.position.set(cx * M, 0, -cz * M); g.visible = true; delete G.sofa;
    movable("sofa", "Your sofa", g, () => ({ x: cx, z: cz, rot: 0 }), so.x[1] - so.x[0], so.end - so.back, []);
  }
}
let bar1, bar2;

/* ---------------------------------------------------------------- apply the options */
function drop(group, list) {   // take a fixture and its lights out of the scene, freeing their GPU memory
  fixtures.remove(group);
  group.traverse(o => { if (o.geometry) o.geometry.dispose(); });
  list.forEach(l => { scene.remove(l, l.target); if (l.shadow && l.shadow.map) l.shadow.map.dispose(); });
  list.length = 0;
}
let built = {};
function applyState() {
  for (const k of Object.keys(G)) if (/^[AB]_/.test(k)) G[k].visible = k === `${S.site}_${S.dining}`;
  G.unit_in.visible = !S.drawers; G.unit_out.visible = S.drawers;
  const b2 = `${S.site === "C" ? "B" : S.site}_${S.site === "C" ? (S.dining === "folded" ? "folded" : "six") : S.dining}`;   // v26: C lights like B
  if (built.bar2 !== b2) { if (bar2) drop(bar2, lights.bar2); bar2 = buildBar(R.BAR2[b2], lights.bar2, "bar2"); built.bar2 = b2; }
  const lk = S.lamp + JSON.stringify(S.layout.lamp || {});
  if (built.lamp !== lk) { buildLamp(); built.lamp = lk; }
  if (G.now_ledge) G.now_ledge.visible = S.site !== "A" && S.plants !== "breast";   // v18: with the plants on the breast the ledge comes off
  placeChairs();                                                                   // v20: the chair cupboard, its doors, the chairs in it
  applyDecor();                                                                    // v20: the rug, cushions, curtains, the case's fill and frame
  applySvar();                                                                     // v28: the suggestions' versions
  placeAll();
  repaint();
  applyLight();
  updateCaption();
  store.set(KEY, S);
  dirty();
}
function applyLight() {
  const day = S.tod === "day", hd = S.quality === "hd";
  const L = {}; LAYERS.forEach(k => L[k] = lvl(k));          // v15: the sliders (a scene button fills them in), times the master
  const set = (list, lv) => list.forEach(l => {
    l.intensity = (l.userData.k || 1) * Math.pow(lv / 100, 1.6);
    l.visible = lv > 0;
    if (l.userData.colKey) l.color.set(S.col[l.userData.colKey] || WARM);   // the smart bulbs' colour
    if (l.isSpotLight) { l.castShadow = hd && lv > 0; if (l.userData.glow) l.userData.glow.material.color.set(lv > 0 ? (S.col[l.userData.colKey] || "#fff3dc") : "#3a3a3a"); }
  });
  const area = hd ? 1 : 0;      // Fast leaves out the area lights (the most expensive) and lifts the fill to make up
  set(lights.strip, L.strip * area); set(lights.uprights, L.uprights * area); set(lights.bias, L.bias * area); set(lights.bar1, L.bar1); set(lights.bar2, L.bar2);
  if (!hd) for (const bar of [lights.bar1, lights.bar2]) bar.forEach((l, i) => {   // v22: Fast lights each bar with two of its four heads, twice as bright
    if (i % 2) l.visible = false; else l.intensity *= 2; });
  set(lights.lamp, (S.layout.lamp || {}).off ? 0 : L.lamp);  // v15: the lamp's colour bulbs dim in their app (v18: or it's been removed)
  capShadows(hd ? SHADOW_CAP : 0);                            // v18: never more shadowed spots than the graphics card can take
  if (growGlow) growGlow.forEach(m => m.visible = !!S.grow);
  set(lights.tv, L.bias > 0 && hd ? 100 : 0);
  ledMat.color.set(L.strip > 0 ? "#ffd9a8" : "#5a5248").multiplyScalar(L.strip > 0 ? 0.6 + L.strip / 100 * 1.4 : 1);
  runLed.color.set(L.uprights > 0 ? (S.col.strips || "#ffd9a8") : "#5a5248").multiplyScalar(L.uprights > 0 ? 0.6 + L.uprights / 100 * 1.4 : 1);   // v16: smart colour strips
  ceilMat.emissiveIntensity = 0.55 * Math.pow(L.strip / 100, 1.2);
  tvScreen.material = L.bias > 0 ? screenOn : screenOff;
  lboxFace.material.color.set(S.lbox && !day ? "#ffffff" : "#5a5a5e");
  laserDots.visible = S.laser && !day;
  if (pcGlow) { pcGlow.visible = !!S.pc; pcLight.visible = !!S.pc; }
  for (const [k, g] of Object.entries(IDEA_G)) g.visible = !!S.ideas[k] && (k !== "case" || S.site !== "A");   // v17: ideas, off by default
  if (G.frames) G.frames.visible = !(S.ideas.case && S.site !== "A");                                         // the case replaces the frames
  if (G.frames) G.frames.position.y = S.site !== "A" && S.plants === "breast" ? 0.3 : 0;                        // v18.1: up 30 over the 158 plant stand
  if (ideaLed) ideaLed.color.set(day ? "#8a8578" : "#fff1d6");
  curtShut.visible = !!S.curtains; curtOpen.visible = !S.curtains;
  win.intensity = day ? 75 : 4; win.color.set(day ? "#e3ecff" : "#3b4a7a");
  view.material.map = day ? SKY.day : SKY.night; view.material.needsUpdate = true;
  // bounce light: a real room's walls relight it; this stands in for that, in proportion to what's on. v15: more of it, so the room
  // reads evenly lit rather than as pools under each head
  const on = (L.strip * 1.0 + L.uprights * 0.3 + L.bar1 * 0.5 + L.bar2 * 0.5 + L.lamp * 0.35 + (L.bias > 0 ? 8 : 0) + (S.lbox ? 4 : 0)) / 100;
  hemi.intensity = day ? 0.5 + (hd ? 0 : 0.25) : 0.05 + on * 0.36 + (hd ? 0 : (L.strip * 0.0075 + L.uprights * 0.0015 + (L.bias > 0 ? 0.08 : 0)));
  win.visible = hd || day;
  MATS.forEach(m => { if ("envMapIntensity" in m) m.envMapIntensity = day ? 0.25 : 0.12; });
  gl.toneMappingExposure = day ? 0.5 : 0.62;
  if (gl.shadowMap.enabled !== hd) { gl.shadowMap.enabled = hd; MATS.forEach(m => m.needsUpdate = true); sizeRenderer(); }
  reshadow();
  dirty();
}
const screenOff = new THREE.MeshStandardMaterial({ color: "#050506", roughness: 0.12, metalness: 0.2 });
const screenOn = new THREE.MeshBasicMaterial({ map: SCREEN_TEX, toneMapped: false, color: "#d8d8d8" });

/* ---------------------------------------------------------------- v18: things you can move (edit mode)
   Each movable thing is a group built round the centre of its footprint (room cm, its front towards local +z), on a pivot that
   edit mode drags across the floor and turns. Where it stands, its turn, its colour and whether it's removed live in S.layout[id];
   the things you add live in S.added. The red lamp is rebuilt where you drop it, so its lights move with it. */
const MOV = {};
const movers = new THREE.Group(); scene.add(movers);
function lb(g, x, y, z, w, h, d, mat, cast = true) {      // a box in a movable's own coordinates: x, z its centre, y its bottom
  const m = new THREE.Mesh(new THREE.BoxGeometry(w * M, h * M, d * M), mat);
  m.position.copy(v3(x, y + h / 2, z)); g.add(shadow(m, cast)); return m;
}
/* v22: fewer draws: a static group's direct child meshes become one mesh per material (your plant stand was 152 meshes, the vinyl stand 45).
   Nested groups (the sofa's cushions, the coffee table's tray, the chair cupboard's doors) are left alone, so their own switches still work. */
function mergeStatic(g) {
  g.updateMatrixWorld(true);
  const inv = new THREE.Matrix4().copy(g.matrixWorld).invert(), by = new Map();
  for (const o of g.children) if (o.isMesh && !o.children.length && o.visible && !Array.isArray(o.material) && !o.isInstancedMesh && !o.isSkinnedMesh) {
    const k = o.material.uuid + (o.castShadow ? "c" : "") + (o.receiveShadow ? "r" : "");
    if (!by.has(k)) by.set(k, []); by.get(k).push(o);
  }
  for (const list of by.values()) {
    if (list.length < 2) continue;
    const geos = list.map(o => { const q = o.geometry.index ? o.geometry.toNonIndexed() : o.geometry.clone(); q.applyMatrix4(new THREE.Matrix4().multiplyMatrices(inv, o.matrixWorld)); return q; });
    const names = Object.keys(geos[0].attributes).sort().join();
    if (!geos.every(q => Object.keys(q.attributes).sort().join() === names)) continue;
    const merged = mergeGeometries(geos); if (!merged) continue;
    const m = new THREE.Mesh(merged, list[0].material); m.castShadow = list[0].castShadow; m.receiveShadow = list[0].receiveShadow;
    list.forEach(o => g.remove(o)); g.add(m);
  }
  return g;
}
function movable(id, label, g, def, w, d, mats, flat = false, extra = {}) {
  if (!extra.added && id !== "lamp") mergeStatic(g);   // v22
  const pivot = new THREE.Group(); pivot.add(g); pivot.userData.movId = id;
  movers.add(pivot);
  MOV[id] = Object.assign({ id, label, pivot, def, w, d, mats, flat, base: mats.map(m => "#" + m.color.getHexString()) }, extra);
  return MOV[id];
}
function spotOf(id) {
  const it = MOV[id], L = S.layout[id] || {}, d0 = it.def();
  return { x: L.x ?? d0.x, z: L.z ?? d0.z, rot: L.rot ?? d0.rot ?? 0 };
}
function placeAll() {
  for (const it of Object.values(MOV)) {
    if (it.lamp) continue;                                  // the lamp is rebuilt where it stands (buildLamp)
    if (it.fixed) { it.pivot.visible = !(S.layout[it.id] || {}).off && (!it.when || it.when()); continue; }   // v27: built in where it stands
    const L = S.layout[it.id] || {}, p = spotOf(it.id);
    it.pivot.position.copy(v3(p.x, 0, p.z)); it.pivot.rotation.y = p.rot * Math.PI / 180;
    it.pivot.visible = !L.off && (!it.when || it.when());
    it.mats.forEach((m, i) => m.color.set(L.col && i === 0 ? L.col : it.base[i]));
  }
  if (selBox) selBox.update();
  reshadow();
}
const SHADOW_CAP = Math.max(0, Math.min(4, (gl.capabilities.maxTextures || 16) - 10));
function capShadows(n) {   // the brightest n spotlights cast shadows; the rest light without them
  const sp = Object.values(lights).flat().filter(l => l.isSpotLight && l.visible).sort((a, b) => b.intensity - a.intensity);
  sp.forEach((l, i) => { l.castShadow = i < n; });
}
// a pot with a plant in it, in a movable's coordinates
function potPlant(g, x, y, z, rad, h, trail, r, potM, leafM) {
  const p = new THREE.Mesh(new THREE.CylinderGeometry(rad * M, rad * 0.8 * M, rad * 1.5 * M, 16), potM);
  p.position.copy(v3(x, y + rad * 0.75, z)); g.add(shadow(p));
  const gs = [];
  for (let k = 0; k < 9 + h; k++) {
    const t = k / (9 + h), q = v3(x + (r() - 0.5) * rad * 2, y + rad * 1.5 + 1 + t * h * 2.2, z + (r() - 0.5) * rad * 1.6);
    const s = new THREE.SphereGeometry((0.02 + r() * 0.014) * (1.2 - t * 0.4), 7, 5); s.scale(0.8, 0.55, 0.32); s.rotateZ((r() - 0.5) * 1.4); s.rotateY(r() * 3);
    s.translate(q.x, q.y, q.z); gs.push(s);
  }
  for (let sI = 0; sI < trail; sI++) {
    const xx = x + (r() - 0.5) * rad * 1.6, zz = z + rad * 0.7, len = 12 + r() * 20;
    for (let t = 0; t < len; t += 3) { const s = new THREE.SphereGeometry(0.013, 6, 4); s.scale(0.8, 0.45, 0.4); const q = v3(xx + Math.sin(t / 5 + sI) * 1.5, y + rad * 1.3 - t, zz); s.translate(q.x, q.y, q.z); gs.push(s); }
  }
  g.add(shadow(new THREE.Mesh(mergeGeometries(gs), leafM)));
}
let growGlow = [];
const GLOW_TEX = canvasTex(128, 128, (c, w, h) => { const gr = c.createRadialGradient(w / 2, h / 2, 2, w / 2, h / 2, w / 2);
  gr.addColorStop(0, "rgba(255,214,160,0.75)"); gr.addColorStop(1, "rgba(255,214,160,0)"); c.fillStyle = gr; c.fillRect(0, 0, w, h); });
function buildPlantsAndRecords() {
  const r = rnd(73), PS = R.PLANT_STAND, RS = R.RECORD_SHELF;
  const leafM = reg(new THREE.MeshStandardMaterial({ color: "#4a8640", roughness: 0.65, side: THREE.DoubleSide }));
  const pots = ["#ece6da", "#c9c2b4", "#b5643f", "#7f8f72", "#2f2f2f"].map(c => reg(new THREE.MeshStandardMaterial({ color: c, roughness: 0.75 })));
  // v18.1: the plant stand from the client's listing: 98 × 29.5 × 158, slatted wood, two five-tier towers and an open middle with two shelves
  { const g = new THREE.Group(), wood = reg(new THREE.MeshStandardMaterial({ color: PS.col, map: OAK_TEX, roughness: 0.6 })); wood.userData.noTint = true;
    const w = PS.w, d = PS.d, h = PS.h, [cl, cm, cr] = PS.cols, pt = PS.post;
    const xs = [-w / 2 + pt / 2, -w / 2 + cl, w / 2 - cr, w / 2 - pt / 2];                  // the four post lines across
    for (const x of xs) for (const z of [-d / 2 + pt / 2, d / 2 - pt / 2]) lb(g, x, 0, z, pt, h, pt, wood);
    const tier = (xa, xb, y, plants) => {                                                    // slats front to back, rails at front and back
      for (const z of [-d / 2 + pt / 2, d / 2 - pt / 2]) lb(g, (xa + xb) / 2, y - 2, z, xb - xa, 2, pt, wood);
      const n = Math.max(4, Math.round((xb - xa) / 4.5));
      for (let k = 0; k < n; k++) lb(g, xa + 1.5 + k * (xb - xa - 3) / (n - 1), y, 0, 2.2, 1.2, d - 3, wood);
      for (let j = 0; j < plants; j++) {
        const rad = 5 + r() * 3.5, px = xa + (j + 0.5) * (xb - xa) / plants;
        potPlant(g, px, y + 1.2, (r() - 0.5) * 6, rad, Math.round(4 + r() * 8), r() < 0.35 ? 2 : 0, r, pots[Math.floor(r() * pots.length)], leafM);
      }
    };
    const L = [xs[0] - pt / 2, xs[1]], Rr = [xs[2], xs[3] + pt / 2], Mi = [xs[1], xs[2]];
    PS.tower.forEach((y, ti) => { tier(L[0], L[1], y, ti === 4 ? 1 : 1 + (r() < 0.5 ? 1 : 0)); tier(Rr[0], Rr[1], y, ti === 4 ? 1 : 1 + (r() < 0.5 ? 1 : 0)); });
    PS.middle.forEach((y, mi) => tier(Mi[0], Mi[1], y, 1));
    for (const z of [-d / 2 + pt / 2, d / 2 - pt / 2]) lb(g, 0, h - 2, z, w, 2, pt, wood);  // the top rails across the open middle
    potPlant(g, 0, PS.middle[0] + 1.2, 0, 9, 22, 0, r, pots[0], leafM);
    movable("plants", "Your plant stand", g, () => { const [x, z, f] = R.PLANT_LAYOUTS[S.plants].plants; return { x, z, rot: f < 0 ? 180 : 0 }; }, w, d, [wood]); }
  // v18.1: the client's vinyl stand (their listing): 70 × 32 × 78, black steel, rustic wood; two face-out bays on top, wires below
  { const g = new THREE.Group(), wood = reg(new THREE.MeshStandardMaterial({ color: RS.col, map: OAK_TEX, roughness: 0.65 })); wood.userData.noTint = true;
    const steel = reg(new THREE.MeshStandardMaterial({ color: RS.steel, roughness: 0.45, metalness: 0.6 }));
    const w = RS.w, d = RS.d, h = RS.h, ft = RS.frame_top, p = 2, sy = RS.shelf_y, yb = RS.bottom_y;
    for (const x of [-w / 2 + p / 2, w / 2 - p / 2]) {
      lb(g, x, 0, d / 2 - p / 2, p, ft, p, steel);                                             // front posts to 63 (front is local +z)
      lb(g, x, 0, -d / 2 + p / 2, p, h, p, steel);                                             // rear posts to 78
      const sl = new THREE.Mesh(new THREE.BoxGeometry(p * M, Math.hypot(h - ft, d - p) * M, p * M), steel);   // the slope between them
      sl.position.copy(v3(x, (ft + h) / 2, 0)); sl.rotation.x = -Math.atan2(d - p, h - ft); g.add(shadow(sl));
    }
    lb(g, 0, ft - 6, d / 2 - 1, w, 1.2, 1.2, steel);                                           // the front rail
    lb(g, 0, yb, 0, w - 2 * p, 2, d, wood); lb(g, 0, yb + 2, -d / 2 + 1, w - 2 * p, 10, 1.6, wood);   // bottom shelf and its back board
    lb(g, 0, sy, 0, w - 2 * p, 2, d, wood); lb(g, 0, sy + 2, d / 2 - 0.8, w - 2 * p, RS.lip, 1.6, wood);   // upper shelf and its 10 cm front board
    lb(g, 0, sy + 2, -2, 2, h - sy - 6, d - 8, wood);                                          // the divider between the two bays
    for (const y of [h - 10, h - 22]) lb(g, 0, y, -d / 2 + 1.5, w, 6, 1.6, wood);              // back boards
    const sleeves = ["#e9e3d3", "#2f3e5c", "#d24b33", "#1f1f1f", "#14806d", "#f0c24b", "#7a4fb0", "#e8603c"].map(c => reg(new THREE.MeshStandardMaterial({ color: c, roughness: 0.55 })));
    const lp = R.LP;
    for (const bx of [-w / 4, w / 4]) for (let k = 0; k < 5; k++) {                            // top bays: LPs leaning back, face-out
      const m = new THREE.Mesh(new THREE.BoxGeometry((RS.bay - 2) * M * 0.97, lp * M, 0.004), sleeves[Math.floor(r() * sleeves.length)]);
      m.position.copy(v3(bx, sy + 2 + lp / 2, d / 2 - 6 - k * 3.2)); m.rotation.x = -0.3; g.add(shadow(m));
    }
    for (let k = 0; k < RS.wires; k++) {                                                        // the wire dividers, and LPs between them
      const zz = d / 2 - 3 - k * (d - 6) / (RS.wires - 1);
      for (const x of [-w / 2 + 12, w / 2 - 12]) lb(g, x, yb + 2, zz, 0.5, RS.wire_h, 0.5, steel, false);
      lb(g, 0, yb + 2 + RS.wire_h - 0.5, zz, w - 24, 0.5, 0.5, steel, false);
      if (k < RS.wires - 1) for (let j = 0; j < 3; j++) {
        const m = new THREE.Mesh(new THREE.BoxGeometry(lp * M, lp * M, 0.004), sleeves[Math.floor(r() * sleeves.length)]);
        m.position.copy(v3(0, yb + 2 + lp / 2, zz - 2 - j * 2.5)); m.rotation.x = -0.12; g.add(shadow(m));
      }
    }
    movable("records", "Your vinyl stand", g, () => { const [x, z, f] = R.PLANT_LAYOUTS[S.plants].records; return { x, z, rot: f < 0 ? 180 : 0 }; }, w, d, [wood]); }
  // the red lamp and the C-table idea are movable too
  MOV.lamp = { id: "lamp", label: "Your red lamp", lamp: true, w: 30, d: 30, mats: [], base: [],
    def: () => { const p = R.LAMP_SPOTS[S.lamp] || R.LAMP_SPOTS[DEF.lamp]; return { x: p.x, z: p.z, rot: 0 }; } };
  Object.defineProperty(MOV.lamp, "pivot", { get: () => lamp });
  if (IDEA_G.ctable) {
    const T = R.IDEAS.ctable, cx = (T.x[0] + T.x[1]) / 2, cz = R.SOFA.end;
    shell.remove(IDEA_G.ctable); IDEA_G.ctable.position.copy(v3(-cx, 0, -cz)); IDEA_G.ctable.position.x = cx * M; IDEA_G.ctable.visible = true;
    movable("ctable", "The C-table (an idea)", IDEA_G.ctable, () => ({ x: cx, z: cz, rot: 0 }), T.x[1] - T.x[0], T.depth, [], false, { when: () => !!S.ideas.ctable });
    delete IDEA_G.ctable;
  }
  S.added.forEach(a => addThing(a, false));
}
/* things to add: simple stand-ins at real-world sizes, each with its own colour */
const CATALOGUE = {
  armchair: { label: "Armchair", w: 80, d: 80, col: "#b5643f", build(g, m, oak) {
    lb(g, 0, 10, 0, 76, 32, 76, m); lb(g, 0, 42, -30, 76, 38, 16, m); lb(g, -32, 42, 4, 12, 18, 68, m); lb(g, 32, 42, 4, 12, 18, 68, m);
    for (const [x, z] of [[-33, -33], [33, -33], [-33, 33], [33, 33]]) lb(g, x, 0, z, 4, 10, 4, oak); } },
  sidetable: { label: "Side table", w: 45, d: 45, col: "#c48c57", build(g, m) {
    lb(g, 0, 48, 0, 45, 2.5, 45, m); for (const [x, z] of [[-19, -19], [19, -19], [-19, 19], [19, 19]]) lb(g, x, 0, z, 3.5, 48, 3.5, m); } },
  plant: { label: "Tall floor plant", w: 40, d: 40, col: "#d8cfc0", build(g, m) {
    const leaf = reg(new THREE.MeshStandardMaterial({ color: "#3f7a3a", roughness: 0.65, side: THREE.DoubleSide }));
    potPlant(g, 0, 0, 0, 16, 26, 0, rnd(5), m, leaf); } },
  bookcase: { label: "Slim bookcase", w: 60, d: 30, col: "#c48c57", build(g, m) {
    lb(g, -29, 0, 0, 2, 180, 30, m); lb(g, 29, 0, 0, 2, 180, 30, m); lb(g, 0, 0, -14.5, 60, 180, 1, m);
    const r = rnd(9), cols = ["#2f3e5c", "#d24b33", "#e9e3d3", "#14806d", "#f0c24b"].map(c => reg(new THREE.MeshStandardMaterial({ color: c, roughness: 0.6 })));
    for (const y of [0, 36, 72, 108, 144, 178]) lb(g, 0, y, 0, 56, 2, 30, m);
    for (const y of [2, 38, 74, 110]) { let x = -26; while (x < 22) { const bw = 2 + r() * 3, bh = 22 + r() * 9; lb(g, x + bw / 2, y, -2, bw, bh, 22, cols[Math.floor(r() * cols.length)]); x += bw + 0.3; } } } },
  beanbag: { label: "Beanbag", w: 80, d: 80, col: "#40609a", build(g, m) {
    const b = new THREE.Mesh(new THREE.SphereGeometry(0.4, 24, 16), m); b.scale.set(1, 0.7, 1); b.position.y = 0.28; g.add(shadow(b)); } },
  footstool: { label: "Footstool", w: 50, d: 50, col: "#34507f", build(g, m, oak) {
    lb(g, 0, 10, 0, 50, 30, 50, m); for (const [x, z] of [[-20, -20], [20, -20], [-20, 20], [20, 20]]) lb(g, x, 0, z, 4, 10, 4, oak); } },
  cushion: { label: "Floor cushion", w: 60, d: 60, col: "#e2a33a", build(g, m) { lb(g, 0, 0, 0, 60, 14, 60, m); } },
  crate: { label: "Record crate", w: 36, d: 36, col: "#c49a6c", build(g, m) {
    lb(g, 0, 0, 0, 36, 2, 36, m); lb(g, -17, 0, 0, 2, 30, 36, m); lb(g, 17, 0, 0, 2, 30, 36, m); lb(g, 0, 0, -17, 36, 30, 2, m); lb(g, 0, 0, 17, 36, 14, 2, m);
    const cols = ["#e9e3d3", "#2f3e5c", "#d24b33", "#1f1f1f", "#14806d"].map(c => reg(new THREE.MeshStandardMaterial({ color: c, roughness: 0.55 })));
    for (let k = 0; k < 5; k++) { const s = new THREE.Mesh(new THREE.BoxGeometry(0.31, 0.31, 0.004), cols[k]); s.position.copy(v3(0, 17, 12 - k * 5)); s.rotation.x = -0.15; g.add(s); } } },
};
/* v20: more decor to add; v21: more furniture */
Object.assign(CATALOGUE, {
  rattan: { label: "Rattan armchair", w: 70, d: 72, col: "#c7a26e", build(g, m, oak) {
    const seat = reg(new THREE.MeshStandardMaterial({ color: "#efe7d8", roughness: 0.95 }));
    lb(g, 0, 38, 2, 62, 10, 60, seat);
    const shell = new THREE.Mesh(new THREE.CylinderGeometry(0.36, 0.3, 0.42, 28, 1, true, Math.PI * 0.15, Math.PI * 1.7), m);
    shell.material.side = THREE.DoubleSide; shell.position.set(0, 0.6, 0.03); shell.rotation.y = Math.PI; g.add(shadow(shell));
    for (const [x, z] of [[-26, -26], [26, -26], [-26, 26], [26, 26]]) lb(g, x, 0, z, 3, 38, 3, oak); } },
  ladder: { label: "Blanket ladder (oak)", w: 45, d: 30, col: "#c48c57", build(g, m) {
    const f = new THREE.Group(); lb(f, -20, 0, 0, 3, 165, 3, m); lb(f, 20, 0, 0, 3, 165, 3, m);
    for (const y of [30, 70, 110, 150]) lb(f, 0, y, 0, 40, 2.5, 2.5, m);
    const th = reg(new THREE.MeshStandardMaterial({ color: "#7a8a6a", roughness: 1 })); lb(f, 0, 96, 1.5, 36, 26, 1.2, th);
    f.rotation.x = 0.16; f.position.z = -0.1; g.add(f); } },
  bench: { label: "Oak bench", w: 100, d: 35, col: "#c48c57", build(g, m) {
    lb(g, 0, 40, 0, 100, 4, 35, m); for (const x of [-44, 44]) lb(g, x, 0, 0, 4, 40, 31, m); } },
  arclamp: { label: "Arc floor lamp", w: 40, d: 40, col: "#1f1f21", build(g, m) {
    lb(g, 0, 0, 0, 34, 3, 34, m);
    const pts = []; for (let i = 0; i <= 16; i++) { const t = i / 16; pts.push(new THREE.Vector3(Math.sin(t * 1.4) * 0.9, 0.03 + Math.sin(t * Math.PI * 0.62) * 1.8, 0)); }
    const arc = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 40, 0.009, 8), m); g.add(arc);
    const end = pts[pts.length - 1], shade = new THREE.Mesh(new THREE.ConeGeometry(0.17, 0.2, 28, 1, true), reg(new THREE.MeshStandardMaterial({ color: "#e9e3d3", side: THREE.DoubleSide, emissive: "#ffd9a8", emissiveIntensity: 0.25 })));
    shade.position.set(end.x, end.y - 0.12, 0); g.add(shade); } },
  vase: { label: "Floor vase with grasses", w: 30, d: 30, col: "#d9cfbf", build(g, m) {
    const v = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.13, 0.55, 24), m); v.position.y = 0.275; g.add(shadow(v));
    const stem = reg(new THREE.MeshStandardMaterial({ color: "#c9b48a", roughness: 0.9 })), r = rnd(13);
    for (let k = 0; k < 14; k++) { const h = 0.55 + r() * 0.45, c = new THREE.Mesh(new THREE.CylinderGeometry(0.002, 0.003, h, 4), stem);
      c.position.set((r() - 0.5) * 0.08, 0.55 + h / 2, (r() - 0.5) * 0.08); c.rotation.set((r() - 0.5) * 0.5, 0, (r() - 0.5) * 0.5); g.add(c);
      const plume = new THREE.Mesh(new THREE.SphereGeometry(0.03, 8, 6), stem); plume.scale.set(0.6, 2.2, 0.6); plume.position.copy(c.position).add(new THREE.Vector3(0, h / 2, 0).applyEuler(c.rotation)); g.add(plume); } } },
  pouffe: { label: "Knitted pouffe", w: 50, d: 50, col: "#c7643a", build(g, m) {
    const b = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.25, 0.4, 32), m); b.position.y = 0.2; g.add(shadow(b));
    const t = new THREE.Mesh(new THREE.TorusGeometry(0.235, 0.02, 8, 32), m); t.rotation.x = Math.PI / 2; t.position.y = 0.39; g.add(t); } },
  basket: { label: "Seagrass basket (throws)", w: 45, d: 45, col: "#b89a6c", build(g, m) {
    const b = new THREE.Mesh(new THREE.CylinderGeometry(0.225, 0.19, 0.42, 28, 1, true), m); b.material.side = THREE.DoubleSide; b.position.y = 0.21; g.add(shadow(b));
    lb(g, 0, 0, 0, 36, 1, 36, m);
    const th = reg(new THREE.MeshStandardMaterial({ color: "#e9e3d3", roughness: 1 })), roll = new THREE.Mesh(new THREE.SphereGeometry(0.17, 16, 12), th);
    roll.scale.set(1, 0.55, 1); roll.position.y = 0.42; g.add(shadow(roll)); } },
  mirror: { label: "Floor mirror (oak)", w: 60, d: 8, col: "#c48c57", build(g, m) {
    const glass = reg(new THREE.MeshStandardMaterial({ color: "#c9d3d8", metalness: 0.95, roughness: 0.05 }));
    const f = new THREE.Group(); lb(f, 0, 0, 0, 60, 170, 3, m); const gl = new THREE.Mesh(new THREE.PlaneGeometry(0.54, 1.62), glass); gl.position.set(0, 0.85, 0.016); f.add(gl);
    f.rotation.x = -0.12; f.position.z = 0.04; g.add(f); } },
  lantern: { label: "Lantern and candles", w: 25, d: 25, col: "#1f1f21", build(g, m) {
    lb(g, 0, 0, 0, 24, 1.5, 24, m); lb(g, 0, 44, 0, 24, 2, 24, m);
    for (const [x, z] of [[-11, -11], [11, -11], [-11, 11], [11, 11]]) lb(g, x, 0, z, 1.5, 45, 1.5, m);
    const wax = reg(new THREE.MeshStandardMaterial({ color: "#f3ecdc", roughness: 0.8, emissive: "#ffb35a", emissiveIntensity: 0.15 }));
    const c = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.2, 16), wax); c.position.y = 0.115; g.add(c); } },
});
function addThing(a, fresh = true) {
  const C = CATALOGUE[a.type]; if (!C) return;
  const m = reg(new THREE.MeshStandardMaterial({ color: C.col, roughness: 0.7 })), oak = reg(new THREE.MeshStandardMaterial({ color: "#c48c57", map: OAK_TEX, roughness: 0.55 }));
  const g = new THREE.Group(); C.build(g, m, oak);
  movable(a.id, C.label, g, () => ({ x: a.x, z: a.z, rot: 0 }), C.w, C.d, [m], false, { added: true });
  if (fresh) { S.added.push(a); placeAll(); store.set(KEY, S); }
}
/* ---------------------------------------------------------------- edit mode: tap to pick, drag to move, the panel to turn, colour, remove */
const ray = new THREE.Raycaster(), floorPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
let selId = null, selBox = null, selSurf = null, drag = null, preEditView = null, downXY = null;
function ndc(e) { const r = canvas.getBoundingClientRect(); return new THREE.Vector2(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1); }
function shown(o) { for (; o; o = o.parent) if (!o.visible) return false; return true; }
function hitMovable(e) {
  ray.setFromCamera(ndc(e), camera);
  const roots = Object.values(MOV).map(it => it.pivot).filter(p => p && p.visible);
  const hit = ray.intersectObjects(roots, true).find(h => shown(h.object));
  if (!hit) return null;
  let o = hit.object; while (o && !o.userData.movId) o = o.parent;
  return o ? o.userData.movId : null;
}
function hitSurface(e) {
  ray.setFromCamera(ndc(e), camera);
  for (const h of ray.intersectObjects([shell, fixtures, ...Object.values(G)], true)) {
    if (!shown(h.object)) continue;
    const m = h.object.material; if (!m || Array.isArray(m)) return null;
    if (m.userData && m.userData.ratio !== undefined) return m.userData.ch === "ceil" ? "ceil" : m.userData.ch === "trim" ? "skirt" : "walls";
    return null;                                   // something else is in front
  }
  return null;
}
function floorAt(e) { ray.setFromCamera(ndc(e), camera); const p = new THREE.Vector3(); return ray.ray.intersectPlane(floorPlane, p) ? { x: -p.x / M, z: p.z / M } : null; }
function halfOf(it, rot) {   // a piece's half-width along x and z when turned to rot
  const q = ((rot % 180) + 180) % 180, hx = q === 90 ? it.d / 2 : q === 0 ? it.w / 2 : Math.max(it.w, it.d) / 2, hz = q === 90 ? it.w / 2 : q === 0 ? it.d / 2 : hx;
  return { hx, hz };
}
const zmaxAt = (x, hx) => x + hx <= R.ALC_W ? R.ALC_D : x - hx >= R.BREAST_X[1] ? R.RECESS_Z : 0;   // the wall in front of the window: the alcove, the breast or the recess
function clampItem(it, x, z, rot) {
  const { hx, hz } = halfOf(it, rot);
  x = Math.min(Math.max(x, hx), R.W - hx);
  const zmax = zmaxAt(x, hx);
  z = Math.min(Math.max(z, R.WINDOW_Z + hz), zmax - hz);
  // v19: within 5 cm of a wall, it goes flush against it
  if (x - hx < SNAP) x = hx; else if (R.W - hx - x < SNAP) x = R.W - hx;
  if (z - hz - R.WINDOW_Z < SNAP) z = R.WINDOW_Z + hz; else if (zmax - hz - z < SNAP) z = zmax - hz;
  return { x: Math.round(x), z: Math.round(z) };
}
const SNAP = 15;   // v27: within 15 cm of a wall it goes flush (was 5): "make it easier to clip an item somewhere like a wall"
function wallsTouched(it, p) {   // which walls a piece is flush against now
  const { hx, hz } = halfOf(it, p.rot), zmax = zmaxAt(p.x, hx);
  return { x0: p.x - hx < 1.5, xW: R.W - p.x - hx < 1.5, zmin: p.z - hz - R.WINDOW_Z < 1.5, zmax: zmax - p.z - hz < 1.5 };
}
function turnItem(id, step) {    // v27: a turn keeps a piece against whichever walls it was against
  const it = MOV[id], p = spotOf(id), on = wallsTouched(it, p), rot = ((p.rot + step) % 360 + 360) % 360, { hx, hz } = halfOf(it, rot);
  let x = p.x, z = p.z;
  if (on.x0) x = hx; if (on.xW) x = R.W - hx;
  if (on.zmin) z = R.WINDOW_Z + hz; if (on.zmax) z = zmaxAt(x, hx) - hz;
  const c = clampItem(it, x, z, rot); setLayout(id, { rot, x: c.x, z: c.z });
}
function backToWall(id) {       // v27: to the nearest wall, its back to it (a piece's back is its -z side: the armchair's back, the bookcase's back panel)
  const it = MOV[id], p = spotOf(id), h0 = halfOf(it, p.rot);
  const walls = [{ d: p.x - h0.hx, rot: 270, k: "x0" }, { d: R.W - p.x - h0.hx, rot: 90, k: "xW" },
                 { d: p.z - h0.hz - R.WINDOW_Z, rot: 0, k: "zmin" }, { d: zmaxAt(p.x, h0.hx) - p.z - h0.hz, rot: 180, k: "zmax" }];
  const w = walls.sort((a, b) => a.d - b.d)[0], { hx, hz } = halfOf(it, w.rot);
  let x = p.x, z = p.z;
  if (w.k === "x0") x = hx; else if (w.k === "xW") x = R.W - hx; else if (w.k === "zmin") z = R.WINDOW_Z + hz; else z = zmaxAt(x, hx) - hz;
  const c = clampItem(it, x, z, w.rot); setLayout(id, { rot: w.rot, x: c.x, z: c.z });
}
/* v19: undo, the last ten changes to the layout (moves, turns, colours, removals, additions) */
const UNDO = [];
function snapshot() { return JSON.stringify({ layout: S.layout, added: S.added }); }
function pushUndo() { UNDO.push(snapshot()); if (UNDO.length > 10) UNDO.shift(); undoBtn(); }
function undoBtn() { const b = qs("#r3d-undo"); if (b) b.disabled = !UNDO.length; }
function restoreLayout(o) {
  S.added.forEach(a => { const it = MOV[a.id]; if (it) { movers.remove(it.pivot); delete MOV[a.id]; } });
  S.added = []; S.layout = JSON.parse(JSON.stringify(o.layout || {}));
  (o.added || []).forEach(a => addThing(Object.assign({}, a), true));
  if (o.plants && R.PLANT_LAYOUTS[o.plants]) S.plants = o.plants;
  select(null); built.lamp = null; applyState(); syncButtons();
}
function undo() { const prev = UNDO.pop(); if (!prev) return; restoreLayout(JSON.parse(prev)); undoBtn(); }
function setLayout(id, patch) { S.layout[id] = Object.assign({}, S.layout[id], patch); if (MOV[id] && MOV[id].added) { const a = S.added.find(a => a.id === id); if (a) Object.assign(a, patch); } }
function select(id) {
  selId = id; selSurf = null;
  if (selBox) { scene.remove(selBox); selBox = null; }
  if (id && MOV[id] && MOV[id].pivot) { selBox = new THREE.BoxHelper(MOV[id].pivot, 0xffc46b); scene.add(selBox); }
  editPanel(); dirty();
}
function editPanel() {
  const P = qs("#r3d-sel"); if (!P) return;
  P.hidden = !(selId || selSurf);
  if (selSurf) {
    const lab = { walls: "Walls", ceil: "Ceiling", skirt: "Skirting and radiator" }[selSurf];
    qs("#r3d-selname").textContent = lab;
    const wallHex = S.paint === "custom" ? S.custom : R.PAINTS[S.paint].hex, key = selSurf === "ceil" ? "ceil" : "skirt";
    const cur = selSurf === "walls" || S[key] === "match" ? wallHex : S[key];
    qs("#r3d-selcol").value = cur; qs("#r3d-swatches").hidden = false;
    qs("#r3d-swatches").innerHTML = (selSurf === "walls" ? Object.entries(R.PAINTS).map(([k, { hex: h, name: n }]) => `<button type="button" class="chip" data-swatch="${k}"><span class="dot" style="background:${h}"></span>${n.replace(/ No\..*/, "").replace("Farrow & Ball ", "").replace("Little Greene ", "")}</button>`).join("")
      : `<button type="button" class="chip" data-swatch="match">Same as the walls</button><button type="button" class="chip" data-swatch="${selSurf === "ceil" ? "#f2f0ea" : "#ece8dd"}">${selSurf === "ceil" ? "White" : "Off-white"}</button>`);
    qsa("[data-sel=turn],[data-sel=turn45],[data-sel=wall],[data-sel=remove],[data-sel=copy]").forEach(b => b.hidden = true); qs("#r3d-selsize").textContent = "";
    return;
  }
  if (!selId) return;
  const it = MOV[selId], L = S.layout[selId] || {};
  qs("#r3d-selname").textContent = it.label;
  qs("#r3d-selsize").textContent = it.w && it.d ? `${Math.round(it.w)} × ${Math.round(it.d)} cm` : "";   // v19: its footprint
  qsa("[data-sel=copy]").forEach(b => b.hidden = !it.added);
  qs("#r3d-swatches").hidden = true;
  qsa("[data-sel=turn],[data-sel=turn45],[data-sel=wall]").forEach(b => b.hidden = !!it.lamp || !!it.fixed);
  qsa("[data-sel=remove]").forEach(b => b.hidden = false);
  qs("#r3d-selcol").parentElement.hidden = !it.mats.length;
  if (it.mats.length) qs("#r3d-selcol").value = L.col || it.base[0];
}
function setEdit(on) {
  S.edit = on; root.classList.toggle("editing", on);
  qs("#r3d-editbtn").setAttribute("aria-pressed", String(on));
  qs("#r3d-editbar").hidden = !on;
  if (on) { preEditView = S.view; if (!(VIEWS[S.view] || {}).above) setView("room"); const pn = document.getElementById("r3d-panel"); if (pn) pn.hidden = true; closePop(); }   // v21: edit from the whole room, cut away (v25: the Tools panel steps aside)
  else { select(null); qs("#r3d-addlist").hidden = true; if (preEditView && preEditView !== S.view) setView(preEditView); }
  dirty();
}
function addList() {
  const removed = Object.values(MOV).filter(it => !it.added && (S.layout[it.id] || {}).off);
  qs("#r3d-addlist").innerHTML = removed.map(it => `<button type="button" class="chip" data-putback="${it.id}">↩ ${it.label}</button>`).join("")
    + Object.entries(CATALOGUE).map(([k, c]) => `<button type="button" class="chip" data-add="${k}">${c.label}</button>`).join("");
}
canvas.addEventListener("pointerdown", e => {
  if (!S.edit || e.button > 0) return;
  downXY = [e.clientX, e.clientY];
  const id = hitMovable(e);
  if (!id) return;
  select(id);
  const it = MOV[id], p = spotOf(id), f = floorAt(e);
  if (!f || it.fixed) { downXY = null; return; }        // v27: built-in pieces are selected, not dragged (and the tap isn't a wall's)
  drag = { id, dx: p.x - f.x, dz: p.z - f.z, x0: p.x, z0: p.z, moved: false, before: snapshot() };
  controls.enabled = false; canvas.setPointerCapture(e.pointerId);
});
canvas.addEventListener("pointermove", e => {
  if (!drag) return;
  const f = floorAt(e); if (!f) return;
  const it = MOV[drag.id], p = spotOf(drag.id), c = clampItem(it, f.x + drag.dx, f.z + drag.dz, p.rot);
  drag.moved = true; drag.x = c.x; drag.z = c.z;
  if (it.lamp) { lamp.position.set(-(c.x - drag.x0) * M, 0, (c.z - drag.z0) * M); }
  else it.pivot.position.copy(v3(c.x, 0, c.z));
  if (selBox) selBox.update(); dirty();
});
function endDrag(e) {
  if (drag) {
    const d = drag; drag = null; controls.enabled = true;
    if (d.moved) { UNDO.push(d.before); if (UNDO.length > 10) UNDO.shift(); undoBtn(); setLayout(d.id, { x: d.x, z: d.z }); if (MOV[d.id].lamp) { lamp.position.set(0, 0, 0); built.lamp = null; applyState(); select(d.id); } else { placeAll(); store.set(KEY, S); } }
    return;
  }
  if (S.edit && downXY && Math.hypot(e.clientX - downXY[0], e.clientY - downXY[1]) < 6) {   // a tap on nothing movable: a surface to paint?
    const surf = hitSurface(e);
    select(null); selSurf = surf; editPanel();
  }
  downXY = null;
}
canvas.addEventListener("pointerup", endDrag);
canvas.addEventListener("pointercancel", () => { if (drag) { drag = null; controls.enabled = true; placeAll(); } });
qs("#r3d-editbtn").addEventListener("click", () => setEdit(!S.edit));
qs("#r3d-editdone")?.addEventListener("click", () => setEdit(false));   // v26: a way out of Edit room with the Tools panel shut
qs("#r3d-addfrom")?.addEventListener("click", () => {   // v26: Extras' "Add a piece of furniture": Edit room, its list open
  if (window.DemmaTools) window.DemmaTools.close(); if (!S.edit) setEdit(true); addList(); qs("#r3d-addlist").hidden = false; });
qs(".r3d-edit").addEventListener("click", e => {
  const b = e.target.closest("button"); if (!b || b.closest("#r3d-sel") || b.id === "r3d-editbtn") return;
  if (b.id === "r3d-add") { addList(); const l = qs("#r3d-addlist"); l.hidden = !l.hidden; return; }
  if (b.id === "r3d-undo") { undo(); return; }
  if (b.id === "r3d-share") { shareLayout(); return; }
  if (b.id === "r3d-useshared") { if (sharedDoc) { pushUndo(); restoreLayout(sharedDoc); qs("#r3d-sharest").textContent = "Using the shared layout (↶ Undo goes back)."; } return; }
  if (b.id === "r3d-layreset") { if (!confirm("Put everything back where the plan has it, and take out what you've added?")) return;
    pushUndo();
    S.added.forEach(a => { const it = MOV[a.id]; if (it) { movers.remove(it.pivot); delete MOV[a.id]; } }); S.added = []; S.layout = {};
    select(null); built.lamp = null; applyState(); return; }
  if (b.dataset.putback) { pushUndo(); setLayout(b.dataset.putback, { off: false }); qs("#r3d-addlist").hidden = true; if (MOV[b.dataset.putback].lamp) built.lamp = null; applyState(); select(b.dataset.putback); return; }
  if (b.dataset.add) {
    const t = controls.target, c = clampItem(CATALOGUE[b.dataset.add], -t.x / M, Math.min(t.z / M, -40), 0);
    const a = { id: "a" + Date.now().toString(36), type: b.dataset.add, x: c.x, z: c.z };
    pushUndo(); addThing(a); qs("#r3d-addlist").hidden = true; select(a.id); applyState();
  }
});
qs("#r3d-sel").addEventListener("click", e => {
  const b = e.target.closest("button"); if (!b) return;
  const k = b.dataset.sel;
  if (b.dataset.swatch) {
    const v = b.dataset.swatch;
    if (selSurf === "walls") S.paint = v; else S[selSurf === "ceil" ? "ceil" : "skirt"] = v;
    repaint(); syncButtons(); updateCaption(); store.set(KEY, S); dirty(); editPanel(); return;
  }
  if (k === "done") { select(null); return; }
  if (!selId) return;
  const it = MOV[selId];
  if (k === "turn" || k === "turn45" || k === "wall" || k === "remove" || k === "copy") pushUndo();
  if (k === "copy" && it.added) {     // v19: another of the same, a little way off, turned and coloured the same
    const src = S.added.find(a => a.id === selId), p = spotOf(selId), L = S.layout[selId] || {}, c = clampItem(it, p.x + 25, p.z + 25, p.rot);
    const a = { id: "a" + Date.now().toString(36), type: src.type, x: c.x, z: c.z };
    addThing(a); setLayout(a.id, { rot: p.rot, col: L.col }); placeAll(); store.set(KEY, S); select(a.id); applyState(); return;
  }
  if (k === "turn" || k === "turn45") { turnItem(selId, k === "turn" ? 90 : 45); placeAll(); store.set(KEY, S); }   // v27: a quarter turn, or an eighth
  if (k === "wall") { backToWall(selId); placeAll(); store.set(KEY, S); }
  if (k === "remove") {
    if (it.added) { movers.remove(it.pivot); delete MOV[selId]; S.added = S.added.filter(a => a.id !== selId); delete S.layout[selId]; }
    else { setLayout(selId, { off: true }); if (it.lamp) built.lamp = null; if (it.fixed) placeChairs(); }
    select(null); applyState();
  }
});
qs("#r3d-selcol").addEventListener("pointerdown", () => { if (selId) pushUndo(); });   // one undo step per colour pick
qs("#r3d-selcol").addEventListener("input", e => {
  const v = e.target.value;
  if (selSurf === "walls") { S.paint = "custom"; S.custom = v; repaint(); syncButtons(); updateCaption(); }
  else if (selSurf) { S[selSurf === "ceil" ? "ceil" : "skirt"] = v; repaint(); }
  else if (selId) { setLayout(selId, { col: v }); placeAll(); }
  store.set(KEY, S); dirty();
});
document.addEventListener("keydown", e => { if (S.edit && (e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "z" && !e.shiftKey) { e.preventDefault(); undo(); } });
/* v19: one layout for both of you, kept in the plan page's shared database (only where the page has one: the Claude deck) */
let ldb = null, sharedDoc = null, sharing = Promise.resolve();
(async () => {
  try { ldb = (window.claude && window.claude.use) ? await window.claude.use("db") : null; } catch (e) { ldb = null; }
  if (!ldb) return;
  qsa(".r3d-share").forEach(b => b.hidden = false);
  if (qs("#r3d-picksave")) qs("#r3d-picksave").hidden = false;   // v22: picks can be saved for the next round
  ldb.doc("layouts/shared").onSnapshot(snap => { sharedDoc = snap.exists ? snap.data() : null; shareStatus(); }, () => { qsa(".r3d-share").forEach(b => b.hidden = true); });
})();
function shareStatus() {
  const st = qs("#r3d-sharest"), use = qs("#r3d-useshared"); if (!st) return;
  use.disabled = !sharedDoc;
  if (!sharedDoc) { st.textContent = "No shared layout yet."; return; }
  let when = ""; try { when = new Date(sharedDoc.at).toLocaleString(undefined, { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" }); } catch (e) {}
  st.textContent = `Shared layout saved ${when}.`;
}
function shareLayout() {
  if (!ldb) return;
  const st = qs("#r3d-sharest"); st.textContent = "Saving…";
  const body = JSON.parse(JSON.stringify({ layout: S.layout, added: S.added, plants: S.plants, at: new Date().toISOString() }));
  sharing = sharing.then(() => ldb.doc("layouts/shared").set(body)).then(() => { st.textContent = "Saved: you'll both see this layout under “Use the shared layout”."; },
    e => { st.textContent = e && e.code === "invalid_argument" ? "This view can't save (read-only)." : "Couldn't save. Try again in a moment."; });
}
/* v22: "Your picks": the ideas, suggestions and decor switched on, their rough cost added up, copied or saved as a note */
const PD = (() => { try { return JSON.parse(document.getElementById("picks-data").textContent); } catch (e) { return { ideas: {}, sugg: {}, decor: {} }; } })();
function picks() {
  const items = [];
  for (const [k, on] of Object.entries(S.ideas)) if (on && PD.ideas[k]) items.push({ kind: "Idea", name: PD.ideas[k][0], lo: PD.ideas[k][1], hi: PD.ideas[k][2] });
  for (const [k, on] of Object.entries(S.sugg)) if (on && PD.sugg[k]) {
    const ver = PD.svar && PD.svar[k] && PD.svar[k][svarOf(k)];   // v28: which version
    items.push({ kind: "Suggestion", name: PD.sugg[k][0] + (ver ? ` (${ver.toLowerCase()})` : ""), lo: PD.sugg[k][1], hi: PD.sugg[k][2] }); }
  for (const k of Object.keys(DEF.decor)) if (S.decor[k] !== DEF.decor[k] && PD.decor[k]) {
    const [lab, names] = PD.decor[k], c = k === "cushions" && PD.ideas.cushions;
    items.push({ kind: "Decor", name: `${lab}: ${names[S.decor[k]] || S.decor[k]}`, lo: c ? c[1] : 0, hi: c ? c[2] : 0 });
  }
  return items;
}
const pickText = items => items.map(i => `${i.kind}: ${i.name}${i.hi ? ` (about £${i.lo}–${i.hi})` : ""}`).join("\n");
function updatePicks() {
  const el = qs("#r3d-picklist"); if (!el) return;
  const items = picks(), lo = items.reduce((a, i) => a + i.lo, 0), hi = items.reduce((a, i) => a + i.hi, 0);
  el.innerHTML = items.length ? items.map(i => `<b>${i.name}</b>${i.hi ? ` <span class="r3d-cost">£${i.lo}–${i.hi}</span>` : ""}`).join(" · ")
      + (hi ? `<br>About £${lo}–${hi} together, none of it in the plan's costs.` : "")
    : "Nothing switched on yet: turn on an idea, a suggestion or a decor choice and it shows here.";
  qs("#r3d-pickcopy").disabled = qs("#r3d-picksave").disabled = !items.length;
}
qs("#r3d-pickcopy")?.addEventListener("click", () => {
  const items = picks(), st = qs("#r3d-pickst"), text = "Our picks from the 3D room:\n" + pickText(items);
  const done = () => { st.textContent = "Copied: paste it into your next message."; };
  try { navigator.clipboard.writeText(text).then(done, () => { qs("#r3d-picklist").textContent = text; st.textContent = "Select the list above to copy it."; }); }
  catch (e) { qs("#r3d-picklist").textContent = text; st.textContent = "Select the list above to copy it."; }
});
qs("#r3d-picksave")?.addEventListener("click", () => {
  if (!ldb) return;
  const items = picks(), st = qs("#r3d-pickst"); st.textContent = "Saving…";
  ldb.doc("layouts/picks").set(JSON.parse(JSON.stringify({ items, text: pickText(items), at: new Date().toISOString() })))
    .then(() => { st.textContent = "Saved for the next round."; }, e => { st.textContent = e && e.code === "invalid_argument" ? "This view can't save (read-only)." : "Couldn't save. Try again in a moment."; });
});
/* v18: if the graphics card gives up (most often HD with shadows on a phone), say so and come back in Fast */
canvas.addEventListener("webglcontextlost", e => {
  e.preventDefault(); S.quality = "fast"; S.picked = true; store.set(KEY, S);
  msg.hidden = false; root.classList.remove("ready");
  msg.innerHTML = 'The 3D room ran out of graphics memory (HD with shadows asks a lot of a phone). <button type="button" class="btn" onclick="location.reload()">Reload it in Fast</button>';
});

/* ---------------------------------------------------------------- views */
const VIEWS = {
  // v21, client: "the default 3D room render to be at the best viewing to see most if not all the room without clipping or obstruction":
  // from above the window side, the window wall cut away (updateCut): the media wall, the breast, the door, the stairs, the table's wall,
  // the PC wall, the sofa and the rug in one picture
  room:    { label: "The whole room", eye: [250, 440, -540], at: [238, 60, -118], fov: 50, above: true },
  // v21: the window view moved to the window's middle, over the sofa's back (it stood behind your red lamp)
  window:  { label: "From the window", eye: [190, 192, -298], at: [214, 82, -10], fov: 68 },
  wall:    { label: "The media wall", eye: [140, 128, -285], at: [93, 108, 20], fov: 52 },
  sofa:    { label: "From the sofa", eye: [85, 108, -250], at: [72, 112, 20], fov: 58 },
  door:    { label: "From the door", eye: [372, 165, -6], at: [110, 85, -210], fov: 64 },
  stairs:  { label: "From the stairs", eye: [438, 205, 4], at: [190, 70, -205], fov: 62 },
  dining:  { label: "The dining table", A: { eye: [250, 140, -262], at: [246, 88, 0] }, B: { eye: [250, 150, -150], at: [467, 112, -185] }, C: { eye: [196, 175, -232], at: [430, 78, -130] }, Cs: { eye: [196, 175, -232], at: [430, 78, -130] }, fov: 60 },   // v21: back from the lamp
  chairs:  { label: "The chair cupboard", eye: [255, 200, -190], at: [460, 95, -262], C: { eye: [262, 170, -120], at: [462, 92, -200] }, Cs: { eye: [228, 178, -150], at: [462, 92, -232] }, fov: 54 },   // v20; v21 clear of the lamp; v30 the compact's chair bay
  windowwall: { label: "The window wall", eye: [236, 150, -70], at: [236, 120, -309], fov: 66 },   // v17: for the ideas' stills
  breast:  { label: "The chimney breast", eye: [246, 140, -250], at: [246, 120, 0], fov: 54 },   // v17: for the ideas' stills
  pc:      { label: "The PC side wall", eye: [345, 135, -168], at: [0, 112, -168], fov: 56 },
  // v31: sitting at the open table's far end, looking at the cabinet; the wall beside the cabinet, by the pipe boxing
  sit:     { label: "Sitting at the table", eye: [258, 115, -128], at: [455, 98, -150], fov: 62 },
  beside:  { label: "Beside the cabinet", eye: [236, 152, -112], at: [462, 84, -262], fov: 60 },
  plan:    { label: "Bird’s eye", eye: [233.5, 1050, -135], at: [233.5, 0, -134.9], fov: 30, above: true },   // v21: closer, the room fills it
  doll:    { label: "Dolls’ house", eye: [610, 450, -560], at: [228, 55, -125], fov: 44, above: true },      // v21: closer, cut away
};
let tween = null;
/* v17: the camera stays in the room: x, y and z inside its walls, in front of the chimney breast, the alcove only within it */
let walked = false;
const freeAbove = () => (VIEWS[S.view] || {}).above && !walked;
function clampRoom(p, target = false) {   // the target (what you orbit round) may sit on a wall's face or a little past it
  const lo = target ? -10 : 4, x = Math.min(Math.max(-p.x / M, lo), R.W - lo), y = Math.min(Math.max(p.y / M, target ? 0 : 20), R.CEIL - (target ? 0 : 8));
  const zmax = target ? R.RECESS_Z + 10 : x <= R.ALC_W ? R.ALC_D - 4 : x <= R.BREAST_X[1] + 4 ? -4 : R.RECESS_Z - 4;
  const z = Math.min(Math.max(p.z / M, R.WINDOW_Z + (target ? -30 : 6)), zmax);
  const q = v3(x, y, z), moved = q.distanceToSquared(p) > 1e-10;
  p.copy(q); return moved;
}
function walk(kind, k = 1) {        // about 15 cm a press on the floor plane; turns 10°; v31: up and down 10 cm; k < 1 while a button's held
  if (tween) return;
  walked = true; controls.maxDistance = 6;
  const fwd = controls.target.clone().sub(camera.position); fwd.y = 0;
  if (fwd.lengthSq() < 1e-8) fwd.set(0, 0, 1);
  fwd.normalize();
  const side = new THREE.Vector3(-fwd.z, 0, fwd.x), step = 0.15 * k;
  if (kind === "tl" || kind === "tr") {
    const off = controls.target.clone().sub(camera.position).applyAxisAngle(new THREE.Vector3(0, 1, 0), (kind === "tl" ? 1 : -1) * Math.PI / 18 * k);
    controls.target.copy(camera.position).add(off);
  } else if (kind === "u" || kind === "dn") {
    const dy = (kind === "u" ? 1 : -1) * 0.1 * k, y = camera.position.y + dy;
    if (y / M < 30 || y / M > R.CEIL - 10) return;
    camera.position.y = y; controls.target.y += dy;
  } else {
    const d = kind === "f" ? fwd.multiplyScalar(step) : kind === "b" ? fwd.multiplyScalar(-step) : kind === "r" ? side.multiplyScalar(step) : side.multiplyScalar(-step);
    camera.position.add(d); controls.target.add(d);
  }
  clampRoom(camera.position); clampRoom(controls.target, true);
  controls.update(); dirty(); syncEye();
}
const WALK_KEYS = { w: "f", arrowup: "f", s: "b", arrowdown: "b", a: "l", arrowleft: "l", d: "r", arrowright: "r", q: "tl", e: "tr",
                    r: "u", f: "dn", pageup: "u", pagedown: "dn" };   // v31: R and F (or Page Up and Down) go up and down
/* v31: the camera's height, how a drag moves it, and the move buttons on the room */
function lift(cm) {          // the eye to a height in cm, still looking the same way
  tween = null; walked = true; controls.maxDistance = 6;
  const y = Math.max(30, Math.min(R.CEIL - 10, cm)) * M, dy = y - camera.position.y;
  camera.position.y = y; controls.target.y += dy;
  clampRoom(camera.position); clampRoom(controls.target, true); controls.update(); dirty(); syncEye();
}
function levelView() {       // look straight ahead, no tilt
  const d = controls.target.clone().sub(camera.position); d.y = 0;
  if (d.lengthSq() < 1e-6) return;
  controls.target.y = camera.position.y; controls.update(); dirty();
}
function seatLook() {        // "look round from here": the point you turn round sits just in front of your eye; circling: 2.2 m on
  const d = controls.target.clone().sub(camera.position);
  if (d.lengthSq() < 1e-8) d.set(0, 0, 1);
  controls.target.copy(camera.position).addScaledVector(d.normalize(), S.cam === "look" ? 0.35 : 2.2);
  clampRoom(controls.target, true); controls.update(); dirty();
}
function applyCam(reseat = true) {
  const look = S.cam === "look";
  controls.enableZoom = !look; controls.rotateSpeed = look ? 0.4 : 0.55;
  if (reseat) seatLook();
}
let eyeT = 0;
function syncEye() {         // the height slider follows the camera
  const now = performance.now(); if (now - eyeT < 80) return; eyeT = now;
  const i = qs("#r3d-eye"), o = qs("#r3d-eyeout"); if (!i || document.activeElement === i) return;
  const cm = Math.round(camera.position.y / M); i.value = Math.min(220, Math.max(40, cm)); if (o) o.textContent = cm > 220 ? "above the room" : `${cm} cm`;
}
function applyPad() { const p = qs("#r3d-pad"); if (p) p.hidden = !S.pad; }
let wheelAcc = 0;            // looking round, the wheel (or a two-finger scroll) walks
canvas.addEventListener("wheel", e => {
  if (S.cam !== "look") return;
  e.preventDefault(); wheelAcc += e.deltaY;
  if (Math.abs(wheelAcc) >= 60) { walk(wheelAcc < 0 ? "f" : "b"); wheelAcc = 0; }
}, { passive: false });
let padT = null;             // a move button held down keeps moving, in smaller steps
const padStop = () => { if (padT) { clearTimeout(padT.t); clearInterval(padT.i); padT = null; } };
root.addEventListener("pointerdown", e => {
  const b = e.target.closest("[data-walk]"); if (!b) return;
  e.preventDefault(); padStop(); const k = b.dataset.walk; walk(k);
  padT = { t: setTimeout(() => { if (padT) padT.i = setInterval(() => walk(k, 0.4), 60); }, 300) };
});
["pointerup", "pointercancel"].forEach(ev => document.addEventListener(ev, padStop)); window.addEventListener("blur", padStop);
root.addEventListener("keydown", e => {
  if (e.altKey || e.ctrlKey || e.metaKey || /^(input|select|textarea)$/i.test(e.target.tagName)) return;
  if (e.target.tagName === "BUTTON" && !e.target.dataset.walk && e.key.startsWith("Arrow")) return;   // arrows still move between buttons
  const k = WALK_KEYS[e.key.toLowerCase()]; if (!k) return;
  e.preventDefault(); walk(k);
});
canvas.addEventListener("pointerdown", () => { canvas.focus({ preventScroll: true }); if (tourSt) tourEnd(); showStop(); });   // v28: touching the room ends the tour (v31: and "Watch it open")
function setView(name, instant, dur) {
  const v = VIEWS[name] || VIEWS.window; S.view = name;
  walked = false; controls.maxDistance = v.above ? 16 : 6;
  const p = (S.site === "C" && S.cab === "sliding" && v.Cs) || v[S.site] || v;   // v30: "Cs", the sliding cabinet's own eye
  const eye = v3(...p.eye), at = v3(...p.at);
  const from = { eye: camera.position.clone(), at: controls.target.clone(), fov: camera.fov };
  setAbove(!v.above);
  baseFov = v.fov;
  if (instant) { tween = null; camera.position.copy(eye); controls.target.copy(at);   // v30: an instant view stops any flight still under way
                camera.fov = fitFov(v.fov); camera.updateProjectionMatrix(); controls.update(); if (S.cam === "look") seatLook(); dirty(); syncEye(); }
  else tween = { t0: performance.now(), from, to: { eye, at, fov: fitFov(v.fov) }, dur: dur || 900 };
  qsa("[data-view]").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.view === name)));
  store.set(KEY, S); updateCaption();
}
/* ---------------------------------------------------------------- v28: the guided tour (room3d_page.tour)
   Each stop flies to its view (slower than a tap) and shows its caption; a stop's own choices (the cabinet open) are put back after it.
   Touching the room, Esc or End stops it. Reduced motion: no flying, the same stops. */
const TOURD = JSON.parse((document.getElementById("tour-data") || {}).textContent || '{"stops":[]}');
const REDUCE = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
const FLY = 2200, DWELL = 5200;
let tourSt = null;
function tourStart() {
  if (!TOURD.stops.length) return;
  if (S.edit) qs("#r3d-editdone")?.click();
  window.DemmaTools?.close(); closePop();
  tourSt = { i: -1, keep: {}, timer: 0, paused: false, t0: 0 };
  root.classList.add("touring"); qs("#r3d-tour").hidden = false;
  tourGo(0);
}
function tourGo(i) {
  if (!tourSt) return;
  const stops = TOURD.stops; clearTimeout(tourSt.timer);
  if (i >= stops.length) { tourEnd(); return; }
  i = Math.max(0, i); tourSt.i = i;
  const st = stops[i], keep = tourSt.keep;
  for (const k of Object.keys(keep)) if (!(st.set && k in st.set)) { S[k] = keep[k]; delete keep[k]; }   // put back the last stop's choices
  if (st.set) for (const [k, v] of Object.entries(st.set)) { if (!(k in keep)) keep[k] = S[k]; S[k] = v; }
  applyState(); syncButtons();
  setView(st.view, REDUCE, FLY);
  qs("#r3d-tourn").textContent = `Stop ${i + 1} of ${stops.length}`;
  qs("#r3d-tourh").textContent = st.title; qs("#r3d-tourp").textContent = st.text;
  qs("#r3d-tourbar").style.width = `${(i + 1) / stops.length * 100}%`;
  tourSt.t0 = performance.now();
  if (!tourSt.paused) tourSt.timer = setTimeout(() => tourGo(i + 1), (REDUCE ? 0 : FLY) + DWELL);
}
function tourCtl(c) {
  if (!tourSt) return;
  if (c === "stop") { tourEnd(); return; }
  if (c === "next") { tourGo(tourSt.i + 1); return; }
  if (c === "prev") { tourGo(tourSt.i - 1); return; }
  if (c === "pause") {
    tourSt.paused = !tourSt.paused; const b = qs('[data-tour="pause"]');
    b.setAttribute("aria-label", tourSt.paused ? "Carry on" : "Pause"); b.querySelector(".ms").textContent = tourSt.paused ? "play_arrow" : "pause";
    clearTimeout(tourSt.timer); if (!tourSt.paused) tourSt.timer = setTimeout(() => tourGo(tourSt.i + 1), DWELL);
  }
}
function tourEnd() {
  if (!tourSt) return;
  clearTimeout(tourSt.timer);
  const keep = tourSt.keep; tourSt = null;
  if (Object.keys(keep).length) { Object.assign(S, keep); applyState(); syncButtons(); }
  root.classList.remove("touring"); qs("#r3d-tour").hidden = true;
  qs("#r3d-tourbtn")?.focus({ preventScroll: true });
}
document.addEventListener("keydown", e => { if (e.key === "Escape" && tourSt) { e.preventDefault(); tourEnd(); } });

/* ---------------------------------------------------------------- v28: "copy link to this view"
   The look (where you stand and every choice, not Edit room's moves) as a plain #look-<token> (base64url JSON), which the page's
   router leaves alone. The link is always the GitHub Pages page, so anyone can open it. */
const LOOK_STR = { site: ["A", "B", "C"], dining: ["folded", "four", "six"], chairs: null, plants: null, seat: ["off", "up", "down"], scene: null, tod: ["evening", "day"], paint: null, lamp: null, cab: ["compact", "sliding"], beside: null };   // v30: which cabinet; v31: beside it
const LOOK_BOOL = ["drawers", "curtains", "lbox", "laser", "pc", "grow", "tdoor", "foot"];   // v31: the open table's floor
const HEX = /^#[0-9a-f]{6}$/i;
const cm = v => [-v.x / M, v.y / M, v.z / M].map(n => Math.round(n));
function lookOf() {
  const o = { v: S.view, c: [...cm(camera.position), ...cm(controls.target), Math.round(baseFov)] };
  for (const k of Object.keys(LOOK_STR)) o[k] = S[k];
  for (const k of LOOK_BOOL) if (S[k] !== DEF[k]) o[k] = S[k] ? 1 : 0;
  if (S.paint === "custom") o.custom = S.custom;
  if (S.ceil !== "match") o.ceil = S.ceil;
  if (S.skirt !== "match") o.skirt = S.skirt;
  const dd = {}; for (const k of Object.keys(DEF.decor)) if (S.decor[k] !== DEF.decor[k]) dd[k] = S.decor[k];
  if (Object.keys(dd).length) o.decor = dd;
  const on = m => Object.keys(m).filter(k => m[k]);
  if (on(S.sugg).length) o.sugg = on(S.sugg);
  if (on(S.ideas).length) o.ideas = on(S.ideas);
  const sv = {}; for (const k of on(S.sugg)) if (svarOf(k) !== SVAR[k]?.[0][0]) sv[k] = svarOf(k);
  if (Object.keys(sv).length) o.svar = sv;
  if (!(sameAsScene() && S.master === 100)) { o.lv = S.lv; o.master = S.master; o.col = S.col; }
  return o;
}
const b64u = t => btoa(unescape(encodeURIComponent(t))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
const unb64u = t => decodeURIComponent(escape(atob(t.replace(/-/g, "+").replace(/_/g, "/"))));
function lookUrl() {
  const here = location.href.split("#")[0], local = location.protocol === "file:" || /^(localhost|127\.0\.0\.1)$/.test(location.hostname) || /github\.io$/.test(location.hostname);
  return (local ? here : TOURD.pages) + "#look-" + b64u(JSON.stringify(lookOf()));
}
function toast(t) {   // the clock starts once two frames have drawn (applying a look can recompile the room first)
  const el = qs("#r3d-toast"); if (!el) return; el.textContent = t; el.hidden = false; clearTimeout(toast.t);
  requestAnimationFrame(() => requestAnimationFrame(() => { clearTimeout(toast.t); toast.t = setTimeout(() => { el.hidden = true; }, 3200); }));
}
function copyLook() {
  const url = lookUrl(), st = qs("#r3d-linkst");
  const shown = () => { st.innerHTML = ""; const i = document.createElement("input"); i.readOnly = true; i.value = url; i.className = "r3d-linkbox"; i.setAttribute("aria-label", "The link to this view"); st.append("Copy this link: ", i); i.focus(); i.select(); };
  const done = () => { st.textContent = "Copied. Paste it into a message: it opens the room just like this."; toast("Link copied"); };
  try { navigator.clipboard.writeText(url).then(done, shown); } catch (e) { shown(); }
}
function applyLook(tok) {
  let o; try { o = JSON.parse(unb64u(tok)); } catch (e) { return false; }
  if (!o || typeof o !== "object") return false;
  const ok = (k, v) => typeof v === "string" && (LOOK_STR[k] ? LOOK_STR[k].includes(v) : k === "scene" ? v in SCENES : k === "plants" ? v in R.PLANT_LAYOUTS : k === "paint" ? (v in R.PAINTS || v === "custom") : /^[a-z0-9_]{1,24}$/i.test(v));
  for (const k of Object.keys(LOOK_STR)) if (ok(k, o[k])) S[k] = o[k];
  for (const k of LOOK_BOOL) if (k in o) S[k] = !!o[k];
  if (HEX.test(o.custom || "")) S.custom = o.custom;
  S.ceil = HEX.test(o.ceil || "") ? o.ceil : "match"; S.skirt = HEX.test(o.skirt || "") ? o.skirt : "match";
  S.decor = Object.assign({}, DEF.decor); if (o.decor && typeof o.decor === "object") for (const k of Object.keys(DEF.decor)) if (typeof o.decor[k] === "string") S.decor[k] = o.decor[k];
  const set = a => Object.fromEntries((Array.isArray(a) ? a : []).filter(k => typeof k === "string").map(k => [k, true]));
  S.sugg = set(o.sugg); S.ideas = set(o.ideas);
  S.svar = {}; if (o.svar && typeof o.svar === "object") for (const [k, v] of Object.entries(o.svar)) if (SVAR[k]?.some(x => x[0] === v)) S.svar[k] = v;
  if (o.lv && typeof o.lv === "object") { S.lv = Object.assign({}, SCENES[S.scene].levels); for (const k of LAYERS) if (Number.isFinite(+o.lv[k])) S.lv[k] = Math.max(0, Math.min(100, +o.lv[k])); S.master = Number.isFinite(+o.master) ? Math.max(0, Math.min(100, +o.master)) : 100; }
  else { S.lv = Object.assign({}, SCENES[S.scene].levels); S.master = 100; }
  if (o.col && typeof o.col === "object") for (const k of Object.keys(DEF.col)) if (HEX.test(o.col[k] || "")) S.col[k] = o.col[k];
  applyState(); syncButtons();
  setView(o.v in VIEWS ? o.v : "room", true);
  const c = Array.isArray(o.c) && o.c.length === 7 && o.c.every(Number.isFinite) ? o.c : null;
  if (c) { camera.position.copy(v3(c[0], c[1], c[2])); controls.target.copy(v3(c[3], c[4], c[5])); baseFov = Math.max(20, Math.min(90, c[6])); camera.fov = fitFov(baseFov); camera.updateProjectionMatrix(); controls.update(); updateCut(); dirty(); }
  store.set(KEY, S);
  return true;
}
function lookFromHash() {
  const m = (location.hash || "").match(/^#look-([A-Za-z0-9_-]+)$/); if (!m) return;
  if (applyLook(m[1])) toast("Opened the shared view");
  try { history.replaceState(history.state, "", "#room"); } catch (e) {}
}
addEventListener("hashchange", () => { if (started) lookFromHash(); });

let cutSide = "";
function updateCut() {        // which wall the camera is outside of, if any (only in the views from above, before you walk)
  let side = "", best = 0;
  if (freeAbove()) {
    const x = -camera.position.x / M, z = camera.position.z / M;
    for (const [k, v] of Object.entries({ win: R.WINDOW_Z - z, stairs: x - R.W, pc: -x, wall: z - R.ALC_D })) if (v > best) { best = v; side = k; }
  }
  if (side === cutSide) return false;
  cutSide = side; const A = CLIP[0], n = A.normal;
  if (side === "win") { n.set(0, 0, 1); A.constant = -(R.WINDOW_Z + CUT_IN) * M; }
  else if (side === "stairs") { n.set(1, 0, 0); A.constant = (R.W - CUT_IN) * M; }
  else if (side === "pc") { n.set(-1, 0, 0); A.constant = -CUT_IN * M; }
  else if (side === "wall") { n.set(0, 0, -1); A.constant = -12 * M; }
  else { n.set(0, 0, 1); A.constant = 1e3; }
  reshadow();
  return true;
}
/* ---------------------------------------------------------------- v25: the numbered stickers on the room
   Each has an anchor in room cm (room3d_page.hotspots). Every frame the camera moves it is projected to the stage; a sticker behind
   the camera or off the picture hides; one on a wall seen from behind (and not opened by the cutaway) fades. Tapping one opens the
   popover under it: Open in the plan (the page's Plan sheet, at that chapter) and Fly here (the matching view). */
const HOTS = JSON.parse((document.getElementById("hotspots-data") || {}).textContent || "[]");
const stickEls = {}; qsa(".stk").forEach(b => { stickEls[b.dataset.hot] = b; });
const pop = qs("#r3d-pop"), stage = qs(".r3d-stage");
let popId = null;
const _p = new THREE.Vector3();
let labelsOn = true; try { labelsOn = localStorage.getItem("mw26-labels") !== "off"; } catch (e) {}
function setLabels(on) {
  labelsOn = on; try { localStorage.setItem("mw26-labels", on ? "on" : "off"); } catch (e) {}
  if (!on) { closePop(); Object.values(stickEls).forEach(el => { el.hidden = true; }); }
  document.getElementById("r3d")?.classList.toggle("nolabels", !on);
  qsa("[data-labels]").forEach(b => b.setAttribute("aria-pressed", String((b.dataset.labels === "on") === on)));
  const t = qs("#r3d-lbl"); if (t) { t.setAttribute("aria-pressed", String(on)); t.querySelector(".ms").textContent = on ? "label_off" : "label"; t.querySelector(".t").textContent = on ? "Hide labels" : "Show labels"; }
  dirty();
}
document.addEventListener("click", e => { const b = e.target.closest("#r3d-lbl, [data-labels]"); if (!b) return; setLabels(b.id === "r3d-lbl" ? !labelsOn : b.dataset.labels === "on"); });
function placeStickers() {
  if (!HOTS.length || !started || !labelsOn) return;
  const w = stage.clientWidth, h = stage.clientHeight, cx = -camera.position.x / M, cz = camera.position.z / M;
  const placed = [];   // v26: labels never sit on top of each other (each one moves down clear of those already placed)
  for (const H of HOTS) {
    const el = stickEls[H.id]; if (!el) continue;
    _p.copy(v3(...H.at)).project(camera);
    const off = _p.z > 1 || _p.z < -1 || Math.abs(_p.x) > 1.02 || Math.abs(_p.y) > 1.02;
    el.hidden = off;
    if (off) { if (popId === H.id) closePop(); continue; }
    const hw = (el.offsetWidth || 140) / 2 + 6, x = Math.max(hw + railR, Math.min(w - hw, (_p.x + 1) / 2 * w)); let y = Math.max(28, Math.min(h - 28, (1 - _p.y) / 2 * h));   // kept whole on screen
    if (cover && x + hw > cover.left && x - hw < cover.right && y + 20 > cover.top && y - 20 < cover.bottom) { el.hidden = true; if (popId === H.id) closePop(); continue; }   // v26: not under the Tools panel
    const ew = el.offsetWidth || 140, eh = el.offsetHeight || 40;
    for (let k = 0; k < 8; k++) {
      const hit = placed.find(q => Math.abs(x - q.x) < (ew + q.w) / 2 + 4 && Math.abs(y - q.y) < (eh + q.h) / 2 + 4);
      if (!hit) break;
      y = hit.y + (eh + hit.h) / 2 + 4;
    }
    placed.push({ x, y, w: ew, h: eh });
    el.style.left = x + "px"; el.style.top = y + "px";
    const behind = H.nrm && !(H.cut && H.cut === cutSide) && ((cx - H.at[0]) * H.nrm[0] + (cz - H.at[2]) * H.nrm[1]) < 0;
    el.classList.toggle("behind", !!behind);
    if (popId === H.id) placePop(el);
  }
}
function placePop(el) {
  const sw = stage.clientWidth, x = parseFloat(el.style.left), y = parseFloat(el.style.top), pw = 290;
  const left = Math.max(12, Math.min(sw - pw - 12, x - pw / 2));
  pop.style.left = left + "px"; pop.style.top = (y + 30) + "px"; pop.style.setProperty("--ax", (x - left) + "px");
}
function openPop(id) {
  const H = HOTS.find(h => h.id === id); if (!H) return;
  if (popId) stickEls[popId].setAttribute("aria-expanded", "false");
  popId = id; const el = stickEls[id]; el.setAttribute("aria-expanded", "true");
  pop.style.setProperty("--h", H.hue);
  qs("#r3d-pop-h").textContent = H.name;
  const ul = qs(".facts", pop); ul.textContent = "";
  H.facts.forEach(f => { const li = document.createElement("li"); li.textContent = f; ul.appendChild(li); });
  pop.hidden = false; placePop(el); qs(".go", pop).focus({ preventScroll: true });
}
function closePop() { if (popId && stickEls[popId]) stickEls[popId].setAttribute("aria-expanded", "false"); popId = null; if (pop) pop.hidden = true; }
qsa(".stk").forEach(b => b.addEventListener("click", e => { e.stopPropagation(); popId === b.dataset.hot ? closePop() : openPop(b.dataset.hot); }));
if (pop) pop.addEventListener("click", e => {
  const b = e.target.closest("button"); if (!b) return;
  const H = HOTS.find(h => h.id === popId);
  if (b.classList.contains("x")) { const was = popId; closePop(); if (was) stickEls[was].focus(); return; }
  if (!H) return;
  if (b.dataset.popgo === "fly") { setView(H.view); closePop(); }
  else if (b.dataset.popgo === "plan") { closePop(); window.dispatchEvent(new CustomEvent("demma-open", { detail: { sheet: "plan", chapter: H.chapter } })); }
});
canvas.addEventListener("pointerdown", () => { if (popId) closePop(); });
document.addEventListener("keydown", e => { if (e.key === "Escape" && popId) { const was = popId; closePop(); stickEls[was].focus(); } });
new ResizeObserver(() => placeStickers()).observe(stage);
/* ---------------------------------------------------------------- v30, client: "make function so say i click the dining cabinet i can
   manage options to open it, close it etc as goes for drawers and other items i can interact with". A tap on the room (not a drag, not
   in Edit room) finds what's under it and opens a card of what it can do. The card's buttons are the room's own controls (data-dining,
   data-chairs, data-drawers, data-tog...), so they work, and stay in step with the Tools panel, exactly as its buttons do. */
const act = qs("#r3d-act");
let actId = null, actXY = null, tapDown = null;
const clippedAt = p => CLIP.every(pl => pl.distanceToPoint(p) < 0);           // the cutaway hides what's on the far side of both planes
const under = (o, g) => { if (!g) return false; for (; o; o = o.parent) if (o === g) return true; return false; };
function pickItem(e) {
  ray.setFromCamera(ndc(e), camera);
  const hit = ray.intersectObjects(scene.children, true).find(h => h.object.isMesh && shown(h.object) && !clippedAt(h.point) && !(selBox && h.object === selBox));
  if (!hit) return null;
  const o = hit.object, p = hit.point;
  const near = (obj, r) => !!obj && obj.getWorldPosition(new THREE.Vector3()).distanceTo(p) < r * M;
  if (S.site === "C" && (under(o, cab) || under(o, optC))) return "cab";
  if (under(o, chairCab) || under(o, chairsIn) || under(o, chairsHook)) return "chaircab";
  if (under(o, seatUp) || under(o, seatDown)) return "seat";
  if (under(o, lamp)) return "lamp";
  if (under(o, bar1)) return "bar1";
  if (under(o, bar2)) return "bar2";
  if (under(o, curtOpen) || under(o, curtShut)) return "curtains";
  if (o === tvScreen) return "tv";
  if (o === lboxFace) return "lbox";
  if (under(o, pcGlow)) return "pc";
  let m = o; while (m && !m.userData.movId) m = m.parent;
  if (m && MOV[m.userData.movId]) return "mov:" + m.userData.movId;
  for (const [k, g] of Object.entries(G)) if (under(o, g)) {
    if (k === "unit_in" || k === "unit_out") return "wall";
    if (/^[AB]_/.test(k)) return "table";
    if (near(tvScreen, 70)) return "tv";                                       // the TV's own frame and stand are in the room's fixed parts
    if (near(lboxFace, 30)) return "lbox";
    if (near(pcLight, 40)) return "pc";
    return null;
  }
  return null;
}
const btn = (label, attrs, on) => ({ label, attrs, on });
function actItems(id) {     // [title, how it is now, buttons]
  const folded = S.dining === "folded", lv = k => (S.lv[k] ?? 0) > 0;
  if (id === "cab" && S.site !== "C") id = "table";
  if (id === "table" && S.site === "C") id = "cab";
  if (id === "cab") {
    const sl = S.cab === "sliding", d = cabDoors();
    const st = !folded ? `Open for ${S.dining}: the table is out` : d.table ? "Packed away, the table door open" : d.chairs ? "Packed away, the chair door open" : "Packed away: the table and the six chairs inside";
    return [sl ? "The sliding dining cabinet (the alternative)" : "The dining cabinet", st, [
      btn("Open for six", { dining: "six" }, S.dining === "six"), btn("Open for four", { dining: "four" }, S.dining === "four"),
      btn(folded ? "Folded away" : "Fold it away", { dining: "folded" }, folded),
      ...(folded ? [btn(d.table ? "Shut the table door" : "Open the table door", { tdoor: d.table ? "shut" : "open" }),
                    btn(d.chairs ? "Shut the chair door" : "Open the chair door", { chairs: d.chairs ? "cupboard" : "open" })] : []),
      btn(sl ? "Show the compact one" : "Show the sliding one", { cab: sl ? "compact" : "sliding" }),
      btn("Look at it", { view: "dining" }), btn("Read about it", { actgo: "dining" })]];
  }
  if (id === "table") return [S.site === "A" ? "The flip-top on the breast (the alternative)" : "The flip-top by the stairs (the alternative)", folded ? "Folded" : `Open for ${S.dining}`, [
      btn("Open for six", { dining: "six" }, S.dining === "six"), btn("Open for four", { dining: "four" }, S.dining === "four"),
      btn(folded ? "Folded" : "Fold it", { dining: "folded" }, folded), btn("Show the dining cabinet", { site: "C" }), btn("Look at it", { view: "dining" })]];
  if (id === "chaircab") return ["The flip-top's chair cupboard", S.chairs === "open" ? "Doors open" : "Doors shut", [
      btn(S.chairs === "open" ? "Shut the doors" : "Open the doors", { chairs: S.chairs === "open" ? "cupboard" : "open" }), btn("Look at it", { view: "chairs" })]];
  if (id === "seat") return ["The fold-down seat", S.seat === "down" ? "Down" : "Folded up", [
      btn(S.seat === "down" ? "Fold it up" : "Fold it down", { seat: S.seat === "down" ? "up" : "down" })]];
  if (id === "wall") return ["The media wall", S.drawers ? "Every drawer pulled out" : "Drawers shut", [
      btn(S.drawers ? "Push the drawers in" : "Pull the drawers out", { drawers: S.drawers ? "in" : "out" }),
      btn(lv("bias") ? "TV off" : "TV on", { layer: "bias:" + (lv("bias") ? "off" : "on") }), btn("Film lights", { scene: "film" }, S.scene === "film"),
      btn("Look at it", { view: "wall" }), btn("Read about it", { actgo: "wall" })]];
  if (id === "tv") return ["The TV", lv("bias") ? "On, its bias light behind it" : "Off", [
      btn(lv("bias") ? "Turn it off" : "Turn it on", { layer: "bias:" + (lv("bias") ? "off" : "on") }), btn("Film lights", { scene: "film" }, S.scene === "film"), btn("Look at it", { view: "sofa" })]];
  if (id === "lamp") return ["Your red lamp", lv("lamp") ? "On" : "Off", [
      btn(lv("lamp") ? "Turn it off" : "Turn it on", { layer: "lamp:" + (lv("lamp") ? "off" : "on") }), btn("Move it", { actedit: "lamp" })]];
  if (id === "bar1" || id === "bar2") return [id === "bar1" ? "Spot bar 1, over the sofa" : "Spot bar 2, over the table", lv(id) ? "On" : "Off", [
      btn(lv(id) ? "Turn it off" : "Turn it on", { layer: id + ":" + (lv(id) ? "off" : "on") }),
      btn("Bright", { scene: "bright" }, S.scene === "bright"), btn("Cosy", { scene: "cosy" }, S.scene === "cosy"), btn("Film", { scene: "film" }, S.scene === "film")]];
  if (id === "curtains") return ["The curtains", S.curtains ? "Drawn" : "Open", [btn(S.curtains ? "Open them" : "Draw them", { tog: "curtains" })]];
  if (id === "lbox") return ["Your OBEGRÄNSAD light box", S.lbox ? "On" : "Off", [btn(S.lbox ? "Turn it off" : "Turn it on", { tog: "lbox" })]];
  if (id === "pc") return ["Your PC", S.pc ? "Lit" : "Dark", [btn(S.pc ? "Lights off" : "Lights on", { tog: "pc" }), btn("Look at it", { view: "pc" }), btn("Read about it", { actgo: "side" })]];
  if (id.startsWith("mov:")) { const it = MOV[id.slice(4)]; if (!it) return null;
    return [it.label, it.fixed ? "Built in: it can come off, but not move" : "Drag it in Edit room, or change its colour", [btn(it.fixed ? "Take it off or put it back" : "Move it", { actedit: it.id })]]; }
  return null;
}
function renderAct() {
  const items = actId && actItems(actId);
  if (!items) { closeAct(); return; }
  const [title, st, bs] = items;
  qs("#r3d-act-h").textContent = title; qs("#r3d-act-st").textContent = st;
  const box = qs("#r3d-acts"); box.textContent = "";
  for (const b of bs) {
    const el = document.createElement("button"); el.type = "button"; el.textContent = b.label;
    for (const [k, v] of Object.entries(b.attrs)) el.dataset[k] = v;
    if (b.on !== undefined) el.setAttribute("aria-pressed", String(!!b.on));
    box.appendChild(el);
  }
  placeAct();
}
function placeAct() {
  if (!actXY) return;
  const sw = stage.clientWidth, sh = stage.clientHeight, pw = act.offsetWidth || 300, ph = act.offsetHeight || 200;
  const left = Math.max(12, Math.min(sw - pw - 12, actXY[0] - pw / 2));
  const below = actXY[1] + 22 + ph < sh - 90, top = below ? actXY[1] + 22 : Math.max(12, actXY[1] - ph - 22);
  act.style.left = left + "px"; act.style.top = top + "px"; act.style.setProperty("--ax", (actXY[0] - left) + "px");
  act.classList.toggle("above", !below);
}
function openAct(id, xy) {
  if (popId) closePop();
  actId = id; actXY = xy; act.hidden = false; renderAct();
  if (!act.hidden) { const f = qs("#r3d-acts button"); if (f) f.focus({ preventScroll: true }); }
}
function closeAct() { actId = null; if (act) act.hidden = true; }
if (act) {
  act.addEventListener("click", e => {
    const b = e.target.closest("button"); if (!b) return;
    if (b.classList.contains("x")) { closeAct(); return; }
    const d = b.dataset;
    if (d.actgo) { closeAct(); window.dispatchEvent(new CustomEvent("demma-open", { detail: { sheet: "plan", chapter: d.actgo } })); return; }
    if (d.actedit) { const id = d.actedit; closeAct(); setEdit(true); select(id); return; }
    if (d.view) setTimeout(closeAct, 0);                     // the room flies there; the card has done its job
  });
  canvas.addEventListener("pointerdown", e => { tapDown = (S.edit || e.button > 0) ? null : [e.clientX, e.clientY, performance.now()]; if (actId) closeAct(); });
  canvas.addEventListener("pointerup", e => {
    const t = tapDown; tapDown = null;
    if (!t || S.edit || Math.hypot(e.clientX - t[0], e.clientY - t[1]) > 6 || performance.now() - t[2] > 600) return;
    const id = pickItem(e); if (!id) return;
    const r = stage.getBoundingClientRect();
    openAct(id, [e.clientX - r.left, e.clientY - r.top]);
  });
  document.addEventListener("keydown", e => { if (e.key === "Escape" && actId) closeAct(); });
}
function setAbove(show) {   // the floor above (the stairwell's upper walls) hides in the views from above
  scene.traverse(o => { if (o.name === "above") o.visible = show; });
  view.visible = show;
}

/* ---------------------------------------------------------------- render loop, only when something changed */
let need = 2, moving = false, still_t = 0, lowRes = false;
function dirty() { need = Math.max(need, 2); }
function fullRatio() { return S.quality === "hd" ? Math.min(window.devicePixelRatio || 1, 1.5) : Math.min(window.devicePixelRatio || 1, 1) * 0.85; }
/* v21: narrower screens (phones show the room at 4:3) widen the field of view so every view takes in as much of the room across as at 16:9 */
let baseFov = 50;
const fitFov = (fov, asp = camera.aspect) => asp >= 16 / 9 ? fov : Math.min(95, 2 * Math.atan(Math.tan(fov * Math.PI / 360) * (16 / 9) / asp) * 180 / Math.PI);
function sizeRenderer() {
  const w = canvas.clientWidth, h = canvas.clientHeight;
  if (!w || !h) return;
  if (!started) { start(); return; }
  // v14.1: while you drag, the picture renders at a lower resolution; it sharpens again as soon as you stop
  gl.setPixelRatio(lowRes ? Math.max(0.5, fullRatio() * 0.5) : fullRatio());
  gl.setSize(w, h, false);
  camera.aspect = w / h; if (!tween) camera.fov = fitFov(baseFov); applyShift(); dirty();
}
/* v26: with the Tools panel open, the room slides into the space beside it (laptop: left of the panel; phone: above it, half way) */
const shift = { x: 0, y: 0 }; let cover = null;   // cover: the open panel's box, so stickers under it hide
function applyShift() {
  const w = canvas.clientWidth, h = canvas.clientHeight;
  if (w && h && (shift.x || shift.y)) camera.setViewOffset(w, h, shift.x, shift.y, w, h); else camera.clearViewOffset();
  camera.updateProjectionMatrix();
}
let railR = 0;   // the right edge of the page's section rail (laptop), so stickers stay clear of it
function measureShift(open) {
  const p = document.getElementById("r3d-panel"), w = canvas.clientWidth, h = canvas.clientHeight, rail = document.querySelector(".rail");
  railR = rail && getComputedStyle(rail).display !== "none" ? rail.getBoundingClientRect().right + 6 : 0;
  shift.x = shift.y = 0; cover = null;
  if (open && p && !p.hidden && w) {
    const r = p.getBoundingClientRect(); cover = r;
    if (innerWidth >= 900) shift.x = Math.round(Math.max(0, w - r.left - railR) / 2);
    else shift.y = Math.round(Math.max(0, h - r.top) / 4);
  }
  applyShift(); dirty();
}
addEventListener("demma-tools", e => requestAnimationFrame(() => measureShift(!!e.detail)));
addEventListener("resize", () => measureShift(!!(window.DemmaTools && window.DemmaTools.isOpen())));
requestAnimationFrame(() => { measureShift(false); setLabels(labelsOn); });
new ResizeObserver(sizeRenderer).observe(canvas);
controls.addEventListener("start", () => { moving = true; });
controls.addEventListener("end", () => { moving = false; });
function frame(now) {
  requestAnimationFrame(frame);
  if (!canvas.clientWidth) return;
  if (tween) {
    const k = Math.min(1, (now - tween.t0) / (tween.dur || 900)), e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
    camera.position.lerpVectors(tween.from.eye, tween.to.eye, e);
    controls.target.lerpVectors(tween.from.at, tween.to.at, e);
    camera.fov = tween.from.fov + (tween.to.fov - tween.from.fov) * e; camera.updateProjectionMatrix();
    if (k >= 1) { tween = null; if (S.cam === "look") seatLook(); syncEye(); }   // v31: looking round, the turning point comes back in front of you
    need = 2;
  }
  const changed = controls.update();
  if (changed) need = 2;
  if (cabTween(now)) need = 2;                                    // v30: the cabinet's doors swinging or sliding
  if (!tween && !freeAbove() && (clampRoom(camera.position) | clampRoom(controls.target, true))) need = 2;   // v17: never outside the room
  const active = moving || changed || !!tween;
  if (active) { still_t = now; if (!lowRes) { lowRes = true; sizeRenderer(); } }
  else if (lowRes && now - still_t > 180) { lowRes = false; sizeRenderer(); }
  if (updateCut()) need = 2;
  if (need > 0) {
    const t = probe > 0 && !lowRes ? performance.now() : 0;
    gl.render(scene, camera); need--; placeStickers();
    if (t) { const c = gl.getContext(); c.readPixels(0, 0, 1, 1, c.RGBA, c.UNSIGNED_BYTE, PX); probeT.push(performance.now() - t); probe--; if (!probe) autoQuality(); }
  }
}
// v14.1: if this device takes too long over a full HD frame, drop to Fast (unless you picked a quality yourself)
let probe = 3; const probeT = [], PX = new Uint8Array(4);
function autoQuality() {
  const ms = probeT.sort((a, b) => a - b)[1];
  if (ms > 70 && S.quality === "hd" && !S.picked) {
    S.quality = "fast"; applyLight(); syncButtons();
    qs("#r3d-savest").textContent = "Switched to Fast for this device; pick HD for shadows (saved pictures always have them).";
  }
}

/* ---------------------------------------------------------------- caption and HD save */
function updateCaption() {
  try { updatePicks(); } catch (e) {}   // v22
  const sc = SCENES[S.scene];
  const site = S.site === "A" ? "Table on the chimney breast" : S.site === "C" ? (S.cab === "sliding" ? "The sliding dining cabinet (the alternative)" : "The compact dining cabinet") : "Table under the shelf by the stairs";
  const cl = (cabC().len_open || cabC().len);
  const din = S.site === "C" ? { folded: "folded away, the six chairs inside", four: `open, ${cl} long, for four`, six: `open, ${cl} long, for six` }[S.dining]
    : { folded: "folded on the wall", four: "open on its gate leg, for four", six: "open on its gate leg, for six" }[S.dining];
  const paint = S.paint === "custom" ? `your colour ${S.custom}` : R.PAINTS[S.paint].name;
  const lights = sameAsScene() && S.master === 100 ? sc.name : `your lighting (from ${sc.name})`;
  qs("#r3d-cap").textContent = `${(VIEWS[S.view] || VIEWS.window).label} · ${site}, ${din} · ${lights} · ${paint}${S.drawers ? " · drawers out" : ""}${Object.values(S.ideas).some(Boolean) ? " · ideas shown (not in the plan)" : ""}${Object.keys(DEF.decor).some(k => S.decor[k] !== DEF.decor[k]) ? " · decor tried" : ""}${Object.values(S.sugg).some(Boolean) ? " · suggestions shown" : ""}`;
}
function still(w, h) {
  if (!started) start();
  const pr = gl.getPixelRatio(), size = gl.getSize(new THREE.Vector2()), asp = camera.aspect;
  const fov0 = camera.fov;
  gl.setPixelRatio(1); gl.setSize(w, h, false); camera.aspect = w / h; camera.fov = fitFov(baseFov); camera.clearViewOffset(); camera.updateProjectionMatrix();
  const was = gl.shadowMap.enabled, wasQ = S.quality; gl.shadowMap.enabled = true; gl.shadowMap.type = THREE.PCFSoftShadowMap;
  if (wasQ !== "hd") { S.quality = "hd"; applyLight(); gl.shadowMap.enabled = true; }
  const big = SMALL ? 1024 : 2048;   // v18: phones keep 1024 maps for the picture, and at most six spots cast shadows
  Object.values(lights).flat().forEach(l => { if (l.isSpotLight && l.visible) { l.castShadow = true; l.shadow.mapSize.set(big, big); if (l.shadow.map) { l.shadow.map.dispose(); l.shadow.map = null; } } });
  capShadows(Math.max(0, Math.min(6, (gl.capabilities.maxTextures || 16) - 10)));
  MATS.forEach(m => m.needsUpdate = true);
  updateCut(); reshadow();
  gl.render(scene, camera);
  const url = canvas.toDataURL("image/png");
  gl.shadowMap.type = THREE.PCFShadowMap; S.quality = wasQ;
  gl.shadowMap.enabled = was;
  MATS.forEach(m => m.needsUpdate = true);
  Object.values(lights).flat().forEach(l => { if (l.isSpotLight) { l.shadow.mapSize.set(1024, 1024); if (l.shadow.map) { l.shadow.map.dispose(); l.shadow.map = null; } } });
  applyLight();
  gl.setPixelRatio(pr); gl.setSize(size.x, size.y, false); camera.aspect = asp; camera.fov = fov0; applyShift(); dirty();
  return url;
}
function stillName() {
  const site = S.site === "A" ? "breast" : S.site === "C" ? `stairs wall (the ${S.cab === "sliding" ? "sliding" : "compact"} cabinet)` : "stairs wall";
  return `Media wall v${R.VERSION || ""} - 3D - ${(VIEWS[S.view] || VIEWS.window).label.replace(/[’']/g, "")} - table on the ${site}, ${S.dining} - ${SCENES[S.scene].name}.png`;
}
qs("#r3d-save").addEventListener("click", async () => {
  const st = qs("#r3d-savest");
  const [sw, sh] = SMALL ? [2560, 1440] : [3840, 2160];   // v18: phones save at 2560 × 1440 so the picture doesn't take the room down
  st.textContent = `Rendering ${sw} × ${sh}…`;
  await new Promise(r => setTimeout(r, 30));
  const url = still(sw, sh);
  const blob = await (await fetch(url)).blob();
  const dl = (window.claude && window.claude.use) ? await window.claude.use("downloads") : null;
  if (dl) {
    try { await dl.save({ filename: stillName(), data: blob }); st.textContent = "Saved."; }
    catch (e) { st.textContent = e && e.code === "declined" ? "Not saved." : "Couldn’t save here: right-click the picture instead."; }
  } else if (!window.claude) {
    const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = stillName(); a.click(); st.textContent = "Saved.";
  } else st.textContent = "Saving isn’t available in this view.";
});

/* ---------------------------------------------------------------- the controls */
function press(attr, val) { qsa(`[data-${attr}]`).forEach(b => b.setAttribute("aria-pressed", String(b.dataset[attr] === String(val)))); }
const sameAsScene = () => LAYERS.every(k => (S.lv[k] ?? 0) === (SCENES[S.scene].levels[k] ?? 0));
function syncButtons() {
  press("site", S.site); press("dining", S.dining); press("scene", S.scene); press("tod", S.tod);
  qsa("[data-scene]").forEach(b => b.classList.toggle("adjusted", b.dataset.scene === S.scene && !(sameAsScene() && S.master === 100)));   // v25: "Bright · adjusted"
  const ln = qs("#r3d-litst"); if (ln) ln.textContent = SCENES[S.scene].name + (sameAsScene() && S.master === 100 ? "" : " · adjusted") + (S.tod === "day" ? " · daytime" : "");
  const bn = qs("#r3d-boost"); if (bn) bn.hidden = !tableOpen(); press("paint", S.paint); press("lamp", S.lamp);
  press("drawers", S.drawers ? "out" : "in"); press("quality", S.quality); press("view", S.view);
  press("ceil", S.ceil); press("skirt", S.skirt); press("plants", S.plants); press("chairs", S.chairs); press("seat", S.seat);
  press("cab", S.cab); press("tdoor", S.tdoor ? "open" : "shut");                                   // v30
  press("cam", S.cam); press("pad", S.pad ? "on" : "off"); press("foot", S.foot ? "on" : "off"); press("beside", S.beside); syncEye();   // v31
  qsa("[data-tog]").forEach(b => b.setAttribute("aria-pressed", String(!!S[b.dataset.tog])));
  qsa("[data-idea]").forEach(b => b.setAttribute("aria-pressed", String(!!S.ideas[b.dataset.idea])));
  qsa("[data-sugg]").forEach(b => b.setAttribute("aria-pressed", String(!!S.sugg[b.dataset.sugg])));
  qsa("[data-svar]").forEach(b => { const [k, v] = b.dataset.svar.split(":"); b.setAttribute("aria-pressed", String(svarOf(k) === v)); });   // v28
  let anyOn = false; qsa("[data-svrow]").forEach(r => { const on = !!S.sugg[r.dataset.svrow]; r.hidden = !on; anyOn = anyOn || on; });
  const svn = qs("#r3d-svnone"); if (svn) svn.hidden = anyOn;
  qsa("[data-decor]").forEach(b => { const [k, v] = b.dataset.decor.split(":"); b.setAttribute("aria-pressed", String(S.decor[k] === v)); });
  qs("#r3d-custom").value = S.custom;
  qsa("[data-paintcustom]").forEach(b => b.setAttribute("aria-pressed", String(S.paint === "custom" && S.custom.toLowerCase() === b.dataset.paintcustom.toLowerCase())));
  if (S.ceil !== "match" && qs("#r3d-ceil")) qs("#r3d-ceil").value = S.ceil;
  if (S.skirt !== "match" && qs("#r3d-skirt")) qs("#r3d-skirt").value = S.skirt;
  qsa("[data-lv]").forEach(i => { const k = i.dataset.lv, v = k === "master" ? S.master : (S.lv[k] ?? 0); i.value = v; qs(`[data-lvout="${k}"]`).textContent = `${Math.round(v)}%`; });
  qsa("[data-col]").forEach(i => { i.value = S.col[i.dataset.col] || WARM; });
  if (actId) renderAct();                                                                           // v30: the item's card follows
}
root.addEventListener("click", e => {
  const b = e.target.closest("button"); if (!b || !root.contains(b)) return;
  const d = b.dataset;
  if (d.view) { setView(d.view); return; }
  if (d.walk) { if (e.detail === 0) walk(d.walk); return; }   // v31: a pointer moves on pointerdown (held, it repeats); Enter or Space here
  if (d.eye) { lift(+d.eye); return; }
  if (d.level) { levelView(); return; }
  if (d.site) { S.site = d.site; applyState(); if (S.view === "dining") setView("dining"); }
  else if (d.dining) { S.dining = d.dining; S.tdoor = false; applyState(); if (S.view === "dining") setView("dining"); }   // v30: folding it shuts the door too
  else if (d.cab) { S.cab = d.cab; S.site = "C"; applyState(); if (S.view === "dining" || S.view === "chairs") setView(S.view); }   // v30: the compact or the sliding cabinet
  else if (d.tdoor) { S.tdoor = d.tdoor === "open"; if (S.tdoor && S.chairs === "open") S.chairs = "cupboard"; applyState(); }
  else if (d.scene) S.scene = d.scene, S.lv = Object.assign({}, SCENES[d.scene].levels), S.master = 100, applyLight(), updateCaption(), store.set(KEY, S);   // tapping the tile again resets it
  else if (d.tod) S.tod = d.tod, applyLight(), updateCaption(), store.set(KEY, S);
  else if (d.ceil) S.ceil = d.ceil, repaint(), store.set(KEY, S), dirty();
  else if (d.skirt) S.skirt = d.skirt, repaint(), store.set(KEY, S), dirty();
  else if (d.colreset) S.col[d.colreset] = WARM, applyLight(), store.set(KEY, S);
  else if (d.tog) S[d.tog] = !S[d.tog], applyLight(), store.set(KEY, S);
  else if (d.layer) { const [k, v] = d.layer.split(":"); S.lv = Object.assign({}, S.lv, { [k]: v === "on" ? (SCENES[S.scene].levels[k] || 60) : 0 }); applyLight(); updateCaption(); store.set(KEY, S); }   // v30: a light on or off from a card
  else if (d.sugg || d.suggall) {     // v21: a suggestion on or off (a piece you'd removed in Edit room comes back), or all of them
    const keys = d.sugg ? [d.sugg] : qsa("[data-sugg]").map(x => x.dataset.sugg), on = d.sugg ? !S.sugg[d.sugg] : d.suggall === "on";
    S.sugg = Object.assign({}, S.sugg); keys.forEach(k => { S.sugg[k] = on; if (S.layout["sg_" + k]) delete S.layout["sg_" + k].off; });
    applyState(); }
  else if (d.svar) { const [k, v] = d.svar.split(":"); S.svar = Object.assign({}, S.svar, { [k]: v }); applySvar(); placeAll(); updateCaption(); store.set(KEY, S); dirty(); }   // v28
  else if (d.tour) { tourCtl(d.tour); return; }
  else if (b.id === "r3d-tourbtn") { tourStart(); return; }
  else if (b.id === "r3d-link") { copyLook(); return; }
  else if (d.decor) {           // v20: decor; picking what's in the case (or its frame) shows the case, which hangs with the table by the stairs
    const [k, v] = d.decor.split(":"), was = S.ideas.case && S.site !== "A"; S.decor = Object.assign({}, S.decor, { [k]: v });
    if (k === "fill" || k === "frame") { S.ideas = Object.assign({}, S.ideas, { case: true }); if (S.site === "A") S.site = "C"; }   // v27: the case needs the breast free
    applyState(); if ((k === "fill" || k === "frame") && !was) setView("breast"); }
  else if (d.idea) S.ideas = Object.assign({}, S.ideas, { [d.idea]: !S.ideas[d.idea] }), applyLight(), placeAll(), updateCaption(), store.set(KEY, S);
  else if (d.plants) {           // v18: the layout puts the stand and the shelf back on their spots for it
    S.plants = d.plants; for (const k of ["plants", "records"]) if (S.layout[k]) { delete S.layout[k].x; delete S.layout[k].z; delete S.layout[k].rot; }
    applyState(); }
  else if (d.paint) S.paint = d.paint, repaint(), updateCaption(), store.set(KEY, S), dirty();
  else if (d.lamp) S.lamp = d.lamp, applyState();
  else if (d.drawers) S.drawers = d.drawers === "out", applyState();
  else if (d.chairs) { S.chairs = d.chairs; if (d.chairs === "open") S.tdoor = false; applyState(); }   // v30: one door open at a time
  else if (d.seat) S.seat = d.seat, applyState();
  else if (d.cam) S.cam = d.cam, applyCam(), store.set(KEY, S);
  else if (d.moment) { playMoment(d.moment); return; }                                              // v31
  else if (d.showopen) { showOpen(); return; }
  else if (d.beside) { S.beside = d.beside; if (d.beside !== "clear") { S.site = "C"; S.cab = "compact"; } applyState(); }   // v31
  else if (d.foot) { S.foot = d.foot === "on"; if (S.foot) { S.site = "C"; S.dining = "folded"; } applyState(); }
  else if (d.pad) S.pad = d.pad === "on", applyPad(), store.set(KEY, S);
  else if (d.quality) S.quality = d.quality, S.picked = true, applyLight(), store.set(KEY, S);
  else if (b.id === "r3d-full") { const st = document.documentElement; (document.fullscreenElement ? document.exitFullscreen() : st.requestFullscreen?.())?.catch?.(() => {}); return; }
  else if (d.paintcustom) S.custom = d.paintcustom, S.paint = "custom", repaint(), updateCaption(), store.set(KEY, S), dirty();   // v25: Deep green, a ready-made custom colour
  else if (b.id === "r3d-reset") { setView(S.view); return; }
  else return;
  syncButtons();
});
qs("#r3d-custom").addEventListener("input", e => { S.custom = e.target.value; S.paint = "custom"; repaint(); syncButtons(); updateCaption(); store.set(KEY, S); dirty(); });
// v15: the sliders, the colour bulbs, and the ceiling and skirting paints
root.addEventListener("input", e => {
  const t = e.target, d = t.dataset;
  if (d.lv) { const v = +t.value; if (d.lv === "master") S.master = v; else S.lv[d.lv] = v; qs(`[data-lvout="${d.lv}"]`).textContent = `${v}%`; syncButtons(); applyLight(); updateCaption(); }
  else if (d.col) { S.col[d.col] = t.value; applyLight(); }
  else if (t.id === "r3d-ceil") { S.ceil = t.value; press("ceil", ""); repaint(); dirty(); }
  else if (t.id === "r3d-skirt") { S.skirt = t.value; press("skirt", ""); repaint(); dirty(); }
  else if (t.id === "r3d-eye") { lift(+t.value); const o = qs("#r3d-eyeout"); if (o) o.textContent = `${t.value} cm`; return; }   // v31
  else return;
  store.set(KEY, S);
});

/* ---------------------------------------------------------------- go: built the first time the room is on screen (v14.1) */
let started = false;
function start() {
  started = true;
  const t0 = performance.now();
  const pmrem = new THREE.PMREMGenerator(gl);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  pmrem.dispose();
  gl.localClippingEnabled = true;
  buildShell(); buildLights(); buildFurniture(); buildSuggest(); buildSeatAndPouf();
  bar1 = buildBar(R.BAR1, lights.bar1, "bar1");
  gl.shadowMap.enabled = S.quality === "hd";
  cabSnap = true; applyState(); cabSnap = false;          // v30: the doors start where they are, no swing
  syncButtons();
  scene.traverse(o => { if (o.isMesh || o.isPoints || o.isLine) [].concat(o.material).forEach(m => m && !m.clippingPlanes && clipMat(m)); });   // v21: the cutaway
  setView(S.view, true);
  applyCam(S.cam === "look"); applyPad();                                               // v31
  sizeRenderer();
  gl.compile(scene, camera);
  msg.hidden = true;
  root.classList.add("ready");
  requestAnimationFrame(frame);
  lookFromHash();                                                                       // v28: a shared #look- link (after the first compile, so its note shows)
  try {                                                                                 // v30: once, say the room's things can be tapped
    if (!localStorage.getItem("mw30-taphint") && !/^#look-/.test(location.hash)) { setTimeout(() => toast("Tip: tap the dining cabinet, the drawers or the lamp to work them"), 1800); localStorage.setItem("mw30-taphint", "1"); }
  } catch (e) {}
  // for the headless stills (shot3d.py): set the options and a view, then take a picture
  window.R3D = {
    set(o) { oldScene(o); Object.assign(S, o); S.decor = Object.assign({}, DEF.decor, o.decor || S.decor); if (o.scene && !o.lv) S.lv = Object.assign({}, SCENES[o.scene].levels); if (o.quality) S.picked = true; cabSnap = true; applyState(); cabSnap = false; syncButtons(); if (o.view) setView(o.view, true); },
    still, ready: true, buildMs: Math.round(performance.now() - t0), _dbg: { gl, scene, lights, THREE, S, MOV, UNDO, camera, controls, VIEWS, MATS, OAK_TEX },
    bench(n = 30) {   // ms per frame while orbiting at full resolution, for tuning
      const t = performance.now();
      for (let i = 0; i < n; i++) { controls.rotateLeft ? controls.rotateLeft(0.01) : 0; camera.position.applyAxisAngle(new THREE.Vector3(0, 1, 0), 0.004); camera.lookAt(controls.target); gl.render(scene, camera); }
      const px = new Uint8Array(4); const c = gl.getContext(); c.readPixels(0, 0, 1, 1, c.RGBA, c.UNSIGNED_BYTE, px);
      return (performance.now() - t) / n;
    },
  };
  if (window.__r3dPending) { window.R3D.set(window.__r3dPending); window.__r3dPending = null; }
}
window.addEventListener("r3d-set", e => { if (window.R3D) window.R3D.set(e.detail); else window.__r3dPending = e.detail; });
