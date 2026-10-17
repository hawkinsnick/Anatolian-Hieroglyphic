#!/usr/bin/env python3
"""Trace available edition metadata without inventing a Luwian sign corpus."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'research/edition-reconciliation-pilot.json'
EXPECTED = '4f6f42fe58fdfc556d662cebf1f4dd25d3deb27c11e4b9234f1ed533dd6c482d'


def build(root=ROOT):
    root = Path(root)
    raw = (root / SOURCE).read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXPECTED:
        raise ValueError('edition metadata checksum differs')
    records = json.loads(raw)['records']
    ids = [r['id'] for r in records]
    if len(ids) != 7 or len(ids) != len(set(ids)):
        raise ValueError('expected seven distinct native metadata IDs')
    rights_path = 'research/rights-source-matrix.json'
    cases = []
    for i, row in enumerate(records):
        cases.append({
            'native_id': row['id'], 'native_record': row,
            'source_locator': {'path': SOURCE, 'sha256': EXPECTED, 'pointer': f'/records/{i}'},
            'edition_locators_reported': {k: v for k, v in row.items() if k.startswith('chli')},
            'direct_edition_consultation_established_by_this_pilot': False,
            'source_sign_occurrences_available_in_this_pilot': False,
            'accepted_reading': None,
            'next_research_step': 'Establish intended-use rights and consult the cited edition at the reported locus. Admit attributed reading-level evidence with exact sign/line locators before comparing a sign or word.',
            'review_question': 'Does the reported edition locator concern this named entry, and what precisely does the consulted source establish? Keep object identity, chronology, reading and source dependence separate.',
        })
    return {
        'format': 'anatolian-hieroglyphic-task-pilot-v1',
        'pilot_id': 'HL-EDITION-TRACE-7-v1',
        'question': 'Which existing metadata dossiers provide routes for a future sign-reading study, and which evidence is still missing?',
        'selection': 'All seven existing edition-metadata-pilot records; no inferred join to the 287 digital-entry dossiers.',
        'reproduction': {'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                         'source_sha256': EXPECTED, 'rights_path': rights_path,
                         'rights_sha256': hashlib.sha256((root / rights_path).read_bytes()).hexdigest()},
        'summary': {'metadata_dossiers': len(cases),
                    'dossiers_with_reported_edition_locators': sum(bool(c['edition_locators_reported']) for c in cases),
                    'sign_reading_pilot_executed': False,
                    'direct_edition_checks_performed': 0,
                    'new_accepted_readings': 0,
                    'independent_witness_count': None},
        'cases': cases,
        'rights': 'Identity/bibliographic metadata only; retain research/rights-source-matrix.json. No CHLI transcriptions, photographs, facsimiles or sign tables are ingested by this pilot.',
        'scientific_status': 'DOCUMENTARY_ROUTING_READY_READING_LEVEL_STUDY_REQUIRES_SOURCE_ADMISSION',
        'scholar_relationship': 'Research-use hypothesis only; no scholar request, participation or endorsement.',
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--write', action='store_true')
    p.add_argument('--check', action='store_true')
    a = p.parse_args()
    result = build()
    out = ROOT / 'analysis/task-pilot-example.json'
    if a.check and json.loads(out.read_bytes()) != result:
        raise SystemExit('pilot result differs')
    if a.write:
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__': main()
