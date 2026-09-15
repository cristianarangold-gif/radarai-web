from pathlib import Path
import re

path = Path('index.html')
s = path.read_text(encoding='utf-8')
start = s.find('function renderCatalog(){')
end = s.find('function bindCatalogActions', start)
if start < 0 or end < 0:
    raise SystemExit('No se encontró el renderizador del catálogo')

new_render = r'''function renderCatalog(){
  const grid=$('#tools-grid'); if(!grid)return;
  const groups=[['ia-general','IA general','🤖'],['escritura','Escritura','✍️'],['imagenes','Imágenes','🎨'],['video','Vídeo','🎬'],['audio','Audio y música','🎵'],['programacion','Programación','💻'],['educacion','Educación','📚'],['marketing','Marketing','📈'],['productividad','Productividad','💼']];
  const aliases={'IA general':'ia-general','ia-general':'ia-general','Escritura':'escritura','escritura':'escritura','Imágenes':'imagenes','imagenes':'imagenes','Vídeo':'video','video':'video','Audio y música':'audio','audio':'audio','Programación':'programacion','programacion':'programacion','Educación':'educacion','educacion':'educacion','Marketing':'marketing','marketing':'marketing','Productividad':'productividad','productividad':'productividad'};
  const keyFor=(t)=>t.catKey||aliases[t.cat]||String(t.cat||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/\s+/g,'-');
  const cardFor=(id,t)=>`<article class="tool-card" data-category="${keyFor(t)}" data-tool-id="${id}" data-price="${t.price||''}" data-level="${t.level||''}" data-platform="${t.platform||''}" data-language="${t.lang||''}" data-search="${normalize([t.name,t.cat,t.desc,...(t.tags||[])].join(' '))}"><div class="tool-card-top"><div aria-hidden="true" class="tool-logo text-logo">${String(t.name||'?').slice(0,1)}</div><div class="tool-name-wrap"><p class="tool-name">${t.name||''}</p><p class="tool-category">${t.cat||''}</p></div><button aria-label="Guardar en favoritas" class="favorite-btn" data-favorite="${id}" title="Guardar en favoritas" type="button">☆</button></div><p class="tool-desc">${t.desc||''}</p><div class="tool-tags">${(t.tags||[]).slice(0,3).map(x=>`<span class="tool-tag">${x}</span>`).join('')}</div><div class="tool-meta"><span>${t.level||''}</span><span>${t.platform||''}</span><span>${t.lang==='multi'?'Multidioma':t.lang==='es'?'Español':'Inglés'}</span><span class="score-badge">Radar <strong>${radarScore(id)}</strong></span></div><div class="tool-card-bottom"><button aria-pressed="false" class="compare-btn" data-compare="${id}" type="button">Comparar</button><span class="tool-price">${t.price==='gratis'?'Gratis':t.price==='freemium'?'Gratis + opciones de pago':'De pago'}</span><a class="tool-link" href="herramientas/${id}/index.html">Ver ficha completa</a></div></article>`;
  grid.innerHTML=groups.map(([key,label,icon],i)=>{
    const items=Object.entries(TOOLS).filter(([id,t])=>keyFor(t)===key).map(([id,t])=>cardFor(id,t)).join('');
    const count=Object.values(TOOLS).filter(t=>keyFor(t)===key).length;
    return `<details class="catalog-group" data-group="${key}"${i===0?' open':''}><summary><span class="catalog-group-title"><span aria-hidden="true">${icon}</span><strong>${label}</strong><small>${count} herramientas</small></span><span class="catalog-group-toggle" aria-hidden="true">＋</span></summary><div class="tools-grid">${items||'<p class="empty-category">No hay herramientas disponibles en esta categoría.</p>'}</div></details>`;
  }).join('');
  bindCatalogActions();
}
'''

s = s[:start] + new_render + s[end:]

menu = '''<div class="radar-menu-wrap"><button class="radar-menu-toggle" type="button" aria-expanded="false" aria-controls="radar-main-menu">☰ Menú</button><nav id="radar-main-menu" class="radar-main-menu"><a href="#inicio">Inicio</a><a href="#herramientas">Herramientas</a><a href="#categorias">Categorías</a><a href="#articulos">Artículos</a><a href="/noticias/index.html">Noticias IA</a><a href="/reviews/index.html">Reviews IA</a><a href="/rankings/index.html">Rankings</a><a href="/alternativas/index.html">Alternativas</a><a href="/precios/index.html">Precios</a><a href="#seo-recursos">Guías IA</a><a href="/sobre-radar-ia/index.html">Sobre Radar IA</a><a href="/metodologia/index.html">Metodología</a><a href="/revisiones/index.html">Revisiones</a><a href="#preguntas-frecuentes">Preguntas frecuentes</a></nav></div>'''
s = re.sub(r'<nav[^>]*class=["\'][^"\']*main-nav[^"\']*["\'][^>]*>.*?</nav>', menu, s, count=1, flags=re.S|re.I)

# Menú cerrado por defecto; el botón alterna abrir/cerrar.
if 'radar-main-menu{' not in s:
    addon = '''<style>.radar-menu-wrap{position:relative}.radar-menu-toggle{background:var(--surface,#161d30);color:var(--text-primary,#f1f4fa);border:1px solid var(--border,#2a3454);border-radius:10px;padding:9px 15px;font-weight:600;cursor:pointer}.radar-main-menu{display:none;position:absolute;right:0;top:calc(100% + 8px);width:280px;max-height:70vh;overflow:auto;padding:10px;background:var(--surface,#161d30);border:1px solid var(--border,#2a3454);border-radius:14px;box-shadow:0 18px 40px rgba(0,0,0,.35);z-index:300}.radar-main-menu.is-open{display:flex;flex-direction:column}.radar-main-menu a{padding:9px 10px;border-radius:8px;color:var(--text-secondary,#9ba6c0);text-decoration:none}.radar-main-menu a:hover{background:var(--surface-2,#1c243a);color:var(--text-primary,#f1f4fa)}@media(max-width:700px){.radar-main-menu{right:auto;left:0;width:min(280px,calc(100vw - 32px))}}</style><script>document.addEventListener('click',function(e){var b=e.target.closest('.radar-menu-toggle');if(b){var m=document.getElementById('radar-main-menu');if(!m)return;var o=m.classList.toggle('is-open');b.setAttribute('aria-expanded',String(o))}else if(!e.target.closest('.radar-menu-wrap')){var m=document.getElementById('radar-main-menu');if(m){m.classList.remove('is-open');var b=m.parentElement.querySelector('.radar-menu-toggle');if(b)b.setAttribute('aria-expanded','false')}}});</script>'''
    s = s.replace('</head>', addon + '</head>', 1)

path.write_text(s, encoding='utf-8')
print('Catálogo de IA y menú principal corregidos')
