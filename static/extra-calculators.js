"use strict";
(function(root,factory){
 const api=factory();
 if(typeof module==="object"&&module.exports)module.exports=api;
 if(root)root.ExtraCalculators=api;
})(typeof window!=="undefined"?window:null,function(){
 function finite(...values){if(values.some(v=>typeof v!=="number"||!Number.isFinite(v)))throw Error("Enter valid finite numbers");}
 function percentage(part,total){finite(part,total);return part*total/100;}
 function gcd(a,b){while(b){[a,b]=[b,a%b];}return Math.abs(a);}
 function fraction(a,b,c,d,operation){finite(a,b,c,d);if(![a,b,c,d].every(Number.isSafeInteger)||b===0||d===0)throw Error("Use whole-number numerators and nonzero denominators");
 let n,den;
 if(operation==="add"){n=a*d+c*b;den=b*d;}
 else if(operation==="subtract"){n=a*d-c*b;den=b*d;}
 else if(operation==="multiply"){n=a*c;den=b*d;}
 else if(operation==="divide"){if(c===0)throw Error("Cannot divide by zero");n=a*d;den=b*c;}
 else throw Error("Unknown fraction operation");
 if(!Number.isSafeInteger(n)||!Number.isSafeInteger(den))throw Error("Fraction exceeds safe integer range");
 if(den<0){n=-n;den=-den;}const divisor=gcd(Math.abs(n),den);return {n:n/divisor,d:den/divisor};
 }
 function compound(principal,rate,years,frequency){finite(principal,rate,years,frequency);if(principal<0||years<0||rate<=-100*frequency||!Number.isSafeInteger(frequency)||frequency<1||frequency>365)throw Error("Invalid investment values");const value=principal*Math.pow(1+rate/(100*frequency),frequency*years);if(!Number.isFinite(value))throw Error("Result exceeds supported range");return value;}
 function parseISO(s){if(typeof s!=="string"||!/^(\d{4})-(\d{2})-(\d{2})$/.test(s))throw Error("Use YYYY-MM-DD dates");const [y,m,d]=s.split("-").map(Number);const ms=Date.UTC(y,m-1,d);const t=new Date(ms);if(y<100||t.getUTCFullYear()!==y||t.getUTCMonth()!==m-1||t.getUTCDate()!==d)throw Error("Invalid calendar date");return ms;}
 function dateDifference(start,end){return (parseISO(end)-parseISO(start))/86400000;}
 return {percentage,fraction,compound,dateDifference};
});
