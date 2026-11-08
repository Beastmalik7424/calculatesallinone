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
 const ratioMode=document.getElementById("ratio-mode");
 if(ratioMode){
  const updateRatioFields=()=>{
   const mode=ratioMode.value;
   for(const id of ["a","b","c","d","factor"]){
    const wrapper=document.getElementById("ratio-field-"+id);
    const visible=id==="a"||id==="b"||(mode==="three"&&id==="c")||(mode==="proportion"&&(id==="c"||id==="d"))||(mode==="scale"&&id==="factor");
    if(wrapper){wrapper.hidden=!visible;const input=wrapper.querySelector("input");if(input)input.disabled=!visible;}
   }
   output.textContent="";
  };
  ratioMode.addEventListener("change",updateRatioFields);
  updateRatioFields();
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
   else if(mode==="percentage-difference"){
    const answer=window.ExtraCalculators.percentageDifference(v("first"),v("second"));
    const format=n=>n!==0&&(Math.abs(n)<1e-6||Math.abs(n)>=1e12)?n.toExponential(6):n.toLocaleString("en-US",{maximumFractionDigits:8});
    result="Percentage difference: "+format(answer.percentage)+"% | Absolute difference: "+format(answer.difference)+" | Average: "+format(answer.average);
   }
   else if(mode==="ratio"){
    const kind=document.getElementById("ratio-mode").value;
    const format=n=>n!==0&&(Math.abs(n)<1e-6||Math.abs(n)>=1e12)?n.toExponential(6):n.toLocaleString("en-US",{maximumFractionDigits:8});
    const raw=id=>{const node=document.getElementById(id);if(!node)throw Error("Missing input field");const value=node.value.trim();if(value==="")throw Error("Complete all fields");return value;};
    if(kind==="simplify"){
     const x=window.ExtraCalculators.simplifyRatio(raw("a"),raw("b"));
     result="Simplified ratio: "+x.a+":"+x.b;
    }else if(kind==="three"){
     const x=window.ExtraCalculators.simplifyRatioThree(raw("a"),raw("b"),raw("c"));
     result="Simplified three-term ratio: "+x.a+":"+x.b+":"+x.c;
    }else if(kind==="proportion"){
     const optional=id=>{const node=document.getElementById(id);if(!node)throw Error("Missing input field");const raw=node.value.trim();if(raw==="")return null;const n=Number(raw);if(!Number.isFinite(n))throw Error("Enter valid numbers");return n;};
     const x=window.ExtraCalculators.solveProportion(optional("a"),optional("b"),optional("c"),optional("d"));
     result="Proportion: "+format(x.a)+":"+format(x.b)+" = "+format(x.c)+":"+format(x.d)+" | Missing "+x.missing+" = "+format(x.value);
    }else if(kind==="scale"){
     const x=window.ExtraCalculators.scaleRatio(v("a"),v("b"),v("factor"));
     result="Equivalent ratio: "+format(x.a)+":"+format(x.b);
    }else throw Error("Choose a calculation type");
   }
   else if(mode==="fraction"){const x=window.ExtraCalculators.fraction(v("a"),v("b"),v("c"),v("d"),document.getElementById("operation").value);result=x.n+"/"+x.d;}
   else if(mode==="compound"){const principal=v("principal");const future=window.ExtraCalculators.compound(principal,v("rate"),v("years"),v("frequency"));result="Final amount: "+future.toLocaleString("en-US",{minimumFractionDigits:2,maximumFractionDigits:2})+" | Interest earned: "+(future-principal).toLocaleString("en-US",{minimumFractionDigits:2,maximumFractionDigits:2});}
   else if(mode==="date"){const start=document.getElementById("start").value,end=document.getElementById("end").value;result=window.ExtraCalculators.dateDifference(start,end).toLocaleString("en-US")+" days (end minus start)";}
   output.textContent=result;
  }catch(error){output.textContent=error.message;}
 });
})();
