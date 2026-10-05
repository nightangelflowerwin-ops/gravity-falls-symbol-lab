from pathlib import Path
root=Path(__file__).resolve().parent
shell=(root/'src/shell.html').read_text(encoding='utf-8')
panel=(root/'src/calendar-panel.html').read_text(encoding='utf-8')
engine=(root/'src/calendar-engine.js').read_text(encoding='utf-8')
data=(root/'src/data.json').read_text(encoding='utf-8')
shell=shell.replace('<footer>',panel+'<footer>',1).replace('__DATA__',data).replace('</script></html>','</script>\n<script>'+engine+'</script></html>')
shell=shell.replace('<title>Gravity Falls · Image Dictionary</title>','<title>Gravity Falls · Symbol and Calendar Lab</title>')
(root/'index.html').write_text(shell,encoding='utf-8')
print('Built index.html')
