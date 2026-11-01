"use strict";
(function(){
 const form=document.getElementById("extra-calculator-form");
 if(!form||!window.ExtraCalculators)return;
 const output=document.getElementById("extra-result");
 const pctMode=document.getElementById("pct-mode");
 if(pctMode){const labels={of:["Percentage (%)","Number"],whatpercent:["First number (the part)","Second number (the whole)"],change:["Starting value","New value"]};
  const setLabels=()=>{const l=labels[pctMode.value]||labels.of;document.querySelector('label[for="value"]').textContent=l[0];document.querySelector('label[for="total"]').textContent=l[1];output.textContent="";};
  pctMode.addEventListener("change",setLabels);setLabels();}
 form.addEventListener("submit",function(event){
  event.preventDefault();
  try{
   const v=id=>{const node=document.getElementById(id);if(!node||node.value.trim()==="")throw Error("Complete all fields");const n=Number(node.value);if(!Number.isFinite(n))throw Error("Enter valid numbers");return n;};
   const mode=form.dataset.calculator;let result;
   const fmt=n=>n.toLocaleString("en-US",{maximumFractionDigits:10});
   if(mode==="percentage"){const kind=(document.getElementById("pct-mode")||{}).value||"of";const a=v("value"),b=v("total");
    if(kind==="whatpercent")result=fmt(a)+" is "+fmt(window.ExtraCalculators.whatPercent(a,b))+"% of "+fmt(b);
    else if(kind==="change"){const c=window.ExtraCalculators.percentChange(a,b);result=(c>=0?"Increase of ":"Decrease of ")+fmt(Math.abs(c))+"% (from "+fmt(a)+" to "+fmt(b)+")";}
    else result=fmt(window.ExtraCalculators.percentage(a,b));}
   else if(mode==="fraction"){const x=window.ExtraCalculators.fraction(v("a"),v("b"),v("c"),v("d"),document.getElementById("operation").value);result=x.n+"/"+x.d;}
   else if(mode==="compound"){const principal=v("principal");const future=window.ExtraCalculators.compound(principal,v("rate"),v("years"),v("frequency"));result="Final amount: "+future.toLocaleString("en-US",{minimumFractionDigits:2,maximumFractionDigits:2})+" | Interest earned: "+(future-principal).toLocaleString("en-US",{minimumFractionDigits:2,maximumFractionDigits:2});}
   else if(mode==="date"){const start=document.getElementById("start").value,end=document.getElementById("end").value;result=window.ExtraCalculators.dateDifference(start,end).toLocaleString("en-US")+" days (end minus start)";}
   output.textContent=result;
  }catch(error){output.textContent=error.message;}
 });
})();
