# Reproducibility

This package includes a new independent reference implementation of equations in the supplied GL-Agent v1.0 paper. It was reconstructed on **22 October 2026** from the manuscript, workbook formulas and synthetic parameters. The original executable supplement described in the manuscript was not among the supplied files.

## Run

Python **3.10 or later** is required. No third-party packages are needed for numerical calculations or workbook-cache comparisons.

```bash
python3 src/gl_agent_reference.py --out local-results --check-workbook workbooks/GL-Agent-Simulator.xlsx
```

Without `--check-workbook`, the command reproduces the independent numerical model and its tests but does not inspect the Excel file:

```bash
python3 src/gl_agent_reference.py --out local-results
```

If Matplotlib is already available, `--plots` additionally creates bounded-migration, welfare and durability figures. It is optional and has no effect on numerical verification.

The command exits with a nonzero status if a model check or requested workbook comparison fails. Output is written to the chosen directory. Use a separate directory such as `local-results/`; do not overwrite the checked-in `results/` evidence during ordinary exploration.

## Expected baseline

The reviewed run passed **30 model checks** and **39,251 workbook-value comparisons**. Comparison tolerance is `abs(actual-expected) <= 1e-7` or relative tolerance `1e-10`. The maximum observed scaled difference was `1.6968542473909438e-13`, at `ScenarioCurves!J44`, where the scaling denominator is `max(1, abs(expected))`.

The comparisons cover publication inputs, the main trajectory, six scenario trajectories and summaries, durability, stacking, bounded migration, and saved Verification statuses. The count includes inputs and statuses as well as formula caches. The workbook itself contains 39,208 formula cells; these two counts describe different populations.

| Result | Independent continuous value | Workbook grid |
| --- | ---: | ---: |
| Default welfare optimum | 1.446033874 | 1.45 |
| Default global risk minimum | 2.057115003 | 2.06 |
| High-loss smooth welfare optimum | 2.588028971 | 2.59 |
| High-loss smooth risk minimum | 5.685049918 | 5.69 |
| High-loss steep welfare optimum | 2.023920308 | 2.02 |
| High-loss steep global risk minimum | 5.781680590 | 5.78 |
| Bounded-migration risk minimum | 2.197224577 | 2.20 |
| Bounded-migration welfare optimum | Approximately 1.679110 | 1.68 |

## What the tests cover

The checks include numerical extrema, finite-difference confirmation of analytic risk derivatives, welfare accounting, zero-risk and zero-productivity corners, the exact q-only entry threshold, nesting, bounded-migration conditions, the capacity-crossing counterexample, durability crossover and zero-rate limits, stacking boundaries, refresh reset/carry-over limits, and rejection of invalid model parameters.

Additional fixed-seed checks evaluate 500 heterogeneous exponential cases, 500 heterogeneous hyperbolic cases and 500 bounded-migration sign cases. The seed is `20261022`. Extreme migration sign tests factor out a positive exponential to avoid underflow changing a nonzero mathematical sign into numerical zero.

These selected checks support agreement of implementations and the tested implications. They do not prove arbitrary code correct or test empirical validity.

## Outputs

| File | Contents |
| --- | --- |
| `parameters.json` | Synthetic default and six presets, with reconstruction provenance |
| `numerical_results.csv` | Continuous extrema, stationary points and search settings |
| `curve_results.csv` | Default plus six preset trajectories at 0.01 intervals |
| `bounded_results.csv` | Bounded-migration trajectory at 0.01 intervals |
| `verification_results.csv` | Individual results for all 30 checks |
| `verification_summary.json` | Test totals, extrema and optional workbook-comparison evidence |
| `bounded-migration.png`, `welfare.png`, `durability.png` | Optional figures from `--plots` |

`verification_summary.json` carries structured arrays for stationary points. CSV list fields are descriptive strings. The checked-in [summary](../results/verification_summary.json) and [check results](../results/verification_results.csv) record the reviewed run.

## Changed assumptions and saved caches

The publication defaults and regression expectations are intentionally frozen in `src/gl_agent_reference.py`. `parameters.json` is an output recording those assumptions, not an automatically loaded input configuration. Editing that JSON alone will not change the calculations or tests.

For a new study, change the parameter definitions and the relevant expectations together, use a new result directory, assign a new version and document the departure from the publication baseline. Do not expect a changed workbook to pass a default-specific check.

The workbook reader uses standard-library ZIP/XML parsing and reads saved numeric values. It never edits the workbook and never asks Excel to recalculate it. A workbook modified without saving refreshed caches is unsuitable for this comparison. A passing cache check is not proof that the native spreadsheet application updates correctly after every possible input edit.

The continuous optimizer scans for derivative sign changes on `[0,10]` at spacing `0.001`, then uses bisection. This resolves the supplied cases. It is not guaranteed to find tangential roots or optima outside the search interval for arbitrary new parameters.

## Source identity and provenance

The original source files were renamed for portable repository paths. Their original SHA-256 identities were:

| Original source | SHA-256 |
| --- | --- |
| `paper/GL-Agent-Paper.docx` | `2ea7c5aac5a03345edb46e8cad93ebba970dbebadf7bc9fb5f4b784ac58d2a0d` |
| `workbooks/GL-Agent-Simulator.xlsx` | `a6505a6ef47b5c25f561c9550a1ba6ba2614bd149e1a1bf3cfc08bf510cd5dbd` |

The public copies were metadata-cleaned on 27 October 2026. Their current identities are:

| Public repository file | SHA-256 |
| --- | --- |
| `paper/GL-Agent-Paper.docx` | `f20669b44e26f03c0bc0bef94799475d725920e9a9ab51043dcfe8dc86f1678d` |
| `workbooks/GL-Agent-Simulator.xlsx` | `b957da960ee9940291728e5d3a7045a5af510dd8705393709656870452f18f9e` |

Document properties and absolute local paths were removed and the Public sensitivity labels were retained. Main document text, all three media files, simulator formulas and saved cell values match the original sources. The manuscript header and page-number footers were restored after Office cleanup removed them. Original hashes remain recorded for provenance in `validation/manifest.json`.

The manuscript describes an earlier supplement with 24 checks and 37,048 comparisons. This reconstructed package has a different implementation and coverage. Its results must be identified separately. Checksums establish file identity, not scientific validity. The earlier supplement DOI `10.5281/zenodo.22656510` was confirmed on 26 October 2026; its listed files differ from this package. No DOI is assigned to this reconstructed release. Use a new deposit version for a superseding artifact set or cite the earlier DOI only as related material.
