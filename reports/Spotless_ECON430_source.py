"""Spotless ECON 430: analysis source exported from the report notebooks."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parents[1] / 'notebooks')

# 01_economic_theory
# Section 1: Economic Theory and Hypothesis
# 1(a) Economic Research Question
# 1(b) Relevant Economic Theory and Academic Literature
# 1(c) Specific, Testable Economic Hypothesis
# 1(d) Expected Coefficient Signs and Magnitudes
# 02_data_description_eda
# Section 2: Data Description and Exploratory Analysis
# 2(a) Dataset Description
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from IPython.display import display, Markdown, HTML

root = next((folder for folder in [Path.cwd(), *Path.cwd().parents]
             if (folder / "data/processed/parking_cross_section.csv").is_file()), None)
if root is None:
    raise FileNotFoundError("The project data/processed/parking_cross_section.csv file is required.")

parking_full = pd.read_csv(
    root / "data/processed/parking_cross_section.csv",
    dtype={"SpaceID": str, "GEOID": str}
)
parking = parking_full[parking_full["RateType"].isin(["FLAT", "TOD"])].copy()
dependent_variable = "occupancy_rate"

candidate_variables = [
    "price_midpoint", "time_limit_hours", "population_density", "median_income",
    "nearby_restaurant_retail_count", "drive_alone_share", "RateType", "MeterType",
    "housing_density", "transit_share", "walk_share", "nearby_business_count"
]

print("Original spaces:", len(parking_full))
print("FLAT and TOD spaces:", len(parking))
print("Spaces with observed income:", parking["median_income"].notna().sum())
parking["RateType"].value_counts()

# Preserve complete table text in report outputs.
pd.set_option("display.max_colwidth", None)
pd.set_option("display.max_columns", 30)
pd.set_option("display.max_rows", 100)

measurement_table_1 = pd.DataFrame([['Los Angeles Department of Transportation sensor archive and meter inventory', 'Space-level occupancy, price/rate structure, time limits, meter technology and coordinates in Los Angeles', 'August 2025 occupancy; October 2026 inventory snapshot'], ['U.S. Census Bureau ACS, TIGER/Line and Gazetteer', 'Los Angeles County tract population, housing, income, resident commuting, containing tract and land area', 'ACS 2024 five-year release (2020–2024); 2024 geography'], ['Los Angeles Office of Finance business registry', 'Located registered accounts within 0.25 miles of a parking space; all businesses and NAICS 722/44–45 subset', 'October 2026 snapshot']], columns=['Source', 'Variables and geographic coverage', 'Period'])
display(HTML(measurement_table_1.to_html(index=False, escape=True, max_rows=None, max_cols=None, border=0)))

measurement_table_2 = pd.DataFrame([['occupancy_rate', 'Occupied minutes divided by retained valid minutes; a fraction from 0 to 1'], ['price_midpoint', 'Stated hourly price for FLAT meters; midpoint of hourly rate endpoints for TOD meters, in dollars'], ['time_limit_hours', 'Posted time limit mapped to hours'], ['population_density', 'People per square mile of tract land'], ['housing_density', 'Housing units per square mile of tract land'], ['median_income', 'Tract median household income in 2024 dollars'], ['drive_alone_share, transit_share, walk_share', 'Share of resident workers using each mode; the denominator includes workers at home'], ['nearby_restaurant_retail_count', 'Located food-service, drinking-place and retail registrations within 0.25 miles; NAICS 722 and 44–45'], ['nearby_business_count', 'All located business registrations within 0.25 miles'], ['RateType', 'FLAT or TOD pricing structure'], ['MeterType', 'Single-space or multi-space meter']], columns=['Variable', 'Definition and units'])
display(HTML(measurement_table_2.to_html(index=False, escape=True, max_rows=None, max_cols=None, border=0)))

measurement_table_3 = pd.DataFrame([['SpaceID, BlockFace', 'Source parking-space identifier and block-face label; identifiers, not quantitative predictors'], ['occupied_minutes, total_minutes, active_days', 'Retained occupied minutes, retained valid minutes, and distinct transaction-active calendar days'], ['RateRange, MeteredTimeLimit', 'Original stated price and permitted-duration labels retained for traceability'], ['latitude, longitude', 'Meter coordinates in decimal degrees'], ['GEOID', 'Eleven-character identifier of the containing Census tract'], ['population, housing_units', 'ACS tract totals in people and housing units'], ['commuters, drive_alone, public_transit, walked', 'ACS total workers age 16+ and the corresponding resident commute-mode counts; people'], ['ALAND_SQMI', 'Tract land area, excluding water, in square miles; denominator for population/housing density'], ['zoning_code, zoning_class, zoning_description', 'Available source zoning labels; sparse linkage excludes them from regression'], ['tract_match_status, acs_match_status, zoning_match_status', 'Linkage-status categories used to document geographic and attribute matches']], columns=['Supporting field', 'Definition and units'])
display(HTML(measurement_table_3.to_html(index=False, escape=True, max_rows=None, max_cols=None, border=0)))

# 2(b) Descriptive Statistics
numeric_variables = [
    "occupancy_rate", "price_midpoint", "time_limit_hours", "population_density",
    "median_income", "nearby_restaurant_retail_count", "drive_alone_share",
    "housing_density", "transit_share", "walk_share", "nearby_business_count"
]

indicator_data = pd.get_dummies(parking[["RateType", "MeterType"]], drop_first=True, dtype=int)
descriptive_data = parking[numeric_variables].join(indicator_data)
descriptive = descriptive_data.describe().T[
    ["count", "mean", "50%", "std", "min", "max"]
].rename(columns={"50%": "median"})
descriptive["skewness"] = descriptive_data.skew()
descriptive["excess_kurtosis"] = descriptive_data.kurt()
descriptive["kurtosis"] = descriptive["excess_kurtosis"] + 3
descriptive.round(3)

category_counts = pd.concat({
    name: parking[name].value_counts(dropna=False).rename("Spaces").to_frame()
    for name in ["RateType", "MeterType"]
}, names=["Variable", "Category"])
display(category_counts)

# 2(c) Histograms, Boxplots, Correlations and Scatterplots
plot_variables = [
    "occupancy_rate", "price_midpoint", "population_density",
    "median_income", "nearby_restaurant_retail_count"
]
plot_labels = [
    "Occupancy rate", "Price midpoint ($)",
    "Population per square mile", "Median household income (2024 $)",
    "Food-service/retail registrations within 0.25 miles"
]

fig, axes = plt.subplots(5, 2, figsize=(12, 17))

for i, variable in enumerate(plot_variables):
    values = parking[variable].dropna()
    axes[i, 0].hist(values, bins=25, color="steelblue", edgecolor="white")
    axes[i, 0].set_xlabel(plot_labels[i])
    axes[i, 0].set_ylabel("Parking spaces")
    axes[i, 1].boxplot(values)
    axes[i, 1].set_ylabel(plot_labels[i])
    axes[i, 1].set_xticks([])

fig.suptitle("Distributions in the FLAT + TOD sample", fontsize=14)
fig.tight_layout(rect=[0, 0, 1, 0.98])
plt.show()

scatter_variables = [
    "price_midpoint", "population_density", "median_income",
    "nearby_restaurant_retail_count", "drive_alone_share"
]
scatter_labels = [
    "Price midpoint ($)", "Population per square mile",
    "Median household income (2024 $)",
    "Food-service/retail registrations within 0.25 miles",
    "Drive-alone share"
]

fig, axes = plt.subplots(3, 2, figsize=(12, 12))
axes = axes.flatten()

for i, variable in enumerate(scatter_variables):
    axes[i].scatter(
        parking[variable], parking[dependent_variable],
        s=12, alpha=0.25, color="steelblue"
    )
    axes[i].set_xlabel(scatter_labels[i])
    axes[i].set_ylabel("Occupancy rate")
    axes[i].set_ylim(0, 1)

axes[5].axis("off")
fig.suptitle("Occupancy and candidate predictors", fontsize=14)
fig.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()

correlations = descriptive_data.corr()
labels = [
    "Occupancy", "Price", "Time limit", "Population density", "Income",
    "Food/retail count", "Drive-alone share", "Housing density",
    "Transit share", "Walk share", "All-business count", "TOD indicator", "Single-space indicator"
]

assert len(labels) == len(correlations)
fig, ax = plt.subplots(figsize=(13, 11))
heatmap = ax.imshow(correlations, cmap="coolwarm", vmin=-1, vmax=1)
ax.set_xticks(range(len(labels)), labels, rotation=45, ha="right")
ax.set_yticks(range(len(labels)), labels)
fig.colorbar(heatmap, ax=ax, label="Pearson correlation")
ax.set_title("Correlations in the FLAT and TOD sample")
fig.tight_layout()
plt.show()

# 2(d) Q-Q Plots and Density Plots
continuous_variables = [v for v in numeric_variables if v != "time_limit_hours"]
fig, axes = plt.subplots(len(continuous_variables), 2,
                         figsize=(12, 3 * len(continuous_variables)))

for i, variable in enumerate(continuous_variables):
    values = parking[variable].dropna()
    values.plot.density(ax=axes[i, 0])
    axes[i, 0].set_title(variable + ": density")
    sm.qqplot(values, line="s", ax=axes[i, 1])
    axes[i, 1].set_title(variable + ": normal Q-Q")

fig.tight_layout()
plt.show()

# 2(e) Nonlinearities and Possible Transformations
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, name in zip(axes, ["price_midpoint", "population_density", "nearby_restaurant_retail_count"]):
    pairs = parking[[name, "occupancy_rate"]].dropna().copy()
    pairs["bin"] = pd.qcut(pairs[name], q=10, duplicates="drop")
    means = pairs.groupby("bin", observed=True).agg(
        predictor_mean=(name, "mean"), occupancy_mean=("occupancy_rate", "mean"),
        spaces=("occupancy_rate", "size"))
    ax.plot(means.predictor_mean, means.occupancy_mean, "o-")
    ax.set(xlabel=name, ylabel="Mean occupancy")
fig.suptitle("Binned relationships: descriptive screens for nonlinearity")
fig.tight_layout()
plt.show()

# 2(f) Outliers
q1 = parking[numeric_variables].quantile(0.25)
q3 = parking[numeric_variables].quantile(0.75)
iqr = q3 - q1
lower_fence = q1 - 1.5 * iqr
upper_fence = q3 + 1.5 * iqr

outside_fences = (
    parking[numeric_variables].lt(lower_fence)
    | parking[numeric_variables].gt(upper_fence)
)

iqr_check = pd.DataFrame({
    "observed_count": parking[numeric_variables].count(),
    "lower_fence": lower_fence,
    "upper_fence": upper_fence,
    "outside_count": outside_fences.sum(),
    "outside_percent": outside_fences.sum() / parking[numeric_variables].count() * 100
})

iqr_check.round(3)

tract_extremes = parking.groupby("GEOID").agg(
    spaces=("SpaceID", "size"),
    population_density=("population_density", "first"),
    housing_density=("housing_density", "first"),
    median_income=("median_income", "first")
)

tract_extremes.sort_values("population_density", ascending=False).head(5).round(2)

parking.nlargest(5, "nearby_restaurant_retail_count")[[
    "SpaceID", "BlockFace", "nearby_restaurant_retail_count",
    "nearby_business_count", "occupancy_rate"
]]

# 2(g) Missing Values and Sensitivity Analysis
eda_variables = ["occupancy_rate"] + candidate_variables
missingness = pd.DataFrame({
    "Missing": parking[eda_variables].isna().sum(),
    "Percent": parking[eda_variables].isna().mean() * 100
})
display(missingness.round(2))

missing_income = parking["median_income"].isna()
display(parking[missing_income].groupby("GEOID").agg(
    spaces=("SpaceID", "size"),
    mean_occupancy=("occupancy_rate", "mean")
))
parking.groupby(missing_income)["occupancy_rate"].agg(
    ["count", "mean", "median"]
).rename_axis("Income missing")

# Missing-income treatment and imputation sensitivity
missing_base = ["price_midpoint", "population_density", "nearby_restaurant_retail_count"]
available = parking.dropna(subset=["occupancy_rate", *missing_base]).copy()
observed_income = available.dropna(subset=["median_income"]).copy()
median_income_fill = observed_income["median_income"].median()
assert pd.notna(median_income_fill)
imputed_income = available.copy()
imputed_income["income_missing"] = imputed_income["median_income"].isna().astype(int)
imputed_income["median_income"] = imputed_income["median_income"].fillna(median_income_fill)
assert imputed_income.loc[imputed_income.income_missing.eq(0), "median_income"].equals(observed_income["median_income"])
missing_fits = [
    ("Income-complete sample; no income regressor", observed_income, missing_base),
    ("All available spaces; no income regressor", available, missing_base),
    ("Complete-case income regressor", observed_income, [*missing_base, "median_income"]),
    ("Median-imputed income + missingness indicator", imputed_income,
     [*missing_base, "median_income", "income_missing"])
]
missing_rows = []
for label, frame, columns in missing_fits:
    fit = sm.OLS(frame.occupancy_rate, sm.add_constant(frame[columns])).fit(cov_type="HC1")
    interval = fit.conf_int().loc["price_midpoint"]
    missing_rows.append({"Treatment": label, "N": int(fit.nobs),
                         "Price association (pp per dollar)": 100 * fit.params["price_midpoint"],
                         "HC1 lower (pp)": 100 * interval[0],
                         "HC1 upper (pp)": 100 * interval[1]})
missing_sensitivity = pd.DataFrame(missing_rows)
display(missing_sensitivity.round(4))
display(Markdown(f"The median fill is **{median_income_fill:,.0f} dollars**, applied to **{int(imputed_income.income_missing.sum())}** spaces. Under the fixed three-predictor specification, restoring missing-income spaces changes the price association from **{missing_sensitivity.iloc[0]['Price association (pp per dollar)']:.3f}** to **{missing_sensitivity.iloc[1]['Price association (pp per dollar)']:.3f}** occupancy pp per dollar. With income included, the complete-case and imputation-benchmark associations are **{missing_sensitivity.iloc[2]['Price association (pp per dollar)']:.3f}** and **{missing_sensitivity.iloc[3]['Price association (pp per dollar)']:.3f}**. These are sensitivity comparisons, not replacements for the final Model 3. HC1 does not address imputation uncertainty or tract dependence."))

# 2(h) Pandas Profiling
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning,
                            message=r"(?s).*import ydata_profiling.*deprecated.*")
    warnings.filterwarnings("ignore", message="IProgress not found.*")
    from ydata_profiling import ProfileReport

profile_data = pd.get_dummies(
    parking[["occupancy_rate"] + candidate_variables], drop_first=True, dtype=int
)
from contextlib import redirect_stderr
from io import StringIO

with redirect_stderr(StringIO()):
    profile = ProfileReport(profile_data, minimal=True, progress_bar=False)
    summary = profile.description_set

print("Observations:", summary.table["n"])
print("Missing cells:", summary.table["n_cells_missing"])
pd.DataFrame({"Profiling alert": [str(alert) for alert in summary.alerts]})

# 03_variable_selection_models
# Section 3: Variable Selection and Model Development
# 3(a) Boruta Algorithm
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from IPython.display import display, Markdown


root = next((folder for folder in [Path.cwd(), *Path.cwd().parents]
             if (folder / "data/processed/parking_cross_section.csv").is_file()), None)
if root is None:
    raise FileNotFoundError("The project data/processed/parking_cross_section.csv file is required.")
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

# Preserve complete table text in report outputs.
pd.set_option("display.max_colwidth", None)
pd.set_option("display.max_columns", 30)
pd.set_option("display.max_rows", 100)


from boruta import BorutaPy
from sklearn.ensemble import RandomForestRegressor

# Prepare data
parking_Y = y.values
parking_X = X.values.astype(np.float32)

# Random forest
rf = RandomForestRegressor(max_depth=5, random_state=10)

# Boruta
boruta = BorutaPy(
    rf,
    n_estimators="auto",
    verbose=0,
    max_iter=100, perc=100, alpha=0.05,
    random_state=10,
    two_step=True
)

boruta.fit(parking_X, parking_Y)

print("\nConfirmed:", list(X.columns[boruta.support_]))


boruta_keep = [
    "Confirmed" if c else "Tentative" if t else "Reject"
    for c, t in zip(boruta.support_, boruta.support_weak_)
]

boruta_features = zip(
    X.columns,
    boruta.ranking_,
    boruta_keep
)

for feat in boruta_features:
    print("Feature: {:<35} Rank: {}, Keep: {}".format(
        feat[0], feat[1], feat[2]
    ))

boruta_confirmed = list(X.columns[boruta.support_])
boruta_tentative = list(X.columns[boruta.support_weak_])
boruta_rejected = list(X.columns[~(boruta.support_ | boruta.support_weak_)])
display(Markdown(f"Boruta confirms **{len(boruta_confirmed)}** predictors: {', '.join(boruta_confirmed)}. It leaves **{len(boruta_tentative)}** tentative and rejects **{len(boruta_rejected)}**: {', '.join(boruta_rejected) if boruta_rejected else 'none'}. This all-relevant screen evaluates nonlinear predictive importance; confirmation does not imply an individually significant OLS slope or a causal effect."))

# 3(b) Mallows Cp Criterion

full_model = sm.OLS(y, sm.add_constant(X)).fit()

print(full_model.summary())


from itertools import combinations

sigma2 = full_model.mse_resid

cp_results = []

for k in range(1, len(X.columns) + 1):
    for cols in combinations(X.columns, k):
        model = sm.OLS(y, sm.add_constant(X[list(cols)])).fit()

        rss = sum(model.resid ** 2)
        p = k + 1

        cp = rss / sigma2 - (len(y) - 2 * p)

        cp_results.append({
            "Variables": cols,
            "Number of predictors": k,
            "Cp": cp,
            "Adjusted R2": model.rsquared_adj
        })

cp_results = pd.DataFrame(cp_results)

cp_results.sort_values("Cp").head(10)


best_cp = cp_results.loc[
    cp_results.groupby("Number of predictors")["Cp"].idxmin()
]

best_cp[["Number of predictors", "Cp", "Adjusted R2"]].round(3)


plt.figure(figsize=(8, 5))

plt.plot(
    best_cp["Number of predictors"],
    best_cp["Cp"],
    marker="o"
)

plt.plot(
    best_cp["Number of predictors"],
    best_cp["Number of predictors"] + 1,
    linestyle="--",
    label="Cp = number of parameters"
)

plt.xlabel("Number of predictors")
plt.ylabel("Mallows' Cp")
plt.title("Mallows' Cp by Model Size")
plt.legend()
plt.show()


best_8 = cp_results[
    cp_results["Number of predictors"] == 8
].sort_values("Cp").iloc[0]

print("Best 8-variable model:")
for variable in best_8["Variables"]:
    print(variable)

print("\nMallows' Cp:", round(best_8["Cp"], 3))
print("Adjusted R2:", round(best_8["Adjusted R2"], 3))

global_cp = cp_results.loc[cp_results["Cp"].idxmin()]
display(Markdown(f"The smallest searched Cp is **{global_cp['Cp']:.3f}**, with **{int(global_cp['Number of predictors'])} slopes** ({int(global_cp['Number of predictors']) + 1} parameters including the intercept). Its predictors are {', '.join(global_cp['Variables'])}. The dashed line in the plot marks Cp equal to the parameter count; the lowest Cp and closeness to this line are related diagnostics, not significance tests."))

# 3(c) Variance Inflation Factors

from statsmodels.stats.outliers_influence import variance_inflation_factor

X_vif = sm.add_constant(X)

vif = pd.DataFrame()
vif["Variable"] = X_vif.columns
vif["VIF"] = [
    variance_inflation_factor(X_vif.values, i)
    for i in range(X_vif.shape[1])
]

vif.round(2)


X_reduced = X.drop(columns=[
    "housing_density",
    "nearby_business_count"
])

X_vif_reduced = sm.add_constant(X_reduced)

vif_reduced = pd.DataFrame({
    "Variable": X_vif_reduced.columns,
    "VIF": [
        variance_inflation_factor(X_vif_reduced.values, i)
        for i in range(X_vif_reduced.shape[1])
    ]
})

vif_reduced.round(2)

# 3(d) Three Competing Regression Models
# Fixed rule: retain EVERY slope with conventional p < 0.05 in the
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
selection_table = pd.DataFrame({"Full-model p":full_model.pvalues.drop("const"),
                                  "Included in Model 3":[v in predictors for v in X.columns]})
selection_table["Selected-model p"] = model3.pvalues.reindex(selection_table.index)
assert model3.pvalues.drop("const").lt(alpha).all()
display(selection_table)
print("Model 3 predictors:", predictors)

# Model 1: Simple Regression with the Theoretically Most Important Predictor
print(model1.summary())

# Model 2: Multiple Regression with 2–3 Key Predictors
print(model2.summary())

# Model 3: Multiple Regression with All Statistically Significant Predictors
print(model3.summary())

from statsmodels.stats.outliers_influence import variance_inflation_factor
current_vif = pd.DataFrame({"Variable":X3.columns,
 "VIF":[variance_inflation_factor(X3.values,i) for i in range(X3.shape[1])]})
display(current_vif)
current_cp = np.sum(model3.resid**2)/full_model.mse_resid - (len(y)-2*len(model3.params))
print("Model 3 Cp:",current_cp, "; minimum searched Cp:",cp_results["Cp"].min())

slope_vif = current_vif.loc[current_vif.Variable.ne("const")].set_index("Variable")["VIF"]
vif_max = slope_vif.idxmax()
vif_over_five = list(slope_vif.loc[slope_vif.gt(5)].index)
display(Markdown(f"In Model 3, the largest slope VIF is **{slope_vif[vif_max]:.2f}** for **{vif_max}**. Predictors above the common screening value 5 are **{', '.join(vif_over_five) if vif_over_five else 'none'}**. These thresholds are heuristics, not automatic deletion rules. Overlapping business measures can inflate individual uncertainty; their retained coefficients describe composition conditional on total activity, and VIF does not diagnose endogeneity."))
display(Markdown(f"Model 3 Cp is **{current_cp:.3f}**, compared with the searched minimum **{cp_results.Cp.min():.3f}**. The final specification follows the declared significance rule rather than claiming to be the global Cp optimum."))

# 3(e) AIC, BIC, Adjusted R², and Cross-Validation Comparison
from sklearn.model_selection import KFold, cross_val_score
from sklearn.linear_model import LinearRegression
folds = KFold(n_splits=5, shuffle=True, random_state=10)
fits = {"Model 1": model1, "Model 2": model2, "Model 3": model3,
        "Seven-predictor sensitivity": legacy_model}
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
cv_results.plot(marker="o",figsize=(10,5))
plt.ylabel("Held-out RMSE (occupancy fraction)"); plt.tight_layout(); plt.show()

# 3(f) Final Model Selection and Justification
required = comparison.loc[["Model 1","Model 2","Model 3"]]
display(pd.Series({"Highest adjusted R2":required["Adjusted R2"].idxmax(),
                   "Lowest AIC":required["AIC"].idxmin(),"Lowest BIC":required["BIC"].idxmin(),
                   "Lowest CV RMSE":required["Mean 5-fold RMSE"].idxmin()}))
display(Markdown(f"Model 3 is carried forward with **{len(predictors)} slopes** on **{len(data):,} spaces**. Its adjusted R² is **{model3.rsquared_adj:.5f}**, AIC **{model3.aic:.2f}**, BIC **{model3.bic:.2f}**, and mean held-out RMSE **{fold_errors['Model 3'].mean():.5f}**. "))
table_dir = root/"reports/tables"; table_dir.mkdir(parents=True,exist_ok=True)
_export_chars = (table_dir/"current_model_comparison.json").write_text(comparison.to_json(orient="index",indent=2))

delta_rmse = comparison.loc["Model 2", "Mean 5-fold RMSE"] - comparison.loc["Model 3", "Mean 5-fold RMSE"]
display(Markdown(f"Among the three competing specifications, Model 3 has the best displayed adjusted R², AIC, BIC and mean held-out RMSE. Its mean error improves over Model 2 by **{100 * delta_rmse:.3f} occupancy percentage points of RMSE**. It adds travel context, tariff structure and commercial composition to the parsimonious demand controls. This justifies carrying Model 3 forward, while the Cp comparison, correlated regressors, endogenous prices and post-selection uncertainty prevent treating it as a uniquely correct or causal model."))

# 04_diagnostics_robustness
# Section 4: Final Model Diagnostics and Robustness
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from IPython.display import display, Markdown


root = next((folder for folder in [Path.cwd(), *Path.cwd().parents]
             if (folder / "data/processed/parking_cross_section.csv").is_file()), None)
if root is None:
    raise FileNotFoundError("The project data/processed/parking_cross_section.csv file is required.")
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

# Preserve complete table text in report outputs.
pd.set_option("display.max_colwidth", None)
pd.set_option("display.max_columns", 30)
pd.set_option("display.max_rows", 100)

from statsmodels.stats.stattools import jarque_bera
from statsmodels.stats.diagnostic import het_breuschpagan, het_white, linear_reset

parking["RateType_TOD"] = parking["RateType"].eq("TOD").astype(int)

print("Common-sample observations:", len(data))
print("Unique spaces:", parking.loc[data.index, "SpaceID"].nunique())
print("Census tracts:", parking.loc[data.index, "GEOID"].nunique())

X1 = sm.add_constant(data[["price_midpoint"]])
model1 = sm.OLS(y, X1).fit()

X2 = sm.add_constant(data[[
    "price_midpoint", "population_density",
    "nearby_restaurant_retail_count"
]])
model2 = sm.OLS(y, X2).fit()

# Fixed rule: retain EVERY slope with conventional p < 0.05 in the
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
model_check = pd.DataFrame({
    "Model": ["Model 1", "Model 2", "Model 3"],
    "N": [int(model1.nobs), int(model2.nobs), int(model3.nobs)],
    "Adjusted R2": [model1.rsquared_adj, model2.rsquared_adj, model3.rsquared_adj],
    "AIC": [model1.aic, model2.aic, model3.aic],
    "BIC": [model1.bic, model2.bic, model3.bic]
})
display(model_check.round(5))
print("Model 3 predictors:", predictors)

model3_hc1 = sm.OLS(y, X3).fit(cov_type="HC1")

coefficient_check = pd.DataFrame({
    "Model 1": model1.params,
    "Model 2": model2.params,
    "Model 3": model3.params
})
coefficient_check.style.format("{:.6g}", na_rep="—")

display(Markdown(f"All three models use **{len(data):,} unique spaces** in **{parking.loc[data.index, 'GEOID'].nunique()} tracts**. Model 3 has adjusted R² **{model3.rsquared_adj:.5f}**, AIC **{model3.aic:.2f}**, and BIC **{model3.bic:.2f}**. Its predictor definition matches the final specification in Sections 3 and 5."))

# 4(a) Linearity
# Inspect the residual plots
fitted = model3.fittedvalues
residuals = model3.resid
influence = model3.get_influence()
standardized = influence.resid_studentized_internal

print("Fitted occupancy outside [0, 1]:", (~fitted.between(0, 1)).sum())
residuals.describe()

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes[0, 0].scatter(fitted, residuals, s=10, alpha=0.3)
axes[0, 0].set_xlabel("Fitted occupancy")
axes[0, 1].scatter(data["price_midpoint"], residuals, s=10, alpha=0.3)
axes[0, 1].set_xlabel("Price midpoint ($)")
axes[1, 0].scatter(data["population_density"], residuals, s=10, alpha=0.3)
axes[1, 0].set_xlabel("Population per square mile")

axes[0, 0].axhline(0, color="red", linestyle="--")
axes[0, 1].axhline(0, color="red", linestyle="--")
axes[1, 0].axhline(0, color="red", linestyle="--")
axes[0, 0].set_ylabel("Residual")
axes[0, 1].set_ylabel("Residual")
axes[1, 0].set_ylabel("Residual")
axes[1, 1].hist(residuals, bins=30, color="steelblue", edgecolor="white")
axes[1, 1].set_xlabel("Residual")
axes[1, 1].set_ylabel("Parking spaces")
fig.suptitle("Model 3 residual checks")
fig.tight_layout()
plt.show()

display(Markdown(f"Residuals are centered near zero overall and range from **{residuals.min():.3f} to {residuals.max():.3f}**. Their spread is not uniform, and shared tract measurements create vertical bands in the density plot. **{int((~fitted.between(0, 1)).sum())} fitted values lie outside [0, 1]**, a limitation of unconstrained OLS for a bounded outcome. Predictions are not clipped."))

# Check the linear functional form
reset = linear_reset(model3, power=2, test_type="fitted", use_f=True)
print(reset)

display(Markdown(f"RESET gives **F = {float(reset.fvalue):.3f}**, **p = {float(reset.pvalue):.3g}**, indicating a functional-form concern at 5%. Because this is the conventional test and heteroskedasticity is present, it is interpreted alongside the residual plots. The right-tailed, positive density variable motivates the log alternative below; the primary specification remains unchanged."))

# Log-density sensitivity
log_data = data.copy()
assert log_data["population_density"].gt(0).all()
log_data["log_population_density"] = np.log(log_data["population_density"])
log_predictors = ["log_population_density" if v == "population_density" else v for v in predictors]
log_X = sm.add_constant(log_data[log_predictors])
log_model = sm.OLS(y, log_X).fit()
log_hc1 = sm.OLS(y, log_X).fit(cov_type="HC1")
log_reset = linear_reset(log_model, power=2, test_type="fitted", use_f=True)
log_comparison = pd.DataFrame({
    "Specification": ["Original density (primary)", "Log density (robustness)"],
    "N": [int(model3.nobs), int(log_model.nobs)],
    "Price coefficient": [model3.params["price_midpoint"], log_model.params["price_midpoint"]],
    "HC1 price SE": [model3_hc1.bse["price_midpoint"], log_hc1.bse["price_midpoint"]],
    "Adjusted R2": [model3.rsquared_adj, log_model.rsquared_adj],
    "AIC": [model3.aic, log_model.aic],
    "BIC": [model3.bic, log_model.bic],
    "RESET p-value": [float(reset.pvalue), float(log_reset.pvalue)]
})
log_comparison.style.format({"Price coefficient": "{:.6f}", "HC1 price SE": "{:.6f}",
    "Adjusted R2": "{:.5f}", "AIC": "{:.2f}", "BIC": "{:.2f}", "RESET p-value": "{:.3e}"})

display(Markdown(f"With log density, price changes from **{model3.params['price_midpoint']:.5f} to {log_model.params['price_midpoint']:.5f}**. Adjusted R² changes from **{model3.rsquared_adj:.5f} to {log_model.rsquared_adj:.5f}**, and AIC changes from **{model3.aic:.2f} to {log_model.aic:.2f}**. RESET still rejects (**p = {float(log_reset.pvalue):.3g}**). The transformation preserves the positive price association without resolving the specification concern."))

# 4(b) Homoskedasticity
# Check constant variance and compare robust uncertainty
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(fitted, np.sqrt(np.abs(standardized)), s=10, alpha=0.3)
ax.set_xlabel("Fitted occupancy")
ax.set_ylabel("Square root of |standardized residual|")
ax.set_title("Model 3: scale-location plot")
fig.tight_layout()
plt.show()

bp = het_breuschpagan(residuals, X3)
white = het_white(residuals, X3)
variance_tests = pd.DataFrame({
    "Test": ["Breusch–Pagan (default Koenker version)", "White"],
    "LM statistic": [bp[0], white[0]],
    "LM p-value": [bp[1], white[1]],
    "F statistic": [bp[2], white[2]],
    "F p-value": [bp[3], white[3]]
})
variance_tests.style.format({
    "LM statistic": "{:.3f}", "LM p-value": "{:.3e}",
    "F statistic": "{:.3f}", "F p-value": "{:.3e}"
})

display(Markdown(f"Both tests reject constant variance: the Breusch–Pagan LM p-value is **{bp[1]:.3g}**, and White's is **{white[1]:.3g}**. Conventional standard errors, intervals and tests therefore need caution. HC1 changes uncertainty estimates, not OLS coefficients, and does not correct a misspecified mean. HC1 still treats different spaces as independent."))

robust_comparison = pd.DataFrame({
    "Coefficient": model3.params,
    "OLS SE": model3.bse,
    "HC1 SE": model3_hc1.bse,
    "OLS p-value": model3.pvalues,
    "HC1 p-value": model3_hc1.pvalues,
    "HC1 95% lower": model3_hc1.conf_int()[0],
    "HC1 95% upper": model3_hc1.conf_int()[1]
})
print("Largest coefficient change:", (model3.params - model3_hc1.params).abs().max())
robust_comparison.style.format({
    "Coefficient": "{:.6g}", "OLS SE": "{:.6g}", "HC1 SE": "{:.6g}",
    "OLS p-value": "{:.3e}", "HC1 p-value": "{:.3e}",
    "HC1 95% lower": "{:.6g}", "HC1 95% upper": "{:.6g}"
})

display(Markdown(f"The price estimate stays **{model3.params['price_midpoint']:.5f}**. Its HC1 SE is **{model3_hc1.bse['price_midpoint']:.6f}**, compared with conventional SE **{model3.bse['price_midpoint']:.6f}**; the HC1 95% interval is **[{model3_hc1.conf_int().loc['price_midpoint', 0]:.5f}, {model3_hc1.conf_int().loc['price_midpoint', 1]:.5f}]**. The positive association remains statistically clear. HC1 normal-reference inference does not account for within-tract dependence or model selection."))

# 4(c) Residual Normality
# Check residual normality
fig, ax = plt.subplots(figsize=(7, 5))
sm.qqplot(standardized, line="s", ax=ax)
ax.set_title("Model 3: Q-Q plot of standardized residuals")
fig.tight_layout()
plt.show()

jb = jarque_bera(residuals)
normality = pd.Series(jb, index=["JB statistic", "P-value", "Skewness", "Kurtosis"])
normality

display(Markdown(f"Jarque–Bera is **{jb[0]:.3f}**, **p = {jb[1]:.4f}**; residual normality is **{'rejected' if jb[1] < .05 else 'not rejected'} at 5%**. Skewness is **{jb[2]:.3f}** and kurtosis **{jb[3]:.3f}**. The Q-Q plot shows the shape and tail departures. Normality alone does not establish constant variance, independence, or correct conditional-mean specification."))

# 4(d) Outliers and Influence
# Screen for influential observations
diagnostics = parking.loc[data.index, ["SpaceID", "BlockFace", "GEOID"]].copy()
diagnostics["cooks_d"] = influence.cooks_distance[0]
diagnostics["hat_diag"] = influence.hat_matrix_diag
diagnostics["studentized_residual"] = influence.resid_studentized_external
diagnostics["standardized_residual"] = influence.resid_studentized_internal

n = int(model3.nobs)
p = len(model3.params)
cook_cutoff = 4 / n
leverage_cutoff = 2 * p / n

diagnostics["cook_flag"] = diagnostics["cooks_d"] > cook_cutoff
diagnostics["leverage_flag"] = diagnostics["hat_diag"] > leverage_cutoff
diagnostics["residual_flag"] = diagnostics["studentized_residual"].abs() > 2
diagnostics["standardized_flag"] = diagnostics["standardized_residual"].abs() > 2

print("Rows align with the model:", diagnostics.index.equals(model3.model.data.row_labels))
print("n, p (including intercept):", n, p)
print("Cook cutoff:", cook_cutoff)
print("Leverage cutoff:", leverage_cutoff)
diagnostics[["cook_flag", "leverage_flag", "residual_flag", "standardized_flag"]].sum()

diagnostics.nlargest(10, "cooks_d")[[
    "SpaceID", "BlockFace", "GEOID", "cooks_d", "hat_diag",
    "studentized_residual", "cook_flag", "leverage_flag", "residual_flag"
]]

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].scatter(diagnostics.index, diagnostics["cooks_d"], s=10, alpha=0.5)
axes[0].axhline(cook_cutoff, color="red", linestyle="--", label="4/n")
axes[0].set_xlabel("Original CSV row index")
axes[0].set_ylabel("Cook's distance")
axes[0].legend()
axes[1].scatter(diagnostics["hat_diag"], diagnostics["studentized_residual"],
                s=10, alpha=0.4)
axes[1].axvline(leverage_cutoff, color="red", linestyle="--")
axes[1].axhline(2, color="grey", linestyle="--")
axes[1].axhline(-2, color="grey", linestyle="--")
axes[1].set_xlabel("Leverage")
axes[1].set_ylabel("Externally studentized residual")
fig.suptitle("Model 3 influence screens")
fig.tight_layout()
plt.show()

display(Markdown(f"The screens flag **{int(diagnostics.cook_flag.sum())}/{n:,}** spaces by Cook's distance, **{int(diagnostics.leverage_flag.sum())}/{n:,}** by leverage, and **{int(diagnostics.residual_flag.sum())}/{n:,}** by externally studentized residuals. The internally standardized-residual screen also flags **{int(diagnostics.standardized_flag.sum())}/{n:,}** spaces at |residual| > 2; these groups overlap. The highest Cook's distance is **{diagnostics.cooks_d.max():.5f}**, at SpaceID **{diagnostics.loc[diagnostics.cooks_d.idxmax(), 'SpaceID']}**. Identifiers and neighborhood context warrant review; flags do not establish incorrect records."))

# Coefficient-specific influence: DFBETAS
# Use the fitted model's observation order, retaining original CSV row labels.
dfbetas_model_rows = pd.Index(model3.model.data.row_labels)
dfbetas_values = model3.get_influence().dfbetas
assert dfbetas_values.shape == (int(model3.nobs), len(model3.params))
assert dfbetas_model_rows.is_unique
assert dfbetas_model_rows.equals(X3.index)
assert dfbetas_model_rows.equals(y.index)
assert dfbetas_model_rows.equals(diagnostics.index)
np.testing.assert_allclose(model3.model.exog, X3.loc[dfbetas_model_rows].to_numpy())
np.testing.assert_allclose(model3.model.endog, y.loc[dfbetas_model_rows].to_numpy())
assert np.isfinite(dfbetas_values).all()

dfbetas = pd.DataFrame(
    dfbetas_values, index=dfbetas_model_rows, columns=model3.params.index
)
dfbetas.index.name = "source_row"
assert dfbetas.columns.equals(model3.params.index)
dfbetas_cutoff = 2 / np.sqrt(int(model3.nobs))
print(f"DFBETAS rows verified against model observations: {len(dfbetas):,}")
print(f"Screening rule only: |DFBETAS| > 2/sqrt(n) = {dfbetas_cutoff:.5f}")

# Report magnitude, signed value, and the matching observation for each coefficient.
dfbetas_peak_rows = dfbetas.abs().idxmax()
dfbetas_summary = pd.DataFrame({
    "Max absolute DFBETAS": dfbetas.abs().max(),
    "Signed DFBETAS at maximum": [dfbetas.loc[row, name] for name, row in dfbetas_peak_rows.items()],
    "Source row at maximum": dfbetas_peak_rows,
    "SpaceID at maximum": [parking.loc[row, "SpaceID"] for row in dfbetas_peak_rows],
    "Count above screening rule": dfbetas.abs().gt(dfbetas_cutoff).sum()
})
dfbetas_summary.index.name = "Coefficient"
dfbetas_summary.style.format({
    "Max absolute DFBETAS": "{:.5f}",
    "Signed DFBETAS at maximum": "{:.5f}"
})

fig, axes = plt.subplots(4, 2, figsize=(14, 12), sharex=True)
for ax, name in zip(axes.flat, dfbetas.columns):
    ax.scatter(dfbetas.index, dfbetas[name], s=8, alpha=0.45)
    ax.axhline(0, color="grey", linewidth=0.7)
    ax.axhline(dfbetas_cutoff, color="red", linestyle="--",
               label="±2/√n: screening rule only")
    ax.axhline(-dfbetas_cutoff, color="red", linestyle="--")
    ax.set_title(name)
    ax.set_ylabel("DFBETAS")
    ax.legend(fontsize=8)
for ax in axes[-1]:
    ax.set_xlabel("Original CSV row index (model observations)")
fig.suptitle("Model 3: coefficient-specific influence; flags do not establish bad records")
fig.tight_layout()
plt.show()

from IPython.display import display, Markdown

dfbetas_most_affected = dfbetas_summary["Max absolute DFBETAS"].idxmax()
dfbetas_any_flags = int(dfbetas.abs().gt(dfbetas_cutoff).any(axis=1).sum())
dfbetas_price_peak = dfbetas_summary.loc["price_midpoint"]
display(Markdown(
    f"**DFBETAS interpretation.** {dfbetas_any_flags:,} of {len(dfbetas):,} spaces "
    f"exceed the ±{dfbetas_cutoff:.5f} screening rule for at least one coefficient. "
    f"The largest absolute DFBETAS is "
    f"{dfbetas_summary.loc[dfbetas_most_affected, 'Max absolute DFBETAS']:.5f} "
    f"for **{dfbetas_most_affected}**. For price, the largest absolute value is "
    f"{dfbetas_price_peak['Max absolute DFBETAS']:.5f}, at SpaceID "
    f"**{dfbetas_price_peak['SpaceID at maximum']}**. "
    "The table and panels show which coefficients are most sensitive to individual observations; "
    "the signed values indicate the direction of the full-fit minus deleted-fit change. "
    "Flag counts overlap across coefficients and a low screening threshold can flag many ordinary "
    "observations. These results motivate contextual review, not automatic deletion, and do not "
    "resolve heteroskedasticity, spatial dependence, or endogeneity. "
    "All observations and the original Model 3 remain unchanged."
))
# Guard against unintended changes to the primary model or its sample.
assert int(model3.nobs) == len(dfbetas_model_rows)
np.testing.assert_allclose(model3.params.to_numpy(), np.linalg.lstsq(X3, y, rcond=None)[0])

# Check sensitivity to Cook's-distance flags
keep = diagnostics["cooks_d"] <= cook_cutoff
model3_sensitivity = sm.OLS(y.loc[keep], X3.loc[keep]).fit()

sensitivity = pd.DataFrame({
    "Sample": ["Full sample (primary)", "Cook <= 4/n (sensitivity)"],
    "N": [int(model3.nobs), int(model3_sensitivity.nobs)],
    "Price coefficient": [model3.params["price_midpoint"],
                          model3_sensitivity.params["price_midpoint"]],
    "Price p-value": [model3.pvalues["price_midpoint"],
                      model3_sensitivity.pvalues["price_midpoint"]],
    "Adjusted R2": [model3.rsquared_adj, model3_sensitivity.rsquared_adj]
})
sensitivity.style.format({
    "Price coefficient": "{:.6f}", "Price p-value": "{:.3e}", "Adjusted R2": "{:.5f}"
})

sensitivity_coefficients = pd.DataFrame({
    "Full-sample coefficient": model3.params,
    "Sensitivity coefficient": model3_sensitivity.params,
    "Sensitivity p-value": model3_sensitivity.pvalues
})
sensitivity_coefficients.style.format({
    "Full-sample coefficient": "{:.6g}", "Sensitivity coefficient": "{:.6g}",
    "Sensitivity p-value": "{:.3e}"
})

display(Markdown(f"Excluding **{int((~keep).sum())}** Cook-flagged spaces in the sensitivity fit leaves **{int(model3_sensitivity.nobs):,}** observations. Price changes from **{model3.params['price_midpoint']:.5f} to {model3_sensitivity.params['price_midpoint']:.5f}**, remaining positive. Adjusted R² changes from **{model3.rsquared_adj:.5f} to {model3_sensitivity.rsquared_adj:.5f}**. Screening on residual influence can mechanically improve fit; differences across these samples do not establish superiority. The full sample remains primary, and conventional sensitivity p-values do not resolve heteroskedasticity or dependence."))

# 4(e) Bootstrap
# Bootstrap the preferred specification
np.random.seed(90095)
n_boot = 1000
bootstrap_coefficients = []

for i in range(n_boot):
    sample = data.sample(n=len(data), replace=True)
    X_boot = sm.add_constant(sample[predictors])
    bootstrap_model = sm.OLS(sample["occupancy_rate"], X_boot).fit()
    bootstrap_coefficients.append(bootstrap_model.params)

bootstrap = pd.DataFrame(bootstrap_coefficients)
print("Bootstrap replications:", len(bootstrap))
bootstrap_summary = pd.DataFrame({
    "Original OLS": model3.params,
    "Bootstrap mean": bootstrap.mean(),
    "Bootstrap SE": bootstrap.std(ddof=1),
    "Percentile 95% lower": bootstrap.quantile(0.025),
    "Percentile 95% upper": bootstrap.quantile(0.975)
})
bootstrap_summary.style.format("{:.6g}")

plt.figure(figsize=(8, 5))
plt.hist(bootstrap["price_midpoint"], bins=30, color="steelblue", edgecolor="white")
plt.axvline(model3.params["price_midpoint"], color="red", linestyle="--",
            label="Original OLS price coefficient")
plt.xlabel("Bootstrapped price coefficient")
plt.ylabel("Replications")
plt.title("Price coefficient: 1,000 row-bootstrap samples")
plt.legend()
plt.tight_layout()
plt.show()

display(Markdown(f"The original price coefficient is **{model3.params['price_midpoint']:.5f}**; its bootstrap mean is **{bootstrap_summary.loc['price_midpoint', 'Bootstrap mean']:.5f}**, SE **{bootstrap_summary.loc['price_midpoint', 'Bootstrap SE']:.6f}**, and percentile interval **[{bootstrap_summary.loc['price_midpoint', 'Percentile 95% lower']:.5f}, {bootstrap_summary.loc['price_midpoint', 'Percentile 95% upper']:.5f}]**. Row resampling supports stability of the positive association, conditional on the fixed specification. It assumes independence across spaces despite shared characteristics in 45 tracts, and does not correct endogeneity, mixed source dates, selection uncertainty, or functional form."))

# 4(f) Cross-Validation
# Five-fold held-out prediction accuracy
# Actual held-out predictions for the unchanged specifications, using common folds.
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error

cv_folds = list(KFold(n_splits=5, shuffle=True, random_state=10).split(data))
cv_rows = []
cv_oof = pd.DataFrame(index=data.index)
cv_full_params_before = model3.params.copy()
for cv_name, cv_design in [("Model 1", X1), ("Model 2", X2), ("Model 3", X3)]:
    assert cv_design.index.equals(y.index)
    cv_predictions = pd.Series(np.nan, index=data.index, dtype=float)
    cv_seen = np.zeros(len(data), dtype=int)
    for cv_fold, (cv_train, cv_test) in enumerate(cv_folds, start=1):
        assert not np.intersect1d(cv_train, cv_test).size
        cv_fit = sm.OLS(y.iloc[cv_train], cv_design.iloc[cv_train]).fit()
        cv_pred = cv_fit.predict(cv_design.iloc[cv_test])
        cv_predictions.iloc[cv_test] = cv_pred.to_numpy()
        cv_seen[cv_test] += 1
        cv_rows.append({"Model": cv_name, "Fold": cv_fold,
                        "Training N": len(cv_train), "Held-out N": len(cv_test),
                        "Held-out RMSE": np.sqrt(mean_squared_error(y.iloc[cv_test], cv_pred))})
    assert (cv_seen == 1).all() and cv_predictions.notna().all()
    cv_oof[cv_name] = cv_predictions
cv_fold_results = pd.DataFrame(cv_rows)
cv_summary_actual = cv_fold_results.groupby("Model")["Held-out RMSE"].agg(
    **{"Mean fold RMSE": "mean", "Fold RMSE SD": "std"})
cv_summary_actual["Pooled out-of-fold RMSE"] = [
    np.sqrt(mean_squared_error(y, cv_oof[name])) for name in cv_summary_actual.index]
# Cross-validation uses local fits; the primary Model 3 is untouched.
pd.testing.assert_series_equal(model3.params, cv_full_params_before)
assert int(model3.nobs) == len(data)
display(cv_fold_results.round(5))
display(cv_summary_actual.round(5))
print("Verified five held-out folds per model; each observation predicted once using training-only fits.")
print(f"Model 3 mean fold RMSE: {cv_summary_actual.loc['Model 3', 'Mean fold RMSE']:.5f} "
      f"({100 * cv_summary_actual.loc['Model 3', 'Mean fold RMSE']:.2f} occupancy percentage points).")

display(Markdown(f"Model 3's mean five-fold held-out RMSE is **{cv_summary_actual.loc['Model 3', 'Mean fold RMSE']:.5f}**, or **{100 * cv_summary_actual.loc['Model 3', 'Mean fold RMSE']:.2f} occupancy percentage points**. It has the lowest error of the three fixed specifications. Nearby spaces and common tracts can occur in training and test folds, and selection used this sample. These are held-out-space predictions within the observed setting, not independent validation of the full selection procedure or new-neighborhood accuracy."))

# Validation with training-only predictor selection
selection_rows = []
selection_oof = pd.Series(np.nan, index=data.index, dtype=float)
selection_seen = np.zeros(len(data), dtype=int)
selection_primary_before = model3.params.copy()
for selection_fold, (selection_train, selection_test) in enumerate(cv_folds, start=1):
    assert not np.intersect1d(selection_train, selection_test).size
    screen = sm.OLS(y.iloc[selection_train],
                    sm.add_constant(X.iloc[selection_train], has_constant="add")).fit()
    fold_predictors = list(screen.pvalues.drop("const").loc[lambda value: value < 0.05].index)
    selection_fit = sm.OLS(y.iloc[selection_train],
                          sm.add_constant(X.iloc[selection_train][fold_predictors], has_constant="add")).fit()
    selection_prediction = selection_fit.predict(
        sm.add_constant(X.iloc[selection_test][fold_predictors], has_constant="add"))
    selection_oof.iloc[selection_test] = selection_prediction.to_numpy()
    selection_seen[selection_test] += 1
    selection_rows.append({"Fold": selection_fold,
                           "Training N": len(selection_train), "Held-out N": len(selection_test),
                           "Selected slopes": len(fold_predictors),
                           "Held-out RMSE": np.sqrt(mean_squared_error(y.iloc[selection_test], selection_prediction)),
                           "Predictors selected on training rows": ", ".join(fold_predictors)})
selection_cv = pd.DataFrame(selection_rows)
assert (selection_seen == 1).all() and selection_oof.notna().all()
pd.testing.assert_series_equal(model3.params, selection_primary_before)
selection_cv_summary = pd.Series({
    "Folds": len(selection_cv),
    "Mean fold RMSE": selection_cv["Held-out RMSE"].mean(),
    "Fold RMSE SD": selection_cv["Held-out RMSE"].std(ddof=1),
    "Pooled out-of-fold RMSE": np.sqrt(mean_squared_error(y, selection_oof))
})
display(selection_cv)
display(selection_cv_summary.to_frame("Training-only selection validation"))
display(Markdown(f"Repeating selection within the training folds gives mean held-out RMSE **{selection_cv_summary['Mean fold RMSE']:.5f}**, or **{100 * selection_cv_summary['Mean fold RMSE']:.2f} occupancy percentage points**, compared with **{cv_summary_actual.loc['Model 3', 'Mean fold RMSE']:.5f}** when the selected specification is held fixed. Each observation is predicted once without using its outcome to select slopes or estimate coefficients for that fold. The full-sample final Model 3 and all fixed-model comparison results remain unchanged."))

# 4(g) OLS Violations and Implications
# Check coverage and feasible sample sensitivities
print("Transaction-active days in the primary sample:")
print(parking.loc[data.index, "active_days"].value_counts().sort_index())

valid_month_fraction = parking.loc[data.index, "total_minutes"] / (31 * 24 * 60)
valid_month_fraction.describe()

days_data = data.loc[parking.loc[data.index, "active_days"].ge(28)].copy()
days_model = sm.OLS(days_data["occupancy_rate"], sm.add_constant(days_data[predictors])).fit(cov_type="HC1")
income_data = parking[["occupancy_rate", *predictors]].dropna()
income_model = sm.OLS(income_data["occupancy_rate"], sm.add_constant(income_data[predictors])).fit(cov_type="HC1")

sample_checks = pd.DataFrame([
    ["Primary common sample", model3_hc1],
    ["At least 28 active days", days_model],
    ["Retain missing-income spaces", income_model]
], columns=["Sample", "Fit"])
sample_summary = pd.DataFrame({
    "Sample": sample_checks["Sample"],
    "N": [int(m.nobs) for m in sample_checks["Fit"]],
    "Price coefficient": [m.params["price_midpoint"] for m in sample_checks["Fit"]],
    "HC1 95% lower": [m.conf_int().loc["price_midpoint", 0] for m in sample_checks["Fit"]],
    "HC1 95% upper": [m.conf_int().loc["price_midpoint", 1] for m in sample_checks["Fit"]],
    "Adjusted R2": [m.rsquared_adj for m in sample_checks["Fit"]]
})
sample_summary.round(6)

display(Markdown(f"The 28-day sensitivity contains **{int(days_model.nobs):,} spaces** and gives a price coefficient of **{days_model.params['price_midpoint']:.5f}**, compared with **{model3.params['price_midpoint']:.5f}** in the primary fit. Restoring the 44 missing-income spaces gives **{int(income_model.nobs):,} observations** and **{income_model.params['price_midpoint']:.5f}**; income is not a final predictor, so no imputation is needed. Both preserve a positive association, but the 28-day restriction changes composition rather than the interval definition."))

# Limitations of sensor-threshold comparisons
# Diagnostic findings and implications
diagnostic_summary = pd.DataFrame([['Residual plots', 'Uneven spread; tract bands', 'Inspect variance and mean specification; Residual patterns warrant examination of variance and mean specification.'], ['Jarque–Bera', f'p = {jb[1]:.3g}', ('Reject residual normality at 5%' if jb[1] < .05 else 'Do not reject residual normality at 5%') + '; this does not establish other OLS assumptions.'], ['Breusch–Pagan LM', f'p = {bp[1]:.3e}', 'Reject constant variance; HC1 uncertainty is compared separately.'], ['White LM', f'p = {white[1]:.3e}', 'Reject constant variance'], ['RESET', f'p = {float(reset.pvalue):.3e}', 'Possible functional-form problem'], ['Influence', f"{diagnostics['cook_flag'].sum()} Cook flags / {n}", 'Screening flags, not confirmed errors; Flags warrant contextual review.'], ['DFBETAS', f'Max |DFBETAS| = {dfbetas.abs().to_numpy().max():.5f}; {dfbetas_any_flags} spaces flagged', 'Coefficient-specific screening only; Flags do not justify automatic deletion.'], ['Cook sensitivity', f"Price = {model3_sensitivity.params['price_midpoint']:.5f}", 'Positive price association remains; The full sample remains primary.'], ['Row bootstrap', f"{len(bootstrap):,} draws; price CI [{bootstrap_summary.loc['price_midpoint', 'Percentile 95% lower']:.5f}, {bootstrap_summary.loc['price_midpoint', 'Percentile 95% upper']:.5f}]", 'Positive interval; independence assumed; Within-tract dependence remains unresolved.'], ['Five-fold CV', f"Model 3 mean RMSE {cv_summary_actual.loc['Model 3', 'Mean fold RMSE']:.5f} (computed here)", 'Best of the three fixed models; New-neighborhood validity remains unresolved.'], ['Log-density check', f"Price = {log_model.params['price_midpoint']:.5f}; RESET p = {float(log_reset.pvalue):.3e}", 'Price stable; RESET still rejects; The original specification remains primary.'], ['28 active days', f"N = {int(days_model.nobs)}; price = {days_model.params['price_midpoint']:.5f}", 'Positive association in a stricter sample; This changes sample composition, not the interval definition.'], ['Income-missingness sensitivity', f"N = {int(income_model.nobs)}; price = {income_model.params['price_midpoint']:.5f}", 'Retaining missing-income spaces preserves sign; The original common sample remains primary.'], ['Other sensor thresholds', 'Alternate interval cutoffs not estimated', 'Coverage rules may affect Y and sample']], columns=['Diagnostic', 'Result', 'Interpretation'])
# Two narrow, wrapping tables preserve every character without changing values.
from IPython.display import HTML, display
from html import escape

summary_style = """<style>
.section4-summary {width:100%; table-layout:fixed; border-collapse:collapse; margin-bottom:1.5em;}
.section4-summary th, .section4-summary td {
    white-space:normal !important; overflow-wrap:anywhere;
    overflow:visible !important; text-overflow:clip !important;
    text-align:left !important; vertical-align:top; padding:8px;
    border-bottom:1px solid #bbb; max-width:none !important;
}
.section4-summary th:first-child, .section4-summary td:first-child {width:28%;}
</style>"""
summary_fragments = [summary_style]
for summary_title, summary_columns in [
    ("Diagnostic results", ["Diagnostic", "Result"]),
    ("Diagnostic interpretation and caveats", ["Diagnostic", "Interpretation"])
]:
    with pd.option_context("display.max_colwidth", None):
        summary_table = diagnostic_summary[summary_columns].to_html(
            index=False, escape=True, max_rows=None, max_cols=None,
            classes="section4-summary", border=0)
    # Verify the HTML contains each complete value, without Pandas truncation.
    for summary_column in summary_columns:
        for summary_value in diagnostic_summary[summary_column]:
            assert escape(str(summary_value)) in summary_table
    assert "..." not in summary_table and "…" not in summary_table
    summary_fragments.append("<h4>" + escape(summary_title) + "</h4>" + summary_table)
display(HTML("".join(summary_fragments)))

display(Markdown(f"The full-sample price coefficient is **{100 * model3.params['price_midpoint']:.2f} occupancy percentage points per $1**. HC1 and row-bootstrap intervals exclude zero. Strong variance and RESET rejections mean the linear model is not fully validated. Residual normality is {'rejected' if jb[1] < .05 else 'not rejected'} at 5%; neither result resolves shared-tract dependence, price endogeneity, or mixed data vintages. The full sample remains primary, influence screens do not become deletion rules, and the log-density comparison does not remove the specification concern."))

table_dir = root / "reports/tables"
table_dir.mkdir(parents=True, exist_ok=True)
_diagnostics_export = (table_dir / "current_diagnostics.json").write_text(json.dumps({
    "predictors": predictors, "n": int(model3.nobs),
    "tests": {"BP LM": {"Statistic": bp[0], "p": bp[1]},
              "White LM": {"Statistic": white[0], "p": white[1]},
              "RESET F": {"Statistic": float(reset.fvalue), "p": float(reset.pvalue)},
              "Jarque–Bera": {"Statistic": jb[0], "p": jb[1]}},
    "bootstrap_draws": len(bootstrap),
    "bootstrap": json.loads(bootstrap_summary.to_json(orient="index")),
    "dfbetas": json.loads(dfbetas_summary.to_json(orient="index")),
    "any_dfbetas_flags": dfbetas_any_flags,
    "dfbetas_cutoff": dfbetas_cutoff,
    "model_coefficients": model3.params.to_dict(),
    "influence_screens": diagnostics[["cook_flag", "leverage_flag", "residual_flag", "standardized_flag"]].sum().to_dict(),
    "dfbetas_rows": len(dfbetas),
    "dfbetas_columns": list(dfbetas.columns),
    "cross_validation": json.loads(cv_summary_actual.to_json(orient="index")),
    "selection_aware_cross_validation": selection_cv_summary.to_dict(),
    "selection_aware_folds": json.loads(selection_cv.to_json(orient="records")),
    "robustness": json.loads(sample_summary.set_index("Sample").to_json(orient="index"))
}, indent=2))

# 05_results_interpretation
# Section 5: Results and Economic Interpretation
# 5(a) Professional Final Regression Table
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from IPython.display import display, Markdown


root = next((folder for folder in [Path.cwd(), *Path.cwd().parents]
             if (folder / "data/processed/parking_cross_section.csv").is_file()), None)
if root is None:
    raise FileNotFoundError("The project data/processed/parking_cross_section.csv file is required.")
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
# Fixed rule: retain EVERY slope with conventional p < 0.05 in the
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

# Preserve complete table text in report outputs.
pd.set_option("display.max_colwidth", None)
pd.set_option("display.max_columns", 30)
pd.set_option("display.max_rows", 100)

regression_table=pd.DataFrame({"OLS coefficient":model3.params,"Conventional SE":model3.bse,
 "HC1 SE":hc1.bse,"Conventional p":model3.pvalues,"HC1 p":hc1.pvalues,
 "HC1 95% lower":hc1.conf_int()[0],"HC1 95% upper":hc1.conf_int()[1]})
regression_table.index.name="Parameter"
display(regression_table.style.format("{:.6g}"))
display(Markdown(f"**Outcome:** monthly occupancy fraction. **N:** {int(model3.nobs):,}; **slopes:** {len(predictors)}; **R²:** {model3.rsquared:.5f}; **adjusted R²:** {model3.rsquared_adj:.5f}. HC1 uses statsmodels' default normal-reference inference; conventional and robust intervals should not be mixed."))

# 5(b) Economic Interpretation of All Coefficients
changes=pd.Series({"price_midpoint":1,"population_density":1000,
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

# 5(c) Statistical vs. Economic Significance
display(pd.DataFrame({"HC1 p":hc1.pvalues[predictors],"Significant at 5%":hc1.pvalues[predictors]<.05,
                      "Scaled occupancy pp":effects["Occupancy difference (pp)"]}))
display(Markdown(f"A $1 price comparison is {effects.loc['price_midpoint','Occupancy difference (pp)']:.2f} occupancy pp, against a common-sample mean of {100*y.mean():.2f}%. Economic relevance depends on the realistic price change and local support, not just the p-value. Statistical significance is conditional on selection and the covariance assumptions and does not establish causality."))

# 5(d) Confidence Intervals for Key Parameters
price_interval_pp = 100 * hc1.conf_int().loc["price_midpoint"]
display(Markdown(f"For a **one-dollar higher stated price proxy**, the HC1 95% interval is **{price_interval_pp.iloc[0]:.3f} to {price_interval_pp.iloc[1]:.3f} occupancy percentage points**, holding included covariates fixed. It excludes zero under the fitted inference assumptions, supporting a positive conditional association; it does not identify the occupancy effect of an imposed rate increase. The density, registration, share and TOD intervals in 5(b) use their corresponding economic comparison units, so precision is assessed on the same scale as the estimated change."))

# 5(e) R² and Model Fit in Economic Context
from sklearn.model_selection import KFold, cross_val_score
from sklearn.linear_model import LinearRegression
folds = KFold(n_splits=5, shuffle=True, random_state=10)
fits = {"Model 1": model1, "Model 2": model2, "Model 3": model3,
        "Seven-predictor sensitivity": legacy_model}
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
display(Markdown(f"Model 3 explains **{100*model3.rsquared:.2f}%** of sample occupancy variation; **{100*(1-model3.rsquared):.2f}%** remains unexplained. Its mean five-fold RMSE is **{100*fold_errors['Model 3'].mean():.2f} occupancy pp**. This monthly cross-sectional error is not an instantaneous availability probability or out-of-city validation."))

# Comparison with academic literature
# Conclusion
table_dir=root/"reports/tables";table_dir.mkdir(parents=True,exist_ok=True)
_export_chars = (table_dir/"current_final_results.json").write_text(json.dumps({
 "n":len(data),"predictors":predictors,"selection_rule":"all conventional p<.05 slopes in original 12-candidate full OLS",
 "coefficients":json.loads(regression_table.to_json(orient="index")),
 "economic_effects":json.loads(effects.to_json(orient="index")),
 "model_comparison":json.loads(comparison.to_json(orient="index"))},indent=2))

# 06_limitations_extensions
# Section 6: Limitations, Policy Implications, and Extensions
# 6(a) Key Data, Methodological, and Scope Limitations
# 6(b) Potential Sources of Bias
# 6(c) Policy Implications
# 6(d) Concrete Future Research Extensions
# 6(e) External Validity
# References
