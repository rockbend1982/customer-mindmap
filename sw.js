/* 織網 service worker — 讓加到主畫面後可離線開啟 */
const CACHE = "zhiwang-v1.1.0";
const ASSETS = ["./", "./index.html", "./manifest.json", "./icon-192.png", "./icon-512.png", "./apple-touch-icon.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

/* 頁面走「網路優先、失敗用快取」，確保更新後不會卡在舊版；其他資源快取優先 */
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  if (e.request.mode === "navigate" || e.request.destination === "document") {
    // 只有主頁的回應能寫進 index.html 的快取；其他頁（例如 demo.html）若也寫入，
    // 會讓主 App 離線時顯示錯的頁面
    const path = new URL(e.request.url).pathname;
    const isMain = path.endsWith("/") || path.endsWith("/index.html");
    e.respondWith(
      fetch(e.request)
        .then(res => {
          if (isMain){
            const copy = res.clone();
            caches.open(CACHE).then(c => c.put("./index.html", copy));
          }
          return res;
        })
        .catch(() => caches.match(isMain ? "./index.html" : e.request))
    );
    return;
  }
  e.respondWith(
    caches.match(e.request).then(hit => hit || fetch(e.request).then(res => {
      const copy = res.clone();
      caches.open(CACHE).then(c => c.put(e.request, copy));
      return res;
    }))
  );
});
