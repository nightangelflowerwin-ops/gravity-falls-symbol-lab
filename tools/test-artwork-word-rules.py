from pathlib import Path
import json,re,hashlib,html
root=Path(__file__).resolve().parents[1]
source=root/'reports/whitepaper-image-extraction.json'
d=json.loads(source.read_text(encoding='utf-8'))
tokens=[]
for r in d['letterRecords']:
    for m in re.finditer(r'\[[^\]]+\]|[A-Za-z]+(?:[-’\'][A-Za-z]+)*-?',r['transcription']):
        tokens.append({'word':m.group(),'spans':[{'region':r['index'],'block':r['block'],'letter':r['displayLetter'],'start':m.start(),'end':m.end()}]})
joins=[(['transac','tions'],'transactions'),(['an','nounced'],'announced'),(['cent','ral'],'central'),(['au','thority'],'authority'),(['tran','sacti','on'],'transaction'),(['spen','ding'],'spending'),(['dou','dle-','spent'],'doudle-spent')]
joined=[];i=0;audit=[]
while i<len(tokens):
    for pieces,word in joins:
        if [t['word'] for t in tokens[i:i+len(pieces)]]==pieces:
            spans=[s for t in tokens[i:i+len(pieces)] for s in t['spans']]
            joined.append({'word':word,'spans':spans});audit.append({'pieces':pieces,'joined':word,'spans':spans});i+=len(pieces);break
    else:joined.append(tokens[i]);i+=1
for i,t in enumerate(joined,1):t['position']=i
first=[];last=[];regions=[]
for r in d['letterRecords']:
    ts=[t for t in joined if t['spans'][0]['region']==r['index']]
    if ts:first.append(ts[0]);last.append(ts[-1])
    regions.append({'index':r['index'],'block':r['block'],'letter':r['displayLetter'],'oddWords':[t['position'] for t in ts[::2]],'evenWords':[t['position'] for t in ts[1::2]],'reverseWords':[t['position'] for t in ts[::-1]]})
blocks=[joined[i:i+12] for i in range(0,len(joined),12)]
variants={'First word per region':first,'Last word per region':last,'Odd words across displayed order':joined[::2],'Even words across displayed order':joined[1::2],'Reverse words across displayed order':joined[::-1],'Odd regions first words':first[::2],'Even regions first words':first[1::2],'Rotate twelve word blocks one position':[t for b in blocks for t in b[1:]+b[:1]],'Alternate twelve word blocks':[t for b in blocks for t in b[::2]+b[1::2]]}
tests=[{'rule':k,'positions':[t['position'] for t in v],'output':' '.join(t['word'] for t in v)} for k,v in variants.items()]
assert sorted(t['position'] for t in variants['Odd words across displayed order']+variants['Even words across displayed order'])==list(range(1,len(joined)+1))
assert variants['Reverse words across displayed order'][::-1]==joined
for k in ['Rotate twelve word blocks one position','Alternate twelve word blocks']:assert sorted(t['position'] for t in variants[k])==list(range(1,len(joined)+1))
report={'title':'Whole word rule tests','supersedes':'The earlier artwork initial tests did not apply rules to whole words. This report corrects that interpretation.','sourceSHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'scope':'Whole words in displayed title order: WELCOME TO THE BRAVE NEW WORLD. Footer excluded. Only declared handwritten fragments are joined; spellings and uncertainty markers remain unchanged. A joined word crossing a region boundary is assigned to its starting region, with all spans retained. Twelve word blocks and a one position rotation are exploratory conventions, not established instructions.','conclusion':'No distinct additional coherent message is evident in these whole word outputs. Ordinary Bitcoin sentences in the reordered material are source text, not a new decipherment. The provisional transcription and unspecified reading anchors limit the result.','tokens':joined,'fragmentJoins':audit,'tests':tests,'regions':regions,'checks':{'regions':25,'words':len(joined),'wholeTextRules':len(tests),'perRegionRules':75,'assertionsPassed':4},'limits':['The handwritten geometric reading paths have not been measured; circular and compass traversal remain untested.','Only observed line breaks are recorded, so a reliable alternating line extraction is unavailable.','No book supplied word substitution dictionary has been established.','Unknown readings are retained as bracketed tokens rather than filled from the whitepaper.']}
(root/'reports/artwork-whole-word-tests.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
md='# Whole word rule tests\n\n'+report['supersedes']+'\n\n'+report['scope']+'\n\n'+report['conclusion']+'\n\n'
panel='<details id="artworkWholeWordTests"><summary>Whole word rule tests</summary><p>'+html.escape(report['supersedes'])+'</p><p>'+html.escape(report['scope'])+'</p><p class="notice">'+html.escape(report['conclusion'])+'</p>'
for t in tests:
    md+='## '+t['rule']+'\n\n'+t['output']+'\n\n'
    panel+='<h3>'+t['rule']+'</h3><p>'+html.escape(t['output'])+'</p>'
md+='## Each region\n\n'
panel+='<details><summary>Each region</summary>'
for r in regions:
    heading=str(r['index'])+' '+r['block']+' '+r['letter'];md+='### '+heading+'\n\n';panel+='<h3>'+heading+'</h3>'
    for k in ['oddWords','evenWords','reverseWords']:
        output=' '.join(joined[i-1]['word'] for i in r[k]);md+=k+': '+output+'\n\n';panel+='<p><strong>'+k+':</strong> '+html.escape(output)+'</p>'
panel+='</details><ul>'+''.join('<li>'+html.escape(x)+'</li>' for x in report['limits'])+'</ul><p>All whole words, source spans and output positions are included in the book comparison JSON export.</p></details>'
(root/'reports/artwork-whole-word-tests.md').write_text(md,encoding='utf-8')
p=root/'src/book-study-panel.html';s=p.read_text(encoding='utf-8');s=re.sub(r'<details id="artworkTextRuleTests">.*?</details>','',s,flags=re.S);s=s.replace('<h3>Name count hypothesis</h3>',panel+'<h3>Name count hypothesis</h3>');p.write_text(s,encoding='utf-8')
p=root/'src/book-study-data.json';book=json.loads(p.read_text(encoding='utf-8'));book['artworkTextRuleTests']['supersededBy']='artworkWholeWordTests';book['artworkWholeWordTests']=report;p.write_text(json.dumps(book,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report['checks']))
for t in tests[:2]:print(t['rule']+': '+t['output'])
