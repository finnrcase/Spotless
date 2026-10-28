"""Build the current rubric-complete analysis while preserving prior notebook cells.

The prior analysis is retained verbatim after the current section in each main
notebook. Only current cells run; the historical appendix is never re-executed.
Run with Python 3.12 and the project requirements, from the repository root.
"""
import argparse
import copy
import hashlib
import html
import importlib.metadata
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
BASE = '96d4bb1b5983b92644b56466e9500051e0846de6'
NAMES = ['01_economic_theory', '02_data_description_eda', '03_variable_selection_models',
         '04_diagnostics_robustness', '05_results_interpretation', '06_limitations_extensions']
TITLES = ['Economic Theory and Hypothesis', 'Data Description and Exploratory Analysis',
          'Variable Selection and Model Development', 'Final Model Diagnostics and Robustness',
          'Results and Economic Interpretation', 'Limitations, Policy Implications, and Extensions']
POINTS = [15,25,25,20,25,10]
SHOUP = 'https://escholarship.org/content/qt55s7079f/qt55s7079f.pdf'
PIERCE = 'https://www.its.ucla.edu/wp-content/uploads/sites/10/2017/06/Getting-the-Prices-Right-An-Evaluation-of-Pricing-Parking-by-Demand-in-San-Francisco.pdf'

def saved(path):
    return subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT)

def h(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def currency(text):
    """Keep currency from being mistaken for paired inline MathJax delimiters."""
    return re.sub(r'(?<!\\)\$(?=\d)',lambda match:r'\$',text)

SETUP = '''from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from IPython.display import display, Markdown

%matplotlib inline

root = Path.cwd().parent
parking_full = pd.read_csv(root / "data/processed/parking_cross_section.csv",
                          dtype={"SpaceID": str, "GEOID": str})
parking = parking_full.loc[parking_full["RateType"].isin(["FLAT", "TOD"])].copy()
dependent_variable = "occupancy_rate"
candidate_variables = [
    "price_midpoint", "time_limit_hours", "population_density", "median_income",
    "nearby_restaurant_retail_count", "drive_alone_share", "RateType", "MeterType",
    "housing_density", "transit_share", "walk_share", "nearby_business_count"
]
encoded = pd.get_dummies(parking[candidate_variables], drop_first=True, dtype=int)
data = pd.concat([parking[["occupancy_rate"]], encoded], axis=1).dropna().copy()
y = data["occupancy_rate"]
X = data.drop(columns="occupancy_rate")
assert parking_full["SpaceID"].is_unique
assert parking.loc[data.index, "SpaceID"].is_unique
print("Original / FLAT+TOD / common:", len(parking_full), len(parking), len(data))
print("Candidates / common-sample tracts:", X.shape[1], parking.loc[data.index, "GEOID"].nunique())
'''

MODELS = '''# Fixed rule: retain EVERY slope with conventional p < 0.05 in the
# original 12-candidate full OLS model, on the same complete-case sample.
# This is one screen, not repeated p-value deletion or hold-out tuning.
full_model = sm.OLS(y, sm.add_constant(X)).fit()
alpha = 0.05
predictors = [v for v in X.columns if full_model.pvalues[v] < alpha]
legacy_predictors = ["price_midpoint", "time_limit_hours", "population_density",
                     "nearby_restaurant_retail_count", "drive_alone_share",
                     "transit_share", "RateType_TOD"]
X1 = sm.add_constant(data[["price_midpoint"]])
X2 = sm.add_constant(data[["price_midpoint", "population_density", "nearby_restaurant_retail_count"]])
X3 = sm.add_constant(data[predictors])
model1 = sm.OLS(y, X1).fit()
model2 = sm.OLS(y, X2).fit()
model3 = sm.OLS(y, X3).fit()
hc1 = sm.OLS(y, X3).fit(cov_type="HC1")
legacy_model = sm.OLS(y, sm.add_constant(data[legacy_predictors])).fit()
assert set(predictors) == set(full_model.pvalues.drop("const").loc[lambda p: p < alpha].index)
'''

CV = '''from sklearn.model_selection import KFold, cross_val_score
from sklearn.linear_model import LinearRegression
folds = KFold(n_splits=5, shuffle=True, random_state=10)
fits = {"Model 1": model1, "Model 2": model2, "Model 3 (rubric)": model3,
        "Prior seven (supporting)": legacy_model}
fold_errors = {}
for label, fit in fits.items():
    columns = [v for v in fit.model.exog_names if v != "const"]
    fold_errors[label] = -cross_val_score(LinearRegression(), data[columns], y,
                                        cv=folds, scoring="neg_root_mean_squared_error")
cv_results = pd.DataFrame(fold_errors, index=pd.Index(range(1, 6), name="Held-out fold"))
comparison = pd.DataFrame({
    label: {"Slopes": len(fit.params)-1, "N": int(fit.nobs), "R2": fit.rsquared,
            "Adjusted R2": fit.rsquared_adj, "AIC": fit.aic, "BIC": fit.bic,
            "In-sample RMSE": np.sqrt(np.mean(fit.resid**2)),
            "Mean 5-fold RMSE": fold_errors[label].mean(),
            "SD across folds": fold_errors[label].std(ddof=1)}
    for label, fit in fits.items()
}).T
display(cv_results.round(6))
display(comparison.round(6))
'''

THEORY = f'''Shoup (2006) models the choice between searching for a cheaper curb space and paying for immediately available off-street parking. The relative monetary and time costs explain why scarce curb space can produce cruising. This motivates occupancy as an economically relevant outcome and a downward demand response to price, holding other demand conditions constant. We do not measure cruising directly. [Shoup, *Transport Policy* 13(6), 479–486]({SHOUP}).

Pierce and Shoup (2013) study SFpark price/occupancy adjustments and report average price elasticity about −0.4, with substantial heterogeneity. Their setting illustrates why tariff changes and location differences answer different questions: administrators can set higher tariffs where demand is stronger. [Pierce and Shoup, *JAPA* 79(1), 67–81, doi:10.1080/01944363.2013.787307]({PIERCE}).

In our cross-section, nearby activity and residential density can shift parking demand, while walking/transit alternatives and local parking supply can offset it. Resident commuting shares are contextual proxies, not the modes of the actual parkers. Therefore price endogeneity, destination sorting and omitted supply prevent interpreting an OLS coefficient as a structural demand response. We estimate conditional associations, and compare them with the demand hypothesis without claiming causal identification.'''

EXPECTED = f'''The demand hypothesis predicts a negative **causal** price response conditional on demand; observed cross-location price associations can have either sign when prices respond to demand. A useful magnitude benchmark is elasticity ε≈−0.4 from [Pierce and Shoup (2013)]({PIERCE}). At an **illustrative** 50% occupancy and $2/hour price, a 10% price rise ($0.20) implies approximately a 4% relative occupancy decline, or **2 occupancy percentage points**. Locally, β≈εq/p≈−0.10 occupancy-fraction units per dollar. This is a transportability benchmark, not an imposed coefficient, a preregistered prior, or a causal estimate for Los Angeles. Large $1 changes need not follow the local approximation.

The other slopes have no calibrated structural magnitudes in these two sources. Discussing size therefore requires units, scale and the occupancy bound rather than invented numerical priors:

| Candidate | Demand-based sign expectation / qualification | Magnitude scale |
|---|---|---|
| Price midpoint | Negative holding demand fixed; cross-location sign can reverse | $0.20 and $1 changes; benchmark above; not an elasticity coefficient |
| Time limit | Longer stays can raise occupancy; turnover response makes sign ambiguous | 1 additional hour implies 100β percentage points |
| Population/housing density | Positive demand pressure, offset by local supply/mode choice | 1,000 people or housing units per square mile implies 100,000β pp |
| Median income | Ambiguous: car demand versus price/time sensitivity | $10,000 implies 1,000,000β pp; no calibrated prior |
| Food-service/retail and all-business counts | Positive demand pressure in isolation; conditional composition effects can reverse signs | 100 registrations implies 10,000β pp; not 100 distinct new storefronts |
| Drive-alone / transit / walk shares | Ambiguous resident demand, substitution and centrality mechanisms | A 10-pp share change implies 10β occupancy pp; shares are fractions |
| TOD / meter technology indicators | Ambiguous assignment and location differences | Indicator switch implies 100β pp relative to reference |

Effects are local comparisons within observed support, not unlimited linear extrapolations. Occupancy is between zero and one: a 5-pp change is meaningful against 50% occupancy, but is a 10% **relative** change, not 5%. Boundedness, saturation and overlapping covariates limit plausible effect sizes. These expectations are stated explicitly for interpretation; estimates below are not modified to match them.'''

METHODS = {
 '1a':'Define the space-level economic question and scope',
 '1b':'Review the two cited academic studies in three theory paragraphs',
 '1c':'State the conditional price-sign hypothesis and inference interpretation',
 '1d':'Translate a literature elasticity into an illustrative magnitude and discuss every candidate’s scale',
 '2a':'Document sources, vintages, variable units and the unchanged sample flow',
 '2b':'Compute all seven required descriptive statistics with explicit denominators',
 '2c':'Plot key distributions/relationships and the candidate correlation matrix',
 '2d':'Plot density and normal Q-Q panels for every numeric candidate',
 '2e':'Discuss skewness, functional form and the linked log-density check',
 '2f':'Screen IQR extremes and link coefficient/residual influence diagnostics',
 '2g':'Tabulate missingness/tract patterns, justify no imputation and link the restored-income sample',
 '2h':'Execute minimal Profiling on the outcome and all encoded candidates, then discuss alerts',
 '3a':'Fit the original seeded Boruta/random-forest specification',
 '3b':'Calculate Cp for every nonempty candidate subset and compare the current model',
 '3c':'Calculate full/reduced/current VIF and explain overlapping predictors',
 '3d':'Fit the required one-, three- and full-candidate-significant specifications with a declared rule',
 '3e':'Compute AIC/BIC/adjusted R² and identical five-fold held-out errors',
 '3f':'Combine the economic rationale, significance rule and displayed comparison criteria',
 '4a':'Plot residuals/fitted values and execute squared-fitted RESET',
 '4b':'Execute BP/White, plot scale-location and compare conventional/HC1 uncertainty',
 '4c':'Plot residual Q-Q/histogram and execute Jarque–Bera for the current model',
 '4d':'Compute Cook, leverage and studentized residuals with source IDs; leave DFBETAS unimplemented as requested',
 '4e':'Fit 1,000 seeded row-bootstrap regressions and compare all parameters with OLS',
 '4f':'Refit the actual five training/held-out folds and report RMSE',
 '4g':'Interpret current tests and refit existing feasible specification/sample sensitivities',
 '5a':'Present every coefficient with conventional and HC1 uncertainty, N and fit',
 '5b':'Rescale every slope to economic units and explain the intercept',
 '5c':'Compare computed p-values with economically scaled magnitudes',
 '5d':'Calculate all HC1 intervals and explain coverage and inference limitations',
 '5e':'Interpret fit/error, compare findings with both studies and state the conclusion',
 '6a':'Review data, model and scope limitations without deleting inherited caveats',
 '6b':'Explain endogeneity, omission, measurement and selection mechanisms',
 '6c':'State cautious policy implications consistent with associational evidence',
 '6d':'Specify concrete sensor, vintage, identification and validation extensions',
 '6e':'Define the population/time context and unsupported transfers'
}

def section_note(key):
    status=('Partial — DFBETAS remains required but its addition was cancelled by the user.'
            if key=='4d' else 'Complete for analytical coverage; execution evidence is recorded separately, and no grade is guaranteed.')
    return (f'\n\n**Method:** {METHODS[key]}. '
            '**Evidence:** current code/outputs or cited substantive discussion immediately below. '
            '**Interpretation:** accompanies the evidence, including units and limitations. '
            f'**Status:** {status}')

def normalize_cleaning(mapping):
    """Repair only the inherited notebook schema/absent IDs, not calculations."""
    changes={}
    for path in sorted((ROOT/'notebooks/cleaning').glob('*.ipynb')):
        raw=json.loads(path.read_text(encoding='utf-8'))
        baseline=json.loads(saved(path.relative_to(ROOT).as_posix()))
        additions=[]
        for index,cell in enumerate(raw['cells']):
            if not cell.get('id'):
                cell['id']='clean-'+h((path.name,index))[:18]
            if not baseline['cells'][index].get('id'):additions.append(index)
            for m in mapping:
                if m['destination']==path.relative_to(ROOT).as_posix() and m['destination_index']==index:
                    m['destination_id']=cell['id'];m['destination_sha256']=h(cell)
                    if index in additions and 'stable missing cell ID' not in m['change']:
                        m['change']+='; assigned stable missing cell ID for schema 4.5'
        raw['nbformat_minor']=5
        path.write_text(json.dumps(raw,indent=1,ensure_ascii=False)+'\n',encoding='utf-8')
        changes[path.name]={'original_minor':baseline['nbformat_minor'],'current_minor':5,
                            'assigned_missing_ids_at_indices':additions,
                            'source_outputs_metadata_unchanged':True}
    return changes

def build():
    import nbformat as nbf
    for name in NAMES:
        polished=ROOT/f'notebooks/{name}.ipynb'
        if polished.exists() and json.loads(polished.read_text(encoding='utf-8'))['metadata'].get('spotless_history_path'):
            raise SystemExit(f'{name} has a submission edit. Use run/export; baseline build would overwrite that edit.')
    books = {}
    def md(i,text):
        text=currency(text)
        books[i].cells.append(nbf.v4.new_markdown_cell(text,id='credit-'+h((i,text))[:18]))
    def code(i,text):
        books[i].cells.append(nbf.v4.new_code_cell(text,id='credit-'+h((i,text))[:18]))
    def section(i,letter,title,requirement):
        md(i,f'<a id="current-{i}{letter}"></a>\n\n## {i}({letter}) {title}\n\n**Requirement:** {requirement}'+section_note(f'{i}{letter}'))
    for i,name in enumerate(NAMES,1):
        nb = json.loads(saved(f'notebooks/{name}.ipynb'))
        books[i] = nbf.v4.new_notebook(metadata=copy.deepcopy(nb['metadata']))
        letters={1:'abcd',2:'abcdefgh',3:'abcdef',4:'abcdefg',5:'abcde',6:'abcde'}[i]
        toc=' · '.join(f'[{i}({x})](#current-{i}{x})' for x in letters)
        md(i,f'# Section {i} — {TITLES[i-1]}\n\n**ECON 430 Project 1 · {POINTS[i-1]} points**\n\n'
           f'{toc}\n\nThis is the current submission analysis. Requirements follow the [professor’s PDF](../project1-1%20%281%29.pdf). '
           'Section 4 letters organize its unlettered diagnostic bullets. '
           'The prior analysis is preserved verbatim in the historical appendix at the end; its old results/statuses do not describe the current model. '
           'Current Model 3 uses the explicit full-candidate significance rule in Section 3(d); the former seven-predictor model remains supporting evidence.\n\n'
           '**Execution:** fresh Python kernel, working directory `notebooks/`; install the compatible project requirements. '
           'Input is the unchanged [4,139-space processed CSV](../data/processed/parking_cross_section.csv), built by '
           '[cleaning/03](cleaning/03_build_cross_section.ipynb). Main 01/06 are narrative; 02–05 reload their own inputs. '
           '[01](01_economic_theory.ipynb) · [02](02_data_description_eda.ipynb) · [03](03_variable_selection_models.ipynb) · '
           '[04](04_diagnostics_robustness.ipynb) · [05](05_results_interpretation.ipynb) · [06](06_limitations_extensions.ipynb).')

    section(1,'a','Economic Research Question','State a clear economic research question.')
    md(1,'How do stated parking prices, parking rules and neighborhood characteristics relate to differences in August 2025 monthly occupancy across Los Angeles sensor-equipped metered spaces? One observation is one parking space; this is an associational cross-sectional study, not a price experiment or real-time availability model.')
    section(1,'b','Relevant Economic Theory and Academic Literature','Review theory in 2–3 paragraphs and cite at least two academic sources.')
    md(1,THEORY)
    section(1,'c','Specific, Testable Economic Hypothesis','State a specific testable relationship.')
    md(1,'The economic demand prediction is β_price < 0 holding other demand determinants fixed. For the observed linear conditional association we inspect the estimated slope, its conventional/HC1 95% interval and sign relative to zero; the reported intervals use two-sided inference. A positive estimate contradicts the negative *association* prediction, but cannot reject the law of demand because the regressions do not identify an exogenous price response. Density and business activity are contextual demand hypotheses; commuting-share and tariff-structure signs are ambiguous.')
    section(1,'d','Expected Coefficient Signs and Magnitudes','Discuss both expected signs and magnitudes in economic units.')
    md(1,EXPECTED)

    section(2,'a','Dataset Source, Time Period, Sample Selection, and Variable Definitions','Describe data sources, periods, sampling and variables.')
    md(2,'LADOT August 2025 transactions are aggregated to occupied/valid minutes under the inherited ≤24-hour gap and ≥25 raw-active-day rules: 4,185 spaces. Inventory matching excludes 46, leaving 4,139. FLAT/TOD restriction excludes 79 JUMP spaces whose midpoint mixes durations, leaving 4,060; the common complete-case analysis has 4,016 after 44 missing incomes. No zoning-missingness filter is used. Prices/business registrations are October 2026 proxies; ACS is the 2024 five-year release (2020–2024), with 2024 geography/land area.\n\n[Detailed variable definitions and assumptions](../README.md) and [source URLs/vintages](../docs/data_sources.md) are retained. Cleaning notebooks document persistence, UNKNOWN exclusions, active-day definitions and mixed zoning recovery. Spaces are not a random sample of all Los Angeles parking.')
    code(2,SETUP)
    code(2,'''definitions = pd.DataFrame([
 ["occupancy_rate", "Occupied valid minutes / all retained valid minutes", "fraction 0–1"],
 ["price_midpoint", "FLAT hourly amount / TOD hourly-endpoint midpoint", "dollars/hour proxy"],
 ["time_limit_hours", "Mapped source parking-duration label", "hours"],
 ["population_density / housing_density", "ACS count / Gazetteer land area", "people / units per sq mile"],
 ["median_income", "ACS median household income", "2024 dollars"],
 ["drive_alone_share / transit_share / walk_share", "Mode workers / total workers incl. home workers", "fractions"],
 ["nearby_restaurant_retail_count", "NAICS 722, 44–45 located registrations within 0.25 miles", "registry accounts"],
 ["nearby_business_count", "All located registrations within 0.25 miles", "registry accounts"],
 ["RateType_TOD", "TOD=1, FLAT=0", "indicator"],
 ["MeterType_Single-Space", "Single-space=1, multi-space=0", "indicator"]
], columns=["Variable", "Definition", "Units"])
display(definitions)
display(parking.groupby("RateType").size().rename("Spaces"))
''')
    section(2,'b','Comprehensive Descriptive Statistics','Mean, median, standard deviation, min, max, skewness and kurtosis.')
    code(2,'''numeric_variables = [v for v in candidate_variables if v not in ["RateType", "MeterType"]]
numeric_variables = ["occupancy_rate", *numeric_variables]
descriptive = parking[numeric_variables].describe().T[["count","mean","50%","std","min","max"]].rename(columns={"50%":"median"})
descriptive["skewness"] = parking[numeric_variables].skew()
descriptive["excess kurtosis"] = parking[numeric_variables].kurt()
display(descriptive.round(4))
''')
    md(2,'All quantities retain original units. Excess kurtosis uses zero as the normal reference. Income summaries omit only its missing values; other columns use all FLAT/TOD observations. Mean/median differences and upper tails motivate distributional inspection, not automatic trimming.')
    section(2,'c','Histograms, Boxplots, Correlation Heatmap, and Scatterplots','Show all four visualization types and interpret key relationships.')
    # Reuse the exact original plotting methods; no original code/output is removed.
    oldeda=json.loads(subprocess.check_output(['git','show','1a6ef43:notebooks/04_eda.ipynb'],cwd=ROOT))
    for idx in [21,24]: code(2,''.join(oldeda['cells'][idx]['source']))
    code(2,'''correlations = parking[numeric_variables].corr()
fig, ax = plt.subplots(figsize=(12,10))
im = ax.imshow(correlations, cmap="coolwarm", vmin=-1, vmax=1)
ax.set_xticks(range(len(correlations)), correlations.columns, rotation=90)
ax.set_yticks(range(len(correlations)), correlations.index)
fig.colorbar(im, ax=ax, label="Pearson correlation")
ax.set_title("FLAT/TOD outcome and numeric candidates; available-pair correlations")
fig.tight_layout(); plt.show()
display(correlations.round(3))
''')
    md(2,'Price/density/business activity have upper tails; occupancy varies widely at the same price. Housing/population density and the two business counts overlap strongly. Positive pairwise price correlation is compatible with demand-responsive tariffs, and is not a causal price elasticity. Correlations involving income use observed pairs; the rest need not have that smaller denominator.')
    section(2,'d','Q-Q Plots and Density Plots','Assess all numeric candidate distributions, with discrete-variable qualifications.')
    code(2,'''# Include all numeric candidates, even counts and discrete time limits, so
# no analysis variable is silently omitted. Discrete panels are descriptive.
fig, axes = plt.subplots(len(numeric_variables), 2, figsize=(12,3*len(numeric_variables)))
for row, variable in enumerate(numeric_variables):
    values = parking[variable].dropna()
    values.plot.density(ax=axes[row,0])
    axes[row,0].set_title(variable + " — density (descriptive for discrete values)")
    sm.qqplot(values, line="s", ax=axes[row,1])
    axes[row,1].set_title(variable + " — normal Q-Q")
fig.tight_layout(); plt.show()
''')
    md(2,'Right-tail departures are visible for densities, income and business counts; shares are bounded and time limits are discrete. Smooth KDEs for counts/discrete limits are only visual summaries and can extend beyond feasible support. Predictors need not be Gaussian for OLS. Assess residuals separately in Section 4(c), and consider logs for positive skewed predictors rather than forcing normality.')
    section(2,'e','Nonlinearities and Potential Transformations','Discuss possible nonlinearity and transformations.')
    md(2,'Scatterplots show changing spread and repeated tract values; they do not uniquely identify a nonlinear mean. Population density is strictly positive and skewed, motivating the inherited natural-log-density sensitivity, now refitted for current Model 3 in Section 4(g). Zeros make naïve logs of all shares inappropriate. The primary level specification is retained for interpretable marginal associations; residual/RESET evidence and the log sensitivity determine how cautiously to interpret it.')
    section(2,'f','Outlier Detection and Discussion','Use IQR and model-based residual diagnostics.')
    for idx in [31,33,34]: code(2,''.join(oldeda['cells'][idx]['source']))
    md(2,'The 1.5-IQR rule screens unusual distributions, not data validity. A zero IQR for time limits flags valid non-two-hour categories; very dense tracts and co-located registry accounts deserve interpretation. Section 4(d) supplies standardized/studentized residuals, Cook and leverage. DFBETAS is not implemented, as requested. No flag permanently removes an observation or changes the saved CSV.')
    section(2,'g','Missing Values, Imputation Decisions, and Sensitivity Analysis','Document missingness, justify treatment and evaluate sensitivity.')
    code(2,'''missingness = pd.DataFrame({"Missing":parking[candidate_variables].isna().sum(),
                            "Percent":100*parking[candidate_variables].isna().mean()})
display(missingness)
display(parking.loc[parking["median_income"].isna()].groupby("GEOID").agg(Spaces=("SpaceID","size"), Mean_occupancy=("occupancy_rate","mean")))
display(parking.groupby(parking["median_income"].isna())["occupancy_rate"].agg(["count","mean","median"]))
''')
    md(2,'Income is missing for 44 spaces in two tracts, and their mean occupancy differs from complete cases. We retain them in descriptive EDA and use the same income-complete comparison sample for all selection/models. No fabricated income is imputed. Income is not a final slope, so Section 4(g) explicitly restores those 44 spaces for a sample sensitivity. Sparse zoning is excluded as a predictor rather than deleting almost every row; no unrelated missing column defines the analysis sample.')
    section(2,'h','Pandas Profiling Analysis and Findings','Execute Profiling and discuss findings.')
    code(2,'''from ydata_profiling import ProfileReport
profile_columns = ["occupancy_rate", *X.columns]
profile_data = pd.concat([parking[["occupancy_rate"]], encoded], axis=1)
profile = ProfileReport(profile_data[profile_columns], minimal=True, progress_bar=False)
profile_summary = profile.description_set
print("Profiled rows:", profile_summary.table["n"])
print("Missing cells / variables:", profile_summary.table["n_cells_missing"], profile_summary.table["n_vars_with_missing"])
display(pd.DataFrame({"Profiling alert":[str(a) for a in profile_summary.alerts]}))
''')
    md(2,'Profiling covers the outcome and all 12 encoded candidates before complete-case filtering. Income missingness is the substantive treatment issue; uniqueness and zeros in shares/indicators are not evidence of recording errors. Minimal mode is an inspection tool, not automatic cleaning or a substitute for the heatmap, IQR and regression diagnostics.')

    section(3,'a','Boruta Algorithm','Apply Boruta and document parameters.')
    code(3,SETUP)
    md(3,'Random forest max_depth=5; Boruta n_estimators="auto", random_state=10, two_step=True, verbose=2; Boruta 0.4.3 defaults otherwise. Feature importance is predictive relevance, not an OLS significance test. The original 12-candidate sample and seed are unchanged.')
    oldsel=json.loads(subprocess.check_output(['git','show','1a6ef43:notebooks/05_variable_selection.ipynb'],cwd=ROOT))
    for idx in [7,8]: code(3,''.join(oldsel['cells'][idx]['source']))
    section(3,'b','Mallows Cp Criterion','Use Cp for variable selection and explain the comparison.')
    for idx in [9,10,11,12,13]: code(3,''.join(oldsel['cells'][idx]['source']))
    md(3,'Cp uses full-candidate residual variance, with parameter count including the intercept. All 4,095 nonempty subsets are compared. The best-eight display is supporting evidence, not a claim of a global optimum. Cp minimizes a different tradeoff from the rubric’s significance-based Model 3; we report the current model’s Cp below rather than claiming it is the minimum.')
    section(3,'c','Variance Inflation Factors','Check multicollinearity and explain implications.')
    for idx in [4,5]: code(3,''.join(oldsel['cells'][idx]['source']))
    md(3,'Population/housing density and overlapping business counts inflate full-set VIF. VIF measures slope uncertainty from overlapping predictors, not bias or economic importance. Current Model 3 deliberately includes all full-candidate significant predictors, including both business counts; report their actual VIF and conditional-composition interpretation rather than hiding overlap. The former low-VIF specification remains a supporting comparison.')
    section(3,'d','Three Competing Regression Models','Model 1: one key predictor; Model 2: 2–3; Model 3: all statistically significant predictors, with rationale.')
    md(3,'**Declared significance rule:** take every non-intercept predictor with conventional two-sided p<0.05 in the original 12-candidate full OLS regression on the common sample. This is a single documented screen, not iterative deletion, a Boruta synonym, or selection tuned on held-out outcomes. Post-selection p-values/CIs are descriptive conditional inference, not selection-adjusted coverage. HC1 significance is also reported as a sensitivity to variance assumptions.\n\nThe latest request to close rubric gaps authorizes this additional Model 3. The previous seven-predictor specification and every old result remain intact in the historical appendix and are also refitted as a supporting comparator.')
    code(3,MODELS+'''selection_table = pd.DataFrame({"Full-model p":full_model.pvalues.drop("const"),
                                  "Included in rubric Model 3":[v in predictors for v in X.columns]})
display(selection_table)
print("Current Model 3 predictors:", predictors)
''')
    for label,fit,reason in [('Model 1 — Simple Regression with the Theoretically Most Important Predictor','model1','Price is the main economic demand question.'),('Model 2 — Multiple Regression with 2–3 Key Predictors','model2','Price, density and food-service/retail activity capture local demand with three slopes.'),('Model 3 — Multiple Regression with All Statistically Significant Predictors','model3','Includes every full-candidate slope meeting the declared 5% rule; broader demand and activity composition are represented.')]:
        md(3,'### '+label+'\n\n'+reason)
        code(3,f'print({fit}.summary())')
    code(3,'''from statsmodels.stats.outliers_influence import variance_inflation_factor
current_vif = pd.DataFrame({"Variable":X3.columns,
 "VIF":[variance_inflation_factor(X3.values,i) for i in range(X3.shape[1])]})
display(current_vif)
current_cp = np.sum(model3.resid**2)/full_model.mse_resid - (len(y)-2*len(model3.params))
print("Current Model 3 Cp:",current_cp, "; minimum searched Cp:",cp_results["Cp"].min())
''')
    section(3,'e','AIC, BIC, Adjusted R², and Cross-Validation Comparison','Compare all requested fit/prediction criteria on identical observations.')
    code(3,CV+'''cv_results.plot(marker="o",figsize=(10,5))
plt.ylabel("Held-out RMSE (occupancy fraction)"); plt.tight_layout(); plt.show()
''')
    md(3,'Each fold fits a fresh LinearRegression on training rows only; identical shuffled five-fold splits use seed 10. The significance screen and Boruta/Cp exploration precede this fixed-specification CV, so it is not nested validation of the entire selection procedure. Nearby spaces/tracts occur in both folds; this is held-out-space accuracy within the observed setting, not new-neighborhood or future-time performance.')
    section(3,'f','Final Model Selection and Justification','Select a final model with economic and statistical reasoning.')
    code(3,'''required = comparison.loc[["Model 1","Model 2","Model 3 (rubric)"]]
display(pd.Series({"Highest adjusted R2":required["Adjusted R2"].idxmax(),
                   "Lowest AIC":required["AIC"].idxmin(),"Lowest BIC":required["BIC"].idxmin(),
                   "Lowest CV RMSE":required["Mean 5-fold RMSE"].idxmin()}))
display(Markdown(f"Current Model 3 is carried forward with **{len(predictors)} slopes** on **{len(data):,} spaces**. Its adjusted R² is **{model3.rsquared_adj:.5f}**, AIC **{model3.aic:.2f}**, BIC **{model3.bic:.2f}**, and mean held-out RMSE **{fold_errors['Model 3 (rubric)'].mean():.5f}**. These are computed values, not copied reference constants."))
table_dir = root/"reports/tables"; table_dir.mkdir(parents=True,exist_ok=True)
(table_dir/"current_model_comparison.json").write_text(comparison.to_json(orient="index",indent=2))
''')
    md(3,'The final specification satisfies the explicit full-candidate significance rule and represents price, density, travel context, tariff structure and commercial composition. Selection is justified by the displayed criteria among the required competitors, while the Cp optimum and former specification remain visible. Retaining both business counts makes the retail coefficient a composition association holding total registrations fixed. Neither good fit nor small p-values validates causality or the OLS assumptions; Section 4 checks them.')

    section(4,'a','Linearity: Residuals vs. Fitted and RESET','Residual/fitted plot and RESET test.')
    code(4,SETUP+MODELS)
    code(4,'''from statsmodels.stats.diagnostic import het_breuschpagan, het_white, linear_reset
from statsmodels.stats.stattools import jarque_bera
influence = model3.get_influence()
fitted, residuals = model3.fittedvalues, model3.resid
standardized = influence.resid_studentized_internal
fig, axes = plt.subplots(1,2,figsize=(12,4))
axes[0].scatter(fitted,residuals,s=8,alpha=.25); axes[0].axhline(0,color="red")
axes[0].set(xlabel="Fitted occupancy",ylabel="Residual",title="Current Model 3")
axes[1].scatter(data["population_density"],residuals,s=8,alpha=.25)
axes[1].axhline(0,color="red"); axes[1].set(xlabel="People per sq mile",ylabel="Residual")
plt.tight_layout(); plt.show()
reset = linear_reset(model3,power=2,test_type="fitted",use_f=True)
print("RESET:",reset)
print("Predictions outside [0,1]:",int((~fitted.between(0,1)).sum()))
''')
    md(4,'RESET tests whether a squared fitted term adds explanatory power; rejection flags possible mean misspecification, not a unique remedy. Read the conventional test alongside heteroskedasticity evidence. Tract bands reflect repeated predictors; out-of-range predictions are left visible rather than clipped.')
    section(4,'b','Homoskedasticity: Breusch–Pagan, White, and Scale-Location','Execute both tests and the scale-location plot.')
    code(4,'''bp = het_breuschpagan(residuals,X3)
white = het_white(residuals,X3)
variance_tests = pd.DataFrame([bp,white],index=["Breusch–Pagan (Koenker default)","White"],
                             columns=["LM statistic","LM p","F statistic","F p"])
display(variance_tests)
plt.figure(figsize=(8,4)); plt.scatter(fitted,np.sqrt(np.abs(standardized)),s=8,alpha=.25)
plt.xlabel("Fitted occupancy"); plt.ylabel("sqrt(|internally standardized residual|)")
plt.title("Scale-location"); plt.tight_layout(); plt.show()
uncertainty = pd.DataFrame({"Coefficient":model3.params,"OLS SE":model3.bse,
                           "HC1 SE":hc1.bse,"OLS p":model3.pvalues,"HC1 p":hc1.pvalues})
display(uncertainty)
''')
    md(4,'The variance-test null is constant error variance; small p-values reject it. Final inference uses HC1, which keeps OLS coefficients but adjusts uncertainty under heteroskedasticity. HC1 does not fix endogeneity, omitted mean structure, selection or spatial dependence.')
    section(4,'c','Residual Normality: Q-Q, Jarque–Bera, and Histograms','Show all three residual-normality diagnostics.')
    code(4,'''fig,axes=plt.subplots(1,2,figsize=(12,4))
sm.qqplot(standardized,line="s",ax=axes[0]); axes[0].set_title("Current residual normal Q-Q")
axes[1].hist(residuals,bins=30,edgecolor="white"); axes[1].set(xlabel="Residual",ylabel="Spaces")
plt.tight_layout(); plt.show()
jb=jarque_bera(residuals)
display(pd.Series(jb,index=["JB","p","skewness","kurtosis"]))
display(Markdown(f"Jarque–Bera p={jb[1]:.4g}: **{'reject' if jb[1]<.05 else 'do not reject'}** normality at 5%. This conclusion applies to current Model 3, not the historical specification. A large sample can detect modest deviations; normality is not evidence of exogeneity or independent errors."))
''')
    section(4,'d',"Outliers and Influence: Cook's Distance, Leverage, and DFBETAS",'The rubric requires Cook’s distance, leverage/residual plots and DFBETAS. DFBETAS remains missing because its addition was cancelled by the user.')
    code(4,'''n,p = len(data),len(model3.params)
diagnostics = parking.loc[data.index,["SpaceID","BlockFace","GEOID"]].copy()
diagnostics["Cook D"] = influence.cooks_distance[0]
diagnostics["Leverage"] = influence.hat_matrix_diag
diagnostics["Studentized residual"] = influence.resid_studentized_external
display(diagnostics.nlargest(10,"Cook D"))
fig,axes=plt.subplots(1,2,figsize=(12,4))
axes[0].scatter(diagnostics.index,diagnostics["Cook D"],s=8)
axes[0].axhline(4/n,color="red"); axes[0].set(xlabel="Original source row",ylabel="Cook D")
axes[1].scatter(diagnostics["Leverage"],diagnostics["Studentized residual"],s=8,alpha=.3)
axes[1].axvline(2*p/n,color="red"); axes[1].axhline(2,color="grey");axes[1].axhline(-2,color="grey")
axes[1].set(xlabel="Leverage",ylabel="Externally studentized residual")
plt.tight_layout(); plt.show()
''')
    md(4,'Cook’s 4/n, leverage 2p/n and |studentized residual|>2 are complementary screening rules, not hypothesis-test guarantees or permanent cleaning rules. Source IDs above allow follow-up review; no source observation is deleted. **DFBETAS: Missing.** Its addition was explicitly cancelled by the user, so this required rubric component is not claimed complete.')
    section(4,'e','Robustness: 1,000-Replication Bootstrap vs. OLS','Bootstrap all coefficients 1,000 times and compare to OLS.')
    code(4,'''np.random.seed(90095)
n_boot=1000
draws=[]
for draw in range(n_boot):
    sample=data.sample(n=len(data),replace=True)
    fit=sm.OLS(sample["occupancy_rate"],sm.add_constant(sample[predictors])).fit()
    draws.append(fit.params)
bootstrap=pd.DataFrame(draws)
bootstrap_summary=pd.DataFrame({"OLS estimate":model3.params,"OLS SE":model3.bse,
 "HC1 SE":hc1.bse,"Bootstrap mean":bootstrap.mean(),"Bootstrap SE":bootstrap.std(ddof=1),
 "Bootstrap 95% lower":bootstrap.quantile(.025),"Bootstrap 95% upper":bootstrap.quantile(.975)})
display(bootstrap_summary)
plt.figure(figsize=(8,4));plt.hist(bootstrap["price_midpoint"],bins=30,edgecolor="white")
plt.axvline(model3.params["price_midpoint"],color="red",label="OLS")
plt.xlabel("Price coefficient");plt.ylabel("Bootstrap draws");plt.legend();plt.tight_layout();plt.show()
print("Completed bootstrap draws:",len(bootstrap))
''')
    md(4,'These are ordinary row-bootstrap percentile intervals with the selected predictor set held fixed. Compare centering and dispersion against OLS/HC1 in the table, not only price. Resampling rows assumes independent spaces; it does not reproduce model-selection uncertainty or clustered neighborhood shocks.')
    section(4,'f','Validation: 5-Fold or 10-Fold Cross-Validation and Out-of-Sample Accuracy','Actual five-fold held-out fits and prediction errors.')
    code(4,CV)
    md(4,'This is actual five-fold computation, not a table of copied historical scores. Seed 10 and identical folds make the fixed-specification comparison reproducible; each fit uses its training rows only. The limitations of prior selection and geographically shared folds remain as stated in 3(e). RMSE is in occupancy fractions; multiplying by 100 yields percentage points.')
    section(4,'g','OLS Assumption Violations and Implications','Discuss actual results and retain feasible sensitivity checks.')
    code(4,'''keep=diagnostics["Cook D"]<=4/n
cook_model=sm.OLS(y.loc[keep],X3.loc[keep]).fit(cov_type="HC1")
log_data=data.copy();log_data["log_population_density"]=np.log(log_data["population_density"])
log_predictors=["log_population_density" if v=="population_density" else v for v in predictors]
log_ols=sm.OLS(y,sm.add_constant(log_data[log_predictors])).fit()
log_fit=sm.OLS(y,sm.add_constant(log_data[log_predictors])).fit(cov_type="HC1")
log_reset=linear_reset(log_ols,power=2,test_type="fitted",use_f=True)
days_data=data.loc[parking.loc[data.index,"active_days"].ge(28)]
days_fit=sm.OLS(days_data["occupancy_rate"],sm.add_constant(days_data[predictors])).fit(cov_type="HC1")
all_encoded=pd.concat([parking[["occupancy_rate"]],encoded],axis=1)
income_data=all_encoded[["occupancy_rate",*predictors]].dropna()
income_fit=sm.OLS(income_data["occupancy_rate"],sm.add_constant(income_data[predictors])).fit(cov_type="HC1")
check_fits={"Current primary":hc1,"Cook <=4/n":cook_model,"Log density":log_fit,
            "At least 28 active days":days_fit,"Restore missing-income spaces":income_fit}
robustness=pd.DataFrame({name:{"N":int(f.nobs),"Price":f.params["price_midpoint"],
 "HC1 lower":f.conf_int().loc["price_midpoint",0],"HC1 upper":f.conf_int().loc["price_midpoint",1],
 "Adjusted R2":f.rsquared_adj} for name,f in check_fits.items()}).T
display(robustness)
tests=pd.DataFrame({"Statistic":[bp[0],white[0],float(reset.fvalue),jb[0]],
                    "p":[bp[1],white[1],float(reset.pvalue),jb[1]]},
                   index=["BP LM","White LM","RESET F","Jarque–Bera"])
display(tests)
print("Log-density RESET p:",float(log_reset.pvalue))
display(Markdown(f"Current Model 3: **{'reject' if bp[1]<.05 else 'do not reject'}** constant variance (BP), **{'reject' if white[1]<.05 else 'do not reject'}** constant variance (White), **{'reject' if float(reset.pvalue)<.05 else 'do not reject'}** the RESET null, and **{'reject' if jb[1]<.05 else 'do not reject'}** residual normality at 5%. Read the plots and limitations alongside these decisions; HC1 does not repair a misspecified conditional mean."))
table_dir=root/"reports/tables";table_dir.mkdir(parents=True,exist_ok=True)
(table_dir/"current_diagnostics.json").write_text(json.dumps({
 "predictors":predictors,"n":len(data),"tests":json.loads(tests.to_json(orient="index")),
 "dfbetas_status":"Missing: addition cancelled by user",
 "bootstrap_draws":len(bootstrap),"bootstrap":json.loads(bootstrap_summary.to_json(orient="index")),
 "robustness":json.loads(robustness.to_json(orient="index"))},indent=2))
''')
    md(4,'Heteroskedasticity, mean specification, possible tail deviations and within-tract/spatial dependence qualify inference. Conditional price associations are not causal demand responses; correlated and later-vintage regressors can reflect omitted demand. The common-sample, log-density, Cook and ≥28-day checks are separate comparisons, not new cleaning rules. The saved outcome remains unchanged. Raw 12/48-hour, expanded 20-day and Sunday-reporting sensitivities require original sensor inputs and remain proposed extensions rather than invented results.')

    section(5,'a','Professional Final Regression Table','Present current final model with clearly labeled uncertainty.')
    code(5,SETUP+MODELS)
    code(5,'''regression_table=pd.DataFrame({"OLS coefficient":model3.params,"Conventional SE":model3.bse,
 "HC1 SE":hc1.bse,"Conventional p":model3.pvalues,"HC1 p":hc1.pvalues,
 "HC1 95% lower":hc1.conf_int()[0],"HC1 95% upper":hc1.conf_int()[1]})
regression_table.index.name="Parameter"
display(regression_table.style.format("{:.6g}"))
display(Markdown(f"**Outcome:** monthly occupancy fraction. **N:** {int(model3.nobs):,}; **slopes:** {len(predictors)}; **R²:** {model3.rsquared:.5f}; **adjusted R²:** {model3.rsquared_adj:.5f}. HC1 uses statsmodels' default normal-reference inference; conventional and robust intervals should not be mixed."))
''')
    section(5,'b','Economic Interpretation of All Coefficients','Interpret every coefficient, including the intercept, in economic units.')
    code(5,'''changes=pd.Series({"price_midpoint":1,"population_density":1000,
 "nearby_restaurant_retail_count":100,"transit_share":.1,"walk_share":.1,
 "nearby_business_count":100,"RateType_TOD":1})
labels={"price_midpoint":"$1 higher stated hourly proxy",
 "population_density":"1,000 more people per sq mile",
 "nearby_restaurant_retail_count":"100 more food/retail registrations, total fixed",
 "transit_share":"10-pp higher resident transit share",
 "walk_share":"10-pp higher resident walk share",
 "nearby_business_count":"100 more total registrations, food/retail fixed",
 "RateType_TOD":"TOD versus FLAT"}
effects=pd.DataFrame({"Comparison":[labels[v] for v in predictors],
 "Occupancy difference (pp)":100*hc1.params[predictors]*changes[predictors],
 "HC1 lower (pp)":100*hc1.conf_int().loc[predictors,0]*changes[predictors],
 "HC1 upper (pp)":100*hc1.conf_int().loc[predictors,1]*changes[predictors],
 "HC1 p":hc1.pvalues[predictors]})
display(effects.style.format({c:"{:.4g}" for c in effects if c!="Comparison"}))
for v in predictors:
    effect=effects.loc[v,"Occupancy difference (pp)"]
    lo,hi=effects.loc[v,["HC1 lower (pp)","HC1 upper (pp)"]]
    display(Markdown(f"- **{labels[v]}:** associated with **{abs(effect):.3f} percentage points {'higher' if effect>=0 else 'lower'} occupancy**, holding other included covariates fixed; HC1 95% CI **[{lo:.3f}, {hi:.3f}] pp**."))
display(Markdown(f"**Intercept:** {model3.params['const']:.5f} occupancy, or {100*model3.params['const']:.2f}%, for a FLAT space with zero values for all numeric covariates. This joint zero-covariate profile is outside observed support, so it is an algebraic baseline, not an estimate for a typical parking space."))
''')
    md(5,'Both business counts are in this specification. Holding the total fixed, a higher food/retail count represents a change in registration composition; holding food/retail fixed, a higher total represents other registrations. The negative conditional food/retail coefficient is therefore not the effect of opening new businesses. Shares describe tract residents, and a 10-percentage-point share change is 0.10 in fraction units. No coefficient is interpreted as a proven causal effect.')
    section(5,'c','Statistical vs. Economic Significance','Separate precision from economic importance.')
    code(5,'''display(pd.DataFrame({"HC1 p":hc1.pvalues[predictors],"Significant at 5%":hc1.pvalues[predictors]<.05,
                      "Scaled occupancy pp":effects["Occupancy difference (pp)"]}))
display(Markdown(f"A $1 price comparison is {effects.loc['price_midpoint','Occupancy difference (pp)']:.2f} occupancy pp, against a common-sample mean of {100*y.mean():.2f}%. Economic relevance depends on the realistic price change and local support, not just the p-value. Statistical significance is conditional on selection and the covariance assumptions and does not establish causality."))
''')
    section(5,'d','Confidence Intervals for Key Parameters','Calculate and interpret confidence intervals.')
    md(5,'The tables in 5(a)–5(b) calculate HC1 95% intervals for every parameter and express every slope interval in the same scaled economic units. An interval spanning zero does not establish a nonzero association; an interval excluding zero does not establish an exogenous price effect. The 95% interpretation refers to long-run coverage under the fitted inference assumptions, not a 95% probability attached to a fixed unknown coefficient. Prior selection and correlated neighborhood errors can invalidate nominal coverage; Section 4(e) adds conditional row-bootstrap intervals without claiming to solve those issues.')
    section(5,'e','R² and Model Fit in Economic Context','Explain fit, predictive error and literature comparison.')
    code(5,CV+'''display(Markdown(f"Current Model 3 explains **{100*model3.rsquared:.2f}%** of sample occupancy variation; **{100*(1-model3.rsquared):.2f}%** remains unexplained. Its mean five-fold RMSE is **{100*fold_errors['Model 3 (rubric)'].mean():.2f} occupancy pp**. This monthly cross-sectional error is not an instantaneous availability probability or out-of-city validation."))
''')
    md(5,f'''### Comparison with academic literature

Shoup’s (2006) search-cost mechanism concerns the curb/off-street price tradeoff and scarce spaces. Our positive conditional price association need not contradict it: a cross-location regression can combine strong demand with officials’ higher tariffs, and our outcome does not measure search time. [Shoup (2006)]({SHOUP}).

Pierce and Shoup (2013) report an average elasticity about −0.4 from SFpark adjustments, whereas our level coefficient is an occupancy-fraction difference per dollar across LA spaces. The units and designs differ. A positive LA association cannot be interpreted as an opposite causal elasticity; source dates, omitted demand and tariff assignment differ. [Pierce and Shoup (2013)]({PIERCE}).

The conditional commercial-composition estimates and resident mode shares describe spatial context, not identified demand shifts. Our data therefore support historically aligned tariff-change research rather than a claim that higher tariffs cause occupancy to rise. The 1(d) elasticity translation is an illustrative benchmark, not a fitted restriction.

### Conclusion

We retain the negative demand hypothesis as theory, report the observed conditional associations without sign manipulation, and carry the explicitly defined full-candidate-significant Model 3 through actual fit, validation and diagnostic procedures. Economic size, uncertainty and unresolved specification/dependence limits must be read together. Prior seven-predictor estimates remain supporting historical evidence, not mislabeled current results.''')
    code(5,'''table_dir=root/"reports/tables";table_dir.mkdir(parents=True,exist_ok=True)
(table_dir/"current_final_results.json").write_text(json.dumps({
 "n":len(data),"predictors":predictors,"selection_rule":"all conventional p<.05 slopes in original 12-candidate full OLS",
 "coefficients":json.loads(regression_table.to_json(orient="index")),
 "economic_effects":json.loads(effects.to_json(orient="index")),
 "model_comparison":json.loads(comparison.to_json(orient="index"))},indent=2))
''')

    section(6,'a','Key Data, Methodological, and Scope Limitations','Discuss data, methodology and scope.')
    md(6,'The monthly outcome assumes recorded states persist until the next transaction over retained intervals, excludes UNKNOWN starts and gaps above 24 hours, and uses ≥25 raw-active days rather than verified full monitoring. Sensor selection, systematic reporting (including Sundays), unequal retained minutes and unverified boundary coverage limit outcome validity. Inventory time-limit mapping (including `2HR-30MIN`) and broader coordinate anomalies remain source caveats.\n\nAugust 2025 occupancy is paired with October 2026 price/business snapshots, 2020–2024 ACS and 2024 geography. Business registrations are not necessarily distinct storefronts active during the outcome month, and missing coordinates/classifications limit counts. Only 49/4,139 zoning codes match; zoning cannot reliably control land use, and no nearest-parcel substitute is invented.\n\nOLS is unconstrained for a bounded outcome. Residual variance/mean/normality concerns must use the **current** diagnostic outputs. Multiple spaces share only 45 common-sample tracts; repeated neighborhood values and local shocks can correlate errors. HC1, row bootstrap and random-space CV do not eliminate that dependence. Selection-conditioned p-values are not adjustment for the search across candidate models. These issues qualify inference even when slopes are significant.')
    section(6,'b','Potential Sources of Bias','Identify mechanisms and their implications.')
    md(6,'Demand-responsive tariff setting and omitted employment, parking supply, enforcement, destinations and events can jointly affect prices and occupancy; this can generate a positive association despite downward demand. Later-vintage proxies introduce measurement error that need not be classical or simply attenuating. Sensor-equipped spaces, inventory linkage and common-sample exclusion can select the population. Business composition and residential mode shares are imperfect proxies for actual parker demand. No net direction for all biases can be identified from these data; reversing a coefficient would not resolve them.')
    section(6,'c','Policy Implications','Describe policy implications where applicable.')
    md(6,'The findings motivate collecting historically aligned prices, occupancy and supply before evaluating demand-responsive pricing. They do not justify raising tariffs because a cross-sectional slope is positive, nor removing commercial activity because a conditional composition slope is negative. Assess availability, turnover, spillovers, equity and business access jointly. Monthly average occupancy cannot set a live parking recommendation or a universal occupancy target for every neighborhood.')
    section(6,'d','Concrete Future Research Extensions','Propose specific, feasible next studies.')
    md(6,'First, rebuild separate outcomes from original transactions under 12/24/48-hour gaps and 20/25/28-day eligibility, and compare Sundays with other days. Separate a common-space outcome change from expanded-sample composition and recheck predictor linkage. Second, align tariff/business vintages with the outcome month and collect curb supply/enforcement controls. Third, use repeated tariff/occupancy periods with a credible identification design to examine demand response; report pretrends and confounding rather than equating time changes with causality. Fourth, evaluate spatially grouped and future-time held-out samples and, where course scope permits, tract-aware inference. These are proposed extensions, not methods claimed to have been executed.')
    section(6,'e','External Validity','Define generalizable populations and contexts.')
    md(6,'Evidence concerns retained LADOT sensor-equipped metered spaces represented in August 2025 and the observed tract contexts. It does not establish transfer to all LA neighborhoods, unmetered/private/off-street parking, other cities, future tariff regimes or time-specific availability. Random five-fold results test other spaces from the same observed setting; they are not a transfer test. The historically mismatched proxies further restrict interpreting the fitted associations as an exact snapshot of August 2025 demand.')
    md(6,f'''### References

- Shoup, D. C. (2006). Cruising for parking. *Transport Policy*, 13(6), 479–486. doi:10.1016/j.tranpol.2006.05.005. [Paper]({SHOUP}).
- Pierce, G., & Shoup, D. (2013). Getting the prices right: An evaluation of pricing parking by demand in San Francisco. *Journal of the American Planning Association*, 79(1), 67–81. doi:10.1080/01944363.2013.787307. [Paper]({PIERCE}).
- LADOT. August 2025 Sensor Transactions archive and October 2026 Metered Parking Inventory & Policies snapshot. Source endpoints, retrieval dates and manifests: [project catalog](../docs/data_sources.md).
- U.S. Census Bureau. 2024 ACS five-year estimates B01003/B19013/B25001/B08301, 2024 TIGER/Line tract boundaries and 2024 Gazetteer land areas. Delivered/linked as documented in [construction report](../docs/notebook03_completion_report.md).
- City of Los Angeles Office of Finance. Listing of Active Businesses, October 2026 snapshot; NAICS 722/44/45 subset. City generalized zoning polygons and explicitly documented supplemental retrievals. [Catalog and retrieval provenance](../docs/data_sources.md).
- Dr. Rojas. *Economics 430 Project 1 — Applied Econometric Analysis*, Fall 2026, UCLA. [Assignment PDF](../project1-1%20%281%29.pdf).

The original course-lecture attributions and all additional source references remain preserved in the historical analysis and source documentation. No newly added method is falsely described as having a worked lecture example.''')

    root_report=ROOT/'reports';root_report.mkdir(exist_ok=True)
    manifest={"baseline":BASE,"notebooks":{},"data_sha256":{}}
    for path in (ROOT/'data/processed').glob('*.csv'):
        manifest['data_sha256'][path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
    mapping=json.loads(saved('docs/notebook_cell_migration.json'))
    for i,name in enumerate(NAMES,1):
        letters={1:'abcd',2:'abcdefgh',3:'abcdef',4:'abcdefg',5:'abcde',6:'abcde'}[i]
        gap=' Section 4(d) is Partial: DFBETAS is unimplemented following the user’s cancellation.' if i==4 else ''
        md(i,'## Section Summary and Rubric Coverage\n\n'+', '.join(f'{i}({x})' for x in letters)+' have current methods/evidence or substantive discussion.'+gap+' Computational completion is accepted only after clean-kernel execution passes; names and syllabus review are deferred to final packaging by the group. No grade or causal finding is guaranteed. The historical material below is preserved supporting work, not current status evidence.')
        count=len(books[i].cells)
        old=json.loads(saved(f'notebooks/{name}.ipynb'))
        md(i,'# Historical analysis preserved before rubric completion\n\nEverything below is retained verbatim from commit `96d4bb1`. Its old notebook numbers, model definitions, diagnostic conclusions and compliance claims are historical. Use the current analysis above for submission results. No original calculation, explanation, figure or output has been removed.')
        offset=count+1
        books[i].cells.extend(copy.deepcopy(old['cells']))
        books[i].metadata['spotless_current_cell_count']=count
        books[i].metadata['spotless_preserved_baseline']=BASE
        for m in mapping:
            if m['destination']==f'notebooks/{name}.ipynb':m['destination_index']+=offset
        manifest['notebooks'][name+'.ipynb']={"current_cells":count,"historical_offset":offset,
               "preserved_cells":len(old['cells']),"preserved_sha256":[h(c) for c in old['cells']]}
        # Serialize raw dictionaries so original array/string representations
        # and historical cell payloads are not normalized by nbformat.
        (ROOT/f'notebooks/{name}.ipynb').write_text(json.dumps(books[i],indent=1,ensure_ascii=False)+'\n',encoding='utf-8')
    manifest['cleaning_schema_updates']=normalize_cleaning(mapping)
    (ROOT/'docs/notebook_cell_migration.json').write_text(json.dumps(mapping,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (ROOT/'docs/rubric_completion_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Built six current sections; all previous cells preserved verbatim in appendices.')

def run(only=None):
    import nbformat as nbf
    from nbclient import NotebookClient
    scratch=ROOT/'.validation';kern=scratch/'jupyter/kernels/spotless-current';kern.mkdir(parents=True,exist_ok=True)
    (kern/'kernel.json').write_text(json.dumps({"argv":[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],"display_name":"Spotless current","language":"python"}))
    os.environ['JUPYTER_PATH']=str(scratch/'jupyter')+os.pathsep+os.environ.get('JUPYTER_PATH','')
    os.environ['IPYTHONDIR']=str(scratch/'ipython-current')
    os.environ.pop('PYTHONPATH',None)
    results=[]
    if only and (ROOT/'docs/current_execution_results.json').exists():
        results=[r for r in json.loads((ROOT/'docs/current_execution_results.json').read_text())['runs'] if not r['notebook'].startswith(only)]
    for name in NAMES:
        if only and not name.startswith(only):continue
        path=ROOT/f'notebooks/{name}.ipynb';raw=json.loads(path.read_text(encoding='utf-8'))
        count=raw['metadata']['spotless_current_cell_count']
        current=nbf.reads(json.dumps({**raw,'cells':raw['cells'][:count]}),as_version=4)
        start=time.time();print('Executing '+name,flush=True)
        if any(c.cell_type=='code' for c in current.cells):
            NotebookClient(current,timeout=1800,kernel_name='spotless-current',allow_errors=False,
                           resources={"metadata":{"path":str(path.parent)}}).execute()
        for cell in current.cells:
            if cell.cell_type=='markdown':cell.source=currency(cell.source)
            for output in cell.get('outputs',[]):
                data=output.get('data',{})
                if 'text/markdown' in data:
                    value=data['text/markdown']
                    data['text/markdown']=currency(''.join(value) if isinstance(value,list) else value)
        raw['cells'][:count]=json.loads(nbf.writes(current))['cells']
        raw['metadata']['language_info']=copy.deepcopy(current.metadata.get('language_info',{'name':'python'}))
        # Keep progress-stream CR characters and every other historical payload
        # exactly as Git recorded them; notebook readers may normalize CR to CRLF.
        if not raw['metadata'].get('spotless_history_path'):
            preserved=json.loads(saved(f'notebooks/{name}.ipynb'))['cells']
            raw['cells'][count+1:]=preserved
        path.write_text(json.dumps(raw,indent=1,ensure_ascii=False)+'\n',encoding='utf-8')
        results.append({"notebook":path.name,"status":"PASS","code_cells":sum(c.cell_type=='code' for c in current.cells),"seconds":round(time.time()-start,1)})
        results.sort(key=lambda r:r['notebook'])
        (ROOT/'docs/current_execution_results.json').write_text(json.dumps({"runs":results},indent=2)+'\n')
        print('PASS '+name,flush=True)
    versions={p:importlib.metadata.version(p) for p in ['pandas','numpy','scipy','statsmodels','scikit-learn','matplotlib','boruta','ydata-profiling','geopandas','nbclient','nbconvert','ipykernel']}
    (ROOT/'docs/current_execution_results.json').write_text(json.dumps({"python":sys.version,"versions":versions,"runs":results},indent=2)+'\n')

def export():
    import nbformat as nbf
    from nbconvert import HTMLExporter
    current=[]
    meta_path=ROOT/'reports/submission_metadata.json'
    if not meta_path.exists():meta_path.write_text(json.dumps({"group_members":[],"syllabus_policies_reviewed":False},indent=2)+'\n')
    meta=json.loads(meta_path.read_text())
    names=meta.get('group_members',[])
    title='# Spotless — Metered Parking Occupancy in Los Angeles\n\nECON 430 · Project 1 · UCLA · Fall 2026\n\n'
    title+=('**Group members:** '+', '.join(names)) if names else '**Draft for final packaging: group names will be added by the group.**'
    title+='\n\nOne cross-sectional report. The current analysis, executed outputs, references and all producing Python code follow in rubric order. Original historical analysis remains in the repository appendices. No submission has been made on the group’s behalf.'
    current.append(nbf.v4.new_markdown_cell(title))
    sources=[]
    for name in NAMES:
        nb=nbf.read(ROOT/f'notebooks/{name}.ipynb',as_version=4)
        cells=copy.deepcopy(nb.cells[:nb.metadata['spotless_current_cell_count']])
        for c in cells:
            if c.cell_type=='markdown':
                # Report links target the repository, not nonexistent report-relative notebook files.
                c.source=re.sub(r'\]\(\.\./([^)]*)\)',r'](https://github.com/finnrcase/Spotless/blob/refactor/430-rubric-alignment/\1)',c.source)
                c.source=re.sub(r'\]\((0[1-6]_[^)]*\.ipynb|cleaning/[^)]*\.ipynb)\)',r'](https://github.com/finnrcase/Spotless/blob/refactor/430-rubric-alignment/notebooks/\1)',c.source)
            if c.cell_type=='code':sources.append(f'# {name}\n'+c.source.replace('%matplotlib inline','')+'\n')
        current.extend(cells)
    current.append(nbf.v4.new_markdown_cell(
        '# Appendix — Original data-construction Python source\n\n'
        'The three cleaning notebooks below are provided as source for transparency. '
        'They are **not rerun in this report** because original raw inputs are not present. '
        'Use working directory `notebooks/cleaning/` and the documented raw inputs to rebuild separately. '
        'The main analysis above starts from the three unchanged tracked processed CSVs. '
        'The source includes original export cells; do not run them over fixed originals when validating a rebuild.'))
    cleaning_source=[]
    for path in sorted((ROOT/'notebooks/cleaning').glob('*.ipynb')):
        raw=json.loads(path.read_text(encoding='utf-8'))
        current.append(nbf.v4.new_markdown_cell('## '+path.stem))
        for cell in raw['cells']:
            if cell['cell_type']=='code':
                source=''.join(cell['source'])
                current.append(nbf.v4.new_code_cell(source))
                cleaning_source.append('# '+path.name+'\n'+source+'\n')
    combined=nbf.v4.new_notebook(cells=current,metadata={"language_info":{"name":"python"}})
    inherited_templates=str(Path(sys.base_prefix)/'share/jupyter/nbconvert/templates')
    exporter=HTMLExporter(template_name='lab',extra_template_basedirs=[inherited_templates],
                          extra_template_paths=[inherited_templates])
    exporter.embed_images=True
    body,_=exporter.from_notebook_node(combined)
    body=body.replace('\r\n','\n').replace('\r','\n')
    body='\n'.join(line.rstrip() for line in body.splitlines()).rstrip()+'\n'
    # Generated source remains visible in the HTML and is also exported for convenience.
    (ROOT/'reports/Spotless_ECON430_Project1.html').write_text(body,encoding='utf-8',newline='\n')
    (ROOT/'reports/Spotless_ECON430_source.py').write_text('''"""Source for the current six notebook sections, in report order.
Run with the working directory set to notebooks/. Notebook outputs are in HTML.
Each section reinitializes its own inputs, so source may also be run sectionwise.
"""\n\n'''+ '\n'.join(sources).rstrip()+'\n',encoding='utf-8',newline='\n')
    (ROOT/'reports/Spotless_cleaning_source.py').write_text(
        '"""Original cleaning source. Working directory: notebooks/cleaning/; raw inputs required.\n'
        'Run only in a separate reconstruction workspace to protect fixed processed files.\n"""\n\n'+
        '\n'.join(cleaning_source).rstrip()+'\n',encoding='utf-8',newline='\n')
    print('Exported self-contained HTML report and Python source; group metadata readiness:',bool(names))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['build','run','export']);parser.add_argument('--only')
    args=parser.parse_args()
    if args.action=='run':run(args.only)
    else:{'build':build,'export':export}[args.action]()
