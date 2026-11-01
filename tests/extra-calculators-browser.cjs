"use strict";
const {chromium}=require("playwright");
(async()=>{
 const browser=await chromium.launch({headless:true,args:["--no-sandbox"]});
 const base="http://127.0.0.1:4174";
 const viewports=[{width:390,height:844},{width:1366,height:768}];
 try{
  for(const viewport of viewports){
   const page=await browser.newPage({viewport});
   const errors=[];
   page.on("pageerror",e=>errors.push(e.message));
   page.on("console",msg=>{if(msg.type()==="error")errors.push(msg.text());});
   for(const [path,fields,expected] of [
    ["/fraction-calculator/",[["a","1"],["b","2"],["c","1"],["d","3"]],"5/6"],
    ["/compound-interest-calculator/",[["principal","1000"],["rate","10"],["years","1"],["frequency","2"]],"1,102.50"],
    ["/date-calculator/",[["start","2024-02-28"],["end","2024-03-01"]],"2 days"]
   ]){
    const response=await page.goto(base+path);
    if(!response||response.status()!==200)throw Error(path+" HTTP failure at "+viewport.width+"px");
    const form=page.locator("#extra-calculator-form");
    const box=await form.boundingBox();
    if(!box||box.y+box.height>viewport.height)throw Error(path+" calculator form is not fully visible in the first viewport at "+viewport.width+"px");
    for(const [id,value] of fields){const el=page.locator("#"+id);if(await el.count())await el.fill(value);}
    await form.locator("button[type=submit]").click();
    const result=await page.locator("#extra-result").innerText();
    if(!result.includes(expected))throw Error(path+" wrong result at "+viewport.width+"px: "+result);
    if(errors.length)throw Error(path+" browser errors: "+errors.join("; "));
    console.log(path+" "+viewport.width+"px PASS: "+result);
   }

   const response=await page.goto(base+"/percentage-calculator/");
   if(!response||response.status()!==200)throw Error("percentage calculator HTTP failure");
   const form=page.locator("#extra-calculator-form");
   const box=await form.boundingBox();
   if(!box||box.y+box.height>viewport.height)throw Error("Percentage calculator form is not fully visible in the first viewport at "+viewport.width+"px");
   const mode=page.locator("#pct-mode");
   const result=page.locator("#extra-result");
   const value=page.locator("#value");
   const total=page.locator("#total");
   await value.fill("25");await total.fill("200");await form.locator("button[type=submit]").click();
   if(!(await result.innerText()).includes("50"))throw Error("Percentage-of mode should return 50");
   await mode.selectOption("whatpercent");
   if((await result.innerText()).trim()!=="")throw Error("Changing percentage mode must clear stale results");
   if(await page.locator('label[for="value"]').innerText()!=="First number (the part)")throw Error("Reverse mode first label is incorrect");
   if(await page.locator('label[for="total"]').innerText()!=="Second number (the whole)")throw Error("Reverse mode second label is incorrect");
   await value.fill("30");await total.fill("120");await form.locator("button[type=submit]").click();
   if(!(await result.innerText()).includes("30 is 25% of 120"))throw Error("Reverse percentage should return 25%");
   await total.fill("0");await form.locator("button[type=submit]").click();
   if(!(await result.innerText()).includes("whole amount cannot be zero"))throw Error("Reverse percentage must reject a zero whole amount");
   await mode.selectOption("change");
   if((await result.innerText()).trim()!=="")throw Error("Changing to percentage-change mode must clear stale results");
   if(await page.locator('label[for="value"]').innerText()!=="Starting value")throw Error("Percentage-change start label is incorrect");
   if(await page.locator('label[for="total"]').innerText()!=="New value")throw Error("Percentage-change end label is incorrect");
   await value.fill("80");await total.fill("100");await form.locator("button[type=submit]").click();
   if(!(await result.innerText()).includes("Increase of 25%"))throw Error("80 to 100 should be a 25% increase");
   await value.fill("100");await total.fill("80");await form.locator("button[type=submit]").click();
   if(!(await result.innerText()).includes("Decrease of 20%"))throw Error("100 to 80 should be a 20% decrease");
   await value.fill("0");await total.fill("100");await form.locator("button[type=submit]").click();
   if(!(await result.innerText()).includes("starting value must be greater than zero"))throw Error("Percentage change must reject a zero starting value");
   if(errors.length)throw Error("Percentage browser errors at "+viewport.width+"px: "+errors.join("; "));
   console.log("/percentage-calculator/ "+viewport.width+"px PASS: all three modes, validation, dynamic labels and stale-result clearing");
   await page.close();
  }

  for(const width of [320,390,1366]){
   for(const path of ["/","/percentage-calculator/","/fraction-calculator/","/compound-interest-calculator/","/date-calculator/","/bmi-calculator/","/zakat-calculator/"]){
    const page=await browser.newPage({viewport:{width,height:width===1366?768:844}});
    const response=await page.goto(base+path);
    if(!response||response.status()!==200)throw Error(path+" HTTP failure at "+width+"px");
    const sw=await page.evaluate(()=>document.documentElement.scrollWidth);
    if(sw>width)throw Error(path+" horizontal overflow at "+width+"px: "+sw);
    await page.close();
   }
   console.log(width+"px responsive overflow audit PASS");
  }
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
