# GL-Agent review

Reviewed 22 October 2026. Sources: [the supplied paper](../paper/GL-Agent-Paper.docx) and [simulator](../workbooks/GL-Agent-Simulator.xlsx). Original bytes are preserved under portable repository filenames.

## Decision

Keep **GL-Agent** as the project name and use **`gl-agent`** as the repository name. The manuscript already establishes that identity. Describe it as **an Excel simulator and reproducible research model for the economics of AI-agent controls**.

The numerical core is consistent with the manuscript and reproduces correctly at the supplied inputs. The files should be described as a theoretical research release. They are not a calibrated organizational risk estimator. Public packaging needs more than a renamed workbook: the original executable supplement is absent, legacy Excel Notes contradict the revised paper, input health can report VALID for nonnumeric data, and native LibreOffice rendering exposes drawing/chart problems.

The new independent reference implementation supplied with this audit closes the missing-code gap honestly. It is a reconstruction from the attached equations and parameters, not a recovery of the original code cited by the paper.

## What was inspected

The workbook contains ten sheets and **39,208 formula cells**, including shared-formula children. Every formula has a cached value, and no cached cell is an Excel error. There are no VBA macros, external-workbook links, defined names, data validation rules, or worksheet protection. The absence of validation is relevant to public usability. Protection would prevent accidental edits but is not a security boundary.

| Sheet | Formula cells | Purpose |
| --- | ---: | --- |
| Dashboard | 46 | Inputs, selected-intensity derivatives, grid extrema, outside option |
| Curves | 17,017 | Full legacy-model trajectory over 1,001 intensity values |
| Examples | 42 | Six synthetic parameter presets and outputs |
| ScenarioCurves | 13,013 | All six preset trajectories |
| Durability | 2,010 | Discounted avoided loss over 501 time points |
| Stacking | 41 | Common-mode mixture over one to ten layers |
| Notes | 0 | Main interpretation and limitations |
| BoundedMigration | 7,015 | Governed-share model, derivative and optima |
| Sources | 0 | Source and scope notes |
| Verification | 24 | Twelve two-formula default regression checks |

The paper has 419 native Word math elements, three tables, no tracked insertions or deletions, and no comments part. It renders to 28 pages. The full content was extracted and reviewed, and all pages were reviewed in contact sheets with key equations/tables checked in the rendered output. The document has sparse late pages, notably the single remaining reference on page 24, but no substantive pagination defect was found. This was not a manuscript editing task.

## Independent numerical verification

`src/gl_agent_reference.py` implements the equations using Python's standard library. The optional plotting flag requires Matplotlib. It reads Excel OOXML caches without editing the workbook. Model input parameters are deliberately frozen to the publication baseline for the workbook regression.

The fresh run passed **30 substantive checks**, including analytic versus finite-difference derivatives, q-only corner cases, the nesting identity, the non-monotonic high-loss case, bounded migration, the reviewer-capacity counterexample, durability limits, independent and common-failure limits, refresh carry-over limits, and invalid-input rejection. Randomized checks used a fixed seed and included 500 heterogeneous exponential cases, 500 heterogeneous hyperbolic cases, and 500 bounded-migration sign cases. The derivative sign check factors out a strictly positive exponential to avoid floating-point underflow in extreme generated cases.

The reconstructed implementation compared **39,251 input, formula-cache and status values** with the workbook. All passed at relative tolerance `1e-10` or absolute tolerance `1e-7`. The largest difference divided by `max(1, abs(expected))` was **1.6968542473909438e-13**, at `ScenarioCurves!J44`. These are comparisons, not a claim that every formula was recalculated in Microsoft Excel.

| Case | Continuous welfare optimum | Continuous global risk minimum | Maximum welfare |
| --- | ---: | ---: | ---: |
| Retained default | 1.446033874 | 2.057115003 | 1,249,569.876 |
| Summarization | 1.349251634 | 1.510906130 | 199,549.238 |
| MCP DevOps | 6.933998394 | 7.837549089 | 1,685,467.484 |
| Finance | 2.978364571 | 5.089347190 | 2,489,463.999 |
| Drafting | 0 | 0.169002485 | 132,500.000 |
| High-loss / smooth | 2.588028971 | 5.685049918 | 729,541.596 |
| High-loss / steep | 2.023920308 | 5.781680590 | 792,899.840 |

All values are synthetic annual-model results. Currency precision is numerical precision, not empirical accuracy. The Excel default grid correctly returns `Dashboard!C32 = 1.45` and `C33 = 2.06`; the difference from continuous values is expected from the 0.01 grid.

The steep preset has welfare stationary points at 2.023920308, 3.191083502, and 4.851557949. The first maximum is globally better than the last. At intensity 4, welfare is increasing again, with a derivative of approximately +49,022.77. This matters to the stale instruction discussed below.

The bounded-migration analytical minimum is 2.197224577 and the continuous welfare optimum is approximately 1.679110. The 0.01 workbook grid correctly returns 2.20 and 1.68. The q-only default optimum, residual risk and all-in share also match the manuscript: 2.941769763, 142,857.142857 and 0.367721220.

## Findings requiring attention

### 1. Legacy Notes contain scientific and operational claims that the revised paper rejects

The visible `Notes` sheet is substantially better than the old cell Notes. A user hovering a cell receives a conflicting explanation. This is a release-relevant content defect.

| Location | Existing issue | Recommended change |
| --- | --- | --- |
| `Dashboard!C9` | Suggests fewer than about five campaigns rarely justify controls, without conditioning on severity or burden. | Explain campaign attribution and annual units without universal numeric anchors. |
| `Dashboard!C10` | Presents 20–50% attack success as typical benchmark evidence without a source. | Require a declared generator, budget, feedback and evaluation universe. Treat 0.2 as synthetic. |
| `Dashboard!C11` | Supplies unsourced sector monetary anchors and describes worst reversible action rather than conditional expected severity. | Use the paper's expected gross loss conditional on crossing, with separate tail analysis. |
| `Dashboard!C14` | Claims capability tax often exceeds cash cost without evidence. | Describe valuation and avoid double-counting labour. |
| `Dashboard!C15` | Describes a catch-and-prevent fraction with plausibility anchors. | Define loss-weighted prevented/recovered fraction. Detection rate is insufficient. |
| `Dashboard!C18` | Claims one reviewer sustains 2,000–5,000 alerts per year at meaningful depth. | Use measured service time, queue rules and severity-weighted outcomes. |
| `Dashboard!C19` | Calls the two-maxima region evidence that greedy control purchasing fails. | Match Section 6.3: non-convexity alone does not establish a superior bundle. |
| `Dashboard!C24` | Promises a dropdown that does not exist. | Add a genuine input control or say to enter a numeric intensity between zero and ten. |
| `Dashboard!C31` | Says optimized residual always equals `k/gamma`. | State the interior condition; the corner residual is `R0`. |
| `Dashboard!C32` | Says every marginal increase beyond the welfare optimum is harmful. | Distinguish the global grid maximum from local derivative signs; the steep preset is a counterexample. |
| `Dashboard!C33` | Implies all points beyond the global minimum necessarily have locally increasing risk. | Say their risk cannot be below the global grid minimum; use the analytic derivative for local direction. |
| `Dashboard!C38` | Claims full-model burden always lies below the q-only share. | Remove the implied universal ordering. For gamma=0, kappa=2, load=0 and displacement=0, q-only optimum is zero but full-model optimum is about 1.2572. |
| `Durability!C7`, `C9` | Says decay is per adaptation cycle; visible labels and manuscript say per year. Assigns unsourced ranges to semantic/architectural controls. | Use calendar rates in inverse years, and distinguish `delta = kappa × effort arrival`. Remove type-based empirical anchors. |
| `Stacking!C6`, `C7` | Gives unsourced realistic ranges for same-model dependence and marginal failure. | Treat beta as a normalized mixture index and estimate common-universe marginals/joint failure. |

Replacing all old numerical-range guidance with paper-aligned explanations is cleaner than retaining inconsistent fragments.

### 2. The input-health formula accepts blanks and some text as VALID

`Dashboard!I15` checks inequalities but does not check that all 13 inputs and the dial are numeric. In an in-memory engine test, clearing `C9` left I15 as VALID and treated exposure as zero. Entering the text `unknown` in `C9` also left I15 as VALID while downstream calculations returned `#VALUE!`.

A minimal repair is to add `COUNT(C9:C21)=13` and `ISNUMBER(C24)` to the existing `AND` checks. An outer `IFERROR(...,"CHECK INPUTS")` is justified for the diagnostic itself; it must not convert calculation failures into valid zero results. Add numeric data validation with appropriate probability and positivity bounds to the actual editable input ranges. Do not represent the current I15 formula as comprehensive input validation.

`BoundedMigration!C22` likewise uses MIN and inequalities without requiring numeric completeness. `Stacking` and `Durability` have no separate domain status. Negative beta, probability above one, or negative decay can be entered without a workbook-level input rejection. Their mathematical valid domains should be enforced or checked locally.

### 3. Drawing and chart compatibility is poor

The imported OOXML contains empty and hidden legacy drawing objects around `Dashboard!A1:F35`. Both the artifact renderer and bundled LibreOffice PDF output show a large white object covering most of the title and input area. The underlying cell content remains present. `xl/drawings/drawing1.xml` includes `Text Box 24` and `AutoShape 24` elements with empty/custom geometry; remove these stray objects in the revised workbook while preserving the actual charts.

The native LibreOffice render also turns the welfare chart into an enormous legend with 1,001 coloured entries. `xl/charts/chart1.xml` defines a single-series line chart with `varyColors=1`. Rebuild it as an ordinary single-series line or numeric scatter chart with a clear title, one series and sparse numeric axis ticks. The adjacent risk chart's densely repeated gridlines and category labels also need adjustment. These are observed compatibility issues; Microsoft Excel's native UI has not been inspected, so the finding does not assert identical behaviour in every Excel version.

The `Examples` view also formats new high-loss columns G:H differently from C:F. The former show raw decimal probabilities and ungrouped amounts. Apply consistent input number formats when updating the release.

### 4. The reproducibility package described by the paper is missing

The manuscript's Section 7.3 and Appendix D refer to `gl_agent_reference.py`, `parameters.json`, numerical CSVs, figures and a 24-check execution record. Only the paper and workbook were attached. The newly created code should have an explicit provenance statement and separate results. Do not present its 30 checks and 39,251 comparisons as the original paper's claimed 24 checks and 37,048 comparisons.

The original manuscript can remain an archived publication baseline, accompanied by a brief repository note describing the new audit implementation. A future manuscript revision should update the reproducibility counts and file paths if this new implementation becomes the canonical supplement.

### 5. Licensing and deposit statements conflict

The paper's declarations explicitly license the simulator and Python implementation under MIT and the manuscript, explanatory documentation, figures, synthetic parameters and numerical results under CC BY 4.0. This grants a clear file-level allocation to preserve in the repository.

`Notes!C22` still says the distribution licence and repository DOI are to be chosen by the author. Replace it with the actual licence allocation and a reference to the repository licence files. A follow-up lookup on 26 October 2026 confirmed that manuscript DOI `10.5281/zenodo.22656510` resolves to a published Reproducibility Supplement (Version 1.0) dated 8 September 2026. Its listed workbook, Python implementation, and numerical outputs do not match this reconstructed package. Treat that DOI as an earlier related deposit. If this repository supersedes it, create and cite a new deposit version; otherwise link it as related material. Do not assign the earlier DOI to this different artifact set.

## Source checks and publication data

Spot checks verified the existence and matching titles/authors of the 2026 papers by Choi, Hermon and colleagues, and Le and colleagues using arXiv and the publisher:

- <https://arxiv.org/abs/2604.23058>
- <https://arxiv.org/html/2606.30783v1>
- <https://link.springer.com/article/10.1186/s42400-026-00628-w>

These checks do not constitute a full literature review or verification of every attribution.

The supplied inputs are explicitly synthetic. No operational incidents, credentials or confidential business records were found. The paper includes the author's contact details and ORCID as intentional publication metadata. A follow-up inspection on 26 October 2026 found Microsoft Information Protection label records in both the manuscript and the workbook. The records contain opaque label/site identifiers but no readable classification label. Check whether that metadata belongs in the public distribution rather than inferring sensitivity from its mere presence. See the [publication-metadata record](../validation/publication-metadata.json).

## Validation limits

The cached results and independent model checks are strong evidence for the published numerical examples. They do not establish that the model describes real deployments. The independent continuous optimizer scans for derivative sign changes over [0,10], then refines roots by bisection. It verifies the supplied regimes but is not a theorem prover or guaranteed finder of tangential stationary points in arbitrary new parameterizations.

Artifact-tool correctly recalculated direct scalar outputs but did not reliably refresh shared grid dependencies after scenario edits. In particular, the high-loss edit left the displayed grid extrema at baseline in that engine. Consequently those tests are recorded as an engine limitation, not as evidence of an Excel formula defect. Native LibreOffice rendered the source workbook and its baseline outputs; an interactive Microsoft Excel edit/recalculate/save/reopen cycle was not available.

## Suggested public quick start

1. Download the workbook rather than opening GitHub's binary preview. Open it in desktop Excel and enable automatic calculation.
2. Read the repository's known issues for the exact workbook version. Work from a copy.
3. Read `Notes` first. The labels name synthetic assumptions, not measured industry defaults.
4. Set `Dashboard!C9:C21` with consistent annual units and choose `C24` between zero and ten.
5. Read the welfare and risk optima in C32:C33, the grid boundary warning in C41, and local derivatives in C44:C45. Inspect the whole curve in a non-convex case.
6. Use `BoundedMigration` for the governed-share alternative. Keep its accounting separate from the legacy quadratic displacement term.
7. Use `Durability` for gross avoided-loss comparisons and `Stacking` only under its stated common-universe, equal-marginal model.
8. Run `python3 src/gl_agent_reference.py --out local-results --check-workbook workbooks/GL-Agent-Simulator.xlsx` against the unchanged publication inputs. The check requires current saved caches. Optional `--plots` generates three figures.

## Reconstructed supplement files

- `src/gl_agent_reference.py` — standalone independent model and regression CLI.
- `results/parameters.json` — documented synthetic parameters and provenance.
- `results/numerical_results.csv` — continuous extrema and stationary points.
- `results/curve_results.csv` — seven complete legacy-model trajectories.
- `results/bounded_results.csv` — bounded migration trajectory.
- `results/verification_results.csv` — 30 fresh check results.
- `results/verification_summary.json` — machine-readable execution and cache-comparison summary.
- `results/bounded-migration.png`, `welfare.png`, `durability.png` — figures from the reconstructed implementation.

Intermediate XML extractions and rendering files are not required to execute the reconstructed supplement.

## Publication preparation addendum — 26 October 2026

A subsequent repository-only inspection found Microsoft Information Protection label records in every supplied Office source in this repository. The identifiers are omitted from the [publication-metadata record](../validation/publication-metadata.json). Their presence alone is not a confidentiality determination. No source Office artifact was modified during this follow-up.

The GitHub workflow now runs the independent model and workbook comparisons, then compares all generated numerical evidence with the checked-in baseline. The [browser publishing guide](../PUBLISHING.md), [native Excel acceptance record](../validation/native-excel-acceptance.md), and release-evidence checks were added for publication preparation. These changes affect repository scaffolding and documentation; they do not change the functional findings or numerical/workbook baselines recorded above.
