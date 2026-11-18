import hashlib
import html


def build_calorie_page(head, shell, write):
    """Generate the adult calorie calculator and its supporting SEO content."""
    path = "/calorie-calculator/"
    site = "https://calculateallinone.vercel.app"
    title = "Calorie Calculator: TDEE, BMR & Macros | CalculatesAll"
    description = (
        "Estimate adult maintenance calories, TDEE, resting energy and macros with "
        "Mifflin–St Jeor, Revised Harris–Benedict or Katch–McArdle."
    )

    sources = [
        (
            "Mifflin–St Jeor original research (1990)",
            "https://pubmed.ncbi.nlm.nih.gov/2305711/",
            "The original study developed a resting energy expenditure prediction equation from measurements in 498 healthy adults aged 19–78. It supports the Mifflin–St Jeor equation, not an individual measurement or guarantee.",
        ),
        (
            "Roza and Shizgal: Revised Harris–Benedict equation (1984)",
            "https://pubmed.ncbi.nlm.nih.gov/6741850/",
            "The 1984 paper reevaluated the Harris–Benedict equations using indirect calorimetry data. This page uses the revised male and female equations reported by Roza and Shizgal.",
        ),
        (
            "Cunningham: Body composition as a determinant of energy expenditure (1991)",
            "https://pubmed.ncbi.nlm.nih.gov/1957828/",
            "This peer-reviewed paper proposes the generalized resting-energy equation 370 + 21.6 × fat-free mass in kilograms, the equation commonly used as Katch–McArdle. The result depends on the accuracy of the body-fat estimate used to derive fat-free mass.",
        ),
        (
            "National Academies: Dietary Reference Intakes for Energy (2023)",
            "https://www.ncbi.nlm.nih.gov/books/NBK591031/",
            "Provides reference context for total energy expenditure, resting energy expenditure, physical activity and variation between individuals. The consumer activity factors on this page are not National Academies equations.",
        ),
        (
            "FAO/WHO/UNU: Human Energy Requirements",
            "https://www.fao.org/4/y5686e/y5686e00.htm",
            "Explains human energy requirements and physical activity level. Its formal PAL framework is different from the simplified activity multipliers used by this calculator.",
        ),
        (
            "NIDDK: About the Body Weight Planner",
            "https://www.niddk.nih.gov/health-information/weight-management/body-weight-planner",
            "NIDDK states that its adult Body Weight Planner is not intended for people under 18 or for people who are pregnant or breastfeeding. This calculator is also not intended for pregnancy or breastfeeding.",
        ),
        (
            "Mayo Clinic: Calorie Calculator",
            "https://www.mayoclinic.org/healthy-lifestyle/weight-loss/in-depth/calorie-calculator/itt-20402304",
            "Provides consumer guidance about estimating calorie needs. Prediction equations can differ from an individual's actual energy requirements, particularly where health or activity circumstances are not represented by the inputs.",
        ),
    ]

    faq = [
        (
            "How many calories do I need each day?",
            "There is no single calorie number that fits every adult. Your estimated daily energy needs depend on age, body size, the equation used and your usual activity. Enter your own measurements to see an estimate, then treat it as a starting point rather than a measured requirement or personal diet instruction.",
        ),
        (
            "What are maintenance calories?",
            "Maintenance calories are an estimate of the daily energy intake associated with keeping body weight broadly stable over time. This calculator estimates maintenance by multiplying a resting-energy estimate by an activity factor. Real weight trends are affected by water, digestion, illness, medication and other factors, so a calculated number is not a guarantee.",
        ),
        (
            "What does TDEE mean?",
            "TDEE means total daily energy expenditure: the energy your body uses across a full day. It includes resting energy expenditure, the thermic effect of food and physical activity. This calculator approximates TDEE by multiplying a resting estimate by a selected activity factor. It does not measure every part of daily energy expenditure.",
        ),
        (
            "What is BMR, and is it the same as RMR or REE?",
            "BMR means basal metabolic rate. RMR means resting metabolic rate, and REE means resting energy expenditure. They describe related resting-energy concepts but are measured under different conditions and are not always interchangeable. The selected prediction equation estimates resting energy. It is not a laboratory measurement of your BMR.",
        ),
        (
            "Which calorie formula should I choose?",
            "Mifflin–St Jeor is the default and recommended starting option for this general adult calculator. Revised Harris–Benedict is another established prediction equation. Katch–McArdle uses estimated lean body mass and therefore requires a body-fat percentage. Katch–McArdle can be especially sensitive to an inaccurate body-fat estimate. Different equations can give different results for the same person.",
        ),
        (
            "What is the Mifflin–St Jeor equation?",
            "For the male coefficient, the equation is 10 × weight in kg + 6.25 × height in cm − 5 × age + 5. For the female coefficient, use the same weight, height and age terms, then subtract 161 instead of adding 5. The original study measured resting energy expenditure in healthy adults aged 19–78. This is a prediction equation, not a measurement.",
        ),
        (
            "What is the Revised Harris–Benedict equation?",
            "The revised male equation is 88.362 + 13.397 × weight in kg + 4.799 × height in cm − 5.677 × age. The revised female equation is 447.593 + 9.247 × weight in kg + 3.098 × height in cm − 4.330 × age. These are the Roza and Shizgal revisions published in 1984, not the original 1919 coefficients.",
        ),
        (
            "How does the Katch–McArdle formula work?",
            "Katch–McArdle estimates resting metabolic rate as 370 + 21.6 × lean body mass in kilograms. Lean body mass is estimated as body weight × (1 − body-fat percentage ÷ 100). Because the calculation depends on body-fat percentage, an inaccurate body-fat reading can materially change the result. The formula does not independently verify body composition.",
        ),
        (
            "What activity level should I select?",
            "Choose the description that best represents your usual full-day movement, including work, walking, household activity and planned exercise. Sedentary means mostly seated with little planned movement. Light means some walking or light exercise. Moderate means regular moderate exercise. Very active means frequent hard exercise or a physically demanding job. Extra active means very demanding daily work or training. These multipliers are simplified assumptions, not measured physical activity levels.",
        ),
        (
            "Should I add exercise calories separately?",
            "Usually not when your selected activity factor already represents your exercise and daily movement. Adding exercise calories a second time can count the same activity twice. The activity factor is an estimate, so it may still differ from your actual routine.",
        ),
        (
            "What is a calorie deficit?",
            "A calorie deficit means energy intake is below energy expenditure over a period of time. The −300 and −500 kcal figures shown after calculation are simple arithmetic comparisons with estimated maintenance. They are not individualized prescriptions, a recommendation that every adult should lose weight, or a promise of a particular rate of change.",
        ),
        (
            "What is a calorie surplus?",
            "A calorie surplus means energy intake is above energy expenditure over a period of time. The +250 kcal figure is an arithmetic comparison with estimated maintenance, not a personalized muscle-gain or weight-gain prescription. Results vary and no outcome is guaranteed.",
        ),
        (
            "Why can two calorie calculators give different results?",
            "Calculators may use different equations, body-composition inputs, activity factors, unit conversions, rounding rules and reference populations. Some estimate resting energy while others use different methods to estimate total daily energy expenditure. Compare the formula and assumptions as well as the final number.",
        ),
        (
            "Can I use this calculator during pregnancy or breastfeeding?",
            "No. This calculator is for adults aged 18 or older who are not pregnant or breastfeeding. Pregnancy and lactation change energy needs and require context that this general calculator does not collect. Speak with a qualified healthcare professional for individualized guidance. Do not use the deficit, surplus or macro examples on this page as pregnancy or breastfeeding advice.",
        ),
        (
            "Can teenagers use this calculator?",
            "No. This calculator is intended for adults aged 18 or older only. Children and teenagers have different growth-related energy needs and should not use these adult equations for dietary decisions.",
        ),
        (
            "Can I use the results if I have diabetes or another medical condition?",
            "This is not a clinical calculator and it does not account for diagnoses, medicines, treatment, recovery, eating-disorder history or other individual health factors. If you have diabetes or another medical condition, discuss energy and nutrition decisions with your healthcare professional or registered dietitian.",
        ),
        (
            "Does a lower calorie number guarantee weight loss?",
            "No. The figures are estimates and do not guarantee weight loss, weight gain, muscle gain or a particular timeline. Body-weight changes are influenced by many factors, and the calculation is not a dynamic body-weight model.",
        ),
        (
            "What does the macro split mean?",
            "The example maintenance split allocates 30% of estimated maintenance calories to protein, 40% to carbohydrates and 30% to fat. Grams are calculated using 4 kcal per gram for protein and carbohydrates and 9 kcal per gram for fat. This is a simple illustrative split, not a universally optimal or medically tailored nutrition plan.",
        ),
        (
            "Are my measurements sent to a server?",
            "The calculator performs its arithmetic in your browser. Its calculation code does not send the entered age, weight, height, body-fat percentage or result to a calculation API, add them to the page URL or save them in browser storage. The website host and third-party resources may still process ordinary technical request data as described in the Privacy Policy.",
        ),
        (
            "Is the resting estimate a minimum safe calorie intake?",
            "No. REE is not a universal minimum safe calorie intake. A resting-energy estimate is not a nutritional requirement or a personal calorie limit. Do not use it to set a restrictive diet or make medical decisions.",
        ),
        (
            "Is this calculator medical advice or medically reviewed?",
            "No. It is an educational estimation tool, not medical advice, diagnosis or treatment. This calculator has not been medically reviewed. The linked sources support the named equations and general context; they do not approve, certify or endorse this website.",
        ),
        (
            "Why are results shown to one decimal place?",
            "The formulas calculate using the entered values and keep full precision during the calculation. Results are rounded to one decimal place for display. Other calculators may round at a different stage, which can create small differences.",
        ),
    ]

    input_class = "w-full min-w-0 rounded-lg border border-stone-400 bg-white px-3 py-2 text-base text-stone-900 min-h-[44px] dark:bg-stone-950 dark:text-white"
    compact_input_class = input_class.replace("px-3", "px-1").replace("text-base", "text-sm")
    label_class = "mb-1 block text-sm font-medium text-stone-800 dark:text-stone-200"
    body = (
        '<nav aria-label="Breadcrumb" class="mb-3 text-sm text-stone-700 dark:text-stone-300">'
        '<ol class="flex flex-wrap items-center gap-2"><li><a class="underline text-sky-800 dark:text-sky-300" href="/">Home</a></li>'
        '<li aria-hidden="true">/</li><li><a class="underline text-sky-800 dark:text-sky-300" href="/health/">Health</a></li>'
        '<li aria-hidden="true">/</li><li aria-current="page">Calorie Calculator</li></ol></nav>'
        '<header class="mb-4"><p class="text-xs font-bold uppercase tracking-wide text-sky-800 dark:text-sky-300">Adult calorie estimate</p>'
        '<h1 class="mt-1 text-2xl font-bold text-stone-950 dark:text-white">Calorie Calculator</h1>'
        '<p class="mt-2 text-sm leading-5 text-stone-700 dark:text-stone-300">Estimate adult maintenance calories (TDEE), resting energy and a simple macro split with three established formulas.</p></header>'
        '<section class="rounded-xl border border-stone-300 bg-white p-3 shadow-sm dark:border-stone-700 dark:bg-stone-900 sm:p-5">'
        '<h2 id="calorie-form-title" class="sr-only">Calculate your daily calorie estimate</h2>'
        ''
        '<form id="calorie-form" aria-labelledby="calorie-form-title" novalidate class="mt-2 grid grid-cols-2 gap-2 sm:gap-3">'
        '<div class="min-w-0"><label for="cal-age" class="' + label_class + '">Age (years)</label>'
        '<input id="cal-age" type="number" min="18" max="120" step="1" inputmode="numeric" autocomplete="off" placeholder="e.g. 30" class="' + input_class + '"></div>'
        '<div class="min-w-0"><label for="cal-formula" class="' + label_class + '">Calculation formula</label>'
        '<select id="cal-formula" class="' + input_class + '"><option value="mifflin" selected>Mifflin–St Jeor (recommended)</option><option value="harris-benedict">Revised Harris–Benedict</option><option value="katch-mcardle">Katch–McArdle (requires body fat %)</option></select></div>'
        '<div class="min-w-0"><label for="cal-coefficient" class="' + label_class + '">Equation coefficient</label>'
        '<select id="cal-coefficient" class="' + input_class + '"><option value="">Choose coefficient</option><option value="male">Male coefficient</option><option value="female">Female coefficient</option></select>'
        '<p class="mt-1 text-xs leading-5 text-stone-600 dark:text-stone-400">Required for Mifflin–St Jeor and Revised Harris–Benedict. Katch–McArdle does not use this input.</p></div>'
        '<div class="min-w-0"><label for="cal-activity" class="' + label_class + '">Activity level</label>'
        '<select id="cal-activity" class="' + input_class + '"><option value="">Choose activity</option><option value="sedentary">Sedentary</option><option value="light">Light activity</option><option value="moderate">Moderate activity</option><option value="very_active">Very active</option><option value="extra_active">Extra active</option></select></div>'
        '<div class="min-w-0"><label for="cal-weight" class="' + label_class + '">Weight</label>'
        '<div class="grid grid-cols-[minmax(0,1fr)_3.5rem] gap-1"><input id="cal-weight" type="number" min="0" step="any" inputmode="decimal" placeholder="e.g. 70" class="' + compact_input_class + '">'
        '<select id="cal-weight-unit" aria-label="Weight unit" class="' + compact_input_class + '"><option value="kg">kg</option><option value="lb">lb</option></select></div></div>'
        '<div class="min-w-0"><label id="cal-height-label" for="cal-height" class="' + label_class + '">Height</label>'
        '<div class="grid grid-cols-[minmax(0,1fr)_3.5rem] gap-1"><div id="cal-height-metric"><input id="cal-height" type="number" min="0" step="any" inputmode="decimal" placeholder="e.g. 175" class="' + compact_input_class + '"></div>'
        '<div id="cal-height-imperial" class="grid grid-cols-2 gap-1" hidden><input id="cal-height-ft" type="number" min="3" max="8" step="1" inputmode="numeric" aria-label="Height in feet" placeholder="ft" disabled class="' + compact_input_class + '">'
        '<input id="cal-height-in" type="number" min="0" max="11.99" step="any" inputmode="decimal" aria-label="Remaining height in inches" placeholder="in" disabled class="' + compact_input_class + '"></div>'
        '<select id="cal-height-unit" aria-label="Height unit" class="' + compact_input_class + '"><option value="cm">cm</option><option value="ft-in">ft/in</option></select></div></div>'
        '<div id="cal-body-fat-field" class="col-span-2 min-w-0" hidden><label for="cal-body-fat" class="' + label_class + '">Body-fat percentage (%)</label>'
        '<input id="cal-body-fat" type="number" min="3" max="70" step="any" inputmode="decimal" placeholder="e.g. 20" disabled class="' + input_class + '">'
        '<p class="mt-1 text-xs leading-5 text-stone-600 dark:text-stone-400">Used only by Katch–McArdle. Enter a reasonably measured estimate, not a guess.</p></div>'
        '<div class="col-span-2 flex flex-wrap gap-2 pt-1"><button id="cal-calculate" type="button" class="min-h-[44px] flex-1 rounded-lg bg-sky-800 px-4 py-2 font-semibold text-white hover:bg-sky-900 focus:outline-none focus:ring-2 focus:ring-sky-500">Calculate calories</button>'
        '<button id="cal-reset" type="button" class="min-h-[44px] rounded-lg border border-stone-400 px-4 py-2 font-semibold text-stone-800 hover:bg-stone-100 dark:border-stone-600 dark:text-stone-100 dark:hover:bg-stone-800">Reset</button></div>'
        '<p id="calorie-error" class="col-span-2 empty:hidden text-sm font-medium text-red-700 dark:text-red-300" role="alert" aria-live="assertive"></p>'
        '<div id="calorie-result" class="col-span-2 mt-1 rounded-lg border border-sky-300 bg-sky-50 p-3 text-stone-950 dark:border-sky-800 dark:bg-sky-950/40 dark:text-white sm:p-4" role="status" aria-live="polite" hidden></div>'
        '</form></section>'
        '<aside role="note" class="mt-4 rounded-lg border border-amber-400 bg-amber-50 p-3 text-sm leading-6 text-amber-950 dark:border-amber-800 dark:bg-amber-950/30 dark:text-amber-100"><strong>Important health notice:</strong> Estimate only – not medical advice. For adults aged 18 or older only. Do not use this calculator during pregnancy or breastfeeding, for children or teenagers, or as a substitute for advice from a qualified healthcare professional. No weight-loss or weight-gain outcome is guaranteed.</aside>'
        '<section class="mt-8"><h2 class="text-xl font-semibold">How many calories do I need?</h2>'
        '<p class="mt-2 leading-7">Your daily calorie needs are influenced by your age, body size, body composition, activity, health and other individual factors. A calorie calculator estimates energy needs from a mathematical model. It cannot measure your metabolism or account for every personal circumstance. Use the result as an educational reference, not as an exact daily requirement.</p>'
        '<p class="mt-2 leading-7">The maintenance estimate is intended to approximate the calories associated with maintaining body weight over time. Day-to-day scale readings can move for reasons unrelated to body fat, including fluid balance, food in the digestive system and normal biological variation.</p></section>'
        '<section class="mt-8"><h2 class="text-xl font-semibold">TDEE, maintenance calories and BMR explained</h2>'
        '<p class="mt-2 leading-7"><strong>Total daily energy expenditure (TDEE)</strong> is the energy used across a full day. It includes resting energy, the thermic effect of food and physical activity. This calculator estimates TDEE by multiplying a predicted resting-energy value by one of five activity factors.</p>'
        '<p class="mt-2 leading-7"><strong>Maintenance calories</strong> are a practical term for an estimated daily intake associated with stable body weight over time. In this tool, maintenance calories and estimated TDEE use the same calculated value.</p>'
        '<p class="mt-2 leading-7"><strong>Basal metabolic rate (BMR)</strong>, <strong>resting metabolic rate (RMR)</strong> and <strong>resting energy expenditure (REE)</strong> refer to related but not identical concepts. The formulas estimate resting energy under their published assumptions. They do not replace indirect calorimetry or a clinical assessment.</p></section>'
        '<section class="mt-8"><h2 class="text-xl font-semibold">The three calorie formulas</h2>'
        '<h3 class="mt-4 text-lg font-semibold">1. Mifflin–St Jeor (default and recommended)</h3>'
        '<p class="mt-2 leading-7">Male coefficient: REE = 10 × weight (kg) + 6.25 × height (cm) − 5 × age + 5. Female coefficient: REE = 10 × weight (kg) + 6.25 × height (cm) − 5 × age − 161. The original 1990 study developed the equation from resting-energy measurements in 498 healthy adults aged 19–78. The equation is a population prediction, not a personal measurement.</p>'
        '<h3 class="mt-4 text-lg font-semibold">2. Revised Harris–Benedict (Roza and Shizgal, 1984)</h3>'
        '<p class="mt-2 leading-7">Male coefficient: REE = 88.362 + 13.397 × weight (kg) + 4.799 × height (cm) − 5.677 × age. Female coefficient: REE = 447.593 + 9.247 × weight (kg) + 3.098 × height (cm) − 4.330 × age. These revised equations are distinct from the original Harris–Benedict equations published in 1919.</p>'
        '<h3 class="mt-4 text-lg font-semibold">3. Katch–McArdle (body-composition based)</h3>'
        '<p class="mt-2 leading-7">Estimated resting metabolic rate = 370 + 21.6 × lean body mass (kg). Lean body mass = body weight (kg) × (1 − body-fat percentage ÷ 100). This option requires body-fat percentage and does not use the male or female coefficient input. Its output is only as useful as the body-fat estimate entered. Consumer body-composition devices and visual estimates can be inaccurate.</p>'
        '<p class="mt-2 leading-7">The three equations estimate related resting-energy outcomes using different inputs and study assumptions. They should not be expected to produce identical numbers. Mifflin–St Jeor is selected by default as a practical general-adult starting point, not because it is guaranteed to be the most accurate formula for every person.</p></section>'
        '<section class="mt-8"><h2 class="text-xl font-semibold">Activity levels and TDEE multipliers</h2>'
        '<p class="mt-2 leading-7">After estimating resting energy, the calculator multiplies it by the selected activity factor. These five factors are simplified consumer-calculator assumptions. They are not coefficients from the original Mifflin–St Jeor or Revised Harris–Benedict papers, and they are not the formal FAO/WHO/UNU physical activity level categories.</p>'
        '<ul class="mt-2 list-disc space-y-2 pl-6"><li><strong>Sedentary (1.2):</strong> mostly seated work and little planned movement.</li><li><strong>Light activity (1.375):</strong> some walking or light exercise, with mostly light daily movement.</li><li><strong>Moderate activity (1.55):</strong> regular moderate exercise and a generally active daily routine.</li><li><strong>Very active (1.725):</strong> frequent hard exercise or a physically demanding job.</li><li><strong>Extra active (1.9):</strong> very demanding daily physical work or training.</li></ul>'
        '<p class="mt-2 leading-7">Choose the closest description for your whole day, including work, walking, household tasks and planned exercise. Do not add exercise calories a second time if the activity factor already represents that movement. The factor is approximate and can overestimate or underestimate an individual’s TDEE.</p></section>'
        '<section class="mt-8"><h2 class="text-xl font-semibold">Calorie deficit, surplus and maintenance targets</h2>'
        '<p class="mt-2 leading-7">A calorie deficit means estimated intake is below estimated energy expenditure. A calorie surplus means estimated intake is above estimated energy expenditure. The results panel shows maintenance, maintenance minus 300 kcal, maintenance minus 500 kcal and maintenance plus 250 kcal so the arithmetic can be compared clearly.</p>'
        '<p class="mt-2 leading-7">These deficit and surplus figures are illustrative calculations, not personalized recommendations. A fixed reduction or increase is not appropriate for every adult. The calculator does not screen for low energy availability, nutritional adequacy, medical conditions, medication, eating-disorder risk or other reasons a target may be unsuitable. It does not predict a rate of weight change and makes no weight-loss or weight-gain guarantee.</p></section>'
        '<section class="mt-8"><h2 class="text-xl font-semibold">Simple maintenance macro split</h2>'
        '<p class="mt-2 leading-7">The results panel includes an illustrative split of 30% of maintenance calories from protein, 40% from carbohydrates and 30% from fat. Gram estimates use 4 kcal per gram for protein and carbohydrates and 9 kcal per gram for fat. This is a simple arithmetic example, not a universally optimal ratio, a clinical nutrition plan or an assessment of your individual needs. Food quality, preferences, health and total nutritional adequacy also matter.</p></section>'
        '<section class="mt-8"><h2 class="text-xl font-semibold">Why can calorie calculators give different results?</h2>'
        '<p class="mt-2 leading-7">Two calculators can return different values for the same person because they may use different resting-energy formulas, sex coefficients, activity multipliers, body-fat inputs, population samples, unit conversions or rounding methods. Some tools estimate resting energy, while others estimate total daily energy expenditure directly. Wearables and exercise machines use their own models and can also differ.</p>'
        '<p class="mt-2 leading-7">Compare the formula, inputs and assumptions before comparing the final number. A difference between two estimates does not automatically mean one calculator is broken. Neither output should be treated as a measured metabolic rate.</p></section>'
        '<section class="mt-8"><h2 class="text-xl font-semibold">Pregnancy, breastfeeding and medical conditions</h2>'
        '<p class="mt-2 leading-7"><strong>This calculator is not intended for pregnancy or breastfeeding.</strong> Pregnancy and lactation change nutritional and energy requirements, and an ordinary adult prediction equation or fixed deficit/surplus example is not an appropriate substitute for individualized care. Speak with a qualified healthcare professional or registered dietitian for guidance during pregnancy or breastfeeding.</p>'
        '<p class="mt-2 leading-7">This tool is also not designed to adjust for diabetes, thyroid conditions, other metabolic or chronic diseases, medication, recovery from illness, competitive sport, eating-disorder history or clinical nutrition needs. If any of these circumstances apply, do not use the displayed values to set a diet or treatment target. Seek advice from a professional who knows your health history.</p>'
        '<p class="mt-2 leading-7">The equations are population-level estimates. Their original study groups and assumptions do not represent every country, body type, age or health circumstance. In particular, the original Mifflin–St Jeor sample was adults aged 19–78, while this page accepts adults from age 18 as a broad consumer input range. The age input range does not mean that every age has equal validation evidence.</p></section>'
        '<section class="mt-8"><h2 class="text-xl font-semibold">Worked example</h2>'
        '<p class="mt-2 leading-7">For an adult aged 30 with a weight of 70 kg, a height of 175 cm and the male coefficient, Mifflin–St Jeor gives: 10 × 70 + 6.25 × 175 − 5 × 30 + 5 = 1,648.75 kcal/day resting energy. With the sedentary factor of 1.2, the estimated maintenance value is 1,648.75 × 1.2 = 1,978.5 kcal/day. The displayed result is rounded to one decimal place.</p>'
        '<p class="mt-2 leading-7">The arithmetic example demonstrates the formula only. It is not a prediction for every adult with these measurements and is not a diet recommendation.</p></section>'
        '<section class="mt-8"><h2 class="text-xl font-semibold">Limitations and safety</h2>'
        '<ul class="mt-2 list-disc space-y-2 pl-6"><li>Estimate only – not medical advice, diagnosis or treatment.</li><li>Adults aged 18 or older only. Not for children or teenagers.</li><li>Not intended for pregnancy or breastfeeding.</li><li>No weight-loss, weight-gain, muscle-gain or timeline guarantee.</li><li>Deficit, surplus and macro figures are illustrative arithmetic, not personalized prescriptions.</li><li>Prediction equations can overestimate or underestimate actual energy needs.</li><li>Katch–McArdle depends on the accuracy of the entered body-fat percentage.</li><li>Activity multipliers are simplified assumptions, not measured activity or validated individual TDEE.</li><li>A resting-energy estimate is not a minimum safe calorie intake.</li><li>This calculator has not been medically reviewed.</li></ul></section>'
        '<section class="mt-8"><h2 class="text-xl font-semibold">Privacy: calculations stay in your browser</h2>'
        '<p class="mt-2 leading-7">The calculator performs the formula calculations in your browser using JavaScript. Your calculator measurements are not sent to a calculation server or API. The calculator code does not submit age, weight, height, body-fat percentage or results, place those values in the page URL, or save them in browser storage. Reset clears the entered values and displayed result. The website host and third-party resources may still process ordinary technical request data, as explained in the <a class="underline text-sky-800 dark:text-sky-300" href="/privacy/">Privacy Policy</a>.</p></section>'
        '<section class="mt-8"><h2 class="text-xl font-semibold">Frequently asked questions</h2><div class="mt-2">'
        + "".join(
            '<details class="border-b border-stone-300 py-3 dark:border-stone-700"><summary class="min-h-[44px] cursor-pointer font-medium">'
            + html.escape(question)
            + '</summary><p class="mt-2 leading-7">'
            + html.escape(answer)
            + '</p></details>'
            for question, answer in faq
        )
        + '</div></section>'
        '<section class="mt-8"><h2 class="text-xl font-semibold">Page ownership and medical review</h2>'
        '<p class="mt-2 leading-7">Site maintainer: Muhammad Fayyaz Adeel. No qualified medical professional has reviewed this calculator or its implementation. The cited research supports the named formulas and general context, not medical certification or endorsement of this website.</p></section>'
        '<section class="mt-8"><h2 class="text-xl font-semibold">Sources and references</h2><ul class="mt-2 list-disc space-y-3 pl-6">'
        + "".join(
            '<li><a class="underline text-sky-800 dark:text-sky-300" href="'
            + html.escape(url, quote=True)
            + '" target="_blank" rel="noopener noreferrer">'
            + html.escape(source_title)
            + '</a><p class="text-sm leading-6">'
            + html.escape(note)
            + '</p></li>'
            for source_title, url, note in sources
        )
        + '</ul></section>'
        '<nav aria-label="Related calculators" class="mt-8"><h2 class="text-xl font-semibold">Related tools</h2><ul class="mt-2 list-disc space-y-1 pl-6">'
        '<li><a class="underline text-sky-800 dark:text-sky-300" href="/bmi-calculator/">Adult BMI Calculator</a></li>'
        '<li><a class="underline text-sky-800 dark:text-sky-300" href="/health/">Health calculators and guidance</a></li>'
        '<li><a class="underline text-sky-800 dark:text-sky-300" href="/methodology/">Calculation methodology</a></li>'
        '<li><a class="underline text-sky-800 dark:text-sky-300" href="/about/">About CalculatesAll</a></li></ul></nav>'
        '<p class="mt-6 text-sm text-stone-700 dark:text-stone-300">For a correction, use the <a class="underline text-sky-800 dark:text-sky-300" href="/contact/">Contact page</a>. Do not send medical records or other sensitive personal information.</p>'
    )

    schema = [
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": title,
            "url": site + path,
            "description": description,
            "publisher": {"@id": site + "/#organization"},
            "citation": [url for _, url, _ in sources],
            "inLanguage": "en",
        },
        {
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": "Calorie Calculator",
            "url": site + path,
            "description": description,
            "applicationCategory": "HealthApplication",
            "operatingSystem": "Any",
            "browserRequirements": "Requires JavaScript",
            "publisher": {"@id": site + "/#organization"},
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "inLanguage": "en",
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": site + "/"},
                {"@type": "ListItem", "position": 2, "name": "Health", "item": site + "/health/"},
                {"@type": "ListItem", "position": 3, "name": "Calorie Calculator", "item": site + path},
            ],
        },
    ]

    document = head(title, description, path, schema) + shell(body, current_path=path)
    with open("static/calorie-calculator.js", "rb") as script_file:
        script_version = hashlib.sha256(script_file.read()).hexdigest()[:12]
    document = document.replace(
        "</body>",
        f'<script defer src="/assets/calorie-calculator.js?v={script_version}"></script></body>',
    )
    write(path, document)
    return path
