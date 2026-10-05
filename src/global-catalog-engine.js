const GLOBALCAT=__GLOBAL_CATALOG_DATA__;
document.getElementById('globalCatalogSummary').textContent=`Unicode ${GLOBALCAT.version} · ${GLOBALCAT.characterCount.toLocaleString()} public assigned characters · ${GLOBALCAT.scriptCount} scripts plus Common and Inherited · ${GLOBALCAT.leads.length} additional source leads`;
document.getElementById('globalCatalogScope').textContent=GLOBALCAT.scope;
document.getElementById('globalConclusion').textContent=GLOBALCAT.conclusion;
document.getElementById('globalSnapshot').href=GLOBALCAT.archive;
document.getElementById('globalLicense').textContent=GLOBALCAT.license;
document.getElementById('globalReport').textContent=GLOBALCAT.report;
document.getElementById('globalManifest').innerHTML=GLOBALCAT.manifest.map(file=>`<p><a href="${escapeText(file.url)}" target="_blank" rel="noopener">${escapeText(file.file)}</a> · ${file.bytes} bytes<br><small style="overflow-wrap:anywhere">SHA256 ${file.sha256}</small></p>`).join('');
for(const family of GLOBALCAT.families){const option=document.createElement('option');option.value=family.key;option.textContent=family.name;document.getElementById('globalScript').append(option)}
function globalTable(headers,rows){return `<table><thead><tr>${headers.map(header=>`<th>${escapeText(header)}</th>`).join('')}</tr></thead><tbody>${rows.map(row=>`<tr>${row.map(value=>`<td>${value}</td>`).join('')}</tr>`).join('')}</tbody></table>`}
function globalRender(){
 const mode=document.getElementById('globalCollection').value,raw=document.getElementById('globalSearch').value.trim(),query=raw.toLowerCase(),script=document.getElementById('globalScript').value;
 let rows=[],headers=[],count=0;
 if(mode==='unicode'){
  const families=GLOBALCAT.families.filter(family=>(script==='all'||family.key===script)&&(family.name+' '+family.priority+' '+family.status).toLowerCase().includes(query));count=families.length;headers=['Script group','Characters','Examples','Coverage'];rows=families.map(family=>[escapeText(family.name),family.count,Array.from(String.fromCodePoint(...family.examples)).map(c=>escapeText(c)).join(' '),escapeText(family.priority+' · '+family.status)]);
 }else if(mode==='leads'){
  const leads=GLOBALCAT.leads.filter(lead=>(lead.name+' '+lead.category+' '+lead.basis).toLowerCase().includes(query));count=leads.length;headers=['Family or collection','Type','Evidence and coverage'];rows=leads.map(lead=>[`<a href="${escapeText(lead.url)}" target="_blank" rel="noopener">${escapeText(lead.name)}</a>`,escapeText(lead.category),escapeText(lead.basis)+'<br><strong>'+escapeText(lead.status)+'</strong>']);
 }else{
  headers=['Character','Code point','Name or range','Script group'];const code=/^(?:u\+|0x)([0-9a-f]{1,6})$/i.exec(query),literal=Array.from(raw).length===1?raw.codePointAt(0):null,target=code?parseInt(code[1],16):literal;
  const matches=GLOBALCAT.entries.filter(entry=>(script==='all'||entry[3]===script)&&(target!==null?entry[0]===target:(!query||entry[1].toLowerCase().includes(query)||entry[3].replaceAll('_',' ').toLowerCase().includes(query))));count=matches.length;rows=matches.slice(0,200).map(entry=>[escapeText(String.fromCodePoint(entry[0])),`U+${entry[0].toString(16).toUpperCase().padStart(4,'0')}`,escapeText(entry[1]),escapeText(entry[3].replaceAll('_',' '))]);
  const ranges=GLOBALCAT.ranges.filter(range=>(script==='all'||range.script===script)&&(target!==null?target>=range.start&&target<=range.end:(!query||range.name.toLowerCase().includes(query)||range.script.replaceAll('_',' ').toLowerCase().includes(query))));count+=ranges.length;rows.push(...ranges.map(range=>[target!==null?escapeText(String.fromCodePoint(target)):'Algorithmic range',target!==null?`U+${target.toString(16).toUpperCase()}`:`U+${range.start.toString(16).toUpperCase()} to U+${range.end.toString(16).toUpperCase()}`,escapeText(range.name+' · '+(range.end-range.start+1)+' characters; names represented by source range'),escapeText(range.script.replaceAll('_',' '))]));
 }
 document.getElementById('globalResultCount').textContent=`${count} matching ${mode==='characters'?'explicit records or compressed ranges':'records'}${mode==='characters'&&count>200?' · first 200 explicit records shown':''}`;
 document.getElementById('globalResults').innerHTML=globalTable(headers,rows);
}
for(const id of ['globalCollection','globalScript'])document.getElementById(id).addEventListener('change',globalRender);
document.getElementById('globalSearch').addEventListener('input',globalRender);
document.getElementById('globalExport').addEventListener('click',()=>download('global-glyph-catalog.json',GLOBALCAT));
globalRender();
