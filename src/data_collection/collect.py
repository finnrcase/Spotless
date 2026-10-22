"""Download original response bodies only. No cleaning, merging, or modeling.

Each run creates a new UTC-stamped directory under each source category.
HTTP errors and unexpected HTML are logged, never mislabeled as datasets.
"""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import csv
import hashlib
import json
import os
import requests
import time

ROOT = Path(__file__).resolve().parents[2]
UA = 'UCLA-ECON430-parking-source-acquisition/1.0 (academic research)'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--month', default='2025_08', help='LADOT attachment month YYYY_MM')
    parser.add_argument('--max-mb', type=int, default=600, help='Maximum per-file response size')
    args = parser.parse_args()
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    audit = ROOT / 'docs' / 'retrievals' / stamp
    audit.mkdir(parents=True, exist_ok=False)
    manifest = []

    def fetch(category, name, url, *, params=None, kind='data'):
        path = ROOT / 'data/raw' / category / stamp / name
        path.parent.mkdir(parents=True, exist_ok=True)
        record = dict(category=category, file=str(path.relative_to(ROOT)), requested_url=url,
                      params=params, kind=kind, retrieved_utc=datetime.now(timezone.utc).isoformat())
        tmp = path.with_suffix(path.suffix + '.partial')
        try:
            # Inspect advertised length before a potentially large download.
            try:
                head = requests.head(url, params=params, headers={'User-Agent': UA},
                                     allow_redirects=True, timeout=30)
                record['head_status'] = head.status_code
                record['head_headers'] = dict(head.headers)
                if int(head.headers.get('Content-Length', 0)) > args.max_mb * 1000000:
                    raise ValueError('HEAD size exceeds configured maximum')
            except requests.RequestException as exc:
                record['head_warning'] = str(exc)
            with requests.get(url, params=params, headers={'User-Agent': UA, 'Accept-Encoding': 'identity'},
                              stream=True, timeout=(30, 180)) as r:
                record.update(final_url=r.url, status=r.status_code, response_headers=dict(r.headers))
                r.raise_for_status()
                if 'text/html' in r.headers.get('Content-Type', '') and not name.endswith('.html'):
                    raise ValueError('Unexpected HTML response, possibly missing key or moved endpoint')
                total = 0
                digest = hashlib.sha256()
                with tmp.open('xb') as out:
                    for chunk in r.iter_content(1024 * 1024):
                        total += len(chunk)
                        if total > args.max_mb * 1000000:
                            raise ValueError('Stream exceeds configured maximum')
                        out.write(chunk)
                        digest.update(chunk)
                expected = r.headers.get('Content-Length')
                if expected and not r.headers.get('Content-Encoding') and total != int(expected):
                    raise ValueError('Incomplete response')
            # Inspect structure only; never reserialize raw responses.
            if name.endswith('.json'):
                obj = json.loads(tmp.read_bytes())
                if isinstance(obj, dict) and 'error' in obj:
                    raise ValueError('API returned error: ' + str(obj['error']))
            tmp.rename(path)
            record.update(success=True, bytes=total, sha256=digest.hexdigest())
            print(f'OK {category}/{name}: {total:,} bytes', flush=True)
        except Exception as exc:
            tmp.unlink(missing_ok=True)
            record.update(success=False, error=str(exc))
            print(f'FAILED {category}/{name}: {exc}', flush=True)
        return record

    def save(record):
        manifest.append(record)
        with (audit / 'manifest.jsonl').open('a') as f:
            f.write(json.dumps(record) + '\n')
        return record

    socrata = [('ladot_occupancy','cj8s-ivry','archive'),
               ('ladot_occupancy','e7h6-4a3e','current'),
               ('ladot_meters','s49e-q6j2','inventory'),
               ('parking_regulations','krk7-ayq2','street_sweeping'),
               ('parking_regulations','s3st-6nwi','permit_districts'),
               ('parking_regulations','jp2s-nfz4','calendar_sign_locations'),
               ('points_of_interest','6rrh-rzua','active_businesses')]
    jobs = []
    for category, ident, name in socrata:
        rec = save(fetch(category, name+'_metadata.json', f'https://data.lacity.org/api/views/{ident}.json', kind='metadata'))
        if not rec['success']:
            continue
        meta = json.loads((ROOT / rec['file']).read_bytes())
        if ident == 'cj8s-ivry':
            match = [a for a in meta.get('metadata', {}).get('attachments', [])
                     if args.month in a['filename']]
            if not match:
                raise RuntimeError('Requested month not in rolling archive; inspect saved metadata')
            attachment = match[0]
            jobs.append((category, attachment['filename'],
                         f"https://data.lacity.org/api/views/{ident}/files/{attachment['assetId']}" ,
                         {'download':'true', 'filename':attachment['filename']}))
        else:
            # Full native export, no row/column filters and no SODA default row cap.
            jobs.append((category, name+'.csv', f'https://data.lacity.org/api/views/{ident}/rows.csv',
                         {'accessType':'DOWNLOAD'}))

    year = args.month[:4]
    jobs += [
        ('weather', 'LAX_'+year+'.csv', f'https://noaa-global-hourly-pds.s3.amazonaws.com/{year}/72295023174.csv', None),
        ('weather', 'downtown_USC_'+year+'.csv', f'https://noaa-global-hourly-pds.s3.amazonaws.com/{year}/72287493134.csv', None),
        ('weather', 'isd-format-document.pdf', 'https://www.ncei.noaa.gov/pub/data/noaa/isd-format-document.pdf', None),
        ('census', '2024_gaz_tracts_06.txt', 'https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2024_Gazetteer/2024_gaz_tracts_06.txt', None),
        ('census', 'acs2024_5yr_la_county_tracts.json', 'https://api.censusreporter.org/1.0/data/show/acs2024_5yr',
         {'table_ids':'B01003,B25001,B19013,B08301', 'geo_ids':'140|05000US06037'}),
        ('events', 'dodgers_schedule_'+args.month+'.json', 'https://statsapi.mlb.com/api/v1/schedule',
         {'sportId':1,'teamId':119,'startDate':year+'-'+args.month[-2:]+'-01',
          'endDate':year+'-'+args.month[-2:]+'-'+str(__import__('calendar').monthrange(int(year),int(args.month[-2:]))[1]), 'hydrate':'venue'}),
        ('events', 'ucla_term_2025_26.ics', 'https://registrar.ucla.edu/file/f039f93a-3331-4124-96ce-8f4773e00c6f', None),
        ('other', 'metro_rail_gtfs.zip', 'https://gitlab.com/LACMTA/gtfs_rail/-/raw/master/gtfs_rail.zip', None),
        ('other', 'metro_rail_readme.md', 'https://gitlab.com/LACMTA/gtfs_rail/-/raw/master/README.md', None),
    ]
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = [pool.submit(fetch,c,n,u,params=p) for c,n,u,p in jobs]
        for future in as_completed(futures):
            save(future.result())

    # Obtain every zoning feature through stable ID ordering. Pages remain separate
    # original JSON responses, in the server's default response CRS.
    base = 'https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75'
    metadata = save(fetch('land_use','zoning_metadata.json',base,params={'f':'pjson'},kind='metadata'))
    count = save(fetch('land_use','zoning_count.json',base+'/query',
                       params={'f':'json','where':'1=1','returnCountOnly':'true'},kind='metadata'))
    save(fetch('land_use','zoning_source_ids.json',base+'/query',
               params={'f':'json','where':'1=1','returnIdsOnly':'true'},kind='metadata'))
    if metadata['success'] and count['success']:
        n = json.loads((ROOT/count['file']).read_bytes())['count']
        if n > 100000:
            raise RuntimeError('Unexpected zoning volume; inspect before downloading')
        pages = range(0,n,1000)
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures = [pool.submit(fetch,'land_use',f'zoning_offset_{offset:06}.json',base+'/query',
                      params={'f':'json','where':'1=1','outFields':'*','returnGeometry':'true',
                              'orderByFields':'OBJECTID','resultOffset':offset,'resultRecordCount':1000}) for offset in pages]
            for future in as_completed(futures):
                save(future.result())
    print('Manifest:', audit/'manifest.jsonl', flush=True)
    if any(not r['success'] for r in manifest):
        raise SystemExit('Some downloads failed. See manifest; successful originals retained.')


if __name__ == '__main__':
    main()
