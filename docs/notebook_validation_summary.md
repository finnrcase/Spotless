> **Current execution update:** current code, including Profiling, passes fresh kernels. The user cancelled DFBETAS, so that required diagnostic remains Missing and 4(d) is Partial. Current results intentionally use a new significance-based Model 3; see [changes](rubric_completion_changes.md), [execution](current_execution_results.json), and [verification](current_readiness.json). The summary below is the preserved pre-completion migration record. Raw reconstruction remains unverified.

# Notebook migration validation

Baseline commit: `1a6ef43cc32cd4e51d72e928ca2d9edfcfbcbc30` (`Kerem_Vis`). Migration branch: `refactor/430-rubric-alignment`. The recorded `main` reference is `e480f468a9366603f908f4a7c72ab6c4b5999925` and remains unchanged. Validation was performed October 27, 2026.

## Preservation and structure — passed

- All **263 original cells** are accounted for at **268 destinations**, including five intentional copies for independent setup, coefficient/intercept interpretation, policy context and the sensor-processing plan. The [cell migration audit](notebook_restructure_audit.md) enumerates every destination; [JSON provenance](notebook_cell_migration.json) records hashes and zero-based indices.
- Every original saved output, including all **11 PNG figure outputs**, HTML regression/descriptive tables, stream output and numerical results, is retained exactly. Original cell metadata, execution counts and existing IDs are preserved. Missing analysis IDs receive deterministic IDs. Notebook-level original metadata is retained in the [baseline inventory](notebook_baseline_inventory.json).
- Six main notebooks have ordered rubric headings, roadmaps, requirements/method/evidence/interpretation/status notes, dependencies and end summaries. Their notebook schemas validate. The three cleaning notebooks retain the inherited 4.4 declaration with some 4.5-style IDs; their copies validate under 4.5. This known baseline format inconsistency was not silently repaired.
- Cleaning cell order is unchanged. Only `../data/` → `../../data/` and `../docs/` → `../../docs/` substitutions were applied, so relative targets remain the same. Historical paths printed in saved output remain historical output rather than being edited.
- Existing processed data, supporting documentation, acquisition scripts and `Visualization/` artifacts compare unchanged against the baseline, allowing Git’s normal CRLF conversion. No raw or processed file was written, and no data-construction/export cell was executed.
- Reordered log-density sensitivity executes after its HC1 reference fit; a bridge copies the existing `selected_variables` list to `predictors` for the moved selection-summary table. The moved results EDA uses identifier prefixes to avoid overwriting the original EDA sample. These are execution-dependency corrections, with no changed econometric methods, predictors, sample rules or seeds.

## Sample targets — passed against unchanged processed files

| Quantity | Original target | Current verification | Scope |
|---|---:|---:|---|
| Cleaned occupancy | 4,185 | 4,185 | Read existing CSV; raw aggregation not rerun |
| Cleaned inventory | 35,015 | 35,015 | Read existing CSV; raw cleaning not rerun |
| Original cross-section | 4,139 | 4,139 | Unique SpaceIDs; 36 columns retained |
| FLAT + TOD EDA | 4,060 | 4,060 | Original filter reapplied; 79 JUMP spaces excluded |
| Common regression sample | 4,016 | 4,016 | Original complete-case definitions reapplied |
| Common-sample tracts | 45 | 45 | Original GEOID linkage retained |

These are comparison targets and assertions, not hard-coded data-generation results.

## Fresh-kernel execution and numerical comparison

The [machine-readable execution report](notebook_validation_results.json) is the authoritative run log. Each main notebook starts in a separate Python kernel with working directory `notebooks/`. Execution copies are written under ignored `.validation/`; published notebooks retain their original saved outputs. Narrative-only notebooks 01 and 06 receive schema/navigation checks rather than a fictitious code-execution claim.

Main notebooks 03 (selection/models), 04 (diagnostics/robustness) and 05 (results/interpretation) execute without cell errors. Main notebook 03 freshly reproduces Boruta with the isolated pinned package, all 4,095 Cp subsets, VIF, regressions and five-fold comparison. Main notebook 02 executes all EDA, descriptive, density/Q-Q and missingness code except the blocked Profiling cell. Earlier missing-package and ordering failures were investigated; dependency/order corrections are documented above rather than accepted as numerical changes.

Every successful migrated code cell with an original saved output is compared at its saved display precision. This includes visible numerical cells in HTML Styler tables, not merely their memory-address representations. Tolerance is `rtol=1e-5`, `atol=5e-6`; timestamps, progress text and memory addresses are excluded. Figure pixel identity is not required across rendering environments; the **original** figure payloads are separately checked for exact preservation. Matching printed figures/tables cannot establish equality at precision not saved in the original outputs.

| Result family | Original baseline retained for comparison |
|---|---|
| Candidate definitions and sample | Original 12 encoded candidates, seven preferred predictors, unchanged 4,016 rows |
| Boruta | 10 confirmed; income and meter type rejected; original seed 10 and RF/Boruta settings |
| Mallows Cp | Exhaustive 4,095 nonempty subsets; best-ten Cp 9.949599; best-eight 11.789 |
| VIF | Full/reduced tables retained; selected slope VIFs below 2 |
| Models 1/2/3 | 1/3/7 predictors; price estimates approximately 0.054515 / 0.059991 / 0.055633 |
| Adjusted R² | 0.15657 / 0.24293 / 0.27235 |
| AIC | −2483.67051 / −2915.51726 / −3070.71241 |
| BIC | −2471.07443 / −2890.32509 / −3020.32808 |
| Five-fold mean RMSE | 0.17756 / 0.16821 / 0.16532; seed 10; actual training-fold fits retained |
| Coefficients and uncertainty | All conventional and HC1 coefficients, standard errors, p-values and CIs retained; price HC1 SE approximately 0.002322 and CI [0.051081, 0.060184] |
| Diagnostics | BP p ≈ 3.37e−41; White p ≈ 4.75e−63; RESET F ≈ 122.078, p ≈ 5.60e−28; JB p ≈ 0.1469 |
| Influence | 249 Cook, 136 leverage and 189 residual flags; Cook sensitivity N=3,767; four fitted occupancies exceed one |
| Bootstrap | 1,000 draws, seed 90095; price mean ≈ 0.05548, SE ≈ 0.002374, percentile CI [0.05091, 0.06011]; all coefficients compared |
| Existing sensitivities | Log density price ≈ 0.05516; ≥28 days N=1,609 and price ≈ 0.04963; restored income-missing N=4,060 and price ≈ 0.05716 |
| Figures/tables | All original payloads retained; executable generating code preserved; fresh renderings remain temporary |

The final run records **75 successful output comparisons with zero numerical mismatches**. The JSON report identifies each compared source/destination cell. No statistical output is changed to make a narrative or rubric status look better. A favorable normality test does not override heteroskedasticity, RESET rejection, dependence or endogeneity concerns.

## Unvalidated or blocked work

**Raw reconstruction:** `data/raw/` is absent in this checkout. Occupancy rebuilding needs `data/raw/ladot_occupancy/20261017T052111914317Z/Sensor Transactions_2025_08.csv`; inventory cleaning needs `data/raw/ladot_meters/20261017T052111914317Z/inventory.csv`. Cross-section rebuilding additionally needs the original ACS JSON, Gazetteer text file, TIGER/Line shapefile and companion files, business registry CSV, original zoning listing/pages and the two documented supplemental zoning pages. GeoPandas/Shapely are not installed in the available validation environment. The cleaned CSVs can be checked but do not establish a fresh end-to-end reconstruction.

All new local notebook/audit/navigation links resolve. One inherited README link points to the absent raw TIGER/Line shapefile; it remains as a documented source dependency rather than being removed or redirected to a different vintage.

**Profiling:** Original `ProfileReport(..., minimal=True, progress_bar=False)` code and its successful summary/alerts remain. The available qecon Python 3.12 environment lacks Profiling’s transitive dependencies, including dacite, pydantic, visions, phik and numba; its NumPy 2.4.1 and matplotlib 3.10.8 also exceed the pinned profiling package’s stated upper constraints. The two already-declared course packages were downloaded into ignored `.validation/packages` without changing the global environment or `requirements.txt`. Boruta is usable with access to that isolated directory; importing a usable `ProfileReport` remains blocked. The sandbox additionally cannot read newly elevated package directories; this is recorded as an environment restriction, not an analysis result.

**Inherited missing analyses/deliverables:** DFBETAS has no original implementation; raw interval/day/Sunday extensions remain plans; Model 3’s significance discrepancy, expected-magnitude discussion, remaining continuous-variable panels, developed literature comparison and final group packaging remain as listed in the [rubric audit](rubric_compliance_audit.md). No syllabus policy review or actual submission is claimed.

## Repeating validation

From the repository root with a suitable Python environment:

```bash
python src/audit_restructured_notebooks.py
python src/audit_restructured_notebooks.py --execute
```

The first command verifies preservation, unchanged baseline files/main, ordered headings, cleaning paths, schema and sample counts. The second runs the main workflow in separate kernels; it can record missing dependencies as explicit cell errors. `--execute --only 03` reruns just the selection/model notebook while retaining other run records. Install the existing project requirements in an isolated compatible environment for a full replay; raw reconstruction additionally needs the original inputs in a separate workspace to avoid overwriting fixed processed files.

`src/restructure_notebooks.py` regenerates the migration deterministically from the recorded Git baseline; it does not run statistical analysis. Its provenance records and assertions make each original cell reviewable. Regenerating notebooks does not itself rerun or refresh numerical results.

**Outcome:** lossless migration and structural validation passed. Numerical preservation passed; fresh numerical checks are separately recorded per cell. Full end-to-end reproducibility is **not** claimed.
