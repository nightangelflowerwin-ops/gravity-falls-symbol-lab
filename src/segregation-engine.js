const SEG=__SEGREGATION_DATA__;
document.getElementById('segAtlas').href=SEG.atlas;
document.getElementById('segSummary').textContent=`106 inscription glyphs · ${SEG.groups.length} shape groups · 1 unassigned inscription glyph · 2 unclassified tablet marks · ${SEG.references.count} reference forms`;
document.getElementById('segConclusion').textContent=SEG.conclusion;
document.getElementById('segMethod').textContent=SEG.method;
document.getElementById('segScope').textContent=SEG.scope;
for(const family of SEG.references.families){const option=document.createElement('option');option.value=family;option.textContent=family;document.getElementById('segFamily').append(option)}
for(const region of [...new Set(SEG.items.map(item=>item.region))]){const option=document.createElement('option');option.value=region;option.textContent=region;document.getElementById('segRegion').append(option)}
document.getElementById('segSources').innerHTML=SEG.sources.map(source=>`<p><a href="${escapeText(source.url)}" target="_blank" rel="noopener">${escapeText(source.title)}</a><br>${escapeText(source.finding)}</p>`).join('');
function segRender(){
 const mode=document.getElementById('segFilter').value,family=document.getElementById('segFamily').value,region=document.getElementById('segRegion').value;
 let items=SEG.items.filter(item=>(mode==='unknown'?item.status.startsWith('Unresolved'):!item.status.includes('graphic'))&&(region==='all'||item.region===region));
 if(mode==='groups')items=items.filter((item,index,array)=>array.findIndex(other=>other.group===item.group)===index);
 document.getElementById('segInventory').innerHTML=items.map(item=>{
 const group=SEG.groups.find(group=>group.id===item.group);
 const matches=item.comparisons.filter(match=>family==='all'||family===match.family).map(match=>`<details><summary>${escapeText(match.family)} · best affinity ${match.candidates[0].score}%</summary>${match.candidates.map(candidate=>`<p><img src="${candidate.image}" alt="Reference form" style="width:40px;height:50px;object-fit:contain;background:white"> ${escapeText(candidate.symbol)} · ${candidate.score}%<br><small>${escapeText(candidate.basis)}</small></p>`).join('')}</details>`).join('');
 return `<article class="segCard" style="padding:12px;border:1px solid #777;border-radius:8px;min-width:0;overflow-wrap:anywhere"><h3>${escapeText(item.unknownId||item.id)} · ${escapeText(item.group)}</h3><img src="${item.image}" alt="Separated artwork glyph ${item.id}" style="width:70px;height:80px;object-fit:contain;background:white;image-rendering:pixelated"><p>${escapeText(item.region)}<br>${escapeText(item.status)}${item.annotation?` · ${escapeText(item.annotation)}`:''}</p><p>${group?`${group.members.length} occurrences in group · ${escapeText(group.members.join(', '))}`:'Graphic excluded from letter clustering'}</p><small>Source region bounds ${item.rect.join(', ')}${item.span.length?` · oriented crop columns ${item.span.join(' to ')}`:''}</small>${matches||'<p>No automatic letter comparison for this graphic.</p>'}</article>`;
 }).join('')||'<p>No objects match these filters.</p>';
}
for(const id of ['segFilter','segFamily','segRegion'])document.getElementById(id).addEventListener('change',segRender);
document.getElementById('segExport').addEventListener('click',()=>{const blob=new Blob([JSON.stringify(SEG,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='image-segregation.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)});
segRender();

function segNavigate(){if(location.hash==='#segregationPanel'){document.getElementById('researchView').value='segregation';researchChangeView();document.getElementById('researchPanel').scrollIntoView()}}
window.addEventListener('hashchange',segNavigate);segNavigate();
