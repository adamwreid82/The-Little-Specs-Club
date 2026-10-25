"""Regression tests for the non-destructive eight-angle reference-sheet audit."""
import copy
import hashlib
from pathlib import Path
import tempfile
import unittest

from check_reference_sheets import ANGLES, CHECKS, audit, load_yaml, verify_sheet_files

ROOT = Path(__file__).resolve().parents[1]
SHEET_ID = "sheet_drive_id_123456"
SHEET_HASH = "a" * 64


def fixture():
    registry = {"characters": {"Ben": {
        "image_id": "source_image_123456",
        "profile_id": "source_profile_123456",
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


if __name__ == "__main__":
    unittest.main()
