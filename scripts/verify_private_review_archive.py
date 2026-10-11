"""Verify archive bytes without extracting, executing code or validating science."""
import argparse
import hashlib
import json
from pathlib import PurePosixPath
import zipfile

def verify(path):
    with zipfile.ZipFile(path) as archive:
        names=archive.namelist()
        if len(names)!=len(set(names)):
            raise ValueError("Duplicate archive paths")
        if any(PurePosixPath(n).is_absolute() or ".." in PurePosixPath(n).parts or "\\" in n or ":" in n for n in names):
            raise ValueError("Unsafe archive path")
        manifest=json.loads(archive.read("REVIEW-MANIFEST.json"))
        expected=set(manifest["files"])|{"REVIEW-MANIFEST.json"}
        if set(names)!=expected:
            raise ValueError("Archive membership mismatch")
        for name, record in manifest["files"].items():
            h=hashlib.sha256();size=0
            with archive.open(name) as handle:
                for block in iter(lambda:handle.read(1024*1024),b""):
                    h.update(block);size+=len(block)
            if size!=record["bytes"] or h.hexdigest()!=record["sha256"]:
                raise ValueError("Payload mismatch: "+name)
    return {"status":"passed","payloads":len(manifest["files"]),"scope":"Archive membership and bytes only, not scientific validation or permission to share."}

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive")
    print(json.dumps(verify(parser.parse_args().archive),indent=2))
