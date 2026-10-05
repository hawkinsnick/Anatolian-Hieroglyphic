import copy, importlib.util, pathlib, pytest
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('reconcile',ROOT/'scripts/reconcile.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def inputs():return [m.load(p) for p in m.INPUTS]
def test_generated_artifacts():
 for path,content in m.outputs().items():assert (ROOT/path).read_text()==content
@pytest.mark.parametrize('attack',['duplicate','orphan','identity','text_leak','uncertainty','portable_identity','hash'])
def test_hostile_source_mutations(attack):
 a=inputs()
 if attack=='duplicate':a[0]['rows'][1]['ediana_id']=a[0]['rows'][0]['ediana_id']
 if attack=='orphan':a[1]['records'][0]['ediana_id']=999
 if attack=='identity':a[1]['records'][0]['response_siglum']='ANOTHER OBJECT'
 if attack=='text_leak':a[1]['records'][0]['translation']='unsupported admission'
 if attack=='uncertainty':a[2]['rows'][0]['period_uncertain']=not a[2]['rows'][0]['period_uncertain']
 if attack=='portable_identity':a[3]['explicit_nonmonumental_or_portable_entries'][0]['siglum']='OTHER'
 if attack=='hash':a[1]['records'][0]['response_sha256']='bad'
 with pytest.raises(ValueError):m.construct(*a)
def test_conflict_survives_and_unknowns_stay_unknown():
 r=m.construct(*inputs());e=next(e for e in r['entries'] if e['siglum']=='KARKAMIŠ A30h')
 assert {p['value'] for p in e['period_candidates']}=={'transition','late'}
 assert all(e['physical_object_count'] is None and not e['canonical_object_admitted'] and e['linguistic_assertions']==[] and e['review_status']=='UNADJUDICATED_METADATA' for e in r['entries'])
 assert all(e['object_class']['value']=='UNKNOWN' for e in r['entries'] if e['ediana_id'] not in {x['ediana_id'] for x in inputs()[3]['explicit_nonmonumental_or_portable_entries']})
 assert all(edge['independent_witness'] is False for edge in r['source_edges'])
def test_no_reference_is_not_a_bibliographic_edition():
 r=m.construct(*inputs());items=[p for e in r['entries'] for p in e['edition_locators']]
 assert any(p['reference_kind']=='CROSS_REFERENCE' for p in items)
 assert any(p['reference_kind']=='SOURCE_NOTICE' for p in items)
 assert all(not p['direct_edition_checked'] for p in items)
 assert next(e for e in r['entries'] if e['ediana_id']==274)['edition_status']=='UNKNOWN'

def test_no_source_orphans():
 r=m.construct(*inputs());targets={a["id"] for a in r["bibliographic_authorities"]}|{s["id"] for s in m.load("data/sources.json")["sources"]}
 assert all(e["to"] in targets for e in r["source_edges"])
