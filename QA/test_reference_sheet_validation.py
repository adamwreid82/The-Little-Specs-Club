"""Regression tests for the non-destructive eight-angle reference-sheet audit."""
import copy
import hashlib
from pathlib import Path
import tempfile
import contextlib
import io
import json
import yaml
import unittest

from check_reference_sheets import ANGLES, CHECKS, audit, load_yaml, verify_sheet_files, main

ROOT = Path(__file__).resolve().parents[1]
SHEET_ID = "sheet_drive_id_123456"
SHEET_HASH = "a" * 64


def fixture():
    registry = {"characters": {"Ben": {
        "image_id": "source_image_123456",
        "profile_id": "source_profile_123456",
        "image_sha256": "c" * 64, "profile_sha256": "d" * 64,
    }}}
    ledger = {"schema_version": 1, "characters": {"Ben": {
        "reference_standard": True, "sheet": None, "angles": {}, "approval": None,
    }}}
    return ledger, registry


def complete():
    ledger, registry = fixture()
    ledger["characters"]["Ben"]["sheet"] = {
        "drive_id": SHEET_ID, "sha256": SHEET_HASH, "revision": "REV1",
    }
    record = {
        "status": "PASS",
        "sheet_drive_id": SHEET_ID, "sheet_sha256": SHEET_HASH, "sheet_revision": "REV1",
        "source_image_sha256": "c" * 64, "source_profile_sha256": "d" * 64,
        "evidence": "Synthetic test fixture only; not a real inspection",
        "checks": {key: "PASS" for key in CHECKS},
        "source_image_id": registry["characters"]["Ben"]["image_id"],
        "source_profile_id": registry["characters"]["Ben"]["profile_id"],
        "reviewed_by": "human reviewer",
        "reviewed_on": "2026-10-25",
    }
    ledger["characters"]["Ben"]["angles"] = {
        angle: copy.deepcopy(record) for angle in ANGLES
    }
    ledger["characters"]["Ben"]["approval"] = {
        "status": "APPROVED", "approved_by": "Adam Reid",
        "sheet_drive_id": SHEET_ID, "sheet_revision": "REV1",
        "approval_quote": "Synthetic approval fixture only",
        "approved_on": "2026-10-25",
        "sheet_sha256": SHEET_HASH,
        "evidence": "Exact author approval record in Drive",
    }
    return ledger, registry


class ReferenceSheetTests(unittest.TestCase):
    def test_real_inventory_has_every_registered_character_without_false_pass(self):
        ledger = load_yaml(ROOT / "QA/reference-sheet-ledger.yaml")
        registry = load_yaml(ROOT / "CANON/source-registry.yaml")
        errors, report, _ = audit(ledger, registry)
        self.assertEqual(errors, [])
        self.assertEqual(report["characters"], len(registry["characters"]))
        self.assertEqual(report["angles_required"], 8 * len(registry["characters"]))
        self.assertEqual(report["angles_pass_recorded"], 0)
        self.assertEqual(report["sheets_with_approval_records"], 0)
        self.assertFalse(report["visual_comparison_performed_by_script"])

    def test_empty_inventory_is_not_pass(self):
        errors, report, _ = audit(*fixture())
        self.assertEqual(errors, [])
        self.assertEqual(report["angles_missing"], 8)
        self.assertEqual(report["angles_pass_recorded"], 0)

    def test_complete_record_is_structurally_valid_not_visual_certification(self):
        errors, report, _ = audit(*complete())
        self.assertEqual(errors, [])
        self.assertEqual(report["angles_pass_recorded"], 8)
        self.assertEqual(report["sheets_with_approval_records"], 1)
        self.assertFalse(report["visual_comparison_performed_by_script"])

    def test_approval_without_eight_passes_fails(self):
        ledger, registry = complete()
        del ledger["characters"]["Ben"]["angles"]["back"]
        self.assertTrue(any("approval requires eight" in e for e in audit(ledger, registry)[0]))

    def test_unverified_angle_cannot_be_approved(self):
        ledger, registry = complete()
        ledger["characters"]["Ben"]["angles"]["right"]["status"] = "UNVERIFIED"
        self.assertTrue(audit(ledger, registry)[0])

    def test_human_author_approval_record_mandatory(self):
        ledger, registry = complete()
        ledger["characters"]["Ben"]["approval"]["approved_by"] = "Codex"
        self.assertTrue(any("author approval" in e for e in audit(ledger, registry)[0]))

    def test_approval_bound_to_exact_image_hash(self):
        ledger, registry = complete()
        ledger["characters"]["Ben"]["sheet"]["sha256"] = "b" * 64
        self.assertTrue(any("approved hash" in e for e in audit(ledger, registry)[0]))

    def test_pass_requires_original_source_and_profile_ids(self):
        ledger, registry = complete()
        ledger["characters"]["Ben"]["angles"]["front"]["source_image_id"] = "different"
        self.assertTrue(any("source_image_id" in e for e in audit(ledger, registry)[0]))

    def test_missing_check_cannot_be_visual_pass(self):
        ledger, registry = complete()
        del ledger["characters"]["Ben"]["angles"]["front"]["checks"]["outfit"]
        self.assertTrue(any("all checks" in e for e in audit(ledger, registry)[0]))

    def test_not_visible_requires_explicit_reason(self):
        ledger, registry = complete()
        ledger["characters"]["Ben"]["angles"]["back"]["checks"]["face"] = "NOT_VISIBLE"
        self.assertTrue(any("NOT_VISIBLE requires explanation" in e
                            for e in audit(ledger, registry)[0]))
        ledger["characters"]["Ben"]["angles"]["back"]["not_visible_reasons"] = {
            "face": "Not geometrically visible from the back"
        }
        self.assertEqual(audit(ledger, registry)[0], [])

    def test_failed_angle_needs_ledger_reason(self):
        ledger, registry = fixture()
        ledger["characters"]["Ben"]["angles"]["left"] = {"status": "FAIL"}
        self.assertTrue(any("repair notes" in e for e in audit(ledger, registry)[0]))

    def test_unknown_character_or_angle_rejected(self):
        ledger, registry = fixture()
        ledger["characters"]["Ben"]["angles"]["underside"] = {"status": "PENDING"}
        self.assertTrue(any("unknown angle" in e for e in audit(ledger, registry)[0]))
        ledger["characters"]["Unknown"] = {}
        self.assertTrue(any("not in approved source registry" in e
                            for e in audit(ledger, registry)[0]))

    def test_raw_bytes_can_be_verified_and_tampering_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "sheet.png"
            p.write_bytes(b"unchanged approved binary")
            sha = hashlib.sha256(p.read_bytes()).hexdigest()
            sheets = {SHEET_ID: ("Ben", sha)}
            errors, matched = verify_sheet_files({SHEET_ID: "sheet.png"}, sheets, Path(tmp))
            self.assertEqual((errors, matched), ([], 1))
            p.write_bytes(b"other bytes")
            errors, matched = verify_sheet_files({SHEET_ID: "sheet.png"}, sheets, Path(tmp))
            self.assertEqual(matched, 0)
            self.assertTrue(any("mismatch" in e for e in errors))


    def test_identity_cannot_pass_as_not_visible(self):
        ledger, registry = complete()
        front = ledger["characters"]["Ben"]["angles"]["front"]
        front["checks"]["identity"] = "NOT_VISIBLE"
        front["not_visible_reasons"] = {"identity": "Unclear"}
        self.assertTrue(any("identity must be visibly checked PASS" in e
                            for e in audit(ledger, registry)[0]))

    def test_duplicate_keys_in_ledger_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "duplicate.yaml"
            p.write_text("schema_version: 1\nschema_version: 1\ncharacters: {}\n")
            with self.assertRaises(ValueError):
                load_yaml(p)


    def test_missing_character_fails(self):
        ledger, registry = fixture()
        ledger["characters"].clear()
        self.assertTrue(any("missing from ledger" in e for e in audit(ledger, registry)[0]))

    def test_changed_source_hash_invalidates_old_review(self):
        for kind in ("image", "profile"):
            with self.subTest(kind=kind):
                ledger, registry = complete()
                registry["characters"]["Ben"][kind + "_sha256"] = "e" * 64
                errors, summary, _ = audit(ledger, registry)
                self.assertTrue(any("sha256" in e for e in errors))
                self.assertEqual(summary["character_reports"]["Ben"]["visual_review_status"], "UNVERIFIED")

    def test_changed_candidate_invalidates_old_review(self):
        for key, value in (("sha256", "e" * 64), ("revision", "REV2"),
                           ("drive_id", "another_sheet_12345")):
            with self.subTest(key=key):
                ledger, registry = complete()
                ledger["characters"]["Ben"]["approval"] = None
                ledger["characters"]["Ben"]["sheet"][key] = value
                self.assertTrue(any("exact sheet" in e for e in audit(ledger, registry)[0]))

    def test_pass_needs_evidence(self):
        ledger, registry = complete()
        del ledger["characters"]["Ben"]["angles"]["front"]["evidence"]
        self.assertTrue(any("inspection evidence" in e for e in audit(ledger, registry)[0]))

    def test_invalid_calendar_date_fails(self):
        ledger, registry = complete()
        ledger["characters"]["Ben"]["angles"]["front"]["reviewed_on"] = "2026-02-31"
        ledger["characters"]["Ben"]["approval"]["approved_on"] = "2026-13-01"
        self.assertGreaterEqual(len(audit(ledger, registry)[0]), 2)

    def test_malformed_status_is_failure_not_crash(self):
        ledger, registry = complete()
        ledger["characters"]["Ben"]["angles"]["front"]["status"] = []
        self.assertTrue(audit(ledger, registry)[0])
        ledger, registry = complete()
        ledger["characters"]["Ben"]["angles"]["front"]["checks"]["face"] = []
        self.assertTrue(audit(ledger, registry)[0])

    def test_unknown_and_unreadable_raw_files_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            sheets = {SHEET_ID: ("Ben", SHEET_HASH)}
            for mapping in ({"unknown": "x.png"}, {SHEET_ID: "missing.png"}):
                self.assertTrue(verify_sheet_files(mapping, sheets, Path(tmp))[0])

    def test_exact_approval_wording_and_version_required(self):
        for field in ("approval_quote", "sheet_drive_id", "sheet_revision"):
            with self.subTest(field=field):
                ledger, registry = complete()
                del ledger["characters"]["Ben"]["approval"][field]
                self.assertTrue(audit(ledger, registry)[0])

    def test_reports_missing_and_failed_angles(self):
        ledger, registry = fixture()
        _, summary, _ = audit(ledger, registry)
        self.assertEqual(summary["character_reports"]["Ben"]["visual_review_status"], "UNVERIFIED")
        ledger["characters"]["Ben"]["angles"]["front"] = {"status": "FAIL", "notes": "Repair required"}
        errors, summary, _ = audit(ledger, registry)
        self.assertFalse(errors)
        self.assertEqual(summary["character_reports"]["Ben"]["visual_review_status"], "FAIL")

class ReferenceSheetCliTests(unittest.TestCase):
    def run_cli(self, ledger, registry, *flags):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "ledger.yaml").write_text(yaml.safe_dump(ledger))
            (root / "registry.yaml").write_text(yaml.safe_dump(registry))
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = main(["--ledger", str(root / "ledger.yaml"), "--registry",
                             str(root / "registry.yaml"), "--json", *flags])
            return code, json.loads(output.getvalue())

    def test_pending_inventory_reports_unverified(self):
        code, report = self.run_cli(*fixture())
        self.assertEqual(code, 0)
        self.assertEqual(report["mechanical_status"], "PASS")
        self.assertEqual(report["visual_review_status"], "UNVERIFIED")
        self.assertEqual(report["byte_verification_status"], "UNVERIFIED")

    def test_complete_gate_rejects_missing_views(self):
        code, report = self.run_cli(*fixture(), "--require-complete")
        self.assertEqual(code, 1)
        self.assertTrue(report["errors"])

    def test_raw_gate_rejects_missing_sheet_files(self):
        code, report = self.run_cli(*complete(), "--require-all-assets")
        self.assertEqual(code, 1)
        self.assertEqual(report["byte_verification_status"], "UNVERIFIED")

    def test_complete_synthetic_records_are_not_authenticated_approval(self):
        code, report = self.run_cli(*complete(), "--require-complete")
        self.assertEqual(code, 0)
        self.assertFalse(report["approval_authenticated_by_script"])
        self.assertFalse(report["summary"]["visual_comparison_performed_by_script"])

    def test_malformed_ledger_returns_json_failure(self):
        code, report = self.run_cli({"characters": []}, fixture()[1])
        self.assertEqual(code, 1)
        self.assertEqual(report["visual_review_status"], "UNVERIFIED")


if __name__ == "__main__":
    unittest.main()
