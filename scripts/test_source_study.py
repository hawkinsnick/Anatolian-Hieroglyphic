import copy
import json
import unittest
from pathlib import Path
import source_study as s
from research_delivery import validate_review


class SourceStudyTests(unittest.TestCase):
    def setUp(self):
        self.study = json.loads((s.ROOT / s.STUDY).read_bytes())

    def test_native_study_and_packet_replay(self):
        result = s.outputs()
        for path, value in result.items():
            self.assertEqual(json.loads((s.ROOT / path).read_bytes()), value)
        self.assertIsNone(result[s.PACKET]['reviewer'])
        self.assertIsNone(result[s.PACKET]['assessment'])
        self.assertFalse(result[s.PACKET]['scientific_approval_granted'])

    def test_acceptance_outreach_or_calibration_promotion_rejected(self):
        for key in ('expert_acceptance_added', 'calibration_executed', 'messages_sent'):
            bad = copy.deepcopy(self.study);bad[key] = True
            with self.subTest(key=key), self.assertRaises(ValueError): s.validate_study(bad)
        bad = copy.deepcopy(self.study);bad['canonical_readings_added'] = 1
        with self.assertRaises(ValueError): s.validate_study(bad)

    def test_source_attribution_and_pin_drift_rejected(self):
        bad = copy.deepcopy(self.study);bad['claims'][0]['source_id'] = 'UNCONSULTED'
        with self.assertRaises(ValueError): s.validate_study(bad)
        bad = copy.deepcopy(self.study);bad['input_pins'][0]['sha256'] = '0' * 64
        with self.assertRaises(ValueError): s.validate_study(bad)

    def test_prepared_form_cannot_be_passed_as_review(self):
        form = s.outputs()[s.FORM]
        with self.assertRaises(ValueError): validate_review(form)
        forged = copy.deepcopy(form);forged['status'] = 'SUBMITTED_FOR_MAINTAINER_CHECK';forged['scientific_approval_granted'] = True
        with self.assertRaises(ValueError): validate_review(forged)

    def test_corpus_specific_interpretation_boundaries(self):
        bad = copy.deepcopy(self.study)
        if bad['repository'].endswith('/Linear-B'):
            bad['acquisition']['linked_linguistic_annotations_acquired'] = True
        elif bad['repository'].endswith('/Linear-A'):
            bad['comparison']['source_reading_pair_established'] = True
        else:
            bad['attestation_assertions'][2]['reported_form_literal'] = 'URBS-mi-ni'
        with self.assertRaises(ValueError): s.validate_study(bad)


if __name__ == '__main__': unittest.main()
