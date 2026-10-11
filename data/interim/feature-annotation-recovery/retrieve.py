import requests,json,hashlib,pathlib,concurrent.futures
p=pathlib.Path('data/interim/feature-annotation-recovery')
urls={
'pmc-oa.xml':'https://pmc.ncbi.nlm.nih.gov/utils/oa/oa.fcgi?id=PMC10313767',
'pmc-bioc.xml':'https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/PMC10313767/unicode',
'manuscript-supplement.pdf':'https://pmc.ncbi.nlm.nih.gov/articles/instance/10313767/bin/NIHMS1876412-supplement-supplementary_information.pdf',
'publisher.html':'https://www.nature.com/articles/s41589-023-01276-8'
}
def get(x):
 name,u=x
 try:
  r=requests.get(u,timeout=30); b=r.content; (p/name).write_bytes(b)
  return dict(file=name,url=u,status=r.status_code,content_type=r.headers.get('Content-Type'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 except Exception as e:return dict(file=name,url=u,error=str(e))
rows=list(concurrent.futures.ThreadPoolExecutor(4).map(get,urls.items()));(p/'retrievals.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
