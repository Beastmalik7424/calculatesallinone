"use strict";
(function(root,factory){
 const api=factory();
 if(typeof module==="object"&&module.exports)module.exports=api;
 if(root)root.ExtraCalculators=api;
})(typeof window!=="undefined"?window:null,function(){
 function finite(...values){if(values.some(v=>typeof v!=="number"||!Number.isFinite(v)))throw Error("Enter valid finite numbers");}
 function percentage(part,total){finite(part,total);const result=Math.abs(part)>=Math.abs(total)?(part/100)*total:part*(total/100);if(!Number.isFinite(result))throw Error("Result exceeds supported range");return result;}
 function percentageShare(part,whole){finite(part,whole);if(whole===0)throw Error("The whole amount cannot be zero");const result=part/whole*100;if(!Number.isFinite(result))throw Error("Result exceeds supported range");return result;}
 function percentageChange(start,end){
  finite(start,end);
  if(start<=0)throw Error("The starting value must be greater than zero");
  const difference=end-start;
  let result;
  if(Number.isFinite(difference)){
   const direct=(difference/start)*100;
   if(Number.isFinite(direct))result=direct;
  }
  if(result===undefined){
   const scale=Math.max(Math.abs(start),Math.abs(end),1);
   const base=start/scale;
   result=((end/scale-base)/base)*100;
  }
  if(!Number.isFinite(result))throw Error("Result exceeds supported range");
  return result;
 }
 function percentageDifference(first,second){
  finite(first,second);
  if(first<0||second<0)throw Error("Enter two non-negative values");
  const scale=Math.max(first,second);
  if(scale===0)throw Error("Both values cannot be zero because their average is zero");
  const normalizedFirst=first/scale,normalizedSecond=second/scale;
  const normalizedAverage=(normalizedFirst+normalizedSecond)/2;
  const raw=(Math.abs(normalizedFirst-normalizedSecond)/normalizedAverage)*100;
  const percentage=Math.round(raw*1e12)/1e12;
  const difference=Math.abs(first-second);
  const sum=first+second;
  const average=Number.isFinite(sum)?sum/2:first/2+second/2;
  if(average===0)throw Error("The average is too small to represent reliably. Enter larger values");
  finite(difference,average,percentage);
  return {difference,average,percentage};
 }
 function gcd(a,b){while(b){[a,b]=[b,a%b];}return Math.abs(a);}
 function fraction(a,b,c,d,operation){finite(a,b,c,d);if(![a,b,c,d].every(Number.isSafeInteger)||b===0||d===0)throw Error("Use whole-number numerators and nonzero denominators");
 const A=BigInt(a),B=BigInt(b),C=BigInt(c),D=BigInt(d);
 let n,den;
 if(operation==="add"){n=A*D+C*B;den=B*D;}
 else if(operation==="subtract"){n=A*D-C*B;den=B*D;}
 else if(operation==="multiply"){n=A*C;den=B*D;}
 else if(operation==="divide"){if(C===0n)throw Error("Cannot divide by zero");n=A*D;den=B*C;}
 else throw Error("Unknown fraction operation");
 if(den<0n){n=-n;den=-den;}
 let x=n<0n?-n:n,y=den;
 while(y!==0n){const remainder=x%y;x=y;y=remainder;}
 n/=x;den/=x;
 const limit=BigInt(Number.MAX_SAFE_INTEGER);
 if(n>limit||n< -limit||den>limit)throw Error("Fraction exceeds safe integer range");
 return {n:Number(n),d:Number(den)};
 }
 function compound(principal,rate,years,frequency){finite(principal,rate,years,frequency);if(principal<0||years<0||rate<=-100*frequency||!Number.isSafeInteger(frequency)||frequency<1||frequency>365)throw Error("Invalid investment values");const value=principal*Math.pow(1+rate/(100*frequency),frequency*years);if(!Number.isFinite(value))throw Error("Result exceeds supported range");return value;}
 function parseISO(s){if(typeof s!=="string"||!/^(\d{4})-(\d{2})-(\d{2})$/.test(s))throw Error("Use YYYY-MM-DD dates");const [y,m,d]=s.split("-").map(Number);const ms=Date.UTC(y,m-1,d);const t=new Date(ms);if(y<100||t.getUTCFullYear()!==y||t.getUTCMonth()!==m-1||t.getUTCDate()!==d)throw Error("Invalid calendar date");return ms;}
 function scaledRatioTerm(value){
  if(typeof value==="number"&&!Number.isFinite(value))throw Error("Enter valid finite numbers");
  if(typeof value!=="number"&&typeof value!=="string")throw Error("Enter valid ratio terms");
  let raw=String(value).trim();
  if(raw.startsWith("-"))throw Error("Ratio terms must be non-negative");
  if(raw===".")throw Error("Enter a valid decimal value");
  if(raw.startsWith("."))raw="0"+raw;
  if(raw.endsWith("."))raw=raw.slice(0,-1);
  const match=/^([0-9]+)(?:[.]([0-9]{1,6}))?$/.exec(raw);
  if(!match)throw Error("Use non-negative values with up to 6 decimal places");
  return BigInt(match[1])*1000000n+BigInt((match[2]||"").padEnd(6,"0")||"0");
 }
 function gcdBigInt(a,b){while(b!==0n){[a,b]=[b,a%b];}return a<0n?-a:a;}
 function simplifyRatio(a,b){
  const first=scaledRatioTerm(a),second=scaledRatioTerm(b);
  if(first===0n&&second===0n)throw Error("Both ratio terms cannot be zero");
  const divisor=gcdBigInt(first,second);
  return {a:(first/divisor).toString(),b:(second/divisor).toString()};
 }
 function simplifyRatioThree(a,b,c){
  const terms=[a,b,c].map(scaledRatioTerm);
  if(terms.every(term=>term===0n))throw Error("All three ratio terms cannot be zero");
  const divisor=gcdBigInt(gcdBigInt(terms[0],terms[1]),terms[2]);
  return {a:(terms[0]/divisor).toString(),b:(terms[1]/divisor).toString(),c:(terms[2]/divisor).toString()};
 }
 function multiplyDivide(first,second,divisor){
  // Divide the numerator factor closest to the divisor first to avoid avoidable intermediate overflow or underflow.
  const candidates=[{ratio:first/divisor,other:second},{ratio:second/divisor,other:first}]
   .filter(item=>Number.isFinite(item.ratio)&&item.ratio>0)
   .map(item=>({value:item.ratio*item.other,distance:Math.abs(Math.log(item.ratio))}))
   .filter(item=>Number.isFinite(item.value)&&item.value>0)
   .sort((left,right)=>left.distance-right.distance);
  if(candidates.length)return candidates[0].value;
  const fallback=(first*second)/divisor;
  if(Number.isFinite(fallback)&&fallback>0)return fallback;
  throw Error("Result exceeds supported range");
 }
 function solveProportion(a,b,c,d){
  const values=[a,b,c,d];
  const missing=values.map((value,index)=>value===null?index:-1).filter(index=>index!==-1);
  if(missing.length!==1)throw Error("Leave exactly one proportion value blank");
  const known=values.filter(value=>value!==null);
  finite(...known);
  if(known.some(value=>value<=0))throw Error("Enter three positive values to solve a proportion");
  let value;
  switch(missing[0]){
   case 0:value=multiplyDivide(b,c,d);break;
   case 1:value=multiplyDivide(a,d,c);break;
   case 2:value=multiplyDivide(a,d,b);break;
   case 3:value=multiplyDivide(b,c,a);break;
  }
  if(!Number.isFinite(value)||value<=0)throw Error("Result exceeds supported range");
  const completed=values.slice();completed[missing[0]]=value;
  return {missing:["A","B","C","D"][missing[0]],value,a:completed[0],b:completed[1],c:completed[2],d:completed[3]};
 }
 function scaledProductToString(value){
  const scale=1000000000000n;
  const whole=value/scale;
  const fraction=(value%scale).toString().padStart(12,"0").replace(/0+$/,"");
  return fraction?whole.toString()+"."+fraction:whole.toString();
 }
 function scaleRatio(a,b,factor){
  const first=scaledRatioTerm(a),second=scaledRatioTerm(b),multiplier=scaledRatioTerm(factor);
  if(first===0n&&second===0n)throw Error("Use non-negative ratio terms, not both zero, and a positive scale factor");
  if(multiplier===0n)throw Error("Use non-negative ratio terms, not both zero, and a positive scale factor");
  return {a:scaledProductToString(first*multiplier),b:scaledProductToString(second*multiplier)};
 }
 function dateDifference(start,end){return (parseISO(end)-parseISO(start))/86400000;}
 return {percentage,percentageShare,percentageChange,percentageDifference,simplifyRatio,simplifyRatioThree,solveProportion,scaleRatio,fraction,compound,dateDifference};
});
