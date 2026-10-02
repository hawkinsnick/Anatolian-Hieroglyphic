import json,pathlib
R=pathlib.Path(__file__).parents[1]
def L(p): return json.loads((R/p).read_text())
def test_boundary():
 p=L('project.json'); x=L('research/pre-expert-maximum.json'); a=L('ai-skill/references/authority-profile.json')
 assert p['canonical_records']==0 and x['target']=='PRE_EXPERT_MAXIMUM' and len(x['human_only_boundary'])>=3
 assert any(r['role']=='pre_expert_maximum' for r in a['required_authorities'])
def test_release_assurance():
 for p in ['research/evidence-matrix.json','research/rights-register.json','research/source-lineage.json','research/expert-review-packet.json','research/acquisition-queue.json']: L(p)
 assert L('research/catalogue-register.json')['status']=='DISCOVERY_REGISTER'
 assert 'independent' in L('research/source-lineage.json')['independence_rule'].lower()
