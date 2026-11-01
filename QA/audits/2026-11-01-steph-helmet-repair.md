# Steph PPE R13: helmet alignment and sticker contour

Status: REVIEW CANDIDATE, pending Adam Reid's approval. Date: 2026-11-01.

Adam reported: “Stephs logo on her hard hat is not centered correctly and the job sticker is not going along the conture of the hardhat”. This is a correction request, not approval. R12 fails these reported checks; previous review statements do not override this feedback.

## Exact files

| Version | Drive ID | SHA-256 |
| --- | --- | --- |
| R12, retained | 1lt05e84WTpywOsGdEj_W4PXxiofSIWE7 | 56202643bb7ef262613ca676c1fa620307649f728762262dfc569867afb00619 |
| R13, new review | 1RzQn7GGlNnUYR8K6C-zxvM9qPSlvUWTO | 78d19a8adf859dbcc6a3f9e07fcb18c8ff5046cfcd8ca775fba12c759cf49a30 |

R13: `Steph_PPE_8_Angles_REVIEW_R13.png`, 3072 × 2048 pixels, 3,596,137 bytes.

Candidate: https://drive.google.com/file/d/1RzQn7GGlNnUYR8K6C-zxvM9qPSlvUWTO/view

Before/after helmet proof: https://drive.google.com/file/d/136ZHCbdmIaipVgW8vsE0Bs1V3VWbsexd/view

## Controlling references

- Steph paired approved PNG: `1gF-pOjdltQVujd5NyCcX-Brh-EI0vQ9j`, SHA-256 `0338ba00d3cc122c7e1baecca56b577f51b54ea4a8f24ed2b7bbbc29685b934a`.
- Steph profile: `1hzABye97w5caJMYh90wvyGXrd17gXCBS`. Read its current text; front-right project sticker, light-gray hard hat, and own character details govern.
- October 24 kids helmet placement lock: `1B0kSrRIjoMRs4z3LdJTPLHgMu6XKi8M-` and JSON `1U0C5qL3S2PthHHznZ91Awn6RjMtcrGML`. Exact author statement: “Ben’s hard hat logo is good, lets use its location for the other kids”.
- Ben PPE R5 visual master: `1jfdO92dW-tXMyhoWgmb2AxhAKWqqlCFx`, SHA-256 `e1754499e1bfc3acc6054df9f57b4417eda1db64be4c34fb1cb7712390c4746a`. Front panel, proportions and brim clearance control; page coordinates do not transfer directly to Steph.
- Exact LS asset: `1T2tCGf79Efg-xpuYWBAi04-d7XG99sP_`, SHA-256 `96a47ac122989b3527e3fc5f8aa58544fd438799c2c4d7041cca4ef40de34a42`.
- Exact project sticker: `1-nHpjvk0OBnVLBpLPjtPCTpyIde4nUAz`, SHA-256 `adcfdcdbe9c533268012e45d5c2662cf10c8b5ef684eb389528cf7107a4975ba`.

## Repairs and visual inspection

Used the built-in image-editing tool for a temporary blank-helmet background. Composited only inside the former decal footprints, then projected the original locked PNG assets onto the shell. No branding was generated, mirrored or substituted. Local surface projections are recorded in `verification.json`; these coordinates are specific to Steph's R12/R13 sheet.

| View | Targeted correction and observation |
| --- | --- |
| Front | LS badge moved into the center of the molded front panel, with Ben-reference proportional fit and visible brim clearance. Job sticker follows the side shell's taper and local slope. |
| Front-right | Badge centered within the visible front panel. Job sticker retains the wearer-right anchor beside it and follows the shallow curved surface. |
| Right profile | Existing job sticker reprojected along the local shell/brim slope. No new LS profile fragment invented. |
| Front-left | Badge centered within the front panel. Far-side job sticker remains narrow and follows the shell's taper. |
| Rear-right, back, rear-left, left profile | Pixels unchanged; no new rear badge or opposite-side sticker added. |

Inspected the full export, all eight helmet crops, a before/after comparison, and enlarged front detail. No visible old-logo ghosts, rectangular seams or new rim/hair overlap were found in these repaired footprints. Original face, subtle freckles, eyes, glasses, red hair, helmet silhouette, brim, hoodie, vest emblems, trousers and shoes are unchanged. Ben, Leo, Vinny and Maya artwork was not edited. Vinny R15 and Maya R8 approval records remain unchanged.

Regression checks for future edits: inspect front-panel centering and brim clearance at every visible angle; a sticker's baseline, taper and compression must follow the local helmet shell, not just a flat page rotation. Preserve the wearer-relative anchor and exact asset. Inspect the entire removed-logo footprint for remnants. These implement existing canon and the current correction request, not a new design lock.

## Verification and limits

Pixel comparison: 18,825 changed pixels including the revision footer; **zero changed pixels outside the bounded old/new helmet decal footprints and footer**. Locked local artwork/source hashes matched their recorded authority. The uploaded candidate metadata confirms filename, destination and exact byte count.

Repository ledger and local raw-image SHA-256 checks passed using `check_reference_sheets.py --asset-files ... --require-all-assets --json`. The check validates references and supplied bytes, not visual correctness. Current registered files are Vinny R15, Maya R8 and Steph R13.

This is a visual fit to a painted helmet, not a calibrated 3D model. Mathematical cross-view surface registration, hidden/profile decal extents, unresolved full-canon checks, physical heights and print readiness remain UNVERIFIED. All eight Steph ledger view states remain UNVERIFIED rather than claiming a whole-view PASS from this targeted repair. Author approval remains null.

Earlier candidates and source masters are retained. Steph R13 is not archived or marked approved. GitHub work remains on draft PR 4, branch `review/kids-ppe-repair-2026-10-27`; no merge.

## Image-edit prompt and provenance

Mode: built-in image generation/editing tool, used only for local blank-shell texture. Exact final branding was composited from the two locked PNGs.

Prompt: “Use case: precise-object-edit. This exact 1600x800 image is a technical cleanup atlas of the SAME red-haired child in eight camera views, 4 columns by 2 rows. Edit target image 1. REMOVE ONLY the blue/yellow LS logo and tiny circular job sticker printed on the light gray HARD HATS in top-left, top-second, top-third, bottom-right cells. Fill their footprints with seamless existing light gray helmet plastic, preserving curvature, highlights and molded vertical ribs. No new logos, no decals. Keep ALL grid positions, crop sizes, helmet silhouette, helmet brim, molded ribs outside the former decal footprints, face, eyes, glasses, freckles, hair, hoodie, vest and existing circular VEST logos completely unchanged. This is only a temporary clean helmet background for later compositing the exact locked artwork. Preserve 4x2 layout and original canvas aspect; do not rearrange or enlarge any face or helmet.”

The generated atlas itself is not the candidate; all changes outside the bounded decal footprints were discarded during composition.
