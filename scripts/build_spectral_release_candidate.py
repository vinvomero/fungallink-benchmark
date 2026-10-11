"""Build a private, hash-checked spectral candidate without changing scientific files."""
import csv
import hashlib
import json
from pathlib import Path
import shutil
import sys
import zipfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'data/processed/spectral-release-candidate-v1-2026-10-11'
SCOPE = 'data/manifests/spectral-release-scope-draft-v3-2026-10-11.tsv'
REPRO = 'data/interim/spectral-arithmetic-reproduction-2026-10-11/receipt.json'
TABLE = 'data/interim/admitted-input-coverage-2026-10-09/spec2class/MIBiG2.0_compounds_with_AS_BGC_CF_NPC_classes.txt'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
    if DEST.exists():
        raise FileExistsError('Candidate already exists; preserve it and choose a new version')
    with (ROOT / SCOPE).open(encoding='utf-8', newline='') as handle:
        rows = list(csv.DictReader(handle, delimiter='\t'))
    if len(rows) != 83 or len({r['path'] for r in rows}) != 83:
        raise ValueError('Unexpected spectral inventory')
    selected = {}
    for row in rows:
        path = ROOT / row['path']
        if digest(path) != row['sha256'] or path.stat().st_size != int(row['bytes']):
            raise ValueError('Inventory changed: ' + row['path'])
        if row['proposed_disposition'].startswith('proposed_include'):
            selected[row['path']] = row['sha256']
    if len(selected) != 77:
        raise ValueError('Unexpected proposed inclusion count')
    original_selected = set(selected)
    reproduction = json.loads((ROOT / REPRO).read_text(encoding='utf-8'))
    for name, expected in reproduction['copied_files'].items():
        if digest(ROOT / name) != expected:
            raise ValueError('Reproduction input changed: ' + name)
        if name != TABLE:
            selected[name] = expected
    extras = [SCOPE, REPRO, 'data/manifests/npclassscore-method.json',
              'docs/release/npclassscore-dependency-route-2026-10-11.md',
              'docs/release/spectral-dependency-dispositions-2026-10-11.md',
              'docs/release/spectral-arithmetic-reproduction-2026-10-11.md',
              'protocol/sixmsa-class-linking-diagnostic-v1.md',
              'planning/spectral-sequence-disposition-2026-10-11.json',
              'scripts/build_spectral_release_candidate.py']
    for name in extras:
        selected[name] = digest(ROOT / name)
    for name in selected:
        p = Path(name)
        if p.is_absolute() or '..' in p.parts or not (ROOT / p).resolve().is_relative_to(ROOT):
            raise ValueError('Unsafe package path: ' + name)
    workspace = DEST / 'workspace'
    workspace.mkdir(parents=True)
    for name, expected in selected.items():
        target = workspace / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
        if digest(target) != expected:
            raise ValueError('Copy verification failed: ' + name)
    asset = json.loads((ROOT / 'data/manifests/npclassscore-method.json').read_text(encoding='utf-8'))['reference_asset']
    dependencies = {
        'scope': 'Saved-class arithmetic reproduction only; full raw processing and predictor inference are outside this candidate.',
        'required_external_files': [dict(path=TABLE, **asset)],
        'runtime': 'Python standard library; verified previously with Python 3.13.5 on Windows. No third-party Python packages needed for saved-class verification.',
        'historical_dependencies': 'Raw acquisitions, MZmine, Spec2Class source, binary and SVM weights, and original environments are not bundled. Frozen run records document these; see docs/release/spectral-dependency-dispositions-2026-10-11.md.',
    }
    (workspace / 'DEPENDENCIES.json').write_text(json.dumps(dependencies, indent=2) + '\n', encoding='utf-8')
    (workspace / 'README.md').write_text('''# Private spectral release candidate, version 1

This is a proposed spectral supplement for owner review, not an authorized public release or the full FungalLink benchmark. No license for original contributions has been selected here.

The current benchmark has 30 admitted relationships across 16 query identities. Eleven relationships have complete evaluated coverage. These two spectral diagnostics remain partial and add zero complete evaluations: 6-MSA scores 291 of 1,249 candidates; ilicicolin H scores 89 of 98. Seventeen FAC/HEx relationships still lack usable inputs. The authoritative admission ledger remains in the main project, outside this spectral-only candidate.

Frozen manifests and curation records retain historical candidate-only, not-admitted and not-ready fields. Those fields describe their original snapshots and are not the current admission ledger. Do not rewrite them or infer that biological admission supplies missing method inputs. Historical local paths are provenance, not portable commands.

The package preserves 77 proposed files from the 83-file inventory, plus reproduction code, saved genomic classes, protocols and attribution records. Six excluded source files remain in the private project: two redundant CSV exports, three runtime pickle files and one execution log. SHA256SUMS.json covers every payload other than itself. The external class table and predictor weights are not bundled.

To reproduce the saved-class arithmetic, extract this archive to a separate directory. Retrieve the exact table described in DEPENDENCIES.json using docs/release/npclassscore-dependency-route-2026-10-11.md. Its destination directory is included. Then run from the extracted root:

```
python -I scripts/verify_saved_spectral_diagnostics.py --root .
```

This checks saved input/output hashes and reconstructs all 1,347 rows and partial-rank bounds. It does not repeat predictor inference, raw measurement processing, sequence annotation or scientific adjudication. It is not independent biological validation. Unknown or missing classes remain unavailable.

Source datasets: MSV000101420 for 6-MSA and MSV000095813 for Trichoderma. The former query sequence is from the Saccharomyces expression host, not proof of a black-yeast genome in the assay. The latter is a QM6a reference window, not an authenticated mutant genome. Source terms, accession attribution and pinned external dependencies retain their separate scopes.

The Caesar comparative benchmark, running phylogeny comparison, full manuscript and final public-release decisions remain in the main project. Relative links inside retained historical records may point outside this deliberately limited candidate; DEPENDENCIES.json and this README define the executable reproduction boundary.
''', encoding='utf-8')
    hashes = {p.relative_to(workspace).as_posix(): digest(p) for p in sorted(workspace.rglob('*')) if p.is_file()}
    (workspace / 'SHA256SUMS.json').write_text(json.dumps(hashes, indent=2) + '\n', encoding='utf-8')
    archive = DEST / 'fungallink-spectral-private-candidate-v1.zip'
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(workspace.rglob('*')):
            if p.is_file():
                z.write(p, p.relative_to(workspace).as_posix())
    with zipfile.ZipFile(archive) as z:
        if set(z.namelist()) != set(hashes) | {'SHA256SUMS.json'}:
            raise ValueError('Archive membership mismatch')
        for name, expected in hashes.items():
            if hashlib.sha256(z.read(name)).hexdigest() != expected:
                raise ValueError('Archive hash mismatch: ' + name)
    receipt = dict(status='built_and_archive_hashes_verified', utc=datetime.now(timezone.utc).isoformat(),
                   command=[sys.executable, 'scripts/build_spectral_release_candidate.py'], python=sys.version,
                   inventory_sha256=digest(ROOT/SCOPE), selected_inventory_files=len(original_selected),
                   additional_source_files=len(set(selected)-original_selected), payload_files=len(hashes),
                   archive=str(archive.relative_to(ROOT)), archive_bytes=archive.stat().st_size,
                   archive_sha256=digest(archive), scope='Private packaging integrity only; no scientific correctness or public approval implied')
    (DEST / 'build-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    build()
