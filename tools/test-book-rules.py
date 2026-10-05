from pathlib import Path
import argparse, hashlib, json, re, random, html
p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path,required=True);a=p.parse_args()
root=Path(__file__).resolve().parents[1]
book=json.loads((root/'src/book-study-data.json').read_text(encoding='utf-8'))
results=[]
methods={'baseline':'Initial of each whitespace token containing an ASCII letter','odd':'Initials at odd token positions','even':'Initials at even token positions','reverse':'All initials in reverse source order','circle':'Rotate each consecutive twelve initial block left by one','alternateCircle':'Odd then even positions within each consecutive twelve initial block'}
checks=0
for m in book['manifest']:
    n=m['chapter'];s=(a.source_dir/f'{n:02}.txt').read_text(encoding='utf-8').strip()
    assert hashlib.sha256(s.encode()).hexdigest()==m['normalizedTextSHA256']
    tokens=list(re.finditer(r'\S+',s));pairs=[]
    for i,t in enumerate(tokens,1):
        if i<=2:continue
        letter=re.search('[A-Za-z]',t.group())
        if letter:pairs.append((i,letter.group().upper(),t.start()+letter.start()))
    base=''.join(x[1] for x in pairs)
    variants={'baseline':pairs,'odd':[x for x in pairs if x[0]%2],'even':[x for x in pairs if not x[0]%2],'reverse':pairs[::-1]}
    blocks=[pairs[i:i+12] for i in range(0,len(pairs),12)]
    variants['circle']=[x for b in blocks for x in b[1:]+b[:1]]
    variants['alternateCircle']=[x for b in blocks for x in b[::2]+b[1::2]]
    assert sorted(variants['odd']+variants['even'])==pairs
    assert variants['reverse'][::-1]==pairs
    assert sorted(variants['circle'])==pairs==sorted(variants['alternateCircle'])
    checks+=4
    shuffled=pairs.copy();random.Random(20261005+n).shuffle(shuffled)
    for method,v in variants.items():
        out=''.join(x[1] for x in v)
        results.append({'chapter':n,'method':method,'length':len(out),'preview':out[:24],'previewTokenPositions':[x[0] for x in v[:24]],'previewCharacterPositions':[x[2] for x in v[:24]],'outputSHA256':hashlib.sha256(out.encode()).hexdigest(),'sourceSHA256':m['normalizedTextSHA256'],'source':m['url']})
    results.append({'chapter':n,'method':'shuffledControl','length':len(base),'preview':''.join(x[1] for x in shuffled[:24]),'previewTokenPositions':[x[0] for x in shuffled[:24]],'previewCharacterPositions':[x[2] for x in shuffled[:24]],'source':m['url']})
data={'title':'Chapter rule experiments','scope':'All eighteen saved chapter bodies, matched to the existing source hashes. Chapter heading tokens 1 and 2 excluded; decorative spaced opening letters retained. Token positions remain one based in the original normalized transcription. Character positions are zero based. Only short initial previews are published, not full transformed chapter bodies.','rules':methods,'limitations':['Initial extraction is an exploratory choice, not an instruction established by the novel.','Twelve initial blocks begin at the chapter body start; this anchor and a one position rotation are explicitly arbitrary probes.','Odd and even refer to original whitespace token positions, including tokens without letters; such tokens contribute no initial.','Shuffled samples use fixed random seeds as comparison controls, not statistical proof.','No predefined target plaintext or independent validation is available. Readable fragments do not establish success.','Compass bearings were not forced into word indices: sixteen compass points are not a supplied book indexing rule.','The novel label meanings T, circle and question mark are classifications, not a complete letter substitution alphabet.'],'checks':{'chapters':18,'hashesMatched':18,'structuralAssertions':checks,'experiments':108,'controls':18},'conclusion':'The published previews show no evident sustained message on inspection. This limited test does not rule out a book cipher. No rule is accepted and no recovered message is claimed.','results':results}
(root/'reports/chapter-rule-experiments.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
md='# Chapter rule experiments\n\n'+data['scope']+'\n\n'+data['conclusion']+'\n\n'
for k,v in methods.items():md+=k+': '+v+'\n\n'
md+='Limits\n\n'+'\n'.join('- '+x for x in data['limitations'])+'\n\n| Chapter | Method | Initial preview |\n|---|---|---|\n'
panel='<details id="chapterRuleExperiments"><summary>Chapter rule experiments</summary><p>'+html.escape(data['scope'])+'</p><p class="notice">'+html.escape(data['conclusion'])+'</p><ul>'+''.join('<li>'+html.escape(x)+'</li>' for x in data['limitations'])+'</ul><p>'+html.escape(json.dumps(methods))+'</p><div style="overflow:auto;max-height:520px"><table><thead><tr><th>Chapter</th><th>Method</th><th>Initial preview</th><th>Source token positions</th></tr></thead><tbody>'
for r in results:
    md+=f"| {r['chapter']} | {r['method']} | {r['preview']} |\n"
    panel+='<tr><td>'+str(r['chapter'])+'</td><td>'+r['method']+'</td><td>'+r['preview']+'</td><td>'+', '.join(map(str,r['previewTokenPositions']))+'</td></tr>'
panel+='</tbody></table></div><p>Complete coordinates and checks are included in the book comparison JSON export.</p></details>'
(root/'reports/chapter-rule-experiments.md').write_text(md,encoding='utf-8')
path=root/'src/book-study-panel.html';text=path.read_text(encoding='utf-8');text=re.sub(r'<details id="chapterRuleExperiments">.*?</details>','',text,flags=re.S);path.write_text(text.replace('<h3>Name count hypothesis</h3>',panel+'<h3>Name count hypothesis</h3>'),encoding='utf-8')
book['ruleExperiments']=data;(root/'src/book-study-data.json').write_text(json.dumps(book,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(data['checks']))
