"use strict";
(function(){
 const form=document.getElementById("extra-calculator-form");
 if(!form||!window.ExtraCalculators)return;
 const output=document.getElementById("extra-result");
 const percentageMode=document.getElementById("percentage-mode");
 if(percentageMode){
  const valueLabel=form.querySelector('label[for="value"]');
  const totalLabel=form.querySelector('label[for="total"]');
  const updatePercentageLabels=()=>{
   const labels={
    of:["Percentage (%)","Number"],
    share:["Part","Whole"],
    change:["Starting value","New value"]
   };
   const selected=labels[percentageMode.value]||labels.of;
   if(valueLabel)valueLabel.textContent=selected[0];
   if(totalLabel)totalLabel.textContent=selected[1];
   output.textContent="";
  };
  percentageMode.addEventListener("change",updatePercentageLabels);
  updatePercentageLabels();
 }
 form.addEventListener("submit",function(event){
  event.preventDefault();
  try{
   const v=id=>{const node=document.getElementById(id);if(!node||node.value.trim()==="")throw Error("Complete all fields");const n=Number(node.value);if(!Number.isFinite(n))throw Error("Enter valid numbers");return n;};
   const mode=form.dataset.calculator;let result;
   if(mode==="percentage"){
    const a=v("value"),b=v("total"),kind=document.getElementById("percentage-mode").value;
    if(kind==="share"){
     const answer=window.ExtraCalculators.percentageShare(a,b);
     result="Answer: "+answer.toLocaleString("en-US",{maximumFractionDigits:8})+"% | Calculation: "+a+" ÷ "+b+" × 100";
    }else if(kind==="change"){
     const answer=window.ExtraCalculators.percentageChange(a,b);
     const direction=answer>0?"Increase of ":answer<0?"Decrease of ":"No change: ";
     result=direction+Math.abs(answer).toLocaleString("en-US",{maximumFractionDigits:8})+"% (from "+a+" to "+b+")";
    }else{
     const answer=window.ExtraCalculators.percentage(a,b);
     result="Answer: "+answer.toLocaleString("en-US",{maximumFractionDigits:8})+" | Calculation: "+b+" × "+a+" ÷ 100";
    }
   }
   else if(mode==="fraction"){const x=window.ExtraCalculators.fraction(v("a"),v("b"),v("c"),v("d"),document.getElementById("operation").value);result=x.n+"/"+x.d;}
   else if(mode==="compound"){const principal=v("principal");const future=window.ExtraCalculators.compound(principal,v("rate"),v("years"),v("frequency"));result="Final amount: "+future.toLocaleString("en-US",{minimumFractionDigits:2,maximumFractionDigits:2})+" | Interest earned: "+(future-principal).toLocaleString("en-US",{minimumFractionDigits:2,maximumFractionDigits:2});}
   else if(mode==="date"){const start=document.getElementById("start").value,end=document.getElementById("end").value;result=window.ExtraCalculators.dateDifference(start,end).toLocaleString("en-US")+" days (end minus start)";}
   output.textContent=result;
  }catch(error){output.textContent=error.message;}
 });
})();
