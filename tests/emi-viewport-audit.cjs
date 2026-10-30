const { chromium } = require('playwright');
(async () => {
 const browser = await chromium.launch({headless:true,args:['--no-sandbox']});
 const failures=[];
 for (const size of [{width:320,height:568},{width:360,height:740},{width:390,height:844},{width:1366,height:768}]) {
  const page=await browser.newPage({viewport:size,deviceScaleFactor:1});
  const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  await page.goto('http://127.0.0.1:8123/emi-calculator/',{waitUntil:'load'});
  await page.locator('#amount').fill('895842100');
  await page.locator('#rate').fill('12');
  await page.locator('#tenure').fill('5');
  await page.locator('#loan-form button[type=submit]').click();
  const d=await page.evaluate(()=>{
   const q=s=>document.querySelector(s).getBoundingClientRect();
   const cards=[...document.querySelectorAll('.metric')].map(el=>{const r=el.getBoundingClientRect();const value=el.querySelector('strong').getBoundingClientRect();return {label:el.querySelector('span').textContent,cardWidth:r.width,valueWidth:value.width,valueScroll:el.querySelector('strong').scrollWidth,cardRight:r.right,valueRight:value.right,cardBottom:r.bottom}});
   return {overflow:document.documentElement.scrollWidth>innerWidth+2,formColumns:getComputedStyle(document.querySelector('#loan-form>.grid')).gridTemplateColumns,amount:q('#amount'),rate:q('#rate'),metrics:cards,values:[...document.querySelectorAll('.metric strong')].map(x=>x.textContent),submit:q('#loan-form button[type=submit]')};
  });
  console.log('EMI viewport',size,JSON.stringify({overflow:d.overflow,columns:d.formColumns,metrics:d.metrics,values:d.values,submitBottom:d.submit.bottom,viewport:size.height,errors}));
  if(d.overflow)failures.push(size.width+' horizontal page overflow');
  if(size.width<=390 && d.amount.right>d.rate.left)failures.push(size.width+' form fields not in two columns');
  if(d.metrics.some(x=>x.valueScroll>x.valueWidth+2||x.valueRight>x.cardRight+2))failures.push(size.width+' metric content overflows card');
  if(!d.values[0].includes('1,99,27,512')||!d.values[2].includes('1,19,56,50,763'))failures.push(size.width+' EMI output unexpected');
  if(errors.length)failures.push(size.width+' JS errors '+errors.join(';'));
  await page.screenshot({path:'/tmp/emi-'+size.width+'.png',fullPage:true});
  await page.close();
 }
 await browser.close();
 if(failures.length){console.error('EMI VIEWPORT FAILURES:',failures.join('; '));process.exitCode=1;}
 else console.log('EMI viewport/browser checks PASS (does not claim entire page fits one screen)');
})().catch(e=>{console.error(e);process.exitCode=1});
