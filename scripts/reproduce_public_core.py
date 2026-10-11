"""Replay the released core from its immutable nested package."""
import argparse,hashlib,json,subprocess,sys,zipfile
from pathlib import Path
from datetime import datetime,timezone

def main():
    ap=argparse.ArgumentParser();ap.add_argument('root',nargs='?',default='.');ap.add_argument('--all-rosters',action='store_true');ap.add_argument('--output',default='public-core-replay');args=ap.parse_args()
    root=Path(args.root).resolve();out=(root/args.output).resolve()
    if out.exists():raise FileExistsError('Use a new output directory: '+str(out))
    archive=root/'data/processed/core-numerical-candidate-v1-2026-10-11/fungallink-core-numerical-private-v1.zip'
    out.mkdir(parents=True)
    with zipfile.ZipFile(archive) as z:
        for name in z.namelist():
            if not (out/name).resolve().is_relative_to(out):raise ValueError('Unsafe member')
        manifest=json.loads(z.read('MANIFEST.json'))
        for name,r in manifest['files'].items():
            raw=z.read(name)
            if len(raw)!=r['bytes'] or hashlib.sha256(raw).hexdigest()!=r['sha256']:raise ValueError(name)
        z.extractall(out)
    records=[]
    for track in ['expanded','emericellamide','acetylaszonalenin']:
        command=[sys.executable,'-I','-S','-B',track+'/reproduce.py']+(['--all-rosters'] if args.all_rosters else [])
        run=subprocess.run(command,cwd=out,capture_output=True,text=True)
        (out/(track+'-stdout.txt')).write_text(run.stdout,encoding='utf-8');(out/(track+'-stderr.txt')).write_text(run.stderr,encoding='utf-8')
        records.append({'track':track,'command':command,'returncode':run.returncode})
        if run.returncode:raise RuntimeError(track+' failed; inspect retained logs')
    receipt={'utc':datetime.now(timezone.utc).isoformat(),'state':'complete','scope':'All rosters' if args.all_rosters else 'Primary roster; four methods across three tracks','python':sys.version,'runs':records,'scientific_validation':False}
    (out/'public-replay.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
