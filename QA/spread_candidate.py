"""Resolve explicit spread candidates without inferring chronology or approval."""
from pathlib import Path
import re

ID = re.compile(r"[A-Za-z0-9_-]{10,}")
SHA = re.compile(r"[0-9a-f]{64}")
IDENTITY_KEYS = ("drive_id", "candidate_drive_id", "png_drive_id", "image_drive_id")


def normalize(record, label):
    if not isinstance(record, dict):
        raise ValueError(f"{label}: candidate must be a mapping")
    result = {"record": label}
    for target, aliases in {
        "drive_id": IDENTITY_KEYS,
        "sha256": ("sha256", "candidate_sha256"),
        "filename": ("filename", "candidate_filename"),
        "dimensions": ("dimensions", "dimensions_px", "dimensions_pixels"),
    }.items():
        values = [record[k] for k in aliases if k in record]
        if values and any(v != values[0] for v in values[1:]):
            raise ValueError(f"{label}: conflicting {target} aliases")
        result[target] = values[0] if values else None
    for field, pattern in (("drive_id", ID), ("sha256", SHA)):
        value = result[field]
        if value is not None and (not isinstance(value, str) or not pattern.fullmatch(value)):
            raise ValueError(f"{label}: invalid {field}")
    result["path"] = record.get("path")
    result["revision"] = record.get("revision", record.get("version"))
    return result


def resolve_candidate(manifest):
    """Return candidate, its review record and issues; never choose by mtime/date."""
    active = manifest.get("active_review")
    if "active_review" in manifest and not isinstance(active, dict):
        raise ValueError("active_review must be a mapping")
    active = active or {}
    pointer = manifest.get("active_candidate")
    if pointer is not None:
        if not isinstance(pointer, str) or pointer not in manifest or pointer in {
            "history", "archive", "version_a", "active_candidate"
        }:
            raise ValueError("active_candidate must name a top-level candidate record")
        record, label = manifest[pointer], pointer
        # A second explicit identity cannot silently override the pointer.
        explicit = active.get("candidate", active)
        if isinstance(explicit, dict) and any(k in explicit for k in IDENTITY_KEYS):
            left, right = normalize(record, label), normalize(explicit, "active_review")
            if any(left[k] != right[k] for k in ("drive_id", "sha256")):
                raise ValueError("active_candidate conflicts with active_review")
        candidate = normalize(record, label)
        review = record if not active else active
    elif "candidate" in active or any(k in active for k in IDENTITY_KEYS):
        record = active.get("candidate", active)
        candidate = normalize(record, "active_review.candidate" if "candidate" in active else "active_review")
        review = active
        if "candidate" in active and any(k in active for k in IDENTITY_KEYS):
            outer = normalize(active, "active_review")
            if any(outer[k] != candidate[k] for k in ("drive_id", "sha256")):
                raise ValueError("Nested candidate conflicts with active_review identity")
    else:
        # No active identity: an older version_b cannot outrank other candidates.
        others = [key for key, value in manifest.items()
                  if key not in {"version_b", "version_a", "active_review", "history", "archive",
                                 "sources", "qa", "approved_LS_application_reference"}
                  and not key.startswith("historical_") and isinstance(value, dict)
                  and (any(k in value for k in IDENTITY_KEYS[1:])
                       or ("drive_id" in value and "sha256" in value))
                  and value.get("historical_status") is None
                  and value.get("archived") is not True
                  and not any(word in str(value.get("status", "")).upper()
                              for word in ("SUPERSEDED", "REJECTED", "HISTORICAL"))]
        if others:
            return None, {}, ["No explicit active identity; version_b competes with: " + ", ".join(others)]
        if not isinstance(manifest.get("version_b"), dict):
            return None, {}, ["No explicit active candidate identity"]
        candidate = normalize(manifest["version_b"], "version_b")
        review = active or manifest["version_b"]
    missing = [key for key in ("drive_id", "sha256") if candidate[key] is None]
    return candidate, review, ["Active candidate lacks " + ", ".join(missing)] if missing else []


def confined_path(raw, base, boundary):
    """Repository references must remain within the permitted tree, even via symlinks."""
    if not isinstance(raw, str) or not raw.strip() or Path(raw).is_absolute():
        raise ValueError("expected a relative nonempty path")
    path = (base / raw).resolve()
    if not path.is_relative_to(boundary.resolve()):
        raise ValueError("path escapes permitted tree")
    return path


def audit_path(review, spread, root):
    audit = review.get("audit")
    if isinstance(audit, dict):
        raw = audit.get("path")
    else:
        raw = review.get("audit_path", review.get("report", audit))
    if raw is None:
        return None
    # Existing title manifests use repository-relative paths; others use spread-relative.
    base = root if isinstance(raw, str) and raw.startswith(spread.relative_to(root).as_posix() + "/") else spread
    return confined_path(raw, base, root)
