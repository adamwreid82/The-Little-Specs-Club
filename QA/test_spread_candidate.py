"""Synthetic candidate/evidence fixtures; no production artwork or approvals."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from PIL import Image
import yaml
from check_canon import read_yaml
from run_spread_qa import inspect_spread
from spread_candidate import resolve_candidate

ROOT = Path(__file__).resolve().parents[1]
SID = "synthetic_drive_id_12345"


def manifest():
    return {"spread": "13-14", "status": "REVIEW_REQUIRED", "version_b": {
        "path": "version-b/", "status": "review_required",
        "drive_id": SID, "sha256": "a" * 64, "dimensions_pixels": [8, 4],
        "filename": "active.png", "audit_path": "qa/current.md"}}


class ResolutionTests(unittest.TestCase):
    def test_nested_active_candidate_wins_over_stale_version_b(self):
        data = manifest()
        data["active_review"] = {"candidate": {"drive_id": "current_drive_id_1234", "sha256": "b" * 64}}
        candidate, _, issues = resolve_candidate(data)
        self.assertFalse(issues)
        self.assertEqual(candidate["drive_id"], "current_drive_id_1234")

    def test_nested_conflicting_outer_identity_fails(self):
        data = manifest()
        data["active_review"] = {"drive_id": SID, "sha256": "a" * 64,
                                 "candidate": {"drive_id": SID, "sha256": "b" * 64}}
        with self.assertRaisesRegex(ValueError, "conflicts"):
            resolve_candidate(data)

    def test_flat_candidate_aliases(self):
        data = manifest()
        data["active_review"] = {"candidate_drive_id": SID, "candidate_sha256": "b" * 64}
        self.assertEqual(resolve_candidate(data)[0]["sha256"], "b" * 64)

    def test_direct_active_review_title_schema(self):
        data = {"active_review": {"drive_id": SID, "sha256": "b" * 64, "revision": "REV9"}}
        self.assertFalse(resolve_candidate(data)[2])

    def test_audit_only_review_uses_unambiguous_version_b(self):
        data = manifest()
        data["active_review"] = {"audit_path": "qa/current.md"}
        self.assertEqual(resolve_candidate(data)[0]["record"], "version_b")

    def test_repairs_without_pointer_block_older_version_b(self):
        data = manifest()
        data["repair_r6"] = {"png_drive_id": "repaired_drive_id_123", "sha256": "b" * 64}
        self.assertIsNone(resolve_candidate(data)[0])
        self.assertTrue(resolve_candidate(data)[2])
        data["active_candidate"] = "repair_r6"
        self.assertEqual(resolve_candidate(data)[0]["sha256"], "b" * 64)

    def test_conflicting_explicit_pointers_rejected(self):
        data = manifest()
        data["active_candidate"] = "version_b"
        data["active_review"] = {"drive_id": SID, "sha256": "b" * 64}
        with self.assertRaisesRegex(ValueError, "conflicts"):
            resolve_candidate(data)

    def test_malformed_active_review_never_falls_back(self):
        for value in (None, [], "REV1", {"candidate": None}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                resolve_candidate(dict(manifest(), active_review=value))

    def test_missing_hash_is_unverified_invalid_hash_is_error(self):
        data = manifest()
        del data["version_b"]["sha256"]
        self.assertTrue(resolve_candidate(data)[2])
        data["version_b"]["sha256"] = "invalid"
        with self.assertRaises(ValueError):
            resolve_candidate(data)

    def test_conflicting_aliases_fail(self):
        data = manifest()
        data["version_b"]["candidate_drive_id"] = "other_drive_id_12345"
        with self.assertRaises(ValueError):
            resolve_candidate(data)

    def test_reference_standard_is_not_a_competing_candidate(self):
        data = manifest()
        data["approved_LS_application_reference"] = {"drive_id": "source_drive_id_1234", "sha256": "b" * 64}
        self.assertFalse(resolve_candidate(data)[2])
        approved = read_yaml(ROOT / "BOOK-01/spread-11-12/manifest.yaml")
        self.assertEqual(resolve_candidate(approved)[0]["drive_id"], approved["version_b"]["drive_id"])

    def test_production_active_records_and_ambiguity(self):
        data = read_yaml(ROOT / "BOOK-01/spread-05-06/manifest.yaml")
        self.assertEqual(resolve_candidate(data)[0]["sha256"], data["active_review"]["candidate_sha256"])
        data = read_yaml(ROOT / "BOOK-01/spread-13-14/manifest.yaml")
        self.assertIsNone(resolve_candidate(data)[0])


class InspectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.spread = self.root / "BOOK-01/spread-13-14"
        (self.spread / "version-b").mkdir(parents=True)
        (self.spread / "qa").mkdir()
        (self.root / "CANON").mkdir()
        (self.root / "CANON/global-canon.yaml").write_text("spread: {width_px: 8, height_px: 4}")
        self.image = self.spread / "version-b/active.png"
        Image.new("RGB", (8, 4), "green").save(self.image)
        self.data = manifest()
        self.data["version_b"]["sha256"] = hashlib.sha256(self.image.read_bytes()).hexdigest()
        self.evidence = self.spread / "qa/current.md"
        self.evidence.write_text("Synthetic candidate SHA-256: " + self.data["version_b"]["sha256"])

    def inspect(self, **kwargs):
        (self.spread / "manifest.yaml").write_text(yaml.safe_dump(self.data))
        return inspect_spread(self.spread, self.root, **kwargs)

    def test_exact_filename_selected_despite_other_png(self):
        Image.new("RGB", (3, 3)).save(self.spread / "version-b/aaa-old.png")
        report = self.inspect()
        self.assertEqual(report["byte_verification"], "PASS")
        self.assertEqual(report["image_status"], "PASS")
        self.assertEqual(report["evidence_binding"], "PASS")
        self.assertEqual(report["visual_review"], "UNVERIFIED")
        self.assertFalse(report["approval_authenticated"])

    def test_no_filename_never_scans_directory(self):
        del self.data["version_b"]["filename"]
        self.assertEqual(self.inspect()["byte_verification"], "UNVERIFIED")

    def test_map_must_supply_exact_active_drive_id(self):
        self.assertEqual(self.inspect(file_map={"old_drive_id": str(self.image)})["byte_verification"], "UNVERIFIED")
        self.assertEqual(self.inspect(file_map={SID: "version-b/active.png"}, map_base=self.spread)["byte_verification"], "PASS")

    def test_hash_mismatch_skips_image_checks(self):
        self.image.write_bytes(b"tampered")
        report = self.inspect()
        self.assertEqual(report["byte_verification"], "FAIL")
        self.assertEqual(report["image_status"], "UNVERIFIED")

    def test_wrong_format_or_dimensions_fail(self):
        for size, fmt in (((7, 4), "PNG"), ((8, 4), "JPEG")):
            with self.subTest(fmt=fmt):
                Image.new("RGB", size).save(self.image, format=fmt)
                self.data["version_b"]["sha256"] = hashlib.sha256(self.image.read_bytes()).hexdigest()
                self.assertEqual(self.inspect()["image_status"], "FAIL")

    def test_recorded_dimensions_must_match_decode(self):
        self.data["version_b"]["dimensions_pixels"] = [9, 4]
        self.assertEqual(self.inspect()["image_status"], "FAIL")

    def test_stale_audit_is_not_current_evidence(self):
        self.evidence.write_text("Old candidate SHA-256: " + "b" * 64)
        self.assertEqual(self.inspect()["evidence_binding"], "FAIL")

    def test_missing_audit_unverified(self):
        self.evidence.unlink()
        self.assertEqual(self.inspect()["evidence_binding"], "UNVERIFIED")

    def test_ambiguous_candidate_skips_all_evidence(self):
        self.data["repair"] = {"png_drive_id": "repaired_drive_id_123", "sha256": "b" * 64}
        report = self.inspect()
        self.assertEqual(report["candidate_resolution"], "UNVERIFIED")
        self.assertNotIn("audit_path", report)
        self.assertEqual(report["byte_verification"], "UNVERIFIED")

    def test_paths_and_symlinks_cannot_escape_spread(self):
        for filename in ("../active.png", "/tmp/active.png"):
            self.data["version_b"]["filename"] = filename
            self.assertTrue(self.inspect()["errors"])
        self.data["version_b"]["filename"] = "link.png"
        (self.spread / "version-b/link.png").symlink_to(self.root / "elsewhere.png")
        self.assertTrue(self.inspect()["errors"])

    def test_audit_path_cannot_escape_repository(self):
        self.data["version_b"]["audit_path"] = "../../../../outside.md"
        self.assertEqual(self.inspect()["evidence_binding"], "FAIL")

    def test_repository_relative_audit_supported(self):
        self.data["version_b"]["audit_path"] = "BOOK-01/spread-13-14/qa/current.md"
        self.assertEqual(self.inspect()["evidence_binding"], "PASS")

    def test_explicit_active_never_borrows_old_audit(self):
        self.data["active_review"] = {"drive_id": SID, "sha256": self.data["version_b"]["sha256"]}
        self.assertEqual(self.inspect()["evidence_binding"], "UNVERIFIED")

    def test_cli_works_outside_repo_and_reports_unverified_exit(self):
        proc = subprocess.run([sys.executable, str(ROOT / "QA/run_spread_qa.py"),
                               str(ROOT / "BOOK-01/spread-13-14"), "--json"],
                              cwd=self.root, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["candidate_resolution"], "UNVERIFIED")


if __name__ == "__main__":
    unittest.main()
