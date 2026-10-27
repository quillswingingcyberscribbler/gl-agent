# Methodology

GL-Agent asks whether a proposed control change improves the value of an admissible AI-agent deployment after considering both its protection and its burden. The [paper](../paper/GL-Agent-Paper.docx) provides the formal results, assumptions and proposed measurement designs. The Excel and Python implementations illustrate selected scalar families.

## Define the boundary first

The unit of analysis is a deployment, action class and authority boundary. An attack campaign has a probability of crossing that boundary, a conditional gross loss after crossing, and an amount of loss prevented or recovered by the subsequent intervention stage.

For a single class, residual expected attack loss is:

$$R = \lambda q L(1-h)$$

Here `lambda` is campaigns per year, `q` is the boundary-crossing probability, `L` is expected gross loss conditional on crossing, and `h` is the **loss-weighted prevented fraction**. A detection rate alone does not identify `h`. Campaign counts and downstream losses must not be counted repeatedly across overlapping boundaries.

The reduced objective is:

$$W = B - R - C - D$$

`B` is delivered benefit, `C` direct control cost, and `D` incremental displacement loss that is not already inside `R`. All terms use a consistent period and monetary unit. Legal, rights and separately justified catastrophic-risk constraints define the admissible set before welfare optimization.

## The legacy simulator

The `Dashboard`, `Curves`, `Examples` and `ScenarioCurves` sheets use a scalar intensity `x` along a declared control path:

$$q(x)=q_0 e^{-\gamma x}$$

$$h(x)=h_{\max}(1-e^{-\kappa_d x})\frac{1}{1+\exp((v_0x-A_c)/s)}$$

$$R_{total}(x)=\lambda q(x)L(1-h(x))+dx^2$$

$$W(x)=B_0-(c+\tau)x-R_{total}(x)$$

`c` measures direct annual cost per unit intensity. `tau` measures lost useful capability in the same units. The review component combines increasing intervention opportunity with a fatigue factor driven by load relative to capacity. This is a constructed response family, not a measured universal law.

The workbook evaluates 1,001 intensity values from zero to ten. It selects the first point in a tie. Its optima have grid resolution 0.01. The independent implementation additionally scans analytic derivative sign changes and refines them by bisection.

### Global optimum and local direction

A welfare optimum and a risk minimum answer different questions. With a strictly increasing all-in burden along a feasible path, a global welfare maximizer cannot lie beyond the earliest global risk minimizer under the paper's stated conditions. This result does not imply that either curve is unimodal.

For the supplied high-loss steep-fatigue preset, welfare has local maxima near 2.024 and 4.852. The earlier maximum is globally better, but welfare increases between the intervening local minimum and the later peak. Read the local derivative before claiming that another increment always makes things worse.

Crossing reviewer capacity is neither necessary nor sufficient for total risk to increase. Continued probability reduction can outweigh fatigue, while displacement can reverse total risk even without fatigue.

## The restricted q-only result

With exponential residual loss and a linear all-in burden `k = c + tau`, the positive optimum is:

$$x^*=\frac{1}{\gamma}\log\frac{\gamma R_0}{k}$$

It applies when `gamma × R0 > k`. Otherwise the optimum is zero. Interior optimized residual risk is `k/gamma`; corner residual risk remains `R0`.

Within the restricted optimized family, all-in burden relative to baseline loss is bounded by `1/e`. The paper extends the result to specified heterogeneous and convex-portfolio settings. The full fatigue/displacement simulator is not covered by a universal 1/e budget rule. A bound derived from an unconstrained optimum also does not override an admissibility requirement.

## Bounded migration

The separate `BoundedMigration` sheet uses a fixed reference workload. The governed share falls as `sigma = exp(-rho × x)`, full-workload governed risk falls exponentially, and the substitute channel has constant full-workload risk `U`:

$$R_{total}(x)=r_0e^{-(\gamma+\rho)x}+U(1-e^{-\rho x})$$

Migration is bounded by the available workload. Realized risk can nonetheless fall and later rise. For positive `r0`, `U`, `gamma` and `rho`, an interior minimum exists exactly when `(gamma + rho) × r0 > rho × U`:

$$x_R=\frac{1}{\gamma}\log\frac{(\gamma+\rho)r_0}{\rho U}$$

The exact incremental-displacement identity is `D = (1-sigma) × (U-RG)`, where `RG` is full-workload governed risk. Adding this `D` to an already mixed total risk double-counts displacement. Abandoned tasks, substitute completion and expanded permissions are different outcomes and need separate measurement.

## Durability and dependence

`Durability` evaluates gross discounted avoided loss under constant baseline exposure:

$$V(T)=R_0\epsilon_0\frac{1-e^{-(r+\delta)T}}{r+\delta}$$

The limit is `R0 × epsilon0 × T` when `r + delta = 0`. Rates use inverse years. Calendar decay can be decomposed into adaptability per unit attacker effort and effort arrival, but that decomposition needs measurement. A control's semantic or architectural label does not supply a decay coefficient.

`Stacking` uses a specific joint-failure mixture for equal-marginal layers:

$$Q_n=(1-\beta)q^n+\beta q$$

For fixed beta greater than zero and `0 < q < 1`, improvement relative to one layer approaches `1/beta`. This is conditional on the mixture, common evaluation universe and conjunctive harm model. Correlation alone does not establish a universal ceiling, causal shared-model failure, or failure of submodular selection guarantees.

The independent Python implementation also verifies the paper's refresh carry-over limits. That mechanism is not an additional editable worksheet.

## Evidence and intended use

The inputs are synthetic. The project separates mathematical implications, tests of assumptions and empirical hypotheses. It provides a transparent sensitivity model and a measurement agenda. Operational use requires estimating exposure, conditional loss, prevented loss, benefit and migration with their uncertainty, and checking whether the response family fits the specific deployment.

The [review](review.md) records what was checked. [Known issues](known-issues.md) lists the archived workbook's implementation and guidance limitations.
