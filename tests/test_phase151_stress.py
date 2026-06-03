import pytest
import pandas as pd
from usa_signal_bot.backtesting.stress_robustness.walk_forward_ingestion import ingest_walk_forward_review_payload
from usa_signal_bot.backtesting.stress_robustness.stress_scenario_policy import build_default_stress_scenario_policy
from usa_signal_bot.backtesting.stress_robustness.price_shock_scenarios import build_price_shock_scenarios
from usa_signal_bot.backtesting.stress_robustness.scenario_path_builder import build_scenario_paths
from usa_signal_bot.backtesting.stress_robustness.scenario_replay_runner import run_scenario_replays
from usa_signal_bot.backtesting.stress_robustness.monte_carlo_policy import build_default_monte_carlo_policy
from usa_signal_bot.backtesting.stress_robustness.monte_carlo_path_generator import build_monte_carlo_paths
from usa_signal_bot.backtesting.stress_robustness.monte_carlo_replay_runner import run_monte_carlo_replays
from usa_signal_bot.backtesting.stress_robustness.monte_carlo_distribution_analyzer import build_monte_carlo_distribution_summary

def test_ingest_payload():
    payload = {
        "review_id": "rev1",
        "context": {
            "ready_for_phase151": True,
            "safety_boundary_validated": True,
            "phase151_readiness_gate_passed": True,
            "research_data_only": True,
            "walk_forward_executed": True
        }
    }
    res = ingest_walk_forward_review_payload(payload)
    assert res.valid_for_phase151 is True

def test_stress_scenario_pipeline():
    policy = build_default_stress_scenario_policy()
    scenarios = build_price_shock_scenarios(policy)
    assert len(scenarios) > 0

    df = pd.DataFrame({"return": [0.01, -0.02, 0.03, -0.01, 0.02]})
    paths = build_scenario_paths(scenarios, df)
    assert len(paths) == len(scenarios)

    results = run_scenario_replays(scenarios, paths)
    assert len(results) == len(scenarios)
    assert results[0].simulated_only is True
    assert results[0].broker_execution_used is False

def test_monte_carlo_pipeline():
    policy = build_default_monte_carlo_policy()
    policy.path_count = 10 # speed up

    df = pd.DataFrame({"return": [0.01, -0.02, 0.03, -0.01, 0.02]})
    paths = build_monte_carlo_paths(df, policy)
    assert len(paths) == 10

    results = run_monte_carlo_replays(paths)
    assert len(results) == 10
    assert results[0].simulated_only is True

    dist = build_monte_carlo_distribution_summary(results)
    assert dist.summary_valid is True
    assert dist.not_investment_advice is True
