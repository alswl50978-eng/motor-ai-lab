'use strict';
const $=id=>document.getElementById(id);
const LABELS=['손바닥','주먹','손 없음'], ICONS=['✋','✊','▧'];
const MIN=5, MAX=40, EPOCHS=30, THRESHOLD=.7, KEY='light-lab-answers-v1';
let samples=[[],[],[]], base=null, classifier=null, stream=null, busy=false, ready=false, version=0, last=null, records=[];
function setLamp(on,message){$('lamp-room').classList.toggle('on',on);$('lamp-state').textContent=message;}
function invalidate(){ready=false;last=null;$('record').disabled=true;$('prediction').textContent='사진이 바뀌었습니다. 다시 학습하세요.';setLamp(false,'학습 대기 · 전등 꺼짐');}
function sync(){
 $('train').disabled=busy||samples.some(s=>s.length<MIN);
 $('clear-samples').disabled=busy;
 $('start-camera').disabled=busy||!!stream;
 $('stop-camera').disabled=busy||!stream;
 $('predict-camera').disabled=busy||!ready||!stream;
 $('test-file').disabled=busy||!ready;
 document.querySelectorAll('[data-capture]').forEach(b=>b.disabled=busy||!stream||samples[+b.dataset.capture].length>=MAX);
 document.querySelectorAll('[data-upload]').forEach(b=>b.disabled=busy||samples[+b.dataset.upload].length>=MAX);
 document.querySelectorAll('[data-remove]').forEach(b=>b.disabled=busy||!samples[+b.dataset.remove].length);
 LABELS.forEach((_,i)=>{$('count-'+i).textContent=samples[i].length+' / '+MAX+'장';});
}
LABELS.forEach((name,i)=>{
 const card=document.createElement('article');card.className='sample-card';
 card.innerHTML=`<div class="sample-heading"><h3>${ICONS[i]} ${name}</h3><span id="count-${i}" class="small"></span></div><div class="actions"><button data-capture="${i}">지금 모습 1장 담기</button><label class="file-button">사진 파일 추가<input type="file" accept="image/*" multiple data-upload="${i}" aria-label="${name} 학습 사진 추가"></label><button class="text-button" data-remove="${i}">마지막 사진 빼기</button></div><div class="thumbs" id="thumbs-${i}"></div>`;
 $('sample-cards').append(card);
});
function frame(source){
 const w=source.videoWidth||source.naturalWidth||source.width,h=source.videoHeight||source.naturalHeight||source.height;
 if(!w||!h)throw new Error('카메라 영상이 아직 준비되지 않았습니다. 잠시 후 다시 눌러 주세요.');
 const c=document.createElement('canvas');c.width=c.height=224;
 // Preserve the whole frame with letterboxing; training and inference use exactly the same preprocessing.
 const ctx=c.getContext('2d'),scale=Math.min(224/w,224/h);ctx.fillStyle='#000';ctx.fillRect(0,0,224,224);ctx.drawImage(source,(224-w*scale)/2,(224-h*scale)/2,w*scale,h*scale);return c;
}
function addSample(i,c){
 if(samples[i].length>=MAX)return;
 samples[i].push(c);const img=document.createElement('img');img.src=c.toDataURL('image/jpeg',.8);img.alt=LABELS[i]+' 학습 사진 '+samples[i].length;$('thumbs-'+i).append(img);
 invalidate();$('train-status').textContent=samples.every(s=>s.length>=MIN)?'사진이 준비됐어요. 학습하기를 눌러 주세요.':'세 종류를 각각 5장 이상 모으세요.';sync();
}
function loadImage(file){return new Promise((resolve,reject)=>{
 if(!file.type.startsWith('image/'))return reject(new Error('이미지 파일을 선택하세요.'));
 if(file.size>15*1024*1024)return reject(new Error('사진 한 장은 15MB 이하로 선택하세요.'));
 const url=URL.createObjectURL(file),img=new Image();img.onload=()=>{URL.revokeObjectURL(url);resolve(img);};img.onerror=()=>{URL.revokeObjectURL(url);reject(new Error('사진을 읽지 못했습니다. JPG 또는 PNG를 시도하세요.'));};img.src=url;
});}
$('start-camera').onclick=async()=>{
 if(busy)return;busy=true;sync();
 try{
  if(!navigator.mediaDevices?.getUserMedia)throw new Error('카메라를 사용할 수 없는 환경입니다. HTTPS 주소에서 열거나 사진 파일을 이용하세요.');
  stream=await navigator.mediaDevices.getUserMedia({video:{width:640,height:480},audio:false});$('camera').srcObject=stream;await $('camera').play();$('camera-placeholder').hidden=true;$('camera-status').textContent='카메라가 켜졌어요. 손과 배경만 담아 주세요.';
 }catch(e){stopCamera();$('camera-status').textContent='카메라 연결 실패: '+e.message+' 사진 파일로도 실습할 수 있어요.';}
 finally{busy=false;sync();}
};
function stopCamera(){if(stream)stream.getTracks().forEach(t=>t.stop());stream=null;$('camera').srcObject=null;$('camera-placeholder').hidden=false;$('camera-status').textContent='카메라를 껐습니다.';sync();}
$('stop-camera').onclick=stopCamera;window.addEventListener('pagehide',stopCamera);
document.querySelectorAll('[data-capture]').forEach(b=>b.onclick=()=>{try{addSample(+b.dataset.capture,frame($('camera')));}catch(e){$('camera-status').textContent=e.message;}});
document.querySelectorAll('[data-upload]').forEach(input=>input.onchange=async()=>{
 if(busy)return;busy=true;sync();const i=+input.dataset.upload;let errors=0;
 try{for(const file of input.files){if(samples[i].length>=MAX)break;try{addSample(i,frame(await loadImage(file)));}catch(e){errors++;$('camera-status').textContent=e.message;}}}
 finally{input.value='';busy=false;sync();if(errors)$('train-status').textContent='일부 파일을 읽지 못했습니다. 사진 개수를 확인하세요.';}
});
document.querySelectorAll('[data-remove]').forEach(b=>b.onclick=()=>{const i=+b.dataset.remove;samples[i].pop();$('thumbs-'+i).lastElementChild?.remove();invalidate();sync();$('train-status').textContent='사진이 바뀌었어요. 개수를 확인하고 다시 학습하세요.';});
async function getBase(){if(!base){if(!window.tf||!window.mobilenet)throw new Error('학습 라이브러리를 읽지 못했습니다. 페이지 파일을 확인하세요.');await tf.ready();base=await mobilenet.load({version:2,alpha:0.5});}return base;}
function features(c){return tf.tidy(()=>base.infer(c,true).flatten());}
function newClassifier(size){const model=tf.sequential();model.add(tf.layers.dense({inputShape:[size],units:3,activation:'softmax'}));model.compile({optimizer:tf.train.adam(.003),loss:'categoricalCrossentropy'});return model;}
$('train').onclick=async()=>{
 if(busy||samples.some(s=>s.length<MIN))return;
 busy=true;invalidate();sync();$('train-status').textContent='사전학습 모델을 준비합니다. 처음에는 다운로드 시간이 필요합니다.';$('training-progress').value=0;
 let rows=[],X=null,Y=null,next=null;
 try{
  await getBase();const labels=[];
  for(let i=0;i<3;i++)for(const c of samples[i]){rows.push(features(c));labels.push(i);await tf.nextFrame();}
  X=tf.stack(rows);Y=tf.tidy(()=>tf.oneHot(tf.tensor1d(labels,'int32'),3));rows.forEach(t=>t.dispose());rows=[];
  next=newClassifier(X.shape[1]);
  const counts=samples.map(s=>s.length),total=counts.reduce((a,b)=>a+b,0);
  await next.fit(X,Y,{epochs:EPOCHS,batchSize:Math.min(16,total),shuffle:true,classWeight:Object.fromEntries(counts.map((n,i)=>[i,total/(3*n)])),callbacks:{onEpochEnd:async(epoch,logs)=>{
   $('training-progress').value=epoch+1;$('train-status').textContent=`학습 중 ${epoch+1} / ${EPOCHS}`;$('loss').textContent='학습 손실: '+logs.loss.toFixed(4)+' · 낮아져도 새 사진에서 확인해야 합니다.';await tf.nextFrame();
  }}});
  if(classifier)classifier.dispose();classifier=next;next=null;version++;ready=true;$('train-status').textContent=`모델 v${version} 학습 완료! 학습에 쓰지 않은 새 사진으로 테스트하세요.`;$('prediction').textContent='새 사진을 선택하거나 지금 모습을 예측하세요.';
 }catch(e){$('train-status').textContent='학습 실패: '+e.message+' 인터넷 연결과 모델 다운로드 허용 여부를 확인하고 다시 시도하세요.';}
 finally{rows.forEach(t=>t.dispose());X?.dispose();Y?.dispose();next?.dispose();busy=false;sync();}
};
function decision(scores){let i=0;for(let j=1;j<3;j++)if(scores[j]>scores[i])i=j;return {index:scores[i]>=THRESHOLD?i:-1,score:scores[i]};}
async function predict(c){
 if(busy||!ready)return;busy=true;last=null;$('record').disabled=true;setLamp(false,'예측 중 · 전등 꺼짐');sync();
 try{
  const scores=tf.tidy(()=>{const f=features(c).expandDims(0);return Array.from(classifier.predict(f).dataSync());});
  if(scores.some(v=>!Number.isFinite(v)))throw new Error('예측 점수를 계산하지 못했습니다. 다시 학습하세요.');
  const d=decision(scores);last={...d,version,scores};$('test-preview').src=c.toDataURL('image/jpeg',.8);$('test-preview').hidden=false;
  $('scores').replaceChildren();scores.forEach((v,i)=>{const row=document.createElement('div');row.className='score-row';row.innerHTML=`<span>${LABELS[i]}</span><div class="bar"><i style="width:${Math.max(0,Math.min(100,v*100))}%"></i></div><span>${(v*100).toFixed(1)}%</span>`;$('scores').append(row);});
  $('prediction').textContent=d.index<0?'판단 보류 · 한 종류의 점수가 충분히 높지 않아요.':`AI 분류: ${LABELS[d.index]} · 모델 v${version}`;
  setLamp(d.index===0,d.index===0?'켜기 · 전등 ON':d.index===1?'끄기 · 전등 OFF':d.index===2?'손 없음 · 대기 / OFF':'판단 보류 · OFF');
  $('truth').value='';$('record-status').textContent='실제 손동작을 선택하고 기록하세요.';
 }catch(e){$('prediction').textContent='예측 실패: '+e.message;}
 finally{busy=false;sync();}
}
$('predict-camera').onclick=async()=>{try{await predict(frame($('camera')));}catch(e){$('prediction').textContent=e.message;}};
$('test-file').onchange=async function(){const f=this.files[0];this.value='';if(!f||busy||!ready)return;busy=true;sync();try{const c=frame(await loadImage(f));busy=false;await predict(c);}catch(e){$('prediction').textContent=e.message;}finally{busy=false;sync();}};
$('truth').onchange=()=>{$('record').disabled=!last||$('truth').value==='';};
$('record').onclick=()=>{if(!last||$('truth').value==='')return;records.push({...last,truth:+$('truth').value});last=null;$('record').disabled=true;renderRecords();$('record-status').textContent='기록했습니다. 다음 새 사진을 테스트하세요.';};
function renderRecords(){
 $('records').replaceChildren();if(!records.length){const tr=document.createElement('tr'),td=document.createElement('td');td.colSpan=5;td.textContent='새 사진을 테스트하고 기록하세요.';tr.append(td);$('records').append(tr);}
 records.forEach((r,i)=>{const tr=document.createElement('tr');[i+1,'v'+r.version,LABELS[r.truth],r.index<0?'보류':LABELS[r.index],r.index<0?'보류':r.truth===r.index?'맞음':'틀림'].forEach(v=>{const td=document.createElement('td');td.textContent=v;tr.append(td);});$('records').append(tr);});
 const versions=[...new Set(records.map(r=>r.version))];$('record-summary').textContent=versions.length?versions.map(v=>{const a=records.filter(r=>r.version===v),correct=a.filter(r=>r.index===r.truth).length,hold=a.filter(r=>r.index<0).length;return `v${v}: ${a.length}회 중 ${correct}회 맞음 (${(correct/a.length*100).toFixed(0)}%), 보류 ${hold}회 포함`;}).join(' / ')+' · 이 기록의 결과이며 일반 성능을 뜻하지 않습니다.':'정답을 선택한 기록으로만 집계합니다.';
}
$('clear-records').onclick=()=>{if(confirm('테스트 기록을 지울까요?')){records=[];renderRecords();}};
$('clear-samples').onclick=()=>{if(busy||!confirm('학습 사진과 모델을 지울까요? 답안과 테스트 기록은 유지합니다.'))return;samples=[[],[],[]];LABELS.forEach((_,i)=>$('thumbs-'+i).replaceChildren());classifier?.dispose();classifier=null;invalidate();$('training-progress').value=0;$('loss').textContent='학습 결과는 실행 후 표시됩니다.';$('train-status').textContent='세 종류를 각각 5장 이상 모으세요.';sync();};
let saved={};try{saved=JSON.parse(localStorage.getItem(KEY)||'{}')||{};}catch{}
document.querySelectorAll('[data-save]').forEach(el=>{el.value=typeof saved[el.id]==='string'?saved[el.id]:'';el.addEventListener('input',()=>{try{const a={};document.querySelectorAll('[data-save]').forEach(x=>a[x.id]=x.value);localStorage.setItem(KEY,JSON.stringify(a));$('save-status').textContent='답안을 이 브라우저에 저장했습니다.';}catch{$('save-status').textContent='자동 저장을 사용할 수 없습니다. 인쇄/PDF로 저장하세요.';}});});
$('clear-answers').onclick=()=>{if(!confirm('이 실습의 답안만 지울까요?'))return;try{localStorage.removeItem(KEY);}catch{}document.querySelectorAll('[data-save]').forEach(x=>x.value='');$('save-status').textContent='이 실습 답안을 지웠습니다.';};
function makePrint(){const area=$('print-area');area.replaceChildren();const h=document.createElement('h1');h.textContent='LIGHT LAB · 손동작 AI 스위치';area.append(h);const team=document.createElement('p');team.textContent='모둠: '+$('team').value;area.append(team);document.querySelectorAll('.question').forEach(q=>{const article=document.createElement('article'),title=document.createElement('h2'),prompt=document.createElement('p'),a=document.createElement('p');title.textContent=q.querySelector('h3').textContent;prompt.textContent=q.querySelector('p').textContent;a.textContent=q.querySelector('textarea').value||'\n\n';article.append(title,prompt,a);area.append(article);});area.append($('records').closest('table').cloneNode(true));const summary=document.createElement('p');summary.textContent=$('record-summary').textContent;area.append(summary);}
$('print-answers').onclick=()=>{makePrint();window.print();};window.addEventListener('beforeprint',makePrint);sync();
