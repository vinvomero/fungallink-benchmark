"""Restore the three exact upstream assets without replacing existing files."""
import hashlib,json,sys
from pathlib import Path
from urllib.request import urlopen,Request

def main():
    root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
    rows=json.loads((root/'UPSTREAM-INPUTS.json').read_text(encoding='utf-8'))
    receipt=[]
    for row in rows:
        p=(root/row['path']).resolve()
        if not p.is_relative_to(root):raise ValueError('Path escapes root')
        existing=p.exists()
        if existing:raw=p.read_bytes()
        else:
            with urlopen(Request(row['url'],headers={'User-Agent':'FungalLink/1.0 public reproduction'}),timeout=120) as r:raw=r.read()
        sha=hashlib.sha256(raw).hexdigest()
        if sha!=row['sha256'] or len(raw)!=row['bytes']:raise ValueError('Upstream bytes differ: '+row['path'])
        if not existing:
            p.parent.mkdir(parents=True,exist_ok=True)
            with p.open('xb') as f:f.write(raw)
        receipt.append({'path':row['path'],'url':row['url'],'sha256':sha,'status':'existing_verified' if existing else 'downloaded_verified'})
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
