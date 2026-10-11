"""Synthetic ranking tests, including an independent permutation oracle."""
import copy
import itertools
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts.evaluate_rankings import evaluate, main


def example(scores=(0, 0, 0, 0), products=None):
    ids = ["a", "b", "c", "d"]
    benchmark = {
        "track_id": "feature", "query_type": "GCF", "candidate_universe_id": "synthetic-v1",
        "queries": [{"query_id": "q", "group_id": "g", "cohort_id": "c",
                     "candidate_ids": ids, "products": products or {"p1": ["a"], "p2": ["b"]}}],
    }
    run = {"method_id": "synthetic", "method_version": "1", "run_id": "run-1",
           "track_id": "feature", "query_type": "GCF", "candidate_universe_id": "synthetic-v1",
           "score_direction": "higher", "outputs": [{"query_id": "q", "status": "ok",
           "scores": [{"candidate_id": c, "score": s} for c, s in zip(ids, scores)]}]}
    return benchmark, run


def oracle(scores, products, cutoff):
    blocks = [[c for c in scores if scores[c] == s] for s in sorted(set(scores.values()), reverse=True)]
    observations = []
    for choices in itertools.product(*(list(itertools.permutations(b)) for b in blocks)):
        ordering = sum((list(b) for b in choices), [])
        ranks = [min(ordering.index(c) + 1 for c in members) for members in products.values()]
        observations.append({"hit": float(min(ranks) <= cutoff), "rr": 1 / min(ranks),
                             "recovery": sum(r <= cutoff for r in ranks) / len(ranks),
                             "all": float(max(ranks) <= cutoff)})
    return {key: (sum(o[key] for o in observations) / len(observations),
                  min(o[key] for o in observations), max(o[key] for o in observations))
            for key in observations[0]}


class RankingTests(unittest.TestCase):
    def test_hand_calculated_all_tied(self):
        result = evaluate(*example(), cutoffs=(1, 2, 10, 100))
        q = result["queries"][0]
        self.assertAlmostEqual(q["metrics"]["hit@1"], .5)
        self.assertAlmostEqual(q["metrics"]["hit@2"], 5 / 6)
        self.assertAlmostEqual(q["metrics"]["rr"], 13 / 18)
        self.assertAlmostEqual(q["metrics"]["product_recovery@2"], .5)
        self.assertAlmostEqual(q["metrics"]["all_products@2"], 1 / 6)
        self.assertEqual(q["first_positive_rank"], {"best": 1, "worst": 3})
        self.assertEqual(q["effective_cutoffs"]["100"], 4)
        self.assertEqual(result["summary"]["capped_query_counts"]["100"], 1)

    def test_exhaustive_tie_permutations(self):
        for scores in itertools.product((0, 1), repeat=4):
            for products in ({"one": ["a", "b"]}, {"one": ["a", "c"], "two": ["b"]},
                             {"one": ["a"], "two": ["b"], "three": ["d"]}):
                benchmark, run = example(scores, products)
                q = evaluate(benchmark, run, cutoffs=(1, 2, 3, 4))["queries"][0]
                for k in range(1, 5):
                    expected = oracle(dict(zip("abcd", scores)), products, k)
                    for name, oracle_name in ((f"hit@{k}", "hit"), ("rr", "rr"),
                                              (f"product_recovery@{k}", "recovery"),
                                              (f"all_products@{k}", "all")):
                        self.assertAlmostEqual(q["metrics"][name], expected[oracle_name][0])
                        if name in q["metric_bounds"]:
                            self.assertAlmostEqual(q["metric_bounds"][name]["worst"], expected[oracle_name][1])
                            self.assertAlmostEqual(q["metric_bounds"][name]["best"], expected[oracle_name][2])

    def test_id_join_direction_and_ion_grouping(self):
        benchmark, run = example((1, 2, 3, 4), {"one_product": ["a", "b"]})
        run["score_direction"] = "lower"
        original = evaluate(benchmark, run)
        run["outputs"][0]["scores"].reverse()
        benchmark["queries"][0]["candidate_ids"].reverse()
        self.assertEqual(original, evaluate(benchmark, run))
        self.assertEqual(original["queries"][0]["metrics"]["product_recovery@1"], 1)
        self.assertEqual(len(original["queries"][0]["products"]), 1)

    def test_nonoutput_and_empty_conditional(self):
        for status in ("abstention", "input_unavailable", "execution_failure"):
            benchmark, run = example()
            run["outputs"] = [{"query_id": "q", "status": status, "reason": "synthetic reason"}]
            result = evaluate(benchmark, run)
            self.assertEqual(result["queries"][0]["status"], status)
            self.assertIsNone(result["queries"][0]["metrics"])
            self.assertIsNone(result["summary"]["conditional"]["metrics"])
            self.assertEqual(result["summary"]["conditional"]["estimability"], "not_estimable")
            self.assertEqual(result["summary"]["end_to_end"]["metrics"]["rr"], 0)
            self.assertEqual(result["summary"]["status_counts"][status], 1)

    def test_invalid_outputs(self):
        mutations = [
            lambda r: r["outputs"][0]["scores"].pop(),
            lambda r: r["outputs"][0]["scores"].append({"candidate_id": "a", "score": 2}),
            lambda r: r["outputs"][0]["scores"][0].update(candidate_id="alias-a"),
            lambda r: r["outputs"][0]["scores"][0].update(score=float("nan")),
            lambda r: r["outputs"][0]["scores"][0].update(score=float("inf")),
            lambda r: r["outputs"][0]["scores"][0].update(score=True),
            lambda r: r["outputs"][0]["scores"][0].update(score="1"),
            lambda r: r["outputs"].clear(),
            lambda r: r["outputs"][0].update(status="mystery"),
            lambda r: r["outputs"][0].update(scores=None),
        ]
        for mutate in mutations:
            benchmark, run = example()
            mutate(run)
            result = evaluate(benchmark, run)
            self.assertEqual(result["queries"][0]["status"], "invalid_output")
            self.assertTrue(result["queries"][0]["reason"])
            self.assertEqual(result["summary"]["coverage"], 0)

    def test_nonoutput_rejects_scores(self):
        for status in ("abstention", "input_unavailable", "execution_failure"):
            benchmark, run = example()
            run["outputs"][0].update(status=status, scores=[], reason="synthetic reason")
            query = evaluate(benchmark, run)["queries"][0]
            self.assertEqual(query["status"], "invalid_output")
            self.assertEqual(query["reason"], "non-output status must not contain scores")

    def test_nonoutput_rejects_empty_reason(self):
        benchmark, run = example()
        run["outputs"] = [{"query_id": "q", "status": "abstention", "reason": ""}]
        query = evaluate(benchmark, run)["queries"][0]
        self.assertEqual(query["status"], "invalid_output")
        self.assertEqual(query["reason"], "non-output reason must be a nonempty string")

    def test_full_boundary_all_products(self):
        # At cutoff 2 the top tie block is fully selected. A product below it
        # still prevents all-products recovery.
        for products, expected in (({"one": ["a"], "two": ["b"]}, 1.0),
                                   ({"one": ["a"], "two": ["c"]}, 0.0)):
            query = evaluate(*example((1, 1, 0, 0), products), cutoffs=(2,))["queries"][0]
            self.assertEqual(query["metrics"]["all_products@2"], expected)
            self.assertEqual(query["metric_bounds"]["all_products@2"], {"best": expected, "worst": expected})

    def test_full_pool_9339_api(self):
        benchmark, run = example()
        ids = [f"candidate-{i}" for i in range(9339)]
        benchmark["queries"][0].update(candidate_ids=ids, products={f"p{i}": [ids[i]] for i in range(3)})
        run["outputs"][0]["scores"] = [{"candidate_id": candidate, "score": 0} for candidate in reversed(ids)]
        query = evaluate(benchmark, run, cutoffs=(9339,))["queries"][0]
        self.assertEqual(query["status"], "valid_output")
        for metric in ("hit", "product_recovery", "all_products"):
            self.assertEqual(query["metrics"][f"{metric}@9339"], 1.0)
        self.assertEqual(query["metric_bounds"]["all_products@9339"], {"best": 1.0, "worst": 1.0})

    def test_invalid_gold_and_envelopes(self):
        mutations = [
            lambda b, r: b["queries"][0].update(products={}),
            lambda b, r: b["queries"][0].update(products={"p": []}),
            lambda b, r: b["queries"][0].update(products={"p": ["unknown"]}),
            lambda b, r: b["queries"][0].update(products={"p": ["a", "a"]}),
            lambda b, r: b["queries"][0].update(products={"p": ["a"], "q": ["a"]}),
            lambda b, r: b["queries"][0]["candidate_ids"].append("a"),
            lambda b, r: b["queries"].append(copy.deepcopy(b["queries"][0])),
            lambda b, r: r["outputs"].append(copy.deepcopy(r["outputs"][0])),
            lambda b, r: r["outputs"][0].update(query_id="unknown"),
            lambda b, r: r.update(score_direction="undeclared"),
            lambda b, r: r.update(track_id="other"),
            lambda b, r: r.update(candidate_universe_id="other"),
        ]
        for mutate in mutations:
            benchmark, run = example()
            mutate(benchmark, run)
            with self.assertRaises(ValueError):
                evaluate(benchmark, run)

    def test_query_id_join_and_inputs_are_unchanged(self):
        benchmark, run = example((4, 3, 2, 1))
        benchmark["queries"].append(dict(copy.deepcopy(benchmark["queries"][0]), query_id="second"))
        run["outputs"].insert(0, {"query_id": "second", "status": "execution_failure", "reason": "fixture"})
        before = copy.deepcopy((benchmark, run))
        result = evaluate(benchmark, run)
        self.assertEqual((benchmark, run), before)
        self.assertEqual(result["queries"][0]["metrics"]["rr"], 1)
        self.assertEqual(result["queries"][1]["status"], "execution_failure")

    def test_score_equality_does_not_round(self):
        benchmark, run = example((1, 0, 1.000000000001, 0), {"one": ["a"]})
        q = evaluate(benchmark, run)["queries"][0]
        self.assertEqual(q["metrics"]["rr"], .5)
        self.assertEqual(q["first_positive_rank"], {"best": 2, "worst": 2})

    def test_cli_rejects_duplicate_json_keys(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            (path / "gold.json").write_text('{"queries": [], "queries": []}')
            process = subprocess.run([sys.executable, str(root / "scripts/evaluate_rankings.py"),
                                      "--benchmark", str(path / "gold.json"),
                                      "--run", str(root / "tests/fixtures/evaluator/run.json"),
                                      "--output", str(path / "result.json")], capture_output=True, text=True)
            self.assertEqual(process.returncode, 2)
            self.assertIn("duplicate JSON object key", process.stderr)
            self.assertFalse((path / "result.json").exists())

    def test_hierarchy_and_counts(self):
        benchmark, run = example((4, 3, 2, 1))
        template = benchmark["queries"].pop()
        output = run["outputs"].pop()
        # g1: cohort c1 has 3 successes; c2 has 1 failure. g2: 1 failure.
        for i, (g, c, ok) in enumerate([("g1", "c1", True)] * 3 + [("g1", "c2", False), ("g2", "c3", False)]):
            query = dict(copy.deepcopy(template), query_id=str(i), group_id=g, cohort_id=c)
            benchmark["queries"].append(query)
            run["outputs"].append(dict(copy.deepcopy(output), query_id=str(i)) if ok else
                                  {"query_id": str(i), "status": "abstention", "reason": "fixture"})
        result = evaluate(benchmark, run)
        summary = result["summary"]
        self.assertEqual(summary["end_to_end"]["metrics"]["rr"], .25)
        self.assertEqual(summary["conditional"]["metrics"]["rr"], 1)
        self.assertEqual(summary["coverage"], .6)
        self.assertEqual(summary["hierarchical_coverage"], .25)
        self.assertEqual(summary["hierarchical_status_rates"]["abstention"], .75)
        self.assertEqual(summary["group_count"], 2)
        self.assertEqual(summary["covered_group_count"], 1)
        self.assertEqual(len(result["cohorts"]), 3)
        self.assertEqual(result["groups"][0]["conditional"]["query_count"], 3)

    def test_file_cli(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "result.json"
            destination.write_bytes(b"previous report")
            process = subprocess.run([sys.executable, str(root / "scripts/evaluate_rankings.py"),
                                      "--benchmark", str(root / "tests/fixtures/evaluator/benchmark.json"),
                                      "--run", str(root / "tests/fixtures/evaluator/run.json"),
                                      "--output", str(destination)], capture_output=True, text=True)
            self.assertEqual(process.returncode, 0, process.stderr)
            result = json.loads(destination.read_text())
            self.assertAlmostEqual(result["queries"][0]["metrics"]["rr"], 13 / 18)
            self.assertEqual(list(Path(temp).iterdir()), [destination])

    def test_conditional_hierarchy_unequal_covered_children(self):
        benchmark, run = example(products={"one": ["a"]})
        template = benchmark["queries"].pop()
        run["outputs"].clear()
        # g1/c1: (1 + 1/2 + 1/2)/3 = 2/3; g1/c2: 1/4.
        # g2/c3: (1/3 + 1/3)/2 = 1/3. Empty children are excluded.
        rows = [("g1", "c1", 1), ("g1", "c1", 2), ("g1", "c1", 2),
                ("g1", "c2", 4), ("g1", "empty", None),
                ("g2", "c3", 3), ("g2", "c3", 3), ("empty", "empty", None)]
        for i, (group, cohort, rank) in enumerate(rows):
            benchmark["queries"].append(dict(copy.deepcopy(template), query_id=str(i), group_id=group, cohort_id=cohort))
            output = {"query_id": str(i), "status": "abstention", "reason": "fixture"}
            if rank is not None:
                ordering = list("bcd")
                ordering.insert(rank - 1, "a")
                output = {"query_id": str(i), "status": "ok",
                          "scores": [{"candidate_id": candidate, "score": 4 - j}
                                     for j, candidate in enumerate(ordering)]}
            run["outputs"].append(output)
        result = evaluate(benchmark, run)
        cohorts = {(c["group_id"], c["cohort_id"]): c for c in result["cohorts"]}
        for key, expected in {("g1", "c1"): 2 / 3, ("g1", "c2"): 1 / 4, ("g2", "c3"): 1 / 3}.items():
            self.assertAlmostEqual(cohorts[key]["conditional"]["metrics"]["rr"], expected)
        groups = {g["group_id"]: g for g in result["groups"]}
        self.assertAlmostEqual(groups["g1"]["conditional"]["metrics"]["rr"], 11 / 24)
        self.assertAlmostEqual(groups["g2"]["conditional"]["metrics"]["rr"], 1 / 3)
        self.assertIsNone(groups["empty"]["conditional"]["metrics"])
        self.assertIsNone(cohorts[("g1", "empty")]["conditional"]["metrics"])
        self.assertAlmostEqual(result["summary"]["conditional"]["metrics"]["rr"], 19 / 48)

    def test_main_replace_failure_preserves_previous_report(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "result.json"
            previous = b"previous successful report\n"
            destination.write_bytes(previous)
            completed_reports = []

            def fail_replace(source, target):
                self.assertEqual(target, destination)
                self.assertEqual(Path(source).parent, destination.parent)
                # A complete, closed file must exist before replacement.
                with Path(source).open(encoding="utf-8") as report:
                    completed_reports.append(json.load(report))
                raise OSError("injected replacement failure")

            argv = ["evaluate_rankings", "--benchmark", str(root / "tests/fixtures/evaluator/benchmark.json"),
                    "--run", str(root / "tests/fixtures/evaluator/run.json"), "--output", str(destination)]
            with patch.object(sys, "argv", argv), patch("scripts.evaluate_rankings.os.replace", side_effect=fail_replace), \
                    patch("sys.stderr", new_callable=io.StringIO) as stderr:
                with self.assertRaises(SystemExit) as error:
                    main()
            self.assertEqual(error.exception.code, 2)
            self.assertIn("injected replacement failure", stderr.getvalue())
            self.assertEqual(len(completed_reports), 1)
            self.assertAlmostEqual(completed_reports[0]["queries"][0]["metrics"]["rr"], 13 / 18)
            self.assertEqual(destination.read_bytes(), previous)
            self.assertEqual(list(Path(temp).iterdir()), [destination])

    def test_main_partial_write_preserves_previous_report(self):
        root = Path(__file__).resolve().parents[1]
        real_open = io.open
        partial_writes = []

        class FailingWriter:
            def __init__(self, stream):
                self.stream = stream

            def __getattr__(self, name):
                return getattr(self.stream, name)

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return self.stream.__exit__(*args)

            def write(self, text):
                self.stream.write(text[:17])
                self.stream.flush()
                partial_writes.append(text[:17])
                raise OSError("injected partial write failure")

        def faulty_open(file, mode="r", *args, **kwargs):
            stream = real_open(file, mode, *args, **kwargs)
            return FailingWriter(stream) if "w" in mode else stream

        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "result.json"
            previous = b"previous successful report\n"
            destination.write_bytes(previous)
            argv = ["evaluate_rankings", "--benchmark", str(root / "tests/fixtures/evaluator/benchmark.json"),
                    "--run", str(root / "tests/fixtures/evaluator/run.json"), "--output", str(destination)]
            with patch.object(sys, "argv", argv), patch("io.open", side_effect=faulty_open), \
                    patch("sys.stderr", new_callable=io.StringIO) as stderr:
                with self.assertRaises(SystemExit) as error:
                    main()
            self.assertEqual(error.exception.code, 2)
            self.assertIn("injected partial write failure", stderr.getvalue())
            self.assertEqual(len(partial_writes), 1)
            self.assertEqual(destination.read_bytes(), previous)
            self.assertEqual(list(Path(temp).iterdir()), [destination])


if __name__ == "__main__":
    unittest.main()
