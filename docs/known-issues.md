# Known issues

This reviewed prerelease preserves the source manuscript and workbook. Default numerical calculations reproduce, but the following issues remain in that archived workbook. These findings should remain visible until a corrected workbook passes the relevant checks.

| Priority | Issue | Effect | Workaround or next change |
| --- | --- | --- | --- |
| High | `Dashboard!I15` accepts a blank or text campaign rate as VALID. | Missing exposure can become zero; text can produce `#VALUE!` while health remains VALID. | Enter numeric values in every required input. Add numeric completeness checks and validation in the next workbook. |
| High | Legacy cell Notes contradict the revised paper. | Hover guidance overstates calibration, misstates units and confuses local direction with global optima. | Follow the paper and this repository's methodology. Replace the old Notes before release. |
| High | Stray drawing objects cover the Dashboard input area in two tested non-Excel renderers. | The opening view can be unusable in previews and LibreOffice. | Use the independent Python workflow; remove empty legacy shapes and verify native Excel plus a secondary renderer. |
| Medium | Welfare chart has `varyColors=1`; LibreOffice produces a 1,001-item legend. | The curve disappears under its legend in that renderer. | Rebuild the single-series chart with sparse axis ticks and explicit series formatting. |
| Medium | Probability/positivity constraints are not enforced by data validation. | Impossible inputs can produce plausible-looking outputs on subsidiary sheets. | Respect the domains in methodology; add local numeric/domain checks. |
| Medium | `Dashboard!C24` Note promises an absent dropdown. | Guidance describes an interaction the file does not provide. | Type a number from zero to ten. |
| Medium | `Notes!C22` says licence/DOI are undecided; paper grants licences and mentions a DOI. | Distribution metadata is inconsistent. | Follow the repository's file-level licences. Verify any DOI and version correspondence before assigning it to this package. |
| Low | High-loss input columns use different number formats. | Probabilities and amounts are less consistent to read. | Harmonize `Examples!G:H` with equivalent C:F rows. |

## Cell-Note errata

The full audit lists each affected cell. The most consequential corrections are:

- `Dashboard!C31`: residual risk equals `k/gamma` only at an interior q-only optimum. At the corner it is `R0`.
- `Dashboard!C32`: the global welfare optimum does not make the derivative negative everywhere to its right. The supplied steep preset has positive marginal welfare at intensity 4.
- `Dashboard!C33`: compare a point with the global risk minimum separately from the point's local derivative.
- `Dashboard!C19`: two local maxima alone do not demonstrate that greedy portfolio choice missed a better bundle.
- `Dashboard!C38`: full-model optimal burden need not be below q-only optimal burden.
- `Durability!C7` and `C9`: calendar decay rates are per year, not per adaptation cycle.
- `Dashboard!C9:C18` and `Stacking!C6:C7`: numerical “typical” or “realistic” anchors in old Notes are not calibrated evidence.

## Verification boundaries

The new Python implementation is independently reconstructed. It does not claim to be the original supplementary code mentioned in the paper. The archived `Verification` sheet contains fixed default expectations and will legitimately change when model inputs change.

The audit verified saved workbook values and independently computed model results. An artifact-engine attempt to change inputs did not reliably refresh shared grid dependencies, so it is not treated as a successful Excel recalculation test. Native LibreOffice rendered the baseline. Microsoft Excel edit/recalculate/save/reopen testing remains a release check.

## Publication metadata check

A follow-up inspection on 26 October 2026 found a Microsoft Information Protection label record in both source Office files, the manuscript and the workbook. Confirm that this metadata and the intentional author contact details are appropriate for public distribution. The label/site identifiers are not reproduced in the [publication-metadata record](../validation/publication-metadata.json). Their presence alone does not establish confidentiality. If public release copies are changed, update the source hashes and rerun validation.

See [issues to open](issues-to-open.md) for concrete fixes and acceptance criteria, and [the review](review.md) for evidence.
