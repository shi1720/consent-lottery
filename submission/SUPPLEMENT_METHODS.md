# Supplementary methodological information

## Tool assistance

OpenAI Codex, using the GPT-6 model family identified in the research session, assisted with literature searches, hypothesis development, mathematical derivations, experimental design, code, computational verification, figures and manuscript drafting. An exact serving snapshot identifier was not supplied and is not asserted. No external model API experiment was run. The manuscript's model-independent mechanism claims rest on the displayed proofs and executed code.

This was an extended interaction initiated by a request for an original, technically correct research paper and reproducible implementation suitable for an AAMAS 2027 workshop. An exact relevant excerpt of the initial task prompt was:

> You have done great work till now - I now want you to write an end to end research paper - actual research paper that can be accepted into publications and presented at major conferences - not just faking it. it needs to be great - complete - include real code - figures, visuals, etc. and actual thing of research that contributes to it - something that has commercial applications as well and do your literature review to make sure we are actually writing a new paper on a new topic and proposing a highly possible novel solution - spend a lot of time on that. do actual work - write code - add to github etc. to share with the paper - very professional paper - add me as author and everything - highly technical and correct and end to end - take all the time you need - great language - must meet all the requirements - and please make sure it is correct and has high chance of getting accepted into major publications and conferences.

This is an excerpt, not a reconstructed complete prompt or complete conversation export. Unrelated account setup instructions and confidential information are excluded. Full exact conversation history and internal model state are not included in this artifact. The research process and the distinctions between predeclared experiments and exploratory theory are retained in the protocol, amendments, source audit, source code and raw result files.

The initial exploration rejected broad synchronization and generic negotiation-privacy ideas after finding close prior work. It also rejected a binary graph-boundary mechanism as a novelty claim. The retained analysis developed the participation-incidence characterization. The exact five-cycle frontier and the explicit epsilon=log(2) construction were derived after observing the declared cycle LP results; this sequence is documented in `notes/AMENDMENTS.md`.

All code checks and internal mathematical review were performed within the same tool-assisted workflow. They are not external peer review. No claim is made that a human reviewer has independently validated the manuscript. The named author remains responsible for reviewing the work and any declarations made at submission.

## Reproduction details

- Python 3.9.6, NumPy 2.0.2, SciPy 1.13.1 and Matplotlib 3.9.4.
- Public-profile design, fixed seeds 27000–27023 and exact finite expectations.
- The optimizer's privacy inequalities include all 2^n profiles, regardless of prior support.
- Separate saved-result verification does not import SciPy or the implementation package.
- Rational cycle verification enumerates all 64 output events on each of 160 directed input edges.
- The 762 small mechanism distributions are independently reconstructed as fractions and checked exactly. This certifies the reconstructed distributions, not arbitrary floating-point execution of the optimizer output.
- The sampler accepts rational weights and does not renormalize or retry after private vetoes.
- Figures are deterministic Matplotlib renderings of mathematical constructions and saved computed results. No generated illustrative imagery was used.

The manuscript, code, data, protocol and this disclosure are intended to be considered together when preparing the actual workshop submission.
