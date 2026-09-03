/* نواف الشريف · site.js (shared by all pages, both languages) */
(function(){
  'use strict';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hasGsap = typeof gsap !== 'undefined';
  const en = document.documentElement.lang === 'en';
  const rtl = document.documentElement.dir !== 'ltr';
  const WA = 'https://wa.me/966548767480';
  const T = en ? {
    close:'Close ✕', prev:'Previous', next:'Next', lbHint:'Click anywhere to close',
    similar:'I want something similar', similarMsg:'Hello Nawaf, I saw this project on your site and I want something similar',
    formIntro:'Hello Nawaf, I came from your website.', name:'Name', biz:'Business', sit:'Situation', mailSubject:'Inquiry from the website'
  } : {
    close:'اغلاق ✕', prev:'السابق', next:'التالي', lbHint:'اضغط في اي مكان للاغلاق',
    similar:'اريد عمل مشابه', similarMsg:'مرحبا نواف، شفت هذا العمل في موقعك واريد شي مشابه',
    formIntro:'مرحبا نواف، وصلتك من موقعك.', name:'الاسم', biz:'النشاط', sit:'وصف الحالة', mailSubject:'استفسار من الموقع'
  };
  if (hasGsap && typeof ScrollTrigger !== 'undefined') gsap.registerPlugin(ScrollTrigger);

  /* ── hero transform scene ── */
  const scene = document.getElementById('scene');
  let pinned = false;
  if (scene) {
    const cv = document.getElementById('cv');
    const ctx = cv.getContext('2d');
    const hlA = document.getElementById('hlA');
    const hlB = document.getElementById('hlB');
    const cue = scene.querySelector('.scroll-cue');
    const lerp = (a,b,t)=>a+(b-a)*t;
    const hex = h=>[parseInt(h.slice(1,3),16),parseInt(h.slice(3,5),16),parseInt(h.slice(5,7),16)];
    const mix = (c1,c2,t)=>`rgb(${Math.round(lerp(c1[0],c2[0],t))},${Math.round(lerp(c1[1],c2[1],t))},${Math.round(lerp(c1[2],c2[2],t))})`;
    const BG_D=hex('#0D1015'), BG_L=hex('#F4F5F1');
    const TX_D=hex('#3A4250'), TX_L=hex('#B9BDB4');
    let W,H,parts=[];
    const DIGITS='0123456789'.split('');
    function build(){
      const dpr=Math.min(devicePixelRatio||1,2);
      W=scene.clientWidth; H=scene.clientHeight;
      cv.width=W*dpr; cv.height=H*dpr; ctx.setTransform(dpr,0,0,dpr,0,0);
      parts=[];
      const cols=Math.max(4,Math.floor(W/64)), rows=Math.max(4,Math.floor(H/64));
      const gx=W/(cols+1), gy=H/(rows+1);
      const cells=[];
      for(let r=1;r<=rows;r++)for(let c=1;c<=cols;c++)cells.push([c*gx,r*gy]);
      for(let i=cells.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[cells[i],cells[j]]=[cells[j],cells[i]];}
      const n=Math.min(cells.length,220);
      for(let i=0;i<n;i++){
        parts.push({sx:Math.random()*W, sy:Math.random()*H, tx:cells[i][0], ty:cells[i][1],
          d:DIGITS[Math.floor(Math.random()*10)], r:(Math.random()-.5)*1.6, s:12+Math.random()*10,
          drift:Math.random()*Math.PI*2, amp:6+Math.random()*10, accent:Math.random()<.06});
      }
    }
    let prog=0; const t0=performance.now();
    const easeIO = t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;
    function draw(){
      const t=(performance.now()-t0)/1000;
      const e=easeIO(prog);
      ctx.clearRect(0,0,W,H);
      ctx.textAlign='center'; ctx.textBaseline='middle';
      for(const p of parts){
        const wob=1-e;
        const x=lerp(p.sx,p.tx,e)+Math.cos(t*.7+p.drift)*p.amp*wob;
        const y=lerp(p.sy,p.ty,e)+Math.sin(t*.9+p.drift)*p.amp*wob;
        ctx.save(); ctx.translate(x,y); ctx.rotate(p.r*(1-e));
        ctx.font=`${lerp(p.s,13,e)}px 'IBM Plex Mono', ui-monospace, monospace`;
        ctx.fillStyle=p.accent?'#2E5CFF':mix(TX_D,TX_L,e);
        ctx.globalAlpha=p.accent?.9:.85;
        ctx.fillText(p.d,0,0); ctx.restore();
      }
    }
    const clamp01=v=>Math.min(1,Math.max(0,v));
    if (reduce || !hasGsap) {
      prog=1; build(); draw();
      scene.style.background='#F4F5F1';
      if(hlA) hlA.style.display='none';
      if(hlB){ hlB.style.opacity=1; }
      document.documentElement.setAttribute('data-reduced','');
    } else {
      pinned=true;
      build();
      let rT; addEventListener('resize',()=>{clearTimeout(rT);rT=setTimeout(build,150);});
      gsap.ticker.add(draw);
      /* 130% pin: the first headline leaves while the second arrives, no empty screen in between */
      ScrollTrigger.create({
        trigger:scene, start:'top top', end:'+=130%', pin:true, scrub:.5,
        onUpdate(self){
          prog=self.progress;
          scene.style.background=mix(BG_D,BG_L,easeIO(prog));
          const a=1-clamp01((prog-.06)/.26);
          const b=clamp01((prog-.34)/.30);
          hlA.style.opacity=a; hlA.style.transform=`translateY(${(1-a)*-36}px)`;
          hlB.style.opacity=b; hlB.style.transform=`translateY(${(1-b)*36}px)`;
          if(cue) cue.classList.toggle('off',prog>.04);
        }
      });
    }
  }

  /* ── scroll reveals ── */
  const rvs=document.querySelectorAll('.rv');
  if(reduce){ rvs.forEach(el=>{el.style.opacity=1;el.style.transform='none';}); }
  else if(hasGsap && typeof ScrollTrigger!=='undefined'){
    document.querySelectorAll('.metrics .m').forEach((el,i)=>{ el.dataset.rvd=(i*0.08).toFixed(2); });
    rvs.forEach(el=>{
      gsap.fromTo(el,{opacity:0,y:26},{opacity:1,y:0,duration:.8,ease:'power3.out',
        delay:parseFloat(el.dataset.rvd||0),
        scrollTrigger:{trigger:el,start:'top 87%'}});
    });
  } else {
    const io=new IntersectionObserver(es=>{es.forEach(en=>{if(en.isIntersecting){en.target.style.transition='opacity .7s,transform .7s';en.target.style.opacity=1;en.target.style.transform='none';io.unobserve(en.target);}});},{threshold:.12});
    rvs.forEach(el=>io.observe(el));
  }

  /* ── nav scrolled state (waits for the pinned hero to lighten) ── */
  const navEl=document.querySelector('.nav');
  if(navEl){
    const onScroll=()=>{
      const th=pinned ? innerHeight*0.72 : 40;
      navEl.classList.toggle('scrolled', (scrollY||pageYOffset)>th);
    };
    onScroll(); addEventListener('scroll',onScroll,{passive:true});
  }

  /* ── detail overlay (works + systems) ── */
  const overlay=document.getElementById('overlay');
  if(overlay){
    const sheet=overlay.querySelector('.sheet');
    const cases=document.getElementById('case-data');
    const prods=document.getElementById('product-data');
    let lastFocus=null, sheetShots=[], sheetIndex=0;
    const ICO_P='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 6l-6 6 6 6"/></svg>';
    const ICO_N='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg>';
    function wireSheet(){
      sheet.querySelectorAll('a.waorder').forEach(a=>{
        a.href=WA+'?text='+encodeURIComponent(a.getAttribute('data-msg')||'');
      });
      const gal=sheet.querySelector('.cgallery');
      const main=sheet.querySelector('.cg-main');
      if(!gal||!main) return;
      main.loading='eager';
      const thumbs=[...sheet.querySelectorAll('.cg-th')];
      sheetShots=thumbs.length?thumbs.map(t=>t.getAttribute('data-full')):[main.getAttribute('src')];
      let i=Math.max(0,thumbs.findIndex(t=>t.classList.contains('on')));
      if(i<0) i=0;
      function show(n){
        i=(n+sheetShots.length)%sheetShots.length;
        main.src=sheetShots[i];
        thumbs.forEach((x,k)=>x.classList.toggle('on',k===i));
        const c=gal.querySelector('.cg-count');
        if(c) c.textContent=(i+1)+' / '+sheetShots.length;
        sheetIndex=i;
      }
      thumbs.forEach((t,k)=>t.addEventListener('click',()=>show(k)));
      if(sheetShots.length>1){
        const stage=document.createElement('div');
        stage.className='cg-stage';
        main.parentNode.insertBefore(stage,main); stage.appendChild(main);
        const prev=document.createElement('button'); prev.type='button'; prev.className='cg-nav cg-prev'; prev.innerHTML=ICO_P; prev.setAttribute('aria-label',T.prev);
        const next=document.createElement('button'); next.type='button'; next.className='cg-nav cg-next'; next.innerHTML=ICO_N; next.setAttribute('aria-label',T.next);
        const cnt=document.createElement('span'); cnt.className='cg-count num';
        stage.appendChild(prev); stage.appendChild(next); stage.appendChild(cnt);
        prev.addEventListener('click',e=>{e.stopPropagation();show(i-1);});
        next.addEventListener('click',e=>{e.stopPropagation();show(i+1);});
      }
      show(i);
    }
    function openDetail(src){
      if(!src) return;
      sheet.scrollTop=0;
      sheet.innerHTML='<button class="close" type="button">'+T.close+'</button>'+src.innerHTML;
      overlay.classList.add('open');
      document.body.style.overflow='hidden';
      lastFocus=document.activeElement;
      sheet.querySelector('.close').focus();
      wireSheet();
      if(!reduce && hasGsap){
        gsap.fromTo(overlay.querySelector('.backdrop'),{opacity:0},{opacity:1,duration:.35,ease:'power2.out'});
        gsap.fromTo(sheet,{xPercent:rtl?-8:8,opacity:0},{xPercent:0,opacity:1,duration:.45,ease:'power3.out'});
      }
    }
    function closeDetail(){
      const done=()=>{
        overlay.classList.remove('open');
        document.body.style.overflow='';
        if(lastFocus) lastFocus.focus();
      };
      if(!reduce && hasGsap){
        gsap.to(overlay.querySelector('.backdrop'),{opacity:0,duration:.25,ease:'power2.in'});
        gsap.to(sheet,{xPercent:rtl?-6:6,opacity:0,duration:.28,ease:'power2.in',onComplete:done});
      } else done();
    }
    const keyOpen=(el,fn)=>el.addEventListener('keydown',e=>{ if(e.target!==el) return; if(e.key==='Enter'||e.key===' '){ e.preventDefault(); fn(); } });
    document.querySelectorAll('[data-open-case]').forEach(b=>{
      const fn=()=>openDetail(cases && cases.querySelector('[data-case="'+b.dataset.openCase+'"]'));
      b.addEventListener('click',fn); keyOpen(b,fn);
    });
    document.querySelectorAll('[data-open-prod]').forEach(card=>{
      const id=card.getAttribute('data-open-prod');
      const open=()=>openDetail(prods && prods.querySelector('[data-prod="'+id+'"]'));
      card.addEventListener('click',e=>{ if(e.target.closest('a')) return; open(); });
      keyOpen(card,open);
    });
    /* archive rows -> same detail sheet (text-only when no screenshots exist) */
    document.querySelectorAll('.arow').forEach(row=>{
      const head=row.querySelector('.arow-head'); if(!head) return;
      const cid=row.getAttribute('data-case');
      head.addEventListener('click',()=>{
        if(cid && cases && cases.querySelector('[data-case="'+cid+'"]')){
          openDetail(cases.querySelector('[data-case="'+cid+'"]')); return;
        }
        const title=(head.querySelector('.t')||{}).textContent||'';
        const cat=(head.querySelector('.cat')||{}).textContent||'';
        const stat=(head.querySelector('.stat')||{}).textContent||'';
        const pad=row.querySelector('.arow-pad');
        const parts=pad?[...pad.querySelectorAll('.part')].map(x=>x.outerHTML).join(''):'';
        const q=pad?pad.querySelector('.quote'):null;
        const sector=q?q.childNodes[0].textContent.trim():'';
        const tmp=document.createElement('div');
        tmp.innerHTML='<span class="cat-tag">'+cat+(stat?' · '+stat:'')+'</span>'+
          '<h3>'+title+'</h3>'+
          (sector?'<p class="sector">'+sector+'</p>':'')+
          parts+
          '<a class="ask waorder" data-msg="'+T.similarMsg+'" target="_blank" rel="noopener">'+T.similar+'</a>';
        openDetail(tmp);
      });
    });
    overlay.addEventListener('click',e=>{
      if(e.target.classList.contains('backdrop')||e.target.classList.contains('close')) closeDetail();
    });
    addEventListener('keydown',e=>{ if(e.key==='Escape'&&overlay.classList.contains('open')&&!document.querySelector('.lightbox.open')) closeDetail(); });
  }

  /* ── full-image lightbox ── */
  const lb=document.createElement('div');
  lb.className='lightbox';
  lb.innerHTML='<button class="lb-close" type="button" aria-label="'+T.close+'">✕</button><button class="lb-nav lb-prev" type="button" aria-label="'+T.prev+'"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 6l-6 6 6 6"/></svg></button><img alt=""><button class="lb-nav lb-next" type="button" aria-label="'+T.next+'"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg></button><div class="lb-hint">'+T.lbHint+'</div>';
  document.body.appendChild(lb);
  const lbImg=lb.querySelector('img');
  function openLB(src,alt){
    lbImg.src=src; lbImg.alt=alt||'';
    lb.classList.add('open');
    if(!reduce&&hasGsap){
      gsap.fromTo(lb,{opacity:0},{opacity:1,duration:.22,ease:'power2.out'});
      gsap.fromTo(lbImg,{scale:.94},{scale:1,duration:.3,ease:'power3.out'});
    }
  }
  function closeLB(){
    if(!reduce&&hasGsap){
      gsap.to(lb,{opacity:0,duration:.18,ease:'power2.in',onComplete:()=>{lb.classList.remove('open');gsap.set(lb,{opacity:1});}});
    } else lb.classList.remove('open');
  }
  const lbPrev=lb.querySelector('.lb-prev'), lbNext=lb.querySelector('.lb-next');
  let lbList=[], lbIdx=0;
  function lbShow(n){
    if(!lbList.length) return;
    lbIdx=(n+lbList.length)%lbList.length;
    lbImg.src=lbList[lbIdx];
    const multi=lbList.length>1;
    lbPrev.style.display=multi?'grid':'none';
    lbNext.style.display=multi?'grid':'none';
  }
  lbPrev.addEventListener('click',e=>{e.stopPropagation();lbShow(lbIdx-1);});
  lbNext.addEventListener('click',e=>{e.stopPropagation();lbShow(lbIdx+1);});
  lb.addEventListener('click',e=>{ if(e.target===lbImg||e.target.closest('.lb-nav')) return; closeLB(); });
  document.addEventListener('click',e=>{
    const im=e.target.closest('.sheet .cg-main');
    if(!im) return;
    const ths=[...document.querySelectorAll('.sheet .cg-th')];
    lbList=ths.length?ths.map(t=>t.getAttribute('data-full')):[im.src];
    let k=ths.findIndex(t=>t.classList.contains('on')); if(k<0) k=0;
    openLB(im.src,im.alt);
    lbShow(k);
  });
  addEventListener('keydown',e=>{
    if(!lb.classList.contains('open')) return;
    if(e.key==='Escape') closeLB();
    else if(e.key==='ArrowLeft') lbShow(lbIdx+ (rtl?-1:1));
    else if(e.key==='ArrowRight') lbShow(lbIdx+ (rtl?1:-1));
  });

  /* ── archive filters ── */
  const filterBtns=document.querySelectorAll('.filters button');
  if(filterBtns.length){
    filterBtns.forEach(btn=>{
      btn.addEventListener('click',()=>{
        filterBtns.forEach(b=>b.classList.remove('on'));
        btn.classList.add('on');
        const f=btn.dataset.filter;
        document.querySelectorAll('.arow').forEach(r=>{
          r.classList.toggle('hide', f!=='all' && r.dataset.cat!==f);
        });
      });
    });
  }

  /* ── archive thumbnails by category ── */
  const CATIMG={dash:'/img/thumb-dash.svg',sys:'/img/thumb-sys.svg',rep:'/img/thumb-rep.svg',study:'/img/thumb-study.svg',auto:'/img/thumb-auto.svg'};
  document.querySelectorAll('.arow').forEach(row=>{
    const head=row.querySelector('.arow-head'); if(!head) return;
    const t=head.querySelector('.t'); if(!t||head.querySelector('.arow-thumb')) return;
    const cat=row.getAttribute('data-cat')||'dash';
    const cid=row.getAttribute('data-case');
    const cimg=cid&&document.querySelector('#case-data [data-case="'+cid+'"] .cg-main');
    const thumb=document.createElement('span'); thumb.className='arow-thumb';
    thumb.style.backgroundImage='url('+(cimg?cimg.getAttribute('src'):(CATIMG[cat]||CATIMG.dash))+')';
    const main=document.createElement('span'); main.className='arow-main';
    head.insertBefore(main,t); main.appendChild(thumb); main.appendChild(t);
  });

  /* ── mobile menu ── */
  const burger=document.querySelector('.burger');
  const mmenu=document.querySelector('.mmenu');
  if(burger&&mmenu){
    burger.addEventListener('click',()=>{mmenu.classList.add('open'); mmenu.querySelector('.close').focus();});
    mmenu.addEventListener('click',e=>{
      if(e.target.tagName==='A'||e.target.classList.contains('close')){ mmenu.classList.remove('open'); burger.focus(); }
    });
    addEventListener('keydown',e=>{ if(e.key==='Escape'&&mmenu.classList.contains('open')){ mmenu.classList.remove('open'); burger.focus(); } });
  }

  /* ── marquee duplication ── */
  document.querySelectorAll('.marquee').forEach(mq=>{
    if(reduce) return;
    mq.innerHTML+=mq.innerHTML;
  });

  /* ── contact form → WhatsApp (default) or email ── */
  const form=document.getElementById('contact-form');
  if(form){
    const compose=()=>{
      const name=form.querySelector('[name=name]').value.trim();
      const biz=form.querySelector('[name=biz]').value.trim();
      const msg=form.querySelector('[name=msg]').value.trim();
      return `${T.formIntro}\n${T.name}: ${name}\n${T.biz}: ${biz}\n${T.sit}: ${msg}`;
    };
    form.addEventListener('submit',e=>{
      e.preventDefault();
      window.open(WA+'?text='+encodeURIComponent(compose()),'_blank','noopener');
    });
    const mailBtn=form.querySelector('[data-mail]');
    if(mailBtn) mailBtn.addEventListener('click',()=>{
      if(!form.reportValidity()) return;
      location.href='mailto:'+mailBtn.getAttribute('data-mail')+'?subject='+encodeURIComponent(T.mailSubject)+'&body='+encodeURIComponent(compose());
    });
  }
})();
