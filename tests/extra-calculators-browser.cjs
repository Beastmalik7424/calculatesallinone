"use strict";
const {chromium}=require("playwright");
(async()=>{
 const browser=await chromium.launch({headless:true,args:["--no-sandbox"]});
 const base="http://127.0.0.1:4174";
 const viewports=[{width:320,height:568},{width:390,height:844},{width:1366,height:768}];
 try{
  for(const viewport of viewports){
   const page=await browser.newPage({viewport});
   const errors=[];
   page.on("pageerror",e=>errors.push(e.message));
   page.on("console",msg=>{if(msg.type()==="error")errors.push(msg.text());});
   for(const [path,fields,expected] of [
    ["/fraction-calculator/",[["a","1"],["b","2"],["c","1"],["d","3"]],"5/6"],
    ["/compound-interest-calculator/",[["principal","1000"],["rate","10"],["years","1"],["frequency","2"]],"1,102.50"],
    ["/date-calculator/",[["start","2024-02-28"],["end","2024-03-01"]],"2 days"],
    ["/percentage-difference-calculator/",[["first","40"],["second","60"]],"40%"],
    ["/ratio-calculator/",[["a","10"],["b","15"]],"2:3"]
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
    if(path==="/date-calculator/"){
     for(const id of ["start","end"]){
      if(await page.locator("#"+id).getAttribute("autocomplete")!=="off")throw Error("Date input "+id+" must declare autocomplete=off at "+viewport.width+"px");
     }
     for(const [start,end,expectedDays] of [
      ["0001-01-01","0001-01-02","1 day"],
      ["0004-02-28","0004-03-01","2 days"],
      ["0099-12-31","0100-01-01","1 day"],
      ["0100-02-28","0100-03-01","1 day"],
      ["0400-02-28","0400-03-01","2 days"]
     ]){
      await page.locator("#start").fill(start);
      await page.locator("#end").fill(end);
      await form.locator("button[type=submit]").click();
      const dateResult=await page.locator("#extra-result").innerText();
      if(!dateResult.includes(expectedDays))throw Error("Date difference "+start+" to "+end+" expected "+expectedDays+" at "+viewport.width+"px: "+dateResult);
     }
     for(const label of ['label:has(#date-count-elapsed)','label:has(#date-count-inclusive)']){
      const target=await page.locator(label).boundingBox();
      if(!target||target.height<44)throw Error("Date-count radio target is below 44px at "+viewport.width+"px: "+label);
     }
     await page.locator("#start").fill("2024-01-31");
     await page.locator("#end").fill("2024-02-29");
     await page.locator("#date-count-elapsed").check();
     await form.locator("button[type=submit]").click();
     const elapsedResult=await page.locator("#extra-result").innerText();
     if(!elapsedResult.includes("29 days (elapsed)")||!elapsedResult.includes("0 years, 1 month, 0 days")||!elapsedResult.includes("4.14 weeks"))throw Error("Elapsed date result or calendar breakdown is incorrect at "+viewport.width+"px: "+elapsedResult);
     await page.locator("#date-count-inclusive").check();
     if(await page.locator("#extra-result").innerText())throw Error("Changing the date-count mode should clear the previous result");
     await form.locator("button[type=submit]").click();
     const inclusiveResult=await page.locator("#extra-result").innerText();
     if(!inclusiveResult.includes("30 days (inclusive)")||!inclusiveResult.includes("0 years, 1 month, 0 days"))throw Error("Inclusive count must change the day total only at "+viewport.width+"px: "+inclusiveResult);
     await page.locator("#start").fill("2024-03-01");
     await page.locator("#end").fill("2024-01-31");
     await form.locator("button[type=submit]").click();
     const reverseResult=await page.locator("#extra-result").innerText();
     if(!reverseResult.includes("-31 days (inclusive)")||!reverseResult.includes("0 years, -1 month, -1 day"))throw Error("Reversed inclusive date result lost its sign or calendar breakdown at "+viewport.width+"px: "+reverseResult);
    }
    if(path==="/ratio-calculator/"){
     const ratioMode=page.locator("#ratio-mode");
     await ratioMode.selectOption("three");
     if(!(await page.locator("#ratio-field-c").isVisible())||await page.locator("#ratio-field-d").isVisible()||await page.locator("#ratio-field-factor").isVisible())throw Error("Three-term mode must show C and hide D and the scale factor");
     await page.locator("#a").fill("100");await page.locator("#b").fill("200");await page.locator("#c").fill("400");
     await form.locator("button[type=submit]").click();
     if(!(await page.locator("#extra-result").innerText()).includes("1:2:4"))throw Error("100:200:400 should simplify to 1:2:4");
     await page.locator("#a").fill("1.5");await page.locator("#b").fill("3");await page.locator("#c").fill("4.5");
     await form.locator("button[type=submit]").click();
     if(!(await page.locator("#extra-result").innerText()).includes("1:2:3"))throw Error("Decimal three-term ratio 1.5:3:4.5 should simplify to 1:2:3");
     await page.locator("#a").fill("0");await page.locator("#b").fill("0");await page.locator("#c").fill("5");
     await form.locator("button[type=submit]").click();
     if(!(await page.locator("#extra-result").innerText()).includes("0:0:1"))throw Error("A three-term ratio with two zero terms should reduce to 0:0:1");
     await page.locator("#a").fill("0");await page.locator("#b").fill("0");await page.locator("#c").fill("0");
     await form.locator("button[type=submit]").click();
     if(!(await page.locator("#extra-result").innerText()).includes("All three ratio terms cannot be zero"))throw Error("An all-zero three-term ratio must be rejected");
     await ratioMode.selectOption("proportion");
     if(!(await page.locator("#ratio-field-c").isVisible())||!(await page.locator("#ratio-field-d").isVisible())||await page.locator("#ratio-field-factor").isVisible())throw Error("Proportion mode must show C and D and hide the scale factor");
     await page.locator("#a").fill("2");await page.locator("#b").fill("3");await page.locator("#c").fill("4");await page.locator("#d").fill("");
     await form.locator("button[type=submit]").click();
     if(!(await page.locator("#extra-result").innerText()).includes("Missing D = 6"))throw Error("2:3 = 4:D should solve D as 6");
     await page.locator("#a").fill("1e308");await page.locator("#b").fill("1e-308");await page.locator("#c").fill("1e308");await page.locator("#d").fill("");
     await form.locator("button[type=submit]").click();
     if(!(await page.locator("#extra-result").innerText()).includes("Missing D = 1.000000e-308"))throw Error("A representable tiny proportion result must not be displayed as zero");
     await ratioMode.selectOption("scale");
     if(!(await page.locator("#ratio-field-factor").isVisible())||await page.locator("#ratio-field-c").isVisible())throw Error("Scale mode must show the factor and hide proportion fields");
     await page.locator("#a").fill("2");await page.locator("#b").fill("3");await page.locator("#factor").fill("4");
     await form.locator("button[type=submit]").click();
     if(!(await page.locator("#extra-result").innerText()).includes("8:12"))throw Error("Scaling 2:3 by 4 should return 8:12");
     await page.locator("#a").fill("9007199254740993");await page.locator("#b").fill("2");await page.locator("#factor").fill("1");
     await form.locator("button[type=submit]").click();
     if(!(await page.locator("#extra-result").innerText()).includes("9007199254740993:2"))throw Error("Scale mode must preserve whole-number precision above Number.MAX_SAFE_INTEGER");
     await page.locator("#a").fill("1.5");await page.locator("#b").fill("2.5");await page.locator("#factor").fill("0.1");
     await form.locator("button[type=submit]").click();
     if(!(await page.locator("#extra-result").innerText()).includes("0.15:0.25"))throw Error("Decimal scaling must preserve exact results up to twelve decimal places");
     await page.locator("#a").fill("1.0000001");await page.locator("#b").fill("2");await page.locator("#factor").fill("1");
     await form.locator("button[type=submit]").click();
     if(!(await page.locator("#extra-result").innerText()).includes("up to 6 decimal places"))throw Error("Scale mode must reject more than six decimal places");
     await ratioMode.selectOption("simplify");
     await page.locator("#a").fill("1.5");await page.locator("#b").fill("2.5");
     await form.locator("button[type=submit]").click();
     if(!(await page.locator("#extra-result").innerText()).includes("3:5"))throw Error("Decimal ratio 1.5:2.5 should simplify to 3:5");
     await page.locator("#a").fill("9007199254740993");await page.locator("#b").fill("9007199254740995");
     await form.locator("button[type=submit]").click();
     if(!(await page.locator("#extra-result").innerText()).includes("9007199254740993:9007199254740995"))throw Error("Ratio inputs must preserve integer precision above Number.MAX_SAFE_INTEGER");
     await page.locator("#a").fill("0");await page.locator("#b").fill("0");
     await form.locator("button[type=submit]").click();
     if(!(await page.locator("#extra-result").innerText()).includes("Both ratio terms cannot be zero"))throw Error("Zero-to-zero ratio must be rejected");
     await ratioMode.selectOption("proportion");
     await page.locator("#a").fill("2");await page.locator("#b").fill("3");await page.locator("#c").fill("");await page.locator("#d").fill("");
     await form.locator("button[type=submit]").click();
     if(!(await page.locator("#extra-result").innerText()).includes("Leave exactly one proportion value blank"))throw Error("Proportion mode must require exactly three known values");
    }
    if(path==="/percentage-difference-calculator/"){
     if(await page.locator("#first").getAttribute("min")!=="0"||await page.locator("#second").getAttribute("min")!=="0")throw Error("Percentage difference inputs must reject negative values at the HTML level");
     await page.locator("#first").fill("60");await page.locator("#second").fill("40");await form.locator("button[type=submit]").click();
     if(!(await page.locator("#extra-result").innerText()).includes("40%"))throw Error("Swapping percentage-difference inputs must preserve the result");
     await page.locator("#first").fill("0");await page.locator("#second").fill("10");await form.locator("button[type=submit]").click();
     if(!(await page.locator("#extra-result").innerText()).includes("200%"))throw Error("Zero versus a positive value should return 200%");
     await page.locator("#first").fill("0");await page.locator("#second").fill("0");await form.locator("button[type=submit]").click();
     if(!(await page.locator("#extra-result").innerText()).includes("Both values cannot be zero"))throw Error("Two zero values must be rejected");
     await page.locator("#first").fill("5e-324");await page.locator("#second").fill("5e-324");await form.locator("button[type=submit]").click();
     if(!(await page.locator("#extra-result").innerText()).includes("Average: 4.940656e-324"))throw Error("Equal minimum positive values must retain a representable average");
    }
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
   const page=await browser.newPage({viewport:{width,height:width===390?844:768}});
   const errors=[];page.on("pageerror",e=>errors.push(e.message));
   page.on("console",msg=>{if(msg.type()==="error")errors.push(msg.text());});
   const response=await page.goto(base+"/unit-converter/");
   if(!response||response.status()!==200)throw Error("Unit converter HTTP failure at "+width+"px");
   const unitResult=page.locator("#conv-result");
   await page.locator("#u-cat").selectOption("weight");
   await page.locator("#u-from").selectOption("kg");
   await page.locator("#u-to").selectOption("lb");
   await page.locator("#u-val").fill("1");
   await page.locator("#conv-form button[type=submit]").click();
   if(!(await unitResult.innerText()).includes("2.20462"))throw Error("1 kg to pounds reference conversion failed");
   await page.locator("#u-cat").selectOption("length");
   await page.locator("#u-from").selectOption("mi");
   await page.locator("#u-to").selectOption("km");
   await page.locator("#u-val").fill("1");
   await page.locator("#conv-form button[type=submit]").click();
   if(!(await unitResult.innerText()).includes("1.60934"))throw Error("1 mile to kilometres reference conversion failed");
   await page.locator("#u-cat").selectOption("temp");
   await page.locator("#u-from").selectOption("F");
   await page.locator("#u-to").selectOption("C");
   await page.locator("#u-val").fill("100");
   await page.locator("#conv-form button[type=submit]").click();
   if(!(await unitResult.innerText()).includes("37.78"))throw Error("100 Fahrenheit to Celsius reference conversion failed");
   const unitRuns=await page.evaluate(()=>{
    const form=document.querySelector("#conv-form"),category=document.querySelector("#u-cat");
    const value=document.querySelector("#u-val"),from=document.querySelector("#u-from"),to=document.querySelector("#u-to");
    const output=document.querySelector("#conv-result");
    const units={
     weight:{keys:["kg","g","lb","oz"],factor:{kg:1,g:0.001,lb:0.45359237,oz:0.028349523125}},
     length:{keys:["m","cm","km","ft","in","mi"],factor:{m:1,cm:0.01,km:1000,ft:0.3048,in:0.0254,mi:1609.344}},
     temp:{keys:["C","F","K"]}
    };
    let seed=20261114;
    const random=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)/4294967296;};
    let count=0;
    for(let i=0;i<1000;i++){
     const name=["weight","length","temp"][i%3],spec=units[name];
     category.value=name;category.dispatchEvent(new Event("change",{bubbles:true}));
     const source=spec.keys[Math.floor(random()*spec.keys.length)];
     const target=spec.keys[Math.floor(random()*spec.keys.length)];
     let input;
     if(name==="weight"||name==="length")input=random()*100000;
     else input=source==="K"?random()*1000:source==="F"?-459.67+random()*1000:-273.15+random()*1000;
     from.value=source;to.value=target;value.value=String(input);
     form.dispatchEvent(new Event("submit",{bubbles:true,cancelable:true}));
     const match=output.textContent.match(/ equals ([+-]?[0-9,]+(?:\.[0-9]+)?) /);
     if(!match)throw new Error("unit simulation "+i+" returned unexpected text: "+output.textContent);
     const actual=Number(match[1].replace(/,/g,""));
     let expected;
     if(name==="temp"){
      const c=source==="C"?input:source==="F"?(input-32)*5/9:input-273.15;
      expected=target==="C"?c:target==="F"?c*9/5+32:c+273.15;
     }else expected=input*spec.factor[source]/spec.factor[target];
     const tolerance=name==="temp"?0.0051:1e-5*Math.max(1,Math.abs(expected));
     if(!Number.isFinite(actual)||Math.abs(actual-expected)>tolerance)
      throw new Error("unit simulation "+i+" mismatch "+name+" "+source+" to "+target+": expected "+expected+", got "+actual);
     count++;
    }
    return count;
   });
   if(unitRuns!==1000)throw Error("Expected 1,000 unit-conversion simulations, got "+unitRuns);
   await page.locator("#u-cat").selectOption("weight");
   await page.locator("#u-from").selectOption("kg");
   await page.locator("#u-to").selectOption("lb");
   await page.locator("#u-val").fill("-1");
   await page.locator("#conv-form button[type=submit]").click();
   if(!(await unitResult.innerText()).includes("cannot be negative"))throw Error("Negative mass validation failed");
   await page.locator("#u-cat").selectOption("length");
   await page.locator("#u-from").selectOption("m");
   await page.locator("#u-to").selectOption("cm");
   await page.locator("#u-val").fill("-1");
   await page.locator("#conv-form button[type=submit]").click();
   if(!(await unitResult.innerText()).includes("cannot be negative"))throw Error("Negative length validation failed");
   await page.locator("#u-cat").selectOption("temp");
   await page.locator("#u-from").selectOption("C");
   await page.locator("#u-to").selectOption("K");
   await page.locator("#u-val").fill("-273.151");
   await page.locator("#conv-form button[type=submit]").click();
   if(!(await unitResult.innerText()).includes("below absolute zero"))throw Error("Absolute-zero validation failed");
   if(errors.length)throw Error("Unit converter browser errors: "+errors.join("; "));
   console.log("Unit converter PASS "+width+"px: 1,000 deterministic conversions, reference values and input boundaries");
   await page.close();
  }

  for(const width of [320,390,1366]){
   const viewport={width,height:width===390?844:width===320?568:768};
   const page=await browser.newPage({viewport});
   const errors=[];page.on("pageerror",e=>errors.push(e.message));
   page.on("console",msg=>{if(msg.type()==="error")errors.push(msg.text());});
   page.on("dialog",dialog=>dialog.accept());
   const response=await page.goto(base+"/tasbih-counter/");
   if(!response||response.status()!==200)throw Error("Tasbih page HTTP failure at "+width+"px");
   const order=await page.evaluate(()=>{
    const rect=s=>{const r=document.querySelector(s).getBoundingClientRect();return {top:r.top,bottom:r.bottom};};
    const tap=document.querySelector("#t-tap");
    const tapStyle=getComputedStyle(tap);
    const carousel=document.querySelector(".ca-calculator-carousel");
    const primary=carousel?.querySelector('[data-tool-set="primary"]');
    return {count:rect("#t-count"),tap:rect("#t-tap"),tapDisplay:tapStyle.display,tapVisibility:tapStyle.visibility,tapOpacity:tapStyle.opacity,tapPointerEvents:tapStyle.pointerEvents,actions:rect("#t-tap + .grid"),settings:rect(".ca-tasbih-settings"),phrase:rect("#t-phrase"),target:rect("#t-target"),undo:rect("#t-undo"),reset:rect("#t-reset"),carouselLinks:primary?.querySelectorAll("[data-tool-shortcut]").length||0,activeHref:primary?.querySelector('a[aria-current="page"]')?.getAttribute("href"),overflow:document.documentElement.scrollWidth>innerWidth+2};
   });
   if(!(order.count.top<order.settings.top&&order.settings.top<order.tap.top&&order.tap.top<order.actions.top))throw Error("Tasbih count, phrase/target settings, tap and reset must follow the intended first-screen order at "+width+"px: "+JSON.stringify(order));
   if(order.tap.bottom<=order.tap.top||order.tapDisplay==="none"||order.tapVisibility!=="visible"||Number(order.tapOpacity)===0||order.tapPointerEvents==="none")throw Error("Tasbih Count one button is not visibly clickable: "+JSON.stringify(order));
   if(order.carouselLinks<8||order.activeHref!=="/tasbih-counter/")throw Error("Tasbih page carousel is incomplete or current tool is not active: "+JSON.stringify(order));
   if(order.settings.bottom>viewport.height||order.phrase.bottom>viewport.height||order.target.bottom>viewport.height||order.count.bottom>viewport.height||order.undo.bottom>viewport.height||order.reset.bottom>viewport.height||order.overflow)throw Error("Tasbih count, phrase/target and primary actions must fit the first viewport at "+width+"px: "+JSON.stringify(order));
   for(let i=0;i<33;i++)await page.locator("#t-tap").click();
   if((await page.locator("#t-count").innerText()).trim()!=="33")throw Error("Tasbih tap count should reach 33");
   await page.locator("#t-undo").click();
   if((await page.locator("#t-count").innerText()).trim()!=="32")throw Error("Tasbih undo should return count to 32");
   await page.locator("#t-reset").click();
   if((await page.locator("#t-count").innerText()).trim()!=="0")throw Error("Tasbih reset should return count to 0");
   await page.locator("#t-phrase").selectOption("custom");
   await page.locator("#t-custom-phrase").fill("Test dhikr");
   if(await page.locator("#t-custom-phrase").isDisabled())throw Error("Tasbih custom phrase field should enable");
   await page.locator("#t-target").selectOption("99");
   await page.reload();
   if((await page.locator("#t-target").inputValue())!=="99")throw Error("Tasbih preset target must persist across reload");
   if((await page.locator("#t-phrase").inputValue())!=="custom"||(await page.locator("#t-custom-phrase").inputValue())!=="Test dhikr")throw Error("Tasbih custom phrase must persist across reload");
   await page.locator("#t-target").selectOption("custom");
   await page.locator("#t-custom-target").fill("0");
   await page.locator("#t-tap").click();
   if((await page.locator("#t-count").innerText()).trim()!=="0"||!(await page.locator("#t-target-error").innerText()).includes("1 to 10,000"))throw Error("Tasbih must reject a custom target below 1");
   await page.locator("#t-custom-target").fill("10001");
   await page.locator("#t-tap").click();
   if((await page.locator("#t-count").innerText()).trim()!=="0"||!(await page.locator("#t-target-error").innerText()).includes("1 to 10,000"))throw Error("Tasbih must reject a custom target above 10,000");
   await page.locator("#t-custom-target").fill("123");
   if(!(await page.locator("#t-custom-target-wrap").isVisible()))throw Error("Tasbih custom target field should become visible");
   const countAfterThousand=await page.evaluate(()=>{
    const button=document.querySelector("#t-tap");
    for(let i=0;i<1000;i++)button.click();
    return document.querySelector("#t-count").textContent.trim();
   });
   if(countAfterThousand!=="1000")throw Error("Tasbih must preserve all 1,000 manual taps without target auto-reset: "+countAfterThousand);
   await page.reload();
   if((await page.locator("#t-count").innerText()).trim()!=="1000")throw Error("Tasbih count must persist across reload in the same browser");
   if((await page.locator("#t-target").inputValue())!=="custom"||(await page.locator("#t-custom-target").inputValue())!=="123")throw Error("Tasbih custom target must persist across reload");
   if((await page.locator("#t-phrase").inputValue())!=="custom"||(await page.locator("#t-custom-phrase").inputValue())!=="Test dhikr")throw Error("Tasbih custom phrase must remain selected after reload");
   const countAfterUndo=await page.evaluate(()=>{
    const button=document.querySelector("#t-undo");
    for(let i=0;i<1000;i++)button.click();
    return document.querySelector("#t-count").textContent.trim();
   });
   if(countAfterUndo!=="0")throw Error("Tasbih must reverse 1,000 undo operations to zero: "+countAfterUndo);
   if(errors.length)throw Error("Tasbih browser errors: "+errors.join("; "));
   console.log("Tasbih browser PASS "+width+"px: count/actions above settings, tap/undo/reset and custom phrase/target");
   await page.close();
  }

  {
   const page=await browser.newPage({viewport:{width:390,height:844}});
   const errors=[];page.on("pageerror",e=>errors.push(e.message));
   page.on("console",msg=>{if(msg.type()==="error")errors.push(msg.text());});
   await page.addInitScript(()=>Object.defineProperty(window,"localStorage",{configurable:true,get(){throw new DOMException("Storage blocked","SecurityError");}}));
   const response=await page.goto(base+"/tasbih-counter/");
   if(!response||response.status()!==200)throw Error("Tasbih blocked-storage page HTTP failure");
   if(!(await page.locator("#t-storage-note").isVisible()))throw Error("Tasbih must disclose unavailable browser storage");
   await page.locator("#t-tap").click();
   if((await page.locator("#t-count").innerText()).trim()!=="1")throw Error("Tasbih must still count in memory when storage is blocked");
   await page.reload();
   if((await page.locator("#t-count").innerText()).trim()!=="0")throw Error("Tasbih must not claim persistence when browser storage is blocked");
   if(errors.length)throw Error("Tasbih blocked-storage browser errors: "+errors.join("; "));
   console.log("Tasbih blocked-storage fallback PASS: visible notice, in-memory count, reload reset");
   await page.close();
  }

  {
   const page=await browser.newPage({viewport:{width:390,height:844}});
   const response=await page.goto(base+"/ur/tasbih-counter/");
   if(!response||response.status()!==200)throw Error("Urdu Tasbih page HTTP failure");
   await page.locator("#t-target").selectOption("custom");
   await page.locator("#t-custom-target").fill("77");
   await page.reload();
   if((await page.locator("#t-target").inputValue())!=="custom"||(await page.locator("#t-custom-target").inputValue())!=="77")throw Error("Urdu Tasbih custom target must persist across reload");
   console.log("Urdu Tasbih custom target persistence PASS");
   await page.close();
  }

  for(const width of [320,360,390,1366]){
   for(const path of ["/","/percentage-calculator/","/percentage-difference-calculator/","/fraction-calculator/","/ratio-calculator/","/compound-interest-calculator/","/date-calculator/","/bmi-calculator/","/zakat-calculator/"]){
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
