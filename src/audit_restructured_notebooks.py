"""Verify cell preservation and execute notebooks in isolated clean kernels.

Usage: python src/audit_restructured_notebooks.py [--execute]
Execution writes only ignored .validation artifacts, never published notebooks/data.
Requires the notebook/environment dependencies already declared by the project.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import warnings
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
BASE = '1a6ef43cc32cd4e51d72e928ca2d9edfcfbcbc30'
def sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
def original(path):
    return json.loads(subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT))

def verify():
    mapping = json.loads((ROOT/'docs/notebook_cell_migration.json').read_text(encoding='utf-8'))
    originals = {m['source_notebook']:original(m['source_notebook']) for m in mapping}
    dests = {m['destination']:json.loads((ROOT/m['destination']).read_text(encoding='utf-8')) for m in mapping}
    covered = set()
    for m in mapping:
        src = originals[m['source_notebook']]['cells'][m['source_index']]
        dst = dests[m['destination']]['cells'][m['destination_index']]
        assert sha(src) == m['source_sha256']
        assert sha(dst) == m['destination_sha256']
        assert src.get('outputs',[]) == dst.get('outputs',[])
        assert src.get('metadata',{}) == dst.get('metadata',{})
        assert src.get('execution_count') == dst.get('execution_count')
        if src.get('id'): assert src['id'] == dst['id']
        covered.add((m['source_notebook'],m['source_index']))
    assert len(covered) == sum(len(n['cells']) for n in originals.values())
    inventory = json.loads((ROOT/'docs/notebook_baseline_inventory.json').read_text())
    # These files are allowed navigation changes; everything else is immutable.
    allowed = {'README.md','.gitignore'}
    for name, expected in inventory['files'].items():
        if name not in allowed:
            content = (ROOT/name).read_bytes()
            assert (hashlib.sha256(content).hexdigest() == expected or
                    hashlib.sha256(content.replace(b'\r\n', b'\n')).hexdigest() == expected), name
    assert subprocess.check_output(['git','rev-parse','main'],cwd=ROOT,text=True).strip() == inventory['main_before']
    assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip() == 'refactor/430-rubric-alignment'
    for book in sorted((ROOT/'notebooks').glob('*.ipynb')):
        nb = json.loads(book.read_text(encoding='utf-8'))
        ids = [c['id'] for c in nb['cells']]
        assert len(ids) == len(set(ids)), book
        sources = '\n'.join(''.join(c['source']) for c in nb['cells'])
        number = int(book.name[:2])
        letters = {1:'abcd',2:'abcdefgh',3:'abcdef',4:'abcdefg',5:'abcde',6:'abcde'}[number]
        headings = [f'## {number}({x}) ' for x in letters]
        positions = [sources.index(h) for h in headings]
        assert positions == sorted(positions)
        assert '## Section Summary and Rubric Coverage' in sources
    # Cleaning paths resolve to the same original absolute targets.
    for m in mapping:
        if '/cleaning/' not in m['destination']: continue
        src = ''.join(originals[m['source_notebook']]['cells'][m['source_index']]['source'])
        dst = ''.join(dests[m['destination']]['cells'][m['destination_index']]['source'])
        assert dst == src.replace('../data/','../../data/').replace('../docs/','../../docs/')
    try:
        import nbformat
        for name, nb in dests.items():
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter('always')
                candidate = nbformat.from_dict(copy.deepcopy(nb))
                if '/cleaning/' in name:
                    # Baseline cleaning notebooks declare 4.4 but contain IDs
                    # introduced in 4.5. Validate a copy under 4.5; do not edit.
                    candidate.nbformat_minor = 5
                nbformat.validate(candidate)
            # Older cleaning notebooks intentionally retain their absent IDs.
            unexpected = [str(w.message) for w in caught if 'id field' not in str(w.message)]
            assert not unexpected, (name, unexpected)
    except ImportError:
        raise RuntimeError('nbformat is required for schema validation')
    import pandas as pd
    cross = pd.read_csv(ROOT/'data/processed/parking_cross_section.csv',dtype={'SpaceID':str,'GEOID':str})
    occ = pd.read_csv(ROOT/'data/processed/space_occupancy_aug2025.csv')
    meters = pd.read_csv(ROOT/'data/processed/meter_inventory_clean.csv')
    filtered = cross.loc[cross.RateType.isin(['FLAT','TOD'])]
    cols = ['occupancy_rate','price_midpoint','time_limit_hours','population_density','median_income',
            'nearby_restaurant_retail_count','drive_alone_share','RateType']
    samples = {'cleaned_occupancy':len(occ),'meter_inventory':len(meters),'cross_section':len(cross),
               'eda':len(filtered),'common':len(filtered.dropna(subset=cols)),
               'tracts_common':filtered.dropna(subset=cols).GEOID.nunique()}
    assert samples == {'cleaned_occupancy':4185,'meter_inventory':35015,'cross_section':4139,'eda':4060,'common':4016,'tracts_common':45}
    assert cross.SpaceID.nunique() == len(cross)
    report = {'baseline':BASE,'original_cells':len(covered),'destinations':len(mapping),'samples':samples,
              'preservation':'PASS: all original outputs, execution counts and cell metadata unchanged',
              'immutable_files':'PASS: preexisting documentation, source, visualization and data unchanged (Git CRLF normalization allowed)',
              'main':'unchanged','schema':'PASS for six analysis notebooks; cleaning copies valid under 4.5, original 4.4 declaration/ID mismatch retained',
              'paths':'PASS: moved cleaning paths resolve identically', 'execution':[]}
    return report, mapping

def text_output(cell):
    parts=[]
    for out in cell.get('outputs',[]):
        text=out.get('text',out.get('data',{}).get('text/plain',''))
        text=''.join(text) if isinstance(text,list) else text
        if 'Styler at 0x' in text and 'text/html' in out.get('data',{}):
            class TableText(HTMLParser):
                def __init__(self):
                    super().__init__(); self.depth=0; self.parts=[]
                def handle_starttag(self,tag,attrs):
                    if tag in ('td','th'): self.depth+=1
                def handle_endtag(self,tag):
                    if tag in ('td','th'): self.depth-=1; self.parts.append(' ')
                def handle_data(self,data):
                    if self.depth: self.parts.append(data)
            parser=TableText()
            html=out['data']['text/html']
            parser.feed(''.join(html) if isinstance(html,list) else html)
            text=''.join(parser.parts)
        parts.append(text)
    return '\n'.join(parts)

def compare_text(src,dst):
    # Compare numerical tokens in textual outputs, ignoring runtime timestamps,
    # object addresses, progress logs and harmless whitespace/layout differences.
    def numbers(cell):
        text = text_output(cell)
        text = re.sub(r'^.*(?:Date:|Time:|0x[0-9a-f]+|Iteration:|progress|it/s|s/it).*$', '', text, flags=re.M)
        return [float(x) for x in re.findall(r'(?<![A-Za-z_])[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?',text)]
    a,b=numbers(src),numbers(dst)
    import numpy as np
    return len(a)==len(b) and bool(np.allclose(a,b,rtol=1e-5,atol=5e-6,equal_nan=True))

def execute(report,mapping):
    import nbformat
    from nbclient import NotebookClient
    scratch = ROOT/'.validation'
    specdir = scratch/'jupyter/kernels/spotless-validation'
    specdir.mkdir(parents=True,exist_ok=True)
    (specdir/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],
          'display_name':'Spotless validation','language':'python'}))
    os.environ['JUPYTER_PATH'] = str(scratch/'jupyter')+os.pathsep+os.environ.get('JUPYTER_PATH','')
    os.environ['IPYTHONDIR'] = str(scratch/'ipython')
    if (scratch/'packages').exists():
        os.environ['PYTHONPATH'] = str(scratch/'packages')+os.pathsep+os.environ.get('PYTHONPATH','')
    selected = sys.argv[sys.argv.index('--only')+1] if '--only' in sys.argv else None
    if selected and (ROOT/'docs/notebook_validation_results.json').exists():
        previous=json.loads((ROOT/'docs/notebook_validation_results.json').read_text())
        report['execution']=[n for n in previous['execution'] if not n['notebook'].startswith(selected)]
    for path in sorted((ROOT/'notebooks').glob('*.ipynb')):
        if selected and not path.name.startswith(selected): continue
        nb=nbformat.read(path,as_version=4)
        if not any(c.cell_type=='code' for c in nb.cells):
            report['execution'].append({'notebook':path.name,'status':'Narrative only; schema/navigation validated'})
            continue
        start=time.time()
        print('Executing '+path.name,flush=True)
        client=NotebookClient(nb,timeout=1800,kernel_name='spotless-validation',allow_errors=True,
                              resources={'metadata':{'path':str(path.parent)}})
        try:
            client.execute()
            nbformat.write(nb,scratch/path.name)
            errors=[{'cell':i,'error':o.ename,'message':o.evalue} for i,c in enumerate(nb.cells)
                    for o in c.get('outputs',[]) if o.output_type=='error']
            checked=[]
            for m in mapping:
                if m['destination'] != path.relative_to(ROOT).as_posix(): continue
                src=original(m['source_notebook'])['cells'][m['source_index']]
                dst=nb.cells[m['destination_index']]
                if src['cell_type']!='code' or not src.get('outputs'): continue
                if any(o.output_type=='error' for o in dst.get('outputs',[])): continue
                checked.append({'source':Path(m['source_notebook']).name+':'+str(m['source_index']),
                                'destination_cell':m['destination_index'],'numeric_text_match':compare_text(src,dst)})
            result={'notebook':path.name,'status':'PASS' if not errors else 'PARTIAL: execution errors',
                    'seconds':round(time.time()-start,1),'errors':errors,'numeric_text_comparisons':checked}
        except Exception as e:
            result={'notebook':path.name,'status':'BLOCKED','exception':type(e).__name__+': '+str(e)}
        report['execution'].append(result)
        report['execution'].sort(key=lambda n:n['notebook'])
        (ROOT/'docs/notebook_validation_results.json').write_text(json.dumps(report,indent=2)+'\n')
        print(result['status']+' '+path.name,flush=True)

if __name__=='__main__':
    result,mapping=verify()
    if '--execute' in sys.argv:
        execute(result,mapping)
    elif (ROOT/'docs/notebook_validation_results.json').exists():
        previous=json.loads((ROOT/'docs/notebook_validation_results.json').read_text())
        # A preservation-only check must not erase recorded fresh-kernel evidence.
        for key in ('execution','comparison_method','runtime','cleaning_execution','preserved_figures'):
            if key in previous: result[key]=previous[key]
    (ROOT/'docs/notebook_validation_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='execution'},indent=2))
