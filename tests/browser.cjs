const {chromium}=require('playwright');
const assert=require('node:assert/strict'),path=require('node:path'),{pathToFileURL}=require('node:url');
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.BROWSER_CHANNEL?{channel:process.env.BROWSER_CHANNEL}:{})});
 const page=await browser.newPage({viewport:{width:1440,height:1000},acceptDownloads:true});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(pathToFileURL(path.resolve(__dirname,'../index.html')).href);
 await page.waitForFunction(()=>calReady&&calControls.length===13,null,{timeout:60000});
 const report=await page.evaluate(()=>calSerializable());
 assert(report.controls.every(c=>c.pass));assert.equal(report.results.length,30);assert.equal(report.sensitivityAudit.runs.length,360);
 assert(report.results.filter(r=>['gold','goldSwap','week','younger'].includes(r.method)).every(r=>r.matched===0));
 const checks=await page.evaluate(()=>runTests());assert(checks.slice(0,6).every(c=>c.accuracy===1));
 await page.selectOption('#calFilter','gold');assert.equal(await page.locator('#calResults tbody tr').count(),6);
 await page.getByText('Recorded sensitivity audit · 360 comparisons',{exact:true}).click();await page.selectOption('#calSweepFilter','55');assert.equal(await page.locator('#calSweepResults tbody tr').count(),24);
 await page.fill('#calText','ᚠ□ᚢᛜ');await page.click('#calTextRun');assert.match(await page.locator('#calTextResult').textContent(),/1 □ 2 □/);
 await page.selectOption('#calFilter','elder');await page.fill('#calText','ᛜᛝ');await page.click('#calTextRun');assert.match(await page.locator('#calTextResult').textContent(),/ŋ ŋ/);
 await page.selectOption('#calFilter','all');await page.click('#calControl');assert.match(await page.locator('#calTextResult').textContent(),/17 18 19/);
 await page.check('#calReverse');await page.click('#calRun');await page.waitForFunction(()=>calResults.length===30&&calResults.every(r=>r.direction==='reversed'));
 const reversed=await page.evaluate(()=>calSerializable());assert.deepEqual(reversed.results.map(r=>r.total),report.results.map(r=>r.total));
 await page.uncheck('#calReverse');await page.click('#calRun');await page.waitForFunction(()=>calResults.length===30&&calResults.every(r=>r.direction==='original'));
 const downloadPromise=page.waitForEvent('download');await page.click('#calExport');assert.equal((await downloadPromise).suggestedFilename(),'runic-calendar-experiment.json');
 await page.setViewportSize({width:390,height:844});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 assert.deepEqual(errors,[]);require('node:fs').writeFileSync(path.resolve(__dirname,'../reports/browser-verification.json'),JSON.stringify({passed:true,calendarControls:13,sensitivityComparisons:360,checks:['six source samples reproduced','method filter','sensitivity filter','strict rune transcription','Ingwaz lookup','known control','reverse preserves counts','JSON export','390px mobile width','no browser errors']},null,2));await browser.close();console.log('Passed calendar controls, 360-record audit, sample reproduction, filters, strict transcription, reversal, export and mobile width.');
})().catch(e=>{console.error(e);process.exit(1)});

