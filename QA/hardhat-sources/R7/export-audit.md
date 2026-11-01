# Hardhat Sources R7 export audit

2026-11-01. Status: PENDING AUTHOR APPROVAL.

Adam requested a new review revision from all current SVG files, then specified R7 because R6 already exists. His final source selection was: “Hardhat Sources R5 - Logo and Placement Corrections - REVIEW 2026-10-21\Editable Sources and Placement Records”.

Source folder: https://drive.google.com/drive/folders/1a_M9FhDZNTlgbJxcUw2CRvp7Sai41_ov

New R7 folder: https://drive.google.com/drive/folders/17J0cREVTUkPV2TlcFZhH3zht5igIaaoU

Review PDF: https://drive.google.com/file/d/1Ms6pJt5DToOiDZRN4NO4riBb2ZB7utAQ/view

PDF SHA-256: `668facf3d3ddc4b5dc21a09e092e71552f7fe4129ea13c2f356c5646254014f0`; 59,028,791 bytes; 27 pages.

## Scope and sources

All 26 SVGs in the selected folder were included, regardless of modification date. Twenty-three files show November 1 updates; Maya, Leo and Mrs. Harper retain October 21 timestamps. Each source ID, modified time, filename, byte count and SHA-256 is recorded in the R7 register. Exact original source bytes are retained in the review package.

The existing R6 set is a separate 3D-model review. Its README and folder were checked to avoid a revision conflict. R7 follows Adam's selected edited R5 SVGs; no R6 geometry or older PNG preview was substituted.

## Export behavior

Inkscape directly rendered each edited SVG into a PNG and a PDF page. The combined PDF contains an index and 26 character pages with bookmarks. No image generation, decal repositioning, shell retouching, asset substitution or new 3D fitting was performed.

The only authored SVG changes are the two review/footer text elements, which now identify R7 and pending approval. The full XML tree with text elements removed was compared before and after and is identical for all 26 sheets. This preserves shell imagery, clipping, embedded artwork, transforms, sticker locations, logo scale and colors.

R7 placement records snapshot the actual SVG elements and their nested transforms. Old R5 JSON placement coordinates were not used to rebuild the artwork. The snapshot's `embedded_asset_sha256` field hashes the complete embedded data-URI representation; it is not a claim that the underlying PNG bytes have that hash. The unchanged non-text SVG tree is the preservation check.

## Checks completed

- All 26 source and derived SVGs parse; all internal referenced IDs resolve; assets are embedded.
- Twenty-six PNGs decode and retain their source canvas dimensions.
- Combined PDF has 27 pages and 27 bookmarks, in the documented index order.
- All 26 character pages contain an R7 REVIEW label.
- All final PDF pages were rasterized and inspected in five contact sheets. The cover and a full character page were also inspected at larger size. All four views are visible on every character sheet; no missing graphics or new export clipping was found.
- Source and output SHA-256 values are recorded. Original source SVGs and earlier R5/R6 review files were not overwritten.

Result: PASS for export completeness and preservation of authored SVG artwork. This does not certify canon, logo placement, surface curvature, physical dimensions, mathematical 3D consistency or print readiness. Those design judgments remain for Adam's review of R7.

The existing full-character PPE sheets and their approval records are unchanged. R7 is a helmet-source review set, and no author approval has been inferred from successful export checks.
