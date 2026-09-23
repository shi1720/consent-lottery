"""Contract menus and fixed lotteries. Masks encode private participation bits.

Column 0 is abstention; columns 1..m are public contract identifiers.
Lottery weights must be fixed without reading the current private profile.
"""
from dataclasses import dataclass
from typing import Tuple

import numpy as np
from scipy.optimize import linprog


@dataclass(frozen=True)
class Menu:
    n: int
    contracts: Tuple[int, ...]

    def __post_init__(self):
        if not isinstance(self.n, int) or self.n < 1:
            raise ValueError("n must be a positive integer")
        if not self.contracts or len(set(self.contracts)) != len(self.contracts):
            raise ValueError("contracts must be nonempty and distinct")
        if any(not isinstance(c, int) or c <= 0 or c >= 2**self.n for c in self.contracts):
            raise ValueError("each contract must be a nonempty subset of the agents")

    @property
    def incidence(self):
        return np.array([[(c >> i) & 1 for c in self.contracts]
                         for i in range(self.n)], dtype=float)

    def feasible(self, profile):
        if profile < 0 or profile >= 2**self.n:
            raise ValueError("profile out of range")
        return np.array([(c & profile) == c for c in self.contracts])


def budgets(delta, n):
    d = np.broadcast_to(np.asarray(delta, dtype=float), (n,)).copy()
    if not np.isfinite(d).all() or np.any(d < 0) or np.any(d > 1):
        raise ValueError("delta must be finite and between zero and one")
    return d


def packing(menu, delta, values=None, profile=None):
    """Solve the row polytope; also return a independently evaluated LP dual.

    If used as a fixed lottery, values and the design profile must be public.
    A profile-conditioned optimum is an upper bound, not automatically a
    privacy-preserving adaptive algorithm.
    """
    d = budgets(delta, menu.n)
    v = np.ones(len(menu.contracts)) if values is None else np.asarray(values, dtype=float)
    if v.shape != (len(menu.contracts),) or not np.isfinite(v).all() or (v < 0).any():
        raise ValueError("values must be finite, nonnegative, one per contract")
    A = np.vstack([menu.incidence, np.ones(len(v))])
    rhs = np.r_[d, 1.]
    allowed = np.ones(len(v), dtype=bool) if profile is None else menu.feasible(profile)
    bounds = [(0, None) if ok else (0, 0) for ok in allowed]
    result = linprog(-v, A_ub=A, b_ub=rhs, bounds=bounds, method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    # The restricted-column dual is min d.y + z, A.T y + z >= v.
    dual = linprog(rhs, A_ub=-A[:, allowed].T, b_ub=-v[allowed],
                   bounds=(0, None), method="highs") if allowed.any() else None
    return {"weights": result.x, "value": float(v @ result.x),
            "dual_value": float(dual.fun) if dual is not None else 0.,
            "dual": dual.x if dual is not None else np.zeros(menu.n + 1),
            "max_constraint_residual": float(max(0, np.max(A @ result.x - rhs)))}


def lottery(menu, weights, delta=None):
    """All-profile output distributions of one public draw, then private veto.

    No rejection sampling or private renormalization. On veto output only 0.
    """
    w = np.asarray(weights, dtype=float)
    if w.shape != (len(menu.contracts),) or not np.isfinite(w).all():
        raise ValueError("invalid weights")
    if w.min() < -1e-10 or w.sum() > 1 + 1e-10:
        raise ValueError("weights must form a subprobability distribution")
    if delta is not None and np.any(menu.incidence @ w > budgets(delta, menu.n) + 1e-10):
        raise ValueError("weights exceed a participation privacy budget")
    P = np.zeros((2**menu.n, len(w) + 1))
    for x in range(len(P)):
        P[x, 1:] = w * menu.feasible(x)
        P[x, 0] = 1 - P[x, 1:].sum()
    return P


def uniform_lottery(menu, delta):
    degrees = menu.incidence.sum(axis=1)
    d = budgets(delta, menu.n)
    amount = min(1 / len(menu.contracts), np.min(d[degrees > 0] / degrees[degrees > 0]))
    return np.full(len(menu.contracts), amount)


def profile_prior(n, q):
    """Public independent participation prior, in increasing mask order."""
    qs = np.broadcast_to(np.asarray(q, dtype=float), (n,))
    if not np.isfinite(qs).all() or (qs < 0).any() or (qs > 1).any():
        raise ValueError("invalid prior")
    return np.array([np.prod([qs[i] if x & (1 << i) else 1 - qs[i]
                             for i in range(n)]) for x in range(2**n)])
