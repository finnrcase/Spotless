# Design-Validation Audit of RAW Data

**Overall assessment: YELLOW — workable with material caveats.**

This document preserves the read-only design-validation audit reported in the project conversation on October 16, 2026 (Pacific time). It is an audit of **raw source data, not analytical results**. It does not establish cleaning decisions, select a final sample, calculate occupancy rates, or estimate a model. The proposed future design is one sensor-equipped LADOT metered parking space per cross-sectional observation, with an August 2025 duration-based occupancy outcome.

The validation calculations were temporary and in memory. No cleaned, merged, transformed, or processed dataset was saved. This document was written during subsequent workspace organization from the completed audit findings; the validation was not rerun during that setup.

## Sources and scope

Paths are relative to the project root:

- Historical occupancy: `data/raw/ladot_occupancy/20261017T052111914317Z/Sensor Transactions_2025_08.csv`.
- Meter inventory: `data/raw/ladot_meters/20261017T052111914317Z/inventory.csv`.
- Saved archive/current occupancy metadata, inventory metadata, and the other sources described in [data_sources.md](data_sources.md).

The historical CSV has four actual columns: `SpaceID`, `EventTime_Local`, `EventTime_UTC`, and `OccupancyState`. The existing raw dictionary follows the archive portal's three metadata fields and omits `EventTime_Local`; the CSV and acquisition audit retain all four. This documentation discrepancy does not indicate a change to the raw file.

## Historical SpaceID matching

Exact raw ID strings were compared without normalization. No merged dataset was created.

| Measure | Count |
|---|---:|
| Historical occupancy events | 3,707,820 |
| Historical distinct SpaceIDs | **4,905** |
| Inventory rows | 35,022 |
| Inventory distinct SpaceIDs | 35,015 |
| Matched historical IDs | **4,849** |
| Unmatched historical IDs | **56** |
| Inventory IDs absent from historical occupancy | 30,166 |
| Historical ID match rate | **98.86%** |

Seven inventory IDs each appear twice; their paired rows are identical across the exported fields. Four duplicated IDs match historical occupancy: `CT258`, `CT256`, `CT252`, and `CT257`. The other three are `CT259`, `CT253`, and `CT254`. No duplicates were removed.

Among the 4,849 matched IDs, missingness is **0.00%** for `LatLng`, `RateRange`, `MeteredTimeLimit`, `MeterType`, and `RateType`. Basic checks found finite, nonzero coordinates within valid latitude/longitude bounds, dollar-denominated tariff strings, hour/minute time-limit representations, and recognized meter-type categories. These checks do not establish spatial accuracy, historical accuracy, or analysis-ready numerical variables.

| Raw category | Matched spaces |
|---|---:|
| RateType: TOD | 3,829 |
| RateType: FLAT | 921 |
| RateType: JUMP | 99 |
| MeterType: Single-Space | 4,674 |
| MeterType: Multi-Space | 175 |

**78.96% of matched spaces have time-of-day tariffs.** A current rate range does not supply the complete hourly tariff schedule or establish the price charged in August 2025.

## Sensor state quality

| Unique raw state | Records | Share of records |
|---|---:|---:|
| VACANT | 1,849,424 | 49.8790% |
| OCCUPIED | 1,847,148 | 49.8176% |
| UNKNOWN | 11,248 | 0.3034% |
| Other values | 0 | 0.0000% |

**908 spaces (18.51%)** have at least one UNKNOWN observation. Shares of event records are not shares of observed time.

| Check | Result |
|---|---:|
| Duplicate same-space timestamp groups | 0 |
| Spaces with duplicate timestamps | 0 |
| Conflicting states at the same timestamp | 0 |
| Backward timestamp steps within a space in original file order | 0 |
| Consecutive identical-state pairs | **6,653** |
| Spaces with consecutive identical states | 2,346 |
| VACANT followed by VACANT | 5,296 |
| OCCUPIED followed by OCCUPIED | 1,357 |
| UNKNOWN followed by UNKNOWN | 0 |

Identical-state pairs have distinct timestamps. They account for 0.1797% of 3,702,915 adjacent within-space pairs and occur in 47.83% of spaces. Sample sequences also contain transitions only seconds apart; sensor behavior versus real short stops remains unresolved. No records were removed or repaired.

## Duration interpretation: B — strongly suggested, not explicitly documented

The saved archive metadata describes sensor activity. The current-feed metadata describes last-known occupancy state and an occupancy transaction timestamp. Mostly alternating state sequences support an event/state interpretation.

However, the saved material does not explicitly guarantee that each row exclusively represents a state change, that a reported state remains valid until the next transaction, or that every transition is captured. It does not establish off-hours reporting, outage/reset behavior, or missing-transmission conventions. Consecutive identical states show that not every row necessarily changes state. Earlier acquisition wording describing all records as state changes was too strong.

If state persistence and observation validity are established, a future duration-based outcome could use occupied intervals divided by valid occupied-plus-vacant intervals. No such intervals or outcome were constructed. The first-to-last span is not automatically all valid time. Extending a first or last state to the month boundary also requires justification. UNKNOWN, gaps, and differing observation windows need explicit future methodological decisions.

## Sensor coverage diagnostics

These are raw-data validation summaries, not final variables or sample restrictions. An event day is a local calendar day with at least one event, not proof of continuous monitoring. Percentiles use linear interpolation at position `(n - 1) × p` in sorted audit values.

| Per-space measure | Minimum | 25th percentile | Median | 75th percentile | Maximum |
|---|---:|---:|---:|---:|---:|
| Events | 1 | 389 | **589** | 878 | 8,517 |
| Distinct local event days | 1 | 26 | **26** | 31 | 31 |
| First-to-last span, days | 0.00 | 29.38 | **29.69** | 30.58 | 31.00 |
| Longest inter-event gap, hours | 0.0064 | 24.14 | **38.73** | 45.62 | 543.18 |

Gap summaries cover 4,903 spaces with at least two events. The two single-event spaces have no inter-event gap.

| Statistic | First local event | Last local event |
|---|---|---|
| Earliest | Aug. 1, 00:00:01 | Aug. 25, 00:00:09 |
| 25th percentile | Aug. 1, 00:00:55 | Aug. 30, 16:28:37 |
| Median | Aug. 1, 04:03:01 | Aug. 30, 18:00:27 |
| 75th percentile | Aug. 1, 08:18:39 | Aug. 31, 17:57:55 |
| Latest | Aug. 30, 17:44:09 | Aug. 31, 23:59:59 |

| Illustrative coverage descriptor | Spaces |
|---|---:|
| Events on all 31 days | 1,351 |
| Events on at least 28 days | 1,683 |
| Events on at least 25 days | 4,185 |
| First event Aug. 1 and last event Aug. 31 | 1,773 |
| First-to-last span at least 30 days | 1,750 |
| Events on seven or fewer days | 53 |
| Ten or fewer events | 20 |
| One event | 2 |
| First-to-last span under seven days | 15 |
| Longest gap at least 24 hours | 3,686 |
| Longest gap at least 72 hours | 517 |

These descriptors overlap and are **not exclusion thresholds**. Long gaps may represent stable states, suspended reporting, or lost observations; timestamps alone do not distinguish these cases.

Among inventory-matched spaces, 1,316 have events on all 31 days, 1,643 on at least 28 days, and 4,139 on at least 25 days. These are not selected samples.

## Sunday / reporting pattern

| Sunday in August 2025 | Spaces with events |
|---|---:|
| August 3 | 1,831 |
| August 10 | 1,853 |
| August 17 | 1,778 |
| August 24 | 1,738 |
| August 31 | 1,821 |

Other days have approximately 4,589–4,758 spaces with events. This recurring pattern suggests a reporting/operating issue to resolve; it does not establish that absent spaces were vacant, offline, or unobserved. The audit did not decide how Sundays should enter a future outcome.

## August local / UTC boundary verification

| Check | Finding |
|---|---|
| First recorded local timestamp | `8/1/2025 12:00:01 AM` |
| Last recorded local timestamp | `8/31/2025 11:59:59 PM` |
| First corresponding UTC timestamp | `8/1/2025 7:00:01 AM` |
| Last corresponding UTC timestamp | `9/1/2025 6:59:59 AM` |
| UTC minus local | Exactly seven hours in all 3,707,820 records |
| Records outside August by local timestamp | 0 |

The relationship agrees with Los Angeles PDT (UTC−7) throughout August; there is no daylight saving transition within the month. The attachment follows local-calendar August boundaries. It does not independently establish each space's state at the exact beginning of the month or continuous observation for all 31 days. Raw timestamp strings were not rewritten or timezone-converted.

## Potential predictor coverage

Ratings assess plausible raw inputs, not completed predictors. No spatial, demographic, business, permit, or transit joins were performed.

| Candidate | Rating | Caveat |
|---|---|---|
| Meter price/rate | USABLE WITH CAVEATS | Mostly TOD ranges; historical prices and complete schedules absent |
| Metered time limit | USABLE WITH CAVEATS | Complete field, but compound limits and later vintage |
| Meter type | STRONG | Recognized categories with variation; historical stability assumed |
| Latitude/longitude | STRONG | Complete plausible matched coordinates; accuracy unverified |
| Zoning | USABLE WITH CAVEATS | Current designation, source duplicate IDs, spatial assignment unresolved |
| Population | USABLE WITH CAVEATS | ACS estimates available; space-to-tract assignment absent |
| Housing units | USABLE WITH CAVEATS | Same geography and vintage concerns |
| Median household income | USABLE WITH CAVEATS | Estimates/MOEs present; tract linkage and estimate codes need review |
| Commute characteristics | USABLE WITH CAVEATS | Resident commuting, not local workplace employment |
| Land area for density | USABLE WITH CAVEATS | Gazetteer tract area present; compatible linkage not built |
| Nearby businesses | USABLE WITH CAVEATS | 2026 registry; historic operation and coordinate completeness unresolved |
| Nearby restaurants via NAICS | USABLE WITH CAVEATS | Classification, historical presence, and proximity unresolved |
| Nearby retail via NAICS | USABLE WITH CAVEATS | Same registry/classification caveats |
| Distance to UCLA | NOT CURRENTLY USABLE | No defined campus reference point/boundary or distance measure |
| Permit district | WEAK | Legacy 2015 layer; applicability unverified |
| Street sweeping | WEAK | Legacy textual boundaries; no direct space key or explicit weekday field |
| Transit proximity | USABLE WITH CAVEATS | Stop coordinates exist; neither collected service schedule matches August 2025 |

ACS tables collected are population, housing units, median household income, and transportation to work. Gazetteer internal points are not tract polygons; a tract assignment source remains missing. Zoning is a legal designation, not verified observed land use. Business registrations are not necessarily distinct operating destinations. No nearby-business counts, densities, distances, or other spatial features exist yet.

## Historical-vintage concerns

These are qualitative risk judgments, not comparisons with historical versions.

| Source | Risk | Reason |
|---|---|---|
| October 2026 inventory overall | HIGH VINTAGE RISK | Prices/rules may differ from August 2025 |
| Inventory coordinates / meter type | LOW VINTAGE RISK | Plausibly stable for persistent IDs, but changes possible |
| Inventory time limits | MODERATE VINTAGE RISK | Potential rule changes; no effective dates |
| October 2026 business registry | HIGH VINTAGE RISK | Openings, closures, relocation and future-business leakage |
| 2024 ACS five-year estimates | MODERATE VINTAGE RISK | Pre-outcome neighborhood proxy averaging 2020–2024 |
| Current zoning | MODERATE VINTAGE RISK | Potential rezoning; effective dates unchecked |
| Legacy permit districts | HIGH VINTAGE RISK | Approximately ten-year gap |
| Legacy sweeping / sign files | HIGH VINTAGE RISK | Old tables; sign locations do not establish restrictions |
| Metro schedules | HIGH VINTAGE RISK | Neither 2022 nor 2026 service represents August 2025 |

Coordinates and broad neighborhood characteristics are more plausibly stable than prices, rules, businesses, or service schedules. Historical equivalence has not been verified. No vintage mismatch was fixed.

## Cross-sectional / OLS considerations

One row per space with one August summary outcome would be cross-sectional, even though many raw events underlie each outcome. Repeated event rows are not independent cross-sectional observations. Comparable observation windows and a defensible duration interpretation are prerequisites.

OLS is conceptually possible for a continuous occupancy fraction, but its 0–1 bounds can lead to out-of-range predictions and heteroskedasticity. Unequal valid observation durations can imply unequal outcome precision. A single OCCUPIED/VACANT reading would instead be a binary outcome. No outcome, model, diagnostics, or validation split has been created.

Issues for later design and interpretation include demand-responsive price endogeneity, omitted neighborhood factors, spatial dependence among nearby spaces, common block/destination conditions, selection into sensor-equipped metered parking, outcome and predictor measurement error, unequal observation windows, and correlated predictors. Calendar/weather variables common to all spaces offer little cross-space variation in a shared observation window. Many issues belong in inference, limitations, and robustness work, but unresolved outcome validity cannot be handled solely with a limitations paragraph.

## Feasibility and unresolved questions

| Question | Assessment |
|---|---|
| Raw backbone sufficient? | YELLOW — strong ID/sample-size backbone, conditional outcome validity |
| More than 500 valid spaces likely? | GREEN — PROBABLY, with substantial numerical headroom |
| Defensible continuous occupancy outcome likely? | YELLOW — plausible, pending semantics and valid-time rules |
| At least five meaningful predictor candidates? | GREEN — yes, pending linkage, vintage, and variation checks |
| Proceed with proposed design? | YELLOW — conditional on resolving material audit questions |

The number of spaces without severe coverage problems is **not established**. Defining that group requires justified validity rules; high event counts or many event days alone do not prove continuous reliable monitoring. No final inclusion/exclusion threshold was chosen.

Top five risks identified:

1. Unverified state persistence and transition capture.
2. Sunday/off-hours patterns and ambiguous long gaps.
3. Current tariff ranges instead of historical time-specific prices.
4. Vintage mismatch in business, zoning, and restriction sources.
5. Spatial dependence, sensor selection, and demand-responsive pricing.

Questions for the student to resolve in future work include state semantics and validity, comparable observation windows, UNKNOWN/gap/repeated-state/boundary treatment, unmatched and duplicated IDs, tariff/time-limit representation, geographic assignment, predictor vintage, and the final valid sample size. These are unresolved questions, **not decisions made by this document**. Record actual decisions separately in [cleaning_decisions.md](cleaning_decisions.md).

## Integrity at completion of the validation audit

All 56 original downloaded files matched their recorded SHA-256 hashes. No raw file changed; no cleaned, merged, processed, or final feature dataset was created; no imputation, modeling, or visualization occurred. `data/interim/` and `data/processed/` remained empty. Temporary calculations were held in memory only.
