# Research protocol — 23 September 2026

This is an independent project. No results or code from the other research projects are reused.

## Question and candidate contribution

For public candidate contracts whose execution requires the private participation of named agents, what is the maximum probability (or public value) of a feasible, publicly observable agreement under participant-level differential privacy? Can a single policy attain the optimum at every participation profile?

The known obstruction between hard feasibility and privacy is not claimed as new. The proposed contribution is an exact contract-incidence characterization, a globally private lottery attaining any one profile's upper bound, and an explicit obstruction to simultaneous optimality. These claims will be narrowed or removed if they fail verification or duplicate prior work.

## Model fixed before experiments

- Public finite contract menu; a contract is a nonempty set of required agents and a nonnegative public utility.
- Each agent has one private availability/participation bit. Adjacent profiles differ in one bit.
- At most one contract is selected. No contract may execute with an unavailable required agent.
- Public output is the executed contract identifier or a single abstention symbol.
- Trusted broker knows the bits. Public menus, utility, priors and lottery weights are not computed from these private bits.
- Differential privacy covers this output, not arbitrary messages, timing or a broker's internal state.
- No incentive compatibility or general LLM negotiation claim.

## Planned checks

1. Compare the proposed local packing bound with an independently constructed full-profile privacy LP, for all 127 nonempty menus on three agents, three delta values (0.01, 0.1, 0.4), and epsilon in {0, log 2}. Use a public objective concentrated on the all-available profile. Store complete distributions and constraint residuals.
2. Derive and check a five-cycle counterexample to simultaneous pointwise optimality. Compute its full-profile tradeoff as the objective weight on full availability varies over 21 equally spaced values. Do not claim numerical optimality is a proof.
3. Evaluate 24 seeded six-agent menus, eight distinct contracts of sizes two or three, uniform public utilities, independent availability priors q in {0.5, 0.8}, delta in {0.02, 0.1, 0.25}, epsilon in {0, log 2}. Compare a uniform fixed lottery, a prior-optimized fixed lottery, the full-profile adaptive LP, and an unattainable pointwise upper bound. Exact expectations over all 64 profiles; synthetic scenarios, not measured deployment rates.
4. Independently audit distributions through event enumeration on small outputs and the exact finite-output hockey-stick formula on all outputs. Include deliberately incorrect singleton-only checks and private renormalization as negative controls.
5. Rational arithmetic checks of hand-derived examples and primal/dual certificates; meaningful unit tests for feasibility, privacy, normalization, weights and reproducibility.

## Reporting

Retain all evaluated fixtures, failed numerical solves, parameters and scripts. No learned performance claim, statistical significance claim, real-world adoption claim or guaranteed publication novelty. Any experiment changed after observation must be recorded in AMENDMENTS.md. A working theorem can be conclusive within its assumptions without asserting deployment effectiveness.

## Prior-art screen already completed

The broad feasibility/privacy conflict is established by private exchange and private optimization. Binary distance-to-boundary mechanisms also already exist and are not a contribution. The focused literature comparison will cover those results, general finite-mechanism optimization, and current agent negotiation work. Search absence is not proof of novelty.
