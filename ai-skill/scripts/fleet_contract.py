#!/usr/bin/env python3
"""Replay the fleet contract adapter; preserve the corpus-native bundle schema."""
import argparse, hashlib, json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
REQUIRED={'corpus_is_authoritative','missing_means_unknown','cross_corpus_equivalence_requires_explicit_evidence','preserve_uncertainty','preserve_source_independence','preserve_rights'}
LICENSES=['LICENSE','LICENSE-CODE','LICENSE-CONTENT.md','LICENSING.md','NOTICE']
def build(root=ROOT):
    manifest=json.loads((root/'ai-skill/manifest.json').read_text())
    contract=json.loads((root/'ai-skill/references/fleet-contract.json').read_text())
    if set(contract['behavioral_gates'])!=REQUIRED or any(v is not True for v in contract['behavioral_gates'].values()):
        raise ValueError('missing or disabled behavioral gate')
    if contract['scientific_approval_granted'] is not False: raise ValueError('scientific approval prohibited')
    if manifest['master_contract_0_3_1']!='IMPLEMENTED': raise ValueError('contract implementation undeclared')
    paths=set(LICENSES+['ai-skill/SKILL.md','ai-skill/manifest.json','ai-skill/references/authority-profile.json','ai-skill/references/fleet-contract.json','ai-skill/references/corpus-project-contract.md','ai-skill/generated/research-bundle-index.json','ai-skill/scripts/fleet_contract.py','ai-skill/scripts/validate_bundle.py'])
    authority=json.loads((root/'ai-skill/references/authority-profile.json').read_text())
    paths.update(a['path'] for a in authority.get('required_authorities',[]) if a.get('required'))
    native=json.loads((root/'ai-skill/generated/research-bundle-index.json').read_text())
    paths.update(native.get('authoritative_inputs',[]))
    paths.update(native.get('files',[]))
    if authority.get('canonical_dataset'):paths.add(authority['canonical_dataset'])
    paths.update(a['path'] for a in native.get('artifacts',[]))
    artifacts=[]
    for rel in sorted(paths):
        p=(root/rel).resolve()
        if not p.is_relative_to(root.resolve()) or not p.is_file(): raise ValueError('missing or unsafe authority: '+rel)
        data=p.read_bytes(); artifacts.append({'path':rel,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
    skill=(root/'ai-skill/SKILL.md').read_text()
    if 'ai-skill/references/corpus-project-contract.md' not in skill or 'ai-skill/generated/fleet-contract-index.json' not in skill:
        raise ValueError('skill does not route through contract and stale-input check')
    return {'schema_version':'0.3.1','repository':manifest['canonical_project'],'native_bundle_schema_preserved':True,'contract':contract['behavioral_gates'],'scientific_approval_granted':False,'artifacts':artifacts}
def replay(root=ROOT,write=False):
    result=build(root); p=root/'ai-skill/generated/fleet-contract-index.json'
    data=(json.dumps(result,indent=2)+'\n').encode()
    if write:p.write_bytes(data)
    elif not p.is_file() or p.read_bytes()!=data:raise ValueError('stale contract adapter: regenerate with --write')
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args()
    replay(write=a.write);print('PASS: fleet contract adapter, authority hashes and behavioral gates; no scientific certification')
