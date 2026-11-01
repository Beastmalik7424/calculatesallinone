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
    if(!box||box.y+box.height>viewport.height)throw Error(path+" form is not fully visible in the first viewport at "+viewport.width+"px");
    for(const [id,value] of fields)await page.locator("#"+id).fill(value);
    await form.locator("button[type=submit]").click();
    const result=await page.locator("#extra-result").innerText();
    if(!result.includes(expected))throw Error(path+" wrong result at "+viewport.width+"px: "+result);
    if(errors.length)throw Error(path+" browser errors: "+errors.join("; "));
    console.log(path+" "+viewport.width+"px PASS: "+result);
   }

   const response=await page.goto(base+"/percentage-calculator/");
   if(!response||response.status()!==200)throw Error("Percentage calculator HTTP failure");
   const form=page.locator("#extra-calculator-form");
   const box=await form.boundingBox();
   if(!box||box.y+box.height>viewport.height)throw Error("Percentage form is not fully visible in the first viewport at "+viewport.width+"px");
   const mode=page.locator("#percentage-mode");
   const result=page.locator("#extra-result");
   const value=page.locator("#value");
   const total=page.locator("#total");
   await value.fill("25");await total.fill("200");await form.locator("button[type=submit]").click();
   if(!(await result.innerText()).includes("Answer: 50"))throw Error("Percentage-of mode should return 50");
   await mode.selectOption("share");
   if((await result.innerText()).trim()!=="")throw Error("Changing percentage mode must clear stale results");
   const shareLabels=await page.evaluate(()=>({part:document.querySelector('label[for="value"]').textContent.trim(),whole:document.querySelector('label[for="total"]').textContent.trim()}));
   if(shareLabels.part!=="Part"||shareLabels.whole!=="Whole")throw Error("Reverse-mode labels are incorrect: "+JSON.stringify(shareLabels));
   await value.fill("45");await total.fill("250");await form.locator("button[type=submit]").click();
   const share=await result.innerText();
   if(!share.includes("18%")||!share.includes("45 ÷ 250 × 100"))throw Error("Reverse percentage calculation failed: "+share);
   await total.fill("0");await form.locator("button[type=submit]").click();
   if(!(await result.innerText()).includes("whole amount cannot be zero"))throw Error("Reverse percentage must reject a zero whole amount");
   await mode.selectOption("change");
   if((await result.innerText()).trim()!=="")throw Error("Changing to percentage-change mode must clear stale results");
   const changeLabels=await page.evaluate(()=>({start:document.querySelector('label[for="value"]').textContent.trim(),end:document.querySelector('label[for="total"]').textContent.trim()}));
   if(changeLabels.start!=="Starting value"||changeLabels.end!=="New value")throw Error("Percentage-change labels are incorrect: "+JSON.stringify(changeLabels));
   await value.fill("80");await total.fill("100");await form.locator("button[type=submit]").click();
   const increase=await result.innerText();
   if(!increase.includes("Increase of 25%"))throw Error("80 to 100 should be a 25% increase: "+increase);
   await value.fill("100");await total.fill("80");await form.locator("button[type=submit]").click();
   const decrease=await result.innerText();
   if(!decrease.includes("Decrease of 20%"))throw Error("100 to 80 should be a 20% decrease: "+decrease);
   await value.fill("0");await total.fill("80");await form.locator("button[type=submit]").click();
   if(!(await result.innerText()).includes("starting value must be greater than zero"))throw Error("Percentage change must reject zero starting value");
   await value.fill("-50");await total.fill("-25");await form.locator("button[type=submit]").click();
   if(!(await result.innerText()).includes("starting value must be greater than zero"))throw Error("Percentage change must reject negative starting value");
   const layout=await page.evaluate(()=>{
    const f=document.querySelector("#extra-calculator-form");
    const button=f.querySelector("button");
    const controls=[...f.querySelectorAll("input,select")];
    const b=button.getBoundingClientRect();
    return {horizontal:document.documentElement.scrollWidth>innerWidth+2,
      buttonVisible:b.top<innerHeight&&b.bottom>0,
      controlsFit:controls.every(el=>{const r=el.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth+2;})};
   });
   if(layout.horizontal||!layout.buttonVisible||!layout.controlsFit||errors.length)throw Error("Percentage responsive failure at "+viewport.width+"px: "+JSON.stringify({layout,errors}));
   console.log("/percentage-calculator/ "+viewport.width+"px PASS: three modes, dynamic labels, validation and first-screen layout");
   await page.close();
  }

  for(const width of [320,360,390,1366]){
   const viewport={width,height:width<500?740:768};
   for(const path of ["/","/percentage-calculator/","/fraction-calculator/","/compound-interest-calculator/","/date-calculator/","/bmi-calculator/","/zakat-calculator/"]){
    const page=await browser.newPage({viewport});
    const response=await page.goto(base+path);
    if(!response||response.status()!==200)throw Error(path+" HTTP failure at "+width+"px");
    const sw=await page.evaluate(()=>document.documentElement.scrollWidth);
    if(sw>width+2)throw Error(path+" horizontal overflow at "+width+"px: "+sw);
    await page.close();
   }
   console.log(width+"px site overflow audit PASS");
  }

  for(const width of [320,360,390,1366]){
   const page=await browser.newPage({viewport:{width,height:width<500?740:768}});
   const errors=[];page.on("pageerror",e=>errors.push(e.message));
   page.on("console",msg=>{if(msg.type()==="error")errors.push(msg.text());});
   const response=await page.goto(base+"/emi-calculator/");
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
      badCard:cards.some(el=>{const box=el.getBoundingClientRect(),strong=el.querySelector("strong");return strong.scrollWidth>strong.clientWidth+2||strong.getBoundingClientRect().right>box.right+2;}),
      emi:document.querySelector("#emi-out").textContent};
   });
   if(result.horizontal||result.badCard||width<500&&!result.sideBySide||errors.length||result.emi.includes("NaN"))throw Error("EMI responsive failure "+width+": "+JSON.stringify({result,errors}));
   console.log("EMI responsive browser PASS "+width+"px",result.emi);
   await page.close();
  }
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
