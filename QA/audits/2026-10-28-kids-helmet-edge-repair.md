# Vinny and Maya helmet-edge repair, 2026-10-28

Adam reported: "Maya and Vinny still have hair and helmet bled" after receiving Vinny PPE R13 and Maya PPE R6. Treat those versions as failed for this reported defect. The preceding audit's observation that no obvious shell penetration was seen did not adequately detect the visible dark rim smears and shell contamination. This audit supersedes that observation for the identified regions.

## New candidates

| Candidate | Drive ID | SHA-256 | Bytes |
| --- | --- | --- | ---: |
| Vinny_PPE_8_Angles_REVIEW_R14.png | 1eqKPQs4Oi4QkjNi79w3IQg0Lq3OIiZo8 | d3903640a95d570848a46a940a5b079c87a269082f873690bda223028826d1db | 3764411 |
| Maya_PPE_8_Angles_REVIEW_R7.png | 1rMA-hXpMNguE8j0eexITY4vGoCY9mrHA | 514b4cfb128a417c40b51747a927d49d1a99dcd46da990e3af1aa1d4d3eb58af | 3792724 |

Both are 3072 x 2048 PNGs and remain unapproved REVIEW candidates. Earlier versions remain intact. Steph R12 is unchanged.

## Actual findings and repairs

- Vinny front and front-right: dark, blurred rectangular contamination interrupted the green outer rim directly beneath the LS badge. Rebuilt the affected solid green shell/rim surface so the lower edge reads continuously over the original hair.
- Vinny front-left: cleaned local shell/rim transitions around the existing badge. Inspected the crown and repaired a ghost fragment into a connected green ridge. Removed a pale ghost near the right-profile outline where supported by the blank-shell source.
- Maya front: gray/green discoloration beneath the front-left sticker contaminated the yellow shell and rim. Restored yellow shell shading and a continuous yellow lower edge.
- Maya front-right, left profile and front-left: cleaned local decal-adjacent shell/brim transitions and inspected separation from the original curls.
- Inspected all eight head views for each character, the magnified before/after crops and full exported sheets. The identified rim smears and discolored patch edges are corrected in these candidates. This focused inspection is not an assertion that every possible detail has author approval.

## Preservation and method

Used the established approved PNG/profile pairs from the preceding source comparison: Vinny PNG 1m-mxpb7Fpu04jWj5sYVJTHxvXXPySuSa with profile 1vG_CJ45X87ZsYlNr-Rq2VJiuRHaTtw4S; Maya PNG 1RZtZjt-3eX0iFFcKw1ZxtnlXj3pkoerU with profile 1nERipp0Qz3AUFuYFkJ25rOuM0UfIGnV3. The source pairs and locked branding assets are unchanged. AGENTS.md was reread and the latest Drive candidates, active repair ledger and GitHub sheet ledger were reconciled before editing.

Built-in imagegen produced two cropped blank-shell repair guides. Only bounded shell/rim regions were composed into the actual sheets. No generated whole face or character was substituted. The shell boundary, rather than an indiscriminate original-hair mask, controls the repaired rim so a dark defect is not accidentally protected as hair. The crown guide initially left a small white slit under its raised lip; that slit was closed with adjacent green shell pixels before delivery.

Opaque existing LS and project-sticker pixels were preserved at their exact positions. Transparent edge pixels use the same locked asset projection to blend onto the repaired shell. No branding was relocated, resized or regenerated. Original hair beneath the rim, eyes, faces, glasses, ears, clothing, vest emblems and all lower-body artwork were preserved outside the bounded repairs. Footer revisions changed only to R14 and R7.

Pixel comparison recorded zero changes outside the declared head-crop repair footprints and footer. All eight sampled lower-face bands for each character are unchanged. A separate skin-pixel check in visible-face windows returned zero changes. These are bounded preservation checks, not a complete automated likeness comparison. Exact results are recorded in verification.json.

PNG decoding succeeded. Repository ledger and supplied local raw-byte checks passed with no errors. Their visual-review status remains UNVERIFIED because the scripts do not perform image recognition or grant author approval. Drive metadata sizes were checked against the exports.

## Remaining limits

Exact badge and sticker projection across views, independent relative physical-height relationships and naturally hidden details remain unverified. No approved source was overwritten and no new character design was approved. The current whole-sheet angle records remain UNVERIFIED for overall certification; the two prior candidates are rejected for the reported bleed. The earlier nine vest-panel repairs and Steph freckle work are preserved.

Review branch: review/kids-ppe-repair-2026-10-27. Draft PR: https://github.com/adamwreid82/The-Little-Specs-Club/pull/4. No automatic merge.
