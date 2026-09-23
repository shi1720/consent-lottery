from fractions import Fraction as F
from itertools import combinations
import numpy as np
import pytest

from consent_lottery import Menu, packing, lottery, uniform_lottery, profile_prior, audit, optimal_mechanism


def test_five_cycle_unique_optima_and_exact_obstruction():
    # Full optimum: each of five edges has mass delta/2.
    # Remove vertex 0: path edges (1,2), (2,3), (3,4).
    d = F(1, 10)
    full = [1 - 5*d/2] + [d/2]*5
    withdrawn = [1 - 2*d, 0, d, 0, d, 0]
    separating_event = (1, 3, 5)
    assert sum(full[j] for j in separating_event) == 3*d/2
    assert sum(withdrawn[j] for j in separating_event) == 0
    assert 3*d/2 > d
    menu = Menu(5, (3, 6, 12, 24, 17))
    assert packing(menu, .1, profile=31)['value'] == pytest.approx(.25)
    assert packing(menu, .1, profile=30)['value'] == pytest.approx(.2)


@pytest.mark.parametrize('epsilon', [0, np.log(2), np.log(10)])
def test_full_profile_bound_from_unrestricted_dp_lp(epsilon):
    menu = Menu(3, (3, 5, 6))
    prior = np.zeros(8); prior[-1] = 1
    result = optimal_mechanism(menu, epsilon, .2, prior)
    assert result['value'] == pytest.approx(.3)
    assert audit(menu, result['P'], epsilon, .2, True)['max_privacy_excess'] < 1e-8


def test_heterogeneous_budgets_weighted_target_row():
    menu = Menu(4, (3, 5, 10, 12, 15))
    delta = [.05, .1, .2, .3]
    values = [1, 2, 3, 4, 10]
    for target in (3, 7, 15):
        packed = packing(menu, delta, values=values, profile=target)
        P = lottery(menu, packed['weights'], delta)
        assert packed['value'] == pytest.approx(packed['dual_value'])
        assert audit(menu, P, 0, delta, True)['max_privacy_excess'] < 1e-8
        prior = np.zeros(16); prior[target] = 1
        unrestricted = optimal_mechanism(menu, 1, delta, prior, values)
        assert unrestricted['value'] == pytest.approx(packed['value'])


def test_singletons_do_not_certify_approximate_dp():
    menu = Menu(3, (3, 5))
    P = lottery(menu, [.1, .1])
    result = audit(menu, P, np.log(2), .1, True)
    assert result['max_singleton_divergence'] <= .1 + 1e-10
    assert result['max_divergence'] == pytest.approx(.2)
    assert result['event_enumeration_disagreement'] < 1e-12


def test_private_renormalization_breaks_privacy():
    menu = Menu(3, (3, 5, 6))
    P = lottery(menu, [.05]*3, .1)
    for x in range(len(P)):
        if P[x, 1:].sum() > 0:
            P[x, 1:] /= P[x, 1:].sum()
            P[x, 0] = 0
    assert audit(menu, P, 1, .1)['max_divergence'] == pytest.approx(1)


def test_repeated_draws_have_more_privacy_loss():
    # A sole feasible contract fires with delta per independent trial.
    d = F(1, 10)
    once = d
    twice = 1 - (1-d)**2
    assert twice == F(19, 100) and twice > once


@pytest.mark.parametrize('bad', [(-1,), (0,), (8,), (1, 1)])
def test_invalid_menu_rejected(bad):
    with pytest.raises(ValueError): Menu(3, bad)


def test_empty_and_public_prior_boundary():
    menu = Menu(2, (1, 2, 3))
    assert packing(menu, .1, profile=0)['value'] == 0
    assert profile_prior(2, 0).tolist() == [1, 0, 0, 0]
    assert profile_prior(2, 1).tolist() == [0, 0, 0, 1]
    assert np.isclose(profile_prior(2, [.2, .7]).sum(), 1)


def test_pointwise_reoptimization_fails_cycle():
    menu = Menu(5, (3, 6, 12, 24, 17))
    P = np.array([lottery(menu, packing(menu, .1, profile=x)['weights'])[x]
                  for x in range(32)])
    assert audit(menu, P, 0, .1)['max_privacy_excess'] >= .05 - 1e-9


def test_fixed_lottery_endpoint_tradeoff():
    menu = Menu(5, (3, 6, 12, 24, 17))
    P = lottery(menu, [.05]*5, .1)
    prior = np.zeros(32)
    for i in range(5): prior[31 ^ (1 << i)] = .2
    result = optimal_mechanism(menu, 0, .1, prior, full_row=P[-1])
    assert result['value'] == pytest.approx(.15)


def test_invalid_lottery_and_budget_rejected():
    menu = Menu(2, (1, 2))
    for w in ([-.1, .1], [.6, .6], [float('nan'), 0], [.1]):
        with pytest.raises(ValueError): lottery(menu, w)
    with pytest.raises(ValueError): lottery(menu, [.2, .2], .1)
    with pytest.raises(ValueError): packing(menu, -.1)


def test_zero_privacy_requires_abstention():
    menu = Menu(3, (1, 3, 7))
    prior = profile_prior(3, .8)
    assert optimal_mechanism(menu, 3, 0, prior)['value'] == pytest.approx(0)


def test_auditor_catches_feasibility_and_normalization():
    menu = Menu(2, (3,))
    P = np.zeros((4, 2)); P[:, 0] = 1
    P[0, 1] = .1
    result = audit(menu, P, 0, .1)
    assert result['max_infeasible_mass'] == .1
    assert result['max_normalization_error'] == pytest.approx(.1)
