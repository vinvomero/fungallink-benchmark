"""Read-only handoff-record checks. These do not validate scientific conclusions."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re


def prior_ledger_bytes(root, payload, amendment):
    """Reverse one documented cell suffix, proving every other byte unchanged."""
    if amendment.get("operation") != "append_cell_suffix":
        raise ValueError("unsupported provenance amendment operation")
    snapshot = (Path(root) / amendment["before_snapshot"]).read_bytes()
    if hashlib.sha256(snapshot).hexdigest() != amendment.get("before_sha256"):
        raise ValueError("provenance before-snapshot hash mismatch")
    if hashlib.sha256(payload).hexdigest() != amendment.get("after_sha256"):
        raise ValueError("provenance after hash mismatch")
    suffix = amendment.get("appended_text", "").encode("utf-8")
    if not suffix or any(c in suffix for c in (b"\t", b"\r", b"\n", b'"')):
        raise ValueError("provenance suffix must be a plain nonempty TSV cell suffix")
    lines = payload.splitlines(keepends=True)
    columns = lines[0].decode("utf-8-sig").rstrip("\r\n").split("\t")
    if len(columns) != len(set(columns)):
        raise ValueError("duplicate ledger columns")
    key_index = columns.index("relationship_id")
    field_index = columns.index(amendment["field"])
    if field_index == key_index:
        raise ValueError("provenance amendment cannot change relationship identity")
    matches = 0
    for i, line in enumerate(lines[1:], 1):
        body = line.rstrip(b"\r\n")
        ending = line[len(body):]
        cells = body.split(b"\t")
        if len(cells) != len(columns):
            raise ValueError("provenance amendment requires plain TSV rows")
        if cells[key_index].decode("utf-8") == amendment["relationship_id"]:
            matches += 1
            cell = cells[field_index]
            if cell.startswith(b'"') or not cell.endswith(suffix):
                raise ValueError("declared provenance suffix is absent")
            cells[field_index] = cell[:-len(suffix)]
            lines[i] = b"\t".join(cells) + ending
    if matches != 1:
        raise ValueError("provenance amendment must identify exactly one relationship")
    reconstructed = b"".join(lines)
    if reconstructed != snapshot:
        raise ValueError("ledger differs beyond the declared provenance suffix")
    return reconstructed


def check(root):
    root = Path(root)
    errors, warnings = [], []

    def reference(path, owner):
        if not path or not (root / path).exists():
            errors.append(f"{owner}: missing reference {path!r}")
            return False
        return True

    def read(path):
        if not reference(path, "record"):
            return {}
        try:
            return json.loads((root / path).read_text(encoding="utf-8-sig"))
        except (OSError, ValueError) as exc:
            errors.append(f"{path}: unreadable JSON: {exc}")
            return {}

    index = read("planning/artifact-index.json")
    for item in index.get("artifacts", []) + index.get("collections", []):
        reference(item.get("path"), "artifact index")
    for path in read("planning/source-registry-index.json").get("registry_paths", []):
        reference(path, "source registry locator")
    questions = read("planning/questions.json").get("questions", [])
    seen = set()
    for question in questions:
        key = question.get("id")
        if not key or key in seen:
            errors.append(f"Missing or duplicate question ID: {key}")
        seen.add(key)
        if question.get("status") not in {"resolved", "partial", "blocked", "uninvestigated"}:
            errors.append(f"{key}: invalid status")
        if question.get("status") == "resolved" and not question.get("evidence"):
            errors.append(f"{key}: resolved without evidence")
        for field in ("prior_attempts", "decision", "uncertainty", "reopen_when"):
            if not question.get(field):
                errors.append(f"{key}: missing {field}")
        for path in question.get("evidence", []):
            reference(path, key)
    case_path = root / "data/curated/remaining-admission-closeout-2026-10-07.tsv"
    if case_path.exists():
        with case_path.open(encoding="utf-8-sig", newline="") as handle:
            cases = {x["case_id"]: x for x in csv.DictReader(handle, delimiter="\t")}
        for question in questions:
            if "source_row" in question and cases.get(question["id"]) != question["source_row"]:
                errors.append(f"{question['id']}: copied case row differs from authoritative ledger")
    search = "planning/search-log.tsv"
    if reference(search, "search log"):
        with (root / search).open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                reference(row.get("request_path"), row.get("record_id"))
                if row.get("result_path"):
                    reference(row["result_path"], row.get("record_id"))
                else:
                    warnings.append(f"{row.get('record_id')}: result not yet indexed")
    for run in read("planning/run-records.json").get("runs", []):
        key = run.get("id", "unnamed run")
        state = read(run.get("status_path", ""))
        reference(run.get("identity_path"), key)
        status = state.get("state")
        if not status:
            errors.append(f"{key}: incomplete state record")
        elif status in {"complete", "completed"}:
            if run.get("completion_glob"):
                found = list(root.glob(run["completion_glob"]))
                if len(found) != run.get("expected_count"):
                    errors.append(f"{key}: completion count {len(found)} != {run.get('expected_count')}")
                for receipt in found:
                    read(receipt.relative_to(root).as_posix())
            else:
                errors.append(f"{key}: terminal success lacks indexed completion outputs")
        elif status in {"failed", "error"}:
            reference(run.get("failure_record"), key)
        else:
            warnings.append(f"{key}: nonterminal {status}; verify live process before resumption")
            if not run.get("process_record"):
                errors.append(f"{key}: nonterminal run lacks process record")
        if run.get("process_record"):
            process = read(run["process_record"])
            if not process.get("pid") or not process.get("process", {}).get("start_ticks"):
                errors.append(f"{key}: incomplete process identity")
    protected = read("planning/protected-records-before-2026-10-08.json")
    # Preserve the original baseline. Dated, append-only admissions may extend
    # the mutable label ledger without rewriting any previously protected byte.
    amendments = read("planning/authorized-record-amendments.json") if (root / "planning/authorized-record-amendments.json").exists() else {}
    supersessions_path = "planning/provenance-supersession-amendments.json"
    supersessions = read(supersessions_path) if (root / supersessions_path).exists() else {}
    for path, expected in protected.items():
        if reference(path, "protected record"):
            payload = (root / path).read_bytes()
            actual = hashlib.sha256(payload).hexdigest()
            if path in supersessions:
                amendment = supersessions[path]
                try:
                    if path != "data/curated/label-evidence.tsv":
                        raise ValueError("provenance amendment is restricted to the label ledger")
                    if not (reference(amendment.get("decision_path"), "provenance amendment")
                            and reference(amendment.get("verification_path"), "provenance amendment")):
                        raise ValueError("missing provenance amendment evidence")
                    payload = prior_ledger_bytes(root, payload, amendment)
                    actual = hashlib.sha256(payload).hexdigest()
                except (KeyError, OSError, UnicodeError, ValueError) as exc:
                    errors.append(f"Invalid provenance amendment for {path}: {exc}")
                    continue
            if actual != expected:
                amendment = amendments.get(path, {})
                prefix_bytes = amendment.get("preserved_prefix_bytes", 0)
                authorized = (
                    path == "data/curated/label-evidence.tsv"
                    and amendment.get("baseline_sha256") == expected
                    and amendment.get("current_sha256") == actual
                    and isinstance(prefix_bytes, int)
                    and 0 < prefix_bytes < len(payload)
                    and hashlib.sha256(payload[:prefix_bytes]).hexdigest() == expected
                    and reference(amendment.get("decision_path"), "admission amendment")
                    and reference(amendment.get("verification_path"), "admission amendment")
                )
                if not authorized:
                    errors.append(f"Protected record changed since handoff baseline: {path}")
    for path in ("planning/CURRENT_STATE.md", "planning/RECOVERY.md"):
        if reference(path, "startup"):
            text = (root / path).read_text(encoding="utf-8")
            for link in re.findall(r"\]\(([^)]+)\)", text):
                if not re.match(r"[a-z]+://", link) and not link.startswith("#"):
                    reference((Path(path).parent / link.split("#")[0]).as_posix(), path)
    return {"scope": "Record structure and file presence only; not scientific validation or a live process probe.",
            "questions_checked": len(questions), "protected_records_checked": len(protected),
            "errors": errors, "warnings": warnings, "ok": not errors}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, help="Optionally save the report; default is read-only")
    args = parser.parse_args()
    result = check(args.root)
    output = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    print(output, end="")
    raise SystemExit(0 if result["ok"] else 1)
