# Pages 11–12 REV25: helmet-logo placement correction — 2026-10-10

PENDING AUTHOR REVIEW. Approved: false. Overall all-pass: false. No archive moves.

Adam: “Hard hat logos are not in the correct location”.

Current Version B: https://drive.google.com/file/d/1TjCblgPjDtqp0Ti_RtQQ9yF5JAiKc0mH/view?usp=drivesdk
Matching art-only A draft: https://drive.google.com/file/d/1x3Py1ki2CNW2jAzDhGowBW_O4NwLCkMU/view?usp=drivesdk
Base: REV24, retained in Drive with its audit and production record. All earlier candidates remain preserved.

## Scope and controlling authority

The Oct 5 hard_hat_badge_application_lock in CANON/character-rules.yaml controls the six LS applications. Its approved reference is Drive 1WV1NJ9hH9PE4nNgnKk9DbY1HR9-KEtY2, SHA256 2b9f89198ee798afe02f116a2e09eb6695cf2db5cdbe0b40cb682ca04fcb576b. Source artwork is Drive 1T2tCGf79Efg-xpuYWBAi04-d7XG99sP_, SHA256 96a47ac122989b3527e3fc5f8aa58544fd438799c2c4d7041cca4ef40de34a42. Size and position approval for the reference does not approve this spread.

Five visible LS badges were removed locally and replaced with the exact approved graphic. Placement was adapted to the visible front panel, pose, nose direction and brim. Vinny's badge was raised and shifted toward his facial centerline; the other visible badges were fitted within their front panels. Intrinsic source proportions are retained before pose projection; the prior Vinny insert had been stretched before projection. Employer logos retain their independent source/baseline and unchanged pixels. Leo is seen from the rear/side; no camera-facing LS mark was added.

## Helmet-by-helmet review

| Person | Result | Scope |
|---|---|---|
| Ben | Corrected; author placement review pending | Exact LS asset, narrow front-panel projection, within visible shell |
| Leo | PASS preserved visibility rule | Front badge naturally hidden; no rear badge added |
| Vinny | Corrected; author placement review pending | Exact asset, raised within front panel, original intrinsic proportions before projection |
| Steph | Corrected; author placement review pending | Exact LS asset fitted inside gray front panel |
| Maya | Corrected; author placement review pending | Exact LS asset fitted inside yellow front panel with brim clearance |
| Mrs. Harper | Corrected; author placement review pending | Exact LS asset fitted inside white front panel |
| Ms. Rivera | PASS preservation | Employer logo and project sticker unchanged; not replaced with LS |
| Mr. Brooks | PASS preservation | Employer logo unchanged; separate Oct 1 baseline retained |

This is a focused application review, not a fresh complete character/site certification. No universal numeric tolerance or physical decal dimension is inferred. Exact physical scale and rigorous pose rectification remain UNVERIFIED. The visible candidate is presented for Adam's placement feedback.

## Verification

PASS exact registered LS artwork identity. PASS full PNG decode and 5100 × 2550 at 300 dpi. PASS zero changed pixels outside the recorded small logo/cleaning footprints. PASS zero changed lettering-region pixels. PASS original text layer added to A matches B with zero changed channels. Faces, hair, glasses, clothing, hands, shoes, table, site and employer-logo pixels remain unchanged. Full-size helmet crops and full-spread preview inspected for duplicate marks, ghosting, floating marks and patch edges.

An initial unsaved assembly placed some marks outside helmet edges. This failed local check was corrected before the Drive candidate was created. It was not recorded as current or approved. The final placement footprints and exact coordinates are in REV25_VERIFICATION.json.

## Remaining issues and approval

Author feedback on these applications and Vinny's regenerated full likeness remains pending. Exact barefoot heights, held-sticker comparative/physical scale, hidden details, complete site geometry, native print proof and matching current bleed exports remain unverified. Historical PDFs are not REV25 proofs. Text/fonts remain unchanged for Adam's manual wording.

No source PNG, profile, canon design, manuscript or approved spread was overwritten. REV24 and prior versions remain preserved; no Superseded moves without explicit approval.

## Method and reproducibility

Built-in imagegen produced a blank-shell clean plate for the five existing LS marks in a local eight-panel crop sheet. Prompt: remove only the five blue/yellow LS badges; restore shell color, lighting, texture and curvature; preserve helmet edges/ridges/brim, faces, hair, eyewear, two CIVIC RIDGE employer logos and Rivera's round sticker; leave Leo's blue helmet untouched; no new marks or rearrangement. Sharp transfers only small recorded cleaning footprints, composites the exact LS source with pose projection, and reuses the original text layer. No external API/model fallback.

production/finish_rev25.cjs and qa/REV25_VERIFICATION_2026-10-10.json record the assembly, hashes, coordinates and preservation checks. A source-grounded regression check requires inspection after every helmet/head repair; CI cannot supply visual or author approval. Drive readback evidence will be recorded separately.

