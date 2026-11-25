// Offline support: keeps the app (page, Leaflet, three.js, fonts) in the device cache so it opens without a connection.
// The page itself is network-first (so updates arrive when online, with a 4 s timeout), everything else cache-first.
const V = "rp-v2";
const CORE = ["./", "index.html", "lib/leaflet-1.9.4b.js", "lib/three-r128.min.js", "manifest.webmanifest", "icon-180.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(V).then(c => c.addAll(CORE)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", e => {
  const r = e.request; if (r.method !== "GET") return;
  const u = new URL(r.url), scope = new URL(self.registration.scope);
  const page = r.mode === "navigate" || (u.origin === scope.origin && (u.pathname === scope.pathname || u.pathname === scope.pathname + "index.html"));
  if (page) {
    const net = fetch(u.origin === scope.origin ? new Request(r.url, { cache: "no-store" }) : r).then(res => { if (res.ok) { const cp = res.clone(); caches.open(V).then(c => c.put("index.html", cp)); } return res; });
    const timeout = new Promise(ok => setTimeout(ok, 4000));
    e.respondWith(Promise.race([net.catch(() => null), timeout.then(() => null)]).then(res => res || caches.match("index.html")).then(res => res || net));
    return;
  }
  if (u.origin === scope.origin || /(^|\.)fonts\.(googleapis|gstatic)\.com$/.test(u.hostname)) {
    e.respondWith(caches.match(r).then(hit => hit || fetch(r).then(res => { if (res.ok || res.type === "opaque") { const cp = res.clone(); caches.open(V).then(c => c.put(r, cp)); } return res; })));
  }
});
