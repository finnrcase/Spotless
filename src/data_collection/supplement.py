"""Save corrected NOAA documentation and current Metro feed as new originals.

The first acquisition also retained the outdated official GitHub Metro feed;
this script preserves that acquisition while adding the current GitLab source.
"""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import requests

ROOT = Path(__file__).resolve().parents[2]

def main():
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    audit = ROOT/'docs/retrievals'/stamp
    audit.mkdir(parents=True, exist_ok=False)
    jobs = [
        ('weather','isd-format-document.pdf','https://www.ncei.noaa.gov/pub/data/noaa/isd-format-document.pdf'),
        ('other','metro_rail_gtfs.zip','https://gitlab.com/LACMTA/gtfs_rail/-/raw/master/gtfs_rail.zip'),
        ('other','metro_rail_readme.md','https://gitlab.com/LACMTA/gtfs_rail/-/raw/master/README.md'),
    ]
    for category,name,url in jobs:
        h = requests.head(url, allow_redirects=True, timeout=30)
        if int(h.headers.get('Content-Length',0)) > 20000000:
            raise ValueError('Unexpected size')
        r = requests.get(url,headers={'User-Agent':'UCLA-ECON430-parking-source-acquisition/1.0','Accept-Encoding':'identity'},timeout=90)
        r.raise_for_status()
        if 'text/html' in r.headers.get('Content-Type',''):
            raise ValueError('Unexpected HTML')
        p = ROOT/'data/raw'/category/stamp/name
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('xb') as f:
            f.write(r.content)
        rec = dict(category=category,file=str(p.relative_to(ROOT)),requested_url=url,
                   final_url=r.url,retrieved_utc=datetime.now(timezone.utc).isoformat(),
                   status=r.status_code,response_headers=dict(r.headers),head_headers=dict(h.headers),
                   kind='documentation' if name.endswith(('.pdf','.md')) else 'data',
                   bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest(),success=True)
        with (audit/'manifest.jsonl').open('a') as f:
            f.write(json.dumps(rec)+'\n')
        print('OK',p.name,len(r.content))

if __name__ == '__main__':
    main()
