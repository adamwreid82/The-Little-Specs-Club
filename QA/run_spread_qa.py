"""Read-only spread QA for the manifest's exact candidate; never grants approval."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from PIL import Image
import yaml
from check_canon import read_yaml
from check_manifest import validate_manifest
from spread_candidate import audit_path, confined_path, resolve_candidate

ROOT = Path(__file__).resolve().parents[1]


def inspect_spread(spread, root=ROOT, file_map=None, map_base=None):
    spread, root = Path(spread).resolve(), Path(root).resolve()
    report = {
        "candidate_resolution": "UNVERIFIED", "candidate": None,
        "byte_verification": "UNVERIFIED", "image_status": "UNVERIFIED",
        "evidence_binding": "UNVERIFIED", "visual_review": "UNVERIFIED",
        "approval_authenticated": False, "errors": [], "unverified": [],
    }
    errors, pending = report["errors"], report["unverified"]
    try:
        if not spread.is_relative_to(root):
            raise ValueError("spread must be within repository root")
        manifest = read_yaml(spread / "manifest.yaml")
        errors.extend(validate_manifest(manifest))
        candidate, review, issues = resolve_candidate(manifest)
        report["candidate"] = candidate
        pending.extend(issues)
        if issues:
            return finish(report)
        report["candidate_resolution"] = "PASS"
    except (OSError, ValueError, TypeError, yaml.YAMLError) as exc:
        errors.append(str(exc))
        return finish(report)

    # Only examine evidence after an unambiguous ID/hash has been resolved.
    try:
        evidence = audit_path(review, spread, root)
        if evidence is None or not evidence.is_file():
            pending.append("Active candidate audit unavailable locally; no historical audit substituted")
        else:
            text = evidence.read_text(encoding="utf-8")
            report["audit_path"] = str(evidence.relative_to(root))
            # This certifies only a hash citation, never the correctness of a visual finding.
            if re.search(r"(?<![0-9a-fA-F])" + re.escape(candidate["sha256"]) + r"(?![0-9a-fA-F])", text):
                report["evidence_binding"] = "PASS"
            else:
                report["evidence_binding"] = "FAIL"
                errors.append("Selected audit does not cite the active candidate SHA-256")
    except (OSError, ValueError, UnicodeError) as exc:
        report["evidence_binding"] = "FAIL"
        errors.append(f"audit: {exc}")

    try:
        local = None
        if file_map is not None:
            if candidate["drive_id"] in file_map:
                raw = file_map[candidate["drive_id"]]
                if not isinstance(raw, str) or not raw.strip():
                    raise ValueError("asset map path must be nonempty text")
                local = Path(map_base or root) / raw
            else:
                pending.append("Active Drive ID absent from supplied raw-file map")
        elif candidate.get("filename"):
            filename = candidate["filename"]
            if not isinstance(filename, str) or Path(filename).name != filename or filename in {".", ".."}:
                raise ValueError("candidate filename must be a basename")
            folder = confined_path(candidate.get("path") or "version-b/", spread, spread)
            local = confined_path(filename, folder, spread)
        elif candidate.get("path"):
            path = confined_path(candidate["path"], spread, spread)
            if path.suffix.lower() == ".png":
                local = path
        if local is None or not local.is_file():
            pending.append("Exact active candidate bytes unavailable; no directory scan or filename guessing")
        else:
            with local.open("rb") as stream:
                actual = hashlib.file_digest(stream, "sha256").hexdigest()
            if actual != candidate["sha256"]:
                report["byte_verification"] = "FAIL"
                errors.append("Active candidate SHA-256 mismatch; image checks skipped")
            else:
                report["byte_verification"] = "PASS"
                with Image.open(local) as image:
                    image.load()
                    report["actual_dimensions"] = list(image.size)
                    report["actual_format"] = image.format
                    canon = read_yaml(root / "CANON/global-canon.yaml")["spread"]
                    expected = [canon["width_px"], canon["height_px"]]
                    if image.format != "PNG" or list(image.size) != expected:
                        errors.append(f"Image must be PNG at canon dimensions {expected}")
                        report["image_status"] = "FAIL"
                    elif candidate["dimensions"] is not None and candidate["dimensions"] != list(image.size):
                        errors.append("Decoded dimensions disagree with active candidate metadata")
                        report["image_status"] = "FAIL"
                    else:
                        report["image_status"] = "PASS"
    except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError, Image.DecompressionBombError) as exc:
        report["image_status"] = "FAIL"
        errors.append(f"candidate file: {exc}")
    pending.append("Visual likeness, layout, typography, manuscript and approval require separate evidence review")
    return finish(report)


def finish(report):
    report["mechanical_status"] = "FAIL" if report["errors"] else "PASS"
    report["result"] = "FAIL" if report["errors"] else "UNVERIFIED"
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spread", type=Path)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--asset-files", type=Path, help="Drive ID -> original local file YAML map")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        mapping = read_yaml(args.asset_files) if args.asset_files else None
        report = inspect_spread(args.spread, args.root, mapping,
                                args.asset_files.resolve().parent if args.asset_files else None)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        report = finish({"errors": [str(exc)], "unverified": [], "visual_review": "UNVERIFIED"})
    canon = subprocess.run([sys.executable, str(Path(__file__).with_name("check_canon.py")),
                            "--root", str(args.root), "--json"], capture_output=True, text=True)
    report["canon_references"] = json.loads(canon.stdout)
    if canon.returncode:
        report["errors"].append("Canon reference validation failed")
        finish(report)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"{report['result']}: {report.get('candidate')}")
        for key in ("candidate_resolution", "byte_verification", "image_status", "evidence_binding", "visual_review"):
            print(f"{key}: {report.get(key, 'UNVERIFIED')}")
        for key in ("errors", "unverified"):
            for issue in report[key]:
                print(f"{key.upper()}: {issue}")
    # 0 is reserved for a future complete gate; absent/visual evidence is never a success.
    return 1 if report["errors"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
