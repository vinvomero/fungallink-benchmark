"""Negative fixtures exercise record checks, not scientific conclusions."""
import importlib.util
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("project_state", Path(__file__).resolve().parents[1] / "scripts/check_project_state.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RecordsTest(unittest.TestCase):
    def test_provenance_suffix_preserves_other_cells_and_exact_bytes(self):
        before = b"relationship_id\talternative_loci_status\tlabel\r\nr1\told evidence\tdirect\r\nr2\tnone\treference\r\n"
        suffix = " | CURRENT SUPERSESSION: correction.md"
        after = before.replace(b"old evidence", b"old evidence" + suffix.encode())
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "before.tsv").write_bytes(before)
            amendment = {
                "operation": "append_cell_suffix", "before_snapshot": "before.tsv",
                "before_sha256": hashlib.sha256(before).hexdigest(),
                "after_sha256": hashlib.sha256(after).hexdigest(),
                "relationship_id": "r1", "field": "alternative_loci_status",
                "appended_text": suffix,
            }
            self.assertEqual(module.prior_ledger_bytes(root, after, amendment), before)
            # Even a matching new after-hash cannot authorize changes elsewhere.
            changed_other_cell = after.replace(b"direct", b"rejected")
            edited = dict(amendment, after_sha256=hashlib.sha256(changed_other_cell).hexdigest())
            with self.assertRaisesRegex(ValueError, "beyond the declared"):
                module.prior_ledger_bytes(root, changed_other_cell, edited)
            changed_suffix = after.replace(b"correction.md", b"fabricated.md")
            edited = dict(amendment, after_sha256=hashlib.sha256(changed_suffix).hexdigest())
            with self.assertRaisesRegex(ValueError, "suffix is absent"):
                module.prior_ledger_bytes(root, changed_suffix, edited)
            with self.assertRaisesRegex(ValueError, "after hash mismatch"):
                module.prior_ledger_bytes(root, after, dict(amendment, after_sha256="0" * 64))
            (root / "before.tsv").write_bytes(before.replace(b"reference", b"direct"))
            with self.assertRaisesRegex(ValueError, "before-snapshot hash mismatch"):
                module.prior_ledger_bytes(root, after, amendment)

    def test_missing_reference_resolved_without_evidence_and_incomplete_run(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "planning").mkdir()
            def put(name, value):
                (root / name).write_text(json.dumps(value), encoding="utf-8")
            put("planning/artifact-index.json", {"artifacts": [{"path": "missing.tsv"}]})
            put("planning/source-registry-index.json", {"registry_paths": []})
            put("planning/questions.json", {"questions": [{"id": "q", "status": "resolved", "evidence": [], "prior_attempts": "attempt", "decision": "decision", "uncertainty": "scope", "reopen_when": "new evidence"}]})
            put("planning/run-records.json", {"runs": [{"id": "r", "status_path": "state.json", "identity_path": "identity.json"}]})
            put("state.json", {"state": "complete"})
            put("identity.json", {})
            put("planning/protected-records-before-2026-10-08.json", {})
            (root / "planning/search-log.tsv").write_text("record_id\trequest_path\tresult_path\n", encoding="utf-8")
            for name in ["CURRENT_STATE.md", "RECOVERY.md"]:
                (root / "planning" / name).write_text("Fixture", encoding="utf-8")
            report = module.check(root)
            self.assertFalse(report["ok"])
            self.assertEqual(len(report["errors"]), 3)
            self.assertTrue(any("missing.tsv" in e for e in report["errors"]))
            self.assertTrue(any("resolved without evidence" in e for e in report["errors"]))
            self.assertTrue(any("terminal success lacks" in e for e in report["errors"]))
            # Repair each record; the same fixture must then pass.
            (root / "missing.tsv").write_text("evidence", encoding="utf-8")
            question = json.loads((root / "planning/questions.json").read_text(encoding="utf-8"))
            question["questions"][0]["evidence"] = ["missing.tsv"]
            put("planning/questions.json", question)
            put("done.json", {"state": "complete"})
            put("planning/run-records.json", {"runs": [{"id": "r", "status_path": "state.json", "identity_path": "identity.json", "completion_glob": "done.json", "expected_count": 1}]})
            self.assertTrue(module.check(root)["ok"])


if __name__ == "__main__":
    unittest.main()
