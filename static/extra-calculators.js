"use strict";
(function(root,factory){
 const api=factory();
 if(typeof module==="object"&&module.exports)module.exports=api;
 if(root)root.ExtraCalculators=api;
})(typeof window!=="undefined"?window:null,function(){
 function finite(...values){if(values.some(v=>typeof v!=="number"||!Number.isFinite(v)))throw Error("Enter valid finite numbers");}
 function percentage(part,total){finite(part,total);const result=Math.abs(part)>=Math.abs(total)?(part/100)*total:part*(total/100);if(!Number.isFinite(result))throw Error("Result exceeds supported range");return result;}
 function percentageShare(part,whole){finite(part,whole);if(whole===0)throw Error("The whole amount cannot be zero");const result=part/whole*100;if(!Number.isFinite(result))throw Error("Result exceeds supported range");return result;}
 function whatPercent(part,whole){return percentageShare(part,whole);}
 function percentChange(from,to){finite(from,to);if(from<=0)throw Error("The starting value must be greater than zero");const result=(to-from)/from*100;if(!Number.isFinite(result))throw Error("Result exceeds supported range");return result;}

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
 function dateDifference(start,end){return (parseISO(end)-parseISO(start))/86400000;}
 return {percentage,percentageShare,whatPercent,percentChange,fraction,compound,dateDifference};
});
