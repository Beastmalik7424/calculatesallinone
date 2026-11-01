# Adult Calorie Calculator source and assumptions register

Verification date: 2026-11-02  
Feature version: 1.0  
Publication scope: English adult maintenance estimate only

## Claim and source register

| Claim or implementation | Source | Population / scope | Implementation use | Limitation | Pages/components using claim |
|---|---|---|---|---|
| Mifflin–St Jeor resting-energy equations use the published male and female coefficients | Mifflin MD, St Jeor ST et al. “A new predictive equation for resting energy expenditure in healthy individuals.” American Journal of Clinical Nutrition, 1990. [PubMed 2305711](https://pubmed.ncbi.nlm.nih.gov/2305711/) | Original study included 498 healthy adults aged 19–78 | REE formula only | Predictive equation, not an individual metabolic measurement or guarantee. The original study sample does not cover age 18 or ages above 78. |
| Adult energy requirements can be discussed using BMR and physical activity level concepts | FAO/WHO/UNU, *Human Energy Requirements*, 2004. [Full report](https://www.fao.org/4/y5686e/y5686e00.htm) and [adult energy requirements chapter](https://www.fao.org/4/y5686e/y5686e07.htm) | Population-level adult energy requirements and PAL framework | Context for distinguishing the report's BMR/PAL framework from this consumer calculator | Not the source of the Mifflin equation or the five consumer multipliers. No FAO certification or endorsement is claimed. | `/calorie-calculator/`, `calorie_calculator.py`, `research/calorie-calculator-source-register.md` |
| Adult guidance should exclude people under 18 and pregnant or breastfeeding users from an ordinary planner | NIDDK, [About the Body Weight Planner](https://www.niddk.nih.gov/health-information/weight-management/body-weight-planner) | NIDDK planner states adults 18+ and excludes younger people and pregnant or breastfeeding women | Conservative eligibility boundary and user-facing exclusion | The NIDDK planner is a different dynamic model. This calculator does not implement it and does not claim NIDDK approval. | `/calorie-calculator/`, `calorie_calculator.py`, `static/calorie-calculator.js` |

## Application-defined assumptions

| Identifier | Version | Multiplier | Display label | Source | Limitation |
|---|---:|---:|---|---|---|
| sedentary | 1.0 | 1.2 | Sedentary | Application-defined consumer preset | Approximate heuristic, not individually validated or a measured PAL. |
| light | 1.0 | 1.375 | Light activity | Application-defined consumer preset | Approximate heuristic, not individually validated or a measured PAL. |
| moderate | 1.0 | 1.55 | Moderate activity | Application-defined consumer preset | Approximate heuristic, not individually validated or a measured PAL. |
| very_active | 1.0 | 1.725 | Very active | Application-defined consumer preset | Approximate heuristic, not individually validated or a measured PAL. |
| extra_active | 1.0 | 1.9 | Extra active | Application-defined consumer preset | Approximate heuristic, not individually validated or a measured PAL. |

These activity values are configuration assumptions supplied for a consumer estimate. They are not coefficients from the Mifflin–St Jeor study and are not represented as FAO/WHO/UNU PAL categories. They have not been clinically validated for this website.

## Validation policy

- Age accepts whole years from 18 to 120. Age 18 and ages above 78 are accepted only with an explicit note that they fall outside the original Mifflin study sample.
- Weight is normalized to kilograms and checked against a broad 20–500 kg input guardrail.
- Height is normalized to centimetres and checked against a broad 100–250 cm input guardrail.
- These are broad input-error guardrails, not medical reference ranges or population eligibility criteria.
- Inputs must be finite numbers. Empty, malformed, non-finite, zero, negative and unsupported unit values are rejected.
- Weight conversion uses 1 lb = 0.45359237 kg. Height conversion uses 1 inch = 2.54 cm. Raw values are normalized once and not repeatedly converted during unit toggles.
- Intermediate calculations retain full JavaScript number precision. Formatting is applied only to displayed results.
- No statistical confidence interval is calculated.
- Pregnancy, breastfeeding, both, or a declined eligibility answer blocks the ordinary estimate.
- The output is REE multiplied by an app-defined activity assumption. It is not a measured TDEE and is not a weight-loss or weight-gain prescription.

## Review and release status

- Source links and claims checked: 2026-11-02.
- Code testing: pending CI and browser results.
- Preview verification: pending.
- Production verification: pending.
- Qualified clinical review: not performed.
- Medical certification or endorsement: none claimed.
