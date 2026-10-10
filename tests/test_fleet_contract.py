import json, runpy, shutil, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE=runpy.run_path(str(ROOT/'ai-skill/scripts/fleet_contract.py'))
class ContractTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.root=Path(self.temp.name)
        shutil.copytree(ROOT,self.root,dirs_exist_ok=True,ignore=shutil.ignore_patterns('.git','__pycache__','.pytest_cache'))
    def tearDown(self):self.temp.cleanup()
    def test_stale_canonical_input_rejected(self):
        index=MODULE['replay'](self.root)
        artifact=next(a for a in index['artifacts'] if a['path'].startswith(('data/','research/')))
        p=self.root/artifact['path'];p.write_bytes(p.read_bytes()+b'\n')
        with self.assertRaises(ValueError):MODULE['replay'](self.root)
    def test_disabled_rights_and_false_approval_rejected(self):
        p=self.root/'ai-skill/references/fleet-contract.json';original=json.loads(p.read_text())
        for key in ('preserve_rights','preserve_source_independence'):
            obj=json.loads(json.dumps(original));obj['behavioral_gates'][key]=False;p.write_text(json.dumps(obj))
            with self.assertRaises(ValueError):MODULE['build'](self.root)
        original['scientific_approval_granted']=True;p.write_text(json.dumps(original))
        with self.assertRaises(ValueError):MODULE['build'](self.root)
    def test_missing_license_rejected(self):
        (self.root/'NOTICE').unlink()
        with self.assertRaises(ValueError):MODULE['build'](self.root)
if __name__=='__main__':unittest.main()
