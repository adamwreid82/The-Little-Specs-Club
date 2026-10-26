# Initial setup audit — 2026-10-25

Scope: read-only audit of main `267370f7dc80bf24dd8634895d683428db9ae0c6`
and draft PR #1 head `0451a209c97e80d433d0b0eaeab1e7ef2bc3c9e3`, followed by
QA-only hardening on `codex/reference-sheet-qa-hardening-2026-10-25`.
The development branch starts from PR #1; the follow-up PR targets that branch
so its incremental changes can be reviewed independently. Neither PR is merged.

## Existing and operational

- Read AGENTS.md, README, QA and character/book documentation, source registry,
  validator implementation, workflow definitions, and series illustration workflow.
- Main has 23 passing regression tests. Canon reference validation passes strictly:
  27 characters and 79 distinct registered assets, no warnings. Raw-byte verification
  was NOT run. Registry hashes are recorded expectations, not fresh Drive attestations.
- Existing canon checks cover ID/hash syntax, cross-links, height order and coverage,
  helmet colors, emblem/logo consistency, sticker placements and source profile copies.
- PR #1 supplies a strict-YAML eight-angle ledger/validator, documentation, and
  15 additional tests (38 total, despite its description saying 13). Its observed
  Actions run 40221937008 completed successfully.
- The PR ledger contains 27 characters and 216 missing review angles, no registered
  sheets and no approval records. This is missing registration, NOT evidence that
  no reference artwork exists in Drive. Ben/Leo are benchmarks only.
- All 16 active Book 1 manifests were checked using the existing validator: 15
  pass structurally. `BOOK-01/spread-01-02/manifest.yaml` fails with missing
  `spread`, missing `version_b`, and non-mapping `version_a`. No manifest changed.
- Existing versioned spread audits, archives and candidate metadata already provide
  production history. A series-wide illustration workflow and production template
  already exist; they were not recreated.

## Findings and implemented hardening

PR #1's angle reviews were not bound to candidate hashes/revisions or source
hashes. Changing those could leave an old visual PASS record structurally valid.
Reviews now require exact candidate ID/hash/revision, both character-specific
source hashes and IDs, inspection evidence, reviewer and a valid calendar date.
Approvals additionally require exact candidate ID/revision and Adam's quoted
wording. The existing matching-hash and named-author checks remain. These are
metadata checks; software cannot authenticate a reviewer or Adam's consent.

Reports now separate mechanical status, recorded visual-review status and raw
sheet-byte status, and identify each character's eight angle states. Missing
reviews remain UNVERIFIED. Hidden checks remain explicitly listed when they have
no visible PASS across views. Recorded failures retain required repair notes.
Malformed status values fail without crashing. No actual reviews were populated.

Python 3.12 setup uses the existing PyYAML/Pillow dependencies, pinned in
`requirements-dev.txt`; both Python workflows use it. Canon CI saves JSON reports
as artifacts. Local setup and exact-version evidence requirements are documented
in `QA/REFERENCE_SHEETS.md`. Python cache/virtualenv files are ignored.

## Verification

- Python 3.12 virtualenv: `/workspace/lsc-venv`; installed PyYAML 6.0.3, Pillow 12.0.0.
- 52 unit/CLI tests pass: original 38 plus 14 hardening tests. Synthetic review and
  approval fixtures are test data only, never production approvals.
- Scenarios include missing characters/views, unknown characters/angles, duplicate
  YAML keys, changed source hashes and candidate identity/hash/revision, invalid
  metadata/dates, missing evidence, failed checks, unauthorized approver, missing
  exact approval wording, matching/tampered/unreadable/unregistered raw files,
  pending inventory and completion/raw-file gates.
- `python QA/check_canon.py --strict --json`: PASS, bytes not_run, 0/79 verified.
- `python QA/check_reference_sheets.py --json`: mechanical PASS; visual and sheet
  bytes UNVERIFIED; 0 registered sheets, 216 missing angles, 0 approval records.
- `--require-complete`: expected exit 1 with an incomplete report.
- Existing spread runner on 13–14: canon and manifest structure pass; reports no
  local Version B PNG. That run does not verify Drive artwork or layout.
- `git diff --check`: clean. Protected paths are unchanged from PR #1's head.
- New remote CI results are available on the follow-up PR; do not interpret green
  Actions checks as an artwork approval or print-readiness finding.

## Access actually checked

GitHub connector reads, authenticated repository CLI access, and Drive read access
work. Drive master-canon folder metadata and children were read; the current
review index `1txG_ODz4IcnD2RP5Dy0A6-WjEwF8Sb8L` was fetched. It retains unresolved
repair findings and historical approvals. Ben's registered PNG metadata is
accessible. Its bytes were not downloaded or compared. This does not establish
availability/hash consistency for every asset or certify that the older index is
fully reconciled with newer repository checkpoints. No Drive files were written.

CI has no demonstrated Drive credentials. It deliberately validates offline records;
live original-byte retrieval and visual comparisons must use authorized access.
No other service is assumed available or needed for this setup.

## Remaining work and approvals

- Register real Drive reference deliverables, verify original bytes against hashes,
  inspect each angle against its own approved PNG and written profile, and save
  version-specific evidence. All artwork likeness remains UNVERIFIED in this setup.
- Revision history is preserved through existing Drive versions/audits and Git;
  there is no new automated append-only repair ledger or Drive immutability guard.
  Changing a candidate invalidates old review evidence; it does not repair artwork.
- The spread runner selects the first local `version-b/*.png`, rather than resolving
  the manifest's current active candidate, and skips image checks when none is local.
  Its dimension checker covers size only, not format/DPI/print sharpness, gutter,
  typography or manuscript fidelity. Full five-book QA orchestration remains pending.
- The Approval Gate workflow prints a reminder; it does not enforce authenticated
  author consent. Manifest `approved_by` text alone is not adequate evidence.
- Historical typography references differ (Architects Daughter in typography canon
  versus scoped Roboto guidance for new composition restarts). Resolve applicability
  against actual approved records before implementing typography gates; do not
  silently rewrite locked standards or apply new rules to historical approvals.
- Adam reviews code PRs and explicitly approves each exact artwork version. Source
  changes, new canon standards, publication and final artwork approvals remain
  outside this assignment. No approval is required to continue routine QA coding.

Recommended next development task: resolve active spread candidates from manifests,
bind technical and visual evidence to the exact candidate hash and manuscript,
and report unavailable Drive bytes as UNVERIFIED. Then register the first existing
reference sheet with real source comparisons. Preserve all earlier versions.

No artwork, manuscript, approved source file, locked canon record, or production
manifest was changed. No artwork was generated, visually passed, approved, published
or archived; no historical version was deleted.
