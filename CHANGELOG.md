# Changelog

## Public-copy metadata cleanup — 2026-10-27

- Retained the visible Public sensitivity labels and removed document properties and absolute local paths from the public manuscript and simulator. `lastModifiedBy` is empty in both files.
- Restored the manuscript header and page-number footers after Office cleanup removed them. Main document text and all three media files are unchanged. DOCX XSD and semantic checks passed; the 29-page visual review found no blank or clipped pages and no content loss.
- Verified that all 10 simulator worksheets, 39,208 formulas and saved cell values match the original source. All 30 independent model checks and 39,251 workbook-value comparisons pass.
- New manuscript SHA-256: `f20669b44e26f03c0bc0bef94799475d725920e9a9ab51043dcfe8dc86f1678d`. New simulator SHA-256: `b957da960ee9940291728e5d3a7045a5af510dd8705393709656870452f18f9e`.
- Updated the source manifest, publication-metadata record, release status, README, publishing guide, known issues, review, reproducibility guide, validation guide and issue drafts.

Formal native Excel acceptance and the documented workbook input, Note, drawing and chart issues remain open. The earlier Zenodo DOI remains a related earlier deposit and is not assigned to this reconstructed package.

## Web-publication preparation — 2026-10-26

Repository-only update before the initial GitHub import. The unpublished package version and functional-review baseline remain unchanged.

- Replaced the command-line import guide with browser-only repository, upload, Actions, visibility, and release instructions.
- Expanded CI to compare all generated numerical evidence. Verified that the earlier Zenodo DOI resolves and documented its distinct artifact inventory. Included the full CC BY 4.0 legal text alongside the project allocation notice.
- Added an Office publication-metadata record, a native Excel acceptance template, and explicit evidence checks in the stable-release gate.
- Added the author ORCID to the primary citation metadata and clarified post-import repository status documentation.

No source workbook or manuscript bytes were changed. This preparation does not establish native Microsoft Excel acceptance, resolve licensing decisions, or close functional blockers.

## 0.1.0-review.1 — 2026-10-22

Initial repository preparation and independent review package.

- Included Supplied manuscript v1.0, 7 September 2026; accompanying simulator with original source bytes preserved.
- Added project orientation, methodology, quick start and cell-specific known issues.
- Added recorded verification evidence and reproducible read-only checks.
- Added a project mascot, citation metadata and contribution/issue templates.
- Added a source checksum manifest and package-integrity workflow.

This package version describes the repository scaffolding and review. It does not increment the supplied workbook versions. Proposed corrections have not been applied to the source workbooks. See [release status](validation/release-status.json) and the [review](docs/review.md).
