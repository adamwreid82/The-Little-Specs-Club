# The Little Specs Club production instructions

## Codex implementation update: 2026-10-25

This file contains historical production checkpoints below. A dated checkpoint is
NOT proof of the latest approved candidate. Before every task, reconcile the
current Drive review index, exact approved asset hashes, GitHub manifests and
newer approvals. Never infer a source change from an old checkpoint.

Codex's approved initial role is to **write and test production QA code**,
not replace artists, generate or overwrite source artwork, silently correct
characters, or self-approve a spread or reference sheet. Work in a separate
branch and open a pull request; do not merge automatically.

For character sheets, read QA/REFERENCE_SHEETS.md, run
python QA/check_reference_sheets.py, and use QA/reference-sheet-ledger.yaml.
The ledger initially has 27 characters / 216 required views, all pending.
Ben and Leo are comparison standards only, not auto-verified sheet approvals.
Never claim the script performed image likeness comparison. A visible feature
that cannot be checked is UNVERIFIED. The approval record must preserve
Adam's exact evidence for the exact raw image hash. Never invent evidence.

Do not change user-approved normal or construction clothing, faces, builds,
PPE colors, helmet logos, sticker locations, or approved source file bytes.
Use character-specific source image and profile. For small artwork repairs,
preserve already-correct regions; any artwork edit needs separate authorization
beyond this technical QA implementation.

GitHub is the production control record. Approved Drive canon/profile/source pairs remain the visual authority and Drive stores the artwork. Use both on every review or production task.

## Before work

Read the spread manifest, its active_review record and linked audits, CANON/source-registry.yaml, character rules, applicable book/construction/layout rules and the current Drive review index. Read this file at the start of every production session. Reconcile current Drive and GitHub records before choosing a candidate. Use the newest explicitly identified candidate, preserving historical approved assets and rejected drafts.

## Current review mode, authorized by Adam on 2026-10-10

Adam authorized an autonomous correction pass through the remaining Book 1 spreads, Pages 13–32: audit each spread, fix every identified issue, rerun the canon check and repeat corrections. Always compare every named person to BOTH the approved Drive source PNG and profile on each spread. Continue between candidates without waiting for feedback. Keep hidden or genuinely unmeasurable items explicitly UNVERIFIED; never count them as passes. Save each candidate and audit to Drive and GitHub. This production authorization does not approve new artwork; final candidate approval remains Adam’s. Preserve existing lettering as content-space placeholders and do not redo fonts. Preserve approved Pages 3–12 and earlier candidates.

## Saving and synchronizing

Save each separate revision and its audit to Drive. Record candidate Drive IDs, filename, SHA-256, dimensions, audit reference, unresolved issues and approval state in the GitHub spread manifest. Commit the audit and checking evidence to GitHub. Update the Drive review index with those references and the GitHub checkpoint. Preserve all earlier candidates and approval evidence.

When Adam explicitly approves a candidate, update BOTH Drive review records and the GitHub candidate/approval records, naming the exact approved version, bytes and scope and recording his explicit approval wording. Never transfer a historical lock to a newer candidate. A correction request is not approval. A repository change, successful CI or visual review does not grant approval.

When a correction exposes a recurring canon detail, add a source-grounded regression check to GitHub using the existing approved profile/PNG authority. Separate existing-canon checks from a proposed new design standard; a new standard requires explicit author approval. Do not overwrite approved source images merely because a spread was repaired.

On explicit approval, move all earlier spread artwork, proofs, editable candidates and their per-version audits into the approved spread’s Superseded folder, each in an identifiable version/date folder. Preserve original file IDs, bytes and historical approval evidence; never delete or overwrite them. Keep the newly approved candidate and its current audits active. Preserve shared book-wide audits in place. Record and verify archive folder IDs and file moves in the GitHub manifest and Drive approval record. Apply the same archive inventory to repository records; Git history preserves earlier content.

## Verification limits

Run the repository mechanical checks appropriate to changed manifests and canon references. Visual source comparison remains a manual image inspection; CI validates records and references, not likeness. Keep hidden details UNVERIFIED. Pixel preservation and export dimensions do not certify native print sharpness, physical proof or complete KDP readiness.

## Current checkpoint

Pages 11–12 REV27 artwork is explicitly APPROVED by Adam Reid on 2026-10-10: “Approve”. Read BOOK-01/spread-11-12/manifest.yaml and qa/REV27_APPROVAL_2026-10-10.md. Matching Version A uses the same approved art. Eighty-five earlier spread files are preserved in 29 Superseded revision/date folders with verified inventory. Final manual wording and seventeen technical verification entries remain open; approval does not certify print readiness. Earlier spread approval evidence remains in each spread manifest. The 2026-10-10 autonomous correction authorization now permits work through Pages 13–32. Preserve approved artwork unless Adam explicitly requests a change.
