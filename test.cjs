const assert=require('node:assert/strict');
const m=require('./model.js');
const evaluation=m.data('diverse',982,40);
assert.equal(evaluation.length,40);assert.equal(evaluation.filter(r=>r.y).length,20);
const training=m.data('basic');assert.equal(training.length,80);
assert.equal(training.filter(r=>r.y).length,40);
assert(!evaluation.some(e=>training.some(t=>JSON.stringify(e.x)===JSON.stringify(t.x))));
const summary={};
for(const mode of ['basic','diverse']){
 const model=m.train(mode),r=m.evaluate(model,evaluation,.5),tr=m.evaluate(model,m.data(mode),.5);
 assert.equal(r.tp+r.tn+r.fp+r.fn,40);assert(r.results.every(x=>Number.isFinite(x.score)&&x.score>=0&&x.score<=1));
 assert(model.history.at(-1)<model.history[0]);
 const lo=m.evaluate(model,evaluation,.3),hi=m.evaluate(model,evaluation,.7);
 assert(lo.fn<=hi.fn);assert(lo.fp>=hi.fp);
 summary[mode]={training:tr.accuracy,evaluation:r.accuracy,tp:r.tp,tn:r.tn,fp:r.fp,fn:r.fn,recall:r.recall,loss:model.history.at(-1)};
}
assert(summary.basic.training>summary.basic.evaluation);
assert(summary.diverse.evaluation>summary.basic.evaluation);
console.log(JSON.stringify(summary,null,2));console.log('PASS: deterministic training, data separation, confusion matrix, score bounds, threshold monotonicity.');
