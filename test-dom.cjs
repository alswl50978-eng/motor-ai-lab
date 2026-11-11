// UI behavior plus real TensorFlow classifier fitting. Feature extractor and camera are test doubles.
const fs=require('node:fs'),assert=require('node:assert/strict');
const {JSDOM}=require('./tmp/qa/node_modules/jsdom');
const tf=require('./assets/tf.min.js');
(async()=>{
 await tf.setBackend('cpu');await tf.ready();
 const html=fs.readFileSync('index.html','utf8');
 const dom=new JSDOM(html,{url:'https://example.org/',runScripts:'outside-only'}),w=dom.window,d=w.document;
 w.tf=tf;w.confirm=()=>true;let printed=false;w.print=()=>{printed=true;};
 w.localStorage.setItem('unrelated','keep');
 const fakeBase={infer:c=>tf.tensor2d([c.feature||[12,0,0]],[1,3])};
 w.mobilenet={load:async()=>fakeBase};
 w.eval(fs.readFileSync('app.js','utf8')+'\nwindow.testAPI={addSample,decision,predict,makePrint,setBase:x=>base=x,state:()=>({ready,busy,version,sizes:samples.map(s=>s.length),records,last,classifier}),setHead:m=>{classifier?.dispose();classifier=m;ready=true;sync();}};');
 const api=w.testAPI;
 const ids=[...d.querySelectorAll('[id]')].map(x=>x.id);assert.equal(new Set(ids).size,ids.length);
 for(const el of d.querySelectorAll('script[src],link[href],a[download]'))assert(fs.existsSync(el.getAttribute('src')||el.getAttribute('href')));
 for(const a of d.querySelectorAll('a[href^="#"]')){const id=a.getAttribute('href').slice(1);if(id)assert(d.getElementById(id));}
 assert(d.querySelector('#train').disabled);assert(d.querySelector('#predict-camera').disabled);
 assert.equal(api.decision([.69,.2,.11]).index,-1);assert.equal(api.decision([.7,.2,.1]).index,0);
 const photo=i=>({feature:[0,0,0].map((_,j)=>i===j?12:0),toDataURL:()=> 'data:image/png;base64,AA=='});
 for(let i=0;i<3;i++)for(let j=0;j<5;j++)api.addSample(i,photo(i));
 assert(!d.querySelector('#train').disabled);await d.querySelector('#train').onclick();
 assert(api.state().ready);assert.equal(api.state().version,1);assert.equal(d.querySelector('#training-progress').value,30);
 const score=tf.tidy(()=>Array.from(api.state().classifier.predict(tf.tensor2d([[12,0,0]])).dataSync()));assert(score.every(Number.isFinite));assert(Math.abs(score.reduce((a,b)=>a+b,0)-1)<1e-4);
 // Deterministic predictions test the lamp and record paths independently of random training outcomes.
 let scores=[.91,.05,.04];api.setHead({predict:()=>tf.tensor2d([scores]),dispose(){}});
 await api.predict(photo(0));assert(d.querySelector('#lamp-room').classList.contains('on'));
 assert(d.querySelector('#record').disabled);d.querySelector('#truth').value='0';d.querySelector('#truth').onchange();d.querySelector('#record').onclick();assert.equal(api.state().records.length,1);d.querySelector('#record').onclick();assert.equal(api.state().records.length,1);
 scores=[.1,.85,.05];await api.predict(photo(1));assert(!d.querySelector('#lamp-room').classList.contains('on'));
 scores=[.3,.3,.4];await api.predict(photo(2));assert.equal(api.state().last.index,-1);assert.match(d.querySelector('#prediction').textContent,/보류/);
 d.querySelector('#truth').value='2';d.querySelector('#truth').onchange();d.querySelector('#record').onclick();assert.match(d.querySelector('#record-summary').textContent,/50%/);
 api.addSample(0,photo(0));assert(!api.state().ready);assert(d.querySelector('#test-file').disabled);
 // A download error must not leave the previous lamp on or predictions enabled.
 api.setBase(null);w.mobilenet.load=async()=>{throw new Error('offline')};await d.querySelector('#train').onclick();assert(!api.state().ready);assert.match(d.querySelector('#train-status').textContent,/실패/);assert(!d.querySelector('#lamp-room').classList.contains('on'));
 d.querySelector('#q1').value='<script>test</script>';d.querySelector('#q1').dispatchEvent(new w.Event('input'));assert(w.localStorage.getItem('light-lab-answers-v1').includes('script'));
 d.querySelector('#print-answers').onclick();assert(printed);assert.equal(d.querySelector('#print-area script'),null);assert(d.querySelector('#print-area').textContent.includes('<script>test</script>'));
 d.querySelector('#clear-answers').onclick();assert.equal(w.localStorage.getItem('unrelated'),'keep');assert.equal(d.querySelector('#q1').value,'');
 d.querySelector('#clear-samples').onclick();assert(api.state().sizes.every(n=>n===0));assert(d.querySelector('#train').disabled);
 d.querySelector('#clear-records').onclick();assert.equal(api.state().records.length,0);
 await d.querySelector('#start-camera').onclick();assert.match(d.querySelector('#camera-status').textContent,/실패/);
 dom.window.close();console.log('PASS: real TF classifier fit; collection/retraining guards; ON/OFF/hold; versioned records; failure recovery; scoped storage; safe print; links/assets.');
})().catch(e=>{console.error(e);process.exitCode=1;});
