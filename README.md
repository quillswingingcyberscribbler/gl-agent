<img src="assets/logo.png" alt="GL-Agent logo" width="160">

# GL-Agent

**An Excel simulator and reproducible research model for the economics of AI-agent controls.**

GL-Agent explores how control intensity changes attack loss, useful capability, reviewer workload and displaced activity. It distinguishes the point that maximizes welfare from the point that minimizes realized risk, and makes the assumptions behind those results inspectable.

**Status:** reviewed prerelease `0.1.0-review.1`, based on manuscript and simulator v1.0. The supplied numerical examples reproduce. The public manuscript and simulator were metadata-cleaned on 27 October 2026; the Public sensitivity labels are retained. Main text, media files, formulas and saved cell values match the original sources. The manuscript header and page-number footers were restored. The archived workbook still needs input-validation, cell-Note and drawing/chart corrections before a polished stable release. See [known issues](docs/known-issues.md).


## Start here

| You want to… | Open |
| --- | --- |
| Explore the model in Excel | [GL-Agent-Simulator.xlsx](workbooks/GL-Agent-Simulator.xlsx) and the [quick start](docs/quickstart.md) |
| Read the theory and measurement protocol | [GL-Agent-Paper.docx](paper/GL-Agent-Paper.docx) |
| Understand the model boundaries | [Methodology](docs/methodology.md) |
| Reproduce the numerical examples | [Reproducibility guide](docs/reproducibility.md) |
| Inspect the audit evidence | [Review](docs/review.md) and [machine-readable results](results/verification_summary.json) |
| Prepare the next release | [Issues to open](docs/issues-to-open.md) |

The public paper and workbook are metadata-cleaned copies with portable filenames. Their current hashes and the previous source identities are documented in [validation/manifest.json](validation/manifest.json). All numerical presets are synthetic. Names such as “Finance” and “MCP DevOps” identify constructed scenarios, not measured sector profiles.

## Run the independent checks

Python 3.10 or later is sufficient; the verification command uses only the standard library:

```bash
python3 src/gl_agent_reference.py --out local-results --check-workbook workbooks/GL-Agent-Simulator.xlsx
```

The checked-in `results/` directory records the reviewed baseline. Use `local-results/` for a new run so the reference evidence remains easy to compare.

The supplied Python code is an **independent reconstruction from the attached paper and workbook**, prepared on 22 October 2026. The original executable supplement described in the paper was not supplied. This package does not claim to recover that original implementation or its execution record.

## What the review established

- **30 independent model checks passed**, covering derivatives, corners, bounded migration, fatigue, durability, dependence and refresh limits.
- **39,251 saved-value comparisons passed** against the supplied workbook; the largest scaled difference was approximately `1.70e-13`.
- The default continuous welfare optimum is **1.446034** and global risk minimum **2.057115**. The workbook's 0.01 grid correctly reports **1.45** and **2.06**.
- All six scenario presets reproduce, including the steep-fatigue case with two local welfare maxima.

These checks establish numerical agreement and selected mathematical implications. Saved-value comparisons do not replace an interactive Excel recalculation test, and synthetic agreement does not establish empirical model fit.

## Project contents

```text
paper/       Supplied manuscript
workbooks/   Supplied Excel simulator
src/         Independent Python reference implementation
results/     Parameters, numerical outputs, verification and figures
docs/        Usage, methodology, review and release issues
assets/      Project identity
```

## Author, citation and licensing

Matthias Muhlert, [ORCID 0009-0006-3640-7779](https://orcid.org/0009-0006-3640-7779). The source manuscript is v1.0, dated 7 September 2026, and identifies itself as a preprint that has not been peer reviewed. Use [CITATION.cff](CITATION.cff) for citation metadata. No DOI is assigned to this reconstructed package. The earlier [reproducibility-supplement DOI](https://doi.org/10.5281/zenodo.22656510) now resolves, but its file inventory differs from this package and must be cited as a related earlier deposit rather than as this release.

The simulator and Python code use the **MIT License**. The manuscript, explanatory documentation, figures, synthetic parameters and numerical results use **CC BY 4.0**, following the manuscript's explicit allocation. See the repository licence files for the applicable terms.

## Prepare publication

The [browser-only publishing guide](PUBLISHING.md) covers repository creation, file upload, Actions, visibility, and prerelease creation through GitHub's web interface. The [publication-metadata review](validation/publication-metadata.json) is complete. For a stable release, complete the [native Excel acceptance record](validation/native-excel-acceptance.md) and address the functional workbook issues described above.
