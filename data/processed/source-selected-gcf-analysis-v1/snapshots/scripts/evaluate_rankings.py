"""Evaluate complete candidate scores against separate, canonical-ID gold data."""
import argparse
from collections import Counter, defaultdict
import json
import math
import os
from pathlib import Path
import tempfile


STATUSES = ("valid_output", "abstention", "input_unavailable", "execution_failure", "invalid_output")
IDENTITIES = ("track_id", "query_type", "candidate_universe_id")


def _identifier(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a nonempty string")
    return value


def _object(value, field):
    if not isinstance(value, dict):
        raise ValueError(f"{field} must be an object")
    return value


def _list(value, field):
    if not isinstance(value, list):
        raise ValueError(f"{field} must be a list")
    return value


def _unique_ids(value, field):
    values = _list(value, field)
    for item in values:
        _identifier(item, field)
    if not values or len(set(values)) != len(values):
        raise ValueError(f"{field} must be nonempty with no duplicate canonical IDs")
    return set(values)


def _gold(benchmark):
    _object(benchmark, "benchmark")
    for key in IDENTITIES:
        _identifier(benchmark.get(key), key)
    queries = {}
    for query in _list(benchmark.get("queries"), "queries"):
        _object(query, "query")
        qid = _identifier(query.get("query_id"), "query_id")
        if qid in queries:
            raise ValueError(f"duplicate gold query: {qid}")
        for key in ("group_id", "cohort_id"):
            _identifier(query.get(key), key)
        candidates = _unique_ids(query.get("candidate_ids"), "candidate_ids")
        products = _object(query.get("products"), "products")
        if not products:
            raise ValueError(f"query {qid} has no product targets")
        seen = set()
        for product, members in products.items():
            _identifier(product, "product_id")
            targets = _unique_ids(members, "product target IDs")
            if not targets <= candidates:
                raise ValueError(f"query {qid}: product targets outside candidate set")
            if seen & targets:
                raise ValueError(f"query {qid}: overlapping products require adjudication")
            seen.update(targets)
        queries[qid] = query
    if not queries:
        raise ValueError("benchmark needs at least one query")
    return queries


def _submission(run, benchmark, queries):
    _object(run, "run")
    for key in ("method_id", "method_version", "run_id") + IDENTITIES:
        _identifier(run.get(key), key)
    for key in IDENTITIES:
        if run[key] != benchmark[key]:
            raise ValueError(f"run {key} does not match benchmark")
    if run.get("score_direction") not in ("higher", "lower"):
        raise ValueError("score_direction must be higher or lower")
    outputs = {}
    for output in _list(run.get("outputs"), "outputs"):
        _object(output, "query output")
        qid = _identifier(output.get("query_id"), "output query_id")
        if qid not in queries:
            raise ValueError(f"unknown output query: {qid}")
        if qid in outputs:
            raise ValueError(f"duplicate output query: {qid}")
        outputs[qid] = output
    return outputs


def _scores(output, candidates):
    scores = {}
    for row in _list(output.get("scores"), "scores"):
        _object(row, "score row")
        candidate = _identifier(row.get("candidate_id"), "candidate_id")
        if candidate not in candidates:
            raise ValueError(f"unknown canonical candidate ID: {candidate}")
        if candidate in scores:
            raise ValueError(f"duplicate canonical candidate ID: {candidate}")
        score = row.get("score")
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise ValueError(f"score for {candidate} must be a finite number")
        if isinstance(score, float) and not math.isfinite(score):
            raise ValueError(f"score for {candidate} must be finite")
        scores[candidate] = score
    missing = candidates - scores.keys()
    if missing:
        raise ValueError("partial ranking; missing candidates: " + ", ".join(sorted(missing)))
    return scores


def _choose(n, r):
    return math.comb(n, r) if 0 <= r <= n else 0


def _hit(t, p, r):
    denominator = _choose(t, r)
    return (denominator - _choose(t - p, r)) / denominator


def _first_target(blocks, targets, cutoffs):
    above = 0
    for block in blocks:
        p = len(block & targets)
        if p:
            t = len(block)
            # Probability that the first positive is at position u, updated
            # from its hypergeometric mass rather than substituting mean rank.
            probability = p / t
            terms = []
            for u in range(1, t - p + 2):
                terms.append(probability / (above + u))
                if u < t - p + 1:
                    probability *= (t - u - p + 1) / (t - u)
            return {
                "rank": {"best": above + 1, "worst": above + t - p + 1},
                "rr": math.fsum(terms),
                "hits": {k: _hit(t, p, min(t, max(0, k - above))) for k in cutoffs},
            }
        above += len(block)
    raise ValueError("target missing from ranking")


def _all_products(blocks, products, cutoff):
    recovered = set()
    above = 0
    for block in blocks:
        t = len(block)
        if above + t < cutoff:
            recovered.update(j for j, targets in products.items() if targets & block)
            above += t
            continue
        r = cutoff - above
        counts = [len(targets & block) for j, targets in products.items() if j not in recovered]
        if not counts:
            return 1.0, {"best": 1.0, "worst": 1.0}
        if 0 in counts or r < len(counts):
            return 0.0, {"best": 0.0, "worst": 0.0}
        if r == t:
            return 1.0, {"best": 1.0, "worst": 1.0}
        # Count size-r subsets hitting every remaining disjoint product.
        # Coefficient of x**r in (1+x)**other * product((1+x)**p - 1).
        other = t - sum(counts)
        dp = [_choose(other, i) for i in range(r + 1)]
        for p in counts:
            coefficients = [_choose(p, i) for i in range(min(p, r) + 1)]
            dp = [sum(dp[n - i] * coefficients[i] for i in range(1, min(p, n) + 1))
                  for n in range(r + 1)]
        return dp[r] / _choose(t, r), {"best": 1.0, "worst": float(all(r > t - p for p in counts))}
    raise ValueError("cutoff outside candidate set")


def _rank_metrics(scores, product_lists, direction, cutoffs):
    by_score = defaultdict(set)
    for candidate, score in scores.items():
        by_score[score].add(candidate)
    blocks = [by_score[s] for s in sorted(by_score, reverse=direction == "higher")]
    products = {j: set(targets) for j, targets in product_lists.items()}
    effective = {k: min(k, len(scores)) for k in cutoffs}
    first = _first_target(blocks, set().union(*products.values()), effective.values())
    per_product = {j: _first_target(blocks, targets, effective.values()) for j, targets in sorted(products.items())}
    metrics = {"rr": first["rr"]}
    bounds = {"rr": {"best": 1 / first["rank"]["best"], "worst": 1 / first["rank"]["worst"]}}
    for k, cap in effective.items():
        metrics[f"hit@{k}"] = first["hits"][cap]
        metrics[f"product_recovery@{k}"] = math.fsum(p["hits"][cap] for p in per_product.values()) / len(products)
        metrics[f"all_products@{k}"], bounds[f"all_products@{k}"] = _all_products(blocks, products, cap)
        bounds[f"hit@{k}"] = {"best": float(first["rank"]["best"] <= cap),
                                "worst": float(first["rank"]["worst"] <= cap)}
    return {"metrics": metrics, "metric_bounds": bounds, "first_positive_rank": first["rank"],
            "products": {j: {"first_target_rank": p["rank"], "expected_rr": p["rr"],
                              "hit": {str(k): p["hits"][cap] for k, cap in effective.items()}}
                         for j, p in per_product.items()}}


def _query_result(query, output, direction, cutoffs):
    result = {key: query[key] for key in ("query_id", "group_id", "cohort_id")}
    size = len(query["candidate_ids"])
    result.update(pool_size=size, product_count=len(query["products"]),
                  effective_cutoffs={str(k): min(k, size) for k in cutoffs},
                  metrics=None, metric_bounds=None, first_positive_rank=None, products=None)
    try:
        if output is None:
            raise ValueError("missing query output")
        status = output.get("status")
        if status in STATUSES[1:4]:
            reason = _identifier(output.get("reason"), "non-output reason")
            if "scores" in output:
                raise ValueError("non-output status must not contain scores")
            result.update(status=status, reason=reason)
        elif status == "ok":
            scores = _scores(output, set(query["candidate_ids"]))
            result.update(_rank_metrics(scores, query["products"], direction, cutoffs))
            result.update(status="valid_output", reason=None)
        else:
            raise ValueError("status must be ok, abstention, input_unavailable or execution_failure")
    except ValueError as exc:
        result.update(status="invalid_output", reason=str(exc))
    return result


def _mean_metrics(items):
    if not items:
        return None
    return {key: math.fsum(row[key] for row in items) / len(items) for key in items[0]}


def _aggregate(rows, metric_names, children=None):
    valid = [r for r in rows if r["status"] == "valid_output"]
    counts = Counter(r["status"] for r in rows)
    zero = dict.fromkeys(metric_names, 0.0)
    if children is None:
        conditional = _mean_metrics([r["metrics"] for r in valid])
        end_to_end = _mean_metrics([r["metrics"] if r["metrics"] is not None else zero for r in rows])
        status_rates = {s: counts[s] / len(rows) for s in STATUSES}
    else:
        conditional = _mean_metrics([c["conditional"]["metrics"] for c in children if c["conditional"]["metrics"] is not None])
        end_to_end = _mean_metrics([c["end_to_end"]["metrics"] for c in children])
        status_rates = _mean_metrics([c["hierarchical_status_rates"] for c in children])
    return {
        "query_count": len(rows), "valid_query_count": len(valid),
        "status_counts": {s: counts[s] for s in STATUSES},
        "status_rates": {s: counts[s] / len(rows) for s in STATUSES},
        "coverage": len(valid) / len(rows), "hierarchical_coverage": status_rates["valid_output"],
        "hierarchical_status_rates": status_rates,
        "conditional": {"query_count": len(valid), "metrics": conditional,
                        "estimability": "estimable" if conditional is not None else "not_estimable"},
        "end_to_end": {"query_count": len(rows), "metrics": end_to_end},
    }


def evaluate(benchmark, run, cutoffs=(1, 10, 100)):
    """Return per-query and hierarchical metrics; reject invalid gold/envelopes.

    Malformed attributable query outputs become invalid_output with a reason.
    Gold and method scores are separate objects; neither input is mutated.
    """
    cutoffs = tuple(cutoffs)
    if not cutoffs or any(type(k) is not int or k < 1 for k in cutoffs) or len(set(cutoffs)) != len(cutoffs):
        raise ValueError("cutoffs must be distinct positive integers")
    cutoffs = tuple(sorted(cutoffs))
    queries = _gold(benchmark)
    outputs = _submission(run, benchmark, queries)
    rows = [_query_result(q, outputs.get(qid), run["score_direction"], cutoffs) for qid, q in sorted(queries.items())]
    metric_names = ["rr"] + [f"{metric}@{k}" for k in cutoffs for metric in ("hit", "product_recovery", "all_products")]
    cohort_rows = defaultdict(list)
    group_rows = defaultdict(list)
    for row in rows:
        cohort_rows[(row["group_id"], row["cohort_id"])].append(row)
        group_rows[row["group_id"]].append(row)
    cohorts = [dict(_aggregate(members, metric_names), group_id=g, cohort_id=c,
                    query_ids=[r["query_id"] for r in members]) for (g, c), members in sorted(cohort_rows.items())]
    groups = []
    for group, members in sorted(group_rows.items()):
        children = [c for c in cohorts if c["group_id"] == group]
        groups.append(dict(_aggregate(members, metric_names, children), group_id=group,
                           cohort_count=len(children), covered_cohort_count=sum(c["valid_query_count"] > 0 for c in children),
                           cohort_ids=[c["cohort_id"] for c in children], query_ids=[r["query_id"] for r in members]))
    summary = _aggregate(rows, metric_names, groups)
    summary.update(group_count=len(groups), covered_group_count=sum(g["valid_query_count"] > 0 for g in groups),
                   group_cohort_count=len(cohorts), covered_group_cohort_count=sum(c["valid_query_count"] > 0 for c in cohorts),
                   group_coverage=sum(g["valid_query_count"] > 0 for g in groups) / len(groups),
                   pool_sizes={r["query_id"]: r["pool_size"] for r in rows},
                   capped_query_counts={str(k): sum(r["pool_size"] < k for r in rows) for k in cutoffs})
    return {"schema_version": "1", **{key: run[key] for key in IDENTITIES + ("method_id", "method_version", "run_id", "score_direction")},
            "cutoffs": list(cutoffs), "queries": rows, "cohorts": cohorts, "groups": groups, "summary": summary}


def _json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark", required=True, type=Path)
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        benchmark = json.loads(args.benchmark.read_text(encoding="utf-8"), object_pairs_hook=_json_object)
        run = json.loads(args.run.read_text(encoding="utf-8"), object_pairs_hook=_json_object)
        result = evaluate(benchmark, run)
        serialized = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=args.output.parent,
                                             prefix=f".{args.output.name}.", suffix=".tmp", delete=False) as report:
                temporary = Path(report.name)
                report.write(serialized)
            os.replace(temporary, args.output)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    except (ValueError, OSError) as exc:
        parser.exit(2, f"evaluation error: {exc}\n")


if __name__ == "__main__":
    main()
