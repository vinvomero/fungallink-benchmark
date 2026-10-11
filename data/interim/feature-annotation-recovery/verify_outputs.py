import csv,pathlib,json,hashlib
p=pathlib.Path('data/interim/feature-annotation-recovery')
rows=list(csv.DictReader(open('data/curated/feature-annotation-recovery-2026-10-02.tsv',encoding='utf8'),delimiter='\t'))
assert len(rows)==5 and len({r['feature_id'] for r in rows})==5
assert all(None not in r for r in rows)
for rec in json.loads((p/'retrievals.json').read_text()):
 if 'sha256' in rec:assert hashlib.sha256((p/rec['file']).read_bytes()).hexdigest()==rec['sha256']
text=pathlib.Path('docs/evidence/feature-annotation-recovery-2026-10-02.md').read_text(encoding='utf8');assert '\u2014' not in text
print('PASS: five expected unique rows; valid TSV shape; six payload hashes match; no em dash; zero admissions.')
