"""One-time manuscript integration; no scientific calculations or score changes."""
from pathlib import Path
import csv, hashlib, json, shutil

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')

owned = ['manuscript/benchmark-paper-review.md', 'manuscript/Supplementary-Methods.md',
         'manuscript/claim-evidence.tsv', 'manuscript/benchmark-paper-review-claim-map.json',
         'docs/release/reproduction-stages-v1.md', 'docs/release/release-map-v1.md']
for path in owned:
    dest = WORK / 'before' / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists(): shutil.copy2(ROOT / path, dest)

p = ROOT / owned[0]
s = p.read_text(encoding='utf-8-sig')
assert '### Similarity and dependence' not in s
methods = '''### Similarity and dependence

A separate companion analysis measures resemblance only where retained representations permit comparison, without changing labels, retrieval scores or frozen analysis groups. Supported structures use binary Morgan fingerprints with radius 2, 2,048 bits, bond types enabled and chirality disabled; Tanimoto is the fraction of shared set bits in their union. Chiral sensitivity is withheld because source identifiers do not resolve the stereochemical distinctions in the supplied structures. Compatible source-annotated core proteins use global BLOSUM62 alignment with gap opening −10 and extension −0.5, including terminal gaps. Identity is identical residues divided by paired nongap residues, with coverage reported against both full sequences. Protein-content fractions use all displayed annotated proteins as denominators and qualifying core matches as numerators; they are lower bounds, not whole-cluster similarity estimates.

Within each native joined spectral pool, peaks below m/z 10, within ±1 Da of a known precursor, or below 1% of the base peak are removed. Square-root intensities are L2-normalized before CosineHungarian matching at 0.02 Da. Resemblance flags require cosine at least 0.7 and six matched peaks; 0.9 is a stricter sensitivity. Typed dependence edges distinguish shared queries, curated pathways, construct/host context, sequence identity and spectral resemblance. Reference membership is assessed against declared retained assets separately from model-training membership. The [protocol](../protocol/similarity-independence-v1.md), [report](../docs/evaluation/similarity-independence-v1.md) and [data dictionary](../docs/release/similarity-independence-v1.md) preserve parameters, provenance, missingness and software versions.

'''
s = s.replace('## Data Records\n', methods + '## Data Records\n')
s = s.replace('| `manuscript/scientific-review-v1.tsv`', '| `data/processed/similarity-independence-v1/` | Representation, pair, dependence and exposure tables; manifest with parameters, environment and input/output hashes |\n| `docs/release/similarity-independence-v1.md` | Similarity table dictionary, eligible denominators, joins and reproduction limits |\n| `manuscript/scientific-review-v1.tsv`')
s = s.replace('under `data/processed/presubmission-release-candidate-v1/`', 'with the similarity companion under `data/processed/presubmission-release-candidate-v3/`')
results = '''### Representation coverage and dependence

Five source-specific product crosswalks support machine-readable connectivity structures: acetylaszonalenin, emericellamide A, griseofulvin, fellutamide B and aspernidine A. Their ten pairwise Tanimoto values range from 0.0323 to 0.1463; none reaches 0.7. The other 425 relationship pairs are unavailable because 25 relationships lack supported structures. This subset cannot establish chemical diversity across all 30 relationships. The genomic analysis represents 79 displayed members of seven source-selected GCFs and ten accepted locus, construct or CDS anchors. Of 10,516 cross-member core pair records, 3,575 have compatible annotated roles and numerical alignments. Incompatible roles remain null, and incomplete or core-only representations cannot establish whole-cluster dissimilarity.

All 91 Trichoderma and 291 black-yeast native joined spectra survived the declared filtering, yielding 4,095 and 42,195 within-pool pairs, respectively. Of these 46,290 comparisons, 93 meet the 0.7/six-peak resemblance rule and 51 meet the 0.9/six-peak rule. The 26,481 cross-pool pairs are excluded because the retained export charges have opposite signs. Seven Trichoderma and 958 black-yeast candidates still lack joined spectra. High cosine does not identify an isomer, adduct or genome-product relationship; acquisition settings and missing spectra limit interpretation.

Eight valactamide relationships share one query and four benzomalvin relationships share another. Three AtFAC9J20 loci share a construct/host context without becoming one pathway. The conservative dependence scenario has five components, only one containing complete evaluated relationships. These scenarios preserve the frozen complete-analysis group and establish no independent holdout or between-group uncertainty estimate. Bounded reference-file checks are recorded separately from weight-specific predictor training membership, which remains unknown. All counts and numerical checks concern retained records; human chemical and biological review remains pending.

'''
s = s.replace('## Usage Notes\n', results + '## Usage Notes\n')
write(owned[0], s)

p = ROOT / owned[1]
s = p.read_text(encoding='utf-8-sig')
s += '''
## Similarity and dependence companion analysis

The frozen [similarity protocol](../protocol/similarity-independence-v1.md) and [result manifest](../data/processed/similarity-independence-v1/manifest.json) define the retained representations, parameters and environment. The [report](../docs/evaluation/similarity-independence-v1.md) and [dictionary](../docs/release/similarity-independence-v1.md) give pair-table joins and missingness rules. This companion changes no admissions, candidate universes, scores or frozen groups: the inventory remains 30 relationships/16 query identities with 11 complete, two partial and 17 missing input states.

Five supported connectivity structures yield ten numerical chemical pairs among 435 possible relationship pairs; 425 remain unavailable. RDKit Morgan fingerprints use radius 2, 2,048 bits, bond types and no chirality. No tautomer canonicalization or charge neutralization is applied. Exact isomeric equality is separate from Tanimoto equality. Source stereochemistry needs reconciliation before chiral sensitivity; independently checked source formulas are unavailable. Unresolved alternatives and proposed structures are not silently assigned exact structures.

The genomic records cover 79 source-displayed GCF members with 1,209 proteins and ten accepted anchors with 43 annotated proteins. Global Biopython alignment uses BLOSUM62, gap opening −10 and extension −0.5 with equal terminal penalties; the first library-optimal path is retained and path ties are counted. Compatible roles yield 3,575 numerical comparisons in 10,516 cross-member core pair records. Identity divides identical nongap residues by paired nongap residues; coverage divides paired residues by each full sequence length. Screens use identity at least 70% or 90%, each with at least 80% coverage on both sides. Reciprocal-best ties and displayed gene order are retained. Qualifying core matches divided by all annotated proteins give lower-bound content fractions, not whole-cluster similarity. The saved reference-correspondence records retain their original evidence scope and hashes.

Spectral processing retains finite positive peaks at m/z at least 10, removes peaks within ±1 Da of known precursor m/z, and retains peaks at least 1% of the base peak. Intensities are square-root transformed and L2-normalized; matchms CosineHungarian uses 0.02 Da tolerance, mz_power=0 and intensity_power=1 on the transformed intensities. All 382 retained spectra survive processing. The 4,095 Trichoderma and 42,195 black-yeast within-pool pairs total 46,290; 26,481 cross-pool pairs are excluded for opposite native-export charge signs. Cosine at least 0.7 with six matched peaks flags 93 pairs, and the 0.9 sensitivity flags 51. Native scan identity, peak-list equality and shared source-event membership remain separate fields. Source collision-energy values are 20 and 40 respectively, with units unrecorded. Missing instrument metadata remains unknown. Seven Trichoderma and 958 black-yeast candidates still have no saved native joins; no historical Caesar feature-to-native-spectrum join is supplied.

Dependence components are separately versioned scenarios built from the printed edge rules. They do not replace frozen groups or create independent observations. The conservative scenario has five components but just one with complete evaluated relationships, so an independent grouped holdout and between-group uncertainty remain unestablished. Exposure records distinguish retrospective selection, declared reference-file membership and weight-specific training membership. A pinned class table or Rosetta mapping is not a complete training roster, and no Rosetta experiment was run. Spec2Class training membership remains unknown despite retained execution receipts and weight hashes.

Software checks cover all 30 relationship IDs, eligible pair accounting, null-versus-zero handling, exact-duplicate fixtures, independent fingerprint bit arithmetic, saved alignment arithmetic and a cosine fixture of 0.48. Retained host verification checks hashes and output structure; it does not replace human chemical or biological judgment. The v3 package carries the completed outputs and consumed inputs with an input-disposition index. No similarity calculations or retrieval experiments were rerun during manuscript integration; no new download-only replay is claimed.
'''
write(owned[1], s)

p = ROOT / owned[4]
s = p.read_text(encoding='utf-8-sig').replace('Exact predictor training overlap and reference-record overlap are unknown.', 'Weight-specific predictor training overlap remains unknown. The similarity companion records bounded stable-ID membership checks against declared retained reference files; those checks do not establish model-training membership.')
s = s.replace('The table preserves correspondence evidence and known shared groups; it supplies no full chemical-similarity or spectral-redundancy matrix.', 'The task table preserves correspondence evidence and known shared groups. The [similarity companion](similarity-independence-v1.md) adds ten chemical pairs from five supported structures, 3,575 compatible core-protein comparisons and 46,290 within-pool spectral comparisons. Twenty-five relationships lack supported structures, and missing spectra or incompatible comparisons remain unavailable. These bounded matrices do not establish chemical diversity for the full inventory or an independent holdout.')
write(owned[4], s)
p = ROOT / owned[5]
s = p.read_text(encoding='utf-8-sig').replace('version 1 with delivery correction', 'version 1 with similarity delivery update')
s = s.replace('The current private container is `fungallink-presubmission-release-v2.zip`. It supersedes v1 for source-link delivery only; the frozen v1 container remains retained. Scientific payloads and rendered manuscripts are unchanged.', 'The current private container is `fungallink-presubmission-release-v3.zip`. It adds the completed similarity companion, its inputs and provenance, and revised manuscript/release documentation. Frozen v1 and v2 containers remain retained. Every inherited scientific input, score, evaluation and nested archive remains byte-identical to v2; changed inherited manuscript/documentation paths and new payloads are listed in the v3 build receipt.')
s = s.replace('Verify `fungallink-presubmission-release-v2.zip`', 'Verify `fungallink-presubmission-release-v3.zip`')
s += '\n## Similarity companion in private candidate v3\n\nThe [similarity dictionary](similarity-independence-v1.md) describes the bounded pair tables and their joins. The [input-disposition index](../../data/manifests/similarity-input-disposition-v1.tsv) identifies every manifest-consumed input at its exact outer archive path and hash. The output manifest, stage receipts, source sequence/structure/spectrum records, scripts and recorded environment accompany the outputs. Package checks verify membership and bytes; they do not claim a new scientific rerun, public source retrieval or human biological review. The prior replay evidence applies only to the unchanged inherited numerical payloads.\n'
write(owned[5], s)

p = ROOT / owned[2]
with p.open(encoding='utf-8-sig', newline='') as f:
    reader=csv.DictReader(f, delimiter='\t'); fields=reader.fieldnames; rows=list(reader)
rows.append(dict(zip(fields, ['DD15', 'current_record_supported_with_limits', 'Methods; Data Records; Technical Validation; Supplementary Methods', 'Similarity companion retains five structures/ten chemical pairs, 3,575 compatible core comparisons and 46,290 within-pool spectral pairs; one complete-analysis group and unknown predictor training overlap remain.', '', 'docs/evaluation/similarity-independence-v1.md; data/processed/similarity-independence-v1/manifest.json; protocol/similarity-independence-v1.md; planning/similarity-independence-work-2026-10-11/host-verification.json', 'Representation-limited companion analysis; no score reruns', '2026-10-11', 'Twenty-five relationships lack supported structures; no independent holdout or human chemical/biological validation.'])))
with p.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
p=ROOT/owned[3];obj=json.loads(p.read_text(encoding='utf-8-sig'))
obj['similarity_companion']={'claim_id':'DD15','report':'../docs/evaluation/similarity-independence-v1.md','manifest':'../data/processed/similarity-independence-v1/manifest.json','structures':5,'chemical_pairs':10,'unavailable_chemical_relationship_pairs':425,'compatible_genomic_pairs':3575,'within_pool_spectral_pairs':46290,'complete_analysis_groups':1,'holdout_established':False,'predictor_training_overlap':'unknown','scientific_reruns_during_integration':False}
write(owned[3],json.dumps(obj,indent=2)+'\n')
write('planning/similarity-manuscript-integration-2026-10-11/authoring-receipt.json',json.dumps({'status':'authored','requested_route':'gpt-6-astra/medium','actual_serving_receipt':'unavailable','owned_sources':owned,'behavior_change':False,'tests_added':False,'verification_strategy':'Frozen-byte comparison, manuscript text coverage, rendered-page review and new ZIP hash verification; no scientific rerun.'},indent=2)+'\n')
print('Integrated',len(owned),'sources')
