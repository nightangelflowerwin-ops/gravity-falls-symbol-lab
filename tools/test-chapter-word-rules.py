from pathlib import Path
import argparse,hashlib,json,re,html
p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path,required=True);a=p.parse_args()
root=Path(__file__).resolve().parents[1]
book=json.loads((root/'src/book-study-data.json').read_text(encoding='utf-8'))
results=[];first=[];last=[];checked=0
for m in book['manifest']:
    chapter=m['chapter'];s=(a.source_dir/f'{chapter:02}.txt').read_text(encoding='utf-8').strip()
    assert hashlib.sha256(s.encode()).hexdigest()==m['normalizedTextSHA256']
    start=re.match(r'Chapter\s+\S+\s+',s).end()
    words=[{'word':t.group(),'chapter':chapter,'position':i,'characterStart':t.start(),'characterEnd':t.end()} for i,t in enumerate(re.finditer(r'\[[^\]]+\]|[A-Za-z]+(?:[-’\'][A-Za-z]+)*|\d+(?:[.,]\d+)*',s[start:]),1)]
    for t in words:t['characterStart']+=start;t['characterEnd']+=start
    assert all(s[t['characterStart']:t['characterEnd']]==t['word'] for t in words)
    groups=[(0,2),(2,4)] if chapter==2 else ([] if chapter==1 else [(0,2)])
    for lo,hi in reversed(groups):
        parts=words[lo:hi]
        words[lo:hi]=[{'word':''.join(t['word'] for t in parts),'chapter':chapter,'characterStart':parts[0]['characterStart'],'characterEnd':parts[-1]['characterEnd'],'typographicJoin':[t['word'] for t in parts]}]
    for i,t in enumerate(words,1):
        t['position']=i;t['rawSpan']=s[t['characterStart']:t['characterEnd']]
    first.append(words[0]);last.append(words[-1])
    blocks=[words[i:i+12] for i in range(0,len(words),12)]
    variants={'Odd words':words[::2],'Even words':words[1::2],'Reverse words':words[::-1],'Rotate twelve word blocks one position':[t for b in blocks for t in b[1:]+b[:1]],'Alternate twelve word blocks':[t for b in blocks for t in b[::2]+b[1::2]]}
    assert sorted(t['position'] for t in variants['Odd words']+variants['Even words'])==list(range(1,len(words)+1))
    assert variants['Reverse words'][::-1]==words
    for k in ['Rotate twelve word blocks one position','Alternate twelve word blocks']:assert sorted(t['position'] for t in variants[k])==list(range(1,len(words)+1))
    checked+=4
    for k,v in variants.items():
        output=' '.join(t['word'] for t in v)
        results.append({'chapter':chapter,'rule':k,'source':m['url'],'sourceSHA256':m['normalizedTextSHA256'],'sourceWordCount':len(words),'outputWordCount':len(v),'outputSHA256':hashlib.sha256(output.encode()).hexdigest(),'preview':' '.join(t['word'] for t in v[:12]),'previewPositions':v[:12]})
globalTests=[{'rule':k,'output':' '.join(t['word'] for t in v),'positions':v} for k,v in {'First word per chapter':first,'Last word per chapter':last,'Odd chapters first words':first[::2],'Even chapters first words':first[1::2]}.items()]
data={'title':'Whole word tests across eighteen chapters','scope':'Five word order rules applied separately to every chapter, plus four chapter boundary selections. Chapters replace artwork regions for boundary tests; this is a declared analogy. Chapter headings excluded. Words preserve case and spelling; internal apostrophes and hyphens remain within words, digit expressions remain tokens. Reviewed decorative opening splits are joined explicitly: the first two tokens in chapters 3 through 18, and MR and FOSTER in chapter 2; chapter 1 is unchanged. Original spans and join pieces are retained. Positions are one based in this word tokenizer; character offsets refer to the saved normalized chapter body.','publication':'Full outputs were computed transiently; only twelve word previews, positions, counts and hashes are published. Full transformed novel text is not redistributed.','conclusion':'No new coherent message is evident in the published previews or chapter boundary selections. Full output hashes document computation, not semantic validation of every output. No hidden cipher is established or ruled out.','limits':['Circular traversal has no supplied chapter start point beyond the exploratory body start.','Twelve word blocks and a one position rotation are exploratory choices.','Each chapter is one region; individual artwork letter boundaries have no established equivalent inside chapters.','No book supplied word substitution dictionary or target plaintext is available.'],'checks':{'sourceHashesMatched':18,'exactWordSpansVerified':True,'structuralAssertions':checked,'chapterRules':90,'boundaryRules':4},'chapterTests':results,'boundaryTests':globalTests}
(root/'reports/chapter-whole-word-tests.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md='# Whole word tests across eighteen chapters\n\n'+data['scope']+'\n\n'+data['publication']+'\n\n'+data['conclusion']+'\n\n'
panel='<details id="chapterWholeWordTests"><summary>Whole word tests across eighteen chapters</summary><p>'+html.escape(data['scope'])+'</p><p>'+html.escape(data['publication'])+'</p><p class="notice">'+html.escape(data['conclusion'])+'</p>'
for t in globalTests:
    md+='## '+t['rule']+'\n\n'+t['output']+'\n\n';panel+='<h3>'+t['rule']+'</h3><p>'+html.escape(t['output'])+'</p>'
md+='| Chapter | Rule | Twelve word preview |\n|---|---|---|\n'
panel+='<div style="overflow:auto;max-height:600px"><table><thead><tr><th>Chapter</th><th>Rule</th><th>Twelve word preview</th></tr></thead><tbody>'
for t in results:
    md+=f"| {t['chapter']} | {t['rule']} | {t['preview']} |\n"
    panel+='<tr><td>'+str(t['chapter'])+'</td><td>'+t['rule']+'</td><td>'+html.escape(t['preview'])+'</td></tr>'
panel+='</tbody></table></div><p>Coordinates, counts and hashes are included in the book comparison JSON export.</p></details>'
(root/'reports/chapter-whole-word-tests.md').write_text(md,encoding='utf-8')
path=root/'src/book-study-panel.html';text=path.read_text(encoding='utf-8');text=re.sub(r'<details id="chapterWholeWordTests">.*?</details>','',text,flags=re.S);text=text.replace('<h3>Name count hypothesis</h3>',panel+'<h3>Name count hypothesis</h3>');path.write_text(text,encoding='utf-8')
book['chapterWholeWordTests']=data;(root/'src/book-study-data.json').write_text(json.dumps(book,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(data['checks']))
for t in globalTests:print(t['rule']+': '+t['output'])
