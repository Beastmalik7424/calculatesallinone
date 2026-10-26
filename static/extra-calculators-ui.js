"use strict";
(function(){
 const form=document.getElementById("extra-calculator-form");
 if(!form||!window.ExtraCalculators)return;
 const output=document.getElementById("extra-result");
 form.addEventListener("submit",function(event){
  event.preventDefault();
  try{
   const v=id=>{const node=document.getElementById(id);if(!node||node.value.trim()==="")throw Error("Complete all fields");const n=Number(node.value);if(!Number.isFinite(n))throw Error("Enter valid numbers");return n;};
   const mode=form.dataset.calculator;let result;
   if(mode==="percentage")result=window.ExtraCalculators.percentage(v("value"),v("total")).toLocaleString("en-US",{maximumFractionDigits:10});
   else if(mode==="fraction"){const x=window.ExtraCalculators.fraction(v("a"),v("b"),v("c"),v("d"),document.getElementById("operation").value);result=x.n+"/"+x.d;}
   else if(mode==="compound"){const principal=v("principal");const future=window.ExtraCalculators.compound(principal,v("rate"),v("years"),v("frequency"));result="Final amount: "+future.toLocaleString("en-US",{minimumFractionDigits:2,maximumFractionDigits:2})+" | Interest earned: "+(future-principal).toLocaleString("en-US",{minimumFractionDigits:2,maximumFractionDigits:2});}
   else if(mode==="date"){const start=document.getElementById("start").value,end=document.getElementById("end").value;result=window.ExtraCalculators.dateDifference(start,end).toLocaleString("en-US")+" days (end minus start)";}
   output.textContent=result;
  }catch(error){output.textContent=error.message;}
 });
})();
