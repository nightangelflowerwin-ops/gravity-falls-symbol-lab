const DECIPHER=__DECIPHER_DATA__;
$('decipherReadings').innerHTML=researchTable(['Location','Recorded plaintext','English meaning','Evidence status'],DECIPHER.readings.map(r=>[r.region,r.text,r.meaning,r.status]));
$('decipherMethod').textContent=DECIPHER.referenceForms+' rendered reference forms; '+DECIPHER.comparisons+' orientation comparisons. '+DECIPHER.method;
$('decipherConclusion').textContent=DECIPHER.conclusion;
$('decipherLicense').textContent=DECIPHER.license;
$('decipherCoverage').innerHTML=researchTable(['Font family','Unique rendered forms','Source integrity'],DECIPHER.fonts.map(f=>[f.family,f.forms,f.sha256]));
$('decipherUnknown').innerHTML=researchTable(['Orientation','Nearest family','Font encoding key','Shape score','Lead over runner up'],DECIPHER.unknownCandidates.map(r=>[r.orientation,r.top[0].family,r.top[0].fontKey,r.top[0].score+'%',r.lead+' points']));
function decipherRender(){const filter=$('decipherFilter').value,rows=DECIPHER.rows.filter(r=>filter==='all'||filter==='unknown'&&r.id==='G099'||filter==='screen'&&r.passesShapeScreen);$('decipherRows').innerHTML='<p>'+rows.length+' comparisons shown</p>'+researchTable(['Glyph','Region','Orientation','Nearest family','Font key','Score','Lead','Shape screen'],rows.map(r=>[r.id,r.region,r.orientation,r.top[0].family,r.top[0].fontKey,r.top[0].score+'%',r.lead+' points',r.passesShapeScreen?'Pass; identity unaccepted':'Fail']));}
$('decipherFilter').onchange=decipherRender;$('decipherExport').onclick=()=>download('decipherment-audit.json',DECIPHER);decipherRender();
