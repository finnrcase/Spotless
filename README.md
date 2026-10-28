# Spotless: ECON 430 Parking Occupancy Project

A cross-sectional analysis of August 2025 occupancy at Los Angeles sensor-equipped metered parking spaces.

## Report files

- [Combined report notebook](notebooks/Spotless_complete.ipynb)
- [HTML report with embedded figures and Python source](reports/Spotless_ECON430_Project1.html)
- [Analysis Python source](reports/Spotless_ECON430_source.py)
- [Data-construction Python source](reports/Spotless_cleaning_source.py)

The six report notebooks contain the same final analysis in separate sections:

| Section | Notebook |
|---|---|
| Economic theory and hypothesis | [01](notebooks/01_economic_theory.ipynb) |
| Data description and exploratory analysis | [02](notebooks/02_data_description_eda.ipynb) |
| Variable selection and model development | [03](notebooks/03_variable_selection_models.ipynb) |
| Diagnostics and robustness | [04](notebooks/04_diagnostics_robustness.ipynb) |
| Results and economic interpretation | [05](notebooks/05_results_interpretation.ipynb) |
| Limitations, policy implications and extensions | [06](notebooks/06_limitations_extensions.ipynb) |

The report uses 4,016 complete-case spaces in 45 Census tracts and evaluates 12 candidate predictors. Model 3 includes every slope meeting the declared conventional 5% significance screen in the full candidate model. Sections 3–5 use the same predictor definition. DFBETAS, 1,000 bootstrap replications and actual five-fold held-out predictions are included.

The final price association is about 5.15 occupancy percentage points per dollar. This is a conditional association, not a causal price effect. Diagnostics identify heteroskedasticity, functional-form concerns and residual nonnormality; spatial dependence, source timing and model selection also qualify inference.

## Reproduce the analysis

Use Python 3.12 and install the compatible dependencies:

```bash
python -m pip install -r requirements-lock.txt
```

Open the combined notebook from `notebooks/` and run its cells in order. Alternatively, run each report notebook with its own fresh kernel from that folder. The narrative-only sections contain no calculations. The analysis uses the tracked processed CSVs and does not modify them.

To rerun every section in an independent fresh kernel and verify the combined notebook:

```bash
python src/run_report_notebooks.py --include-combined
```

To regenerate the HTML and source files from saved notebook outputs, then verify them:

```bash
python src/build_submission_report.py
python src/verify_current_report.py
```

The original raw inputs are required only to reconstruct the data using `notebooks/cleaning/`; they are absent from this checkout. Those notebooks retain their construction methods and saved outputs. Supplementary notebooks in `Visualization/` explore the full matched sample rather than the report's restricted sample.

## Submission details

The assignment accepts one PDF or HTML report per group. Add the verified group-member names to `reports/submission_metadata.json`, complete the syllabus Assignment Policies review, and regenerate the HTML. The literature-review paragraphs remain unchanged for the authors' final review. Nothing has been submitted or pushed.

## Verification and provenance

- [Verified Sections 2–7 requirements](docs/requirements_2_to_7_verified.md)
- [Second full audit](docs/submission_second_audit.md)
- [Final audit and full change log](docs/submission_audit_changes.md)
- [Current verification results](docs/submission_audit_results.json)
- [Independent clean-kernel execution](docs/submission_audit_execution.json)
- [Combined notebook execution](docs/submission_audit_combined.json)
- [Data sources and acquisition details](docs/data_sources.md)
- [Cleaning decisions](docs/cleaning_decisions.md)
- [Earlier README and historical workflow](docs/archive/README_before_final_report_audit.md)

Earlier audit documents describe prior versions. The final audit above supersedes their completion labels and old model results.
