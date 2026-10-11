from pathlib import Path
import datetime, ftplib, hashlib, json, os, platform

root = Path.cwd()
p = root/'data/raw/blackyeast-sixmsa-inputs-2026-10-09'
p.mkdir(parents=True, exist_ok=True)
inventory = json.loads((root/'data/interim/black-yeast-screen-2026-10-09/massive-inventory.json').read_text())
name = '20231206_Ac-C18_NEG_UMETAB420_14092_EXT_SC_6MSA_C2.raw'
matches = [x for x in inventory['files'] if x['path'].endswith('/'+name)]
assert len(matches) == 1
remote = matches[0]
out = p/name
receipt = p/'retrieval.json'
assert not out.exists() and not receipt.exists(), 'Inspect existing output instead of repeating retrieval'
run = dict(status='running', started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
           pid=os.getpid(), python=platform.python_version(),
           command='python data/interim/black-yeast-screen-2026-10-09/retrieve_sixmsa_raw.py',
           source_inventory='data/interim/black-yeast-screen-2026-10-09/massive-inventory.json',
           remote=remote, output=str(out.relative_to(root)),
           scope='One full source acquisition for candidate-pool reconstruction; not a completed benchmark evaluation')
(p/'run.json').write_text(json.dumps(run,indent=2)+'\n')
try:
    with ftplib.FTP_TLS('massive-ftp.ucsd.edu',timeout=60) as ftp:
        ftp.login(); ftp.prot_p()
        with out.with_suffix('.raw.partial').open('wb') as stream:
            ftp.retrbinary('RETR '+remote['path'],stream.write,blocksize=1048576)
    partial = out.with_suffix('.raw.partial')
    assert partial.stat().st_size == int(remote['size'])
    partial.rename(out)
    result = dict(url='ftp://massive-ftp.ucsd.edu'+remote['path'], transport='FTP_TLS',
                  path=str(out.relative_to(root)).replace('\\','/'), bytes=out.stat().st_size,
                  sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
                  retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    receipt.write_text(json.dumps(result,indent=2)+'\n')
    run.update(status='completed', receipt=str(receipt.relative_to(root)))
    print(json.dumps(result))
except Exception as exc:
    run.update(status='failed', failure=repr(exc))
    raise
finally:
    run['updated_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (p/'run.json').write_text(json.dumps(run,indent=2)+'\n')
