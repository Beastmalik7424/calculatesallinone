"use strict";
const {chromium}=require("playwright");
(async()=>{
 const browser=await chromium.launch({headless:true,args:["--no-sandbox"]});
 try{
  const cases=[
   ["/percentage-calculator/",[["value","25"],["total","200"]],"50"],
   ["/fraction-calculator/",[["a","1"],["b","2"],["c","1"],["d","3"]],"5/6"],
   ["/compound-interest-calculator/",[["principal","1000"],["rate","10"],["years","1"],["frequency","2"]],"1,102.50"],
   ["/date-calculator/",[["start","2024-02-28"],["end","2024-03-01"]],"2 days"],
   ["/percentage-calculator/",[["pct-mode","whatpercent"],["value","30"],["total","120"]],"is 25% of 120"],
   ["/percentage-calculator/",[["pct-mode","change"],["value","100"],["total","80"]],"Decrease of 20%"]
  ];
  for(const [path,fields,expected] of cases){
   const page=await browser.newPage({viewport:{width:390,height:844}});
   const errors=[];page.on("pageerror",e=>errors.push(e.message));
   const response=await page.goto("http://127.0.0.1:4174"+path);
   if(!response||response.status()!==200)throw Error(path+" HTTP failure");
   for(const [id,value] of fields){const el=page.locator("#"+id);if(id==="pct-mode")await el.selectOption(value);else await el.fill(value);}
   await page.locator("#extra-calculator-form button[type=submit]").click();
   const text=await page.locator("#extra-result").innerText();
   if(!text.includes(expected))throw Error(path+" wrong result: "+text);
   if(errors.length)throw Error(path+" browser errors: "+errors.join("; "));
   console.log(path+" interactive result PASS: "+text);
   await page.close();
  }
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
