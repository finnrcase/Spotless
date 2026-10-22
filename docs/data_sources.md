# Raw data sources and acquisition report

Acquisition only. No cleaning, transformation, imputation, observation removal, merging, feature engineering, EDA, statistical models, or prediction models were performed. Record counts, timestamp extents, schema inspection and hashes below are read-only acquisition checks.

Retrieval occurred October 16, 2026 in America/Los_Angeles (October 17 UTC). Every original is in a unique UTC-stamped directory. Exact request parameters, final URLs, HTTP response dates/Last-Modified headers, sizes, SHA-256 hashes and failures are in [retrieval manifests](retrievals/) and [acquisition_audit.json](acquisition_audit.json). Files are source response bodies; documentation and audit JSON are project-generated provenance.

One entire historical month was selected before download; this is a source-period choice, not filtering a downloaded dataset. HEAD checks and streamed byte caps prevented unexpected huge downloads. No source export used a row cap or observation filter; zoning uses where=1=1 and full pagination. Census geographic/table requests and the MLB team/month request define the acquisition scope. Raw values, headers and timestamp strings are unchanged.

## ladot_occupancy

- Provider: City of Los Angeles / LADOT
- Geographic coverage: Sensor-equipped metered street spaces in LA; not all curb parking.
- Eventual variables: Outcome: recorded occupancy state; timestamps and space IDs support later cross-sectional construction.
- Limitations: Historical file: complete August 2025 attachment, chosen for overlap with available legacy NOAA weather. Raw UTC-labelled timestamp span is 8/1/2025 7:00:01 AM through 9/1/2025 6:59:59 AM, so attachment month is not a strict UTC calendar-month boundary. No rows selected or removed. Current feed is a separate retrieval snapshot, not a historical panel. Event records are state changes, not evenly spaced availability observations; unknown states, stale sensors, missing baselines, and sensor coverage require later review. Repeated events do not count as independent cross-sectional units.
- License / usage: Socrata licenseId PUBLIC_DOMAIN. Archive table is empty: real historical records are in metadata attachments. rowsUpdatedAt on the archive table is not the monthly attachment update date; viewLastModified and attachment listing are preserved.

| Original file (relative to project root) | Format | Bytes | Records | Date coverage |
|---|---|---:|---:|---|
| [data/raw/ladot_occupancy/20261017T052111914317Z/archive_metadata.json](../data/raw/ladot_occupancy/20261017T052111914317Z/archive_metadata.json) | json | 11,410 | n/a (metadata/documentation) | Snapshot / not stated; see limitations |
| [data/raw/ladot_occupancy/20261017T052111914317Z/current_metadata.json](../data/raw/ladot_occupancy/20261017T052111914317Z/current_metadata.json) | json | 8,624 | n/a (metadata/documentation) | Snapshot / not stated; see limitations |
| [data/raw/ladot_occupancy/20261017T052111914317Z/current.csv](../data/raw/ladot_occupancy/20261017T052111914317Z/current.csv) | csv | 147,490 | 3909 | 10/02/2026 08:44:59 AM to 10/17/2026 05:19:59 AM |
| [data/raw/ladot_occupancy/20261017T052111914317Z/Sensor Transactions_2025_08.csv](../data/raw/ladot_occupancy/20261017T052111914317Z/Sensor%20Transactions_2025_08.csv) | csv | 241,918,438 | 3707820 | 8/1/2025 7:00:01 AM to 9/1/2025 6:59:59 AM |

Exact endpoints and retrieval dates:

- `archive_metadata.json`: [https://data.lacity.org/api/views/cj8s-ivry.json](https://data.lacity.org/api/views/cj8s-ivry.json); retrieved `2026-10-17T05:21:11.914673+00:00`.
- `current_metadata.json`: [https://data.lacity.org/api/views/e7h6-4a3e.json](https://data.lacity.org/api/views/e7h6-4a3e.json); retrieved `2026-10-17T05:21:12.770131+00:00`.
- `current.csv`: [https://data.lacity.org/api/views/e7h6-4a3e/rows.csv?accessType=DOWNLOAD](https://data.lacity.org/api/views/e7h6-4a3e/rows.csv?accessType=DOWNLOAD); retrieved `2026-10-17T05:21:18.399343+00:00`.
  Acquisition count: 3,909 distinct source space IDs; usability has not been assessed.
- `Sensor Transactions_2025_08.csv`: [https://data.lacity.org/api/views/cj8s-ivry/files/180f7617-dcf4-467c-b151-1e4710c7daf0?download=true&filename=Sensor+Transactions_2025_08.csv](https://data.lacity.org/api/views/cj8s-ivry/files/180f7617-dcf4-467c-b151-1e4710c7daf0?download=true&filename=Sensor+Transactions_2025_08.csv); retrieved `2026-10-17T05:21:18.399112+00:00`.
  Acquisition count: 4,905 distinct source space IDs; usability has not been assessed.

- `archive_metadata.json` provider timestamps (UTC): rowsUpdatedAt = 2019-10-04T00:14:20+00:00; viewLastModified = 2026-09-29T15:52:28+00:00.
- `current_metadata.json` provider timestamps (UTC): rowsUpdatedAt = 2026-10-17T05:20:54+00:00; viewLastModified = 2022-03-01T18:46:09+00:00.
## ladot_meters

- Provider: City of Los Angeles / LADOT
- Geographic coverage: All on-street metered spaces in published inventory.
- Eventual variables: Potential predictors: RateRange, RateType, MeteredTimeLimit, MeterType, location and block face.
- Limitations: Seven published columns only. Description mentions operating hours and restrictions, but those columns are absent. No separate numeric price, zone, exact address, or historical effective dates are provided. RateRange can describe variable tariffs; no numeric parsing performed. Current inventory may differ from August 2025.
- License / usage: Socrata licenseId PUBLIC_DOMAIN.

| Original file (relative to project root) | Format | Bytes | Records | Date coverage |
|---|---|---:|---:|---|
| [data/raw/ladot_meters/20261017T052111914317Z/inventory_metadata.json](../data/raw/ladot_meters/20261017T052111914317Z/inventory_metadata.json) | json | 16,870 | n/a (metadata/documentation) | Snapshot / not stated; see limitations |
| [data/raw/ladot_meters/20261017T052111914317Z/inventory.csv](../data/raw/ladot_meters/20261017T052111914317Z/inventory.csv) | csv | 2,777,557 | 35022 | Snapshot / not stated; see limitations |

Exact endpoints and retrieval dates:

- `inventory_metadata.json`: [https://data.lacity.org/api/views/s49e-q6j2.json](https://data.lacity.org/api/views/s49e-q6j2.json); retrieved `2026-10-17T05:21:13.626094+00:00`.
- `inventory.csv`: [https://data.lacity.org/api/views/s49e-q6j2/rows.csv?accessType=DOWNLOAD](https://data.lacity.org/api/views/s49e-q6j2/rows.csv?accessType=DOWNLOAD); retrieved `2026-10-17T05:21:18.402744+00:00`.

- `inventory_metadata.json` provider timestamps (UTC): rowsUpdatedAt = 2026-10-16T13:30:43+00:00; viewLastModified = 2023-03-21T19:39:47+00:00.
## parking_regulations

- Provider: City of Los Angeles / LADOT and Bureau of Street Services
- Geographic coverage: Published LA posted sweeping routes, permit districts and calendar sign block faces.
- Eventual variables: Possible future sweeping time, permit district and sign-location predictors; inventory also supplies metered time limits.
- Limitations: Sweeping table rowsUpdatedAt is 2014; permit districts 2015; calendar sign locations 2019. These are legacy sources, not verified current or August 2025 rules. Sweeping boundaries are text, not street-segment geometry; no explicit weekday column. Calendar signs describe installation, not sign rules. No complete citywide no-parking-period/curb-regulation inventory was verified. Do not infer restriction schedules from sign locations.
- License / usage: Sweeping and permit datasets: CC0_10; calendar sign locations: PUBLIC_DOMAIN, per saved metadata.

| Original file (relative to project root) | Format | Bytes | Records | Date coverage |
|---|---|---:|---:|---|
| [data/raw/parking_regulations/20261017T052111914317Z/street_sweeping_metadata.json](../data/raw/parking_regulations/20261017T052111914317Z/street_sweeping_metadata.json) | json | 14,939 | n/a (metadata/documentation) | Snapshot / not stated; see limitations |
| [data/raw/parking_regulations/20261017T052111914317Z/permit_districts_metadata.json](../data/raw/parking_regulations/20261017T052111914317Z/permit_districts_metadata.json) | json | 7,297 | n/a (metadata/documentation) | Snapshot / not stated; see limitations |
| [data/raw/parking_regulations/20261017T052111914317Z/calendar_sign_locations_metadata.json](../data/raw/parking_regulations/20261017T052111914317Z/calendar_sign_locations_metadata.json) | json | 6,934 | n/a (metadata/documentation) | Snapshot / not stated; see limitations |
| [data/raw/parking_regulations/20261017T052111914317Z/street_sweeping.csv](../data/raw/parking_regulations/20261017T052111914317Z/street_sweeping.csv) | csv | 73,161 | 864 | Snapshot / not stated; see limitations |
| [data/raw/parking_regulations/20261017T052111914317Z/permit_districts.csv](../data/raw/parking_regulations/20261017T052111914317Z/permit_districts.csv) | csv | 824,768 | 155 | Snapshot / not stated; see limitations |
| [data/raw/parking_regulations/20261017T052111914317Z/calendar_sign_locations.csv](../data/raw/parking_regulations/20261017T052111914317Z/calendar_sign_locations.csv) | csv | 43,240 | 139 | Snapshot / not stated; see limitations |

Exact endpoints and retrieval dates:

- `street_sweeping_metadata.json`: [https://data.lacity.org/api/views/krk7-ayq2.json](https://data.lacity.org/api/views/krk7-ayq2.json); retrieved `2026-10-17T05:21:14.746512+00:00`.
- `permit_districts_metadata.json`: [https://data.lacity.org/api/views/s3st-6nwi.json](https://data.lacity.org/api/views/s3st-6nwi.json); retrieved `2026-10-17T05:21:15.727137+00:00`.
- `calendar_sign_locations_metadata.json`: [https://data.lacity.org/api/views/jp2s-nfz4.json](https://data.lacity.org/api/views/jp2s-nfz4.json); retrieved `2026-10-17T05:21:16.631842+00:00`.
- `street_sweeping.csv`: [https://data.lacity.org/api/views/krk7-ayq2/rows.csv?accessType=DOWNLOAD](https://data.lacity.org/api/views/krk7-ayq2/rows.csv?accessType=DOWNLOAD); retrieved `2026-10-17T05:21:18.403872+00:00`.
- `permit_districts.csv`: [https://data.lacity.org/api/views/s3st-6nwi/rows.csv?accessType=DOWNLOAD](https://data.lacity.org/api/views/s3st-6nwi/rows.csv?accessType=DOWNLOAD); retrieved `2026-10-17T05:21:18.404356+00:00`.
- `calendar_sign_locations.csv`: [https://data.lacity.org/api/views/jp2s-nfz4/rows.csv?accessType=DOWNLOAD](https://data.lacity.org/api/views/jp2s-nfz4/rows.csv?accessType=DOWNLOAD); retrieved `2026-10-17T05:21:19.846900+00:00`.

- `street_sweeping_metadata.json` provider timestamps (UTC): rowsUpdatedAt = 2014-05-28T23:03:43+00:00; viewLastModified = 2020-11-30T17:19:52+00:00.
- `permit_districts_metadata.json` provider timestamps (UTC): rowsUpdatedAt = 2015-08-13T13:17:55+00:00; viewLastModified = 2024-04-10T19:09:19+00:00.
- `calendar_sign_locations_metadata.json` provider timestamps (UTC): rowsUpdatedAt = 2019-09-05T22:08:49+00:00; viewLastModified = 2020-11-30T17:17:32+00:00.
## land_use

- Provider: City of Los Angeles / City Planning via NavigateLA
- Geographic coverage: Entire Generalized Zoning layer, 58,952 features at acquisition.
- Eventual variables: Potential residential/commercial/industrial zoning and neighborhood land-use classification predictors.
- Limitations: Zoning is a legal designation, not observed current land use. All features and all attributes requested, no geographic clipping. Pagination uses OBJECTID order, pages saved separately. Server default geometry CRS is EPSG:3857 in responses; layer source metadata lists EPSG:2229. No client reprojection. Concurrent server edits can affect pagination. No verified layer update date or historical effective-date coverage. The provider itself returns repeated OBJECTID values: 58,952 records and 58,855 distinct IDs. The audit compares the complete multiset of IDs with the independently downloaded source ID listing; duplicates are retained.
- License / usage: Publicly accessible City service; copyrightText is blank and no explicit reuse license in layer metadata. Do not assume CC0; confirm City GIS terms before redistribution.

| Original file (relative to project root) | Format | Bytes | Records | Date coverage |
|---|---|---:|---:|---|
| [data/raw/land_use/20261017T052111914317Z/zoning_metadata.json](../data/raw/land_use/20261017T052111914317Z/zoning_metadata.json) | json | 11,641 | n/a (metadata/documentation) | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052111914317Z/zoning_count.json](../data/raw/land_use/20261017T052111914317Z/zoning_count.json) | json | 15 | n/a (metadata/documentation) | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052111914317Z/zoning_offset_000000.json](../data/raw/land_use/20261017T052111914317Z/zoning_offset_000000.json) | json | 15,604,793 | 5000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052111914317Z/zoning_offset_005000.json](../data/raw/land_use/20261017T052111914317Z/zoning_offset_005000.json) | json | 15,789,056 | 5000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052111914317Z/zoning_offset_010000.json](../data/raw/land_use/20261017T052111914317Z/zoning_offset_010000.json) | json | 18,915,074 | 5000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052111914317Z/zoning_offset_015000.json](../data/raw/land_use/20261017T052111914317Z/zoning_offset_015000.json) | json | 30,025,124 | 5000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052111914317Z/zoning_offset_030000.json](../data/raw/land_use/20261017T052111914317Z/zoning_offset_030000.json) | json | 18,735,854 | 5000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052111914317Z/zoning_offset_035000.json](../data/raw/land_use/20261017T052111914317Z/zoning_offset_035000.json) | json | 32,623,896 | 5000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052111914317Z/zoning_offset_050000.json](../data/raw/land_use/20261017T052111914317Z/zoning_offset_050000.json) | json | 28,532,991 | 5000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052111914317Z/zoning_offset_055000.json](../data/raw/land_use/20261017T052111914317Z/zoning_offset_055000.json) | json | 15,812,425 | 3952 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052508603880Z/zoning_offset_020000_count_1000.json](../data/raw/land_use/20261017T052508603880Z/zoning_offset_020000_count_1000.json) | json | 9,213,095 | 1000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052508603880Z/zoning_offset_021000_count_1000.json](../data/raw/land_use/20261017T052508603880Z/zoning_offset_021000_count_1000.json) | json | 15,200,997 | 1000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052508603880Z/zoning_offset_022000_count_1000.json](../data/raw/land_use/20261017T052508603880Z/zoning_offset_022000_count_1000.json) | json | 16,790,394 | 1000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052508603880Z/zoning_offset_023000_count_1000.json](../data/raw/land_use/20261017T052508603880Z/zoning_offset_023000_count_1000.json) | json | 11,406,843 | 1000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052508603880Z/zoning_offset_024000_count_1000.json](../data/raw/land_use/20261017T052508603880Z/zoning_offset_024000_count_1000.json) | json | 9,594,910 | 1000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052508603880Z/zoning_offset_025000_count_1000.json](../data/raw/land_use/20261017T052508603880Z/zoning_offset_025000_count_1000.json) | json | 13,755,958 | 1000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052508603880Z/zoning_offset_026000_count_1000.json](../data/raw/land_use/20261017T052508603880Z/zoning_offset_026000_count_1000.json) | json | 10,546,118 | 1000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052508603880Z/zoning_offset_027000_count_1000.json](../data/raw/land_use/20261017T052508603880Z/zoning_offset_027000_count_1000.json) | json | 5,489,085 | 1000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052508603880Z/zoning_offset_028000_count_1000.json](../data/raw/land_use/20261017T052508603880Z/zoning_offset_028000_count_1000.json) | json | 7,369,611 | 1000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052508603880Z/zoning_offset_029000_count_1000.json](../data/raw/land_use/20261017T052508603880Z/zoning_offset_029000_count_1000.json) | json | 3,959,779 | 1000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052508603880Z/zoning_offset_040000_count_1000.json](../data/raw/land_use/20261017T052508603880Z/zoning_offset_040000_count_1000.json) | json | 9,378,229 | 1000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052508603880Z/zoning_offset_041000_count_1000.json](../data/raw/land_use/20261017T052508603880Z/zoning_offset_041000_count_1000.json) | json | 8,163,207 | 1000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052508603880Z/zoning_offset_042000_count_1000.json](../data/raw/land_use/20261017T052508603880Z/zoning_offset_042000_count_1000.json) | json | 22,634,605 | 1000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052508603880Z/zoning_offset_043000_count_1000.json](../data/raw/land_use/20261017T052508603880Z/zoning_offset_043000_count_1000.json) | json | 29,547,124 | 1000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052508603880Z/zoning_offset_044000_count_1000.json](../data/raw/land_use/20261017T052508603880Z/zoning_offset_044000_count_1000.json) | json | 17,272,567 | 1000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052508603880Z/zoning_offset_045000_count_1000.json](../data/raw/land_use/20261017T052508603880Z/zoning_offset_045000_count_1000.json) | json | 18,924,404 | 1000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052508603880Z/zoning_offset_046000_count_1000.json](../data/raw/land_use/20261017T052508603880Z/zoning_offset_046000_count_1000.json) | json | 13,066,766 | 1000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052508603880Z/zoning_offset_047000_count_1000.json](../data/raw/land_use/20261017T052508603880Z/zoning_offset_047000_count_1000.json) | json | 6,139,067 | 1000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052508603880Z/zoning_offset_048000_count_1000.json](../data/raw/land_use/20261017T052508603880Z/zoning_offset_048000_count_1000.json) | json | 5,320,561 | 1000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052508603880Z/zoning_offset_049000_count_1000.json](../data/raw/land_use/20261017T052508603880Z/zoning_offset_049000_count_1000.json) | json | 7,074,054 | 1000 | Snapshot / not stated; see limitations |
| [data/raw/land_use/20261017T052654015392Z/zoning_source_ids.json](../data/raw/land_use/20261017T052654015392Z/zoning_source_ids.json) | json | 342,637 | n/a (metadata/documentation) | Snapshot / not stated; see limitations |

Exact endpoints and retrieval dates:

- `zoning_metadata.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75?f=pjson](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75?f=pjson); retrieved `2026-10-17T05:22:14.646886+00:00`.
- `zoning_count.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&returnCountOnly=true](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&returnCountOnly=true); retrieved `2026-10-17T05:22:15.008469+00:00`.
- `zoning_offset_000000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=0&resultRecordCount=5000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=0&resultRecordCount=5000); retrieved `2026-10-17T05:22:36.807663+00:00`.
- `zoning_offset_005000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=5000&resultRecordCount=5000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=5000&resultRecordCount=5000); retrieved `2026-10-17T05:22:36.808747+00:00`.
- `zoning_offset_010000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=10000&resultRecordCount=5000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=10000&resultRecordCount=5000); retrieved `2026-10-17T05:22:36.808410+00:00`.
- `zoning_offset_015000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=15000&resultRecordCount=5000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=15000&resultRecordCount=5000); retrieved `2026-10-17T05:22:47.916925+00:00`.
- `zoning_offset_030000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=30000&resultRecordCount=5000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=30000&resultRecordCount=5000); retrieved `2026-10-17T05:23:06.504952+00:00`.
- `zoning_offset_035000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=35000&resultRecordCount=5000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=35000&resultRecordCount=5000); retrieved `2026-10-17T05:23:18.417217+00:00`.
- `zoning_offset_050000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=50000&resultRecordCount=5000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=50000&resultRecordCount=5000); retrieved `2026-10-17T05:23:52.020867+00:00`.
- `zoning_offset_055000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=55000&resultRecordCount=5000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=55000&resultRecordCount=5000); retrieved `2026-10-17T05:24:09.492316+00:00`.
- `zoning_offset_020000_count_1000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=20000&resultRecordCount=1000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=20000&resultRecordCount=1000); retrieved `2026-10-17T05:25:08.604397+00:00`.
- `zoning_offset_021000_count_1000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=21000&resultRecordCount=1000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=21000&resultRecordCount=1000); retrieved `2026-10-17T05:25:08.604527+00:00`.
- `zoning_offset_022000_count_1000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=22000&resultRecordCount=1000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=22000&resultRecordCount=1000); retrieved `2026-10-17T05:25:08.604632+00:00`.
- `zoning_offset_023000_count_1000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=23000&resultRecordCount=1000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=23000&resultRecordCount=1000); retrieved `2026-10-17T05:25:16.379642+00:00`.
- `zoning_offset_024000_count_1000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=24000&resultRecordCount=1000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=24000&resultRecordCount=1000); retrieved `2026-10-17T05:25:16.380018+00:00`.
- `zoning_offset_025000_count_1000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=25000&resultRecordCount=1000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=25000&resultRecordCount=1000); retrieved `2026-10-17T05:25:16.392231+00:00`.
- `zoning_offset_026000_count_1000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=26000&resultRecordCount=1000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=26000&resultRecordCount=1000); retrieved `2026-10-17T05:25:19.599168+00:00`.
- `zoning_offset_027000_count_1000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=27000&resultRecordCount=1000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=27000&resultRecordCount=1000); retrieved `2026-10-17T05:25:20.497355+00:00`.
- `zoning_offset_028000_count_1000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=28000&resultRecordCount=1000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=28000&resultRecordCount=1000); retrieved `2026-10-17T05:25:20.886506+00:00`.
- `zoning_offset_029000_count_1000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=29000&resultRecordCount=1000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=29000&resultRecordCount=1000); retrieved `2026-10-17T05:25:22.439984+00:00`.
- `zoning_offset_040000_count_1000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=40000&resultRecordCount=1000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=40000&resultRecordCount=1000); retrieved `2026-10-17T05:25:23.232363+00:00`.
- `zoning_offset_041000_count_1000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=41000&resultRecordCount=1000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=41000&resultRecordCount=1000); retrieved `2026-10-17T05:25:24.193065+00:00`.
- `zoning_offset_042000_count_1000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=42000&resultRecordCount=1000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=42000&resultRecordCount=1000); retrieved `2026-10-17T05:25:25.721727+00:00`.
- `zoning_offset_043000_count_1000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=43000&resultRecordCount=1000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=43000&resultRecordCount=1000); retrieved `2026-10-17T05:25:27.251568+00:00`.
- `zoning_offset_044000_count_1000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=44000&resultRecordCount=1000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=44000&resultRecordCount=1000); retrieved `2026-10-17T05:25:30.191153+00:00`.
- `zoning_offset_045000_count_1000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=45000&resultRecordCount=1000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=45000&resultRecordCount=1000); retrieved `2026-10-17T05:25:33.066129+00:00`.
- `zoning_offset_046000_count_1000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=46000&resultRecordCount=1000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=46000&resultRecordCount=1000); retrieved `2026-10-17T05:25:35.270512+00:00`.
- `zoning_offset_047000_count_1000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=47000&resultRecordCount=1000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=47000&resultRecordCount=1000); retrieved `2026-10-17T05:25:35.750956+00:00`.
- `zoning_offset_048000_count_1000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=48000&resultRecordCount=1000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=48000&resultRecordCount=1000); retrieved `2026-10-17T05:25:38.030234+00:00`.
- `zoning_offset_049000_count_1000.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=49000&resultRecordCount=1000](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=49000&resultRecordCount=1000); retrieved `2026-10-17T05:25:40.096760+00:00`.
- `zoning_source_ids.json`: [https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&returnIdsOnly=true](https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&returnIdsOnly=true); retrieved `2026-10-17T05:26:56.285328+00:00`.

## census

- Provider: U.S. Census Bureau; ACS delivered through Census Reporter public API
- Geographic coverage: ACS: all LA County census tracts requested; Gazetteer: entire California tract file.
- Eventual variables: ACS population, housing units, household income, journey-to-work mode estimates and margins of error; Gazetteer land area and tract identifiers can support later density measures.
- Limitations: ACS2024_5yr is a 2020–2024 survey period, not August 2025 conditions. County contains areas outside LA city. Census Reporter is a third-party delivery service; raw response includes release/table metadata. Census direct API redirected to missing_key.html; no credentials fabricated. Gazetteer contains area and internal points, not tract boundaries or population. No density, geographic joins or commuting shares calculated.
- License / usage: Census federal statistical data are public; cite Census and Census Reporter delivery. API response contains no separate explicit license grant; no blanket license inferred for service code or other website material.

| Original file (relative to project root) | Format | Bytes | Records | Date coverage |
|---|---|---:|---:|---|
| [data/raw/census/20261017T052111914317Z/2024_gaz_tracts_06.txt](../data/raw/census/20261017T052111914317Z/2024_gaz_tracts_06.txt) | txt | 1,835,120 | 9129 | ACS 2020–2024; geography vintage 2024 |
| [data/raw/census/20261017T052111914317Z/acs2024_5yr_la_county_tracts.json](../data/raw/census/20261017T052111914317Z/acs2024_5yr_la_county_tracts.json) | json | 2,720,939 | 2498 | ACS 2020–2024; geography vintage 2024 |

Exact endpoints and retrieval dates:

- `2024_gaz_tracts_06.txt`: [https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2024_Gazetteer/2024_gaz_tracts_06.txt](https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2024_Gazetteer/2024_gaz_tracts_06.txt); retrieved `2026-10-17T05:21:21.671800+00:00`.
- `acs2024_5yr_la_county_tracts.json`: [https://api.censusreporter.org/1.0/data/show/acs2024_5yr?table_ids=B01003%2CB25001%2CB19013%2CB08301&geo_ids=140%7C05000US06037](https://api.censusreporter.org/1.0/data/show/acs2024_5yr?table_ids=B01003%2CB25001%2CB19013%2CB08301&geo_ids=140%7C05000US06037); retrieved `2026-10-17T05:21:21.936270+00:00`.

## points_of_interest

- Provider: City of Los Angeles / Office of Finance
- Geographic coverage: Full published Listing of Active Businesses, including registered locations outside LA.
- Eventual variables: NAICS and location fields could support later restaurant, retail, entertainment and business counts.
- Limitations: Full source export retained, including blanks and businesses outside city limits. Active means no reported cessation; not independently verified open establishments. NAICS are self-reported and source description references 2007 codes; entries are not necessarily distinct physical destinations. Snapshot is October 2026, not a complete historical August 2025 business census. Schools/universities are not exhaustively covered. OSM was considered but not downloaded because this official full business registry provides a reproducible POI starting point without a second overlapping snapshot.
- License / usage: Socrata licenseId CC0_10. Contains public business names and addresses; no Google Maps scraping.

| Original file (relative to project root) | Format | Bytes | Records | Date coverage |
|---|---|---:|---:|---|
| [data/raw/points_of_interest/20261017T052111914317Z/active_businesses_metadata.json](../data/raw/points_of_interest/20261017T052111914317Z/active_businesses_metadata.json) | json | 37,019 | n/a (metadata/documentation) | Snapshot / not stated; see limitations |
| [data/raw/points_of_interest/20261017T052111914317Z/active_businesses.csv](../data/raw/points_of_interest/20261017T052111914317Z/active_businesses.csv) | csv | 141,737,194 | 632799 | Snapshot / not stated; see limitations |

Exact endpoints and retrieval dates:

- `active_businesses_metadata.json`: [https://data.lacity.org/api/views/6rrh-rzua.json](https://data.lacity.org/api/views/6rrh-rzua.json); retrieved `2026-10-17T05:21:17.473747+00:00`.
- `active_businesses.csv`: [https://data.lacity.org/api/views/6rrh-rzua/rows.csv?accessType=DOWNLOAD](https://data.lacity.org/api/views/6rrh-rzua/rows.csv?accessType=DOWNLOAD); retrieved `2026-10-17T05:21:20.099459+00:00`.

- `active_businesses_metadata.json` provider timestamps (UTC): rowsUpdatedAt = 2026-10-15T18:06:00+00:00; viewLastModified = 2026-10-15T18:03:36+00:00.
## events

- Provider: MLB Advanced Media; UCLA Registrar
- Geographic coverage: Dodgers schedule includes home AND away games; UCLA academic calendar includes administrative milestones.
- Eventual variables: Potential nearby scheduled sports-event timing and UCLA term/activity timing.
- Limitations: MLB query requests all Dodgers games in August 2025; away games retained. Not a comprehensive LA event list, attendance measure, or measured parking impact. UCLA ICS is an academic calendar, not a concerts or athletics feed. No event indicators, distances or local-date conversions generated. Concert/venue-wide historical event coverage remains a gap; see additional sources below.
- License / usage: MLB response carries copyright and links http://gdx.mlb.com/components/copyright.txt; public endpoint is not a blanket open-data license. UCLA public calendar has no explicit open-data license verified. Retain attribution and check terms before redistribution.

| Original file (relative to project root) | Format | Bytes | Records | Date coverage |
|---|---|---:|---:|---|
| [data/raw/events/20261017T052111914317Z/dodgers_schedule_2025_08.json](../data/raw/events/20261017T052111914317Z/dodgers_schedule_2025_08.json) | json | 40,763 | 28 | 2025-08-01T23:35:00Z to 2025-08-31T20:10:00Z |
| [data/raw/events/20261017T052111914317Z/ucla_term_2025_26.ics](../data/raw/events/20261017T052111914317Z/ucla_term_2025_26.ics) | ics | 94,749 | 376 | 20250602 to 20261023 |

Exact endpoints and retrieval dates:

- `dodgers_schedule_2025_08.json`: [https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId=119&startDate=2025-08-01&endDate=2025-08-31&hydrate=venue](https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId=119&startDate=2025-08-01&endDate=2025-08-31&hydrate=venue); retrieved `2026-10-17T05:21:22.212173+00:00`.
- `ucla_term_2025_26.ics`: [https://registrar.ucla.edu/file/f039f93a-3331-4124-96ce-8f4773e00c6f](https://registrar.ucla.edu/file/f039f93a-3331-4124-96ce-8f4773e00c6f); retrieved `2026-10-17T05:21:22.460304+00:00`.

## weather

- Provider: NOAA / NCEI, NOAA public AWS mirror
- Geographic coverage: LAX station 72295023174 and downtown USC 72287493134; station measurements, not all LA microclimates.
- Eventual variables: Potential temperature, wind, precipitation and present-weather predictors, subject to later decoding and quality checks.
- Limitations: Full available 2025 station files saved, not cut to occupancy month. LAX ends 2025-08-27 07:59 UTC and downtown ends 2025-08-25 07:59 UTC: the end of the parking month is NOT covered. LAX is the primary hourly/synoptic source; downtown file contains SOD daily summary reports with many hourly fields encoded missing. ISD fields include scaling, quality flags and missing codes; no decoding performed. Annual filename does not guarantee a full year. Legacy NCEI /data/global-hourly URL redirected to an HTML bucket index; direct NOAA S3 objects worked. GHCNh supersedes legacy ISD, so a missing legacy 2026 object does NOT imply no 2026 NOAA observations exist. A newer NOAA source is needed to close the late-August gap; nothing was imputed.
- License / usage: NOAA public-access environmental data; cite NOAA NCEI Global Surface Hourly and station/year. Keep provider quality flags. Corrected ISD manual downloaded from /pub/data/noaa/.

| Original file (relative to project root) | Format | Bytes | Records | Date coverage |
|---|---|---:|---:|---|
| [data/raw/weather/20261017T052111914317Z/downtown_USC_2025.csv](../data/raw/weather/20261017T052111914317Z/downtown_USC_2025.csv) | csv | 150,556 | 207 | 2025-01-01T07:59:00 to 2025-08-25T07:59:00 |
| [data/raw/weather/20261017T052111914317Z/LAX_2025.csv](../data/raw/weather/20261017T052111914317Z/LAX_2025.csv) | csv | 5,219,474 | 9082 | 2025-01-01T00:00:00 to 2025-08-27T07:59:00 |
| [data/raw/weather/20261017T052208206062Z/isd-format-document.pdf](../data/raw/weather/20261017T052208206062Z/isd-format-document.pdf) | pdf | 1,187,390 | n/a (metadata/documentation) | Snapshot / not stated; see limitations |

Exact endpoints and retrieval dates:

- `downtown_USC_2025.csv`: [https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72287493134.csv](https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72287493134.csv); retrieved `2026-10-17T05:21:20.830060+00:00`.
- `LAX_2025.csv`: [https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72295023174.csv](https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72295023174.csv); retrieved `2026-10-17T05:21:20.827127+00:00`.
- `isd-format-document.pdf`: [https://www.ncei.noaa.gov/pub/data/noaa/isd-format-document.pdf](https://www.ncei.noaa.gov/pub/data/noaa/isd-format-document.pdf); retrieved `2026-10-17T05:22:12.189360+00:00`.

## other

- Provider: Los Angeles County Metropolitan Transportation Authority (LACMTA)
- Geographic coverage: Metro rail network, not all bus or regional transit service.
- Eventual variables: Potential station proximity and scheduled transit service as alternatives to driving.
- Limitations: Original GitHub mirror proved stale (October 2022 service); retained for provenance and rejected for August 2025 service modeling. Current official GitLab feed added (October 2026), useful as a station reference with vintage caveat, not historical August 2025 service. No extraction, stop filtering or distance computation. A historical GTFS vintage remains necessary for historically accurate service measures.
- License / usage: Official public feed; accompanying provider README saved. No standalone explicit redistribution license verified; review provider terms before redistribution.

| Original file (relative to project root) | Format | Bytes | Records | Date coverage |
|---|---|---:|---:|---|
| [data/raw/other/20261017T052111914317Z/metro_rail_gtfs.zip](../data/raw/other/20261017T052111914317Z/metro_rail_gtfs.zip) | zip | 732,635 | n/a (metadata/documentation) | 20221007 to 20221021 |
| [data/raw/other/20261017T052111914317Z/metro_rail_readme.md](../data/raw/other/20261017T052111914317Z/metro_rail_readme.md) | md | 3,347 | n/a (metadata/documentation) | Snapshot / not stated; see limitations |
| [data/raw/other/20261017T052208206062Z/metro_rail_gtfs.zip](../data/raw/other/20261017T052208206062Z/metro_rail_gtfs.zip) | zip | 1,632,567 | n/a (metadata/documentation) | 20261016 to 20261030 |
| [data/raw/other/20261017T052208206062Z/metro_rail_readme.md](../data/raw/other/20261017T052208206062Z/metro_rail_readme.md) | md | 3,598 | n/a (metadata/documentation) | Snapshot / not stated; see limitations |

Exact endpoints and retrieval dates:

- `metro_rail_gtfs.zip`: [https://raw.githubusercontent.com/LACMTA/gtfs_rail/master/gtfs_rail.zip](https://raw.githubusercontent.com/LACMTA/gtfs_rail/master/gtfs_rail.zip); retrieved `2026-10-17T05:21:22.495192+00:00`.
  ZIP member counts (excluding header): agency.txt: 1, calendar.txt: 24, calendar_dates.txt: 0, routes.txt: 7, shapes.txt: 7,713, stops.txt: 427, stop_times.txt: 87,549, trips.txt: 6,653, feed_info.txt: 1.
- `metro_rail_readme.md`: [https://raw.githubusercontent.com/LACMTA/gtfs_rail/master/README.md](https://raw.githubusercontent.com/LACMTA/gtfs_rail/master/README.md); retrieved `2026-10-17T05:21:22.796491+00:00`.
- `metro_rail_gtfs.zip`: [https://gitlab.com/LACMTA/gtfs_rail/-/raw/master/gtfs_rail.zip](https://gitlab.com/LACMTA/gtfs_rail/-/raw/master/gtfs_rail.zip); retrieved `2026-10-17T05:22:13.314653+00:00`.
  ZIP member counts (excluding header): agency.txt: 1, calendar.txt: 29, calendar_dates.txt: 2, fare_attributes.txt: 1, fare_rules.txt: 6, routes.txt: 6, shapes.txt: 17,590, stops.txt: 463, stop_times.txt: 201,271, trips.txt: 8,678, feed_info.txt: 1.
- `metro_rail_readme.md`: [https://gitlab.com/LACMTA/gtfs_rail/-/raw/master/README.md](https://gitlab.com/LACMTA/gtfs_rail/-/raw/master/README.md); retrieved `2026-10-17T05:22:13.627461+00:00`.

## Investigated sources, access requirements and gaps

- **Direct Census ACS API:** `https://api.census.gov/data/2024/acs/acs5?get=NAME,B01003_001E,B25001_001E,B19013_001E&for=tract:*&in=state:06%20county:037` redirected to a missing-key page. [Official examples](https://api.census.gov/data/2024/acs/acs5/examples.html) now require a personal key; request one at https://api.census.gov/data/key_signup.html for direct access. Census Reporter response was saved instead. No secret/key is stored.
- **Ticketmaster concerts / sports / venues:** [Discovery API documentation](https://developer.ticketmaster.com/products-and-docs/apis/discovery-manual/v2/), endpoint `https://app.ticketmaster.com/discovery/v2/events.json`. Requires developer account/API key in `apikey`; no request made with invented credentials. Geographic/date queries and pagination would be needed. Historical August 2025 completeness is not verified; do not assume past events remain queryable. Bulk Discovery Feed also requires access/key. No bulk concert archive downloaded.
- **UCLA event listings:** [UCLA events](https://www.ucla.edu/events), [Community](https://community.ucla.edu/), [calendar integration information](https://community.ucla.edu/manage). Public listings exist but a complete historical bulk API was not verified. Guessed `/events.ics` returned 404 and was rejected. The verified Registrar ICS was saved instead; it is not a substitute for a comprehensive event history.
- **OpenStreetMap:** reproducible public alternative via https://overpass-api.de/api/interpreter and https://wiki.openstreetmap.org/wiki/Overpass_API; restaurant/shop/amenity tags could expand coverage, including schools. Not downloaded: official full business registry prioritized; current OSM would introduce a second time-mismatched POI snapshot. OSM would require ODbL attribution/usage review and deliberate historical-snapshot choice.
- **NOAA:** [legacy product](https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database), [replacement GHCNh](https://www.ncei.noaa.gov/products/global-historical-climatology-network-hourly). Legacy 2026 S3 prefix for LAX was empty; failed/moved ISD manual URL returned HTML, not data, and was rejected. Correct PDF was saved. Weather overlaps August 2025 but ends before the parking month does. GHCNh is the route to investigate for a future 2026 extension.
- **Metro:** GitHub raw file downloaded successfully but internally has October 2022 service dates; rejected as contemporary schedule data and retained unchanged. GitLab feed is current October 2026; neither is a verified August 2025 schedule.
- **Street restrictions:** retained legacy public tables with explicit vintage caveats. A recent comprehensive curb/no-parking schedule was not verified. Meter operating hours are not fields in the downloaded inventory despite its broad description.
- **Calendar variables:** not generated. Original occupancy timestamps remain exactly as supplied. No holiday dummy file, hour, weekend or month variable created.

## Suitability for the later ECON 430 phase

The historical file contains many more than 500 events and more than 500 distinct source spaces (see audit), but 500 usable independent cross-sectional observations have not been established. Constructing an appropriate single-period space/block cross-section is later work. Sensor transitions are not directly time-weighted occupancy fractions; repeated records are not independent cross-sectional observations. At least five plausible predictor concepts are present in source fields (meter type, rate type, rate range, time limit, zoning, population/housing/income, business locations and weather), but actual usability and historical alignment remain untested. Time-only weather/event/calendar variables cannot explain differences within a simultaneous snapshot without variation; study design must address that later. No model specifications, descriptive statistics or validation splits have been created.

## Download failures retained in provenance

- `https://www.ncei.noaa.gov/data/global-hourly/doc/isd-format-document.pdf` (parameters `None`): Unexpected HTML response, possibly missing key or moved endpoint. No failed response was saved as a data file. NOAA documentation was recovered at the corrected URL; all four failed zoning pages were recovered as disjoint smaller responses, with complete count and source-ID-multiplicity verification in the audit.
- `https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query` (parameters `{'f': 'json', 'where': '1=1', 'outFields': '*', 'returnGeometry': 'true', 'orderByFields': 'OBJECTID', 'resultOffset': 20000, 'resultRecordCount': 5000}`): 502 Server Error: Bad Gateway for url: https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=20000&resultRecordCount=5000. No failed response was saved as a data file. NOAA documentation was recovered at the corrected URL; all four failed zoning pages were recovered as disjoint smaller responses, with complete count and source-ID-multiplicity verification in the audit.
- `https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query` (parameters `{'f': 'json', 'where': '1=1', 'outFields': '*', 'returnGeometry': 'true', 'orderByFields': 'OBJECTID', 'resultOffset': 25000, 'resultRecordCount': 5000}`): 502 Server Error: Bad Gateway for url: https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=25000&resultRecordCount=5000. No failed response was saved as a data file. NOAA documentation was recovered at the corrected URL; all four failed zoning pages were recovered as disjoint smaller responses, with complete count and source-ID-multiplicity verification in the audit.
- `https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query` (parameters `{'f': 'json', 'where': '1=1', 'outFields': '*', 'returnGeometry': 'true', 'orderByFields': 'OBJECTID', 'resultOffset': 40000, 'resultRecordCount': 5000}`): 502 Server Error: Bad Gateway for url: https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=40000&resultRecordCount=5000. No failed response was saved as a data file. NOAA documentation was recovered at the corrected URL; all four failed zoning pages were recovered as disjoint smaller responses, with complete count and source-ID-multiplicity verification in the audit.
- `https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query` (parameters `{'f': 'json', 'where': '1=1', 'outFields': '*', 'returnGeometry': 'true', 'orderByFields': 'OBJECTID', 'resultOffset': 45000, 'resultRecordCount': 5000}`): 502 Server Error: Bad Gateway for url: https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query?f=json&where=1%3D1&outFields=%2A&returnGeometry=true&orderByFields=OBJECTID&resultOffset=45000&resultRecordCount=5000. No failed response was saved as a data file. NOAA documentation was recovered at the corrected URL; all four failed zoning pages were recovered as disjoint smaller responses, with complete count and source-ID-multiplicity verification in the audit.
