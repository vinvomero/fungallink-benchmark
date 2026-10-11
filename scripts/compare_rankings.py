"""Compare two raw method runs using paired pathway-group differences."""
import argparse
import json
import math
import os
from pathlib import Path
import platform
import random
import tempfile

if __package__:
    from .evaluate_rankings import evaluate, _json_object
else:
    from evaluate_rankings import evaluate, _json_object


BOOTSTRAP_DRAWS = 10000
BOOTSTRAP_SEED = 20260930


def _percentile(ordered, probability):
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def _contrast(a, b):
    by_id = {group["group_id"]: group for group in b["groups"]}
    groups = []
    for group_a in a["groups"]:
        group_b = by_id[group_a["group_id"]]
        metrics_a = group_a["end_to_end"]["metrics"]
        metrics_b = group_b["end_to_end"]["metrics"]
        groups.append({"group_id": group_a["group_id"], "query_ids": group_a["query_ids"],
                       "query_count": group_a["query_count"], "cohort_count": group_a["cohort_count"],
                       "cohort_ids": group_a["cohort_ids"], "a": metrics_a, "b": metrics_b,
                       "differences": {key: value - metrics_b[key] for key, value in metrics_a.items()}})
    count = len(groups)
    names = list(groups[0]["differences"])
    samples = {key: [] for key in names}
    if count > 1:
        generator = random.Random(BOOTSTRAP_SEED)
        for _ in range(BOOTSTRAP_DRAWS):
            # The same groups are drawn for both methods and every metric.
            selected = [groups[generator.randrange(count)]["differences"] for _ in range(count)]
            for key in names:
                samples[key].append(math.fsum(row[key] for row in selected) / count)
    metrics = {}
    for key in names:
        ordered = sorted(samples[key])
        interval = {"lower": _percentile(ordered, .025) if ordered else None,
                    "upper": _percentile(ordered, .975) if ordered else None,
                    "estimability": "estimable" if ordered else "not_estimable"}
        metrics[key] = {"a": a["summary"]["end_to_end"]["metrics"][key],
                        "b": b["summary"]["end_to_end"]["metrics"][key],
                        "difference": math.fsum(g["differences"][key] for g in groups) / count,
                        "interval": interval,
                        "interval_width": interval["upper"] - interval["lower"] if ordered else None,
                        "tied_group_count": sum(g["differences"][key] == 0 for g in groups)}
        halves = [sorted(samples[key][:BOOTSTRAP_DRAWS // 2]), sorted(samples[key][BOOTSTRAP_DRAWS // 2:])]
        endpoints = [{"lower": _percentile(half, .025), "upper": _percentile(half, .975)}
                     for half in halves] if ordered else []
        metrics[key]["monte_carlo_stability"] = {
            "first_half_interval": endpoints[0] if endpoints else None,
            "second_half_interval": endpoints[1] if endpoints else None,
            "max_endpoint_difference": max(abs(endpoints[0][edge] - endpoints[1][edge])
                                           for edge in ("lower", "upper")) if endpoints else None,
            "interpretation": "split-draw diagnostic; no pass threshold" if endpoints else "not_estimable"}
    leave_one_out = []
    for omitted in groups:
        retained = [g for g in groups if g["group_id"] != omitted["group_id"]]
        leave_one_out.append({"omitted_group_id": omitted["group_id"], "group_count": len(retained),
                              "differences": {key: math.fsum(g["differences"][key] for g in retained) / len(retained)
                                              for key in names} if retained else None,
                              "estimability": "estimable" if retained else "not_estimable"})
    return {"population": {key: a["summary"][key] for key in ("query_count", "group_count", "group_cohort_count")},
            "groups": groups, "metrics": metrics, "leave_one_group_out": leave_one_out,
            "bootstrap": {"draws": BOOTSTRAP_DRAWS, "completed_draws": BOOTSTRAP_DRAWS if count > 1 else 0,
                          "seed": BOOTSTRAP_SEED, "confidence_level": .95,
                          "method": "paired pathway-group percentile",
                          "percentile_rule": "linear interpolation at (draws - 1) * probability",
                          "generator": "random.Random (Mersenne Twister)",
                          "python_version": platform.python_version(),
                          "settings_status": "software defaults; scientific freeze requires a dated declaration",
                          "interpretation": "descriptive; conditional on observed cohorts, candidate pools and curated labels",
                          "limitation": "Few groups give discrete, potentially unstable intervals; a nominal interval does not establish superiority.",
                          "monte_carlo_stability": "first-half versus second-half percentile endpoints per metric"},
            "evaluations": {"a": a, "b": b}}


def _matched_evaluations(benchmark, runs, selected, cutoffs):
    subset_benchmark = {**benchmark, "queries": [q for q in benchmark["queries"] if q["query_id"] in selected]}
    return [evaluate(subset_benchmark,
                     {**run, "outputs": [o for o in run["outputs"] if o["query_id"] in selected]}, cutoffs=cutoffs)
            for run in runs]


def _membership(benchmark, selected):
    known = {q["query_id"] for q in benchmark["queries"]}
    retained = [q for q in benchmark["queries"] if q["query_id"] in selected]
    groups = {q["group_id"] for q in retained}
    return {"query_ids": sorted(selected), "omitted_query_ids": sorted(known - selected),
            "omitted_group_ids": sorted({q["group_id"] for q in benchmark["queries"]} - groups),
            "population": {"query_count": len(retained), "group_count": len(groups),
                           "group_cohort_count": len({(q["group_id"], q["cohort_id"]) for q in retained})}}


def compare(benchmark, run_a, run_b, cutoffs=(1, 10, 100), predeclared_subset=None):
    """Evaluate raw runs on one benchmark, then compare end-to-end group means.

    An optional subset has name, provenance and query_ids, declared from input
    manifests before inspecting outputs. The caller supplies that provenance;
    this function cannot verify when the declaration was made.
    """
    cutoffs = tuple(cutoffs)
    a = evaluate(benchmark, run_a, cutoffs=cutoffs)
    b = evaluate(benchmark, run_b, cutoffs=cutoffs)
    result = {"schema_version": "1", "direction": "a_minus_b", "estimand": "end_to_end",
              "population_role": "full_track_primary", **_contrast(a, b)}
    valid_ids = [{q["query_id"] for q in evaluation["queries"] if q["status"] == "valid_output"}
                 for evaluation in (a, b)]
    selected_valid = valid_ids[0] & valid_ids[1]
    diagnostic = {"population_role": "outcome_dependent_diagnostic_only",
                  "estimand": "paired_valid_output", **_membership(benchmark, selected_valid),
                  "estimability": "estimable" if selected_valid else "not_estimable",
                  "metrics": None, "groups": [], "evaluations": None}
    if selected_valid:
        da, db = _matched_evaluations(benchmark, (run_a, run_b), selected_valid, cutoffs)
        diagnostic["evaluations"] = {"a": da, "b": db}
        diagnostic["metrics"] = {key: {"a": value, "b": db["summary"]["end_to_end"]["metrics"][key],
                                         "difference": value - db["summary"]["end_to_end"]["metrics"][key]}
                                 for key, value in da["summary"]["end_to_end"]["metrics"].items()}
        for ga, gb in zip(da["groups"], db["groups"]):
            diagnostic["groups"].append({"group_id": ga["group_id"], "query_count": ga["query_count"],
                                         "cohort_count": ga["cohort_count"], "query_ids": ga["query_ids"],
                                         "a": ga["end_to_end"]["metrics"], "b": gb["end_to_end"]["metrics"],
                                         "differences": {key: value - gb["end_to_end"]["metrics"][key]
                                                         for key, value in ga["end_to_end"]["metrics"].items()}})
    result["paired_valid_diagnostic"] = diagnostic
    if predeclared_subset is not None:
        if not isinstance(predeclared_subset, dict):
            raise ValueError("predeclared_subset must be an object")
        for field in ("name", "provenance"):
            value = predeclared_subset.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"predeclared_subset {field} must be a nonempty string")
        ids = predeclared_subset.get("query_ids")
        if not isinstance(ids, list) or any(not isinstance(qid, str) for qid in ids):
            raise ValueError("predeclared_subset query_ids must be a list of query IDs")
        selected = set(ids)
        known = {q["query_id"] for q in benchmark["queries"]}
        if len(selected) != len(ids) or not selected <= known:
            raise ValueError("predeclared_subset query_ids must be unique known query IDs")
        subset = (_contrast(*_matched_evaluations(benchmark, (run_a, run_b), selected, cutoffs))
                  if selected else {"metrics": None, "groups": [], "leave_one_group_out": [],
                                    "bootstrap": None, "evaluations": None})
        result["common_input_subset"] = {
            "name": predeclared_subset["name"], "provenance": predeclared_subset["provenance"],
            "population_role": "predeclared_common_input", "estimand": "end_to_end",
            "estimability": "estimable" if selected else "not_estimable", **_membership(benchmark, selected),
            **subset}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark", required=True, type=Path)
    parser.add_argument("--run-a", required=True, type=Path)
    parser.add_argument("--run-b", required=True, type=Path)
    parser.add_argument("--predeclared-subset", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        inputs = [json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_json_object)
                  for path in (args.benchmark, args.run_a, args.run_b)]
        subset = (json.loads(args.predeclared_subset.read_text(encoding="utf-8"), object_pairs_hook=_json_object)
                  if args.predeclared_subset else None)
        result = compare(*inputs, predeclared_subset=subset)
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
        parser.exit(2, f"comparison error: {exc}\n")


if __name__ == "__main__":
    main()
