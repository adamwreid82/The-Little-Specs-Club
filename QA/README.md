# QA
Mechanical QA can PASS dimensions, manifests, filenames and other deterministic rules. Visual character/canon checks must be recorded against approved source references. Automation may reject a candidate, but it may never mark a spread FINAL LOCKED. Adam's explicit approval is required.

## Canon references and raw asset hashes

Run `python QA/check_canon.py` from any directory (or supply `--root PATH`).
This read-only check validates required source/image IDs, SHA256 syntax, shared-ID
hash consistency, the badge/emblem/sticker/Civic Ridge links, registry-key links,
full height/color coverage and child height order, sticker exclusions and duplicate
adult placement records, and existing `CHARACTERS/*/profile.yaml` references.
Duplicate YAML keys and malformed files fail rather than silently overwriting values.
The spread runner runs this check before spread manifest checks. Canon reference QA
also runs on relevant pushes and pull requests. No Drive credentials are needed in CI.

A reference PASS is **not** a raw-file hash verification, a visual canon audit,
proof of live Drive availability, or permission to mark a spread FINAL LOCKED.
The output explicitly reports `byte_verification: not_run` unless files are supplied.
The spread manifest check retains the existing positional filename command and allows
pending development folders, but rejects malformed fields and a locked state without
an `approved_by` record. That field still requires human review; arbitrary text is not
proof of Adam's approval.

For byte verification, download original files through the authorized Drive connection,
without conversion or re-encoding, then create a local YAML mapping:

```yaml
# raw-files.yaml: Drive ID -> local raw file (relative to this mapping or absolute)
1-mBZA9mDqfIQdSXOhPK83ZCvbIo30U21: downloads/emblem.png
```

```sh
python QA/check_canon.py --asset-files raw-files.yaml --json
python QA/check_canon.py --asset-files raw-files.yaml --require-all-assets --strict
python -m unittest discover -s QA -p 'test_*.py' -v
```

A subset map checks only the supplied files and reports partial coverage. Unknown IDs,
missing/unreadable supplied files, absent registered hashes, and mismatching bytes fail.
`--require-all-assets` also fails if any registered asset lacks a supplied file.
`--strict` promotes incomplete metadata warnings to failure. The tool never downloads,
modifies source files, repairs registered hashes, or grants approval.

### Adult hash audit completed 2026-09-27

The raw-Drive audit reconciled the 22 adult source/profile pairs (44 files), including
Elena Rivera and Marcus Jackson's missing profile hashes. See
`CANON/ADULT_SOURCE_HASH_AUDIT_2026-09-27.md` for the previous values, verified raw
hashes, scope, and evidence. No source art or Word profile content was changed.
This completed audit does not make future reference-only CI runs byte verification;
supply fresh raw files when checking live Drive content. The five child profile YAML
copies were separately synchronized to the verified emblem-update hashes.

## Exact active spread candidates

`run_spread_qa.py` no longer chooses the first PNG in `version-b/`. It resolves
an exact Drive ID and SHA-256 before examining candidate files or audit evidence.
It accepts the existing `active_review.candidate`, flat `active_review` identity,
and `candidate_drive_id`/`candidate_sha256` formats. Conflicting identity aliases
or explicit pointers fail. An explicit active identity can differ from historical
`version_b`; no metadata or evidence is silently borrowed from the old candidate.

Without an active identity, `version_b` is usable only when no other unarchived,
nonhistorical candidate record competes with it. Audit/index records and the known
approved LS source reference are not competing artwork candidates. Dates, revision
numbers, YAML order, file timestamps and approval flags never select a candidate.
Ambiguous records remain UNVERIFIED and their evidence is not checked.

For future reconciliation of legacy manifests, `active_candidate` may name the
exact top-level candidate record (for example `masked_local_r6_2026_10_11`). This
is a metadata pointer, not an approval. This implementation does not add pointers
or change any existing production records. If `active_review` also names an image,
both pointers must agree on ID/hash. Audit paths come from the selected record or
its explicit active review, never an unrelated top-level `qa` or old revision.

```sh
python QA/run_spread_qa.py BOOK-01/spread-13-14 --json
# Optional: map the active Drive ID to an original downloaded file.
python QA/run_spread_qa.py BOOK-01/spread-13-14 --asset-files raw-files.yaml --json
```

The raw-file map is the same ID-to-path YAML form used for canon checks; relative
paths are resolved against the map file. Otherwise, only an exact candidate file
path or its exact filename is used, never a directory scan. For existing active
records without a path, the filename is looked up under `version-b/`. Hash mismatch
fails and prevents image decoding/checks. Matching bytes are fully decoded and
checked for PNG format, canon dimensions and agreement with candidate dimensions.
Missing local files stay UNVERIFIED; there is no automatic Drive download.

`evidence_binding: PASS` means only that the selected audit cites the exact active
candidate SHA-256. It does not validate the document's findings, confirm live Drive
bytes, certify likeness, or authenticate an approval. Missing audits are UNVERIFIED;
an available audit without the candidate hash fails linkage. Image/hash checks,
recorded evidence linkage and visual review are reported separately. Visual review,
layout, typography, manuscript fidelity, and approval remain UNVERIFIED by this tool.

Exit codes: **1** for failed mechanical checks, **2** for incomplete verification.
A full artwork PASS/exit 0 is intentionally not available from this mechanical
runner. Spread QA uploads its JSON report even on a failed/incomplete run. Its
GitHub workflow still requires manual dispatch; Canon QA automatically runs the
regression suite on relevant branch pushes and PRs.

### Read-only production check — 2026-10-25

The new resolver identifies explicit active records for Pages 1–12. Pages 13–32
have competing historical/current repair records without an explicit active
pointer, so candidate resolution remains UNVERIFIED. No candidate is inferred to
be current from chronology. Pages 1–2 still has the existing manifest schema mismatch;
its selected REV9 audit also lacks the candidate hash citation required for linkage.
These findings do not revoke or grant any artwork approval. No production manifest,
artwork, source, manuscript, canon record, or prior audit was changed.
