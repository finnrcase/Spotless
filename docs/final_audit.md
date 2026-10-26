# Final ECON 430 audit and corrections

Reviewed October 22, 2026. This report covers the current Spotless workspace, especially Notebooks 05–08. The original audit made no commit or push; the user subsequently authorized publication on October 25, 2026.

The review used the actual `project1-1.pdf` assignment and 130-point rubric, the available Regression Lectures 0–2 and their numbered copies, `Case_1_430_Lab.ipynb`, Notebooks 01–08, README, saved outputs and the existing cross-section. Course materials were read from the local Downloads folder; they were not copied into the repository.

## Issues ranked by severity

| Priority | Issue found | Correction or remaining limitation |
|---|---|---|
| High | Strong heteroskedasticity makes conventional uncertainty an unsuitable default final presentation | Verified BP/White; Notebook 08 presents HC1 SEs, p-values and confidence intervals, with conventional inference separately labeled |
| High | RESET strongly rejects the original mean specification | Verified test and inspected residual plots; added the lecture's natural-log density alternative. RESET still rejects, so the concern remains disclosed |
| High | Model 2 had four predictors despite the mandatory 2–3 requirement | Removed time limit from Model 2 only. Updated fits, metrics, CV and prose throughout 06–08; Model 3 remains unchanged |
| High | Required DFBETAS is absent | Still outstanding. No worked example was found in the available lectures/lab; implementing it would violate the requested lecture-only restriction |
| High | 4,016 spaces share 45 tracts; several predictors repeat within tracts | Explained correlated errors and the limits of HC1, row bootstrap and random-fold CV. No lecture example of clustered inference was found, so none was added |
| High | Existing Notebook 08 was a placeholder | Completed that exact file with literature, sample/EDA, selection, final table, economic interpretation, model comparisons, diagnostics, robustness, limitations, conclusion and compliance checklist |
| Medium | Model 3 is not a significance-only subset of candidate predictors | Original seven retained as instructed; time limit and transit share are explicitly insignificant. The rubric's significance-based wording needs instructor clarification; no claim that all included terms are significant |
| Medium | Predictor Q-Q/density plots and Pandas Profiling discussion were missing from the existing EDA | Added lecture-level plots and actual Profiling summary/alerts in Notebook 08; no additional cleaning |
| Medium | Missing-income exclusion had no completed sensitivity comparison | Compared the unchanged 4,016-space common sample with all 4,060 FLAT/TOD spaces. Income is not a final regressor, so no imputation is needed |
| Medium | Minimum-active-day and sensor-interval sensitivities were unfinished | Completed a 28-day restriction using existing data. Interval-cutoff, 20-day expansion and Sunday-reporting checks remain uncompleted; documented raw-processing requirements |
| Medium | Data vintages, price endogeneity and midpoint meaning limit interpretation | Kept these limitations prominent; no causal or instantaneous-availability claim |
| Medium | Random-fold results can be optimistic for new neighborhoods and after selection | Disclosed that nearby/same-tract spaces can occur in both folds and selection preceded validation. Training-only regression fits are preserved; no advanced validation design added |
| Low | Duplicate best-eight Cp display in Notebook 05 | Removed the exact duplicate; all remaining analytical code and selection results preserved |
| Low | Notebook 05 installed Boruta during analysis; dependencies were undeclared | Removed the installation cell and declared the existing course tools in requirements: Boruta 0.4.3 and ydata-profiling 4.18.4 |
| Low | README still described 05–08 as unimplemented shells | Corrected statuses, sample/model definitions, completed checks, results, seeds and remaining gaps |
| Submission | Final PDF/HTML group report was not packaged | Still pending: member names and final PDF/HTML packaging with Python source; nothing was submitted |

## What changed

- **05:** removed duplicate best-eight Cp output and replaced runtime package installation with an environment note. Boruta, subset search, VIF calculations and selected variables are unchanged.
- **06:** corrected Model 2 to price, population density and food-service/retail count; propagated its estimates, predictor count and five-fold results. Models 1 and 3 and the common sample are unchanged.
- **07:** reproduced the corrected model comparison; added log-density, 28-day and missing-income sensitivities; updated CV references and assignment status. Preserved the original diagnostics, influence results and 1,000-draw bootstrap.
- **08:** completed the existing notebook, including an HC1 final table and all requested report sections. Reused verified selection, bootstrap and CV results rather than repeat expensive calculations.
- **README/requirements:** corrected stale documentation and declared already-required course packages.

## Updated model comparison

Every primary comparison uses the same 4,016 observations. Predictor counts exclude the intercept. CV is shuffled five-fold RMSE with seed 10, with a new fit on each training fold.

| Model | Predictors | Price coefficient | Adjusted R² | AIC | BIC | Mean CV RMSE |
|---|---|---:|---:|---:|---:|---:|
| 1 | Price | 0.054515 | 0.156565 | -2483.67051 | -2471.07443 | 0.177564 |
| 2, corrected | Price, population density, food-service/retail count | 0.059991 | 0.242932 | -2915.51726 | -2890.32509 | 0.168208 |
| 3, primary | Model 2 plus time limit, drive-alone share, transit share and TOD | 0.055633 | 0.272354 | -3070.71241 | -3020.32808 | 0.165315 |

Only Model 2's primary estimates changed. Model 3 still has ordinary R² 0.273623. Its CV improvement over corrected Model 2 is about 0.29 occupancy percentage points of RMSE.

### Primary coefficients and HC1 inference

Coefficients use occupancy fractions, not percentage points. TOD compares TOD with FLAT. Density is people per square mile and commuting shares are fractions.

| Term | Coefficient | Conventional SE | HC1 SE | HC1 p-value | HC1 95% CI |
|---|---:|---:|---:|---:|---|
| Intercept | 0.456337 | 0.015794 | 0.017116 | 1.29e-156 | [0.422792, 0.489883] |
| Price midpoint | 0.055633 | 0.002361 | 0.002322 | 7.93e-127 | [0.051081, 0.060184] |
| Time limit, hours | 0.004879 | 0.002948 | 0.003137 | 0.1199 | [-0.001269, 0.011028] |
| Population density | 4.57052e-6 | 2.21771e-7 | 2.37074e-7 | 8.08e-83 | [4.10586e-6, 5.03518e-6] |
| Nearby food-service/retail registrations | -0.000321282 | 2.29852e-5 | 2.42980e-5 | 6.50e-40 | [-0.000368905, -0.000273659] |
| Drive-alone share | -0.198101 | 0.020831 | 0.021101 | 6.09e-21 | [-0.239458, -0.156744] |
| Transit share | 0.019647 | 0.046836 | 0.045213 | 0.6639 | [-0.068968, 0.108262] |
| TOD indicator | 0.033004 | 0.007316 | 0.008571 | 1.18e-4 | [0.016206, 0.049802] |

**Price interpretation is unchanged:** a $1 higher price proxy is associated with about **5.56 percentage points higher monthly occupancy**, holding the included variables constant. HC1 gives a 95% interval of about **5.11–6.02 percentage points**. This is not a causal effect, elasticity, actual payment comparison or probability of finding a space at a particular time.

Time limit and transit share are not individually significant at 5%. Higher commercial count and drive-alone share have negative conditional estimates, which should not be recast as causal effects or suppressed because they differ from simple expectations.

## Verified diagnostics and robustness

| Check | Verified result | Interpretation |
|---|---|---|
| BP, default Koenker LM version | p = 3.37378e-41 | Reject constant variance |
| White LM | p = 4.75468e-63 | Reject constant variance |
| RESET, squared fitted term | F = 122.07775; p = 5.60494e-28 | Functional-form concern remains |
| Jarque–Bera | 3.83598; p = 0.146902 | Do not reject normality; does not validate other assumptions |
| Influence screens | 249 Cook, 136 leverage, 189 studentized-residual flags; overlapping groups | Inspection flags, not confirmed errors or permanent deletions |
| Fitted values outside [0,1] | 4 | Unclipped; bounded-outcome limitation disclosed |
| Cook <= 4/n sensitivity | N = 3,767; price = 0.054769 | Sign remains positive; selected-sample fit improvement is not proof of superiority |
| Log population density | N = 4,016; price = 0.055160; adjusted R² = 0.273255; AIC = -3075.68630 | Small fit/price change; RESET still rejects, p = 1.41594e-19 |
| At least 28 active days | N = 1,609; price = 0.049628; HC1 CI [0.041057, 0.058199] | Positive association in a different, stricter sample; interval definition unchanged |
| Restore missing-income spaces | N = 4,060; price = 0.057162; HC1 CI [0.052560, 0.061763] | Sign survives the original common-sample exclusion; no income imputation |
| Row bootstrap | 1,000 draws; price mean 0.055485, SE 0.002374, percentile CI [0.050914, 0.060106] | All coefficient distributions summarized in 07; independent-row assumption remains |

HC1 addresses heteroskedastic covariance under independence. It does not fix shared-tract errors, misspecification, endogeneity, temporal misalignment or selection. Ordinary row bootstrap has the same independence limitation.

## Unchanged work and remaining gaps

Raw and processed datasets were not written. Notebooks 01–04, occupancy construction, all original filters and variable definitions, source paths, geographic matching, business radius, the 4,139-space saved cross-section, 4,016-space primary sample and seven-variable Model 3 are unchanged. Sensitivity restrictions exist only in memory and do not remove source observations.

**Known mandatory gap:** DFBETAS remains outstanding because it is explicitly required but no worked course example was found. Under the lecture-only instruction, it was flagged rather than improvised. **Rubric clarification:** Model 3 includes all individually significant terms within its own specification, but is not the significance-only model across all candidates; time limit and transit share remain. The user's instruction to keep the original seven-variable model was followed.

A different sensor-interval cutoff requires rereading/sorting 3,707,820 transactions, reconstructing next-event durations before UNKNOWN filtering, and aggregating new occupied/valid minutes. A 20-day expansion also requires recovering newly eligible spaces and verifying their predictor linkage. These raw-data changes were not performed. Interval/20-day/Sunday checks are useful project sensitivities, not separately named mandatory rubric items; the 28-day check must not be described as completing all of them.

## Requirement-by-requirement checklist

| Rubric | Requirement | Status / evidence |
|---|---|---|
| Theory, 15 points | Question, 2–3 literature paragraphs, two academic sources | Complete in 08 Section 1: Shoup (2006), Pierce and Shoup (2013), linked to academic sources |
| Theory | Testable hypothesis, signs and magnitudes | Complete; negative starting price hypothesis, signs discussed, no unsupported numeric prior |
| Data/EDA, 25 | Cross-section, >=500 rows, >=5 potential predictors; sources, period, definitions | Complete, Notebooks 01–04 and 08 Sections 1–2 |
| Data/EDA | Mean, median, SD, min/max, skewness, kurtosis | Complete, 04 and 08 |
| Data/EDA | Histograms, boxplots, scatterplots, correlation heatmap | Complete in 04 |
| Data/EDA | Continuous-variable density and Q-Q plots, nonlinearities | Complete in 08; functional-form comparison in 07 |
| Data/EDA | IQR/residual outliers, missingness, treatment rationale and sensitivity | Complete, 04/07/08; no imputation of final regressors needed |
| Data/EDA | Pandas Profiling findings | Complete, 08: 4,060 rows, 44 missing cells in income; unique-value/zero alerts discussed |
| Selection, 25 | Boruta, stated parameters | Complete in 05; fixed seed 10 |
| Selection | Mallows' Cp and VIF | Complete in 05; global Cp optimum and preferred seven distinguished |
| Selection | Model 1 one predictor; Model 2 two or three | Complete: 1 and 3 predictors |
| Selection | Model 3 significance-based wording | Clarification needed; original seven retained transparently, not every term significant |
| Selection | Adjusted R², AIC, BIC, CV, model justification | Complete, 06/08; preference among the three fixed models |
| Diagnostics, 20 | Residual/fitted, RESET | Complete in 07; unfavorable result retained |
| Diagnostics | BP, White, scale-location | Complete in 07; HC1 final presentation in 08 |
| Diagnostics | Residual Q-Q, JB and histogram | Complete in 07 |
| Diagnostics | Cook, leverage, DFBETAS | Partial: Cook/leverage done; DFBETAS outstanding under lecture-only restriction |
| Diagnostics | Bootstrap >=1,000, compare coefficients with OLS | Complete for all primary coefficients in 07 |
| Diagnostics | Five OR ten folds; out-of-sample predictions | Complete: five folds in 06, training-only fits; validation limits disclosed |
| Results, 25 | All estimates, SEs, p-values and CIs; economic units | Complete in 08 with HC1 and conventional inference distinguished |
| Results | R², fit/prediction and statistical versus economic significance | Complete, 06/08; insignificant terms retained visibly |
| Limitations, 10 | Bias, policy relevance, external validity, extensions | Complete, 07/08; no causal pricing recommendation |
| Code, 10 | Readable executable source, generated output and reproducible seeds | Modified notebooks freshly executed; seed 10 for selection/CV and 90095 for bootstrap |
| Submission | One PDF/HTML group report, names, Python source | Pending final packaging/submission; notebooks contain the source and evidence |

## Execution and integrity verification

- Notebooks **05, 06, 07 and 08** each executed successfully from fresh kernels, with no error outputs. The last Notebook 08 run also has no warning outputs. All code cells have execution counts.
- Notebooks **01–04** were reviewed and their saved outputs contain no errors; they were **not freshly executed**, to avoid rewriting the construction outputs. This audit does not claim a fresh end-to-end rebuild of all eight notebooks.
- Checked notebook format validity, model specifications/sample sizes, updated Model 2 prose, matching coefficients/HC1 tables across 07–08, reference CV metrics against executed 06, and bootstrap references against executed 07. Residual and predictor plots were rendered and visually inspected.
- All remaining Notebook 05 analytical code matches the prior version exactly after removing the installation and duplicate cells.
- The **three processed CSV SHA-256 hashes** match the pre-edit baseline. All **66 raw-file sizes and modification times** match the baseline; no new data files were created. Notebooks 01–04 also match their pre-edit hashes.
- `parking_cross_section.csv` SHA-256: `644615c218966773b367f902dd9e559f081dfe78023374f0fbc9aa6a1dafbb70`.
- Package verification used a temporary isolated environment with access to the existing scientific packages; installing course-required Profiling did not downgrade the global matplotlib installation.
- No classes, custom statistical framework, new advanced estimator, clustered SEs or DFBETAS implementation was introduced. The existing project-requested Cook **4/n** threshold is the sole screening rule noted as not coming from a worked lecture cutoff. Log transformation, HC1 and all added comparisons use the demonstrated elementary methods.
- No raw acquisition, permanent row removal, imputation, source-variable redefinition or overwrite of the data occurred during this audit. The initial audit did not commit or push; subsequent publication was explicitly requested by the user.

## October 25 follow-up: time-limit inference

Verified the prior four-predictor Model 2 against its committed output and a refit on the same 4,016-space common sample. Its time-limit coefficient is **0.003648375**, conventional SE **0.002946629**, p **0.215732**. Model 3 gives **0.004879287**, conventional SE **0.002947964**, p **0.097975**; its HC1 SE is **0.003137173**, p **0.119871**. The row indices align exactly, and the only additional predictors in that historical comparison are drive-alone share, transit share and TOD.

The changed coefficient and p-value reflect conditioning on these additional controls, with almost unchanged conventional SE, rather than a sample or alignment error. Neither conventional estimate reaches 5%; Model 3 only reaches 10% conventionally and does not do so under HC1. A short explanation was added to Notebook 06, explicitly distinguishing the historical four-predictor comparison from the corrected three-predictor Model 2. No model was changed to seek significance.

Read-only format inspection also found that unchanged Notebooks 01–04 declare notebook minor version 4 while containing cell IDs supported by minor version 5. Modern nbformat reads them and their saved outputs contain no errors, but strict validation against their declared older schema rejects those IDs. Their files were left unchanged; schema validation passes for the modified Notebooks 05–08.
