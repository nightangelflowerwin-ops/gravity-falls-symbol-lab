import json,re,bisect,zipfile,base64,hashlib,tempfile
from pathlib import Path
from collections import Counter,defaultdict
p=Path(__file__).resolve().parents[1]
scratch=tempfile.TemporaryDirectory()
src=Path(scratch.name)
with zipfile.ZipFile(p/'reports/unicode-source-snapshot.zip') as archive:
 for name in ['ReadMe.txt','UnicodeData.txt','Scripts.txt','Blocks.txt','LICENSE.txt']:
  (src/name).write_bytes(archive.read(name))
license=(src/'LICENSE.txt').read_bytes();(p/'licenses/Unicode-LICENSE.txt').write_bytes(license)
def ranges(file):
 result=[]
 for line in (src/file).read_text(encoding='utf-8').splitlines():
  line=line.split('#')[0].strip()
  if not line:continue
  bounds,value=line.split(';');bounds=bounds.strip().split('..');result.append((int(bounds[0],16),int(bounds[-1],16),value.strip()))
 return sorted(result)
scriptRanges=ranges('Scripts.txt');starts=[r[0] for r in scriptRanges]
def script(cp):
 i=bisect.bisect_right(starts,cp)-1
 return scriptRanges[i][2] if i>=0 and cp<=scriptRanges[i][1] else 'Unknown'
entries=[];large=[];counts=Counter();samples=defaultdict(list);first=None
for line in (src/'UnicodeData.txt').read_text(encoding='utf-8').splitlines():
 parts=line.split(';');cp=int(parts[0],16);name,category=parts[1:3]
 if name.endswith(', First>'):first=(cp,name,category);continue
 if name.endswith(', Last>'):
  a,n,c=first;first=None
  if c in ['Co','Cs']:continue
  family=script(a);large.append({'start':a,'end':cp,'name':n[1:-8],'category':c,'script':family});counts[family]+=cp-a+1
  if not samples[family]:samples[family]=[a+i for i in range(min(12,cp-a+1))]
  continue
 if category in ['Co','Cs']:continue
 family=script(cp);counts[family]+=1;entries.append([cp,name,category,family])
 if category[0] in 'LNPS' and len(samples[family])<12:samples[family].append(cp)
priority={'Runic','Ogham','Old_Turkic','Old_Hungarian','Old_Italic','Tifinagh','Phoenician','Glagolitic','Gothic','Carian','Lycian','Lydian','Old_Permic','Ugaritic','Old_Persian','Cypriot','Linear_A','Linear_B','Cypro_Minoan','Phaistos_Disc'}
families=[{'name':name.replace('_',' '),'key':name,'count':count,'examples':samples[name],'priority':'Priority comparison' if name in priority else 'Catalogued','status':'Existing limited templates' if name=='Runic' else 'Not image tested','source':'https://www.unicode.org/Public/18.0.0/ucd/Scripts.txt'} for name,count in sorted(counts.items())]
leads=[]
def lead(name,category,url,basis,status='Source located; not image tested'):leads.append(dict(name=name,category=category,url=url,basis=basis,status=status))
for name in ['Theban','Alphabet of the Magi','Celestial','Malachim','Passing the River','Chaldean','Enochian']:
 lead(name,'Historical and occult','https://esotericarchives.com/fonts/','Peterson reference fonts cite named historical witnesses. Fonts carry CC BY 4.0 attribution; fonts and historical handwriting must be compared separately.','Existing provisional chart slots' if name in ['Celestial','Malachim','Passing the River'] else 'Source located; not image tested')
lead('Enochian manuscript witness','Historical and occult','https://searcharchives.bl.uk/catalog/040-002115572','British Library Sloane MS 3188; manuscript catalog source, not a glyph comparison result.')
lead('Theban early printed witness','Historical and occult','https://commons.wikimedia.org/wiki/File:Theban_alphabet_from_Polygraphia_1518.png','Scan attributed to Polygraphia 1518; original page lead.')
lead('Pigpen','Geometric cipher','https://www.nist.gov/document/ccawpigpencipherpdf','NIST teaching chart provides a standard reference; variant arrangements must be retained.')
lead('Historical cipher alphabets','Manuscript cipher','https://www.diva-portal.org/smash/get/diva2%3A1437998/FULLTEXT01.pdf','DECODE database documentation identifies historical ciphertext and key collections. Individual alphabets not yet indexed.')
lead('Voynich manuscript','Undeciphered manuscript','https://beinecke.library.yale.edu/beinecke/collections/beinecke-cipher-voynich-manuscript','Yale collection source. Manuscript signs are not assumed to have known alphabetic values.')
lead('Gravity Falls Journal 3','Fictional and constructed','https://books.disney.com/book/gravity-falls-journal-3/','Publisher establishes the book. Exact printed cipher keys need page level inspection; existing chart is community sourced.','Existing English chart; primary key review pending')
lead('Constructed script discovery index','Fictional and constructed','https://www.omniglot.com/conscripts/index.htm','Discovery index for additional authored scripts. Index inclusion does not establish provenance of the artwork. Individual entries not yet reviewed.')
lead('Alchemical symbols','Symbol system','https://www.unicode.org/Public/18.0.0/charts/PDF/U1F700.pdf','Unicode chart supplies encoded sign names. Symbols are not necessarily letters.')
lead('Astronomical and astrological symbols','Symbol system','https://www.unicode.org/Public/18.0.0/charts/PDF/U2600.pdf','Miscellaneous Symbols is a starting block; relevant signs can occur in other blocks.')
lead('Geometric shapes and technical signs','Symbol system','https://www.unicode.org/Public/18.0.0/charts/PDF/U25A0.pdf','A geometric sign may be decoration or notation, rather than a writing system.')
manifest=[{'file':f.name,'url':'https://www.unicode.org/Public/18.0.0/ucd/'+f.name if f.name!='LICENSE.txt' else 'https://www.unicode.org/license.txt','bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(src.iterdir()) if f.is_file()]
archive=p/'reports/unicode-source-snapshot.zip'

d={'version':'18.0.0','retrieved':'2026-10-05','scope':'All public assigned character records in this UnicodeData snapshot, including compressed algorithmic ranges; private use and surrogate code points excluded. This catalog covers encoded characters, not every glyph variant, language or cipher. Script property groups Common and Inherited are not languages.','characterCount':sum(counts.values()),'scriptCount':len(families)-sum(f['key'] in ['Common','Inherited','Unknown'] for f in families),'families':families,'entries':entries,'ranges':large,'blocks':[{'start':a,'end':b,'name':v} for a,b,v in ranges('Blocks.txt')],'leads':leads,'manifest':manifest,'archive':'data:application/zip;base64,'+base64.b64encode(archive.read_bytes()).decode(),'license':license.decode(),'conclusion':'A source catalog has been collected. Newly indexed scripts have not been image matched. The final border glyph and tablet marks remain unresolved. Font coverage, handwriting variants, rotations and held out controls must be checked before expanding automatic matches.'}
d['report']=(p/'reports/global-glyph-source-pass.md').read_text(encoding='utf-8')
(p/'src/global-catalog-data.json').write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
(p/'reports/global-catalog-summary.json').write_text(json.dumps({k:v for k,v in d.items() if k not in ['entries','archive','license']},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'characters':d['characterCount'],'scripts':d['scriptCount'],'groups':len(families),'explicitRecords':len(entries),'ranges':len(large),'leads':len(leads),'bytes':(p/'src/global-catalog-data.json').stat().st_size}))
