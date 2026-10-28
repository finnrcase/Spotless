# Verified coverage: Project 1 Sections 2–7

This record follows the user-provided requirements. Section 1 was excluded from revision and is byte-for-byte unchanged. This checklist is separate from the teacher-facing report.

| Requirement | Result | Saved evidence |
|---|---|---|
| 2(a): sources, periods, selection and variable definitions | Verified | Notebook 02; cells 3, 5, 7, 9 |
| 2(b): mean, median, SD, min, max, skewness and kurtosis | Verified | Notebook 02; cells 11 |
| 2(c): histograms/boxplots | Verified | Notebook 02; cells 15 |
| 2(c): scatterplots | Verified | Notebook 02; cells 16 |
| 2(c): correlation heatmap | Verified | Notebook 02; cells 17 |
| 2(d): continuous-variable Q-Q and density plots | Verified | Notebook 02; cells 20 |
| 2(e): nonlinearities and transformations | Verified | Notebook 02; cells 23, 24 |
| 2(f): IQR outliers and interpretation | Verified | Notebook 02; cells 27 |
| 2(f): standardized residuals | Verified | Notebook 04; cells 35 |
| 2(g): missingness patterns | Verified | Notebook 02; cells 32 |
| 2(g): justified treatment, explicit imputation and sensitivity | Verified | Notebook 02; cells 34, 35 |
| 2(h): actual Pandas Profiling findings | Verified | Notebook 02; cells 37 |
| 3(a): Boruta fitting and findings | Verified | Notebook 03; cells 5, 7 |
| 3(b): exhaustive Cp calculation and interpretation | Verified | Notebook 03; cells 10, 15 |
| 3(c): VIFs and selected-model interpretation | Verified | Notebook 03; cells 29, 30 |
| 3(d): three fitted models and significance rule | Verified | Notebook 03; cells 22, 24, 26, 28 |
| 3(e): AIC/BIC/adjusted R2 and actual CV | Verified | Notebook 03; cells 32 |
| 3(f): economic and statistical final-model justification | Verified | Notebook 03; cells 36 |
| 4(a): residual vs fitted | Verified | Notebook 04; cells 14 |
| 4(a): RESET | Verified | Notebook 04; cells 17, 21 |
| 4(b): BP, White and scale-location | Verified | Notebook 04; cells 25 |
| 4(c): residual Q-Q and Jarque-Bera | Verified | Notebook 04; cells 31 |
| 4(c): residual histogram | Verified | Notebook 04; cells 14 |
| 4(d): Cook and leverage vs residual plots | Verified | Notebook 04; cells 37 |
| 4(d): coefficient-labeled, row-aligned DFBETAS | Verified | Notebook 04; cells 40 |
| 4(e): 1,000 bootstrap estimates compared with OLS | Verified | Notebook 04; cells 49 |
| 4(d): DFBETAS plot | Verified | Notebook 04; cells 41 |
| 4(d): DFBETAS interpretation and screening caveat | Verified | Notebook 04; cells 42 |
| 4(f): fixed-model five-fold held-out accuracy | Verified | Notebook 04; cells 54 |
| 4(f): training-only selection validation | Verified | Notebook 04; cells 57 |
| 4(g): OLS violations and implications | Verified | Notebook 04; cells 66, 67 |
| 5(a): final regression table | Verified | Notebook 05; cells 4 |
| 5(b): every coefficient and intercept in economic units | Verified | Notebook 05; cells 6 |
| 5(c): statistical versus economic significance | Verified | Notebook 05; cells 9 |
| 5(d): calculated key-parameter intervals and interpretation | Verified | Notebook 05; cells 12 |
| 5(e): model fit in economic context | Verified | Notebook 05; cells 14 |
| 6(a): limitations | Verified | Notebook 06; cells 3 |
| 6(b): bias | Verified | Notebook 06; cells 5 |
| 6(c): policy | Verified | Notebook 06; cells 7 |
| 6(d): extensions | Verified | Notebook 06; cells 9 |
| 6(e): external validity | Verified | Notebook 06; cells 11 |
| 7: clear section headers and documented methods | Verified | Combined report, source appendix and execution records |
| 7: seeded reproducibility and pinned input/version information | Verified | Combined report, source appendix and execution records |
| 7: readable and bounded computation | Verified | Combined report, source appendix and execution records |
| 7: programmatically generated figures and analytical/definition tables | Verified | Combined report, source appendix and execution records |

## Additions made to meet the requirements explicitly

- Expanded source, date, sample-selection and variable definitions, including the dummy reference categories and supporting construction fields.
- Rendered definition/source tables programmatically; descriptive statistics now also cover both indicators, alongside category counts.
- Added binned nonlinearity plots and specific discussion of their shape, suitable transformations and the limits of marginal patterns.
- Added an explicit median-imputation-plus-missingness-indicator sensitivity, alongside complete-case/no-income sample comparisons. Observed income values and the primary analysis are unchanged.
- Added result-specific Boruta, global Cp and selected-model VIF interpretation, economic model rationale and quantitative final-model justification.
- Added direct interpretation of the price confidence-interval endpoints in economic units.
- Added actual five-fold training-only predictor selection, retaining the fixed-model comparison. Selection-procedure RMSE is approximately 0.16333, versus 0.16280 for the fixed selected specification.
- Made report data loading work from the repository root or notebook directory. Added a commit-pinned CSV reference, file hash and recorded execution versions to Section 7.
- Reexecuted Sections 2–6 and the combined notebook in fresh project-root kernels. All 45 requirement/output checks passed; data and final-model parameters are unchanged.

## Boundary between analytical coverage and submission details

Every listed analysis requirement in Sections 2–7 has implemented code or substantive prose and verified saved evidence. Tests that reject OLS assumptions are reported honestly; completing a diagnostic does not imply the assumption holds.

The assignment separately requires group-member names and review of the syllabus Assignment Policies. The names have not been provided and the review has not been confirmed. These cannot be completed by inventing author information or marking an unperformed review as done.

The main analysis is reproducible from the fixed processed CSV linked in Section 7. Original raw transactions and spatial inputs are absent, so raw-data reconstruction is not represented as reexecuted. The source is included for transparency.

No commit, push or course submission was performed.
