"""Acquire public identifiers and bibliography only; discard linguistic text in memory.
Run explicitly, never in offline validation. Requires beautifulsoup4.
"""
import concurrent.futures, hashlib, json, pathlib, urllib.parse, urllib.request, time
from bs4 import BeautifulSoup
ROOT = pathlib.Path(__file__).resolve().parents[1]
URL = 'https://www.ediana.gwi.uni-muenchen.de/corpus.php'
def save(path, value):
    (ROOT/path).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
def get(url, data=None):
    return urllib.request.urlopen(urllib.request.Request(url, data=data, headers={'User-Agent':'AH-corpus-metadata-reconciliation/2.0'}), timeout=45).read()
def fetch(ids):
    data=urllib.parse.urlencode({'searchterms':'{}','corpus_text':'true','language':'hieroglyphic','docids':','.join(map(str,ids))}).encode()
    try:
        raw=get('https://www.ediana.gwi.uni-muenchen.de/includes/api.php',data)
        response=json.loads(raw)
        out=[]
        for label, rows in response.items():
            if not rows: continue
            head=rows[0]
            out.append({'ediana_id':int(head['docid']), 'response_siglum':label,
                        'principal_edition_refs':[('UNPUBLISHED_PERSONAL_COMMUNICATION_FROM_HAWKINS' if v.startswith('Annotation conducted based on the personal communication') else v) for v in head.get('ref',[])], 'response_sha256':hashlib.sha256(raw).hexdigest()})
        return out, None
    except Exception as exc:
        return [], {'ids':ids, 'error':str(exc)}
def main():
    raw=get(URL); soup=BeautifulSoup(raw,'html.parser')
    rows=[{'ediana_id':int(n['docid']),'siglum':n.get_text(strip=True)} for n in soup.select('#h_luwian_table span[docid]')]
    assert len(rows)==287 and {r['ediana_id'] for r in rows}==set(range(287)), 'Live denominator drift: review before replacing register'
    observed=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
    save('research/ediana-list-snapshot.json',{'schema_version':'1.0','source_url':URL,'observed_at':observed,'response_sha256':hashlib.sha256(raw).hexdigest(),'selector':'#h_luwian_table span[docid]','rows':rows})
    editions=[]; failures=[]
    batches=[list(range(i,min(i+7,287))) for i in range(0,287,7)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for ix,(data,error) in enumerate(pool.map(fetch,batches)):
            editions.extend(data)
            if error: failures.append(error)
            print('metadata batches',ix+1,'/',len(batches),flush=True)
            save('research/ediana-edition-snapshot.json',{'schema_version':'1.0','source_url':'https://www.ediana.gwi.uni-muenchen.de/includes/api.php','observed_at':observed,'request_fields':{'language':'hieroglyphic','corpus_text':'true','searchterms':'{}'},'extraction':'response label, first row docid and ref only; linguistic fields discarded','records':sorted(editions,key=lambda x:x['ediana_id']),'failures':failures})
if __name__=='__main__': main()
