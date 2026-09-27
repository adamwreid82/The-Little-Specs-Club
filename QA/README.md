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
