"""Generate acquisition inventory and raw dictionary from saved audit/metadata."""
from pathlib import Path
from datetime import datetime, timezone
import json

ROOT=Path(__file__).resolve().parents[2]

def main():
    records=json.loads((ROOT/'docs/acquisition_audit.json').read_text())
    notes={
      'ladot_occupancy':('City of Los Angeles / LADOT','Sensor-equipped metered street spaces in LA; not all curb parking.',
        'Outcome: recorded occupancy state; timestamps and space IDs support later cross-sectional construction.',
        'Historical file: complete August 2025 attachment, chosen for overlap with available legacy NOAA weather. Raw UTC-labelled timestamp span is 8/1/2025 7:00:01 AM through 9/1/2025 6:59:59 AM, so attachment month is not a strict UTC calendar-month boundary. No rows selected or removed. Current feed is a separate retrieval snapshot, not a historical panel. Event records are state changes, not evenly spaced availability observations; unknown states, stale sensors, missing baselines, and sensor coverage require later review. Repeated events do not count as independent cross-sectional units.',
        'Socrata licenseId PUBLIC_DOMAIN. Archive table is empty: real historical records are in metadata attachments. rowsUpdatedAt on the archive table is not the monthly attachment update date; viewLastModified and attachment listing are preserved.'),
      'ladot_meters':('City of Los Angeles / LADOT','All on-street metered spaces in published inventory.',
        'Potential predictors: RateRange, RateType, MeteredTimeLimit, MeterType, location and block face.',
        'Seven published columns only. Description mentions operating hours and restrictions, but those columns are absent. No separate numeric price, zone, exact address, or historical effective dates are provided. RateRange can describe variable tariffs; no numeric parsing performed. Current inventory may differ from August 2025.',
        'Socrata licenseId PUBLIC_DOMAIN.'),
      'parking_regulations':('City of Los Angeles / LADOT and Bureau of Street Services','Published LA posted sweeping routes, permit districts and calendar sign block faces.',
        'Possible future sweeping time, permit district and sign-location predictors; inventory also supplies metered time limits.',
        'Sweeping table rowsUpdatedAt is 2014; permit districts 2015; calendar sign locations 2019. These are legacy sources, not verified current or August 2025 rules. Sweeping boundaries are text, not street-segment geometry; no explicit weekday column. Calendar signs describe installation, not sign rules. No complete citywide no-parking-period/curb-regulation inventory was verified. Do not infer restriction schedules from sign locations.',
        'Sweeping and permit datasets: CC0_10; calendar sign locations: PUBLIC_DOMAIN, per saved metadata.'),
      'land_use':('City of Los Angeles / City Planning via NavigateLA','Entire Generalized Zoning layer, 58,952 features at acquisition.',
        'Potential residential/commercial/industrial zoning and neighborhood land-use classification predictors.',
        'Zoning is a legal designation, not observed current land use. All features and all attributes requested, no geographic clipping. Pagination uses OBJECTID order, pages saved separately. Server default geometry CRS is EPSG:3857 in responses; layer source metadata lists EPSG:2229. No client reprojection. Concurrent server edits can affect pagination. No verified layer update date or historical effective-date coverage. The provider itself returns repeated OBJECTID values: 58,952 records and 58,855 distinct IDs. The audit compares the complete multiset of IDs with the independently downloaded source ID listing; duplicates are retained.',
        'Publicly accessible City service; copyrightText is blank and no explicit reuse license in layer metadata. Do not assume CC0; confirm City GIS terms before redistribution.'),
      'census':('U.S. Census Bureau; ACS delivered through Census Reporter public API','ACS: all LA County census tracts requested; Gazetteer: entire California tract file.',
        'ACS population, housing units, household income, journey-to-work mode estimates and margins of error; Gazetteer land area and tract identifiers can support later density measures.',
        'ACS2024_5yr is a 2020–2024 survey period, not August 2025 conditions. County contains areas outside LA city. Census Reporter is a third-party delivery service; raw response includes release/table metadata. Census direct API redirected to missing_key.html; no credentials fabricated. Gazetteer contains area and internal points, not tract boundaries or population. No density, geographic joins or commuting shares calculated.',
        'Census federal statistical data are public; cite Census and Census Reporter delivery. API response contains no separate explicit license grant; no blanket license inferred for service code or other website material.'),
      'points_of_interest':('City of Los Angeles / Office of Finance','Full published Listing of Active Businesses, including registered locations outside LA.',
        'NAICS and location fields could support later restaurant, retail, entertainment and business counts.',
        'Full source export retained, including blanks and businesses outside city limits. Active means no reported cessation; not independently verified open establishments. NAICS are self-reported and source description references 2007 codes; entries are not necessarily distinct physical destinations. Snapshot is October 2026, not a complete historical August 2025 business census. Schools/universities are not exhaustively covered. OSM was considered but not downloaded because this official full business registry provides a reproducible POI starting point without a second overlapping snapshot.',
        'Socrata licenseId CC0_10. Contains public business names and addresses; no Google Maps scraping.'),
      'events':('MLB Advanced Media; UCLA Registrar','Dodgers schedule includes home AND away games; UCLA academic calendar includes administrative milestones.',
        'Potential nearby scheduled sports-event timing and UCLA term/activity timing.',
        'MLB query requests all Dodgers games in August 2025; away games retained. Not a comprehensive LA event list, attendance measure, or measured parking impact. UCLA ICS is an academic calendar, not a concerts or athletics feed. No event indicators, distances or local-date conversions generated. Concert/venue-wide historical event coverage remains a gap; see additional sources below.',
        'MLB response carries copyright and links http://gdx.mlb.com/components/copyright.txt; public endpoint is not a blanket open-data license. UCLA public calendar has no explicit open-data license verified. Retain attribution and check terms before redistribution.'),
      'weather':('NOAA / NCEI, NOAA public AWS mirror','LAX station 72295023174 and downtown USC 72287493134; station measurements, not all LA microclimates.',
        'Potential temperature, wind, precipitation and present-weather predictors, subject to later decoding and quality checks.',
        'Full available 2025 station files saved, not cut to occupancy month. LAX ends 2025-08-27 07:59 UTC and downtown ends 2025-08-25 07:59 UTC: the end of the parking month is NOT covered. LAX is the primary hourly/synoptic source; downtown file contains SOD daily summary reports with many hourly fields encoded missing. ISD fields include scaling, quality flags and missing codes; no decoding performed. Annual filename does not guarantee a full year. Legacy NCEI /data/global-hourly URL redirected to an HTML bucket index; direct NOAA S3 objects worked. GHCNh supersedes legacy ISD, so a missing legacy 2026 object does NOT imply no 2026 NOAA observations exist. A newer NOAA source is needed to close the late-August gap; nothing was imputed.',
        'NOAA public-access environmental data; cite NOAA NCEI Global Surface Hourly and station/year. Keep provider quality flags. Corrected ISD manual downloaded from /pub/data/noaa/.'),
      'other':('Los Angeles County Metropolitan Transportation Authority (LACMTA)','Metro rail network, not all bus or regional transit service.',
        'Potential station proximity and scheduled transit service as alternatives to driving.',
        'Original GitHub mirror proved stale (October 2022 service); retained for provenance and rejected for August 2025 service modeling. Current official GitLab feed added (October 2026), useful as a station reference with vintage caveat, not historical August 2025 service. No extraction, stop filtering or distance computation. A historical GTFS vintage remains necessary for historically accurate service measures.',
        'Official public feed; accompanying provider README saved. No standalone explicit redistribution license verified; review provider terms before redistribution.'),
    }
    lines=['# Raw data sources and acquisition report','',
      'Acquisition only. No cleaning, transformation, imputation, observation removal, merging, feature engineering, EDA, statistical models, or prediction models were performed. Record counts, timestamp extents, schema inspection and hashes below are read-only acquisition checks.', '',
      'Retrieval occurred October 16, 2026 in America/Los_Angeles (October 17 UTC). Every original is in a unique UTC-stamped directory. Exact request parameters, final URLs, HTTP response dates/Last-Modified headers, sizes, SHA-256 hashes and failures are in [retrieval manifests](retrievals/) and [acquisition_audit.json](acquisition_audit.json). Files are source response bodies; documentation and audit JSON are project-generated provenance.', '',
      'One entire historical month was selected before download; this is a source-period choice, not filtering a downloaded dataset. HEAD checks and streamed byte caps prevented unexpected huge downloads. No source export used a row cap or observation filter; zoning uses where=1=1 and full pagination. Census geographic/table requests and the MLB team/month request define the acquisition scope. Raw values, headers and timestamp strings are unchanged.','']
    dictionary=['# Raw data dictionary','', 'Names below refer to source columns or nested JSON keys exactly. API field names can differ from CSV export headers. No values have been decoded, renamed or changed. Provider metadata is saved alongside originals.','']
    for category,(provider,geo,variables,limitations,license_notes) in notes.items():
        items=[r for r in records if r['category']==category and r['success']]
        lines += [f'## {category}','',f'- Provider: {provider}',f'- Geographic coverage: {geo}',f'- Eventual variables: {variables}',f'- Limitations: {limitations}',f'- License / usage: {license_notes}','', '| Original file (relative to project root) | Format | Bytes | Records | Date coverage |', '|---|---|---:|---:|---|']
        dictionary += [f'## {category}','']
        for rec in items:
            p=ROOT/rec['file']; rows=rec.get('rows','n/a (metadata/documentation)')
            coverage=rec.get('raw_timestamp_extent',rec.get('service_date_extent'))
            cov=' to '.join(coverage) if coverage else ('ACS 2020–2024; geography vintage 2024' if category=='census' else 'Snapshot / not stated; see limitations')
            lines += [f"| [{rec['file']}](../{rec['file'].replace(' ','%20')}) | {p.suffix[1:]} | {rec['bytes']:,} | {rows} | {cov} |"]
        lines += ['', 'Exact endpoints and retrieval dates:','']
        for rec in items:
            lines += [f"- `{Path(rec['file']).name}`: [{rec['final_url']}]({rec['final_url']}); retrieved `{rec['retrieved_utc']}`."]
            if 'distinct_space_ids' in rec:lines += [f"  Acquisition count: {rec['distinct_space_ids']:,} distinct source space IDs; usability has not been assessed."]
            if rec.get('members'):
                lines += ['  ZIP member counts (excluding header): '+', '.join(f"{k}: {v['rows']:,}" for k,v in rec['members'].items())+'.']
        lines += ['']
        for rec in items:
            p=ROOT/rec['file']
            if p.name.endswith('_metadata.json') and category!='land_use':
                meta=json.loads(p.read_bytes())
                lines += [f"- `{p.name}` provider timestamps (UTC): "+'; '.join(f"{k} = {datetime.fromtimestamp(meta[k],timezone.utc).isoformat()}" for k in ['rowsUpdatedAt','viewLastModified'] if meta.get(k))+'.']
                dictionary += [f'### {meta["name"]}', '', '| CSV column | API field | Provider type | Meaning / caveat |','|---|---|---|---|']
                for c in meta.get('columns',[]):
                    if c.get('fieldName','').startswith(':'):continue
                    desc=(c.get('description') or 'No column definition supplied; use the literal source field and dataset context.').replace('\n',' ').replace('|',' / ')
                    dictionary += [f"| `{c['name']}` | `{c['fieldName']}` | {c.get('dataTypeName','')} | {desc} |"]
                dictionary += ['']
        if category=='land_use':
            meta=json.loads((ROOT/next(r['file'] for r in items if r['file'].endswith('zoning_metadata.json'))).read_bytes())
            dictionary += ['| Raw attribute | Source type | Description |','|---|---|---|']
            meanings={'OBJECTID':'Source feature ID; used only for pagination order.','ZONE_CMPLT':'Complete zoning designation.','ZONE_UNDER':'Underlying zoning designation.','ZONING_DESCRIPTION':'General zoning class text.','ZONE_CLASS':'Source zoning class.','ZONE_CODE':'Source zoning code.','JTX_ID':'Source workflow identifier; definition not supplied.','PAPER_ST':'Source indicator; coded meaning not supplied.','TOOLTIP':'Provider tooltip text.','Shape':'Geometry field; JSON feature geometry contains rings.'}
            for f in meta['fields']:dictionary += [f"| `{f['name']}` | {f['type']} | {meanings.get(f['name'],'Source field; no definition supplied.')} |"]
            dictionary += ['', '`features[].attributes` contains the fields; `features[].geometry.rings` stores polygons. `spatialReference` describes the response coordinates. Pages are unmerged.','']
    dictionary += ['## Additional source formats','',
      '- **Census Reporter ACS JSON:** `release` identifies vintage; `tables` defines labels and column codes. `data[tract_geoid][table].estimate` and `.error` preserve estimates and margins of error. Tables: `B01003` population; `B25001` housing units; `B19013` median household income; `B08301` means of transportation to work. Source code `B01003001` differs from direct Census API `B01003_001E`. Missing/sentinel codes remain as supplied. `geography` describes geographic IDs.',
      '- **2024 Gazetteer TSV:** `USPS` state abbreviation; `GEOID` tract identifier; `ALAND`, `AWATER` area in square meters; `ALAND_SQMI`, `AWATER_SQMI` area in square miles; `INTPTLAT`, `INTPTLONG` internal point coordinates. Header padding is preserved.',
      '- **NOAA CSV:** `STATION` station identifier; `DATE` observation timestamp (UTC per ISD); `LATITUDE`, `LONGITUDE`, `ELEVATION`, `NAME` station metadata; `SOURCE`, `REPORT_TYPE`, `CALL_SIGN`, `QUALITY_CONTROL` provenance/report flags. `WND` packs wind direction/type/speed and quality; `TMP`, `DEW` pack scaled temperature/dew point and quality; `SLP` pressure; `CIG`, `VIS` ceiling/visibility; `AA1`–`AA3` precipitation period/depth/flags; `AW*`, `AT*`, `AU*`, `MW*` weather code groups when present; `KA*` extrema/period groups; `REM` remarks; `EQD` quality information. Not every station has every field. Consult the saved 137-page ISD manual before any later decoding; codes and missing values are unchanged.',
      '- **MLB JSON:** `dates[].date`, `dates[].games[].gamePk`, `gameDate`, `officialDate`, `status`, `teams.home`, `teams.away`, `venue.id`, `venue.name` identify games, scheduled UTC times, teams and venues. `copyright` retains usage notice. `totalGames` is source count. Home/away distinction must be respected later.',
      '- **UCLA ICS:** `UID` event ID, `DTSTAMP` source stamp, `DTSTART` start (often `VALUE=DATE`), `DURATION` duration, `SUMMARY` title, `DESCRIPTION` details; calendar `X-WR-TIMEZONE` gives timezone. ICS wrapped/escaped lines remain unchanged; no calendar predictors created.',
      '- **Metro GTFS ZIP:** `stops.txt`: `stop_id`, `stop_name`, `stop_lat`, `stop_lon`, `location_type`, `parent_station`; `routes.txt`: route identifiers and types; `trips.txt`: trip, route and service IDs; `stop_times.txt`: arrivals/departures, stop sequence and IDs; `calendar.txt`: service IDs, weekday flags and start/end dates; `calendar_dates.txt`: exceptions; `shapes.txt`: route geometry points; `agency.txt`, `feed_info.txt`: provider/vintage. All ZIP members remain inside original archives, unextracted. Inspect the archive vintage before use.','']
    lines += ['## Investigated sources, access requirements and gaps','',
      '- **Direct Census ACS API:** `https://api.census.gov/data/2024/acs/acs5?get=NAME,B01003_001E,B25001_001E,B19013_001E&for=tract:*&in=state:06%20county:037` redirected to a missing-key page. [Official examples](https://api.census.gov/data/2024/acs/acs5/examples.html) now require a personal key; request one at https://api.census.gov/data/key_signup.html for direct access. Census Reporter response was saved instead. No secret/key is stored.',
      '- **Ticketmaster concerts / sports / venues:** [Discovery API documentation](https://developer.ticketmaster.com/products-and-docs/apis/discovery-manual/v2/), endpoint `https://app.ticketmaster.com/discovery/v2/events.json`. Requires developer account/API key in `apikey`; no request made with invented credentials. Geographic/date queries and pagination would be needed. Historical August 2025 completeness is not verified; do not assume past events remain queryable. Bulk Discovery Feed also requires access/key. No bulk concert archive downloaded.',
      '- **UCLA event listings:** [UCLA events](https://www.ucla.edu/events), [Community](https://community.ucla.edu/), [calendar integration information](https://community.ucla.edu/manage). Public listings exist but a complete historical bulk API was not verified. Guessed `/events.ics` returned 404 and was rejected. The verified Registrar ICS was saved instead; it is not a substitute for a comprehensive event history.',
      '- **OpenStreetMap:** reproducible public alternative via https://overpass-api.de/api/interpreter and https://wiki.openstreetmap.org/wiki/Overpass_API; restaurant/shop/amenity tags could expand coverage, including schools. Not downloaded: official full business registry prioritized; current OSM would introduce a second time-mismatched POI snapshot. OSM would require ODbL attribution/usage review and deliberate historical-snapshot choice.',
      '- **NOAA:** [legacy product](https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database), [replacement GHCNh](https://www.ncei.noaa.gov/products/global-historical-climatology-network-hourly). Legacy 2026 S3 prefix for LAX was empty; failed/moved ISD manual URL returned HTML, not data, and was rejected. Correct PDF was saved. Weather overlaps August 2025 but ends before the parking month does. GHCNh is the route to investigate for a future 2026 extension.',
      '- **Metro:** GitHub raw file downloaded successfully but internally has October 2022 service dates; rejected as contemporary schedule data and retained unchanged. GitLab feed is current October 2026; neither is a verified August 2025 schedule.',
      '- **Street restrictions:** retained legacy public tables with explicit vintage caveats. A recent comprehensive curb/no-parking schedule was not verified. Meter operating hours are not fields in the downloaded inventory despite its broad description.',
      '- **Calendar variables:** not generated. Original occupancy timestamps remain exactly as supplied. No holiday dummy file, hour, weekend or month variable created.','',
      '## Suitability for the later ECON 430 phase','',
      'The historical file contains many more than 500 events and more than 500 distinct source spaces (see audit), but 500 usable independent cross-sectional observations have not been established. Constructing an appropriate single-period space/block cross-section is later work. Sensor transitions are not directly time-weighted occupancy fractions; repeated records are not independent cross-sectional observations. At least five plausible predictor concepts are present in source fields (meter type, rate type, rate range, time limit, zoning, population/housing/income, business locations and weather), but actual usability and historical alignment remain untested. Time-only weather/event/calendar variables cannot explain differences within a simultaneous snapshot without variation; study design must address that later. No model specifications, descriptive statistics or validation splits have been created.','',
      '## Download failures retained in provenance','']
    for r in records:
        if not r['success']:lines += [f"- `{r['requested_url']}` (parameters `{r.get('params')}`): {r.get('error')}. No failed response was saved as a data file. NOAA documentation was recovered at the corrected URL; all four failed zoning pages were recovered as disjoint smaller responses, with complete count and source-ID-multiplicity verification in the audit."]
    (ROOT/'docs/data_sources.md').write_text('\n'.join(lines)+'\n')
    (ROOT/'docs/data_dictionary_raw.md').write_text('\n'.join(dictionary)+'\n')

if __name__=='__main__':main()
