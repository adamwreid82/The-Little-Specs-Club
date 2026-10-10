# Pages 11–12 REV26: restore locked helmet applications — 2026-10-10

PENDING AUTHOR SPREAD REVIEW. Approved: false. Overall all-pass: false. No archive moves.

Adam reconfirmed: “I meant for that to be locked moving forward”.
Correction instruction: “Fix the current spread”.

Version B: https://drive.google.com/file/d/1NVi-26CR-w3qJPI3ZUaNooOBxJDbhJz4/view?usp=drivesdk
Matching art-only A: https://drive.google.com/file/d/10vr1CAtinJzehjEBR869wv87EZ-WyeeE/view?usp=drivesdk
Base: REV25. REV25 and all earlier artwork/audits remain preserved.

## Controlling lock

The Oct 5 six-character LS size/position lock applies to all subsequent spreads and future books. No new logo standard or approval is requested. CANON/approvals/LS_HELMET_APPLICATION_APPROVAL_2026-10-05.md and CANON/character-rules.yaml record Adam's Oct 10 prospective-scope confirmation without changing the locked reference or graphic.

Approved application reference: Drive 1WV1NJ9hH9PE4nNgnKk9DbY1HR9-KEtY2, SHA256 2b9f89198ee798afe02f116a2e09eb6695cf2db5cdbe0b40cb682ca04fcb576b.
Exact LS artwork source: Drive 1T2tCGf79Efg-xpuYWBAi04-d7XG99sP_, SHA256 96a47ac122989b3527e3fc5f8aa58544fd438799c2c4d7041cca4ef40de34a42.
Brooks's employer-logo baseline remains the separate Oct 1 approval.

## Correction and reference comparison

REV25's generic “fitted within shell” check was insufficient to establish the approved application relationship. This revision uses the locked reference applications directly. Four comparable poses use manually identified crown and brim landmarks to transfer the approved badge bounding region to the scene. The exact source graphic is uniformly scaled first, then projected to that approved region, with the locked narrow white outer contrast outline. Reference landmark coordinates, matrices and badge regions are recorded in REV26_REFERENCE_TRANSFER.json. These are production measurements for this candidate, not a newly approved numeric tolerance or physical size.

Ben's much stronger opposite-facing profile uses a narrow nose-facing front-panel projection rather than mirroring the reference or displaying a badge on the side. Leo's front panel faces away; his front badge remains naturally hidden.

| Person | Result | Visible scope |
|---|---|---|
| Ben | PASS manual visible application | Exact artwork, front-panel projection facing his nose, raised above brim; no mirror |
| Leo | PASS visibility rule | No front badge added to rear/side shell |
| Vinny | PASS manual visible application | Locked proportional fit and projected tilt transferred from reference; narrow outer outline |
| Steph | PASS manual visible application | Reference crown/brim relationship transferred to gray front panel |
| Maya | PASS manual visible application | Moved from low/sideward position to locked reference front-panel region; brim clearance restored |
| Mrs. Harper | PASS manual visible application | Raised and moved inward to reference front-panel region; proportional fit retained |
| Ms. Rivera | PASS preservation | Employer mark and project sticker unchanged; no LS substitution |
| Mr. Brooks | PASS preservation | Employer mark unchanged; separate approval retained |

The manual visible application passes do not establish physical decal inches, rigorous 3D rectification or approval of the spread. The existing design lock remains approved; this candidate remains unapproved.

## Preservation and output

PASS zero changed pixels outside recorded small old/new logo footprints. PASS zero changed lettering-region pixels. PASS A plus original transparent text layer equals B with zero changed channels. PASS both PNGs fully decoded, 5100 × 2550 at 300 dpi. Exact source/reference hashes matched the registered authority. The five helmet crops and complete spread were inspected for shell-edge crossing, brim clearance, ghosting, duplicate marks, floaters and patch seams.

Faces, eyes, hair, glasses, character bodies, clothing, hands, shoes, table, site and employer logos remain original REV25 pixels outside the helmet marks. Vinny was not regenerated again. Lettering/fonts unchanged. Source sheets, profiles and approved spreads unchanged.

## Remaining review items

Adam's whole-spread review and Vinny full-likeness feedback remain pending. Exact barefoot heights, held-sticker comparative/physical scale, hidden details, full site geometry, native print/physical proof and matching current bleed exports remain unverified. Badge physical dimensions have not been established by the lock; do not invent inches or call that a new design failure. Historical PDFs are not REV26 proofs.

Nothing approved by “Fix the current spread”. No archive moves. Await feedback after showing the complete candidate.

## Method and reproducibility

Built-in imagegen supplies a blank-shell clean plate removing only the five current LS marks in the eight-panel crop sheet. Prompt: remove the five LS badges; restore surrounding shell light/color/curvature; preserve all ridges/brims/helmet edges, faces, hair, eyewear, two employer marks, Rivera's round sticker and Leo's plain rear/side helmet; no new marks or rearrangement. Sharp transfers only small recorded old-logo footprints, inserts exact source graphics using the reference projection and reuses original lettering. No full scene regeneration or external API fallback.

Production script: production/finish_rev26.cjs.
Reference measurements: qa/REV26_REFERENCE_TRANSFER_2026-10-10.json.
Pixel/hash checks: qa/REV26_VERIFICATION_2026-10-10.json.
Prospective regression record: qa/REV26_LOCKED_HELMET_CONTINUITY_2026-10-10.yaml.
Drive evidence package preserves the clean plate, reference crops, exact graphic, text layer, script, measurements, previews and audit. Base artwork is retained separately in Drive. Full Drive readback hash/decode results are in the verification record.

