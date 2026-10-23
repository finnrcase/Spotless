# NOTEBOOK 03 COMPLETION REPORT

Completed October 21, 2026 (Pacific time). Notebook 03 was a saved two-cell shell at the start; the earlier Census/merge work described in the instructions was not present on disk. The notebook implements those agreed definitions and adds the requested spatial/business/zoning stages. No OLS, EDA notebook, variable selection, hypothesis tests, diagnostics, or model-based transformations were performed.

## 1. Final dataset

- Final rows: **4,139**.
- Final columns: **36**.
- Unique SpaceIDs: **4,139**.
- Duplicate SpaceIDs: **0**.
- Saved path: `data/processed/parking_cross_section.csv`.
- Saved CSV SHA-256: `644615c218966773b367f902dd9e559f081dfe78023374f0fbc9aa6a1dafbb70`.
- Contains one row per retained space and preserves missing candidate predictors; this is not a complete-case estimation sample.

Columns: `SpaceID`, `occupancy_rate`, `occupied_minutes`, `total_minutes`, `active_days`, `BlockFace`, `MeterType`, `RateType`, `RateRange`, `MeteredTimeLimit`, `price_midpoint`, `time_limit_hours`, `latitude`, `longitude`, `GEOID`, `population`, `median_income`, `housing_units`, `commuters`, `drive_alone`, `public_transit`, `walked`, `ALAND_SQMI`, `population_density`, `housing_density`, `drive_alone_share`, `transit_share`, `walk_share`, `nearby_business_count`, `nearby_restaurant_retail_count`, `zoning_code`, `zoning_class`, `zoning_description`, `tract_match_status`, `acs_match_status`, `zoning_match_status`.

## 2. Parking + meter merge

- Occupancy starting N: **4,185**.
- Meter matches: **4,139**.
- Unmatched: **46**.
- Match rate: **98.9008%**.
- Treatment: display unmatched examples, explicitly exclude those 46 from the base because meter covariates/location are unavailable, retain all 4,139 matched spaces through later steps. No source or Notebook 01/02 output was modified.

## 3. Census geographic match

- Boundary source: official U.S. Census Bureau TIGER/Line California tract shapefile, `data/raw/census/tigerline_2024_california_tracts/tl_2024_06_tract.shp`; https://www2.census.gov/geo/tiger/TIGER2024/TRACT/tl_2024_06_tract.zip.
- Vintage: **2024**.
- California tract count: **9,129**.
- LA County tract count: **2,498** (`STATEFP=06`, `COUNTYFP=037`).
- Parking spaces assigned: **4,139**; unmatched **0**; match rate **100%**.
- CRS/method: points treated as WGS84 EPSG:4326, tract polygons reprojected from NAD83 EPSG:4269 to match; GeoPandas `within` point-in-polygon join. No centroid/nearest fallback.
- Multiple assignments/duplicate SpaceIDs: **0**. All 4,139 assigned tracts also match an ACS record.

## 4. ACS variables

2024 ACS five-year release (2020–2024), delivered through Census Reporter. The table lists direct Census-style estimate codes; the JSON uses the corresponding compact codes such as `B01003001` rather than `B01003_001E`. Missing counts below are parking-space rows, not unique tracts.

| Retained variable | ACS source | Definition | Missing |
|---|---|---|---:|
| `population` | B01003_001E | Tract population | 0 |
| `median_income` | B19013_001E | Median household income, 2024 inflation-adjusted dollars | 44 |
| `housing_units` | B25001_001E | Tract housing units | 0 |
| `commuters` | B08301_001E | Total workers age 16+, including those working from home; retained project variable name | 0 |
| `drive_alone` | B08301_003E | Workers driving alone | 0 |
| `public_transit` | B08301_010E | Workers using public transportation | 0 |
| `walked` | B08301_019E | Workers walking to work | 0 |
| `drive_alone_share` | B08301_003E / B08301_001E | Drive-alone workers / total workers | 0 |
| `transit_share` | B08301_010E / B08301_001E | Public-transit workers / total workers | 0 |
| `walk_share` | B08301_019E / B08301_001E | Walking workers / total workers | 0 |
| `population_density` | B01003_001E + Gazetteer | Population / ALAND_SQMI | 0 |
| `housing_density` | B25001_001E + Gazetteer | Housing units / ALAND_SQMI | 0 |

No ACS imputation. Zero total-worker denominators remain missing. At the tract level, 42 income estimates are missing and 25 commuting-share denominators are zero; the final sample has 44 missing incomes and no missing commuting shares. These are resident characteristics, not workplace employment measures.

## 5. Density variables

- Population density: people per **square mile of tract land**, population / `ALAND_SQMI`.
- Housing density: housing units per **square mile of tract land**, housing_units / `ALAND_SQMI`.
- All **2,498** ACS tracts match Gazetteer land area. **3** have nonpositive land area, with no missing areas; densities stay missing for those tracts.
- Both tract densities have **2,495 nonmissing values**. The parking spaces fall in other tracts, so final density missing counts are **0** each. No zero-area values or density missingness were silently filled.

## 6. Business activity

- Raw records: **632,799**. Exact duplicate rows **0**, duplicate account IDs **0**.
- Missing raw LOCATION **66,505**; missing NAICS **57,281**.
- Usable geocoded records: **559,615** after parsing, valid latitude/longitude ranges, and excluding (0,0). **73,184** records cannot contribute for location reasons. Projected nonfinite points **0**.
- Vintage: **October 2026**, versus August 2025 occupancy. No attempt was made to claim this is a historical business census.
- Radius: fixed **0.25 miles = 402.336 metres**, chosen as a local walking-distance proxy without model optimization.
- Distance method/CRS: GeoPandas metre buffers and intersecting-point join in **EPSG:26911, NAD83 / UTM zone 11N**.
- Variables: `nearby_business_count`, counting located registry accounts; `nearby_restaurant_retail_count`, counting located accounts with NAICS prefixes **722, 44, or 45**. Prefix 722 includes food services/drinking places beyond restaurants; missing classifications contribute only to the all-business count. **65,528** located records qualify for the subset.
- Different accounts at the same address remain separate. Counts are not necessarily distinct physical operating destinations.

| Variable | Minimum | Median | Mean | Maximum |
|---|---:|---:|---:|---:|
| `nearby_business_count` | 129 | 949 | 1,177.134 | 4,825 |
| `nearby_restaurant_retail_count` | 21 | 176 | 228.786 | 878 |

All **4,139** spaces receive counts; missing counts **0**. The left spatial join would produce zero for no located eligible records, not missing. Zero means absence in the observed geocoded registry subset, not proof of zero actual business activity; no zero counts occur in this particular sample.

## 7. Zoning

- Original acquisition: **58,952 records**, **58,855 distinct source IDs**, across 28 pages.
- Source availability: four iCloud-placeholder pages were inaccessible. Two were restored from hash-identical official responses. Two differing current pages were saved separately under `data/raw/land_use/supplement_20261022/`, preserving the original placeholders.
- The mixed pages contain **58,956 features**; **4 new IDs** outside original coverage are excluded only in memory. All original distinct IDs remain represented in **58,952** working records, but **40 IDs** have changed duplicate multiplicities. This is a mixed-retrieval layer, not an identical historical reconstruction.
- Duplicate handling: **0 exact duplicate features**; **97 repeated IDs** are retained because their features differ. Fifteen ring sets produce empty areas and are omitted only from spatial matching; **58,937 nonempty valid features** remain. No manual geometry repair or invented boundary is applied.
- Geometry/CRS: ArcGIS rings converted to polygon areas using Shapely `build_area(MultiLineString(rings))`, EPSG:3857.
- Fields: source `ZONE_CMPLT`, `ZONE_CLASS`, `ZONING_DESCRIPTION`, saved as `zoning_code`, `zoning_class`, `zoning_description`. No invented broad commercial/residential/industrial grouping. Blank source labels become missing in derived labels.
- Spatial matches: **49 codes (1.1839%)**; **4,090 unmatched (98.8161%)**; no parking IDs duplicated, no multiple-polygon or conflicting-label assignments in this run.
- General overlap rule: identical matching label combinations may collapse to one assignment; conflicting combinations remain missing with an ambiguous flag, never an arbitrary first polygon.
- Street points mostly do not fall inside zoning polygons, likely reflecting street-versus-parcel coverage. No nearest-parcel fallback. Only **20** nonmissing source class labels remain; this is **not yet a broadly usable zoning predictor**.

## 8. Final candidate predictors

`price_midpoint`, `time_limit_hours`, `MeterType`, `RateType`, `latitude`, `longitude`, `population`, `median_income`, `housing_units`, `population_density`, `housing_density`, `drive_alone_share`, `transit_share`, `walk_share`, `nearby_business_count`, `nearby_restaurant_retail_count`, `zoning_code`, `zoning_class`, `zoning_description`.

These include alternatives and correlated measures, not a selected model. Source `RateRange` and `MeteredTimeLimit`, `BlockFace`, GEOID, commuting counts, and tract area are retained for traceability or future consideration; choosing further specifications is deferred. Match-status fields are quality/support fields, not proposed explanatory variables.

## 9. Missingness

No complete-case restriction is imposed. Counts and percentages are measured over all 4,139 rows.

| Candidate X | Missing count | Missing percent |
|---|---:|---:|
| `price_midpoint` | 0 | 0.0000% |
| `time_limit_hours` | 0 | 0.0000% |
| `MeterType` | 0 | 0.0000% |
| `RateType` | 0 | 0.0000% |
| `latitude` | 0 | 0.0000% |
| `longitude` | 0 | 0.0000% |
| `population` | 0 | 0.0000% |
| `median_income` | 44 | 1.0631% |
| `housing_units` | 0 | 0.0000% |
| `population_density` | 0 | 0.0000% |
| `housing_density` | 0 | 0.0000% |
| `drive_alone_share` | 0 | 0.0000% |
| `transit_share` | 0 | 0.0000% |
| `walk_share` | 0 | 0.0000% |
| `nearby_business_count` | 0 | 0.0000% |
| `nearby_restaurant_retail_count` | 0 | 0.0000% |
| `zoning_code` | 4,090 | 98.8161% |
| `zoning_class` | 4,119 | 99.5168% |
| `zoning_description` | 4,091 | 98.8403% |

## 10. Important assumptions

1. Exact SpaceID matching and exclusion of the 46 unmatched inventory IDs establish the base; no later predictor-based exclusions.
2. The prepared occupancy outcome, 24-hour gap rule, UNKNOWN exclusion, ≥25 raw active days, and meter variables are inherited unchanged.
3. Meter coordinates are interpreted as WGS84 longitude/latitude. Broad Southern California bounds are a validation assertion, not a coordinate correction; all base points pass.
4. Tract matching requires a containing polygon, without nearest fallback. All tract assignments are unique.
5. ACS geography codes are the 11-digit tract GEOIDs; commuting shares use all B08301 workers, including home workers.
6. Gazetteer densities use square miles of land and leave nonpositive denominators missing; no ACS imputation.
7. Fixed quarter-mile buffers in local metre-based UTM projection; radius not chosen from regression results.
8. Business activity counts located registry records, including distinct co-located accounts; unavailable coordinates cannot contribute. Missing NAICS is not a food-service/retail classification.
9. NAICS 722 and 44–45 define the combined food-service/retail subset. Zero denotes no eligible observed located records, not verified absence of businesses.
10. Later-vintage business/meter sources are proxies for historical conditions, not exact August 2025 measurements.
11. Two supplemental zoning pages and restriction to original distinct-ID coverage are explicit source-recovery choices; changed multiplicities are disclosed.
12. ArcGIS rings are interpreted as polygon linework; exact duplicate features may be removed, repeated IDs alone are not removed, and empty areas are not spatially matched.
13. Zoning requires containing polygons; conflicting labels stay missing and source blanks are treated as missing. No broad categories or nearest assignments are invented.
14. Missing candidate predictors do not remove parking rows, and quality flags remain in the saved dataset. No final predictor selection or causal interpretation is imposed.

## 11. Data-vintage mismatches

| Source | Vintage |
|---|---|
| Occupancy | August 2025 local-calendar month |
| Meter inventory | October 2026 snapshot; reused Notebook 02 output |
| ACS | 2024 five-year release, 2020–2024 estimates |
| Gazetteer / TIGER/Line | 2024 geographic files |
| Business registry | October 2026 snapshot |
| Zoning | Original October 16, 2026 retrieval plus two October 21 Pacific / October 22 UTC supplements; effective zoning dates unverified |

No historical equivalence was established. Price remains potentially endogenous; the dataset supports association analysis, not automatic causal claims.

## 12. Problems or unresolved issues

- Zoning coverage is only 49/4,139; code/class/description missingness differs because some matched source labels are blank. This is the main unresolved spatial predictor.
- Two original zoning placeholders remain unreadable; reproducibility uses explicitly saved supplemental copies whose attributes need not match the original dates.
- Median income is missing for 44 parking rows; no imputation or complete-case selection.
- 73,184 business records lack usable locations, and some classifications are missing. The later registry may reflect future openings/closures, co-located accounts, administrative registrations, and activity other than physical destinations.
- Whole-inventory coordinate problems remain outside this base; all 4,139 retained coordinates passed the stated check without changes.
- Price midpoint simplifies TOD/JUMP amounts and may mix durations. The inherited compound time-limit interpretation remains a caveat.
- Sensor persistence/reporting, researcher-chosen occupancy rules, unequal valid time, sensor selection, spatial dependence, and source vintage remain limitations from the existing project.
- No assignment of the 46 inventory-unmatched spaces and no zoning fallback were attempted. No final model-specific sample or predictor set has been chosen.

## 13. Code/method complexity

Runtime: Python 3.14; pandas 3.0.2, NumPy 2.4.4, GeoPandas 1.2.0, Shapely 2.2.0, pyproj 3.8.0, and pyogrio 0.13.0. GeoPandas was already listed in project requirements but missing from the runtime, so it and its geospatial dependencies were installed; requirements.txt was not changed.

Notebook tools are pandas merges/groupby/strings/summaries, NumPy flags and finite checks, GeoPandas shapefile loading/CRS conversion/point-in-polygon/buffers/spatial joins, Shapely polygon construction, and standard-library JSON/Path/Counter. No custom notebook functions/classes or ML pipelines. GIS-specific methods may be beyond ECON 430, but are used only for geographic linkage and fixed-radius counting. In particular, [Shapely build_area](https://shapely.readthedocs.io/en/stable/reference/shapely.build_area.html) handles polygon areas/holes from source ring linework; [GeoPandas spatial joins](https://geopandas.org/en/stable/docs/reference/api/geopandas.sjoin.html) support the containment/counting steps. No spatial econometric model or hypothesis test.

## 14. Files changed

- Modified `notebooks/03_build_cross_section.ipynb` (executed, documented; no saved errors/debug dumps).
- Created `data/processed/parking_cross_section.csv`.
- Updated `README.md` and `docs/data_sources.md`.
- Created `docs/notebook03_completion_report.md` (this report).
- Created `data/raw/land_use/supplement_20261022/zoning_offset_035000.json` and `zoning_offset_055000.json` from official current responses, separately from originals.
- Created `docs/retrievals/20261022T054720128988Z/manifest.jsonl`.
- Restored local availability of original `zoning_offset_000000.json` and `zoning_offset_030000.json` with identical acquisition hashes and original modification times; their source contents are unchanged.
- Notebooks 01, 02, and 04–08, both previous processed inputs, ACS/Gazetteer/TIGER source files, acquisition scripts, and requirements remain unchanged. The two other original zoning placeholders were not overwritten.

## 15. Notebook structure

- 1. Load the prepared parking data
- 2. Match occupancy to meter characteristics
- 3. Read the Census estimates by tract
- 4. Construct commuting shares and densities
- 5. Load the official tract polygons
- 6. Assign parking spaces to Census tracts
- 7. Attach the ACS candidate predictors
- 8. Inspect the business registry
- 9. Prepare located businesses and a transparent activity subset
- 10. Count businesses within a quarter mile
- 11. Read and validate the zoning batches
- 12. Match the available zoning polygons
- 13. Assemble one row per parking space
- 14. Validate the candidate variables
- 15. Save the cross-section for later analysis
- Summary

## 16. Validation outputs

One row per space: **4,139 rows / 4,139 unique IDs / 0 duplicates**. All assigned tract and ACS matches are unique. No further parking rows removed.

| Numeric variable | Minimum | Maximum |
|---|---:|---:|
| `occupancy_rate` | 0.003520 | 0.998916 |
| `occupied_minutes` | 99.050000 | 39,082.250000 |
| `total_minutes` | 14,080.333333 | 44,635.466667 |
| `active_days` | 25.000000 | 31.000000 |
| `price_midpoint` | 0.500000 | 8.000000 |
| `time_limit_hours` | 0.250000 | 10.000000 |
| `latitude` | 33.736298 | 34.105161 |
| `longitude` | -118.480323 | -118.236110 |
| `population` | 1,051.000000 | 13,681.000000 |
| `median_income` | 9,375.000000 | 157,115.000000 |
| `housing_units` | 0.000000 | 7,590.000000 |
| `commuters` | 225.000000 | 7,007.000000 |
| `drive_alone` | 20.000000 | 2,820.000000 |
| `public_transit` | 0.000000 | 400.000000 |
| `walked` | 0.000000 | 2,024.000000 |
| `ALAND_SQMI` | 0.018000 | 0.992000 |
| `population_density` | 1,915.322581 | 132,736.842105 |
| `housing_density` | 0.000000 | 101,157.894737 |
| `drive_alone_share` | 0.088889 | 0.790323 |
| `transit_share` | 0.000000 | 0.271111 |
| `walk_share` | 0.000000 | 0.627193 |
| `nearby_business_count` | 129.000000 | 4,825.000000 |
| `nearby_restaurant_retail_count` | 21.000000 | 878.000000 |

- Occupancy or nonmissing commute shares outside [0,1]: **0**.
- Negative values in quantities required to be nonnegative: **0**.
- Infinite/nonfinite nonmissing numeric values: **0**.
- Food-service/retail count above all-business count: **0**.
- Implausible coordinates in the retained base: **0** under the stated broad bounds.
- This does not prove perfect source accuracy or historical validity.

Categorical counts:

- `MeterType`: Single-Space: 4,006; Multi-Space: 133.
- `RateType`: TOD: 3,323; FLAT: 737; JUMP: 79.
- `zoning_class`: MISSING: 4,119; C2: 12; C4: 6; VARIOUS: 1; PF: 1.
- `zoning_description`: MISSING: 4,091; Commercial - ADP, C1, C1.5, C2, C4, C5, CR, CW, LASED, WC: 18; Public (Chapter 1A): 16; Commercial-Mixed (Chapter 1A): 9; Industrial-Mixed (Chapter 1A): 4; Public Facility - PF: 1.

All 20 code cells execute successfully from a fresh kernel with the documented inputs and installed packages. No error outputs are retained. Notebook 04 was not started.
