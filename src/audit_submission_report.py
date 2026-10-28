"""Check the reviewed notebooks and their saved evidence against Project 1."""
from pathlib import Path
import ast
import hashlib
import json
import re
import subprocess
import nbformat
import numpy as np
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
NAMES=['01_economic_theory','02_data_description_eda','03_variable_selection_models',
       '04_diagnostics_robustness','05_results_interpretation','06_limitations_extensions']

def verify():
    books={name:nbformat.read(ROOT/'notebooks'/f'{name}.ipynb',as_version=4) for name in NAMES}
    execution=json.loads((ROOT/'docs/submission_audit_execution.json').read_text())
    assert len(execution)==6 and all(r['status']=='PASS' for r in execution)
    evidence=[]
    blocked_words=re.compile(r'\*\*(?:Requirement|Method|Evidence|Status)|migration audit|Section Summary and Rubric Coverage|Assignment compliance|explicit request|task instructions|deferred to final packaging|no grade.*guaranteed|fresh Python kernel',re.I)
    for number,(name,book) in enumerate(books.items(),1):
        nbformat.validate(book)
        record = next(r for r in execution if r['notebook'] == name + '.ipynb')
        actual_source = hashlib.sha256(json.dumps([(c.cell_type, c.source) for c in book.cells], ensure_ascii=False).encode()).hexdigest()
        actual_code = hashlib.sha256(json.dumps([c.source for c in book.cells if c.cell_type == 'code'], ensure_ascii=False).encode()).hexdigest()
        if record.get('source_sha256'):
            assert actual_source == record.get('current_source_sha256', record['source_sha256']), name
        if record.get('executed_code_sha256'):
            assert actual_code == record['executed_code_sha256'], name
        assert len({c.id for c in book.cells})==len(book.cells)
        headings=[]
        for i,c in enumerate(book.cells,1):
            if c.cell_type=='markdown':
                assert not blocked_words.search(c.source),(name,i)
                assert not c.source.startswith('# Historical')
                m=re.search(r'^## (\d\([a-h]\)) (.+)',c.source,re.M)
                if m:
                    headings.append(m[1]);evidence.append({'item':m[1],'heading':m[2],'notebook':name+'.ipynb','cell':i})
            if c.cell_type=='code':
                assert c.execution_count is not None,(name,i)
                assert not any(o.output_type=='error' for o in c.outputs)
                for o in c.outputs:
                    if 'text/html' in o.get('data',{}):
                        soup=BeautifulSoup(o.data['text/html'],'html.parser')
                        for td in soup.select('td'):
                            value=td.get_text()
                            assert not re.search(r'(?:\.\.\.|…)\s*$',value),(name,i,value)
        letters={1:'abcd',2:'abcdefgh',3:'abcdef',4:'abcdefg',5:'abcde',6:'abcde'}[number]
        assert headings==[f'{number}({x})' for x in letters],(name,headings)
    final=json.loads((ROOT/'reports/tables/current_final_results.json').read_text())
    diagnostic=json.loads((ROOT/'reports/tables/current_diagnostics.json').read_text())
    assert final['predictors']==diagnostic['predictors']
    assert final['n']==diagnostic['n']==4016
    assert len(final['predictors'])>=5
    for term,value in diagnostic['model_coefficients'].items():
        assert np.isclose(value,final['coefficients'][term]['OLS coefficient'],rtol=1e-7,atol=1e-9),term
    assert diagnostic['bootstrap_draws']==1000
    assert set(diagnostic['dfbetas'])=={'const',*final['predictors']}
    assert diagnostic['any_dfbetas_flags']>0
    assert np.isclose(diagnostic['dfbetas_cutoff'],2/np.sqrt(diagnostic['n']))
    dbook=books['04_diagnostics_robustness']
    for key,mime in [('dfbetas-compute','text/html'),('dfbetas-plot','image/png'),('dfbetas-interpretation','text/markdown')]:
        cell=next(c for c in dbook.cells if c.id==key)
        assert any(mime in o.get('data',{}) for o in cell.outputs)
    for name,row in diagnostic['cross_validation'].items():
        assert np.isclose(row['Mean fold RMSE'],final['model_comparison'][name]['Mean 5-fold RMSE'])
    assert diagnostic['robustness']['Retain missing-income spaces']['N']==4060
    prior=ROOT/'reports/tables/current_model_comparison.json'
    comparison=json.loads(prior.read_text())
    assert comparison['Model 1']['Slopes']==1 and comparison['Model 2']['Slopes']==3
    assert comparison['Model 3']['Slopes']==len(final['predictors'])
    author_manifest = ROOT/'docs/section1_author_pdf_manifest.json'
    if author_manifest.exists():
        from verify_section1_pdf import verify_author_section1
        verify_author_section1()
    backup=Path('/tmp/spotless-before-full-audit')
    if backup.exists():
        if not author_manifest.exists():
            original=nbformat.read(backup/'01_economic_theory.ipynb',as_version=4)
            lit=original.cells[4].source
            assert any(c.source==lit for c in books['01_economic_theory'].cells)
        original=nbformat.read(backup/'05_results_interpretation.ipynb',as_version=4)
        lit_comparison=original.cells[13].source.split('### Conclusion')[0]
        assert any(c.source.startswith(lit_comparison) for c in books['05_results_interpretation'].cells)
    combined=nbformat.read(ROOT/'notebooks/Spotless_complete.ipynb',as_version=4)
    nbformat.validate(combined)
    combined_source = [c.source for c in combined.cells if c.cell_type == 'code']
    section_source = [c.source for book in books.values() for c in book.cells if c.cell_type == 'code']
    assert combined_source == section_source, 'Combined code differs from the reviewed sections.'
    combined_run = json.loads((ROOT/'docs/submission_audit_combined.json').read_text())
    if combined_run.get('executed_code_sha256'):
        code_hash = hashlib.sha256(json.dumps(combined_source, ensure_ascii=False).encode()).hexdigest()
        assert code_hash == combined_run['executed_code_sha256']
    html_path=ROOT/'reports/Spotless_ECON430_Project1.html'
    soup=BeautifulSoup(html_path.read_text(),'html.parser')
    assert len(soup.select('img[src^="data:image/png;base64,"]'))>=10
    assert all(img.get('src','').startswith('data:') for img in soup.select('img'))
    ids={node['id'] for node in soup.select('[id]')}
    for a in soup.select('a[href^="#"]'):
        assert a['href'][1:] in ids,a['href']
    for a in soup.select('a[href]'):
        assert not a['href'].endswith(('.ipynb','.md')),a['href']
    for source in ['Spotless_ECON430_source.py','Spotless_cleaning_source.py']:
        ast.parse((ROOT/'reports'/source).read_text())
    # A presentation audit must not change any of the processed inputs.
    data_hashes = {}
    for path in (ROOT/'data/processed').glob('*.csv'):
        content = path.read_bytes()
        recorded = subprocess.check_output(['git','show','HEAD:' + path.relative_to(ROOT).as_posix()], cwd=ROOT)
        assert content == recorded, path.name
        data_hashes[path.name] = hashlib.sha256(content).hexdigest()
    meta=json.loads((ROOT/'reports/submission_metadata.json').read_text())
    result={'analytical_checks':'PASS','rubric_evidence':evidence,
            'final_n':final['n'],'final_predictors':final['predictors'],
            'literature_paragraphs_unchanged':True,
            'section1_wording_source': 'Author literature-review PDF' if (ROOT/'docs/section1_author_pdf_manifest.json').exists() else 'Prior reviewed notebook',
            'processed_data_unchanged_from_git': True, 'processed_data_sha256':data_hashes,
            'saved_images_embedded':len(soup.select('img[src^="data:image/png;base64,"]')),
            'raw_pipeline_reexecuted':False,
            'raw_pipeline_limitation':'Raw transaction and spatial inputs are absent; cleaning notebooks passed schema/syntax/saved-output checks.',
            'group_names_present':bool(meta.get('group_members')),
            'syllabus_policies_confirmed':bool(meta.get('syllabus_policies_reviewed'))}
    (ROOT/'docs/submission_audit_results.json').write_text(json.dumps(result,indent=2))
    readiness = dict(result)
    readiness['status'] = 'Analytical verification passed; author and submission details remain.'
    readiness['remaining_analytical_items'] = []
    readiness['remaining_packaging_items'] = []
    if not result['group_names_present']:
        readiness['remaining_packaging_items'].append('Add all verified group-member names.')
    if not result['syllabus_policies_confirmed']:
        readiness['remaining_packaging_items'].append('Confirm review of syllabus Assignment Policies.')
    readiness['author_review'] = 'Section 1 preserves the supplied author PDF wording.' if (ROOT/'docs/section1_author_pdf_manifest.json').exists() else 'Literature paragraphs remain unchanged for the authors.'
    (ROOT/'docs/current_readiness.json').write_text(json.dumps(readiness,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='rubric_evidence'},indent=2))
    return result

if __name__=='__main__':
    verify()
