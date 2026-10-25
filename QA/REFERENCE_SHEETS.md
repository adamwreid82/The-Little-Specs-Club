# Eight-angle character reference-sheet QA

This is a **source-linked review ledger**, not an image recognizer. The source image and
profile in Google Drive's **00 MASTER CANON** are authoritative. GitHub tracks
mechanical validation and reviewer evidence. Do not move, overwrite, regenerate,
or reapprove existing artwork as a side effect of these checks.

## Cast and current state

- The ledger is generated from all **27 characters** in CANON/source-registry.yaml.
- Eight required angles: front, front_right, right, back_right, back,
  back_left, left, front_left.
- Ben and Leo are **comparison standards**. Their reference_standard flag does
  **not** claim their eight-angle sheets were reviewed or approved by this system.
- Missing records stay **PENDING** and count as missing, never PASS.
- A sheet is one Drive image/deliverable containing eight views. Do not invent
  individual Drive IDs for each of its panels.

## Commands

    python QA/check_reference_sheets.py
    python QA/check_reference_sheets.py --json
    python -m unittest discover -s QA -p 'test_*.py' -v

Default validates record structure without failing just because a sheet is
unfinished. Its result is VALID_LEDGER_NOT_VISUAL_CERTIFICATION, **not**
a finished-artwork PASS. The final gate will fail until every character has
eight documented PASS views plus explicit author approval:

    python QA/check_reference_sheets.py --require-complete

To verify original raw file bytes, download files via authorized Drive access,
make a local YAML mapping of sheet Drive IDs to raw file paths, then run:

    python QA/check_reference_sheets.py --asset-files raw-sheet-files.yaml --require-all-assets

SHA-256 verification does not prove likeness, perspective, logo placement,
profile compliance or print quality. No Drive credentials should be committed.

## Register a real candidate after it exists in Drive

Replace the placeholders below with real details from approved sources:

    Ben:
      reference_standard: true
      sheet:
        drive_id: "ACTUAL_DRIVE_FILE_ID"
        sha256: "ACTUAL_RAW_FILE_SHA256"
        revision: "REV1"
      angles:
        front:
          status: UNVERIFIED
          notes: "Awaiting direct source/profile comparison"
      approval: null

For a fully reviewed angle, use this structure:

    front:
      status: PASS
      source_image_id: "<exact source registry image_id>"
      source_profile_id: "<exact source registry profile_id>"
      reviewed_by: "<reviewer who inspected image>"
      reviewed_on: "YYYY-MM-DD"
      checks:
        identity: PASS
        face: PASS
        hair: PASS
        skin: PASS
        proportions: PASS
        outfit: PASS
        hard_hat_and_color: PASS
        logos: PASS
        job_stickers: PASS

Allowed angle states: PENDING, UNVERIFIED, FAIL, PASS.
Allowed check states: PASS, FAIL, UNVERIFIED, NOT_VISIBLE.
NOT_VISIBLE requires a specific not_visible_reasons entry describing why an
element is inherently out of frame from that angle. Never use NOT_VISIBLE to
disguise an unclear detail. If a property should be visible but is unclear,
record UNVERIFIED. A view PASS means the applicable visible checks were
reviewed; a NOT_VISIBLE subcheck is not evidence that the hidden property
passed. Across views, explicitly inspect those elements from other angles.

A FAIL angle requires repair notes. Assess every person against their **own**
approved source image and written profile. Include face, hair, skin, clothes
(normal and construction), scale, glasses, helmet, LS logo, job stickers and
perspective. Maintain repair records; preserve correct pixels and earlier
versions. Do not regenerate a full character just to repair a small artifact.

## No automatic approval

Leave approval: null until Adam explicitly approves the exact candidate.
After independent verification of that authorization, record:

    approval:
      status: APPROVED
      approved_by: Adam Reid
      approved_on: "YYYY-MM-DD"
      sheet_sha256: "<registered sheet SHA256>"
      evidence: "<exact approval record ID / quote / link>"

The validator checks record completeness and matching SHA. It cannot prove
the reviewer was the author or create consent. Never infer an approval from
a passing check, a GitHub commit, or a successful CI run.

## Codex operational boundary

1. Read AGENTS.md, the source registry, character rules, current Drive index
   and existing repair ledger before any work. Begin with read-only inventory.
2. Improve QA code and tests in a separate branch/PR. Never merge automatically.
3. Metadata checks, hashes and filenames do not justify a likeness PASS.
4. Do not edit Drive, change canonical design, modify approved reference images,
   generate replacement sheets or approve artwork without separate authorization.
5. Keep all prior candidates and their histories. Never silently overwrite art.

After this PR is reviewed, the next step is to register actual Drive reference
sheet IDs and visually compare each view side by side against its own source.
That cannot be performed by this ledger alone.
