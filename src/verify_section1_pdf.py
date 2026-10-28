"""Verify the author PDF's wording, equation tokens and rendered table in Section 1."""
import json
from html import unescape
import re
from pathlib import Path
import nbformat
from bs4 import BeautifulSoup
from nbconvert.filters import markdown2html

ROOT=Path(__file__).resolve().parents[1]

def verify_author_section1(check_export=False):
    manifest=json.loads((ROOT/'docs/section1_author_pdf_manifest.json').read_text())
    book=nbformat.read(ROOT/'notebooks/01_economic_theory.ipynb',as_version=4)
    text='\n'.join(c.source for c in book.cells if c.cell_type=='markdown')
    normalized=re.sub(r'\s+',' ',text.replace(r'\$', '$').replace('$i$', '𝑖').replace('**','')).strip()
    for label,block in manifest['blocks'].items():
        assert re.sub(r'\s+',' ',block).strip() in normalized,label
    for entry in manifest['references']:
        assert entry in normalized,entry
    assert manifest['retained_research_question'] in text
    lit=[c for c in book.cells if c.id.startswith('section1-lit-')]
    actual_paragraphs = [re.sub(r'\s+', ' ', part.replace(r'\$', '$')).strip()
                         for cell in lit for part in cell.source.split('\n\n')
                         if part.strip() and not part.startswith('#')]
    assert actual_paragraphs == manifest['literature_original_paragraphs']
    assert len(actual_paragraphs) == manifest['literature_body_paragraphs']
    model=manifest['equations']['model'];hypotheses=manifest['equations']['hypotheses']
    assert model in text and hypotheses in text
    assert re.findall(r'\\beta_([0-7])',model)==list('01234567')
    for term in ['OccupancyRate','PriceMidpoint','TimeLimitHours','PopulationDensity',
                 'RestaurantRetailCount','DriveAloneShare','TransitShare','RateTypeTOD']:
        assert f'\\mathrm{{{term}}}_i' in model,term
    assert 'H_a &: \\beta_1 < 0' in hypotheses and 'H_0 &: \\beta_1 = 0' in hypotheses
    cell=next(c for c in book.cells if c.id=='section1-expected-signs-table')
    assert cell.cell_type == 'markdown'
    soup=BeautifulSoup(markdown2html(cell.source),'html.parser')
    assert [th.get_text() for th in soup.select('thead th')]==manifest['table_headers']
    actual=[[td.get_text() for td in row.select('td')] for row in soup.select('tbody tr')]
    assert actual==manifest['table_rows']
    assert not any('...' in value or '…' in value for row in actual for value in row)
    if check_export:
        export = (ROOT/'reports/Spotless_ECON430_Project1.html').read_text()
        export_soup = BeautifulSoup(export, 'html.parser')
        visible = re.sub(r'\s+', ' ', export_soup.get_text(' ', strip=True)).strip()
        for entry in manifest['references']:
            assert entry in visible, entry
        assert all(eq in unescape(export) for eq in manifest['equations'].values())
        export_tables = [table for table in export_soup.select('table')
                         if [th.get_text() for th in table.select('thead th')] == manifest['table_headers']]
        assert len(export_tables) == 1
        export_rows = [[td.get_text() for td in row.select('td')]
                       for row in export_tables[0].select('tbody tr')]
        assert export_rows == manifest['table_rows']
        assert len([node for node in export_soup.select('h2')
                    if node.get_text(' ', strip=True).replace('¶', '').strip() == 'References']) == 1
    return {'source':manifest['source_filename'],'verbatim_prose_blocks':len(manifest['blocks']),
            'literature_paragraphs':len(actual_paragraphs),'reference_entries':len(manifest['references']),
            'table_rows':len(actual),'table_columns':4,'equations':2,
            'source_wording_preserved':True,'rendered_table_values_verified':True}

if __name__=='__main__':
    print(json.dumps(verify_author_section1(check_export=True),indent=2))
