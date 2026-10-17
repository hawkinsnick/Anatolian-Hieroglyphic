#!/usr/bin/env python3
"""Replay source-study bindings and prepared review packets; never grant acceptance."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from evidence_query import Evidence, local
from research_delivery import review_template

ROOT = Path(__file__).resolve().parents[1]
STUDY = 'research/source-study-2026-10-17.json'
PACKET = 'review/source-study-packet.json'
FORM = 'review/source-study-response.json'
REPORT = 'analysis/source-study-audit.json'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def validate_study(study, root=ROOT):
    root = Path(root)
    if study['format'] != 'specialist-source-study-v1':
        raise ValueError('unsupported study format')
    if study['canonical_readings_added'] != 0 or any(study[k] is not False for k in
            ('expert_acceptance_added', 'calibration_executed', 'messages_sent')):
        raise ValueError('study must not grant readings, acceptance, calibration or outreach')
    if study['review_status'] != 'PREPARED_NOT_REVIEWED':
        raise ValueError('prepared study is not an actual independent review')
    for pin in study['input_pins']:
        if sha(local(root, pin['path']).read_bytes()) != pin['sha256']:
            raise ValueError('study input pin differs: ' + pin['path'])
    ids = [s['source_id'] for s in study['sources']]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError('duplicate or missing source identity')
    for source in study['sources']:
        if source['source_payload_redistributed'] is not False or source['independent_object_witness_established'] is not False:
            raise ValueError('source access is not republication or independent autopsy')
        if not re.fullmatch('[0-9a-f]{64}', source['receipt']['sha256']):
            raise ValueError('missing exact acquired source hash')
        if not source['rights'] or Path(source['local_verification_filename']).name != source['local_verification_filename']:
            raise ValueError('missing rights or unsafe source filename')
    claims = study['claims']
    if len({c['claim_id'] for c in claims}) != len(claims):
        raise ValueError('duplicate claim ID')
    if any(c['source_id'] not in ids or not c['locator'] for c in claims):
        raise ValueError('claim without source and locus')
    repo = study['repository']
    if repo.endswith('/Linear-B'):
        acquisition = study['acquisition']
        for k in ('same_snapshot_word_crosswalk_acquired', 'linked_linguistic_annotations_acquired', 'certified_graphical_baseline_acquired'):
            if acquisition[k] is not False:
                raise ValueError('identity metadata cannot promote annotation/gold delivery')
        projection = json.loads((root / 'research/damos-live-pilot-2026-10-17.json').read_bytes())
        expected = json.loads((root / 'research/task-pilot.json').read_bytes())['document_ids'] + ['4307']
        rows = projection['rows']
        if [r['source_record_id'] for r in rows] != expected or len(set(expected)) != 26:
            raise ValueError('live identity projection scope drift')
        for row in rows:
            if row['source_id_assertion']['value'] != row['source_record_id']:
                raise ValueError('returned source identity differs')
            if any(row[k] is not False for k in ('linguistic_annotation_payload_acquired', 'physical_word_ids_acquired', 'physical_identity_certified')):
                raise ValueError('live metadata promoted to linguistic or physical evidence')
            if row['snapshot_compatibility_with_registered_derivative'] is not None:
                raise ValueError('same-snapshot compatibility remains unknown')
            if set(row['reported_metadata']) != {'heading', 'heading_short', 'heading_short_new', 'inventory', 'timestamp'}:
                raise ValueError('unexpected source payload projection')
        if acquisition['live_identity_records_acquired'] != len(rows):
            raise ValueError('live record count differs')
    elif repo.endswith('/Linear-A'):
        comparison = study['comparison']
        if comparison['question_type'] != 'SCRIPT_ASSIGNMENT_NOT_COMPETING_WORD_TRANSCRIPTIONS':
            raise ValueError('classification is not a word-reading pair')
        if comparison['source_reading_pair_established'] is not False or comparison['two_independent_physical_witnesses_established'] is not False:
            raise ValueError('documentary disagreement promoted to reading pair/witnesses')
        if comparison['native_sigla_record_join'] is not None:
            raise ValueError('no inferred native identity join')
        if [c['author_preference'] for c in claims] != ['Linear B', 'Linear A'] or any(c['adopted_by_project'] is not False for c in claims):
            raise ValueError('author disagreement or no-adoption boundary differs')
    elif repo.endswith('/Anatolian-Hieroglyphic'):
        rows = study['attestation_assertions']
        if len(rows) != 4 or len({r['assertion_id'] for r in rows}) != 4:
            raise ValueError('four selected Table1 assertions required')
        if any(r['canonical_acceptance'] is not False or r['native_entry_join'] is not None or r['physical_occurrence_geometry'] is not None for r in rows):
            raise ValueError('reported attestation promoted to certified native occurrence')
        if rows[1]['reported_case_literal'] != 'dat.-loc.s.?' or rows[1]['reported_form_literal'] != 'URBS-mi-ni':
            raise ValueError('row2 uncertainty belongs to case classification')
        if rows[2]['reported_case_literal'] != 'dat.-loc.s.' or rows[2]['reported_form_literal'] != 'URBS-mi-ni?':
            raise ValueError('row3 uncertainty belongs to written form')
        if [r['source_locator']['row'] for r in rows] != [1, 2, 3, 4]:
            raise ValueError('Table1 row locators differ')
        if study['comparison']['earlier_name_analysis_directly_consulted'] is not False or study['comparison']['preferred_by_project'] is not None:
            raise ValueError('reported earlier analysis is not independent consultation/adoption')
    else:
        raise ValueError('unknown native study repository')
    return study


def outputs(root=ROOT):
    root = Path(root)
    study_raw = (root / STUDY).read_bytes()
    study = validate_study(json.loads(study_raw), root)
    evidence = Evidence(root)
    dossier = evidence.dossier(study['study_id'], 'source-study')
    packet = {
        'format': 'specialist-source-review-packet-v1', 'repository': study['repository'],
        'study_id': study['study_id'], 'status': 'PREPARED_NOT_REVIEWED',
        'study_provenance': dossier['provenance'], 'profile_sha256': evidence.profile_hash,
        'question': study['question'], 'review_questions': study['review_questions'],
        'source_requirements': [{'source_id': s['source_id'], 'citation': s['citation'],
                                 'receipt': s['receipt'], 'locators': s['consultation_pages'],
                                 'rights': s['rights']} for s in study['sources']],
        'native_dossier_command': f'python scripts/research_delivery.py --dossier {study["study_id"]} --collection source-study',
        'response_form': FORM, 'reviewer': None, 'assessment': None,
        'scientific_approval_granted': False, 'native_changes_applied': False,
        'remaining_gates': study['remaining_gates'],
        'boundary': 'Packet preparation and structural validation do not authenticate expertise, source independence or epigraphic truth. No outreach is sent.'}
    form = review_template('source-study', study['study_id'], root)
    report = {'format': 'specialist-source-study-audit-v1', 'repository': study['repository'],
              'study_id': study['study_id'], 'study_sha256': sha(study_raw),
              'code_sha256': sha(Path(__file__).read_bytes()),
              'source_count': len(study['sources']), 'claim_count': len(study['claims']),
              'result_status': study['result_status'], 'packet_status': packet['status'],
              'reviewer': None, 'expert_acceptance_added': False,
              'inputs': study['input_pins'], 'source_replay_required_for_primary_verification': True}
    return {PACKET: packet, FORM: form, REPORT: report}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--write', action='store_true')
    p.add_argument('--check', action='store_true')
    p.add_argument('--verify-sources', type=Path)
    a = p.parse_args()
    results = outputs()
    for path, result in results.items():
        if a.write:
            (ROOT / path).parent.mkdir(parents=True, exist_ok=True)
            (ROOT / path).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        if a.check and json.loads((ROOT / path).read_bytes()) != result:
            p.exit(2, 'source study packet/report drift: ' + path + '\n')
    if a.verify_sources:
        study = json.loads((ROOT / STUDY).read_bytes())
        for source in study['sources']:
            path = a.verify_sources / source['local_verification_filename']
            if sha(path.read_bytes()) != source['receipt']['sha256']:
                p.exit(2, 'primary source byte mismatch: ' + source['source_id'] + '\n')
    print(json.dumps(results[REPORT], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
