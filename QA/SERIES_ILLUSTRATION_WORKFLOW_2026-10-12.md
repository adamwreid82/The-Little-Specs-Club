# Series illustration production workflow (2026-10-12)

## Authority and purpose
Google Drive approved canon, source PNGs, profiles, and explicit author approvals remain authoritative. GitHub remains the durable technical production record. Airtable base appUivkPUJmlme2lL is a tracking index, NEVER a replacement authority. Consult AGENTS.md first.

## Before a first candidate
1. Resolve the exact book/spread manuscript, character cast and role, story stage, approved backdrop, construction sequence, print format and previous locked assets.
2. For EVERY visible person retrieve the approved source image AND corresponding profile; verify exact file IDs and known SHA-256 hashes against CANON/source-registry.yaml. Never invent missing hashes.
3. Build a per-character scene sheet: appearance, height relationships, locked everyday/construction clothing, PPE mark orientation/scale, equipment interaction and occlusion.
4. Select a perspective appropriate to the narrative; avoid repeated group lineups. Reserve gutter/text-safe zones before image work.
5. Assemble reference images, a scoped prompt and a negative checklist based on previous revision failures. Preserve approved reference bytes.

## Candidate and audit
1. Create Version B first with safe text area; do not approximate or rewrite locked manuscript text.
2. Check EVERY visible individual against both references using focused crops and full-spread review. Evaluate identity, hair/face, proportions, outfits, helmet/vest marks, stage, anatomy, safety, signage, typography and gutter.
3. Every requirement is PASS, FAIL, NOT VISIBLE (only definitely invisible), or UNVERIFIED. Fail and unverified visible items block automated QA pass. Record evidence and source paths.
4. Repair only sourced failed details with localized masks using the approved assets; preserve original pixels outside mask, separately version candidate, and compare masked and full image for regressions.
5. Repeat checks; automated QA does NOT imply author approval. Log revisions and decisions in Drive and GitHub, then mirror metadata in Airtable.
6. Derived Version A must share the approved illustration pixels apart from text removal. Check both variants before KDP packaging.

## Integrations
- Adobe: optional localized edits; do not silently regenerate approved characters or claim pixel preservation without comparison.
- Canva: optional editable typography and layout; confirm exact Architects Daughter 18 pt at final scale and safe zones. Never silently replace locked fonts or manuscript.
- Adobe Acrobat: optional PDF assembly/inspection; validate trim, bleed, pages, embedded fonts, resolution and actual proof separately.
- Airtable: Books, Characters, Spreads, Audit Findings, Revisions, Approvals, Canon Rules. An indexed approval record is only populated using direct author evidence, revision identity and Drive/GitHub references.

## Handoff / reconciliation
Before editing any existing spread, inspect the newest Drive candidates, GitHub manifest and historical audits. Populate Airtable only with verified statuses and references; keep uncertain fields empty or labeled to reconcile. Never infer approval from a dashboard entry, filename, CI result or previous approval of another revision. For all series books preserve the same reusable QA controls and adapt book-specific construction stage rules.
