"""Synthetic paired comparisons with unequal groups and known differences."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import random

from scripts.compare_rankings import compare, main


def fixture(rows):
    benchmark = {"track_id": "feature", "query_type": "GCF",
                 "candidate_universe_id": "synthetic", "queries": []}
    runs = [{**{k: benchmark[k] for k in ("track_id", "query_type", "candidate_universe_id")},
             "method_id": name, "method_version": "1", "run_id": name + "-run",
             "score_direction": "higher", "outputs": []} for name in ("a", "b")]
    for i, (group, cohort, rank_a, rank_b) in enumerate(rows):
        qid = str(i)
        benchmark["queries"].append({"query_id": qid, "group_id": group, "cohort_id": cohort,
                                     "candidate_ids": list("abcd"), "products": {"p": ["a"]}})
        for run, rank in zip(runs, (rank_a, rank_b)):
            output = {"query_id": qid, "status": "execution_failure", "reason": "fixture"}
            if rank is not None:
                ordering = list("bcd")
                ordering.insert(rank - 1, "a")
                output = {"query_id": qid, "status": "ok", "scores": [
                    {"candidate_id": candidate, "score": 4 - j} for j, candidate in enumerate(ordering)]}
            run["outputs"].append(output)
    return benchmark, *runs


class ComparisonTests(unittest.TestCase):
    def test_hand_calculated_unequal_hierarchy_and_failures(self):
        inputs = fixture([("g1", "c1", 1, 2)] * 3 + [("g1", "c2", None, 1),
                                                      ("g2", "c1", 4, None)])
        result = compare(*inputs, cutoffs=(1,))
        self.assertEqual(result["population"], {"query_count": 5, "group_count": 2, "group_cohort_count": 3})
        rr = result["metrics"]["rr"]
        # A: ((1 + 0)/2 + 1/4)/2 = 3/8. B: ((1/2 + 1)/2 + 0)/2 = 3/8.
        self.assertEqual((rr["a"], rr["b"], rr["difference"]), (.375, .375, 0))
        self.assertEqual([g["differences"]["rr"] for g in result["groups"]], [-.25, .25])
        self.assertEqual(rr["interval"], {"lower": -.25, "upper": .25, "estimability": "estimable"})
        self.assertEqual([r["differences"]["rr"] for r in result["leave_one_group_out"]], [.25, -.25])
        self.assertEqual(result["evaluations"]["a"]["summary"]["status_counts"]["execution_failure"], 1)

    def test_pairing_preserves_covariance(self):
        # Both methods vary by group; every paired rr difference is exactly 1/2.
        result = compare(*fixture([("g1", "c", 1, 2), ("g2", "c", 2, None)]), cutoffs=(1,))
        self.assertEqual(result["metrics"]["rr"]["interval"],
                         {"lower": .5, "upper": .5, "estimability": "estimable"})
        self.assertEqual(result["bootstrap"]["draws"], 10000)
        self.assertEqual(result["bootstrap"]["seed"], 20260930)
        stability = result["metrics"]["rr"]["monte_carlo_stability"]
        self.assertEqual(stability["first_half_interval"], {"lower": .5, "upper": .5})
        self.assertEqual(stability["second_half_interval"], {"lower": .5, "upper": .5})
        self.assertEqual(stability["max_endpoint_difference"], 0)

    def test_same_draws_are_used_for_all_metrics(self):
        generator = random.Random(20260930)
        with patch("scripts.compare_rankings.random.Random", return_value=generator), \
                patch.object(generator, "randrange", wraps=generator.randrange) as draw:
            result = compare(*fixture([("g1", "c", 1, 2), ("g2", "c", None, 1)]))
        # Exactly two selected groups per replicate, regardless of metric count.
        self.assertEqual(draw.call_count, 20000)
        self.assertEqual(result["metrics"]["hit@1"]["interval"]["lower"], -1)
        self.assertEqual(result["metrics"]["hit@1"]["interval"]["upper"], 1)

    def test_predeclared_subset_retains_failures_and_full_population(self):
        inputs = fixture([("g1", "c", 1, 2), ("g1", "d", None, 1), ("g2", "c", 4, None)])
        declaration = {"name": "common spectrum inputs", "provenance": "frozen manifest v1, before runs",
                       "query_ids": ["1", "0"]}
        full = compare(*inputs)
        result = compare(*inputs, predeclared_subset=declaration)
        self.assertEqual({k: v for k, v in result.items() if k != "common_input_subset"}, full)
        subset = result["common_input_subset"]
        self.assertEqual(subset["population"], {"query_count": 2, "group_count": 1, "group_cohort_count": 2})
        self.assertEqual(subset["metrics"]["rr"]["difference"], -.25)
        self.assertEqual(subset["omitted_query_ids"], ["2"])
        self.assertEqual(subset["omitted_group_ids"], ["g2"])
        self.assertEqual(subset["provenance"], declaration["provenance"])
        self.assertEqual(subset["evaluations"]["a"]["summary"]["status_counts"]["execution_failure"], 1)

    def test_subset_requires_known_unique_ids_and_provenance(self):
        inputs = fixture([("g", "c", 1, 2)])
        for change in ({"query_ids": ["0", "0"]}, {"query_ids": ["unknown"]},
                       {"provenance": ""}, {"name": ""}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                compare(*inputs, predeclared_subset={"name": "eligible", "provenance": "manifest v1",
                                                     "query_ids": ["0"], **change})

    def test_empty_common_input_subset_is_not_estimable(self):
        result = compare(*fixture([("g", "c", 1, 2)]),
                         predeclared_subset={"name": "no shared inputs", "provenance": "manifest v1", "query_ids": []})
        subset = result["common_input_subset"]
        self.assertEqual(subset["estimability"], "not_estimable")
        self.assertIsNone(subset["metrics"])
        self.assertEqual(subset["population"]["group_count"], 0)
        self.assertEqual(subset["omitted_query_ids"], ["0"])
        self.assertEqual(subset["omitted_group_ids"], ["g"])
        self.assertEqual(result["metrics"]["rr"]["difference"], .5)

    def test_paired_valid_diagnostic_reweights_matched_membership(self):
        result = compare(*fixture([("g1", "c1", 1, 2)] * 3 + [("g1", "c2", 4, 1),
                                 ("g1", "c2", None, 1), ("g2", "c", 1, None)]))
        diagnostic = result["paired_valid_diagnostic"]
        self.assertEqual(diagnostic["population_role"], "outcome_dependent_diagnostic_only")
        self.assertEqual(diagnostic["population"], {"query_count": 4, "group_count": 1, "group_cohort_count": 2})
        # Recompute on paired valid membership: A=(1+1/4)/2, B=(1/2+1)/2.
        self.assertEqual(diagnostic["metrics"]["rr"], {"a": .625, "b": .75, "difference": -.125})
        self.assertEqual(diagnostic["omitted_query_ids"], ["4", "5"])
        self.assertEqual(diagnostic["omitted_group_ids"], ["g2"])
        self.assertEqual(result["population"]["query_count"], 6)
        self.assertNotIn("bootstrap", diagnostic)

    def test_no_paired_valid_outputs_is_not_estimable(self):
        result = compare(*fixture([("g1", "c", 1, None), ("g2", "c", None, 1)]))
        diagnostic = result["paired_valid_diagnostic"]
        self.assertEqual(diagnostic["estimability"], "not_estimable")
        self.assertIsNone(diagnostic["metrics"])
        self.assertEqual(diagnostic["omitted_query_ids"], ["0", "1"])
        self.assertEqual(diagnostic["omitted_group_ids"], ["g1", "g2"])

    def test_one_group_has_no_interval_or_loo_estimate(self):
        result = compare(*fixture([("g", "c1", 1, 2), ("g", "c2", 2, 4)]))
        self.assertEqual(result["population"]["group_count"], 1)
        self.assertEqual(result["metrics"]["rr"]["difference"], .375)
        self.assertEqual(result["metrics"]["rr"]["interval"],
                         {"lower": None, "upper": None, "estimability": "not_estimable"})
        self.assertIsNone(result["leave_one_group_out"][0]["differences"])
        self.assertEqual(result["leave_one_group_out"][0]["group_count"], 0)

    def test_reproducible_order_independent_and_no_mutation(self):
        inputs = fixture([("g1", "c", 1, 2), ("g2", "c", 4, None), ("g3", "c", None, 1)])
        before = copy.deepcopy(inputs)
        result = compare(*inputs)
        self.assertEqual(inputs, before)
        self.assertEqual(result, compare(*inputs))
        for run in inputs[1:]:
            run["outputs"].reverse()
        inputs[0]["queries"].reverse()
        self.assertEqual(result, compare(*inputs))

    def test_rejects_report_and_mismatched_envelope(self):
        benchmark, a, b = fixture([("g", "c", 1, 2)])
        b["candidate_universe_id"] = "different"
        with self.assertRaises(ValueError):
            compare(benchmark, a, b)
        with self.assertRaises(ValueError):
            compare(benchmark, {"summary": {}}, a)

    def test_failed_replacement_preserves_destination_and_removes_temporary(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            for name, content in zip(("benchmark", "a", "b"), fixture([("g", "c", 1, 2)])):
                (folder / (name + ".json")).write_text(json.dumps(content), encoding="utf-8")
            destination = folder / "result.json"
            previous = b"previous report\r\n"
            destination.write_bytes(previous)
            original_files = set(folder.iterdir())
            temporary_files = []

            def fail_replace(source, target):
                temporary = Path(source)
                temporary_files.append(temporary)
                self.assertEqual(Path(target), destination)
                self.assertNotEqual(temporary, destination)
                report = json.loads(temporary.read_text(encoding="utf-8"))
                self.assertEqual(report["metrics"]["rr"]["difference"], .5)
                raise OSError("injected replacement failure")

            argv = ["compare_rankings.py", "--benchmark", str(folder / "benchmark.json"),
                    "--run-a", str(folder / "a.json"), "--run-b", str(folder / "b.json"),
                    "--output", str(destination)]
            with patch.object(sys, "argv", argv), \
                    patch("scripts.compare_rankings.os.replace", side_effect=fail_replace) as replace:
                with self.assertRaises(SystemExit) as raised:
                    main()
            self.assertEqual(raised.exception.code, 2)
            replace.assert_called_once()
            self.assertEqual(destination.read_bytes(), previous)
            self.assertFalse(temporary_files[0].exists())
            self.assertEqual(set(folder.iterdir()), original_files)

    def test_cli(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            for name, content in zip(("benchmark", "a", "b"), fixture([("g", "c", 1, 2)])):
                (folder / (name + ".json")).write_text(json.dumps(content), encoding="utf-8")
            destination = folder / "result.json"
            destination.write_text("previous report", encoding="utf-8")
            command = [sys.executable, str(root / "scripts/compare_rankings.py"),
                       "--benchmark", str(folder / "benchmark.json"), "--run-a", str(folder / "a.json"),
                       "--run-b", str(folder / "b.json"), "--output", str(destination)]
            process = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(json.loads(destination.read_text())["metrics"]["rr"]["difference"], .5)
            (folder / "subset.json").write_text(json.dumps({"name": "inputs", "provenance": "manifest v1",
                                                             "query_ids": ["0"]}), encoding="utf-8")
            command.extend(["--predeclared-subset", str(folder / "subset.json")])
            process = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(json.loads(destination.read_text())["common_input_subset"]["query_ids"], ["0"])
            previous = destination.read_bytes()
            (folder / "b.json").write_text('{"outputs": [], "outputs": []}', encoding="utf-8")
            process = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(process.returncode, 2)
            self.assertIn("duplicate JSON object key", process.stderr)
            self.assertEqual(destination.read_bytes(), previous)
            self.assertFalse(list(folder.glob("*.tmp")))


if __name__ == "__main__":
    unittest.main()
