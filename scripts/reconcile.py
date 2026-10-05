"""Offline, reproducible identity/bibliography reconciliation. No reading admission."""
import argparse, collections, hashlib, json, pathlib, re, unicodedata
ROOT=pathlib.Path(__file__).resolve().parents[1]
INPUTS=['research/ediana-list-snapshot.json','research/ediana-edition-snapshot.json','research/monumental-link-snapshot.json','research/ediana-hieroglyphic-entry-register.json']
def load(path): return json.loads((ROOT/path).read_text())
def encode(x): return json.dumps(x,ensure_ascii=False,indent=2)+'\n'
def norm(s): return ' '.join(unicodedata.normalize('NFC',s).upper().split())
def need(ok,msg):
    if not ok: raise ValueError(msg)
def construct(listing, editions, monuments, portable):
    rows=listing['rows']; ids=[r['ediana_id'] for r in rows]
    need(len(ids)==287 and len(set(ids))==287 and set(ids)==set(range(287)), 'identity denominator/duplicate drift')
    need(all(set(r)=={'ediana_id','siglum'} and r['siglum'] for r in rows),'list field leakage')
    idx={r['ediana_id']:r for r in rows}
    refs={}; allowed={'ediana_id','response_siglum','principal_edition_refs','response_sha256'}
    for e in editions['records']:
        i=e['ediana_id']; need(i in idx and i not in refs,'edition orphan/duplicate')
        need(set(e)==allowed,'edition field leakage')
        need(norm(e['response_siglum'])==norm(idx[i]['siglum']),'API/list identity disagreement')
        need(isinstance(e['principal_edition_refs'],list) and all(isinstance(s,str) and s.strip() for s in e['principal_edition_refs']),'invalid bibliography')
        need(re.fullmatch('[0-9a-f]{64}',e['response_sha256']) is not None,'invalid response hash')
        refs[i]=e
    classes={r['ediana_id']:r for r in portable['explicit_nonmonumental_or_portable_entries']}
    need(len(classes)==len(portable['explicit_nonmonumental_or_portable_entries']),'duplicate portable assertion')
    for i,c in classes.items():
        need(i in idx and norm(c['siglum'])==norm(idx[i]['siglum']),'portable identity disagreement')
    by_name=collections.defaultdict(list)
    for m in monuments['rows']:
        need(m['period'] in ('empire','transition','late') and isinstance(m['period_uncertain'],bool),'invalid period assertion')
        need(m['period_uncertain']==('?' in m['source_siglum']),'uncertainty dropped')
        by_name[norm(m['source_siglum'])].append(m)
    entries=[]; edges=[]; authorities={}
    for row in sorted(rows,key=lambda r:r['ediana_id']):
        i=row['ediana_id']; key=f'EDIANA-HL-{i:03d}'; siglum=row['siglum']; ref=refs.get(i)
        hits=by_name[norm(siglum)]
        cls=classes.get(i)
        locators=[]
        for text in ref['principal_edition_refs'] if ref else []:
            aid='BIB-'+hashlib.sha256(text.encode()).hexdigest()[:16]
            kind='CROSS_REFERENCE' if re.match(r'(?i)^(see |cf\. )',text) else ('SOURCE_NOTICE' if text in ('Not in corpus','UNPUBLISHED_PERSONAL_COMMUNICATION_FROM_HAWKINS') else 'BIBLIOGRAPHIC_REFERENCE')
            authorities[aid]={'reference_kind':kind,'id':aid,'citation_as_supplied':text,'verification':'EDIANA_PRINCIPAL_EDITION_FIELD_ONLY'}
            match=re.fullmatch(r'Hawkins (1995a?|2000a?):\s*(.+)',text)
            locators.append({'reference_kind':kind,'authority_id':aid,'citation_as_supplied':text,'work_hint':({'1995':'Hawkins 1995','1995a':'Hawkins 1995','2000':'CHLI I (Hawkins 2000)','2000a':'CHLI I (Hawkins 2000)'}[match[1]] if match else None),'locator_as_supplied':match[2] if match else None,'direct_edition_checked':False})
            edges.append({'from':key,'to':aid,'relation':'EDIANA_REFERENCE_FIELD_'+kind,'independent_witness':False})
        entries.append({'id':key,'ediana_id':i,'siglum':siglum,'identity_type':'DIGITAL_TEXT_ENTRY','canonical_object_admitted':False,'physical_object_count':None,'review_status':'UNADJUDICATED_METADATA','source_url':listing['source_url']+f'?corpus=hieroglyphic&docid={i}','list_locator':f'#h_luwian_table span[docid="{i}"]','object_class':{'value':cls['object_class'] if cls else 'UNKNOWN','basis':'EXPLICIT_SIGLUM_WORDING' if cls else 'NO_SUPPORTED_ASSERTION','source_id':'EDIANA-LIST'},'period_candidates':[{'value':h['period'],'uncertain':h['period_uncertain'],'source_siglum':h['source_siglum'],'source_url':h['target_url'],'basis':'EXACT_NFC_CASE_WHITESPACE_LABEL_MATCH_ONLY','status':'SECONDARY_DISCOVERY_CANDIDATE'} for h in hits],'period_status':'CANDIDATE_MATCH' if hits else 'UNKNOWN','edition_status':'PRINCIPAL_REFERENCE_CAPTURED' if locators else 'UNKNOWN','edition_locators':locators,'group_decomposition':'UNRESOLVED','linguistic_assertions':[]})
        edges.append({'from':key,'to':'EDIANA-LIST','relation':'IDENTIFIED_BY','independent_witness':False})
    return {'schema_version':'2.0','milestone':'COMPLETE_DIGITAL_IDENTITY_AND_BIBLIOGRAPHY_SPINE','denominator':{'type':'DIGITAL_TEXT_ENTRIES','count':287,'physical_object_count':None},'entries':entries,'bibliographic_authorities':sorted(authorities.values(),key=lambda x:x['id']),'source_edges':edges}
def outputs():
    listing,editions,monuments,portable=[load(p) for p in INPUTS]
    register=construct(listing,editions,monuments,portable)
    es=register['entries']
    summary={'schema_version':'1.0','milestone':register['milestone'],'version':'2.0.0','digital_text_entries':len(es),'principal_reference_entries':sum(bool(e['edition_locators']) for e in es),'principal_reference_assertions':sum(len(e['edition_locators']) for e in es),'distinct_reference_items':len(register['bibliographic_authorities']),'bibliographic_reference_assertions':sum(p['reference_kind']=='BIBLIOGRAPHIC_REFERENCE' for e in es for p in e['edition_locators']),'cross_reference_assertions':sum(p['reference_kind']=='CROSS_REFERENCE' for e in es for p in e['edition_locators']),'source_notices':sum(p['reference_kind']=='SOURCE_NOTICE' for e in es for p in e['edition_locators']),'bibliographic_reference_entries':sum(any(p['reference_kind']=='BIBLIOGRAPHIC_REFERENCE' for p in e['edition_locators']) for e in es),'object_class_assertions':sum(e['object_class']['value']!='UNKNOWN' for e in es),'object_class_unknown':sum(e['object_class']['value']=='UNKNOWN' for e in es),'period_candidate_entries':sum(bool(e['period_candidates']) for e in es),'period_conflict_entries':sum(len({p['value'] for p in e['period_candidates']})>1 for e in es),'period_unknown':sum(not e['period_candidates'] for e in es),'canonical_objects':0,'reading_assertions':0,'expert_verified_entries':0,'source_edges':len(register['source_edges']),'acquisition_failures':editions['failures'],'input_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in INPUTS},'register_sha256':hashlib.sha256(encode(register).encode()).hexdigest()}
    lines=['# Digital identity and bibliography dossiers','',f"Version 2.0.0: {len(es)} eDiAna text entries; {summary['principal_reference_entries']} have populated principal-reference fields (including cross-references and source notices). These are metadata dossiers, not independently collated inscriptions.",'','Period candidates are secondary discovery assertions matched only by NFC, case and whitespace. Ranges, aliases and fragments are not expanded or merged. Physical counts, readings and expert verification remain unknown or zero. Missing object class never implies a monumental object. No protected transcription, translation or images are included.','','| eDiAna ID | Siglum | Object class | Period candidate | Principal edition |','|---|---|---|---|---|']
    esc=lambda s:s.replace('|','\\|').replace('\n',' ')
    for e in es:
        period='; '.join(p['value']+(' (?)' if p['uncertain'] else '') for p in e['period_candidates']) or 'Unknown'
        edition='; '.join(p['citation_as_supplied'] for p in e['edition_locators']) or 'Unknown'
        lines.append(f"| [{e['ediana_id']}]({e['source_url']}) | {esc(e['siglum'])} | {e['object_class']['value']} | {period} | {esc(edition)} |")
    lines += ['','## Next machine work','','Authority-supported object classes and dates; explicit aliases and group membership; direct CHLI I/III edition checks. Principal references do not establish current-edition completeness. Expert gates cover disputed readings, sign identity and linguistic interpretation.','']
    bundle={'schema_version':'2.0','project':'Anatolian-Hieroglyphic','version':'2.0.0','milestone':register['milestone'],'authoritative_inputs':INPUTS+['research/digital-entry-dossiers.json','analysis/current-status.json'],'input_sha256':summary['input_sha256'],'register_sha256':summary['register_sha256'],'guardrails':['287 digital entries are not 287 physical objects.','Bibliographic citation is not direct edition collation.','Discovery period candidates are not adjudicated datings.','Unknown object class is not monumental.','Derivative sources are not independent witnesses.','No new reading or linguistic interpretation admitted.']}
    return {'research/digital-entry-dossiers.json':encode(register),'analysis/current-status.json':encode(summary),'docs/DIGITAL-ENTRY-DOSSIERS.md':'\n'.join(lines),'ai-skill/generated/research-bundle-index.json':encode(bundle)}
def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args()
    for name,content in outputs().items():
        path=ROOT/name
        if args.write: path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
        else: need(path.exists() and path.read_text()==content,'stale derived artifact: '+name)
    print('identity/bibliography reconciliation valid')
if __name__=='__main__':main()
