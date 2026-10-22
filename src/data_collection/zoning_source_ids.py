"""Save source ID listing for independent pagination verification, duplicates intact."""
from pathlib import Path
from datetime import datetime, timezone
import requests, hashlib, json

ROOT=Path(__file__).resolve().parents[2]
def main():
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    url='https://maps.lacity.org/arcgis/rest/services/Mapping/NavigateLA/MapServer/75/query'
    params={'f':'json','where':'1=1','returnIdsOnly':'true'}
    r=requests.get(url,params=params,headers={'Accept-Encoding':'identity'},timeout=90)
    r.raise_for_status()
    assert 'objectIds' in r.json()
    p=ROOT/'data/raw/land_use'/stamp/'zoning_source_ids.json'
    p.parent.mkdir(parents=True,exist_ok=False)
    with p.open('xb') as f:f.write(r.content)
    rec=dict(category='land_use',file=str(p.relative_to(ROOT)),requested_url=url,params=params,
             final_url=r.url,retrieved_utc=datetime.now(timezone.utc).isoformat(),kind='metadata',
             success=True,status=r.status_code,response_headers=dict(r.headers),bytes=len(r.content),
             sha256=hashlib.sha256(r.content).hexdigest())
    audit=ROOT/'docs/retrievals'/stamp
    audit.mkdir(parents=True,exist_ok=False)
    (audit/'manifest.jsonl').write_text(json.dumps(rec)+'\n')
    print('Saved source IDs, including provider duplicate IDs')
if __name__=='__main__':main()
