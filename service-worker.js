// Version: 2025-01-25-v9405
// =============================================
// EduCalc - Service Worker
// =============================================

const CACHE_NAME = 'educalc-v1.0.0';
const urlsToCache = [
    '/',
    '/index.html',
    '/styles.css',
    '/app.js',
    '/manifest.json'
];

// Instalación - cachear archivos estáticos
self.addEventListener('install', event => {
    console.log('Service Worker: Instalando...');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Service Worker: Cacheando archivos');
                return cache.addAll(urlsToCache);
            })
            .then(() => self.skipWaiting())
    );
});

// Activación - limpiar cachés antiguos
self.addEventListener('activate', event => {
    console.log('Service Worker: Activando...');
    
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cache => {
                    if (cache !== CACHE_NAME) {
                        console.log('Service Worker: Borrando caché antiguo', cache);
                        return caches.delete(cache);
                    }
                })
            );
        })
    );
    
    return self.clients.claim();
});

// Fetch - estrategia Network First, fallback a Cache
self.addEventListener('fetch', event => {
    const { request } = event;
    
    // Skip si es una petición al API
    if (request.url.includes('/calculate') || 
        request.url.includes('/validate') || 
        request.url.includes('/operations') ||
        request.url.includes('/health')) {
        // Para el API, siempre intentar red primero
        event.respondWith(
            fetch(request).catch(() => {
                return new Response(
                    JSON.stringify({ 
                        error: 'Sin conexión. Verifica tu conexión a internet.' 
                    }),
                    { 
                        status: 503,
                        headers: { 'Content-Type': 'application/json' }
                    }
                );
            })
        );
        return;
    }
    
    // Para archivos estáticos: Cache first, fallback a network
    event.respondWith(
        caches.match(request)
            .then(cached => {
                // Si está en caché, devolverlo
                if (cached) {
                    return cached;
                }
                
                // Si no, intentar obtenerlo de la red
                return fetch(request)
                    .then(response => {
                        // Cachear la nueva respuesta
                        if (response.status === 200) {
                            const responseClone = response.clone();
                            caches.open(CACHE_NAME)
                                .then(cache => {
                                    cache.put(request, responseClone);
                                });
                        }
                        return response;
                    });
            })
            .catch(() => {
                // Si falla todo, mostrar página offline
                return new Response(
                    '<h1>Sin conexión</h1><p>Verifica tu conexión a internet</p>',
                    { 
                        headers: { 'Content-Type': 'text/html' }
                    }
                );
            })
    );
});

// Sincronización en segundo plano (opcional, para futuro)
self.addEventListener('sync', event => {
    if (event.tag === 'sync-calculations') {
        console.log('Service Worker: Sincronizando cálculos...');
        // Implementar lógica de sincronización aquí
    }
});

// Notificaciones push (opcional, para futuro)
self.addEventListener('push', event => {
    if (event.data) {
        const data = event.data.json();
        const options = {
            body: data.body,
            icon: '/icon-192.png',
            badge: '/icon-192.png'
        };
        event.waitUntil(
            self.registration.showNotification(data.title, options)
        );
    }
});

console.log('Service Worker: Registrado');

