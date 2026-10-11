import requests,pathlib,json,hashlib
p=pathlib.Path('data/interim/feature-annotation-recovery'); rows=json.loads((p/'retrievals.json').read_text())
for name,u in [('gnps-user-summary.html','https://gnps.ucsd.edu/ProteoSAFe/user/summary.jsp?user=lkcaesar'),('reporting-summary.pdf','https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41589-023-01276-8/MediaObjects/41589_2023_1276_MOESM2_ESM.pdf')]:
 try:
  r=requests.get(u,timeout=30);(p/name).write_bytes(r.content);row=dict(file=name,url=u,status=r.status_code,content_type=r.headers.get('Content-Type'),bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest());print(row);rows.append(row)
 except Exception as e:rows.append(dict(file=name,url=u,error=str(e)));print(str(e))
(p/'retrievals.json').write_text(json.dumps(rows,indent=2))
