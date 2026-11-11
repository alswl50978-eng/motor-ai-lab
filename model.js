/* Original educational MLP. No runtime dependencies. Synthetic data only. */
(function(root){
  function rng(seed){return ()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};}
  function data(mode='basic',seed=31,n=80){
    const r=rng(seed),out=[];
    for(let i=0;i<n;i++){
      const y=i%2, type=mode==='basic'?(y?'hot-fault':'normal'):['normal','hot-fault','hot-normal','cool-fault'][i%4];
      const hot=type.startsWith('hot'),fault=type.endsWith('fault');
      const temp=hot?67+r()*16:32+r()*17;
      const vibration=fault?3.8+r()*2.1:0.5+r()*1.4;
      const current=fault?5.8+r()*2:3.1+r()*2.5;
      out.push({id:i+1,temp,current,vibration,y:+fault,type,x:[(temp-25)/65,current/10,vibration/8]});
    }return out;
  }
  function network(seed=42){
    const r=rng(seed),sizes=[3,6,4,1];
    return sizes.slice(1).map((size,l)=>Array.from({length:size},()=>({w:Array.from({length:sizes[l]},()=>(r()*2-1)*0.8),b:0})));
  }
  function forward(net,x){const a=[x];net.forEach((layer,l)=>a.push(layer.map(n=>{let z=n.b+n.w.reduce((s,w,j)=>s+w*a[l][j],0);return l===net.length-1?1/(1+Math.exp(-z)):Math.tanh(z);})));return a;}
  function train(mode){
    const net=network(),rows=data(mode),history=[];
    for(let epoch=0;epoch<700;epoch++){
      let loss=0;
      for(const row of rows){
        const a=forward(net,row.x),p=a[3][0],delta=[[],[],[p-row.y]];
        loss-=row.y*Math.log(Math.max(p,1e-9))+(1-row.y)*Math.log(Math.max(1-p,1e-9));
        for(let l=1;l>=0;l--) delta[l]=net[l].map((_,j)=>net[l+1].reduce((s,n,k)=>s+n.w[j]*delta[l+1][k],0)*(1-a[l+1][j]**2));
        for(let l=0;l<3;l++)net[l].forEach((n,k)=>{n.w=n.w.map((w,j)=>w-0.025*delta[l][k]*a[l][j]);n.b-=0.025*delta[l][k];});
      }
      if(epoch%25===0||epoch===699)history.push(loss/rows.length);
    }
    return {net,history,mode};
  }
  function evaluate(model,rows,threshold=.5){let tp=0,tn=0,fp=0,fn=0;const results=rows.map(row=>{const score=forward(model.net,row.x)[3][0],pred=+(score>=threshold);if(row.y){if(pred)tp++;else fn++;}else{if(pred)fp++;else tn++;}return {...row,score,pred};});return {tp,tn,fp,fn,accuracy:(tp+tn)/rows.length,recall:tp/(tp+fn),results};}
  const api={rng,data,network,forward,train,evaluate};if(typeof module!=='undefined')module.exports=api;else root.MotorAI=api;
})(globalThis);
