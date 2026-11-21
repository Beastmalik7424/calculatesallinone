const { chromium } = require('playwright');
let browser;
(async () => {
 browser = await chromium.launch({headless:true,args:['--no-sandbox']});
// This task changes the shared navigation on the English and Urdu Zakat pages. Other routes retain their existing build and dedicated browser regression suites.
 const slugs=['zakat-calculator','ur/zakat-calculator'];
 let failures=[];
 for (const size of [{width:320,height:568},{width:390,height:844},{width:360,height:740},{width:1366,height:768}]) {
  const page=await browser.newPage({viewport:size,deviceScaleFactor:1});
  for (const slug of slugs) {
   await page.goto('http://127.0.0.1:8123/'+slug+'/',{waitUntil:'load'});
   await page.waitForFunction(() => !!document.querySelector('#zakat-form'), null, {timeout:10000});
   const zakatFormContract = await page.evaluate(() => ({
    next: !!document.querySelector('#zakat-next'),
    back: !!document.querySelector('#zakat-back'),
    progress: !!document.querySelector('#zakat-step-progress'),
    submit: !!document.querySelector('#zakat-submit'),
    fields: [...document.querySelectorAll('#zakat-form input, #zakat-form select, #zakat-form textarea')].filter(e => !e.closest('[hidden]')).length
   }));
   if(zakatFormContract.next || zakatFormContract.back || zakatFormContract.progress) failures.push(slug+' still exposes obsolete wizard navigation');
   if(!zakatFormContract.submit || zakatFormContract.fields < 5) failures.push(slug+' single-page calculator is missing its submit action or input fields');
   const data=await page.evaluate(()=>{
    const section=document.querySelector('#tool-calculator')
      || document.querySelector('#main .ca-home-calculator')
      || document.querySelector('#extra-calculator-form')
      || document.querySelector('#calculator')
      || document.querySelector('#loan-form')
      || document.querySelector('#main form')
      || document.querySelector('#main');
    const visible=(e)=>e && getComputedStyle(e).display!=='none' && getComputedStyle(e).visibility!=='hidden' && e.getBoundingClientRect().height>0;
    const buttons=section ? [...section.querySelectorAll('button,input[type="submit"]')].filter(e=>visible(e)&&!e.hasAttribute('data-share-result-for')) : [];
    const submit=section?.querySelector('button[type="submit"],input[type="submit"]');
    const last=visible(submit) ? submit : buttons[buttons.length-1];
    const r=last?.getBoundingClientRect();
    const mainNav=document.querySelector('header nav[aria-label="Main"]');
    const carousel=document.querySelector('.ca-calculator-carousel');
    const primary=carousel?.querySelector('[data-tool-set="primary"]');
    const shortcuts=primary?[...primary.querySelectorAll('[data-tool-shortcut]')]:[];
    const active=primary?.querySelector('a[aria-current="page"]');
    const carouselRect=carousel?.getBoundingClientRect();
    const headerRect=document.querySelector('header')?.getBoundingClientRect();
    const calculatorRect=document.querySelector('#tool-calculator')?.getBoundingClientRect();
    const formRect=document.querySelector('#zakat-form')?.getBoundingClientRect();
    const gridStyle=primary?getComputedStyle(primary):null;
     const activeShortcutIndex=shortcuts.indexOf(active);
     const activeRect=active?.getBoundingClientRect();
     const carouselBounds=carousel?.getBoundingClientRect();
     const activeShortcutVisible=!!activeRect&&!!carouselBounds&&activeRect.left>=carouselBounds.left-1&&activeRect.right<=carouselBounds.right+1&&activeRect.top>=carouselBounds.top-1&&activeRect.bottom<=carouselBounds.bottom+1;
     const allLinksVisible=shortcuts.length===17 && shortcuts.every(a=>{const s=getComputedStyle(a);return s.display!=='none'&&s.visibility!=='hidden'&&a.getBoundingClientRect().width>0&&a.getBoundingClientRect().height>=44;});
     const allLabelsFit=shortcuts.length===17 && shortcuts.every(a=>{const r=a.getBoundingClientRect();return !!a.dataset.shortLabel&&!!a.getAttribute('aria-label')&&!!a.title&&a.scrollWidth<=a.clientWidth+1&&r.height>=44;});
     const tickerScrollable=!!carousel && carousel.scrollWidth>carousel.clientWidth+1;
     const duplicateGroups=carousel?.querySelectorAll('[data-tool-set="duplicate"]').length||0;
    const zakatSubmit=document.querySelector('#zakat-submit');
    const submitPosition=zakatSubmit?getComputedStyle(zakatSubmit.parentElement).position:null;
    const activeZakatPanels=[...document.querySelectorAll('#zakat-form .zakat-section')].filter(visible);
     const firstField=activeZakatPanels.flatMap(panel=>[...panel.querySelectorAll('input:not([type="hidden"]),select,textarea')]).find(visible);
    const firstFieldRect=firstField?.getBoundingClientRect();
    const firstFieldVisible=!!firstFieldRect && firstFieldRect.top>=-1 && firstFieldRect.bottom<=innerHeight-1 && visible(firstField);
    const firstFieldReachable=!!firstFieldRect && (()=>{const hit=document.elementFromPoint(firstFieldRect.left+firstFieldRect.width/2,firstFieldRect.top+firstFieldRect.height/2);return !!hit&&(hit===firstField||firstField.contains(hit));})();
    const submitRect=zakatSubmit?.getBoundingClientRect();
    const submitVisible=!!submitRect && submitRect.top>=-1 && submitRect.bottom<=innerHeight-1 && visible(zakatSubmit);
    const submitReachable=!!submitRect && (()=>{const hit=document.elementFromPoint(submitRect.left+submitRect.width/2,submitRect.top+submitRect.height/2);return !!hit&&(hit===zakatSubmit||zakatSubmit.contains(hit));})();
    const shortcutHeights=shortcuts.map(a=>a.getBoundingClientRect().height);
    const minShortcutHeight=shortcutHeights.length?Math.min(...shortcutHeights):0;
    const numberInputHeights=[...document.querySelectorAll('#zakat-form input[type="number"]')].map(e=>parseFloat(getComputedStyle(e).height)||0);
    const minNumberInputHeight=numberInputHeights.length?Math.min(...numberInputHeights):0;
    const checkboxLabelHeights=[...document.querySelectorAll('#zakat-form label.flex')].filter(visible).map(e=>Math.max(e.getBoundingClientRect().height,parseFloat(getComputedStyle(e).minHeight)||0));
    const minCheckboxLabelHeight=checkboxLabelHeights.length?Math.min(...checkboxLabelHeights):0;
    const gridColumns=gridStyle?gridStyle.gridTemplateColumns.split(' ').length:0;
    return {lastButton:last?.textContent.trim()||last?.value,top:r?.top,bottom:r?.bottom,viewport:innerHeight,scrollY,overflow:document.documentElement.scrollWidth>innerWidth+2,mainNavFlexWrap:mainNav?getComputedStyle(mainNav).flexWrap:null,mainNavFlexDirection:mainNav?getComputedStyle(mainNav).flexDirection:null,carouselVisible:visible(carousel)&&carouselRect.width>0,carouselBottom:carouselRect?.bottom,calculatorTop:calculatorRect?.top,formTop:formRect?.top,carouselCount:shortcuts.length,allLinksVisible,allLabelsFit,tickerScrollable,duplicateGroups,activeShortcutVisible,activeShortcutIndex,submitPosition,gridColumns,activeHref:active?.getAttribute('href'),headerHeight:headerRect?.height,firstFieldVisible,firstFieldReachable,firstFieldRect:firstFieldRect?{top:firstFieldRect.top,bottom:firstFieldRect.bottom,height:firstFieldRect.height}:null,submitVisible,submitReachable,submitRect:submitRect?{top:submitRect.top,bottom:submitRect.bottom,height:submitRect.height}:null,minShortcutHeight,minNumberInputHeight,minCheckboxLabelHeight};
   });
   const key=slug+' '+size.width+'x'+size.height;
   console.log(key,JSON.stringify(data));
   if(data.overflow) {
    const offenders=await page.evaluate(()=>[...document.querySelectorAll('body *')].map(e=>{
     const r=e.getBoundingClientRect(),s=getComputedStyle(e);
     return {tag:e.tagName,id:e.id,cls:typeof e.className==='string'?e.className.slice(0,100):'',left:Math.round(r.left),right:Math.round(r.right),width:Math.round(r.width),scrollWidth:e.scrollWidth,clientWidth:e.clientWidth,overflowX:s.overflowX,text:(e.textContent||'').trim().replace(/\\s+/g,' ').slice(0,60)};
    }).filter(x=>x.right>innerWidth+2||x.left< -2||x.scrollWidth>x.clientWidth+2).sort((a,b)=>Math.max(b.right-innerWidth,-b.left,b.scrollWidth-b.clientWidth)-Math.max(a.right-innerWidth,-a.left,a.scrollWidth-a.clientWidth)).slice(0,30));
    const metrics=await page.evaluate(()=>({docWidth:document.documentElement.scrollWidth,bodyWidth:document.body.scrollWidth,scrollX:window.scrollX,viewportWidth:window.innerWidth}));
    console.log('OVERFLOW DIAGNOSTIC '+key,JSON.stringify({...metrics,offenders}));
    failures.push(key+' horizontal overflow');
   }
   const urduPage=slug.startsWith('ur/');
   const isZakat=slug.endsWith('zakat-calculator');
   if(isZakat){
    if(!data.carouselVisible||data.carouselCount!==17||!data.allLinksVisible||data.duplicateGroups!==1)failures.push(key+' calculator shortcuts must expose all 17 primary links and one moving duplicate group');
    if(!data.tickerScrollable)failures.push(key+' moving calculator ticker must have an overflow-sized track');
    if(!data.allLabelsFit)failures.push(key+' calculator shortcut labels are clipped or missing accessible names');
    if(!data.activeShortcutVisible||data.activeShortcutIndex!==0)failures.push(key+' current calculator shortcut must be first and visible in the navigation viewport');
    if(data.carouselBottom>205)failures.push(key+' calculator shortcut grid takes too much first-screen space');
    if(data.activeHref!=='/'+slug+'/')failures.push(key+' current calculator shortcut is not active: '+data.activeHref);
    if(data.calculatorTop>=size.height||data.formTop>=size.height)failures.push(key+' Zakat calculator form must begin on the first screen');
    if(!data.lastButton||data.bottom>size.height-8)failures.push(key+' Calculate Zakat action must be visible on the first screen');
    if(!data.firstFieldVisible||!data.firstFieldReachable)failures.push(key+' first Zakat input must be visible and reachable without scrolling');
    if(!data.submitVisible||!data.submitReachable)failures.push(key+' Calculate Zakat button must be visible and reachable without scrolling');
    if(data.scrollY!==0)failures.push(key+' page must remain at the initial scroll position');
     // One-page form: all applicable fields remain on one page; vertical scrolling is permitted on short screens.
    if(size.width<=600&&data.minShortcutHeight<44)failures.push(key+' calculator shortcut touch targets must be at least 44px high: '+data.minShortcutHeight);
    if(size.width<=600&&data.minCheckboxLabelHeight<44)failures.push(key+' Zakat checkbox rows must be at least 44px high: '+data.minCheckboxLabelHeight);
   }
   if(data.submitPosition==='sticky')failures.push(key+' Zakat submit button must not use sticky positioning');
   if(data.submitPosition==='fixed'&&data.submitRect&&data.submitRect.top<data.headerHeight)failures.push(key+' fixed Zakat submit button must remain below the header navigation');
   const screenshotSlug=slug.replaceAll('/','-');
   await page.screenshot({path:'/tmp/'+screenshotSlug+'-'+size.width+'.png',fullPage:false});
  }
  await page.close();
 }
 // Small-phone profit-only test and breadcrumb placement.
 for (const size of [{width:320,height:568},{width:375,height:667},{width:768,height:1024},{width:1366,height:768}]) {
  const small=await browser.newPage({viewport:size,deviceScaleFactor:1});
  await small.goto('http://127.0.0.1:8123/profit-loss-calculator/');
  const p=await small.evaluate(()=>{
   const button=document.querySelector('#pl-form button[type="submit"]').getBoundingClientRect();
   const breadcrumb=document.querySelector('#main nav[aria-label="Breadcrumb"]').getBoundingClientRect();
   const section=document.querySelector('#tool-calculator').getBoundingClientRect();
   return {buttonBottom:button.bottom,breadcrumbTop:breadcrumb.top,sectionBottom:section.bottom,overflow:document.documentElement.scrollWidth>innerWidth+2,wide:[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth+2).slice(0,8).map(e=>({tag:e.tagName,id:e.id,cls:String(e.className).slice(0,70),right:Math.round(e.getBoundingClientRect().right)}))};
  });
  console.log('profit-small '+size.width+'x'+size.height,JSON.stringify(p));
  if(p.buttonBottom>size.height-8||p.overflow)failures.push('profit first-screen failed '+size.width+'x'+size.height);
  if(p.breadcrumbTop<p.sectionBottom)failures.push('profit breadcrumb not below tool');
  await small.screenshot({path:'/tmp/profit-loss-calculator-'+size.width+'.png',fullPage:false});
  await small.close();
 }
 const page=await browser.newPage();
 await page.goto('http://127.0.0.1:8123/profit-loss-calculator/');
 await page.locator('#p-revenue').fill('1000');
 await page.locator('#p-cogs').fill('600');
 await page.locator('#p-expenses').fill('150');
 await page.locator('#pl-form button[type="submit"]').click();
 let result=await page.locator('#pl-result').innerText();
 if(!result.includes('250')||!result.includes('25.00%'))failures.push('business P&L result: '+result);
 await page.locator('input[name="pl-mode"][value="product"]').check();
 if(await page.locator('#pl-business-fields').isVisible())failures.push('business fields visible in product mode');
 await page.locator('#p-cost').fill('80');
 await page.locator('#p-sell').fill('100');
 await page.locator('#pl-form button[type="submit"]').click();
 result=await page.locator('#pl-result').innerText();
 if(!result.includes('20')||!result.includes('25.00'))failures.push('product markup result: '+result);
 // Product gross margin is based on selling price, not cost.
 await page.locator('#p-cost').fill('40');
 await page.locator('#p-sell').fill('50');
 await page.locator('#pl-form button[type="submit"]').click();
 result=await page.locator('#pl-result').innerText();
 if(!result.includes('Profit: 10')||!result.includes('25.00 percent of cost price')||!result.includes('Margin on selling price: 20.00%'))failures.push('product gross margin result: '+result);
 // Zero cost: markup is unavailable, but gross margin remains 100% when selling price is positive.
 await page.locator('#p-cost').fill('0');
 await page.locator('#p-sell').fill('10');
 await page.locator('#pl-form button[type="submit"]').click();
 result=await page.locator('#pl-result').innerText();
 if(!result.includes('Markup is N/A because cost price is zero.')||!result.includes('Margin on selling price: 100.00%'))failures.push('zero-cost markup/margin result: '+result);
 // Zero selling price: margin is unavailable because its denominator is zero.
 await page.locator('#p-cost').fill('10');
 await page.locator('#p-sell').fill('0');
 await page.locator('#pl-form button[type="submit"]').click();
 result=await page.locator('#pl-result').innerText();
 if(!result.includes('Loss: 10')||!result.includes('Margin on selling price: N/A'))failures.push('zero-selling-price result: '+result);
 await page.locator('#p-cost').fill('-1');
 await page.locator('#p-sell').fill('100');
 await page.locator('#pl-form button[type="submit"]').click();
 result=await page.locator('#pl-result').innerText();
 if(!result.includes('Enter a cost price and a selling price of zero or more.'))failures.push('negative cost validation: '+result);

 // Homepage Standard Calculator: actual no-scroll viewport and click checks.
 for (const size of [{width:320,height:568},{width:375,height:667},{width:390,height:844},{width:1024,height:768},{width:1366,height:768}]) {
  const home=await browser.newPage({viewport:size,deviceScaleFactor:1});
  await home.goto('http://127.0.0.1:8123/',{waitUntil:'load'});
  const h=await home.evaluate(()=>{
   const pad=document.querySelector('.ca-home-calculator #calc-pad');
   const display=document.querySelector('.ca-home-calculator #calc-display');
   const buttons=pad?[...pad.querySelectorAll('button')].filter(b=>b.getBoundingClientRect().height>0):[];
   const rect=buttons.length?buttons[buttons.length-1].getBoundingClientRect():null;
   const heading=document.querySelector('.ca-home-header h1');
   const headingStyle=heading?getComputedStyle(heading):null;
   const rootFontSize=parseFloat(getComputedStyle(document.documentElement).fontSize);
   const buttonHeights=buttons.map(b=>b.getBoundingClientRect().height);
   const media=[...document.querySelectorAll('.ca-home-wrap img,.ca-home-wrap video,.ca-home-tools img')].filter(e=>e.getBoundingClientRect().width>innerWidth+2);
   return {buttons:buttons.length,display:!!display,lastButtonBottom:rect?.bottom,viewport:innerHeight,headingFontSize:headingStyle?parseFloat(headingStyle.fontSize):null,rootFontSize,minKeyHeight:buttonHeights.length?Math.min(...buttonHeights):0,overflow:document.documentElement.scrollWidth>innerWidth+2,oversizedMedia:media.length};
  });
  console.log('homepage '+size.width+'x'+size.height,JSON.stringify(h));
  if(!h.display||h.buttons<10)failures.push('homepage calculator missing '+size.width);
  if(size.width<=600 && h.headingFontSize>h.rootFontSize*1.05)failures.push('homepage mobile heading was not reduced relative to the user text scale: '+h.headingFontSize+'px');
  if(h.minKeyHeight<44)failures.push('homepage calculator keypad touch target shrank below 44px: '+h.minKeyHeight);
  if(h.lastButtonBottom>size.height-8)failures.push('homepage scroll required '+size.width+'x'+size.height+' bottom='+h.lastButtonBottom);
  if(h.overflow||h.oversizedMedia)failures.push('homepage overflow '+size.width);
  if(h.buttons>=10) {
   for(const key of ['C','7','+','3','=']) {
    const button=home.locator('#calc-pad button[data-key="'+key+'"]');
    if(await button.count())await button.first().click();
    else failures.push('homepage key missing '+key);
   }
   const value=(await home.locator('#calc-display').innerText()).trim();
   console.log('homepage interaction '+size.width,JSON.stringify({value}));
   if(value!=='10')failures.push('homepage arithmetic failed '+size.width+': '+value);
  }
  await home.screenshot({path:'/tmp/homepage-'+size.width+'.png',fullPage:false});
  await home.close();
 }
 await browser.close();
 if(failures.length){console.error('VIEWPORT/INTERACTION FAILURES:',failures.join('; '));process.exitCode=1;}
 else console.log('All viewport and profit interaction checks PASS');
})().catch(async e=>{console.error(e);if(browser)await browser.close().catch(()=>{});process.exitCode=1;});