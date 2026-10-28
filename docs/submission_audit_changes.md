# Project 1 submission audit and changes

The four-page assignment `project1-1 (1).pdf` was checked against the six report notebooks, their actual Python calculations and saved outputs, the combined notebook, and the final HTML export. This log is separate from the teacher-facing report.

## Changes to the report notebooks

| File | Changes |
|---|---|
| `01_economic_theory.ipynb` | Removed project navigation, execution instructions, repeated rubric/status wrappers and the duplicate historical report. Retained the research question, hypothesis, expected-sign/magnitude discussion and the current literature-review paragraphs verbatim. |
| `02_data_description_eda.ipynb` | Kept the existing wording and EDA. Added Pearson kurtosis beside the already labeled excess kurtosis; fixed links to the actual diagnostic subsections; replaced repository-only source links with a self-contained reference to the report sources. Kept full table text and suppressed irrelevant Profiling progress-bar output. Retained the missingness patterns, justified no-imputation choice and restored-income sensitivity interpretation. |
| `03_variable_selection_models.ipynb` | Removed historical duplicates, authorization notes, checklists and completion claims. Kept the declared full-candidate 5% predictor screen and one-/three-/seven-slope competing models. Made Boruta settings explicit and seeded its forest; replaced internal model labels with `Model 3` and `Seven-predictor sensitivity`. Retained Cp, full/reduced/selected VIFs, actual five-fold comparison, economic reasoning and post-selection caveats. Suppressed the character-count output from writing an exported JSON file. |
| `04_diagnostics_robustness.ipynb` | Corrected a cross-section inconsistency: diagnostics had still used the earlier seven-predictor model, while Sections 3/5 used the selected final model. Now the identical final predictor definition is used everywhere. Restored required standalone diagnostic imports and the TOD indicator for expanded-sample sensitivity. Recomputed all tests, influence results, DFBETAS, 1,000 bootstrap draws and actual five-fold predictions. Replaced stale numerical prose with programmatically generated interpretations. Moved log-density sensitivity into Linearity and arranged its HC1 dependency before use. Retained the two readable diagnostic-summary tables and all substantive caveats. |
| `05_results_interpretation.ipynb` | Removed duplicate historical results and internal scaffolding. Retained the final regression table, all coefficient and intercept interpretations, HC1 intervals, economic/statistical significance discussion, fit/prediction results and literature-comparison paragraphs. Simplified the conclusion and model labels; suppressed export character-count output. |
| `06_limitations_extensions.ipynb` | Removed duplicate historical report, checklists and course/process commentary. Kept substantive limitations, bias, policy, extensions and external-validity discussion. Updated the diagnostic caveat and replaced project-only data-reference links with public source endpoints. Academic reference entries and literature-review prose were not rewritten. |
| `Spotless_complete.ipynb` | Rebuilt from the cleaned, executed report sections so it no longer contains a different or obsolete analysis. Added the code-quality/reproducibility section, seeds and tested package versions. Verified complete execution in a fresh kernel. |

## Supporting notebooks and reproducibility files

- `notebooks/cleaning/03_build_cross_section.ipynb`: replaced two stale notebook-number references in Markdown. Cleaning code and existing outputs were not altered.
- All three cleaning notebooks: checked schema, Python syntax, source paths and saved outputs. Raw inputs are absent, so the raw construction pipeline was not rerun.
- `Visualization/01_cumprice.ipynb`: removed unused optional-package/classroom boilerplate and added an accurate supplementary-exploration title and sample description; retained the exploratory calculations.
- `Visualization/Dip_analysis_3_25_to_4_25.ipynb`: removed a stale TODO, corrected leading indentation in two cells and identified its full-sample exploratory scope. No change to the price interval or data analysis.
- Executed both supplementary notebooks from fresh kernels.
- `requirements.txt`: pinned the two statistical-library versions already used by the project and added `setuptools<81`, required by the existing Profiling package. Used an isolated Python 3.12 environment; no replacement data or model results were invented.
- `src/build_submission_report.py`: exports the reviewed combined notebook, self-contained HTML with embedded plots, analysis Python source and cleaning Python source.
- `src/audit_submission_report.py` and `src/verify_current_report.py`: verify the actual reviewed files rather than the former historical-appendix/cancelled-DFBETAS assumptions. Checks include section order, saved output types, lack of errors/truncated table text, coefficient/predictor consistency, 1,000 bootstraps, held-out accuracy, literature preservation and unchanged processed data.
- `src/complete_rubric.py`: prevents its obsolete baseline builder from silently overwriting the reviewed final report.
- Refreshed the three `reports/tables/current_*.json` files from the actual executed analysis. Rebuilt `reports/Spotless_ECON430_Project1.html`, `reports/Spotless_ECON430_source.py` and `reports/Spotless_cleaning_source.py`.

## Material consistency correction

The final Model 3 defined in Sections 3 and 5 has predictors:
`price_midpoint`, `population_density`, `nearby_restaurant_retail_count`, `transit_share`, `walk_share`, `nearby_business_count`, and `RateType_TOD`.

Section 4 previously diagnosed a different model containing time limit and drive-alone share instead of walk share and total businesses. The audit retained the final-model selection rule and corrected Section 4 to match it. Consequently, the correct final price association is **5.15 occupancy percentage points per dollar**, not the earlier alternative model's 5.56. Final Model 3's residual Jarque–Bera p-value is **0.01764**, so the normality null is rejected at 5%; the prior model's nonrejection no longer describes the final model. Breusch–Pagan, White and RESET still reject their respective nulls. These are model-consistency corrections, not changes to the data or an attempt to obtain preferred significance.

All final estimates describe conditional associations; endogenous prices, source-date differences, selection uncertainty, correlated neighborhood errors and functional-form concerns remain disclosed.

## Verification and remaining submission details

- All six report notebooks passed execution from independent clean kernels.
- The rebuilt combined notebook passed full clean-kernel execution.
- The final report has 4,016 observations and 12 original candidate predictors, exceeding the assignment's minimum sample and candidate requirements.
- DFBETAS has coefficient labels, verified row alignment, saved tables/plots and interpretation for the actual final model; the cutoff is explicitly a screening rule.
- Numerical checks confirm matching coefficients, predictor lists and CV results across Sections 3–5.
- Processed CSVs match the Git HEAD contents exactly. Their hash differences from an older Windows manifest predate this audit; the audit did not change them.
- The HTML contains embedded figures and full analysis/construction Python source, working internal section links and no truncated table entries. Saved figure outputs were visually inspected. An interactive browser was unavailable, so full-browser layout review could not be performed here.
- The literature-review and literature-comparison paragraphs were left unchanged for the authors' review.
- **Group members' names remain absent** from `reports/submission_metadata.json`; the assignment requires them on the submitted report.
- **Syllabus Assignment Policies review is not confirmed** in the available metadata.
- No submission, commit or push was performed. Raw-data reconstruction was not claimed to have been rerun.

Detailed machine-readable evidence: `submission_audit_results.json`, `submission_audit_execution.json`, `submission_audit_combined.json`, and `submission_audit_supporting.json` in this directory.

## Final documentation consistency fixes

- Replaced the README's obsolete missing-DFBETAS and historical-appendix instructions with links to the actual reviewed report and supported export/verification commands. Preserved the prior README in `docs/archive/README_before_final_report_audit.md`.
- Marked earlier readiness/compliance documents as historical rather than leaving contradictory claims presented as current findings.
- Refreshed `docs/current_readiness.json` and `docs/current_execution_results.json` from the actual final verification and execution records.
- Redirected the old `complete_rubric.py export` entry point to the reviewed exporter and disabled its obsolete baseline runner to prevent accidental loss of the report corrections.
- These follow-up fixes do not change notebook calculations, model results, data, or literature-review paragraphs.

A second full audit and its additional presentation/verification fixes are documented in [submission_second_audit.md](submission_second_audit.md). Numerical model results and data remain unchanged.

The final strict Sections 2–7 pass, including added imputation sensitivity and training-only selection validation, is documented in [requirements_2_to_7_verified.md](requirements_2_to_7_verified.md). Section 1 was excluded and preserved byte-for-byte.
