#!/usr/bin/env python3
"""Read-only, source-linked audit of eight-angle character reference sheets.

This validates records, not visual likeness. PASS is a documented reviewer assertion,
not an image-classification result. Never grant artwork approval from this script.
"""
import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import sys

import yaml
from check_canon import read_yaml

ROOT = Path(__file__).resolve().parents[1]
ANGLES = ("front", "front_right", "right", "back_right", "back",
          "back_left", "left", "front_left")
CHECKS = ("identity", "face", "hair", "skin", "proportions", "outfit",
          "hard_hat_and_color", "logos", "job_stickers")
REVIEW_STATES = {"PENDING", "UNVERIFIED", "FAIL", "PASS"}
CHECK_STATES = {"PASS", "FAIL", "UNVERIFIED", "NOT_VISIBLE"}
SHA = re.compile(r"^[0-9a-f]{64}$")
DRIVE_ID = re.compile(r"^[A-Za-z0-9_-]{10,}$")
DATE = re.compile(r"^\d{4}-\d\d-\d\d$")


def load_yaml(path):
    # Reuse the existing strict canon loader: duplicate YAML keys must fail.
    return read_yaml(path)


def valid_id(value):
    return isinstance(value, str) and bool(DRIVE_ID.fullmatch(value))


def valid_sha(value):
    return isinstance(value, str) and bool(SHA.fullmatch(value))


def filled(value):
    return isinstance(value, str) and bool(value.strip())


def valid_date(value):
    if not isinstance(value, str) or not DATE.fullmatch(value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def audit(ledger, registry):
    """Return (errors, summary, sheets), without changing any data or files."""
    errors = []
    characters = registry.get("characters") if isinstance(registry, dict) else None
    if not isinstance(characters, dict) or not characters:
        return ["source registry has no characters mapping"], {}, {}
    entries = ledger.get("characters") if isinstance(ledger, dict) else None
    if not isinstance(entries, dict):
        return ["ledger must contain a characters mapping"], {}, {}
    if type(ledger.get("schema_version")) is not int or ledger.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if set(entries) != set(characters):
        for name in sorted(set(characters) - set(entries), key=str):
            errors.append(f"{name}: missing from ledger")
        for name in sorted(set(entries) - set(characters), key=str):
            errors.append(f"{name}: not in approved source registry")

    sheets = {}
    details = {}
    total_pass = total_fail = total_unverified = total_missing = total_approved = 0
    for name in sorted(characters, key=str):
        row = entries.get(name)
        if not isinstance(row, dict):
            errors.append(f"{name}: expected mapping")
            total_missing += len(ANGLES)
            continue
        character_error_start = len(errors)
        if type(row.get("reference_standard")) is not bool:
            errors.append(f"{name}: reference_standard must be boolean")
        if row.get("reference_standard") is True and name not in {"Ben", "Leo"}:
            errors.append(f"{name}: new visual standard requires author authorization")

        source = characters[name]
        if not isinstance(source, dict):
            errors.append(f"{name}: source registry entry must be mapping")
            source = {}
        sheet = row.get("sheet")
        if sheet is not None:
            if not isinstance(sheet, dict):
                errors.append(f"{name}: sheet must be null or mapping")
            else:
                sid, digest = sheet.get("drive_id"), sheet.get("sha256")
                if not valid_id(sid) or not valid_sha(digest):
                    errors.append(f"{name}: sheet needs a Drive ID and SHA-256")
                elif sid in sheets:
                    errors.append(f"{name}: sheet Drive ID also used by {sheets[sid][0]}")
                else:
                    sheets[sid] = (name, digest)
                if not filled(sheet.get("revision")):
                    errors.append(f"{name}: sheet.revision must identify exact candidate")
        views = row.get("angles")
        if not isinstance(views, dict):
            errors.append(f"{name}: angles must be mapping")
            views = {}
        for unknown in sorted(set(views) - set(ANGLES), key=str):
            errors.append(f"{name}: unknown angle {unknown}")

        visible_checks = set()
        angle_results = {}
        for angle in ANGLES:
            angle_error_start = len(errors)
            angle_results[angle] = "UNVERIFIED"
            v = views.get(angle)
            if v is None:
                total_missing += 1
                continue
            if not isinstance(v, dict):
                errors.append(f"{name}/{angle}: expected review mapping")
                total_unverified += 1
                continue
            state = v.get("status")
            if not isinstance(state, str) or state not in REVIEW_STATES:
                errors.append(f"{name}/{angle}: invalid status {state!r}")
                total_unverified += 1
                continue
            if state == "PASS":
                total_pass += 1
            elif state == "FAIL":
                total_fail += 1
            else:
                total_unverified += 1
            checks = v.get("checks", {})
            if not isinstance(checks, dict):
                errors.append(f"{name}/{angle}: checks must be mapping")
                checks = {}
            for key, val in checks.items():
                if key not in CHECKS or not isinstance(val, str) or val not in CHECK_STATES:
                    errors.append(f"{name}/{angle}: invalid check {key}={val!r}")
            occlusions = v.get("not_visible_reasons", {})
            if not isinstance(occlusions, dict):
                errors.append(f"{name}/{angle}: not_visible_reasons must be mapping")
                occlusions = {}
            for key in occlusions:
                if key not in CHECKS or checks.get(key) != "NOT_VISIBLE":
                    errors.append(f"{name}/{angle}: unexpected not-visible reason {key}")
            for key, val in checks.items():
                if val == "NOT_VISIBLE" and not filled(occlusions.get(key)):
                    errors.append(f"{name}/{angle}: {key} NOT_VISIBLE requires explanation")
            if state == "PASS":
                if not isinstance(sheet, dict):
                    errors.append(f"{name}/{angle}: PASS requires registered sheet")
                if set(checks) != set(CHECKS) or any(
                    val not in ("PASS", "NOT_VISIBLE") for val in checks.values()
                ):
                    errors.append(f"{name}/{angle}: PASS requires all checks PASS/NOT_VISIBLE")
                for essential in ("identity", "proportions", "outfit"):
                    if checks.get(essential) != "PASS":
                        errors.append(f"{name}/{angle}: {essential} must be visibly checked PASS")
                for key, expected in (
                    ("source_image_id", source.get("image_id")),
                    ("source_profile_id", source.get("profile_id")),
                ):
                    if not valid_id(expected) or v.get(key) != expected:
                        errors.append(f"{name}/{angle}: {key} does not match source registry")
                for key in ("image", "profile"):
                    expected = source.get(f"{key}_sha256")
                    if not valid_sha(expected) or v.get(f"source_{key}_sha256") != expected:
                        errors.append(f"{name}/{angle}: source_{key}_sha256 mismatch or unavailable")
                if not isinstance(sheet, dict) or any(
                    v.get(f"sheet_{key}") != sheet.get(key)
                    for key in ("drive_id", "sha256", "revision")
                ):
                    errors.append(f"{name}/{angle}: review must bind exact sheet ID, hash and revision")
                if not filled(v.get("evidence")):
                    errors.append(f"{name}/{angle}: PASS requires visual inspection evidence reference")
                if not filled(v.get("reviewed_by")) or not valid_date(v.get("reviewed_on")):
                    errors.append(f"{name}/{angle}: PASS requires reviewer and YYYY-MM-DD date")
            if (state == "FAIL" or "FAIL" in checks.values()) and not filled(v.get("notes")):
                errors.append(f"{name}/{angle}: FAIL requires repair notes")

            if state == "FAIL" or "FAIL" in checks.values():
                angle_results[angle] = "FAIL"
            elif state == "PASS" and len(errors) == angle_error_start:
                angle_results[angle] = "PASS"
                visible_checks.update(k for k, value in checks.items() if value == "PASS")

        approval = row.get("approval")
        if approval is not None:
            if not isinstance(approval, dict) or approval.get("status") != "APPROVED":
                errors.append(f"{name}: approval must be null or an APPROVED mapping")
            else:
                if sheet is None or set(views) != set(ANGLES) or any(
                    not isinstance(views.get(angle), dict) or
                    views[angle].get("status") != "PASS" for angle in ANGLES
                ):
                    errors.append(f"{name}: approval requires eight reviewed PASS angles")
                if approval.get("approved_by") != "Adam Reid" or not filled(
                    approval.get("evidence")
                ):
                    errors.append(f"{name}: author approval and evidence are required")
                if not isinstance(sheet, dict) or approval.get("sheet_sha256") != sheet.get("sha256"):
                    errors.append(f"{name}: approved hash must match registered sheet")
                if not valid_date(approval.get("approved_on")):
                    errors.append(f"{name}: author approval date required")
                if not isinstance(sheet, dict) or any(
                    approval.get(f"sheet_{key}") != sheet.get(key)
                    for key in ("drive_id", "revision")
                ):
                    errors.append(f"{name}: approval must bind exact sheet ID and revision")
                if not filled(approval.get("approval_quote")):
                    errors.append(f"{name}: exact author approval wording required")
                total_approved += 1
        if len(errors) > character_error_start:
            angle_results = {a: "UNVERIFIED" if status == "PASS" else status
                             for a, status in angle_results.items()}
        details[name] = {
            "sheet_registered": isinstance(sheet, dict),
            "mechanical_status": "FAIL" if len(errors) > character_error_start else "PASS",
            "visual_review_status": "FAIL" if "FAIL" in angle_results.values() else
                "PASS" if all(v == "PASS" for v in angle_results.values()) else "UNVERIFIED",
            "angles": angle_results,
            "checks_without_visible_pass": sorted(set(CHECKS) - visible_checks),
            "approval_record_present": approval is not None,
        }

    summary = {
        "character_reports": details,
        "characters": len(characters),
        "angles_required": len(characters) * len(ANGLES),
        "angles_pass_recorded": total_pass,
        "angles_fail": total_fail,
        "angles_unverified": total_unverified,
        "angles_missing": total_missing,
        "sheets_registered": len(sheets),
        "sheets_with_approval_records": total_approved,
        "visual_comparison_performed_by_script": False,
        "raw_image_verification_performed": False,
    }
    return errors, summary, sheets


def verify_sheet_files(mapping, sheets, base):
    """Verify supplied raw sheet files only; never download, rewrite, or assume bytes."""
    errors, verified = [], 0
    if not isinstance(mapping, dict):
        return ["asset-files mapping must map sheet Drive IDs to local raw paths"], verified
    for sid, path in mapping.items():
        if sid not in sheets:
            errors.append(f"{sid}: unregistered sheet ID in asset file map")
            continue
        if not isinstance(path, str) or not path.strip():
            errors.append(f"{sid}: asset path missing")
            continue
        src = Path(path)
        if not src.is_absolute():
            src = base / src
        try:
            with src.open("rb") as stream:
                h = hashlib.file_digest(stream, "sha256").hexdigest()
        except (OSError, ValueError) as exc:
            errors.append(f"{sid}: cannot read raw file ({exc})")
            continue
        if h != sheets[sid][1]:
            errors.append(f"{sid}: raw image SHA-256 mismatch")
        else:
            verified += 1
    return errors, verified


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=ROOT / "QA/reference-sheet-ledger.yaml")
    parser.add_argument("--registry", type=Path, default=ROOT / "CANON/source-registry.yaml")
    parser.add_argument("--asset-files", type=Path,
                        help="Optional YAML mapping of sheet Drive IDs to downloaded raw files")
    parser.add_argument("--require-all-assets", action="store_true",
                        help="Require raw bytes for every registered sheet")
    parser.add_argument("--require-complete", action="store_true",
                        help="Fail if any angle is not PASS or a sheet lacks author approval")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        ledger, registry = load_yaml(args.ledger), load_yaml(args.registry)
        errors, summary, sheets = audit(ledger, registry)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        errors, summary, sheets = [str(exc)], {}, {}
    verified = 0
    mapping = {}
    if args.asset_files:
        try:
            mapping = load_yaml(args.asset_files)
            file_errors, verified = verify_sheet_files(mapping, sheets, args.asset_files.parent)
            errors.extend(file_errors)
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append(f"asset files: {exc}")
    if args.require_all_assets and (not isinstance(mapping, dict) or set(sheets) != set(mapping)):
        errors.append("not all registered sheet raw files supplied")
    if args.require_complete and summary and (
        summary["angles_pass_recorded"] != summary["angles_required"]
        or summary["sheets_with_approval_records"] != summary["characters"]
    ):
        errors.append("incomplete: not all eight-angle sheets are reviewed and author-approved")
    if summary:
        summary["raw_image_verification_performed"] = bool(args.asset_files)
        summary["raw_sheet_files_verified"] = verified
    byte_status = "UNVERIFIED" if not args.asset_files or verified != len(sheets) or not sheets else "PASS"
    if args.asset_files and errors:
        byte_status = "FAIL"
    visual_states = [r["visual_review_status"] for r in summary.get("character_reports", {}).values()]
    all_reviewed = (len(visual_states) == summary.get("characters") and
                    bool(visual_states) and all(s == "PASS" for s in visual_states))
    visual_status = "FAIL" if "FAIL" in visual_states else "PASS" if all_reviewed else "UNVERIFIED"
    report = {"mechanical_status": "FAIL" if errors else "PASS",
              "visual_review_status": visual_status,
              "byte_verification_status": byte_status,
              "approval_authenticated_by_script": False,
              "result": "FAIL" if errors else "VALID_LEDGER_NOT_VISUAL_CERTIFICATION",
              "summary": summary, "errors": errors}
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"{report['result']}: {summary}")
        for err in errors:
            print("ERROR:", err, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
