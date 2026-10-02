import json,pathlib
R=pathlib.Path(__file__).parents[1]
def load(p): return json.loads((R/p).read_text())
def test_boundary():
 p=load('project.json'); x=load('research/pre-expert-maximum.json'); a=load('ai-skill/references/authority-profile.json')
 assert p['canonical_records']==0
 assert x['target']=='PRE_EXPERT_MAXIMUM'
 assert len(x['human_only_boundary'])>=3
 assert any(r['role']=='pre_expert_maximum' for r in a['required_authorities'])
