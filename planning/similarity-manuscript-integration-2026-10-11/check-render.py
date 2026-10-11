"""Read-only text coverage check for the two current rendered documents."""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import hashlib, json, re

ROOT=Path(__file__).resolve().parents[2]
HERE=ROOT/'manuscript/similarity-integration-render-2026-10-11'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):return ''.join(c for c in s if c.isalnum())
units=[]
for prefix,stem,folder in [('', 'benchmark-paper-review',ROOT/'manuscript'),('methods-','Supplementary-Methods',HERE)]:
    r=json.loads((HERE/f'{prefix}render-receipt.json').read_text())
    source=Path(r['source']);docx=folder/f'{stem}.docx';pdf=folder/f'{stem}.pdf'
    assert sha(source)==r['source_sha256'] and sha(docx)==r['docx_sha256'] and sha(pdf)==r['pdf_sha256']
    texts=[]
    for page in range(1,r['page_count']+1):
        lines=(HERE/f'{prefix}page-{page:02d}.txt').read_text(encoding='utf8').splitlines()
        while lines and not lines[-1].strip():lines.pop()
        if lines and lines[-1].strip()==str(page):lines.pop()
        if lines and lines[0].strip()==str(page):lines.pop(0)
        texts.append('\n'.join(lines))
    with ZipFile(docx) as z:xml=etree.fromstring(z.read('word/document.xml'))
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    paras=[''.join(p.xpath('.//w:t/text()',namespaces=ns)) for p in xml.xpath('//w:p',namespaces=ns)]
    missing=[p for p in paras if p and norm(p) not in norm(''.join(texts))]
    assert not missing,missing
    units.append({'source':source.relative_to(ROOT).as_posix(),'source_sha256':sha(source),
                  'docx':docx.relative_to(ROOT).as_posix(),'docx_sha256':sha(docx),
                  'pdf':pdf.relative_to(ROOT).as_posix(),'pdf_sha256':sha(pdf),'pages':r['page_count'],
                  'missing_pdf_paragraphs':len(missing),'paragraph_and_cell_text_matches':True})
result={'status':'passed','units':units,'visual_review':'Worker and host inspected all 25 pages via seven contact sheets; host checked text geometry with no out-of-page blocks. No visible clipping or overlap.',
        'host_review':'planning/similarity-manuscript-integration-2026-10-11/host-render-review.json',
        'commands':['bundled Python render.py','PowerShell export.ps1 (owned hidden Word instance)','bundled Python rasterize.py; matching --methods switch for supplement'],
        'renderer_reuse':'Existing Word COM/PDFium route reused; prior standard-renderer missing-LibreOffice failure remains in manuscript/trichoderma-integration-verification-2026-10-11.json.',
        'scope':'Current main and Supplementary Methods only; comparative results and historical render manifest untouched.'}
(HERE/'final-manifest.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
print(json.dumps(result,indent=2))
