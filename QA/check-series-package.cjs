#!/usr/bin/env node
/** Static source-reference and series-template preflight.
 * Does NOT establish visual likeness, file-byte hashes, or print readiness.
 * Run from the repository root: node QA/check-series-package.cjs
 */
const fs = require("fs");
const manifest = JSON.parse(fs.readFileSync("QA/SERIES_REFERENCE_PACKAGE_MANIFEST_2026-10-12.json","utf8"));
const template = fs.readFileSync("CANON/series-production-template.yaml","utf8");
const problems = [];
if (!Array.isArray(manifest.characters) || manifest.characters.length !== 27) problems.push("Expected 27 canonical character references");
const names = new Set();
for (const c of manifest.characters || []) {
 if (!c.name || names.has(c.name)) problems.push("Missing or duplicate character name: " + c.name);
 names.add(c.name);
 for (const key of ["image","profile","image_sha256","profile_sha256"])
  if (!c[key]) problems.push(c.name + " missing " + key);
 for (const key of ["image_sha256","profile_sha256"])
  if (c[key] && !/^[0-9a-f]{64}$/.test(c[key])) problems.push(c.name + " invalid "+key);
}
for (const token of ['font: "Roboto"',"font_weight: 400","final_size_pt: 18","width_px: 5100","height_px: 2550"]) {
 if (!template.includes(token)) problems.push("Template missing: "+token);
}
for (const [key,item] of Object.entries(manifest.graphics || {})) {
 if(typeof item === "object" && item.drive_id && !/^[0-9a-f]{64}$/.test(item.sha256 || "")) problems.push(key+" missing valid hash");
}
if (problems.length) { console.error("STATIC PREFLIGHT FAILED:\n"+problems.join("\n")); process.exit(1); }
console.log("STATIC PREFLIGHT PASSED: "+names.size+" indexed people; Roboto 400/18pt; 5100x2550; graphic hash formats.");
console.log("VISUAL INSPECTION, LIVE DRIVE HASH CHECK, FONT EMBEDDING, MANUSCRIPT MATCH, AND AUTHOR APPROVAL STILL REQUIRED.");
