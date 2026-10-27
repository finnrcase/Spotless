# Rubric completion: changes, evidence and remaining packaging

The user requested changes to close all audit gaps after commit `96d4bb1`. All previous notebook cells and outputs are preserved verbatim after a clearly marked historical appendix in each main notebook. The current analysis is presented first. Raw and processed inputs are unchanged. This task makes no changes to `main`; work remains on `refactor/430-rubric-alignment`. During validation an external pull advanced local `main` to `7c491e9`, the merge of PR #2. That external update is preserved.

## Completed analytical changes

- Added theory-based signs and magnitude scales, including an explicitly illustrative elasticity-to-percentage-point translation grounded in Pierce and Shoup (2013). It is not a fabricated ex ante prior or fitted constraint.
- Extended density/Q-Q panels to every numeric analysis candidate, with discrete/count/KDE qualifications.
- Executed actual Profiling for the full candidate data in a compatible isolated Python 3.12 environment. The former missing-dependency blocker is resolved for the main workflow.
- Added current Model 3 containing **all conventional p<0.05 slopes from the original full 12-candidate OLS regression**, using one declared screen on the unchanged 4,016-space sample. No repeated significance deletion or hold-out tuning. The former seven-predictor model remains a supporting comparison and is reproduced numerically.
- Cancelled the DFBETAS addition at the user’s request: its calculation, outputs and price-influence plot are removed. Cook/leverage/studentized-residual analysis remains. DFBETAS is still explicitly required by the professor’s PDF and is marked Missing; 4(d) is Partial.
- Refit every current coefficient, conventional/HC1 uncertainty, VIF, Cp comparison, five-fold score, 1,000 bootstrap draws and all existing feasible sensitivities for the current model. New normality/variance/RESET conclusions use actual new outputs, not old model text.
- Added generated economic interpretations for every current coefficient and intercept, direct academic-literature comparison, a consolidated bibliography, and a single HTML report containing source code and an explicitly unexecuted original-cleaning-source appendix.
- Bounded dependencies compatibly with Profiling and recorded a tested project dependency closure in `requirements-lock.txt`. Global Python was not changed.

## Why some numbers changed

The change from prior seven predictors to the explicitly required significance-based candidate set is deliberate and authorized by the latest task. It replaces time limit and drive-alone share with walking share and all-business count. **These are specification changes, not unexplained data drift.** The sample, outcome, original sources and original historical results are unchanged.

| Quantity | Prior seven (preserved) | Current rubric Model 3 |
|---|---:|---:|
| N | 4,016 | 4,016 |
| Slopes | 7 | 7 |
| Price, occupancy fraction per dollar | 0.055633 | 0.051543 |
| Adjusted R² | 0.272354 | 0.292905 |
| AIC | −3070.712410 | -3185.769994 |
| Mean five-fold RMSE | 0.165315 | 0.162796 |
| JB normality decision at 5% | Do not reject (p≈0.1469) | Reject (p≈0.01764) |

The current price estimate is **5.154 occupancy pp per $1**, HC1 95% interval **[4.713, 5.595] pp**. It remains an association, not a causal tariff response. No DFBETAS result is retained or claimed.

## Execution and preservation

All four current computational notebooks pass fresh separate kernels: EDA (12 code cells), selection/models (17), diagnostics (8), results (6): **43 current code cells, zero cell errors**. Theory/limitations are substantive narrative sections. Runtime versions and timings are in [the current execution record](current_execution_results.json). New tables are generated in `reports/tables/`; old validation logs remain historical evidence.

The [completion manifest](rubric_completion_manifest.json) records every earlier notebook-cell hash and all three input CSV hashes. The [current verifier](../src/verify_current_report.py) checks archival equality, dataset equality, fresh execution counts, Model 3/diagnostic consistency, bootstrap count, absence of the cancelled DFBETAS implementation/results, actual CV consistency, reproduced prior-model metrics, report image embedding and source syntax. The original 263-cell provenance is still available in [the updated migration map](notebook_cell_migration.json).

Raw reconstruction is **not** newly tested: `data/raw/` is absent. Original cleaning source/outputs and acquisition provenance remain preserved. This distinction is separate from the successful current analysis replay from tracked processed CSVs.

## Final packaging — explicitly deferred by the user

1. Add all verified group-member names to `reports/submission_metadata.json` under `group_members`.
2. Review the syllabus Assignment Policies and then set `syllabus_policies_reviewed` truthfully.
3. Run `python src/complete_rubric.py export` and `python src/verify_current_report.py` in the compatible environment. This refreshes the report without rerunning statistical analysis.
4. Open the single HTML, check names, references, figure/table readability and source inclusion; submit it through the course’s required channel. No upload is performed here.

The report remains clearly marked draft while names are missing. Other analytical gaps have executed evidence, but **DFBETAS remains a required missing component by user request**, so 4(d) is Partial. A 100% grade or completed submission is not claimed. The professor retains judgment about economic reasoning, presentation and course policies.
