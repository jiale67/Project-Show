(function(){
  'use strict';
  const projects=window.PROJECTS;
  const defaults=validate(window.PROJECT_ORDER);
  const KEY='ren-jiale-project-order-v1';
  let order=defaults.slice(),editing=false,dragId=null,currentId=null,state={idx:0,total:0},lastFocus=null;
  let notifyTimer=null;
  function validate(o){const seen=new Set();return [...(Array.isArray(o)?o:[]),...Object.keys(projects)].filter(id=>projects[id]&&!seen.has(id)&&seen.add(id));}
  try{const saved=JSON.parse(localStorage.getItem(KEY));if(saved&&JSON.stringify(saved.defaults)===JSON.stringify(defaults))order=validate(saved.order);}catch(e){}
  const $=id=>document.getElementById(id);
  const viewer=$('viewer'),frame=$('project-frame');
  function toast(msg){$('toast').textContent=msg;$('toast').hidden=false;clearTimeout(notifyTimer);notifyTimer=setTimeout(()=>$('toast').hidden=true,2400);}
  function save(){try{localStorage.setItem(KEY,JSON.stringify({order,defaults}));}catch(e){toast('当前排序已应用；可导出排序文件保存。');}}
  function move(id,delta){const i=order.indexOf(id),n=i+delta;if(n<0||n>=order.length)return;[order[i],order[n]]=[order[n],order[i]];save();render();}
  function render(){
    const grid=$('project-grid');grid.replaceChildren();
    order.forEach((id,i)=>{
      const p=projects[id],card=document.createElement('article');card.className='project-card';card.dataset.id=id;card.draggable=editing;
      card.innerHTML='<div><div class="project-no">'+String(i+1).padStart(2,'0')+' / PROJECT</div><h3>'+p.title+'</h3><p>'+p.desc+'</p><div class="tags">'+p.tags+'</div><button class="card-link" data-open>查看项目 <span aria-hidden="true">→</span></button><a class="independent" href="'+p.url+'" target="_blank" rel="noopener">独立打开 ↗</a></div><figure class="img-frame"><img src="'+p.photo+'" alt="'+p.title+'演示帧"></figure><div class="card-meta"><span>'+p.context+'</span><span>'+p.count+' 页</span></div>';
      card.querySelector('[data-open]').onclick=()=>open(id);
      if(editing){const edit=document.createElement('div');edit.className='edit-controls';edit.innerHTML='<span>⋮⋮ 拖动调整顺序</span><span><button data-up aria-label="上移'+p.title+'" '+(i===0?'disabled':'')+'>↑</button> <button data-down aria-label="下移'+p.title+'" '+(i===order.length-1?'disabled':'')+'>↓</button></span>';edit.querySelector('[data-up]').onclick=()=>move(id,-1);edit.querySelector('[data-down]').onclick=()=>move(id,1);card.append(edit);}
      card.addEventListener('dragstart',e=>{if(!editing)return;dragId=id;e.dataTransfer.setData('text/plain',id);e.dataTransfer.effectAllowed='move';card.classList.add('dragging');});
      card.addEventListener('dragend',()=>{dragId=null;document.querySelectorAll('.dragging,.drop-target').forEach(el=>el.classList.remove('dragging','drop-target'));});
      card.addEventListener('dragover',e=>{if(editing&&dragId&&dragId!==id){e.preventDefault();e.dataTransfer.dropEffect='move';card.classList.add('drop-target');}});
      card.addEventListener('dragleave',()=>card.classList.remove('drop-target'));
      card.addEventListener('drop',e=>{e.preventDefault();if(!editing||!dragId||dragId===id)return;const target=order.indexOf(id);order.splice(order.indexOf(dragId),1);order.splice(target,0,dragId);dragId=null;save();render();});
      grid.append(card);
    });
    $('edit-order').textContent=editing?'正在调整顺序':'调整展示顺序 ↕';$('edit-order').setAttribute('aria-pressed',String(editing));$('edit-bar').hidden=!editing;
    $('viewer-tabs').replaceChildren();
    order.forEach((id,i)=>{const b=document.createElement('button');b.textContent=(i+1)+' '+projects[id].title;b.classList.toggle('active',id===currentId);b.onclick=()=>open(id);$('viewer-tabs').append(b);});
  }
  function command(data){if(!viewer.hidden)frame.contentWindow.postMessage({type:'project-command',...data},'*');}
  function open(id,at=0){
    if(!projects[id])return;
    if(viewer.hidden){lastFocus=document.activeElement;$('portal-main').inert=true;document.body.style.overflow='hidden';}
    currentId=id;state={idx:0,total:projects[id].count};viewer.hidden=false;
    $('viewer-project-title').textContent=projects[id].title;$('open-independent').href=projects[id].url+'#/'+(at+1);
    $('viewer-slide-select').replaceChildren();projects[id].slides.forEach((title,i)=>{const o=document.createElement('option');o.value=i;o.textContent=(i+1)+' · '+title;$('viewer-slide-select').append(o);});
    frame.src=projects[id].url+'?embed=1#/'+(at+1);render();updateState({idx:at,total:projects[id].count});
    $('close-viewer').focus();
  }
  function close(){
    command({action:'pause'});viewer.hidden=true;$('portal-main').inert=false;document.body.style.overflow='';frame.removeAttribute('src');currentId=null;
    if(document.fullscreenElement)document.exitFullscreen().catch(()=>{});
    if(lastFocus&&lastFocus.isConnected)lastFocus.focus();
  }
  function edge(delta){
    const i=order.indexOf(currentId),n=i+delta;
    if(n<0){toast('已到第一个项目。');return;}
    if(n>=order.length){toast('四个项目已演示完毕。');return;}
    open(order[n],delta<0?projects[order[n]].count-1:0);
  }
  function step(delta){if(viewer.hidden)return;if(state.idx+delta<0||state.idx+delta>=state.total)edge(delta);else command({action:'step',delta});}
  function updateState(s){
    state=s;const p=projects[currentId];if(!p)return;
    const pos=order.indexOf(currentId),done=order.slice(0,pos).reduce((n,id)=>n+projects[id].count,0),total=order.reduce((n,id)=>n+projects[id].count,0);
    $('viewer-page-count').textContent='项目 '+(pos+1)+' / '+order.length+' · '+(s.idx+1)+' / '+s.total+' 页';
    $('viewer-progress').style.width=((done+s.idx+1)/total*100)+'%';
    $('viewer-slide-select').value=String(s.idx);$('previous').disabled=pos===0&&s.idx===0;$('next').disabled=pos===order.length-1&&s.idx===s.total-1;
    $('open-independent').href=p.url+'#/'+(s.idx+1);
  }
  async function fullscreen(){try{if(document.fullscreenElement)await document.exitFullscreen();else await viewer.requestFullscreen();}catch(e){toast('也可使用浏览器 F11 全屏。');}}
  window.addEventListener('message',e=>{if(viewer.hidden||e.source!==frame.contentWindow)return;const d=e.data;if(!d)return;if(d.id&&d.id!==currentId)return;if(d.type==='project-state')updateState(d);else if(d.type==='project-edge')edge(d.delta);else if(d.type==='project-close')close();});
  frame.addEventListener('load',()=>command({action:'state'}));
  $('edit-order').onclick=()=>{editing=!editing;render();};$('finish-order').onclick=()=>{editing=false;render();toast('展示顺序已保存。');};
  $('reset-order').onclick=()=>{order=defaults.slice();save();render();toast('已恢复默认顺序。');};
  $('export-order').onclick=()=>{const text='// 项目展示默认顺序。可调整数组中的 id。\nwindow.PROJECT_ORDER = '+JSON.stringify(order,null,2)+';\n';const blob=new Blob([text],{type:'text/javascript;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='展示顺序.js';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);toast('用下载文件替换本目录的“展示顺序.js”即可分享排序。');};
  $('start-presentation').onclick=()=>open(order[0]);$('close-viewer').onclick=close;
  $('previous').onclick=()=>step(-1);$('next').onclick=()=>step(1);$('viewer-slide-select').onchange=()=>command({action:'goto',idx:Number($('viewer-slide-select').value)});
  $('viewer-fullscreen').onclick=fullscreen;$('viewer-notes').onclick=()=>command({action:'key',key:'n'});$('viewer-presenter').onclick=()=>command({action:'key',key:'s'});
  $('show-help').onclick=()=>$('help-dialog').showModal();
  document.addEventListener('keydown',e=>{
    if(viewer.hidden||e.ctrlKey||e.metaKey||e.altKey)return;
    if(e.key==='Escape'){if(state.notes||state.overview)command({action:'key',key:'Escape'});else close();return;}
    if(e.target instanceof Element&&e.target.closest('input,select,textarea'))return;
    if(e.key==='ArrowRight'||e.key==='PageDown'){step(1);e.preventDefault();}
    else if(e.key==='ArrowLeft'||e.key==='PageUp'){step(-1);e.preventDefault();}
    else if(e.key===' '&&!(e.target instanceof Element&&e.target.closest('button,a'))){step(1);e.preventDefault();}
    else if(e.key.toLowerCase()==='f'){fullscreen();e.preventDefault();}
    else if(['n','s','o'].includes(e.key.toLowerCase())){command({action:'key',key:e.key.toLowerCase()});e.preventDefault();}
  });
  document.addEventListener('fullscreenchange',()=>{$('viewer-fullscreen').textContent=document.fullscreenElement?'退出全屏 F':'全屏 F';});
  render();
})();
