"""Verify packaged bytes; this is not a scientific-validity assessment."""
import hashlib,json,sys
from pathlib import Path

def main():
    root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
    manifest=json.loads((root/'PUBLIC-MANIFEST.json').read_text(encoding='utf-8'))
    failures=[]
    for name,record in manifest['files'].items():
        p=(root/name).resolve()
        if not p.is_relative_to(root) or not p.is_file():failures.append(name+': missing or unsafe');continue
        with p.open('rb') as f: sha=hashlib.file_digest(f,'sha256').hexdigest()
        if p.stat().st_size!=record['bytes'] or sha!=record['sha256']:failures.append(name+': mismatch')
    print(json.dumps({'checked':len(manifest['files']),'failures':failures,'scope':'File membership and bytes only'},indent=2))
    return bool(failures)

if __name__=='__main__':sys.exit(main())
