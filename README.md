# Los Angeles street parking — UCLA ECON 430

Research question: **What factors explain street-parking occupancy/availability in Los Angeles?**

This project collects raw sources for a future cross-sectional OLS assignment (500+ usable observations, at least five potential predictors) and a later parking-prediction prototype. **No cleaning, transformation, imputation, filtering of downloaded observations, merging, feature engineering, EDA or modeling has been performed.** Counts, schemas, timestamp extents and checksums are acquisition checks only.

The primary historical source is one complete LADOT August 2025 sensor-transaction attachment, paired with available 2025 NOAA station files. LADOT current occupancy and meter inventory are separate snapshots. Additional originals cover restrictions, zoning, ACS tract characteristics, business locations, events and transit. Source-period and geography requests define acquisition scope; raw files retain all returned rows, columns, missing values and timestamp strings.

See [source catalog and acquisition report](docs/data_sources.md), [raw dictionary](docs/data_dictionary_raw.md), [machine-readable audit](docs/acquisition_audit.json), and [HTTP retrieval manifests](docs/retrievals/). The catalog records exact file paths, URLs, dates, counts, licenses, limitations, access requirements and rejected sources. Sources differ in vintage and coverage; having many sensor events does not establish a usable cross-section yet.

The [raw-data design-validation audit](docs/design_validation_audit.md) preserves the later read-only validation findings and its overall **YELLOW** assessment. Use [cleaning_decisions.md](docs/cleaning_decisions.md) to record your own methodological decisions; its sections are intentionally blank. The saved audit identifies questions, not cleaning rules or analytical results.

The notebooks contain only a title, purpose description, and an empty code cell. You will write the cleaning and econometric analysis yourself, following this workflow:

```text
Raw Data f
↓
01 Clean Occupancy
↓
02 Clean Meter Inventory
↓
03 Build Cross-Section
↓
04 EDA
↓
05 Variable Selection
↓
06 Regression Models
↓
07 Diagnostics
↓
08 Results
```

Folder roles:

- `data/raw/`: untouched original source data and provider metadata.
- `data/interim/`: intermediate cleaned/derived files from future work; currently empty.
- `data/processed/`: final analysis-ready datasets from future work; currently empty.
- `notebooks/`: student-written analysis workflow; currently notebook shells without analysis code.
- `src/data_collection/`: existing acquisition scripts.
- `src/cleaning/`, `src/features/`, `src/modeling/`: empty placeholders for future student-written helpers.
- `reports/figures/`: final generated figures; currently empty.
- `reports/tables/`: final generated tables; currently empty.
- `docs/`: data sources, audit information, and methodological decisions.

```text
data/raw/{ladot_occupancy,ladot_meters,parking_regulations,land_use,census,
          points_of_interest,events,weather,other}/<UTC retrieval stamp>/
data/interim/               # empty
data/processed/             # empty
notebooks/
src/data_collection/
src/cleaning/
src/features/
src/modeling/
reports/figures/
reports/tables/
docs/
```

Everything under `data/raw/` is an original downloaded response body or source archive, including provider metadata. Project-generated manifests, dictionaries and audits are under `docs/`. Downloaded ZIPs remain unextracted. Raw files are never overwritten: each execution uses new retrieval directories. The initial stale Metro GitHub archive remains preserved and labeled in the catalog; current Metro GitLab data are saved separately.

For a future local notebook environment, install the packages listed in `requirements.txt` and launch JupyterLab from this project directory. No packages were installed during workspace setup:

```bash
python3 -m pip install -r requirements.txt
python3 -m jupyterlab
```

The existing acquisition workflow can be rerun separately if needed. These commands download new snapshots and regenerate acquisition documentation; they are not required to begin writing the notebooks:

```bash
python3 src/data_collection/collect.py --month 2025_08
python3 src/data_collection/audit.py
python3 src/data_collection/document.py
```

The collector inspects response sizes, enforces a 600 MB per-file cap, uses full Socrata exports and saves all zoning pages without merging them. It needs network access and about 820 MB of disk space per collection. The LADOT archive rolls forward; a removed month cannot be reproduced from the live portal, so preserve these originals and hashes. Live snapshots change on rerun. A failed download exits with an error and is recorded in the manifest; successful originals remain intact. `supplement.py` records the corrected NOAA manual and current Metro feed used during initial acquisition; the main collector already uses those corrected URLs. `retry_zoning.py` recovered four initial failed 5,000-feature pages as smaller disjoint pages. The main collector now uses smaller pages. The audit compares all 58,952 zoning record IDs against the independent source ID listing, including the source's repeated IDs (58,855 distinct IDs). No deduplication was performed. `zoning_source_ids.py` saved that independent listing during the initial acquisition; the main collector also downloads it.

No credentials are required for the collected sources. Direct Census API access and Ticketmaster expansion require personal API keys; instructions and coverage gaps are in the catalog. Future analysis, cleaning, date/time conversion, cross-section construction and statistical modeling are deliberately deferred.
