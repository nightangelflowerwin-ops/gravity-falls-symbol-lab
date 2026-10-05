from pathlib import Path
root=Path(__file__).resolve().parent
shell=(root/'src/shell.html').read_text(encoding='utf-8')
panel=(root/'src/calendar-panel.html').read_text(encoding='utf-8')
engine=(root/'src/calendar-engine.js').read_text(encoding='utf-8')
data=(root/'src/data.json').read_text(encoding='utf-8')
research_panel=(root/'src/research-panel.html').read_text(encoding='utf-8')
research_engine=(root/'src/research-engine.js').read_text(encoding='utf-8').replace('__RESEARCH_DATA__',(root/'src/research-data.json').read_text(encoding='utf-8'))
research_panel=research_panel.replace('__DECIPHER_PANEL__',(root/'src/decipher-panel.html').read_text(encoding='utf-8'))
panel+=research_panel.replace('__SEGREGATION_PANEL__',(root/'src/segregation-panel.html').read_text(encoding='utf-8')).replace('__GLOBAL_CATALOG_PANEL__',(root/'src/global-catalog-panel.html').read_text(encoding='utf-8'))
engine+='\n'+research_engine
engine+='\n'+(root/'src/segregation-engine.js').read_text(encoding='utf-8').replace('__SEGREGATION_DATA__',(root/'src/segregation-data.json').read_text(encoding='utf-8'))
engine+='\n'+(root/'src/global-catalog-engine.js').read_text(encoding='utf-8').replace('__GLOBAL_CATALOG_DATA__',(root/'src/global-catalog-data.json').read_text(encoding='utf-8'))
engine+='\n'+(root/'src/decipher-engine.js').read_text(encoding='utf-8').replace('__DECIPHER_DATA__',(root/'src/decipher-data.json').read_text(encoding='utf-8'))
shell=shell.replace('<footer>',panel+'<footer>',1).replace('__DATA__',data).replace('</script></html>','</script>\n<script>'+engine+'</script></html>')
shell=shell.replace('<title>Gravity Falls · Image Dictionary</title>','<title>Gravity Falls · Symbol and Calendar Lab</title>')
(root/'index.html').write_text(shell,encoding='utf-8')
print('Built index.html')
