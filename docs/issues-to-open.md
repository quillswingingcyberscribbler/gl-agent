# Issues to open

These are prepared issue descriptions for the next GL-Agent workbook release. Copy the items you want to track into GitHub Issues; the issue tracker becomes authoritative once an item has been created there.

## Reject incomplete and nonnumeric model inputs

**Problem:** `Dashboard!I15` reports VALID when `C9` is blank or text. There are no worksheet data-validation rules. Subsidiary sheet domain checks also lack numeric completeness.

**Change:** Add `COUNT(C9:C21)=13` and `ISNUMBER(C24)` to the existing dashboard health conditions. Handle errors in the diagnostic as CHECK INPUTS. Add validation for nonnegative quantities, probabilities from zero to one, positive fatigue smoothness, positive all-in burden and dial bounds. Apply equivalent local completeness/domain checks to Examples, Durability, Stacking and BoundedMigration.

**Acceptance:** Test missing, text, zero, negative, probability-over-one and valid inputs. Missing data must not appear as healthy zero exposure. Invalid input health must remain visible. Valid zero-risk and zero-productivity scenarios must preserve their documented corner behaviour.

## Replace legacy cell Notes with the revised model explanations

**Problem:** Old hover Notes contain unsupported calibration ranges, wrong durability time units, unconditional interior formulas and misleading claims about local versus global optima.

**Change:** Align the Notes with the paper and [methodology](methodology.md). Replace claims of typical attack success, review capacity, dependence and control-type decay with measurement definitions. Correct `C31`, `C32`, `C33`, `C38`, the `C19` bundle claim and the absent-dropdown instruction. Preserve the distinction between detection and loss-weighted prevention.

**Acceptance:** Review the stored Excel Notes as well as the visible cells. The steep preset must no longer contradict the guidance. Annual decay labels must agree with their Notes. No unsourced “realistic” calibration range should remain.

## Repair Dashboard drawings and curve presentation

**Problem:** Empty legacy drawing objects cover the title/input area in artifact rendering and LibreOffice. The welfare chart becomes a giant legend; the risk chart has excessively dense axes/gridlines.

**Change:** Remove stray `Text Box 24` and empty `AutoShape 24` objects while preserving live chart data. Rebuild the welfare and risk charts with explicit series, ordinary series colouring, readable titles and sparse numeric ticks. Harmonize high-loss input number formats.

**Acceptance:** Inspect the opening view and charts in native Excel and a secondary renderer. No drawing should cover input cells. The welfare chart must display the actual curve and one legend entry. Editing the default and steep preset inputs must update the curves and grid extrema.

## Complete a native Excel scenario regression

**Problem:** The audit established independent model agreement and saved-value agreement. The available artifact engine did not reliably refresh shared grid dependencies after input edits; native Microsoft Excel's interaction cycle was not tested.

**Change:** Open the revised workbook in supported desktop Excel, set automatic calculation, change scenarios, force recalculation, save, close and reopen. Record the Excel version and the observed results.

**Acceptance:** The unchanged default returns grid optima 1.45/2.06. The high-loss steep preset returns 2.02/5.78. Zero-risk and zero-productivity corners behave as specified. Invalid inputs are rejected or clearly flagged. Saved results compare with the corresponding independent parameters and expectations.

## Reconcile release metadata and reproducibility provenance

**Problem:** The workbook's older licence/deposit wording conflicts with the manuscript and the confirmed artifact set. The source paper names an original supplement that was not supplied; this repository contains a separately reconstructed implementation.

**Change:** Preserve MIT for workbook/code and CC BY 4.0 for manuscript/docs/figures/parameters/results. Update the workbook deposit wording. The earlier supplement DOI resolves, but its file inventory differs from this package. Create a new deposit version for a superseding release or cite the earlier DOI only as related material. Keep the reconstruction provenance and fresh verification counts explicit. The publication-metadata cleanup is complete: Public classifications were retained, document properties and absolute local paths were removed, and the manuscript header and page-number footers were restored.

**Acceptance:** Citation, licences, README, workbook Notes and any revised manuscript describe the same files and release. The earlier DOI is not assigned to the different reconstructed artifact set. `validation/manifest.json` and `validation/publication-metadata.json` identify the current public copies and their previous source hashes.
