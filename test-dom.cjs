// Run: npm install --prefix tmp/qa jsdom && node test-dom.cjs
// jsdom tests event logic; this is not a browser layout or print-engine test.
const {JSDOM}=require('./tmp/qa/node_modules/jsdom');
const fs=require('node:fs'),assert=require('node:assert/strict');
(async()=>{
 const html=fs.readFileSync('index.html','utf8');
 const dom=new JSDOM(html,{url:'https://example.test/motor-ai-lab/',runScripts:'outside-only'}),w=dom.window,d=w.document;
 let printed=false,downloaded=false;
 w.confirm=()=>true;w.print=()=>{printed=true};w.URL.createObjectURL=()=>{downloaded=true;return 'blob:test'};w.URL.revokeObjectURL=()=>{};w.HTMLAnchorElement.prototype.click=function(){};
 w.eval(fs.readFileSync('model.js','utf8'));w.eval(fs.readFileSync('app.js','utf8'));
 assert.equal(d.querySelectorAll('#data-body tr').length,40);
 const ids=[...d.querySelectorAll('[id]')].map(e=>e.id);assert.equal(new Set(ids).size,ids.length);
 for(const a of d.querySelectorAll('a[href^="#"]')){const id=a.getAttribute('href').slice(1);if(id)assert(d.getElementById(id));}
 for(const el of d.querySelectorAll('script[src],link[href],a[download]')){const f=el.getAttribute('src')||el.getAttribute('href');assert(fs.existsSync(f),f);}
 d.querySelector('#train').click();await new Promise(r=>setTimeout(r,150));
 assert.equal(d.querySelector('#test-acc').textContent,'85.0%');assert.equal(d.querySelector('#fp').textContent,'5');
 d.querySelector('#record').click();assert.equal(d.querySelectorAll('#record-body tr').length,1);
 d.querySelector('[value=diverse]').checked=true;d.querySelector('#train').click();await new Promise(r=>setTimeout(r,150));
 assert.equal(d.querySelector('#test-acc').textContent,'100.0%');d.querySelector('#record').click();assert.equal(d.querySelectorAll('#record-body tr').length,2);
 const slider=d.querySelector('#threshold');slider.value='.3';slider.dispatchEvent(new w.Event('input'));assert.equal(d.querySelector('#threshold-value').textContent,'0.30');
 const answer=d.querySelector('#q1');answer.value='<script>test</script> 테스트 답안';answer.dispatchEvent(new w.Event('input'));
 assert(JSON.parse(w.localStorage.getItem('motor-ai-lab-v1')).q1.includes('테스트'));
 d.querySelector('#print-answers').click();assert(printed);assert(d.querySelector('#print-area').textContent.includes('테스트 답안'));assert.equal(d.querySelectorAll('#print-area script').length,0);
 d.querySelector('[data-quiz=right]').click();assert(d.querySelector('#quiz-feedback').textContent.includes('맞아요'));
 d.querySelector('#csv').click();assert(downloaded);
 d.querySelector('#clear-answers').click();assert.equal(answer.value,'');
 d.querySelector('#clear-records').click();assert(d.querySelector('#record-body').textContent.includes('A 학습'));
 dom.window.close();console.log('PASS: load, anchors/assets, A/B training, threshold, records, local save, print content/escaping, quiz, CSV, resets.');
})().catch(e=>{console.error(e);process.exitCode=1;});
