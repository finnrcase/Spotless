"""Source for the current six notebook sections, in report order.
Run with the working directory set to notebooks/. Notebook outputs are in HTML.
Each section reinitializes its own inputs, so source may also be run sectionwise.
"""

# 02_data_description_eda
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from IPython.display import display, Markdown



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


# 02_data_description_eda
definitions = pd.DataFrame([
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


# 02_data_description_eda
numeric_variables = [v for v in candidate_variables if v not in ["RateType", "MeterType"]]
numeric_variables = ["occupancy_rate", *numeric_variables]
descriptive = parking[numeric_variables].describe().T[["count","mean","50%","std","min","max"]].rename(columns={"50%":"median"})
descriptive["skewness"] = parking[numeric_variables].skew()
descriptive["excess kurtosis"] = parking[numeric_variables].kurt()
display(descriptive.round(4))


# 02_data_description_eda
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

# 02_data_description_eda
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

# 02_data_description_eda
correlations = parking[numeric_variables].corr()
fig, ax = plt.subplots(figsize=(12,10))
im = ax.imshow(correlations, cmap="coolwarm", vmin=-1, vmax=1)
ax.set_xticks(range(len(correlations)), correlations.columns, rotation=90)
ax.set_yticks(range(len(correlations)), correlations.index)
fig.colorbar(im, ax=ax, label="Pearson correlation")
ax.set_title("FLAT/TOD outcome and numeric candidates; available-pair correlations")
fig.tight_layout(); plt.show()
display(correlations.round(3))


# 02_data_description_eda
# Include all numeric candidates, even counts and discrete time limits, so
# no analysis variable is silently omitted. Discrete panels are descriptive.
fig, axes = plt.subplots(len(numeric_variables), 2, figsize=(12,3*len(numeric_variables)))
for row, variable in enumerate(numeric_variables):
    values = parking[variable].dropna()
    values.plot.density(ax=axes[row,0])
    axes[row,0].set_title(variable + " — density (descriptive for discrete values)")
    sm.qqplot(values, line="s", ax=axes[row,1])
    axes[row,1].set_title(variable + " — normal Q-Q")
fig.tight_layout(); plt.show()


# 02_data_description_eda
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

# 02_data_description_eda
tract_extremes = parking.groupby("GEOID").agg(
    spaces=("SpaceID", "size"),
    population_density=("population_density", "first"),
    housing_density=("housing_density", "first"),
    median_income=("median_income", "first")
)

tract_extremes.sort_values("population_density", ascending=False).head(5).round(2)

# 02_data_description_eda
parking.nlargest(5, "nearby_restaurant_retail_count")[[
    "SpaceID", "BlockFace", "nearby_restaurant_retail_count",
    "nearby_business_count", "occupancy_rate"
]]

# 02_data_description_eda
missingness = pd.DataFrame({"Missing":parking[candidate_variables].isna().sum(),
                            "Percent":100*parking[candidate_variables].isna().mean()})
display(missingness)
display(parking.loc[parking["median_income"].isna()].groupby("GEOID").agg(Spaces=("SpaceID","size"), Mean_occupancy=("occupancy_rate","mean")))
display(parking.groupby(parking["median_income"].isna())["occupancy_rate"].agg(["count","mean","median"]))


# 02_data_description_eda
from ydata_profiling import ProfileReport
profile_columns = ["occupancy_rate", *X.columns]
profile_data = pd.concat([parking[["occupancy_rate"]], encoded], axis=1)
profile = ProfileReport(profile_data[profile_columns], minimal=True, progress_bar=False)
profile_summary = profile.description_set
print("Profiled rows:", profile_summary.table["n"])
print("Missing cells / variables:", profile_summary.table["n_cells_missing"], profile_summary.table["n_vars_with_missing"])
display(pd.DataFrame({"Profiling alert":[str(a) for a in profile_summary.alerts]}))


# 03_variable_selection_models
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from IPython.display import display, Markdown



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


# 03_variable_selection_models

from boruta import BorutaPy
from sklearn.ensemble import RandomForestRegressor

# Prepare data
parking_Y = y.values
parking_X = X.values.astype(np.float32)

# Random forest
rf = RandomForestRegressor(max_depth=5)

# Boruta
boruta = BorutaPy(
    rf,
    n_estimators="auto",
    verbose=2,
    random_state=10,
    two_step=True
)

boruta.fit(parking_X, parking_Y)

print("\nConfirmed:", list(X.columns[boruta.support_]))


# 03_variable_selection_models

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


# 03_variable_selection_models

full_model = sm.OLS(y, sm.add_constant(X)).fit()

print(full_model.summary())


# 03_variable_selection_models

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


# 03_variable_selection_models

best_cp = cp_results.loc[
    cp_results.groupby("Number of predictors")["Cp"].idxmin()
]

best_cp[["Number of predictors", "Cp", "Adjusted R2"]].round(3)


# 03_variable_selection_models

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


# 03_variable_selection_models

best_8 = cp_results[
    cp_results["Number of predictors"] == 8
].sort_values("Cp").iloc[0]

print("Best 8-variable model:")
for variable in best_8["Variables"]:
    print(variable)

print("\nMallows' Cp:", round(best_8["Cp"], 3))
print("Adjusted R2:", round(best_8["Adjusted R2"], 3))


# 03_variable_selection_models

from statsmodels.stats.outliers_influence import variance_inflation_factor

X_vif = sm.add_constant(X)

vif = pd.DataFrame()
vif["Variable"] = X_vif.columns
vif["VIF"] = [
    variance_inflation_factor(X_vif.values, i)
    for i in range(X_vif.shape[1])
]

vif.round(2)


# 03_variable_selection_models

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


# 03_variable_selection_models
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
                                  "Included in rubric Model 3":[v in predictors for v in X.columns]})
display(selection_table)
print("Current Model 3 predictors:", predictors)


# 03_variable_selection_models
print(model1.summary())

# 03_variable_selection_models
print(model2.summary())

# 03_variable_selection_models
print(model3.summary())

# 03_variable_selection_models
from statsmodels.stats.outliers_influence import variance_inflation_factor
current_vif = pd.DataFrame({"Variable":X3.columns,
 "VIF":[variance_inflation_factor(X3.values,i) for i in range(X3.shape[1])]})
display(current_vif)
current_cp = np.sum(model3.resid**2)/full_model.mse_resid - (len(y)-2*len(model3.params))
print("Current Model 3 Cp:",current_cp, "; minimum searched Cp:",cp_results["Cp"].min())


# 03_variable_selection_models
from sklearn.model_selection import KFold, cross_val_score
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
cv_results.plot(marker="o",figsize=(10,5))
plt.ylabel("Held-out RMSE (occupancy fraction)"); plt.tight_layout(); plt.show()


# 03_variable_selection_models
required = comparison.loc[["Model 1","Model 2","Model 3 (rubric)"]]
display(pd.Series({"Highest adjusted R2":required["Adjusted R2"].idxmax(),
                   "Lowest AIC":required["AIC"].idxmin(),"Lowest BIC":required["BIC"].idxmin(),
                   "Lowest CV RMSE":required["Mean 5-fold RMSE"].idxmin()}))
display(Markdown(f"Current Model 3 is carried forward with **{len(predictors)} slopes** on **{len(data):,} spaces**. Its adjusted R² is **{model3.rsquared_adj:.5f}**, AIC **{model3.aic:.2f}**, BIC **{model3.bic:.2f}**, and mean held-out RMSE **{fold_errors['Model 3 (rubric)'].mean():.5f}**. These are computed values, not copied reference constants."))
table_dir = root/"reports/tables"; table_dir.mkdir(parents=True,exist_ok=True)
(table_dir/"current_model_comparison.json").write_text(comparison.to_json(orient="index",indent=2))


# 04_diagnostics_robustness
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from IPython.display import display, Markdown



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


# 04_diagnostics_robustness
from statsmodels.stats.diagnostic import het_breuschpagan, het_white, linear_reset
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


# 04_diagnostics_robustness
bp = het_breuschpagan(residuals,X3)
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


# 04_diagnostics_robustness
fig,axes=plt.subplots(1,2,figsize=(12,4))
sm.qqplot(standardized,line="s",ax=axes[0]); axes[0].set_title("Current residual normal Q-Q")
axes[1].hist(residuals,bins=30,edgecolor="white"); axes[1].set(xlabel="Residual",ylabel="Spaces")
plt.tight_layout(); plt.show()
jb=jarque_bera(residuals)
display(pd.Series(jb,index=["JB","p","skewness","kurtosis"]))
display(Markdown(f"Jarque–Bera p={jb[1]:.4g}: **{'reject' if jb[1]<.05 else 'do not reject'}** normality at 5%. This conclusion applies to current Model 3, not the historical specification. A large sample can detect modest deviations; normality is not evidence of exogeneity or independent errors."))


# 04_diagnostics_robustness
n,p = len(data),len(model3.params)
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


# 04_diagnostics_robustness
np.random.seed(90095)
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


# 04_diagnostics_robustness
from sklearn.model_selection import KFold, cross_val_score
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


# 04_diagnostics_robustness
keep=diagnostics["Cook D"]<=4/n
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


# 05_results_interpretation
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from IPython.display import display, Markdown



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


# 05_results_interpretation
regression_table=pd.DataFrame({"OLS coefficient":model3.params,"Conventional SE":model3.bse,
 "HC1 SE":hc1.bse,"Conventional p":model3.pvalues,"HC1 p":hc1.pvalues,
 "HC1 95% lower":hc1.conf_int()[0],"HC1 95% upper":hc1.conf_int()[1]})
regression_table.index.name="Parameter"
display(regression_table.style.format("{:.6g}"))
display(Markdown(f"**Outcome:** monthly occupancy fraction. **N:** {int(model3.nobs):,}; **slopes:** {len(predictors)}; **R²:** {model3.rsquared:.5f}; **adjusted R²:** {model3.rsquared_adj:.5f}. HC1 uses statsmodels' default normal-reference inference; conventional and robust intervals should not be mixed."))


# 05_results_interpretation
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


# 05_results_interpretation
display(pd.DataFrame({"HC1 p":hc1.pvalues[predictors],"Significant at 5%":hc1.pvalues[predictors]<.05,
                      "Scaled occupancy pp":effects["Occupancy difference (pp)"]}))
display(Markdown(f"A $1 price comparison is {effects.loc['price_midpoint','Occupancy difference (pp)']:.2f} occupancy pp, against a common-sample mean of {100*y.mean():.2f}%. Economic relevance depends on the realistic price change and local support, not just the p-value. Statistical significance is conditional on selection and the covariance assumptions and does not establish causality."))


# 05_results_interpretation
from sklearn.model_selection import KFold, cross_val_score
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
display(Markdown(f"Current Model 3 explains **{100*model3.rsquared:.2f}%** of sample occupancy variation; **{100*(1-model3.rsquared):.2f}%** remains unexplained. Its mean five-fold RMSE is **{100*fold_errors['Model 3 (rubric)'].mean():.2f} occupancy pp**. This monthly cross-sectional error is not an instantaneous availability probability or out-of-city validation."))


# 05_results_interpretation
table_dir=root/"reports/tables";table_dir.mkdir(parents=True,exist_ok=True)
(table_dir/"current_final_results.json").write_text(json.dumps({
 "n":len(data),"predictors":predictors,"selection_rule":"all conventional p<.05 slopes in original 12-candidate full OLS",
 "coefficients":json.loads(regression_table.to_json(orient="index")),
 "economic_effects":json.loads(effects.to_json(orient="index")),
 "model_comparison":json.loads(comparison.to_json(orient="index"))},indent=2))
