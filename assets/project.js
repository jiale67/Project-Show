(function(){
  'use strict';
  const slides=[...document.querySelectorAll('.slide')];
  const params=new URLSearchParams(location.search);
  if(params.has('preview'))return;
  const embedded=params.get('embed')==='1'&&window.parent!==window;
  if(embedded)document.body.classList.add('embedded');
  const index=()=>slides.findIndex(s=>s.classList.contains('is-active'));
  const notify=()=>{if(embedded)window.parent.postMessage({type:'project-state',id:document.body.dataset.project,idx:index(),total:slides.length,title:slides[index()]?.dataset.title,notes:!!document.querySelector('.notes-overlay.open'),overview:!!document.querySelector('.overview.open')},'*');};
  const select=document.getElementById('slide-select');
  slides.forEach((s,i)=>{const op=document.createElement('option');op.value=i;op.textContent=(i+1)+' · '+s.dataset.title;select.append(op);});
  function key(k){document.dispatchEvent(new KeyboardEvent('keydown',{key:k,bubbles:true}));}
  function go(n){location.hash='#/'+(Math.max(0,Math.min(slides.length-1,n))+1);}
  function step(delta){
    const n=index()+delta;
    if(n<0||n>=slides.length){if(embedded)window.parent.postMessage({type:'project-edge',id:document.body.dataset.project,delta},'*');return;}
    go(n);
  }
  const seen=new WeakSet();
  function sync(){
    const idx=index();select.value=String(idx);
    document.getElementById('slide-position').textContent=(idx+1)+' / '+slides.length;
    document.getElementById('prev-slide').disabled=idx===0;
    document.getElementById('next-slide').disabled=idx===slides.length-1;
    slides.forEach((s,i)=>s.querySelectorAll('video').forEach(v=>{
      if(i!==idx)v.pause();
      else if(!v.getAttribute('src'))v.src=v.dataset.src;
    }));
    const note=document.querySelector('.notes-overlay');
    if(note&&!note.querySelector('.notes-close')){
      const close=document.createElement('button');close.className='notes-close';close.textContent='关闭 ×';close.onclick=()=>note.classList.remove('open');note.prepend(close);
    }
    notify();
  }
  document.getElementById('prev-slide').onclick=()=>step(-1);
  document.getElementById('next-slide').onclick=()=>step(1);
  select.onchange=()=>go(Number(select.value));
  document.querySelectorAll('[data-key]').forEach(b=>b.onclick=()=>key(b.dataset.key));
  new MutationObserver(sync).observe(document.querySelector('.deck'),{subtree:true,attributes:true,attributeFilter:['class']});
  function observeOverlays(){
    document.querySelectorAll('.notes-overlay,.overview').forEach(el=>new MutationObserver(notify).observe(el,{attributes:true,attributeFilter:['class']}));
    if(!embedded){
      const tools=document.querySelector('.deck-tools'),deck=document.querySelector('.deck');
      const fitControls=()=>{
        const reserved=tools.getBoundingClientRect().height;
        document.body.style.setProperty('--tools-height',reserved+'px');
        deck.style.setProperty('--deck-scale',String(Math.min(innerWidth/1920,Math.max(0,innerHeight-reserved)/1080)));
      };
      window.addEventListener('resize',fitControls);
      new ResizeObserver(fitControls).observe(tools);
      document.fonts.ready.then(fitControls);
      fitControls();
    }
    sync();
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',observeOverlays);else observeOverlays();
  document.addEventListener('keydown',e=>{
    if(e.target instanceof Element){
      const nativeControl=e.target.closest('select,input,textarea,video');
      const nativeActivation=e.target.closest('button,a')&&[' ','Enter'].includes(e.key);
      if(nativeControl||nativeActivation){e.stopImmediatePropagation();return;}
    }
    if(e.ctrlKey||e.altKey||e.metaKey)return;
    if(embedded){
      let delta=['ArrowRight','PageDown',' '].includes(e.key)?1:['ArrowLeft','PageUp'].includes(e.key)?-1:0;
      if(delta&&(index()+delta<0||index()+delta>=slides.length)){e.preventDefault();e.stopImmediatePropagation();step(delta);}
      if(e.key==='Escape'&&!document.querySelector('.overview.open,.notes-overlay.open')){window.parent.postMessage({type:'project-close'},'*');}
    }
  },true);
  window.addEventListener('message',e=>{
    if(!embedded||e.source!==window.parent)return;
    const d=e.data;if(!d||d.type!=='project-command')return;
    if(d.action==='step')step(d.delta);
    else if(d.action==='goto')go(d.idx);
    else if(d.action==='key')key(d.key);
    else if(d.action==='state')notify();
    else if(d.action==='pause')document.querySelectorAll('video').forEach(v=>v.pause());
  });
  document.querySelectorAll('video').forEach(v=>{
    v.addEventListener('error',()=>{
      if(seen.has(v))return;seen.add(v);
      const p=document.createElement('div');p.className='video-error';
      const a=document.createElement('a');a.href=v.dataset.src;a.textContent='在浏览器中打开视频 ↗';a.target='_blank';a.rel='noopener';p.append(a);v.parentElement.append(p);
    });
  });
  window.addEventListener('pagehide',()=>document.querySelectorAll('video').forEach(v=>v.pause()));
  window.addEventListener('hashchange',()=>setTimeout(sync,30));
  sync();
})();
