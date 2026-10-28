# Second full Project 1 audit

This pass reread the assignment PDF and inspected the current six report notebooks, combined notebook, saved results, exported HTML and Python source. It also repeated the supporting visualization runs and the cleaning-notebook static checks. The checks used the current saved files rather than headings or earlier completion claims.

## Findings by component

| Component | Finding |
|---|---|
| Dataset requirements | Verified 4,016 regression observations, 12 candidate predictors and one cross-sectional observation per parking space. |
| 1. Theory and hypothesis | Research question, testable price hypothesis, expected signs and illustrative magnitude benchmark are present. The three literature-review paragraphs and results-to-literature comparison paragraphs remain unchanged. Both cited academic sources were located in the institutional repository. |
| 2. Data description and EDA | Sources, periods, selection and definitions are present. Required descriptive statistics and both kurtosis conventions are calculated. Histograms, boxplots, heatmap, key scatterplots, Q-Q/density panels, outlier screens, missingness patterns, justified no-imputation strategy and actual Profiling findings are saved. The restored-income sensitivity is implemented in Section 4. |
| 3. Selection and models | Boruta parameters and seed, exhaustive 4,095-subset Cp search and VIFs are implemented. Model 1 has one slope; Model 2 has three; Model 3 contains the seven full-candidate slopes meeting the declared 5% screen. AIC/BIC/adjusted R² and actual common-fold errors are compared. Selection and spatial-validation limitations are explicit. |
| 4. Diagnostics | Actual residual/fitted, RESET, BP, White, scale-location, Q-Q, JB and histogram evidence is saved. Cook/leverage plots, coefficient-labeled row-aligned DFBETAS and both internally standardized and externally studentized residual screens are present. The 1,000-draw bootstrap and five-fold predictions were independently reproduced. Violations and implications are discussed. |
| 5. Interpretation | Every slope and the intercept are covered. The final table, HC1 standard errors, p-values and 95% intervals match an independent refit. Economic comparisons use the correct dollar, density, registration and share units. Fit and predictive error are distinguished from causal identification. |
| 6. Limitations and extensions | Data timing, endogeneity, measurement, sample selection, dependence, functional form, bounded predictions, policy scope, external validity and concrete extensions are retained. |
| 7. Reproducibility | All six sections and the combined notebook passed fresh-kernel execution. Random seeds, full source appendices and execution versions are documented. Numerical results agree across notebooks/exports. Processed CSVs match Git HEAD exactly. |

## Fixes made in this pass

1. Made the internally standardized-residual screen explicit at |residual| > 2, alongside the existing externally studentized screen. It flags 195 spaces; it does not delete observations or change the model.
2. Corrected the stray comma in the extensions sentence and standardized the Section 2 title.
3. Specified the predictors of the seven-predictor sensitivity model in prose so its role in the comparison table is unambiguous.
4. Corrected the combined notebook's reference to source “below” to “accompanying source,” which is accurate in both notebook and HTML formats.
5. Added an institutional open-access copy to the references for Pierce and Shoup (2013), without editing protected literature paragraphs. The older UCLA URL redirects to cloud storage inaccessible to the audit browser; this is not proof that the URL fails for ordinary readers. Repository copy: [Getting the Prices Right](https://escholarship.org/uc/item/2h76j73j). Shoup (2006) was also accessible: [Cruising for Parking](https://escholarship.org/content/qt55s7079f/qt55s7079f.pdf).
6. Added `src/run_report_notebooks.py` to reproduce the independent-kernel workflow using the active compatible Python environment. Execution records now include source/code fingerprints.
7. Strengthened verification to compare combined analysis code with individual-section code and ensure recorded executed code matches the saved source. Later Markdown-only refinements are identified explicitly in the execution records.
8. Changed the package-version table to use recorded execution versions, and refreshed the combined report, HTML and Python exports.

These changes do not alter the data, selected predictors, fitted coefficients, uncertainty estimates or earlier numerical findings.

## Independent numerical checks

A separate calculation reproduced:

- The final-model predictor screen and all fitted coefficients.
- Every final-table HC1 standard error, p-value and confidence interval.
- Breusch–Pagan, White, RESET and Jarque–Bera statistics and p-values.
- DFBETAS column labels, observation alignment, maxima, coefficient flag counts and total flagged spaces.
- All 1,000 seeded row-bootstrap draws using NumPy least squares, matching the displayed means, standard errors and percentile intervals.
- Training-only predictions on all five common folds, with every observation held out exactly once.

Final mean fold RMSEs are 0.17756368, 0.16820783 and 0.16279557 for Models 1–3. The model and data are unchanged from the first completed audit. Detailed evidence is in `submission_second_audit_independent.json` and the refreshed execution/verification JSON files.

## Remaining submission details and limits

- Group-member names are still absent from `reports/submission_metadata.json`.
- Review of the syllabus Assignment Policies is not confirmed.
- Literature prose is intentionally unchanged for the authors' final review.
- Raw transactions and original spatial inputs are absent. The cleaning notebooks passed schema, syntax and saved-output checks; the raw construction pipeline was not rerun.
- The HTML was checked for embedded figures, working internal links, complete source appendices and untruncated table text. This pass does not claim an interactive-browser layout review.
- No commit, push or course submission was performed.
