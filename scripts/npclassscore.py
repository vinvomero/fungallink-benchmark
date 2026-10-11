"""Independent, named-ontology NPClassScore counting kernel (stdlib only)."""

import csv
from dataclasses import dataclass
import hashlib
import io
from pathlib import Path

GENOMIC_LEVELS = ('mibig_classes', 'as_classes')
CHEMICAL_LEVELS = ('cf_kingdom', 'cf_superclass', 'cf_class', 'cf_subclass',
                   'cf_direct_parent', 'npc_class', 'npc_superclass',
                   'npc_pathway', 'npc_isglycoside')
TABLE_GENOMIC_LEVELS = ('mibig_classes', 'class:subclass', 'as_classes')
HEADERS = ('compound_name', 'class:subclass', 'as_classes', 'smiles', 'inchi_key') + CHEMICAL_LEVELS


@dataclass
class ClassTable:
    """Public data container; callers must treat its contents as read-only."""

    metadata: dict
    counts: dict


def _terms(cell, separator):
    if not cell:
        return []
    terms = cell.split(separator)
    if any(not term or term != term.strip() for term in terms):
        raise ValueError('empty or untrimmed class term')
    return terms


def _genomic(row):
    annotated = _terms(row['class:subclass'], ',')
    if any(term.count(':') != 1 or not term.partition(':')[0] for term in annotated):
        raise ValueError('class:subclass must contain class:subclass entries')
    classes = [term.partition(':')[0] for term in annotated]
    hybrid = lambda term: any(token in term.lower() for token in ('nrp', 'pks', 'polyketide'))
    if sum(hybrid(term) for term in classes) >= 2:
        classes = ['PKS-NRP_Hybrids'] + [term for term in classes if not hybrid(term)]
    return {'mibig_classes': ['Other' if term == 'Alkaloid' else term for term in classes],
            'class:subclass': [term for term in annotated if term.partition(':')[2]],
            'as_classes': _terms(row['as_classes'], ',')}


def load_class_table(path):
    """Read the pinned-format TSV; see docs/evaluation/npclassscore-kernel.md."""
    raw = Path(path).read_bytes()
    try:
        rows = csv.reader(io.StringIO(raw.decode('utf-8')), delimiter='\t', quoting=csv.QUOTE_NONE)
        headers = next(rows)
    except (UnicodeError, StopIteration) as exc:
        raise ValueError('table must be nonempty UTF-8 TSV') from exc
    if len(headers) != len(HEADERS) or set(headers) != set(HEADERS):
        raise ValueError('table header must contain each required column exactly once')
    counts = {g: {s: {} for s in CHEMICAL_LEVELS} for g in TABLE_GENOMIC_LEVELS}
    vocab = {level: set() for level in TABLE_GENOMIC_LEVELS + CHEMICAL_LEVELS}
    identifiers = set()
    for line, cells in enumerate(rows, start=2):
        if len(cells) != len(headers):
            raise ValueError(f'row {line}: wrong number of columns')
        row = dict(zip(headers, cells))
        identifier = row['compound_name']
        if not identifier or identifier != identifier.strip() or identifier in identifiers:
            raise ValueError(f'row {line}: empty, untrimmed, or duplicate compound identifier')
        identifiers.add(identifier)
        genomic = _genomic(row)
        chemical = {s: _terms(row[s], '; ') for s in CHEMICAL_LEVELS}
        for level, terms in (genomic | chemical).items():
            vocab[level].update(terms)
        for g, genomic_terms in genomic.items():
            for s, chemical_terms in chemical.items():
                for genomic_term in genomic_terms:
                    for chemical_term in chemical_terms:
                        bucket = counts[g][s].setdefault(genomic_term, {})
                        bucket[chemical_term] = bucket.get(chemical_term, 0) + 1
    if not identifiers:
        raise ValueError('table has no compound rows')
    metadata = {
        'source_sha256': hashlib.sha256(raw).hexdigest(),
        'source_size_bytes': len(raw), 'compound_rows': len(identifiers),
        'genomic_levels': list(GENOMIC_LEVELS),
        'table_genomic_levels': list(TABLE_GENOMIC_LEVELS),
        'chemical_levels': list(CHEMICAL_LEVELS),
        'vocabulary': {level: sorted(terms) for level, terms in vocab.items()},
        'vocabulary_sizes': {level: len(terms) for level, terms in vocab.items()},
        'pair_totals': {g: {s: sum(sum(bucket.values()) for bucket in counts[g][s].values())
                            for s in CHEMICAL_LEVELS} for g in TABLE_GENOMIC_LEVELS},
    }
    return ClassTable(metadata, counts)


def score_classes(table, genomic_classes, spectral_classes):
    """Return maximum forward empirical score, or explicit input unavailability."""
    for annotations, levels in ((genomic_classes, GENOMIC_LEVELS), (spectral_classes, CHEMICAL_LEVELS)):
        if not isinstance(annotations, dict) or any(level not in levels for level in annotations):
            raise ValueError('annotations must be dictionaries with supported level names')
    for terms in genomic_classes.values():
        if not isinstance(terms, list) or any(not isinstance(t, str) or not t or t != t.strip() for t in terms):
            raise ValueError('genomic values must be lists of nonempty normalized strings')
    for term in spectral_classes.values():
        if term is not None and (not isinstance(term, str) or not term or term != term.strip()):
            raise ValueError('spectral values must be nonempty normalized strings or null')
    audit = {'source_sha256': table.metadata['source_sha256'], 'direction': 'genomic_to_spectral',
             'pairs': [], 'skipped_pairs': [], 'unknown_terms': []}
    for side, annotations in (('genomic', genomic_classes), ('spectral', spectral_classes)):
        for level in sorted(annotations):
            terms = annotations[level] if side == 'genomic' else [annotations[level]]
            for term in sorted(set(t for t in terms if t is not None)):
                if term not in table.metadata['vocabulary'][level]:
                    audit['unknown_terms'].append({'side': side, 'level': level, 'term': term})
    if audit['unknown_terms']:
        return dict(audit, status='input_unavailable', reason='unknown_vocabulary')
    if not any(genomic_classes.values()):
        return dict(audit, status='input_unavailable', reason='missing_genomic_classes')
    if not any(term is not None for term in spectral_classes.values()):
        return dict(audit, status='input_unavailable', reason='missing_spectral_classes')
    for g in sorted(genomic_classes):
        for genomic_term in sorted(set(genomic_classes[g])):
            for s in sorted(spectral_classes):
                chemical_term = spectral_classes[s]
                if chemical_term is None:
                    continue
                pair = {'genomic_level': g, 'genomic_term': genomic_term,
                        'spectral_level': s, 'spectral_term': chemical_term}
                bucket = table.counts[g][s].get(genomic_term, {})
                denominator = sum(bucket.values())
                if denominator == 0:
                    audit['skipped_pairs'].append(dict(pair, reason='missing_denominator'))
                    continue
                count = bucket.get(chemical_term, 0)
                audit['pairs'].append(dict(pair, count=count, denominator=denominator, score=count / denominator))
    if not audit['pairs']:
        return dict(audit, status='input_unavailable', reason='no_usable_class_pairs')
    return dict(audit, status='ok', score=max(pair['score'] for pair in audit['pairs']))
