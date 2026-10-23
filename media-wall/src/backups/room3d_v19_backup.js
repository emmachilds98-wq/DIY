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
const DEF = { site: "B", dining: "folded", scene: "general", paint: "card_room", custom: "#899081", lamp: "corner", drawers: false,
              quality: SMALL ? "fast" : "hd", view: "window",
              // v15: every light on a slider (the scenes fill them in), the smart bars and the lamp in any colour, ceiling and skirting paints
              lv: null, master: 100, col: { strips: WARM, bar1: WARM, bar2: WARM, lamp0: R.LAMP_RGB[0], lamp1: R.LAMP_RGB[1], lamp2: R.LAMP_RGB[2] },
              ceil: "match", skirt: "match", laser: false, lbox: true, curtains: false, pc: true, ideas: {},   // v17: ideas all off
              // v18: the plant stand and the record shelf's layout, your own moves (edit mode) and the things you've added; the grow lights
              plants: "corner", layout: {}, added: [], grow: true,
              chairs: "hooks" };   // v19: two folded chairs on hooks at the table's window end ("away": in the garage)
DEF.lamp = R.LAMP_DEFAULT || "sofa";   // v18: the window corner holds the plant stand or the record shelf   // v16: the table by the stairs by default; the laser off
const KEY = "mw18-3d";
const S = Object.assign({}, DEF, store.get(KEY, {}));
S.col = Object.assign({}, DEF.col, S.col || {});
if (!S.ideas || typeof S.ideas !== "object") S.ideas = {};
if (!S.layout || typeof S.layout !== "object" || Array.isArray(S.layout)) S.layout = {};
if (!Array.isArray(S.added)) S.added = [];
if (!(S.plants in R.PLANT_LAYOUTS)) S.plants = DEF.plants;
S.edit = false;
if (!(S.paint in R.PAINTS) && S.paint !== "custom") S.paint = DEF.paint;

/* ---------------------------------------------------------------- the lighting scenes (scenes.py) plus daytime */
const SCENES = JSON.parse(document.getElementById("scenes-data").textContent);
SCENES.day = { name: "Daytime", levels: { strip: 0, uprights: 0, bias: 0, bar1: 0, bar2: 0, lamp: 0 }, day: true };
if (!(S.scene in SCENES)) S.scene = DEF.scene;
const LAYERS = ["strip", "uprights", "bias", "bar1", "bar2", "lamp"];
if (!S.lv) S.lv = Object.assign({}, SCENES[S.scene].levels);
const lvl = k => Math.max(0, Math.min(100, (S.lv[k] ?? 0) * S.master / 100));   // a layer's level after the master slider

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
controls.addEventListener("change", () => dirty());

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
const reg = m => (MATS.push(m), m);
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
function kindOf(fill, flags, size) {
  if (fill === "glass") return "glass";
  if (fill === "art") return "art";
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
    plain: () => new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.72 }),
    dark: () => new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.42, metalness: 0.05 }),
    fabric: () => new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.9, bumpMap: CORD, bumpScale: 0.9 }),
    led: () => new THREE.MeshBasicMaterial({ vertexColors: true, toneMapped: false }),
    glass: () => new THREE.MeshPhysicalMaterial({ color: "#ffffff", roughness: 0.04, transmission: 0, transparent: true, opacity: 0.16, depthWrite: false }),
    art: () => new THREE.MeshStandardMaterial({ map: ART_TEX, roughness: 0.5 }),
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
  const egg = paintMat(lum("#346650") / BASE_L, true, false, "trim"), doorP = paintMat(lum("#2a5340") / BASE_L, true, false, "trim");
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
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(Wd * M, (RZ - WZ) * M), reg(new THREE.MeshStandardMaterial({ map: CARPET, roughness: 1, bumpMap: PILE, bumpScale: 0.5 })));
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
  cube(dx0 - 6, 0, RZ - 1.5, 6, R.DOOR_H + 6, 2, egg); cube(dx1, 0, RZ - 1.5, 6, R.DOOR_H + 6, 2, egg);
  cube(dx0 - 6, R.DOOR_H, RZ - 1.5, dx1 - dx0 + 12, 6, 2, egg);
  cube(dx0, 0, RZ + 1, dx1 - dx0, R.DOOR_H, 4, doorP);
  for (const [y0, y1] of [[14, 98], [112, 186]]) cube(dx0 + 9, y0, RZ + 0.6, dx1 - dx0 - 18, y1 - y0, 0.5, doorP);
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
  { const cw = cof.x[1] - cof.x[0], cd = cof.z[1] - cof.z[0], g = new THREE.Group();     // v18: movable in edit mode
    lb(g, 0, 38, 0, cw, 4, cd, cofM);
    for (const [x, z] of [[-cw / 2 + 5, -cd / 2 + 5], [cw / 2 - 5, -cd / 2 + 5], [-cw / 2 + 5, cd / 2 - 5], [cw / 2 - 5, cd / 2 - 5]]) lb(g, x, 0, z, 4, 38, 4, cofM);
    movable("coffee", "Coffee table", g, () => ({ x: (cof.x[0] + cof.x[1]) / 2, z: (cof.z[0] + cof.z[1]) / 2, rot: 0 }), cw, cd, [cofM]); }
  // v15: the rug, 230 × 160 in front of the sofa (geometry.RUG), with its design and a little thickness
  const RG = R.RUG, rugW = RG.x[1] - RG.x[0], rugD = RG.z[1] - RG.z[0];
  const rug = new THREE.Mesh(new THREE.BoxGeometry(rugW * M, 0.008, rugD * M),
    [0, 1, 2, 3, 4, 5].map(i => i === 2 ? reg(new THREE.MeshStandardMaterial({ map: RUG_TEX, roughness: 0.97, bumpMap: PILE, bumpScale: 0.35 }))
                                        : reg(new THREE.MeshStandardMaterial({ color: RG.cols[3], roughness: 1 }))));
  rug.position.y = 0.004; rug.rotation.y = Math.PI; rug.receiveShadow = true;
  { const g = new THREE.Group(); g.add(rug);
    movable("rug", "Rug", g, () => ({ x: (RG.x[0] + RG.x[1]) / 2, z: (RG.z[0] + RG.z[1]) / 2, rot: 0 }), rugW, rugD, [], true); }
  // v15: the curtains, from the client's photo: long pencil-pleat panels to the floor in oatmeal, on a rail just under the ceiling strip
  // running 30 past the window each side; open (stacked either side) or drawn across (S.curtains)
  // "hessian curtains from dunelm with a wood rail": a coarse natural weave, on a 28 mm wooden pole with rings and ball finials
  const CU = R.CURTAIN, cloth = reg(new THREE.MeshStandardMaterial({ color: CU.col, roughness: 1, side: THREE.DoubleSide, map: HESSIAN, bumpMap: HESSIAN, bumpScale: 0.8 }));
  const wood = reg(new THREE.MeshStandardMaterial({ color: CU.pole_col, map: OAK_TEX, roughness: 0.5 }));
  const poleL = wx1 - wx0 + 2 * CU.ext, pole = new THREE.Mesh(new THREE.CylinderGeometry(CU.pole / 2 * M, CU.pole / 2 * M, poleL * M, 16), wood);
  pole.rotation.z = Math.PI / 2; pole.position.copy(v3((wx0 + wx1) / 2, CU.rail_y + CU.pole / 2, CU.z + 1)); shell.add(shadow(pole));
  for (const xf of [wx0 - CU.ext - CU.finial / 2, wx1 + CU.ext + CU.finial / 2]) {
    const f = new THREE.Mesh(new THREE.SphereGeometry(CU.finial / 2 * M, 16, 12), wood); f.position.copy(v3(xf, CU.rail_y + CU.pole / 2, CU.z + 1)); shell.add(shadow(f));
  }
  for (let x = wx0 - CU.ext + 3; x < wx1 + CU.ext - 2; x += 10) {          // rings, one every 10 cm
    const r = new THREE.Mesh(new THREE.TorusGeometry(0.02, 0.0035, 6, 16), wood); r.position.copy(v3(x, CU.rail_y + CU.pole / 2, CU.z + 1)); r.rotation.y = Math.PI / 2; shell.add(r);
  }
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
  const sb = R.SHELF_B, black = reg(new THREE.MeshStandardMaterial({ color: "#1a1a1b", roughness: 0.55 }));
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
  buildChairStore();
  flushCubes(shell);
}
/* v19: two folded FRÖSVI chairs on BJÄRNUM hooks, one above the other, between the table's window end and the pipe boxing */
let chairStore = null;
function buildChairStore() {
  const CS = R.CHAIR_STORE, H = CS.hooks, [cw, cdep, ch] = R.CHAIR_FOLDED;
  const g = new THREE.Group(); g.name = "chairs";
  const wood = reg(new THREE.MeshStandardMaterial({ color: "#b07f50", map: OAK_TEX, roughness: 0.6 }));
  const pad = reg(new THREE.MeshStandardMaterial({ color: "#77736b", roughness: 0.92 }));
  const alu = reg(new THREE.MeshStandardMaterial({ color: "#b9bcc0", roughness: 0.35, metalness: 0.8 }));
  const bx = (x, y, z, w, h, d, m) => { const me = new THREE.Mesh(new THREE.BoxGeometry(w * M, h * M, d * M), m); me.position.copy(v3(x + w / 2, y + h / 2, z + d / 2)); g.add(shadow(me)); };
  const cz = (H.z[0] + H.z[1]) / 2, x0 = H.x - 1 - cdep;                       // each chair's face: 9 thick, its back an inch off the wall
  H.chair_y.forEach(([y0, y1], i) => {
    for (const sd of [-1, 1]) bx(x0, y0, cz + sd * (cw / 2 - 1.5) - 1.5, cdep, ch, 3, wood);   // the frames, legs folded together
    bx(x0 + 1.5, y0 + 28, cz - (cw / 2 - 3), 2.2, 38, cw - 6, pad);                             // the seat, folded up
    bx(x0 + 4, y1 - 27, cz - (cw / 2 - 3), 3, 22, cw - 6, pad);                                  // the padded back
    bx(x0 + 2, y0 + 12, cz - (cw / 2 - 3), 1.8, 3, cw - 6, wood);                                // a stretcher low down
    bx(H.x - R.HOOK[1], H.hook_y[i] - 1, cz - R.HOOK[0] / 2, R.HOOK[1], 1.6, R.HOOK[0], alu);   // the hook through the hole in its back
  });
  scene.add(g); chairStore = g;
}
/* v17: the ideas (ideas.py), each its own group, all hidden until its button is on */
const IDEA_G = {};
let ideaLed;
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
  // 1. the slim glass display case on the breast (it faces the room: the breast's face is z = 0)
  { const g = IDEA_G.case = new THREE.Group(), C = I.case, [x0, x1] = C.x, [y0, y1] = C.y, d = C.d, f = C.frame, z0 = -d;
    ibox(g, x0, y0, -1, x1 - x0, y1 - y0, 1, oak);                                  // the back
    ibox(g, x0, y0, z0, f, y1 - y0, d - 1, oak); ibox(g, x1 - f, y0, z0, f, y1 - y0, d - 1, oak);
    ibox(g, x0, y0, z0, x1 - x0, f, d - 1, oak); ibox(g, x0, y1 - f, z0, x1 - x0, f, d - 1, oak);
    ibox(g, x0 + f, (y0 + y1) / 2 - 0.3, z0 + 1, x1 - x0 - 2 * f, 0.6, d - 2, glassM, false);   // a glass shelf
    ibox(g, x0, y0, z0 - 0.4, x1 - x0, y1 - y0, 0.4, glassM, false);                       // the toughened glass front
    ideaLed = new THREE.MeshBasicMaterial({ color: "#fff1d6", toneMapped: false });
    ibox(g, x0 + f, y1 - f - 0.5, z0 + 2, x1 - x0 - 2 * f, 0.5, 1.2, ideaLed, false);
    // collectibles: a cap on its button top, small boxes and figures
    const cols = ["#1d2a4a", "#a33b2b", "#e2c35a", "#2f6b5a", "#d9d4c7"].map(c => reg(new THREE.MeshStandardMaterial({ color: c, roughness: 0.6 })));
    const ym = (y0 + y1) / 2 + 0.3, xs = [x0 + 12, x0 + 30, x0 + 50, x0 + 70];
    xs.forEach((x, i) => ibox(g, x, y0 + f, z0 + 3, 7 + (i % 2) * 3, 8 + (i % 3) * 4, 5, cols[i % cols.length]));
    const cap = new THREE.Mesh(new THREE.SphereGeometry(0.07, 20, 10, 0, Math.PI * 2, 0, Math.PI / 2), cols[0]); cap.position.copy(v3(x0 + 22, ym, z0 + 6)); g.add(shadow(cap));
    const brim = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.006, 0.06), cols[0]); brim.position.copy(v3(x0 + 22, ym + 0.3, z0 + 1.5)); g.add(brim);
    xs.slice(1).forEach((x, i) => ibox(g, x + 3, ym, z0 + 4, 5, 9 + i * 3, 4, cols[(i + 2) % cols.length]));
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
  const b2 = `${S.site}_${S.dining}`;
  if (built.bar2 !== b2) { if (bar2) drop(bar2, lights.bar2); bar2 = buildBar(R.BAR2[b2], lights.bar2, "bar2"); built.bar2 = b2; }
  const lk = S.lamp + JSON.stringify(S.layout.lamp || {});
  if (built.lamp !== lk) { buildLamp(); built.lamp = lk; }
  if (G.now_ledge) G.now_ledge.visible = S.site === "B" && S.plants !== "breast";   // v18: with the plants on the breast the ledge comes off
  if (chairStore) chairStore.visible = S.chairs !== "away" && S.dining === "folded";  // v19: at dinner they're the chairs you're sitting on
  placeAll();
  repaint();
  applyLight();
  updateCaption();
  store.set(KEY, S);
  dirty();
}
function applyLight() {
  const sc = SCENES[S.scene], day = !!sc.day, hd = S.quality === "hd";
  const L = {}; LAYERS.forEach(k => L[k] = lvl(k));          // v15: the sliders (a scene button fills them in), times the master
  const set = (list, lv) => list.forEach(l => {
    l.intensity = (l.userData.k || 1) * Math.pow(lv / 100, 1.6);
    l.visible = lv > 0;
    if (l.userData.colKey) l.color.set(S.col[l.userData.colKey] || WARM);   // the smart bulbs' colour
    if (l.isSpotLight) { l.castShadow = hd && lv > 0; if (l.userData.glow) l.userData.glow.material.color.set(lv > 0 ? (S.col[l.userData.colKey] || "#fff3dc") : "#3a3a3a"); }
  });
  const area = hd ? 1 : 0;      // Fast leaves out the area lights (the most expensive) and lifts the fill to make up
  set(lights.strip, L.strip * area); set(lights.uprights, L.uprights * area); set(lights.bias, L.bias * area); set(lights.bar1, L.bar1); set(lights.bar2, L.bar2);
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
  for (const [k, g] of Object.entries(IDEA_G)) g.visible = !!S.ideas[k] && (k !== "case" || S.site === "B");   // v17: ideas, off by default
  if (G.frames) G.frames.visible = !(S.ideas.case && S.site === "B");                                         // the case replaces the frames
  if (G.frames) G.frames.position.y = S.site === "B" && S.plants === "breast" ? 0.3 : 0;                        // v18.1: up 30 over the 158 plant stand
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
function movable(id, label, g, def, w, d, mats, flat = false, extra = {}) {
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
  { const g = new THREE.Group(), wood = reg(new THREE.MeshStandardMaterial({ color: PS.col, map: OAK_TEX, roughness: 0.6 }));
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
  { const g = new THREE.Group(), wood = reg(new THREE.MeshStandardMaterial({ color: RS.col, map: OAK_TEX, roughness: 0.65 }));
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
function clampItem(it, x, z, rot) {
  const q = ((rot % 180) + 180) % 180, hx = q === 90 ? it.d / 2 : q === 0 ? it.w / 2 : Math.max(it.w, it.d) / 2, hz = q === 90 ? it.w / 2 : q === 0 ? it.d / 2 : hx;
  x = Math.min(Math.max(x, hx), R.W - hx);
  const zmax = x + hx <= R.ALC_W ? R.ALC_D : x - hx >= R.BREAST_X[1] ? R.RECESS_Z : 0;
  z = Math.min(Math.max(z, R.WINDOW_Z + hz), zmax - hz);
  // v19: within 5 cm of a wall, it goes flush against it
  if (x - hx < SNAP) x = hx; else if (R.W - hx - x < SNAP) x = R.W - hx;
  if (z - hz - R.WINDOW_Z < SNAP) z = R.WINDOW_Z + hz; else if (zmax - hz - z < SNAP) z = zmax - hz;
  return { x: Math.round(x), z: Math.round(z) };
}
const SNAP = 5;
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
    const lab = { walls: "Walls", ceil: "Ceiling", skirt: "Skirting, door and radiator" }[selSurf];
    qs("#r3d-selname").textContent = lab;
    const wallHex = S.paint === "custom" ? S.custom : R.PAINTS[S.paint].hex, key = selSurf === "ceil" ? "ceil" : "skirt";
    const cur = selSurf === "walls" || S[key] === "match" ? wallHex : S[key];
    qs("#r3d-selcol").value = cur; qs("#r3d-swatches").hidden = false;
    qs("#r3d-swatches").innerHTML = (selSurf === "walls" ? Object.entries(R.PAINTS).map(([k, { hex: h, name: n }]) => `<button type="button" class="chip" data-swatch="${k}"><span class="dot" style="background:${h}"></span>${n.replace(/ No\..*/, "").replace("Farrow & Ball ", "").replace("Little Greene ", "")}</button>`).join("")
      : `<button type="button" class="chip" data-swatch="match">Same as the walls</button><button type="button" class="chip" data-swatch="${selSurf === "ceil" ? "#f2f0ea" : "#ece8dd"}">${selSurf === "ceil" ? "White" : "Off-white"}</button>`);
    qsa("[data-sel=turn],[data-sel=remove],[data-sel=copy]").forEach(b => b.hidden = true); qs("#r3d-selsize").textContent = "";
    return;
  }
  if (!selId) return;
  const it = MOV[selId], L = S.layout[selId] || {};
  qs("#r3d-selname").textContent = it.label;
  qs("#r3d-selsize").textContent = it.w && it.d ? `${Math.round(it.w)} × ${Math.round(it.d)} cm` : "";   // v19: its footprint
  qsa("[data-sel=copy]").forEach(b => b.hidden = !it.added);
  qs("#r3d-swatches").hidden = true;
  qsa("[data-sel=turn]").forEach(b => b.hidden = !!it.lamp);
  qsa("[data-sel=remove]").forEach(b => b.hidden = false);
  qs("#r3d-selcol").parentElement.hidden = !it.mats.length;
  if (it.mats.length) qs("#r3d-selcol").value = L.col || it.base[0];
}
function setEdit(on) {
  S.edit = on; root.classList.toggle("editing", on);
  qs("#r3d-editbtn").setAttribute("aria-pressed", String(on));
  qs("#r3d-editbar").hidden = !on;
  if (on) { preEditView = S.view; if (!(VIEWS[S.view] || {}).above) setView("doll"); }
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
  if (!f) return;
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
  if (k === "turn" || k === "remove" || k === "copy") pushUndo();
  if (k === "copy" && it.added) {     // v19: another of the same, a little way off, turned and coloured the same
    const src = S.added.find(a => a.id === selId), p = spotOf(selId), L = S.layout[selId] || {}, c = clampItem(it, p.x + 25, p.z + 25, p.rot);
    const a = { id: "a" + Date.now().toString(36), type: src.type, x: c.x, z: c.z };
    addThing(a); setLayout(a.id, { rot: p.rot, col: L.col }); placeAll(); store.set(KEY, S); select(a.id); applyState(); return;
  }
  if (k === "turn") { const p = spotOf(selId), rot = (p.rot + 45) % 360, c = clampItem(it, p.x, p.z, rot); setLayout(selId, { rot, x: c.x, z: c.z }); placeAll(); store.set(KEY, S); }
  if (k === "remove") {
    if (it.added) { movers.remove(it.pivot); delete MOV[selId]; S.added = S.added.filter(a => a.id !== selId); delete S.layout[selId]; }
    else { setLayout(selId, { off: true }); if (it.lamp) built.lamp = null; }
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
/* v18: if the graphics card gives up (most often HD with shadows on a phone), say so and come back in Fast */
canvas.addEventListener("webglcontextlost", e => {
  e.preventDefault(); S.quality = "fast"; S.picked = true; store.set(KEY, S);
  msg.hidden = false; root.classList.remove("ready");
  msg.innerHTML = 'The 3D room ran out of graphics memory (HD with shadows asks a lot of a phone). <button type="button" class="btn" onclick="location.reload()">Reload it in Fast</button>';
});

/* ---------------------------------------------------------------- views */
const VIEWS = {
  window:  { label: "From the window", eye: [292, 158, -298], at: [196, 96, 10], fov: 66 },
  wall:    { label: "The media wall", eye: [140, 128, -285], at: [93, 108, 20], fov: 52 },
  sofa:    { label: "From the sofa", eye: [62, 104, -255], at: [72, 112, 20], fov: 58 },
  door:    { label: "From the door", eye: [372, 165, -6], at: [110, 85, -210], fov: 64 },
  stairs:  { label: "From the stairs", eye: [438, 205, 4], at: [190, 70, -205], fov: 62 },
  dining:  { label: "The dining table", A: { eye: [250, 140, -262], at: [246, 88, 0] }, B: { eye: [190, 150, -172], at: [467, 126, -182] }, fov: 56 },
  chairs:  { label: "The chairs on their hooks", eye: [300, 168, -140], at: [467, 98, -258], fov: 42 },   // v19
  windowwall: { label: "The window wall", eye: [236, 150, -70], at: [236, 120, -309], fov: 66 },   // v17: for the ideas' stills
  breast:  { label: "The chimney breast", eye: [246, 140, -250], at: [246, 120, 0], fov: 54 },   // v17: for the ideas' stills
  pc:      { label: "The PC side wall", eye: [345, 135, -168], at: [0, 112, -168], fov: 56 },
  plan:    { label: "Bird’s eye", eye: [233.5, 1150, -135], at: [233.5, 0, -134.9], fov: 30, above: true },
  doll:    { label: "Dolls’ house", eye: [780, 560, -700], at: [230, 60, -120], fov: 40, above: true },
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
function walk(kind) {        // about 15 cm a press on the floor plane; turns 10°
  if (tween) return;
  walked = true; controls.maxDistance = 6;
  const fwd = controls.target.clone().sub(camera.position); fwd.y = 0;
  if (fwd.lengthSq() < 1e-8) fwd.set(0, 0, 1);
  fwd.normalize();
  const side = new THREE.Vector3(-fwd.z, 0, fwd.x), step = 0.15;
  if (kind === "tl" || kind === "tr") {
    const off = controls.target.clone().sub(camera.position).applyAxisAngle(new THREE.Vector3(0, 1, 0), (kind === "tl" ? 1 : -1) * Math.PI / 18);
    controls.target.copy(camera.position).add(off);
  } else {
    const d = kind === "f" ? fwd.multiplyScalar(step) : kind === "b" ? fwd.multiplyScalar(-step) : kind === "r" ? side.multiplyScalar(step) : side.multiplyScalar(-step);
    camera.position.add(d); controls.target.add(d);
  }
  clampRoom(camera.position); clampRoom(controls.target, true);
  controls.update(); dirty();
}
const WALK_KEYS = { w: "f", arrowup: "f", s: "b", arrowdown: "b", a: "l", arrowleft: "l", d: "r", arrowright: "r", q: "tl", e: "tr" };
root.addEventListener("keydown", e => {
  if (e.altKey || e.ctrlKey || e.metaKey || /^(input|select|textarea)$/i.test(e.target.tagName)) return;
  if (e.target.tagName === "BUTTON" && !e.target.dataset.walk && e.key.startsWith("Arrow")) return;   // arrows still move between buttons
  const k = WALK_KEYS[e.key.toLowerCase()]; if (!k) return;
  e.preventDefault(); walk(k);
});
canvas.addEventListener("pointerdown", () => canvas.focus({ preventScroll: true }));
function setView(name, instant) {
  const v = VIEWS[name] || VIEWS.window; S.view = name;
  walked = false; controls.maxDistance = v.above ? 16 : 6;
  const p = v[S.site] || v;
  const eye = v3(...p.eye), at = v3(...p.at);
  const from = { eye: camera.position.clone(), at: controls.target.clone(), fov: camera.fov };
  setAbove(!v.above);
  if (instant) { camera.position.copy(eye); controls.target.copy(at); camera.fov = v.fov; camera.updateProjectionMatrix(); controls.update(); dirty(); }
  else tween = { t0: performance.now(), from, to: { eye, at, fov: v.fov } };
  qsa("[data-view]").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.view === name)));
  store.set(KEY, S); updateCaption();
}
function setAbove(show) {   // the floor above (the stairwell's upper walls) hides in the views from above
  scene.traverse(o => { if (o.name === "above") o.visible = show; });
  view.visible = show;
}

/* ---------------------------------------------------------------- render loop, only when something changed */
let need = 2, moving = false, still_t = 0, lowRes = false;
function dirty() { need = Math.max(need, 2); }
function fullRatio() { return S.quality === "hd" ? Math.min(window.devicePixelRatio || 1, 1.5) : Math.min(window.devicePixelRatio || 1, 1) * 0.85; }
function sizeRenderer() {
  const w = canvas.clientWidth, h = canvas.clientHeight;
  if (!w || !h) return;
  if (!started) { start(); return; }
  // v14.1: while you drag, the picture renders at a lower resolution; it sharpens again as soon as you stop
  gl.setPixelRatio(lowRes ? Math.max(0.5, fullRatio() * 0.5) : fullRatio());
  gl.setSize(w, h, false);
  camera.aspect = w / h; camera.updateProjectionMatrix(); dirty();
}
new ResizeObserver(sizeRenderer).observe(canvas);
controls.addEventListener("start", () => { moving = true; });
controls.addEventListener("end", () => { moving = false; });
function frame(now) {
  requestAnimationFrame(frame);
  if (!canvas.clientWidth) return;
  if (tween) {
    const k = Math.min(1, (now - tween.t0) / 900), e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
    camera.position.lerpVectors(tween.from.eye, tween.to.eye, e);
    controls.target.lerpVectors(tween.from.at, tween.to.at, e);
    camera.fov = tween.from.fov + (tween.to.fov - tween.from.fov) * e; camera.updateProjectionMatrix();
    if (k >= 1) tween = null;
    need = 2;
  }
  const changed = controls.update();
  if (changed) need = 2;
  if (!tween && !freeAbove() && (clampRoom(camera.position) | clampRoom(controls.target, true))) need = 2;   // v17: never outside the room
  const active = moving || changed || !!tween;
  if (active) { still_t = now; if (!lowRes) { lowRes = true; sizeRenderer(); } }
  else if (lowRes && now - still_t > 180) { lowRes = false; sizeRenderer(); }
  if (need > 0) {
    const t = probe > 0 && !lowRes ? performance.now() : 0;
    gl.render(scene, camera); need--;
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
  const sc = SCENES[S.scene];
  const site = S.site === "A" ? "Table on the chimney breast" : "Table under the shelf by the stairs";
  const din = { folded: "folded on the wall", four: "open on its gate leg, for four", six: "open on its gate leg, for six" }[S.dining];
  const paint = S.paint === "custom" ? `your colour ${S.custom}` : R.PAINTS[S.paint].name;
  const lights = sameAsScene() && S.master === 100 ? sc.name : `your lighting (from ${sc.name})`;
  qs("#r3d-cap").textContent = `${(VIEWS[S.view] || VIEWS.window).label} · ${site}, ${din} · ${lights} · ${paint}${S.drawers ? " · drawers out" : ""}${Object.values(S.ideas).some(Boolean) ? " · ideas shown (not in the plan)" : ""}`;
}
function still(w, h) {
  if (!started) start();
  const pr = gl.getPixelRatio(), size = gl.getSize(new THREE.Vector2()), asp = camera.aspect;
  gl.setPixelRatio(1); gl.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
  const was = gl.shadowMap.enabled, wasQ = S.quality; gl.shadowMap.enabled = true; gl.shadowMap.type = THREE.PCFSoftShadowMap;
  if (wasQ !== "hd") { S.quality = "hd"; applyLight(); gl.shadowMap.enabled = true; }
  const big = SMALL ? 1024 : 2048;   // v18: phones keep 1024 maps for the picture, and at most six spots cast shadows
  Object.values(lights).flat().forEach(l => { if (l.isSpotLight && l.visible) { l.castShadow = true; l.shadow.mapSize.set(big, big); if (l.shadow.map) { l.shadow.map.dispose(); l.shadow.map = null; } } });
  capShadows(Math.max(0, Math.min(6, (gl.capabilities.maxTextures || 16) - 10)));
  MATS.forEach(m => m.needsUpdate = true);
  reshadow();
  gl.render(scene, camera);
  const url = canvas.toDataURL("image/png");
  gl.shadowMap.type = THREE.PCFShadowMap; S.quality = wasQ;
  gl.shadowMap.enabled = was;
  MATS.forEach(m => m.needsUpdate = true);
  Object.values(lights).flat().forEach(l => { if (l.isSpotLight) { l.shadow.mapSize.set(1024, 1024); if (l.shadow.map) { l.shadow.map.dispose(); l.shadow.map = null; } } });
  applyLight();
  gl.setPixelRatio(pr); gl.setSize(size.x, size.y, false); camera.aspect = asp; camera.updateProjectionMatrix(); dirty();
  return url;
}
function stillName() {
  const site = S.site === "A" ? "breast" : "stairs wall";
  return `Media wall v19 - 3D - ${(VIEWS[S.view] || VIEWS.window).label.replace(/[’']/g, "")} - table on the ${site}, ${S.dining} - ${SCENES[S.scene].name}.png`;
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
  press("site", S.site); press("dining", S.dining); press("scene", sameAsScene() ? S.scene : ""); press("paint", S.paint); press("lamp", S.lamp);
  press("drawers", S.drawers ? "out" : "in"); press("quality", S.quality); press("view", S.view);
  press("ceil", S.ceil); press("skirt", S.skirt); press("plants", S.plants); press("chairs", S.chairs);
  qsa("[data-tog]").forEach(b => b.setAttribute("aria-pressed", String(!!S[b.dataset.tog])));
  qsa("[data-idea]").forEach(b => b.setAttribute("aria-pressed", String(!!S.ideas[b.dataset.idea])));
  qs("#r3d-custom").value = S.custom;
  if (S.ceil !== "match" && qs("#r3d-ceil")) qs("#r3d-ceil").value = S.ceil;
  if (S.skirt !== "match" && qs("#r3d-skirt")) qs("#r3d-skirt").value = S.skirt;
  qsa("[data-lv]").forEach(i => { const k = i.dataset.lv, v = k === "master" ? S.master : (S.lv[k] ?? 0); i.value = v; qs(`[data-lvout="${k}"]`).textContent = `${Math.round(v)}%`; });
  qsa("[data-col]").forEach(i => { i.value = S.col[i.dataset.col] || WARM; });
}
root.addEventListener("click", e => {
  const b = e.target.closest("button"); if (!b || !root.contains(b)) return;
  const d = b.dataset;
  if (d.view) { setView(d.view); return; }
  if (d.walk) { walk(d.walk); return; }
  if (d.site) { S.site = d.site; applyState(); if (S.view === "dining") setView("dining"); }
  else if (d.dining) S.dining = d.dining, applyState();
  else if (d.scene) S.scene = d.scene, S.lv = Object.assign({}, SCENES[d.scene].levels), applyLight(), updateCaption(), store.set(KEY, S);
  else if (d.ceil) S.ceil = d.ceil, repaint(), store.set(KEY, S), dirty();
  else if (d.skirt) S.skirt = d.skirt, repaint(), store.set(KEY, S), dirty();
  else if (d.colreset) S.col[d.colreset] = WARM, applyLight(), store.set(KEY, S);
  else if (d.tog) S[d.tog] = !S[d.tog], applyLight(), store.set(KEY, S);
  else if (d.idea) S.ideas = Object.assign({}, S.ideas, { [d.idea]: !S.ideas[d.idea] }), applyLight(), placeAll(), updateCaption(), store.set(KEY, S);
  else if (d.plants) {           // v18: the layout puts the stand and the shelf back on their spots for it
    S.plants = d.plants; for (const k of ["plants", "records"]) if (S.layout[k]) { delete S.layout[k].x; delete S.layout[k].z; delete S.layout[k].rot; }
    applyState(); }
  else if (d.paint) S.paint = d.paint, repaint(), updateCaption(), store.set(KEY, S), dirty();
  else if (d.lamp) S.lamp = d.lamp, applyState();
  else if (d.drawers) S.drawers = d.drawers === "out", applyState();
  else if (d.chairs) S.chairs = d.chairs, applyState();
  else if (d.quality) S.quality = d.quality, S.picked = true, applyLight(), store.set(KEY, S);
  else if (b.id === "r3d-full") { const st = qs(".r3d-stage"); (document.fullscreenElement ? document.exitFullscreen() : st.requestFullscreen?.())?.catch?.(() => {}); return; }
  else if (b.id === "r3d-reset") { setView(S.view); return; }
  else return;
  syncButtons();
});
qs("#r3d-custom").addEventListener("input", e => { S.custom = e.target.value; S.paint = "custom"; repaint(); syncButtons(); updateCaption(); store.set(KEY, S); dirty(); });
// v15: the sliders, the colour bulbs, and the ceiling and skirting paints
root.addEventListener("input", e => {
  const t = e.target, d = t.dataset;
  if (d.lv) { const v = +t.value; if (d.lv === "master") S.master = v; else S.lv[d.lv] = v; qs(`[data-lvout="${d.lv}"]`).textContent = `${v}%`; press("scene", sameAsScene() ? S.scene : ""); applyLight(); updateCaption(); }
  else if (d.col) { S.col[d.col] = t.value; applyLight(); }
  else if (t.id === "r3d-ceil") { S.ceil = t.value; press("ceil", ""); repaint(); dirty(); }
  else if (t.id === "r3d-skirt") { S.skirt = t.value; press("skirt", ""); repaint(); dirty(); }
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
  buildShell(); buildLights(); buildFurniture();
  bar1 = buildBar(R.BAR1, lights.bar1, "bar1");
  gl.shadowMap.enabled = S.quality === "hd";
  applyState();
  syncButtons();
  setView(S.view, true);
  sizeRenderer();
  gl.compile(scene, camera);
  msg.hidden = true;
  root.classList.add("ready");
  requestAnimationFrame(frame);
  // for the headless stills (shot3d.py): set the options and a view, then take a picture
  window.R3D = {
    set(o) { Object.assign(S, o); if (o.scene && !o.lv) S.lv = Object.assign({}, SCENES[o.scene].levels); if (o.quality) S.picked = true; applyState(); syncButtons(); if (o.view) setView(o.view, true); },
    still, ready: true, buildMs: Math.round(performance.now() - t0), _dbg: { gl, scene, lights, THREE, S, MOV, UNDO, camera },
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
