import copy
import json
import tempfile
import unittest
from pathlib import Path
import review_walkthrough as w
from research_delivery import validate_review


class WalkthroughTests(unittest.TestCase):
    def test_checked_outputs_replay(self):
        for path, value in w.outputs().items():
            self.assertEqual(w.read(w.ROOT,path),value)

    def test_example_and_draft_are_not_reviews(self):
        result=w.outputs()
        for path in (w.EXAMPLE,w.FORM):
            with self.assertRaises(ValueError):validate_review(result[path])
        self.assertIsNone(result[w.EXAMPLE]['reviewer'])
        self.assertTrue(result[w.EXAMPLE]['demonstration_only'])

    def test_teaching_cannot_claim_actual_review(self):
        spec=w.read(w.ROOT,w.SPEC)
        for key,value in [('demonstration_only',False),('human_review_occurred',True),('scientific_approval_granted',True)]:
            bad=copy.deepcopy(spec);bad[key]=value
            with self.assertRaises(ValueError):w.validate_followup(w.ROOT,bad)

    def test_domain_boundary_mutation_rejected(self):
        spec=w.read(w.ROOT,w.SPEC)
        original=w.read
        def changed(root,path):
            d=original(root,path)
            if path==spec['record_path']:
                if spec['repository'].endswith('/Linear-B'):d['acquisition']['linked_linguistic_annotations_acquired']=True
                elif spec['repository'].endswith('/Linear-A'):d['claims'][1]['complete_alternative_word_reading']='INFERRED'
                else:d['reference_candidates'][2]['source_form_literal']='URBS-mi-ni'
            return d
        w.read=changed
        try:
            with self.assertRaises(ValueError):w.validate_followup(w.ROOT,spec)
        finally:w.read=original

    def test_documentary_claims_cannot_grant_scientific_acceptance(self):
        spec=w.read(w.ROOT,w.SPEC)
        original=w.read
        def changed(root,path):
            d=original(root,path)
            if path==spec['record_path']:d['expert_acceptance_added']=True
            return d
        w.read=changed
        try:
            with self.assertRaises(ValueError):w.validate_followup(w.ROOT,spec)
        finally:w.read=original


if __name__=='__main__':unittest.main()
