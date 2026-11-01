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
   const mode=page.locator("#percentage-mode");
   const result=page.locator("#extra-result");
   const value=page.locator("#value");
   const total=page.locator("#total");
   const defaultLabels=await page.evaluate(()=>({percentage:document.querySelector('label[for="value"]').textContent.trim(),number:document.querySelector('label[for="total"]').textContent.trim()}));
   if(defaultLabels.percentage!=="Percentage (%)"||defaultLabels.number!=="Number")throw Error("Default percentage labels are incorrect: "+JSON.stringify(defaultLabels));
   await value.fill("25");await total.fill("200");await form.locator("button[type=submit]").click();
   if(!(await result.innerText()).includes("Answer: 50"))throw Error("Default percentage mode should return 50");
   await mode.selectOption("share");
   if((await result.innerText()).trim()!=="")throw Error("Changing percentage mode must clear stale results");
   if(await page.locator('label[for="value"]').innerText()!=="Part")throw Error("Reverse mode first label is incorrect");
   if(await page.locator('label[for="total"]').innerText()!=="Whole")throw Error("Reverse mode second label is incorrect");
   await value.fill("45");await total.fill("250");await form.locator("button[type=submit]").click();
   if(!(await result.innerText()).includes("18%")||!(await result.innerText()).includes("45 ÷ 250 × 100"))throw Error("Reverse percentage should return 18%");
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

  for(const width of [390,1366]){
   const page=await browser.newPage({viewport:{width,height:width===390?844:768}});
   const errors=[];page.on("pageerror",e=>errors.push(e.message));
   page.on("console",msg=>{if(msg.type()==="error")errors.push(msg.text());});
   const response=await page.goto(base+"/bmi-calculator/");
   if(!response||response.status()!==200)throw Error("BMI page HTTP failure at "+width+"px");
   const form=page.locator("#bmi-form");
   const formBox=await form.boundingBox();
   const buttonBox=await form.locator('button[type="submit"]').boundingBox();
   if(!formBox||!buttonBox||formBox.y+formBox.height>(width===390?844:768))throw Error("BMI form not fully visible at "+width+"px");
   if(width===1366){
    const display=await form.evaluate(el=>getComputedStyle(el).display);
    if(display!=="grid")throw Error("BMI desktop form must use the two-column grid, got "+display);
   }
   await page.locator("#b-kg").fill("70");
   await page.locator("#b-cm").fill("170");
   await form.locator('button[type="submit"]').click();
   const metric=await page.locator("#bmi-result").innerText();
   if(!metric.includes("24.2"))throw Error("BMI metric result incorrect: "+metric);
   await page.locator("#bmi-weight-lb").check();
   await page.locator("#b-lb").fill("154.324");
   await page.locator("#bmi-height-ftin").check();
   await page.locator("#b-ft").fill("5");
   await page.locator("#b-in").fill("7");
   await form.locator('button[type="submit"]').click();
   const imperial=await page.locator("#bmi-result").innerText();
   if(!imperial.includes("24.2"))throw Error("BMI imperial result incorrect: "+imperial);
   const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2);
   if(overflow||errors.length)throw Error("BMI layout/browser failure at "+width+"px: "+JSON.stringify({overflow,errors}));
   console.log("BMI browser PASS "+width+"px: metric and imperial = 24.2, first-screen form aligned");
   await page.close();
  }

  for(const width of [390,1366]){
   const viewport={width,height:width===390?844:768};
   const page=await browser.newPage({viewport});
   const errors=[];page.on("pageerror",e=>errors.push(e.message));
   page.on("console",msg=>{if(msg.type()==="error")errors.push(msg.text());});
   page.on("dialog",dialog=>dialog.accept());
   const response=await page.goto(base+"/tasbih-counter/");
   if(!response||response.status()!==200)throw Error("Tasbih page HTTP failure at "+width+"px");
   const order=await page.evaluate(()=>{
    const rect=s=>{const r=document.querySelector(s).getBoundingClientRect();return {top:r.top,bottom:r.bottom};};
    return {count:rect("#t-count"),tap:rect("#t-tap"),actions:rect("#t-tap + .grid"),settings:rect(".ca-tasbih-settings"),phrase:rect("#t-phrase"),target:rect("#t-target"),undo:rect("#t-undo"),reset:rect("#t-reset"),overflow:document.documentElement.scrollWidth>innerWidth+2};
   });
   if(!(order.count.top<order.settings.top&&order.settings.top<order.tap.top&&order.tap.top<order.actions.top))throw Error("Tasbih count, phrase/target settings, tap and reset must follow the intended first-screen order at "+width+"px: "+JSON.stringify(order));
   if(order.settings.bottom>(width===390?844:768)||order.count.bottom>(width===390?844:768)||order.undo.bottom>(width===390?844:768)||order.reset.bottom>(width===390?844:768)||order.overflow)throw Error("Tasbih count, phrase/target and primary actions must fit the first viewport at "+width+"px: "+JSON.stringify(order));
   if(order.count.bottom>(width===390?844:768)||order.undo.bottom>(width===390?844:768)||order.reset.bottom>(width===390?844:768)||order.overflow)throw Error("Tasbih first-screen or overflow failure at "+width+"px: "+JSON.stringify(order));
   for(let i=0;i<33;i++)await page.locator("#t-tap").click();
   if((await page.locator("#t-count").innerText()).trim()!=="33")throw Error("Tasbih tap count should reach 33");
   await page.locator("#t-undo").click();
   if((await page.locator("#t-count").innerText()).trim()!=="32")throw Error("Tasbih undo should return count to 32");
   await page.locator("#t-reset").click();
   if((await page.locator("#t-count").innerText()).trim()!=="0")throw Error("Tasbih reset should return count to 0");
   await page.locator("#t-phrase").selectOption("custom");
   await page.locator("#t-custom-phrase").fill("Test dhikr");
   if(await page.locator("#t-custom-phrase").isDisabled())throw Error("Tasbih custom phrase field should enable");
   await page.locator("#t-target").selectOption("custom");
   await page.locator("#t-custom-target").fill("33");
   if(!(await page.locator("#t-custom-target-wrap").isVisible()))throw Error("Tasbih custom target field should become visible");
   if(errors.length)throw Error("Tasbih browser errors: "+errors.join("; "));
   console.log("Tasbih browser PASS "+width+"px: count/actions above settings, tap/undo/reset and custom phrase/target");
   await page.close();
  }

  for(const width of [320,360,390,1366]){
   for(const path of ["/","/percentage-calculator/","/fraction-calculator/","/compound-interest-calculator/","/date-calculator/","/bmi-calculator/","/zakat-calculator/"]){
    const page=await browser.newPage({viewport:{width,height:width===1366?768:844}});
    const response=await page.goto(base+path);
    if(!response||response.status()!==200)throw Error(path+" HTTP failure at "+width+"px");
    const sw=await page.evaluate(()=>document.documentElement.scrollWidth);
    if(sw>width+2)throw Error(path+" horizontal overflow at "+width+"px: "+sw);
    await page.close();
   }
   console.log(width+"px responsive overflow audit PASS");
  }

  for(const width of [320,360,390,1366]){
   const page=await browser.newPage({viewport:{width,height:width===320?568:width===360?740:width===390?844:768}});
   const errors=[];page.on("pageerror",e=>errors.push(e.message));
   page.on("console",msg=>{if(msg.type()==="error")errors.push(msg.text());});
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
      badCard:cards.some(el=>{const box=el.getBoundingClientRect(),strong=el.querySelector("strong");return strong.scrollWidth>strong.clientWidth+2||strong.getBoundingClientRect().right>box.right+2;}),
      emi:document.querySelector("#emi-out").textContent,
      submitBottom:document.querySelector("#loan-form button[type=submit]").getBoundingClientRect().bottom};
   });
   if(result.horizontal||result.badCard||width<500&&!result.sideBySide||errors.length||result.emi.includes("NaN")||([390,1366].includes(width)&&result.submitBottom>(width===390?844:768)))throw Error("EMI responsive/first-screen failure "+width+": "+JSON.stringify({result,errors}));
   console.log("EMI responsive browser PASS "+width+"px",result.emi);
   await page.close();
  }
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
