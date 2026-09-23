# Literature and contribution audit

Search and source inspection date: **23 September 2026**. This is a focused prior-art review, not proof of universal novelty or a patent search. Primary sources are listed in `sources.json`, with retrieval URLs and SHA-256 hashes. Downloaded papers were inspected locally, including relevant theorem statements, model definitions and limitations. Third-party papers are excluded from the repository.

## Research directions rejected or narrowed

1. General LLM plan synchronization already has direct recent work, including SyncPlan (arXiv:2608.01652); it was not developed into this paper.
2. General behavioral leakage during negotiation has a close recent paper by Rani (arXiv:2607.06815). We did not claim to discover it.
3. Impossibility of hiding private hard feasibility is established in private allocation, exchange and constraint optimization. A bare impossibility argument would be too weak as a new contribution.
4. A proposed binary distance-to-infeasibility mechanism was rejected as novel because graph-based optimal binary mechanisms already cover closely related constructions.
5. The final question is the projection of feasible private contract mechanisms onto a fixed input row, and compatibility of individually optimal rows. The five-cycle exact frontier and the epsilon separation provide more than the original support observation.

## Closest antecedents and precise distinctions

| Primary source | Existing contribution relevant here | What the manuscript adds or does not claim |
|---|---|---|
| [Hsu et al., Private Matchings and Allocations, 2016](https://arxiv.org/abs/1311.2828) | Allocation under joint DP; ordinary output privacy conflicts with accurate allocations. | Our observed output publicly names one entire contract; adjacency changes a participation bit. We do not present allocation impossibility as new. |
| [Kannan et al., Private Pareto Optimal Exchange, 2018](https://jamiemorgenstern.com/papers/private-ttc.pdf) | Privacy/individual-rationality obstruction in exchange; marginal privacy as a relaxation. | The event used in the necessity proof is the same kind of support obstruction. New claim is its exact incidence-polytope characterization plus constructive extension, in a different restricted model. |
| [Muñoz Medina et al., Private Optimization without Constraint Violations, 2021](https://proceedings.mlr.press/v130/munoz21a.html) | Always-feasible optimization with private linear constraint bounds and near-optimal error bounds. | We optimize distributions on discrete public contracts and characterize the attainable row exactly. We do not claim the first private always-feasible optimizer. |
| [Damle et al., Differentially Private Multi-Agent Constraint Optimization, 2021](https://doi.org/10.1145/3486622.3493929) | Randomized private DCOP solving. The final paper explicitly limits the studied setting to soft constraints and discusses hard-constraint leakage. | This is directly relevant multi-agent prior work. Our hard feasibility results should not be framed as refuting its stated scope. |
| [Ghosh et al., Universally Utility-Maximizing Privacy Mechanisms, 2012](https://timroughgarden.org/papers/priv.pdf) | Finite mechanism LPs, optimality and public-prior utility. | Our all-profile LP is an evaluation implementation of established machinery. It is not claimed as a new general optimizer. |
| [Brenner and Nissim, Impossibility of Differentially Private Universally Optimal Mechanisms, 2010](https://arxiv.org/abs/1008.0256) | General nonexistence results, including cycles in a query-output privacy graph. | Our contract cycle is not their privacy graph; the input graph is the Boolean cube. The contribution is the explicit approximate-DP frontier and mechanisms, not the generic insight that optima can conflict. |
| [Fernandes et al., Universal Optimality and Robust Utility Bounds for Metric Differential Privacy, 2022](https://arxiv.org/abs/2205.01258) | Generalized universal optimality and utility capacities. | We do not claim a new universal-utility framework. Our theorem is a special finite contract-selection characterization with hard output exclusions. |
| [Torkamani et al., Optimal Binary Differential Privacy via Graphs, 2023](https://arxiv.org/abs/2310.20486) | Optimal binary mechanisms determined through boundary behavior. | We rejected a binary-boundary proposal as a contribution. The retained work depends on multiple contract identities and event unions. |
| [Wyse et al., Commitment to Cooperation with Self-Negotiated Contracts, 2026](https://arxiv.org/abs/2607.22750) | Enforceable contract representations and LLM cooperation experiments. | This motivates agent contracting. We do not reproduce its benchmark or infer improvements in LLM cooperation. |
| [Rani, Behavioral Privacy Leakage in Agentic Negotiation, 2026](https://arxiv.org/abs/2607.06815) | Randomized negotiation traces and behavioral privacy claims. | Our result covers a terminal outcome under a declared adjacency relation. We do not claim its reported experiments measure this problem, and we do not reproduce its performance figures. |
| [Dwork and Roth, Algorithmic Foundations of Differential Privacy, 2014](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf) | Standard DP, post-processing, composition and elementary privacy reasoning. | Used as background; the privacy definition and support argument are not new. |

## Queries used in the focused screen

- `differential privacy bilateral trade individual rationality impossibility feasibility agreement`
- `private multi agent constraint satisfaction differential privacy feasible solution impossibility`
- `negotiation differential privacy impossibility`
- `differential privacy binary graph optimal mechanism boundary`
- `differential privacy distance to infeasible`
- `differential privacy feasible fractional packing`
- `differential privacy star graph optimal mechanism`
- `differential privacy matching delta individual rationality`
- `differential privacy hypergraph matching`
- `differential privacy participation probability matching`
- `optimal differentially private linear program finite mechanisms`
- `privacy feasible fractional matching`
- `contract selection differential privacy`
- `differential privacy fractional packing number`
- `differential privacy five-cycle`
- `differential privacy consent fractional`
- `private participation matching`
- `privacy contract lotteries`

Broader queries also screened LLM negotiation, commitment, handoff and privacy work. Absence of an exact result in these searches is not a novelty certificate. No comprehensive patent database search was performed.

## Claim assessment

**Defensible specific contribution:** the exact set of attainable rows for the stated private-participation model; a simple global extension for each row; the exact C5 success frontier at epsilon=0; and the explicit strict gain at epsilon=log(2), with every pointwise optimum unchanged.

**Established ingredients:** support-based privacy obstruction, coupling/total variation, fractional matching, LP duality, symmetrization, approximate-DP event checks, finite-mechanism LPs and convex mixtures.

**Not established:** first-ever treatment of outcome leakage, broad novelty of private contract lotteries, patentability, commercial demand, superiority on real negotiations, or a high numerical chance of acceptance. A suitable workshop may value the exact results and reproducible artifact; a reviewer may still judge the model too narrow or the specialization too incremental.
