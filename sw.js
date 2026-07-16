/* COBBLEVERSE 한국어 가이드 — 오프라인 캐시
   버전 올릴 때 CACHE 이름을 바꾸면 이전 캐시 자동 정리됨 */
const CACHE = 'cvz-v1.2.2';
const SPRITES = 'cvz-sprites';
const CORE = [
  './',
  './index.html',
  './cobblemon-korea-guide.html',
  './icon.svg',
  './manifest.json',
  './legacy/base-mod-guide.html'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(
        ks.filter(k => k !== CACHE && k !== SPRITES && k.startsWith('cvz-'))
          .map(k => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const u = new URL(e.request.url);

  // 스프라이트 CDN: cache-first (파일 불변)
  if (u.hostname === 'raw.githubusercontent.com') {
    e.respondWith(
      caches.open(SPRITES).then(c =>
        c.match(e.request).then(r =>
          r || fetch(e.request).then(n => {
            if (n.ok) c.put(e.request, n.clone());
            return n;
          })
        )
      )
    );
    return;
  }

  // 같은 출처: network-first (항상 최신), 오프라인이면 캐시
  if (u.origin === location.origin) {
    e.respondWith(
      fetch(e.request).then(n => {
        const copy = n.clone();
        caches.open(CACHE).then(c => c.put(e.request, copy));
        return n;
      }).catch(() => caches.match(e.request))
    );
  }
});
