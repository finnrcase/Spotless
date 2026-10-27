"""Validate current results, preserve all archived cells/data, and write readiness evidence."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

import nbformat
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def verify():
    manifest=json.loads((ROOT/'docs/rubric_completion_manifest.json').read_text())
    execution=json.loads((ROOT/'docs/current_execution_results.json').read_text())
    assert len(execution['runs'])==6 and all(r['status']=='PASS' for r in execution['runs'])
    runs={r['notebook']:r for r in execution['runs']}
    evidence=[]
    original_count=0
    for name,info in manifest['notebooks'].items():
        nb=json.loads((ROOT/'notebooks'/name).read_text(encoding='utf-8'))
        old=nb['cells'][info['historical_offset']:]
        assert [digest(c) for c in old]==info['preserved_sha256'],name
        original_count+=len(old)
        current=nb['cells'][:info['current_cells']]
        nbformat.validate(nbformat.reads(json.dumps({**nb,'cells':current}),as_version=4))
        ids=[c['id'] for c in nb['cells']]
        assert len(ids)==len(set(ids)),name
        code=[c for c in current if c['cell_type']=='code']
        assert len(code)==runs[name]['code_cells']
        assert all(c.get('execution_count') is not None for c in code),name
        assert not any(o['output_type']=='error' for c in code for o in c.get('outputs',[])),name
        number=int(name[:2]);found=[]
        for index,cell in enumerate(current):
            text=''.join(cell['source'])
            m=re.search(r'^## (\d\([a-h]\)) (.+)',text,re.M)
            if m:
                found.append(m[1]);evidence.append({'item':m[1],'heading':m[2],
                   'notebook':name,'cell':index,'status':'Partial' if m[1]=='4(d)' else 'Complete',
                   'evidence':('Cook/leverage implemented; required DFBETAS addition cancelled by user.' if m[1]=='4(d)' else
                     'Current executed code/output and interpretation within this subsection; narrative-only sections reviewed as text.')})
        assert not any(re.search(r'\.dfbetas\b|\bdfbetas\s*=', ''.join(c['source'])) for c in code),name
        letters={1:'abcd',2:'abcdefgh',3:'abcdef',4:'abcdefg',5:'abcde',6:'abcde'}[number]
        assert found==[f'{number}({x})' for x in letters],name
    for name,expected in manifest['data_sha256'].items():
        assert hashlib.sha256((ROOT/'data/processed'/name).read_bytes()).hexdigest()==expected,name
    for path in (ROOT/'notebooks/cleaning').glob('*.ipynb'):
        raw=json.loads(path.read_text(encoding='utf-8'))
        baseline=json.loads(subprocess.check_output(['git','show',f"{manifest['baseline']}:"+path.relative_to(ROOT).as_posix()],cwd=ROOT))
        nbformat.validate(nbformat.reads(json.dumps(raw),as_version=4))
        assert len(raw['cells'])==len(baseline['cells'])
        for current,old in zip(raw['cells'],baseline['cells']):
            comparison=dict(current)
            if not old.get('id'):comparison.pop('id',None)
            assert comparison==old,path.name
    final=json.loads((ROOT/'reports/tables/current_final_results.json').read_text())
    diagnostic=json.loads((ROOT/'reports/tables/current_diagnostics.json').read_text())
    assert final['predictors']==diagnostic['predictors']
    assert diagnostic['bootstrap_draws']==1000
    assert diagnostic.get('dfbetas_status')=='Missing: addition cancelled by user'
    assert 'dfbetas' not in diagnostic and 'any_dfbetas_flags' not in diagnostic
    assert final['n']==diagnostic['n']==4016
    assert diagnostic['robustness']['Restore missing-income spaces']['N']==4060
    assert diagnostic['robustness']['At least 28 active days']['N']==1609
    comparison=json.loads((ROOT/'reports/tables/current_model_comparison.json').read_text())
    for model,row in comparison.items():
        for column,value in row.items():
            assert np.isclose(value,final['model_comparison'][model][column],rtol=1e-8,atol=1e-8),(model,column)
    assert comparison['Model 1']['Slopes']==1 and comparison['Model 2']['Slopes']==3
    # The prior specification is refitted for continuity, not overwritten.
    assert np.isclose(comparison['Prior seven (supporting)']['Adjusted R2'],.27235,atol=5e-6)
    assert np.isclose(comparison['Prior seven (supporting)']['AIC'],-3070.71241,atol=1e-5)
    report=(ROOT/'reports/Spotless_ECON430_Project1.html').read_text(encoding='utf-8')
    assert 'data:image/png;base64,' in report
    assert 'Max absolute DFBETAS' not in report and 'Price DFBETAS' not in report
    for token in ['DFBETAS','Jarque','Pandas Profiling','Confidence Intervals','References',
                  'Original data-construction Python source','Source']:
        assert token in report,token
    assert len(report)>100000
    for name in ['Spotless_ECON430_source.py','Spotless_cleaning_source.py']:
        import ast
        ast.parse((ROOT/'reports'/name).read_text(encoding='utf-8'))
    meta=json.loads((ROOT/'reports/submission_metadata.json').read_text())
    blockers=[]
    if not meta.get('group_members'):blockers.append('All group members’ verified names are deferred to final packaging by the user.')
    if not meta.get('syllabus_policies_reviewed'):blockers.append('Syllabus Assignment Policies review is deferred to final packaging by the user.')
    main=subprocess.check_output(['git','rev-parse','main'],cwd=ROOT,text=True).strip()
    original_main='e480f468a9366603f908f4a7c72ab6c4b5999925'
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    assert branch=='refactor/430-rubric-alignment'
    result={'status':'Current code executes; required DFBETAS is missing by user request; final packaging remains' if blockers else 'Current code executes; required DFBETAS is missing by user request',
            'current_rubric_items':evidence,'historical_cells_preserved':original_count,
            'data_hashes_unchanged':True,'new_model_and_diagnostics_consistent':True,
            'prior_model_metrics_reproduced':True,'html_embedded_images':True,
            'python_source_syntax_valid':True,'main_unchanged_since_initial_inventory':main==original_main,
            'main_modified_by_this_task':False,'main_reference':main,'main_initial_reference':original_main,
            'main_note':'An external pull advanced main to the merge of PR #2 during this task; no main mutation is performed by these tools.' if main!=original_main else 'Main remains at the initial reference.',
            'cleaning_schema_valid_without_method_changes':True,
            'raw_pipeline_reexecuted':False,
            'raw_pipeline_note':'Raw files are absent; current main workflow is reproducible from the unchanged tracked processed CSVs.',
            'remaining_analytical_items':['4(d)-DFBETAS is required by the PDF but its addition was cancelled by the user.'],
            'remaining_packaging_items':blockers}
    (ROOT/'docs/current_readiness.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='current_rubric_items'},indent=2,ensure_ascii=False))
    return result

if __name__=='__main__':verify()
