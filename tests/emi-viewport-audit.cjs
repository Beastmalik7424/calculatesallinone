const { chromium } = require('playwright');
function isExpectedGooglePreferredSourceReportOnlyNotice(text) {
 return text.startsWith('Framing \'https://news.google.com/\' violates the following report-only Content Security Policy directive: "frame-ancestors \'self\'".') && text.includes("The violation has been logged, but no further action has been taken.");
}
const BASE_URL = (process.env.BASE_URL || 'http://127.0.0.1:4174').replace(/\/+$/, '');
(async () => {
 const browser = await chromium.launch({headless:true,args:['--no-sandbox']});
 const failures=[];
 for (const size of [{width:320,height:568},{width:360,height:740},{width:390,height:844},{width:1366,height:768}]) {
  const page=await browser.newPage({viewport:size,deviceScaleFactor:1});
  const errors=[];
  page.on('pageerror',e=>errors.push(String(e)));
  page.on('console',msg=>{if(msg.type()==='error'&&!isExpectedGooglePreferredSourceReportOnlyNotice(msg.text()))errors.push('console: '+msg.text());});
  const response=await page.goto(BASE_URL+'/emi-calculator/',{waitUntil:'load'});
  if(!response||response.status()!==200)throw Error('EMI page HTTP failure at '+size.width+'px');
  const submitLocator=page.locator('#loan-form button[type=submit]');
  const submitBefore=await submitLocator.boundingBox();
  if((size.width===390||size.width===1366)&&(!submitBefore||submitBefore.y<0||submitBefore.y+submitBefore.height>size.height))failures.push(size.width+' Calculate button is not fully visible before scrolling');
  await page.locator('#amount').fill('500000');
  await page.locator('#rate').fill('12');
  await page.locator('#tenure').fill('5');
  await submitLocator.click();
  const d=await page.evaluate(()=>{
   const q=s=>document.querySelector(s).getBoundingClientRect();
   const cards=[...document.querySelectorAll('.metric')].map(el=>{const r=el.getBoundingClientRect();const value=el.querySelector('strong').getBoundingClientRect();return {label:el.querySelector('span').textContent,cardWidth:r.width,valueWidth:value.width,valueScroll:el.querySelector('strong').scrollWidth,cardRight:r.right,valueRight:value.right,cardBottom:r.bottom}});
   const metricsBox=q('#metrics');
   const firstValue=q('#metrics .metric:first-child strong');
   return {overflow:document.documentElement.scrollWidth>innerWidth+2,formColumns:getComputedStyle(document.querySelector('#loan-form>.grid')).gridTemplateColumns,amount:q('#amount'),rate:q('#rate'),metrics:cards,values:[...document.querySelectorAll('.metric strong')].map(x=>x.textContent),submit:q('#loan-form button[type=submit]'),metricsBox,firstValue,metricsDisplay:getComputedStyle(document.querySelector('#metrics')).display};
  });
  console.log('EMI viewport',size,JSON.stringify({overflow:d.overflow,columns:d.formColumns,metrics:d.metrics,values:d.values,submitBottom:d.submit.bottom,metricsTop:d.metricsBox.top,firstValueTop:d.firstValue.top,firstValueBottom:d.firstValue.bottom,viewport:size.height,errors}));
  if(d.overflow)failures.push(size.width+' horizontal page overflow');
  if((size.width===390||size.width===1366)&&(d.submit.top<0||d.submit.bottom>size.height))failures.push(size.width+' Calculate button is not fully visible in the first viewport');
  if(d.metricsBox.width<=0||d.metricsBox.height<=0||d.metricsDisplay==='none')failures.push(size.width+' calculated result metrics are not visible after submission');
  if(size.width===390&&(d.firstValue.top<0||d.firstValue.bottom>size.height))failures.push(size.width+' first calculated EMI value is not visible in the first viewport after submission');
  if(size.width<=390 && d.amount.right>d.rate.left)failures.push(size.width+' form fields not in two columns');
  if(d.metrics.some(x=>x.valueScroll>x.valueWidth+2||x.valueRight>x.cardRight+2))failures.push(size.width+' metric content overflows card');
  if(d.values.some(v=>v.includes('NaN')||v.includes('Infinity'))||d.values[0].includes('0.00'))failures.push(size.width+' EMI output invalid');
  if(errors.length)failures.push(size.width+' JS errors '+errors.join(';'));
  await page.screenshot({path:'/tmp/emi-'+size.width+'.png',fullPage:true});
  await page.close();
 }
 await browser.close();
 if(failures.length){console.error('EMI VIEWPORT FAILURES:',failures.join('; '));process.exitCode=1;}
 else console.log('EMI viewport/browser checks PASS: first result visible at 390x844; Calculate action visible at 390x844 and 1366x768; valid metrics at all widths');
})().catch(e=>{console.error(e);process.exitCode=1});
