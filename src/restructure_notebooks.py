"""Lossless, deterministic migration from the recorded ECON 430 baseline.

Run from the repository root. Originals are read from Git, never from a
previous migration. This script writes notebooks and cell-level provenance;
it never executes analysis or writes data.
"""
import copy
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tokenize

BASE = '1a6ef43cc32cd4e51d72e928ca2d9edfcfbcbc30'
MAIN = 'e480f468a9366603f908f4a7c72ab6c4b5999925'
ROOT = Path(__file__).resolve().parents[1]
OLD_NAMES = ['01_clean_occupancy', '02_clean_meter_inventory', '03_build_cross_section',
             '04_eda', '05_variable_selection', '06_regression_models', '07_diagnostics', '08_results']
NEW_NAMES = ['01_economic_theory', '02_data_description_eda', '03_variable_selection_models',
             '04_diagnostics_robustness', '05_results_interpretation', '06_limitations_extensions']

def git_bytes(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT)

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

old = {i+1: json.loads(git_bytes(f'notebooks/{name}.ipynb')) for i, name in enumerate(OLD_NAMES)}
baseline_files = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE], cwd=ROOT, text=True).splitlines()
baseline = {'base_commit': BASE, 'main_before': MAIN, 'files': {}, 'notebooks': {}}
for path in baseline_files:
    if not path.startswith('notebooks/'):
        baseline['files'][path] = hashlib.sha256(git_bytes(path)).hexdigest()
for i, nb in old.items():
    baseline['notebooks'][OLD_NAMES[i-1]+'.ipynb'] = {
        'sha256': hashlib.sha256(git_bytes(f'notebooks/{OLD_NAMES[i-1]}.ipynb')).hexdigest(),
        'metadata': nb['metadata'],
        'cells': [{'index': j, 'id': c.get('id'), 'type': c['cell_type'],
                   'cell_sha256': digest(c), 'outputs_sha256': digest(c.get('outputs', []))}
                  for j, c in enumerate(nb['cells'])]}

docs = ROOT/'docs'
docs.mkdir(exist_ok=True)
# Persist the complete pre-edit inventory before writing any notebook.
(docs/'notebook_baseline_inventory.json').write_text(json.dumps(baseline, indent=2)+'\n', encoding='utf-8')

books = {i: {'cells': [], 'metadata': copy.deepcopy(old[4 if i == 2 else 8]['metadata']),
             'nbformat': 4, 'nbformat_minor': 5} for i in range(1, 7)}
mapping = []
sections = {}

def md(book, text):
    books[book]['cells'].append({'cell_type': 'markdown', 'id': 'rubric-'+digest(text)[:16],
                                'metadata': {}, 'source': text.splitlines(keepends=True)})

def take(book, source, indices, note='', rename=False):
    for j in indices:
        cell = copy.deepcopy(old[source]['cells'][j])
        original = copy.deepcopy(cell)
        if rename and cell['cell_type'] == 'code':
            names = ['parking_all', 'parking', 'predictors', 'variables', 'data', 'y', 'X3', 'model3', 'hc1']
            tokens = tokenize.generate_tokens(io.StringIO(''.join(cell['source'])).readline)
            cell['source'] = tokenize.untokenize([
                t._replace(string='results_'+t.string) if t.type == tokenize.NAME and t.string in names else t
                for t in tokens]).splitlines(keepends=True)
        if 'id' not in cell:
            cell['id'] = f'original-{source:02d}-{j:03d}'
        # Keep original execution counts, outputs and cell metadata exactly.
        dest = len(books[book]['cells'])
        books[book]['cells'].append(cell)
        mapping.append({'source_notebook': f'notebooks/{OLD_NAMES[source-1]}.ipynb',
                        'source_index': j, 'source_id': original.get('id'),
                        'destination': f'notebooks/{NEW_NAMES[book-1]}.ipynb',
                        'destination_index': dest, 'destination_id': cell['id'],
                        'heading': sections.get(book, 'Introduction'),
                        'change': note or ('Identifier namespace only; same calculations, sample, models and outputs' if rename else 'Unchanged'),
                        'source_sha256': digest(original), 'destination_sha256': digest(cell)})

def heading(book, id, title, requirement, method, evidence, interpretation, status, gap=''):
    sections[book] = f'{id} {title}'
    md(book, f'<a id="rubric-{id.replace("(", "").replace(")", "").lower()}"></a>\n\n## {id} {title}\n\n'
       f'**Requirement:** {requirement}\n\n**Method:** {method}\n\n**Evidence:** {evidence}\n\n'
       f'**Interpretation:** {interpretation}\n\n**Status: {status}.** {gap}')

titles = ['Economic Theory and Hypothesis', 'Data Description and Exploratory Analysis',
          'Variable Selection and Model Development', 'Final Model Diagnostics and Robustness',
          'Results and Economic Interpretation', 'Limitations, Policy Implications, and Extensions']
points = [15,25,25,20,25,10]
items = [list('abcd'),list('abcdefgh'),list('abcdef'),list('abcdefg'),list('abcde'),list('abcde')]
for i in books:
    toc = '\n'.join(f'- [{i}({x})](#rubric-{i}{x})' for x in items[i-1])
    md(i, f'# Section {i} — {titles[i-1]}\n\n**Assignment Section {i}: {points[i-1]} points.** '
       f'This notebook organizes the existing {titles[i-1].lower()} material without changing the analysis.\n\n'
       f'Authority: [professor’s assignment PDF](../project1-1%20%281%29.pdf), pp. 2–4; '
       f'[exhaustive evidence audit](../docs/rubric_compliance_audit.md). Requirements are paraphrased in each subsection. '
       f'Section 4 letters are organizational labels; the PDF uses diagnostic bullets. Historical numbered headings and forward-looking statements inside preserved cells refer to the original eight-notebook workflow; use this roadmap and the [cell migration audit](../docs/notebook_restructure_audit.md) for current locations. Historical compliance claims are preserved as source material; the new evidence audit supersedes them.\n\n'
       f'### Roadmap\n\n{toc}\n\n### Dependencies and navigation\n\n'
       '[Cleaning pipeline](cleaning/03_build_cross_section.ipynb) → '
       '[fixed cross-section](../data/processed/parking_cross_section.csv). '
       'Run each notebook with its own fresh Python kernel and working directory `notebooks/`. '
       'Sections 1 and 6 are narrative; sections 2–5 reload their own inputs. '
       '[Theory](01_economic_theory.ipynb) · [EDA](02_data_description_eda.ipynb) · '
       '[Models](03_variable_selection_models.ipynb) · [Diagnostics](04_diagnostics_robustness.ipynb) · '
       '[Results](05_results_interpretation.ipynb) · [Limitations](06_limitations_extensions.ipynb).')

heading(1,'1(a)','Economic Research Question','State a clear economic research question.',
        'Retain the original question and distinguish association from causation.', 'Original results introduction below and README §1.',
        'One observation is one sensor-equipped metered space, not one sensor event.', 'Complete')
md(1, '> How is metered parking occupancy associated with the stated price proxy and local demand conditions?\n\n'
      'The preserved introduction in 1(b) supplies the question, sample, theory and hypothesis together; it is retained in full to avoid splitting substantive text.')
heading(1,'1(b)','Relevant Economic Theory and Academic Literature','Provide 2–3 theory-review paragraphs citing at least two academic sources.',
        'Preserve the two literature paragraphs and their source links.', 'Original 08 cell 0, retained below.',
        'Scarce curb space and demand-responsive tariffs motivate the endogeneity caveat.', 'Complete')
take(1,8,[0])
heading(1,'1(c)','Specific, Testable Economic Hypothesis','Formulate a specific testable relationship between key variables.',
        'Retain the stated negative conditional price hypothesis.', 'Final paragraph of the original introduction in 1(b).',
        'The positive observed price coefficient does not support that negative association; it is not a causal demand estimate.', 'Complete')
md(1, 'The original testable prediction is a negative price coefficient holding included demand conditions fixed. '
      'The final results preserve its comparison with the positive estimated association in Section 5.')
heading(1,'1(d)','Expected Coefficient Signs and Magnitudes','Discuss expected coefficient signs and magnitudes based on theory.',
        'Preserve the original sign predictions and explicit refusal to invent a numerical prior.', 'Original 08 cell 0; README §2.',
        'Sign predictions exist, but reporting estimated magnitudes does not supply an ex ante theoretical magnitude.', 'Partial',
        'Theory-based expected magnitudes or a fuller justified magnitude discussion remain outstanding; no estimates or assumptions are changed.')

heading(2,'2(a)','Dataset Source, Time Period, Sample Selection, and Variable Definitions',
        'Describe sources, time period, sample selection and variable definitions.',
        'Retain original EDA setup and the detailed construction documentation.', 'Original 04 cells 0–10; cleaning notebooks; README §§3–9; data_sources.md.',
        'August 2025 occupancy is paired with 2024 ACS and October 2026 price/business proxies.', 'Complete')
take(2,4,range(0,11))
heading(2,'2(b)','Comprehensive Descriptive Statistics','Tabulate mean, median, standard deviation, minimum, maximum, skewness and kurtosis.',
        'Retain the 4,060-space descriptive table; excess kurtosis is labeled.', 'Original 04 cells 11–13.',
        'Income has 4,016 observed values; other numeric candidates have 4,060.', 'Complete')
take(2,4,range(11,14))
heading(2,'2(c)','Histograms, Boxplots, Correlation Heatmap, and Scatterplots','Generate all four visualization types for key relationships.',
        'Retain every EDA visualization and accompanying discussion.', 'Original 04 cells 20–29, saved PNG and tabular outputs.',
        'Pairwise patterns do not identify conditional or causal effects.', 'Complete')
take(2,4,range(20,30))
heading(2,'2(d)','Q-Q Plots and Density Plots','Assess continuous-variable normality with Q-Q and density plots.',
        'Move the original results EDA additions here; namespace their setup to protect the 4,060-space EDA objects.',
        'Original 08 cells 1, 3–7; the plotting loop covers seven variables on the common 4,016-space sample.',
        'Predictor normality is not an OLS requirement. Housing density, walk share and all-business count lack their own Q-Q/density panels.',
        'Partial','Extend plot coverage to the remaining continuous EDA candidates if the rubric is read to cover every continuous candidate.')
take(2,8,[1,3,4,5,6,7],rename=True,note='Moved EDA addition; code variable names prefixed results_ to isolate original results sample; outputs unchanged')
heading(2,'2(e)','Nonlinearities and Potential Transformations','Discuss potential nonlinearities and possible transformations.',
        'Retain right-tail discussion and link the existing log-density sensitivity.', 'Original 04 cell 35; Section 4(a), original 07 cells 23–25.',
        'Log density does not resolve RESET rejection; primary specification is preserved.', 'Complete')
take(2,4,[35])
heading(2,'2(f)','Outlier Detection and Discussion','Comment on outliers using IQR and standardized residual methods.',
        'Retain IQR screens and link model-based residual and influence screens.', 'Original 04 cells 30–34; Section 4(d).',
        'A flag is not a deletion rule; discrete time limits have zero IQR.', 'Complete')
take(2,4,range(30,35))
heading(2,'2(g)','Missing Values, Imputation Decisions, and Sensitivity Analysis','Document patterns, justify treatment or imputation and analyze sensitivity.',
        'Keep missing incomes in EDA; use the documented common sample and restore missing-income spaces in the existing sensitivity.',
        'Original 04 cells 14–19; original 08 cell 9 below; Section 4(g), original 07 cells 45–46.',
        'Income missingness is concentrated in two tracts; no final regressor needs imputation. Restoring 44 spaces changes the price association.', 'Complete')
take(2,4,range(14,20))
take(2,8,[9],rename=True)
heading(2,'2(h)','Pandas Profiling Analysis and Findings','Discuss findings from Pandas Profiling.',
        'Move the executed minimal ProfileReport and its alert interpretation without changing profiling settings.',
        'Original 08 cells 8, 10; saved report summary and alerts.',
        '44 missing incomes and unique/zero alerts are reported; alerts are not proof of recording errors.', 'Complete',
        'Saved execution is present; fresh execution requires the already-declared ydata-profiling package.')
take(2,8,[8,10],rename=True)
md(2,'### Supporting Evidence — Original EDA handoff\n\nThe following original handoff predates the later EDA additions; its planned-work wording is historical.')
take(2,4,[36,37])

md(3,'### Common candidate-sample setup\n\nSelection starts from 12 encoded candidates and 4,016 complete cases. The model-comparison setup later reloads its own data; preserve that boundary.')
take(3,5,range(0,4))
heading(3,'3(a)','Boruta Algorithm','Apply Boruta and document parameters.',
        'Retain RandomForestRegressor(max_depth=5), automatic tree count, seed 10, two_step=True and verbose=2.',
        'Original 05 cells 6–8: 10 confirmed, income and meter type rejected; saved iterations through 30/100.',
        'Boruta importance is not the same as an individual OLS p-value.', 'Complete',
        'Unspecified parameters use package defaults; Boruta 0.4.3 is pinned. Fresh execution requires that declared dependency.')
take(3,5,[6,7,8])
heading(3,'3(b)','Mallows Cp Criterion','Apply Mallows Cp for variable selection.',
        'Retain the full-model variance estimate and exhaustive 4,095 nonempty subsets, including the best-eight display.',
        'Original 05 cells 9–13: minimum Cp 9.949599 (10 predictors), best-eight Cp 11.789.',
        'The preferred seven-predictor model is not the global Cp minimum.', 'Complete')
take(3,5,range(9,14))
heading(3,'3(c)','Variance Inflation Factors','Check multicollinearity with VIF.',
        'Retain full and reduced VIF tables, selection comparison and preferred-model VIFs.',
        'Original 05 cells 4–5, 14–16.', 'Preferred slope VIFs are below two; the intercept VIF is not treated as a slope diagnostic.', 'Complete')
take(3,5,[4,5,14,15,16])
heading(3,'3(d)','Three Competing Regression Models','Develop and economically/statistically justify Models 1, 2 and 3.',
        'Preserve the existing 1-, 3- and 7-predictor specifications and common sample.',
        'Original 06 cells 0–13.', 'Model 3 includes insignificant time limit and transit share and excludes some significant full-model terms.',
        'Partial','Original full-candidate regression has significant walk_share (p<0.001) and nearby_business_count (p<0.001), both omitted from Model 3. Model 3 time limit p=0.098 and transit share p=0.675 are not significant at 5%. The preserved specification is not all significant candidates or a significance-only subset.')
take(3,6,range(0,4))
for title, indices in [
    ('Model 1 — Simple Regression with the Theoretically Most Important Predictor', range(4,7)),
    ('Model 2 — Multiple Regression with 2–3 Key Predictors', range(7,10)),
    ('Model 3 — Multiple Regression with All Statistically Significant Predictors', range(10,14))]:
    md(3,'### '+title+ ('\n\n**Partial:** This is the rubric’s requested model description, not a claim that the unchanged seven-predictor model satisfies it.' if 'Model 3' in title else ''))
    take(3,6,indices)
heading(3,'3(e)','AIC, BIC, Adjusted R², and Cross-Validation Comparison','Compare all models using AIC, BIC, adjusted R² and cross-validation.',
        'Retain the complete in-sample comparison and shuffled five-fold, training-only prediction comparison (seed 10).',
        'Original 06 cells 14–19, 24–28.', 'Model 3 has the best metrics among these fixed specifications; selection and nearby-space leakage limits remain.', 'Complete')
take(3,6,range(14,20))
take(3,6,range(24,29))
heading(3,'3(f)','Final Model Selection and Justification','Select the final model with detailed economic/statistical justification.',
        'Retain the comparison winners and economic rationale alongside the significance discrepancy.',
        'Original 06 cells 29–34; original 08 cells 11–12.', 'The seven-predictor model is preferred among the three compared, with modest prediction gains.', 'Complete')
take(3,6,range(29,35))
books[3]['cells'].append({'cell_type':'code', 'id':'bridge-final-predictors', 'metadata':{},
                         'execution_count':None, 'outputs':[], 'source':[
                             '# Bridge the retained selection list to the moved results summary.\n',
                             'predictors = selected_variables.copy()\n']})
take(3,8,[11,12])
md(3,'### Supporting Evidence — Original coefficient interpretation\n\nRetained in its original execution context; final HC1 interpretation is in Section 5.')
take(3,6,range(20,24))

md(4,'### Reproduce the common sample and unchanged models')
take(4,7,range(0,8))
heading(4,'4(a)','Linearity: Residuals vs. Fitted and RESET','Show residuals versus fitted values and test specification with RESET.',
        'Retain residual panels, RESET and the existing log-density sensitivity.', 'Original 07 cells 8–11 and 20–25.',
        'RESET rejects; log density preserves the price sign but does not repair the functional form.', 'Complete')
take(4,7,range(8,12))
take(4,7,range(20,23))
heading(4,'4(b)','Homoskedasticity: Breusch–Pagan, White, and Scale-Location','Provide BP, White and scale-location diagnostics.',
        'Retain both tests, plot and HC1 comparison.', 'Original 07 cells 15–19.',
        'Both tests reject constant variance; HC1 does not address shared-tract dependence.', 'Complete')
take(4,7,range(15,20))
md(4,'### Supporting Evidence — Linearity follow-up using log density\n\nThis original sensitivity belongs to 4(a), but executes here after the HC1 reference fit it uses has been defined. The original calculation and primary model remain unchanged.')
take(4,7,range(23,26))
heading(4,'4(c)','Residual Normality: Q-Q, Jarque–Bera, and Histograms','Provide all three residual normality checks.',
        'Retain Q-Q/JB cells and the residual histogram within 4(a)’s shared panel.', 'Original 07 cells 12–14 and cell 10.',
        'JB p=0.1469 does not reject normality; this does not validate other assumptions.', 'Complete')
take(4,7,range(12,15))
heading(4,'4(d)',"Outliers and Influence: Cook's Distance, Leverage, and DFBETAS",'Provide Cook’s plot, leverage versus residuals and DFBETAS.',
        'Retain Cook/leverage/studentized-residual screens and existing exclusion sensitivity.', 'Original 07 cells 26–34.',
        'Screens overlap and do not prove bad records. DFBETAS is mentioned but never computed.', 'Partial','DFBETAS implementation, saved results and interpretation are Missing; no new diagnostic is introduced in this reorganization.')
take(4,7,range(26,35))
heading(4,'4(e)','Robustness: 1,000-Replication Bootstrap vs. OLS','Bootstrap coefficients 1,000 times and compare to OLS.',
        'Retain row resampling with seed 90095, all coefficient comparisons and the price histogram.', 'Original 07 cells 35–38.',
        'The row bootstrap holds selection fixed and assumes independent rows.', 'Complete')
take(4,7,range(35,39))
heading(4,'4(f)','Validation: 5-Fold or 10-Fold Cross-Validation and Out-of-Sample Accuracy','Perform five- or ten-fold validation and report held-out accuracy.',
        'Link actual five-fold training-only fits in Section 3(e), preserving the original reference table here.',
        'Section 3(e), original 06 cells 24–28; original 07 cells 39–41 below.',
        'Mean Model 3 held-out RMSE is 0.16532; this is not an untouched test of selection or new-neighborhood performance.', 'Complete')
take(4,7,range(39,42))
heading(4,'4(g)','OLS Assumption Violations and Implications','Document violations and discuss implications.',
        'Retain coverage/sample checks, diagnostic summary, assumptions and remaining raw-sensor work.',
        'Original 07 cells 42–51; final results diagnostic/robustness discussion in Section 5 supplementary material.',
        'Variance and specification violations, spatial dependence and bounded predictions qualify inference; sensor rebuilds remain unexecuted.', 'Complete')
take(4,7,range(42,52))

md(5,'### Reload the unchanged final model')
take(5,8,[1,2])
heading(5,'5(a)','Professional Final Regression Table','Present final model results in a professional regression table.',
        'Retain the original final table distinguishing conventional and HC1 uncertainty.', 'Original 08 cells 13–14.',
        'HC1 changes covariance estimates, not coefficients.', 'Complete')
take(5,8,[13,14])
heading(5,'5(b)','Economic Interpretation of All Coefficients','Interpret every coefficient’s magnitude, direction and units.',
        'Retain final HC1 slope scaling and duplicate the original complete coefficient narrative, including the intercept.',
        'Original 08 cells 15–16 plus original 06 cells 22–23 duplicated below.',
        'Occupancy effects are percentage-point differences. The duplicated narrative’s intervals are conventional OLS; use the labeled HC1 table for final inference.', 'Complete')
take(5,8,[15,16])
take(5,6,[22,23],note='Duplicated verbatim for complete coefficient/intercept narrative; intervals here are conventional, not HC1')
heading(5,'5(c)','Statistical vs. Economic Significance','Distinguish statistical significance from economic significance.',
        'Use economic units and the uncertainty distinction already in 5(b).', 'Original 08 cells 15–16 and original 06 cells 22–23 in 5(b).',
        'A precise association does not imply a causal effect; time limit and transit share remain uncertain.', 'Complete')
heading(5,'5(d)','Confidence Intervals for Key Parameters','Calculate and interpret confidence intervals for key parameters.',
        'Retain HC1 parameter intervals and percentage-point intervals for all slopes.', 'Tables in 5(a)–5(b); price interval interpretation in original 08 cell 15.',
        'Price HC1 interval is about 5.11–6.02 occupancy percentage points per dollar; dependence remains unresolved.', 'Complete')
heading(5,'5(e)','R² and Model Fit in Economic Context','Discuss R² and model fit economically.',
        'Retain fit/prediction tables and discussion.', 'Original 08 cells 17–19.',
        'About 27.36% of within-sample variation is explained; substantial variation remains.', 'Complete')
take(5,8,[17,18,19])
md(5,'### Supporting Evidence — Diagnostics and robustness in the final results\n\nAll original summary calculations and outputs remain here, even where Section 4 contains the primary checks.')
take(5,8,range(20,26))
md(5,'### Conclusion and historical assignment checklist\n\nThe original checklist is retained verbatim. The new audit supersedes its completion claims, particularly expected magnitudes, continuous-variable coverage, and Model 3.')
take(5,8,[27,28])
md(5,'### Literature comparison — audit note\n\nThe theory review motivates scarcity and demand-responsive pricing, while the positive price association and negative conditional commercial-count association differ from the simple demand predictions. '
      'The original conclusion discusses this tension, but a developed comparison of the final findings with the cited studies remains **Partial** under the PDF’s page-4 assessment criterion. No unverified account of those studies’ numerical results is added.')

heading(6,'6(a)','Key Data, Methodological, and Scope Limitations','Discuss data, methodology and scope limitations.',
        'Retain the full original limitations cell and relevant README/documentation evidence.', 'Original 08 cell 26 below; README §8; Section 4(g).',
        'Sensor selection, reporting rules, bounded outcomes, historical mismatches, spatial dependence and incomplete zoning constrain inference.', 'Complete')
take(6,8,[26])
md(6,'### Supporting Evidence — Detailed inherited assumptions\n\n'
      'The [README’s detailed assumptions table](../README.md#8-assumptions-and-methodological-decisions) and '
      '[construction completion report](../docs/notebook03_completion_report.md) remain intact. In particular, only 49/4,139 zoning codes match; '
      'broader inventory coordinates include unresolved anomalies outside the retained base; the `2HR-30MIN` interpretation is unverified; '
      'business registrations can share addresses and omit usable locations; ACS commuter shares characterize residents, not the people parking. '
      'The outcome assumes state persistence over retained intervals, excludes UNKNOWN intervals and gaps above 24 hours, '
      'and counts raw active days rather than continuous monitoring. These are inherited assumptions, not new cleaning rules.')
heading(6,'6(b)','Potential Sources of Bias','Identify biases and how they could affect conclusions.',
        'Retain endogeneity/omission discussion and connect documented measurement/selection limitations.',
        'Original limitations in 6(a); README §§2, 8; Sections 4(g), 5 conclusion.',
        'Demand-responsive prices can confound the positive association; omitted demand, sensor selection and vintage measurement errors may distort slopes. Their net directions are not identified.', 'Complete')
heading(6,'6(c)','Policy Implications','Describe policy implications where applicable.',
        'Duplicate the original cautious conclusion for direct access to its policy discussion.', 'Original 08 cell 27 below.',
        'Historically aligned demand-responsive pricing research is warranted; current associations do not justify a causal tariff recommendation.', 'Complete')
take(6,8,[27],note='Conclusion duplicated verbatim for policy and application context')
heading(6,'6(d)','Concrete Future Research Extensions','Suggest concrete future research extensions.',
        'Retain existing sensor-check plan and application discussion.', 'Original 07 cell 47 duplicated below; conclusion in 6(c); README §13.',
        '12/24/48-hour intervals, 20/25/28-day samples and Sunday reporting need raw inputs; time-specific availability requires future/location validation.', 'Complete')
take(6,7,[47],note='Processing plan duplicated verbatim; remains a plan, not an implemented result')
heading(6,'6(e)','External Validity','State populations/contexts to which results generalize.',
        'Retain the observed-sample limitation and clarify its population/time scope.', 'Original 08 cell 26 in 6(a), original conclusion in 6(c); README §3.',
        'Evidence describes retained sensor-equipped LA metered spaces in August 2025. It does not establish transfer to unmetered parking, other cities/months, all LA neighborhoods, or instantaneous availability.', 'Complete')

gaps = {
    1:'1(a)–1(c) have source evidence. 1(d) is Partial: theory-based expected magnitudes are not developed.',
    2:'Descriptives, four EDA visualization types, nonlinearities, IQR/missingness and profiling have saved evidence. 2(d) is Partial for continuous candidates without Q-Q/density panels. The missing-income sensitivity is in Section 4(g).',
    3:'Boruta, Cp, VIF, comparisons and final justification have saved evidence. 3(d) is Partial: the unchanged seven-variable Model 3 does not include all significant full-candidate terms and retains insignificant terms. No model was changed.',
    4:'All listed diagnostic components have saved evidence except DFBETAS (Missing), making 4(d) Partial. Five-fold evidence is implemented in Section 3(e), not generated by this notebook’s reference table. Raw-sensor rebuilds remain additional uncompleted work.',
    5:'5(a)–5(e) have saved tables and interpretation, including the intercept. Conventional narrative intervals and final HC1 intervals remain explicitly distinguished. Page-4 literature comparison is Partial. Final group PDF/HTML packaging is Missing.',
    6:'6(a)–6(e) have retained discussion and linked detailed evidence. These are limitations and proposed extensions, not completed new models or causal policy findings.'}
for i in books:
    md(i,'## Section Summary and Rubric Coverage\n\n'+gaps[i]+'\n\n'
       'Preserved outputs record earlier execution, not a claim that this migrated workflow has been rerun. '
       'See [validation evidence](../docs/notebook_validation_summary.md) for fresh execution results and blockers, '
       'and the [rubric audit](../docs/rubric_compliance_audit.md) for evidence-backed component status.')

# Cleaning notebooks retain their complete cell order; only relative paths change.
for i in range(1,4):
    nb = copy.deepcopy(old[i])
    for j, c in enumerate(nb['cells']):
        original = copy.deepcopy(c)
        c['source'] = [s.replace('../data/', '../../data/').replace('../docs/', '../../docs/') for s in c['source']]
        # IDs are intentionally untouched here to retain cleaning metadata exactly.
        mapping.append({'source_notebook': f'notebooks/{OLD_NAMES[i-1]}.ipynb', 'source_index': j,
                        'source_id': original.get('id'), 'destination': f'notebooks/cleaning/{OLD_NAMES[i-1]}.ipynb',
                        'destination_index': j, 'destination_id': c.get('id'),
                        'heading': next((s.strip() for s in ''.join(c['source']).splitlines() if s.startswith('#')), 'Original ordered cleaning cell'),
                        'change': 'Relative ../data and ../docs paths gain one parent; saved historical path outputs unchanged' if c != original else 'Unchanged',
                        'source_sha256': digest(original), 'destination_sha256': digest(c)})
    books[6+i] = nb

# Every original cell must have a destination before any notebook is written.
for source, nb in old.items():
    for j in range(len(nb['cells'])):
        assert any(m['source_notebook'] == f'notebooks/{OLD_NAMES[source-1]}.ipynb' and m['source_index'] == j for m in mapping), (source,j)

(docs/'notebook_cell_migration.json').write_text(json.dumps(mapping, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
for i, nb in books.items():
    name = f'notebooks/{NEW_NAMES[i-1]}.ipynb' if i <= 6 else f'notebooks/cleaning/{OLD_NAMES[i-7]}.ipynb'
    path = ROOT/name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False)+'\n', encoding='utf-8')

# Validate migrated objects before removing old working-tree notebook paths.
for m in mapping:
    c = json.loads((ROOT/m['destination']).read_text(encoding='utf-8'))['cells'][m['destination_index']]
    source = OLD_NAMES.index(Path(m['source_notebook']).stem)+1
    orig = old[source]['cells'][m['source_index']]
    assert c.get('outputs',[]) == orig.get('outputs',[])
    assert c.get('metadata',{}) == orig.get('metadata',{})
    assert c.get('execution_count') == orig.get('execution_count')
    if m['change'] == 'Unchanged':
        compare = copy.deepcopy(c)
        if 'id' not in orig:
            compare.pop('id',None)
        assert compare == orig
for name in OLD_NAMES:
    (ROOT/f'notebooks/{name}.ipynb').unlink(missing_ok=True)

lines = ['# Notebook restructure audit', '', f'Baseline: `{BASE}` on `Kerem_Vis`; main recorded as `{MAIN}`.', '',
         'Migration branch: `refactor/430-rubric-alignment`. Original notebooks remain recoverable from the baseline commit. '
         'All original cell sources, outputs (including PNG/HTML), execution counts and metadata have destinations. '
         'Existing cell IDs are preserved; absent analysis IDs get deterministic IDs. Cleaning IDs remain unchanged. '
         'Old working-tree paths were removed only after cell-level preservation assertions passed. No data are overwritten.', '',
         'The JSON inventory was written before notebook edits. [Baseline inventory](notebook_baseline_inventory.json) records original hashes and metadata; '
         '[machine-readable mapping](notebook_cell_migration.json) records each source and destination hash/index. '
         'Indices in this report are zero-based. Duplicate destinations are intentional and individually listed.', '',
         'Reordering moves diagnostics into rubric order, selection into Boruta/Cp/VIF order, and EDA into 2(a)–2(h). '
         'Original internal headings/text and historical completion claims remain verbatim. The new audit supersedes those claims. '
         'The original results EDA setup is duplicated with identifier names prefixed `results_` so it cannot overwrite the original EDA sample. '
         'One new bridge assigns the unchanged selected_variables list to predictors for the moved results summary. '
         'The log-density check executes after the HC1 reference fit under 4(b), with an explicit cross-reference to 4(a). '
         'This setup retains its existing model fits solely as inherited dependencies. No econometric specification changes.', '',
         'README and supporting documentation are retained; current navigation is added separately and obsolete notebook file links are corrected. '
         'Detailed README definitions, source references and assumptions are linked from Sections 1, 2 and 6. '
         'No acquisition source, visualization file, raw/processed input, or preexisting documentation file is deleted.', '']
for source in range(1,9):
    lines += [f'## Original {OLD_NAMES[source-1]}.ipynb', '', '| Index / original ID | Type | Destination / cell | Heading | Change / preservation |', '|---|---|---|---|---|']
    for m in mapping:
        if Path(m['source_notebook']).stem != OLD_NAMES[source-1]: continue
        typ = old[source]['cells'][m['source_index']]['cell_type']
        lines.append(f'| {m["source_index"]} / {m["source_id"] or "absent"} | {typ} | [{Path(m["destination"]).name}](../{m["destination"]}) / {m["destination_index"]} | {m["heading"]} | {m["change"]}; outputs and metadata preserved |')
    lines += ['']
lines += ['## Validation boundary', '', 'See [validation summary](notebook_validation_summary.md). Byte-identical saved outputs establish preservation, not fresh reproducibility.']
(docs/'notebook_restructure_audit.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(f'Mapped all {sum(len(n["cells"]) for n in old.values())} original cells to {len(mapping)} destinations; preserved all saved outputs and metadata.')
