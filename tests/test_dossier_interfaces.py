"""Detect omission of the full source-bound register in researcher interfaces."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def test_full_dossier_api_and_lossless_export():
    expected = json.loads((ROOT / 'research/digital-entry-dossiers.json').read_text())['entries']
    assert len(expected) == 287
    raw = subprocess.check_output([sys.executable, str(ROOT / 'scripts/research_api.py'), 'entries', '--limit', '300'])
    assert json.loads(raw)['records'] == expected
    with tempfile.TemporaryDirectory() as folder:
        target = Path(folder) / 'full.json'
        subprocess.run([sys.executable, str(ROOT / 'scripts/export_research_layer.py'), 'json', str(target)], check=True)
        assert json.loads(target.read_text()) == expected
        assert json.loads(target.with_suffix('.json.manifest.json').read_text())['records'] == 287


def test_browser_preserves_dossier_rows():
    import runpy
    builder = runpy.run_path(str(ROOT / 'scripts/build_corpus_browser.py'))
    rows = builder['build']()['records']
    dossiers = [r['record'] for r in rows if r['source'] == 'research/digital-entry-dossiers.json']
    assert dossiers == json.loads((ROOT / 'research/digital-entry-dossiers.json').read_text())['entries']
