# Spotless — ECON 430 Parking Occupancy Project

UCLA ECON 430 Applied Econometric Analysis. **Current stage:** Notebooks 01–03 are completed. The saved candidate cross-section has **4,139 parking spaces and 36 columns**, including meter, Census, and business measures. Zoning coverage is weak (49 source-code matches); EDA, variable selection, OLS, and diagnostics have not begun.

This README records the current design and workflow. Implemented details come from the notebook code, saved outputs, and local processed files; hypotheses and future work are labeled separately. The earlier [raw-data audit](docs/design_validation_audit.md) and [acquisition catalog](docs/data_sources.md) describe earlier phases, so statements there that no cleaning has occurred are historical, not the project's current status.

## 1. Project overview

Working research question:

> What parking-price, parking-rule, location, and neighborhood characteristics explain differences in metered street-parking occupancy across Los Angeles?

We are constructing a cross-sectional dataset with one observation per LADOT sensor-equipped metered parking space, then estimating OLS models explaining differences in occupancy. The assignment calls for at least 500 observations and five meaningful predictors; Notebook 03 exceeds the observation requirement and supplies more than five candidate predictors. Later model-specific samples and selected predictors have not been determined.

Spotless is also a longer-term parking-availability idea. Live prediction, event/weather features, and other extensions are separate from the current ECON 430 cross-sectional analysis.

## 2. Economic motivation and hypotheses

The main relationship of interest is between parking price and occupancy. Our working hypothesis is that, holding other demand factors constant, higher prices reduce parking demand and are associated with lower occupancy.

Price may be endogenous: LADOT can charge more where underlying demand is already high. A positive observed price–occupancy relationship would therefore not imply that raising prices causes occupancy to increase. The planned models explain conditional associations, without a causal identification strategy.

Greater nearby business activity and population or housing density could increase demand. Time limits may affect turnover and occupancy, but their sign is uncertain. Zoning, neighborhood income, commuting characteristics, and location may help explain systematic demand differences; their effects are hypotheses to investigate, not established findings.

## 3. Unit of observation

**Unit of the saved cross-section: one LADOT sensor-equipped metered parking space.** The raw file contains millions of timestamped sensor transactions, but Notebook 01 aggregates retained durations into one August 2025 occupancy measure per space. The regression dataset is cross-sectional, not an event-level dataset or panel.

The resulting sample represents retained sensor-equipped metered spaces, not all street parking or all neighborhoods in Los Angeles.

## 4. Dependent variable — COMPLETED

[`01_clean_occupancy.ipynb`](notebooks/01_clean_occupancy.ipynb) constructs **`occupancy_rate`**, August 2025 time-weighted occupancy during retained valid observation time:

```text
occupancy_rate = occupied valid minutes / total valid minutes
```

Transactions are unevenly spaced. Counting the percentage of transaction rows marked OCCUPIED would weight short and long intervals equally and would not measure the fraction of time occupied.

### Implemented construction

1. Load `data/raw/ladot_occupancy/20261017T052111914317Z/Sensor Transactions_2025_08.csv`: **3,707,820 transactions**, **4,905 SpaceIDs**, and four fields (`SpaceID`, `EventTime_Local`, `EventTime_UTC`, `OccupancyState`). Raw states are VACANT (1,849,424), OCCUPIED (1,847,148), and UNKNOWN (11,248).
2. Inspect shape, types, missingness, state counts, exact duplicates, timestamp range, event counts, elapsed coverage, active days, and a sample event sequence. These checks do not themselves remove records. The saved outputs show no conventional missing values in the four raw fields and no exact duplicate transaction rows.
3. Parse `EventTime_Local` using `%m/%d/%Y %I:%M:%S %p` and sort by `SpaceID` and local timestamp. Recorded local timestamps run from August 1, 00:00:01 through August 31, 23:59:59. The raw audit found a consistent seven-hour UTC/local difference, matching Los Angeles PDT.
4. Use the next recorded transaction within the same space to calculate the current state's duration in minutes. This assumes the recorded state persists until that next transaction over retained intervals. No duration is assigned after a space's last event, and it is not extended to month-end.
5. Retain intervals with a nonmissing duration, duration **at most 1,440 minutes**, and a starting state other than UNKNOWN. Intervals longer than 24 hours are excluded because they may represent unreliable or unobserved reporting periods; **exactly 24 hours is retained**. UNKNOWN-start intervals are excluded from occupied/vacant duration. The next timestamp is found before filtering, so UNKNOWN records are not skipped to bridge a longer interval.
6. Sum occupied valid minutes and total valid minutes by SpaceID, then take their ratio. The interval rule marks 3,677,140 records valid; 4,901 spaces have an occupancy rate before the active-day restriction.
7. Require **at least 25 distinct active calendar days**. `active_days` is counted from the raw transactions before interval filtering: it is not a count of complete monitoring days or days containing valid intervals.

Both the **24-hour cutoff** and **25-active-day requirement** are researcher-selected rules, not official LADOT definitions.

### Saved result

[`data/processed/space_occupancy_aug2025.csv`](data/processed/space_occupancy_aug2025.csv) contains **4,185 parking-space observations** with `SpaceID`, `occupied_minutes`, `total_minutes`, `occupancy_rate`, and `active_days`.

The saved notebook reports mean occupancy **0.536**, median **0.537**, 25th percentile **0.400**, and 75th percentile **0.679** (rounded). This completed dependent-variable file is an input to Notebook 03; it is distinct from the 4,139-space candidate cross-section and any later model-specific sample. Occupancy refers to retained valid time rather than verified continuous monitoring of all of August.

## 5. Meter inventory variables — COMPLETED, with unresolved validation

[`02_clean_meter_inventory.ipynb`](notebooks/02_clean_meter_inventory.ipynb) prepares the LADOT inventory from `data/raw/ladot_meters/20261017T052111914317Z/inventory.csv`.

The raw inventory has **35,022 rows**, **35,015 unique SpaceIDs**, and seven extra records associated with repeated IDs. The notebook inspects the paired records, confirms identical exported attributes, and removes exact duplicate rows with `drop_duplicates()`. The saved inventory has **35,015 rows and no repeated SpaceIDs**.

Original fields are `SpaceID`, `BlockFace`, `MeterType`, `RateType`, `RateRange`, `MeteredTimeLimit`, and `LatLng`. The notebook inspects their missingness and category distributions before constructing numeric variables. Value-count and summary checks are not additional filters.

### Constructed variables

| Variable | Implemented definition |
|---|---|
| `time_limit_hours` | Explicit mapping from the stated time-limit label to hours |
| `price_midpoint` | Arithmetic mean of the dollar amounts extracted from `RateRange` |
| `latitude`, `longitude` | Numeric components obtained by splitting `LatLng` |

Time-limit examples are `15MIN → 0.25`, `30MIN → 0.5`, `1HR → 1`, and `2HR → 2`. The existing mapping interprets `2HR-30MIN` as **2.5 hours**; this compound-label interpretation has not been independently verified as a parking rule. The remaining mapped hour labels are 4, 6, 7, 10, 13, and 14. `MeteredTimeLimit` is preserved beside the numeric version.

For prices, the notebook extracts numbers immediately following dollar signs, converts them to numeric values, and averages them. For example:

| `RateRange` | `price_midpoint` |
|---|---:|
| `$1.50` | 1.50 |
| `$0.50 - $3.00` | 1.75 |
| `$5.00 - $7.00` | 6.00 |

A single stated amount is reproduced exactly. For **FLAT**, **TOD** (time-of-day), and **JUMP** structures, interpretation differs: a midpoint summarizes the stated amounts, not necessarily a driver's actual payment. In JUMP strings, amounts may refer to hourly and multi-hour charges; averaging them does **not** normalize them to a common hourly rate. `RateRange` and `RateType` are preserved so that information is not lost.

`MeterType` and `RateType` remain categorical; indicator/dummy encoding is **PLANNED/CANDIDATE**, not implemented. Notebook 03 uses coordinates for tract assignment, business counts, and the available zoning linkage; further location controls remain candidates.

### Validation, linkage check, and output

The saved summaries show no missing values in the four constructed numeric variables. **UNRESOLVED:** they also show an impossible latitude below −90 and a positive maximum longitude, suggesting some source coordinate pairs may be reversed. Notebook 02 flags this but does not correct or remove those records. Notebook 03 checks the matched 4,139-space sample and finds no missing coordinates or values outside broad Southern California bounds; no coordinate corrections are applied to that sample. The broader inventory issue remains unresolved outside the retained base sample.

An in-memory left-merge check finds **4,139 matches (98.90%)** and **46 unmatched spaces** among Notebook 01's 4,185 observations. Notebook 02 uses this as a diagnostic without changing its output. Notebook 03 explicitly excludes the 46 unmatched occupancy spaces to establish the 4,139-space base, then preserves that base through all spatial/predictor merges.

[`data/processed/meter_inventory_clean.csv`](data/processed/meter_inventory_clean.csv) contains all **35,015 unique inventory spaces** and ten columns: `SpaceID`, `BlockFace`, `MeterType`, `RateType`, `RateRange`, `MeteredTimeLimit`, `price_midpoint`, `time_limit_hours`, `latitude`, and `longitude`. The temporary `price_numbers` list and original `LatLng` string are not exported. The file is not restricted to occupancy matches.

## 6. Candidate explanatory variables

**COMPLETED** means constructed or retained in the processed outputs of Notebooks 02–03, not selected for a regression or fully validated for August 2025. Notebook 03 now attaches the constructed Census and business measures; candidate status does not mean a variable has been selected for regression.

| Variable | Status | Source | Economic meaning / hypothesis |
|---|---|---|---|
| `price_midpoint` | COMPLETED | LADOT inventory | Price proxy; expected negative conditional association, potentially endogenous |
| `time_limit_hours` | COMPLETED | LADOT inventory | Permitted duration; sign uncertain; compound-label interpretation needs review |
| `MeterType` | COMPLETED | LADOT inventory | Single-space versus multi-space technology/control |
| `RateType` | COMPLETED | LADOT inventory | FLAT/TOD/JUMP pricing structure/control |
| `latitude`, `longitude` | COMPLETED; base sample checked | LADOT inventory | Location and spatial linkage; broader inventory anomalies remain outside the base |
| `GEOID` | COMPLETED geographic identifier | 2024 Census TIGER/Line | Containing Census tract; linkage key rather than a numeric economic predictor |
| `population` | COMPLETED | ACS B01003 | Tract population; local demand context |
| `housing_units` | COMPLETED | ACS B25001 | Tract housing stock; residential demand context |
| `population_density` | COMPLETED | ACS population / Gazetteer ALAND_SQMI | People per square mile of tract land; potentially positive |
| `housing_density` | COMPLETED | ACS housing / Gazetteer ALAND_SQMI | Housing units per square mile of land; potentially positive |
| `median_income` | COMPLETED; 44 missing | ACS B19013 | Socioeconomic control in 2024 dollars; sign ambiguous |
| `drive_alone_share`, `transit_share`, `walk_share` | COMPLETED | ACS B08301 | Resident transportation behavior; denominator includes workers who work from home |
| `nearby_business_count` | COMPLETED | LA business registry | Located registered businesses within 0.25 miles; potentially positive |
| `nearby_restaurant_retail_count` | COMPLETED | Registry / NAICS 722, 44–45 | Located food-service/drinking-place and retail records within 0.25 miles |
| `zoning_code`, `zoning_class`, `zoning_description` | CONSTRUCTED; coverage UNRESOLVED | LA generalized zoning | Source labels only; 49 codes matched, unsuitable as a broadly available control yet |
| Location controls | PLANNED/CANDIDATE | Derived from spatial information | Systematic geographic differences; specification undecided |

Notebook 03 also retains the source commuting counts (`commuters`, `drive_alone`, `public_transit`, `walked`) and `ALAND_SQMI` as traceable components. Neither the counts nor the density/share alternatives have been selected for a model. Location controls beyond the coordinates remain planned.

### ACS definitions used in Notebook 03

The source is **2024 ACS five-year estimates (2020–2024)**. These are the compact estimate codes actually read from the Census Reporter JSON; for example, `B01003001` corresponds to direct Census API code `B01003_001E`.

| Retained field | ACS table / JSON estimate code | Definition |
|---|---|---|
| `population` | B01003 / `B01003001` | Tract population |
| `median_income` | B19013 / `B19013001` | Median household income in 2024 inflation-adjusted dollars |
| `housing_units` | B25001 / `B25001001` | Tract housing units |
| `commuters` | B08301 / `B08301001` | Total workers age 16+, including workers at home; project variable name retained |
| `drive_alone` | B08301 / `B08301003` | Workers driving alone |
| `public_transit` | B08301 / `B08301010` | Workers using public transportation |
| `walked` | B08301 / `B08301019` | Workers walking to work |
| `drive_alone_share` | `drive_alone / commuters` | Share of all source-table workers driving alone |
| `transit_share` | `public_transit / commuters` | Share using public transportation |
| `walk_share` | `walked / commuters` | Share walking to work |

Zero worker denominators remain missing, not zero. These characterize tract residents rather than workplace employment or parking users specifically.

```text
population_density = population / ALAND_SQMI
housing_density    = housing_units / ALAND_SQMI
```

`ALAND_SQMI` is tract land area in square miles from the 2024 Gazetteer. All 2,498 ACS tracts match an area record; three have nonpositive land area and retain missing densities, giving 2,495 nonmissing tract densities. No retained parking spaces lie in those three tracts, so both density columns are complete in the parking cross-section.

### Notebook 03 construction and missingness — COMPLETED

[`03_build_cross_section.ipynb`](notebooks/03_build_cross_section.ipynb) saves [`data/processed/parking_cross_section.csv`](data/processed/parking_cross_section.csv): **4,139 rows, 36 columns, 4,139 unique SpaceIDs, no duplicates**. The 46 inventory-unmatched occupancy spaces are excluded explicitly; no additional parking spaces are removed for missing predictors.

- **Census:** load 9,129 California TIGER/Line tracts and retain 2,498 LA County tracts (`STATEFP="06"`, `COUNTYFP="037"`). WGS84 meter points (EPSG:4326) are matched with `within` to tract polygons reprojected from NAD83 (EPSG:4269). All **4,139** spaces receive a tract and ACS record (**100%**, zero unmatched); no centroid/nearest fallback or multiple assignments occur. A geographically unmatched space would remain in the base with missing geographic predictors, rather than be silently dropped.
- **ACS:** population (B01003), housing units (B25001), median income (B19013), and commuting counts (B08301). Shares divide mode counts by B08301 total workers age 16+, including home workers; zero totals remain missing. All 2,498 ACS tracts match Gazetteer area. Density is count / `ALAND_SQMI`; three nonpositive-area tracts remain missing, giving 2,495 tract densities. None of the retained spaces falls in those three tracts.
- **Businesses:** 632,799 raw records; no exact duplicates or repeated location-account IDs. There are 66,505 missing LOCATION values and 57,281 missing NAICS values. Basic parsing/coordinate checks leave **559,615 usable located records** (73,184 excluded from spatial counting). Two counts use a fixed **0.25-mile / 402.336-metre** buffer in **EPSG:26911 (NAD83 / UTM 11N)**. The subset uses NAICS prefixes 722 and 44–45, so it includes food services/drinking places beyond restaurants alone. Different accounts at the same address are not collapsed. Both `nearby_business_count` and `nearby_restaurant_retail_count` are present for all **4,139 spaces (100%)**. A meter with no eligible located records receives zero, not missing; a zero would not prove there are no real businesses. No zero business counts occur in this saved sample. No radius was optimized using outcomes or model performance.
- **Zoning:** strict point-in-polygon matching only; preserve source `ZONE_CMPLT`, `ZONE_CLASS`, and `ZONING_DESCRIPTION` as `zoning_code`, `zoning_class`, and `zoning_description`. No invented broad categories or nearest-parcel assignments. Only **49 spaces (1.18%)** receive a source code; **4,090** do not. No multiple parking matches or conflicting labels occur. The implemented overlap rule collapses identical label combinations but leaves conflicting combinations missing with an ambiguous flag, rather than taking the first polygon. Blank labels are represented as missing; all unmatched or ambiguous spaces stay in the dataset. The street/parcel coverage mismatch remains unresolved, so these are incomplete candidates, not ready general zoning controls.

**Source availability caveat:** four original zoning JSON pages were unreadable iCloud placeholders. Two were restored with hashes identical to the original acquisition. Two differing current official responses were preserved separately in `data/raw/land_use/supplement_20261022/`; originals were not overwritten. The mixed 28 pages contain 58,956 features. Four IDs outside the original acquisition coverage are omitted from the working layer, leaving 58,952 records and all 58,855 original distinct IDs; 40 IDs have changed duplicate multiplicities. There are zero exact duplicate features, and the 97 repeated IDs are retained because they describe distinct features. Fifteen empty polygon areas cannot be spatially matched, leaving 58,937 nonempty features. These supplements do not recreate an identical historical zoning snapshot.

| Candidate missingness in saved cross-section | Missing | Percent |
|---|---:|---:|
| `median_income` | 44 | 1.06% |
| `zoning_code` | 4,090 | 98.82% |
| `zoning_class` | 4,119 | 99.52% |
| `zoning_description` | 4,091 | 98.84% |
| Other 15 fields in Notebook 03's candidate-variable check | 0 each | 0.00% |

No missing ACS estimates are imputed and no complete-case sample is imposed. Business counts describe a later registry with incomplete geocoding, not August 2025 counts of distinct operating destinations. Neighborhood/price coefficients remain associations, with vintage and endogeneity concerns. The [Notebook 03 completion report](docs/notebook03_completion_report.md) records definitions, validation ranges, provenance, and remaining limitations.

## 7. Data sources collected

The initial acquisition retained **56 original files**, including metadata, zoning pages, source documentation, and two transit-feed versions (approximately **818.5 MB**). On October 21, 2026, the official **2024 Census TIGER/Line California tract boundary archive** was added, along with its unchanged extracted shapefile components. Exact URLs, filenames, retrieval/update dates, licenses, and checksums are in [data_sources.md](docs/data_sources.md) and the [retrieval manifests](docs/retrievals/); [acquisition_audit.json](docs/acquisition_audit.json) records the initial acquisition only.

### Core regression inputs

| Source | Coverage / vintage | Current use or outstanding limitation |
|---|---|---|
| LADOT historical occupancy | August 2025 local-calendar attachment | Completed outcome construction |
| LADOT meter inventory | October 2026 snapshot | Initial predictors completed; prices/rules may differ from August 2025 |
| LA generalized zoning | Layer retrieved October 2026; effective vintage unverified | Point-in-polygon attempted; only 49 source-code matches. Two separately documented supplemental pages were needed; repeated IDs are distinct features |
| ACS via Census Reporter | 2024 five-year release, covering 2020–2024; LA County tract query | Population, housing, income and commuting candidates attached to all 4,139 spaces; income missing for 44 |
| Census tract Gazetteer | California, 2024 | IDs, land areas, internal points; **not tract boundary polygons** |
| Census TIGER/Line tract boundaries | California, **2024 vintage**; acquired October 21, 2026 | Official polygon shapefile collected for point-in-polygon matching of LADOT coordinates to actual Census tracts; all 4,139 base spaces assigned by containing polygon |
| LA active-business registry | October 2026 snapshot | Quarter-mile all-business and food-service/retail counts constructed; historical operation and geocoding limitations remain |

The official [U.S. Census Bureau TIGER/Line archive](https://www2.census.gov/geo/tiger/TIGER2024/TRACT/tl_2024_06_tract.zip) is preserved at `data/raw/census/tigerline_2024_california_tracts/tl_2024_06_tract.zip`. Its unmodified shapefile is [tl_2024_06_tract.shp](data/raw/census/tigerline_2024_california_tracts/tl_2024_06_tract.shp), with all companion files in the same directory. The archive is 32,451,946 bytes and contains 9,129 tract records; the source CRS is NAD83, as recorded in its `.prj`. Notebook 03 now filters these polygons in memory to Los Angeles County and assigns meter points by containing polygon using `GEOID`. Source shapefile components, the existing ACS JSON, and Gazetteer file are unchanged.

Census tract internal points cannot establish which tract contains a parking space; the newly collected polygons provide that missing input. Tract matching and attaching ACS estimates are now completed in Notebook 03; further neighborhood-feature choices belong to later analysis. Current zoning is a designation, and the business registry is not a complete August 2025 census of operating destinations.

### Data vintages used in the cross-section

| Data | Date / vintage actually used | Mismatch to flag |
|---|---|---|
| Parking occupancy | August 2025, Los Angeles local-calendar month | Reference period for Y |
| LADOT meter inventory | October 2026 snapshot, processed in Notebook 02 | Prices, time limits, and equipment may differ from August 2025 |
| ACS | 2024 five-year release, estimating 2020–2024 | A multiyear neighborhood proxy, not an August 2025 measurement |
| Census geography | 2024 TIGER/Line polygons and 2024 Gazetteer areas | Geographic vintage predates the occupancy month |
| LA active-business registry | October 2026 snapshot | Potential business openings/closures after the outcome month; counts are not historical August 2025 activity |
| LA zoning | Original October 16, 2026 retrieval plus two October 21 Pacific / October 22 UTC supplemental pages | Mixed retrieval dates; effective zoning dates unverified |

These mismatches are retained and disclosed, not assumed away. Later analysis should not interpret the cross-section as a causal estimate of price or perfectly contemporaneous neighborhood effects.

### Optional or extension sources

| Source | Coverage / caveat |
|---|---|
| Current LADOT occupancy | October 2026 last-known-state snapshot; not the August outcome |
| Street sweeping | Legacy 2014 table with textual route boundaries |
| Preferential parking districts | Legacy 2015 layer |
| Calendar sign locations | Legacy 2019 installation information, not complete sign rules |
| Dodgers schedule | August 2025 games, including away games |
| UCLA calendar | Academic/administrative calendar, not a comprehensive event archive |
| NOAA weather | LAX observations through Aug. 27, 2025; downtown daily-summary reports through Aug. 25 |
| Metro rail GTFS | October 2026 service plus a stale October 2022 archive retained for provenance; neither is August 2025 service |

These sources are not all intended for the primary regression. Monthly aggregation also limits the role of weather/calendar variables common to every space's observation window. Public access does not establish unrestricted redistribution rights for every optional source; consult the source catalog.

## 8. Assumptions and methodological decisions

| Decision / assumption | Reason | Potential limitation |
|---|---|---|
| State persistence | Assign the current state until the next transaction within a space | Saved LADOT documentation does not guarantee perfect continuous reporting |
| Exclude UNKNOWN-start intervals | Cannot classify occupied/vacant duration | Unknown time may be systematically different from retained time |
| Maximum interval of 24 hours | Avoid assuming extremely long reporting gaps are known continuous states | Researcher-selected cutoff; a long gap can also reflect a stable state |
| At least 25 raw active days | Seek coverage across most of August | Researcher-selected restriction; event days do not prove continuous observation |
| Do not extend the final event | No subsequent transaction supplies an interval endpoint | Month-boundary coverage differs across spaces |
| Use `price_midpoint` | Simple numeric summary of stated amounts | Simplifies TOD/JUMP schedules and can mix amounts covering different durations |
| Interpret `2HR-30MIN` as 2.5 hours | Existing explicit time-limit mapping | Compound-label meaning remains unverified; original label retained |
| Cross-sectional associations | Compare monthly outcomes across spaces | Not automatically causal effects |
| Price may respond to demand | High-demand locations may receive higher tariffs | Price coefficient lacks a causal interpretation without stronger identification |
| Sensor selection/reporting | Use available sensor-equipped spaces and retained intervals | May not represent all LA parking; audit found systematic Sunday reporting differences |
| Spatial dependence | Nearby spaces share destinations and demand conditions | Correlated errors can challenge conventional OLS inference |
| Bounded outcome | OLS is the planned ECON 430 framework for a fraction in [0, 1] | Out-of-range fitted values and heteroskedasticity are possible |
| Mixed data vintages | Use available meter/neighborhood/activity sources | Measurement error; dates must be documented as variables are added |
| Strict containing-polygon matching | Use actual tract/zoning boundaries | No nearest fallback; zoning covers only 49 parking points |
| Quarter-mile business radius | Fixed local walking-distance proxy in metre-based CRS | Researcher-selected; registry locations/classifications are incomplete |
| Count registry accounts | Distinct registered locations, including co-located accounts | Not necessarily distinct physical destinations or historically operating firms |
| Preserve Census missingness | Leave the 44 missing incomes unimputed; use missing shares/densities when denominators are nonpositive | No complete-case sample has been selected |
| Retain geographically unmatched spaces | Keep the base after tract/ACS/zoning left joins; missing assignments remain explicit | Actual tract/ACS unmatched count is zero; zoning has 4,090 unmatched |
| ACS worker denominator and land-area units | Shares use total workers including home workers; densities use square miles of land | Resident proxies and rounded Gazetteer areas, not direct local parking demand |
| Food-service/retail subset | Use transparent NAICS prefixes 722 and 44–45 | Broader than restaurants alone; unclassified records cannot enter the subset |
| Original zoning labels and overlap handling | Preserve source code/class/description; conflicting assignments would stay missing | No broad-category interpretation or nearest-parcel fallback |
| Preserve missing predictors | Allow later transparent missingness decisions | Model-specific sample size remains undecided |
| Zoning source recovery and geometry | Two separately saved current pages; original ID coverage, no exact-feature duplicates, 15 empty areas omitted | Mixed vintage and incomplete point coverage; no broad category inferred |

These are implemented assumptions or identified concerns, not completed robustness findings. The raw audit's **YELLOW** outcome-validity assessment remains relevant: the current cleaning rules operationalize a measure, but do not establish flawless sensor reporting.

## 9. Current sample and data flow

```text
3,707,820 raw occupancy transactions → 4,905 raw sensor SpaceIDs
→ valid time-weighted occupancy → ≥25 raw active days → 4,185 spaces
→ meter matches: 4,139 / 4,185 (98.90%); exclude 46 unmatched
→ 4,139 base spaces
→ containing Census tract and ACS record: 4,139 / 4,139 (100%)
→ quarter-mile business and food-service/retail counts: 4,139 / 4,139 (100%)
→ zoning source code: 49 assigned (1.18%); 4,090 unmatched retained
→ saved cross-section: 4,139 rows × 36 columns                   [COMPLETED]
  4,139 unique SpaceIDs; 0 duplicate SpaceIDs
→ EDA → variable selection → OLS → diagnostics → results        [PLANNED]
```

### Current regression dataset

- **Dependent variable:** `occupancy_rate`, August 2025 time-weighted occupancy.
- **Unit / N:** one retained LADOT parking space; **4,139 rows, 4,139 unique SpaceIDs, zero duplicates**.
- **Shape:** 36 columns, including **19 named candidate fields** in Notebook 03's validation list: 16 non-zoning candidates and three sparse source zoning fields. Categorical encoding and final predictor selection have **not** happened.
- **Saved output:** [`data/processed/parking_cross_section.csv`](data/processed/parking_cross_section.csv).
- **Support:** original duration totals, active days, rate/time-limit labels, Census components, and match-status fields remain available for traceability.

This is the completed Notebook 03 construction output. A later regression's estimation sample may differ because predictor selection and missing-data decisions remain open; the notebook does not impose a complete-case sample.

## 10. Notebook workflow

Run notebooks in numerical order. Relative data paths assume a notebook working directory of `notebooks/`. Notebooks 01–03 have executed code and saved validation outputs. Notebooks 04–08 remain shells with no analysis code.

| Notebook | Status | Purpose / planned course methods |
|---|---|---|
| [01 Clean Occupancy](notebooks/01_clean_occupancy.ipynb) | COMPLETED | Construct and clean the dependent variable |
| [02 Clean Meter Inventory](notebooks/02_clean_meter_inventory.ipynb) | COMPLETED; coordinate issue UNRESOLVED | Prepare meter characteristics and initial predictors; check occupancy linkage |
| [03 Build Cross-Section](notebooks/03_build_cross_section.ipynb) | COMPLETED; zoning coverage unresolved | Combine Y/meters; assign tracts; attach ACS counts, densities and shares; construct business counts and partial zoning labels; validate one row per SpaceID; save `parking_cross_section.csv` |
| [04 EDA](notebooks/04_eda.ipynb) | PLANNED | Descriptive statistics, distributions, correlations, scatterplots, missingness, and consideration of transformations/outliers |
| [05 Variable Selection](notebooks/05_variable_selection.ipynb) | PLANNED | ECON 430 tools including Boruta, Mallows Cp, and VIF |
| [06 Regression Models](notebooks/06_regression_models.ipynb) | PLANNED | Simple OLS, a 2–3 predictor model, and a broader supported model; compare adjusted R², AIC/BIC, and cross-validation |
| [07 Diagnostics](notebooks/07_diagnostics.ipynb) | PLANNED | Residual plots, RESET, Breusch–Pagan, White, QQ/Jarque–Bera, Cook's distance, leverage, DFBETAS, bootstrap, and cross-validation |
| [08 Results](notebooks/08_results.ipynb) | PLANNED | Regression tables, confidence intervals, coefficient/economic interpretation, statistical versus economic significance, and report outputs |

Prioritize methods taught in ECON 430 and explicitly required by the assignment. The listed later-stage tools are a plan, not implemented analyses; unnecessary advanced methods should not expand the scope.

## 11. Current project status

- [x] Raw data acquisition and source documentation.
- [x] Acquire official 2024 TIGER/Line polygons and assign all 4,139 base spaces to LA County tracts.
- [x] Read-only raw-data design-validation audit.
- [x] Occupancy cleaning and dependent-variable construction: 4,185 spaces.
- [x] Meter-inventory preparation and initial predictors: 35,015 spaces; coordinate validity remains unresolved.
- [x] Build and save the Notebook 03 candidate cross-section: 4,139 spaces, 36 columns.
- [x] Validate the saved cross-section: 4,139 unique SpaceIDs and zero duplicates.
- [x] Validate coordinates in the retained 4,139-space base; broader inventory anomalies remain outside that base.
- [ ] Resolve remaining variable-interpretation and weak zoning-coverage issues.
- [x] Add Census/neighborhood candidates and establish tract linkage; preserve 44 missing incomes.
- [x] Add fixed quarter-mile business and food-service/retail counts.
- [x] Implement zoning matching and preserve original source labels; 49 code assignments, no arbitrary fallback.
- [ ] Resolve broad zoning/land-use coverage; 4,090 spaces remain unmatched.
- [ ] EDA on the final analysis dataset.
- [ ] Variable selection.
- [ ] OLS model estimation and comparison.
- [ ] Diagnostics, robustness, and out-of-sample validation.
- [ ] Final interpretation, tables, and figures.
- [ ] Final ECON 430 report.

Early distribution and missingness checks in the cleaning notebooks do not mean Notebook 04's EDA is complete. `docs/cleaning_decisions.md` remains a headings-only template; implemented choices are currently documented in the notebooks and this README. No final report figures or tables have been generated.

## 12. Reproducibility and repository notes

```text
notebooks/              Student-written cleaning and econometric workflow
data/raw/              Original source files and provider metadata; do not edit
data/interim/          Intermediate outputs; currently empty
data/processed/        Notebook-generated outputs; three CSVs, including the Notebook 03 candidate cross-section
src/data_collection/   Existing download and acquisition-audit scripts
src/{cleaning,features,modeling}/  Placeholder directories with .gitkeep files
reports/{figures,tables}/         Final report outputs; currently empty
docs/                  Sources, retrieval records, raw audit, and decisions template
```

Notebooks, code, and documentation are tracked in Git. Raw data are intentionally excluded from GitHub because of their size; the current `.gitignore` excludes the entire `data/` directory, including processed files. A clone therefore needs the original source files restored at the documented paths before the notebooks can run. The three processed CSVs are regenerated by Notebooks 01, 02, and 03. Read `SpaceID` and Census `GEOID` as strings when loading them so identifiers retain leading zeros. Notebook 03 also needs the separately documented supplemental zoning pages, not fresh live replacements for its fixed source files.

From the project root, a local environment can use:

```bash
python3 -m pip install -r requirements.txt
python3 -m jupyterlab
```

To reproduce the dataset from its inputs, run Notebooks 01–03 in numerical order, with the kernel working directory set to `notebooks/`. **For new analysis, start Notebook 04 from `../data/processed/parking_cross_section.csv`; do not rebuild the merges there.** Read `SpaceID` and `GEOID` as strings. Notebook 03 is the authoritative construction pipeline for this saved cross-section. Keep the named source files and retrieval directories consistent with the notebook paths. Dependencies for some planned course tools, including Boruta, are not yet declared; address them when those stages are implemented. No random procedures have been implemented; later random procedures should use explicit seeds consistent with the assignment's reproducibility requirement.

Acquisition scripts can obtain new snapshots, but they are not prerequisites for continuing with the existing sources. `collect.py --month 2025_08` uses a rolling LADOT archive, full exports, and separate retrieval directories. The original month may eventually disappear, and current inventory/business snapshots change. Preserve original files and manifests rather than silently replacing them with a new vintage. Direct Census API and Ticketmaster expansion require personal keys; collected data used public endpoints including Census Reporter.

The source catalog and raw dictionary preserve acquisition-era context, not an up-to-date account of all cleaning. In particular, the dictionary omits `EventTime_Local` from the historical archive fields even though it is present in the CSV, and the catalog's description of all events as state changes is stronger than the saved documentation supports. The audit and the explicit persistence assumption above qualify that interpretation. Methodological changes should be recorded in this README and the relevant notebook or decision log.

## 13. Guidance for future work

**Handoff:** Notebook 03 is now the authoritative data-construction pipeline. Continue in Notebook 04 using the saved `data/processed/parking_cross_section.csv`. Do not silently reconstruct Y, change the 24-hour or 25-day rules, alter the quarter-mile business radius, switch geographic matching, or redefine variables. Document any intentional change and its effect on the sample in the relevant notebook and this README.

- Preserve the one-row-per-parking-space cross-sectional design unless the research question is intentionally changed.
- Preserve time-weighted occupancy; do not substitute the percentage of OCCUPIED transaction rows.
- Do not silently change the 24-hour or 25-day thresholds. Document alternatives as robustness checks and explain any change to the main specification.
- Treat `price_midpoint` as a proxy, not an exact transaction price or universally comparable hourly tariff.
- Distinguish associations from causal effects, especially for price.
- Preserve the validated base coordinates and inspect any expanded sample separately; the broader inventory anomalies are not evidence that all inventory coordinates are reliable.
- Keep planned and candidate variables distinct from completed variables. Preserve the 4,139-space Notebook 03 base unless a documented later sample decision changes it; distinguish that dataset from a model-specific estimation sample.
- Follow ECON 430 methods and assignment requirements rather than adding unrelated techniques.
- Update this README whenever a major dataset, variable, cleaning rule, sample restriction, or modeling decision changes.
