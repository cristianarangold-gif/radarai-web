from pathlib import Path

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
path.write_text(s, encoding='utf-8')
print('Catálogo de IA corregido')
