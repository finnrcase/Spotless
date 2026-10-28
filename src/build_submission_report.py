"""Export the reviewed report notebooks, embedded figures, and Python source."""
from pathlib import Path
import ast
import copy
import html
import hashlib
import subprocess
import importlib.metadata
import json
import re

import nbformat
from nbconvert import HTMLExporter

ROOT = Path(__file__).resolve().parents[1]
REPORT_NAMES = [
    '01_economic_theory', '02_data_description_eda',
    '03_variable_selection_models', '04_diagnostics_robustness',
    '05_results_interpretation', '06_limitations_extensions',
]

def python_source(notebooks, working_directory):
    lines = [
        '"""Spotless ECON 430: analysis source exported from the report notebooks."""',
        'from pathlib import Path', 'import os',
        f'os.chdir(Path(__file__).resolve().parents[1] / {working_directory!r})', '',
    ]
    for name, notebook in notebooks:
        lines.append('# ' + name)
        for cell in notebook.cells:
            if cell.cell_type == 'markdown':
                for line in cell.source.splitlines():
                    if line.startswith('#'):
                        lines.append('# ' + line.lstrip('# '))
            elif cell.cell_type == 'code':
                source = '\n'.join(line for line in cell.source.splitlines()
                                   if not line.strip().startswith('%matplotlib'))
                lines.extend([source, ''])
    result = '\n'.join(lines) + '\n'
    ast.parse(result)
    return result


def build():
    reports = ROOT / 'reports'
    reports.mkdir(exist_ok=True)
    meta_path = reports / 'submission_metadata.json'
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    members = meta.get('group_members', [])
    byline = '\n\n' + ', '.join(members) if members else ''
    combined = nbformat.v4.new_notebook(metadata={
        'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
        'language_info': {'name': 'python'},
    })
    combined.cells.append(nbformat.v4.new_markdown_cell(
        '# Parking Occupancy in Los Angeles\n\nECON 430: Project 1' + byline))
    books = []
    author_references = []
    for name in REPORT_NAMES:
        book = nbformat.read(ROOT / 'notebooks' / (name + '.ipynb'), as_version=4)
        books.append((name, book))
        for source_cell in book.cells:
            if name == '01_economic_theory' and source_cell.id == 'section1-author-references':
                author_references = source_cell.source.split('### References', 1)[1].strip().split('\n\n')
                continue
            cell = copy.deepcopy(source_cell)
            if name == '06_limitations_extensions' and cell.cell_type == 'markdown' and cell.source.startswith('### References') and author_references:
                data_references = [line for line in cell.source.splitlines()
                                   if line.startswith('- ') and not line.startswith(('- Shoup,', '- Pierce,'))]
                cell.source = '# References\n\n' + '\n\n'.join(author_references + data_references)
            if cell.cell_type == 'markdown':
                # A single document uses internal links rather than notebook-file links.
                cell.source = re.sub(r'\([^()\s]+\.ipynb#(section-[^)]+)\)', r'(#\1)', cell.source)
                cell.source = re.sub(r'^(#{1,5}) ', lambda m: m[1] + '# ', cell.source, flags=re.M)
                cell.source = cell.source.replace('../docs/', '../docs/')
            cell.id = f'report-{len(combined.cells):03d}'
            combined.cells.append(cell)
    version_names = ['numpy','pandas','scipy','statsmodels','scikit-learn',
                     'matplotlib','boruta','ydata-profiling']
    execution_path = ROOT / 'docs/current_execution_results.json'
    recorded_versions = json.loads(execution_path.read_text()).get('versions', {}) if execution_path.exists() else {}
    versions = {name: recorded_versions.get(name) or importlib.metadata.version(name)
                for name in version_names}
    versions_table = '\n'.join(f'| {name} | {version} |' for name,version in versions.items())
    data_revision = subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip()
    data_hash = hashlib.sha256((ROOT/'data/processed/parking_cross_section.csv').read_bytes()).hexdigest()
    data_url = f'https://github.com/finnrcase/Spotless/blob/{data_revision}/data/processed/parking_cross_section.csv'
    input_reference = (f'\n\nThe analysis starts from the fixed [space-level cross-section]({data_url}) '
                       f'(4,139 matched spaces before the report restrictions). Its SHA-256 is `{data_hash}`. '
                       'The report uses the 4,016 common complete cases after the stated restrictions. '
                       'The executed environment uses Python 3.12; the accompanying requirements lock records dependencies.')

    combined.cells.append(nbformat.v4.new_markdown_cell(
        '## Section 7: Code Quality and Reproducibility\n\n'
        'The analysis uses a fixed space-level dataset, explicit variable units and a common '
        'complete-case sample. Random seeds are 10 for Boruta and five-fold validation and '
        '90095 for the 1,000-replication bootstrap. Data-based tables, figures and coefficient interpretations '
        'are generated programmatically. The accompanying Python source contains the analysis and '
        'original data-construction steps.\n\n'
        '| Package | Version |\n|---|---|\n' + versions_table + input_reference))
    combined.cells[-1].id = f'report-{len(combined.cells)-1:03d}'
    nbformat.validate(combined)
    nbformat.write(combined, ROOT / 'notebooks/Spotless_complete.ipynb')
    main_source = python_source(books, 'notebooks')
    cleaning = [(path.stem, nbformat.read(path, as_version=4))
                for path in sorted((ROOT/'notebooks/cleaning').glob('*.ipynb'))]
    cleaning_source = python_source(cleaning, 'notebooks/cleaning')
    (reports/'Spotless_ECON430_source.py').write_text(main_source)
    (reports/'Spotless_cleaning_source.py').write_text(cleaning_source)
    exporter = HTMLExporter(template_name='lab')
    exporter.exclude_input = True
    exporter.exclude_input_prompt = True
    exporter.exclude_output_prompt = True
    body, _ = exporter.from_notebook_node(combined)
    source_appendix = (
        '<section class="source-appendix"><h2>Appendix: Python Source Code</h2>'
        '<details><summary>Analysis source</summary><pre><code>' + html.escape(main_source) +
        '</code></pre></details><details><summary>Data-construction source</summary><pre><code>' +
        html.escape(cleaning_source) + '</code></pre></details></section>')
    css = '''<style>
body { max-width: 1200px; margin: auto; }
.jp-RenderedHTMLCommon table { max-width:100%; }
.jp-RenderedHTMLCommon th, .jp-RenderedHTMLCommon td {
 white-space:normal; overflow-wrap:anywhere; text-align:left;
}
.jp-RenderedHTMLCommon td code {white-space:normal; overflow-wrap:anywhere;}
.jp-OutputArea-output { overflow:visible; }
.jp-RenderedHTMLCommon p { line-height:1.6; }
.source-appendix { margin:2em; }
.source-appendix pre { white-space:pre-wrap; overflow-wrap:anywhere; }
@media print { .jp-Cell { break-inside:auto; } img { max-width:100%; } }
</style>'''
    body = body.replace('</head>', css+'</head>').replace('</body>',source_appendix+'</body>')
    body = '\n'.join(line.rstrip() for line in body.splitlines()) + '\n'
    (reports/'Spotless_ECON430_Project1.html').write_text(body)
    print('Exported six report sections, combined notebook, Section 7, embedded images, and both source appendices.')
    print('Group names present:', bool(members))

if __name__ == '__main__':
    build()
