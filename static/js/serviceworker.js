var staticCacheName = "0.1.0";

const resourcesToCache = [
    '/',
];

const addResourcesToCache = async (event) => {
    const cache = await caches.open(staticCacheName);
    await cache.addAll(resourcesToCache);
};

self.addEventListener('install', (event) => {

    console.log("[ServiceWorker] Install");

    event.waitUntil(
        addResourcesToCache()
    );
});

const deleteCache = async key => {
    await caches.delete(key)
}

const deleteOldCaches = async () => {
    const keyList = await caches.keys()
    const cachesToDelete = keyList.filter(key => (key !== staticCacheName))
    await Promise.all(cachesToDelete.map(deleteCache));
}

self.addEventListener('activate', (event) => {
    console.log("[ServiceWorker] Activate");
    event.waitUntil(deleteOldCaches());
});


const cacheFirst = async ({ request, preloadResponsePromise, fallbackUrl }) => {
    const responseFromCache = await caches.match(request);
    try {
        return responseFromCache || await fetch(request);
    } catch (error) {
        const fallbackResponse = await caches.match(fallbackUrl);
        if (fallbackResponse) {
            return fallbackResponse;
        }

        return new Response('Network error', {
            status: 408,
            headers: { 'Content-Type': 'text/plain' },
        });
    }
};

self.addEventListener("fetch", (event) => {
    var requestUrl = new URL(event.request.url);
    if (requestUrl.origin === location.origin) {
        if ((requestUrl.pathname === '/')) {
            event.respondWith(
                cacheFirst({
                    request: event.request,
                    fallbackUrl: "/",
                })
            );
            return;
      }
    }
});
