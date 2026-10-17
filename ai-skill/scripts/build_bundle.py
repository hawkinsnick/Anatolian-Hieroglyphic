"""Refresh a corpus-native bundle without changing its native fields or evidence counts."""
import hashlib,json,os,subprocess,runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
index_path=ROOT/'ai-skill/generated/research-bundle-index.json';index=json.loads(index_path.read_text());profile=json.loads((ROOT/'ai-skill/references/authority-profile.json').read_text())
native=runpy.run_path(str(ROOT/'scripts/reconcile.py'))['outputs'](True)
index.update(json.loads(native['ai-skill/generated/research-bundle-index.json']))
paths=set(index.get('authoritative_inputs',[]))|set(index.get('files',[]))|{a['path'] for a in index.get('artifacts',[])}|{a['path'] for a in profile['required_authorities'] if a.get('required',True)}
paths|={'ai-skill/SKILL.md','ai-skill/references/authority-profile.json','ai-skill/scripts/build_bundle.py','ai-skill/scripts/validate_bundle.py'}
paths|={'scripts/test_native_evidence_query.py', 'scripts/evidence_query.py', 'analysis/evidence-query-coverage.json', 'research/evidence-query-profile.json', 'docs/EVIDENCE-AND-ALTERNATIVES.md'}
paths|={'analysis/attribution-review-audit.json', 'research/attribution-review.json', 'scripts/attribution_review.py', 'scripts/test_attribution_review.py', 'docs/ATTRIBUTION-REVIEW.md'}
paths |= {p for _,p in [("research_delivery", p) for p in ['scripts/research_delivery.py','scripts/test_research_delivery.py','docs/RESEARCH-DELIVERY.md','analysis/research-delivery.json']]}
if any(p.startswith('ai-skill/generated/') for p in paths):raise ValueError('native source inputs cannot include generated bundle cycles')
paths |= {'scripts/task_pilot.py', 'analysis/task-pilot-example.json', 'docs/RESEARCH-TASK-PILOT.md', 'scripts/test_task_pilot.py'}
old={a['path']:a for a in index.get('artifacts',[])};artifacts=[]
for p in sorted(paths):
 f=(ROOT/p).resolve()
 if not f.is_relative_to(ROOT) or not f.is_file():raise ValueError('missing or unsafe native authority '+p)
 raw=f.read_bytes();artifacts.append({**old.get(p,{'path':p,'role':'native_authority'}),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
index['artifacts']=artifacts
if 'collection_evidence_fingerprint' in index:index['collection_evidence_fingerprint']=json.loads((ROOT/'research/collection-work-ledger.json').read_text())['evidence_fingerprint']
if 'input_sha256' in index:index['input_sha256']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in index['authoritative_inputs']}
source=os.environ.get('SOURCE_COMMIT') or subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();index['source_commit']=source
index_path.write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
(ROOT/'ai-skill/generated/source-state.json').write_text(json.dumps({'schema_version':'1.0','source_commit':source,'bundle_index':'ai-skill/generated/research-bundle-index.json','native_schema_preserved':True},indent=2)+'\n')
runpy.run_path(str(ROOT/'ai-skill/scripts/fleet_contract.py'))['replay'](ROOT,True)
print('Native fields preserved; refreshed authority hashes and exact source commit:',source)
