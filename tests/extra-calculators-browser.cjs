"use strict";
const {chromium}=require("playwright");
(async()=>{
 const browser=await chromium.launch({headless:true,args:["--no-sandbox"]});
 try{
  const cases=[
   ["/percentage-calculator/",[["value","25"],["total","200"]],"50"],
   ["/fraction-calculator/",[["a","1"],["b","2"],["c","1"],["d","3"]],"5/6"],
   ["/compound-interest-calculator/",[["principal","1000"],["rate","10"],["years","1"],["frequency","2"]],"1,102.50"],
   ["/date-calculator/",[["start","2024-02-28"],["end","2024-03-01"]],"2 days"]
  ];
  for(const [path,fields,expected] of cases){
   const page=await browser.newPage({viewport:{width:390,height:844}});
   const errors=[];page.on("pageerror",e=>errors.push(e.message));
   const response=await page.goto("http://127.0.0.1:4174"+path);
   if(!response||response.status()!==200)throw Error(path+" HTTP failure");
   for(const [id,value] of fields)await page.locator("#"+id).fill(value);
   await page.locator("#extra-calculator-form button[type=submit]").click();
   const text=await page.locator("#extra-result").innerText();
   if(!text.includes(expected))throw Error(path+" wrong result: "+text);
   if(errors.length)throw Error(path+" browser errors: "+errors.join("; "));
   console.log(path+" interactive result PASS: "+text);
   await page.close();
  }

  for(const width of [320,360,390,1366]){
   const page=await browser.newPage({viewport:{width,height:width<500?740:768}});
   const errors=[];page.on("pageerror",e=>errors.push(e.message));
   const response=await page.goto("http://127.0.0.1:4174/emi-calculator/");
   if(!response||response.status()!==200)throw Error("EMI page HTTP failure");
   await page.locator("#amount").fill("895842100");
   await page.locator("#rate").fill("12");
   await page.locator("#tenure").fill("5");
   await page.locator("#loan-form button[type=submit]").click();
   const result=await page.evaluate(()=>{
    const a=document.querySelector("#amount").getBoundingClientRect();
    const b=document.querySelector("#rate").getBoundingClientRect();
    const cards=[...document.querySelectorAll(".metric")];
    return {horizontal:document.documentElement.scrollWidth>innerWidth+2,
     sideBySide:a.right<=b.left+2,
     badCard:cards.some(el=>{const box=el.getBoundingClientRect(),strong=el.querySelector("strong");return strong.scrollWidth>strong.clientWidth+2||strong.getBoundingClientRect().right>box.right+2}),
     emi:document.querySelector("#emi-out").textContent};
   });
   if(result.horizontal||result.badCard||width<500&&!result.sideBySide||errors.length||result.emi.includes("NaN"))throw Error("EMI responsive failure "+width+": "+JSON.stringify({result,errors}));
   console.log("EMI responsive browser PASS "+width+"px",result.emi);
   await page.screenshot({path:"/tmp/emi-"+width+".png",fullPage:true});
   await page.close();
  }
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
