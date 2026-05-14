import os
import re

def ensure_dir(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

def write_file(file_path, content):
    ensure_dir(file_path)
    with open(file_path, 'w') as f:
        f.write(content)

# ---------------------------------------------------------
# REPORTING (cost_robustness/robustness_reporting.py)
# ---------------------------------------------------------
reporting_content = """
from typing import Any, Dict
from usa_signal_bot.cost_robustness.robustness_models import (
    CostStressScenario, CostStressedTradeResult, CostStressedBacktestResult,
    ExecutionSensitivityMatrix, WalkForwardCostRobustnessResult, CostFragilityAssessment, CostRobustnessReview
)
from usa_signal_bot.cost_robustness.stress_scenarios import stress_scenarios_to_text
from usa_signal_bot.cost_robustness.stressed_results import stressed_trade_results_to_text, stressed_backtest_result_to_text
from usa_signal_bot.cost_robustness.sensitivity_matrix import execution_sensitivity_matrix_to_text
from usa_signal_bot.cost_robustness.walk_forward_cost_robustness import walk_forward_cost_robustness_to_text
from usa_signal_bot.cost_robustness.fragility_detector import cost_fragility_assessment_to_text

def cost_stress_scenario_to_text(item: CostStressScenario) -> str:
    return stress_scenarios_to_text([item])

def cost_stressed_trade_result_to_text(item: CostStressedTradeResult) -> str:
    return stressed_trade_results_to_text([item])

def cost_stressed_backtest_result_to_text(item: CostStressedBacktestResult) -> str:
    return stressed_backtest_result_to_text(item)

def cost_robustness_review_to_text(item: CostRobustnessReview, limit: int = 100) -> str:
    lines = [
        "========================================",
        "COST ROBUSTNESS REVIEW",
        "========================================",
        f"Review ID: {item.review_id}",
        f"Report Type: {item.report_type.value}",
        f"Created At: {item.created_at_utc}",
        ""
    ]
    if item.fragility_assessment:
        lines.append(cost_fragility_assessment_to_text(item.fragility_assessment))
        lines.append("")
    if item.sensitivity_matrix:
        lines.append(execution_sensitivity_matrix_to_text(item.sensitivity_matrix, limit))
        lines.append("")
    if item.walk_forward_result:
        lines.append(walk_forward_cost_robustness_to_text(item.walk_forward_result, limit))
        lines.append("")

    lines.append(cost_robustness_limitations_text())
    return "\\n".join(lines)

def robustness_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Robustness Store Summary: {summary}"

def cost_robustness_limitations_text() -> str:
    return (
        "\\n*** IMPORTANT LIMITATIONS & DISCLAIMERS ***\\n"
        "- This is a purely local heuristic cost simulation.\\n"
        "- No real broker, no live orders, no real order book.\\n"
        "- A PASS status is NOT a live execution approval.\\n"
        "- NOT investment advice. Does not guarantee real fill performance.\\n"
        "*********************************************"
    )
"""
write_file("usa_signal_bot/cost_robustness/robustness_reporting.py", reporting_content)

# ---------------------------------------------------------
# CLI & HEALTH (app/cli.py, core/health.py modifications placeholder)
# ---------------------------------------------------------
# We will create placeholder files or append to them
cli_patch = """
import click
from usa_signal_bot.cost_robustness.stress_scenarios import default_cost_stress_scenarios, stress_scenarios_to_text
from usa_signal_bot.cost_robustness.slippage_stress import build_slippage_stress_scenarios, slippage_stress_summary_to_text
from usa_signal_bot.cost_robustness.spread_stress import build_spread_stress_scenarios, spread_stress_summary_to_text
from usa_signal_bot.cost_robustness.impact_stress import build_market_impact_stress_scenarios, impact_stress_summary_to_text
from usa_signal_bot.cost_robustness.fee_stress import build_fee_stress_scenarios, fee_stress_summary_to_text
from usa_signal_bot.cost_robustness.participation_stress import build_participation_stress_scenarios, participation_stress_summary_to_text
from usa_signal_bot.cost_robustness.fill_realism_stress import build_fill_realism_stress_scenarios
from usa_signal_bot.cost_robustness.sensitivity_matrix import run_execution_sensitivity_matrix, execution_sensitivity_matrix_to_text
from usa_signal_bot.cost_robustness.walk_forward_cost_robustness import evaluate_walk_forward_cost_robustness, walk_forward_cost_robustness_to_text
from usa_signal_bot.cost_robustness.fragility_detector import detect_cost_fragility, cost_fragility_assessment_to_text
from usa_signal_bot.cost_robustness.breakeven_costs import breakeven_costs_to_text
from usa_signal_bot.cost_robustness.robustness_store import robustness_store_summary
from usa_signal_bot.cost_robustness.robustness_validation import validate_no_live_execution_language_in_cost_robustness, cost_robustness_validation_report_to_text
from pathlib import Path

# Add CLI commands here in the actual app/cli.py
"""
write_file("usa_signal_bot/cost_robustness/__init__.py", "")
