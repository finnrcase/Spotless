"""Execute the report sections in fresh kernels using the active Python environment."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import sys
import time

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

from build_submission_report import REPORT_NAMES, ROOT, build


def source_digest(notebook):
    source = [(cell.cell_type, cell.source) for cell in notebook.cells]
    return hashlib.sha256(json.dumps(source, ensure_ascii=False).encode()).hexdigest()


def execute(path, working_directory=None):
    notebook = nbformat.read(path, as_version=4)
    digest = source_digest(notebook)
    manager = KernelManager(kernel_name='python3')
    manager.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
    started = time.monotonic()
    print('Running', path.name, flush=True)
    NotebookClient(notebook, timeout=600, km=manager,
                   resources={'metadata': {'path': str(working_directory or path.parent)}}).execute()
    nbformat.validate(notebook)
    assert not any(output.output_type == 'error'
                   for cell in notebook.cells for output in cell.get('outputs', []))
    assert source_digest(notebook) == digest
    nbformat.write(notebook, path)
    result = {'notebook': path.name, 'status': 'PASS',
              'seconds': round(time.monotonic() - started, 1),
              'code_cells': sum(cell.cell_type == 'code' for cell in notebook.cells),
              'kernel_working_directory': str((working_directory or path.parent).relative_to(ROOT)),
              'source_sha256': digest,
              'executed_code_sha256': hashlib.sha256(json.dumps([cell.source for cell in notebook.cells if cell.cell_type == 'code'], ensure_ascii=False).encode()).hexdigest()}
    print(json.dumps(result), flush=True)
    return result


def run(include_combined=False, start_section=1, kernel_root=False):
    if sys.version_info >= (3, 14):
        raise SystemExit('Use Python 3.12: the project Profiling dependency does not support Python 3.14.')
    processed = ROOT / 'data/processed'
    before = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
              for path in processed.glob('*.csv')}
    previous_path = ROOT / 'docs/submission_audit_execution.json'
    previous = json.loads(previous_path.read_text()) if previous_path.exists() else []
    results = [r for r in previous if int(r['notebook'][:2]) < start_section]
    if start_section > 1:
        assert len(results) == start_section - 1, 'Earlier execution records are required for excluded sections.'
    for name in REPORT_NAMES[start_section - 1:]:
        result = execute(ROOT / 'notebooks' / (name + '.ipynb'), ROOT if kernel_root else None)
        results.append(result)
        (ROOT / 'docs/submission_audit_execution.json').write_text(json.dumps(results, indent=2))
    version_names = ['numpy','pandas','scipy','statsmodels','scikit-learn',
                     'matplotlib','boruta','ydata-profiling','geopandas',
                     'nbclient','nbconvert','ipykernel']
    (ROOT / 'docs/current_execution_results.json').write_text(json.dumps({
        'python': sys.version,
        'versions': {name: importlib.metadata.version(name) for name in version_names},
        'runs': results
    }, indent=2))
    build()
    if include_combined:
        result = execute(ROOT / 'notebooks/Spotless_complete.ipynb', ROOT if kernel_root else None)
        (ROOT / 'docs/submission_audit_combined.json').write_text(json.dumps(result, indent=2))
    after = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
             for path in processed.glob('*.csv')}
    assert before == after, 'Processed data changed during report execution.'
    from audit_submission_report import verify
    verify()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--include-combined', action='store_true')
    parser.add_argument('--start-section', type=int, choices=[1, 2], default=1)
    parser.add_argument('--kernel-root', action='store_true')
    arguments = parser.parse_args()
    run(arguments.include_combined, arguments.start_section, arguments.kernel_root)
