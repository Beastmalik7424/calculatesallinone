(function () {
  "use strict"

  var MSG = {
    en: {
      zakatNoPrice: "Net zakatable wealth is {net}. Enter the silver price per gram to check Nisab. No Zakat amount is shown until Nisab is verified.",
      zakatInput: "Enter zero or a positive value for each amount and silver price.",
      zakatBelow: "Net wealth {net} is below Nisab of {nisab}. Zakat is not due on this wealth.",
      zakatHawl: "Net wealth {net} is above Nisab of {nisab}. Zakat is due only after one full lunar year (hawl). Tick the lunar year box when that period is complete.",
      zakatDue: "Zakat payable at 2.5 percent: {amount}. Confirm the calculation and rules with a qualified scholar before you pay.",
      bmiInput: "Enter a weight from 2 to 500 kg and a height from 50 to 300 cm.",
      bmiInputImp: "Enter a weight from 4 to 1100 lb, a height of 1 to 9 ft, and inches from 0 to 11.9.",
      bmiWeightError: "Enter a weight from 20 to 300 kg using digits and an optional decimal point.",
      bmiWeightLbError: "Enter a weight from 44.1 to 661.3 lb using digits and an optional decimal point.",
      bmiCmError: "Enter a height from 50 to 260 cm using digits and an optional decimal point.",
      bmiFtError: "Enter a whole number of feet from 1 to 8.",
      bmiInError: "Enter inches from 0 to 11.99 using digits and an optional decimal point.",
      bmiStrictResult: "Your BMI is {bmi}. Based on the rounded result, this is in the {label} category for adults (WHO).",
      bmiDisclaimer: "BMI is a general screening tool. It does not measure body fat directly and does not replace advice from a doctor.",
      bmiCalcError: "We could not calculate a valid BMI from those values. Check your entries and try again.",
      bmiResult: "Your BMI is {bmi}, which is in the {label} range for adults (WHO). BMI is a screening measure, not a diagnosis.",
      bmiUnder: "underweight",
      bmiNormal: "normal weight",
      bmiOver: "overweight",
      bmiObese: "obesity",
      profitEnter: "Enter a cost price and a selling price of zero or more.",
      profitWord: "Profit",
      lossWord: "Loss",
      profitNA: "Percentage is N/A because cost price is zero.",
      profitPct: "percent of cost price",
      ageEnter: "Enter your date of birth.",
      ageFuture: "Date of birth cannot be in the future.",
      ageCheck: "Please check the date of birth.",
      ageResult: "Age: {y} years, {m} months and {d} days. Total days lived: {t}.",
      discInput: "Enter a price of zero or more and a discount from 0 to 100 percent.",
      discResult: "You save {saved}. Final price: {final}. Tax is not included.",
      convEnter: "Enter a numeric value.",
      convAbsoluteZero: "Temperature cannot be below absolute zero (-273.15 °C).",
      convKelvin: "Kelvin cannot be below zero, which is absolute zero.",
      convNeg: "A {cat} cannot be negative.",
      convResult: "{v} {from} equals {out} {to}.",
      calcError: "Error",
      calcDiv: "Cannot divide by zero",
      calcSqrtNegative: "Square root of a negative number is not a real number.",
      calcNeedValue: "Enter a number or expression first.",
      calcScientificMode: "Scientific Mode",
      calcStandardMode: "Standard Mode",
      calcDomainError: "Math domain error",
      tasbihNone: "No target set.",
      tasbihReached: "Target of {goal} reached. Press Reset to start again.",
      tasbihLeft: "{left} to go for a target of {goal}.",
      themeDark: "Dark mode",
      themeLight: "Light mode",
      numeric: "en-US",
      units: {
        kg: "kilograms", g: "grams", lb: "pounds", oz: "ounces",
        m: "meters", cm: "centimeters", km: "kilometers", ft: "feet", in: "inches", mi: "miles",
        C: "Celsius", F: "Fahrenheit", K: "Kelvin"
      },
      cats: { weight: "weight", length: "length", temp: "temperature" }
    },
    ur: {
      zakatNoPrice: "خالص قابلِ زکوٰۃ مال {net} ہے۔ نصاب چیک کرنے کے لیے چاندی کی فی گرام قیمت لکھیں۔ نصاب کی تصدیق تک زکوٰۃ کی رقم نہیں دکھائی جائے گی۔",
      zakatInput: "تمام رقوم صفر یا اس سے زیادہ درج کریں۔",
      zakatBelow: "خالص مال {net} نصاب {nisab} سے کم ہے۔ اس مال پر زکوٰۃ واجب نہیں۔",
      zakatHawl: "خالص مال {net} نصاب {nisab} سے زیادہ ہے۔ زکوٰۃ قمری سال مکمل ہونے کے بعد واجب ہوگی۔ مدت پوری ہونے پر قمری سال والا خانہ نشان زد کریں۔",
      zakatDue: "2.5 فیصد زکوٰۃ واجب الادا: {amount}۔ ادائیگی سے پہلے حساب اور اصولوں کی تصدیق کسی مستند عالم سے کریں۔",
      bmiInput: "وزن 2 سے 500 کلو گرام اور قد 50 سے 300 سینٹی میٹر کے درمیان لکھیں۔",
      bmiInputImp: "وزن 4 سے 1100 پاؤنڈ، قد 1 سے 9 فٹ، اور انچ 0 سے 11.9 کے درمیان لکھیں۔",
      bmiWeightError: "وزن 20 سے 300 کلوگرام کے درمیان درج کریں۔ عدد کے ساتھ زیادہ سے زیادہ ایک اعشاری نقطہ استعمال کریں۔",
      bmiWeightLbError: "وزن 44.1 سے 661.3 پاؤنڈ کے درمیان درج کریں۔ عدد کے ساتھ زیادہ سے زیادہ ایک اعشاری نقطہ استعمال کریں۔",
      bmiCmError: "قد 50 سے 260 سینٹی میٹر کے درمیان درج کریں۔ عدد کے ساتھ زیادہ سے زیادہ ایک اعشاری نقطہ استعمال کریں۔",
      bmiFtError: "فٹ کی مکمل عددی قدر 1 سے 8 کے درمیان درج کریں۔",
      bmiInError: "انچ 0 سے 11.99 کے درمیان درج کریں۔ عدد کے ساتھ زیادہ سے زیادہ ایک اعشاری نقطہ استعمال کریں۔",
      bmiStrictResult: "آپ کا BMI {bmi} ہے۔ گول کی گئی قدر کے مطابق یہ بالغوں میں {label} کی حد میں آتا ہے (WHO)۔",
      bmiDisclaimer: "BMI ایک عمومی اسکریننگ پیمانہ ہے۔ یہ جسمانی چربی کو براہ راست نہیں ناپتا اور ڈاکٹر کے مشورے کا متبادل نہیں۔",
      bmiCalcError: "ان قدروں سے درست BMI نہیں نکالا جا سکا۔ اندراجات چیک کر کے دوبارہ کوشش کریں۔",
      bmiResult: "آپ کا BMI {bmi} ہے، جو بالغوں کے لیے WHO کے مطابق {label} کی حد میں ہے۔ BMI ایک اسکریننگ پیمانہ ہے، تشخیص نہیں۔",
      bmiUnder: "کم وزن",
      bmiNormal: "معمول کا وزن",
      bmiOver: "زیادہ وزن",
      bmiObese: "موٹاپا",
      profitEnter: "قیمت خرید اور قیمت فروخت صفر یا اس سے زیادہ لکھیں۔",
      profitWord: "منافع",
      lossWord: "نقصان",
      profitNA: "فیصد N/A ہے کیونکہ قیمت خرید صفر ہے۔",
      profitPct: "فیصد قیمت خرید پر",
      ageEnter: "اپنی تاریخ پیدائش لکھیں۔",
      ageFuture: "تاریخ پیدائش مستقبل کی نہیں ہو سکتی۔",
      ageCheck: "براہ کرم تاریخ پیدائش دوبارہ دیکھیں۔",
      ageResult: "عمر: {y} سال، {m} مہینے اور {d} دن۔ زندگی کے کل دن: {t}۔",
      discInput: "قیمت صفر یا اس سے زیادہ اور ڈسکاؤنٹ 0 سے 100 فیصد کے درمیان لکھیں۔",
      discResult: "آپ کی بچت {saved}۔ آخری قیمت: {final}۔ ٹیکس شامل نہیں ہے۔",
      convEnter: "عددی قدر لکھیں۔",
      convAbsoluteZero: "درجہ حرارت مطلق صفر (-273.15 °C) سے کم نہیں ہو سکتا۔",
      convKelvin: "کیلون صفر سے کم نہیں ہو سکتا، کیونکہ یہ مطلق صفر ہے۔",
      convNeg: "{cat} منفی نہیں ہو سکتی۔",
      convResult: "{v} {from} برابر ہے {out} {to} کے۔",
      calcError: "خرابی",
      calcDiv: "صفر سے تقسیم نہیں ہو سکتی",
      calcSqrtNegative: "منفی عدد کا مربع جذر حقیقی عدد نہیں ہوتا۔",
      calcNeedValue: "پہلے کوئی عدد یا حساب درج کریں۔",
      calcScientificMode: "سائنسی کیلکولیٹر",
      calcStandardMode: "معیاری کیلکولیٹر",
      calcDomainError: "ریاضی کی حد سے باہر قدر",
      tasbihNone: "کوئی ہدف مقرر نہیں۔",
      tasbihReached: "ہدف {goal} پورا ہو گیا۔ دوبارہ شروع کرنے کے لیے ری سیٹ دبائیں۔",
      tasbihLeft: "ہدف {goal} کے لیے {left} باقی۔",
      themeDark: "ڈارک موڈ",
      themeLight: "لائٹ موڈ",
      numeric: "ur-PK",
      units: {
        kg: "کلو گرام", g: "گرام", lb: "پاؤنڈ", oz: "اونس",
        m: "میٹر", cm: "سینٹی میٹر", km: "کلو میٹر", ft: "فٹ", in: "انچ", mi: "میل",
        C: "سینٹی گریڈ", F: "فارن ہائیٹ", K: "کیلون"
      },
      cats: { weight: "وزن", length: "لمبائی", temp: "درجہ حرارت" }
    },
    ar: {
      zakatNoPrice: "صافي المال الخاضع للزكاة هو {net}. أدخل سعر غرام الفضة للتحقق من النصاب. لن يظهر مبلغ الزكاة حتى يتم التحقق من النصاب.",
      zakatInput: "أدخل صفرًا أو قيمة موجبة لكل مبلغ ولسعر الفضة.",
      zakatBelow: "صافي المال {net} أقل من النصاب {nisab}. لا تجب الزكاة على هذا المال.",
      zakatHawl: "صافي المال {net} أعلى من النصاب {nisab}. لا تجب الزكاة إلا بعد اكتمال سنة قمرية واحدة (الحول). حدّد مربع السنة القمرية عند اكتمالها.",
      zakatDue: "الزكاة المستحقة بنسبة 2.5٪: {amount}. تحقّق من الحساب والأحكام مع عالم مؤهل قبل الدفع.",
      bmiInput: "أدخل وزنًا من 2 إلى 500 كغ وطولًا من 50 إلى 300 سم.",
      bmiInputImp: "أدخل وزنًا من 4 إلى 1100 رطل، وطولًا من 1 إلى 9 أقدام، وبوصات من 0 إلى أقل من 12.",
      bmiResult: "مؤشر كتلة جسمك هو {bmi}، ويقع ضمن فئة {label} للبالغين وفق منظمة الصحة العالمية. المؤشر أداة فحص وليس تشخيصًا.",
      bmiUnder: "نقص الوزن",
      bmiNormal: "وزن طبيعي",
      bmiOver: "زيادة الوزن",
      bmiObese: "السمنة",
      profitEnter: "أدخل سعر تكلفة وسعر بيع يساوي كل منهما صفرًا أو أكثر.",
      profitWord: "ربح",
      lossWord: "خسارة",
      profitNA: "النسبة غير متاحة لأن سعر التكلفة يساوي صفرًا.",
      profitPct: "من سعر التكلفة بالمئة",
      ageEnter: "أدخل تاريخ ميلادك.",
      ageFuture: "لا يمكن أن يكون تاريخ الميلاد في المستقبل.",
      ageCheck: "يرجى التحقق من تاريخ الميلاد.",
      ageResult: "العمر: {y} سنة و{m} شهر و{d} يوم. إجمالي أيام الحياة: {t}.",
      discInput: "أدخل سعرًا يساوي صفرًا أو أكثر وخصمًا من 0 إلى 100 بالمئة.",
      discResult: "وفّرت {saved}. السعر النهائي: {final}. لا تشمل الضريبة.",
      convEnter: "أدخل قيمة رقمية.",
      convAbsoluteZero: "لا يمكن أن تكون درجة الحرارة أقل من الصفر المطلق (-273.15 °م).",
      convKelvin: "لا يمكن أن تكون درجة الحرارة بالكلفن أقل من الصفر، فهو الصفر المطلق.",
      convNeg: "لا يمكن أن تكون قيمة {cat} سالبة.",
      convResult: "‏{v} {from} تساوي {out} {to}.",
      calcError: "خطأ",
      calcDiv: "لا يمكن القسمة على صفر",
      calcSqrtNegative: "الجذر التربيعي لعدد سالب ليس عددًا حقيقيًا.",
      calcNeedValue: "أدخل عددًا أو تعبيرًا أولًا.",
      tasbihNone: "لم يتم تحديد هدف.",
      tasbihReached: "تم بلوغ الهدف {goal}. اضغط إعادة الضبط للبدء من جديد.",
      tasbihLeft: "تبقّى {left} للوصول إلى الهدف {goal}.",
      themeDark: "الوضع الداكن",
      themeLight: "الوضع الفاتح",
      numeric: "ar",
      units: { kg: "كيلوغرام", g: "غرام", lb: "رطل", oz: "أونصة", m: "متر", cm: "سنتيمتر", km: "كيلومتر", ft: "قدم", in: "بوصة", mi: "ميل", C: "مئوية", F: "فهرنهايت", K: "كلفن" },
      cats: { weight: "الوزن", length: "الطول", temp: "درجة الحرارة" }
    },
    hi: {
      zakatNoPrice: "शुद्ध ज़कात योग्य संपत्ति {net} है। निसाब जाँचने के लिए चाँदी का प्रति ग्राम मूल्य दर्ज करें। निसाब की पुष्टि होने तक ज़कात की राशि नहीं दिखाई जाएगी।",
      zakatInput: "हर राशि और चाँदी के मूल्य के लिए शून्य या सकारात्मक संख्या दर्ज करें।",
      zakatBelow: "शुद्ध संपत्ति {net}, निसाब {nisab} से कम है। इस संपत्ति पर ज़कात देय नहीं है।",
      zakatHawl: "शुद्ध संपत्ति {net}, निसाब {nisab} से अधिक है। ज़कात तभी देय है जब एक पूरा चंद्र वर्ष (हौल) बीत जाए। अवधि पूरी होने पर चंद्र वर्ष वाला बॉक्स चुनें।",
      zakatDue: "2.5 प्रतिशत की देय ज़कात: {amount}। भुगतान से पहले गणना और नियमों की पुष्टि किसी योग्य विद्वान से करें।",
      bmiInput: "2 से 500 किलोग्राम वजन और 50 से 300 सेंटीमीटर ऊँचाई दर्ज करें।",
      bmiInputImp: "4 से 1100 पाउंड वजन, 1 से 9 फीट ऊँचाई और 0 से 11.9 इंच दर्ज करें।",
      bmiResult: "आपका BMI {bmi} है, जो WHO के अनुसार वयस्कों की {label} श्रेणी में आता है। BMI जाँच का माप है, निदान नहीं।",
      bmiUnder: "कम वजन",
      bmiNormal: "सामान्य वजन",
      bmiOver: "अधिक वजन",
      bmiObese: "मोटापा",
      profitEnter: "लागत मूल्य और बिक्री मूल्य शून्य या उससे अधिक दर्ज करें।",
      profitWord: "लाभ",
      lossWord: "हानि",
      profitNA: "प्रतिशत उपलब्ध नहीं है क्योंकि लागत मूल्य शून्य है।",
      profitPct: "लागत मूल्य का प्रतिशत",
      ageEnter: "अपनी जन्मतिथि दर्ज करें।",
      ageFuture: "जन्मतिथि भविष्य की नहीं हो सकती।",
      ageCheck: "कृपया जन्मतिथि जाँचें।",
      ageResult: "आयु: {y} वर्ष, {m} महीने और {d} दिन। जीवन के कुल दिन: {t}।",
      discInput: "शून्य या उससे अधिक मूल्य और 0 से 100 प्रतिशत तक की छूट दर्ज करें।",
      discResult: "आपकी बचत {saved} है। अंतिम मूल्य: {final}। कर शामिल नहीं है।",
      convEnter: "संख्यात्मक मान दर्ज करें।",
      convAbsoluteZero: "तापमान परम शून्य (-273.15 °C) से कम नहीं हो सकता।",
      convKelvin: "केल्विन का मान शून्य से कम नहीं हो सकता, क्योंकि यही परम शून्य है।",
      convNeg: "{cat} ऋणात्मक नहीं हो सकता।",
      convResult: "{v} {from} = {out} {to}।",
      calcError: "त्रुटि",
      calcDiv: "शून्य से भाग नहीं दे सकते",
      calcSqrtNegative: "ऋणात्मक संख्या का वर्गमूल वास्तविक संख्या नहीं है।",
      calcNeedValue: "पहले कोई संख्या या गणितीय अभिव्यक्ति दर्ज करें।",
      tasbihNone: "कोई लक्ष्य निर्धारित नहीं है।",
      tasbihReached: "लक्ष्य {goal} पूरा हुआ। फिर से शुरू करने के लिए रीसेट दबाएँ।",
      tasbihLeft: "लक्ष्य {goal} तक {left} बाकी हैं।",
      themeDark: "डार्क मोड",
      themeLight: "लाइट मोड",
      numeric: "hi-IN",
      units: { kg: "किलोग्राम", g: "ग्राम", lb: "पाउंड", oz: "औंस", m: "मीटर", cm: "सेंटीमीटर", km: "किलोमीटर", ft: "फुट", in: "इंच", mi: "मील", C: "सेल्सियस", F: "फ़ारेनहाइट", K: "केल्विन" },
      cats: { weight: "वज़न", length: "लंबाई", temp: "तापमान" }
    },
    es: {
      zakatNoPrice: "El patrimonio neto sujeto a zakat es {net}. Introduce el precio de la plata por gramo para comprobar el nisab. No se mostrará el importe de zakat hasta verificar el nisab.",
      zakatInput: "Introduce cero o un valor positivo para cada importe y para el precio de la plata.",
      zakatBelow: "El patrimonio neto {net} está por debajo del nisab de {nisab}. No corresponde pagar zakat por este patrimonio.",
      zakatHawl: "El patrimonio neto {net} supera el nisab de {nisab}. El zakat solo corresponde tras completar un año lunar (hawl). Marca la casilla del año lunar cuando se haya cumplido.",
      zakatDue: "Zakat pagadero al 2,5 %: {amount}. Confirma el cálculo y las normas con una persona experta cualificada antes de pagar.",
      bmiInput: "Introduce un peso de 2 a 500 kg y una altura de 50 a 300 cm.",
      bmiInputImp: "Introduce un peso de 4 a 1100 lb, una altura de 1 a 9 pies y pulgadas de 0 a menos de 12.",
      bmiResult: "Tu IMC es {bmi}, dentro del rango de {label} para adultos según la OMS. El IMC es una medida de cribado, no un diagnóstico.",
      bmiUnder: "bajo peso",
      bmiNormal: "peso normal",
      bmiOver: "sobrepeso",
      bmiObese: "obesidad",
      profitEnter: "Introduce un precio de coste y un precio de venta iguales o superiores a cero.",
      profitWord: "Beneficio",
      lossWord: "Pérdida",
      profitNA: "El porcentaje no está disponible porque el precio de coste es cero.",
      profitPct: "del precio de coste",
      ageEnter: "Introduce tu fecha de nacimiento.",
      ageFuture: "La fecha de nacimiento no puede estar en el futuro.",
      ageCheck: "Comprueba la fecha de nacimiento.",
      ageResult: "Edad: {y} años, {m} meses y {d} días. Días totales vividos: {t}.",
      discInput: "Introduce un precio igual o superior a cero y un descuento del 0 al 100 %.",
      discResult: "Ahorras {saved}. Precio final: {final}. No incluye impuestos.",
      convEnter: "Introduce un valor numérico.",
      convAbsoluteZero: "La temperatura no puede ser inferior al cero absoluto (-273,15 °C).",
      convKelvin: "Los kelvin no pueden ser inferiores a cero, que es el cero absoluto.",
      convNeg: "El valor de {cat} no puede ser negativo.",
      convResult: "{v} {from} equivale a {out} {to}.",
      calcError: "Error",
      calcDiv: "No se puede dividir entre cero",
      calcSqrtNegative: "La raíz cuadrada de un número negativo no es un número real.",
      calcNeedValue: "Introduce primero un número o una expresión.",
      tasbihNone: "No se ha establecido ningún objetivo.",
      tasbihReached: "Objetivo de {goal} alcanzado. Pulsa Reiniciar para empezar de nuevo.",
      tasbihLeft: "Quedan {left} para alcanzar el objetivo de {goal}.",
      themeDark: "Modo oscuro",
      themeLight: "Modo claro",
      numeric: "es-ES",
      units: { kg: "kilogramos", g: "gramos", lb: "libras", oz: "onzas", m: "metros", cm: "centímetros", km: "kilómetros", ft: "pies", in: "pulgadas", mi: "millas", C: "Celsius", F: "Fahrenheit", K: "kelvin" },
      cats: { weight: "peso", length: "longitud", temp: "temperatura" }
    },
    fr: {
      zakatNoPrice: "Le patrimoine net soumis à la zakat est de {net}. Saisissez le prix de l’argent par gramme pour vérifier le nisab. Aucun montant de zakat ne sera affiché avant cette vérification.",
      zakatInput: "Saisissez zéro ou une valeur positive pour chaque montant et pour le prix de l’argent.",
      zakatBelow: "Le patrimoine net {net} est inférieur au nisab de {nisab}. La zakat n’est pas due sur ce patrimoine.",
      zakatHawl: "Le patrimoine net {net} dépasse le nisab de {nisab}. La zakat n’est due qu’après une année lunaire complète (hawl). Cochez la case de l’année lunaire une fois cette période écoulée.",
      zakatDue: "Zakat due au taux de 2,5 % : {amount}. Faites vérifier le calcul et les règles par une personne qualifiée avant de payer.",
      bmiInput: "Saisissez un poids de 2 à 500 kg et une taille de 50 à 300 cm.",
      bmiInputImp: "Saisissez un poids de 4 à 1100 lb, une taille de 1 à 9 pieds et des pouces de 0 à moins de 12.",
      bmiResult: "Votre IMC est de {bmi}, dans la catégorie {label} pour les adultes selon l’OMS. L’IMC est un outil de dépistage, pas un diagnostic.",
      bmiUnder: "insuffisance pondérale",
      bmiNormal: "poids normal",
      bmiOver: "surpoids",
      bmiObese: "obésité",
      profitEnter: "Saisissez un prix de revient et un prix de vente supérieurs ou égaux à zéro.",
      profitWord: "Bénéfice",
      lossWord: "Perte",
      profitNA: "Le pourcentage n’est pas disponible car le prix de revient est nul.",
      profitPct: "du prix de revient",
      ageEnter: "Saisissez votre date de naissance.",
      ageFuture: "La date de naissance ne peut pas être dans le futur.",
      ageCheck: "Veuillez vérifier la date de naissance.",
      ageResult: "Âge : {y} ans, {m} mois et {d} jours. Nombre total de jours vécus : {t}.",
      discInput: "Saisissez un prix supérieur ou égal à zéro et une remise comprise entre 0 et 100 %.",
      discResult: "Vous économisez {saved}. Prix final : {final}. Hors taxes.",
      convEnter: "Saisissez une valeur numérique.",
      convAbsoluteZero: "La température ne peut pas être inférieure au zéro absolu (-273,15 °C).",
      convKelvin: "La température en kelvins ne peut pas être inférieure à zéro, qui correspond au zéro absolu.",
      convNeg: "La valeur de {cat} ne peut pas être négative.",
      convResult: "{v} {from} équivaut à {out} {to}.",
      calcError: "Erreur",
      calcDiv: "Division par zéro impossible",
      calcSqrtNegative: "La racine carrée d’un nombre négatif n’est pas un nombre réel.",
      calcNeedValue: "Saisissez d’abord un nombre ou une expression.",
      tasbihNone: "Aucun objectif défini.",
      tasbihReached: "Objectif de {goal} atteint. Appuyez sur Réinitialiser pour recommencer.",
      tasbihLeft: "Encore {left} pour atteindre l’objectif de {goal}.",
      themeDark: "Mode sombre",
      themeLight: "Mode clair",
      numeric: "fr-FR",
      units: { kg: "kilogrammes", g: "grammes", lb: "livres", oz: "onces", m: "mètres", cm: "centimètres", km: "kilomètres", ft: "pieds", in: "pouces", mi: "miles", C: "Celsius", F: "Fahrenheit", K: "kelvins" },
      cats: { weight: "poids", length: "longueur", temp: "température" }
    }
  }

  var UNITS = {
    weight: { keys: ["kg", "g", "lb", "oz"], base: { kg: 1, g: 0.001, lb: 0.45359237, oz: 0.028349523125 } },
    length: { keys: ["m", "cm", "km", "ft", "in", "mi"], base: { m: 1, cm: 0.01, km: 1000, ft: 0.3048, in: 0.0254, mi: 1609.344 } },
    temp: { keys: ["C", "F", "K"], base: {} }
  }

  function lang () {
    var code = (document.documentElement.lang || "en").toLowerCase().split("-")[0]
    return Object.prototype.hasOwnProperty.call(MSG, code) ? code : "en"
  }

  function t (key, vars) {
    var table = MSG[lang()]
    var text = table[key] !== undefined ? table[key] : MSG.en[key]
    if (vars) {
      Object.keys(vars).forEach(function (name) {
        text = text.split("{" + name + "}").join(String(vars[name]))
      })
    }
    return text
  }

  function $ (id) {
    return document.getElementById(id)
  }

  function num (id) {
    var el = $(id)
    if (!el || el.value === "") return null
    var v = Number(el.value)
    return isFinite(v) ? v : null
  }

  function say (id, text) {
    var el = $(id)
    if (el) el.textContent = text
  }

  function fmt (n) {
    return n.toLocaleString(MSG[lang()].numeric, { maximumFractionDigits: 2 })
  }

  /* Zakat: Nisab is 612.36 g of silver. The amount is shown only after the Nisab and hawl checks. */
  function initZakat () {
    var form = $("zakat-form")
    if (!form) return
    var assetIds = ["z-cash", "z-gold", "z-silver", "z-stock", "z-recv"]
    form.addEventListener("submit", function (e) {
      e.preventDefault()
      var allIds = assetIds.concat(["z-debts", "z-silverprice"])
      var hasInvalidAmount = allIds.some(function (id) {
        var el = $(id)
        if (!el || el.value === "") return false
        var value = Number(el.value)
        return !isFinite(value) || value < 0
      })
      if (hasInvalidAmount) {
        say("zakat-result", t("zakatInput"))
        return
      }
      var assets = 0
      assetIds.forEach(function (id) {
        assets += num(id) || 0
      })
      var net = Math.max(0, assets - (num("z-debts") || 0))
      var price = num("z-silverprice")
      if (price === null || price <= 0) {
        say("zakat-result", t("zakatNoPrice", { net: fmt(net) }))
        return
      }
      var nisab = 612.36 * price
      if (net < nisab) {
        say("zakat-result", t("zakatBelow", { net: fmt(net), nisab: fmt(nisab) }))
        return
      }
      if (!$("z-hawl").checked) {
        say("zakat-result", t("zakatHawl", { net: fmt(net), nisab: fmt(nisab) }))
        return
      }
      say("zakat-result", t("zakatDue", { amount: fmt(net * 0.025) }))
    })
  }

  /* BMI: WHO adult ranges. Imperial inches must be 0 to 11.9. */
  function initBMI () {
    var form = $("bmi-form")
    if (!form) return
    var heightCmRadio = $("bmi-height-cm")
    var heightFtInRadio = $("bmi-height-ftin")
    var weightKgRadio = $("bmi-weight-kg")
    var weightLbRadio = $("bmi-weight-lb")
    if (heightCmRadio && heightFtInRadio && weightKgRadio && weightLbRadio) {
      var metricGroup = $("bmi-metric")
      var imperialGroup = $("bmi-imperial")
      var kgGroup = $("bmi-weight-kg-group")
      var lbGroup = $("bmi-weight-lb-group")
      var kgInput = $("b-kg")
      var lbInput = $("b-lb")
      var cmInput = $("b-cm")
      var ftInput = $("b-ft")
      var inInput = $("b-in")
      var fields = [
        ["b-kg", "b-kg-error", "bmiWeightError", 20, 300, false],
        ["b-lb", "b-lb-error", "bmiWeightLbError", 44.1, 661.3, false],
        ["b-cm", "b-cm-error", "bmiCmError", 50, 260, false],
        ["b-ft", "b-ft-error", "bmiFtError", 1, 8, true],
        ["b-in", "b-in-error", "bmiInError", 0, 11.99, false]
      ]
      function clearError(field) {
        var input = $(field[0])
        var error = $(field[1])
        if (error) error.textContent = ""
        if (input && input.removeAttribute) input.removeAttribute("aria-invalid")
      }
      function clearErrors() { fields.forEach(clearError) }
      function clearResult() { say("bmi-result", "") }
      function toggleWeightUnit() {
        var kilograms = weightKgRadio.checked
        if (kgGroup) {
          kgGroup.classList.toggle("!hidden", !kilograms)
          kgGroup.setAttribute("aria-hidden", String(!kilograms))
        }
        if (lbGroup) {
          lbGroup.classList.toggle("!hidden", kilograms)
          lbGroup.setAttribute("aria-hidden", String(kilograms))
        }
        if (kgInput) kgInput.disabled = !kilograms
        if (lbInput) lbInput.disabled = kilograms
        clearErrors()
        clearResult()
      }
      function toggleHeightUnit() {
        var metric = heightCmRadio.checked
        if (metricGroup) {
          metricGroup.classList.toggle("!hidden", !metric)
          metricGroup.setAttribute("aria-hidden", String(!metric))
        }
        if (imperialGroup) {
          imperialGroup.classList.toggle("!hidden", metric)
          imperialGroup.setAttribute("aria-hidden", String(metric))
        }
        if (cmInput) cmInput.disabled = !metric
        if (ftInput) ftInput.disabled = metric
        if (inInput) inInput.disabled = metric
        clearErrors()
        clearResult()
      }
      function readField(field) {
        var input = $(field[0])
        var error = $(field[1])
        if (!input || input.disabled) return null
        var raw = String(input.value == null ? "" : input.value).trim()
        var value = null
        if (raw !== "" && /^\d+(?:\.\d+)?$/.test(raw)) value = Number(raw)
        var invalid = value === null || !isFinite(value) || value < field[3] || value > field[4] ||
          (field[5] && !Number.isInteger(value))
        if (invalid) {
          if (error) error.textContent = t(field[2])
          if (input.setAttribute) input.setAttribute("aria-invalid", "true")
          return null
        }
        if (error) error.textContent = ""
        if (input.removeAttribute) input.removeAttribute("aria-invalid")
        return value
      }
      heightCmRadio.addEventListener("change", toggleHeightUnit)
      heightFtInRadio.addEventListener("change", toggleHeightUnit)
      weightKgRadio.addEventListener("change", toggleWeightUnit)
      weightLbRadio.addEventListener("change", toggleWeightUnit)
      fields.forEach(function (field) {
        var input = $(field[0])
        if (input) input.addEventListener("input", function () {
          clearError(field)
          clearResult()
        })
      })
      toggleWeightUnit()
      toggleHeightUnit()
      form.addEventListener("submit", function (e) {
        e.preventDefault()
        clearErrors()
        var kg = null
        if (weightKgRadio.checked) {
          kg = readField(fields[0])
        } else {
          var pounds = readField(fields[1])
          if (pounds !== null) kg = pounds * 0.45359237
        }
        var heightCm = null
        if (heightCmRadio.checked) {
          heightCm = readField(fields[2])
        } else {
          var ft = readField(fields[3])
          var inches = readField(fields[4])
          if (ft !== null && inches !== null) heightCm = (ft * 12 + inches) * 2.54
        }
        if (kg === null || heightCm === null || !isFinite(heightCm) || heightCm <= 0) {
          clearResult()
          return
        }
        var meters = heightCm / 100
        var bmi = kg / (meters * meters)
        if (!isFinite(bmi) || bmi <= 0) {
          say("bmi-result", t("bmiCalcError"))
          return
        }
        var roundedBMI = Number(bmi.toFixed(1))
        var label = roundedBMI < 18.5 ? t("bmiUnder") :
          roundedBMI < 25 ? t("bmiNormal") :
          roundedBMI < 30 ? t("bmiOver") : t("bmiObese")
        say("bmi-result", t("bmiStrictResult", { bmi: roundedBMI.toFixed(1), label: label }) + " " + t("bmiDisclaimer"))
      })
      return
    }
    // Legacy path for other localized pages, whose UI is unchanged.
    var unit = $("bmi-unit")
    function toggle() {
      var metric = unit.value === "metric"
      $("bmi-metric").classList.toggle("hidden", !metric)
      $("bmi-imperial").classList.toggle("hidden", metric)
    }
    unit.addEventListener("change", toggle)
    toggle()
    form.addEventListener("submit", function (e) {
      e.preventDefault()
      var bmi = 0
      if (unit.value === "metric") {
        var kg = num("b-kg")
        var cm = num("b-cm")
        if (kg === null || cm === null || kg < 2 || kg > 500 || cm < 50 || cm > 300) {
          say("bmi-result", t("bmiInput"))
          return
        }
        bmi = kg / Math.pow(cm / 100, 2)
      } else {
        var lb = num("b-lb")
        var ft = num("b-ft")
        var inch = num("b-in") || 0
        if (lb === null || lb < 4 || lb > 1100 || ft === null || ft < 1 || ft > 9 || inch < 0 || inch >= 12) {
          say("bmi-result", t("bmiInputImp"))
          return
        }
        bmi = 703 * lb / Math.pow(ft * 12 + inch, 2)
      }
      var label = bmi < 18.5 ? t("bmiUnder") : bmi < 25 ? t("bmiNormal") : bmi < 30 ? t("bmiOver") : t("bmiObese")
      say("bmi-result", t("bmiResult", { bmi: bmi.toFixed(1), label: label }))
    })
  }

  function initProfit () {
    var form = $("pl-form")
    if (!form) return
    form.addEventListener("submit", function (e) {
      e.preventDefault()
      var cost = num("p-cost")
      var sell = num("p-sell")
      if (cost === null || sell === null || cost < 0 || sell < 0) {
        say("pl-result", t("profitEnter"))
        return
      }
      var diff = sell - cost
      var word = diff >= 0 ? t("profitWord") : t("lossWord")
      var amount = fmt(Math.abs(diff))
      if (cost === 0) {
        say("pl-result", word + ": " + amount + ". " + t("profitNA"))
        return
      }
      var pct = (diff / cost) * 100
      say("pl-result", word + ": " + amount + " (" + Math.abs(pct).toFixed(2) + " " + t("profitPct") + ").")
    })
  }

  function initAge () {
    var form = $("age-form")
    if (!form) return
    form.addEventListener("submit", function (e) {
      e.preventDefault()
      var value = $("a-dob").value
      if (!value) {
        say("age-result", t("ageEnter"))
        return
      }
      var parts = value.split("-").map(Number)
      var dob = new Date(parts[0], parts[1] - 1, parts[2])
      var now = new Date()
      var today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
      if (dob > today) {
        say("age-result", t("ageFuture"))
        return
      }
      var years = today.getFullYear() - dob.getFullYear()
      var months = today.getMonth() - dob.getMonth()
      var days = today.getDate() - dob.getDate()
      if (days < 0) {
        months -= 1
        days += new Date(today.getFullYear(), today.getMonth(), 0).getDate()
      }
      if (months < 0) {
        months += 12
        years -= 1
      }
      if (years > 150) {
        say("age-result", t("ageCheck"))
        return
      }
      var total = Math.floor((Date.UTC(today.getFullYear(), today.getMonth(), today.getDate()) - Date.UTC(parts[0], parts[1] - 1, parts[2])) / 86400000)
      say("age-result", t("ageResult", { y: years, m: months, d: days, t: fmt(total) }))
    })
  }

  function initDiscount () {
    var form = $("disc-form")
    if (!form) return
    form.addEventListener("submit", function (e) {
      e.preventDefault()
      var price = num("d-price")
      var pct = num("d-pct")
      if (price === null || pct === null || price < 0 || pct < 0 || pct > 100) {
        say("disc-result", t("discInput"))
        return
      }
      var saved = Math.round(price * pct) / 100
      var final = Math.round((price - saved) * 100) / 100
      say("disc-result", t("discResult", { saved: fmt(saved), final: fmt(final) }))
    })
  }

  function unitName (key) {
    return MSG[lang()].units[key]
  }

  function fillUnits () {
    var cat = $("u-cat").value
    var from = $("u-from")
    var to = $("u-to")
    from.innerHTML = ""
    to.innerHTML = ""
    UNITS[cat].keys.forEach(function (key) {
      var a = document.createElement("option")
      a.value = key
      a.textContent = unitName(key)
      from.appendChild(a)
      var b = document.createElement("option")
      b.value = key
      b.textContent = unitName(key)
      to.appendChild(b)
    })
    to.selectedIndex = 1
  }

  function toCelsius (v, unit) {
    if (unit === "C") return v
    if (unit === "F") return (v - 32) * 5 / 9
    return v - 273.15
  }

  function fromCelsius (c, unit) {
    if (unit === "C") return c
    if (unit === "F") return c * 9 / 5 + 32
    return c + 273.15
  }

  function initConverter () {
    var form = $("conv-form")
    if (!form) return
    $("u-cat").addEventListener("change", fillUnits)
    fillUnits()
    form.addEventListener("submit", function (e) {
      e.preventDefault()
      var cat = $("u-cat").value
      var v = num("u-val")
      var from = $("u-from").value
      var to = $("u-to").value
      if (v === null) {
        say("conv-result", t("convEnter"))
        return
      }
      if (cat === "temp") {
        var celsius = toCelsius(v, from)
        if (celsius < -273.1500001) {
          say("conv-result", t("convAbsoluteZero"))
          return
        }
        var converted = fromCelsius(celsius, to)
        say("conv-result", t("convResult", { v: fmt(v), from: unitName(from), out: converted.toFixed(2), to: unitName(to) }))
        return
      }
      if (v < 0) {
        say("conv-result", t("convNeg", { cat: MSG[lang()].cats[cat] }))
        return
      }
      var base = UNITS[cat].base
      var out = v * base[from] / base[to]
      var shown = Number(out.toPrecision(6)).toLocaleString(MSG[lang()].numeric, { maximumFractionDigits: 6 })
      say("conv-result", t("convResult", { v: fmt(v), from: unitName(from), out: shown, to: unitName(to) }))
    })
  }

  /* Standard calculator: recursive descent parser with parentheses. No eval, no Function constructor. */
  function evaluate (expr) {
    var tokens = expr.match(/(?:\d+(?:\.\d*)?|\.\d+)|[+\-*\/()]/g)
    if (!tokens) throw new Error("incomplete")
    var pos = 0

    function peek () {
      return tokens[pos]
    }

    function next () {
      pos += 1
      return tokens[pos - 1]
    }

    function factor () {
      var tok = next()
      if (tok === undefined) throw new Error("incomplete")
      if (tok === "-") return -factor()
      if (tok === "(") {
        var inner = sum()
        if (next() !== ")") throw new Error("incomplete")
        return inner
      }
      var n = Number(tok)
      if (!isFinite(n)) throw new Error("invalid")
      return n
    }

    function product () {
      var value = factor()
      while (peek() === "*" || peek() === "/") {
        var op = next()
        var right = factor()
        if (op === "/") {
          if (right === 0) throw new Error("divzero")
          value = value / right
        } else {
          value = value * right
        }
      }
      return value
    }

    function sum () {
      var value = product()
      while (peek() === "+" || peek() === "-") {
        var op = next()
        var right = product()
        value = op === "+" ? value + right : value - right
      }
      return value
    }

    var result = sum()
    if (pos !== tokens.length) throw new Error("incomplete")
    if (!isFinite(result)) throw new Error("invalid")
    return result
  }

  function evaluateScientific (expr, angleMode, ansValue) {
    var source = String(expr || "").replace(/\s+/g, "")
    if (!source) throw new Error("incomplete")
    if (source.length > 1000) throw new Error("invalid")
    var tokenPattern = /(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?|[A-Za-z]+|[+\-*\/^(),!%]/g
    var tokens = []
    var match
    var consumed = ""
    while ((match = tokenPattern.exec(source)) !== null) {
      tokens.push(match[0])
      consumed += match[0]
    }
    if (consumed !== source || !tokens.length || tokens.length > 256) throw new Error("invalid")
    var pos = 0
    function peek () { return tokens[pos] }
    function next () { return tokens[pos++] }
    function requireFinite (value) {
      if (!isFinite(value)) throw new Error("invalid")
      return value
    }
    function factorial (value) {
      if (!isFinite(value) || value < 0 || Math.floor(value) !== value || value > 170) throw new Error("domain")
      var out = 1
      for (var k = 2; k <= value; k += 1) out *= k
      return out
    }
    function choose (n, r, permutation) {
      if (!isFinite(n) || !isFinite(r) || Math.floor(n) !== n || Math.floor(r) !== r || n < 0 || r < 0 || r > n || n > 170) throw new Error("domain")
      var out = 1
      for (var k = 0; k < r; k += 1) out *= n - k
      return permutation ? out : out / factorial(r)
    }
    function callFunction (name, args) {
      var x = args[0]
      if (["mean", "median", "min", "max", "sum", "stdev", "stdevp", "var", "varp", "gcd", "lcm"].indexOf(name) !== -1) {
        if (!args.length || (["stdev", "var"].indexOf(name) !== -1 && args.length < 2)) throw new Error("domain")
        var values = args.slice()
        if (name === "sum") return values.reduce(function (a, b) { return a + b }, 0)
        if (name === "mean") return values.reduce(function (a, b) { return a + b }, 0) / values.length
        if (name === "min") return Math.min.apply(Math, values)
        if (name === "max") return Math.max.apply(Math, values)
        if (name === "median") {
          values.sort(function (a, b) { return a - b })
          var mid = Math.floor(values.length / 2)
          return values.length % 2 ? values[mid] : (values[mid - 1] + values[mid]) / 2
        }
        if (name === "gcd" || name === "lcm") {
          var resultInt = Math.abs(values[0])
          for (var gi = 0; gi < values.length; gi += 1) {
            if (Math.floor(values[gi]) !== values[gi] || Math.abs(values[gi]) > 1e9) throw new Error("domain")
          }
          for (var g = 1; g < values.length; g += 1) {
            var aInt = resultInt, bInt = Math.abs(values[g])
            while (bInt) { var tempInt = bInt; bInt = aInt % bInt; aInt = tempInt }
            resultInt = name === "gcd" ? aInt : (resultInt === 0 || values[g] === 0 ? 0 : Math.abs(resultInt * values[g]) / aInt)
          }
          return resultInt
        }
        var avg = values.reduce(function (a, b) { return a + b }, 0) / values.length
        var squares = values.reduce(function (total, n) { return total + Math.pow(n - avg, 2) }, 0)
        var divisor = (name === "stdev" || name === "var") ? values.length - 1 : values.length
        var variance = squares / divisor
        return (name === "stdev" || name === "stdevp") ? Math.sqrt(variance) : variance
      }
      if (name === "log" && args.length === 2) {
        if (args[0] <= 0 || args[1] <= 0 || args[1] === 1) throw new Error("domain")
        return requireFinite(Math.log(args[0]) / Math.log(args[1]))
      }
      if (name === "root") {
        if (args.length !== 2 || args[0] === 0) throw new Error("domain")
        var degree = args[0], radicand = args[1]
        if (radicand < 0 && (Math.floor(degree) !== degree || Math.abs(degree % 2) !== 1)) throw new Error("domain")
        return requireFinite(radicand < 0 ? -Math.pow(-radicand, 1 / degree) : Math.pow(radicand, 1 / degree))
      }
      if (name === "npr" || name === "ncr" || name === "mod") {
        if (args.length !== 2) throw new Error("domain")
        if (name === "npr") return choose(args[0], args[1], true)
        if (name === "ncr") return choose(args[0], args[1], false)
        if (args[1] === 0) throw new Error("divzero")
        return args[0] % args[1]
      }
      if (args.length !== 1) throw new Error("domain")
      var radians = angleMode === "DEG" ? x * Math.PI / 180 : x
      var value
      switch (name) {
        case "sin": value = Math.sin(radians); break
        case "cos": value = Math.cos(radians); break
        case "tan":
          if (Math.abs(Math.cos(radians)) < 1e-12) throw new Error("domain")
          value = Math.tan(radians); break
        case "asin": case "arcsin":
          if (x < -1 || x > 1) throw new Error("domain")
          value = Math.asin(x); if (angleMode === "DEG") value *= 180 / Math.PI; break
        case "acos": case "arccos":
          if (x < -1 || x > 1) throw new Error("domain")
          value = Math.acos(x); if (angleMode === "DEG") value *= 180 / Math.PI; break
        case "atan": case "arctan":
          value = Math.atan(x); if (angleMode === "DEG") value *= 180 / Math.PI; break
        case "acsc": if (Math.abs(x) < 1 || x === 0) throw new Error("domain"); value = Math.asin(1 / x); if (angleMode === "DEG") value *= 180 / Math.PI; break
        case "asec": if (Math.abs(x) < 1) throw new Error("domain"); value = Math.acos(1 / x); if (angleMode === "DEG") value *= 180 / Math.PI; break
        case "acot": value = Math.atan2(1, x); if (angleMode === "DEG") value *= 180 / Math.PI; break
        case "sinh": value = Math.sinh(x); break
        case "cosh": value = Math.cosh(x); break
        case "tanh": value = Math.tanh(x); break
        case "csch": if (x === 0) throw new Error("domain"); value = 1 / Math.sinh(x); break
        case "sech": value = 1 / Math.cosh(x); break
        case "coth": if (x === 0) throw new Error("domain"); value = 1 / Math.tanh(x); break
        case "asinh": value = Math.asinh(x); break
        case "acosh": if (x < 1) throw new Error("domain"); value = Math.acosh(x); break
        case "atanh": if (x <= -1 || x >= 1) throw new Error("domain"); value = Math.atanh(x); break
        case "sqrt": if (x < 0) throw new Error("domain"); value = Math.sqrt(x); break
        case "cbrt": value = Math.cbrt(x); break
        case "abs": value = Math.abs(x); break
        case "log": if (x <= 0) throw new Error("domain"); value = Math.log(x) / Math.LN10; break
        case "ln": if (x <= 0) throw new Error("domain"); value = Math.log(x); break
        case "exp": value = Math.exp(x); break
        case "floor": value = Math.floor(x); break
        case "ceil": value = Math.ceil(x); break
        case "round": value = Math.round(x); break
        case "fact": case "factorial": value = factorial(x); break
        case "sec": if (Math.abs(Math.cos(radians)) < 1e-12) throw new Error("domain"); value = 1 / Math.cos(radians); break
        case "csc": if (Math.abs(Math.sin(radians)) < 1e-12) throw new Error("domain"); value = 1 / Math.sin(radians); break
        case "cot": if (Math.abs(Math.sin(radians)) < 1e-12) throw new Error("domain"); value = 1 / Math.tan(radians); break
        default: throw new Error("invalid")
      }
      return requireFinite(value)
    }
    function primary () {
      var tok = next()
      if (tok === undefined) throw new Error("incomplete")
      if (tok === "(") {
        var inner = sum()
        if (next() !== ")") throw new Error("incomplete")
        return inner
      }
      if (/^(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$/.test(tok)) return requireFinite(Number(tok))
      if (/^[A-Za-z]+$/.test(tok)) {
        var name = tok.toLowerCase()
        if (peek() === "(") {
          next()
          var args = []
          if (peek() !== ")") {
            args.push(sum())
            while (peek() === ",") { next(); args.push(sum()) }
          }
          if (next() !== ")") throw new Error("incomplete")
          return requireFinite(callFunction(name, args))
        }
        if (name === "pi") return Math.PI
        if (name === "e") return Math.E
        if (name === "ans") return requireFinite(ansValue)
        throw new Error("invalid")
      }
      throw new Error("invalid")
    }
    function postfix () {
      var value = primary()
      while (peek() === "!" || peek() === "%") {
        var op = next()
        value = op === "!" ? factorial(value) : value / 100
      }
      return requireFinite(value)
    }
    function power () {
      var value = postfix()
      if (peek() === "^") {
        next()
        value = Math.pow(value, unary())
      }
      return requireFinite(value)
    }
    function unary () {
      if (peek() === "+") { next(); return unary() }
      if (peek() === "-") { next(); return -unary() }
      return power()
    }
    function product () {
      var value = unary()
      while (peek() === "*" || peek() === "/") {
        var op = next()
        var right = unary()
        if (op === "/" && right === 0) throw new Error("divzero")
        value = op === "*" ? value * right : value / right
        requireFinite(value)
      }
      return value
    }
    function sum () {
      var value = product()
      while (peek() === "+" || peek() === "-") {
        var op = next()
        var right = product()
        value = op === "+" ? value + right : value - right
        requireFinite(value)
      }
      return value
    }
    var result = sum()
    if (pos !== tokens.length) throw new Error("incomplete")
    return requireFinite(result)
  }

  function initCalculator () {
    var pad = $("calc-pad")
    if (!pad) return
    var display = $("calc-display")
    var sciPad = $("scientific-pad")
    var modeToggle = $("calc-mode-toggle")
    var historyEl = $("calc-history")
    var expr = ""
    var scientific = false
    var angleMode = "DEG"
    var ansValue = 0
    var memory = 0
    var history = []
    if (sciPad) sciPad.hidden = true
    if (modeToggle) {
      modeToggle.textContent = t("calcScientificMode")
      modeToggle.setAttribute("aria-pressed", "false")
    }
    function format (value) {
      if (!isFinite(value)) throw new Error("invalid")
      var rounded = Math.abs(value) < 1e12 ? Math.round(value * 1e12) / 1e12 : value
      return String(rounded)
    }
    function render (text) {
      display.textContent = text === "" ? "0" : text.replace(/\*/g, "×").replace(/\//g, "÷").replace(/-/g, "−")
    }
    function errorText (err) {
      if (err.message === "divzero") return t("calcDiv")
      if (err.message === "domain") return t("calcDomainError")
      if (err.message === "incomplete") return t("calcError")
      return t("calcError")
    }
    function paintHistory () {
      if (!historyEl) return
      historyEl.textContent = history.slice(-5).reverse().join("  ·  ")
    }
    function clear () {
      expr = ""
      render("")
    }
    function press (key) {
      if (key === "angle-toggle") {
        angleMode = angleMode === "DEG" ? "RAD" : "DEG"
        var angleBtn = $("calc-angle-toggle")
        if (angleBtn) {
          angleBtn.textContent = angleMode
          angleBtn.setAttribute("aria-pressed", angleMode === "RAD" ? "true" : "false")
        }
        return
      }
      if (key === "C") { clear(); return }
      if (key === "BS") { expr = expr.slice(0, -1); render(expr); return }
      if (key === "M+") {
        try { memory = scientific ? evaluateScientific(expr, angleMode, ansValue) : evaluate(expr) } catch (err) { return }
        return
      }
      if (key === "MR") { expr += format(memory); render(expr); return }
      if (key === "MC") { memory = 0; return }
      if (key === "Ans") { expr += "ans"; render(expr); return }
      if (key === "pi" || key === "e") { expr += key; render(expr); return }
      if ((key === "square" || key === "cube") && scientific) { expr += key === "square" ? "^2" : "^3"; render(expr); return }
      if (key === "tenpow" && scientific) { expr += "10^("; render(expr); return }
      if (key === "reciprocal" && scientific) { expr += "1/("; render(expr); return }
      if (key === "sqrt" && !scientific) {
        if (expr.trim() === "") { display.textContent = t("calcNeedValue"); return }
        try {
          var radicand = evaluate(expr)
          if (radicand < 0) { expr = ""; display.textContent = t("calcSqrtNegative"); return }
          expr = format(Math.sqrt(radicand)); render(expr)
        } catch (err) { expr = ""; display.textContent = errorText(err) }
        return
      }
      if (key === "sqrt" || key === "cbrt" || key === "sin" || key === "cos" || key === "tan" ||
          key === "asin" || key === "acos" || key === "atan" || key === "sinh" || key === "cosh" ||
          key === "tanh" || key === "csch" || key === "sech" || key === "coth" || key === "asinh" || key === "acosh" || key === "atanh" || key === "acsc" || key === "asec" || key === "acot" || key === "root" || key === "abs" ||
          key === "log" || key === "ln" || key === "exp" || key === "floor" || key === "ceil" ||
          key === "round" || key === "sec" || key === "csc" || key === "cot" || key === "nPr" ||
          key === "nCr" || key === "mod" || key === "mean" || key === "median" || key === "min" || key === "max" || key === "sum" || key === "stdev" || key === "stdevp" || key === "var" || key === "varp" || key === "gcd" || key === "lcm") {
        expr += key + "("
        render(expr)
        return
      }
      if (key === "=") {
        try {
          var value = scientific ? evaluateScientific(expr, angleMode, ansValue) : evaluate(expr)
          ansValue = value
          var result = format(value)
          history.push(expr + " = " + result)
          if (history.length > 20) history.shift()
          paintHistory()
          expr = result
          render(expr)
        } catch (err) {
          display.textContent = errorText(err)
          expr = ""
        }
        return
      }
      if (key === "%") {
        if (scientific) { expr += "%"; render(expr) }
        else {
          expr = expr.replace(/(\d+\.?\d*)$/, function (m) { return String(Number(m) / 100) })
          render(expr)
        }
        return
      }
      if (scientific && key === "-" && /[+*\/^]$/.test(expr)) { expr += key; render(expr); return }
      if (/^[+\-*\/^]$/.test(key)) {
        if (expr === "" && key !== "-") return
        if (/[+\-*\/^]$/.test(expr) && expr.length > 1) expr = expr.slice(0, -1)
        expr += key
        render(expr)
        return
      }
      if (key === "!" || key === "(" || key === ")" || key === ",") {
        expr += key
        render(expr)
        return
      }
      if (key === "0" && expr === "") { expr = "0"; render(expr); return }
      expr += key
      render(expr)
    }
    pad.addEventListener("click", function (e) {
      var btn = e.target.closest("button")
      if (!btn) return
      press(btn.getAttribute("data-key"))
    })
    if (sciPad) sciPad.addEventListener("click", function (e) {
      var btn = e.target.closest("button")
      if (!btn) return
      press(btn.getAttribute("data-key"))
    })
    document.addEventListener("keydown", function (e) {
      var target = e.target || {}
      var tag = String(target.tagName || "").toLowerCase()
      if (tag === "input" || tag === "textarea" || tag === "select" || target.isContentEditable) return
      if (e.key === "Enter" || e.key === "=") { press("="); e.preventDefault(); return }
      if (e.key === "Backspace") { press("BS"); e.preventDefault(); return }
      if (e.key === "Escape") { press("C"); e.preventDefault(); return }
      if (/^[0-9.]$/.test(e.key) || "+-*/^(),!%".indexOf(e.key) !== -1) { press(e.key); e.preventDefault() }
    })
    if (modeToggle) modeToggle.addEventListener("click", function () {
      scientific = !scientific
      expr = ""
      render("")
      if (sciPad) sciPad.hidden = !scientific
      pad.hidden = scientific
      modeToggle.textContent = scientific ? t("calcStandardMode") : t("calcScientificMode")
      modeToggle.setAttribute("aria-pressed", scientific ? "true" : "false")
      var angleBtn = $("calc-angle-toggle")
      if (angleBtn) angleBtn.textContent = angleMode
    })
  }

  function initTasbih () {
    var countEl = $("t-count")
    if (!countEl) return
    var target = $("t-target")
    var customTarget = $("t-custom-target")
    var customTargetWrap = $("t-custom-target-wrap")
    var targetError = $("t-target-error")
    var phrase = $("t-phrase")
    var customPhrase = $("t-custom-phrase")
    var phraseError = $("t-phrase-error")
    var progress = $("t-progress")
    var lifetimeEl = $("t-lifetime")
    var storageNote = $("t-storage-note")
    var count = 0
    var lifetime = 0
    var phraseValue = "SubhanAllah"
    var storageAvailable = true
    var lastTargetReached = false

    function readStored (key) {
      try {
        return window.localStorage.getItem(key)
      } catch (err) {
        storageAvailable = false
        return null
      }
    }
    function writeStored (key, value) {
      try {
        window.localStorage.setItem(key, String(value))
      } catch (err) {
        storageAvailable = false
      }
    }
    function showStorageState () {
      if (storageNote) storageNote.hidden = storageAvailable
    }
    function activePhrase () {
      if (phrase.value === "custom") return customPhrase.value.trim()
      return phrase.value
    }
    function activeTarget () {
      if (target.value !== "custom") return Number(target.value)
      var raw = customTarget.value.trim()
      if (!/^[0-9]+$/.test(raw)) return null
      var n = Number(raw)
      return Number.isSafeInteger(n) && n >= 1 && n <= 10000 ? n : null
    }
    function saveCount () { writeStored("tasbih.count", count); showStorageState() }
    function savePhrase () { writeStored("tasbih.phrase", phrase.value === "custom" ? "custom:" + customPhrase.value.trim() : phrase.value); showStorageState() }
    function saveLifetime () { writeStored("tasbih.lifetime", lifetime); showStorageState() }
    function paint (allowVibration) {
      countEl.textContent = String(count)
      if (lifetimeEl) lifetimeEl.textContent = String(lifetime)
      var goal = activeTarget()
      if (target.value === "custom" && goal === null) {
        targetError.textContent = "Enter a whole number from 1 to 10,000."
        progress.textContent = "Set a valid target to see progress."
        lastTargetReached = false
        return
      }
      targetError.textContent = ""
      if (goal !== null && count >= goal) {
        progress.textContent = "Target of " + goal + " reached."
        if (allowVibration && !lastTargetReached && typeof navigator !== "undefined" && typeof navigator.vibrate === "function") {
          try { navigator.vibrate(80) } catch (err) { /* vibration is optional */ }
        }
        lastTargetReached = true
      } else {
        progress.textContent = goal === null ? "Set a valid target to see progress." : (goal - count) + " to go for a target of " + goal + "."
        lastTargetReached = false
      }
    }
    function increment () {
      var goal = activeTarget()
      if (goal === null) {
        targetError.textContent = "Enter a whole number from 1 to 10,000."
        customTarget.focus()
        return
      }
      if (phrase.value === "custom" && !activePhrase()) {
        phraseError.textContent = "Enter a custom phrase up to 40 characters."
        customPhrase.focus()
        return
      }
      phraseError.textContent = ""
      count += 1
      lifetime += 1
      saveCount()
      saveLifetime()
      paint(true)
    }
    var storedCount = readStored("tasbih.count")
    var storedPhrase = readStored("tasbih.phrase")
    var storedLifetime = readStored("tasbih.lifetime")
    if (storedCount !== null && /^[0-9]+$/.test(storedCount) && Number.isSafeInteger(Number(storedCount))) count = Number(storedCount)
    if (storedPhrase !== null && ["SubhanAllah", "Alhamdulillah", "Allahu Akbar", "Astaghfirullah", "La ilaha illallah"].indexOf(storedPhrase) !== -1) phraseValue = storedPhrase
    else if (storedPhrase !== null && storedPhrase.indexOf("custom:") === 0) phraseValue = storedPhrase.slice(7)
    if (storedLifetime !== null && /^[0-9]+$/.test(storedLifetime) && Number.isSafeInteger(Number(storedLifetime))) lifetime = Number(storedLifetime)
    phrase.value = storedPhrase !== null && storedPhrase.indexOf("custom:") === 0 ? "custom" : phraseValue
    if (phrase.value === "custom") customPhrase.value = phraseValue
    customTargetWrap.hidden = target.value !== "custom"
    customPhrase.disabled = phrase.value !== "custom"
    phrase.addEventListener("change", function () {
      customPhrase.disabled = phrase.value !== "custom"
      if (phrase.value === "custom") customPhrase.focus()
      phraseError.textContent = ""
      phraseValue = phrase.value === "custom" ? customPhrase.value.trim() : phrase.value
      savePhrase()
      paint()
    })
    customPhrase.addEventListener("input", function () {
      if (customPhrase.value.length > 40) customPhrase.value = customPhrase.value.slice(0, 40)
      phraseError.textContent = ""
      if (phrase.value === "custom") {
        phraseValue = customPhrase.value.trim()
        savePhrase()
      }
      showStorageState()
    })
    target.addEventListener("change", function () {
      customTargetWrap.hidden = target.value !== "custom"
      targetError.textContent = ""
      lastTargetReached = false
      paint()
    })
    customTarget.addEventListener("input", function () {
      targetError.textContent = ""
      lastTargetReached = false
      paint()
    })
    $("t-tap").addEventListener("click", increment)
    $("t-undo").addEventListener("click", function () {
      if (count > 0) count -= 1
      saveCount()
      paint()
    })
    $("t-reset").addEventListener("click", function () {
      if (!window.confirm("Reset the current count to zero?")) return
      count = 0
      lastTargetReached = false
      saveCount()
      paint()
    })
    document.addEventListener("keydown", function (event) {
      if (event.defaultPrevented || event.ctrlKey || event.metaKey || event.altKey) return
      var el = event.target
      if (el && (el.isContentEditable || /^(INPUT|TEXTAREA|SELECT|BUTTON)$/.test(el.tagName))) return
      if (event.code === "Space" || event.key === "Enter") {
        event.preventDefault()
        increment()
      }
    })
    showStorageState()
    paint()
  }

  function initStopwatch () {
    var display = $("sw-display")
    if (!display) return
    var startedAt = 0
    var elapsed = 0
    var timer = null
    function pad (n) {
      return String(n).padStart(2, "0")
    }
    function paint () {
      var ms = elapsed
      var h = Math.floor(ms / 3600000)
      var m = Math.floor(ms / 60000) % 60
      var s = Math.floor(ms / 1000) % 60
      var cs = Math.floor(ms / 10) % 100
      display.textContent = pad(h) + ":" + pad(m) + ":" + pad(s) + "." + pad(cs)
    }
    function tick () {
      var now = performance.now()
      elapsed += now - startedAt
      startedAt = now
      paint()
    }
    $("sw-start").addEventListener("click", function () {
      if (timer) return
      startedAt = performance.now()
      timer = setInterval(tick, 50)
    })
    $("sw-stop").addEventListener("click", function () {
      if (!timer) return
      tick()
      clearInterval(timer)
      timer = null
    })
    $("sw-reset").addEventListener("click", function () {
      if (timer) clearInterval(timer)
      timer = null
      elapsed = 0
      paint()
    })
    paint()
  }

  /* Dark mode: the class is set before first paint in the page head. This only switches it and remembers the choice. */
  function initTheme () {
    var btn = $("theme-toggle")
    if (!btn) return
    function isDark () {
      return document.documentElement.classList.contains("dark")
    }
    function label () {
      btn.textContent = isDark() ? t("themeLight") : t("themeDark")
      btn.setAttribute("aria-pressed", isDark() ? "true" : "false")
    }
    btn.addEventListener("click", function () {
      var dark = !isDark()
      document.documentElement.classList.toggle("dark", dark)
      try {
        window.localStorage.setItem("theme", dark ? "dark" : "light")
      } catch (err) {
        return
      }
      label()
    })
    label()
  }

  function initAds () {
    var slots = document.querySelectorAll(".adsbygoogle")
    if (!slots.length) return
    slots.forEach(function () {
      try {
        (window.adsbygoogle = window.adsbygoogle || []).push({})
      } catch (err) {
        return
      }
    })
  }

  document.addEventListener("DOMContentLoaded", function () {
    initTheme()
    initZakat()
    initBMI()
    initProfit()
    initAge()
    initDiscount()
    initConverter()
    initCalculator()
    initTasbih()
    initStopwatch()
    initAds()
  })
})()
