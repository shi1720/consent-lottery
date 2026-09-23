"""Reference full-profile finite-output DP optimization.

This exponential-state oracle is an evaluation baseline, not a scalable broker.
It constructs DP constraints directly, independently of the packing theorem.
"""
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from .core import budgets


def optimal_mechanism(menu, epsilon, delta, prior, values=None, full_row=None):
    if epsilon < 0 or not np.isfinite(epsilon):
        raise ValueError("invalid epsilon")
    d = budgets(delta, menu.n)
    states, outputs = 2**menu.n, len(menu.contracts) + 1
    pi = np.asarray(prior, dtype=float)
    if pi.shape != (states,) or (pi < 0).any() or not np.isclose(pi.sum(), 1):
        raise ValueError("prior must be a probability vector over profiles")
    v = np.r_[0., np.ones(outputs - 1) if values is None else values]
    if v.shape != (outputs,) or not np.isfinite(v).all() or (v < 0).any():
        raise ValueError("invalid public values")
    edges = [(x, x ^ (1 << i), i) for x in range(states) for i in range(menu.n)]
    probvars = states * outputs
    variables = probvars + len(edges) * outputs
    cost = np.zeros(variables)
    cost[:probvars] = -(pi[:, None] * v[None, :]).ravel()
    bounds = []
    for x in range(states):
        bounds.append((0, 1))
        bounds.extend((0, 1) if ok else (0, 0) for ok in menu.feasible(x))
    bounds.extend([(0, None)] * (variables - probvars))
    rows, cols, vals, rhs = [], [], [], []
    row = 0
    for e, (x, y, i) in enumerate(edges):
        for j in range(outputs):
            rows.extend([row] * 3)
            cols.extend([x * outputs + j, y * outputs + j, probvars + e * outputs + j])
            vals.extend([1., -np.exp(epsilon), -1.])
            rhs.append(0.)
            row += 1
        for j in range(outputs):
            rows.append(row); cols.append(probvars + e * outputs + j); vals.append(1.)
        rhs.append(d[i]); row += 1
    Aub = coo_matrix((vals, (rows, cols)), shape=(row, variables)).tocsr()
    er, ec, ev, beq = [], [], [], []
    for x in range(states):
        er.extend([x] * outputs); ec.extend(range(x * outputs, (x + 1) * outputs))
        ev.extend([1.] * outputs); beq.append(1.)
    if full_row is not None:
        if len(full_row) != outputs:
            raise ValueError("full row shape mismatch")
        for j, target in enumerate(full_row):
            er.append(states + j); ec.append((states - 1) * outputs + j); ev.append(1.)
            beq.append(float(target))
    Aeq = coo_matrix((ev, (er, ec)), shape=(len(beq), variables)).tocsr()
    result = linprog(cost, A_ub=Aub, b_ub=rhs, A_eq=Aeq, b_eq=beq,
                     bounds=bounds, method="highs",
                     options={"dual_feasibility_tolerance": 1e-9,
                              "primal_feasibility_tolerance": 1e-9})
    if not result.success:
        raise RuntimeError(result.message)
    P = result.x[:probvars].reshape(states, outputs)
    return {"P": P, "value": float(-result.fun), "status": result.message,
            "variables": variables, "inequalities": row,
            "max_solver_residual": float(max(0., -(result.ineqlin.residual.min())))}
