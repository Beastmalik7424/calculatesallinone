# Health hub WHO underweight subcategory audit (v8)

Audit date: 23 November 2026

## 1. WHO source

Primary source: https://iris.who.int/bitstream/handle/10665/43190/9241593024_eng.pdf

Access date: 23 November 2026. The primary WHO PDF opened successfully and its text was readable. **Primary PDF verified: YES.** The publication is *The SuRF Report 2: Surveillance of chronic disease Risk Factors: Country-level data and comparable estimates* (WHO, 2005). Table 3.1 is on printed page 22.

Exact Table 3.1 rows (BMI in kg/m²):

- Severe thinness | <16.00 | <16.00
- Moderate thinness | 16.00 – 16.99 | 16.00 – 16.99
- Mild thinness | 17.00 – 18.49 | 17.00 – 18.49

The two numeric columns are the principal cut-off points and additional cut-off points. The three quoted subcategory rows carry the same values in both columns.

## 2. Other sources checked and Nutrition Landscape distinction

WHO Nutrition Landscape Information System help page: https://apps.who.int/nutrition/landscape/help.aspx?menu=0&helpid=392&lang=EN (accessed 23 November 2026). It describes BMI <17.0 as “moderate and severe thinness” and BMI <18.5 as “underweight”. It also notes that BMI <16.0 is associated with markedly increased risk. This page presents a combined population-monitoring indicator for moderate and severe thinness. It does not provide the three separate grade bands, including mild thinness, that are stated in Table 3.1.

The Health body cites SuRF Report 2, Table 3.1 because the sentence makes a three-subcategory classification claim and that primary table explicitly lists all three grades and their exact cut-off ranges. The Nutrition Landscape page is not contradictory: it aggregates moderate and severe thinness at BMI <17.0 for its monitoring indicator, rather than reproducing the full three-grade table. The Nutrition Landscape page is recorded as a separate WHO indicator page, not as a substitute for the primary table.

## 3. Changed files

Exactly four paths are intended in the final base-to-HEAD comparison:

1. `content_v13.py`: only the `HUB_EXTRA["health"]` value changed. In the WHO body paragraph, the existing subcategory sentence was replaced with: “The WHO SuRF Report 2, Table 3.1, divides underweight into three subcategories. Severe thinness is below 16.00. Moderate thinness is 16.00 to 16.99. Mild thinness is 17.00 to 18.49.”
2. `build.py`: only the WHO adult BMI FAQ tuple changed. No other `build.py` line differs from the base.
3. `tests/health_content_v8.py`: new AST-based test. It reads source text, parses with `ast`, and does not import `build.py` or `content_v13.py`.
4. `review/health_audit_v8.md`: this audit report.

The only changed line in `build.py` is the WHO FAQ tuple. The removed base line was:

```python
            ("What are the WHO adult BMI categories?", "The WHO table lists underweight below 18.50, normal range 18.50 to 24.99, pre-obese 25.00 to 29.99, obese class I 30.00 to 34.99, obese class II 35.00 to 39.99, and obese class III at 40.00 or higher. The English calculator result groups the obesity classes into one displayed obesity label. It displays four broad labels and selects them from the unrounded BMI using the 18.5, 25 and 30 thresholds."),
```

The added line is:

```python
            ("What are the WHO adult BMI categories?", "The WHO table lists underweight below 18.50. Underweight is divided into three subcategories in SuRF Report 2, Table 3.1. Severe thinness is below 16.00. Moderate thinness is 16.00 to 16.99. Mild thinness is 17.00 to 18.49. It also lists normal range 18.50 to 24.99, pre-obese 25.00 to 29.99, obese class I 30.00 to 34.99, obese class II 35.00 to 39.99, and obese class III at 40.00 or higher. The English calculator result groups the obesity classes into one displayed obesity label. It displays four broad labels and selects them from the unrounded BMI using the 18.5, 25 and 30 thresholds."),
```

## 4. Commit hashes in order

1. Content: `a35da4cec6eba96d4a03d1d8376ea4bded30ea40`
2. Test: `349a4e0384408df4c480b3965e63f7d1700b8370`
3. Report: this file is contained in the third commit. Its SHA is recorded in the final completion record; embedding a commit's own SHA inside its tree would change that SHA.

The previous remote branch HEAD was `34ff498cd628aca04141cebe48dac0a8f874504a`. The branch history was rebuilt from base `02a302020622ff3c4e2e6aa75f15a12fd9a5f830` as content, then test, then report. The first two old commits were already in content-then-test order, so they did not need swapping.

## 5. Test results

- Base-commit test on isolated source snapshot: **FAIL as expected, exit code 1**. The exact committed `tests/health_content_v8.py` script was run with Python against an isolated AST fixture populated from the base revision's WHO FAQ tuple. It stopped at the expected missing phrase: `WHO FAQ missing 'severe thinness'`.
- Updated-branch test on isolated source snapshot: **PASS, exit code 0**. The same committed test script was run against an isolated AST fixture populated from the branch's Health body paragraph and all eight Health FAQ tuples. Output: `PASS: health_content_v8`.
- This is an alternative source-snapshot execution, not the requested `git worktree add` run. A full local worktree could not be created because this container cannot resolve or connect to `github.com`. The test logic, target content and eight FAQ tuples were executed in Python, but the fixture was not the complete repository checkout. Treat the exact worktree requirement as **NOT RUN**.
- The AST-based test reads files as text, parses with `ast`, and does not import `build.py` or `content_v13.py`. It checks all six required phrases, the 6–8 FAQ count, prohibited punctuation, reviewer/date/credential signals, and the single-line-group `build.py` difference.
- The GitHub compare result independently confirms that the real branch `build.py` differs from the base by exactly one removed and one added WHO FAQ tuple line. This compare result is not a substitute for the unavailable full-worktree test.

## 6. Build and install results

- Clean GitHub Actions checkout: **PASS**. Workflow run [Build and smoke test #45183840068](https://github.com/Beastmalik7424/calculatesallinone/actions/runs/45183840068), on final source/test commit `e4fa63c973bc9240536c177cae4c135068beaf83`, completed with conclusion `success`.
- `npm ci`: **PASS, exit code 0**. The runner log shows 76 packages added, 77 audited and zero vulnerabilities. The subsequent CI steps ran, confirming the command returned successfully.
- `npm run build`: **PASS, exit code 0**. The clean runner executed the package build chain. It included CSS build, `python3 build.py`, `seo_finalize.py`, all configured content and calculator tests, `python3 tests/site-output-smoke.py`, and other smoke/property tests. The step completed successfully and later CI steps ran.
- The CI job completed with success. All 33 listed job steps completed successfully, including the build, generated-page smoke test, sitemap/internal-link checks, HTML validation, Lighthouse checks and safe monetization configuration.
- The build logs include the 14,000 deterministic calculator simulations, 39,703 unit/property assertions and 3 generated-page integration contracts previously recorded. The custom `health_content_v8.py` test is not in the package build command and was run separately only via the source-snapshot alternative above.
- Local direct `git clone` and `git worktree add` remain **NOT RUN** because this container cannot resolve/connect to `github.com`. The GitHub Actions runner is the clean-checkout alternative for install and build.


### Recorded command-log tails

Source: GitHub Actions clean-checkout run [#45183840068](https://github.com/Beastmalik7424/calculatesallinone/actions/runs/45183840068), job `build`. Both shell steps ran under `bash -e`; the workflow continued and completed successfully, so both command exit codes were 0.

`npm ci` tail (the step produced 18 lines total):

```text
##[group]Run npm ci
npm ci
shell: /usr/bin/bash -e {0}
env:
  pythonLocation: /opt/hostedtoolcache/Python/3.12.16/x64
  PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.12.16/x64/lib/pkgconfig
  Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.16/x64
  Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.16/x64
  Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.16/x64
  LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.12.16/x64/lib
##[endgroup]

added 76 packages, and audited 77 packages in 1s

19 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
```

`npm run build` final 30 log lines:

```text
xmllint: sitemap XML valid
##[group]Run test -s public/index.html
test -s public/index.html
test -s public/ur/index.html
test -s public/sitemap.xml
test -s public/robots.txt
grep -q 'Standard Calculator' public/index.html
grep -q 'Free' public/index.html
grep -q 'محفوظ' public/ur/index.html
test -s public/assets/og-image.png
grep -q '/assets/og-image.png' public/index.html
python -c "import struct; p=open('public/assets/og-image.png', 'rb').read(24); assert p[:8] == bytes([137,80,78,71,13,10,26,10]) and struct.unpack('>II', p[16:24]) == (1200,630)"
test -s public/assets/og-image.svg
grep -q '/standard-calculator/' public/sitemap.xml
grep -q 'href="https://calculateallinone.vercel.app/standard-calculator/"' public/standard-calculator/index.html
grep -q 'href="/ur/zakat-calculator/"' public/zakat-calculator/index.html
grep -q 'href="/zakat-calculator/"' public/ur/zakat-calculator/index.html
grep -q 'PRIVATE BY DESIGN' public/index.html
python -c "import os,pathlib; client=os.environ.get('ADSENSE_CLIENT','ca-pub-9453966537556063').strip(); expected='google.com, '+client.removeprefix('ca-')+', DIRECT, f08c47fec0942fa0'; assert pathlib.Path('public/ads.txt').read_text(encoding='utf-8').strip() == expected, 'ads.txt must match the configured publisher ID'"
if grep -Eq 'Ø|Ù|Ã|âŒ|âˆ|Â©' public/ur/index.html; then echo 'Mojibake found in Urdu home page'; exit 1; fi
if grep -Eq 'âŒ«|Ã·|Ã—|âˆ’' public/index.html; then echo 'Corrupted calculator symbols found'; exit 1; fi
shell: /usr/bin/bash -e {0}
env:
  pythonLocation: /opt/hostedtoolcache/Python/3.12.16/x64
  PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.12.16/x64/lib/pkgconfig
  Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.16/x64
  Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.16/x64
  Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.16/x64
  LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.12.16/lib
##[endgroup]
```

## 7. Preview and live checks

Preview for code-and-test commit `349a4e0384408df4c480b3965e63f7d1700b8370`:

- Deployment ID: `dpl_EyMpqFrsGZfSRyeqWH4WaxA7uD4W`
- State: **READY**
- Preview URL: https://calculatesall-dnnvmo25p-malikadeelbhatti-1187.vercel.app
- `/health/` fetch: HTTP 200.
- All three subcategory sentences appear in the rendered body.
- The corrected WHO FAQ answer appears in the rendered FAQ and structured FAQ data.
- H1 count: 1.
- FAQ `details` count: 8.
- DOM tag outline compared with the current production `/health/`: identical, 362 tags in each document. This checks the structural outline, not visual pixel equality. It supports that the content-only change preserved the page structure and layout skeleton.

The report-only third commit is created after this preview check. It does not modify build inputs. The final report commit's own deployment is to be checked after it is pushed; that later deployment result is recorded in the final completion message.

## 8. Pull request

PR #323 was confirmed closed and unmerged. A new draft PR, #324, was opened after the report commit was pushed: https://github.com/Beastmalik7424/calculatesallinone/pull/324. PR #322 is confirmed merged. The new draft PR has not been merged.

## 9. Deviations and remaining issues

- The local `git clone` and `git worktree add` commands could not run because the execution container cannot resolve or connect to `github.com`. A direct retry using a pinned GitHub IP also failed to connect. The exact test was therefore exercised with an isolated source-snapshot fixture in Python, and the full clean-checkout install/build ran successfully in GitHub Actions.
- The test snapshot run is an alternative, not the requested complete repository worktree run. Its base exit code was 1 and updated snapshot exit code was 0. This limitation remains explicit.
- The three-commit sequence is content, test, report. The first two earlier commits were already in the required content-then-test order. The report commit was amended to record the later test and CI evidence while retaining exactly three commits.
- An earlier workflow unintentionally triggered a Vercel build that invoked `tests/site-output-smoke.py` before that invocation had been authorized. This prior event is disclosed. The current owner instruction expressly authorizes the repository build and its tests, including that script.
- No changes were made to `main`, PR #322, PR #323, `health-audit-v7`, or any other branch. No merge was performed. No branch was deleted.
- Medical review not completed. Plagiarism and originality clearance not completed.

## 10. Medical and originality limitations

**Medical review not completed. Plagiarism and originality clearance not completed.**


## 11. Follow-up independent source and originality review

Follow-up review date: 23 November 2026. This section supersedes the earlier pending-status notes above where a later result is recorded.

### Medical-content source verification

The Health hub claims relevant to this change and its surrounding BMI/calorie explanations were cross-checked against independent primary or authoritative sources:

- WHO, *The SuRF Report 2*, Table 3.1, printed page 22: severe thinness <16.00 kg/m²; moderate thinness 16.00–16.99; mild thinness 17.00–18.49. Primary source: https://iris.who.int/bitstream/handle/10665/43190/9241593024_eng.pdf.
- WHO, *Malnutrition in women* and NLiS help content: confirms adult BMI is a screening/population indicator, <18.5 underweight and <17.0 thinness; the NLiS combined indicator groups moderate and severe thinness and is not a replacement for the three-band SuRF table.
- WHO 2021 SEARO District Clinician Manual, adult classification table: independently reproduces the three thinness bands for adults and states that interpretation must remain in clinical context.
- NCBI Bookshelf, WHO consolidated TB guidelines, 2025, Table 1 and definitions: independently gives adult severe undernutrition <16, moderate 16.0–16.99, mild 17.0–18.49, and underweight <18.5; child/adolescent definitions use age-specific measures.
- CDC adult BMI guidance and CDC's 16 December 2025 BMI overview: confirm BMI is a screening measure, not a diagnosis; adult CDC categories apply from age 20, while ages 2–19 use BMI-for-age percentiles.
- Mifflin et al., 1990, PubMed PMID 2305711: confirms the equation coefficients and the original sample of 498 healthy adults aged 19–78.
- National Academies of Sciences, Engineering, and Medicine, *Dietary Reference Intakes for Energy* (2023), Tables 5-16 and 5-17 and breastfeeding equations: confirms separate age/sex/life-stage equations and the inactive, low-active, active and very-active PAL categories used for the pregnancy/lactation path.
- WHO Expert Consultation, 2004, PubMed PMID 14726171: confirms that Asian BMI action points 23.0, 27.5, 32.5 and 37.5 are additional public-health action points, not a replacement set of universal individual diagnostic thresholds.

**Finding:** no factual conflict was identified in the audited claims against these sources. The copy correctly distinguishes WHO population classification, CDC adult age scope, BMI screening limitations, the original Mifflin-St Jeor study population, consumer activity multipliers, and the separate National Academies life-stage estimates. No calculator formula or result behavior was changed.

**Review boundary:** this is an independent source-based editorial and medical-accuracy review, not a review by a licensed physician or registered dietitian. No clinician has been identified as the reviewer, and no professional credential or medical-review claim is made. The existing page statement that the guide has not been medically reviewed must remain. A formal clinician sign-off cannot be manufactured by an online source comparison.

### Originality and similarity screening

- The complete Health body content section and the newly changed WHO FAQ text were submitted to the AISEO plagiarism checker in a follow-up run.
- Checker result: 1,461 words counted; plagiarism/similarity score 6%; uniqueness score 94%; 89 matched words; one returned source reference.
- The matched phrases were short, common technical expressions (BMI formula wording, broad BMI labels, equation coefficients, and standard age/category references). The only returned source URL was a Brave search redirect (https://search.brave.com/go/v1), not an attributable publication. It is therefore not valid evidence that the text was copied from a particular source.
- Targeted indexed-web searches for distinctive sentences in the Health copy did not surface an exact sentence-level match. This is a bounded manual search, not an exhaustive search of every web page or unpublished work.
- The first automated attempt returned HTTP 502. The subsequent complete-content submission succeeded.

**Finding:** the automated and manual screens did not identify a substantiated unattributed passage. The 94% uniqueness result is a screening result, not a legal opinion or guarantee of originality. No text was rewritten solely to chase a numerical score.

### Updated release and scope status

- PR #324 was freshly verified as **open, Draft, mergeable, and not merged**. It remains Draft in accordance with the explicit release instruction.
- The PR still changes exactly four paths: `content_v13.py`, `build.py`, `tests/health_content_v8.py`, and this report. No other page, calculator, formula, layout, CSS, navigation, route, or production file was changed.
- The latest recorded Build and smoke test run #45214489071 completed successfully. All 33 listed build/test/SEO/browser/monetization steps and the job completion steps passed. The six other PR-associated workflow runs also completed successfully.
- The committed custom AST test was previously exercised with the source-snapshot alternative: base fixture failed as expected and updated fixture passed. The exact full-worktree invocation remains not run because the execution environment could not connect to github.com. Do not describe the snapshot run as the full-worktree test.
- The preview evidence remains the READY Vercel preview recorded above. No production deployment or merge was performed.

**Final audit disposition:** source-based medical accuracy review and automated/manual originality screening are complete within the stated limits. Licensed-clinician sign-off and the exact local full-worktree test remain outstanding. PR #324 stays Draft and production remains unchanged.
