"""G1′ (c) travel-notch control: exact values and estimator interface."""
import numpy as np

from touchbed import notch as N
from touchbed.lookahead import lookahead_gap
from touchbed.travel_notch import TravelNotchProblem, costs, exact_values


def test_costs_and_feasibility():
    P = TravelNotchProblem(12.0)
    b = P.start()
    c = costs(0.0, 12.0)
    assert c[N.H_ACT] == 1.0 and np.allclose(c[:N.H_ACT], 13.0)
    assert P.feasible(b).all()
    bv = P.step_budget(b, 0)              # vertical first: 1 stroke left, only verticals reachable
    assert abs(bv.tau_rem - 1.0) < 1e-12 and not P.feasible(bv)[N.H_ACT] and P.feasible(bv)[:N.H_ACT].all()
    bh = P.step_budget(b, N.H_ACT)        # horizontal first: 13 left, everything reachable
    assert abs(bh.tau_rem - 13.0) < 1e-12 and P.feasible(bh).all()
    assert not P.budget_left(P.step_budget(bv, 0))


def test_exact_gap_has_travel_structure():
    ex = exact_values(12.0)
    assert ex["a_opt_is_horizontal"] and ex["a_greedy"] != N.H_ACT
    assert ex["gap_rel"] >= 0.10              # the G1′ (c) precondition on the exact value


def test_estimator_runs_on_travel_notch():
    P = TravelNotchProblem(12.0)
    r = lookahead_gap(P, np.log(N.prior_belief()), P.start(), seed=3, C1=6, M_outer=4, top=2, reest=1, greedy_M=8)
    assert np.isfinite(r["v_la"]) and r["a_greedy"] != N.H_ACT
