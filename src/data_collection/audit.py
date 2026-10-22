"""Read-only acquisition audit: checksums, record counts, headers, date extent.

Writes provenance documentation only, never a data table or changed raw file.
This is acquisition validation, not exploratory analysis.
"""
from pathlib import Path
import csv
import hashlib
import json
import zipfile
from collections import Counter
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]

def main():
    records = []
    for manifest in sorted((ROOT/'docs/retrievals').glob('*/manifest.jsonl')):
        for line in manifest.read_text().splitlines():
            rec = json.loads(line)
            if not rec['success']:
                records.append(rec)
                continue
            p = ROOT/rec['file']
            h = hashlib.sha256()
            with p.open('rb') as f:
                for chunk in iter(lambda:f.read(1024*1024), b''):
                    h.update(chunk)
            assert h.hexdigest() == rec['sha256'], f'Hash mismatch: {p}'
            rec['checksum_verified'] = True
            if p.suffix in ['.csv','.txt']:
                dates = []
                n = 0
                spaces = set()
                lo = hi = None
                with p.open(encoding='utf-8-sig',newline='') as f:
                    reader = csv.DictReader(f,delimiter='\t' if p.suffix=='.txt' else ',')
                    rec['columns'] = reader.fieldnames
                    key = next((c for c in reader.fieldnames if c in ['EventTime_UTC','EventTime','DATE']),None)
                    for row in reader:
                        n += 1
                        if 'SpaceID' in row and rec['category']=='ladot_occupancy':
                            spaces.add(row['SpaceID'])
                        if key and row.get(key):
                            val = row[key]
                            try:
                                parsed = datetime.fromisoformat(val)
                            except ValueError:
                                parsed = datetime.strptime(val,'%m/%d/%Y %I:%M:%S %p')
                            if lo is None or parsed < lo[0]: lo = (parsed,val)
                            if hi is None or parsed > hi[0]: hi = (parsed,val)
                rec['rows'] = n
                if spaces:rec['distinct_space_ids'] = len(spaces)
                if lo:rec['raw_timestamp_extent'] = [lo[1],hi[1]]
            elif p.suffix=='.json':
                obj = json.loads(p.read_bytes())
                if 'features' in obj:
                    rec['rows'] = len(obj['features'])
                    rec['exceededTransferLimit'] = obj.get('exceededTransferLimit',False)
                    rec['spatialReference'] = obj.get('spatialReference')
                    rec['columns'] = [f['name'] for f in obj.get('fields',[])]
                elif p.name.startswith('acs'):
                    rec['rows'] = len(obj['data'])
                    rec['release'] = obj.get('release')
                    rec['tables'] = obj.get('tables')
                elif 'schedule' in p.name:
                    games = [g for d in obj['dates'] for g in d.get('games',[])]
                    rec['rows'] = len(games)
                    rec['raw_timestamp_extent'] = [min(g['gameDate'] for g in games),max(g['gameDate'] for g in games)]
            elif p.suffix=='.ics':
                text = p.read_text()
                assert text.startswith('BEGIN:VCALENDAR')
                rec['rows'] = text.count('BEGIN:VEVENT')
                dates = [line.split(':',1)[1] for line in text.splitlines() if line.startswith('DTSTART')]
                rec['raw_timestamp_extent'] = [min(dates),max(dates)]
            elif p.suffix=='.zip':
                with zipfile.ZipFile(p) as z:
                    assert z.testzip() is None
                    rec['members'] = {i.filename: {'bytes':i.file_size,
                        'rows':sum(1 for _ in z.open(i.filename))-1} for i in z.infolist() if not i.is_dir()}
                    if 'calendar.txt' in z.namelist():
                        rows = list(csv.DictReader(z.read('calendar.txt').decode('utf-8-sig').splitlines()))
                        rec['service_date_extent'] = [min(r['start_date'] for r in rows), max(r['end_date'] for r in rows)]
            records.append(rec)
    # Each new complete collection is its own snapshot; recovery pages attach
    # to the most recent preceding source-count snapshot.
    snapshots={Path(r['file']).parent.name:{'ids':[],'count':json.loads((ROOT/r['file']).read_bytes())['count']}
               for r in records if r.get('success') and Path(r['file']).name=='zoning_count.json'}
    for rec in records:
        if rec.get('success') and rec['category']=='land_use':
            p=ROOT/rec['file']
            if not snapshots:continue
            stamp=max(s for s in snapshots if s<=p.parent.name)
            if p.name=='zoning_source_ids.json':
                snapshots[stamp]['source_ids']=json.loads(p.read_bytes())['objectIds']
            if p.name.startswith('zoning_offset_'):
                obj=json.loads(p.read_bytes())
                snapshots[stamp]['ids'].extend(f['attributes']['OBJECTID'] for f in obj['features'])
    for stamp,snapshot in snapshots.items():
        assert len(snapshot['ids'])==snapshot['count'], 'Incomplete zoning pagination'
        assert Counter(snapshot['ids'])==Counter(snapshot['source_ids']), 'Zoning IDs differ from independent source listing'
        print('Complete zoning layer:',len(snapshot['ids']),'records;',len(set(snapshot['ids'])),'distinct IDs. Provider duplicate IDs retained.')
    destination = ROOT/'docs/acquisition_audit.json'
    destination.write_text(json.dumps(records,indent=2))
    print('Verified',sum(r.get('checksum_verified',False) for r in records),'original files')
    for r in records:
        if r.get('rows') is not None:
            print(Path(r['file']).name, r['rows'], r.get('raw_timestamp_extent',r.get('service_date_extent','')))
    assert not list((ROOT/'data/interim').iterdir())
    assert not list((ROOT/'data/processed').iterdir())

if __name__ == '__main__':
    main()
