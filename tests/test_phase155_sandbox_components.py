import pytest
import pandas as pd
from usa_signal_bot.portfolio.construction.portfolio_construction_policy import build_default_portfolio_construction_policy
from usa_signal_bot.portfolio.construction.sandbox_allocation_method_contracts import build_sandbox_allocation_method_contracts
from usa_signal_bot.portfolio.construction.sandbox_candidate_builder import build_portfolio_sandbox_candidates
from usa_signal_bot.portfolio.construction.equal_sandbox_allocation import build_equal_sandbox_allocation
from usa_signal_bot.portfolio.construction.prototype_exposure_table import build_prototype_exposure_table
from usa_signal_bot.portfolio.construction.constraint_normalization_engine import normalize_sandbox_allocation_results
from usa_signal_bot.portfolio.construction.allocation_sandbox_safety_boundary import build_allocation_sandbox_safety_boundary_rules, build_allocation_sandbox_safety_boundary_result

def test_build_policy():
    policy = build_default_portfolio_construction_policy()
    assert policy.actual_target_weights_allowed is False
    assert policy.capital_deployment_allowed is False

def test_method_contracts():
    policy = build_default_portfolio_construction_policy()
    contracts = build_sandbox_allocation_method_contracts(policy)
    assert len(contracts) == 4
    for c in contracts:
        assert c.produces_sandbox_prototype_weight is True
        assert c.produces_actual_allocation is False
        assert c.produces_actual_target_weight is False

def test_equal_allocation_and_exposure():
    policy = build_default_portfolio_construction_policy()

    matrix_payload = {
        "matrix": {
            "AAPL": {"eligible": True},
            "MSFT": {"eligible": True}
        }
    }

    cands = build_portfolio_sandbox_candidates(matrix_payload)
    assert len(cands) == 2

    res = build_equal_sandbox_allocation(cands, policy)
    assert len(res) == 2
    assert res[0].sandbox_prototype_weight == 0.5

    norm = normalize_sandbox_allocation_results(res, policy)
    assert norm[0].normalized_sandbox_weight == 0.1  # default cap is 0.1

    table = build_prototype_exposure_table(norm, cands)
    assert table.no_actual_allocation is True
    assert len(table.records) == 2

def test_safety_boundary():
    rules = build_allocation_sandbox_safety_boundary_rules()
    bound = build_allocation_sandbox_safety_boundary_result(rules)
    assert bound.boundary_passed is True
    assert bound.no_actual_allocation is True
    assert bound.no_capital_deployment is True
    assert bound.no_broker_execution is True

def test_unsafe_boundary():
    rules = build_allocation_sandbox_safety_boundary_rules({"actual_target_weights_produced": True})
    bound = build_allocation_sandbox_safety_boundary_result(rules)
    assert bound.boundary_passed is False
