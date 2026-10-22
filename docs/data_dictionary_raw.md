# Raw data dictionary

Names below refer to source columns or nested JSON keys exactly. API field names can differ from CSV export headers. No values have been decoded, renamed or changed. Provider metadata is saved alongside originals.

## ladot_occupancy

### LADOT Parking Meter Occupancy - Archive

| CSV column | API field | Provider type | Meaning / caveat |
|---|---|---|---|
| `SpaceID` | `spaceid` | text | No column definition supplied; use the literal source field and dataset context. |
| `EventTime_UTC` | `eventtime_utc` | text | No column definition supplied; use the literal source field and dataset context. |
| `OccupancyState` | `occupancystate` | text | No column definition supplied; use the literal source field and dataset context. |

### LADOT Parking Meter Occupancy

| CSV column | API field | Provider type | Meaning / caveat |
|---|---|---|---|
| `SpaceID` | `spaceid` | text | Unique metered parking space identifier, as seen on meter body or curb.  |
| `EventTime_UTC` | `eventtime` | calendar_date | Occupancy transaction timestamp (UTC).  |
| `OccupancyState` | `occupancystate` | text | Last known occupancy state. |

## ladot_meters

### LADOT Metered Parking Inventory & Policies

| CSV column | API field | Provider type | Meaning / caveat |
|---|---|---|---|
| `SpaceID` | `spaceid` | text | Unique metered parking space identifier, as seen on meter body or curb. |
| `BlockFace` | `blockface` | text | Block number and street of metered space. |
| `MeterType` | `metertype` | text | Single-space or multi-space meter. |
| `RateType` | `ratetype` | text | Hourly rate type - FLAT, JUMP, SEASONAL, Time-of-Day (TOD) |
| `RateRange` | `raterange` | text | JUMP: $X.XX/hr-$X.XX/max; SEASONAL: Fall/Winter & Spring/Summer; TOD: Min-Max hourly rate range |
| `MeteredTimeLimit` | `timelimit` | text | Maximum parking time limit during metered hours. |
| `LatLng` | `latlng` | location | Location (Lat/Lng) |

## parking_regulations

### Posted Street Sweeping Routes

| CSV column | API field | Provider type | Meaning / caveat |
|---|---|---|---|
| `Route No` | `route_no` | text | No column definition supplied; use the literal source field and dataset context. |
| `Council District` | `cd` | text | No column definition supplied; use the literal source field and dataset context. |
| `Time Start` | `time_start` | text | No column definition supplied; use the literal source field and dataset context. |
| `Time End` | `time_end` | text | No column definition supplied; use the literal source field and dataset context. |
| `Boundaries` | `boundaries` | text | No column definition supplied; use the literal source field and dataset context. |

### LADOT_PPD

| CSV column | API field | Provider type | Meaning / caveat |
|---|---|---|---|
| `the_geom` | `the_geom` | multipolygon | No column definition supplied; use the literal source field and dataset context. |
| `PPDNUM` | `ppdnum` | number | No column definition supplied; use the literal source field and dataset context. |
| `PPDNAME` | `ppdname` | text | No column definition supplied; use the literal source field and dataset context. |

### LADOT Parking Calendar Sign Locations

| CSV column | API field | Provider type | Meaning / caveat |
|---|---|---|---|
| `Blockface` | `blockface` | text | Block number and street of sign. |
| `Status` | `status` | text | Installation status. |
| `Sign Count` | `signcount` | text | Number of calendar signs on blockface. |
| `the_geom` | `the_geom` | multipolygon | Location geometry |

## land_use

| Raw attribute | Source type | Description |
|---|---|---|
| `OBJECTID` | esriFieldTypeOID | Source feature ID; used only for pagination order. |
| `ZONE_CMPLT` | esriFieldTypeString | Complete zoning designation. |
| `ZONE_UNDER` | esriFieldTypeString | Underlying zoning designation. |
| `JTX_ID` | esriFieldTypeInteger | Source workflow identifier; definition not supplied. |
| `PAPER_ST` | esriFieldTypeSmallInteger | Source indicator; coded meaning not supplied. |
| `Shape` | esriFieldTypeGeometry | Geometry field; JSON feature geometry contains rings. |
| `ZONE_CLASS` | esriFieldTypeString | Source zoning class. |
| `ZONE_CODE` | esriFieldTypeSmallInteger | Source zoning code. |
| `ZONING_DESCRIPTION` | esriFieldTypeString | General zoning class text. |
| `TOOLTIP` | esriFieldTypeString | Provider tooltip text. |

`features[].attributes` contains the fields; `features[].geometry.rings` stores polygons. `spatialReference` describes the response coordinates. Pages are unmerged.

## census

## points_of_interest

### Listing of Active Businesses

| CSV column | API field | Provider type | Meaning / caveat |
|---|---|---|---|
| `LOCATION ACCOUNT #` | `location_account` | text | The account number of the business location. |
| `BUSINESS NAME` | `business_name` | text | The legal name of the business. |
| `DBA NAME` | `dba_name` | text | Doing Business As (DBA) name. If more than one DBA name exists, then all names are shown as a pipe-separated list. |
| `STREET ADDRESS` | `street_address` | text | Street address of the business location. |
| `CITY` | `city` | text | City of the business location. |
| `ZIP CODE` | `zip_code` | text | Zip code of the business location. |
| `LOCATION DESCRIPTION` | `location_description` | text | Abbreviated address description of the business location. |
| `MAILING ADDRESS` | `mailing_address` | text | Mailing address of the business. |
| `MAILING CITY` | `mailing_city` | text | Mailing address city of the business. |
| `MAILING ZIP CODE` | `mailing_zip_code` | text | Mailing address Zip code of the business. |
| `NAICS` | `naics` | text | The self-reported North American Industry Classification System (NAICS) code, which is used in classifying business establishments. |
| `PRIMARY NAICS DESCRIPTION` | `primary_naics_description` | text | Description of the primary NAICS code. Descriptions that are noted as "(1997 NAICS)" apply the code and description designated in 1997 as referred to in the New Business Exemption Ordinance. |
| `COUNCIL DISTRICT` | `council_district` | number | The council district # reflects the current council district assignment for that location address. "0" means the business location is out of the City. |
| `LOCATION START DATE` | `location_start_date` | calendar_date | The start date of the first business activity registered at this location. |
| `LOCATION END DATE` | `location_end_date` | text | The most recent end date of all business activities at the location. |
| `LOCATION` | `location_1` | location | Latitude & Longitude, if present, for this business location. |

## events

## weather

## other

## Additional source formats

- **Census Reporter ACS JSON:** `release` identifies vintage; `tables` defines labels and column codes. `data[tract_geoid][table].estimate` and `.error` preserve estimates and margins of error. Tables: `B01003` population; `B25001` housing units; `B19013` median household income; `B08301` means of transportation to work. Source code `B01003001` differs from direct Census API `B01003_001E`. Missing/sentinel codes remain as supplied. `geography` describes geographic IDs.
- **2024 Gazetteer TSV:** `USPS` state abbreviation; `GEOID` tract identifier; `ALAND`, `AWATER` area in square meters; `ALAND_SQMI`, `AWATER_SQMI` area in square miles; `INTPTLAT`, `INTPTLONG` internal point coordinates. Header padding is preserved.
- **NOAA CSV:** `STATION` station identifier; `DATE` observation timestamp (UTC per ISD); `LATITUDE`, `LONGITUDE`, `ELEVATION`, `NAME` station metadata; `SOURCE`, `REPORT_TYPE`, `CALL_SIGN`, `QUALITY_CONTROL` provenance/report flags. `WND` packs wind direction/type/speed and quality; `TMP`, `DEW` pack scaled temperature/dew point and quality; `SLP` pressure; `CIG`, `VIS` ceiling/visibility; `AA1`–`AA3` precipitation period/depth/flags; `AW*`, `AT*`, `AU*`, `MW*` weather code groups when present; `KA*` extrema/period groups; `REM` remarks; `EQD` quality information. Not every station has every field. Consult the saved 137-page ISD manual before any later decoding; codes and missing values are unchanged.
- **MLB JSON:** `dates[].date`, `dates[].games[].gamePk`, `gameDate`, `officialDate`, `status`, `teams.home`, `teams.away`, `venue.id`, `venue.name` identify games, scheduled UTC times, teams and venues. `copyright` retains usage notice. `totalGames` is source count. Home/away distinction must be respected later.
- **UCLA ICS:** `UID` event ID, `DTSTAMP` source stamp, `DTSTART` start (often `VALUE=DATE`), `DURATION` duration, `SUMMARY` title, `DESCRIPTION` details; calendar `X-WR-TIMEZONE` gives timezone. ICS wrapped/escaped lines remain unchanged; no calendar predictors created.
- **Metro GTFS ZIP:** `stops.txt`: `stop_id`, `stop_name`, `stop_lat`, `stop_lon`, `location_type`, `parent_station`; `routes.txt`: route identifiers and types; `trips.txt`: trip, route and service IDs; `stop_times.txt`: arrivals/departures, stop sequence and IDs; `calendar.txt`: service IDs, weekday flags and start/end dates; `calendar_dates.txt`: exceptions; `shapes.txt`: route geometry points; `agency.txt`, `feed_info.txt`: provider/vintage. All ZIP members remain inside original archives, unextracted. Inspect the archive vintage before use.

