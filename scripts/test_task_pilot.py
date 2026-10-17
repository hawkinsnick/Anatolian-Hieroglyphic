import tempfile
import unittest
from pathlib import Path
import task_pilot as t


class PilotTests(unittest.TestCase):
    def test_real_metadata_replay_preserves_dispute_and_no_readings(self):
        r = t.build()
        self.assertEqual(r['summary']['metadata_dossiers'], 7)
        self.assertFalse(r['summary']['sign_reading_pilot_executed'])
        self.assertIsNone(r['summary']['independent_witness_count'])
        self.assertEqual(r['cases'][0]['native_record']['period'], 'TRANSITION? / disputed')
        self.assertTrue(all(c['accepted_reading'] is None for c in r['cases']))

    def test_modified_source_refused(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'research').mkdir()
            (root / t.SOURCE).write_text('{"records": []}')
            with self.assertRaisesRegex(ValueError, 'checksum'): t.build(root)


if __name__ == '__main__': unittest.main()
