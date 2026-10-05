from pathlib import Path
import json,re,hashlib,html
root=Path(__file__).resolve().parents[1]
source=root/'reports/whitepaper-image-extraction.json'
d=json.loads(source.read_text(encoding='utf-8'))
letters=d['letterRecords']
units=[]
for r in letters:
    words=[]
    for match in re.finditer(r'\[[^\]]+\]|[A-Za-z]+(?:[-’\'][A-Za-z]+)*',r['transcription']):
        raw=match.group();uncertain=raw.startswith('[')
        words.append({'raw':raw,'initial':'?' if uncertain else raw[0].upper(),'final':'?' if uncertain else raw[-1].upper(),'characterStart':match.start(),'characterEnd':match.end()})
    initials=''.join(w['initial'] for w in words)
    units.append({'index':r['index'],'block':r['block'],'letter':r['displayLetter'],'confidence':r['confidence'],'wordCount':len(words),'tokens':words,'initials':initials,'oddInitials':initials[::2],'evenInitials':initials[1::2],'reverseInitials':initials[::-1]})
first=''.join(u['initials'][0] if u['initials'] else '?' for u in units)
last=''.join(u['initials'][-1] if u['initials'] else '?' for u in units)
continuous=''.join(u['initials'] for u in units)
tests=[{'rule':'First word initial per large letter','output':first},{'rule':'Last word initial per large letter','output':last},{'rule':'Odd large letters first initials','output':first[::2]},{'rule':'Even large letters first initials','output':first[1::2]},{'rule':'Reverse large letter order first initials','output':first[::-1]},{'rule':'Odd words across displayed order','output':continuous[::2]},{'rule':'Even words across displayed order','output':continuous[1::2]},{'rule':'Reverse words across displayed order','output':continuous[::-1]}]
alignment=json.loads((root/'reports/whitepaper-alignment-summary.json').read_text(encoding='utf-8'))
report={'title':'Rules applied to the artwork lettering','sourceSHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'readingOrder':'WELCOME, TO, THE, BRAVE, NEW, WORLD. Footer excluded from these letter based tests.','scope':'Applied to the existing provisional manual transcription after visual inspection of the supplied artwork. The original letter records are preserved. Split words are not silently joined, spellings are not repaired, uncertain bracketed readings become one unknown token. These are token order tests, not verified paths around glyph outlines.','conclusion':'No evident sustained readable message appears in these fixed output strings. The transcription remains provisional. Neither these outputs nor apparent whitepaper differences establish a cipher.','limits':['Circular path reading and compass traversal require spatial word coordinates and an explicit start point; they were not approximated by invented coordinates.','The 25 large letters are not a twelve position ring. Rotating their order without a selected start is underdetermined.','Visual line breaks are only partially recorded, so alternating lines is not a reliable test on this transcription.','Alignment differences may be handwriting or transcription errors. No anomaly letters are accepted as hidden plaintext.'],'tests':tests,'units':units,'referenceDifferences':alignment['alignmentDifferenceGroups']}
assert len(units)==25
for u in units:
    assert u['reverseInitials'][::-1]==u['initials']
    assert len(u['oddInitials'])+len(u['evenInitials'])==len(u['initials'])
(root/'reports/artwork-text-rule-tests.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
md='# Rules applied to the artwork lettering\n\n'+report['scope']+'\n\n'+report['conclusion']+'\n\n'
panel='<details id="artworkTextRuleTests"><summary>Rules applied to the artwork lettering</summary><p>'+html.escape(report['scope'])+'</p><p class="notice">'+html.escape(report['conclusion'])+'</p>'
for t in tests:
    md+='## '+t['rule']+'\n\n'+t['output']+'\n\n'
    panel+='<h3>'+t['rule']+'</h3><p style="overflow-wrap:anywhere">'+t['output']+'</p>'
md+='## Individual letter regions\n\n| Position | Block | Letter | Odd word initials | Even word initials |\n|---|---|---|---|---|\n'
panel+='<div style="overflow:auto;max-height:500px"><table><thead><tr><th>Position</th><th>Block</th><th>Letter</th><th>Odd word initials</th><th>Even word initials</th></tr></thead><tbody>'
for u in units:
    md+=f"| {u['index']} | {u['block']} | {u['letter']} | {u['oddInitials']} | {u['evenInitials']} |\n"
    panel+='<tr>'+''.join('<td>'+str(u[k])+'</td>' for k in ['index','block','letter','oddInitials','evenInitials'])+'</tr>'
panel+='</tbody></table></div><ul>'+''.join('<li>'+html.escape(x)+'</li>' for x in report['limits'])+'</ul><p>Source tokens, positions, outputs and provisional whitepaper differences are included in the book comparison JSON export.</p></details>'
md+='\n## Limits\n\n'+'\n'.join('- '+x for x in report['limits'])+'\n'
(root/'reports/artwork-text-rule-tests.md').write_text(md,encoding='utf-8')
p=root/'src/book-study-panel.html';s=p.read_text(encoding='utf-8');s=re.sub(r'<details id="artworkTextRuleTests">.*?</details>','',s,flags=re.S);p.write_text(s.replace('<h3>Name count hypothesis</h3>',panel+'<h3>Name count hypothesis</h3>'),encoding='utf-8')
p=root/'src/book-study-data.json';book=json.loads(p.read_text(encoding='utf-8'));book['artworkTextRuleTests']=report;p.write_text(json.dumps(book,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'letterRegions':len(units),'wholeRegionRules':len(tests),'firstInitials':first,'lastInitials':last,'checks':'passed'}))
