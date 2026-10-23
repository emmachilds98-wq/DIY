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
const DEF = { site: "A", dining: "folded", scene: "everyday", paint: "card_room", custom: "#899081", lamp: "corner", drawers: false,
              quality: SMALL ? "fast" : "hd", view: "window" };
const S = Object.assign({}, DEF, store.get("mw14-3d", {}));
if (!(S.paint in R.PAINTS) && S.paint !== "custom") S.paint = DEF.paint;

/* ---------------------------------------------------------------- the lighting scenes (scenes.py) plus daytime */
const SCENES = JSON.parse(document.getElementById("scenes-data").textContent);
SCENES.day = { name: "Daytime", levels: { strip: 0, uprights: 0, bias: 0, bar1: 0, bar2: 0, lamp: 0 }, day: true };
if (!(S.scene in SCENES)) S.scene = DEF.scene;

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
controls.maxDistance = 16;
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
const CARPET = canvasTex(512, 512, (g, w, h) => {
  const r = rnd(3);
  g.fillStyle = "#8a8780"; g.fillRect(0, 0, w, h);
  const im = g.getImageData(0, 0, w, h), d = im.data;
  for (let i = 0; i < d.length; i += 4) { const n = (r() - 0.5) * 46; d[i] += n; d[i + 1] += n; d[i + 2] += n * 1.05; }
  g.putImageData(im, 0, 0);
});
CARPET.repeat.set(5, 5);
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
function paintColour(ratio) {
  const c = new THREE.Color(paintHex()); const o = {}; c.getHSL(o);
  return new THREE.Color().setHSL(o.h, o.s, Math.min(0.92, o.l * Math.pow(ratio, 0.6)));
}
function paintMat(ratio, eggshell, both) {
  const k = ratio.toFixed(2) + (eggshell ? "e" : "") + (both ? "d" : "");
  if (!paintMats.has(k)) paintMats.set(k, reg(new THREE.MeshStandardMaterial({ color: paintColour(ratio), roughness: eggshell ? 0.45 : 0.92,
    bumpMap: eggshell ? null : WALL_BUMP, bumpScale: 0.6, side: both ? THREE.DoubleSide : THREE.FrontSide, userData: { ratio } })));
  return paintMats.get(k);
}
function repaint() { paintMats.forEach(m => m.color.copy(paintColour(m.userData.ratio))); }
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
    fabric: () => new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.95, bumpMap: CARPET, bumpScale: 0.4 }),
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
const SOFT = new Set(["#2a2b30", "#a19c95"]);   // v14.1: the sofa's cord and its cushion, upholstered rather than boxy
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
  const wallP = paintMat(lum("#2d5a46") / BASE_L), recP = paintMat(lum("#264c3a") / BASE_L), ceilP = paintMat(lum("#33604a") / BASE_L);
  const egg = paintMat(lum("#346650") / BASE_L, true), doorP = paintMat(lum("#2a5340") / BASE_L, true);
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
  // floor (carpet) and ceiling (painted, with the opening over the stairs)
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(Wd * M, (RZ - WZ) * M), reg(new THREE.MeshStandardMaterial({ map: CARPET, roughness: 1 })));
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
  ceilMat = ceilP.clone(); ceilMat.emissiveMap = ceilGlow; ceilMat.emissive = new THREE.Color("#ffe2c0"); ceilMat.userData = { ratio: ceilP.userData.ratio };
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
  [[wx0, wy0, fw, wy1 - wy0], [wx1 - fw, wy0, fw, wy1 - wy0], [wx0, wy0, wx1 - wx0, fw], [wx0, wy1 - fw, wx1 - wx0, fw], [mid - 3, wy0, 6, wy1 - wy0],
   [wx0, wy0 + 0.68 * (wy1 - wy0), wx1 - wx0, 5]].forEach(([x, y, w, h]) => cube(x, y, WZ - 4, w, h, 7, white));
  cube(wx0 - 4, wy0 - 3, WZ, wx1 - wx0 + 8, 3, 9, white);
  const glass = reg(new THREE.MeshPhysicalMaterial({ color: "#dfe8ee", roughness: 0.02, transparent: true, opacity: 0.12, depthWrite: false }));
  const pane = new THREE.Mesh(new THREE.PlaneGeometry((wx1 - wx0) * M, (wy1 - wy0) * M), glass);
  pane.position.copy(v3(mid, (wy0 + wy1) / 2, WZ - 1)); shell.add(pane);
  view = new THREE.Mesh(new THREE.PlaneGeometry(40, 14), new THREE.MeshBasicMaterial({ map: SKY.night, toneMapped: false }));
  view.position.copy(v3(mid, 300, WZ - 900)); shell.add(view);
  // the radiator under the window, painted in
  const [rx0, rx1] = R.RADIATOR_X, [ry0, ry1] = R.RADIATOR_Y, radP = paintMat(lum("#3b6e56") / BASE_L, true);
  for (let x = rx0; x < rx1 - 2; x += 5) cube(x, ry0, WZ + 3, 3.4, ry1 - ry0, 7, radP);
  // the coffee table (its footprint from the plan; drawn as a plain low table)
  const cof = R.COFFEE, cofM = reg(new THREE.MeshStandardMaterial({ color: "#2c2a28", roughness: 0.5 }));
  cube(cof.x[0], 38, cof.z[0], cof.x[1] - cof.x[0], 4, cof.z[1] - cof.z[0], cofM);
  for (const [x, z] of [[cof.x[0] + 3, cof.z[0] + 3], [cof.x[1] - 7, cof.z[0] + 3], [cof.x[0] + 3, cof.z[1] - 7], [cof.x[1] - 7, cof.z[1] - 7]]) cube(x, 0, z, 4, 38, 4, cofM);
  // a rug in front of the wall
  const rug = new THREE.Mesh(new THREE.PlaneGeometry(1.7, 2.3), reg(new THREE.MeshStandardMaterial({ color: "#8f8374", roughness: 1, map: CARPET })));
  rug.rotation.x = -Math.PI / 2; rug.position.copy(v3(150, 0.3, -150)); rug.receiveShadow = true; shell.add(rug);
  // shelf B: the client's 2 m black floating shelf on the stairs wall, with the speaker box and the plant from the photo
  const sb = R.SHELF_B, black = reg(new THREE.MeshStandardMaterial({ color: "#1a1a1b", roughness: 0.55 }));
  cube(Wd - sb.d, sb.top - sb.t, sb.z[1], sb.d, sb.t, sb.z[0] - sb.z[1], black);
  cube(Wd - 14, sb.top, sb.z[0] - 60, 12, 42, 56, black);
  const pot = reg(new THREE.MeshStandardMaterial({ color: "#5d6b5a", roughness: 0.8 })), leaf = reg(new THREE.MeshStandardMaterial({ color: "#3f7a3a", roughness: 0.7 }));
  const potM = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.055, 0.12, 20), pot); potM.position.copy(v3(Wd - 12, sb.top + 6, sb.z[1] + 15)); shell.add(shadow(potM));
  const r = rnd(4), leaves = [];
  for (let i = 0; i < 70; i++) {
    const g = new THREE.SphereGeometry(0.022 + r() * 0.012, 8, 6); g.scale(1, 0.55, 1.2);
    const t = r(), q = v3(Wd - 6 - r() * 10, sb.top + 12 - t * (t < 0.5 ? 20 : 150), sb.z[1] + 8 + r() * 14);
    g.translate(q.x, q.y, q.z); leaves.push(g);
  }
  shell.add(shadow(new THREE.Mesh(mergeGeometries(leaves), leaf)));
  // ceiling LED strip: an emissive line round the room's edge
  ledMat = new THREE.MeshBasicMaterial({ color: "#ffd9a8", toneMapped: false });
  const ly = R.LED_Y - 0.8;
  [[0.5, WZ + 1, 1, AD - WZ - 2], [Wd - 1.5, WZ + 1, 1, front - WZ - 2]].forEach(([x, z, w, d]) => cube(x, ly, z, w, 0.8, d, ledMat, false));
  [[1, WZ + 0.5, Wd - 2], [1, AD - 1.5, A - 2], [B0, -1.5, B1 - B0], [B1, RZ - 1.5, wx - B1]].forEach(([x, z, w]) => cube(x, ly, z, w, 0.8, 1, ledMat, false));
  flushCubes(shell);
}
let view, ledMat, ceilGlow, ceilMat;

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
  for (const x of [2.25, 133.25]) { const l = area("#ffcf96", 2, 112, [x, 134, 22], [x, 134, 40]); l.userData.k = 3500; lights.uprights.push(l); }
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
function spotHead(group, apex, dir, col, lightList, kSpot) {
  const shade = new THREE.Mesh(new THREE.CylinderGeometry(0.019, 0.075, 0.13, 28, 1, true), headMat(col));
  const cap = new THREE.Mesh(new THREE.CylinderGeometry(0.011, 0.019, 0.038, 16), toppers);
  const glow = new THREE.Mesh(new THREE.CircleGeometry(0.06, 24), new THREE.MeshBasicMaterial({ color: "#fff3dc", toneMapped: false }));   // one each: it dims with its own light
  const head = new THREE.Group();
  shade.position.y = -0.065 - 0.038; cap.position.y = -0.019; glow.position.y = -0.155; glow.rotation.x = Math.PI / 2;
  head.add(shade, cap, glow); shadow(shade); shadow(cap, true);
  head.position.copy(apex);
  head.quaternion.setFromUnitVectors(new THREE.Vector3(0, -1, 0), dir);
  group.add(head);
  const sp = new THREE.SpotLight("#ffe2b8", 1, 0, 0.42, 0.85, 2);
  sp.position.copy(apex.clone().add(dir.clone().multiplyScalar(0.14)));
  sp.target.position.copy(apex.clone().add(dir.clone().multiplyScalar(3)));
  sp.shadow.mapSize.set(1024, 1024); sp.shadow.bias = -0.0004; sp.shadow.normalBias = 0.02; sp.shadow.camera.near = 0.05;
  sp.userData = { k: kSpot, glow };
  scene.add(sp, sp.target); lightList.push(sp);
}
function buildBar(spec, list) {
  const g = new THREE.Group(); g.name = "bar";
  const C = R.CEIL;
  const rose = new THREE.Mesh(new THREE.CylinderGeometry(0.065, 0.065, 0.025, 28), white); rose.position.copy(v3(spec.x, C - 1.25, spec.z)); g.add(rose);
  const barM = new THREE.Mesh(new THREE.BoxGeometry(0.84, 0.013, 0.022), white); barM.position.copy(v3(spec.x, C - 3.2, spec.z)); g.add(shadow(barM));
  for (const h of spec.heads) {
    const apex = v3(spec.x + h.dx, C - 6.5, spec.z), tgt = v3(...h.tgt);
    const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.004, 0.004, 0.03, 8), headMat(h.stem));
    stem.position.copy(v3(spec.x + h.dx, C - 5, spec.z)); g.add(stem);
    spotHead(g, apex, tgt.clone().sub(apex).normalize(), h.col, list, 260);
  }
  fixtures.add(g); return g;
}
let lamp;
const LAMP_BLACK = new THREE.MeshStandardMaterial({ color: "#151515", roughness: 0.35, metalness: 0.4 });
function buildLamp() {   // three adjustable heads on a black pole, as in the photo; on/off only
  if (lamp) drop(lamp, lights.lamp);
  const spot = R.LAMP_SPOTS[S.lamp] || R.LAMP_SPOTS.corner;
  const g = new THREE.Group(); lamp = g;
  const blk = LAMP_BLACK;
  const base = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.15, 0.025, 32), blk); base.position.copy(v3(spot.x, 1.25, spot.z)); g.add(shadow(base));
  const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.011, 0.011, R.LAMP.h * M, 12), blk); pole.position.copy(v3(spot.x, R.LAMP.h / 2, spot.z)); g.add(shadow(pole));
  const toward = new THREE.Vector3(...[233 - spot.x, 0, -135 - spot.z]).normalize();      // the room's middle, in room coords
  const aims = [[R.LAMP.h - 8, [toward.x * 60, 110, toward.z * 60]], [R.LAMP.h - 45, [toward.x * 160, -40, toward.z * 160]], [R.LAMP.h - 80, [toward.x * 90, -110, toward.z * 90]]];
  for (const [y, off] of aims) {
    const apex = v3(spot.x + toward.x * 9, y, spot.z + toward.z * 9);
    const tgt = v3(spot.x + off[0], y + off[1], spot.z + off[2]);
    const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 0.1, 8), blk); arm.position.copy(v3(spot.x + toward.x * 5, y, spot.z + toward.z * 5));
    arm.rotation.z = Math.PI / 2; arm.rotation.y = Math.atan2(toward.z, -toward.x); g.add(arm);
    spotHead(g, apex, tgt.clone().sub(apex).normalize(), "#3a1f2a", lights.lamp, 140);
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
  if (built.bar2 !== b2) { if (bar2) drop(bar2, lights.bar2); bar2 = buildBar(R.BAR2[b2], lights.bar2); built.bar2 = b2; }
  if (built.lamp !== S.lamp) { buildLamp(); built.lamp = S.lamp; }
  repaint();
  applyLight();
  updateCaption();
  store.set("mw14-3d", S);
  dirty();
}
function applyLight() {
  const sc = SCENES[S.scene], L = sc.levels, day = !!sc.day, hd = S.quality === "hd";
  const set = (list, lv) => list.forEach(l => {
    l.intensity = (l.userData.k || 1) * Math.pow(lv / 100, 1.6);
    l.visible = lv > 0;
    if (l.isSpotLight) { l.castShadow = hd && lv > 0; if (l.userData.glow) l.userData.glow.material.color.set(lv > 0 ? "#fff3dc" : "#3a3a3a"); }
  });
  const area = hd ? 1 : 0;      // Fast leaves out the area lights (the most expensive) and lifts the fill to make up
  set(lights.strip, L.strip * area); set(lights.uprights, L.uprights * area); set(lights.bias, L.bias * area); set(lights.bar1, L.bar1); set(lights.bar2, L.bar2);
  set(lights.lamp, L.lamp > 0 ? 100 : 0);                   // the lamp is on or off: no dimmer
  set(lights.tv, L.bias > 0 && hd ? 100 : 0);
  ledMat.color.set(L.strip > 0 ? "#ffd9a8" : "#5a5248").multiplyScalar(L.strip > 0 ? 0.6 + L.strip / 100 * 1.4 : 1);
  ceilMat.emissiveIntensity = 0.55 * Math.pow(L.strip / 100, 1.2);
  tvScreen.material = L.bias > 0 ? screenOn : screenOff;
  win.intensity = day ? 75 : 4; win.color.set(day ? "#e3ecff" : "#3b4a7a");
  view.material.map = day ? SKY.day : SKY.night; view.material.needsUpdate = true;
  // bounce light: a real room's walls relight it; this stands in for that, in proportion to what's on
  const on = (L.strip * 1.0 + L.uprights * 0.25 + L.bar1 * 0.35 + L.bar2 * 0.35 + (L.lamp > 0 ? 30 : 0) + (L.bias > 0 ? 8 : 0)) / 100;
  hemi.intensity = day ? 0.5 + (hd ? 0 : 0.25) : 0.05 + on * 0.32 + (hd ? 0 : (L.strip * 0.0075 + L.uprights * 0.0015 + (L.bias > 0 ? 0.08 : 0)));
  win.visible = hd || day;
  MATS.forEach(m => { if ("envMapIntensity" in m) m.envMapIntensity = day ? 0.25 : 0.12; });
  gl.toneMappingExposure = day ? 0.5 : 0.75;
  if (gl.shadowMap.enabled !== hd) { gl.shadowMap.enabled = hd; MATS.forEach(m => m.needsUpdate = true); sizeRenderer(); }
  reshadow();
  dirty();
}
const screenOff = new THREE.MeshStandardMaterial({ color: "#050506", roughness: 0.12, metalness: 0.2 });
const screenOn = new THREE.MeshBasicMaterial({ map: SCREEN_TEX, toneMapped: false, color: "#d8d8d8" });

/* ---------------------------------------------------------------- views */
const VIEWS = {
  window:  { label: "From the window", eye: [292, 158, -298], at: [196, 96, 10], fov: 66 },
  wall:    { label: "The media wall", eye: [140, 128, -285], at: [93, 108, 20], fov: 52 },
  sofa:    { label: "From the sofa", eye: [62, 104, -255], at: [72, 112, 20], fov: 58 },
  door:    { label: "From the door", eye: [372, 165, -6], at: [110, 85, -210], fov: 64 },
  stairs:  { label: "From the stairs", eye: [438, 205, 4], at: [190, 70, -205], fov: 62 },
  dining:  { label: "The dining table", A: { eye: [250, 140, -262], at: [246, 88, 0] }, B: { eye: [198, 140, -180], at: [467, 92, -180] }, fov: 56 },
  pc:      { label: "The PC side wall", eye: [345, 135, -168], at: [0, 112, -168], fov: 56 },
  plan:    { label: "Bird’s eye", eye: [233.5, 1150, -135], at: [233.5, 0, -134.9], fov: 30, above: true },
  doll:    { label: "Dolls’ house", eye: [780, 560, -700], at: [230, 60, -120], fov: 40, above: true },
};
let tween = null;
function setView(name, instant) {
  const v = VIEWS[name] || VIEWS.window; S.view = name;
  const p = v[S.site] || v;
  const eye = v3(...p.eye), at = v3(...p.at);
  const from = { eye: camera.position.clone(), at: controls.target.clone(), fov: camera.fov };
  setAbove(!v.above);
  if (instant) { camera.position.copy(eye); controls.target.copy(at); camera.fov = v.fov; camera.updateProjectionMatrix(); controls.update(); dirty(); }
  else tween = { t0: performance.now(), from, to: { eye, at, fov: v.fov } };
  qsa("[data-view]").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.view === name)));
  store.set("mw14-3d", S); updateCaption();
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
  const din = { folded: "folded", four: "down for four", six: "lifted off with its leaf, for six" }[S.dining];
  const paint = S.paint === "custom" ? `your colour ${S.custom}` : R.PAINTS[S.paint].name;
  qs("#r3d-cap").textContent = `${(VIEWS[S.view] || VIEWS.window).label} · ${site}, ${din} · ${sc.name} · ${paint}${S.drawers ? " · drawers out" : ""}`;
}
function still(w, h) {
  if (!started) start();
  const pr = gl.getPixelRatio(), size = gl.getSize(new THREE.Vector2()), asp = camera.aspect;
  gl.setPixelRatio(1); gl.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
  const was = gl.shadowMap.enabled, wasQ = S.quality; gl.shadowMap.enabled = true; gl.shadowMap.type = THREE.PCFSoftShadowMap;
  if (wasQ !== "hd") { S.quality = "hd"; applyLight(); gl.shadowMap.enabled = true; }
  Object.values(lights).flat().forEach(l => { if (l.isSpotLight && l.visible) { l.castShadow = true; l.shadow.mapSize.set(2048, 2048); if (l.shadow.map) { l.shadow.map.dispose(); l.shadow.map = null; } } });
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
  return `Media wall v14 - 3D - ${(VIEWS[S.view] || VIEWS.window).label.replace(/[’']/g, "")} - table on the ${site}, ${S.dining} - ${SCENES[S.scene].name}.png`;
}
qs("#r3d-save").addEventListener("click", async () => {
  const st = qs("#r3d-savest");
  st.textContent = "Rendering 3840 × 2160…";
  await new Promise(r => setTimeout(r, 30));
  const url = still(3840, 2160);
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
function syncButtons() {
  press("site", S.site); press("dining", S.dining); press("scene", S.scene); press("paint", S.paint); press("lamp", S.lamp);
  press("drawers", S.drawers ? "out" : "in"); press("quality", S.quality); press("view", S.view);
  qs("#r3d-custom").value = S.custom;
}
root.addEventListener("click", e => {
  const b = e.target.closest("button"); if (!b || !root.contains(b)) return;
  const d = b.dataset;
  if (d.view) { setView(d.view); return; }
  if (d.site) { S.site = d.site; applyState(); if (S.view === "dining") setView("dining"); }
  else if (d.dining) S.dining = d.dining, applyState();
  else if (d.scene) S.scene = d.scene, applyLight(), updateCaption(), store.set("mw14-3d", S);
  else if (d.paint) S.paint = d.paint, repaint(), updateCaption(), store.set("mw14-3d", S), dirty();
  else if (d.lamp) S.lamp = d.lamp, applyState();
  else if (d.drawers) S.drawers = d.drawers === "out", applyState();
  else if (d.quality) S.quality = d.quality, S.picked = true, applyLight(), store.set("mw14-3d", S);
  else if (b.id === "r3d-full") { const st = qs(".r3d-stage"); (document.fullscreenElement ? document.exitFullscreen() : st.requestFullscreen?.())?.catch?.(() => {}); return; }
  else if (b.id === "r3d-reset") { setView(S.view); return; }
  else return;
  syncButtons();
});
qs("#r3d-custom").addEventListener("input", e => { S.custom = e.target.value; S.paint = "custom"; repaint(); syncButtons(); updateCaption(); store.set("mw14-3d", S); dirty(); });

/* ---------------------------------------------------------------- go: built the first time the room is on screen (v14.1) */
let started = false;
function start() {
  started = true;
  const t0 = performance.now();
  const pmrem = new THREE.PMREMGenerator(gl);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  pmrem.dispose();
  buildShell(); buildLights(); buildFurniture();
  bar1 = buildBar(R.BAR1, lights.bar1);
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
    set(o) { Object.assign(S, o); if (o.quality) S.picked = true; applyState(); syncButtons(); if (o.view) setView(o.view, true); },
    still, ready: true, buildMs: Math.round(performance.now() - t0), _dbg: { gl, scene, lights, THREE },
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
