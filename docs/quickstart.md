# Quick start

GL-Agent supports two workflows: an interactive Excel exploration and an independent reproduction of the published synthetic examples. Start with the Python workflow if your spreadsheet application displays the archived workbook poorly.

## Excel workflow

Download [the workbook](../workbooks/GL-Agent-Simulator.xlsx), make a working copy and open it in desktop Excel. Use automatic calculation. The supplied workbook's legacy drawing objects render badly in LibreOffice and some preview engines; see [known issues](known-issues.md).

1. Read the workbook's `Notes` sheet and this repository's [methodology](methodology.md). Some old hover Notes remain inconsistent with the revised paper; the repository's [errata](known-issues.md) identify them.
2. Define the deployment, action class, protected boundary and control path. Intensity `x` is a position along that declared path, not a universal security rating.
3. Enter the annual assumptions in `Dashboard!C9:C21`. Keep units consistent and use numeric values throughout. The current input-health cell does not reliably reject blank or text entries.
4. Enter a numeric intensity from zero to ten in `Dashboard!C24`. The old Note mentions a dropdown, but no dropdown exists in this version.
5. Read the outputs below, inspect the full curves and record the assumptions with any conclusion.

| Output | Location | Interpretation |
| --- | --- | --- |
| Q-only optimal intensity | `Dashboard!C30` | Restricted model without review or displacement |
| Full-model welfare optimum | `Dashboard!C32` | Best welfare point on the 0.01 grid |
| Full-model global risk minimum | `Dashboard!C33` | Lowest total-risk point on the same grid |
| Maximum welfare and outside option | `Dashboard!C39:C40` | Comparison with non-deployment, normalized to zero |
| Search-range warning | `Dashboard!C41` | An optimum at the upper edge needs a wider search |
| Selected-point welfare and risk | `Dashboard!C42:C43` | Outcomes at the dial setting |
| Local marginal directions | `Dashboard!C44:C45` | Whether a small increase currently raises or lowers each outcome |

The default should show welfare-optimal intensity **1.45** and risk-minimizing intensity **2.06**. A changed set of inputs need not retain the default `Verification` results.

### Compare synthetic presets

`Examples!C:H` contains six parameter columns. Copy the thirteen input values from rows 6–18 into `Dashboard!C9:C21`, preserving their order. These are independent scenarios, not a calibrated ranking of industries.

Try the **High-loss / steep** column. Its welfare curve has two local maxima, and the earlier one is globally better. Beyond a global maximum, the local derivative can still become positive again. This is why the whole curve and marginal signs are both useful.

### Explore the other mechanisms

- `BoundedMigration` models a governed workload share and a substitute channel. It is a separate accounting model; do not add its mixed risk to the legacy quadratic displacement term.
- `Durability` compares gross discounted avoided loss over time. Rates are per year. Setup costs, operating costs and capability burden are excluded from this comparison.
- `Stacking` applies a specific common-shock mixture to equal-marginal layers. Enter probabilities and beta between zero and one. A dependence estimate needs marginal and joint results from the same evaluation cases.

## Python workflow

From the repository directory, run:

```bash
python3 src/gl_agent_reference.py --out local-results --check-workbook workbooks/GL-Agent-Simulator.xlsx
```

The command writes numerical results, curves, parameters and verification records, prints a compact result, and exits unsuccessfully if a check fails. With the supplied workbook and unchanged defaults, expect **30 model checks passed** and **39,251 saved-value comparisons passed**.

If Matplotlib is available, add `--plots` to generate the three figures:

```bash
python3 src/gl_agent_reference.py --out local-results --check-workbook workbooks/GL-Agent-Simulator.xlsx --plots
```

The workbook check compares saved caches with fixed publication expectations. It does not recalculate Excel formulas or automatically reinterpret changed assumptions. See [reproducibility](reproducibility.md) before using modified inputs.
