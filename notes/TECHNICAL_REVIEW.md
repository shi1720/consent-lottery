# Internal technical review

Date: 23 September 2026. This is an internal tool-assisted audit, not external peer review or author approval.

## Mathematical claims

### Exact row projection

Necessity uses the event comprising **all** contracts incident to one agent, compared to that agent's withdrawal. This yields a sum constraint, not a per-contract delta constraint. Normalization and infeasible-output exclusions complete the polytope. Sufficiency uses a fixed lottery on the whole public menu and a same-draw coupling at every neighboring profile. Any differing output requires drawing an incident contract, whose mass is at most delta_i. The proof covers every profile, including inputs with zero objective prior.

The design profile is held fixed while constructing the extension. Re-solving the packing LP after seeing each private input is not licensed by the theorem. The manuscript distinguishes those quantifiers explicitly.

The fractional matching reduction concerns probabilities of selecting **one** contract, not a simultaneously executable fractional allocation. Uniform positive delta gives min(1, delta times fractional matching number). Nonempty contracts ensure finite matching number. The dual has nonnegative participant prices and an extra normalization price.

### Five-cycle incompatibility

For delta <= 2/5, full success 5 delta / 2 saturates all five participation loads. Odd-cycle linear equations force every edge probability to delta/2. A withdrawn vertex leaves a path of three edges; success 2 delta uniquely sets endpoint edges to delta and the middle to zero. The event consisting of both removed edges plus the middle surviving edge has mass 3 delta / 2 against zero. Its privacy violation cannot be fixed by increasing finite epsilon.

### Exact zero-epsilon frontier

Dihedral averaging preserves h and mean w and respects the full Boolean-cube privacy domain. Let full edge probability be a; path probabilities b,c,b; and two-edge path probabilities d,d. The following bounds hold:

- h = 5a <= 5 delta / 2.
- 2d <= delta from a shared agent's load.
- 2b <= d + delta from the event containing both endpoint edges and deletion of one endpoint.
- b+c <= delta from the path's interior load.
- 3a <= c+delta from the deleted-edges-plus-middle event.

These imply w <= 7 delta / 4 and w <= 3 delta - 3h/5. Both endpoint constructions have nonnegative residual abstention, and exhaustive transition cases bound total variation. Convex mixtures attain the complete nondominated segment. The rational checker verifies 63 explicit mixture distributions without SciPy or implementation imports.

### Positive epsilon separation

Mechanism C has path probabilities delta,0,delta; full probabilities delta/3; and smaller-profile rules in the paper. For multiplier two, the only additional reverse-direction expression is delta/2 + max(0,3 delta - 1), bounded by delta exactly when delta <= 2/5. Full-profile abstention contributes max(0,7 delta / 3 - 1) = 0 in this range. All transition cases are accounted for. Mean withdrawal success 2 delta reaches the pointwise bound. Three rational instances verify all events; the proof covers the whole stated delta interval.

## Computational checks

- All 1,113 primary solver distributions are retained: 762 exhaustive, 63 cycle and 288 benchmark.
- Independent verification of the 762 small mechanisms uses rational reconstruction and exact DP inequalities. It certifies those reconstructed distributions, not floating-point sampling by the LP implementation.
- All 381 packing primal/dual certificates meet exact feasibility and weak-duality equality.
- Every larger saved policy is checked against the finite-output hockey-stick formula. Maximum positive floating-point excess is below 6e-16, against a declared audit tolerance 1e-8.
- Benchmark expectations are independently recomputed from all input profiles and public priors.
- In all 288 benchmark comparisons, adaptive expected utility exceeds the fixed-lottery value; this is a property of the fixed synthetic suite, not a significance claim about deployments.
- The broker uses exact rational loads and integer sampling, with one-use enforcement within one process. It is not a persistent or side-channel-secure production broker.
- 22 tests passed after the sampler was added. Tests cover the privacy union pitfall, private renormalization, repeated use, invalid weights and exact finite sample-space counts.

## Limitations that must remain visible

The participation bit is a strong simplification. It applies across all public contracts incident to that agent. Arbitrary private acceptability sets, private prices and private menu generation are not modeled. Public executed identities create the exclusion obstruction. A different observer or joint-privacy requirement can change the result. Tiny delta implies tiny throughput in small menus. The adaptive oracle is exponential, and no general efficient adaptive approximation is provided. These are material limits on commercial use and venue fit.

## Literature and originality assessment

The support obstruction, fractional packing, coupling, LP duality, finite privacy LPs, convex symmetrization and generic incompatibility of optimal privacy mechanisms are established. The exact row projection and explicit contract-cycle frontier are the manuscript's specific claims. No exact duplicate was identified in the focused primary-source review, but completeness of novelty and patentability are not certified.

## Presentation checks

Use the official unmodified AAMAS class with unsubmitted manuscript metadata. All seven final rendered pages, references, figures and margins were inspected; see `PDF_QA.md`. The author PDF must not claim a proceedings appearance or submission number. Do not submit through the organizer workshop-proposal form.
