const CACHE='quran365-v4';
const SHELL=['./','./index.html','./styles.css','./app.js','./plan.js','./manifest.webmanifest','./icons/quran.svg','./icons/apple-touch-icon.png','./icons/icon-192.png','./icons/icon-512.png','./icons/maskable-512.png','./data/plan.json','./data/summaries.json','./data/quran-data.json'];
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting())));
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('quran365-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',event=>{
 const req=event.request;if(req.method!=='GET')return;const url=new URL(req.url);
 if(url.origin!==location.origin&&url.hostname!=='fonts.googleapis.com'&&url.hostname!=='fonts.gstatic.com')return;
 if(url.origin===location.origin&&/\/data\/quran-data\.json$/.test(url.pathname)){
  event.respondWith(caches.open(CACHE).then(async cache=>{const hit=await cache.match(req);if(hit)return hit;try{const res=await fetch(req);if(res.ok)cache.put(req,res.clone());return res}catch(e){return new Response('Quran data is not cached yet. Connect once and reload.',{status:503,headers:{'Content-Type':'text/plain'}})}}));return;
 }
 event.respondWith(caches.match(req).then(hit=>{const network=fetch(req).then(res=>{if(res.ok&&((url.origin===location.origin)||(url.hostname==='fonts.gstatic.com'||url.hostname==='fonts.googleapis.com')))caches.open(CACHE).then(c=>c.put(req,res.clone()));return res}).catch(()=>hit);return hit||network}));
});
