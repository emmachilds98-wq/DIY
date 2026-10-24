// v39: the page opens from the device after the first visit (network first for the page, so a new round shows; cache first for the
// rest: three.js from its CDN, the fonts and the pictures). Version 42.
const C = "demma-v42";
self.addEventListener("install", e => { self.skipWaiting(); e.waitUntil(caches.open(C).then(c => c.addAll(["./", "manifest.webmanifest"]).catch(() => {}))); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== C).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", e => {
  const r = e.request; if (r.method !== "GET") return;
  const u = new URL(r.url), page = r.mode === "navigate" || (u.origin === location.origin && (u.pathname.endsWith("/") || u.pathname.endsWith("index.html")));
  if (page) { e.respondWith(fetch(r).then(res => { const cp = res.clone(); caches.open(C).then(c => c.put(r, cp)); return res; }).catch(() => caches.match(r).then(m => m || caches.match("./")))); return; }
  if (/\.pdf$/.test(u.pathname)) return;                                   // the PDFs come from the network
  e.respondWith(caches.match(r).then(m => m || fetch(r).then(res => { if (res.ok || res.type === "opaque") { const cp = res.clone(); caches.open(C).then(c => c.put(r, cp)); } return res; })));
});
