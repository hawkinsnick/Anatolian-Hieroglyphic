#!/usr/bin/env python3
"""Replay a bounded source follow-up and a clearly simulated reviewer exercise."""
import argparse
import hashlib
import json
from pathlib import Path
from evidence_query import Evidence, local
from research_delivery import review_template, validate_review

ROOT = Path(__file__).resolve().parents[1]
SPEC = 'research/review-exercise-2026-10-18.json'
EXAMPLE = 'review/teaching-example.json'
FORM = 'review/followup-response.json'
PACKET = 'review/followup-packet.json'
REPORT = 'analysis/review-walkthrough-audit.json'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(root, path):
    return json.loads(local(root, path).read_bytes())


def validate_followup(root, spec):
    root = Path(root)
    if not spec['demonstration_only'] or spec['human_review_occurred'] or spec['scientific_approval_granted']:
        raise ValueError('teaching is not human review or acceptance')
    if spec['repository'].endswith('/Linear-B'):
        study = read(root, 'research/source-study-2026-10-17.json')
        from source_study import validate_study
        validate_study(study, root)
        acquisition = study['acquisition']
        if acquisition['live_identity_records_acquired'] != 26 or acquisition['linked_linguistic_annotations_acquired'] is not False:
            raise ValueError('metadata must not become delivered annotations')
        return study
    study = read(root, spec['record_path'])
    for key in ('scientific_approval_granted', 'expert_acceptance_added', 'messages_sent',
                'physical_identity_certified', 'independence_established'):
        if study[key] is not False:
            raise ValueError('documentary follow-up cannot promote ' + key)
    if study['canonical_readings_added'] != 0 or study['review_status'] != 'PREPARED_NOT_REVIEWED':
        raise ValueError('no new canonical reading or completed review')
    for pin in study['input_pins']:
        if sha(local(root, pin['path']).read_bytes()) != pin['sha256']:
            raise ValueError('follow-up input pin drift: ' + pin['path'])
    if study['repository'].endswith('/Linear-A'):
        c = study['comparison']
        if c['full_word_reading_pair_collated'] or c['both_original_page_images_checked'] or c['native_sigla_join'] is not None:
            raise ValueError('limited text access is not full page/word collation or native identity')
        if not c['first_position_disagreement_documented'] or not c['qualification_delta']:
            raise ValueError('missing disagreement and qualification scope')
        if any(s['page_image_checked'] or s['full_publication_pdf_acquired'] for s in study['sources']):
            raise ValueError('unacquired publication promoted to full PDF/page inspection')
        if study['claims'][1]['complete_alternative_word_reading'] is not None:
            raise ValueError('do not reconstruct a complete Davis reading from the introduction')
        native = [json.loads(line)['source_record_id'] for line in local(root, 'research/sigla-source-documents.jsonl').read_text().splitlines()]
        if 'PK Zb 21' in native or len(native) != 802:
            raise ValueError('revisit no-join scope against changed native document view')
    else:
        rows = study['reference_candidates']
        old = read(root, 'research/source-study-2026-10-17.json')['attestation_assertions']
        dossiers = read(root, 'research/digital-entry-dossiers.json')['entries']
        for row, assertion in zip(rows, old):
            if any(row[k] is not False for k in ('exact_section_alignment_established', 'linguistic_record_join_applied', 'canonical_acceptance')):
                raise ValueError('reference candidate cannot become an exact reading join')
            if row['match_status'] != 'DOCUMENTARY_REFERENCE_CANDIDATE_ONLY':
                raise ValueError('candidate status promoted')
            for left, right in [('source_assertion_id','assertion_id'), ('source_locator','source_locator'),
                                ('source_case_literal','reported_case_literal'), ('source_form_literal','reported_form_literal'),
                                ('source_attestation','reported_attestation_literal')]:
                if row[left] != assertion[right]:
                    raise ValueError('lost source form, locus or uncertainty scope')
            index = int(row['catalogue_pointer'].removeprefix('/entries/'))
            target = dossiers[index]
            if row['catalogue_candidate_id'] != target['id'] or row['catalogue_siglum'] != target['siglum']:
                raise ValueError('catalogue pointer/identity drift')
        if len(rows) != 4 or len({r['catalogue_candidate_id'] for r in rows}) != 3:
            raise ValueError('four assertions are not four catalogue entries or objects')
        for receipt in study['live_catalogue_receipts']:
            rows = receipt['metadata_projection']
            if len(rows) != 1 or rows[0]['returned_docid'] != receipt['request']['docids']:
                raise ValueError('API metadata request/response identity differs')
    return study


def outputs(root=ROOT):
    root = Path(root)
    spec = read(root, SPEC)
    study = validate_followup(root, spec)
    evidence = Evidence(root)
    target = spec['target']
    dossier = evidence.dossier(target['id'], target['collection'])
    packet = {'format':'followup-review-packet-v1','repository':spec['repository'],
              'status':'PREPARED_NOT_REVIEWED','target':target,
              'provenance':dossier['provenance'],'profile_sha256':evidence.profile_hash,
              'question':spec['question'],'review_questions':study['review_questions'],
              'remaining_gates':study['remaining_gates'],'guide':'docs/REVIEWER-WALKTHROUGH.md',
              'source_access':study.get('sources',[]),'real_response_form':FORM,
              'teaching_example':EXAMPLE,'reviewer':None,'assessment':None,
              'human_review_occurred':False,'scientific_approval_granted':False}
    example = {'format':'review-teaching-example-v1','status':'SIMULATED_MAINTAINER_EXERCISE_NOT_REVIEW',
               'demonstration_only':True,'human_review_occurred':False,'reviewer':None,
               'target':target,'profile_sha256':evidence.profile_hash,'provenance':dossier['provenance'],
               'practice_decision':'MORE_SOURCE_REQUIRED','practice_assessment':spec['practice_assessment'],
               'evidence_inspected_for_this_exercise':'Committed documentary register only; this example is not a new primary-source consultation or a specialist response.',
               'scientific_approval_granted':False,'native_changes_applied':False,
               'submission_warning':'Do not submit or reformat this example as a real review. A real reviewer must independently inspect sources, identify themselves and provide their own assessment.'}
    try:
        validate_review(example, root)
    except (ValueError, KeyError):
        pass
    else:
        raise ValueError('teaching example was accepted as a native review submission')
    form = review_template(target['collection'], target['id'], root)
    audit = {'format':'review-walkthrough-audit-v1','repository':spec['repository'],
             'spec_sha256':sha(local(root,SPEC).read_bytes()),'record_sha256':sha(local(root,spec['record_path']).read_bytes()),
             'code_sha256':sha(Path(__file__).read_bytes()),'profile_sha256':evidence.profile_hash,
             'status':'PASS_DOCUMENTARY_REPLAY_AND_DEMONSTRATION_SEPARATION',
             'human_review_occurred':False,'scientific_approval_granted':False,
             'limitation':'Software replay does not verify original-page fidelity, object identity, permissions, expertise or epigraphic truth.'}
    return {PACKET:packet, FORM:form, EXAMPLE:example, REPORT:audit}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = outputs()
    for path,value in result.items():
        if args.write:
            (ROOT/path).parent.mkdir(parents=True,exist_ok=True)
            (ROOT/path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
        if args.check and read(ROOT,path) != value:
            parser.exit(2, 'walkthrough output drift: '+path+'\n')
    print(json.dumps(result[REPORT],indent=2))


if __name__ == '__main__':
    main()
