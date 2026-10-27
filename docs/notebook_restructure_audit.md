# Notebook restructure audit

Baseline: `1a6ef43cc32cd4e51d72e928ca2d9edfcfbcbc30` on `Kerem_Vis`; main recorded as `e480f468a9366603f908f4a7c72ab6c4b5999925`.

Migration branch: `refactor/430-rubric-alignment`. Original notebooks remain recoverable from the baseline commit. All original cell sources, outputs (including PNG/HTML), execution counts and metadata have destinations. Existing cell IDs are preserved; absent analysis IDs get deterministic IDs. Cleaning IDs remain unchanged. Old working-tree paths were removed only after cell-level preservation assertions passed. No data are overwritten.

The JSON inventory was written before notebook edits. [Baseline inventory](notebook_baseline_inventory.json) records original hashes and metadata; [machine-readable mapping](notebook_cell_migration.json) records each source and destination hash/index. Indices in this report are zero-based. Duplicate destinations are intentional and individually listed.

Reordering moves diagnostics into rubric order, selection into Boruta/Cp/VIF order, and EDA into 2(a)–2(h). Original internal headings/text and historical completion claims remain verbatim. The new audit supersedes those claims. The original results EDA setup is duplicated with identifier names prefixed `results_` so it cannot overwrite the original EDA sample. One new bridge assigns the unchanged selected_variables list to predictors for the moved results summary. The log-density check executes after the HC1 reference fit under 4(b), with an explicit cross-reference to 4(a). This setup retains its existing model fits solely as inherited dependencies. No econometric specification changes.

README and supporting documentation are retained; current navigation is added separately and obsolete notebook file links are corrected. Detailed README definitions, source references and assumptions are linked from Sections 1, 2 and 6. No acquisition source, visualization file, raw/processed input, or preexisting documentation file is deleted.

## Original 01_clean_occupancy.ipynb

| Index / original ID | Type | Destination / cell | Heading | Change / preservation |
|---|---|---|---|---|
| 0 / absent | markdown | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 0 | # 01 — Clean Occupancy Data | Unchanged; outputs and metadata preserved |
| 1 / 4c8888b9 | markdown | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 1 | ## 1. Load the raw transactions | Unchanged; outputs and metadata preserved |
| 2 / absent | code | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 2 | Original ordered cleaning cell | Relative ../data and ../docs paths gain one parent; saved historical path outputs unchanged; outputs and metadata preserved |
| 3 / 7717963a | markdown | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 3 | ## 2. Check the records and timestamps | Unchanged; outputs and metadata preserved |
| 4 / absent | code | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 4 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 5 / absent | code | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 5 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 6 / absent | code | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 6 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 7 / e260f311 | markdown | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 7 | ## 3. Inspect coverage across parking spaces | Unchanged; outputs and metadata preserved |
| 8 / absent | code | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 8 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 9 / absent | code | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 9 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 10 / absent | code | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 10 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 11 / d17af22f | markdown | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 11 | ## 4. Inspect one space’s event sequence | Unchanged; outputs and metadata preserved |
| 12 / absent | code | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 12 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 13 / 3aecec9a | markdown | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 13 | ## 5. Measure time in each recorded state | Unchanged; outputs and metadata preserved |
| 14 / absent | code | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 14 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 15 / 385d1516 | markdown | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 15 | ## 6. Inspect long gaps between events | Unchanged; outputs and metadata preserved |
| 16 / absent | code | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 16 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 17 / absent | code | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 17 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 18 / c460bf09 | markdown | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 18 | ## 7. Identify valid intervals | Unchanged; outputs and metadata preserved |
| 19 / absent | code | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 19 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 20 / 6008ef2a | markdown | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 20 | ## 8. Calculate the monthly occupancy rate | Unchanged; outputs and metadata preserved |
| 21 / absent | code | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 21 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 22 / 0dfc9169 | markdown | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 22 | ## 9. Require at least 25 active calendar days | Unchanged; outputs and metadata preserved |
| 23 / absent | code | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 23 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 24 / 2e9f6b53 | markdown | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 24 | ## 10. Save the parking-space cross-section | Unchanged; outputs and metadata preserved |
| 25 / absent | code | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 25 | Original ordered cleaning cell | Relative ../data and ../docs paths gain one parent; saved historical path outputs unchanged; outputs and metadata preserved |
| 26 / ff5200db | markdown | [01_clean_occupancy.ipynb](../notebooks/cleaning/01_clean_occupancy.ipynb) / 26 | ## Summary | Unchanged; outputs and metadata preserved |

## Original 02_clean_meter_inventory.ipynb

| Index / original ID | Type | Destination / cell | Heading | Change / preservation |
|---|---|---|---|---|
| 0 / absent | markdown | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 0 | # 02 — Clean Meter Inventory | Unchanged; outputs and metadata preserved |
| 1 / 8b9b2632 | markdown | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 1 | ## 1. Load the raw meter inventory | Unchanged; outputs and metadata preserved |
| 2 / absent | code | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 2 | Original ordered cleaning cell | Relative ../data and ../docs paths gain one parent; saved historical path outputs unchanged; outputs and metadata preserved |
| 3 / b5365051 | markdown | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 3 | ## 2. Check the inventory structure and categories | Unchanged; outputs and metadata preserved |
| 4 / absent | code | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 4 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 5 / absent | code | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 5 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 6 / 99fbdb9d | markdown | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 6 | ## 3. Confirm and remove exact duplicate records | Unchanged; outputs and metadata preserved |
| 7 / absent | code | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 7 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 8 / absent | code | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 8 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 9 / e58c52b1 | markdown | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 9 | ## 4. Express parking time limits in hours | Unchanged; outputs and metadata preserved |
| 10 / absent | code | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 10 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 11 / absent | code | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 11 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 12 / 2c443088 | markdown | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 12 | ## 5. Inspect pricing structures and extract dollar amounts | Unchanged; outputs and metadata preserved |
| 13 / absent | code | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 13 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 14 / absent | code | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 14 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 15 / 59b0ae48 | markdown | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 15 | ## 6. Construct the price proxy and numeric coordinates | Unchanged; outputs and metadata preserved |
| 16 / absent | code | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 16 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 17 / 512f9e1c | markdown | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 17 | ## 7. Validate the numeric variables | Unchanged; outputs and metadata preserved |
| 18 / absent | code | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 18 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 19 / 2b7cd98c | markdown | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 19 | ## 8. Check matches to the cleaned occupancy sample | Unchanged; outputs and metadata preserved |
| 20 / absent | code | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 20 | Original ordered cleaning cell | Relative ../data and ../docs paths gain one parent; saved historical path outputs unchanged; outputs and metadata preserved |
| 21 / absent | code | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 21 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 22 / 8647f09f | markdown | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 22 | ## 9. Save the cleaned meter inventory | Unchanged; outputs and metadata preserved |
| 23 / absent | code | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 23 | Original ordered cleaning cell | Relative ../data and ../docs paths gain one parent; saved historical path outputs unchanged; outputs and metadata preserved |
| 24 / 2f5fc169 | markdown | [02_clean_meter_inventory.ipynb](../notebooks/cleaning/02_clean_meter_inventory.ipynb) / 24 | ## Summary | Unchanged; outputs and metadata preserved |

## Original 03_build_cross_section.ipynb

| Index / original ID | Type | Destination / cell | Heading | Change / preservation |
|---|---|---|---|---|
| 0 / 20e6a435 | markdown | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 0 | # 03 — Build Cross-Section | Unchanged; outputs and metadata preserved |
| 1 / defa1eaa | markdown | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 1 | ## 1. Load the prepared parking data | Unchanged; outputs and metadata preserved |
| 2 / 759e34ea | code | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 2 | Original ordered cleaning cell | Relative ../data and ../docs paths gain one parent; saved historical path outputs unchanged; outputs and metadata preserved |
| 3 / 5a83c322 | markdown | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 3 | ## 2. Match occupancy to meter characteristics | Unchanged; outputs and metadata preserved |
| 4 / 32ff0bd6 | code | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 4 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 5 / f40fdba6 | markdown | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 5 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 6 / b7442355 | code | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 6 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 7 / 2eb0f30b | markdown | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 7 | ## 3. Read the Census estimates by tract | Unchanged; outputs and metadata preserved |
| 8 / 43202101 | code | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 8 | Original ordered cleaning cell | Relative ../data and ../docs paths gain one parent; saved historical path outputs unchanged; outputs and metadata preserved |
| 9 / ccb48697 | markdown | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 9 | ## 4. Construct commuting shares and densities | Unchanged; outputs and metadata preserved |
| 10 / e799fdf6 | code | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 10 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 11 / 9b745afd | code | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 11 | Original ordered cleaning cell | Relative ../data and ../docs paths gain one parent; saved historical path outputs unchanged; outputs and metadata preserved |
| 12 / 09f1d13e | markdown | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 12 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 13 / 3da90620 | code | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 13 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 14 / 972708be | markdown | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 14 | ## 5. Load the official tract polygons | Unchanged; outputs and metadata preserved |
| 15 / 1f19140b | code | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 15 | Original ordered cleaning cell | Relative ../data and ../docs paths gain one parent; saved historical path outputs unchanged; outputs and metadata preserved |
| 16 / bc36f206 | markdown | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 16 | ## 6. Assign parking spaces to Census tracts | Unchanged; outputs and metadata preserved |
| 17 / dce4bbbc | code | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 17 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 18 / 2a7c8de5 | markdown | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 18 | ## 7. Attach the ACS candidate predictors | Unchanged; outputs and metadata preserved |
| 19 / 509aaa6d | code | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 19 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 20 / 7d21d511 | markdown | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 20 | ## 8. Inspect the business registry | Unchanged; outputs and metadata preserved |
| 21 / 4a5fe6eb | code | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 21 | Original ordered cleaning cell | Relative ../data and ../docs paths gain one parent; saved historical path outputs unchanged; outputs and metadata preserved |
| 22 / df341a0d | markdown | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 22 | ## 9. Prepare located businesses and a transparent activity subset | Unchanged; outputs and metadata preserved |
| 23 / 7d687b3b | code | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 23 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 24 / d2782d76 | markdown | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 24 | ## 10. Count businesses within a quarter mile | Unchanged; outputs and metadata preserved |
| 25 / b6f157fc | code | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 25 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 26 / 1643c159 | markdown | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 26 | ## 11. Read and validate the zoning batches | Relative ../data and ../docs paths gain one parent; saved historical path outputs unchanged; outputs and metadata preserved |
| 27 / 57cf4e7b | code | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 27 | Original ordered cleaning cell | Relative ../data and ../docs paths gain one parent; saved historical path outputs unchanged; outputs and metadata preserved |
| 28 / 89747be4 | markdown | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 28 | ## 12. Match the available zoning polygons | Unchanged; outputs and metadata preserved |
| 29 / 27b79ba8 | code | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 29 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 30 / 8ddf2a4d | markdown | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 30 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 31 / 407d42bf | code | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 31 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 32 / 422151d5 | markdown | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 32 | ## 13. Assemble one row per parking space | Unchanged; outputs and metadata preserved |
| 33 / 6d3d91b0 | code | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 33 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 34 / 85fcccdd | markdown | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 34 | ## 14. Validate the candidate variables | Unchanged; outputs and metadata preserved |
| 35 / 462a4c15 | code | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 35 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 36 / 55741014 | code | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 36 | Original ordered cleaning cell | Unchanged; outputs and metadata preserved |
| 37 / 9d522ee7 | markdown | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 37 | ## 15. Save the cross-section for later analysis | Unchanged; outputs and metadata preserved |
| 38 / 864f455d | code | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 38 | Original ordered cleaning cell | Relative ../data and ../docs paths gain one parent; saved historical path outputs unchanged; outputs and metadata preserved |
| 39 / 4a98ce43 | markdown | [03_build_cross_section.ipynb](../notebooks/cleaning/03_build_cross_section.ipynb) / 39 | ## Summary | Unchanged; outputs and metadata preserved |

## Original 04_eda.ipynb

| Index / original ID | Type | Destination / cell | Heading | Change / preservation |
|---|---|---|---|---|
| 0 / 4327a8d5 | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 2 | 2(a) Dataset Source, Time Period, Sample Selection, and Variable Definitions | Unchanged; outputs and metadata preserved |
| 1 / 5e77eb52 | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 3 | 2(a) Dataset Source, Time Period, Sample Selection, and Variable Definitions | Unchanged; outputs and metadata preserved |
| 2 / 4b7c7f05 | code | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 4 | 2(a) Dataset Source, Time Period, Sample Selection, and Variable Definitions | Unchanged; outputs and metadata preserved |
| 3 / d46a5236 | code | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 5 | 2(a) Dataset Source, Time Period, Sample Selection, and Variable Definitions | Unchanged; outputs and metadata preserved |
| 4 / 014359bb | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 6 | 2(a) Dataset Source, Time Period, Sample Selection, and Variable Definitions | Unchanged; outputs and metadata preserved |
| 5 / aa6a0723 | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 7 | 2(a) Dataset Source, Time Period, Sample Selection, and Variable Definitions | Unchanged; outputs and metadata preserved |
| 6 / 5f859ed4 | code | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 8 | 2(a) Dataset Source, Time Period, Sample Selection, and Variable Definitions | Unchanged; outputs and metadata preserved |
| 7 / 1dec5ee1 | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 9 | 2(a) Dataset Source, Time Period, Sample Selection, and Variable Definitions | Unchanged; outputs and metadata preserved |
| 8 / 172bf99f | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 10 | 2(a) Dataset Source, Time Period, Sample Selection, and Variable Definitions | Unchanged; outputs and metadata preserved |
| 9 / a928e435 | code | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 11 | 2(a) Dataset Source, Time Period, Sample Selection, and Variable Definitions | Unchanged; outputs and metadata preserved |
| 10 / 35a57577 | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 12 | 2(a) Dataset Source, Time Period, Sample Selection, and Variable Definitions | Unchanged; outputs and metadata preserved |
| 11 / 0cfaf58b | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 14 | 2(b) Comprehensive Descriptive Statistics | Unchanged; outputs and metadata preserved |
| 12 / 058187e9 | code | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 15 | 2(b) Comprehensive Descriptive Statistics | Unchanged; outputs and metadata preserved |
| 13 / 42b5f329 | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 16 | 2(b) Comprehensive Descriptive Statistics | Unchanged; outputs and metadata preserved |
| 20 / aaed4d9b | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 18 | 2(c) Histograms, Boxplots, Correlation Heatmap, and Scatterplots | Unchanged; outputs and metadata preserved |
| 21 / b5ec1c88 | code | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 19 | 2(c) Histograms, Boxplots, Correlation Heatmap, and Scatterplots | Unchanged; outputs and metadata preserved |
| 22 / 5d0fe595 | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 20 | 2(c) Histograms, Boxplots, Correlation Heatmap, and Scatterplots | Unchanged; outputs and metadata preserved |
| 23 / 870ef019 | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 21 | 2(c) Histograms, Boxplots, Correlation Heatmap, and Scatterplots | Unchanged; outputs and metadata preserved |
| 24 / 75f4c4d0 | code | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 22 | 2(c) Histograms, Boxplots, Correlation Heatmap, and Scatterplots | Unchanged; outputs and metadata preserved |
| 25 / e26336c3 | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 23 | 2(c) Histograms, Boxplots, Correlation Heatmap, and Scatterplots | Unchanged; outputs and metadata preserved |
| 26 / 7a5a4512 | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 24 | 2(c) Histograms, Boxplots, Correlation Heatmap, and Scatterplots | Unchanged; outputs and metadata preserved |
| 27 / 4812cfa2 | code | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 25 | 2(c) Histograms, Boxplots, Correlation Heatmap, and Scatterplots | Unchanged; outputs and metadata preserved |
| 28 / 23c6194e | code | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 26 | 2(c) Histograms, Boxplots, Correlation Heatmap, and Scatterplots | Unchanged; outputs and metadata preserved |
| 29 / 04bbed66 | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 27 | 2(c) Histograms, Boxplots, Correlation Heatmap, and Scatterplots | Unchanged; outputs and metadata preserved |
| 35 / a6a467c5 | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 36 | 2(e) Nonlinearities and Potential Transformations | Unchanged; outputs and metadata preserved |
| 30 / 6ba01cd0 | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 38 | 2(f) Outlier Detection and Discussion | Unchanged; outputs and metadata preserved |
| 31 / 55183605 | code | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 39 | 2(f) Outlier Detection and Discussion | Unchanged; outputs and metadata preserved |
| 32 / 47a8880f | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 40 | 2(f) Outlier Detection and Discussion | Unchanged; outputs and metadata preserved |
| 33 / 93354d18 | code | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 41 | 2(f) Outlier Detection and Discussion | Unchanged; outputs and metadata preserved |
| 34 / 84c30bd9 | code | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 42 | 2(f) Outlier Detection and Discussion | Unchanged; outputs and metadata preserved |
| 14 / f70f0f6d | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 44 | 2(g) Missing Values, Imputation Decisions, and Sensitivity Analysis | Unchanged; outputs and metadata preserved |
| 15 / 71fc07af | code | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 45 | 2(g) Missing Values, Imputation Decisions, and Sensitivity Analysis | Unchanged; outputs and metadata preserved |
| 16 / c39faaef | code | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 46 | 2(g) Missing Values, Imputation Decisions, and Sensitivity Analysis | Unchanged; outputs and metadata preserved |
| 17 / fe98a831 | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 47 | 2(g) Missing Values, Imputation Decisions, and Sensitivity Analysis | Unchanged; outputs and metadata preserved |
| 18 / 7496c063 | code | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 48 | 2(g) Missing Values, Imputation Decisions, and Sensitivity Analysis | Unchanged; outputs and metadata preserved |
| 19 / 09690363 | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 49 | 2(g) Missing Values, Imputation Decisions, and Sensitivity Analysis | Unchanged; outputs and metadata preserved |
| 36 / 4db1b00f | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 55 | 2(h) Pandas Profiling Analysis and Findings | Unchanged; outputs and metadata preserved |
| 37 / 82e9b567 | code | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 56 | 2(h) Pandas Profiling Analysis and Findings | Unchanged; outputs and metadata preserved |

## Original 05_variable_selection.ipynb

| Index / original ID | Type | Destination / cell | Heading | Change / preservation |
|---|---|---|---|---|
| 0 / 78894574 | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 2 | Introduction | Unchanged; outputs and metadata preserved |
| 1 / a0a084b3 | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 3 | Introduction | Unchanged; outputs and metadata preserved |
| 2 / 0afd58ff | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 4 | Introduction | Unchanged; outputs and metadata preserved |
| 3 / e534b821 | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 5 | Introduction | Unchanged; outputs and metadata preserved |
| 6 / 2c6a1658 | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 7 | 3(a) Boruta Algorithm | Unchanged; outputs and metadata preserved |
| 7 / 87799c85 | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 8 | 3(a) Boruta Algorithm | Unchanged; outputs and metadata preserved |
| 8 / 35f21dcc | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 9 | 3(a) Boruta Algorithm | Unchanged; outputs and metadata preserved |
| 9 / 28064bf9 | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 11 | 3(b) Mallows Cp Criterion | Unchanged; outputs and metadata preserved |
| 10 / aa2ca302 | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 12 | 3(b) Mallows Cp Criterion | Unchanged; outputs and metadata preserved |
| 11 / c6116a0e | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 13 | 3(b) Mallows Cp Criterion | Unchanged; outputs and metadata preserved |
| 12 / f294ad56 | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 14 | 3(b) Mallows Cp Criterion | Unchanged; outputs and metadata preserved |
| 13 / cfb03b16 | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 15 | 3(b) Mallows Cp Criterion | Unchanged; outputs and metadata preserved |
| 4 / 003ca0d9 | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 17 | 3(c) Variance Inflation Factors | Unchanged; outputs and metadata preserved |
| 5 / e0a71541 | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 18 | 3(c) Variance Inflation Factors | Unchanged; outputs and metadata preserved |
| 14 / acd2ad11 | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 19 | 3(c) Variance Inflation Factors | Unchanged; outputs and metadata preserved |
| 15 / b135e413 | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 20 | 3(c) Variance Inflation Factors | Unchanged; outputs and metadata preserved |
| 16 / 20091861 | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 21 | 3(c) Variance Inflation Factors | Unchanged; outputs and metadata preserved |

## Original 06_regression_models.ipynb

| Index / original ID | Type | Destination / cell | Heading | Change / preservation |
|---|---|---|---|---|
| 0 / d8d80c1a | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 23 | 3(d) Three Competing Regression Models | Unchanged; outputs and metadata preserved |
| 1 / 8e3f66a7 | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 24 | 3(d) Three Competing Regression Models | Unchanged; outputs and metadata preserved |
| 2 / acfc54c8 | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 25 | 3(d) Three Competing Regression Models | Unchanged; outputs and metadata preserved |
| 3 / db16b7d4 | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 26 | 3(d) Three Competing Regression Models | Unchanged; outputs and metadata preserved |
| 4 / 63d77da5 | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 28 | 3(d) Three Competing Regression Models | Unchanged; outputs and metadata preserved |
| 5 / 4732a8c3 | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 29 | 3(d) Three Competing Regression Models | Unchanged; outputs and metadata preserved |
| 6 / b72e06b8 | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 30 | 3(d) Three Competing Regression Models | Unchanged; outputs and metadata preserved |
| 7 / eb472af4 | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 32 | 3(d) Three Competing Regression Models | Unchanged; outputs and metadata preserved |
| 8 / e587588e | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 33 | 3(d) Three Competing Regression Models | Unchanged; outputs and metadata preserved |
| 9 / 522eb9c3 | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 34 | 3(d) Three Competing Regression Models | Unchanged; outputs and metadata preserved |
| 10 / 8819a47d | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 36 | 3(d) Three Competing Regression Models | Unchanged; outputs and metadata preserved |
| 11 / 2f8d254e | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 37 | 3(d) Three Competing Regression Models | Unchanged; outputs and metadata preserved |
| 12 / 74661b1f | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 38 | 3(d) Three Competing Regression Models | Unchanged; outputs and metadata preserved |
| 13 / 8eeb5661 | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 39 | 3(d) Three Competing Regression Models | Unchanged; outputs and metadata preserved |
| 14 / ef6439ee | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 41 | 3(e) AIC, BIC, Adjusted R², and Cross-Validation Comparison | Unchanged; outputs and metadata preserved |
| 15 / 87747448 | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 42 | 3(e) AIC, BIC, Adjusted R², and Cross-Validation Comparison | Unchanged; outputs and metadata preserved |
| 16 / bb407043 | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 43 | 3(e) AIC, BIC, Adjusted R², and Cross-Validation Comparison | Unchanged; outputs and metadata preserved |
| 17 / 4f0cad3d | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 44 | 3(e) AIC, BIC, Adjusted R², and Cross-Validation Comparison | Unchanged; outputs and metadata preserved |
| 18 / 432bedb2 | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 45 | 3(e) AIC, BIC, Adjusted R², and Cross-Validation Comparison | Unchanged; outputs and metadata preserved |
| 19 / 8b85b502 | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 46 | 3(e) AIC, BIC, Adjusted R², and Cross-Validation Comparison | Unchanged; outputs and metadata preserved |
| 24 / 7cb48532 | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 47 | 3(e) AIC, BIC, Adjusted R², and Cross-Validation Comparison | Unchanged; outputs and metadata preserved |
| 25 / ad5ee1bd | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 48 | 3(e) AIC, BIC, Adjusted R², and Cross-Validation Comparison | Unchanged; outputs and metadata preserved |
| 26 / ed91582f | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 49 | 3(e) AIC, BIC, Adjusted R², and Cross-Validation Comparison | Unchanged; outputs and metadata preserved |
| 27 / e4d5cdba | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 50 | 3(e) AIC, BIC, Adjusted R², and Cross-Validation Comparison | Unchanged; outputs and metadata preserved |
| 28 / b56f12f3 | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 51 | 3(e) AIC, BIC, Adjusted R², and Cross-Validation Comparison | Unchanged; outputs and metadata preserved |
| 29 / c723fc83 | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 53 | 3(f) Final Model Selection and Justification | Unchanged; outputs and metadata preserved |
| 30 / d0aca6e9 | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 54 | 3(f) Final Model Selection and Justification | Unchanged; outputs and metadata preserved |
| 31 / 8beba178 | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 55 | 3(f) Final Model Selection and Justification | Unchanged; outputs and metadata preserved |
| 32 / 2f6689c1 | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 56 | 3(f) Final Model Selection and Justification | Unchanged; outputs and metadata preserved |
| 33 / 0cf81cef | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 57 | 3(f) Final Model Selection and Justification | Unchanged; outputs and metadata preserved |
| 34 / 2ca74c13 | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 58 | 3(f) Final Model Selection and Justification | Unchanged; outputs and metadata preserved |
| 20 / 357e07b4 | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 63 | 3(f) Final Model Selection and Justification | Unchanged; outputs and metadata preserved |
| 21 / eadd4444 | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 64 | 3(f) Final Model Selection and Justification | Unchanged; outputs and metadata preserved |
| 22 / de24b79c | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 65 | 3(f) Final Model Selection and Justification | Unchanged; outputs and metadata preserved |
| 23 / 037bc340 | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 66 | 3(f) Final Model Selection and Justification | Unchanged; outputs and metadata preserved |
| 22 / de24b79c | markdown | [05_results_interpretation.ipynb](../notebooks/05_results_interpretation.ipynb) / 10 | 5(b) Economic Interpretation of All Coefficients | Duplicated verbatim for complete coefficient/intercept narrative; intervals here are conventional, not HC1; outputs and metadata preserved |
| 23 / 037bc340 | markdown | [05_results_interpretation.ipynb](../notebooks/05_results_interpretation.ipynb) / 11 | 5(b) Economic Interpretation of All Coefficients | Duplicated verbatim for complete coefficient/intercept narrative; intervals here are conventional, not HC1; outputs and metadata preserved |

## Original 07_diagnostics.ipynb

| Index / original ID | Type | Destination / cell | Heading | Change / preservation |
|---|---|---|---|---|
| 0 / 0802414b | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 2 | Introduction | Unchanged; outputs and metadata preserved |
| 1 / 48b2a2f4 | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 3 | Introduction | Unchanged; outputs and metadata preserved |
| 2 / a537bbda | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 4 | Introduction | Unchanged; outputs and metadata preserved |
| 3 / 78a429c9 | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 5 | Introduction | Unchanged; outputs and metadata preserved |
| 4 / db689f63 | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 6 | Introduction | Unchanged; outputs and metadata preserved |
| 5 / e161a071 | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 7 | Introduction | Unchanged; outputs and metadata preserved |
| 6 / 0f8c735e | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 8 | Introduction | Unchanged; outputs and metadata preserved |
| 7 / 9d9489d7 | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 9 | Introduction | Unchanged; outputs and metadata preserved |
| 8 / e9b38b66 | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 11 | 4(a) Linearity: Residuals vs. Fitted and RESET | Unchanged; outputs and metadata preserved |
| 9 / aca50b5e | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 12 | 4(a) Linearity: Residuals vs. Fitted and RESET | Unchanged; outputs and metadata preserved |
| 10 / ce87051e | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 13 | 4(a) Linearity: Residuals vs. Fitted and RESET | Unchanged; outputs and metadata preserved |
| 11 / 311e5e19 | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 14 | 4(a) Linearity: Residuals vs. Fitted and RESET | Unchanged; outputs and metadata preserved |
| 20 / 49f1bc2e | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 15 | 4(a) Linearity: Residuals vs. Fitted and RESET | Unchanged; outputs and metadata preserved |
| 21 / 383a4cb2 | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 16 | 4(a) Linearity: Residuals vs. Fitted and RESET | Unchanged; outputs and metadata preserved |
| 22 / 6078573a | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 17 | 4(a) Linearity: Residuals vs. Fitted and RESET | Unchanged; outputs and metadata preserved |
| 15 / 8b555240 | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 19 | 4(b) Homoskedasticity: Breusch–Pagan, White, and Scale-Location | Unchanged; outputs and metadata preserved |
| 16 / 919a88b3 | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 20 | 4(b) Homoskedasticity: Breusch–Pagan, White, and Scale-Location | Unchanged; outputs and metadata preserved |
| 17 / d061e24c | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 21 | 4(b) Homoskedasticity: Breusch–Pagan, White, and Scale-Location | Unchanged; outputs and metadata preserved |
| 18 / 17f76d27 | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 22 | 4(b) Homoskedasticity: Breusch–Pagan, White, and Scale-Location | Unchanged; outputs and metadata preserved |
| 19 / 4deefb2f | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 23 | 4(b) Homoskedasticity: Breusch–Pagan, White, and Scale-Location | Unchanged; outputs and metadata preserved |
| 23 / 937c7fbf | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 25 | 4(b) Homoskedasticity: Breusch–Pagan, White, and Scale-Location | Unchanged; outputs and metadata preserved |
| 24 / 93d866a2 | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 26 | 4(b) Homoskedasticity: Breusch–Pagan, White, and Scale-Location | Unchanged; outputs and metadata preserved |
| 25 / d7ef4816 | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 27 | 4(b) Homoskedasticity: Breusch–Pagan, White, and Scale-Location | Unchanged; outputs and metadata preserved |
| 12 / b5f8b783 | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 29 | 4(c) Residual Normality: Q-Q, Jarque–Bera, and Histograms | Unchanged; outputs and metadata preserved |
| 13 / ea4ad754 | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 30 | 4(c) Residual Normality: Q-Q, Jarque–Bera, and Histograms | Unchanged; outputs and metadata preserved |
| 14 / 8be99b07 | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 31 | 4(c) Residual Normality: Q-Q, Jarque–Bera, and Histograms | Unchanged; outputs and metadata preserved |
| 26 / c6fd2d4a | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 33 | 4(d) Outliers and Influence: Cook's Distance, Leverage, and DFBETAS | Unchanged; outputs and metadata preserved |
| 27 / 2e7b8ab9 | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 34 | 4(d) Outliers and Influence: Cook's Distance, Leverage, and DFBETAS | Unchanged; outputs and metadata preserved |
| 28 / 11b87dbd | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 35 | 4(d) Outliers and Influence: Cook's Distance, Leverage, and DFBETAS | Unchanged; outputs and metadata preserved |
| 29 / dbb7a257 | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 36 | 4(d) Outliers and Influence: Cook's Distance, Leverage, and DFBETAS | Unchanged; outputs and metadata preserved |
| 30 / 7960b6f1 | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 37 | 4(d) Outliers and Influence: Cook's Distance, Leverage, and DFBETAS | Unchanged; outputs and metadata preserved |
| 31 / fbea936b | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 38 | 4(d) Outliers and Influence: Cook's Distance, Leverage, and DFBETAS | Unchanged; outputs and metadata preserved |
| 32 / 357d2b60 | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 39 | 4(d) Outliers and Influence: Cook's Distance, Leverage, and DFBETAS | Unchanged; outputs and metadata preserved |
| 33 / 5f3fee6c | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 40 | 4(d) Outliers and Influence: Cook's Distance, Leverage, and DFBETAS | Unchanged; outputs and metadata preserved |
| 34 / ce17a24e | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 41 | 4(d) Outliers and Influence: Cook's Distance, Leverage, and DFBETAS | Unchanged; outputs and metadata preserved |
| 35 / 9cf91be0 | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 43 | 4(e) Robustness: 1,000-Replication Bootstrap vs. OLS | Unchanged; outputs and metadata preserved |
| 36 / 84f170a0 | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 44 | 4(e) Robustness: 1,000-Replication Bootstrap vs. OLS | Unchanged; outputs and metadata preserved |
| 37 / 9fcf0da3 | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 45 | 4(e) Robustness: 1,000-Replication Bootstrap vs. OLS | Unchanged; outputs and metadata preserved |
| 38 / 050320fb | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 46 | 4(e) Robustness: 1,000-Replication Bootstrap vs. OLS | Unchanged; outputs and metadata preserved |
| 39 / cd555730 | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 48 | 4(f) Validation: 5-Fold or 10-Fold Cross-Validation and Out-of-Sample Accuracy | Unchanged; outputs and metadata preserved |
| 40 / f8d8690b | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 49 | 4(f) Validation: 5-Fold or 10-Fold Cross-Validation and Out-of-Sample Accuracy | Unchanged; outputs and metadata preserved |
| 41 / 8018da86 | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 50 | 4(f) Validation: 5-Fold or 10-Fold Cross-Validation and Out-of-Sample Accuracy | Unchanged; outputs and metadata preserved |
| 42 / 73009da4 | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 52 | 4(g) OLS Assumption Violations and Implications | Unchanged; outputs and metadata preserved |
| 43 / 1289294f | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 53 | 4(g) OLS Assumption Violations and Implications | Unchanged; outputs and metadata preserved |
| 44 / 5673c249 | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 54 | 4(g) OLS Assumption Violations and Implications | Unchanged; outputs and metadata preserved |
| 45 / a4b56433 | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 55 | 4(g) OLS Assumption Violations and Implications | Unchanged; outputs and metadata preserved |
| 46 / bdce26a4 | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 56 | 4(g) OLS Assumption Violations and Implications | Unchanged; outputs and metadata preserved |
| 47 / 118c31ff | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 57 | 4(g) OLS Assumption Violations and Implications | Unchanged; outputs and metadata preserved |
| 48 / 116b43a2 | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 58 | 4(g) OLS Assumption Violations and Implications | Unchanged; outputs and metadata preserved |
| 49 / eeac47ac | code | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 59 | 4(g) OLS Assumption Violations and Implications | Unchanged; outputs and metadata preserved |
| 50 / ce4cd411 | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 60 | 4(g) OLS Assumption Violations and Implications | Unchanged; outputs and metadata preserved |
| 51 / 2f2f33b3 | markdown | [04_diagnostics_robustness.ipynb](../notebooks/04_diagnostics_robustness.ipynb) / 61 | 4(g) OLS Assumption Violations and Implications | Unchanged; outputs and metadata preserved |
| 47 / 118c31ff | markdown | [06_limitations_extensions.ipynb](../notebooks/06_limitations_extensions.ipynb) / 8 | 6(d) Concrete Future Research Extensions | Processing plan duplicated verbatim; remains a plan, not an implemented result; outputs and metadata preserved |

## Original 08_results.ipynb

| Index / original ID | Type | Destination / cell | Heading | Change / preservation |
|---|---|---|---|---|
| 0 / 10527e60 | markdown | [01_economic_theory.ipynb](../notebooks/01_economic_theory.ipynb) / 4 | 1(b) Relevant Economic Theory and Academic Literature | Unchanged; outputs and metadata preserved |
| 1 / 38732e16 | code | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 29 | 2(d) Q-Q Plots and Density Plots | Moved EDA addition; code variable names prefixed results_ to isolate original results sample; outputs unchanged; outputs and metadata preserved |
| 3 / 8471695d | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 30 | 2(d) Q-Q Plots and Density Plots | Moved EDA addition; code variable names prefixed results_ to isolate original results sample; outputs unchanged; outputs and metadata preserved |
| 4 / 1eec94c0 | code | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 31 | 2(d) Q-Q Plots and Density Plots | Moved EDA addition; code variable names prefixed results_ to isolate original results sample; outputs unchanged; outputs and metadata preserved |
| 5 / 916b34da | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 32 | 2(d) Q-Q Plots and Density Plots | Moved EDA addition; code variable names prefixed results_ to isolate original results sample; outputs unchanged; outputs and metadata preserved |
| 6 / 14b4c20f | code | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 33 | 2(d) Q-Q Plots and Density Plots | Moved EDA addition; code variable names prefixed results_ to isolate original results sample; outputs unchanged; outputs and metadata preserved |
| 7 / d0eee2e9 | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 34 | 2(d) Q-Q Plots and Density Plots | Moved EDA addition; code variable names prefixed results_ to isolate original results sample; outputs unchanged; outputs and metadata preserved |
| 9 / 8684f268 | code | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 50 | 2(g) Missing Values, Imputation Decisions, and Sensitivity Analysis | Identifier namespace only; same calculations, sample, models and outputs; outputs and metadata preserved |
| 8 / 77ed570a | code | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 52 | 2(h) Pandas Profiling Analysis and Findings | Identifier namespace only; same calculations, sample, models and outputs; outputs and metadata preserved |
| 10 / bf2d5143 | markdown | [02_data_description_eda.ipynb](../notebooks/02_data_description_eda.ipynb) / 53 | 2(h) Pandas Profiling Analysis and Findings | Identifier namespace only; same calculations, sample, models and outputs; outputs and metadata preserved |
| 11 / a5237489 | markdown | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 60 | 3(f) Final Model Selection and Justification | Unchanged; outputs and metadata preserved |
| 12 / ae528018 | code | [03_variable_selection_models.ipynb](../notebooks/03_variable_selection_models.ipynb) / 61 | 3(f) Final Model Selection and Justification | Unchanged; outputs and metadata preserved |
| 1 / 38732e16 | code | [05_results_interpretation.ipynb](../notebooks/05_results_interpretation.ipynb) / 2 | Introduction | Unchanged; outputs and metadata preserved |
| 2 / 9ae6683e | markdown | [05_results_interpretation.ipynb](../notebooks/05_results_interpretation.ipynb) / 3 | Introduction | Unchanged; outputs and metadata preserved |
| 13 / 8321a5b2 | markdown | [05_results_interpretation.ipynb](../notebooks/05_results_interpretation.ipynb) / 5 | 5(a) Professional Final Regression Table | Unchanged; outputs and metadata preserved |
| 14 / cfff877f | code | [05_results_interpretation.ipynb](../notebooks/05_results_interpretation.ipynb) / 6 | 5(a) Professional Final Regression Table | Unchanged; outputs and metadata preserved |
| 15 / c4e6e4ff | markdown | [05_results_interpretation.ipynb](../notebooks/05_results_interpretation.ipynb) / 8 | 5(b) Economic Interpretation of All Coefficients | Unchanged; outputs and metadata preserved |
| 16 / 92b8bfd6 | code | [05_results_interpretation.ipynb](../notebooks/05_results_interpretation.ipynb) / 9 | 5(b) Economic Interpretation of All Coefficients | Unchanged; outputs and metadata preserved |
| 17 / fc808a98 | markdown | [05_results_interpretation.ipynb](../notebooks/05_results_interpretation.ipynb) / 15 | 5(e) R² and Model Fit in Economic Context | Unchanged; outputs and metadata preserved |
| 18 / bb66ad45 | code | [05_results_interpretation.ipynb](../notebooks/05_results_interpretation.ipynb) / 16 | 5(e) R² and Model Fit in Economic Context | Unchanged; outputs and metadata preserved |
| 19 / 0a9e64b9 | markdown | [05_results_interpretation.ipynb](../notebooks/05_results_interpretation.ipynb) / 17 | 5(e) R² and Model Fit in Economic Context | Unchanged; outputs and metadata preserved |
| 20 / a42717fb | markdown | [05_results_interpretation.ipynb](../notebooks/05_results_interpretation.ipynb) / 19 | 5(e) R² and Model Fit in Economic Context | Unchanged; outputs and metadata preserved |
| 21 / 64894bec | code | [05_results_interpretation.ipynb](../notebooks/05_results_interpretation.ipynb) / 20 | 5(e) R² and Model Fit in Economic Context | Unchanged; outputs and metadata preserved |
| 22 / 19a909ca | markdown | [05_results_interpretation.ipynb](../notebooks/05_results_interpretation.ipynb) / 21 | 5(e) R² and Model Fit in Economic Context | Unchanged; outputs and metadata preserved |
| 23 / ee68ab76 | markdown | [05_results_interpretation.ipynb](../notebooks/05_results_interpretation.ipynb) / 22 | 5(e) R² and Model Fit in Economic Context | Unchanged; outputs and metadata preserved |
| 24 / 8ca38864 | code | [05_results_interpretation.ipynb](../notebooks/05_results_interpretation.ipynb) / 23 | 5(e) R² and Model Fit in Economic Context | Unchanged; outputs and metadata preserved |
| 25 / 8e56627e | markdown | [05_results_interpretation.ipynb](../notebooks/05_results_interpretation.ipynb) / 24 | 5(e) R² and Model Fit in Economic Context | Unchanged; outputs and metadata preserved |
| 27 / f05fa41d | markdown | [05_results_interpretation.ipynb](../notebooks/05_results_interpretation.ipynb) / 26 | 5(e) R² and Model Fit in Economic Context | Unchanged; outputs and metadata preserved |
| 28 / 8b56b711 | markdown | [05_results_interpretation.ipynb](../notebooks/05_results_interpretation.ipynb) / 27 | 5(e) R² and Model Fit in Economic Context | Unchanged; outputs and metadata preserved |
| 26 / bcd62006 | markdown | [06_limitations_extensions.ipynb](../notebooks/06_limitations_extensions.ipynb) / 2 | 6(a) Key Data, Methodological, and Scope Limitations | Unchanged; outputs and metadata preserved |
| 27 / f05fa41d | markdown | [06_limitations_extensions.ipynb](../notebooks/06_limitations_extensions.ipynb) / 6 | 6(c) Policy Implications | Conclusion duplicated verbatim for policy and application context; outputs and metadata preserved |

## Validation boundary

See [validation summary](notebook_validation_summary.md). Byte-identical saved outputs establish preservation, not fresh reproducibility.
