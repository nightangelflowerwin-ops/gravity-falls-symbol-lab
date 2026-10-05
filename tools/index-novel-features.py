import argparse,bisect,csv,hashlib,json,re
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('--source-dir',type=Path,required=True);args=parser.parse_args()
root=Path(__file__).resolve().parents[1];book=json.loads((root/'src/book-study-data.json').read_text(encoding='utf-8'))
vocab={
'Artwork vocabulary':['order and stability','brave new world','stability','liberty','freedom','history','monuments','pyramids','tower','towers','camera','cameras','police','breath','breathe','breathing','seed','seeds','moon','black','white','rain','numbers','figures'],
'Symbol vocabulary':['question mark','circle','circular','cross','crosses','sign of the T','T-Model','Alpha','Alphas','Beta','Betas','Gamma','Gammas','Delta','Deltas','Epsilon','Epsilons','letters','words','names','sum','multiply','divide','division','double','twice','equal','mirrors'],
'Directions':['north-east','north east','south-east','south east','south-south-west','north','south','east','west','northwards','southwards','eastwards','westwards','left','right','clockwise','anticlockwise','upside down','heads','tails'],
'Weekdays':['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','Mondays','Tuesdays','Wednesdays','Thursdays','Fridays','Saturdays','Sundays'],
'Names':['Henry Foster','Mr. Foster','Foster','Bernard Marx','Bernard','Marx','Mustapha Mond','Mond','Helmholtz Watson','Helmholtz','Watson','Lenina Crowne','Lenina','Fanny Crowne','Fanny','Linda','John','Tomakin','Shakespeare','Miranda','Ford','Freud','Mitsima','Darwin Bonaparte','Primo Mellon','Benito Hoover','Morgana Rothschild','Pookong','Awonawilona','Jesus']}
number_words='zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million millions billion dozen dozens score scores half quarter first second third fourth fifth sixth seventh eighth ninth tenth eleventh twelfth'.split()
num='(?:'+ '|'.join(sorted(number_words,key=len,reverse=True))+')'
number_pattern=re.compile(r'(?<!\w)(?:\d+(?:[.,]\d+)*(?:st|nd|rd|th)?|'+num+r'(?:[\s-]+(?:(?:and\s+)?(?:a\s+)?)'+num+r')*)(?!\w)',re.I)
focus=[
'Inspect the hatchery labels and Foster’s recorded quantities. The T, circle and question mark categories are explicit; assigning them to the artwork still requires a consistent mapping.',
'Inspect repetition schedules and how a memorized recitation differs from understood meaning. Repetition counts are facts in context, not instructions to skip or select words.',
'Inspect the destruction of monuments, references to pyramids and rejection of history. This gives a thematic anchor for the statue and seal, without selecting a glyph alphabet.',
'Inspect the disc topped Charing T Tower and the propaganda building. Keep their London identity separate from the artwork’s Seattle landmark.',
'Inspect the twelve person circular service and its alternating arrangement. The name count of twelve does not independently select this scene.',
'Inspect liberty, privacy, the boundary fence and travel directions. There is no explicit link from these routes to a reading direction in the artwork.',
'Inspect the Tuesdays and Fridays tower recollection. Preserve both weekdays and the building’s identity rather than selecting Tuesday alone.',
'Inspect learning to read, creation seeds, making a moon shaped pot base and John’s title phrase. These occur in different scenes; joining them requires an evidenced rule.',
'Inspect Bernard’s timetable and permits. The precise times provide source facts but no artwork instruction currently selects one.',
'Inspect the exact Order and Stability phrase and the Director’s argument about dissent. This is a textual anchor, not an encoded character assignment.',
'Inspect weekday lists, industrial group sizes and the racialized film. Tuesday occurs in a list with other days, so it is not a unique pointer.',
'Inspect censorship, clocks and Shakespeare’s poem about identity and number. Literary language about unity and division does not by itself prescribe arithmetic.',
'Inspect Foster’s appearance, the missed injection and its stated future interval. Their relevance to the artwork’s dates has not been established.',
'Inspect Linda’s loss of breath and the hospital’s numbered ward and bed. The breath parallel is specific, but the hospital numbers are not automatically indices.',
'Inspect the two staff groups, disruption of soma distribution and police response. Keep group quantities, weapon descriptions and political themes separate.',
'Inspect Mond’s tradeoff between stability and freedom, the Cyprus experiment and the iceberg proportions. None supplies an independently selected extraction rule.',
'Inspect the monetary cost example and John’s demand for freedom. Do not treat an incidental price as a key solely because the artwork involves Bitcoin.',
'Inspect seed packets, concealed cameras and the closing direction sequence. Preserve its order and reversal; no artwork instruction currently selects or applies it.']
records=[];chapters=[]
for m in book['manifest']:
 n=m['chapter'];text=(args.source_dir/f'{n:02}.txt').read_text(encoding='utf-8');assert hashlib.sha256(text.encode()).hexdigest()==m['normalizedTextSHA256'],f'Chapter {n} source changed'
 starts=[a.start() for a in re.finditer(r'\S+',text)];matches=[]
 for kind,terms in vocab.items():
  candidates=[]
  for term in terms:
   pattern=r'(?<!\w)'+re.escape(term).replace(r'\ ',r'\s+')+r'(?!\w)'
   for hit in re.finditer(pattern,text,re.I):candidates.append((hit.start(),hit.end(),term))
  selected=[]
  for a,b,term in sorted(candidates,key=lambda t:(-(t[1]-t[0]),t[0])):
   if any(a<y and b>x for x,y,_ in selected):continue
   selected.append((a,b,term))
  for a,b,term in selected:matches.append((a,b,kind,term))
 for hit in number_pattern.finditer(text):
  if hit.start()<text.find(' ',text.find(' ')+1):continue
  matches.append((hit.start(),hit.end(),'Number expressions',hit.group().casefold()))
 chapter_records=[]
 for i,(a,b,kind,term) in enumerate(sorted(matches),1):
  row={'id':f'C{n:02}R{i:04}','chapter':n,'kind':kind,'term':term,'literal':text[a:b],'charStart':a,'charEnd':b,'wordStart':bisect.bisect_right(starts,a),'wordEnd':bisect.bisect_right(starts,b-1)}
  assert row['literal']==text[row['charStart']:row['charEnd']];chapter_records.append(row)
 records+=chapter_records;chapters.append({'chapter':n,'focus':focus[n-1],'records':len(chapter_records),'counts':{k:sum(r['kind']==k for r in chapter_records) for k in list(vocab)+['Number expressions']},'url':m['url'],'normalizedTextSHA256':m['normalizedTextSHA256']})
data={'version':1,'title':'Chapter feature extraction','scope':'All eighteen previously reviewed chapter bodies. This is a literal occurrence index over six explicit categories, not an exhaustive list of every name or a decipherment. Overlapping long and short terms within a category are reduced to the longest match. Different categories can share a source span.','coordinates':'Zero based character offsets with exclusive end; one based whitespace token positions. Positions refer to the existing whitespace normalized chapter text, including its Chapter heading, not printed page coordinates. No letter spacing, spelling or punctuation is silently repaired.','limits':'Number expressions include pronouns and ordinals as well as quantities; they require contextual review. The vocabulary lists define coverage. Decorative letter spacing and unlisted variants can be missed. No extracted occurrence is accepted as a key, and no ordering or numerical rule is established.','chapters':chapters,'records':records,'vocabulary':vocab,'numberWords':number_words,'numberPattern':number_pattern.pattern,'checks':{'chapters':18,'sourceHashesMatched':18,'exactSpansVerified':len(records),'uniqueIds':len(set(r['id'] for r in records)),'allChaptersRepresented':sorted(set(r['chapter'] for r in records))==list(range(1,19))}}
assert data['checks']['uniqueIds']==len(records) and data['checks']['allChaptersRepresented']
md='# Chapter feature extraction\n\n'+data['scope']+'\n\n'+data['coordinates']+'\n\n'+data['limits']+'\n\n## Chapter reading and extraction review\n\n'
for c in chapters:md+=f"### Chapter {c['chapter']}\n\n[Read chapter]({c['url']}). {c['records']} recorded occurrences.\n\n{c['focus']}\n\n"+'; '.join(k+': '+str(v) for k,v in c['counts'].items())+'.\n\n'
md+='## Reproduce\n\nRun python tools/index-novel-features.py --source-dir PATH using the private normalized chapter files named 01.txt through 18.txt from the earlier review. Each input must match its recorded SHA256 value. The full novel text is not redistributed. The CSV and JSON preserve repeated occurrences and source positions; no phrase or decoding result is assembled.\n'
data['report']=md
(root/'src/chapter-extraction-data.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
(root/'reports/chapter-feature-extraction.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'reports/chapter-feature-extraction.md').write_text(md,encoding='utf-8')
with (root/'reports/chapter-feature-extraction.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
print(json.dumps(data['checks']))
