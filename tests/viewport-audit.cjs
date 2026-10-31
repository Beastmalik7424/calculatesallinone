const { chromium } = require('playwright');
(async () => {
 const browser = await chromium.launch({headless:true,args:['--no-sandbox']});
 const slugs=['zakat-calculator','bmi-calculator','profit-loss-calculator','discount-calculator','age-calculator','unit-converter','stopwatch','emi-calculator','standard-calculator','tasbih-counter','years-to-days-calculator','query-calculator','percentage-calculator','fraction-calculator','compound-interest-calculator','date-calculator','ur/age-calculator','ur/bmi-calculator','ur/discount-calculator','ur/profit-loss-calculator','ur/standard-calculator','ur/stopwatch','ur/tasbih-counter','ur/unit-converter','ur/zakat-calculator'];
 let failures=[];
 for (const size of [{width:320,height:568},{width:390,height:844},{width:360,height:740},{width:1366,height:768}]) {
  const page=await browser.newPage({viewport:size,deviceScaleFactor:1});
  for (const slug of slugs) {
   await page.goto('http://127.0.0.1:8123/'+slug+'/',{waitUntil:'load'});
   const data=await page.evaluate(()=>{
    const section=document.querySelector('#tool-calculator');
    const visible=(e)=>e && getComputedStyle(e).display!=='none' && e.getBoundingClientRect().height>0;
    const buttons=[...section.querySelectorAll('button')].filter(visible);
    const last=buttons[buttons.length-1];
    const r=last?.getBoundingClientRect();
    return {lastButton:last?.textContent.trim(),top:r?.top,bottom:r?.bottom,viewport:innerHeight,overflow:document.documentElement.scrollWidth>innerWidth+2};
   });
   const key=slug+' '+size.width+'x'+size.height;
   console.log(key,JSON.stringify(data));
   if(data.overflow)failures.push(key+' horizontal overflow');
   if(!data.lastButton||data.bottom>size.height-8)failures.push(key+' primary button below fold');
   await page.screenshot({path:'/tmp/'+slug+'-'+size.width+'.png',fullPage:false});
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
   const media=[...document.querySelectorAll('.ca-home-wrap img,.ca-home-wrap video,.ca-home-tools img')].filter(e=>e.getBoundingClientRect().width>innerWidth+2);
   return {buttons:buttons.length,display:!!display,lastButtonBottom:rect?.bottom,viewport:innerHeight,overflow:document.documentElement.scrollWidth>innerWidth+2,oversizedMedia:media.length};
  });
  console.log('homepage '+size.width+'x'+size.height,JSON.stringify(h));
  if(!h.display||h.buttons<10)failures.push('homepage calculator missing '+size.width);
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
})().catch(e=>{console.error(e);process.exitCode=1});