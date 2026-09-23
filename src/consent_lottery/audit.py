"""Audit finite mechanisms without trusting optimization slack variables."""
from itertools import combinations
import numpy as np
from .core import budgets


def audit(menu, P, epsilon, delta, enumerate_events=False):
    P = np.asarray(P, dtype=float)
    if P.shape != (2**menu.n, len(menu.contracts) + 1):
        raise ValueError("distribution shape mismatch")
    d = budgets(delta, menu.n)
    if not np.isfinite(epsilon) or epsilon < 0 or not np.isfinite(P).all():
        raise ValueError("nonfinite inputs or negative epsilon")
    max_divergence = max_excess = 0.
    witness = None
    edge_count = 0
    singleton_max = 0.
    event_disagreement = 0.
    for x in range(2**menu.n):
        for i in range(menu.n):
            y = x ^ (1 << i)
            diff = P[x] - np.exp(epsilon) * P[y]
            divergence = float(np.maximum(diff, 0).sum())
            singleton_max = max(singleton_max, float(diff.max()))
            edge_count += 1
            if divergence > max_divergence:
                max_divergence = divergence
                witness = {"from": x, "to": y, "agent": i,
                           "event": np.flatnonzero(diff > 1e-12).tolist()}
            max_excess = max(max_excess, divergence - d[i])
            if enumerate_events:
                event_max = max(sum(diff[j] for j in s)
                                for k in range(len(diff) + 1)
                                for s in combinations(range(len(diff)), k))
                event_disagreement = max(event_disagreement, abs(event_max - divergence))
    infeasible_mass = max(float(P[x, 1:][~menu.feasible(x)].sum()) for x in range(len(P)))
    return {"max_divergence": max_divergence, "max_privacy_excess": max_excess,
            "max_singleton_divergence": singleton_max, "witness": witness,
            "max_infeasible_mass": infeasible_mass,
            "max_normalization_error": float(np.abs(P.sum(axis=1) - 1).max()),
            "negative_mass": float(max(0, -P.min())), "directed_edges": edge_count,
            "event_enumeration_disagreement": event_disagreement}
