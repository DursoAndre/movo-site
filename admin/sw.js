// Service worker do painel admin: guarda só o "casco" (página, ícones). Dados do Supabase nunca passam por aqui.
const CACHE = "movo-admin-v13";
const CASCO = ["/admin/", "/admin/manifest.webmanifest", "/admin/icon-192.png", "/admin/icon-512.png"];
self.addEventListener("install", (e) => { e.waitUntil(caches.open(CACHE).then((c) => c.addAll(CASCO)).then(() => self.skipWaiting())); });
self.addEventListener("activate", (e) => { e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", (e) => {
  const u = new URL(e.request.url);
  if (e.request.method !== "GET" || u.origin !== location.origin || !u.pathname.startsWith("/admin/")) return;
  // rede primeiro (sempre a versão mais nova); sem rede, usa o casco guardado
  e.respondWith(fetch(e.request).then((r) => { const cp = r.clone(); caches.open(CACHE).then((c) => c.put(e.request, cp)); return r; }).catch(() => caches.match(e.request).then((m) => m || caches.match("/admin/"))));
});
