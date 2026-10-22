"""Retry failed 5,000-feature zoning pages as disjoint 1,000-feature pages.

Original successful pages are retained. New responses are not merged.
"""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import requests
import time

ROOT=Path(__file__).resolve().parents[2]

def main():
    originals=[]
    for p in (ROOT/'docs/retrievals').glob('*/manifest.jsonl'):
        originals.extend(json.loads(x) for x in p.read_text().splitlines())
    failed=[r for r in originals if not r['success'] and 'zoning_offset_' in r['file']]
    if not failed:return
    # Retry only offsets for which no successful full or split response exists.
    successful={r.get('params',{}).get('resultOffset') for r in originals
                if r['success'] and r.get('params') and 'resultOffset' in r['params']}
    offsets=sorted({o for r in failed for o in range(r['params']['resultOffset'],r['params']['resultOffset']+5000,1000)
                    if o not in successful})
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    audit=ROOT/'docs/retrievals'/stamp
    audit.mkdir(parents=True,exist_ok=False)
    folder=ROOT/'data/raw/land_use'/stamp
    folder.mkdir(parents=True,exist_ok=False)
    url='https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query'
    def download(offset):
        params={'f':'json','where':'1=1','outFields':'*','returnGeometry':'true',
                'orderByFields':'OBJECTID','resultOffset':offset,'resultRecordCount':1000}
        p=folder/f'zoning_offset_{offset:06}_count_1000.json'
        rec=dict(category='land_use',file=str(p.relative_to(ROOT)),requested_url=url,params=params,
                 retrieved_utc=datetime.now(timezone.utc).isoformat(),kind='data')
        for attempt in range(3):
            try:
                r=requests.get(url,params=params,headers={'User-Agent':'UCLA-ECON430-parking-source-acquisition/1.0','Accept-Encoding':'identity'},timeout=180)
                r.raise_for_status()
                obj=r.json()
                if 'error' in obj:raise ValueError(obj['error'])
                assert len(obj['features'])==1000
                if len(r.content)>60000000:raise ValueError('Unexpected page size')
                with p.open('xb') as f:f.write(r.content)
                rec.update(success=True,status=r.status_code,final_url=r.url,response_headers=dict(r.headers),
                           bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest())
                print('OK',p.name,len(r.content),flush=True)
                return rec
            except Exception as exc:
                rec.update(success=False,error=str(exc))
                if attempt<2:time.sleep(2)
        return rec
    with ThreadPoolExecutor(max_workers=3) as pool:
        for rec in pool.map(download,offsets):
            with (audit/'manifest.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
    if any(not json.loads(x)['success'] for x in (audit/'manifest.jsonl').read_text().splitlines()):
        raise SystemExit('Some retries failed; inspect manifest')

if __name__=='__main__':main()
