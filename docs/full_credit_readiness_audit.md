> Historical audit: this document describes an earlier version. Use [the final report audit](submission_audit_changes.md) and [current verification](submission_audit_results.json) for the saved report.

> **Historical estimate assessed the pre-completion version.** See [current coverage](rubric_compliance_audit.md), [changes](rubric_completion_changes.md), and [verified current execution](current_execution_results.json). Other analytical gaps have current evidence, but DFBETAS remains required and Missing because the user cancelled its addition. Group names and syllabus review remain deferred. No guaranteed full-credit grade is asserted.

# ECON 430 full-credit readiness audit and estimated grade

Reviewed October 27, 2026 against commit `3507f1c6507c975c55ef04994acd73ca62e0a928`, the six main notebooks, three cleaning notebooks, processed CSVs, saved outputs and recorded execution evidence. Authority: [the professor’s four-page assignment PDF](../project1-1%20%281%29.pdf), SHA-256 `925f6c47394ebaf43430faad04166c1719082a0ff2b35b8e9e4f4e31539bd679`. Its sections total **130 points**; the PDF does not allocate points within subsections or specify letter-grade cutoffs.

**Verdict: not yet ready to claim full credit. Estimated analysis grade: 115/130 (88.5%).** This is my judgment, not the instructor’s awarded score. A reasonable grading-discretion range is 110–120/130, not a statistical confidence interval. The estimate assumes the existing material is assembled into an accepted submission. **The repository itself is not presently a compliant final submission:** the only PDF/HTML deliverable located is the assignment PDF, not a group report. Any additional format, names, late-submission or syllabus-policy penalty is unknown and is not invented or folded into this score.

No model, predictor, coefficient, cleaning rule, seed, source data or notebook was changed during this audit. This report checks readiness; it does not complete the missing analyses.

## Estimated marks by the professor’s section weights

| Component | Available | Estimated | Reason for the estimated deduction |
|---|---:|---:|---|
| 1. Economic theory and hypothesis | 15 | 13 | Question, two academic sources and testable hypothesis are present. Expected signs are discussed, but expected magnitudes remain underdeveloped. |
| 2. Data description and EDA | 25 | 23 | Strong descriptive, visualization, outlier and missingness evidence. Q-Q/density coverage omits additional candidate distributions. Profiling has saved successful evidence, although fresh replay is blocked. Its environment problem is counted under Section 7 rather than deducted twice. |
| 3. Variable selection and models | 25 | 21 | Boruta, Cp, VIF, three models and all requested comparisons exist. Model 3’s compliance with “including all statistically significant predictors” is unresolved, and the significance scope needs an explicit argument. |
| 4. Diagnostics and robustness | 20 | 17 | Required plots/tests, influence screens, 1,000 bootstrap replications and five-fold validation exist. **DFBETAS is missing.** |
| 5. Results and interpretation | 25 | 23 | Final table, all slopes/intercept, units, uncertainty, fit and economic/statistical significance are covered. Direct comparison of final findings with the academic literature is limited. |
| 6. Limitations, policy and extensions | 10 | 10 | All five requested topics have substantive discussion. No additional mandatory omission found. |
| 7. Code quality and reproducibility | 10 | 8 | Seeded analyses and generating code are present. Profiling cannot currently replay, a full raw reconstruction is untested, and historical headings/references require final editorial review. |
| **Total** | **130** | **115** | **88.5%; final-submission acceptance is a separate unresolved condition.** |

The deductions above are estimates, not official per-item point values. In particular, a strict interpretation of Model 3 or rejection of an improperly formatted submission could produce a lower result.

## Findings that must be resolved before claiming full coverage

### 1. Missing required submission — definite gap

PDF p. 1 requires **one written PDF or HTML report per group**, containing economic motivation/hypothesis, data description, methodology, coefficient interpretation/results, limitations, conclusion, references and Python source, with **all group members’ names**. The notebooks supply most of the content, but no assembled final report or verified full member list was found. GitHub branches and notebooks are not the specified upload format. The assignment PDF is not the student report.

Acceptance evidence needed: a reviewed final PDF/HTML, verified names, readable figures/tables, references and source code included in the submitted artifact. Check the course syllabus’s Assignment Policies; the syllabus is not available here. The PDF states a due date of October 30, 2026, but gives no time or submission penalty schedule.

### 2. DFBETAS — definite mandatory omission

PDF p. 3 explicitly lists DFBETAS under outliers/influence. [Notebook 04](../notebooks/04_diagnostics_robustness.ipynb), 4(d), retains Cook’s distance, leverage, studentized residuals and sensitivity analysis, but contains **no DFBETAS calculation, result or interpretation**. A heading or statement that no lecture example was available does not satisfy the assignment.

Acceptance evidence needed: an executed coefficient-influence analysis using DFBETAS, an explained screening/inspection method, identification of affected coefficients/observations and an economic/statistical interpretation. Preserve the original primary model and distinguish inspection flags from data errors. This audit does not implement a new diagnostic or lift earlier method-preservation constraints.

### 3. Model 3’s significance requirement — substantive rubric risk

The exact instruction is **“Multiple regression including all statistically significant predictors.”** It does **not** explicitly say “include only significant predictors.” Keeping theoretically motivated insignificant controls is therefore not, by itself, proof of noncompliance; do not mechanically remove variables to make every p-value small.

The actual unresolved issue is scope: [Notebook 03](../notebooks/03_variable_selection_models.ipynb), cell 11, reports a full 12-candidate model in which `walk_share` and `nearby_business_count` are significant at 5% (both displayed p<0.001). Neither is in the final seven-predictor Model 3. The project explains collinearity/parsimony choices, but does not demonstrate that Model 3 contains all significant predictors under an explicitly defined eligible candidate set and testing rule. Boruta importance is not individual OLS significance.

Time limit and transit share have final conventional p-values about 0.098 and 0.675, respectively; HC1 gives about 0.120 and 0.664. Those facts should remain transparent, but are not the sole reason to flag 3(d). Acceptance evidence: clarify the intended candidate universe/significance standard and obtain a defensible reconciliation with the professor’s wording. An explanatory note alone does not guarantee instructor acceptance. This audit preserves the original models rather than silently replacing Model 3.

### 4. Expected magnitudes — explicit requirement with weak treatment

PDF 1(d) asks for expected **signs and magnitudes** grounded in theory. [Notebook 01](../notebooks/01_economic_theory.ipynb), cell 4, supplies sign predictions and says theory does not pin down a credible numerical magnitude. That is a sensible caution, but reporting estimated coefficients later is not the same as discussing expectations before examining results.

Acceptance evidence needed: a defensible discussion of plausible economic size in the variables’ units, including occupancy’s 0–1 bound and what is or is not identifiable from the cited theory. The PDF does not require a fabricated numerical prior or an arbitrary effect-size target.

### 5. Continuous-variable Q-Q/density coverage — conservative scope risk

PDF 2(d) asks for Q-Q and density plots for continuous variables. [Notebook 02](../notebooks/02_data_description_eda.ipynb), cell 33, plots seven variables: outcome, price, population density, income, food-service/retail count, drive-alone share and transit share. Additional EDA candidates `housing_density` and `walk_share` have no such panels. `nearby_business_count` is also omitted; although count-valued, it is treated as a distributional candidate elsewhere and including it would remove a scope ambiguity.

Acceptance evidence needed: cover the remaining relevant distributions and interpret them, or explicitly justify a narrower declared continuous-variable analysis set. Time limits and TOD status may reasonably be handled as discrete/categorical. The PDF does not require every histogram/scatterplot to cover every candidate; its visualization instruction specifies appropriate key relationships.

### 6. Final results versus literature — explicit page-4 grading criterion

The page-4 assessment table includes **literature comparison** under results/interpretation. [Notebook 01](../notebooks/01_economic_theory.ipynb) cites Shoup (2006) and Pierce and Shoup (2013); [Notebook 05](../notebooks/05_results_interpretation.ipynb) discusses tension with a simple demand hypothesis, but does not develop a study-by-study comparison of the final findings with those sources. Merely repeating citations or the original hypothesis leaves a grading risk.

Acceptance evidence needed: compare the positive conditional price association and other relevant results with what the cited work actually studies/finds, explicitly discussing different settings, designs, tariff proxies and endogeneity. Do not equate a cross-sectional association with a causal pricing response or invent the papers’ numerical results. External paper contents were not independently re-reviewed in this local rubric audit.

### 7. Reproducibility — verified in part, not end to end

The existing [execution report](notebook_validation_results.json) records fresh successful runs for main notebooks 03, 04 and 05, with **75 numerical output comparisons and zero mismatches** across successful checked outputs. Notebook 02’s Profiling cell 52 failed to import a usable `ProfileReport`; its original successful summary and alerts remain saved. This distinction earns credit for actual implemented Profiling, but prevents claiming a clean full replay.

The current environment lacks Profiling transitive dependencies and has NumPy/matplotlib versions outside its declared constraints. `data/raw/` is absent, and the required geospatial environment is unavailable for a raw reconstruction. Raw inputs being excluded from Git is not automatically a rubric violation; documented, obtainable inputs and a working rebuild are the relevant reproducibility evidence. The three fixed processed CSVs are available and support the regressions.

Acceptance evidence needed: a compatible isolated environment and successful EDA/ProfileReport replay; clear dependency/version instructions and raw-input access/provenance sufficient for a separate safe reconstruction. Review the inherited cleaning notebook format-version mismatch. Do not overwrite original CSVs merely to prove that an export cell runs.

### 8. Final presentation and references — deliverable quality risks

Some preserved cells retain old notebook numbers, duplicate titles, historical “Complete” claims and conventional intervals alongside final HC1 intervals. Current wrappers explain the differences, and the calculations are not thereby wrong, but a final report should not force a grader to reconcile historical versions. Source citations exist; a consolidated report bibliography has not been assembled.

Acceptance evidence needed: a final presentation with current references, clear sample names/units, consistent labeling of conventional versus HC1 inference, one current conclusion, and a complete bibliography. Preserve the original work in the repository while preparing that presentation.

## Every substantive PDF item checked

“Covered” below means actual text/code/saved evidence exists, not a guarantee of full marks for its quality. For granular original/destination cell locators, use the [130-row compliance audit](rubric_compliance_audit.md). Section 4 letters are organizational labels; the PDF uses bullets.

| Item | Requirement / evidence checked | Current assessment |
|---|---|---|
| 1(a) | Clear economic research question; Notebook 01 | Covered |
| 1(b) | 2–3 theory/literature paragraphs and at least two academic sources; Notebook 01 | Covered; literature review is concise |
| 1(c) | Specific, testable relationship; negative conditional price hypothesis | Covered |
| 1(d) | Expected signs **and magnitudes** | Partial: expected magnitudes weak |
| 2(a) | Sources, period, sample selection and definitions; Notebook 02, cleaning, detailed README | Covered; vintage mismatches disclosed |
| 2(b) | Mean, median, SD, min, max, skewness, kurtosis | All seven present; excess kurtosis labeled |
| 2(c) | Histograms, boxplots, correlation heatmap, key scatterplots | All four types present |
| 2(d) | Continuous-variable Q-Q and density plots | Present for seven variables; additional-candidate scope risk |
| 2(e) | Potential nonlinearities and transformations | Covered; existing log-density check and persistent RESET concern |
| 2(f) | Outlier methods and discussion | IQR plus standardized/studentized-residual and influence discussion; no automatic deletion |
| 2(g) | Missingness patterns, treatment/imputation justification, sensitivity | Covered: 44 missing incomes in two tracts, no imputation, restore-44 sensitivity |
| 2(h) | Findings from Pandas Profiling | Actual saved run and alert interpretation present; fresh replay blocked |
| 3(a) | Boruta with documented parameters | Covered; pinned Boruta, seeded fit and selection output |
| 3(b) | Mallows Cp | Covered; full-model variance, 4,095 subsets and results |
| 3(c) | VIF | Covered; full/reduced/selected tables |
| 3(d)-1 | Simple model with theoretically most important predictor | Covered: price-only Model 1 |
| 3(d)-2 | Model with 2–3 key predictors | Covered: three slopes in Model 2 |
| 3(d)-3 | Model including all statistically significant predictors | Unresolved candidate-set/significance interpretation |
| 3(d)-rationale | Economic/statistical justification for the competing models | Present; significance reconciliation still needed |
| 3(e) | AIC, BIC, adjusted R² **and** CV comparison | All four present; same common sample |
| 3(f) | Final model and detailed economic/statistical justification | Present; preference is among three fixed specifications |
| 4(a) | Residual/fitted plots **and** RESET | Both present; unfavorable result retained |
| 4(b) | BP, White **and** scale-location | All three present; HC1 comparison distinguishes covariance from mean specification |
| 4(c) | Residual Q-Q, JB **and** histogram | All three present |
| 4(d) | Cook plot, leverage/residual plot **and** DFBETAS | First two present; DFBETAS Missing |
| 4(e) | 1,000-replication coefficient bootstrap compared with OLS | Present for all eight parameters including intercept; seed 90095 |
| 4(f) | Five- **or** ten-fold CV and out-of-sample accuracy | Present: five training-only folds, RMSE, seed 10 |
| 4(g) | OLS violations and implications | Present: variance, mean, dependence, boundedness and causal limits |
| 5(a) | Professional final regression table | Present; estimates, conventional/HC1 uncertainty distinguished |
| 5(b) | ALL coefficients, economic magnitude/direction/units | Seven slopes plus intercept covered; effects in occupancy percentage points |
| 5(c) | Statistical versus economic significance | Covered; uncertain terms are not hidden |
| 5(d) | Key confidence intervals calculated and interpreted | Covered; HC1 price interval approximately 5.11–6.02 pp per dollar |
| 5(e) | R²/model fit in economic context | Covered; R² about 0.274 and held-out RMSE about 16.53 occupancy pp |
| 5, p.4 | Compare final results with literature | Partial: developed comparison absent |
| 6(a) | Data, methodological and scope limitations | Covered |
| 6(b) | Bias sources and implications | Covered; no invented net bias direction |
| 6(c) | Policy implications if applicable | Covered with appropriate causal caution |
| 6(d) | Concrete future research | Covered; sensor cutoffs/day/Sunday plans and future/location validation |
| 6(e) | External validity/populations/contexts | Covered; restricted sensor-equipped LA spaces and August 2025 scope |
| 7-comments | Commented Python and clear section headers | Present; final editorial consistency needs review |
| 7-seeds | Reproducible analysis and random seeds | Seeds present; environment/raw-rebuild evidence incomplete |
| 7-efficiency | Efficient/readable code | Broadly present; exhaustive Cp over only 12 candidates is not automatically a violation |
| 7-generation | Programmatically generated figures/tables | Producing code present; copied historical summaries are labeled references to actual generating code |

## Dataset and submission checklist

Fresh read-only CSV checks reconfirmed 4,139 rows, 36 columns and 4,139 unique SpaceIDs; 4,060 FLAT/TOD spaces; 4,016 common complete cases in 45 tracts; 44 missing incomes. These are the unchanged processed files, not a fresh raw reconstruction.

| Requirement | Finding |
|---|---|
| At least 500 observations | Met: 4,016 common regression observations |
| At least five potential predictors | Met: 12 encoded candidates and seven final slopes |
| Appropriate cross-sectional structure | Met structurally: one observation per space, monthly outcome; assumptions/limits disclosed |
| Use an example dataset listed in PDF | Not required: PDF allows any chosen dataset |
| Economic motivation/hypothesis | Present as report content |
| Data description | Present as report content |
| Methodology | Present as report content |
| Results and coefficient interpretation | Present as report content |
| Limitations | Present as report content |
| Conclusion | Present as report content |
| References | Academic/data citations present; consolidated final bibliography pending |
| Python source | Present in notebooks; inclusion in final submitted artifact pending |
| One report per group | No final assembled report located |
| All group members’ names | No verified complete report roster located |
| PDF/HTML submission | Missing student deliverable; only the professor’s assignment PDF exists |
| Review syllabus Assignment Policies | Not verified; syllabus unavailable |
| Submission by deadline | No actual submission verified; PDF lists October 30, 2026 |

## What should not be mistaken for a missing rubric requirement

- The rubric does not set a minimum R², require the price coefficient to be negative, require all null tests to be favorable, or require a causal identification strategy. Reporting unfavorable outcomes honestly is appropriate.
- It requires **five or ten** folds, not both. The existing five-fold implementation meets that method requirement. Selection leakage and shared-neighborhood folds limit interpretation and are disclosed; a completely different validation design is not separately mandated.
- Clustered/spatial inference, 12/48-hour sensor rebuilds, 20-day expansion, Sunday comparisons and alternative outcome models can improve research, but are not separately enumerated mandatory diagnostics. Their absence should not be counted as automatic named-item deductions.
- Boruta importance, low VIF and coefficient p-values answer different questions. None alone proves compliance with the Model 3 wording.
- Programmatically constructed reference tables are not automatically nonprogrammatic merely because they contain copied values, provided the actual generating analysis and provenance remain. Replacing copied references with derived artifacts would strengthen reproducibility, but the prior audit’s “Partial” label should not be interpreted as proof of a separate missing plot/table requirement.

**Final readiness judgment:** the analysis is substantial and mostly covers the rubric, but **130/130 is not currently defensible**. DFBETAS and the final submission are definite gaps; the remaining items above are the specific content and reproducibility risks to resolve. Only the professor can award the final grade or waive a requirement.
