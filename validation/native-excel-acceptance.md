# Native Microsoft Excel acceptance

Status: **PENDING**. No native Microsoft Excel acceptance has been recorded for GL-Agent.

Package: `0.1.0-review.1`. Sources: manuscript v1.0 and accompanying simulator. This record was prepared on 2026-10-26; it is an acceptance template, not evidence that the checks have occurred.

## Environment and artifact identity

- Excel edition and full build:
- Operating system and version:
- Reviewer:
- Test date:
- Working-copy filenames:
- Working-copy SHA-256 hashes, if different from the manifest:
- Other applications used for secondary rendering, if any:

## Required application cycle

- [ ] Open a disposable working copy in the intended desktop Microsoft Excel build.
- [ ] Confirm automatic calculation and exercise the intended input controls.
- [ ] Force a full recalculation and inspect relevant outputs for errors or stale values.
- [ ] Save, close, and reopen the file; repeat the affected checks against the reopened file.
- [ ] Confirm formulas, validations, tables, conditional formatting, navigation, protection, charts, and print settings survived as intended.
- [ ] Inspect the intended report/print views rather than inferring them from the interactive display.

## Project-specific acceptance cases

- [ ] With unchanged defaults, verify workbook grid optima 1.45 for welfare and 2.06 for global risk.
- [ ] Verify the high-loss steep preset reports 2.02 and 5.78, and exercise zero-risk and zero-productivity corners.
- [ ] After the input-validation repair, confirm blank, text, negative, and out-of-domain inputs are rejected or clearly flagged.
- [ ] Review all corrected cell Notes, the opening Dashboard view, chart legends, axis labels, and the secondary-renderer appearance.
- [ ] Confirm the workbook license/deposit wording and any DOI reference identify the actual artifact set being released.

## Results and evidence

Record each result, unexpected behavior, screenshot/PDF evidence location, and follow-up issue here. Keep real organizational assessments and personal data out of the public repository.

## Completion

- [ ] All required cases pass. Any exception remains recorded as a release blocker and `stable_release_ready` remains false.
- [ ] The reviewer and test date are recorded above.
- [ ] `validation/release-status.json` has been updated only after reviewing this evidence.
- [ ] Source hashes, citation/version metadata, and the change log have been updated if an artifact intentionally changed.
