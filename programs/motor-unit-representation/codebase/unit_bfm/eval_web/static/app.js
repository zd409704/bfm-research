'use strict';
const $ = id => document.getElementById(id);
const state = {catalog:null, cases:[], trajectory:null, frame:0, playing:false, elapsed:0, last:null, request:0, jobKey:null};
const liveState = {id:null,count:0,status:null,trajectory:null,viewing:false,busy:false,generation:0};
const colors = ['#3279c4','#36a69e','#db883b','#9462bd'];
const fmt = (v,d=3) => v == null || !Number.isFinite(v) ? '—' : v.toFixed(d);
function error(e) {$('error').textContent = typeof e === 'string' ? e : e.message; $('error').hidden=false;}
async function api(path, body) {
  const options = body === undefined ? {} : {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)};
  const r = await fetch(path,options); const result = await r.json();
  if (!r.ok) throw new Error(result.error || `HTTP ${r.status}`); return result;
}
const query = (path, obj) => `${path}?${new URLSearchParams(obj)}`;
function options(select, rows, value='id', label='label') {
  select.replaceChildren(...rows.map(row => {const o=document.createElement('option');o.value=row[value];o.textContent=row[label];return o;}));
}
function safeRun(fn) {return (...args) => Promise.resolve().then(()=>fn(...args)).catch(error);}
function planInfo() {
  const p=state.catalog.plans.find(p=>p.id===$('plan').value);
  $('plan-description').textContent=p?.description||'';
  $('plan-count').textContent=p?.count.toLocaleString()||'—';
}
async function catalog(keep=true) {
  const previous={cp:$('checkpoint').value,plan:$('plan').value,ev:$('evaluation').value};
  const result=await api('/api/catalog');state.catalog=result;
  options($('checkpoint'),result.checkpoints);options($('plan'),result.plans,'id','name');options($('evaluation'),result.evaluations);
  if(keep && result.checkpoints.some(r=>r.id===previous.cp))$('checkpoint').value=previous.cp;
  if(keep && previous.plan)$('plan').value=previous.plan;
  if(keep && result.evaluations.some(r=>r.id===previous.ev))$('evaluation').value=previous.ev;
  else if(!keep && result.evaluations.some(r=>r.id==='rf_v2_full/motion_panel'))$('evaluation').value='rf_v2_full/motion_panel';
  options($('video-select'),result.videos,'url','label');
  if(result.videos.length)$('video').src=$('video-select').value;
  planInfo();showJob(result.job);
}
async function selectEvaluation() {
  leaveLive();stop();const id=$('evaluation').value;if(!id)return;
  $('loading').textContent='Read Results...';
  const result=await api(query('/api/evaluation',{id}));
  if($('evaluation').value!==id)return;
  $('provenance').textContent=`Current view:${result.checkpoint} · ${result.label}. The above checkpoint is used for a new assessment.`;
  options($('dataset'),result.files.map(f=>({id:f.name,label:`${f.name} · ${f.count}Track`})));
  if(result.files.some(f=>f.name==='reward_query.npz'))$('dataset').value='reward_query.npz';
  const root=$('summary');root.replaceChildren();
  for(const row of result.summary){const div=document.createElement('div');div.className='summary-row';
    const name=document.createElement('span');name.textContent=row.name;
    const value=document.createElement('span');value.className='value';value.textContent=fmt(row.value,4);
    const unit=document.createElement('small');unit.textContent=row.unit;value.append(unit);
    const note=document.createElement('span');note.className='hint';note.textContent=row.note;
    div.append(name,value,note);root.append(div);}
  $('metrics-link').href=query('/asset',{path:id+'/'+(result.kind==='nominal'?'summary.json':result.kind==='atlas'?'index.json':'metrics.json')});
  await selectDataset();
}
async function selectDataset() {
  stop();const id=$('evaluation').value,file=$('dataset').value;if(!id||!file)return;
  const cases=await api(query('/api/cases',{id,file}));
  if(id!==$('evaluation').value||file!==$('dataset').value)return;
  state.cases=cases;
  const filters=[{id:'all',label:'All cases'}];
  const keys=new Set();for(const c of cases){const key=c.period===null?c.task:`p${c.period}`;
    if(!keys.has(key)){keys.add(key);filters.push({id:key,label:c.period===null?c.task:c.period===0?'Fixed First Command':`${c.period}ms Switch`});}}
  options($('filter'),filters);$('download').href=query('/asset',{path:id+'/'+file});
  await filterCases();
}
async function filterCases() {
  const filter=$('filter').value;
  const cases=state.cases.filter(c=>filter==='all'||(c.period===null?c.task:`p${c.period}`)===filter);
  options($('case'),cases,'index','label');
  $('case-count').textContent=`Show${cases.length} / ${state.cases.length}bars;arranged by original index`;
  await selectCase();
}
async function selectCase() {
  leaveLive();stop();const req=++state.request;$('loading').textContent='Prepare trajectory...';
  const trajectory=await api(query('/api/trajectory',{id:$('evaluation').value,file:$('dataset').value,index:$('case').value}));
  if(req!==state.request)return;
  if(trajectory.session?.config?.physics)trajectory.goal.scope += ' '+physicsReport(trajectory.session);
  state.trajectory=trajectory;state.frame=0;state.elapsed=0;$('timeline').max=trajectory.time.length-1;$('timeline').value=0;
  $('compare').disabled=!trajectory.comparison;
  $('compare-label').textContent=trajectory.comparison_label||'Collapse Parsing Reference';
  $('stage-label').textContent='Save qpos playback. Non-replicate';$('play').disabled=false;
  $('show-target').disabled=trajectory.goal.kind==='random';
  const goal=trajectory.goal;
  $('goal-title').textContent=goal.title;$('goal-source').textContent=goal.source;
  $('goal-expression').textContent=goal.expression;$('goal-description').textContent=goal.description;
  $('goal-criterion').textContent=goal.criterion;$('goal-scope').textContent=goal.scope;
  $('goal-semantics').textContent=goal.semantics;
  const kind=trajectory.evaluation.kind;
  $('case-note').textContent=goal.kind==='random'?'Randomz does not specify targets; motion differences are influenced by both primary and random dynamics.':kind==='analytic'?'The parsing controller calculates the action directly, without the use of z; this file still saves the corresponding query code.':kind.startsWith('switch')?'Toggle the indicator to have a whole-way transient; short call does not require instantaneous arrival.':trajectory.case.task==='Speed'?'The velocity error is calculated on a sample with a distance greater than 0.15 rad along the target direction; the curved line shows the target after the boundary drops.':trajectory.case.task==='Adaptive.'?'The target force rectangular is calculated by the current q/dq, which represents the driving force rectangular relationship and does not amount to arbitrary exposure control.':'The indicator describes actual errors and does not set a threshold for ex post success; stopping by a limit cannot automatically be considered a high-quality brake.';
  const cards=$('case-metrics');cards.replaceChildren();
  for(const metric of trajectory.metrics){const card=document.createElement('div');card.textContent=metric.label;
    const b=document.createElement('b');b.textContent=fmt(metric.value,metric.unit==='%'?1:3);const unit=document.createElement('small');unit.textContent=metric.unit;b.append(unit);card.append(b);
    const other=trajectory.comparison?.metrics.find(m=>m.label===metric.label);if(other){const em=document.createElement('em');em.textContent=`${trajectory.comparison_label||'Analytical'} ${fmt(other.value,3)} ${other.unit}`;card.append(em);}cards.append(card);}
  $('loading').textContent=`${trajectory.time.length}Frame 100 Hz`;
  drawAll();
}
function canvasContext(canvas) {
  const rect=canvas.getBoundingClientRect(),dpr=Math.min(window.devicePixelRatio||1,2);
  const w=Math.max(1,rect.width),h=Math.max(1,rect.height);
  if(canvas.width!==Math.round(w*dpr)||canvas.height!==Math.round(h*dpr)){canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr);}
  const ctx=canvas.getContext('2d');ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,w,h);return {ctx,w,h};
}
function drawMotion() {
  const {ctx,w,h}=canvasContext($('motion')),t=state.trajectory;if(!t)return;
  const f=state.frame,pose=t.pose,other=$('compare').checked?t.comparison?.pose:null;
  const target=$('show-target').checked?t.goal_pose:null;
  let points=[];
  const gather=(p,only)=>{for(const frame of only?[p.frames[f]]:p.frames)for(const link of frame)points.push([link[0],link[1]],[link[2],link[3]]);};
  gather(pose,$('follow').checked);if(other)gather(other,$('follow').checked);if(target)gather(target,$('follow').checked);
  let xmin=Infinity,xmax=-Infinity,zmin=Infinity,zmax=-Infinity;
  for(const [x,z] of points){xmin=Math.min(xmin,x);xmax=Math.max(xmax,x);zmin=Math.min(zmin,z);zmax=Math.max(zmax,z);}
  if(pose.ground)zmin=Math.min(zmin,0);
  const cx=(xmin+xmax)/2,cz=(zmin+zmax)/2;
  const scale=Math.min((w-100)/Math.max(.75,xmax-xmin+.35),(h-95)/Math.max(.8,zmax-zmin+.25));
  const X=x=>w/2+(x-cx)*scale,Z=z=>h/2+12-(z-cz)*scale;
  ctx.lineWidth=1;ctx.strokeStyle='#e1e7ef';
  for(let x=Math.floor((cx-w/2/scale)/.2)*.2;x<cx+w/2/scale;x+=.2){ctx.beginPath();ctx.moveTo(X(x),0);ctx.lineTo(X(x),h);ctx.stroke();}
  for(let z=Math.floor((cz-h/2/scale)/.2)*.2;z<cz+h/2/scale;z+=.2){ctx.beginPath();ctx.moveTo(0,Z(z));ctx.lineTo(w,Z(z));ctx.stroke();}
  if(pose.ground){ctx.fillStyle='#e4e9e9';ctx.fillRect(0,Z(0),w,h-Z(0));ctx.strokeStyle='#9daab3';ctx.beginPath();ctx.moveTo(0,Z(0));ctx.lineTo(w,Z(0));ctx.stroke();}
  function render(p,ghost){p.frames[f].forEach((r,i)=>{ctx.lineCap='round';ctx.lineWidth=ghost?7:13;ctx.strokeStyle=ghost?'#a6b1bc':p.links[i].color;ctx.globalAlpha=ghost?.48:1;
    ctx.beginPath();ctx.moveTo(X(r[0]),Z(r[1]));ctx.lineTo(X(r[2]),Z(r[3]));ctx.stroke();
    ctx.lineWidth=2;ctx.fillStyle=ghost?'#e1e5e9':'#fff';ctx.beginPath();ctx.arc(X(r[0]),Z(r[1]),5,0,Math.PI*2);ctx.fill();ctx.stroke();
    if(!ghost){ctx.fillStyle='#41566e';ctx.font='11px sans-serif';ctx.fillText(p.links[i].name,(X(r[0])+X(r[2]))/2+12,(Z(r[1])+Z(r[3]))/2);}});ctx.globalAlpha=1;}
  if(other)render(other,true);render(pose,false);
  const distal=pose.links.findIndex(l=>l.name==='D'),motor=pose.frames[f][distal];
  if(target){ctx.strokeStyle='#b57b10';ctx.fillStyle='#9c6809';ctx.lineWidth=3;ctx.setLineDash([8,5]);
    target.frames[f].forEach((r,i)=>{if(!['D','T'].includes(target.links[i].name))return;
      ctx.beginPath();ctx.moveTo(X(r[0]),Z(r[1]));ctx.lineTo(X(r[2]),Z(r[3]));ctx.stroke();
      ctx.setLineDash([]);ctx.beginPath();ctx.arc(X(r[2]),Z(r[3]),7,0,Math.PI*2);ctx.stroke();ctx.setLineDash([8,5]);});
    ctx.setLineDash([]);ctx.font='12px sans-serif';const r=target.frames[f][distal];
    ctx.fillText(`q* ${fmt(t.targets.q[f])} rad`,X(r[2])+10,Z(r[3])-10);
  }
  if($('show-target').checked&&motor&&['velocity','brake','compliance'].includes(t.goal.kind)){
    const key=t.goal.kind==='compliance'?'tau':'dq',value=t.targets[key][f],x=X(motor[0]),y=Z(motor[1]),radius=32;
    ctx.strokeStyle='#b57b10';ctx.fillStyle='#9c6809';ctx.lineWidth=3;ctx.setLineDash([]);
    if(Math.abs(value)>.0001){const sign=Math.sign(value),a0=-Math.PI/2,a1=a0+sign*1.8;
      ctx.beginPath();ctx.arc(x,y,radius,a0,a1,sign<0);ctx.stroke();
      const ex=x+radius*Math.cos(a1),ey=y+radius*Math.sin(a1),tx=-Math.sin(a1)*sign,ty=Math.cos(a1)*sign;
      ctx.beginPath();ctx.moveTo(ex,ey);ctx.lineTo(ex-10*tx-5*ty,ey-10*ty+5*tx);ctx.lineTo(ex-10*tx+5*ty,ey-10*ty-5*tx);ctx.closePath();ctx.fill();
    }else{ctx.setLineDash([4,4]);ctx.beginPath();ctx.arc(x,y,radius,0,Math.PI*2);ctx.stroke();ctx.setLineDash([]);}
    ctx.font='12px sans-serif';ctx.fillText(`${key==='tau'?'τ*':'dq*'} ${fmt(value,2)} ${key==='tau'?'N·m':'rad/s'}`,x+44,y-25);
  }
  for(const e of t.perturbations?.[f]||[]){const idx=pose.links.findIndex(l=>l.name===e.side);if(idx<0)continue;
    const r=pose.frames[f][idx],x=X(r[0]+e.fraction*(r[2]-r[0])),y=Z(r[1]+e.fraction*(r[3]-r[1]));
    ctx.strokeStyle='#b65c41';ctx.fillStyle='#a04c34';ctx.lineWidth=3;ctx.setLineDash([]);
    const force=Math.hypot(e.fx,e.fz);
    if(force>.0001){const dx=e.fx/force,dy=-e.fz/force,length=Math.min(85,Math.max(18,force*10));
      ctx.beginPath();ctx.moveTo(x-length*dx,y-length*dy);ctx.lineTo(x,y);ctx.stroke();
      ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x-10*dx-5*dy,y-10*dy+5*dx);ctx.lineTo(x-10*dx+5*dy,y-10*dy-5*dx);ctx.closePath();ctx.fill();
      ctx.font='11px sans-serif';ctx.fillText(`Outburst #${e.id} ${fmt(force,1)} N`,x-length*dx-10,y-length*dy-10);}
    if(Math.abs(e.my)>.0001){const sign=Math.sign(e.my),a0=-Math.PI/2,a1=a0+sign*1.8,rr=23;
      ctx.beginPath();ctx.arc(x,y,rr,a0,a1,sign<0);ctx.stroke();
      const ex=x+rr*Math.cos(a1),ey=y+rr*Math.sin(a1),tx=-Math.sin(a1)*sign,ty=Math.cos(a1)*sign;
      ctx.beginPath();ctx.moveTo(ex,ey);ctx.lineTo(ex-8*tx-4*ty,ey-8*ty+4*tx);ctx.lineTo(ex-8*tx+4*ty,ey-8*ty-4*tx);ctx.closePath();ctx.fill();
      ctx.font='11px sans-serif';ctx.fillText(`My...${fmt(e.my,2)} N·m`,x+30,y+18);}
  }
  ctx.fillStyle='#7d8b9d';ctx.font='10px sans-serif';ctx.fillText('x →   z ↑   / m',16,h-15);
  ctx.fillText('x-z plane . Grid 0.2 m',Math.max(16,w-190),h-15);
}
const chartDefs={q:{keys:['q'],limits:[-1.2,1.2]},dq:{keys:['dq']},tau:{keys:['tau']},u:{keys:['u'],limits:[-1,1]},force:{keys:['p_fx','p_fz','d_fx','d_fz']},moment:{keys:['p_my','d_my']},contact:{keys:['p_contact','d_contact'],limits:[0,1]}};
function drawChart(canvas,key) {
  const {ctx,w,h}=canvasContext(canvas),t=state.trajectory;if(!t)return;
  const def={...chartDefs[key]};if(key==='q')def.limits=t.joint_limits||[-1.2,1.2];
  const left=43,right=10,top=12,bottom=25,pw=w-left-right,ph=h-top-bottom;
  const lines=def.keys.map((name,i)=>({values:t.series[name],color:colors[key==='moment'||key==='contact'?i*2:i],dash:[]}));
  if($('show-target').checked&&t.targets[key])lines.push({values:t.targets[key],color:'#b57b10',dash:[5,4]});
  if($('compare').checked && t.comparison && def.keys.length===1)lines.push({values:t.comparison.series[key],color:'#8f99a6',dash:[3,3]});
  const values=lines.flatMap(l=>l.values.filter(v=>v!=null));if(def.limits)values.push(...def.limits);
  let lo=Math.min(...values),hi=Math.max(...values),range=Math.max(hi-lo,.2);lo-=range*.13;hi+=range*.13;
  const X=i=>left+i/Math.max(1,t.time.length-1)*pw,Y=v=>top+(hi-v)/(hi-lo)*ph;
  ctx.font='9px sans-serif';ctx.fillStyle='#7b8796';ctx.lineWidth=1;
  for(let j=0;j<=3;j++){const v=lo+(hi-lo)*j/3,y=Y(v);ctx.strokeStyle='#eaf0f4';ctx.setLineDash([]);ctx.beginPath();ctx.moveTo(left,y);ctx.lineTo(w-right,y);ctx.stroke();ctx.textAlign='right';ctx.fillText(Math.abs(v)>=100?v.toFixed(0):v.toFixed(1),left-7,y+3);}
  ctx.textAlign='center';for(let j=0;j<=5;j++)ctx.fillText(`${fmt((t.time.at(-1)||0)*j/5,1)}s`,left+pw*j/5,h-5);
  for(const event of t.events||[]){const duration=t.time.at(-1)||.01,x=left+pw*event.start/duration;
    if(event.start<=duration){ctx.fillStyle='#b65c4118';ctx.fillRect(x,top,pw*Math.min(event.duration,duration-event.start)/duration,ph);}}
  if(def.limits){ctx.strokeStyle='#d7b9b3';ctx.setLineDash([3,4]);for(const v of def.limits){ctx.beginPath();ctx.moveTo(left,Y(v));ctx.lineTo(w-right,Y(v));ctx.stroke();}}
  for(const line of lines){ctx.strokeStyle=line.color;ctx.lineWidth=1.6;ctx.setLineDash(line.dash);ctx.beginPath();let open=false;line.values.forEach((v,i)=>{if(v==null){open=false;return;}if(!open){ctx.moveTo(X(i),Y(v));open=true;}else ctx.lineTo(X(i),Y(v));});ctx.stroke();}
  ctx.setLineDash([]);ctx.strokeStyle='#233d5c55';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(X(state.frame),top);ctx.lineTo(X(state.frame),h-bottom);ctx.stroke();
  ctx.fillStyle='#2d6fbc';ctx.beginPath();ctx.arc(X(state.frame),Y(lines[0].values[state.frame]),3,0,Math.PI*2);ctx.fill();
}
function drawZ() {
  const {ctx,w,h}=canvasContext($('latent')),t=state.trajectory;if(!t||!t.z.length)return;
  const z=t.z.length===1?t.z[0]:t.z[state.frame],max=Math.max(1,...z.map(Math.abs)),margin=16,step=(w-2*margin)/16;
  ctx.strokeStyle='#dce5ee';ctx.beginPath();ctx.moveTo(margin,h/2);ctx.lineTo(w-margin,h/2);ctx.stroke();
  for(let i=0;i<16;i++){const height=z[i]/max*(h/2-25);ctx.fillStyle=z[i]>=0?'#4d8bca':'#82a9cf';ctx.fillRect(margin+i*step+2,h/2-Math.max(0,height),Math.max(2,step-5),Math.abs(height));ctx.fillStyle='#8793a2';ctx.font='8px sans-serif';ctx.textAlign='center';ctx.fillText(i+1,margin+(i+.5)*step,h-7);}
}
function drawAll() {
  const t=state.trajectory;if(!t||!t.time.length)return;
  drawMotion();document.querySelectorAll('[data-chart]').forEach(c=>drawChart(c,c.dataset.chart));drawZ();drawGoal();
  $('time-label').textContent=`${t.time[state.frame].toFixed(2)} s`;
  const live=$('live');live.replaceChildren();for(const [key,label,unit] of [['q','joint angle','rad'],['dq','Joint speed','rad/s'],['tau','Real Power Rectangular','N·m'],['u','Send Command','']]){const d=document.createElement('div');d.className='live-value';const s=document.createElement('span');s.textContent=label;const b=document.createElement('b');b.textContent=fmt(t.series[key][state.frame],key==='q'?3:2);const small=document.createElement('small');small.textContent=unit;b.append(small);d.append(s,b);live.append(d);}
}
function drawGoal() {
  const t=state.trajectory,f=state.frame,goal=t.goal,root=$('goal-values');root.replaceChildren();
  $('goal-panel').classList.toggle('no-target',goal.kind==='random');
  $('goal-phase').textContent=goal.phase?`Command${goal.phase[f]+1}. . . . . . . . . . . . . . . . . . . . . . . .`:'';
  for(const channel of goal.channels){const row=document.createElement('div');row.className='goal-value-row';
    const label=document.createElement('span');label.textContent=channel.label;
    const ref=t.targets[channel.key][f],actual=t.series[channel.key][f];
    for(const [name,value] of [['Objective',ref],['Actual',actual],['Actual - Target',actual-ref]]){
      const cell=document.createElement('div'),caption=document.createElement('small'),v=document.createElement('b');
      caption.textContent=name;v.textContent=`${fmt(value)} ${channel.unit}`;cell.append(caption,v);row.append(cell);}
    row.prepend(label);root.append(row);
  }
}

const liveFields={q:[0,1.2],dq:[1,6],tau:[12,6],u:[13,1],p_fx:[18,20],p_fz:[19,20],d_fx:[21,20],d_fz:[22,20],p_my:[20,6],d_my:[23,6],p_contact:[14,1],d_contact:[15,1]};
function leaveLive(){liveState.viewing=false;$('play').disabled=false;}
let physicsSchema=null;
function readPhysics(){return Object.fromEntries(physicsSchema.fields.map(f=>[f.key,Number($('param-'+f.key).value)]));}
function writePhysics(values){for(const f of physicsSchema.fields)$('param-'+f.key).value=String(Math.min(f.max,Math.max(f.min,Number(values[f.key].toPrecision(7)))));physicsVisibility();}
function physicsVisibility(){if(!physicsSchema)return;const role=Number($('live-role').value);
  for(const f of physicsSchema.fields)$('param-'+f.key).parentElement.hidden=!!f.roles&&!f.roles.includes(role);
  for(const [group] of physicsSchema.groups)$('physics-group-'+group).hidden=!physicsSchema.fields.some(f=>f.group===group&&(!f.roles||f.roles.includes(role)));
  physicsPreview();}
function physicsPreview(){if(!physicsSchema)return;const p=readPhysics(),angle=$('live-task').value!=='velocity'&&$('live-task').value!=='brake';
  const lo=p.lower,hi=p.upper,out=angle&&(Number($('live-target').value)<lo||Number($('live-target').value)>hi);
  const changed=Math.abs(lo+1.2)>1e-8||Math.abs(hi-1.2)>1e-8;
  $('physics-preview').textContent=`Physical limits [${fmt(lo)}, ${fmt(hi)}] rad(${fmt(lo*180/Math.PI,1)}° ~ ${fmt(hi*180/Math.PI,1)}°). The training is fixed at ±1.2 Rad (±68.8°); the original query entry limit of 0.8 Rad (45.8°) has been cancelled.${changed?' The current limits are outside training conditions.':''}${out?' The current angle reference lies outside the physical limits and can be used to observe the constrained response.':''}`;
  $('physics-preview').classList.toggle('outside',changed||out);}
function physicsReport(meta){const p=meta.config.physics,ood=meta.outside_training||[];
  return `Effective entry into force: limit [T]${fmt(p.lower)}, ${fmt(p.upper)}] rad;P ${fmt(p.lp,2)} m / ${fmt(p.mp,2)} kg,D ${fmt(p.ld,2)} m / ${fmt(p.md,2)}kg (basic mass, plus weight and density multiplier).${ood.length?' Outside training range: '+ood.join(', ')+'.':' The listed physical parameters are within the training marginal ranges; this combination may still be unseen.'}${meta.target_outside_limits?' The angle target exceeds the physical limits.':''}Enter the value that is still a simulation of the privileges.`;}
async function setupPhysics(){physicsSchema=await api('/api/live/parameters');const root=$('physics-fields');
  for(const [key,label] of physicsSchema.groups){const details=document.createElement('details');details.className='physics-group';details.id='physics-group-'+key;details.open=key==='limits';
    const summary=document.createElement('summary');summary.textContent=label;details.append(summary);const grid=document.createElement('div');grid.className='live-config-grid';
    for(const f of physicsSchema.fields.filter(f=>f.group===key)){const box=document.createElement('div');box.className='physics-field';const l=document.createElement('label');l.htmlFor='param-'+f.key;l.textContent=f.label;
      const input=document.createElement('input');input.id=l.htmlFor;input.type='number';input.min=f.min;input.max=f.max;input.step=f.step;input.value=f.default;input.addEventListener('input',physicsPreview);
      const note=document.createElement('small');note.textContent=f.key==='root_pitch'?'Training: R1 ± 0.35; R2 in the vicinity of 0 or 0 or ±0.35 rad':f.key==='root_vz'?'Training: R1 ± 0.5; R2 ± 0.3 m/s':f.key==='clearance'?'Training: 80 per cent 0.001; 20 per cent 0.02 – 0.10 m':`Training:${f.training[0]===f.training[1]?'Fixed '+f.training[0]:f.training.join(' ~ ')}${f.log?' (log-uniform)':''}`;
      box.append(l,input,note);grid.append(box);}
    details.append(grid);root.append(details);}
  physicsVisibility();}
async function samplePhysics(){const old=readPhysics();const p=await api('/api/live/sample',{role:Number($('live-role').value),seed:Number($('physics-seed').value)});
  p.lower=old.lower;p.upper=old.upper;writePhysics(p);}

function setupLive(result){
  if(['running','paused'].includes(result.status)&&result.meta.config.physics){
    const c=result.meta.config;
    for(const [id,value] of Object.entries({'live-role':c.role,'live-task':c.task,'live-target':c.alpha[1],
      'live-duration':c.duration,'live-q':c.initial_q,'live-dq':c.initial_dq,'live-k':c.task==='compliance'?c.alpha[2]:1,
      'live-d':c.task==='compliance'?c.alpha[3]:.15,'live-bias':c.task==='compliance'?c.alpha[4]:0,'physics-seed':c.seed}))$(id).value=String(value);
    $('auto-pulses').checked=c.auto_pulses;writePhysics(c.physics);liveTaskInfo();
  }
  liveState.id=result.meta.id;liveState.count=0;liveState.status=result.status;
  const series=()=>Object.fromEntries(Object.keys(liveFields).map(k=>[k,[]]));
  const pose=()=>({links:result.links,frames:[],ground:result.ground});
  const t={time:[],series:series(),targets:Object.fromEntries(result.goal.channels.map(c=>[c.key,[]])),
    joint_limits:[result.meta.config.physics?.lower??-1.2,result.meta.config.physics?.upper??1.2],
    goal:result.goal,pose:pose(),z:[result.z],perturbations:[],events:[],metrics:[],
    evaluation:{kind:'live'},comparison:{series:series(),pose:pose()},reference:{series:series()},
    comparison_label:result.meta.comparison_label,meta:result.meta};
  if(result.goal.kind==='hold')t.goal_pose=pose();
  liveState.trajectory=t;
}
function showLive(){
  const t=liveState.trajectory;if(!t)return;
  ++state.request;stop();liveState.viewing=true;state.trajectory=t;state.frame=Math.max(0,t.time.length-1);
  $('goal-title').textContent=t.goal.title;$('goal-source').textContent=t.goal.source;
  $('goal-expression').textContent=t.goal.expression;$('goal-description').textContent=t.goal.description;
  $('goal-criterion').textContent=t.goal.criterion;$('goal-scope').textContent=t.goal.scope;
  $('goal-semantics').textContent=t.goal.semantics;$('show-target').disabled=false;
  $('compare').disabled=false;$('compare-label').textContent=t.comparison_label;
  $('stage-label').textContent='Real-time CPU simulations... and grays are also subject to the same external disturbance.';
  $('play').disabled=['running','paused'].includes(liveState.status);
  $('case-note').textContent=`${t.meta.checkpoint} · ${t.meta.description} ${t.meta.note}`;
  liveMetrics();drawAll();
}
function liveMetrics(){
  const t=liveState.trajectory;if(!t?.time.length)return;
  const root=$('case-metrics');root.replaceChildren();
  const rms=a=>Math.sqrt(a.reduce((s,v)=>s+v*v,0)/Math.max(1,a.length));
  const branchMetric=(branch)=>{const q=branch.series.q,v=branch.series.dq,tau=branch.series.tau,a=t.meta.config.alpha;
    if(a[0]===0)return rms(q.slice(-100).map(x=>x-a[1]));
    if(a[0]===1){const [lo,hi]=t.joint_limits;const samples=v.filter((x,i)=>(a[1]>=0?hi-q[i]:q[i]-lo)>.15).map(x=>x-a[1]);return samples.length?rms(samples):null;}
    if(a[0]===2)return rms(v.slice(-100));
    return rms(tau.map((x,i)=>x-(a[4]+a[2]*(a[1]-q[i])-a[3]*v[i])));};
  const kind=t.meta.config.alpha[0],labels=['RMSE last second/run segment maintained','Viable inter-zone speed RMSE','Last second/run segment speed RMS','RMSE Rund Radial Rectangular Relationship'];
  const card=document.createElement('div');card.textContent=labels[kind];const b=document.createElement('b');
  b.textContent=`${fmt(branchMetric(t))} ${['rad','rad/s','rad/s','N·m'][kind]}`;
  const em=document.createElement('em');em.textContent=`Action Playback${fmt(branchMetric(t.comparison))}`;card.append(b,em);root.append(card);
}
function receiveLive(result){
  if(!result)return;
  if(result.meta.id!==liveState.id)setupLive(result);
  const t=liveState.trajectory;
  if(result.offset!==liveState.count)throw new Error('Time frame is not synchronized. Please re-open the real time image.');
  for(const row of result.frames){t.time.push(row.time);t.pose.frames.push(row.poses[0]);t.comparison.pose.frames.push(row.poses[1]);
    for(const [branch,i] of [[t,0],[t.comparison,1],[t.reference,2]])for(const [key,[column,scale]] of Object.entries(liveFields))branch.series[key].push(row.y[i][column]*scale);
    if(t.goal_pose)t.goal_pose.frames.push(row.goal_pose);
    t.perturbations.push(row.perturbations);
    const q=row.y[0][0]*1.2,v=row.y[0][1]*6,a=t.meta.config.alpha;
    if(a[0]===0){t.targets.q.push(a[1]);t.targets.dq.push(0);}
    else if(a[0]===1){const [lo,hi]=t.joint_limits;const ramp=Math.max(0,Math.min(1,(a[1]>=0?hi-q:q-lo)/.15));t.targets.dq.push(a[1]*ramp*ramp*(3-2*ramp));}
    else if(a[0]===2)t.targets.dq.push(0);
    else t.targets.tau.push(a[4]+a[2]*(a[1]-q)-a[3]*v);
  }
  liveState.count=result.count;liveState.status=result.status;t.events=result.events;
  const active=['running','paused'].includes(result.status);
  $('live-setup').disabled=active;
  $('live-start').disabled=active;$('live-stop').disabled=!active;$('live-pause').disabled=!active;
  $('live-step').disabled=result.status!=='paused';
  $('live-pause').textContent=result.status==='paused'?'Continue Simulation':'Pause Simulation';$('live-pulse').disabled=!active;$('live-view').disabled=false;
  const names={running:'Simulation in progress',paused:'Simulation Paused',completed:'Completed and saved',stopped:'Stopped and saved',failed:'Simulation Failed'};
  $('live-status').textContent=`${names[result.status]} · ${(result.count*.01).toFixed(2)} s / ${result.meta.config.duration} s · ${result.events.length}Sub-planned/ manual disturbance${result.meta.checkpoint}${liveState.viewing?'':' · Switch back to live view'}`;
  const physics=result.meta.config.physics;
  if(physics){$('live-physics-summary').textContent=physicsReport(result.meta);$('live-parameters').hidden=false;
    $('live-parameter-values').textContent=JSON.stringify(result.meta.config,null,2);}
  $('live-stats').textContent=`q RMS: Closed${fmt(result.feedback_vs_reference_q_rms)}Rad / Action Playback${fmt(result.replay_vs_reference_q_rms)} rad`;
  const log=$('pulse-log');log.replaceChildren();for(const e of result.events){const line=document.createElement('div');line.textContent=`#${e.id} · ${e.start.toFixed(2)}s · ${e.side} · Fx ${e.fx} / Fz ${e.fz} N · My ${e.my} N·m · ${e.duration}s`;log.append(line);}
  if(result.error)error(result.error);
  if(liveState.viewing){state.frame=Math.max(0,t.time.length-1);$('timeline').max=Math.max(0,t.time.length-1);$('timeline').value=state.frame;
    $('loading').textContent=`Real time${result.count}Frame 100 Hz Simulation Control`;$('play').disabled=active;
    liveMetrics();drawAll();}
}
async function livePoll(){
  if(liveState.busy)return;
  liveState.busy=true;const generation=liveState.generation;
  try{const args=liveState.id?{id:liveState.id,since:liveState.count}:{since:0};
    const result=await api(query('/api/live/state',args));
    if(generation!==liveState.generation)return;
    if(result&&(!liveState.id||result.meta.id===liveState.id)){
      const attach=!liveState.id&&['running','paused'].includes(result.status);receiveLive(result);if(attach)showLive();
    }
  }catch(e){if(generation===liveState.generation){if(e.message.includes('Real-time experiments replaced.')){liveState.id=null;liveState.count=0;}else error(e);}}
  finally{if(generation===liveState.generation)liveState.busy=false;}
}
async function liveLoop(){await livePoll();setTimeout(liveLoop,200);}
function liveTaskInfo(){const task=$('live-task').value;$('live-compliance').hidden=task!=='compliance';$('live-target').disabled=task==='brake';
  $('live-target-label').textContent=task==='velocity'?'Target dq* / Rad/s':task==='compliance'?'Spring balance qref / Rad':'Target q* / Rad';
  $('live-target').min=task==='velocity'?-4:-Math.PI;$('live-target').max=task==='velocity'?4:Math.PI;}
function stop(){state.playing=false;state.last=null;$('play').textContent='Play';$('play').setAttribute('aria-label','Play');}
function tick(now){if(state.playing&&state.trajectory){if(state.last!==null){state.elapsed+=(now-state.last)*Number($('speed').value);state.frame=Math.min(Math.floor(state.elapsed/10),state.trajectory.time.length-1);$('timeline').value=state.frame;drawAll();if(state.frame===state.trajectory.time.length-1)stop();}if(state.playing)state.last=now;}requestAnimationFrame(tick);}
function showJob(job) {
  if(!job){$('job-panel').hidden=true;return;} $('job-panel').hidden=false;
  const names={running:'Evaluation under way',completed:'Completed',failed:'Implementation Failed',cancelled:'Stopped'};
  $('job-state').textContent=names[job.status]||job.status;$('job-state').className='status-pill '+job.status;
  $('job-stage').textContent=job.stage;$('job-log').textContent=job.log||'Preparatory process...';
  $('run').disabled=job.status==='running';$('cancel').hidden=job.status!=='running';
}
async function poll(){try{const job=await api('/api/job');showJob(job);const key=job?job.id+':'+job.status:null;
  if(job?.status==='completed' && state.jobKey!==key){await catalog(true);const ev=state.catalog.evaluations.find(e=>e.id.includes(job.id));if(ev){$('evaluation').value=ev.id;await selectEvaluation();}}
  state.jobKey=key;}catch(e){error(e);}setTimeout(poll,2000);}
$('plan').addEventListener('change',planInfo);
$('run').addEventListener('click',safeRun(async()=>{$('error').hidden=true;$('run').disabled=true;try{showJob(await api('/api/run',{checkpoint:$('checkpoint').value,plan:$('plan').value}));}catch(e){$('run').disabled=false;throw e;}}));
$('cancel').addEventListener('click',safeRun(async()=>showJob(await api('/api/cancel',{}))));
$('refresh').addEventListener('click',safeRun(async()=>{await catalog(true);await selectEvaluation();}));
$('evaluation').addEventListener('change',safeRun(selectEvaluation));$('dataset').addEventListener('change',safeRun(selectDataset));$('filter').addEventListener('change',safeRun(filterCases));$('case').addEventListener('change',safeRun(selectCase));
$('play').addEventListener('click',()=>{if(state.playing)stop();else if(state.trajectory){if(state.frame>=state.trajectory.time.length-1){state.frame=0;state.elapsed=0;}state.playing=true;state.last=null;$('play').textContent='II Pause';$('play').setAttribute('aria-label','Pause');}});
$('timeline').addEventListener('input',()=>{stop();state.frame=Number($('timeline').value);state.elapsed=state.frame*10;drawAll();});
$('follow').addEventListener('change',drawAll);$('compare').addEventListener('change',drawAll);$('show-target').addEventListener('change',drawAll);
$('live-task').addEventListener('change',()=>{liveTaskInfo();physicsPreview();});
$('live-role').addEventListener('change',physicsVisibility);
$('live-target').addEventListener('input',physicsPreview);
$('physics-sample').addEventListener('click',safeRun(samplePhysics));
$('physics-reset').addEventListener('click',()=>{writePhysics(Object.fromEntries(physicsSchema.fields.map(f=>[f.key,f.default])));$('auto-pulses').checked=false;});
$('live-start').addEventListener('click',safeRun(async()=>{
  $('error').hidden=true;$('live-start').disabled=true;$('live-setup').disabled=true;$('live-status').textContent='Load Freezing weights to Simulate CPU...';
  ++liveState.generation;liveState.busy=true;
  try{const result=await api('/api/live/start',{checkpoint:$('checkpoint').value,role:Number($('live-role').value),task:$('live-task').value,
    target:Number($('live-target').value),duration:Number($('live-duration').value),initial_q:Number($('live-q').value),initial_dq:Number($('live-dq').value),
    stiffness:Number($('live-k').value),damping:Number($('live-d').value),bias:Number($('live-bias').value),
    physics:readPhysics(),seed:Number($('physics-seed').value),auto_pulses:$('auto-pulses').checked});
    setupLive(result);receiveLive(result);showLive();
  }catch(e){$('live-start').disabled=false;$('live-setup').disabled=false;throw e;}finally{liveState.busy=false;}
}));
$('live-pulse').addEventListener('click',safeRun(async()=>{showLive();const event=await api('/api/live/pulse',{id:liveState.id,
  side:$('pulse-side').value,fx:Number($('pulse-fx').value),fz:Number($('pulse-fz').value),my:Number($('pulse-my').value),
  duration:Number($('pulse-duration').value),fraction:Number($('pulse-fraction').value)});
  $('live-status').textContent=`I'm in a disturbance #${event.id}:: Simulation${event.start.toFixed(2)}s works`;await livePoll();
}));
$('live-pause').addEventListener('click',safeRun(async()=>{await api('/api/live/control',{id:liveState.id,action:liveState.status==='paused'?'resume':'pause'});await livePoll();}));
$('live-step').addEventListener('click',safeRun(async()=>{await api('/api/live/control',{id:liveState.id,action:'step'});await livePoll();}));
$('live-stop').addEventListener('click',safeRun(async()=>{await api('/api/live/control',{id:liveState.id,action:'stop'});await livePoll();await catalog(true);}));
$('live-view').addEventListener('click',showLive);
$('video-select').addEventListener('change',()=>{$('video').src=$('video-select').value;});
document.querySelectorAll('[data-chart]').forEach(c=>c.addEventListener('click',e=>{if(!state.trajectory)return;stop();const rect=c.getBoundingClientRect();state.frame=Math.round(Math.max(0,Math.min(1,(e.clientX-rect.left-43)/(rect.width-53)))*(state.trajectory.time.length-1));state.elapsed=state.frame*10;$('timeline').value=state.frame;drawAll();}));
new ResizeObserver(()=>drawAll()).observe($('motion'));
if(location.protocol==='file:'){error('Start local services: unit_bfm/.venv/bin/python-m unit_bfm.eval_web.server-port 8766, then open http://127.0.0.1:8766');}
else safeRun(async()=>{await setupPhysics();await catalog(false);await selectEvaluation();state.jobKey=state.catalog.job?state.catalog.job.id+':'+state.catalog.job.status:null;poll();liveLoop();})();
requestAnimationFrame(tick);
